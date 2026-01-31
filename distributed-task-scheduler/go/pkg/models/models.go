// Package models defines the core data structures for the distributed task scheduler.
//
// This package contains all the domain models used throughout the system:
//   - Task: Represents a single task instance
//   - CronJob: Represents a recurring job definition
//   - Worker: Represents a worker node
//   - TaskResult: Detailed execution result
//   - TaskEvent: Audit log entry
//
// All models use UUIDs for identification to support distributed ID generation
// without coordination.
package models

import (
	"encoding/json"
	"time"

	"github.com/google/uuid"
)

// TaskStatus represents the current state of a task in its lifecycle.
type TaskStatus string

const (
	// TaskStatusPending indicates the task is scheduled for future execution.
	TaskStatusPending TaskStatus = "PENDING"

	// TaskStatusQueued indicates the task is ready and waiting for a worker.
	TaskStatusQueued TaskStatus = "QUEUED"

	// TaskStatusActive indicates the task is being executed by a worker.
	TaskStatusActive TaskStatus = "ACTIVE"

	// TaskStatusCompleted indicates the task finished successfully.
	TaskStatusCompleted TaskStatus = "COMPLETED"

	// TaskStatusFailed indicates the task execution failed (may be retried).
	TaskStatusFailed TaskStatus = "FAILED"

	// TaskStatusDead indicates the task exceeded retry limit.
	TaskStatusDead TaskStatus = "DEAD"

	// TaskStatusCancelled indicates the task was cancelled before execution.
	TaskStatusCancelled TaskStatus = "CANCELLED"
)

// IsTerminal returns true if this is a terminal (final) state.
func (s TaskStatus) IsTerminal() bool {
	return s == TaskStatusCompleted || s == TaskStatusDead || s == TaskStatusCancelled
}

// CanTransitionTo checks if transition to the new status is valid.
func (s TaskStatus) CanTransitionTo(newStatus TaskStatus) bool {
	validTransitions := map[TaskStatus][]TaskStatus{
		TaskStatusPending:   {TaskStatusQueued, TaskStatusCancelled},
		TaskStatusQueued:    {TaskStatusActive, TaskStatusCancelled},
		TaskStatusActive:    {TaskStatusCompleted, TaskStatusFailed},
		TaskStatusFailed:    {TaskStatusQueued, TaskStatusDead},
		TaskStatusCompleted: {},
		TaskStatusDead:      {},
		TaskStatusCancelled: {},
	}

	valid, ok := validTransitions[s]
	if !ok {
		return false
	}

	for _, v := range valid {
		if v == newStatus {
			return true
		}
	}
	return false
}

// WorkerStatus represents the health state of a worker node.
type WorkerStatus string

const (
	// WorkerStatusActive indicates the worker is healthy and processing tasks.
	WorkerStatusActive WorkerStatus = "ACTIVE"

	// WorkerStatusDraining indicates the worker is shutting down gracefully.
	WorkerStatusDraining WorkerStatus = "DRAINING"

	// WorkerStatusInactive indicates the worker is offline or unhealthy.
	WorkerStatusInactive WorkerStatus = "INACTIVE"
)

// CronJobStatus represents the status of a cron job.
type CronJobStatus string

const (
	// CronJobStatusEnabled indicates the job is active and will create tasks on schedule.
	CronJobStatusEnabled CronJobStatus = "ENABLED"

	// CronJobStatusDisabled indicates the job is paused.
	CronJobStatusDisabled CronJobStatus = "DISABLED"

	// CronJobStatusDeleted indicates the job is soft-deleted.
	CronJobStatusDeleted CronJobStatus = "DELETED"
)

// ConcurrencyPolicy determines behavior when a cron job triggers while
// a previous instance is still running.
type ConcurrencyPolicy string

