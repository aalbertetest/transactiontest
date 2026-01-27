import type { FastifyInstance, FastifyReply, FastifyRequest } from "fastify";
import crypto from "node:crypto";

import type { Logger } from "@dsp/common";
import type { Metrics } from "@dsp/common";

export type RequestContext = {
  requestId: string;
  principal?: {
    tenantId?: string;
    userId?: string;
    email?: string;
  };
};

declare module "fastify" {
  interface FastifyRequest {
    ctx: RequestContext;
  }
}

export function installBaseMiddleware(app: FastifyInstance, deps: { logger: Logger; metrics: Metrics }) {
  app.addHook("onRequest", async (req) => {
    const incoming = req.headers["x-request-id"];
    const requestId = typeof incoming === "string" && incoming.length > 0 ? incoming : `req_${crypto.randomUUID()}`;
    req.ctx = { requestId };
  });

  app.addHook("onResponse", async (req, reply) => {
    const route = (req.routeOptions && req.routeOptions.url) || "unknown";
    const status = String(reply.statusCode);
    deps.metrics.httpRequestsTotal.labels(req.method, route, status).inc(1);
  });

  app.setErrorHandler((err, req, reply) => {
    deps.logger.error({ err, request_id: req.ctx?.requestId }, "request failed");
    reply.status(500).send({
      error: "internal",
      message: "internal server error",
      request_id: req.ctx?.requestId ?? "unknown"
    });
  });
}

export function sendError(reply: FastifyReply, status: number, requestId: string, code: string, message: string) {
  reply.status(status).send({ error: code, message, request_id: requestId });
}

export function getBearerToken(req: FastifyRequest): string | undefined {
  const h = req.headers.authorization;
  if (!h || typeof h !== "string") return undefined;
  const [typ, tok] = h.split(" ");
  if (typ?.toLowerCase() !== "bearer" || !tok) return undefined;
  return tok;
}

