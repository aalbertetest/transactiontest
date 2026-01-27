import pino, { type Logger as PinoLogger } from "pino";

export type LogLevel = "debug" | "info" | "warn" | "error";

export type Logger = PinoLogger;

export type LoggerOptions = {
  service: string;
  env: string;
  level: LogLevel;
};

/**
 * Create a structured JSON logger.
 *
 * Requirements:
 * - Never log secrets (tokens, passwords, payment method details).
 * - Include correlation fields whenever available.
 *
 * Correlation fields (recommended):
 * - request_id
 * - trace_id
 * - tenant_id
 */
export function createLogger(opts: LoggerOptions): Logger {
  return pino({
    level: opts.level,
    base: {
      service: opts.service,
      env: opts.env
    },
    redact: {
      // Aggressive defaults; services may add more paths.
      paths: [
        "password",
        "token",
        "access_token",
        "refresh_token",
        "authorization",
        "headers.authorization"
      ],
      remove: true
    }
  });
}

