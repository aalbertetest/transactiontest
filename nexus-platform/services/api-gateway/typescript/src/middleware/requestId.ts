// =============================================================================
// NEXUS PLATFORM - API GATEWAY - REQUEST ID MIDDLEWARE
// =============================================================================
// Generates and propagates unique request IDs.
// =============================================================================

import { Request, Response, NextFunction } from 'express';
import { v4 as uuidv4 } from 'uuid';

/**
 * Extended request type with request ID
 */
declare global {
  namespace Express {
    interface Request {
      requestId: string;
      correlationId: string;
      startTime: number;
    }
  }
}

/**
 * Request ID middleware.
 * 
 * Generates a unique request ID for each incoming request and adds it to
 * both the request object and response headers.
 */
export function requestIdMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Get or generate request ID
  const requestId = req.headers['x-request-id'] as string || `req_${uuidv4().replace(/-/g, '')}`;
  
  // Get or generate correlation ID
  const correlationId = req.headers['x-correlation-id'] as string || requestId;
  
  // Add to request
  req.requestId = requestId;
  req.correlationId = correlationId;
  req.startTime = Date.now();
  
  // Add to response headers
  res.setHeader('X-Request-ID', requestId);
  res.setHeader('X-Correlation-ID', correlationId);
  
  next();
}
