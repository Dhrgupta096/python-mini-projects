#!/usr/bin/env python3
"""Conway's Game of Life grid simulation and oscillator self-check."""
from __future__ import annotations

Grid = list[list[int]]


def count_neighbors(grid: Grid, r: int, c: int) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                count += grid[nr][nc]
    return count


def step(grid: Grid) -> Grid:
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            alive = grid[r][c]
            n = count_neighbors(grid, r, c)
            if alive and n in (2, 3):
                new_grid[r][c] = 1
            elif not alive and n == 3:
                new_grid[r][c] = 1
    return new_grid


def self_check() -> None:
    blinker = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]
    next_gen = step(blinker)
    assert next_gen == [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]
    assert step(next_gen) == blinker
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
