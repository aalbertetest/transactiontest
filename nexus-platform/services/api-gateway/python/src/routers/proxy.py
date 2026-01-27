# =============================================================================
# NEXUS PLATFORM - API GATEWAY - PROXY ROUTER
# =============================================================================
# Dynamic reverse proxy for routing requests to backend services.
# =============================================================================

"""
Proxy Router

This module implements the core proxy functionality of the API Gateway,
routing requests to appropriate backend services based on path mapping.

Features:
- Path-based routing
- Request/response transformation
- Header forwarding
- Error handling
- Retry logic
- Streaming response support
"""

import time
from typing import Dict, Optional

import httpx
import structlog
from fastapi import APIRouter, Request, Response
from fastapi.responses import StreamingResponse

from ..services.service_discovery import ServiceDiscovery
from ..middleware.circuit_breaker import with_circuit_breaker
from ..middleware.metrics import record_upstream_duration
from ..utils.errors import NotFoundError, ServiceUnavailable, TimeoutError

logger = structlog.get_logger(__name__)

router = APIRouter()


# Service routing configuration
# Maps URL path prefixes to backend services
SERVICE_ROUTES: Dict[str, str] = {
    "/auth": "auth-service",
    "/users": "user-service",
    "/payments": "payment-service",
    "/workflows": "workflow-engine",
    "/queue": "distributed-queue",
    "/stream": "streaming-platform",
    "/cache": "cache-layer",
    "/scheduler": "scheduler-service",
    "/workers": "worker-fleet",
}

# Headers to forward from client to backend
FORWARD_HEADERS = {
    "accept",
    "accept-encoding",
    "accept-language",
    "content-type",
    "content-length",
    "user-agent",
    "x-request-id",
    "x-correlation-id",
    "x-forwarded-for",
    "x-forwarded-proto",
    "x-real-ip",
    "authorization",
}

# Headers to exclude from forwarding
EXCLUDED_HEADERS = {
    "host",
    "connection",
    "keep-alive",
    "transfer-encoding",
    "te",
    "trailer",
    "upgrade",
}

# Headers to add to backend requests
def get_proxy_headers(request: Request) -> Dict[str, str]:
    """
    Build headers to forward to backend services.
    
    Args:
        request: The incoming request.
    
    Returns:
        Dict: Headers to forward.
    """
    headers = {}
    
    # Forward allowed headers
    for key, value in request.headers.items():
        key_lower = key.lower()
        if key_lower in FORWARD_HEADERS and key_lower not in EXCLUDED_HEADERS:
            headers[key] = value
    
    # Add gateway-specific headers
    headers["X-Gateway-Request-Id"] = getattr(request.state, "request_id", "unknown")
    
    # Add user info if authenticated
    user = getattr(request.state, "user", None)
    if user:
        headers["X-User-Id"] = user.user_id
        if user.tenant_id:
            headers["X-Tenant-Id"] = user.tenant_id
        if user.roles:
            headers["X-User-Roles"] = ",".join(user.roles)
    
    # Add forwarding info
    client_ip = request.headers.get("X-Forwarded-For")
    if not client_ip and request.client:
        client_ip = request.client.host
    if client_ip:
        headers["X-Forwarded-For"] = client_ip
    
    headers["X-Forwarded-Proto"] = request.url.scheme
    headers["X-Forwarded-Host"] = request.headers.get("Host", request.url.netloc)
    
    return headers


def get_target_service(path: str) -> Optional[str]:
    """
    Determine the target service based on request path.
    
    Args:
        path: The request path.
    
    Returns:
        Optional[str]: The target service name, or None if no match.
    """
    for prefix, service in SERVICE_ROUTES.items():
        if path.startswith(prefix):
            return service
    return None


def transform_path(path: str, service: str) -> str:
    """
    Transform the request path for the backend service.
    
    By default, removes the service prefix from the path.
    
    Args:
        path: The original request path.
        service: The target service name.
    
    Returns:
        str: The transformed path.
    """
    # Find the matching prefix
    for prefix, svc in SERVICE_ROUTES.items():
        if svc == service and path.startswith(prefix):
            # Remove the prefix
            transformed = path[len(prefix):] or "/"
            return transformed
    
    return path


