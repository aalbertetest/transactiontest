"""
Worker processes for workflow, activity, and timer tasks.
"""

from __future__ import annotations

import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from typing import Optional

from .engine import ActivityContext, WorkflowEngine
from .logging_utils import get_logger


class BaseWorker:
    def __init__(self, name: str, engine: WorkflowEngine, concurrency: int = 1) -> None:
        self._name = name
        self._engine = engine
        self._concurrency = concurrency
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._logger = get_logger(name)

    def start(self) -> None:
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

    def run(self) -> None:
        raise NotImplementedError

    @property
    def stopped(self) -> bool:
        return self._stop_event.is_set()


class WorkflowWorker(BaseWorker):
    def run(self) -> None:
        while not self.stopped:
            tasks = self._engine.queue.lease_tasks(
                self._engine.config.workflow_task_queue,
                limit=self._concurrency,
                lease_seconds=self._engine.config.task_lease_seconds,
            )
            if not tasks:
                time.sleep(self._engine.config.worker_poll_interval_seconds)
                continue
            for task in tasks:
                try:
                    self._engine.process_workflow_task(task)
                except Exception as exc:
                    self._logger.exception("Workflow task failed: %s", exc)
                    self._engine.queue.fail_task(task.task_id, str(exc))


class ActivityWorker(BaseWorker):
    def run(self) -> None:
        while not self.stopped:
            tasks = self._engine.queue.lease_tasks(
                self._engine.config.activity_task_queue,
                limit=self._concurrency,
                lease_seconds=self._engine.config.task_lease_seconds,
            )
            if not tasks:
                time.sleep(self._engine.config.worker_poll_interval_seconds)
                continue
            for task in tasks:
                self._handle_task(task)

    def _handle_task(self, task) -> None:
        payload = task.payload
        activity_name = payload.get("activity_name")
        if activity_name not in self._engine._activities:
            self._engine.queue.fail_task(task.task_id, "unknown_activity")
            return
        definition = self._engine._activities[activity_name]
        self._engine.record_activity_started(task.run_id, payload.get("activity_id", ""), task.task_id, task.attempt)
        context = ActivityContext(self._engine, task.task_id)

        def _run_activity():
            return definition.func(context, payload.get("input", {}))

        with ThreadPoolExecutor(max_workers=1) as executor:
            future = executor.submit(_run_activity)
            try:
                result = future.result(timeout=definition.timeout_seconds)
            except FutureTimeout:
                self._engine.queue.fail_task(task.task_id, "timeout")
                self._engine.record_activity_failed(
                    run_id=task.run_id,
                    activity_id=payload.get("activity_id", ""),
                    error="timeout",
                    task_id=task.task_id,
                    attempt=task.attempt,
                    retry_policy=definition.retry_policy,
                )
                return
            except Exception as exc:
                self._engine.queue.fail_task(task.task_id, str(exc))
                self._engine.record_activity_failed(
                    run_id=task.run_id,
                    activity_id=payload.get("activity_id", ""),
                    error=str(exc),
                    task_id=task.task_id,
                    attempt=task.attempt,
                    retry_policy=definition.retry_policy,
                )
                return

        self._engine.queue.complete_task(task.task_id)
        self._engine.record_activity_completed(
            run_id=task.run_id,
            activity_id=payload.get("activity_id", ""),
            result=result,
            task_id=task.task_id,
            attempt=task.attempt,
        )


class TimerWorker(BaseWorker):
    def run(self) -> None:
        while not self.stopped:
            tasks = self._engine.queue.lease_tasks(
                self._engine.config.timer_task_queue,
                limit=self._concurrency,
                lease_seconds=self._engine.config.task_lease_seconds,
            )
            if not tasks:
                time.sleep(self._engine.config.worker_poll_interval_seconds)
                continue
            for task in tasks:
                payload = task.payload
                self._engine.record_timer_fired(task.run_id, payload.get("timer_id", ""))
                self._engine.queue.complete_task(task.task_id)
