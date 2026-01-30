package config

import (
	"encoding/json"
	"os"
	"strconv"
)

// EngineConfig holds runtime configuration for the engine.
type EngineConfig struct {
	DBPath                       string  `json:"db_path"`
	WorkflowQueue                string  `json:"workflow_queue"`
	ActivityQueue                string  `json:"activity_queue"`
	WorkerPollIntervalSeconds    float64 `json:"worker_poll_interval_seconds"`
	SchedulerPollIntervalSeconds float64 `json:"scheduler_poll_interval_seconds"`
	LeaseSeconds                 int     `json:"lease_seconds"`
	ActivityMaxAttempts          int     `json:"activity_max_attempts"`
	WorkflowMaxAttempts          int     `json:"workflow_max_attempts"`
	BackoffInitialSeconds        float64 `json:"backoff_initial_seconds"`
	BackoffMaxSeconds            float64 `json:"backoff_max_seconds"`
	BackoffJitter                float64 `json:"backoff_jitter"`
	WorkflowTaskTimeoutSeconds   int     `json:"workflow_task_timeout_seconds"`
	ActivityTaskTimeoutSeconds   int     `json:"activity_task_timeout_seconds"`
	LogLevel                     string  `json:"log_level"`
	MetricsEnabled               bool    `json:"metrics_enabled"`
}

// DefaultConfig returns the default configuration.
func DefaultConfig() EngineConfig {
	return EngineConfig{
		DBPath:                       "workflow.db",
		WorkflowQueue:                "workflow",
		ActivityQueue:                "activity",
		WorkerPollIntervalSeconds:    0.2,
		SchedulerPollIntervalSeconds: 0.5,
		LeaseSeconds:                 30,
		ActivityMaxAttempts:          5,
		WorkflowMaxAttempts:          3,
		BackoffInitialSeconds:        1.0,
		BackoffMaxSeconds:            30.0,
		BackoffJitter:                0.2,
		WorkflowTaskTimeoutSeconds:   60,
		ActivityTaskTimeoutSeconds:   300,
		LogLevel:                     "INFO",
		MetricsEnabled:               true,
	}
}

// LoadConfig loads configuration from an optional JSON file and environment overrides.
func LoadConfig(path string) (EngineConfig, error) {
	cfg := DefaultConfig()
	if path != "" {
		raw, err := os.ReadFile(path)
		if err != nil {
			return cfg, err
		}
		if err := json.Unmarshal(raw, &cfg); err != nil {
			return cfg, err
		}
	}

	// Environment overrides with WF_ prefix.
	overrideString(&cfg.DBPath, "WF_DB_PATH")
	overrideString(&cfg.WorkflowQueue, "WF_WORKFLOW_QUEUE")
	overrideString(&cfg.ActivityQueue, "WF_ACTIVITY_QUEUE")
	overrideFloat(&cfg.WorkerPollIntervalSeconds, "WF_WORKER_POLL_INTERVAL_SECONDS")
	overrideFloat(&cfg.SchedulerPollIntervalSeconds, "WF_SCHEDULER_POLL_INTERVAL_SECONDS")
	overrideInt(&cfg.LeaseSeconds, "WF_LEASE_SECONDS")
	overrideInt(&cfg.ActivityMaxAttempts, "WF_ACTIVITY_MAX_ATTEMPTS")
	overrideInt(&cfg.WorkflowMaxAttempts, "WF_WORKFLOW_MAX_ATTEMPTS")
	overrideFloat(&cfg.BackoffInitialSeconds, "WF_BACKOFF_INITIAL_SECONDS")
	overrideFloat(&cfg.BackoffMaxSeconds, "WF_BACKOFF_MAX_SECONDS")
	overrideFloat(&cfg.BackoffJitter, "WF_BACKOFF_JITTER")
	overrideInt(&cfg.WorkflowTaskTimeoutSeconds, "WF_WORKFLOW_TASK_TIMEOUT_SECONDS")
	overrideInt(&cfg.ActivityTaskTimeoutSeconds, "WF_ACTIVITY_TASK_TIMEOUT_SECONDS")
	overrideString(&cfg.LogLevel, "WF_LOG_LEVEL")
	overrideBool(&cfg.MetricsEnabled, "WF_METRICS_ENABLED")

	return cfg, nil
}

func overrideString(target *string, key string) {
	if value, ok := os.LookupEnv(key); ok {
		*target = value
	}
}

func overrideInt(target *int, key string) {
	if value, ok := os.LookupEnv(key); ok {
		if parsed, err := strconv.Atoi(value); err == nil {
			*target = parsed
		}
	}
}

func overrideFloat(target *float64, key string) {
	if value, ok := os.LookupEnv(key); ok {
		if parsed, err := strconv.ParseFloat(value, 64); err == nil {
			*target = parsed
		}
	}
}

func overrideBool(target *bool, key string) {
	if value, ok := os.LookupEnv(key); ok {
		*target = value == "1" || value == "true" || value == "TRUE" || value == "yes"
	}
}
