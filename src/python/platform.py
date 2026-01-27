#!/usr/bin/env python3
import base64
import datetime as dt
import hashlib
import hmac
import json
import os
import queue
import random
import socket
import sqlite3
import threading
import time
import urllib.request
import uuid
from dataclasses import dataclass, asdict
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any, Callable, Dict, List, Optional, Tuple

# ---------------------------
# Configuration and utilities
# ---------------------------


class Config:
    def __init__(self) -> None:
        self.gateway_port = int(os.getenv("GATEWAY_PORT", "8080"))
        self.auth_port = int(os.getenv("AUTH_PORT", "8081"))
        self.user_port = int(os.getenv("USER_PORT", "8082"))
        self.payment_port = int(os.getenv("PAYMENT_PORT", "8083"))
        self.workflow_port = int(os.getenv("WORKFLOW_PORT", "8084"))
        self.queue_port = int(os.getenv("QUEUE_PORT", "8085"))
        self.stream_port = int(os.getenv("STREAM_PORT", "8086"))
        self.cache_port = int(os.getenv("CACHE_PORT", "8087"))
        self.db_port = int(os.getenv("DB_PORT", "8088"))
        self.ws_port = int(os.getenv("WS_PORT", "8089"))
        self.scheduler_port = int(os.getenv("SCHEDULER_PORT", "8090"))
        self.worker_port = int(os.getenv("WORKER_PORT", "8091"))
        self.jwt_secret = os.getenv("JWT_SECRET", "dev-secret")
        self.db_path = os.getenv("DB_PATH", "platform.db")
        self.rate_limit_per_min = int(os.getenv("RATE_LIMIT_PER_MIN", "600"))
        self.worker_concurrency = int(os.getenv("WORKER_CONCURRENCY", "8"))
        self.env = os.getenv("ENV", "dev")
        self.service_only = [s.strip() for s in os.getenv("SERVICE_ONLY", "").split(",") if s.strip()]


class Logger:
    def __init__(self, service: str) -> None:
        self.service = service

    def log(self, level: str, message: str, **fields: Any) -> None:
        entry = {
            "ts": dt.datetime.utcnow().isoformat() + "Z",
            "level": level,
            "service": self.service,
            "message": message,
            "fields": fields,
        }
        print(json.dumps(entry, sort_keys=True))

    def info(self, message: str, **fields: Any) -> None:
        self.log("INFO", message, **fields)

    def warn(self, message: str, **fields: Any) -> None:
        self.log("WARN", message, **fields)

    def error(self, message: str, **fields: Any) -> None:
        self.log("ERROR", message, **fields)


class Metrics:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.counters: Dict[str, int] = {}
        self.latencies: Dict[str, List[float]] = {}

    def inc(self, name: str, value: int = 1) -> None:
        with self._lock:
            self.counters[name] = self.counters.get(name, 0) + value

    def observe(self, name: str, value: float) -> None:
        with self._lock:
            self.latencies.setdefault(name, []).append(value)

    def render(self) -> str:
        lines: List[str] = []
        with self._lock:
            for name, value in self.counters.items():
                lines.append(f"# TYPE {name} counter")
                lines.append(f"{name} {value}")
            for name, values in self.latencies.items():
                if values:
                    avg = sum(values) / len(values)
                else:
                    avg = 0
                lines.append(f"# TYPE {name} gauge")
                lines.append(f"{name}_avg {avg}")
        return "\n".join(lines) + "\n"


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str, retryable: bool = False) -> None:
        super().__init__(message)
        self.status = status
        self.code = code
        self.message = message
        self.retryable = retryable


@dataclass
class UserModel:
    id: str
    email: str
    display_name: str
    status: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PaymentIntentModel:
    id: str
    user_id: str
    amount: int
    currency: str
    status: str
    idempotency_key: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class WorkflowRunModel:
    id: str
    workflow_id: str
    status: str
    current_step: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QueueMessageModel:
    id: str
    queue: str
    payload: Dict[str, Any]
    attempt: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class StreamRecordModel:
    topic: str
    partition: int
    offset: int
    key: str
    value: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CacheEntryModel:
    key: str
    value: str
    ttl_seconds: int

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def json_response(handler: BaseHTTPRequestHandler, status: int, body: Dict[str, Any]) -> None:
    payload = json.dumps(body).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json")
    handler.send_header("Content-Length", str(len(payload)))
    handler.end_headers()
    handler.wfile.write(payload)


def parse_body(handler: BaseHTTPRequestHandler) -> Dict[str, Any]:
    length = int(handler.headers.get("Content-Length", "0"))
    if length == 0:
        return {}
    raw = handler.rfile.read(length)
    try:
        return json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError:
        raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_json", "Invalid JSON payload")


def validate_required(body: Dict[str, Any], fields: List[str]) -> None:
    for field in fields:
        if body.get(field) in (None, ""):
            raise ApiError(HTTPStatus.BAD_REQUEST, "validation_error", f"Missing field: {field}")


def get_header(handler: BaseHTTPRequestHandler, name: str) -> str:
    return handler.headers.get(name, "")


def now_utc() -> float:
    return time.time()


def generate_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:12]}"


def with_retry(fn: Callable[[], Any], retries: int = 3, base_delay: float = 0.05) -> Any:
    attempt = 0
    while True:
        try:
            return fn()
        except Exception as exc:
            attempt += 1
            if attempt > retries:
                raise exc
            delay = base_delay * (2 ** (attempt - 1))
            jitter = random.random() * base_delay
            time.sleep(delay + jitter)


class RateLimiter:
    def __init__(self, limit_per_min: int) -> None:
        self.limit = limit_per_min
        self._lock = threading.Lock()
        self._tokens: Dict[str, Tuple[int, float]] = {}

    def allow(self, key: str) -> bool:
        now = now_utc()
        with self._lock:
            tokens, ts = self._tokens.get(key, (self.limit, now))
            elapsed = now - ts
            if elapsed >= 60:
                tokens = self.limit
                ts = now
            if tokens <= 0:
                self._tokens[key] = (tokens, ts)
                return False
            self._tokens[key] = (tokens - 1, ts)
            return True


class IdempotencyStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._store: Dict[str, Tuple[float, Dict[str, Any]]] = {}
        self.ttl = 3600

    def get(self, key: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None
            ts, value = entry
            if now_utc() - ts > self.ttl:
                del self._store[key]
                return None
            return value

    def set(self, key: str, value: Dict[str, Any]) -> None:
        with self._lock:
            self._store[key] = (now_utc(), value)


# ---------------------------
# HTTP routing and middleware
# ---------------------------


class RequestContext:
    def __init__(self, handler: BaseHTTPRequestHandler, body: Dict[str, Any], path_params: Dict[str, str]) -> None:
        self.handler = handler
        self.body = body
        self.path_params = path_params
        self.correlation_id = get_header(handler, "Correlation-Id") or generate_id("corr")
        self.idempotency_key = get_header(handler, "Idempotency-Key")
        self.start = now_utc()


HandlerFunc = Callable[[RequestContext], None]
MiddlewareFunc = Callable[[RequestContext, HandlerFunc], None]


class Router:
    def __init__(self) -> None:
        self.routes: List[Tuple[str, List[str], HandlerFunc, List[MiddlewareFunc]]] = []

    def add(self, method: str, path: str, handler: HandlerFunc, middleware: Optional[List[MiddlewareFunc]] = None) -> None:
        segments = [seg for seg in path.strip("/").split("/") if seg]
        self.routes.append((method.upper(), segments, handler, middleware or []))

    def match(self, method: str, path: str) -> Tuple[Optional[HandlerFunc], Dict[str, str], List[MiddlewareFunc]]:
        segments = [seg for seg in path.strip("/").split("/") if seg]
        for route_method, route_segs, handler, middleware in self.routes:
            if route_method != method.upper():
                continue
            if len(route_segs) != len(segments):
                continue
            params: Dict[str, str] = {}
            matched = True
            for rseg, seg in zip(route_segs, segments):
                if rseg.startswith("{") and rseg.endswith("}"):
                    params[rseg.strip("{}")] = seg
                elif rseg != seg:
                    matched = False
                    break
            if matched:
                return handler, params, middleware
        return None, {}, []


class ServiceHandler(BaseHTTPRequestHandler):
    router: Router = Router()
    metrics: Metrics = Metrics()
    logger: Logger = Logger("service")

    def _handle(self) -> None:
        handler, params, middleware = self.router.match(self.command, self.path.split("?")[0])
        if not handler:
            json_response(self, HTTPStatus.NOT_FOUND, {"error": {"code": "not_found", "message": "route not found"}})
            return
        try:
            body = parse_body(self)
            ctx = RequestContext(self, body, params)
            self._apply_middleware(ctx, handler, middleware)
        except ApiError as exc:
            json_response(
                self,
                exc.status,
                {"error": {"code": exc.code, "message": exc.message, "retryable": exc.retryable}},
            )
        except Exception as exc:
            self.logger.error("unhandled_error", error=str(exc))
            json_response(
                self,
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"error": {"code": "internal_error", "message": "internal error", "retryable": True}},
            )

    def _apply_middleware(self, ctx: RequestContext, handler: HandlerFunc, middleware: List[MiddlewareFunc]) -> None:
        def call_next(index: int, context: RequestContext) -> None:
            if index == len(middleware):
                handler(context)
                return
            mw = middleware[index]
            mw(context, lambda c=context: call_next(index + 1, c))

        call_next(0, ctx)

    def do_GET(self) -> None:
        self._handle()

    def do_POST(self) -> None:
        self._handle()

    def do_PUT(self) -> None:
        self._handle()

    def do_PATCH(self) -> None:
        self._handle()

    def do_DELETE(self) -> None:
        self._handle()

    def log_message(self, format: str, *args: Any) -> None:
        return


def middleware_logging(logger: Logger, metrics: Metrics) -> MiddlewareFunc:
    def apply(ctx: RequestContext, nxt: HandlerFunc) -> None:
        start = now_utc()
        logger.info("request_start", path=ctx.handler.path, method=ctx.handler.command, correlation_id=ctx.correlation_id)
        nxt(ctx)
        latency = now_utc() - start
        metrics.inc("http_requests_total")
        metrics.observe("http_request_latency_seconds", latency)
        logger.info("request_end", path=ctx.handler.path, latency_ms=int(latency * 1000))

    return apply


def middleware_rate_limit(rate_limiter: RateLimiter) -> MiddlewareFunc:
    def apply(ctx: RequestContext, nxt: HandlerFunc) -> None:
        key = ctx.handler.client_address[0]
        if not rate_limiter.allow(key):
            raise ApiError(HTTPStatus.TOO_MANY_REQUESTS, "rate_limited", "Too many requests", retryable=True)
        nxt(ctx)

    return apply


def middleware_auth(validate: Callable[[RequestContext], None]) -> MiddlewareFunc:
    def apply(ctx: RequestContext, nxt: HandlerFunc) -> None:
        validate(ctx)
        nxt(ctx)

    return apply


# ---------------------------
# Data stores and brokers
# ---------------------------


class CacheStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._data: Dict[str, Tuple[str, float]] = {}

    def get(self, key: str) -> Optional[str]:
        with self._lock:
            if key not in self._data:
                return None
            value, exp = self._data[key]
            if exp and now_utc() > exp:
                del self._data[key]
                return None
            return value

    def put(self, key: str, value: str, ttl_seconds: int) -> None:
        exp = now_utc() + ttl_seconds if ttl_seconds else 0
        with self._lock:
            self._data[key] = (value, exp)

    def delete(self, key: str) -> None:
        with self._lock:
            if key in self._data:
                del self._data[key]


