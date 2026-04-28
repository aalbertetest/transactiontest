"""LRU cache: evict least-recently-used when over capacity."""

from __future__ import annotations

from collections import OrderedDict
from typing import Generic, Hashable, Optional, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """
    Least-recently-used eviction.

    Get/set touch order. Time O(1) amortized per operation (OrderedDict). Space O(capacity).
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._cap = capacity
        self._data: OrderedDict[K, V] = OrderedDict()

    @property
    def capacity(self) -> int:
        return self._cap

    def __len__(self) -> int:
        return len(self._data)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        if key not in self._data:
            return default
        self._data.move_to_end(key)
        return self._data[key]

    def __getitem__(self, key: K) -> V:
        if key not in self._data:
            raise KeyError(key)
        self._data.move_to_end(key)
        return self._data[key]

    def __setitem__(self, key: K, value: V) -> None:
        if key in self._data:
            self._data.move_to_end(key)
            self._data[key] = value
            return
        self._data[key] = value
        if len(self._data) > self._cap:
            self._data.popitem(last=False)

    def __delitem__(self, key: K) -> None:
        del self._data[key]

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def peek(self, key: K, default: Optional[V] = None) -> Optional[V]:
        """Read without marking as recently used."""
        return self._data.get(key, default)
