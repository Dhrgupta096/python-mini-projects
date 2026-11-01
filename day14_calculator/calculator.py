#!/usr/bin/env python3
"""Recursive descent evaluator for arithmetic expressions (+, -, *, /, parentheses)."""
from __future__ import annotations
import re


def tokenize(expr: str) -> list[str]:
    return re.findall(r"\d+(?:\.\d+)?|[+\-*/()]", expr)


def evaluate(expr: str) -> float:
    tokens = tokenize(expr)
    pos = 0

    def parse_factor() -> float:
        nonlocal pos
        token = tokens[pos]
        if token == "(":
            pos += 1
            val = parse_expr()
            assert tokens[pos] == ")"
            pos += 1
            return val
        pos += 1
        return float(token)

    def parse_term() -> float:
        nonlocal pos
        val = parse_factor()
        while pos < len(tokens) and tokens[pos] in ("*", "/"):
            op = tokens[pos]
            pos += 1
            rhs = parse_factor()
            val = (val * rhs) if op == "*" else (val / rhs)
        return val

    def parse_expr() -> float:
        nonlocal pos
        val = parse_term()
        while pos < len(tokens) and tokens[pos] in ("+", "-"):
            op = tokens[pos]
            pos += 1
            rhs = parse_term()
            val = (val + rhs) if op == "+" else (val - rhs)
        return val

    res = parse_expr()
    assert pos == len(tokens)
    return res


def self_check() -> None:
    assert evaluate("3 + 5 * 2") == 13.0
    assert evaluate("(3 + 5) * 2") == 16.0
    assert evaluate("10 / 2 - 3") == 2.0
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
