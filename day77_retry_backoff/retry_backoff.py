#!/usr/bin/env python3
"""Exponential backoff with full randomized jitter."""
from __future__ import annotations
import random
from typing import Callable, Any


def retry_with_backoff(
    func: Callable[[], Any],
    max_retries: int = 4,
    base_delay: float = 0.1,
    max_delay: float = 1.0,
    seed: int | None = 42,
) -> Any:
    rng = random.Random(seed)
    attempts = 0
    while True:
        try:
            return func()
        except Exception:
            attempts += 1
            if attempts > max_retries:
                raise
            temp = min(max_delay, base_delay * (2 ** (attempts - 1)))
            sleep_duration = rng.uniform(0, temp)


def self_check() -> None:
    calls = 0

    def flaky() -> str:
        nonlocal calls
        calls += 1
        if calls < 3:
            raise ConnectionError("Temporary outage")
        return "success"

    res = retry_with_backoff(flaky, max_retries=4, seed=123)
    assert res == "success"
    assert calls == 3
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
