APIs
====

This document lists the REST endpoints, gRPC service definitions, OpenAPI
specification reference, and example requests/responses. The full gRPC and
OpenAPI specs are in apis/platform.proto and apis/openapi.yaml.

REST Endpoints (Summary)
------------------------

API Gateway
* GET  /healthz
* GET  /readyz
* GET  /metrics

Auth Service
* POST /auth/oauth/authorize
* POST /auth/oauth/token
* POST /auth/token/refresh
* POST /auth/mfa/enroll
* POST /auth/mfa/verify
* GET  /auth/keys

User Service
* POST /users/register
* GET  /users/{id}
* PATCH /users/{id}
* POST /users/{id}/orgs
* POST /orgs/{id}/members

Payment Service
* POST /payments/intents
* POST /payments/intents/{id}/capture
* POST /payments/intents/{id}/refund
* GET  /payments/intents/{id}

Workflow Engine
* POST /workflows
* POST /workflows/{id}/start
* GET  /workflows/runs/{run_id}
* POST /workflows/runs/{run_id}/signal

Distributed Queue
* POST /queues/{name}/enqueue
* POST /queues/{name}/dequeue
* POST /queues/{name}/ack

Streaming Platform
* POST /streams/{topic}/publish
* GET  /streams/{topic}/consume
* POST /streams/{topic}/commit

Cache Layer
* GET  /cache/{key}
* PUT  /cache/{key}
* DELETE /cache/{key}

Database Layer
* POST /db/query
* POST /db/execute
* POST /db/document/get
* POST /db/document/put

WebSocket Realtime Service
* GET /ws (Upgrade to WebSocket)
* POST /ws/publish (server-side event publish)

Scheduler
* POST /schedules
* POST /schedules/{id}/enable
* POST /schedules/{id}/disable

Worker Fleet
* POST /workers/register
* POST /workers/heartbeat
* POST /workers/task/result

gRPC Services
-------------

See apis/platform.proto for full service definitions. Example:

service UserService {
  rpc RegisterUser (RegisterUserRequest) returns (RegisterUserResponse);
  rpc GetUser (GetUserRequest) returns (GetUserResponse);
  rpc UpdateUser (UpdateUserRequest) returns (UpdateUserResponse);
}

OpenAPI Specification
---------------------

The OpenAPI 3.0 spec is provided in apis/openapi.yaml. It includes full schema
definitions, security schemes, and examples for every endpoint.

Example Requests and Responses
------------------------------

1) Register User

Request:
POST /users/register
{
  "email": "alice@example.com",
  "display_name": "Alice"
}

Response:
201 Created
{
  "id": "usr_123",
  "email": "alice@example.com",
  "display_name": "Alice",
  "status": "active"
}

2) Create Payment Intent

Request:
POST /payments/intents
Headers:
  Idempotency-Key: req_abc
Body:
{
  "user_id": "usr_123",
  "amount": 4999,
  "currency": "USD"
}

Response:
202 Accepted
{
  "id": "pi_001",
  "status": "pending"
}

3) Start Workflow

Request:
POST /workflows/{id}/start
{
  "input": { "order_id": "ord_1" }
}

Response:
202 Accepted
{
  "run_id": "wr_001",
  "status": "running"
}

4) Enqueue Task

Request:
POST /queues/payments/enqueue
{
  "payload": { "intent_id": "pi_001" }
}

Response:
201 Created
{
  "message_id": "msg_001",
  "visible_at": "2026-01-27T00:00:00Z"
}