class QueueBroker:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._queues: Dict[str, List[Dict[str, Any]]] = {}
        self._inflight: Dict[str, Dict[str, Any]] = {}

    def enqueue(self, queue_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        msg = {
            "id": generate_id("msg"),
            "queue": queue_name,
            "payload": payload,
            "attempt": 0,
            "visible_at": now_utc(),
        }
        with self._lock:
            self._queues.setdefault(queue_name, []).append(msg)
        return msg

    def dequeue(self, queue_name: str, max_messages: int = 1) -> List[Dict[str, Any]]:
        now = now_utc()
        msgs: List[Dict[str, Any]] = []
        with self._lock:
            queue = self._queues.get(queue_name, [])
            visible = [m for m in queue if m["visible_at"] <= now]
            for msg in visible[:max_messages]:
                msg["attempt"] += 1
                msg["visible_at"] = now + 30
                self._inflight[msg["id"]] = msg
                msgs.append(msg)
        return msgs

    def ack(self, message_id: str, success: bool) -> None:
        with self._lock:
            msg = self._inflight.pop(message_id, None)
            if not msg:
                return
            if not success:
                msg["visible_at"] = now_utc() + min(60 * msg["attempt"], 300)
                self._queues.setdefault(msg["queue"], []).append(msg)


class StreamBroker:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._topics: Dict[str, Dict[str, Any]] = {}
        self._offsets: Dict[str, Dict[Tuple[str, int], int]] = {}

    def create_topic(self, name: str, partitions: int = 3, retention_seconds: int = 86400) -> None:
        with self._lock:
            if name in self._topics:
                return
            self._topics[name] = {
                "partitions": partitions,
                "retention_seconds": retention_seconds,
                "records": {p: [] for p in range(partitions)},
                "offsets": {p: 0 for p in range(partitions)},
            }

    def publish(self, topic: str, key: str, value: str) -> Dict[str, Any]:
        with self._lock:
            if topic not in self._topics:
                self.create_topic(topic)
            data = self._topics[topic]
            partition = hash(key) % data["partitions"]
            offset = data["offsets"][partition]
            record = {"topic": topic, "partition": partition, "offset": offset, "key": key, "value": value}
            data["records"][partition].append(record)
            data["offsets"][partition] = offset + 1
            return record

    def consume(self, topic: str, group: str, max_records: int = 10) -> List[Dict[str, Any]]:
        with self._lock:
            if topic not in self._topics:
                return []
            data = self._topics[topic]
            group_offsets = self._offsets.setdefault(group, {})
            records: List[Dict[str, Any]] = []
            for partition in range(data["partitions"]):
                offset = group_offsets.get((topic, partition), 0)
                part_records = data["records"][partition]
                for record in part_records[offset : offset + max_records]:
                    records.append(record)
            return records

    def commit(self, topic: str, group: str, partition: int, offset: int) -> None:
        with self._lock:
            self._offsets.setdefault(group, {})[(topic, partition)] = offset


class DocumentStore:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._collections: Dict[str, Dict[str, Dict[str, Any]]] = {}

    def get(self, collection: str, key: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            return self._collections.get(collection, {}).get(key)

    def put(self, collection: str, key: str, doc: Dict[str, Any]) -> None:
        with self._lock:
            self._collections.setdefault(collection, {})[key] = doc


class WebSocketConnection:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.lock = threading.Lock()

    def send_text(self, payload: str) -> None:
        data = payload.encode("utf-8")
        length = len(data)
        header = bytes([0x81, length])
        with self.lock:
            self.sock.sendall(header + data)


class WebSocketHub:
    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._connections: List[WebSocketConnection] = []

    def register(self, conn: WebSocketConnection) -> None:
        with self._lock:
            self._connections.append(conn)

    def publish(self, payload: str) -> None:
        with self._lock:
            conns = list(self._connections)
        for conn in conns:
            try:
                conn.send_text(payload)
            except Exception:
                continue


class SchedulerEngine:
    def __init__(self, queue_broker: QueueBroker) -> None:
        self._lock = threading.Lock()
        self._schedules: Dict[str, Dict[str, Any]] = {}
        self._queue = queue_broker
        self._stop = threading.Event()

    def create_schedule(self, cron: str, payload: Dict[str, Any]) -> str:
        schedule_id = generate_id("sched")
        with self._lock:
            self._schedules[schedule_id] = {
                "cron": cron,
                "payload": payload,
                "enabled": True,
                "next_run": now_utc() + 5,
            }
        return schedule_id

    def set_enabled(self, schedule_id: str, enabled: bool) -> None:
        with self._lock:
            if schedule_id in self._schedules:
                self._schedules[schedule_id]["enabled"] = enabled

    def _tick(self) -> None:
        now = now_utc()
        with self._lock:
            schedules = list(self._schedules.items())
        for schedule_id, schedule in schedules:
            if not schedule["enabled"]:
                continue
            if schedule["next_run"] <= now:
                self._queue.enqueue("scheduler", {"schedule_id": schedule_id, "payload": schedule["payload"]})
                schedule["next_run"] = now + 60

    def start(self) -> None:
        def run() -> None:
            while not self._stop.is_set():
                self._tick()
                time.sleep(1)

        threading.Thread(target=run, daemon=True).start()


class WorkerFleet:
    def __init__(self, queue_broker: QueueBroker, payment_service: "PaymentService", workflow_engine: "WorkflowEngine", logger: Logger) -> None:
        self._queue = queue_broker
        self._payment = payment_service
        self._workflow = workflow_engine
        self._logger = logger
        self._workers: Dict[str, Dict[str, Any]] = {}
        self._stop = threading.Event()
        self._pool: queue.Queue = queue.Queue()

    def register(self, worker_id: str, capabilities: Dict[str, Any]) -> None:
        self._workers[worker_id] = {"capabilities": capabilities, "last_heartbeat": now_utc()}

    def heartbeat(self, worker_id: str) -> None:
        if worker_id in self._workers:
            self._workers[worker_id]["last_heartbeat"] = now_utc()

    def _execute_message(self, msg: Dict[str, Any]) -> None:
        queue_name = msg["queue"]
        try:
            if queue_name == "payments":
                self._payment.process_charge(msg["payload"])
            elif queue_name == "workflow":
                self._workflow.process_task(msg["payload"])
            elif queue_name == "scheduler":
                self._workflow.process_scheduled(msg["payload"])
            self._queue.ack(msg["id"], True)
        except Exception as exc:
            self._logger.error("worker_task_failed", error=str(exc))
            self._queue.ack(msg["id"], False)

    def start(self, concurrency: int) -> None:
        def worker_loop() -> None:
            while not self._stop.is_set():
                msg = self._pool.get()
                if msg is None:
                    return
                self._execute_message(msg)

        for _ in range(concurrency):
            threading.Thread(target=worker_loop, daemon=True).start()

        def dispatcher() -> None:
            while not self._stop.is_set():
                for queue_name in ["payments", "workflow", "scheduler"]:
                    messages = self._queue.dequeue(queue_name, max_messages=2)
                    for msg in messages:
                        self._pool.put(msg)
                time.sleep(0.5)

        threading.Thread(target=dispatcher, daemon=True).start()


# ---------------------------
# Authentication helpers
# ---------------------------


def jwt_encode(payload: Dict[str, Any], secret: str, expires_in: int) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    payload = dict(payload)
    payload["exp"] = int(now_utc()) + expires_in
    header_b64 = base64.urlsafe_b64encode(json.dumps(header).encode("utf-8")).rstrip(b"=")
    payload_b64 = base64.urlsafe_b64encode(json.dumps(payload).encode("utf-8")).rstrip(b"=")
    signing_input = header_b64 + b"." + payload_b64
    signature = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    sig_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=")
    return f"{header_b64.decode()}.{payload_b64.decode()}.{sig_b64.decode()}"


def jwt_decode(token: str, secret: str) -> Dict[str, Any]:
    parts = token.split(".")
    if len(parts) != 3:
        raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid_token", "Invalid token")
    header_b64, payload_b64, sig_b64 = parts
    signing_input = f"{header_b64}.{payload_b64}".encode("utf-8")
    expected = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    actual = base64.urlsafe_b64decode(sig_b64 + "==")
    if not hmac.compare_digest(expected, actual):
        raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid_token", "Signature mismatch")
    payload = json.loads(base64.urlsafe_b64decode(payload_b64 + "==").decode("utf-8"))
    if payload.get("exp", 0) < int(now_utc()):
        raise ApiError(HTTPStatus.UNAUTHORIZED, "expired_token", "Token expired")
    return payload


def totp(secret: str, timestamp: Optional[int] = None, step: int = 30) -> str:
    if timestamp is None:
        timestamp = int(now_utc())
    counter = int(timestamp / step)
    key = base64.b32decode(secret, casefold=True)
    msg = counter.to_bytes(8, "big")
    digest = hmac.new(key, msg, hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    code = (int.from_bytes(digest[offset : offset + 4], "big") & 0x7FFFFFFF) % 1000000
    return f"{code:06d}"


# ---------------------------
# Service implementations
# ---------------------------


class AuthService:
    def __init__(self, db: sqlite3.Connection, config: Config, logger: Logger) -> None:
        self.db = db
        self.config = config
        self.logger = logger
        self._clients: Dict[str, Dict[str, Any]] = {}
        self._auth_codes: Dict[str, Dict[str, Any]] = {}
        self._refresh_tokens: Dict[str, Dict[str, Any]] = {}
        self._mfa: Dict[str, Dict[str, Any]] = {}

    def register_client(self, client_id: str, secret: str, redirect_uris: str, scopes: str) -> None:
        self._clients[client_id] = {
            "client_id": client_id,
            "secret": secret,
            "redirect_uris": redirect_uris,
            "scopes": scopes,
        }

    def authorize(self, ctx: RequestContext) -> None:
        body = ctx.body
        validate_required(body, ["client_id", "redirect_uri", "user_id"])
        client_id = body.get("client_id", "")
        redirect_uri = body.get("redirect_uri", "")
        user_id = body.get("user_id", "")
        if client_id not in self._clients or user_id == "":
            raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid_client", "Invalid client")
        code = generate_id("code")
        self._auth_codes[code] = {"client_id": client_id, "user_id": user_id, "expires_at": now_utc() + 300}
        json_response(ctx.handler, HTTPStatus.OK, {"code": code, "state": body.get("state")})

    def token(self, ctx: RequestContext) -> None:
        body = ctx.body
        grant_type = body.get("grant_type", "authorization_code")
        if grant_type == "authorization_code":
            validate_required(body, ["code", "client_id", "client_secret"])
            code = body.get("code", "")
            client_id = body.get("client_id", "")
            client_secret = body.get("client_secret", "")
            client = self._clients.get(client_id)
            if not client or client["secret"] != client_secret:
                raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid_client", "Invalid client")
            auth_code = self._auth_codes.get(code)
            if not auth_code or auth_code["expires_at"] < now_utc():
                raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid_code", "Invalid authorization code")
            payload = {"sub": auth_code["user_id"], "scope": client["scopes"], "mfa": False}
            access = jwt_encode(payload, self.config.jwt_secret, expires_in=3600)
            refresh = generate_id("rft")
            self._refresh_tokens[refresh] = {"user_id": auth_code["user_id"], "expires_at": now_utc() + 86400}
            json_response(ctx.handler, HTTPStatus.OK, {"access_token": access, "refresh_token": refresh, "expires_in": 3600})
            return
        if grant_type == "client_credentials":
            client_id = body.get("client_id", "")
            client_secret = body.get("client_secret", "")
            client = self._clients.get(client_id)
            if not client or client["secret"] != client_secret:
                raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid_client", "Invalid client")
            payload = {"sub": client_id, "scope": client["scopes"], "mfa": True}
            access = jwt_encode(payload, self.config.jwt_secret, expires_in=3600)
            json_response(ctx.handler, HTTPStatus.OK, {"access_token": access, "refresh_token": "", "expires_in": 3600})
            return
        raise ApiError(HTTPStatus.BAD_REQUEST, "unsupported_grant", "Unsupported grant type")

    def refresh(self, ctx: RequestContext) -> None:
        body = ctx.body
        validate_required(body, ["refresh_token"])
        token = body.get("refresh_token", "")
        entry = self._refresh_tokens.get(token)
        if not entry or entry["expires_at"] < now_utc():
            raise ApiError(HTTPStatus.UNAUTHORIZED, "invalid_refresh", "Invalid refresh token")
        payload = {"sub": entry["user_id"], "scope": "basic", "mfa": True}
        access = jwt_encode(payload, self.config.jwt_secret, expires_in=3600)
        json_response(ctx.handler, HTTPStatus.OK, {"access_token": access, "refresh_token": token, "expires_in": 3600})

    def enroll_mfa(self, ctx: RequestContext) -> None:
        validate_required(ctx.body, ["user_id"])
        user_id = ctx.body.get("user_id", "")
        if user_id == "":
            raise ApiError(HTTPStatus.BAD_REQUEST, "missing_user", "user_id required")
        secret = base64.b32encode(os.urandom(10)).decode("utf-8")
        self._mfa[user_id] = {"secret": secret, "enabled": True}
        uri = f"otpauth://totp/Platform:{user_id}?secret={secret}&issuer=Platform"
        json_response(ctx.handler, HTTPStatus.OK, {"secret": secret, "uri": uri})

    def verify_mfa(self, ctx: RequestContext) -> None:
        validate_required(ctx.body, ["user_id", "code"])
        user_id = ctx.body.get("user_id", "")
        code = ctx.body.get("code", "")
        entry = self._mfa.get(user_id)
        if not entry:
            raise ApiError(HTTPStatus.NOT_FOUND, "mfa_not_enrolled", "MFA not enrolled")
        valid = totp(entry["secret"]) == code
        json_response(ctx.handler, HTTPStatus.OK, {"verified": valid})


class UserService:
    def __init__(self, db: sqlite3.Connection, logger: Logger) -> None:
        self.db = db
        self.logger = logger
        self._lock = threading.Lock()

    def register(self, ctx: RequestContext) -> None:
        validate_required(ctx.body, ["email", "display_name"])
        email = ctx.body.get("email", "")
        display_name = ctx.body.get("display_name", "")
        if "@" not in email or display_name == "":
            raise ApiError(HTTPStatus.BAD_REQUEST, "invalid_user", "Invalid user data")
        user_id = generate_id("usr")
        with self._lock:
            self.db.execute(
                "INSERT INTO users (id, email, display_name, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
                (user_id, email, display_name, "active", dt.datetime.utcnow(), dt.datetime.utcnow()),
            )
            self.db.commit()
        json_response(ctx.handler, HTTPStatus.CREATED, {"id": user_id, "email": email, "display_name": display_name, "status": "active"})

    def get_user(self, ctx: RequestContext) -> None:
        user_id = ctx.path_params.get("id", "")
        cur = self.db.execute("SELECT id, email, display_name, status FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if not row:
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "User not found")
        json_response(ctx.handler, HTTPStatus.OK, {"id": row[0], "email": row[1], "display_name": row[2], "status": row[3]})

    def update_user(self, ctx: RequestContext) -> None:
        user_id = ctx.path_params.get("id", "")
        display_name = ctx.body.get("display_name", "")
        status = ctx.body.get("status", "")
        with self._lock:
            self.db.execute(
                "UPDATE users SET display_name = ?, status = ?, updated_at = ? WHERE id = ?",
                (display_name, status, dt.datetime.utcnow(), user_id),
            )
            self.db.commit()
        self.get_user(ctx)


class PaymentService:
    def __init__(self, db: sqlite3.Connection, queue_broker: QueueBroker, stream_broker: StreamBroker, idempotency: IdempotencyStore) -> None:
        self.db = db
        self.queue = queue_broker
        self.stream = stream_broker
        self.idempotency = idempotency
        self._lock = threading.Lock()

    def create_intent(self, ctx: RequestContext) -> None:
        body = ctx.body
        validate_required(body, ["user_id", "amount", "currency"])
        key = ctx.idempotency_key or body.get("idempotency_key", "")
        if not key:
            raise ApiError(HTTPStatus.BAD_REQUEST, "missing_idempotency", "Idempotency-Key required")
        cached = self.idempotency.get(key)
        if cached:
            json_response(ctx.handler, HTTPStatus.OK, cached)
            return
        intent_id = generate_id("pi")
        with self._lock:
            self.db.execute(
                "INSERT INTO payment_intents (id, user_id, amount, currency, status, idempotency_key, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (intent_id, body.get("user_id"), body.get("amount"), body.get("currency"), "pending", key, dt.datetime.utcnow(), dt.datetime.utcnow()),
            )
            self.db.commit()
        self.queue.enqueue("payments", {"intent_id": intent_id})
        response = {"id": intent_id, "status": "pending"}
        self.idempotency.set(key, response)
        json_response(ctx.handler, HTTPStatus.ACCEPTED, response)

    def get_intent(self, ctx: RequestContext) -> None:
        intent_id = ctx.path_params.get("id", "")
        cur = self.db.execute("SELECT id, user_id, amount, currency, status, idempotency_key FROM payment_intents WHERE id = ?", (intent_id,))
        row = cur.fetchone()
        if not row:
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Payment intent not found")
        json_response(
            ctx.handler,
            HTTPStatus.OK,
            {"id": row[0], "user_id": row[1], "amount": row[2], "currency": row[3], "status": row[4], "idempotency_key": row[5]},
        )

    def capture_intent(self, ctx: RequestContext) -> None:
        intent_id = ctx.path_params.get("id", "")
        with self._lock:
            self.db.execute("UPDATE payment_intents SET status = ?, updated_at = ? WHERE id = ?", ("captured", dt.datetime.utcnow(), intent_id))
            self.db.commit()
        self.get_intent(ctx)

    def refund_intent(self, ctx: RequestContext) -> None:
        intent_id = ctx.path_params.get("id", "")
        amount = ctx.body.get("amount", 0)
        refund_id = generate_id("rf")
        with self._lock:
            self.db.execute(
                "INSERT INTO refunds (id, charge_id, amount, status, created_at) VALUES (?, ?, ?, ?, ?)",
                (refund_id, intent_id, amount, "pending", dt.datetime.utcnow()),
            )
            self.db.commit()
        self.get_intent(ctx)

    def process_charge(self, payload: Dict[str, Any]) -> None:
        intent_id = payload.get("intent_id")
        if not intent_id:
            return
        with self._lock:
            self.db.execute("UPDATE payment_intents SET status = ?, updated_at = ? WHERE id = ?", ("succeeded", dt.datetime.utcnow(), intent_id))
            charge_id = generate_id("ch")
            self.db.execute(
                "INSERT INTO charges (id, intent_id, status, processor_ref, created_at) VALUES (?, ?, ?, ?, ?)",
                (charge_id, intent_id, "succeeded", "processor_ref", dt.datetime.utcnow()),
            )
            self.db.commit()
        self.stream.publish("payments", intent_id, json.dumps({"intent_id": intent_id, "status": "succeeded"}))


class WorkflowEngine:
    def __init__(self, db: sqlite3.Connection, queue_broker: QueueBroker, stream_broker: StreamBroker) -> None:
        self.db = db
        self.queue = queue_broker
        self.stream = stream_broker
        self._lock = threading.Lock()

    def register(self, ctx: RequestContext) -> None:
        body = ctx.body
        validate_required(body, ["name"])
        wf_id = generate_id("wf")
        with self._lock:
            self.db.execute(
                "INSERT INTO workflows (id, name, version, definition, created_at) VALUES (?, ?, ?, ?, ?)",
                (wf_id, body.get("name", ""), 1, json.dumps(body.get("definition", {})), dt.datetime.utcnow()),
            )
            self.db.commit()
        json_response(ctx.handler, HTTPStatus.CREATED, {"workflow_id": wf_id})

    def start(self, ctx: RequestContext) -> None:
        wf_id = ctx.path_params.get("id", "")
        run_id = generate_id("wr")
        with self._lock:
            self.db.execute(
                "INSERT INTO workflow_runs (id, workflow_id, status, current_step, history, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (run_id, wf_id, "running", "start", "[]", dt.datetime.utcnow(), dt.datetime.utcnow()),
            )
            self.db.commit()
        self.queue.enqueue("workflow", {"run_id": run_id, "step": "start"})
        self.stream.publish("workflows", run_id, json.dumps({"run_id": run_id, "status": "running"}))
        json_response(ctx.handler, HTTPStatus.ACCEPTED, {"run_id": run_id, "status": "running"})

    def get_run(self, ctx: RequestContext) -> None:
        run_id = ctx.path_params.get("run_id", "")
        cur = self.db.execute("SELECT id, workflow_id, status, current_step FROM workflow_runs WHERE id = ?", (run_id,))
        row = cur.fetchone()
        if not row:
            raise ApiError(HTTPStatus.NOT_FOUND, "not_found", "Workflow run not found")
        json_response(ctx.handler, HTTPStatus.OK, {"id": row[0], "workflow_id": row[1], "status": row[2], "current_step": row[3]})

    def process_task(self, payload: Dict[str, Any]) -> None:
        run_id = payload.get("run_id")
        step = payload.get("step")
        if not run_id or not step:
            return
        with self._lock:
            self.db.execute(
                "UPDATE workflow_runs SET current_step = ?, updated_at = ? WHERE id = ?",
                (step, dt.datetime.utcnow(), run_id),
            )
            self.db.commit()
        if step == "start":
            self.queue.enqueue("workflow", {"run_id": run_id, "step": "complete"})
        elif step == "complete":
            with self._lock:
                self.db.execute(
                    "UPDATE workflow_runs SET status = ?, updated_at = ? WHERE id = ?",
                    ("completed", dt.datetime.utcnow(), run_id),
                )
                self.db.commit()
            self.stream.publish("workflows", run_id, json.dumps({"run_id": run_id, "status": "completed"}))

    def process_scheduled(self, payload: Dict[str, Any]) -> None:
        schedule_id = payload.get("schedule_id")
        self.stream.publish("schedules", schedule_id or "unknown", json.dumps(payload))


class CacheService:
    def __init__(self, cache: CacheStore) -> None:
        self.cache = cache

    def get(self, ctx: RequestContext) -> None:
        key = ctx.path_params.get("key", "")
        value = self.cache.get(key)
        if value is None:
            raise ApiError(HTTPStatus.NOT_FOUND, "cache_miss", "Cache miss")
        json_response(ctx.handler, HTTPStatus.OK, {"key": key, "value": value})

    def put(self, ctx: RequestContext) -> None:
        key = ctx.path_params.get("key", "")
        value = ctx.body.get("value", "")
        ttl = int(ctx.body.get("ttl_seconds", 60))
        self.cache.put(key, value, ttl)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})

    def delete(self, ctx: RequestContext) -> None:
        key = ctx.path_params.get("key", "")
        self.cache.delete(key)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})


