package engine

import (
	"context"
	"time"
)

type WorkflowWorker struct {
	engine *WorkflowEngine
	stop   chan struct{}
}

func NewWorkflowWorker(engine *WorkflowEngine) *WorkflowWorker {
	return &WorkflowWorker{engine: engine, stop: make(chan struct{})}
}

func (w *WorkflowWorker) Start() {
	go w.run()
}

func (w *WorkflowWorker) Stop() {
	close(w.stop)
}

func (w *WorkflowWorker) run() {
	for {
		select {
		case <-w.stop:
			return
		default:
		}
		tasks, err := w.engine.Queue.LeaseTasks(w.engine.Config.WorkflowTaskQueue, 1, w.engine.Config.TaskLeaseSeconds)
		if err != nil || len(tasks) == 0 {
			time.Sleep(w.engine.Config.WorkerPollInterval)
			continue
		}
		for _, task := range tasks {
			_ = w.engine.ProcessWorkflowTask(task)
		}
	}
}

type ActivityWorker struct {
	engine      *WorkflowEngine
	concurrency int
	stop        chan struct{}
	semaphore   chan struct{}
}

func NewActivityWorker(engine *WorkflowEngine, concurrency int) *ActivityWorker {
	return &ActivityWorker{
		engine:      engine,
		concurrency: concurrency,
		stop:        make(chan struct{}),
		semaphore:   make(chan struct{}, concurrency),
	}
}

func (w *ActivityWorker) Start() {
	go w.run()
}

func (w *ActivityWorker) Stop() {
	close(w.stop)
}

func (w *ActivityWorker) run() {
	for {
		select {
		case <-w.stop:
			return
		default:
		}
		tasks, err := w.engine.Queue.LeaseTasks(w.engine.Config.ActivityTaskQueue, w.concurrency, w.engine.Config.TaskLeaseSeconds)
		if err != nil || len(tasks) == 0 {
			time.Sleep(w.engine.Config.WorkerPollInterval)
			continue
		}
		for _, task := range tasks {
			w.semaphore <- struct{}{}
			go func(t Task) {
				defer func() { <-w.semaphore }()
				w.handleTask(t)
			}(task)
		}
	}
}

func (w *ActivityWorker) handleTask(task Task) {
	activityName, _ := task.Payload["activity_name"].(string)
	definition, ok := w.engine.activities[activityName]
	if !ok {
		_ = w.engine.Queue.FailTask(task.TaskID, "unknown_activity")
		return
	}
	activityID, _ := task.Payload["activity_id"].(string)
	w.engine.RecordActivityStarted(task.RunID, activityID, task.TaskID, task.Attempt)
	actCtx := &ActivityContext{engine: w.engine, taskID: task.TaskID}
	input, _ := task.Payload["input"].(map[string]interface{})

	ctx, cancel := context.WithTimeout(context.Background(), time.Duration(definition.TimeoutSeconds)*time.Second)
	defer cancel()
	resultCh := make(chan map[string]interface{}, 1)
	errCh := make(chan error, 1)

	go func() {
		result, err := definition.Func(actCtx, input)
		if err != nil {
			errCh <- err
			return
		}
		resultCh <- result
	}()

	select {
	case <-ctx.Done():
		_ = w.engine.Queue.FailTask(task.TaskID, "timeout")
		w.engine.RecordActivityFailed(task.RunID, activityID, task.TaskID, task.Attempt, "timeout", definition.RetryPolicy)
	case err := <-errCh:
		_ = w.engine.Queue.FailTask(task.TaskID, err.Error())
		w.engine.RecordActivityFailed(task.RunID, activityID, task.TaskID, task.Attempt, err.Error(), definition.RetryPolicy)
	case result := <-resultCh:
		_ = w.engine.Queue.CompleteTask(task.TaskID)
		w.engine.RecordActivityCompleted(task.RunID, activityID, task.TaskID, task.Attempt, result)
	}
}

type TimerWorker struct {
	engine *WorkflowEngine
	stop   chan struct{}
}

func NewTimerWorker(engine *WorkflowEngine) *TimerWorker {
	return &TimerWorker{engine: engine, stop: make(chan struct{})}
}

func (w *TimerWorker) Start() {
	go w.run()
}

func (w *TimerWorker) Stop() {
	close(w.stop)
}

func (w *TimerWorker) run() {
	for {
		select {
		case <-w.stop:
			return
		default:
		}
		tasks, err := w.engine.Queue.LeaseTasks(w.engine.Config.TimerTaskQueue, 1, w.engine.Config.TaskLeaseSeconds)
		if err != nil || len(tasks) == 0 {
			time.Sleep(w.engine.Config.WorkerPollInterval)
			continue
		}
		for _, task := range tasks {
			timerID, _ := task.Payload["timer_id"].(string)
			w.engine.RecordTimerFired(task.RunID, timerID)
			_ = w.engine.Queue.CompleteTask(task.TaskID)
		}
	}
}
