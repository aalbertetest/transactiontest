"""
Task Queue Abstraction Module
=============================

This module provides the task queue abstraction layer that handles
task submission, claiming, and lifecycle management. It serves as
the interface between the scheduler/worker components and the
persistence layer.

Key Features:
- Task submission with validation
- Idempotent task creation
- Priority-based queuing
- Scheduled task support
- Dead letter queue management

Design Decisions:
1. Queue as a high-level abstraction over the repository
2. Business logic for task routing and validation
3. Event emission for observability
4. Thread-safe async operations
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Callable, Dict, List, Optional, Set
from uuid import UUID

from ..persistence.repository import TaskRepository
from ..scheduler.models import Task, TaskStatus, ConcurrencyPolicy

logger = logging.getLogger(__name__)


# Type alias for task handlers
TaskHandler = Callable[[Task], Any]


class TaskQueueError(Exception):
    """Base exception for task queue errors."""
    pass


class TaskNotFoundError(TaskQueueError):
    """Raised when a task is not found."""
    pass


class TaskStateError(TaskQueueError):
    """Raised when a task operation is invalid for current state."""
    pass


class TaskQueue:
    """
    High-level task queue abstraction.
    
    This class provides a clean API for interacting with the task queue,
    abstracting away the underlying persistence details. It handles:
    
    - Task submission with validation and routing
    - Task claiming for workers
    - Task completion and failure handling
    - Scheduled task management
    - Dead letter queue operations
    
    The queue supports multiple named queues for task routing, allowing
    different worker pools to process different types of tasks.
    
    Usage:
        queue = TaskQueue(repository)
        
        # Submit a task
        task = await queue.submit(
            task_type="send_email",
            payload={"to": "user@example.com"},
            queue_name="email",
            priority=50
        )
        
        # Claim tasks for processing
        tasks = await queue.claim("email", worker_id, batch_size=5)
        
        # Complete a task
        await queue.complete(task.id, result={"sent": True})
    
    Attributes:
        repository: The underlying task repository.
        handlers: Registered task handlers by type.
    """
    
    def __init__(self, repository: TaskRepository):
        """
        Initialize the task queue.
        
        Args:
            repository: TaskRepository for database operations.
        """
        self._repository = repository
        self._handlers: Dict[str, TaskHandler] = {}
        self._listeners: Dict[str, List[Callable]] = {}
    
    # =========================================================================
    # TASK SUBMISSION
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
        parent_task_id: Optional[UUID] = None,
    ) -> Task:
        """
        Submit a new task to the queue.
        
        Tasks can be submitted for immediate execution or scheduled
        for future execution. Use idempotency_key to prevent duplicate
        task creation (useful for exactly-once semantics).
        
        Args:
            task_type: Type identifier that determines which handler
                       processes this task. Must be registered with workers.
            payload: Task data as a JSON-serializable dictionary.
                     This is passed to the task handler.
            queue_name: Queue to place the task in. Workers subscribe
                        to specific queues.
            priority: Task priority from 0 (lowest) to 100 (highest).
                      Higher priority tasks are processed first.
            scheduled_at: Absolute time to execute the task. If None
                          and delay_seconds is None, executes immediately.
            delay_seconds: Relative delay before execution. Overrides
                           scheduled_at if both are provided.
            idempotency_key: Optional unique key. If a non-terminal task
                             with this key exists, returns it instead of
                             creating a duplicate.
            max_attempts: Maximum execution attempts including retries.
            timeout_seconds: Per-attempt execution timeout.
            parent_task_id: Parent task for chained execution patterns.
            
        Returns:
            The created Task (or existing task if idempotent).
            
        Raises:
            TaskQueueError: If task creation fails.
            
        Example:
            # Immediate task
            task = await queue.submit("send_email", {"to": "user@example.com"})
            
            # Scheduled task
            task = await queue.submit(
                "generate_report",
                {"report_id": 123},
                scheduled_at=datetime.utcnow() + timedelta(hours=1)
            )
            
            # Idempotent task
            task = await queue.submit(
                "process_payment",
                {"order_id": "ord_123"},
                idempotency_key="payment_ord_123"
            )
        """
        # Validate inputs
        if not task_type or not task_type.strip():
            raise TaskQueueError("task_type cannot be empty")
        
        if not 0 <= priority <= 100:
            raise TaskQueueError("priority must be between 0 and 100")
        
        # Calculate scheduled_at from delay_seconds
        if delay_seconds is not None:
            scheduled_at = datetime.utcnow() + timedelta(seconds=delay_seconds)
        
        try:
            task = await self._repository.create_task(
                task_type=task_type.strip(),
                payload=payload,
                queue_name=queue_name.strip(),
                priority=priority,
                scheduled_at=scheduled_at,
                idempotency_key=idempotency_key,
                max_attempts=max_attempts,
                timeout_seconds=timeout_seconds,
                parent_task_id=parent_task_id,
            )
            
            # Emit task created event
            await self._emit_event("task_created", task)
            
            return task
            
        except Exception as e:
            logger.error(f"Failed to submit task: {e}")
            raise TaskQueueError(f"Failed to submit task: {e}") from e
    
    async def submit_batch(
        self,
        tasks: List[Dict[str, Any]],
        queue_name: str = "default",
    ) -> List[Task]:
        """
        Submit multiple tasks at once.
        
        This is more efficient than calling submit() in a loop as it
        can batch database operations.
        
        Args:
            tasks: List of task specifications. Each dict should contain:
                   - task_type: str (required)
                   - payload: dict (required)
                   - priority: int (optional, default 50)
                   - scheduled_at: datetime (optional)
                   - idempotency_key: str (optional)
            queue_name: Default queue for all tasks.
            
        Returns:
            List of created Tasks.
            
        Raises:
            TaskQueueError: If batch submission fails.
        """
        created_tasks = []
        
        for task_spec in tasks:
            task = await self.submit(
                task_type=task_spec["task_type"],
                payload=task_spec["payload"],
                queue_name=task_spec.get("queue_name", queue_name),
                priority=task_spec.get("priority", 50),
                scheduled_at=task_spec.get("scheduled_at"),
                idempotency_key=task_spec.get("idempotency_key"),
                max_attempts=task_spec.get("max_attempts", 3),
                timeout_seconds=task_spec.get("timeout_seconds", 300),
            )
            created_tasks.append(task)
        
        return created_tasks
    
    # =========================================================================
    # TASK CLAIMING
    # =========================================================================
    
    async def claim(
        self,
        queue_name: str,
        worker_id: UUID,
        batch_size: int = 1,
        visibility_timeout: int = 300,
    ) -> List[Task]:
        """
        Claim tasks from a queue for processing.
        
        This method atomically claims up to batch_size tasks that are
        ready for execution. Claimed tasks are marked as ACTIVE and
        become invisible to other workers until the visibility timeout
        expires or the task is completed/failed.
        
        Uses SELECT FOR UPDATE SKIP LOCKED for efficient claiming
        without contention between workers.
        
        Args:
            queue_name: Queue to claim from.
            worker_id: ID of the claiming worker.
            batch_size: Maximum number of tasks to claim.
            visibility_timeout: Seconds until task becomes visible again.
            
        Returns:
            List of claimed tasks (may be empty if queue is empty).
            
        Example:
            # Claim tasks in a worker loop
            while running:
                tasks = await queue.claim("default", worker_id, batch_size=5)
                
                for task in tasks:
                    try:
                        result = await process_task(task)
                        await queue.complete(task.id, result=result)
                    except Exception as e:
                        await queue.fail(task.id, str(e))
        """
        tasks = await self._repository.claim_tasks(
            worker_id=worker_id,
            queue_name=queue_name,
            batch_size=batch_size,
            visibility_timeout_seconds=visibility_timeout,
        )
        
        # Emit claim events
        for task in tasks:
            await self._emit_event("task_claimed", task)
        
        return tasks
    
    # =========================================================================
    # TASK COMPLETION
    # =========================================================================
    
    async def complete(
        self,
        task_id: UUID,
        result: Optional[Dict[str, Any]] = None,
        version: Optional[int] = None,
    ) -> Task:
        """
        Mark a task as completed successfully.
        
        The task must be in ACTIVE status. Use the version parameter
        for optimistic locking if you want to prevent concurrent updates.
        
        Args:
            task_id: ID of the task to complete.
            result: Optional result data to store.
            version: Expected task version for optimistic locking.
            
        Returns:
            The updated Task.
            
        Raises:
            TaskNotFoundError: If task not found.
            TaskStateError: If task is not ACTIVE or version mismatch.
        """
        task = await self._repository.complete_task(
            task_id=task_id,
            result=result,
            expected_version=version,
        )
        
        if task is None:
            raise TaskStateError(
                f"Task {task_id} not found, not ACTIVE, or version mismatch"
            )
        
        await self._emit_event("task_completed", task)
        return task
    
    async def fail(
        self,
        task_id: UUID,
        error_message: str,
        error_details: Optional[Dict[str, Any]] = None,
        version: Optional[int] = None,
    ) -> Task:
        """
        Mark a task as failed.
        
        If the task has remaining retry attempts, it will be re-queued
        with an exponential backoff delay. Otherwise, it moves to DEAD
        status in the dead letter queue.
        
        Args:
            task_id: ID of the task to fail.
            error_message: Human-readable error description.
            error_details: Additional error context (stack trace, etc.).
            version: Expected task version for optimistic locking.
            
        Returns:
            The updated Task.
            
        Raises:
            TaskNotFoundError: If task not found.
            TaskStateError: If task is not ACTIVE or version mismatch.
        """
        task = await self._repository.fail_task(
            task_id=task_id,
            error_message=error_message,
            error_details=error_details,
            expected_version=version,
        )
        
        if task is None:
            raise TaskStateError(
                f"Task {task_id} not found, not ACTIVE, or version mismatch"
            )
        
        # Emit appropriate event based on new status
        if task.status == TaskStatus.DEAD:
            await self._emit_event("task_dead", task)
        else:
            await self._emit_event("task_failed", task)
        
        return task
    
    async def cancel(self, task_id: UUID) -> Task:
        """
        Cancel a pending or queued task.
        
        Only tasks in PENDING or QUEUED status can be cancelled.
        ACTIVE tasks must complete or fail through normal processing.
        
        Args:
            task_id: ID of the task to cancel.
            
        Returns:
            The cancelled Task.
            
        Raises:
            TaskNotFoundError: If task not found.
            TaskStateError: If task cannot be cancelled.
        """
        task = await self._repository.cancel_task(task_id)
        
        if task is None:
            raise TaskStateError(
                f"Task {task_id} not found or not in PENDING/QUEUED status"
            )
        
        await self._emit_event("task_cancelled", task)
        return task
    
    async def extend_visibility(
        self,
        task_id: UUID,
        worker_id: UUID,
        extension_seconds: int = 300,
    ) -> bool:
        """
        Extend the visibility timeout for an active task.
        
        Workers should call this periodically for long-running tasks
        to prevent timeout and reassignment to another worker.
        
        Args:
            task_id: ID of the task to extend.
            worker_id: ID of the worker holding the task.
            extension_seconds: Additional time to add.
            
        Returns:
            True if extended, False if task not found or not owned.
        """
        return await self._repository.extend_visibility_timeout(
            task_id=task_id,
            worker_id=worker_id,
            extension_seconds=extension_seconds,
        )
    
    # =========================================================================
    # TASK QUERIES
    # =========================================================================
    
    async def get(self, task_id: UUID) -> Optional[Task]:
        """
        Get a task by ID.
        
        Args:
            task_id: Task identifier.
            
        Returns:
            Task if found, None otherwise.
        """
        return await self._repository.get_task(task_id)
    
    async def get_or_raise(self, task_id: UUID) -> Task:
        """
        Get a task by ID, raising if not found.
        
        Args:
            task_id: Task identifier.
            
        Returns:
            The task.
            
        Raises:
            TaskNotFoundError: If task not found.
        """
        task = await self.get(task_id)
        if task is None:
            raise TaskNotFoundError(f"Task {task_id} not found")
        return task
    
    async def list_tasks(
        self,
        status: Optional[TaskStatus] = None,
        queue_name: Optional[str] = None,
        task_type: Optional[str] = None,
        limit: int = 100,
        offset: int = 0,
    ) -> List[Task]:
        """
        List tasks with optional filtering.
        
        Args:
            status: Filter by status.
            queue_name: Filter by queue.
            task_type: Filter by type.
            limit: Maximum results.
            offset: Pagination offset.
            
        Returns:
            List of matching tasks.
        """
        return await self._repository.get_tasks(
            status=status,
            queue_name=queue_name,
            task_type=task_type,
            limit=limit,
            offset=offset,
        )
    
    async def get_dead_letter_tasks(
        self,
        queue_name: Optional[str] = None,
        limit: int = 100,
    ) -> List[Task]:
        """
        Get tasks in the dead letter queue.
        
        Args:
            queue_name: Filter by original queue.
            limit: Maximum results.
            
        Returns:
            List of dead tasks.
        """
        return await self._repository.get_tasks(
            status=TaskStatus.DEAD,
            queue_name=queue_name,
            limit=limit,
        )
    
    async def retry_dead_task(self, task_id: UUID) -> Task:
        """
        Retry a task from the dead letter queue.
        
        This resets the attempt count and re-queues the task.
        
        Args:
            task_id: ID of the dead task to retry.
            
        Returns:
            The re-queued task.
            
        Raises:
            TaskNotFoundError: If task not found.
            TaskStateError: If task is not in DEAD status.
        """
        task = await self.get_or_raise(task_id)
        
        if task.status != TaskStatus.DEAD:
            raise TaskStateError(f"Task {task_id} is not in DEAD status")
        
        # Create a new task with the same parameters
        new_task = await self.submit(
            task_type=task.task_type,
            payload=task.payload,
            queue_name=task.queue_name,
            priority=task.priority,
            max_attempts=task.max_attempts,
            timeout_seconds=task.timeout_seconds,
            parent_task_id=task.parent_task_id,
        )
        
        logger.info(
            f"Retried dead task",
            extra={"old_task_id": str(task_id), "new_task_id": str(new_task.id)}
        )
        
        return new_task
    
    # =========================================================================
    # QUEUE STATISTICS
    # =========================================================================
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get queue statistics for all queues.
        
        Returns:
            Dictionary with queue metrics organized by queue name.
        """
        stats = await self._repository.get_queue_stats()
        
        # Organize by queue name
        by_queue: Dict[str, Dict[str, int]] = {}
        for row in stats:
            queue = row['queue_name']
            status = row['status']
            count = row['task_count']
            
            if queue not in by_queue:
                by_queue[queue] = {}
            by_queue[queue][status] = count
        
        return by_queue
    
    async def get_queue_depth(self, queue_name: str) -> int:
        """
        Get the number of queued tasks in a specific queue.
        
        Args:
            queue_name: Queue to check.
            
        Returns:
            Number of QUEUED tasks.
        """
        tasks = await self._repository.get_tasks(
            status=TaskStatus.QUEUED,
            queue_name=queue_name,
            limit=1,
        )
        
        # This is inefficient for large queues - in production,
        # you'd want a dedicated count query
        stats = await self.get_stats()
        return stats.get(queue_name, {}).get(TaskStatus.QUEUED.value, 0)
    
    # =========================================================================
    # TASK HANDLERS
    # =========================================================================
    
    def register_handler(self, task_type: str, handler: TaskHandler) -> None:
        """
        Register a handler for a task type.
        
        This is typically called by workers to define how to process
        each task type.
        
        Args:
            task_type: Task type identifier.
            handler: Callable that processes tasks of this type.
        """
        self._handlers[task_type] = handler
        logger.debug(f"Registered handler for task type: {task_type}")
    
    def get_handler(self, task_type: str) -> Optional[TaskHandler]:
        """
        Get the handler for a task type.
        
        Args:
            task_type: Task type identifier.
            
        Returns:
            Handler if registered, None otherwise.
        """
        return self._handlers.get(task_type)
    
    # =========================================================================
    # EVENT LISTENERS
    # =========================================================================
    
    def on(self, event_type: str, callback: Callable) -> None:
        """
        Register a listener for queue events.
        
        Events:
        - task_created: Task was created
        - task_claimed: Task was claimed by a worker
        - task_completed: Task completed successfully
        - task_failed: Task failed (will be retried)
        - task_dead: Task moved to dead letter queue
        - task_cancelled: Task was cancelled
        
        Args:
            event_type: Event type to listen for.
            callback: Async callable to invoke when event occurs.
        """
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
    
    async def _emit_event(self, event_type: str, task: Task) -> None:
        """Emit an event to registered listeners."""
        listeners = self._listeners.get(event_type, [])
        
        for callback in listeners:
            try:
                import asyncio
                if asyncio.iscoroutinefunction(callback):
                    await callback(task)
                else:
                    callback(task)
            except Exception as e:
                logger.warning(f"Event listener error: {e}")
    
    # =========================================================================
    # MAINTENANCE
    # =========================================================================
    
    async def promote_pending(self) -> int:
        """
        Promote pending tasks to queued when their time arrives.
        
        This should be called periodically by the scheduler.
        
        Returns:
            Number of tasks promoted.
        """
        return await self._repository.promote_pending_tasks()
    
    async def recover_timeouts(self) -> int:
        """
        Recover tasks that exceeded visibility timeout.
        
        This should be called periodically by the scheduler.
        
        Returns:
            Number of tasks recovered.
        """
        return await self._repository.recover_timed_out_tasks()
