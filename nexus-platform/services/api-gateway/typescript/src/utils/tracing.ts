// =============================================================================
// NEXUS PLATFORM - API GATEWAY - TRACING
// =============================================================================
// OpenTelemetry distributed tracing setup.
// =============================================================================

import { NodeSDK } from '@opentelemetry/sdk-node';
import { JaegerExporter } from '@opentelemetry/exporter-jaeger';
import { HttpInstrumentation } from '@opentelemetry/instrumentation-http';
import { ExpressInstrumentation } from '@opentelemetry/instrumentation-express';
import { Resource } from '@opentelemetry/resources';
import { SemanticResourceAttributes } from '@opentelemetry/semantic-conventions';
import { logger } from './logger';

/**
 * Tracing configuration
 */
interface TracingConfig {
  serviceName: string;
  jaegerHost: string;
  jaegerPort: number;
  samplingRate: number;
}

let sdk: NodeSDK | null = null;

/**
 * Initialize OpenTelemetry tracing.
 */
export async function initTracing(config: TracingConfig): Promise<void> {
  try {
    const exporter = new JaegerExporter({
      host: config.jaegerHost,
      port: config.jaegerPort,
    });

    sdk = new NodeSDK({
      resource: new Resource({
        [SemanticResourceAttributes.SERVICE_NAME]: config.serviceName,
        [SemanticResourceAttributes.SERVICE_VERSION]: '1.0.0',
        [SemanticResourceAttributes.DEPLOYMENT_ENVIRONMENT]: 'production',
      }),
      traceExporter: exporter,
      instrumentations: [
        new HttpInstrumentation(),
        new ExpressInstrumentation(),
      ],
    });

    await sdk.start();
    
    logger.info({
      serviceName: config.serviceName,
      jaegerHost: config.jaegerHost,
      jaegerPort: config.jaegerPort,
    }, 'Tracing initialized');

    // Graceful shutdown
    process.on('SIGTERM', async () => {
      if (sdk) {
        await sdk.shutdown();
        logger.info('Tracing shutdown complete');
      }
    });
  } catch (error) {
    logger.error({ error }, 'Failed to initialize tracing');
    throw error;
  }
}

/**
 * Shutdown tracing.
 */
export async function shutdownTracing(): Promise<void> {
  if (sdk) {
    await sdk.shutdown();
    sdk = null;
  }
}
