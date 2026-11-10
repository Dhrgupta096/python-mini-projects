#!/usr/bin/env python3
"""Line-by-line text difference engine using Longest Common Subsequence."""
from __future__ import annotations


def compute_lcs(a: list[str], b: list[str]) -> list[list[int]]:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])
    return dp


def diff_lines(text1: str, text2: str) -> list[str]:
    a = text1.splitlines()
    b = text2.splitlines()
    dp = compute_lcs(a, b)
    i, j = len(a), len(b)
    result: list[str] = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            result.append(f"  {a[i - 1]}")
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            result.append(f"+ {b[j - 1]}")
            j -= 1
        else:
            result.append(f"- {a[i - 1]}")
            i -= 1
    return list(reversed(result))


def self_check() -> None:
    t1 = "alpha\nbeta\ngamma"
    t2 = "alpha\nbeta\ndelta"
    d = diff_lines(t1, t2)
    assert "  alpha" in d
    assert "  beta" in d
    assert "- gamma" in d
    assert "+ delta" in d
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
