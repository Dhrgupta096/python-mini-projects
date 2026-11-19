#!/usr/bin/env python3
"""Min-heap Dijkstra shortest path solver with path reconstruction."""
from __future__ import annotations
import heapq


def dijkstra(
    graph: dict[str, list[tuple[str, float]]], start: str, goal: str
) -> tuple[float, list[str]]:
    dist: dict[str, float] = {start: 0.0}
    prev: dict[str, str | None] = {start: None}
    pq: list[tuple[float, str]] = [(0.0, start)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist.get(u, float("inf")):
            continue
        if u == goal:
            break
        for v, w in graph.get(u, []):
            nd = d + w
            if nd < dist.get(v, float("inf")):
                dist[v] = nd
                prev[v] = u
                heapq.heappush(pq, (nd, v))
    if goal not in dist:
        return float("inf"), []
    path: list[str] = []
    curr: str | None = goal
    while curr is not None:
        path.append(curr)
        curr = prev[curr]
    return dist[goal], path[::-1]


def self_check() -> None:
    graph = {
        "A": [("B", 2), ("C", 5)],
        "B": [("C", 1), ("D", 4)],
        "C": [("D", 1)],
        "D": [],
    }
    assert dijkstra(graph, "A", "D") == (4.0, ["A", "B", "C", "D"])
    assert dijkstra(graph, "D", "A") == (float("inf"), [])
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
