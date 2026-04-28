"""
LRU and LFU caches with explicit eviction policies.

LRU (Least Recently Used)
-------------------------
**Time:** `get` / `set` / `delete` — **O(1)** average (hash map + doubly-linked list or OrderedDict).
**Space:** **O(capacity)** for stored entries plus **O(1)** bookkeeping.

Walkthrough — LRU
-----------------
Maintain insertion/recency order; on access, mark entry as most recent; on eviction remove least recent.

Edge cases: capacity 0 (no storage), capacity 1 (every new key evicts previous), repeated access updates order.

LFU (Least Frequently Used)
---------------------------
**Time:** `get` / `set` — **O(1)** average with bucketed frequency lists (hash map + per-frequency FIFO).

**Space:** **O(capacity)** entries plus **O(number of distinct frequencies)** ≤ O(capacity).

Walkthrough — LFU
-----------------
Track access count per key; eviction picks smallest frequency, ties broken by **FIFO** among those keys.

Edge cases: new key starts at frequency 1; increment on get/set; when evicting from min bucket, update min_freq.
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Dict, Generic, Hashable, Iterator, Optional, Tuple, TypeVar

K = TypeVar("K", bound=Hashable)
V = TypeVar("V")


class LRUCache(Generic[K, V]):
    """Fixed-capacity cache evicting least-recently-used entries."""

    __slots__ = ("_cap", "_data")

    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self._cap = capacity
        self._data: OrderedDict[K, V] = OrderedDict()

    @property
    def capacity(self) -> int:
        return self._cap

    def __len__(self) -> int:
        return len(self._data)

    def __contains__(self, key: object) -> bool:
        return key in self._data

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
        if self._cap == 0:
            return
        if key in self._data:
            self._data.move_to_end(key)
            self._data[key] = value
            return
        self._data[key] = value
        if len(self._data) > self._cap:
            self._data.popitem(last=False)

    def __delitem__(self, key: K) -> None:
        del self._data[key]

    def pop(self, key: K, default: object = ...) -> V:
        if key in self._data:
            return self._data.pop(key)
        if default is ...:
            raise KeyError(key)
        return default  # type: ignore[no-any-return]

    def clear(self) -> None:
        self._data.clear()

    def items(self) -> Iterator[Tuple[K, V]]:
        return iter(self._data.items())


class LFUCache(Generic[K, V]):
    """Fixed-capacity cache evicting least-frequently-used; ties broken by FIFO."""

    __slots__ = ("_cap", "_kv", "_freq", "_min_f")

    def __init__(self, capacity: int) -> None:
        if capacity < 0:
            raise ValueError("capacity must be non-negative")
        self._cap = capacity
        self._kv: Dict[K, Tuple[V, int]] = {}
        self._freq: Dict[int, OrderedDict[K, None]] = {}
        self._min_f = 0

    @property
    def capacity(self) -> int:
        return self._cap

    def __len__(self) -> int:
        return len(self._kv)

    def _bump_min(self) -> None:
        while self._min_f not in self._freq or not self._freq[self._min_f]:
            self._min_f += 1

    def _remove_from_freq(self, key: K, f: int) -> None:
        del self._freq[f][key]
        if not self._freq[f]:
            del self._freq[f]
            if f == self._min_f:
                self._bump_min()

    def _increment(self, key: K) -> None:
        val, f = self._kv[key]
        self._remove_from_freq(key, f)
        nf = f + 1
        if nf not in self._freq:
            self._freq[nf] = OrderedDict()
        self._freq[nf][key] = None
        self._kv[key] = (val, nf)

    def _evict_one(self) -> None:
        assert self._kv
        self._bump_min()
        victim = next(iter(self._freq[self._min_f]))
        del self._freq[self._min_f][victim]
        if not self._freq[self._min_f]:
            del self._freq[self._min_f]
        del self._kv[victim]
        if self._freq:
            self._min_f = min(self._freq)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        if key not in self._kv:
            return default
        val, _ = self._kv[key]
        self._increment(key)
        return val

    def __getitem__(self, key: K) -> V:
        if key not in self._kv:
            raise KeyError(key)
        val, _ = self._kv[key]
        self._increment(key)
        return val

    def __setitem__(self, key: K, value: V) -> None:
        if self._cap == 0:
            return
        if key in self._kv:
            _, f = self._kv[key]
            self._kv[key] = (value, f)
            self._increment(key)
            return
        if len(self._kv) >= self._cap:
            self._evict_one()
        self._kv[key] = (value, 1)
        if 1 not in self._freq:
            self._freq[1] = OrderedDict()
        self._freq[1][key] = None
        self._min_f = 1

    def __contains__(self, key: object) -> bool:
        return key in self._kv

    def __delitem__(self, key: K) -> None:
        if key not in self._kv:
            raise KeyError(key)
        _, f = self._kv.pop(key)
        del self._freq[f][key]
        if not self._freq[f]:
            del self._freq[f]
            if self._kv and f == self._min_f:
                self._min_f = min(self._freq)

    def clear(self) -> None:
        self._kv.clear()
        self._freq.clear()
        self._min_f = 0


def demo_caches() -> None:
    lru: LRUCache[int, str] = LRUCache(2)
    lru[1] = "a"
    lru[2] = "b"
    _ = lru[1]
    lru[3] = "c"
    assert 2 not in lru

    lfu: LFUCache[int, str] = LFUCache(2)
    lfu[1] = "a"
    lfu[2] = "b"
    _ = lfu[1]
    _ = lfu[1]
    lfu[3] = "c"
    assert 2 not in lfu


if __name__ == "__main__":
    demo_caches()
