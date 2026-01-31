// Package metrics provides Prometheus-compatible metrics for the distributed task scheduler.
//
// Metrics exposed:
//   - Task operations (created, claimed, completed, failed)
//   - Queue depth and latency
//   - Worker health and capacity
//   - Scheduler leadership
package metrics

import (
	"fmt"
	"net/http"
	"sync"

	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"github.com/rs/zerolog/log"
)

// Metrics contains all Prometheus metrics.
type Metrics struct {
	// Task metrics
	TasksTotal        *prometheus.CounterVec
	TaskDuration      *prometheus.HistogramVec
	TaskQueueTime     *prometheus.HistogramVec
	QueueDepth        *prometheus.GaugeVec

	// Cron job metrics
	CronRunsTotal     *prometheus.CounterVec
	CronNextRun       *prometheus.GaugeVec

	// Scheduler metrics
	SchedulerIsLeader prometheus.Gauge

	// Worker metrics
	ActiveWorkers     prometheus.Gauge
	WorkerCapacity    *prometheus.GaugeVec
	WorkerActiveTasks *prometheus.GaugeVec
	WorkerEvents      *prometheus.CounterVec

	// Database metrics
	DBPoolSize        *prometheus.GaugeVec
	DBQueryDuration   *prometheus.HistogramVec

	namespace string
	enabled   bool
}

var (
	globalMetrics *Metrics
	once          sync.Once
)

// durationBuckets defines histogram buckets for task duration.
var durationBuckets = []float64{
	0.01, 0.025, 0.05, 0.075, 0.1,
	0.25, 0.5, 0.75, 1.0,
	2.5, 5.0, 7.5, 10.0,
	30.0, 60.0, 120.0, 300.0, 600.0,
}

// NewMetrics creates a new Metrics instance.
func NewMetrics(namespace string, enabled bool) *Metrics {
	if !enabled {
		return &Metrics{enabled: false}
	}

	m := &Metrics{
		namespace: namespace,
		enabled:   true,

		// Task metrics
		TasksTotal: promauto.NewCounterVec(
			prometheus.CounterOpts{
				Namespace: namespace,
				Name:      "tasks_total",
				Help:      "Total number of task operations",
			},
			[]string{"operation", "task_type", "queue"},
		),

		TaskDuration: promauto.NewHistogramVec(
			prometheus.HistogramOpts{
				Namespace: namespace,
				Name:      "task_duration_seconds",
				Help:      "Task execution duration in seconds",
				Buckets:   durationBuckets,
			},
			[]string{"task_type", "queue", "status"},
		),

		TaskQueueTime: promauto.NewHistogramVec(
			prometheus.HistogramOpts{
				Namespace: namespace,
				Name:      "task_queue_time_seconds",
				Help:      "Time spent waiting in queue",
				Buckets:   durationBuckets,
			},
			[]string{"task_type", "queue"},
		),

		QueueDepth: promauto.NewGaugeVec(
			prometheus.GaugeOpts{
				Namespace: namespace,
				Name:      "queue_depth",
				Help:      "Current number of tasks in queue",
			},
			[]string{"queue", "status"},
		),

		// Cron job metrics
		CronRunsTotal: promauto.NewCounterVec(
			prometheus.CounterOpts{
				Namespace: namespace,
				Name:      "cron_runs_total",
				Help:      "Total number of cron job runs",
			},
			[]string{"job_name", "status"},
		),

		CronNextRun: promauto.NewGaugeVec(
			prometheus.GaugeOpts{
				Namespace: namespace,
				Name:      "cron_next_run_timestamp",
				Help:      "Unix timestamp of next scheduled cron run",
			},
			[]string{"job_name"},
		),

		// Scheduler metrics
		SchedulerIsLeader: promauto.NewGauge(
			prometheus.GaugeOpts{
				Namespace: namespace,
				Name:      "scheduler_is_leader",
				Help:      "Whether this scheduler instance is the leader",
			},
		),

		// Worker metrics
		ActiveWorkers: promauto.NewGauge(
			prometheus.GaugeOpts{
				Namespace: namespace,
				Name:      "active_workers",
				Help:      "Number of active workers",
			},
		),

		WorkerCapacity: promauto.NewGaugeVec(
			prometheus.GaugeOpts{
				Namespace: namespace,
				Name:      "worker_capacity",
				Help:      "Worker task capacity (concurrency)",
			},
			[]string{"worker_id"},
		),

		WorkerActiveTasks: promauto.NewGaugeVec(
			prometheus.GaugeOpts{
				Namespace: namespace,
				Name:      "worker_active_tasks",
				Help:      "Number of tasks currently being processed by worker",
			},
			[]string{"worker_id"},
		),

		WorkerEvents: promauto.NewCounterVec(
			prometheus.CounterOpts{
				Namespace: namespace,
				Name:      "worker_events_total",
				Help:      "Total worker lifecycle events",
			},
			[]string{"event"},
		),

		// Database metrics
		DBPoolSize: promauto.NewGaugeVec(
			prometheus.GaugeOpts{
				Namespace: namespace,
				Name:      "db_pool_size",
				Help:      "Database connection pool size",
			},
			[]string{"state"},
		),

		DBQueryDuration: promauto.NewHistogramVec(
			prometheus.HistogramOpts{
				Namespace: namespace,
				Name:      "db_query_duration_seconds",
				Help:      "Database query duration",
				Buckets:   []float64{0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5},
			},
			[]string{"operation"},
		),
	}

	return m
}

