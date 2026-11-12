#!/usr/bin/env python3
"""Streaming binary cursor buffer for unpacking primitives and structured bytes."""
from __future__ import annotations
import struct


class ByteBuffer:
    def __init__(self, data: bytes):
        self.data = data
        self.offset = 0

    def remaining(self) -> int:
        return len(self.data) - self.offset

    def read_uint8(self) -> int:
        val = self.data[self.offset]
        self.offset += 1
        return val

    def read_uint16_be(self) -> int:
        val = struct.unpack_from(">H", self.data, self.offset)[0]
        self.offset += 2
        return val

    def read_uint32_be(self) -> int:
        val = struct.unpack_from(">I", self.data, self.offset)[0]
        self.offset += 4
        return val

    def read_bytes(self, length: int) -> bytes:
        val = self.data[self.offset : self.offset + length]
        self.offset += length
        return val

    def read_pstring(self) -> str:
        length = self.read_uint8()
        return self.read_bytes(length).decode("utf-8")


def self_check() -> None:
    packet = struct.pack(">H B I B", 0xCAFE, 2, 100, 11) + b"Antigravity"
    buf = ByteBuffer(packet)
    assert buf.read_uint16_be() == 0xCAFE
    assert buf.read_uint8() == 2
    assert buf.read_uint32_be() == 100
    assert buf.read_pstring() == "Antigravity"
    assert buf.remaining() == 0
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
