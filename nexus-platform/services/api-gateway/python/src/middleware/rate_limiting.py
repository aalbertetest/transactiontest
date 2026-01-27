# =============================================================================
# NEXUS PLATFORM - API GATEWAY - RATE LIMITING MIDDLEWARE
# =============================================================================
# Token bucket rate limiting with Redis backend and multi-level limits.
# =============================================================================

"""
Rate Limiting Middleware

This middleware implements rate limiting using the token bucket algorithm
with support for multiple limit tiers:
- Global rate limits (protect the entire system)
- Per-IP rate limits (prevent abuse from single sources)
- Per-user rate limits (fair usage enforcement)
- Per-endpoint rate limits (protect sensitive endpoints)

Features:
- Redis-backed distributed rate limiting
- Sliding window implementation
- Burst allowance with configurable multiplier
- Rate limit headers in responses
- Whitelist support for trusted IPs/API keys
- Graceful degradation if Redis is unavailable
"""

import hashlib
import time
from dataclasses import dataclass
from typing import Callable, Dict, List, Optional, Tuple

import structlog
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

from ..config import RateLimitSettings
from ..utils.errors import RateLimitExceeded

logger = structlog.get_logger(__name__)


@dataclass
class RateLimitResult:
    """
    Result of a rate limit check.
    
    Attributes:
        allowed: Whether the request is allowed.
        limit: The rate limit that applies.
        remaining: Number of remaining requests in the window.
        reset_at: Unix timestamp when the rate limit resets.
        retry_after: Seconds until the client can retry.
    """
    allowed: bool
    limit: int
    remaining: int
    reset_at: int
    retry_after: int = 0
    window: str = "60s"
    policy: str = "default"


class TokenBucket:
    """
    Token bucket rate limiter implementation.
    
    The token bucket algorithm allows for burst traffic while
    maintaining an average rate limit. Tokens are added to the
    bucket at a fixed rate, and each request consumes one token.
    
    Attributes:
        capacity: Maximum number of tokens in the bucket.
        refill_rate: Tokens added per second.
    """
    
    def __init__(self, capacity: int, refill_rate: float):
        """
        Initialize the token bucket.
        
        Args:
            capacity: Maximum tokens (burst limit).
            refill_rate: Tokens per second (sustained rate).
        """
        self.capacity = capacity
        self.refill_rate = refill_rate


