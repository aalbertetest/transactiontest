import Database from 'better-sqlite3';
import fs from 'node:fs';
import path from 'node:path';

export function openDb(dbPath) {
  if (dbPath !== ':memory:') {
    fs.mkdirSync(path.dirname(dbPath), { recursive: true });
  }
  const db = new Database(dbPath);
  db.pragma('journal_mode = WAL');
  db.pragma('foreign_keys = ON');
  migrate(db);
  return db;
}

function migrate(db) {
  db.exec(`
    CREATE TABLE IF NOT EXISTS users (
      id            TEXT PRIMARY KEY,
      email         TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      created_at    INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS refresh_tokens (
      id          TEXT PRIMARY KEY,
      user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      token_hash  TEXT NOT NULL UNIQUE,
      expires_at  INTEGER NOT NULL,
      revoked_at  INTEGER,
      created_at  INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_refresh_user ON refresh_tokens(user_id);

    CREATE TABLE IF NOT EXISTS tasks (
      id          TEXT PRIMARY KEY,
      user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      title       TEXT NOT NULL,
      description TEXT,
      status      TEXT NOT NULL CHECK (status IN ('todo','doing','done')),
      due_at      INTEGER,
      created_at  INTEGER NOT NULL,
      updated_at  INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_tasks_user_created
      ON tasks(user_id, created_at DESC, id DESC);
    CREATE INDEX IF NOT EXISTS idx_tasks_user_status_created
      ON tasks(user_id, status, created_at DESC, id DESC);

    CREATE TABLE IF NOT EXISTS user_prefs (
      user_id     TEXT PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
      prefs_json  TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS notifications (
      id              TEXT PRIMARY KEY,
      idempotency_key TEXT NOT NULL UNIQUE,
      user_id         TEXT NOT NULL,
      channel         TEXT NOT NULL,
      template        TEXT NOT NULL,
      payload_json    TEXT NOT NULL,
      status          TEXT NOT NULL CHECK (status IN ('pending','in_flight','sent','dead')),
      attempts        INTEGER NOT NULL DEFAULT 0,
      scheduled_at    INTEGER NOT NULL,
      claimed_at      INTEGER,
      last_error      TEXT,
      created_at      INTEGER NOT NULL
    );
    CREATE INDEX IF NOT EXISTS idx_notifications_due
      ON notifications(status, scheduled_at);
  `);
}
