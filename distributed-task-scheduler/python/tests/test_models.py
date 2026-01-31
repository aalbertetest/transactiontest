"""
Unit Tests for Data Models
==========================

Tests for the core data models used in the distributed task scheduler.
These tests verify:
- Model validation
- State transitions
- Retry policy calculations
- Serialization/deserialization
"""

import pytest
from datetime import datetime, timedelta
from uuid import uuid4

from scheduler.models import (
    Task, TaskStatus, CronJob, CronJobStatus, Worker, WorkerStatus,
    RetryPolicy, ConcurrencyPolicy
)


class TestTaskStatus:
    """Tests for TaskStatus enum and transitions."""
    
    def test_terminal_states(self):
        """Test that terminal states are correctly identified."""
        assert TaskStatus.COMPLETED.is_terminal()
        assert TaskStatus.DEAD.is_terminal()
        assert TaskStatus.CANCELLED.is_terminal()
        
        assert not TaskStatus.PENDING.is_terminal()
        assert not TaskStatus.QUEUED.is_terminal()
        assert not TaskStatus.ACTIVE.is_terminal()
        assert not TaskStatus.FAILED.is_terminal()
    
    def test_valid_transitions(self):
        """Test valid state transitions."""
        # PENDING can go to QUEUED or CANCELLED
        assert TaskStatus.PENDING.can_transition_to(TaskStatus.QUEUED)
        assert TaskStatus.PENDING.can_transition_to(TaskStatus.CANCELLED)
        
        # QUEUED can go to ACTIVE or CANCELLED
        assert TaskStatus.QUEUED.can_transition_to(TaskStatus.ACTIVE)
        assert TaskStatus.QUEUED.can_transition_to(TaskStatus.CANCELLED)
        
        # ACTIVE can go to COMPLETED or FAILED
        assert TaskStatus.ACTIVE.can_transition_to(TaskStatus.COMPLETED)
        assert TaskStatus.ACTIVE.can_transition_to(TaskStatus.FAILED)
        
        # FAILED can go to QUEUED (retry) or DEAD
        assert TaskStatus.FAILED.can_transition_to(TaskStatus.QUEUED)
        assert TaskStatus.FAILED.can_transition_to(TaskStatus.DEAD)
    
    def test_invalid_transitions(self):
        """Test that invalid transitions are rejected."""
        # Terminal states cannot transition
        assert not TaskStatus.COMPLETED.can_transition_to(TaskStatus.QUEUED)
        assert not TaskStatus.DEAD.can_transition_to(TaskStatus.QUEUED)
        assert not TaskStatus.CANCELLED.can_transition_to(TaskStatus.QUEUED)
        
        # Invalid direct transitions
        assert not TaskStatus.PENDING.can_transition_to(TaskStatus.ACTIVE)
        assert not TaskStatus.QUEUED.can_transition_to(TaskStatus.COMPLETED)
        assert not TaskStatus.ACTIVE.can_transition_to(TaskStatus.QUEUED)


class TestRetryPolicy:
    """Tests for RetryPolicy."""
    
    def test_default_values(self):
        """Test default retry policy values."""
        policy = RetryPolicy()
        
        assert policy.max_attempts == 3
        assert policy.base_delay == 1.0
        assert policy.max_delay == 3600.0
        assert policy.exponential_base == 2.0
        assert policy.jitter is True
    
    def test_calculate_delay_no_jitter(self):
        """Test delay calculation without jitter."""
        policy = RetryPolicy(
            base_delay=1.0,
            exponential_base=2.0,
            max_delay=3600.0,
            jitter=False
        )
        
        # First retry: 1 * 2^0 = 1
        assert policy.calculate_delay(0) == 1.0
        
        # Second retry: 1 * 2^1 = 2
        assert policy.calculate_delay(1) == 2.0
        
        # Third retry: 1 * 2^2 = 4
        assert policy.calculate_delay(2) == 4.0
        
        # Fourth retry: 1 * 2^3 = 8
        assert policy.calculate_delay(3) == 8.0
    
    def test_calculate_delay_with_cap(self):
        """Test that delay is capped at max_delay."""
        policy = RetryPolicy(
            base_delay=100.0,
            exponential_base=2.0,
            max_delay=500.0,
            jitter=False
        )
        
        # First retry: 100 * 2^0 = 100
        assert policy.calculate_delay(0) == 100.0
        
        # Second retry: 100 * 2^1 = 200
        assert policy.calculate_delay(1) == 200.0
        
        # Third retry: 100 * 2^2 = 400
        assert policy.calculate_delay(2) == 400.0
        
        # Fourth retry: 100 * 2^3 = 800, capped to 500
        assert policy.calculate_delay(3) == 500.0
    
    def test_calculate_delay_with_jitter(self):
        """Test that jitter adds randomization."""
        policy = RetryPolicy(
            base_delay=10.0,
            exponential_base=2.0,
            jitter=True
        )
        
        # With jitter, delay should be between 0 and calculated value
        delays = [policy.calculate_delay(2) for _ in range(100)]
        
        # All delays should be <= 40 (10 * 2^2)
        assert all(0 <= d <= 40.0 for d in delays)
        
        # With jitter, we should have some variation
        assert len(set(delays)) > 1
    
    def test_should_retry_wildcard(self):
        """Test retry on all exceptions with wildcard."""
        policy = RetryPolicy(retry_on=["*"])
        
        assert policy.should_retry("ValueError")
        assert policy.should_retry("RuntimeError")
        assert policy.should_retry("CustomException")
    
    def test_should_retry_specific(self):
        """Test retry on specific exceptions."""
        policy = RetryPolicy(
            retry_on=["ConnectionError", "TimeoutError"],
            no_retry_on=[]
        )
        
        assert policy.should_retry("ConnectionError")
        assert policy.should_retry("TimeoutError")
        assert not policy.should_retry("ValueError")
    
    def test_should_retry_blocklist(self):
        """Test no_retry_on takes precedence."""
        policy = RetryPolicy(
            retry_on=["*"],
            no_retry_on=["ValueError", "ValidationError"]
        )
        
        assert policy.should_retry("RuntimeError")
        assert not policy.should_retry("ValueError")
        assert not policy.should_retry("ValidationError")


