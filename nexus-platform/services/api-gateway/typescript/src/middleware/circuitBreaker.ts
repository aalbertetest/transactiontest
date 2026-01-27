// =============================================================================
// NEXUS PLATFORM - API GATEWAY - CIRCUIT BREAKER MIDDLEWARE
// =============================================================================
// Circuit breaker pattern implementation using opossum.
// =============================================================================

import { Request, Response, NextFunction } from 'express';
import CircuitBreaker from 'opossum';
import { config } from '../config';
import { logger } from '../utils/logger';

/**
 * Circuit breaker registry
 */
const circuitBreakers: Map<string, CircuitBreaker<[Request, Response, NextFunction], void>> = new Map();

/**
 * Circuit breaker options
 */
const circuitBreakerOptions: CircuitBreaker.Options = {
  timeout: config.circuitBreaker.timeout,
  errorThresholdPercentage: 50,
  resetTimeout: config.circuitBreaker.resetTimeout,
  volumeThreshold: config.circuitBreaker.failureThreshold,
};

/**
 * Get or create circuit breaker for a service
 */
function getCircuitBreaker(serviceName: string): CircuitBreaker<[Request, Response, NextFunction], void> {
  if (!circuitBreakers.has(serviceName)) {
    // Create a pass-through function
    const passThrough = async (
      _req: Request,
      _res: Response,
      next: NextFunction
    ): Promise<void> => {
      return new Promise((resolve) => {
        next();
        resolve();
      });
    };

    const cb = new CircuitBreaker(passThrough, {
      ...circuitBreakerOptions,
      name: serviceName,
    });

    // Event listeners
    cb.on('open', () => {
      logger.warn({ service: serviceName }, 'Circuit breaker opened');
    });

    cb.on('halfOpen', () => {
      logger.info({ service: serviceName }, 'Circuit breaker half-open');
    });

    cb.on('close', () => {
      logger.info({ service: serviceName }, 'Circuit breaker closed');
    });

    cb.on('fallback', () => {
      logger.warn({ service: serviceName }, 'Circuit breaker fallback triggered');
    });

    circuitBreakers.set(serviceName, cb);
  }

  return circuitBreakers.get(serviceName)!;
}

/**
 * Get all circuit breaker states
 */
export function getCircuitBreakerStates(): Record<string, { state: string; stats: CircuitBreaker.Stats }> {
  const states: Record<string, { state: string; stats: CircuitBreaker.Stats }> = {};

  for (const [name, cb] of circuitBreakers) {
    let state: string;
    if (cb.opened) {
      state = 'open';
    } else if (cb.halfOpen) {
      state = 'half_open';
    } else {
      state = 'closed';
    }

    states[name] = {
      state,
      stats: cb.stats,
    };
  }

  return states;
}

/**
 * Reset circuit breaker for a service
 */
export function resetCircuitBreaker(serviceName?: string): void {
  if (serviceName) {
    const cb = circuitBreakers.get(serviceName);
    if (cb) {
      cb.close();
      logger.info({ service: serviceName }, 'Circuit breaker reset');
    }
  } else {
    for (const [name, cb] of circuitBreakers) {
      cb.close();
      logger.info({ service: name }, 'Circuit breaker reset');
    }
  }
}

/**
 * Circuit breaker middleware factory.
 * 
 * Creates a middleware that wraps requests with circuit breaker protection.
 */
export function circuitBreakerMiddleware(serviceName: string) {
  return async (req: Request, res: Response, next: NextFunction): Promise<void> => {
    const cb = getCircuitBreaker(serviceName);

    try {
      await cb.fire(req, res, next);
    } catch (error) {
      // Circuit breaker is open
      logger.error({
        service: serviceName,
        requestId: req.requestId,
        error: (error as Error).message,
      }, 'Circuit breaker rejected request');

      res.status(503).json({
        error: {
          code: 'SERVICE_UNAVAILABLE',
          message: `Service '${serviceName}' is temporarily unavailable`,
          requestId: req.requestId,
          retryAfter: Math.ceil(config.circuitBreaker.resetTimeout / 1000),
        },
      });
    }
  };
}
