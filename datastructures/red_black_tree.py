"""
Red-black tree: self-balancing binary search tree with O(log n) worst-case operations.

Each node stores a key (and optional satellite data). Colors satisfy:
1. Every node is RED or BLACK.
2. The root is BLACK.
3. NIL leaves are BLACK.
4. No consecutive reds (a RED node's parent is BLACK).
5. Every path from a node to descendant NIL has the same black-height.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, Iterator, Optional, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class Color(Enum):
    RED = 0
    BLACK = 1


@dataclass
class _RBNode(Generic[K, V]):
    key: K
    value: V
    color: Color
    left: Optional["_RBNode[K, V]"]
    right: Optional["_RBNode[K, V]"]
    parent: Optional["_RBNode[K, V]"]


class RedBlackTree(Generic[K, V]):
    """
    Ordered map backed by a red-black tree.

    Average / worst-case time per insert, delete, search: O(log n).
    Space: O(n) for n stored keys.
    """

    def __init__(self) -> None:
        self._nil: _RBNode[K, V] = _RBNode(
            key=None,  # type: ignore[arg-type]
            value=None,  # type: ignore[arg-type]
            color=Color.BLACK,
            left=None,
            right=None,
            parent=None,
        )
        self._nil.left = self._nil
        self._nil.right = self._nil
        self._root: _RBNode[K, V] = self._nil
        self._size = 0

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: object) -> bool:
        return self._find_node(key) is not self._nil

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        n = self._find_node(key)
        if n is self._nil:
            return default
        return n.value

    def __getitem__(self, key: K) -> V:
        n = self._find_node(key)
        if n is self._nil:
            raise KeyError(key)
        return n.value

    def __setitem__(self, key: K, value: V) -> None:
        self.insert(key, value)

    def __delitem__(self, key: K) -> None:
        self.delete(key)

    def insert(self, key: K, value: V) -> None:
        """Insert or update key. Time O(log n), space O(1) auxiliary."""
        z = _RBNode(
            key=key,
            value=value,
            color=Color.RED,
            left=self._nil,
            right=self._nil,
            parent=self._nil,
        )
        y: Optional[_RBNode[K, V]] = self._nil
        x = self._root
        while x is not self._nil:
            y = x
            if key < x.key:
                x = x.left  # type: ignore[assignment]
            elif key > x.key:
                x = x.right  # type: ignore[assignment]
            else:
                x.value = value
                return
        z.parent = y
        if y is self._nil:
            self._root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self._size += 1
        self._insert_fixup(z)

    def delete(self, key: K) -> None:
        """Remove key. Time O(log n), space O(1) auxiliary."""
        z = self._find_node(key)
        if z is self._nil:
            raise KeyError(key)
        y = z
        y_orig_color = y.color
        if z.left is self._nil:
            x = z.right  # type: ignore[assignment]
            self._transplant(z, z.right)
        elif z.right is self._nil:
            x = z.left  # type: ignore[assignment]
            self._transplant(z, z.left)
        else:
            y = self._minimum(z.right)
            y_orig_color = y.color
            x = y.right  # type: ignore[assignment]
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
        if y_orig_color == Color.BLACK:
            self._delete_fixup(x)
        self._size -= 1

    def _minimum(self, n: _RBNode[K, V]) -> _RBNode[K, V]:
        while n.left is not self._nil:
            n = n.left
        return n

    def _find_node(self, key: object) -> _RBNode[K, V]:
        x = self._root
        while x is not self._nil:
            if key == x.key:
                return x
            if key < x.key:
                x = x.left  # type: ignore[assignment]
            else:
                x = x.right  # type: ignore[assignment]
        return self._nil

    def _left_rotate(self, x: _RBNode[K, V]) -> None:
        y = x.right  # type: ignore[assignment]
        x.right = y.left
        if y.left is not self._nil:
            y.left.parent = x
        y.parent = x.parent
        if x.parent is self._nil:
            self._root = y
        elif x is x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def _right_rotate(self, y: _RBNode[K, V]) -> None:
        x = y.left  # type: ignore[assignment]
        y.left = x.right
        if x.right is not self._nil:
            x.right.parent = y
        x.parent = y.parent
        if y.parent is self._nil:
            self._root = x
        elif y is y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
        x.right = y
        y.parent = x

    def _transplant(self, u: _RBNode[K, V], v: _RBNode[K, V]) -> None:
        if u.parent is self._nil:
            self._root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _insert_fixup(self, z: _RBNode[K, V]) -> None:
        while z.parent.color == Color.RED:
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = Color.BLACK
                    z.parent.parent.color = Color.RED
                    self._left_rotate(z.parent.parent)
        self._root.color = Color.BLACK

    def _delete_fixup(self, x: _RBNode[K, V]) -> None:
        while x is not self._root and x.color == Color.BLACK:
            if x is x.parent.left:
                w = x.parent.right
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == Color.BLACK and w.right.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.right.color == Color.BLACK:
                        w.left.color = Color.BLACK
                        w.color = Color.RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.right.color = Color.BLACK
                    self._left_rotate(x.parent)
                    x = self._root
            else:
                w = x.parent.left
                if w.color == Color.RED:
                    w.color = Color.BLACK
                    x.parent.color = Color.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == Color.BLACK and w.left.color == Color.BLACK:
                    w.color = Color.RED
                    x = x.parent
                else:
                    if w.left.color == Color.BLACK:
                        w.right.color = Color.BLACK
                        w.color = Color.RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = Color.BLACK
                    w.left.color = Color.BLACK
                    self._right_rotate(x.parent)
                    x = self._root
        x.color = Color.BLACK

    def items_inorder(self) -> Iterator[tuple[K, V]]:
        """Sorted (key, value) pairs. Time O(n)."""

        def walk(n: _RBNode[K, V]) -> Iterator[tuple[K, V]]:
            if n is self._nil:
                return
            yield from walk(n.left)
            yield (n.key, n.value)
            yield from walk(n.right)

        yield from walk(self._root)
