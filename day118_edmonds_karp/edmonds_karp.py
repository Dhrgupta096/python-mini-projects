#!/usr/bin/env python3
"""Edmonds-Karp BFS-based Ford-Fulkerson maximum network flow solver."""
from __future__ import annotations
from collections import defaultdict, deque


def max_flow(edges: list[tuple[str, str, int]], source: str, sink: str) -> int:
    cap: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    adj: dict[str, set[str]] = defaultdict(set)
    for u, v, c in edges:
        cap[u][v] += c
        adj[u].add(v)
        adj[v].add(u)

    total = 0
    while True:
        parent: dict[str, str | None] = {source: None}
        q: deque[str] = deque([source])
        while q and sink not in parent:
            u = q.popleft()
            for v in adj[u]:
                if v not in parent and cap[u][v] > 0:
                    parent[v] = u
                    q.append(v)
        if sink not in parent:
            break
        bottleneck = float("inf")
        v = sink
        while v != source:
            u = parent[v]
            assert u is not None
            bottleneck = min(bottleneck, cap[u][v])
            v = u
        flow = int(bottleneck)
        v = sink
        while v != source:
            u = parent[v]
            assert u is not None
            cap[u][v] -= flow
            cap[v][u] += flow
            v = u
        total += flow
    return total


def self_check() -> None:
    edges = [("S", "A", 10), ("S", "B", 5), ("A", "B", 15), ("A", "T", 5), ("B", "T", 10)]
    assert max_flow(edges, "S", "T") == 15
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
