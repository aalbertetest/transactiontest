# =============================================================================
# NEXUS PLATFORM - API GATEWAY - METRICS MIDDLEWARE
# =============================================================================
# Prometheus metrics collection for observability.
# =============================================================================

"""
Metrics Middleware

This middleware collects Prometheus metrics for all HTTP requests,
providing visibility into API Gateway performance and behavior.

Metrics collected:
- Request count (by method, path, status)
- Request duration histogram
- Request/response size histograms
- Active request count (gauge)
- Error counts (by type)
- Rate limit metrics
- Circuit breaker metrics

All metrics follow Prometheus naming conventions and include
appropriate labels for filtering and aggregation.
"""

import time
from typing import Callable, List

from fastapi import Request, Response
from prometheus_client import Counter, Gauge, Histogram, Info
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import MetricsSettings


# =============================================================================
# METRIC DEFINITIONS
# =============================================================================

# Info metric for service identification
SERVICE_INFO = Info(
    "nexus_gateway",
    "API Gateway service information",
)

# Request counter
REQUEST_COUNT = Counter(
    "nexus_gateway_requests_total",
    "Total number of HTTP requests",
    ["method", "path", "status", "service"],
)

# Request duration histogram
REQUEST_DURATION = Histogram(
    "nexus_gateway_request_duration_seconds",
    "HTTP request duration in seconds",
    ["method", "path", "status"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
)

# Request size histogram
REQUEST_SIZE = Histogram(
    "nexus_gateway_request_size_bytes",
    "HTTP request size in bytes",
    ["method", "path"],
    buckets=[100, 1000, 10000, 100000, 1000000, 10000000],
)

# Response size histogram
RESPONSE_SIZE = Histogram(
    "nexus_gateway_response_size_bytes",
    "HTTP response size in bytes",
    ["method", "path", "status"],
    buckets=[100, 1000, 10000, 100000, 1000000, 10000000],
)

# Active requests gauge
ACTIVE_REQUESTS = Gauge(
    "nexus_gateway_active_requests",
    "Number of currently active requests",
    ["method"],
)

# Error counter
ERROR_COUNT = Counter(
    "nexus_gateway_errors_total",
    "Total number of errors",
    ["type", "method", "path"],
)

# Rate limit counter
RATE_LIMIT_COUNT = Counter(
    "nexus_gateway_rate_limit_total",
    "Total number of rate-limited requests",
    ["policy", "method", "path"],
)

# Circuit breaker counter
CIRCUIT_BREAKER_COUNT = Counter(
    "nexus_gateway_circuit_breaker_total",
    "Total number of circuit breaker events",
    ["service", "state", "action"],
)

# Authentication counter
AUTH_COUNT = Counter(
    "nexus_gateway_auth_total",
    "Total number of authentication attempts",
    ["method", "result"],
)

# Upstream request duration
UPSTREAM_DURATION = Histogram(
    "nexus_gateway_upstream_duration_seconds",
    "Upstream service request duration in seconds",
    ["service", "method", "status"],
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0],
)

# Cache metrics
CACHE_HITS = Counter(
    "nexus_gateway_cache_hits_total",
    "Total number of cache hits",
    ["path"],
)

CACHE_MISSES = Counter(
    "nexus_gateway_cache_misses_total",
    "Total number of cache misses",
    ["path"],
)


