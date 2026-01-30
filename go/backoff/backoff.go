package backoff

import (
	"math"
	"math/rand"
)

// Compute returns exponential backoff with jitter.
func Compute(attempt int, initialSeconds float64, maxSeconds float64, jitter float64) float64 {
	if attempt < 1 {
		attempt = 1
	}
	exp := math.Min(maxSeconds, initialSeconds*math.Pow(2, float64(attempt-1)))
	if jitter <= 0 {
		return exp
	}
	delta := exp * jitter
	return math.Max(0, exp+(rand.Float64()*2*delta-delta))
}
