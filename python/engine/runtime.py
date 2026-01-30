from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from .models import (
    EVENT_ACTIVITY_TASK_COMPLETED,
    EVENT_ACTIVITY_TASK_FAILED,
    EVENT_ACTIVITY_TASK_SCHEDULED,
    EVENT_ACTIVITY_TASK_TIMED_OUT,
    EVENT_SIGNAL_RECEIVED,
    EVENT_TIMER_FIRED,
    EVENT_TIMER_SCHEDULED,
    EVENT_VERSION_MARKER_RECORDED,
    HistoryEvent,
    RetryPolicy,
)


class WorkflowError(Exception):
    pass


class ActivityFailedError(WorkflowError):
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(message)
        self.details = details or {}


class NonDeterministicError(WorkflowError):
    pass


@dataclass(frozen=True)
class ActivityCall:
    name: str
    input: Dict[str, Any]
    retry_policy: RetryPolicy
    schedule_to_close_timeout_seconds: int
    start_to_close_timeout_seconds: int
    heartbeat_timeout_seconds: int


@dataclass(frozen=True)
class SleepCall:
    duration_seconds: int


@dataclass(frozen=True)
class WaitSignal:
    signal_name: str


@dataclass(frozen=True)
class VersionMarker:
    change_id: str
    min_supported: int
    max_supported: int


@dataclass
class Command:
    command_type: str
    attributes: Dict[str, Any]


@dataclass
class WorkflowRunResult:
    status: str
    result: Optional[Any] = None
    error: Optional[str] = None
    command: Optional[Command] = None


class WorkflowContext:
    """
    Helper for workflow authoring. All methods return an Operation that must be yielded
    from the workflow generator.
    """

    def __init__(self, default_retry_policy: RetryPolicy) -> None:
        self._default_retry_policy = default_retry_policy

    def execute_activity(
        self,
        name: str,
        input_payload: Dict[str, Any],
        retry_policy: Optional[RetryPolicy] = None,
        schedule_to_close_timeout_seconds: int = 300,
        start_to_close_timeout_seconds: int = 60,
        heartbeat_timeout_seconds: int = 30,
    ) -> ActivityCall:
        return ActivityCall(
            name=name,
            input=input_payload,
            retry_policy=retry_policy or self._default_retry_policy,
            schedule_to_close_timeout_seconds=schedule_to_close_timeout_seconds,
            start_to_close_timeout_seconds=start_to_close_timeout_seconds,
            heartbeat_timeout_seconds=heartbeat_timeout_seconds,
        )

    def sleep(self, duration_seconds: int) -> SleepCall:
        return SleepCall(duration_seconds=duration_seconds)

    def wait_signal(self, signal_name: str) -> WaitSignal:
        return WaitSignal(signal_name=signal_name)

    def get_version(self, change_id: str, min_supported: int, max_supported: int) -> VersionMarker:
        return VersionMarker(
            change_id=change_id,
            min_supported=min_supported,
            max_supported=max_supported,
        )


class HistoryView:
    """
    Pre-processed view of the history to drive deterministic replay.
    """

    def __init__(self, history: List[HistoryEvent]) -> None:
        self.activity_scheduled: List[HistoryEvent] = []
        self.activity_results: Dict[str, HistoryEvent] = {}
        self.timer_scheduled: List[HistoryEvent] = []
        self.timer_results: Dict[str, HistoryEvent] = {}
        self.signals: Dict[str, List[Dict[str, Any]]] = {}
        self.version_markers: Dict[str, int] = {}

        for event in history:
            if event.event_type == EVENT_ACTIVITY_TASK_SCHEDULED:
                self.activity_scheduled.append(event)
            elif event.event_type in (
                EVENT_ACTIVITY_TASK_COMPLETED,
                EVENT_ACTIVITY_TASK_FAILED,
                EVENT_ACTIVITY_TASK_TIMED_OUT,
            ):
                activity_id = event.attributes.get("activity_id")
                if activity_id:
                    self.activity_results[activity_id] = event
            elif event.event_type == EVENT_TIMER_SCHEDULED:
                self.timer_scheduled.append(event)
            elif event.event_type == EVENT_TIMER_FIRED:
                timer_id = event.attributes.get("timer_id")
                if timer_id:
                    self.timer_results[timer_id] = event
            elif event.event_type == EVENT_SIGNAL_RECEIVED:
                name = event.attributes.get("signal_name")
                payload = event.attributes.get("payload", {})
                if name:
                    self.signals.setdefault(name, []).append(payload)
            elif event.event_type == EVENT_VERSION_MARKER_RECORDED:
                change_id = event.attributes.get("change_id")
                version = event.attributes.get("version")
                if change_id is not None and version is not None:
                    self.version_markers[str(change_id)] = int(version)


