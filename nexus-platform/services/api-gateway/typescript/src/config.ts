// =============================================================================
// NEXUS PLATFORM - API GATEWAY - CONFIGURATION
// =============================================================================
// Centralized configuration management with environment variable support.
// =============================================================================

import { z } from 'zod';
import dotenv from 'dotenv';

// Load environment variables
dotenv.config();

/**
 * Environment schema with validation
 */
const envSchema = z.object({
  // Environment
  NEXUS_ENVIRONMENT: z.enum(['development', 'staging', 'production', 'testing']).default('development'),
  NEXUS_DEBUG: z.string().transform(v => v === 'true').default('false'),
  NEXUS_SERVICE_NAME: z.string().default('api-gateway'),
  NEXUS_SERVICE_VERSION: z.string().default('1.0.0'),
  HOSTNAME: z.string().optional(),

  // Server
  SERVER_HOST: z.string().default('0.0.0.0'),
  SERVER_PORT: z.string().transform(Number).default('8080'),
  SERVER_REQUEST_TIMEOUT: z.string().transform(Number).default('30'),
  SERVER_KEEPALIVE_TIMEOUT: z.string().transform(Number).default('65'),
  SERVER_GRACEFUL_SHUTDOWN_TIMEOUT: z.string().transform(Number).default('30'),
  SERVER_MAX_REQUEST_SIZE: z.string().default('10mb'),
  SERVER_CORS_ENABLED: z.string().transform(v => v === 'true').default('true'),
  SERVER_CORS_ORIGINS: z.string().default('*'),
  SERVER_CORS_METHODS: z.string().default('GET,POST,PUT,DELETE,PATCH,OPTIONS'),
  SERVER_CORS_HEADERS: z.string().default('*'),
  SERVER_CORS_CREDENTIALS: z.string().transform(v => v === 'true').default('true'),

  // Auth
  AUTH_JWT_SECRET_KEY: z.string().default('CHANGE_ME_IN_PRODUCTION_USE_STRONG_SECRET'),
  AUTH_JWT_ALGORITHM: z.string().default('HS256'),
  AUTH_JWT_ISSUER: z.string().default('nexus-platform'),
  AUTH_JWT_AUDIENCE: z.string().default('nexus-api'),
  AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: z.string().transform(Number).default('15'),
  AUTH_JWT_REFRESH_TOKEN_EXPIRE_DAYS: z.string().transform(Number).default('7'),
  AUTH_API_KEY_HEADER: z.string().default('X-API-Key'),
  AUTH_API_KEY_PREFIX: z.string().default('nxp_'),

  // Rate Limiting
  RATE_LIMIT_ENABLED: z.string().transform(v => v === 'true').default('true'),
  RATE_LIMIT_WINDOW_MS: z.string().transform(Number).default('60000'),
  RATE_LIMIT_MAX_REQUESTS: z.string().transform(Number).default('100'),

  // Circuit Breaker
  CIRCUIT_BREAKER_ENABLED: z.string().transform(v => v === 'true').default('true'),
  CIRCUIT_BREAKER_FAILURE_THRESHOLD: z.string().transform(Number).default('5'),
  CIRCUIT_BREAKER_SUCCESS_THRESHOLD: z.string().transform(Number).default('3'),
  CIRCUIT_BREAKER_TIMEOUT: z.string().transform(Number).default('30000'),
  CIRCUIT_BREAKER_RESET_TIMEOUT: z.string().transform(Number).default('60000'),

  // Backend Services
  BACKEND_AUTH_SERVICE_URL: z.string().default('http://auth-service:8081'),
  BACKEND_USER_SERVICE_URL: z.string().default('http://user-service:8082'),
  BACKEND_PAYMENT_SERVICE_URL: z.string().default('http://payment-service:8083'),
  BACKEND_WORKFLOW_SERVICE_URL: z.string().default('http://workflow-engine:8084'),
  BACKEND_QUEUE_SERVICE_URL: z.string().default('http://distributed-queue:8085'),
  BACKEND_STREAMING_SERVICE_URL: z.string().default('http://streaming-platform:8086'),
  BACKEND_CACHE_SERVICE_URL: z.string().default('http://cache-layer:8087'),
  BACKEND_WEBSOCKET_SERVICE_URL: z.string().default('http://websocket-service:8089'),
  BACKEND_SCHEDULER_SERVICE_URL: z.string().default('http://scheduler-service:8090'),
  BACKEND_WORKER_SERVICE_URL: z.string().default('http://worker-fleet:8091'),
  BACKEND_REQUEST_TIMEOUT: z.string().transform(Number).default('30000'),

  // Cache (Redis)
  CACHE_ENABLED: z.string().transform(v => v === 'true').default('true'),
  CACHE_REDIS_URL: z.string().default('redis://redis:6379/0'),
  CACHE_REDIS_PREFIX: z.string().default('nexus:gateway:cache:'),
  CACHE_DEFAULT_TTL: z.string().transform(Number).default('300'),

  // Logging
  LOG_LEVEL: z.enum(['trace', 'debug', 'info', 'warn', 'error', 'fatal']).default('info'),
  LOG_FORMAT: z.enum(['json', 'pretty']).default('json'),
  LOG_REQUESTS: z.string().transform(v => v === 'true').default('true'),

  // Metrics
  METRICS_ENABLED: z.string().transform(v => v === 'true').default('true'),
  METRICS_ENDPOINT: z.string().default('/metrics'),
  METRICS_PREFIX: z.string().default('nexus_gateway'),

  // Tracing
  TRACING_ENABLED: z.string().transform(v => v === 'true').default('true'),
  TRACING_JAEGER_HOST: z.string().default('jaeger'),
  TRACING_JAEGER_PORT: z.string().transform(Number).default('6831'),
  TRACING_SAMPLING_RATE: z.string().transform(Number).default('1.0'),
});

