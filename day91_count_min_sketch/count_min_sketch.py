#!/usr/bin/env python3
"""Count-Min Sketch probabilistic data structure for frequency estimation in streams."""
from __future__ import annotations
import hashlib


class CountMinSketch:
    def __init__(self, width: int = 1000, depth: int = 5):
        self.width = width
        self.depth = depth
        self.table = [[0] * width for _ in range(depth)]

    def _hashes(self, item: str) -> list[int]:
        b = item.encode("utf-8")
        indices: list[int] = []
        for i in range(self.depth):
            h = int(hashlib.md5(b + bytes([i])).hexdigest(), 16)
            indices.append(h % self.width)
        return indices

    def add(self, item: str, count: int = 1) -> None:
        for d, idx in enumerate(self._hashes(item)):
            self.table[d][idx] += count

    def estimate(self, item: str) -> int:
        return min(self.table[d][idx] for d, idx in enumerate(self._hashes(item)))


def self_check() -> None:
    cms = CountMinSketch(width=500, depth=5)
    for _ in range(50):
        cms.add("apple")
    for _ in range(25):
        cms.add("banana")
    assert cms.estimate("apple") >= 50
    assert cms.estimate("banana") >= 25
    assert cms.estimate("cherry") == 0
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
