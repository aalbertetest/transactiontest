// =============================================================================
// NEXUS PLATFORM - API GATEWAY - METRICS
// =============================================================================
// Prometheus metrics collection.
// =============================================================================

package metrics

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	// RequestsTotal counts total HTTP requests.
	RequestsTotal *prometheus.CounterVec

	// RequestDuration observes request duration.
	RequestDuration *prometheus.HistogramVec

	// RequestSize observes request size.
	RequestSize *prometheus.HistogramVec

	// ResponseSize observes response size.
	ResponseSize *prometheus.HistogramVec

	// ActiveRequests tracks currently active requests.
	ActiveRequests *prometheus.GaugeVec

	// ErrorsTotal counts total errors.
	ErrorsTotal *prometheus.CounterVec

	// UpstreamDuration observes upstream request duration.
	UpstreamDuration *prometheus.HistogramVec

	// CircuitBreakerState tracks circuit breaker states.
	CircuitBreakerState *prometheus.GaugeVec

	// RateLimitTotal counts rate limited requests.
	RateLimitTotal *prometheus.CounterVec

	// CacheHits counts cache hits.
	CacheHits *prometheus.CounterVec

	// CacheMisses counts cache misses.
	CacheMisses *prometheus.CounterVec
)

// Init initializes all metrics with the given prefix.
func Init(prefix string) {
	RequestsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: prefix + "_requests_total",
			Help: "Total number of HTTP requests",
		},
		[]string{"method", "path", "status", "service"},
	)

	RequestDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    prefix + "_request_duration_seconds",
			Help:    "HTTP request duration in seconds",
			Buckets: []float64{0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0},
		},
		[]string{"method", "path", "status"},
	)

	RequestSize = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    prefix + "_request_size_bytes",
			Help:    "HTTP request size in bytes",
			Buckets: []float64{100, 1000, 10000, 100000, 1000000},
		},
		[]string{"method", "path"},
	)

	ResponseSize = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    prefix + "_response_size_bytes",
			Help:    "HTTP response size in bytes",
			Buckets: []float64{100, 1000, 10000, 100000, 1000000},
		},
		[]string{"method", "path", "status"},
	)

	ActiveRequests = promauto.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: prefix + "_active_requests",
			Help: "Number of currently active requests",
		},
		[]string{"method"},
	)

	ErrorsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: prefix + "_errors_total",
			Help: "Total number of errors",
		},
		[]string{"type", "method", "path"},
	)

	UpstreamDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    prefix + "_upstream_duration_seconds",
			Help:    "Upstream service request duration in seconds",
			Buckets: []float64{0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0, 10.0, 30.0},
		},
		[]string{"service", "method", "status"},
	)

	CircuitBreakerState = promauto.NewGaugeVec(
		prometheus.GaugeOpts{
			Name: prefix + "_circuit_breaker_state",
			Help: "Circuit breaker state (0=closed, 1=half-open, 2=open)",
		},
		[]string{"service"},
	)

	RateLimitTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: prefix + "_rate_limit_total",
			Help: "Total number of rate-limited requests",
		},
		[]string{"policy", "method", "path"},
	)

	CacheHits = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: prefix + "_cache_hits_total",
			Help: "Total number of cache hits",
		},
		[]string{"path"},
	)

	CacheMisses = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: prefix + "_cache_misses_total",
			Help: "Total number of cache misses",
		},
		[]string{"path"},
	)
}

// RecordRequest records a request metric.
func RecordRequest(method, path, status, service string, duration float64) {
	if RequestsTotal != nil {
		RequestsTotal.WithLabelValues(method, path, status, service).Inc()
	}
	if RequestDuration != nil {
		RequestDuration.WithLabelValues(method, path, status).Observe(duration)
	}
}

// RecordUpstream records an upstream request metric.
func RecordUpstream(service, method, status string, duration float64) {
	if UpstreamDuration != nil {
		UpstreamDuration.WithLabelValues(service, method, status).Observe(duration)
	}
}

// RecordError records an error metric.
func RecordError(errorType, method, path string) {
	if ErrorsTotal != nil {
		ErrorsTotal.WithLabelValues(errorType, method, path).Inc()
	}
}

// RecordRateLimit records a rate limit event.
func RecordRateLimit(policy, method, path string) {
	if RateLimitTotal != nil {
		RateLimitTotal.WithLabelValues(policy, method, path).Inc()
	}
}

// SetCircuitBreakerState sets the circuit breaker state metric.
func SetCircuitBreakerState(service string, state int) {
	if CircuitBreakerState != nil {
		CircuitBreakerState.WithLabelValues(service).Set(float64(state))
	}
}

// RecordCacheHit records a cache hit.
func RecordCacheHit(path string) {
	if CacheHits != nil {
		CacheHits.WithLabelValues(path).Inc()
	}
}

// RecordCacheMiss records a cache miss.
func RecordCacheMiss(path string) {
	if CacheMisses != nil {
		CacheMisses.WithLabelValues(path).Inc()
	}
}
