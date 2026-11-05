#!/usr/bin/env python3
"""Breadth-First Search (BFS) grid shortest path finder."""
from __future__ import annotations
from collections import deque


def find_shortest_path(grid: list[str], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]] | None:
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return None


def self_check() -> None:
    maze = [
        "S..#.",
        "#..#.",
        "...#.",
        ".##..",
        "....E",
    ]
    path = find_shortest_path(maze, (0, 0), (4, 4))
    assert path is not None
    assert path[0] == (0, 0) and path[-1] == (4, 4)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
