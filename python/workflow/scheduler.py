"""
Scheduler loop to deliver timers and handle expired task leases.
"""

from __future__ import annotations

import threading
import time
import uuid
from typing import Optional

from .config import EngineConfig
from .engine import WorkflowEngine
from .logging import get_logger
from .types import TaskType


class Scheduler:
    """
    Scheduler that scans for timers and expired tasks.
    """

    def __init__(self, engine: WorkflowEngine, config: EngineConfig, scheduler_id: Optional[str] = None) -> None:
        self.engine = engine
        self.config = config
        self.scheduler_id = scheduler_id or f"scheduler-{uuid.uuid4()}"
        self.logger = get_logger("workflow.scheduler")

    def run(self, stop_event: threading.Event) -> None:
        self.logger.info("Scheduler %s started", self.scheduler_id)
        while not stop_event.is_set():
            # Deliver timers.
            due_timers = self.engine.persistence.list_due_timers()
            for task in due_timers:
                try:
                    self.logger.info("Delivering timer task %s", task.task_id)
                    self.engine.handle_timer_task(task)
                except Exception as exc:  # pylint: disable=broad-except
                    self.logger.exception("Timer task handling error: %s", exc)

            # Handle expired leases (timeouts).
            expired_tasks = self.engine.persistence.list_expired_leases()
            for task in expired_tasks:
                try:
                    self.logger.warning("Handling expired task lease %s", task.task_id)
                    self.engine.handle_task_timeout(task)
                except Exception as exc:  # pylint: disable=broad-except
                    self.logger.exception("Expired lease handling error: %s", exc)

            time.sleep(self.config.scheduler_poll_interval_seconds)
        self.logger.info("Scheduler %s stopped", self.scheduler_id)

    def start_in_thread(self) -> threading.Event:
        stop_event = threading.Event()
        thread = threading.Thread(target=self.run, args=(stop_event,), daemon=True)
        thread.start()
        return stop_event
