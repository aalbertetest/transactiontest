package models

import (
	"encoding/json"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestTaskStatus_IsTerminal(t *testing.T) {
	tests := []struct {
		status   TaskStatus
		terminal bool
	}{
		{TaskStatusPending, false},
		{TaskStatusQueued, false},
		{TaskStatusActive, false},
		{TaskStatusCompleted, true},
		{TaskStatusFailed, false},
		{TaskStatusDead, true},
		{TaskStatusCancelled, true},
	}

	for _, tt := range tests {
		t.Run(string(tt.status), func(t *testing.T) {
			assert.Equal(t, tt.terminal, tt.status.IsTerminal())
		})
	}
}

func TestTaskStatus_CanTransitionTo(t *testing.T) {
	tests := []struct {
		from  TaskStatus
		to    TaskStatus
		valid bool
	}{
		// Valid transitions
		{TaskStatusPending, TaskStatusQueued, true},
		{TaskStatusPending, TaskStatusCancelled, true},
		{TaskStatusQueued, TaskStatusActive, true},
		{TaskStatusQueued, TaskStatusCancelled, true},
		{TaskStatusActive, TaskStatusCompleted, true},
		{TaskStatusActive, TaskStatusFailed, true},
		{TaskStatusFailed, TaskStatusQueued, true},
		{TaskStatusFailed, TaskStatusDead, true},

		// Invalid transitions
		{TaskStatusPending, TaskStatusActive, false},
		{TaskStatusQueued, TaskStatusCompleted, false},
		{TaskStatusActive, TaskStatusQueued, false},
		{TaskStatusCompleted, TaskStatusQueued, false},
		{TaskStatusDead, TaskStatusQueued, false},
		{TaskStatusCancelled, TaskStatusQueued, false},
	}

	for _, tt := range tests {
		name := string(tt.from) + " -> " + string(tt.to)
		t.Run(name, func(t *testing.T) {
			assert.Equal(t, tt.valid, tt.from.CanTransitionTo(tt.to))
		})
	}
}

func TestNewTask(t *testing.T) {
	payload := json.RawMessage(`{"key": "value"}`)
	task := NewTask("send_email", payload)

	assert.NotEqual(t, uuid.Nil, task.ID)
	assert.Equal(t, "send_email", task.TaskType)
	assert.Equal(t, "default", task.QueueName)
	assert.Equal(t, TaskStatusQueued, task.Status)
	assert.Equal(t, 50, task.Priority)
	assert.Equal(t, 3, task.MaxAttempts)
	assert.Equal(t, 0, task.AttemptCount)
	assert.Equal(t, 300, task.TimeoutSeconds)
	assert.Equal(t, 1, task.Version)
	assert.NotNil(t, task.QueuedAt)
}

func TestTask_CanRetry(t *testing.T) {
	tests := []struct {
		name         string
		status       TaskStatus
		attemptCount int
		maxAttempts  int
		canRetry     bool
	}{
		{"failed with retries", TaskStatusFailed, 1, 3, true},
		{"failed at limit", TaskStatusFailed, 3, 3, false},
		{"not failed", TaskStatusQueued, 1, 3, false},
		{"completed", TaskStatusCompleted, 1, 3, false},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			task := &Task{
				Status:       tt.status,
				AttemptCount: tt.attemptCount,
				MaxAttempts:  tt.maxAttempts,
			}
			assert.Equal(t, tt.canRetry, task.CanRetry())
		})
	}
}

func TestTask_ExecutionDuration(t *testing.T) {
	t.Run("with both timestamps", func(t *testing.T) {
		started := time.Now()
		completed := started.Add(5 * time.Second)
		task := &Task{
			StartedAt:   &started,
			CompletedAt: &completed,
		}

		duration := task.ExecutionDuration()
		require.NotNil(t, duration)
		assert.Equal(t, 5*time.Second, *duration)
	})

	t.Run("without completed", func(t *testing.T) {
		started := time.Now()
		task := &Task{
			StartedAt: &started,
		}

		assert.Nil(t, task.ExecutionDuration())
	})

	t.Run("without started", func(t *testing.T) {
		completed := time.Now()
		task := &Task{
			CompletedAt: &completed,
		}

		assert.Nil(t, task.ExecutionDuration())
	})
}

func TestNewCronJob(t *testing.T) {
	job := NewCronJob("daily_cleanup", "0 0 * * *", "cleanup")

	assert.NotEqual(t, uuid.Nil, job.ID)
	assert.Equal(t, "daily_cleanup", job.Name)
	assert.Equal(t, "0 0 * * *", job.Schedule)
	assert.Equal(t, "UTC", job.Timezone)
	assert.Equal(t, "cleanup", job.TaskType)
	assert.Equal(t, "default", job.QueueName)
	assert.Equal(t, 50, job.Priority)
	assert.Equal(t, 3, job.MaxAttempts)
	assert.Equal(t, CronJobStatusEnabled, job.Status)
	assert.Equal(t, ConcurrencyPolicyAllow, job.ConcurrencyPolicy)
}

