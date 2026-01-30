package engine

import (
	"time"

	"github.com/google/uuid"
)

type TaskQueue struct {
	persistence *SqlitePersistence
}

func NewTaskQueue(persistence *SqlitePersistence) *TaskQueue {
	return &TaskQueue{persistence: persistence}
}

func (q *TaskQueue) EnqueueTask(runID, taskType, queueName string, payload map[string]interface{}, scheduledAt *float64, timeoutSeconds *int, heartbeatTimeoutSeconds *int, maxAttempts int) (string, error) {
	taskID := uuid.NewString()
	now := float64(time.Now().UnixNano()) / 1e9
	scheduled := now
	if scheduledAt != nil {
		scheduled = *scheduledAt
	}
	var timeoutAt *float64
	if timeoutSeconds != nil {
		value := scheduled + float64(*timeoutSeconds)
		timeoutAt = &value
	}
	task := Task{
		TaskID:                  taskID,
		RunID:                   runID,
		TaskType:                taskType,
		QueueName:               queueName,
		Status:                  "PENDING",
		ScheduledAt:             scheduled,
		Attempt:                 0,
		MaxAttempts:             maxAttempts,
		Payload:                 payload,
		HeartbeatTimeoutSeconds: heartbeatTimeoutSeconds,
		TimeoutAt:               timeoutAt,
	}
	if err := q.persistence.InsertTask(task); err != nil {
		return "", err
	}
	return taskID, nil
}

func (q *TaskQueue) LeaseTasks(queueName string, limit int, leaseSeconds int) ([]Task, error) {
	return q.persistence.LeaseTasks(queueName, limit, leaseSeconds)
}

func (q *TaskQueue) CompleteTask(taskID string) error {
	now := float64(time.Now().UnixNano()) / 1e9
	return q.persistence.UpdateTaskStatus(taskID, "COMPLETED", &now, nil)
}

func (q *TaskQueue) FailTask(taskID string, error string) error {
	now := float64(time.Now().UnixNano()) / 1e9
	return q.persistence.UpdateTaskStatus(taskID, "FAILED", &now, &error)
}

func (q *TaskQueue) RescheduleTask(taskID string, scheduledAt float64) error {
	return q.persistence.UpdateTaskSchedule(taskID, scheduledAt)
}

func (q *TaskQueue) Heartbeat(taskID string) error {
	now := float64(time.Now().UnixNano()) / 1e9
	return q.persistence.UpdateTaskHeartbeat(taskID, now)
}

func (q *TaskQueue) GetTask(taskID string) (*Task, error) {
	return q.persistence.GetTask(taskID)
}
