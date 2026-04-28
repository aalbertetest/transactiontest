# Data structures reference

This document summarizes **time and space complexity**, **step-by-step behaviour**, **edge cases**, and links implementations under [`ds/`](../ds/).

---

## 1. Red–Black tree (`ds/red_black_tree.py`)

### Complexity

| Operation | Average | Worst case |
|-----------|---------|------------|
| Search | \(O(\log n)\) | \(O(\log n)\) |
| Insert | \(O(\log n)\) | \(O(\log n)\) |
| Delete | \(O(\log n)\) | \(O(\log n)\) |

**Space:** \(O(n)\) nodes; each node stores key, value, color, and three pointers.

### Invariants

- Every node is red or black; the root is black.
- Red nodes have only black children.
- Every path from a node to its descendant leaves has the same number of black nodes (“black height”).
- Leaves are implicit (`None`); we treat missing children as black leaves.

### Insert walkthrough

1. **BST insert** as if unbalanced, attaching a new **red** node (may violate “red parent”).
2. If parent is black, done.
3. If parent is red, fix using **recolor** and **rotations** (cases: uncle red → recolor grandparent and recurse; else rotate around grandparent to restore balance).
4. Force root to black after fix.

### Delete walkthrough

1. **BST delete** using successor/predecessor replacement when two children exist.
2. Track whether removed node was **black** (violates black-height if not compensated).
3. If replacement exists, run **`_fix_delete`** from it; if deleted leaf had **no child**, run **`_fix_double_black_nil`** at the parent slot (“double black” at absent child).
4. Ensure root is black.

### Edge cases

- **Empty tree:** insert creates a single black root.
- **Duplicate keys:** updates value in place (no duplicate nodes).
- **Delete missing key:** raises `KeyError`.
- **Delete black leaf with no child:** requires double-black fixup at parent’s missing-child pointer.

---

## 2. B-tree (`ds/btree.py`)

Minimum degree **`t` ≥ 2**: each node holds **at most** \(2t - 1\) keys and **at most** \(2t\) children; internal nodes have **at least** \(t\) children except root.

### Complexity

| Operation | Worst case |
|-----------|------------|
| Search | \(O(\log_t n)\) disk-oriented depth |
| Insert | \(O(\log_t n)\) |
| Delete | \(O(\log_t n)\) |

**Space:** \(O(n)\) keys distributed across nodes.

### Insert walkthrough

1. If root is full (\(2t-1\) keys), split root and grow height by one.
2. Descend to leaf; split full children on the way (**`_split_child`** promotes median).
3. Insert key into sorted leaf position.

### Delete walkthrough

1. Find key; if internal, replace with predecessor/successor or merge children then recurse.
2. If traversing to child with \< \(t\) keys, **borrow** from sibling or **merge** with sibling and parent separator.

### Edge cases

- **Root shrink:** if root becomes empty after merge, replace by sole child.
- **Duplicate insert:** raises `ValueError` (this implementation rejects duplicates).

---

## 3. Bloom filter (`ds/bloom_filter.py`)

### Complexity

| Operation | Time | Space |
|-----------|------|-------|
| Add / query | \(O(k)\) hash probes | \(O(m)\) counters |

\(m\) = bit-array length, \(k\) = hash functions; \(k \approx (m/n)\ln 2\) for target false-positive rate.

### Walkthrough

1. Hash item to \(k\) indices in \([0, m)\).
2. **Add:** increment each counter (capped).
3. **Query:** “possibly contains” iff **all** \(k\) counters are nonzero.

### Edge cases

- **False positives:** unavoidable for compact \(m\).
- **False negatives:** none for pure insert-only Bloom; **counting** filter `remove` can cause false negatives if you remove non-inserted items or counters saturate.
- **Hash collisions** across distinct items share buckets.

---

## 4. Consistent hashing (`ds/consistent_hash.py`)

### Complexity

| Operation | Time |
|-----------|------|
| Add/remove node | \(O(R \cdot \log V)\): \(R\) replicas, \(V\) virtual slots |
| Lookup | \(O(\log V)\) binary search on sorted tokens |

**Space:** \(O(V)\) for \(V = |\text{physical nodes}| \times R\) virtual nodes.

### Walkthrough

1. Each physical server gets **`replicas`** hashes on a ring \([0, 2^{64})\).
2. **`get_node(key)`:** hash key; choose first virtual token **≥** hash, wrap at end.
3. Adding/removing a server only moves keys between **neighbours** on average.

### Edge cases

- **Empty ring:** `get_node` raises `RuntimeError`.
- **Uneven load:** mitigate with higher **`replicas`**.
- **Hotspots:** depend on hash quality and placement.

---

## 5. LRU cache (`ds/cache.py` → `LRUCache`)

### Complexity

| Operation | Time |
|-----------|------|
| get / set | \(O(1)\) |

**Space:** \(O(\text{capacity})\).

### Walkthrough

- **`OrderedDict`:** on access, **`move_to_end`**; on eviction, **`popitem(last=False)`** removes LRU.

### Edge cases

- Capacity \< 1 rejected.
- Updating existing key does not count as “new” insertion for eviction order until touched again depending on implementation — here set refreshes position.

---

## 6. LFU cache (`ds/cache.py` → `LFUCache`)

### Complexity

| Operation | Time |
|-----------|------|
| get / set | \(O(1)\) average (dict + per-frequency lists) |

**Space:** \(O(\text{capacity})\).

### Walkthrough

- Keys grouped by **frequency** in **`OrderedDict`** lists (FIFO tie-break within frequency).
- **`get`/`[]`** increments frequency and moves key to next list.
- Eviction pops **least frequent**, oldest among ties.

### Edge cases

- **`__contains__`** must check **`_val`** only — membership must not “touch” frequency.
- After eviction, **`_min_freq`** is recomputed from remaining lists.

---

## Example usage (see `tests/test_ds.py`)

```python
from ds import (
    RedBlackTree, BTree, BloomFilter,
    ConsistentHashRing, LRUCache, LFUCache,
)

# Red-black map
rbt = RedBlackTree()
rbt["x"] = 1
assert rbt["x"] == 1

# B-tree set (degree t=2)
bt = BTree(t=2)
bt.insert(10)
assert 10 in bt

# Bloom filter
bf = BloomFilter(expected_n=1000, false_positive_rate=0.01)
bf.add("user:42")
assert bf.possibly_contains("user:42")

# Consistent hash
ring: ConsistentHashRing[str] = ConsistentHashRing(replicas=100)
ring.add_node("db1")
ring.add_node("db2")
node = ring.get_node("session-7")

# Caches
lru: LRUCache[int, str] = LRUCache(3)
lru[1] = "a"
lfu: LFUCache[int, str] = LFUCache(2)
lfu[1] = "a"
```

Run tests from repo root:

```bash
python3 -m unittest tests.test_ds -v
```
