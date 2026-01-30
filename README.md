# Distributed Workflow Engine (Temporal-Inspired)

This repository contains a **production-grade, event-driven workflow engine** inspired by Temporal.
It implements deterministic workflows, durable event history, task queues, worker polling,
activity retries with backoff, heartbeats, timeouts, and a persistence layer.

The codebase includes **two complete implementations**:

- **Python** (`/python`) using the standard library and SQLite
- **Go** (`/go`) using SQLite (pure Go driver)

The engine is designed so that the **same architectural principles** apply in both implementations:

- Workflow logic is *deterministically replayed* from persisted history.
- External side-effects are isolated in activities and executed with **at-least-once** semantics.
- Every decision is recorded as a history event, enabling fault recovery and replay.

---

## 1. High-Level Architecture Explanation

This engine splits responsibilities across a small set of logical components. In production,
these components would typically run as independent services. In this repository, they are
implemented as composable libraries (with local runners for examples and tests).

**Core Components**

1. **Frontend API (Workflow Engine Core)**
   - Handles workflow start and signal commands.
   - Appends initial events and enqueues workflow tasks.

2. **History (Persistence Layer)**
   - Stores the immutable event history for each workflow execution.
   - Stores workflow metadata (state, result, error).
   - Stores activity tasks and timers for timeouts and scheduling.

3. **Matching / Task Queue**
   - Durable queue with leasing semantics.
   - Workers poll this queue to pick up workflow tasks and activity tasks.

4. **Worker Process**
   - Executes workflow tasks by replaying history.
   - Executes activity tasks with heartbeats, retries, and timeouts.

5. **Scheduler / Timer Service**
   - Monitors timers and timeouts.
   - Fires timers and enqueues new workflow tasks.
   - Detects heartbeat timeouts and schedules retries.

**Key Design Principles**

- **Event Sourcing:** All state transitions are recorded as history events.
- **Determinism:** Workflow code is replayed on each decision.
- **Isolation:** Activities are the only place where non-deterministic side-effects occur.
- **Recoverability:** On crash, state is rebuilt by replaying events.

---

## 2. ASCII Architecture Diagrams

### 2.1 Logical Components

```
            +------------------------------+
            |        Frontend API          |
            |  Start/Signal Workflow       |
            +--------------+---------------+
                           |
                           | Append events + enqueue workflow task
                           v
            +--------------+---------------+
            |            History           |
            | (Event Log + Workflow State) |
            +--------------+---------------+
                           |
                           | Persist tasks, timers, activities
                           v
            +--------------+---------------+
            |          Task Queue          |
            | (Durable, Leased, Polled)    |
            +--------------+---------------+
                           |
                           | Poll
                           v
             +-------------+-------------+
             |           Worker          |
             | Workflow Tasks / Activities|
             +-------------+-------------+
                           |
                           | Heartbeats, results, failures
                           v
            +--------------+---------------+
            |        Scheduler/Timers      |
            | Timeout scan + timer firing  |
            +------------------------------+
```

### 2.2 Execution Flow

```
Client          Engine           History           Queue            Worker
  |               |                |                |                |
  | Start WF      |                |                |                |
  +-------------->|                |                |                |
  |               | Create WF      |                |                |
  |               | Append events  |                |                |
  |               +--------------->|                |                |
  |               | Enqueue WF     |                |                |
  |               +-------------------------------> |                |
  |               |                |                | Poll           |
  |               |                |                | <--------------+
  |               |                |                | Run workflow   |
  |               |                | <--------------+ Append events  |
  |               |                |                | Enqueue tasks  |
  |               |                +------------------------------->
```

---

## 3. State Machine Design for Workflows

Workflows are modeled as a deterministic state machine driven by **events** and **tasks**.
The workflow transitions are explicit and durable. The states and transitions are:

```
 +--------------------+
 |   NOT_STARTED      |
 +---------+----------+
           |
           | WorkflowExecutionStarted
           v
 +--------------------+
 |      RUNNING       |
 +---------+----------+
           |
           | WorkflowTaskScheduled / Started / Completed
           v
 +--------------------+
 |   WAITING (IDLE)   |<----+
 +---------+----------+     |
           |                |
           | SignalReceived |
           +----------------+
           |
           | ActivityCompleted / TimerFired
           v
 +--------------------+
 |      RUNNING       |
 +---------+----------+
           |
           | WorkflowExecutionCompleted
           v
 +--------------------+
 |     COMPLETED      |
 +--------------------+

 Failure Path:
   RUNNING -> WorkflowExecutionFailed -> FAILED

 Termination Path:
   RUNNING -> TERMINATED
```

