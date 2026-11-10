#!/usr/bin/env python3
"""Min-heap priority task queue and scheduler."""
from __future__ import annotations
import heapq
from typing import NamedTuple


class Task(NamedTuple):
    priority: int
    task_id: str
    action_name: str


class TaskScheduler:
    def __init__(self):
        self._heap: list[Task] = []
        self._completed: list[str] = []

    def add_task(self, task_id: str, priority: int, action_name: str) -> None:
        heapq.heappush(self._heap, Task(priority, task_id, action_name))

    def run_next(self) -> Task | None:
        if not self._heap:
            return None
        task = heapq.heappop(self._heap)
        self._completed.append(task.task_id)
        return task

    def is_empty(self) -> bool:
        return len(self._heap) == 0


def self_check() -> None:
    scheduler = TaskScheduler()
    scheduler.add_task("task_low", 10, "cleanup")
    scheduler.add_task("task_high", 1, "send_alert")
    scheduler.add_task("task_med", 5, "process_data")
    order = []
    while not scheduler.is_empty():
        t = scheduler.run_next()
        if t:
            order.append(t.task_id)
    assert order == ["task_high", "task_med", "task_low"]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
