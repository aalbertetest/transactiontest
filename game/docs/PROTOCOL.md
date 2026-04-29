# WebSocket Game Protocol Specification

## Overview

All messages are JSON-encoded. Each message has a `type` field identifying the
message kind and an optional `seq` (sequence number) for ordering/reconciliation.

Messages flow over a single WebSocket connection per client.

---

## Transport

- **Protocol**: WebSocket (ws://)
- **Encoding**: JSON text frames
- **Tick rate**: Server runs at 20 Hz (50 ms tick); clients run at 60 fps
- **Direction markers**: C→S (client to server), S→C (server to client)

---

## Message Types

### C→S: `input`

Sent every frame (or on change). Contains the client's current input state plus
a monotonically increasing sequence number used for reconciliation.

```json
{
  "type": "input",
  "seq": 1042,
  "tick": 312,
  "keys": {
    "up":    false,
    "down":  true,
    "left":  false,
    "right": true
  },
  "fire": false,
  "angle": 1.5707963
}
```

| Field   | Type    | Description                                         |
|---------|---------|-----------------------------------------------------|
| `seq`   | uint32  | Monotonic input sequence number (client-side)       |
| `tick`  | uint32  | Last server tick the client is aware of             |
| `keys`  | object  | Boolean WASD/arrow key states                       |
| `fire`  | boolean | Whether the fire button is held                     |
| `angle` | float   | Mouse/aim angle in radians from player center       |

---

### S→C: `init`

Sent once on connection. Provides the assigned player ID and initial world state.

```json
{
  "type": "init",
  "playerId": "p_abc123",
  "tick": 0,
  "config": {
    "arenaW": 1200,
    "arenaH": 800,
    "playerSpeed": 200,
    "playerRadius": 16,
    "projectileSpeed": 450,
    "projectileRadius": 5,
    "projectileTtl": 2000,
    "fireRateMs": 250,
    "maxHealth": 100,
    "tickRateHz": 20
  }
}
```

---

### S→C: `state`

Authoritative world snapshot sent every server tick to all connected clients.

```json
{
  "type": "state",
  "tick": 313,
  "ts":   1714412800123,
  "players": [
    {
      "id": "p_abc123",
      "x": 340.5,
      "y": 210.0,
      "vx": 141.4,
      "vy": 141.4,
      "angle": 0.785,
      "health": 80,
      "score": 3,
      "alive": true,
      "lastInputSeq": 1042
    }
  ],
  "projectiles": [
    {
      "id": "proj_001",
      "ownerId": "p_abc123",
      "x": 400.0,
      "y": 250.0,
      "vx": 318.2,
      "vy": 318.2,
      "ttl": 1750
    }
  ]
}
```

| Field              | Type    | Description                                      |
|--------------------|---------|--------------------------------------------------|
| `tick`             | uint32  | Server tick counter                              |
| `ts`               | uint64  | Server Unix timestamp ms (for lag estimation)    |
| `players`          | array   | All connected players' states                    |
| `lastInputSeq`     | uint32  | Echoed back so client can discard stale predictions |
| `projectiles`      | array   | All active projectiles                           |

---

### S→C: `playerJoined`

Broadcast when a new player connects.

```json
{
  "type": "playerJoined",
  "player": {
    "id": "p_xyz789",
    "x": 600.0,
    "y": 400.0,
    "health": 100,
    "score": 0,
    "alive": true
  }
}
```

---

### S→C: `playerLeft`

Broadcast when a player disconnects.

```json
{
  "type": "playerLeft",
  "playerId": "p_xyz789"
}
```

---

### S→C: `hit`

Sent to the player that was hit and to the shooter (for score update).

```json
{
  "type": "hit",
  "targetId":  "p_abc123",
  "shooterId": "p_xyz789",
  "damage":    20,
  "health":    60
}
```

---

### S→C: `killed`

Broadcast when a player is eliminated.

```json
{
  "type": "killed",
  "targetId":  "p_abc123",
  "shooterId": "p_xyz789"
}
```

---

### S→C: `respawn`

Sent to the eliminated player after respawn delay.

```json
{
  "type": "respawn",
  "playerId": "p_abc123",
  "x": 150.0,
  "y": 300.0,
  "health": 100
}
```

---

### S→C: `anticheat`

Sent to a client when a suspicious action is detected.  
Repeated violations result in disconnection.

```json
{
  "type":    "anticheat",
  "reason":  "speed_violation",
  "details": "measured 520 px/s, max allowed 220 px/s"
}
```

| `reason` value      | Meaning                          |
|---------------------|----------------------------------|
| `speed_violation`   | Player moved faster than allowed |
| `teleport`          | Position jumped > threshold      |
| `fire_rate`         | Fired faster than allowed        |

---

### S→C: `pong`

Response to a client-sent `ping` for RTT measurement.

```json
{ "type": "pong", "ts": 1714412800123, "clientTs": 1714412800100 }
```

### C→S: `ping`

```json
{ "type": "ping", "clientTs": 1714412800100 }
```

---

## Client Prediction & Reconciliation

1. Client applies `input` locally immediately (prediction).
2. Client stores a ring-buffer of `(seq, inputState, predictedPosition)`.
3. On receiving a `state` snapshot the client:
   - Discards all buffered inputs with `seq ≤ lastInputSeq`.
   - Rewinds position to the server-authoritative position.
   - Re-applies all remaining buffered inputs forward.
   - Smoothly interpolates the visual position toward the reconciled position.

---

## Anti-Cheat Checks (Server-Side)

| Check         | Logic                                                                 |
|---------------|-----------------------------------------------------------------------|
| Speed         | Compare distance moved per tick against `maxSpeed * tickDt * 1.15` tolerance |
| Teleport      | Flag if positional delta > 2× arena diagonal in one tick             |
| Fire rate     | Track `lastFireTime`; reject shots < `fireRateMs` apart              |
| Input sanity  | Reject inputs with `seq` far behind or far ahead of last known seq   |
