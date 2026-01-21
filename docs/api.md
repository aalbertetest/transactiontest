# API Documentation

This document describes the REST API surface of the Workflow Engine. The
canonical OpenAPI spec is at `openapi/workflow-engine.yaml`.

## 1. Base URL

```
http://<host>:8080/v1
```

## 2. Key Endpoints

### 2.1 Create Workflow

```
POST /v1/workflows
```

Request:

```json
{
  "name": "daily-report",
  "description": "Generate and publish daily report",
  "spec": {
    "steps": [
      {"id": "fetch", "type": "http_request", "params": {"url": "https://example.com"}},
      {"id": "sleep", "type": "sleep", "params": {"seconds": 2}, "depends_on": ["fetch"]}
    ]
  }
}
```

### 2.2 Trigger Workflow Run

```
POST /v1/workflow-runs
```

Request:

```json
{
  "workflow_id": "uuid",
  "input": {"name": "world"}
}
```

### 2.3 Fetch Run Status

```
GET /v1/workflow-runs/{id}
```

Response:

```json
{
  "id": "uuid",
  "status": "running",
  "started_at": "2026-01-01T12:00:00Z",
  "finished_at": null,
  "output": null
}
```

## 3. Error Model

All errors follow a standard structure:

```json
{
  "error": {
    "code": "invalid_request",
    "message": "workflow_id is required",
    "details": {"field": "workflow_id"}
  }
}
```

## 4. Authentication

The API supports:

- mTLS between client and gateway
- JWT bearer tokens for user-level authorization
- Kubernetes service accounts for internal calls

See `docs/security.md` for details.
