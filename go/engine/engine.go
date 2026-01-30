package engine

import (
	"encoding/json"
	"errors"
	"fmt"
	"reflect"
	"sync"
	"time"

	"github.com/google/uuid"

	"workflow/backoff"
	"workflow/config"
	"workflow/logging"
	"workflow/metrics"
	"workflow/persistence"
	"workflow/queue"
)

const (
	EventWorkflowStarted       = "WorkflowStarted"
	EventWorkflowTaskScheduled = "WorkflowTaskScheduled"
	EventWorkflowTaskStarted   = "WorkflowTaskStarted"
	EventWorkflowTaskCompleted = "WorkflowTaskCompleted"
	EventWorkflowCompleted     = "WorkflowCompleted"
	EventWorkflowFailed        = "WorkflowFailed"
	EventActivityScheduled     = "ActivityScheduled"
	EventActivityStarted       = "ActivityStarted"
	EventActivityCompleted     = "ActivityCompleted"
	EventActivityFailed        = "ActivityFailed"
	EventActivityTimedOut      = "ActivityTimedOut"
	EventTimerStarted          = "TimerStarted"
	EventTimerFired            = "TimerFired"
	EventMarkerRecorded        = "MarkerRecorded"
)

// WorkflowContext provides deterministic access to history and scheduling.
type WorkflowContext struct {
	WorkflowID string
	RunID      string
	history    []Event
	commands   []map[string]any
	activitySeq int
	timerSeq    int
	scheduledActivities map[string]map[string]any
	completedActivities map[string]map[string]any
	failedActivities    map[string]map[string]any
	startedTimers       map[string]map[string]any
	firedTimers         map[string]map[string]any
	markers             map[string]int
}

func NewWorkflowContext(workflowID string, runID string, history []Event) *WorkflowContext {
	ctx := &WorkflowContext{
		WorkflowID:           workflowID,
		RunID:                runID,
		history:              history,
		commands:             []map[string]any{},
		scheduledActivities:  map[string]map[string]any{},
		completedActivities:  map[string]map[string]any{},
		failedActivities:     map[string]map[string]any{},
		startedTimers:        map[string]map[string]any{},
		firedTimers:          map[string]map[string]any{},
		markers:              map[string]int{},
	}
	ctx.indexHistory()
	return ctx
}

func (c *WorkflowContext) indexHistory() {
	for _, event := range c.history {
		switch event.EventType {
		case EventActivityScheduled:
			c.scheduledActivities[event.Attributes["activity_id"].(string)] = event.Attributes
		case EventActivityCompleted:
			c.completedActivities[event.Attributes["activity_id"].(string)] = event.Attributes
		case EventActivityFailed:
			c.failedActivities[event.Attributes["activity_id"].(string)] = event.Attributes
		case EventTimerStarted:
			c.startedTimers[event.Attributes["timer_id"].(string)] = event.Attributes
		case EventTimerFired:
			c.firedTimers[event.Attributes["timer_id"].(string)] = event.Attributes
		case EventMarkerRecorded:
			c.markers[event.Attributes["change_id"].(string)] = int(event.Attributes["version"].(float64))
		}
	}
}

// Commands returns the commands emitted by workflow execution.
func (c *WorkflowContext) Commands() []map[string]any {
	return c.commands
}

// RunActivity schedules an activity or returns its recorded result.
func (c *WorkflowContext) RunActivity(
	name string,
	input map[string]any,
	timeoutSeconds *int,
	maxAttempts *int,
	heartbeatIntervalSeconds *int,
) (map[string]any, error) {
	normalizedInput := normalizeMap(input)
	activityID := c.WorkflowID + ":activity:" + itoa(c.activitySeq)
	c.activitySeq++

	if completed, ok := c.completedActivities[activityID]; ok {
		return completed["result"].(map[string]any), nil
	}
	if failed, ok := c.failedActivities[activityID]; ok {
		return nil, WorkflowApplicationError{Message: failed["error"].(string)}
	}
	if scheduled, ok := c.scheduledActivities[activityID]; ok {
		if scheduled["name"].(string) != name {
			return nil, DeterminismError{Message: "activity name changed during replay"}
		}
		if !mapsEqual(scheduled["input"].(map[string]any), normalizedInput) {
			return nil, DeterminismError{Message: "activity input changed during replay"}
		}
		return nil, PendingActivity{ActivityID: activityID}
	}

	c.commands = append(c.commands, map[string]any{
		"type":                     "ScheduleActivity",
		"activity_id":              activityID,
		"name":                     name,
		"input":                    normalizedInput,
		"timeout_seconds":          timeoutSeconds,
		"max_attempts":             maxAttempts,
		"heartbeat_interval_seconds": heartbeatIntervalSeconds,
	})
	return nil, PendingActivity{ActivityID: activityID}
}

