// Package config provides configuration management for the distributed task scheduler.
//
// Configuration can be loaded from:
//   - YAML configuration files
//   - Environment variables (with DTS_ prefix)
//   - Programmatic defaults
//
// Environment variables override file configuration, and file configuration
// overrides defaults.
package config

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"time"

	"gopkg.in/yaml.v3"
)

// Config is the root configuration structure.
type Config struct {
	Database  DatabaseConfig  `yaml:"database"`
	Scheduler SchedulerConfig `yaml:"scheduler"`
	Worker    WorkerConfig    `yaml:"worker"`
	Retry     RetryConfig     `yaml:"retry"`
	Metrics   MetricsConfig   `yaml:"metrics"`
	Logging   LoggingConfig   `yaml:"logging"`

	// Environment is the deployment environment name.
	Environment string `yaml:"environment"`

	// Debug enables debug mode.
	Debug bool `yaml:"debug"`
}

// DatabaseConfig contains database connection settings.
type DatabaseConfig struct {
	// Host is the database server hostname.
	Host string `yaml:"host"`

	// Port is the database server port.
	Port int `yaml:"port"`

	// Name is the database name.
	Name string `yaml:"name"`

	// User is the database username.
	User string `yaml:"user"`

	// Password is the database password.
	Password string `yaml:"password"`

	// MaxConnections is the maximum pool connections.
	MaxConnections int `yaml:"max_connections"`

	// MinConnections is the minimum pool connections.
	MinConnections int `yaml:"min_connections"`

	// ConnectionTimeout is the connection timeout.
	ConnectionTimeout time.Duration `yaml:"connection_timeout"`

	// CommandTimeout is the default command timeout.
	CommandTimeout time.Duration `yaml:"command_timeout"`

	// SSLMode is the PostgreSQL SSL mode.
	SSLMode string `yaml:"ssl_mode"`
}

// DSN returns the PostgreSQL connection string.
func (c *DatabaseConfig) DSN() string {
	password := ""
	if c.Password != "" {
		password = ":" + c.Password
	}
	return fmt.Sprintf("postgresql://%s%s@%s:%d/%s?sslmode=%s",
		c.User, password, c.Host, c.Port, c.Name, c.SSLMode)
}

// SchedulerConfig contains scheduler service settings.
type SchedulerConfig struct {
	// LeaderElectionTTL is the leader lock TTL in seconds.
	LeaderElectionTTL int `yaml:"leader_election_ttl"`

	// LeaderRenewalInterval is the lock renewal interval in seconds.
	LeaderRenewalInterval int `yaml:"leader_renewal_interval"`

	// CronTickInterval is the cron evaluation interval.
	CronTickInterval time.Duration `yaml:"cron_tick_interval"`

	// HealthCheckInterval is the worker health check interval.
	HealthCheckInterval time.Duration `yaml:"health_check_interval"`

	// PendingPromotionInterval is the pending task promotion interval.
	PendingPromotionInterval time.Duration `yaml:"pending_promotion_interval"`

	// TimeoutRecoveryInterval is the timeout recovery interval.
	TimeoutRecoveryInterval time.Duration `yaml:"timeout_recovery_interval"`

	// InstanceID is the unique scheduler instance ID.
	InstanceID string `yaml:"instance_id"`
}

// WorkerConfig contains worker process settings.
type WorkerConfig struct {
	// Queues is the list of queues to process.
	Queues []string `yaml:"queues"`

	// Concurrency is the maximum concurrent tasks.
	Concurrency int `yaml:"concurrency"`

	// BatchSize is the number of tasks to claim per poll.
	BatchSize int `yaml:"batch_size"`

	// HeartbeatInterval is the heartbeat interval.
	HeartbeatInterval time.Duration `yaml:"heartbeat_interval"`

	// VisibilityTimeout is the task visibility timeout.
	VisibilityTimeout time.Duration `yaml:"visibility_timeout"`

	// PollInterval is the poll interval when queue is empty.
	PollInterval time.Duration `yaml:"poll_interval"`

	// MaxPollInterval is the maximum poll interval during backoff.
	MaxPollInterval time.Duration `yaml:"max_poll_interval"`

	// ShutdownTimeout is the graceful shutdown timeout.
	ShutdownTimeout time.Duration `yaml:"shutdown_timeout"`

	// WorkerID is the unique worker ID.
	WorkerID string `yaml:"worker_id"`
}

