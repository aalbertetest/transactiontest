'use strict';

const http   = require('http');
const fs     = require('fs');
const path   = require('path');
const { WebSocketServer } = require('ws');
const { v4: uuidv4 }      = require('uuid');

const CFG = require('./config');
const { respawnPlayer, serializeWorld } = require('./gameState');
const { LobbyManager, LOBBY_STATE }     = require('./lobbyManager');

// ─── HTTP server ──────────────────────────────────────────────────────────────

const httpServer = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/index.html') {
    fs.readFile(path.join(__dirname, '../client/index.html'), (err, data) => {
      if (err) { res.writeHead(404); res.end('Not found'); return; }
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    });
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

// ─── State ────────────────────────────────────────────────────────────────────

const mgr = new LobbyManager();

// All connected sessions (before or after lobby assignment)
// session: { id, name, ws, role: 'none'|'player'|'spectator', lobbyId: string|null }
const sessions = new Map();   // sessionId → session

// ─── WebSocket server ─────────────────────────────────────────────────────────

const wss = new WebSocketServer({ server: httpServer });

wss.on('connection', (ws) => {
  const sessionId = 'c_' + uuidv4().slice(0, 8);
  const session   = { id: sessionId, name: `Player_${sessionId.slice(2, 6)}`, ws, role: 'none', lobbyId: null };
  sessions.set(sessionId, session);

  console.log(`[+] ${sessionId} connected  (${sessions.size} total)`);

  // Greet with the session id and current lobby list
  sendTo(ws, {
    type:     'welcome',
    sessionId,
    name:     session.name,
    lobbies:  mgr.listLobbies(),
    config: {
      arenaW:           CFG.ARENA_W,
      arenaH:           CFG.ARENA_H,
      playerSpeed:      CFG.PLAYER_SPEED,
      playerRadius:     CFG.PLAYER_RADIUS,
      projectileSpeed:  CFG.PROJECTILE_SPEED,
      projectileRadius: CFG.PROJECTILE_RADIUS,
      projectileTtl:    CFG.PROJECTILE_TTL_MS,
      fireRateMs:       CFG.FIRE_RATE_MS,
      maxHealth:        CFG.MAX_HEALTH,
      tickRateHz:       CFG.TICK_RATE_HZ,
      lobbyMaxPlayers:  CFG.LOBBY_MAX_PLAYERS,
      lobbyMinToStart:  CFG.LOBBY_MIN_TO_START,
      scoreLimit:       CFG.MATCH_SCORE_LIMIT,
      timeLimitS:       CFG.MATCH_TIME_LIMIT_S,
    },
  });

  ws.on('message', (raw) => {
    let msg;
    try { msg = JSON.parse(raw); } catch { return; }
    handleMessage(sessionId, msg);
  });

  ws.on('close', () => handleDisconnect(sessionId));
  ws.on('error', (err) => console.error(`[!] ${sessionId}: ${err.message}`));
});

// ─── Message router ───────────────────────────────────────────────────────────

function handleMessage(sessionId, msg) {
  const session = sessions.get(sessionId);
  if (!session) return;

  switch (msg.type) {
    // ── Lobby hall ────────────────────────────────────────────────────────────
    case 'setName':        handleSetName(session, msg);           break;
    case 'createLobby':    handleCreateLobby(session, msg);       break;
    case 'joinLobby':      handleJoinLobby(session, msg);         break;
    case 'spectate':       handleSpectate(session, msg);          break;
    case 'leaveLobby':     handleLeaveLobby(session);             break;
    case 'joinQueue':      handleJoinQueue(session);              break;
    case 'leaveQueue':     handleLeaveQueue(session);             break;
    case 'listLobbies':    handleListLobbies(session);            break;

    // ── Lobby room ────────────────────────────────────────────────────────────
    case 'setReady':       handleSetReady(session, msg);          break;
    case 'startNow':       handleStartNow(session);               break;

    // ── In-game ───────────────────────────────────────────────────────────────
    case 'input':          handleInput(session, msg);             break;
    case 'ping':           sendTo(session.ws, { type: 'pong', ts: Date.now(), clientTs: msg.clientTs }); break;

    default: break;
  }
}

// ─── Lobby hall handlers ──────────────────────────────────────────────────────

function handleSetName(session, msg) {
  if (typeof msg.name !== 'string') return;
  const name = msg.name.trim().slice(0, 24) || session.name;
  session.name = name;
  sendTo(session.ws, { type: 'nameSet', name });
}

