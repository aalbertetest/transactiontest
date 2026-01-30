"""
Workflow engine core implementation.
"""

from __future__ import annotations

import threading
import time
import uuid
from typing import Any, Callable, Dict, List, Optional

from .backoff import compute_backoff_seconds
from .config import EngineConfig
from .exceptions import DeterminismError, PendingActivity, PendingTimer, WorkflowApplicationError
from .logging import get_logger
from .metrics import MetricsRegistry
from .persistence import SQLitePersistence
from .queue import TaskQueue
from .state_machine import validate_transition
from .types import Event, Task, TaskState, TaskType, WorkflowExecution, WorkflowState


EVENT_WORKFLOW_STARTED = "WorkflowStarted"
EVENT_WORKFLOW_TASK_SCHEDULED = "WorkflowTaskScheduled"
EVENT_WORKFLOW_TASK_STARTED = "WorkflowTaskStarted"
EVENT_WORKFLOW_TASK_COMPLETED = "WorkflowTaskCompleted"
EVENT_WORKFLOW_COMPLETED = "WorkflowCompleted"
EVENT_WORKFLOW_FAILED = "WorkflowFailed"
EVENT_ACTIVITY_SCHEDULED = "ActivityScheduled"
EVENT_ACTIVITY_STARTED = "ActivityStarted"
EVENT_ACTIVITY_COMPLETED = "ActivityCompleted"
EVENT_ACTIVITY_FAILED = "ActivityFailed"
EVENT_ACTIVITY_TIMED_OUT = "ActivityTimedOut"
EVENT_TIMER_STARTED = "TimerStarted"
EVENT_TIMER_FIRED = "TimerFired"
EVENT_MARKER_RECORDED = "MarkerRecorded"


