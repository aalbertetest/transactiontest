# Production SaaS Monorepo

A full-stack SaaS starter with React, TypeScript, Tailwind CSS, NestJS, JWT/OAuth-style authentication, mocked Stripe-like billing, PostgreSQL migrations, tests, and GitHub Actions CI/CD.

## Apps and packages

- `apps/web` - Vite React frontend with Tailwind CSS and typed API calls.
- `apps/api` - NestJS backend with auth, billing, health checks, and migration tooling.
- `packages/shared` - Shared TypeScript contracts and plan utilities used by both apps.
- `docs` - Architecture and operational notes.

## Quick start

```bash
npm install
cp .env.example .env
npm run dev
```

The web app runs on `http://localhost:5173` and proxies `/api` to the NestJS API on `http://localhost:3000`.

Demo login:

- Email: `founder@example.com`
- Password: `password`

## Verification

```bash
npm run typecheck
npm run lint
npm test
npm run test:integration
npm run build
```

## Database migrations

SQL migrations live in `apps/api/migrations`. Build the API first, set `DATABASE_URL`, then run:

```bash
npm run build --workspace @saas/api
npm run migration:status --workspace @saas/api
npm run migration:up --workspace @saas/api
```

## Billing

The billing module exposes a Stripe-like provider interface and a mock implementation. Controllers and services depend on the provider abstraction so a real Stripe adapter can replace `MockStripeBillingProvider` without changing route handlers.

## CI/CD

- `.github/workflows/ci.yml` installs, typechecks, lints, tests, integration-tests, and builds on PRs and pushes to `main`.
- `.github/workflows/cd.yml` builds deployable artifacts from `main` and uploads web/API artifacts for deployment systems.
