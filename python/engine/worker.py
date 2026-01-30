from __future__ import annotations

import json
import threading
import time
from typing import Any, Callable, Dict, Optional

from .config import Config
from .logging_utils import get_logger
from .metrics import MetricsRegistry
from .models import (
    ACTIVITY_STATE_COMPLETED,
    ACTIVITY_STATE_FAILED,
    ACTIVITY_STATE_TIMED_OUT,
    EVENT_ACTIVITY_TASK_COMPLETED,
    EVENT_ACTIVITY_TASK_FAILED,
    EVENT_ACTIVITY_TASK_RETRY_SCHEDULED,
    EVENT_ACTIVITY_TASK_SCHEDULED,
    EVENT_ACTIVITY_TASK_STARTED,
    EVENT_TIMER_SCHEDULED,
    EVENT_VERSION_MARKER_RECORDED,
    EVENT_WORKFLOW_EXECUTION_COMPLETED,
    EVENT_WORKFLOW_EXECUTION_FAILED,
    EVENT_WORKFLOW_TASK_COMPLETED,
    EVENT_WORKFLOW_TASK_STARTED,
    EVENT_WORKFLOW_TASK_SCHEDULED,
    WORKFLOW_STATE_COMPLETED,
    WORKFLOW_STATE_FAILED,
    WORKFLOW_STATE_RUNNING,
    WORKFLOW_STATE_WAITING,
    RetryPolicy,
)
from .persistence import SQLiteStore
from .queue import TaskQueue
from .retry import compute_backoff_seconds
from .runtime import WorkflowRunner


class ActivityContext:
    """
    Execution context for activities, allowing heartbeats.
    """

    def __init__(self, store: SQLiteStore, activity_id: str) -> None:
        self._store = store
        self._activity_id = activity_id

    def heartbeat(self, details: Dict[str, Any]) -> None:
        self._store.record_activity_heartbeat(self._activity_id, details)


