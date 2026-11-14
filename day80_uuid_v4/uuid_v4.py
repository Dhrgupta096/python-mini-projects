#!/usr/bin/env python3
"""RFC 4122 compliant UUID Version 4 generator and validator."""
from __future__ import annotations
import secrets
import re


def generate_uuid4() -> str:
    random_bytes = bytearray(secrets.token_bytes(16))
    random_bytes[6] = (random_bytes[6] & 0x0F) | 0x40
    random_bytes[8] = (random_bytes[8] & 0x3F) | 0x80
    hex_str = random_bytes.hex()
    return f"{hex_str[0:8]}-{hex_str[8:12]}-{hex_str[12:16]}-{hex_str[16:20]}-{hex_str[20:32]}"


def is_valid_uuid4(uuid_str: str) -> bool:
    pattern = r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"
    return bool(re.match(pattern, uuid_str.lower()))


def self_check() -> None:
    u = generate_uuid4()
    assert len(u) == 36
    assert is_valid_uuid4(u)
    assert u[14] == "4"
    assert u[19] in "89abAB"
    assert generate_uuid4() != generate_uuid4()
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
