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
    def __init__(self, capacity: int, refill_rate_per_sec: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_sec
        self.tokens = float(capacity)
        self.last_refill = time.monotonic()

    def allow_request(self, tokens: int = 1, current_time: float | None = None) -> bool:
        now = time.monotonic() if current_time is None else current_time
        elapsed = now - self.last_refill
        self.tokens = min(self.capacity, self.tokens + elapsed * self.refill_rate)
        self.last_refill = now

        if self.tokens >= tokens:
            self.tokens -= tokens
            return True
        return False


def self_check() -> None:
    limiter = TokenBucket(capacity=3, refill_rate_per_sec=1.0)
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
