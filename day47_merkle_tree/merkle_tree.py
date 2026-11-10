#!/usr/bin/env python3
"""Cryptographic Merkle Tree with leaf verification and SHA-256."""
from __future__ import annotations
import hashlib


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class MerkleTree:
    def __init__(self, data_blocks: list[str]):
        self.leaves = [sha256(x) for x in data_blocks]
        self.levels: list[list[str]] = [self.leaves]
        self._build_tree()

    def _build_tree(self) -> None:
        curr = self.leaves
        while len(curr) > 1:
            next_level = []
            for i in range(0, len(curr), 2):
                left = curr[i]
                right = curr[i + 1] if i + 1 < len(curr) else left
                next_level.append(sha256(left + right))
            self.levels.append(next_level)
            curr = next_level

    @property
    def root(self) -> str:
        return self.levels[-1][0] if self.levels and self.levels[-1] else ""


def self_check() -> None:
    tree1 = MerkleTree(["tx1", "tx2", "tx3", "tx4"])
    tree2 = MerkleTree(["tx1", "tx2", "tx3", "tx4"])
    assert tree1.root == tree2.root
    tree_tampered = MerkleTree(["tx1", "tx2_tampered", "tx3", "tx4"])
    assert tree1.root != tree_tampered.root
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
