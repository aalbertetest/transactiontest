# Operations Guide

This document provides operational guidance for running the Workflow Engine in
production environments.

## 1. Deployment Model

- API service is stateless and horizontally scalable.
- Scheduler is leader-elected and requires multiple replicas for failover.
- Executors scale horizontally based on task throughput.
- PostgreSQL should be deployed with streaming replication and backup policies.

## 2. Scaling Considerations

### API

- Scale based on request rate and latency.
- Use autoscaling on CPU and request count.

### Scheduler

- One active leader per shard group.
- Scale by increasing shard count and adding scheduler replicas.

### Executors

- Scale based on queue depth and task processing latency.
- Ensure per-node resource limits match workload requirements.

## 3. Database Operations

- Configure `max_connections` to handle API, scheduler, and executor pools.
- Use connection pooling (e.g., PgBouncer) in production.
- Run regular vacuum and analyze to maintain performance.
- Configure PITR and WAL archiving for recovery.

## 4. Backups and Recovery

Recommended strategy:

- Daily full backups.
- Continuous WAL archiving.
- Regular restore drills.

## 5. Upgrades

1. Deploy new API version (backward compatible).
2. Deploy new scheduler (supports old schema).
3. Deploy new executors.
4. Apply database migrations.

## 6. Incident Response

Common incidents:

- **Task backlog**: scale executors, check DB pressure.
- **Scheduler failover**: verify leader election and DB availability.
- **Database latency**: verify indexes and storage I/O.

Use the runbook section in `docs/testing.md` for chaos and recovery drills.
