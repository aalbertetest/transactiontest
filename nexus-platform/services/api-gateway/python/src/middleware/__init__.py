# =============================================================================
# NEXUS PLATFORM - API GATEWAY - MIDDLEWARE
# =============================================================================
# Middleware components for request/response processing.
# =============================================================================

"""
Middleware Package

This package contains all middleware components for the API Gateway:
- RequestIDMiddleware: Generates unique request IDs
- LoggingMiddleware: Request/response logging
- MetricsMiddleware: Prometheus metrics collection
- TracingMiddleware: OpenTelemetry distributed tracing
- AuthenticationMiddleware: JWT/API key authentication
- RateLimitMiddleware: Rate limiting
- CircuitBreakerMiddleware: Circuit breaker pattern
"""

from .authentication import AuthenticationMiddleware
from .circuit_breaker import CircuitBreakerMiddleware
from .logging import LoggingMiddleware
from .metrics import MetricsMiddleware
from .rate_limiting import RateLimitMiddleware
from .request_id import RequestIDMiddleware
from .tracing import TracingMiddleware

__all__ = [
    "AuthenticationMiddleware",
    "CircuitBreakerMiddleware",
    "LoggingMiddleware",
    "MetricsMiddleware",
    "RateLimitMiddleware",
    "RequestIDMiddleware",
    "TracingMiddleware",
]