const (
	// ConcurrencyPolicyAllow creates new task regardless of previous run status.
	ConcurrencyPolicyAllow ConcurrencyPolicy = "ALLOW"

	// ConcurrencyPolicyForbid skips this run if previous is still active.
	ConcurrencyPolicyForbid ConcurrencyPolicy = "FORBID"

	// ConcurrencyPolicyReplace cancels previous run and starts new.
	ConcurrencyPolicyReplace ConcurrencyPolicy = "REPLACE"
)

// Task represents a single task instance in the scheduler.
//
// A task is the fundamental unit of work. Each task has:
//   - A type that determines which handler processes it
//   - A payload containing the data needed for execution
//   - Lifecycle metadata for tracking state and timing
type Task struct {
	// ID is the unique task identifier (UUID).
	ID uuid.UUID `json:"id"`

	// TaskType determines which handler processes this task.
	// Examples: "send_email", "process_payment", "generate_report"
	TaskType string `json:"task_type"`

	// QueueName is the queue this task belongs to.
	// Workers subscribe to specific queues for task routing.
	QueueName string `json:"queue_name"`

	// Status is the current lifecycle state.
	Status TaskStatus `json:"status"`

	// Priority determines execution order (0-100, higher = first).
	Priority int `json:"priority"`

	// Payload contains the task data as JSON.
	Payload json.RawMessage `json:"payload"`

	// Result contains the execution result (set on completion).
	Result json.RawMessage `json:"result,omitempty"`

	// ErrorMessage contains the error description (set on failure).
	ErrorMessage string `json:"error_message,omitempty"`

	// ErrorDetails contains detailed error info.
	ErrorDetails json.RawMessage `json:"error_details,omitempty"`

	// IdempotencyKey prevents duplicate task creation.
	IdempotencyKey string `json:"idempotency_key,omitempty"`

	// ParentTaskID links to parent task for chained execution.
	ParentTaskID *uuid.UUID `json:"parent_task_id,omitempty"`

	// CronJobID links to the source cron job if scheduled.
	CronJobID *uuid.UUID `json:"cron_job_id,omitempty"`

	// ScheduledAt is when to execute the task (nil = immediate).
	ScheduledAt *time.Time `json:"scheduled_at,omitempty"`

	// MaxAttempts is the maximum execution attempts including retries.
	MaxAttempts int `json:"max_attempts"`

	// AttemptCount is the number of execution attempts so far.
	AttemptCount int `json:"attempt_count"`

	// RetryDelaySeconds is the base delay for exponential backoff.
	RetryDelaySeconds float64 `json:"retry_delay_seconds"`

	// TimeoutSeconds is the per-attempt execution timeout.
	TimeoutSeconds int `json:"timeout_seconds"`

	// WorkerID is the assigned worker (when ACTIVE).
	WorkerID *uuid.UUID `json:"worker_id,omitempty"`

	// VisibilityTimeout is when the task becomes visible again.
	VisibilityTimeout *time.Time `json:"visibility_timeout,omitempty"`

	// Version is used for optimistic locking.
	Version int `json:"version"`

	// Timestamps for lifecycle tracking.
	CreatedAt   time.Time  `json:"created_at"`
	UpdatedAt   time.Time  `json:"updated_at"`
	QueuedAt    *time.Time `json:"queued_at,omitempty"`
	StartedAt   *time.Time `json:"started_at,omitempty"`
	CompletedAt *time.Time `json:"completed_at,omitempty"`
}

// NewTask creates a new task with sensible defaults.
func NewTask(taskType string, payload json.RawMessage) *Task {
	now := time.Now().UTC()
	return &Task{
		ID:                uuid.New(),
		TaskType:          taskType,
		QueueName:         "default",
		Status:            TaskStatusQueued,
		Priority:          50,
		Payload:           payload,
		MaxAttempts:       3,
		AttemptCount:      0,
		RetryDelaySeconds: 1.0,
		TimeoutSeconds:    300,
		Version:           1,
		CreatedAt:         now,
		UpdatedAt:         now,
		QueuedAt:          &now,
	}
}

