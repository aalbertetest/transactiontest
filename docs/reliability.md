Reliability
===========

This section describes the reliability patterns implemented in code and
operational controls required for production-scale behavior.

Idempotency
-----------

* All mutating endpoints accept an Idempotency-Key header.
* Payment intent creation uses an idempotency store to avoid duplicate charges.
* Worker retries are safe because task processing is idempotent by design.

Exactly-Once vs At-Least-Once
-----------------------------

* Queue and workflow tasks are at-least-once.
* The distributed queue replays unacked tasks with exponential backoff.
* Exactly-once semantics are achieved at the application layer using:
  - Idempotency keys
  - Task deduplication IDs
  - Deterministic workflow state machines

Backpressure
------------

* API Gateway monitors upstream latency and rejects excess traffic.
* Queue consumers use visibility timeouts to avoid pileups.
* Streaming consumers limit batch size and commit offsets explicitly.

Rate Limiting
-------------

* Token bucket per client IP at the gateway and service level.
* Service-level rate limits are enforced through middleware.
* Burst allowance is configurable via RATE_LIMIT_PER_MIN.

Circuit Breakers
----------------

* Client SDKs implement retry with exponential backoff.
* Retries are capped to avoid infinite loops.
* Gateway returns 502 on upstream errors, preventing cascading failure.

Leader Election
---------------

* Scheduler uses a single active instance in the reference runtime.
* In production, leadership should use a distributed lock (e.g., etcd/Consul).
* Database layer should elect a primary for writes.

Replication
-----------

* Database layer assumes a leader-replica topology.
* Stream partitions are replicated and failover to a new leader.
* Cache layer can be replicated with consistent hashing and gossip.

Sharding
--------

* Queue shards by queue name hash.
* Streams partition by key and topic.
* User data can shard by user_id hash.
* Workflows can shard by workflow_id.

Retry and Timeout Strategy
--------------------------

* Retry on transient errors only (503/timeout).
* Respect exponential backoff with jitter.
* Enforce explicit timeout budgets to avoid request storms.

Data Consistency
----------------

* Payments are eventually consistent until worker confirms charge.
* User updates are strongly consistent within a single shard.
* Streams provide ordered delivery per partition, not globally.
