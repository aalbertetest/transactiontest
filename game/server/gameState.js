'use strict';

/**
 * Pure game-state reducer.
 *
 * All functions are side-effect-free and operate on plain JS objects so they
 * can be tested independently of the WebSocket layer.
 */

const { v4: uuidv4 } = require('uuid');
const CFG = require('./config');

// ─── Helpers ─────────────────────────────────────────────────────────────────

function clamp(v, lo, hi) {
  return v < lo ? lo : v > hi ? hi : v;
}

function dist(ax, ay, bx, by) {
  const dx = ax - bx;
  const dy = ay - by;
  return Math.sqrt(dx * dx + dy * dy);
}

function randomSpawn() {
  return {
    x: CFG.PLAYER_RADIUS + Math.random() * (CFG.ARENA_W - CFG.PLAYER_RADIUS * 2),
    y: CFG.PLAYER_RADIUS + Math.random() * (CFG.ARENA_H - CFG.PLAYER_RADIUS * 2),
  };
}

// ─── Player factory ───────────────────────────────────────────────────────────

function createPlayer(id) {
  const spawn = randomSpawn();
  return {
    id,
    x: spawn.x,
    y: spawn.y,
    vx: 0,
    vy: 0,
    angle: 0,
    health: CFG.MAX_HEALTH,
    score: 0,
    alive: true,
    lastInputSeq: 0,
    lastFireTime: 0,
    // anti-cheat
    prevX: spawn.x,
    prevY: spawn.y,
    violations: 0,
  };
}

// ─── Core reducer ────────────────────────────────────────────────────────────

/**
 * Apply a single player's input to their state for one dt step.
 *
 * Returns { player, newProjectiles, violation }.
 * `violation` is null or { reason, details }.
 */
function applyInput(player, input, now, dt) {
  if (!player.alive) return { player, newProjectiles: [], violation: null };

  const { keys = {}, fire = false, angle = 0, seq = 0 } = input;

  // Build velocity from keys
  let dx = 0;
  let dy = 0;
  if (keys.up    || keys.w) dy -= 1;
  if (keys.down  || keys.s) dy += 1;
  if (keys.left  || keys.a) dx -= 1;
  if (keys.right || keys.d) dx += 1;

  // Normalise diagonal
  const mag = Math.sqrt(dx * dx + dy * dy);
  if (mag > 0) {
    dx = (dx / mag) * CFG.PLAYER_SPEED;
    dy = (dy / mag) * CFG.PLAYER_SPEED;
  }

  const newX = clamp(player.x + dx * dt, CFG.PLAYER_RADIUS, CFG.ARENA_W - CFG.PLAYER_RADIUS);
  const newY = clamp(player.y + dy * dt, CFG.PLAYER_RADIUS, CFG.ARENA_H - CFG.PLAYER_RADIUS);

  // ── Anti-cheat: speed check ───────────────────────────────────────────────
  const moved = dist(player.x, player.y, newX, newY);
  const maxAllowed = CFG.PLAYER_SPEED * dt * CFG.SPEED_TOLERANCE;
  let violation = null;

  if (moved > maxAllowed + 0.5) {
    violation = {
      reason: 'speed_violation',
      details: `moved ${moved.toFixed(1)} px in ${(dt * 1000).toFixed(0)} ms, max ${maxAllowed.toFixed(1)}`,
    };
  }

  // ── Anti-cheat: teleport check ────────────────────────────────────────────
  const jump = dist(player.prevX, player.prevY, newX, newY);
  if (jump > CFG.TELEPORT_THRESHOLD) {
    violation = {
      reason: 'teleport',
      details: `position jumped ${jump.toFixed(1)} px (threshold ${CFG.TELEPORT_THRESHOLD})`,
    };
  }

  // Build updated player
  const updated = {
    ...player,
    x: newX,
    y: newY,
    vx: dx,
    vy: dy,
    angle,
    prevX: player.x,
    prevY: player.y,
    lastInputSeq: Math.max(player.lastInputSeq, seq),
  };

  // ── Fire projectile ───────────────────────────────────────────────────────
  const newProjectiles = [];
  if (fire && now - player.lastFireTime >= CFG.FIRE_RATE_MS) {
    // Anti-cheat: fire-rate handled by the guard above
    newProjectiles.push(createProjectile(player.id, newX, newY, angle, now));
    updated.lastFireTime = now;
  } else if (fire && now - player.lastFireTime < CFG.FIRE_RATE_MS) {
    // Silently drop; not a violation (latency can cause this legitimately)
  }

  return { player: updated, newProjectiles, violation };
}

// ─── Projectile factory ───────────────────────────────────────────────────────

function createProjectile(ownerId, x, y, angle, now) {
  return {
    id: uuidv4(),
    ownerId,
    x,
    y,
    vx: Math.cos(angle) * CFG.PROJECTILE_SPEED,
    vy: Math.sin(angle) * CFG.PROJECTILE_SPEED,
    createdAt: now,
    ttl: CFG.PROJECTILE_TTL_MS,
  };
}

// ─── World tick ──────────────────────────────────────────────────────────────

