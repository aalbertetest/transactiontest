package engine

import (
	"database/sql"
	"encoding/json"
	"sync"
	"time"

	_ "modernc.org/sqlite"
)

var schemaStatements = []string{
	`CREATE TABLE IF NOT EXISTS workflows (
		workflow_id TEXT PRIMARY KEY,
		workflow_type TEXT NOT NULL,
		status TEXT NOT NULL,
		created_at REAL NOT NULL,
		updated_at REAL NOT NULL,
		current_run_id TEXT NOT NULL,
		run_timeout_seconds INTEGER NOT NULL
	)`,
	`CREATE TABLE IF NOT EXISTS workflow_runs (
		run_id TEXT PRIMARY KEY,
		workflow_id TEXT NOT NULL,
		workflow_type TEXT NOT NULL,
		status TEXT NOT NULL,
		state TEXT NOT NULL,
		state_data TEXT NOT NULL,
		created_at REAL NOT NULL,
		updated_at REAL NOT NULL,
		last_event_id INTEGER DEFAULT 0,
		last_heartbeat_at REAL,
		workflow_task_timeout_seconds INTEGER NOT NULL,
		run_timeout_seconds INTEGER NOT NULL
	)`,
	`CREATE TABLE IF NOT EXISTS history_events (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		run_id TEXT NOT NULL,
		event_type TEXT NOT NULL,
		timestamp REAL NOT NULL,
		attributes TEXT NOT NULL
	)`,
	`CREATE TABLE IF NOT EXISTS tasks (
		task_id TEXT PRIMARY KEY,
		run_id TEXT NOT NULL,
		task_type TEXT NOT NULL,
		queue_name TEXT NOT NULL,
		status TEXT NOT NULL,
		scheduled_at REAL NOT NULL,
		leased_until REAL,
		completed_at REAL,
		attempt INTEGER NOT NULL,
		max_attempts INTEGER NOT NULL,
		payload TEXT NOT NULL,
		last_heartbeat_at REAL,
		heartbeat_timeout_seconds INTEGER,
		timeout_at REAL,
		last_error TEXT
	)`,
	`CREATE INDEX IF NOT EXISTS idx_tasks_queue ON tasks(queue_name, status, scheduled_at)`,
	`CREATE INDEX IF NOT EXISTS idx_events_run ON history_events(run_id, id)`,
	`CREATE INDEX IF NOT EXISTS idx_runs_status ON workflow_runs(status, updated_at)`,
}

type SqlitePersistence struct {
	db  *sql.DB
	mu  sync.Mutex
}

func NewSqlitePersistence(path string) (*SqlitePersistence, error) {
	db, err := sql.Open("sqlite", path)
	if err != nil {
		return nil, err
	}
	p := &SqlitePersistence{db: db}
	if err := p.Initialize(); err != nil {
		return nil, err
	}
	return p, nil
}

func (p *SqlitePersistence) Initialize() error {
	p.mu.Lock()
	defer p.mu.Unlock()
	if _, err := p.db.Exec("PRAGMA journal_mode=WAL"); err != nil {
		return err
	}
	for _, stmt := range schemaStatements {
		if _, err := p.db.Exec(stmt); err != nil {
			return err
		}
	}
	return nil
}

func (p *SqlitePersistence) now() float64 {
	return float64(time.Now().UnixNano()) / 1e9
}

