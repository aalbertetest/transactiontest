from __future__ import annotations

import threading
import time
from typing import Optional

from .config import Config
from .logging_utils import get_logger
from .metrics import MetricsRegistry
from .models import (
    ACTIVITY_STATE_RETRYING,
    ACTIVITY_STATE_SCHEDULED,
    ACTIVITY_STATE_STARTED,
    EVENT_ACTIVITY_TASK_RETRY_SCHEDULED,
    EVENT_ACTIVITY_TASK_TIMED_OUT,
    EVENT_TIMER_FIRED,
    EVENT_TIMER_SCHEDULED,
    WORKFLOW_STATE_FAILED,
)
from .persistence import SQLiteStore
from .queue import TaskQueue
from .retry import compute_backoff_seconds


class TimerScheduler:
    """
    Scans for timers and activity timeouts, firing them and enqueuing workflow tasks.
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
        self._logger = get_logger("scheduler")
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None

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
            time.sleep(self._config.scheduler_interval_seconds)

    def run_once(self) -> None:
        now = int(time.time())
        self._fire_due_timers(now)
        self._handle_activity_timeouts(now)

    def _fire_due_timers(self, now: int) -> None:
        # Timers are deterministic: when a timer is due, record TimerFired and
        # schedule a new workflow task to resume the workflow.
        due = self._store.list_due_timers(now)
        for timer in due:
            timer_id = timer["timer_id"]
            workflow_id = timer["workflow_id"]
            run_id = timer["run_id"]
            self._store.mark_timer_fired(timer_id)
            self._store.append_event(
                workflow_id,
                run_id,
                EVENT_TIMER_FIRED,
                {"timer_id": timer_id},
            )
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
            self._logger.info("timer fired timer_id=%s workflow_id=%s", timer_id, workflow_id)
            if self._metrics:
                self._metrics.increment("scheduler.timer_fired")

    def _handle_activity_timeouts(self, now: int) -> None:
        # Detect activity timeouts by comparing scheduled/start/heartbeat timestamps.
        activities = self._store.list_activity_tasks_by_state(
            [ACTIVITY_STATE_SCHEDULED, ACTIVITY_STATE_STARTED, ACTIVITY_STATE_RETRYING]
        )
        for activity in activities:
            timeout_reason = self._activity_timeout_reason(activity, now)
            if not timeout_reason:
                continue
            error_message = f"activity timeout: {timeout_reason}"
            if activity.attempt + 1 < activity.max_attempts:
                self._store.record_activity_retrying(activity.activity_id, error_message)
                self._store.append_event(
                    activity.workflow_id,
                    activity.run_id,
                    EVENT_ACTIVITY_TASK_TIMED_OUT,
                    {"activity_id": activity.activity_id, "error": error_message},
                )
                self._store.append_event(
                    activity.workflow_id,
                    activity.run_id,
                    EVENT_ACTIVITY_TASK_RETRY_SCHEDULED,
                    {"activity_id": activity.activity_id, "error": error_message},
                )
                backoff = compute_backoff_seconds(activity.retry_policy, activity.attempt + 1)
                payload = {
                    "activity_id": activity.activity_id,
                    "workflow_id": activity.workflow_id,
                    "run_id": activity.run_id,
                }
                self._queue.enqueue(
                    queue_name=self._config.task_queue_name,
                    task_type="activity",
                    payload=payload,
                    visible_at=now + backoff,
                )
                self._logger.warning(
                    "activity timeout retry scheduled activity_id=%s backoff=%s",
                    activity.activity_id,
                    backoff,
                )
                if self._metrics:
                    self._metrics.increment("scheduler.activity_retry")
                continue

            self._store.record_activity_timed_out(activity.activity_id, error_message)
            self._store.append_event(
                activity.workflow_id,
                activity.run_id,
                EVENT_ACTIVITY_TASK_TIMED_OUT,
                {"activity_id": activity.activity_id, "error": error_message},
            )
            execution = self._store.get_workflow_execution(activity.workflow_id, activity.run_id)
            task_queue = execution["task_queue"] if execution else self._config.task_queue_name
            workflow_type = execution["workflow_type"] if execution else "unknown"
            payload = {
                "workflow_id": activity.workflow_id,
                "run_id": activity.run_id,
                "workflow_type": workflow_type,
                "task_queue": task_queue,
            }
            self._queue.enqueue(queue_name=task_queue, task_type="workflow", payload=payload)
            self._logger.error(
                "activity timed out and failed activity_id=%s workflow_id=%s",
                activity.activity_id,
                activity.workflow_id,
            )
            if self._metrics:
                self._metrics.increment("scheduler.activity_timeout")

    @staticmethod
    def _activity_timeout_reason(activity, now: int) -> Optional[str]:
        if activity.state in (ACTIVITY_STATE_SCHEDULED, ACTIVITY_STATE_RETRYING):
            if now - activity.scheduled_at > activity.schedule_to_close_timeout_seconds:
                return "schedule_to_close"
        if activity.state == ACTIVITY_STATE_STARTED:
            if activity.started_at and now - activity.started_at > activity.start_to_close_timeout_seconds:
                return "start_to_close"
            if activity.heartbeat_at and now - activity.heartbeat_at > activity.heartbeat_timeout_seconds:
                return "heartbeat_timeout"
        return None