class Worker:
    """
    Worker that polls workflow and activity task queues.
    """

    def __init__(
        self,
        store: SQLiteStore,
        queue: TaskQueue,
        config: Config,
        metrics: Optional[MetricsRegistry] = None,
    ) -> None:
        self._store = store
        self._queue = queue
        self._config = config
        self._metrics = metrics
        self._logger = get_logger("worker")
        self._workflow_registry: Dict[str, Callable[..., Any]] = {}
        self._activity_registry: Dict[str, Callable[..., Any]] = {}
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

    def register_workflow(self, name: str, workflow_func: Callable[..., Any]) -> None:
        self._workflow_registry[name] = workflow_func

    def register_activity(self, name: str, activity_func: Callable[..., Any]) -> None:
        self._activity_registry[name] = activity_func

    def start(self) -> None:
        self._stop_event.clear()
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

    def run(self) -> None:
        while not self._stop_event.is_set():
            self.run_once()
            time.sleep(self._config.poll_interval_seconds)

    def run_once(self) -> None:
        workflow_task = self._queue.poll(
            queue_name=self._config.task_queue_name,
            task_type="workflow",
            lease_duration_seconds=self._config.lease_duration_seconds,
            worker_id=self._config.worker_id,
        )
        if workflow_task:
            self._handle_workflow_task(workflow_task)

        activity_task = self._queue.poll(
            queue_name=self._config.task_queue_name,
            task_type="activity",
            lease_duration_seconds=self._config.lease_duration_seconds,
            worker_id=self._config.worker_id,
        )
        if activity_task:
            self._handle_activity_task(activity_task)

    def _handle_workflow_task(self, task) -> None:
        payload = task.payload
        workflow_id = payload["workflow_id"]
        run_id = payload["run_id"]
        workflow_type = payload["workflow_type"]
        execution = self._store.get_workflow_execution(workflow_id, run_id)
        if not execution:
            self._queue.ack(task.id)
            return
        if execution["state"] in (WORKFLOW_STATE_COMPLETED, WORKFLOW_STATE_FAILED):
            self._queue.ack(task.id)
            return

        # Lookup workflow function by name. This keeps the workflow type stable
        # across replays while allowing code updates.
        workflow_func = self._workflow_registry.get(workflow_type)
        if not workflow_func:
            self._store.set_workflow_state(workflow_id, run_id, WORKFLOW_STATE_FAILED, error="workflow type not registered")
            self._queue.ack(task.id)
            return

        # Append a WorkflowTaskStarted event for auditable task ownership.
        self._store.append_event(workflow_id, run_id, EVENT_WORKFLOW_TASK_STARTED, {"worker_id": self._config.worker_id})
        history = self._store.get_history(workflow_id, run_id)
        default_retry = RetryPolicy(
            initial_interval_seconds=self._config.retry_initial_interval_seconds,
            max_interval_seconds=self._config.retry_max_interval_seconds,
            backoff_coefficient=self._config.retry_backoff_coefficient,
            max_attempts=self._config.retry_max_attempts,
        )
        runner = WorkflowRunner(
            workflow_func=workflow_func,
            input_payload=self._parse_input(execution["input"]),
            history=history,
            default_retry_policy=default_retry,
        )
        result = runner.run()

        if result.status == "COMMAND" and result.command:
            command_type = result.command.command_type
            if command_type == "activity":
                # Persist the activity task and then enqueue it for workers.
                activity_id = self._store.create_activity_task(
                    workflow_id=workflow_id,
                    run_id=run_id,
                    activity_name=result.command.attributes["activity_name"],
                    input_payload=result.command.attributes["input"],
                    retry_policy=RetryPolicy.from_dict(result.command.attributes["retry_policy"]),
                    schedule_to_close_timeout_seconds=result.command.attributes["schedule_to_close_timeout_seconds"],
                    start_to_close_timeout_seconds=result.command.attributes["start_to_close_timeout_seconds"],
                    heartbeat_timeout_seconds=result.command.attributes["heartbeat_timeout_seconds"],
                )
                self._store.append_event(
                    workflow_id,
                    run_id,
                    EVENT_ACTIVITY_TASK_SCHEDULED,
                    {
                        "activity_id": activity_id,
                        "activity_name": result.command.attributes["activity_name"],
                        "input": result.command.attributes["input"],
                    },
                )
                self._queue.enqueue(
                    queue_name=self._config.task_queue_name,
                    task_type="activity",
                    payload={
                        "activity_id": activity_id,
                        "workflow_id": workflow_id,
                        "run_id": run_id,
                    },
                )
                self._store.append_event(
                    workflow_id, run_id, EVENT_WORKFLOW_TASK_COMPLETED, {"status": "COMMAND"}
                )
            elif command_type == "timer":
                # Timers are driven by the scheduler and produce TimerFired events.
                fire_at = int(time.time()) + int(result.command.attributes["duration_seconds"])
                timer_id = self._store.create_timer(workflow_id, run_id, fire_at)
                self._store.append_event(
                    workflow_id,
                    run_id,
                    EVENT_TIMER_SCHEDULED,
                    {"timer_id": timer_id, "fire_at": fire_at},
                )
                self._store.append_event(
                    workflow_id, run_id, EVENT_WORKFLOW_TASK_COMPLETED, {"status": "COMMAND"}
                )
            elif command_type == "version_marker":
                self._store.append_event(
                    workflow_id,
                    run_id,
                    EVENT_VERSION_MARKER_RECORDED,
                    result.command.attributes,
                )
                self._store.append_event(
                    workflow_id, run_id, EVENT_WORKFLOW_TASK_COMPLETED, {"status": "COMMAND"}
                )
                payload = {
                    "workflow_id": workflow_id,
                    "run_id": run_id,
                    "workflow_type": workflow_type,
                    "task_queue": self._config.task_queue_name,
                }
                self._queue.enqueue(queue_name=self._config.task_queue_name, task_type="workflow", payload=payload)
            else:
                self._store.append_event(
                    workflow_id, run_id, EVENT_WORKFLOW_TASK_COMPLETED, {"status": "UNKNOWN_COMMAND"}
                )
        elif result.status == "WAITING":
            self._store.set_workflow_state(workflow_id, run_id, WORKFLOW_STATE_WAITING)
            self._store.append_event(
                workflow_id, run_id, EVENT_WORKFLOW_TASK_COMPLETED, {"status": "WAITING"}
            )
        elif result.status == "COMPLETED":
            self._store.set_workflow_state(workflow_id, run_id, WORKFLOW_STATE_COMPLETED, result={"result": result.result})
            self._store.append_event(
                workflow_id, run_id, EVENT_WORKFLOW_EXECUTION_COMPLETED, {"result": result.result}
            )
            self._store.append_event(
                workflow_id, run_id, EVENT_WORKFLOW_TASK_COMPLETED, {"status": "COMPLETED"}
            )
        else:
            self._store.set_workflow_state(workflow_id, run_id, WORKFLOW_STATE_FAILED, error=result.error)
            self._store.append_event(
                workflow_id, run_id, EVENT_WORKFLOW_EXECUTION_FAILED, {"error": result.error}
            )
            self._store.append_event(
                workflow_id, run_id, EVENT_WORKFLOW_TASK_COMPLETED, {"status": "FAILED"}
            )
        self._queue.ack(task.id)

        if self._metrics:
            self._metrics.increment("worker.workflow_task")

    def _handle_activity_task(self, task) -> None:
        payload = task.payload
        activity_id = payload["activity_id"]
        activity = self._store.get_activity_task(activity_id)
        if not activity:
            self._queue.ack(task.id)
            return
        if activity.state in (ACTIVITY_STATE_COMPLETED, ACTIVITY_STATE_FAILED, ACTIVITY_STATE_TIMED_OUT):
            self._queue.ack(task.id)
            return

        activity_func = self._activity_registry.get(activity.activity_name)
        if not activity_func:
            self._store.record_activity_failed(activity_id, "activity not registered")
            self._queue.ack(task.id)
            return

        self._store.record_activity_started(activity_id, self._config.worker_id)
        self._store.append_event(
            activity.workflow_id,
            activity.run_id,
            EVENT_ACTIVITY_TASK_STARTED,
            {"activity_id": activity_id, "worker_id": self._config.worker_id},
        )
        ctx = ActivityContext(self._store, activity_id)
        try:
            result = activity_func(ctx, activity.input)
            self._store.record_activity_completed(activity_id, result)
            self._store.append_event(
                activity.workflow_id,
                activity.run_id,
                EVENT_ACTIVITY_TASK_COMPLETED,
                {"activity_id": activity_id, "result": result},
            )
            self._schedule_workflow_after_activity(activity.workflow_id, activity.run_id)
        except Exception as exc:
            error_message = str(exc)
            if activity.attempt + 1 < activity.max_attempts:
                self._store.record_activity_retrying(activity_id, error_message)
                self._store.append_event(
                    activity.workflow_id,
                    activity.run_id,
                    EVENT_ACTIVITY_TASK_FAILED,
                    {"activity_id": activity_id, "error": error_message},
                )
                self._store.append_event(
                    activity.workflow_id,
                    activity.run_id,
                    EVENT_ACTIVITY_TASK_RETRY_SCHEDULED,
                    {"activity_id": activity_id, "error": error_message},
                )
                backoff = compute_backoff_seconds(activity.retry_policy, activity.attempt + 1)
                self._queue.enqueue(
                    queue_name=self._config.task_queue_name,
                    task_type="activity",
                    payload={
                        "activity_id": activity_id,
                        "workflow_id": activity.workflow_id,
                        "run_id": activity.run_id,
                    },
                    visible_at=int(time.time()) + backoff,
                )
                self._logger.warning(
                    "activity failed retry scheduled activity_id=%s backoff=%s",
                    activity_id,
                    backoff,
                )
            else:
                self._store.record_activity_failed(activity_id, error_message)
                self._store.append_event(
                    activity.workflow_id,
                    activity.run_id,
                    EVENT_ACTIVITY_TASK_FAILED,
                    {"activity_id": activity_id, "error": error_message},
                )
                self._schedule_workflow_after_activity(activity.workflow_id, activity.run_id)
        self._queue.ack(task.id)
        if self._metrics:
            self._metrics.increment("worker.activity_task")

    def _schedule_workflow_after_activity(self, workflow_id: str, run_id: str) -> None:
        execution = self._store.get_workflow_execution(workflow_id, run_id)
        task_queue = execution["task_queue"] if execution else self._config.task_queue_name
        workflow_type = execution["workflow_type"] if execution else "unknown"
        payload = {
            "workflow_id": workflow_id,
            "run_id": run_id,
            "workflow_type": workflow_type,
            "task_queue": task_queue,
        }
        self._queue.enqueue(queue_name=task_queue, task_type="workflow", payload=payload)
        self._store.append_event(
            workflow_id,
            run_id,
            EVENT_WORKFLOW_TASK_SCHEDULED,
            {"task_queue": task_queue},
        )
        if execution and execution["state"] == WORKFLOW_STATE_WAITING:
            self._store.set_workflow_state(workflow_id, run_id, WORKFLOW_STATE_RUNNING)

    @staticmethod
    def _parse_input(input_json: str) -> Dict[str, Any]:
        if not input_json:
            return {}
        try:
            return json.loads(input_json)
        except Exception:
            return {}

