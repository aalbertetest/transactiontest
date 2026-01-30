# Distributed Event-Driven Workflow Engine (Temporal-like)

This repository contains **full, real implementations** of a production-grade, event-driven workflow engine
in **Python and Go**, with deterministic execution, durable persistence, a scheduler, workers, heartbeats,
timeouts, retries, and detailed documentation. The architecture follows **event sourcing** and deterministic
replay, inspired by systems like Temporal and Cadence.

---

## 1. High-Level Architecture (Extremely Detailed)

At a high level, the system is organized into **five major subsystems**:

1. **Front Door / API Surface**
   - The entrypoint for starting workflows, querying status, and registering workflow/activity code.
   - In this repository, the API is embedded in the engine class for simplicity.
2. **Workflow Engine Core (History + Orchestration)**
   - Owns workflow state and history, ensures deterministic execution, and schedules tasks.
3. **Task Queues**
   - Durable queues for workflow tasks, activity tasks, and timers.
   - Backed by the persistence layer.
4. **Worker Fleet**
   - Stateless workers poll queues and execute workflow code or activities.
   - Workers emit completion events to resume workflows.
5. **Scheduler / Timer Service**
   - Periodically scans for timers and expired leases.
   - Delivers timer events and triggers retries for timed-out tasks.

### Architectural Principles

- **Event Sourcing**: All decisions are encoded as immutable history events.
- **Deterministic Replay**: Workflow code replays history to produce the same sequence of commands.
- **At-Least-Once Delivery**: Tasks may be re-run; workflow logic is idempotent by design.
- **Leases + Heartbeats**: Execution ownership is maintained with lease expiry and heartbeats.
- **Durable Queues**: Task queues are persisted in a SQL database to survive crashes.

---

## 2. ASCII Architecture Diagrams

### 2.1 High-Level System Diagram

```
                           +----------------------+
                           |   Client / API Call  |
                           +----------+-----------+
                                      |
                                      v
                          +-----------+------------+
                          |  Workflow Engine Core  |
                          |  (Orchestrator + FSM)  |
                          +-----+-----------+------+
                                |           |
                                |           |
                     +----------+           +-----------+
                     |                                  |
                     v                                  v
          +--------------------+               +--------------------+
          |  Persistence Layer |               |    Task Queues     |
          |  (SQLite / SQL)    |               |  (Workflow/Activity|
          +---------+----------+               |   /Timer Queues)   |
                    |                          +---------+----------+
                    |                                    |
                    |                                    v
                    |                         +----------+----------+
                    |                         |       Workers       |
                    |                         | (Poll + Execute)    |
                    |                         +----------+----------+
                    |                                    |
                    |                                    v
                    |                         +----------+----------+
                    |                         |   Scheduler / Timer |
                    |                         |   Lease Expiry Loop |
                    |                         +---------------------+
```

### 2.2 Event-Sourcing & Replay Pipeline

```
           (Workflow Task)
                 |
                 v
    +---------------------------+
    | Load History from DB      |
    +-------------+-------------+
                  |
                  v
    +---------------------------+
    | Replay Workflow Code      |
    | Deterministic Decisions   |
    +-------------+-------------+
                  |
                  v
    +---------------------------+
    | Emit Commands             |
    | - Schedule Activity       |
    | - Start Timer             |
    | - Complete Workflow       |
    +-------------+-------------+
                  |
                  v
    +---------------------------+
    | Persist Events + Tasks    |
    +---------------------------+
```

### 2.3 Workflow State Machine Diagram

```
       +-----------+
       |  CREATED  |
       +-----+-----+
             |
             v
       +-----+-----+
       |  RUNNING  |
       +-----+-----+
      /   |   |   \
     v    v   v    v
 COMPLETED FAILED TIMED_OUT CANCELED/TERMINATED
```

### 2.4 Task Queue Polling Diagram

```
            +--------------------+
            |   Worker Poll Loop |
            +---------+----------+
                      |
       +--------------+--------------+
       |                             |
       v                             v
 +-------------+              +--------------+
 | Workflow Q  |              | Activity Q   |
 +------+------+              +------+-------+
        |                            |
        v                            v
 +-------------+              +--------------+
 | Execute WF  |              | Execute Act  |
 +-------------+              +--------------+
```

---

## 3. Workflow State Machine Design

### States
- **CREATED**: Execution record exists, but no events yet.
- **RUNNING**: Workflow is active; can accept workflow tasks and activity completions.
- **COMPLETED**: Workflow successfully finished.
- **FAILED**: Workflow terminated due to unhandled error or exceeded retry budget.
- **TIMED_OUT**: Workflow or task timed out beyond configured thresholds.
- **CANCELED**: Explicit user cancellation.
- **TERMINATED**: Forced shutdown (administrative stop).

