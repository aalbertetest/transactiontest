// Package persistence provides the repository for database operations.
package persistence

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/rs/zerolog/log"

	"github.com/distributed-task-scheduler/pkg/models"
)

// Repository provides data access for the task scheduler.
type Repository struct {
	db *Database
}

// NewRepository creates a new repository.
func NewRepository(db *Database) *Repository {
	return &Repository{db: db}
}

// ============================================================================
// TASK OPERATIONS
// ============================================================================

// CreateTask creates a new task.
func (r *Repository) CreateTask(ctx context.Context, task *models.Task) (*models.Task, error) {
	now := time.Now().UTC()
	task.CreatedAt = now
	task.UpdatedAt = now

	if task.ID == uuid.Nil {
		task.ID = uuid.New()
	}
	if task.Version == 0 {
		task.Version = 1
	}

	// Determine initial status based on scheduling
	if task.ScheduledAt != nil && task.ScheduledAt.After(now) {
		task.Status = models.TaskStatusPending
		task.QueuedAt = nil
	} else {
		task.Status = models.TaskStatusQueued
		task.QueuedAt = &now
		task.ScheduledAt = nil
	}

	payloadJSON, err := json.Marshal(task.Payload)
	if err != nil {
		return nil, fmt.Errorf("failed to marshal payload: %w", err)
	}

	query := `
		INSERT INTO tasks (
			id, task_type, queue_name, status, priority, payload,
			idempotency_key, scheduled_at, max_attempts, timeout_seconds,
			retry_delay_seconds, parent_task_id, cron_job_id,
			queued_at, created_at, updated_at, version
		) VALUES (
			$1, $2, $3, $4, $5, $6,
			$7, $8, $9, $10,
			$11, $12, $13,
			$14, $15, $15, $16
		)
		RETURNING *
	`

	row := r.db.QueryRow(ctx, query,
		task.ID,
		task.TaskType,
		task.QueueName,
		string(task.Status),
		task.Priority,
		payloadJSON,
		nullString(task.IdempotencyKey),
		task.ScheduledAt,
		task.MaxAttempts,
		task.TimeoutSeconds,
		task.RetryDelaySeconds,
		task.ParentTaskID,
		task.CronJobID,
		task.QueuedAt,
		now,
		task.Version,
	)

	created, err := scanTask(row)
	if err != nil {
		return nil, fmt.Errorf("failed to create task: %w", err)
	}

	log.Info().
		Str("task_id", created.ID.String()).
		Str("task_type", created.TaskType).
		Str("status", string(created.Status)).
		Str("queue", created.QueueName).
		Msg("Created task")

	return created, nil
}

// GetTask retrieves a task by ID.
func (r *Repository) GetTask(ctx context.Context, taskID uuid.UUID) (*models.Task, error) {
	query := `
		SELECT * FROM tasks
		WHERE id = $1 AND deleted_at IS NULL
	`

	row := r.db.QueryRow(ctx, query, taskID)
	return scanTask(row)
}

// GetTaskByIdempotencyKey retrieves a non-terminal task by idempotency key.
func (r *Repository) GetTaskByIdempotencyKey(ctx context.Context, key string) (*models.Task, error) {
	query := `
		SELECT * FROM tasks
		WHERE idempotency_key = $1
		  AND status NOT IN ('FAILED', 'DEAD', 'CANCELLED')
		  AND deleted_at IS NULL
		ORDER BY created_at DESC
		LIMIT 1
	`

	row := r.db.QueryRow(ctx, query, key)
	task, err := scanTask(row)
	if err == pgx.ErrNoRows {
		return nil, nil
	}
	return task, err
}

// ClaimTasks claims tasks for a worker.
func (r *Repository) ClaimTasks(
	ctx context.Context,
	workerID uuid.UUID,
	queueName string,
	batchSize int,
	visibilityTimeoutSeconds int,
) ([]*models.Task, error) {
	query := `SELECT * FROM claim_tasks($1, $2, $3, $4)`

	rows, err := r.db.Query(ctx, query,
		workerID,
		queueName,
		batchSize,
		visibilityTimeoutSeconds,
	)
	if err != nil {
		return nil, fmt.Errorf("failed to claim tasks: %w", err)
	}
	defer rows.Close()

	var tasks []*models.Task
	for rows.Next() {
		task, err := scanTaskFromRows(rows)
		if err != nil {
			return nil, err
		}
		tasks = append(tasks, task)
	}

	if len(tasks) > 0 {
		taskIDs := make([]string, len(tasks))
		for i, t := range tasks {
			taskIDs[i] = t.ID.String()
		}
		log.Debug().
			Str("worker_id", workerID.String()).
			Str("queue", queueName).
			Strs("task_ids", taskIDs).
			Msg("Claimed tasks")
	}

	return tasks, nil
}

