// =============================================================================
// NEXUS PLATFORM - API GATEWAY - METRICS UTILITY
// =============================================================================
// Prometheus metrics initialization.
// =============================================================================

import { logger } from './logger';

/**
 * Initialize metrics collection.
 */
export function initMetrics(prefix: string): void {
  logger.info({ prefix }, 'Metrics initialized');
  // Metrics are initialized in the middleware module
  // This function provides a hook for any additional setup
}
