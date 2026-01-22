import time

from cache.cluster import Cluster
from cache.node import Node
from cache.transport import InMemoryTransport


def bench_node_set_get(iterations: int = 50000) -> None:
    node = Node("n1")
    start = time.perf_counter()
    for i in range(iterations):
        node.set(f"k{i}", i)
    mid = time.perf_counter()
    for i in range(iterations):
        node.get(f"k{i}")
    end = time.perf_counter()
    set_qps = iterations / (mid - start)
    get_qps = iterations / (end - mid)
    print(f"node set: {set_qps:.0f} ops/s")
    print(f"node get: {get_qps:.0f} ops/s")


def bench_cluster_set_get(iterations: int = 50000) -> None:
    transport = InMemoryTransport()
    nodes = [Node("a", transport=transport), Node("b", transport=transport)]
    cluster = Cluster(nodes, replication_factor=2)
    start = time.perf_counter()
    for i in range(iterations):
        cluster.set(f"k{i}", i)
    mid = time.perf_counter()
    for i in range(iterations):
        cluster.get(f"k{i}")
    end = time.perf_counter()
    set_qps = iterations / (mid - start)
    get_qps = iterations / (end - mid)
    print(f"cluster set: {set_qps:.0f} ops/s")
    print(f"cluster get: {get_qps:.0f} ops/s")


if __name__ == "__main__":
    bench_node_set_get()
    bench_cluster_set_get()
