#!/usr/bin/env python3
"""Probabilistic Skip List with O(log n) expected search, insert, and delete."""
from __future__ import annotations
import random


class SkipNode:
    def __init__(self, key: int, value: str, level: int):
        self.key = key
        self.value = value
        self.forward: list[SkipNode | None] = [None] * (level + 1)


class SkipList:
    MAX_LEVEL = 4
    P = 0.5

    def __init__(self):
        self.level = 0
        self.header = SkipNode(-1, "", self.MAX_LEVEL)

    def _random_level(self) -> int:
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, key: int, value: str) -> None:
        update: list[SkipNode] = [self.header] * (self.MAX_LEVEL + 1)
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr
        curr = curr.forward[0]
        if curr and curr.key == key:
            curr.value = value
            return
        lvl = self._random_level()
        if lvl > self.level:
            for i in range(self.level + 1, lvl + 1):
                update[i] = self.header
            self.level = lvl
        new_node = SkipNode(key, value, lvl)
        for i in range(lvl + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

    def search(self, key: int) -> str | None:
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
        curr = curr.forward[0]
        return curr.value if (curr and curr.key == key) else None

    def delete(self, key: int) -> bool:
        update: list[SkipNode] = [self.header] * (self.MAX_LEVEL + 1)
        curr = self.header
        for i in range(self.level, -1, -1):
            while curr.forward[i] and curr.forward[i].key < key:
                curr = curr.forward[i]
            update[i] = curr
        curr = curr.forward[0]
        if not curr or curr.key != key:
            return False
        for i in range(self.level + 1):
            if update[i].forward[i] != curr:
                break
            update[i].forward[i] = curr.forward[i]
        while self.level > 0 and self.header.forward[self.level] is None:
            self.level -= 1
        return True


def self_check() -> None:
    sl = SkipList()
    sl.insert(3, "three")
    sl.insert(1, "one")
    sl.insert(7, "seven")
    sl.insert(5, "five")
    assert sl.search(1) == "one"
    assert sl.search(3) == "three"
    assert sl.search(5) == "five"
    assert sl.search(7) == "seven"
    assert sl.search(9) is None
    sl.insert(3, "THREE")
    assert sl.search(3) == "THREE"
    assert sl.delete(3)
    assert sl.search(3) is None
    assert not sl.delete(99)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
