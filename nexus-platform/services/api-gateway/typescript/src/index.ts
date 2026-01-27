// =============================================================================
// NEXUS PLATFORM - API GATEWAY - TYPESCRIPT IMPLEMENTATION
// =============================================================================
// Production-grade API Gateway server entry point.
// =============================================================================

import { createServer } from './server';
import { config } from './config';
import { logger } from './utils/logger';
import { initTracing } from './utils/tracing';
import { initMetrics } from './utils/metrics';

/**
 * Main entry point for the API Gateway.
 * 
 * Initializes all components and starts the HTTP server.
 */
async function main(): Promise<void> {
  logger.info({
    service: config.serviceName,
    version: config.serviceVersion,
    environment: config.environment,
    nodeVersion: process.version,
  }, 'Starting Nexus Platform API Gateway');

  try {
    // Initialize tracing
    if (config.tracing.enabled) {
      await initTracing({
        serviceName: config.serviceName,
        jaegerHost: config.tracing.jaegerHost,
        jaegerPort: config.tracing.jaegerPort,
        samplingRate: config.tracing.samplingRate,
      });
      logger.info('Distributed tracing initialized');
    }

    // Initialize metrics
    if (config.metrics.enabled) {
      initMetrics(config.metrics.prefix);
      logger.info('Prometheus metrics initialized');
    }

    // Create and start server
    const server = await createServer();
    const address = `${config.server.host}:${config.server.port}`;

    server.listen(config.server.port, config.server.host, () => {
      logger.info({ address }, 'API Gateway listening');
    });

    // Graceful shutdown handlers
    const shutdown = async (signal: string): Promise<void> => {
      logger.info({ signal }, 'Received shutdown signal');

      // Stop accepting new connections
      server.close((err) => {
        if (err) {
          logger.error({ err }, 'Error closing server');
          process.exit(1);
        }
        logger.info('Server closed');
      });

      // Wait for existing connections with timeout
      const timeout = config.server.gracefulShutdownTimeout * 1000;
      const forceExit = setTimeout(() => {
        logger.warn('Graceful shutdown timeout, forcing exit');
        process.exit(1);
      }, timeout);

      try {
        // Add cleanup tasks here (close Redis, etc.)
        clearTimeout(forceExit);
        logger.info('Graceful shutdown complete');
        process.exit(0);
      } catch (error) {
        logger.error({ error }, 'Error during shutdown');
        process.exit(1);
      }
    };

    process.on('SIGTERM', () => shutdown('SIGTERM'));
    process.on('SIGINT', () => shutdown('SIGINT'));

    // Handle uncaught exceptions
    process.on('uncaughtException', (error) => {
      logger.fatal({ error }, 'Uncaught exception');
      process.exit(1);
    });

    process.on('unhandledRejection', (reason, promise) => {
      logger.fatal({ reason, promise }, 'Unhandled rejection');
      process.exit(1);
    });

  } catch (error) {
    logger.fatal({ error }, 'Failed to start API Gateway');
    process.exit(1);
  }
}

// Start the application
main();
