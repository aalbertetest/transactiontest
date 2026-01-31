"""
Configuration Settings Module
==============================

This module provides a comprehensive configuration system for the distributed
task scheduler. It supports:
- YAML configuration files
- Environment variable overrides
- Validation of configuration values
- Default values for all settings

Configuration is loaded in this order (later overrides earlier):
1. Default values
2. YAML configuration file
3. Environment variables

Environment variables use the prefix DTS_ (Distributed Task Scheduler).
Nested settings use double underscores: DTS_DATABASE__HOST=localhost

Example config.yaml:
    database:
      host: localhost
      port: 5432
      name: taskscheduler
    
    scheduler:
      leader_election_ttl: 30
      cron_tick_interval: 1
    
    worker:
      concurrency: 10
      queues:
        - default
        - high-priority
"""

import os
from pathlib import Path
from typing import List, Optional, Any, Dict
from functools import lru_cache

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseModel):
    """
    Database connection settings.
    
    The database is the central persistence layer for the task scheduler.
    PostgreSQL 13+ is required for the SKIP LOCKED feature used in task claiming.
    
    Attributes:
        host: Database server hostname or IP address.
        port: Database server port (default 5432 for PostgreSQL).
        name: Database name to connect to.
        user: Database username for authentication.
        password: Database password (prefer environment variable).
        max_connections: Maximum number of connections in the pool.
            Should be tuned based on worker concurrency and scheduler instances.
        min_connections: Minimum connections to keep open in the pool.
        connection_timeout: Timeout in seconds for acquiring a connection.
        command_timeout: Default timeout for SQL commands.
        ssl_mode: PostgreSQL SSL mode (disable, require, verify-ca, verify-full).
    """
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, ge=1, le=65535, description="Database port")
    name: str = Field(default="taskscheduler", description="Database name")
    user: str = Field(default="postgres", description="Database user")
    password: str = Field(default="", description="Database password")
    max_connections: int = Field(default=20, ge=1, le=1000, description="Max pool connections")
    min_connections: int = Field(default=5, ge=1, le=100, description="Min pool connections")
    connection_timeout: float = Field(default=30.0, ge=1.0, description="Connection timeout seconds")
    command_timeout: float = Field(default=60.0, ge=1.0, description="Command timeout seconds")
    ssl_mode: str = Field(default="prefer", description="SSL mode")
    
    @property
    def dsn(self) -> str:
        """
        Generate a PostgreSQL connection DSN (Data Source Name).
        
        Returns:
            Connection string in format: postgresql://user:password@host:port/dbname
        """
        password_part = f":{self.password}" if self.password else ""
        return f"postgresql://{self.user}{password_part}@{self.host}:{self.port}/{self.name}"
    
    @property
    def asyncpg_dsn(self) -> str:
        """
        Generate a connection DSN suitable for asyncpg.
        
        asyncpg uses a slightly different DSN format with query parameters
        for SSL and other options.
        """
        base_dsn = self.dsn
        if self.ssl_mode != "disable":
            base_dsn += f"?ssl={self.ssl_mode}"
        return base_dsn


class SchedulerSettings(BaseModel):
    """
    Scheduler service settings.
    
    The scheduler is responsible for:
    - Leader election among scheduler instances
    - Cron job evaluation and task creation
    - Health monitoring of workers
    - Promotion of pending tasks to queued
    
    Attributes:
        leader_election_ttl: Time-to-live for leader lock in seconds.
            The leader must renew before this expires or another instance takes over.
        leader_renewal_interval: How often the leader renews its lock.
            Should be significantly less than TTL for safety margin.
        cron_tick_interval: How often to evaluate cron jobs in seconds.
            1 second provides good granularity for most use cases.
        health_check_interval: How often to check worker health in seconds.
        pending_promotion_interval: How often to check for pending tasks to promote.
        timeout_recovery_interval: How often to recover timed-out tasks.
        instance_id: Unique identifier for this scheduler instance.
            Auto-generated if not specified.
    """
    leader_election_ttl: int = Field(
        default=30, 
        ge=5, 
        le=300,
        description="Leader lock TTL in seconds"
    )
    leader_renewal_interval: int = Field(
        default=10,
        ge=1,
        le=60,
        description="Leader lock renewal interval in seconds"
    )
    cron_tick_interval: float = Field(
        default=1.0,
        ge=0.1,
        le=60.0,
        description="Cron evaluation interval in seconds"
    )
    health_check_interval: int = Field(
        default=10,
        ge=1,
        le=300,
        description="Worker health check interval in seconds"
    )
    pending_promotion_interval: float = Field(
        default=1.0,
        ge=0.1,
        le=60.0,
        description="Pending task promotion interval in seconds"
    )
    timeout_recovery_interval: int = Field(
        default=30,
        ge=5,
        le=300,
        description="Timeout recovery interval in seconds"
    )
    instance_id: Optional[str] = Field(
        default=None,
        description="Unique scheduler instance ID"
    )
    
    @field_validator('leader_renewal_interval')
    @classmethod
    def renewal_less_than_ttl(cls, v: int, info) -> int:
        """Ensure renewal interval is less than TTL for safety."""
        # Note: We can't access other fields directly in field_validator
        # This is validated in model_validator instead
        return v


