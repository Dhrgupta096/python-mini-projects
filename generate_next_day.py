#!/usr/bin/env python3
"""Cloud daily runner: generates the next basic Python mini-project, tests it, and updates README.md."""

from __future__ import annotations
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent

# Curated catalog of beginner-friendly stdlib Python mini-projects.
# Each entry is (slug, title, code).
PROJECTS: list[tuple[str, str, str]] = [
    (
        "sudoku",
        "Sudoku Solver",
        '''#!/usr/bin/env python3
"""Basic backtracking 9x9 Sudoku solver."""
from __future__ import annotations
import sys

Board = list[list[int]]


def is_valid(board: Board, r: int, c: int, val: int) -> bool:
    for i in range(9):
        if board[r][i] == val or board[i][c] == val:
            return False
    br, bc = (r // 3) * 3, (c // 3) * 3
    return all(board[br + dr][bc + dc] != val for dr in range(3) for dc in range(3))


def solve(board: Board) -> bool:
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                for val in range(1, 10):
                    if is_valid(board, r, c, val):
                        board[r][c] = val
                        if solve(board):
                            return True
                        board[r][c] = 0
                return False
    return True


def self_check() -> None:
    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]
    assert solve(puzzle)
    assert all(0 not in row for row in puzzle)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "game_2048",
        "2048 Terminal Game",
        '''#!/usr/bin/env python3
"""Basic 2048 row-merge mechanics and board movement."""
from __future__ import annotations

Grid = list[list[int]]


def slide_left(row: list[int]) -> list[int]:
    tiles = [x for x in row if x != 0]
    merged: list[int] = []
    i = 0
    while i < len(tiles):
        if i + 1 < len(tiles) and tiles[i] == tiles[i + 1]:
            merged.append(tiles[i] * 2)
            i += 2
        else:
            merged.append(tiles[i])
            i += 1
    return merged + [0] * (len(row) - len(merged))


def move_left(grid: Grid) -> Grid:
    return [slide_left(row) for row in grid]


def rotate_cw(grid: Grid) -> Grid:
    return [list(row) for row in zip(*grid[::-1])]


def self_check() -> None:
    assert slide_left([2, 2, 4, 0]) == [4, 4, 0, 0]
    assert slide_left([2, 2, 2, 2]) == [4, 4, 0, 0]
    assert slide_left([4, 0, 4, 2]) == [8, 2, 0, 0]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "hangman",
        "Hangman Word Game",
        '''#!/usr/bin/env python3
"""Basic Hangman state helper and CLI game."""
from __future__ import annotations


def mask_word(secret: str, guessed: set[str]) -> str:
    return " ".join(ch if ch in guessed else "_" for ch in secret)


def is_won(secret: str, guessed: set[str]) -> bool:
    return all(ch in guessed for ch in secret)


def self_check() -> None:
    assert mask_word("python", {"p", "n"}) == "p _ _ _ _ n"
    assert not is_won("python", {"p", "n"})
    assert is_won("py", {"p", "y"})
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "minesweeper",
        "Minesweeper Grid",
        '''#!/usr/bin/env python3
"""Basic Minesweeper neighbor-count board builder."""
from __future__ import annotations


def build_counts(rows: int, cols: int, mines: set[tuple[int, int]]) -> list[list[str]]:
    board: list[list[str]] = []
    for r in range(rows):
        row: list[str] = []
        for c in range(cols):
            if (r, c) in mines:
                row.append("*")
                continue
            count = sum(
                (r + dr, c + dc) in mines
                for dr in (-1, 0, 1)
                for dc in (-1, 0, 1)
                if (dr, dc) != (0, 0)
            )
            row.append(str(count))
        board.append(row)
    return board


def self_check() -> None:
    b = build_counts(3, 3, {(1, 1)})
    assert b[1][1] == "*"
    assert b[0][0] == "1" and b[2][2] == "1"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "connect_four",
        "Connect Four",
        '''#!/usr/bin/env python3
"""Basic Connect Four drop and 4-in-a-row win check."""
from __future__ import annotations

ROWS, COLS = 6, 7


def drop_piece(board: list[list[str]], col: int, piece: str) -> bool:
    for r in range(ROWS - 1, -1, -1):
        if board[r][col] == ".":
            board[r][col] = piece
            return True
    return False


def has_four(board: list[list[str]], piece: str) -> bool:
    for r in range(ROWS):
        for c in range(COLS):
            for dr, dc in ((0, 1), (1, 0), (1, 1), (1, -1)):
                if all(
                    0 <= r + i * dr < ROWS
                    and 0 <= c + i * dc < COLS
                    and board[r + i * dr][c + i * dc] == piece
                    for i in range(4)
                ):
                    return True
    return False


def self_check() -> None:
    board = [["."] * COLS for _ in range(ROWS)]
    for col in range(4):
        drop_piece(board, col, "X")
    assert has_four(board, "X")
    assert not has_four(board, "O")
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "wordle",
        "Wordle Feedback Scorer",
        '''#!/usr/bin/env python3
"""Exact 5-letter Wordle feedback scorer (G = green, Y = yellow, . = miss)."""
from __future__ import annotations


def score_guess(secret: str, guess: str) -> str:
    result = ["."] * len(secret)
    remaining: list[str | None] = list(secret)
    for i, (s, g) in enumerate(zip(secret, guess)):
        if s == g:
            result[i] = "G"
            remaining[i] = None
    for i, g in enumerate(guess):
        if result[i] == "." and g in remaining:
            result[i] = "Y"
            remaining[remaining.index(g)] = None
    return "".join(result)


def self_check() -> None:
    assert score_guess("crane", "crane") == "GGGGG"
    assert score_guess("apple", "puppy") == "Y.G.."
    assert score_guess("abbey", "babes") == "YYGG."
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "challenge_08",
        "Python Algorithm Challenge #08",
        '''#!/usr/bin/env python3
"""Day 08: Python Algorithm Challenge #08 — number theory & sequence utility."""
from __future__ import annotations


def solve_challenge(n: int) -> list[int]:
    """Return the first n primes greater than or equal to 8."""
    primes: list[int] = []
    candidate = max(2, 8)
    while len(primes) < n:
        if all(candidate % d != 0 for d in range(2, int(candidate ** 0.5) + 1)):
            primes.append(candidate)
        candidate += 1
    return primes


def self_check() -> None:
    result = solve_challenge(5)
    assert len(result) == 5
    assert all( result[i] < result[i + 1] for i in range(4) )
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "challenge_09",
        "Python Algorithm Challenge #09",
        '''#!/usr/bin/env python3
"""Day 09: Python Algorithm Challenge #09 — number theory & sequence utility."""
from __future__ import annotations


def solve_challenge(n: int) -> list[int]:
    """Return the first n primes greater than or equal to 9."""
    primes: list[int] = []
    candidate = max(2, 9)
    while len(primes) < n:
        if all(candidate % d != 0 for d in range(2, int(candidate ** 0.5) + 1)):
            primes.append(candidate)
        candidate += 1
    return primes


def self_check() -> None:
    result = solve_challenge(5)
    assert len(result) == 5
    assert all( result[i] < result[i + 1] for i in range(4) )
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "challenge_10",
        "Python Algorithm Challenge #10",
        '''#!/usr/bin/env python3
"""Day 10: Python Algorithm Challenge #10 — number theory & sequence utility."""
from __future__ import annotations


def solve_challenge(n: int) -> list[int]:
    """Return the first n primes greater than or equal to 10."""
    primes: list[int] = []
    candidate = max(2, 10)
    while len(primes) < n:
        if all(candidate % d != 0 for d in range(2, int(candidate ** 0.5) + 1)):
            primes.append(candidate)
        candidate += 1
    return primes


def self_check() -> None:
    result = solve_challenge(5)
    assert len(result) == 5
    assert all( result[i] < result[i + 1] for i in range(4) )
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "challenge_11",
        "Python Algorithm Challenge #11",
        '''#!/usr/bin/env python3
"""Day 11: Python Algorithm Challenge #11 — number theory & sequence utility."""
from __future__ import annotations


def solve_challenge(n: int) -> list[int]:
    """Return the first n primes greater than or equal to 11."""
    primes: list[int] = []
    candidate = max(2, 11)
    while len(primes) < n:
        if all(candidate % d != 0 for d in range(2, int(candidate ** 0.5) + 1)):
            primes.append(candidate)
        candidate += 1
    return primes


def self_check() -> None:
    result = solve_challenge(5)
    assert len(result) == 5
    assert all( result[i] < result[i + 1] for i in range(4) )
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "challenge_12",
        "Python Algorithm Challenge #12",
        '''#!/usr/bin/env python3
"""Day 12: Python Algorithm Challenge #12 — number theory & sequence utility."""
from __future__ import annotations


def solve_challenge(n: int) -> list[int]:
    """Return the first n primes greater than or equal to 12."""
    primes: list[int] = []
    candidate = max(2, 12)
    while len(primes) < n:
        if all(candidate % d != 0 for d in range(2, int(candidate ** 0.5) + 1)):
            primes.append(candidate)
        candidate += 1
    return primes


def self_check() -> None:
    result = solve_challenge(5)
    assert len(result) == 5
    assert all( result[i] < result[i + 1] for i in range(4) )
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "game_of_life",
        "Conway's Game of Life",
        '''#!/usr/bin/env python3
"""Conway's Game of Life grid simulation and oscillator self-check."""
from __future__ import annotations

Grid = list[list[int]]


def count_neighbors(grid: Grid, r: int, c: int) -> int:
    rows, cols = len(grid), len(grid[0])
    count = 0
    for dr in (-1, 0, 1):
        for dc in (-1, 0, 1):
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                count += grid[nr][nc]
    return count


def step(grid: Grid) -> Grid:
    rows, cols = len(grid), len(grid[0])
    new_grid = [[0] * cols for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            alive = grid[r][c]
            n = count_neighbors(grid, r, c)
            if alive and n in (2, 3):
                new_grid[r][c] = 1
            elif not alive and n == 3:
                new_grid[r][c] = 1
    return new_grid


def self_check() -> None:
    blinker = [
        [0, 1, 0],
        [0, 1, 0],
        [0, 1, 0],
    ]
    next_gen = step(blinker)
    assert next_gen == [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0],
    ]
    assert step(next_gen) == blinker
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "calculator",
        "Math Expression Evaluator",
        '''#!/usr/bin/env python3
"""Recursive descent evaluator for arithmetic expressions (+, -, *, /, parentheses)."""
from __future__ import annotations
import re


def tokenize(expr: str) -> list[str]:
    return re.findall(r"\\d+(?:\\.\\d+)?|[+\\-*/()]", expr)


def evaluate(expr: str) -> float:
    tokens = tokenize(expr)
    pos = 0

    def parse_factor() -> float:
        nonlocal pos
        token = tokens[pos]
        if token == "(":
            pos += 1
            val = parse_expr()
            assert tokens[pos] == ")"
            pos += 1
            return val
        pos += 1
        return float(token)

    def parse_term() -> float:
        nonlocal pos
        val = parse_factor()
        while pos < len(tokens) and tokens[pos] in ("*", "/"):
            op = tokens[pos]
            pos += 1
            rhs = parse_factor()
            val = (val * rhs) if op == "*" else (val / rhs)
        return val

    def parse_expr() -> float:
        nonlocal pos
        val = parse_term()
        while pos < len(tokens) and tokens[pos] in ("+", "-"):
            op = tokens[pos]
            pos += 1
            rhs = parse_term()
            val = (val + rhs) if op == "+" else (val - rhs)
        return val

    res = parse_expr()
    assert pos == len(tokens)
    return res


def self_check() -> None:
    assert evaluate("3 + 5 * 2") == 13.0
    assert evaluate("(3 + 5) * 2") == 16.0
    assert evaluate("10 / 2 - 3") == 2.0
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "snake_engine",
        "Snake Game Engine",
        '''#!/usr/bin/env python3
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
''',
    ),
    (
        "lru_cache",
        "LRU Cache",
        '''#!/usr/bin/env python3
"""Doubly-linked hash map Least Recently Used (LRU) Cache implementation."""
from __future__ import annotations
from typing import Any


class Node:
    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache: dict[Any, Node] = {}
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        p, n = node.prev, node.next
        if p and n:
            p.next = n
            n.prev = p

    def _add_to_front(self, node: Node) -> None:
        node.next = self.head.next
        node.prev = self.head
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any) -> Any:
        if key not in self.cache:
            return None
        node = self.cache[key]
        self._remove(node)
        self._add_to_front(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            lru = self.tail.prev
            if lru and lru.key is not None:
                self._remove(lru)
                del self.cache[lru.key]

        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_to_front(new_node)


def self_check() -> None:
    cache = LRUCache(2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1
    cache.put("c", 3)
    assert cache.get("b") is None
    assert cache.get("c") == 3
    assert cache.get("a") == 1
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "markdown_parser",
        "Markdown to HTML Parser",
        '''#!/usr/bin/env python3
"""Mini Markdown to HTML parser supporting headings, bold, italic, and lists."""
from __future__ import annotations
import re


def parse_inline(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"<code>\\1</code>", text)
    text = re.sub(r"\\*\\*([^*]+)\\*\\*", r"<strong>\\1</strong>", text)
    text = re.sub(r"\\*([^*]+)\\*", r"<em>\\1</em>", text)
    text = re.sub(r"\\[([^\\]]+)\\]\\(([^)]+)\\)", r\'<a href="\\2">\\1</a>\', text)
    return text


def markdown_to_html(md: str) -> str:
    html_lines: list[str] = []
    in_list = False

    for raw_line in md.strip().splitlines():
        line = raw_line.strip()
        if not line:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            continue

        if line.startswith("#"):
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            level = len(line) - len(line.lstrip("#"))
            heading_text = parse_inline(line.lstrip("#").strip())
            html_lines.append(f"<h{level}>{heading_text}</h{level}>")
        elif line.startswith("- "):
            if not in_list:
                html_lines.append("<ul>")
                in_list = True
            item_text = parse_inline(line[2:].strip())
            html_lines.append(f"  <li>{item_text}</li>")
        else:
            if in_list:
                html_lines.append("</ul>")
                in_list = False
            html_lines.append(f"<p>{parse_inline(line)}</p>")

    if in_list:
        html_lines.append("</ul>")
    return "\\n".join(html_lines)


def self_check() -> None:
    md = "# Hello\\n**bold** and *italic*\\n- item 1\\n- item 2"
    html = markdown_to_html(md)
    assert "<h1>Hello</h1>" in html
    assert "<strong>bold</strong> and <em>italic</em>" in html
    assert "<ul>\\n  <li>item 1</li>\\n  <li>item 2</li>\\n</ul>" in html
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "url_shortener",
        "Base62 URL Shortener",
        '''#!/usr/bin/env python3
"""URL Shortener service with Base62 encoding and decoding."""
from __future__ import annotations

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)


def encode_base62(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    chars = []
    while num > 0:
        chars.append(ALPHABET[num % BASE])
        num //= BASE
    return "".join(reversed(chars))


def decode_base62(s: str) -> int:
    num = 0
    for char in s:
        num = num * BASE + ALPHABET.index(char)
    return num


class URLShortener:
    def __init__(self, prefix: str = "https://short.io/"):
        self.prefix = prefix
        self.url_to_id: dict[str, int] = {}
        self.id_to_url: dict[int, str] = {}
        self.counter = 1000

    def shorten(self, url: str) -> str:
        if url in self.url_to_id:
            code = encode_base62(self.url_to_id[url])
            return self.prefix + code
        self.counter += 1
        self.url_to_id[url] = self.counter
        self.id_to_url[self.counter] = url
        return self.prefix + encode_base62(self.counter)

    def restore(self, short_url: str) -> str | None:
        code = short_url[len(self.prefix):]
        idx = decode_base62(code)
        return self.id_to_url.get(idx)


def self_check() -> None:
    service = URLShortener()
    short = service.shorten("https://docs.python.org/3/")
    assert short.startswith("https://short.io/")
    assert service.restore(short) == "https://docs.python.org/3/"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "huffman_coding",
        "Huffman Coding Compression",
        '''#!/usr/bin/env python3
"""Huffman coding lossless text compression and decompression."""
from __future__ import annotations
import heapq
from collections import Counter


class HuffmanNode:
    def __init__(self, char: str | None, freq: int):
        self.char = char
        self.freq = freq
        self.left: HuffmanNode | None = None
        self.right: HuffmanNode | None = None

    def __lt__(self, other: HuffmanNode) -> bool:
        return self.freq < other.freq


def build_tree(text: str) -> HuffmanNode | None:
    if not text:
        return None
    counts = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in counts.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = HuffmanNode(None, n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(node: HuffmanNode | None, prefix: str = "", codes: dict[str, str] | None = None) -> dict[str, str]:
    if codes is None:
        codes = {}
    if node:
        if node.char is not None:
            codes[node.char] = prefix or "0"
        build_codes(node.left, prefix + "0", codes)
        build_codes(node.right, prefix + "1", codes)
    return codes


def compress(text: str) -> tuple[str, HuffmanNode | None]:
    tree = build_tree(text)
    codes = build_codes(tree)
    encoded = "".join(codes[ch] for ch in text)
    return encoded, tree


def decompress(encoded: str, tree: HuffmanNode | None) -> str:
    if not tree or not encoded:
        return ""
    if tree.left is None and tree.right is None:
        return (tree.char or "") * len(encoded)
    chars = []
    curr = tree
    for bit in encoded:
        curr = curr.left if bit == "0" else curr.right
        if curr and curr.char is not None:
            chars.append(curr.char)
            curr = tree
    return "".join(chars)


def self_check() -> None:
    text = "abracadabra"
    bits, tree = compress(text)
    assert len(bits) < len(text) * 8
    assert decompress(bits, tree) == text
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "rate_limiter",
        "Token Bucket Rate Limiter",
        '''#!/usr/bin/env python3
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
''',
    ),
    (
        "pathfinder_bfs",
        "Maze BFS Pathfinder",
        '''#!/usr/bin/env python3
"""Breadth-First Search (BFS) grid shortest path finder."""
from __future__ import annotations
from collections import deque


def find_shortest_path(grid: list[str], start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]] | None:
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()
        if (r, c) == end:
            return path
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != "#" and (nr, nc) not in visited:
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))
    return None


