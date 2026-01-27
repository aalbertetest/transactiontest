Data Models, Schemas, and Migrations
====================================

This platform uses a hybrid data model:

* SQL for transactional data (users, payments, workflow state).
* NoSQL (document store) for event logs and large payloads.
* Time-partitioned tables for high-volume logs.

SQL Schema (Logical)
--------------------

Users and Organizations
-----------------------

CREATE TABLE users (
  id              TEXT PRIMARY KEY,
  email           TEXT UNIQUE NOT NULL,
  display_name    TEXT NOT NULL,
  status          TEXT NOT NULL,
  created_at      TIMESTAMP NOT NULL,
  updated_at      TIMESTAMP NOT NULL
);

CREATE TABLE orgs (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  owner_id    TEXT NOT NULL REFERENCES users(id),
  created_at  TIMESTAMP NOT NULL
);

CREATE TABLE memberships (
  user_id     TEXT NOT NULL REFERENCES users(id),
  org_id      TEXT NOT NULL REFERENCES orgs(id),
  role        TEXT NOT NULL,
  PRIMARY KEY (user_id, org_id)
);

Authentication
--------------

CREATE TABLE oauth_clients (
  client_id           TEXT PRIMARY KEY,
  client_secret_hash  TEXT NOT NULL,
  redirect_uris       TEXT NOT NULL,
  scopes              TEXT NOT NULL,
  created_at          TIMESTAMP NOT NULL
);

CREATE TABLE auth_codes (
  code        TEXT PRIMARY KEY,
  client_id   TEXT NOT NULL REFERENCES oauth_clients(client_id),
  user_id     TEXT NOT NULL REFERENCES users(id),
  expires_at  TIMESTAMP NOT NULL
);

CREATE TABLE refresh_tokens (
  token       TEXT PRIMARY KEY,
  user_id     TEXT NOT NULL REFERENCES users(id),
  expires_at  TIMESTAMP NOT NULL
);

CREATE TABLE mfa_secrets (
  user_id     TEXT PRIMARY KEY REFERENCES users(id),
  secret      TEXT NOT NULL,
  enabled     BOOLEAN NOT NULL,
  created_at  TIMESTAMP NOT NULL
);

Payments
--------

CREATE TABLE payment_intents (
  id                TEXT PRIMARY KEY,
  user_id           TEXT NOT NULL REFERENCES users(id),
  amount            BIGINT NOT NULL,
  currency          TEXT NOT NULL,
  status            TEXT NOT NULL,
  idempotency_key   TEXT NOT NULL,
  created_at        TIMESTAMP NOT NULL,
  updated_at        TIMESTAMP NOT NULL
);

CREATE TABLE charges (
  id                TEXT PRIMARY KEY,
  intent_id         TEXT NOT NULL REFERENCES payment_intents(id),
  status            TEXT NOT NULL,
  processor_ref     TEXT NOT NULL,
  created_at        TIMESTAMP NOT NULL
);

CREATE TABLE refunds (
  id                TEXT PRIMARY KEY,
  charge_id         TEXT NOT NULL REFERENCES charges(id),
  amount            BIGINT NOT NULL,
  status            TEXT NOT NULL,
  created_at        TIMESTAMP NOT NULL
);

Workflows
---------

CREATE TABLE workflows (
  id          TEXT PRIMARY KEY,
  name        TEXT NOT NULL,
  version     INTEGER NOT NULL,
  definition  TEXT NOT NULL,
  created_at  TIMESTAMP NOT NULL
);

CREATE TABLE workflow_runs (
  id            TEXT PRIMARY KEY,
  workflow_id   TEXT NOT NULL REFERENCES workflows(id),
  status        TEXT NOT NULL,
  current_step  TEXT NOT NULL,
  history       TEXT NOT NULL,
  created_at    TIMESTAMP NOT NULL,
  updated_at    TIMESTAMP NOT NULL
);

CREATE TABLE tasks (
  id           TEXT PRIMARY KEY,
  run_id       TEXT NOT NULL REFERENCES workflow_runs(id),
  step         TEXT NOT NULL,
  payload      TEXT NOT NULL,
  attempt      INTEGER NOT NULL,
  status       TEXT NOT NULL,
  created_at   TIMESTAMP NOT NULL,
  updated_at   TIMESTAMP NOT NULL
);

Queues and Streams
------------------

CREATE TABLE queue_messages (
  id          TEXT PRIMARY KEY,
  queue_name  TEXT NOT NULL,
  payload     TEXT NOT NULL,
  attempt     INTEGER NOT NULL,
  visible_at  TIMESTAMP NOT NULL,
  created_at  TIMESTAMP NOT NULL
);

CREATE TABLE stream_topics (
  name               TEXT PRIMARY KEY,
  partitions         INTEGER NOT NULL,
  retention_seconds  INTEGER NOT NULL,
  created_at         TIMESTAMP NOT NULL
);

CREATE TABLE stream_records (
  topic       TEXT NOT NULL,
  partition   INTEGER NOT NULL,
  offset      BIGINT NOT NULL,
  key         TEXT NOT NULL,
  value       TEXT NOT NULL,
  timestamp   TIMESTAMP NOT NULL,
  PRIMARY KEY (topic, partition, offset)
);

Schedules
---------

CREATE TABLE schedules (
  id          TEXT PRIMARY KEY,
  cron        TEXT NOT NULL,
  payload     TEXT NOT NULL,
  enabled     BOOLEAN NOT NULL,
  created_at  TIMESTAMP NOT NULL
);

CREATE TABLE scheduled_tasks (
  id           TEXT PRIMARY KEY,
  schedule_id  TEXT NOT NULL REFERENCES schedules(id),
  run_at       TIMESTAMP NOT NULL,
  status       TEXT NOT NULL
);

NoSQL Schemas
-------------

Document Store Collections:

1) events
  {
    "_id": "uuid",
    "type": "payment.charge.succeeded",
    "source": "payments-service",
    "subject": "charge:ch_123",
    "time": "2026-01-27T00:00:00Z",
    "data": { ... }
  }

2) audit_logs
  {
    "_id": "uuid",
    "actor": "user:usr_1",
    "action": "payments.charge",
    "resource": "charge:ch_123",
    "timestamp": "2026-01-27T00:00:00Z",
    "metadata": { ... }
  }

Migrations
----------

See db/migrations/001_init.sql and db/migrations/002_indexes.sql for the full
schema and indexing strategy.

Index Strategy
--------------

* users.email UNIQUE index for login.
* payment_intents.idempotency_key index for idempotent requests.
* queue_messages.queue_name + visible_at for efficient polling.
* stream_records(topic, partition, offset) clustered primary key.
* workflow_runs.workflow_id + status for workflow querying.
* scheduled_tasks(run_at) index for scheduler efficiency.

Partitioning Strategy
---------------------

* stream_records are partitioned by topic and partition number.
* queue_messages can be sharded by queue_name hash.
* workflow_runs can be partitioned by workflow_id hash to scale.
* audit_logs and events in NoSQL are partitioned by time (daily).