// Sleep schedules a durable timer.
func (c *WorkflowContext) Sleep(seconds float64) error {
	timerID := c.WorkflowID + ":timer:" + itoa(c.timerSeq)
	c.timerSeq++

	if _, ok := c.firedTimers[timerID]; ok {
		return nil
	}
	if started, ok := c.startedTimers[timerID]; ok {
		if started["timeout_seconds"].(float64) != seconds {
			return DeterminismError{Message: "timer duration changed during replay"}
		}
		return PendingTimer{TimerID: timerID}
	}

	c.commands = append(c.commands, map[string]any{
		"type":            "StartTimer",
		"timer_id":        timerID,
		"timeout_seconds": seconds,
	})
	return PendingTimer{TimerID: timerID}
}

// GetVersion records or returns version markers.
func (c *WorkflowContext) GetVersion(changeID string, minVersion int, maxVersion int) int {
	if version, ok := c.markers[changeID]; ok {
		return version
	}
	c.commands = append(c.commands, map[string]any{
		"type":      "RecordMarker",
		"change_id": changeID,
		"version":   maxVersion,
	})
	return maxVersion
}

// ActivityContext provides activity helpers such as heartbeats.
type ActivityContext struct {
	engine                  *WorkflowEngine
	task                    *Task
	heartbeatIntervalSeconds *int
	lastDetails             map[string]any
	stop                    chan struct{}
	wg                      sync.WaitGroup
}

func NewActivityContext(engine *WorkflowEngine, task *Task, heartbeatIntervalSeconds *int) *ActivityContext {
	return &ActivityContext{
		engine:                  engine,
		task:                    task,
		heartbeatIntervalSeconds: heartbeatIntervalSeconds,
		lastDetails:             map[string]any{},
		stop:                    make(chan struct{}),
	}
}

func (a *ActivityContext) StartHeartbeatLoop() {
	if a.heartbeatIntervalSeconds == nil {
		return
	}
	a.wg.Add(1)
	go func() {
		defer a.wg.Done()
		ticker := time.NewTicker(time.Duration(*a.heartbeatIntervalSeconds) * time.Second)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				a.Heartbeat(a.lastDetails)
			case <-a.stop:
				return
			}
		}
	}()
}

func (a *ActivityContext) Heartbeat(details map[string]any) {
	a.lastDetails = details
	_ = a.engine.persistence.HeartbeatTask(
		a.task.TaskID,
		map[string]any{
			"workflow_id": a.task.WorkflowID,
			"run_id":      a.task.RunID,
			"details":     details,
		},
		a.engine.config.LeaseSeconds,
	)
}

func (a *ActivityContext) Stop() {
	close(a.stop)
	a.wg.Wait()
}

// WorkflowHandler is the workflow function signature.
type WorkflowHandler func(ctx *WorkflowContext, input map[string]any) (any, error)

// ActivityHandler is the activity function signature.
type ActivityHandler func(ctx *ActivityContext, input map[string]any) (any, error)

// WorkflowEngine orchestrates workflows, tasks, and persistence.
type WorkflowEngine struct {
	config        config.EngineConfig
	persistence   *persistence.SQLitePersistence
	workflowQueue *queue.TaskQueue
	activityQueue *queue.TaskQueue
	logger        *logging.Logger
	metrics       *metrics.Registry
	workflows     map[string]WorkflowHandler
	activities    map[string]ActivityHandler
}

// NewWorkflowEngine creates a new engine.
func NewWorkflowEngine(cfg config.EngineConfig, p *persistence.SQLitePersistence) *WorkflowEngine {
	return &WorkflowEngine{
		config:        cfg,
		persistence:   p,
		workflowQueue: queue.NewTaskQueue(p, cfg.WorkflowQueue),
		activityQueue: queue.NewTaskQueue(p, cfg.ActivityQueue),
		logger:        logging.New(cfg.LogLevel),
		metrics:       metrics.NewRegistry(),
		workflows:     map[string]WorkflowHandler{},
		activities:    map[string]ActivityHandler{},
	}
}