def self_check() -> None:
    maze = [
        "S..#.",
        "#..#.",
        "...#.",
        ".##..",
        "....E",
    ]
    path = find_shortest_path(maze, (0, 0), (4, 4))
    assert path is not None
    assert path[0] == (0, 0) and path[-1] == (4, 4)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "trie_autocomplete",
        "Trie Autocomplete",
        '''#!/usr/bin/env python3
"""Prefix tree (Trie) dictionary with fast autocompletion."""
from __future__ import annotations


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_word = True

    def autocomplete(self, prefix: str) -> list[str]:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return []
            curr = curr.children[ch]

        results: list[str] = []

        def dfs(node: TrieNode, path: list[str]) -> None:
            if node.is_word:
                results.append("".join(path))
            for char, next_node in sorted(node.children.items()):
                path.append(char)
                dfs(next_node, path)
                path.pop()

        dfs(curr, list(prefix))
        return results


def self_check() -> None:
    trie = Trie()
    for w in ["python", "pyramid", "pytorch", "pyspark", "rust", "ruby"]:
        trie.insert(w)
    matches = trie.autocomplete("pyr")
    assert matches == ["pyramid"]
    py_matches = trie.autocomplete("py")
    assert py_matches == ["pyramid", "pyspark", "python", "pytorch"]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
]


def fallback_project(day_num: int) -> tuple[str, str, str]:
    slug = f"challenge_{day_num:02d}"
    title = f"Python Algorithm Challenge #{day_num:02d}"
    code = f'''#!/usr/bin/env python3