async def proxy_request(
    request: Request,
    service: str,
    target_path: str,
) -> Response:
    """
    Proxy a request to a backend service.
    
    Args:
        request: The incoming request.
        service: Target service name.
        target_path: Path on the target service.
    
    Returns:
        Response: The proxied response.
    """
    app_state = getattr(request.app.state, "app_state", None)
    http_client = getattr(app_state, "http_client", None)
    service_discovery: ServiceDiscovery = getattr(app_state, "service_discovery", None)
    
    if not http_client:
        raise ServiceUnavailable(
            service="gateway",
            message="HTTP client not initialized",
        )
    
    # Get service endpoint
    if service_discovery:
        endpoint = await service_discovery.get_endpoint(service)
    else:
        # Fallback to static configuration
        settings = getattr(app_state, "settings", None)
        endpoint = getattr(settings.backend, f"{service.replace('-', '_')}_url", None)
    
    if not endpoint:
        raise NotFoundError(
            resource_type="service",
            resource_id=service,
            message=f"Service '{service}' not found",
        )
    
    # Build target URL
    target_url = f"{endpoint}{target_path}"
    if request.url.query:
        target_url = f"{target_url}?{request.url.query}"
    
    # Build headers
    headers = get_proxy_headers(request)
    
    # Get request body
    body = await request.body()
    
    # Log the proxy request
    logger.debug(
        "Proxying request",
        service=service,
        method=request.method,
        target_url=target_url,
        request_id=getattr(request.state, "request_id", None),
    )
    
    start_time = time.perf_counter()
    
    try:
        # Make the request with circuit breaker protection
        async def make_request():
            return await http_client.request(
                method=request.method,
                url=target_url,
                headers=headers,
                content=body if body else None,
                follow_redirects=False,
            )
        
        response = await with_circuit_breaker(
            service,
            make_request,
        )
        
        duration = time.perf_counter() - start_time
        
        # Record metrics
        record_upstream_duration(
            service=service,
            method=request.method,
            status=response.status_code,
            duration=duration,
        )
        
        logger.debug(
            "Upstream response received",
            service=service,
            status_code=response.status_code,
            duration_ms=round(duration * 1000, 2),
            request_id=getattr(request.state, "request_id", None),
        )
        
        # Build response headers (exclude hop-by-hop headers)
        response_headers = {}
        for key, value in response.headers.items():
            key_lower = key.lower()
            if key_lower not in EXCLUDED_HEADERS:
                response_headers[key] = value
        
        # Add gateway headers
        response_headers["X-Gateway-Request-Id"] = getattr(
            request.state, "request_id", "unknown"
        )
        response_headers["X-Upstream-Service"] = service
        response_headers["X-Upstream-Duration-Ms"] = str(round(duration * 1000, 2))
        
        # Return streaming response for large bodies
        if response.headers.get("content-length"):
            content_length = int(response.headers.get("content-length", 0))
            if content_length > 1024 * 1024:  # 1MB threshold
                return StreamingResponse(
                    content=response.aiter_bytes(),
                    status_code=response.status_code,
                    headers=response_headers,
                    media_type=response.headers.get("content-type"),
                )
        
        return Response(
            content=response.content,
            status_code=response.status_code,
            headers=response_headers,
            media_type=response.headers.get("content-type"),
        )
        
    except httpx.TimeoutException as e:
        duration = time.perf_counter() - start_time
        record_upstream_duration(
            service=service,
            method=request.method,
            status=504,
            duration=duration,
        )
        
        logger.error(
            "Upstream request timeout",
            service=service,
            target_url=target_url,
            duration_ms=round(duration * 1000, 2),
            request_id=getattr(request.state, "request_id", None),
        )
        
        raise TimeoutError(
            service=service,
            timeout=duration,
        )
        
    except httpx.ConnectError as e:
        logger.error(
            "Failed to connect to upstream service",
            service=service,
            target_url=target_url,
            error=str(e),
            request_id=getattr(request.state, "request_id", None),
        )
        
        raise ServiceUnavailable(
            service=service,
            message=f"Failed to connect: {str(e)}",
        )
        
    except Exception as e:
        logger.exception(
            "Unexpected error proxying request",
            service=service,
            target_url=target_url,
            request_id=getattr(request.state, "request_id", None),
        )
        raise


@router.api_route(
    "/{path:path}",
    methods=["GET", "POST", "PUT", "DELETE", "PATCH", "HEAD", "OPTIONS"],
    include_in_schema=False,
)
async def proxy_all(request: Request, path: str) -> Response:
    """
    Catch-all proxy endpoint.
    
    Routes all requests that don't match specific endpoints
    to the appropriate backend service.
    
    Args:
        request: The incoming request.
        path: The request path.
    
    Returns:
        Response: The proxied response.
    """
    # Add leading slash
    full_path = f"/{path}"
    
    # Find target service
    service = get_target_service(full_path)
    
    if not service:
        raise NotFoundError(
            message=f"No service found for path: {full_path}",
            details={"path": full_path},
        )
    
    # Transform path for backend
    target_path = transform_path(full_path, service)
    
    return await proxy_request(request, service, target_path)
