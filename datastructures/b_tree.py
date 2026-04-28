"""
B-tree with minimum degree `min_degree` (CLRS notation t >= 2).

Each node holds at most `2*t - 1` keys; non-root nodes hold at least `t - 1` keys.

Time: search/insert/delete O(t * h) with h = O(log_t n). Space O(n).
"""

from __future__ import annotations

from typing import Generic, Iterator, List, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _BTreeNode(Generic[K, V]):
    __slots__ = ("keys", "values", "children", "leaf")

    def __init__(self, leaf: bool) -> None:
        self.keys: List[K] = []
        self.values: List[V] = []
        self.children: List["_BTreeNode[K, V]"] = []
        self.leaf = leaf


class BTree(Generic[K, V]):
    """
    Ordered map backed by a B-tree.

    `min_degree` (t): internal nodes (except root) have between t-1 and 2t-1 keys.
    """

    def __init__(self, min_degree: int = 2) -> None:
        if min_degree < 2:
            raise ValueError("min_degree must be at least 2")
        self._t = min_degree
        self._root = _BTreeNode[K, V](True)
        self._size = 0

    @property
    def min_degree(self) -> int:
        return self._t

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: object) -> bool:
        node = self._root
        while True:
            i = _key_index(node, key)  # type: ignore[arg-type]
            if i < len(node.keys) and key == node.keys[i]:
                return True
            if node.leaf:
                return False
            node = node.children[i]

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        node = self._root
        while True:
            i = _key_index(node, key)
            if i < len(node.keys) and key == node.keys[i]:
                return node.values[i]
            if node.leaf:
                return default
            node = node.children[i]

    def __getitem__(self, key: K) -> V:
        node = self._root
        while True:
            i = _key_index(node, key)
            if i < len(node.keys) and key == node.keys[i]:
                return node.values[i]
            if node.leaf:
                raise KeyError(key)
            node = node.children[i]

    def __setitem__(self, key: K, value: V) -> None:
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        self.delete(key)

    def insert(self, key: K, value: V) -> None:
        """Insert or update. O(t * height)."""
        t = self._t
        root = self._root
        if len(root.keys) == 2 * t - 1:
            new_root = _BTreeNode[K, V](False)
            new_root.children.append(root)
            self._split_child(new_root, 0)
            self._root = new_root
        self._insert_nonfull(self._root, key, value)

    def delete(self, key: K) -> None:
        """Remove key. O(t * height). Raises KeyError if missing."""
        if self._size == 0:
            raise KeyError(key)
        self._delete_key(self._root, key)
        if len(self._root.keys) == 0 and not self._root.leaf:
            self._root = self._root.children[0]

    def _insert_nonfull(self, node: _BTreeNode[K, V], key: K, value: V) -> None:
        t = self._t
        if node.leaf:
            i = _key_index(node, key)
            if i < len(node.keys) and node.keys[i] == key:
                node.values[i] = value
                return
            node.keys.insert(i, key)
            node.values.insert(i, value)
            self._size += 1
            return
        i = _key_index(node, key)
        if i < len(node.keys) and node.keys[i] == key:
            node.values[i] = value
            return
        if len(node.children[i].keys) == 2 * t - 1:
            self._split_child(node, i)
            if key > node.keys[i]:
                i += 1
        self._insert_nonfull(node.children[i], key, value)

    def _split_child(self, parent: _BTreeNode[K, V], i: int) -> None:
        t = self._t
        full = parent.children[i]
        mid = t - 1
        right = _BTreeNode[K, V](full.leaf)
        right.keys = full.keys[t : 2 * t - 1]
        right.values = full.values[t : 2 * t - 1]
        if not full.leaf:
            right.children = full.children[t : 2 * t]
        promote_k = full.keys[mid]
        promote_v = full.values[mid]
        full.keys = full.keys[:mid]
        full.values = full.values[:mid]
        if not full.leaf:
            full.children = full.children[:t]
        parent.keys.insert(i, promote_k)
        parent.values.insert(i, promote_v)
        parent.children.insert(i + 1, right)

    def _delete_key(self, node: _BTreeNode[K, V], key: K) -> None:
        t = self._t
        i = _key_index(node, key)
        if i < len(node.keys) and node.keys[i] == key:
            return self._delete_from_node(node, i)
        if node.leaf:
            raise KeyError(key)
        self._fill_child(node, i)
        i = _key_index(node, key)
        if i < len(node.keys) and node.keys[i] == key:
            return self._delete_from_node(node, i)
        return self._delete_key(node.children[i], key)

    def _delete_from_node(self, node: _BTreeNode[K, V], i: int) -> None:
        t = self._t
        if node.leaf:
            node.keys.pop(i)
            node.values.pop(i)
            self._size -= 1
            return
        left = node.children[i]
        right = node.children[i + 1]
        if len(left.keys) >= t:
            pk, pv = _pop_max(left)
            node.keys[i], node.values[i] = pk, pv
            self._size -= 1
            return
        if len(right.keys) >= t:
            sk, sv = _pop_min(right)
            node.keys[i], node.values[i] = sk, sv
            self._size -= 1
            return
        k = node.keys[i]
        self._merge(node, i)
        return self._delete_key(node.children[i], k)

    def _fill_child(self, parent: _BTreeNode[K, V], ci: int) -> None:
        t = self._t
        child = parent.children[ci]
        if len(child.keys) >= t - 1:
            return
        if ci > 0 and len(parent.children[ci - 1].keys) >= t:
            self._borrow_from_prev(parent, ci)
        elif ci < len(parent.children) - 1 and len(parent.children[ci + 1].keys) >= t:
            self._borrow_from_next(parent, ci)
        else:
            if ci > 0:
                self._merge(parent, ci - 1)
            else:
                self._merge(parent, ci)

    def _borrow_from_prev(self, parent: _BTreeNode[K, V], ci: int) -> None:
        child = parent.children[ci]
        left = parent.children[ci - 1]
        sep = ci - 1
        if not child.leaf:
            child.children.insert(0, left.children.pop())
        child.keys.insert(0, parent.keys[sep])
        child.values.insert(0, parent.values[sep])
        parent.keys[sep] = left.keys.pop()
        parent.values[sep] = left.values.pop()

    def _borrow_from_next(self, parent: _BTreeNode[K, V], ci: int) -> None:
        child = parent.children[ci]
        right = parent.children[ci + 1]
        sep = ci
        if not child.leaf:
            child.children.append(right.children.pop(0))
        child.keys.append(parent.keys[sep])
        child.values.append(parent.values[sep])
        parent.keys[sep] = right.keys.pop(0)
        parent.values[sep] = right.values.pop(0)

    def _merge(self, parent: _BTreeNode[K, V], i: int) -> None:
        left = parent.children[i]
        right = parent.children[i + 1]
        sep_k = parent.keys.pop(i)
        sep_v = parent.values.pop(i)
        left.keys.append(sep_k)
        left.values.append(sep_v)
        left.keys.extend(right.keys)
        left.values.extend(right.values)
        if not left.leaf:
            left.children.extend(right.children)
        parent.children.pop(i + 1)

    def items_inorder(self) -> Iterator[tuple[K, V]]:
        def walk(n: _BTreeNode[K, V]) -> Iterator[tuple[K, V]]:
            if n.leaf:
                for j in range(len(n.keys)):
                    yield (n.keys[j], n.values[j])
                return
            for j in range(len(n.keys)):
                yield from walk(n.children[j])
                yield (n.keys[j], n.values[j])
            yield from walk(n.children[-1])

        if len(self._root.keys) == 0:
            return
        yield from walk(self._root)


def _key_index(node: _BTreeNode[K, V], key: K) -> int:
    i = 0
    while i < len(node.keys) and key > node.keys[i]:
        i += 1
    return i


def _pop_max(node: _BTreeNode[K, V]) -> tuple[K, V]:
    while not node.leaf:
        node = node.children[-1]
    k = node.keys.pop()
    v = node.values.pop()
    return k, v


def _pop_min(node: _BTreeNode[K, V]) -> tuple[K, V]:
    while not node.leaf:
        node = node.children[0]
    k = node.keys.pop(0)
    v = node.values.pop(0)
    return k, v
