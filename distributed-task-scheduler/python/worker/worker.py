"""
Worker Process Module
=====================

This module implements the worker process that executes tasks from the
distributed task scheduler. Workers:

1. Register themselves with the system on startup
2. Poll queues for available tasks
3. Execute tasks using registered handlers
4. Send heartbeats to indicate liveness
5. Report results back to the scheduler

Design Decisions:
1. Async task execution with configurable concurrency
2. Graceful shutdown with task completion
3. Automatic heartbeat and visibility timeout extension
4. Handler isolation with exception capture
"""

import asyncio
import logging
import os
import signal
import socket
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from typing import Any, Callable, Coroutine, Dict, List, Optional, Set, Union
from uuid import UUID, uuid4

from ..config.settings import Settings, WorkerSettings
from ..persistence.database import Database
from ..persistence.repository import TaskRepository
from ..queue.task_queue import TaskQueue
from ..scheduler.models import Task, TaskStatus

logger = logging.getLogger(__name__)

# Type for task handlers - can be sync or async
TaskHandler = Union[
    Callable[[Task], Any],
    Callable[[Task], Coroutine[Any, Any, Any]]
]


class WorkerError(Exception):
    """Base exception for worker errors."""
    pass


class HandlerNotFoundError(WorkerError):
    """Raised when no handler is registered for a task type."""
    pass


class TaskExecutionError(WorkerError):
    """Raised when task execution fails."""
    def __init__(self, message: str, error_type: str, traceback: str):
        super().__init__(message)
        self.error_type = error_type
        self.traceback = traceback