// WorkflowQueue exposes the workflow task queue for workers.
func (e *WorkflowEngine) WorkflowQueue() *queue.TaskQueue {
	return e.workflowQueue
}

// ActivityQueue exposes the activity task queue for workers.
func (e *WorkflowEngine) ActivityQueue() *queue.TaskQueue {
	return e.activityQueue
}

// Persistence exposes the persistence layer.
func (e *WorkflowEngine) Persistence() *persistence.SQLitePersistence {
	return e.persistence
}

// RegisterWorkflow registers a workflow function.
func (e *WorkflowEngine) RegisterWorkflow(name string, handler WorkflowHandler) {
	e.workflows[name] = handler
}

// RegisterActivity registers an activity function.
func (e *WorkflowEngine) RegisterActivity(name string, handler ActivityHandler) {
	e.activities[name] = handler
}

// StartWorkflow starts a new workflow execution.
func (e *WorkflowEngine) StartWorkflow(workflowType string, input map[string]any) (WorkflowExecution, error) {
	workflowID := uuid.New().String()
	if value, ok := input["workflow_id"]; ok {
		if typed, ok := value.(string); ok {
			workflowID = typed
		}
	}
	runID := uuid.New().String()
	execution, err := e.persistence.CreateWorkflowExecution(workflowID, runID, workflowType, input)
	if err != nil {
		return execution, err
	}
	// WorkflowStarted anchors the deterministic history.
	_, _ = e.persistence.AppendEvent(workflowID, runID, EventWorkflowStarted, map[string]any{
		"workflow_type": workflowType,
		"input":         input,
	})
	// First workflow task kicks off decision processing.
	e.scheduleWorkflowTask(workflowID, runID)
	e.metrics.Counter("workflows_started").Inc(1)
	return execution, nil
}

func (e *WorkflowEngine) scheduleWorkflowTask(workflowID string, runID string) {
	_, _ = e.persistence.AppendEvent(workflowID, runID, EventWorkflowTaskScheduled, map[string]any{
		"queue": e.config.WorkflowQueue,
	})
	_, _ = e.workflowQueue.Enqueue(
		TaskWorkflow,
		workflowID,
		runID,
		map[string]any{},
		e.config.WorkflowMaxAttempts,
		nil,
		ptrInt(e.config.WorkflowTaskTimeoutSeconds),
	)
}

func (e *WorkflowEngine) scheduleActivityTask(
	workflowID string,
	runID string,
	activityID string,
	name string,
	input map[string]any,
	timeoutSeconds *int,
	maxAttempts *int,
	heartbeatIntervalSeconds *int,
	notBefore *float64,
) {
	_, _ = e.persistence.AppendEvent(workflowID, runID, EventActivityScheduled, map[string]any{
		"activity_id":              activityID,
		"name":                     name,
		"input":                    input,
		"timeout_seconds":          timeoutSeconds,
		"max_attempts":             maxAttempts,
		"heartbeat_interval_seconds": heartbeatIntervalSeconds,
	})
	maxAttemptsValue := e.config.ActivityMaxAttempts
	if maxAttempts != nil {
		maxAttemptsValue = *maxAttempts
	}
	timeoutValue := e.config.ActivityTaskTimeoutSeconds
	if timeoutSeconds != nil {
		timeoutValue = *timeoutSeconds
	}
	_, _ = e.activityQueue.Enqueue(
		TaskActivity,
		workflowID,
		runID,
		map[string]any{
			"activity_id":              activityID,
			"name":                     name,
			"input":                    input,
			"heartbeat_interval_seconds": heartbeatIntervalSeconds,
		},
		maxAttemptsValue,
		notBefore,
		ptrInt(timeoutValue),
	)
}

func (e *WorkflowEngine) startTimer(workflowID string, runID string, timerID string, timeoutSeconds float64) {
	fireAt := nowSeconds() + timeoutSeconds
	_, _ = e.persistence.AppendEvent(workflowID, runID, EventTimerStarted, map[string]any{
		"timer_id":        timerID,
		"timeout_seconds": timeoutSeconds,
	})
	_, _ = e.persistence.CreateTask("timer", TaskTimer, workflowID, runID, map[string]any{
		"timer_id": timerID,
	}, 1, &fireAt, nil)
}

