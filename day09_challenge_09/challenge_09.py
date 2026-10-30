#!/usr/bin/env python3
"""Day 09: Python Algorithm Challenge #09 — number theory & sequence utility."""
from __future__ import annotations


def solve_challenge(n: int) -> list[int]:
    """Return the first n primes greater than or equal to 9."""
    primes: list[int] = []
    candidate = max(2, 9)
    while len(primes) < n:
        if all(candidate % d != 0 for d in range(2, int(candidate ** 0.5) + 1)):
            primes.append(candidate)
        candidate += 1
    return primes


def self_check() -> None:
    result = solve_challenge(5)
    assert len(result) == 5
    assert all( result[i] < result[i + 1] for i in range(4) )
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
