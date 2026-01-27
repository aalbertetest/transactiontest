## Reliability

This document defines the reliability properties and implementation patterns used across DSP.

---

## Idempotency

### Where it applies

All **mutating** APIs MUST be idempotent:

- Create/update/delete resources
- Payment processing operations (intents, captures, refunds)
- Workflow start/signal/cancel/terminate
- Queue publish (for producer retry)

### Idempotency key contract

- Clients provide: `Idempotency-Key: <uuid>` header (REST) and `idempotency_key` field (gRPC metadata or request).
- Key scope:
  - **Tenant-scoped**
  - **Endpoint-scoped** (same key can be reused safely across different endpoints)
- Key TTL:
  - default 24h (configurable)

### Storage strategy

Idempotency is enforced using an `idempotency_keys` table:

- Uniqueness constraint on `(tenant_id, endpoint, idempotency_key)`
- Stored result includes:
  - `request_hash` (canonical request to prevent key-reuse with different payloads)
  - `response_status`, `response_body` (or response reference), `created_at`, `locked_at`

### Concurrency strategy (duplicate in-flight requests)

If two identical requests with the same key arrive concurrently:

- First request inserts row and acquires a lock (DB row lock or advisory lock).
- Second request waits on lock with bounded timeout; if timeout, returns `409` with a retry-after hint.

---

## Delivery semantics: exactly-once vs at-least-once

### Principles

- **Exactly-once** is only feasible end-to-end under strong constraints (single transactional system).
- DSP uses **at-least-once** delivery with **idempotent consumers** and **deduplication**.

### Queue semantics

- Queue delivery is **at-least-once** with visibility timeout.
- Consumer must `ack` on successful processing.
- If consumer fails, message becomes visible again after timeout.

### Stream semantics

- Stream consumption is **at-least-once** unless consumer uses transactional offset commits with idempotent outputs.
- Producers use:
  - idempotent produce (producer ID + sequence) where supported
  - retries with backoff + metadata refresh

### Outbox pattern

All DB -> stream publishes occur using an outbox:

- In the same SQL transaction as state write, insert into `outbox_events`.
- A relay process reads outbox events and publishes to stream, marking delivered.
- This ensures **no lost events** under producer crashes.

---

## Backpressure

Backpressure is enforced at multiple layers:

- **Gateway**:
  - per-tenant rate limits
  - concurrency limits (max in-flight)
  - request body size limits
- **Queue**:
  - consumer-side prefetch limit
  - visibility timeout tuned per task type
  - DLQ after max receive count
- **Streaming**:
  - producer batching + linger
  - consumer max bytes per fetch
  - partition-level flow control (pause/resume)
- **Workers**:
  - per-tenant concurrency caps
  - task-type concurrency caps (CPU vs IO)

---

## Rate limiting

### Goals

- Protect internal services and shared dependencies.
- Provide predictable tenancy fairness.

### Policies

- Gateway enforces:
  - per-tenant \(RPS\)
  - per-API-key \(RPS\)
  - burst limits via token bucket
- Services enforce:
  - per-tenant expensive endpoints guard (secondary limiter)

### Storage

- Preferred: cache-backed counters (Redis-like) with local fallback.
- Fallback: in-process token buckets (approximate) when cache unavailable.

---

## Circuit breakers

All outbound calls MUST use:

- **timeouts** (client-side)
- **retries with exponential backoff + jitter**
- **circuit breaker** (open/half-open/closed)
- **bulkheads** (separate pools for separate dependencies)

Circuit breakers open on:

- consecutive timeouts above threshold
- error rate above threshold within rolling window

---

## Leader election and coordination

Used for:

- Stream group coordination
- Scheduler leadership
- Outbox relay leadership per shard

Strategy:

- Prefer Kubernetes Lease objects for leadership in cluster.
- For data-plane primitives, use KV store leases where appropriate.

---

## Replication, sharding, and partitioning

### Database

- SQL: primary/replica with read routing where safe.
- Partitioning:
  - by `tenant_id` (range/hash) for large tables
  - time-based partitioning for append-heavy logs

### Queue

- Shard by `(tenant_id, queue_name)` -> partition.
- Replicate partitions across nodes with leader/follower.

### Stream

- Topic partitions are the scaling unit.
- Partition key:
  - `tenant_id` for isolation + fairness
  - `workflow_id` for ordering where required

