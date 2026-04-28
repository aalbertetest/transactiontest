"""Tests for ds package."""

import unittest

from ds import BloomFilter, BTree, ConsistentHashRing, LFUCache, LRUCache, RedBlackTree


class TestRedBlackTree(unittest.TestCase):
    def test_insert_search_delete(self) -> None:
        t = RedBlackTree()
        for i in range(100):
            t[i] = i * 2
        self.assertEqual(t[50], 100)
        for i in range(100):
            self.assertEqual(t[i], i * 2)
        for i in range(0, 100, 2):
            del t[i]
        for i in range(0, 100, 2):
            with self.assertRaises(KeyError):
                _ = t[i]
        for i in range(1, 100, 2):
            self.assertEqual(t[i], i * 2)

    def test_sorted_items(self) -> None:
        t = RedBlackTree()
        keys = [5, 2, 8, 1, 9]
        for k in keys:
            t[k] = k
        self.assertEqual(list(t.keys()), [1, 2, 5, 8, 9])


class TestBTree(unittest.TestCase):
    def test_order_t2(self) -> None:
        bt = BTree(t=2)
        vals = list(range(50))
        for v in vals:
            bt.insert(v)
        for v in vals:
            self.assertIn(v, bt)
        for v in vals[::2]:
            bt.delete(v)
        for v in vals[::2]:
            self.assertNotIn(v, bt)
        self.assertEqual(list(bt.items()), sorted(vals[1::2]))

    def test_duplicate_raises(self) -> None:
        bt = BTree(t=2)
        bt.insert(1)
        with self.assertRaises(ValueError):
            bt.insert(1)


class TestBloomFilter(unittest.TestCase):
    def test_membership(self) -> None:
        bf = BloomFilter(expected_n=1000, false_positive_rate=0.01)
        for i in range(500):
            bf.add(f"k{i}")
        for i in range(500):
            self.assertTrue(bf.possibly_contains(f"k{i}"))
        false_pos = sum(1 for j in range(500, 2000) if bf.possibly_contains(f"k{j}"))
        self.assertLess(false_pos, 50)


class TestConsistentHash(unittest.TestCase):
    def test_ring(self) -> None:
        r: ConsistentHashRing[str] = ConsistentHashRing(replicas=50)
        r.add_node("a")
        r.add_node("b")
        counts = {"a": 0, "b": 0}
        for i in range(2000):
            counts[r.get_node(f"key{i}")] += 1
        self.assertTrue(all(c > 0 for c in counts.values()))
        r.remove_node("a")
        for i in range(100):
            self.assertEqual(r.get_node(f"x{i}"), "b")


class TestCaches(unittest.TestCase):
    def test_lru(self) -> None:
        c: LRUCache[int, str] = LRUCache(2)
        c[1] = "a"
        c[2] = "b"
        c[1]
        c[3] = "c"
        self.assertNotIn(2, c)
        self.assertEqual(c[1], "a")

    def test_lfu(self) -> None:
        c: LFUCache[int, str] = LFUCache(2)
        c[1] = "a"
        c[2] = "b"
        c[1]
        c[1]
        c[3] = "c"
        self.assertNotIn(2, c)


if __name__ == "__main__":
    unittest.main()
