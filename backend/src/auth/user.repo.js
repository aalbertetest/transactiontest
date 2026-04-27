import crypto from 'node:crypto';

export class UserRepo {
  constructor(db) {
    this.db = db;
  }

  findByEmail(email) {
    const row = this.db
      .prepare('SELECT id, email, password_hash, created_at FROM users WHERE email = ?')
      .get(email);
    return row ? rowToUser(row) : null;
  }

  findById(id) {
    const row = this.db
      .prepare('SELECT id, email, password_hash, created_at FROM users WHERE id = ?')
      .get(id);
    return row ? rowToUser(row) : null;
  }

  create({ email, passwordHash }) {
    const id = crypto.randomUUID();
    const createdAt = Date.now();
    this.db
      .prepare(
        `INSERT INTO users (id, email, password_hash, created_at)
         VALUES (?, ?, ?, ?)`,
      )
      .run(id, email, passwordHash, createdAt);
    return { id, email, passwordHash, createdAt };
  }
}

function rowToUser(r) {
  return {
    id: r.id,
    email: r.email,
    passwordHash: r.password_hash,
    createdAt: r.created_at,
  };
}
