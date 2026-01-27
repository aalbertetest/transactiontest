# =============================================================================
# NEXUS PLATFORM - AUTHENTICATION SERVICE - CONFIGURATION
# =============================================================================
# Centralized configuration with environment variable support.
# =============================================================================

from typing import List, Optional
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerConfig(BaseSettings):
    """Server configuration."""
    model_config = SettingsConfigDict(env_prefix="SERVER_")
    
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8081)
    cors_origins: List[str] = Field(default=["*"])


class DatabaseConfig(BaseSettings):
    """Database configuration."""
    model_config = SettingsConfigDict(env_prefix="DATABASE_")
    
    host: str = Field(default="postgres")
    port: int = Field(default=5432)
    name: str = Field(default="nexus_auth")
    user: str = Field(default="nexus")
    password: str = Field(default="nexus_password")
    pool_size: int = Field(default=20)
    
    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class RedisConfig(BaseSettings):
    """Redis configuration."""
    model_config = SettingsConfigDict(env_prefix="REDIS_")
    
    url: str = Field(default="redis://redis:6379/0")
    prefix: str = Field(default="nexus:auth:")


class JWTConfig(BaseSettings):
    """JWT configuration."""
    model_config = SettingsConfigDict(env_prefix="JWT_")
    
    secret_key: str = Field(default="CHANGE_ME_IN_PRODUCTION_USE_256_BIT_KEY")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=15)
    refresh_token_expire_days: int = Field(default=7)
    issuer: str = Field(default="nexus-platform")
    audience: str = Field(default="nexus-api")


class MFAConfig(BaseSettings):
    """MFA configuration."""
    model_config = SettingsConfigDict(env_prefix="MFA_")
    
    totp_issuer: str = Field(default="Nexus Platform")
    totp_digits: int = Field(default=6)
    totp_interval: int = Field(default=30)
    backup_codes_count: int = Field(default=10)
    sms_provider: str = Field(default="twilio")


class OAuthConfig(BaseSettings):
    """OAuth2 provider configuration."""
    model_config = SettingsConfigDict(env_prefix="OAUTH_")
    
    google_client_id: Optional[str] = Field(default=None)
    google_client_secret: Optional[str] = Field(default=None)
    github_client_id: Optional[str] = Field(default=None)
    github_client_secret: Optional[str] = Field(default=None)
    redirect_url: str = Field(default="http://localhost:8080/auth/callback")


class PasswordConfig(BaseSettings):
    """Password policy configuration."""
    model_config = SettingsConfigDict(env_prefix="PASSWORD_")
    
    min_length: int = Field(default=12)
    require_uppercase: bool = Field(default=True)
    require_lowercase: bool = Field(default=True)
    require_numbers: bool = Field(default=True)
    require_special: bool = Field(default=True)
    hash_algorithm: str = Field(default="argon2")


class LoggingConfig(BaseSettings):
    """Logging configuration."""
    model_config = SettingsConfigDict(env_prefix="LOG_")
    
    level: str = Field(default="INFO")
    format: str = Field(default="json")


class Settings(BaseSettings):
    """Main settings class."""
    model_config = SettingsConfigDict(env_prefix="NEXUS_")
    
    environment: str = Field(default="development")
    debug: bool = Field(default=False)
    service_name: str = Field(default="auth-service")
    service_version: str = Field(default="1.0.0")
    
    server: ServerConfig = Field(default_factory=ServerConfig)
    database: DatabaseConfig = Field(default_factory=DatabaseConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    jwt: JWTConfig = Field(default_factory=JWTConfig)
    mfa: MFAConfig = Field(default_factory=MFAConfig)
    oauth: OAuthConfig = Field(default_factory=OAuthConfig)
    password: PasswordConfig = Field(default_factory=PasswordConfig)
    logging: LoggingConfig = Field(default_factory=LoggingConfig)
    
    def is_development(self) -> bool:
        return self.environment == "development"
    
    def is_production(self) -> bool:
        return self.environment == "production"


settings = Settings()
