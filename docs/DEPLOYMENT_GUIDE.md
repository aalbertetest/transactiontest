## Deployment Guide

This guide describes how DSP is deployed to Kubernetes and how environments are managed.

---

## Deployment model

DSP is deployed as a set of Kubernetes Deployments/StatefulSets:

- stateless services: gateway, auth, user, payments, workflow, scheduler, websocket
- workers: horizontally scaled deployments, potentially with node pools by workload type
- stateful dependencies (examples):
  - Postgres (managed service recommended)
  - Redis (managed service recommended)
  - Stream/Queue (managed or in-cluster, depending on environment)

---

## Environments

- `dev`: single cluster, minimal HA, faster iteration, relaxed retention
- `staging`: production-like, canary testing, chaos testing enabled
- `prod`: multi-AZ, strict policies, audited changes

---

## Secrets

Secrets MUST be managed by an external secret manager in staging/prod.

Supported patterns:

- External Secrets Operator (ESO) to sync secrets into Kubernetes Secrets
- Sealed Secrets (acceptable for dev only)

---

## Kubernetes deployment flow

1. Apply namespaces and CRDs (metrics, secrets operator, ingress).
2. Deploy shared infra (if in-cluster):
   - cache, stream, queue, database (or configure external endpoints)
3. Deploy platform services:
   - auth + user + gateway first (to enable authn)
   - payments, workflow, scheduler, websocket, workers
4. Configure ingress and DNS.
5. Run smoke tests.

---

## Helm charts

This repo will provide Helm charts in `infra/helm/`:

- `dsp-platform` umbrella chart
- per-service subcharts (gateway/auth/user/...)

---

## Terraform examples

Terraform examples live in `infra/terraform/` and illustrate:

- managed Postgres + read replicas
- managed Redis
- Kubernetes cluster baseline (VPC, node pools, IAM)
- secrets manager integration

