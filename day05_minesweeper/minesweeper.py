#!/usr/bin/env python3
"""Basic Minesweeper neighbor-count board builder."""
from __future__ import annotations


def build_counts(rows: int, cols: int, mines: set[tuple[int, int]]) -> list[list[str]]:
    board: list[list[str]] = []
    for r in range(rows):
        row: list[str] = []
        for c in range(cols):
            if (r, c) in mines:
                row.append("*")
                continue
            count = sum(
                (r + dr, c + dc) in mines
                for dr in (-1, 0, 1)
                for dc in (-1, 0, 1)
                if (dr, dc) != (0, 0)
            )
            row.append(str(count))
        board.append(row)
    return board


def self_check() -> None:
    b = build_counts(3, 3, {(1, 1)})
    assert b[1][1] == "*"
    assert b[0][0] == "1" and b[2][2] == "1"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
