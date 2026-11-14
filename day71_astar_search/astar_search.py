#!/usr/bin/env python3
"""A* pathfinding algorithm on 2D grids with Manhattan distance heuristic."""
from __future__ import annotations
import heapq


def astar(grid: list[str], start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]] | None:
    rows, cols = len(grid), len(grid[0])
    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
    cost_so_far: dict[tuple[int, int], int] = {start: 0}

    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            break
        r, c = current
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#":
                next_node = (nr, nc)
                new_cost = cost_so_far[current] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + heuristic(goal, next_node)
                    heapq.heappush(frontier, (priority, next_node))
                    came_from[next_node] = current

    if goal not in came_from:
        return None
    curr = goal
    path = []
    while curr is not None:
        path.append(curr)
        curr = came_from[curr]
    path.reverse()
    return path


def self_check() -> None:
    maze = [
        "S..#.",
        ".#.#.",
        ".#...",
        "...#G",
    ]
    path = astar(maze, (0, 0), (3, 4))
    assert path is not None
    assert path[0] == (0, 0)
    assert path[-1] == (3, 4)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
