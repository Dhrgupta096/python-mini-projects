#!/usr/bin/env python3
"""Disjoint Set Union (DSU / Union-Find) with rank heuristic and path compression."""
from __future__ import annotations


class DisjointSet:
    def __init__(self, elements: list[str]):
        self.parent = {x: x for x in elements}
        self.rank = {x: 0 for x in elements}
        self.count = len(elements)

    def find(self, x: str) -> str:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x: str, y: str) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        self.count -= 1
        return True

    def connected(self, x: str, y: str) -> bool:
        return self.find(x) == self.find(y)


def self_check() -> None:
    dsu = DisjointSet(["A", "B", "C", "D", "E"])
    assert dsu.count == 5
    assert dsu.union("A", "B")
    assert dsu.union("B", "C")
    assert not dsu.union("A", "C")
    assert dsu.connected("A", "C")
    assert not dsu.connected("A", "D")
    assert dsu.count == 3
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
