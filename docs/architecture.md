Architecture
============

1. Full System Overview
-----------------------

The platform is a cloud-native, multi-service system that provides:

* A public API entry point (API Gateway) with routing, auth enforcement, and
  rate limiting.
* A dedicated Authentication Service implementing OAuth2, JWT issuance, and
  MFA enforcement.
* Domain services for Users, Payments, Workflows, Queues, Streams, Cache,
  Database access, WebSocket realtime, Scheduling, and Worker orchestration.
* A shared observability model (structured logs, metrics, tracing context).
* Strong reliability primitives (idempotency, retries, backpressure,
  circuit breakers, and quorum-based replication).

The platform is intentionally polyglot. Every service is implemented with
feature parity in Python, Go, and TypeScript. Each runtime starts all services
locally for simplicity. In production, these services run as independent
deployments.

Core design principles:

* Stateless compute where possible; stateful components are explicit.
* Idempotent APIs and deterministic workflows.
* Clear separation of control plane (Auth, Scheduler, Workflow) and data plane
  (Queue, Stream, Database, Cache).
* Explicitly modeled failure modes and recovery strategies.
* Comprehensive audit and security posture.

2. ASCII Architecture Diagrams
------------------------------

High-level topology
-------------------

                        +---------------------------+
                        |         Clients           |
                        |  Web / Mobile / Partners  |
                        +-------------+-------------+
                                      |
                                      v
                        +---------------------------+
                        |        API Gateway        |
                        |  TLS, Auth, Rate Limits   |
                        +------+------+------+------+ 
                               |      |      |
                               |      |      v
                               |      |  +-----------+
                               |      |  | WebSocket |
                               |      |  |  Service  |
                               |      |  +-----------+
                               |      |
                               v      v
                      +------------+  +--------------+
                      | Auth       |  | User Service |
                      | Service    |  +--------------+
                      +------------+         |
                               |             |
                               v             v
                         +-----------+   +-----------+
                         | Payments  |   | Workflow  |
                         | Service   |   | Engine    |
                         +-----------+   +-----------+
                               |             |
                               v             v
               +--------------------------+  +-----------------+
               | Distributed Queue        |  | Scheduler       |
               +--------------------------+  +-----------------+
                               |             |
                               v             v
                        +-------------+  +--------------+
                        | Worker Fleet|  | Streaming    |
                        | (Autoscale) |  | Platform     |
                        +------+------+  +--------------+
                               |             |
                               v             v
                        +-------------+  +--------------+
                        | Cache Layer |  | Database     |
                        +-------------+  | Layer        |
                                          +-------------+

Control and data planes
-----------------------

  Control Plane:
    - API Gateway
    - Authentication Service
    - Workflow Engine
    - Scheduler

  Data Plane:
    - Distributed Queue
    - Streaming Platform
    - Cache Layer
    - Database Layer
    - Worker Fleet (execution of jobs)

3. Service-to-Service Communication Flow
----------------------------------------

Primary request flow (User Signup)
----------------------------------

1) Client -> API Gateway: POST /users/register
2) API Gateway -> Auth Service: verify client credentials, validate token
3) API Gateway -> User Service: create user
4) User Service -> Database Layer: insert user record
5) User Service -> Cache Layer: cache user profile
6) User Service -> WebSocket Service: publish "user.created" event
7) API Gateway -> Client: 201 Created

Payment flow (Idempotent charge)
--------------------------------

1) Client -> API Gateway: POST /payments/charge (Idempotency-Key header)
2) Gateway -> Auth Service: validate JWT & MFA claims
3) Gateway -> Payments Service: create payment intent
4) Payments Service -> Database Layer: store intent
5) Payments Service -> Distributed Queue: enqueue "charge" job
6) Worker Fleet -> Queue: pull job, execute charge
7) Worker Fleet -> Payments Service: update payment status
8) Payments Service -> Streaming Platform: emit payment event
9) Payments Service -> Client via Gateway: 202 Accepted or 200 if completed

Workflow execution flow
-----------------------

