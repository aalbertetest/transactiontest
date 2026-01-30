from __future__ import annotations

import json
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from typing import Any, Dict, Iterable, List, Optional, Tuple

from .models import (
    ACTIVITY_STATE_COMPLETED,
    ACTIVITY_STATE_FAILED,
    ACTIVITY_STATE_RETRYING,
    ACTIVITY_STATE_SCHEDULED,
    ACTIVITY_STATE_STARTED,
    ACTIVITY_STATE_TIMED_OUT,
    TIMER_STATE_FIRED,
    TIMER_STATE_SCHEDULED,
    HistoryEvent,
    RetryPolicy,
    ActivityTask,
    WORKFLOW_STATE_RUNNING,
)


class SQLiteStore:
    """
    SQLite-backed persistence layer. This intentionally exposes explicit
    operations to make the write-ahead event log visible and deterministic.
    """

    def __init__(self, db_path: str) -> None:
        self._conn = sqlite3.connect(db_path, check_same_thread=False)
        self._conn.row_factory = sqlite3.Row
        self._lock = threading.Lock()
        self.init_schema()

    @property
    def connection(self):
        return self._conn

    @contextmanager
    def transaction(self):
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute("BEGIN IMMEDIATE")
            try:
                yield cursor
                self._conn.commit()
            except Exception:
                self._conn.rollback()
                raise

    def init_schema(self) -> None:
        with self._lock:
            self._conn.executescript(
                """
                PRAGMA journal_mode=WAL;

                CREATE TABLE IF NOT EXISTS workflow_executions (
                    workflow_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    workflow_type TEXT NOT NULL,
                    state TEXT NOT NULL,
                    input TEXT,
                    result TEXT,
                    error TEXT,
                    task_queue TEXT NOT NULL,
                    started_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL,
                    version INTEGER NOT NULL,
                    PRIMARY KEY (workflow_id, run_id)
                );

                CREATE TABLE IF NOT EXISTS history_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    workflow_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    event_time INTEGER NOT NULL,
                    attributes TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_history_workflow
                    ON history_events (workflow_id, run_id, id);

                CREATE TABLE IF NOT EXISTS activity_tasks (
                    activity_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    activity_name TEXT NOT NULL,
                    input TEXT NOT NULL,
                    state TEXT NOT NULL,
                    scheduled_at INTEGER NOT NULL,
                    started_at INTEGER,
                    completed_at INTEGER,
                    heartbeat_at INTEGER,
                    heartbeat_details TEXT,
                    attempt INTEGER NOT NULL,
                    max_attempts INTEGER NOT NULL,
                    retry_policy TEXT NOT NULL,
                    schedule_to_close_timeout_seconds INTEGER NOT NULL,
                    start_to_close_timeout_seconds INTEGER NOT NULL,
                    heartbeat_timeout_seconds INTEGER NOT NULL,
                    last_failure TEXT
                );

                CREATE INDEX IF NOT EXISTS idx_activity_workflow
                    ON activity_tasks (workflow_id, run_id, state);

                CREATE TABLE IF NOT EXISTS timers (
                    timer_id TEXT PRIMARY KEY,
                    workflow_id TEXT NOT NULL,
                    run_id TEXT NOT NULL,
                    fire_at INTEGER NOT NULL,
                    created_at INTEGER NOT NULL,
                    fired_at INTEGER,
                    state TEXT NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_timers_due
                    ON timers (state, fire_at);

                CREATE TABLE IF NOT EXISTS task_queue (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    queue_name TEXT NOT NULL,
                    task_type TEXT NOT NULL,
                    payload TEXT NOT NULL,
                    visible_at INTEGER NOT NULL,
                    lease_owner TEXT,
                    lease_expires_at INTEGER,
                    attempts INTEGER NOT NULL,
                    max_attempts INTEGER NOT NULL,
                    created_at INTEGER NOT NULL
                );

                CREATE INDEX IF NOT EXISTS idx_task_queue_lookup
                    ON task_queue (queue_name, task_type, visible_at, lease_expires_at);
                """
            )
            self._conn.commit()

    def create_workflow_execution(
        self,
        workflow_id: str,
        workflow_type: str,
        input_payload: Dict[str, Any],
        task_queue: str,
    ) -> str:
        run_id = str(uuid.uuid4())
        now = int(time.time())
        input_json = json.dumps(input_payload)
        with self.transaction() as cursor:
            cursor.execute(
                """
                INSERT INTO workflow_executions (
                    workflow_id, run_id, workflow_type, state, input,
                    result, error, task_queue, started_at, updated_at, version
                ) VALUES (?, ?, ?, ?, ?, NULL, NULL, ?, ?, ?, 1)
                """,
                (
                    workflow_id,
                    run_id,
                    workflow_type,
                    WORKFLOW_STATE_RUNNING,
                    input_json,
                    task_queue,
                    now,
                    now,
                ),
            )
        return run_id

    def get_workflow_execution(self, workflow_id: str, run_id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT workflow_id, run_id, workflow_type, state, input, result,
                       error, task_queue, started_at, updated_at, version
                FROM workflow_executions
                WHERE workflow_id = ? AND run_id = ?
                """,
                (workflow_id, run_id),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def set_workflow_state(
        self,
        workflow_id: str,
        run_id: str,
        state: str,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ) -> None:
        now = int(time.time())
        result_json = json.dumps(result) if result is not None else None
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE workflow_executions
                SET state = ?, result = ?, error = ?, updated_at = ?
                WHERE workflow_id = ? AND run_id = ?
                """,
                (state, result_json, error, now, workflow_id, run_id),
            )
            self._conn.commit()

    def append_event(
        self,
        workflow_id: str,
        run_id: str,
        event_type: str,
        attributes: Dict[str, Any],
    ) -> int:
        now = int(time.time())
        attributes_json = json.dumps(attributes, sort_keys=True)
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                INSERT INTO history_events (
                    workflow_id, run_id, event_type, event_time, attributes
                ) VALUES (?, ?, ?, ?, ?)
                """,
                (workflow_id, run_id, event_type, now, attributes_json),
            )
            self._conn.commit()
            return int(cursor.lastrowid)

    def get_history(self, workflow_id: str, run_id: str) -> List[HistoryEvent]:
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT id, event_type, event_time, attributes
                FROM history_events
                WHERE workflow_id = ? AND run_id = ?
                ORDER BY id ASC
                """,
                (workflow_id, run_id),
            )
            rows = cursor.fetchall()
        history: List[HistoryEvent] = []
        for row in rows:
            history.append(
                HistoryEvent(
                    event_id=int(row["id"]),
                    event_type=str(row["event_type"]),
                    event_time=int(row["event_time"]),
                    attributes=json.loads(row["attributes"]),
                )
            )
        return history

    def create_activity_task(
        self,
        workflow_id: str,
        run_id: str,
        activity_name: str,
        input_payload: Dict[str, Any],
        retry_policy: RetryPolicy,
        schedule_to_close_timeout_seconds: int,
        start_to_close_timeout_seconds: int,
        heartbeat_timeout_seconds: int,
    ) -> str:
        activity_id = str(uuid.uuid4())
        now = int(time.time())
        with self.transaction() as cursor:
            cursor.execute(
                """
                INSERT INTO activity_tasks (
                    activity_id, workflow_id, run_id, activity_name, input, state,
                    scheduled_at, started_at, completed_at, heartbeat_at,
                    heartbeat_details, attempt, max_attempts, retry_policy,
                    schedule_to_close_timeout_seconds, start_to_close_timeout_seconds,
                    heartbeat_timeout_seconds, last_failure
                ) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, 0, ?, ?, ?, ?, ?, NULL)
                """,
                (
                    activity_id,
                    workflow_id,
                    run_id,
                    activity_name,
                    json.dumps(input_payload),
                    ACTIVITY_STATE_SCHEDULED,
                    now,
                    retry_policy.max_attempts,
                    json.dumps(retry_policy.to_dict()),
                    schedule_to_close_timeout_seconds,
                    start_to_close_timeout_seconds,
                    heartbeat_timeout_seconds,
                ),
            )
        return activity_id

    def get_activity_task(self, activity_id: str) -> Optional[ActivityTask]:
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT * FROM activity_tasks WHERE activity_id = ?
                """,
                (activity_id,),
            )
            row = cursor.fetchone()
        if row is None:
            return None
        retry_policy = RetryPolicy.from_dict(json.loads(row["retry_policy"]))
        heartbeat_details = json.loads(row["heartbeat_details"]) if row["heartbeat_details"] else None
        return ActivityTask(
            activity_id=row["activity_id"],
            workflow_id=row["workflow_id"],
            run_id=row["run_id"],
            activity_name=row["activity_name"],
            input=json.loads(row["input"]),
            state=row["state"],
            scheduled_at=row["scheduled_at"],
            started_at=row["started_at"],
            completed_at=row["completed_at"],
            heartbeat_at=row["heartbeat_at"],
            heartbeat_details=heartbeat_details,
            attempt=row["attempt"],
            max_attempts=row["max_attempts"],
            retry_policy=retry_policy,
            schedule_to_close_timeout_seconds=row["schedule_to_close_timeout_seconds"],
            start_to_close_timeout_seconds=row["start_to_close_timeout_seconds"],
            heartbeat_timeout_seconds=row["heartbeat_timeout_seconds"],
            last_failure=row["last_failure"],
        )

    def record_activity_started(self, activity_id: str, worker_id: str) -> None:
        now = int(time.time())
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE activity_tasks
                SET state = ?, started_at = ?, heartbeat_at = ?, heartbeat_details = ?
                WHERE activity_id = ?
                """,
                (ACTIVITY_STATE_STARTED, now, now, json.dumps({"worker_id": worker_id}), activity_id),
            )
            self._conn.commit()

    def record_activity_heartbeat(self, activity_id: str, details: Dict[str, Any]) -> None:
        now = int(time.time())
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE activity_tasks
                SET heartbeat_at = ?, heartbeat_details = ?
                WHERE activity_id = ?
                """,
                (now, json.dumps(details), activity_id),
            )
            self._conn.commit()

    def record_activity_completed(self, activity_id: str, result: Dict[str, Any]) -> None:
        now = int(time.time())
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE activity_tasks
                SET state = ?, completed_at = ?, last_failure = NULL
                WHERE activity_id = ?
                """,
                (ACTIVITY_STATE_COMPLETED, now, activity_id),
            )
            self._conn.commit()

    def record_activity_failed(self, activity_id: str, error: str) -> None:
        now = int(time.time())
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE activity_tasks
                SET state = ?, completed_at = ?, last_failure = ?
                WHERE activity_id = ?
                """,
                (ACTIVITY_STATE_FAILED, now, error, activity_id),
            )
            self._conn.commit()

    def record_activity_retrying(self, activity_id: str, error: str) -> None:
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE activity_tasks
                SET state = ?, last_failure = ?, attempt = attempt + 1
                WHERE activity_id = ?
                """,
                (ACTIVITY_STATE_RETRYING, error, activity_id),
            )
            self._conn.commit()

    def record_activity_timed_out(self, activity_id: str, error: str) -> None:
        now = int(time.time())
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE activity_tasks
                SET state = ?, completed_at = ?, last_failure = ?
                WHERE activity_id = ?
                """,
                (ACTIVITY_STATE_TIMED_OUT, now, error, activity_id),
            )
            self._conn.commit()

    def list_activity_tasks_by_state(self, states: Iterable[str]) -> List[ActivityTask]:
        placeholders = ",".join("?" for _ in states)
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                f"""
                SELECT * FROM activity_tasks WHERE state IN ({placeholders})
                """,
                tuple(states),
            )
            rows = cursor.fetchall()
        tasks: List[ActivityTask] = []
        for row in rows:
            retry_policy = RetryPolicy.from_dict(json.loads(row["retry_policy"]))
            heartbeat_details = json.loads(row["heartbeat_details"]) if row["heartbeat_details"] else None
            tasks.append(
                ActivityTask(
                    activity_id=row["activity_id"],
                    workflow_id=row["workflow_id"],
                    run_id=row["run_id"],
                    activity_name=row["activity_name"],
                    input=json.loads(row["input"]),
                    state=row["state"],
                    scheduled_at=row["scheduled_at"],
                    started_at=row["started_at"],
                    completed_at=row["completed_at"],
                    heartbeat_at=row["heartbeat_at"],
                    heartbeat_details=heartbeat_details,
                    attempt=row["attempt"],
                    max_attempts=row["max_attempts"],
                    retry_policy=retry_policy,
                    schedule_to_close_timeout_seconds=row["schedule_to_close_timeout_seconds"],
                    start_to_close_timeout_seconds=row["start_to_close_timeout_seconds"],
                    heartbeat_timeout_seconds=row["heartbeat_timeout_seconds"],
                    last_failure=row["last_failure"],
                )
            )
        return tasks

    def create_timer(self, workflow_id: str, run_id: str, fire_at: int) -> str:
        timer_id = str(uuid.uuid4())
        now = int(time.time())
        with self.transaction() as cursor:
            cursor.execute(
                """
                INSERT INTO timers (
                    timer_id, workflow_id, run_id, fire_at, created_at, fired_at, state
                ) VALUES (?, ?, ?, ?, ?, NULL, ?)
                """,
                (timer_id, workflow_id, run_id, fire_at, now, TIMER_STATE_SCHEDULED),
            )
        return timer_id

    def list_due_timers(self, now: int) -> List[Dict[str, Any]]:
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                SELECT timer_id, workflow_id, run_id, fire_at
                FROM timers
                WHERE state = ? AND fire_at <= ?
                ORDER BY fire_at ASC
                """,
                (TIMER_STATE_SCHEDULED, now),
            )
            rows = cursor.fetchall()
        timers: List[Dict[str, Any]] = []
        for row in rows:
            timers.append(
                {
                    "timer_id": row["timer_id"],
                    "workflow_id": row["workflow_id"],
                    "run_id": row["run_id"],
                    "fire_at": row["fire_at"],
                }
            )
        return timers

    def mark_timer_fired(self, timer_id: str) -> None:
        now = int(time.time())
        with self._lock:
            cursor = self._conn.cursor()
            cursor.execute(
                """
                UPDATE timers
                SET state = ?, fired_at = ?
                WHERE timer_id = ?
                """,
                (TIMER_STATE_FIRED, now, timer_id),
            )
            self._conn.commit()

