-- ============================================================================
-- DISTRIBUTED TASK SCHEDULER - DATABASE SCHEMA
-- ============================================================================
-- This schema provides the persistence layer for a production-grade
-- distributed task scheduling system. It supports:
--   - Task definitions and execution tracking
--   - Cron job scheduling
--   - Worker registration and health monitoring
--   - Leader election for scheduler HA
--   - Distributed locking
--
-- Database: PostgreSQL 13+
-- ============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- For UUID generation
CREATE EXTENSION IF NOT EXISTS "pg_trgm";        -- For text search optimization

-- ============================================================================
-- ENUM TYPES
-- ============================================================================

-- Task status represents the current state of a task in its lifecycle.
-- See README for full state transition diagram.
CREATE TYPE task_status AS ENUM (
    'PENDING',      -- Created but scheduled for future execution
    'QUEUED',       -- Ready for immediate execution, waiting for worker
    'ACTIVE',       -- Currently being executed by a worker
    'COMPLETED',    -- Successfully finished
    'FAILED',       -- Execution failed (may be retried)
    'DEAD',         -- Exceeded retry limit, in dead letter queue
    'CANCELLED'     -- Manually cancelled before execution
);

-- Worker status represents the health state of a worker node.
CREATE TYPE worker_status AS ENUM (
    'ACTIVE',       -- Worker is healthy and processing tasks
    'DRAINING',     -- Worker is stopping, finishing current tasks
    'INACTIVE'      -- Worker is offline or unhealthy
);

-- Cron job status
CREATE TYPE cron_job_status AS ENUM (
    'ENABLED',      -- Job is active and will create tasks on schedule
    'DISABLED',     -- Job is paused, no new tasks will be created
    'DELETED'       -- Soft-deleted, preserved for history
);

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- TASKS TABLE
-- ----------------------------------------------------------------------------
-- The tasks table is the central table storing all task instances.
-- Each row represents a single execution of a task (or scheduled execution).
--
-- DESIGN DECISIONS:
-- 1. UUID primary key for distributed ID generation without coordination
-- 2. JSONB for payload/result to support arbitrary task data
-- 3. Separate columns for common query fields (status, priority, etc.)
-- 4. Version column for optimistic locking
-- 5. Comprehensive timestamps for debugging and metrics
-- ----------------------------------------------------------------------------
CREATE TABLE tasks (
    -- Primary identifier - UUID for distributed generation
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Task type determines which handler processes this task
    -- Examples: 'send_email', 'process_payment', 'generate_report'
    task_type VARCHAR(255) NOT NULL,
    
    -- Queue name for routing tasks to specific worker pools
    -- Allows separating tasks by priority, resource requirements, etc.
    queue_name VARCHAR(255) NOT NULL DEFAULT 'default',
    
    -- Current task status (see task_status enum)
    status task_status NOT NULL DEFAULT 'QUEUED',
    
    -- Task priority (0-100, higher = more important)
    -- Tasks are dequeued in priority order, then by scheduled_at, then created_at
    priority INTEGER NOT NULL DEFAULT 50 CHECK (priority >= 0 AND priority <= 100),
    
    -- Arbitrary task payload as JSON
    -- Contains all data needed by the task handler
    payload JSONB NOT NULL DEFAULT '{}',
    
    -- Task result (set on completion)
    -- Contains output data from successful execution
    result JSONB,
    
    -- Error information (set on failure)
    error_message TEXT,
    error_details JSONB,
    
    -- Idempotency key for deduplication
    -- If set, prevents duplicate task creation with same key
    idempotency_key VARCHAR(255),
    
    -- Parent task ID for task chaining/dependencies
    parent_task_id UUID REFERENCES tasks(id),
    
    -- Cron job ID if this task was created by a cron job
    cron_job_id UUID,  -- Foreign key added after cron_jobs table
    
    -- Scheduling
    -- scheduled_at: When the task should be executed (NULL = immediate)
    -- If scheduled_at > NOW(), task stays in PENDING until that time
    scheduled_at TIMESTAMP WITH TIME ZONE,
    
    -- Retry configuration
    max_attempts INTEGER NOT NULL DEFAULT 3,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    retry_delay_seconds FLOAT NOT NULL DEFAULT 1.0,
    
    -- Execution timeout in seconds
    timeout_seconds INTEGER NOT NULL DEFAULT 300,
    
    -- Worker assignment
    -- worker_id: Which worker is processing this task
    -- visibility_timeout: When task becomes visible again if not completed
    worker_id UUID,
    visibility_timeout TIMESTAMP WITH TIME ZONE,
    
    -- Optimistic locking version
    version INTEGER NOT NULL DEFAULT 1,
    
    -- Timestamps for lifecycle tracking
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    queued_at TIMESTAMP WITH TIME ZONE,          -- When task entered QUEUED
    started_at TIMESTAMP WITH TIME ZONE,          -- When worker started execution
    completed_at TIMESTAMP WITH TIME ZONE,        -- When task finished (success/fail/dead)
    
    -- Soft delete support
    deleted_at TIMESTAMP WITH TIME ZONE
);

