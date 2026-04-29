# WebSocket Game Protocol Specification

## Overview

All messages are JSON-encoded text frames. Each has a `type` field.  
Direction markers: **C→S** (client to server), **S→C** (server to client).

---

## Transport

| Property | Value |
|----------|-------|
| Protocol | WebSocket (ws://) |
| Encoding | JSON text frames |
| Server tick | 20 Hz (50 ms) |
| Client render | 60 fps |

---

## Connection lifecycle

```
Client connects
  └─ S→C  welcome           (session id, lobby list, config)
  └─ C→S  setName           (optional — set display name)

In lobby hall:
  C→S  createLobby | joinLobby | spectate | joinQueue | leaveQueue | listLobbies

In lobby room (WAITING state):
  C→S  setReady | startNow | leaveLobby
  S→C  lobbyState            (broadcast on any change)
  S→C  countdown             (remaining seconds)
  S→C  countdownCancelled

Match running (IN_PROGRESS):
  C→S  input                 (20 Hz)
  S→C  state                 (20 Hz broadcast to players + spectators)
  S→C  hit | killed | respawn | playerLeft
  S→C  matchOver             (final leaderboard)

Any time:
  C→S  ping  →  S→C  pong
  S→C  error
  S→C  anticheat
```

---

## Message Catalogue

---

### S→C `welcome`

Sent immediately on connection.

```json
{
  "type":      "welcome",
  "sessionId": "c_ab12ef34",
  "name":      "Player_ab12",
  "lobbies":   [...],
  "config": {
    "arenaW": 1200, "arenaH": 800,
    "playerSpeed": 200, "playerRadius": 16,
    "projectileSpeed": 450, "projectileRadius": 5,
    "projectileTtl": 2000, "fireRateMs": 250,
    "maxHealth": 100, "tickRateHz": 20,
    "lobbyMaxPlayers": 8, "lobbyMinToStart": 2,
    "scoreLimit": 10, "timeLimitS": 300
  }
}
```

---

### C→S `setName`

Set or change display name (≤24 chars). Server echoes `nameSet`.

```json
{ "type": "setName", "name": "Alice" }
```

### S→C `nameSet`

```json
{ "type": "nameSet", "name": "Alice" }
```

---

### C→S `createLobby`

Create a new lobby and join it as a player.

```json
{ "type": "createLobby", "name": "Friendly duel" }
```

### C→S `joinLobby`

Join an existing WAITING lobby as a player.

```json
{ "type": "joinLobby", "lobbyId": "lobby_ab12ef34" }
```

### C→S `spectate`

Join any non-FINISHED lobby as a spectator (read-only).

```json
{ "type": "spectate", "lobbyId": "lobby_ab12ef34" }
```

### S→C `joinedLobby`

Sent to the joining client after a successful `createLobby`, `joinLobby`, or `spectate`.

```json
{
  "type":  "joinedLobby",
  "role":  "player",
  "lobby": { ...LobbyInfo }
}
```

`role` is `"player"` or `"spectator"`.

---

### C→S `leaveLobby`

Leave the current lobby (returns client to hall state).

```json
{ "type": "leaveLobby" }
```

---

### C→S `joinQueue` / `leaveQueue`

Opt into automatic matchmaking. The server runs the matchmaker every 2 s,
pairs clients into lobbies, and sends `matchmakingPlaced`.

```json
{ "type": "joinQueue" }
{ "type": "leaveQueue" }
```

### S→C `queueJoined`

```json
{ "type": "queueJoined", "queueSize": 4 }
```

### S→C `queueLeft`

```json
{ "type": "queueLeft" }
```

### S→C `matchmakingPlaced`

Sent when the matchmaker assigns a client to a lobby.

```json
{
  "type":  "matchmakingPlaced",
  "lobby": { ...LobbyInfo }
}
```

---

### C→S `listLobbies`

Request a fresh lobby list.

```json
{ "type": "listLobbies" }
```

### S→C `lobbyList`

Sent to clients in the hall (not in a lobby) whenever a lobby changes,
or in response to `listLobbies`.

```json
{
  "type":    "lobbyList",
  "lobbies": [ ...LobbyInfo ]
}
```

---

### S→C `lobbyState`

Broadcast to everyone in a lobby whenever membership or ready-state changes.

```json
{
  "type":  "lobbyState",
  "lobby": { ...LobbyInfo }
}
```

**LobbyInfo schema:**

```json
{
  "id":            "lobby_ab12ef34",
  "name":          "Friendly duel",
  "state":         "waiting",
  "playerCount":   2,
  "maxPlayers":    8,
  "spectatorCount": 1,
  "players": [
    { "id": "c_aa11bb22", "name": "Alice", "ready": true },
    { "id": "c_cc33dd44", "name": "Bob",   "ready": false }
  ]
}
```

`state` values: `waiting` | `countdown` | `in_progress` | `finished`

---

### C→S `setReady`

Toggle ready status in the lobby room.

```json
{ "type": "setReady", "ready": true }
```

When **all players** mark ready (and count ≥ `lobbyMinToStart`), the server
starts the countdown automatically.

---

### C→S `startNow`

Force-start the countdown (skips full-ready requirement). Requires ≥ `lobbyMinToStart` players.

```json
{ "type": "startNow" }
```

---

### S→C `countdown`

Sent every second during the pre-match countdown.

```json
{ "type": "countdown", "remaining": 3 }
```

### S→C `countdownCancelled`

Countdown aborted (player left, dropping below minimum).

```json
{ "type": "countdownCancelled", "reason": "Not enough players." }
```

---

### S→C `matchStart`

Match begins. Clients should initialize game state.

```json
{ "type": "matchStart", "lobbyId": "lobby_ab12ef34", "tick": 0 }
```

---

### C→S `input`

Sent every frame (or whenever input changes). Same as before.

```json
{
  "type":  "input",
  "seq":   1042,
  "tick":  312,
  "keys":  { "up": false, "down": true, "left": false, "right": true },
  "fire":  false,
  "angle": 1.5707963
}
```

---

### S→C `state`

Authoritative world snapshot, 20 Hz. Sent to **all** lobby members (players + spectators).

```json
{
  "type": "state",
  "tick": 313,
  "ts":   1714412800123,
  "players": [
    {
      "id": "c_aa11bb22",
      "x": 340.5, "y": 210.0,
      "vx": 141.4, "vy": 141.4,
      "angle": 0.785,
      "health": 80, "score": 3, "alive": true,
      "lastInputSeq": 1042
    }
  ],
  "projectiles": [
    { "id": "...", "ownerId": "c_aa11bb22", "x": 400, "y": 250, "vx": 318, "vy": 318 }
  ]
}
```

---

### S→C `hit`

```json
{ "type": "hit", "targetId": "c_aa11bb22", "shooterId": "c_cc33dd44", "damage": 20, "health": 60 }
```

### S→C `killed`

```json
{ "type": "killed", "targetId": "c_aa11bb22", "shooterId": "c_cc33dd44" }
```

### S→C `respawn`

```json
{ "type": "respawn", "playerId": "c_aa11bb22", "x": 150.0, "y": 300.0, "health": 100 }
```

### S→C `playerLeft`

Player disconnected or left lobby during match.

```json
{ "type": "playerLeft", "playerId": "c_aa11bb22" }
```

---

### S→C `matchOver`

Match ends (score limit, time limit, or all players abandoned).

```json
{
  "type":      "matchOver",
  "reason":    "score",
  "winnerId":  "c_aa11bb22",
  "leaderboard": [
    { "id": "c_aa11bb22", "name": "Alice", "score": 10, "alive": true },
    { "id": "c_cc33dd44", "name": "Bob",   "score":  4, "alive": false }
  ]
}
```

`reason` values: `score` | `time` | `abandon`

The lobby is destroyed ~10 s after this message.

---

### S→C `anticheat`

```json
{ "type": "anticheat", "reason": "speed_violation", "details": "..." }
```

| reason | trigger |
|--------|---------|
| `speed_violation` | moved > `playerSpeed × dt × 1.20` |
| `teleport` | position jumped > 400 px |
| `fire_rate` | fired faster than `fireRateMs` |

5 violations → disconnect.

---

### S→C `error`

```json
{ "type": "error", "message": "Lobby is full or in progress." }
```

---

### C→S `ping` / S→C `pong`

```json
{ "type": "ping", "clientTs": 1714412800100 }
{ "type": "pong", "ts": 1714412800123, "clientTs": 1714412800100 }
```

---

## Client Prediction & Reconciliation

1. Client applies `input` locally immediately.
2. Stores `{ seq, input, x, y }` in a ring-buffer.
3. On each `state` snapshot:
   - Discard buffer entries with `seq ≤ lastInputSeq`.
   - Rewind to server-authoritative position.
   - Re-apply remaining buffer entries.
   - Smooth-correct visually (snap if error > 10 px, otherwise lerp 30%).

Spectators skip prediction entirely and render the raw server `state`.

---

## Anti-Cheat (server-side)

| Check | Logic |
|-------|-------|
| Speed | `moved > playerSpeed × dt × 1.20` → `speed_violation` |
| Teleport | `delta > 400 px` in one tick → `teleport` |
| Fire rate | `now - lastFireTime < fireRateMs` → shot silently dropped |
| Repeat | 5 violations → WS close 1008 |

---

## Lobby State Machine

```
WAITING
  │  (all ready OR force-start)
  ▼
COUNTDOWN  ──(player leaves, < min)──► WAITING
  │  (timer expires)
  ▼
IN_PROGRESS  ──(score/time/abandon)──► FINISHED ──(10 s)──► destroyed
```

Spectators may join in WAITING, COUNTDOWN, or IN_PROGRESS.
