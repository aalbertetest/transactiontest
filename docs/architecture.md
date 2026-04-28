# Architecture

## Monorepo layout

The repository uses npm workspaces so shared contracts can be developed and versioned with both deployable apps.

```text
apps/
  api/      NestJS service boundary for auth, billing, migrations, and health
  web/      React/Vite/Tailwind user interface
packages/
  shared/   Cross-app TypeScript contracts and SaaS plan metadata
docs/       Architecture and operations documentation
```

## Frontend

The frontend is a Vite React application. Tailwind CSS is integrated through the official Vite plugin, keeping styling local to components and avoiding a custom CSS build pipeline. API access is isolated in `src/api.ts` so generated clients or token injection can be added without changing view components.

## Backend

NestJS modules divide the backend into explicit domains:

- `AuthModule` owns credential login, OAuth callback exchange, JWT issuing, and JWT guards.
- `BillingModule` owns plan reads, checkout sessions, customer portal sessions, and webhook verification.
- `HealthModule` gives infrastructure a stable liveness endpoint.

Repositories are intentionally thin in this starter. The demo user repository is in-memory for tests and local startup; production persistence is represented by SQL migrations and can be wired behind the same repository interface.

## Authentication

JWT authentication uses Passport's bearer strategy and a configurable `JWT_SECRET`. Password verification uses PBKDF2 from Node's crypto library for the seeded demo account. OAuth is modeled as a callback endpoint that maps provider authorization output to a linked user; in production, the callback should exchange the code with Google/GitHub and verify provider claims before calling `oauthLogin`.

## Billing

Billing follows a Stripe-like port/adapter architecture:

- `BillingProvider` defines checkout, portal, and webhook operations.
- `MockStripeBillingProvider` returns realistic hosted URLs and verifies a webhook secret.
- `BillingService` validates shared plan IDs before calling the provider.

This keeps route handlers stable when replacing the mock with the official Stripe SDK.

## Database migrations

Migrations are plain SQL files with a small runner that records applied files in `schema_migrations`. The schema includes organizations, users, OAuth identities, and subscriptions with provider identifiers. Plain SQL keeps production DDL reviewable and database-native.

## Testing strategy

- Unit tests cover shared utilities and backend domain services.
- Frontend tests render the landing page with mocked network calls.
- API integration tests boot a Nest application, exercise health, login/JWT, and billing checkout routes.

## Deployment

CI validates every PR. CD currently packages artifacts from `main`; real environments can replace artifact upload steps with container builds, static hosting deployment, and API release commands.
