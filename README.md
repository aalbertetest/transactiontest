# Multiplayer Game Backend

This repository contains a production-ready multiplayer backend skeleton with
matchmaking, authoritative state sync, persistence, anti-cheat checks, and
deployment configs.

## Features

- **Matchmaking**: region-aware queue, Redis-backed option for multi-instance
  coordination.
- **State sync**: authoritative server state, sequence-validated inputs, and
  broadcast snapshots.
- **Networking**: REST APIs for matchmaking + WebSocket game sessions.
- **Persistence**: PostgreSQL/SQLite support for sessions, tickets, and event logs.
- **Anti-cheat**: input validation, rate limiting, sequence checks, and
  violation tracking.
- **Scaling**: stateless API servers, Redis queues, shared database, cleanup of
  inactive sessions.

## Architecture Overview

```
Clients -> HTTP API (FastAPI) -> Postgres
        -> WebSocket Game Sessions
        -> Redis (matchmaking queue, optional)
```

The server is authoritative: clients send input deltas, and the server computes
movement, broadcasts the latest state, and persists events for audit.

## API Endpoints

### Authentication

```
POST /auth/issue
{ "player_id": "player-123" }
```

Returns a signed token used in headers or WebSocket query params.

### Matchmaking

- `POST /matchmaking/join`
- `GET /matchmaking/status/{ticket_id}`
- `POST /matchmaking/cancel/{ticket_id}`

Headers required:

```
X-Player-Id: player-123
X-Player-Token: <token>
```

### Sessions

```
GET /sessions/{session_id}
```

### WebSocket Game Loop

```
ws://host/ws/game/{session_id}?player_id=player-123&token=<token>
```

Client input payload:

```json
{
  "type": "input",
  "seq": 42,
  "dx": 1.0,
  "dy": 0.0,
  "dt": 0.05
}
```

Server broadcast payload:

```json
{
  "type": "state",
  "session_id": "...",
  "version": 7,
  "server_ts": 1735689600.0,
  "players": {
    "player-123": { "x": 1.2, "y": 0.4 }
  }
}
```

## Local Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
uvicorn app.main:app --reload
```

## Running with Docker

```bash
docker compose up --build
```

## Testing

```bash
pytest
```

## Scaling Notes

- Run multiple API instances behind a load balancer.
- Use Redis queue backend for matchmaking to avoid per-node queues.
- Store persistent state in Postgres and emit events for audit/analytics.
- Increase WebSocket capacity by sharding sessions or routing by session_id.
- Use external observability (logs/metrics/traces) to detect abuse patterns.
