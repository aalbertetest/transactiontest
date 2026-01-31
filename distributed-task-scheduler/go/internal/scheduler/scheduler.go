// Package scheduler implements the main scheduler service for the distributed task scheduler.
//
// The scheduler is responsible for:
//   - Leader election among multiple scheduler instances
//   - Cron job evaluation and task creation
//   - Pending task promotion
//   - Visibility timeout recovery
//   - Worker health monitoring
package scheduler

import (
	"context"
	"encoding/json"
	"fmt"
	"os"
	"sync"
	"time"

	"github.com/google/uuid"
	"github.com/robfig/cron/v3"
	"github.com/rs/zerolog/log"

	"github.com/distributed-task-scheduler/internal/config"
	"github.com/distributed-task-scheduler/internal/persistence"
	"github.com/distributed-task-scheduler/pkg/models"
)

const (
	// CronLeaderLock is the lock name for leader election.
	CronLeaderLock = "cron_leader"
)

// Scheduler is the main scheduler service.
type Scheduler struct {
	config       config.SchedulerConfig
	workerConfig config.WorkerConfig
	db           *persistence.Database
	repo         *persistence.Repository

	instanceID   uuid.UUID
	instanceName string

	isLeader bool
	running  bool

	mu     sync.RWMutex
	cancel context.CancelFunc
	wg     sync.WaitGroup

	// Statistics
	stats Stats
}

// Stats contains scheduler statistics.
type Stats struct {
	TasksCreated        int64     `json:"tasks_created"`
	CronRuns            int64     `json:"cron_runs"`
	TasksPromoted       int64     `json:"tasks_promoted"`
	TasksRecovered      int64     `json:"tasks_recovered"`
	LeaderAcquisitions  int64     `json:"leader_acquisitions"`
	LastLeaderCheck     time.Time `json:"last_leader_check"`
	LastCronEval        time.Time `json:"last_cron_eval"`
}

// NewScheduler creates a new scheduler instance.
func NewScheduler(cfg *config.Config, db *persistence.Database) *Scheduler {
	instanceID := uuid.New()
	if cfg.Scheduler.InstanceID != "" {
		if parsed, err := uuid.Parse(cfg.Scheduler.InstanceID); err == nil {
			instanceID = parsed
		}
	}

	hostname, _ := os.Hostname()
	instanceName := fmt.Sprintf("%s:%d", hostname, os.Getpid())

	return &Scheduler{
		config:       cfg.Scheduler,
		workerConfig: cfg.Worker,
		db:           db,
		repo:         persistence.NewRepository(db),
		instanceID:   instanceID,
		instanceName: instanceName,
	}
}

// Start starts the scheduler service.
func (s *Scheduler) Start(ctx context.Context) error {
	s.mu.Lock()
	if s.running {
		s.mu.Unlock()
		return nil
	}
	s.running = true
	s.mu.Unlock()

	log.Info().
		Str("instance_id", s.instanceID.String()).
		Str("instance_name", s.instanceName).
		Msg("Starting scheduler")

	ctx, s.cancel = context.WithCancel(ctx)

	// Start background loops
	s.wg.Add(5)
	go s.leaderElectionLoop(ctx)
	go s.cronEvaluationLoop(ctx)
	go s.pendingPromotionLoop(ctx)
	go s.timeoutRecoveryLoop(ctx)
	go s.healthCheckLoop(ctx)

	log.Info().Msg("Scheduler started")

	return nil
}

// Stop stops the scheduler gracefully.
func (s *Scheduler) Stop(ctx context.Context) error {
	s.mu.Lock()
	if !s.running {
		s.mu.Unlock()
		return nil
	}
	s.running = false
	s.mu.Unlock()

	log.Info().Msg("Stopping scheduler")

	// Cancel all background tasks
	if s.cancel != nil {
		s.cancel()
	}

	// Wait for tasks to complete
	done := make(chan struct{})
	go func() {
		s.wg.Wait()
		close(done)
	}()

	select {
	case <-done:
		log.Info().Msg("All scheduler tasks completed")
	case <-ctx.Done():
		log.Warn().Msg("Shutdown timeout, some tasks may not have completed")
	}

	// Release leader lock if held
	if s.IsLeader() {
		if _, err := s.repo.ReleaseLock(context.Background(), CronLeaderLock, s.instanceID); err != nil {
			log.Warn().Err(err).Msg("Failed to release leader lock")
		} else {
			log.Info().Msg("Released leader lock")
		}
	}

	log.Info().Msg("Scheduler stopped")
	return nil
}

// IsLeader returns whether this instance is the leader.
func (s *Scheduler) IsLeader() bool {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.isLeader
}

// GetStats returns scheduler statistics.
func (s *Scheduler) GetStats() Stats {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.stats
}

// ============================================================================
// TASK OPERATIONS
// ============================================================================

