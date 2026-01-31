from __future__ import annotations

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    database_url: str
    redis_url: str | None
    secret_key: str
    matchmaking_size: int
    max_input_rate: int
    max_speed: float
    state_ttl_seconds: int

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            database_url=os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./game.db"),
            redis_url=os.getenv("REDIS_URL"),
            secret_key=os.getenv("SECRET_KEY", "dev-secret"),
            matchmaking_size=int(os.getenv("MATCHMAKING_SIZE", "2")),
            max_input_rate=int(os.getenv("MAX_INPUT_RATE", "20")),
            max_speed=float(os.getenv("MAX_SPEED", "6.0")),
            state_ttl_seconds=int(os.getenv("STATE_TTL_SECONDS", "300")),
        )
