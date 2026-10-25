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
    assert score_guess("apple", "puppy") == ".Y.G."
    assert score_guess("abbey", "babes") == "YYGG."
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
