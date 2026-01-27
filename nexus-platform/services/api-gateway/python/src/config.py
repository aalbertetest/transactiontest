# =============================================================================
# NEXUS PLATFORM - API GATEWAY - CONFIGURATION
# =============================================================================
# Centralized configuration management with environment variable support,
# validation, and sensible defaults for all service settings.
# =============================================================================

"""
Configuration Module

This module handles all configuration for the API Gateway service including:
- Server settings (host, port, workers)
- Authentication configuration (JWT settings, API key settings)
- Rate limiting configuration
- Circuit breaker settings
- Backend service URLs
- Database and cache connections
- Observability settings (logging, metrics, tracing)

Configuration is loaded from environment variables with fallback to defaults.
All settings are validated using Pydantic for type safety.
"""

import os
from enum import Enum
from functools import lru_cache
from typing import Any, Dict, List, Optional, Set

from pydantic import Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Environment(str, Enum):
    """Deployment environment enumeration."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"
    TESTING = "testing"


class LogLevel(str, Enum):
    """Logging level enumeration."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ServerSettings(BaseSettings):
    """
    Server configuration settings.
    
    Controls the HTTP server behavior including host, port, workers,
    and timeouts.
    """
    model_config = SettingsConfigDict(env_prefix="SERVER_")
    
    # Basic server configuration
    host: str = Field(default="0.0.0.0", description="Server bind host")
    port: int = Field(default=8080, ge=1, le=65535, description="Server bind port")
    workers: int = Field(default=4, ge=1, le=32, description="Number of worker processes")
    
    # Timeouts (in seconds)
    request_timeout: int = Field(default=30, ge=1, le=300, description="Request timeout")
    keepalive_timeout: int = Field(default=65, ge=1, le=300, description="Keep-alive timeout")
    graceful_shutdown_timeout: int = Field(default=30, ge=1, le=120, description="Graceful shutdown timeout")
    
    # Request limits
    max_request_size: int = Field(default=10 * 1024 * 1024, description="Max request body size in bytes")
    max_header_size: int = Field(default=16 * 1024, description="Max header size in bytes")
    
    # SSL/TLS
    ssl_enabled: bool = Field(default=False, description="Enable SSL/TLS")
    ssl_cert_path: Optional[str] = Field(default=None, description="Path to SSL certificate")
    ssl_key_path: Optional[str] = Field(default=None, description="Path to SSL private key")
    
    # CORS settings
    cors_enabled: bool = Field(default=True, description="Enable CORS")
    cors_origins: List[str] = Field(
        default=["*"],
        description="Allowed CORS origins"
    )
    cors_methods: List[str] = Field(
        default=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
        description="Allowed CORS methods"
    )
    cors_headers: List[str] = Field(
        default=["*"],
        description="Allowed CORS headers"
    )
    cors_credentials: bool = Field(default=True, description="Allow credentials in CORS")
    cors_max_age: int = Field(default=600, description="CORS preflight cache max age")


