"""
Background scheduler for timeout and heartbeat sweeps.
"""

from __future__ import annotations

import threading
import time
from typing import Optional

from .engine import WorkflowEngine
from .logging_utils import get_logger


class Scheduler:
    def __init__(self, engine: WorkflowEngine) -> None:
        self._engine = engine
        self._stop_event = threading.Event()
        self._thread: Optional[threading.Thread] = None
        self._logger = get_logger("scheduler")

    def start(self) -> None:
        self._thread = threading.Thread(target=self.run, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop_event.set()
        if self._thread:
            self._thread.join(timeout=5)

    def run(self) -> None:
        while not self._stop_event.is_set():
            now = time.time()
            heartbeat_expired = self._engine.persistence.find_heartbeat_expired_tasks(now)
            for task in heartbeat_expired:
                self._logger.warning("Heartbeat timeout for task %s", task.task_id)
                self._engine.record_heartbeat_timeout(task.task_id)

            timed_out = self._engine.persistence.find_timeout_expired_tasks(now)
            for task in timed_out:
                self._logger.warning("Task timeout for task %s", task.task_id)
                self._engine.record_task_timeout(task.task_id)

            run_timeouts = self._engine.persistence.find_run_timeouts(now)
            for run in run_timeouts:
                self._logger.warning("Workflow run timeout for %s", run["run_id"])
                self._engine.record_run_timeout(run["run_id"])

            time.sleep(self._engine.config.scheduler_interval_seconds)
