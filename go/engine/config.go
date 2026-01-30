package engine

import (
	"encoding/json"
	"os"
	"strconv"
)

// Config defines all runtime configuration for the engine.
type Config struct {
	DBPath                            string  `json:"db_path"`
	TaskQueueName                     string  `json:"task_queue_name"`
	WorkerID                          string  `json:"worker_id"`
	PollIntervalSeconds               float64 `json:"poll_interval_seconds"`
	SchedulerIntervalSeconds          float64 `json:"scheduler_interval_seconds"`
	LeaseDurationSeconds              int     `json:"lease_duration_seconds"`
	ActivityHeartbeatTimeoutSeconds   int     `json:"activity_heartbeat_timeout_seconds"`
	ActivityScheduleToCloseTimeoutSec int     `json:"activity_schedule_to_close_timeout_seconds"`
	ActivityStartToCloseTimeoutSec    int     `json:"activity_start_to_close_timeout_seconds"`
	RetryInitialIntervalSeconds       int     `json:"retry_initial_interval_seconds"`
	RetryMaxIntervalSeconds           int     `json:"retry_max_interval_seconds"`
	RetryBackoffCoefficient           float64 `json:"retry_backoff_coefficient"`
	RetryMaxAttempts                  int     `json:"retry_max_attempts"`
	MetricsEnabled                    bool    `json:"metrics_enabled"`
	LogLevel                          string  `json:"log_level"`
}

// DefaultConfig returns configuration with sensible defaults.
func DefaultConfig() Config {
	return Config{
		DBPath:                            "workflow.db",
		TaskQueueName:                     "default",
		WorkerID:                          "worker-1",
		PollIntervalSeconds:               0.5,
		SchedulerIntervalSeconds:          0.5,
		LeaseDurationSeconds:              30,
		ActivityHeartbeatTimeoutSeconds:   30,
		ActivityScheduleToCloseTimeoutSec: 300,
		ActivityStartToCloseTimeoutSec:    60,
		RetryInitialIntervalSeconds:       1,
		RetryMaxIntervalSeconds:           60,
		RetryBackoffCoefficient:           2.0,
		RetryMaxAttempts:                  3,
		MetricsEnabled:                    true,
		LogLevel:                          "INFO",
	}
}

// LoadConfigFromEnv overrides defaults from environment variables.
func LoadConfigFromEnv() Config {
	cfg := DefaultConfig()
	cfg.DBPath = getEnvString("WF_DB_PATH", cfg.DBPath)
	cfg.TaskQueueName = getEnvString("WF_TASK_QUEUE", cfg.TaskQueueName)
	cfg.WorkerID = getEnvString("WF_WORKER_ID", cfg.WorkerID)
	cfg.PollIntervalSeconds = getEnvFloat("WF_POLL_INTERVAL_SECONDS", cfg.PollIntervalSeconds)
	cfg.SchedulerIntervalSeconds = getEnvFloat("WF_SCHEDULER_INTERVAL_SECONDS", cfg.SchedulerIntervalSeconds)
	cfg.LeaseDurationSeconds = getEnvInt("WF_LEASE_DURATION_SECONDS", cfg.LeaseDurationSeconds)
	cfg.ActivityHeartbeatTimeoutSeconds = getEnvInt("WF_ACTIVITY_HEARTBEAT_TIMEOUT_SECONDS", cfg.ActivityHeartbeatTimeoutSeconds)
	cfg.ActivityScheduleToCloseTimeoutSec = getEnvInt("WF_ACTIVITY_SCHEDULE_TO_CLOSE_TIMEOUT_SECONDS", cfg.ActivityScheduleToCloseTimeoutSec)
	cfg.ActivityStartToCloseTimeoutSec = getEnvInt("WF_ACTIVITY_START_TO_CLOSE_TIMEOUT_SECONDS", cfg.ActivityStartToCloseTimeoutSec)
	cfg.RetryInitialIntervalSeconds = getEnvInt("WF_RETRY_INITIAL_INTERVAL_SECONDS", cfg.RetryInitialIntervalSeconds)
	cfg.RetryMaxIntervalSeconds = getEnvInt("WF_RETRY_MAX_INTERVAL_SECONDS", cfg.RetryMaxIntervalSeconds)
	cfg.RetryBackoffCoefficient = getEnvFloat("WF_RETRY_BACKOFF_COEFFICIENT", cfg.RetryBackoffCoefficient)
	cfg.RetryMaxAttempts = getEnvInt("WF_RETRY_MAX_ATTEMPTS", cfg.RetryMaxAttempts)
	cfg.MetricsEnabled = getEnvBool("WF_METRICS_ENABLED", cfg.MetricsEnabled)
	cfg.LogLevel = getEnvString("WF_LOG_LEVEL", cfg.LogLevel)
	return cfg
}

// LoadConfigFromFile merges a JSON config file with environment overrides.
func LoadConfigFromFile(path string) (Config, error) {
	cfg := LoadConfigFromEnv()
	handle, err := os.Open(path)
	if err != nil {
		return cfg, err
	}
	defer handle.Close()

	decoder := json.NewDecoder(handle)
	if err := decoder.Decode(&cfg); err != nil {
		return cfg, err
	}
	return cfg, nil
}

func getEnvString(name, def string) string {
	value := os.Getenv(name)
	if value == "" {
		return def
	}
	return value
}

func getEnvInt(name string, def int) int {
	value := os.Getenv(name)
	if value == "" {
		return def
	}
	parsed, err := strconv.Atoi(value)
	if err != nil {
		return def
	}
	return parsed
}

func getEnvFloat(name string, def float64) float64 {
	value := os.Getenv(name)
	if value == "" {
		return def
	}
	parsed, err := strconv.ParseFloat(value, 64)
	if err != nil {
		return def
	}
	return parsed
}

func getEnvBool(name string, def bool) bool {
	value := os.Getenv(name)
	if value == "" {
		return def
	}
	return value == "1" || value == "true" || value == "yes" || value == "on"
}
