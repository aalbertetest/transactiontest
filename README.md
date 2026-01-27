## Distributed Software Platform (DSP)

This repository contains a **cloud-native distributed software platform** designed to resemble a blend of **AWS primitives**, **Temporal-style workflows**, **Kafka-style streaming**, and **Stripe-style payments**.

It is intentionally implemented as a **polyglot reference platform**:

- **Python** service implementations + SDKs
- **Go** service implementations + SDKs
- **TypeScript (Node.js)** service implementations + SDKs

The platform is designed to run on Kubernetes with clear separation between:

- **Control plane**: authn/authz, orchestration, scheduling, workflow control, management APIs
- **Data plane**: streaming/queue hot paths, websocket fanout, worker execution

### Repository layout

- `docs/`: architecture, data, security, reliability, runbooks
- `apis/`: OpenAPI specs, gRPC protobufs, examples
- `infra/`: Dockerfiles, Kubernetes manifests, Helm charts, Terraform, CI/CD pipelines
- `services/`: service implementations (by service and language)
- `libs/`: shared libraries (by language) for config/logging/metrics/retry/tracing
- `scripts/`: tooling for local dev and CI

### Services (logical)

- API Gateway
- Authentication Service (OAuth2, JWT, MFA)
- User Service
- Payment Processing Service
- Workflow Engine
- Distributed Queue
- Streaming Platform
- Cache Layer
- Database Layer
- WebSocket Realtime Service
- Scheduler
- Worker Fleet

### Where to start

- Read `docs/ARCHITECTURE.md` for the full system overview, diagrams, flows, and failure recovery paths.
- Read `docs/DEPLOYMENT_GUIDE.md` for Kubernetes deployment flows and environment bootstrapping.
- Read `docs/API_GUIDE.md` for REST + gRPC APIs, OpenAPI specs, and example requests/responses.
- Read `docs/DEVELOPER_GUIDE.md` for local development and contributing.

