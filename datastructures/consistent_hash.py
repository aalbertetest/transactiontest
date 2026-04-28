"""
Consistent hashing: map keys to nodes with minimal remapping when nodes are added/removed.

Ring: 64-bit hash space. Each node placed at multiple virtual replicas
for better load balance. Lookup finds first replica >= key hash (wrap).

Time: O(log V) per lookup with bisect (V = virtual nodes). Space O(V).
"""

from __future__ import annotations

import bisect
import hashlib
from dataclasses import dataclass
from typing import Dict, Generic, Hashable, Iterable, Iterator, List, Optional, Tuple, TypeVar

T = TypeVar("T", bound=Hashable)


def _hash_int(key: bytes, bits: int = 64) -> int:
    h = hashlib.sha256(key).digest()
    nbytes = (bits + 7) // 8
    mask = (1 << bits) - 1
    return int.from_bytes(h[:nbytes], "little") & mask


@dataclass(frozen=True)
class RingNode(Generic[T]):
    """Physical node identifier (your shard/server id)."""

    id: T


class ConsistentHashRing(Generic[T]):
    """
    Hash ring with virtual nodes per physical node.

    `replicas`: virtual points per physical node (higher = smoother distribution).
    """

    def __init__(self, replicas: int = 150) -> None:
        if replicas < 1:
            raise ValueError("replicas must be >= 1")
        self._replicas = replicas
        self._ring: List[int] = []
        self._node_at: Dict[int, T] = {}
        self._sorted_hashes: List[int] = []

    def __len__(self) -> int:
        return len({self._node_at[h] for h in self._sorted_hashes})

    def add_node(self, node: T) -> None:
        """Register a physical node and its virtual replicas."""
        for i in range(self._replicas):
            h = _vnode_hash(node, i)
            if h not in self._node_at:
                bisect.insort(self._sorted_hashes, h)
            self._node_at[h] = node

    def remove_node(self, node: T) -> None:
        """Remove all virtual replicas for `node`. Raises KeyError if unknown."""
        found = False
        for i in range(self._replicas):
            h = _vnode_hash(node, i)
            if h in self._node_at and self._node_at[h] == node:
                found = True
                del self._node_at[h]
                idx = bisect.bisect_left(self._sorted_hashes, h)
                if idx < len(self._sorted_hashes) and self._sorted_hashes[idx] == h:
                    self._sorted_hashes.pop(idx)
        if not found:
            raise KeyError(node)

    def get_node(self, key: bytes) -> Optional[T]:
        """Map key to a node, or None if ring is empty."""
        if not self._sorted_hashes:
            return None
        hk = _hash_int(key)
        idx = bisect.bisect_right(self._sorted_hashes, hk)
        if idx == len(self._sorted_hashes):
            idx = 0
        return self._node_at[self._sorted_hashes[idx]]

    def get_n_nodes(self, key: bytes, n: int) -> List[T]:
        """Return up to `n` distinct successor nodes on the ring (for replication)."""
        if n <= 0 or not self._sorted_hashes:
            return []
        hk = _hash_int(key)
        idx = bisect.bisect_right(self._sorted_hashes, hk)
        seen: set = set()
        out: List[T] = []
        m = len(self._sorted_hashes)
        for step in range(m):
            j = (idx + step) % m
            node = self._node_at[self._sorted_hashes[j]]
            if node not in seen:
                seen.add(node)
                out.append(node)
            if len(out) >= n:
                break
        return out

    def iter_nodes_in_ring_order(self) -> Iterator[Tuple[int, T]]:
        """(hash, node) in ascending hash order (includes virtual duplicates)."""
        for h in self._sorted_hashes:
            yield h, self._node_at[h]


def _vnode_hash(node: Hashable, replica_index: int) -> int:
    data = f"{node!r}:{replica_index}".encode()
    return _hash_int(data)
