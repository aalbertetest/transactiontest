from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Dict, Optional

# Event types used by the workflow engine.
# These strings are persisted in history and must remain stable.
EVENT_WORKFLOW_EXECUTION_STARTED = "WorkflowExecutionStarted"
EVENT_WORKFLOW_EXECUTION_COMPLETED = "WorkflowExecutionCompleted"
EVENT_WORKFLOW_EXECUTION_FAILED = "WorkflowExecutionFailed"
EVENT_WORKFLOW_EXECUTION_SIGNALED = "WorkflowExecutionSignaled"
EVENT_WORKFLOW_TASK_SCHEDULED = "WorkflowTaskScheduled"
EVENT_WORKFLOW_TASK_STARTED = "WorkflowTaskStarted"
EVENT_WORKFLOW_TASK_COMPLETED = "WorkflowTaskCompleted"
EVENT_ACTIVITY_TASK_SCHEDULED = "ActivityTaskScheduled"
EVENT_ACTIVITY_TASK_STARTED = "ActivityTaskStarted"
EVENT_ACTIVITY_TASK_COMPLETED = "ActivityTaskCompleted"
EVENT_ACTIVITY_TASK_FAILED = "ActivityTaskFailed"
EVENT_ACTIVITY_TASK_TIMED_OUT = "ActivityTaskTimedOut"
EVENT_ACTIVITY_TASK_RETRY_SCHEDULED = "ActivityTaskRetryScheduled"
EVENT_TIMER_SCHEDULED = "TimerScheduled"
EVENT_TIMER_FIRED = "TimerFired"
EVENT_SIGNAL_RECEIVED = "SignalReceived"
EVENT_VERSION_MARKER_RECORDED = "VersionMarkerRecorded"

# Workflow execution states.
WORKFLOW_STATE_RUNNING = "RUNNING"
WORKFLOW_STATE_WAITING = "WAITING"
WORKFLOW_STATE_COMPLETED = "COMPLETED"
WORKFLOW_STATE_FAILED = "FAILED"
WORKFLOW_STATE_TERMINATED = "TERMINATED"

# Activity states.
ACTIVITY_STATE_SCHEDULED = "SCHEDULED"
ACTIVITY_STATE_STARTED = "STARTED"
ACTIVITY_STATE_COMPLETED = "COMPLETED"
ACTIVITY_STATE_FAILED = "FAILED"
ACTIVITY_STATE_TIMED_OUT = "TIMED_OUT"
ACTIVITY_STATE_RETRYING = "RETRYING"

# Timer states.
TIMER_STATE_SCHEDULED = "SCHEDULED"
TIMER_STATE_FIRED = "FIRED"


@dataclass(frozen=True)
class RetryPolicy:
    """
    Retry policy for activities. These values are serialized into JSON so they
    can be persisted and reloaded across worker restarts.
    """

    initial_interval_seconds: int
    max_interval_seconds: int
    backoff_coefficient: float
    max_attempts: int

    def to_dict(self) -> Dict[str, Any]:
        return {
            "initial_interval_seconds": self.initial_interval_seconds,
            "max_interval_seconds": self.max_interval_seconds,
            "backoff_coefficient": self.backoff_coefficient,
            "max_attempts": self.max_attempts,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "RetryPolicy":
        return RetryPolicy(
            initial_interval_seconds=int(data["initial_interval_seconds"]),
            max_interval_seconds=int(data["max_interval_seconds"]),
            backoff_coefficient=float(data["backoff_coefficient"]),
            max_attempts=int(data["max_attempts"]),
        )


@dataclass(frozen=True)
class HistoryEvent:
    """
    A single event in the workflow execution history.
    """

    event_id: int
    event_type: str
    event_time: int
    attributes: Dict[str, Any]

    def attributes_json(self) -> str:
        return json.dumps(self.attributes, sort_keys=True)


@dataclass(frozen=True)
class QueueTask:
    """
    A task fetched from a task queue.
    """

    id: int
    queue_name: str
    task_type: str
    payload: Dict[str, Any]
    visible_at: int
    lease_owner: Optional[str]
    lease_expires_at: Optional[int]
    attempts: int
    max_attempts: int


@dataclass(frozen=True)
class ActivityTask:
    """
    An activity task is a durable record of an activity execution.
    """

    activity_id: str
    workflow_id: str
    run_id: str
    activity_name: str
    input: Dict[str, Any]
    state: str
    scheduled_at: int
    started_at: Optional[int]
    completed_at: Optional[int]
    heartbeat_at: Optional[int]
    heartbeat_details: Optional[Dict[str, Any]]
    attempt: int
    max_attempts: int
    retry_policy: RetryPolicy
    schedule_to_close_timeout_seconds: int
    start_to_close_timeout_seconds: int
    heartbeat_timeout_seconds: int
    last_failure: Optional[str]

