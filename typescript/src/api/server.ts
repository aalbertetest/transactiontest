import express, { Request, Response } from "express";

import { config } from "../common/config.js";
import { hashRequest } from "../common/idempotency.js";
import { store } from "../common/store.js";

type RequestWithRawBody = Request & { rawBody?: Buffer };

const app = express();
app.use(
  express.json({
    verify: (req, _res, buf) => {
      (req as RequestWithRawBody).rawBody = buf;
    }
  })
);

if (store.merchants.size === 0) {
  store.addMerchant("Demo Merchant", config.apiKey);
}

const authenticate = (req: Request, res: Response) => {
  const auth = req.header("Authorization") ?? "";
  if (!auth.startsWith("Bearer ")) {
    res.status(401).json({ error: "unauthorized" });
    return undefined;
  }
  const apiKey = auth.replace("Bearer ", "").trim();
  const merchant = store.getMerchantByApiKey(apiKey);
  if (!merchant) {
    res.status(401).json({ error: "unauthorized" });
    return undefined;
  }
  return merchant;
};

const requireIdempotencyKey = (req: Request, res: Response) => {
  const key = req.header("Idempotency-Key");
  if (!key) {
    res.status(400).json({ error: "missing Idempotency-Key" });
    return undefined;
  }
  return key;
};

const handleIdempotency = (
  res: Response,
  merchantId: string,
  key: string,
  requestHash: string
) => {
  const record = store.getIdempotency(merchantId, key);
  if (!record) return undefined;
  if (record.requestHash !== requestHash) {
    res.status(409).json({ error: "idempotency key reuse with different payload" });
    return "conflict";
  }
  res.status(record.statusCode).set("Content-Type", "application/json").send(record.responseBody);
  return "replayed";
};

const writeIdempotentResponse = (
  res: Response,
  merchantId: string,
  key: string,
  requestHash: string,
  payload: unknown,
  status: number
) => {
  const responseBody = JSON.stringify(payload);
  store.setIdempotency(merchantId, key, requestHash, responseBody, status);
  res.status(status).json(payload);
};

app.post("/v1/payment_intents", (req: RequestWithRawBody, res) => {
  const merchant = authenticate(req, res);
  if (!merchant) return;
  const idempotencyKey = requireIdempotencyKey(req, res);
  if (!idempotencyKey) return;
  const rawBody = req.rawBody ?? Buffer.from("");
  const requestHash = hashRequest(req.path, rawBody);
  if (handleIdempotency(res, merchant.id, idempotencyKey, requestHash)) return;

  const payload = req.body ?? {};
  if (!payload.amount || !payload.currency || !payload.payment_method_token) {
    res.status(400).json({ error: "invalid request" });
    return;
  }
  const intent = store.createPaymentIntent(merchant.id, {
    amount: payload.amount,
    currency: String(payload.currency).toUpperCase(),
    customerId: payload.customer_id,
    paymentMethodToken: payload.payment_method_token,
    captureMethod: payload.capture_method ?? "automatic",
    metadata: payload.metadata ?? {},
    returnUrl: payload.return_url
  });
  writeIdempotentResponse(
    res,
    merchant.id,
    idempotencyKey,
    requestHash,
    {
      id: intent.id,
      status: intent.status,
      amount: intent.amount,
      currency: intent.currency,
      client_secret: intent.clientSecret
    },
    200
  );
});

app.post("/v1/payment_intents/:id/confirm", (req: RequestWithRawBody, res) => {
  const merchant = authenticate(req, res);
  if (!merchant) return;
  const idempotencyKey = requireIdempotencyKey(req, res);
  if (!idempotencyKey) return;
  const rawBody = req.rawBody ?? Buffer.from("");
  const requestHash = hashRequest(req.path, rawBody);
  if (handleIdempotency(res, merchant.id, idempotencyKey, requestHash)) return;

  const intent = store.getPaymentIntent(req.params.id);
  if (!intent || intent.merchantId !== merchant.id) {
    res.status(404).json({ error: "not found" });
    return;
  }
  if (!["requires_confirmation", "processing"].includes(intent.status)) {
    writeIdempotentResponse(
      res,
      merchant.id,
      idempotencyKey,
      requestHash,
      { id: intent.id, status: intent.status, charge_id: intent.chargeId },
      200
    );
    return;
  }
  store.updatePaymentIntent(intent.id, { status: "processing" });
  store.enqueueTask({ type: "process_payment", intentId: intent.id });
  writeIdempotentResponse(
    res,
    merchant.id,
    idempotencyKey,
    requestHash,
    { id: intent.id, status: "processing" },
    202
  );
});

app.get("/v1/payment_intents/:id", (req, res) => {
  const merchant = authenticate(req, res);
  if (!merchant) return;
  const intent = store.getPaymentIntent(req.params.id);
  if (!intent || intent.merchantId !== merchant.id) {
    res.status(404).json({ error: "not found" });
    return;
  }
  res.json({
    id: intent.id,
    status: intent.status,
    amount: intent.amount,
    currency: intent.currency,
    client_secret: intent.clientSecret,
    charge_id: intent.chargeId
  });
});

app.post("/v1/charges/:id/refunds", (req: RequestWithRawBody, res) => {
  const merchant = authenticate(req, res);
  if (!merchant) return;
  const idempotencyKey = requireIdempotencyKey(req, res);
  if (!idempotencyKey) return;
  const rawBody = req.rawBody ?? Buffer.from("");
  const requestHash = hashRequest(req.path, rawBody);
  if (handleIdempotency(res, merchant.id, idempotencyKey, requestHash)) return;

  const charge = store.getCharge(req.params.id);
  if (!charge) {
    res.status(404).json({ error: "charge not found" });
    return;
  }
  const refundAmount = req.body?.amount ?? charge.amount;
  const refund = store.createRefund(charge.id, refundAmount, "succeeded");
  store.createEvent(merchant.id, "charge.refunded", {
    id: refund.id,
    charge_id: charge.id,
    amount: refund.amount
  });
  writeIdempotentResponse(
    res,
    merchant.id,
    idempotencyKey,
    requestHash,
    {
      id: refund.id,
      status: refund.status,
      amount: refund.amount,
      charge_id: charge.id
    },
    200
  );
});

app.post("/v1/webhook_endpoints", (req: RequestWithRawBody, res) => {
  const merchant = authenticate(req, res);
  if (!merchant) return;
  const idempotencyKey = requireIdempotencyKey(req, res);
  if (!idempotencyKey) return;
  const rawBody = req.rawBody ?? Buffer.from("");
  const requestHash = hashRequest(req.path, rawBody);
  if (handleIdempotency(res, merchant.id, idempotencyKey, requestHash)) return;

  const payload = req.body ?? {};
  if (!payload.url) {
    res.status(400).json({ error: "invalid request" });
    return;
  }
  const endpoint = store.addWebhookEndpoint(merchant.id, payload.url, payload.enabled ?? true);
  writeIdempotentResponse(
    res,
    merchant.id,
    idempotencyKey,
    requestHash,
    { id: endpoint.id, url: endpoint.url, enabled: endpoint.enabled },
    200
  );
});

app.get("/v1/events", (req, res) => {
  const merchant = authenticate(req, res);
  if (!merchant) return;
  res.json(store.listEvents(merchant.id));
});

app.listen(config.apiPort, () => {
  console.log(`API listening on :${config.apiPort}`);
});
