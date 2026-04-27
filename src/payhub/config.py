"""Application configuration (12-factor)."""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="PAYHUB_", env_file=".env", extra="ignore")

    database_url: str = "sqlite:///./payhub.db"
    jwt_secret: str = "CHANGE_ME_IN_PRODUCTION_USE_OPENSSL_RAND"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    bootstrap_admin_key: str | None = None
    environment: str = "development"
    log_json: bool = False
    rate_limit_default: str = "60/minute"
    idempotency_ttl_hours: int = 72


@lru_cache
def get_settings() -> Settings:
    return Settings()
