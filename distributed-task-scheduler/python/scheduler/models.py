"""
Data Models Module
==================

This module defines the core data models used throughout the distributed
task scheduler. These models use Pydantic for validation and serialization.

Model Hierarchy:
- Task: Represents a single task instance
- CronJob: Represents a recurring job definition
- Worker: Represents a worker node
- TaskResult: Detailed execution result for a task
- TaskEvent: Audit log entry for task state changes

Design Decisions:
1. Use Pydantic for automatic validation and serialization
2. Enums for status fields to ensure type safety
3. UUID for all primary keys (distributed ID generation)
4. Separate domain models from database models (clean architecture)
5. Immutable-by-default with explicit mutators
"""

from datetime import datetime, timedelta
from enum import Enum
from typing import Optional, Any, Dict, List
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator, ConfigDict


class TaskStatus(str, Enum):
    """
    Task lifecycle status.
    
    States:
        PENDING: Task is scheduled for future execution
        QUEUED: Task is ready and waiting for a worker
        ACTIVE: Task is being executed by a worker
        COMPLETED: Task finished successfully
        FAILED: Task execution failed (may be retried)
        DEAD: Task exceeded retry limit
        CANCELLED: Task was cancelled before execution
    
    Valid transitions:
        PENDING -> QUEUED (when scheduled_at <= now)
        PENDING -> CANCELLED (manual cancellation)
        QUEUED -> ACTIVE (worker claims task)
        QUEUED -> CANCELLED (manual cancellation)
        ACTIVE -> COMPLETED (successful execution)
        ACTIVE -> FAILED (execution error or timeout)
        FAILED -> QUEUED (retry)
        FAILED -> DEAD (retry limit exceeded)
    """
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    DEAD = "DEAD"
    CANCELLED = "CANCELLED"
    
    def is_terminal(self) -> bool:
        """Check if this is a terminal (final) state."""
        return self in (TaskStatus.COMPLETED, TaskStatus.DEAD, TaskStatus.CANCELLED)
    
    def can_transition_to(self, new_status: "TaskStatus") -> bool:
        """
        Check if transition to the new status is valid.
        
        Args:
            new_status: The target status to transition to.
            
        Returns:
            True if the transition is valid, False otherwise.
        """
        valid_transitions = {
            TaskStatus.PENDING: {TaskStatus.QUEUED, TaskStatus.CANCELLED},
            TaskStatus.QUEUED: {TaskStatus.ACTIVE, TaskStatus.CANCELLED},
            TaskStatus.ACTIVE: {TaskStatus.COMPLETED, TaskStatus.FAILED},
            TaskStatus.FAILED: {TaskStatus.QUEUED, TaskStatus.DEAD},
            TaskStatus.COMPLETED: set(),  # Terminal
            TaskStatus.DEAD: set(),  # Terminal
            TaskStatus.CANCELLED: set(),  # Terminal
        }
        return new_status in valid_transitions.get(self, set())


class WorkerStatus(str, Enum):
    """
    Worker node status.
    
    States:
        ACTIVE: Worker is healthy and processing tasks
        DRAINING: Worker is shutting down gracefully
        INACTIVE: Worker is offline or unhealthy
    """
    ACTIVE = "ACTIVE"
    DRAINING = "DRAINING"
    INACTIVE = "INACTIVE"


class CronJobStatus(str, Enum):
    """
    Cron job status.
    
    States:
        ENABLED: Job is active and will create tasks on schedule
        DISABLED: Job is paused, no new tasks created
        DELETED: Soft-deleted, preserved for history
    """
    ENABLED = "ENABLED"
    DISABLED = "DISABLED"
    DELETED = "DELETED"


class ConcurrencyPolicy(str, Enum):
    """
    Concurrency policy for cron jobs.
    
    Determines behavior when a cron job triggers while a previous
    instance is still running.
    
    Policies:
        ALLOW: Create new task regardless of previous run status
        FORBID: Skip this run if previous is still active
        REPLACE: Cancel previous run and start new
    """
    ALLOW = "ALLOW"
    FORBID = "FORBID"
    REPLACE = "REPLACE"