function handleCreateLobby(session, msg) {
  if (session.lobbyId) return sendError(session.ws, 'Already in a lobby.');
  const lobby = mgr.createLobby(msg.name);
  const ok    = lobby.addPlayer(session.id, session.name, session.ws);
  if (!ok) return sendError(session.ws, 'Could not join lobby.');
  session.role    = 'player';
  session.lobbyId = lobby.id;

  sendTo(session.ws, { type: 'joinedLobby', role: 'player', lobby: lobby.toLobbyInfo() });
  broadcastLobbyState(lobby);
  broadcastLobbyList();
  console.log(`[lobby] ${session.id} created & joined ${lobby.id}`);
}

function handleJoinLobby(session, msg) {
  if (session.lobbyId) return sendError(session.ws, 'Already in a lobby.');
  const lobby = mgr.getLobby(msg.lobbyId);
  if (!lobby) return sendError(session.ws, 'Lobby not found.');
  if (!lobby.canJoinAsPlayer()) return sendError(session.ws, 'Lobby is full or in progress.');

  lobby.addPlayer(session.id, session.name, session.ws);
  session.role    = 'player';
  session.lobbyId = lobby.id;

  sendTo(session.ws, { type: 'joinedLobby', role: 'player', lobby: lobby.toLobbyInfo() });
  lobby.broadcastToAll({ type: 'lobbyState', lobby: lobby.toLobbyInfo() });
  broadcastLobbyList();
  checkAutoCountdown(lobby);
  console.log(`[lobby] ${session.id} joined ${lobby.id}`);
}

function handleSpectate(session, msg) {
  if (session.lobbyId) return sendError(session.ws, 'Already in a lobby.');
  const lobby = mgr.getLobby(msg.lobbyId);
  if (!lobby) return sendError(session.ws, 'Lobby not found.');
  if (!lobby.canJoinAsSpectator()) return sendError(session.ws, 'Spectator slots full.');

  lobby.addSpectator(session.id, session.name, session.ws);
  session.role    = 'spectator';
  session.lobbyId = lobby.id;

  sendTo(session.ws, { type: 'joinedLobby', role: 'spectator', lobby: lobby.toLobbyInfo() });

  // Send current world snapshot immediately if match running
  if (lobby.state === LOBBY_STATE.IN_PROGRESS && lobby.world) {
    const snap = serializeWorld(lobby.world);
    sendTo(session.ws, {
      type: 'state', tick: snap.tick, ts: Date.now(),
      players: snap.players, projectiles: snap.projectiles,
    });
  }
  console.log(`[lobby] ${session.id} spectating ${lobby.id}`);
}

function handleLeaveLobby(session) {
  cleanupSessionFromLobby(session);
}

function handleJoinQueue(session) {
  if (session.lobbyId) return sendError(session.ws, 'Leave your current lobby first.');
  mgr.enqueue(session.id, session.name, session.ws);
  sendTo(session.ws, { type: 'queueJoined', queueSize: mgr.queue.size });
  console.log(`[queue] ${session.id} joined (size: ${mgr.queue.size})`);
}

function handleLeaveQueue(session) {
  mgr.dequeue(session.id);
  sendTo(session.ws, { type: 'queueLeft' });
}

function handleListLobbies(session) {
  sendTo(session.ws, { type: 'lobbyList', lobbies: mgr.listLobbies() });
}

// ─── Lobby room handlers ──────────────────────────────────────────────────────

function handleSetReady(session, msg) {
  if (session.role !== 'player' || !session.lobbyId) return;
  const lobby = mgr.getLobby(session.lobbyId);
  if (!lobby || lobby.state !== LOBBY_STATE.WAITING) return;

  lobby.setReady(session.id, !!msg.ready);
  lobby.broadcastToAll({ type: 'lobbyState', lobby: lobby.toLobbyInfo() });
  checkAutoCountdown(lobby);
}

function handleStartNow(session) {
  // Host (first player) can force-start with >= MIN_TO_START players
  if (session.role !== 'player' || !session.lobbyId) return;
  const lobby = mgr.getLobby(session.lobbyId);
  if (!lobby) return;
  if (lobby.state !== LOBBY_STATE.WAITING && lobby.state !== LOBBY_STATE.COUNTDOWN) return;
  if (lobby.players.size < CFG.LOBBY_MIN_TO_START) {
    return sendError(session.ws, `Need at least ${CFG.LOBBY_MIN_TO_START} players.`);
  }
  if (lobby.state === LOBBY_STATE.COUNTDOWN) lobby.cancelCountdown();
  beginCountdown(lobby);
}

