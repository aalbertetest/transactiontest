"""
Configuration loading for the workflow engine.

The engine supports JSON configuration files plus environment overrides.
Environment variables are prefixed with WF_.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict


@dataclass(frozen=True)
class EngineConfig:
    # Persistence
    db_path: str = "workflow.db"
    # Queues
    workflow_queue: str = "workflow"
    activity_queue: str = "activity"
    # Scheduler/worker behavior
    worker_poll_interval_seconds: float = 0.2
    scheduler_poll_interval_seconds: float = 0.5
    lease_seconds: int = 30
    # Retry and backoff
    activity_max_attempts: int = 5
    workflow_max_attempts: int = 3
    backoff_initial_seconds: float = 1.0
    backoff_max_seconds: float = 30.0
    backoff_jitter: float = 0.2
    # Timeouts
    workflow_task_timeout_seconds: int = 60
    activity_task_timeout_seconds: int = 300
    # Logging
    log_level: str = "INFO"
    # Metrics
    metrics_enabled: bool = True


def _apply_env_overrides(data: Dict[str, Any]) -> Dict[str, Any]:
    # Environment override format: WF_<FIELD_NAME_IN_UPPERCASE>
    # Example: WF_DB_PATH=/tmp/workflow.db
    for field in EngineConfig.__dataclass_fields__.values():
        env_key = f"WF_{field.name.upper()}"
        if env_key in os.environ:
            raw_value = os.environ[env_key]
            # Best-effort type parsing for known field types.
            if field.type is bool:
                data[field.name] = raw_value.lower() in ("1", "true", "yes", "on")
            elif field.type is int:
                data[field.name] = int(raw_value)
            elif field.type is float:
                data[field.name] = float(raw_value)
            else:
                data[field.name] = raw_value
    return data


def load_config(path: str | None = None) -> EngineConfig:
    """
    Load configuration from JSON file and environment overrides.

    If path is None, the configuration is built from defaults and environment only.
    """
    data: Dict[str, Any] = {}
    if path:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    data = _apply_env_overrides(data)
    return EngineConfig(**data)
