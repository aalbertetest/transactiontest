"""
Prometheus Metrics Module
=========================

This module provides Prometheus-compatible metrics for monitoring the
distributed task scheduler. It exposes metrics for:

- Task operations (created, claimed, completed, failed, dead)
- Queue depth and latency
- Worker health and capacity
- Scheduler leadership and cron job execution

Metrics follow Prometheus naming conventions:
- Counter: dts_tasks_total (with labels)
- Gauge: dts_queue_depth
- Histogram: dts_task_duration_seconds

Usage:
    from metrics import MetricsCollector, setup_metrics
    
    # Initialize metrics
    metrics = setup_metrics(port=9090)
    
    # Record task creation
    metrics.task_created("send_email", "default")
    
    # Record task completion with duration
    metrics.task_completed("send_email", "default", duration=1.5)
    
    # Update queue depth gauge
    metrics.set_queue_depth("default", 42)
"""

import logging
from typing import Dict, Optional
from prometheus_client import (
    Counter, Gauge, Histogram, Info,
    start_http_server, REGISTRY, CollectorRegistry
)

from ..config.settings import MetricsSettings

logger = logging.getLogger(__name__)

# Default histogram buckets for task duration (in seconds)
# Covers sub-second to multi-minute tasks
DURATION_BUCKETS = (
    0.01, 0.025, 0.05, 0.075, 0.1,
    0.25, 0.5, 0.75, 1.0,
    2.5, 5.0, 7.5, 10.0,
    30.0, 60.0, 120.0, 300.0, 600.0
)


