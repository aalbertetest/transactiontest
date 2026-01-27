// =============================================================================
// NEXUS PLATFORM - API GATEWAY - EXPRESS SERVER
// =============================================================================
// Express server setup with middleware and routing configuration.
// =============================================================================

import express, { Express, Request, Response, NextFunction } from 'express';
import cors from 'cors';
import helmet from 'helmet';
import compression from 'compression';
import { createProxyMiddleware } from 'http-proxy-middleware';

import { config } from './config';
import { logger } from './utils/logger';
import { requestIdMiddleware } from './middleware/requestId';
import { loggingMiddleware } from './middleware/logging';
import { authenticationMiddleware } from './middleware/authentication';
import { rateLimitMiddleware } from './middleware/rateLimit';
import { circuitBreakerMiddleware } from './middleware/circuitBreaker';
import { metricsMiddleware, metricsHandler } from './middleware/metrics';
import { errorHandler, notFoundHandler } from './middleware/errorHandler';
import { healthRouter } from './routes/health';
import { adminRouter } from './routes/admin';

/**
 * Service route configuration
 */
const SERVICE_ROUTES: Record<string, string> = {
  '/auth': 'auth-service',
  '/users': 'user-service',
  '/payments': 'payment-service',
  '/workflows': 'workflow-engine',
  '/queue': 'distributed-queue',
  '/stream': 'streaming-platform',
  '/cache': 'cache-layer',
  '/scheduler': 'scheduler-service',
  '/workers': 'worker-fleet',
};

/**
 * Creates and configures the Express application.
 */
export async function createServer(): Promise<Express> {
  const app = express();

  // Trust proxy (for X-Forwarded-* headers)
  app.set('trust proxy', true);

  // ==========================================================================
  // GLOBAL MIDDLEWARE
  // ==========================================================================

  // Request ID generation
  app.use(requestIdMiddleware);

  // Security headers
  app.use(helmet({
    contentSecurityPolicy: false, // Disable for API gateway
  }));

  // CORS
  if (config.server.cors.enabled) {
    app.use(cors({
      origin: config.server.cors.origins,
      methods: config.server.cors.methods,
      allowedHeaders: config.server.cors.headers,
      credentials: config.server.cors.credentials,
      maxAge: 600,
    }));
  }

  // Response compression
  app.use(compression());

  // Body parsing
  app.use(express.json({ limit: config.server.maxRequestSize }));
  app.use(express.urlencoded({ extended: true, limit: config.server.maxRequestSize }));

  // Request logging
  if (config.logging.logRequests) {
    app.use(loggingMiddleware);
  }

  // Metrics collection
  if (config.metrics.enabled) {
    app.use(metricsMiddleware);
  }

  // ==========================================================================
  // HEALTH CHECK ROUTES (unauthenticated)
  // ==========================================================================

  app.use('/', healthRouter);

  // Metrics endpoint
  if (config.metrics.enabled) {
    app.get(config.metrics.endpoint, metricsHandler);
  }

  // ==========================================================================
  // RATE LIMITING
  // ==========================================================================

  if (config.rateLimit.enabled) {
    app.use(rateLimitMiddleware);
  }

  // ==========================================================================
  // AUTHENTICATION
  // ==========================================================================

  app.use(authenticationMiddleware);

  // ==========================================================================
  // ADMIN ROUTES
  // ==========================================================================

  app.use('/admin', adminRouter);

  // ==========================================================================
  // PROXY ROUTES
  // ==========================================================================

  // Setup proxy for each service
  for (const [pathPrefix, serviceName] of Object.entries(SERVICE_ROUTES)) {
    const targetUrl = config.backend.services[serviceName as keyof typeof config.backend.services];
    
    if (!targetUrl) {
      logger.warn({ serviceName, pathPrefix }, 'No URL configured for service');
      continue;
    }

    // Apply circuit breaker
    if (config.circuitBreaker.enabled) {
      app.use(pathPrefix, circuitBreakerMiddleware(serviceName));
    }

    // Setup proxy middleware
    app.use(pathPrefix, createProxyMiddleware({
      target: targetUrl,
      changeOrigin: true,
      pathRewrite: {
        [`^${pathPrefix}`]: '', // Remove prefix
      },
      timeout: config.backend.requestTimeout,
      proxyTimeout: config.backend.requestTimeout,
      onProxyReq: (proxyReq, req) => {
        // Add gateway headers
        const requestId = (req as Request & { requestId?: string }).requestId;
        if (requestId) {
          proxyReq.setHeader('X-Gateway-Request-Id', requestId);
        }

        // Add user info if authenticated
        const user = (req as Request & { user?: { id: string; tenantId?: string; roles?: string[] } }).user;
        if (user) {
          proxyReq.setHeader('X-User-Id', user.id);
          if (user.tenantId) {
            proxyReq.setHeader('X-Tenant-Id', user.tenantId);
          }
          if (user.roles && user.roles.length > 0) {
            proxyReq.setHeader('X-User-Roles', user.roles.join(','));
          }
        }

        // Forward client IP
        const clientIp = req.ip || req.socket.remoteAddress;
        if (clientIp) {
          proxyReq.setHeader('X-Forwarded-For', clientIp);
        }
      },
      onProxyRes: (proxyRes, req, res) => {
        // Add response headers
        const requestId = (req as Request & { requestId?: string }).requestId;
        if (requestId) {
          res.setHeader('X-Gateway-Request-Id', requestId);
        }
        res.setHeader('X-Upstream-Service', serviceName);
      },
      onError: (err, req, res) => {
        logger.error({
          error: err.message,
          service: serviceName,
          path: req.url,
          requestId: (req as Request & { requestId?: string }).requestId,
        }, 'Proxy error');

        if (!res.headersSent) {
          res.status(502).json({
            error: {
              code: 'BAD_GATEWAY',
              message: `Failed to connect to ${serviceName}`,
              requestId: (req as Request & { requestId?: string }).requestId,
            },
          });
        }
      },
      logLevel: 'warn',
      logProvider: () => ({
        log: (msg: string) => logger.debug(msg),
        debug: (msg: string) => logger.debug(msg),
        info: (msg: string) => logger.info(msg),
        warn: (msg: string) => logger.warn(msg),
        error: (msg: string) => logger.error(msg),
      }),
    }));

    logger.info({ pathPrefix, targetUrl, serviceName }, 'Proxy route configured');
  }

  // ==========================================================================
  // ERROR HANDLING
  // ==========================================================================

  // 404 handler
  app.use(notFoundHandler);

  // Global error handler
  app.use(errorHandler);

  return app;
}
