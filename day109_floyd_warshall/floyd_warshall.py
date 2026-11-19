#!/usr/bin/env python3
"""Floyd-Warshall dynamic programming algorithm for all-pairs shortest paths."""
from __future__ import annotations


def floyd_warshall(n: int, edges: list[tuple[int, int, float]]) -> list[list[float]]:
    inf = float("inf")
    dist = [[0.0 if i == j else inf for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        if w < dist[u][v]:
            dist[u][v] = float(w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist


def self_check() -> None:
    edges = [(0, 1, 3), (0, 3, 7), (1, 0, 8), (1, 2, 2), (2, 0, 5), (2, 3, 1), (3, 0, 2)]
    dist = floyd_warshall(4, edges)
    assert dist[0] == [0.0, 3.0, 5.0, 6.0]
    assert dist[3][2] == 7.0
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