// ExecuteWorkflowTask runs a workflow task and applies commands.
func (e *WorkflowEngine) ExecuteWorkflowTask(task *Task, workerID string) {
	execution, err := e.persistence.GetWorkflowExecution(task.WorkflowID, task.RunID)
	if err != nil {
		e.logger.Error("Failed to load workflow execution: %v", err)
		return
	}
	if execution.State != StateRunning {
		_ = e.workflowQueue.Complete(task.TaskID)
		return
	}
	// Record start so replays show which worker processed the decision.
	_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventWorkflowTaskStarted, map[string]any{
		"worker_id": workerID,
	})
	history, err := e.persistence.ListEvents(task.WorkflowID, task.RunID)
	if err != nil {
		e.logger.Error("Failed to load history: %v", err)
		return
	}
	// The context replays history to enforce deterministic behavior.
	ctx := NewWorkflowContext(task.WorkflowID, task.RunID, history)
	workflowFn, ok := e.workflows[execution.WorkflowType]
	if !ok {
		e.logger.Error("Workflow not registered: %s", execution.WorkflowType)
		return
	}
	result, err := workflowFn(ctx, execution.Input)
	if err == nil {
		ctx.commands = append(ctx.commands, map[string]any{
			"type":   "CompleteWorkflow",
			"result": result,
		})
	} else {
		var pendingActivity PendingActivity
		var pendingTimer PendingTimer
		if errors.As(err, &pendingActivity) || errors.As(err, &pendingTimer) {
			// Pending external event.
		} else {
			ctx.commands = append(ctx.commands, map[string]any{
				"type":  "FailWorkflow",
				"error": err.Error(),
			})
		}
	}

	for _, cmd := range ctx.commands {
		switch cmd["type"] {
		case "ScheduleActivity":
			// Activity scheduling creates an ActivityScheduled event and task.
			e.scheduleActivityTask(
				task.WorkflowID,
				task.RunID,
				cmd["activity_id"].(string),
				cmd["name"].(string),
				cmd["input"].(map[string]any),
				optionalInt(cmd["timeout_seconds"]),
				optionalInt(cmd["max_attempts"]),
				optionalInt(cmd["heartbeat_interval_seconds"]),
				nil,
			)
		case "StartTimer":
			// Timers are delivered by the scheduler as durable tasks.
			e.startTimer(
				task.WorkflowID,
				task.RunID,
				cmd["timer_id"].(string),
				cmd["timeout_seconds"].(float64),
			)
		case "RecordMarker":
			// Markers support deterministic versioning.
			_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventMarkerRecorded, map[string]any{
				"change_id": cmd["change_id"].(string),
				"version":   cmd["version"].(int),
			})
		case "CompleteWorkflow":
			// Terminal success state.
			_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventWorkflowCompleted, map[string]any{
				"result": cmd["result"],
			})
			_ = ValidateTransition(execution.State, StateCompleted)
			completed := nowSeconds()
			_ = e.persistence.UpdateWorkflowState(task.WorkflowID, task.RunID, StateCompleted, &completed)
			e.metrics.Counter("workflows_completed").Inc(1)
		case "FailWorkflow":
			// Terminal failure state.
			_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventWorkflowFailed, map[string]any{
				"error": cmd["error"].(string),
			})
			_ = ValidateTransition(execution.State, StateFailed)
			completed := nowSeconds()
			_ = e.persistence.UpdateWorkflowState(task.WorkflowID, task.RunID, StateFailed, &completed)
			e.metrics.Counter("workflows_failed").Inc(1)
		}
	}
	_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventWorkflowTaskCompleted, map[string]any{
		"worker_id": workerID,
	})
	_ = e.workflowQueue.Complete(task.TaskID)
}

