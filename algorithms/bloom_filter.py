"""Bloom filter: probabilistic set membership with configurable false-positive rate."""

from __future__ import annotations

import hashlib
import math
import struct
from typing import Iterable, Iterator, List, Optional, Set


def _optimal_m(n: int, p: float) -> int:
    """Bits m for n elements and false positive rate p."""
    if p <= 0 or p >= 1:
        raise ValueError("false positive rate p must be in (0, 1)")
    return max(1, int(math.ceil(-n * math.log(p) / (math.log(2) ** 2))))


def _optimal_k(m: int, n: int) -> int:
    """Number of hash functions."""
    if n <= 0:
        return 1
    return max(1, int(round((m / n) * math.log(2))))


class BloomFilter:
    """
    Approximate set: add and possibly_contains; no delete (use CountingBloomFilter elsewhere).

    * Space O(m) bits with m ≈ -n ln(p) / (ln 2)^2 for target false positive p at n elements.
    * Add / query O(k) hash evaluations, k ≈ (m/n) ln 2.
    * False positives possible; false negatives never (if no remove).
    """

    def __init__(self, expected_elements: int, false_positive_rate: float = 0.01) -> None:
        if expected_elements < 1:
            raise ValueError("expected_elements must be >= 1")
        self._n_cap = expected_elements
        self._p = false_positive_rate
        self._m = _optimal_m(expected_elements, false_positive_rate)
        self._k = _optimal_k(self._m, expected_elements)
        self._bits: bytearray = bytearray((self._m + 7) // 8)
        self._count = 0

    @property
    def bit_length(self) -> int:
        return self._m

    @property
    def num_hashes(self) -> int:
        return self._k

    @property
    def approx_count(self) -> int:
        """Number of adds (may overcount if same logical item added with different bytes)."""
        return self._count

    def _indices(self, item: bytes) -> Iterator[int]:
        # Double hashing from two 64-bit values derived from SHA-256(item || i)
        for i in range(self._k):
            h = hashlib.sha256(item + bytes([i])).digest()
            a = struct.unpack(">Q", h[:8])[0]
            b = struct.unpack(">Q", h[8:16])[0] | 1  # odd for full period mix
            yield (a + i * b) % self._m

    def _to_bytes(self, item: object) -> bytes:
        if isinstance(item, bytes):
            return item
        if isinstance(item, str):
            return item.encode("utf-8")
        return str(item).encode("utf-8")

    def _set_bit(self, i: int) -> None:
        self._bits[i // 8] |= 1 << (i % 8)

    def _get_bit(self, i: int) -> bool:
        return bool(self._bits[i // 8] & (1 << (i % 8)))

    def add(self, item: object) -> None:
        b = self._to_bytes(item)
        for i in self._indices(b):
            self._set_bit(i)
        self._count += 1

    def update(self, iterable: Iterable[object]) -> None:
        for x in iterable:
            self.add(x)

    def possibly_contains(self, item: object) -> bool:
        b = self._to_bytes(item)
        return all(self._get_bit(i) for i in self._indices(b))

    def __contains__(self, item: object) -> bool:
        return self.possibly_contains(item)

    def estimated_fpp(self) -> float:
        """Estimated false positive probability after approx_count inserts."""
        if self._m == 0:
            return 1.0
        x = math.exp(-self._k * self._count / self._m)
        return (1 - x) ** self._k

    @classmethod
    def from_capacity(
        cls,
        expected_elements: int,
        false_positive_rate: float = 0.01,
        initial: Optional[Iterable[object]] = None,
    ) -> "BloomFilter":
        bf = cls(expected_elements, false_positive_rate)
        if initial:
            bf.update(initial)
        return bf
