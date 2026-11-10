#!/usr/bin/env python3
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