// CompleteTask marks a task as completed.
func (r *Repository) CompleteTask(
	ctx context.Context,
	taskID uuid.UUID,
	result json.RawMessage,
	expectedVersion *int,
) (*models.Task, error) {
	now := time.Now().UTC()

	var query string
	var args []interface{}

	if expectedVersion != nil {
		query = `
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
		`
		args = []interface{}{taskID, string(models.TaskStatusCompleted), result, now, *expectedVersion}
	} else {
		query = `
			UPDATE tasks
			SET status = $2,
				result = $3,
				completed_at = $4,
				version = version + 1
			WHERE id = $1
			  AND status = 'ACTIVE'
			  AND deleted_at IS NULL
			RETURNING *
		`
		args = []interface{}{taskID, string(models.TaskStatusCompleted), result, now}
	}

	row := r.db.QueryRow(ctx, query, args...)
	task, err := scanTask(row)
	if err == pgx.ErrNoRows {
		log.Warn().
			Str("task_id", taskID.String()).
			Msg("Failed to complete task (not found or version mismatch)")
		return nil, nil
	}
	if err != nil {
		return nil, fmt.Errorf("failed to complete task: %w", err)
	}

	log.Info().
		Str("task_id", taskID.String()).
		Msg("Task completed")

	return task, nil
}

// FailTask marks a task as failed.
func (r *Repository) FailTask(
	ctx context.Context,
	taskID uuid.UUID,
	errorMessage string,
	errorDetails json.RawMessage,
	expectedVersion *int,
) (*models.Task, error) {
	now := time.Now().UTC()

	// First get the task to check retry status
	task, err := r.GetTask(ctx, taskID)
	if err != nil || task == nil {
		return nil, err
	}

	var newStatus models.TaskStatus
	var scheduledAt *time.Time
	var completedAt *time.Time

	if task.AttemptCount < task.MaxAttempts {
		// Calculate retry delay with exponential backoff
		delaySeconds := task.RetryDelaySeconds * float64(1<<(task.AttemptCount-1))
		if delaySeconds > 3600 {
			delaySeconds = 3600 // Cap at 1 hour
		}
		retryTime := now.Add(time.Duration(delaySeconds * float64(time.Second)))

		newStatus = models.TaskStatusQueued
		scheduledAt = &retryTime

		log.Info().
			Str("task_id", taskID.String()).
			Int("attempt", task.AttemptCount).
			Int("max_attempts", task.MaxAttempts).
			Float64("retry_delay", delaySeconds).
			Msg("Task failed, scheduling retry")
	} else {
		// Move to dead letter queue
		newStatus = models.TaskStatusDead
		completedAt = &now

		log.Warn().
			Str("task_id", taskID.String()).
			Int("attempts", task.AttemptCount).
			Str("error", errorMessage).
			Msg("Task moved to dead letter queue")
	}

	var query string
	var args []interface{}

	if expectedVersion != nil {
		query = `
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
		`
		args = []interface{}{taskID, string(newStatus), errorMessage, errorDetails, scheduledAt, completedAt, *expectedVersion}
	} else {
		query = `
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
		`
		args = []interface{}{taskID, string(newStatus), errorMessage, errorDetails, scheduledAt, completedAt}
	}

	row := r.db.QueryRow(ctx, query, args...)
	return scanTask(row)
}

