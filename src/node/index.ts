import http, { IncomingMessage, ServerResponse } from "http";
import crypto from "crypto";
import url from "url";

// ---------------------------
// Configuration and utilities
// ---------------------------

type Config = {
  gatewayPort: number;
  authPort: number;
  userPort: number;
  paymentPort: number;
  workflowPort: number;
  queuePort: number;
  streamPort: number;
  cachePort: number;
  dbPort: number;
  wsPort: number;
  schedulerPort: number;
  workerPort: number;
  jwtSecret: string;
  rateLimitPerMin: number;
  workerConcurrency: number;
  env: string;
  serviceOnly: string[];
};

function loadConfig(): Config {
  return {
    gatewayPort: parseInt(process.env.GATEWAY_PORT || "8080", 10),
    authPort: parseInt(process.env.AUTH_PORT || "8081", 10),
    userPort: parseInt(process.env.USER_PORT || "8082", 10),
    paymentPort: parseInt(process.env.PAYMENT_PORT || "8083", 10),
    workflowPort: parseInt(process.env.WORKFLOW_PORT || "8084", 10),
    queuePort: parseInt(process.env.QUEUE_PORT || "8085", 10),
    streamPort: parseInt(process.env.STREAM_PORT || "8086", 10),
    cachePort: parseInt(process.env.CACHE_PORT || "8087", 10),
    dbPort: parseInt(process.env.DB_PORT || "8088", 10),
    wsPort: parseInt(process.env.WS_PORT || "8089", 10),
    schedulerPort: parseInt(process.env.SCHEDULER_PORT || "8090", 10),
    workerPort: parseInt(process.env.WORKER_PORT || "8091", 10),
    jwtSecret: process.env.JWT_SECRET || "dev-secret",
    rateLimitPerMin: parseInt(process.env.RATE_LIMIT_PER_MIN || "600", 10),
    workerConcurrency: parseInt(process.env.WORKER_CONCURRENCY || "8", 10),
    env: process.env.ENV || "dev",
    serviceOnly: (process.env.SERVICE_ONLY || "").split(",").map((s) => s.trim()).filter(Boolean),
  };
}

function nowUnix(): number {
  return Math.floor(Date.now() / 1000);
}

function newId(prefix: string): string {
  return `${prefix}_${crypto.randomBytes(6).toString("hex")}`;
}

// ---------------------------
// Logging and metrics
// ---------------------------

class Logger {
  constructor(private service: string) {}

  log(level: string, message: string, fields: Record<string, unknown> = {}): void {
    const entry = {
      ts: new Date().toISOString(),
      level,
      service: this.service,
      message,
      fields,
    };
    process.stdout.write(`${JSON.stringify(entry)}\n`);
  }

  info(message: string, fields?: Record<string, unknown>): void {
    this.log("INFO", message, fields || {});
  }

  warn(message: string, fields?: Record<string, unknown>): void {
    this.log("WARN", message, fields || {});
  }

  error(message: string, fields?: Record<string, unknown>): void {
    this.log("ERROR", message, fields || {});
  }
}

class Metrics {
  counters: Record<string, number> = {};
  latencies: Record<string, number[]> = {};

  inc(name: string, value = 1): void {
    this.counters[name] = (this.counters[name] || 0) + value;
  }

  observe(name: string, value: number): void {
    if (!this.latencies[name]) this.latencies[name] = [];
    this.latencies[name].push(value);
  }

  render(): string {
    const lines: string[] = [];
    Object.entries(this.counters).forEach(([name, value]) => {
      lines.push(`# TYPE ${name} counter`);
      lines.push(`${name} ${value}`);
    });
    Object.entries(this.latencies).forEach(([name, values]) => {
      const avg = values.length ? values.reduce((a, b) => a + b, 0) / values.length : 0;
      lines.push(`# TYPE ${name} gauge`);
      lines.push(`${name}_avg ${avg}`);
    });
    return `${lines.join("\n")}\n`;
  }
}

// ---------------------------
// Errors, retry, rate limits
// ---------------------------

class ApiError extends Error {
  constructor(
    public status: number,
    public code: string,
    public message: string,
    public retryable = false
  ) {
    super(message);
  }
}

// Data models for typed SDK usage
type UserModel = {
  id: string;
  email: string;
  display_name: string;
  status: string;
};

type PaymentIntentModel = {
  id: string;
  user_id: string;
  amount: number;
  currency: string;
  status: string;
  idempotency_key?: string;
};

type WorkflowRunModel = {
  id: string;
  workflow_id: string;
  status: string;
  current_step: string;
};

type QueueMessageModel = {
  id: string;
  queue: string;
  payload: Record<string, unknown>;
  attempt: number;
};

type StreamRecordModel = {
  topic: string;
  partition: number;
  offset: number;
  key: string;
  value: string;
};

async function withRetry<T>(fn: () => Promise<T>, retries = 3): Promise<T> {
  let lastError: Error | null = null;
  for (let i = 0; i <= retries; i += 1) {
    try {
      return await fn();
    } catch (err) {
      lastError = err as Error;
      await new Promise((resolve) => setTimeout(resolve, 50 * Math.pow(2, i)));
    }
  }
  throw lastError!;
}

class RateLimiter {
  private tokens: Record<string, number> = {};
  private timestamps: Record<string, number> = {};

  constructor(private limit: number) {}

  allow(key: string): boolean {
    const now = nowUnix();
    if (!this.timestamps[key] || now - this.timestamps[key] >= 60) {
      this.tokens[key] = this.limit;
      this.timestamps[key] = now;
    }
    if (this.tokens[key] <= 0) return false;
    this.tokens[key] -= 1;
    return true;
  }
}

class IdempotencyStore {
  private store: Record<string, { ts: number; value: Record<string, unknown> }> = {};
  private ttl = 3600;

  get(key: string): Record<string, unknown> | null {
    const entry = this.store[key];
    if (!entry) return null;
    if (nowUnix() - entry.ts > this.ttl) {
      delete this.store[key];
      return null;
    }
    return entry.value;
  }

  set(key: string, value: Record<string, unknown>): void {
    this.store[key] = { ts: nowUnix(), value };
  }
}

// ---------------------------
// HTTP routing and middleware
// ---------------------------

type Context = {
  req: IncomingMessage;
  res: ServerResponse;
  body: Record<string, unknown>;
  params: Record<string, string>;
  correlationId: string;
  idempotencyKey: string;
};

type Handler = (ctx: Context) => Promise<void> | void;
type Middleware = (ctx: Context, next: () => Promise<void>) => Promise<void>;

