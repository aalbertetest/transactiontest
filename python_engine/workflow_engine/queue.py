"""
Task queue abstraction backed by SQLite.
"""

from __future__ import annotations

import time
import uuid
from typing import Any, Dict, List, Optional

from .models import Task
from .persistence import SqlitePersistence


class TaskQueue:
    def __init__(self, persistence: SqlitePersistence) -> None:
        self._persistence = persistence

    def enqueue_task(
        self,
        run_id: str,
        task_type: str,
        queue_name: str,
        payload: Dict[str, Any],
        scheduled_at: Optional[float] = None,
        timeout_seconds: Optional[int] = None,
        heartbeat_timeout_seconds: Optional[int] = None,
        max_attempts: int = 1,
    ) -> str:
        task_id = str(uuid.uuid4())
        now = time.time()
        scheduled = scheduled_at if scheduled_at is not None else now
        timeout_at = None
        if timeout_seconds is not None:
            timeout_at = scheduled + timeout_seconds
        task = Task(
            task_id=task_id,
            run_id=run_id,
            task_type=task_type,
            queue_name=queue_name,
            status="PENDING",
            scheduled_at=scheduled,
            leased_until=None,
            completed_at=None,
            attempt=0,
            max_attempts=max_attempts,
            payload=payload,
            last_heartbeat_at=None,
            heartbeat_timeout_seconds=heartbeat_timeout_seconds,
            timeout_at=timeout_at,
            last_error=None,
        )
        self._persistence.insert_task(task)
        return task_id

    def lease_tasks(self, queue_name: str, limit: int, lease_seconds: int) -> List[Task]:
        now = time.time()
        return self._persistence.lease_tasks(queue_name, now, limit, lease_seconds)

    def complete_task(self, task_id: str) -> None:
        self._persistence.update_task_status(task_id, "COMPLETED", completed_at=time.time())

    def fail_task(self, task_id: str, error: str) -> None:
        self._persistence.update_task_status(task_id, "FAILED", completed_at=time.time(), last_error=error)

    def reschedule_task(self, task_id: str, scheduled_at: float) -> None:
        self._persistence.update_task_schedule(task_id, scheduled_at)

    def heartbeat(self, task_id: str) -> None:
        self._persistence.update_task_heartbeat(task_id, time.time())

    def get_task(self, task_id: str) -> Optional[Task]:
        return self._persistence.get_task(task_id)
