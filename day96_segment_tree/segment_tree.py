#!/usr/bin/env python3
"""Iterative Segment Tree for O(log n) range sum queries and point updates."""
from __future__ import annotations


class SegmentTree:
    def __init__(self, data: list[int]):
        self.n = len(data)
        self.tree = [0] * (2 * self.n)
        for i, val in enumerate(data):
            self.tree[self.n + i] = val
        for i in range(self.n - 1, 0, -1):
            self.tree[i] = self.tree[2 * i] + self.tree[2 * i + 1]

    def update(self, index: int, value: int) -> None:
        pos = index + self.n
        self.tree[pos] = value
        while pos > 1:
            pos //= 2
            self.tree[pos] = self.tree[2 * pos] + self.tree[2 * pos + 1]

    def query(self, left: int, right: int) -> int:
        """Return sum on half-open interval [left, right)."""
        res = 0
        l = left + self.n
        r = right + self.n
        while l < r:
            if l & 1:
                res += self.tree[l]
                l += 1
            if r & 1:
                r -= 1
                res += self.tree[r]
            l //= 2
            r //= 2
        return res


def self_check() -> None:
    st = SegmentTree([1, 3, 5, 7, 9, 11])
    assert st.query(0, 6) == 36
    assert st.query(1, 4) == 15
    st.update(2, 10)
    assert st.query(1, 4) == 20
    assert st.query(0, 6) == 41
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