class WorkflowRunner:
    """
    Deterministic workflow runner that replays history and returns either a new command,
    a waiting state, or final completion.
    """

    def __init__(
        self,
        workflow_func,
        input_payload: Dict[str, Any],
        history: List[HistoryEvent],
        default_retry_policy: RetryPolicy,
    ) -> None:
        self._workflow_func = workflow_func
        self._input = input_payload
        self._history_view = HistoryView(history)
        self._activity_index = 0
        self._timer_index = 0
        self._signal_consumed: Dict[str, int] = {}
        self._default_retry_policy = default_retry_policy

    def run(self) -> WorkflowRunResult:
        context = WorkflowContext(self._default_retry_policy)
        generator = self._workflow_func(context, self._input)
        send_value = None

        try:
            while True:
                try:
                    if send_value is None:
                        operation = next(generator)
                    else:
                        operation = generator.send(send_value)
                    send_value = None
                except StopIteration as exc:
                    return WorkflowRunResult(status="COMPLETED", result=exc.value)

                if isinstance(operation, ActivityCall):
                    result = self._handle_activity(operation)
                    if result.status == "COMMAND":
                        return result
                    if result.status == "WAITING":
                        return result
                    if result.status == "ERROR":
                        try:
                            send_value = generator.throw(
                                ActivityFailedError(result.error or "activity failed", result.result)
                            )
                        except StopIteration as exc:
                            return WorkflowRunResult(status="COMPLETED", result=exc.value)
                    else:
                        send_value = result.result
                elif isinstance(operation, SleepCall):
                    result = self._handle_timer(operation)
                    if result.status == "COMMAND":
                        return result
                    if result.status == "WAITING":
                        return result
                    send_value = result.result
                elif isinstance(operation, WaitSignal):
                    result = self._handle_signal(operation)
                    if result.status == "WAITING":
                        return result
                    send_value = result.result
                elif isinstance(operation, VersionMarker):
                    result = self._handle_version_marker(operation)
                    if result.status == "COMMAND":
                        return result
                    send_value = result.result
                else:
                    raise NonDeterministicError(
                        f"Unsupported operation type {type(operation).__name__}"
                    )
        except Exception as exc:
            return WorkflowRunResult(status="FAILED", error=str(exc))

    def _handle_activity(self, operation: ActivityCall) -> WorkflowRunResult:
        # Replay path: if the activity has already been scheduled in history, we
        # must NOT schedule it again. Instead we look for its completion event.
        if self._activity_index < len(self._history_view.activity_scheduled):
            scheduled_event = self._history_view.activity_scheduled[self._activity_index]
            self._activity_index += 1
            if scheduled_event.attributes.get("activity_name") != operation.name:
                raise NonDeterministicError(
                    f"Activity name mismatch. Expected {scheduled_event.attributes.get('activity_name')} "
                    f"but got {operation.name}"
                )
            activity_id = scheduled_event.attributes.get("activity_id")
            if not activity_id:
                raise NonDeterministicError("Scheduled activity missing activity_id")
            completion = self._history_view.activity_results.get(activity_id)
            if completion is None:
                # The activity is scheduled but has not completed yet. We must
                # suspend the workflow task and wait for the completion event.
                return WorkflowRunResult(status="WAITING")
            if completion.event_type == EVENT_ACTIVITY_TASK_COMPLETED:
                return WorkflowRunResult(status="RESULT", result=completion.attributes.get("result"))
            error_message = completion.attributes.get("error", "activity failed")
            return WorkflowRunResult(status="ERROR", error=error_message, result=completion.attributes)

        # No scheduled activity exists in history at this point, so emit a new
        # command for the engine to persist and schedule.
        return WorkflowRunResult(
            status="COMMAND",
            command=Command(
                command_type="activity",
                attributes={
                    "activity_name": operation.name,
                    "input": operation.input,
                    "retry_policy": operation.retry_policy.to_dict(),
                    "schedule_to_close_timeout_seconds": operation.schedule_to_close_timeout_seconds,
                    "start_to_close_timeout_seconds": operation.start_to_close_timeout_seconds,
                    "heartbeat_timeout_seconds": operation.heartbeat_timeout_seconds,
                },
            ),
        )

    def _handle_timer(self, operation: SleepCall) -> WorkflowRunResult:
        # Replay path: if the timer is already scheduled, check for its firing.
        if self._timer_index < len(self._history_view.timer_scheduled):
            scheduled_event = self._history_view.timer_scheduled[self._timer_index]
            self._timer_index += 1
            timer_id = scheduled_event.attributes.get("timer_id")
            if not timer_id:
                raise NonDeterministicError("Timer scheduled without timer_id")
            fired = self._history_view.timer_results.get(timer_id)
            if fired is None:
                # Timer is scheduled but not fired. Wait until scheduler fires it.
                return WorkflowRunResult(status="WAITING")
            return WorkflowRunResult(status="RESULT", result={"timer_id": timer_id})

        # No timer exists in history yet; emit a new timer command.
        return WorkflowRunResult(
            status="COMMAND",
            command=Command(
                command_type="timer",
                attributes={"duration_seconds": operation.duration_seconds},
            ),
        )

    def _handle_signal(self, operation: WaitSignal) -> WorkflowRunResult:
        name = operation.signal_name
        consumed = self._signal_consumed.get(name, 0)
        available = self._history_view.signals.get(name, [])
        if consumed < len(available):
            payload = available[consumed]
            self._signal_consumed[name] = consumed + 1
            return WorkflowRunResult(status="RESULT", result=payload)
        # Signals are buffered in history; if none are available yet, block.
        return WorkflowRunResult(status="WAITING")

    def _handle_version_marker(self, operation: VersionMarker) -> WorkflowRunResult:
        if operation.change_id in self._history_view.version_markers:
            version = self._history_view.version_markers[operation.change_id]
            if not (operation.min_supported <= version <= operation.max_supported):
                raise NonDeterministicError(
                    f"Version {version} for change_id {operation.change_id} outside supported range"
                )
            return WorkflowRunResult(status="RESULT", result=version)
        return WorkflowRunResult(
            status="COMMAND",
            command=Command(
                command_type="version_marker",
                attributes={
                    "change_id": operation.change_id,
                    "version": operation.max_supported,
                },
            ),
        )

