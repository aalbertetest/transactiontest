# =============================================================================
# NEXUS PLATFORM - API GATEWAY - CIRCUIT BREAKER MIDDLEWARE
# =============================================================================
# Circuit breaker pattern implementation for fault tolerance.
# =============================================================================

"""
Circuit Breaker Middleware

This middleware implements the circuit breaker pattern to prevent
cascading failures when backend services are unhealthy.

States:
- CLOSED: Normal operation, requests flow through
- OPEN: Circuit is tripped, requests fail immediately
- HALF_OPEN: Testing if service has recovered

Features:
- Per-service circuit breakers
- Configurable failure thresholds
- Automatic recovery testing
- Metrics and alerting integration
- Graceful degradation support
"""

import asyncio
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, Optional

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import CircuitBreakerSettings
from ..utils.errors import ServiceUnavailable

logger = structlog.get_logger(__name__)


class CircuitState(Enum):
    """Circuit breaker states."""
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


@dataclass
class CircuitBreaker:
    """
    Circuit breaker for a single service.
    
    Tracks failures and manages state transitions for a single
    backend service.
    
    Attributes:
        service_name: Name of the service being protected.
        failure_threshold: Failures before opening circuit.
        success_threshold: Successes needed to close from half-open.
        timeout: Time in seconds before testing recovery.
        state: Current circuit state.
        failure_count: Current failure count.
        success_count: Success count in half-open state.
        last_failure_time: Timestamp of last failure.
        last_state_change: Timestamp of last state change.
    """
    service_name: str
    failure_threshold: int = 5
    success_threshold: int = 3
    timeout: int = 60
    state: CircuitState = CircuitState.CLOSED
    failure_count: int = 0
    success_count: int = 0
    last_failure_time: float = 0.0
    last_state_change: float = field(default_factory=time.time)
    
    # Lock for thread-safe state updates
    _lock: asyncio.Lock = field(default_factory=asyncio.Lock)
    
    async def record_success(self) -> None:
        """
        Record a successful request.
        
        In CLOSED state: Reset failure count.
        In HALF_OPEN state: Increment success count, potentially close circuit.
        """
        async with self._lock:
            if self.state == CircuitState.CLOSED:
                self.failure_count = 0
                
            elif self.state == CircuitState.HALF_OPEN:
                self.success_count += 1
                
                if self.success_count >= self.success_threshold:
                    self._transition_to(CircuitState.CLOSED)
                    logger.info(
                        "Circuit breaker closed",
                        service=self.service_name,
                        success_count=self.success_count,
                    )
    
    async def record_failure(self) -> None:
        """
        Record a failed request.
        
        In CLOSED state: Increment failure count, potentially open circuit.
        In HALF_OPEN state: Immediately open circuit.
        """
        async with self._lock:
            self.last_failure_time = time.time()
            
            if self.state == CircuitState.CLOSED:
                self.failure_count += 1
                
                if self.failure_count >= self.failure_threshold:
                    self._transition_to(CircuitState.OPEN)
                    logger.warning(
                        "Circuit breaker opened",
                        service=self.service_name,
                        failure_count=self.failure_count,
                    )
                    
            elif self.state == CircuitState.HALF_OPEN:
                self._transition_to(CircuitState.OPEN)
                logger.warning(
                    "Circuit breaker reopened after failed recovery test",
                    service=self.service_name,
                )
    
    def _transition_to(self, new_state: CircuitState) -> None:
        """
        Transition to a new state.
        
        Args:
            new_state: The state to transition to.
        """
        old_state = self.state
        self.state = new_state
        self.last_state_change = time.time()
        
        # Reset counters on state change
        if new_state == CircuitState.CLOSED:
            self.failure_count = 0
            self.success_count = 0
        elif new_state == CircuitState.HALF_OPEN:
            self.success_count = 0
        
        logger.info(
            "Circuit breaker state changed",
            service=self.service_name,
            old_state=old_state.value,
            new_state=new_state.value,
        )
    
    async def allow_request(self) -> bool:
        """
        Check if a request should be allowed.
        
        Returns:
            bool: True if request is allowed.
        """
        async with self._lock:
            if self.state == CircuitState.CLOSED:
                return True
            
            elif self.state == CircuitState.OPEN:
                # Check if timeout has elapsed
                if time.time() - self.last_state_change >= self.timeout:
                    self._transition_to(CircuitState.HALF_OPEN)
                    return True
                return False
            
            else:  # HALF_OPEN
                # Allow limited requests to test recovery
                return True
    
    def get_state(self) -> Dict:
        """
        Get current circuit breaker state as dict.
        
        Returns:
            Dict: Current state information.
        """
        return {
            "service": self.service_name,
            "state": self.state.value,
            "failure_count": self.failure_count,
            "success_count": self.success_count,
            "last_failure": self.last_failure_time,
            "last_state_change": self.last_state_change,
            "time_in_state": time.time() - self.last_state_change,
        }


