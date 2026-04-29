'use strict';

/**
 * Unit tests for game state reducer.
 * Uses Node.js built-in test runner (node --test).
 */

const { describe, it, before, beforeEach } = require('node:test');
const assert = require('node:assert/strict');

const {
  createPlayer,
  createProjectile,
  applyInput,
  tickWorld,
  respawnPlayer,
  serializeWorld,
  clamp,
  dist,
} = require('../gameState');

const CFG = require('../config');

// ─── Helpers ─────────────────────────────────────────────────────────────────

function makeWorld(players = [], projectiles = []) {
  const pMap = new Map();
  for (const p of players) pMap.set(p.id, p);
  const projMap = new Map();
  for (const proj of projectiles) projMap.set(proj.id, proj);
  return { players: pMap, projectiles: projMap, tick: 0 };
}

function noInput() {
  return { keys: {}, fire: false, angle: 0, seq: 0 };
}

// ─── clamp ────────────────────────────────────────────────────────────────────

describe('clamp', () => {
  it('returns value when within range', () => {
    assert.equal(clamp(5, 0, 10), 5);
  });

  it('clamps to lo', () => {
    assert.equal(clamp(-5, 0, 10), 0);
  });

  it('clamps to hi', () => {
    assert.equal(clamp(15, 0, 10), 10);
  });
});

// ─── dist ─────────────────────────────────────────────────────────────────────

describe('dist', () => {
  it('returns 0 for same point', () => {
    assert.equal(dist(3, 4, 3, 4), 0);
  });

  it('computes euclidean distance', () => {
    assert.equal(dist(0, 0, 3, 4), 5);
  });
});

// ─── createPlayer ─────────────────────────────────────────────────────────────

describe('createPlayer', () => {
  it('creates player with correct id', () => {
    const p = createPlayer('p1');
    assert.equal(p.id, 'p1');
  });

  it('starts at full health', () => {
    const p = createPlayer('p1');
    assert.equal(p.health, CFG.MAX_HEALTH);
  });

  it('starts alive', () => {
    const p = createPlayer('p1');
    assert.ok(p.alive);
  });

  it('spawns within arena bounds', () => {
    for (let i = 0; i < 50; i++) {
      const p = createPlayer(`p${i}`);
      assert.ok(p.x >= CFG.PLAYER_RADIUS && p.x <= CFG.ARENA_W - CFG.PLAYER_RADIUS,
        `x=${p.x} out of bounds`);
      assert.ok(p.y >= CFG.PLAYER_RADIUS && p.y <= CFG.ARENA_H - CFG.PLAYER_RADIUS,
        `y=${p.y} out of bounds`);
    }
  });
});

// ─── applyInput ───────────────────────────────────────────────────────────────

