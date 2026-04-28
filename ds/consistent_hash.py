"""Consistent hashing ring with virtual nodes."""

from __future__ import annotations

import bisect
import hashlib
from dataclasses import dataclass
from typing import Any, Callable, Dict, Generic, Hashable, Iterable, List, Optional, TypeVar

T = TypeVar("T")


def _default_hash(key: bytes) -> int:
    return int.from_bytes(hashlib.sha256(key).digest()[:8], "big")


@dataclass(frozen=True)
class RingNode(Generic[T]):
    token: int
    physical: T


class ConsistentHashRing(Generic[T]):
    """
    Keys are assigned to the first server at or after hash(key) on the ring.
    """

    def __init__(
        self,
        replicas: int = 150,
        hash_fn: Optional[Callable[[bytes], int]] = None,
    ) -> None:
        if replicas < 1:
            raise ValueError("replicas must be >= 1")
        self._replicas = replicas
        self._hash = hash_fn or _default_hash
        self._tokens: List[int] = []
        self._nodes: List[RingNode[T]] = []
        self._counts: Dict[T, int] = {}

    def add_node(self, node: T) -> None:
        """Add a physical node with `replicas` virtual positions."""
        if node in self._counts:
            raise ValueError("node already in ring")
        self._counts[node] = self._replicas
        for i in range(self._replicas):
            raw = f"{node!r}:{i}".encode("utf-8", errors="replace")
            tok = self._hash(raw)
            ins = bisect.bisect_left(self._tokens, tok)
            self._tokens.insert(ins, tok)
            self._nodes.insert(ins, RingNode(token=tok, physical=node))

    def remove_node(self, node: T) -> None:
        if node not in self._counts:
            raise KeyError(node)
        del self._counts[node]
        new_tok: List[int] = []
        new_nodes: List[RingNode[T]] = []
        for t, rn in zip(self._tokens, self._nodes):
            if rn.physical != node:
                new_tok.append(t)
                new_nodes.append(rn)
        self._tokens = new_tok
        self._nodes = new_nodes

    def get_node(self, key: Hashable) -> T:
        if not self._tokens:
            raise RuntimeError("ring is empty")
        kb = str(key).encode("utf-8", errors="replace")
        h = self._hash(kb)
        idx = bisect.bisect_left(self._tokens, h)
        if idx == len(self._tokens):
            idx = 0
        return self._nodes[idx].physical

    def __len__(self) -> int:
        return len(self._counts)

    def physical_nodes(self) -> Iterable[T]:
        return self._counts.keys()
