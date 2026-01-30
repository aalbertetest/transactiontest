"""
SQLite persistence layer for the workflow engine.

This module implements the durable storage for workflow executions,
event history, tasks, and activity heartbeats.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
import uuid
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .types import Event, Task, TaskState, TaskType, WorkflowExecution, WorkflowState


def _now() -> float:
    return time.time()


def _json_dumps(value: Dict[str, Any]) -> str:
    # Sort keys to guarantee deterministic JSON encoding.
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def _json_loads(value: str) -> Dict[str, Any]:
    if not value:
        return {}
    return json.loads(value)


class SQLitePersistence:
    def __init__(self, db_path: str) -> None:
        # check_same_thread=False allows multi-threaded access with explicit locking.
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self._init_pragmas()
        self.init_schema()

    def _init_pragmas(self) -> None:
        with self._conn:
            self._conn.execute("PRAGMA journal_mode=WAL")
            self._conn.execute("PRAGMA synchronous=NORMAL")
            self._conn.execute("PRAGMA foreign_keys=ON")
            self._conn.execute("PRAGMA busy_timeout=5000")

    def init_schema(self) -> None:
        with self._conn:
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS workflow_executions (
                    workflow_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    state TEXT NOT NULL,
                    workflow_type TEXT NOT NULL,
                    input_json TEXT NOT NULL,
                    started_at REAL NOT NULL,
                    completed_at REAL,
                    last_event_id INTEGER NOT NULL,
                    version INTEGER NOT NULL,
                    PRIMARY KEY (workflow_id, run_id)
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS workflow_events (
                    workflow_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    event_id INTEGER NOT NULL,
                    event_type TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    attributes_json TEXT NOT NULL,
                    PRIMARY KEY (workflow_id, run_id, event_id)
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    queue TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    workflow_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    state TEXT NOT NULL,
                    attempts INTEGER NOT NULL,
                    max_attempts INTEGER NOT NULL,
                    not_before REAL NOT NULL,
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL,
                    lease_expires_at REAL,
                    worker_id TEXT,
                    timeout_seconds INTEGER
                )
                """
            )
            self._conn.execute(
                """
                CREATE TABLE IF NOT EXISTS activity_heartbeats (
                    task_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    last_heartbeat REAL NOT NULL,
                    details_json TEXT NOT NULL
                )
                """
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_queue_state ON tasks(queue, state, not_before)"
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_lease ON tasks(state, lease_expires_at)"
            )
            self._conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_tasks_type_state ON tasks(task_type, state, not_before)"
            )

    def create_workflow_execution(
        self,
        workflow_id: str,
        run_id: str,
        workflow_type: str,
        input_data: Dict[str, Any],
    ) -> WorkflowExecution:
        with self._lock, self._conn:
            now = _now()
            self._conn.execute(
                """
                INSERT INTO workflow_executions
                (workflow_id, run_id, state, workflow_type, input_json, started_at, completed_at, last_event_id, version)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    workflow_id,
                    run_id,
                    WorkflowState.RUNNING.value,
                    workflow_type,
                    _json_dumps(input_data),
                    now,
                    None,
                    0,
                    1,
                ),
            )
            return WorkflowExecution(
                workflow_id=workflow_id,
                run_id=run_id,
                state=WorkflowState.RUNNING,
                workflow_type=workflow_type,
                input=input_data,
                started_at=now,
                completed_at=None,
                last_event_id=0,
                version=1,
            )

    def get_workflow_execution(self, workflow_id: str, run_id: str) -> WorkflowExecution:
        row = self._conn.execute(
            """
            SELECT * FROM workflow_executions WHERE workflow_id = ? AND run_id = ?
            """,
            (workflow_id, run_id),
        ).fetchone()
        if not row:
            raise KeyError(f"Workflow execution not found: {workflow_id}/{run_id}")
        return WorkflowExecution(
            workflow_id=row["workflow_id"],
            run_id=row["run_id"],
            state=WorkflowState(row["state"]),
            workflow_type=row["workflow_type"],
            input=_json_loads(row["input_json"]),
            started_at=row["started_at"],
            completed_at=row["completed_at"],
            last_event_id=row["last_event_id"],
            version=row["version"],
        )

    def update_workflow_state(
        self,
        workflow_id: str,
        run_id: str,
        new_state: WorkflowState,
        completed_at: Optional[float],
    ) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                """
                UPDATE workflow_executions
                SET state = ?, completed_at = ?
                WHERE workflow_id = ? AND run_id = ?
                """,
                (new_state.value, completed_at, workflow_id, run_id),
            )

    def append_event(
        self,
        workflow_id: str,
        run_id: str,
        event_type: str,
        attributes: Dict[str, Any],
    ) -> Event:
        with self._lock, self._conn:
            row = self._conn.execute(
                """
                SELECT last_event_id FROM workflow_executions
                WHERE workflow_id = ? AND run_id = ?
                """,
                (workflow_id, run_id),
            ).fetchone()
            if not row:
                raise KeyError(f"Workflow execution not found: {workflow_id}/{run_id}")
            next_event_id = row["last_event_id"] + 1
            timestamp = _now()
            self._conn.execute(
                """
                INSERT INTO workflow_events
                (workflow_id, run_id, event_id, event_type, timestamp, attributes_json)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    workflow_id,
                    run_id,
                    next_event_id,
                    event_type,
                    timestamp,
                    _json_dumps(attributes),
                ),
            )
            self._conn.execute(
                """
                UPDATE workflow_executions
                SET last_event_id = ?
                WHERE workflow_id = ? AND run_id = ?
                """,
                (next_event_id, workflow_id, run_id),
            )
            return Event(
                workflow_id=workflow_id,
                run_id=run_id,
                event_id=next_event_id,
                event_type=event_type,
                timestamp=timestamp,
                attributes=attributes,
            )

    def list_events(self, workflow_id: str, run_id: str) -> List[Event]:
        rows = self._conn.execute(
            """
            SELECT * FROM workflow_events
            WHERE workflow_id = ? AND run_id = ?
            ORDER BY event_id ASC
            """,
            (workflow_id, run_id),
        ).fetchall()
        return [
            Event(
                workflow_id=row["workflow_id"],
                run_id=row["run_id"],
                event_id=row["event_id"],
                event_type=row["event_type"],
                timestamp=row["timestamp"],
                attributes=_json_loads(row["attributes_json"]),
            )
            for row in rows
        ]

    def create_task(
        self,
        queue: str,
        task_type: TaskType,
        workflow_id: str,
        run_id: str,
        payload: Dict[str, Any],
        max_attempts: int,
        not_before: Optional[float] = None,
        timeout_seconds: Optional[int] = None,
    ) -> Task:
        with self._lock, self._conn:
            now = _now()
            task_id = str(uuid.uuid4())
            self._conn.execute(
                """
                INSERT INTO tasks
                (task_id, queue, task_type, workflow_id, run_id, payload_json, state, attempts,
                 max_attempts, not_before, created_at, updated_at, lease_expires_at, worker_id, timeout_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task_id,
                    queue,
                    task_type.value,
                    workflow_id,
                    run_id,
                    _json_dumps(payload),
                    TaskState.PENDING.value,
                    0,
                    max_attempts,
                    not_before if not_before is not None else now,
                    now,
                    now,
                    None,
                    None,
                    timeout_seconds,
                ),
            )
            return Task(
                task_id=task_id,
                queue=queue,
                task_type=task_type,
                workflow_id=workflow_id,
                run_id=run_id,
                payload=payload,
                state=TaskState.PENDING,
                attempts=0,
                max_attempts=max_attempts,
                not_before=not_before if not_before is not None else now,
                created_at=now,
                updated_at=now,
                lease_expires_at=None,
                worker_id=None,
                timeout_seconds=timeout_seconds,
            )

    def poll_task(
        self,
        queue: str,
        worker_id: str,
        lease_seconds: int,
    ) -> Optional[Task]:
        with self._lock, self._conn:
            now = _now()
            row = self._conn.execute(
                """
                SELECT * FROM tasks
                WHERE queue = ? AND state = ? AND not_before <= ?
                ORDER BY created_at ASC
                LIMIT 1
                """,
                (queue, TaskState.PENDING.value, now),
            ).fetchone()
            if not row:
                return None
            lease_expires_at = now + lease_seconds
            self._conn.execute(
                """
                UPDATE tasks
                SET state = ?, updated_at = ?, lease_expires_at = ?, worker_id = ?
                WHERE task_id = ?
                """,
                (
                    TaskState.IN_PROGRESS.value,
                    now,
                    lease_expires_at,
                    worker_id,
                    row["task_id"],
                ),
            )
            return Task(
                task_id=row["task_id"],
                queue=row["queue"],
                task_type=TaskType(row["task_type"]),
                workflow_id=row["workflow_id"],
                run_id=row["run_id"],
                payload=_json_loads(row["payload_json"]),
                state=TaskState.IN_PROGRESS,
                attempts=row["attempts"],
                max_attempts=row["max_attempts"],
                not_before=row["not_before"],
                created_at=row["created_at"],
                updated_at=now,
                lease_expires_at=lease_expires_at,
                worker_id=worker_id,
                timeout_seconds=row["timeout_seconds"],
            )

    def complete_task(self, task_id: str) -> None:
        with self._lock, self._conn:
            self._conn.execute(
                """
                UPDATE tasks
                SET state = ?, updated_at = ?, lease_expires_at = NULL
                WHERE task_id = ?
                """,
                (TaskState.DONE.value, _now(), task_id),
            )

    def fail_task(self, task_id: str, error: str, retry_at: Optional[float]) -> Task:
        with self._lock, self._conn:
            row = self._conn.execute(
                """
                SELECT * FROM tasks WHERE task_id = ?
                """,
                (task_id,),
            ).fetchone()
            if not row:
                raise KeyError(f"Task not found: {task_id}")
            attempts = row["attempts"] + 1
            state = TaskState.PENDING.value if attempts < row["max_attempts"] else TaskState.FAILED.value
            not_before = retry_at if retry_at is not None else _now()
            self._conn.execute(
                """
                UPDATE tasks
                SET state = ?, attempts = ?, not_before = ?, updated_at = ?, lease_expires_at = NULL
                WHERE task_id = ?
                """,
                (state, attempts, not_before, _now(), task_id),
            )
            return Task(
                task_id=row["task_id"],
                queue=row["queue"],
                task_type=TaskType(row["task_type"]),
                workflow_id=row["workflow_id"],
                run_id=row["run_id"],
                payload=_json_loads(row["payload_json"]),
                state=TaskState(state),
                attempts=attempts,
                max_attempts=row["max_attempts"],
                not_before=not_before,
                created_at=row["created_at"],
                updated_at=_now(),
                lease_expires_at=None,
                worker_id=None,
                timeout_seconds=row["timeout_seconds"],
            )

    def heartbeat_task(self, task_id: str, details: Dict[str, Any], lease_seconds: int) -> None:
        with self._lock, self._conn:
            now = _now()
            lease_expires_at = now + lease_seconds
            self._conn.execute(
                """
                UPDATE tasks
                SET lease_expires_at = ?, updated_at = ?
                WHERE task_id = ?
                """,
                (lease_expires_at, now, task_id),
            )
            self._conn.execute(
                """
                INSERT INTO activity_heartbeats (task_id, workflow_id, run_id, last_heartbeat, details_json)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(task_id) DO UPDATE SET last_heartbeat = excluded.last_heartbeat, details_json = excluded.details_json
                """,
                (task_id, details.get("workflow_id"), details.get("run_id"), now, _json_dumps(details)),
            )

    def get_task(self, task_id: str) -> Task:
        row = self._conn.execute(
            """
            SELECT * FROM tasks WHERE task_id = ?
            """,
            (task_id,),
        ).fetchone()
        if not row:
            raise KeyError(f"Task not found: {task_id}")
        return Task(
            task_id=row["task_id"],
            queue=row["queue"],
            task_type=TaskType(row["task_type"]),
            workflow_id=row["workflow_id"],
            run_id=row["run_id"],
            payload=_json_loads(row["payload_json"]),
            state=TaskState(row["state"]),
            attempts=row["attempts"],
            max_attempts=row["max_attempts"],
            not_before=row["not_before"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            lease_expires_at=row["lease_expires_at"],
            worker_id=row["worker_id"],
            timeout_seconds=row["timeout_seconds"],
        )

    def list_due_timers(self) -> List[Task]:
        now = _now()
        rows = self._conn.execute(
            """
            SELECT * FROM tasks
            WHERE task_type = ? AND state = ? AND not_before <= ?
            ORDER BY not_before ASC
            """,
            (TaskType.TIMER_TASK.value, TaskState.PENDING.value, now),
        ).fetchall()
        return [self._row_to_task(row) for row in rows]

    def list_expired_leases(self) -> List[Task]:
        now = _now()
        rows = self._conn.execute(
            """
            SELECT * FROM tasks
            WHERE state = ? AND lease_expires_at IS NOT NULL AND lease_expires_at <= ?
            ORDER BY lease_expires_at ASC
            """,
            (TaskState.IN_PROGRESS.value, now),
        ).fetchall()
        return [self._row_to_task(row) for row in rows]

    def _row_to_task(self, row: sqlite3.Row) -> Task:
        return Task(
            task_id=row["task_id"],
            queue=row["queue"],
            task_type=TaskType(row["task_type"]),
            workflow_id=row["workflow_id"],
            run_id=row["run_id"],
            payload=_json_loads(row["payload_json"]),
            state=TaskState(row["state"]),
            attempts=row["attempts"],
            max_attempts=row["max_attempts"],
            not_before=row["not_before"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
            lease_expires_at=row["lease_expires_at"],
            worker_id=row["worker_id"],
            timeout_seconds=row["timeout_seconds"],
        )
