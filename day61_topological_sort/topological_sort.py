#!/usr/bin/env python3
"""Kahn's algorithm for topological sorting of Directed Acyclic Graphs."""
from __future__ import annotations
from collections import deque, defaultdict


def topological_sort(graph: dict[str, list[str]]) -> list[str]:
    in_degree = defaultdict(int)
    all_nodes = set(graph.keys())
    for node, neighbors in graph.items():
        for nbr in neighbors:
            in_degree[nbr] += 1
            all_nodes.add(nbr)
    queue = deque([n for n in all_nodes if in_degree[n] == 0])
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nbr in graph.get(node, []):
            in_degree[nbr] -= 1
            if in_degree[nbr] == 0:
                queue.append(nbr)
    if len(order) != len(all_nodes):
        raise ValueError("Cycle detected in graph")
    return order


def self_check() -> None:
    g = {
        "build": ["test"],
        "lint": ["test"],
        "test": ["package"],
        "package": ["deploy"],
        "deploy": [],
    }
    order = topological_sort(g)
    assert order.index("test") > order.index("build")
    assert order.index("test") > order.index("lint")
    assert order.index("deploy") > order.index("package")
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
