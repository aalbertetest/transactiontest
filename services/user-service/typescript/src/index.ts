import Fastify from "fastify";
import helmet from "@fastify/helmet";
import cors from "@fastify/cors";

import { createLogger, createMetrics, startMetricsServer } from "@dsp/common";

import { loadUserConfigFromEnv } from "./config.js";
import { createJwtVerifier } from "./auth.js";
import { getBearerToken, installBaseMiddleware, sendError } from "./http.js";

const cfg = loadUserConfigFromEnv(process.env);
const logger = createLogger({ service: cfg.serviceName, env: cfg.env, level: cfg.logLevel });
const metrics = createMetrics(cfg.serviceName);
startMetricsServer({ addr: cfg.metricsAddr, registry: metrics.registry, logger });

const verifier = createJwtVerifier(cfg.jwtSecrets, { issuer: cfg.jwtIssuer, audience: cfg.jwtAudience });

const app = Fastify({ logger: false });
await app.register(helmet);
await app.register(cors, { origin: true });
installBaseMiddleware(app, { logger, metrics });

app.get("/healthz", async () => ({ status: "ok" }));
app.get("/readyz", async () => ({ status: "ok" }));

// Auth middleware for protected endpoints.
app.addHook("preHandler", async (req, reply) => {
  // Only protect /v1/* endpoints in this service.
  if (!req.url.startsWith("/v1/")) return;

  const token = getBearerToken(req);
  if (!token) {
    return sendError(reply, 401, req.ctx.requestId, "unauthorized", "missing bearer token");
  }

  try {
    const payload = await verifier.verify(token);
    req.ctx.principal = {
      tenantId: typeof payload.tid === "string" ? payload.tid : undefined,
      userId: typeof payload.sub === "string" ? payload.sub : undefined,
      email: typeof payload.email === "string" ? payload.email : undefined
    };
  } catch {
    return sendError(reply, 401, req.ctx.requestId, "unauthorized", "invalid token");
  }
});

app.get("/v1/users/me", async (req) => {
  const p = req.ctx.principal ?? {};
  return {
    id: p.userId ?? "unknown",
    email: p.email ?? "unknown",
    tenant_id: p.tenantId,
    created_at: new Date().toISOString()
  };
});

const [host, portStr] = cfg.httpAddr.includes(":") ? cfg.httpAddr.split(":") : ["0.0.0.0", cfg.httpAddr];
const port = Number(portStr);
app.listen({ host, port }).then(() => {
  logger.info({ addr: cfg.httpAddr }, "user-service listening");
});

