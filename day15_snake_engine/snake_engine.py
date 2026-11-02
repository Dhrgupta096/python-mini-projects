#!/usr/bin/env python3
"""Deterministic 2D Snake game mechanics and collision engine."""
from __future__ import annotations
from typing import NamedTuple


class Point(NamedTuple):
    x: int
    y: int


class SnakeGame:
    def __init__(self, width: int = 10, height: int = 10):
        self.width = width
        self.height = height
        self.snake = [Point(5, 5), Point(4, 5), Point(3, 5)]
        self.direction = Point(1, 0)
        self.food = Point(7, 5)
        self.game_over = False

    def change_direction(self, dx: int, dy: int) -> None:
        if (self.direction.x + dx, self.direction.y + dy) != (0, 0):
            self.direction = Point(dx, dy)

    def step(self) -> bool:
        if self.game_over:
            return False
        head = self.snake[0]
        new_head = Point(head.x + self.direction.x, head.y + self.direction.y)

        if not (0 <= new_head.x < self.width and 0 <= new_head.y < self.height):
            self.game_over = True
            return False
        if new_head in self.snake[:-1]:
            self.game_over = True
            return False

        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.food = Point((self.food.x + 3) % self.width, (self.food.y + 2) % self.height)
        else:
            self.snake.pop()
        return True


def self_check() -> None:
    game = SnakeGame(10, 10)
    assert len(game.snake) == 3
    game.step()
    assert game.snake[0] == Point(6, 5)
    game.step()
    assert game.snake[0] == Point(7, 5)
    assert len(game.snake) == 4
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
