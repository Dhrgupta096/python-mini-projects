#!/usr/bin/env python3
"""Rabin-Karp rolling polynomial hash substring search."""
from __future__ import annotations


def rabin_karp(pattern: str, text: str) -> list[int]:
    m, n = len(pattern), len(text)
    if m == 0 or n < m:
        return []
    base, mod = 256, 1_000_000_007
    high = pow(base, m - 1, mod)
    p_hash = t_hash = 0
    for i in range(m):
        p_hash = (p_hash * base + ord(pattern[i])) % mod
        t_hash = (t_hash * base + ord(text[i])) % mod
    matches: list[int] = []
    for i in range(n - m + 1):
        if p_hash == t_hash and text[i : i + m] == pattern:
            matches.append(i)
        if i < n - m:
            t_hash = ((t_hash - ord(text[i]) * high) * base + ord(text[i + m])) % mod
    return matches


def self_check() -> None:
    assert rabin_karp("ana", "banana") == [1, 3]
    assert rabin_karp("xyz", "banana") == []
    assert rabin_karp("aa", "aaaa") == [0, 1, 2]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
