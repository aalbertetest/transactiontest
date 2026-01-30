"""
Data models for tasks, events, and policies.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class RetryPolicy:
    initial_interval_seconds: float = 1.0
    backoff_coefficient: float = 2.0
    max_interval_seconds: float = 60.0
    max_attempts: int = 5


@dataclass
class HistoryEvent:
    event_id: int
    run_id: str
    event_type: str
    timestamp: float
    attributes: Dict[str, Any]

    @staticmethod
    def from_row(row: Dict[str, Any]) -> "HistoryEvent":
        return HistoryEvent(
            event_id=row["id"],
            run_id=row["run_id"],
            event_type=row["event_type"],
            timestamp=row["timestamp"],
            attributes=json.loads(row["attributes"] or "{}"),
        )


@dataclass
class Task:
    task_id: str
    run_id: str
    task_type: str
    queue_name: str
    status: str
    scheduled_at: float
    leased_until: Optional[float]
    completed_at: Optional[float]
    attempt: int
    max_attempts: int
    payload: Dict[str, Any]
    last_heartbeat_at: Optional[float]
    heartbeat_timeout_seconds: Optional[int]
    timeout_at: Optional[float]
    last_error: Optional[str]

    @staticmethod
    def from_row(row: Dict[str, Any]) -> "Task":
        return Task(
            task_id=row["task_id"],
            run_id=row["run_id"],
            task_type=row["task_type"],
            queue_name=row["queue_name"],
            status=row["status"],
            scheduled_at=row["scheduled_at"],
            leased_until=row["leased_until"],
            completed_at=row["completed_at"],
            attempt=row["attempt"],
            max_attempts=row["max_attempts"],
            payload=json.loads(row["payload"] or "{}"),
            last_heartbeat_at=row["last_heartbeat_at"],
            heartbeat_timeout_seconds=row["heartbeat_timeout_seconds"],
            timeout_at=row["timeout_at"],
            last_error=row["last_error"],
        )
