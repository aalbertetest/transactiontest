import tempfile
import unittest

from cache.cluster import Cluster
from cache.node import Node
from cache.persistence import Persistence
from cache.transport import InMemoryTransport


class CacheTests(unittest.TestCase):
    def test_set_get_ttl(self) -> None:
        now = [0]
        clock = lambda: now[0]
        node = Node("n1", clock=clock)
        node.set("a", "value", ttl_ms=10)
        self.assertEqual(node.get("a"), "value")
        now[0] = 11
        self.assertIsNone(node.get("a"))

    def test_lru_eviction(self) -> None:
        node = Node("n1", capacity=2, clock=lambda: 0)
        node.set("a", 1)
        node.set("b", 2)
        node.get("a")
        node.set("c", 3)
        self.assertIsNone(node.get("b"))
        self.assertEqual(node.get("a"), 1)
        self.assertEqual(node.get("c"), 3)

    def test_replication(self) -> None:
        transport = InMemoryTransport()
        node_a = Node("a", transport=transport, clock=lambda: 0)
        node_b = Node("b", transport=transport, clock=lambda: 0)
        cluster = Cluster([node_a, node_b], replication_factor=2)
        cluster.set("k1", "v1")
        self.assertEqual(node_b.get("k1"), "v1")

    def test_persistence_snapshot_and_log(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            snapshot = f"{tmp}/snapshot.json"
            log = f"{tmp}/aof.log"
            persistence = Persistence(snapshot, log)
            now = [1000]
            clock = lambda: now[0]
            node = Node("n1", clock=clock, persistence=persistence)
            node.set("a", "value")
            node.snapshot()
            node.set("b", "value2", ttl_ms=100)

            node2 = Node("n2", clock=clock, persistence=persistence)
            node2.load()
            self.assertEqual(node2.get("a"), "value")
            self.assertEqual(node2.get("b"), "value2")

            now[0] += 200
            self.assertIsNone(node2.get("b"))

    def test_pubsub_cluster(self) -> None:
        transport = InMemoryTransport()
        node_a = Node("a", transport=transport)
        node_b = Node("b", transport=transport)
        cluster = Cluster([node_a, node_b], replication_factor=2)
        received = []

        node_b.subscribe("news", lambda payload: received.append(payload))
        cluster.publish("news", {"hello": "world"})

        self.assertEqual(received, [{"hello": "world"}])


if __name__ == "__main__":
    unittest.main()
