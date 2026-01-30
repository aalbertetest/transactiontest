package engine

// WorkflowState represents workflow lifecycle states.
type WorkflowState string

const (
	StateCreated   WorkflowState = "CREATED"
	StateRunning   WorkflowState = "RUNNING"
	StateCompleted WorkflowState = "COMPLETED"
	StateFailed    WorkflowState = "FAILED"
	StateTimedOut  WorkflowState = "TIMED_OUT"
	StateCanceled  WorkflowState = "CANCELED"
	StateTerminated WorkflowState = "TERMINATED"
)

// TaskType represents the task type.
type TaskType string

const (
	TaskWorkflow TaskType = "WORKFLOW_TASK"
	TaskActivity TaskType = "ACTIVITY_TASK"
	TaskTimer    TaskType = "TIMER_TASK"
)

// TaskState represents task state.
type TaskState string

const (
	TaskPending    TaskState = "PENDING"
	TaskInProgress TaskState = "IN_PROGRESS"
	TaskDone       TaskState = "DONE"
	TaskFailed     TaskState = "FAILED"
)

// Event represents an event in workflow history.
type Event struct {
	WorkflowID string
	RunID      string
	EventID    int64
	EventType  string
	Timestamp  float64
	Attributes map[string]any
}

// Task represents a queued task.
type Task struct {
	TaskID        string
	Queue         string
	TaskType      TaskType
	WorkflowID    string
	RunID         string
	Payload       map[string]any
	State         TaskState
	Attempts      int
	MaxAttempts   int
	NotBefore     float64
	CreatedAt     float64
	UpdatedAt     float64
	LeaseExpires  *float64
	WorkerID      *string
	TimeoutSeconds *int
}

// WorkflowExecution captures the durable execution record.
type WorkflowExecution struct {
	WorkflowID  string
	RunID       string
	State       WorkflowState
	WorkflowType string
	Input       map[string]any
	StartedAt   float64
	CompletedAt *float64
	LastEventID int64
	Version     int
}
