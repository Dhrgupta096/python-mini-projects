#!/usr/bin/env python3
"""2D spatial partition QuadTree for bounding box region queries."""
from __future__ import annotations
from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float
    data: str


class Rect(NamedTuple):
    x: float
    y: float
    w: float
    h: float

    def contains(self, p: Point) -> bool:
        return self.x <= p.x <= self.x + self.w and self.y <= p.y <= self.y + self.h

    def intersects(self, other: Rect) -> bool:
        return not (
            other.x > self.x + self.w
            or other.x + other.w < self.x
            or other.y > self.y + self.h
            or other.y + other.h < self.y
        )


class QuadTree:
    def __init__(self, boundary: Rect, capacity: int = 4):
        self.boundary = boundary
        self.capacity = capacity
        self.points: list[Point] = []
        self.divided = False
        self.children: list[QuadTree] = []

    def subdivide(self) -> None:
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w / 2, self.boundary.h / 2
        self.children = [
            QuadTree(Rect(x, y, w, h), self.capacity),
            QuadTree(Rect(x + w, y, w, h), self.capacity),
            QuadTree(Rect(x, y + h, w, h), self.capacity),
            QuadTree(Rect(x + w, y + h, w, h), self.capacity),
        ]
        self.divided = True

    def insert(self, p: Point) -> bool:
        if not self.boundary.contains(p):
            return False
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(p)
            return True
        if not self.divided:
            self.subdivide()
            old_pts = self.points
            self.points = []
            for pt in old_pts:
                for c in self.children:
                    if c.insert(pt):
                        break
        return any(c.insert(p) for c in self.children)

    def query(self, range_rect: Rect) -> list[Point]:
        found: list[Point] = []
        if not self.boundary.intersects(range_rect):
            return found
        for p in self.points:
            if range_rect.contains(p):
                found.append(p)
        if self.divided:
            for c in self.children:
                found.extend(c.query(range_rect))
        return found


def self_check() -> None:
    qt = QuadTree(Rect(0, 0, 100, 100), capacity=2)
    qt.insert(Point(10, 10, "A"))
    qt.insert(Point(20, 20, "B"))
    qt.insert(Point(80, 80, "C"))
    matches = qt.query(Rect(0, 0, 30, 30))
    names = {p.data for p in matches}
    assert names == {"A", "B"}
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