// SubmitTask submits a new task.
func (s *Scheduler) SubmitTask(ctx context.Context, opts TaskOptions) (*models.Task, error) {
	task := models.NewTask(opts.TaskType, opts.Payload)
	task.QueueName = opts.QueueName
	task.Priority = opts.Priority

	if opts.ScheduledAt != nil {
		task.ScheduledAt = opts.ScheduledAt
	}
	if opts.IdempotencyKey != "" {
		// Check for existing task
		existing, err := s.repo.GetTaskByIdempotencyKey(ctx, opts.IdempotencyKey)
		if err != nil {
			return nil, err
		}
		if existing != nil {
			return existing, nil
		}
		task.IdempotencyKey = opts.IdempotencyKey
	}
	if opts.MaxAttempts > 0 {
		task.MaxAttempts = opts.MaxAttempts
	}
	if opts.TimeoutSeconds > 0 {
		task.TimeoutSeconds = opts.TimeoutSeconds
	}

	created, err := s.repo.CreateTask(ctx, task)
	if err != nil {
		return nil, err
	}

	s.mu.Lock()
	s.stats.TasksCreated++
	s.mu.Unlock()

	return created, nil
}

// TaskOptions configures task creation.
type TaskOptions struct {
	TaskType       string
	Payload        json.RawMessage
	QueueName      string
	Priority       int
	ScheduledAt    *time.Time
	IdempotencyKey string
	MaxAttempts    int
	TimeoutSeconds int
}

// GetTask retrieves a task by ID.
func (s *Scheduler) GetTask(ctx context.Context, taskID uuid.UUID) (*models.Task, error) {
	return s.repo.GetTask(ctx, taskID)
}

// CancelTask cancels a pending or queued task.
func (s *Scheduler) CancelTask(ctx context.Context, taskID uuid.UUID) (*models.Task, error) {
	return s.repo.CancelTask(ctx, taskID)
}

// ============================================================================
// CRON JOB OPERATIONS
// ============================================================================

// CreateCronJob creates a new cron job.
func (s *Scheduler) CreateCronJob(ctx context.Context, opts CronJobOptions) (*models.CronJob, error) {
	// Validate cron expression
	parser := cron.NewParser(cron.Minute | cron.Hour | cron.Dom | cron.Month | cron.Dow)
	schedule, err := parser.Parse(opts.Schedule)
	if err != nil {
		return nil, fmt.Errorf("invalid cron expression: %w", err)
	}

	job := models.NewCronJob(opts.Name, opts.Schedule, opts.TaskType)
	job.Description = opts.Description
	job.TaskPayload = opts.TaskPayload
	job.QueueName = opts.QueueName
	job.Priority = opts.Priority

	if opts.Timezone != "" {
		job.Timezone = opts.Timezone
	}
	if opts.MaxAttempts > 0 {
		job.MaxAttempts = opts.MaxAttempts
	}
	if opts.TimeoutSeconds > 0 {
		job.TimeoutSeconds = opts.TimeoutSeconds
	}
	if opts.ConcurrencyPolicy != "" {
		job.ConcurrencyPolicy = opts.ConcurrencyPolicy
	}
	if opts.Metadata != nil {
		job.Metadata = opts.Metadata
	}

	// Calculate first run time
	nextRun := schedule.Next(time.Now().UTC())
	job.NextRunAt = &nextRun

	return s.repo.CreateCronJob(ctx, job)
}

// CronJobOptions configures cron job creation.
type CronJobOptions struct {
	Name              string
	Description       string
	Schedule          string
	Timezone          string
	TaskType          string
	TaskPayload       json.RawMessage
	QueueName         string
	Priority          int
	MaxAttempts       int
	TimeoutSeconds    int
	ConcurrencyPolicy models.ConcurrencyPolicy
	Metadata          json.RawMessage
}

// GetCronJob retrieves a cron job by ID.
func (s *Scheduler) GetCronJob(ctx context.Context, jobID uuid.UUID) (*models.CronJob, error) {
	return s.repo.GetCronJob(ctx, jobID)
}

// ============================================================================
// BACKGROUND LOOPS
// ============================================================================

func (s *Scheduler) leaderElectionLoop(ctx context.Context) {
	defer s.wg.Done()

	ttl := s.config.LeaderElectionTTL
	interval := time.Duration(s.config.LeaderRenewalInterval) * time.Second

	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			s.tryAcquireLeadership(ctx, ttl)
		}
	}
}

func (s *Scheduler) tryAcquireLeadership(ctx context.Context, ttl int) {
	acquired, err := s.repo.TryAcquireLock(ctx, CronLeaderLock, s.instanceID, s.instanceName, ttl)
	if err != nil {
		log.Error().Err(err).Msg("Leader election error")
		s.mu.Lock()
		s.isLeader = false
		s.mu.Unlock()
		return
	}

	s.mu.Lock()
	wasLeader := s.isLeader
	s.isLeader = acquired
	s.stats.LastLeaderCheck = time.Now()

	if acquired && !wasLeader {
		s.stats.LeaderAcquisitions++
		log.Info().Msg("Acquired leader lock - now the active scheduler")
	} else if !acquired && wasLeader {
		log.Warn().Msg("Lost leader lock - now standby")
	}
	s.mu.Unlock()
}