class MetricsCollector:
    """
    Prometheus metrics collector for the distributed task scheduler.
    
    This class wraps Prometheus metrics and provides a clean API for
    recording task scheduler operations. All metrics are prefixed with
    the configured namespace (default: 'dts').
    
    Metrics exposed:
    
    Counters:
        - {namespace}_tasks_total: Total tasks by operation, type, queue, status
        - {namespace}_cron_runs_total: Total cron job runs by job name, status
        - {namespace}_worker_events_total: Worker lifecycle events
    
    Gauges:
        - {namespace}_queue_depth: Current tasks in queue by queue name, status
        - {namespace}_active_workers: Number of active workers
        - {namespace}_scheduler_is_leader: Whether this instance is leader
    
    Histograms:
        - {namespace}_task_duration_seconds: Task execution duration
        - {namespace}_task_queue_time_seconds: Time spent waiting in queue
    
    Info:
        - {namespace}_scheduler_info: Scheduler instance information
        - {namespace}_worker_info: Worker instance information
    
    Attributes:
        namespace: Metric name prefix
        enabled: Whether metrics collection is enabled
    """
    
    def __init__(
        self,
        namespace: str = "dts",
        enabled: bool = True,
        registry: Optional[CollectorRegistry] = None
    ):
        """
        Initialize the metrics collector.
        
        Args:
            namespace: Prefix for all metric names.
            enabled: Whether to enable metrics collection.
            registry: Optional custom Prometheus registry.
        """
        self.namespace = namespace
        self.enabled = enabled
        self._registry = registry or REGISTRY
        
        if not enabled:
            logger.info("Metrics collection disabled")
            return
        
        # =====================================================================
        # TASK METRICS
        # =====================================================================
        
        # Task operations counter
        # Labels: operation (created, claimed, completed, failed, dead, cancelled)
        #         task_type, queue
        self.tasks_total = Counter(
            f'{namespace}_tasks_total',
            'Total number of task operations',
            ['operation', 'task_type', 'queue'],
            registry=self._registry
        )
        
        # Task execution duration histogram
        # Labels: task_type, queue, status (success, failure)
        self.task_duration = Histogram(
            f'{namespace}_task_duration_seconds',
            'Task execution duration in seconds',
            ['task_type', 'queue', 'status'],
            buckets=DURATION_BUCKETS,
            registry=self._registry
        )
        
        # Queue time histogram (time from creation to start)
        # Labels: task_type, queue
        self.task_queue_time = Histogram(
            f'{namespace}_task_queue_time_seconds',
            'Time spent waiting in queue',
            ['task_type', 'queue'],
            buckets=DURATION_BUCKETS,
            registry=self._registry
        )
        
        # Queue depth gauge
        # Labels: queue, status (queued, active, pending)
        self.queue_depth = Gauge(
            f'{namespace}_queue_depth',
            'Current number of tasks in queue',
            ['queue', 'status'],
            registry=self._registry
        )
        
        # =====================================================================
        # CRON JOB METRICS
        # =====================================================================
        
        # Cron job runs counter
        # Labels: job_name, status (triggered, skipped, failed)
        self.cron_runs = Counter(
            f'{namespace}_cron_runs_total',
            'Total number of cron job runs',
            ['job_name', 'status'],
            registry=self._registry
        )
        
        # Next cron run timestamp
        # Labels: job_name
        self.cron_next_run = Gauge(
            f'{namespace}_cron_next_run_timestamp',
            'Unix timestamp of next scheduled cron run',
            ['job_name'],
            registry=self._registry
        )
        
        # =====================================================================
        # SCHEDULER METRICS
        # =====================================================================
        
        # Leader status gauge
        self.is_leader = Gauge(
            f'{namespace}_scheduler_is_leader',
            'Whether this scheduler instance is the leader',
            registry=self._registry
        )
        
        # Scheduler info
        self.scheduler_info = Info(
            f'{namespace}_scheduler',
            'Scheduler instance information',
            registry=self._registry
        )
        
        # =====================================================================
        # WORKER METRICS
        # =====================================================================
        
        # Active workers gauge
        self.active_workers = Gauge(
            f'{namespace}_active_workers',
            'Number of active workers',
            registry=self._registry
        )
        
        # Worker capacity gauge
        # Labels: worker_id
        self.worker_capacity = Gauge(
            f'{namespace}_worker_capacity',
            'Worker task capacity (concurrency)',
            ['worker_id'],
            registry=self._registry
        )
        
        # Worker active tasks gauge
        # Labels: worker_id
        self.worker_active_tasks = Gauge(
            f'{namespace}_worker_active_tasks',
            'Number of tasks currently being processed by worker',
            ['worker_id'],
            registry=self._registry
        )
        
        # Worker events counter
        # Labels: event (registered, heartbeat, deregistered, timeout)
        self.worker_events = Counter(
            f'{namespace}_worker_events_total',
            'Total worker lifecycle events',
            ['event'],
            registry=self._registry
        )
        
        # Worker info
        self.worker_info = Info(
            f'{namespace}_worker',
            'Worker instance information',
            registry=self._registry
        )
        
        # =====================================================================
        # DATABASE METRICS
        # =====================================================================
        
        # Database connection pool gauge
        self.db_pool_size = Gauge(
            f'{namespace}_db_pool_size',
            'Database connection pool size',
            ['state'],  # idle, used
            registry=self._registry
        )
        
        # Database query duration
        self.db_query_duration = Histogram(
            f'{namespace}_db_query_duration_seconds',
            'Database query duration',
            ['operation'],  # claim, complete, fail, etc.
            buckets=(0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5),
            registry=self._registry
        )
        
        logger.info(f"Metrics collector initialized with namespace '{namespace}'")
    
    # =========================================================================
    # TASK METRIC METHODS
    # =========================================================================
    
    def task_created(self, task_type: str, queue: str) -> None:
        """Record a task creation."""
        if not self.enabled:
            return
        self.tasks_total.labels(
            operation='created',
            task_type=task_type,
            queue=queue
        ).inc()
    
    def task_claimed(self, task_type: str, queue: str) -> None:
        """Record a task being claimed by a worker."""
        if not self.enabled:
            return
        self.tasks_total.labels(
            operation='claimed',
            task_type=task_type,
            queue=queue
        ).inc()
    
    def task_completed(
        self,
        task_type: str,
        queue: str,
        duration: float,
        queue_time: Optional[float] = None
    ) -> None:
        """
        Record a task completion.
        
        Args:
            task_type: Task type identifier.
            queue: Queue name.
            duration: Execution duration in seconds.
            queue_time: Optional time spent waiting in queue.
        """
        if not self.enabled:
            return
        
        self.tasks_total.labels(
            operation='completed',
            task_type=task_type,
            queue=queue
        ).inc()
        
        self.task_duration.labels(
            task_type=task_type,
            queue=queue,
            status='success'
        ).observe(duration)
        
        if queue_time is not None:
            self.task_queue_time.labels(
                task_type=task_type,
                queue=queue
            ).observe(queue_time)
    
    def task_failed(
        self,
        task_type: str,
        queue: str,
        duration: float,
        will_retry: bool = False
    ) -> None:
        """
        Record a task failure.
        
        Args:
            task_type: Task type identifier.
            queue: Queue name.
            duration: Execution duration in seconds.
            will_retry: Whether the task will be retried.
        """
        if not self.enabled:
            return
        
        operation = 'failed' if will_retry else 'dead'
        self.tasks_total.labels(
            operation=operation,
            task_type=task_type,
            queue=queue
        ).inc()
        
        self.task_duration.labels(
            task_type=task_type,
            queue=queue,
            status='failure'
        ).observe(duration)
    
    def task_cancelled(self, task_type: str, queue: str) -> None:
        """Record a task cancellation."""
        if not self.enabled:
            return
        self.tasks_total.labels(
            operation='cancelled',
            task_type=task_type,
            queue=queue
        ).inc()
    
    def set_queue_depth(self, queue: str, status: str, count: int) -> None:
        """
        Update queue depth gauge.
        
        Args:
            queue: Queue name.
            status: Task status (queued, active, pending).
            count: Number of tasks.
        """
        if not self.enabled:
            return
        self.queue_depth.labels(queue=queue, status=status).set(count)
    
    # =========================================================================
    # CRON JOB METRIC METHODS
    # =========================================================================
    
    def cron_triggered(self, job_name: str) -> None:
        """Record a cron job trigger."""
        if not self.enabled:
            return
        self.cron_runs.labels(job_name=job_name, status='triggered').inc()
    
    def cron_skipped(self, job_name: str) -> None:
        """Record a cron job skip (due to concurrency policy)."""
        if not self.enabled:
            return
        self.cron_runs.labels(job_name=job_name, status='skipped').inc()
    
    def cron_failed(self, job_name: str) -> None:
        """Record a cron job failure."""
        if not self.enabled:
            return
        self.cron_runs.labels(job_name=job_name, status='failed').inc()
    
    def set_cron_next_run(self, job_name: str, timestamp: float) -> None:
        """Set the next run timestamp for a cron job."""
        if not self.enabled:
            return
        self.cron_next_run.labels(job_name=job_name).set(timestamp)
    
    # =========================================================================
    # SCHEDULER METRIC METHODS
    # =========================================================================
    
    def set_leader_status(self, is_leader: bool) -> None:
        """Update leader status gauge."""
        if not self.enabled:
            return
        self.is_leader.set(1 if is_leader else 0)
    
    def set_scheduler_info(
        self,
        instance_id: str,
        instance_name: str,
        version: str
    ) -> None:
        """Set scheduler instance information."""
        if not self.enabled:
            return
        self.scheduler_info.info({
            'instance_id': instance_id,
            'instance_name': instance_name,
            'version': version,
        })
    
    # =========================================================================
    # WORKER METRIC METHODS
    # =========================================================================
    
    def set_active_workers(self, count: int) -> None:
        """Update active workers gauge."""
        if not self.enabled:
            return
        self.active_workers.set(count)
    
    def worker_registered(self, worker_id: str) -> None:
        """Record a worker registration."""
        if not self.enabled:
            return
        self.worker_events.labels(event='registered').inc()
    
    def worker_heartbeat(self) -> None:
        """Record a worker heartbeat."""
        if not self.enabled:
            return
        self.worker_events.labels(event='heartbeat').inc()
    
    def worker_deregistered(self, worker_id: str) -> None:
        """Record a worker deregistration."""
        if not self.enabled:
            return
        self.worker_events.labels(event='deregistered').inc()
    
    def worker_timeout(self, worker_id: str) -> None:
        """Record a worker timeout."""
        if not self.enabled:
            return
        self.worker_events.labels(event='timeout').inc()
    
    def set_worker_capacity(self, worker_id: str, capacity: int) -> None:
        """Set worker capacity."""
        if not self.enabled:
            return
        self.worker_capacity.labels(worker_id=worker_id).set(capacity)
    
    def set_worker_active_tasks(self, worker_id: str, count: int) -> None:
        """Set worker active task count."""
        if not self.enabled:
            return
        self.worker_active_tasks.labels(worker_id=worker_id).set(count)
    
    def set_worker_info(
        self,
        worker_id: str,
        worker_name: str,
        queues: str,
        version: str
    ) -> None:
        """Set worker instance information."""
        if not self.enabled:
            return
        self.worker_info.info({
            'worker_id': worker_id,
            'worker_name': worker_name,
            'queues': queues,
            'version': version,
        })
    
    # =========================================================================
    # DATABASE METRIC METHODS
    # =========================================================================
    
    def set_db_pool_stats(self, idle: int, used: int) -> None:
        """Update database pool statistics."""
        if not self.enabled:
            return
        self.db_pool_size.labels(state='idle').set(idle)
        self.db_pool_size.labels(state='used').set(used)
    
    def observe_db_query(self, operation: str, duration: float) -> None:
        """Record a database query duration."""
        if not self.enabled:
            return
        self.db_query_duration.labels(operation=operation).observe(duration)


# Global metrics instance
_metrics: Optional[MetricsCollector] = None


def setup_metrics(
    settings: Optional[MetricsSettings] = None,
    port: int = 9090,
    path: str = "/metrics",
    namespace: str = "dts",
    start_server: bool = True
) -> MetricsCollector:
    """
    Set up and optionally start the metrics server.
    
    Args:
        settings: Optional MetricsSettings (overrides other params).
        port: Port to expose metrics on.
        path: URL path for metrics endpoint.
        namespace: Metric name prefix.
        start_server: Whether to start the HTTP server.
        
    Returns:
        Configured MetricsCollector instance.
    """
    global _metrics
    
    if settings:
        enabled = settings.enabled
        port = settings.port
        namespace = settings.namespace
    else:
        enabled = True
    
    _metrics = MetricsCollector(namespace=namespace, enabled=enabled)
    
    if enabled and start_server:
        try:
            start_http_server(port)
            logger.info(f"Metrics server started on port {port}")
        except Exception as e:
            logger.error(f"Failed to start metrics server: {e}")
    
    return _metrics


def get_metrics() -> Optional[MetricsCollector]:
    """Get the global metrics collector instance."""
    return _metrics
