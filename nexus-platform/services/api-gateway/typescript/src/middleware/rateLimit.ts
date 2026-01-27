// =============================================================================
// NEXUS PLATFORM - API GATEWAY - RATE LIMITING MIDDLEWARE
// =============================================================================
// Express rate limiting using express-rate-limit.
// =============================================================================

import rateLimit from 'express-rate-limit';
import { config } from '../config';
import { logger } from '../utils/logger';

/**
 * Rate limiter middleware.
 * 
 * Limits requests per IP address within a time window.
 */
export const rateLimitMiddleware = rateLimit({
  windowMs: config.rateLimit.windowMs,
  max: config.rateLimit.maxRequests,
  standardHeaders: true,
  legacyHeaders: false,
  
  // Custom key generator (use user ID if authenticated, else IP)
  keyGenerator: (req) => {
    if (req.user?.id) {
      return `user:${req.user.id}`;
    }
    return `ip:${req.ip}`;
  },
  
  // Skip rate limiting for certain paths
  skip: (req) => {
    const skipPaths = ['/health', '/ready', '/live', '/metrics'];
    return skipPaths.includes(req.path);
  },
  
  // Custom handler for rate limit exceeded
  handler: (req, res) => {
    logger.warn({
      requestId: req.requestId,
      ip: req.ip,
      userId: req.user?.id,
      path: req.path,
    }, 'Rate limit exceeded');

    res.status(429).json({
      error: {
        code: 'RATE_LIMIT_EXCEEDED',
        message: 'Too many requests, please try again later',
        requestId: req.requestId,
        retryAfter: Math.ceil(config.rateLimit.windowMs / 1000),
      },
    });
  },
  
  // Custom message
  message: {
    error: {
      code: 'RATE_LIMIT_EXCEEDED',
      message: 'Too many requests, please try again later',
    },
  },
});
