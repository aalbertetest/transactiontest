# Usage Guide

This document provides detailed usage examples for the Distributed Task Scheduler.

## Table of Contents

1. [Quick Start](#quick-start)
2. [Python Usage](#python-usage)
3. [Go Usage](#go-usage)
4. [Task Types](#task-types)
5. [Cron Jobs](#cron-jobs)
6. [Error Handling](#error-handling)
7. [Monitoring](#monitoring)

---

## Quick Start

### Prerequisites

1. PostgreSQL 13+ running
2. Python 3.9+ or Go 1.21+

### Database Setup

```bash
# Create database
createdb taskscheduler

# Apply schema
psql -d taskscheduler -f sql/001_initial_schema.sql
```

### Configuration

```bash
# Copy example config
cp config.example.yaml config.yaml

# Edit with your settings
vim config.yaml
```

### Start Services

```bash
# Terminal 1: Start scheduler
python -m scheduler.main --config config.yaml

# Terminal 2: Start worker
python -m worker.main --config config.yaml

# Or with Go:
go run ./cmd/scheduler --config config.yaml
go run ./cmd/worker --config config.yaml
```

---

## Python Usage

### Basic Task Submission

```python
import asyncio
from scheduler import TaskScheduler
from config import Settings

async def main():
    # Load configuration
    settings = Settings.from_yaml('config.yaml')
    
    # Create scheduler
    scheduler = TaskScheduler(settings)
    await scheduler.start()
    
    try:
        # Submit an immediate task
        task = await scheduler.submit(
            task_type="send_email",
            payload={
                "to": "user@example.com",
                "subject": "Welcome!",
                "body": "Thanks for signing up."
            },
            priority=50
        )
        print(f"Created task: {task.id}")
        
        # Submit a high-priority task
        urgent_task = await scheduler.submit(
            task_type="process_payment",
            payload={"order_id": "ord_12345", "amount": 99.99},
            queue_name="high-priority",
            priority=90
        )
        
        # Submit a scheduled task (1 hour from now)
        from datetime import datetime, timedelta
        scheduled_task = await scheduler.submit(
            task_type="generate_report",
            payload={"report_id": 123},
            scheduled_at=datetime.utcnow() + timedelta(hours=1)
        )
        
        # Submit with idempotency key (prevents duplicates)
        idempotent_task = await scheduler.submit(
            task_type="charge_card",
            payload={"charge_id": "ch_abc123"},
            idempotency_key="charge_ch_abc123"
        )
        
    finally:
        await scheduler.stop()

asyncio.run(main())
```

### Creating a Worker with Custom Handlers

```python
import asyncio
from worker import Worker
from scheduler.models import Task
from config import Settings

async def main():
    settings = Settings.from_yaml('config.yaml')
    worker = Worker(settings)
    
    # Register handlers using decorator
    @worker.task("send_email")
    async def send_email_handler(task: Task):
        """Send an email using the task payload."""
        email = task.payload
        print(f"Sending email to {email['to']}")
        
        # Simulate sending email
        await asyncio.sleep(1)
        
        # Return result (stored in task.result)
        return {
            "sent": True,
            "message_id": "msg_12345"
        }
    
    @worker.task("process_payment")
    async def payment_handler(task: Task):
        """Process a payment."""
        order_id = task.payload["order_id"]
        amount = task.payload["amount"]
        
        # Process payment logic here
        # ...
        
        return {"success": True, "transaction_id": "tx_67890"}
    
    # Register sync handler (also supported)
    @worker.task("sync_data")
    def sync_handler(task: Task):
        """Synchronous handler example."""
        # This runs in a thread pool
        import time
        time.sleep(2)
        return {"synced": True}
    
    # Start worker
    await worker.start()

asyncio.run(main())
```

### Creating Cron Jobs

```python
import asyncio
from scheduler import TaskScheduler
from scheduler.models import ConcurrencyPolicy
from config import Settings

async def main():
    settings = Settings.from_yaml('config.yaml')
    scheduler = TaskScheduler(settings)
    await scheduler.start()
    
    try:
        # Daily cleanup at midnight
        daily_job = await scheduler.create_cron_job(
            name="daily_cleanup",
            schedule="0 0 * * *",  # minute hour day month weekday
            task_type="cleanup",
            task_payload={"max_age_days": 30},
            description="Clean up old records daily"
        )
        
        # Hourly metrics aggregation
        hourly_job = await scheduler.create_cron_job(
            name="hourly_metrics",
            schedule="0 * * * *",  # Every hour at minute 0
            task_type="aggregate_metrics",
            task_payload={"granularity": "1h"},
            queue_name="analytics",
            priority=40
        )
        
        # Every 5 minutes health check
        health_job = await scheduler.create_cron_job(
            name="health_check",
            schedule="*/5 * * * *",  # Every 5 minutes
            task_type="system_health",
            task_payload={},
            concurrency_policy=ConcurrencyPolicy.FORBID  # Skip if previous is running
        )
        
        # Weekday morning reports at 9 AM
        report_job = await scheduler.create_cron_job(
            name="morning_report",
            schedule="0 9 * * 1-5",  # 9 AM Monday-Friday
            task_type="generate_report",
            task_payload={"type": "daily_summary"},
            timezone="America/New_York"
        )
        
        print(f"Created cron jobs: {daily_job.name}, {hourly_job.name}")
        
    finally:
        await scheduler.stop()

asyncio.run(main())
```

---

## Go Usage

### Basic Task Submission

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    
    "github.com/distributed-task-scheduler/internal/config"
    "github.com/distributed-task-scheduler/internal/persistence"
    "github.com/distributed-task-scheduler/internal/scheduler"
)

func main() {
    ctx := context.Background()
    
    // Load configuration
    cfg, err := config.LoadConfig("config.yaml")
    if err != nil {
        log.Fatal(err)
    }
    
    // Connect to database
    db := persistence.NewDatabase(cfg.Database)
    if err := db.Connect(ctx); err != nil {
        log.Fatal(err)
    }
    defer db.Close()
    
    // Create scheduler
    sched := scheduler.NewScheduler(cfg, db)
    if err := sched.Start(ctx); err != nil {
        log.Fatal(err)
    }
    defer sched.Stop(ctx)
    
    // Submit a task
    payload, _ := json.Marshal(map[string]interface{}{
        "to":      "user@example.com",
        "subject": "Welcome!",
    })
    
    task, err := sched.SubmitTask(ctx, scheduler.TaskOptions{
        TaskType:  "send_email",
        Payload:   payload,
        QueueName: "default",
        Priority:  50,
    })
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Printf("Created task: %s\n", task.ID)
}
```

### Creating a Worker with Handlers

```go
package main

import (
    "context"
    "encoding/json"
    "fmt"
    "log"
    "os"
    "os/signal"
    "syscall"
    "time"
    
    "github.com/distributed-task-scheduler/internal/config"
    "github.com/distributed-task-scheduler/internal/persistence"
    "github.com/distributed-task-scheduler/internal/worker"
    "github.com/distributed-task-scheduler/pkg/models"
)

func main() {
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    
    // Load configuration
    cfg, err := config.LoadConfig("config.yaml")
    if err != nil {
        log.Fatal(err)
    }
    
    // Connect to database
    db := persistence.NewDatabase(cfg.Database)
    if err := db.Connect(ctx); err != nil {
        log.Fatal(err)
    }
    defer db.Close()
    
    // Create worker
    w := worker.NewWorker(cfg, db)
    
    // Register handlers
    w.RegisterHandler("send_email", func(ctx context.Context, task *models.Task) (json.RawMessage, error) {
        var payload struct {
            To      string `json:"to"`
            Subject string `json:"subject"`
        }
        if err := json.Unmarshal(task.Payload, &payload); err != nil {
            return nil, err
        }
        
        fmt.Printf("Sending email to %s: %s\n", payload.To, payload.Subject)
        
        // Simulate work
        time.Sleep(time.Second)
        
        return json.Marshal(map[string]interface{}{
            "sent":       true,
            "message_id": "msg_12345",
        })
    })
    
    w.RegisterHandler("process_payment", func(ctx context.Context, task *models.Task) (json.RawMessage, error) {
        var payload struct {
            OrderID string  `json:"order_id"`
            Amount  float64 `json:"amount"`
        }
        if err := json.Unmarshal(task.Payload, &payload); err != nil {
            return nil, err
        }
        
        // Process payment
        fmt.Printf("Processing payment for order %s: $%.2f\n", payload.OrderID, payload.Amount)
        
        return json.Marshal(map[string]interface{}{
            "success":        true,
            "transaction_id": "tx_67890",
        })
    })
    
    // Start worker
    if err := w.Start(ctx); err != nil {
        log.Fatal(err)
    }
    
    // Wait for shutdown signal
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
    <-sigChan
    
    // Graceful shutdown
    shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 30*time.Second)
    defer shutdownCancel()
    
    w.Stop(shutdownCtx)
}
```

---

## Task Types

### Recommended Task Type Patterns

```
# Use dot notation for namespacing
email.send
email.verify
payment.charge
payment.refund
report.generate
report.export
cleanup.sessions
cleanup.files
```

### Task Payload Guidelines

```json
{
  "task_type": "email.send",
  "payload": {
    "recipient_id": 12345,
    "template": "welcome",
    "variables": {
      "name": "John",
      "link": "https://example.com/verify"
    },
    "metadata": {
      "source": "signup",
      "campaign_id": "summer2024"
    }
  }
}
```

---

## Error Handling

### Retry Configuration

```python
# Per-task retry configuration
task = await scheduler.submit(
    task_type="flaky_api_call",
    payload={"endpoint": "https://api.example.com"},
    max_attempts=5,        # Up to 5 attempts
    timeout_seconds=30,    # 30 second timeout per attempt
)
```

### Handler Error Handling

```python
@worker.task("risky_operation")
async def risky_handler(task: Task):
    try:
        result = await do_risky_thing()
        return {"success": True, "data": result}
    except TransientError as e:
        # Will be retried
        raise e
    except PermanentError as e:
        # Log and fail permanently (goes to dead letter after max attempts)
        logger.error(f"Permanent failure: {e}")
        raise e
```

### Dead Letter Queue

```python
# Query dead letter tasks
dead_tasks = await queue.get_dead_letter_tasks(
    queue_name="default",
    limit=100
)

for task in dead_tasks:
    print(f"Dead task: {task.id}")
    print(f"Error: {task.error_message}")
    print(f"Attempts: {task.attempt_count}")
    
    # Manually retry if needed
    if should_retry(task):
        new_task = await queue.retry_dead_task(task.id)
```

---

## Monitoring

### Prometheus Metrics

Key metrics to monitor:

| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `dts_tasks_total` | Task operations by type/queue/status | - |
| `dts_queue_depth` | Tasks waiting in queue | > 10000 |
| `dts_task_duration_seconds` | Execution time histogram | p99 > timeout |
| `dts_active_workers` | Number of healthy workers | < minimum |
| `dts_scheduler_is_leader` | Leadership status | - |

### Example Prometheus Queries

```promql
# Task throughput
rate(dts_tasks_total{operation="completed"}[5m])

# Error rate
rate(dts_tasks_total{operation="failed"}[5m]) / rate(dts_tasks_total{operation="completed"}[5m])

# Queue depth
dts_queue_depth{status="queued"}

# P99 task duration
histogram_quantile(0.99, rate(dts_task_duration_seconds_bucket[5m]))

# Active workers
dts_active_workers
```

### Health Endpoints

```bash
# Scheduler health
curl http://scheduler:8080/health

# Worker health
curl http://worker:8080/health

# Metrics
curl http://scheduler:9090/metrics
```

### Grafana Dashboard

Import the provided dashboard:

```bash
# Copy dashboard JSON
cp docs/grafana-dashboard.json /var/lib/grafana/dashboards/
```

---

## Best Practices

### Task Design

1. **Idempotency**: Design tasks to be safely re-executed
2. **Small Payloads**: Store large data externally, pass references
3. **Timeouts**: Set realistic timeouts for each task type
4. **Logging**: Include task_id in all log messages

### Queue Design

1. **Separate Queues**: Use different queues for different priorities
2. **Resource Isolation**: Separate CPU-intensive from I/O tasks
3. **Monitoring**: Alert on queue depth and latency

### Scaling

1. **Horizontal**: Add more workers for throughput
2. **Vertical**: Increase concurrency for I/O-bound tasks
3. **Database**: Use read replicas for monitoring queries
