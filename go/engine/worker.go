package engine

import (
	"encoding/json"
	"time"
)

// ActivityFunc defines the signature for activity code.
type ActivityFunc func(ctx *ActivityContext, input map[string]interface{}) (interface{}, error)

// ActivityContext allows activities to heartbeat.
type ActivityContext struct {
	store      *SQLiteStore
	activityID string
}

func (c *ActivityContext) Heartbeat(details map[string]interface{}) error {
	return c.store.RecordActivityHeartbeat(c.activityID, details)
}

// Worker polls workflow and activity task queues.
type Worker struct {
	store      *SQLiteStore
	queue      TaskQueue
	config     Config
	metrics    *MetricsRegistry
	logger     *Logger
	workflows  map[string]WorkflowFunc
	activities map[string]ActivityFunc
	stopCh     chan struct{}
}

func NewWorker(store *SQLiteStore, queue TaskQueue, config Config, metrics *MetricsRegistry) *Worker {
	return &Worker{
		store:      store,
		queue:      queue,
		config:     config,
		metrics:    metrics,
		logger:     NewLogger(config.LogLevel),
		workflows:  make(map[string]WorkflowFunc),
		activities: make(map[string]ActivityFunc),
		stopCh:     make(chan struct{}),
	}
}

func (w *Worker) RegisterWorkflow(name string, workflow WorkflowFunc) {
	w.workflows[name] = workflow
}

func (w *Worker) RegisterActivity(name string, activity ActivityFunc) {
	w.activities[name] = activity
}

func (w *Worker) Start() {
	go w.Run()
}

func (w *Worker) Stop() {
	close(w.stopCh)
}

func (w *Worker) Run() {
	for {
		select {
		case <-w.stopCh:
			return
		default:
			w.RunOnce()
			time.Sleep(time.Duration(w.config.PollIntervalSeconds * float64(time.Second)))
		}
	}
}

func (w *Worker) RunOnce() {
	workflowTask, _ := w.queue.Poll(w.config.TaskQueueName, "workflow", w.config.LeaseDurationSeconds, w.config.WorkerID)
	if workflowTask != nil {
		w.handleWorkflowTask(workflowTask)
	}
	activityTask, _ := w.queue.Poll(w.config.TaskQueueName, "activity", w.config.LeaseDurationSeconds, w.config.WorkerID)
	if activityTask != nil {
		w.handleActivityTask(activityTask)
	}
}

