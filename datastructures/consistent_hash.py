"""
Consistent hashing — minimal virtual-node ring for distributed cache/routing.

Complexity
----------
Let R = number of virtual replicas per physical node, N = physical nodes, K = number of keys to route.

- Add/remove node (rebalance only affected segments): **O(R log(RN))** for sorted structure;
  with `bisect` on a sorted key list: finding successors **O(log(RN))** per key lookup.
- Key lookup: **O(log(RN))** for binary search on sorted ring positions.

Space: **O(RN)** ring entries (each stores node id and hash position).

Walkthrough — lookup
--------------------
Hash key → angle on circle → find first ring entry ≥ hash (wrap); return that node.

Walkthrough — add node
----------------------
Insert R virtual points `(hash(node_id, i), node_id)` into sorted structure.

Edge cases
----------
- **Empty ring**: `get_node` raises `RuntimeError`.
- **Single physical node**: every key maps to it.
- **Collisions**: same hash position may occur; `bisect_left` picks first; duplicates allowed.
"""

from __future__ import annotations

import bisect
import hashlib
from dataclasses import dataclass
from typing import Generic, Hashable, Iterable, List, Optional, Tuple, TypeVar

TNode = TypeVar("TNode", bound=Hashable)


@dataclass(frozen=True)
class _RingEntry(Generic[TNode]):
    position: int
    node: TNode


class ConsistentHashRing(Generic[TNode]):
    """
    Consistent hash ring with configurable virtual replicas per physical node.
    """

    def __init__(self, replicas: int = 150) -> None:
        if replicas < 1:
            raise ValueError("replicas must be >= 1")
        self._replicas = replicas
        self._entries: List[_RingEntry[TNode]] = []

    def __len__(self) -> int:
        return len(self._entries)

    @property
    def replicas(self) -> int:
        return self._replicas

    def _vnode_positions(self, node: TNode) -> List[int]:
        base = str(node).encode()
        out: List[int] = []
        for i in range(self._replicas):
            h = hashlib.blake2b(base + b"|" + str(i).encode(), digest_size=8).digest()
            out.append(int.from_bytes(h, "little"))
        return out

    def add_node(self, node: TNode) -> None:
        for pos in self._vnode_positions(node):
            entry = _RingEntry(pos, node)
            positions = [e.position for e in self._entries]
            idx = bisect.bisect_left(positions, pos)
            self._entries.insert(idx, entry)

    def remove_node(self, node: TNode) -> None:
        self._entries = [e for e in self._entries if e.node != node]

    def add_nodes(self, nodes: Iterable[TNode]) -> None:
        for n in nodes:
            self.add_node(n)

    @staticmethod
    def _key_hash(key: bytes) -> int:
        return int.from_bytes(hashlib.blake2b(key, digest_size=8).digest(), "little")

    def get_node(self, key: bytes) -> TNode:
        if not self._entries:
            raise RuntimeError("consistent hash ring is empty")
        h = self._key_hash(key)
        positions = [e.position for e in self._entries]
        idx = bisect.bisect_left(positions, h)
        if idx == len(self._entries):
            idx = 0
        return self._entries[idx].node

    def get_nodes(self, key: bytes, count: int) -> List[TNode]:
        """Return up to `count` distinct physical nodes walking clockwise from key."""
        if count < 1:
            return []
        if not self._entries:
            raise RuntimeError("consistent hash ring is empty")
        h = self._key_hash(key)
        positions = [e.position for e in self._entries]
        idx = bisect.bisect_left(positions, h)
        if idx == len(self._entries):
            idx = 0
        seen: set[TNode] = set()
        out: List[TNode] = []
        n = len(self._entries)
        for step in range(n):
            e = self._entries[(idx + step) % n]
            if e.node not in seen:
                seen.add(e.node)
                out.append(e.node)
            if len(out) >= count:
                break
        return out


def demo_ring() -> None:
    ring: ConsistentHashRing[str] = ConsistentHashRing(replicas=20)
    ring.add_nodes(["a", "b", "c"])
    n = ring.get_node(b"session:42")
    assert n in {"a", "b", "c"}


if __name__ == "__main__":
    demo_ring()