// ─── In-game handler ──────────────────────────────────────────────────────────

function handleInput(session, msg) {
  if (session.role !== 'player' || !session.lobbyId) return;
  const lobby = mgr.getLobby(session.lobbyId);
  if (!lobby || lobby.state !== LOBBY_STATE.IN_PROGRESS) return;
  if (!lobby.world || !lobby.world.players.has(session.id)) return;
  lobby.pendingInputs.set(session.id, msg);
}

// ─── Disconnect ───────────────────────────────────────────────────────────────

function handleDisconnect(sessionId) {
  const session = sessions.get(sessionId);
  if (!session) return;
  sessions.delete(sessionId);
  mgr.dequeue(sessionId);
  cleanupSessionFromLobby(session, /* disconnected */ true);
  console.log(`[-] ${sessionId} disconnected  (${sessions.size} total)`);
}

function cleanupSessionFromLobby(session, disconnected = false) {
  if (!session.lobbyId) return;
  const lobby = mgr.getLobby(session.lobbyId);
  session.lobbyId = null;
  session.role    = 'none';
  if (!lobby) return;

  if (session.role === 'spectator' || (lobby.spectators && lobby.spectators.has(session.id))) {
    lobby.removeSpectator(session.id);
    lobby.broadcastToAll({ type: 'lobbyState', lobby: lobby.toLobbyInfo() });
    return;
  }

  const wasInProgress = lobby.state === LOBBY_STATE.IN_PROGRESS;
  lobby.removePlayer(session.id);
  lobby.broadcastToAll({ type: 'playerLeft', playerId: session.id });
  lobby.broadcastToAll({ type: 'lobbyState', lobby: lobby.toLobbyInfo() });

  // If all players gone from an active match, end it
  if (wasInProgress && lobby.players.size === 0) {
    finishMatch(lobby, null, 'abandon');
    return;
  }

  // If a player leaves during countdown and drops below minimum, cancel
  if (lobby.state === LOBBY_STATE.COUNTDOWN && lobby.players.size < CFG.LOBBY_MIN_TO_START) {
    lobby.cancelCountdown();
    lobby.broadcastToAll({ type: 'countdownCancelled', reason: 'Not enough players.' });
    lobby.broadcastToAll({ type: 'lobbyState', lobby: lobby.toLobbyInfo() });
  }

  broadcastLobbyList();
}

// ─── Countdown & match start ──────────────────────────────────────────────────

function checkAutoCountdown(lobby) {
  if (lobby.state !== LOBBY_STATE.WAITING) return;
  if (lobby.allReady) beginCountdown(lobby);
}

function beginCountdown(lobby) {
  if (lobby.state === LOBBY_STATE.COUNTDOWN) return; // already running
  lobby.startCountdown(
    (remaining) => {
      lobby.broadcastToAll({ type: 'countdown', remaining });
    },
    () => {
      startMatch(lobby);
    }
  );
  lobby.broadcastToAll({ type: 'lobbyState', lobby: lobby.toLobbyInfo() });
  console.log(`[lobby] ${lobby.id} countdown started`);
}

function startMatch(lobby) {
  lobby.startMatch();
  lobby.broadcastToAll({ type: 'matchStart', lobbyId: lobby.id, tick: 0 });
  broadcastLobbyList();
  console.log(`[lobby] ${lobby.id} match started (${lobby.players.size} players)`);

  // Per-lobby game loop
  lobby.tickInterval = setInterval(() => runLobbyTick(lobby), CFG.TICK_MS);
}

// ─── Per-lobby game tick ──────────────────────────────────────────────────────

