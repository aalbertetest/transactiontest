"""
Worker process that polls task queues and executes tasks.
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


class Worker:
    """
    Worker that polls workflow and activity queues.
    """

    def __init__(self, engine: WorkflowEngine, config: EngineConfig, worker_id: Optional[str] = None) -> None:
        self.engine = engine
        self.config = config
        self.worker_id = worker_id or f"worker-{uuid.uuid4()}"
        self.logger = get_logger("workflow.worker")

    def run(self, stop_event: threading.Event) -> None:
        """
        Run the polling loop until stop_event is set.
        """
        self.logger.info("Worker %s started", self.worker_id)
        while not stop_event.is_set():
            task = self.engine.workflow_queue.poll(self.worker_id, self.config.lease_seconds)
            if task:
                self.logger.info("Worker %s executing workflow task %s", self.worker_id, task.task_id)
                try:
                    self.engine.execute_workflow_task(task, self.worker_id)
                except Exception as exc:  # pylint: disable=broad-except
                    self.logger.exception("Workflow task failed: %s", exc)
                continue

            task = self.engine.activity_queue.poll(self.worker_id, self.config.lease_seconds)
            if task:
                self.logger.info("Worker %s executing activity task %s", self.worker_id, task.task_id)
                try:
                    self.engine.execute_activity_task(task, self.worker_id)
                except Exception as exc:  # pylint: disable=broad-except
                    self.logger.exception("Activity task failed: %s", exc)
                continue

            time.sleep(self.config.worker_poll_interval_seconds)
        self.logger.info("Worker %s stopped", self.worker_id)

    def start_in_thread(self) -> threading.Event:
        stop_event = threading.Event()
        thread = threading.Thread(target=self.run, args=(stop_event,), daemon=True)
        thread.start()
        return stop_event
