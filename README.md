# Event-Driven Workflow Engine (Python + Go)

This repository contains a full, real implementation of a deterministic, event-driven workflow engine inspired by Temporal.
It includes a complete Python implementation and a complete Go implementation, along with unit tests, integration tests,
example workflows, and detailed documentation that mirrors production-grade behavior.

---

## 1. High-Level Architecture Explanation

At a high level, the engine is composed of five core subsystems:

1. **API/Engine Core**: Accepts workflow start requests, registers workflows and activities, applies deterministic decisions,
   and appends authoritative history events.
2. **Persistence Layer**: Stores workflow state, workflow runs, event history, tasks, and timeouts using durable storage
   (SQLite in this reference implementation).
3. **Task Queue Layer**: Provides a queue abstraction that supports leasing, retries, and worker polling.
4. **Workers**: Workflow workers (deciders), activity workers (executors), and timer workers (sleep/wake).
5. **Scheduler / Sweeper**: Periodically scans for timeouts, heartbeat failures, and run timeouts.

The design is event-sourced: every deterministic decision and external side effect is captured as an immutable event
in the history log. The workflow code replays history, ensuring deterministic results even after failures.

---

## 2. ASCII Architecture Diagrams

### System-Level Flow

```
┌────────────────────┐        ┌────────────────────┐
│   Client / API     │        │    Workflow Engine │
│ start_workflow()   │───────▶│  - Registry        │
│ register_workflow  │        │  - Decision Core   │
└────────────────────┘        └─────────┬──────────┘
                                        │
                                        │ append events
                                        ▼
                             ┌──────────────────────┐
                             │     Persistence      │
                             │  - workflows         │
                             │  - workflow_runs     │
                             │  - history_events    │
                             │  - tasks             │
                             └─────────┬────────────┘
                                       │
                                       │ lease tasks
                                       ▼
          ┌───────────────────┬────────────────────┬───────────────────┐
          │ Workflow Workers  │  Activity Workers  │   Timer Workers   │
          │ (deciders)        │  (executors)       │ (sleep/wake)      │
          └───────────────────┴────────────────────┴───────────────────┘
                                       │
                                       │ emit ActivityCompleted/TimerFired
                                       ▼
                                ┌──────────────┐
                                │  Task Queue  │
                                │ (lease/ack)  │
                                └──────────────┘
```

### Event Sourcing and Replay

```
Workflow Task:
  ┌───────────────────────────────────────────────────────────┐
  │ 1) Load history events for run                            │
  │ 2) Reconstruct deterministic state via WorkflowContext    │
  │ 3) WorkflowDefinition.decide() produces commands          │
  │ 4) Engine appends events for commands                     │
  │ 5) Engine schedules activity/timer tasks                  │
  └───────────────────────────────────────────────────────────┘
```

---

## 3. State Machine Design for Workflows

The engine treats workflow definitions as **explicit state machines**. Every workflow is in a state, and each workflow
task drives a deterministic transition based on event history.

**WorkflowDefinition Interface**
- `initial_state() / InitialState()`: The starting state name.
- `decide(ctx, state, state_data, history)`: A deterministic decision function that returns:
  - `next_state`: The next state.
  - `commands`: Activity schedules, timers, or completion commands.
  - `complete` or `failure` flags.

**Example States (Order Workflow)**

```
START
  │ schedule validate_order
  ▼
WAIT_VALIDATE
  │ activity completed?
  ▼
CHARGE
  │ schedule charge_card
  ▼
WAIT_CHARGE
  │ activity completed?
  ▼
SLEEP
  │ schedule timer
  ▼
WAIT_TIMER
  │ timer fired?
  ▼
SEND_RECEIPT
  │ schedule send_receipt
  ▼
WAIT_RECEIPT
  │ activity completed?
  ▼
DONE
```

Each state transition is deterministic because it is solely driven by immutable history events.

---

## 4. Persistence Model with Schemas

The persistence layer is event-sourced. All authoritative changes are appended as immutable history events.
The workflow run state is a cache derived from those events for efficient polling.

### SQL Schema (shared between Python/Go)

```
workflows(
  workflow_id TEXT PRIMARY KEY,
  workflow_type TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at REAL NOT NULL,
  updated_at REAL NOT NULL,
  current_run_id TEXT NOT NULL,
  run_timeout_seconds INTEGER NOT NULL
)

workflow_runs(
  run_id TEXT PRIMARY KEY,
  workflow_id TEXT NOT NULL,
  workflow_type TEXT NOT NULL,
  status TEXT NOT NULL,
  state TEXT NOT NULL,
  state_data TEXT NOT NULL,
  created_at REAL NOT NULL,
  updated_at REAL NOT NULL,
  last_event_id INTEGER DEFAULT 0,
  last_heartbeat_at REAL,
  workflow_task_timeout_seconds INTEGER NOT NULL,
  run_timeout_seconds INTEGER NOT NULL
)

history_events(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_id TEXT NOT NULL,
  event_type TEXT NOT NULL,
  timestamp REAL NOT NULL,
  attributes TEXT NOT NULL
)

tasks(
  task_id TEXT PRIMARY KEY,
  run_id TEXT NOT NULL,
  task_type TEXT NOT NULL,
  queue_name TEXT NOT NULL,
  status TEXT NOT NULL,
  scheduled_at REAL NOT NULL,
  leased_until REAL,
  completed_at REAL,
  attempt INTEGER NOT NULL,
  max_attempts INTEGER NOT NULL,
  payload TEXT NOT NULL,
  last_heartbeat_at REAL,
  heartbeat_timeout_seconds INTEGER,
  timeout_at REAL,
  last_error TEXT
)
```

