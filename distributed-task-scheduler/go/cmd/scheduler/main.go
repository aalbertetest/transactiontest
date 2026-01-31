// Package main provides the entry point for the scheduler service.
//
// Usage:
//
//	scheduler --config config.yaml
//
// Environment variables:
//   - DTS_CONFIG_PATH: Path to configuration file
//   - DTS_DATABASE__*: Database settings
//   - DTS_SCHEDULER__*: Scheduler settings
package main

import (
	"context"
	"flag"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/rs/zerolog"
	"github.com/rs/zerolog/log"

	"github.com/distributed-task-scheduler/internal/config"
	"github.com/distributed-task-scheduler/internal/persistence"
	"github.com/distributed-task-scheduler/internal/scheduler"
)

func main() {
	// Parse command line flags
	configPath := flag.String("config", "", "Path to configuration file")
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
		Bool("debug", cfg.Debug).
		Msg("Starting distributed task scheduler")

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

	// Create and start scheduler
	sched := scheduler.NewScheduler(cfg, db)
	if err := sched.Start(ctx); err != nil {
		log.Fatal().Err(err).Msg("Failed to start scheduler")
	}

	log.Info().Msg("Scheduler is running. Press Ctrl+C to stop.")

	// Wait for shutdown signal
	<-sigChan
	log.Info().Msg("Received shutdown signal")

	// Graceful shutdown with timeout
	shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), 30*time.Second)
	defer shutdownCancel()

	if err := sched.Stop(shutdownCtx); err != nil {
		log.Error().Err(err).Msg("Error during scheduler shutdown")
	}

	log.Info().Msg("Scheduler shutdown complete")
}
