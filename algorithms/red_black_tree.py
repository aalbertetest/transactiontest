"""Red-black tree (CLRS-style): ordered map with O(log n) search, insert, and delete."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Generic, Iterator, Optional, Tuple, TypeVar

K = TypeVar("K")
V = TypeVar("V")


class _Color(Enum):
    RED = 0
    BLACK = 1


@dataclass
class _Node(Generic[K, V]):
    key: K
    value: V
    left: "_Node[K, V]"
    right: "_Node[K, V]"
    parent: Optional["_Node[K, V]"]
    color: _Color


class RedBlackTree(Generic[K, V]):
    """
    Ordered map backed by a red-black tree.

    Height is at most 2 log(n+1). Search, insert, and delete are O(log n).
    """

    def __init__(self) -> None:
        self._nil = _Node(
            key=None,  # type: ignore[arg-type]
            value=None,  # type: ignore[arg-type]
            left=None,  # type: ignore[arg-type]
            right=None,  # type: ignore[arg-type]
            parent=None,
            color=_Color.BLACK,
        )
        self._nil.left = self._nil
        self._nil.right = self._nil
        self._root: _Node[K, V] = self._nil
        self._n = 0

    def __len__(self) -> int:
        return self._n

    def __bool__(self) -> bool:
        return self._root is not self._nil

    def _find_node(self, key: K) -> _Node[K, V]:
        x = self._root
        while x is not self._nil and key != x.key:
            if key < x.key:
                x = x.left
            else:
                x = x.right
        return x

    def get(self, key: K, default: Optional[V] = None) -> Optional[V]:
        x = self._find_node(key)
        if x is self._nil:
            return default
        return x.value

    def __getitem__(self, key: K) -> V:
        x = self._find_node(key)
        if x is self._nil:
            raise KeyError(key)
        return x.value

    def __contains__(self, key: object) -> bool:
        if self._root is self._nil:
            return False
        try:
            return self._find_node(key) is not self._nil  # type: ignore[arg-type]
        except TypeError:
            return False

    def _left_rotate(self, x: _Node[K, V]) -> None:
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

    def _right_rotate(self, x: _Node[K, V]) -> None:
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

    def _insert_fixup(self, z: _Node[K, V]) -> None:
        while z.parent is not None and z.parent.color == _Color.RED:
            assert z.parent.parent is not None
            if z.parent is z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == _Color.RED:
                    z.parent.color = _Color.BLACK
                    y.color = _Color.BLACK
                    z.parent.parent.color = _Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._left_rotate(z)
                    z.parent.color = _Color.BLACK
                    z.parent.parent.color = _Color.RED
                    self._right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == _Color.RED:
                    z.parent.color = _Color.BLACK
                    y.color = _Color.BLACK
                    z.parent.parent.color = _Color.RED
                    z = z.parent.parent
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._right_rotate(z)
                    z.parent.color = _Color.BLACK
                    z.parent.parent.color = _Color.RED
                    self._left_rotate(z.parent.parent)
        self._root.color = _Color.BLACK

    def put(self, key: K, value: V) -> None:
        y: Optional[_Node[K, V]] = None
        x = self._root
        while x is not self._nil:
            y = x
            if key == x.key:
                x.value = value
                return
            if key < x.key:
                x = x.left
            else:
                x = x.right
        z = _Node(
            key=key,
            value=value,
            left=self._nil,
            right=self._nil,
            parent=y,
            color=_Color.RED,
        )
        if y is None:
            self._root = z
        elif key < y.key:
            y.left = z
        else:
            y.right = z
        self._insert_fixup(z)
        self._n += 1

    def __setitem__(self, key: K, value: V) -> None:
        self.put(key, value)

    def _transplant(self, u: _Node[K, V], v: _Node[K, V]) -> None:
        if u.parent is None:
            self._root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        v.parent = u.parent

    def _minimum(self, x: _Node[K, V]) -> _Node[K, V]:
        while x.left is not self._nil:
            x = x.left
        return x

    def _delete_fixup(self, x: _Node[K, V]) -> None:
        while x is not self._root and x.color == _Color.BLACK:
            assert x.parent is not None
            if x is x.parent.left:
                w = x.parent.right
                if w.color == _Color.RED:
                    w.color = _Color.BLACK
                    x.parent.color = _Color.RED
                    self._left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == _Color.BLACK and w.right.color == _Color.BLACK:
                    w.color = _Color.RED
                    x = x.parent
                else:
                    if w.right.color == _Color.BLACK:
                        w.left.color = _Color.BLACK
                        w.color = _Color.RED
                        self._right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = _Color.BLACK
                    w.right.color = _Color.BLACK
                    self._left_rotate(x.parent)
                    x = self._root
            else:
                w = x.parent.left
                if w.color == _Color.RED:
                    w.color = _Color.BLACK
                    x.parent.color = _Color.RED
                    self._right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == _Color.BLACK and w.left.color == _Color.BLACK:
                    w.color = _Color.RED
                    x = x.parent
                else:
                    if w.left.color == _Color.BLACK:
                        w.right.color = _Color.BLACK
                        w.color = _Color.RED
                        self._left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = _Color.BLACK
                    w.left.color = _Color.BLACK
                    self._right_rotate(x.parent)
                    x = self._root
        x.color = _Color.BLACK

    def remove(self, key: K) -> None:
        z = self._find_node(key)
        if z is self._nil:
            raise KeyError(key)
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
        if y_orig_color == _Color.BLACK:
            self._delete_fixup(x)
        self._n -= 1

    def __delitem__(self, key: K) -> None:
        self.remove(key)

    def _inorder(self, x: _Node[K, V]) -> Iterator[Tuple[K, V]]:
        if x is self._nil:
            return
        yield from self._inorder(x.left)
        yield x.key, x.value
        yield from self._inorder(x.right)

    def items(self) -> Iterator[Tuple[K, V]]:
        yield from self._inorder(self._root)

    def keys(self) -> Iterator[K]:
        for k, _ in self.items():
            yield k

    def values(self) -> Iterator[V]:
        for _, v in self.items():
            yield v
