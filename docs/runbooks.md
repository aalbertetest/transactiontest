Runbooks
========

API Gateway Latency Spike
-------------------------

Symptoms:
* p95 latency > 1s
* 5xx error rate increases

Actions:
1) Check upstream service latencies via /metrics.
2) Enable rate limit tightening temporarily.
3) Confirm circuit breakers are tripping.
4) Scale gateway replicas.

Authentication Outage
---------------------

Symptoms:
* 401/503 errors in gateway
* Token validation failures

Actions:
1) Verify JWT public key cache is healthy.
2) Confirm auth service replicas are running.
3) Temporarily allow cached tokens if configured.

Payment Processing Delays
-------------------------

Symptoms:
* Payment intents remain "pending"
* Queue depth grows

Actions:
1) Check queue length and worker health.
2) Scale worker replicas.
3) Inspect dead-letter queue for failed tasks.
4) Verify downstream processor connectivity.

Workflow Stalls
---------------

Symptoms:
* Workflow runs stuck in "running"
* No state transitions

Actions:
1) Check scheduler health and leases.
2) Confirm workflow queue messages are being processed.
3) Requeue stuck tasks with same idempotency key.

Database Failover
-----------------

Symptoms:
* Write errors or timeouts

Actions:
1) Validate primary node health.
2) Promote replica if primary is down.
3) Update connection strings or service discovery.
4) Reconcile with WAL replay.

WebSocket Fan-out Issues
------------------------

Symptoms:
* Clients disconnect frequently
* High memory use in websocket service

Actions:
1) Check connection count per node.
2) Scale websocket service horizontally.
3) Enable message batching or throttling.
4) Fallback to polling endpoints.