class DatabaseService:
    def __init__(self, db: sqlite3.Connection, docs: DocumentStore) -> None:
        self.db = db
        self.docs = docs
        self._lock = threading.Lock()

    def query(self, ctx: RequestContext) -> None:
        sql = ctx.body.get("sql", "")
        params = ctx.body.get("params", [])
        with self._lock:
            cur = self.db.execute(sql, params)
            rows = [dict(zip([c[0] for c in cur.description], row)) for row in cur.fetchall()]
        json_response(ctx.handler, HTTPStatus.OK, {"rows": rows})

    def execute(self, ctx: RequestContext) -> None:
        sql = ctx.body.get("sql", "")
        params = ctx.body.get("params", [])
        with self._lock:
            self.db.execute(sql, params)
            self.db.commit()
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})

    def document_get(self, ctx: RequestContext) -> None:
        collection = ctx.body.get("collection", "")
        key = ctx.body.get("key", "")
        doc = self.docs.get(collection, key)
        if not doc:
            raise ApiError(HTTPStatus.NOT_FOUND, "doc_not_found", "Document not found")
        json_response(ctx.handler, HTTPStatus.OK, {"document": doc})

    def document_put(self, ctx: RequestContext) -> None:
        collection = ctx.body.get("collection", "")
        key = ctx.body.get("key", "")
        document = ctx.body.get("document", {})
        self.docs.put(collection, key, document)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})


