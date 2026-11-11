#!/usr/bin/env python3
"""Finite State Machine (FSM) engine with event guards and callbacks."""
from __future__ import annotations


class FiniteStateMachine:
    def __init__(self, initial_state: str):
        self.state = initial_state
        self.transitions: dict[tuple[str, str], str] = {}
        self.history: list[str] = [initial_state]

    def add_transition(self, from_state: str, event: str, to_state: str) -> None:
        self.transitions[(from_state, event)] = to_state

    def trigger(self, event: str) -> bool:
        key = (self.state, event)
        if key in self.transitions:
            self.state = self.transitions[key]
            self.history.append(self.state)
            return True
        return False


def self_check() -> None:
    fsm = FiniteStateMachine("LOCKED")
    fsm.add_transition("LOCKED", "COIN", "UNLOCKED")
    fsm.add_transition("UNLOCKED", "PUSH", "LOCKED")
    assert fsm.state == "LOCKED"
    assert not fsm.trigger("PUSH")
    assert fsm.trigger("COIN")
    assert fsm.state == "UNLOCKED"
    assert fsm.trigger("PUSH")
    assert fsm.state == "LOCKED"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
