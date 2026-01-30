from __future__ import annotations

import time
from typing import Any, Dict, Optional

from .config import Config
from .logging_utils import get_logger
from .metrics import MetricsRegistry
from .models import (
    EVENT_SIGNAL_RECEIVED,
    EVENT_WORKFLOW_EXECUTION_STARTED,
    EVENT_WORKFLOW_TASK_SCHEDULED,
    WORKFLOW_STATE_RUNNING,
    WORKFLOW_STATE_WAITING,
)
from .persistence import SQLiteStore
from .queue import TaskQueue


class WorkflowEngine:
    """
    Core workflow engine API. This is the entry point for clients that start
    workflows and send signals.
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
        self._logger = get_logger("engine")

    def start_workflow(
        self,
        workflow_id: str,
        workflow_type: str,
        input_payload: Dict[str, Any],
        task_queue: Optional[str] = None,
    ) -> str:
        if task_queue is None:
            task_queue = self._config.task_queue_name
        run_id = self._store.create_workflow_execution(
            workflow_id=workflow_id,
            workflow_type=workflow_type,
            input_payload=input_payload,
            task_queue=task_queue,
        )
        self._store.append_event(
            workflow_id,
            run_id,
            EVENT_WORKFLOW_EXECUTION_STARTED,
            {
                "workflow_type": workflow_type,
                "input": input_payload,
                "task_queue": task_queue,
            },
        )
        self._schedule_workflow_task(workflow_id, run_id, workflow_type, task_queue)
        if self._metrics:
            self._metrics.increment("engine.start_workflow")
        self._logger.info("workflow started workflow_id=%s run_id=%s", workflow_id, run_id)
        return run_id

    def signal_workflow(
        self,
        workflow_id: str,
        run_id: str,
        signal_name: str,
        payload: Dict[str, Any],
    ) -> None:
        self._store.append_event(
            workflow_id,
            run_id,
            EVENT_SIGNAL_RECEIVED,
            {
                "signal_name": signal_name,
                "payload": payload,
            },
        )
        execution = self._store.get_workflow_execution(workflow_id, run_id)
        task_queue = execution["task_queue"] if execution else self._config.task_queue_name
        self._schedule_workflow_task(workflow_id, run_id, execution["workflow_type"], task_queue)
        if execution and execution["state"] == WORKFLOW_STATE_WAITING:
            self._store.set_workflow_state(workflow_id, run_id, WORKFLOW_STATE_RUNNING)
        if self._metrics:
            self._metrics.increment("engine.signal_workflow")
        self._logger.info(
            "workflow signaled workflow_id=%s run_id=%s signal=%s",
            workflow_id,
            run_id,
            signal_name,
        )

    def _schedule_workflow_task(
        self, workflow_id: str, run_id: str, workflow_type: str, task_queue: str
    ) -> None:
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