// Setup initializes global metrics and optionally starts the HTTP server.
func Setup(namespace string, enabled bool, port int, startServer bool) *Metrics {
	once.Do(func() {
		globalMetrics = NewMetrics(namespace, enabled)

		if enabled && startServer {
			go func() {
				addr := fmt.Sprintf(":%d", port)
				http.Handle("/metrics", promhttp.Handler())
				log.Info().Int("port", port).Msg("Starting metrics server")
				if err := http.ListenAndServe(addr, nil); err != nil {
					log.Error().Err(err).Msg("Metrics server error")
				}
			}()
		}
	})

	return globalMetrics
}

// Get returns the global metrics instance.
func Get() *Metrics {
	return globalMetrics
}

// ============================================================================
// TASK METRICS
// ============================================================================

// TaskCreated records a task creation.
func (m *Metrics) TaskCreated(taskType, queue string) {
	if !m.enabled {
		return
	}
	m.TasksTotal.WithLabelValues("created", taskType, queue).Inc()
}

// TaskClaimed records a task being claimed.
func (m *Metrics) TaskClaimed(taskType, queue string) {
	if !m.enabled {
		return
	}
	m.TasksTotal.WithLabelValues("claimed", taskType, queue).Inc()
}

// TaskCompleted records a task completion.
func (m *Metrics) TaskCompleted(taskType, queue string, duration float64) {
	if !m.enabled {
		return
	}
	m.TasksTotal.WithLabelValues("completed", taskType, queue).Inc()
	m.TaskDuration.WithLabelValues(taskType, queue, "success").Observe(duration)
}

// TaskFailed records a task failure.
func (m *Metrics) TaskFailed(taskType, queue string, duration float64, willRetry bool) {
	if !m.enabled {
		return
	}
	operation := "dead"
	if willRetry {
		operation = "failed"
	}
	m.TasksTotal.WithLabelValues(operation, taskType, queue).Inc()
	m.TaskDuration.WithLabelValues(taskType, queue, "failure").Observe(duration)
}

// TaskCancelled records a task cancellation.
func (m *Metrics) TaskCancelled(taskType, queue string) {
	if !m.enabled {
		return
	}
	m.TasksTotal.WithLabelValues("cancelled", taskType, queue).Inc()
}

