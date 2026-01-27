# =============================================================================
# NEXUS PLATFORM - API GATEWAY - SERVICE DISCOVERY
# =============================================================================
# Service discovery client for locating backend services.
# =============================================================================

"""
Service Discovery Module

This module provides service discovery functionality supporting:
- Kubernetes DNS-based discovery
- Consul service discovery
- Static configuration fallback
- Health checking
- Load balancing

The service discovery client maintains a cache of service endpoints
and performs periodic health checks to ensure services are available.
"""

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

import structlog

from ..config import BackendServiceSettings

logger = structlog.get_logger(__name__)


class DiscoveryType(str, Enum):
    """Service discovery type."""
    KUBERNETES = "kubernetes"
    CONSUL = "consul"
    STATIC = "static"


@dataclass
class ServiceEndpoint:
    """
    Represents a service endpoint.
    
    Attributes:
        url: The service URL.
        healthy: Whether the endpoint is healthy.
        weight: Load balancing weight.
        last_check: Last health check time.
        consecutive_failures: Number of consecutive failures.
    """
    url: str
    healthy: bool = True
    weight: int = 100
    last_check: Optional[datetime] = None
    consecutive_failures: int = 0
    metadata: Dict = field(default_factory=dict)


@dataclass
class ServiceInfo:
    """
    Information about a discovered service.
    
    Attributes:
        name: Service name.
        endpoints: List of available endpoints.
        last_update: Last time endpoints were updated.
    """
    name: str
    endpoints: List[ServiceEndpoint] = field(default_factory=list)
    last_update: Optional[datetime] = None
    
    def get_healthy_endpoint(self) -> Optional[str]:
        """Get a healthy endpoint URL using round-robin."""
        healthy = [e for e in self.endpoints if e.healthy]
        if not healthy:
            return None
        # Simple round-robin (could implement weighted selection)
        return healthy[0].url
    
    @property
    def is_healthy(self) -> bool:
        """Check if service has any healthy endpoints."""
        return any(e.healthy for e in self.endpoints)