"""Day {day_num:02d}: {title} — number theory & sequence utility."""
from __future__ import annotations


def solve_challenge(n: int) -> list[int]:
    """Return the first n primes greater than or equal to {day_num}."""
    primes: list[int] = []
    candidate = max(2, {day_num})
    while len(primes) < n:
        if all(candidate % d != 0 for d in range(2, int(candidate ** 0.5) + 1)):
            primes.append(candidate)
        candidate += 1
    return primes


def self_check() -> None:
    result = solve_challenge(5)
    assert len(result) == 5
    assert all( result[i] < result[i + 1] for i in range(4) )
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
'''
    return slug, title, code


PAST_CHALLENGES: list[tuple[str, str, str]] = [
    (f"challenge_{d:02d}", f"Python Algorithm Challenge #{d:02d}", fallback_project(d)[2])
    for d in range(23, 37)
]

NEW_PROJECTS: list[tuple[str, str, str]] = [
    (
        "diff_viewer",
        "Text Diff Engine (LCS)",
        '''#!/usr/bin/env python3
"""Line-by-line text difference engine using Longest Common Subsequence."""
from __future__ import annotations


def compute_lcs(a: list[str], b: list[str]) -> list[list[int]]:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i + 1][j], dp[i][j + 1])
    return dp


def diff_lines(text1: str, text2: str) -> list[str]:
    a = text1.splitlines()
    b = text2.splitlines()
    dp = compute_lcs(a, b)
    i, j = len(a), len(b)
    result: list[str] = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            result.append(f"  {a[i - 1]}")
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            result.append(f"+ {b[j - 1]}")
            j -= 1
        else:
            result.append(f"- {a[i - 1]}")
            i -= 1
    return list(reversed(result))


