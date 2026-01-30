package engine

import "math"

// ComputeBackoffSeconds calculates exponential backoff duration for attempts.
// attempt is 1-based.
func ComputeBackoffSeconds(policy RetryPolicy, attempt int) int {
	if attempt <= 0 {
		return policy.InitialIntervalSeconds
	}
	interval := float64(policy.InitialIntervalSeconds) * math.Pow(policy.BackoffCoefficient, float64(attempt-1))
	if interval > float64(policy.MaxIntervalSeconds) {
		interval = float64(policy.MaxIntervalSeconds)
	}
	return int(math.Ceil(interval))
}
