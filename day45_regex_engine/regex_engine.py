#!/usr/bin/env python3
"""Recursive pattern matcher supporting literals, wildcard '.', and Kleene star '*'."""
from __future__ import annotations


def is_match(text: str, pattern: str) -> bool:
    if not pattern:
        return not text
    first_match = bool(text) and (pattern[0] == text[0] or pattern[0] == ".")
    if len(pattern) >= 2 and pattern[1] == "*":
        return is_match(text, pattern[2:]) or (first_match and is_match(text[1:], pattern))
    return first_match and is_match(text[1:], pattern[1:])


def self_check() -> None:
    assert is_match("aa", "a*")
    assert is_match("ab", ".*")
    assert is_match("aab", "c*a*b")
    assert not is_match("mississippi", "mis*is*p*.")
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