class CircuitBreakerRegistry:
    """
    Registry of circuit breakers for all services.
    
    Manages circuit breakers for multiple backend services,
    ensuring each service has its own circuit breaker.
    """
    
    def __init__(self, settings: CircuitBreakerSettings):
        """
        Initialize the registry.
        
        Args:
            settings: Circuit breaker configuration.
        """
        self.settings = settings
        self._breakers: Dict[str, CircuitBreaker] = {}
        self._lock = asyncio.Lock()
    
    async def get_breaker(self, service_name: str) -> CircuitBreaker:
        """
        Get or create a circuit breaker for a service.
        
        Args:
            service_name: Name of the service.
        
        Returns:
            CircuitBreaker: The circuit breaker for the service.
        """
        async with self._lock:
            if service_name not in self._breakers:
                self._breakers[service_name] = CircuitBreaker(
                    service_name=service_name,
                    failure_threshold=self.settings.failure_threshold,
                    success_threshold=self.settings.success_threshold,
                    timeout=self.settings.reset_timeout,
                )
            return self._breakers[service_name]
    
    def get_all_states(self) -> Dict[str, Dict]:
        """
        Get state of all circuit breakers.
        
        Returns:
            Dict: State of all circuit breakers.
        """
        return {
            name: breaker.get_state()
            for name, breaker in self._breakers.items()
        }
    
    async def reset(self, service_name: Optional[str] = None) -> None:
        """
        Reset circuit breaker(s).
        
        Args:
            service_name: Service to reset, or None to reset all.
        """
        async with self._lock:
            if service_name:
                if service_name in self._breakers:
                    breaker = self._breakers[service_name]
                    breaker._transition_to(CircuitState.CLOSED)
            else:
                for breaker in self._breakers.values():
                    breaker._transition_to(CircuitState.CLOSED)


# Global registry instance
_registry: Optional[CircuitBreakerRegistry] = None


def get_registry(settings: CircuitBreakerSettings = None) -> CircuitBreakerRegistry:
    """
    Get or create the global circuit breaker registry.
    
    Args:
        settings: Optional settings for creating new registry.
    
    Returns:
        CircuitBreakerRegistry: The global registry.
    """
    global _registry
    if _registry is None:
        if settings is None:
            from ..config import get_settings
            settings = get_settings().circuit_breaker
        _registry = CircuitBreakerRegistry(settings)
    return _registry


class CircuitBreakerMiddleware(BaseHTTPMiddleware):
    """
    Circuit breaker middleware for fault tolerance.
    
    This middleware wraps all requests and applies circuit breaker
    logic based on the target backend service.
    
    Attributes:
        settings: Circuit breaker configuration.
        registry: Circuit breaker registry.
    """
    
    def __init__(
        self,
        app: Callable,
        settings: CircuitBreakerSettings,
    ):
        """
        Initialize circuit breaker middleware.
        
        Args:
            app: The ASGI application to wrap.
            settings: Circuit breaker configuration.
        """
        super().__init__(app)
        self.settings = settings
        self.registry = get_registry(settings)
    
    def _extract_service_name(self, request: Request) -> str:
        """
        Extract the target service name from the request.
        
        Uses the first path segment to determine the service.
        
        Args:
            request: The incoming request.
        
        Returns:
            str: The service name.
        """
        path = request.url.path.strip("/")
        
        # Extract first path segment as service name
        if "/" in path:
            service = path.split("/")[0]
        else:
            service = path or "default"
        
        # Map common paths to services
        service_mapping = {
            "auth": "auth-service",
            "users": "user-service",
            "payments": "payment-service",
            "workflows": "workflow-engine",
            "queue": "distributed-queue",
            "stream": "streaming-platform",
            "cache": "cache-layer",
            "ws": "websocket-service",
            "scheduler": "scheduler-service",
            "workers": "worker-fleet",
        }
        
        return service_mapping.get(service, service)
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request with circuit breaker protection.
        
        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.
        
        Returns:
            Response: The response.
        
        Raises:
            ServiceUnavailable: If circuit is open.
        """
        # Skip circuit breaker if disabled
        if not self.settings.enabled:
            return await call_next(request)
        
        # Skip for health check endpoints
        if request.url.path in ("/health", "/ready", "/live", "/metrics"):
            return await call_next(request)
        
        # Get circuit breaker for the target service
        service_name = self._extract_service_name(request)
        breaker = await self.registry.get_breaker(service_name)
        
        # Check if request is allowed
        if not await breaker.allow_request():
            logger.warning(
                "Circuit breaker rejected request",
                service=service_name,
                state=breaker.state.value,
                request_id=getattr(request.state, "request_id", None),
            )
            raise ServiceUnavailable(
                service=service_name,
                retry_after=self.settings.reset_timeout,
            )
        
        # Store breaker in request state for potential use by handlers
        request.state.circuit_breaker = breaker
        
        try:
            # Process request
            response = await call_next(request)
            
            # Record success for non-error responses
            if response.status_code < 500:
                await breaker.record_success()
            else:
                # Server errors count as failures
                await breaker.record_failure()
            
            return response
            
        except Exception as e:
            # Record failure for any exception
            await breaker.record_failure()
            raise


async def with_circuit_breaker(
    service_name: str,
    operation: Callable,
    *args,
    **kwargs,
):
    """
    Execute an operation with circuit breaker protection.
    
    This is a utility function for wrapping arbitrary async operations
    with circuit breaker logic.
    
    Args:
        service_name: Name of the service being called.
        operation: The async operation to execute.
        *args: Positional arguments for the operation.
        **kwargs: Keyword arguments for the operation.
    
    Returns:
        The result of the operation.
    
    Raises:
        ServiceUnavailable: If circuit is open.
    
    Example:
        result = await with_circuit_breaker(
            "payment-service",
            http_client.post,
            "/payments",
            json={"amount": 100},
        )
    """
    registry = get_registry()
    breaker = await registry.get_breaker(service_name)
    
    if not await breaker.allow_request():
        raise ServiceUnavailable(
            service=service_name,
            retry_after=registry.settings.reset_timeout,
        )
    
    try:
        result = await operation(*args, **kwargs)
        await breaker.record_success()
        return result
    except Exception as e:
        await breaker.record_failure()
        raise
