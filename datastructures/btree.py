"""
B-Tree (generalized search tree for block-oriented storage).

Parameters
----------
`degree` (often written *t* in textbooks): minimum degree **≥ 2**.
- Max keys per node: `2 * degree - 1`
- Min keys (non-root): `degree - 1`
- Max children: `2 * degree`

Complexity (n keys, degree t)
-----------------------------
Let h = tree height. Height is O(log_t n) because each node branches up to 2t children.

- Search: O(h) = O(log_t n) comparisons per level; **O(log n)** in big-O base omitted (same as O(log_t n)).
- Insert: O(h) splits along one root-to-leaf path.
- Delete: O(h); may merge/borrow along one path.

Space: O(n) keys plus O(n/t) internal metadata (children pointers); auxiliary rotation arrays O(t) per node.

Walkthrough — search
--------------------
Start at root; find smallest index i with key ≤ search key (binary search or linear for small t);
if equal, hit; else recurse into child i.

Walkthrough — insert
--------------------
Always insert into a leaf. If leaf would overflow (> 2t-1 keys), split **before** descending
(split on the way down if full) so each insertion stays single-pass.

Walkthrough — delete
--------------------
If key not in leaf, descend; ensure child along path has ≥ t keys (borrow/merge) **before**
recursing (except merge may reduce root — handled separately).

Edge cases
----------
- Empty tree: first insert creates root with one key.
- Root may have fewer than t-1 keys (only exception).
- Duplicate keys: insert **updates** the stored value (same as a mapping).
"""

from __future__ import annotations

from bisect import bisect_left
from dataclasses import dataclass, field
from typing import Generic, Iterator, List, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _BTreeNode(Generic[K, V]):
    keys: List[K] = field(default_factory=list)
    values: List[V] = field(default_factory=list)
    children: List["_BTreeNode[K, V]"] = field(default_factory=list)
    leaf: bool = True


