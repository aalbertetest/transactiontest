# Arena — Realtime Multiplayer Game Prototype

A top-down arena shooter with an authoritative WebSocket server, client-side
prediction, server reconciliation, lag simulation, and basic anti-cheat.

```
game/
├── server/
│   ├── server.js        ← WebSocket + HTTP server entry point
│   ├── gameState.js     ← Pure state reducer (players, projectiles, physics)
│   ├── config.js        ← Tunable constants
│   ├── package.json
│   └── tests/
│       └── gameState.test.js   ← Node built-in test runner
├── client/
│   └── index.html       ← Self-contained HTML canvas client
├── tests/
│   └── loadtest.js      ← 200-client load test script
└── docs/
    └── PROTOCOL.md      ← Message schema reference
```

---

## Quick Start

### 1. Install dependencies

```bash
cd game/server
npm install
```

### 2. Start the server

```bash
npm start
# → Arena game server running on http://localhost:8080
```

### 3. Open the client

Navigate to [http://localhost:8080](http://localhost:8080) in your browser.
Open multiple tabs to test multiplayer. The server URL field defaults to
`ws://localhost:8080`.

---

## Running Unit Tests

```bash
cd game/server
node --test tests/gameState.test.js
```

Tests cover:
- `clamp` / `dist` helpers
- `createPlayer` — bounds, health, alive state
- `applyInput` — movement, normalisation, clamping, fire rate, angle
- Anti-cheat — speed and teleport detection
- `tickWorld` — tick counter, projectile lifecycle, hit/kill events, scoring
- `respawnPlayer` — health restore, arena bounds
- `serializeWorld` — array output, no internal fields leaked

---

## Load Test (200 clients)

Requires the server to be running.

```bash
cd game/tests
node loadtest.js [clients] [duration_s] [server_url]

# Default: 200 clients, 30 seconds, ws://localhost:8080
node loadtest.js

# Example: 50 clients for 10 s against a remote server
node loadtest.js 50 10 ws://example.com:8080
```

Set `VERBOSE=1` to see per-bot error messages.

The report prints:
- Connected / initialized client counts
- Total messages and bytes transferred (RX/TX, KB/s)
- RTT statistics: mean, p50, p95, p99

---

## Architecture

### Server (Node.js + ws)

- Single-threaded game loop at **20 Hz** (`setInterval`).
- `tickWorld()` is a **pure function** — takes a world snapshot + pending inputs
  and returns the next world + events. No side effects; fully testable.
- Broadcasts the full state snapshot every tick.
- Handles respawns via `setTimeout` (off-tick, no impact on frame budget).

### Client (vanilla JS + Canvas)

| Feature | Details |
|---------|---------|
| Client prediction | Applies input locally at 60 fps; does not wait for server round-trip |
| Prediction buffer | Ring-buffer of `(seq, input, position)` |
| Server reconciliation | On every server snapshot: discard acked inputs, rewind to server pos, re-apply remaining inputs; smooth-corrects position if delta < 10px |
| Interpolation | Remote players rendered 100 ms behind real-time using two-snapshot lerp |
| Lag simulation | Optional delay queue; slider from 0–500 ms |
| Toggles | Prediction / reconciliation / interpolation / lag / debug overlay all individually switchable at runtime |

### Anti-Cheat (server-side)

| Check | Threshold |
|-------|-----------|
| Speed | `playerSpeed * dt * 1.20` tolerance per tick |
| Teleport | > 400 px jump in one tick |
| Fire rate | Server tracks `lastFireTime`; drops early shots silently |
| Repeat violations | Client receives `anticheat` message; disconnected after 5 total |

---

## Protocol

See [`docs/PROTOCOL.md`](docs/PROTOCOL.md) for full message schemas.

Key message types:

| Type | Direction | Purpose |
|------|-----------|---------|
| `init` | S→C | Player ID + world config |
| `input` | C→S | Key state + aim angle + seq number |
| `state` | S→C | Full authoritative snapshot (20 Hz) |
| `hit` | S→C | Damage event |
| `killed` | S→C | Elimination event |
| `respawn` | S→C | Respawn position |
| `playerJoined` | S→C | New connection broadcast |
| `playerLeft` | S→C | Disconnection broadcast |
| `anticheat` | S→C | Violation notice |
| `ping` / `pong` | C↔S | RTT measurement |

---

## Configuration

All server constants live in `server/config.js`:

```js
PLAYER_SPEED:      200,    // px/s
PLAYER_RADIUS:     16,
PROJECTILE_SPEED:  450,    // px/s
PROJECTILE_TTL_MS: 2000,
FIRE_RATE_MS:      250,
TICK_RATE_HZ:      20,
RESPAWN_DELAY_MS:  3000,
ARENA_W:           1200,
ARENA_H:           800,
MAX_VIOLATIONS:    5,
```

The server sends `config` to clients in the `init` message so the client mirrors
the same constants without duplication.

---

## Environment Variable

| Variable | Default | Purpose |
|----------|---------|---------|
| `PORT` | `8080` | HTTP + WebSocket port |
