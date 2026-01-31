# Operational Guide

This document provides operational guidance for running the Distributed Task Scheduler in production.

## Table of Contents

1. [Deployment](#deployment)
2. [Configuration](#configuration)
3. [Scaling](#scaling)
4. [Monitoring](#monitoring)
5. [Troubleshooting](#troubleshooting)
6. [Maintenance](#maintenance)
7. [Disaster Recovery](#disaster-recovery)

---

## Deployment

### System Requirements

**Scheduler Service:**
- 1-2 CPU cores
- 512MB - 1GB RAM
- Run 2-3 instances for HA (only leader is active)

**Worker Service:**
- 2-4 CPU cores per worker
- 1-4GB RAM (depends on task requirements)
- Scale horizontally based on queue depth

**Database (PostgreSQL):**
- 2-4 CPU cores
- 4-8GB RAM
- SSD storage recommended
- Enable connection pooling (PgBouncer) for large deployments

### Docker Deployment

```dockerfile
# Dockerfile.scheduler
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "-m", "scheduler.main", "--config", "/etc/dts/config.yaml"]
```

```yaml
# docker-compose.yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: taskscheduler
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./sql/001_initial_schema.sql:/docker-entrypoint-initdb.d/001_initial_schema.sql
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  scheduler:
    build:
      context: ./python
      dockerfile: Dockerfile.scheduler
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DTS_DATABASE__HOST: postgres
      DTS_DATABASE__PASSWORD: ${DB_PASSWORD}
    volumes:
      - ./config.yaml:/etc/dts/config.yaml:ro
    deploy:
      replicas: 2  # HA with leader election
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  worker:
    build:
      context: ./python
      dockerfile: Dockerfile.worker
    depends_on:
      postgres:
        condition: service_healthy
    environment:
      DTS_DATABASE__HOST: postgres
      DTS_DATABASE__PASSWORD: ${DB_PASSWORD}
      DTS_WORKER__QUEUES: default,high-priority
    volumes:
      - ./config.yaml:/etc/dts/config.yaml:ro
    deploy:
      replicas: 4  # Scale based on load
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
```

### Kubernetes Deployment

```yaml
# scheduler-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dts-scheduler
spec:
  replicas: 2  # HA
  selector:
    matchLabels:
      app: dts-scheduler
  template:
    metadata:
      labels:
        app: dts-scheduler
    spec:
      containers:
      - name: scheduler
        image: your-registry/dts-scheduler:latest
        env:
        - name: DTS_DATABASE__PASSWORD
          valueFrom:
            secretKeyRef:
              name: dts-secrets
              key: db-password
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        volumeMounts:
        - name: config
          mountPath: /etc/dts
      volumes:
      - name: config
        configMap:
          name: dts-config

---
# worker-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dts-worker
spec:
  replicas: 4  # Scale based on load
  selector:
    matchLabels:
      app: dts-worker
  template:
    metadata:
      labels:
        app: dts-worker
    spec:
      containers:
      - name: worker
        image: your-registry/dts-worker:latest
        env:
        - name: DTS_DATABASE__PASSWORD
          valueFrom:
            secretKeyRef:
              name: dts-secrets
              key: db-password
        - name: DTS_WORKER__QUEUES
          value: "default,high-priority"
        resources:
          requests:
            memory: "1Gi"
            cpu: "1000m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        lifecycle:
          preStop:
            exec:
              command: ["/bin/sh", "-c", "sleep 30"]  # Grace period
```

---

## Configuration

### Environment Variables

All configuration can be overridden via environment variables:

```bash
# Database
DTS_DATABASE__HOST=localhost
DTS_DATABASE__PORT=5432
DTS_DATABASE__NAME=taskscheduler
DTS_DATABASE__USER=postgres
DTS_DATABASE__PASSWORD=secret
DTS_DATABASE__MAX_CONNECTIONS=20

# Scheduler
DTS_SCHEDULER__LEADER_ELECTION_TTL=30
DTS_SCHEDULER__CRON_TICK_INTERVAL=1s
DTS_SCHEDULER__INSTANCE_ID=scheduler-1

# Worker
DTS_WORKER__QUEUES=default,high-priority
DTS_WORKER__CONCURRENCY=10
DTS_WORKER__BATCH_SIZE=5
DTS_WORKER__WORKER_ID=worker-1

# Metrics
DTS_METRICS__ENABLED=true
DTS_METRICS__PORT=9090

# Logging
DTS_LOGGING__LEVEL=INFO
DTS_LOGGING__FORMAT=json
```

### Production Configuration Recommendations

```yaml
database:
  max_connections: 50  # Based on workers * concurrency
  min_connections: 10
  connection_timeout: 10s  # Fail fast
  ssl_mode: require  # Always in production

scheduler:
  leader_election_ttl: 30
  leader_renewal_interval: 10
  health_check_interval: 15

worker:
  concurrency: 20  # Adjust based on task resource needs
  batch_size: 10
  visibility_timeout: 10m  # Longer than longest task
  shutdown_timeout: 120s  # Allow long tasks to complete

logging:
  level: INFO
  format: json
  output: stdout

metrics:
  enabled: true
```

---

## Scaling

### Horizontal Scaling

**Workers:**
```bash
# Scale workers based on queue depth
kubectl scale deployment dts-worker --replicas=10

# Or use HPA
kubectl autoscale deployment dts-worker \
  --min=2 --max=20 \
  --cpu-percent=70
```

**Capacity Planning:**
```
Required Workers = (Tasks per Second) * (Average Task Duration) / (Worker Concurrency)

Example:
  - 100 tasks/second
  - 2 second average duration
  - 10 concurrency per worker
  
  Required = 100 * 2 / 10 = 20 workers
```

### Vertical Scaling

Increase worker concurrency for I/O-bound tasks:

```yaml
worker:
  concurrency: 50  # High for I/O-bound
  # concurrency: 5  # Low for CPU-bound
```

### Database Scaling

1. **Connection Pooling**: Use PgBouncer
2. **Read Replicas**: For monitoring queries
3. **Partitioning**: Partition tasks table by date

```sql
-- Partition tasks by month
CREATE TABLE tasks_2024_01 PARTITION OF tasks
FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');
```

---

## Monitoring

### Key Metrics

| Metric | Warning | Critical | Action |
|--------|---------|----------|--------|
| Queue Depth | > 5000 | > 10000 | Scale workers |
| Error Rate | > 5% | > 10% | Investigate failures |
| Task Duration p99 | > 50% timeout | > 80% timeout | Optimize tasks |
| Worker Count | < 80% desired | < 50% desired | Check worker health |
| DB Connections | > 80% max | > 95% max | Scale pool |

### Prometheus Alerting Rules

```yaml
groups:
- name: dts-alerts
  rules:
  - alert: HighQueueDepth
    expr: dts_queue_depth{status="queued"} > 10000
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High queue depth"
      description: "Queue {{ $labels.queue }} has {{ $value }} pending tasks"

  - alert: HighErrorRate
    expr: |
      rate(dts_tasks_total{operation="failed"}[5m]) / 
      rate(dts_tasks_total{operation="completed"}[5m]) > 0.1
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High task error rate"
      description: "Error rate is {{ $value | humanizePercentage }}"

  - alert: NoActiveWorkers
    expr: dts_active_workers < 1
    for: 1m
    labels:
      severity: critical
    annotations:
      summary: "No active workers"
      description: "No workers are processing tasks"

  - alert: SchedulerNotLeader
    expr: sum(dts_scheduler_is_leader) < 1
    for: 2m
    labels:
      severity: critical
    annotations:
      summary: "No scheduler leader"
      description: "No scheduler instance has leadership"
```

### Log Aggregation

Configure structured JSON logging for easy aggregation:

```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "message": "Task completed",
  "task_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "task_type": "send_email",
  "queue": "default",
  "duration_ms": 1523,
  "worker_id": "worker-1"
}
```

---

## Troubleshooting

### Common Issues

#### 1. Tasks Stuck in ACTIVE

**Symptoms**: Tasks remain in ACTIVE status for too long

**Diagnosis**:
```sql
SELECT id, task_type, worker_id, started_at, visibility_timeout
FROM tasks
WHERE status = 'ACTIVE'
  AND started_at < NOW() - INTERVAL '1 hour';
```

**Solutions**:
1. Check worker health: `SELECT * FROM workers WHERE status = 'ACTIVE'`
2. Increase visibility timeout if tasks are legitimately long
3. Force recovery: `SELECT recover_timed_out_tasks()`

#### 2. High Queue Depth

**Symptoms**: Queue keeps growing

**Diagnosis**:
```sql
SELECT queue_name, status, COUNT(*) 
FROM tasks 
WHERE deleted_at IS NULL 
GROUP BY queue_name, status;
```

**Solutions**:
1. Add more workers
2. Increase worker concurrency
3. Check for slow task types
4. Review database performance

#### 3. Duplicate Execution

**Symptoms**: Same task executed multiple times

**Diagnosis**:
```sql
SELECT task_id, COUNT(*) 
FROM task_results 
GROUP BY task_id 
HAVING COUNT(*) > 1;
```

**Solutions**:
1. Use idempotency keys for critical tasks
2. Increase visibility timeout
3. Check for network issues causing heartbeat failures

#### 4. Database Connection Exhaustion

**Symptoms**: "too many connections" errors

**Diagnosis**:
```sql
SELECT count(*) FROM pg_stat_activity;
```

**Solutions**:
1. Reduce `max_connections` per service
2. Use PgBouncer for connection pooling
3. Check for connection leaks

### Debug Queries

```sql
-- Current queue status
SELECT * FROM v_queue_summary;

-- Worker status
SELECT * FROM v_worker_summary;

-- Recent failures
SELECT id, task_type, error_message, attempt_count, created_at
FROM tasks
WHERE status = 'FAILED'
ORDER BY created_at DESC
LIMIT 20;

-- Dead letter queue
SELECT id, task_type, error_message, attempt_count
FROM tasks
WHERE status = 'DEAD'
ORDER BY completed_at DESC
LIMIT 20;

-- Long running tasks
SELECT id, task_type, started_at, 
       EXTRACT(EPOCH FROM (NOW() - started_at)) as running_seconds
FROM tasks
WHERE status = 'ACTIVE'
ORDER BY started_at ASC
LIMIT 20;
```

---

## Maintenance

### Regular Tasks

**Daily:**
- Review error rates and dead letter queue
- Check queue depth trends

**Weekly:**
- Review task duration percentiles
- Analyze slow task types
- Check database performance

**Monthly:**
- Archive old completed tasks
- Review and update retention policies
- Capacity planning review

### Data Retention

```sql
-- Archive tasks older than 30 days
INSERT INTO tasks_archive
SELECT * FROM tasks
WHERE status IN ('COMPLETED', 'DEAD', 'CANCELLED')
  AND completed_at < NOW() - INTERVAL '30 days';

DELETE FROM tasks
WHERE status IN ('COMPLETED', 'DEAD', 'CANCELLED')
  AND completed_at < NOW() - INTERVAL '30 days';

-- Clean up old events
DELETE FROM task_events
WHERE created_at < NOW() - INTERVAL '90 days';
```

### Database Maintenance

```sql
-- Analyze tables for query optimization
ANALYZE tasks;
ANALYZE cron_jobs;
ANALYZE workers;

-- Vacuum to reclaim space
VACUUM ANALYZE tasks;
```

---

## Disaster Recovery

### Backup Strategy

**Database:**
```bash
# Daily full backup
pg_dump -Fc taskscheduler > backup_$(date +%Y%m%d).dump

# Point-in-time recovery with WAL archiving
# Configure in postgresql.conf:
# archive_mode = on
# archive_command = 'cp %p /backup/wal/%f'
```

### Recovery Procedures

**1. Worker Failure:**
- Tasks automatically recovered via visibility timeout
- No manual intervention needed

**2. Scheduler Failure:**
- Leadership automatically transferred to another instance
- Cron jobs continue with minimal delay

**3. Database Failure:**
```bash
# Restore from backup
pg_restore -d taskscheduler backup.dump

# Recover in-progress tasks
SELECT recover_timed_out_tasks();
```

**4. Complete Outage:**
1. Restore database from backup
2. Deploy scheduler instances
3. Deploy worker instances
4. Verify cron jobs are scheduled correctly
5. Check for any tasks that need manual retry

### High Availability Checklist

- [ ] 2+ scheduler instances deployed
- [ ] Database with replication configured
- [ ] Monitoring and alerting active
- [ ] Backup strategy verified
- [ ] Recovery procedure documented and tested
- [ ] Load balancer health checks configured
