package engine

import (
	"time"
)

type Scheduler struct {
	engine *WorkflowEngine
	stop   chan struct{}
}

func NewScheduler(engine *WorkflowEngine) *Scheduler {
	return &Scheduler{engine: engine, stop: make(chan struct{})}
}

func (s *Scheduler) Start() {
	go s.run()
}

func (s *Scheduler) Stop() {
	close(s.stop)
}

func (s *Scheduler) run() {
	ticker := time.NewTicker(s.engine.Config.SchedulerInterval)
	defer ticker.Stop()
	for {
		select {
		case <-s.stop:
			return
		case <-ticker.C:
			now := float64(time.Now().UnixNano()) / 1e9
			heartbeatTasks, _ := s.engine.Persistence.FindHeartbeatExpiredTasks(now)
			for _, task := range heartbeatTasks {
				s.engine.RecordHeartbeatTimeout(task.TaskID)
			}
			timeoutTasks, _ := s.engine.Persistence.FindTimeoutExpiredTasks(now)
			for _, task := range timeoutTasks {
				s.engine.RecordTaskTimeout(task.TaskID)
			}
			runTimeouts, _ := s.engine.Persistence.FindRunTimeouts(now)
			for _, run := range runTimeouts {
				if runID, ok := run["run_id"].(string); ok {
					s.engine.RecordRunTimeout(runID)
				}
			}
		}
	}
}
