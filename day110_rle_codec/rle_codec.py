#!/usr/bin/env python3
"""Byte-oriented Run-Length Encoding (RLE) compressor and decompressor."""
from __future__ import annotations


def rle_encode(data: bytes) -> bytes:
    out = bytearray()
    i = 0
    n = len(data)
    while i < n:
        b = data[i]
        run = 1
        while i + run < n and data[i + run] == b and run < 255:
            run += 1
        out.append(run)
        out.append(b)
        i += run
    return bytes(out)


def rle_decode(encoded: bytes) -> bytes:
    if len(encoded) % 2 != 0:
        raise ValueError("Invalid RLE stream length")
    out = bytearray()
    for i in range(0, len(encoded), 2):
        out.extend(bytes([encoded[i + 1]]) * encoded[i])
    return bytes(out)


def self_check() -> None:
    sample = b"AAAAABBBCCDAA" + b"X" * 300
    enc = rle_encode(sample)
    assert len(enc) < len(sample)
    assert rle_decode(enc) == sample
    assert rle_decode(rle_encode(b"")) == b""
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
