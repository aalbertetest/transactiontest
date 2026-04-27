import dotenv from "dotenv";

dotenv.config({ path: new URL("../../.env", import.meta.url) });
dotenv.config();

const required = (name: string, fallback?: string) => {
  const value = process.env[name] ?? fallback;
  if (!value) {
    throw new Error(`Missing required environment variable: ${name}`);
  }
  return value;
};

export const env = {
  nodeEnv: process.env.NODE_ENV ?? "development",
  port: Number(process.env.PORT ?? 4000),
  databaseUrl: required("DATABASE_URL", "postgresql://collab:collab@localhost:5432/collab_editor?schema=public"),
  jwtAccessSecret: required("JWT_ACCESS_SECRET", "dev-access-token-secret-change-me"),
  jwtRefreshSecret: required("JWT_REFRESH_SECRET", "dev-refresh-token-secret-change-me"),
  jwtAudience: process.env.JWT_AUDIENCE ?? "collab-code-editor",
  jwtIssuer: process.env.JWT_ISSUER ?? "collab-code-api",
  accessTokenTtl: process.env.ACCESS_TOKEN_TTL ?? "15m",
  refreshTokenTtlDays: Number(process.env.REFRESH_TOKEN_TTL_DAYS ?? 30),
  corsOrigin: process.env.CORS_ORIGIN ?? "http://localhost:5173",
  documentFlushMs: Number(process.env.DOCUMENT_FLUSH_MS ?? 1000)
};

export const isProduction = env.nodeEnv === "production";
