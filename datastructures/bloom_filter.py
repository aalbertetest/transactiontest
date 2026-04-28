"""
Bloom filter: approximate set membership with tunable false-positive rate.

Uses k independent hash functions derived from double hashing (few seeds).
Bit array size m, expected elements n: optimal k ≈ (m/n) ln 2.

Time: O(k) add and query. Space: O(m) bits.
False positive rate ≈ (1 - e^(-kn/m))^k; no false negatives for inserted items.
"""

from __future__ import annotations

import hashlib
import math
from typing import Iterable, Optional

# Universal-ish mixing for 64-bit state (SplitMix64 style)
def _mix64(z: int) -> int:
    z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9 & 0xFFFFFFFFFFFFFFFF
    z = (z ^ (z >> 27)) * 0x94D049BB133111EB & 0xFFFFFFFFFFFFFFFF
    return z ^ (z >> 31)


class BloomFilter:
    """
    Probabilistic set: `add` and `maybe_contains`.

    `capacity`: expected number of insertions (used with `error_rate` to size m, k).
    Or pass explicit `size` (m) and `hash_count` (k).
    """

    def __init__(
        self,
        capacity: Optional[int] = None,
        error_rate: float = 0.01,
        size: Optional[int] = None,
        hash_count: Optional[int] = None,
        seed: int = 0,
    ) -> None:
        if size is not None and hash_count is not None:
            self._m = size
            self._k = hash_count
        elif capacity is not None:
            if capacity <= 0:
                raise ValueError("capacity must be positive")
            if not 0 < error_rate < 1:
                raise ValueError("error_rate must be in (0, 1)")
            self._m = max(1, _optimal_m(capacity, error_rate))
            self._k = max(1, _optimal_k(self._m, capacity))
        else:
            raise ValueError("Provide (capacity, error_rate) or (size, hash_count)")
        self._bits = bytearray((self._m + 7) // 8)
        self._seed = seed & 0xFFFFFFFFFFFFFFFF
        self._n = 0

    @property
    def bit_length(self) -> int:
        return self._m

    @property
    def hash_count(self) -> int:
        return self._k

    def __len__(self) -> int:
        """Number of inserted elements (counter; filter does not store keys)."""
        return self._n

    def clear(self) -> None:
        self._bits[:] = b"\x00" * len(self._bits)
        self._n = 0

    def add(self, item: bytes) -> None:
        """Insert item (bytes). O(k)."""
        seen = set()
        for pos in self._positions(item):
            if pos not in seen:
                seen.add(pos)
                self._set_bit(pos)
        self._n += 1

    def add_many(self, items: Iterable[bytes]) -> None:
        for it in items:
            self.add(it)

    def maybe_contains(self, item: bytes) -> bool:
        """If False, item was definitely not added; if True, probably added. O(k)."""
        for pos in self._positions(item):
            if not self._get_bit(pos):
                return False
        return True

    def __contains__(self, item: bytes) -> bool:
        return self.maybe_contains(item)

    def estimated_fpp(self) -> float:
        """Estimated false positive probability after _n inserts (approximation)."""
        if self._m == 0:
            return 1.0
        p = math.exp(-self._k * self._n / self._m)
        return (1 - p) ** self._k

    def _positions(self, item: bytes) -> list[int]:
        h1, h2 = _two_hashes(item, self._seed)
        m = self._m
        k = self._k
        out = []
        x = h1 & 0xFFFFFFFFFFFFFFFF
        y = h2 & 0xFFFFFFFFFFFFFFFF
        for i in range(k):
            out.append((x + i * y) % m)
        return out

    def _set_bit(self, i: int) -> None:
        self._bits[i >> 3] |= 1 << (i & 7)

    def _get_bit(self, i: int) -> bool:
        return bool(self._bits[i >> 3] & (1 << (i & 7)))


def _two_hashes(data: bytes, seed: int) -> tuple[int, int]:
    """Two 64-bit hashes from SHA-256(data || seed)."""
    buf = data + seed.to_bytes(8, "little")
    d = hashlib.sha256(buf).digest()
    h1 = int.from_bytes(d[:8], "little")
    h2 = int.from_bytes(d[8:16], "little")
    return _mix64(h1), _mix64(h2)


def _optimal_m(n: int, p: float) -> int:
    return int(math.ceil(-n * math.log(p) / (math.log(2) ** 2)))


def _optimal_k(m: int, n: int) -> int:
    if n <= 0:
        return 1
    return max(1, round((m / n) * math.log(2)))