// SetQueueDepth updates the queue depth gauge.
func (m *Metrics) SetQueueDepth(queue, status string, count float64) {
	if !m.enabled {
		return
	}
	m.QueueDepth.WithLabelValues(queue, status).Set(count)
}

// ============================================================================
// CRON JOB METRICS
// ============================================================================

// CronTriggered records a cron job trigger.
func (m *Metrics) CronTriggered(jobName string) {
	if !m.enabled {
		return
	}
	m.CronRunsTotal.WithLabelValues(jobName, "triggered").Inc()
}

// CronSkipped records a cron job skip.
func (m *Metrics) CronSkipped(jobName string) {
	if !m.enabled {
		return
	}
	m.CronRunsTotal.WithLabelValues(jobName, "skipped").Inc()
}

// CronFailed records a cron job failure.
func (m *Metrics) CronFailed(jobName string) {
	if !m.enabled {
		return
	}
	m.CronRunsTotal.WithLabelValues(jobName, "failed").Inc()
}

// SetCronNextRun sets the next run timestamp for a cron job.
func (m *Metrics) SetCronNextRun(jobName string, timestamp float64) {
	if !m.enabled {
		return
	}
	m.CronNextRun.WithLabelValues(jobName).Set(timestamp)
}

// ============================================================================
// SCHEDULER METRICS
// ============================================================================

// SetLeaderStatus updates the leader status gauge.
func (m *Metrics) SetLeaderStatus(isLeader bool) {
	if !m.enabled {
		return
	}
	val := float64(0)
	if isLeader {
		val = 1
	}
	m.SchedulerIsLeader.Set(val)
}

// ============================================================================
// WORKER METRICS
// ============================================================================

// SetActiveWorkers updates the active workers gauge.
func (m *Metrics) SetActiveWorkers(count float64) {
	if !m.enabled {
		return
	}
	m.ActiveWorkers.Set(count)
}

// WorkerRegistered records a worker registration.
func (m *Metrics) WorkerRegistered() {
	if !m.enabled {
		return
	}
	m.WorkerEvents.WithLabelValues("registered").Inc()
}

// WorkerHeartbeat records a worker heartbeat.
func (m *Metrics) WorkerHeartbeat() {
	if !m.enabled {
		return
	}
	m.WorkerEvents.WithLabelValues("heartbeat").Inc()
}

// WorkerDeregistered records a worker deregistration.
func (m *Metrics) WorkerDeregistered() {
	if !m.enabled {
		return
	}
	m.WorkerEvents.WithLabelValues("deregistered").Inc()
}

// WorkerTimeout records a worker timeout.
func (m *Metrics) WorkerTimeout() {
	if !m.enabled {
		return
	}
	m.WorkerEvents.WithLabelValues("timeout").Inc()
}

// SetWorkerCapacity sets worker capacity.
func (m *Metrics) SetWorkerCapacity(workerID string, capacity float64) {
	if !m.enabled {
		return
	}
	m.WorkerCapacity.WithLabelValues(workerID).Set(capacity)
}

// SetWorkerActiveTasks sets worker active task count.
func (m *Metrics) SetWorkerActiveTasks(workerID string, count float64) {
	if !m.enabled {
		return
	}
	m.WorkerActiveTasks.WithLabelValues(workerID).Set(count)
}

// ============================================================================
// DATABASE METRICS
// ============================================================================

// SetDBPoolStats updates database pool statistics.
func (m *Metrics) SetDBPoolStats(idle, used float64) {
	if !m.enabled {
		return
	}
	m.DBPoolSize.WithLabelValues("idle").Set(idle)
	m.DBPoolSize.WithLabelValues("used").Set(used)
}

// ObserveDBQuery records a database query duration.
func (m *Metrics) ObserveDBQuery(operation string, duration float64) {
	if !m.enabled {
		return
	}
	m.DBQueryDuration.WithLabelValues(operation).Observe(duration)
}
