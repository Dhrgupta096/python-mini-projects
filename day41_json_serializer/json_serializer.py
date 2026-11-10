#!/usr/bin/env python3
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
        escaped = obj.replace('"', '\\"').replace('\n', '\\n')
        return f'"{escaped}"'
    if isinstance(obj, list):
        if not obj:
            return "[]"
        items = [f"{sp_next}{serialize_json(x, indent, current_level + 1)}" for x in obj]
        return "[\n" + ",\n".join(items) + f"\n{sp}]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = [
            f'{sp_next}"{k}": {serialize_json(v, indent, current_level + 1)}'
            for k, v in obj.items()
        ]
        return "{\n" + ",\n".join(items) + f"\n{sp}}}"
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
