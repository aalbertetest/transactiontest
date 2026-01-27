## Architecture

This document is the canonical description of the **Distributed Software Platform (DSP)** architecture.

It contains:

- Full system overview
- ASCII architecture diagrams
- Service-to-service communication flow
- Data flow diagrams
- Failure scenarios and recovery paths

---

## 1) Full system overview

DSP is a cloud-native platform composed of multiple **domain services** and **platform primitives**:

- **Identity & Access**: Authentication Service (OAuth2/OIDC, JWT, MFA), authorization via policy + roles
- **API Surface**: API Gateway (REST + gRPC entrypoint, auth, rate limiting, request normalization)
- **Core Domain**:
  - **User Service**: tenants, users, organizations, API keys, entitlements
  - **Payment Processing Service**: payment intents, idempotency keys, ledger entries, webhook ingestion
- **Orchestration**:
  - **Workflow Engine**: durable workflows, timers, activities, retries, compensation, history/event sourcing
  - **Scheduler**: cron/at triggers; schedules workflow starts; timer wheel support
  - **Worker Fleet**: horizontally scalable workers that execute activities/tasks
- **Messaging**:
  - **Distributed Queue**: work queue (at-least-once), delayed messages, visibility timeout, DLQ
  - **Streaming Platform**: append-only logs, consumer groups, partitions, offsets, retention
- **Realtime**:
  - **WebSocket Realtime Service**: multi-tenant fanout, presence, topic subscriptions, delivery acks
- **Storage & State**:
  - **Cache Layer**: low-latency cache, rate-limit counters, session/MFA challenges, hot reads
  - **Database Layer**: SQL for strongly-consistent metadata + ledger, NoSQL/log storage for event histories

DSP is designed with **failure as a first-class concern**:

- The system assumes nodes, pods, and whole zones can fail.
- It relies on **idempotency keys**, **dedupe**, **outbox patterns**, and **reconciliation jobs**.
- Communication uses **explicit timeouts**, **retries with jitter**, **circuit breakers**, and **bulkheads**.
- Critical state transitions are modeled as **append-only events** and/or **transactions**.

### Multi-tenancy model

All external-facing APIs are multi-tenant.

- **Tenant** is a top-level isolation boundary (data partitioning, per-tenant rate limits, per-tenant keys).
- **Org** and **Project** are sub-scopes within a tenant, used for RBAC and resource namespaces.

### Control plane vs data plane

The platform emphasizes a split:

- **Control plane** handles auth, orchestration, configuration, and management APIs.
- **Data plane** handles high-throughput queue/stream ingestion, websocket fanout, and worker execution.

---

## 2) ASCII architecture diagrams

### 2.1 High-level system (external + internal)

```
                 +------------------+
   Clients       |  Admin Console   |
 (SDKs/CLI/UI)   +---------+--------+
                           |
                           v
                 +------------------+       +---------------------+
                 |   API Gateway    |<----->|  Auth Service (OIDC) |
                 |  REST + gRPC     |       | OAuth2/JWT/MFA       |
                 +----+-----+-------+       +----------+----------+
                      |     |                          |
        --------------+     +--------------------------+
        |                                  |
        v                                  v
 +--------------+                  +------------------+
 | User Service |                  | Payment Service  |
 | tenants/users|                  | intents/ledger   |
 +------+-------+                  +----+-------------+
        |                               |
        |                               v
        |                        +--------------+
        |                        | Database     |
        |                        | (SQL + KV)   |
        |                        +------+-------+
        |                               |
        v                               v
 +------------------+          +----------------------+
 | Workflow Engine  |<-------->|  Scheduler           |
 | durable state    |          | cron/timers          |
 +---+------+-------+          +----------+-----------+
     |      |                              |
     |      v                              v
     |   +------------------+     +-------------------+
     |   | Distributed Queue|     | Streaming Platform|
     |   | tasks, DLQ       |     | partitions/offset |
     |   +--------+---------+     +---------+---------+
     |            |                         |
     v            v                         v
 +----------------------+          +----------------------+
 | Worker Fleet         |          | WebSocket Realtime   |
 | executes activities  |          | pub/sub + fanout     |
 +----------------------+          +----------------------+
```

### 2.2 Internal platform primitives (cross-cutting)

```
 +----------------------------- Platform Libraries -----------------------------+
 | Config Loader | Structured Logging | Metrics | Tracing | Retry | Validation |
 +--------------------+----------------------+------------------+--------------+
                      |                      |
                      v                      v
            +----------------+        +------------------+
            | Secrets Store  |        | Observability    |
            | (KMS/Vault)    |        | (OTel/Prom/Graf) |
            +----------------+        +------------------+
```

---

## 3) Service-to-service communication flow

DSP uses a **mixed communication model**:

- **North-south** (clients -> platform): REST + gRPC through API Gateway.
- **East-west** (service -> service): gRPC for synchronous calls; streaming/queue for async; webhook ingestion for external systems.

### 3.1 Request flow: authenticated API call (REST)

1. Client calls API Gateway with `Authorization: Bearer <token>` and an idempotency key (when applicable).
2. Gateway validates token via Auth Service (local JWT verification + optional introspection for opaque tokens).
3. Gateway applies:
   - tenant resolution
   - rate limiting / quota enforcement
   - request validation (OpenAPI)
4. Gateway routes to target service:
   - `User Service` for identity/resource metadata
   - `Payment Service` for payment workflows
   - `Workflow Engine` for orchestration endpoints
