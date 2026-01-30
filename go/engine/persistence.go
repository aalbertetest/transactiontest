package engine

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"sync"
	"time"

	_ "modernc.org/sqlite"
)

// WorkflowExecution holds persisted execution metadata.
type WorkflowExecution struct {
	WorkflowID   string
	RunID        string
	WorkflowType string
	State        string
	Input        string
	Result       sql.NullString
	Error        sql.NullString
	TaskQueue    string
	StartedAt    int64
	UpdatedAt    int64
	Version      int
}

// SQLiteStore implements persistence using SQLite.
type SQLiteStore struct {
	db *sql.DB
	mu sync.Mutex
}

func NewSQLiteStore(dbPath string) (*SQLiteStore, error) {
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return nil, err
	}
	store := &SQLiteStore{db: db}
	if err := store.InitSchema(); err != nil {
		return nil, err
	}
	return store, nil
}

func (s *SQLiteStore) DB() *sql.DB {
	return s.db
}

func (s *SQLiteStore) InitSchema() error {
	s.mu.Lock()
	defer s.mu.Unlock()
	schema := `
	PRAGMA journal_mode=WAL;

	CREATE TABLE IF NOT EXISTS workflow_executions (
		workflow_id TEXT NOT NULL,
		run_id TEXT NOT NULL,
		workflow_type TEXT NOT NULL,
		state TEXT NOT NULL,
		input TEXT,
		result TEXT,
		error TEXT,
		task_queue TEXT NOT NULL,
		started_at INTEGER NOT NULL,
		updated_at INTEGER NOT NULL,
		version INTEGER NOT NULL,
		PRIMARY KEY (workflow_id, run_id)
	);

	CREATE TABLE IF NOT EXISTS history_events (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		workflow_id TEXT NOT NULL,
		run_id TEXT NOT NULL,
		event_type TEXT NOT NULL,
		event_time INTEGER NOT NULL,
		attributes TEXT NOT NULL
	);

	CREATE INDEX IF NOT EXISTS idx_history_workflow
		ON history_events (workflow_id, run_id, id);

	CREATE TABLE IF NOT EXISTS activity_tasks (
		activity_id TEXT PRIMARY KEY,
		workflow_id TEXT NOT NULL,
		run_id TEXT NOT NULL,
		activity_name TEXT NOT NULL,
		input TEXT NOT NULL,
		state TEXT NOT NULL,
		scheduled_at INTEGER NOT NULL,
		started_at INTEGER,
		completed_at INTEGER,
		heartbeat_at INTEGER,
		heartbeat_details TEXT,
		attempt INTEGER NOT NULL,
		max_attempts INTEGER NOT NULL,
		retry_policy TEXT NOT NULL,
		schedule_to_close_timeout_seconds INTEGER NOT NULL,
		start_to_close_timeout_seconds INTEGER NOT NULL,
		heartbeat_timeout_seconds INTEGER NOT NULL,
		last_failure TEXT
	);

	CREATE INDEX IF NOT EXISTS idx_activity_workflow
		ON activity_tasks (workflow_id, run_id, state);

	CREATE TABLE IF NOT EXISTS timers (
		timer_id TEXT PRIMARY KEY,
		workflow_id TEXT NOT NULL,
		run_id TEXT NOT NULL,
		fire_at INTEGER NOT NULL,
		created_at INTEGER NOT NULL,
		fired_at INTEGER,
		state TEXT NOT NULL
	);

	CREATE INDEX IF NOT EXISTS idx_timers_due
		ON timers (state, fire_at);

	CREATE TABLE IF NOT EXISTS task_queue (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		queue_name TEXT NOT NULL,
		task_type TEXT NOT NULL,
		payload TEXT NOT NULL,
		visible_at INTEGER NOT NULL,
		lease_owner TEXT,
		lease_expires_at INTEGER,
		attempts INTEGER NOT NULL,
		max_attempts INTEGER NOT NULL,
		created_at INTEGER NOT NULL
	);

	CREATE INDEX IF NOT EXISTS idx_task_queue_lookup
		ON task_queue (queue_name, task_type, visible_at, lease_expires_at);
	`
	_, err := s.db.Exec(schema)
	return err
}

