package engine

import (
	"time"
)

// TimerScheduler scans for due timers and activity timeouts.
type TimerScheduler struct {
	store   *SQLiteStore
	queue   TaskQueue
	config  Config
	metrics *MetricsRegistry
	logger  *Logger
	stopCh  chan struct{}
}

func NewTimerScheduler(store *SQLiteStore, queue TaskQueue, config Config, metrics *MetricsRegistry) *TimerScheduler {
	return &TimerScheduler{
		store:   store,
		queue:   queue,
		config:  config,
		metrics: metrics,
		logger:  NewLogger(config.LogLevel),
		stopCh:  make(chan struct{}),
	}
}

func (s *TimerScheduler) Start() {
	go s.Run()
}

func (s *TimerScheduler) Stop() {
	close(s.stopCh)
}

func (s *TimerScheduler) Run() {
	for {
		select {
		case <-s.stopCh:
			return
		default:
			s.RunOnce()
			time.Sleep(time.Duration(s.config.SchedulerIntervalSeconds * float64(time.Second)))
		}
	}
}

func (s *TimerScheduler) RunOnce() {
	now := time.Now().Unix()
	s.fireDueTimers(now)
	s.handleActivityTimeouts(now)
}

func (s *TimerScheduler) fireDueTimers(now int64) {
	timers, err := s.store.ListDueTimers(now)
	if err != nil {
		s.logger.Errorf("list due timers error=%v", err)
		return
	}
	for _, timer := range timers {
		timerID := timer["timer_id"].(string)
		workflowID := timer["workflow_id"].(string)
		runID := timer["run_id"].(string)
		if err := s.store.MarkTimerFired(timerID); err != nil {
			s.logger.Errorf("mark timer fired error=%v", err)
			continue
		}
		_, _ = s.store.AppendEvent(workflowID, runID, EventTimerFired, map[string]interface{}{
			"timer_id": timerID,
		})
		exec, err := s.store.GetWorkflowExecution(workflowID, runID)
		if err != nil || exec == nil {
			continue
		}
		payload := map[string]interface{}{
			"workflow_id":   workflowID,
			"run_id":        runID,
			"workflow_type": exec.WorkflowType,
			"task_queue":    exec.TaskQueue,
		}
		_, _ = s.queue.Enqueue(exec.TaskQueue, "workflow", payload, nil, 1)
		if s.metrics != nil {
			s.metrics.Inc("scheduler.timer_fired", 1)
		}
	}
}

func (s *TimerScheduler) handleActivityTimeouts(now int64) {
	activities, err := s.store.ListActivityTasksByState([]string{ActivityStateScheduled, ActivityStateStarted, ActivityStateRetrying})
	if err != nil {
		s.logger.Errorf("list activities error=%v", err)
		return
	}
	for _, activity := range activities {
		reason := activityTimeoutReason(activity, now)
		if reason == "" {
			continue
		}
		errMessage := "activity timeout: " + reason
		if activity.Attempt+1 < activity.MaxAttempts {
			_ = s.store.RecordActivityRetrying(activity.ActivityID, errMessage)
			_, _ = s.store.AppendEvent(activity.WorkflowID, activity.RunID, EventActivityTaskTimedOut, map[string]interface{}{
				"activity_id": activity.ActivityID,
				"error":       errMessage,
			})
			_, _ = s.store.AppendEvent(activity.WorkflowID, activity.RunID, EventActivityTaskRetryScheduled, map[string]interface{}{
				"activity_id": activity.ActivityID,
				"error":       errMessage,
			})
			backoff := ComputeBackoffSeconds(activity.RetryPolicy, activity.Attempt+1)
			payload := map[string]interface{}{
				"activity_id": activity.ActivityID,
				"workflow_id": activity.WorkflowID,
				"run_id":      activity.RunID,
			}
			visibleAt := now + int64(backoff)
			_, _ = s.queue.Enqueue(s.config.TaskQueueName, "activity", payload, &visibleAt, 1)
			if s.metrics != nil {
				s.metrics.Inc("scheduler.activity_retry", 1)
			}
			continue
		}
		_ = s.store.RecordActivityTimedOut(activity.ActivityID, errMessage)
		_, _ = s.store.AppendEvent(activity.WorkflowID, activity.RunID, EventActivityTaskTimedOut, map[string]interface{}{
			"activity_id": activity.ActivityID,
			"error":       errMessage,
		})
		exec, err := s.store.GetWorkflowExecution(activity.WorkflowID, activity.RunID)
		if err == nil && exec != nil {
			payload := map[string]interface{}{
				"workflow_id":   activity.WorkflowID,
				"run_id":        activity.RunID,
				"workflow_type": exec.WorkflowType,
				"task_queue":    exec.TaskQueue,
			}
			_, _ = s.queue.Enqueue(exec.TaskQueue, "workflow", payload, nil, 1)
		}
		if s.metrics != nil {
			s.metrics.Inc("scheduler.activity_timeout", 1)
		}
	}
}

func activityTimeoutReason(activity ActivityTask, now int64) string {
	switch activity.State {
	case ActivityStateScheduled, ActivityStateRetrying:
		if now-activity.ScheduledAt > int64(activity.ScheduleToCloseTimeoutSeconds) {
			return "schedule_to_close"
		}
	case ActivityStateStarted:
		if activity.StartedAt != nil && now-*activity.StartedAt > int64(activity.StartToCloseTimeoutSeconds) {
			return "start_to_close"
		}
		if activity.HeartbeatAt != nil && now-*activity.HeartbeatAt > int64(activity.HeartbeatTimeoutSeconds) {
			return "heartbeat_timeout"
		}
	}
	return ""
}
