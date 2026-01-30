package engine

import (
	"database/sql"
	"encoding/json"
	"sync"
	"time"
)

// TaskQueue defines the queue abstraction.
type TaskQueue interface {
	Enqueue(queueName, taskType string, payload map[string]interface{}, visibleAt *int64, maxAttempts int) (int64, error)
	Poll(queueName, taskType string, leaseDurationSeconds int, workerID string) (*QueueTask, error)
	Ack(taskID int64) error
	Nack(taskID int64, delaySeconds int) error
}

// DBTaskQueue implements TaskQueue using SQLite.
type DBTaskQueue struct {
	db      *sql.DB
	mu      sync.Mutex
	metrics *MetricsRegistry
}

func NewDBTaskQueue(db *sql.DB, metrics *MetricsRegistry) *DBTaskQueue {
	return &DBTaskQueue{db: db, metrics: metrics}
}

func (q *DBTaskQueue) Enqueue(queueName, taskType string, payload map[string]interface{}, visibleAt *int64, maxAttempts int) (int64, error) {
	q.mu.Lock()
	defer q.mu.Unlock()

	now := time.Now().Unix()
	if visibleAt == nil {
		visibleAt = &now
	}
	payloadJSON, _ := json.Marshal(payload)
	result, err := q.db.Exec(
		`INSERT INTO task_queue (
			queue_name, task_type, payload, visible_at, lease_owner, lease_expires_at, attempts, max_attempts, created_at
		) VALUES (?, ?, ?, ?, NULL, NULL, 0, ?, ?)`,
		queueName, taskType, string(payloadJSON), *visibleAt, maxAttempts, now,
	)
	if err != nil {
		return 0, err
	}
	if q.metrics != nil {
		q.metrics.Inc("queue.enqueue", 1)
	}
	return result.LastInsertId()
}

func (q *DBTaskQueue) Poll(queueName, taskType string, leaseDurationSeconds int, workerID string) (*QueueTask, error) {
	q.mu.Lock()
	defer q.mu.Unlock()

	now := time.Now().Unix()
	leaseExpires := now + int64(leaseDurationSeconds)

	tx, err := q.db.Begin()
	if err != nil {
		return nil, err
	}
	defer tx.Rollback()

	row := tx.QueryRow(
		`SELECT id FROM task_queue
		WHERE queue_name = ? AND task_type = ? AND visible_at <= ?
		  AND (lease_expires_at IS NULL OR lease_expires_at <= ?)
		  AND attempts < max_attempts
		ORDER BY id LIMIT 1`,
		queueName, taskType, now, now,
	)
	var taskID int64
	if err := row.Scan(&taskID); err != nil {
		if err == sql.ErrNoRows {
			_ = tx.Commit()
			return nil, nil
		}
		return nil, err
	}

	result, err := tx.Exec(
		`UPDATE task_queue
		SET lease_owner = ?, lease_expires_at = ?, attempts = attempts + 1
		WHERE id = ? AND (lease_expires_at IS NULL OR lease_expires_at <= ?)`,
		workerID, leaseExpires, taskID, now,
	)
	if err != nil {
		return nil, err
	}
	affected, _ := result.RowsAffected()
	if affected == 0 {
		_ = tx.Commit()
		return nil, nil
	}

	row = tx.QueryRow(
		`SELECT id, queue_name, task_type, payload, visible_at, lease_owner, lease_expires_at, attempts, max_attempts
		FROM task_queue WHERE id = ?`,
		taskID,
	)
	var task QueueTask
	var payloadJSON string
	var leaseOwner sql.NullString
	var leaseExpiresAt sql.NullInt64
	if err := row.Scan(
		&task.ID, &task.QueueName, &task.TaskType, &payloadJSON, &task.VisibleAt,
		&leaseOwner, &leaseExpiresAt, &task.Attempts, &task.MaxAttempts,
	); err != nil {
		return nil, err
	}
	if leaseOwner.Valid {
		task.LeaseOwner = &leaseOwner.String
	}
	if leaseExpiresAt.Valid {
		task.LeaseExpiresAt = &leaseExpiresAt.Int64
	}
	if err := json.Unmarshal([]byte(payloadJSON), &task.Payload); err != nil {
		return nil, err
	}
	if err := tx.Commit(); err != nil {
		return nil, err
	}
	if q.metrics != nil {
		q.metrics.Inc("queue.poll", 1)
	}
	return &task, nil
}

func (q *DBTaskQueue) Ack(taskID int64) error {
	q.mu.Lock()
	defer q.mu.Unlock()

	_, err := q.db.Exec(`DELETE FROM task_queue WHERE id = ?`, taskID)
	if err == nil && q.metrics != nil {
		q.metrics.Inc("queue.ack", 1)
	}
	return err
}

func (q *DBTaskQueue) Nack(taskID int64, delaySeconds int) error {
	q.mu.Lock()
	defer q.mu.Unlock()

	visibleAt := time.Now().Unix() + int64(delaySeconds)
	_, err := q.db.Exec(
		`UPDATE task_queue SET visible_at = ?, lease_owner = NULL, lease_expires_at = NULL WHERE id = ?`,
		visibleAt, taskID,
	)
	if err == nil && q.metrics != nil {
		q.metrics.Inc("queue.nack", 1)
	}
	return err
}
