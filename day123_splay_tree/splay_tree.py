#!/usr/bin/env python3
"""Self-adjusting Splay Binary Search Tree with amortized O(log n) operations."""
from __future__ import annotations


class SplayNode:
    def __init__(self, key: int):
        self.key = key
        self.left: SplayNode | None = None
        self.right: SplayNode | None = None


class SplayTree:
    def __init__(self):
        self.root: SplayNode | None = None

    def _rot_right(self, x: SplayNode) -> SplayNode:
        y = x.left
        assert y is not None
        x.left = y.right
        y.right = x
        return y

    def _rot_left(self, x: SplayNode) -> SplayNode:
        y = x.right
        assert y is not None
        x.right = y.left
        y.left = x
        return y

    def _splay(self, node: SplayNode | None, key: int) -> SplayNode | None:
        if node is None or node.key == key:
            return node
        if key < node.key:
            if node.left is None:
                return node
            if key < node.left.key:
                node.left.left = self._splay(node.left.left, key)
                node = self._rot_right(node)
            elif key > node.left.key:
                node.left.right = self._splay(node.left.right, key)
                if node.left.right is not None:
                    node.left = self._rot_left(node.left)
            return node if node.left is None else self._rot_right(node)
        else:
            if node.right is None:
                return node
            if key > node.right.key:
                node.right.right = self._splay(node.right.right, key)
                node = self._rot_left(node)
            elif key < node.right.key:
                node.right.left = self._splay(node.right.left, key)
                if node.right.left is not None:
                    node.right = self._rot_right(node.right)
            return node if node.right is None else self._rot_left(node)

    def insert(self, key: int) -> None:
        if self.root is None:
            self.root = SplayNode(key)
            return
        self.root = self._splay(self.root, key)
        assert self.root is not None
        if self.root.key == key:
            return
        node = SplayNode(key)
        if key < self.root.key:
            node.right = self.root
            node.left = self.root.left
            self.root.left = None
        else:
            node.left = self.root
            node.right = self.root.right
            self.root.right = None
        self.root = node

    def search(self, key: int) -> bool:
        self.root = self._splay(self.root, key)
        return self.root is not None and self.root.key == key


def self_check() -> None:
    st = SplayTree()
    for v in [10, 20, 30, 40, 50, 25]:
        st.insert(v)
    assert st.search(25) and st.root is not None and st.root.key == 25
    assert st.search(10) and st.root.key == 10
    assert not st.search(99)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
