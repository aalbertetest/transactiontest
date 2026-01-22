package retry

import (
	"math/rand"
	"time"
)

func WithRetries(operation func() (string, error), maxAttempts int, baseBackoff time.Duration, retryable func(error) bool) (string, error) {
	var lastErr error
	for attempt := 1; attempt <= maxAttempts; attempt++ {
		value, err := operation()
		if err == nil {
			return value, nil
		}
		lastErr = err
		if !retryable(err) || attempt == maxAttempts {
			break
		}
		sleep := baseBackoff * time.Duration(1<<(attempt-1))
		jitter := time.Duration(rand.Intn(int(baseBackoff/5) + 1))
		time.Sleep(sleep + jitter)
	}
	return "", lastErr
}
