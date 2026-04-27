import { describe, it, expect, beforeEach } from 'vitest';
import request from 'supertest';
import { buildApp } from '../src/app.js';
import { openDb } from '../src/db.js';

const config = {
  jwtSecret: 'a'.repeat(64),
  port: 0,
  dbPath: ':memory:',
  bcryptCost: 4,
  accessTtl: '15m',
  refreshTtlMs: 1000 * 60 * 60,
};

async function makeUser(app, email) {
  const res = await request(app)
    .post('/auth/register')
    .send({ email, password: 'correcthorsebattery' });
  return res.body.accessToken;
}

describe('tasks', () => {
  let ctx;
  beforeEach(() => {
    ctx = buildApp({ config, db: openDb(':memory:') });
  });

  it('rejects unauthenticated requests', async () => {
    const res = await request(ctx.app).get('/tasks');
    expect(res.status).toBe(401);
  });

  it('creates and lists tasks for the owner', async () => {
    const token = await makeUser(ctx.app, 'a@example.com');
    const create = await request(ctx.app)
      .post('/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: 'first' });
    expect(create.status).toBe(201);
    expect(create.body.status).toBe('todo');

    const list = await request(ctx.app)
      .get('/tasks')
      .set('Authorization', `Bearer ${token}`);
    expect(list.status).toBe(200);
    expect(list.body.items).toHaveLength(1);
    expect(list.body.items[0].title).toBe('first');
  });

  it('forbids access to another user’s task', async () => {
    const tokA = await makeUser(ctx.app, 'a@example.com');
    const tokB = await makeUser(ctx.app, 'b@example.com');

    const create = await request(ctx.app)
      .post('/tasks')
      .set('Authorization', `Bearer ${tokA}`)
      .send({ title: 'mine' });
    const taskId = create.body.id;

    const stolen = await request(ctx.app)
      .get(`/tasks/${taskId}`)
      .set('Authorization', `Bearer ${tokB}`);
    expect(stolen.status).toBe(403);

    const stolenDelete = await request(ctx.app)
      .delete(`/tasks/${taskId}`)
      .set('Authorization', `Bearer ${tokB}`);
    expect(stolenDelete.status).toBe(403);
  });

  it('paginates with a stable cursor', async () => {
    const token = await makeUser(ctx.app, 'a@example.com');
    for (let i = 0; i < 5; i++) {
      await request(ctx.app)
        .post('/tasks')
        .set('Authorization', `Bearer ${token}`)
        .send({ title: `t${i}` });
    }

    const page1 = await request(ctx.app)
      .get('/tasks?limit=2')
      .set('Authorization', `Bearer ${token}`);
    expect(page1.body.items).toHaveLength(2);
    expect(page1.body.nextCursor).toBeTruthy();

    const page2 = await request(ctx.app)
      .get(`/tasks?limit=2&cursor=${encodeURIComponent(page1.body.nextCursor)}`)
      .set('Authorization', `Bearer ${token}`);
    expect(page2.body.items).toHaveLength(2);

    const ids1 = page1.body.items.map((t) => t.id);
    const ids2 = page2.body.items.map((t) => t.id);
    for (const id of ids2) expect(ids1).not.toContain(id);
  });

  it('rejects SQL-shaped junk in fields', async () => {
    const token = await makeUser(ctx.app, 'a@example.com');
    const res = await request(ctx.app)
      .post('/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: '', status: 'banana' });
    expect(res.status).toBe(400);
  });
});
