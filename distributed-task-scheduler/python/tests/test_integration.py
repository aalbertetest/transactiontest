"""
Integration Tests
=================

Integration tests that test the full stack with a real database.
These tests use testcontainers to spin up a PostgreSQL instance.

Note: These tests require Docker to be available.
"""

import asyncio
import pytest
from datetime import datetime, timedelta
from uuid import uuid4

# Try to import testcontainers, skip tests if not available
try:
    from testcontainers.postgres import PostgresContainer
    HAS_TESTCONTAINERS = True
except ImportError:
    HAS_TESTCONTAINERS = False

from config.settings import Settings, DatabaseSettings
from persistence.database import Database
from persistence.repository import TaskRepository
from queue.task_queue import TaskQueue
from scheduler.models import Task, TaskStatus, CronJob


# Skip all tests in this module if testcontainers not available
pytestmark = pytest.mark.skipif(
    not HAS_TESTCONTAINERS,
    reason="testcontainers not installed"
)


@pytest.fixture(scope="module")
def postgres_container():
    """Start a PostgreSQL container for testing."""
    with PostgresContainer("postgres:15") as postgres:
        yield postgres


@pytest.fixture(scope="module")
def db_settings(postgres_container):
    """Get database settings from container."""
    return DatabaseSettings(
        host=postgres_container.get_container_host_ip(),
        port=int(postgres_container.get_exposed_port(5432)),
        name=postgres_container.dbname,
        user=postgres_container.username,
        password=postgres_container.password,
    )


@pytest.fixture(scope="module")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def database(db_settings):
    """Create and connect database."""
    db = Database(db_settings)
    await db.connect()
    
    # Apply schema (simplified for testing)
    schema_sql = """
    -- Create extension
    CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
    
    -- Create types
    DO $$ BEGIN
        CREATE TYPE task_status AS ENUM (
            'PENDING', 'QUEUED', 'ACTIVE', 'COMPLETED', 'FAILED', 'DEAD', 'CANCELLED'
        );
    EXCEPTION WHEN duplicate_object THEN NULL;
    END $$;
    
    -- Create tasks table
    CREATE TABLE IF NOT EXISTS tasks (
        id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
        task_type VARCHAR(255) NOT NULL,
        queue_name VARCHAR(255) NOT NULL DEFAULT 'default',
        status task_status NOT NULL DEFAULT 'QUEUED',
        priority INTEGER NOT NULL DEFAULT 50,
        payload JSONB NOT NULL DEFAULT '{}',
        result JSONB,
        error_message TEXT,
        error_details JSONB,
        idempotency_key VARCHAR(255),
        parent_task_id UUID,
        cron_job_id UUID,
        scheduled_at TIMESTAMP WITH TIME ZONE,
        max_attempts INTEGER NOT NULL DEFAULT 3,
        attempt_count INTEGER NOT NULL DEFAULT 0,
        retry_delay_seconds FLOAT NOT NULL DEFAULT 1.0,
        timeout_seconds INTEGER NOT NULL DEFAULT 300,
        worker_id UUID,
        visibility_timeout TIMESTAMP WITH TIME ZONE,
        version INTEGER NOT NULL DEFAULT 1,
        created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
        queued_at TIMESTAMP WITH TIME ZONE,
        started_at TIMESTAMP WITH TIME ZONE,
        completed_at TIMESTAMP WITH TIME ZONE,
        deleted_at TIMESTAMP WITH TIME ZONE
    );
    
    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks (status);
    CREATE INDEX IF NOT EXISTS idx_tasks_queue ON tasks (queue_name, status);
    
    -- Create claim function
    CREATE OR REPLACE FUNCTION claim_tasks(
        p_worker_id UUID,
        p_queue_name VARCHAR(255),
        p_batch_size INTEGER,
        p_visibility_timeout_seconds INTEGER
    )
    RETURNS SETOF tasks AS $$
    BEGIN
        RETURN QUERY
        WITH claimed AS (
            SELECT t.id
            FROM tasks t
            WHERE t.queue_name = p_queue_name
              AND t.status = 'QUEUED'
              AND (t.scheduled_at IS NULL OR t.scheduled_at <= NOW())
              AND t.deleted_at IS NULL
            ORDER BY t.priority DESC, t.created_at ASC
            LIMIT p_batch_size
            FOR UPDATE SKIP LOCKED
        )
        UPDATE tasks
        SET status = 'ACTIVE',
            worker_id = p_worker_id,
            started_at = NOW(),
            attempt_count = attempt_count + 1,
            visibility_timeout = NOW() + (p_visibility_timeout_seconds || ' seconds')::INTERVAL,
            version = version + 1
        WHERE id IN (SELECT id FROM claimed)
        RETURNING *;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Create promote function
    CREATE OR REPLACE FUNCTION promote_pending_tasks()
    RETURNS INTEGER AS $$
    DECLARE
        promoted_count INTEGER;
    BEGIN
        WITH promoted AS (
            UPDATE tasks
            SET status = 'QUEUED',
                queued_at = NOW(),
                version = version + 1
            WHERE status = 'PENDING'
              AND scheduled_at <= NOW()
              AND deleted_at IS NULL
            RETURNING id
        )
        SELECT COUNT(*) INTO promoted_count FROM promoted;
        RETURN promoted_count;
    END;
    $$ LANGUAGE plpgsql;
    
    -- Create recovery function
    CREATE OR REPLACE FUNCTION recover_timed_out_tasks()
    RETURNS INTEGER AS $$
    DECLARE
        recovered_count INTEGER;
    BEGIN
        WITH recovered AS (
            UPDATE tasks
            SET status = CASE
                    WHEN attempt_count >= max_attempts THEN 'DEAD'::task_status
                    ELSE 'QUEUED'::task_status
                END,
                worker_id = NULL,
                visibility_timeout = NULL,
                error_message = COALESCE(error_message, 'Visibility timeout exceeded'),
                version = version + 1
            WHERE status = 'ACTIVE'
              AND visibility_timeout < NOW()
              AND deleted_at IS NULL
            RETURNING id
        )
        SELECT COUNT(*) INTO recovered_count FROM recovered;
        RETURN recovered_count;
    END;
    $$ LANGUAGE plpgsql;
    """
    
    async with db.acquire() as conn:
        await conn.execute(schema_sql)
    
    yield db
    
    # Cleanup
    async with db.acquire() as conn:
        await conn.execute("DROP TABLE IF EXISTS tasks CASCADE")
    
    await db.disconnect()


