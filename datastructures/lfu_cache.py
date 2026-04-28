"""LFU cache: evict least-frequently-used; ties broken by LRU (FIFO within same count)."""

from __future__ import annotations

from collections import OrderedDict, defaultdict
from typing import DefaultDict, Dict, Generic, Hashable, Optional, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LFUCache(Generic[K, V]):
    """
    Least-frequently-used cache.

    Time O(1) average for get/set (OrderedDict per frequency level). Space O(capacity).

    `min_freq` tracks the smallest frequency present; eviction removes the oldest key
    among keys at `min_freq` (LRU tie-break).
    """

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._cap = capacity
        self._values: Dict[K, V] = {}
        self._key_freq: Dict[K, int] = {}
        self._freq_keys: DefaultDict[int, OrderedDict[K, None]] = defaultdict(OrderedDict)
        self._min_freq = 0

    @property
    def capacity(self) -> int:
        return self._cap

    def __len__(self) -> int:
        return len(self._values)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        if key not in self._values:
            return default
        self._bump(key)
        return self._values[key]

    def __getitem__(self, key: K) -> V:
        if key not in self._values:
            raise KeyError(key)
        self._bump(key)
        return self._values[key]

    def __setitem__(self, key: K, value: V) -> None:
        if key in self._values:
            self._values[key] = value
            self._bump(key)
            return
        if len(self._values) >= self._cap:
            self._evict_one()
        self._values[key] = value
        self._key_freq[key] = 1
        self._freq_keys[1][key] = None
        self._min_freq = 1

    def __delitem__(self, key: K) -> None:
        if key not in self._values:
            raise KeyError(key)
        self._remove_key(key)

    def __contains__(self, key: object) -> bool:
        return key in self._values

    def _bump(self, key: K) -> None:
        f = self._key_freq[key]
        self._freq_keys[f].pop(key)
        if not self._freq_keys[f]:
            del self._freq_keys[f]
            if f == self._min_freq and self._freq_keys:
                self._min_freq = min(self._freq_keys)
        nf = f + 1
        self._key_freq[key] = nf
        self._freq_keys[nf][key] = None

    def _evict_one(self) -> None:
        k, _ = self._freq_keys[self._min_freq].popitem(last=False)
        del self._values[k]
        del self._key_freq[k]
        if not self._freq_keys[self._min_freq]:
            del self._freq_keys[self._min_freq]
            if self._freq_keys:
                self._min_freq = min(self._freq_keys)

    def _remove_key(self, key: K) -> None:
        f = self._key_freq[key]
        self._freq_keys[f].pop(key)
        if not self._freq_keys[f]:
            del self._freq_keys[f]
            if f == self._min_freq and self._freq_keys:
                self._min_freq = min(self._freq_keys)
        del self._values[key]
        del self._key_freq[key]
