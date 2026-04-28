"""LRU and LFU caches (capacity-limited, dict-like get/set)."""

from __future__ import annotations

from collections import Counter, OrderedDict
from typing import Any, Dict, Generic, Hashable, Optional, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """Least Recently Used: evicts the stale key on overflow."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._cap = capacity
        self._data: OrderedDict[K, V] = OrderedDict()

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
        if len(self._data) > self._cap:
            self._data.popitem(last=False)

    def __contains__(self, key: object) -> bool:
        return key in self._data

    def pop(self, key: K, default: Any = None) -> Any:
        return self._data.pop(key, default)


class LFUCache(Generic[K, V]):
    """Least Frequently Used: evicts smallest frequency; ties broken by LRU."""

    def __init__(self, capacity: int) -> None:
        if capacity < 1:
            raise ValueError("capacity must be >= 1")
        self._cap = capacity
        self._val: Dict[K, V] = {}
        self._freq: Counter[K] = Counter()
        self._lists: Dict[int, OrderedDict[K, None]] = {}
        self._min_freq = 0

    def __len__(self) -> int:
        return len(self._val)

    def _touch(self, key: K) -> None:
        f = self._freq[key]
        self._freq[key] = f + 1
        del self._lists[f][key]
        if not self._lists[f]:
            del self._lists[f]
            if self._min_freq == f:
                self._min_freq += 1
        nf = f + 1
        if nf not in self._lists:
            self._lists[nf] = OrderedDict()
        self._lists[nf][key] = None

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        if key not in self._val:
            return default
        self._touch(key)
        return self._val[key]

    def __getitem__(self, key: K) -> V:
        if key not in self._val:
            raise KeyError(key)
        self._touch(key)
        return self._val[key]

    def __setitem__(self, key: K, value: V) -> None:
        if key in self._val:
            self._val[key] = value
            self._touch(key)
            return
        if len(self._val) >= self._cap:
            self._evict()
        self._val[key] = value
        self._freq[key] = 1
        if 1 not in self._lists:
            self._lists[1] = OrderedDict()
        self._lists[1][key] = None
        self._min_freq = 1

    def _evict(self) -> None:
        k, _ = self._lists[self._min_freq].popitem(last=False)
        del self._val[k]
        del self._freq[k]
        if not self._lists[self._min_freq]:
            del self._lists[self._min_freq]
        if self._lists:
            self._min_freq = min(self._lists)

    def pop(self, key: K, default: Any = None) -> Any:
        if key not in self._val:
            return default
        v = self._val.pop(key)
        f = self._freq.pop(key)
        del self._lists[f][key]
        if not self._lists[f]:
            del self._lists[f]
        if self._lists:
            self._min_freq = min(self._lists)
        else:
            self._min_freq = 0
        return v

    def __contains__(self, key: object) -> bool:
        return key in self._val