// CancelTask cancels a pending or queued task.
func (r *Repository) CancelTask(ctx context.Context, taskID uuid.UUID) (*models.Task, error) {
	now := time.Now().UTC()

	query := `
		UPDATE tasks
		SET status = 'CANCELLED',
			completed_at = $2,
			version = version + 1
		WHERE id = $1
		  AND status IN ('PENDING', 'QUEUED')
		  AND deleted_at IS NULL
		RETURNING *
	`

	row := r.db.QueryRow(ctx, query, taskID, now)
	task, err := scanTask(row)
	if err == pgx.ErrNoRows {
		return nil, nil
	}
	if err != nil {
		return nil, err
	}

	log.Info().Str("task_id", taskID.String()).Msg("Task cancelled")
	return task, nil
}

// ExtendVisibilityTimeout extends the visibility timeout for an active task.
func (r *Repository) ExtendVisibilityTimeout(
	ctx context.Context,
	taskID uuid.UUID,
	workerID uuid.UUID,
	extensionSeconds int,
) (bool, error) {
	newTimeout := time.Now().UTC().Add(time.Duration(extensionSeconds) * time.Second)

	query := `
		UPDATE tasks
		SET visibility_timeout = $3,
			version = version + 1
		WHERE id = $1
		  AND worker_id = $2
		  AND status = 'ACTIVE'
		  AND deleted_at IS NULL
		RETURNING id
	`

	var id uuid.UUID
	err := r.db.QueryRow(ctx, query, taskID, workerID, newTimeout).Scan(&id)
	if err == pgx.ErrNoRows {
		return false, nil
	}
	if err != nil {
		return false, err
	}

	return true, nil
}

// PromotePendingTasks promotes pending tasks to queued.
func (r *Repository) PromotePendingTasks(ctx context.Context) (int, error) {
	var count int
	err := r.db.QueryRow(ctx, "SELECT promote_pending_tasks()").Scan(&count)
	if err != nil {
		return 0, fmt.Errorf("failed to promote pending tasks: %w", err)
	}

	if count > 0 {
		log.Debug().Int("count", count).Msg("Promoted pending tasks")
	}

	return count, nil
}

// RecoverTimedOutTasks recovers tasks that exceeded visibility timeout.
func (r *Repository) RecoverTimedOutTasks(ctx context.Context) (int, error) {
	var count int
	err := r.db.QueryRow(ctx, "SELECT recover_timed_out_tasks()").Scan(&count)
	if err != nil {
		return 0, fmt.Errorf("failed to recover timed out tasks: %w", err)
	}

	if count > 0 {
		log.Info().Int("count", count).Msg("Recovered timed out tasks")
	}

	return count, nil
}

// ============================================================================
// CRON JOB OPERATIONS
// ============================================================================

// CreateCronJob creates a new cron job.
func (r *Repository) CreateCronJob(ctx context.Context, job *models.CronJob) (*models.CronJob, error) {
	now := time.Now().UTC()
	job.CreatedAt = now
	job.UpdatedAt = now

	if job.ID == uuid.Nil {
		job.ID = uuid.New()
	}

	query := `
		INSERT INTO cron_jobs (
			id, name, description, schedule, timezone,
			task_type, task_payload, queue_name, priority,
			max_attempts, timeout_seconds, concurrency_policy,
			status, next_run_at, metadata, created_at, updated_at
		) VALUES (
			$1, $2, $3, $4, $5,
			$6, $7, $8, $9,
			$10, $11, $12,
			$13, $14, $15, $16, $16
		)
		RETURNING *
	`

	row := r.db.QueryRow(ctx, query,
		job.ID,
		job.Name,
		job.Description,
		job.Schedule,
		job.Timezone,
		job.TaskType,
		job.TaskPayload,
		job.QueueName,
		job.Priority,
		job.MaxAttempts,
		job.TimeoutSeconds,
		string(job.ConcurrencyPolicy),
		string(job.Status),
		job.NextRunAt,
		job.Metadata,
		now,
	)

	created, err := scanCronJob(row)
	if err != nil {
		return nil, fmt.Errorf("failed to create cron job: %w", err)
	}

	log.Info().
		Str("job_id", created.ID.String()).
		Str("name", created.Name).
		Str("schedule", created.Schedule).
		Msg("Created cron job")

	return created, nil
}

// GetCronJob retrieves a cron job by ID.
func (r *Repository) GetCronJob(ctx context.Context, jobID uuid.UUID) (*models.CronJob, error) {
	query := `SELECT * FROM cron_jobs WHERE id = $1 AND deleted_at IS NULL`
	row := r.db.QueryRow(ctx, query, jobID)
	return scanCronJob(row)
}

