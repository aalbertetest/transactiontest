"""
Workflow definition interfaces and deterministic context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, List, Optional, Protocol

from .models import HistoryEvent, RetryPolicy


@dataclass
class Command:
    command_type: str
    attributes: Dict[str, Any]


@dataclass
class ScheduleActivity(Command):
    def __init__(
        self,
        command_id: str,
        activity_id: str,
        activity_name: str,
        input: Dict[str, Any],
        timeout_seconds: int,
        heartbeat_timeout_seconds: int,
        retry_policy: RetryPolicy,
    ) -> None:
        super().__init__(
            command_type="ScheduleActivity",
            attributes={
                "command_id": command_id,
                "activity_id": activity_id,
                "activity_name": activity_name,
                "input": input,
                "timeout_seconds": timeout_seconds,
                "heartbeat_timeout_seconds": heartbeat_timeout_seconds,
                "retry_policy": retry_policy.__dict__,
            },
        )


@dataclass
class ScheduleTimer(Command):
    def __init__(self, command_id: str, timer_id: str, timeout_seconds: int) -> None:
        super().__init__(
            command_type="ScheduleTimer",
            attributes={"command_id": command_id, "timer_id": timer_id, "timeout_seconds": timeout_seconds},
        )


@dataclass
class CompleteWorkflow(Command):
    def __init__(self, result: Dict[str, Any]) -> None:
        super().__init__(
            command_type="CompleteWorkflow",
            attributes={"result": result},
        )


@dataclass
class FailWorkflow(Command):
    def __init__(self, error: str) -> None:
        super().__init__(
            command_type="FailWorkflow",
            attributes={"error": error},
        )


@dataclass
class DecisionResult:
    next_state: str
    state_data: Dict[str, Any]
    commands: List[Command] = field(default_factory=list)
    complete: bool = False
    failure: Optional[str] = None


class WorkflowDefinition(Protocol):
    name: str

    def initial_state(self) -> str:
        ...

    def decide(
        self,
        ctx: "WorkflowContext",
        state: str,
        state_data: Dict[str, Any],
        history: List[HistoryEvent],
    ) -> DecisionResult:
        ...


class WorkflowContext:
    def __init__(self, run_id: str, state_data: Dict[str, Any], history: Iterable[HistoryEvent]) -> None:
        self.run_id = run_id
        self.state_data = state_data
        self._history = list(history)
        self._sequence = int(state_data.get("sequence", 0))

    def _events(self, event_type: str) -> List[HistoryEvent]:
        return [event for event in self._history if event.event_type == event_type]

    def workflow_input(self) -> Dict[str, Any]:
        for event in self._events("WorkflowStarted"):
            return event.attributes.get("input", {})
        return {}

    def current_time(self) -> float:
        latest = None
        for event in self._history:
            if event.event_type in ("WorkflowTaskStarted", "WorkflowStarted"):
                latest = event.timestamp
        return latest if latest is not None else 0.0

    def next_sequence(self) -> int:
        self._sequence += 1
        self.state_data["sequence"] = self._sequence
        return self._sequence

    def ensure_command_id(self, prefix: str, key: str) -> str:
        stored = self.state_data.get(key)
        if stored:
            return stored
        command_id = f"{prefix}-{self.next_sequence()}"
        self.state_data[key] = command_id
        return command_id

    def activity_completed(self, activity_id: str) -> bool:
        return any(
            event.event_type == "ActivityCompleted" and event.attributes.get("activity_id") == activity_id
            for event in self._history
        )

    def activity_failed(self, activity_id: str) -> Optional[str]:
        for event in self._history:
            if event.event_type == "ActivityFailed" and event.attributes.get("activity_id") == activity_id:
                return event.attributes.get("error")
        return None

    def activity_result(self, activity_id: str) -> Optional[Dict[str, Any]]:
        for event in self._history:
            if event.event_type == "ActivityCompleted" and event.attributes.get("activity_id") == activity_id:
                return event.attributes.get("result")
        return None

    def timer_fired(self, timer_id: str) -> bool:
        return any(
            event.event_type == "TimerFired" and event.attributes.get("timer_id") == timer_id
            for event in self._history
        )

    def has_command_event(self, command_type: str, command_id: str) -> bool:
        for event in self._history:
            if event.event_type == command_type and event.attributes.get("command_id") == command_id:
                return True
        return False