class AuthSettings(BaseSettings):
    """
    Authentication configuration settings.
    
    Manages JWT token configuration, API key settings, and OAuth2 providers.
    """
    model_config = SettingsConfigDict(env_prefix="AUTH_")
    
    # JWT Settings
    jwt_secret_key: str = Field(
        default="CHANGE_ME_IN_PRODUCTION_USE_STRONG_SECRET_KEY_256_BITS",
        description="Secret key for JWT signing (HS256) or path to private key (RS256)"
    )
    jwt_algorithm: str = Field(default="RS256", description="JWT signing algorithm")
    jwt_public_key_path: Optional[str] = Field(default=None, description="Path to JWT public key for RS256")
    jwt_private_key_path: Optional[str] = Field(default=None, description="Path to JWT private key for RS256")
    jwt_access_token_expire_minutes: int = Field(default=15, ge=1, le=60, description="Access token expiry")
    jwt_refresh_token_expire_days: int = Field(default=7, ge=1, le=30, description="Refresh token expiry")
    jwt_issuer: str = Field(default="nexus-platform", description="JWT issuer claim")
    jwt_audience: List[str] = Field(default=["nexus-api"], description="JWT audience claim")
    
    # API Key Settings
    api_key_header: str = Field(default="X-API-Key", description="Header name for API key")
    api_key_prefix: str = Field(default="nxp_", description="API key prefix")
    api_key_hash_algorithm: str = Field(default="sha256", description="API key hash algorithm")
    
    # OAuth2 Providers
    oauth2_enabled: bool = Field(default=True, description="Enable OAuth2 authentication")
    google_client_id: Optional[str] = Field(default=None, description="Google OAuth2 client ID")
    google_client_secret: Optional[str] = Field(default=None, description="Google OAuth2 client secret")
    github_client_id: Optional[str] = Field(default=None, description="GitHub OAuth2 client ID")
    github_client_secret: Optional[str] = Field(default=None, description="GitHub OAuth2 client secret")
    
    # Session Settings
    session_cookie_name: str = Field(default="nexus_session", description="Session cookie name")
    session_cookie_secure: bool = Field(default=True, description="Secure cookie flag")
    session_cookie_httponly: bool = Field(default=True, description="HttpOnly cookie flag")
    session_cookie_samesite: str = Field(default="lax", description="SameSite cookie attribute")


class RateLimitSettings(BaseSettings):
    """
    Rate limiting configuration settings.
    
    Controls request rate limits at various levels (global, per-user, per-endpoint).
    """
    model_config = SettingsConfigDict(env_prefix="RATE_LIMIT_")
    
    # Enable/disable rate limiting
    enabled: bool = Field(default=True, description="Enable rate limiting")
    
    # Global rate limits
    global_requests_per_minute: int = Field(default=10000, ge=1, description="Global requests per minute")
    global_requests_per_second: int = Field(default=1000, ge=1, description="Global requests per second")
    
    # Per-user rate limits
    user_requests_per_minute: int = Field(default=100, ge=1, description="Per-user requests per minute")
    user_requests_per_second: int = Field(default=20, ge=1, description="Per-user requests per second")
    
    # Per-IP rate limits
    ip_requests_per_minute: int = Field(default=60, ge=1, description="Per-IP requests per minute")
    ip_requests_per_second: int = Field(default=10, ge=1, description="Per-IP requests per second")
    
    # Per-endpoint rate limits (can be overridden per route)
    endpoint_requests_per_minute: int = Field(default=100, ge=1, description="Per-endpoint requests per minute")
    
    # Burst allowance
    burst_multiplier: float = Field(default=2.0, ge=1.0, le=10.0, description="Burst allowance multiplier")
    
    # Rate limit storage
    storage_backend: str = Field(default="redis", description="Rate limit storage backend (redis, memory)")
    
    # Response headers
    include_headers: bool = Field(default=True, description="Include rate limit headers in response")
    
    # Whitelist
    whitelisted_ips: List[str] = Field(default=[], description="IPs exempt from rate limiting")
    whitelisted_api_keys: List[str] = Field(default=[], description="API keys exempt from rate limiting")


class CircuitBreakerSettings(BaseSettings):
    """
    Circuit breaker configuration settings.
    
    Controls fault tolerance behavior for backend service calls.
    """
    model_config = SettingsConfigDict(env_prefix="CIRCUIT_BREAKER_")
    
    # Enable/disable circuit breaker
    enabled: bool = Field(default=True, description="Enable circuit breaker")
    
    # Failure thresholds
    failure_threshold: int = Field(default=5, ge=1, le=100, description="Failures before opening circuit")
    success_threshold: int = Field(default=3, ge=1, le=100, description="Successes to close circuit")
    
    # Timeouts
    timeout: int = Field(default=30, ge=1, le=120, description="Operation timeout in seconds")
    reset_timeout: int = Field(default=60, ge=1, le=300, description="Time before half-open state")
    
    # State management
    half_open_max_calls: int = Field(default=3, ge=1, le=10, description="Max calls in half-open state")
    
    # Monitoring window
    rolling_window_seconds: int = Field(default=60, ge=10, le=300, description="Rolling window for failure rate")