---

## 5. Exactly-Once vs At-Least-Once Execution

### Workflow Logic (Exactly-Once Semantics)
- The workflow logic itself is **exactly-once** from a logical perspective.
- Each workflow decision is deterministic and replays from the immutable history.
- Duplicate workflow tasks simply replay the history and produce the same decisions.

### Activities (At-Least-Once Semantics)
- Activities are **at-least-once** due to retries and worker failures.
- Every activity attempt is recorded as `ActivityStarted` + `ActivityCompleted/Failed`.
- To achieve effective exactly-once behavior, activities must be idempotent.

**Key Behavior**
| Component            | Delivery Semantics |
|---------------------|--------------------|
| Workflow tasks      | Exactly-once (logical) |
| Activity tasks      | At-least-once |
| Timers              | At-least-once |

---

## 6. Failure Recovery and Replay Logic

Failure recovery is handled by **event replay**:

1. Worker fails after scheduling an activity.
2. New worker replays history and sees the `ActivityScheduled` event.
3. It does **not** reschedule the activity because the command ID is already present.
4. Execution continues deterministically.

**Replay Behavior**
- WorkflowContext scans the event history for ActivityCompleted, ActivityFailed, TimerFired, etc.
- Decisions are deterministic because commands are based solely on history.

**Timeouts and Retries**
- Task leases expire automatically; tasks become eligible again.
- Scheduler sweeps heartbeat timeouts and task timeouts.
- RetryPolicy determines exponential backoff and max attempts.

---

## 7. Task Queues and Worker Polling

The queue abstraction supports:
- **Enqueue**: Insert task into the DB with PENDING status.
- **Lease**: Mark tasks as LEASED for a fixed duration.
- **Ack/Complete**: Mark tasks as COMPLETED.
- **Fail**: Mark tasks as FAILED (with retry reschedule if needed).

Workers poll by queue name:
- Workflow workers poll `workflow-tasks`.
- Activity workers poll `activity-tasks`.
- Timer workers poll `timer-tasks`.

---

## 8. Deterministic Execution Guarantees

Determinism is enforced by:
- **Event sourcing**: All side effects appear as events.
- **Command IDs**: Deterministic IDs ensure idempotent scheduling.
- **WorkflowContext**: Reads only from history; no direct wall-clock time.
- **State machine design**: Workflow code is purely state/transition based.

The workflow must not:
- Use random numbers without recording them.
- Use direct wall-clock time without recording it.
- Read external state without converting it into history events.

---

## 9. Versioning and Backward Compatibility

The engine is designed to support **workflow versioning** through:
- Stable event types (`ActivityScheduled`, `TimerFired`, etc.).
- Stable command IDs within the workflow definition.
- Ability to add new states without breaking old histories.
- The `state_data` dictionary can carry migration flags.

Recommended practices:
- Introduce a `get_version()` decision point that records a `WorkflowVersionMarker` event.
- Gate behavior changes on recorded version markers.
- Avoid renaming event types; add new event types if needed.

---

## 10. Security Model

Production systems should enforce:
- **Authentication**: Signed tokens or mutual TLS for worker and client requests.
- **Authorization**: Per-namespace ACLs or RBAC for workflow/queue access.
- **Encryption in transit**: TLS for all API and worker traffic.
- **Encryption at rest**: Encrypted storage for database and logs.
- **Audit logging**: Record workflow start, termination, and failures.
- **Secrets isolation**: Activities must not leak secrets into workflow history.

This reference implementation is a single-node process, but the security model outlines
exactly what would be required in a production multi-tenant system.

---

# Python Implementation

## Location

```
python_engine/
  workflow_engine/
  examples/
  tests/
```

## Running the Example

```
cd python_engine
python examples/example_workflows.py
```

## Running Tests

```
cd python_engine
python -m unittest discover -s tests -p "test_*.py"
```

---

# Go Implementation

## Location

```
go_engine/
  engine/
  examples/
```

## Running the Example

```
cd go_engine
go run ./examples
```

## Running Tests

```
cd go_engine
go test ./...
```

---

## Notes

- Both engines are fully functional and deterministic.
- Both engines include workflow workers, activity workers, timer workers, and schedulers.
- Both engines support retries, heartbeats, timeouts, and durable replay.
