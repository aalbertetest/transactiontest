package engine

import "fmt"

type Command struct {
	CommandType string
	Attributes  map[string]interface{}
}

func ScheduleActivity(commandID, activityID, activityName string, input map[string]interface{}, timeoutSeconds int, heartbeatTimeoutSeconds int, retryPolicy RetryPolicy) Command {
	return Command{
		CommandType: "ScheduleActivity",
		Attributes: map[string]interface{}{
			"command_id":              commandID,
			"activity_id":             activityID,
			"activity_name":           activityName,
			"input":                   input,
			"timeout_seconds":         timeoutSeconds,
			"heartbeat_timeout_seconds": heartbeatTimeoutSeconds,
			"retry_policy":            retryPolicy,
		},
	}
}

func ScheduleTimer(commandID, timerID string, timeoutSeconds int) Command {
	return Command{
		CommandType: "ScheduleTimer",
		Attributes: map[string]interface{}{
			"command_id":     commandID,
			"timer_id":       timerID,
			"timeout_seconds": timeoutSeconds,
		},
	}
}

func CompleteWorkflow(result map[string]interface{}) Command {
	return Command{
		CommandType: "CompleteWorkflow",
		Attributes:  map[string]interface{}{"result": result},
	}
}

func FailWorkflow(error string) Command {
	return Command{
		CommandType: "FailWorkflow",
		Attributes:  map[string]interface{}{"error": error},
	}
}

type DecisionResult struct {
	NextState string
	StateData map[string]interface{}
	Commands  []Command
	Complete  bool
	Failure   string
}

type WorkflowDefinition interface {
	Name() string
	InitialState() string
	Decide(ctx *WorkflowContext, state string, stateData map[string]interface{}, history []HistoryEvent) DecisionResult
}

type WorkflowContext struct {
	RunID     string
	StateData map[string]interface{}
	History   []HistoryEvent
	sequence  int
}

func NewWorkflowContext(runID string, stateData map[string]interface{}, history []HistoryEvent) *WorkflowContext {
	seq := 0
	if val, ok := stateData["sequence"].(float64); ok {
		seq = int(val)
	}
	if val, ok := stateData["sequence"].(int); ok {
		seq = val
	}
	return &WorkflowContext{
		RunID:     runID,
		StateData: stateData,
		History:   history,
		sequence:  seq,
	}
}

func (c *WorkflowContext) NextSequence() int {
	c.sequence++
	c.StateData["sequence"] = c.sequence
	return c.sequence
}

func (c *WorkflowContext) EnsureCommandID(prefix, key string) string {
	if existing, ok := c.StateData[key].(string); ok && existing != "" {
		return existing
	}
	cmdID := fmt.Sprintf("%s-%d", prefix, c.NextSequence())
	c.StateData[key] = cmdID
	return cmdID
}

func (c *WorkflowContext) WorkflowInput() map[string]interface{} {
	for _, event := range c.History {
		if event.EventType == "WorkflowStarted" {
			if input, ok := event.Attributes["input"].(map[string]interface{}); ok {
				return input
			}
		}
	}
	return map[string]interface{}{}
}

func (c *WorkflowContext) CurrentTime() float64 {
	var latest float64
	for _, event := range c.History {
		if event.EventType == "WorkflowTaskStarted" || event.EventType == "WorkflowStarted" {
			latest = event.Timestamp
		}
	}
	return latest
}

func (c *WorkflowContext) ActivityCompleted(activityID string) bool {
	for _, event := range c.History {
		if event.EventType == "ActivityCompleted" && event.Attributes["activity_id"] == activityID {
			return true
		}
	}
	return false
}

func (c *WorkflowContext) ActivityResult(activityID string) map[string]interface{} {
	for _, event := range c.History {
		if event.EventType == "ActivityCompleted" && event.Attributes["activity_id"] == activityID {
			if result, ok := event.Attributes["result"].(map[string]interface{}); ok {
				return result
			}
		}
	}
	return nil
}

func (c *WorkflowContext) TimerFired(timerID string) bool {
	for _, event := range c.History {
		if event.EventType == "TimerFired" && event.Attributes["timer_id"] == timerID {
			return true
		}
	}
	return false
}
