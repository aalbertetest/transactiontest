// =============================================================================
// NEXUS PLATFORM - API GATEWAY - METRICS MIDDLEWARE
// =============================================================================
// Prometheus metrics collection middleware.
// =============================================================================

import { Request, Response, NextFunction } from 'express';
import client from 'prom-client';
import { config } from '../config';

// Initialize metrics
const register = new client.Registry();

// Add default metrics
client.collectDefaultMetrics({ register });

// Custom metrics
const httpRequestsTotal = new client.Counter({
  name: `${config.metrics.prefix}_http_requests_total`,
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'path', 'status'],
  registers: [register],
});

const httpRequestDuration = new client.Histogram({
  name: `${config.metrics.prefix}_http_request_duration_seconds`,
  help: 'HTTP request duration in seconds',
  labelNames: ['method', 'path', 'status'],
  buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
  registers: [register],
});

const httpRequestSize = new client.Histogram({
  name: `${config.metrics.prefix}_http_request_size_bytes`,
  help: 'HTTP request size in bytes',
  labelNames: ['method', 'path'],
  buckets: [100, 1000, 10000, 100000, 1000000],
  registers: [register],
});

const httpResponseSize = new client.Histogram({
  name: `${config.metrics.prefix}_http_response_size_bytes`,
  help: 'HTTP response size in bytes',
  labelNames: ['method', 'path', 'status'],
  buckets: [100, 1000, 10000, 100000, 1000000],
  registers: [register],
});

const activeRequests = new client.Gauge({
  name: `${config.metrics.prefix}_active_requests`,
  help: 'Number of active requests',
  labelNames: ['method'],
  registers: [register],
});

const upstreamRequestDuration = new client.Histogram({
  name: `${config.metrics.prefix}_upstream_duration_seconds`,
  help: 'Upstream service request duration in seconds',
  labelNames: ['service', 'method', 'status'],
  buckets: [0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10, 30],
  registers: [register],
});

const circuitBreakerState = new client.Gauge({
  name: `${config.metrics.prefix}_circuit_breaker_state`,
  help: 'Circuit breaker state (0=closed, 1=half-open, 2=open)',
  labelNames: ['service'],
  registers: [register],
});

const rateLimitHits = new client.Counter({
  name: `${config.metrics.prefix}_rate_limit_hits_total`,
  help: 'Total number of rate limit hits',
  labelNames: ['policy', 'method', 'path'],
  registers: [register],
});

/**
 * Normalize path for metrics labels.
 * Replaces dynamic segments with placeholders.
 */
function normalizePath(path: string): string {
  return path
    // Replace UUIDs
    .replace(/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/gi, '{id}')
    // Replace numeric IDs
    .replace(/\/\d+/g, '/{id}')
    // Replace long hex strings
    .replace(/\/[0-9a-f]{16,}/gi, '/{token}');
}

/**
 * Metrics middleware.
 * 
 * Collects metrics for all HTTP requests.
 */
export function metricsMiddleware(
  req: Request,
  res: Response,
  next: NextFunction
): void {
  // Skip metrics endpoint
  if (req.path === config.metrics.endpoint) {
    return next();
  }

  const startTime = Date.now();
  const method = req.method;
  const path = normalizePath(req.path);

  // Increment active requests
  activeRequests.labels(method).inc();

  // Record request size
  const contentLength = parseInt(req.get('content-length') || '0', 10);
  if (contentLength > 0) {
    httpRequestSize.labels(method, path).observe(contentLength);
  }

  // Capture response end
  const originalEnd = res.end;
  res.end = function (chunk?: unknown, ...args: unknown[]): Response {
    // Calculate duration
    const duration = (Date.now() - startTime) / 1000;
    const status = res.statusCode.toString();

    // Record metrics
    httpRequestsTotal.labels(method, path, status).inc();
    httpRequestDuration.labels(method, path, status).observe(duration);

    // Record response size
    const responseLength = parseInt(res.get('content-length') || '0', 10);
    if (responseLength > 0) {
      httpResponseSize.labels(method, path, status).observe(responseLength);
    }

    // Decrement active requests
    activeRequests.labels(method).dec();

    return originalEnd.call(this, chunk, ...args);
  } as typeof res.end;

  next();
}

/**
 * Metrics endpoint handler.
 */
export async function metricsHandler(req: Request, res: Response): Promise<void> {
  try {
    res.set('Content-Type', register.contentType);
    res.end(await register.metrics());
  } catch (error) {
    res.status(500).end();
  }
}

/**
 * Record upstream request duration.
 */
export function recordUpstreamDuration(
  service: string,
  method: string,
  status: number,
  duration: number
): void {
  upstreamRequestDuration.labels(service, method, status.toString()).observe(duration);
}

/**
 * Record circuit breaker state.
 */
export function recordCircuitBreakerState(
  service: string,
  state: 'closed' | 'half_open' | 'open'
): void {
  const stateValue = state === 'closed' ? 0 : state === 'half_open' ? 1 : 2;
  circuitBreakerState.labels(service).set(stateValue);
}

/**
 * Record rate limit hit.
 */
export function recordRateLimitHit(
  policy: string,
  method: string,
  path: string
): void {
  rateLimitHits.labels(policy, method, normalizePath(path)).inc();
}
