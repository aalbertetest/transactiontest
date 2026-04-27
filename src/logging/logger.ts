import pino from "pino";

export function createLogger() {
  return pino({
    level: process.env.LOG_LEVEL ?? "info",
  });
}

export const logger = createLogger();
