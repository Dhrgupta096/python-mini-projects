#!/usr/bin/env python3
"""Binary tree Rope data structure for fast string concatenation and indexing."""
from __future__ import annotations


class RopeNode:
    def __init__(self, text: str = "", left: RopeNode | None = None, right: RopeNode | None = None):
        self.text = text
        self.left = left
        self.right = right
        if left is None and right is None:
            self.weight = len(text)
        else:
            self.weight = _total_len(left)

    def __len__(self) -> int:
        return _total_len(self)


def _total_len(node: RopeNode | None) -> int:
    if node is None:
        return 0
    if node.left is None and node.right is None:
        return len(node.text)
    return node.weight + _total_len(node.right)


def concat(left: RopeNode, right: RopeNode) -> RopeNode:
    return RopeNode("", left=left, right=right)


def char_at(node: RopeNode, index: int) -> str:
    if index < 0 or index >= len(node):
        raise IndexError("Rope index out of range")
    curr: RopeNode | None = node
    while curr is not None:
        if curr.left is None and curr.right is None:
            return curr.text[index]
        if index < curr.weight:
            curr = curr.left
        else:
            index -= curr.weight
            curr = curr.right
    raise IndexError("Rope index out of range")


def to_string(node: RopeNode | None) -> str:
    if node is None:
        return ""
    if node.left is None and node.right is None:
        return node.text
    return to_string(node.left) + to_string(node.right)


def self_check() -> None:
    r1 = RopeNode("Hello, ")
    r2 = RopeNode("Python ")
    r3 = RopeNode("Rope!")
    full = concat(concat(r1, r2), r3)
    assert len(full) == 19
    assert to_string(full) == "Hello, Python Rope!"
    assert char_at(full, 0) == "H"
    assert char_at(full, 7) == "P"
    assert char_at(full, 18) == "!"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
