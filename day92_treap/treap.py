#!/usr/bin/env python3
"""Treap data structure combining Binary Search Tree keys and Heap priorities."""
from __future__ import annotations
import random


class TreapNode:
    def __init__(self, key: int, priority: float | None = None):
        self.key = key
        self.priority = random.random() if priority is None else priority
        self.left: TreapNode | None = None
        self.right: TreapNode | None = None


def _rotate_right(y: TreapNode) -> TreapNode:
    x = y.left
    assert x is not None
    y.left = x.right
    x.right = y
    return x


def _rotate_left(x: TreapNode) -> TreapNode:
    y = x.right
    assert y is not None
    x.right = y.left
    y.left = x
    return y


def insert(root: TreapNode | None, key: int, priority: float | None = None) -> TreapNode:
    if root is None:
        return TreapNode(key, priority)
    if key < root.key:
        root.left = insert(root.left, key, priority)
        if root.left.priority > root.priority:
            root = _rotate_right(root)
    elif key > root.key:
        root.right = insert(root.right, key, priority)
        if root.right.priority > root.priority:
            root = _rotate_left(root)
    return root


def search(root: TreapNode | None, key: int) -> bool:
    curr = root
    while curr:
        if curr.key == key:
            return True
        curr = curr.left if key < curr.key else curr.right
    return False


def inorder(root: TreapNode | None) -> list[int]:
    res: list[int] = []
    if root:
        res.extend(inorder(root.left))
        res.append(root.key)
        res.extend(inorder(root.right))
    return res


def self_check() -> None:
    root: TreapNode | None = None
    keys = [50, 30, 20, 40, 70, 60, 80]
    for k in keys:
        root = insert(root, k)
    assert inorder(root) == sorted(keys)
    assert search(root, 40)
    assert search(root, 70)
    assert not search(root, 99)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
