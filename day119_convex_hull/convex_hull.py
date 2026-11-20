#!/usr/bin/env python3
"""Andrew's monotone chain O(n log n) 2D convex hull algorithm."""
from __future__ import annotations

Point = tuple[float, float]


def _cross(o: Point, a: Point, b: Point) -> float:
    return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])


def convex_hull(points: list[Point]) -> list[Point]:
    pts = sorted(set(points))
    if len(pts) <= 1:
        return pts
    lower: list[Point] = []
    for p in pts:
        while len(lower) >= 2 and _cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: list[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and _cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def self_check() -> None:
    hull = convex_hull([(0, 0), (1, 1), (2, 2), (0, 2), (2, 0), (1, 0.5)])
    assert hull == [(0, 0), (2, 0), (2, 2), (0, 2)]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
