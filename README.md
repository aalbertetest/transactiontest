# Collaborative Code Editor

A production-oriented full-stack reference implementation of a real-time collaborative code editor: React + TypeScript, Express, PostgreSQL + Prisma, JWT auth with refresh-token rotation, Monaco syntax highlighting, Yjs CRDT sync over WebSockets, and cursor presence.

## Architecture

- **Web app (`apps/web`)**: React + TypeScript + Vite. Zustand stores durable session state and lightweight project selection state. Monaco provides the VSCode-like editor surface.
- **API (`apps/api`)**: Express HTTP API for auth, project/document metadata, and document snapshots.
- **Realtime server**: WebSocket upgrade endpoint at `/ws/collaboration`. Each document maps to an in-memory Yjs room; updates are persisted back to Postgres after a debounce.
- **Database**: Postgres stores users, refresh-token hashes, project memberships, document metadata, CRDT state blobs, plain-text read models, and snapshots.

## Local setup

1. Install dependencies:
   ```bash
   npm install
   ```
2. Start Postgres:
   ```bash
   docker compose up -d postgres
   ```
3. Configure the API:
   ```bash
   cp apps/api/.env.example apps/api/.env
   ```
4. Generate Prisma client and run migrations:
   ```bash
   npm run prisma:generate
   npm run prisma:migrate
   ```
5. Start both apps:
   ```bash
   npm run dev
   ```
6. Open `http://localhost:5173`, register an account, create/open a project, and open the same document in another browser session to test collaboration.

## Useful commands

```bash
npm run typecheck
npm run test
npm run build
```

## Environment

API defaults are development-friendly. Production deployments must set strong values for:

- `DATABASE_URL`
- `JWT_ACCESS_SECRET`
- `JWT_REFRESH_SECRET`
- `CORS_ORIGIN`

Prisma ORM 7 uses `apps/api/prisma.config.ts` for the CLI database URL and the
Postgres driver adapter at runtime.

