# Realtime Chat Platform

This repository contains a fully working, minimal Slack-like chat platform with
WebSockets, authentication, presence, durable message queues, retries, and
Kubernetes deployment manifests.

## Features

- WebSocket chat with per-channel messaging and acks
- JWT authentication and password hashing
- Presence tracking with periodic broadcasts
- Durable outbox queue with retry and offline handling
- SQLite for local persistence, PostgreSQL-compatible schema
- Horizontal scaling via per-instance routing and Kubernetes manifests
- Tests for auth, chat delivery, and retry logic

## Architecture (high level)

```
Client --HTTP--> FastAPI (auth/channels)
Client --WS----> FastAPI (websocket + presence)
                          |
                          +--> SQL DB (users, channels, messages, presence)
                          +--> Outbox queue (durable delivery + retries)
```

- Each API instance has a unique `INSTANCE_ID`.
- Presence updates assign pending outbox jobs to the correct instance.
- Delivery workers run in-process and claim jobs targeted to their instance.

## WebSocket protocol

Client sends:

```
{"type": "message", "channel_id": "...", "content": "..."}
```

Server sends:

```
{"type": "ack", "message_id": "..."}
{"type": "message", "message": {...}}
{"type": "presence", "user_id": "...", "status": "online|offline", ...}
```

## Local development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Environment variables (optional):

- `DATABASE_URL` (default: `sqlite+aiosqlite:///./chat.db`)
- `JWT_SECRET` (default: `dev-secret`)
- `INSTANCE_ID` (default: random)
- `ENABLE_BACKGROUND_WORKERS` (default: true)

## Running tests

```bash
pip install -r requirements-dev.txt
pytest
```

## Kubernetes

Apply the manifests in `k8s/`:

```bash
kubectl apply -f k8s/
```

This creates:

- A PostgreSQL deployment + service
- A chat API deployment (3 replicas) + service
- ConfigMap and Secret for configuration

Adjust `JWT_SECRET` and DB credentials before deploying.
