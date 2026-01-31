# Distributed Task Scheduler

A production-grade distributed task scheduling system similar to Kubernetes CronJobs or Celery. This system provides reliable, scalable task execution with support for scheduled jobs, retries, and distributed worker coordination.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Component Responsibilities](#component-responsibilities)
3. [Task Lifecycle](#task-lifecycle)
4. [Failure Modes and Recovery](#failure-modes-and-recovery)
5. [Core Design](#core-design)
6. [Quick Start](#quick-start)
7. [Configuration](#configuration)
8. [Operational Notes](#operational-notes)

---

# ARCHITECTURE

## High-Level System Overview

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DISTRIBUTED TASK SCHEDULER                         │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐                   │
│  │   Client     │    │   Client     │    │   Client     │                   │
│  │   (API)      │    │   (CLI)      │    │   (SDK)      │                   │
│  └──────┬───────┘    └──────┬───────┘    └──────┬───────┘                   │
│         │                   │                   │                            │
│         └───────────────────┼───────────────────┘                            │
│                             ▼                                                │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                        SCHEDULER SERVICE                             │    │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │    │
│  │  │   Task      │  │   Cron      │  │   Leader    │  │   Health    │ │    │
│  │  │   Router    │  │   Engine    │  │   Election  │  │   Monitor   │ │    │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │    │
│  └────────────────────────────┬────────────────────────────────────────┘    │
│                               │                                              │
│                               ▼                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         TASK QUEUE                                   │    │
│  │  ┌─────────────────────────────────────────────────────────────┐    │    │
│  │  │  Priority Queue   │  Delayed Queue   │  Dead Letter Queue  │    │    │
│  │  └─────────────────────────────────────────────────────────────┘    │    │
│  │                                                                      │    │
│  │  Implementations: PostgreSQL (default) | Redis | In-Memory          │    │
│  └────────────────────────────┬────────────────────────────────────────┘    │
│                               │                                              │
│         ┌─────────────────────┼─────────────────────┐                       │
│         ▼                     ▼                     ▼                       │
│  ┌─────────────┐       ┌─────────────┐       ┌─────────────┐               │
│  │   WORKER    │       │   WORKER    │       │   WORKER    │               │
│  │   Node 1    │       │   Node 2    │       │   Node N    │               │
│  │             │       │             │       │             │               │
│  │ ┌─────────┐ │       │ ┌─────────┐ │       │ ┌─────────┐ │               │
│  │ │Executor │ │       │ │Executor │ │       │ │Executor │ │               │
│  │ │  Pool   │ │       │ │  Pool   │ │       │ │  Pool   │ │               │
│  │ └─────────┘ │       │ └─────────┘ │       │ └─────────┘ │               │
│  │ ┌─────────┐ │       │ ┌─────────┐ │       │ ┌─────────┐ │               │
│  │ │Heartbeat│ │       │ │Heartbeat│ │       │ │Heartbeat│ │               │
│  │ └─────────┘ │       │ └─────────┘ │       │ └─────────┘ │               │
│  └─────────────┘       └─────────────┘       └─────────────┘               │
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                      PERSISTENCE LAYER                               │    │
│  │                                                                      │    │
│  │  ┌──────────────────┐    ┌──────────────────┐                       │    │
│  │  │   PostgreSQL     │    │   State Store    │                       │    │
│  │  │   (Tasks, Jobs,  │    │   (Leader,       │                       │    │
│  │  │    Results)      │    │    Heartbeats)   │                       │    │
│  │  └──────────────────┘    └──────────────────┘                       │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Component Responsibilities

### 1. Scheduler Service

The Scheduler Service is the brain of the system. It runs as a highly-available service with leader election.

**Responsibilities:**
- **Task Routing**: Receives task submissions from clients and routes them to appropriate queues based on task type, priority, and scheduling requirements.
- **Cron Engine**: Evaluates cron expressions and creates task instances at scheduled times. Uses a tick-based approach with 1-second granularity.
- **Leader Election**: Ensures only one scheduler instance processes cron jobs at any time to prevent duplicate task creation. Uses database-based leader election with TTL.
- **Health Monitoring**: Tracks worker health via heartbeats and reassigns tasks from failed workers.
- **Queue Management**: Moves tasks between queues (pending → active → completed/failed/dead-letter).

### 2. Worker Process

Workers are the execution units that process tasks.

**Responsibilities:**
- **Task Fetching**: Polls the task queue for available work using long-polling or push-based notification.
- **Task Execution**: Runs task handlers in isolated execution contexts with resource limits.
- **Heartbeat Emission**: Sends periodic heartbeats to indicate liveness and report progress on long-running tasks.
- **Result Reporting**: Reports task completion status, results, and errors back to the persistence layer.
- **Graceful Shutdown**: Completes in-flight tasks before shutting down, or returns them to the queue.

### 3. Task Queue

The queue system manages task ordering and delivery.

**Responsibilities:**
- **Priority Ordering**: Tasks are dequeued based on priority (higher priority first) and then by scheduled time.
- **Delayed Execution**: Supports scheduling tasks for future execution.
- **At-Least-Once Delivery**: Guarantees tasks are delivered at least once (uses visibility timeout pattern).
- **Dead Letter Queue**: Failed tasks that exceed retry limits are moved to DLQ for manual inspection.

### 4. Persistence Layer

Provides durable storage for all system state.

**Responsibilities:**
- **Task Storage**: Stores task definitions, parameters, and results.
- **Job Definitions**: Stores cron job definitions and their execution history.
- **State Coordination**: Stores leader election state, worker registrations, and heartbeats.
- **Transactional Integrity**: Ensures atomic state transitions using database transactions.

---

## Task Lifecycle

### State Diagram

```
                                    ┌────────────────────┐
                                    │                    │
                                    ▼                    │
┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
│ PENDING  │───▶│  QUEUED  │───▶│  ACTIVE  │───▶│ COMPLETED│
└──────────┘    └──────────┘    └──────────┘    └──────────┘
                     │               │                │
                     │               │                │
                     ▼               ▼                ▼
                ┌──────────┐    ┌──────────┐    ┌──────────┐
                │ CANCELLED│    │  FAILED  │───▶│   DEAD   │
                └──────────┘    └──────────┘    └──────────┘
                                     │
                                     │ (retry)
                                     ▼
                                ┌──────────┐
                                │  QUEUED  │
                                └──────────┘
```

### State Definitions

| State | Description |
|-------|-------------|
| **PENDING** | Task created but not yet eligible for execution (scheduled for future) |
| **QUEUED** | Task is in the queue waiting for a worker to pick it up |
| **ACTIVE** | Task is being executed by a worker |
| **COMPLETED** | Task finished successfully |
| **FAILED** | Task execution failed (may be retried) |
| **DEAD** | Task exceeded retry limit, moved to dead letter queue |
| **CANCELLED** | Task was cancelled before execution |

### State Transitions

1. **PENDING → QUEUED**: When scheduled time arrives
2. **QUEUED → ACTIVE**: When worker claims the task
3. **ACTIVE → COMPLETED**: When worker reports success
4. **ACTIVE → FAILED**: When worker reports failure or timeout occurs
5. **FAILED → QUEUED**: When retry is attempted
6. **FAILED → DEAD**: When retry limit exceeded
7. **QUEUED → CANCELLED**: When task is cancelled before pickup
8. **PENDING → CANCELLED**: When scheduled task is cancelled

---

## Failure Modes and Recovery

### 1. Worker Crash During Execution

**Detection**: Worker stops sending heartbeats. Health monitor detects missing heartbeat after `heartbeat_timeout` (default: 30s).

**Recovery**:
1. Health monitor marks worker as unhealthy
2. All ACTIVE tasks assigned to crashed worker are transitioned to FAILED
3. Tasks with remaining retries are re-queued with exponential backoff
4. Tasks exceeding retry limit are moved to dead letter queue

**Implementation**:
```sql
-- Pseudo-SQL for recovery
UPDATE tasks
SET status = 'FAILED',
    failed_at = NOW(),
    error_message = 'Worker heartbeat timeout'
WHERE worker_id = '<crashed_worker_id>'
  AND status = 'ACTIVE';
```

### 2. Scheduler Crash

**Detection**: Other scheduler instances detect leader has stopped renewing leadership lock.

**Recovery**:
1. Leader election triggers, new leader is elected
2. New leader resumes cron evaluation from last checkpoint
3. No tasks are lost (all state is in database)

### 3. Database Failure

**Detection**: Connection errors to database.

**Recovery**:
1. All components enter retry mode with exponential backoff
2. Workers complete in-memory tasks but cannot claim new ones
3. System automatically resumes when database recovers

### 4. Network Partition

**Scenario**: Workers become isolated from scheduler/database.

**Recovery**:
1. Isolated workers cannot claim new tasks (database unreachable)
2. In-flight tasks continue until completion or local timeout
3. Tasks on isolated workers will timeout and be reassigned
4. When partition heals, workers re-register and resume normal operation

### 5. Duplicate Execution

**Prevention**:
1. Idempotency keys on task creation prevent duplicate submissions
2. Atomic task claiming with `SELECT FOR UPDATE SKIP LOCKED`
3. Optimistic locking on task state transitions

---

# CORE DESIGN

## 5. Task Queue Design

### Queue Structure

The task queue uses a database-backed design for durability with optional Redis acceleration.

```
┌─────────────────────────────────────────────────────────────────┐
│                        TASK QUEUE                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    IMMEDIATE QUEUE                       │   │
│  │  Priority-ordered tasks ready for immediate execution    │   │
│  │  Order: priority DESC, created_at ASC                    │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                    DELAYED QUEUE                         │   │
│  │  Tasks scheduled for future execution                    │   │
│  │  Order: scheduled_at ASC                                 │   │
│  │  Promoted to immediate queue when scheduled_at <= NOW()  │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  DEAD LETTER QUEUE                       │   │
│  │  Tasks that exceeded retry limit                         │   │
│  │  Preserved for debugging and manual retry                │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

### Visibility Timeout Pattern

To ensure at-least-once delivery without distributed locks:

1. Worker claims task with `SELECT FOR UPDATE SKIP LOCKED`
2. Task is marked ACTIVE with `visibility_timeout` timestamp
3. If worker doesn't complete before timeout, task becomes visible again
4. Heartbeats extend the visibility timeout for long-running tasks

```python
# Claiming a task (simplified)
WITH claimed AS (
    SELECT id FROM tasks
    WHERE status = 'QUEUED'
      AND (scheduled_at IS NULL OR scheduled_at <= NOW())
    ORDER BY priority DESC, created_at ASC
    LIMIT 1
    FOR UPDATE SKIP LOCKED
)
UPDATE tasks
SET status = 'ACTIVE',
    worker_id = :worker_id,
    started_at = NOW(),
    visibility_timeout = NOW() + INTERVAL '5 minutes'
WHERE id = (SELECT id FROM claimed)
RETURNING *;
```

## 6. Scheduling Algorithm

### Cron Expression Evaluation

The scheduler uses a tick-based approach:

1. Leader scheduler runs a tick loop every second
2. Each tick evaluates all active cron jobs
3. For each job where `next_run_at <= NOW()`, create a task instance
4. Calculate and store `next_run_at` for the job

```python
def evaluate_cron_jobs():
    """
    Called every second by the leader scheduler.
    """
    now = datetime.utcnow()
    
    # Get all jobs due for execution
    due_jobs = db.query("""
        SELECT * FROM cron_jobs
        WHERE enabled = true
          AND next_run_at <= :now
        FOR UPDATE SKIP LOCKED
    """, now=now)
    
    for job in due_jobs:
        # Create task instance
        task = create_task_from_job(job)
        
        # Calculate next run time
        next_run = croniter(job.schedule, now).get_next(datetime)
        
        # Update job with next run time
        db.execute("""
            UPDATE cron_jobs
            SET next_run_at = :next_run,
                last_run_at = :now
            WHERE id = :job_id
        """, next_run=next_run, now=now, job_id=job.id)
```

### Priority-Based Scheduling

Tasks are dequeued based on:
1. **Priority** (0-100, higher = more important)
2. **Scheduled Time** (earlier scheduled = dequeued first)
3. **Creation Time** (FIFO within same priority/schedule)

```sql
-- Task dequeue query
SELECT * FROM tasks
WHERE status = 'QUEUED'
  AND (scheduled_at IS NULL OR scheduled_at <= NOW())
ORDER BY priority DESC, scheduled_at ASC NULLS FIRST, created_at ASC
LIMIT 1
FOR UPDATE SKIP LOCKED;
```

## 7. Worker Coordination

### Worker Registration

Workers register on startup and maintain presence via heartbeats:

```python
def register_worker():
    """
    Register this worker with the system.
    Called on worker startup.
    """
    worker = db.execute("""
        INSERT INTO workers (id, hostname, pid, started_at, last_heartbeat)
        VALUES (:id, :hostname, :pid, NOW(), NOW())
        ON CONFLICT (id) DO UPDATE
        SET hostname = :hostname,
            pid = :pid,
            started_at = NOW(),
            last_heartbeat = NOW(),
            status = 'ACTIVE'
        RETURNING *
    """, id=worker_id, hostname=socket.gethostname(), pid=os.getpid())
    
    return worker
```

### Task Claiming (Competing Consumers)

Multiple workers compete to claim tasks without conflicts:

```sql
-- Atomic task claim with SKIP LOCKED prevents contention
WITH claimed AS (
    SELECT id FROM tasks
    WHERE status = 'QUEUED'
      AND queue_name = :queue_name
      AND (scheduled_at IS NULL OR scheduled_at <= NOW())
    ORDER BY priority DESC, created_at ASC
    LIMIT :batch_size
    FOR UPDATE SKIP LOCKED
)
UPDATE tasks
SET status = 'ACTIVE',
    worker_id = :worker_id,
    started_at = NOW(),
    attempt_count = attempt_count + 1,
    visibility_timeout = NOW() + INTERVAL '5 minutes'
WHERE id IN (SELECT id FROM claimed)
RETURNING *;
```

## 8. Retry and Backoff Strategy

### Exponential Backoff with Jitter

```python
def calculate_retry_delay(attempt: int, base_delay: float = 1.0, 
                          max_delay: float = 3600.0) -> float:
    """
    Calculate retry delay using exponential backoff with full jitter.
    
    Formula: min(max_delay, random(0, base_delay * 2^attempt))
    
    This prevents thundering herd when many tasks fail simultaneously.
    """
    exponential_delay = base_delay * (2 ** attempt)
    capped_delay = min(max_delay, exponential_delay)
    jittered_delay = random.uniform(0, capped_delay)
    return jittered_delay
```

### Retry Configuration

```python
@dataclass
class RetryPolicy:
    max_attempts: int = 3          # Maximum total attempts (1 initial + 2 retries)
    base_delay: float = 1.0        # Base delay in seconds
    max_delay: float = 3600.0      # Maximum delay (1 hour)
    exponential_base: float = 2.0  # Exponential multiplier
    jitter: bool = True            # Add randomization
    
    # Retry only on specific exceptions
    retry_on: List[str] = field(default_factory=lambda: ['*'])
    
    # Don't retry on these exceptions
    no_retry_on: List[str] = field(default_factory=list)
```

## 9. Idempotency Guarantees

### Idempotency Key Pattern

Tasks can include an idempotency key to prevent duplicate execution:

```python
def submit_task(task_type: str, payload: dict, idempotency_key: str = None):
    """
    Submit a task with optional idempotency key.
    
    If idempotency_key is provided and a task with that key exists:
    - If existing task is PENDING/QUEUED/ACTIVE, return existing task
    - If existing task is COMPLETED, return existing task (no re-execution)
    - If existing task is FAILED/DEAD, create new task (allows retry)
    """
    if idempotency_key:
        existing = db.query("""
            SELECT * FROM tasks
            WHERE idempotency_key = :key
              AND status NOT IN ('FAILED', 'DEAD', 'CANCELLED')
            ORDER BY created_at DESC
            LIMIT 1
        """, key=idempotency_key)
        
        if existing:
            return existing  # Return existing task, don't create duplicate
    
    # Create new task
    return create_task(task_type, payload, idempotency_key)
```

### State Transition Guards

All state transitions are protected by optimistic locking:

```sql
-- Only transition if in expected state
UPDATE tasks
SET status = 'COMPLETED',
    completed_at = NOW(),
    result = :result,
    version = version + 1
WHERE id = :task_id
  AND status = 'ACTIVE'
  AND version = :expected_version
RETURNING *;
```

## 10. Heartbeats and Timeouts

### Heartbeat Protocol

```
Worker                                          Scheduler
   │                                                │
   │  1. Send heartbeat every 10 seconds            │
   │ ──────────────────────────────────────────────▶│
   │                                                │
   │  2. Heartbeat includes:                        │
   │     - worker_id                                │
   │     - active_task_ids                          │
   │     - resource_usage (cpu, memory)             │
   │     - queue_capacity                           │
   │                                                │
   │  3. Scheduler updates last_heartbeat           │
   │◀────────────────────────────────────────────── │
   │                                                │
   │  4. If no heartbeat for 30s:                   │
   │     - Mark worker unhealthy                    │
   │     - Reassign active tasks                    │
   │                                                │
```

### Timeout Configuration

```python
@dataclass
class TimeoutConfig:
    # Worker heartbeat interval
    heartbeat_interval: int = 10  # seconds
    
    # Time after which a worker is considered dead
    worker_timeout: int = 30  # seconds
    
    # Default task execution timeout
    default_task_timeout: int = 300  # 5 minutes
    
    # Maximum task execution timeout
    max_task_timeout: int = 86400  # 24 hours
    
    # Visibility timeout for claimed tasks
    visibility_timeout: int = 300  # 5 minutes
```

---

# QUICK START

## Prerequisites

- Python 3.9+ or Go 1.21+
- PostgreSQL 13+
- (Optional) Redis 6+ for queue acceleration

## Installation

### Python

```bash
cd python
pip install -r requirements.txt
```

### Go

```bash
cd go
go mod download
```

## Running

### 1. Start PostgreSQL and apply migrations

```bash
psql -h localhost -U postgres -d taskscheduler -f sql/001_initial_schema.sql
```

### 2. Start the Scheduler

```bash
# Python
python -m scheduler.main --config config.yaml

# Go
go run ./cmd/scheduler --config config.yaml
```

### 3. Start Workers

```bash
# Python
python -m worker.main --config config.yaml --queues default,high-priority

# Go
go run ./cmd/worker --config config.yaml --queues default,high-priority
```

### 4. Submit a Task

```python
from scheduler.client import TaskClient

client = TaskClient("http://localhost:8080")

# Submit immediate task
task = client.submit(
    task_type="send_email",
    payload={"to": "user@example.com", "subject": "Hello"},
    priority=50
)

# Submit scheduled task
task = client.submit(
    task_type="generate_report",
    payload={"report_id": 123},
    scheduled_at=datetime.utcnow() + timedelta(hours=1)
)

# Create cron job
job = client.create_cron_job(
    name="daily_cleanup",
    schedule="0 0 * * *",  # Midnight daily
    task_type="cleanup",
    payload={"max_age_days": 30}
)
```

---

# CONFIGURATION

## Configuration File (config.yaml)

```yaml
# Database configuration
database:
  host: localhost
  port: 5432
  name: taskscheduler
  user: postgres
  password: ${DB_PASSWORD}
  max_connections: 20
  connection_timeout: 30

# Scheduler configuration
scheduler:
  # Number of scheduler instances (for HA)
  leader_election_ttl: 30  # seconds
  cron_tick_interval: 1    # seconds
  health_check_interval: 10 # seconds

# Worker configuration
worker:
  # Queues to process (comma-separated)
  queues:
    - default
    - high-priority
  
  # Maximum concurrent tasks per worker
  concurrency: 10
  
  # Task fetch batch size
  batch_size: 5
  
  # Heartbeat settings
  heartbeat_interval: 10  # seconds
  
  # Graceful shutdown timeout
  shutdown_timeout: 60    # seconds

# Queue configuration
queue:
  # Default visibility timeout
  visibility_timeout: 300  # seconds
  
  # Polling interval when queue is empty
  poll_interval: 1  # seconds
  
  # Maximum poll interval (for backoff)
  max_poll_interval: 30  # seconds

# Retry configuration
retry:
  default_max_attempts: 3
  default_base_delay: 1.0
  default_max_delay: 3600.0

# Metrics configuration
metrics:
  enabled: true
  port: 9090
  path: /metrics

# Logging configuration
logging:
  level: INFO
  format: json
  output: stdout
```

---

# OPERATIONAL NOTES

## Monitoring

### Key Metrics

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `tasks_queued` | Number of tasks in queue | > 10000 |
| `tasks_active` | Number of tasks being processed | > workers * concurrency |
| `tasks_failed` | Failed task rate | > 5% |
| `task_duration_seconds` | Task execution duration | p99 > timeout |
| `worker_count` | Number of healthy workers | < desired |
| `queue_lag_seconds` | Time oldest task has waited | > 300s |

### Health Endpoints

- `GET /health` - Basic liveness check
- `GET /ready` - Readiness check (database connected)
- `GET /metrics` - Prometheus metrics

## Scaling

### Horizontal Scaling

- **Schedulers**: Run 2-3 instances for HA (only leader is active)
- **Workers**: Scale based on queue depth and task duration
- **Database**: Consider read replicas for monitoring queries

### Capacity Planning

```
Required Workers = (Tasks per Second) * (Average Task Duration) / (Worker Concurrency)
```

## Troubleshooting

### Tasks Stuck in ACTIVE

1. Check worker health: `SELECT * FROM workers WHERE status = 'ACTIVE'`
2. Check for long-running tasks: `SELECT * FROM tasks WHERE status = 'ACTIVE' AND started_at < NOW() - INTERVAL '1 hour'`
3. Force timeout: Update stuck tasks to FAILED

### High Queue Depth

1. Add more workers
2. Increase worker concurrency
3. Check for slow task types
4. Review database performance

### Duplicate Execution

1. Verify idempotency keys are being used
2. Check for network issues causing heartbeat failures
3. Review visibility timeout settings