class Router {
  private routes: Array<{
    method: string;
    segments: string[];
    handler: Handler;
    middleware: Middleware[];
  }> = [];

  add(method: string, path: string, handler: Handler, middleware: Middleware[] = []): void {
    const segments = path.replace(/^\/|\/$/g, "").split("/").filter(Boolean);
    this.routes.push({ method: method.toUpperCase(), segments, handler, middleware });
  }

  async handle(req: IncomingMessage, res: ServerResponse): Promise<void> {
    const parsed = url.parse(req.url || "", true);
    const segments = (parsed.pathname || "").replace(/^\/|\/$/g, "").split("/").filter(Boolean);
    for (const route of this.routes) {
      if (route.method !== (req.method || "").toUpperCase()) continue;
      if (route.segments.length !== segments.length) continue;
      const params: Record<string, string> = {};
      let matched = true;
      route.segments.forEach((seg, idx) => {
        if (seg.startsWith("{") && seg.endsWith("}")) {
          params[seg.slice(1, -1)] = segments[idx];
        } else if (seg !== segments[idx]) {
          matched = false;
        }
      });
      if (!matched) continue;
      const body = await readBody(req);
      const ctx: Context = {
        req,
        res,
        body,
        params,
        correlationId: req.headers["correlation-id"]?.toString() || newId("corr"),
        idempotencyKey: req.headers["idempotency-key"]?.toString() || "",
      };
      const chain = route.middleware.reduceRight(
        (next, mw) => () => mw(ctx, next),
        async () => route.handler(ctx)
      );
      try {
        await chain();
      } catch (err) {
        handleError(res, err as Error, ctx.correlationId);
      }
      return;
    }
    json(res, 404, { error: { code: "not_found", message: "route not found" } });
  }
}

async function readBody(req: IncomingMessage): Promise<Record<string, unknown>> {
  const chunks: Buffer[] = [];
  for await (const chunk of req) {
    chunks.push(chunk as Buffer);
  }
  if (!chunks.length) return {};
  try {
    return JSON.parse(Buffer.concat(chunks).toString("utf-8"));
  } catch {
    throw new ApiError(400, "invalid_json", "Invalid JSON payload");
  }
}

function json(res: ServerResponse, status: number, body: unknown): void {
  const payload = Buffer.from(JSON.stringify(body));
  res.writeHead(status, { "Content-Type": "application/json", "Content-Length": payload.length });
  res.end(payload);
}

function handleError(res: ServerResponse, err: Error, correlationId: string): void {
  if (err instanceof ApiError) {
    json(res, err.status, {
      error: { code: err.code, message: err.message, retryable: err.retryable, request_id: correlationId },
    });
    return;
  }
  json(res, 500, { error: { code: "internal_error", message: "internal error" } });
}

function middlewareLogging(logger: Logger, metrics: Metrics): Middleware {
  return async (ctx, next) => {
    const start = Date.now();
    logger.info("request_start", { path: ctx.req.url });
    await next();
    metrics.inc("http_requests_total");
    metrics.observe("http_request_latency_seconds", (Date.now() - start) / 1000);
  };
}

function middlewareRateLimit(limiter: RateLimiter): Middleware {
  return async (ctx, next) => {
    const ip = ctx.req.socket.remoteAddress || "unknown";
    if (!limiter.allow(ip)) {
      throw new ApiError(429, "rate_limited", "Too many requests", true);
    }
    await next();
  };
}

function middlewareAuth(secret: string): Middleware {
  return async (ctx, next) => {
    const auth = ctx.req.headers.authorization || "";
    const token = auth.replace("Bearer ", "");
    if (!token) throw new ApiError(401, "missing_token", "Missing token");
    jwtDecode(token, secret);
    await next();
  };
}

// ---------------------------
// Stores and brokers
// ---------------------------

class CacheStore {
  private data: Record<string, { value: string; exp: number }> = {};

  get(key: string): string | null {
    const entry = this.data[key];
    if (!entry) return null;
    if (entry.exp && Date.now() > entry.exp) {
      delete this.data[key];
      return null;
    }
    return entry.value;
  }

  put(key: string, value: string, ttlSeconds: number): void {
    const exp = ttlSeconds ? Date.now() + ttlSeconds * 1000 : 0;
    this.data[key] = { value, exp };
  }

  delete(key: string): void {
    delete this.data[key];
  }
}

class QueueBroker {
  private queues: Record<string, Array<Record<string, unknown>>> = {};
  private inflight: Record<string, Record<string, unknown>> = {};

  enqueue(name: string, payload: Record<string, unknown>): Record<string, unknown> {
    const msg = {
      id: newId("msg"),
      queue: name,
      payload,
      attempt: 0,
      visible_at: nowUnix(),
    };
    this.queues[name] = this.queues[name] || [];
    this.queues[name].push(msg);
    return msg;
  }

  dequeue(name: string, max = 1): Array<Record<string, unknown>> {
    const now = nowUnix();
    const queue = this.queues[name] || [];
    const msgs = queue.filter((m) => (m.visible_at as number) <= now).slice(0, max);
    msgs.forEach((m) => {
      m.attempt = (m.attempt as number) + 1;
      m.visible_at = now + 30;
      this.inflight[m.id as string] = m;
    });
    return msgs;
  }

  ack(id: string, success: boolean): void {
    const msg = this.inflight[id];
    if (!msg) return;
    delete this.inflight[id];
    if (!success) {
      msg.visible_at = nowUnix() + Math.min(60 * (msg.attempt as number), 300);
      this.queues[msg.queue as string] = this.queues[msg.queue as string] || [];
      this.queues[msg.queue as string].push(msg);
    }
  }
}

class StreamBroker {
  private topics: Record<string, { partitions: number; records: Record<number, Array<Record<string, unknown>>>; offsets: Record<number, number> }> = {};
  private offsets: Record<string, Record<string, number>> = {};

  createTopic(name: string, partitions = 3): void {
    if (this.topics[name]) return;
    const records: Record<number, Array<Record<string, unknown>>> = {};
    const offsets: Record<number, number> = {};
    for (let i = 0; i < partitions; i += 1) {
      records[i] = [];
      offsets[i] = 0;
    }
    this.topics[name] = { partitions, records, offsets };
  }

  publish(topic: string, key: string, value: string): Record<string, unknown> {
    if (!this.topics[topic]) this.createTopic(topic);
    const info = this.topics[topic];
    const partition = Math.abs(hashString(key)) % info.partitions;
    const offset = info.offsets[partition];
    const record = { topic, partition, offset, key, value };
    info.records[partition].push(record);
    info.offsets[partition] += 1;
    return record;
  }

