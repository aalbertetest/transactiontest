# =============================================================================
# NEXUS PLATFORM - API GATEWAY - MAIN APPLICATION
# =============================================================================
# FastAPI application setup with middleware, routing, and lifecycle management.
# =============================================================================

"""
Main Application Module

This module creates and configures the FastAPI application for the API Gateway.
It sets up all middleware, routers, exception handlers, and lifecycle events.

The application follows these principles:
- Dependency injection for testability
- Graceful startup and shutdown
- Comprehensive error handling
- Request tracing and logging
- Health monitoring
"""

import asyncio
import signal
import sys
from contextlib import asynccontextmanager
from datetime import datetime, timezone
from typing import AsyncGenerator, Callable
from uuid import uuid4

import structlog
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from .config import Settings, get_settings
from .middleware.authentication import AuthenticationMiddleware
from .middleware.circuit_breaker import CircuitBreakerMiddleware
from .middleware.logging import LoggingMiddleware
from .middleware.metrics import MetricsMiddleware
from .middleware.rate_limiting import RateLimitMiddleware
from .middleware.request_id import RequestIDMiddleware
from .middleware.tracing import TracingMiddleware
from .routers import health, proxy, admin
from .services.service_discovery import ServiceDiscovery
from .utils.errors import (
    APIError,
    AuthenticationError,
    RateLimitExceeded,
    ServiceUnavailable,
)
from .utils.logger import setup_logging

# Initialize structured logger
logger = structlog.get_logger(__name__)


class ApplicationState:
    """
    Application state container.
    
    Holds references to shared resources that need to be accessible
    across the application lifecycle.
    """
    
    def __init__(self):
        self.settings: Settings = None
        self.service_discovery: ServiceDiscovery = None
        self.http_client = None
        self.redis_client = None
        self.db_pool = None
        self.is_shutting_down: bool = False
        self.startup_time: datetime = None
        self.request_count: int = 0


