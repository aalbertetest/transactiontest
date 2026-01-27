// =============================================================================
// NEXUS PLATFORM - API GATEWAY - LOGGING MIDDLEWARE
// =============================================================================
// Request/response logging middleware.
// =============================================================================

import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';

/**
 * Logging middleware.
 * 
 * Logs all HTTP requests with timing and response information.
 */
export function loggingMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  const startTime = req.startTime || Date.now();

  // Capture original end method
  const originalEnd = res.end;
  let responseBody: unknown;

  // Override end to capture response
  res.end = function (chunk?: unknown, ...args: unknown[]): Response {
    if (chunk) {
      responseBody = chunk;
    }

    const duration = Date.now() - startTime;
    const logData = {
      requestId: req.requestId,
      correlationId: req.correlationId,
      method: req.method,
      path: req.path,
      query: Object.keys(req.query).length > 0 ? req.query : undefined,
      statusCode: res.statusCode,
      duration,
      userAgent: req.get('user-agent'),
      ip: req.ip,
      userId: req.user?.id,
      contentLength: res.get('content-length'),
    };

    // Choose log level based on status code
    if (res.statusCode >= 500) {
      logger.error(logData, 'HTTP request completed with server error');
    } else if (res.statusCode >= 400) {
      logger.warn(logData, 'HTTP request completed with client error');
    } else {
      logger.info(logData, 'HTTP request completed');
    }

    // Call original end
    return originalEnd.call(this, chunk, ...args);
  } as typeof res.end;

  next();
}
