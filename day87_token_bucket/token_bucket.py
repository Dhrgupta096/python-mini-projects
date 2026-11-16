#!/usr/bin/env python3
"""Token Bucket Rate Limiter algorithm for traffic shaping and burst handling."""
from __future__ import annotations
import time


class TokenBucket:
    def __init__(self, capacity: float, refill_rate: float, current_tokens: float | None = None, now: float | None = None):
        self.capacity = float(capacity)
        self.refill_rate = float(refill_rate)
        self.tokens = self.capacity if current_tokens is None else float(current_tokens)
        self.last_refill = time.monotonic() if now is None else float(now)

    def _refill(self, now: float | None = None) -> None:
        t = time.monotonic() if now is None else now
        elapsed = t - self.last_refill
        if elapsed > 0:
            self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = t

    def consume(self, tokens: float = 1.0, now: float | None = None) -> bool:
        self._refill(now)
        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


def self_check() -> None:
    tb = TokenBucket(capacity=5.0, refill_rate=2.0, now=10.0)
    assert tb.consume(3.0, now=10.0)
    assert tb.consume(2.0, now=10.0)
    assert not tb.consume(1.0, now=10.0)
    assert tb.consume(1.0, now=10.5)
    assert not tb.consume(1.0, now=10.5)
    assert tb.consume(2.0, now=11.5)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