function runLobbyTick(lobby) {
  if (lobby.state !== LOBBY_STATE.IN_PROGRESS) return;

  const now    = Date.now();
  const result = lobby.tick(now);
  if (!result) return;

  const { events, violations } = result;

  // Anti-cheat
  for (const v of violations) {
    const s = sessionByPlayerId(v.playerId);
    if (!s) continue;
    sendTo(s.ws, { type: 'anticheat', reason: v.reason, details: v.details });
    console.warn(`[AC] ${v.playerId} – ${v.reason} (total: ${v.total})`);
    if (v.total >= CFG.MAX_VIOLATIONS) {
      s.ws.close(1008, 'Anti-cheat violation limit reached');
    }
  }

  // Events (hit, killed, respawn)
  for (const evt of events) {
    lobby.broadcastToAll(evt);

    if (evt.type === 'killed') {
      setTimeout(() => {
        if (lobby.state !== LOBBY_STATE.IN_PROGRESS) return;
        const { world: rw, respawnData } = respawnPlayer(lobby.world, evt.targetId);
        if (respawnData) {
          lobby.world = rw;
          lobby.broadcastToAll({ type: 'respawn', ...respawnData });
        }
      }, CFG.RESPAWN_DELAY_MS);
    }
  }

  // Check win condition
  const win = lobby.checkWinCondition();
  if (win) { finishMatch(lobby, win.winnerId, win.reason); return; }

  // Broadcast world snapshot to all in lobby (players + spectators)
  const snap = serializeWorld(lobby.world);
  lobby.broadcastToAll({
    type:        'state',
    tick:        snap.tick,
    ts:          now,
    players:     snap.players,
    projectiles: snap.projectiles,
  });
}

// ─── Match end ────────────────────────────────────────────────────────────────

function finishMatch(lobby, winnerId, reason) {
  if (lobby.state === LOBBY_STATE.FINISHED) return;
  if (lobby.tickInterval) { clearInterval(lobby.tickInterval); lobby.tickInterval = null; }
  lobby.endMatch(winnerId, reason);

  const board = lobby.leaderboard();
  lobby.broadcastToAll({
    type:        'matchOver',
    reason,
    winnerId,
    leaderboard: board,
  });

  console.log(`[lobby] ${lobby.id} match over — winner: ${winnerId} (${reason})`);

  // Destroy lobby after a brief delay (gives clients time to read results)
  setTimeout(() => {
    mgr.destroyLobby(lobby.id);
    broadcastLobbyList();
  }, 10_000);
}

// ─── Matchmaking loop ─────────────────────────────────────────────────────────

setInterval(() => {
  const placed = mgr.runMatchmaking();
  if (placed.length === 0) return;

  // Notify each placed client of their new lobby
  for (const { entry, lobby } of placed) {
    const session = sessions.get(entry.id);
    if (!session) continue;
    session.role    = 'player';
    session.lobbyId = lobby.id;
    sendTo(entry.ws, {
      type:  'matchmakingPlaced',
      lobby: lobby.toLobbyInfo(),
    });
  }

  // Gather unique lobbies and send lobby state + check countdown
  const affectedLobbies = new Set(placed.map(p => p.lobby));
  for (const lobby of affectedLobbies) {
    lobby.broadcastToAll({ type: 'lobbyState', lobby: lobby.toLobbyInfo() });
    checkAutoCountdown(lobby);
  }

  broadcastLobbyList();
  console.log(`[MM] placed ${placed.length} client(s) into lobbies`);
}, CFG.MM_INTERVAL_MS);

// ─── Lobby-list garbage collector ─────────────────────────────────────────────

setInterval(() => mgr.sweep(), 15_000);

// ─── Helpers ─────────────────────────────────────────────────────────────────

function sendTo(ws, msg) {
  if (ws && ws.readyState === 1) ws.send(JSON.stringify(msg));
}

function sendError(ws, message) {
  sendTo(ws, { type: 'error', message });
}

function broadcastLobbyList() {
  const lobbies = mgr.listLobbies();
  const data    = JSON.stringify({ type: 'lobbyList', lobbies });
  for (const s of sessions.values()) {
    if (!s.lobbyId && s.ws.readyState === 1) s.ws.send(data);
  }
}

function broadcastLobbyState(lobby) {
  lobby.broadcastToAll({ type: 'lobbyState', lobby: lobby.toLobbyInfo() });
}

function sessionByPlayerId(playerId) {
  return sessions.get(playerId) || null;
}

// ─── Start ────────────────────────────────────────────────────────────────────

httpServer.listen(CFG.PORT, () => {
  console.log(`Arena game server  →  http://localhost:${CFG.PORT}`);
  console.log(`Tick: ${CFG.TICK_RATE_HZ} Hz  |  Arena: ${CFG.ARENA_W}×${CFG.ARENA_H}  |  Score limit: ${CFG.MATCH_SCORE_LIMIT}`);
});

module.exports = { mgr, sessions, sendTo };
