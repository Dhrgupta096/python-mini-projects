#!/usr/bin/env python3
"""Tarjan's O(V+E) algorithm for finding Strongly Connected Components (SCCs)."""
from __future__ import annotations


def tarjan_scc(graph: dict[str, list[str]]) -> list[list[str]]:
    index = 0
    indices: dict[str, int] = {}
    lowlink: dict[str, int] = {}
    stack: list[str] = []
    on_stack: set[str] = set()
    sccs: list[list[str]] = []

    def strongconnect(v: str) -> None:
        nonlocal index
        indices[v] = lowlink[v] = index
        index += 1
        stack.append(v)
        on_stack.add(v)
        for w in graph.get(v, []):
            if w not in indices:
                strongconnect(w)
                lowlink[v] = min(lowlink[v], lowlink[w])
            elif w in on_stack:
                lowlink[v] = min(lowlink[v], indices[w])
        if lowlink[v] == indices[v]:
            comp: list[str] = []
            while True:
                w = stack.pop()
                on_stack.remove(w)
                comp.append(w)
                if w == v:
                    break
            sccs.append(sorted(comp))

    for node in sorted(graph):
        if node not in indices:
            strongconnect(node)
    return sorted(sccs)


def self_check() -> None:
    dg = {"A": ["B"], "B": ["C", "E"], "C": ["A"], "D": ["C"], "E": ["F"], "F": ["E"]}
    assert tarjan_scc(dg) == [["A", "B", "C"], ["D"], ["E", "F"]]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