// CanRetry returns true if the task can be retried.
func (t *Task) CanRetry() bool {
	return t.Status == TaskStatusFailed && t.AttemptCount < t.MaxAttempts
}

// ExecutionDuration returns the execution duration if available.
func (t *Task) ExecutionDuration() *time.Duration {
	if t.StartedAt == nil || t.CompletedAt == nil {
		return nil
	}
	d := t.CompletedAt.Sub(*t.StartedAt)
	return &d
}

// CronJob represents a recurring job definition.
//
// Cron jobs create task instances according to their schedule.
// The scheduler evaluates all enabled cron jobs and creates tasks
// when next_run_at <= now.
type CronJob struct {
	// ID is the unique job identifier.
	ID uuid.UUID `json:"id"`

	// Name is a human-readable unique name.
	Name string `json:"name"`

	// Description is a human-readable description.
	Description string `json:"description,omitempty"`

	// Schedule is the cron expression (5 fields: minute hour day month weekday).
	Schedule string `json:"schedule"`

	// Timezone for schedule evaluation (default UTC).
	Timezone string `json:"timezone"`

	// TaskType is the type of task to create.
	TaskType string `json:"task_type"`

	// TaskPayload is the payload for created tasks.
	TaskPayload json.RawMessage `json:"task_payload"`

	// QueueName is the queue for created tasks.
	QueueName string `json:"queue_name"`

	// Priority for created tasks (0-100).
	Priority int `json:"priority"`

	// MaxAttempts for created tasks.
	MaxAttempts int `json:"max_attempts"`

	// TimeoutSeconds for created tasks.
	TimeoutSeconds int `json:"timeout_seconds"`

	// Status is the job status.
	Status CronJobStatus `json:"status"`

	// ConcurrencyPolicy determines overlapping run handling.
	ConcurrencyPolicy ConcurrencyPolicy `json:"concurrency_policy"`

	// NextRunAt is the next scheduled execution time.
	NextRunAt *time.Time `json:"next_run_at,omitempty"`

	// LastRunAt is the last execution time.
	LastRunAt *time.Time `json:"last_run_at,omitempty"`

	// Statistics.
	RunCount     int64 `json:"run_count"`
	SuccessCount int64 `json:"success_count"`
	FailureCount int64 `json:"failure_count"`

	// Metadata for extensibility.
	Metadata json.RawMessage `json:"metadata,omitempty"`

	// Timestamps.
	CreatedAt time.Time `json:"created_at"`
	UpdatedAt time.Time `json:"updated_at"`
}

// NewCronJob creates a new cron job with sensible defaults.
func NewCronJob(name, schedule, taskType string) *CronJob {
	now := time.Now().UTC()
	return &CronJob{
		ID:                uuid.New(),
		Name:              name,
		Schedule:          schedule,
		Timezone:          "UTC",
		TaskType:          taskType,
		TaskPayload:       json.RawMessage("{}"),
		QueueName:         "default",
		Priority:          50,
		MaxAttempts:       3,
		TimeoutSeconds:    300,
		Status:            CronJobStatusEnabled,
		ConcurrencyPolicy: ConcurrencyPolicyAllow,
		Metadata:          json.RawMessage("{}"),
		CreatedAt:         now,
		UpdatedAt:         now,
	}
}

// SuccessRate returns the success rate as a percentage.
func (j *CronJob) SuccessRate() *float64 {
	if j.RunCount == 0 {
		return nil
	}
	rate := float64(j.SuccessCount) / float64(j.RunCount) * 100
	return &rate
}

// CreateTask creates a new task instance from this cron job.
func (j *CronJob) CreateTask() *Task {
	now := time.Now().UTC()
	cronJobID := j.ID
	return &Task{
		ID:                uuid.New(),
		TaskType:          j.TaskType,
		QueueName:         j.QueueName,
		Status:            TaskStatusQueued,
		Priority:          j.Priority,
		Payload:           j.TaskPayload,
		CronJobID:         &cronJobID,
		MaxAttempts:       j.MaxAttempts,
		TimeoutSeconds:    j.TimeoutSeconds,
		RetryDelaySeconds: 1.0,
		Version:           1,
		CreatedAt:         now,
		UpdatedAt:         now,
		QueuedAt:          &now,
	}
}

