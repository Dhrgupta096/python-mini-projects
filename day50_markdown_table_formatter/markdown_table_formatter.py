#!/usr/bin/env python3
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
    return "\n".join(result)


def self_check() -> None:
    raw = "|ID|Name|Score|\n|-|-|-|\n|1|Alice|95|\n|20|Bob|8|"
    formatted = format_markdown_table(raw)
    assert "| ID | Name  | Score |" in formatted
    assert "| 1  | Alice | 95    |" in formatted
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
