-- Base schema for the distributed platform

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
