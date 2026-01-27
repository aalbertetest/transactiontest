# =============================================================================
# NEXUS PLATFORM - API GATEWAY - ADMIN ROUTER
# =============================================================================
# Administrative endpoints for gateway management.
# =============================================================================

"""
Admin Router

This module provides administrative endpoints for managing the API Gateway:
- Configuration viewing
- Circuit breaker management
- Cache management
- Service discovery information
- Runtime statistics

All admin endpoints require admin authentication and are not
exposed in the public API documentation.
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional

import structlog
from fastapi import APIRouter, Depends, Request
from pydantic import BaseModel, Field

from ..middleware.authentication import require_roles, AuthenticatedUser
from ..middleware.circuit_breaker import get_registry

logger = structlog.get_logger(__name__)

router = APIRouter()


class CircuitBreakerState(BaseModel):
    """Circuit breaker state information."""
    service: str
    state: str
    failure_count: int
    success_count: int
    last_failure: Optional[float]
    last_state_change: float
    time_in_state: float


class CircuitBreakerListResponse(BaseModel):
    """Response containing all circuit breaker states."""
    circuit_breakers: List[CircuitBreakerState]


class CircuitBreakerResetRequest(BaseModel):
    """Request to reset a circuit breaker."""
    service: Optional[str] = Field(
        None,
        description="Service name to reset, or None to reset all"
    )


class GatewayStatsResponse(BaseModel):
    """Gateway runtime statistics."""
    uptime_seconds: float
    total_requests: int
    active_requests: int
    error_count: int
    circuit_breakers_open: int
    cache_hit_rate: Optional[float]
    services_healthy: int
    services_unhealthy: int


class ServiceInfo(BaseModel):
    """Information about a registered service."""
    name: str
    endpoint: str
    healthy: bool
    last_check: Optional[datetime]


class ServiceListResponse(BaseModel):
    """Response containing registered services."""
    services: List[ServiceInfo]


class ConfigResponse(BaseModel):
    """Non-sensitive configuration information."""
    environment: str
    service_name: str
    service_version: str
    rate_limiting_enabled: bool
    circuit_breaker_enabled: bool
    tracing_enabled: bool
    cache_enabled: bool


@router.get(
    "/circuit-breakers",
    response_model=CircuitBreakerListResponse,
    summary="List Circuit Breakers",
    description="Get the state of all circuit breakers.",
)
async def list_circuit_breakers(
    request: Request,
    user: AuthenticatedUser = Depends(require_roles("admin")),
) -> CircuitBreakerListResponse:
    """
    List all circuit breakers and their states.
    
    Requires admin role.
    
    Returns:
        CircuitBreakerListResponse: List of circuit breaker states.
    """
    registry = get_registry()
    states = registry.get_all_states()
    
    circuit_breakers = [
        CircuitBreakerState(**state)
        for state in states.values()
    ]
    
    return CircuitBreakerListResponse(circuit_breakers=circuit_breakers)


@router.post(
    "/circuit-breakers/reset",
    summary="Reset Circuit Breaker",
    description="Reset a circuit breaker to closed state.",
)
async def reset_circuit_breaker(
    request: Request,
    reset_request: CircuitBreakerResetRequest,
    user: AuthenticatedUser = Depends(require_roles("admin")),
) -> Dict:
    """
    Reset a circuit breaker to closed state.
    
    Args:
        reset_request: Request specifying which circuit breaker to reset.
    
    Returns:
        Dict: Success message.
    """
    registry = get_registry()
    await registry.reset(reset_request.service)
    
    logger.info(
        "Circuit breaker reset",
        service=reset_request.service or "all",
        reset_by=user.user_id,
    )
    
    return {
        "success": True,
        "message": f"Circuit breaker(s) reset: {reset_request.service or 'all'}",
    }


@router.get(
    "/services",
    response_model=ServiceListResponse,
    summary="List Services",
    description="Get list of registered backend services.",
)
async def list_services(
    request: Request,
    user: AuthenticatedUser = Depends(require_roles("admin")),
) -> ServiceListResponse:
    """
    List all registered backend services.
    
    Returns:
        ServiceListResponse: List of services and their health status.
    """
    app_state = getattr(request.app.state, "app_state", None)
    service_discovery = getattr(app_state, "service_discovery", None)
    
    services = []
    
    if service_discovery:
        registered = await service_discovery.get_all_services()
        for name, info in registered.items():
            services.append(ServiceInfo(
                name=name,
                endpoint=info.get("endpoint", "unknown"),
                healthy=info.get("healthy", False),
                last_check=info.get("last_check"),
            ))
    
    return ServiceListResponse(services=services)


@router.get(
    "/stats",
    response_model=GatewayStatsResponse,
    summary="Gateway Statistics",
    description="Get runtime statistics for the gateway.",
)
async def get_stats(
    request: Request,
    user: AuthenticatedUser = Depends(require_roles("admin")),
) -> GatewayStatsResponse:
    """
    Get gateway runtime statistics.
    
    Returns:
        GatewayStatsResponse: Runtime statistics.
    """
    app_state = getattr(request.app.state, "app_state", None)
    
    # Calculate uptime
    startup_time = getattr(app_state, "startup_time", datetime.now(timezone.utc))
    uptime = (datetime.now(timezone.utc) - startup_time).total_seconds()
    
    # Get circuit breaker stats
    registry = get_registry()
    cb_states = registry.get_all_states()
    open_count = sum(
        1 for s in cb_states.values()
        if s.get("state") == "open"
    )
    
    # Get service health
    service_discovery = getattr(app_state, "service_discovery", None)
    healthy_count = 0
    unhealthy_count = 0
    
    if service_discovery:
        services = await service_discovery.get_all_services()
        for info in services.values():
            if info.get("healthy"):
                healthy_count += 1
            else:
                unhealthy_count += 1
    
    return GatewayStatsResponse(
        uptime_seconds=round(uptime, 2),
        total_requests=getattr(app_state, "request_count", 0),
        active_requests=0,  # Would need to track this
        error_count=0,  # Would need to track this
        circuit_breakers_open=open_count,
        cache_hit_rate=None,  # Would need to calculate
        services_healthy=healthy_count,
        services_unhealthy=unhealthy_count,
    )


@router.get(
    "/config",
    response_model=ConfigResponse,
    summary="Gateway Configuration",
    description="Get non-sensitive gateway configuration.",
)
async def get_config(
    request: Request,
    user: AuthenticatedUser = Depends(require_roles("admin")),
) -> ConfigResponse:
    """
    Get non-sensitive gateway configuration.
    
    Returns:
        ConfigResponse: Gateway configuration.
    """
    app_state = getattr(request.app.state, "app_state", None)
    settings = getattr(app_state, "settings", None)
    
    if not settings:
        from ..config import get_settings
        settings = get_settings()
    
    return ConfigResponse(
        environment=settings.environment.value,
        service_name=settings.service_name,
        service_version=settings.service_version,
        rate_limiting_enabled=settings.rate_limit.enabled,
        circuit_breaker_enabled=settings.circuit_breaker.enabled,
        tracing_enabled=settings.tracing.enabled,
        cache_enabled=settings.cache.enabled,
    )


@router.post(
    "/cache/clear",
    summary="Clear Cache",
    description="Clear the gateway response cache.",
)
async def clear_cache(
    request: Request,
    pattern: Optional[str] = None,
    user: AuthenticatedUser = Depends(require_roles("admin")),
) -> Dict:
    """
    Clear the gateway response cache.
    
    Args:
        pattern: Optional pattern to match keys to clear.
    
    Returns:
        Dict: Success message.
    """
    app_state = getattr(request.app.state, "app_state", None)
    redis_client = getattr(app_state, "redis_client", None)
    settings = getattr(app_state, "settings", None)
    
    if not redis_client:
        return {
            "success": False,
            "message": "Cache not configured",
        }
    
    # Clear cache keys matching pattern
    cache_prefix = settings.cache.redis_prefix if settings else "nexus:gateway:cache:"
    
    if pattern:
        search_pattern = f"{cache_prefix}{pattern}*"
    else:
        search_pattern = f"{cache_prefix}*"
    
    # Use SCAN to find keys (safe for large datasets)
    keys_deleted = 0
    cursor = 0
    
    while True:
        cursor, keys = await redis_client.scan(
            cursor=cursor,
            match=search_pattern,
            count=100,
        )
        
        if keys:
            await redis_client.delete(*keys)
            keys_deleted += len(keys)
        
        if cursor == 0:
            break
    
    logger.info(
        "Cache cleared",
        pattern=pattern or "all",
        keys_deleted=keys_deleted,
        cleared_by=user.user_id,
    )
    
    return {
        "success": True,
        "message": f"Cache cleared: {keys_deleted} keys deleted",
        "keys_deleted": keys_deleted,
    }


@router.post(
    "/reload",
    summary="Reload Configuration",
    description="Reload gateway configuration without restart.",
)
async def reload_config(
    request: Request,
    user: AuthenticatedUser = Depends(require_roles("admin")),
) -> Dict:
    """
    Reload gateway configuration.
    
    Note: Not all configuration changes can be applied without restart.
    
    Returns:
        Dict: Reload status.
    """
    from ..config import get_settings
    
    # Clear settings cache
    get_settings.cache_clear()
    
    # Reload settings
    new_settings = get_settings()
    
    # Update app state
    app_state = getattr(request.app.state, "app_state", None)
    if app_state:
        app_state.settings = new_settings
    
    logger.info(
        "Configuration reloaded",
        reloaded_by=user.user_id,
    )
    
    return {
        "success": True,
        "message": "Configuration reloaded",
        "note": "Some settings require restart to take effect",
    }
