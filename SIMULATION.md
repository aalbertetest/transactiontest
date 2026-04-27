# Startup Engineering Team Simulation

> A four-person engineering team builds a task-management backend across three
> feature cycles. Each cycle follows the same loop: **CTO designs → Junior
> implements (badly) → Reviewer tears it apart → Senior rewrites → CTO
> evaluates scalability**.
>
> The "final" Senior implementations are also materialized as runnable code in
> [`backend/`](./backend) so this simulation isn't just theatre — the code at
> the end of each cycle actually runs.

**Cast**

| Role | Name | Personality |
|------|------|-------------|
| CTO | Priya | Pragmatic, thinks in trade-offs and 10x-load thought experiments |
| Senior Engineer | Marcus | Boring-tech evangelist, loves boundaries and tests |
| Junior Engineer | Devon | Keen, ships fast, hasn't been burned yet |
| Reviewer | Sam | Ex-platform engineer, allergic to hand-waving |

**Stack chosen up-front**

- Node.js + Express
- SQLite (better-sqlite3) for local dev; the data layer is abstracted so
  Postgres is a drop-in swap
- JWT (access) + opaque refresh tokens
- `zod` for validation, `bcrypt` for password hashing
- An in-process pub/sub notification bus with a pluggable transport
  (`console`, `email`, `webhook`)

---

## Standup 0 — Kickoff

**Priya (CTO):** "We're building a task manager backend. Three vertical slices:
auth, task CRUD, notifications. Constraints: single region to start, but I want
the code to survive a Postgres migration and a worker fleet without a rewrite.
No premature microservices. We optimize for *reversibility*, not cleverness."

**Marcus (Senior):** "I'd like a domain layer that doesn't import Express, and a
thin HTTP layer that doesn't know about SQL. Boring boundaries."

**Devon (Junior):** "I can have a working version by end of day."

**Sam (Reviewer):** "I will read every line."

---

# Cycle 1 — Auth system

## 1.1 CTO design

**Priya:** "Requirements:

1. Email + password registration; passwords hashed with bcrypt (cost ≥ 12).
2. Short-lived JWT access tokens (15 min), opaque refresh tokens stored
   server-side so we can revoke.
3. Rate limit `/login` per IP and per email to slow credential stuffing.
4. Constant-time response on login failures — no user enumeration via timing or
   error messages.
5. All auth state behind an `AuthService` interface so we can swap to OAuth or
   a managed provider later.

Non-goals for v1: SSO, MFA, password reset (tracked, not built today)."

```
┌──────────────┐   POST /auth/register     ┌─────────────────┐
│              │ ─────────────────────────▶│                 │
│  HTTP layer  │   POST /auth/login         │  AuthService     │──▶ UserRepo
│  (Express)   │ ─────────────────────────▶│  (domain logic)  │──▶ TokenRepo
│              │   POST /auth/refresh       │                 │
└──────────────┘ ─────────────────────────▶└─────────────────┘
```

## 1.2 Junior's first version (intentionally flawed)

**Devon:** "Done! Login works, register works, I even put the secret in the
code so we don't forget it."

```js
// auth.js  — Devon's v1
const express = require('express');
const jwt = require('jsonwebtoken');
const router = express.Router();
const users = []; // in-memory, who needs a DB

const SECRET = 'supersecret123';

router.post('/register', (req, res) => {
  const { email, password } = req.body;
  users.push({ email, password });
  res.send('ok');
});

router.post('/login', (req, res) => {
  const { email, password } = req.body;
  const user = users.find(u => u.email === email);
  if (!user) return res.status(404).send('user not found');
  if (user.password !== password) return res.status(401).send('wrong password');
  const token = jwt.sign({ email }, SECRET);
  res.json({ token });
});

router.get('/me', (req, res) => {
  const token = req.headers.authorization.split(' ')[1];
  const data = jwt.verify(token, SECRET);
  res.json(data);
});

module.exports = router;
```

