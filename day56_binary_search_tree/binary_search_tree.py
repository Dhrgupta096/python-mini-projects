#!/usr/bin/env python3
"""Self-balancing AVL Binary Search Tree implementation."""
from __future__ import annotations


class AVLNode:
    def __init__(self, key: int):
        self.key = key
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None
        self.height = 1


def get_height(node: AVLNode | None) -> int:
    return node.height if node else 0


def get_balance(node: AVLNode | None) -> int:
    return get_height(node.left) - get_height(node.right) if node else 0


def rotate_right(y: AVLNode) -> AVLNode:
    x = y.left
    assert x is not None
    t2 = x.right
    x.right = y
    y.left = t2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def rotate_left(x: AVLNode) -> AVLNode:
    y = x.right
    assert y is not None
    t2 = y.left
    y.left = x
    x.right = t2
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def insert_avl(root: AVLNode | None, key: int) -> AVLNode:
    if not root:
        return AVLNode(key)
    if key < root.key:
        root.left = insert_avl(root.left, key)
    elif key > root.key:
        root.right = insert_avl(root.right, key)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    bal = get_balance(root)

    if bal > 1 and root.left and key < root.left.key:
        return rotate_right(root)
    if bal < -1 and root.right and key > root.right.key:
        return rotate_left(root)
    if bal > 1 and root.left and key > root.left.key:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if bal < -1 and root.right and key < root.right.key:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root


def inorder(root: AVLNode | None) -> list[int]:
    return inorder(root.left) + [root.key] + inorder(root.right) if root else []


def self_check() -> None:
    root = None
    keys = [10, 20, 30, 40, 50, 25]
    for k in keys:
        root = insert_avl(root, k)
    assert inorder(root) == sorted(keys)
    assert abs(get_balance(root)) <= 1
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
