// =============================================================================
// NEXUS PLATFORM - API GATEWAY - ADMIN ROUTES
// =============================================================================
// Administrative endpoints for gateway management.
// =============================================================================

import { Router, Request, Response } from 'express';
import { requireRole } from '../middleware/authentication';
import { getCircuitBreakerStates, resetCircuitBreaker } from '../middleware/circuitBreaker';
import { config } from '../config';

export const adminRouter = Router();

// Require admin role for all admin routes
adminRouter.use(requireRole('admin'));

/**
 * Get gateway statistics
 */
adminRouter.get('/stats', (_req: Request, res: Response) => {
  const uptime = process.uptime();
  const memoryUsage = process.memoryUsage();

  res.json({
    uptime_seconds: uptime,
    memory: {
      heapUsed: memoryUsage.heapUsed,
      heapTotal: memoryUsage.heapTotal,
      rss: memoryUsage.rss,
    },
    environment: config.environment,
    version: config.serviceVersion,
    nodeVersion: process.version,
  });
});

/**
 * Get circuit breaker states
 */
adminRouter.get('/circuit-breakers', (_req: Request, res: Response) => {
  const states = getCircuitBreakerStates();
  res.json({
    circuit_breakers: Object.entries(states).map(([name, info]) => ({
      service: name,
      state: info.state,
      stats: info.stats,
    })),
  });
});

/**
 * Reset circuit breaker
 */
adminRouter.post('/circuit-breakers/reset', (req: Request, res: Response) => {
  const { service } = req.body as { service?: string };
  
  resetCircuitBreaker(service);

  res.json({
    success: true,
    message: `Circuit breaker(s) reset: ${service || 'all'}`,
  });
});

/**
 * Get configuration (non-sensitive)
 */
adminRouter.get('/config', (_req: Request, res: Response) => {
  res.json({
    environment: config.environment,
    service_name: config.serviceName,
    service_version: config.serviceVersion,
    rate_limiting_enabled: config.rateLimit.enabled,
    circuit_breaker_enabled: config.circuitBreaker.enabled,
    tracing_enabled: config.tracing.enabled,
    cache_enabled: config.cache.enabled,
    metrics_enabled: config.metrics.enabled,
  });
});

/**
 * Clear cache
 */
adminRouter.post('/cache/clear', async (req: Request, res: Response) => {
  // In production, this would clear Redis cache
  res.json({
    success: true,
    message: 'Cache cleared',
  });
});

/**
 * List registered services
 */
adminRouter.get('/services', (_req: Request, res: Response) => {
  const services = Object.entries(config.backend.services).map(([name, url]) => ({
    name,
    endpoint: url,
    healthy: true, // Would check actual health
  }));

  res.json({
    services,
  });
});