// RetryConfig contains default retry policy settings.
type RetryConfig struct {
	// DefaultMaxAttempts is the default maximum attempts.
	DefaultMaxAttempts int `yaml:"default_max_attempts"`

	// DefaultBaseDelay is the default base delay in seconds.
	DefaultBaseDelay float64 `yaml:"default_base_delay"`

	// DefaultMaxDelay is the default maximum delay in seconds.
	DefaultMaxDelay float64 `yaml:"default_max_delay"`

	// ExponentialBase is the exponential multiplier.
	ExponentialBase float64 `yaml:"exponential_base"`

	// Jitter enables delay randomization.
	Jitter bool `yaml:"jitter"`
}

// MetricsConfig contains metrics and observability settings.
type MetricsConfig struct {
	// Enabled indicates if metrics are enabled.
	Enabled bool `yaml:"enabled"`

	// Port is the metrics server port.
	Port int `yaml:"port"`

	// Path is the metrics endpoint path.
	Path string `yaml:"path"`

	// Namespace is the metric name prefix.
	Namespace string `yaml:"namespace"`
}

// LoggingConfig contains logging configuration.
type LoggingConfig struct {
	// Level is the log level (DEBUG, INFO, WARN, ERROR).
	Level string `yaml:"level"`

	// Format is the log format (json, console).
	Format string `yaml:"format"`

	// Output is the log output (stdout, stderr, or file path).
	Output string `yaml:"output"`

	// IncludeTimestamp indicates if timestamps should be included.
	IncludeTimestamp bool `yaml:"include_timestamp"`
}

// DefaultConfig returns a configuration with sensible defaults.
func DefaultConfig() *Config {
	return &Config{
		Database: DatabaseConfig{
			Host:              "localhost",
			Port:              5432,
			Name:              "taskscheduler",
			User:              "postgres",
			Password:          "",
			MaxConnections:    20,
			MinConnections:    5,
			ConnectionTimeout: 30 * time.Second,
			CommandTimeout:    60 * time.Second,
			SSLMode:           "prefer",
		},
		Scheduler: SchedulerConfig{
			LeaderElectionTTL:        30,
			LeaderRenewalInterval:    10,
			CronTickInterval:         1 * time.Second,
			HealthCheckInterval:      10 * time.Second,
			PendingPromotionInterval: 1 * time.Second,
			TimeoutRecoveryInterval:  30 * time.Second,
			InstanceID:               "",
		},
		Worker: WorkerConfig{
			Queues:            []string{"default"},
			Concurrency:       10,
			BatchSize:         5,
			HeartbeatInterval: 10 * time.Second,
			VisibilityTimeout: 5 * time.Minute,
			PollInterval:      1 * time.Second,
			MaxPollInterval:   30 * time.Second,
			ShutdownTimeout:   60 * time.Second,
			WorkerID:          "",
		},
		Retry: RetryConfig{
			DefaultMaxAttempts: 3,
			DefaultBaseDelay:   1.0,
			DefaultMaxDelay:    3600.0,
			ExponentialBase:    2.0,
			Jitter:             true,
		},
		Metrics: MetricsConfig{
			Enabled:   true,
			Port:      9090,
			Path:      "/metrics",
			Namespace: "dts",
		},
		Logging: LoggingConfig{
			Level:            "INFO",
			Format:           "json",
			Output:           "stdout",
			IncludeTimestamp: true,
		},
		Environment: "development",
		Debug:       false,
	}
}

// LoadConfig loads configuration from a YAML file.
// Environment variables override file values.
func LoadConfig(path string) (*Config, error) {
	cfg := DefaultConfig()

	// Load from file if exists
	if path != "" {
		data, err := os.ReadFile(path)
		if err != nil {
			if !os.IsNotExist(err) {
				return nil, fmt.Errorf("failed to read config file: %w", err)
			}
			// File not found, use defaults
		} else {
			// Expand environment variables in file
			expanded := os.ExpandEnv(string(data))

			if err := yaml.Unmarshal([]byte(expanded), cfg); err != nil {
				return nil, fmt.Errorf("failed to parse config file: %w", err)
			}
		}
	}

	// Override with environment variables
	loadFromEnv(cfg)

	// Validate configuration
	if err := cfg.Validate(); err != nil {
		return nil, fmt.Errorf("invalid configuration: %w", err)
	}

	return cfg, nil
}