## 1.3 Reviewer tears it apart

**Sam:** "I have a list. Sit down.

1. **Plaintext passwords.** You're storing them in memory, unhashed. If this
   process ever gets a heap dump shipped to a logging service, every account is
   compromised forever. Use bcrypt with a cost factor and *never* keep the
   plaintext in any variable longer than necessary.
2. **Hardcoded secret in source.** `'supersecret123'` is now in git history.
   Rotate it, then move it to env, then add a check that refuses to boot if
   `JWT_SECRET` is missing or shorter than 32 bytes.
3. **User enumeration.** `404 user not found` vs `401 wrong password` lets an
   attacker harvest valid emails. Return the *same* generic error and take
   roughly the same time on both paths.
4. **No token expiry, no refresh.** `jwt.sign` with no `expiresIn`? That token
   is valid until the heat death of the universe. And there's no revocation
   path — if a laptop is stolen, you have no story.
5. **`/me` will crash on missing header.** `req.headers.authorization.split`
   throws `TypeError` and Express returns a 500 with a stack trace. Fantastic
   recon for an attacker.
6. **No validation.** I can register with `email = { $ne: null }` or a 10MB
   password. You haven't typed the input.
7. **No rate limiting.** I will brute-force this in an afternoon.
8. **In-memory `users` array.** Restart the process and everyone's account
   evaporates. Also: not safe across workers.
9. **No tests.** None. Zero. I refuse to merge.

This is not a code review, this is a security incident waiting for a calendar
invite."

**Devon:** "...okay, fair."

## 1.4 Senior rewrites it properly

**Marcus:** "I'll split this into HTTP, service, and repo layers. The service
doesn't know what Express is; the repo doesn't know what HTTP is. That keeps
the test surface small."

```ts
// src/auth/auth.schema.ts
import { z } from 'zod';

export const credentialsSchema = z.object({
  email: z.string().email().max(254),
  password: z.string().min(12).max(200),
});
export type Credentials = z.infer<typeof credentialsSchema>;
```

```ts
// src/auth/auth.service.ts
import bcrypt from 'bcrypt';
import crypto from 'node:crypto';
import jwt from 'jsonwebtoken';
import { Credentials } from './auth.schema';
import { UserRepo, RefreshTokenRepo } from './ports';
import { config } from '../config';

const BCRYPT_COST = 12;
const ACCESS_TTL = '15m';
const REFRESH_TTL_MS = 1000 * 60 * 60 * 24 * 30; // 30 days

export class AuthError extends Error {
  constructor(public code: 'invalid_credentials' | 'email_taken' | 'invalid_token') {
    super(code);
  }
}

export class AuthService {
  constructor(private users: UserRepo, private refreshTokens: RefreshTokenRepo) {}

  async register({ email, password }: Credentials) {
    const existing = await this.users.findByEmail(email);
    if (existing) throw new AuthError('email_taken');
    const passwordHash = await bcrypt.hash(password, BCRYPT_COST);
    const user = await this.users.create({ email, passwordHash });
    return this.issueTokens(user.id);
  }

  async login({ email, password }: Credentials) {
    const user = await this.users.findByEmail(email);
    // Always run bcrypt to keep timing roughly constant even on missing user.
    const hash = user?.passwordHash ?? '$2b$12$invalidinvalidinvalidinvalidinvalidinvalidinvalidinvali';
    const ok = await bcrypt.compare(password, hash);
    if (!user || !ok) throw new AuthError('invalid_credentials');
    return this.issueTokens(user.id);
  }

  async refresh(rawToken: string) {
    const hashed = sha256(rawToken);
    const record = await this.refreshTokens.findByHash(hashed);
    if (!record || record.revokedAt || record.expiresAt < Date.now()) {
      throw new AuthError('invalid_token');
    }
    await this.refreshTokens.revoke(record.id);
    return this.issueTokens(record.userId);
  }

  async logout(rawToken: string) {
    const record = await this.refreshTokens.findByHash(sha256(rawToken));
    if (record) await this.refreshTokens.revoke(record.id);
  }

  private async issueTokens(userId: string) {
    const accessToken = jwt.sign({ sub: userId }, config.jwtSecret, {
      expiresIn: ACCESS_TTL,
      issuer: 'tasks-api',
    });
    const raw = crypto.randomBytes(32).toString('base64url');
    await this.refreshTokens.create({
      userId,
      tokenHash: sha256(raw),
      expiresAt: Date.now() + REFRESH_TTL_MS,
    });
    return { accessToken, refreshToken: raw };
  }
}

function sha256(s: string) {
  return crypto.createHash('sha256').update(s).digest('hex');
}
```

