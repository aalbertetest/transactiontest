package engine

import (
	"time"
)

// WorkflowEngine is the entry point for starting and signaling workflows.
type WorkflowEngine struct {
	store   *SQLiteStore
	queue   TaskQueue
	config  Config
	metrics *MetricsRegistry
	logger  *Logger
}

func NewWorkflowEngine(store *SQLiteStore, queue TaskQueue, config Config, metrics *MetricsRegistry) *WorkflowEngine {
	return &WorkflowEngine{
		store:   store,
		queue:   queue,
		config:  config,
		metrics: metrics,
		logger:  NewLogger(config.LogLevel),
	}
}

func (e *WorkflowEngine) StartWorkflow(workflowID, workflowType string, input map[string]interface{}, taskQueue string) (string, error) {
	if taskQueue == "" {
		taskQueue = e.config.TaskQueueName
	}
	runID, err := e.store.CreateWorkflowExecution(workflowID, workflowType, input, taskQueue)
	if err != nil {
		return "", err
	}
	_, _ = e.store.AppendEvent(workflowID, runID, EventWorkflowExecutionStarted, map[string]interface{}{
		"workflow_type": workflowType,
		"input":         input,
		"task_queue":    taskQueue,
	})
	_ = e.scheduleWorkflowTask(workflowID, runID, workflowType, taskQueue)
	if e.metrics != nil {
		e.metrics.Inc("engine.start_workflow", 1)
	}
	e.logger.Infof("workflow started workflow_id=%s run_id=%s", workflowID, runID)
	return runID, nil
}

func (e *WorkflowEngine) SignalWorkflow(workflowID, runID, signalName string, payload map[string]interface{}) error {
	_, err := e.store.AppendEvent(workflowID, runID, EventSignalReceived, map[string]interface{}{
		"signal_name": signalName,
		"payload":     payload,
		"received_at": time.Now().Unix(),
	})
	if err != nil {
		return err
	}
	exec, err := e.store.GetWorkflowExecution(workflowID, runID)
	if err != nil {
		return err
	}
	taskQueue := e.config.TaskQueueName
	workflowType := ""
	if exec != nil {
		taskQueue = exec.TaskQueue
		workflowType = exec.WorkflowType
		if exec.State == WorkflowStateWaiting {
			_ = e.store.SetWorkflowState(workflowID, runID, WorkflowStateRunning, nil, nil)
		}
	}
	if err := e.scheduleWorkflowTask(workflowID, runID, workflowType, taskQueue); err != nil {
		return err
	}
	if e.metrics != nil {
		e.metrics.Inc("engine.signal_workflow", 1)
	}
	e.logger.Infof("workflow signaled workflow_id=%s run_id=%s signal=%s", workflowID, runID, signalName)
	return nil
}

func (e *WorkflowEngine) scheduleWorkflowTask(workflowID, runID, workflowType, taskQueue string) error {
	payload := map[string]interface{}{
		"workflow_id":   workflowID,
		"run_id":        runID,
		"workflow_type": workflowType,
		"task_queue":    taskQueue,
	}
	_, err := e.queue.Enqueue(taskQueue, "workflow", payload, nil, 1)
	if err != nil {
		return err
	}
	_, _ = e.store.AppendEvent(workflowID, runID, EventWorkflowTaskScheduled, map[string]interface{}{
		"task_queue": taskQueue,
	})
	return nil
}
