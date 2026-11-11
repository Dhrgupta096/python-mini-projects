#!/usr/bin/env python3
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