**Key Details:**

- A workflow task is the *decision task* that executes workflow code.
- Waiting means the workflow is paused until a signal, activity result, or timer.
- Each workflow task replays the entire history deterministically.

---

## 4. Persistence Model with Schemas

Both Python and Go implementations store data in SQLite. The schema is the same
for consistency and determinism across languages.

### 4.1 `workflow_executions`

Tracks high-level execution state.

```sql
CREATE TABLE IF NOT EXISTS workflow_executions (
    workflow_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    workflow_type TEXT NOT NULL,
    state TEXT NOT NULL,
    input TEXT,
    result TEXT,
    error TEXT,
    task_queue TEXT NOT NULL,
    started_at INTEGER NOT NULL,
    updated_at INTEGER NOT NULL,
    version INTEGER NOT NULL,
    PRIMARY KEY (workflow_id, run_id)
);
```

### 4.2 `history_events`

Immutable event log of workflow execution history.

```sql
CREATE TABLE IF NOT EXISTS history_events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    workflow_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    event_type TEXT NOT NULL,
    event_time INTEGER NOT NULL,
    attributes TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_history_workflow
    ON history_events (workflow_id, run_id, id);
```

### 4.3 `activity_tasks`

Durable record for each activity execution.

```sql
CREATE TABLE IF NOT EXISTS activity_tasks (
    activity_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    activity_name TEXT NOT NULL,
    input TEXT NOT NULL,
    state TEXT NOT NULL,
    scheduled_at INTEGER NOT NULL,
    started_at INTEGER,
    completed_at INTEGER,
    heartbeat_at INTEGER,
    heartbeat_details TEXT,
    attempt INTEGER NOT NULL,
    max_attempts INTEGER NOT NULL,
    retry_policy TEXT NOT NULL,
    schedule_to_close_timeout_seconds INTEGER NOT NULL,
    start_to_close_timeout_seconds INTEGER NOT NULL,
    heartbeat_timeout_seconds INTEGER NOT NULL,
    last_failure TEXT
);
```

### 4.4 `timers`

Stores workflow timers for deterministic scheduling.

```sql
CREATE TABLE IF NOT EXISTS timers (
    timer_id TEXT PRIMARY KEY,
    workflow_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    fire_at INTEGER NOT NULL,
    created_at INTEGER NOT NULL,
    fired_at INTEGER,
    state TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_timers_due
    ON timers (state, fire_at);
```

### 4.5 `task_queue`

Durable, leased queue for workflow and activity tasks.

```sql
CREATE TABLE IF NOT EXISTS task_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    queue_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    payload TEXT NOT NULL,
    visible_at INTEGER NOT NULL,
    lease_owner TEXT,
    lease_expires_at INTEGER,
    attempts INTEGER NOT NULL,
    max_attempts INTEGER NOT NULL,
    created_at INTEGER NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_task_queue_lookup
    ON task_queue (queue_name, task_type, visible_at, lease_expires_at);
```

---

## 5. Exactly-Once vs At-Least-Once Execution

**Workflow code** is deterministic and replayed from history, which produces a
logical **exactly-once** effect for workflow decisions.

**Activities** are side-effecting and can be retried. Therefore, they have
**at-least-once execution** semantics.

**Implications:**

- Activities **must be idempotent** or use external deduplication keys.
- Workflow code is safe from side effects and gets replayed deterministically.

---

## 6. Failure Recovery and Replay Logic

**Failure recovery** is achieved through event sourcing:

1. Every state transition is appended to `history_events`.
2. If a worker crashes, another worker can replay all history events.
3. The replay reconstructs the workflow's logical state and continues.

**Replay Steps (per workflow task):**

1. Load workflow execution metadata.
2. Fetch history events for the workflow run.
3. Create a deterministic runner.
4. Run workflow code from the beginning.
5. When the code reaches an operation:
   - If it exists in history, replay the result.
   - If not, emit a command to schedule it.

---

## 7. Task Queues and Worker Polling

Workers use a **leased polling model**:

1. Worker polls for a task in `task_queue`.
2. The queue entry is leased to the worker for a fixed duration.
3. Worker processes the task, then ACKs.
4. If the worker crashes, the lease expires and another worker can pick up.

