# Payment Processing System - Architecture

This repo provides a production-grade reference implementation of a payment
processing system in Python, Go, and TypeScript. It focuses on PCI concepts,
idempotency, retries, webhook delivery, fraud detection, schemas, APIs, and
worker-driven processing.

## High-level goals

- Keep PCI scope minimal by never storing PAN/CVV.
- Use tokenized payment methods and vault integration.
- Guarantee idempotency for all state-changing requests.
- Use retries with jitter and bounded backoff for external calls.
- Emit events to an outbox and deliver webhooks with signatures.
- Run all long-running work in workers for reliability and scale.

## Core services

1. API service
   - Authenticates merchant requests.
   - Accepts PaymentIntent creation, confirmation, refunds.
   - Enforces idempotency and emits domain events.
2. Worker service
   - Processes payment confirmations/captures.
   - Performs fraud checks and risk scoring.
   - Delivers webhooks with retry policies.

## PCI scope and card data handling

PCI concepts included in code and docs:

- Tokenization: API accepts a payment_method_token only. Raw PAN/CVV are
  handled by a PCI-compliant vault or a hosted fields/redirect flow.
- Minimal data storage: no PAN/CVV stored; only last4, brand, expiry month/year.
- Encryption at rest: secrets are encrypted using KMS/HSM in production.
- Network segmentation: PCI systems are isolated and access is restricted.
- Auditability: all access to sensitive operations is logged.
- Key rotation: webhook signing and encryption keys rotate regularly.
- Least privilege: each service uses scoped credentials.

## Idempotency

- Each POST endpoint accepts Idempotency-Key header.
- The system stores a hash of the request payload with the key.
- Replays of the same key return the exact prior response.
- Conflicts (same key, different payload) return 409.

## Retries and backoff

- All outbound calls (processor, webhooks) use bounded exponential backoff.
- Retries include jitter to avoid thundering herds.
- A max retry count and a dead-letter state is enforced.

## Webhooks

- Events are stored in an outbox table before delivery.
- Webhook deliveries use HMAC-SHA256 signatures.
- A delivery record is created for each attempt.
- Failures are retried by the worker with backoff and final state tracked.

## Fraud detection

The risk engine applies:

- Velocity rules: limit attempts per card and per customer.
- Amount rules: blocks suspicious high-value payments for new customers.
- IP/geo mismatches (demo uses a simple country check).
- Custom blocklists/allowlists.

Fraud rules are modeled as a scoring pipeline that outputs:

- risk_score (0-100)
- decision: allow, review, block

## Data flow (simplified)

1. Merchant creates PaymentIntent -> status: requires_confirmation
2. Merchant confirms PaymentIntent -> worker processes:
   - Fraud checks
   - External processor authorization/capture
   - Persist charge, emit event
3. Webhook worker delivers events to merchant endpoint

## Observability

- Structured logs with correlation IDs.
- Metrics: success rates, p95 latency, webhook retry counts.
- Tracing: trace headers propagated across services.

## Failure modes

- Duplicate requests are handled via idempotency.
- Processor timeouts produce retryable states.
- Webhook failures are retried, then marked failed.

