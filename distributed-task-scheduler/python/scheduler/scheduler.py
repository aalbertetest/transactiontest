"""
Task Scheduler Service
======================

This module implements the main scheduler service for the distributed
task scheduler. The scheduler is responsible for:

1. Leader election among multiple scheduler instances
2. Cron job evaluation and task creation
3. Pending task promotion to queued
4. Visibility timeout recovery
5. Worker health monitoring

Design Decisions:
1. Leader election ensures only one scheduler processes cron jobs
2. Tick-based cron evaluation for predictable timing
3. Graceful shutdown with task completion
4. Health check endpoint for load balancer probes
"""

import asyncio
import logging
import os
import signal
import socket
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import UUID, uuid4

from croniter import croniter

from ..config.settings import Settings, SchedulerSettings
from ..persistence.database import Database
from ..persistence.repository import TaskRepository
from ..queue.task_queue import TaskQueue
from .models import Task, CronJob, CronJobStatus, ConcurrencyPolicy

logger = logging.getLogger(__name__)

# Lock name for leader election
CRON_LEADER_LOCK = "cron_leader"


class TaskScheduler:
    """
    Main scheduler service for the distributed task scheduler.
    
    The scheduler runs several background loops:
    
    1. **Leader Election Loop**: Attempts to acquire/renew the leader lock.
       Only the leader runs cron evaluation and some maintenance tasks.
    
    2. **Cron Evaluation Loop**: Evaluates cron jobs and creates task
       instances when they're due. Only runs on the leader.
    
    3. **Pending Promotion Loop**: Moves PENDING tasks to QUEUED when
       their scheduled time arrives.
    
    4. **Timeout Recovery Loop**: Recovers tasks that exceeded their
       visibility timeout (worker may have crashed).
    
    5. **Health Check Loop**: Monitors worker health and marks stale
       workers as inactive.
    
    Usage:
        settings = Settings.from_yaml('config.yaml')
        scheduler = TaskScheduler(settings)
        
        # Start the scheduler
        await scheduler.start()
        
        # Submit tasks programmatically
        task = await scheduler.submit(
            task_type="send_email",
            payload={"to": "user@example.com"}
        )
        
        # Create cron jobs
        job = await scheduler.create_cron_job(
            name="daily_report",
            schedule="0 9 * * *",
            task_type="generate_report",
            payload={"format": "pdf"}
        )
        
        # Stop the scheduler
        await scheduler.stop()
    
    Attributes:
        settings: Application settings
        instance_id: Unique identifier for this scheduler instance
        is_leader: Whether this instance is the current leader
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize the scheduler.
        
        Args:
            settings: Application settings.
        """
        self.settings = settings
        self._scheduler_settings = settings.scheduler
        
        # Generate unique instance ID
        self.instance_id = UUID(self._scheduler_settings.instance_id) if self._scheduler_settings.instance_id else uuid4()
        self.instance_name = f"{socket.gethostname()}:{os.getpid()}"
        
        # Initialize components (lazily connected)
        self._db: Optional[Database] = None
        self._repository: Optional[TaskRepository] = None
        self._queue: Optional[TaskQueue] = None
        
        # State
        self._running = False
        self._is_leader = False
        self._tasks: List[asyncio.Task] = []
        
        # Statistics
        self._stats = {
            "tasks_created": 0,
            "cron_runs": 0,
            "tasks_promoted": 0,
            "tasks_recovered": 0,
            "leader_acquisitions": 0,
        }
        
        logger.info(
            f"Scheduler initialized",
            extra={
                "instance_id": str(self.instance_id),
                "instance_name": self.instance_name,
            }
        )
    
    @classmethod
    def from_config(cls, config_path: str) -> "TaskScheduler":
        """
        Create a scheduler from a configuration file.
        
        Args:
            config_path: Path to YAML configuration file.
            
        Returns:
            Configured TaskScheduler instance.
        """
        settings = Settings.from_yaml(config_path)
        return cls(settings)
    
    @property
    def is_leader(self) -> bool:
        """Check if this instance is the current leader."""
        return self._is_leader
    
    @property
    def is_running(self) -> bool:
        """Check if scheduler is running."""
        return self._running
    
    @property
    def queue(self) -> TaskQueue:
        """Get the task queue (must be started first)."""
        if self._queue is None:
            raise RuntimeError("Scheduler not started. Call start() first.")
        return self._queue
    
    # =========================================================================
    # LIFECYCLE
    # =========================================================================
    
    async def start(self) -> None:
        """
        Start the scheduler service.
        
        This connects to the database and starts all background loops.
        The method blocks until stop() is called.
        """
        if self._running:
            logger.warning("Scheduler already running")
            return
        
        logger.info("Starting scheduler...")
        
        # Connect to database
        self._db = Database(self.settings.database)
        await self._db.connect()
        
        # Initialize repository and queue
        self._repository = TaskRepository(self._db)
        self._queue = TaskQueue(self._repository)
        
        self._running = True
        
        # Set up signal handlers for graceful shutdown
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
        
        # Start background tasks
        self._tasks = [
            asyncio.create_task(self._leader_election_loop(), name="leader_election"),
            asyncio.create_task(self._cron_evaluation_loop(), name="cron_evaluation"),
            asyncio.create_task(self._pending_promotion_loop(), name="pending_promotion"),
            asyncio.create_task(self._timeout_recovery_loop(), name="timeout_recovery"),
            asyncio.create_task(self._health_check_loop(), name="health_check"),
        ]
        
        logger.info("Scheduler started")
        
        # Wait for all tasks to complete (they run forever until stopped)
        try:
            await asyncio.gather(*self._tasks)
        except asyncio.CancelledError:
            logger.info("Scheduler tasks cancelled")
    
    async def stop(self) -> None:
        """
        Stop the scheduler gracefully.
        
        This releases the leader lock, cancels background tasks,
        and closes the database connection.
        """
        if not self._running:
            return
        
        logger.info("Stopping scheduler...")
        self._running = False
        
        # Release leader lock if held
        if self._is_leader and self._repository:
            try:
                await self._repository.release_lock(CRON_LEADER_LOCK, self.instance_id)
                logger.info("Released leader lock")
            except Exception as e:
                logger.warning(f"Failed to release leader lock: {e}")
        
        # Cancel all background tasks
        for task in self._tasks:
            task.cancel()
        
        # Wait for cancellation
        if self._tasks:
            await asyncio.gather(*self._tasks, return_exceptions=True)
        
        # Close database connection
        if self._db:
            await self._db.disconnect()
        
        logger.info("Scheduler stopped")
    
    # =========================================================================
    # TASK OPERATIONS
    # =========================================================================
    
    async def submit(
        self,
        task_type: str,
        payload: Dict[str, Any],
        queue_name: str = "default",
        priority: int = 50,
        scheduled_at: Optional[datetime] = None,
        delay_seconds: Optional[float] = None,
        idempotency_key: Optional[str] = None,
        max_attempts: int = 3,
        timeout_seconds: int = 300,
    ) -> Task:
        """
        Submit a new task.
        
        See TaskQueue.submit() for full documentation.
        
        Returns:
            The created task.
        """
        task = await self.queue.submit(
            task_type=task_type,
            payload=payload,
            queue_name=queue_name,
            priority=priority,
            scheduled_at=scheduled_at,
            delay_seconds=delay_seconds,
            idempotency_key=idempotency_key,
            max_attempts=max_attempts,
            timeout_seconds=timeout_seconds,
        )
        
        self._stats["tasks_created"] += 1
        return task
    
    async def get_task(self, task_id: UUID) -> Optional[Task]:
        """Get a task by ID."""
        return await self.queue.get(task_id)
    
    async def cancel_task(self, task_id: UUID) -> Task:
        """Cancel a pending or queued task."""
        return await self.queue.cancel(task_id)
    
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
            name: Unique job name for identification.
            schedule: Cron expression (5 fields: minute hour day month weekday).
                      Examples:
                      - "0 * * * *" - Every hour at minute 0
                      - "0 9 * * 1-5" - 9 AM on weekdays
                      - "*/5 * * * *" - Every 5 minutes
            task_type: Type of task to create when triggered.
            task_payload: Payload for created tasks.
            queue_name: Queue for created tasks.
            priority: Priority for created tasks (0-100).
            description: Human-readable description.
            timezone: Timezone for schedule evaluation (e.g., "America/New_York").
            max_attempts: Maximum attempts for created tasks.
            timeout_seconds: Timeout for created tasks.
            concurrency_policy: How to handle overlapping runs:
                - ALLOW: Create new task regardless
                - FORBID: Skip if previous is still running
                - REPLACE: Cancel previous and start new
            metadata: Arbitrary metadata for the job.
            
        Returns:
            Created CronJob.
            
        Raises:
            ValueError: If schedule is invalid.
        """
        # Validate cron expression
        try:
            croniter(schedule)
        except Exception as e:
            raise ValueError(f"Invalid cron expression '{schedule}': {e}")
        
        return await self._repository.create_cron_job(
            name=name,
            schedule=schedule,
            task_type=task_type,
            task_payload=task_payload,
            queue_name=queue_name,
            priority=priority,
            description=description,
            timezone=timezone,
            max_attempts=max_attempts,
            timeout_seconds=timeout_seconds,
            concurrency_policy=concurrency_policy,
            metadata=metadata,
        )
    
    async def get_cron_job(self, job_id: UUID) -> Optional[CronJob]:
        """Get a cron job by ID."""
        return await self._repository.get_cron_job(job_id)
    
    async def get_cron_job_by_name(self, name: str) -> Optional[CronJob]:
        """Get a cron job by name."""
        return await self._repository.get_cron_job_by_name(name)
    
    async def disable_cron_job(self, job_id: UUID) -> Optional[CronJob]:
        """Disable a cron job."""
        return await self._repository.disable_cron_job(job_id)
    
    async def enable_cron_job(self, job_id: UUID) -> Optional[CronJob]:
        """Enable a disabled cron job."""
        return await self._repository.enable_cron_job(job_id)
    
    # =========================================================================
    # BACKGROUND LOOPS
    # =========================================================================
    
    async def _leader_election_loop(self) -> None:
        """
        Background loop for leader election.
        
        Continuously attempts to acquire or renew the leader lock.
        The TTL-based lock automatically expires if not renewed,
        allowing another instance to take over if the leader crashes.
        """
        ttl = self._scheduler_settings.leader_election_ttl
        interval = self._scheduler_settings.leader_renewal_interval
        
        while self._running:
            try:
                # Try to acquire/renew the leader lock
                acquired = await self._repository.try_acquire_lock(
                    lock_name=CRON_LEADER_LOCK,
                    holder_id=self.instance_id,
                    holder_name=self.instance_name,
                    ttl_seconds=ttl,
                )
                
                if acquired and not self._is_leader:
                    # Just became leader
                    self._is_leader = True
                    self._stats["leader_acquisitions"] += 1
                    logger.info("Acquired leader lock - now the active scheduler")
                    
                elif not acquired and self._is_leader:
                    # Lost leadership
                    self._is_leader = False
                    logger.warning("Lost leader lock - now standby")
                    
            except Exception as e:
                logger.error(f"Leader election error: {e}")
                self._is_leader = False
            
            await asyncio.sleep(interval)
    
    async def _cron_evaluation_loop(self) -> None:
        """
        Background loop for cron job evaluation.
        
        Only runs on the leader. Checks all enabled cron jobs and
        creates task instances for any that are due.
        """
        tick_interval = self._scheduler_settings.cron_tick_interval
        
        while self._running:
            try:
                if self._is_leader:
                    await self._evaluate_cron_jobs()
            except Exception as e:
                logger.error(f"Cron evaluation error: {e}")
            
            await asyncio.sleep(tick_interval)
    
    async def _evaluate_cron_jobs(self) -> None:
        """
        Evaluate all cron jobs and create tasks for due jobs.
        """
        due_jobs = await self._repository.get_due_cron_jobs()
        
        for job in due_jobs:
            try:
                await self._trigger_cron_job(job)
            except Exception as e:
                logger.error(
                    f"Failed to trigger cron job: {e}",
                    extra={"job_id": str(job.id), "job_name": job.name}
                )
    
    async def _trigger_cron_job(self, job: CronJob) -> None:
        """
        Trigger a cron job by creating a task instance.
        
        Handles concurrency policy checks and updates job statistics.
        """
        now = datetime.utcnow()
        
        # Handle concurrency policy
        if job.concurrency_policy == ConcurrencyPolicy.FORBID:
            # Check if previous task is still running
            active_tasks = await self._repository.get_tasks(
                task_type=job.task_type,
                status=TaskStatus.ACTIVE,
                limit=1,
            )
            if active_tasks:
                logger.info(
                    f"Skipping cron job due to FORBID policy - previous still active",
                    extra={"job_name": job.name}
                )
                # Still update next_run_at
                cron = croniter(job.schedule, now)
                next_run = cron.get_next(datetime)
                await self._repository.update_cron_job_after_run(
                    job_id=job.id,
                    next_run_at=next_run,
                    success=True,  # Not a failure, just skipped
                )
                return
        
        elif job.concurrency_policy == ConcurrencyPolicy.REPLACE:
            # Cancel any active tasks from this job
            active_tasks = await self._repository.get_tasks(
                task_type=job.task_type,
                cron_job_id=job.id,
                status=TaskStatus.ACTIVE,
            )
            for task in active_tasks:
                try:
                    await self._queue.cancel(task.id)
                except Exception:
                    pass  # Task may have completed already
        
        # Create the task
        task = await self._repository.create_task(
            task_type=job.task_type,
            payload=job.task_payload,
            queue_name=job.queue_name,
            priority=job.priority,
            max_attempts=job.max_attempts,
            timeout_seconds=job.timeout_seconds,
            cron_job_id=job.id,
        )
        
        # Calculate next run time
        cron = croniter(job.schedule, now)
        next_run = cron.get_next(datetime)
        
        # Update job statistics
        await self._repository.update_cron_job_after_run(
            job_id=job.id,
            next_run_at=next_run,
            success=True,
        )
        
        self._stats["cron_runs"] += 1
        
        logger.info(
            f"Triggered cron job",
            extra={
                "job_name": job.name,
                "task_id": str(task.id),
                "next_run": str(next_run),
            }
        )
    
    async def _pending_promotion_loop(self) -> None:
        """
        Background loop for promoting pending tasks.
        
        Moves tasks from PENDING to QUEUED when their scheduled
        time arrives.
        """
        interval = self._scheduler_settings.pending_promotion_interval
        
        while self._running:
            try:
                promoted = await self._repository.promote_pending_tasks()
                if promoted > 0:
                    self._stats["tasks_promoted"] += promoted
                    logger.debug(f"Promoted {promoted} pending tasks to queued")
            except Exception as e:
                logger.error(f"Pending promotion error: {e}")
            
            await asyncio.sleep(interval)
    
    async def _timeout_recovery_loop(self) -> None:
        """
        Background loop for recovering timed-out tasks.
        
        Finds tasks that have been ACTIVE longer than their visibility
        timeout and either re-queues them or moves them to dead letter.
        """
        interval = self._scheduler_settings.timeout_recovery_interval
        
        while self._running:
            try:
                recovered = await self._repository.recover_timed_out_tasks()
                if recovered > 0:
                    self._stats["tasks_recovered"] += recovered
            except Exception as e:
                logger.error(f"Timeout recovery error: {e}")
            
            await asyncio.sleep(interval)
    
    async def _health_check_loop(self) -> None:
        """
        Background loop for worker health monitoring.
        
        Only runs on the leader. Finds workers with stale heartbeats
        and marks them as inactive.
        """
        interval = self._scheduler_settings.health_check_interval
        timeout = self.settings.worker.heartbeat_interval * 3  # 3x heartbeat = stale
        
        while self._running:
            try:
                if self._is_leader:
                    stale_workers = await self._repository.get_stale_workers(timeout)
                    
                    for worker in stale_workers:
                        logger.warning(
                            f"Worker heartbeat timeout",
                            extra={
                                "worker_id": str(worker.id),
                                "worker_name": worker.name,
                                "last_heartbeat": str(worker.last_heartbeat),
                            }
                        )
                        
                        tasks_affected = await self._repository.mark_worker_inactive(worker.id)
                        
                        if tasks_affected > 0:
                            logger.warning(
                                f"Failed {tasks_affected} tasks from inactive worker",
                                extra={"worker_id": str(worker.id)}
                            )
            except Exception as e:
                logger.error(f"Health check error: {e}")
            
            await asyncio.sleep(interval)
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get scheduler statistics.
        
        Returns:
            Dictionary with scheduler metrics.
        """
        return {
            "instance_id": str(self.instance_id),
            "instance_name": self.instance_name,
            "is_leader": self._is_leader,
            "is_running": self._running,
            **self._stats,
        }
    
    async def get_health(self) -> Dict[str, Any]:
        """
        Get scheduler health status.
        
        Returns:
            Health check result with component status.
        """
        health = {
            "status": "healthy",
            "instance_id": str(self.instance_id),
            "is_leader": self._is_leader,
            "components": {},
        }
        
        # Check database
        try:
            if self._db:
                db_healthy = await self._db.health_check()
                health["components"]["database"] = {
                    "status": "healthy" if db_healthy else "unhealthy"
                }
                if not db_healthy:
                    health["status"] = "unhealthy"
            else:
                health["components"]["database"] = {"status": "not_connected"}
                health["status"] = "unhealthy"
        except Exception as e:
            health["components"]["database"] = {"status": "error", "error": str(e)}
            health["status"] = "unhealthy"
        
        return health


# Entry point for running scheduler directly
async def main():
    """Main entry point for the scheduler."""
    import sys
    
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Load configuration
    config_path = os.environ.get("DTS_CONFIG_PATH", "config.yaml")
    
    if len(sys.argv) > 1 and sys.argv[1].startswith("--config"):
        if "=" in sys.argv[1]:
            config_path = sys.argv[1].split("=")[1]
        elif len(sys.argv) > 2:
            config_path = sys.argv[2]
    
    try:
        settings = Settings.from_yaml(config_path)
    except FileNotFoundError:
        logger.info("Config file not found, using defaults")
        settings = Settings()
    
    # Create and start scheduler
    scheduler = TaskScheduler(settings)
    await scheduler.start()


if __name__ == "__main__":
    asyncio.run(main())
