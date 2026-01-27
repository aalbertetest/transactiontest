## API Guide

This guide describes:

- REST endpoints (OpenAPI)
- gRPC services (protobuf)
- Example requests and responses

Canonical specifications live in:

- `apis/openapi/`
- `apis/proto/`

---

## REST (OpenAPI)

The gateway exposes a unified REST surface.

- Spec: `apis/openapi/gateway.yaml`

### Conventions

- All requests are scoped to a tenant via either:
  - `X-Tenant-Id` header (server-to-server), or
  - token claims `tid` (end-user tokens)
- Correlation headers:
  - `X-Request-Id` (optional; server generates if missing)
  - `Traceparent` (W3C trace context)
- Idempotency:
  - `Idempotency-Key` for POST/PUT/PATCH/DELETE where relevant

### Example: Create payment intent

Request:

```bash
curl -X POST "http://localhost:8080/v1/payments/intents" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Idempotency-Key: 7a1c9f7a-0b4b-4df9-9d3b-6b00c6f4e4f0" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 1999,
    "currency": "USD",
    "customer_id": "cus_123",
    "description": "Example purchase"
  }'
```

Response:

```json
{
  "id": "pi_01HZY0M5B8R9W1",
  "status": "REQUIRES_CONFIRMATION",
  "amount": 1999,
  "currency": "USD",
  "customer_id": "cus_123",
  "created_at": "2026-01-27T00:00:00Z"
}
```

### Example: Start workflow

```bash
curl -X POST "http://localhost:8080/v1/workflows/start" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -H "Idempotency-Key: 0f5b3a3e-8c5b-4a3e-a4f9-2cbe4c4d6a55" \
  -H "Content-Type: application/json" \
  -d '{
    "workflow_type": "payment_capture",
    "workflow_id": "wf_capture_pi_01HZY0M5B8R9W1",
    "input": {"payment_intent_id": "pi_01HZY0M5B8R9W1"}
  }'
```

---

## gRPC (protobuf)

The platform exposes gRPC for:

- internal service-to-service calls
- high-throughput control-plane operations

Protobufs live in `apis/proto/`.

### gRPC metadata conventions

- `x-tenant-id`: tenant scope
- `x-request-id`: correlation ID
- `x-idempotency-key`: idempotency (where relevant)