func (p *SqlitePersistence) CreateRun(workflowID, workflowType, runID, state string, stateData map[string]interface{}, runTimeoutSeconds int, workflowTaskTimeoutSeconds int, inputPayload map[string]interface{}) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	now := p.now()
	stateJSON, _ := json.Marshal(stateData)
	inputJSON, _ := json.Marshal(map[string]interface{}{"input": inputPayload})
	_, err := p.db.Exec(
		`INSERT INTO workflows (workflow_id, workflow_type, status, created_at, updated_at, current_run_id, run_timeout_seconds)
		 VALUES (?, ?, ?, ?, ?, ?, ?)`,
		workflowID, workflowType, "RUNNING", now, now, runID, runTimeoutSeconds,
	)
	if err != nil {
		return err
	}
	_, err = p.db.Exec(
		`INSERT INTO workflow_runs (run_id, workflow_id, workflow_type, status, state, state_data, created_at, updated_at, workflow_task_timeout_seconds, run_timeout_seconds)
		 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
		runID, workflowID, workflowType, "RUNNING", state, string(stateJSON), now, now, workflowTaskTimeoutSeconds, runTimeoutSeconds,
	)
	if err != nil {
		return err
	}
	_, err = p.db.Exec(
		`INSERT INTO history_events (run_id, event_type, timestamp, attributes)
		 VALUES (?, ?, ?, ?)`,
		runID, "WorkflowStarted", now, string(inputJSON),
	)
	return err
}

func (p *SqlitePersistence) AppendEvent(runID, eventType string, attributes map[string]interface{}) (HistoryEvent, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	now := p.now()
	attrJSON, _ := json.Marshal(attributes)
	res, err := p.db.Exec(
		`INSERT INTO history_events (run_id, event_type, timestamp, attributes)
		 VALUES (?, ?, ?, ?)`,
		runID, eventType, now, string(attrJSON),
	)
	if err != nil {
		return HistoryEvent{}, err
	}
	eventID, _ := res.LastInsertId()
	_, _ = p.db.Exec(`UPDATE workflow_runs SET last_event_id=?, updated_at=? WHERE run_id=?`, eventID, now, runID)
	return HistoryEvent{
		EventID:    eventID,
		RunID:      runID,
		EventType:  eventType,
		Timestamp:  now,
		Attributes: attributes,
	}, nil
}

func (p *SqlitePersistence) ListEvents(runID string) ([]HistoryEvent, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	rows, err := p.db.Query(`SELECT id, run_id, event_type, timestamp, attributes FROM history_events WHERE run_id=? ORDER BY id ASC`, runID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var events []HistoryEvent
	for rows.Next() {
		var id int64
		var rid, eventType string
		var ts float64
		var attrs string
		if err := rows.Scan(&id, &rid, &eventType, &ts, &attrs); err != nil {
			return nil, err
		}
		events = append(events, HistoryEvent{
			EventID:    id,
			RunID:      rid,
			EventType:  eventType,
			Timestamp:  ts,
			Attributes: decodeJSON(attrs),
		})
	}
	return events, nil
}

func (p *SqlitePersistence) GetRun(runID string) (map[string]interface{}, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	row := p.db.QueryRow(`SELECT run_id, workflow_id, workflow_type, status, state, state_data, created_at, updated_at, workflow_task_timeout_seconds, run_timeout_seconds FROM workflow_runs WHERE run_id=?`, runID)
	var rid, wid, wtype, status, state, stateData string
	var created, updated float64
	var wfTimeout, runTimeout int
	err := row.Scan(&rid, &wid, &wtype, &status, &state, &stateData, &created, &updated, &wfTimeout, &runTimeout)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"run_id":                   rid,
		"workflow_id":              wid,
		"workflow_type":            wtype,
		"status":                   status,
		"state":                    state,
		"state_data":               decodeJSON(stateData),
		"created_at":               created,
		"updated_at":               updated,
		"workflow_task_timeout_seconds": wfTimeout,
		"run_timeout_seconds":      runTimeout,
	}, nil
}

func (p *SqlitePersistence) UpdateRunState(runID, state string, stateData map[string]interface{}, status string) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	now := p.now()
	stateJSON, _ := json.Marshal(stateData)
	_, err := p.db.Exec(`UPDATE workflow_runs SET state=?, state_data=?, status=?, updated_at=? WHERE run_id=?`, state, string(stateJSON), status, now, runID)
	if err != nil {
		return err
	}
	_, _ = p.db.Exec(`UPDATE workflows SET status=?, updated_at=? WHERE current_run_id=?`, status, now, runID)
	return nil
}

func (p *SqlitePersistence) InsertTask(task Task) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	payloadJSON, _ := json.Marshal(task.Payload)
	_, err := p.db.Exec(
		`INSERT INTO tasks (task_id, run_id, task_type, queue_name, status, scheduled_at, leased_until, completed_at, attempt, max_attempts, payload, last_heartbeat_at, heartbeat_timeout_seconds, timeout_at, last_error)
		 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)`,
		task.TaskID, task.RunID, task.TaskType, task.QueueName, task.Status, task.ScheduledAt, task.LeasedUntil, task.CompletedAt, task.Attempt, task.MaxAttempts, string(payloadJSON), task.LastHeartbeatAt, task.HeartbeatTimeoutSeconds, task.TimeoutAt, task.LastError,
	)
	return err
}

func (p *SqlitePersistence) UpdateTaskStatus(taskID, status string, completedAt *float64, lastError *string) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	_, err := p.db.Exec(`UPDATE tasks SET status=?, completed_at=?, last_error=? WHERE task_id=?`, status, completedAt, lastError, taskID)
	return err
}

func (p *SqlitePersistence) UpdateTaskSchedule(taskID string, scheduledAt float64) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	_, err := p.db.Exec(`UPDATE tasks SET status='PENDING', scheduled_at=?, leased_until=NULL WHERE task_id=?`, scheduledAt, taskID)
	return err
}

func (p *SqlitePersistence) UpdateTaskHeartbeat(taskID string, heartbeatAt float64) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	_, err := p.db.Exec(`UPDATE tasks SET last_heartbeat_at=? WHERE task_id=?`, heartbeatAt, taskID)
	return err
}

func (p *SqlitePersistence) GetTask(taskID string) (*Task, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	row := p.db.QueryRow(`SELECT task_id, run_id, task_type, queue_name, status, scheduled_at, leased_until, completed_at, attempt, max_attempts, payload, last_heartbeat_at, heartbeat_timeout_seconds, timeout_at, last_error FROM tasks WHERE task_id=?`, taskID)
	var task Task
	var payload string
	var leasedUntil, completedAt, lastHeartbeatAt, timeoutAt sql.NullFloat64
	var heartbeatTimeout sql.NullInt64
	var lastError sql.NullString
	if err := row.Scan(&task.TaskID, &task.RunID, &task.TaskType, &task.QueueName, &task.Status, &task.ScheduledAt, &leasedUntil, &completedAt, &task.Attempt, &task.MaxAttempts, &payload, &lastHeartbeatAt, &heartbeatTimeout, &timeoutAt, &lastError); err != nil {
		return nil, err
	}
	task.Payload = decodeJSON(payload)
	if leasedUntil.Valid {
		task.LeasedUntil = &leasedUntil.Float64
	}
	if completedAt.Valid {
		task.CompletedAt = &completedAt.Float64
	}
	if lastHeartbeatAt.Valid {
		task.LastHeartbeatAt = &lastHeartbeatAt.Float64
	}
	if heartbeatTimeout.Valid {
		val := int(heartbeatTimeout.Int64)
		task.HeartbeatTimeoutSeconds = &val
	}
	if timeoutAt.Valid {
		task.TimeoutAt = &timeoutAt.Float64
	}
	if lastError.Valid {
		task.LastError = &lastError.String
	}
	return &task, nil
}

func (p *SqlitePersistence) LeaseTasks(queueName string, limit int, leaseSeconds int) ([]Task, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	now := p.now()
	tx, err := p.db.Begin()
	if err != nil {
		return nil, err
	}
	rows, err := tx.Query(
		`SELECT task_id, run_id, task_type, queue_name, status, scheduled_at, leased_until, completed_at, attempt, max_attempts, payload, last_heartbeat_at, heartbeat_timeout_seconds, timeout_at, last_error
		 FROM tasks
		 WHERE queue_name=?
		   AND ((status='PENDING' AND scheduled_at<=?) OR (status='LEASED' AND leased_until<=?))
		   AND (timeout_at IS NULL OR timeout_at>=?)
		 ORDER BY scheduled_at ASC
		 LIMIT ?`,
		queueName, now, now, now, limit,
	)
	if err != nil {
		_ = tx.Rollback()
		return nil, err
	}
	defer rows.Close()
	var leased []Task
	for rows.Next() {
		var task Task
		var payload string
		var leasedUntil, completedAt, lastHeartbeatAt, timeoutAt sql.NullFloat64
		var heartbeatTimeout sql.NullInt64
		var lastError sql.NullString
		if err := rows.Scan(&task.TaskID, &task.RunID, &task.TaskType, &task.QueueName, &task.Status, &task.ScheduledAt, &leasedUntil, &completedAt, &task.Attempt, &task.MaxAttempts, &payload, &lastHeartbeatAt, &heartbeatTimeout, &timeoutAt, &lastError); err != nil {
			_ = tx.Rollback()
			return nil, err
		}
		task.Payload = decodeJSON(payload)
		if task.Attempt >= task.MaxAttempts {
			err = p.updateTaskStatusTx(tx, task.TaskID, "FAILED", nil, strPtr("max_attempts_exceeded"))
			if err != nil {
				_ = tx.Rollback()
				return nil, err
			}
			continue
		}
		attempt := task.Attempt + 1
		leasedUntilVal := now + float64(leaseSeconds)
		_, err := tx.Exec(`UPDATE tasks SET status='LEASED', leased_until=?, attempt=?, last_heartbeat_at=? WHERE task_id=?`, leasedUntilVal, attempt, now, task.TaskID)
		if err != nil {
			_ = tx.Rollback()
			return nil, err
		}
		task.Status = "LEASED"
		task.Attempt = attempt
		task.LeasedUntil = &leasedUntilVal
		task.LastHeartbeatAt = &now
		leased = append(leased, task)
	}
	if err := tx.Commit(); err != nil {
		return nil, err
	}
	return leased, nil
}

func (p *SqlitePersistence) updateTaskStatusTx(tx *sql.Tx, taskID, status string, completedAt *float64, lastError *string) error {
	_, err := tx.Exec(`UPDATE tasks SET status=?, completed_at=?, last_error=? WHERE task_id=?`, status, completedAt, lastError, taskID)
	return err
}

func (p *SqlitePersistence) FindHeartbeatExpiredTasks(now float64) ([]Task, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	rows, err := p.db.Query(
		`SELECT task_id, run_id, task_type, queue_name, status, scheduled_at, leased_until, completed_at, attempt, max_attempts, payload, last_heartbeat_at, heartbeat_timeout_seconds, timeout_at, last_error
		 FROM tasks
		 WHERE status='LEASED'
		   AND heartbeat_timeout_seconds IS NOT NULL
		   AND last_heartbeat_at IS NOT NULL
		   AND last_heartbeat_at + heartbeat_timeout_seconds <= ?`,
		now,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []Task
	for rows.Next() {
		task, err := scanTask(rows)
		if err != nil {
			return nil, err
		}
		out = append(out, task)
	}
	return out, nil
}

func (p *SqlitePersistence) FindTimeoutExpiredTasks(now float64) ([]Task, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	rows, err := p.db.Query(
		`SELECT task_id, run_id, task_type, queue_name, status, scheduled_at, leased_until, completed_at, attempt, max_attempts, payload, last_heartbeat_at, heartbeat_timeout_seconds, timeout_at, last_error
		 FROM tasks
		 WHERE status='LEASED'
		   AND timeout_at IS NOT NULL
		   AND timeout_at <= ?`,
		now,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []Task
	for rows.Next() {
		task, err := scanTask(rows)
		if err != nil {
			return nil, err
		}
		out = append(out, task)
	}
	return out, nil
}

func (p *SqlitePersistence) FindRunTimeouts(now float64) ([]map[string]interface{}, error) {
	p.mu.Lock()
	defer p.mu.Unlock()
	rows, err := p.db.Query(
		`SELECT run_id, workflow_id, workflow_type, state, state_data FROM workflow_runs WHERE status='RUNNING' AND created_at + run_timeout_seconds <= ?`,
		now,
	)
	if err != nil {
		return nil, err
	}
	defer rows.Close()
	var out []map[string]interface{}
	for rows.Next() {
		var runID, workflowID, workflowType, state, stateData string
		if err := rows.Scan(&runID, &workflowID, &workflowType, &state, &stateData); err != nil {
			return nil, err
		}
		out = append(out, map[string]interface{}{
			"run_id":       runID,
			"workflow_id":  workflowID,
			"workflow_type": workflowType,
			"state":        state,
			"state_data":   decodeJSON(stateData),
		})
	}
	return out, nil
}

func scanTask(rows *sql.Rows) (Task, error) {
	var task Task
	var payload string
	var leasedUntil, completedAt, lastHeartbeatAt, timeoutAt sql.NullFloat64
	var heartbeatTimeout sql.NullInt64
	var lastError sql.NullString
	err := rows.Scan(&task.TaskID, &task.RunID, &task.TaskType, &task.QueueName, &task.Status, &task.ScheduledAt, &leasedUntil, &completedAt, &task.Attempt, &task.MaxAttempts, &payload, &lastHeartbeatAt, &heartbeatTimeout, &timeoutAt, &lastError)
	if err != nil {
		return task, err
	}
	task.Payload = decodeJSON(payload)
	if leasedUntil.Valid {
		task.LeasedUntil = &leasedUntil.Float64
	}
	if completedAt.Valid {
		task.CompletedAt = &completedAt.Float64
	}
	if lastHeartbeatAt.Valid {
		task.LastHeartbeatAt = &lastHeartbeatAt.Float64
	}
	if heartbeatTimeout.Valid {
		val := int(heartbeatTimeout.Int64)
		task.HeartbeatTimeoutSeconds = &val
	}
	if timeoutAt.Valid {
		task.TimeoutAt = &timeoutAt.Float64
	}
	if lastError.Valid {
		task.LastError = &lastError.String
	}
	return task, nil
}

func strPtr(value string) *string {
	return &value
}