class WorkerSettings(BaseModel):
    """
    Worker process settings.
    
    Workers are the execution units that process tasks. Each worker:
    - Registers itself with the system on startup
    - Polls queues for tasks to process
    - Sends heartbeats to indicate liveness
    - Executes task handlers in a thread/process pool
    
    Attributes:
        queues: List of queue names this worker processes.
            Workers only claim tasks from their configured queues.
        concurrency: Maximum number of concurrent tasks.
            Should be tuned based on task resource requirements.
        batch_size: Number of tasks to claim in each poll.
            Larger batches reduce database round-trips but increase
            rebalancing delay if worker crashes.
        heartbeat_interval: How often to send heartbeat in seconds.
        visibility_timeout: How long a task remains invisible after claiming.
            Should be longer than typical task duration.
        poll_interval: How often to poll for tasks when queue is empty.
        max_poll_interval: Maximum poll interval during backoff.
        shutdown_timeout: Time to wait for tasks to complete during shutdown.
        worker_id: Unique identifier for this worker.
            Auto-generated if not specified.
    """
    queues: List[str] = Field(
        default_factory=lambda: ["default"],
        description="Queues this worker processes"
    )
    concurrency: int = Field(
        default=10,
        ge=1,
        le=1000,
        description="Maximum concurrent tasks"
    )
    batch_size: int = Field(
        default=5,
        ge=1,
        le=100,
        description="Tasks to claim per poll"
    )
    heartbeat_interval: int = Field(
        default=10,
        ge=1,
        le=60,
        description="Heartbeat interval in seconds"
    )
    visibility_timeout: int = Field(
        default=300,
        ge=30,
        le=86400,
        description="Visibility timeout in seconds"
    )
    poll_interval: float = Field(
        default=1.0,
        ge=0.1,
        le=60.0,
        description="Poll interval in seconds"
    )
    max_poll_interval: float = Field(
        default=30.0,
        ge=1.0,
        le=300.0,
        description="Maximum poll interval during backoff"
    )
    shutdown_timeout: int = Field(
        default=60,
        ge=5,
        le=3600,
        description="Shutdown timeout in seconds"
    )
    worker_id: Optional[str] = Field(
        default=None,
        description="Unique worker ID"
    )
    
    @field_validator('queues')
    @classmethod
    def validate_queues(cls, v: List[str]) -> List[str]:
        """Ensure at least one queue is configured."""
        if not v:
            raise ValueError("At least one queue must be configured")
        return [q.strip() for q in v if q.strip()]


class RetrySettings(BaseModel):
    """
    Default retry policy settings.
    
    These settings provide defaults for task retry behavior.
    Individual tasks can override these values.
    
    Attributes:
        default_max_attempts: Maximum attempts including the first try.
        default_base_delay: Base delay for exponential backoff in seconds.
        default_max_delay: Maximum delay cap in seconds.
        exponential_base: Base for exponential calculation (typically 2).
        jitter: Whether to add randomization to prevent thundering herd.
    """
    default_max_attempts: int = Field(default=3, ge=1, le=100)
    default_base_delay: float = Field(default=1.0, ge=0.1, le=3600.0)
    default_max_delay: float = Field(default=3600.0, ge=1.0, le=86400.0)
    exponential_base: float = Field(default=2.0, ge=1.1, le=10.0)
    jitter: bool = Field(default=True)


class MetricsSettings(BaseModel):
    """
    Metrics and observability settings.
    
    The scheduler exports Prometheus-compatible metrics for monitoring.
    
    Attributes:
        enabled: Whether to enable metrics export.
        port: Port to expose metrics endpoint on.
        path: URL path for metrics endpoint.
        namespace: Metric name prefix.
    """
    enabled: bool = Field(default=True)
    port: int = Field(default=9090, ge=1, le=65535)
    path: str = Field(default="/metrics")
    namespace: str = Field(default="dts")


class LoggingSettings(BaseModel):
    """
    Logging configuration settings.
    
    Supports structured JSON logging for production and
    human-readable console logging for development.
    
    Attributes:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        format: Output format ('json' or 'console').
        output: Output destination ('stdout', 'stderr', or file path).
        include_timestamp: Whether to include timestamps in logs.
    """
    level: str = Field(default="INFO")
    format: str = Field(default="json")
    output: str = Field(default="stdout")
    include_timestamp: bool = Field(default=True)
    
    @field_validator('level')
    @classmethod
    def validate_level(cls, v: str) -> str:
        """Validate log level."""
        valid_levels = {'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'}
        v_upper = v.upper()
        if v_upper not in valid_levels:
            raise ValueError(f"Invalid log level: {v}. Must be one of {valid_levels}")
        return v_upper


