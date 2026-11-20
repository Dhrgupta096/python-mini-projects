#!/usr/bin/env python3
"""Gale-Shapley deferred-acceptance algorithm for stable matching."""
from __future__ import annotations


def stable_matching(
    proposers: dict[str, list[str]], receivers: dict[str, list[str]]
) -> dict[str, str]:
    rank = {r: {p: i for i, p in enumerate(prefs)} for r, prefs in receivers.items()}
    free = list(proposers.keys())
    next_idx = {p: 0 for p in proposers}
    engaged_to: dict[str, str] = {}

    while free:
        p = free.pop(0)
        r = proposers[p][next_idx[p]]
        next_idx[p] += 1
        if r not in engaged_to:
            engaged_to[r] = p
        else:
            cur = engaged_to[r]
            if rank[r][p] < rank[r][cur]:
                engaged_to[r] = p
                free.append(cur)
            else:
                free.append(p)
    return {p: r for r, p in engaged_to.items()}


def self_check() -> None:
    matches = stable_matching(
        {"A": ["X", "Y", "Z"], "B": ["Y", "X", "Z"], "C": ["X", "Y", "Z"]},
        {"X": ["B", "A", "C"], "Y": ["A", "B", "C"], "Z": ["A", "B", "C"]},
    )
    assert matches == {"A": "X", "B": "Y", "C": "Z"}
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
