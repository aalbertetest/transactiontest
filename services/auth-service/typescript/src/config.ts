import { z } from "zod";
import { BaseConfigSchema, loadBaseConfigFromEnv } from "@dsp/common";

/**
 * Auth service configuration (TypeScript).
 *
 * Security notes:
 * - For production, prefer asymmetric JWT signing (RS256/EdDSA) with JWKS publication.
 * - This initial implementation uses HS256 with key rotation support to keep the stack
 *   runnable without external key infrastructure.
 */
export const AuthConfigSchema = BaseConfigSchema.extend({
  jwtIssuer: z.string().min(1).default("dsp-auth"),
  jwtAudience: z.string().min(1).default("dsp"),

  /**
   * Comma-separated secrets.
   * - first secret is used for signing new tokens
   * - all secrets are accepted for verification (key rotation)
   */
  jwtSecrets: z.string().min(16),
  jwtKid: z.string().min(1).default("k1"),

  accessTokenTtlSeconds: z.coerce.number().int().positive().default(900),
  refreshTokenTtlSeconds: z.coerce.number().int().positive().default(60 * 60 * 24 * 7),

  // Bootstrap identity for local dev.
  bootstrapTenantId: z.string().min(1).default("ten_dev"),
  bootstrapUserId: z.string().min(1).default("usr_dev"),
  bootstrapEmail: z.string().email().default("admin@example.com"),
  bootstrapPassword: z.string().min(8).default("ChangeMeNow123!"),
  bootstrapTotpSecret: z.string().min(16).optional()
});

export type AuthConfig = z.infer<typeof AuthConfigSchema>;

export function loadAuthConfigFromEnv(env: NodeJS.ProcessEnv): AuthConfig {
  const base = loadBaseConfigFromEnv(env);
  const parsed = AuthConfigSchema.safeParse({
    ...base,
    jwtIssuer: env.DSP_JWT_ISSUER,
    jwtAudience: env.DSP_JWT_AUDIENCE,
    jwtSecrets: env.DSP_JWT_SECRETS,
    jwtKid: env.DSP_JWT_KID,
    accessTokenTtlSeconds: env.DSP_ACCESS_TOKEN_TTL_SECONDS,
    refreshTokenTtlSeconds: env.DSP_REFRESH_TOKEN_TTL_SECONDS,
    bootstrapTenantId: env.DSP_BOOTSTRAP_TENANT_ID,
    bootstrapUserId: env.DSP_BOOTSTRAP_USER_ID,
    bootstrapEmail: env.DSP_BOOTSTRAP_EMAIL,
    bootstrapPassword: env.DSP_BOOTSTRAP_PASSWORD,
    bootstrapTotpSecret: env.DSP_BOOTSTRAP_TOTP_SECRET
  });

  if (!parsed.success) {
    const msg = parsed.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ");
    throw new Error(`Invalid auth configuration: ${msg}`);
  }

  return parsed.data;
}