-- ----------------------------------------------------------------------------
-- CRON_JOBS TABLE
-- ----------------------------------------------------------------------------
-- Stores cron job definitions. Each cron job creates task instances
-- according to its schedule.
--
-- DESIGN DECISIONS:
-- 1. Separate from tasks table for clean separation of concerns
-- 2. Stores next_run_at for efficient scheduling queries
-- 3. last_run_at and run_count for monitoring
-- 4. Concurrency policy controls overlapping execution handling
-- ----------------------------------------------------------------------------
CREATE TABLE cron_jobs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Human-readable job name (must be unique)
    name VARCHAR(255) NOT NULL UNIQUE,
    
    -- Description for documentation
    description TEXT,
    
    -- Cron schedule expression (standard 5-field: min hour day month weekday)
    -- Examples: "0 * * * *" (hourly), "0 0 * * *" (daily midnight)
    schedule VARCHAR(100) NOT NULL,
    
    -- Timezone for schedule evaluation (default UTC)
    timezone VARCHAR(50) NOT NULL DEFAULT 'UTC',
    
    -- Task configuration - what task to create
    task_type VARCHAR(255) NOT NULL,
    task_payload JSONB NOT NULL DEFAULT '{}',
    queue_name VARCHAR(255) NOT NULL DEFAULT 'default',
    priority INTEGER NOT NULL DEFAULT 50 CHECK (priority >= 0 AND priority <= 100),
    
    -- Retry configuration for created tasks
    max_attempts INTEGER NOT NULL DEFAULT 3,
    timeout_seconds INTEGER NOT NULL DEFAULT 300,
    
    -- Job status
    status cron_job_status NOT NULL DEFAULT 'ENABLED',
    
    -- Scheduling state
    next_run_at TIMESTAMP WITH TIME ZONE,
    last_run_at TIMESTAMP WITH TIME ZONE,
    
    -- Statistics
    run_count BIGINT NOT NULL DEFAULT 0,
    success_count BIGINT NOT NULL DEFAULT 0,
    failure_count BIGINT NOT NULL DEFAULT 0,
    
    -- Concurrency policy: what to do if previous run is still executing
    -- 'ALLOW': Create new task regardless (default)
    -- 'FORBID': Skip this run if previous is still active
    -- 'REPLACE': Cancel previous and start new
    concurrency_policy VARCHAR(20) NOT NULL DEFAULT 'ALLOW' 
        CHECK (concurrency_policy IN ('ALLOW', 'FORBID', 'REPLACE')),
    
    -- Timestamps
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    -- Metadata for extensibility
    metadata JSONB NOT NULL DEFAULT '{}'
);

-- Add foreign key from tasks to cron_jobs
ALTER TABLE tasks ADD CONSTRAINT fk_tasks_cron_job 
    FOREIGN KEY (cron_job_id) REFERENCES cron_jobs(id);

