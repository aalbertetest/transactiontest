"""
Configuration loading for the workflow engine.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict


@dataclass
class EngineConfig:
    db_path: str = "engine.sqlite"
    workflow_task_queue: str = "workflow-tasks"
    activity_task_queue: str = "activity-tasks"
    timer_task_queue: str = "timer-tasks"
    worker_poll_interval_seconds: float = 0.5
    scheduler_interval_seconds: float = 1.0
    task_lease_seconds: int = 30
    activity_heartbeat_timeout_seconds: int = 60
    workflow_task_timeout_seconds: int = 30
    run_timeout_seconds: int = 3600
    max_task_attempts: int = 10
    log_level: str = "INFO"
    metrics_enabled: bool = True
    extra: Dict[str, Any] = field(default_factory=dict)


def _coerce_value(value: str) -> Any:
    lowered = value.lower()
    if lowered in ("true", "false"):
        return lowered == "true"
    try:
        if "." in value:
            return float(value)
        return int(value)
    except ValueError:
        return value


def load_config(config_path: str | None = None) -> EngineConfig:
    """
    Load configuration from a JSON file and environment variables.

    Environment variables override file values using the prefix WF_ENGINE_.
    For example: WF_ENGINE_DB_PATH, WF_ENGINE_LOG_LEVEL.
    """
    data: Dict[str, Any] = {}
    if config_path:
        with open(config_path, "r", encoding="utf-8") as handle:
            data = json.load(handle)

    env_prefix = "WF_ENGINE_"
    for key, value in os.environ.items():
        if not key.startswith(env_prefix):
            continue
        config_key = key[len(env_prefix) :].lower()
        data[config_key] = _coerce_value(value)

    config = EngineConfig()
    for field_name in config.__dataclass_fields__:
        if field_name in data:
            setattr(config, field_name, data[field_name])
    if "extra" in data and isinstance(data["extra"], dict):
        config.extra.update(data["extra"])
    return config
