// Package worker implements the task worker process for the distributed task scheduler.
//
// Workers are responsible for:
//   - Registering with the system
//   - Polling queues for tasks
//   - Executing task handlers
//   - Sending heartbeats
//   - Reporting results
package worker

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"runtime"
	"sync"
	"sync/atomic"
	"time"

	"github.com/google/uuid"
	"github.com/rs/zerolog/log"

	"github.com/distributed-task-scheduler/internal/config"
	"github.com/distributed-task-scheduler/internal/persistence"
	"github.com/distributed-task-scheduler/pkg/models"
)

// TaskHandler is a function that processes a task.
type TaskHandler func(ctx context.Context, task *models.Task) (json.RawMessage, error)

// Worker is a task processing worker.
type Worker struct {
	config   config.WorkerConfig
	db       *persistence.Database
	repo     *persistence.Repository

	workerID   uuid.UUID
	workerName string
	hostname   string

	handlers map[string]TaskHandler

	running      bool
	shuttingDown atomic.Bool
	activeTasks  sync.Map
	taskCount    int32

	mu     sync.RWMutex
	cancel context.CancelFunc
	wg     sync.WaitGroup

	// Semaphore for concurrency control
	semaphore chan struct{}

	// Statistics
	stats Stats
}

// Stats contains worker statistics.
type Stats struct {
	TasksProcessed int64 `json:"tasks_processed"`
	TasksSucceeded int64 `json:"tasks_succeeded"`
	TasksFailed    int64 `json:"tasks_failed"`
	TasksRetried   int64 `json:"tasks_retried"`
}

// NewWorker creates a new worker instance.
func NewWorker(cfg *config.Config, db *persistence.Database) *Worker {
	workerID := uuid.New()
	if cfg.Worker.WorkerID != "" {
		if parsed, err := uuid.Parse(cfg.Worker.WorkerID); err == nil {
			workerID = parsed
		}
	}

	hostname, _ := os.Hostname()
	workerName := fmt.Sprintf("%s:%d", hostname, os.Getpid())

	return &Worker{
		config:     cfg.Worker,
		db:         db,
		repo:       persistence.NewRepository(db),
		workerID:   workerID,
		workerName: workerName,
		hostname:   hostname,
		handlers:   make(map[string]TaskHandler),
		semaphore:  make(chan struct{}, cfg.Worker.Concurrency),
	}
}

// RegisterHandler registers a handler for a task type.
func (w *Worker) RegisterHandler(taskType string, handler TaskHandler) {
	w.mu.Lock()
	defer w.mu.Unlock()
	w.handlers[taskType] = handler
	log.Info().Str("task_type", taskType).Msg("Registered task handler")
}

// GetHandler returns the handler for a task type.
func (w *Worker) GetHandler(taskType string) (TaskHandler, bool) {
	w.mu.RLock()
	defer w.mu.RUnlock()
	handler, ok := w.handlers[taskType]
	return handler, ok
}

// Start starts the worker.
func (w *Worker) Start(ctx context.Context) error {
	w.mu.Lock()
	if w.running {
		w.mu.Unlock()
		return nil
	}
	w.running = true
	w.mu.Unlock()

	log.Info().
		Str("worker_id", w.workerID.String()).
		Str("worker_name", w.workerName).
		Strs("queues", w.config.Queues).
		Int("concurrency", w.config.Concurrency).
		Msg("Starting worker")

	ctx, w.cancel = context.WithCancel(ctx)

	// Register with system
	if err := w.register(ctx); err != nil {
		return fmt.Errorf("failed to register worker: %w", err)
	}

	// Start background tasks
	w.wg.Add(2)
	go w.pollLoop(ctx)
	go w.heartbeatLoop(ctx)

	log.Info().Msg("Worker started")

	return nil
}

// Stop stops the worker gracefully.
func (w *Worker) Stop(ctx context.Context) error {
	w.mu.Lock()
	if !w.running {
		w.mu.Unlock()
		return nil
	}
	w.running = false
	w.shuttingDown.Store(true)
	w.mu.Unlock()

	log.Info().Msg("Stopping worker")

	// Cancel polling loop
	if w.cancel != nil {
		w.cancel()
	}

	// Wait for active tasks with timeout
	activeCount := atomic.LoadInt32(&w.taskCount)
	if activeCount > 0 {
		log.Info().
			Int32("active_tasks", activeCount).
			Dur("timeout", w.config.ShutdownTimeout).
			Msg("Waiting for active tasks to complete")

		done := make(chan struct{})
		go func() {
			for atomic.LoadInt32(&w.taskCount) > 0 {
				time.Sleep(100 * time.Millisecond)
			}
			close(done)
		}()

		select {
		case <-done:
			log.Info().Msg("All tasks completed")
		case <-time.After(w.config.ShutdownTimeout):
			log.Warn().
				Int32("remaining", atomic.LoadInt32(&w.taskCount)).
				Msg("Shutdown timeout, some tasks may not have completed")
		}
	}

	// Wait for background tasks
	w.wg.Wait()

	// Deregister
	if _, err := w.repo.DeregisterWorker(context.Background(), w.workerID); err != nil {
		log.Warn().Err(err).Msg("Failed to deregister worker")
	}

	log.Info().Msg("Worker stopped")
	return nil
}