-- ----------------------------------------------------------------------------
-- WORKERS TABLE
-- ----------------------------------------------------------------------------
-- Tracks registered worker nodes and their health status.
--
-- DESIGN DECISIONS:
-- 1. Workers self-register on startup
-- 2. Heartbeats update last_heartbeat timestamp
-- 3. Workers with stale heartbeats are marked INACTIVE
-- 4. Stores resource information for intelligent task routing
-- ----------------------------------------------------------------------------
CREATE TABLE workers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- Human-readable identifier (hostname:pid)
    name VARCHAR(255) NOT NULL,
    
    -- Network location
    hostname VARCHAR(255) NOT NULL,
    ip_address INET,
    port INTEGER,
    
    -- Process information
    pid INTEGER NOT NULL,
    
    -- Worker configuration
    queues VARCHAR(255)[] NOT NULL DEFAULT ARRAY['default'],
    concurrency INTEGER NOT NULL DEFAULT 10,
    
    -- Current status
    status worker_status NOT NULL DEFAULT 'ACTIVE',
    
    -- Resource tracking
    active_task_count INTEGER NOT NULL DEFAULT 0,
    cpu_usage FLOAT,
    memory_usage FLOAT,
    
    -- Heartbeat tracking
    last_heartbeat TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    heartbeat_interval_seconds INTEGER NOT NULL DEFAULT 10,
    
    -- Lifecycle timestamps
    started_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    stopped_at TIMESTAMP WITH TIME ZONE,
    
    -- Version of worker software (for compatibility checks)
    version VARCHAR(50),
    
    -- Metadata
    metadata JSONB NOT NULL DEFAULT '{}'
);

-- ----------------------------------------------------------------------------
-- SCHEDULER_LOCKS TABLE
-- ----------------------------------------------------------------------------
-- Implements distributed locks for leader election and coordination.
-- Uses a simple lease-based approach with TTL.
--
-- DESIGN DECISIONS:
-- 1. Named locks allow multiple independent lock types
-- 2. TTL-based expiration for automatic cleanup on crashes
-- 3. Simple UPDATE-based acquisition with conflict handling
-- ----------------------------------------------------------------------------
CREATE TABLE scheduler_locks (
    -- Lock name (e.g., 'cron_leader', 'migration')
    lock_name VARCHAR(255) PRIMARY KEY,
    
    -- Who currently holds the lock
    holder_id UUID NOT NULL,
    holder_name VARCHAR(255),
    
    -- When the lock was acquired
    acquired_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    
    -- When the lock expires (holder must renew before this)
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL,
    
    -- Metadata about the lock holder
    metadata JSONB NOT NULL DEFAULT '{}'
);

