#!/usr/bin/env python3
"""Levenshtein edit distance and fuzzy keyword suggestion ranker."""
from __future__ import annotations


def levenshtein(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )
    return dp[m][n]


def find_closest(query: str, vocabulary: list[str]) -> str | None:
    if not vocabulary:
        return None
    return min(vocabulary, key=lambda word: levenshtein(query, word))


def self_check() -> None:
    assert levenshtein("kitten", "sitting") == 3
    vocab = ["python", "java", "javascript", "golang", "ruby"]
    assert find_closest("pythn", vocab) == "python"
    assert find_closest("rubi", vocab) == "ruby"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