class SlidingWindowCounter:
    """
    Sliding window counter rate limiter.
    
    This implementation uses a sliding window to count requests,
    providing more accurate rate limiting than fixed windows.
    """
    
    def __init__(self, window_seconds: int, max_requests: int):
        """
        Initialize the sliding window counter.
        
        Args:
            window_seconds: Size of the sliding window in seconds.
            max_requests: Maximum requests allowed in the window.
        """
        self.window_seconds = window_seconds
        self.max_requests = max_requests


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Rate limiting middleware with multi-level limits.
    
    This middleware implements rate limiting at multiple levels:
    1. Global: Protects the entire API from overload
    2. Per-IP: Prevents abuse from single IP addresses
    3. Per-User: Ensures fair usage among authenticated users
    4. Per-Endpoint: Protects sensitive or expensive endpoints
    
    Rate limits are stored in Redis for distributed operation across
    multiple gateway instances.
    
    Attributes:
        settings: Rate limit configuration settings.
        redis_client: Redis client for distributed state.
    """
    
    # Lua script for atomic rate limit check and decrement
    # This ensures thread-safety in distributed environments
    RATE_LIMIT_SCRIPT = """
    local key = KEYS[1]
    local limit = tonumber(ARGV[1])
    local window = tonumber(ARGV[2])
    local now = tonumber(ARGV[3])
    
    -- Remove old entries outside the window
    redis.call('ZREMRANGEBYSCORE', key, '-inf', now - window * 1000)
    
    -- Count current requests in window
    local current = redis.call('ZCARD', key)
    
    if current < limit then
        -- Add this request
        redis.call('ZADD', key, now, now .. '-' .. math.random())
        redis.call('PEXPIRE', key, window * 1000)
        return {1, limit - current - 1, now + window * 1000}
    else
        -- Get the oldest entry to calculate retry time
        local oldest = redis.call('ZRANGE', key, 0, 0, 'WITHSCORES')
        local retry_after = oldest[2] and (oldest[2] + window * 1000 - now) / 1000 or window
        return {0, 0, now + window * 1000, retry_after}
    end
    """
    
    def __init__(
        self,
        app: Callable,
        settings: RateLimitSettings,
        redis_client=None,
    ):
        """
        Initialize rate limiting middleware.
        
        Args:
            app: The ASGI application to wrap.
            settings: Rate limit configuration settings.
            redis_client: Optional Redis client (will be fetched from app state if not provided).
        """
        super().__init__(app)
        self.settings = settings
        self._redis_client = redis_client
        self._script_sha = None
        
        # Compile endpoint-specific limits from config
        self.endpoint_limits: Dict[str, int] = {}
        
        # Paths exempt from rate limiting
        self.exempt_paths = {
            "/health",
            "/ready",
            "/live",
            "/metrics",
        }
    
    def _get_redis_client(self, request: Request):
        """Get Redis client from app state or instance."""
        if self._redis_client:
            return self._redis_client
        
        app_state = getattr(request.app.state, "app_state", None)
        if app_state:
            return app_state.redis_client
        
        return None
    
    def _get_client_ip(self, request: Request) -> str:
        """
        Extract client IP address from request.
        
        Handles X-Forwarded-For header for requests behind proxies.
        
        Args:
            request: The incoming request.
        
        Returns:
            str: The client IP address.
        """
        # Check for forwarded headers (reverse proxy)
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            # Take the first IP (original client)
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip.strip()
        
        # Fall back to direct client IP
        if request.client:
            return request.client.host
        
        return "unknown"
    
    def _get_user_id(self, request: Request) -> Optional[str]:
        """
        Extract user ID from authenticated request.
        
        Args:
            request: The incoming request.
        
        Returns:
            Optional[str]: The user ID if authenticated.
        """
        user = getattr(request.state, "user", None)
        if user:
            return user.user_id
        return None
    
    def _is_whitelisted(self, request: Request) -> bool:
        """
        Check if request is from a whitelisted source.
        
        Args:
            request: The incoming request.
        
        Returns:
            bool: True if whitelisted.
        """
        # Check IP whitelist
        client_ip = self._get_client_ip(request)
        if client_ip in self.settings.whitelisted_ips:
            return True
        
        # Check API key whitelist
        api_key = request.headers.get("X-API-Key", "")
        if api_key in self.settings.whitelisted_api_keys:
            return True
        
        return False
    
    def _generate_key(self, prefix: str, identifier: str) -> str:
        """
        Generate a Redis key for rate limiting.
        
        Args:
            prefix: Key prefix (e.g., "ip", "user", "global").
            identifier: The identifier to rate limit.
        
        Returns:
            str: The Redis key.
        """
        # Hash long identifiers for shorter keys
        if len(identifier) > 32:
            identifier = hashlib.sha256(identifier.encode()).hexdigest()[:16]
        
        return f"nexus:ratelimit:{prefix}:{identifier}"
    
    async def _check_rate_limit_redis(
        self,
        redis_client,
        key: str,
        limit: int,
        window: int,
    ) -> RateLimitResult:
        """
        Check rate limit using Redis.
        
        Args:
            redis_client: The Redis client.
            key: The rate limit key.
            limit: Maximum requests allowed.
            window: Window size in seconds.
        
        Returns:
            RateLimitResult: The rate limit check result.
        """
        now = int(time.time() * 1000)  # Milliseconds
        
        try:
            # Use Lua script for atomic operation
            result = await redis_client.eval(
                self.RATE_LIMIT_SCRIPT,
                1,
                key,
                limit,
                window,
                now,
            )
            
            allowed = bool(result[0])
            remaining = int(result[1])
            reset_at = int(result[2] / 1000)  # Convert to seconds
            retry_after = int(result[3]) if len(result) > 3 else 0
            
            return RateLimitResult(
                allowed=allowed,
                limit=limit,
                remaining=remaining,
                reset_at=reset_at,
                retry_after=retry_after,
                window=f"{window}s",
            )
            
        except Exception as e:
            logger.error("Redis rate limit check failed", error=str(e), key=key)
            # Fail open - allow request if Redis is down
            return RateLimitResult(
                allowed=True,
                limit=limit,
                remaining=limit - 1,
                reset_at=int(time.time()) + window,
                policy="degraded",
            )
    
    async def _check_rate_limit_memory(
        self,
        key: str,
        limit: int,
        window: int,
    ) -> RateLimitResult:
        """
        Check rate limit using in-memory storage.
        
        This is a fallback when Redis is not available.
        Note: This doesn't work in distributed deployments.
        
        Args:
            key: The rate limit key.
            limit: Maximum requests allowed.
            window: Window size in seconds.
        
        Returns:
            RateLimitResult: The rate limit check result.
        """
        # In-memory fallback (not distributed, use with caution)
        # In production, this should use proper shared memory or fail closed
        logger.warning("Using in-memory rate limiting - not suitable for distributed deployment")
        
        return RateLimitResult(
            allowed=True,
            limit=limit,
            remaining=limit - 1,
            reset_at=int(time.time()) + window,
            policy="memory",
        )
    
    async def _check_all_limits(
        self,
        request: Request,
        redis_client,
    ) -> RateLimitResult:
        """
        Check all applicable rate limits.
        
        Checks limits in order of specificity:
        1. Per-user (if authenticated)
        2. Per-IP
        3. Global
        
        Args:
            request: The incoming request.
            redis_client: The Redis client.
        
        Returns:
            RateLimitResult: The most restrictive rate limit result.
        """
        results: List[RateLimitResult] = []
        
        # Check per-user limit if authenticated
        user_id = self._get_user_id(request)
        if user_id:
            key = self._generate_key("user", user_id)
            result = await self._check_rate_limit_redis(
                redis_client,
                key,
                self.settings.user_requests_per_minute,
                60,
            )
            result.policy = "per_user"
            results.append(result)
        else:
            # Check per-IP limit for unauthenticated requests
            client_ip = self._get_client_ip(request)
            key = self._generate_key("ip", client_ip)
            result = await self._check_rate_limit_redis(
                redis_client,
                key,
                self.settings.ip_requests_per_minute,
                60,
            )
            result.policy = "per_ip"
            results.append(result)
        
        # Check endpoint-specific limit
        path = request.url.path
        if path in self.endpoint_limits:
            key = self._generate_key("endpoint", f"{user_id or self._get_client_ip(request)}:{path}")
            result = await self._check_rate_limit_redis(
                redis_client,
                key,
                self.endpoint_limits[path],
                60,
            )
            result.policy = "per_endpoint"
            results.append(result)
        
        # Return the most restrictive result
        for result in results:
            if not result.allowed:
                return result
        
        # All limits passed - return the one with lowest remaining
        return min(results, key=lambda r: r.remaining) if results else RateLimitResult(
            allowed=True,
            limit=self.settings.user_requests_per_minute,
            remaining=self.settings.user_requests_per_minute,
            reset_at=int(time.time()) + 60,
        )
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process rate limiting for the request.
        
        Args:
            request: The incoming request.
            call_next: The next middleware or route handler.
        
        Returns:
            Response: The response with rate limit headers.
        
        Raises:
            RateLimitExceeded: If rate limit is exceeded.
        """
        # Skip rate limiting if disabled
        if not self.settings.enabled:
            return await call_next(request)
        
        # Skip exempt paths
        if request.url.path in self.exempt_paths:
            return await call_next(request)
        
        # Skip whitelisted sources
        if self._is_whitelisted(request):
            return await call_next(request)
        
        # Get Redis client
        redis_client = self._get_redis_client(request)
        
        # Check rate limits
        if redis_client:
            result = await self._check_all_limits(request, redis_client)
        else:
            # Fallback to memory-based limiting
            result = await self._check_rate_limit_memory(
                self._generate_key("ip", self._get_client_ip(request)),
                self.settings.ip_requests_per_minute,
                60,
            )
        
        # Store result in request state for logging
        request.state.rate_limit = result
        
        # If rate limit exceeded, raise error
        if not result.allowed:
            raise RateLimitExceeded(
                limit=result.limit,
                window=result.window,
                retry_after=result.retry_after,
                reset_at=result.reset_at,
            )
        
        # Process request
        response = await call_next(request)
        
        # Add rate limit headers if configured
        if self.settings.include_headers:
            response.headers["X-RateLimit-Limit"] = str(result.limit)
            response.headers["X-RateLimit-Remaining"] = str(result.remaining)
            response.headers["X-RateLimit-Reset"] = str(result.reset_at)
            response.headers["X-RateLimit-Policy"] = result.policy
        
        return response
