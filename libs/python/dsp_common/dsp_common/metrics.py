from __future__ import annotations

import http.server
import socketserver
import threading
from dataclasses import dataclass

from prometheus_client import CONTENT_TYPE_LATEST, CollectorRegistry, Counter, Histogram, generate_latest


@dataclass(frozen=True)
class Metrics:
    registry: CollectorRegistry
    http_requests_total: Counter
    http_request_duration_seconds: Histogram


def create_metrics(service_name: str) -> Metrics:
    """
    Metrics contract:
    - avoid unbounded label cardinality
    - label by route template, not raw path
    """
    reg = CollectorRegistry()
    http_requests_total = Counter(
        "http_requests_total",
        "Total HTTP requests",
        ["service", "method", "route", "status"],
        registry=reg,
    )
    http_request_duration_seconds = Histogram(
        "http_request_duration_seconds",
        "HTTP request duration in seconds",
        ["service", "method", "route", "status"],
        buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10),
        registry=reg,
    )
    # The service label is a constant conceptually, but prometheus_client doesn't
    # support const labels natively on these primitives; enforce via wrapper usage.
    return Metrics(registry=reg, http_requests_total=http_requests_total, http_request_duration_seconds=http_request_duration_seconds)


def start_metrics_server(addr: str, metrics: Metrics) -> threading.Thread:
    """
    Start a minimal Prometheus scrape endpoint on /metrics.
    Uses stdlib HTTP server to avoid heavy dependencies.
    """

    host, port_str = addr.split(":") if ":" in addr else ("0.0.0.0", addr)
    port = int(port_str)

    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self) -> None:  # noqa: N802
            if self.path != "/metrics":
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b"not found")
                return

            body = generate_latest(metrics.registry)
            self.send_response(200)
            self.send_header("Content-Type", CONTENT_TYPE_LATEST)
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, format: str, *args) -> None:  # noqa: A002
            # Do not emit default unstructured access logs; services log explicitly.
            return

    httpd = socketserver.TCPServer((host, port), Handler)

    t = threading.Thread(target=httpd.serve_forever, name="metrics-server", daemon=True)
    t.start()
    return t