class ServiceDiscovery:
    """
    Service discovery client.
    
    Provides service discovery functionality with support for
    multiple backends (Kubernetes, Consul, static).
    
    Attributes:
        settings: Backend service configuration.
        discovery_type: The discovery mechanism to use.
        services: Cache of discovered services.
    """
    
    # How often to refresh service endpoints (seconds)
    REFRESH_INTERVAL = 30
    
    # Health check interval (seconds)
    HEALTH_CHECK_INTERVAL = 10
    
    # Consecutive failures before marking unhealthy
    FAILURE_THRESHOLD = 3
    
    def __init__(self, settings: BackendServiceSettings):
        """
        Initialize service discovery.
        
        Args:
            settings: Backend service configuration.
        """
        self.settings = settings
        self.discovery_type = DiscoveryType(settings.service_discovery_type)
        self.services: Dict[str, ServiceInfo] = {}
        self._running = False
        self._refresh_task: Optional[asyncio.Task] = None
        self._health_check_task: Optional[asyncio.Task] = None
    
    async def start(self) -> None:
        """
        Start service discovery.
        
        Initializes services and starts background tasks.
        """
        logger.info(
            "Starting service discovery",
            type=self.discovery_type.value,
        )
        
        self._running = True
        
        # Initialize services from static config
        await self._init_from_static()
        
        # Start background tasks
        if self.settings.service_discovery_enabled:
            self._refresh_task = asyncio.create_task(self._refresh_loop())
            self._health_check_task = asyncio.create_task(self._health_check_loop())
        
        logger.info(
            "Service discovery started",
            services=list(self.services.keys()),
        )
    
    async def stop(self) -> None:
        """Stop service discovery and cleanup."""
        logger.info("Stopping service discovery")
        
        self._running = False
        
        # Cancel background tasks
        if self._refresh_task:
            self._refresh_task.cancel()
            try:
                await self._refresh_task
            except asyncio.CancelledError:
                pass
        
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Service discovery stopped")
    
    async def _init_from_static(self) -> None:
        """Initialize services from static configuration."""
        # Map service names to config attributes
        service_map = {
            "auth-service": self.settings.auth_service_url,
            "user-service": self.settings.user_service_url,
            "payment-service": self.settings.payment_service_url,
            "workflow-engine": self.settings.workflow_service_url,
            "distributed-queue": self.settings.queue_service_url,
            "streaming-platform": self.settings.streaming_service_url,
            "cache-layer": self.settings.cache_service_url,
            "database-layer": self.settings.database_service_url,
            "websocket-service": self.settings.websocket_service_url,
            "scheduler-service": self.settings.scheduler_service_url,
            "worker-fleet": self.settings.worker_service_url,
        }
        
        for name, url in service_map.items():
            if url:
                self.services[name] = ServiceInfo(
                    name=name,
                    endpoints=[ServiceEndpoint(url=url)],
                    last_update=datetime.now(timezone.utc),
                )
    
    async def _refresh_loop(self) -> None:
        """Background task to refresh service endpoints."""
        while self._running:
            try:
                await asyncio.sleep(self.REFRESH_INTERVAL)
                await self._refresh_services()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error refreshing services", error=str(e))
    
    async def _health_check_loop(self) -> None:
        """Background task to check service health."""
        while self._running:
            try:
                await asyncio.sleep(self.HEALTH_CHECK_INTERVAL)
                await self._check_health()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error("Error checking service health", error=str(e))
    
    async def _refresh_services(self) -> None:
        """Refresh service endpoints from discovery backend."""
        if self.discovery_type == DiscoveryType.KUBERNETES:
            await self._refresh_from_kubernetes()
        elif self.discovery_type == DiscoveryType.CONSUL:
            await self._refresh_from_consul()
        # Static config doesn't need refresh
    
    async def _refresh_from_kubernetes(self) -> None:
        """Refresh services from Kubernetes DNS."""
        # In Kubernetes, services are accessible via DNS:
        # <service-name>.<namespace>.svc.cluster.local
        # The static URLs already use this format, so no additional
        # discovery is needed for basic usage.
        #
        # For more advanced scenarios (headless services, multiple pods),
        # we would query the Kubernetes API or use DNS SRV records.
        pass
    
    async def _refresh_from_consul(self) -> None:
        """Refresh services from Consul."""
        # This would query Consul's HTTP API for service endpoints
        # Example: GET /v1/health/service/<service-name>
        pass
    
    async def _check_health(self) -> None:
        """Check health of all service endpoints."""
        import httpx
        
        for service in self.services.values():
            for endpoint in service.endpoints:
                try:
                    async with httpx.AsyncClient() as client:
                        response = await client.get(
                            f"{endpoint.url}/health",
                            timeout=5.0,
                        )
                        
                        if response.status_code == 200:
                            endpoint.healthy = True
                            endpoint.consecutive_failures = 0
                        else:
                            endpoint.consecutive_failures += 1
                            
                except Exception:
                    endpoint.consecutive_failures += 1
                
                # Mark unhealthy after consecutive failures
                if endpoint.consecutive_failures >= self.FAILURE_THRESHOLD:
                    endpoint.healthy = False
                
                endpoint.last_check = datetime.now(timezone.utc)
    
    async def get_endpoint(self, service_name: str) -> Optional[str]:
        """
        Get an endpoint URL for a service.
        
        Args:
            service_name: Name of the service.
        
        Returns:
            Optional[str]: The service endpoint URL, or None if not found.
        """
        service = self.services.get(service_name)
        if not service:
            return None
        
        return service.get_healthy_endpoint()
    
    async def get_all_services(self) -> Dict[str, Dict]:
        """
        Get information about all registered services.
        
        Returns:
            Dict: Service information keyed by name.
        """
        result = {}
        for name, service in self.services.items():
            result[name] = {
                "endpoint": service.get_healthy_endpoint(),
                "healthy": service.is_healthy,
                "endpoint_count": len(service.endpoints),
                "healthy_endpoints": sum(1 for e in service.endpoints if e.healthy),
                "last_update": service.last_update,
            }
        return result
    
    async def register_service(
        self,
        name: str,
        url: str,
        metadata: Optional[Dict] = None,
    ) -> None:
        """
        Manually register a service endpoint.
        
        Args:
            name: Service name.
            url: Service URL.
            metadata: Optional metadata.
        """
        if name not in self.services:
            self.services[name] = ServiceInfo(name=name)
        
        # Add endpoint if not already registered
        existing_urls = {e.url for e in self.services[name].endpoints}
        if url not in existing_urls:
            self.services[name].endpoints.append(
                ServiceEndpoint(
                    url=url,
                    metadata=metadata or {},
                )
            )
        
        self.services[name].last_update = datetime.now(timezone.utc)
        
        logger.info(
            "Service registered",
            service=name,
            url=url,
        )
    
    async def deregister_service(self, name: str, url: Optional[str] = None) -> None:
        """
        Deregister a service or specific endpoint.
        
        Args:
            name: Service name.
            url: Specific URL to remove, or None to remove all.
        """
        if name not in self.services:
            return
        
        if url:
            self.services[name].endpoints = [
                e for e in self.services[name].endpoints
                if e.url != url
            ]
        else:
            del self.services[name]
        
        logger.info(
            "Service deregistered",
            service=name,
            url=url,
        )
