"""Red-black binary search tree (unique keys)."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterator, Optional


class Color(Enum):
    RED = 0
    BLACK = 1


@dataclass
class RBNode:
    key: Any
    value: Any
    color: Color = Color.RED
    left: Optional["RBNode"] = None
    right: Optional["RBNode"] = None
    parent: Optional["RBNode"] = None


class RedBlackTree:
    """
    Left-leaning style properties:
    - Every node is red or black.
    - Root is black.
    - Leaves (NIL) are black — we use None as absence; parent pointers maintain structure.
    - Red nodes have black children.
    - Every path from a node to descendant leaves has the same number of black nodes.
    """

    def __init__(self) -> None:
        self._root: Optional[RBNode] = None

    def __len__(self) -> int:
        return self._count_nodes(self._root)

    def _count_nodes(self, n: Optional[RBNode]) -> int:
        if n is None:
            return 0
        return 1 + self._count_nodes(n.left) + self._count_nodes(n.right)

    def get(self, key: Any) -> Optional[Any]:
        n = self._find_node(key)
        return None if n is None else n.value

    def __contains__(self, key: Any) -> bool:
        return self._find_node(key) is not None

    def __getitem__(self, key: Any) -> Any:
        n = self._find_node(key)
        if n is None:
            raise KeyError(key)
        return n.value

    def __setitem__(self, key: Any, value: Any) -> None:
        self.insert(key, value)

    def __delitem__(self, key: Any) -> None:
        self.delete(key)

    def _find_node(self, key: Any) -> Optional[RBNode]:
        n = self._root
        while n is not None:
            if key == n.key:
                return n
            if key < n.key:
                n = n.left
            else:
                n = n.right
        return None

    def insert(self, key: Any, value: Any) -> None:
        if self._root is None:
            self._root = RBNode(key=key, value=value, color=Color.BLACK)
            return

        parent: Optional[RBNode] = None
        cur = self._root
        while cur is not None:
            parent = cur
            if key == cur.key:
                cur.value = value
                return
            if key < cur.key:
                cur = cur.left
            else:
                cur = cur.right

        z = RBNode(key=key, value=value, parent=parent)
        assert parent is not None
        if key < parent.key:
            parent.left = z
        else:
            parent.right = z
        self._fix_insert(z)

    def _rotate_left(self, x: RBNode) -> None:
        y = x.right
        assert y is not None
        x.right = y.left
        if y.left is not None:
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

    def _rotate_right(self, x: RBNode) -> None:
        y = x.left
        assert y is not None
        x.left = y.right
        if y.right is not None:
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

    def _fix_insert(self, z: RBNode) -> None:
        while z.parent is not None and z.parent.color == Color.RED:
            gp = z.parent.parent
            assert gp is not None
            if z.parent is gp.left:
                y = gp.right
                if y is not None and y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    gp.color = Color.RED
                    z = gp
                else:
                    if z is z.parent.right:
                        z = z.parent
                        self._rotate_left(z)
                    assert z.parent is not None
                    z.parent.color = Color.BLACK
                    gp.color = Color.RED
                    self._rotate_right(gp)
            else:
                y = gp.left
                if y is not None and y.color == Color.RED:
                    z.parent.color = Color.BLACK
                    y.color = Color.BLACK
                    gp.color = Color.RED
                    z = gp
                else:
                    if z is z.parent.left:
                        z = z.parent
                        self._rotate_right(z)
                    assert z.parent is not None
                    z.parent.color = Color.BLACK
                    gp.color = Color.RED
                    self._rotate_left(gp)
        assert self._root is not None
        self._root.color = Color.BLACK

    def minimum(self, n: RBNode) -> RBNode:
        while n.left is not None:
            n = n.left
        return n

    def delete(self, key: Any) -> None:
        z = self._find_node(key)
        if z is None:
            raise KeyError(key)

        y = z
        y_orig_color = y.color
        nil_parent: Optional[RBNode] = None
        nil_is_left = False
        if z.left is None:
            x = z.right
            nil_parent = z.parent
            nil_is_left = nil_parent is not None and z is nil_parent.left
            self._transplant(z, z.right)
        elif z.right is None:
            x = z.left
            nil_parent = z.parent
            nil_is_left = nil_parent is not None and z is nil_parent.left
            self._transplant(z, z.left)
        else:
            y = self.minimum(z.right)
            y_orig_color = y.color
            x = y.right
            if y.parent is z:
                if x is not None:
                    x.parent = y
            else:
                self._transplant(y, y.right)
                y.right = z.right
                if y.right is not None:
                    y.right.parent = y
            self._transplant(z, y)
            y.left = z.left
            if y.left is not None:
                y.left.parent = y
            y.color = z.color

        if y_orig_color == Color.BLACK:
            if x is not None:
                self._fix_delete(x)
            elif nil_parent is not None:
                self._fix_double_black_nil(nil_parent, nil_is_left)

        if self._root is not None:
            self._root.color = Color.BLACK

    def _transplant(self, u: RBNode, v: Optional[RBNode]) -> None:
        if u.parent is None:
            self._root = v
        elif u is u.parent.left:
            u.parent.left = v
        else:
            u.parent.right = v
        if v is not None:
            v.parent = u.parent

    def _fix_double_black_nil(self, parent: RBNode, is_left: bool) -> None:
        """Double-black at a missing child of parent (replacement was None)."""
        x: Optional[RBNode] = None
        while parent is not None:
            if is_left:
                w = parent.right
                if w is not None and w.color == Color.RED:
                    w.color = Color.BLACK
                    parent.color = Color.RED
                    self._rotate_left(parent)
                    w = parent.right
                wl_black = w is None or w.left is None or w.left.color == Color.BLACK
                wr_black = w is None or w.right is None or w.right.color == Color.BLACK
                if wl_black and wr_black:
                    if w is not None:
                        w.color = Color.RED
                    if parent.color == Color.RED:
                        parent.color = Color.BLACK
                        break
                    gp = parent.parent
                    is_left = gp is not None and parent is gp.left
                    parent = gp
                    continue
                if wr_black and w is not None:
                    if w.left is not None:
                        w.left.color = Color.BLACK
                    w.color = Color.RED
                    self._rotate_right(w)
                    w = parent.right
                if w is not None:
                    w.color = parent.color
                    parent.color = Color.BLACK
                    if w.right is not None:
                        w.right.color = Color.BLACK
                    self._rotate_left(parent)
                break
            else:
                w = parent.left
                if w is not None and w.color == Color.RED:
                    w.color = Color.BLACK
                    parent.color = Color.RED
                    self._rotate_right(parent)
                    w = parent.left
                wl_black = w is None or w.left is None or w.left.color == Color.BLACK
                wr_black = w is None or w.right is None or w.right.color == Color.BLACK
                if wl_black and wr_black:
                    if w is not None:
                        w.color = Color.RED
                    if parent.color == Color.RED:
                        parent.color = Color.BLACK
                        break
                    gp = parent.parent
                    is_left = gp is not None and parent is gp.left
                    parent = gp
                    continue
                if wl_black and w is not None:
                    if w.right is not None:
                        w.right.color = Color.BLACK
                    w.color = Color.RED
                    self._rotate_left(w)
                    w = parent.left
                if w is not None:
                    w.color = parent.color
                    parent.color = Color.BLACK
                    if w.left is not None:
                        w.left.color = Color.BLACK
                    self._rotate_right(parent)
                break
        if self._root is not None:
            self._root.color = Color.BLACK

    def _fix_delete(self, x: Optional[RBNode]) -> None:
        while x is not self._root and (x is None or x.color == Color.BLACK):
            if x is None:
                break
            parent = x.parent
            if parent is None:
                break
            if x is parent.left:
                w = parent.right
                if w is not None and w.color == Color.RED:
                    w.color = Color.BLACK
                    parent.color = Color.RED
                    self._rotate_left(parent)
                    w = parent.right
                wl_black = w is None or w.left is None or w.left.color == Color.BLACK
                wr_black = w is None or w.right is None or w.right.color == Color.BLACK
                if wl_black and wr_black:
                    if w is not None:
                        w.color = Color.RED
                    x = parent
                else:
                    if wr_black and w is not None:
                        if w.left is not None:
                            w.left.color = Color.BLACK
                        w.color = Color.RED
                        self._rotate_right(w)
                        w = parent.right
                    if w is not None:
                        w.color = parent.color
                        parent.color = Color.BLACK
                        if w.right is not None:
                            w.right.color = Color.BLACK
                        self._rotate_left(parent)
                    x = self._root
            else:
                w = parent.left
                if w is not None and w.color == Color.RED:
                    w.color = Color.BLACK
                    parent.color = Color.RED
                    self._rotate_right(parent)
                    w = parent.left
                wl_black = w is None or w.left is None or w.left.color == Color.BLACK
                wr_black = w is None or w.right is None or w.right.color == Color.BLACK
                if wl_black and wr_black:
                    if w is not None:
                        w.color = Color.RED
                    x = parent
                else:
                    if wl_black and w is not None:
                        if w.right is not None:
                            w.right.color = Color.BLACK
                        w.color = Color.RED
                        self._rotate_left(w)
                        w = parent.left
                    if w is not None:
                        w.color = parent.color
                        parent.color = Color.BLACK
                        if w.left is not None:
                            w.left.color = Color.BLACK
                        self._rotate_right(parent)
                    x = self._root
        if x is not None:
            x.color = Color.BLACK

    def items(self) -> Iterator[tuple[Any, Any]]:
        for k, v in self._inorder(self._root):
            yield k, v

    def _inorder(self, n: Optional[RBNode]) -> Iterator[tuple[Any, Any]]:
        if n is None:
            return
        yield from self._inorder(n.left)
        yield n.key, n.value
        yield from self._inorder(n.right)

    def keys(self) -> Iterator[Any]:
        for k, _ in self.items():
            yield k

    def values(self) -> Iterator[Any]:
        for _, v in self.items():
            yield v
