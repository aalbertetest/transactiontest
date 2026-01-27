Core Services
=============

This section defines all services, their responsibilities, core data models,
and service-specific behavior. For exact REST and gRPC definitions, see
docs/apis.md and apis/platform.proto.

Common Service Contracts
------------------------

All services expose:

* /healthz: liveness probe
* /readyz: readiness probe
* /metrics: Prometheus-compatible metrics
* Correlation-ID header for trace correlation
* Idempotency-Key header for operations that mutate state
* JSON error format:
  {
    "error": {
      "code": "string",
      "message": "string",
      "retryable": true|false,
      "details": { ... }
    }
  }

1. API Gateway
--------------

Responsibilities:
* TLS termination, routing, rate limiting, request shaping.
* Auth enforcement and token validation.
* Request/response logging and metrics.

Key Models:
* Route { path, method, upstream, timeout_ms, auth_required }
* RateLimit { key, limit, window_seconds }

Notes:
* Gateway implements backpressure by rejecting requests when upstream latency
  exceeds thresholds.
* Supports Canary and blue/green routing using request headers.

2. Authentication Service (OAuth2, JWT, MFA)
--------------------------------------------

Responsibilities:
* OAuth2 authorization code and client credentials flows.
* JWT issuance, refresh, and validation.
* MFA enrollment (TOTP) and verification.

Key Models:
* ClientApp { client_id, client_secret_hash, redirect_uris, scopes }
* AuthCode { code, client_id, user_id, expires_at }
* AccessToken { token, user_id, scopes, expires_at, mfa_verified }
* RefreshToken { token, user_id, expires_at }
* MfaSecret { user_id, secret, enabled }

3. User Service
---------------

Responsibilities:
* User profile creation and management.
* Credential reset coordination (delegates to Auth service).
* Organization and team membership management.

Key Models:
* User { id, email, display_name, status, created_at }
* Org { id, name, owner_id }
* Membership { user_id, org_id, role }

4. Payment Processing Service
-----------------------------

Responsibilities:
* Accepts idempotent charge requests.
* Manages payment intents, captures, refunds.
* Emits ledger events and reconciles asynchronously.

Key Models:
* PaymentIntent { id, user_id, amount, currency, status, idempotency_key }
* Charge { id, intent_id, status, processor_ref }
* Refund { id, charge_id, amount, status }

5. Workflow Engine
------------------

Responsibilities:
* Defines workflows and durable execution state.
* Coordinates task scheduling and worker dispatch.
* Supports retries with backoff and deterministic state transitions.

Key Models:
* Workflow { id, name, version, steps[] }
* WorkflowRun { id, workflow_id, status, current_step, history[] }
* Task { id, run_id, step, payload, attempt, status }

6. Distributed Queue
--------------------

Responsibilities:
* Reliable task delivery (at-least-once).
* Ack, retry, and dead-letter handling.
* Partitioned queues for scale.

Key Models:
* QueueMessage { id, queue, payload, attempt, visible_at }
* Ack { message_id, status, error }

7. Streaming Platform
---------------------

Responsibilities:
* Append-only logs with partitioning.
* Consumer group offset tracking.
* Event retention policies.

Key Models:
* Topic { name, partitions, retention_seconds }
* Record { offset, key, value, timestamp }
* ConsumerOffset { group, topic, partition, offset }

8. Cache Layer
--------------

Responsibilities:
* Shared read-through and write-through cache.
* TTL management and eviction.
* Cache invalidation via event stream.

Key Models:
* CacheEntry { key, value, ttl_seconds, expires_at }

9. Database Layer
-----------------

Responsibilities:
* SQL/NoSQL abstraction for core services.
* Provides transactional and query APIs.
* Manages partitioning and replication routing.

Key Models:
* QueryRequest { sql, params, consistency }
* DocumentRequest { collection, key, payload }

10. WebSocket Realtime Service
------------------------------

Responsibilities:
* Persistent realtime subscriptions.
* Event fan-out to connected clients.
* Authentication and authorization for channels.

Key Models:
* Connection { id, user_id, channels, created_at }
* Subscription { connection_id, topic, filters }

11. Scheduler
-------------

Responsibilities:
* Cron-like schedule definitions.
* Lease-based scheduling for tasks.
* Emits tasks to queues with deterministic IDs.

Key Models:
* Schedule { id, cron, payload, enabled }
* ScheduledTask { id, schedule_id, run_at, status }

12. Worker Fleet
----------------

Responsibilities:
* Executes tasks from queues.
* Reports status back to workflow engine.
* Supports per-task concurrency limits and timeouts.

Key Models:
* Worker { id, status, capabilities, last_heartbeat }
* TaskResult { task_id, status, output, error }

Cross-Service Events
--------------------

Events are emitted to the Streaming Platform using a consistent schema:

  EventEnvelope {
    id, type, source, subject, time, data
  }

Examples:
* user.created
* payment.intent.created
* payment.charge.succeeded
* workflow.run.started
* workflow.step.completed
* cache.invalidate

These events can be consumed by WebSocket service and external clients through
stream subscriptions.
