# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - MAIN APPLICATION
# =============================================================================
# FastAPI application for OAuth2, JWT, and MFA authentication.
# =============================================================================

"""
Authentication Service Main Application

This service provides comprehensive authentication and authorization including:
- User registration and login
- JWT token management (access and refresh tokens)
- OAuth2/OIDC authentication (Google, GitHub, etc.)
- Multi-factor authentication (TOTP, SMS, Email, WebAuthn)
- API key management
- Session management
- Password reset and email verification
"""

import asyncio
from contextlib import asynccontextmanager
from datetime import datetime, timezone

import structlog
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, ORJSONResponse

from .config import settings
from .api import auth, users, mfa, sessions, api_keys, oauth
from .core.database import init_db, close_db
from .core.redis import init_redis, close_redis
from .utils.logger import setup_logging

logger = structlog.get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info(
        "Starting Authentication Service",
        service=settings.service_name,
        version=settings.service_version,
        environment=settings.environment,
    )
    
    # Initialize database
    await init_db()
    logger.info("Database initialized")
    
    # Initialize Redis
    await init_redis()
    logger.info("Redis initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down Authentication Service")
    
    await close_redis()
    await close_db()
    
    logger.info("Authentication Service shutdown complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    setup_logging()
    
    app = FastAPI(
        title="Nexus Platform Authentication Service",
        description="""
        Authentication and authorization service for the Nexus Platform.
        
        ## Features
        - User registration and login
        - JWT token management
        - OAuth2/OIDC providers
        - Multi-factor authentication
        - API key management
        - Session management
        
        ## Authentication Methods
        - Bearer token (JWT)
        - API key (X-API-Key header)
        - OAuth2 (Google, GitHub, etc.)
        """,
        version=settings.service_version,
        docs_url="/docs" if settings.is_development() else None,
        redoc_url="/redoc" if settings.is_development() else None,
        default_response_class=ORJSONResponse,
        lifespan=lifespan,
    )
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.server.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Exception handlers
    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        logger.exception(
            "Unhandled exception",
            error=str(exc),
            path=request.url.path,
        )
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "An internal error occurred",
                }
            },
        )
    
    # Health check
    @app.get("/health")
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.service_name,
            "version": settings.service_version,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
    
    @app.get("/ready")
    async def readiness_check():
        return {"ready": True, "message": "Service is ready"}
    
    @app.get("/live")
    async def liveness_check():
        return {"alive": True, "message": "Service is alive"}
    
    # Include routers
    app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(mfa.router, prefix="/mfa", tags=["MFA"])
    app.include_router(sessions.router, prefix="/sessions", tags=["Sessions"])
    app.include_router(api_keys.router, prefix="/api-keys", tags=["API Keys"])
    app.include_router(oauth.router, prefix="/oauth", tags=["OAuth"])
    
    return app


app = create_app()


def main():
    """Entry point for running the service."""
    import uvicorn
    
    uvicorn.run(
        "src.main:app",
        host=settings.server.host,
        port=settings.server.port,
        reload=settings.debug,
        log_level=settings.logging.level.lower(),
    )


if __name__ == "__main__":
    main()
