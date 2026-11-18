#!/usr/bin/env python3
"""Vitter Algorithm R Reservoir Sampling for uniform random k-samples over streams."""
from __future__ import annotations
import random
from typing import Iterable, TypeVar

T = TypeVar("T")


def reservoir_sample(stream: Iterable[T], k: int, rng: random.Random | None = None) -> list[T]:
    if k < 0:
        raise ValueError("Sample size k must be non-negative")
    if k == 0:
        return []
    r = rng or random.Random()
    reservoir: list[T] = []
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = r.randint(0, i)
            if j < k:
                reservoir[j] = item
    return reservoir


def self_check() -> None:
    rng = random.Random(42)
    sample = reservoir_sample(range(1000), 10, rng=rng)
    assert len(sample) == 10
    assert len(set(sample)) == 10
    assert all(0 <= x < 1000 for x in sample)
    assert reservoir_sample([1, 2, 3], 5, rng=rng) == [1, 2, 3]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
