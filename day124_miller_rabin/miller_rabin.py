#!/usr/bin/env python3
"""Deterministic 64-bit Miller-Rabin primality testing utility."""
from __future__ import annotations


def is_probable_prime(n: int) -> bool:
    if n < 2:
        return False
    small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
    for p in small:
        if n == p:
            return True
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in small:
        if a >= n:
            continue
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def self_check() -> None:
    assert is_probable_prime(2)
    assert is_probable_prime(1_000_000_007)
    assert is_probable_prime(2_147_483_647)
    assert not is_probable_prime(561)
    assert not is_probable_prime(1_000_000_009 * 3)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