class BTree(Generic[K, V]):
    """
    In-memory B-tree mapping comparable keys to values.

    `degree` is the minimum degree t (≥ 2).
    """

    def __init__(self, degree: int = 3) -> None:
        if degree < 2:
            raise ValueError("degree must be >= 2")
        self.degree = degree
        self._root = _BTreeNode[K, V]()
        self._len = 0

    def __len__(self) -> int:
        return self._len

    def __contains__(self, key: object) -> bool:
        return self._search(self._root, key) is not None

    def __getitem__(self, key: K) -> V:
        r = self._search(self._root, key)
        if r is None:
            raise KeyError(key)
        node, i = r
        return node.values[i]

    def __setitem__(self, key: K, value: V) -> None:
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        self.delete(key)

    def _search(self, node: _BTreeNode[K, V], key: K) -> Optional[Tuple[_BTreeNode[K, V], int]]:
        i = bisect_left(node.keys, key)
        if i < len(node.keys) and node.keys[i] == key:
            return node, i
        if node.leaf:
            return None
        return self._search(node.children[i], key)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        r = self._search(self._root, key)
        return default if r is None else r[0].values[r[1]]

    def insert(self, key: K, value: V) -> None:
        """Insert or update key."""
        max_keys = 2 * self.degree - 1
        if len(self._root.keys) == max_keys:
            new_root = _BTreeNode[K, V](leaf=False)
            new_root.children.append(self._root)
            self._split_child(new_root, 0)
            self._root = new_root
        self._insert_non_full(self._root, key, value)

    def _split_child(self, parent: _BTreeNode[K, V], index: int) -> None:
        t = self.degree
        y = parent.children[index]
        z = _BTreeNode[K, V](leaf=y.leaf)
        mid = t - 1
        mid_key = y.keys[mid]
        mid_val = y.values[mid]
        z.keys = y.keys[mid + 1 :]
        z.values = y.values[mid + 1 :]
        y.keys = y.keys[:mid]
        y.values = y.values[:mid]
        if not y.leaf:
            z.children = y.children[mid + 1 :]
            y.children = y.children[: mid + 1]
        parent.keys.insert(index, mid_key)
        parent.values.insert(index, mid_val)
        parent.children.insert(index + 1, z)

    def _insert_non_full(self, node: _BTreeNode[K, V], key: K, value: V) -> None:
        max_keys = 2 * self.degree - 1
        i = bisect_left(node.keys, key)
        if i < len(node.keys) and node.keys[i] == key:
            node.values[i] = value
            return
        if node.leaf:
            node.keys.insert(i, key)
            node.values.insert(i, value)
            self._len += 1
            return
        if len(node.children[i].keys) == max_keys:
            self._split_child(node, i)
            if i < len(node.keys) and key == node.keys[i]:
                node.values[i] = value
                return
            if key > node.keys[i]:
                i += 1
        self._insert_non_full(node.children[i], key, value)

    def delete(self, key: K) -> None:
        """Remove key; raises KeyError if absent."""
        if not self._root.keys:
            raise KeyError(key)
        self._delete(self._root, key)
        if not self._root.keys and not self._root.leaf:
            self._root = self._root.children[0]

    def _delete(self, node: _BTreeNode[K, V], key: K) -> None:
        i = bisect_left(node.keys, key)

        if node.leaf:
            if i < len(node.keys) and node.keys[i] == key:
                node.keys.pop(i)
                node.values.pop(i)
                self._len -= 1
            else:
                raise KeyError(key)
            return

        if i < len(node.keys) and node.keys[i] == key:
            self._delete_internal(node, i)
            return

        ci = i if i < len(node.children) else len(node.children) - 1
        ci = self._ensure_child_fill(node, ci)
        self._delete(node.children[ci], key)

    def _delete_internal(self, node: _BTreeNode[K, V], index: int) -> None:
        min_keys = self.degree - 1
        left = node.children[index]
        right = node.children[index + 1]
        if len(left.keys) > min_keys:
            pred_k, pred_v = self._pop_max(left)
            node.keys[index] = pred_k
            node.values[index] = pred_v
            self._len -= 1
        elif len(right.keys) > min_keys:
            succ_k, succ_v = self._pop_min(right)
            node.keys[index] = succ_k
            node.values[index] = succ_v
            self._len -= 1
        else:
            merge_key = node.keys[index]
            self._merge_children(node, index)
            self._delete(node.children[index], merge_key)

    def _pop_max(self, node: _BTreeNode[K, V]) -> Tuple[K, V]:
        if node.leaf:
            return node.keys.pop(), node.values.pop()
        ci = self._ensure_child_fill(node, len(node.children) - 1)
        return self._pop_max(node.children[ci])

    def _pop_min(self, node: _BTreeNode[K, V]) -> Tuple[K, V]:
        if node.leaf:
            k = node.keys.pop(0)
            v = node.values.pop(0)
            return k, v
        ci = self._ensure_child_fill(node, 0)
        return self._pop_min(node.children[ci])

    def _merge_children(self, parent: _BTreeNode[K, V], index: int) -> None:
        y = parent.children[index]
        z = parent.children[index + 1]
        sep_k = parent.keys.pop(index)
        sep_v = parent.values.pop(index)
        parent.children.pop(index + 1)
        y.keys.append(sep_k)
        y.values.append(sep_v)
        y.keys.extend(z.keys)
        y.values.extend(z.values)
        if not y.leaf:
            y.children.extend(z.children)

    def _ensure_child_fill(self, parent: _BTreeNode[K, V], index: int) -> int:
        """Ensure parent.children[index] has at least degree-1 keys; return (possibly shifted) index."""
        t = self.degree
        min_keys = t - 1
        if len(parent.children[index].keys) >= min_keys:
            return index
        if index > 0 and len(parent.children[index - 1].keys) > min_keys:
            self._rotate_right(parent, index)
            return index
        if index < len(parent.children) - 1 and len(parent.children[index + 1].keys) > min_keys:
            self._rotate_left(parent, index)
            return index
        if index < len(parent.children) - 1:
            self._merge_children(parent, index)
            return index
        self._merge_children(parent, index - 1)
        return index - 1

    def _rotate_right(self, parent: _BTreeNode[K, V], index: int) -> None:
        """Borrow from left sibling into child at index."""
        left = parent.children[index - 1]
        child = parent.children[index]
        sep_idx = index - 1
        child.keys.insert(0, parent.keys[sep_idx])
        child.values.insert(0, parent.values[sep_idx])
        if not child.leaf:
            child.children.insert(0, left.children.pop())
        parent.keys[sep_idx] = left.keys.pop()
        parent.values[sep_idx] = left.values.pop()

    def _rotate_left(self, parent: _BTreeNode[K, V], index: int) -> None:
        """Borrow from right sibling into child at index."""
        child = parent.children[index]
        right = parent.children[index + 1]
        sep_idx = index
        child.keys.append(parent.keys[sep_idx])
        child.values.append(parent.values[sep_idx])
        if not child.leaf:
            child.children.append(right.children.pop(0))
        parent.keys[sep_idx] = right.keys.pop(0)
        parent.values[sep_idx] = right.values.pop(0)

    def items(self) -> Iterator[Tuple[K, V]]:
        yield from self._items_node(self._root)

    def _items_node(self, node: _BTreeNode[K, V]) -> Iterator[Tuple[K, V]]:
        if node.leaf:
            yield from zip(node.keys, node.values)
            return
        for i in range(len(node.keys)):
            yield from self._items_node(node.children[i])
            yield node.keys[i], node.values[i]
        yield from self._items_node(node.children[-1])


def demo_btree() -> None:
    b: BTree[int, str] = BTree(degree=2)
    for x in range(10):
        b[x] = str(x)
    assert b[5] == "5"
    del b[5]
    assert 5 not in b


if __name__ == "__main__":
    demo_btree()
