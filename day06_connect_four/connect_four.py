#!/usr/bin/env python3
"""Basic Connect Four drop and 4-in-a-row win check."""
from __future__ import annotations

ROWS, COLS = 6, 7


def drop_piece(board: list[list[str]], col: int, piece: str) -> bool:
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ".":
            board[r][col] = piece
            return True
    return False


def has_four(board: list[list[str]], piece: str) -> bool:
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                if all(
                    0 <= r + i * dr < ROWS
                    and 0 <= c + i * dc < COLS
                    and board[r + i * dr][c + i * dc] == piece
                    for i in range(4)
                ):
                    return True
    return False


def self_check() -> None:
    board = [["."] * COLS for _ in range(ROWS)]
    for col in range(4):
        drop_piece(board, col, "X")
    assert has_four(board, "X")
    assert not has_four(board, "O")
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