```ts
// src/auth/auth.router.ts
import { Router } from 'express';
import { credentialsSchema } from './auth.schema';
import { AuthService, AuthError } from './auth.service';
import { rateLimit } from '../middleware/rateLimit';

export function authRouter(svc: AuthService) {
  const r = Router();

  r.post('/register',
    rateLimit({ key: req => req.ip, max: 20, windowMs: 60_000 }),
    async (req, res, next) => {
      try {
        const creds = credentialsSchema.parse(req.body);
        const tokens = await svc.register(creds);
        res.status(201).json(tokens);
      } catch (e) { next(e); }
    });

  r.post('/login',
    rateLimit({ key: req => `${req.ip}:${req.body?.email ?? ''}`, max: 10, windowMs: 60_000 }),
    async (req, res, next) => {
      try {
        const creds = credentialsSchema.parse(req.body);
        const tokens = await svc.login(creds);
        res.json(tokens);
      } catch (e) { next(e); }
    });

  r.post('/refresh', async (req, res, next) => {
    try {
      const { refreshToken } = req.body ?? {};
      if (typeof refreshToken !== 'string') throw new AuthError('invalid_token');
      res.json(await svc.refresh(refreshToken));
    } catch (e) { next(e); }
  });

  return r;
}
```

Notes on what changed and *why*:

- **Hashing:** bcrypt cost 12 + a "fake hash" path so login timing on a missing
  user is statistically indistinguishable from a wrong password.
- **Generic errors:** all auth failures collapse to `invalid_credentials`. The
  client cannot tell "no such user" from "wrong password".
- **Revocable refresh tokens:** access tokens are short-lived (15 min) and
  stateless; refresh tokens are random opaque bytes, stored *hashed* (so a DB
  leak doesn't grant long-lived sessions), single-use (rotated on each
  refresh), and revocable.
- **Validation:** `zod` rejects malformed bodies before the service ever sees
  them.
