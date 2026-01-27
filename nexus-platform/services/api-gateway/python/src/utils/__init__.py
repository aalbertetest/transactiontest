# =============================================================================
# NEXUS PLATFORM - API GATEWAY - UTILITIES
# =============================================================================

"""
Utilities Package

This package contains utility modules for the API Gateway:
- errors: Custom exception classes
- logger: Structured logging setup
- retry: Retry utilities with backoff
- validation: Request validation helpers
"""

from .errors import (
    APIError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    RateLimitExceeded,
    ServiceUnavailable,
    ValidationError,
)
from .logger import setup_logging, get_logger

__all__ = [
    "APIError",
    "AuthenticationError",
    "AuthorizationError",
    "NotFoundError",
    "RateLimitExceeded",
    "ServiceUnavailable",
    "ValidationError",
    "setup_logging",
    "get_logger",
]
