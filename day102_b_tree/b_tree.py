#!/usr/bin/env python3
"""Order-t B-Tree supporting search and balanced node-splitting insertion."""
from __future__ import annotations


class BTreeNode:
    def __init__(self, leaf: bool = False):
        self.leaf = leaf
        self.keys: list[int] = []
        self.children: list[BTreeNode] = []


class BTree:
    def __init__(self, t: int = 2):
        self.t = t
        self.root = BTreeNode(leaf=True)

    def search(self, k: int, node: BTreeNode | None = None) -> bool:
        curr = self.root if node is None else node
        i = 0
        while i < len(curr.keys) and k > curr.keys[i]:
            i += 1
        if i < len(curr.keys) and k == curr.keys[i]:
            return True
        if curr.leaf:
            return False
        return self.search(k, curr.children[i])

    def insert(self, k: int) -> None:
        r = self.root
        if len(r.keys) == 2 * self.t - 1:
            s = BTreeNode(leaf=False)
            self.root = s
            s.children.append(r)
            self._split_child(s, 0)
            self._insert_non_full(s, k)
        else:
            self._insert_non_full(r, k)

    def _split_child(self, parent: BTreeNode, i: int) -> None:
        t = self.t
        y = parent.children[i]
        z = BTreeNode(leaf=y.leaf)
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, y.keys[t - 1])
        z.keys = y.keys[t:]
        y.keys = y.keys[:t - 1]
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

    def _insert_non_full(self, x: BTreeNode, k: int) -> None:
        i = len(x.keys) - 1
        if x.leaf:
            x.keys.append(0)
            while i >= 0 and k < x.keys[i]:
                x.keys[i + 1] = x.keys[i]
                i -= 1
            x.keys[i + 1] = k
        else:
            while i >= 0 and k < x.keys[i]:
                i -= 1
            i += 1
            if len(x.children[i].keys) == 2 * self.t - 1:
                self._split_child(x, i)
                if k > x.keys[i]:
                    i += 1
            self._insert_non_full(x.children[i], k)


def self_check() -> None:
    bt = BTree(t=2)
    for val in [10, 20, 5, 6, 12, 30, 7, 17]:
        bt.insert(val)
    for val in [10, 20, 5, 6, 12, 30, 7, 17]:
        assert bt.search(val)
    assert not bt.search(99)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
