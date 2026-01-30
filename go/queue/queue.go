package queue

import (
	"workflow/engine"
	"workflow/persistence"
)

// TaskQueue wraps persistence for a specific queue name.
type TaskQueue struct {
	persistence *persistence.SQLitePersistence
	queueName   string
}

// NewTaskQueue creates a queue abstraction for a named queue.
func NewTaskQueue(p *persistence.SQLitePersistence, queueName string) *TaskQueue {
	return &TaskQueue{
		persistence: p,
		queueName:   queueName,
	}
}

// Enqueue creates a new task.
func (q *TaskQueue) Enqueue(
	taskType engine.TaskType,
	workflowID string,
	runID string,
	payload map[string]any,
	maxAttempts int,
	notBefore *float64,
	timeoutSeconds *int,
) (engine.Task, error) {
	return q.persistence.CreateTask(
		q.queueName,
		taskType,
		workflowID,
		runID,
		payload,
		maxAttempts,
		notBefore,
		timeoutSeconds,
	)
}

// Poll claims a pending task.
func (q *TaskQueue) Poll(workerID string, leaseSeconds int) (*engine.Task, error) {
	return q.persistence.PollTask(q.queueName, workerID, leaseSeconds)
}

// Complete marks a task complete.
func (q *TaskQueue) Complete(taskID string) error {
	return q.persistence.CompleteTask(taskID)
}

// Fail marks a task failed and reschedules if needed.
func (q *TaskQueue) Fail(taskID string, retryAt *float64) (engine.Task, error) {
	return q.persistence.FailTask(taskID, retryAt)
}