class RetrySettings(BaseSettings):
    """
    Retry configuration settings.
    
    Controls retry behavior for failed requests to backend services.
    """
    model_config = SettingsConfigDict(env_prefix="RETRY_")
    
    # Enable/disable retries
    enabled: bool = Field(default=True, description="Enable automatic retries")
    
    # Retry limits
    max_attempts: int = Field(default=3, ge=1, le=10, description="Maximum retry attempts")
    
    # Backoff settings
    initial_backoff_ms: int = Field(default=100, ge=10, le=10000, description="Initial backoff in milliseconds")
    max_backoff_ms: int = Field(default=10000, ge=100, le=60000, description="Maximum backoff in milliseconds")
    backoff_multiplier: float = Field(default=2.0, ge=1.0, le=5.0, description="Backoff multiplier")
    jitter: bool = Field(default=True, description="Add jitter to backoff")
    
    # Retryable conditions
    retry_on_status_codes: List[int] = Field(
        default=[408, 429, 500, 502, 503, 504],
        description="HTTP status codes to retry"
    )
    retry_on_exceptions: List[str] = Field(
        default=["ConnectionError", "TimeoutError"],
        description="Exception types to retry"
    )


class BackendServiceSettings(BaseSettings):
    """
    Backend service URLs and configuration.
    
    Defines all upstream services that the API Gateway routes to.
    """
    model_config = SettingsConfigDict(env_prefix="BACKEND_")
    
    # Service discovery
    service_discovery_enabled: bool = Field(default=True, description="Enable service discovery")
    service_discovery_type: str = Field(default="kubernetes", description="Service discovery type (kubernetes, consul, static)")
    
    # Service URLs (used when service discovery is disabled or as fallback)
    auth_service_url: str = Field(default="http://auth-service:8081", description="Auth service URL")
    user_service_url: str = Field(default="http://user-service:8082", description="User service URL")
    payment_service_url: str = Field(default="http://payment-service:8083", description="Payment service URL")
    workflow_service_url: str = Field(default="http://workflow-engine:8084", description="Workflow service URL")
    queue_service_url: str = Field(default="http://distributed-queue:8085", description="Queue service URL")
    streaming_service_url: str = Field(default="http://streaming-platform:8086", description="Streaming service URL")
    cache_service_url: str = Field(default="http://cache-layer:8087", description="Cache service URL")
    database_service_url: str = Field(default="http://database-layer:8088", description="Database service URL")
    websocket_service_url: str = Field(default="http://websocket-service:8089", description="WebSocket service URL")
    scheduler_service_url: str = Field(default="http://scheduler-service:8090", description="Scheduler service URL")
    worker_service_url: str = Field(default="http://worker-fleet:8091", description="Worker service URL")
    
    # Connection pooling
    max_connections_per_host: int = Field(default=100, ge=10, le=1000, description="Max connections per host")
    max_keepalive_connections: int = Field(default=20, ge=5, le=100, description="Max keepalive connections")
    keepalive_expiry: int = Field(default=30, ge=5, le=120, description="Keepalive expiry in seconds")
    
    # Timeouts
    connect_timeout: float = Field(default=5.0, ge=0.1, le=30.0, description="Connection timeout in seconds")
    read_timeout: float = Field(default=30.0, ge=1.0, le=120.0, description="Read timeout in seconds")
    write_timeout: float = Field(default=30.0, ge=1.0, le=120.0, description="Write timeout in seconds")


