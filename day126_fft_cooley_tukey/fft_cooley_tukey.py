#!/usr/bin/env python3
"""Cooley-Tukey radix-2 Fast Fourier Transform (FFT) and polynomial multiplication."""
from __future__ import annotations
import cmath


def fft(a: list[complex], invert: bool = False) -> list[complex]:
    n = len(a)
    if n <= 1:
        return list(a)
    if n & (n - 1) != 0:
        raise ValueError("Length must be a power of 2")
    even = fft(a[0::2], invert)
    odd = fft(a[1::2], invert)
    ang = (2.0 * cmath.pi / n) * (1 if invert else -1)
    w = 1 + 0j
    wn = cmath.rect(1.0, ang)
    out = [0j] * n
    half = n // 2
    for i in range(half):
        t = w * odd[i]
        out[i] = even[i] + t
        out[i + half] = even[i] - t
        w *= wn
    if invert:
        return [x / 2.0 for x in out]
    return out


def poly_multiply(p: list[int], q: list[int]) -> list[int]:
    size = 1
    target = len(p) + len(q) - 1
    while size < target:
        size <<= 1
    fa = fft([complex(x) for x in p] + [0j] * (size - len(p)))
    fb = fft([complex(x) for x in q] + [0j] * (size - len(q)))
    fc = fft([fa[i] * fb[i] for i in range(size)], invert=True)
    return [round(fc[i].real) for i in range(target)]


def self_check() -> None:
    assert poly_multiply([1, 2, 3], [4, 5]) == [4, 13, 22, 15]
    sig = [1 + 0j, 2 + 0j, 3 + 0j, 4 + 0j]
    rec = fft(fft(sig), invert=True)
    assert all(abs(rec[i] - sig[i]) < 1e-9 for i in range(4))
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
