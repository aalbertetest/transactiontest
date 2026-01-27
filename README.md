Distributed Platform - Cloud Native Reference Implementation
============================================================

This repository contains a complete, production-grade reference platform that
combines the capabilities of an API gateway, authentication system, user and
payment services, workflow engine, distributed queue, streaming platform,
cache layer, database layer, WebSocket realtime service, scheduler, and a
worker fleet. The platform is intentionally multi-language: each service has
full implementations in Python, Go, and TypeScript (Node.js). The platform is
designed to be cloud-native and operationally robust with reliability,
security, and observability baked in.

This is a reference implementation and blueprint. The code is organized to
support learning, extension, and deployment in real environments. It uses only
standard libraries for portability and auditability. Where production systems
would normally pull external dependencies (for example, JWT or protobuf
libraries), this repository includes self-contained implementations that are
fully commented and easy to audit.

Repository Layout
-----------------

  - docs/
      architecture.md        System overview, diagrams, flows, failure modes
      services.md            Service definitions, contracts, models
      data.md                SQL/NoSQL schemas, migrations, indexing
      apis.md                REST, gRPC, OpenAPI, examples
      infra.md               Docker, K8s, Helm, Terraform, CI/CD, secrets
      reliability.md         Idempotency, retries, backpressure, sharding
      security.md            Threat model, TLS, rotation, audit logging
      testing.md             Unit/integration/load/chaos tests
      developer-guide.md     Local development, code structure
      api-guide.md           SDK usage and client patterns
      deployment-guide.md    Deployment steps and environment setup
      runbooks.md            Operational runbooks and on-call procedures
  - src/
      python/platform.py     Full Python implementations for all services
      go/main.go             Full Go implementations for all services
      node/index.ts          Full TypeScript implementations for all services
  - apis/
      platform.proto         gRPC definitions for all services
      openapi.yaml           OpenAPI specification for REST API
  - db/
      migrations/
          001_init.sql       Base schema
          002_indexes.sql    Indexes and partitioning helpers
  - infra/
      k8s/platform.yaml      Kubernetes manifests
      helm/                  Helm chart example
      terraform/main.tf      Terraform example
  - .github/workflows/ci.yml CI pipeline (build/test/lint)

Quick Start (Local)
-------------------

1) Python (single-process multi-service runtime):

  - python3 src/python/platform.py

2) Go (single-binary multi-service runtime):

  - go run src/go/main.go

3) TypeScript (Node.js):

  - node --loader ts-node/esm src/node/index.ts

Each runtime starts all services on distinct ports. The API Gateway then routes
traffic to the correct backend service. See docs/architecture.md and
docs/apis.md for port mappings and endpoint contracts.

Design Notes
------------

* All services are standalone and self-hosted. The platform does not assume a
  specific cloud provider.
* Observability is built in: every service exposes structured logs and
  Prometheus-compatible metrics.
* Core reliability patterns are implemented in code: retries with jitter,
  circuit breakers, idempotency keys, rate limits, and backpressure controls.
* Security controls are integrated into middleware: mTLS, JWT verification,
  role-based authorization, and audit logging.

How to Navigate
---------------

Start with docs/architecture.md to understand the system, then read
docs/services.md for detailed service behavior and data models. Use
docs/apis.md for exact REST and gRPC definitions and docs/infra.md for
deployment and automation. The source implementations are designed to be read
side-by-side across languages for clarity and parity.
