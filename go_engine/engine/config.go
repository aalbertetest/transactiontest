package engine

import (
	"encoding/json"
	"os"
	"strconv"
	"strings"
	"time"
)

type Config struct {
	DBPath                         string
	WorkflowTaskQueue              string
	ActivityTaskQueue              string
	TimerTaskQueue                 string
	WorkerPollInterval             time.Duration
	SchedulerInterval              time.Duration
	TaskLeaseSeconds               int
	ActivityHeartbeatTimeoutSeconds int
	WorkflowTaskTimeoutSeconds     int
	RunTimeoutSeconds              int
	MaxTaskAttempts                int
	LogLevel                       string
}

func DefaultConfig() Config {
	return Config{
		DBPath:                         "engine.sqlite",
		WorkflowTaskQueue:              "workflow-tasks",
		ActivityTaskQueue:              "activity-tasks",
		TimerTaskQueue:                 "timer-tasks",
		WorkerPollInterval:             500 * time.Millisecond,
		SchedulerInterval:              1 * time.Second,
		TaskLeaseSeconds:               30,
		ActivityHeartbeatTimeoutSeconds: 60,
		WorkflowTaskTimeoutSeconds:     30,
		RunTimeoutSeconds:              3600,
		MaxTaskAttempts:                10,
		LogLevel:                       "INFO",
	}
}

func LoadConfig(path string) (Config, error) {
	cfg := DefaultConfig()
	if path != "" {
		data, err := os.ReadFile(path)
		if err != nil {
			return cfg, err
		}
		_ = json.Unmarshal(data, &cfg)
	}

	prefix := "WF_ENGINE_"
	for _, env := range os.Environ() {
		parts := strings.SplitN(env, "=", 2)
		if len(parts) != 2 {
			continue
		}
		key := parts[0]
		value := parts[1]
		if !strings.HasPrefix(key, prefix) {
			continue
		}
		field := strings.ToLower(strings.TrimPrefix(key, prefix))
		switch field {
		case "db_path":
			cfg.DBPath = value
		case "workflow_task_queue":
			cfg.WorkflowTaskQueue = value
		case "activity_task_queue":
			cfg.ActivityTaskQueue = value
		case "timer_task_queue":
			cfg.TimerTaskQueue = value
		case "worker_poll_interval_seconds":
			if v, err := strconv.ParseFloat(value, 64); err == nil {
				cfg.WorkerPollInterval = time.Duration(v * float64(time.Second))
			}
		case "scheduler_interval_seconds":
			if v, err := strconv.ParseFloat(value, 64); err == nil {
				cfg.SchedulerInterval = time.Duration(v * float64(time.Second))
			}
		case "task_lease_seconds":
			if v, err := strconv.Atoi(value); err == nil {
				cfg.TaskLeaseSeconds = v
			}
		case "activity_heartbeat_timeout_seconds":
			if v, err := strconv.Atoi(value); err == nil {
				cfg.ActivityHeartbeatTimeoutSeconds = v
			}
		case "workflow_task_timeout_seconds":
			if v, err := strconv.Atoi(value); err == nil {
				cfg.WorkflowTaskTimeoutSeconds = v
			}
		case "run_timeout_seconds":
			if v, err := strconv.Atoi(value); err == nil {
				cfg.RunTimeoutSeconds = v
			}
		case "max_task_attempts":
			if v, err := strconv.Atoi(value); err == nil {
				cfg.MaxTaskAttempts = v
			}
		case "log_level":
			cfg.LogLevel = value
		}
	}

	return cfg, nil
}