// Worker represents a task processing node.
//
// Workers register themselves on startup and send periodic heartbeats.
// The scheduler uses heartbeats to detect failed workers.
type Worker struct {
	// ID is the unique worker identifier.
	ID uuid.UUID `json:"id"`

	// Name is a human-readable name (usually hostname:pid).
	Name string `json:"name"`

	// Hostname is the machine hostname.
	Hostname string `json:"hostname"`

	// IPAddress is the worker's IP address.
	IPAddress string `json:"ip_address,omitempty"`

	// Port is the health check port.
	Port int `json:"port,omitempty"`

	// PID is the process ID.
	PID int `json:"pid"`

	// Queues is the list of queues this worker processes.
	Queues []string `json:"queues"`

	// Concurrency is the maximum concurrent tasks.
	Concurrency int `json:"concurrency"`

	// Status is the worker health status.
	Status WorkerStatus `json:"status"`

	// ActiveTaskCount is the current number of active tasks.
	ActiveTaskCount int `json:"active_task_count"`

	// CPUUsage is the CPU utilization percentage.
	CPUUsage *float64 `json:"cpu_usage,omitempty"`

	// MemoryUsage is the memory utilization percentage.
	MemoryUsage *float64 `json:"memory_usage,omitempty"`

	// LastHeartbeat is the last heartbeat timestamp.
	LastHeartbeat time.Time `json:"last_heartbeat"`

	// HeartbeatIntervalSeconds is the expected heartbeat interval.
	HeartbeatIntervalSeconds int `json:"heartbeat_interval_seconds"`

	// StartedAt is when the worker started.
	StartedAt time.Time `json:"started_at"`

	// StoppedAt is when the worker stopped (if applicable).
	StoppedAt *time.Time `json:"stopped_at,omitempty"`

	// Version is the software version.
	Version string `json:"version,omitempty"`

	// Metadata for extensibility.
	Metadata json.RawMessage `json:"metadata,omitempty"`
}

// NewWorker creates a new worker with sensible defaults.
func NewWorker(name, hostname string, pid int) *Worker {
	now := time.Now().UTC()
	return &Worker{
		ID:                       uuid.New(),
		Name:                     name,
		Hostname:                 hostname,
		PID:                      pid,
		Queues:                   []string{"default"},
		Concurrency:              10,
		Status:                   WorkerStatusActive,
		ActiveTaskCount:          0,
		LastHeartbeat:            now,
		HeartbeatIntervalSeconds: 10,
		StartedAt:                now,
		Metadata:                 json.RawMessage("{}"),
	}
}

// IsHealthy checks if the worker is considered healthy.
//
// A worker is healthy if it's ACTIVE and its last heartbeat
// is within the expected interval (with some tolerance).
func (w *Worker) IsHealthy() bool {
	if w.Status != WorkerStatusActive {
		return false
	}

	// Allow 3x heartbeat interval as grace period
	maxAge := time.Duration(w.HeartbeatIntervalSeconds*3) * time.Second
	return time.Since(w.LastHeartbeat) < maxAge
}

// AvailableCapacity returns the remaining task capacity.
func (w *Worker) AvailableCapacity() int {
	available := w.Concurrency - w.ActiveTaskCount
	if available < 0 {
		return 0
	}
	return available
}

