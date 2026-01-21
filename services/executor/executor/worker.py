import json
import logging
import time
from datetime import timedelta
from typing import Dict, List

import psycopg2
from psycopg2.extras import RealDictCursor
from prometheus_client import Counter, Gauge

from executor.config import (
    EXECUTOR_ID,
    POLL_INTERVAL_MS,
    LOCK_TTL_SECONDS,
    BATCH_SIZE,
    SHARD_COUNT,
    SHARDS,
)
from executor.db import get_connection
from executor.tasks import execute_step, parse_payload

logger = logging.getLogger("executor")

TASKS_CLAIMED = Counter("executor_tasks_claimed_total", "Tasks claimed by executor")
TASKS_SUCCEEDED = Counter("executor_tasks_succeeded_total", "Tasks succeeded")
TASKS_FAILED = Counter("executor_tasks_failed_total", "Tasks failed")
QUEUE_DEPTH = Gauge("executor_queue_depth", "Queued tasks visible to executor")


def parse_shards() -> List[int]:
    if not SHARDS:
        return list(range(SHARD_COUNT))
    shards = []
    for token in SHARDS.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            shards.append(int(token))
        except ValueError:
            continue
    return shards


def run_forever() -> None:
    shards = parse_shards()
    if not shards:
        raise RuntimeError("no shards configured for executor")

    while True:
        try:
            with get_connection() as conn:
                requeue_stale_tasks(conn)
                queue_depth(conn, shards)
                tasks = claim_tasks(conn, shards)
                if not tasks:
                    time.sleep(POLL_INTERVAL_MS / 1000)
                    continue
                for task in tasks:
                    execute_task(conn, task)
        except psycopg2.Error as exc:
            logger.error("database error: %s", exc)
            time.sleep(1)


def requeue_stale_tasks(conn) -> None:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE tasks
            SET status = 'queued', locked_by = NULL, locked_at = NULL
            WHERE status = 'running'
              AND locked_at < now() - (%s || ' seconds')::interval
            """,
            (LOCK_TTL_SECONDS,),
        )
        conn.commit()


def queue_depth(conn, shards: List[int]) -> None:
    with conn.cursor() as cursor:
        cursor.execute(
            """
            SELECT COUNT(*) AS count
            FROM tasks
            WHERE status = 'queued'
              AND run_after <= now()
              AND shard_id = ANY(%s)
            """,
            (shards,),
        )
        result = cursor.fetchone()
        QUEUE_DEPTH.set(result[0] if result else 0)


def claim_tasks(conn, shards: List[int]) -> List[Dict]:
    # Claim tasks with SELECT FOR UPDATE SKIP LOCKED to safely distribute work
    # across multiple executors without double execution.
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("BEGIN")
        cursor.execute(
            """
            SELECT id, run_id, step_id, attempt, max_attempts, payload
            FROM tasks
            WHERE status = 'queued'
              AND run_after <= now()
              AND shard_id = ANY(%s)
            ORDER BY run_after, created_at
            FOR UPDATE SKIP LOCKED
            LIMIT %s
            """,
            (shards, BATCH_SIZE),
        )
        rows = cursor.fetchall()
        if not rows:
            cursor.execute("COMMIT")
            return []

        task_ids = [row["id"] for row in rows]
        cursor.execute(
            """
            UPDATE tasks
            SET status = 'running',
                attempt = attempt + 1,
                locked_by = %s,
                locked_at = now(),
                updated_at = now()
            WHERE id = ANY(%s)
            """,
            (EXECUTOR_ID, task_ids),
        )

        for row in rows:
            cursor.execute(
                """
                INSERT INTO task_attempts (task_id, attempt, status)
                VALUES (%s, %s, 'running')
                """,
                (row["id"], row["attempt"] + 1),
            )

        cursor.execute("COMMIT")
        TASKS_CLAIMED.inc(len(rows))
        return rows


def execute_task(conn, task: Dict) -> None:
    # Execute a single task and update task/task_attempt tables transactionally.
    task_id = task["id"]
    attempt = task["attempt"] + 1
    max_attempts = task["max_attempts"]
    payload = parse_payload(task["payload"])

    result = execute_step(payload)

    with conn.cursor() as cursor:
        if result.status == "succeeded":
            cursor.execute(
                """
                UPDATE tasks
                SET status = 'succeeded',
                    updated_at = now(),
                    locked_by = NULL,
                    locked_at = NULL
                WHERE id = %s
                """,
                (task_id,),
            )
            cursor.execute(
                """
                UPDATE task_attempts
                SET status = 'succeeded', finished_at = now(), output = %s
                WHERE task_id = %s AND attempt = %s
                """,
                (json.dumps(result.output), task_id, attempt),
            )
            TASKS_SUCCEEDED.inc()
        else:
            if attempt < max_attempts:
                backoff_seconds = min(60, 2 ** attempt)
                cursor.execute(
                    """
                    UPDATE tasks
                    SET status = 'queued',
                        run_after = now() + (%s || ' seconds')::interval,
                        updated_at = now(),
                        locked_by = NULL,
                        locked_at = NULL
                    WHERE id = %s
                    """,
                    (backoff_seconds, task_id),
                )
            else:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET status = 'failed',
                        updated_at = now(),
                        locked_by = NULL,
                        locked_at = NULL
                    WHERE id = %s
                    """,
                    (task_id,),
                )
            cursor.execute(
                """
                UPDATE task_attempts
                SET status = 'failed', finished_at = now(), output = %s, error = %s
                WHERE task_id = %s AND attempt = %s
                """,
                (json.dumps(result.output), result.error or "unknown error", task_id, attempt),
            )
            TASKS_FAILED.inc()
        conn.commit()