// Parse and validate environment variables
const env = envSchema.parse(process.env);

/**
 * Application configuration object
 */
export const config = {
  environment: env.NEXUS_ENVIRONMENT,
  debug: env.NEXUS_DEBUG,
  serviceName: env.NEXUS_SERVICE_NAME,
  serviceVersion: env.NEXUS_SERVICE_VERSION,
  instanceId: env.HOSTNAME || `gateway-${process.pid}`,

  server: {
    host: env.SERVER_HOST,
    port: env.SERVER_PORT,
    requestTimeout: env.SERVER_REQUEST_TIMEOUT,
    keepaliveTimeout: env.SERVER_KEEPALIVE_TIMEOUT,
    gracefulShutdownTimeout: env.SERVER_GRACEFUL_SHUTDOWN_TIMEOUT,
    maxRequestSize: env.SERVER_MAX_REQUEST_SIZE,
    cors: {
      enabled: env.SERVER_CORS_ENABLED,
      origins: env.SERVER_CORS_ORIGINS.split(','),
      methods: env.SERVER_CORS_METHODS.split(','),
      headers: env.SERVER_CORS_HEADERS.split(','),
      credentials: env.SERVER_CORS_CREDENTIALS,
    },
  },

  auth: {
    jwt: {
      secretKey: env.AUTH_JWT_SECRET_KEY,
      algorithm: env.AUTH_JWT_ALGORITHM,
      issuer: env.AUTH_JWT_ISSUER,
      audience: env.AUTH_JWT_AUDIENCE,
      accessTokenExpireMinutes: env.AUTH_JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
      refreshTokenExpireDays: env.AUTH_JWT_REFRESH_TOKEN_EXPIRE_DAYS,
    },
    apiKey: {
      header: env.AUTH_API_KEY_HEADER,
      prefix: env.AUTH_API_KEY_PREFIX,
    },
  },

  rateLimit: {
    enabled: env.RATE_LIMIT_ENABLED,
    windowMs: env.RATE_LIMIT_WINDOW_MS,
    maxRequests: env.RATE_LIMIT_MAX_REQUESTS,
  },

  circuitBreaker: {
    enabled: env.CIRCUIT_BREAKER_ENABLED,
    failureThreshold: env.CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    successThreshold: env.CIRCUIT_BREAKER_SUCCESS_THRESHOLD,
    timeout: env.CIRCUIT_BREAKER_TIMEOUT,
    resetTimeout: env.CIRCUIT_BREAKER_RESET_TIMEOUT,
  },

  backend: {
    services: {
      'auth-service': env.BACKEND_AUTH_SERVICE_URL,
      'user-service': env.BACKEND_USER_SERVICE_URL,
      'payment-service': env.BACKEND_PAYMENT_SERVICE_URL,
      'workflow-engine': env.BACKEND_WORKFLOW_SERVICE_URL,
      'distributed-queue': env.BACKEND_QUEUE_SERVICE_URL,
      'streaming-platform': env.BACKEND_STREAMING_SERVICE_URL,
      'cache-layer': env.BACKEND_CACHE_SERVICE_URL,
      'websocket-service': env.BACKEND_WEBSOCKET_SERVICE_URL,
      'scheduler-service': env.BACKEND_SCHEDULER_SERVICE_URL,
      'worker-fleet': env.BACKEND_WORKER_SERVICE_URL,
    },
    requestTimeout: env.BACKEND_REQUEST_TIMEOUT,
  },

  cache: {
    enabled: env.CACHE_ENABLED,
    redisUrl: env.CACHE_REDIS_URL,
    redisPrefix: env.CACHE_REDIS_PREFIX,
    defaultTtl: env.CACHE_DEFAULT_TTL,
  },

  logging: {
    level: env.LOG_LEVEL,
    format: env.LOG_FORMAT,
    logRequests: env.LOG_REQUESTS,
  },

  metrics: {
    enabled: env.METRICS_ENABLED,
    endpoint: env.METRICS_ENDPOINT,
    prefix: env.METRICS_PREFIX,
  },

  tracing: {
    enabled: env.TRACING_ENABLED,
    jaegerHost: env.TRACING_JAEGER_HOST,
    jaegerPort: env.TRACING_JAEGER_PORT,
    samplingRate: env.TRACING_SAMPLING_RATE,
  },
} as const;

/**
 * Type for the configuration object
 */
export type Config = typeof config;

/**
 * Check if running in development mode
 */
export function isDevelopment(): boolean {
  return config.environment === 'development';
}

/**
 * Check if running in production mode
 */
export function isProduction(): boolean {
  return config.environment === 'production';
}

/**
 * Validate production configuration
 */
export function validateProductionConfig(): void {
  if (isProduction()) {
    if (config.auth.jwt.secretKey.includes('CHANGE_ME')) {
      throw new Error('JWT secret key must be changed in production');
    }
    if (config.debug) {
      throw new Error('Debug mode must be disabled in production');
    }
    if (config.server.cors.origins.includes('*')) {
      console.warn('Warning: Wildcard CORS origin in production');
    }
  }
}

// Validate on import
validateProductionConfig();