class RetryPolicy(BaseModel):
    """
    Retry configuration for a task.
    
    Implements exponential backoff with optional jitter to prevent
    thundering herd problems when many tasks fail simultaneously.
    
    Backoff formula:
        delay = min(max_delay, base_delay * (exponential_base ** attempt))
        if jitter: delay = random(0, delay)
    
    Attributes:
        max_attempts: Maximum total attempts (1 = no retries)
        base_delay: Initial delay in seconds
        max_delay: Maximum delay cap in seconds
        exponential_base: Multiplier for each retry (typically 2)
        jitter: Add randomization to prevent thundering herd
        retry_on: Exception types to retry on ('*' = all)
        no_retry_on: Exception types to never retry on
    """
    max_attempts: int = Field(default=3, ge=1, le=100)
    base_delay: float = Field(default=1.0, ge=0.0, le=3600.0)
    max_delay: float = Field(default=3600.0, ge=0.0, le=86400.0)
    exponential_base: float = Field(default=2.0, ge=1.0, le=10.0)
    jitter: bool = Field(default=True)
    retry_on: List[str] = Field(default_factory=lambda: ["*"])
    no_retry_on: List[str] = Field(default_factory=list)
    
    def calculate_delay(self, attempt: int) -> float:
        """
        Calculate the delay before the next retry attempt.
        
        Args:
            attempt: Current attempt number (0-indexed)
            
        Returns:
            Delay in seconds before the next retry
        """
        import random
        
        # Calculate exponential delay
        exponential_delay = self.base_delay * (self.exponential_base ** attempt)
        
        # Cap at max_delay
        capped_delay = min(self.max_delay, exponential_delay)
        
        # Apply jitter if enabled
        if self.jitter:
            return random.uniform(0, capped_delay)
        
        return capped_delay
    
    def should_retry(self, exception_type: str) -> bool:
        """
        Determine if a retry should be attempted for the given exception.
        
        Args:
            exception_type: Fully qualified exception class name
            
        Returns:
            True if retry should be attempted, False otherwise
        """
        # Check no_retry_on first (blocklist takes precedence)
        if exception_type in self.no_retry_on:
            return False
        
        # Check retry_on (allowlist)
        if "*" in self.retry_on:
            return True
        
        return exception_type in self.retry_on


