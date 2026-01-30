package engine

import (
	"fmt"
	"time"

	"github.com/google/uuid"
)

type ActivityFunc func(ctx *ActivityContext, input map[string]interface{}) (map[string]interface{}, error)

type ActivityDefinition struct {
	Name                    string
	Func                    ActivityFunc
	RetryPolicy             RetryPolicy
	TimeoutSeconds          int
	HeartbeatTimeoutSeconds int
}

type ActivityContext struct {
	engine *WorkflowEngine
	taskID string
}

func (c *ActivityContext) Heartbeat() {
	_ = c.engine.Queue.Heartbeat(c.taskID)
	c.engine.Metrics.Counter("activity_heartbeats_total").Inc("default", 1)
}

type WorkflowEngine struct {
	Config      Config
	Logger      *Logger
	Persistence *SqlitePersistence
	Queue       *TaskQueue
	Metrics     *MetricsRegistry
	workflows   map[string]WorkflowDefinition
	activities  map[string]ActivityDefinition
}

func NewWorkflowEngine(config Config) (*WorkflowEngine, error) {
	persistence, err := NewSqlitePersistence(config.DBPath)
	if err != nil {
		return nil, err
	}
	engine := &WorkflowEngine{
		Config:      config,
		Logger:      NewLogger("engine"),
		Persistence: persistence,
		Queue:       NewTaskQueue(persistence),
		Metrics:     NewMetricsRegistry(),
		workflows:   map[string]WorkflowDefinition{},
		activities:  map[string]ActivityDefinition{},
	}
	return engine, nil
}

func (e *WorkflowEngine) RegisterWorkflow(def WorkflowDefinition) {
	e.workflows[def.Name()] = def
}

func (e *WorkflowEngine) RegisterActivity(name string, fn ActivityFunc, retryPolicy *RetryPolicy, timeoutSeconds *int, heartbeatTimeoutSeconds *int) {
	policy := DefaultRetryPolicy()
	if retryPolicy != nil {
		policy = *retryPolicy
	}
	timeout := e.Config.WorkflowTaskTimeoutSeconds
	if timeoutSeconds != nil {
		timeout = *timeoutSeconds
	}
	heartbeat := e.Config.ActivityHeartbeatTimeoutSeconds
	if heartbeatTimeoutSeconds != nil {
		heartbeat = *heartbeatTimeoutSeconds
	}
	e.activities[name] = ActivityDefinition{
		Name:                    name,
		Func:                    fn,
		RetryPolicy:             policy,
		TimeoutSeconds:          timeout,
		HeartbeatTimeoutSeconds: heartbeat,
	}
}

func (e *WorkflowEngine) StartWorkflow(workflowType, workflowID string, inputPayload map[string]interface{}, runTimeoutSeconds *int) (string, error) {
	definition, ok := e.workflows[workflowType]
	if !ok {
		return "", fmt.Errorf("unknown workflow type %s", workflowType)
	}
	runID := uuid.NewString()
	timeout := e.Config.RunTimeoutSeconds
	if runTimeoutSeconds != nil {
		timeout = *runTimeoutSeconds
	}
	err := e.Persistence.CreateRun(workflowID, workflowType, runID, definition.InitialState(), map[string]interface{}{"sequence": 0}, timeout, e.Config.WorkflowTaskTimeoutSeconds, inputPayload)
	if err != nil {
		return "", err
	}
	_, err = e.EnqueueWorkflowTask(runID)
	if err != nil {
		return "", err
	}
	return runID, nil
}

func (e *WorkflowEngine) EnqueueWorkflowTask(runID string) (string, error) {
	timeout := e.Config.WorkflowTaskTimeoutSeconds
	return e.Queue.EnqueueTask(runID, "workflow_task", e.Config.WorkflowTaskQueue, map[string]interface{}{"run_id": runID}, nil, &timeout, nil, e.Config.MaxTaskAttempts)
}

func (e *WorkflowEngine) EnqueueActivityTask(runID string, payload map[string]interface{}, timeoutSeconds int, heartbeatTimeoutSeconds int, maxAttempts int) (string, error) {
	return e.Queue.EnqueueTask(runID, "activity_task", e.Config.ActivityTaskQueue, payload, nil, &timeoutSeconds, &heartbeatTimeoutSeconds, maxAttempts)
}

func (e *WorkflowEngine) EnqueueTimerTask(runID string, payload map[string]interface{}, fireAt float64) (string, error) {
	return e.Queue.EnqueueTask(runID, "timer_task", e.Config.TimerTaskQueue, payload, &fireAt, nil, nil, e.Config.MaxTaskAttempts)
}

