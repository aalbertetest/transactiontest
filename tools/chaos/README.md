# Chaos Testing Scripts

These scripts intentionally terminate pods to validate failover and retry logic.

## Kill Executors

```
NAMESPACE=workflow-engine COUNT=2 ./tools/chaos/kill-executors.sh
```

Expected outcome: queued tasks are retried and completed by remaining workers.

## Kill Scheduler Leader

```
NAMESPACE=workflow-engine ./tools/chaos/kill-scheduler.sh
```

Expected outcome: a standby scheduler acquires the leader lock and resumes
task scheduling within the lease TTL.