class Task(BaseModel):
    """
    Task model representing a single task instance.
    
    A task is the fundamental unit of work in the scheduler. Each task
    has a type (determining which handler processes it), a payload
    (containing the data needed for execution), and lifecycle metadata.
    
    Tasks can be:
    - Immediate: Executed as soon as a worker is available
    - Scheduled: Executed at a specific future time
    - Recurring: Created by a cron job on a schedule
    
    Attributes:
        id: Unique task identifier (UUID)
        task_type: Type identifier for routing to handlers
        queue_name: Queue this task belongs to
        status: Current lifecycle status
        priority: Execution priority (0-100, higher = first)
        payload: Task data as JSON-compatible dict
        result: Execution result (set on completion)
        error_message: Error description (set on failure)
        error_details: Detailed error info (stack trace, etc.)
        idempotency_key: Optional key to prevent duplicates
        parent_task_id: Parent task for chained execution
        cron_job_id: Source cron job if scheduled
        scheduled_at: When to execute (None = immediate)
        retry_policy: Retry configuration
        timeout_seconds: Execution timeout
        worker_id: Assigned worker (when ACTIVE)
        visibility_timeout: When task becomes visible again
        attempt_count: Number of execution attempts
        version: Optimistic locking version
        created_at: When task was created
        updated_at: Last modification time
        queued_at: When task entered QUEUED state
        started_at: When execution started
        completed_at: When task finished
    """
    model_config = ConfigDict(use_enum_values=True)
    
    # Identity
    id: UUID = Field(default_factory=uuid4)
    task_type: str = Field(..., min_length=1, max_length=255)
    queue_name: str = Field(default="default", min_length=1, max_length=255)
    
    # Status and priority
    status: TaskStatus = Field(default=TaskStatus.QUEUED)
    priority: int = Field(default=50, ge=0, le=100)
    
    # Payload and result
    payload: Dict[str, Any] = Field(default_factory=dict)
    result: Optional[Dict[str, Any]] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    error_details: Optional[Dict[str, Any]] = Field(default=None)
    
    # Relationships and deduplication
    idempotency_key: Optional[str] = Field(default=None, max_length=255)
    parent_task_id: Optional[UUID] = Field(default=None)
    cron_job_id: Optional[UUID] = Field(default=None)
    
    # Scheduling
    scheduled_at: Optional[datetime] = Field(default=None)
    
    # Retry configuration
    max_attempts: int = Field(default=3, ge=1, le=100)
    retry_delay_seconds: float = Field(default=1.0, ge=0.0)
    timeout_seconds: int = Field(default=300, ge=1, le=86400)
    
    # Worker assignment
    worker_id: Optional[UUID] = Field(default=None)
    visibility_timeout: Optional[datetime] = Field(default=None)
    
    # Execution tracking
    attempt_count: int = Field(default=0, ge=0)
    version: int = Field(default=1, ge=1)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    queued_at: Optional[datetime] = Field(default=None)
    started_at: Optional[datetime] = Field(default=None)
    completed_at: Optional[datetime] = Field(default=None)
    
    @field_validator('task_type', 'queue_name')
    @classmethod
    def validate_identifier(cls, v: str) -> str:
        """Validate task type and queue name format."""
        if not v or not v.strip():
            raise ValueError("Value cannot be empty or whitespace")
        return v.strip()
    
    @property
    def is_terminal(self) -> bool:
        """Check if task is in a terminal state."""
        return TaskStatus(self.status).is_terminal()
    
    @property
    def can_retry(self) -> bool:
        """Check if task can be retried."""
        return (
            self.status == TaskStatus.FAILED and
            self.attempt_count < self.max_attempts
        )
    
    @property
    def execution_duration(self) -> Optional[timedelta]:
        """Calculate execution duration if available."""
        if self.started_at and self.completed_at:
            return self.completed_at - self.started_at
        return None
    
    def with_status(self, new_status: TaskStatus) -> "Task":
        """
        Create a copy of this task with a new status.
        
        This is the primary way to transition task state while
        maintaining immutability of the model.
        
        Args:
            new_status: The new status to set
            
        Returns:
            A new Task instance with the updated status
            
        Raises:
            ValueError: If the transition is not valid
        """
        current_status = TaskStatus(self.status)
        if not current_status.can_transition_to(new_status):
            raise ValueError(
                f"Invalid status transition: {self.status} -> {new_status.value}"
            )
        
        updates = {"status": new_status, "version": self.version + 1}
        
        # Set appropriate timestamps
        if new_status == TaskStatus.QUEUED:
            updates["queued_at"] = datetime.utcnow()
        elif new_status == TaskStatus.ACTIVE:
            updates["started_at"] = datetime.utcnow()
        elif new_status in (TaskStatus.COMPLETED, TaskStatus.FAILED, TaskStatus.DEAD):
            updates["completed_at"] = datetime.utcnow()
        
        return self.model_copy(update=updates)