// GetStats returns worker statistics.
func (w *Worker) GetStats() Stats {
	w.mu.RLock()
	defer w.mu.RUnlock()
	return w.stats
}

// ActiveTaskCount returns the number of active tasks.
func (w *Worker) ActiveTaskCount() int {
	return int(atomic.LoadInt32(&w.taskCount))
}

// ============================================================================
// REGISTRATION
// ============================================================================

func (w *Worker) register(ctx context.Context) error {
	// Get list of registered handlers
	w.mu.RLock()
	handlerTypes := make([]string, 0, len(w.handlers))
	for taskType := range w.handlers {
		handlerTypes = append(handlerTypes, taskType)
	}
	w.mu.RUnlock()

	metadata, _ := json.Marshal(map[string]interface{}{
		"go_version": runtime.Version(),
		"handlers":   handlerTypes,
	})

	worker := &models.Worker{
		ID:          w.workerID,
		Name:        w.workerName,
		Hostname:    w.hostname,
		PID:         os.Getpid(),
		Queues:      w.config.Queues,
		Concurrency: w.config.Concurrency,
		Version:     "1.0.0",
		Metadata:    metadata,
	}

	_, err := w.repo.RegisterWorker(ctx, worker)
	return err
}

// ============================================================================
// TASK PROCESSING
// ============================================================================

func (w *Worker) pollLoop(ctx context.Context) {
	defer w.wg.Done()

	pollInterval := w.config.PollInterval
	maxPollInterval := w.config.MaxPollInterval
	batchSize := w.config.BatchSize
	visibilityTimeout := int(w.config.VisibilityTimeout.Seconds())

	currentInterval := pollInterval
	emptyPolls := 0

	for {
		select {
		case <-ctx.Done():
			return
		default:
		}

		if w.shuttingDown.Load() {
			return
		}

		// Check capacity
		availableCapacity := w.config.Concurrency - int(atomic.LoadInt32(&w.taskCount))
		if availableCapacity <= 0 {
			time.Sleep(pollInterval)
			continue
		}

		// Poll each queue
		claimedAny := false
		for _, queueName := range w.config.Queues {
			if w.shuttingDown.Load() {
				return
			}

			fetchSize := batchSize
			if fetchSize > availableCapacity {
				fetchSize = availableCapacity
			}

			tasks, err := w.repo.ClaimTasks(ctx, w.workerID, queueName, fetchSize, visibilityTimeout)
			if err != nil {
				log.Error().Err(err).Str("queue", queueName).Msg("Failed to claim tasks")
				continue
			}

			if len(tasks) > 0 {
				claimedAny = true
				emptyPolls = 0
				currentInterval = pollInterval

				for _, task := range tasks {
					// Acquire semaphore slot
					w.semaphore <- struct{}{}
					atomic.AddInt32(&w.taskCount, 1)

					go func(t *models.Task) {
						defer func() {
							<-w.semaphore
							atomic.AddInt32(&w.taskCount, -1)
						}()
						w.processTask(ctx, t)
					}(task)
				}

				availableCapacity -= len(tasks)
			}
		}

		if !claimedAny {
			// Empty poll - backoff
			emptyPolls++
			currentInterval = time.Duration(float64(currentInterval) * 1.5)
			if currentInterval > maxPollInterval {
				currentInterval = maxPollInterval
			}
		}

		time.Sleep(currentInterval)
	}
}

