import { config } from "../common/config.js";
import { evaluateFraud } from "../common/fraud.js";
import { ProcessorClient, ProcessorDeclinedError, RetryableProcessorError } from "../common/processor.js";
import { withRetries } from "../common/retry.js";
import { store } from "../common/store.js";
import { deliverWebhook } from "../common/webhooks.js";

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

const processPayment = async (intentId: string) => {
  const intent = store.getPaymentIntent(intentId);
  if (!intent || intent.status !== "processing") return;

  const { score, decision, signals } = evaluateFraud(intent);
  store.createFraudAssessment(intent.id, score, decision, signals);

  if (decision === "block") {
    store.updatePaymentIntent(intent.id, { status: "failed" });
    store.createEvent(intent.merchantId, "payment_intent.failed", {
      id: intent.id,
      status: "failed",
      reason: "fraud_block"
    });
    return;
  }

  const processor = new ProcessorClient();
  try {
    const reference = await withRetries(
      async () => processor.authorize(intent.amount, intent.paymentMethodToken),
      config.maxRetryAttempts,
      config.baseBackoffMs,
      (err) => err instanceof RetryableProcessorError
    );
    const charge = store.createCharge(intent.id, intent.amount, intent.currency, "succeeded");
    store.updatePaymentIntent(intent.id, {
      status: "succeeded",
      chargeId: charge.id,
      processorReference: reference
    });
    store.createEvent(intent.merchantId, "payment_intent.succeeded", {
      id: intent.id,
      status: "succeeded",
      charge_id: charge.id
    });
  } catch (error) {
    const reason = error instanceof ProcessorDeclinedError ? "declined" : "processor_unavailable";
    store.updatePaymentIntent(intent.id, { status: "failed" });
    store.createEvent(intent.merchantId, "payment_intent.failed", {
      id: intent.id,
      status: "failed",
      reason
    });
  }
};

const deliverWebhooks = async (eventId: string) => {
  const event = store.events.get(eventId);
  if (!event) return;
  const payload = {
    id: event.id,
    type: event.type,
    created_at: event.createdAt,
    data: event.data
  };
  const endpoints = store.listWebhookEndpoints(event.merchantId);
  for (const endpoint of endpoints) {
    try {
      await withRetries(
        () => deliverWebhook(endpoint.url, config.webhookSigningSecret, payload),
        config.maxRetryAttempts,
        config.baseBackoffMs,
        () => true
      );
    } catch {
      store.updateEventStatus(event.id, "failed");
      return;
    }
  }
  store.updateEventStatus(event.id, "delivered");
};

const runWorker = async () => {
  while (true) {
    const task = store.dequeueTask();
    if (!task) {
      await sleep(config.workerPollIntervalMs);
      continue;
    }
    if (task.type === "process_payment" && task.intentId) {
      await processPayment(task.intentId);
    }
    if (task.type === "deliver_webhooks" && task.eventId) {
      await deliverWebhooks(task.eventId);
    }
  }
};

runWorker();
