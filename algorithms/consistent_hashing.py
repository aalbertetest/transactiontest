"""Consistent hashing ring with virtual nodes for better load balance."""

from __future__ import annotations

import bisect
import hashlib
from dataclasses import dataclass
from typing import Dict, Generic, Hashable, Iterator, List, Optional, Tuple, TypeVar

T = TypeVar("T")


def _hash_int(key: bytes) -> int:
    return int.from_bytes(hashlib.md5(key).digest()[:8], "big", signed=False)


@dataclass(frozen=True)
class VirtualNode(Generic[T]):
    position: int
    node: T
    vnode_index: int


class ConsistentHashRing(Generic[T]):
    """
    Map keys to physical nodes; adding/removing a node moves only O(1/N) keys in expectation.

    * Each physical node is placed at `replicas` positions on the ring (virtual nodes).
    * lookup O(log(N * replicas)) binary search on sorted positions.
    * Space O(N * replicas) for the sorted list plus node metadata.
    """

    def __init__(self, replicas: int = 150) -> None:
        if replicas < 1:
            raise ValueError("replicas must be >= 1")
        self._replicas = replicas
        self._positions: List[int] = []
        self._vnodes: List[VirtualNode[T]] = []
        self._node_weights: Dict[T, int] = {}

    def __len__(self) -> int:
        return len(self._node_weights)

    def __bool__(self) -> bool:
        return bool(self._positions)

    def _vnode_key(self, node: T, i: int) -> bytes:
        return f"{node!r}:{i}".encode("utf-8", errors="replace")

    def add_node(self, node: T, weight: int = 1) -> None:
        if weight < 1:
            raise ValueError("weight must be >= 1")
        if node in self._node_weights:
            raise ValueError("node already present; remove first to change weight")
        self._node_weights[node] = weight
        count = self._replicas * weight
        for i in range(count):
            pos = _hash_int(self._vnode_key(node, i))
            vn = VirtualNode(position=pos, node=node, vnode_index=i)
            idx = bisect.bisect_left(self._positions, pos)
            self._positions.insert(idx, pos)
            self._vnodes.insert(idx, vn)

    def remove_node(self, node: T) -> None:
        if node not in self._node_weights:
            raise KeyError(node)
        w = self._node_weights.pop(node)
        count = self._replicas * w
        to_remove: List[Tuple[int, int]] = []
        for i in range(count):
            pos = _hash_int(self._vnode_key(node, i))
            to_remove.append((pos, i))
        for pos, vi in to_remove:
            idx = bisect.bisect_left(self._positions, pos)
            found = False
            while idx < len(self._positions) and self._positions[idx] == pos:
                v = self._vnodes[idx]
                if v.node == node and v.vnode_index == vi:
                    del self._positions[idx]
                    del self._vnodes[idx]
                    found = True
                    break
                idx += 1
            if not found:
                raise RuntimeError("consistent hash invariant broken")

    def _key_position(self, key: Hashable) -> int:
        if isinstance(key, bytes):
            b = key
        elif isinstance(key, str):
            b = key.encode("utf-8")
        else:
            b = str(key).encode("utf-8")
        return _hash_int(b)

    def get_node(self, key: Hashable) -> T:
        if not self._positions:
            raise RuntimeError("ring is empty")
        pos = self._key_position(key)
        idx = bisect.bisect_right(self._positions, pos) % len(self._positions)
        return self._vnodes[idx].node

    def get_nodes(self, key: Hashable, n: int) -> List[T]:
        """Return up to n distinct physical nodes walking clockwise from key."""
        if n < 1:
            raise ValueError("n must be >= 1")
        if not self._positions:
            raise RuntimeError("ring is empty")
        pos = self._key_position(key)
        start = bisect.bisect_right(self._positions, pos) % len(self._positions)
        out: List[T] = []
        seen: set = set()
        for j in range(len(self._positions)):
            vn = self._vnodes[(start + j) % len(self._vnodes)]
            if vn.node not in seen:
                seen.add(vn.node)
                out.append(vn.node)
            if len(out) >= n:
                break
        return out

    def nodes(self) -> Iterator[T]:
        yield from self._node_weights.keys()