# Global application state
app_state = ApplicationState()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Application lifespan manager.
    
    Handles startup and shutdown events for the application, including:
    - Initializing connections (database, Redis, HTTP clients)
    - Starting background tasks
    - Setting up signal handlers
    - Graceful shutdown of all resources
    
    Args:
        app: The FastAPI application instance.
        
    Yields:
        None: Control returns to the application.
    """
    settings = get_settings()
    app_state.settings = settings
    app_state.startup_time = datetime.now(timezone.utc)
    
    logger.info(
        "Starting API Gateway",
        service=settings.service_name,
        version=settings.service_version,
        environment=settings.environment.value,
        instance_id=settings.instance_id,
    )
    
    # Initialize HTTP client for backend requests
    import httpx
    
    app_state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(
            connect=settings.backend.connect_timeout,
            read=settings.backend.read_timeout,
            write=settings.backend.write_timeout,
            pool=settings.backend.connect_timeout,
        ),
        limits=httpx.Limits(
            max_connections=settings.backend.max_connections_per_host,
            max_keepalive_connections=settings.backend.max_keepalive_connections,
            keepalive_expiry=settings.backend.keepalive_expiry,
        ),
        http2=True,
    )
    
    # Initialize Redis client for caching and rate limiting
    if settings.cache.enabled or settings.rate_limit.enabled:
        import redis.asyncio as redis
        
        app_state.redis_client = redis.from_url(
            settings.cache.redis_url,
            encoding="utf-8",
            decode_responses=True,
        )
        
        # Test Redis connection
        try:
            await app_state.redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.error("Failed to connect to Redis", error=str(e))
            if settings.is_production():
                raise
    
    # Initialize database connection pool
    if settings.database.host:
        from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
        from sqlalchemy.orm import sessionmaker
        
        engine = create_async_engine(
            settings.database.url,
            pool_size=settings.database.pool_size,
            max_overflow=settings.database.max_overflow,
            pool_timeout=settings.database.pool_timeout,
            pool_recycle=settings.database.pool_recycle,
            echo=settings.debug,
        )
        
        app_state.db_pool = sessionmaker(
            engine,
            class_=AsyncSession,
            expire_on_commit=False,
        )
        
        logger.info("Database connection pool initialized")
    
    # Initialize service discovery
    app_state.service_discovery = ServiceDiscovery(settings.backend)
    await app_state.service_discovery.start()
    
    logger.info(
        "API Gateway started successfully",
        startup_time_ms=(datetime.now(timezone.utc) - app_state.startup_time).total_seconds() * 1000,
    )
    
    # Store state in app for access in routes
    app.state.app_state = app_state
    
    try:
        yield
    finally:
        # Shutdown sequence
        logger.info("Initiating graceful shutdown")
        app_state.is_shutting_down = True
        
        # Wait for in-flight requests (up to graceful_shutdown_timeout)
        shutdown_deadline = datetime.now(timezone.utc).timestamp() + settings.server.graceful_shutdown_timeout
        
        while app_state.request_count > 0:
            if datetime.now(timezone.utc).timestamp() > shutdown_deadline:
                logger.warning(
                    "Shutdown timeout reached, forcing shutdown",
                    remaining_requests=app_state.request_count,
                )
                break
            await asyncio.sleep(0.1)
        
        # Close HTTP client
        if app_state.http_client:
            await app_state.http_client.aclose()
            logger.info("HTTP client closed")
        
        # Close Redis connection
        if app_state.redis_client:
            await app_state.redis_client.close()
            logger.info("Redis connection closed")
        
        # Stop service discovery
        if app_state.service_discovery:
            await app_state.service_discovery.stop()
            logger.info("Service discovery stopped")
        
        logger.info("API Gateway shutdown complete")


def create_app(settings: Settings = None) -> FastAPI:
    """
    Create and configure the FastAPI application.
    
    This factory function creates a new FastAPI instance with all
    middleware, routers, and exception handlers configured.
    
    Args:
        settings: Optional settings override. If not provided,
                  settings are loaded from environment.
    
    Returns:
        FastAPI: Configured FastAPI application instance.
    """
    if settings is None:
        settings = get_settings()
    
    # Setup logging
    setup_logging(settings.logging)
    
    # Create FastAPI app
    app = FastAPI(
        title="Nexus Platform API Gateway",
        description="""
        The Nexus Platform API Gateway is the central entry point for all API requests.
        
        ## Features
        
        - **Authentication**: JWT and API key authentication
        - **Rate Limiting**: Per-user, per-IP, and per-endpoint rate limits
        - **Circuit Breaker**: Automatic fault tolerance for backend services
        - **Request Routing**: Dynamic routing to backend microservices
        - **Caching**: Response caching for improved performance
        - **Observability**: Comprehensive logging, metrics, and tracing
        
        ## Authentication
        
        Most endpoints require authentication via:
        - Bearer token (JWT) in Authorization header
        - API key in X-API-Key header
        
        ## Rate Limits
        
        - 100 requests per minute per user
        - 60 requests per minute per IP (unauthenticated)
        - Rate limit headers included in responses
        """,
        version=settings.service_version,
        docs_url="/docs" if settings.is_development() else None,
        redoc_url="/redoc" if settings.is_development() else None,
        openapi_url="/openapi.json" if settings.is_development() else None,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    
    # =========================================================================
    # EXCEPTION HANDLERS
    # =========================================================================
    
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        """Handle custom API errors with structured response."""
        logger.warning(
            "API error",
            error_code=exc.code,
            error_message=exc.message,
            request_id=getattr(request.state, "request_id", None),
            path=request.url.path,
        )
        
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                    "request_id": getattr(request.state, "request_id", None),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            },
        )
    
    @app.exception_handler(AuthenticationError)
    async def auth_error_handler(request: Request, exc: AuthenticationError) -> JSONResponse:
        """Handle authentication errors."""
        logger.warning(
            "Authentication error",
            error_message=str(exc),
            request_id=getattr(request.state, "request_id", None),
            path=request.url.path,
        )
        
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={
                "error": {
                    "code": "AUTHENTICATION_ERROR",
                    "message": str(exc),
                    "request_id": getattr(request.state, "request_id", None),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            },
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    @app.exception_handler(RateLimitExceeded)
    async def rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
        """Handle rate limit exceeded errors."""
        logger.warning(
            "Rate limit exceeded",
            limit=exc.limit,
            window=exc.window,
            request_id=getattr(request.state, "request_id", None),
            path=request.url.path,
            client_ip=request.client.host if request.client else None,
        )
        
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={
                "error": {
                    "code": "RATE_LIMIT_EXCEEDED",
                    "message": f"Rate limit exceeded. Try again in {exc.retry_after} seconds.",
                    "limit": exc.limit,
                    "window": exc.window,
                    "retry_after": exc.retry_after,
                    "request_id": getattr(request.state, "request_id", None),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            },
            headers={
                "Retry-After": str(exc.retry_after),
                "X-RateLimit-Limit": str(exc.limit),
                "X-RateLimit-Remaining": "0",
                "X-RateLimit-Reset": str(exc.reset_at),
            },
        )
    
    @app.exception_handler(ServiceUnavailable)
    async def service_unavailable_handler(request: Request, exc: ServiceUnavailable) -> JSONResponse:
        """Handle service unavailable errors (circuit breaker open)."""
        logger.error(
            "Service unavailable",
            service=exc.service,
            request_id=getattr(request.state, "request_id", None),
            path=request.url.path,
        )
        
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={
                "error": {
                    "code": "SERVICE_UNAVAILABLE",
                    "message": f"Service '{exc.service}' is temporarily unavailable. Please try again later.",
                    "service": exc.service,
                    "retry_after": exc.retry_after,
                    "request_id": getattr(request.state, "request_id", None),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            },
            headers={"Retry-After": str(exc.retry_after)},
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
        """Handle request validation errors with detailed field information."""
        errors = []
        for error in exc.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            errors.append({
                "field": field,
                "message": error["msg"],
                "type": error["type"],
            })
        
        logger.warning(
            "Validation error",
            errors=errors,
            request_id=getattr(request.state, "request_id", None),
            path=request.url.path,
        )
        
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Request validation failed",
                    "details": errors,
                    "request_id": getattr(request.state, "request_id", None),
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            },
        )
    
    @app.exception_handler(Exception)
    async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
        """Handle unexpected errors with proper logging."""
        request_id = getattr(request.state, "request_id", None)
        
        logger.exception(
            "Unhandled exception",
            error=str(exc),
            error_type=type(exc).__name__,
            request_id=request_id,
            path=request.url.path,
        )
        
        # In production, don't expose internal error details
        if settings.is_production():
            message = "An internal error occurred. Please try again later."
            details = None
        else:
            message = str(exc)
            details = {"type": type(exc).__name__}
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": message,
                    "details": details,
                    "request_id": request_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            },
        )
    
    # =========================================================================
    # MIDDLEWARE (order matters - first added = outermost)
    # =========================================================================
    
    # GZip compression for responses
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    
    # CORS handling
    if settings.server.cors_enabled:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.server.cors_origins,
            allow_credentials=settings.server.cors_credentials,
            allow_methods=settings.server.cors_methods,
            allow_headers=settings.server.cors_headers,
            max_age=settings.server.cors_max_age,
        )
    
    # Request ID middleware (generates unique ID for each request)
    app.add_middleware(RequestIDMiddleware)
    
    # Logging middleware (logs all requests/responses)
    app.add_middleware(LoggingMiddleware, settings=settings.logging)
    
    # Metrics middleware (collects Prometheus metrics)
    if settings.metrics.enabled:
        app.add_middleware(MetricsMiddleware, settings=settings.metrics)
    
    # Tracing middleware (OpenTelemetry distributed tracing)
    if settings.tracing.enabled:
        app.add_middleware(TracingMiddleware, settings=settings.tracing)
    
    # Rate limiting middleware
    if settings.rate_limit.enabled:
        app.add_middleware(RateLimitMiddleware, settings=settings.rate_limit)
    
    # Circuit breaker middleware
    if settings.circuit_breaker.enabled:
        app.add_middleware(CircuitBreakerMiddleware, settings=settings.circuit_breaker)
    
    # Authentication middleware
    app.add_middleware(AuthenticationMiddleware, settings=settings.auth)
    
    # =========================================================================
    # ROUTERS
    # =========================================================================
    
    # Health check endpoints (/health, /ready, /live)
    app.include_router(health.router, tags=["Health"])
    
    # Admin endpoints (/admin/*)
    app.include_router(admin.router, prefix="/admin", tags=["Admin"])
    
    # Metrics endpoint
    if settings.metrics.enabled:
        from .routers import metrics as metrics_router
        app.include_router(metrics_router.router, tags=["Metrics"])
    
    # Proxy router for all other requests (must be last)
    app.include_router(proxy.router, tags=["Proxy"])
    
    # =========================================================================
    # ROOT ENDPOINT
    # =========================================================================
    
    @app.get("/", include_in_schema=False)
    async def root():
        """Root endpoint returning service info."""
        return {
            "service": settings.service_name,
            "version": settings.service_version,
            "environment": settings.environment.value,
            "status": "operational",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    return app


# Create default app instance
app = create_app()


def main():
    """
    Entry point for running the API Gateway.
    
    This function is called when the module is run directly.
    It starts the uvicorn server with the configured settings.
    """
    import uvicorn
    
    settings = get_settings()
    
    uvicorn.run(
        "src.main:app",
        host=settings.server.host,
        port=settings.server.port,
        workers=settings.server.workers if not settings.debug else 1,
        reload=settings.debug,
        log_level=settings.logging.level.value.lower(),
        access_log=settings.logging.log_requests,
        timeout_keep_alive=settings.server.keepalive_timeout,
        limit_max_requests=10000 if settings.is_production() else None,
    )


if __name__ == "__main__":
    main()