// GetDueCronJobs retrieves cron jobs that are due for execution.
func (r *Repository) GetDueCronJobs(ctx context.Context) ([]*models.CronJob, error) {
	query := `
		SELECT * FROM cron_jobs
		WHERE status = 'ENABLED'
		  AND next_run_at <= $1
		  AND deleted_at IS NULL
		FOR UPDATE SKIP LOCKED
	`

	rows, err := r.db.Query(ctx, query, time.Now().UTC())
	if err != nil {
		return nil, fmt.Errorf("failed to get due cron jobs: %w", err)
	}
	defer rows.Close()

	var jobs []*models.CronJob
	for rows.Next() {
		job, err := scanCronJobFromRows(rows)
		if err != nil {
			return nil, err
		}
		jobs = append(jobs, job)
	}

	return jobs, nil
}

// UpdateCronJobAfterRun updates cron job statistics after a run.
func (r *Repository) UpdateCronJobAfterRun(
	ctx context.Context,
	jobID uuid.UUID,
	nextRunAt time.Time,
	success bool,
) (*models.CronJob, error) {
	now := time.Now().UTC()

	var query string
	if success {
		query = `
			UPDATE cron_jobs
			SET next_run_at = $2,
				last_run_at = $3,
				run_count = run_count + 1,
				success_count = success_count + 1
			WHERE id = $1 AND deleted_at IS NULL
			RETURNING *
		`
	} else {
		query = `
			UPDATE cron_jobs
			SET next_run_at = $2,
				last_run_at = $3,
				run_count = run_count + 1,
				failure_count = failure_count + 1
			WHERE id = $1 AND deleted_at IS NULL
			RETURNING *
		`
	}

	row := r.db.QueryRow(ctx, query, jobID, nextRunAt, now)
	return scanCronJob(row)
}

// ============================================================================
// WORKER OPERATIONS
// ============================================================================

// RegisterWorker registers or updates a worker.
func (r *Repository) RegisterWorker(ctx context.Context, worker *models.Worker) (*models.Worker, error) {
	now := time.Now().UTC()

	query := `
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
	`

	row := r.db.QueryRow(ctx, query,
		worker.ID,
		worker.Name,
		worker.Hostname,
		nullString(worker.IPAddress),
		nullInt(worker.Port),
		worker.PID,
		worker.Queues,
		worker.Concurrency,
		now,
		worker.Version,
		worker.Metadata,
	)

	registered, err := scanWorker(row)
	if err != nil {
		return nil, fmt.Errorf("failed to register worker: %w", err)
	}

	log.Info().
		Str("worker_id", registered.ID.String()).
		Str("name", registered.Name).
		Strs("queues", registered.Queues).
		Int("concurrency", registered.Concurrency).
		Msg("Registered worker")

	return registered, nil
}

// Heartbeat updates worker heartbeat.
func (r *Repository) Heartbeat(
	ctx context.Context,
	workerID uuid.UUID,
	activeTaskCount int,
	cpuUsage *float64,
	memoryUsage *float64,
) (bool, error) {
	query := `
		UPDATE workers
		SET last_heartbeat = $2,
			active_task_count = $3,
			cpu_usage = $4,
			memory_usage = $5
		WHERE id = $1 AND status = 'ACTIVE'
		RETURNING id
	`

	var id uuid.UUID
	err := r.db.QueryRow(ctx, query,
		workerID,
		time.Now().UTC(),
		activeTaskCount,
		cpuUsage,
		memoryUsage,
	).Scan(&id)

	if err == pgx.ErrNoRows {
		return false, nil
	}
	if err != nil {
		return false, err
	}

	return true, nil
}

// DeregisterWorker deregisters a worker.
func (r *Repository) DeregisterWorker(ctx context.Context, workerID uuid.UUID) (bool, error) {
	now := time.Now().UTC()

	query := `
		UPDATE workers
		SET status = 'INACTIVE',
			stopped_at = $2
		WHERE id = $1
		RETURNING id
	`

	var id uuid.UUID
	err := r.db.QueryRow(ctx, query, workerID, now).Scan(&id)
	if err == pgx.ErrNoRows {
		return false, nil
	}
	if err != nil {
		return false, err
	}

	log.Info().Str("worker_id", workerID.String()).Msg("Deregistered worker")
	return true, nil
}

