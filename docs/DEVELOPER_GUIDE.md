## Developer Guide

This guide explains how to work on DSP locally and how the repository is organized for polyglot service implementations.

---

## Repository model

DSP is a monorepo with:

- shared API contracts (`apis/openapi`, `apis/proto`)
- shared libraries per language (`libs/python`, `libs/go`, `libs/typescript`)
- service implementations per language (`services/<service>/<language>`)

Each service implementation includes:

- server
- client SDK
- config loader
- structured logging
- metrics
- retry logic + timeouts
- concurrency handling
- error handling
- data models + validation
- middleware/interceptors

---

## Local prerequisites

- Docker + Docker Compose (for local infra)
- Go toolchain (for Go services)
- Python 3.11+ (for Python services)
- Node.js 20+ (for TypeScript services)

---

## Local environment layout

Each service reads configuration from (in order):

1. environment variables
2. mounted config file (yaml/json)
3. defaults

Required cross-service env variables (common):

- `DSP_ENV` (dev/staging/prod)
- `DSP_SERVICE_NAME`
- `DSP_LOG_LEVEL` (debug/info/warn/error)
- `DSP_HTTP_ADDR` (e.g. `0.0.0.0:8080`)
- `DSP_GRPC_ADDR` (e.g. `0.0.0.0:9090`)

---

## Running locally (high level)

The intended local workflow:

- bring up local infra (Postgres/Redis/stream/queue) using docker compose
- run services individually from source
- run integration tests against local stack

This repository will include:

- `infra/local/docker-compose.yaml`
- `scripts/dev/*` helper scripts for bootstrapping

---

## Coding standards

- Prefer explicit timeouts on all outbound calls.
- Never log secrets or full payment payloads.
- Return typed errors with stable `error.code`.
- Use idempotency keys for all mutating operations.
- Emit domain events via outbox (SQL) or transactionally consistent patterns.

---

## Observability standards

Every service exposes:

- `/healthz` (liveness)
- `/readyz` (readiness)
- `/metrics` (Prometheus)

All logs are JSON, include:

- `service`, `env`, `request_id`, `trace_id`, `tenant_id` (where applicable)

