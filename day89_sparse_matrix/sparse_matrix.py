#!/usr/bin/env python3
"""Compressed Sparse Row (CSR) matrix representation and vector multiplication."""
from __future__ import annotations


class CSRMatrix:
    def __init__(self, dense_matrix: list[list[float]]):
        self.rows = len(dense_matrix)
        self.cols = len(dense_matrix[0]) if self.rows > 0 else 0
        self.values: list[float] = []
        self.col_indices: list[int] = []
        self.row_ptr: list[int] = [0]

        for row in dense_matrix:
            for c, val in enumerate(row):
                if val != 0:
                    self.values.append(val)
                    self.col_indices.append(c)
            self.row_ptr.append(len(self.values))

    def matvec(self, x: list[float]) -> list[float]:
        if len(x) != self.cols:
            raise ValueError(f"Dimension mismatch: expected {self.cols}, got {len(x)}")
        result = [0.0] * self.rows
        for r in range(self.rows):
            start = self.row_ptr[r]
            end = self.row_ptr[r + 1]
            row_sum = 0.0
            for idx in range(start, end):
                row_sum += self.values[idx] * x[self.col_indices[idx]]
            result[r] = row_sum
        return result

    def sparsity(self) -> float:
        total = self.rows * self.cols
        if total == 0:
            return 0.0
        return 1.0 - (len(self.values) / total)


def self_check() -> None:
    dense = [
        [1.0, 0.0, 0.0, 2.0],
        [0.0, 0.0, 3.0, 0.0],
        [4.0, 0.0, 0.0, 5.0],
    ]
    csr = CSRMatrix(dense)
    assert csr.values == [1.0, 2.0, 3.0, 4.0, 5.0]
    assert csr.col_indices == [0, 3, 2, 0, 3]
    assert csr.row_ptr == [0, 2, 3, 5]
    vec = [1.0, 2.0, 3.0, 4.0]
    out = csr.matvec(vec)
    assert out == [9.0, 9.0, 24.0]
    assert round(csr.sparsity(), 4) == round(7 / 12, 4)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
