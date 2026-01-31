"""
Task Repository Module
======================

This module provides the data access layer for the distributed task scheduler.
It implements the Repository pattern to abstract database operations and
provide a clean API for the scheduler and worker components.

Key Features:
- CRUD operations for tasks, cron jobs, and workers
- Atomic task claiming with SKIP LOCKED
- Leader election support
- Optimistic locking for state transitions

Design Decisions:
1. Repository pattern for clean separation of concerns
2. Async operations for high throughput
3. Optimistic locking to prevent lost updates
4. Parameterized queries to prevent SQL injection
5. Comprehensive logging for debugging
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

from asyncpg import Record

from .database import Database, record_to_dict, records_to_dicts
from ..scheduler.models import (
    Task, TaskStatus, CronJob, CronJobStatus, Worker, WorkerStatus,
    TaskResult, TaskEvent, ConcurrencyPolicy
)

logger = logging.getLogger(__name__)


class TaskRepository:
    """
    Repository for task-related database operations.
    
    This class provides all database operations needed by the scheduler
    and workers, including:
    - Task CRUD (Create, Read, Update, Delete)
    - Task claiming and completion
    - Cron job management
    - Worker registration and heartbeat
    - Leader election
    
    All methods are asynchronous and use the connection pool
    for efficient database access.
    
    Usage:
        repo = TaskRepository(database)
        
        # Create a task
        task = await repo.create_task(
            task_type="send_email",
            payload={"to": "user@example.com"},
            priority=50
        )
        
        # Claim tasks for processing
        tasks = await repo.claim_tasks(worker_id, "default", batch_size=5)
        
        # Complete a task
        await repo.complete_task(task.id, result={"sent": True})
    
    Attributes:
        db: Database connection manager
    """
    
    def __init__(self, db: Database):
        """
        Initialize the repository.
        
        Args:
            db: Database connection manager (must be connected).
        """
        self.db = db
    
    # =========================================================================
    # TASK OPERATIONS
    # =========================================================================
    
    async def create_task(
        self,
        task_type: str,
        payload: Dict[str, Any],
        queue_name: str = "default",
        priority: int = 50,
        scheduled_at: Optional[datetime] = None,
        idempotency_key: Optional[str] = None,
        max_attempts: int = 3,
        timeout_seconds: int = 300,
        parent_task_id: Optional[UUID] = None,
        cron_job_id: Optional[UUID] = None,
    ) -> Task:
        """
        Create a new task.
        
        This method creates a task in either PENDING or QUEUED status
        depending on whether it's scheduled for the future.
        
        If an idempotency_key is provided, the method first checks for
        existing non-terminal tasks with that key and returns the existing
        task instead of creating a duplicate.
        
        Args:
            task_type: Type identifier for routing to handlers.
            payload: Task data as a JSON-serializable dict.
            queue_name: Queue to place the task in.
            priority: Task priority (0-100, higher = first).
            scheduled_at: When to execute (None = immediate).
            idempotency_key: Optional key to prevent duplicates.
            max_attempts: Maximum execution attempts.
            timeout_seconds: Execution timeout per attempt.
            parent_task_id: Parent task for chained execution.
            cron_job_id: Source cron job if scheduled.
            
        Returns:
            The created (or existing, if idempotent) Task.
            
        Raises:
            DatabaseError: If task creation fails.
        """
        # Check for existing task with same idempotency key
        if idempotency_key:
            existing = await self._get_task_by_idempotency_key(idempotency_key)
            if existing:
                logger.debug(
                    f"Returning existing task for idempotency_key={idempotency_key}"
                )
                return existing
        
        # Determine initial status based on scheduling
        now = datetime.utcnow()
        if scheduled_at and scheduled_at > now:
            status = TaskStatus.PENDING
            queued_at = None
        else:
            status = TaskStatus.QUEUED
            queued_at = now
            scheduled_at = None  # Clear scheduled_at for immediate tasks
        
        task_id = uuid4()
        
        # Insert the task
        query = """
            INSERT INTO tasks (
                id, task_type, queue_name, status, priority, payload,
                idempotency_key, scheduled_at, max_attempts, timeout_seconds,
                parent_task_id, cron_job_id, queued_at, created_at, updated_at
            ) VALUES (
                $1, $2, $3, $4, $5, $6,
                $7, $8, $9, $10,
                $11, $12, $13, $14, $14
            )
            RETURNING *
        """
        
        import json
        row = await self.db.fetch_one(
            query,
            task_id,
            task_type,
            queue_name,
            status.value,
            priority,
            json.dumps(payload),
            idempotency_key,
            scheduled_at,
            max_attempts,
            timeout_seconds,
            parent_task_id,
            cron_job_id,
            queued_at,
            now,
        )
        
        task = self._row_to_task(row)
        logger.info(
            f"Created task",
            extra={
                "task_id": str(task.id),
                "task_type": task_type,
                "status": status.value,
                "queue": queue_name,
            }
        )
        
        return task
    
    async def get_task(self, task_id: UUID) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task UUID.
            
        Returns:
            Task if found, None otherwise.
        """
        query = """
            SELECT * FROM tasks
            WHERE id = $1 AND deleted_at IS NULL
        """
        row = await self.db.fetch_one(query, task_id)
        return self._row_to_task(row) if row else None
    
    async def get_tasks(
        self,
        status: Optional[TaskStatus] = None,
        queue_name: Optional[str] = None,
        task_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Task]:
        """
        Get tasks with optional filters.
        
        Args:
            status: Filter by status.
            queue_name: Filter by queue.
            task_type: Filter by task type.
            limit: Maximum number of results.
            offset: Number of results to skip.
            
        Returns:
            List of matching tasks.
        """
        conditions = ["deleted_at IS NULL"]
        params: List[Any] = []
        param_idx = 1
        
        if status:
            conditions.append(f"status = ${param_idx}")
            params.append(status.value)
            param_idx += 1
        
        if queue_name:
            conditions.append(f"queue_name = ${param_idx}")
            params.append(queue_name)
            param_idx += 1
        
        if task_type:
            conditions.append(f"task_type = ${param_idx}")
            params.append(task_type)
            param_idx += 1
        
        params.extend([limit, offset])
        
        query = f"""
            SELECT * FROM tasks
            WHERE {' AND '.join(conditions)}
            ORDER BY created_at DESC
            LIMIT ${param_idx} OFFSET ${param_idx + 1}
        """
        
        rows = await self.db.fetch(query, *params)
        return [self._row_to_task(row) for row in rows]
    
    async def claim_tasks(
        self,
        worker_id: UUID,
        queue_name: str,
        batch_size: int = 1,
        visibility_timeout_seconds: int = 300,
    ) -> List[Task]:
        """
        Claim tasks for a worker.
        
        This method atomically claims up to batch_size tasks from the
        specified queue. It uses SELECT FOR UPDATE SKIP LOCKED to
        prevent contention between multiple workers.
        
        Claimed tasks are moved to ACTIVE status with a visibility
        timeout. If the worker doesn't complete the task before the
        timeout, the task becomes available for other workers.
        
        Args:
            worker_id: ID of the claiming worker.
            queue_name: Queue to claim from.
            batch_size: Maximum tasks to claim.
            visibility_timeout_seconds: How long task stays invisible.
            
        Returns:
            List of claimed tasks (may be empty if queue is empty).
        """
        now = datetime.utcnow()
        visibility_timeout = now + timedelta(seconds=visibility_timeout_seconds)
        
        # Use the database function for atomic claiming
        query = """
            SELECT * FROM claim_tasks($1, $2, $3, $4)
        """
        
        rows = await self.db.fetch(
            query,
            worker_id,
            queue_name,
            batch_size,
            visibility_timeout_seconds,
        )
        
        tasks = [self._row_to_task(row) for row in rows]
        
        if tasks:
            logger.debug(
                f"Claimed {len(tasks)} tasks",
                extra={
                    "worker_id": str(worker_id),
                    "queue": queue_name,
                    "task_ids": [str(t.id) for t in tasks],
                }
            )
        
        return tasks
    
    async def complete_task(
        self,
        task_id: UUID,
        result: Optional[Dict[str, Any]] = None,
        expected_version: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Mark a task as completed successfully.
        
        Args:
            task_id: Task to complete.
            result: Optional result data.
            expected_version: For optimistic locking.
            
        Returns:
            Updated task, or None if not found/version mismatch.
        """
        now = datetime.utcnow()
        
        import json
        result_json = json.dumps(result) if result else None
        
        # Build query with optional version check
        if expected_version is not None:
            query = """
                UPDATE tasks
                SET status = $2,
                    result = $3,
                    completed_at = $4,
                    version = version + 1
                WHERE id = $1
                  AND status = 'ACTIVE'
                  AND version = $5
                  AND deleted_at IS NULL
                RETURNING *
            """
            params = [task_id, TaskStatus.COMPLETED.value, result_json, now, expected_version]
        else:
            query = """
                UPDATE tasks
                SET status = $2,
                    result = $3,
                    completed_at = $4,
                    version = version + 1
                WHERE id = $1
                  AND status = 'ACTIVE'
                  AND deleted_at IS NULL
                RETURNING *
            """
            params = [task_id, TaskStatus.COMPLETED.value, result_json, now]
        
        row = await self.db.fetch_one(query, *params)
        
        if row:
            task = self._row_to_task(row)
            logger.info(
                f"Task completed",
                extra={"task_id": str(task_id), "status": "COMPLETED"}
            )
            return task
        
        logger.warning(
            f"Failed to complete task (not found or version mismatch)",
            extra={"task_id": str(task_id), "expected_version": expected_version}
        )
        return None
    
    async def fail_task(
        self,
        task_id: UUID,
        error_message: str,
        error_details: Optional[Dict[str, Any]] = None,
        expected_version: Optional[int] = None,
    ) -> Optional[Task]:
        """
        Mark a task as failed.
        
        If the task has remaining retry attempts, it will be re-queued
        with an exponential backoff delay. Otherwise, it moves to DEAD.
        
        Args:
            task_id: Task to fail.
            error_message: Human-readable error description.
            error_details: Detailed error info (stack trace, etc.).
            expected_version: For optimistic locking.
            
        Returns:
            Updated task, or None if not found/version mismatch.
        """
        now = datetime.utcnow()
        
        import json
        error_details_json = json.dumps(error_details) if error_details else None
        
        # First, get the current task to check retry status
        task = await self.get_task(task_id)
        if not task:
            return None
        
        # Determine next status and scheduling
        if task.attempt_count < task.max_attempts:
            # Calculate retry delay with exponential backoff
            delay_seconds = task.retry_delay_seconds * (2 ** (task.attempt_count - 1))
            delay_seconds = min(delay_seconds, 3600)  # Cap at 1 hour
            
            new_status = TaskStatus.QUEUED
            scheduled_at = now + timedelta(seconds=delay_seconds)
            completed_at = None
            
            logger.info(
                f"Task failed, scheduling retry",
                extra={
                    "task_id": str(task_id),
                    "attempt": task.attempt_count,
                    "max_attempts": task.max_attempts,
                    "retry_delay": delay_seconds,
                }
            )
        else:
            # Move to dead letter queue
            new_status = TaskStatus.DEAD
            scheduled_at = None
            completed_at = now
            
            logger.warning(
                f"Task moved to dead letter queue",
                extra={
                    "task_id": str(task_id),
                    "attempts": task.attempt_count,
                    "error": error_message,
                }
            )
        
        # Build query with optional version check
        if expected_version is not None:
            query = """
                UPDATE tasks
                SET status = $2,
                    error_message = $3,
                    error_details = $4,
                    scheduled_at = $5,
                    completed_at = $6,
                    worker_id = NULL,
                    visibility_timeout = NULL,
                    version = version + 1
                WHERE id = $1
                  AND status = 'ACTIVE'
                  AND version = $7
                  AND deleted_at IS NULL
                RETURNING *
            """
            params = [
                task_id, new_status.value, error_message, error_details_json,
                scheduled_at, completed_at, expected_version
            ]
        else:
            query = """
                UPDATE tasks
                SET status = $2,
                    error_message = $3,
                    error_details = $4,
                    scheduled_at = $5,
                    completed_at = $6,
                    worker_id = NULL,
                    visibility_timeout = NULL,
                    version = version + 1
                WHERE id = $1
                  AND status = 'ACTIVE'
                  AND deleted_at IS NULL
                RETURNING *
            """
            params = [
                task_id, new_status.value, error_message, error_details_json,
                scheduled_at, completed_at
            ]
        
        row = await self.db.fetch_one(query, *params)
        return self._row_to_task(row) if row else None
    
    async def cancel_task(self, task_id: UUID) -> Optional[Task]:
        """
        Cancel a pending or queued task.
        
        Only tasks in PENDING or QUEUED status can be cancelled.
        ACTIVE tasks must be failed by the worker.
        
        Args:
            task_id: Task to cancel.
            
        Returns:
            Updated task, or None if not found or not cancellable.
        """
        query = """
            UPDATE tasks
            SET status = 'CANCELLED',
                completed_at = $2,
                version = version + 1
            WHERE id = $1
              AND status IN ('PENDING', 'QUEUED')
              AND deleted_at IS NULL
            RETURNING *
        """
        
        row = await self.db.fetch_one(query, task_id, datetime.utcnow())
        
        if row:
            logger.info(f"Task cancelled", extra={"task_id": str(task_id)})
            return self._row_to_task(row)
        
        return None
    
    async def extend_visibility_timeout(
        self,
        task_id: UUID,
        worker_id: UUID,
        extension_seconds: int = 300,
    ) -> bool:
        """
        Extend the visibility timeout for an active task.
        
        Workers should call this periodically for long-running tasks
        to prevent timeout and reassignment.
        
        Args:
            task_id: Task to extend.
            worker_id: Worker holding the task.
            extension_seconds: How much to extend by.
            
        Returns:
            True if extended, False if task not found or not owned.
        """
        new_timeout = datetime.utcnow() + timedelta(seconds=extension_seconds)
        
        query = """
            UPDATE tasks
            SET visibility_timeout = $3,
                version = version + 1
            WHERE id = $1
              AND worker_id = $2
              AND status = 'ACTIVE'
              AND deleted_at IS NULL
            RETURNING id
        """
        
        row = await self.db.fetch_one(query, task_id, worker_id, new_timeout)
        return row is not None
    
    async def promote_pending_tasks(self) -> int:
        """
        Move pending tasks to queued when their scheduled time arrives.
        
        This is called periodically by the scheduler to promote
        tasks that were scheduled for future execution.
        
        Returns:
            Number of tasks promoted.
        """
        result = await self.db.fetch_val("SELECT promote_pending_tasks()")
        logger.debug(f"Promoted {result} pending tasks to queued")
        return result
    
    async def recover_timed_out_tasks(self) -> int:
        """
        Recover tasks that exceeded their visibility timeout.
        
        Tasks that have been ACTIVE longer than their visibility
        timeout are either re-queued (if retries remain) or moved
        to the dead letter queue.
        
        Returns:
            Number of tasks recovered.
        """
        result = await self.db.fetch_val("SELECT recover_timed_out_tasks()")
        if result > 0:
            logger.info(f"Recovered {result} timed-out tasks")
        return result
    
    async def get_queue_stats(self) -> List[Dict[str, Any]]:
        """
        Get queue statistics for monitoring.
        
        Returns:
            List of dictionaries with queue metrics.
        """
        query = """
            SELECT * FROM v_queue_summary
            ORDER BY queue_name, status
        """
        rows = await self.db.fetch(query)
        return records_to_dicts(rows)
    
    async def _get_task_by_idempotency_key(
        self,
        idempotency_key: str
    ) -> Optional[Task]:
        """Get a non-terminal task by idempotency key."""
        query = """
            SELECT * FROM tasks
            WHERE idempotency_key = $1
              AND status NOT IN ('FAILED', 'DEAD', 'CANCELLED')
              AND deleted_at IS NULL
            ORDER BY created_at DESC
            LIMIT 1
        """
        row = await self.db.fetch_one(query, idempotency_key)
        return self._row_to_task(row) if row else None
    
    # =========================================================================
    # CRON JOB OPERATIONS
    # =========================================================================
    
    async def create_cron_job(
        self,
        name: str,
        schedule: str,
        task_type: str,
        task_payload: Optional[Dict[str, Any]] = None,
        queue_name: str = "default",
        priority: int = 50,
        description: Optional[str] = None,
        timezone: str = "UTC",
        max_attempts: int = 3,
        timeout_seconds: int = 300,
        concurrency_policy: ConcurrencyPolicy = ConcurrencyPolicy.ALLOW,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> CronJob:
        """
        Create a new cron job.
        
        Args:
            name: Unique job name.
            schedule: Cron expression (5 fields).
            task_type: Type of task to create.
            task_payload: Payload for created tasks.
            queue_name: Queue for created tasks.
            priority: Priority for created tasks.
            description: Human-readable description.
            timezone: Timezone for schedule evaluation.
            max_attempts: Max attempts for created tasks.
            timeout_seconds: Timeout for created tasks.
            concurrency_policy: How to handle overlapping runs.
            metadata: Arbitrary metadata.
            
        Returns:
            Created CronJob.
        """
        from croniter import croniter
        import json
        
        now = datetime.utcnow()
        
        # Calculate first run time
        cron = croniter(schedule, now)
        next_run_at = cron.get_next(datetime)
        
        job_id = uuid4()
        
        query = """
            INSERT INTO cron_jobs (
                id, name, description, schedule, timezone,
                task_type, task_payload, queue_name, priority,
                max_attempts, timeout_seconds, concurrency_policy,
                next_run_at, metadata, created_at, updated_at
            ) VALUES (
                $1, $2, $3, $4, $5,
                $6, $7, $8, $9,
                $10, $11, $12,
                $13, $14, $15, $15
            )
            RETURNING *
        """
        
        row = await self.db.fetch_one(
            query,
            job_id,
            name,
            description,
            schedule,
            timezone,
            task_type,
            json.dumps(task_payload or {}),
            queue_name,
            priority,
            max_attempts,
            timeout_seconds,
            concurrency_policy.value,
            next_run_at,
            json.dumps(metadata or {}),
            now,
        )
        
        job = self._row_to_cron_job(row)
        logger.info(
            f"Created cron job",
            extra={
                "job_id": str(job.id),
                "name": name,
                "schedule": schedule,
                "next_run": str(next_run_at),
            }
        )
        
        return job
    
    async def get_cron_job(self, job_id: UUID) -> Optional[CronJob]:
        """Get a cron job by ID."""
        query = """
            SELECT * FROM cron_jobs
            WHERE id = $1 AND deleted_at IS NULL
        """
        row = await self.db.fetch_one(query, job_id)
        return self._row_to_cron_job(row) if row else None
    
    async def get_cron_job_by_name(self, name: str) -> Optional[CronJob]:
        """Get a cron job by name."""
        query = """
            SELECT * FROM cron_jobs
            WHERE name = $1 AND deleted_at IS NULL
        """
        row = await self.db.fetch_one(query, name)
        return self._row_to_cron_job(row) if row else None
    
    async def get_due_cron_jobs(self) -> List[CronJob]:
        """
        Get all cron jobs that are due for execution.
        
        Returns:
            List of cron jobs where next_run_at <= now.
        """
        query = """
            SELECT * FROM cron_jobs
            WHERE status = 'ENABLED'
              AND next_run_at <= $1
              AND deleted_at IS NULL
            FOR UPDATE SKIP LOCKED
        """
        rows = await self.db.fetch(query, datetime.utcnow())
        return [self._row_to_cron_job(row) for row in rows]
    
    async def update_cron_job_after_run(
        self,
        job_id: UUID,
        next_run_at: datetime,
        success: bool,
    ) -> Optional[CronJob]:
        """
        Update cron job statistics after a run.
        
        Args:
            job_id: Job to update.
            next_run_at: Next scheduled run time.
            success: Whether the created task succeeded.
            
        Returns:
            Updated job, or None if not found.
        """
        now = datetime.utcnow()
        
        if success:
            query = """
                UPDATE cron_jobs
                SET next_run_at = $2,
                    last_run_at = $3,
                    run_count = run_count + 1,
                    success_count = success_count + 1
                WHERE id = $1 AND deleted_at IS NULL
                RETURNING *
            """
        else:
            query = """
                UPDATE cron_jobs
                SET next_run_at = $2,
                    last_run_at = $3,
                    run_count = run_count + 1,
                    failure_count = failure_count + 1
                WHERE id = $1 AND deleted_at IS NULL
                RETURNING *
            """
        
        row = await self.db.fetch_one(query, job_id, next_run_at, now)
        return self._row_to_cron_job(row) if row else None
    
    async def disable_cron_job(self, job_id: UUID) -> Optional[CronJob]:
        """Disable a cron job."""
        query = """
            UPDATE cron_jobs
            SET status = 'DISABLED'
            WHERE id = $1 AND deleted_at IS NULL
            RETURNING *
        """
        row = await self.db.fetch_one(query, job_id)
        return self._row_to_cron_job(row) if row else None
    
    async def enable_cron_job(self, job_id: UUID) -> Optional[CronJob]:
        """Enable a disabled cron job."""
        from croniter import croniter
        
        now = datetime.utcnow()
        
        # Get current job to recalculate next_run_at
        job = await self.get_cron_job(job_id)
        if not job:
            return None
        
        cron = croniter(job.schedule, now)
        next_run_at = cron.get_next(datetime)
        
        query = """
            UPDATE cron_jobs
            SET status = 'ENABLED',
                next_run_at = $2
            WHERE id = $1 AND deleted_at IS NULL
            RETURNING *
        """
        row = await self.db.fetch_one(query, job_id, next_run_at)
        return self._row_to_cron_job(row) if row else None
    
    # =========================================================================
    # WORKER OPERATIONS
    # =========================================================================
    
    async def register_worker(
        self,
        worker_id: UUID,
        name: str,
        hostname: str,
        pid: int,
        queues: List[str],
        concurrency: int,
        ip_address: Optional[str] = None,
        port: Optional[int] = None,
        version: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Worker:
        """
        Register a worker or update its registration.
        
        Workers call this on startup to announce themselves to the system.
        If a worker with the same ID exists, it's updated instead.
        
        Args:
            worker_id: Unique worker identifier.
            name: Human-readable name (hostname:pid).
            hostname: Machine hostname.
            pid: Process ID.
            queues: List of queues to process.
            concurrency: Maximum concurrent tasks.
            ip_address: Optional IP address.
            port: Optional health check port.
            version: Software version.
            metadata: Arbitrary metadata.
            
        Returns:
            Registered Worker.
        """
        import json
        now = datetime.utcnow()
        
        query = """
            INSERT INTO workers (
                id, name, hostname, ip_address, port, pid,
                queues, concurrency, status, last_heartbeat,
                started_at, version, metadata
            ) VALUES (
                $1, $2, $3, $4, $5, $6,
                $7, $8, 'ACTIVE', $9,
                $9, $10, $11
            )
            ON CONFLICT (id) DO UPDATE SET
                name = $2,
                hostname = $3,
                ip_address = $4,
                port = $5,
                pid = $6,
                queues = $7,
                concurrency = $8,
                status = 'ACTIVE',
                last_heartbeat = $9,
                started_at = $9,
                stopped_at = NULL,
                version = $10,
                metadata = $11
            RETURNING *
        """
        
        row = await self.db.fetch_one(
            query,
            worker_id,
            name,
            hostname,
            ip_address,
            port,
            pid,
            queues,
            concurrency,
            now,
            version,
            json.dumps(metadata or {}),
        )
        
        worker = self._row_to_worker(row)
        logger.info(
            f"Registered worker",
            extra={
                "worker_id": str(worker_id),
                "name": name,
                "queues": queues,
                "concurrency": concurrency,
            }
        )
        
        return worker
    
    async def heartbeat(
        self,
        worker_id: UUID,
        active_task_count: int = 0,
        cpu_usage: Optional[float] = None,
        memory_usage: Optional[float] = None,
    ) -> bool:
        """
        Send a worker heartbeat.
        
        Workers call this periodically to indicate they're alive.
        
        Args:
            worker_id: Worker sending the heartbeat.
            active_task_count: Number of tasks currently processing.
            cpu_usage: CPU utilization percentage.
            memory_usage: Memory utilization percentage.
            
        Returns:
            True if heartbeat recorded, False if worker not found.
        """
        query = """
            UPDATE workers
            SET last_heartbeat = $2,
                active_task_count = $3,
                cpu_usage = $4,
                memory_usage = $5
            WHERE id = $1 AND status = 'ACTIVE'
            RETURNING id
        """
        
        row = await self.db.fetch_one(
            query,
            worker_id,
            datetime.utcnow(),
            active_task_count,
            cpu_usage,
            memory_usage,
        )
        
        return row is not None
    
    async def deregister_worker(self, worker_id: UUID) -> bool:
        """
        Deregister a worker (graceful shutdown).
        
        Args:
            worker_id: Worker to deregister.
            
        Returns:
            True if deregistered, False if not found.
        """
        query = """
            UPDATE workers
            SET status = 'INACTIVE',
                stopped_at = $2
            WHERE id = $1
            RETURNING id
        """
        
        row = await self.db.fetch_one(query, worker_id, datetime.utcnow())
        
        if row:
            logger.info(f"Deregistered worker", extra={"worker_id": str(worker_id)})
        
        return row is not None
    
    async def get_active_workers(self) -> List[Worker]:
        """Get all active workers."""
        query = """
            SELECT * FROM workers
            WHERE status = 'ACTIVE'
            ORDER BY last_heartbeat DESC
        """
        rows = await self.db.fetch(query)
        return [self._row_to_worker(row) for row in rows]
    
    async def get_stale_workers(self, timeout_seconds: int = 30) -> List[Worker]:
        """
        Get workers with stale heartbeats.
        
        Args:
            timeout_seconds: Heartbeat age threshold.
            
        Returns:
            List of workers with old heartbeats.
        """
        cutoff = datetime.utcnow() - timedelta(seconds=timeout_seconds)
        
        query = """
            SELECT * FROM workers
            WHERE status = 'ACTIVE'
              AND last_heartbeat < $1
        """
        rows = await self.db.fetch(query, cutoff)
        return [self._row_to_worker(row) for row in rows]
    
    async def mark_worker_inactive(self, worker_id: UUID) -> int:
        """
        Mark a worker as inactive and fail its tasks.
        
        Args:
            worker_id: Worker to mark inactive.
            
        Returns:
            Number of tasks affected.
        """
        now = datetime.utcnow()
        
        # Mark worker inactive
        await self.db.execute(
            """
            UPDATE workers
            SET status = 'INACTIVE',
                stopped_at = $2
            WHERE id = $1
            """,
            worker_id,
            now,
        )
        
        # Fail active tasks assigned to this worker
        result = await self.db.execute(
            """
            UPDATE tasks
            SET status = 'FAILED',
                error_message = 'Worker heartbeat timeout',
                worker_id = NULL,
                visibility_timeout = NULL,
                version = version + 1
            WHERE worker_id = $1
              AND status = 'ACTIVE'
              AND deleted_at IS NULL
            """,
            worker_id,
        )
        
        # Extract count from "UPDATE N" result
        count = int(result.split()[1]) if result else 0
        
        if count > 0:
            logger.warning(
                f"Failed tasks due to worker timeout",
                extra={"worker_id": str(worker_id), "task_count": count}
            )
        
        return count
    
    # =========================================================================
    # LEADER ELECTION
    # =========================================================================
    
    async def try_acquire_lock(
        self,
        lock_name: str,
        holder_id: UUID,
        holder_name: str,
        ttl_seconds: int = 30,
    ) -> bool:
        """
        Try to acquire a distributed lock.
        
        This is used for leader election. Only one instance can hold
        a lock at a time. The lock automatically expires after TTL.
        
        Args:
            lock_name: Name of the lock to acquire.
            holder_id: Identifier of the lock requester.
            holder_name: Human-readable holder name.
            ttl_seconds: Lock time-to-live in seconds.
            
        Returns:
            True if lock acquired, False if held by another.
        """
        result = await self.db.fetch_val(
            "SELECT try_acquire_lock($1, $2, $3, $4)",
            lock_name,
            holder_id,
            holder_name,
            ttl_seconds,
        )
        return result
    
    async def release_lock(self, lock_name: str, holder_id: UUID) -> bool:
        """
        Release a distributed lock.
        
        Args:
            lock_name: Name of the lock to release.
            holder_id: Identifier of the lock holder.
            
        Returns:
            True if released, False if not held.
        """
        result = await self.db.fetch_val(
            "SELECT release_lock($1, $2)",
            lock_name,
            holder_id,
        )
        return result
    
    async def get_lock_holder(self, lock_name: str) -> Optional[Dict[str, Any]]:
        """
        Get information about who holds a lock.
        
        Args:
            lock_name: Name of the lock to check.
            
        Returns:
            Lock info dict, or None if not held.
        """
        query = """
            SELECT * FROM scheduler_locks
            WHERE lock_name = $1 AND expires_at > NOW()
        """
        row = await self.db.fetch_one(query, lock_name)
        return record_to_dict(row)
    
    # =========================================================================
    # HELPER METHODS
    # =========================================================================
    
    def _row_to_task(self, row: Optional[Record]) -> Optional[Task]:
        """Convert a database row to a Task model."""
        if row is None:
            return None
        
        import json
        
        data = dict(row)
        
        # Handle JSONB fields
        if isinstance(data.get('payload'), str):
            data['payload'] = json.loads(data['payload'])
        if isinstance(data.get('result'), str):
            data['result'] = json.loads(data['result'])
        if isinstance(data.get('error_details'), str):
            data['error_details'] = json.loads(data['error_details'])
        
        # Convert status string to enum
        if isinstance(data.get('status'), str):
            data['status'] = TaskStatus(data['status'])
        
        return Task(**data)
    
    def _row_to_cron_job(self, row: Optional[Record]) -> Optional[CronJob]:
        """Convert a database row to a CronJob model."""
        if row is None:
            return None
        
        import json
        
        data = dict(row)
        
        # Handle JSONB fields
        if isinstance(data.get('task_payload'), str):
            data['task_payload'] = json.loads(data['task_payload'])
        if isinstance(data.get('metadata'), str):
            data['metadata'] = json.loads(data['metadata'])
        
        # Convert status string to enum
        if isinstance(data.get('status'), str):
            data['status'] = CronJobStatus(data['status'])
        if isinstance(data.get('concurrency_policy'), str):
            data['concurrency_policy'] = ConcurrencyPolicy(data['concurrency_policy'])
        
        return CronJob(**data)
    
    def _row_to_worker(self, row: Optional[Record]) -> Optional[Worker]:
        """Convert a database row to a Worker model."""
        if row is None:
            return None
        
        import json
        
        data = dict(row)
        
        # Handle JSONB fields
        if isinstance(data.get('metadata'), str):
            data['metadata'] = json.loads(data['metadata'])
        
        # Convert status string to enum
        if isinstance(data.get('status'), str):
            data['status'] = WorkerStatus(data['status'])
        
        # Handle array types
        if data.get('queues') and not isinstance(data['queues'], list):
            data['queues'] = list(data['queues'])
        
        return Worker(**data)
