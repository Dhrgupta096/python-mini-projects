#!/usr/bin/env python3
"""Publish-Subscribe event emitter with once and typed callback support."""
from __future__ import annotations
from typing import Callable, Any


class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list[Callable[..., Any]]] = {}

    def on(self, event: str, callback: Callable[..., Any]) -> None:
        self._listeners.setdefault(event, []).append(callback)

    def once(self, event: str, callback: Callable[..., Any]) -> None:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            self.off(event, wrapper)
            return callback(*args, **kwargs)
        self.on(event, wrapper)

    def off(self, event: str, callback: Callable[..., Any]) -> None:
        if event in self._listeners and callback in self._listeners[event]:
            self._listeners[event].remove(callback)

    def emit(self, event: str, *args: Any, **kwargs: Any) -> list[Any]:
        callbacks = list(self._listeners.get(event, []))
        return [cb(*args, **kwargs) for cb in callbacks]


def self_check() -> None:
    bus = EventEmitter()
    log: list[str] = []
    bus.on("ping", lambda val: log.append(f"ping:{val}"))
    bus.once("ping", lambda val: log.append("once"))
    bus.emit("ping", 1)
    bus.emit("ping", 2)
    assert log == ["ping:1", "once", "ping:2"]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
