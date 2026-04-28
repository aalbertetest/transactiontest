# Architecture

## High level

```
┌────────────┐  HTTPS  ┌─────────────┐  Prisma  ┌─────────────┐
│  React Web │ ──────▶ │ NestJS API  │ ───────▶ │  Database   │
│  (Vite)    │ ◀────── │             │ ◀─────── │  (SQLite/PG)│
└────────────┘         └─────────────┘          └─────────────┘
        ▲                     │
        │  redirect           │ webhook (HMAC-SHA256)
        ▼                     ▼
   Google OAuth         PaymentProvider (Mock Stripe)
```

## Monorepo layout

- `apps/api` — NestJS server. Modules: `AuthModule`, `UsersModule`, `BillingModule`, `PrismaModule`. A `HealthController` exposes `/api/health`.
- `apps/web` — React + Vite. Routing via `react-router-dom`, server cache via TanStack Query, auth state in a persisted Zustand store.
- `packages/shared` — Pure TypeScript types and the canonical `PLANS` list. Shared by API (used by the seed script) and Web (used by typed components).

The workspaces are wired with npm workspaces and a path alias (`@saas/shared`) so each app sees the shared package as source for type-checking with no build step required.

## Authentication

- **Local** — bcrypt-hashed passwords, validated by `LocalStrategy`. On register/login the API issues a short-lived access JWT (15 min) and a longer-lived refresh JWT (30 days). The hashed refresh token is persisted in `RefreshToken` so we can revoke individual sessions and detect reuse.
- **OAuth (Google)** — Passport's `passport-google-oauth20`. The callback route resolves or creates the user, links by `(provider, providerId)`, then issues tokens and 302-redirects back to the web app's `/oauth` page with `access`/`refresh` in the query string.
- **Refresh** — `POST /auth/refresh` looks up the refresh token by SHA-256 hash, verifies the JWT, marks it revoked, and issues a fresh pair (rotation).
- **Authorization** — `JwtAuthGuard` (default) and a `RolesGuard` for role-gated endpoints. `JwtStrategy` extracts the bearer token, verifies signature, and attaches `{ id, email, role }` to `req.user`.

## Billing (Stripe-style mock)

`apps/api/src/billing/payment-provider.ts` defines the abstract `PaymentProvider` (customers, checkout sessions, subscriptions, cancellations, webhook verification). `MockStripeProvider` implements it in-process: deterministic IDs, HMAC-signed webhook bodies, and immediate "active" subscriptions to keep development frictionless.

To switch to real Stripe, add a `StripeProvider` that implements the same interface and wire it in `BillingModule` providers — no other code changes.

The data model uses `Plan`, `Subscription`, and `Invoice` rows owned by a `User`. Webhooks are routed through `BillingService.handleWebhook`, which dispatches by event type (`checkout.session.completed`, `invoice.paid`, `customer.subscription.updated`, `customer.subscription.deleted`).

## Database & migrations

Prisma manages the schema. The provider is SQLite by default for zero-config local development and CI. The migration directory in `apps/api/prisma/migrations` contains a hand-checked initial migration; the migration lock pins the provider to keep CI deterministic.

The seed script (`prisma/seed.ts`) imports `PLANS` from `@saas/shared` and upserts them, ensuring the same plan catalog ships everywhere.

## Frontend architecture

- **Routing** — Public routes (landing, login, register, OAuth callback) and a `ProtectedRoute` wrapper that redirects to `/login` when no token is present.
- **State** — `useAuth` (Zustand + `persist`) holds tokens and the public user. The Axios client reads tokens from this store and silently refreshes on 401, retrying the original request once.
- **Server cache** — TanStack Query owns plan/subscription/invoice fetching, providing automatic invalidation after mutations.
- **Styling** — Tailwind with a small `@layer components` set (`btn-primary`, `card`, `input`).

## Testing strategy

- **Unit tests** — Pure logic only (no IO). `AuthService` and `BillingService` are tested with hand-rolled fakes; the mock payment provider is tested directly. On the web side, the auth store and a representative page are tested with Vitest + Testing Library.
- **Integration tests** — `apps/api/test/auth.e2e-spec.ts` boots the full Nest application against a fresh SQLite file (created in a temp directory), runs migrations + seed, then hits the HTTP surface with `supertest`. This proves end-to-end that auth + billing actually work together.

## CI/CD

`.github/workflows/ci.yml` runs three jobs on every push/PR:

1. `api` — installs, generates the Prisma client, lints, runs unit tests, then the e2e suite.
2. `web` — lints, runs Vitest, builds the production bundle.
3. `docker` — on `main`, builds both Docker images via Buildx (fast PR feedback by skipping registry pushes).

`deploy.yml` triggers on version tags (`v*.*.*`) and pushes the API + Web images to GHCR.

## Security defaults

- `helmet` middleware on the API.
- Strict CORS (configurable origin list).
- `class-validator` global pipe with `whitelist` and `forbidNonWhitelisted`.
- Rate-limiting via `@nestjs/throttler` (120 req/min by default).
- Refresh tokens stored hashed (SHA-256) and rotated on every refresh.
- Webhook payloads verified with HMAC-SHA256 against `BILLING_WEBHOOK_SECRET`.
