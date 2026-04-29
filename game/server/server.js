'use strict';

const http    = require('http');
const { WebSocketServer } = require('ws');
const { v4: uuidv4 }      = require('uuid');

const CFG = require('./config');
const {
  createPlayer,
  tickWorld,
  respawnPlayer,
  serializeWorld,
} = require('./gameState');

// ─── World state ─────────────────────────────────────────────────────────────

let world = {
  players:     new Map(),   // id → player
  projectiles: new Map(),   // id → projectile
  tick:        0,
};

// Latest unprocessed input per player
const pendingInputs = new Map();   // playerId → input

// WebSocket connections
const clients = new Map();         // playerId → ws

// ─── HTTP server (serves the client HTML on /) ───────────────────────────────

const fs = require('fs');
const path = require('path');

const httpServer = http.createServer((req, res) => {
  if (req.url === '/' || req.url === '/index.html') {
    const filePath = path.join(__dirname, '../client/index.html');
    fs.readFile(filePath, (err, data) => {
      if (err) {
        res.writeHead(404);
        res.end('Not found');
        return;
      }
      res.writeHead(200, { 'Content-Type': 'text/html' });
      res.end(data);
    });
  } else {
    res.writeHead(404);
    res.end('Not found');
  }
});

// ─── WebSocket server ─────────────────────────────────────────────────────────

const wss = new WebSocketServer({ server: httpServer });

wss.on('connection', (ws) => {
  const playerId = 'p_' + uuidv4().slice(0, 8);
  clients.set(playerId, ws);

  // Add player to world
  const player = createPlayer(playerId);
  world.players.set(playerId, player);

  console.log(`[+] ${playerId} connected  (${clients.size} total)`);

  // Send init message
  send(ws, {
    type:     'init',
    playerId,
    tick:     world.tick,
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
    },
  });

  // Broadcast playerJoined to others
  broadcast({
    type:   'playerJoined',
    player: {
      id:     player.id,
      x:      player.x,
      y:      player.y,
      health: player.health,
      score:  player.score,
      alive:  player.alive,
    },
  }, playerId);

  // ── Message handler ─────────────────────────────────────────────────────
  ws.on('message', (raw) => {
    let msg;
    try {
      msg = JSON.parse(raw);
    } catch {
      return;
    }

    switch (msg.type) {
      case 'input':
        handleInput(playerId, msg);
        break;

      case 'ping':
        send(ws, { type: 'pong', ts: Date.now(), clientTs: msg.clientTs });
        break;

      default:
        break;
    }
  });

  ws.on('close', () => {
    world.players.delete(playerId);
    clients.delete(playerId);
    pendingInputs.delete(playerId);
    console.log(`[-] ${playerId} disconnected (${clients.size} total)`);
    broadcast({ type: 'playerLeft', playerId });
  });

  ws.on('error', (err) => {
    console.error(`[!] ${playerId} error: ${err.message}`);
  });
});

// ─── Input handler ────────────────────────────────────────────────────────────

function handleInput(playerId, msg) {
  // Basic sanity: ignore inputs for unknown players
  if (!world.players.has(playerId)) return;

  // Only keep the latest input per player (server integrates at tick rate)
  pendingInputs.set(playerId, msg);
}

// ─── Game loop ────────────────────────────────────────────────────────────────

let lastTick = Date.now();

function gameTick() {
  const now = Date.now();
  const dt  = (now - lastTick) / 1000;
  lastTick  = now;

  const { world: nextWorld, events, violations } = tickWorld(world, pendingInputs, now, dt);
  world = nextWorld;

  // Handle anti-cheat violations
  for (const v of violations) {
    const ws = clients.get(v.playerId);
    if (!ws) continue;
    send(ws, { type: 'anticheat', reason: v.reason, details: v.details });
    console.warn(`[AC] ${v.playerId} – ${v.reason}: ${v.details} (total: ${v.total})`);

    if (v.total >= CFG.MAX_VIOLATIONS) {
      console.warn(`[AC] Disconnecting ${v.playerId} after ${v.total} violations`);
      ws.close(1008, 'Anti-cheat violation limit reached');
    }
  }

  // Broadcast events (hit, killed)
  for (const event of events) {
    broadcast(event);

    // Schedule respawn
    if (event.type === 'killed') {
      setTimeout(() => {
        const { world: respawnedWorld, respawnData } = respawnPlayer(world, event.targetId);
        if (respawnData) {
          world = respawnedWorld;
          broadcast({ type: 'respawn', ...respawnData });
        }
      }, CFG.RESPAWN_DELAY_MS);
    }
  }

  // Broadcast world state snapshot
  const snapshot = serializeWorld(world);
  broadcast({
    type: 'state',
    tick: snapshot.tick,
    ts:   now,
    players:     snapshot.players,
    projectiles: snapshot.projectiles,
  });
}

setInterval(gameTick, CFG.TICK_MS);

// ─── Helpers ─────────────────────────────────────────────────────────────────

function send(ws, msg) {
  if (ws.readyState === ws.OPEN) {
    ws.send(JSON.stringify(msg));
  }
}

function broadcast(msg, excludeId = null) {
  const data = JSON.stringify(msg);
  for (const [id, ws] of clients) {
    if (id === excludeId) continue;
    if (ws.readyState === ws.OPEN) {
      ws.send(data);
    }
  }
}

// ─── Start ────────────────────────────────────────────────────────────────────

httpServer.listen(CFG.PORT, () => {
  console.log(`Arena game server running on http://localhost:${CFG.PORT}`);
  console.log(`Tick rate: ${CFG.TICK_RATE_HZ} Hz  |  Arena: ${CFG.ARENA_W}×${CFG.ARENA_H}`);
});

module.exports = { world, clients, broadcast }; // exported for tests
