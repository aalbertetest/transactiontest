# Distributed Workflow Engine (DWE)

This repository contains a production-grade, multi-service distributed workflow engine designed for reliability, scale, and operational transparency. The system is implemented across three services written in different languages to demonstrate a polyglot, production-style architecture:

- **API Service (TypeScript/Node.js)**: Public control plane that manages workflows, versions, and run requests.
- **Scheduler Service (Go)**: Leader-elected coordinator that schedules workflow steps into the queue.
- **Executor Service (Python)**: Worker fleet that executes queued tasks and reports results.

The engine is designed to be:

- **Durable**: All state is persisted to PostgreSQL and is replayable after crash.
- **Fault-tolerant**: Leaders can fail, workers can restart, and tasks are retried safely.
- **Scalable**: Sharded scheduling and execution allow linear scaling.
- **Secure**: Defense-in-depth security hardening is described and configured.

## Repository Layout

```
.
├── README.md
├── docs
│   ├── architecture.md
│   ├── api.md
│   ├── operations.md
│   ├── security.md
│   └── testing.md
├── openapi
│   └── workflow-engine.yaml
├── schema
│   ├── schema.sql
│   └── migrations
│       └── 001_init.sql
├── services
│   ├── api
│   ├── scheduler
│   └── executor
├── deploy
│   ├── kubernetes
│   └── helm
├── monitoring
│   ├── prometheus.yaml
│   └── grafana
└── tools
    ├── loadtest
    └── chaos
```

## Quick Start (Local)

1. Provision PostgreSQL:

```
docker run --rm -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=workflow postgres:16
```

2. Apply schema:

```
psql postgres://postgres:postgres@localhost:5432/workflow -f schema/schema.sql
```

3. Start services (each in its own terminal):

```
cd services/api && npm install && npm run dev
cd services/scheduler && go run ./cmd/scheduler
cd services/executor && pip install -r requirements.txt && python -m executor.main
```

4. Create a workflow and trigger a run using the API:

```
curl -X POST http://localhost:8080/v1/workflows \
  -H "Content-Type: application/json" \
  -d @examples/workflow-basic.json

curl -X POST http://localhost:8080/v1/workflow-runs \
  -H "Content-Type: application/json" \
  -d '{"workflow_id":"<id>","input":{"name":"world"}}'
```

## Key Concepts

- **Workflow**: A named, versioned DAG of steps.
- **Run**: A single execution of a workflow version with input parameters.
- **Task**: A scheduled unit of work for a specific step and run.

## Documentation

Detailed design and operational guidance is in:

- `docs/architecture.md`
- `docs/security.md`
- `docs/operations.md`
- `docs/testing.md`
- `openapi/workflow-engine.yaml`

## Licensing

This repository is intended for educational and reference purposes. Adapt it for production by reviewing your security, compliance, and reliability requirements.
