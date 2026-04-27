import crypto from 'node:crypto';

export class RefreshTokenRepo {
  constructor(db) {
    this.db = db;
  }

  create({ userId, tokenHash, expiresAt }) {
    const id = crypto.randomUUID();
    const createdAt = Date.now();
    this.db
      .prepare(
        `INSERT INTO refresh_tokens (id, user_id, token_hash, expires_at, created_at)
         VALUES (?, ?, ?, ?, ?)`,
      )
      .run(id, userId, tokenHash, expiresAt, createdAt);
    return { id, userId, tokenHash, expiresAt, createdAt, revokedAt: null };
  }

  findByHash(tokenHash) {
    const row = this.db
      .prepare(
        `SELECT id, user_id, token_hash, expires_at, revoked_at
         FROM refresh_tokens WHERE token_hash = ?`,
      )
      .get(tokenHash);
    if (!row) return null;
    return {
      id: row.id,
      userId: row.user_id,
      tokenHash: row.token_hash,
      expiresAt: row.expires_at,
      revokedAt: row.revoked_at,
    };
  }

  revoke(id) {
    this.db
      .prepare('UPDATE refresh_tokens SET revoked_at = ? WHERE id = ?')
      .run(Date.now(), id);
  }
}
