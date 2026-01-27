package metrics

import (
	"net/http"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
)

type Metrics struct {
	Registry *prometheus.Registry

	HTTPRequestsTotal        *prometheus.CounterVec
	HTTPRequestDurationSeconds *prometheus.HistogramVec
}

func New(service string) *Metrics {
	reg := prometheus.NewRegistry()

	// Default Go + process metrics.
	reg.MustRegister(
		prometheus.NewProcessCollector(prometheus.ProcessCollectorOpts{}),
		prometheus.NewGoCollector(),
	)

	reqs := promauto.With(reg).NewCounterVec(prometheus.CounterOpts{
		Name: "http_requests_total",
		Help: "Total HTTP requests",
		ConstLabels: map[string]string{
			"service": service,
		},
	}, []string{"method", "route", "status"})

	dur := promauto.With(reg).NewHistogramVec(prometheus.HistogramOpts{
		Name: "http_request_duration_seconds",
		Help: "HTTP request duration in seconds",
		ConstLabels: map[string]string{
			"service": service,
		},
		Buckets: []float64{0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5, 10},
	}, []string{"method", "route", "status"})

	return &Metrics{
		Registry: reg,
		HTTPRequestsTotal: reqs,
		HTTPRequestDurationSeconds: dur,
	}
}

func Handler(reg *prometheus.Registry) http.Handler {
	return promhttp.HandlerFor(reg, promhttp.HandlerOpts{})
}

