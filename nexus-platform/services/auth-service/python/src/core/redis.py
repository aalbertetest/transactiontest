# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - REDIS
# =============================================================================
# Redis connection and caching utilities.
# =============================================================================

from typing import Optional
import redis.asyncio as redis

from ..config import settings

# Global Redis client
_redis_client: Optional[redis.Redis] = None


async def init_redis() -> None:
    """Initialize Redis connection."""
    global _redis_client
    _redis_client = redis.from_url(
        settings.redis.url,
        encoding="utf-8",
        decode_responses=True,
    )
    # Test connection
    await _redis_client.ping()


async def close_redis() -> None:
    """Close Redis connection."""
    global _redis_client
    if _redis_client:
        await _redis_client.close()
        _redis_client = None


def get_redis() -> redis.Redis:
    """Get Redis client instance."""
    if not _redis_client:
        raise RuntimeError("Redis not initialized")
    return _redis_client


async def set_cache(
    key: str,
    value: str,
    ttl: int = 300,
) -> None:
    """Set a cache value with TTL."""
    client = get_redis()
    await client.setex(
        f"{settings.redis.prefix}{key}",
        ttl,
        value,
    )


async def get_cache(key: str) -> Optional[str]:
    """Get a cache value."""
    client = get_redis()
    return await client.get(f"{settings.redis.prefix}{key}")


async def delete_cache(key: str) -> None:
    """Delete a cache value."""
    client = get_redis()
    await client.delete(f"{settings.redis.prefix}{key}")


async def add_to_blacklist(
    token_jti: str,
    ttl: int,
) -> None:
    """Add a token to the blacklist."""
    client = get_redis()
    await client.setex(
        f"{settings.redis.prefix}blacklist:{token_jti}",
        ttl,
        "1",
    )


async def is_blacklisted(token_jti: str) -> bool:
    """Check if a token is blacklisted."""
    client = get_redis()
    result = await client.get(f"{settings.redis.prefix}blacklist:{token_jti}")
    return result is not None


async def increment_failed_attempts(
    identifier: str,
    window: int = 900,  # 15 minutes
) -> int:
    """Increment failed login attempts for rate limiting."""
    client = get_redis()
    key = f"{settings.redis.prefix}failed:{identifier}"
    
    count = await client.incr(key)
    if count == 1:
        await client.expire(key, window)
    
    return count


async def get_failed_attempts(identifier: str) -> int:
    """Get current failed login attempts."""
    client = get_redis()
    key = f"{settings.redis.prefix}failed:{identifier}"
    result = await client.get(key)
    return int(result) if result else 0


async def clear_failed_attempts(identifier: str) -> None:
    """Clear failed login attempts."""
    client = get_redis()
    await client.delete(f"{settings.redis.prefix}failed:{identifier}")
