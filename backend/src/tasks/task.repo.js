import crypto from 'node:crypto';

export class TaskRepo {
  constructor(db) {
    this.db = db;
  }

  create({ userId, title, description, status, dueAt }) {
    const id = crypto.randomUUID();
    const now = Date.now();
    const dueAtMs = dueAt ? Date.parse(dueAt) : null;
    this.db
      .prepare(
        `INSERT INTO tasks (id, user_id, title, description, status, due_at, created_at, updated_at)
         VALUES (?, ?, ?, ?, ?, ?, ?, ?)`,
      )
      .run(id, userId, title, description ?? null, status, dueAtMs, now, now);
    return this.findById(id);
  }

  findById(id) {
    const row = this.db
      .prepare(
        `SELECT id, user_id, title, description, status, due_at, created_at, updated_at
         FROM tasks WHERE id = ?`,
      )
      .get(id);
    return row ? rowToTask(row) : null;
  }

  update(id, patch) {
    const sets = [];
    const params = { id };
    if ('title' in patch) {
      sets.push('title = @title');
      params.title = patch.title;
    }
    if ('description' in patch) {
      sets.push('description = @description');
      params.description = patch.description ?? null;
    }
    if ('status' in patch) {
      sets.push('status = @status');
      params.status = patch.status;
    }
    if ('dueAt' in patch) {
      sets.push('due_at = @dueAt');
      params.dueAt = patch.dueAt ? Date.parse(patch.dueAt) : null;
    }
    sets.push('updated_at = @updatedAt');
    params.updatedAt = Date.now();
    this.db
      .prepare(`UPDATE tasks SET ${sets.join(', ')} WHERE id = @id`)
      .run(params);
    return this.findById(id);
  }

  delete(id) {
    this.db.prepare('DELETE FROM tasks WHERE id = ?').run(id);
  }

  listForUser(userId, { status, cursor, limit }) {
    const where = ['user_id = @userId'];
    const params = { userId, limit };
    if (status) {
      where.push('status = @status');
      params.status = status;
    }
    if (cursor) {
      const decoded = decodeCursor(cursor);
      if (decoded) {
        where.push('(created_at < @cAt OR (created_at = @cAt AND id < @cId))');
        params.cAt = decoded.createdAt;
        params.cId = decoded.id;
      }
    }
    const rows = this.db
      .prepare(
        `SELECT id, user_id, title, description, status, due_at, created_at, updated_at
         FROM tasks
         WHERE ${where.join(' AND ')}
         ORDER BY created_at DESC, id DESC
         LIMIT @limit`,
      )
      .all(params);
    const items = rows.map(rowToTask);
    const nextCursor =
      items.length === limit
        ? encodeCursor({
            createdAt: items[items.length - 1].createdAt,
            id: items[items.length - 1].id,
          })
        : null;
    return { items, nextCursor };
  }
}

function rowToTask(r) {
  return {
    id: r.id,
    userId: r.user_id,
    title: r.title,
    description: r.description,
    status: r.status,
    dueAt: r.due_at ? new Date(r.due_at).toISOString() : null,
    createdAt: r.created_at,
    updatedAt: r.updated_at,
  };
}

function encodeCursor(c) {
  return Buffer.from(JSON.stringify(c)).toString('base64url');
}
function decodeCursor(s) {
  try {
    const obj = JSON.parse(Buffer.from(s, 'base64url').toString('utf8'));
    if (typeof obj.createdAt === 'number' && typeof obj.id === 'string') return obj;
    return null;
  } catch {
    return null;
  }
}
