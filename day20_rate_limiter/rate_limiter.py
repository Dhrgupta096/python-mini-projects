#!/usr/bin/env python3
"""Token Bucket rate limiter for API requests."""
from __future__ import annotations
import time


class TokenBucket:
    def __init__(self, capacity: int, refill_rate_per_sec: float, start_time: float | None = None):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = time.monotonic() if start_time is None else start_time

    def allow_request(self, tokens: int = 1, current_time: float | None = None) -> bool:
        now = time.monotonic() if current_time is None else current_time
        elapsed = max(0.0, now - self.last_refill)
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


def self_check() -> None:
    limiter = TokenBucket(capacity=3, refill_rate_per_sec=1.0, start_time=0.0)
    assert limiter.allow_request(1, current_time=0.0)
    assert limiter.allow_request(1, current_time=0.0)
    assert limiter.allow_request(1, current_time=0.0)
    assert not limiter.allow_request(1, current_time=0.0)
    assert limiter.allow_request(1, current_time=1.0)
    assert not limiter.allow_request(1, current_time=1.0)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
