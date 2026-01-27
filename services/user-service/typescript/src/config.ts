import { z } from "zod";
import { BaseConfigSchema, loadBaseConfigFromEnv } from "@dsp/common";

export const UserConfigSchema = BaseConfigSchema.extend({
  jwtIssuer: z.string().min(1).default("dsp-auth"),
  jwtAudience: z.string().min(1).default("dsp"),
  jwtSecrets: z.string().min(16)
});

export type UserConfig = z.infer<typeof UserConfigSchema>;

export function loadUserConfigFromEnv(env: NodeJS.ProcessEnv): UserConfig {
  const base = loadBaseConfigFromEnv(env);
  const parsed = UserConfigSchema.safeParse({
    ...base,
    jwtIssuer: env.DSP_JWT_ISSUER,
    jwtAudience: env.DSP_JWT_AUDIENCE,
    jwtSecrets: env.DSP_JWT_SECRETS
  });

  if (!parsed.success) {
    const msg = parsed.error.issues.map((i) => `${i.path.join(".")}: ${i.message}`).join("; ");
    throw new Error(`Invalid user-service configuration: ${msg}`);
  }
  return parsed.data;
}