class QueueService:
    def __init__(self, broker: QueueBroker) -> None:
        self.broker = broker

    def enqueue(self, ctx: RequestContext) -> None:
        name = ctx.path_params.get("name", "")
        payload = ctx.body.get("payload", {})
        msg = self.broker.enqueue(name, payload)
        json_response(ctx.handler, HTTPStatus.CREATED, msg)

    def dequeue(self, ctx: RequestContext) -> None:
        name = ctx.path_params.get("name", "")
        msgs = self.broker.dequeue(name, max_messages=1)
        json_response(ctx.handler, HTTPStatus.OK, {"messages": msgs})

    def ack(self, ctx: RequestContext) -> None:
        msg_id = ctx.body.get("message_id", "")
        success = bool(ctx.body.get("success", True))
        self.broker.ack(msg_id, success)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})


class StreamService:
    def __init__(self, broker: StreamBroker) -> None:
        self.broker = broker

    def publish(self, ctx: RequestContext) -> None:
        topic = ctx.path_params.get("topic", "")
        key = ctx.body.get("key", "")
        value = json.dumps(ctx.body.get("value", {}))
        record = self.broker.publish(topic, key, value)
        json_response(ctx.handler, HTTPStatus.OK, record)

    def consume(self, ctx: RequestContext) -> None:
        topic = ctx.path_params.get("topic", "")
        group = ctx.body.get("group", "default")
        records = self.broker.consume(topic, group)
        json_response(ctx.handler, HTTPStatus.OK, {"records": records})

    def commit(self, ctx: RequestContext) -> None:
        topic = ctx.path_params.get("topic", "")
        group = ctx.body.get("group", "default")
        partition = int(ctx.body.get("partition", 0))
        offset = int(ctx.body.get("offset", 0))
        self.broker.commit(topic, group, partition, offset)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})


class WebSocketService:
    def __init__(self, hub: WebSocketHub) -> None:
        self.hub = hub

    def publish(self, ctx: RequestContext) -> None:
        payload = json.dumps(ctx.body.get("payload", {}))
        self.hub.publish(payload)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})


