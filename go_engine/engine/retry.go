package engine

import (
	"math"
	"math/rand"
)

func ComputeBackoffSeconds(attempt int, policy RetryPolicy) float64 {
	if attempt <= 0 {
		return policy.InitialIntervalSeconds
	}
	interval := policy.InitialIntervalSeconds * math.Pow(policy.BackoffCoefficient, float64(attempt-1))
	if interval > policy.MaxIntervalSeconds {
		interval = policy.MaxIntervalSeconds
	}
jitter := interval * 0.1
	return interval + rand.Float64()*2*jitter - jitter
}

func ShouldRetry(attempt int, policy RetryPolicy) bool {
	return attempt < policy.MaxAttempts
}