### Transitions
- CREATED → RUNNING: when the workflow is started.
- RUNNING → COMPLETED: when workflow code returns successfully.
- RUNNING → FAILED: unhandled error or task retries exhausted.
- RUNNING → TIMED_OUT: system timeouts exceeded.
- RUNNING → CANCELED/TERMINATED: external intervention.

### Determinism Constraints
All transitions are driven by **events**. Any state change must correspond to:
- A workflow task event,
- A timer firing event, or
- A completion/failure event for activities or workflows.

---

## 4. Persistence Model with Schemas

Persistence uses **SQLite** with write-ahead logging and durable indices. The schema is shared
between the Python and Go implementations.

### 4.1 Workflow Executions
```sql
CREATE TABLE workflow_executions (
  workflow_id   TEXT NOT NULL,
  run_id        TEXT NOT NULL,
  state         TEXT NOT NULL,
  workflow_type TEXT NOT NULL,
  input_json    TEXT NOT NULL,
  started_at    REAL NOT NULL,
  completed_at  REAL,
  last_event_id INTEGER NOT NULL,
  version       INTEGER NOT NULL,
  PRIMARY KEY (workflow_id, run_id)
);
```

### 4.2 Workflow Events (Event Sourcing)
```sql
CREATE TABLE workflow_events (
  workflow_id    TEXT NOT NULL,
  run_id         TEXT NOT NULL,
  event_id       INTEGER NOT NULL,
  event_type     TEXT NOT NULL,
  timestamp      REAL NOT NULL,
  attributes_json TEXT NOT NULL,
  PRIMARY KEY (workflow_id, run_id, event_id)
);
```

### 4.3 Tasks (Workflow / Activity / Timer)
```sql
CREATE TABLE tasks (
  task_id          TEXT PRIMARY KEY,
  queue            TEXT NOT NULL,
  task_type        TEXT NOT NULL,
  workflow_id      TEXT NOT NULL,
  run_id           TEXT NOT NULL,
  payload_json     TEXT NOT NULL,
  state            TEXT NOT NULL,
  attempts         INTEGER NOT NULL,
  max_attempts     INTEGER NOT NULL,
  not_before       REAL NOT NULL,
  created_at       REAL NOT NULL,
  updated_at       REAL NOT NULL,
  lease_expires_at REAL,
  worker_id        TEXT,
  timeout_seconds  INTEGER
);
```

### 4.4 Activity Heartbeats
```sql
CREATE TABLE activity_heartbeats (
  task_id        TEXT PRIMARY KEY,
  workflow_id    TEXT NOT NULL,
  run_id         TEXT NOT NULL,
  last_heartbeat REAL NOT NULL,
  details_json   TEXT NOT NULL
);
```

### 4.5 Indices
```sql
CREATE INDEX idx_tasks_queue_state ON tasks(queue, state, not_before);
CREATE INDEX idx_tasks_lease ON tasks(state, lease_expires_at);
CREATE INDEX idx_tasks_type_state ON tasks(task_type, state, not_before);
```

---

## 5. Exactly-Once vs At-Least-Once Execution

**Exactly-once execution** is impossible in distributed systems without global consensus + perfect failure detection.
The engine instead provides:

### **At-Least-Once Task Delivery**
- Tasks are leased by workers.
- If a worker crashes, the lease expires.
- Scheduler re-queues the task.

### **Effectively-Once Workflow Semantics**
While tasks can run multiple times, workflows remain deterministic because:
- Activity results are recorded as events.
- On replay, the workflow **uses recorded results**, not re-executed code.
- If an activity ran twice, only the first completion event is authoritative.

### Summary
| Layer         | Semantics       | Mechanism                       |
|--------------|-----------------|---------------------------------|
| Task Delivery | At-Least-Once   | Leases + retries                |
| Workflow State| Effectively Once| Event-sourcing + replay         |

---

## 6. Failure Recovery and Replay Logic

### Failure Scenarios Covered
1. **Worker Crash**: Lease expires → task rescheduled.
2. **Activity Timeout**: Scheduler marks task timed-out → retry or fail.
3. **Process Restart**: Engine rebuilds in-memory state from event history.

### Replay Logic
- Workflow tasks always load **entire event history**.
- Workflow code uses history to rebuild a deterministic state.
- Any mismatch (e.g., activity arguments changed) raises **DeterminismError**.

---

## 7. Task Queues and Worker Polling

### Queue Types
1. Workflow Task Queue
2. Activity Task Queue
3. Timer Queue (logical; scheduler-driven)

### Polling Flow
```
Worker Poll Loop:
  poll(workflow_queue)
    if task -> execute workflow
  poll(activity_queue)
    if task -> execute activity
  sleep(poll_interval)
```

---

## 8. Deterministic Execution Guarantees

