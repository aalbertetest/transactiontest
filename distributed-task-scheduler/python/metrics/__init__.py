"""Metrics and observability module."""

from .prometheus import MetricsCollector, setup_metrics

__all__ = ["MetricsCollector", "setup_metrics"]