class CronJob(BaseModel):
    """
    Cron job model representing a recurring task definition.
    
    Cron jobs create task instances according to their schedule.
    The scheduler evaluates all enabled cron jobs every tick and
    creates tasks when next_run_at <= now.
    
    Attributes:
        id: Unique job identifier
        name: Human-readable job name (unique)
        description: Job description
        schedule: Cron expression (minute hour day month weekday)
        timezone: Timezone for schedule evaluation
        task_type: Type of task to create
        task_payload: Payload for created tasks
        queue_name: Queue for created tasks
        priority: Priority for created tasks
        max_attempts: Max attempts for created tasks
        timeout_seconds: Timeout for created tasks
        status: Job status (ENABLED, DISABLED, DELETED)
        concurrency_policy: How to handle overlapping runs
        next_run_at: Next scheduled execution time
        last_run_at: Last execution time
        run_count: Total number of runs
        success_count: Successful runs
        failure_count: Failed runs
        metadata: Arbitrary metadata
        created_at: When job was created
        updated_at: Last modification time
    """
    model_config = ConfigDict(use_enum_values=True)
    
    # Identity
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = Field(default=None)
    
    # Schedule
    schedule: str = Field(..., min_length=1, max_length=100)
    timezone: str = Field(default="UTC")
    
    # Task configuration
    task_type: str = Field(..., min_length=1, max_length=255)
    task_payload: Dict[str, Any] = Field(default_factory=dict)
    queue_name: str = Field(default="default")
    priority: int = Field(default=50, ge=0, le=100)
    max_attempts: int = Field(default=3, ge=1, le=100)
    timeout_seconds: int = Field(default=300, ge=1, le=86400)
    
    # Status
    status: CronJobStatus = Field(default=CronJobStatus.ENABLED)
    concurrency_policy: ConcurrencyPolicy = Field(default=ConcurrencyPolicy.ALLOW)
    
    # Scheduling state
    next_run_at: Optional[datetime] = Field(default=None)
    last_run_at: Optional[datetime] = Field(default=None)
    
    # Statistics
    run_count: int = Field(default=0, ge=0)
    success_count: int = Field(default=0, ge=0)
    failure_count: int = Field(default=0, ge=0)
    
    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    @field_validator('schedule')
    @classmethod
    def validate_schedule(cls, v: str) -> str:
        """Validate cron expression format."""
        # Basic validation - proper validation happens at runtime with croniter
        parts = v.split()
        if len(parts) != 5:
            raise ValueError(
                f"Invalid cron expression: expected 5 fields, got {len(parts)}. "
                "Format: minute hour day month weekday"
            )
        return v
    
    @property
    def success_rate(self) -> Optional[float]:
        """Calculate success rate as a percentage."""
        if self.run_count == 0:
            return None
        return (self.success_count / self.run_count) * 100
    
    def create_task(self) -> Task:
        """
        Create a new task instance from this cron job.
        
        Returns:
            A new Task configured according to this job's settings.
        """
        return Task(
            task_type=self.task_type,
            queue_name=self.queue_name,
            status=TaskStatus.QUEUED,
            priority=self.priority,
            payload=self.task_payload.copy(),
            cron_job_id=self.id,
            max_attempts=self.max_attempts,
            timeout_seconds=self.timeout_seconds,
            queued_at=datetime.utcnow(),
        )