class Worker:
    """
    Task worker that processes tasks from the queue.
    
    The worker runs a continuous loop that:
    1. Polls configured queues for available tasks
    2. Claims tasks atomically
    3. Executes tasks using registered handlers
    4. Reports results back to the persistence layer
    5. Sends periodic heartbeats
    
    Workers can process multiple tasks concurrently up to the
    configured concurrency limit. Each task runs in its own
    asyncio task with isolation.
    
    Usage:
        # Create worker
        settings = Settings.from_yaml('config.yaml')
        worker = Worker(settings)
        
        # Register task handlers
        @worker.task("send_email")
        async def send_email(task: Task):
            email = task.payload["to"]
            # ... send email ...
            return {"sent": True}
        
        @worker.task("process_payment")
        def process_payment(task: Task):  # Sync handler also supported
            order_id = task.payload["order_id"]
            # ... process payment ...
            return {"success": True}
        
        # Start worker
        await worker.start()
    
    Attributes:
        settings: Application settings
        worker_id: Unique worker identifier
        worker_name: Human-readable name (hostname:pid)
        queues: List of queues this worker processes
        concurrency: Maximum concurrent tasks
    """
    
    def __init__(self, settings: Settings):
        """
        Initialize the worker.
        
        Args:
            settings: Application settings.
        """
        self.settings = settings
        self._worker_settings = settings.worker
        
        # Generate unique worker ID
        worker_id_str = self._worker_settings.worker_id
        self.worker_id = UUID(worker_id_str) if worker_id_str else uuid4()
        self.worker_name = f"{socket.gethostname()}:{os.getpid()}"
        
        # Configuration
        self.queues = self._worker_settings.queues
        self.concurrency = self._worker_settings.concurrency
        
        # Components (lazily initialized)
        self._db: Optional[Database] = None
        self._repository: Optional[TaskRepository] = None
        self._queue: Optional[TaskQueue] = None
        
        # Task handlers
        self._handlers: Dict[str, TaskHandler] = {}
        
        # State
        self._running = False
        self._shutting_down = False
        self._active_tasks: Dict[UUID, asyncio.Task] = {}
        self._semaphore: Optional[asyncio.Semaphore] = None
        
        # Background task references
        self._poll_task: Optional[asyncio.Task] = None
        self._heartbeat_task: Optional[asyncio.Task] = None
        
        # Thread pool for sync handlers
        self._executor = ThreadPoolExecutor(max_workers=self.concurrency)
        
        # Statistics
        self._stats = {
            "tasks_processed": 0,
            "tasks_succeeded": 0,
            "tasks_failed": 0,
            "tasks_retried": 0,
        }
        
        logger.info(
            f"Worker initialized",
            extra={
                "worker_id": str(self.worker_id),
                "worker_name": self.worker_name,
                "queues": self.queues,
                "concurrency": self.concurrency,
            }
        )
    
    @classmethod
    def from_config(cls, config_path: str) -> "Worker":
        """
        Create a worker from a configuration file.
        
        Args:
            config_path: Path to YAML configuration file.
            
        Returns:
            Configured Worker instance.
        """
        settings = Settings.from_yaml(config_path)
        return cls(settings)
    
    # =========================================================================
    # HANDLER REGISTRATION
    # =========================================================================
    
    def register_handler(self, task_type: str, handler: TaskHandler) -> None:
        """
        Register a handler for a task type.
        
        Args:
            task_type: Task type identifier.
            handler: Callable that processes tasks of this type.
                     Can be sync or async.
        """
        self._handlers[task_type] = handler
        logger.info(f"Registered handler for task type: {task_type}")
    
    def task(self, task_type: str) -> Callable[[TaskHandler], TaskHandler]:
        """
        Decorator for registering task handlers.
        
        Args:
            task_type: Task type identifier.
            
        Returns:
            Decorator function.
            
        Example:
            @worker.task("send_email")
            async def send_email(task: Task):
                # ... handle task ...
                return result
        """
        def decorator(handler: TaskHandler) -> TaskHandler:
            self.register_handler(task_type, handler)
            return handler
        return decorator
    
    def get_handler(self, task_type: str) -> Optional[TaskHandler]:
        """Get the handler for a task type."""
        return self._handlers.get(task_type)
    
    # =========================================================================
    # LIFECYCLE
    # =========================================================================
    
    async def start(self) -> None:
        """
        Start the worker.
        
        This connects to the database, registers the worker, and
        starts the polling and heartbeat loops.
        """
        if self._running:
            logger.warning("Worker already running")
            return
        
        logger.info("Starting worker...")
        
        # Connect to database
        self._db = Database(self.settings.database)
        await self._db.connect()
        
        # Initialize repository and queue
        self._repository = TaskRepository(self._db)
        self._queue = TaskQueue(self._repository)
        
        # Create concurrency semaphore
        self._semaphore = asyncio.Semaphore(self.concurrency)
        
        # Register worker with system
        await self._register()
        
        self._running = True
        
        # Set up signal handlers for graceful shutdown
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            loop.add_signal_handler(sig, lambda: asyncio.create_task(self.stop()))
        
        # Start background tasks
        self._poll_task = asyncio.create_task(self._poll_loop(), name="poll_loop")
        self._heartbeat_task = asyncio.create_task(self._heartbeat_loop(), name="heartbeat_loop")
        
        logger.info("Worker started")
        
        # Wait for shutdown
        try:
            await asyncio.gather(self._poll_task, self._heartbeat_task)
        except asyncio.CancelledError:
            logger.info("Worker tasks cancelled")
    
    async def stop(self) -> None:
        """
        Stop the worker gracefully.
        
        This stops accepting new tasks, waits for in-flight tasks
        to complete (up to shutdown_timeout), then deregisters.
        """
        if not self._running:
            return
        
        logger.info("Stopping worker...")
        self._shutting_down = True
        self._running = False
        
        # Cancel background tasks
        if self._poll_task:
            self._poll_task.cancel()
        if self._heartbeat_task:
            self._heartbeat_task.cancel()
        
        # Wait for in-flight tasks with timeout
        if self._active_tasks:
            timeout = self._worker_settings.shutdown_timeout
            logger.info(
                f"Waiting for {len(self._active_tasks)} active tasks "
                f"(timeout: {timeout}s)"
            )
            
            try:
                await asyncio.wait_for(
                    asyncio.gather(*self._active_tasks.values(), return_exceptions=True),
                    timeout=timeout
                )
            except asyncio.TimeoutError:
                logger.warning(
                    f"Shutdown timeout reached, {len(self._active_tasks)} tasks still active"
                )
        
        # Deregister worker
        if self._repository:
            try:
                await self._repository.deregister_worker(self.worker_id)
            except Exception as e:
                logger.warning(f"Failed to deregister worker: {e}")
        
        # Close database connection
        if self._db:
            await self._db.disconnect()
        
        # Shutdown executor
        self._executor.shutdown(wait=False)
        
        logger.info("Worker stopped")
    
    async def _register(self) -> None:
        """Register this worker with the system."""
        await self._repository.register_worker(
            worker_id=self.worker_id,
            name=self.worker_name,
            hostname=socket.gethostname(),
            pid=os.getpid(),
            queues=self.queues,
            concurrency=self.concurrency,
            version="1.0.0",
            metadata={
                "python_version": os.sys.version,
                "handlers": list(self._handlers.keys()),
            }
        )
    
    # =========================================================================
    # TASK PROCESSING
    # =========================================================================
    
    async def _poll_loop(self) -> None:
        """
        Main polling loop that fetches and processes tasks.
        
        Uses exponential backoff when queues are empty to reduce
        database load.
        """
        poll_interval = self._worker_settings.poll_interval
        max_poll_interval = self._worker_settings.max_poll_interval
        batch_size = self._worker_settings.batch_size
        visibility_timeout = self._worker_settings.visibility_timeout
        
        current_interval = poll_interval
        empty_polls = 0
        
        while self._running:
            try:
                # Check if we have capacity
                available_capacity = self.concurrency - len(self._active_tasks)
                if available_capacity <= 0:
                    await asyncio.sleep(poll_interval)
                    continue
                
                # Claim tasks from each queue
                claimed_any = False
                
                for queue_name in self.queues:
                    if not self._running:
                        break
                    
                    # Claim tasks
                    fetch_size = min(batch_size, available_capacity)
                    tasks = await self._queue.claim(
                        queue_name=queue_name,
                        worker_id=self.worker_id,
                        batch_size=fetch_size,
                        visibility_timeout=visibility_timeout,
                    )
                    
                    if tasks:
                        claimed_any = True
                        empty_polls = 0
                        current_interval = poll_interval
                        
                        # Start processing each task
                        for task in tasks:
                            # Create processing task
                            async_task = asyncio.create_task(
                                self._process_task(task),
                                name=f"task_{task.id}"
                            )
                            self._active_tasks[task.id] = async_task
                            
                            # Clean up when done
                            async_task.add_done_callback(
                                lambda t, tid=task.id: self._active_tasks.pop(tid, None)
                            )
                        
                        available_capacity -= len(tasks)
                
                if not claimed_any:
                    # Empty poll - backoff
                    empty_polls += 1
                    current_interval = min(
                        current_interval * 1.5,
                        max_poll_interval
                    )
                
                await asyncio.sleep(current_interval)
                
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(f"Poll loop error: {e}")
                await asyncio.sleep(poll_interval)
    
    async def _process_task(self, task: Task) -> None:
        """
        Process a single task.
        
        This wraps the task handler with error handling, timeout
        management, and result reporting.
        """
        async with self._semaphore:
            started_at = datetime.utcnow()
            
            logger.info(
                f"Processing task",
                extra={
                    "task_id": str(task.id),
                    "task_type": task.task_type,
                    "attempt": task.attempt_count,
                }
            )
            
            # Get handler
            handler = self._handlers.get(task.task_type)
            if handler is None:
                error_msg = f"No handler registered for task type: {task.task_type}"
                logger.error(error_msg)
                await self._fail_task(task, error_msg, "HandlerNotFoundError")
                return
            
            # Execute with timeout
            try:
                result = await asyncio.wait_for(
                    self._execute_handler(handler, task),
                    timeout=task.timeout_seconds
                )
                
                # Success
                duration = (datetime.utcnow() - started_at).total_seconds()
                await self._complete_task(task, result, duration)
                
            except asyncio.TimeoutError:
                error_msg = f"Task execution timeout after {task.timeout_seconds}s"
                logger.error(error_msg, extra={"task_id": str(task.id)})
                await self._fail_task(task, error_msg, "TimeoutError")
                
            except asyncio.CancelledError:
                # Worker is shutting down - don't report as failure
                # Task will timeout and be reassigned
                logger.warning(
                    f"Task processing cancelled due to shutdown",
                    extra={"task_id": str(task.id)}
                )
                raise
                
            except Exception as e:
                # Handler raised an exception
                error_type = type(e).__name__
                error_msg = str(e)
                error_tb = traceback.format_exc()
                
                logger.error(
                    f"Task execution failed: {error_msg}",
                    extra={
                        "task_id": str(task.id),
                        "error_type": error_type,
                    }
                )
                
                await self._fail_task(task, error_msg, error_type, error_tb)
    
    async def _execute_handler(self, handler: TaskHandler, task: Task) -> Any:
        """
        Execute a task handler.
        
        Handles both sync and async handlers.
        """
        if asyncio.iscoroutinefunction(handler):
            # Async handler
            return await handler(task)
        else:
            # Sync handler - run in thread pool
            loop = asyncio.get_running_loop()
            return await loop.run_in_executor(self._executor, handler, task)
    
    async def _complete_task(
        self,
        task: Task,
        result: Any,
        duration: float
    ) -> None:
        """Report task completion."""
        try:
            # Convert result to dict if not already
            if result is None:
                result_dict = None
            elif isinstance(result, dict):
                result_dict = result
            else:
                result_dict = {"result": result}
            
            await self._queue.complete(
                task_id=task.id,
                result=result_dict,
                version=task.version,
            )
            
            self._stats["tasks_processed"] += 1
            self._stats["tasks_succeeded"] += 1
            
            logger.info(
                f"Task completed",
                extra={
                    "task_id": str(task.id),
                    "duration_seconds": round(duration, 3),
                }
            )
            
        except Exception as e:
            logger.error(f"Failed to report task completion: {e}")
    
    async def _fail_task(
        self,
        task: Task,
        error_message: str,
        error_type: str,
        error_traceback: Optional[str] = None
    ) -> None:
        """Report task failure."""
        try:
            error_details = {
                "error_type": error_type,
                "attempt": task.attempt_count,
            }
            if error_traceback:
                error_details["traceback"] = error_traceback
            
            updated_task = await self._queue.fail(
                task_id=task.id,
                error_message=error_message,
                error_details=error_details,
                version=task.version,
            )
            
            self._stats["tasks_processed"] += 1
            self._stats["tasks_failed"] += 1
            
            if updated_task and updated_task.status == TaskStatus.QUEUED:
                self._stats["tasks_retried"] += 1
            
        except Exception as e:
            logger.error(f"Failed to report task failure: {e}")
    
    # =========================================================================
    # HEARTBEAT
    # =========================================================================
    
    async def _heartbeat_loop(self) -> None:
        """
        Background loop that sends heartbeats and extends visibility.
        """
        interval = self._worker_settings.heartbeat_interval
        
        while self._running or self._active_tasks:
            try:
                # Get resource usage
                cpu_usage = self._get_cpu_usage()
                memory_usage = self._get_memory_usage()
                
                # Send heartbeat
                await self._repository.heartbeat(
                    worker_id=self.worker_id,
                    active_task_count=len(self._active_tasks),
                    cpu_usage=cpu_usage,
                    memory_usage=memory_usage,
                )
                
                # Extend visibility timeout for long-running tasks
                visibility_extension = self._worker_settings.visibility_timeout
                for task_id in list(self._active_tasks.keys()):
                    try:
                        await self._queue.extend_visibility(
                            task_id=task_id,
                            worker_id=self.worker_id,
                            extension_seconds=visibility_extension,
                        )
                    except Exception as e:
                        logger.warning(
                            f"Failed to extend visibility for task {task_id}: {e}"
                        )
                
            except asyncio.CancelledError:
                raise
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
            
            await asyncio.sleep(interval)
    
    def _get_cpu_usage(self) -> Optional[float]:
        """Get current CPU usage percentage."""
        try:
            import os
            # Simple approximation using load average on Unix
            if hasattr(os, 'getloadavg'):
                load = os.getloadavg()[0]
                cpu_count = os.cpu_count() or 1
                return min(100.0, (load / cpu_count) * 100)
        except Exception:
            pass
        return None
    
    def _get_memory_usage(self) -> Optional[float]:
        """Get current memory usage percentage."""
        try:
            import resource
            # Get memory usage in KB
            rusage = resource.getrusage(resource.RUSAGE_SELF)
            # maxrss is in KB on Linux, bytes on macOS
            import sys
            if sys.platform == 'darwin':
                mem_mb = rusage.ru_maxrss / (1024 * 1024)
            else:
                mem_mb = rusage.ru_maxrss / 1024
            
            # This is just the process memory, not percentage of total
            # Return None for now as we'd need psutil for accurate %
            return None
        except Exception:
            pass
        return None
    
    # =========================================================================
    # STATISTICS
    # =========================================================================
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get worker statistics.
        
        Returns:
            Dictionary with worker metrics.
        """
        return {
            "worker_id": str(self.worker_id),
            "worker_name": self.worker_name,
            "is_running": self._running,
            "active_tasks": len(self._active_tasks),
            "queues": self.queues,
            "concurrency": self.concurrency,
            **self._stats,
        }
    
    @property
    def active_task_count(self) -> int:
        """Get number of currently active tasks."""
        return len(self._active_tasks)


# Entry point for running worker directly
async def main():
    """Main entry point for the worker."""
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
    
    # Create worker
    worker = Worker(settings)
    
    # Register example handlers (in real usage, these would be imported)
    @worker.task("echo")
    async def echo_handler(task: Task):
        """Simple echo handler for testing."""
        return {"echo": task.payload}
    
    @worker.task("sleep")
    async def sleep_handler(task: Task):
        """Sleep handler for testing timeouts."""
        duration = task.payload.get("duration", 1)
        await asyncio.sleep(duration)
        return {"slept": duration}
    
    # Start worker
    await worker.start()


if __name__ == "__main__":
    asyncio.run(main())