@pytest.fixture
def repository(database):
    """Create repository with database."""
    return TaskRepository(database)


@pytest.fixture
def task_queue(repository):
    """Create task queue with repository."""
    return TaskQueue(repository)


class TestDatabaseIntegration:
    """Integration tests for database operations."""
    
    @pytest.mark.asyncio
    async def test_create_and_get_task(self, repository):
        """Test creating and retrieving a task."""
        task = await repository.create_task(
            task_type="integration_test",
            payload={"key": "value"},
            queue_name="test_queue",
            priority=75
        )
        
        assert task.id is not None
        assert task.task_type == "integration_test"
        assert task.status == TaskStatus.QUEUED
        
        # Retrieve the task
        retrieved = await repository.get_task(task.id)
        
        assert retrieved is not None
        assert retrieved.id == task.id
        assert retrieved.payload == {"key": "value"}
    
    @pytest.mark.asyncio
    async def test_claim_task(self, repository):
        """Test claiming a task."""
        # Create a task
        task = await repository.create_task(
            task_type="claim_test",
            payload={},
            queue_name="claim_queue"
        )
        
        worker_id = uuid4()
        
        # Claim the task
        claimed = await repository.claim_tasks(
            worker_id=worker_id,
            queue_name="claim_queue",
            batch_size=1,
            visibility_timeout_seconds=300
        )
        
        assert len(claimed) == 1
        assert claimed[0].id == task.id
        assert claimed[0].status == TaskStatus.ACTIVE
        assert claimed[0].worker_id == worker_id
        assert claimed[0].attempt_count == 1
    
    @pytest.mark.asyncio
    async def test_claim_respects_priority(self, repository):
        """Test that claiming respects priority order."""
        # Create tasks with different priorities
        low_priority = await repository.create_task(
            task_type="priority_test",
            payload={"priority": "low"},
            queue_name="priority_queue",
            priority=10
        )
        
        high_priority = await repository.create_task(
            task_type="priority_test",
            payload={"priority": "high"},
            queue_name="priority_queue",
            priority=90
        )
        
        medium_priority = await repository.create_task(
            task_type="priority_test",
            payload={"priority": "medium"},
            queue_name="priority_queue",
            priority=50
        )
        
        worker_id = uuid4()
        
        # Claim one task at a time
        first = await repository.claim_tasks(
            worker_id=worker_id,
            queue_name="priority_queue",
            batch_size=1,
            visibility_timeout_seconds=300
        )
        
        assert first[0].id == high_priority.id
        
        second = await repository.claim_tasks(
            worker_id=worker_id,
            queue_name="priority_queue",
            batch_size=1,
            visibility_timeout_seconds=300
        )
        
        assert second[0].id == medium_priority.id
    
    @pytest.mark.asyncio
    async def test_complete_task(self, repository):
        """Test completing a task."""
        task = await repository.create_task(
            task_type="complete_test",
            payload={},
            queue_name="complete_queue"
        )
        
        worker_id = uuid4()
        
        # Claim the task
        claimed = await repository.claim_tasks(
            worker_id=worker_id,
            queue_name="complete_queue",
            batch_size=1,
            visibility_timeout_seconds=300
        )
        
        # Complete the task
        completed = await repository.complete_task(
            task_id=claimed[0].id,
            result={"output": "success"}
        )
        
        assert completed is not None
        assert completed.status == TaskStatus.COMPLETED
        assert completed.result == {"output": "success"}
        assert completed.completed_at is not None
    
    @pytest.mark.asyncio
    async def test_fail_and_retry_task(self, repository):
        """Test failing a task that gets retried."""
        task = await repository.create_task(
            task_type="retry_test",
            payload={},
            queue_name="retry_queue",
            max_attempts=3
        )
        
        worker_id = uuid4()
        
        # Claim the task
        claimed = await repository.claim_tasks(
            worker_id=worker_id,
            queue_name="retry_queue",
            batch_size=1,
            visibility_timeout_seconds=300
        )
        
        # Fail the task (should be re-queued since max_attempts=3)
        failed = await repository.fail_task(
            task_id=claimed[0].id,
            error_message="First attempt failed"
        )
        
        assert failed is not None
        assert failed.status == TaskStatus.QUEUED  # Re-queued for retry
        assert failed.error_message == "First attempt failed"
    
    @pytest.mark.asyncio
    async def test_fail_to_dead_letter(self, repository):
        """Test failing a task that goes to dead letter."""
        task = await repository.create_task(
            task_type="dead_letter_test",
            payload={},
            queue_name="dead_letter_queue",
            max_attempts=1  # No retries
        )
        
        worker_id = uuid4()
        
        # Claim the task
        claimed = await repository.claim_tasks(
            worker_id=worker_id,
            queue_name="dead_letter_queue",
            batch_size=1,
            visibility_timeout_seconds=300
        )
        
        # Fail the task (should go to DEAD since max_attempts=1)
        failed = await repository.fail_task(
            task_id=claimed[0].id,
            error_message="Permanent failure"
        )
        
        assert failed is not None
        assert failed.status == TaskStatus.DEAD


