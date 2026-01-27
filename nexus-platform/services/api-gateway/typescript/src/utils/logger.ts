// =============================================================================
// NEXUS PLATFORM - API GATEWAY - LOGGER
// =============================================================================
// Structured logging using pino.
// =============================================================================

import pino from 'pino';
import { config } from '../config';

/**
 * Logger configuration
 */
const loggerConfig: pino.LoggerOptions = {
  level: config.logging.level,
  base: {
    service: config.serviceName,
    version: config.serviceVersion,
    environment: config.environment,
    instanceId: config.instanceId,
  },
  timestamp: pino.stdTimeFunctions.isoTime,
};

// Use pretty printing in development
if (config.logging.format === 'pretty' || config.environment === 'development') {
  loggerConfig.transport = {
    target: 'pino-pretty',
    options: {
      colorize: true,
      translateTime: 'SYS:standard',
      ignore: 'pid,hostname',
    },
  };
}

/**
 * Application logger instance
 */
export const logger = pino(loggerConfig);

/**
 * Create a child logger with additional context
 */
export function createChildLogger(context: Record<string, unknown>): pino.Logger {
  return logger.child(context);
}

/**
 * Create a request-scoped logger
 */
export function createRequestLogger(
  requestId: string,
  userId?: string
): pino.Logger {
  return logger.child({
    requestId,
    userId,
  });
}
