"""Counting Bloom filter (approximate set membership)."""

from __future__ import annotations

import hashlib
import math
import struct
from typing import Iterable, List


def _hashes(key: bytes, k: int, m: int, seed: int = 0x9E3779B9) -> List[int]:
    """k independent-ish indexes in [0, m) using SHA-256 streaming."""
    out: List[int] = []
    buf = key
    counter = 0
    while len(out) < k:
        h = hashlib.sha256(struct.pack("<I", seed + counter) + buf).digest()
        for j in range(0, len(h) - 7, 8):
            if len(out) >= k:
                break
            val = int.from_bytes(h[j : j + 8], "big")
            out.append(val % m)
        counter += 1
    return out


class BloomFilter:
    """
    Counting Bloom filter: supports add, remove (approximate), and possibly_contains.
    False negatives never occur for standard Bloom (non-removing); with removals,
    false negatives are possible if removal saturates counters incorrectly — use
    conservative sizing or avoid remove when possible.
    """

    def __init__(self, expected_n: int, false_positive_rate: float, max_counter: int = 15) -> None:
        if expected_n <= 0:
            raise ValueError("expected_n must be positive")
        if not 0 < false_positive_rate < 1:
            raise ValueError("false_positive_rate must be in (0, 1)")
        self._max_c = max_counter
        m_float = -expected_n * math.log(false_positive_rate) / (math.log(2) ** 2)
        self._m = max(8, int(math.ceil(m_float)))
        k_float = (self._m / expected_n) * math.log(2)
        self._k = max(1, int(round(k_float)))
        self._bits = [0] * self._m

    @property
    def m(self) -> int:
        return self._m

    @property
    def k(self) -> int:
        return self._k

    def _key_bytes(self, item: object) -> bytes:
        if isinstance(item, bytes):
            return item
        return str(item).encode("utf-8", errors="replace")

    def add(self, item: object) -> None:
        kb = self._key_bytes(item)
        for i in _hashes(kb, self._k, self._m):
            self._bits[i] = min(self._max_c, self._bits[i] + 1)

    def remove(self, item: object) -> None:
        """Decrement counters; may cause false negatives if item was not inserted."""
        kb = self._key_bytes(item)
        for i in _hashes(kb, self._k, self._m):
            if self._bits[i] > 0:
                self._bits[i] -= 1

    def possibly_contains(self, item: object) -> bool:
        kb = self._key_bytes(item)
        for i in _hashes(kb, self._k, self._m):
            if self._bits[i] == 0:
                return False
        return True

    def clear(self) -> None:
        for i in range(self._m):
            self._bits[i] = 0

    def update(self, items: Iterable[object]) -> None:
        for x in items:
            self.add(x)
