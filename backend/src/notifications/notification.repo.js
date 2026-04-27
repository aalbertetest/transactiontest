import crypto from 'node:crypto';

export class NotificationRepo {
  constructor(db) {
    this.db = db;
  }

  /**
   * Insert a pending notification, idempotent by `idempotencyKey`. Returns
   * `null` if a row with that key already exists (so a retry of the same
   * domain event doesn't double-enqueue).
   */
  enqueue({ idempotencyKey, userId, channel, template, payload, scheduledAt }) {
    const id = crypto.randomUUID();
    const now = Date.now();
    const result = this.db
      .prepare(
        `INSERT OR IGNORE INTO notifications
           (id, idempotency_key, user_id, channel, template, payload_json,
            status, attempts, scheduled_at, created_at)
         VALUES (?, ?, ?, ?, ?, ?, 'pending', 0, ?, ?)`,
      )
      .run(
        id,
        idempotencyKey,
        userId,
        channel,
        template,
        JSON.stringify(payload),
        scheduledAt ?? now,
        now,
      );
    if (result.changes === 0) return null;
    return this._findById(id);
  }

  /**
   * Atomically claim up to `limit` due notifications. Marks them as
   * `in_flight` so a sibling worker doesn't pick them up again. In Postgres
   * this would be `SELECT … FOR UPDATE SKIP LOCKED`.
   */
  claimDue(limit, now = Date.now()) {
    const claim = this.db.transaction((lim, ts) => {
      const rows = this.db
        .prepare(
          `SELECT id, user_id, channel, template, payload_json, attempts
           FROM notifications
           WHERE status = 'pending' AND scheduled_at <= ?
           ORDER BY scheduled_at ASC
           LIMIT ?`,
        )
        .all(ts, lim);
      if (rows.length === 0) return [];
      const placeholders = rows.map(() => '?').join(',');
      this.db
        .prepare(
          `UPDATE notifications
           SET status = 'in_flight', claimed_at = ?
           WHERE id IN (${placeholders})`,
        )
        .run(ts, ...rows.map((r) => r.id));
      return rows.map((r) => ({
        id: r.id,
        userId: r.user_id,
        channel: r.channel,
        template: r.template,
        payload: JSON.parse(r.payload_json),
        attempts: r.attempts,
      }));
    });
    return claim(limit, now);
  }

  markSent(id) {
    this.db
      .prepare(`UPDATE notifications SET status = 'sent' WHERE id = ?`)
      .run(id);
  }

  reschedule(id, scheduledAt, attempts, lastError) {
    this.db
      .prepare(
        `UPDATE notifications
         SET status = 'pending', scheduled_at = ?, attempts = ?, last_error = ?
         WHERE id = ?`,
      )
      .run(scheduledAt, attempts, lastError ?? null, id);
  }

  deadLetter(id, reason) {
    this.db
      .prepare(
        `UPDATE notifications SET status = 'dead', last_error = ? WHERE id = ?`,
      )
      .run(reason, id);
  }

  countByStatus(status) {
    return this.db
      .prepare(`SELECT COUNT(*) AS n FROM notifications WHERE status = ?`)
      .get(status).n;
  }

  _findById(id) {
    const r = this.db
      .prepare(`SELECT * FROM notifications WHERE id = ?`)
      .get(id);
    if (!r) return null;
    return {
      id: r.id,
      idempotencyKey: r.idempotency_key,
      userId: r.user_id,
      channel: r.channel,
      template: r.template,
      payload: JSON.parse(r.payload_json),
      status: r.status,
      attempts: r.attempts,
      scheduledAt: r.scheduled_at,
    };
  }
}
