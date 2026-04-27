# tasks-backend

Runnable companion to [`../SIMULATION.md`](../SIMULATION.md). This is the
"Senior-version" code at the end of each cycle: auth, task CRUD, and
notifications, wired together with an in-process event bus and a notification
worker.

## Running

```bash
cd backend
npm install
JWT_SECRET=$(node -e "console.log(require('crypto').randomBytes(32).toString('hex'))") \
  npm start
```

The API listens on `http://localhost:3000`. SQLite data lives in
`./data/app.db` (created on first boot).

## Tests

```bash
npm test
```

Vitest covers:

- Auth happy/sad paths and constant-time login on a missing user
- Task ownership enforcement and keyset pagination
- Notification retry-with-backoff and dead-letter on max attempts
- Idempotency: the same event can't be enqueued twice

## Endpoints

| Method | Path | Auth | Notes |
|---|---|---|---|
| POST | `/auth/register` | – | Body: `{ email, password }` (password ≥ 12 chars). Returns access + refresh tokens. |
| POST | `/auth/login` | – | Same body. Generic error on failure (no enumeration). |
| POST | `/auth/refresh` | – | Body: `{ refreshToken }`. Rotates the refresh token. |
| POST | `/auth/logout` | – | Body: `{ refreshToken }`. |
| GET | `/tasks` | Bearer | Query: `status`, `cursor`, `limit` (≤100). Keyset pagination. |
| POST | `/tasks` | Bearer | Body: `{ title, description?, status?, dueAt? }`. |
| GET | `/tasks/:id` | Bearer | 404 if not found, 403 if not yours. |
| PATCH | `/tasks/:id` | Bearer | Partial update. |
| DELETE | `/tasks/:id` | Bearer | 204 on success. |

## Architecture

```
HTTP layer (Express routers)
        │
        ▼
Service layer (AuthService, TaskService) — owns business + authz rules
        │
        ▼
Repo layer (UserRepo, RefreshTokenRepo, TaskRepo, NotificationRepo)
        │
        ▼
SQLite (better-sqlite3)

Tasks emit domain events on an in-process EventBus.
NotificationDispatcher subscribes and enqueues rows in `notifications`.
NotificationWorker drains the queue with retry + backoff + DLQ.
```

See `../SIMULATION.md` for the full design dialogue and the rejected junior
versions that came before this code.
