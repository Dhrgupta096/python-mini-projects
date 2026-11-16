#!/usr/bin/env python3
"""2D K-D Tree for spatial partitioning and exact nearest neighbor query."""
from __future__ import annotations
import math

Point2D = tuple[float, float]


class KDNode:
    def __init__(self, point: Point2D, left: KDNode | None = None, right: KDNode | None = None):
        self.point = point
        self.left = left
        self.right = right


def build_kd_tree(points: list[Point2D], depth: int = 0) -> KDNode | None:
    if not points:
        return None
    axis = depth % 2
    points.sort(key=lambda p: p[axis])
    median = len(points) // 2
    return KDNode(
        point=points[median],
        left=build_kd_tree(points[:median], depth + 1),
        right=build_kd_tree(points[median + 1:], depth + 1),
    )


def nearest_neighbor(root: KDNode | None, target: Point2D) -> tuple[Point2D | None, float]:
    best_point: Point2D | None = None
    best_dist = float("inf")

    def search(node: KDNode | None, depth: int) -> None:
        nonlocal best_point, best_dist
        if not node:
            return
        d = math.hypot(node.point[0] - target[0], node.point[1] - target[1])
        if d < best_dist:
            best_dist = d
            best_point = node.point
        axis = depth % 2
        diff = target[axis] - node.point[axis]
        first = node.left if diff < 0 else node.right
        second = node.right if diff < 0 else node.left
        search(first, depth + 1)
        if abs(diff) < best_dist:
            search(second, depth + 1)

    search(root, 0)
    return best_point, best_dist


def self_check() -> None:
    pts: list[Point2D] = [(2.0, 3.0), (5.0, 4.0), (9.0, 6.0), (4.0, 7.0), (8.0, 1.0), (7.0, 2.0)]
    tree = build_kd_tree(pts)
    assert tree is not None
    nn, dist = nearest_neighbor(tree, (9.0, 2.0))
    assert nn == (8.0, 1.0)
    assert round(dist, 4) == round(math.hypot(1.0, 1.0), 4)
    nn2, _ = nearest_neighbor(tree, (2.0, 3.1))
    assert nn2 == (2.0, 3.0)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
