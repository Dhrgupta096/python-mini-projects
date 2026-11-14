#!/usr/bin/env python3
"""Least-Significant-Digit (LSD) Radix Sort for integers."""
from __future__ import annotations


def radix_sort(arr: list[int]) -> list[int]:
    if not arr:
        return []
    positives = [x for x in arr if x >= 0]
    negatives = [-x for x in arr if x < 0]

    def _counting_radix(nums: list[int]) -> list[int]:
        if not nums:
            return []
        max_num = max(nums)
        exp = 1
        output = list(nums)
        while max_num // exp > 0:
            buckets = [[] for _ in range(10)]
            for val in output:
                digit = (val // exp) % 10
                buckets[digit].append(val)
            output = [item for b in buckets for item in b]
            exp *= 10
        return output

    sorted_pos = _counting_radix(positives)
    sorted_neg = [-x for x in reversed(_counting_radix(negatives))]
    return sorted_neg + sorted_pos


def self_check() -> None:
    sample = [170, 45, 75, 90, -802, 24, 2, -66, 0]
    sorted_arr = radix_sort(sample)
    assert sorted_arr == sorted(sample)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
