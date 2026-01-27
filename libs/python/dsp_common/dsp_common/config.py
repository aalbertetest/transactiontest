from __future__ import annotations

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseModel):
    env: str
    service_name: str
    log_level: str
    http_addr: str
    metrics_addr: str


class _EnvSettings(BaseSettings):
    """
    Environment-driven settings (shared across DSP services).
    Keep variable names stable across languages.
    """

    model_config = SettingsConfigDict(env_prefix="DSP_", extra="ignore")

    ENV: str = Field(default="dev")
    SERVICE_NAME: str
    LOG_LEVEL: str = Field(default="info")
    HTTP_ADDR: str = Field(default="0.0.0.0:8080")
    METRICS_ADDR: str = Field(default="0.0.0.0:9091")


def load_base_config() -> BaseConfig:
    s = _EnvSettings()  # reads environment variables
    env = s.ENV.strip()
    if env not in ("dev", "staging", "prod"):
        raise ValueError(f"Invalid DSP_ENV: {env!r}")

    log_level = s.LOG_LEVEL.strip()
    if log_level not in ("debug", "info", "warn", "error"):
        raise ValueError(f"Invalid DSP_LOG_LEVEL: {log_level!r}")

    service_name = s.SERVICE_NAME.strip()
    if not service_name:
        raise ValueError("DSP_SERVICE_NAME is required")

    return BaseConfig(
        env=env,
        service_name=service_name,
        log_level=log_level,
        http_addr=s.HTTP_ADDR.strip(),
        metrics_addr=s.METRICS_ADDR.strip(),
    )

