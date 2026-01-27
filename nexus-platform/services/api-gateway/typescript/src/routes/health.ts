// =============================================================================
// NEXUS PLATFORM - API GATEWAY - HEALTH ROUTES
// =============================================================================
// Health check endpoints for Kubernetes probes.
// =============================================================================

import { Router, Request, Response } from 'express';
import { config } from '../config';

export const healthRouter = Router();

/**
 * Root endpoint
 */
healthRouter.get('/', (_req: Request, res: Response) => {
  res.json({
    service: config.serviceName,
    version: config.serviceVersion,
    environment: config.environment,
    status: 'operational',
    timestamp: new Date().toISOString(),
  });
});

/**
 * Health check endpoint
 */
healthRouter.get('/health', (_req: Request, res: Response) => {
  // In production, check dependencies here
  const startTime = process.uptime();

  res.json({
    status: 'healthy',
    service: config.serviceName,
    version: config.serviceVersion,
    uptime_seconds: startTime,
    timestamp: new Date().toISOString(),
    checks: {
      self: true,
    },
  });
});

/**
 * Readiness probe endpoint
 */
healthRouter.get('/ready', (_req: Request, res: Response) => {
  // Check if service is ready to accept traffic
  res.json({
    ready: true,
    message: 'Service is ready',
  });
});

/**
 * Liveness probe endpoint
 */
healthRouter.get('/live', (_req: Request, res: Response) => {
  // Simple liveness check
  res.json({
    alive: true,
    message: 'Service is alive',
  });
});
