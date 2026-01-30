package engine

import (
	"fmt"
)

// WorkflowFunc defines the signature for workflow code.
type WorkflowFunc func(ctx *WorkflowContext, input map[string]interface{}) (interface{}, error)

// ActivityOptions configures activity execution.
type ActivityOptions struct {
	RetryPolicy                   *RetryPolicy
	ScheduleToCloseTimeoutSeconds int
	StartToCloseTimeoutSeconds    int
	HeartbeatTimeoutSeconds       int
}

// WorkflowContext provides deterministic APIs for workflow code.
type WorkflowContext struct {
	runner *WorkflowRunner
}

// ExecuteActivity schedules or replays an activity deterministically.
func (ctx *WorkflowContext) ExecuteActivity(name string, input map[string]interface{}, opts *ActivityOptions) (interface{}, error) {
	return ctx.runner.handleActivity(name, input, opts)
}

// Sleep schedules or replays a timer deterministically.
func (ctx *WorkflowContext) Sleep(durationSeconds int) error {
	_, err := ctx.runner.handleTimer(durationSeconds)
	return err
}

// WaitSignal blocks until a signal is available.
func (ctx *WorkflowContext) WaitSignal(name string) (map[string]interface{}, error) {
	return ctx.runner.handleSignal(name)
}

// GetVersion records or replays a version marker for deterministic upgrades.
func (ctx *WorkflowContext) GetVersion(changeID string, minSupported, maxSupported int) (int, error) {
	return ctx.runner.handleVersion(changeID, minSupported, maxSupported)
}

// Command represents a pending decision from workflow execution.
type Command struct {
	CommandType string
	Attributes  map[string]interface{}
}

// WorkflowRunResult is the outcome of a workflow task.
type WorkflowRunResult struct {
	Status  string
	Result  interface{}
	Error   string
	Command *Command
}

// ActivityError is returned when an activity fails.
type ActivityError struct {
	Message string
	Details map[string]interface{}
}

func (e ActivityError) Error() string {
	return e.Message
}

type workflowYield struct {
	status  string
	command *Command
}

// HistoryView is a preprocessed summary of history for deterministic replay.
type HistoryView struct {
	ActivityScheduled []HistoryEvent
	ActivityResults   map[string]HistoryEvent
	TimerScheduled    []HistoryEvent
	TimerResults      map[string]HistoryEvent
	Signals           map[string][]map[string]interface{}
	VersionMarkers    map[string]int
}

func NewHistoryView(history []HistoryEvent) HistoryView {
	view := HistoryView{
		ActivityResults: make(map[string]HistoryEvent),
		TimerResults:    make(map[string]HistoryEvent),
		Signals:         make(map[string][]map[string]interface{}),
		VersionMarkers:  make(map[string]int),
	}
	for _, event := range history {
		switch event.EventType {
		case EventActivityTaskScheduled:
			view.ActivityScheduled = append(view.ActivityScheduled, event)
		case EventActivityTaskCompleted, EventActivityTaskFailed, EventActivityTaskTimedOut:
			if id, ok := event.Attributes["activity_id"].(string); ok {
				view.ActivityResults[id] = event
			}
		case EventTimerScheduled:
			view.TimerScheduled = append(view.TimerScheduled, event)
		case EventTimerFired:
			if id, ok := event.Attributes["timer_id"].(string); ok {
				view.TimerResults[id] = event
			}
		case EventSignalReceived:
			name, _ := event.Attributes["signal_name"].(string)
			payload, _ := event.Attributes["payload"].(map[string]interface{})
			if name != "" {
				view.Signals[name] = append(view.Signals[name], payload)
			}
		case EventVersionMarkerRecorded:
			changeID, _ := event.Attributes["change_id"].(string)
			versionFloat, _ := event.Attributes["version"].(float64)
			if changeID != "" {
				view.VersionMarkers[changeID] = int(versionFloat)
			}
		}
	}
	return view
}

// WorkflowRunner deterministically executes workflow code.
type WorkflowRunner struct {
	workflowFunc       WorkflowFunc
	inputPayload       map[string]interface{}
	historyView        HistoryView
	activityIndex      int
	timerIndex         int
	signalConsumed     map[string]int
	defaultRetryPolicy RetryPolicy
}

func NewWorkflowRunner(workflowFunc WorkflowFunc, inputPayload map[string]interface{}, history []HistoryEvent, retryPolicy RetryPolicy) *WorkflowRunner {
	return &WorkflowRunner{
		workflowFunc:       workflowFunc,
		inputPayload:       inputPayload,
		historyView:        NewHistoryView(history),
		signalConsumed:     make(map[string]int),
		defaultRetryPolicy: retryPolicy,
	}
}

