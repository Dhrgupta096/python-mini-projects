#!/usr/bin/env python3
"""Shannon-Fano optimal prefix-free binary code tree generator."""
from __future__ import annotations


def shannon_fano(frequencies: dict[str, int]) -> dict[str, str]:
    if not frequencies:
        return {}
    sorted_items = sorted(frequencies.items(), key=lambda kv: kv[1], reverse=True)
    codes = {sym: "" for sym, _ in sorted_items}

    def partition(items: list[tuple[str, int]], prefix: str) -> None:
        if len(items) == 1:
            sym, _ = items[0]
            codes[sym] = prefix or "0"
            return
        total = sum(freq for _, freq in items)
        running = 0
        split_idx = 0
        min_diff = total
        for i, (_, freq) in enumerate(items):
            running += freq
            diff = abs(total - 2 * running)
            if diff < min_diff:
                min_diff = diff
                split_idx = i + 1
        left = items[:split_idx]
        right = items[split_idx:]
        partition(left, prefix + "0")
        partition(right, prefix + "1")

    partition(sorted_items, "")
    return codes


def self_check() -> None:
    freqs = {"A": 15, "B": 7, "C": 6, "D": 6, "E": 5}
    codes = shannon_fano(freqs)
    assert len(codes) == 5
    assert len(set(codes.values())) == 5
    for c1 in codes.values():
        for c2 in codes.values():
            if c1 != c2:
                assert not c1.startswith(c2)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