class TestTask:
    """Tests for Task model."""
    
    def test_create_task(self):
        """Test basic task creation."""
        task = Task(
            task_type="send_email",
            payload={"to": "user@example.com"}
        )
        
        assert task.id is not None
        assert task.task_type == "send_email"
        assert task.queue_name == "default"
        assert task.status == TaskStatus.QUEUED
        assert task.priority == 50
        assert task.payload == {"to": "user@example.com"}
        assert task.version == 1
    
    def test_task_with_scheduling(self):
        """Test task with scheduled execution."""
        future = datetime.utcnow() + timedelta(hours=1)
        
        task = Task(
            task_type="generate_report",
            payload={"report_id": 123},
            status=TaskStatus.PENDING,
            scheduled_at=future
        )
        
        assert task.status == TaskStatus.PENDING
        assert task.scheduled_at == future
    
    def test_task_with_idempotency_key(self):
        """Test task with idempotency key."""
        task = Task(
            task_type="process_payment",
            payload={"order_id": "ord_123"},
            idempotency_key="payment_ord_123"
        )
        
        assert task.idempotency_key == "payment_ord_123"
    
    def test_task_is_terminal(self):
        """Test is_terminal property."""
        completed = Task(task_type="test", status=TaskStatus.COMPLETED)
        assert completed.is_terminal
        
        queued = Task(task_type="test", status=TaskStatus.QUEUED)
        assert not queued.is_terminal
    
    def test_task_can_retry(self):
        """Test can_retry property."""
        # Failed with retries remaining
        failed_retryable = Task(
            task_type="test",
            status=TaskStatus.FAILED,
            attempt_count=1,
            max_attempts=3
        )
        assert failed_retryable.can_retry
        
        # Failed with no retries remaining
        failed_exhausted = Task(
            task_type="test",
            status=TaskStatus.FAILED,
            attempt_count=3,
            max_attempts=3
        )
        assert not failed_exhausted.can_retry
        
        # Not failed
        queued = Task(task_type="test", status=TaskStatus.QUEUED)
        assert not queued.can_retry
    
    def test_task_with_status_transition(self):
        """Test with_status creates new task with updated status."""
        original = Task(
            task_type="test",
            status=TaskStatus.QUEUED,
            version=1
        )
        
        active = original.with_status(TaskStatus.ACTIVE)
        
        # Original unchanged
        assert original.status == TaskStatus.QUEUED
        assert original.version == 1
        
        # New task has updated status and version
        assert active.status == TaskStatus.ACTIVE
        assert active.version == 2
        assert active.started_at is not None
    
    def test_task_invalid_transition_raises(self):
        """Test that invalid transition raises ValueError."""
        task = Task(task_type="test", status=TaskStatus.QUEUED)
        
        with pytest.raises(ValueError, match="Invalid status transition"):
            task.with_status(TaskStatus.COMPLETED)
    
    def test_task_validation(self):
        """Test task validation."""
        # Empty task_type
        with pytest.raises(ValueError):
            Task(task_type="   ", payload={})
        
        # Invalid priority
        with pytest.raises(ValueError):
            Task(task_type="test", priority=150)
    
    def test_execution_duration(self):
        """Test execution_duration property."""
        started = datetime.utcnow()
        completed = started + timedelta(seconds=5)
        
        task = Task(
            task_type="test",
            status=TaskStatus.COMPLETED,
            started_at=started,
            completed_at=completed
        )
        
        assert task.execution_duration == timedelta(seconds=5)
        
        # No completed_at
        incomplete = Task(task_type="test", started_at=started)
        assert incomplete.execution_duration is None


