#!/usr/bin/env python3
"""Bellman-Ford single-source shortest paths with negative cycle detection."""
from __future__ import annotations

Edge = tuple[str, str, float]


def bellman_ford(vertices: list[str], edges: list[Edge], source: str) -> dict[str, float]:
    dist: dict[str, float] = {v: float("inf") for v in vertices}
    dist[source] = 0.0

    for _ in range(len(vertices) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != float("inf") and dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                updated = True
        if not updated:
            break

    for u, v, w in edges:
        if dist[u] != float("inf") and dist[u] + w < dist[v]:
            raise ValueError("Graph contains a negative-weight cycle")

    return dist


def self_check() -> None:
    verts = ["A", "B", "C", "D"]
    edges: list[Edge] = [
        ("A", "B", 4),
        ("A", "C", 5),
        ("B", "C", -3),
        ("C", "D", 2),
    ]
    d = bellman_ford(verts, edges, "A")
    assert d == {"A": 0.0, "B": 4.0, "C": 1.0, "D": 3.0}

    neg_edges: list[Edge] = [("A", "B", 1), ("B", "C", -2), ("C", "A", -1)]
    try:
        bellman_ford(["A", "B", "C"], neg_edges, "A")
        assert False, "Should detect negative cycle"
    except ValueError:
        pass
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
