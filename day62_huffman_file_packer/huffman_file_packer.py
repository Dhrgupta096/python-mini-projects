#!/usr/bin/env python3
"""Byte-aligned bit-packer and unpacker for variable-length bitstreams."""
from __future__ import annotations


class BitStreamWriter:
    def __init__(self):
        self.bytes_out = bytearray()
        self.current_byte = 0
        self.bit_count = 0

    def write_bit(self, bit: int) -> None:
        self.current_byte = (self.current_byte << 1) | (bit & 1)
        self.bit_count += 1
        if self.bit_count == 8:
            self.bytes_out.append(self.current_byte)
            self.current_byte = 0
            self.bit_count = 0

    def write_bits(self, bit_string: str) -> None:
        for b in bit_string:
            self.write_bit(1 if b == "1" else 0)

    def flush(self) -> bytes:
        if self.bit_count > 0:
            self.bytes_out.append(self.current_byte << (8 - self.bit_count))
            self.current_byte = 0
            self.bit_count = 0
        return bytes(self.bytes_out)


class BitStreamReader:
    def __init__(self, data: bytes):
        self.data = data
        self.byte_pos = 0
        self.bit_pos = 0

    def read_bit(self) -> int | None:
        if self.byte_pos >= len(self.data):
            return None
        bit = (self.data[self.byte_pos] >> (7 - self.bit_pos)) & 1
        self.bit_pos += 1
        if self.bit_pos == 8:
            self.bit_pos = 0
            self.byte_pos += 1
        return bit


def self_check() -> None:
    writer = BitStreamWriter()
    test_bits = "11010010111"
    writer.write_bits(test_bits)
    packed = writer.flush()
    reader = BitStreamReader(packed)
    recovered = "".join(str(reader.read_bit()) for _ in range(len(test_bits)))
    assert recovered == test_bits
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
