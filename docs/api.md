# API Reference (Summary)

All endpoints use JSON. POST endpoints require Idempotency-Key.

## Authentication

Use an API key in the Authorization header:

```
Authorization: Bearer <api_key>
```

## Endpoints

### Create PaymentIntent

`POST /v1/payment_intents`

Request:
```
{
  "amount": 1299,
  "currency": "USD",
  "customer_id": "cus_123",
  "payment_method_token": "pm_tok_abc",
  "capture_method": "automatic",
  "metadata": {"order_id": "A-1001"},
  "return_url": "https://merchant.example/return"
}
```

Response:
```
{
  "id": "pi_123",
  "status": "requires_confirmation",
  "client_secret": "pi_123_secret_456"
}
```

### Confirm PaymentIntent

`POST /v1/payment_intents/{id}/confirm`

Response:
```
{
  "id": "pi_123",
  "status": "succeeded",
  "charge_id": "ch_789"
}
```

### Get PaymentIntent

`GET /v1/payment_intents/{id}`

### Refund Charge

`POST /v1/charges/{id}/refunds`

### Create Webhook Endpoint

`POST /v1/webhook_endpoints`

### List Events

`GET /v1/events`

## Webhook events

Event payloads are signed with HMAC-SHA256.

Headers:
- `Payment-Signature: t=<unix_ts>,v1=<hex_hmac>`

Events:
- `payment_intent.succeeded`
- `payment_intent.failed`
- `charge.refunded`

