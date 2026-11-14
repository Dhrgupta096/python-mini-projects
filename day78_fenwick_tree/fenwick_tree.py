#!/usr/bin/env python3
"""Binary Indexed Tree (Fenwick Tree) for O(log n) point updates and prefix sums."""
from __future__ import annotations


class FenwickTree:
    def __init__(self, size: int):
        self.size = size
        self.tree = [0] * (size + 1)

    def add(self, index: int, delta: int) -> None:
        idx = index + 1
        while idx <= self.size:
            self.tree[idx] += delta
            idx += idx & -idx

    def prefix_sum(self, index: int) -> int:
        idx = index + 1
        total = 0
        while idx > 0:
            total += self.tree[idx]
            idx -= idx & -idx
        return total

    def range_sum(self, left: int, right: int) -> int:
        if left > right:
            return 0
        return self.prefix_sum(right) - (self.prefix_sum(left - 1) if left > 0 else 0)


def self_check() -> None:
    vals = [3, 2, -1, 6, 5, 4, -3, 3, 7]
    bit = FenwickTree(len(vals))
    for i, v in enumerate(vals):
        bit.add(i, v)
    assert bit.prefix_sum(4) == sum(vals[:5])
    assert bit.range_sum(2, 6) == sum(vals[2:7])
    bit.add(3, 4)
    assert bit.range_sum(2, 6) == sum(vals[2:7]) + 4
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
