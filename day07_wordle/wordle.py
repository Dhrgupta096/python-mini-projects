#!/usr/bin/env python3
"""Exact 5-letter Wordle feedback scorer (G = green, Y = yellow, . = miss)."""
from __future__ import annotations


def score_guess(secret: str, guess: str) -> str:
    result = ["."] * len(secret)
    remaining: list[str | None] = list(secret)
    for i, (s, g) in enumerate(zip(secret, guess)):
        if s == g:
            result[i] = "G"
            remaining[i] = None
    for i, g in enumerate(guess):
        if result[i] == "." and g in remaining:
            result[i] = "Y"
            remaining[remaining.index(g)] = None
    return "".join(result)


def self_check() -> None:
    assert score_guess("crane", "crane") == "GGGGG"
    assert score_guess("apple", "puppy") == "Y.G.."
    assert score_guess("abbey", "babes") == "YYGG."
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
