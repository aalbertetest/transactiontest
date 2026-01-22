from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional

from .node import Node
from .sharding import HashRing


class Cluster:
    def __init__(self, nodes: Iterable[Node], replication_factor: int = 2) -> None:
        self._nodes: Dict[str, Node] = {node.id: node for node in nodes}
        self._ring = HashRing(list(self._nodes.keys()))
        self._replication_factor = max(1, min(replication_factor, len(self._nodes)))

    def add_node(self, node: Node) -> None:
        self._nodes[node.id] = node
        self._ring.add_node(node.id)
        self._replication_factor = min(self._replication_factor, len(self._nodes))

    def remove_node(self, node_id: str) -> None:
        self._nodes.pop(node_id, None)
        self._ring.remove_node(node_id)
        self._replication_factor = min(self._replication_factor, len(self._nodes))

    def get(self, key: str) -> Optional[Any]:
        nodes = self._ring.get_nodes(key, self._replication_factor)
        for node_id in nodes:
            value = self._nodes[node_id].get(key)
            if value is not None:
                return value
        return None

    def set(self, key: str, value: Any, ttl_ms: Optional[int] = None) -> int:
        nodes = self._ring.get_nodes(key, self._replication_factor)
        if not nodes:
            raise ValueError("cluster has no nodes")
        primary_id = nodes[0]
        replica_ids = nodes[1:]
        return self._nodes[primary_id].set(key, value, ttl_ms=ttl_ms, replica_ids=replica_ids)

    def delete(self, key: str) -> bool:
        nodes = self._ring.get_nodes(key, self._replication_factor)
        if not nodes:
            return False
        primary_id = nodes[0]
        replica_ids = nodes[1:]
        return self._nodes[primary_id].delete(key, replica_ids=replica_ids)

    def expire(self, key: str, ttl_ms: int) -> bool:
        nodes = self._ring.get_nodes(key, self._replication_factor)
        if not nodes:
            return False
        primary_id = nodes[0]
        replica_ids = nodes[1:]
        return self._nodes[primary_id].expire(key, ttl_ms, replica_ids=replica_ids)

    def publish(self, channel: str, payload: Any) -> int:
        if not self._nodes:
            return 0
        primary_id = self._ring.get_node(channel)
        replica_ids = [node_id for node_id in self._nodes if node_id != primary_id]
        return self._nodes[primary_id].publish(
            channel, payload, replica_ids=replica_ids
        )

    def sweep_expired(self) -> None:
        for node in self._nodes.values():
            node.sweep_expired()

    def snapshot(self) -> None:
        for node in self._nodes.values():
            node.snapshot()