class SchedulerService:
    def __init__(self, scheduler: SchedulerEngine) -> None:
        self.scheduler = scheduler

    def create(self, ctx: RequestContext) -> None:
        validate_required(ctx.body, ["cron"])
        cron = ctx.body.get("cron", "")
        payload = ctx.body.get("payload", {})
        schedule_id = self.scheduler.create_schedule(cron, payload)
        json_response(ctx.handler, HTTPStatus.CREATED, {"schedule_id": schedule_id})

    def enable(self, ctx: RequestContext) -> None:
        schedule_id = ctx.path_params.get("id", "")
        self.scheduler.set_enabled(schedule_id, True)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})

    def disable(self, ctx: RequestContext) -> None:
        schedule_id = ctx.path_params.get("id", "")
        self.scheduler.set_enabled(schedule_id, False)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})


class WorkerService:
    def __init__(self, worker: WorkerFleet) -> None:
        self.worker = worker

    def register(self, ctx: RequestContext) -> None:
        worker_id = ctx.body.get("worker_id", "")
        capabilities = ctx.body.get("capabilities", {})
        self.worker.register(worker_id, capabilities)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})

    def heartbeat(self, ctx: RequestContext) -> None:
        worker_id = ctx.body.get("worker_id", "")
        self.worker.heartbeat(worker_id)
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})

    def task_result(self, ctx: RequestContext) -> None:
        json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"})


# ---------------------------
# API Gateway
# ---------------------------


class HttpClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def request(self, method: str, path: str, body: Dict[str, Any], headers: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
        url = self.base_url + path
        payload = json.dumps(body).encode("utf-8")
        req = urllib.request.Request(url, data=payload if method != "GET" else None, method=method)
        req.add_header("Content-Type", "application/json")
        for k, v in (headers or {}).items():
            req.add_header(k, v)

        def do() -> Dict[str, Any]:
            with urllib.request.urlopen(req, timeout=3) as resp:
                return json.loads(resp.read().decode("utf-8"))

        return with_retry(do)


class AuthClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def authorize(self, client_id: str, redirect_uri: str, scope: str, user_id: str, state: str = "") -> Dict[str, Any]:
        return self.http.request("POST", "/auth/oauth/authorize", {"client_id": client_id, "redirect_uri": redirect_uri, "scope": scope, "user_id": user_id, "state": state})

    def token(self, code: str, client_id: str, client_secret: str) -> Dict[str, Any]:
        return self.http.request("POST", "/auth/oauth/token", {"grant_type": "authorization_code", "code": code, "client_id": client_id, "client_secret": client_secret})

    def refresh(self, refresh_token: str) -> Dict[str, Any]:
        return self.http.request("POST", "/auth/token/refresh", {"refresh_token": refresh_token})

    def enroll_mfa(self, user_id: str) -> Dict[str, Any]:
        return self.http.request("POST", "/auth/mfa/enroll", {"user_id": user_id})

    def verify_mfa(self, user_id: str, code: str) -> Dict[str, Any]:
        return self.http.request("POST", "/auth/mfa/verify", {"user_id": user_id, "code": code})


class UserClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def register(self, email: str, display_name: str) -> Dict[str, Any]:
        return self.http.request("POST", "/users/register", {"email": email, "display_name": display_name})

    def get(self, user_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/users/{user_id}", {})

    def update(self, user_id: str, display_name: str, status: str) -> Dict[str, Any]:
        return self.http.request("PATCH", f"/users/{user_id}", {"display_name": display_name, "status": status})


class PaymentClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def create_intent(self, user_id: str, amount: int, currency: str, idempotency_key: str) -> Dict[str, Any]:
        return self.http.request("POST", "/payments/intents", {"user_id": user_id, "amount": amount, "currency": currency, "idempotency_key": idempotency_key})

    def get_intent(self, intent_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/payments/intents/{intent_id}", {})

    def capture_intent(self, intent_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/payments/intents/{intent_id}/capture", {})

    def refund_intent(self, intent_id: str, amount: int) -> Dict[str, Any]:
        return self.http.request("POST", f"/payments/intents/{intent_id}/refund", {"amount": amount})


class WorkflowClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def register(self, name: str, definition: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/workflows", {"name": name, "definition": definition})

    def start(self, workflow_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", f"/workflows/{workflow_id}/start", {"input": payload})

    def get_run(self, run_id: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/workflows/runs/{run_id}", {})


class QueueClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def enqueue(self, name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", f"/queues/{name}/enqueue", {"payload": payload})

    def dequeue(self, name: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/queues/{name}/dequeue", {})

    def ack(self, name: str, message_id: str, success: bool) -> Dict[str, Any]:
        return self.http.request("POST", f"/queues/{name}/ack", {"message_id": message_id, "success": success})


class StreamClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def publish(self, topic: str, key: str, value: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", f"/streams/{topic}/publish", {"key": key, "value": value})

    def consume(self, topic: str, group: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/streams/{topic}/consume", {"group": group})

    def commit(self, topic: str, group: str, partition: int, offset: int) -> Dict[str, Any]:
        return self.http.request("POST", f"/streams/{topic}/commit", {"group": group, "partition": partition, "offset": offset})


class CacheClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def get(self, key: str) -> Dict[str, Any]:
        return self.http.request("GET", f"/cache/{key}", {})

    def put(self, key: str, value: str, ttl_seconds: int) -> Dict[str, Any]:
        return self.http.request("PUT", f"/cache/{key}", {"value": value, "ttl_seconds": ttl_seconds})

    def delete(self, key: str) -> Dict[str, Any]:
        return self.http.request("DELETE", f"/cache/{key}", {})


class DatabaseClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def query(self, sql: str, params: List[Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/db/query", {"sql": sql, "params": params})

    def execute(self, sql: str, params: List[Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/db/execute", {"sql": sql, "params": params})

    def document_get(self, collection: str, key: str) -> Dict[str, Any]:
        return self.http.request("POST", "/db/document/get", {"collection": collection, "key": key})

    def document_put(self, collection: str, key: str, document: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/db/document/put", {"collection": collection, "key": key, "document": document})


class WebSocketClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def publish(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/ws/publish", {"payload": payload})


class SchedulerClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def create(self, cron: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/schedules", {"cron": cron, "payload": payload})

    def enable(self, schedule_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/schedules/{schedule_id}/enable", {})

    def disable(self, schedule_id: str) -> Dict[str, Any]:
        return self.http.request("POST", f"/schedules/{schedule_id}/disable", {})


class WorkerClient:
    def __init__(self, base_url: str) -> None:
        self.http = HttpClient(base_url)

    def register(self, worker_id: str, capabilities: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/workers/register", {"worker_id": worker_id, "capabilities": capabilities})

    def heartbeat(self, worker_id: str) -> Dict[str, Any]:
        return self.http.request("POST", "/workers/heartbeat", {"worker_id": worker_id})

    def task_result(self, task_id: str, status: str, output: Dict[str, Any]) -> Dict[str, Any]:
        return self.http.request("POST", "/workers/task/result", {"task_id": task_id, "status": status, "output": output})


class ApiGateway:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.clients = {
            "auth": HttpClient(f"http://127.0.0.1:{config.auth_port}"),
            "user": HttpClient(f"http://127.0.0.1:{config.user_port}"),
            "payment": HttpClient(f"http://127.0.0.1:{config.payment_port}"),
            "workflow": HttpClient(f"http://127.0.0.1:{config.workflow_port}"),
            "queue": HttpClient(f"http://127.0.0.1:{config.queue_port}"),
            "stream": HttpClient(f"http://127.0.0.1:{config.stream_port}"),
            "cache": HttpClient(f"http://127.0.0.1:{config.cache_port}"),
            "db": HttpClient(f"http://127.0.0.1:{config.db_port}"),
            "ws": HttpClient(f"http://127.0.0.1:{config.ws_port}"),
            "scheduler": HttpClient(f"http://127.0.0.1:{config.scheduler_port}"),
            "worker": HttpClient(f"http://127.0.0.1:{config.worker_port}"),
        }

    def forward(self, service: str, ctx: RequestContext) -> None:
        client = self.clients[service]
        body = ctx.body
        headers = {"Correlation-Id": ctx.correlation_id}
        if ctx.idempotency_key:
            headers["Idempotency-Key"] = ctx.idempotency_key
        resp = client.request(ctx.handler.command, ctx.handler.path, body, headers=headers)
        json_response(ctx.handler, HTTPStatus.OK, resp)


# ---------------------------
# Platform assembly
# ---------------------------


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
  id TEXT PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  display_name TEXT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS payment_intents (
  id TEXT PRIMARY KEY,
  user_id TEXT NOT NULL,
  amount BIGINT NOT NULL,
  currency TEXT NOT NULL,
  status TEXT NOT NULL,
  idempotency_key TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS charges (
  id TEXT PRIMARY KEY,
  intent_id TEXT NOT NULL,
  status TEXT NOT NULL,
  processor_ref TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS refunds (
  id TEXT PRIMARY KEY,
  charge_id TEXT NOT NULL,
  amount BIGINT NOT NULL,
  status TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS workflows (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  version INTEGER NOT NULL,
  definition TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL
);
CREATE TABLE IF NOT EXISTS workflow_runs (
  id TEXT PRIMARY KEY,
  workflow_id TEXT NOT NULL,
  status TEXT NOT NULL,
  current_step TEXT NOT NULL,
  history TEXT NOT NULL,
  created_at TIMESTAMP NOT NULL,
  updated_at TIMESTAMP NOT NULL
);
"""


def init_db(path: str) -> sqlite3.Connection:
    db = sqlite3.connect(path, check_same_thread=False)
    for stmt in SCHEMA_SQL.strip().split(";"):
        if stmt.strip():
            db.execute(stmt)
    db.commit()
    return db


def validate_jwt(config: Config) -> Callable[[RequestContext], None]:
    def apply(ctx: RequestContext) -> None:
        token = get_header(ctx.handler, "Authorization").replace("Bearer ", "")
        if not token:
            raise ApiError(HTTPStatus.UNAUTHORIZED, "missing_token", "Missing Bearer token")
        jwt_decode(token, config.jwt_secret)

    return apply


def build_router_for_service(service_name: str, logger: Logger, metrics: Metrics, rate_limiter: RateLimiter, auth: Optional[Callable[[RequestContext], None]]) -> Router:
    router = Router()
    base_middleware = [middleware_logging(logger, metrics), middleware_rate_limit(rate_limiter)]
    if auth:
        base_middleware.append(middleware_auth(auth))

    def add(method: str, path: str, handler: HandlerFunc) -> None:
        router.add(method, path, handler, base_middleware)

    def add_public(method: str, path: str, handler: HandlerFunc) -> None:
        router.add(method, path, handler, [middleware_logging(logger, metrics), middleware_rate_limit(rate_limiter)])

    # health and metrics
    add_public("GET", "/healthz", lambda ctx: json_response(ctx.handler, HTTPStatus.OK, {"status": "ok"}))
    add_public("GET", "/readyz", lambda ctx: json_response(ctx.handler, HTTPStatus.OK, {"status": "ready"}))
    add_public("GET", "/metrics", lambda ctx: ctx.handler.wfile.write(metrics.render().encode("utf-8")))
    return router


def start_server(port: int, router: Router, logger: Logger, metrics: Metrics) -> None:
    handler_cls = type("Handler", (ServiceHandler,), {})
    handler_cls.router = router
    handler_cls.logger = logger
    handler_cls.metrics = metrics
    server = ThreadingHTTPServer(("0.0.0.0", port), handler_cls)
    threading.Thread(target=server.serve_forever, daemon=True).start()


def main() -> None:
    config = Config()
    rate_limiter = RateLimiter(config.rate_limit_per_min)
    metrics = Metrics()

    db = init_db(config.db_path)
    cache = CacheStore()
    docs = DocumentStore()
    queue_broker = QueueBroker()
    stream_broker = StreamBroker()
    idempotency = IdempotencyStore()
    ws_hub = WebSocketHub()

    auth_logger = Logger("auth")
    auth_service = AuthService(db, config, auth_logger)
    auth_service.register_client("platform_cli", "platform_secret", "http://localhost", "basic")

    user_service = UserService(db, Logger("user"))
    payment_service = PaymentService(db, queue_broker, stream_broker, idempotency)
    workflow_engine = WorkflowEngine(db, queue_broker, stream_broker)
    cache_service = CacheService(cache)
    db_service = DatabaseService(db, docs)
    queue_service = QueueService(queue_broker)
    stream_service = StreamService(stream_broker)
    ws_service = WebSocketService(ws_hub)
    scheduler_engine = SchedulerEngine(queue_broker)
    worker_fleet = WorkerFleet(queue_broker, payment_service, workflow_engine, Logger("workers"))

    def is_enabled(name: str) -> bool:
        return not config.service_only or name in config.service_only

    if is_enabled("scheduler"):
        scheduler_engine.start()
    if is_enabled("worker"):
        worker_fleet.start(config.worker_concurrency)
    scheduler_service = SchedulerService(scheduler_engine)
    worker_service = WorkerService(worker_fleet)

    jwt_validator = validate_jwt(config)

    # Auth service router
    auth_router = build_router_for_service("auth", auth_logger, metrics, rate_limiter, None)
    auth_router.add("POST", "/auth/oauth/authorize", auth_service.authorize)
    auth_router.add("POST", "/auth/oauth/token", auth_service.token)
    auth_router.add("POST", "/auth/token/refresh", auth_service.refresh)
    auth_router.add("POST", "/auth/mfa/enroll", auth_service.enroll_mfa)
    auth_router.add("POST", "/auth/mfa/verify", auth_service.verify_mfa)

    # User service router
    user_router = build_router_for_service("user", Logger("user"), metrics, rate_limiter, jwt_validator)
    user_router.add("POST", "/users/register", user_service.register)
    user_router.add("GET", "/users/{id}", user_service.get_user)
    user_router.add("PATCH", "/users/{id}", user_service.update_user)

    # Payment service router
    payment_router = build_router_for_service("payment", Logger("payment"), metrics, rate_limiter, jwt_validator)
    payment_router.add("POST", "/payments/intents", payment_service.create_intent)
    payment_router.add("GET", "/payments/intents/{id}", payment_service.get_intent)
    payment_router.add("POST", "/payments/intents/{id}/capture", payment_service.capture_intent)
    payment_router.add("POST", "/payments/intents/{id}/refund", payment_service.refund_intent)

    # Workflow router
    workflow_router = build_router_for_service("workflow", Logger("workflow"), metrics, rate_limiter, jwt_validator)
    workflow_router.add("POST", "/workflows", workflow_engine.register)
    workflow_router.add("POST", "/workflows/{id}/start", workflow_engine.start)
    workflow_router.add("GET", "/workflows/runs/{run_id}", workflow_engine.get_run)

    # Queue router
    queue_router = build_router_for_service("queue", Logger("queue"), metrics, rate_limiter, jwt_validator)
    queue_router.add("POST", "/queues/{name}/enqueue", queue_service.enqueue)
    queue_router.add("POST", "/queues/{name}/dequeue", queue_service.dequeue)
    queue_router.add("POST", "/queues/{name}/ack", queue_service.ack)

    # Stream router
    stream_router = build_router_for_service("stream", Logger("stream"), metrics, rate_limiter, jwt_validator)
    stream_router.add("POST", "/streams/{topic}/publish", stream_service.publish)
    stream_router.add("GET", "/streams/{topic}/consume", stream_service.consume)
    stream_router.add("POST", "/streams/{topic}/commit", stream_service.commit)

    # Cache router
    cache_router = build_router_for_service("cache", Logger("cache"), metrics, rate_limiter, jwt_validator)
    cache_router.add("GET", "/cache/{key}", cache_service.get)
    cache_router.add("PUT", "/cache/{key}", cache_service.put)
    cache_router.add("DELETE", "/cache/{key}", cache_service.delete)

    # Database router
    db_router = build_router_for_service("db", Logger("db"), metrics, rate_limiter, jwt_validator)
    db_router.add("POST", "/db/query", db_service.query)
    db_router.add("POST", "/db/execute", db_service.execute)
    db_router.add("POST", "/db/document/get", db_service.document_get)
    db_router.add("POST", "/db/document/put", db_service.document_put)

    # WebSocket router (HTTP publish)
    ws_router = build_router_for_service("ws", Logger("ws"), metrics, rate_limiter, jwt_validator)
    ws_router.add("POST", "/ws/publish", ws_service.publish)

    # Scheduler router
    scheduler_router = build_router_for_service("scheduler", Logger("scheduler"), metrics, rate_limiter, jwt_validator)
    scheduler_router.add("POST", "/schedules", scheduler_service.create)
    scheduler_router.add("POST", "/schedules/{id}/enable", scheduler_service.enable)
    scheduler_router.add("POST", "/schedules/{id}/disable", scheduler_service.disable)

    # Worker router
    worker_router = build_router_for_service("worker", Logger("worker"), metrics, rate_limiter, jwt_validator)
    worker_router.add("POST", "/workers/register", worker_service.register)
    worker_router.add("POST", "/workers/heartbeat", worker_service.heartbeat)
    worker_router.add("POST", "/workers/task/result", worker_service.task_result)

    # Gateway router
    gateway_router = build_router_for_service("gateway", Logger("gateway"), metrics, rate_limiter, None)
    gateway = ApiGateway(config)
    gateway_router.add("POST", "/auth/oauth/authorize", lambda ctx: gateway.forward("auth", ctx))
    gateway_router.add("POST", "/auth/oauth/token", lambda ctx: gateway.forward("auth", ctx))
    gateway_router.add("POST", "/auth/token/refresh", lambda ctx: gateway.forward("auth", ctx))
    gateway_router.add("POST", "/auth/mfa/enroll", lambda ctx: gateway.forward("auth", ctx))
    gateway_router.add("POST", "/auth/mfa/verify", lambda ctx: gateway.forward("auth", ctx))
    gateway_router.add("POST", "/users/register", lambda ctx: gateway.forward("user", ctx))
    gateway_router.add("GET", "/users/{id}", lambda ctx: gateway.forward("user", ctx))
    gateway_router.add("PATCH", "/users/{id}", lambda ctx: gateway.forward("user", ctx))
    gateway_router.add("POST", "/payments/intents", lambda ctx: gateway.forward("payment", ctx))
    gateway_router.add("GET", "/payments/intents/{id}", lambda ctx: gateway.forward("payment", ctx))
    gateway_router.add("POST", "/payments/intents/{id}/capture", lambda ctx: gateway.forward("payment", ctx))
    gateway_router.add("POST", "/payments/intents/{id}/refund", lambda ctx: gateway.forward("payment", ctx))
    gateway_router.add("POST", "/workflows", lambda ctx: gateway.forward("workflow", ctx))
    gateway_router.add("POST", "/workflows/{id}/start", lambda ctx: gateway.forward("workflow", ctx))
    gateway_router.add("GET", "/workflows/runs/{run_id}", lambda ctx: gateway.forward("workflow", ctx))
    gateway_router.add("POST", "/queues/{name}/enqueue", lambda ctx: gateway.forward("queue", ctx))
    gateway_router.add("POST", "/queues/{name}/dequeue", lambda ctx: gateway.forward("queue", ctx))
    gateway_router.add("POST", "/queues/{name}/ack", lambda ctx: gateway.forward("queue", ctx))
    gateway_router.add("POST", "/streams/{topic}/publish", lambda ctx: gateway.forward("stream", ctx))
    gateway_router.add("GET", "/streams/{topic}/consume", lambda ctx: gateway.forward("stream", ctx))
    gateway_router.add("POST", "/streams/{topic}/commit", lambda ctx: gateway.forward("stream", ctx))
    gateway_router.add("GET", "/cache/{key}", lambda ctx: gateway.forward("cache", ctx))
    gateway_router.add("PUT", "/cache/{key}", lambda ctx: gateway.forward("cache", ctx))
    gateway_router.add("DELETE", "/cache/{key}", lambda ctx: gateway.forward("cache", ctx))
    gateway_router.add("POST", "/db/query", lambda ctx: gateway.forward("db", ctx))
    gateway_router.add("POST", "/db/execute", lambda ctx: gateway.forward("db", ctx))
    gateway_router.add("POST", "/db/document/get", lambda ctx: gateway.forward("db", ctx))
    gateway_router.add("POST", "/db/document/put", lambda ctx: gateway.forward("db", ctx))
    gateway_router.add("POST", "/ws/publish", lambda ctx: gateway.forward("ws", ctx))
    gateway_router.add("POST", "/schedules", lambda ctx: gateway.forward("scheduler", ctx))
    gateway_router.add("POST", "/schedules/{id}/enable", lambda ctx: gateway.forward("scheduler", ctx))
    gateway_router.add("POST", "/schedules/{id}/disable", lambda ctx: gateway.forward("scheduler", ctx))
    gateway_router.add("POST", "/workers/register", lambda ctx: gateway.forward("worker", ctx))
    gateway_router.add("POST", "/workers/heartbeat", lambda ctx: gateway.forward("worker", ctx))
    gateway_router.add("POST", "/workers/task/result", lambda ctx: gateway.forward("worker", ctx))

    if is_enabled("auth"):
        start_server(config.auth_port, auth_router, Logger("auth"), metrics)
    if is_enabled("user"):
        start_server(config.user_port, user_router, Logger("user"), metrics)
    if is_enabled("payment"):
        start_server(config.payment_port, payment_router, Logger("payment"), metrics)
    if is_enabled("workflow"):
        start_server(config.workflow_port, workflow_router, Logger("workflow"), metrics)
    if is_enabled("queue"):
        start_server(config.queue_port, queue_router, Logger("queue"), metrics)
    if is_enabled("stream"):
        start_server(config.stream_port, stream_router, Logger("stream"), metrics)
    if is_enabled("cache"):
        start_server(config.cache_port, cache_router, Logger("cache"), metrics)
    if is_enabled("db"):
        start_server(config.db_port, db_router, Logger("db"), metrics)
    if is_enabled("ws"):
        start_server(config.ws_port, ws_router, Logger("ws"), metrics)
    if is_enabled("scheduler"):
        start_server(config.scheduler_port, scheduler_router, Logger("scheduler"), metrics)
    if is_enabled("worker"):
        start_server(config.worker_port, worker_router, Logger("worker"), metrics)
    if is_enabled("gateway"):
        start_server(config.gateway_port, gateway_router, Logger("gateway"), metrics)

    Logger("platform").info("platform_started", ports={
        "gateway": config.gateway_port,
        "auth": config.auth_port,
        "user": config.user_port,
        "payment": config.payment_port,
        "workflow": config.workflow_port,
        "queue": config.queue_port,
        "stream": config.stream_port,
        "cache": config.cache_port,
        "db": config.db_port,
        "ws": config.ws_port,
        "scheduler": config.scheduler_port,
        "worker": config.worker_port,
    })
    while True:
        time.sleep(5)


if __name__ == "__main__":
    main()
