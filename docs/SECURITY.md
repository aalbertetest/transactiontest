## Security

This document defines the security model, threat model, and concrete implementation requirements for DSP.

---

## Threat model

### Assets

- User identities and authentication factors
- API keys and OAuth2 client secrets
- Payment and ledger data
- Workflow definitions and execution history (may contain sensitive payloads)
- Audit logs (integrity-critical)
- Encryption keys (root of trust)

### Adversaries

- External attackers (internet-originated)
- Malicious tenants (multi-tenant abuse)
- Insider threats (operator misuse)
- Supply-chain attacks (dependency compromise)

### Primary threats and mitigations

- **Credential stuffing**: rate limiting, MFA, suspicious login detection, password hashing (argon2/bcrypt)
- **Token theft**: short-lived access tokens, refresh token rotation, TLS everywhere, secure storage
- **Replay attacks**: nonce/jti checks for sensitive flows, idempotency keys, webhook signatures
- **Privilege escalation**: RBAC + policy evaluation, least privilege, default deny
- **Data exfiltration**: tenant isolation, encryption at rest, restricted debug endpoints, audit logging
- **Service-to-service spoofing**: mTLS, SPIFFE/SPIRE or equivalent identity, workload identity
- **Webhook forgery**: HMAC signatures, timestamp tolerance, replay protection

---

## TLS and mTLS setup

### External TLS

- Gateway terminates TLS using a managed ingress (e.g., NGINX/Envoy).
- Minimum TLS version: TLS 1.2 (prefer TLS 1.3).
- Strong cipher suites only; disable legacy renegotiation.

### Internal mTLS

- All service-to-service traffic uses mTLS.
- Each workload obtains a short-lived certificate (via SPIFFE/SPIRE or cert-manager).
- Authorization includes both:
  - network identity (mTLS cert SPIFFE ID)
  - application identity (JWT/service token for fine-grained scopes)

---

## Authentication and authorization

### OAuth2/OIDC

Auth Service acts as:

- OAuth2 Authorization Server
- OIDC Provider (discovery + JWKS)

Token types:

- Access token: JWT, short TTL (5–15 minutes)
- Refresh token: opaque or JWT, rotation enabled, longer TTL (days), stored hashed

### MFA

Supported factors:

- TOTP (RFC 6238)
- WebAuthn (FIDO2) (optional, but architecture supports it)
- Recovery codes (one-time use)

MFA requirements:

- Step-up authentication for high-risk operations (API key creation, payouts, key rotation)
- Rate limits and lockouts for TOTP verification attempts

### Authorization

Enforcement layers:

- Gateway: coarse checks (token validity, tenant scope)
- Services: fine checks (RBAC + policy)

Policy model:

- `subject` (user/service), `action`, `resource`, `tenant`
- Default deny; explicit allow rules

---

## Secrets management

### Requirements

- No secrets in git.
- Secrets are injected at runtime via:
  - Kubernetes Secrets (encrypted at rest)
  - External secret managers (Vault/ASM/GCP Secret Manager) via external-secrets operator

### Key material

- JWT signing keys stored in KMS-backed secret store.
- Payment webhook secrets stored per-tenant/per-integration.

---

## Key rotation

### JWT signing keys

- Keys are versioned with `kid`.
- Rotation:
  - publish new key, begin signing new tokens with it
  - keep previous keys available for verification until max token TTL passes
  - retire old keys

### Database and at-rest encryption keys

- Envelope encryption:
  - DEK per record/bucket (rotatable)
  - KEK in KMS
- Rotate KEKs periodically; re-wrap DEKs without rewriting all ciphertext.

---

## Encryption at rest

- SQL storage uses:
  - disk encryption (cloud provider) AND
  - application-level encryption for selected fields (PII/payment tokens)
- KV/Log storage uses:
  - encrypted volumes and/or built-in encryption

PII fields that MUST be encrypted at application layer:

- email (optionally tokenized depending on query needs)
- phone number
- payment method tokens

---

## Audit logging

Audit logs MUST be:

- append-only
- tamper-evident (hash-chained batches)
- tenant-scoped
- retained per policy

Events captured:

- auth events (login, mfa, token issuance, failures)
- policy/admin changes
- payment and ledger state changes
- key creation/rotation/revocation

