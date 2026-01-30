package scheduler

import (
	"time"

	"github.com/google/uuid"

	"workflow/config"
	"workflow/engine"
	"workflow/logging"
)

// Scheduler scans for timers and expired tasks.
type Scheduler struct {
	engine      *engine.WorkflowEngine
	config      config.EngineConfig
	schedulerID string
	logger      *logging.Logger
}

// New creates a new scheduler.
func New(engine *engine.WorkflowEngine, cfg config.EngineConfig) *Scheduler {
	return &Scheduler{
		engine:      engine,
		config:      cfg,
		schedulerID: "scheduler-" + uuid.New().String(),
		logger:      logging.New(cfg.LogLevel),
	}
}

// Run executes the scheduling loop until stop is closed.
func (s *Scheduler) Run(stop <-chan struct{}) {
	s.logger.Info("Scheduler %s started", s.schedulerID)
	for {
		select {
		case <-stop:
			s.logger.Info("Scheduler %s stopped", s.schedulerID)
			return
		default:
		}

		timers, err := s.engine.Persistence().ListDueTimers()
		if err == nil {
			for _, task := range timers {
				s.engine.HandleTimerTask(&task)
			}
		}

		expired, err := s.engine.Persistence().ListExpiredLeases()
		if err == nil {
			for _, task := range expired {
				s.engine.HandleTaskTimeout(&task)
			}
		}

		time.Sleep(time.Duration(s.config.SchedulerPollIntervalSeconds * float64(time.Second)))
	}
}
