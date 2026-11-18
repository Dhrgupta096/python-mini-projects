#!/usr/bin/env python3
"""HyperLogLog probabilistic distinct-count cardinality estimator."""
from __future__ import annotations
import hashlib
import math


class HyperLogLog:
    def __init__(self, b: int = 8):
        self.b = b
        self.m = 1 << b
        self.registers = [0] * self.m
        self.alpha = 0.7213 / (1.0 + 1.079 / self.m)

    def _hash64(self, item: str) -> int:
        digest = hashlib.sha256(item.encode("utf-8")).digest()
        return int.from_bytes(digest[:8], "big")

    def add(self, item: str) -> None:
        x = self._hash64(item)
        idx = x >> (64 - self.b)
        w = x & ((1 << (64 - self.b)) - 1)
        rho = (64 - self.b) - w.bit_length() + 1 if w != 0 else (64 - self.b + 1)
        if rho > self.registers[idx]:
            self.registers[idx] = rho

    def count(self) -> int:
        z = sum(2.0 ** (-r) for r in self.registers)
        est = self.alpha * (self.m ** 2) / z
        if est <= 2.5 * self.m:
            zeros = self.registers.count(0)
            if zeros > 0:
                est = self.m * math.log(self.m / zeros)
        return round(est)


def self_check() -> None:
    hll = HyperLogLog(b=10)
    for i in range(1000):
        hll.add(f"user_{i}")
    for i in range(500):
        hll.add(f"user_{i}")
    est = hll.count()
    assert 850 <= est <= 1150, f"Unexpected estimate: {est}"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
