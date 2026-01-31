// Package main provides the entry point for the worker process.
//
// Usage:
//
//	worker --config config.yaml --queues default,high-priority
//
// Environment variables:
//   - DTS_CONFIG_PATH: Path to configuration file
//   - DTS_WORKER__*: Worker settings
package main

import (
	"context"
	"encoding/json"
	"flag"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/distributed-task-scheduler/internal/config"
	"github.com/distributed-task-scheduler/internal/persistence"
	"github.com/distributed-task-scheduler/internal/worker"
	"github.com/distributed-task-scheduler/pkg/models"
)

func main() {
	// Parse command line flags
	configPath := flag.String("config", "", "Path to configuration file")
	queuesFlag := flag.String("queues", "", "Comma-separated list of queues to process")
	flag.Parse()

	// Check environment variable for config path
	if *configPath == "" {
		*configPath = os.Getenv("DTS_CONFIG_PATH")
	}

	// Setup logging
	zerolog.TimeFieldFormat = time.RFC3339
	log.Logger = log.Output(zerolog.ConsoleWriter{Out: os.Stderr, TimeFormat: time.RFC3339})

	// Load configuration
	cfg, err := config.LoadConfig(*configPath)
	if err != nil {
		log.Fatal().Err(err).Msg("Failed to load configuration")
	}

	// Override queues from command line if provided
	if *queuesFlag != "" {
		cfg.Worker.Queues = strings.Split(*queuesFlag, ",")
	}

	// Set log level
	switch cfg.Logging.Level {
	case "DEBUG":
		zerolog.SetGlobalLevel(zerolog.DebugLevel)
	case "INFO":
		zerolog.SetGlobalLevel(zerolog.InfoLevel)
	case "WARN":
		zerolog.SetGlobalLevel(zerolog.WarnLevel)
	case "ERROR":
		zerolog.SetGlobalLevel(zerolog.ErrorLevel)
	}

	if cfg.Logging.Format == "json" {
		log.Logger = zerolog.New(os.Stdout).With().Timestamp().Logger()
	}

	log.Info().
		Str("environment", cfg.Environment).
		Strs("queues", cfg.Worker.Queues).
		Int("concurrency", cfg.Worker.Concurrency).
		Msg("Starting task worker")

	// Create context that cancels on signal
	ctx, cancel := context.WithCancel(context.Background())
	defer cancel()

	// Handle shutdown signals
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)

	// Connect to database
	db := persistence.NewDatabase(cfg.Database)
	if err := db.Connect(ctx); err != nil {
		log.Fatal().Err(err).Msg("Failed to connect to database")
	}
	defer db.Close()

	// Create worker
	w := worker.NewWorker(cfg, db)

	// Register example handlers
	registerExampleHandlers(w)

	// Start worker
	if err := w.Start(ctx); err != nil {
		log.Fatal().Err(err).Msg("Failed to start worker")
	}

	log.Info().Msg("Worker is running. Press Ctrl+C to stop.")

	// Wait for shutdown signal
	<-sigChan
	log.Info().Msg("Received shutdown signal")

	// Graceful shutdown with timeout
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), cfg.Worker.ShutdownTimeout)
	defer shutdownCancel()

	if err := w.Stop(shutdownCtx); err != nil {
		log.Error().Err(err).Msg("Error during worker shutdown")
	}

	log.Info().Msg("Worker shutdown complete")
}

// registerExampleHandlers registers example task handlers for demonstration.
func registerExampleHandlers(w *worker.Worker) {
	// Echo handler - returns the payload as the result
	w.RegisterHandler("echo", func(ctx context.Context, task *models.Task) (json.RawMessage, error) {
		log.Info().
			Str("task_id", task.ID.String()).
			RawJSON("payload", task.Payload).
			Msg("Echo handler processing task")

		return json.Marshal(map[string]interface{}{
			"echo":       task.Payload,
			"task_id":    task.ID.String(),
			"attempt":    task.AttemptCount,
			"queue":      task.QueueName,
			"processed_at": time.Now().UTC(),
		})
	})

	// Sleep handler - sleeps for the specified duration
	w.RegisterHandler("sleep", func(ctx context.Context, task *models.Task) (json.RawMessage, error) {
		var payload struct {
			Duration int `json:"duration"`
		}
		if err := json.Unmarshal(task.Payload, &payload); err != nil {
			return nil, err
		}

		duration := time.Duration(payload.Duration) * time.Second
		log.Info().
			Str("task_id", task.ID.String()).
			Dur("duration", duration).
			Msg("Sleep handler processing task")

		select {
		case <-time.After(duration):
			return json.Marshal(map[string]interface{}{
				"slept":    payload.Duration,
				"task_id":  task.ID.String(),
			})
		case <-ctx.Done():
			return nil, ctx.Err()
		}
	})

	// Fail handler - always fails (for testing retry logic)
	w.RegisterHandler("fail", func(ctx context.Context, task *models.Task) (json.RawMessage, error) {
		log.Info().
			Str("task_id", task.ID.String()).
			Int("attempt", task.AttemptCount).
			Msg("Fail handler - intentionally failing")

		return nil, &TestError{Message: "intentional failure for testing"}
	})

	log.Info().Msg("Registered example handlers: echo, sleep, fail")
}

// TestError is a custom error type for testing.
type TestError struct {
	Message string
}

func (e *TestError) Error() string {
	return e.Message
}
