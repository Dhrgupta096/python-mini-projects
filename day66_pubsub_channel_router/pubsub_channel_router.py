#!/usr/bin/env python3
"""MQTT-style hierarchical topic message router with '+' and '#' wildcards."""
from __future__ import annotations
from typing import Callable, Any


class TopicRouter:
    def __init__(self):
        self.subscriptions: list[tuple[list[str], Callable[[str, Any], None]]] = []

    def subscribe(self, pattern: str, handler: Callable[[str, Any], None]) -> None:
        parts = pattern.strip("/").split("/")
        self.subscriptions.append((parts, handler))

    def _match(self, pattern_parts: list[str], topic_parts: list[str]) -> bool:
        p_idx, t_idx = 0, 0
        while p_idx < len(pattern_parts) and t_idx < len(topic_parts):
            p = pattern_parts[p_idx]
            if p == "#":
                return True
            if p != "+" and p != topic_parts[t_idx]:
                return False
            p_idx += 1
            t_idx += 1
        if p_idx < len(pattern_parts) and pattern_parts[p_idx] == "#":
            return True
        return p_idx == len(pattern_parts) and t_idx == len(topic_parts)

    def publish(self, topic: str, message: Any) -> int:
        topic_parts = topic.strip("/").split("/")
        delivered = 0
        for pat_parts, handler in self.subscriptions:
            if self._match(pat_parts, topic_parts):
                handler(topic, message)
                delivered += 1
        return delivered


def self_check() -> None:
    router = TopicRouter()
    log: list[str] = []
    router.subscribe("home/+/temp", lambda t, m: log.append(f"single:{m}"))
    router.subscribe("home/#", lambda t, m: log.append(f"multi:{m}"))
    router.publish("home/kitchen/temp", 22)
    router.publish("home/living/lights/switch", "on")
    assert log == ["single:22", "multi:22", "multi:on"]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
