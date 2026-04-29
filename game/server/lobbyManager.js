'use strict';

/**
 * Lobby & Matchmaking manager.
 *
 * Lifecycle of a lobby:
 *
 *  WAITING → COUNTDOWN → IN_PROGRESS → FINISHED → (destroyed)
 *
 * Spectators may join a lobby in any state except FINISHED.
 * Matchmaking fills WAITING lobbies from the global queue.
 */

const { v4: uuidv4 } = require('uuid');
const CFG            = require('./config');
const { createPlayer, tickWorld, respawnPlayer, serializeWorld } = require('./gameState');

// ─── Constants ────────────────────────────────────────────────────────────────

const LOBBY_STATE = {
  WAITING:     'waiting',
  COUNTDOWN:   'countdown',
  IN_PROGRESS: 'in_progress',
  FINISHED:    'finished',
};

// ─── Lobby class ─────────────────────────────────────────────────────────────

class Lobby {
  constructor(id, name) {
    this.id      = id;
    this.name    = name;
    this.state   = LOBBY_STATE.WAITING;
    this.createdAt = Date.now();

    // Players: Map<playerId, { id, name, ready, ws }>
    this.players    = new Map();
    // Spectators: Map<specId, { id, name, ws }>
    this.spectators = new Map();

    // Game world (only active during IN_PROGRESS)
    this.world       = null;
    this.pendingInputs = new Map();

    this.tickInterval   = null;
    this.lastTick       = null;
    this.countdownTimer = null;
    this.idleTimer      = null;
    this.matchStartTime = null;

    this._resetIdleTimer();
  }

  // ── Membership ──────────────────────────────────────────────────────────────

  canJoinAsPlayer() {
    return (
      this.state === LOBBY_STATE.WAITING &&
      this.players.size < CFG.LOBBY_MAX_PLAYERS
    );
  }

  canJoinAsSpectator() {
    return (
      this.state !== LOBBY_STATE.FINISHED &&
      this.spectators.size < CFG.LOBBY_MAX_SPECTATORS
    );
  }

  addPlayer(playerId, name, ws) {
    if (!this.canJoinAsPlayer()) return false;
    this.players.set(playerId, { id: playerId, name, ready: false, ws });
    this._cancelIdleTimer();
    return true;
  }

  addSpectator(specId, name, ws) {
    if (!this.canJoinAsSpectator()) return false;
    this.spectators.set(specId, { id: specId, name, ws });
    this._cancelIdleTimer();
    return true;
  }

  removePlayer(playerId) {
    this.players.delete(playerId);
    this.pendingInputs.delete(playerId);
    if (this.world) {
      this.world.players.delete(playerId);
    }
    if (this.players.size === 0 && this.spectators.size === 0) {
      this._resetIdleTimer();
    }
  }

  removeSpectator(specId) {
    this.spectators.delete(specId);
    if (this.players.size === 0 && this.spectators.size === 0) {
      this._resetIdleTimer();
    }
  }

  // ── Ready system ─────────────────────────────────────────────────────────────

  setReady(playerId, isReady) {
    const p = this.players.get(playerId);
    if (!p) return;
    p.ready = isReady;
  }

  get readyCount() {
    let n = 0;
    for (const p of this.players.values()) if (p.ready) n++;
    return n;
  }

  get allReady() {
    if (this.players.size < CFG.LOBBY_MIN_TO_START) return false;
    for (const p of this.players.values()) if (!p.ready) return false;
    return true;
  }

  // ── Countdown ────────────────────────────────────────────────────────────────

  startCountdown(onTick, onExpire) {
    if (this.state !== LOBBY_STATE.WAITING) return;
    this.state = LOBBY_STATE.COUNTDOWN;
    let remaining = CFG.LOBBY_COUNTDOWN_S;

    onTick(remaining);
    this.countdownTimer = setInterval(() => {
      remaining--;
      if (remaining <= 0) {
        clearInterval(this.countdownTimer);
        this.countdownTimer = null;
        onExpire();
      } else {
        onTick(remaining);
      }
    }, 1000);
  }

  cancelCountdown() {
    if (this.countdownTimer) {
      clearInterval(this.countdownTimer);
      this.countdownTimer = null;
    }
    if (this.state === LOBBY_STATE.COUNTDOWN) {
      this.state = LOBBY_STATE.WAITING;
    }
  }

  // ── Match ────────────────────────────────────────────────────────────────────

  startMatch() {
    this.state = LOBBY_STATE.IN_PROGRESS;
    this.matchStartTime = Date.now();

    // Create game world with all players
    const worldPlayers = new Map();
    for (const [id] of this.players) {
      const gp = createPlayer(id);
      worldPlayers.set(id, gp);
    }
    this.world = {
      players:     worldPlayers,
      projectiles: new Map(),
      tick:        0,
    };
    this.pendingInputs = new Map();

    this.lastTick = Date.now();
  }

  tick(now) {
    if (this.state !== LOBBY_STATE.IN_PROGRESS || !this.world) return null;

    const dt = (now - this.lastTick) / 1000;
    this.lastTick = now;

    const { world: nextWorld, events, violations } = tickWorld(
      this.world, this.pendingInputs, now, dt
    );
    this.world = nextWorld;

    return { events, violations };
  }

  checkWinCondition() {
    if (!this.world) return null;
    // Score limit
    for (const p of this.world.players.values()) {
      if (p.score >= CFG.MATCH_SCORE_LIMIT) return { reason: 'score', winnerId: p.id };
    }
    // Time limit
    const elapsed = (Date.now() - this.matchStartTime) / 1000;
    if (elapsed >= CFG.MATCH_TIME_LIMIT_S) {
      // Find highest score
      let best = null;
      for (const p of this.world.players.values()) {
        if (!best || p.score > best.score) best = p;
      }
      return { reason: 'time', winnerId: best ? best.id : null };
    }
    return null;
  }