// ExecuteActivityTask runs the activity and reports result.
func (e *WorkflowEngine) ExecuteActivityTask(task *Task, workerID string) {
	activityID := task.Payload["activity_id"].(string)
	name := task.Payload["name"].(string)
	input := task.Payload["input"].(map[string]any)
	handler, ok := e.activities[name]
	if !ok {
		e.logger.Error("Activity not registered: %s", name)
		return
	}
	// Record ActivityStarted before running user code.
	_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventActivityStarted, map[string]any{
		"activity_id": activityID,
		"worker_id":   workerID,
	})
	ctx := NewActivityContext(e, task, optionalInt(task.Payload["heartbeat_interval_seconds"]))
	ctx.StartHeartbeatLoop()
	result, err := handler(ctx, input)
	ctx.Stop()
	if err == nil {
		// Successful completion: record and resume workflow.
		_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventActivityCompleted, map[string]any{
			"activity_id": activityID,
			"result":      result,
		})
		_ = e.activityQueue.Complete(task.TaskID)
		e.scheduleWorkflowTask(task.WorkflowID, task.RunID)
		e.metrics.Counter("activities_completed").Inc(1)
		return
	}
	_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventActivityFailed, map[string]any{
		"activity_id": activityID,
		"error":       err.Error(),
	})
	delay := backoff.Compute(task.Attempts+1, e.config.BackoffInitialSeconds, e.config.BackoffMaxSeconds, e.config.BackoffJitter)
	retryAt := nowSeconds() + delay
	taskUpdate, _ := e.activityQueue.Fail(task.TaskID, &retryAt)
	if taskUpdate.State == TaskFailed {
		// Resume workflow once retries are exhausted.
		e.scheduleWorkflowTask(task.WorkflowID, task.RunID)
	}
	e.metrics.Counter("activities_failed").Inc(1)
}

// HandleTimerTask delivers a timer and schedules workflow task.
func (e *WorkflowEngine) HandleTimerTask(task *Task) {
	timerID := task.Payload["timer_id"].(string)
	_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventTimerFired, map[string]any{
		"timer_id": timerID,
	})
	_ = e.persistence.CompleteTask(task.TaskID)
	e.scheduleWorkflowTask(task.WorkflowID, task.RunID)
}

// HandleTaskTimeout handles expired leases.
func (e *WorkflowEngine) HandleTaskTimeout(task *Task) {
	switch task.TaskType {
	case TaskActivity:
		activityID := task.Payload["activity_id"].(string)
		// Timeout is a failure that may be retried.
		_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventActivityTimedOut, map[string]any{
			"activity_id": activityID,
		})
		delay := backoff.Compute(task.Attempts+1, e.config.BackoffInitialSeconds, e.config.BackoffMaxSeconds, e.config.BackoffJitter)
		retryAt := nowSeconds() + delay
		taskUpdate, _ := e.activityQueue.Fail(task.TaskID, &retryAt)
		if taskUpdate.State == TaskFailed {
			e.scheduleWorkflowTask(task.WorkflowID, task.RunID)
		}
	case TaskWorkflow:
		delay := backoff.Compute(task.Attempts+1, e.config.BackoffInitialSeconds, e.config.BackoffMaxSeconds, e.config.BackoffJitter)
		retryAt := nowSeconds() + delay
		taskUpdate, _ := e.workflowQueue.Fail(task.TaskID, &retryAt)
		if taskUpdate.State == TaskFailed {
			_, _ = e.persistence.AppendEvent(task.WorkflowID, task.RunID, EventWorkflowFailed, map[string]any{
				"error": "workflow task timed out and max attempts exceeded",
			})
			completed := nowSeconds()
			_ = e.persistence.UpdateWorkflowState(task.WorkflowID, task.RunID, StateFailed, &completed)
		}
	default:
		_ = e.persistence.CompleteTask(task.TaskID)
	}
}

func nowSeconds() float64 {
	return float64(time.Now().UnixNano()) / 1e9
}

func ptrInt(value int) *int {
	return &value
}

func optionalInt(value any) *int {
	if value == nil {
		return nil
	}
	switch typed := value.(type) {
	case int:
		return &typed
	case *int:
		return typed
	case float64:
		converted := int(typed)
		return &converted
	}
	return nil
}

func itoa(value int) string {
	return fmt.Sprintf("%d", value)
}

func mapsEqual(a map[string]any, b map[string]any) bool {
	if len(a) != len(b) {
		return false
	}
	for key, value := range a {
		if bvalue, ok := b[key]; ok {
			if !reflect.DeepEqual(value, bvalue) {
				return false
			}
		} else {
			return false
		}
	}
	return true
}

func normalizeMap(input map[string]any) map[string]any {
	if input == nil {
		return map[string]any{}
	}
	data, err := json.Marshal(input)
	if err != nil {
		return input
	}
	var result map[string]any
	if err := json.Unmarshal(data, &result); err != nil {
		return input
	}
	return result
}