func (s *SQLiteStore) CreateWorkflowExecution(
	workflowID, workflowType string,
	inputPayload map[string]interface{},
	taskQueue string,
) (string, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	runID := NewUUID()
	inputJSON, _ := json.Marshal(inputPayload)
	now := time.Now().Unix()

	_, err := s.db.Exec(
		`INSERT INTO workflow_executions (
			workflow_id, run_id, workflow_type, state, input, result, error, task_queue, started_at, updated_at, version
		) VALUES (?, ?, ?, ?, ?, NULL, NULL, ?, ?, ?, 1)`,
		workflowID, runID, workflowType, WorkflowStateRunning, string(inputJSON), taskQueue, now, now,
	)
	if err != nil {
		return "", err
	}
	return runID, nil
}

func (s *SQLiteStore) GetWorkflowExecution(workflowID, runID string) (*WorkflowExecution, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	row := s.db.QueryRow(
		`SELECT workflow_id, run_id, workflow_type, state, input, result, error, task_queue, started_at, updated_at, version
		FROM workflow_executions WHERE workflow_id = ? AND run_id = ?`,
		workflowID, runID,
	)

	var exec WorkflowExecution
	if err := row.Scan(
		&exec.WorkflowID, &exec.RunID, &exec.WorkflowType, &exec.State, &exec.Input,
		&exec.Result, &exec.Error, &exec.TaskQueue, &exec.StartedAt, &exec.UpdatedAt, &exec.Version,
	); err != nil {
		if err == sql.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}
	return &exec, nil
}

func (s *SQLiteStore) SetWorkflowState(workflowID, runID, state string, result map[string]interface{}, errMessage *string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().Unix()
	var resultJSON *string
	if result != nil {
		bytes, _ := json.Marshal(result)
		encoded := string(bytes)
		resultJSON = &encoded
	}

	_, err := s.db.Exec(
		`UPDATE workflow_executions SET state = ?, result = ?, error = ?, updated_at = ? WHERE workflow_id = ? AND run_id = ?`,
		state, resultJSON, errMessage, now, workflowID, runID,
	)
	return err
}

func (s *SQLiteStore) AppendEvent(workflowID, runID, eventType string, attributes map[string]interface{}) (int64, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().Unix()
	attrs, _ := json.Marshal(attributes)
	result, err := s.db.Exec(
		`INSERT INTO history_events (workflow_id, run_id, event_type, event_time, attributes)
		VALUES (?, ?, ?, ?, ?)`,
		workflowID, runID, eventType, now, string(attrs),
	)
	if err != nil {
		return 0, err
	}
	return result.LastInsertId()
}