  consume(topic: string, group: string, max = 10): Array<Record<string, unknown>> {
    const info = this.topics[topic];
    if (!info) return [];
    const keyPrefix = `${topic}:`;
    this.offsets[group] = this.offsets[group] || {};
    const out: Array<Record<string, unknown>> = [];
    for (let p = 0; p < info.partitions; p += 1) {
      const key = `${keyPrefix}${p}`;
      const offset = this.offsets[group][key] || 0;
      const records = info.records[p].slice(offset, offset + max);
      out.push(...records);
    }
    return out;
  }

  commit(topic: string, group: string, partition: number, offset: number): void {
    this.offsets[group] = this.offsets[group] || {};
    this.offsets[group][`${topic}:${partition}`] = offset;
  }
}

function hashString(input: string): number {
  return crypto.createHash("sha256").update(input).digest()[0];
}

class DocumentStore {
  private items: Record<string, Record<string, Record<string, unknown>>> = {};

  get(collection: string, key: string): Record<string, unknown> | null {
    return this.items[collection]?.[key] || null;
  }

  put(collection: string, key: string, doc: Record<string, unknown>): void {
    this.items[collection] = this.items[collection] || {};
    this.items[collection][key] = doc;
  }
}

// ---------------------------
// JWT and MFA helpers
// ---------------------------

function jwtEncode(payload: Record<string, unknown>, secret: string, expiresIn: number): string {
  const header = Buffer.from(JSON.stringify({ alg: "HS256", typ: "JWT" })).toString("base64url");
  const body = Buffer.from(JSON.stringify({ ...payload, exp: nowUnix() + expiresIn })).toString("base64url");
  const signing = `${header}.${body}`;
  const sig = crypto.createHmac("sha256", secret).update(signing).digest("base64url");
  return `${signing}.${sig}`;
}

function jwtDecode(token: string, secret: string): Record<string, unknown> {
  const [header, body, sig] = token.split(".");
  if (!header || !body || !sig) throw new ApiError(401, "invalid_token", "Invalid token");
  const expected = crypto.createHmac("sha256", secret).update(`${header}.${body}`).digest("base64url");
  if (expected !== sig) throw new ApiError(401, "invalid_token", "Signature mismatch");
  const payload = JSON.parse(Buffer.from(body, "base64url").toString("utf-8"));
  if (payload.exp < nowUnix()) throw new ApiError(401, "expired_token", "Token expired");
  return payload;
}

function totp(secret: string): string {
  const key = Buffer.from(secret, "base64");
  const counter = Math.floor(nowUnix() / 30);
  const buf = Buffer.alloc(8);
  buf.writeBigInt64BE(BigInt(counter), 0);
  const hmac = crypto.createHmac("sha1", key).update(buf).digest();
  const offset = hmac[hmac.length - 1] & 0x0f;
  const code = (hmac.readUInt32BE(offset) & 0x7fffffff) % 1000000;
  return code.toString().padStart(6, "0");
}

// ---------------------------
// Services
// ---------------------------

class AuthService {
  private clients: Record<string, string> = {};
  private authCodes: Record<string, string> = {};
  private refreshTokens: Record<string, string> = {};
  private mfa: Record<string, string> = {};

  constructor(private config: Config) {}

  registerClient(id: string, secret: string): void {
    this.clients[id] = secret;
  }

  authorize(ctx: Context): void {
    const clientId = (ctx.body.client_id as string) || "";
    const userId = (ctx.body.user_id as string) || "";
    if (!clientId || !userId) throw new ApiError(401, "invalid_client", "Invalid client");
    const code = newId("code");
    this.authCodes[code] = userId;
    json(ctx.res, 200, { code, state: ctx.body.state });
  }

  token(ctx: Context): void {
    const grant = (ctx.body.grant_type as string) || "authorization_code";
    if (grant !== "authorization_code") {
      throw new ApiError(400, "unsupported_grant", "Unsupported grant");
    }
    const code = (ctx.body.code as string) || "";
    const clientId = (ctx.body.client_id as string) || "";
    const clientSecret = (ctx.body.client_secret as string) || "";
    if (this.clients[clientId] !== clientSecret) {
      throw new ApiError(401, "invalid_client", "Invalid client");
    }
    const userId = this.authCodes[code];
    if (!userId) throw new ApiError(401, "invalid_code", "Invalid code");
    const token = jwtEncode({ sub: userId, scope: "basic", mfa: false }, this.config.jwtSecret, 3600);
    const refresh = newId("rft");
    this.refreshTokens[refresh] = userId;
    json(ctx.res, 200, { access_token: token, refresh_token: refresh, expires_in: 3600 });
  }

  refresh(ctx: Context): void {
    const refresh = (ctx.body.refresh_token as string) || "";
    const userId = this.refreshTokens[refresh];
    if (!userId) throw new ApiError(401, "invalid_refresh", "Invalid refresh token");
    const token = jwtEncode({ sub: userId, scope: "basic", mfa: true }, this.config.jwtSecret, 3600);
    json(ctx.res, 200, { access_token: token, refresh_token: refresh, expires_in: 3600 });
  }

  enrollMfa(ctx: Context): void {
    const userId = (ctx.body.user_id as string) || "";
    if (!userId) throw new ApiError(400, "missing_user", "user_id required");
    const secret = crypto.randomBytes(10).toString("base64");
    this.mfa[userId] = secret;
    const uri = `otpauth://totp/Platform:${userId}?secret=${secret}&issuer=Platform`;
    json(ctx.res, 200, { secret, uri });
  }

  verifyMfa(ctx: Context): void {
    const userId = (ctx.body.user_id as string) || "";
    const code = (ctx.body.code as string) || "";
    const secret = this.mfa[userId];
    if (!secret) throw new ApiError(404, "mfa_not_enrolled", "MFA not enrolled");
    json(ctx.res, 200, { verified: totp(secret) === code });
  }
}

class UserService {
  private users: Record<string, Record<string, unknown>> = {};

  register(ctx: Context): void {
    const email = (ctx.body.email as string) || "";
    const displayName = (ctx.body.display_name as string) || "";
    if (!email.includes("@") || !displayName) throw new ApiError(400, "invalid_user", "Invalid user data");
    const id = newId("usr");
    this.users[id] = { id, email, display_name: displayName, status: "active" };
    json(ctx.res, 201, this.users[id]);
  }