Determinism is enforced by:
- Storing **every decision** as an event.
- Replaying workflow code against these events.
- Preventing non-deterministic operations (randomness, time, external I/O)
  unless wrapped inside activities.

### Deterministic Primitives
| Operation         | Engine Implementation              |
|------------------|------------------------------------|
| Activities        | ActivityScheduled + Completed/Failed |
| Sleep/Timer       | TimerStarted + TimerFired          |
| Versioning        | MarkerRecorded                     |

---

## 9. Versioning and Backward Compatibility

The engine supports deterministic workflow upgrades via **markers**:

1. Workflow code calls `get_version(change_id, min, max)`.
2. If the marker exists, the recorded version is returned.
3. If not, the engine records `MarkerRecorded` with `max_version`.

This allows:
- Existing workflows to replay old logic,
- New workflows to execute updated logic,
- Safe evolution of workflow code without replay divergence.

---

## 10. Security Model

Even though this repo provides a local engine, the architecture is designed for production:

- **Authentication**: API endpoints should be protected with mutual TLS or OAuth.
- **Authorization**: RBAC and namespace scoping (workflow namespace or tenant ID).
- **Transport Security**: TLS for worker ↔ engine communication.
- **Data Security**:
  - Encrypt event history at rest.
  - Encrypt secrets (activity inputs) using envelope encryption.
- **Multi-Tenancy**:
  - Each workflow namespace has isolated queues and persistence.
  - Quotas enforced on task throughput.
- **Audit Logging**:
  - Workflow events naturally serve as a full audit log.

---

# Implementation (Python)

## Directory Layout
```
python/
  workflow/
    engine.py
    persistence.py
    worker.py
    scheduler.py
    config.py
    backoff.py
    logging.py
    metrics.py
    queue.py
    exceptions.py
    types.py
    state_machine.py
  examples/
    example_workflows.py
  tests/
    test_engine_unit.py
```

## Running Example (Python)
```bash
cd python
PYTHONPATH=. python examples/example_workflows.py
```

## Running Tests (Python)
```bash
cd python
PYTHONPATH=. python -m unittest discover -s tests -p "test_*.py"
```

---

# Implementation (Go)

## Directory Layout
```
go/
  engine/
    engine.go
    errors.go
    types.go
    state_machine.go
  persistence/
    sqlite.go
  queue/
    queue.go
  scheduler/
    scheduler.go
  worker/
    worker.go
  config/
    config.go
  logging/
    logging.go
  metrics/
    metrics.go
  backoff/
    backoff.go
  examples/
    example_workflows.go
  tests/
    engine_test.go
```

## Running Example (Go)
```bash
cd go
go run ./examples
```

## Running Tests (Go)
```bash
cd go
go test ./...
```

---

# Retry, Backoff, Heartbeats, and Timeout Handling

### Retry & Backoff
- Exponential backoff with jitter.
- Configurable max attempts.
- Activity and workflow tasks each track attempts independently.

### Heartbeats
- Activities can call `ctx.heartbeat(...)` (Python) or `ctx.Heartbeat(...)` (Go).
- Heartbeats update lease expiry and record progress.

### Timeouts
- Leases expire if a worker stalls.
- Scheduler converts lease expiry into timeouts.
- Timed-out tasks are retried or failed.

---

# Logging and Metrics

Both implementations provide:
- Structured logging (INFO/WARN/ERROR).
- Basic metrics registry (counters, gauges, histograms).

Metrics counters include:
- `workflows_started`
- `workflows_completed`
- `workflows_failed`
- `activities_completed`
- `activities_failed`

---

# Configuration Loading

### JSON Config + Environment Overrides
Example JSON:
```json
{
  "db_path": "workflow.db",
  "workflow_queue": "workflow",
  "activity_queue": "activity",
  "worker_poll_interval_seconds": 0.2,
  "scheduler_poll_interval_seconds": 0.5,
  "lease_seconds": 30,
  "activity_max_attempts": 5
}
```

Environment overrides use `WF_` prefix, e.g.:
```
WF_DB_PATH=/tmp/workflow.db
WF_WORKFLOW_QUEUE=workflow
```

---

# Example Workflow

The example workflow implements a bank transfer:

1. **Debit Account Activity**
2. **Timer Delay**
3. **Credit Account Activity**

The workflow is deterministic: activity results are recorded in history so that
any retry or replay follows the same path.

---

# Integration + Unit Tests

Both Python and Go include:
- End-to-end tests that start a worker and scheduler.
- Workflow completion verification.
- Backoff tests (Python).

---

# Summary of Production-Grade Guarantees

This engine includes:
- Durable event history
- Deterministic replay
- Task leasing + retry/backoff
- Scheduler-driven timers and timeouts
- Heartbeat-based progress tracking
- Structured logging + metrics
