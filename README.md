# Payment Processing System (Python, Go, TypeScript)

This repository provides a production-grade reference implementation of a
payment processing system in **Python**, **Go**, and **TypeScript** with:

- PCI concepts and scope minimization
- Idempotency, retries, and backoff
- Webhooks with signing
- Fraud detection pipeline
- Schemas (Postgres, OpenAPI, webhook JSON)
- API + worker separation

> NOTE: The code uses an in-memory store to keep the sample runnable. The
> interfaces are designed to be swapped with Postgres + Redis/queue in a real
> production deployment. See `schemas/postgres.sql` for the intended schema.

## Repository layout

```
docs/                Architecture and API notes
schemas/             SQL + JSON schemas + OpenAPI
python/              FastAPI API service + worker
go/                  net/http API service + worker
typescript/          Express API service + worker
```

## PCI concepts covered

- No PAN/CVV storage: only tokenized payment_method_token is accepted.
- Tokenization: card data handled by a PCI-compliant vault/hosted flow.
- Segmentation and least privilege (documented in architecture).
- Webhook signing and key rotation (modeled via config).

## API quickstart (Python)

```
cd python
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export API_KEY=test_key_123
uvicorn app.main:app --reload
```

Worker (same process for demo or separate):
```
PYTHONPATH=. python worker/main.py
```

## API quickstart (Go)

```
cd go
export API_KEY=test_key_123
go run ./cmd/api
```

Start the worker in the same process:
```
START_WORKER=true go run ./cmd/api
```

Or separately (note: in-memory store is per-process):
```
go run ./cmd/worker
```

## API quickstart (TypeScript)

```
cd typescript
npm install
export API_KEY=test_key_123
npm run dev
```

Worker (same memory caveat):
```
npm run worker
```

## Core endpoints

- `POST /v1/payment_intents` (Idempotency-Key required)
- `POST /v1/payment_intents/{id}/confirm` (Idempotency-Key required)
- `GET /v1/payment_intents/{id}`
- `POST /v1/charges/{id}/refunds` (Idempotency-Key required)
- `POST /v1/webhook_endpoints` (Idempotency-Key required)
- `GET /v1/events`

See `docs/api.md` and `schemas/openapi.yaml` for details.

## Webhook signing

Webhooks are signed with:

```
Payment-Signature: t=<unix_ts>,v1=<hex_hmac>
```

Secret key is `WEBHOOK_SIGNING_SECRET`.

## Fraud detection

The risk engine applies:

- High-amount thresholds
- Unsupported currency checks
- Guest checkout risk

Results are persisted as fraud assessments and used to block or allow charges.