  get(ctx: Context): void {
    const user = this.users[ctx.params.id];
    if (!user) throw new ApiError(404, "not_found", "User not found");
    json(ctx.res, 200, user);
  }

  update(ctx: Context): void {
    const user = this.users[ctx.params.id];
    if (!user) throw new ApiError(404, "not_found", "User not found");
    if (ctx.body.display_name) user.display_name = ctx.body.display_name;
    if (ctx.body.status) user.status = ctx.body.status;
    json(ctx.res, 200, user);
  }
}

class PaymentService {
  private intents: Record<string, Record<string, unknown>> = {};

  constructor(
    private queue: QueueBroker,
    private stream: StreamBroker,
    private idempotency: IdempotencyStore
  ) {}

  createIntent(ctx: Context): void {
    const key = ctx.idempotencyKey || (ctx.body.idempotency_key as string) || "";
    if (!key) throw new ApiError(400, "missing_idempotency", "Idempotency-Key required");
    const cached = this.idempotency.get(key);
    if (cached) {
      json(ctx.res, 200, cached);
      return;
    }
    const id = newId("pi");
    this.intents[id] = {
      id,
      user_id: ctx.body.user_id,
      amount: ctx.body.amount,
      currency: ctx.body.currency,
      status: "pending",
    };
    this.queue.enqueue("payments", { intent_id: id });
    this.idempotency.set(key, { id, status: "pending" });
    json(ctx.res, 202, { id, status: "pending" });
  }

  getIntent(ctx: Context): void {
    const intent = this.intents[ctx.params.id];
    if (!intent) throw new ApiError(404, "not_found", "Payment intent not found");
    json(ctx.res, 200, intent);
  }

  captureIntent(ctx: Context): void {
    const intent = this.intents[ctx.params.id];
    if (!intent) throw new ApiError(404, "not_found", "Payment intent not found");
    intent.status = "captured";
    json(ctx.res, 200, intent);
  }

  refundIntent(ctx: Context): void {
    const intent = this.intents[ctx.params.id];
    if (!intent) throw new ApiError(404, "not_found", "Payment intent not found");
    intent.status = "refunded";
    json(ctx.res, 200, intent);
  }

  processCharge(payload: Record<string, unknown>): void {
    const id = payload.intent_id as string;
    const intent = this.intents[id];
    if (intent) intent.status = "succeeded";
    this.stream.publish("payments", id, JSON.stringify({ status: "succeeded" }));
  }
}

class WorkflowEngine {
  private workflows: Record<string, Record<string, unknown>> = {};
  private runs: Record<string, Record<string, unknown>> = {};

  constructor(private queue: QueueBroker, private stream: StreamBroker) {}

  register(ctx: Context): void {
    const id = newId("wf");
    this.workflows[id] = { id, name: ctx.body.name, definition: ctx.body.definition };
    json(ctx.res, 201, { workflow_id: id });
  }

  start(ctx: Context): void {
    const runId = newId("wr");
    this.runs[runId] = { id: runId, workflow_id: ctx.params.id, status: "running", current_step: "start" };
    this.queue.enqueue("workflow", { run_id: runId, step: "start" });
    this.stream.publish("workflows", runId, JSON.stringify({ status: "running" }));
    json(ctx.res, 202, { run_id: runId, status: "running" });
  }

  getRun(ctx: Context): void {
    const run = this.runs[ctx.params.run_id];
    if (!run) throw new ApiError(404, "not_found", "Workflow run not found");
    json(ctx.res, 200, run);
  }

  processTask(payload: Record<string, unknown>): void {
    const runId = payload.run_id as string;
    const step = payload.step as string;
    const run = this.runs[runId];
    if (!run) return;
    run.current_step = step;
    if (step === "start") this.queue.enqueue("workflow", { run_id: runId, step: "complete" });
    if (step === "complete") {
      run.status = "completed";
      this.stream.publish("workflows", runId, JSON.stringify({ status: "completed" }));
    }
  }
}

class QueueService {
  constructor(private broker: QueueBroker) {}

  enqueue(ctx: Context): void {
    const msg = this.broker.enqueue(ctx.params.name, (ctx.body.payload as Record<string, unknown>) || {});
    json(ctx.res, 201, msg);
  }

  dequeue(ctx: Context): void {
    const msgs = this.broker.dequeue(ctx.params.name, 1);
    json(ctx.res, 200, { messages: msgs });
  }

  ack(ctx: Context): void {
    const msgId = (ctx.body.message_id as string) || "";
    const success = (ctx.body.success as boolean) ?? true;
    this.broker.ack(msgId, success);
    json(ctx.res, 200, { status: "ok" });
  }
}

class StreamService {
  constructor(private broker: StreamBroker) {}

  publish(ctx: Context): void {
    const record = this.broker.publish(ctx.params.topic, (ctx.body.key as string) || "", JSON.stringify(ctx.body.value || {}));
    json(ctx.res, 200, record);
  }

  consume(ctx: Context): void {
    const records = this.broker.consume(ctx.params.topic, (ctx.body.group as string) || "default");
    json(ctx.res, 200, { records });
  }

  commit(ctx: Context): void {
    const partition = Number(ctx.body.partition || 0);
    const offset = Number(ctx.body.offset || 0);
    this.broker.commit(ctx.params.topic, (ctx.body.group as string) || "default", partition, offset);
    json(ctx.res, 200, { status: "ok" });
  }
}

class CacheService {
  constructor(private cache: CacheStore) {}

  get(ctx: Context): void {
    const value = this.cache.get(ctx.params.key);
    if (!value) throw new ApiError(404, "cache_miss", "Cache miss");
    json(ctx.res, 200, { key: ctx.params.key, value });
  }

  put(ctx: Context): void {
    const value = (ctx.body.value as string) || "";
    const ttl = Number(ctx.body.ttl_seconds || 60);
    this.cache.put(ctx.params.key, value, ttl);
    json(ctx.res, 200, { status: "ok" });
  }

  delete(ctx: Context): void {
    this.cache.delete(ctx.params.key);
    json(ctx.res, 200, { status: "ok" });
  }
}

class DatabaseService {
  private users: Record<string, Record<string, unknown>> = {};
  constructor(private docs: DocumentStore) {}

  query(ctx: Context): void {
    const sql = ((ctx.body.sql as string) || "").toLowerCase();
    if (sql.includes("from users")) {
      const rows = Object.values(this.users);
      json(ctx.res, 200, { rows });
      return;
    }
    throw new ApiError(400, "unsupported_sql", "Unsupported SQL in demo engine");
  }

