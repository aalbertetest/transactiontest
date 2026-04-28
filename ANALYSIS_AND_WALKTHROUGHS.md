# Data structures: complexity, walkthroughs, and edge cases

This document accompanies the Python implementations in `algorithms/`.

## Red-black tree (`red_black_tree.py`)

**Model:** Classic red-black BST with sentinel `NIL` (CLRS). Each node stores key, value, left, right, parent, and color.

**Time:** Search, insert, and delete are **O(log n)** worst case. In-order traversal of all keys is **O(n)**.

**Space:** **O(n)** nodes; each node holds two child references, parent, key, value, and color.

### Walkthrough: insert

1. BST-insert the new node as **red** (may violate red-red or root-red).
2. If parent is black, done.
3. If parent is red, the uncle determines the case:
   - Uncle red: recolor parent, uncle, and grandparent; move cursor to grandparent and repeat.
   - Uncle black + triangle: rotate parent to align into a line.
   - Uncle black + line: rotate grandparent, recolor parent and grandparent.
4. Force **root black** after fixup.

### Walkthrough: delete

1. Standard BST delete with transplant; track the color of the node actually removed (`y`).
2. If a black node was removed, a black deficit appears on the extra child `x`; run **delete-fixup** (mirror symmetric cases) pushing extra black up the tree or borrowing from sibling.

### Edge cases

- **Empty tree:** root is `NIL`; deletes raise `KeyError`.
- **Duplicate key on `put`:** updates value only; size unchanged.
- **`None` as value:** supported; `get(key, default)` cannot distinguish “missing” from “stored `None`” if you use `default=None`—use `__contains__` or catch `KeyError` on `__getitem__`.

---

## B-tree (`btree.py`)

**Model:** Parameter **t ≥ 2** (minimum degree). Internal nodes have between **t−1** and **2t−1** keys (except root may have fewer). Children interleave keys.

**Time:** Each node visit scans **O(t)** keys; height **O(log_t n)** ⇒ search/insert/delete **O(t log_t n)**. For fixed `t`, treat as **O(log n)** with a larger constant than binary trees.

**Space:** **O(n)** keys and values plus child pointers.

### Walkthrough: insert

1. If root is full (**2t−1** keys), split root: new empty root with two children; split old root’s median up.
2. Descend into appropriate child; split any full child on the way (**preemptive split**).
3. Insert into leaf (sorted keys) or update existing key.

### Walkthrough: delete

1. Locate key. In a leaf: remove key.
2. In internal node: replace with predecessor or successor from a child with enough keys, or merge children and recurse.
3. Before descending, if child has **t−2** keys (below minimum), **borrow** from sibling or **merge** with sibling and parent separator.

### Edge cases

- **t = 2** (2-3-4 style): smallest sensible degree; more splits/merges.
- **Large t:** shorter tree, wider nodes, higher per-node scan cost.
- **Duplicate insert:** value overwrite; size unchanged.

---

## Bloom filter (`bloom_filter.py`)

**Model:** Bit array of length **m**; **k** independent hash positions per item (here: double hashing from SHA-256 chunks).

**Time:** Add and query **O(k)** with **k = O(1)** for fixed expected load.

**Space:** **O(m)** bits with **m ≈ −n ln p / (ln 2)²** for **n** expected elements and target false-positive rate **p**.

### Walkthrough: add

1. Hash item to **k** indices in `[0, m)`.
2. Set those bits to 1.

### Walkthrough: query

1. Compute the same **k** indices; return true iff **all** bits are 1.

### Edge cases

- **No deletion:** standard Bloom filters have false positives; deleting can create **false negatives** unless you use a counting variant (not implemented here).
- **Saturation:** after many more inserts than designed **n**, false-positive rate rises (`estimated_fpp()`).
- **Collisions of unrelated items:** any combination of prior inserts can set bits; unrelated keys may still test positive.

---

## Consistent hashing (`consistent_hashing.py`)

**Model:** Hash ring **0 … 2⁶⁴−1** (MD5 digest truncated to 64 bits). Each physical node occupies **replicas × weight** virtual positions. Lookup walks clockwise from `hash(key)` to first virtual node.

**Time:** Add/remove node **O(R)** for **R** virtual nodes of that server; lookup **O(log(N·replicas))** binary search.

**Space:** **O(N · replicas · average weight)** sorted positions.

### Walkthrough: `get_node(key)`

1. Compute ring position `h(key)`.
2. Binary search first virtual position **≥** `h(key)`; wrap if past end.
3. Return owning physical node.

### Edge cases

- **Empty ring:** `get_node` raises `RuntimeError`.
- **Single node:** all keys map to it.
- **Low replicas:** uneven load; increase replicas for smoother distribution.
- **Duplicate add:** `add_node` rejects duplicates; remove then re-add to change weight.

---

## LRU cache (`lru_cache.py`)

**Model:** `OrderedDict` for **move-to-end** on access and **popitem(last=False)** for LRU eviction.

**Time:** **O(1)** amortized get/put (CPython `OrderedDict`).

**Space:** **O(capacity)** entries.

### Walkthrough: `get`

1. If missing, return default.
2. If TTL expired, delete and return default.
3. Otherwise move key to MRU end and return value.

### Walkthrough: `put`

1. If key exists, update and refresh order.
2. If over capacity after insert, evict LRU (front).

### Edge cases

- **`None` values:** supported; `__contains__` checks structure after TTL check.
- **TTL 0 or very small:** entries expire immediately on next clock read.
- **Capacity 1:** every new distinct key evicts the previous.

---

## LFU cache (`lfu_cache.py`)

**Model:** Per-frequency buckets (`OrderedDict`) for FIFO among same frequency; map key → frequency and value.

**Time:** **O(1)** get/put amortized.

**Space:** **O(capacity)**.

### Walkthrough: `get`

1. Increment key’s frequency: remove from old bucket, append to `freq+1` bucket.
2. Update `min_freq` if the lowest bucket emptied.

### Walkthrough: `put` (new key at capacity)

1. Evict **FIFO** from bucket `min_freq` (least frequent, oldest among them).
2. Insert new key at frequency 1.

### Edge cases

- **Tie on frequency:** oldest in that frequency bucket evicted (LFU with LRU tie-break).
- **Updating existing key:** does not increase size; frequency increases only on `get` / repeated `put` updates paths that call `_touch`.

---

## Running tests

```bash
python3 -m unittest discover -s tests -p "test_*.py" -v
```
