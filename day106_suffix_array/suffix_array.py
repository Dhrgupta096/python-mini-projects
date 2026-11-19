#!/usr/bin/env python3
"""Suffix Array and Kasai's O(n) LCP array builder for string analysis."""
from __future__ import annotations


def build_suffix_array(text: str) -> list[int]:
    return sorted(range(len(text)), key=lambda i: text[i:])


def build_lcp(text: str, sa: list[int]) -> list[int]:
    n = len(text)
    if n == 0:
        return []
    rank = [0] * n
    for i, pos in enumerate(sa):
        rank[pos] = i
    lcp = [0] * n
    h = 0
    for i in range(n):
        r = rank[i]
        if r > 0:
            j = sa[r - 1]
            while i + h < n and j + h < n and text[i + h] == text[j + h]:
                h += 1
            lcp[r] = h
            if h > 0:
                h -= 1
    return lcp


def self_check() -> None:
    sa = build_suffix_array("banana")
    assert sa == [5, 3, 1, 0, 4, 2]
    assert build_lcp("banana", sa) == [0, 1, 3, 0, 0, 2]
    assert build_lcp("", []) == []
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
