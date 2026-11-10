#!/usr/bin/env python3
"""Fault-tolerant circuit breaker state machine (Closed, Open, Half-Open)."""
from __future__ import annotations
import time
from typing import Callable, Any


class CircuitBreakerOpenException(Exception):
    pass


class CircuitBreaker:
    def __init__(self, failure_threshold: int = 3, recovery_time: float = 2.0):
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.state = "CLOSED"
        self.failures = 0
        self.last_failure_time = 0.0

    def call(self, func: Callable[[], Any], now: float | None = None) -> Any:
        current_time = time.monotonic() if now is None else now
        if self.state == "OPEN":
            if current_time - self.last_failure_time >= self.recovery_time:
                self.state = "HALF_OPEN"
            else:
                raise CircuitBreakerOpenException("Circuit is open")

        try:
            result = func()
            if self.state == "HALF_OPEN":
                self.state = "CLOSED"
                self.failures = 0
            return result
        except Exception:
            self.failures += 1
            self.last_failure_time = current_time
            if self.failures >= self.failure_threshold or self.state == "HALF_OPEN":
                self.state = "OPEN"
            raise


def self_check() -> None:
    cb = CircuitBreaker(failure_threshold=2, recovery_time=5.0)
    fail_call = lambda: (_ for _ in ()).throw(RuntimeError("Remote down"))
    success_call = lambda: "ok"

    try:
        cb.call(fail_call, now=10.0)
    except RuntimeError:
        pass
    assert cb.state == "CLOSED"

    try:
        cb.call(fail_call, now=10.5)
    except RuntimeError:
        pass
    assert cb.state == "OPEN"

    try:
        cb.call(success_call, now=12.0)
        assert False, "Should raise CircuitBreakerOpenException"
    except CircuitBreakerOpenException:
        pass

    assert cb.call(success_call, now=16.0) == "ok"
    assert cb.state == "CLOSED"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
