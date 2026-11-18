#!/usr/bin/env python3
"""Knuth-Morris-Pratt (KMP) O(n+m) exact substring search using LPS array."""
from __future__ import annotations


def build_lps(pattern: str) -> list[int]:
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        elif length != 0:
            length = lps[length - 1]
        else:
            lps[i] = 0
            i += 1
    return lps


def kmp_search(pattern: str, text: str) -> list[int]:
    if not pattern:
        return []
    lps = build_lps(pattern)
    matches: list[int] = []
    i = j = 0
    while i < len(text):
        if text[i] == pattern[j]:
            i += 1
            j += 1
            if j == len(pattern):
                matches.append(i - j)
                j = lps[j - 1]
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
    return matches


def self_check() -> None:
    assert build_lps("ABABCABAB") == [0, 0, 1, 2, 0, 1, 2, 3, 4]
    assert kmp_search("ABAB", "ABABABCABAB") == [0, 2, 7]
    assert kmp_search("XYZ", "ABCDEF") == []
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
