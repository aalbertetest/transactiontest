"""LFU cache: evict least frequently used; ties broken by least recently used among that frequency."""

from __future__ import annotations

from collections import OrderedDict, defaultdict
from typing import DefaultDict, Dict, Generic, Hashable, Iterator, Optional, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LFUCache(Generic[K, V]):
    """
    O(1) get and put (amortized): frequency buckets of LRU lists + key metadata.

    * Space O(capacity).
    * Evicts key with smallest frequency; among equal frequency, oldest by insertion order in that bucket.
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._capacity = capacity
        self._min_freq = 0
        self._values: Dict[K, V] = {}
        self._freq: Dict[K, int] = {}
        self._buckets: DefaultDict[int, "OrderedDict[K, None]"] = defaultdict(OrderedDict)

    def __len__(self) -> int:
        return len(self._values)

    def _touch(self, key: K) -> None:
        f = self._freq[key]
        self._buckets[f].pop(key)
        if not self._buckets[f]:
            del self._buckets[f]
            if f == self._min_freq:
                self._min_freq += 1
        self._freq[key] = f + 1
        self._buckets[f + 1][key] = None

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        if key not in self._values:
            return default
        self._touch(key)
        return self._values[key]

    def __getitem__(self, key: K) -> V:
        if key not in self._values:
            raise KeyError(key)
        self._touch(key)
        return self._values[key]

    def put(self, key: K, value: V) -> None:
        if key in self._values:
            self._values[key] = value
            self._touch(key)
            return
        if len(self._values) >= self._capacity:
            evict_key, _ = self._buckets[self._min_freq].popitem(last=False)
            del self._values[evict_key]
            del self._freq[evict_key]
        self._values[key] = value
        self._freq[key] = 1
        self._buckets[1][key] = None
        self._min_freq = 1

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def __delitem__(self, key: K) -> None:
        if key not in self._values:
            raise KeyError(key)
        f = self._freq.pop(key)
        del self._values[key]
        self._buckets[f].pop(key)
        if not self._buckets[f]:
            del self._buckets[f]
        if not self._values:
            self._min_freq = 0
        elif f == self._min_freq and self._min_freq not in self._buckets:
            self._min_freq = min(self._buckets.keys())

    def __contains__(self, key: object) -> bool:
        if not isinstance(key, Hashable):
            return False
        return key in self._values  # type: ignore[operator]

    def items(self) -> Iterator[tuple[K, V]]:
        yield from self._values.items()
