#!/usr/bin/env python3
"""Basic 2048 row-merge mechanics and board movement."""
from __future__ import annotations

Grid = list[list[int]]


def slide_left(row: list[int]) -> list[int]:
    tiles = [x for x in row if x != 0]
    merged: list[int] = []
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            merged.append(tiles[i] * 2)
            i += 2
        else:
            merged.append(tiles[i])
            i += 1
    return merged + [0] * (len(row) - len(merged))


def move_left(grid: Grid) -> Grid:
    return [slide_left(row) for row in grid]


def rotate_cw(grid: Grid) -> Grid:
    return [list(row) for row in zip(*grid[::-1])]


def self_check() -> None:
    assert slide_left([2, 2, 4, 0]) == [4, 4, 0, 0]
    assert slide_left([2, 2, 2, 2]) == [4, 4, 0, 0]
    assert slide_left([4, 0, 4, 2]) == [8, 2, 0, 0]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