func (e *WorkflowEngine) ProcessWorkflowTask(task Task) error {
	run, err := e.Persistence.GetRun(task.RunID)
	if err != nil {
		return err
	}
	if run["status"] != "RUNNING" {
		_ = e.Queue.CompleteTask(task.TaskID)
		return nil
	}
	_, _ = e.Persistence.AppendEvent(task.RunID, "WorkflowTaskStarted", map[string]interface{}{"task_id": task.TaskID})
	history, err := e.Persistence.ListEvents(task.RunID)
	if err != nil {
		return err
	}
	def := e.workflows[run["workflow_type"].(string)]
	stateData := run["state_data"].(map[string]interface{})
	ctx := NewWorkflowContext(task.RunID, stateData, history)
	decision := def.Decide(ctx, run["state"].(string), ctx.StateData, history)
	e.applyDecision(task.RunID, decision, history)
	_ = e.Queue.CompleteTask(task.TaskID)
	e.Metrics.Counter("workflow_tasks_completed_total").Inc("default", 1)
	return nil
}

func (e *WorkflowEngine) applyDecision(runID string, decision DecisionResult, history []HistoryEvent) {
	status := "RUNNING"
	terminalFromCommand := ""
	for _, cmd := range decision.Commands {
		e.applyCommand(runID, cmd, history)
		if cmd.CommandType == "CompleteWorkflow" {
			terminalFromCommand = "COMPLETED"
		}
		if cmd.CommandType == "FailWorkflow" {
			terminalFromCommand = "FAILED"
		}
	}
	if terminalFromCommand != "" {
		status = terminalFromCommand
	} else if decision.Complete {
		status = "COMPLETED"
		_, _ = e.Persistence.AppendEvent(runID, "WorkflowCompleted", map[string]interface{}{"result": map[string]interface{}{"status": "completed"}})
	} else if decision.Failure != "" {
		status = "FAILED"
		_, _ = e.Persistence.AppendEvent(runID, "WorkflowFailed", map[string]interface{}{"error": decision.Failure})
	}
	_ = e.Persistence.UpdateRunState(runID, decision.NextState, decision.StateData, status)
	_, _ = e.Persistence.AppendEvent(runID, "WorkflowTaskCompleted", map[string]interface{}{
		"state":    decision.NextState,
		"commands": e.commandTypes(decision.Commands),
	})
}

func (e *WorkflowEngine) commandTypes(commands []Command) []string {
	out := make([]string, 0, len(commands))
	for _, cmd := range commands {
		out = append(out, cmd.CommandType)
	}
	return out
}

func (e *WorkflowEngine) applyCommand(runID string, command Command, history []HistoryEvent) {
	switch command.CommandType {
	case "ScheduleActivity":
		e.applyScheduleActivity(runID, command, history)
	case "ScheduleTimer":
		e.applyScheduleTimer(runID, command, history)
	case "CompleteWorkflow":
		_, _ = e.Persistence.AppendEvent(runID, "WorkflowCompleted", map[string]interface{}{"result": command.Attributes["result"]})
	case "FailWorkflow":
		_, _ = e.Persistence.AppendEvent(runID, "WorkflowFailed", map[string]interface{}{"error": command.Attributes["error"]})
	}
}

func (e *WorkflowEngine) historyHasCommand(history []HistoryEvent, eventType, commandID string) bool {
	for _, event := range history {
		if event.EventType == eventType {
			if cmdID, ok := event.Attributes["command_id"].(string); ok && cmdID == commandID {
				return true
			}
		}
	}
	return false
}

func (e *WorkflowEngine) applyScheduleActivity(runID string, command Command, history []HistoryEvent) {
	commandID, ok := command.Attributes["command_id"].(string)
	if !ok || commandID == "" {
		panic("ScheduleActivity requires command_id")
	}
	if e.historyHasCommand(history, "ActivityScheduled", commandID) {
		return
	}
	activityName, _ := command.Attributes["activity_name"].(string)
	if _, ok := e.activities[activityName]; !ok {
		panic(fmt.Sprintf("unknown activity %s", activityName))
	}
	activityID, _ := command.Attributes["activity_id"].(string)
	input, _ := command.Attributes["input"].(map[string]interface{})
	timeoutSeconds := intFromAttribute(command.Attributes["timeout_seconds"])
	heartbeatSeconds := intFromAttribute(command.Attributes["heartbeat_timeout_seconds"])
	retryPolicy := retryPolicyFromAttribute(command.Attributes["retry_policy"])

	_, _ = e.Persistence.AppendEvent(runID, "ActivityScheduled", map[string]interface{}{
		"command_id":               commandID,
		"activity_id":              activityID,
		"activity_name":            activityName,
		"input":                    input,
		"timeout_seconds":          timeoutSeconds,
		"heartbeat_timeout_seconds": heartbeatSeconds,
		"retry_policy":             retryPolicy,
	})
	_, _ = e.EnqueueActivityTask(runID, map[string]interface{}{
		"run_id":        runID,
		"activity_id":   activityID,
		"activity_name": activityName,
		"input":         input,
		"retry_policy":  retryPolicy,
	}, timeoutSeconds, heartbeatSeconds, retryPolicy.MaxAttempts)
}

