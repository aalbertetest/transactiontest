package main

import (
	"time"

	"github.com/cursor/platform/lib/go/pkg/logger"
	"github.com/robfig/cron/v3"
	"go.uber.org/zap"
)

func main() {
	logger.Init("info", "json")

	c := cron.New()

	// Add daily cleanup job
	c.AddFunc("@daily", func() {
		logger.Info("Running daily cleanup")
		// In reality, this would push a message to NATS or call an API
	})

	// Add hourly stats rollup
	c.AddFunc("@hourly", func() {
		logger.Info("Running hourly stats rollup")
	})

	// Start cron
	c.Start()
	logger.Info("Scheduler started")

	// Keep running
	select {}
}
