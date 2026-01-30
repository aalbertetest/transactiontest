"""
SQLite persistence layer with explicit schemas.
"""

from __future__ import annotations

import json
import sqlite3
import threading
import time
from typing import Any, Dict, Iterable, List, Optional

from .models import HistoryEvent, Task


SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS workflows (
        workflow_id TEXT PRIMARY KEY,
        workflow_type TEXT NOT NULL,
        status TEXT NOT NULL,
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL,
        current_run_id TEXT NOT NULL,
        run_timeout_seconds INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS workflow_runs (
        run_id TEXT PRIMARY KEY,
        workflow_id TEXT NOT NULL,
        workflow_type TEXT NOT NULL,
        status TEXT NOT NULL,
        state TEXT NOT NULL,
        state_data TEXT NOT NULL,
        created_at REAL NOT NULL,
        updated_at REAL NOT NULL,
        last_event_id INTEGER DEFAULT 0,
        last_heartbeat_at REAL,
        workflow_task_timeout_seconds INTEGER NOT NULL,
        run_timeout_seconds INTEGER NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS history_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT NOT NULL,
        event_type TEXT NOT NULL,
        timestamp REAL NOT NULL,
        attributes TEXT NOT NULL
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS tasks (
        task_id TEXT PRIMARY KEY,
        run_id TEXT NOT NULL,
        task_type TEXT NOT NULL,
        queue_name TEXT NOT NULL,
        status TEXT NOT NULL,
        scheduled_at REAL NOT NULL,
        leased_until REAL,
        completed_at REAL,
        attempt INTEGER NOT NULL,
        max_attempts INTEGER NOT NULL,
        payload TEXT NOT NULL,
        last_heartbeat_at REAL,
        heartbeat_timeout_seconds INTEGER,
        timeout_at REAL,
        last_error TEXT
    )
    """,
    "CREATE INDEX IF NOT EXISTS idx_tasks_queue ON tasks(queue_name, status, scheduled_at)",
    "CREATE INDEX IF NOT EXISTS idx_events_run ON history_events(run_id, id)",
    "CREATE INDEX IF NOT EXISTS idx_runs_status ON workflow_runs(status, updated_at)",
]


class SqlitePersistence:
    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._conn = sqlite3.connect(self._db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self.initialize()

    def initialize(self) -> None:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("PRAGMA journal_mode=WAL")
            for statement in SCHEMA_STATEMENTS:
                cur.execute(statement)
            self._conn.commit()

    def create_run(
        self,
        workflow_id: str,
        workflow_type: str,
        run_id: str,
        state: str,
        state_data: Dict[str, Any],
        run_timeout_seconds: int,
        workflow_task_timeout_seconds: int,
        input_payload: Dict[str, Any],
    ) -> None:
        now = time.time()
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                INSERT INTO workflows (workflow_id, workflow_type, status, created_at, updated_at, current_run_id, run_timeout_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (workflow_id, workflow_type, "RUNNING", now, now, run_id, run_timeout_seconds),
            )
            cur.execute(
                """
                INSERT INTO workflow_runs (run_id, workflow_id, workflow_type, status, state, state_data, created_at, updated_at, workflow_task_timeout_seconds, run_timeout_seconds)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    run_id,
                    workflow_id,
                    workflow_type,
                    "RUNNING",
                    state,
                    json.dumps(state_data),
                    now,
                    now,
                    workflow_task_timeout_seconds,
                    run_timeout_seconds,
                ),
            )
            cur.execute(
                """
                INSERT INTO history_events (run_id, event_type, timestamp, attributes)
                VALUES (?, ?, ?, ?)
                """,
                (run_id, "WorkflowStarted", now, json.dumps({"input": input_payload})),
            )
            self._conn.commit()

    def append_event(self, run_id: str, event_type: str, attributes: Dict[str, Any]) -> HistoryEvent:
        now = time.time()
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                INSERT INTO history_events (run_id, event_type, timestamp, attributes)
                VALUES (?, ?, ?, ?)
                """,
                (run_id, event_type, now, json.dumps(attributes)),
            )
            event_id = cur.lastrowid
            cur.execute(
                "UPDATE workflow_runs SET last_event_id=?, updated_at=? WHERE run_id=?",
                (event_id, now, run_id),
            )
            self._conn.commit()
        return HistoryEvent(event_id=event_id, run_id=run_id, event_type=event_type, timestamp=now, attributes=attributes)

    def list_events(self, run_id: str) -> List[HistoryEvent]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                "SELECT * FROM history_events WHERE run_id=? ORDER BY id ASC",
                (run_id,),
            )
            rows = cur.fetchall()
        return [HistoryEvent.from_row(row) for row in rows]

    def get_run(self, run_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("SELECT * FROM workflow_runs WHERE run_id=?", (run_id,))
            row = cur.fetchone()
        if not row:
            return None
        return {
            "run_id": row["run_id"],
            "workflow_id": row["workflow_id"],
            "workflow_type": row["workflow_type"],
            "status": row["status"],
            "state": row["state"],
            "state_data": json.loads(row["state_data"] or "{}"),
            "created_at": row["created_at"],
            "updated_at": row["updated_at"],
            "workflow_task_timeout_seconds": row["workflow_task_timeout_seconds"],
            "run_timeout_seconds": row["run_timeout_seconds"],
        }

    def update_run_state(self, run_id: str, state: str, state_data: Dict[str, Any], status: str) -> None:
        now = time.time()
        with self._lock:
            self._conn.execute(
                """
                UPDATE workflow_runs
                SET state=?, state_data=?, status=?, updated_at=?
                WHERE run_id=?
                """,
                (state, json.dumps(state_data), status, now, run_id),
            )
            self._conn.execute(
                "UPDATE workflows SET status=?, updated_at=? WHERE current_run_id=?",
                (status, now, run_id),
            )
            self._conn.commit()

    def insert_task(self, task: Task) -> None:
        with self._lock:
            self._conn.execute(
                """
                INSERT INTO tasks (task_id, run_id, task_type, queue_name, status, scheduled_at, leased_until, completed_at,
                                   attempt, max_attempts, payload, last_heartbeat_at, heartbeat_timeout_seconds, timeout_at, last_error)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    task.task_id,
                    task.run_id,
                    task.task_type,
                    task.queue_name,
                    task.status,
                    task.scheduled_at,
                    task.leased_until,
                    task.completed_at,
                    task.attempt,
                    task.max_attempts,
                    json.dumps(task.payload),
                    task.last_heartbeat_at,
                    task.heartbeat_timeout_seconds,
                    task.timeout_at,
                    task.last_error,
                ),
            )
            self._conn.commit()

    def update_task_status(self, task_id: str, status: str, completed_at: Optional[float] = None, last_error: Optional[str] = None) -> None:
        with self._lock:
            self._conn.execute(
                """
                UPDATE tasks SET status=?, completed_at=?, last_error=?
                WHERE task_id=?
                """,
                (status, completed_at, last_error, task_id),
            )
            self._conn.commit()

    def update_task_lease(self, task_id: str, leased_until: float, attempt: int) -> None:
        with self._lock:
            self._conn.execute(
                """
                UPDATE tasks SET status='LEASED', leased_until=?, attempt=?, last_heartbeat_at=?
                WHERE task_id=?
                """,
                (leased_until, attempt, time.time(), task_id),
            )
            self._conn.commit()

    def update_task_schedule(self, task_id: str, scheduled_at: float) -> None:
        with self._lock:
            self._conn.execute(
                """
                UPDATE tasks SET status='PENDING', scheduled_at=?, leased_until=NULL
                WHERE task_id=?
                """,
                (scheduled_at, task_id),
            )
            self._conn.commit()

    def update_task_heartbeat(self, task_id: str, heartbeat_at: float) -> None:
        with self._lock:
            self._conn.execute(
                """
                UPDATE tasks SET last_heartbeat_at=?
                WHERE task_id=?
                """,
                (heartbeat_at, task_id),
            )
            self._conn.commit()

    def get_task(self, task_id: str) -> Optional[Task]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("SELECT * FROM tasks WHERE task_id=?", (task_id,))
            row = cur.fetchone()
        if not row:
            return None
        return Task.from_row(row)

    def list_tasks(self, task_ids: Iterable[str]) -> List[Task]:
        ids = list(task_ids)
        if not ids:
            return []
        placeholders = ",".join("?" for _ in ids)
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(f"SELECT * FROM tasks WHERE task_id IN ({placeholders})", ids)
            rows = cur.fetchall()
        return [Task.from_row(row) for row in rows]

    def find_candidate_tasks(self, queue_name: str, now: float, limit: int) -> List[Task]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                SELECT * FROM tasks
                WHERE queue_name=?
                AND (
                    (status='PENDING' AND scheduled_at<=?)
                    OR (status='LEASED' AND leased_until<=?)
                )
                AND (timeout_at IS NULL OR timeout_at>=?)
                ORDER BY scheduled_at ASC
                LIMIT ?
                """,
                (queue_name, now, now, now, limit),
            )
            rows = cur.fetchall()
        return [Task.from_row(row) for row in rows]

    def lease_tasks(self, queue_name: str, now: float, limit: int, lease_seconds: int) -> List[Task]:
        leased: List[Task] = []
        with self._lock:
            cur = self._conn.cursor()
            cur.execute("BEGIN IMMEDIATE")
            cur.execute(
                """
                SELECT * FROM tasks
                WHERE queue_name=?
                AND (
                    (status='PENDING' AND scheduled_at<=?)
                    OR (status='LEASED' AND leased_until<=?)
                )
                AND (timeout_at IS NULL OR timeout_at>=?)
                ORDER BY scheduled_at ASC
                LIMIT ?
                """,
                (queue_name, now, now, now, limit),
            )
            rows = cur.fetchall()
            for row in rows:
                task = Task.from_row(row)
                if task.attempt >= task.max_attempts:
                    cur.execute(
                        "UPDATE tasks SET status='FAILED', last_error=? WHERE task_id=?",
                        ("max_attempts_exceeded", task.task_id),
                    )
                    continue
                attempt = task.attempt + 1
                leased_until = now + lease_seconds
                cur.execute(
                    """
                    UPDATE tasks
                    SET status='LEASED', leased_until=?, attempt=?, last_heartbeat_at=?
                    WHERE task_id=?
                    """,
                    (leased_until, attempt, now, task.task_id),
                )
                task.status = "LEASED"
                task.leased_until = leased_until
                task.attempt = attempt
                task.last_heartbeat_at = now
                leased.append(task)
            self._conn.commit()
        return leased

    def find_heartbeat_expired_tasks(self, now: float) -> List[Task]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                SELECT * FROM tasks
                WHERE status='LEASED'
                AND heartbeat_timeout_seconds IS NOT NULL
                AND last_heartbeat_at IS NOT NULL
                AND last_heartbeat_at + heartbeat_timeout_seconds <= ?
                """,
                (now,),
            )
            rows = cur.fetchall()
        return [Task.from_row(row) for row in rows]

    def find_timeout_expired_tasks(self, now: float) -> List[Task]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                SELECT * FROM tasks
                WHERE status='LEASED'
                AND timeout_at IS NOT NULL
                AND timeout_at <= ?
                """,
                (now,),
            )
            rows = cur.fetchall()
        return [Task.from_row(row) for row in rows]

    def find_run_timeouts(self, now: float) -> List[Dict[str, Any]]:
        with self._lock:
            cur = self._conn.cursor()
            cur.execute(
                """
                SELECT * FROM workflow_runs
                WHERE status='RUNNING'
                AND created_at + run_timeout_seconds <= ?
                """,
                (now,),
            )
            rows = cur.fetchall()
        return [
            {
                "run_id": row["run_id"],
                "workflow_id": row["workflow_id"],
                "workflow_type": row["workflow_type"],
                "state": row["state"],
                "state_data": json.loads(row["state_data"] or "{}"),
            }
            for row in rows
        ]