func (w *Worker) handleWorkflowTask(task *QueueTask) {
	payload := task.Payload
	workflowID := payload["workflow_id"].(string)
	runID := payload["run_id"].(string)
	workflowType := payload["workflow_type"].(string)

	exec, err := w.store.GetWorkflowExecution(workflowID, runID)
	if err != nil || exec == nil {
		_ = w.queue.Ack(task.ID)
		return
	}
	if exec.State == WorkflowStateCompleted || exec.State == WorkflowStateFailed {
		_ = w.queue.Ack(task.ID)
		return
	}

	workflowFunc := w.workflows[workflowType]
	if workflowFunc == nil {
		errMsg := "workflow type not registered"
		_ = w.store.SetWorkflowState(workflowID, runID, WorkflowStateFailed, nil, &errMsg)
		_ = w.queue.Ack(task.ID)
		return
	}

	// Record ownership of the workflow task for observability and audit.
	_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowTaskStarted, map[string]interface{}{
		"worker_id": w.config.WorkerID,
	})

	history, err := w.store.GetHistory(workflowID, runID)
	if err != nil {
		_ = w.queue.Ack(task.ID)
		return
	}
	input := parseJSONMap(exec.Input)
	defaultRetry := RetryPolicy{
		InitialIntervalSeconds: w.config.RetryInitialIntervalSeconds,
		MaxIntervalSeconds:     w.config.RetryMaxIntervalSeconds,
		BackoffCoefficient:     w.config.RetryBackoffCoefficient,
		MaxAttempts:            w.config.RetryMaxAttempts,
	}
	runner := NewWorkflowRunner(workflowFunc, input, history, defaultRetry)
	result := runner.Run()

	switch result.Status {
	case "COMMAND":
		if result.Command != nil {
			switch result.Command.CommandType {
			case "activity":
				// Persist the activity task and enqueue it for workers.
				attrs := result.Command.Attributes
				retryPolicy := decodeRetryPolicy(attrs["retry_policy"], defaultRetry)
				inputMap, _ := ensureMap(attrs["input"])
				scheduleToClose := mustInt(attrs["schedule_to_close_timeout_seconds"], w.config.ActivityScheduleToCloseTimeoutSec)
				startToClose := mustInt(attrs["start_to_close_timeout_seconds"], w.config.ActivityStartToCloseTimeoutSec)
				heartbeatTimeout := mustInt(attrs["heartbeat_timeout_seconds"], w.config.ActivityHeartbeatTimeoutSeconds)
				activityID, err := w.store.CreateActivityTask(
					workflowID, runID,
					attrs["activity_name"].(string),
					inputMap,
					retryPolicy,
					scheduleToClose,
					startToClose,
					heartbeatTimeout,
				)
				if err == nil {
					_, _ = w.store.AppendEvent(workflowID, runID, EventActivityTaskScheduled, map[string]interface{}{
						"activity_id":   activityID,
						"activity_name": attrs["activity_name"],
						"input":         attrs["input"],
					})
					payload := map[string]interface{}{
						"activity_id": activityID,
						"workflow_id": workflowID,
						"run_id":      runID,
					}
					_, _ = w.queue.Enqueue(w.config.TaskQueueName, "activity", payload, nil, 1)
				}
				_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowTaskCompleted, map[string]interface{}{
					"status": "COMMAND",
				})
			case "timer":
				// Timers are driven by the scheduler; only record and schedule.
				fireAt := time.Now().Unix() + int64(mustInt(result.Command.Attributes["duration_seconds"], 0))
				timerID, err := w.store.CreateTimer(workflowID, runID, fireAt)
				if err == nil {
					_, _ = w.store.AppendEvent(workflowID, runID, EventTimerScheduled, map[string]interface{}{
						"timer_id": timerID,
						"fire_at":  fireAt,
					})
				}
				_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowTaskCompleted, map[string]interface{}{
					"status": "COMMAND",
				})
			case "version_marker":
				_, _ = w.store.AppendEvent(workflowID, runID, EventVersionMarkerRecorded, result.Command.Attributes)
				_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowTaskCompleted, map[string]interface{}{
					"status": "COMMAND",
				})
				payload := map[string]interface{}{
					"workflow_id":   workflowID,
					"run_id":        runID,
					"workflow_type": workflowType,
					"task_queue":    w.config.TaskQueueName,
				}
				_, _ = w.queue.Enqueue(w.config.TaskQueueName, "workflow", payload, nil, 1)
			}
		}
	case "WAITING":
		_ = w.store.SetWorkflowState(workflowID, runID, WorkflowStateWaiting, nil, nil)
		_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowTaskCompleted, map[string]interface{}{
			"status": "WAITING",
		})
	case "COMPLETED":
		_ = w.store.SetWorkflowState(workflowID, runID, WorkflowStateCompleted, map[string]interface{}{"result": result.Result}, nil)
		_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowExecutionCompleted, map[string]interface{}{
			"result": result.Result,
		})
		_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowTaskCompleted, map[string]interface{}{
			"status": "COMPLETED",
		})
	default:
		errMsg := result.Error
		_ = w.store.SetWorkflowState(workflowID, runID, WorkflowStateFailed, nil, &errMsg)
		_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowExecutionFailed, map[string]interface{}{
			"error": result.Error,
		})
		_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowTaskCompleted, map[string]interface{}{
			"status": "FAILED",
		})
	}
	_ = w.queue.Ack(task.ID)
	if w.metrics != nil {
		w.metrics.Inc("worker.workflow_task", 1)
	}
}