**Queue task types:**

- `workflow`: decision tasks for deterministic replay.
- `activity`: activity tasks for side effects.

---

## 8. Deterministic Execution Guarantees

Determinism is enforced by:

- **Replaying events in order** for each workflow task.
- **Validating scheduled operations** against history.
- **Recording version markers** for code evolution.

Non-determinism is detected when:

- A workflow schedules a different activity than in history.
- A workflow schedules timers with different parameters.

When detected, the workflow fails with a deterministic error.

---

## 9. Versioning and Backward Compatibility

Workflow code changes must be compatible with **existing histories**.
This engine uses **version markers** that are recorded into history the first
time a code path is executed. Replays use the recorded version.

### Version Marker Semantics

- `get_version(change_id, min, max)` (Python) / `GetVersion(changeID, min, max)` (Go)
- If no marker exists, the engine records one with `max`.
- On replay, the recorded version is used.
- If a workflow attempts to use a version outside `[min, max]`, it fails deterministically.

This ensures that **old executions** remain compatible while **new executions**
can use updated behavior.

---

## 10. Security Model

This implementation is designed with a **defense-in-depth security model**:

1. **Authentication**
   - Clients authenticate to the frontend via API tokens or mutual TLS.
   - Worker identities are tied to service accounts.

2. **Authorization**
   - Role-based access control (RBAC) for workflows and task queues.
   - Permissions scoped to workflow namespaces.

3. **Transport Security**
   - All internal and external calls use TLS.
   - TLS client certificates for worker identity.

4. **Data Security**
   - Encryption at rest for SQLite or backend storage.
   - History events are immutable and auditable.

5. **Audit Logging**
   - Workflow starts, signals, and terminations are recorded.
   - Activity execution attempts are fully logged.

6. **Isolation**
   - Activities run in isolated worker processes.
   - Sensitive workflows can use dedicated queues.

---

# Python Implementation

## Python Modules

```
python/
  engine/
    config.py           # Config loading
    engine.py           # Start/signal workflows
    logging_utils.py    # Logging setup
    metrics.py          # In-process metrics
    models.py           # Event and state constants
    persistence.py      # SQLite persistence
    queue.py            # Task queue abstraction
    retry.py            # Retry policy + backoff
    runtime.py          # Deterministic workflow runtime
    scheduler.py        # Timer + timeout scheduler
    worker.py           # Worker process
  examples/
    simple_workflow.py  # End-to-end example
  tests/
    test_queue.py
    test_workflow_replay.py
    test_integration.py
```

## Running the Python Example

```bash
cd python
PYTHONPATH=. python examples/simple_workflow.py
```

## Running Python Tests

```bash
cd python
PYTHONPATH=. python -m unittest discover -s tests -p "test_*.py"
```

---

# Go Implementation

## Go Modules

```
go/
  engine/
    config.go
    engine.go
    logging.go
    metrics.go
    models.go
    persistence.go
    queue.go
    retry.go
    runtime.go
    scheduler.go
    worker.go
  cmd/engine/main.go
  examples/simple_workflow.go
  engine/*_test.go
```

## Running the Go Example

```bash
cd go
go run ./examples/simple_workflow.go
```

## Running the Go Engine Binary

```bash
cd go
WF_RUN_EXAMPLE=1 go run ./cmd/engine
```

## Running Go Tests

```bash
cd go
go test ./...
```

---

# Operational Notes

## Deterministic Workflows

Workflow code must avoid direct non-deterministic behavior:

- Do NOT access real time directly.
- Do NOT generate random numbers in workflows.
- Use activities for all side effects.

## Activity Idempotency

Activities are retried and therefore **must be idempotent** or use
external deduplication keys.

## Observability

- Logs are emitted for workflow lifecycle events.
- Metrics counters/gauges/histograms are exposed in-process.

---

# Example Workflows

**Greeting Workflow**

- Schedules a `compose_greeting` activity.
- Waits on a timer.
- Waits for an `approval` signal.
- Returns result with version marker.

---

# Full Feature Checklist (Implemented)

- Workflow engine core
- Task scheduler
- Worker process
- Persistence layer
- Queue abstraction
- Retry and backoff
- Heartbeats
- Timeout handling
- Logging and metrics
- Configuration loading
- Unit tests
- Integration tests
- Example workflows

---

# License

This repository is for educational and demonstration purposes.

