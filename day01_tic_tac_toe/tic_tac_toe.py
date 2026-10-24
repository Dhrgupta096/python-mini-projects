#!/usr/bin/env python3
"""Day 01: Minimal CLI Tic-Tac-Toe with built-in self-check."""

from __future__ import annotations
import sys

WIN_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),
    (0, 3, 6), (1, 4, 7), (2, 5, 8),
    (0, 4, 8), (2, 4, 6),
)


def winner(board: list[str]) -> str | None:
    for a, b, c in WIN_LINES:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]
    return "Draw" if " " not in board else None


def render(board: list[str]) -> str:
    rows = [" | ".join(board[i:i + 3]) for i in range(0, 9, 3)]
    return "\n---------\n".join(rows)


def self_check() -> None:
    assert winner(["X", "X", "X", " ", "O", " ", " ", " ", "O"]) == "X"
    assert winner(["O", "X", "X", " ", "O", " ", " ", " ", "O"]) == "O"
    assert winner(["X", "O", "X", "X", "O", "O", "O", "X", "X"]) == "Draw"
    assert winner([" "] * 9) is None
    print("Self-check passed.")


def play() -> None:
    board = [" "] * 9
    turn = "X"
    while not (result := winner(board)):
        print(f"\n{render(board)}\n")
        try:
            move = int(input(f"Player {turn} (1-9): ")) - 1
        except (ValueError, EOFError):
            print("Enter a number from 1 to 9.")
            continue
        if not (0 <= move < 9) or board[move] != " ":
            print("Invalid move, try again.")
            continue
        board[move] = turn
        turn = "O" if turn == "X" else "X"
    print(f"\n{render(board)}\n\nResult: {result}!")


if __name__ == "__main__":
    if "--check" in sys.argv:
        self_check()
    else:
        play()
