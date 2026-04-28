"""B-tree (order t: max 2t-1 keys per node, min t-1 keys except root)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Iterator, List, Optional


@dataclass
class BTreeNode:
    keys: List[Any] = field(default_factory=list)
    children: List["BTreeNode"] = field(default_factory=list)
    leaf: bool = True

    def __len__(self) -> int:
        return len(self.keys)


class BTree:
    """
    B-tree with configurable minimum degree `t` (t >= 2).
    Each node holds at most `2*t - 1` keys and at most `2*t` children.
    """

    def __init__(self, t: int = 2) -> None:
        if t < 2:
            raise ValueError("minimum degree t must be >= 2")
        self._t = t
        self._root = BTreeNode(leaf=True)

    @property
    def t(self) -> int:
        return self._t

    def search(self, key: Any) -> Optional[tuple[BTreeNode, int]]:
        return self._search_node(self._root, key)

    def _search_node(self, x: BTreeNode, key: Any) -> Optional[tuple[BTreeNode, int]]:
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1
        if i < len(x.keys) and key == x.keys[i]:
            return x, i
        if x.leaf:
            return None
        return self._search_node(x.children[i], key)

    def __contains__(self, key: Any) -> bool:
        return self.search(key) is not None

    def insert(self, key: Any) -> None:
        root = self._root
        if len(root.keys) == 2 * self._t - 1:
            s = BTreeNode(leaf=False)
            s.children.append(root)
            self._split_child(s, 0)
            self._root = s
        self._insert_non_full(self._root, key)

    def _split_child(self, parent: BTreeNode, i: int) -> None:
        t = self._t
        y = parent.children[i]
        z = BTreeNode(leaf=y.leaf)
        promote = y.keys[t - 1]
        z.keys = y.keys[t:]
        y.keys = y.keys[: t - 1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]
        parent.keys.insert(i, promote)
        parent.children.insert(i + 1, z)

    def _insert_non_full(self, x: BTreeNode, key: Any) -> None:
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1
        if i < len(x.keys) and key == x.keys[i]:
            raise ValueError(f"duplicate key: {key!r}")
        if x.leaf:
            x.keys.insert(i, key)
            return
        if len(x.children[i].keys) == 2 * self._t - 1:
            self._split_child(x, i)
            if key > x.keys[i]:
                i += 1
        self._insert_non_full(x.children[i], key)

    def delete(self, key: Any) -> None:
        if not self._delete_from(self._root, key):
            raise KeyError(key)
        if len(self._root.keys) == 0 and not self._root.leaf:
            self._root = self._root.children[0]

    def _delete_from(self, x: BTreeNode, key: Any) -> bool:
        t = self._t
        i = 0
        while i < len(x.keys) and key > x.keys[i]:
            i += 1
        if i < len(x.keys) and key == x.keys[i]:
            if x.leaf:
                x.keys.pop(i)
                return True
            self._delete_internal(x, i)
            return True
        if x.leaf:
            return False
        child = x.children[i]
        if len(child.keys) < t:
            self._ensure_min_keys(x, i)
            return self._delete_from(self._root, key)
        return self._delete_from(child, key)

    def _delete_internal(self, x: BTreeNode, i: int) -> None:
        t = self._t
        key = x.keys[i]
        if len(x.children[i].keys) >= t:
            pred = self._predecessor(x.children[i])
            x.keys[i] = pred
            self._delete_from(x.children[i], pred)
        elif len(x.children[i + 1].keys) >= t:
            succ = self._successor(x.children[i + 1])
            x.keys[i] = succ
            self._delete_from(x.children[i + 1], succ)
        else:
            self._merge_children(x, i)
            self._delete_from(x.children[i], key)

    def _predecessor(self, x: BTreeNode) -> Any:
        while not x.leaf:
            x = x.children[-1]
        return x.keys[-1]

    def _successor(self, x: BTreeNode) -> Any:
        while not x.leaf:
            x = x.children[0]
        return x.keys[0]

    def _ensure_min_keys(self, parent: BTreeNode, i: int) -> None:
        t = self._t
        if i > 0 and len(parent.children[i - 1].keys) >= t:
            self._rotate_right(parent, i)
        elif i < len(parent.children) - 1 and len(parent.children[i + 1].keys) >= t:
            self._rotate_left(parent, i)
        else:
            if i < len(parent.children) - 1:
                self._merge_children(parent, i)
            else:
                self._merge_children(parent, i - 1)

    def _rotate_right(self, parent: BTreeNode, i: int) -> None:
        child = parent.children[i]
        left = parent.children[i - 1]
        child.keys.insert(0, parent.keys[i - 1])
        if not child.leaf:
            c = left.children.pop()
            child.children.insert(0, c)
        parent.keys[i - 1] = left.keys.pop()

    def _rotate_left(self, parent: BTreeNode, i: int) -> None:
        child = parent.children[i]
        right = parent.children[i + 1]
        child.keys.append(parent.keys[i])
        if not child.leaf:
            c = right.children.pop(0)
            child.children.append(c)
        parent.keys[i] = right.keys.pop(0)

    def _merge_children(self, parent: BTreeNode, i: int) -> None:
        child = parent.children[i]
        sib = parent.children[i + 1]
        mid = parent.keys.pop(i)
        child.keys.append(mid)
        child.keys.extend(sib.keys)
        if not child.leaf:
            child.children.extend(sib.children)
        parent.children.pop(i + 1)

    def items(self) -> Iterator[Any]:
        yield from self._inorder(self._root)

    def _inorder(self, x: Optional[BTreeNode]) -> Iterator[Any]:
        if x is None:
            return
        if x.leaf:
            for k in x.keys:
                yield k
            return
        for i in range(len(x.keys)):
            yield from self._inorder(x.children[i])
            yield x.keys[i]
        yield from self._inorder(x.children[-1])