describe('applyInput', () => {
  let player;
  const dt   = 1 / 20;   // one server tick
  const now  = Date.now();

  beforeEach(() => {
    player = createPlayer('p1');
    player.x = 400;
    player.y = 300;
    player.prevX = 400;
    player.prevY = 300;
  });

  it('no-op when no keys pressed', () => {
    const { player: out } = applyInput(player, noInput(), now, dt);
    assert.equal(out.x, 400);
    assert.equal(out.y, 300);
  });

  it('moves right when right key held', () => {
    const input = { keys: { right: true }, fire: false, angle: 0, seq: 1 };
    const { player: out } = applyInput(player, input, now, dt);
    assert.ok(out.x > 400, `expected x > 400, got ${out.x}`);
    assert.equal(out.y, 300);
  });

  it('moves up when up key held', () => {
    const input = { keys: { up: true }, fire: false, angle: 0, seq: 1 };
    const { player: out } = applyInput(player, input, now, dt);
    assert.ok(out.y < 300, `expected y < 300, got ${out.y}`);
  });

  it('normalises diagonal movement speed', () => {
    const input = { keys: { right: true, down: true }, fire: false, angle: 0, seq: 1 };
    const { player: out } = applyInput(player, input, now, dt);
    const moved = dist(400, 300, out.x, out.y);
    const expected = CFG.PLAYER_SPEED * dt;
    assert.ok(Math.abs(moved - expected) < 0.5,
      `diagonal distance ${moved.toFixed(3)} should be ~${expected.toFixed(3)}`);
  });

  it('clamps position to arena edges', () => {
    player.x = 0;
    player.y = 0;
    const input = { keys: { up: true, left: true }, fire: false, angle: 0, seq: 1 };
    const { player: out } = applyInput(player, input, now, dt);
    assert.ok(out.x >= CFG.PLAYER_RADIUS);
    assert.ok(out.y >= CFG.PLAYER_RADIUS);
  });

  it('does nothing when player is dead', () => {
    player.alive = false;
    const input = { keys: { right: true }, fire: false, angle: 0, seq: 1 };
    const { player: out } = applyInput(player, input, now, dt);
    assert.equal(out.x, player.x);
    assert.equal(out.y, player.y);
  });

  it('updates lastInputSeq', () => {
    const input = { keys: {}, fire: false, angle: 0, seq: 42 };
    const { player: out } = applyInput(player, input, now, dt);
    assert.equal(out.lastInputSeq, 42);
  });

  it('does not decrease lastInputSeq for older seq', () => {
    player.lastInputSeq = 50;
    const input = { keys: {}, fire: false, angle: 0, seq: 10 };
    const { player: out } = applyInput(player, input, now, dt);
    assert.equal(out.lastInputSeq, 50);
  });

  it('fires a projectile', () => {
    const input = { keys: {}, fire: true, angle: 0, seq: 1 };
    const { newProjectiles } = applyInput(player, input, now, dt);
    assert.equal(newProjectiles.length, 1);
  });

  it('respects fire rate — no double-fire in same tick', () => {
    const input = { keys: {}, fire: true, angle: 0, seq: 1 };
    const { player: p1, newProjectiles: p1proj } = applyInput(player, input, now, dt);
    assert.equal(p1proj.length, 1);

    // Immediately fire again — should be rate-limited
    const { newProjectiles: p2proj } = applyInput(p1, input, now + 10, dt);
    assert.equal(p2proj.length, 0, 'should not fire before fire-rate window expires');
  });

  it('fires again after fire-rate window', () => {
    const input = { keys: {}, fire: true, angle: 0, seq: 1 };
    const { player: p1 } = applyInput(player, input, now, dt);
    const { newProjectiles } = applyInput(p1, { ...input, seq: 2 }, now + CFG.FIRE_RATE_MS + 1, dt);
    assert.equal(newProjectiles.length, 1);
  });

  it('sets projectile velocity from angle', () => {
    const angle = Math.PI / 4;
    const input = { keys: {}, fire: true, angle, seq: 1 };
    const { newProjectiles } = applyInput(player, input, now, dt);
    const proj = newProjectiles[0];
    assert.ok(Math.abs(proj.vx - Math.cos(angle) * CFG.PROJECTILE_SPEED) < 0.01);
    assert.ok(Math.abs(proj.vy - Math.sin(angle) * CFG.PROJECTILE_SPEED) < 0.01);
  });
});

// ─── Anti-cheat: speed violation ─────────────────────────────────────────────

describe('anti-cheat: speed', () => {
  it('flags speed violation when moved too far', () => {
    const player = createPlayer('cheat');
    player.x = 100;
    player.y = 100;
    player.prevX = 100;
    player.prevY = 100;

    // Build an input that would normally move them to 100,100 but we manually
    // set prevX/Y far away to simulate teleport
    player.prevX = 0;
    player.prevY = 0;
    player.x = 600; // simulate a huge position jump

    const input = { keys: { right: true }, fire: false, angle: 0, seq: 1 };
    const { violation } = applyInput(player, input, Date.now(), 1 / 20);

    assert.ok(violation !== null, 'should detect a violation');
    assert.ok(
      violation.reason === 'teleport' || violation.reason === 'speed_violation',
      `unexpected reason: ${violation?.reason}`
    );
  });

  it('does not flag normal movement', () => {
    const player = createPlayer('legit');
    player.x = 400;
    player.y = 300;
    player.prevX = 400;
    player.prevY = 300;

    const input = { keys: { right: true }, fire: false, angle: 0, seq: 1 };
    const { violation } = applyInput(player, input, Date.now(), 1 / 20);

    assert.equal(violation, null, `unexpected violation: ${violation?.reason}`);
  });
});

