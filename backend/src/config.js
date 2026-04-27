export function loadConfig(env = process.env) {
  const jwtSecret = env.JWT_SECRET;
  if (!jwtSecret || jwtSecret.length < 32) {
    throw new Error(
      'JWT_SECRET must be set and at least 32 characters. ' +
        'Generate one with: node -e "console.log(require(\'crypto\').randomBytes(32).toString(\'hex\'))"',
    );
  }
  return {
    jwtSecret,
    port: Number(env.PORT ?? 3000),
    dbPath: env.DB_PATH ?? './data/app.db',
    bcryptCost: Number(env.BCRYPT_COST ?? 12),
    accessTtl: env.ACCESS_TTL ?? '15m',
    refreshTtlMs: Number(env.REFRESH_TTL_MS ?? 1000 * 60 * 60 * 24 * 30),
  };
}