-- ----------------------------------------------------------------------------
-- TASK_RESULTS TABLE
-- ----------------------------------------------------------------------------
-- Stores detailed task execution results for completed tasks.
-- Separated from tasks table to keep the hot tasks table smaller.
--
-- DESIGN DECISIONS:
-- 1. Separate table for large results (can be archived independently)
-- 2. Stores full execution trace for debugging
-- 3. Can be partitioned by completion date for easy cleanup
-- ----------------------------------------------------------------------------
CREATE TABLE task_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    task_id UUID NOT NULL REFERENCES tasks(id),
    
    -- Worker that executed
    worker_id UUID REFERENCES workers(id),
    
    -- Execution attempt number
    attempt_number INTEGER NOT NULL,
    
    -- Execution status for this attempt
    success BOOLEAN NOT NULL,
    
    -- Result or error
    result JSONB,
    error_message TEXT,
    error_type VARCHAR(255),
    error_traceback TEXT,
    
    -- Timing
    started_at TIMESTAMP WITH TIME ZONE NOT NULL,
    completed_at TIMESTAMP WITH TIME ZONE NOT NULL,
    duration_ms INTEGER NOT NULL,
    
    -- Resource usage
    cpu_time_ms INTEGER,
    memory_peak_mb INTEGER,
    
    -- Logs and traces
    logs TEXT,
    
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- TASK_EVENTS TABLE
-- ----------------------------------------------------------------------------
-- Audit log of all task state transitions for debugging and compliance.
--
-- DESIGN DECISIONS:
-- 1. Append-only table for audit trail
-- 2. Captures all state transitions with context
-- 3. Can be used for event sourcing if needed
-- ----------------------------------------------------------------------------
CREATE TABLE task_events (
    id BIGSERIAL PRIMARY KEY,
    task_id UUID NOT NULL,  -- No FK for performance, task might be deleted
    
    -- Event type (state transition or action)
    event_type VARCHAR(50) NOT NULL,
    
    -- State transition
    from_status task_status,
    to_status task_status,
    
    -- Who triggered the event
    triggered_by VARCHAR(255),  -- 'scheduler', 'worker:<id>', 'api', 'system'
    
    -- Additional context
    details JSONB NOT NULL DEFAULT '{}',
    
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- ============================================================================
-- INDEXES
-- ============================================================================
-- Index strategy optimizes for common query patterns:
-- 1. Dequeuing tasks by status, priority, and schedule
-- 2. Finding tasks by idempotency key
-- 3. Monitoring worker health
-- 4. Cron job scheduling
-- ============================================================================

-- TASKS INDEXES

-- Primary dequeue index: finds queued tasks ordered by priority and time
-- This is the most critical index for system performance
CREATE INDEX idx_tasks_dequeue ON tasks (
    queue_name,
    status,
    priority DESC,
    scheduled_at ASC NULLS FIRST,
    created_at ASC
) WHERE status = 'QUEUED' AND deleted_at IS NULL;

-- Index for finding tasks by status (for monitoring dashboards)
CREATE INDEX idx_tasks_status ON tasks (status, created_at DESC)
    WHERE deleted_at IS NULL;

-- Index for visibility timeout recovery (find tasks that timed out)
CREATE INDEX idx_tasks_visibility_timeout ON tasks (visibility_timeout)
    WHERE status = 'ACTIVE' AND deleted_at IS NULL;

-- Index for idempotency key lookups
CREATE UNIQUE INDEX idx_tasks_idempotency_key ON tasks (idempotency_key)
    WHERE idempotency_key IS NOT NULL AND deleted_at IS NULL
    AND status NOT IN ('FAILED', 'DEAD', 'CANCELLED');

-- Index for finding tasks by worker (for worker crash recovery)
CREATE INDEX idx_tasks_worker ON tasks (worker_id)
    WHERE status = 'ACTIVE' AND deleted_at IS NULL;

-- Index for cron job task lookups
CREATE INDEX idx_tasks_cron_job ON tasks (cron_job_id, created_at DESC)
    WHERE cron_job_id IS NOT NULL;

-- Index for parent-child task relationships
CREATE INDEX idx_tasks_parent ON tasks (parent_task_id)
    WHERE parent_task_id IS NOT NULL;

-- Index for scheduled tasks promotion
CREATE INDEX idx_tasks_scheduled ON tasks (scheduled_at)
    WHERE status = 'PENDING' AND scheduled_at IS NOT NULL AND deleted_at IS NULL;

-- CRON_JOBS INDEXES

-- Index for finding jobs due for execution
CREATE INDEX idx_cron_jobs_next_run ON cron_jobs (next_run_at)
    WHERE status = 'ENABLED' AND deleted_at IS NULL;

-- WORKERS INDEXES

-- Index for finding active workers
CREATE INDEX idx_workers_status ON workers (status, last_heartbeat DESC)
    WHERE status = 'ACTIVE';

-- Index for heartbeat timeout detection
CREATE INDEX idx_workers_heartbeat ON workers (last_heartbeat)
    WHERE status = 'ACTIVE';

-- TASK_RESULTS INDEXES

-- Index for finding results by task
CREATE INDEX idx_task_results_task ON task_results (task_id, attempt_number);

-- TASK_EVENTS INDEXES

-- Index for event history by task
CREATE INDEX idx_task_events_task ON task_events (task_id, created_at);

-- Index for event type queries (for monitoring specific events)
CREATE INDEX idx_task_events_type ON task_events (event_type, created_at DESC);

-- ============================================================================
-- FUNCTIONS AND TRIGGERS
-- ============================================================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at trigger to relevant tables
CREATE TRIGGER tasks_updated_at
    BEFORE UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER cron_jobs_updated_at
    BEFORE UPDATE ON cron_jobs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Function to create task event on status change
CREATE OR REPLACE FUNCTION create_task_status_event()
RETURNS TRIGGER AS $$
BEGIN
    IF OLD.status IS DISTINCT FROM NEW.status THEN
        INSERT INTO task_events (task_id, event_type, from_status, to_status, triggered_by, details)
        VALUES (
            NEW.id,
            'STATUS_CHANGE',
            OLD.status,
            NEW.status,
            COALESCE(current_setting('app.current_user', true), 'system'),
            jsonb_build_object(
                'worker_id', NEW.worker_id,
                'attempt_count', NEW.attempt_count,
                'version', NEW.version
            )
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER tasks_status_event
    AFTER UPDATE ON tasks
    FOR EACH ROW
    EXECUTE FUNCTION create_task_status_event();

-- Function to claim tasks atomically
-- This function is the core of task dequeuing
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
        ORDER BY t.priority DESC, t.scheduled_at ASC NULLS FIRST, t.created_at ASC
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

-- Function to promote pending tasks to queued
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

-- Function to recover timed out tasks
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
            error_message = CASE
                WHEN error_message IS NULL THEN 'Visibility timeout exceeded'
                ELSE error_message
            END,
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

-- Function to try acquiring a distributed lock
CREATE OR REPLACE FUNCTION try_acquire_lock(
    p_lock_name VARCHAR(255),
    p_holder_id UUID,
    p_holder_name VARCHAR(255),
    p_ttl_seconds INTEGER
)
RETURNS BOOLEAN AS $$
DECLARE
    acquired BOOLEAN;
BEGIN
    -- Try to insert new lock or update expired lock
    INSERT INTO scheduler_locks (lock_name, holder_id, holder_name, expires_at)
    VALUES (p_lock_name, p_holder_id, p_holder_name, NOW() + (p_ttl_seconds || ' seconds')::INTERVAL)
    ON CONFLICT (lock_name) DO UPDATE
    SET holder_id = p_holder_id,
        holder_name = p_holder_name,
        acquired_at = NOW(),
        expires_at = NOW() + (p_ttl_seconds || ' seconds')::INTERVAL
    WHERE scheduler_locks.expires_at < NOW()  -- Only take over expired locks
       OR scheduler_locks.holder_id = p_holder_id;  -- Or renew own lock
    
    -- Check if we hold the lock
    SELECT EXISTS(
        SELECT 1 FROM scheduler_locks
        WHERE lock_name = p_lock_name AND holder_id = p_holder_id
    ) INTO acquired;
    
    RETURN acquired;
END;
$$ LANGUAGE plpgsql;

-- Function to release a distributed lock
CREATE OR REPLACE FUNCTION release_lock(
    p_lock_name VARCHAR(255),
    p_holder_id UUID
)
RETURNS BOOLEAN AS $$
DECLARE
    released BOOLEAN;
BEGIN
    DELETE FROM scheduler_locks
    WHERE lock_name = p_lock_name AND holder_id = p_holder_id;
    
    GET DIAGNOSTICS released = ROW_COUNT;
    RETURN released > 0;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- EXAMPLE DATA
-- ============================================================================
-- Insert some example data for testing and demonstration

-- Example cron job: Daily cleanup at midnight
INSERT INTO cron_jobs (
    id, name, description, schedule, task_type, task_payload,
    queue_name, priority, max_attempts, timeout_seconds, next_run_at
) VALUES (
    'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11',
    'daily_cleanup',
    'Clean up old records and temporary files',
    '0 0 * * *',
    'cleanup',
    '{"max_age_days": 30, "tables": ["task_events", "task_results"]}',
    'maintenance',
    30,
    3,
    3600,
    (CURRENT_DATE + INTERVAL '1 day')::TIMESTAMP WITH TIME ZONE
);

-- Example cron job: Hourly metrics aggregation
INSERT INTO cron_jobs (
    id, name, description, schedule, task_type, task_payload,
    queue_name, priority, max_attempts, timeout_seconds, next_run_at
) VALUES (
    'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a22',
    'hourly_metrics',
    'Aggregate metrics data for dashboards',
    '0 * * * *',
    'aggregate_metrics',
    '{"granularity": "1h", "metrics": ["task_count", "error_rate", "duration"]}',
    'analytics',
    40,
    3,
    600,
    DATE_TRUNC('hour', NOW()) + INTERVAL '1 hour'
);

-- Example pending task
INSERT INTO tasks (
    id, task_type, queue_name, status, priority, payload,
    scheduled_at, max_attempts, timeout_seconds
) VALUES (
    'c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a33',
    'send_email',
    'default',
    'PENDING',
    60,
    '{"to": "user@example.com", "subject": "Welcome!", "template": "welcome"}',
    NOW() + INTERVAL '1 hour',
    3,
    60
);

-- Example queued task with idempotency key
INSERT INTO tasks (
    id, task_type, queue_name, status, priority, payload,
    idempotency_key, max_attempts, timeout_seconds, queued_at
) VALUES (
    'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a44',
    'process_payment',
    'high-priority',
    'QUEUED',
    90,
    '{"order_id": "ord_12345", "amount": 99.99, "currency": "USD"}',
    'payment_ord_12345',
    5,
    120,
    NOW()
);

-- Example failed task in retry
INSERT INTO tasks (
    id, task_type, queue_name, status, priority, payload,
    error_message, attempt_count, max_attempts, timeout_seconds
) VALUES (
    'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a55',
    'send_webhook',
    'default',
    'QUEUED',
    50,
    '{"url": "https://api.example.com/webhook", "event": "order.created"}',
    'Connection timeout after 30 seconds',
    2,
    5,
    30
);

-- ============================================================================
-- VIEWS
-- ============================================================================
-- Useful views for monitoring and debugging

-- View: Task queue summary by queue and status
CREATE VIEW v_queue_summary AS
SELECT
    queue_name,
    status,
    COUNT(*) as task_count,
    MIN(created_at) as oldest_task,
    MAX(created_at) as newest_task,
    AVG(priority) as avg_priority
FROM tasks
WHERE deleted_at IS NULL
GROUP BY queue_name, status
ORDER BY queue_name, status;

-- View: Worker status summary
CREATE VIEW v_worker_summary AS
SELECT
    w.id,
    w.name,
    w.hostname,
    w.status,
    w.concurrency,
    w.active_task_count,
    w.last_heartbeat,
    EXTRACT(EPOCH FROM (NOW() - w.last_heartbeat)) as seconds_since_heartbeat,
    w.queues
FROM workers w
WHERE w.status = 'ACTIVE'
ORDER BY w.last_heartbeat DESC;

-- View: Cron job status with next and last run times
CREATE VIEW v_cron_job_status AS
SELECT
    c.id,
    c.name,
    c.schedule,
    c.status,
    c.next_run_at,
    c.last_run_at,
    c.run_count,
    c.success_count,
    c.failure_count,
    ROUND(c.success_count::NUMERIC / NULLIF(c.run_count, 0) * 100, 2) as success_rate,
    c.task_type
FROM cron_jobs c
WHERE c.deleted_at IS NULL
ORDER BY c.next_run_at ASC NULLS LAST;

-- View: Task processing statistics by task type
CREATE VIEW v_task_stats AS
SELECT
    task_type,
    queue_name,
    COUNT(*) FILTER (WHERE status = 'QUEUED') as queued,
    COUNT(*) FILTER (WHERE status = 'ACTIVE') as active,
    COUNT(*) FILTER (WHERE status = 'COMPLETED') as completed,
    COUNT(*) FILTER (WHERE status = 'FAILED') as failed,
    COUNT(*) FILTER (WHERE status = 'DEAD') as dead,
    AVG(EXTRACT(EPOCH FROM (completed_at - started_at))) FILTER (WHERE status = 'COMPLETED') as avg_duration_seconds
FROM tasks
WHERE deleted_at IS NULL
  AND created_at > NOW() - INTERVAL '24 hours'
GROUP BY task_type, queue_name
ORDER BY queued DESC;

-- ============================================================================
-- COMMENTS
-- ============================================================================
-- Add documentation comments to tables and columns

COMMENT ON TABLE tasks IS 'Core table storing all task instances for the distributed task scheduler';
COMMENT ON COLUMN tasks.task_type IS 'Task type identifier that determines which handler processes this task';
COMMENT ON COLUMN tasks.queue_name IS 'Queue name for routing tasks to specific worker pools';
COMMENT ON COLUMN tasks.status IS 'Current task lifecycle state';
COMMENT ON COLUMN tasks.priority IS 'Task priority 0-100, higher values are processed first';
COMMENT ON COLUMN tasks.visibility_timeout IS 'Timestamp when task becomes visible again if worker fails to complete';
COMMENT ON COLUMN tasks.idempotency_key IS 'Optional key to prevent duplicate task creation';

COMMENT ON TABLE cron_jobs IS 'Cron job definitions that create task instances on schedule';
COMMENT ON COLUMN cron_jobs.schedule IS 'Cron expression (minute hour day month weekday)';
COMMENT ON COLUMN cron_jobs.concurrency_policy IS 'How to handle overlapping executions: ALLOW, FORBID, or REPLACE';

COMMENT ON TABLE workers IS 'Registered worker nodes that process tasks';
COMMENT ON COLUMN workers.last_heartbeat IS 'Last heartbeat timestamp, workers are marked inactive if stale';

COMMENT ON TABLE scheduler_locks IS 'Distributed locks for leader election and coordination';
COMMENT ON COLUMN scheduler_locks.expires_at IS 'Lock expiration time, must be renewed before this';

COMMENT ON FUNCTION claim_tasks IS 'Atomically claim tasks for a worker using SKIP LOCKED pattern';
COMMENT ON FUNCTION try_acquire_lock IS 'Attempt to acquire or renew a distributed lock';