func (e *WorkflowEngine) applyScheduleTimer(runID string, command Command, history []HistoryEvent) {
	commandID, ok := command.Attributes["command_id"].(string)
	if !ok || commandID == "" {
		panic("ScheduleTimer requires command_id")
	}
	if e.historyHasCommand(history, "TimerScheduled", commandID) {
		return
	}
	timerID, _ := command.Attributes["timer_id"].(string)
	timeoutSeconds := intFromAttribute(command.Attributes["timeout_seconds"])
	fireAt := float64(time.Now().UnixNano())/1e9 + float64(timeoutSeconds)
	_, _ = e.Persistence.AppendEvent(runID, "TimerScheduled", map[string]interface{}{
		"command_id": commandID,
		"timer_id":   timerID,
		"fire_at":    fireAt,
	})
	_, _ = e.EnqueueTimerTask(runID, map[string]interface{}{"run_id": runID, "timer_id": timerID}, fireAt)
}

func (e *WorkflowEngine) RecordActivityStarted(runID, activityID, taskID string, attempt int) {
	_, _ = e.Persistence.AppendEvent(runID, "ActivityStarted", map[string]interface{}{
		"activity_id": activityID,
		"task_id":     taskID,
		"attempt":     attempt,
	})
}

func (e *WorkflowEngine) RecordActivityCompleted(runID, activityID, taskID string, attempt int, result map[string]interface{}) {
	_, _ = e.Persistence.AppendEvent(runID, "ActivityCompleted", map[string]interface{}{
		"activity_id": activityID,
		"task_id":     taskID,
		"attempt":     attempt,
		"result":      result,
	})
	_, _ = e.EnqueueWorkflowTask(runID)
}

func (e *WorkflowEngine) RecordActivityFailed(runID, activityID, taskID string, attempt int, err string, retryPolicy RetryPolicy) {
	_, _ = e.Persistence.AppendEvent(runID, "ActivityFailed", map[string]interface{}{
		"activity_id": activityID,
		"task_id":     taskID,
		"attempt":     attempt,
		"error":       err,
	})
	if ShouldRetry(attempt, retryPolicy) {
		backoff := ComputeBackoffSeconds(attempt, retryPolicy)
		scheduledAt := float64(time.Now().UnixNano())/1e9 + backoff
		_ = e.Queue.RescheduleTask(taskID, scheduledAt)
		_, _ = e.Persistence.AppendEvent(runID, "ActivityRetryScheduled", map[string]interface{}{
			"activity_id":    activityID,
			"attempt":        attempt + 1,
			"backoff_seconds": backoff,
		})
	} else {
		_, _ = e.EnqueueWorkflowTask(runID)
	}
}

func (e *WorkflowEngine) RecordTimerFired(runID, timerID string) {
	_, _ = e.Persistence.AppendEvent(runID, "TimerFired", map[string]interface{}{
		"timer_id": timerID,
	})
	_, _ = e.EnqueueWorkflowTask(runID)
}

func (e *WorkflowEngine) RecordTaskTimeout(taskID string) {
	task, err := e.Queue.GetTask(taskID)
	if err != nil || task == nil {
		return
	}
	_ = e.Queue.FailTask(taskID, "timeout")
	if task.TaskType == "activity_task" {
		retryPolicy := retryPolicyFromAttribute(task.Payload["retry_policy"])
		activityID, _ := task.Payload["activity_id"].(string)
		e.RecordActivityFailed(task.RunID, activityID, taskID, task.Attempt, "timeout", retryPolicy)
	}
}

func (e *WorkflowEngine) RecordHeartbeatTimeout(taskID string) {
	task, err := e.Queue.GetTask(taskID)
	if err != nil || task == nil {
		return
	}
	_ = e.Queue.FailTask(taskID, "heartbeat_timeout")
	if task.TaskType == "activity_task" {
		retryPolicy := retryPolicyFromAttribute(task.Payload["retry_policy"])
		activityID, _ := task.Payload["activity_id"].(string)
		e.RecordActivityFailed(task.RunID, activityID, taskID, task.Attempt, "heartbeat_timeout", retryPolicy)
	}
}

func (e *WorkflowEngine) RecordRunTimeout(runID string) {
	_, _ = e.Persistence.AppendEvent(runID, "WorkflowFailed", map[string]interface{}{"error": "run_timeout"})
	_ = e.Persistence.UpdateRunState(runID, "FAILED", map[string]interface{}{}, "FAILED")
}

func retryPolicyFromAttribute(value interface{}) RetryPolicy {
	switch v := value.(type) {
	case RetryPolicy:
		return v
	case map[string]interface{}:
		policy := DefaultRetryPolicy()
		if val, ok := v["initial_interval_seconds"].(float64); ok {
			policy.InitialIntervalSeconds = val
		}
		if val, ok := v["backoff_coefficient"].(float64); ok {
			policy.BackoffCoefficient = val
		}
		if val, ok := v["max_interval_seconds"].(float64); ok {
			policy.MaxIntervalSeconds = val
		}
		if val, ok := v["max_attempts"].(float64); ok {
			policy.MaxAttempts = int(val)
		}
		return policy
	default:
		return DefaultRetryPolicy()
	}
}

func intFromAttribute(value interface{}) int {
	switch v := value.(type) {
	case int:
		return v
	case float64:
		return int(v)
	default:
		return 0
	}
}
