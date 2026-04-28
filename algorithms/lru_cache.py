"""LRU cache using OrderedDict (hash map + doubly-linked order)."""

from __future__ import annotations

from collections import OrderedDict
from typing import Generic, Hashable, Iterator, Optional, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """
    Least-recently-used eviction when capacity is exceeded.

    * get/put O(1) average time; space O(capacity).
    * Optional TTL: entries older than ttl_seconds are treated as missing on access.
    """

    def __init__(self, capacity: int, ttl_seconds: Optional[float] = None) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._ttl = ttl_seconds
        self._data: "OrderedDict[K, tuple[V, Optional[float]]]" = OrderedDict()

    def __len__(self) -> int:
        return len(self._data)

    def _now(self) -> Optional[float]:
        if self._ttl is None:
            return None
        import time

        return time.monotonic()

    def _expired(self, ts: Optional[float]) -> bool:
        if self._ttl is None or ts is None:
            return False
        import time

        return time.monotonic() - ts > self._ttl

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        if key not in self._data:
            return default
        val, ts = self._data[key]
        if self._expired(ts):
            del self._data[key]
            return default
        self._data.move_to_end(key, last=True)
        return val

    def __getitem__(self, key: K) -> V:
        if key not in self._data:
            raise KeyError(key)
        val, ts = self._data[key]
        if self._expired(ts):
            del self._data[key]
            raise KeyError(key)
        self._data.move_to_end(key, last=True)
        return val

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def put(self, key: K, value: V) -> None:
        now = self._now()
        if key in self._data:
            self._data.move_to_end(key, last=True)
        self._data[key] = (value, now)
        if len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def __delitem__(self, key: K) -> None:
        if key not in self._data:
            raise KeyError(key)
        del self._data[key]

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, Hashable):
            return False
        try:
            k = key  # type: ignore[assignment]
            if k not in self._data:
                return False
            _, ts = self._data[k]
            if self._expired(ts):
                del self._data[k]
                return False
            return True
        except TypeError:
            return False

    def items(self) -> Iterator[tuple[K, V]]:
        for k, (v, ts) in list(self._data.items()):
            if not self._expired(ts):
                yield k, v
