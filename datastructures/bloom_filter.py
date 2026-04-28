"""
Bloom filter — probabilistic set membership with **no false negatives**.

Complexity (m bits, k hash functions, n inserted elements)
---------------------------------------------------------
- Insert / query: **O(k)** time (k independent hash probes).
- Space: **O(m)** bits (plus O(k) if storing seeds — here we derive hash indices from two 64-bit hashes).

False positive rate (approximate, independent ideal hashes):

    (1 - exp(-kn/m))^k

Walkthrough — insert
--------------------
Hash element to k positions in [0, m); set those bits to 1.

Walkthrough — query
-------------------
Check all k positions; if any bit is 0, definitely not inserted; if all 1, maybe inserted.

Edge cases
----------
- **Empty filter**: all bits 0; `might_contain` is always False until inserts.
- **Full filter** (all bits 1): every query returns True (useless — tune m, k, expected n).
- **Python hash randomization**: we use **stable** hashing via SHA-256 (not built-in `hash()`).
"""

from __future__ import annotations

import hashlib
import math
from typing import Iterable, Iterator, Optional


def _optimal_k(m: int, n: float) -> int:
    """Approximate optimal k for given m and expected n (may clamp)."""
    if m <= 0 or n <= 0:
        return 1
    k = round((m / n) * math.log(2))
    return max(1, min(k, m))


class BloomFilter:
    """
    Fixed-size bit array Bloom filter using double hashing from one SHA-256 digest.
    """

    __slots__ = ("_bits", "_m", "_k", "_n")

    def __init__(self, expected_elements: int, false_positive_probability: float) -> None:
        if expected_elements <= 0:
            raise ValueError("expected_elements must be positive")
        if not 0 < false_positive_probability < 1:
            raise ValueError("false_positive_probability must be in (0, 1)")
        ln2 = math.log(2)
        m = -expected_elements * math.log(false_positive_probability) / (ln2**2)
        self._m = max(8, int(math.ceil(m)))
        self._k = _optimal_k(self._m, float(expected_elements))
        self._k = min(self._k, self._m)
        self._bits = bytearray((self._m + 7) // 8)
        self._n = 0

    @classmethod
    def from_size(cls, num_bits: int, num_hashes: int) -> "BloomFilter":
        """Construct with explicit m and k (for testing)."""
        if num_bits < 1:
            raise ValueError("num_bits must be >= 1")
        if num_hashes < 1:
            raise ValueError("num_hashes must be >= 1")
        inst = cls.__new__(cls)
        inst._m = num_bits
        inst._k = min(num_hashes, num_bits)
        inst._bits = bytearray((inst._m + 7) // 8)
        inst._n = 0
        return inst

    @property
    def num_bits(self) -> int:
        return self._m

    @property
    def num_hashes(self) -> int:
        return self._k

    @property
    def approximate_size(self) -> int:
        """Number of insert calls (not deduplicated)."""
        return self._n

    def _indices(self, item: bytes) -> Iterator[int]:
        digest = hashlib.sha256(item).digest()
        h1 = int.from_bytes(digest[:8], "little")
        h2 = int.from_bytes(digest[8:16], "little") | 1
        for i in range(self._k):
            yield (h1 + i * h2) % self._m

    def _set_bit(self, index: int) -> None:
        self._bits[index // 8] |= 1 << (index % 8)

    def _get_bit(self, index: int) -> bool:
        return bool(self._bits[index // 8] & (1 << (index % 8)))

    def add(self, item: bytes) -> None:
        for idx in self._indices(item):
            self._set_bit(idx)
        self._n += 1

    def add_many(self, items: Iterable[bytes]) -> None:
        for it in items:
            self.add(it)

    def might_contain(self, item: bytes) -> bool:
        return all(self._get_bit(i) for i in self._indices(item))

    def estimated_fpp(self) -> float:
        """Approximate false positive probability given inserted count (same as independent model)."""
        if self._n == 0:
            return 0.0
        return (1 - math.exp(-self._k * self._n / self._m)) ** self._k


def demo_bloom() -> None:
    bf = BloomFilter.from_size(256, 4)
    bf.add(b"a")
    assert bf.might_contain(b"a")
    assert not bf.might_contain(b"b")


if __name__ == "__main__":
    demo_bloom()