/**
 * Advance the entire world state by `dt` seconds.
 *
 * @param {Object} world   - { players: Map<id, player>, projectiles: Map<id, proj>, tick }
 * @param {Map}    inputs  - Map<playerId, latestInput>
 * @param {number} now     - current timestamp (ms)
 * @param {number} dt      - elapsed seconds since last tick
 * @returns {{ world, events, violations }}
 *   events: array of { type, ...payload } to broadcast
 *   violations: array of { playerId, reason, details }
 */
function tickWorld(world, inputs, now, dt) {
  const events = [];
  const violations = [];
  const nextPlayers = new Map(world.players);
  let nextProjectiles = new Map(world.projectiles);

  // ── Apply player inputs ───────────────────────────────────────────────────
  for (const [id, player] of nextPlayers) {
    const input = inputs.get(id) || {};
    const { player: updated, newProjectiles, violation } = applyInput(player, input, now, dt);

    nextPlayers.set(id, updated);

    for (const proj of newProjectiles) {
      nextProjectiles.set(proj.id, proj);
    }

    if (violation) {
      const p = nextPlayers.get(id);
      const newViolations = (p.violations || 0) + 1;
      nextPlayers.set(id, { ...p, violations: newViolations });
      violations.push({ playerId: id, ...violation, total: newViolations });
    }
  }

  // ── Advance projectiles ───────────────────────────────────────────────────
  const survivingProjectiles = new Map();
  for (const [pid, proj] of nextProjectiles) {
    const age = now - proj.createdAt;
    if (age >= proj.ttl) continue; // expired

    const nx = proj.x + proj.vx * dt;
    const ny = proj.y + proj.vy * dt;

    // Wall collision
    if (nx < 0 || nx > CFG.ARENA_W || ny < 0 || ny > CFG.ARENA_H) continue;

    const movedProj = { ...proj, x: nx, y: ny, ttl: proj.ttl - age + (proj.createdAt - (now - dt)) };

    // Player collision
    let hit = false;
    for (const [playerId, player] of nextPlayers) {
      if (playerId === proj.ownerId) continue;
      if (!player.alive) continue;

      const d = dist(nx, ny, player.x, player.y);
      if (d <= CFG.PLAYER_RADIUS + CFG.PROJECTILE_RADIUS) {
        hit = true;
        const newHealth = Math.max(0, player.health - CFG.PROJECTILE_DAMAGE);
        const alive = newHealth > 0;

        nextPlayers.set(playerId, { ...player, health: newHealth, alive });

        events.push({
          type: 'hit',
          targetId: playerId,
          shooterId: proj.ownerId,
          damage: CFG.PROJECTILE_DAMAGE,
          health: newHealth,
        });

        if (!alive) {
          // Credit score to shooter
          const shooter = nextPlayers.get(proj.ownerId);
          if (shooter) {
            nextPlayers.set(proj.ownerId, { ...shooter, score: shooter.score + 1 });
          }
          events.push({ type: 'killed', targetId: playerId, shooterId: proj.ownerId });
        }
        break;
      }
    }

    if (!hit) {
      survivingProjectiles.set(pid, movedProj);
    }
  }

  const nextWorld = {
    players: nextPlayers,
    projectiles: survivingProjectiles,
    tick: world.tick + 1,
  };

  return { world: nextWorld, events, violations };
}

// ─── Respawn ─────────────────────────────────────────────────────────────────

function respawnPlayer(world, playerId) {
  const player = world.players.get(playerId);
  if (!player) return { world, respawnData: null };

  const spawn = randomSpawn();
  const revived = {
    ...player,
    x: spawn.x,
    y: spawn.y,
    prevX: spawn.x,
    prevY: spawn.y,
    health: CFG.MAX_HEALTH,
    alive: true,
    vx: 0,
    vy: 0,
  };
  const nextPlayers = new Map(world.players);
  nextPlayers.set(playerId, revived);

  return {
    world: { ...world, players: nextPlayers },
    respawnData: { playerId, x: spawn.x, y: spawn.y, health: CFG.MAX_HEALTH },
  };
}

// ─── World snapshot (for broadcast) ─────────────────────────────────────────

function serializeWorld(world) {
  const players = [];
  for (const p of world.players.values()) {
    players.push({
      id:           p.id,
      x:            p.x,
      y:            p.y,
      vx:           p.vx,
      vy:           p.vy,
      angle:        p.angle,
      health:       p.health,
      score:        p.score,
      alive:        p.alive,
      lastInputSeq: p.lastInputSeq,
    });
  }

  const projectiles = [];
  for (const proj of world.projectiles.values()) {
    projectiles.push({
      id:      proj.id,
      ownerId: proj.ownerId,
      x:       proj.x,
      y:       proj.y,
      vx:      proj.vx,
      vy:      proj.vy,
    });
  }

  return { players, projectiles, tick: world.tick };
}

module.exports = {
  createPlayer,
  createProjectile,
  applyInput,
  tickWorld,
  respawnPlayer,
  serializeWorld,
  randomSpawn,
  clamp,
  dist,
};