class TestTaskQueueIntegration:
    """Integration tests for task queue."""
    
    @pytest.mark.asyncio
    async def test_submit_and_claim_workflow(self, task_queue):
        """Test full submit and claim workflow."""
        # Submit a task
        task = await task_queue.submit(
            task_type="workflow_test",
            payload={"step": 1},
            queue_name="workflow_queue",
            priority=60
        )
        
        assert task.status == TaskStatus.QUEUED
        
        worker_id = uuid4()
        
        # Claim the task
        claimed = await task_queue.claim(
            queue_name="workflow_queue",
            worker_id=worker_id,
            batch_size=1
        )
        
        assert len(claimed) == 1
        assert claimed[0].id == task.id
        assert claimed[0].status == TaskStatus.ACTIVE
    
    @pytest.mark.asyncio
    async def test_idempotent_submission(self, task_queue):
        """Test idempotent task submission."""
        idempotency_key = f"idem_{uuid4()}"
        
        # Submit first task
        task1 = await task_queue.submit(
            task_type="idempotent_test",
            payload={"attempt": 1},
            idempotency_key=idempotency_key
        )
        
        # Submit duplicate
        task2 = await task_queue.submit(
            task_type="idempotent_test",
            payload={"attempt": 2},  # Different payload
            idempotency_key=idempotency_key
        )
        
        # Should return the same task
        assert task1.id == task2.id
    
    @pytest.mark.asyncio
    async def test_complete_task_workflow(self, task_queue):
        """Test complete task workflow."""
        task = await task_queue.submit(
            task_type="complete_workflow",
            payload={},
            queue_name="complete_workflow_queue"
        )
        
        worker_id = uuid4()
        
        # Claim
        claimed = await task_queue.claim(
            queue_name="complete_workflow_queue",
            worker_id=worker_id
        )
        
        # Complete
        completed = await task_queue.complete(
            task_id=claimed[0].id,
            result={"status": "done"}
        )
        
        assert completed.status == TaskStatus.COMPLETED
        
        # Verify cannot be claimed again
        empty = await task_queue.claim(
            queue_name="complete_workflow_queue",
            worker_id=worker_id
        )
        
        assert len(empty) == 0