  execute(ctx: Context): void {
    const sql = ((ctx.body.sql as string) || "").toLowerCase();
    if (sql.startsWith("insert into users")) {
      const id = newId("usr");
      this.users[id] = { id };
      json(ctx.res, 200, { status: "ok" });
      return;
    }
    throw new ApiError(400, "unsupported_sql", "Unsupported SQL in demo engine");
  }

  documentGet(ctx: Context): void {
    const doc = this.docs.get((ctx.body.collection as string) || "", (ctx.body.key as string) || "");
    if (!doc) throw new ApiError(404, "doc_not_found", "Document not found");
    json(ctx.res, 200, { document: doc });
  }

  documentPut(ctx: Context): void {
    this.docs.put((ctx.body.collection as string) || "", (ctx.body.key as string) || "", (ctx.body.document as Record<string, unknown>) || {});
    json(ctx.res, 200, { status: "ok" });
  }
}

class WebSocketHub {
  private connections: Set<import("net").Socket> = new Set();

  register(sock: import("net").Socket): void {
    this.connections.add(sock);
    sock.on("close", () => this.connections.delete(sock));
  }

  publish(payload: string): void {
    const data = Buffer.from(payload);
    const header = Buffer.from([0x81, data.length]);
    this.connections.forEach((sock) => sock.write(Buffer.concat([header, data])));
  }
}

class WebSocketService {
  constructor(private hub: WebSocketHub) {}

  publish(ctx: Context): void {
    this.hub.publish(JSON.stringify(ctx.body.payload || {}));
    json(ctx.res, 200, { status: "ok" });
  }

  upgrade(req: IncomingMessage, socket: import("net").Socket): void {
    const key = req.headers["sec-websocket-key"] as string;
    if (!key) {
      socket.destroy();
      return;
    }
    const accept = crypto
      .createHash("sha1")
      .update(`${key}258EAFA5-E914-47DA-95CA-C5AB0DC85B11`)
      .digest("base64");
    socket.write(
      "HTTP/1.1 101 Switching Protocols\r\n" +
        "Upgrade: websocket\r\n" +
        "Connection: Upgrade\r\n" +
        `Sec-WebSocket-Accept: ${accept}\r\n\r\n`
    );
    this.hub.register(socket);
  }
}

class SchedulerEngine {
  private schedules: Record<string, { cron: string; payload: Record<string, unknown>; enabled: boolean; next: number }> = {};

  constructor(private queue: QueueBroker) {}

  create(cron: string, payload: Record<string, unknown>): string {
    const id = newId("sched");
    this.schedules[id] = { cron, payload, enabled: true, next: Date.now() + 5000 };
    return id;
  }

  setEnabled(id: string, enabled: boolean): void {
    if (this.schedules[id]) this.schedules[id].enabled = enabled;
  }

  start(): void {
    setInterval(() => {
      const now = Date.now();
      Object.entries(this.schedules).forEach(([id, sched]) => {
        if (sched.enabled && sched.next <= now) {
          this.queue.enqueue("scheduler", { schedule_id: id, payload: sched.payload });
          sched.next = now + 60000;
        }
      });
    }, 1000);
  }
}

class SchedulerService {
  constructor(private engine: SchedulerEngine) {}

  create(ctx: Context): void {
    const id = this.engine.create((ctx.body.cron as string) || "", (ctx.body.payload as Record<string, unknown>) || {});
    json(ctx.res, 201, { schedule_id: id });
  }

  enable(ctx: Context): void {
    this.engine.setEnabled(ctx.params.id, true);
    json(ctx.res, 200, { status: "ok" });
  }

  disable(ctx: Context): void {
    this.engine.setEnabled(ctx.params.id, false);
    json(ctx.res, 200, { status: "ok" });
  }
}

class WorkerFleet {
  private pool: Array<Record<string, unknown>> = [];

  constructor(private queue: QueueBroker, private payment: PaymentService, private workflow: WorkflowEngine, private logger: Logger) {}

  start(concurrency: number): void {
    for (let i = 0; i < concurrency; i += 1) {
      setInterval(() => {
        const msg = this.pool.shift();
        if (!msg) return;
        const queueName = msg.queue as string;
        if (queueName === "payments") this.payment.processCharge(msg.payload as Record<string, unknown>);
        if (queueName === "workflow") this.workflow.processTask(msg.payload as Record<string, unknown>);
        this.queue.ack(msg.id as string, true);
      }, 100);
    }
    setInterval(() => {
      ["payments", "workflow", "scheduler"].forEach((q) => {
        const msgs = this.queue.dequeue(q, 2);
        this.pool.push(...msgs);
      });
    }, 500);
  }
}

class WorkerService {
  register(ctx: Context): void {
    json(ctx.res, 200, { status: "ok" });
  }
  heartbeat(ctx: Context): void {
    json(ctx.res, 200, { status: "ok" });
  }
  taskResult(ctx: Context): void {
    json(ctx.res, 200, { status: "ok" });
  }
}

// ---------------------------
// API Gateway client
// ---------------------------

class HttpClient {
  constructor(private baseUrl: string) {}

  async request(method: string, path: string, body: Record<string, unknown>, headers: Record<string, string>): Promise<Record<string, unknown>> {
    const payload = JSON.stringify(body || {});
    return withRetry(() => {
      return new Promise((resolve, reject) => {
        const req = http.request(
          `${this.baseUrl}${path}`,
          {
            method,
            headers: { "Content-Type": "application/json", ...headers },
          },
          (res) => {
            const chunks: Buffer[] = [];
            res.on("data", (chunk) => chunks.push(chunk));
            res.on("end", () => {
              try {
                resolve(JSON.parse(Buffer.concat(chunks).toString("utf-8")));
              } catch (err) {
                reject(err);
              }
            });
          }
        );
        req.on("error", reject);
        req.write(payload);
        req.end();
      });
    }, 3);
  }
}

class AuthClient {
  constructor(private http: HttpClient) {}
  authorize(clientId: string, redirectUri: string, scope: string, userId: string, state = ""): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/auth/oauth/authorize", { client_id: clientId, redirect_uri: redirectUri, scope, user_id: userId, state }, {});
  }
  token(code: string, clientId: string, clientSecret: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/auth/oauth/token", { grant_type: "authorization_code", code, client_id: clientId, client_secret: clientSecret }, {});
  }
  refresh(refreshToken: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/auth/token/refresh", { refresh_token: refreshToken }, {});
  }
  enrollMfa(userId: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/auth/mfa/enroll", { user_id: userId }, {});
  }
  verifyMfa(userId: string, code: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/auth/mfa/verify", { user_id: userId, code }, {});
  }
}

