# Data structures: complexity and walkthroughs

This document accompanies `datastructures/` implementations: red-black trees, B-trees, Bloom filters, consistent hashing, LRU and LFU caches.

## Red-black tree (`red_black_tree.py`)

**Operations:** `insert`, `delete`, `search` / `__getitem__`.

| Operation | Time (worst) | Space auxiliary |
|-----------|----------------|-----------------|
| Search    | O(log n)       | O(1)            |
| Insert    | O(log n)       | O(1)            |
| Delete    | O(log n)       | O(1)            |
| In-order scan | O(n)      | O(h) stack if recursive |

**Space:** O(n) total for n keys.

**Walkthrough (insert):** BST insert as RED; fix double-red violations by rotations and recoloring up to root; force root BLACK.

**Walkthrough (delete):** Standard transplant plus delete-fixup when a BLACK node was removed (borrow or rotate sibling cases).

**Edge cases:** Empty tree; duplicate key updates value only; NIL sentinel must stay BLACK; root remains BLACK after fixup.

---

## B-tree (`b_tree.py`)

Minimum degree `t` (default 2). Keys sorted per node; internal nodes have `len(keys)+1` children.

| Operation | Time | Notes |
|-----------|------|--------|
| Search | O(t · h), h = O(log_t n) | Scan inside node O(t) |
| Insert | same | Split full nodes on path |
| Delete | same | Borrow or merge to keep at least t−1 keys per non-root node |

**Space:** O(n).

**Walkthrough (insert):** If root full, split root (height increases). Descend; split child if full before continuing.

**Walkthrough (delete):** Remove from leaf or swap with predecessor or successor; merge or borrow so children stay valid.

**Edge cases:** Root may hold fewer than t−1 keys; empty tree; `min_degree` less than 2 is rejected.

---

## Bloom filter (`bloom_filter.py`)

**Operations:** `add`, `maybe_contains` / `in`.

| Operation | Time | Space |
|-----------|------|-------|
| Add | O(k) hash probes | O(m) bits |
| Query | O(k) | — |

**False positives:** Approximate probability after n inserts: (1 − e^(−kn/m))^k with m bits and k hashes.

**False negatives:** None for items actually inserted.

**Walkthrough:** Derive k positions from two 64-bit hashes; OR bits on insert; AND on query.

**Edge cases:** Duplicate hash positions in one `add` are deduped so bit-setting matches one logical insert.

---

## Consistent hashing (`consistent_hash.py`)

**Operations:** `add_node`, `remove_node`, `get_node`, `get_n_nodes`.

| Operation | Time | Space |
|-----------|------|-------|
| Add or remove vnode | O(V) sorted list ops | O(V) |
| Lookup | O(log V) bisect | — |

V equals replicas times physical nodes.

**Walkthrough:** Place virtual nodes on a ring; map key to first vnode at or after key hash (wrap around).

**Edge cases:** Empty ring returns None; unknown physical node on remove raises KeyError; rarely two virtual hashes collide.

---

## LRU cache (`lru_cache.py`)

| Operation | Time | Space |
|-----------|------|-------|
| get / set | O(1) amortized | O(capacity) |

**Walkthrough:** OrderedDict `move_to_end` on access; pop left when full.

**Edge cases:** Capacity one; updating existing key does not evict.

---

## LFU cache (`lfu_cache.py`)

| Operation | Time | Space |
|-----------|------|-------|
| get / set | O(1) average | O(capacity) |

Frequency buckets use OrderedDict for LRU among ties.

**Walkthrough:** Bump frequency on hit; evict oldest key in the smallest frequency bucket.

**Edge cases:** Maintain `min_freq` when buckets empty after bump or eviction.

---

## Example usage

```python
from datastructures import RedBlackTree, BTree, BloomFilter
from datastructures import ConsistentHashRing, LRUCache, LFUCache

t = RedBlackTree()
t[10] = "x"

bf = BloomFilter(capacity=1000, error_rate=0.001)
bf.add(b"user:42")

ring = ConsistentHashRing[str](replicas=100)
ring.add_node("db-east")
node = ring.get_node(b"payload")

cache = LRUCache(128)
cache["a"] = 1
```

Run tests: `pytest tests/test_datastructures.py -v`.
