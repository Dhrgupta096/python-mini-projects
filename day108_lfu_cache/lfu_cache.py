#!/usr/bin/env python3
"""O(1) Least Frequently Used (LFU) cache with LRU tie-breaking."""
from __future__ import annotations
from collections import OrderedDict, defaultdict


class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.key_val: dict[int, int] = {}
        self.key_freq: dict[int, int] = {}
        self.freq_keys: dict[int, OrderedDict[int, None]] = defaultdict(OrderedDict)
        self.min_freq = 0

    def _touch(self, key: int) -> None:
        f = self.key_freq[key]
        del self.freq_keys[f][key]
        if not self.freq_keys[f] and f == self.min_freq:
            self.min_freq += 1
        self.key_freq[key] = f + 1
        self.freq_keys[f + 1][key] = None

    def get(self, key: int) -> int:
        if key not in self.key_val:
            return -1
        self._touch(key)
        return self.key_val[key]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        if key in self.key_val:
            self.key_val[key] = value
            self._touch(key)
            return
        if len(self.key_val) >= self.capacity:
            evict_key, _ = self.freq_keys[self.min_freq].popitem(last=False)
            del self.key_val[evict_key]
            del self.key_freq[evict_key]
        self.key_val[key] = value
        self.key_freq[key] = 1
        self.freq_keys[1][key] = None
        self.min_freq = 1


def self_check() -> None:
    cache = LFUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    assert cache.get(1) == 10
    cache.put(3, 30)
    assert cache.get(2) == -1
    assert cache.get(3) == 30
    assert cache.get(1) == 10
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
