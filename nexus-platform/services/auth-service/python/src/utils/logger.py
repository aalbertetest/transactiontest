# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - LOGGER
# =============================================================================
# Structured logging configuration using structlog.
# =============================================================================

"""
Logger Configuration

Provides structured logging with:
- JSON output for production
- Pretty console output for development
- Request ID propagation
- Performance metrics
"""

import logging
import sys
from typing import Any, Dict, Optional

import structlog
from structlog.types import Processor

from ..config import settings


def setup_logging() -> None:
    """
    Configure structured logging for the application.
    
    Uses structlog with different renderers for development and production.
    """
    # Set up standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.logging.level.upper()),
    )
    
    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    
    # Common processors
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]
    
    if settings.is_development():
        # Development: colored console output
        processors = shared_processors + [
            structlog.dev.ConsoleRenderer(colors=True),
        ]
    else:
        # Production: JSON output
        processors = shared_processors + [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, settings.logging.level.upper())
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: Optional[str] = None) -> structlog.BoundLogger:
    """
    Get a logger instance.
    
    Args:
        name: Logger name (typically __name__).
    
    Returns:
        structlog.BoundLogger: Configured logger instance.
    """
    return structlog.get_logger(name)


def bind_context(**kwargs: Any) -> None:
    """
    Bind context variables to the current logger context.
    
    These variables will be included in all subsequent log messages
    in the current async context.
    
    Args:
        **kwargs: Key-value pairs to bind.
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def unbind_context(*keys: str) -> None:
    """
    Unbind context variables from the current logger context.
    
    Args:
        *keys: Keys to unbind.
    """
    structlog.contextvars.unbind_contextvars(*keys)


def clear_context() -> None:
    """Clear all context variables."""
    structlog.contextvars.clear_contextvars()


class RequestContext:
    """
    Context manager for request-scoped logging context.
    
    Usage:
        async with RequestContext(request_id="123", user_id="456"):
            logger.info("Processing request")
    """
    
    def __init__(self, **kwargs: Any) -> None:
        self.context = kwargs
        self._token = None
    
    async def __aenter__(self) -> "RequestContext":
        bind_context(**self.context)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        unbind_context(*self.context.keys())
    
    def __enter__(self) -> "RequestContext":
        bind_context(**self.context)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        unbind_context(*self.context.keys())


def log_performance(
    logger: structlog.BoundLogger,
    operation: str,
    duration_ms: float,
    **extra: Any,
) -> None:
    """
    Log a performance metric.
    
    Args:
        logger: Logger instance.
        operation: Name of the operation.
        duration_ms: Duration in milliseconds.
        **extra: Additional context.
    """
    logger.info(
        "Performance metric",
        operation=operation,
        duration_ms=round(duration_ms, 2),
        **extra,
    )


def log_security_event(
    logger: structlog.BoundLogger,
    event_type: str,
    user_id: Optional[str] = None,
    ip_address: Optional[str] = None,
    success: bool = True,
    **extra: Any,
) -> None:
    """
    Log a security-related event.
    
    Args:
        logger: Logger instance.
        event_type: Type of security event.
        user_id: User ID if applicable.
        ip_address: Client IP address.
        success: Whether the event was successful.
        **extra: Additional context.
    """
    log_func = logger.info if success else logger.warning
    log_func(
        "Security event",
        event_type=event_type,
        user_id=user_id,
        ip_address=ip_address,
        success=success,
        **extra,
    )
