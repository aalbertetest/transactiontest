import http from "node:http";
import client from "prom-client";
import type { Logger } from "./logging.js";

/**
 * Metrics registry and helpers.
 *
 * Every service exposes:
 * - /metrics endpoint (Prometheus scrape)
 *
 * Services should:
 * - register default metrics
 * - define request counters/histograms
 * - avoid unbounded label cardinality
 */
export type Metrics = {
  registry: client.Registry;
  httpRequestsTotal: client.Counter<string>;
  httpRequestDurationSeconds: client.Histogram<string>;
};

export function createMetrics(serviceName: string): Metrics {
  const registry = new client.Registry();
  registry.setDefaultLabels({ service: serviceName });
  client.collectDefaultMetrics({ register: registry });

  const httpRequestsTotal = new client.Counter({
    name: "http_requests_total",
    help: "Total HTTP requests",
    labelNames: ["method", "route", "status"] as const,
    registers: [registry]
  });

  const httpRequestDurationSeconds = new client.Histogram({
    name: "http_request_duration_seconds",
    help: "HTTP request duration in seconds",
    labelNames: ["method", "route", "status"] as const,
    buckets: [0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10],
    registers: [registry]
  });

  return { registry, httpRequestsTotal, httpRequestDurationSeconds };
}

export function startMetricsServer(opts: {
  addr: string;
  registry: client.Registry;
  logger: Logger;
}): http.Server {
  const [host, portStr] = opts.addr.includes(":") ? opts.addr.split(":") : ["0.0.0.0", opts.addr];
  const port = Number(portStr);
  if (!Number.isFinite(port)) {
    throw new Error(`Invalid metrics address: ${opts.addr}`);
  }

  const server = http.createServer(async (req, res) => {
    if (req.method === "GET" && req.url === "/metrics") {
      try {
        const body = await opts.registry.metrics();
        res.writeHead(200, { "Content-Type": opts.registry.contentType });
        res.end(body);
      } catch (err) {
        opts.logger.error({ err }, "metrics endpoint failed");
        res.writeHead(500, { "Content-Type": "text/plain" });
        res.end("metrics error");
      }
      return;
    }

    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end("not found");
  });

  server.listen(port, host, () => {
    opts.logger.info({ addr: opts.addr }, "metrics server listening");
  });

  return server;
}

