"""
Unit Tests for Task Queue
=========================

Tests for the task queue abstraction layer, including:
- Task submission
- Task claiming
- Task completion/failure
- Event handling
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

from queue.task_queue import TaskQueue, TaskQueueError, TaskNotFoundError, TaskStateError
from scheduler.models import Task, TaskStatus


class MockRepository:
    """Mock repository for testing."""
    
    def __init__(self):
        self.tasks = {}
        self.create_task = AsyncMock()
        self.get_task = AsyncMock()
        self.get_tasks = AsyncMock(return_value=[])
        self.claim_tasks = AsyncMock(return_value=[])
        self.complete_task = AsyncMock()
        self.fail_task = AsyncMock()
        self.cancel_task = AsyncMock()
        self.extend_visibility_timeout = AsyncMock(return_value=True)
        self.promote_pending_tasks = AsyncMock(return_value=0)
        self.recover_timed_out_tasks = AsyncMock(return_value=0)
        self.get_queue_stats = AsyncMock(return_value=[])


@pytest.fixture
def mock_repository():
    """Create a mock repository."""
    return MockRepository()


@pytest.fixture
def task_queue(mock_repository):
    """Create a task queue with mock repository."""
    return TaskQueue(mock_repository)


class TestTaskSubmission:
    """Tests for task submission."""
    
    @pytest.mark.asyncio
    async def test_submit_immediate_task(self, task_queue, mock_repository):
        """Test submitting an immediate task."""
        expected_task = Task(
            id=uuid4(),
            task_type="send_email",
            payload={"to": "user@example.com"},
            queue_name="default",
            status=TaskStatus.QUEUED
        )
        mock_repository.create_task.return_value = expected_task
        
        task = await task_queue.submit(
            task_type="send_email",
            payload={"to": "user@example.com"}
        )
        
        assert task.task_type == "send_email"
        mock_repository.create_task.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_submit_scheduled_task(self, task_queue, mock_repository):
        """Test submitting a scheduled task."""
        future_time = datetime.utcnow() + timedelta(hours=1)
        
        expected_task = Task(
            task_type="generate_report",
            payload={"report_id": 123},
            status=TaskStatus.PENDING,
            scheduled_at=future_time
        )
        mock_repository.create_task.return_value = expected_task
        
        task = await task_queue.submit(
            task_type="generate_report",
            payload={"report_id": 123},
            scheduled_at=future_time
        )
        
        mock_repository.create_task.assert_called_once()
        call_kwargs = mock_repository.create_task.call_args
        assert call_kwargs.kwargs.get('scheduled_at') == future_time
    
    @pytest.mark.asyncio
    async def test_submit_with_delay(self, task_queue, mock_repository):
        """Test submitting a task with delay."""
        expected_task = Task(
            task_type="delayed_task",
            payload={},
            status=TaskStatus.PENDING
        )
        mock_repository.create_task.return_value = expected_task
        
        await task_queue.submit(
            task_type="delayed_task",
            payload={},
            delay_seconds=3600  # 1 hour
        )
        
        mock_repository.create_task.assert_called_once()
        call_kwargs = mock_repository.create_task.call_args
        # scheduled_at should be approximately 1 hour from now
        scheduled_at = call_kwargs.kwargs.get('scheduled_at')
        assert scheduled_at is not None
        assert scheduled_at > datetime.utcnow()
    
    @pytest.mark.asyncio
    async def test_submit_with_priority(self, task_queue, mock_repository):
        """Test submitting a task with custom priority."""
        expected_task = Task(
            task_type="urgent_task",
            payload={},
            priority=90
        )
        mock_repository.create_task.return_value = expected_task
        
        await task_queue.submit(
            task_type="urgent_task",
            payload={},
            priority=90
        )
        
        call_kwargs = mock_repository.create_task.call_args
        assert call_kwargs.kwargs.get('priority') == 90
    
    @pytest.mark.asyncio
    async def test_submit_empty_task_type_raises(self, task_queue):
        """Test that empty task type raises error."""
        with pytest.raises(TaskQueueError, match="cannot be empty"):
            await task_queue.submit(task_type="", payload={})
    
    @pytest.mark.asyncio
    async def test_submit_invalid_priority_raises(self, task_queue):
        """Test that invalid priority raises error."""
        with pytest.raises(TaskQueueError, match="priority must be"):
            await task_queue.submit(
                task_type="test",
                payload={},
                priority=150
            )


class TestTaskClaiming:
    """Tests for task claiming."""
    
    @pytest.mark.asyncio
    async def test_claim_tasks(self, task_queue, mock_repository):
        """Test claiming tasks from a queue."""
        worker_id = uuid4()
        claimed_task = Task(
            id=uuid4(),
            task_type="test",
            status=TaskStatus.ACTIVE,
            worker_id=worker_id
        )
        mock_repository.claim_tasks.return_value = [claimed_task]
        
        tasks = await task_queue.claim(
            queue_name="default",
            worker_id=worker_id,
            batch_size=5
        )
        
        assert len(tasks) == 1
        assert tasks[0].status == TaskStatus.ACTIVE
        mock_repository.claim_tasks.assert_called_once_with(
            worker_id=worker_id,
            queue_name="default",
            batch_size=5,
            visibility_timeout_seconds=300
        )
    
    @pytest.mark.asyncio
    async def test_claim_empty_queue(self, task_queue, mock_repository):
        """Test claiming from an empty queue."""
        mock_repository.claim_tasks.return_value = []
        
        tasks = await task_queue.claim(
            queue_name="empty_queue",
            worker_id=uuid4()
        )
        
        assert tasks == []


class TestTaskCompletion:
    """Tests for task completion."""
    
    @pytest.mark.asyncio
    async def test_complete_task(self, task_queue, mock_repository):
        """Test completing a task successfully."""
        task_id = uuid4()
        completed_task = Task(
            id=task_id,
            task_type="test",
            status=TaskStatus.COMPLETED,
            result={"success": True}
        )
        mock_repository.complete_task.return_value = completed_task
        
        task = await task_queue.complete(
            task_id=task_id,
            result={"success": True}
        )
        
        assert task.status == TaskStatus.COMPLETED
        mock_repository.complete_task.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_complete_task_not_found_raises(self, task_queue, mock_repository):
        """Test completing a non-existent task raises error."""
        mock_repository.complete_task.return_value = None
        
        with pytest.raises(TaskStateError):
            await task_queue.complete(task_id=uuid4())
    
    @pytest.mark.asyncio
    async def test_fail_task(self, task_queue, mock_repository):
        """Test failing a task."""
        task_id = uuid4()
        failed_task = Task(
            id=task_id,
            task_type="test",
            status=TaskStatus.FAILED,
            error_message="Something went wrong"
        )
        mock_repository.fail_task.return_value = failed_task
        
        task = await task_queue.fail(
            task_id=task_id,
            error_message="Something went wrong"
        )
        
        assert task.status == TaskStatus.FAILED
    
    @pytest.mark.asyncio
    async def test_fail_task_to_dead_letter(self, task_queue, mock_repository):
        """Test failing a task that moves to dead letter queue."""
        task_id = uuid4()
        dead_task = Task(
            id=task_id,
            task_type="test",
            status=TaskStatus.DEAD,
            error_message="Max retries exceeded"
        )
        mock_repository.fail_task.return_value = dead_task
        
        task = await task_queue.fail(
            task_id=task_id,
            error_message="Max retries exceeded"
        )
        
        assert task.status == TaskStatus.DEAD


class TestTaskCancellation:
    """Tests for task cancellation."""
    
    @pytest.mark.asyncio
    async def test_cancel_task(self, task_queue, mock_repository):
        """Test cancelling a queued task."""
        task_id = uuid4()
        cancelled_task = Task(
            id=task_id,
            task_type="test",
            status=TaskStatus.CANCELLED
        )
        mock_repository.cancel_task.return_value = cancelled_task
        
        task = await task_queue.cancel(task_id=task_id)
        
        assert task.status == TaskStatus.CANCELLED
    
    @pytest.mark.asyncio
    async def test_cancel_active_task_raises(self, task_queue, mock_repository):
        """Test that cancelling an active task raises error."""
        mock_repository.cancel_task.return_value = None
        
        with pytest.raises(TaskStateError):
            await task_queue.cancel(task_id=uuid4())


class TestVisibilityExtension:
    """Tests for visibility timeout extension."""
    
    @pytest.mark.asyncio
    async def test_extend_visibility(self, task_queue, mock_repository):
        """Test extending visibility timeout."""
        task_id = uuid4()
        worker_id = uuid4()
        
        result = await task_queue.extend_visibility(
            task_id=task_id,
            worker_id=worker_id,
            extension_seconds=600
        )
        
        assert result is True
        mock_repository.extend_visibility_timeout.assert_called_once_with(
            task_id=task_id,
            worker_id=worker_id,
            extension_seconds=600
        )
    
    @pytest.mark.asyncio
    async def test_extend_visibility_not_owned(self, task_queue, mock_repository):
        """Test extending visibility for task not owned by worker."""
        mock_repository.extend_visibility_timeout.return_value = False
        
        result = await task_queue.extend_visibility(
            task_id=uuid4(),
            worker_id=uuid4()
        )
        
        assert result is False


class TestTaskQueries:
    """Tests for task queries."""
    
    @pytest.mark.asyncio
    async def test_get_task(self, task_queue, mock_repository):
        """Test getting a task by ID."""
        task_id = uuid4()
        task = Task(id=task_id, task_type="test")
        mock_repository.get_task.return_value = task
        
        result = await task_queue.get(task_id)
        
        assert result.id == task_id
    
    @pytest.mark.asyncio
    async def test_get_task_not_found(self, task_queue, mock_repository):
        """Test getting a non-existent task."""
        mock_repository.get_task.return_value = None
        
        result = await task_queue.get(uuid4())
        
        assert result is None
    
    @pytest.mark.asyncio
    async def test_get_or_raise(self, task_queue, mock_repository):
        """Test get_or_raise with existing task."""
        task_id = uuid4()
        task = Task(id=task_id, task_type="test")
        mock_repository.get_task.return_value = task
        
        result = await task_queue.get_or_raise(task_id)
        
        assert result.id == task_id
    
    @pytest.mark.asyncio
    async def test_get_or_raise_not_found(self, task_queue, mock_repository):
        """Test get_or_raise raises on missing task."""
        mock_repository.get_task.return_value = None
        
        with pytest.raises(TaskNotFoundError):
            await task_queue.get_or_raise(uuid4())


class TestEventListeners:
    """Tests for event listeners."""
    
    @pytest.mark.asyncio
    async def test_event_listener_sync(self, task_queue, mock_repository):
        """Test sync event listener."""
        events = []
        
        def listener(task):
            events.append(("created", task.task_type))
        
        task_queue.on("task_created", listener)
        
        expected_task = Task(task_type="test_event")
        mock_repository.create_task.return_value = expected_task
        
        await task_queue.submit(task_type="test_event", payload={})
        
        assert len(events) == 1
        assert events[0] == ("created", "test_event")
    
    @pytest.mark.asyncio
    async def test_event_listener_async(self, task_queue, mock_repository):
        """Test async event listener."""
        events = []
        
        async def listener(task):
            events.append(("created", task.task_type))
        
        task_queue.on("task_created", listener)
        
        expected_task = Task(task_type="test_event")
        mock_repository.create_task.return_value = expected_task
        
        await task_queue.submit(task_type="test_event", payload={})
        
        assert len(events) == 1


class TestHandlerRegistration:
    """Tests for handler registration."""
    
    def test_register_handler(self, task_queue):
        """Test registering a task handler."""
        def handler(task):
            pass
        
        task_queue.register_handler("test_type", handler)
        
        assert task_queue.get_handler("test_type") is handler
    
    def test_get_handler_not_found(self, task_queue):
        """Test getting a non-existent handler."""
        assert task_queue.get_handler("unknown_type") is None


class TestMaintenance:
    """Tests for maintenance operations."""
    
    @pytest.mark.asyncio
    async def test_promote_pending(self, task_queue, mock_repository):
        """Test promoting pending tasks."""
        mock_repository.promote_pending_tasks.return_value = 5
        
        count = await task_queue.promote_pending()
        
        assert count == 5
    
    @pytest.mark.asyncio
    async def test_recover_timeouts(self, task_queue, mock_repository):
        """Test recovering timed-out tasks."""
        mock_repository.recover_timed_out_tasks.return_value = 3
        
        count = await task_queue.recover_timeouts()
        
        assert count == 3


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