// loadFromEnv loads configuration from environment variables.
func loadFromEnv(cfg *Config) {
	// Database settings
	if v := os.Getenv("DTS_DATABASE__HOST"); v != "" {
		cfg.Database.Host = v
	}
	if v := os.Getenv("DTS_DATABASE__PORT"); v != "" {
		if port, err := strconv.Atoi(v); err == nil {
			cfg.Database.Port = port
		}
	}
	if v := os.Getenv("DTS_DATABASE__NAME"); v != "" {
		cfg.Database.Name = v
	}
	if v := os.Getenv("DTS_DATABASE__USER"); v != "" {
		cfg.Database.User = v
	}
	if v := os.Getenv("DTS_DATABASE__PASSWORD"); v != "" {
		cfg.Database.Password = v
	}

	// Scheduler settings
	if v := os.Getenv("DTS_SCHEDULER__LEADER_ELECTION_TTL"); v != "" {
		if ttl, err := strconv.Atoi(v); err == nil {
			cfg.Scheduler.LeaderElectionTTL = ttl
		}
	}
	if v := os.Getenv("DTS_SCHEDULER__INSTANCE_ID"); v != "" {
		cfg.Scheduler.InstanceID = v
	}

	// Worker settings
	if v := os.Getenv("DTS_WORKER__QUEUES"); v != "" {
		cfg.Worker.Queues = strings.Split(v, ",")
	}
	if v := os.Getenv("DTS_WORKER__CONCURRENCY"); v != "" {
		if c, err := strconv.Atoi(v); err == nil {
			cfg.Worker.Concurrency = c
		}
	}
	if v := os.Getenv("DTS_WORKER__WORKER_ID"); v != "" {
		cfg.Worker.WorkerID = v
	}

	// Metrics settings
	if v := os.Getenv("DTS_METRICS__ENABLED"); v != "" {
		cfg.Metrics.Enabled = strings.ToLower(v) == "true"
	}
	if v := os.Getenv("DTS_METRICS__PORT"); v != "" {
		if port, err := strconv.Atoi(v); err == nil {
			cfg.Metrics.Port = port
		}
	}

	// Logging settings
	if v := os.Getenv("DTS_LOGGING__LEVEL"); v != "" {
		cfg.Logging.Level = strings.ToUpper(v)
	}
	if v := os.Getenv("DTS_LOGGING__FORMAT"); v != "" {
		cfg.Logging.Format = v
	}

	// General settings
	if v := os.Getenv("DTS_ENVIRONMENT"); v != "" {
		cfg.Environment = v
	}
	if v := os.Getenv("DTS_DEBUG"); v != "" {
		cfg.Debug = strings.ToLower(v) == "true"
	}
}

// Validate checks that the configuration is valid.
func (c *Config) Validate() error {
	// Validate database settings
	if c.Database.Host == "" {
		return fmt.Errorf("database host is required")
	}
	if c.Database.Port < 1 || c.Database.Port > 65535 {
		return fmt.Errorf("database port must be between 1 and 65535")
	}
	if c.Database.Name == "" {
		return fmt.Errorf("database name is required")
	}
	if c.Database.MinConnections > c.Database.MaxConnections {
		return fmt.Errorf("min_connections cannot be greater than max_connections")
	}

	// Validate scheduler settings
	if c.Scheduler.LeaderRenewalInterval >= c.Scheduler.LeaderElectionTTL {
		return fmt.Errorf("leader_renewal_interval must be less than leader_election_ttl")
	}

	// Validate worker settings
	if len(c.Worker.Queues) == 0 {
		return fmt.Errorf("at least one queue must be configured")
	}
	if c.Worker.Concurrency < 1 {
		return fmt.Errorf("worker concurrency must be at least 1")
	}

	// Validate logging level
	validLevels := map[string]bool{
		"DEBUG": true, "INFO": true, "WARN": true, "ERROR": true,
	}
	if !validLevels[c.Logging.Level] {
		return fmt.Errorf("invalid log level: %s", c.Logging.Level)
	}

	return nil
}
