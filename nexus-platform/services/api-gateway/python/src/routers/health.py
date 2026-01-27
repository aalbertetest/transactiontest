# =============================================================================
# NEXUS PLATFORM - API GATEWAY - HEALTH CHECK ROUTER
# =============================================================================
# Health check endpoints for Kubernetes probes and monitoring.
# =============================================================================

"""
Health Check Router

This module provides health check endpoints for:
- /health - Comprehensive health status with dependency checks
- /ready - Readiness probe for Kubernetes
- /live - Liveness probe for Kubernetes

Health checks follow Kubernetes health probe conventions and provide
detailed status information for monitoring and debugging.
"""

import asyncio
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

import structlog
from fastapi import APIRouter, Depends, Request, Response, status
from pydantic import BaseModel, Field

logger = structlog.get_logger(__name__)

router = APIRouter()


class HealthStatus(str, Enum):
    """Health status enumeration."""
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


class DependencyHealth(BaseModel):
    """Health status of a dependency."""
    name: str = Field(..., description="Dependency name")
    status: HealthStatus = Field(..., description="Health status")
    latency_ms: Optional[float] = Field(None, description="Latency in milliseconds")
    message: Optional[str] = Field(None, description="Status message")
    last_check: Optional[datetime] = Field(None, description="Last check timestamp")


class HealthResponse(BaseModel):
    """Comprehensive health check response."""
    status: HealthStatus = Field(..., description="Overall health status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    uptime_seconds: float = Field(..., description="Service uptime in seconds")
    timestamp: datetime = Field(..., description="Check timestamp")
    dependencies: List[DependencyHealth] = Field(
        default=[],
        description="Health of dependencies"
    )
    checks: Dict[str, bool] = Field(
        default={},
        description="Individual check results"
    )


class ReadinessResponse(BaseModel):
    """Readiness probe response."""
    ready: bool = Field(..., description="Whether service is ready")
    message: str = Field(..., description="Status message")


class LivenessResponse(BaseModel):
    """Liveness probe response."""
    alive: bool = Field(..., description="Whether service is alive")
    message: str = Field(..., description="Status message")


async def check_redis_health(request: Request) -> DependencyHealth:
    """
    Check Redis connection health.
    
    Args:
        request: The incoming request.
    
    Returns:
        DependencyHealth: Redis health status.
    """
    import time
    
    app_state = getattr(request.app.state, "app_state", None)
    redis_client = getattr(app_state, "redis_client", None) if app_state else None
    
    if not redis_client:
        return DependencyHealth(
            name="redis",
            status=HealthStatus.UNHEALTHY,
            message="Redis client not configured",
        )
    
    start = time.perf_counter()
    try:
        await asyncio.wait_for(redis_client.ping(), timeout=2.0)
        latency = (time.perf_counter() - start) * 1000
        
        return DependencyHealth(
            name="redis",
            status=HealthStatus.HEALTHY,
            latency_ms=round(latency, 2),
            last_check=datetime.now(timezone.utc),
        )
    except asyncio.TimeoutError:
        return DependencyHealth(
            name="redis",
            status=HealthStatus.UNHEALTHY,
            message="Connection timeout",
            last_check=datetime.now(timezone.utc),
        )
    except Exception as e:
        return DependencyHealth(
            name="redis",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
            last_check=datetime.now(timezone.utc),
        )


async def check_database_health(request: Request) -> DependencyHealth:
    """
    Check database connection health.
    
    Args:
        request: The incoming request.
    
    Returns:
        DependencyHealth: Database health status.
    """
    import time
    
    app_state = getattr(request.app.state, "app_state", None)
    db_pool = getattr(app_state, "db_pool", None) if app_state else None
    
    if not db_pool:
        return DependencyHealth(
            name="database",
            status=HealthStatus.HEALTHY,  # Not configured, but that's OK
            message="Database not configured",
        )
    
    start = time.perf_counter()
    try:
        async with db_pool() as session:
            await asyncio.wait_for(
                session.execute("SELECT 1"),
                timeout=2.0,
            )
        latency = (time.perf_counter() - start) * 1000
        
        return DependencyHealth(
            name="database",
            status=HealthStatus.HEALTHY,
            latency_ms=round(latency, 2),
            last_check=datetime.now(timezone.utc),
        )
    except asyncio.TimeoutError:
        return DependencyHealth(
            name="database",
            status=HealthStatus.UNHEALTHY,
            message="Connection timeout",
            last_check=datetime.now(timezone.utc),
        )
    except Exception as e:
        return DependencyHealth(
            name="database",
            status=HealthStatus.UNHEALTHY,
            message=str(e),
            last_check=datetime.now(timezone.utc),
        )


async def check_upstream_services(request: Request) -> List[DependencyHealth]:
    """
    Check health of upstream services via service discovery.
    
    Args:
        request: The incoming request.
    
    Returns:
        List[DependencyHealth]: Health status of upstream services.
    """
    app_state = getattr(request.app.state, "app_state", None)
    service_discovery = getattr(app_state, "service_discovery", None) if app_state else None
    
    if not service_discovery:
        return []
    
    results = []
    services = ["auth-service", "user-service", "payment-service"]
    
    for service in services:
        try:
            # Simple check - just verify service is registered
            endpoint = await service_discovery.get_endpoint(service)
            results.append(DependencyHealth(
                name=service,
                status=HealthStatus.HEALTHY if endpoint else HealthStatus.UNHEALTHY,
                message=f"Endpoint: {endpoint}" if endpoint else "Service not found",
                last_check=datetime.now(timezone.utc),
            ))
        except Exception as e:
            results.append(DependencyHealth(
                name=service,
                status=HealthStatus.UNHEALTHY,
                message=str(e),
                last_check=datetime.now(timezone.utc),
            ))
    
    return results


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Comprehensive Health Check",
    description="Returns detailed health status including all dependencies.",
    responses={
        200: {"description": "Service is healthy"},
        503: {"description": "Service is unhealthy"},
    },
)
async def health_check(request: Request) -> HealthResponse:
    """
    Comprehensive health check endpoint.
    
    This endpoint performs health checks on all dependencies and
    returns a detailed status report.
    
    Returns:
        HealthResponse: Comprehensive health status.
    """
    app_state = getattr(request.app.state, "app_state", None)
    settings = getattr(app_state, "settings", None) if app_state else None
    startup_time = getattr(app_state, "startup_time", None) if app_state else None
    
    # Calculate uptime
    if startup_time:
        uptime = (datetime.now(timezone.utc) - startup_time).total_seconds()
    else:
        uptime = 0.0
    
    # Run dependency health checks concurrently
    redis_health, db_health, upstream_health = await asyncio.gather(
        check_redis_health(request),
        check_database_health(request),
        check_upstream_services(request),
        return_exceptions=True,
    )
    
    dependencies = []
    
    # Process results (handle exceptions)
    if isinstance(redis_health, DependencyHealth):
        dependencies.append(redis_health)
    else:
        dependencies.append(DependencyHealth(
            name="redis",
            status=HealthStatus.UNHEALTHY,
            message=str(redis_health),
        ))
    
    if isinstance(db_health, DependencyHealth):
        dependencies.append(db_health)
    else:
        dependencies.append(DependencyHealth(
            name="database",
            status=HealthStatus.UNHEALTHY,
            message=str(db_health),
        ))
    
    if isinstance(upstream_health, list):
        dependencies.extend(upstream_health)
    
    # Determine overall status
    unhealthy_count = sum(
        1 for d in dependencies 
        if d.status == HealthStatus.UNHEALTHY
    )
    degraded_count = sum(
        1 for d in dependencies 
        if d.status == HealthStatus.DEGRADED
    )
    
    if unhealthy_count > 0:
        overall_status = HealthStatus.UNHEALTHY
    elif degraded_count > 0:
        overall_status = HealthStatus.DEGRADED
    else:
        overall_status = HealthStatus.HEALTHY
    
    # Build checks dict
    checks = {
        "redis": dependencies[0].status == HealthStatus.HEALTHY if dependencies else False,
        "database": dependencies[1].status == HealthStatus.HEALTHY if len(dependencies) > 1 else True,
    }
    
    response = HealthResponse(
        status=overall_status,
        service=settings.service_name if settings else "api-gateway",
        version=settings.service_version if settings else "1.0.0",
        uptime_seconds=round(uptime, 2),
        timestamp=datetime.now(timezone.utc),
        dependencies=dependencies,
        checks=checks,
    )
    
    return response


