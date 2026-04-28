"""Tests and usage examples for datastructures package."""

from __future__ import annotations

import random
import unittest

from datastructures.bloom_filter import BloomFilter
from datastructures.btree import BTree
from datastructures.caches import LFUCache, LRUCache
from datastructures.consistent_hash import ConsistentHashRing
from datastructures.red_black_tree import RedBlackTree


class TestRedBlackTree(unittest.TestCase):
    def test_insert_delete_invariants_random(self) -> None:
        for _ in range(5):
            t: RedBlackTree[int, int] = RedBlackTree()
            keys = list(range(50))
            random.shuffle(keys)
            for k in keys:
                t[k] = k * 2
            self.assertEqual(len(t), 50)
            for k in keys:
                self.assertEqual(t[k], k * 2)
            random.shuffle(keys)
            for k in keys:
                del t[k]
            self.assertEqual(len(t), 0)

    def test_duplicate_key_updates(self) -> None:
        t: RedBlackTree[str, int] = RedBlackTree()
        t["x"] = 1
        t["x"] = 2
        self.assertEqual(t["x"], 2)
        self.assertEqual(len(t), 1)


class TestBTree(unittest.TestCase):
    def test_degree2_random(self) -> None:
        for degree in (2, 3, 5):
            b: BTree[int, int] = BTree(degree=degree)
            keys = list(range(200))
            random.shuffle(keys)
            for k in keys:
                b[k] = k * 3
            self.assertEqual(len(b), 200)
            for k in keys:
                self.assertEqual(b[k], k * 3)
            random.shuffle(keys)
            for k in keys:
                del b[k]
            self.assertEqual(len(b), 0)

    def test_missing_raises(self) -> None:
        b: BTree[int, int] = BTree(degree=2)
        b[1] = 1
        with self.assertRaises(KeyError):
            _ = b[2]

    def test_items_sorted(self) -> None:
        b: BTree[int, str] = BTree(degree=2)
        for x in [5, 2, 8, 1]:
            b[x] = str(x)
        self.assertEqual(list(b.items()), [(1, "1"), (2, "2"), (5, "5"), (8, "8")])


class TestBloomFilter(unittest.TestCase):
    def test_no_false_negatives(self) -> None:
        bf = BloomFilter.from_size(4096, 6)
        added = [f"k{i}".encode() for i in range(500)]
        for a in added:
            bf.add(a)
        for a in added:
            self.assertTrue(bf.might_contain(a))

    def test_estimated_fpp_monotone(self) -> None:
        bf = BloomFilter.from_size(1024, 4)
        self.assertGreaterEqual(bf.estimated_fpp(), 0.0)
        bf.add(b"x")
        p1 = bf.estimated_fpp()
        bf.add(b"y")
        self.assertGreaterEqual(bf.estimated_fpp(), p1)


class TestConsistentHash(unittest.TestCase):
    def test_empty_raises(self) -> None:
        ring: ConsistentHashRing[str] = ConsistentHashRing()
        with self.assertRaises(RuntimeError):
            ring.get_node(b"k")

    def test_membership_stable(self) -> None:
        ring: ConsistentHashRing[int] = ConsistentHashRing(replicas=50)
        ring.add_nodes([1, 2, 3])
        n = ring.get_node(b"hello")
        self.assertEqual(ring.get_node(b"hello"), n)

    def test_k_nodes_distinct(self) -> None:
        ring: ConsistentHashRing[str] = ConsistentHashRing(replicas=100)
        ring.add_nodes(["a", "b", "c", "d"])
        nodes = ring.get_nodes(b"x", 3)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(len(set(nodes)), 3)


class TestLRU(unittest.TestCase):
    def test_eviction_order(self) -> None:
        c: LRUCache[int, str] = LRUCache(2)
        c[1] = "a"
        c[2] = "b"
        _ = c[1]
        c[3] = "c"
        self.assertNotIn(2, c)
        self.assertIn(1, c)
        self.assertIn(3, c)

    def test_zero_capacity(self) -> None:
        c: LRUCache[int, str] = LRUCache(0)
        c[1] = "x"
        self.assertEqual(len(c), 0)


class TestLFU(unittest.TestCase):
    def test_evicts_least_frequent(self) -> None:
        c: LFUCache[int, str] = LFUCache(2)
        c[1] = "a"
        c[2] = "b"
        _ = c[1]
        _ = c[1]
        c[3] = "c"
        self.assertNotIn(2, c)
        self.assertIn(1, c)

    def test_set_updates_then_counts(self) -> None:
        c: LFUCache[int, str] = LFUCache(2)
        c[1] = "a"
        c[2] = "b"
        c[1] = "aa"
        _ = c[1]
        c[3] = "c"
        self.assertNotIn(2, c)


def load_tests(loader: unittest.TestLoader, tests: unittest.TestSuite, ignore: object) -> unittest.TestSuite:
    return tests


if __name__ == "__main__":
    unittest.main()
