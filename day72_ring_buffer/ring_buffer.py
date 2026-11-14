#!/usr/bin/env python3
"""Fixed-size circular FIFO ring buffer with overwrite semantics."""
from __future__ import annotations
from typing import Any


class RingBuffer:
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self._buf: list[Any] = [None] * capacity
        self._head = 0
        self._tail = 0
        self._size = 0

    def push(self, item: Any) -> None:
        self._buf[self._tail] = item
        self._tail = (self._tail + 1) % self.capacity
        if self._size == self.capacity:
            self._head = (self._head + 1) % self.capacity
        else:
            self._size += 1

    def pop(self) -> Any:
        if self._size == 0:
            raise IndexError("pop from an empty ring buffer")
        item = self._buf[self._head]
        self._buf[self._head] = None
        self._head = (self._head + 1) % self.capacity
        self._size -= 1
        return item

    def to_list(self) -> list[Any]:
        res = []
        for i in range(self._size):
            res.append(self._buf[(self._head + i) % self.capacity])
        return res


def self_check() -> None:
    rb = RingBuffer(3)
    rb.push(1)
    rb.push(2)
    rb.push(3)
    assert rb.to_list() == [1, 2, 3]
    rb.push(4)
    assert rb.to_list() == [2, 3, 4]
    assert rb.pop() == 2
    assert rb.pop() == 3
    assert rb.to_list() == [4]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
