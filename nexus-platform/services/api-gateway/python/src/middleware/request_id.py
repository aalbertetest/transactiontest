# =============================================================================
# NEXUS PLATFORM - API GATEWAY - REQUEST ID MIDDLEWARE
# =============================================================================
# Generates and propagates unique request IDs for request tracing.
# =============================================================================

"""
Request ID Middleware

This middleware generates a unique request ID for each incoming request,
enabling request tracing across the distributed system. The request ID is:
- Generated using UUID v4 if not provided
- Extracted from X-Request-ID header if present
- Added to request state for access in handlers
- Included in response headers for client correlation
- Propagated to downstream services

The request ID follows the format: req_<uuid4>
"""

import uuid
from typing import Callable

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware for generating and propagating request IDs.
    
    This middleware ensures every request has a unique identifier that can
    be used for logging, tracing, and debugging across the distributed system.
    
    Attributes:
        REQUEST_ID_HEADER: The header name for request ID (X-Request-ID).
        CORRELATION_ID_HEADER: The header name for correlation ID (X-Correlation-ID).
        REQUEST_ID_PREFIX: Prefix for generated request IDs (req_).
    
    Example:
        # Request ID is automatically available in request.state
        @app.get("/example")
        async def example(request: Request):
            request_id = request.state.request_id
            return {"request_id": request_id}
    """
    
    REQUEST_ID_HEADER = "X-Request-ID"
    CORRELATION_ID_HEADER = "X-Correlation-ID"
    REQUEST_ID_PREFIX = "req_"
    
    def __init__(self, app: Callable):
        """
        Initialize the request ID middleware.
        
        Args:
            app: The ASGI application to wrap.
        """
        super().__init__(app)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process the request and add request ID.
        
        This method:
        1. Extracts existing request ID from header or generates new one
        2. Extracts or generates correlation ID for distributed tracing
        3. Stores both IDs in request state
        4. Adds both IDs to response headers
        
        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.
        
        Returns:
            Response: The response with request ID headers.
        """
        # Extract or generate request ID
        request_id = request.headers.get(self.REQUEST_ID_HEADER)
        
        if not request_id:
            # Generate new request ID with prefix
            request_id = f"{self.REQUEST_ID_PREFIX}{uuid.uuid4().hex}"
        elif not request_id.startswith(self.REQUEST_ID_PREFIX):
            # Add prefix if missing (client provided ID without prefix)
            request_id = f"{self.REQUEST_ID_PREFIX}{request_id}"
        
        # Extract or generate correlation ID
        # Correlation ID links related requests (e.g., from same user session)
        correlation_id = request.headers.get(self.CORRELATION_ID_HEADER)
        
        if not correlation_id:
            # Use request ID as correlation ID if not provided
            correlation_id = request_id
        
        # Store in request state for access in handlers
        request.state.request_id = request_id
        request.state.correlation_id = correlation_id
        
        # Process request
        response = await call_next(request)
        
        # Add IDs to response headers
        response.headers[self.REQUEST_ID_HEADER] = request_id
        response.headers[self.CORRELATION_ID_HEADER] = correlation_id
        
        return response


def get_request_id(request: Request) -> str:
    """
    Get the request ID from request state.
    
    This is a convenience function for extracting the request ID from
    the request state. If no request ID is found, generates a new one.
    
    Args:
        request: The FastAPI request object.
    
    Returns:
        str: The request ID.
    
    Example:
        @app.get("/example")
        async def example(request: Request):
            request_id = get_request_id(request)
            logger.info("Processing request", request_id=request_id)
    """
    return getattr(request.state, "request_id", f"req_{uuid.uuid4().hex}")


def get_correlation_id(request: Request) -> str:
    """
    Get the correlation ID from request state.
    
    This is a convenience function for extracting the correlation ID from
    the request state. If no correlation ID is found, returns the request ID.
    
    Args:
        request: The FastAPI request object.
    
    Returns:
        str: The correlation ID.
    """
    return getattr(request.state, "correlation_id", get_request_id(request))
