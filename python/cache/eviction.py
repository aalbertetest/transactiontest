from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional, Protocol


class EvictionPolicy(Protocol):
    def on_get(self, key: str) -> None:
        ...

    def on_set(self, key: str) -> None:
        ...

    def on_delete(self, key: str) -> None:
        ...

    def evict(self, capacity: int, size: int) -> List[str]:
        ...


@dataclass
class _Node:
    key: str
    prev: Optional["_Node"] = None
    next: Optional["_Node"] = None


class LRUEviction(EvictionPolicy):
    def __init__(self) -> None:
        self._nodes: Dict[str, _Node] = {}
        self._head: Optional[_Node] = None
        self._tail: Optional[_Node] = None

    def on_get(self, key: str) -> None:
        node = self._nodes.get(key)
        if not node:
            return
        self._move_to_head(node)

    def on_set(self, key: str) -> None:
        node = self._nodes.get(key)
        if node:
            self._move_to_head(node)
            return
        node = _Node(key=key)
        self._nodes[key] = node
        self._add_to_head(node)

    def on_delete(self, key: str) -> None:
        node = self._nodes.pop(key, None)
        if not node:
            return
        self._remove(node)

    def evict(self, capacity: int, size: int) -> List[str]:
        evicted: List[str] = []
        while size > capacity and self._tail:
            key = self._tail.key
            evicted.append(key)
            self.on_delete(key)
            size -= 1
        return evicted

    def _add_to_head(self, node: _Node) -> None:
        node.prev = None
        node.next = self._head
        if self._head:
            self._head.prev = node
        self._head = node
        if not self._tail:
            self._tail = node

    def _remove(self, node: _Node) -> None:
        if node.prev:
            node.prev.next = node.next
        else:
            self._head = node.next
        if node.next:
            node.next.prev = node.prev
        else:
            self._tail = node.prev
        node.prev = None
        node.next = None

    def _move_to_head(self, node: _Node) -> None:
        if node is self._head:
            return
        self._remove(node)
        self._add_to_head(node)
