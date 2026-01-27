# =============================================================================
# NEXUS PLATFORM - API GATEWAY - LOGGING SETUP
# =============================================================================
# Structured logging configuration using structlog.
# =============================================================================

"""
Logging Module

This module sets up structured logging using structlog with support for:
- JSON output for production
- Colored console output for development
- Context propagation (request ID, user ID, etc.)
- Log level configuration
- Integration with standard logging
"""

import logging
import sys
from typing import Any, Dict, Optional

import structlog
from structlog.types import Processor

from ..config import LoggingSettings, LogLevel


def add_service_context(
    logger: Any,
    method_name: str,
    event_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Add service context to all log entries.
    
    Args:
        logger: The logger instance.
        method_name: The logging method name.
        event_dict: The event dictionary.
    
    Returns:
        Dict: The event dictionary with service context.
    """
    event_dict["service"] = "api-gateway"
    return event_dict


def add_timestamp(
    logger: Any,
    method_name: str,
    event_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Add ISO timestamp to all log entries.
    
    Args:
        logger: The logger instance.
        method_name: The logging method name.
        event_dict: The event dictionary.
    
    Returns:
        Dict: The event dictionary with timestamp.
    """
    from datetime import datetime, timezone
    
    event_dict["timestamp"] = datetime.now(timezone.utc).isoformat()
    return event_dict


def setup_logging(settings: LoggingSettings) -> None:
    """
    Configure structured logging for the application.
    
    This function sets up structlog with appropriate processors
    and handlers based on the configuration.
    
    Args:
        settings: Logging configuration settings.
    """
    # Define shared processors
    shared_processors: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.PositionalArgumentsFormatter(),
        add_timestamp,
        add_service_context,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.UnicodeDecoder(),
    ]
    
    # Configure based on output format
    if settings.format == "json":
        # JSON format for production
        shared_processors.append(
            structlog.processors.format_exc_info,
        )
        renderer = structlog.processors.JSONRenderer()
    else:
        # Colored console output for development
        shared_processors.append(
            structlog.dev.set_exc_info,
        )
        renderer = structlog.dev.ConsoleRenderer(
            colors=True,
            exception_formatter=structlog.dev.rich_traceback,
        )
    
    # Configure structlog
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # Configure standard logging
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=shared_processors,
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            renderer,
        ],
    )
    
    # Setup handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(getattr(logging, settings.level.value))
    
    # Configure specific loggers
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        logger = logging.getLogger(logger_name)
        logger.handlers = [handler]
        logger.propagate = False
    
    # Reduce noise from third-party libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
    
    structlog.get_logger().info(
        "Logging configured",
        level=settings.level.value,
        format=settings.format,
    )


def get_logger(name: Optional[str] = None) -> structlog.stdlib.BoundLogger:
    """
    Get a logger instance.
    
    Args:
        name: Optional logger name. If not provided, uses the caller's module name.
    
    Returns:
        BoundLogger: A structlog bound logger.
    """
    return structlog.get_logger(name)


def bind_context(**kwargs: Any) -> None:
    """
    Bind context variables to the current context.
    
    These variables will be included in all subsequent log messages
    within the current async context.
    
    Args:
        **kwargs: Key-value pairs to bind to the logging context.
    
    Example:
        bind_context(request_id="abc123", user_id="user456")
        logger.info("Processing request")  # Will include request_id and user_id
    """
    structlog.contextvars.bind_contextvars(**kwargs)


def unbind_context(*keys: str) -> None:
    """
    Remove context variables from the current context.
    
    Args:
        *keys: Keys to remove from the logging context.
    """
    structlog.contextvars.unbind_contextvars(*keys)


def clear_context() -> None:
    """
    Clear all context variables from the current context.
    """
    structlog.contextvars.clear_contextvars()


class LogContext:
    """
    Context manager for temporarily binding log context.
    
    Example:
        with LogContext(request_id="abc123"):
            logger.info("Processing")  # Includes request_id
        logger.info("Done")  # Does not include request_id
    """
    
    def __init__(self, **kwargs: Any):
        self.kwargs = kwargs
        self._old_values: Dict[str, Any] = {}
    
    def __enter__(self) -> "LogContext":
        # Store old values and bind new ones
        current = structlog.contextvars.get_contextvars()
        for key in self.kwargs:
            if key in current:
                self._old_values[key] = current[key]
        bind_context(**self.kwargs)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        # Restore old values or unbind
        for key in self.kwargs:
            if key in self._old_values:
                bind_context(**{key: self._old_values[key]})
            else:
                unbind_context(key)