func (r *WorkflowRunner) Run() (result WorkflowRunResult) {
	defer func() {
		if rec := recover(); rec != nil {
			if yield, ok := rec.(workflowYield); ok {
				result = WorkflowRunResult{Status: yield.status, Command: yield.command}
				return
			}
			result = WorkflowRunResult{Status: "FAILED", Error: fmt.Sprintf("%v", rec)}
		}
	}()

	ctx := &WorkflowContext{runner: r}
	output, err := r.workflowFunc(ctx, r.inputPayload)
	if err != nil {
		return WorkflowRunResult{Status: "FAILED", Error: err.Error()}
	}
	return WorkflowRunResult{Status: "COMPLETED", Result: output}
}

func (r *WorkflowRunner) handleActivity(name string, input map[string]interface{}, opts *ActivityOptions) (interface{}, error) {
	if opts == nil {
		opts = &ActivityOptions{
			ScheduleToCloseTimeoutSeconds: 300,
			StartToCloseTimeoutSeconds:    60,
			HeartbeatTimeoutSeconds:       30,
		}
	}
	if opts.ScheduleToCloseTimeoutSeconds == 0 {
		opts.ScheduleToCloseTimeoutSeconds = 300
	}
	if opts.StartToCloseTimeoutSeconds == 0 {
		opts.StartToCloseTimeoutSeconds = 60
	}
	if opts.HeartbeatTimeoutSeconds == 0 {
		opts.HeartbeatTimeoutSeconds = 30
	}
	retryPolicy := r.defaultRetryPolicy
	if opts.RetryPolicy != nil {
		retryPolicy = *opts.RetryPolicy
	}
	if r.activityIndex < len(r.historyView.ActivityScheduled) {
		// Replay path: the activity is already scheduled in history.
		scheduled := r.historyView.ActivityScheduled[r.activityIndex]
		r.activityIndex++
		expectedName, _ := scheduled.Attributes["activity_name"].(string)
		if expectedName != name {
			return nil, fmt.Errorf("non-determinism: activity name mismatch %s vs %s", expectedName, name)
		}
		activityID, _ := scheduled.Attributes["activity_id"].(string)
		completion, ok := r.historyView.ActivityResults[activityID]
		if !ok {
			// Activity exists but hasn't completed yet. Suspend the workflow task.
			panic(workflowYield{status: "WAITING"})
		}
		switch completion.EventType {
		case EventActivityTaskCompleted:
			return completion.Attributes["result"], nil
		case EventActivityTaskFailed, EventActivityTaskTimedOut:
			return nil, ActivityError{
				Message: fmt.Sprintf("activity failed: %v", completion.Attributes["error"]),
				Details: completion.Attributes,
			}
		default:
			return nil, fmt.Errorf("unexpected completion event %s", completion.EventType)
		}
	}

	// No scheduled activity in history at this point. Emit a new command.
	panic(workflowYield{
		status: "COMMAND",
		command: &Command{
			CommandType: "activity",
			Attributes: map[string]interface{}{
				"activity_name":                     name,
				"input":                             input,
				"retry_policy":                      retryPolicy,
				"schedule_to_close_timeout_seconds": opts.ScheduleToCloseTimeoutSeconds,
				"start_to_close_timeout_seconds":    opts.StartToCloseTimeoutSeconds,
				"heartbeat_timeout_seconds":         opts.HeartbeatTimeoutSeconds,
			},
		},
	})
}

func (r *WorkflowRunner) handleTimer(durationSeconds int) (interface{}, error) {
	if r.timerIndex < len(r.historyView.TimerScheduled) {
		// Replay path: timer already exists in history.
		scheduled := r.historyView.TimerScheduled[r.timerIndex]
		r.timerIndex++
		timerID, _ := scheduled.Attributes["timer_id"].(string)
		if timerID == "" {
			return nil, fmt.Errorf("non-determinism: timer without id")
		}
		if _, ok := r.historyView.TimerResults[timerID]; !ok {
			// Timer scheduled but not fired yet; suspend.
			panic(workflowYield{status: "WAITING"})
		}
		return map[string]interface{}{"timer_id": timerID}, nil
	}
	// No timer yet; emit a new timer command.
	panic(workflowYield{
		status: "COMMAND",
		command: &Command{
			CommandType: "timer",
			Attributes: map[string]interface{}{
				"duration_seconds": durationSeconds,
			},
		},
	})
}

func (r *WorkflowRunner) handleSignal(name string) (map[string]interface{}, error) {
	consumed := r.signalConsumed[name]
	signals := r.historyView.Signals[name]
	if consumed < len(signals) {
		payload := signals[consumed]
		r.signalConsumed[name] = consumed + 1
		return payload, nil
	}
	// Signals are buffered; if none available, suspend deterministically.
	panic(workflowYield{status: "WAITING"})
}

func (r *WorkflowRunner) handleVersion(changeID string, minSupported, maxSupported int) (int, error) {
	if version, ok := r.historyView.VersionMarkers[changeID]; ok {
		if version < minSupported || version > maxSupported {
			return 0, fmt.Errorf("version %d outside supported range for %s", version, changeID)
		}
		return version, nil
	}
	panic(workflowYield{
		status: "COMMAND",
		command: &Command{
			CommandType: "version_marker",
			Attributes: map[string]interface{}{
				"change_id": changeID,
				"version":   maxSupported,
			},
		},
	})
}
