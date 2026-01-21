# Security Hardening

This document describes security practices and configuration for the Workflow
Engine.

## 1. Authentication and Authorization

- Use OIDC for user authentication.
- Use JWT tokens with short lifetimes for API access.
- Use Kubernetes service accounts and RBAC for service-to-service access.

## 2. Network Security

- Enforce mTLS between services with a service mesh or mutual TLS gateway.
- Restrict ingress with Kubernetes NetworkPolicies.
- Expose API only through a secure ingress controller.

## 3. Data Protection

- Encrypt PostgreSQL storage at rest using volume encryption.
- Use TLS for all DB connections.
- Store secrets in Kubernetes Secrets or a dedicated secret manager.

## 4. Least Privilege

- Run containers as non-root.
- Use read-only root filesystems.
- Drop all Linux capabilities except those required.

## 5. Auditing and Logging

- Enable audit logs for API requests and administrative actions.
- Log all workflow changes and execution transitions.
- Ship logs to centralized storage and enforce retention policies.

## 6. Supply Chain Security

- Sign container images.
- Scan images for vulnerabilities on every build.
- Use a trusted base image with pinned versions.

## 7. Denial-of-Service Protections

- Rate limit API requests.
- Enforce workflow size and step count limits.
- Validate input sizes for payloads and headers.

## 8. Secrets Management

- Use a KMS to manage encryption keys.
- Rotate secrets regularly.
- Avoid embedding secrets in workflow definitions or logs.

## 9. Compliance

- Maintain data retention policies.
- Provide access logs and audit trails.
- Implement least privilege and data minimization.
