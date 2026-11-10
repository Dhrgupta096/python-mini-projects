#!/usr/bin/env python3
"""Probabilistic Bloom filter with polynomial hash functions."""
from __future__ import annotations


class BloomFilter:
    def __init__(self, size: int = 1024, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = [0] * size

    def _hashes(self, item: str) -> list[int]:
        hashes = []
        for seed in range(self.num_hashes):
            h = 0
            for ch in item:
                h = (h * (31 + seed) + ord(ch)) % self.size
            hashes.append(h)
        return hashes

    def add(self, item: str) -> None:
        for idx in self._hashes(item):
            self.bits[idx] = 1

    def might_contain(self, item: str) -> bool:
        return all(self.bits[idx] == 1 for idx in self._hashes(item))


def self_check() -> None:
    bf = BloomFilter(size=512, num_hashes=3)
    bf.add("apple")
    bf.add("banana")
    assert bf.might_contain("apple")
    assert bf.might_contain("banana")
    assert not bf.might_contain("grapefruit_xyz_not_added")
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
