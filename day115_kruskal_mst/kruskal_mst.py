#!/usr/bin/env python3
"""Kruskal's greedy Minimum Spanning Tree (MST) using Union-Find."""
from __future__ import annotations


def kruskal_mst(
    vertices: list[str], edges: list[tuple[str, str, float]]
) -> tuple[float, list[tuple[str, str, float]]]:
    parent = {v: v for v in vertices}
    rank = {v: 0 for v in vertices}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        if rank[ra] < rank[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        if rank[ra] == rank[rb]:
            rank[ra] += 1
        return True

    mst: list[tuple[str, str, float]] = []
    total = 0.0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        if union(u, v):
            mst.append((u, v, w))
            total += w
    return total, mst


def self_check() -> None:
    cost, tree = kruskal_mst(
        ["A", "B", "C", "D"],
        [("A", "B", 1), ("B", "C", 2), ("A", "C", 3), ("C", "D", 4), ("B", "D", 5)],
    )
    assert cost == 7.0
    assert len(tree) == 3
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