func (w *Worker) handleActivityTask(task *QueueTask) {
	payload := task.Payload
	activityID := payload["activity_id"].(string)
	activity, err := w.store.GetActivityTask(activityID)
	if err != nil || activity == nil {
		_ = w.queue.Ack(task.ID)
		return
	}
	if activity.State == ActivityStateCompleted || activity.State == ActivityStateFailed || activity.State == ActivityStateTimedOut {
		_ = w.queue.Ack(task.ID)
		return
	}

	activityFunc := w.activities[activity.ActivityName]
	if activityFunc == nil {
		_ = w.store.RecordActivityFailed(activityID, "activity not registered")
		_ = w.queue.Ack(task.ID)
		return
	}

	_ = w.store.RecordActivityStarted(activityID, w.config.WorkerID)
	_, _ = w.store.AppendEvent(activity.WorkflowID, activity.RunID, EventActivityTaskStarted, map[string]interface{}{
		"activity_id": activityID,
		"worker_id":   w.config.WorkerID,
	})

	ctx := &ActivityContext{store: w.store, activityID: activityID}
	result, err := activityFunc(ctx, activity.Input)
	if err == nil {
		_ = w.store.RecordActivityCompleted(activityID)
		_, _ = w.store.AppendEvent(activity.WorkflowID, activity.RunID, EventActivityTaskCompleted, map[string]interface{}{
			"activity_id": activityID,
			"result":      result,
		})
		w.scheduleWorkflowAfterActivity(activity.WorkflowID, activity.RunID)
		_ = w.queue.Ack(task.ID)
		return
	}

	errMessage := err.Error()
	if activity.Attempt+1 < activity.MaxAttempts {
		_ = w.store.RecordActivityRetrying(activityID, errMessage)
		_, _ = w.store.AppendEvent(activity.WorkflowID, activity.RunID, EventActivityTaskFailed, map[string]interface{}{
			"activity_id": activityID,
			"error":       errMessage,
		})
		_, _ = w.store.AppendEvent(activity.WorkflowID, activity.RunID, EventActivityTaskRetryScheduled, map[string]interface{}{
			"activity_id": activityID,
			"error":       errMessage,
		})
		backoff := ComputeBackoffSeconds(activity.RetryPolicy, activity.Attempt+1)
		visibleAt := time.Now().Unix() + int64(backoff)
		payload := map[string]interface{}{
			"activity_id": activityID,
			"workflow_id": activity.WorkflowID,
			"run_id":      activity.RunID,
		}
		_, _ = w.queue.Enqueue(w.config.TaskQueueName, "activity", payload, &visibleAt, 1)
		w.logger.Warnf("activity failed retry scheduled activity_id=%s backoff=%d", activityID, backoff)
	} else {
		_ = w.store.RecordActivityFailed(activityID, errMessage)
		_, _ = w.store.AppendEvent(activity.WorkflowID, activity.RunID, EventActivityTaskFailed, map[string]interface{}{
			"activity_id": activityID,
			"error":       errMessage,
		})
		w.scheduleWorkflowAfterActivity(activity.WorkflowID, activity.RunID)
	}
	_ = w.queue.Ack(task.ID)
	if w.metrics != nil {
		w.metrics.Inc("worker.activity_task", 1)
	}
}

func (w *Worker) scheduleWorkflowAfterActivity(workflowID, runID string) {
	exec, err := w.store.GetWorkflowExecution(workflowID, runID)
	if err != nil || exec == nil {
		return
	}
	payload := map[string]interface{}{
		"workflow_id":   workflowID,
		"run_id":        runID,
		"workflow_type": exec.WorkflowType,
		"task_queue":    exec.TaskQueue,
	}
	_, _ = w.queue.Enqueue(exec.TaskQueue, "workflow", payload, nil, 1)
	_, _ = w.store.AppendEvent(workflowID, runID, EventWorkflowTaskScheduled, map[string]interface{}{
		"task_queue": exec.TaskQueue,
	})
	if exec.State == WorkflowStateWaiting {
		_ = w.store.SetWorkflowState(workflowID, runID, WorkflowStateRunning, nil, nil)
	}
}

func parseJSONMap(raw string) map[string]interface{} {
	if raw == "" {
		return map[string]interface{}{}
	}
	var data map[string]interface{}
	if err := json.Unmarshal([]byte(raw), &data); err != nil {
		return map[string]interface{}{}
	}
	return data
}

func decodeRetryPolicy(value interface{}, fallback RetryPolicy) RetryPolicy {
	switch typed := value.(type) {
	case RetryPolicy:
		return typed
	case map[string]interface{}:
		raw, _ := json.Marshal(typed)
		var policy RetryPolicy
		if err := json.Unmarshal(raw, &policy); err == nil {
			return policy
		}
	default:
		raw, _ := json.Marshal(typed)
		var policy RetryPolicy
		if err := json.Unmarshal(raw, &policy); err == nil {
			return policy
		}
	}
	return fallback
}

func mustInt(value interface{}, fallback int) int {
	switch typed := value.(type) {
	case int:
		return typed
	case int64:
		return int(typed)
	case float64:
		return int(typed)
	default:
		return fallback
	}
}

func ensureMap(value interface{}) (map[string]interface{}, error) {
	if val, ok := value.(map[string]interface{}); ok {
		return val, nil
	}
	raw, err := json.Marshal(value)
	if err != nil {
		return nil, err
	}
	var output map[string]interface{}
	if err := json.Unmarshal(raw, &output); err != nil {
		return nil, err
	}
	return output, nil
}
