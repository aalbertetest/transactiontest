package main

import (
	"os"
	"time"

	"payment-processing/internal/store"
	"payment-processing/internal/worker"
)

func main() {
	w := worker.Worker{
		Store:         store.Store,
		WebhookSecret: getenv("WEBHOOK_SIGNING_SECRET", "whsec_test_123"),
		MaxAttempts:   5,
		BaseBackoff:   200 * time.Millisecond,
		PollInterval:  500 * time.Millisecond,
	}
	w.Run()
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}
