#!/usr/bin/env python3
"""Cuckoo Hash Table with O(1) worst-case lookup and automatic rehashing."""
from __future__ import annotations
import hashlib


class CuckooHashTable:
    def __init__(self, capacity: int = 16):
        self.capacity = capacity
        self.t1: list[tuple[str, int] | None] = [None] * capacity
        self.t2: list[tuple[str, int] | None] = [None] * capacity
        self.seed = 0

    def _h1(self, key: str) -> int:
        return int(hashlib.md5(f"1:{self.seed}:{key}".encode()).hexdigest(), 16) % self.capacity

    def _h2(self, key: str) -> int:
        return int(hashlib.sha256(f"2:{self.seed}:{key}".encode()).hexdigest(), 16) % self.capacity

    def get(self, key: str) -> int | None:
        i1 = self._h1(key)
        if self.t1[i1] and self.t1[i1][0] == key:
            return self.t1[i1][1]
        i2 = self._h2(key)
        if self.t2[i2] and self.t2[i2][0] == key:
            return self.t2[i2][1]
        return None

    def delete(self, key: str) -> bool:
        i1 = self._h1(key)
        if self.t1[i1] and self.t1[i1][0] == key:
            self.t1[i1] = None
            return True
        i2 = self._h2(key)
        if self.t2[i2] and self.t2[i2][0] == key:
            self.t2[i2] = None
            return True
        return False

    def _rehash(self, pending: tuple[str, int]) -> None:
        items = [x for x in self.t1 if x] + [x for x in self.t2 if x] + [pending]
        self.capacity *= 2
        self.seed += 1
        self.t1 = [None] * self.capacity
        self.t2 = [None] * self.capacity
        for k, v in items:
            self.put(k, v)

    def put(self, key: str, value: int) -> None:
        i1 = self._h1(key)
        if self.t1[i1] and self.t1[i1][0] == key:
            self.t1[i1] = (key, value)
            return
        i2 = self._h2(key)
        if self.t2[i2] and self.t2[i2][0] == key:
            self.t2[i2] = (key, value)
            return
        item: tuple[str, int] = (key, value)
        for _ in range(self.capacity):
            idx = self._h1(item[0])
            if self.t1[idx] is None:
                self.t1[idx] = item
                return
            item, self.t1[idx] = self.t1[idx], item
            idx2 = self._h2(item[0])
            if self.t2[idx2] is None:
                self.t2[idx2] = item
                return
            item, self.t2[idx2] = self.t2[idx2], item
        self._rehash(item)


def self_check() -> None:
    ch = CuckooHashTable(4)
    for i in range(20):
        ch.put(f"k{i}", i * 10)
    for i in range(20):
        assert ch.get(f"k{i}") == i * 10
    ch.put("k5", 999)
    assert ch.get("k5") == 999
    assert ch.delete("k5")
    assert ch.get("k5") is None
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
