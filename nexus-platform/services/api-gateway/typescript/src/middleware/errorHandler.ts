// =============================================================================
// NEXUS PLATFORM - API GATEWAY - ERROR HANDLER MIDDLEWARE
// =============================================================================
// Centralized error handling middleware.
// =============================================================================

import { Request, Response, NextFunction } from 'express';
import { logger } from '../utils/logger';
import { config, isProduction } from '../config';

/**
 * API Error class for structured errors.
 */
export class ApiError extends Error {
  public readonly statusCode: number;
  public readonly code: string;
  public readonly details?: Record<string, unknown>;

  constructor(
    statusCode: number,
    code: string,
    message: string,
    details?: Record<string, unknown>
  ) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
    this.details = details;
    this.name = 'ApiError';

    // Maintain proper stack trace
    Error.captureStackTrace(this, this.constructor);
  }
}

/**
 * Not found handler.
 * 
 * Handles requests to non-existent routes.
 */
export function notFoundHandler(
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  res.status(404).json({
    error: {
      code: 'NOT_FOUND',
      message: `Resource not found: ${req.method} ${req.path}`,
      requestId: req.requestId,
      timestamp: new Date().toISOString(),
    },
  });
}

/**
 * Global error handler.
 * 
 * Catches all errors and returns a structured error response.
 */
export function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  _next: NextFunction
): void {
  // Log the error
  logger.error({
    error: err.message,
    stack: err.stack,
    requestId: req.requestId,
    method: req.method,
    path: req.path,
    userId: req.user?.id,
  }, 'Request error');

  // Handle API errors
  if (err instanceof ApiError) {
    res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
        requestId: req.requestId,
        timestamp: new Date().toISOString(),
      },
    });
    return;
  }

  // Handle validation errors
  if (err.name === 'ValidationError' || err.name === 'ZodError') {
    res.status(400).json({
      error: {
        code: 'VALIDATION_ERROR',
        message: err.message,
        requestId: req.requestId,
        timestamp: new Date().toISOString(),
      },
    });
    return;
  }

  // Handle JSON syntax errors
  if (err instanceof SyntaxError && 'body' in err) {
    res.status(400).json({
      error: {
        code: 'INVALID_JSON',
        message: 'Invalid JSON in request body',
        requestId: req.requestId,
        timestamp: new Date().toISOString(),
      },
    });
    return;
  }

  // Handle timeout errors
  if (err.name === 'TimeoutError' || err.message.includes('timeout')) {
    res.status(504).json({
      error: {
        code: 'GATEWAY_TIMEOUT',
        message: 'Request timed out',
        requestId: req.requestId,
        timestamp: new Date().toISOString(),
      },
    });
    return;
  }

  // Generic internal server error
  const message = isProduction()
    ? 'An internal error occurred. Please try again later.'
    : err.message;

  const details = isProduction()
    ? undefined
    : { stack: err.stack };

  res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message,
      details,
      requestId: req.requestId,
      timestamp: new Date().toISOString(),
    },
  });
}
