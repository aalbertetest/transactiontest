import { z } from "zod";

/**
 * Shared configuration schema for DSP services (TypeScript).
 *
 * Each service may extend this schema with service-specific settings.
 * Loading precedence:
 * - environment variables
 * - config file (optional in later iterations)
 * - defaults
 */
export const BaseConfigSchema = z.object({
  env: z.enum(["dev", "staging", "prod"]).default("dev"),
  serviceName: z.string().min(1),
  logLevel: z.enum(["debug", "info", "warn", "error"]).default("info"),
  httpAddr: z.string().default("0.0.0.0:8080"),
  metricsAddr: z.string().default("0.0.0.0:9091")
});

export type BaseConfig = z.infer<typeof BaseConfigSchema>;

export function loadBaseConfigFromEnv(env: NodeJS.ProcessEnv): BaseConfig {
  // IMPORTANT: keep env var names stable across languages.
  const parsed = BaseConfigSchema.safeParse({
    env: env.DSP_ENV,
    serviceName: env.DSP_SERVICE_NAME,
    logLevel: env.DSP_LOG_LEVEL,
    httpAddr: env.DSP_HTTP_ADDR,
    metricsAddr: env.DSP_METRICS_ADDR
  });

  if (!parsed.success) {
    const msg = parsed.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ");
    throw new Error(`Invalid configuration: ${msg}`);
  }

  return parsed.data;
}

