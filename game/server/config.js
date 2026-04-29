'use strict';

const CONFIG = {
  PORT: parseInt(process.env.PORT || '8080', 10),

  // Arena dimensions (px)
  ARENA_W: 1200,
  ARENA_H: 800,

  // Player physics
  PLAYER_SPEED: 200,       // px/s
  PLAYER_RADIUS: 16,
  MAX_HEALTH: 100,
  RESPAWN_DELAY_MS: 3000,

  // Projectile physics
  PROJECTILE_SPEED: 450,   // px/s
  PROJECTILE_RADIUS: 5,
  PROJECTILE_TTL_MS: 2000,
  PROJECTILE_DAMAGE: 20,
  FIRE_RATE_MS: 250,       // min ms between shots

  // Server tick
  TICK_RATE_HZ: 20,
  get TICK_MS() { return 1000 / this.TICK_RATE_HZ; },

  // Anti-cheat tolerances
  SPEED_TOLERANCE: 1.20,   // allow 20% over nominal to absorb network jitter
  TELEPORT_THRESHOLD: 400, // px — any jump larger than this is suspicious
  MAX_VIOLATIONS: 5,       // disconnect after this many
};

module.exports = CONFIG;
