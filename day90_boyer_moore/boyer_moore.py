#!/usr/bin/env python3
"""Boyer-Moore-Horspool sublinear exact pattern searching algorithm."""
from __future__ import annotations


def bad_character_table(pattern: str) -> dict[str, int]:
    m = len(pattern)
    table: dict[str, int] = {}
    for i in range(m - 1):
        table[pattern[i]] = m - 1 - i
    return table


def search(pattern: str, text: str) -> list[int]:
    m = len(pattern)
    n = len(text)
    if m == 0 or n < m:
        return []

    shift = bad_character_table(pattern)
    matches: list[int] = []
    i = 0
    while i <= n - m:
        j = m - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            matches.append(i)
            i += shift.get(text[i + m - 1], m)
        else:
            i += shift.get(text[i + m - 1], m)
    return matches


def self_check() -> None:
    text = "ABAAABCDABC"
    assert search("ABC", text) == [4, 8]
    assert search("NOT_HERE", text) == []
    assert search("A", text) == [0, 2, 3, 4, 8]
    assert search("ABAA", text) == [0]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