class CacheSettings(BaseSettings):
    """
    Caching configuration settings.
    
    Controls response caching behavior at the gateway level.
    """
    model_config = SettingsConfigDict(env_prefix="CACHE_")
    
    # Enable/disable caching
    enabled: bool = Field(default=True, description="Enable response caching")
    
    # Cache backend
    backend: str = Field(default="redis", description="Cache backend (redis, memory)")
    
    # Redis settings
    redis_url: str = Field(default="redis://redis:6379/0", description="Redis connection URL")
    redis_prefix: str = Field(default="nexus:gateway:cache:", description="Redis key prefix")
    redis_ssl: bool = Field(default=False, description="Enable Redis SSL")
    
    # TTL settings
    default_ttl_seconds: int = Field(default=300, ge=1, le=86400, description="Default cache TTL")
    max_ttl_seconds: int = Field(default=3600, ge=1, le=86400, description="Maximum cache TTL")
    
    # Cache key settings
    vary_headers: List[str] = Field(
        default=["Accept", "Accept-Encoding", "Authorization"],
        description="Headers to vary cache by"
    )
    
    # Cache control
    respect_cache_control: bool = Field(default=True, description="Respect Cache-Control headers")
    cache_private: bool = Field(default=False, description="Cache private responses")


class DatabaseSettings(BaseSettings):
    """
    Database configuration settings.
    
    Controls database connections for gateway-specific data (rate limits, sessions).
    """
    model_config = SettingsConfigDict(env_prefix="DATABASE_")
    
    # PostgreSQL settings
    host: str = Field(default="postgres", description="Database host")
    port: int = Field(default=5432, ge=1, le=65535, description="Database port")
    name: str = Field(default="nexus_gateway", description="Database name")
    user: str = Field(default="nexus", description="Database user")
    password: str = Field(default="nexus_password", description="Database password")
    
    # Connection pool settings
    pool_size: int = Field(default=20, ge=1, le=100, description="Connection pool size")
    max_overflow: int = Field(default=10, ge=0, le=50, description="Max pool overflow")
    pool_timeout: int = Field(default=30, ge=1, le=120, description="Pool timeout in seconds")
    pool_recycle: int = Field(default=3600, ge=60, le=86400, description="Pool recycle time in seconds")
    
    # SSL settings
    ssl_enabled: bool = Field(default=False, description="Enable database SSL")
    ssl_ca_path: Optional[str] = Field(default=None, description="Path to CA certificate")
    
    @property
    def url(self) -> str:
        """Construct database URL."""
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"


class LoggingSettings(BaseSettings):
    """
    Logging configuration settings.
    
    Controls logging behavior including format, level, and output destinations.
    """
    model_config = SettingsConfigDict(env_prefix="LOG_")
    
    # Log level
    level: LogLevel = Field(default=LogLevel.INFO, description="Log level")
    
    # Output format
    format: str = Field(default="json", description="Log format (json, text)")
    
    # Output destinations
    output: str = Field(default="stdout", description="Log output (stdout, file, both)")
    file_path: Optional[str] = Field(default="/var/log/nexus/gateway.log", description="Log file path")
    
    # Rotation settings (for file output)
    max_file_size_mb: int = Field(default=100, ge=1, le=1000, description="Max log file size in MB")
    backup_count: int = Field(default=10, ge=1, le=100, description="Number of backup files to keep")
    
    # Request logging
    log_requests: bool = Field(default=True, description="Log all requests")
    log_request_body: bool = Field(default=False, description="Log request bodies")
    log_response_body: bool = Field(default=False, description="Log response bodies")
    sensitive_headers: List[str] = Field(
        default=["Authorization", "X-API-Key", "Cookie"],
        description="Headers to redact in logs"
    )
    
    # Correlation
    correlation_id_header: str = Field(default="X-Correlation-ID", description="Correlation ID header")


class MetricsSettings(BaseSettings):
    """
    Metrics configuration settings.
    
    Controls Prometheus metrics collection and exposure.
    """
    model_config = SettingsConfigDict(env_prefix="METRICS_")
    
    # Enable/disable metrics
    enabled: bool = Field(default=True, description="Enable metrics collection")
    
    # Endpoint settings
    endpoint: str = Field(default="/metrics", description="Metrics endpoint path")
    
    # Metric prefixes
    prefix: str = Field(default="nexus_gateway", description="Metric name prefix")
    
    # Histogram buckets
    latency_buckets: List[float] = Field(
        default=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0],
        description="Latency histogram buckets in seconds"
    )
    request_size_buckets: List[float] = Field(
        default=[100, 1000, 10000, 100000, 1000000],
        description="Request size histogram buckets in bytes"
    )