1) Client -> API Gateway: POST /workflows/start
2) Gateway -> Auth Service: verify permissions
3) Gateway -> Workflow Engine: register workflow run
4) Workflow Engine -> Database Layer: persist state + steps
5) Workflow Engine -> Scheduler: schedule next tasks
6) Scheduler -> Distributed Queue: enqueue task for Worker Fleet
7) Worker Fleet -> Workflow Engine: report task completion
8) Workflow Engine -> Streaming Platform: emit state transition events

Streaming + WebSocket flow
--------------------------

1) Service -> Streaming Platform: publish event to topic
2) Streaming Platform -> WebSocket Service: deliver event to connected clients
3) WebSocket Service -> Clients: push event frames

4. Data Flow Diagrams
---------------------

User data flow
--------------

  [Client] -> [Gateway] -> [User Service] -> [Database Layer]
                             |                  |
                             v                  v
                        [Cache Layer]     [Streaming Platform]
                             |                  |
                             v                  v
                       [WebSocket Service] -> [Client Updates]

Payment data flow
-----------------

  [Client] -> [Gateway] -> [Payments Service] -> [Database Layer]
                               |                      |
                               v                      v
                        [Distributed Queue]     [Streaming Platform]
                               |                      |
                               v                      v
                         [Worker Fleet] -> [WebSocket Service]

Workflow data flow
------------------

  [Client] -> [Gateway] -> [Workflow Engine] -> [Database Layer]
                               |                      |
                               v                      v
                           [Scheduler]          [Streaming Platform]
                               |
                               v
                       [Distributed Queue] -> [Worker Fleet]

Queue and stream internal data flow
-----------------------------------

  Producers -> Queue/Stream -> Partitioned Log -> Consumer Groups
                   |                  |
                   v                  v
              Backpressure      Offset Tracking

5. Failure Scenarios and Recovery Paths
---------------------------------------

Gateway failure
--------------
* Symptom: No inbound traffic processed.
* Detection: Health checks fail, 5xx surge.
* Recovery:
  - Load balancer removes unhealthy gateway instances.
  - New instances start and warm caches.
  - Circuit breakers prevent cascading failures.

Auth service outage
-------------------
* Symptom: Token validation errors, 401/503 to clients.
* Recovery:
  - Gateways use cached public keys for JWT validation.
  - OAuth2 tokens already issued remain valid.
  - If outage persists, gateway enters "read-only" mode for safe endpoints.

Database primary failure
------------------------
* Symptom: Write errors, increased latency.
* Recovery:
  - Automatic failover to replica based on leader election.
  - Write-ahead log replay ensures consistency.
  - Client retry logic with jitter for transient errors.

Distributed queue partition loss
--------------------------------
* Symptom: Consumers lag behind, unacked messages.
* Recovery:
  - Rebalance partitions to healthy nodes.
  - Idempotent processing ensures safe retries.
  - Dead-letter queue captures poison messages.

Streaming broker failure
------------------------
* Symptom: Publish failures, stale consumer offsets.
* Recovery:
  - Replicated partitions promote follower to leader.
  - Producers retry with exponential backoff.
  - Consumers resume from last committed offsets.

Worker crash mid-task
---------------------
* Symptom: Task timeouts, workflow step stuck.
* Recovery:
  - Scheduler detects timeout and requeues task.
  - Idempotency keys prevent double execution.
  - Workflow engine marks attempt history.

Cache eviction storm
--------------------
* Symptom: Database load spikes due to cache misses.
* Recovery:
  - Gateway and services enable local LRU caches.
  - Cache warmup runs in background.
  - Circuit breakers throttle non-essential reads.

WebSocket service overload
--------------------------
* Symptom: Connection drops, latency spikes.
* Recovery:
  - Shed non-critical connections.
  - Stream platform switches to batched delivery.
  - Clients fallback to polling endpoints.

Scheduler failure
-----------------
* Symptom: Workflows not progressing.
* Recovery:
  - Workflow engine detects stale scheduled tasks.
  - New scheduler instance picks up leases.
  - Tasks are re-emitted with unchanged identifiers.

Network partition between data centers
--------------------------------------
* Symptom: Split-brain risk, divergent writes.
* Recovery:
  - Use quorum writes (majority) for critical data.
  - Read-only mode for minority partition.
  - Reconciliation via WAL replay and conflict resolution.
