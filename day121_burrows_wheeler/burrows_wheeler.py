#!/usr/bin/env python3
"""Burrows-Wheeler Transform (BWT) forward and inverse transform."""
from __future__ import annotations


def bwt_encode(text: str) -> tuple[str, int]:
    if not text:
        return "", 0
    n = len(text)
    rotations = sorted(range(n), key=lambda i: text[i:] + text[:i])
    encoded = "".join(text[(i - 1) % n] for i in rotations)
    primary_idx = rotations.index(0)
    return encoded, primary_idx


def bwt_decode(encoded: str, primary_idx: int) -> str:
    if not encoded:
        return ""
    n = len(encoded)
    order = sorted(range(n), key=lambda i: (encoded[i], i))
    out: list[str] = []
    idx = primary_idx
    for _ in range(n):
        idx = order[idx]
        out.append(encoded[idx])
    return "".join(out)


def self_check() -> None:
    enc, idx = bwt_encode("banana")
    assert enc == "nnbaaa"
    assert bwt_decode(enc, idx) == "banana"
    enc2, idx2 = bwt_encode("mississippi")
    assert bwt_decode(enc2, idx2) == "mississippi"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
