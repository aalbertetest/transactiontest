#!/usr/bin/env python3
"""Minimal runnable examples for each data structure."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from algorithms import BloomFilter, BTree, ConsistentHashRing, LFUCache, LRUCache, RedBlackTree


def main() -> None:
    # Red-black tree
    rbt: RedBlackTree[str, int] = RedBlackTree()
    rbt["gamma"] = 3
    rbt["alpha"] = 1
    rbt["beta"] = 2
    print("RB tree in-order:", list(rbt.items()))

    # B-tree
    bt = BTree[int, str](t=3)
    for i in [10, 20, 5, 6, 12, 30]:
        bt[i] = f"v{i}"
    print("B-tree get 12:", bt[12])

    # Bloom filter
    bf = BloomFilter(expected_elements=100, false_positive_rate=0.01)
    bf.update(["apple", "banana", "cherry"])
    print("Bloom maybe 'apple':", "apple" in bf)
    print("Bloom maybe 'durian':", "durian" in bf)

    # Consistent hashing
    ring: ConsistentHashRing[str] = ConsistentHashRing(replicas=50)
    for host in ("db1", "db2", "db3"):
        ring.add_node(host)
    print("Key user-42 ->", ring.get_node("user-42"))

    # LRU
    lru: LRUCache[str, int] = LRUCache(2)
    lru["x"] = 1
    lru["y"] = 2
    _ = lru["x"]
    lru["z"] = 3
    print("LRU remaining items:", list(lru.items()))

    # LFU
    lfu: LFUCache[str, int] = LFUCache(2)
    lfu["a"] = 1
    lfu["b"] = 2
    _ = lfu["a"]
    lfu["c"] = 3
    print("LFU has 'a':", "a" in lfu)


if __name__ == "__main__":
    main()