class TestConcurrencyIntegration:
    """Integration tests for concurrent operations."""
    
    @pytest.mark.asyncio
    async def test_concurrent_claims(self, task_queue):
        """Test that concurrent claims don't cause double-claiming."""
        # Create multiple tasks
        tasks = []
        for i in range(10):
            task = await task_queue.submit(
                task_type="concurrent_test",
                payload={"index": i},
                queue_name="concurrent_queue"
            )
            tasks.append(task)
        
        # Simulate multiple workers claiming concurrently
        async def claim_tasks(worker_num):
            worker_id = uuid4()
            claimed = await task_queue.claim(
                queue_name="concurrent_queue",
                worker_id=worker_id,
                batch_size=5
            )
            return claimed
        
        # Run 5 concurrent claim operations
        results = await asyncio.gather(*[
            claim_tasks(i) for i in range(5)
        ])
        
        # Collect all claimed task IDs
        all_claimed_ids = []
        for claimed in results:
            all_claimed_ids.extend([t.id for t in claimed])
        
        # No task should be claimed twice
        assert len(all_claimed_ids) == len(set(all_claimed_ids))
        
        # All tasks should be claimed
        assert len(all_claimed_ids) == 10


class TestFailureSimulation:
    """Tests that simulate various failure scenarios."""
    
    @pytest.mark.asyncio
    async def test_worker_timeout_recovery(self, task_queue, repository):
        """Test recovery of tasks from timed-out workers."""
        # Create a task
        task = await task_queue.submit(
            task_type="timeout_test",
            payload={},
            queue_name="timeout_queue"
        )
        
        worker_id = uuid4()
        
        # Claim with very short visibility timeout
        claimed = await repository.claim_tasks(
            worker_id=worker_id,
            queue_name="timeout_queue",
            batch_size=1,
            visibility_timeout_seconds=1  # 1 second timeout
        )
        
        assert len(claimed) == 1
        assert claimed[0].status == TaskStatus.ACTIVE
        
        # Wait for timeout
        await asyncio.sleep(2)
        
        # Run recovery
        recovered = await repository.recover_timed_out_tasks()
        
        assert recovered == 1
        
        # Task should be re-queued
        retrieved = await repository.get_task(task.id)
        assert retrieved.status == TaskStatus.QUEUED


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