class TracingSettings(BaseSettings):
    """
    Distributed tracing configuration settings.
    
    Controls OpenTelemetry/Jaeger tracing configuration.
    """
    model_config = SettingsConfigDict(env_prefix="TRACING_")
    
    # Enable/disable tracing
    enabled: bool = Field(default=True, description="Enable distributed tracing")
    
    # Service name
    service_name: str = Field(default="api-gateway", description="Service name for tracing")
    
    # Jaeger settings
    jaeger_host: str = Field(default="jaeger", description="Jaeger agent host")
    jaeger_port: int = Field(default=6831, description="Jaeger agent port")
    
    # Sampling
    sampling_rate: float = Field(default=1.0, ge=0.0, le=1.0, description="Trace sampling rate")
    
    # Propagation
    propagation_format: str = Field(default="w3c", description="Trace context propagation format")
    
    # Span settings
    record_exception: bool = Field(default=True, description="Record exceptions in spans")
    record_sql: bool = Field(default=False, description="Record SQL queries in spans")


class Settings(BaseSettings):
    """
    Main settings class that aggregates all configuration sections.
    
    This is the primary configuration interface for the API Gateway service.
    All settings are loaded from environment variables with sensible defaults.
    """
    model_config = SettingsConfigDict(
        env_prefix="NEXUS_",
        env_nested_delimiter="__",
        case_sensitive=False
    )
    
    # Environment
    environment: Environment = Field(default=Environment.DEVELOPMENT, description="Deployment environment")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    # Service identification
    service_name: str = Field(default="api-gateway", description="Service name")
    service_version: str = Field(default="1.0.0", description="Service version")
    instance_id: str = Field(
        default_factory=lambda: os.getenv("HOSTNAME", f"gateway-{os.getpid()}"),
        description="Service instance identifier"
    )
    
    # Nested settings
    server: ServerSettings = Field(default_factory=ServerSettings)
    auth: AuthSettings = Field(default_factory=AuthSettings)
    rate_limit: RateLimitSettings = Field(default_factory=RateLimitSettings)
    circuit_breaker: CircuitBreakerSettings = Field(default_factory=CircuitBreakerSettings)
    retry: RetrySettings = Field(default_factory=RetrySettings)
    backend: BackendServiceSettings = Field(default_factory=BackendServiceSettings)
    cache: CacheSettings = Field(default_factory=CacheSettings)
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    metrics: MetricsSettings = Field(default_factory=MetricsSettings)
    tracing: TracingSettings = Field(default_factory=TracingSettings)
    
    @model_validator(mode='after')
    def validate_production_settings(self) -> 'Settings':
        """Validate that production has appropriate security settings."""
        if self.environment == Environment.PRODUCTION:
            # Ensure JWT secret is changed from default
            if "CHANGE_ME" in self.auth.jwt_secret_key:
                raise ValueError("JWT secret key must be changed in production")
            
            # Ensure debug is disabled
            if self.debug:
                raise ValueError("Debug mode must be disabled in production")
            
            # Ensure CORS is properly configured
            if "*" in self.server.cors_origins:
                raise ValueError("Wildcard CORS origin not allowed in production")
        
        return self
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.environment == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment == Environment.PRODUCTION
    
    def is_testing(self) -> bool:
        """Check if running in testing environment."""
        return self.environment == Environment.TESTING


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Settings are cached for performance. To reload settings,
    clear the cache with get_settings.cache_clear().
    
    Returns:
        Settings: The application settings instance.
    """
    return Settings()


# Convenience alias for importing
settings = get_settings()
