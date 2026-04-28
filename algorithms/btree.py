"""B-tree (order parameter t: min degree, each node except root has >= t-1 keys, <= 2t-1 keys)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Generic, Iterator, List, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


@dataclass
class _BNode(Generic[K, V]):
    keys: List[K] = field(default_factory=list)
    values: List[V] = field(default_factory=list)
    children: List["_BNode[K, V]"] = field(default_factory=list)
    leaf: bool = True


class BTree(Generic[K, V]):
    """
    Disk-oriented B-tree with in-memory nodes.

    * t >= 2 is the minimum degree: non-root nodes hold between t-1 and 2t-1 keys.
    * Search O(t log_t n); insert/delete same order; height O(log_t n).
    * Space O(n) keys plus O(n) child pointers.
    """

    def __init__(self, t: int = 3) -> None:
        if t < 2:
            raise ValueError("minimum degree t must be >= 2")
        self._t = t
        self._root = _BNode[K, V]()
        self._n = 0

    @property
    def t(self) -> int:
        return self._t

    def __len__(self) -> int:
        return self._n

    def _lookup(self, node: _BNode[K, V], key: K) -> Tuple[bool, Optional[V]]:
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1
        if i < len(node.keys) and key == node.keys[i]:
            return True, node.values[i]
        if node.leaf:
            return False, None
        return self._lookup(node.children[i], key)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        ok, v = self._lookup(self._root, key)
        return v if ok else default

    def __getitem__(self, key: K) -> V:
        ok, v = self._lookup(self._root, key)
        if not ok:
            raise KeyError(key)
        return v  # type: ignore[return-value]

    def __contains__(self, key: object) -> bool:
        try:
            ok, _ = self._lookup(self._root, key)  # type: ignore[arg-type]
            return ok
        except TypeError:
            return False

    def _split_child(self, parent: _BNode[K, V], index: int) -> None:
        """Split full child y = parent.children[index] (2t-1 keys) into y, median, z."""
        t = self._t
        y = parent.children[index]
        z = _BNode[K, V](leaf=y.leaf)
        z.keys = y.keys[t:]
        z.values = y.values[t:]
        if not y.leaf:
            z.children = y.children[t:]
        promote_k = y.keys[t - 1]
        promote_v = y.values[t - 1]
        y.keys = y.keys[: t - 1]
        y.values = y.values[: t - 1]
        if not y.leaf:
            y.children = y.children[:t]
        parent.keys.insert(index, promote_k)
        parent.values.insert(index, promote_v)
        parent.children.insert(index + 1, z)

    def _insert_non_full(self, node: _BNode[K, V], key: K, value: V) -> bool:
        """Returns True if a new key was inserted."""
        i = len(node.keys) - 1
        if node.leaf:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            if i >= 0 and key == node.keys[i]:
                node.values[i] = value
                return False
            node.keys.insert(i + 1, key)
            node.values.insert(i + 1, value)
            return True
        while i >= 0 and key < node.keys[i]:
            i -= 1
        i += 1
        if i < len(node.keys) and key == node.keys[i]:
            node.values[i] = value
            return False
        if len(node.children[i].keys) == 2 * self._t - 1:
            self._split_child(node, i)
            if key > node.keys[i]:
                i += 1
        return self._insert_non_full(node.children[i], key, value)

    def __setitem__(self, key: K, value: V) -> None:
        r = self._root
        if len(r.keys) == 2 * self._t - 1:
            s = _BNode[K, V](leaf=False)
            s.children.append(r)
            self._root = s
            self._split_child(s, 0)
            r = s
        if self._insert_non_full(r, key, value):
            self._n += 1

    def _merge(self, parent: _BNode[K, V], i: int) -> None:
        """Merge child i and child i+1 using parent's key at i."""
        left = parent.children[i]
        right = parent.children[i + 1]
        left.keys.append(parent.keys.pop(i))
        left.values.append(parent.values.pop(i))
        left.keys.extend(right.keys)
        left.values.extend(right.values)
        if not right.leaf:
            left.children.extend(right.children)
        parent.children.pop(i + 1)

    def _borrow_from_prev(self, parent: _BNode[K, V], i: int) -> None:
        child = parent.children[i]
        sibling = parent.children[i - 1]
        child.keys.insert(0, parent.keys[i - 1])
        child.values.insert(0, parent.values[i - 1])
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())
        parent.keys[i - 1] = sibling.keys.pop()
        parent.values[i - 1] = sibling.values.pop()

    def _borrow_from_next(self, parent: _BNode[K, V], i: int) -> None:
        child = parent.children[i]
        sibling = parent.children[i + 1]
        child.keys.append(parent.keys[i])
        child.values.append(parent.values[i])
        if not child.leaf:
            child.children.append(sibling.children.pop(0))
        parent.keys[i] = sibling.keys.pop(0)
        parent.values[i] = sibling.values.pop(0)

    def _fill(self, parent: _BNode[K, V], i: int) -> None:
        t = self._t
        if i > 0 and len(parent.children[i - 1].keys) >= t:
            self._borrow_from_prev(parent, i)
        elif i < len(parent.children) - 1 and len(parent.children[i + 1].keys) >= t:
            self._borrow_from_next(parent, i)
        else:
            if i < len(parent.children) - 1:
                self._merge(parent, i)
            else:
                self._merge(parent, i - 1)

    def _delete_from_node(self, node: _BNode[K, V], key: K) -> bool:
        t = self._t
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            if node.leaf:
                node.keys.pop(i)
                node.values.pop(i)
                return True
            if len(node.children[i].keys) >= t:
                pred = self._predecessor(node.children[i])
                pk, pv = pred
                node.keys[i], node.values[i] = pk, pv
                return self._delete_from_node(node.children[i], pk)
            if len(node.children[i + 1].keys) >= t:
                succ = self._successor(node.children[i + 1])
                sk, sv = succ
                node.keys[i], node.values[i] = sk, sv
                return self._delete_from_node(node.children[i + 1], sk)
            self._merge(node, i)
            return self._delete_from_node(node.children[i], key)

        if node.leaf:
            return False

        if len(node.children[i].keys) < t:
            self._fill(node, i)
            if i > len(node.keys):
                return self._delete_from_node(node.children[i - 1], key)
        return self._delete_from_node(node.children[i], key)

    def _predecessor(self, node: _BNode[K, V]) -> Tuple[K, V]:
        while not node.leaf:
            node = node.children[-1]
        return node.keys[-1], node.values[-1]

    def _successor(self, node: _BNode[K, V]) -> Tuple[K, V]:
        while not node.leaf:
            node = node.children[0]
        return node.keys[0], node.values[0]

    def delete(self, key: K) -> None:
        r = self._root
        if not self._delete_from_node(r, key):
            raise KeyError(key)
        self._n -= 1
        if not r.keys and not r.leaf:
            self._root = r.children[0]

    def __delitem__(self, key: K) -> None:
        self.delete(key)

    def _walk(self, node: _BNode[K, V]) -> Iterator[Tuple[K, V]]:
        if node.leaf:
            for k, v in zip(node.keys, node.values):
                yield k, v
            return
        for i in range(len(node.keys)):
            yield from self._walk(node.children[i])
            yield node.keys[i], node.values[i]
        yield from self._walk(node.children[-1])

    def items(self) -> Iterator[Tuple[K, V]]:
        yield from self._walk(self._root)