func TestCronJob_SuccessRate(t *testing.T) {
	t.Run("with runs", func(t *testing.T) {
		job := &CronJob{
			RunCount:     100,
			SuccessCount: 95,
			FailureCount: 5,
		}

		rate := job.SuccessRate()
		require.NotNil(t, rate)
		assert.Equal(t, 95.0, *rate)
	})

	t.Run("no runs", func(t *testing.T) {
		job := &CronJob{
			RunCount: 0,
		}

		assert.Nil(t, job.SuccessRate())
	})
}

func TestCronJob_CreateTask(t *testing.T) {
	jobID := uuid.New()
	job := &CronJob{
		ID:             jobID,
		TaskType:       "test_task",
		TaskPayload:    json.RawMessage(`{"key": "value"}`),
		QueueName:      "test_queue",
		Priority:       75,
		MaxAttempts:    5,
		TimeoutSeconds: 600,
	}

	task := job.CreateTask()

	assert.NotEqual(t, uuid.Nil, task.ID)
	assert.Equal(t, "test_task", task.TaskType)
	assert.Equal(t, "test_queue", task.QueueName)
	assert.Equal(t, 75, task.Priority)
	assert.Equal(t, 5, task.MaxAttempts)
	assert.Equal(t, 600, task.TimeoutSeconds)
	assert.Equal(t, TaskStatusQueued, task.Status)
	assert.NotNil(t, task.CronJobID)
	assert.Equal(t, jobID, *task.CronJobID)
}

func TestNewWorker(t *testing.T) {
	worker := NewWorker("test-worker:1234", "test-host", 1234)

	assert.NotEqual(t, uuid.Nil, worker.ID)
	assert.Equal(t, "test-worker:1234", worker.Name)
	assert.Equal(t, "test-host", worker.Hostname)
	assert.Equal(t, 1234, worker.PID)
	assert.Equal(t, []string{"default"}, worker.Queues)
	assert.Equal(t, 10, worker.Concurrency)
	assert.Equal(t, WorkerStatusActive, worker.Status)
	assert.Equal(t, 0, worker.ActiveTaskCount)
}

func TestWorker_IsHealthy(t *testing.T) {
	tests := []struct {
		name      string
		status    WorkerStatus
		heartbeat time.Time
		interval  int
		healthy   bool
	}{
		{
			"healthy active worker",
			WorkerStatusActive,
			time.Now(),
			10,
			true,
		},
		{
			"stale heartbeat",
			WorkerStatusActive,
			time.Now().Add(-40 * time.Second),
			10,
			false,
		},
		{
			"inactive worker",
			WorkerStatusInactive,
			time.Now(),
			10,
			false,
		},
		{
			"draining worker",
			WorkerStatusDraining,
			time.Now(),
			10,
			false,
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			worker := &Worker{
				Status:                   tt.status,
				LastHeartbeat:            tt.heartbeat,
				HeartbeatIntervalSeconds: tt.interval,
			}
			assert.Equal(t, tt.healthy, worker.IsHealthy())
		})
	}
}

func TestWorker_AvailableCapacity(t *testing.T) {
	tests := []struct {
		name        string
		concurrency int
		active      int
		expected    int
	}{
		{"full capacity", 10, 0, 10},
		{"partial use", 10, 3, 7},
		{"at capacity", 10, 10, 0},
		{"over capacity", 10, 12, 0},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			worker := &Worker{
				Concurrency:     tt.concurrency,
				ActiveTaskCount: tt.active,
			}
			assert.Equal(t, tt.expected, worker.AvailableCapacity())
		})
	}
}

func TestDefaultRetryPolicy(t *testing.T) {
	policy := DefaultRetryPolicy()

	assert.Equal(t, 3, policy.MaxAttempts)
	assert.Equal(t, 1.0, policy.BaseDelay)
	assert.Equal(t, 3600.0, policy.MaxDelay)
	assert.Equal(t, 2.0, policy.ExponentialBase)
	assert.True(t, policy.Jitter)
	assert.Equal(t, []string{"*"}, policy.RetryOn)
	assert.Empty(t, policy.NoRetryOn)
}

func TestRetryPolicy_ShouldRetry(t *testing.T) {
	t.Run("wildcard allows all", func(t *testing.T) {
		policy := &RetryPolicy{
			RetryOn:   []string{"*"},
			NoRetryOn: []string{},
		}

		assert.True(t, policy.ShouldRetry("ValueError"))
		assert.True(t, policy.ShouldRetry("RuntimeError"))
	})

	t.Run("specific allowlist", func(t *testing.T) {
		policy := &RetryPolicy{
			RetryOn:   []string{"ConnectionError", "TimeoutError"},
			NoRetryOn: []string{},
		}

		assert.True(t, policy.ShouldRetry("ConnectionError"))
		assert.True(t, policy.ShouldRetry("TimeoutError"))
		assert.False(t, policy.ShouldRetry("ValueError"))
	})

	t.Run("blocklist takes precedence", func(t *testing.T) {
		policy := &RetryPolicy{
			RetryOn:   []string{"*"},
			NoRetryOn: []string{"ValueError"},
		}

		assert.True(t, policy.ShouldRetry("RuntimeError"))
		assert.False(t, policy.ShouldRetry("ValueError"))
	})
}