class MetricsMiddleware(BaseHTTPMiddleware):
    """
    Prometheus metrics collection middleware.
    
    This middleware wraps all requests and collects metrics
    for monitoring and alerting.
    
    Attributes:
        settings: Metrics configuration.
        prefix: Metric name prefix.
    """
    
    # Paths to exclude from metrics (health checks, metrics endpoint)
    EXCLUDED_PATHS = {
        "/metrics",
        "/health",
        "/ready",
        "/live",
    }
    
    def __init__(
        self,
        app: Callable,
        settings: MetricsSettings,
    ):
        """
        Initialize metrics middleware.
        
        Args:
            app: The ASGI application to wrap.
            settings: Metrics configuration.
        """
        super().__init__(app)
        self.settings = settings
        
        # Set service info
        SERVICE_INFO.info({
            "version": "1.0.0",
            "environment": "production",
        })
    
    def _normalize_path(self, path: str) -> str:
        """
        Normalize path for metrics labels.
        
        Replaces path parameters with placeholders to prevent
        cardinality explosion.
        
        Args:
            path: The request path.
        
        Returns:
            str: Normalized path.
        """
        import re
        
        # Replace UUIDs
        path = re.sub(
            r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
            "{id}",
            path,
            flags=re.IGNORECASE,
        )
        
        # Replace numeric IDs
        path = re.sub(r"/\d+(/|$)", "/{id}\\1", path)
        
        # Replace long hex strings (API keys, tokens)
        path = re.sub(r"/[0-9a-f]{16,}(/|$)", "/{token}\\1", path, flags=re.IGNORECASE)
        
        return path
    
    def _extract_service(self, request: Request) -> str:
        """
        Extract target service from request.
        
        Args:
            request: The incoming request.
        
        Returns:
            str: Service name.
        """
        path = request.url.path.strip("/")
        
        if "/" in path:
            return path.split("/")[0]
        
        return path or "root"
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Collect metrics for the request.
        
        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.
        
        Returns:
            Response: The response.
        """
        # Skip excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)
        
        method = request.method
        path = self._normalize_path(request.url.path)
        service = self._extract_service(request)
        
        # Track active requests
        ACTIVE_REQUESTS.labels(method=method).inc()
        
        # Record request size
        content_length = request.headers.get("Content-Length")
        if content_length:
            REQUEST_SIZE.labels(method=method, path=path).observe(int(content_length))
        
        # Start timing
        start_time = time.perf_counter()
        
        status_code = "500"
        response = None
        
        try:
            response = await call_next(request)
            status_code = str(response.status_code)
            
            # Record response size
            response_size = response.headers.get("Content-Length")
            if response_size:
                RESPONSE_SIZE.labels(
                    method=method,
                    path=path,
                    status=status_code,
                ).observe(int(response_size))
            
            # Track rate limiting
            rate_limit = getattr(request.state, "rate_limit", None)
            if rate_limit and not rate_limit.allowed:
                RATE_LIMIT_COUNT.labels(
                    policy=rate_limit.policy,
                    method=method,
                    path=path,
                ).inc()
            
            # Track authentication
            if hasattr(request.state, "authenticated"):
                AUTH_COUNT.labels(
                    method=getattr(request.state, "auth_method", "unknown"),
                    result="success" if request.state.authenticated else "failure",
                ).inc()
            
            return response
            
        except Exception as e:
            # Track error
            ERROR_COUNT.labels(
                type=type(e).__name__,
                method=method,
                path=path,
            ).inc()
            raise
            
        finally:
            # Record request duration
            duration = time.perf_counter() - start_time
            REQUEST_DURATION.labels(
                method=method,
                path=path,
                status=status_code,
            ).observe(duration)
            
            # Record request count
            REQUEST_COUNT.labels(
                method=method,
                path=path,
                status=status_code,
                service=service,
            ).inc()
            
            # Decrement active requests
            ACTIVE_REQUESTS.labels(method=method).dec()


def record_upstream_duration(
    service: str,
    method: str,
    status: int,
    duration: float,
) -> None:
    """
    Record upstream service request duration.
    
    Call this when making requests to backend services.
    
    Args:
        service: Backend service name.
        method: HTTP method.
        status: Response status code.
        duration: Duration in seconds.
    """
    UPSTREAM_DURATION.labels(
        service=service,
        method=method,
        status=str(status),
    ).observe(duration)


def record_circuit_breaker_event(
    service: str,
    state: str,
    action: str,
) -> None:
    """
    Record circuit breaker event.
    
    Args:
        service: Backend service name.
        state: Circuit breaker state (open, closed, half_open).
        action: Action taken (allow, reject, transition).
    """
    CIRCUIT_BREAKER_COUNT.labels(
        service=service,
        state=state,
        action=action,
    ).inc()


def record_cache_hit(path: str) -> None:
    """Record a cache hit."""
    CACHE_HITS.labels(path=path).inc()


def record_cache_miss(path: str) -> None:
    """Record a cache miss."""
    CACHE_MISSES.labels(path=path).inc()
