from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class Counter:
    name: str
    value: int = 0


@dataclass
class Gauge:
    name: str
    value: float = 0.0


@dataclass
class Histogram:
    name: str
    observations: List[float]

    def observe(self, value: float) -> None:
        self.observations.append(value)

    def snapshot(self) -> Dict[str, float]:
        if not self.observations:
            return {"count": 0, "min": 0.0, "max": 0.0, "avg": 0.0}
        return {
            "count": len(self.observations),
            "min": min(self.observations),
            "max": max(self.observations),
            "avg": sum(self.observations) / len(self.observations),
        }


class MetricsRegistry:
    """
    A minimal in-process metrics registry. This is intentionally simple so it can
    be embedded without external dependencies.
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._counters: Dict[str, Counter] = {}
        self._gauges: Dict[str, Gauge] = {}
        self._histograms: Dict[str, Histogram] = {}

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

    def histogram(self, name: str) -> Histogram:
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = Histogram(name=name, observations=[])
            return self._histograms[name]

    def increment(self, name: str, delta: int = 1) -> None:
        with self._lock:
            counter = self.counter(name)
            counter.value += delta

    def set_gauge(self, name: str, value: float) -> None:
        with self._lock:
            gauge = self.gauge(name)
            gauge.value = value

    def observe(self, name: str, value: float) -> None:
        with self._lock:
            histogram = self.histogram(name)
            histogram.observe(value)

    def snapshot(self) -> Dict[str, Dict[str, float]]:
        with self._lock:
            counters = {name: counter.value for name, counter in self._counters.items()}
            gauges = {name: gauge.value for name, gauge in self._gauges.items()}
            histograms = {
                name: histogram.snapshot() for name, histogram in self._histograms.items()
            }
        return {
            "timestamp": time.time(),
            "counters": counters,
            "gauges": gauges,
            "histograms": histograms,
        }