class UserClient {
  constructor(private http: HttpClient) {}
  register(email: string, displayName: string): Promise<UserModel> {
    return this.http.request("POST", "/users/register", { email, display_name: displayName }, {}) as Promise<UserModel>;
  }
  get(userId: string): Promise<UserModel> {
    return this.http.request("GET", `/users/${userId}`, {}, {}) as Promise<UserModel>;
  }
  update(userId: string, displayName: string, status: string): Promise<UserModel> {
    return this.http.request("PATCH", `/users/${userId}`, { display_name: displayName, status }, {}) as Promise<UserModel>;
  }
}

class PaymentClient {
  constructor(private http: HttpClient) {}
  createIntent(userId: string, amount: number, currency: string, idempotencyKey: string): Promise<PaymentIntentModel> {
    return this.http.request("POST", "/payments/intents", { user_id: userId, amount, currency, idempotency_key: idempotencyKey }, {}) as Promise<PaymentIntentModel>;
  }
  getIntent(intentId: string): Promise<PaymentIntentModel> {
    return this.http.request("GET", `/payments/intents/${intentId}`, {}, {}) as Promise<PaymentIntentModel>;
  }
  captureIntent(intentId: string): Promise<PaymentIntentModel> {
    return this.http.request("POST", `/payments/intents/${intentId}/capture`, {}, {}) as Promise<PaymentIntentModel>;
  }
  refundIntent(intentId: string, amount: number): Promise<PaymentIntentModel> {
    return this.http.request("POST", `/payments/intents/${intentId}/refund`, { amount }, {}) as Promise<PaymentIntentModel>;
  }
}

class WorkflowClient {
  constructor(private http: HttpClient) {}
  register(name: string, definition: Record<string, unknown>): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/workflows", { name, definition }, {});
  }
  start(workflowId: string, payload: Record<string, unknown>): Promise<Record<string, unknown>> {
    return this.http.request("POST", `/workflows/${workflowId}/start`, { input: payload }, {});
  }
  getRun(runId: string): Promise<WorkflowRunModel> {
    return this.http.request("GET", `/workflows/runs/${runId}`, {}, {}) as Promise<WorkflowRunModel>;
  }
}

class QueueClient {
  constructor(private http: HttpClient) {}
  enqueue(name: string, payload: Record<string, unknown>): Promise<QueueMessageModel> {
    return this.http.request("POST", `/queues/${name}/enqueue`, { payload }, {}) as Promise<QueueMessageModel>;
  }
  dequeue(name: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", `/queues/${name}/dequeue`, {}, {});
  }
  ack(name: string, messageId: string, success: boolean): Promise<Record<string, unknown>> {
    return this.http.request("POST", `/queues/${name}/ack`, { message_id: messageId, success }, {});
  }
}

class StreamClient {
  constructor(private http: HttpClient) {}
  publish(topic: string, key: string, value: Record<string, unknown>): Promise<StreamRecordModel> {
    return this.http.request("POST", `/streams/${topic}/publish`, { key, value }, {}) as Promise<StreamRecordModel>;
  }
  consume(topic: string, group: string): Promise<Record<string, unknown>> {
    return this.http.request("GET", `/streams/${topic}/consume`, { group }, {});
  }
  commit(topic: string, group: string, partition: number, offset: number): Promise<Record<string, unknown>> {
    return this.http.request("POST", `/streams/${topic}/commit`, { group, partition, offset }, {});
  }
}

class CacheClient {
  constructor(private http: HttpClient) {}
  get(key: string): Promise<Record<string, unknown>> {
    return this.http.request("GET", `/cache/${key}`, {}, {});
  }
  put(key: string, value: string, ttlSeconds: number): Promise<Record<string, unknown>> {
    return this.http.request("PUT", `/cache/${key}`, { value, ttl_seconds: ttlSeconds }, {});
  }
  delete(key: string): Promise<Record<string, unknown>> {
    return this.http.request("DELETE", `/cache/${key}`, {}, {});
  }
}

class DatabaseClient {
  constructor(private http: HttpClient) {}
  query(sql: string, params: unknown[]): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/db/query", { sql, params }, {});
  }
  execute(sql: string, params: unknown[]): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/db/execute", { sql, params }, {});
  }
  documentGet(collection: string, key: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/db/document/get", { collection, key }, {});
  }
  documentPut(collection: string, key: string, document: Record<string, unknown>): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/db/document/put", { collection, key, document }, {});
  }
}

class WebSocketClient {
  constructor(private http: HttpClient) {}
  publish(payload: Record<string, unknown>): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/ws/publish", { payload }, {});
  }
}

class SchedulerClient {
  constructor(private http: HttpClient) {}
  create(cron: string, payload: Record<string, unknown>): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/schedules", { cron, payload }, {});
  }
  enable(id: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", `/schedules/${id}/enable`, {}, {});
  }
  disable(id: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", `/schedules/${id}/disable`, {}, {});
  }
}

class WorkerClient {
  constructor(private http: HttpClient) {}
  register(workerId: string, capabilities: Record<string, unknown>): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/workers/register", { worker_id: workerId, capabilities }, {});
  }
  heartbeat(workerId: string): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/workers/heartbeat", { worker_id: workerId }, {});
  }
  taskResult(taskId: string, status: string, output: Record<string, unknown>): Promise<Record<string, unknown>> {
    return this.http.request("POST", "/workers/task/result", { task_id: taskId, status, output }, {});
  }
}

class ApiGateway {
  private clients: Record<string, HttpClient>;

  constructor(cfg: Config) {
    this.clients = {
      auth: new HttpClient(`http://127.0.0.1:${cfg.authPort}`),
      user: new HttpClient(`http://127.0.0.1:${cfg.userPort}`),
      payment: new HttpClient(`http://127.0.0.1:${cfg.paymentPort}`),
      workflow: new HttpClient(`http://127.0.0.1:${cfg.workflowPort}`),
      queue: new HttpClient(`http://127.0.0.1:${cfg.queuePort}`),
      stream: new HttpClient(`http://127.0.0.1:${cfg.streamPort}`),
      cache: new HttpClient(`http://127.0.0.1:${cfg.cachePort}`),
      db: new HttpClient(`http://127.0.0.1:${cfg.dbPort}`),
      ws: new HttpClient(`http://127.0.0.1:${cfg.wsPort}`),
      scheduler: new HttpClient(`http://127.0.0.1:${cfg.schedulerPort}`),
      worker: new HttpClient(`http://127.0.0.1:${cfg.workerPort}`),
    };
  }

