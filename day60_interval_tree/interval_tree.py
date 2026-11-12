#!/usr/bin/env python3
"""Augmented 1D Interval Tree for fast overlap queries."""
from __future__ import annotations


class IntervalNode:
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        self.max_end = end
        self.left: IntervalNode | None = None
        self.right: IntervalNode | None = None


def insert_interval(root: IntervalNode | None, start: int, end: int) -> IntervalNode:
    if not root:
        return IntervalNode(start, end)
    if start < root.start:
        root.left = insert_interval(root.left, start, end)
    else:
        root.right = insert_interval(root.right, start, end)
    root.max_end = max(root.max_end, end)
    return root


def query_overlaps(root: IntervalNode | None, start: int, end: int) -> list[tuple[int, int]]:
    results: list[tuple[int, int]] = []
    if not root or root.max_end < start:
        return results
    if root.left and root.left.max_end >= start:
        results.extend(query_overlaps(root.left, start, end))
    if not (root.end < start or root.start > end):
        results.append((root.start, root.end))
    if root.right and root.start <= end:
        results.extend(query_overlaps(root.right, start, end))
    return results


def self_check() -> None:
    root = None
    intervals = [(15, 20), (10, 30), (17, 19), (5, 20), (12, 15), (30, 40)]
    for s, e in intervals:
        root = insert_interval(root, s, e)
    overlaps = query_overlaps(root, 14, 16)
    assert (15, 20) in overlaps
    assert (10, 30) in overlaps
    assert (5, 20) in overlaps
    assert (30, 40) not in overlaps
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