class Worker(BaseModel):
    """
    Worker model representing a task processing node.
    
    Workers register themselves on startup and send periodic heartbeats.
    The scheduler uses heartbeats to detect failed workers and reassign
    their tasks.
    
    Attributes:
        id: Unique worker identifier
        name: Human-readable name (usually hostname:pid)
        hostname: Machine hostname
        ip_address: Worker IP address
        port: Port for health checks (optional)
        pid: Process ID
        queues: List of queues this worker processes
        concurrency: Maximum concurrent tasks
        status: Worker health status
        active_task_count: Current number of active tasks
        cpu_usage: CPU utilization (0-100)
        memory_usage: Memory utilization (0-100)
        last_heartbeat: Last heartbeat timestamp
        heartbeat_interval_seconds: Expected heartbeat interval
        started_at: When worker started
        stopped_at: When worker stopped (if applicable)
        version: Software version
        metadata: Arbitrary metadata
    """
    model_config = ConfigDict(use_enum_values=True)
    
    # Identity
    id: UUID = Field(default_factory=uuid4)
    name: str = Field(..., min_length=1, max_length=255)
    hostname: str = Field(..., min_length=1, max_length=255)
    ip_address: Optional[str] = Field(default=None)
    port: Optional[int] = Field(default=None, ge=1, le=65535)
    pid: int = Field(..., ge=1)
    
    # Configuration
    queues: List[str] = Field(default_factory=lambda: ["default"])
    concurrency: int = Field(default=10, ge=1, le=1000)
    
    # Status
    status: WorkerStatus = Field(default=WorkerStatus.ACTIVE)
    active_task_count: int = Field(default=0, ge=0)
    
    # Resource tracking
    cpu_usage: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    memory_usage: Optional[float] = Field(default=None, ge=0.0, le=100.0)
    
    # Heartbeat
    last_heartbeat: datetime = Field(default_factory=datetime.utcnow)
    heartbeat_interval_seconds: int = Field(default=10, ge=1, le=300)
    
    # Lifecycle
    started_at: datetime = Field(default_factory=datetime.utcnow)
    stopped_at: Optional[datetime] = Field(default=None)
    
    # Metadata
    version: Optional[str] = Field(default=None)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    @property
    def is_healthy(self) -> bool:
        """
        Check if worker is considered healthy.
        
        A worker is healthy if it's ACTIVE and its last heartbeat
        is within the expected interval (with some tolerance).
        """
        if self.status != WorkerStatus.ACTIVE:
            return False
        
        # Allow 3x heartbeat interval as grace period
        max_age = timedelta(seconds=self.heartbeat_interval_seconds * 3)
        return datetime.utcnow() - self.last_heartbeat < max_age
    
    @property
    def available_capacity(self) -> int:
        """Calculate remaining task capacity."""
        return max(0, self.concurrency - self.active_task_count)


class TaskResult(BaseModel):
    """
    Detailed task execution result.
    
    Stored separately from the task for space efficiency and
    to support multiple attempts per task.
    
    Attributes:
        id: Result record identifier
        task_id: Associated task
        worker_id: Worker that executed
        attempt_number: Which attempt this result is for
        success: Whether execution succeeded
        result: Return value (on success)
        error_message: Error description (on failure)
        error_type: Exception class name
        error_traceback: Full stack trace
        started_at: When execution started
        completed_at: When execution finished
        duration_ms: Execution duration in milliseconds
        cpu_time_ms: CPU time consumed
        memory_peak_mb: Peak memory usage
        logs: Captured log output
    """
    id: UUID = Field(default_factory=uuid4)
    task_id: UUID
    worker_id: Optional[UUID] = Field(default=None)
    attempt_number: int = Field(ge=1)
    
    # Result
    success: bool
    result: Optional[Dict[str, Any]] = Field(default=None)
    error_message: Optional[str] = Field(default=None)
    error_type: Optional[str] = Field(default=None)
    error_traceback: Optional[str] = Field(default=None)
    
    # Timing
    started_at: datetime
    completed_at: datetime
    duration_ms: int = Field(ge=0)
    
    # Resource usage
    cpu_time_ms: Optional[int] = Field(default=None, ge=0)
    memory_peak_mb: Optional[int] = Field(default=None, ge=0)
    
    # Logs
    logs: Optional[str] = Field(default=None)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)


class TaskEvent(BaseModel):
    """
    Task state change event for audit logging.
    
    Every state transition is recorded for debugging,
    compliance, and potential event sourcing.
    
    Attributes:
        id: Event sequence number
        task_id: Associated task
        event_type: Type of event (STATUS_CHANGE, etc.)
        from_status: Previous status (for transitions)
        to_status: New status (for transitions)
        triggered_by: Who/what triggered the event
        details: Additional context
        created_at: When event occurred
    """
    id: Optional[int] = Field(default=None)
    task_id: UUID
    event_type: str = Field(..., min_length=1, max_length=50)
    from_status: Optional[TaskStatus] = Field(default=None)
    to_status: Optional[TaskStatus] = Field(default=None)
    triggered_by: Optional[str] = Field(default=None)
    details: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# Type aliases for clarity
TaskId = UUID
WorkerId = UUID
CronJobId = UUID
