"""
Queue abstraction for task scheduling and polling.
"""

from __future__ import annotations

from typing import Optional

from .persistence import SQLitePersistence
from .types import Task, TaskType


class TaskQueue:
    """
    Queue abstraction backed by the persistence layer.
    """

    def __init__(self, persistence: SQLitePersistence, queue_name: str) -> None:
        self._persistence = persistence
        self._queue_name = queue_name

    def enqueue(
        self,
        task_type: TaskType,
        workflow_id: str,
        run_id: str,
        payload: dict,
        max_attempts: int,
        not_before: float | None = None,
        timeout_seconds: int | None = None,
    ) -> Task:
        return self._persistence.create_task(
            queue=self._queue_name,
            task_type=task_type,
            workflow_id=workflow_id,
            run_id=run_id,
            payload=payload,
            max_attempts=max_attempts,
            not_before=not_before,
            timeout_seconds=timeout_seconds,
        )

    def poll(self, worker_id: str, lease_seconds: int) -> Optional[Task]:
        return self._persistence.poll_task(self._queue_name, worker_id, lease_seconds)

    def complete(self, task_id: str) -> None:
        self._persistence.complete_task(task_id)

    def fail(self, task_id: str, error: str, retry_at: float | None) -> Task:
        return self._persistence.fail_task(task_id, error, retry_at)
