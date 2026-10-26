#!/usr/bin/env python3
"""Day 04: Basic Hangman state helper and CLI game."""

from __future__ import annotations
import random
import sys

WORDS = ("python", "variable", "function", "iterator", "terminal", "package")
MAX_TRIES = 6


def mask_word(secret: str, guessed: set[str]) -> str:
    return " ".join(ch if ch in guessed else "_" for ch in secret)


def is_won(secret: str, guessed: set[str]) -> bool:
    return all(ch in guessed for ch in secret)


def self_check() -> None:
    assert mask_word("python", {"p", "n"}) == "p _ _ _ _ n"
    assert not is_won("python", {"p", "n"})
    assert is_won("py", {"p", "y"})
    print("Self-check passed.")


def play() -> None:
    secret = random.choice(WORDS)
    guessed: set[str] = set()
    tries = MAX_TRIES
    while tries > 0 and not is_won(secret, guessed):
        print(f"\nWord: {mask_word(secret, guessed)}  |  Tries left: {tries}")
        try:
            ch = input("Guess a letter (or 'q' to quit): ").strip().lower()
        except EOFError:
            return
        if ch == "q":
            return
        if len(ch) != 1 or not ch.isalpha():
            print("Enter a single letter (a-z).")
            continue
        if ch in guessed:
            print(f"Already guessed '{ch}'.")
            continue
        guessed.add(ch)
        if ch not in secret:
            tries -= 1
            print(f"No '{ch}'!")
    print(f"\nWord: {secret} — {'You won!' if is_won(secret, guessed) else 'Game over!'}")


if __name__ == "__main__":
    if "--check" in sys.argv:
        self_check()
    else:
        play()