  async forward(service: string, ctx: Context): Promise<void> {
    const headers: Record<string, string> = {};
    if (ctx.correlationId) headers["Correlation-Id"] = ctx.correlationId;
    if (ctx.idempotencyKey) headers["Idempotency-Key"] = ctx.idempotencyKey;
    const resp = await this.clients[service].request(ctx.req.method || "GET", ctx.req.url || "/", ctx.body, headers);
    json(ctx.res, 200, resp);
  }
}

function buildRouter(logger: Logger, metrics: Metrics, limiter: RateLimiter, authSecret?: string): Router {
  const router = new Router();
  const base: Middleware[] = [middlewareLogging(logger, metrics), middlewareRateLimit(limiter)];
  const auth = authSecret ? middlewareAuth(authSecret) : null;

  const secured = auth ? [...base, auth] : base;
  router.add("GET", "/healthz", (ctx) => json(ctx.res, 200, { status: "ok" }), base);
  router.add("GET", "/readyz", (ctx) => json(ctx.res, 200, { status: "ready" }), base);
  router.add("GET", "/metrics", (ctx) => ctx.res.end(metrics.render()), base);
  router.add = ((method, path, handler, middleware = []) =>
    Router.prototype.add.call(router, method, path, handler, middleware.length ? middleware : secured)) as Router["add"];
  return router;
}

function startServer(port: number, router: Router, upgradeHandler?: (req: IncomingMessage, socket: import("net").Socket) => void): void {
  const server = http.createServer((req, res) => router.handle(req, res));
  if (upgradeHandler) {
    server.on("upgrade", (req, socket) => upgradeHandler(req, socket));
  }
  server.listen(port);
}

// ---------------------------
// Main
// ---------------------------

const cfg = loadConfig();
const metrics = new Metrics();
const limiter = new RateLimiter(cfg.rateLimitPerMin);
const isEnabled = (name: string): boolean => cfg.serviceOnly.length === 0 || cfg.serviceOnly.includes(name);

const auth = new AuthService(cfg);
auth.registerClient("platform_cli", "platform_secret");
const users = new UserService();
const queueBroker = new QueueBroker();
const streamBroker = new StreamBroker();
const idempotency = new IdempotencyStore();
const payments = new PaymentService(queueBroker, streamBroker, idempotency);
const workflows = new WorkflowEngine(queueBroker, streamBroker);
const cacheStore = new CacheStore();
const docs = new DocumentStore();
const db = new DatabaseService(docs);
const schedulerEngine = new SchedulerEngine(queueBroker);
const wsHub = new WebSocketHub();
const wsService = new WebSocketService(wsHub);
const workerFleet = new WorkerFleet(queueBroker, payments, workflows, new Logger("workers"));
if (isEnabled("worker")) {
  workerFleet.start(cfg.workerConcurrency);
}
if (isEnabled("scheduler")) {
  schedulerEngine.start();
}

const authRouter = buildRouter(new Logger("auth"), metrics, limiter);
authRouter.add("POST", "/auth/oauth/authorize", (ctx) => auth.authorize(ctx));
authRouter.add("POST", "/auth/oauth/token", (ctx) => auth.token(ctx));
authRouter.add("POST", "/auth/token/refresh", (ctx) => auth.refresh(ctx));
authRouter.add("POST", "/auth/mfa/enroll", (ctx) => auth.enrollMfa(ctx));
authRouter.add("POST", "/auth/mfa/verify", (ctx) => auth.verifyMfa(ctx));

const userRouter = buildRouter(new Logger("user"), metrics, limiter, cfg.jwtSecret);
userRouter.add("POST", "/users/register", (ctx) => users.register(ctx));
userRouter.add("GET", "/users/{id}", (ctx) => users.get(ctx));
userRouter.add("PATCH", "/users/{id}", (ctx) => users.update(ctx));

const paymentRouter = buildRouter(new Logger("payment"), metrics, limiter, cfg.jwtSecret);
paymentRouter.add("POST", "/payments/intents", (ctx) => payments.createIntent(ctx));
paymentRouter.add("GET", "/payments/intents/{id}", (ctx) => payments.getIntent(ctx));
paymentRouter.add("POST", "/payments/intents/{id}/capture", (ctx) => payments.captureIntent(ctx));
paymentRouter.add("POST", "/payments/intents/{id}/refund", (ctx) => payments.refundIntent(ctx));

const workflowRouter = buildRouter(new Logger("workflow"), metrics, limiter, cfg.jwtSecret);
workflowRouter.add("POST", "/workflows", (ctx) => workflows.register(ctx));
workflowRouter.add("POST", "/workflows/{id}/start", (ctx) => workflows.start(ctx));
workflowRouter.add("GET", "/workflows/runs/{run_id}", (ctx) => workflows.getRun(ctx));

const queueRouter = buildRouter(new Logger("queue"), metrics, limiter, cfg.jwtSecret);
const queueService = new QueueService(queueBroker);
queueRouter.add("POST", "/queues/{name}/enqueue", (ctx) => queueService.enqueue(ctx));
queueRouter.add("POST", "/queues/{name}/dequeue", (ctx) => queueService.dequeue(ctx));
queueRouter.add("POST", "/queues/{name}/ack", (ctx) => queueService.ack(ctx));

const streamRouter = buildRouter(new Logger("stream"), metrics, limiter, cfg.jwtSecret);
const streamService = new StreamService(streamBroker);
streamRouter.add("POST", "/streams/{topic}/publish", (ctx) => streamService.publish(ctx));
streamRouter.add("GET", "/streams/{topic}/consume", (ctx) => streamService.consume(ctx));
streamRouter.add("POST", "/streams/{topic}/commit", (ctx) => streamService.commit(ctx));

const cacheRouter = buildRouter(new Logger("cache"), metrics, limiter, cfg.jwtSecret);
const cacheService = new CacheService(cacheStore);
cacheRouter.add("GET", "/cache/{key}", (ctx) => cacheService.get(ctx));
cacheRouter.add("PUT", "/cache/{key}", (ctx) => cacheService.put(ctx));
cacheRouter.add("DELETE", "/cache/{key}", (ctx) => cacheService.delete(ctx));

