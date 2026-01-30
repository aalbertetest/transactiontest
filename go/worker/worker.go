package worker

import (
	"time"

	"github.com/google/uuid"

	"workflow/config"
	"workflow/engine"
	"workflow/logging"
)

// Worker polls queues and executes tasks.
type Worker struct {
	engine   *engine.WorkflowEngine
	config   config.EngineConfig
	workerID string
	logger   *logging.Logger
}

// New creates a new worker.
func New(engine *engine.WorkflowEngine, cfg config.EngineConfig) *Worker {
	return &Worker{
		engine:   engine,
		config:   cfg,
		workerID: "worker-" + uuid.New().String(),
		logger:   logging.New(cfg.LogLevel),
	}
}

// Run runs the polling loop until stop is closed.
func (w *Worker) Run(stop <-chan struct{}) {
	w.logger.Info("Worker %s started", w.workerID)
	for {
		select {
		case <-stop:
			w.logger.Info("Worker %s stopped", w.workerID)
			return
		default:
		}

		if task, err := w.engine.WorkflowQueue().Poll(w.workerID, w.config.LeaseSeconds); err == nil && task != nil {
			w.logger.Info("Worker %s executing workflow task %s", w.workerID, task.TaskID)
			w.engine.ExecuteWorkflowTask(task, w.workerID)
			continue
		}
		if task, err := w.engine.ActivityQueue().Poll(w.workerID, w.config.LeaseSeconds); err == nil && task != nil {
			w.logger.Info("Worker %s executing activity task %s", w.workerID, task.TaskID)
			w.engine.ExecuteActivityTask(task, w.workerID)
			continue
		}

		time.Sleep(time.Duration(w.config.WorkerPollIntervalSeconds * float64(time.Second)))
	}
}
