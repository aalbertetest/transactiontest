"""
Minimal metrics implementation with counters, gauges, and histograms.

This is intentionally simple but thread-safe and production-usable for small deployments.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class Counter:
    name: str
    value: int = 0
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def inc(self, amount: int = 1) -> None:
        with self._lock:
            self.value += amount


@dataclass
class Gauge:
    name: str
    value: float = 0.0
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def set(self, value: float) -> None:
        with self._lock:
            self.value = value


@dataclass
class Histogram:
    name: str
    buckets: List[float]
    counts: List[int] = field(init=False)
    _lock: threading.Lock = field(default_factory=threading.Lock, init=False)

    def __post_init__(self) -> None:
        self.counts = [0 for _ in self.buckets]

    def observe(self, value: float) -> None:
        with self._lock:
            for idx, bucket in enumerate(self.buckets):
                if value <= bucket:
                    self.counts[idx] += 1
                    return
            # If value is above all buckets, count in the last bucket.
            self.counts[-1] += 1


class MetricsRegistry:
    """
    Thread-safe registry for metrics.
    """

    def __init__(self) -> None:
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._lock = threading.Lock()

    def counter(self, name: str) -> Counter:
        with self._lock:
            if name not in self._counters:
                self._counters[name] = Counter(name=name)
            return self._counters[name]

    def gauge(self, name: str) -> Gauge:
        with self._lock:
            if name not in self._gauges:
                self._gauges[name] = Gauge(name=name)
            return self._gauges[name]

    def histogram(self, name: str, buckets: List[float]) -> Histogram:
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = Histogram(name=name, buckets=buckets)
            return self._histograms[name]