5. Service performs business logic:
   - reads/writes database with a transaction boundary
   - emits domain events to streaming platform (outbox pattern)
6. Gateway returns response with:
   - `request_id`, `trace_id`
   - `idempotency_key` echo (if provided)

### 3.2 Async flow: workflow activity execution

1. Workflow Engine decides an activity is ready.
2. It enqueues an activity task into Distributed Queue with:
   - `workflow_id`, `run_id`, `activity_id`, `attempt`, `deadline`
3. Worker Fleet polls queue partitions (sharded by tenant/project).
4. Worker claims task (visibility timeout), executes activity, and reports result.
5. Worker emits:
   - activity completion to Workflow Engine (gRPC)
   - operational events to Streaming Platform
6. Workflow Engine appends event to workflow history and schedules next steps.

### 3.3 Streaming consumption flow: consumer groups

1. Producers append events to a topic partition.
2. Consumers join consumer group:
   - group coordinator assigns partitions
3. Consumers read sequentially, commit offsets.
4. If a consumer fails, coordinator triggers rebalance; offsets prevent reprocessing beyond last commit.

---

## 4) Data flow diagrams

### 4.1 Payments (Stripe-like) data flow

```
 Client
   |
   | POST /payments/intents (idempotency-key)
   v
 API Gateway
   |
   v
 Payment Service
   | 1) SQL TX:
   |    - upsert idempotency record
   |    - create payment_intent
   |    - create ledger_pending entry
   |    - write outbox event
   v
 SQL Database  <----->  Cache (idempotency hot path)
   |
   | 2) publish outbox -> stream topic "payments.events"
   v
 Streaming Platform
   |
   | 3) webhook dispatcher + reconciliation consumers
   v
 External Payment Processor (simulated)
   |
   | webhook: payment_succeeded/failed
   v
 API Gateway -> Payment Service -> SQL TX (finalize ledger) -> emit events
```

### 4.2 Workflow state/event sourcing flow (Temporal-like)

```
 Client -> Gateway -> Workflow Engine
                    |
                    | append event: WorkflowStarted
                    v
               Workflow History Store (KV/Log)
                    |
                    | decisions -> activity tasks
                    v
             Distributed Queue -> Worker Fleet
                    |
                    | report completion/failure
                    v
               Workflow Engine -> append event: ActivityCompleted/Failed
```

### 4.3 Realtime websocket fanout flow

```
 Clients (WS) <-> WebSocket Service <-> Cache (presence, routing)
                         |
                         v
               Streaming Platform (topic: realtime.events)
                         |
                         v
                 Consumers (notifications, audit)
```

---

## 5) Failure scenarios and recovery paths

The platform defines **explicit recovery paths** for common failure modes.

### 5.1 API Gateway pod crash mid-request

- **Symptom**: client sees disconnect / 502; upstream service may or may not have received the request.
- **Mitigation**:
  - Clients send **idempotency keys** for all non-read operations.
  - Gateway includes a **request ID** and forwards it downstream as a correlation ID.
- **Recovery**:
  - Client retries with same idempotency key; service dedupes and returns the original result.

### 5.2 Auth signing key rotation causes invalid tokens

- **Symptom**: tokens signed with new key not recognized by services caching old JWKS.
- **Mitigation**:
  - Auth publishes JWKS via cacheable endpoint with `kid`.
  - Services cache JWKS with short TTL and proactively refresh on unknown `kid`.
- **Recovery**:
  - Services fetch updated JWKS and re-validate; no data loss.

### 5.3 Payment webhook delivery duplicates/out-of-order

- **Symptom**: processor retries webhooks; events may arrive out-of-order.
- **Mitigation**:
  - Webhook endpoint is **idempotent** using `(processor_event_id)` uniqueness.
  - Payment state machine is modeled as **monotonic transitions**.
- **Recovery**:
  - Duplicate webhook is ignored; late webhook validated against current state and either accepted or recorded as anomaly for reconciliation.

### 5.4 Distributed Queue message processed twice (at-least-once)

- **Symptom**: worker times out before ack; task re-delivered.
- **Mitigation**:
  - Activity execution is idempotent by `(workflow_id, run_id, activity_id, attempt)` semantics.
  - Results use compare-and-set writes into history (append-only with expected previous event).
- **Recovery**:
  - Second execution is detected; result is either discarded or treated as duplicate completion.

### 5.5 Streaming partition leader fails

- **Symptom**: producers/consumers see timeouts for a partition.
- **Mitigation**:
  - Replication factor \(>= 3\), ISR tracking, leader election.
  - Clients implement retry with exponential backoff and metadata refresh.
- **Recovery**:
  - New leader elected; clients refresh metadata; resume produce/consume from last committed offset.

### 5.6 Workflow Engine node crash

- **Symptom**: in-memory state lost; in-flight decisions interrupted.
- **Mitigation**:
  - Workflow state is derived from durable history (event sourcing).
  - Timers and activities are persisted; scheduler can re-drive.
- **Recovery**:
  - On restart, engine reloads workflow state from history and resumes from last committed event.

### 5.7 Cache outage

- **Symptom**: elevated latency and increased DB load; rate limiting may degrade.
- **Mitigation**:
  - Cache is a **performance optimization**, not a source of truth.
  - Rate limiting falls back to **local leaky bucket** with reduced accuracy.
- **Recovery**:
  - Cache warms gradually; critical operations continue using DB.

