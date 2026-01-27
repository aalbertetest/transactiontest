## Data

This document defines:

- SQL schemas
- NoSQL schemas
- Migrations
- Index strategies
- Partitioning strategies

DSP uses a **polyglot persistence model**:

- **SQL** (PostgreSQL) for strongly consistent metadata and financial ledger
- **KV/Log store** (Cassandra/DynamoDB-like) for workflow histories and high-volume append logs
- **Cache** (Redis-like) for ephemeral and high-QPS state

---

## SQL schemas (PostgreSQL)

### Naming conventions

- Primary keys are string IDs (ULID-like), sortable by time:
  - `ten_...`, `usr_...`, `pi_...`, `wf_...`
- Monetary values stored as integer minor units (`amount_cents` style), but named `amount` for clarity.

### Core tables

#### `tenants`

- `id` (PK)
- `name`
- `created_at`

#### `users`

- `id` (PK)
- `tenant_id` (FK -> tenants.id)
- `email` (unique per tenant)
- `password_hash` (argon2/bcrypt)
- `mfa_totp_secret_encrypted` (nullable)
- `created_at`

Indexes:

- `uniq_users_tenant_email (tenant_id, email)`
- `idx_users_tenant_created_at (tenant_id, created_at desc)`

#### `oauth_clients`

- `id` (PK)
- `tenant_id`
- `client_id` (unique)
- `client_secret_hash`
- `redirect_uris` (jsonb)
- `scopes` (text[])
- `created_at`

#### `refresh_tokens`

- `id` (PK)
- `tenant_id`
- `user_id`
- `token_hash`
- `expires_at`
- `revoked_at` (nullable)
- `created_at`

Indexes:

- `idx_refresh_tokens_user (tenant_id, user_id, created_at desc)`
- `idx_refresh_tokens_expiry (expires_at)`

#### `idempotency_keys`

- `id` (PK)
- `tenant_id`
- `endpoint` (text)
- `idempotency_key` (text)
- `request_hash` (text)
- `response_status` (int)
- `response_body_json` (jsonb)
- `locked_at` (nullable)
- `created_at`

Uniqueness:

- `uniq_idem (tenant_id, endpoint, idempotency_key)`

#### `payment_intents`

- `id` (PK)
- `tenant_id`
- `status` (enum-like text)
- `amount` (bigint)
- `currency` (char(3))
- `customer_id` (text, nullable)
- `description` (text, nullable)
- `created_at`

Indexes:

- `idx_pi_tenant_created (tenant_id, created_at desc)`
- `idx_pi_tenant_status (tenant_id, status, created_at desc)`

#### `ledger_entries`

Double-entry ledger (append-only).

- `id` (PK)
- `tenant_id`
- `payment_intent_id` (nullable)
- `account` (text)
- `direction` (DEBIT/CREDIT)
- `amount` (bigint)
- `currency` (char(3))
- `event_id` (unique per tenant) (dedupe)
- `created_at`

Indexes:

- `idx_ledger_tenant_created (tenant_id, created_at desc)`
- `idx_ledger_pi (tenant_id, payment_intent_id)`
- `uniq_ledger_event (tenant_id, event_id)`

#### `outbox_events`

- `id` (PK)
- `tenant_id`
- `topic` (text)
- `key` (text)
- `payload_json` (jsonb)
- `headers_json` (jsonb)
- `delivered_at` (nullable)
- `created_at`

Indexes:

- `idx_outbox_undelivered (delivered_at, created_at)`
- `idx_outbox_tenant_topic (tenant_id, topic, created_at desc)`

---

## NoSQL schemas (KV/Log store)

### Workflow history store

Partition key:

- `tenant_id#workflow_id`

Sort key:

- `run_id#event_sequence`

Record:

- `event_type`
- `event_payload_json`
- `event_time`

Properties:

- Append-only.
- Reads are sequential scans by run.
- Compaction/retention policies can snapshot and truncate old history segments.

### Stream log segments

Partition key:

- `topic#partition`

Sort key:

- `offset`

Record:

- `timestamp`
- `key`
- `value`
- `headers`

Retention:

- time-based (e.g., 7 days)
- size-based (per partition)

---

## Migrations

Migrations are organized as:

- `infra/migrations/postgres/NNNN_description.sql`

Rules:

- Forward-only migrations.
- For large tables:
  - avoid blocking DDL
  - create indexes concurrently
  - backfill in batches

---

## Index strategies

- Use composite indexes to match query shapes:
  - multi-tenant filters start with `tenant_id`
  - time-range queries include `created_at`
- Prefer partial indexes for hot subsets:
  - payment intents by `status in ('PROCESSING','REQUIRES_CONFIRMATION')`
- Ledger:
  - keep append-only; index by `(tenant_id, created_at)` and `(tenant_id, event_id)`

---

## Partitioning strategies

### SQL partitioning

- `ledger_entries`: partition by month on `created_at` for very large tenants (optional)
- `outbox_events`: partition by day/month, prune after retention

### Stream partitioning

- Partition key = `tenant_id` by default for fairness.
- For ordering constraints:
  - key by `tenant_id#workflow_id` for workflow-specific ordering.

