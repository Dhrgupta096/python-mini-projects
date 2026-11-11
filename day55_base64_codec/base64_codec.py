#!/usr/bin/env python3
"""RFC 4648 standard Base64 bitwise encoder and decoder."""
from __future__ import annotations

CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
REV = {ch: i for i, ch in enumerate(CHARS)}


def b64_encode(data: bytes) -> str:
    result = []
    i = 0
    n = len(data)
    while i < n:
        b0 = data[i]
        b1 = data[i + 1] if i + 1 < n else 0
        b2 = data[i + 2] if i + 2 < n else 0
        triplet = (b0 << 16) | (b1 << 8) | b2
        result.append(CHARS[(triplet >> 18) & 0x3F])
        result.append(CHARS[(triplet >> 12) & 0x3F])
        result.append(CHARS[(triplet >> 6) & 0x3F] if i + 1 < n else "=")
        result.append(CHARS[triplet & 0x3F] if i + 2 < n else "=")
        i += 3
    return "".join(result)


def b64_decode(encoded: str) -> bytes:
    clean = encoded.rstrip("=")
    val = 0
    bits = 0
    out = bytearray()
    for ch in clean:
        val = (val << 6) | REV[ch]
        bits += 6
        if bits >= 8:
            bits -= 8
            out.append((val >> bits) & 0xFF)
    return bytes(out)


def self_check() -> None:
    cases = [b"M", b"Ma", b"Man", b"Hello, Python!"]
    for c in cases:
        enc = b64_encode(c)
        dec = b64_decode(enc)
        assert dec == c
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
