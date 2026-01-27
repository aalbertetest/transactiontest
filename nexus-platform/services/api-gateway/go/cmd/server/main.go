// =============================================================================
// NEXUS PLATFORM - API GATEWAY - MAIN ENTRY POINT
// =============================================================================
// Production-grade API Gateway server with graceful shutdown and lifecycle
// management.
// =============================================================================

package main

import (
	"context"
	"fmt"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/nexus-platform/api-gateway/internal/config"
	"github.com/nexus-platform/api-gateway/internal/gateway"
	"github.com/nexus-platform/api-gateway/internal/logger"
	"github.com/nexus-platform/api-gateway/internal/metrics"
	"github.com/nexus-platform/api-gateway/internal/tracing"
)

// Version information (set at build time via ldflags)
var (
	Version   = "1.0.0"
	BuildTime = "unknown"
	GitCommit = "unknown"
)

func main() {
	// Load configuration
	cfg, err := config.Load()
	if err != nil {
		fmt.Fprintf(os.Stderr, "Failed to load configuration: %v\n", err)
		os.Exit(1)
	}

	// Initialize logger
	log := logger.New(logger.Config{
		Level:      cfg.Logging.Level,
		Format:     cfg.Logging.Format,
		Output:     cfg.Logging.Output,
		Service:    cfg.ServiceName,
		Version:    Version,
		InstanceID: cfg.InstanceID,
	})

	log.Info().
		Str("version", Version).
		Str("build_time", BuildTime).
		Str("git_commit", GitCommit).
		Str("environment", cfg.Environment).
		Msg("Starting Nexus Platform API Gateway")

	// Initialize tracing
	if cfg.Tracing.Enabled {
		tp, err := tracing.InitTracer(tracing.Config{
			ServiceName:  cfg.ServiceName,
			JaegerHost:   cfg.Tracing.JaegerHost,
			JaegerPort:   cfg.Tracing.JaegerPort,
			SamplingRate: cfg.Tracing.SamplingRate,
		})
		if err != nil {
			log.Warn().Err(err).Msg("Failed to initialize tracing, continuing without it")
		} else {
			defer func() {
				ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
				defer cancel()
				if err := tp.Shutdown(ctx); err != nil {
					log.Error().Err(err).Msg("Error shutting down tracer provider")
				}
			}()
			log.Info().Msg("Tracing initialized")
		}
	}

	// Initialize metrics
	if cfg.Metrics.Enabled {
		metrics.Init(cfg.Metrics.Prefix)
		log.Info().Msg("Metrics initialized")
	}

	// Create gateway
	gw, err := gateway.New(gateway.Config{
		Config:  cfg,
		Logger:  log,
		Version: Version,
	})
	if err != nil {
		log.Fatal().Err(err).Msg("Failed to create gateway")
	}

	// Start gateway
	if err := gw.Start(); err != nil {
		log.Fatal().Err(err).Msg("Failed to start gateway")
	}

	// Create HTTP server
	srv := &http.Server{
		Addr:         fmt.Sprintf("%s:%d", cfg.Server.Host, cfg.Server.Port),
		Handler:      gw.Handler(),
		ReadTimeout:  time.Duration(cfg.Server.RequestTimeout) * time.Second,
		WriteTimeout: time.Duration(cfg.Server.RequestTimeout) * time.Second,
		IdleTimeout:  time.Duration(cfg.Server.KeepaliveTimeout) * time.Second,
	}

	// Start server in goroutine
	go func() {
		log.Info().
			Str("address", srv.Addr).
			Msg("HTTP server starting")

		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			log.Fatal().Err(err).Msg("HTTP server error")
		}
	}()

	// Wait for interrupt signal
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)
	<-quit

	log.Info().Msg("Received shutdown signal")

	// Graceful shutdown
	ctx, cancel := context.WithTimeout(
		context.Background(),
		time.Duration(cfg.Server.GracefulShutdownTimeout)*time.Second,
	)
	defer cancel()

	// Shutdown HTTP server
	if err := srv.Shutdown(ctx); err != nil {
		log.Error().Err(err).Msg("HTTP server shutdown error")
	}

	// Stop gateway
	if err := gw.Stop(ctx); err != nil {
		log.Error().Err(err).Msg("Gateway shutdown error")
	}

	log.Info().Msg("API Gateway shutdown complete")
}
