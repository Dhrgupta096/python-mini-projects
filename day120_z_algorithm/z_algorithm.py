#!/usr/bin/env python3
"""Linear-time Z-array construction and exact pattern matching."""
from __future__ import annotations


def compute_z(s: str) -> list[int]:
    n = len(s)
    z = [0] * n
    l = r = 0
    for i in range(1, n):
        if i <= r:
            z[i] = min(r - i + 1, z[i - l])
        while i + z[i] < n and s[z[i]] == s[i + z[i]]:
            z[i] += 1
        if i + z[i] - 1 > r:
            l, r = i, i + z[i] - 1
    return z


def z_search(pattern: str, text: str) -> list[int]:
    if not pattern:
        return []
    combined = pattern + chr(0) + text
    z = compute_z(combined)
    m = len(pattern)
    return [i - m - 1 for i in range(m + 1, len(combined)) if z[i] == m]


def self_check() -> None:
    assert compute_z("aabxaab") == [0, 1, 0, 0, 3, 1, 0]
    assert z_search("aba", "abacaba") == [0, 4]
    assert z_search("zzz", "abacaba") == []
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
