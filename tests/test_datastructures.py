"""
Tests and usage examples for datastructures package.

Run: pytest tests/test_datastructures.py -v
"""

from __future__ import annotations

import pytest

from datastructures import (
    BloomFilter,
    BTree,
    ConsistentHashRing,
    LFUCache,
    LRUCache,
    RedBlackTree,
)


class TestRedBlackTree:
    def test_insert_search_delete(self) -> None:
        t: RedBlackTree[int, str] = RedBlackTree()
        for i in range(100):
            t[i] = str(i)
        assert len(t) == 100
        for i in range(100):
            assert t[i] == str(i)
        for i in range(0, 100, 2):
            del t[i]
        assert len(t) == 50
        with pytest.raises(KeyError):
            _ = t[0]

    def test_sorted_order(self) -> None:
        t: RedBlackTree[int, int] = RedBlackTree()
        keys = [7, 2, 9, 1, 5]
        for k in keys:
            t[k] = k * 10
        assert list(t.items_inorder()) == [(1, 10), (2, 20), (5, 50), (7, 70), (9, 90)]


class TestBTree:
    def test_random_ops(self) -> None:
        bt: BTree[int, str] = BTree(min_degree=3)
        inserted = {}
        for i in range(200):
            bt[i] = f"v{i}"
            inserted[i] = f"v{i}"
        assert len(bt) == 200
        for k, v in inserted.items():
            assert bt[k] == v
        for i in range(0, 200, 3):
            del bt[i]
            inserted.pop(i, None)
        assert len(bt) == len(inserted)
        assert sorted(bt.items_inorder()) == sorted(inserted.items())


class TestBloomFilter:
    def test_no_false_negative(self) -> None:
        bf = BloomFilter(capacity=500, error_rate=0.02)
        items = [f"k{i}".encode() for i in range(400)]
        for x in items:
            bf.add(x)
        for x in items:
            assert x in bf

    def test_clear(self) -> None:
        bf = BloomFilter(size=100, hash_count=4)
        bf.add(b"a")
        bf.clear()
        assert len(bf) == 0


class TestConsistentHash:
    def test_balance_and_removal(self) -> None:
        ring: ConsistentHashRing[str] = ConsistentHashRing(replicas=50)
        nodes = ["a", "b", "c"]
        for n in nodes:
            ring.add_node(n)
        counts = {n: 0 for n in nodes}
        for i in range(3000):
            node = ring.get_node(str(i).encode())
            assert node in counts
            counts[node] += 1
        assert min(counts.values()) > 0
        ring.remove_node("b")
        for i in range(100):
            assert ring.get_node(str(i).encode()) in ("a", "c")


class TestLRU:
    def test_eviction_order(self) -> None:
        c: LRUCache[int, str] = LRUCache(2)
        c[1] = "a"
        c[2] = "b"
        _ = c[1]
        c[3] = "c"
        assert 2 not in c
        assert c[1] == "a"


class TestLFU:
    def test_eviction_by_frequency(self) -> None:
        c: LFUCache[int, str] = LFUCache(2)
        c[1] = "a"
        c[2] = "b"
        _ = c[1]
        _ = c[1]
        c[3] = "c"
        assert 2 not in c
        assert c[1] == "a"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
