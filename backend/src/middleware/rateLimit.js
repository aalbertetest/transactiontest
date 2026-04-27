/**
 * In-process rate limiter. Sliding-ish fixed window per key.
 *
 * For multi-node deployments swap this for a Redis-backed limiter
 * (`INCR key` + `EXPIRE key windowSeconds`), which is the next item on the
 * scaling todo list in SIMULATION.md.
 */
export function rateLimit({ key, max, windowMs }) {
  const buckets = new Map();
  return function rateLimitMw(req, res, next) {
    const k = key(req);
    const now = Date.now();
    const bucket = buckets.get(k);
    if (!bucket || now - bucket.start > windowMs) {
      buckets.set(k, { start: now, count: 1 });
      return next();
    }
    bucket.count += 1;
    if (bucket.count > max) {
      const retryAfter = Math.ceil((windowMs - (now - bucket.start)) / 1000);
      res.set('Retry-After', String(retryAfter));
      return res.status(429).json({ error: 'rate_limited' });
    }
    next();
  };
}
