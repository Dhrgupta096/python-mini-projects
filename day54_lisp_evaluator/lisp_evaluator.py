#!/usr/bin/env python3
"""Tiny Scheme/Lisp S-expression parser and tree evaluator."""
from __future__ import annotations
from typing import Any


def tokenize(chars: str) -> list[str]:
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def parse_tokens(tokens: list[str]) -> Any:
    if not tokens:
        raise SyntaxError("Unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens and tokens[0] != ")":
            L.append(parse_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("Unexpected )")
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var: str):
        return self if var in self else (self.outer.find(var) if self.outer else None)


def standard_env() -> Env:
    env = Env()
    env.update({
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        "=": lambda a, b: a == b,
    })
    return env


def evaluate(x: Any, env: Env) -> Any:
    if isinstance(x, str):
        e = env.find(x)
        if e is None:
            raise NameError(f"Undefined symbol: {x}")
        return e[x]
    elif not isinstance(x, list):
        return x
    op = x[0]
    if op == "if":
        (_, test, conseq, alt) = x
        exp = conseq if evaluate(test, env) else alt
        return evaluate(exp, env)
    elif op == "define":
        (_, symbol, exp) = x
        env[symbol] = evaluate(exp, env)
        return env[symbol]
    elif op == "lambda":
        (_, parms, body) = x
        return lambda *args: evaluate(body, Env(parms, args, env))
    else:
        proc = evaluate(op, env)
        vals = [evaluate(arg, env) for arg in x[1:]]
        return proc(*vals)


def self_check() -> None:
    global_env = standard_env()
    t1 = parse_tokens(tokenize("(+ 10 (* 2 3))"))
    assert evaluate(t1, global_env) == 16
    t2 = parse_tokens(tokenize("(define square (lambda (r) (* r r)))"))
    evaluate(t2, global_env)
    t3 = parse_tokens(tokenize("(square 5)"))
    assert evaluate(t3, global_env) == 25
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
