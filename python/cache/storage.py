from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional, Tuple, Callable

from .eviction import EvictionPolicy, LRUEviction


@dataclass
class Entry:
    value: Any
    expires_at: Optional[int]
    version: int


class Store:
    def __init__(
        self,
        capacity: int = 1024,
        eviction: Optional[EvictionPolicy] = None,
        clock: Optional[Callable[[], int]] = None,
    ) -> None:
        self._entries: Dict[str, Entry] = {}
        self._capacity = capacity
        self._eviction = eviction or LRUEviction()
        self._clock = clock or (lambda: 0)
        self._version = 0

    def set(
        self,
        key: str,
        value: Any,
        ttl_ms: Optional[int] = None,
        *,
        version: Optional[int] = None,
    ) -> Tuple[int, List[str]]:
        expires_at = self._clock() + ttl_ms if ttl_ms is not None else None
        if version is None:
            self._version += 1
            version = self._version
        entry = Entry(value=value, expires_at=expires_at, version=version)
        self._entries[key] = entry
        self._eviction.on_set(key)
        evicted = self._evict_if_needed()
        return version, evicted

    def get(self, key: str) -> Optional[Any]:
        entry = self._entries.get(key)
        if not entry:
            return None
        if self._is_expired(entry):
            self.delete(key)
            return None
        self._eviction.on_get(key)
        return entry.value

    def get_entry(self, key: str) -> Optional[Entry]:
        entry = self._entries.get(key)
        if not entry:
            return None
        if self._is_expired(entry):
            self.delete(key)
            return None
        return entry

    def delete(self, key: str) -> bool:
        existed = key in self._entries
        if existed:
            self._entries.pop(key, None)
            self._eviction.on_delete(key)
        return existed

    def expire(self, key: str, ttl_ms: int, *, version: Optional[int] = None) -> bool:
        entry = self._entries.get(key)
        if not entry:
            return False
        if version is None:
            self._version += 1
            version = self._version
        entry.expires_at = self._clock() + ttl_ms
        entry.version = version
        return True

    def sweep_expired(self) -> List[str]:
        expired: List[str] = []
        for key, entry in list(self._entries.items()):
            if self._is_expired(entry):
                self.delete(key)
                expired.append(key)
        return expired

    def items(self) -> Iterable[Tuple[str, Entry]]:
        return self._entries.items()

    def size(self) -> int:
        return len(self._entries)

    def _is_expired(self, entry: Entry) -> bool:
        return entry.expires_at is not None and self._clock() >= entry.expires_at

    def _evict_if_needed(self) -> List[str]:
        if self._capacity <= 0:
            return []
        if self.size() <= self._capacity:
            return []
        evicted = self._eviction.evict(self._capacity, self.size())
        for key in evicted:
            self._entries.pop(key, None)
        return evicted