func (s *SQLiteStore) GetHistory(workflowID, runID string) ([]HistoryEvent, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	rows, err := s.db.Query(
		`SELECT id, event_type, event_time, attributes
		FROM history_events WHERE workflow_id = ? AND run_id = ? ORDER BY id ASC`,
		workflowID, runID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var history []HistoryEvent
	for rows.Next() {
		var event HistoryEvent
		var attrs string
		if err := rows.Scan(&event.EventID, &event.EventType, &event.EventTime, &attrs); err != nil {
			return nil, err
		}
		if err := json.Unmarshal([]byte(attrs), &event.Attributes); err != nil {
			return nil, err
		}
		history = append(history, event)
	}
	return history, nil
}

func (s *SQLiteStore) CreateActivityTask(
	workflowID, runID, activityName string,
	inputPayload map[string]interface{},
	retryPolicy RetryPolicy,
	scheduleToCloseTimeoutSeconds int,
	startToCloseTimeoutSeconds int,
	heartbeatTimeoutSeconds int,
) (string, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	activityID := NewUUID()
	now := time.Now().Unix()
	inputJSON, _ := json.Marshal(inputPayload)
	retryJSON, _ := json.Marshal(retryPolicy)

	_, err := s.db.Exec(
		`INSERT INTO activity_tasks (
			activity_id, workflow_id, run_id, activity_name, input, state, scheduled_at,
			started_at, completed_at, heartbeat_at, heartbeat_details,
			attempt, max_attempts, retry_policy,
			schedule_to_close_timeout_seconds, start_to_close_timeout_seconds,
			heartbeat_timeout_seconds, last_failure
		) VALUES (?, ?, ?, ?, ?, ?, ?, NULL, NULL, NULL, NULL, 0, ?, ?, ?, ?, ?, NULL)`,
		activityID, workflowID, runID, activityName, string(inputJSON), ActivityStateScheduled, now,
		retryPolicy.MaxAttempts, string(retryJSON),
		scheduleToCloseTimeoutSeconds, startToCloseTimeoutSeconds, heartbeatTimeoutSeconds,
	)
	if err != nil {
		return "", err
	}
	return activityID, nil
}

func (s *SQLiteStore) GetActivityTask(activityID string) (*ActivityTask, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	row := s.db.QueryRow(`SELECT * FROM activity_tasks WHERE activity_id = ?`, activityID)
	var task ActivityTask
	var inputJSON string
	var retryJSON string
	var heartbeatDetails sql.NullString
	var startedAt sql.NullInt64
	var completedAt sql.NullInt64
	var heartbeatAt sql.NullInt64
	var lastFailure sql.NullString
	if err := row.Scan(
		&task.ActivityID, &task.WorkflowID, &task.RunID, &task.ActivityName, &inputJSON,
		&task.State, &task.ScheduledAt, &startedAt, &completedAt, &heartbeatAt, &heartbeatDetails,
		&task.Attempt, &task.MaxAttempts, &retryJSON,
		&task.ScheduleToCloseTimeoutSeconds, &task.StartToCloseTimeoutSeconds,
		&task.HeartbeatTimeoutSeconds, &lastFailure,
	); err != nil {
		if err == sql.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}
	if err := json.Unmarshal([]byte(inputJSON), &task.Input); err != nil {
		return nil, err
	}
	if err := json.Unmarshal([]byte(retryJSON), &task.RetryPolicy); err != nil {
		return nil, err
	}
	if heartbeatDetails.Valid {
		_ = json.Unmarshal([]byte(heartbeatDetails.String), &task.HeartbeatDetails)
	}
	if startedAt.Valid {
		task.StartedAt = &startedAt.Int64
	}
	if completedAt.Valid {
		task.CompletedAt = &completedAt.Int64
	}
	if heartbeatAt.Valid {
		task.HeartbeatAt = &heartbeatAt.Int64
	}
	if lastFailure.Valid {
		task.LastFailure = &lastFailure.String
	}
	return &task, nil
}

func (s *SQLiteStore) RecordActivityStarted(activityID, workerID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().Unix()
	heartbeatDetails, _ := json.Marshal(map[string]interface{}{"worker_id": workerID})
	_, err := s.db.Exec(
		`UPDATE activity_tasks SET state = ?, started_at = ?, heartbeat_at = ?, heartbeat_details = ? WHERE activity_id = ?`,
		ActivityStateStarted, now, now, string(heartbeatDetails), activityID,
	)
	return err
}

func (s *SQLiteStore) RecordActivityHeartbeat(activityID string, details map[string]interface{}) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().Unix()
	detailsJSON, _ := json.Marshal(details)
	_, err := s.db.Exec(
		`UPDATE activity_tasks SET heartbeat_at = ?, heartbeat_details = ? WHERE activity_id = ?`,
		now, string(detailsJSON), activityID,
	)
	return err
}

func (s *SQLiteStore) RecordActivityCompleted(activityID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().Unix()
	_, err := s.db.Exec(
		`UPDATE activity_tasks SET state = ?, completed_at = ?, last_failure = NULL WHERE activity_id = ?`,
		ActivityStateCompleted, now, activityID,
	)
	return err
}

func (s *SQLiteStore) RecordActivityFailed(activityID, errMessage string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().Unix()
	_, err := s.db.Exec(
		`UPDATE activity_tasks SET state = ?, completed_at = ?, last_failure = ? WHERE activity_id = ?`,
		ActivityStateFailed, now, errMessage, activityID,
	)
	return err
}

func (s *SQLiteStore) RecordActivityRetrying(activityID, errMessage string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	_, err := s.db.Exec(
		`UPDATE activity_tasks SET state = ?, last_failure = ?, attempt = attempt + 1 WHERE activity_id = ?`,
		ActivityStateRetrying, errMessage, activityID,
	)
	return err
}

func (s *SQLiteStore) RecordActivityTimedOut(activityID, errMessage string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().Unix()
	_, err := s.db.Exec(
		`UPDATE activity_tasks SET state = ?, completed_at = ?, last_failure = ? WHERE activity_id = ?`,
		ActivityStateTimedOut, now, errMessage, activityID,
	)
	return err
}

