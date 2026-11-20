#!/usr/bin/env python3
"""Textbook RSA key generation (via extended GCD), encryption, and decryption."""
from __future__ import annotations


def egcd(a: int, b: int) -> tuple[int, int, int]:
    if b == 0:
        return a, 1, 0
    g, x1, y1 = egcd(b, a % b)
    return g, y1, x1 - (a // b) * y1


def generate_keys(
    p: int, q: int, e: int = 65537
) -> tuple[tuple[int, int], tuple[int, int]]:
    n = p * q
    phi = (p - 1) * (q - 1)
    g, x, _ = egcd(e, phi)
    if g != 1:
        raise ValueError("e must be coprime to phi(n)")
    d = x % phi
    return (e, n), (d, n)


def rsa_encrypt(m: int, pub: tuple[int, int]) -> int:
    e, n = pub
    if not (0 <= m < n):
        raise ValueError("Message integer must satisfy 0 <= m < n")
    return pow(m, e, n)


def rsa_decrypt(c: int, priv: tuple[int, int]) -> int:
    d, n = priv
    return pow(c, d, n)


def self_check() -> None:
    pub, priv = generate_keys(61, 53, e=17)
    ct = rsa_encrypt(65, pub)
    assert ct == 2790
    assert rsa_decrypt(ct, priv) == 65
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
