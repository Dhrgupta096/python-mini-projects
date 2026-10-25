#!/usr/bin/env python3
"""Day 02: Basic 9x9 CLI Sudoku game & backtracking solver."""

from __future__ import annotations
import copy
import sys

Board = list[list[int]]

STARTER: Board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9],
]


def is_valid(board: Board, r: int, c: int, val: int) -> bool:
    for i in range(9):
        if board[r][i] == val or board[i][c] == val:
            return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    return all(board[br + dr][bc + dc] != val for dr in range(3) for dc in range(3))


def solve(board: Board) -> bool:
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for val in range(1, 10):
                    if is_valid(board, r, c, val):
                        board[r][c] = val
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def render(board: Board) -> str:
    lines: list[str] = []
    for r, row in enumerate(board):
        if r in (3, 6):
            lines.append("------+-------+------")
        chunks = [
            " ".join(str(x) if x else "." for x in row[c:c + 3])
            for c in (0, 3, 6)
        ]
        lines.append(" | ".join(chunks))
    return "\n".join(lines)


def self_check() -> None:
    puzzle = copy.deepcopy(STARTER)
    assert solve(puzzle)
    assert all(0 not in row for row in puzzle)
    assert puzzle[0][:3] == [5, 3, 4]
    print("Self-check passed.")


def play() -> None:
    board = copy.deepcopy(STARTER)
    while any(0 in row for row in board):
        print(f"\n{render(board)}\n")
        cmd = input("Enter 'row col num' (1-9), 'solve', or 'q': ").strip().lower()
        if cmd == "q":
            return
        if cmd == "solve":
            solve(board)
            break
        parts = cmd.split()
        if len(parts) != 3 or not all(p.isdigit() for p in parts):
            print("Format: row col num (e.g., 1 3 4)")
            continue
        r, c, val = (int(p) for p in parts)
        if not (1 <= r <= 9 and 1 <= c <= 9 and 1 <= val <= 9):
            print("Values must be 1 to 9.")
        elif STARTER[r - 1][c - 1] != 0:
            print("Cannot overwrite a fixed clue.")
        elif not is_valid(board, r - 1, c - 1, val):
            print("Conflict in row, column, or 3x3 box!")
        else:
            board[r - 1][c - 1] = val
    print(f"\n{render(board)}\n\nSolved!")


if __name__ == "__main__":
    if "--check" in sys.argv:
        self_check()
    else:
        play()