func (s *Scheduler) cronEvaluationLoop(ctx context.Context) {
	defer s.wg.Done()

	ticker := time.NewTicker(s.config.CronTickInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			if s.IsLeader() {
				if err := s.evaluateCronJobs(ctx); err != nil {
					log.Error().Err(err).Msg("Cron evaluation error")
				}
			}
		}
	}
}

func (s *Scheduler) evaluateCronJobs(ctx context.Context) error {
	jobs, err := s.repo.GetDueCronJobs(ctx)
	if err != nil {
		return err
	}

	for _, job := range jobs {
		if err := s.triggerCronJob(ctx, job); err != nil {
			log.Error().
				Err(err).
				Str("job_id", job.ID.String()).
				Str("job_name", job.Name).
				Msg("Failed to trigger cron job")
		}
	}

	s.mu.Lock()
	s.stats.LastCronEval = time.Now()
	s.mu.Unlock()

	return nil
}

func (s *Scheduler) triggerCronJob(ctx context.Context, job *models.CronJob) error {
	now := time.Now().UTC()

	// Create task from job
	task := job.CreateTask()

	_, err := s.repo.CreateTask(ctx, task)
	if err != nil {
		return fmt.Errorf("failed to create task: %w", err)
	}

	// Calculate next run time
	parser := cron.NewParser(cron.Minute | cron.Hour | cron.Dom | cron.Month | cron.Dow)
	schedule, err := parser.Parse(job.Schedule)
	if err != nil {
		return fmt.Errorf("failed to parse schedule: %w", err)
	}
	nextRun := schedule.Next(now)

	// Update job
	_, err = s.repo.UpdateCronJobAfterRun(ctx, job.ID, nextRun, true)
	if err != nil {
		return fmt.Errorf("failed to update cron job: %w", err)
	}

	s.mu.Lock()
	s.stats.CronRuns++
	s.mu.Unlock()

	log.Info().
		Str("job_name", job.Name).
		Str("task_id", task.ID.String()).
		Time("next_run", nextRun).
		Msg("Triggered cron job")

	return nil
}

func (s *Scheduler) pendingPromotionLoop(ctx context.Context) {
	defer s.wg.Done()

	ticker := time.NewTicker(s.config.PendingPromotionInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			count, err := s.repo.PromotePendingTasks(ctx)
			if err != nil {
				log.Error().Err(err).Msg("Pending promotion error")
			} else if count > 0 {
				s.mu.Lock()
				s.stats.TasksPromoted += int64(count)
				s.mu.Unlock()
			}
		}
	}
}

func (s *Scheduler) timeoutRecoveryLoop(ctx context.Context) {
	defer s.wg.Done()

	ticker := time.NewTicker(s.config.TimeoutRecoveryInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			count, err := s.repo.RecoverTimedOutTasks(ctx)
			if err != nil {
				log.Error().Err(err).Msg("Timeout recovery error")
			} else if count > 0 {
				s.mu.Lock()
				s.stats.TasksRecovered += int64(count)
				s.mu.Unlock()
			}
		}
	}
}

func (s *Scheduler) healthCheckLoop(ctx context.Context) {
	defer s.wg.Done()

	timeout := s.workerConfig.HeartbeatInterval * 3
	ticker := time.NewTicker(s.config.HealthCheckInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			return
		case <-ticker.C:
			if s.IsLeader() {
				s.checkWorkerHealth(ctx, int(timeout.Seconds()))
			}
		}
	}
}

func (s *Scheduler) checkWorkerHealth(ctx context.Context, timeoutSeconds int) {
	staleWorkers, err := s.repo.GetStaleWorkers(ctx, timeoutSeconds)
	if err != nil {
		log.Error().Err(err).Msg("Failed to get stale workers")
		return
	}

	for _, worker := range staleWorkers {
		log.Warn().
			Str("worker_id", worker.ID.String()).
			Str("worker_name", worker.Name).
			Time("last_heartbeat", worker.LastHeartbeat).
			Msg("Worker heartbeat timeout")

		tasksAffected, err := s.repo.MarkWorkerInactive(ctx, worker.ID)
		if err != nil {
			log.Error().
				Err(err).
				Str("worker_id", worker.ID.String()).
				Msg("Failed to mark worker inactive")
		} else if tasksAffected > 0 {
			log.Warn().
				Str("worker_id", worker.ID.String()).
				Int("task_count", tasksAffected).
				Msg("Failed tasks from inactive worker")
		}
	}
}

// ============================================================================
// HEALTH CHECK
// ============================================================================

// Health returns the scheduler health status.
type Health struct {
	Status     string            `json:"status"`
	InstanceID string            `json:"instance_id"`
	IsLeader   bool              `json:"is_leader"`
	Components map[string]string `json:"components"`
}

// GetHealth returns the scheduler health status.
func (s *Scheduler) GetHealth(ctx context.Context) Health {
	health := Health{
		Status:     "healthy",
		InstanceID: s.instanceID.String(),
		IsLeader:   s.IsLeader(),
		Components: make(map[string]string),
	}

	// Check database
	if err := s.db.HealthCheck(ctx); err != nil {
		health.Status = "unhealthy"
		health.Components["database"] = "unhealthy"
	} else {
		health.Components["database"] = "healthy"
	}

	return health
}
