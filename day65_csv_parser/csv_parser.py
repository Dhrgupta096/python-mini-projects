#!/usr/bin/env python3
"""RFC 4180 compliant CSV parser supporting quotes and escaped fields."""
from __future__ import annotations


def parse_csv(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    current_row: list[str] = []
    field: list[str] = []
    in_quotes = False
    i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if in_quotes:
            if c == '"':
                if i + 1 < n and text[i + 1] == '"':
                    field.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                field.append(c)
        else:
            if c == '"':
                in_quotes = True
            elif c == ',':
                current_row.append("".join(field))
                field = []
            elif c in '\r\n':
                if c == '\r' and i + 1 < n and text[i + 1] == '\n':
                    i += 1
                current_row.append("".join(field))
                rows.append(current_row)
                current_row = []
                field = []
            else:
                field.append(c)
        i += 1
    if field or current_row:
        current_row.append("".join(field))
        rows.append(current_row)
    return rows


def self_check() -> None:
    data = 'name,notes,score\n"Smith, John","Said ""hello""",95\nAlice,Regular,100'
    parsed = parse_csv(data)
    assert len(parsed) == 3
    assert parsed[1] == ['Smith, John', 'Said "hello"', '95']
    assert parsed[2] == ['Alice', 'Regular', '100']
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
