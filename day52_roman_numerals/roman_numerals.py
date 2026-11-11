#!/usr/bin/env python3
"""Bidirectional Roman numeral <-> Arabic integer converter."""
from __future__ import annotations

MAPPINGS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
]


def to_roman(n: int) -> str:
    if not (1 <= n <= 3999):
        raise ValueError("Number out of Roman numeral range (1-3999)")
    result = []
    for val, sym in MAPPINGS:
        while n >= val:
            result.append(sym)
            n -= val
    return "".join(result)


def from_roman(s: str) -> int:
    val_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        curr = val_map[ch]
        total = (total - curr) if curr < prev else (total + curr)
        prev = curr
    return total


def self_check() -> None:
    assert to_roman(1994) == "MCMXCIV"
    assert from_roman("MCMXCIV") == 1994
    assert to_roman(58) == "LVIII"
    assert from_roman("LVIII") == 58
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
