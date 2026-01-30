"""
Type definitions for workflow engine data structures.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass
from typing import Any, Dict, Optional


class WorkflowState(str, enum.Enum):
    CREATED = "CREATED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    TIMED_OUT = "TIMED_OUT"
    CANCELED = "CANCELED"
    TERMINATED = "TERMINATED"


class TaskType(str, enum.Enum):
    WORKFLOW_TASK = "WORKFLOW_TASK"
    ACTIVITY_TASK = "ACTIVITY_TASK"
    TIMER_TASK = "TIMER_TASK"


class TaskState(str, enum.Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"


@dataclass
class Event:
    workflow_id: str
    run_id: str
    event_id: int
    event_type: str
    timestamp: float
    attributes: Dict[str, Any]


@dataclass
class Task:
    task_id: str
    queue: str
    task_type: TaskType
    workflow_id: str
    run_id: str
    payload: Dict[str, Any]
    state: TaskState
    attempts: int
    max_attempts: int
    not_before: float
    created_at: float
    updated_at: float
    lease_expires_at: Optional[float]
    worker_id: Optional[str]
    timeout_seconds: Optional[int]


@dataclass
class WorkflowExecution:
    workflow_id: str
    run_id: str
    state: WorkflowState
    workflow_type: str
    input: Dict[str, Any]
    started_at: float
    completed_at: Optional[float]
    last_event_id: int
    version: int
