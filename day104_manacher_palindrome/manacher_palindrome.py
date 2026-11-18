#!/usr/bin/env python3
"""Manacher's O(n) algorithm to find the longest palindromic substring."""
from __future__ import annotations


def longest_palindrome(s: str) -> str:
    if not s:
        return ""
    t = "^#" + "#".join(s) + "#$"
    p = [0] * len(t)
    center = right = 0
    for i in range(1, len(t) - 1):
        mirror = 2 * center - i
        if i < right:
            p[i] = min(right - i, p[mirror])
        while t[i + p[i] + 1] == t[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > right:
            center = i
            right = i + p[i]

    max_len = max(p)
    max_center = p.index(max_len)
    start = (max_center - max_len) // 2
    return s[start : start + max_len]


def self_check() -> None:
    assert longest_palindrome("babad") in ("bab", "aba")
    assert longest_palindrome("cbbd") == "bb"
    assert longest_palindrome("racecar") == "racecar"
    assert longest_palindrome("") == ""
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
