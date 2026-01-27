// =============================================================================
// NEXUS PLATFORM - API GATEWAY - LOGGER
// =============================================================================
// Structured logging using zerolog.
// =============================================================================

package logger

import (
	"io"
	"os"
	"time"

	"github.com/rs/zerolog"
)

// Config holds logger configuration.
type Config struct {
	Level      string
	Format     string
	Output     string
	Service    string
	Version    string
	InstanceID string
}

// New creates a new configured logger.
func New(cfg Config) zerolog.Logger {
	// Parse log level
	level, err := zerolog.ParseLevel(cfg.Level)
	if err != nil {
		level = zerolog.InfoLevel
	}
	zerolog.SetGlobalLevel(level)

	// Configure time format
	zerolog.TimeFieldFormat = time.RFC3339Nano

	// Configure output
	var output io.Writer
	switch cfg.Output {
	case "stdout":
		output = os.Stdout
	case "stderr":
		output = os.Stderr
	default:
		output = os.Stdout
	}

	// Configure format
	if cfg.Format == "text" || cfg.Format == "console" {
		output = zerolog.ConsoleWriter{
			Out:        output,
			TimeFormat: time.RFC3339,
		}
	}

	// Create logger with context
	logger := zerolog.New(output).
		With().
		Timestamp().
		Str("service", cfg.Service).
		Str("version", cfg.Version).
		Str("instance_id", cfg.InstanceID).
		Logger()

	return logger
}

// WithRequestID adds request ID to logger context.
func WithRequestID(logger zerolog.Logger, requestID string) zerolog.Logger {
	return logger.With().Str("request_id", requestID).Logger()
}

// WithUserID adds user ID to logger context.
func WithUserID(logger zerolog.Logger, userID string) zerolog.Logger {
	return logger.With().Str("user_id", userID).Logger()
}

// WithService adds service name to logger context.
func WithService(logger zerolog.Logger, service string) zerolog.Logger {
	return logger.With().Str("target_service", service).Logger()
}