// ─── tickWorld ────────────────────────────────────────────────────────────────

describe('tickWorld', () => {
  it('advances tick counter', () => {
    const world = makeWorld([createPlayer('p1')]);
    const inputs = new Map();
    const { world: next } = tickWorld(world, inputs, Date.now(), 1 / 20);
    assert.equal(next.tick, 1);
  });

  it('moves a player given right input', () => {
    const p = createPlayer('p1');
    p.x = 400; p.y = 400; p.prevX = 400; p.prevY = 400;
    const world  = makeWorld([p]);
    const inputs = new Map([['p1', { keys: { right: true }, fire: false, angle: 0, seq: 1 }]]);
    const { world: next } = tickWorld(world, inputs, Date.now(), 1 / 20);
    assert.ok(next.players.get('p1').x > 400);
  });

  it('spawns a projectile when player fires', () => {
    const p = createPlayer('p1');
    p.x = 400; p.y = 400; p.prevX = 400; p.prevY = 400;
    const world  = makeWorld([p]);
    const now    = Date.now();
    const inputs = new Map([['p1', { keys: {}, fire: true, angle: 0, seq: 1 }]]);
    const { world: next } = tickWorld(world, inputs, now, 1 / 20);
    assert.equal(next.projectiles.size, 1);
  });

  it('removes projectile after hitting a player', () => {
    const shooter = createPlayer('shooter');
    shooter.x = 100; shooter.y = 100;
    shooter.prevX = 100; shooter.prevY = 100;

    const target = createPlayer('target');
    target.x = 110; target.y = 100;  // right next to projectile origin
    target.prevX = 110; target.prevY = 100;

    // Create a projectile heading right, starting at shooter pos
    const proj = createProjectile('shooter', 100, 100, 0, Date.now() - 10);

    const world  = makeWorld([shooter, target], [proj]);
    const inputs = new Map();
    const { world: next, events } = tickWorld(world, inputs, Date.now(), 1 / 20);

    const hitEvent = events.find(e => e.type === 'hit' && e.targetId === 'target');
    assert.ok(hitEvent, 'expected hit event');
    assert.equal(next.projectiles.size, 0, 'projectile should be consumed');
  });

  it('emits killed event when health reaches zero', () => {
    const shooter = createPlayer('shooter');
    shooter.x = 100; shooter.y = 100;

    const target = createPlayer('target');
    target.x = 110; target.y = 100;
    target.health = CFG.PROJECTILE_DAMAGE; // one hit remaining

    const proj = createProjectile('shooter', 100, 100, 0, Date.now() - 10);
    const world  = makeWorld([shooter, target], [proj]);
    const inputs = new Map();
    const { events } = tickWorld(world, inputs, Date.now(), 1 / 20);

    const killEvent = events.find(e => e.type === 'killed' && e.targetId === 'target');
    assert.ok(killEvent, 'expected killed event');
  });

  it('credits score to shooter on kill', () => {
    const shooter = createPlayer('shooter');
    shooter.x = 100; shooter.y = 100;

    const target = createPlayer('target');
    target.x = 110; target.y = 100;
    target.health = CFG.PROJECTILE_DAMAGE;

    const proj = createProjectile('shooter', 100, 100, 0, Date.now() - 10);
    const world  = makeWorld([shooter, target], [proj]);
    const { world: next } = tickWorld(world, new Map(), Date.now(), 1 / 20);

    assert.equal(next.players.get('shooter').score, 1);
  });

  it('expires projectile past TTL', () => {
    const p = createPlayer('p1');
    // Old projectile, well past its TTL
    const proj = createProjectile('p1', 400, 400, 0, Date.now() - CFG.PROJECTILE_TTL_MS - 100);
    const world  = makeWorld([p], [proj]);
    const { world: next } = tickWorld(world, new Map(), Date.now(), 1 / 20);
    assert.equal(next.projectiles.size, 0);
  });

  it('removes projectile that exits arena walls', () => {
    const p = createPlayer('p1');
    // Projectile heading left from x=5 will exit arena
    const proj = createProjectile('p1', 5, 400, Math.PI, Date.now() - 5);
    const world  = makeWorld([p], [proj]);
    const { world: next } = tickWorld(world, new Map(), Date.now(), 1 / 20);
    assert.equal(next.projectiles.size, 0);
  });

  it('does not hit own shooter', () => {
    const p = createPlayer('p1');
    p.x = 100; p.y = 100;
    // Projectile at shooter's own position heading right
    const proj = createProjectile('p1', 100, 100, 0, Date.now() - 5);
    const world  = makeWorld([p], [proj]);
    const { events } = tickWorld(world, new Map(), Date.now(), 1 / 20);
    const hitEvent = events.find(e => e.type === 'hit' && e.targetId === 'p1');
    assert.equal(hitEvent, undefined, 'shooter should not be hit by own projectile');
  });
});

