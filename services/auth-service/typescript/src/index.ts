import Fastify from "fastify";
import helmet from "@fastify/helmet";
import cors from "@fastify/cors";
import bcrypt from "bcryptjs";
import { authenticator } from "otplib";
import crypto from "node:crypto";

import { createLogger, createMetrics, startMetricsServer } from "@dsp/common";

import { loadAuthConfigFromEnv } from "./config.js";
import { TokenRequestSchema } from "./models.js";
import { installBaseMiddleware, sendError, sha256Hex } from "./http.js";
import { createHs256Jwt } from "./tokens.js";
import { InMemoryAuthStore } from "./store.js";

const cfg = loadAuthConfigFromEnv(process.env);
const logger = createLogger({ service: cfg.serviceName, env: cfg.env, level: cfg.logLevel });
const metrics = createMetrics(cfg.serviceName);
startMetricsServer({ addr: cfg.metricsAddr, registry: metrics.registry, logger });

const { signer } = createHs256Jwt(cfg.jwtSecrets, { issuer: cfg.jwtIssuer, audience: cfg.jwtAudience, kid: cfg.jwtKid });

const store = new InMemoryAuthStore();

// Bootstrap a local admin user.
store.upsertUser({
  tenantId: cfg.bootstrapTenantId,
  userId: cfg.bootstrapUserId,
  email: cfg.bootstrapEmail,
  passwordHash: bcrypt.hashSync(cfg.bootstrapPassword, 10),
  totpSecret: cfg.bootstrapTotpSecret,
  createdAt: new Date().toISOString()
});

const app = Fastify({ logger: false });
await app.register(helmet);
await app.register(cors, { origin: true });
installBaseMiddleware(app, { logger, metrics });

app.get("/healthz", async () => ({ status: "ok" }));
app.get("/readyz", async () => ({ status: "ok" }));

app.post("/v1/auth/token", async (req, reply) => {
  const requestId = req.ctx.requestId;
  const parsed = TokenRequestSchema.safeParse(req.body);
  if (!parsed.success) {
    return sendError(reply, 400, requestId, "invalid_request", parsed.error.message);
  }

  const { email, password, mfa_code } = parsed.data;
  const user = store.getUserByEmail(email);
  if (!user) return sendError(reply, 401, requestId, "unauthorized", "invalid credentials");

  const ok = await bcrypt.compare(password, user.passwordHash);
  if (!ok) return sendError(reply, 401, requestId, "unauthorized", "invalid credentials");

  if (user.totpSecret) {
    if (!mfa_code) return sendError(reply, 401, requestId, "mfa_required", "mfa required");
    const good = authenticator.check(mfa_code, user.totpSecret);
    if (!good) return sendError(reply, 401, requestId, "unauthorized", "invalid mfa code");
  }

  // Access token claims:
  // - sub: user id
  // - tid: tenant id
  // - email: email
  const access = await signer.signAccessToken(
    {
      sub: user.userId,
      tid: user.tenantId,
      email: user.email
    },
    cfg.accessTokenTtlSeconds
  );

  // Refresh tokens are stored hashed.
  // In production:
  // - hash with a slow hash and bind to device/session
  // - rotate on every use
  // - revoke on suspicious activity
  const refreshRaw = `rt_${crypto.randomUUID()}`;
  const refreshHash = sha256Hex(refreshRaw);
  const now = Math.floor(Date.now() / 1000);
  store.createRefreshToken({
    tokenHash: refreshHash,
    tenantId: user.tenantId,
    userId: user.userId,
    expiresAtUnix: now + cfg.refreshTokenTtlSeconds
  });

  reply.send({
    access_token: access,
    refresh_token: refreshRaw,
    token_type: "bearer",
    expires_in: cfg.accessTokenTtlSeconds
  });
});

app.post("/v1/auth/refresh", async (req, reply) => {
  const requestId = req.ctx.requestId;
  const body = req.body as any;
  const refresh = typeof body?.refresh_token === "string" ? body.refresh_token : "";
  if (!refresh) return sendError(reply, 400, requestId, "invalid_request", "refresh_token required");

  const tokenHash = sha256Hex(refresh);
  const rec = store.getRefreshByHash(tokenHash);
  if (!rec) return sendError(reply, 401, requestId, "unauthorized", "invalid refresh token");

  const now = Math.floor(Date.now() / 1000);
  if (rec.revokedAtUnix) return sendError(reply, 401, requestId, "unauthorized", "refresh token revoked");
  if (rec.expiresAtUnix <= now) return sendError(reply, 401, requestId, "unauthorized", "refresh token expired");

  // Rotate refresh token on use.
  store.revokeRefresh(tokenHash);
  const newRefreshRaw = `rt_${crypto.randomUUID()}`;
  const newHash = sha256Hex(newRefreshRaw);
  store.createRefreshToken({
    tokenHash: newHash,
    tenantId: rec.tenantId,
    userId: rec.userId,
    expiresAtUnix: now + cfg.refreshTokenTtlSeconds
  });

  const access = await signer.signAccessToken(
    {
      sub: rec.userId,
      tid: rec.tenantId
    },
    cfg.accessTokenTtlSeconds
  );

  reply.send({
    access_token: access,
    refresh_token: newRefreshRaw,
    token_type: "bearer",
    expires_in: cfg.accessTokenTtlSeconds
  });
});

const [host, portStr] = cfg.httpAddr.includes(":") ? cfg.httpAddr.split(":") : ["0.0.0.0", cfg.httpAddr];
const port = Number(portStr);

app.listen({ host, port }).then(() => {
  logger.info({ addr: cfg.httpAddr }, "auth-service listening");
});