class TestCronJob:
    """Tests for CronJob model."""
    
    def test_create_cron_job(self):
        """Test basic cron job creation."""
        job = CronJob(
            name="daily_cleanup",
            schedule="0 0 * * *",
            task_type="cleanup"
        )
        
        assert job.name == "daily_cleanup"
        assert job.schedule == "0 0 * * *"
        assert job.task_type == "cleanup"
        assert job.status == CronJobStatus.ENABLED
        assert job.concurrency_policy == ConcurrencyPolicy.ALLOW
    
    def test_cron_job_validate_schedule(self):
        """Test cron schedule validation."""
        # Valid 5-field cron
        job = CronJob(name="test", schedule="0 * * * *", task_type="test")
        assert job.schedule == "0 * * * *"
        
        # Invalid cron (wrong number of fields)
        with pytest.raises(ValueError, match="expected 5 fields"):
            CronJob(name="test", schedule="0 * *", task_type="test")
    
    def test_cron_job_success_rate(self):
        """Test success_rate calculation."""
        job = CronJob(
            name="test",
            schedule="* * * * *",
            task_type="test",
            run_count=100,
            success_count=95,
            failure_count=5
        )
        
        assert job.success_rate == 95.0
        
        # No runs yet
        new_job = CronJob(name="test", schedule="* * * * *", task_type="test")
        assert new_job.success_rate is None
    
    def test_cron_job_create_task(self):
        """Test task creation from cron job."""
        job = CronJob(
            name="test_job",
            schedule="0 * * * *",
            task_type="test_task",
            task_payload={"key": "value"},
            queue_name="cron_queue",
            priority=75,
            max_attempts=5,
            timeout_seconds=600
        )
        
        task = job.create_task()
        
        assert task.task_type == "test_task"
        assert task.payload == {"key": "value"}
        assert task.queue_name == "cron_queue"
        assert task.priority == 75
        assert task.max_attempts == 5
        assert task.timeout_seconds == 600
        assert task.cron_job_id == job.id
        assert task.status == TaskStatus.QUEUED


class TestWorker:
    """Tests for Worker model."""
    
    def test_create_worker(self):
        """Test basic worker creation."""
        worker = Worker(
            name="test-worker:1234",
            hostname="test-worker",
            pid=1234,
            queues=["default", "high-priority"],
            concurrency=10
        )
        
        assert worker.name == "test-worker:1234"
        assert worker.hostname == "test-worker"
        assert worker.pid == 1234
        assert worker.queues == ["default", "high-priority"]
        assert worker.concurrency == 10
        assert worker.status == WorkerStatus.ACTIVE
    
    def test_worker_is_healthy(self):
        """Test is_healthy property."""
        now = datetime.utcnow()
        
        # Healthy worker with recent heartbeat
        healthy = Worker(
            name="test:1",
            hostname="test",
            pid=1,
            last_heartbeat=now,
            heartbeat_interval_seconds=10
        )
        assert healthy.is_healthy
        
        # Unhealthy - stale heartbeat (> 3x interval)
        stale = Worker(
            name="test:2",
            hostname="test",
            pid=2,
            last_heartbeat=now - timedelta(seconds=40),
            heartbeat_interval_seconds=10
        )
        assert not stale.is_healthy
        
        # Unhealthy - not active
        inactive = Worker(
            name="test:3",
            hostname="test",
            pid=3,
            status=WorkerStatus.INACTIVE,
            last_heartbeat=now
        )
        assert not inactive.is_healthy
    
    def test_worker_available_capacity(self):
        """Test available_capacity property."""
        worker = Worker(
            name="test:1",
            hostname="test",
            pid=1,
            concurrency=10,
            active_task_count=3
        )
        
        assert worker.available_capacity == 7
        
        # Full capacity
        full_worker = Worker(
            name="test:2",
            hostname="test",
            pid=2,
            concurrency=10,
            active_task_count=10
        )
        assert full_worker.available_capacity == 0
        
        # Over capacity (shouldn't happen but handle gracefully)
        over_worker = Worker(
            name="test:3",
            hostname="test",
            pid=3,
            concurrency=10,
            active_task_count=12
        )
        assert over_worker.available_capacity == 0


class TestIntegration:
    """Integration tests across models."""
    
    def test_task_workflow(self):
        """Test a typical task workflow through state transitions."""
        # Create task
        task = Task(
            task_type="process_order",
            payload={"order_id": 123},
            priority=80,
            max_attempts=3
        )
        assert task.status == TaskStatus.QUEUED
        
        # Worker claims task
        active_task = task.with_status(TaskStatus.ACTIVE)
        assert active_task.status == TaskStatus.ACTIVE
        assert active_task.started_at is not None
        
        # Task completes successfully
        completed_task = active_task.with_status(TaskStatus.COMPLETED)
        assert completed_task.status == TaskStatus.COMPLETED
        assert completed_task.completed_at is not None
        assert completed_task.is_terminal
    
    def test_task_retry_workflow(self):
        """Test task retry through failure states."""
        task = Task(
            task_type="flaky_task",
            payload={},
            max_attempts=3,
            attempt_count=1  # First attempt
        )
        
        # Move to active
        active = task.with_status(TaskStatus.ACTIVE)
        
        # Fail
        failed = active.with_status(TaskStatus.FAILED)
        assert failed.status == TaskStatus.FAILED
        assert failed.can_retry  # Still have retries
        
        # Retry (back to queued)
        retried = failed.with_status(TaskStatus.QUEUED)
        assert retried.status == TaskStatus.QUEUED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
