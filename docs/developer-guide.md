Developer Guide
===============

Local Setup
-----------

Prerequisites:
* Python 3.10+
* Go 1.21+
* Node 20+

Run the platform:

Python:
  python3 src/python/platform.py

Go:
  go run src/go/main.go

TypeScript (Node.js):
  node src/node/index.ts

Service Isolation
-----------------

To run only a single service, use SERVICE_ONLY:

  SERVICE_ONLY=gateway python3 src/python/platform.py
  SERVICE_ONLY=auth go run src/go/main.go
  SERVICE_ONLY=worker node src/node/index.ts

SERVICE_ONLY supports comma-separated values to run multiple services in a
single process.

Environment Variables
---------------------

* JWT_SECRET: shared secret for JWT signing.
* RATE_LIMIT_PER_MIN: per-IP rate limit.
* WORKER_CONCURRENCY: worker pool size.
* SERVICE_ONLY: comma-separated list of services to run.

Logging and Metrics
-------------------

* Structured JSON logs by default.
* Metrics endpoint exposed at /metrics.
* Correlation-Id header is propagated across services.

Debugging Tips
--------------

* Use curl to hit API endpoints.
* Use /healthz and /readyz for health checks.
* Use /metrics to inspect counters and latency.
