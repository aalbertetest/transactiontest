from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


def _get_env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    return int(value)


def _get_env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    return float(value)


def _get_env_str(name: str, default: str) -> str:
    value = os.getenv(name)
    if value is None:
        return default
    return value


def _get_env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in ("1", "true", "yes", "y", "on")


@dataclass(frozen=True)
class Config:
    """
    Engine configuration with environment overrides and file loading.
    """

    db_path: str = "workflow.db"
    task_queue_name: str = "default"
    worker_id: str = "worker-1"
    poll_interval_seconds: float = 0.5
    scheduler_interval_seconds: float = 0.5
    lease_duration_seconds: int = 30

    activity_heartbeat_timeout_seconds: int = 30
    activity_schedule_to_close_timeout_seconds: int = 300
    activity_start_to_close_timeout_seconds: int = 60

    retry_initial_interval_seconds: int = 1
    retry_max_interval_seconds: int = 60
    retry_backoff_coefficient: float = 2.0
    retry_max_attempts: int = 3

    metrics_enabled: bool = True
    log_level: str = "INFO"

    @staticmethod
    def from_env() -> "Config":
        return Config(
            db_path=_get_env_str("WF_DB_PATH", "workflow.db"),
            task_queue_name=_get_env_str("WF_TASK_QUEUE", "default"),
            worker_id=_get_env_str("WF_WORKER_ID", "worker-1"),
            poll_interval_seconds=_get_env_float("WF_POLL_INTERVAL_SECONDS", 0.5),
            scheduler_interval_seconds=_get_env_float("WF_SCHEDULER_INTERVAL_SECONDS", 0.5),
            lease_duration_seconds=_get_env_int("WF_LEASE_DURATION_SECONDS", 30),
            activity_heartbeat_timeout_seconds=_get_env_int(
                "WF_ACTIVITY_HEARTBEAT_TIMEOUT_SECONDS", 30
            ),
            activity_schedule_to_close_timeout_seconds=_get_env_int(
                "WF_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT_SECONDS", 300
            ),
            activity_start_to_close_timeout_seconds=_get_env_int(
                "WF_ACTIVITY_START_TO_CLOSE_TIMEOUT_SECONDS", 60
            ),
            retry_initial_interval_seconds=_get_env_int(
                "WF_RETRY_INITIAL_INTERVAL_SECONDS", 1
            ),
            retry_max_interval_seconds=_get_env_int(
                "WF_RETRY_MAX_INTERVAL_SECONDS", 60
            ),
            retry_backoff_coefficient=_get_env_float(
                "WF_RETRY_BACKOFF_COEFFICIENT", 2.0
            ),
            retry_max_attempts=_get_env_int("WF_RETRY_MAX_ATTEMPTS", 3),
            metrics_enabled=_get_env_bool("WF_METRICS_ENABLED", True),
            log_level=_get_env_str("WF_LOG_LEVEL", "INFO"),
        )

    @staticmethod
    def from_file(path: str) -> "Config":
        with open(path, "r", encoding="utf-8") as handle:
            data = json.load(handle)
        return Config.from_dict(data)

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Config":
        base = Config.from_env()
        return Config(
            db_path=data.get("db_path", base.db_path),
            task_queue_name=data.get("task_queue_name", base.task_queue_name),
            worker_id=data.get("worker_id", base.worker_id),
            poll_interval_seconds=data.get(
                "poll_interval_seconds", base.poll_interval_seconds
            ),
            scheduler_interval_seconds=data.get(
                "scheduler_interval_seconds", base.scheduler_interval_seconds
            ),
            lease_duration_seconds=data.get(
                "lease_duration_seconds", base.lease_duration_seconds
            ),
            activity_heartbeat_timeout_seconds=data.get(
                "activity_heartbeat_timeout_seconds",
                base.activity_heartbeat_timeout_seconds,
            ),
            activity_schedule_to_close_timeout_seconds=data.get(
                "activity_schedule_to_close_timeout_seconds",
                base.activity_schedule_to_close_timeout_seconds,
            ),
            activity_start_to_close_timeout_seconds=data.get(
                "activity_start_to_close_timeout_seconds",
                base.activity_start_to_close_timeout_seconds,
            ),
            retry_initial_interval_seconds=data.get(
                "retry_initial_interval_seconds", base.retry_initial_interval_seconds
            ),
            retry_max_interval_seconds=data.get(
                "retry_max_interval_seconds", base.retry_max_interval_seconds
            ),
            retry_backoff_coefficient=data.get(
                "retry_backoff_coefficient", base.retry_backoff_coefficient
            ),
            retry_max_attempts=data.get(
                "retry_max_attempts", base.retry_max_attempts
            ),
            metrics_enabled=data.get("metrics_enabled", base.metrics_enabled),
            log_level=data.get("log_level", base.log_level),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "db_path": self.db_path,
            "task_queue_name": self.task_queue_name,
            "worker_id": self.worker_id,
            "poll_interval_seconds": self.poll_interval_seconds,
            "scheduler_interval_seconds": self.scheduler_interval_seconds,
            "lease_duration_seconds": self.lease_duration_seconds,
            "activity_heartbeat_timeout_seconds": self.activity_heartbeat_timeout_seconds,
            "activity_schedule_to_close_timeout_seconds": self.activity_schedule_to_close_timeout_seconds,
            "activity_start_to_close_timeout_seconds": self.activity_start_to_close_timeout_seconds,
            "retry_initial_interval_seconds": self.retry_initial_interval_seconds,
            "retry_max_interval_seconds": self.retry_max_interval_seconds,
            "retry_backoff_coefficient": self.retry_backoff_coefficient,
            "retry_max_attempts": self.retry_max_attempts,
            "metrics_enabled": self.metrics_enabled,
            "log_level": self.log_level,
        }

