# =============================================================================
# NEXUS PLATFORM - API GATEWAY - LOGGING MIDDLEWARE
# =============================================================================
# Structured logging for all requests and responses.
# =============================================================================

"""
Logging Middleware

This middleware provides comprehensive structured logging for all
HTTP requests and responses flowing through the API Gateway.

Features:
- Structured JSON logging
- Request/response logging with timing
- Sensitive header redaction
- Request body logging (optional, for debugging)
- Correlation ID propagation
- Log level control by path
- Integration with OpenTelemetry tracing
"""

import time
from typing import Callable, List, Set

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import LoggingSettings

logger = structlog.get_logger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Structured logging middleware.
    
    This middleware logs all requests and responses with structured
    context including timing, request details, and response status.
    
    Sensitive information (Authorization headers, API keys, etc.) is
    automatically redacted.
    
    Attributes:
        settings: Logging configuration.
        sensitive_headers: Headers to redact in logs.
        quiet_paths: Paths that are logged at DEBUG level.
    """
    
    # Paths that should be logged at DEBUG level (high frequency)
    DEFAULT_QUIET_PATHS = {
        "/health",
        "/ready",
        "/live",
        "/metrics",
    }
    
    def __init__(
        self,
        app: Callable,
        settings: LoggingSettings,
        quiet_paths: Set[str] = None,
    ):
        """
        Initialize logging middleware.
        
        Args:
            app: The ASGI application to wrap.
            settings: Logging configuration.
            quiet_paths: Paths to log at DEBUG level.
        """
        super().__init__(app)
        self.settings = settings
        self.sensitive_headers = set(
            h.lower() for h in settings.sensitive_headers
        )
        self.quiet_paths = quiet_paths or self.DEFAULT_QUIET_PATHS
    
    def _redact_headers(self, headers: dict) -> dict:
        """
        Redact sensitive headers from log output.
        
        Args:
            headers: The headers dict.
        
        Returns:
            dict: Headers with sensitive values redacted.
        """
        redacted = {}
        for key, value in headers.items():
            if key.lower() in self.sensitive_headers:
                # Redact but show first/last few characters for debugging
                if len(value) > 8:
                    redacted[key] = f"{value[:3]}...{value[-3:]}"
                else:
                    redacted[key] = "[REDACTED]"
            else:
                redacted[key] = value
        return redacted
    
    def _get_client_info(self, request: Request) -> dict:
        """
        Extract client information from request.
        
        Args:
            request: The incoming request.
        
        Returns:
            dict: Client information.
        """
        client_ip = None
        
        # Check forwarded headers
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()
        elif request.headers.get("X-Real-IP"):
            client_ip = request.headers.get("X-Real-IP")
        elif request.client:
            client_ip = request.client.host
        
        return {
            "ip": client_ip,
            "user_agent": request.headers.get("User-Agent", ""),
            "referer": request.headers.get("Referer", ""),
        }
    
    def _get_user_info(self, request: Request) -> dict:
        """
        Extract authenticated user information from request.
        
        Args:
            request: The incoming request.
        
        Returns:
            dict: User information.
        """
        user = getattr(request.state, "user", None)
        if user:
            return {
                "user_id": user.user_id,
                "tenant_id": user.tenant_id,
                "auth_method": getattr(request.state, "auth_method", None),
            }
        return {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Log request and response.
        
        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.
        
        Returns:
            Response: The response.
        """
        # Skip logging if disabled
        if not self.settings.log_requests:
            return await call_next(request)
        
        # Start timing
        start_time = time.perf_counter()
        
        # Get request ID and correlation ID
        request_id = getattr(request.state, "request_id", None)
        correlation_id = getattr(request.state, "correlation_id", None)
        
        # Determine log level based on path
        is_quiet = request.url.path in self.quiet_paths
        log_method = logger.debug if is_quiet else logger.info
        
        # Build request context
        request_context = {
            "request_id": request_id,
            "correlation_id": correlation_id,
            "method": request.method,
            "path": request.url.path,
            "query": str(request.query_params) if request.query_params else None,
            "client": self._get_client_info(request),
        }
        
        # Add headers if configured (redacted)
        if self.settings.log_request_body:
            request_context["headers"] = self._redact_headers(dict(request.headers))
        
        # Log request start
        log_method(
            "Request started",
            **request_context,
        )
        
        # Process request
        response = None
        error = None
        
        try:
            response = await call_next(request)
            
        except Exception as e:
            error = e
            raise
            
        finally:
            # Calculate duration
            duration_ms = (time.perf_counter() - start_time) * 1000
            
            # Build response context
            response_context = {
                "request_id": request_id,
                "correlation_id": correlation_id,
                "method": request.method,
                "path": request.url.path,
                "duration_ms": round(duration_ms, 2),
                "user": self._get_user_info(request),
            }
            
            if response:
                response_context["status_code"] = response.status_code
                
                # Add rate limit info if available
                rate_limit = getattr(request.state, "rate_limit", None)
                if rate_limit:
                    response_context["rate_limit"] = {
                        "limit": rate_limit.limit,
                        "remaining": rate_limit.remaining,
                        "policy": rate_limit.policy,
                    }
                
                # Determine log level based on status code
                if response.status_code >= 500:
                    log_method = logger.error
                elif response.status_code >= 400:
                    log_method = logger.warning
                else:
                    log_method = logger.debug if is_quiet else logger.info
                    
            else:
                response_context["status_code"] = 500
                response_context["error"] = str(error) if error else "Unknown error"
                log_method = logger.error
            
            # Log request completion
            log_method(
                "Request completed",
                **response_context,
            )
        
        return response


class AccessLogFormatter:
    """
    Format access logs in common log formats.
    
    Supports:
    - Combined log format (Apache/Nginx style)
    - JSON format
    - Custom formats
    """
    
    COMBINED_FORMAT = '{client_ip} - {user_id} [{timestamp}] "{method} {path} {protocol}" {status} {size} "{referer}" "{user_agent}"'
    
    @classmethod
    def format_combined(
        cls,
        request: Request,
        response: Response,
        duration_ms: float,
    ) -> str:
        """
        Format log entry in combined log format.
        
        Args:
            request: The request.
            response: The response.
            duration_ms: Request duration in milliseconds.
        
        Returns:
            str: Formatted log entry.
        """
        from datetime import datetime
        
        # Get client IP
        client_ip = request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        if not client_ip and request.client:
            client_ip = request.client.host
        client_ip = client_ip or "-"
        
        # Get user ID
        user = getattr(request.state, "user", None)
        user_id = user.user_id if user else "-"
        
        # Format timestamp
        timestamp = datetime.utcnow().strftime("%d/%b/%Y:%H:%M:%S +0000")
        
        # Get response size
        size = response.headers.get("Content-Length", "-")
        
        return cls.COMBINED_FORMAT.format(
            client_ip=client_ip,
            user_id=user_id,
            timestamp=timestamp,
            method=request.method,
            path=request.url.path,
            protocol=f"HTTP/{request.scope.get('http_version', '1.1')}",
            status=response.status_code,
            size=size,
            referer=request.headers.get("Referer", "-"),
            user_agent=request.headers.get("User-Agent", "-"),
        )
