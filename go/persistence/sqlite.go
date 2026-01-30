package persistence

import (
	"database/sql"
	"encoding/json"
	"errors"
	"strconv"
	"sync"
	"time"

	_ "modernc.org/sqlite"

	"workflow/engine"
)

// SQLitePersistence implements durable persistence on SQLite.
type SQLitePersistence struct {
	db   *sql.DB
	lock sync.Mutex
}

// NewSQLitePersistence opens the database and initializes schema.
func NewSQLitePersistence(dbPath string) (*SQLitePersistence, error) {
	db, err := sql.Open("sqlite", dbPath)
	if err != nil {
		return nil, err
	}
	p := &SQLitePersistence{db: db}
	if err := p.initSchema(); err != nil {
		return nil, err
	}
	return p, nil
}

func (p *SQLitePersistence) initSchema() error {
	p.lock.Lock()
	defer p.lock.Unlock()
	queries := []string{
		`PRAGMA journal_mode=WAL`,
		`PRAGMA synchronous=NORMAL`,
		`PRAGMA foreign_keys=ON`,
		`PRAGMA busy_timeout=5000`,
		`CREATE TABLE IF NOT EXISTS workflow_executions (
			workflow_id TEXT NOT NULL,
			run_id TEXT NOT NULL,
			state TEXT NOT NULL,
			workflow_type TEXT NOT NULL,
			input_json TEXT NOT NULL,
			started_at REAL NOT NULL,
			completed_at REAL,
			last_event_id INTEGER NOT NULL,
			version INTEGER NOT NULL,
			PRIMARY KEY (workflow_id, run_id)
		)`,
		`CREATE TABLE IF NOT EXISTS workflow_events (
			workflow_id TEXT NOT NULL,
			run_id TEXT NOT NULL,
			event_id INTEGER NOT NULL,
			event_type TEXT NOT NULL,
			timestamp REAL NOT NULL,
			attributes_json TEXT NOT NULL,
			PRIMARY KEY (workflow_id, run_id, event_id)
		)`,
		`CREATE TABLE IF NOT EXISTS tasks (
			task_id TEXT PRIMARY KEY,
			queue TEXT NOT NULL,
			task_type TEXT NOT NULL,
			workflow_id TEXT NOT NULL,
			run_id TEXT NOT NULL,
			payload_json TEXT NOT NULL,
			state TEXT NOT NULL,
			attempts INTEGER NOT NULL,
			max_attempts INTEGER NOT NULL,
			not_before REAL NOT NULL,
			created_at REAL NOT NULL,
			updated_at REAL NOT NULL,
			lease_expires_at REAL,
			worker_id TEXT,
			timeout_seconds INTEGER
		)`,
		`CREATE TABLE IF NOT EXISTS activity_heartbeats (
			task_id TEXT PRIMARY KEY,
			workflow_id TEXT NOT NULL,
			run_id TEXT NOT NULL,
			last_heartbeat REAL NOT NULL,
			details_json TEXT NOT NULL
		)`,
		`CREATE INDEX IF NOT EXISTS idx_tasks_queue_state ON tasks(queue, state, not_before)`,
		`CREATE INDEX IF NOT EXISTS idx_tasks_lease ON tasks(state, lease_expires_at)`,
		`CREATE INDEX IF NOT EXISTS idx_tasks_type_state ON tasks(task_type, state, not_before)`,
	}
	for _, query := range queries {
		if _, err := p.db.Exec(query); err != nil {
			return err
		}
	}
	return nil
}

func now() float64 {
	return float64(time.Now().UnixNano()) / 1e9
}

func encodeJSON(value map[string]any) (string, error) {
	if value == nil {
		value = map[string]any{}
	}
	data, err := json.Marshal(value)
	if err != nil {
		return "", err
	}
	return string(data), nil
}

func decodeJSON(data string) (map[string]any, error) {
	if data == "" {
		return map[string]any{}, nil
	}
	var result map[string]any
	if err := json.Unmarshal([]byte(data), &result); err != nil {
		return nil, err
	}
	return result, nil
}

