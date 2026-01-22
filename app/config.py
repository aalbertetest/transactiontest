from __future__ import annotations

import os
import uuid
from dataclasses import dataclass


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    database_url: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"
    access_token_ttl_seconds: int = 3600
    instance_id: str = "local"
    delivery_poll_interval: float = 0.2
    presence_broadcast_interval: float = 1.0
    delivery_batch_size: int = 25
    max_retries: int = 5
    base_retry_seconds: float = 0.5
    max_retry_seconds: float = 10.0
    lease_seconds: float = 15.0
    offline_retry_seconds: float = 5.0
    enable_background_workers: bool = True
    enable_presence_broadcast: bool = True


def get_settings() -> Settings:
    database_url = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./chat.db")
    jwt_secret = os.getenv("JWT_SECRET", "dev-secret")
    instance_id = (
        os.getenv("INSTANCE_ID")
        or os.getenv("POD_NAME")
        or f"local-{uuid.uuid4().hex}"
    )
    return Settings(
        database_url=database_url,
        jwt_secret=jwt_secret,
        jwt_algorithm=os.getenv("JWT_ALGORITHM", "HS256"),
        access_token_ttl_seconds=int(os.getenv("ACCESS_TOKEN_TTL", "3600")),
        instance_id=instance_id,
        delivery_poll_interval=float(os.getenv("DELIVERY_POLL_INTERVAL", "0.2")),
        presence_broadcast_interval=float(
            os.getenv("PRESENCE_BROADCAST_INTERVAL", "1.0")
        ),
        delivery_batch_size=int(os.getenv("DELIVERY_BATCH_SIZE", "25")),
        max_retries=int(os.getenv("MAX_RETRIES", "5")),
        base_retry_seconds=float(os.getenv("BASE_RETRY_SECONDS", "0.5")),
        max_retry_seconds=float(os.getenv("MAX_RETRY_SECONDS", "10.0")),
        lease_seconds=float(os.getenv("LEASE_SECONDS", "15.0")),
        offline_retry_seconds=float(os.getenv("OFFLINE_RETRY_SECONDS", "5.0")),
        enable_background_workers=_env_bool("ENABLE_BACKGROUND_WORKERS", True),
        enable_presence_broadcast=_env_bool("ENABLE_PRESENCE_BROADCAST", True),
    )
