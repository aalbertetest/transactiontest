from __future__ import annotations

import bisect
import hashlib
from typing import List, Sequence


class HashRing:
    def __init__(self, nodes: Sequence[str] | None = None, vnodes: int = 64) -> None:
        self._vnodes = vnodes
        self._ring: List[tuple[int, str]] = []
        if nodes:
            for node_id in nodes:
                self.add_node(node_id)

    def add_node(self, node_id: str) -> None:
        for i in range(self._vnodes):
            h = self._hash(f"{node_id}:{i}")
            bisect.insort(self._ring, (h, node_id))

    def remove_node(self, node_id: str) -> None:
        self._ring = [(h, n) for h, n in self._ring if n != node_id]

    def get_node(self, key: str) -> str:
        if not self._ring:
            raise ValueError("hash ring is empty")
        h = self._hash(key)
        idx = bisect.bisect(self._ring, (h, ""))
        if idx == len(self._ring):
            idx = 0
        return self._ring[idx][1]

    def get_nodes(self, key: str, count: int) -> List[str]:
        if not self._ring:
            return []
        if count <= 0:
            return []
        h = self._hash(key)
        idx = bisect.bisect(self._ring, (h, ""))
        seen = set()
        nodes: List[str] = []
        while len(nodes) < count and len(seen) < len(self._ring):
            if idx == len(self._ring):
                idx = 0
            node_id = self._ring[idx][1]
            if node_id not in seen:
                seen.add(node_id)
                nodes.append(node_id)
            idx += 1
        return nodes

    @staticmethod
    def _hash(value: str) -> int:
        digest = hashlib.sha1(value.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big")