class WorkflowContext:
    """
    Deterministic workflow execution context.

    The context replays history and emits commands. If a command depends on an
    external result (activity/timer), it raises a Pending* exception to suspend
    workflow execution until the result is available.
    """

    def __init__(
        self,
        workflow_id: str,
        run_id: str,
        history: List[Event],
    ) -> None:
        self.workflow_id = workflow_id
        self.run_id = run_id
        self._history = history
        self._commands: List[Dict[str, Any]] = []
        self._activity_seq = 0
        self._timer_seq = 0
        self._scheduled_activities: Dict[str, Dict[str, Any]] = {}
        self._completed_activities: Dict[str, Dict[str, Any]] = {}
        self._failed_activities: Dict[str, Dict[str, Any]] = {}
        self._started_timers: Dict[str, Dict[str, Any]] = {}
        self._fired_timers: Dict[str, Dict[str, Any]] = {}
        self._markers: Dict[str, int] = {}
        self._index_history()

    def _index_history(self) -> None:
        for event in self._history:
            if event.event_type == EVENT_ACTIVITY_SCHEDULED:
                attrs = event.attributes
                self._scheduled_activities[attrs["activity_id"]] = attrs
            elif event.event_type == EVENT_ACTIVITY_COMPLETED:
                attrs = event.attributes
                self._completed_activities[attrs["activity_id"]] = attrs
            elif event.event_type == EVENT_ACTIVITY_FAILED:
                attrs = event.attributes
                self._failed_activities[attrs["activity_id"]] = attrs
            elif event.event_type == EVENT_TIMER_STARTED:
                attrs = event.attributes
                self._started_timers[attrs["timer_id"]] = attrs
            elif event.event_type == EVENT_TIMER_FIRED:
                attrs = event.attributes
                self._fired_timers[attrs["timer_id"]] = attrs
            elif event.event_type == EVENT_MARKER_RECORDED:
                attrs = event.attributes
                self._markers[attrs["change_id"]] = attrs["version"]

    @property
    def commands(self) -> List[Dict[str, Any]]:
        return self._commands

    def run_activity(
        self,
        name: str,
        input_data: Dict[str, Any],
        timeout_seconds: Optional[int] = None,
        max_attempts: Optional[int] = None,
        heartbeat_interval_seconds: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Schedule an activity and deterministically return its result.
        """
        activity_id = f"{self.workflow_id}:activity:{self._activity_seq}"
        self._activity_seq += 1

        if activity_id in self._completed_activities:
            return self._completed_activities[activity_id]["result"]
        if activity_id in self._failed_activities:
            error = self._failed_activities[activity_id]["error"]
            raise WorkflowApplicationError(error)
        if activity_id in self._scheduled_activities:
            scheduled = self._scheduled_activities[activity_id]
            if scheduled["name"] != name or scheduled["input"] != input_data:
                raise DeterminismError("Activity inputs changed during replay")
            raise PendingActivity(activity_id)

        self._commands.append(
            {
                "type": "ScheduleActivity",
                "activity_id": activity_id,
                "name": name,
                "input": input_data,
                "timeout_seconds": timeout_seconds,
                "max_attempts": max_attempts,
                "heartbeat_interval_seconds": heartbeat_interval_seconds,
            }
        )
        raise PendingActivity(activity_id)

    def sleep(self, seconds: float) -> None:
        """
        Deterministically sleep using a durable timer event.
        """
        timer_id = f"{self.workflow_id}:timer:{self._timer_seq}"
        self._timer_seq += 1

        if timer_id in self._fired_timers:
            return
        if timer_id in self._started_timers:
            started = self._started_timers[timer_id]
            if started["timeout_seconds"] != seconds:
                raise DeterminismError("Timer duration changed during replay")
            raise PendingTimer(timer_id)

        self._commands.append(
            {
                "type": "StartTimer",
                "timer_id": timer_id,
                "timeout_seconds": seconds,
            }
        )
        raise PendingTimer(timer_id)

    def get_version(self, change_id: str, min_version: int, max_version: int) -> int:
        """
        Deterministic versioning primitive.
        """
        if change_id in self._markers:
            return self._markers[change_id]
        self._commands.append(
            {
                "type": "RecordMarker",
                "change_id": change_id,
                "version": max_version,
            }
        )
        return max_version


class ActivityContext:
    """
    Context passed into activities for heartbeats and cancellation checks.
    """

    def __init__(
        self,
        engine: "WorkflowEngine",
        task: Task,
        heartbeat_interval_seconds: Optional[int],
    ) -> None:
        self._engine = engine
        self._task = task
        self._heartbeat_interval_seconds = heartbeat_interval_seconds
        self._last_details: Dict[str, Any] = {}
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def start_heartbeat_loop(self) -> None:
        if not self._heartbeat_interval_seconds:
            return
        self._thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
        self._thread.start()

    def _heartbeat_loop(self) -> None:
        while not self._stop_event.is_set():
            time.sleep(self._heartbeat_interval_seconds)
            if self._stop_event.is_set():
                return
            self.heartbeat(self._last_details)

    def heartbeat(self, details: Dict[str, Any]) -> None:
        self._last_details = details
        self._engine.persistence.heartbeat_task(
            self._task.task_id,
            {
                "workflow_id": self._task.workflow_id,
                "run_id": self._task.run_id,
                "details": details,
            },
            self._engine.config.lease_seconds,
        )

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=1.0)


class WorkflowEngine:
    """
    Core engine responsible for workflow orchestration, scheduling, and replay.
    """

    def __init__(self, config: EngineConfig, persistence: SQLitePersistence) -> None:
        self.config = config
        self.persistence = persistence
        self.logger = get_logger("workflow.engine")
        self.metrics = MetricsRegistry()
        self.workflow_queue = TaskQueue(persistence, config.workflow_queue)
        self.activity_queue = TaskQueue(persistence, config.activity_queue)
        self._workflows: Dict[str, Callable[[WorkflowContext, Dict[str, Any]], Any]] = {}
        self._activities: Dict[str, Callable[[ActivityContext, Dict[str, Any]], Any]] = {}

    def register_workflow(
        self, name: str, handler: Callable[[WorkflowContext, Dict[str, Any]], Any]
    ) -> None:
        self._workflows[name] = handler

    def register_activity(
        self, name: str, handler: Callable[[ActivityContext, Dict[str, Any]], Any]
    ) -> None:
        self._activities[name] = handler

    def start_workflow(self, workflow_type: str, input_data: Dict[str, Any]) -> WorkflowExecution:
        workflow_id = input_data.get("workflow_id") or str(uuid.uuid4())
        run_id = str(uuid.uuid4())
        execution = self.persistence.create_workflow_execution(
            workflow_id=workflow_id,
            run_id=run_id,
            workflow_type=workflow_type,
            input_data=input_data,
        )
        # The start event is the root of the deterministic history.
        self.persistence.append_event(
            workflow_id,
            run_id,
            EVENT_WORKFLOW_STARTED,
            {"workflow_type": workflow_type, "input": input_data},
        )
        # Initial workflow task drives the first deterministic decision.
        self._schedule_workflow_task(workflow_id, run_id)
        self.metrics.counter("workflows_started").inc()
        return execution

    def _schedule_workflow_task(self, workflow_id: str, run_id: str) -> None:
        self.persistence.append_event(
            workflow_id,
            run_id,
            EVENT_WORKFLOW_TASK_SCHEDULED,
            {"queue": self.config.workflow_queue},
        )
        self.workflow_queue.enqueue(
            task_type=TaskType.WORKFLOW_TASK,
            workflow_id=workflow_id,
            run_id=run_id,
            payload={},
            max_attempts=self.config.workflow_max_attempts,
            timeout_seconds=self.config.workflow_task_timeout_seconds,
        )

    def _schedule_activity_task(
        self,
        workflow_id: str,
        run_id: str,
        activity_id: str,
        name: str,
        input_data: Dict[str, Any],
        timeout_seconds: Optional[int],
        max_attempts: Optional[int],
        heartbeat_interval_seconds: Optional[int],
        not_before: Optional[float] = None,
    ) -> None:
        payload = {
            "activity_id": activity_id,
            "name": name,
            "input": input_data,
            "heartbeat_interval_seconds": heartbeat_interval_seconds,
        }
        self.persistence.append_event(
            workflow_id,
            run_id,
            EVENT_ACTIVITY_SCHEDULED,
            {
                "activity_id": activity_id,
                "name": name,
                "input": input_data,
                "timeout_seconds": timeout_seconds,
                "max_attempts": max_attempts,
                "heartbeat_interval_seconds": heartbeat_interval_seconds,
            },
        )
        self.activity_queue.enqueue(
            task_type=TaskType.ACTIVITY_TASK,
            workflow_id=workflow_id,
            run_id=run_id,
            payload=payload,
            max_attempts=max_attempts or self.config.activity_max_attempts,
            not_before=not_before,
            timeout_seconds=timeout_seconds or self.config.activity_task_timeout_seconds,
        )

    def _start_timer(
        self,
        workflow_id: str,
        run_id: str,
        timer_id: str,
        timeout_seconds: float,
    ) -> None:
        fire_at = time.time() + timeout_seconds
        self.persistence.append_event(
            workflow_id,
            run_id,
            EVENT_TIMER_STARTED,
            {"timer_id": timer_id, "timeout_seconds": timeout_seconds},
        )
        # Use timer task type to allow the scheduler to deliver it when due.
        self.persistence.create_task(
            queue="timer",
            task_type=TaskType.TIMER_TASK,
            workflow_id=workflow_id,
            run_id=run_id,
            payload={"timer_id": timer_id},
            max_attempts=1,
            not_before=fire_at,
            timeout_seconds=None,
        )

    def execute_workflow_task(self, task: Task, worker_id: str) -> None:
        execution = self.persistence.get_workflow_execution(task.workflow_id, task.run_id)
        if execution.state != WorkflowState.RUNNING:
            self.logger.info("Skipping workflow task for non-running workflow %s", execution.workflow_id)
            self.workflow_queue.complete(task.task_id)
            return

        # Record that the worker began processing the workflow task.
        self.persistence.append_event(
            task.workflow_id,
            task.run_id,
            EVENT_WORKFLOW_TASK_STARTED,
            {"worker_id": worker_id},
        )
        history = self.persistence.list_events(task.workflow_id, task.run_id)
        # The workflow context replays history to ensure deterministic execution.
        context = WorkflowContext(task.workflow_id, task.run_id, history)
        workflow_fn = self._workflows.get(execution.workflow_type)
        if not workflow_fn:
            raise KeyError(f"Workflow type not registered: {execution.workflow_type}")

        workflow_result: Optional[Any] = None
        failure: Optional[str] = None
        try:
            workflow_result = workflow_fn(context, execution.input)
            # If we reach here without pending exceptions, complete workflow.
            context.commands.append({"type": "CompleteWorkflow", "result": workflow_result})
        except PendingActivity:
            pass
        except PendingTimer:
            pass
        except WorkflowApplicationError as exc:
            failure = str(exc)
            context.commands.append({"type": "FailWorkflow", "error": failure})
        except Exception as exc:  # pylint: disable=broad-except
            failure = f"Unhandled workflow error: {exc}"
            context.commands.append({"type": "FailWorkflow", "error": failure})

        # Apply commands deterministically.
        for command in context.commands:
            cmd_type = command["type"]
            if cmd_type == "ScheduleActivity":
                # Schedule activity and record ActivityScheduled event.
                self._schedule_activity_task(
                    workflow_id=task.workflow_id,
                    run_id=task.run_id,
                    activity_id=command["activity_id"],
                    name=command["name"],
                    input_data=command["input"],
                    timeout_seconds=command.get("timeout_seconds"),
                    max_attempts=command.get("max_attempts"),
                    heartbeat_interval_seconds=command.get("heartbeat_interval_seconds"),
                )
            elif cmd_type == "StartTimer":
                # Timers are durable tasks delivered by the scheduler.
                self._start_timer(
                    workflow_id=task.workflow_id,
                    run_id=task.run_id,
                    timer_id=command["timer_id"],
                    timeout_seconds=command["timeout_seconds"],
                )
            elif cmd_type == "RecordMarker":
                # Markers drive deterministic versioning.
                self.persistence.append_event(
                    task.workflow_id,
                    task.run_id,
                    EVENT_MARKER_RECORDED,
                    {"change_id": command["change_id"], "version": command["version"]},
                )
            elif cmd_type == "CompleteWorkflow":
                # Terminal state: workflow completed successfully.
                self.persistence.append_event(
                    task.workflow_id,
                    task.run_id,
                    EVENT_WORKFLOW_COMPLETED,
                    {"result": command["result"]},
                )
                validate_transition(execution.state, WorkflowState.COMPLETED)
                self.persistence.update_workflow_state(
                    task.workflow_id, task.run_id, WorkflowState.COMPLETED, time.time()
                )
                self.metrics.counter("workflows_completed").inc()
            elif cmd_type == "FailWorkflow":
                # Terminal state: workflow failed.
                self.persistence.append_event(
                    task.workflow_id,
                    task.run_id,
                    EVENT_WORKFLOW_FAILED,
                    {"error": command["error"]},
                )
                validate_transition(execution.state, WorkflowState.FAILED)
                self.persistence.update_workflow_state(
                    task.workflow_id, task.run_id, WorkflowState.FAILED, time.time()
                )
                self.metrics.counter("workflows_failed").inc()
            else:
                raise ValueError(f"Unknown command type: {cmd_type}")

        self.persistence.append_event(
            task.workflow_id,
            task.run_id,
            EVENT_WORKFLOW_TASK_COMPLETED,
            {"worker_id": worker_id},
        )
        self.workflow_queue.complete(task.task_id)

    def execute_activity_task(self, task: Task, worker_id: str) -> None:
        payload = task.payload
        activity_id = payload["activity_id"]
        name = payload["name"]
        input_data = payload["input"]
        activity_fn = self._activities.get(name)
        if not activity_fn:
            raise KeyError(f"Activity not registered: {name}")

        # Record that the activity has started before running user code.
        self.persistence.append_event(
            task.workflow_id,
            task.run_id,
            EVENT_ACTIVITY_STARTED,
            {"activity_id": activity_id, "worker_id": worker_id},
        )
        context = ActivityContext(self, task, payload.get("heartbeat_interval_seconds"))
        context.start_heartbeat_loop()
        try:
            # Execute activity logic and record the completion result.
            result = activity_fn(context, input_data)
            context.stop()
            self.persistence.append_event(
                task.workflow_id,
                task.run_id,
                EVENT_ACTIVITY_COMPLETED,
                {"activity_id": activity_id, "result": result},
            )
            self.activity_queue.complete(task.task_id)
            # Schedule a new workflow task to resume execution.
            self._schedule_workflow_task(task.workflow_id, task.run_id)
            self.metrics.counter("activities_completed").inc()
        except Exception as exc:  # pylint: disable=broad-except
            context.stop()
            error = f"Activity error: {exc}"
            self.persistence.append_event(
                task.workflow_id,
                task.run_id,
                EVENT_ACTIVITY_FAILED,
                {"activity_id": activity_id, "error": error},
            )
            retry_delay = compute_backoff_seconds(
                attempt=task.attempts + 1,
                initial_seconds=self.config.backoff_initial_seconds,
                max_seconds=self.config.backoff_max_seconds,
                jitter=self.config.backoff_jitter,
            )
            retry_at = time.time() + retry_delay
            task_update = self.activity_queue.fail(task.task_id, error, retry_at)
            if task_update.state == TaskState.FAILED:
                # If retries are exhausted, resume workflow with failure recorded.
                self._schedule_workflow_task(task.workflow_id, task.run_id)
            self.metrics.counter("activities_failed").inc()

    def handle_timer_task(self, task: Task) -> None:
        timer_id = task.payload["timer_id"]
        self.persistence.append_event(
            task.workflow_id,
            task.run_id,
            EVENT_TIMER_FIRED,
            {"timer_id": timer_id},
        )
        self.persistence.complete_task(task.task_id)
        self._schedule_workflow_task(task.workflow_id, task.run_id)

    def handle_task_timeout(self, task: Task) -> None:
        """
        Called by scheduler to handle expired leases.
        """
        if task.task_type == TaskType.ACTIVITY_TASK:
            activity_id = task.payload["activity_id"]
            # Timeout is treated as a failure that may be retried.
            self.persistence.append_event(
                task.workflow_id,
                task.run_id,
                EVENT_ACTIVITY_TIMED_OUT,
                {"activity_id": activity_id},
            )
            retry_delay = compute_backoff_seconds(
                attempt=task.attempts + 1,
                initial_seconds=self.config.backoff_initial_seconds,
                max_seconds=self.config.backoff_max_seconds,
                jitter=self.config.backoff_jitter,
            )
            retry_at = time.time() + retry_delay
            task_update = self.activity_queue.fail(task.task_id, "timeout", retry_at)
            if task_update.state == TaskState.FAILED:
                self._schedule_workflow_task(task.workflow_id, task.run_id)
        elif task.task_type == TaskType.WORKFLOW_TASK:
            # Workflow task timeout triggers a new workflow task for replay.
            retry_delay = compute_backoff_seconds(
                attempt=task.attempts + 1,
                initial_seconds=self.config.backoff_initial_seconds,
                max_seconds=self.config.backoff_max_seconds,
                jitter=self.config.backoff_jitter,
            )
            retry_at = time.time() + retry_delay
            task_update = self.workflow_queue.fail(task.task_id, "workflow task timeout", retry_at)
            if task_update.state == TaskState.FAILED:
                self.persistence.append_event(
                    task.workflow_id,
                    task.run_id,
                    EVENT_WORKFLOW_FAILED,
                    {"error": "Workflow task timed out and max attempts exceeded"},
                )
                self.persistence.update_workflow_state(
                    task.workflow_id, task.run_id, WorkflowState.FAILED, time.time()
                )
        else:
            self.persistence.complete_task(task.task_id)