@router.get(
    "/ready",
    response_model=ReadinessResponse,
    summary="Readiness Probe",
    description="Kubernetes readiness probe endpoint.",
    responses={
        200: {"description": "Service is ready"},
        503: {"description": "Service is not ready"},
    },
)
async def readiness_check(request: Request, response: Response) -> ReadinessResponse:
    """
    Kubernetes readiness probe endpoint.
    
    Returns 200 if the service is ready to accept traffic,
    503 if it's not ready (e.g., during startup or shutdown).
    
    Returns:
        ReadinessResponse: Readiness status.
    """
    app_state = getattr(request.app.state, "app_state", None)
    
    # Check if service is shutting down
    if app_state and app_state.is_shutting_down:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ReadinessResponse(
            ready=False,
            message="Service is shutting down",
        )
    
    # Check Redis connection (required for rate limiting)
    redis_health = await check_redis_health(request)
    if redis_health.status == HealthStatus.UNHEALTHY:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        return ReadinessResponse(
            ready=False,
            message=f"Redis unhealthy: {redis_health.message}",
        )
    
    return ReadinessResponse(
        ready=True,
        message="Service is ready",
    )


@router.get(
    "/live",
    response_model=LivenessResponse,
    summary="Liveness Probe",
    description="Kubernetes liveness probe endpoint.",
    responses={
        200: {"description": "Service is alive"},
        503: {"description": "Service is not alive"},
    },
)
async def liveness_check() -> LivenessResponse:
    """
    Kubernetes liveness probe endpoint.
    
    Returns 200 if the service process is running.
    This is a simple check that doesn't verify dependencies.
    
    Returns:
        LivenessResponse: Liveness status.
    """
    # Simple liveness check - if we can respond, we're alive
    return LivenessResponse(
        alive=True,
        message="Service is alive",
    )