// ─── respawnPlayer ────────────────────────────────────────────────────────────

describe('respawnPlayer', () => {
  it('restores health and alive flag', () => {
    const p = createPlayer('p1');
    p.health = 0;
    p.alive  = false;
    const world = makeWorld([p]);

    const { world: next, respawnData } = respawnPlayer(world, 'p1');
    const revived = next.players.get('p1');

    assert.ok(revived.alive);
    assert.equal(revived.health, CFG.MAX_HEALTH);
    assert.ok(respawnData !== null);
  });

  it('returns null respawnData for unknown id', () => {
    const world = makeWorld([]);
    const { respawnData } = respawnPlayer(world, 'unknown');
    assert.equal(respawnData, null);
  });

  it('places player within arena', () => {
    const p = createPlayer('p1');
    p.alive = false;
    const world = makeWorld([p]);
    for (let i = 0; i < 20; i++) {
      const { world: next } = respawnPlayer(world, 'p1');
      const r = next.players.get('p1');
      assert.ok(r.x >= CFG.PLAYER_RADIUS && r.x <= CFG.ARENA_W - CFG.PLAYER_RADIUS);
      assert.ok(r.y >= CFG.PLAYER_RADIUS && r.y <= CFG.ARENA_H - CFG.PLAYER_RADIUS);
    }
  });
});

// ─── serializeWorld ───────────────────────────────────────────────────────────

describe('serializeWorld', () => {
  it('returns arrays for players and projectiles', () => {
    const p1 = createPlayer('p1');
    const proj = createProjectile('p1', 400, 400, 0, Date.now());
    const world = makeWorld([p1], [proj]);
    const snap  = serializeWorld(world);

    assert.ok(Array.isArray(snap.players));
    assert.ok(Array.isArray(snap.projectiles));
    assert.equal(snap.players.length, 1);
    assert.equal(snap.projectiles.length, 1);
  });

  it('does not expose internal fields (violations, prevX)', () => {
    const p1 = createPlayer('p1');
    const world = makeWorld([p1]);
    const snap  = serializeWorld(world);
    const pSnap = snap.players[0];

    assert.equal(pSnap.violations, undefined);
    assert.equal(pSnap.prevX, undefined);
    assert.equal(pSnap.lastFireTime, undefined);
  });

  it('propagates tick', () => {
    const world = { players: new Map(), projectiles: new Map(), tick: 42 };
    assert.equal(serializeWorld(world).tick, 42);
  });
});