// CreateWorkflowExecution creates a workflow execution record.
func (p *SQLitePersistence) CreateWorkflowExecution(workflowID string, runID string, workflowType string, input map[string]any) (engine.WorkflowExecution, error) {
	p.lock.Lock()
	defer p.lock.Unlock()
	payload, err := encodeJSON(input)
	if err != nil {
		return engine.WorkflowExecution{}, err
	}
	startedAt := now()
	_, err = p.db.Exec(
		`INSERT INTO workflow_executions
		(workflow_id, run_id, state, workflow_type, input_json, started_at, completed_at, last_event_id, version)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)`,
		workflowID,
		runID,
		engine.StateRunning,
		workflowType,
		payload,
		startedAt,
		nil,
		0,
		1,
	)
	if err != nil {
		return engine.WorkflowExecution{}, err
	}
	return engine.WorkflowExecution{
		WorkflowID:  workflowID,
		RunID:       runID,
		State:       engine.StateRunning,
		WorkflowType: workflowType,
		Input:       input,
		StartedAt:   startedAt,
		CompletedAt: nil,
		LastEventID: 0,
		Version:     1,
	}, nil
}

// GetWorkflowExecution returns the workflow execution record.
func (p *SQLitePersistence) GetWorkflowExecution(workflowID string, runID string) (engine.WorkflowExecution, error) {
	row := p.db.QueryRow(
		`SELECT workflow_id, run_id, state, workflow_type, input_json, started_at, completed_at, last_event_id, version
		FROM workflow_executions WHERE workflow_id = ? AND run_id = ?`,
		workflowID, runID,
	)
	var inputJSON string
	var state string
	var startedAt float64
	var completedAt sql.NullFloat64
	var lastEventID int64
	var version int
	var wfType string
	if err := row.Scan(&workflowID, &runID, &state, &wfType, &inputJSON, &startedAt, &completedAt, &lastEventID, &version); err != nil {
		return engine.WorkflowExecution{}, err
	}
	input, err := decodeJSON(inputJSON)
	if err != nil {
		return engine.WorkflowExecution{}, err
	}
	var completedPtr *float64
	if completedAt.Valid {
		completedPtr = &completedAt.Float64
	}
	return engine.WorkflowExecution{
		WorkflowID:  workflowID,
		RunID:       runID,
		State:       engine.WorkflowState(state),
		WorkflowType: wfType,
		Input:       input,
		StartedAt:   startedAt,
		CompletedAt: completedPtr,
		LastEventID: lastEventID,
		Version:     version,
	}, nil
}

// UpdateWorkflowState updates workflow state.
func (p *SQLitePersistence) UpdateWorkflowState(workflowID string, runID string, state engine.WorkflowState, completedAt *float64) error {
	p.lock.Lock()
	defer p.lock.Unlock()
	_, err := p.db.Exec(
		`UPDATE workflow_executions SET state = ?, completed_at = ? WHERE workflow_id = ? AND run_id = ?`,
		state, completedAt, workflowID, runID,
	)
	return err
}

// AppendEvent appends an event and increments last_event_id.
func (p *SQLitePersistence) AppendEvent(workflowID string, runID string, eventType string, attributes map[string]any) (engine.Event, error) {
	p.lock.Lock()
	defer p.lock.Unlock()
	row := p.db.QueryRow(`SELECT last_event_id FROM workflow_executions WHERE workflow_id = ? AND run_id = ?`, workflowID, runID)
	var lastEventID int64
	if err := row.Scan(&lastEventID); err != nil {
		return engine.Event{}, err
	}
	nextID := lastEventID + 1
	payload, err := encodeJSON(attributes)
	if err != nil {
		return engine.Event{}, err
	}
	ts := now()
	if _, err := p.db.Exec(
		`INSERT INTO workflow_events (workflow_id, run_id, event_id, event_type, timestamp, attributes_json)
		VALUES (?, ?, ?, ?, ?, ?)`,
		workflowID, runID, nextID, eventType, ts, payload,
	); err != nil {
		return engine.Event{}, err
	}
	if _, err := p.db.Exec(
		`UPDATE workflow_executions SET last_event_id = ? WHERE workflow_id = ? AND run_id = ?`,
		nextID, workflowID, runID,
	); err != nil {
		return engine.Event{}, err
	}
	return engine.Event{
		WorkflowID: workflowID,
		RunID:      runID,
		EventID:    nextID,
		EventType:  eventType,
		Timestamp:  ts,
		Attributes: attributes,
	}, nil
}