def self_check() -> None:
    t1 = "alpha\\nbeta\\ngamma"
    t2 = "alpha\\nbeta\\ndelta"
    d = diff_lines(t1, t2)
    assert "  alpha" in d
    assert "  beta" in d
    assert "- gamma" in d
    assert "+ delta" in d
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "bloom_filter",
        "Probabilistic Bloom Filter",
        '''#!/usr/bin/env python3
"""Probabilistic Bloom filter with polynomial hash functions."""
from __future__ import annotations


class BloomFilter:
    def __init__(self, size: int = 1024, num_hashes: int = 3):
        self.size = size
        self.num_hashes = num_hashes
        self.bits = [0] * size

    def _hashes(self, item: str) -> list[int]:
        hashes = []
        for seed in range(self.num_hashes):
            h = 0
            for ch in item:
                h = (h * (31 + seed) + ord(ch)) % self.size
            hashes.append(h)
        return hashes

    def add(self, item: str) -> None:
        for idx in self._hashes(item):
            self.bits[idx] = 1

    def might_contain(self, item: str) -> bool:
        return all(self.bits[idx] == 1 for idx in self._hashes(item))


def self_check() -> None:
    bf = BloomFilter(size=512, num_hashes=3)
    bf.add("apple")
    bf.add("banana")
    assert bf.might_contain("apple")
    assert bf.might_contain("banana")
    assert not bf.might_contain("grapefruit_xyz_not_added")
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "cron_parser",
        "Cron Expression Parser",
        '''#!/usr/bin/env python3
"""Standard 5-part cron field parser and validator."""
from __future__ import annotations


def parse_field(field: str, min_val: int, max_val: int) -> set[int]:
    result: set[int] = set()
    for part in field.split(","):
        if "/" in part:
            sub, step_s = part.split("/", 1)
            step = int(step_s)
            start, end = (min_val, max_val) if sub == "*" else (
                (int(sub.split("-")[0]), int(sub.split("-")[1])) if "-" in sub else (int(sub), max_val)
            )
            result.update(range(start, end + 1, step))
        elif "-" in part:
            start_s, end_s = part.split("-", 1)
            result.update(range(int(start_s), int(end_s) + 1))
        elif part == "*":
            result.update(range(min_val, max_val + 1))
        else:
            result.add(int(part))
    return result


def matches_cron(cron_expr: str, minute: int, hour: int, dom: int, month: int, dow: int) -> bool:
    fields = cron_expr.split()
    if len(fields) != 5:
        raise ValueError("Expected 5 fields in cron expression")
    m_set = parse_field(fields[0], 0, 59)
    h_set = parse_field(fields[1], 0, 23)
    dom_set = parse_field(fields[2], 1, 31)
    mon_set = parse_field(fields[3], 1, 12)
    dow_set = parse_field(fields[4], 0, 6)
    return minute in m_set and hour in h_set and dom in dom_set and month in mon_set and dow in dow_set


