#!/usr/bin/env python3
"""Dijkstra's Shunting-Yard Algorithm to parse and evaluate infix math expressions."""
from __future__ import annotations
import re


def tokenize(expr: str) -> list[str]:
    return re.findall(r"\d+\.?\d*|[+\-*/()^]", expr)


def infix_to_rpn(tokens: list[str]) -> list[str]:
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
    associativity = {"+": "L", "-": "L", "*": "L", "/": "L", "^": "R"}
    output: list[str] = []
    ops: list[str] = []

    for tok in tokens:
        if re.match(r"^\d", tok):
            output.append(tok)
        elif tok in precedence:
            while (
                ops and ops[-1] in precedence
                and (
                    (associativity[tok] == "L" and precedence[tok] <= precedence[ops[-1]])
                    or (associativity[tok] == "R" and precedence[tok] < precedence[ops[-1]])
                )
            ):
                output.append(ops.pop())
            ops.append(tok)
        elif tok == "(":
            ops.append(tok)
        elif tok == ")":
            while ops and ops[-1] != "(":
                output.append(ops.pop())
            if not ops:
                raise ValueError("Mismatched parentheses")
            ops.pop()
    while ops:
        if ops[-1] in "()":
            raise ValueError("Mismatched parentheses")
        output.append(ops.pop())
    return output


def eval_rpn(tokens: list[str]) -> float:
    stack: list[float] = []
    for tok in tokens:
        if re.match(r"^\d", tok):
            stack.append(float(tok))
        else:
            b = stack.pop()
            a = stack.pop()
            if tok == "+":
                stack.append(a + b)
            elif tok == "-":
                stack.append(a - b)
            elif tok == "*":
                stack.append(a * b)
            elif tok == "/":
                stack.append(a / b)
            elif tok == "^":
                stack.append(a ** b)
    return stack[0]


def evaluate(expr: str) -> float:
    return eval_rpn(infix_to_rpn(tokenize(expr)))


def self_check() -> None:
    assert evaluate("3 + 4 * 2 / ( 1 - 5 ) ^ 2") == 3.5
    assert evaluate("(2 + 3) * 4") == 20.0
    assert evaluate("2 ^ 3 ^ 2") == 512.0
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