// GetStaleWorkers gets workers with stale heartbeats.
func (r *Repository) GetStaleWorkers(ctx context.Context, timeoutSeconds int) ([]*models.Worker, error) {
	cutoff := time.Now().UTC().Add(-time.Duration(timeoutSeconds) * time.Second)

	query := `
		SELECT * FROM workers
		WHERE status = 'ACTIVE'
		  AND last_heartbeat < $1
	`

	rows, err := r.db.Query(ctx, query, cutoff)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var workers []*models.Worker
	for rows.Next() {
		worker, err := scanWorkerFromRows(rows)
		if err != nil {
			return nil, err
		}
		workers = append(workers, worker)
	}

	return workers, nil
}

// MarkWorkerInactive marks a worker as inactive and fails its tasks.
func (r *Repository) MarkWorkerInactive(ctx context.Context, workerID uuid.UUID) (int, error) {
	now := time.Now().UTC()

	// Mark worker inactive
	err := r.db.Exec(ctx, `
		UPDATE workers
		SET status = 'INACTIVE',
			stopped_at = $2
		WHERE id = $1
	`, workerID, now)
	if err != nil {
		return 0, err
	}

	// Fail active tasks
	result, err := r.db.Pool().Exec(ctx, `
		UPDATE tasks
		SET status = 'FAILED',
			error_message = 'Worker heartbeat timeout',
			worker_id = NULL,
			visibility_timeout = NULL,
			version = version + 1
		WHERE worker_id = $1
		  AND status = 'ACTIVE'
		  AND deleted_at IS NULL
	`, workerID)
	if err != nil {
		return 0, err
	}

	count := int(result.RowsAffected())
	if count > 0 {
		log.Warn().
			Str("worker_id", workerID.String()).
			Int("task_count", count).
			Msg("Failed tasks due to worker timeout")
	}

	return count, nil
}

// ============================================================================
// LEADER ELECTION
// ============================================================================

// TryAcquireLock attempts to acquire a distributed lock.
func (r *Repository) TryAcquireLock(
	ctx context.Context,
	lockName string,
	holderID uuid.UUID,
	holderName string,
	ttlSeconds int,
) (bool, error) {
	var acquired bool
	err := r.db.QueryRow(ctx,
		"SELECT try_acquire_lock($1, $2, $3, $4)",
		lockName, holderID, holderName, ttlSeconds,
	).Scan(&acquired)

	if err != nil {
		return false, fmt.Errorf("failed to acquire lock: %w", err)
	}

	return acquired, nil
}