const dbRouter = buildRouter(new Logger("db"), metrics, limiter, cfg.jwtSecret);
dbRouter.add("POST", "/db/query", (ctx) => db.query(ctx));
dbRouter.add("POST", "/db/execute", (ctx) => db.execute(ctx));
dbRouter.add("POST", "/db/document/get", (ctx) => db.documentGet(ctx));
dbRouter.add("POST", "/db/document/put", (ctx) => db.documentPut(ctx));

const schedulerRouter = buildRouter(new Logger("scheduler"), metrics, limiter, cfg.jwtSecret);
const schedulerService = new SchedulerService(schedulerEngine);
schedulerRouter.add("POST", "/schedules", (ctx) => schedulerService.create(ctx));
schedulerRouter.add("POST", "/schedules/{id}/enable", (ctx) => schedulerService.enable(ctx));
schedulerRouter.add("POST", "/schedules/{id}/disable", (ctx) => schedulerService.disable(ctx));

const workerRouter = buildRouter(new Logger("worker"), metrics, limiter, cfg.jwtSecret);
const workerService = new WorkerService();
workerRouter.add("POST", "/workers/register", (ctx) => workerService.register(ctx));
workerRouter.add("POST", "/workers/heartbeat", (ctx) => workerService.heartbeat(ctx));
workerRouter.add("POST", "/workers/task/result", (ctx) => workerService.taskResult(ctx));

const wsRouter = buildRouter(new Logger("ws"), metrics, limiter, cfg.jwtSecret);
wsRouter.add("POST", "/ws/publish", (ctx) => wsService.publish(ctx));

const gatewayRouter = buildRouter(new Logger("gateway"), metrics, limiter);
const gateway = new ApiGateway(cfg);
gatewayRouter.add("POST", "/auth/oauth/authorize", (ctx) => gateway.forward("auth", ctx));
gatewayRouter.add("POST", "/auth/oauth/token", (ctx) => gateway.forward("auth", ctx));
gatewayRouter.add("POST", "/auth/token/refresh", (ctx) => gateway.forward("auth", ctx));
gatewayRouter.add("POST", "/auth/mfa/enroll", (ctx) => gateway.forward("auth", ctx));
gatewayRouter.add("POST", "/auth/mfa/verify", (ctx) => gateway.forward("auth", ctx));
gatewayRouter.add("POST", "/users/register", (ctx) => gateway.forward("user", ctx));
gatewayRouter.add("GET", "/users/{id}", (ctx) => gateway.forward("user", ctx));
gatewayRouter.add("PATCH", "/users/{id}", (ctx) => gateway.forward("user", ctx));
gatewayRouter.add("POST", "/payments/intents", (ctx) => gateway.forward("payment", ctx));
gatewayRouter.add("GET", "/payments/intents/{id}", (ctx) => gateway.forward("payment", ctx));
gatewayRouter.add("POST", "/payments/intents/{id}/capture", (ctx) => gateway.forward("payment", ctx));
gatewayRouter.add("POST", "/payments/intents/{id}/refund", (ctx) => gateway.forward("payment", ctx));
gatewayRouter.add("POST", "/workflows", (ctx) => gateway.forward("workflow", ctx));
gatewayRouter.add("POST", "/workflows/{id}/start", (ctx) => gateway.forward("workflow", ctx));
gatewayRouter.add("GET", "/workflows/runs/{run_id}", (ctx) => gateway.forward("workflow", ctx));
gatewayRouter.add("POST", "/queues/{name}/enqueue", (ctx) => gateway.forward("queue", ctx));
gatewayRouter.add("POST", "/queues/{name}/dequeue", (ctx) => gateway.forward("queue", ctx));
gatewayRouter.add("POST", "/queues/{name}/ack", (ctx) => gateway.forward("queue", ctx));
gatewayRouter.add("POST", "/streams/{topic}/publish", (ctx) => gateway.forward("stream", ctx));
gatewayRouter.add("GET", "/streams/{topic}/consume", (ctx) => gateway.forward("stream", ctx));
gatewayRouter.add("POST", "/streams/{topic}/commit", (ctx) => gateway.forward("stream", ctx));
gatewayRouter.add("GET", "/cache/{key}", (ctx) => gateway.forward("cache", ctx));
gatewayRouter.add("PUT", "/cache/{key}", (ctx) => gateway.forward("cache", ctx));
gatewayRouter.add("DELETE", "/cache/{key}", (ctx) => gateway.forward("cache", ctx));
gatewayRouter.add("POST", "/db/query", (ctx) => gateway.forward("db", ctx));
gatewayRouter.add("POST", "/db/execute", (ctx) => gateway.forward("db", ctx));
gatewayRouter.add("POST", "/db/document/get", (ctx) => gateway.forward("db", ctx));
gatewayRouter.add("POST", "/db/document/put", (ctx) => gateway.forward("db", ctx));
gatewayRouter.add("POST", "/ws/publish", (ctx) => gateway.forward("ws", ctx));
gatewayRouter.add("POST", "/schedules", (ctx) => gateway.forward("scheduler", ctx));
gatewayRouter.add("POST", "/schedules/{id}/enable", (ctx) => gateway.forward("scheduler", ctx));
gatewayRouter.add("POST", "/schedules/{id}/disable", (ctx) => gateway.forward("scheduler", ctx));
gatewayRouter.add("POST", "/workers/register", (ctx) => gateway.forward("worker", ctx));
gatewayRouter.add("POST", "/workers/heartbeat", (ctx) => gateway.forward("worker", ctx));
gatewayRouter.add("POST", "/workers/task/result", (ctx) => gateway.forward("worker", ctx));

if (isEnabled("auth")) startServer(cfg.authPort, authRouter);
if (isEnabled("user")) startServer(cfg.userPort, userRouter);
if (isEnabled("payment")) startServer(cfg.paymentPort, paymentRouter);
if (isEnabled("workflow")) startServer(cfg.workflowPort, workflowRouter);
if (isEnabled("queue")) startServer(cfg.queuePort, queueRouter);
if (isEnabled("stream")) startServer(cfg.streamPort, streamRouter);
if (isEnabled("cache")) startServer(cfg.cachePort, cacheRouter);
if (isEnabled("db")) startServer(cfg.dbPort, dbRouter);
if (isEnabled("ws")) startServer(cfg.wsPort, wsRouter, (req, socket) => wsService.upgrade(req, socket));
if (isEnabled("scheduler")) startServer(cfg.schedulerPort, schedulerRouter);
if (isEnabled("worker")) startServer(cfg.workerPort, workerRouter);
if (isEnabled("gateway")) startServer(cfg.gatewayPort, gatewayRouter);