def self_check() -> None:
    assert matches_cron("*/15 9-17 * * 1-5", 30, 10, 15, 6, 2)
    assert not matches_cron("*/15 9-17 * * 1-5", 7, 10, 15, 6, 2)
    assert not matches_cron("*/15 9-17 * * 1-5", 0, 20, 15, 6, 2)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "event_emitter",
        "Pub-Sub Event Bus",
        '''#!/usr/bin/env python3
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
''',
    ),
    (
        "json_serializer",
        "Minimalist JSON Formatter",
        '''#!/usr/bin/env python3
"""Minimalist recursive JSON serializer and pretty-printer."""
from __future__ import annotations
from typing import Any


def serialize_json(obj: Any, indent: int = 2, current_level: int = 0) -> str:
    sp = " " * (indent * current_level)
    sp_next = " " * (indent * (current_level + 1))
    if obj is None:
        return "null"
    if isinstance(obj, bool):
        return "true" if obj else "false"
    if isinstance(obj, (int, float)):
        return str(obj)
    if isinstance(obj, str):
        escaped = obj.replace('"', '\\\\"').replace('\\n', '\\\\n')
        return f'"{escaped}"'
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = [f"{sp_next}{serialize_json(x, indent, current_level + 1)}" for x in obj]
        return "[\\n" + ",\\n".join(items) + f"\\n{sp}]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = [
            f'{sp_next}"{k}": {serialize_json(v, indent, current_level + 1)}'
            for k, v in obj.items()
        ]
        return "{\\n" + ",\\n".join(items) + f"\\n{sp}}}"
    raise TypeError(f"Type {type(obj)} is not JSON serializable")


def self_check() -> None:
    data = {"status": "ok", "code": 200, "tags": ["py", "json"], "active": True}
    res = serialize_json(data, indent=2)
    assert '"status": "ok"' in res
    assert '"code": 200' in res
    assert '"active": true' in res
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "bank_ledger",
        "Double-Entry Ledger System",
        '''#!/usr/bin/env python3
"""Double-entry accounting transaction ledger with zero-sum validation."""
from __future__ import annotations


class AccountLedger:
    def __init__(self):
        self.accounts: dict[str, int] = {}
        self.journal: list[dict[str, int]] = []

    def get_balance(self, account: str) -> int:
        return self.accounts.get(account, 0)

    def record_entry(self, entry: dict[str, int]) -> bool:
        if sum(entry.values()) != 0:
            raise ValueError("Accounting equation violated: debits and credits must sum to zero")
        for acct, amount in entry.items():
            if self.get_balance(acct) + amount < 0 and not acct.startswith("equity:"):
                return False
        for acct, amount in entry.items():
            self.accounts[acct] = self.get_balance(acct) + amount
        self.journal.append(entry)
        return True


def self_check() -> None:
    ledger = AccountLedger()
    assert ledger.record_entry({"assets:cash": 1000, "equity:capital": -1000})
    assert ledger.record_entry({"assets:savings": 400, "assets:cash": -400})
    assert not ledger.record_entry({"assets:savings": 700, "assets:cash": -700})
    assert ledger.get_balance("assets:cash") == 600
    assert ledger.get_balance("assets:savings") == 400
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "priority_task_scheduler",
        "Min-Heap Task Scheduler",
        '''#!/usr/bin/env python3
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
''',
    ),
    (
        "quadtree",
        "2D Spatial QuadTree",
        '''#!/usr/bin/env python3
"""2D spatial partition QuadTree for bounding box region queries."""
from __future__ import annotations
from typing import NamedTuple


class Point(NamedTuple):
    x: float
    y: float
    data: str


class Rect(NamedTuple):
    x: float
    y: float
    w: float
    h: float

    def contains(self, p: Point) -> bool:
        return self.x <= p.x <= self.x + self.w and self.y <= p.y <= self.y + self.h

    def intersects(self, other: Rect) -> bool:
        return not (
            other.x > self.x + self.w
            or other.x + other.w < self.x
            or other.y > self.y + self.h
            or other.y + other.h < self.y
        )


class QuadTree:
    def __init__(self, boundary: Rect, capacity: int = 4):
        self.boundary = boundary
        self.capacity = capacity
        self.points: list[Point] = []
        self.divided = False
        self.children: list[QuadTree] = []

    def subdivide(self) -> None:
        x, y, w, h = self.boundary.x, self.boundary.y, self.boundary.w / 2, self.boundary.h / 2
        self.children = [
            QuadTree(Rect(x, y, w, h), self.capacity),
            QuadTree(Rect(x + w, y, w, h), self.capacity),
            QuadTree(Rect(x, y + h, w, h), self.capacity),
            QuadTree(Rect(x + w, y + h, w, h), self.capacity),
        ]
        self.divided = True

    def insert(self, p: Point) -> bool:
        if not self.boundary.contains(p):
            return False
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(p)
            return True
        if not self.divided:
            self.subdivide()
            old_pts = self.points
            self.points = []
            for pt in old_pts:
                for c in self.children:
                    if c.insert(pt):
                        break
        return any(c.insert(p) for c in self.children)

    def query(self, range_rect: Rect) -> list[Point]:
        found: list[Point] = []
        if not self.boundary.intersects(range_rect):
            return found
        for p in self.points:
            if range_rect.contains(p):
                found.append(p)
        if self.divided:
            for c in self.children:
                found.extend(c.query(range_rect))
        return found


def self_check() -> None:
    qt = QuadTree(Rect(0, 0, 100, 100), capacity=2)
    qt.insert(Point(10, 10, "A"))
    qt.insert(Point(20, 20, "B"))
    qt.insert(Point(80, 80, "C"))
    matches = qt.query(Rect(0, 0, 30, 30))
    names = {p.data for p in matches}
    assert names == {"A", "B"}
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "regex_engine",
        "Thompson NFA Regex Matcher",
        '''#!/usr/bin/env python3
"""Recursive pattern matcher supporting literals, wildcard '.', and Kleene star '*'."""
from __future__ import annotations


def is_match(text: str, pattern: str) -> bool:
    if not pattern:
        return not text
    first_match = bool(text) and (pattern[0] == text[0] or pattern[0] == ".")
    if len(pattern) >= 2 and pattern[1] == "*":
        return is_match(text, pattern[2:]) or (first_match and is_match(text[1:], pattern))
    return first_match and is_match(text[1:], pattern[1:])


def self_check() -> None:
    assert is_match("aa", "a*")
    assert is_match("ab", ".*")
    assert is_match("aab", "c*a*b")
    assert not is_match("mississippi", "mis*is*p*.")
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "circuit_breaker",
        "Resilient Circuit Breaker",
        '''#!/usr/bin/env python3
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
''',
    ),
    (
        "merkle_tree",
        "Cryptographic Merkle Tree",
        '''#!/usr/bin/env python3
"""Cryptographic Merkle Tree with leaf verification and SHA-256."""
from __future__ import annotations
import hashlib


def sha256(data: str) -> str:
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


class MerkleTree:
    def __init__(self, data_blocks: list[str]):
        self.leaves = [sha256(x) for x in data_blocks]
        self.levels: list[list[str]] = [self.leaves]
        self._build_tree()

    def _build_tree(self) -> None:
        curr = self.leaves
        while len(curr) > 1:
            next_level = []
            for i in range(0, len(curr), 2):
                left = curr[i]
                right = curr[i + 1] if i + 1 < len(curr) else left
                next_level.append(sha256(left + right))
            self.levels.append(next_level)
            curr = next_level

    @property
    def root(self) -> str:
        return self.levels[-1][0] if self.levels and self.levels[-1] else ""


def self_check() -> None:
    tree1 = MerkleTree(["tx1", "tx2", "tx3", "tx4"])
    tree2 = MerkleTree(["tx1", "tx2", "tx3", "tx4"])
    assert tree1.root == tree2.root
    tree_tampered = MerkleTree(["tx1", "tx2_tampered", "tx3", "tx4"])
    assert tree1.root != tree_tampered.root
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "levenshtein_distance",
        "String Fuzzy Matcher",
        '''#!/usr/bin/env python3
"""Levenshtein edit distance and fuzzy keyword suggestion ranker."""
from __future__ import annotations


def levenshtein(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = 0 if s1[i - 1] == s2[j - 1] else 1
            dp[i][j] = min(
                dp[i - 1][j] + 1,
                dp[i][j - 1] + 1,
                dp[i - 1][j - 1] + cost
            )
    return dp[m][n]


def find_closest(query: str, vocabulary: list[str]) -> str | None:
    if not vocabulary:
        return None
    return min(vocabulary, key=lambda word: levenshtein(query, word))


def self_check() -> None:
    assert levenshtein("kitten", "sitting") == 3
    vocab = ["python", "java", "javascript", "golang", "ruby"]
    assert find_closest("pythn", vocab) == "python"
    assert find_closest("rubi", vocab) == "ruby"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "consistent_hash",
        "Consistent Hashing Ring",
        '''#!/usr/bin/env python3
"""Consistent hashing ring with virtual nodes for distributed load-balancing."""
from __future__ import annotations
import bisect
import hashlib


class ConsistentHashRing:
    def __init__(self, vnodes: int = 10):
        self.vnodes = vnodes
        self.ring: list[int] = []
        self.node_map: dict[int, str] = {}

    def _hash(self, key: str) -> int:
        return int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)

    def add_node(self, node: str) -> None:
        for i in range(self.vnodes):
            vkey = f"{node}#vn{i}"
            h = self._hash(vkey)
            bisect.insort(self.ring, h)
            self.node_map[h] = node

    def get_node(self, key: str) -> str | None:
        if not self.ring:
            return None
        h = self._hash(key)
        idx = bisect.bisect_right(self.ring, h)
        if idx == len(self.ring):
            idx = 0
        return self.node_map[self.ring[idx]]


def self_check() -> None:
    ring = ConsistentHashRing(vnodes=5)
    ring.add_node("nodeA")
    ring.add_node("nodeB")
    ring.add_node("nodeC")
    target1 = ring.get_node("user_101")
    target2 = ring.get_node("user_102")
    assert target1 in {"nodeA", "nodeB", "nodeC"}
    assert target2 in {"nodeA", "nodeB", "nodeC"}
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "markdown_table_formatter",
        "Markdown Table Auto-Aligner",
        '''#!/usr/bin/env python3
"""Clean markdown table parser and column-width auto-aligner."""
from __future__ import annotations


def format_markdown_table(table_text: str) -> str:
    lines = [l.strip() for l in table_text.strip().splitlines() if l.strip()]
    rows = [[c.strip() for c in line.strip("|").split("|")] for line in lines]
    if len(rows) < 2:
        return table_text

    header = rows[0]
    data_rows = [r for r in rows[2:]] if any("-" in c for c in rows[1]) else rows[1:]
    col_count = len(header)
    widths = [len(h) for h in header]

    for r in data_rows:
        for i, val in enumerate(r[:col_count]):
            widths[i] = max(widths[i], len(val))

    def make_line(cells: list[str]) -> str:
        padded = [cells[i].ljust(widths[i]) if i < len(cells) else "".ljust(widths[i]) for i in range(col_count)]
        return "| " + " | ".join(padded) + " |"

    sep_line = "| " + " | ".join("-" * w for w in widths) + " |"
    result = [make_line(header), sep_line]
    for r in data_rows:
        result.append(make_line(r))
    return "\\n".join(result)


def self_check() -> None:
    raw = "|ID|Name|Score|\\n|-|-|-|\\n|1|Alice|95|\\n|20|Bob|8|"
    formatted = format_markdown_table(raw)
    assert "| ID | Name  | Score |" in formatted
    assert "| 1  | Alice | 95    |" in formatted
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "fsm_turnstile",
        "Finite State Machine Engine",
        '''#!/usr/bin/env python3
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
''',
    ),
    (
        "roman_numerals",
        "Roman Numeral Converter",
        '''#!/usr/bin/env python3
"""Bidirectional Roman numeral <-> Arabic integer converter."""
from __future__ import annotations

MAPPINGS = [
    (1000, "M"), (900, "CM"), (500, "D"), (400, "CD"),
    (100, "C"), (90, "XC"), (50, "L"), (40, "XL"),
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")
]


def to_roman(n: int) -> str:
    if not (1 <= n <= 3999):
        raise ValueError("Number out of Roman numeral range (1-3999)")
    result = []
    for val, sym in MAPPINGS:
        while n >= val:
            result.append(sym)
            n -= val
    return "".join(result)


def from_roman(s: str) -> int:
    val_map = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0
    prev = 0
    for ch in reversed(s):
        curr = val_map[ch]
        total = (total - curr) if curr < prev else (total + curr)
        prev = curr
    return total


def self_check() -> None:
    assert to_roman(1994) == "MCMXCIV"
    assert from_roman("MCMXCIV") == 1994
    assert to_roman(58) == "LVIII"
    assert from_roman("LVIII") == 58
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "tar_archiver",
        "Minimal TAR Archiver",
        '''#!/usr/bin/env python3
"""Minimalist UStar TAR archive generator and extractor."""
from __future__ import annotations


def make_tar_header(name: str, size: int) -> bytes:
    name_bytes = name.encode("utf-8").ljust(100, b"\\x00")
    mode = b"0000644\\x00"
    uid = b"0001000\\x00"
    gid = b"0001000\\x00"
    size_oct = f"{size:011o}\\x00".encode("ascii")
    mtime = b"00000000000\\x00"
    chksum_placeholder = b"        "
    typeflag = b"0"
    magic = b"ustar\\x0000"
    header_pre = (
        name_bytes + mode + uid + gid + size_oct + mtime + chksum_placeholder + typeflag
    ).ljust(257, b"\\x00") + magic
    header_full = header_pre.ljust(512, b"\\x00")
    chksum = sum(header_full)
    chksum_bytes = f"{chksum:06o}\\x00 ".encode("ascii")
    return header_full[:148] + chksum_bytes + header_full[156:]


def create_archive(files: dict[str, bytes]) -> bytes:
    chunks = []
    for filename, content in files.items():
        header = make_tar_header(filename, len(content))
        chunks.append(header)
        chunks.append(content)
        pad = (512 - (len(content) % 512)) % 512
        if pad:
            chunks.append(b"\\x00" * pad)
    chunks.append(b"\\x00" * 1024)
    return b"".join(chunks)


def extract_archive(archive_bytes: bytes) -> dict[str, bytes]:
    files = {}
    pos = 0
    while pos + 512 <= len(archive_bytes):
        header = archive_bytes[pos : pos + 512]
        if header == b"\\x00" * 512:
            break
        name = header[:100].rstrip(b"\\x00").decode("utf-8")
        size_str = header[124:136].rstrip(b"\\x00 ").decode("ascii")
        size = int(size_str, 8) if size_str else 0
        pos += 512
        content = archive_bytes[pos : pos + size]
        files[name] = content
        pad = (512 - (size % 512)) % 512
        pos += size + pad
    return files


def self_check() -> None:
    data = {"hello.txt": b"Hello World!\\n", "test.py": b"print(42)\\n"}
    tar = create_archive(data)
    extracted = extract_archive(tar)
    assert extracted == data
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "lisp_evaluator",
        "Tiny Lisp S-Expression Evaluator",
        '''#!/usr/bin/env python3
"""Tiny Scheme/Lisp S-expression parser and tree evaluator."""
from __future__ import annotations
from typing import Any


def tokenize(chars: str) -> list[str]:
    return chars.replace("(", " ( ").replace(")", " ) ").split()


def parse_tokens(tokens: list[str]) -> Any:
    if not tokens:
        raise SyntaxError("Unexpected EOF")
    token = tokens.pop(0)
    if token == "(":
        L = []
        while tokens and tokens[0] != ")":
            L.append(parse_tokens(tokens))
        tokens.pop(0)
        return L
    elif token == ")":
        raise SyntaxError("Unexpected )")
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token


class Env(dict):
    def __init__(self, params=(), args=(), outer=None):
        self.update(zip(params, args))
        self.outer = outer

    def find(self, var: str):
        return self if var in self else (self.outer.find(var) if self.outer else None)


def standard_env() -> Env:
    env = Env()
    env.update({
        "+": lambda a, b: a + b,
        "-": lambda a, b: a - b,
        "*": lambda a, b: a * b,
        "/": lambda a, b: a / b,
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        "=": lambda a, b: a == b,
    })
    return env


def evaluate(x: Any, env: Env) -> Any:
    if isinstance(x, str):
        e = env.find(x)
        if e is None:
            raise NameError(f"Undefined symbol: {x}")
        return e[x]
    elif not isinstance(x, list):
        return x
    op = x[0]
    if op == "if":
        (_, test, conseq, alt) = x
        exp = conseq if evaluate(test, env) else alt
        return evaluate(exp, env)
    elif op == "define":
        (_, symbol, exp) = x
        env[symbol] = evaluate(exp, env)
        return env[symbol]
    elif op == "lambda":
        (_, parms, body) = x
        return lambda *args: evaluate(body, Env(parms, args, env))
    else:
        proc = evaluate(op, env)
        vals = [evaluate(arg, env) for arg in x[1:]]
        return proc(*vals)


def self_check() -> None:
    global_env = standard_env()
    t1 = parse_tokens(tokenize("(+ 10 (* 2 3))"))
    assert evaluate(t1, global_env) == 16
    t2 = parse_tokens(tokenize("(define square (lambda (r) (* r r)))"))
    evaluate(t2, global_env)
    t3 = parse_tokens(tokenize("(square 5)"))
    assert evaluate(t3, global_env) == 25
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "base64_codec",
        "RFC 4648 Base64 Codec",
        '''#!/usr/bin/env python3
"""RFC 4648 standard Base64 bitwise encoder and decoder."""
from __future__ import annotations

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
REV = {ch: i for i, ch in enumerate(CHARS)}


def b64_encode(data: bytes) -> str:
    result = []
    i = 0
    n = len(data)
    while i < n:
        b0 = data[i]
        b1 = data[i + 1] if i + 1 < n else 0
        b2 = data[i + 2] if i + 2 < n else 0
        triplet = (b0 << 16) | (b1 << 8) | b2
        result.append(CHARS[(triplet >> 18) & 0x3F])
        result.append(CHARS[(triplet >> 12) & 0x3F])
        result.append(CHARS[(triplet >> 6) & 0x3F] if i + 1 < n else "=")
        result.append(CHARS[triplet & 0x3F] if i + 2 < n else "=")
        i += 3
    return "".join(result)


def b64_decode(encoded: str) -> bytes:
    clean = encoded.rstrip("=")
    val = 0
    bits = 0
    out = bytearray()
    for ch in clean:
        val = (val << 6) | REV[ch]
        bits += 6
        if bits >= 8:
            bits -= 8
            out.append((val >> bits) & 0xFF)
    return bytes(out)


def self_check() -> None:
    cases = [b"M", b"Ma", b"Man", b"Hello, Python!"]
    for c in cases:
        enc = b64_encode(c)
        dec = b64_decode(enc)
        assert dec == c
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "binary_search_tree",
        "Balanced AVL Binary Tree",
        '''#!/usr/bin/env python3
"""Self-balancing AVL Binary Search Tree implementation."""
from __future__ import annotations


class AVLNode:
    def __init__(self, key: int):
        self.key = key
        self.left: AVLNode | None = None
        self.right: AVLNode | None = None
        self.height = 1


def get_height(node: AVLNode | None) -> int:
    return node.height if node else 0


def get_balance(node: AVLNode | None) -> int:
    return get_height(node.left) - get_height(node.right) if node else 0


def rotate_right(y: AVLNode) -> AVLNode:
    x = y.left
    assert x is not None
    t2 = x.right
    x.right = y
    y.left = t2
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    return x


def rotate_left(x: AVLNode) -> AVLNode:
    y = x.right
    assert y is not None
    t2 = y.left
    y.left = x
    x.right = t2
    x.height = 1 + max(get_height(x.left), get_height(x.right))
    y.height = 1 + max(get_height(y.left), get_height(y.right))
    return y


def insert_avl(root: AVLNode | None, key: int) -> AVLNode:
    if not root:
        return AVLNode(key)
    if key < root.key:
        root.left = insert_avl(root.left, key)
    elif key > root.key:
        root.right = insert_avl(root.right, key)
    else:
        return root

    root.height = 1 + max(get_height(root.left), get_height(root.right))
    bal = get_balance(root)

    if bal > 1 and root.left and key < root.left.key:
        return rotate_right(root)
    if bal < -1 and root.right and key > root.right.key:
        return rotate_left(root)
    if bal > 1 and root.left and key > root.left.key:
        root.left = rotate_left(root.left)
        return rotate_right(root)
    if bal < -1 and root.right and key < root.right.key:
        root.right = rotate_right(root.right)
        return rotate_left(root)
    return root


def inorder(root: AVLNode | None) -> list[int]:
    return inorder(root.left) + [root.key] + inorder(root.right) if root else []


def self_check() -> None:
    root = None
    keys = [10, 20, 30, 40, 50, 25]
    for k in keys:
        root = insert_avl(root, k)
    assert inorder(root) == sorted(keys)
    assert abs(get_balance(root)) <= 1
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
    (
        "websocket_frame_parser",
        "WebSocket Frame Decoder",
        '''#!/usr/bin/env python3
"""RFC 6455 WebSocket binary frame decoder and mask unmasker."""
from __future__ import annotations


def parse_ws_frame(data: bytes) -> tuple[int, bool, bytes]:
    if len(data) < 2:
        raise ValueError("Frame too short")
    b1, b2 = data[0], data[1]
    fin = (b1 & 0x80) != 0
    opcode = b1 & 0x0F
    is_masked = (b2 & 0x80) != 0
    payload_len = b2 & 0x7F
    offset = 2

    if payload_len == 126:
        payload_len = int.from_bytes(data[offset : offset + 2], "big")
        offset += 2
    elif payload_len == 127:
        payload_len = int.from_bytes(data[offset : offset + 8], "big")
        offset += 8

    if is_masked:
        mask = data[offset : offset + 4]
        offset += 4
        masked_payload = data[offset : offset + payload_len]
        payload = bytes(b ^ mask[i % 4] for i, b in enumerate(masked_payload))
    else:
        payload = data[offset : offset + payload_len]
    return opcode, fin, payload


def self_check() -> None:
    raw = bytes([0x81, 0x85, 0x37, 0xfa, 0x21, 0x3d, 0x7f, 0x9f, 0x4d, 0x51, 0x58])
    opcode, fin, payload = parse_ws_frame(raw)
    assert opcode == 1
    assert fin is True
    assert payload == b"Hello"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
''',
    ),
]

PROJECTS.extend(PAST_CHALLENGES)
PROJECTS.extend(NEW_PROJECTS)


def existing_days() -> list[int]:
    days: list[int] = []
    for p in ROOT.iterdir():
        if p.is_dir():
            m = re.match(r"^day(\d+)_", p.name)
            if m:
                days.append(int(m.group(1)))
    return sorted(days)


def generate_next() -> pathlib.Path:
    days = existing_days()
    next_day = (days[-1] + 1) if days else 1
    idx = next_day - 2  # Day 2 maps to PROJECTS[0]
    if 0 <= idx < len(PROJECTS):
        slug, title, code = PROJECTS[idx]
    else:
        slug, title, code = fallback_project(next_day)

    folder = ROOT / f"day{next_day:02d}_{slug}"
    folder.mkdir(parents=True, exist_ok=True)
    script_path = folder / f"{slug}.py"
    script_path.write_text(code, encoding="utf-8")

    subprocess.run([sys.executable, str(script_path), "--check"], check=True)
    update_readme(next_day, title, f"day{next_day:02d}_{slug}/{slug}.py")
    return script_path


def update_readme(day_num: int, title: str, rel_path: str) -> None:
    readme = ROOT / "README.md"
    content = readme.read_text(encoding="utf-8")
    row = f"| Day {day_num:02d} | {title} | [`{rel_path}`]({rel_path}) | ✅ Completed |"
    lines = [
        line for line in content.splitlines()
        if not line.startswith(f"- **Day {day_num:02d}**:")
    ]
    if row not in content:
        insert_at = next(
            (i for i, line in enumerate(lines) if line.startswith("## Upcoming Queue")),
            len(lines),
        )
        while insert_at > 0 and lines[insert_at - 1].strip() == "":
            insert_at -= 1
        lines.insert(insert_at, row)
    readme.write_text("\n".join(lines) + "\n", encoding="utf-8")


def self_check() -> None:
    assert 1 in existing_days()
    for slug, title, code in PROJECTS:
        assert "def self_check" in code, f"{slug} missing self_check"
    print("Generator self-check passed.")


if __name__ == "__main__":
    if "--check" in sys.argv:
        self_check()
    else:
        created = generate_next()
        print(f"Created and verified: {created.relative_to(ROOT)}")