  endMatch(winnerId, reason) {
    this.state = LOBBY_STATE.FINISHED;
    if (this.tickInterval) { clearInterval(this.tickInterval); this.tickInterval = null; }
  }

  // ── Leaderboard snapshot ─────────────────────────────────────────────────────

  leaderboard() {
    if (!this.world) return [];
    const rows = [];
    for (const p of this.world.players.values()) {
      const meta = this.players.get(p.id);
      rows.push({ id: p.id, name: meta ? meta.name : p.id, score: p.score, alive: p.alive });
    }
    return rows.sort((a, b) => b.score - a.score);
  }

  // ── Serialize for lobby-list / lobby-state messages ──────────────────────────

  toLobbyInfo() {
    return {
      id:          this.id,
      name:        this.name,
      state:       this.state,
      playerCount: this.players.size,
      maxPlayers:  CFG.LOBBY_MAX_PLAYERS,
      spectatorCount: this.spectators.size,
      players: [...this.players.values()].map(p => ({
        id:    p.id,
        name:  p.name,
        ready: p.ready,
      })),
    };
  }

  // ── Broadcast helpers ────────────────────────────────────────────────────────

  broadcastToAll(msg) {
    const data = JSON.stringify(msg);
    for (const p of this.players.values()) wsend(p.ws, data);
    for (const s of this.spectators.values()) wsend(s.ws, data);
  }

  broadcastToPlayers(msg) {
    const data = JSON.stringify(msg);
    for (const p of this.players.values()) wsend(p.ws, data);
  }

  broadcastToSpectators(msg) {
    const data = JSON.stringify(msg);
    for (const s of this.spectators.values()) wsend(s.ws, data);
  }

  sendToOne(id, msg) {
    const p = this.players.get(id) || this.spectators.get(id);
    if (p) wsend(p.ws, JSON.stringify(msg));
  }

  // ── Idle timer ───────────────────────────────────────────────────────────────

  _resetIdleTimer() {
    this._cancelIdleTimer();
    this.idleTimer = setTimeout(() => {
      this._shouldDestroy = true;
    }, CFG.LOBBY_IDLE_TIMEOUT_MS);
  }

  _cancelIdleTimer() {
    if (this.idleTimer) { clearTimeout(this.idleTimer); this.idleTimer = null; }
  }

  destroy() {
    if (this.tickInterval)   clearInterval(this.tickInterval);
    if (this.countdownTimer) clearInterval(this.countdownTimer);
    if (this.idleTimer)      clearTimeout(this.idleTimer);
  }
}

// ─── Helper: safe WebSocket send ─────────────────────────────────────────────

function wsend(ws, data) {
  if (ws && ws.readyState === 1 /* OPEN */) ws.send(data);
}

// ─── LobbyManager class ───────────────────────────────────────────────────────

class LobbyManager {
  constructor() {
    this.lobbies = new Map();   // lobbyId → Lobby
    this.queue   = new Map();   // clientId → { id, name, ws, joinedAt }
  }

  // ── Lobby CRUD ───────────────────────────────────────────────────────────────

  createLobby(name) {
    const id    = 'lobby_' + uuidv4().slice(0, 8);
    const lobby = new Lobby(id, name || `Arena ${this.lobbies.size + 1}`);
    this.lobbies.set(id, lobby);
    return lobby;
  }

  getLobby(id) { return this.lobbies.get(id) || null; }

  listLobbies() {
    return [...this.lobbies.values()]
      .filter(l => l.state !== LOBBY_STATE.FINISHED)
      .map(l => l.toLobbyInfo());
  }

  destroyLobby(lobbyId) {
    const lobby = this.lobbies.get(lobbyId);
    if (lobby) { lobby.destroy(); this.lobbies.delete(lobbyId); }
  }

  // ── Matchmaking queue ────────────────────────────────────────────────────────

  enqueue(clientId, name, ws) {
    if (!this.queue.has(clientId)) {
      this.queue.set(clientId, { id: clientId, name, ws, joinedAt: Date.now() });
    }
  }

  dequeue(clientId) { this.queue.delete(clientId); }

  runMatchmaking() {
    if (this.queue.size < CFG.MM_MIN_QUEUE_TO_FILL) return [];

    const placed = [];

    // Fill existing WAITING lobbies first, then create new ones
    for (const [, entry] of this.queue) {
      let placed_ = false;
      for (const lobby of this.lobbies.values()) {
        if (lobby.canJoinAsPlayer()) {
          lobby.addPlayer(entry.id, entry.name, entry.ws);
          placed.push({ entry, lobby });
          placed_ = true;
          break;
        }
      }
      if (!placed_) {
        const lobby = this.createLobby();
        lobby.addPlayer(entry.id, entry.name, entry.ws);
        placed.push({ entry, lobby });
      }
    }

    for (const { entry } of placed) this.queue.delete(entry.id);
    return placed;
  }

  // ── Sweep finished / idle lobbies ────────────────────────────────────────────

  sweep() {
    for (const [id, lobby] of this.lobbies) {
      if (lobby._shouldDestroy || lobby.state === LOBBY_STATE.FINISHED) {
        lobby.destroy();
        this.lobbies.delete(id);
      }
    }
  }
}

module.exports = { LobbyManager, Lobby, LOBBY_STATE };