// ListEvents returns ordered workflow history.
func (p *SQLitePersistence) ListEvents(workflowID string, runID string) ([]engine.Event, error) {
	rows, err := p.db.Query(
		`SELECT workflow_id, run_id, event_id, event_type, timestamp, attributes_json
		FROM workflow_events WHERE workflow_id = ? AND run_id = ? ORDER BY event_id ASC`,
		workflowID, runID,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var events []engine.Event
	for rows.Next() {
		var event engine.Event
		var attrs string
		if err := rows.Scan(&event.WorkflowID, &event.RunID, &event.EventID, &event.EventType, &event.Timestamp, &attrs); err != nil {
			return nil, err
		}
		decoded, err := decodeJSON(attrs)
		if err != nil {
			return nil, err
		}
		event.Attributes = decoded
		events = append(events, event)
	}
	return events, nil
}

// CreateTask inserts a new task.
func (p *SQLitePersistence) CreateTask(queue string, taskType engine.TaskType, workflowID string, runID string, payload map[string]any, maxAttempts int, notBefore *float64, timeoutSeconds *int) (engine.Task, error) {
	p.lock.Lock()
	defer p.lock.Unlock()
	payloadJSON, err := encodeJSON(payload)
	if err != nil {
		return engine.Task{}, err
	}
	taskID := generateID()
	nowValue := now()
	notBeforeValue := nowValue
	if notBefore != nil {
		notBeforeValue = *notBefore
	}
	_, err = p.db.Exec(
		`INSERT INTO tasks
		(task_id, queue, task_type, workflow_id, run_id, payload_json, state, attempts, max_attempts, not_before, created_at, updated_at, lease_expires_at, worker_id, timeout_seconds)
		VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
		taskID, queue, taskType, workflowID, runID, payloadJSON, engine.TaskPending, 0, maxAttempts, notBeforeValue, nowValue, nowValue, nil, nil, timeoutSeconds,
	)
	if err != nil {
		return engine.Task{}, err
	}
	return engine.Task{
		TaskID:        taskID,
		Queue:         queue,
		TaskType:      taskType,
		WorkflowID:    workflowID,
		RunID:         runID,
		Payload:       payload,
		State:         engine.TaskPending,
		Attempts:      0,
		MaxAttempts:   maxAttempts,
		NotBefore:     notBeforeValue,
		CreatedAt:     nowValue,
		UpdatedAt:     nowValue,
		LeaseExpires:  nil,
		WorkerID:      nil,
		TimeoutSeconds: timeoutSeconds,
	}, nil
}

// PollTask claims a pending task.
func (p *SQLitePersistence) PollTask(queue string, workerID string, leaseSeconds int) (*engine.Task, error) {
	p.lock.Lock()
	defer p.lock.Unlock()
	row := p.db.QueryRow(
		`SELECT task_id, queue, task_type, workflow_id, run_id, payload_json, state, attempts, max_attempts, not_before, created_at, updated_at, lease_expires_at, worker_id, timeout_seconds
		FROM tasks WHERE queue = ? AND state = ? AND not_before <= ? ORDER BY created_at ASC LIMIT 1`,
		queue, engine.TaskPending, now(),
	)
	task, err := scanTaskRow(row)
	if err != nil {
		if errors.Is(err, sql.ErrNoRows) {
			return nil, nil
		}
		return nil, err
	}
	lease := now() + float64(leaseSeconds)
	_, err = p.db.Exec(
		`UPDATE tasks SET state = ?, updated_at = ?, lease_expires_at = ?, worker_id = ? WHERE task_id = ?`,
		engine.TaskInProgress, now(), lease, workerID, task.TaskID,
	)
	if err != nil {
		return nil, err
	}
	task.State = engine.TaskInProgress
	task.LeaseExpires = &lease
	task.WorkerID = &workerID
	return &task, nil
}

// CompleteTask marks a task done.
func (p *SQLitePersistence) CompleteTask(taskID string) error {
	p.lock.Lock()
	defer p.lock.Unlock()
	_, err := p.db.Exec(
		`UPDATE tasks SET state = ?, updated_at = ?, lease_expires_at = NULL WHERE task_id = ?`,
		engine.TaskDone, now(), taskID,
	)
	return err
}

// FailTask marks a task failed and optionally reschedules.
func (p *SQLitePersistence) FailTask(taskID string, retryAt *float64) (engine.Task, error) {
	p.lock.Lock()
	defer p.lock.Unlock()
	row := p.db.QueryRow(
		`SELECT task_id, queue, task_type, workflow_id, run_id, payload_json, state, attempts, max_attempts, not_before, created_at, updated_at, lease_expires_at, worker_id, timeout_seconds
		FROM tasks WHERE task_id = ?`, taskID,
	)
	task, err := scanTaskRow(row)
	if err != nil {
		return engine.Task{}, err
	}
	task.Attempts++
	state := engine.TaskPending
	if task.Attempts >= task.MaxAttempts {
		state = engine.TaskFailed
	}
	notBefore := now()
	if retryAt != nil {
		notBefore = *retryAt
	}
	_, err = p.db.Exec(
		`UPDATE tasks SET state = ?, attempts = ?, not_before = ?, updated_at = ?, lease_expires_at = NULL WHERE task_id = ?`,
		state, task.Attempts, notBefore, now(), taskID,
	)
	if err != nil {
		return engine.Task{}, err
	}
	task.State = state
	task.NotBefore = notBefore
	return task, nil
}

// HeartbeatTask records heartbeat and extends lease.
func (p *SQLitePersistence) HeartbeatTask(taskID string, details map[string]any, leaseSeconds int) error {
	p.lock.Lock()
	defer p.lock.Unlock()
	detailsJSON, err := encodeJSON(details)
	if err != nil {
		return err
	}
	lease := now() + float64(leaseSeconds)
	if _, err := p.db.Exec(
		`UPDATE tasks SET lease_expires_at = ?, updated_at = ? WHERE task_id = ?`,
		lease, now(), taskID,
	); err != nil {
		return err
	}
	_, err = p.db.Exec(
		`INSERT INTO activity_heartbeats (task_id, workflow_id, run_id, last_heartbeat, details_json)
		VALUES (?, ?, ?, ?, ?)
		ON CONFLICT(task_id) DO UPDATE SET last_heartbeat = excluded.last_heartbeat, details_json = excluded.details_json`,
		taskID, details["workflow_id"], details["run_id"], now(), detailsJSON,
	)
	return err
}

// ListDueTimers returns due timer tasks.
func (p *SQLitePersistence) ListDueTimers() ([]engine.Task, error) {
	rows, err := p.db.Query(
		`SELECT task_id, queue, task_type, workflow_id, run_id, payload_json, state, attempts, max_attempts, not_before, created_at, updated_at, lease_expires_at, worker_id, timeout_seconds
		FROM tasks WHERE task_type = ? AND state = ? AND not_before <= ? ORDER BY not_before ASC`,
		engine.TaskTimer, engine.TaskPending, now(),
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	return scanTasks(rows)
}

// ListExpiredLeases returns tasks with expired leases.
func (p *SQLitePersistence) ListExpiredLeases() ([]engine.Task, error) {
	rows, err := p.db.Query(
		`SELECT task_id, queue, task_type, workflow_id, run_id, payload_json, state, attempts, max_attempts, not_before, created_at, updated_at, lease_expires_at, worker_id, timeout_seconds
		FROM tasks WHERE state = ? AND lease_expires_at IS NOT NULL AND lease_expires_at <= ? ORDER BY lease_expires_at ASC`,
		engine.TaskInProgress, now(),
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	return scanTasks(rows)
}

func scanTasks(rows *sql.Rows) ([]engine.Task, error) {
	var tasks []engine.Task
	for rows.Next() {
		task, err := scanTaskRow(rows)
		if err != nil {
			return nil, err
		}
		tasks = append(tasks, task)
	}
	return tasks, nil
}

func scanTaskRow(scanner interface {
	Scan(dest ...any) error
}) (engine.Task, error) {
	var payloadJSON string
	var state string
	var taskType string
	var lease sql.NullFloat64
	var worker sql.NullString
	var timeout sql.NullInt64
	task := engine.Task{}
	if err := scanner.Scan(
		&task.TaskID,
		&task.Queue,
		&taskType,
		&task.WorkflowID,
		&task.RunID,
		&payloadJSON,
		&state,
		&task.Attempts,
		&task.MaxAttempts,
		&task.NotBefore,
		&task.CreatedAt,
		&task.UpdatedAt,
		&lease,
		&worker,
		&timeout,
	); err != nil {
		return engine.Task{}, err
	}
	payload, err := decodeJSON(payloadJSON)
	if err != nil {
		return engine.Task{}, err
	}
	task.TaskType = engine.TaskType(taskType)
	task.State = engine.TaskState(state)
	task.Payload = payload
	if lease.Valid {
		task.LeaseExpires = &lease.Float64
	}
	if worker.Valid {
		task.WorkerID = &worker.String
	}
	if timeout.Valid {
		val := int(timeout.Int64)
		task.TimeoutSeconds = &val
	}
	return task, nil
}

func generateID() string {
	// Use time-based uniqueness with nanoseconds.
	return strconv.FormatInt(time.Now().UnixNano(), 10)
}
