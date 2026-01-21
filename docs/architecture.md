# Architecture

This document describes the system architecture, components, and key algorithms
for the Distributed Workflow Engine (DWE).

## 1. High-Level Architecture

```
                                +-------------------------+
                                |   External Clients     |
                                +------------+------------+
                                             |
                                             | HTTPS / JSON
                                             v
+------------------+            +-------------------------+
|  Auth Provider   |<-----------|      API Service        |
| (OIDC, JWT, mTLS)|            |  (TypeScript/Node.js)   |
+------------------+            +------------+------------+
                                             |
                                             | SQL (PostgreSQL)
                                             v
                              +--------------+--------------+
                              |         PostgreSQL          |
                              |  (state, queue, metadata)   |
                              +--------------+--------------+
                                             |
                  +--------------------------+--------------------------+
                  |                                                     |
                  v                                                     v
      +-----------+------------+                           +------------+-----------+
      |       Scheduler        |                           |        Executors        |
      |        (Go)            |                           |      (Python workers)   |
      |  - leader election     |                           |  - task execution       |
      |  - step scheduling     |                           |  - retries, backoff     |
      +-----------+------------+                           +------------+-----------+
                  |                                                     |
                  | Metrics                                             | Metrics
                  v                                                     v
          +-------+---------+                                   +-------+---------+
          |   Prometheus    |<----------------------------------|   Metrics Export |
          +-----------------+                                   +-----------------+
```

## 2. Core Concepts

- **Workflow**: A named DAG of steps. Each workflow has versions.
- **Workflow Version**: Immutable snapshot of a workflow definition.
- **Run**: A single execution of a workflow version with input parameters.
- **Task**: A schedulable unit representing a step execution in a run.

## 3. Data Flow (Single Run)

```
Client -> API -> workflow_runs (pending)
                 |
                 v
             Scheduler (leader)
                 |
                 v
            tasks (queued)
                 |
                 v
          Executors claim tasks
                 |
                 v
          tasks (running -> succeeded/failed)
                 |
                 v
         workflow_runs updated
```

## 4. Scheduler Design

The scheduler is a leader-elected service. Only one scheduler is active for a
given shard assignment to prevent duplicate scheduling. Followers remain idle
and take over when the leader fails.

### 4.1 Leader Election (PostgreSQL Advisory Lock)

- Each scheduler attempts `pg_try_advisory_lock` on a fixed key.
- If successful, it is the leader for its shard group.
- The lock is periodically refreshed by maintaining a lease row.

```
while true:
    if pg_try_advisory_lock(LEADER_KEY):
        act_as_leader()
    else:
        sleep(backoff)
```

### 4.2 Scheduling Algorithm (DAG Ready Steps)

Steps are scheduled when all dependencies have succeeded.

```
ready_steps = steps where all deps are in succeeded
for step in ready_steps:
    insert task(step_id, run_id, payload)
```

## 5. Executor Design

Executors are stateless workers that poll tasks from the queue (PostgreSQL).
They perform tasks and update status. The queue uses `SELECT FOR UPDATE SKIP
LOCKED` to achieve safe, distributed task claiming.

```
BEGIN;
SELECT * FROM tasks
WHERE status = 'queued' AND run_after <= now()
ORDER BY priority, created_at
FOR UPDATE SKIP LOCKED
LIMIT N;
UPDATE tasks SET status='running', locked_by=?, locked_at=now()
WHERE id IN (...);
COMMIT;
```

## 6. Replication and Fault Tolerance

- **Multiple schedulers**: one leader, others standby.
- **Multiple executors**: shared queue with safe locking.
- **DB replication**: PostgreSQL can run in primary/replica mode.
- **Task retries**: exponential backoff on failure.
- **Idempotency**: tasks are uniquely identified; replays are safe.

## 7. Sharding and Partitioning

Sharding is based on run ID hashing.

```
shard_id = hash(run_id) % SHARD_COUNT
```

- Scheduler instances can be configured to own one or more shards.
- Executors can be configured to claim tasks from assigned shards.

## 8. Raft-Style Consensus (Pseudo-Implementation)

The system uses PostgreSQL locks for leader election in practice, but a Raft-
style model can be used if the control plane is moved to an internal cluster.

```
state: follower | candidate | leader
term: integer
log: list of (term, command)

on election timeout:
    state = candidate
    term += 1
    vote_for = self
    send RequestVote(term, last_log_index, last_log_term)

on ReceiveVoteResponse:
    if majority:
        state = leader
        send AppendEntries(heartbeat)

on AppendEntries from leader:
    if term >= current term:
        state = follower
        reset election timeout
```

### 8.1 Log Replication Pseudocode

```
leader_append(command):
    log.append((term, command))
    for follower in peers:
        send AppendEntries(log[-1])
    wait for majority acks
    commit_index = log_index
    apply(command)
```

## 9. Reliability Guarantees

- **At-least-once task execution**: tasks may execute more than once; steps must be idempotent.
- **Exactly-once state transitions**: state changes are transactionally recorded.
- **Crash recovery**: any "running" task can be reclaimed after lock TTL.

## 10. Security and Compliance

Security controls are described in `docs/security.md` and implemented in
Kubernetes manifests with non-root containers, read-only file systems, and
network policies.
