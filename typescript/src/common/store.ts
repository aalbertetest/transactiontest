import { randomBytes } from "crypto";

export type Merchant = {
  id: string;
  name: string;
  apiKey: string;
};

export type PaymentIntent = {
  id: string;
  merchantId: string;
  amount: number;
  currency: string;
  customerId?: string;
  paymentMethodToken: string;
  captureMethod: string;
  metadata: Record<string, string>;
  returnUrl?: string;
  status: string;
  clientSecret: string;
  chargeId?: string;
  processorReference?: string;
  createdAt: string;
  updatedAt: string;
};

export type Charge = {
  id: string;
  paymentIntentId: string;
  amount: number;
  currency: string;
  status: string;
  createdAt: string;
};

export type Refund = {
  id: string;
  chargeId: string;
  amount: number;
  status: string;
  createdAt: string;
};

export type WebhookEndpoint = {
  id: string;
  merchantId: string;
  url: string;
  enabled: boolean;
  createdAt: string;
};

export type Event = {
  id: string;
  merchantId: string;
  type: string;
  createdAt: string;
  data: Record<string, unknown>;
  status: string;
};

export type FraudAssessment = {
  id: string;
  paymentIntentId: string;
  riskScore: number;
  decision: string;
  signals: Record<string, unknown>;
  createdAt: string;
};

export type IdempotencyRecord = {
  requestHash: string;
  responseBody: string;
  statusCode: number;
  createdAt: string;
};

export type Task = { type: "process_payment" | "deliver_webhooks"; intentId?: string; eventId?: string };

const generateId = (prefix: string) => `${prefix}_${randomBytes(12).toString("hex")}`;
const utcNow = () => new Date().toISOString();

export class InMemoryStore {
  merchants = new Map<string, Merchant>();
  paymentIntents = new Map<string, PaymentIntent>();
  charges = new Map<string, Charge>();
  refunds = new Map<string, Refund>();
  idempotency = new Map<string, IdempotencyRecord>();
  webhookEndpoints = new Map<string, WebhookEndpoint>();
  events = new Map<string, Event>();
  fraudAssessments = new Map<string, FraudAssessment>();
  tasks: Task[] = [];

  addMerchant(name: string, apiKey: string): Merchant {
    const merchant: Merchant = { id: generateId("mch"), name, apiKey };
    this.merchants.set(merchant.id, merchant);
    return merchant;
  }

  getMerchantByApiKey(apiKey: string): Merchant | undefined {
    for (const merchant of this.merchants.values()) {
      if (merchant.apiKey === apiKey) return merchant;
    }
    return undefined;
  }

  getIdempotency(merchantId: string, key: string): IdempotencyRecord | undefined {
    return this.idempotency.get(`${merchantId}:${key}`);
  }

  setIdempotency(
    merchantId: string,
    key: string,
    requestHash: string,
    responseBody: string,
    statusCode: number
  ) {
    this.idempotency.set(`${merchantId}:${key}`, {
      requestHash,
      responseBody,
      statusCode,
      createdAt: utcNow()
    });
  }

  createPaymentIntent(merchantId: string, payload: Omit<PaymentIntent, "id" | "merchantId" | "status" | "clientSecret" | "createdAt" | "updatedAt">): PaymentIntent {
    const id = generateId("pi");
    const intent: PaymentIntent = {
      ...payload,
      id,
      merchantId,
      status: "requires_confirmation",
      clientSecret: `${id}_secret_${randomBytes(6).toString("hex")}`,
      createdAt: utcNow(),
      updatedAt: utcNow()
    };
    this.paymentIntents.set(id, intent);
    return intent;
  }

  getPaymentIntent(id: string): PaymentIntent | undefined {
    return this.paymentIntents.get(id);
  }

  updatePaymentIntent(id: string, updates: Partial<PaymentIntent>): PaymentIntent | undefined {
    const intent = this.paymentIntents.get(id);
    if (!intent) return undefined;
    const updated = { ...intent, ...updates, updatedAt: utcNow() };
    this.paymentIntents.set(id, updated);
    return updated;
  }

  createCharge(intentId: string, amount: number, currency: string, status: string): Charge {
    const charge: Charge = {
      id: generateId("ch"),
      paymentIntentId: intentId,
      amount,
      currency,
      status,
      createdAt: utcNow()
    };
    this.charges.set(charge.id, charge);
    return charge;
  }

  getCharge(id: string): Charge | undefined {
    return this.charges.get(id);
  }

  createRefund(chargeId: string, amount: number, status: string): Refund {
    const refund: Refund = {
      id: generateId("rf"),
      chargeId,
      amount,
      status,
      createdAt: utcNow()
    };
    this.refunds.set(refund.id, refund);
    return refund;
  }

  addWebhookEndpoint(merchantId: string, url: string, enabled: boolean): WebhookEndpoint {
    const endpoint: WebhookEndpoint = {
      id: generateId("we"),
      merchantId,
      url,
      enabled,
      createdAt: utcNow()
    };
    this.webhookEndpoints.set(endpoint.id, endpoint);
    return endpoint;
  }

  listWebhookEndpoints(merchantId: string): WebhookEndpoint[] {
    return [...this.webhookEndpoints.values()].filter(
      (endpoint) => endpoint.merchantId === merchantId && endpoint.enabled
    );
  }

  createEvent(merchantId: string, type: string, data: Record<string, unknown>): Event {
    const event: Event = {
      id: generateId("evt"),
      merchantId,
      type,
      createdAt: utcNow(),
      data,
      status: "pending"
    };
    this.events.set(event.id, event);
    this.tasks.push({ type: "deliver_webhooks", eventId: event.id });
    return event;
  }

  updateEventStatus(eventId: string, status: string) {
    const event = this.events.get(eventId);
    if (!event) return;
    this.events.set(eventId, { ...event, status });
  }

  listEvents(merchantId: string): Event[] {
    return [...this.events.values()].filter((event) => event.merchantId === merchantId);
  }

  createFraudAssessment(
    intentId: string,
    riskScore: number,
    decision: string,
    signals: Record<string, unknown>
  ) {
    const assessment: FraudAssessment = {
      id: generateId("fra"),
      paymentIntentId: intentId,
      riskScore,
      decision,
      signals,
      createdAt: utcNow()
    };
    this.fraudAssessments.set(assessment.id, assessment);
    return assessment;
  }

  enqueueTask(task: Task) {
    this.tasks.push(task);
  }

  dequeueTask(): Task | undefined {
    return this.tasks.shift();
  }
}

export const store = new InMemoryStore();