- **Rate limiting:** keyed by IP for register, by IP+email for login (so one
  noisy IP can't lock out a single account by flooding it).
- **Config:** `config.jwtSecret` is loaded at startup and the process
  *refuses to boot* if it's missing or short.
- **Layering:** the router is ~30 lines and contains zero business logic; the
  service is testable without spinning up Express; the repos are interfaces
  so we can fake them in unit tests and back them with Postgres in prod.

## 1.5 CTO scalability evaluation

**Priya:** "Looks good. Now I'm going to pretend it's six months later and we
have 10× the load:

- **Stateless access tokens** mean any API node can validate a request without
  hitting the DB. ✅ Horizontally scalable.
- **Refresh tokens hit the DB** on `/refresh` and `/logout`. That's a write.
  At 10× traffic this is still cheap (refresh happens every 15 min per active
  user) but I want an index on `token_hash` and a periodic job to delete
  expired rows.
- **Rate limiting is in-process.** That's fine for one node, broken for many.
  Track tech debt: swap the limiter for Redis (`INCR` with `EXPIRE`) before we
  add a second API instance.
- **bcrypt cost 12** is ~250ms per hash on our hardware. Login throughput per
  core is ~4 rps. Fine now; if we hit auth-bound CPU, we move hashing to a
  dedicated worker pool or migrate to argon2id. Don't preempt.
- **Secret rotation:** JWTs are signed with one key. Add `kid` headers and a
  keyring before we rotate in production, otherwise rotation invalidates every
  active session.

Approved. Ship it behind a feature flag."

---

# Cycle 2 — Task CRUD

## 2.1 CTO design

**Priya:** "Tasks belong to users. v1 fields: `id`, `userId`, `title`,
`description`, `status` (`todo|doing|done`), `dueAt`, `createdAt`, `updatedAt`.
Endpoints: list (with pagination + filter by status), get, create, update,
delete. Hard requirements:

1. Authorization is enforced at the *service* layer, not the router. A user
   can only read/write their own tasks. The router is not allowed to be the
   thing standing between an attacker and someone else's data.
2. List endpoints are paginated. Always. No `SELECT *`.
3. Writes emit a domain event (`task.created`, `task.updated`, `task.deleted`)
   on the bus. Notifications subscribe in cycle 3 — the CRUD code does not
   import the notifier."

## 2.2 Junior's first version

**Devon:** "I made it really flexible — you can pass any fields and I'll just
update them."

```js
// tasks.js — Devon's v1
const router = require('express').Router();
const db = require('./db'); // raw sqlite

router.get('/tasks', (req, res) => {
  const rows = db.prepare('SELECT * FROM tasks').all();
  res.json(rows);
});

router.get('/tasks/:id', (req, res) => {
  const row = db.prepare('SELECT * FROM tasks WHERE id = ' + req.params.id).get();
  res.json(row);
});

router.post('/tasks', (req, res) => {
  const { title, description, status, dueAt, userId } = req.body;
  const r = db.prepare(
    `INSERT INTO tasks (user_id, title, description, status, due_at)
     VALUES (?, ?, ?, ?, ?)`
  ).run(userId, title, description, status, dueAt);
  res.json({ id: r.lastInsertRowid });
});

router.patch('/tasks/:id', (req, res) => {
  const fields = Object.keys(req.body).map(k => `${k} = '${req.body[k]}'`).join(', ');
  db.exec(`UPDATE tasks SET ${fields} WHERE id = ${req.params.id}`);
  res.send('ok');
});

router.delete('/tasks/:id', (req, res) => {
  db.exec(`DELETE FROM tasks WHERE id = ${req.params.id}`);
  res.send('ok');
});

module.exports = router;
```

## 2.3 Reviewer tears it apart

**Sam:** "Devon, sit down again.

1. **SQL injection on a silver platter.** `'SELECT * FROM tasks WHERE id = ' +
   req.params.id` — `id = 1; DROP TABLE tasks;--` and we're done. The PATCH is
   even worse; it lets the client control the column list, so I can do
   `?password_hash=…` and overwrite anything in any table you happen to share
   a name with.
2. **No authentication, no authorization.** `userId` comes *from the request
   body*. I can create tasks as anyone. I can read everyone's tasks. The GET
   list returns the entire table to anyone with TCP.
3. **No pagination.** When tasks > a few thousand, the list endpoint becomes
   your incident.
4. **No validation.** `status` accepts `'banana'`. `dueAt` accepts the string
   `'tomorrow'`. Garbage in, garbage forever.
5. **No event emission.** Cycle 3 is going to have to monkey-patch this.
6. **Raw DB calls in the router.** No service layer means no place to put
   authorization or audit logging without duplicating it everywhere.
7. **`SELECT *` is a contract leak.** Add a column and your API shape changes.

Reject."

## 2.4 Senior rewrites it properly

**Marcus:**

```ts
// src/tasks/task.schema.ts
import { z } from 'zod';

export const taskStatus = z.enum(['todo', 'doing', 'done']);

export const createTaskSchema = z.object({
  title: z.string().min(1).max(200),
  description: z.string().max(10_000).optional(),
  status: taskStatus.default('todo'),
  dueAt: z.string().datetime().optional(),
});

export const updateTaskSchema = createTaskSchema.partial();

export const listTasksQuery = z.object({
  status: taskStatus.optional(),
  cursor: z.string().optional(),
  limit: z.coerce.number().int().min(1).max(100).default(20),
});
```

```ts
// src/tasks/task.service.ts
import { TaskRepo } from './ports';
import { EventBus } from '../events/bus';

export class NotFoundError extends Error { code = 'not_found' as const; }
export class ForbiddenError extends Error { code = 'forbidden' as const; }

export class TaskService {
  constructor(private repo: TaskRepo, private bus: EventBus) {}

  list(userId: string, q: { status?: string; cursor?: string; limit: number }) {
    return this.repo.listForUser(userId, q);
  }

  async get(userId: string, id: string) {
    const task = await this.repo.findById(id);
    if (!task) throw new NotFoundError();
    if (task.userId !== userId) throw new ForbiddenError();
    return task;
  }

  async create(userId: string, input: CreateInput) {
    const task = await this.repo.create({ ...input, userId });
    this.bus.emit('task.created', { task });
    return task;
  }

  async update(userId: string, id: string, patch: UpdateInput) {
    const existing = await this.get(userId, id); // reuses the auth check
    const updated = await this.repo.update(id, patch);
    this.bus.emit('task.updated', { before: existing, after: updated });
    return updated;
  }

  async delete(userId: string, id: string) {
    const existing = await this.get(userId, id);
    await this.repo.delete(id);
    this.bus.emit('task.deleted', { task: existing });
  }
}
```

```ts
// src/tasks/task.router.ts
import { Router } from 'express';
import { requireUser } from '../middleware/requireUser';
import { createTaskSchema, updateTaskSchema, listTasksQuery } from './task.schema';
import { TaskService } from './task.service';

export function taskRouter(svc: TaskService) {
  const r = Router();
  r.use(requireUser);

  r.get('/', async (req, res, next) => {
    try {
      const q = listTasksQuery.parse(req.query);
      res.json(await svc.list(req.userId, q));
    } catch (e) { next(e); }
  });

  r.get('/:id', async (req, res, next) => {
    try { res.json(await svc.get(req.userId, req.params.id)); }
    catch (e) { next(e); }
  });

  r.post('/', async (req, res, next) => {
    try {
      const input = createTaskSchema.parse(req.body);
      res.status(201).json(await svc.create(req.userId, input));
    } catch (e) { next(e); }
  });

  r.patch('/:id', async (req, res, next) => {
    try {
      const patch = updateTaskSchema.parse(req.body);
      res.json(await svc.update(req.userId, req.params.id, patch));
    } catch (e) { next(e); }
  });

  r.delete('/:id', async (req, res, next) => {
    try {
      await svc.delete(req.userId, req.params.id);
      res.status(204).end();
    } catch (e) { next(e); }
  });

  return r;
}
```

```ts
// src/tasks/task.repo.sqlite.ts (excerpt — pagination by opaque cursor)
listForUser(userId: string, { status, cursor, limit }: ListQuery) {
  const where = ['user_id = @userId'];
  const params: any = { userId, limit };
  if (status) { where.push('status = @status'); params.status = status; }
  if (cursor) {
    const { createdAt, id } = decodeCursor(cursor);
    where.push('(created_at, id) < (@cAt, @cId)');
    params.cAt = createdAt; params.cId = id;
  }
  const rows = this.db.prepare(`
    SELECT id, user_id, title, description, status, due_at, created_at, updated_at
    FROM tasks
    WHERE ${where.join(' AND ')}
    ORDER BY created_at DESC, id DESC
    LIMIT @limit
  `).all(params).map(rowToTask);
  const next = rows.length === limit
    ? encodeCursor({ createdAt: rows.at(-1)!.createdAt, id: rows.at(-1)!.id })
    : null;
  return { items: rows, nextCursor: next };
}
```

What changed:

- **Parameterized queries everywhere.** No string concatenation touches SQL.
- **`requireUser` middleware** populates `req.userId` from the verified JWT;
  routers read user identity from there, never from the body.
- **Authorization in the service.** `get/update/delete` all funnel through the
  same ownership check, so it can't be forgotten on a new endpoint.
- **Explicit column lists.** No `SELECT *`; adding a column doesn't silently
  change the API.
- **Keyset pagination** (`(created_at, id) < cursor`) instead of `OFFSET`.
  Stable under inserts and O(1) regardless of page number.
- **Domain events** on the bus. The notifier in cycle 3 subscribes; the task
  module never imports it.
- **Typed errors** (`NotFoundError`, `ForbiddenError`) mapped to HTTP codes by
  a single error middleware — no scattered `res.status(...)` calls.

## 2.5 CTO scalability evaluation

**Priya:**

- **Index plan:** `tasks(user_id, created_at DESC, id DESC)` covers list +
  pagination. Add `tasks(user_id, status, created_at DESC, id DESC)` if the
  status filter becomes the dominant query.
- **Read scaling:** all list queries are user-scoped, so the natural shard key
  is `user_id`. We are not sharding now, but the query shape doesn't preclude
  it.
- **Hot users:** a power user with 1M tasks will hurt the list query. Add a
  hard cap (`limit ≤ 100`) — already there — and consider a search index
  (Postgres FTS or Meilisearch) before we add full-text search.
- **Event bus:** in-process for now, which means at-most-once delivery if a
  node dies between commit and emit. For notifications that's tolerable; if we
  ever need exactly-once, we move to the **transactional outbox** pattern —
  write events to an `outbox` table in the same transaction as the task
  change, drain to a real broker (NATS / SQS / Kafka) in a worker. Track as
  tech debt.
- **N+1 risk:** none today; revisit when we add task comments or assignees.

Approved.

---

# Cycle 3 — Notifications

## 3.1 CTO design

**Priya:** "Notifications are the place where junior engineers learn what
'eventual consistency' means. Requirements:

1. **Decoupled.** Triggered by domain events from the bus, never by direct
   calls from the task router.
2. **User preferences.** Each user can opt in/out per channel (email,
   webhook). Default: email on `task.created` for tasks with `dueAt`.
3. **Reliable-ish.** Retry with exponential backoff and a max attempt count;
   poison messages go to a dead-letter table for inspection, not lost.
4. **Idempotent.** Each notification has a deterministic key
   (`event_id:user_id:channel`) so a retry doesn't double-send.
5. **Pluggable transports.** `console` for dev, `email` and `webhook` for
   prod. Adding a new transport is one file."

## 3.2 Junior's first version

**Devon:**

```js
// notifications.js — Devon's v1
const nodemailer = require('nodemailer');
const transporter = nodemailer.createTransport({ /* ... */ });

function notifyTaskCreated(task, user) {
  transporter.sendMail({
    to: user.email,
    subject: 'New task',
    text: 'You created a task: ' + task.title,
  }, (err) => { if (err) console.log(err); });
}

// in task.router.ts:
// router.post('/tasks', async (req, res) => {
//   const task = await db.create(req.body);
//   notifyTaskCreated(task, req.user); // <-- inline
//   res.json(task);
// });
```

## 3.3 Reviewer tears it apart

**Sam:**

1. **Synchronous in the request path.** If the SMTP server is slow, every POST
   /tasks is slow. If SMTP is down, every POST /tasks 500s. The user's task
   creation should not depend on email being healthy.
2. **Errors swallowed into `console.log`.** A real outage will be invisible
   except as confused users.
3. **No retries, no DLQ.** First transient failure = lost notification.
4. **Tight coupling.** The task router imports the notifier. Adding a new
   notification trigger means editing CRUD code.
5. **No idempotency.** A retry double-sends. A user double-clicking 'create'
   triple-sends.
6. **No user preferences.** We just spam everyone.
7. **No template layer.** String concatenation is going to become an HTML
   injection vector when somebody adds rich emails.

## 3.4 Senior rewrites it properly

**Marcus:** "We split this into three pieces: a **dispatcher** that turns
domain events into pending `notifications` rows, a **worker** that drains the
queue with retries, and **transports** that actually send."

```ts
// src/notifications/dispatcher.ts
import { EventBus } from '../events/bus';
import { NotificationRepo } from './ports';
import { UserPrefsRepo } from '../users/ports';
import crypto from 'node:crypto';

export function registerNotificationDispatcher(
  bus: EventBus,
  notes: NotificationRepo,
  prefs: UserPrefsRepo,
) {
  bus.on('task.created', async ({ task, eventId }) => {
    if (!task.dueAt) return;
    const userPrefs = await prefs.get(task.userId);
    for (const channel of userPrefs.channelsFor('task.created')) {
      await notes.enqueue({
        idempotencyKey: `${eventId}:${task.userId}:${channel}`,
        userId: task.userId,
        channel,
        template: 'task.created',
        payload: { taskId: task.id, title: task.title, dueAt: task.dueAt },
      });
    }
  });

  bus.on('task.updated', async ({ before, after, eventId }) => {
    if (before.status !== 'done' && after.status === 'done') {
      const userPrefs = await prefs.get(after.userId);
      for (const channel of userPrefs.channelsFor('task.completed')) {
        await notes.enqueue({
          idempotencyKey: `${eventId}:${after.userId}:${channel}`,
          userId: after.userId,
          channel,
          template: 'task.completed',
          payload: { taskId: after.id, title: after.title },
        });
      }
    }
  });
}
```

```ts
// src/notifications/worker.ts
import { NotificationRepo } from './ports';
import { Transport } from './transports';
import { renderTemplate } from './templates';

const MAX_ATTEMPTS = 6;
const BACKOFF_MS = (n: number) => Math.min(60_000, 2 ** n * 1000); // 1s,2s,4s,…,60s

export class NotificationWorker {
  constructor(
    private repo: NotificationRepo,
    private transports: Record<string, Transport>,
  ) {}

  async tick() {
    const batch = await this.repo.claimDue(20);
    await Promise.all(batch.map(n => this.handle(n)));
  }

  private async handle(n: PendingNotification) {
    const transport = this.transports[n.channel];
    if (!transport) {
      await this.repo.deadLetter(n.id, 'unknown_channel');
      return;
    }
    try {
      const message = renderTemplate(n.template, n.payload);
      await transport.send({ to: n.recipient, message });
      await this.repo.markSent(n.id);
    } catch (err) {
      const attempts = n.attempts + 1;
      if (attempts >= MAX_ATTEMPTS) {
        await this.repo.deadLetter(n.id, String(err));
      } else {
        await this.repo.reschedule(n.id, Date.now() + BACKOFF_MS(attempts), attempts);
      }
    }
  }
}
```

```ts
// src/notifications/transports/index.ts
export interface Transport {
  send(args: { to: string; message: { subject: string; body: string } }): Promise<void>;
}

export { ConsoleTransport } from './console';
export { EmailTransport }   from './email';
export { WebhookTransport } from './webhook';
```

```ts
// src/notifications/repo.sqlite.ts (excerpt — atomic claim)
claimDue(limit: number) {
  // SELECT … FOR UPDATE SKIP LOCKED equivalent in SQLite: a tight transaction.
  return this.db.transaction(() => {
    const rows = this.db.prepare(`
      SELECT * FROM notifications
      WHERE status = 'pending' AND scheduled_at <= @now
      ORDER BY scheduled_at ASC
      LIMIT @limit
    `).all({ now: Date.now(), limit });
    if (rows.length) {
      this.db.prepare(`
        UPDATE notifications SET status = 'in_flight', claimed_at = @now
        WHERE id IN (${rows.map(() => '?').join(',')})
      `).run(...rows.map(r => r.id), { now: Date.now() });
    }
    return rows;
  })();
}
```

What changed:

- **Out of the request path.** The router commits the task and emits an event;
  notifications are enqueued and drained by a worker loop. POST /tasks no
  longer cares whether SMTP is up.
- **Idempotency key per (event, user, channel).** A retry is a no-op at the
  DB layer (`INSERT … ON CONFLICT DO NOTHING`).
- **Retry with exponential backoff and a DLQ.** Failures are visible (DLQ
  table + metric) instead of silent.
- **User preferences** gate every emission; defaults are sane but overridable.
- **Template layer.** Bodies are rendered from named templates with escaped
  payloads; no more string concatenation.
- **Atomic claim** so two worker processes don't double-deliver. In Postgres
  this becomes `SELECT … FOR UPDATE SKIP LOCKED`.

## 3.5 CTO scalability evaluation

**Priya:**

- **Bus is still in-process.** That's the weak link. If the node crashes
  between `bus.emit` and the dispatcher writing to `notifications`, the event
  is lost. **Action:** move the bus to the **transactional outbox** —
  task-write and outbox-write happen in one transaction, a separate process
  reads the outbox and either invokes the dispatcher in-process *or*
  publishes to a real broker. Cheap to add, big reliability win.
- **Worker is single-process.** Fine until ~100 notifications/sec. Beyond
  that, scale workers horizontally; the atomic claim already supports it.
- **Backoff cap of 60s** is aggressive — fine for email, too aggressive for a
  customer webhook that's been down for an hour. Per-channel backoff
  configuration is a future tweak.
- **DLQ has no UI.** Add a tiny admin endpoint to list and replay DLQ rows
  before a real outage forces us to do it under pressure.
- **Multi-tenant fairness:** today a single noisy user could fill the queue
  ahead of everyone else. If we ever ship to teams, partition the queue by
  `user_id % N` or per-tenant priority lanes.

Approved.

---

# Improvements across iterations

| Concern | Cycle 1 (Auth) | Cycle 2 (Tasks) | Cycle 3 (Notifications) |
|---|---|---|---|
| **Layering** | Router → Service → Repo introduced | Reused; service owns authz | Reused; dispatcher + worker + transports |
| **Validation** | `zod` schemas on auth bodies | Schemas on every CRUD body + query | Schemas on event payloads + template inputs |
| **Persistence** | In-memory → repo abstraction | Parameterized SQL, explicit columns, keyset pagination | Atomic claim, DLQ, outbox-ready |
| **Coupling** | Secrets via config | Domain events instead of direct calls | Bus + transport interfaces, transports are one file each |
| **Failure modes** | Generic auth errors, constant-time login | Typed errors → single error middleware | Retries, exponential backoff, DLQ, idempotency |
| **Scaling tech debt** | Redis-backed rate limit, JWT keyring | Outbox + sharding by `user_id` | Move bus to a real broker, per-tenant fairness |

The shape of each cycle is the same: the junior version optimizes for "it
runs"; the senior version optimizes for **boundaries** (so changes are local),
**failure modes** (so the system degrades, not collapses), and **observability
of the unhappy path** (so problems are visible, not silent). The CTO's job at
the end isn't to find more bugs — it's to **name the next constraint**: what
breaks at 10×, and what is the cheapest change today that keeps the door open
for that fix tomorrow.

---

# What's actually in this repo

The Senior versions of each cycle have been materialized as a runnable
backend in [`backend/`](./backend). It's intentionally small — ~600 lines —
but it implements every behavior described above:

- `POST /auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`
- `GET/POST/PATCH/DELETE /tasks` (with keyset pagination and ownership checks)
- An in-process event bus, a notification dispatcher, a worker loop with
  retries + DLQ, and a `console` transport (with `email`/`webhook` stubs)
- SQLite via better-sqlite3 so you can `npm install && npm start` without
  external services
- Vitest tests covering the auth happy/sad paths, ownership enforcement on
  tasks, and the notification retry/DLQ logic

See [`backend/README.md`](./backend/README.md) for run instructions.
