#!/usr/bin/env python3
"""Pure Python 2D matrix multiplication, transpose, and determinant."""
from __future__ import annotations

Matrix = list[list[float]]


def mat_mul(a: Matrix, b: Matrix) -> Matrix:
    rows_a, cols_a = len(a), len(a[0])
    rows_b, cols_b = len(b), len(b[0])
    if cols_a != rows_b:
        raise ValueError("Incompatible dimensions for multiplication")
    res = [[0.0] * cols_b for _ in range(rows_a)]
    for i in range(rows_a):
        for j in range(cols_b):
            res[i][j] = sum(a[i][k] * b[k][j] for k in range(cols_a))
    return res


def mat_transpose(a: Matrix) -> Matrix:
    return [list(row) for row in zip(*a)]


def mat_det(m: Matrix) -> float:
    n = len(m)
    if n == 1:
        return m[0][0]
    if n == 2:
        return m[0][0] * m[1][1] - m[0][1] * m[1][0]
    det = 0.0
    for c in range(n):
        sub = [row[:c] + row[c + 1:] for row in m[1:]]
        det += ((-1) ** c) * m[0][c] * mat_det(sub)
    return det


def self_check() -> None:
    a = [[1.0, 2.0], [3.0, 4.0]]
    b = [[2.0, 0.0], [1.0, 2.0]]
    mul = mat_mul(a, b)
    assert mul == [[4.0, 4.0], [10.0, 8.0]]
    assert mat_det(a) == -2.0
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
