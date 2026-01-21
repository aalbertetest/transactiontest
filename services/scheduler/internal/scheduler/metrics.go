package scheduler

import "github.com/prometheus/client_golang/prometheus"

var (
	SchedulerLoopDuration = prometheus.NewHistogram(prometheus.HistogramOpts{
		Name:    "scheduler_loop_duration_seconds",
		Help:    "Duration of scheduling loop.",
		Buckets: []float64{0.05, 0.1, 0.25, 0.5, 1, 2, 5},
	})
	SchedulerRunsProcessed = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "scheduler_runs_processed_total",
		Help: "Total number of workflow runs processed by scheduler.",
	})
	SchedulerTasksScheduled = prometheus.NewCounter(prometheus.CounterOpts{
		Name: "scheduler_tasks_scheduled_total",
		Help: "Total number of tasks scheduled by scheduler.",
	})
)

func RegisterMetrics() {
	prometheus.MustRegister(SchedulerLoopDuration, SchedulerRunsProcessed, SchedulerTasksScheduled)
}
