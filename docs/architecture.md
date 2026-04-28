# Architecture Documentation

## 1) Monorepo strategy

The codebase uses npm workspaces to keep frontend, backend, and shared domain contracts versioned together.

- `apps/frontend`: user-facing web app
- `apps/backend`: API and business logic
- `packages/shared`: compile-time shared types for contracts

## 2) Authentication design

### JWT

- Local user login issues signed JWT access tokens.
- Protected routes use `JwtAuthGuard`.
- JWT payload carries `sub` and `email` claims.

### OAuth (mock)

The backend provides an OAuth callback endpoint that emulates provider code exchange.

- Input: `provider + code`
- Result: user upsert + OAuth account mapping + JWT issuance

This keeps the abstraction production-compatible while avoiding external dependencies.

## 3) Billing architecture (Stripe-like, mocked)

Billing is split into layers:

1. **Billing API layer** (`BillingController`)
2. **Billing domain/service layer** (`BillingService`)
3. **Provider gateway layer** (`MockBillingGateway`)
4. **Persistence layer** (Prisma models `Subscription`, `Invoice`, `BillingEvent`)

Webhooks are signed and verified (HMAC SHA-256) before state transitions are applied.

## 4) Data model

Main entities:

- `User`
- `OAuthAccount`
- `Subscription`
- `Invoice`
- `BillingEvent`

Prisma migrations are committed in source control for deterministic schema evolution.

## 5) Testing strategy

- **Unit tests:** service-layer behavior in isolation.
- **Integration tests:** full NestJS app + HTTP flow + database + auth guard behavior.

## 6) CI/CD

- CI validates code quality and executable correctness.
- CD builds backend artifacts on main and demonstrates the promotion flow.

## 7) Security notes

- Passwords are bcrypt-hashed.
- Webhooks require signature verification.
- DTO validation with whitelisting rejects unexpected fields.