// ReleaseLock releases a distributed lock.
func (r *Repository) ReleaseLock(
	ctx context.Context,
	lockName string,
	holderID uuid.UUID,
) (bool, error) {
	var released bool
	err := r.db.QueryRow(ctx,
		"SELECT release_lock($1, $2)",
		lockName, holderID,
	).Scan(&released)

	if err != nil {
		return false, fmt.Errorf("failed to release lock: %w", err)
	}

	return released, nil
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

func nullString(s string) interface{} {
	if s == "" {
		return nil
	}
	return s
}

func nullInt(i int) interface{} {
	if i == 0 {
		return nil
	}
	return i
}

func scanTask(row pgx.Row) (*models.Task, error) {
	var t models.Task
	var status string

	err := row.Scan(
		&t.ID, &t.TaskType, &t.QueueName, &status, &t.Priority,
		&t.Payload, &t.Result, &t.ErrorMessage, &t.ErrorDetails,
		&t.IdempotencyKey, &t.ParentTaskID, &t.CronJobID,
		&t.ScheduledAt, &t.MaxAttempts, &t.AttemptCount,
		&t.RetryDelaySeconds, &t.TimeoutSeconds, &t.WorkerID,
		&t.VisibilityTimeout, &t.Version, &t.CreatedAt, &t.UpdatedAt,
		&t.QueuedAt, &t.StartedAt, &t.CompletedAt,
		// deleted_at is not scanned
	)
	if err != nil {
		return nil, err
	}

	t.Status = models.TaskStatus(status)
	return &t, nil
}

func scanTaskFromRows(rows pgx.Rows) (*models.Task, error) {
	var t models.Task
	var status string
	var deletedAt *time.Time

	err := rows.Scan(
		&t.ID, &t.TaskType, &t.QueueName, &status, &t.Priority,
		&t.Payload, &t.Result, &t.ErrorMessage, &t.ErrorDetails,
		&t.IdempotencyKey, &t.ParentTaskID, &t.CronJobID,
		&t.ScheduledAt, &t.MaxAttempts, &t.AttemptCount,
		&t.RetryDelaySeconds, &t.TimeoutSeconds, &t.WorkerID,
		&t.VisibilityTimeout, &t.Version, &t.CreatedAt, &t.UpdatedAt,
		&t.QueuedAt, &t.StartedAt, &t.CompletedAt, &deletedAt,
	)
	if err != nil {
		return nil, err
	}

	t.Status = models.TaskStatus(status)
	return &t, nil
}

func scanCronJob(row pgx.Row) (*models.CronJob, error) {
	var j models.CronJob
	var status, concurrencyPolicy string

	err := row.Scan(
		&j.ID, &j.Name, &j.Description, &j.Schedule, &j.Timezone,
		&j.TaskType, &j.TaskPayload, &j.QueueName, &j.Priority,
		&j.MaxAttempts, &j.TimeoutSeconds, &status, &concurrencyPolicy,
		&j.NextRunAt, &j.LastRunAt, &j.RunCount, &j.SuccessCount,
		&j.FailureCount, &j.Metadata, &j.CreatedAt, &j.UpdatedAt,
		// deleted_at not scanned
	)
	if err != nil {
		return nil, err
	}

	j.Status = models.CronJobStatus(status)
	j.ConcurrencyPolicy = models.ConcurrencyPolicy(concurrencyPolicy)
	return &j, nil
}

func scanCronJobFromRows(rows pgx.Rows) (*models.CronJob, error) {
	var j models.CronJob
	var status, concurrencyPolicy string
	var deletedAt *time.Time

	err := rows.Scan(
		&j.ID, &j.Name, &j.Description, &j.Schedule, &j.Timezone,
		&j.TaskType, &j.TaskPayload, &j.QueueName, &j.Priority,
		&j.MaxAttempts, &j.TimeoutSeconds, &status, &concurrencyPolicy,
		&j.NextRunAt, &j.LastRunAt, &j.RunCount, &j.SuccessCount,
		&j.FailureCount, &j.Metadata, &j.CreatedAt, &j.UpdatedAt,
		&deletedAt,
	)
	if err != nil {
		return nil, err
	}

	j.Status = models.CronJobStatus(status)
	j.ConcurrencyPolicy = models.ConcurrencyPolicy(concurrencyPolicy)
	return &j, nil
}

func scanWorker(row pgx.Row) (*models.Worker, error) {
	var w models.Worker
	var status string

	err := row.Scan(
		&w.ID, &w.Name, &w.Hostname, &w.IPAddress, &w.Port, &w.PID,
		&w.Queues, &w.Concurrency, &status, &w.ActiveTaskCount,
		&w.CPUUsage, &w.MemoryUsage, &w.LastHeartbeat,
		&w.HeartbeatIntervalSeconds, &w.StartedAt, &w.StoppedAt,
		&w.Version, &w.Metadata,
	)
	if err != nil {
		return nil, err
	}

	w.Status = models.WorkerStatus(status)
	return &w, nil
}

func scanWorkerFromRows(rows pgx.Rows) (*models.Worker, error) {
	var w models.Worker
	var status string

	err := rows.Scan(
		&w.ID, &w.Name, &w.Hostname, &w.IPAddress, &w.Port, &w.PID,
		&w.Queues, &w.Concurrency, &status, &w.ActiveTaskCount,
		&w.CPUUsage, &w.MemoryUsage, &w.LastHeartbeat,
		&w.HeartbeatIntervalSeconds, &w.StartedAt, &w.StoppedAt,
		&w.Version, &w.Metadata,
	)
	if err != nil {
		return nil, err
	}

	w.Status = models.WorkerStatus(status)
	return &w, nil
}
