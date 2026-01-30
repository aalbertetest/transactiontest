from __future__ import annotations

import json
import threading
import time
from typing import Any, Dict, Optional

from .metrics import MetricsRegistry
from .models import QueueTask


class TaskQueue:
    """
    Abstract task queue interface.
    """

    def enqueue(
        self,
        queue_name: str,
        task_type: str,
        payload: Dict[str, Any],
        visible_at: Optional[int] = None,
        max_attempts: int = 1,
    ) -> int:
        raise NotImplementedError()

    def poll(
        self,
        queue_name: str,
        task_type: str,
        lease_duration_seconds: int,
        worker_id: str,
    ) -> Optional[QueueTask]:
        raise NotImplementedError()

    def ack(self, task_id: int) -> None:
        raise NotImplementedError()

    def nack(self, task_id: int, delay_seconds: int) -> None:
        raise NotImplementedError()


class DBTaskQueue(TaskQueue):
    """
    SQLite-backed task queue with basic leasing.
    """

    def __init__(self, connection, metrics: Optional[MetricsRegistry] = None) -> None:
        self._conn = connection
        self._lock = threading.Lock()
        self._metrics = metrics

    def enqueue(
        self,
        queue_name: str,
        task_type: str,
        payload: Dict[str, Any],
        visible_at: Optional[int] = None,
        max_attempts: int = 1,
    ) -> int:
        if visible_at is None:
            visible_at = int(time.time())
        payload_json = json.dumps(payload)
        now = int(time.time())
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                INSERT INTO task_queue (
                    queue_name, task_type, payload, visible_at,
                    lease_owner, lease_expires_at, attempts, max_attempts, created_at
                ) VALUES (?, ?, ?, ?, NULL, NULL, 0, ?, ?)
                """,
                (queue_name, task_type, payload_json, visible_at, max_attempts, now),
            )
            self._conn.commit()
            task_id = int(cursor.lastrowid)
        if self._metrics:
            self._metrics.increment("queue.enqueue")
        return task_id

    def poll(
        self,
        queue_name: str,
        task_type: str,
        lease_duration_seconds: int,
        worker_id: str,
    ) -> Optional[QueueTask]:
        now = int(time.time())
        lease_expires_at = now + lease_duration_seconds
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")
            cursor.execute(
                """
                SELECT id FROM task_queue
                WHERE queue_name = ?
                  AND task_type = ?
                  AND visible_at <= ?
                  AND (lease_expires_at IS NULL OR lease_expires_at <= ?)
                  AND attempts < max_attempts
                ORDER BY id
                LIMIT 1
                """,
                (queue_name, task_type, now, now),
            )
            row = cursor.fetchone()
            if row is None:
                self._conn.commit()
                return None
            task_id = int(row[0])
            cursor.execute(
                """
                UPDATE task_queue
                SET lease_owner = ?, lease_expires_at = ?, attempts = attempts + 1
                WHERE id = ?
                """,
                (worker_id, lease_expires_at, task_id),
            )
            cursor.execute(
                """
                SELECT id, queue_name, task_type, payload, visible_at,
                       lease_owner, lease_expires_at, attempts, max_attempts
                FROM task_queue
                WHERE id = ?
                """,
                (task_id,),
            )
            result = cursor.fetchone()
            self._conn.commit()
        if result is None:
            return None
        payload = json.loads(result[3])
        task = QueueTask(
            id=int(result[0]),
            queue_name=str(result[1]),
            task_type=str(result[2]),
            payload=payload,
            visible_at=int(result[4]),
            lease_owner=result[5],
            lease_expires_at=result[6],
            attempts=int(result[7]),
            max_attempts=int(result[8]),
        )
        if self._metrics:
            self._metrics.increment("queue.poll")
        return task

    def ack(self, task_id: int) -> None:
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("DELETE FROM task_queue WHERE id = ?", (task_id,))
            self._conn.commit()
        if self._metrics:
            self._metrics.increment("queue.ack")

    def nack(self, task_id: int, delay_seconds: int) -> None:
        visible_at = int(time.time()) + delay_seconds
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE task_queue
                SET visible_at = ?, lease_owner = NULL, lease_expires_at = NULL
                WHERE id = ?
                """,
                (visible_at, task_id),
            )
            self._conn.commit()
        if self._metrics:
            self._metrics.increment("queue.nack")

