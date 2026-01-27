Testing
=======

Unit Tests
----------

Focus areas:
* Auth: JWT issuance/validation, MFA code validation.
* Payments: idempotency and status transitions.
* Workflows: deterministic step transitions.
* Queue: visibility timeout and retry behavior.

Integration Tests
-----------------

* API Gateway -> Auth -> User Service signup flow.
* Payment creation -> queue -> worker -> streaming event.
* Workflow start -> scheduler -> queue -> worker -> workflow completion.

Load Tests
----------

Use a tool like k6 or Locust to validate:
* 99th percentile latency under peak throughput.
* Queue depth and worker throughput scaling.
* WebSocket fan-out performance for event bursts.

Chaos Tests
-----------

Simulated scenarios:
* Kill a worker while processing tasks.
* Drop database connections to force retries.
* Partition the stream broker to verify consumer recovery.

Example Test Data
-----------------

Users:
[
  { "id": "usr_1", "email": "alice@example.com", "display_name": "Alice" },
  { "id": "usr_2", "email": "bob@example.com", "display_name": "Bob" }
]

Payments:
[
  { "id": "pi_1", "user_id": "usr_1", "amount": 4999, "currency": "USD" }
]

Workflows:
[
  { "id": "wf_1", "name": "order_fulfillment", "definition": { "steps": ["charge", "ship"] } }
]
