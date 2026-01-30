"""
Simple in-memory metrics registry.
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Dict, Tuple


LabelKey = Tuple[Tuple[str, str], ...]


def _normalize_labels(labels: Dict[str, str] | None) -> LabelKey:
    if not labels:
        return ()
    return tuple(sorted((str(k), str(v)) for k, v in labels.items()))


@dataclass
class Counter:
    name: str
    _values: Dict[LabelKey, float]
    _lock: threading.Lock

    def inc(self, value: float = 1.0, labels: Dict[str, str] | None = None) -> None:
        key = _normalize_labels(labels)
        with self._lock:
            self._values[key] = self._values.get(key, 0.0) + value

    def snapshot(self) -> Dict[LabelKey, float]:
        with self._lock:
            return dict(self._values)


@dataclass
class Histogram:
    name: str
    _counts: Dict[LabelKey, int]
    _sums: Dict[LabelKey, float]
    _lock: threading.Lock

    def observe(self, value: float, labels: Dict[str, str] | None = None) -> None:
        key = _normalize_labels(labels)
        with self._lock:
            self._counts[key] = self._counts.get(key, 0) + 1
            self._sums[key] = self._sums.get(key, 0.0) + value

    def snapshot(self) -> Dict[LabelKey, Dict[str, float]]:
        with self._lock:
            return {
                key: {"count": float(self._counts.get(key, 0)), "sum": self._sums.get(key, 0.0)}
                for key in set(self._counts) | set(self._sums)
            }


class MetricsRegistry:
    def __init__(self) -> None:
        self._counters: Dict[str, Counter] = {}
        self._histograms: Dict[str, Histogram] = {}
        self._lock = threading.Lock()

    def counter(self, name: str) -> Counter:
        with self._lock:
            if name not in self._counters:
                self._counters[name] = Counter(name=name, _values={}, _lock=threading.Lock())
            return self._counters[name]

    def histogram(self, name: str) -> Histogram:
        with self._lock:
            if name not in self._histograms:
                self._histograms[name] = Histogram(name=name, _counts={}, _sums={}, _lock=threading.Lock())
            return self._histograms[name]

    def timer(self, name: str, labels: Dict[str, str] | None = None):
        histogram = self.histogram(name)

        class _Timer:
            def __enter__(self_inner):
                self_inner.start = time.time()
                return self_inner

            def __exit__(self_inner, exc_type, exc, tb):
                duration = time.time() - self_inner.start
                histogram.observe(duration, labels=labels)
                return False

        return _Timer()

    def snapshot(self) -> Dict[str, Dict]:
        return {
            "counters": {name: counter.snapshot() for name, counter in self._counters.items()},
            "histograms": {name: hist.snapshot() for name, hist in self._histograms.items()},
        }
