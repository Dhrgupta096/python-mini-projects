#!/usr/bin/env python3
"""Thread-safe Counting Semaphore with context manager support."""
from __future__ import annotations
import threading


class Semaphore:
    def __init__(self, value: int = 1):
        if value < 0:
            raise ValueError("Semaphore initial value must be >= 0")
        self._value = value
        self._cond = threading.Condition(threading.Lock())

    def acquire(self, blocking: bool = True, timeout: float | None = None) -> bool:
        with self._cond:
            while self._value == 0:
                if not blocking or not self._cond.wait(timeout):
                    return False
            self._value -= 1
            return True

    def release(self) -> None:
        with self._cond:
            self._value += 1
            self._cond.notify()

    def __enter__(self) -> bool:
        self.acquire()
        return True

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()


def self_check() -> None:
    sem = Semaphore(2)
    assert sem.acquire()
    assert sem.acquire()
    assert not sem.acquire(blocking=False)
    sem.release()
    assert sem.acquire(blocking=False)
    sem.release()
    with sem:
        pass
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
