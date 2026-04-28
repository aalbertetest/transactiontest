"""Tests for algorithms package."""

from __future__ import annotations

import random
import time
import unittest

from algorithms.bloom_filter import BloomFilter
from algorithms.btree import BTree
from algorithms.consistent_hashing import ConsistentHashRing
from algorithms.lfu_cache import LFUCache
from algorithms.lru_cache import LRUCache
from algorithms.red_black_tree import RedBlackTree, _Color, _Node


class TestRedBlackTree(unittest.TestCase):
    def test_insert_delete_random(self) -> None:
        for n in (0, 1, 20, 200):
            for seed in range(25):
                random.seed(seed)
                keys = list(range(n))
                random.shuffle(keys)
                t: RedBlackTree[int, int] = RedBlackTree()
                ref: dict[int, int] = {}
                for k in keys:
                    t[k] = k * 2
                    ref[k] = k * 2
                self.assertEqual(len(t), len(ref))
                for k in range(n):
                    self.assertEqual(t[k], ref[k])
                random.shuffle(keys)
                for k in keys:
                    del t[k]
                    del ref[k]
                self.assertEqual(len(t), 0)

    def _check_rb(self, t: RedBlackTree[int, int]) -> None:
        nil = t._nil

        def black_height(x: _Node[int, int]) -> int | None:
            if x is nil:
                return 0
            if x.color == _Color.RED:
                if x.left.color == _Color.RED or x.right.color == _Color.RED:
                    return None
            lb = black_height(x.left)
            rb = black_height(x.right)
            if lb is None or rb is None or lb != rb:
                return None
            return lb + (1 if x.color == _Color.BLACK else 0)

        if t._root is not nil and t._root.color != _Color.BLACK:
            self.fail("root must be black")
        h = black_height(t._root)
        self.assertIsNotNone(h)

    def test_rb_invariants_after_ops(self) -> None:
        t: RedBlackTree[int, int] = RedBlackTree()
        for i in range(50):
            t[i] = i
            self._check_rb(t)
        for i in range(0, 50, 2):
            del t[i]
            self._check_rb(t)


class TestBTree(unittest.TestCase):
    def test_fuzz_vs_dict(self) -> None:
        for t_deg in (2, 4):
            for seed in range(15):
                random.seed(seed)
                n = 80
                keys = list(range(n))
                random.shuffle(keys)
                bt = BTree(t_deg)
                ref: dict[int, int] = {}
                for k in keys:
                    bt[k] = k
                    ref[k] = k
                self.assertEqual(len(bt), n)
                random.shuffle(keys)
                for k in keys:
                    del bt[k]
                    del ref[k]
                self.assertEqual(len(bt), 0)


class TestBloomFilter(unittest.TestCase):
    def test_membership(self) -> None:
        bf = BloomFilter(1000, 0.01)
        items = [b"a", b"b", b"hello"]
        for x in items:
            bf.add(x)
        for x in items:
            self.assertTrue(bf.possibly_contains(x))
        self.assertFalse(bf.possibly_contains(b"not-in-set"))

    def test_false_positives_bounded_loosely(self) -> None:
        bf = BloomFilter(500, 0.001)
        present = {f"k{i}".encode() for i in range(500)}
        bf.update(present)
        fp = 0
        trials = 5000
        for j in range(trials):
            cand = f"absent{j}".encode()
            if cand in present:
                continue
            if bf.possibly_contains(cand):
                fp += 1
        self.assertLess(fp / trials, 0.08)


class TestConsistentHash(unittest.TestCase):
    def test_distribution_and_removal(self) -> None:
        ring: ConsistentHashRing[str] = ConsistentHashRing(replicas=80)
        nodes = ["a", "b", "c"]
        for n in nodes:
            ring.add_node(n)
        counts = {n: 0 for n in nodes}
        for i in range(3000):
            counts[ring.get_node(f"key-{i}")] += 1
        self.assertTrue(min(counts.values()) > 0)
        ring.remove_node("b")
        self.assertEqual(len(ring), 2)
        for i in range(100):
            self.assertIn(ring.get_node(f"k{i}"), ("a", "c"))

    def test_empty_ring(self) -> None:
        ring: ConsistentHashRing[str] = ConsistentHashRing()
        with self.assertRaises(RuntimeError):
            ring.get_node("x")


class TestLRU(unittest.TestCase):
    def test_eviction_order(self) -> None:
        c: LRUCache[str, int] = LRUCache(2)
        c["a"] = 1
        c["b"] = 2
        _ = c["a"]
        c["c"] = 3
        self.assertNotIn("b", c)
        self.assertEqual(c["a"], 1)

    def test_ttl(self) -> None:
        c: LRUCache[str, int] = LRUCache(10, ttl_seconds=0.05)
        c["x"] = 1
        self.assertEqual(c["x"], 1)
        time.sleep(0.08)
        with self.assertRaises(KeyError):
            _ = c["x"]


class TestLFU(unittest.TestCase):
    def test_evict_least_frequent(self) -> None:
        c: LFUCache[str, int] = LFUCache(2)
        c["a"] = 1
        c["b"] = 2
        _ = c["a"]
        _ = c["a"]
        c["c"] = 3
        self.assertNotIn("b", c)
        self.assertEqual(c["a"], 1)


if __name__ == "__main__":
    unittest.main()
