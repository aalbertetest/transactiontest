import { describe, it, expect, beforeEach } from 'vitest';
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

class RecordingTransport {
  constructor() { this.sent = []; }
  async send({ to, message }) { this.sent.push({ to, message }); }
}

class FlakyTransport {
  constructor(failuresBeforeSuccess) {
    this.remaining = failuresBeforeSuccess;
    this.sent = [];
  }
  async send({ to, message }) {
    if (this.remaining > 0) {
      this.remaining -= 1;
      throw new Error('transient');
    }
    this.sent.push({ to, message });
  }
}

class AlwaysFailingTransport {
  async send() { throw new Error('boom'); }
}

async function setup({ transports }) {
  const ctx = buildApp({ config, db: openDb(':memory:'), transports });
  // A user + due-dated task -> dispatcher enqueues a notification.
  const tokens = await ctx.services.auth.register({
    email: 'a@example.com',
    password: 'correcthorsebattery',
  });
  const userId = ctx.repos.users.findByEmail('a@example.com').id;
  return { ctx, tokens, userId };
}

describe('notifications', () => {
  let now;
  let nowFn;

  beforeEach(() => {
    // Anchor the worker clock to "now" because the dispatcher uses the real
    // clock when stamping `scheduled_at` on enqueued rows.
    now = Date.now() + 1000;
    nowFn = () => now;
  });

  it('enqueues + sends a notification when a due task is created', async () => {
    const transport = new RecordingTransport();
    const { ctx, userId } = await setup({ transports: { console: transport } });
    ctx.worker.now = nowFn;

    await ctx.services.tasks.create(userId, {
      title: 'pay bill',
      status: 'todo',
      dueAt: new Date(now + 3600_000).toISOString(),
    });

    const drained = await ctx.worker.tick();
    expect(drained).toBe(1);
    expect(transport.sent).toHaveLength(1);
    expect(transport.sent[0].to).toBe('a@example.com');
    expect(transport.sent[0].message.subject).toContain('pay bill');
  });

  it('does NOT enqueue when the task has no dueAt', async () => {
    const transport = new RecordingTransport();
    const { ctx, userId } = await setup({ transports: { console: transport } });
    ctx.worker.now = nowFn;

    await ctx.services.tasks.create(userId, { title: 'no due', status: 'todo' });
    const drained = await ctx.worker.tick();
    expect(drained).toBe(0);
    expect(transport.sent).toHaveLength(0);
  });

  it('retries with exponential backoff and eventually succeeds', async () => {
    const transport = new FlakyTransport(2);
    const { ctx, userId } = await setup({ transports: { console: transport } });
    ctx.worker.now = nowFn;
    ctx.worker.backoffMs = (n) => 1000 * n; // deterministic

    await ctx.services.tasks.create(userId, {
      title: 'flaky',
      status: 'todo',
      dueAt: new Date(now + 3600_000).toISOString(),
    });

    expect(await ctx.worker.tick()).toBe(1);
    expect(transport.sent).toHaveLength(0);
    expect(ctx.repos.notes.countByStatus('pending')).toBe(1);

    now += 5_000;
    expect(await ctx.worker.tick()).toBe(1);
    expect(transport.sent).toHaveLength(0);

    now += 10_000;
    expect(await ctx.worker.tick()).toBe(1);
    expect(transport.sent).toHaveLength(1);
    expect(ctx.repos.notes.countByStatus('sent')).toBe(1);
  });

  it('dead-letters after max attempts', async () => {
    const transport = new AlwaysFailingTransport();
    const { ctx, userId } = await setup({ transports: { console: transport } });
    ctx.worker.now = nowFn;
    ctx.worker.maxAttempts = 3;
    ctx.worker.backoffMs = () => 0;

    await ctx.services.tasks.create(userId, {
      title: 'doomed',
      status: 'todo',
      dueAt: new Date(now + 3600_000).toISOString(),
    });

    for (let i = 0; i < 3; i++) {
      await ctx.worker.tick();
      now += 1; // ensure scheduled_at <= now
    }

    expect(ctx.repos.notes.countByStatus('dead')).toBe(1);
    expect(ctx.repos.notes.countByStatus('pending')).toBe(0);
  });

  it('is idempotent on duplicate enqueue with the same key', async () => {
    const { ctx, userId } = await setup({ transports: { console: new RecordingTransport() } });
    const first = ctx.repos.notes.enqueue({
      idempotencyKey: 'evt-1:user-1:console',
      userId,
      channel: 'console',
      template: 'task.created',
      payload: { taskId: 't1', title: 'x', recipient: 'a@example.com' },
    });
    const second = ctx.repos.notes.enqueue({
      idempotencyKey: 'evt-1:user-1:console',
      userId,
      channel: 'console',
      template: 'task.created',
      payload: { taskId: 't1', title: 'x', recipient: 'a@example.com' },
    });
    expect(first).not.toBeNull();
    expect(second).toBeNull();
    expect(ctx.repos.notes.countByStatus('pending')).toBe(1);
  });
});