class Settings(BaseSettings):
    """
    Root settings class combining all configuration sections.
    
    This class aggregates all configuration subsections and provides
    methods for loading configuration from files and environment variables.
    
    Usage:
        # Load from environment and defaults
        settings = Settings()
        
        # Load from YAML file
        settings = Settings.from_yaml('config.yaml')
        
        # Access nested settings
        db_host = settings.database.host
        worker_concurrency = settings.worker.concurrency
    """
    
    model_config = SettingsConfigDict(
        env_prefix="DTS_",
        env_nested_delimiter="__",
        case_sensitive=False,
    )
    
    # Configuration sections
    database: DatabaseSettings = Field(default_factory=DatabaseSettings)
    scheduler: SchedulerSettings = Field(default_factory=SchedulerSettings)
    worker: WorkerSettings = Field(default_factory=WorkerSettings)
    retry: RetrySettings = Field(default_factory=RetrySettings)
    metrics: MetricsSettings = Field(default_factory=MetricsSettings)
    logging: LoggingSettings = Field(default_factory=LoggingSettings)
    
    # Application-level settings
    environment: str = Field(default="development", description="Environment name")
    debug: bool = Field(default=False, description="Enable debug mode")
    
    @classmethod
    def from_yaml(cls, path: str | Path) -> "Settings":
        """
        Load settings from a YAML configuration file.
        
        Environment variables still override values from the file.
        
        Args:
            path: Path to the YAML configuration file.
            
        Returns:
            Settings instance with loaded configuration.
            
        Raises:
            FileNotFoundError: If the configuration file doesn't exist.
            yaml.YAMLError: If the file contains invalid YAML.
        """
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {path}")
        
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f) or {}
        
        # Expand environment variables in string values
        config_data = cls._expand_env_vars(config_data)
        
        return cls(**config_data)
    
    @classmethod
    def _expand_env_vars(cls, data: Any) -> Any:
        """
        Recursively expand environment variables in configuration values.
        
        Supports ${VAR_NAME} syntax for environment variable substitution.
        If the variable is not set, the original string is preserved.
        
        Args:
            data: Configuration data (dict, list, or scalar).
            
        Returns:
            Configuration data with environment variables expanded.
        """
        if isinstance(data, dict):
            return {k: cls._expand_env_vars(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [cls._expand_env_vars(item) for item in data]
        elif isinstance(data, str):
            # Expand ${VAR_NAME} patterns
            import re
            pattern = r'\$\{([^}]+)\}'
            
            def replacer(match):
                var_name = match.group(1)
                return os.environ.get(var_name, match.group(0))
            
            return re.sub(pattern, replacer, data)
        else:
            return data
    
    @model_validator(mode='after')
    def validate_settings(self) -> "Settings":
        """
        Perform cross-field validation after all fields are loaded.
        """
        # Ensure leader renewal is less than TTL
        if self.scheduler.leader_renewal_interval >= self.scheduler.leader_election_ttl:
            raise ValueError(
                f"leader_renewal_interval ({self.scheduler.leader_renewal_interval}) "
                f"must be less than leader_election_ttl ({self.scheduler.leader_election_ttl})"
            )
        
        # Ensure min_connections <= max_connections
        if self.database.min_connections > self.database.max_connections:
            raise ValueError(
                f"min_connections ({self.database.min_connections}) "
                f"must be <= max_connections ({self.database.max_connections})"
            )
        
        return self


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    This function provides a singleton-like access to settings,
    useful for dependency injection patterns.
    
    Returns:
        Cached Settings instance.
    """
    config_path = os.environ.get("DTS_CONFIG_PATH")
    if config_path and Path(config_path).exists():
        return Settings.from_yaml(config_path)
    return Settings()


# Example usage and testing
if __name__ == "__main__":
    # Demonstrate settings loading
    print("Default settings:")
    settings = Settings()
    print(f"  Database DSN: {settings.database.dsn}")
    print(f"  Worker queues: {settings.worker.queues}")
    print(f"  Worker concurrency: {settings.worker.concurrency}")
    print(f"  Scheduler leader TTL: {settings.scheduler.leader_election_ttl}s")
    
    # Create example YAML config
    example_config = """
database:
  host: ${DB_HOST:-localhost}
  port: 5432
  name: taskscheduler
  user: ${DB_USER:-postgres}
  password: ${DB_PASSWORD}
  max_connections: 20

scheduler:
  leader_election_ttl: 30
  cron_tick_interval: 1
  health_check_interval: 10

worker:
  queues:
    - default
    - high-priority
    - batch
  concurrency: 10
  batch_size: 5
  heartbeat_interval: 10

retry:
  default_max_attempts: 3
  default_base_delay: 1.0
  default_max_delay: 3600.0

metrics:
  enabled: true
  port: 9090

logging:
  level: INFO
  format: json
"""
    print("\nExample YAML configuration:")
    print(example_config)
