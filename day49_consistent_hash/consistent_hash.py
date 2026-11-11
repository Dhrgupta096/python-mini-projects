#!/usr/bin/env python3
"""Consistent hashing ring with virtual nodes for distributed load-balancing."""
from __future__ import annotations
import bisect
import hashlib


class ConsistentHashRing:
    def __init__(self, vnodes: int = 10):
        self.vnodes = vnodes
        self.ring: list[int] = []
        self.node_map: dict[int, str] = {}

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        for i in range(self.vnodes):
            vkey = f"{node}#vn{i}"
            h = self._hash(vkey)
            bisect.insort(self.ring, h)
            self.node_map[h] = node

    def get_node(self, key: str) -> str | None:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.node_map[self.ring[idx]]


def self_check() -> None:
    ring = ConsistentHashRing(vnodes=5)
    ring.add_node("nodeA")
    ring.add_node("nodeB")
    ring.add_node("nodeC")
    target1 = ring.get_node("user_101")
    target2 = ring.get_node("user_102")
    assert target1 in {"nodeA", "nodeB", "nodeC"}
    assert target2 in {"nodeA", "nodeB", "nodeC"}
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
