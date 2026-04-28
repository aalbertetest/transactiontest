"""
Red–Black Tree (ordered map of comparable keys to values).

Complexity (n = number of keys)
------------------------------
- Search: O(log n) time, O(1) extra space (iterative).
- Insert: O(log n) time (rotations + recolor are O(1) per level), O(1) extra space.
- Delete: O(log n) time, O(1) extra space.

Space: O(n) for tree nodes plus O(1) for the sentinel.

Walkthrough — insertion (high level)
------------------------------------
1. BST-insert the new node as **red** (does not break black-height).
2. If parent is black, done.
3. If parent is red, we have a red–red violation; fix using rotations and recoloring
   depending on whether the uncle is red (push black down) or black (rotate + recolor).

Walkthrough — deletion (high level)
------------------------------------
1. Standard BST delete; track a "double-black" deficit when removing a black node.
2. Resolve double-black at the deleted position using sibling-based cases (mirror of insertion).

Edge cases
----------
- Empty tree: insert becomes root and is forced black.
- Duplicate keys: this implementation **replaces** the value (like a dict) rather than storing duplicates.
- Single node: root must stay black after insert.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Generic, Iterator, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _Color:
    RED = 0
    BLACK = 1


@dataclass
class _RBNode(Generic[K, V]):
    key: K
    value: V
    left: "_RBNode[K, V]"
    right: "_RBNode[K, V]"
    parent: Optional["_RBNode[K, V]"]
    color: int


class RedBlackTree(Generic[K, V]):
    """
    Left-leaning style textbook RB tree over keys supporting mapping operations.

    Keys must be totally ordered (support `<`).
    """

    def __init__(self) -> None:
        self._nil: _RBNode[K, V] = _RBNode(
            key=None,  # type: ignore[arg-type]
            value=None,  # type: ignore[arg-type]
            left=None,  # type: ignore[arg-type]
            right=None,  # type: ignore[arg-type]
            parent=None,
            color=_Color.BLACK,
        )
        self._nil.left = self._nil
        self._nil.right = self._nil
        self._root: _RBNode[K, V] = self._nil
        self._len = 0

    def __len__(self) -> int:
        return self._len

    def __contains__(self, key: object) -> bool:
        return self._find_node(key) is not None

    def __getitem__(self, key: K) -> V:
        n = self._find_node(key)
        if n is None:
            raise KeyError(key)
        return n.value

    def __setitem__(self, key: K, value: V) -> None:
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        self.delete(key)

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        n = self._find_node(key)
        return default if n is None else n.value

    def insert(self, key: K, value: V) -> None:
        """Insert or update *key* with *value*."""
        parent = self._nil
        cur = self._root
        while cur is not self._nil:
            parent = cur
            if key == cur.key:
                cur.value = value
                return
            cur = cur.left if key < cur.key else cur.right

        node = _RBNode(
            key=key,
            value=value,
            left=self._nil,
            right=self._nil,
            parent=parent if parent is not self._nil else None,
            color=_Color.RED,
        )
        if parent is self._nil:
            self._root = node
        elif key < parent.key:
            parent.left = node
        else:
            parent.right = node

        self._len += 1
        self._insert_fixup(node)

    def delete(self, key: K) -> None:
        """Remove *key* if present; raises KeyError if missing."""
        z = self._find_node(key)
        if z is None:
            raise KeyError(key)
        self._delete_node(z)

    def _find_node(self, key: object) -> Optional[_RBNode[K, V]]:
        cur = self._root
        while cur is not self._nil:
            if key == cur.key:
                return cur
            cur = cur.left if key < cur.key else cur.right
        return None

    def _rotate_left(self, x: _RBNode[K, V]) -> None:
        y = x.right
        x.right = y.left
        if y.left is not self._nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is None:
            self._root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _rotate_right(self, x: _RBNode[K, V]) -> None:
        y = x.left
        x.left = y.right
        if y.right is not self._nil:
            y.right.parent = x
        y.parent = x.parent
        if x.parent is None:
            self._root = y
        elif x is x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right = x
        x.parent = y

    def _insert_fixup(self, z: _RBNode[K, V]) -> None:
        while z.parent is not None and z.parent.color == _Color.RED:
            gp = z.parent.parent
            assert gp is not None
            if z.parent is gp.left:
                y = gp.right
                if y.color == _Color.RED:
                    z.parent.color = _Color.BLACK
                    y.color = _Color.BLACK
                    gp.color = _Color.RED
                    z = gp
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._rotate_left(z)
                    z.parent.color = _Color.BLACK
                    gp.color = _Color.RED
                    self._rotate_right(gp)
            else:
                y = gp.left
                if y.color == _Color.RED:
                    z.parent.color = _Color.BLACK
                    y.color = _Color.BLACK
                    gp.color = _Color.RED
                    z = gp
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    z.parent.color = _Color.BLACK
                    gp.color = _Color.RED
                    self._rotate_left(gp)
        self._root.color = _Color.BLACK

    def _transplant(self, u: _RBNode[K, V], v: _RBNode[K, V]) -> None:
        if u.parent is None:
            self._root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, x: _RBNode[K, V]) -> _RBNode[K, V]:
        while x.left is not self._nil:
            x = x.left
        return x

    def _delete_fixup(self, x: _RBNode[K, V]) -> None:
        while x is not self._root and x.color == _Color.BLACK:
            assert x.parent is not None
            if x is x.parent.left:
                w = x.parent.right
                if w.color == _Color.RED:
                    w.color = _Color.BLACK
                    x.parent.color = _Color.RED
                    self._rotate_left(x.parent)
                    w = x.parent.right
                if w.left.color == _Color.BLACK and w.right.color == _Color.BLACK:
                    w.color = _Color.RED
                    x = x.parent
                else:
                    if w.right.color == _Color.BLACK:
                        w.left.color = _Color.BLACK
                        w.color = _Color.RED
                        self._rotate_right(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = _Color.BLACK
                    w.right.color = _Color.BLACK
                    self._rotate_left(x.parent)
                    x = self._root
            else:
                w = x.parent.left
                if w.color == _Color.RED:
                    w.color = _Color.BLACK
                    x.parent.color = _Color.RED
                    self._rotate_right(x.parent)
                    w = x.parent.left
                if w.right.color == _Color.BLACK and w.left.color == _Color.BLACK:
                    w.color = _Color.RED
                    x = x.parent
                else:
                    if w.left.color == _Color.BLACK:
                        w.right.color = _Color.BLACK
                        w.color = _Color.RED
                        self._rotate_left(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = _Color.BLACK
                    w.left.color = _Color.BLACK
                    self._rotate_right(x.parent)
                    x = self._root
        x.color = _Color.BLACK

    def _delete_node(self, z: _RBNode[K, V]) -> None:
        y = z
        y_orig_color = y.color
        if z.left is self._nil:
            x = z.right
            self._transplant(z, z.right)
        elif z.right is self._nil:
            x = z.left
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent is z:
                x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            y.left.parent = y
            y.color = z.color
        self._len -= 1
        if y_orig_color == _Color.BLACK:
            self._delete_fixup(x)

    def items(self) -> Iterator[Tuple[K, V]]:
        """In-order traversal yielding (key, value) pairs."""
        stack: list[_RBNode[K, V]] = []
        cur = self._root
        while stack or cur is not self._nil:
            while cur is not self._nil:
                stack.append(cur)
                cur = cur.left
            cur = stack.pop()
            yield cur.key, cur.value
            cur = cur.right

    def keys(self) -> Iterator[K]:
        for k, _ in self.items():
            yield k

    def values(self) -> Iterator[V]:
        for _, v in self.items():
            yield v


def demo_rb_tree() -> None:
    t: RedBlackTree[int, str] = RedBlackTree()
    for i in [10, 20, 30, 15, 25, 5]:
        t[i] = f"v{i}"
    assert t[20] == "v20"
    del t[20]
    assert 20 not in t


if __name__ == "__main__":
    demo_rb_tree()
