# Production-Ready SaaS Monorepo

This repository is a complete full-stack SaaS starter organized as a monorepo.

## Stack

- **Frontend:** React + TypeScript + TailwindCSS + Vite
- **Backend:** Node.js + NestJS + Prisma
- **Auth:** JWT + mocked OAuth callback flow
- **Billing:** Stripe-like architecture with a mock billing gateway + signed webhooks
- **Database:** SQLite + Prisma migrations
- **Testing:** Unit tests + integration tests
- **CI/CD:** GitHub Actions pipelines for CI and deployment simulation

## Monorepo layout

```
apps/
  backend/   NestJS API
  frontend/  React app
packages/
  shared/    Shared TypeScript types
docs/
  architecture.md
.github/workflows/
  ci.yml
  cd.yml
```

## Quick start

1. Install dependencies:

   ```bash
   npm install
   ```

2. Copy environment defaults:

   ```bash
   cp .env.example .env
   ```

3. Generate Prisma client and run migrations:

   ```bash
   npm run db:generate -w @saas/backend
   npm run db:migrate -w @saas/backend
   npm run db:seed -w @saas/backend
   ```

4. Start backend and frontend in separate terminals:

   ```bash
   npm run dev -w @saas/backend
   npm run dev -w @saas/frontend
   ```

   Frontend runs at `http://localhost:5173` and backend at `http://localhost:3000`.

## API highlights

- `POST /auth/register`
- `POST /auth/login`
- `POST /auth/oauth/callback` (mock provider exchange)
- `GET /billing/plans`
- `POST /billing/subscriptions` (JWT-protected)
- `GET /billing/invoices` (JWT-protected)
- `POST /billing/webhooks/mock` (signed webhook)

## Tests

- Run all tests:

  ```bash
  npm test
  ```

- Backend integration tests validate auth + billing flows end-to-end with a migrated SQLite database.

## CI/CD

- **CI (`ci.yml`)** runs lint, unit/integration tests, and builds all workspaces.
- **CD (`cd.yml`)** runs on main branch pushes and produces a deployable backend artifact (mock deployment step included).

## Production hardening checklist

For production rollout, replace or extend:

- SQLite with managed Postgres/MySQL.
- Mock OAuth callback exchange with real OAuth provider SDKs.
- Mock billing gateway with Stripe/Braintree adapters.
- In-memory secrets with a secrets manager.
- Add observability (OpenTelemetry, metrics, alerting).
