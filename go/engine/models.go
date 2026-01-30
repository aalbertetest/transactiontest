package engine

import (
	"encoding/json"
)

// Event type constants.
const (
	EventWorkflowExecutionStarted   = "WorkflowExecutionStarted"
	EventWorkflowExecutionCompleted = "WorkflowExecutionCompleted"
	EventWorkflowExecutionFailed    = "WorkflowExecutionFailed"
	EventWorkflowExecutionSignaled  = "WorkflowExecutionSignaled"
	EventWorkflowTaskScheduled      = "WorkflowTaskScheduled"
	EventWorkflowTaskStarted        = "WorkflowTaskStarted"
	EventWorkflowTaskCompleted      = "WorkflowTaskCompleted"
	EventActivityTaskScheduled      = "ActivityTaskScheduled"
	EventActivityTaskStarted        = "ActivityTaskStarted"
	EventActivityTaskCompleted      = "ActivityTaskCompleted"
	EventActivityTaskFailed         = "ActivityTaskFailed"
	EventActivityTaskTimedOut       = "ActivityTaskTimedOut"
	EventActivityTaskRetryScheduled = "ActivityTaskRetryScheduled"
	EventTimerScheduled             = "TimerScheduled"
	EventTimerFired                 = "TimerFired"
	EventSignalReceived             = "SignalReceived"
	EventVersionMarkerRecorded      = "VersionMarkerRecorded"
)

// Workflow states.
const (
	WorkflowStateRunning    = "RUNNING"
	WorkflowStateWaiting    = "WAITING"
	WorkflowStateCompleted  = "COMPLETED"
	WorkflowStateFailed     = "FAILED"
	WorkflowStateTerminated = "TERMINATED"
)

// Activity states.
const (
	ActivityStateScheduled = "SCHEDULED"
	ActivityStateStarted   = "STARTED"
	ActivityStateCompleted = "COMPLETED"
	ActivityStateFailed    = "FAILED"
	ActivityStateTimedOut  = "TIMED_OUT"
	ActivityStateRetrying  = "RETRYING"
)

// Timer states.
const (
	TimerStateScheduled = "SCHEDULED"
	TimerStateFired     = "FIRED"
)

// RetryPolicy is serialized into history and activity tasks.
type RetryPolicy struct {
	InitialIntervalSeconds int     `json:"initial_interval_seconds"`
	MaxIntervalSeconds     int     `json:"max_interval_seconds"`
	BackoffCoefficient     float64 `json:"backoff_coefficient"`
	MaxAttempts            int     `json:"max_attempts"`
}

// HistoryEvent is a persisted history record.
type HistoryEvent struct {
	EventID    int64                  `json:"event_id"`
	EventType  string                 `json:"event_type"`
	EventTime  int64                  `json:"event_time"`
	Attributes map[string]interface{} `json:"attributes"`
}

func (e HistoryEvent) AttributesJSON() string {
	bytes, _ := json.Marshal(e.Attributes)
	return string(bytes)
}

// QueueTask is a task fetched from the task queue.
type QueueTask struct {
	ID             int64
	QueueName      string
	TaskType       string
	Payload        map[string]interface{}
	VisibleAt      int64
	LeaseOwner     *string
	LeaseExpiresAt *int64
	Attempts       int
	MaxAttempts    int
}

// ActivityTask is a durable activity execution record.
type ActivityTask struct {
	ActivityID                    string
	WorkflowID                    string
	RunID                         string
	ActivityName                  string
	Input                         map[string]interface{}
	State                         string
	ScheduledAt                   int64
	StartedAt                     *int64
	CompletedAt                   *int64
	HeartbeatAt                   *int64
	HeartbeatDetails              map[string]interface{}
	Attempt                       int
	MaxAttempts                   int
	RetryPolicy                   RetryPolicy
	ScheduleToCloseTimeoutSeconds int
	StartToCloseTimeoutSeconds    int
	HeartbeatTimeoutSeconds       int
	LastFailure                   *string
}
