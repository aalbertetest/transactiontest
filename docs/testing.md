# Testing, Load, and Chaos Engineering

This document covers testing, load validation, and chaos scenarios.

## 1. Unit Tests

- API: validation and handler logic.
- Scheduler: shard and scheduling logic.
- Executor: task execution and retry logic.

## 2. Integration Tests

- Use a real PostgreSQL instance.
- Validate end-to-end workflow creation, scheduling, execution.

## 3. Load Testing

The load test script is located at `tools/loadtest/k6-workflows.js`.

Example:

```
k6 run tools/loadtest/k6-workflows.js
```

The script creates workflows and triggers runs at configurable rates.

## 4. Chaos Testing

Chaos scripts and manifests are under `tools/chaos`.

Examples:

- Kill executor pods to validate task retries.
- Kill scheduler leader to validate failover.
- Induce DB latency to test backpressure.

## 5. Runbook Scenarios

### Scenario: Scheduler Failover

1. Identify current leader via logs or metrics.
2. Kill leader pod.
3. Confirm a new leader acquires the lock and resumes scheduling.

### Scenario: Task Backlog

1. Observe queue depth metric.
2. Scale executor replicas.
3. Confirm backlog drains.

### Scenario: DB Failover

1. Promote replica to primary.
2. Update service endpoints.
3. Verify services reconnect and continue.
