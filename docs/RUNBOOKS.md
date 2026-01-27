## Runbooks

This document contains operational runbooks for common incidents.

---

## Gateway elevated 5xx

### Symptoms

- `5xx_rate` increases on gateway
- p95 latency spikes

### Immediate actions

- Check gateway `upstream_errors_by_service`.
- Check whether a downstream dependency is failing (auth, user, payments, workflow).
- Reduce blast radius:
  - tighten rate limits per tenant temporarily
  - enable circuit breaker override if supported

### Recovery

- If one downstream is failing, isolate by:
  - returning degraded responses where safe
  - temporarily disabling non-critical endpoints
- Roll back last deploy if correlated.

---

## Auth token verification failures (sudden spike)

### Symptoms

- `401` spikes across platform
- logs show `unknown_kid` or signature failures

### Immediate actions

- Verify JWKS endpoint health.
- Check whether a key rotation is in progress.

### Recovery

- Trigger JWKS cache refresh in services.
- If rotation misconfigured:
  - re-publish previous key temporarily
  - re-issue tokens

---

## Payments mismatch / double-charge concern

### Symptoms

- customer reports duplicate charges
- webhook retries observed

### Immediate actions

- Search by `Idempotency-Key` and `payment_intent_id`.
- Check `ledger_entries` for duplicated `event_id`.

### Recovery

- If duplicates exist:
  - issue reversal entries (compensating transaction)
  - mark payment intent state appropriately
- If no duplicates:
  - provide evidence from ledger and webhook logs

---

## Workflow stuck / no progress

### Symptoms

- workflow remains RUNNING with no new events
- worker queue depth increases

### Immediate actions

- Check queue consumer lag and worker health.
- Check scheduler leadership (timers).

### Recovery

- Scale worker fleet (HPA).
- If queue partition leader unhealthy, failover or restart.
- Use workflow engine re-drive tool to re-enqueue timed-out activities.