// TaskResult stores detailed task execution results.
type TaskResult struct {
	ID            uuid.UUID       `json:"id"`
	TaskID        uuid.UUID       `json:"task_id"`
	WorkerID      *uuid.UUID      `json:"worker_id,omitempty"`
	AttemptNumber int             `json:"attempt_number"`
	Success       bool            `json:"success"`
	Result        json.RawMessage `json:"result,omitempty"`
	ErrorMessage  string          `json:"error_message,omitempty"`
	ErrorType     string          `json:"error_type,omitempty"`
	ErrorTrace    string          `json:"error_traceback,omitempty"`
	StartedAt     time.Time       `json:"started_at"`
	CompletedAt   time.Time       `json:"completed_at"`
	DurationMs    int             `json:"duration_ms"`
	CPUTimeMs     *int            `json:"cpu_time_ms,omitempty"`
	MemoryPeakMB  *int            `json:"memory_peak_mb,omitempty"`
	Logs          string          `json:"logs,omitempty"`
	CreatedAt     time.Time       `json:"created_at"`
}

// TaskEvent represents a task state change for audit logging.
type TaskEvent struct {
	ID          int64           `json:"id,omitempty"`
	TaskID      uuid.UUID       `json:"task_id"`
	EventType   string          `json:"event_type"`
	FromStatus  TaskStatus      `json:"from_status,omitempty"`
	ToStatus    TaskStatus      `json:"to_status,omitempty"`
	TriggeredBy string          `json:"triggered_by,omitempty"`
	Details     json.RawMessage `json:"details,omitempty"`
	CreatedAt   time.Time       `json:"created_at"`
}

// RetryPolicy defines the retry behavior for a task.
type RetryPolicy struct {
	// MaxAttempts is the maximum total attempts (1 = no retries).
	MaxAttempts int `json:"max_attempts"`

	// BaseDelay is the initial delay in seconds.
	BaseDelay float64 `json:"base_delay"`

	// MaxDelay is the maximum delay cap in seconds.
	MaxDelay float64 `json:"max_delay"`

	// ExponentialBase is the multiplier for each retry.
	ExponentialBase float64 `json:"exponential_base"`

	// Jitter adds randomization to prevent thundering herd.
	Jitter bool `json:"jitter"`

	// RetryOn specifies exception types to retry on ("*" = all).
	RetryOn []string `json:"retry_on"`

	// NoRetryOn specifies exception types to never retry on.
	NoRetryOn []string `json:"no_retry_on"`
}

// DefaultRetryPolicy returns a retry policy with sensible defaults.
func DefaultRetryPolicy() *RetryPolicy {
	return &RetryPolicy{
		MaxAttempts:     3,
		BaseDelay:       1.0,
		MaxDelay:        3600.0,
		ExponentialBase: 2.0,
		Jitter:          true,
		RetryOn:         []string{"*"},
		NoRetryOn:       []string{},
	}
}

// CalculateDelay calculates the delay before the next retry attempt.
func (p *RetryPolicy) CalculateDelay(attempt int) time.Duration {
	// Calculate exponential delay
	exponentialDelay := p.BaseDelay * pow(p.ExponentialBase, float64(attempt))

	// Cap at max_delay
	cappedDelay := min(p.MaxDelay, exponentialDelay)

	// Apply jitter if enabled
	if p.Jitter {
		cappedDelay = randFloat64() * cappedDelay
	}

	return time.Duration(cappedDelay * float64(time.Second))
}

// Helper functions to avoid import inside function
func pow(base, exp float64) float64 {
	result := 1.0
	for i := 0; i < int(exp); i++ {
		result *= base
	}
	return result
}

func min(a, b float64) float64 {
	if a < b {
		return a
	}
	return b
}

func randFloat64() float64 {
	// Simple random - in production use crypto/rand or math/rand
	return float64(time.Now().UnixNano()%1000) / 1000.0
}

// ShouldRetry determines if a retry should be attempted for the given error.
func (p *RetryPolicy) ShouldRetry(errorType string) bool {
	// Check blocklist first
	for _, blocked := range p.NoRetryOn {
		if blocked == errorType {
			return false
		}
	}

	// Check allowlist
	for _, allowed := range p.RetryOn {
		if allowed == "*" || allowed == errorType {
			return true
		}
	}

	return false
}