func (w *Worker) processTask(ctx context.Context, task *models.Task) {
	startedAt := time.Now()

	log.Info().
		Str("task_id", task.ID.String()).
		Str("task_type", task.TaskType).
		Int("attempt", task.AttemptCount).
		Msg("Processing task")

	// Store in active tasks
	w.activeTasks.Store(task.ID, task)
	defer w.activeTasks.Delete(task.ID)

	// Get handler
	handler, ok := w.GetHandler(task.TaskType)
	if !ok {
		errorMsg := fmt.Sprintf("No handler registered for task type: %s", task.TaskType)
		log.Error().Str("task_id", task.ID.String()).Msg(errorMsg)
		w.failTask(ctx, task, errorMsg, "HandlerNotFoundError")
		return
	}

	// Create task context with timeout
	taskCtx, cancel := context.WithTimeout(ctx, time.Duration(task.TimeoutSeconds)*time.Second)
	defer cancel()

	// Execute handler
	result, err := handler(taskCtx, task)

	duration := time.Since(startedAt)

	if err != nil {
		// Check if context was cancelled due to shutdown
		if w.shuttingDown.Load() && ctx.Err() != nil {
			log.Warn().
				Str("task_id", task.ID.String()).
				Msg("Task processing cancelled due to shutdown")
			return
		}

		// Check if timeout
		if taskCtx.Err() == context.DeadlineExceeded {
			errorMsg := fmt.Sprintf("Task execution timeout after %ds", task.TimeoutSeconds)
			log.Error().Str("task_id", task.ID.String()).Msg(errorMsg)
			w.failTask(ctx, task, errorMsg, "TimeoutError")
		} else {
			log.Error().
				Err(err).
				Str("task_id", task.ID.String()).
				Msg("Task execution failed")
			w.failTask(ctx, task, err.Error(), fmt.Sprintf("%T", err))
		}
		return
	}

	// Success
	w.completeTask(ctx, task, result, duration)
}

func (w *Worker) completeTask(ctx context.Context, task *models.Task, result json.RawMessage, duration time.Duration) {
	_, err := w.repo.CompleteTask(ctx, task.ID, result, &task.Version)
	if err != nil {
		log.Error().
			Err(err).
			Str("task_id", task.ID.String()).
			Msg("Failed to report task completion")
		return
	}

	w.mu.Lock()
	w.stats.TasksProcessed++
	w.stats.TasksSucceeded++
	w.mu.Unlock()

	log.Info().
		Str("task_id", task.ID.String()).
		Dur("duration", duration).
		Msg("Task completed")
}

func (w *Worker) failTask(ctx context.Context, task *models.Task, errorMessage, errorType string) {
	errorDetails, _ := json.Marshal(map[string]interface{}{
		"error_type": errorType,
		"attempt":    task.AttemptCount,
	})

	updatedTask, err := w.repo.FailTask(ctx, task.ID, errorMessage, errorDetails, &task.Version)
	if err != nil {
		log.Error().
			Err(err).
			Str("task_id", task.ID.String()).
			Msg("Failed to report task failure")
		return
	}

	w.mu.Lock()
	w.stats.TasksProcessed++
	w.stats.TasksFailed++
	if updatedTask != nil && updatedTask.Status == models.TaskStatusQueued {
		w.stats.TasksRetried++
	}
	w.mu.Unlock()
}

// ============================================================================
// HEARTBEAT
// ============================================================================

func (w *Worker) heartbeatLoop(ctx context.Context) {
	defer w.wg.Done()

	ticker := time.NewTicker(w.config.HeartbeatInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			// Send final heartbeat if tasks still running
			if atomic.LoadInt32(&w.taskCount) > 0 {
				w.sendHeartbeat(context.Background())
			}
			return
		case <-ticker.C:
			w.sendHeartbeat(ctx)
			w.extendVisibilityTimeouts(ctx)
		}
	}
}

func (w *Worker) sendHeartbeat(ctx context.Context) {
	activeCount := int(atomic.LoadInt32(&w.taskCount))

	_, err := w.repo.Heartbeat(ctx, w.workerID, activeCount, nil, nil)
	if err != nil {
		log.Error().Err(err).Msg("Failed to send heartbeat")
	}
}

func (w *Worker) extendVisibilityTimeouts(ctx context.Context) {
	visibilityTimeout := int(w.config.VisibilityTimeout.Seconds())

	w.activeTasks.Range(func(key, value interface{}) bool {
		taskID := key.(uuid.UUID)
		_, err := w.repo.ExtendVisibilityTimeout(ctx, taskID, w.workerID, visibilityTimeout)
		if err != nil {
			log.Warn().
				Err(err).
				Str("task_id", taskID.String()).
				Msg("Failed to extend visibility timeout")
		}
		return true
	})
}

// ============================================================================
// HEALTH
// ============================================================================

// Health returns the worker health status.
type Health struct {
	Status      string   `json:"status"`
	WorkerID    string   `json:"worker_id"`
	WorkerName  string   `json:"worker_name"`
	Queues      []string `json:"queues"`
	Concurrency int      `json:"concurrency"`
	ActiveTasks int      `json:"active_tasks"`
	IsRunning   bool     `json:"is_running"`
}

// GetHealth returns the worker health status.
func (w *Worker) GetHealth() Health {
	w.mu.RLock()
	running := w.running
	w.mu.RUnlock()

	return Health{
		Status:      "healthy",
		WorkerID:    w.workerID.String(),
		WorkerName:  w.workerName,
		Queues:      w.config.Queues,
		Concurrency: w.config.Concurrency,
		ActiveTasks: int(atomic.LoadInt32(&w.taskCount)),
		IsRunning:   running,
	}
}