func (s *SQLiteStore) ListActivityTasksByState(states []string) ([]ActivityTask, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	if len(states) == 0 {
		return nil, nil
	}
	placeholders := ""
	args := make([]interface{}, 0, len(states))
	for i, state := range states {
		if i > 0 {
			placeholders += ","
		}
		placeholders += "?"
		args = append(args, state)
	}
	query := fmt.Sprintf(`SELECT * FROM activity_tasks WHERE state IN (%s)`, placeholders)
	rows, err := s.db.Query(query, args...)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tasks []ActivityTask
	for rows.Next() {
		var task ActivityTask
		var inputJSON string
		var retryJSON string
		var heartbeatDetails sql.NullString
		var startedAt sql.NullInt64
		var completedAt sql.NullInt64
		var heartbeatAt sql.NullInt64
		var lastFailure sql.NullString
		if err := rows.Scan(
			&task.ActivityID, &task.WorkflowID, &task.RunID, &task.ActivityName, &inputJSON,
			&task.State, &task.ScheduledAt, &startedAt, &completedAt, &heartbeatAt, &heartbeatDetails,
			&task.Attempt, &task.MaxAttempts, &retryJSON,
			&task.ScheduleToCloseTimeoutSeconds, &task.StartToCloseTimeoutSeconds,
			&task.HeartbeatTimeoutSeconds, &lastFailure,
		); err != nil {
			return nil, err
		}
		_ = json.Unmarshal([]byte(inputJSON), &task.Input)
		_ = json.Unmarshal([]byte(retryJSON), &task.RetryPolicy)
		if heartbeatDetails.Valid {
			_ = json.Unmarshal([]byte(heartbeatDetails.String), &task.HeartbeatDetails)
		}
		if startedAt.Valid {
			task.StartedAt = &startedAt.Int64
		}
		if completedAt.Valid {
			task.CompletedAt = &completedAt.Int64
		}
		if heartbeatAt.Valid {
			task.HeartbeatAt = &heartbeatAt.Int64
		}
		if lastFailure.Valid {
			task.LastFailure = &lastFailure.String
		}
		tasks = append(tasks, task)
	}
	return tasks, nil
}

func (s *SQLiteStore) CreateTimer(workflowID, runID string, fireAt int64) (string, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	timerID := NewUUID()
	now := time.Now().Unix()
	_, err := s.db.Exec(
		`INSERT INTO timers (timer_id, workflow_id, run_id, fire_at, created_at, fired_at, state)
		VALUES (?, ?, ?, ?, ?, NULL, ?)`,
		timerID, workflowID, runID, fireAt, now, TimerStateScheduled,
	)
	if err != nil {
		return "", err
	}
	return timerID, nil
}

func (s *SQLiteStore) ListDueTimers(now int64) ([]map[string]interface{}, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	rows, err := s.db.Query(
		`SELECT timer_id, workflow_id, run_id, fire_at FROM timers WHERE state = ? AND fire_at <= ? ORDER BY fire_at ASC`,
		TimerStateScheduled, now,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var timers []map[string]interface{}
	for rows.Next() {
		var timerID, workflowID, runID string
		var fireAt int64
		if err := rows.Scan(&timerID, &workflowID, &runID, &fireAt); err != nil {
			return nil, err
		}
		timers = append(timers, map[string]interface{}{
			"timer_id":    timerID,
			"workflow_id": workflowID,
			"run_id":      runID,
			"fire_at":     fireAt,
		})
	}
	return timers, nil
}

func (s *SQLiteStore) MarkTimerFired(timerID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	now := time.Now().Unix()
	_, err := s.db.Exec(`UPDATE timers SET state = ?, fired_at = ? WHERE timer_id = ?`, TimerStateFired, now, timerID)
	return err
}

// ContextTransaction wraps a function in a transaction.
func (s *SQLiteStore) ContextTransaction(ctx context.Context, fn func(tx *sql.Tx) error) error {
	s.mu.Lock()
	defer s.mu.Unlock()

	tx, err := s.db.BeginTx(ctx, &sql.TxOptions{})
	if err != nil {
		return err
	}
	if err := fn(tx); err != nil {
		_ = tx.Rollback()
		return err
	}
	return tx.Commit()
}
