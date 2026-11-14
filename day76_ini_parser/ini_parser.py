#!/usr/bin/env python3
"""Sectioned INI file parser and serializer without external dependencies."""
from __future__ import annotations


def parse_ini(content: str) -> dict[str, dict[str, str]]:
    result: dict[str, dict[str, str]] = {}
    current_section = "DEFAULT"
    result[current_section] = {}
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(";") or line.startswith("#"):
            continue
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1].strip()
            result.setdefault(current_section, {})
        elif "=" in line:
            key, val = line.split("=", 1)
            result[current_section][key.strip()] = val.strip()
    return result


def serialize_ini(data: dict[str, dict[str, str]]) -> str:
    lines = []
    for section, entries in data.items():
        if section != "DEFAULT" or entries:
            lines.append(f"[{section}]")
            for k, v in entries.items():
                lines.append(f"{k} = {v}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"


def self_check() -> None:
    sample = """
    # Server configuration
    [server]
    port = 8080
    host = localhost
    [database]
    name = mydb
    """
    parsed = parse_ini(sample)
    assert parsed["server"]["port"] == "8080"
    assert parsed["database"]["name"] == "mydb"
    serialized = serialize_ini(parsed)
    assert "[server]" in serialized
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
