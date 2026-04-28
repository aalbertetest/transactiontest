# SaaS Monorepo

A production-shaped SaaS starter:

- **Frontend**: React 18 + TypeScript + Vite + Tailwind CSS + React Query + Zustand
- **Backend**: NestJS 10 + Prisma + SQLite (swap to Postgres via `DATABASE_URL`)
- **Auth**: JWT access + refresh tokens, Google OAuth (Passport)
- **Billing**: Stripe-style architecture with a fully mocked provider, webhooks, checkout, plans, subscriptions, invoices
- **Tests**: Jest unit tests + supertest e2e for API, Vitest + Testing Library for web
- **CI/CD**: GitHub Actions (lint, test, e2e, build) + Docker images for API and web
- **Docs**: Architecture overview in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)

## Layout

```
.
├── apps/
│   ├── api/         # NestJS API
│   └── web/         # React + Vite app
├── packages/
│   └── shared/      # Shared TS types (Plan, PublicUser, ...)
├── .github/workflows/
│   ├── ci.yml       # Lint, test, e2e, docker build
│   └── deploy.yml   # Push images to GHCR on tag
├── docker-compose.yml
└── docs/ARCHITECTURE.md
```

## Quickstart

```bash
# 1. install
npm install

# 2. set up the database (SQLite by default)
cp apps/api/.env.example apps/api/.env
npm run prisma:deploy --workspace apps/api
npm run prisma:seed   --workspace apps/api

# 3. run web + api together
cp apps/web/.env.example apps/web/.env
npm run dev
```

- API: <http://localhost:3001/api> (Swagger at `/api/docs`)
- Web: <http://localhost:5173>

### Tests

```bash
npm test                  # unit tests for every workspace
npm run test:integration  # API e2e (boots Nest + SQLite)
```

### Docker

```bash
docker compose up --build
# Web:   http://localhost:8080
# API:   http://localhost:3001/api
```

## Switching to Postgres

In `apps/api/prisma/schema.prisma` change:

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}
```

Set `DATABASE_URL=postgres://user:pass@host:5432/db`, then re-run migrations:

```bash
npm run prisma:migrate --workspace apps/api -- --name init
```

## OAuth (Google)

1. Create a Google Cloud OAuth client (web).
2. Set `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `GOOGLE_CALLBACK_URL` in `apps/api/.env`.
3. The web app's "Continue with Google" button hits `/api/auth/google`, which after consent redirects to `/api/auth/google/callback`. The API issues tokens and bounces the browser back to the web app's `/oauth` route with the tokens as query params.

## Billing

The mock provider is wired through a `PaymentProvider` abstract class so that real Stripe can be dropped in by implementing the same interface. Endpoints:

- `GET  /api/billing/plans`
- `GET  /api/billing/subscription`
- `GET  /api/billing/invoices`
- `POST /api/billing/checkout` (returns a hosted-checkout URL)
- `POST /api/billing/subscribe` (direct subscribe — useful in tests/demos)
- `POST /api/billing/cancel`
- `POST /api/billing/webhook` (HMAC-SHA256 signed)

## License

MIT.
