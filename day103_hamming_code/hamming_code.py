#!/usr/bin/env python3
"""Hamming(7,4) single-bit error-correcting encoder and decoder."""
from __future__ import annotations


def encode_nibble(bits: list[int]) -> list[int]:
    if len(bits) != 4 or any(b not in (0, 1) for b in bits):
        raise ValueError("Input must be 4 bits (0 or 1)")
    d1, d2, d3, d4 = bits
    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p3 = d2 ^ d3 ^ d4
    return [p1, p2, d1, p3, d2, d3, d4]


def decode_block(block: list[int]) -> tuple[list[int], int]:
    """Decode 7-bit Hamming block, correcting any 1-bit error. Returns (data_bits, error_pos_1idx)."""
    if len(block) != 7 or any(b not in (0, 1) for b in block):
        raise ValueError("Block must be 7 bits (0 or 1)")
    b = block.copy()
    s1 = b[0] ^ b[2] ^ b[4] ^ b[6]
    s2 = b[1] ^ b[2] ^ b[5] ^ b[6]
    s3 = b[3] ^ b[4] ^ b[5] ^ b[6]
    err_pos = s1 + (s2 << 1) + (s3 << 2)
    if err_pos != 0:
        b[err_pos - 1] ^= 1
    return [b[2], b[4], b[5], b[6]], err_pos


def self_check() -> None:
    data = [1, 0, 1, 1]
    encoded = encode_nibble(data)
    decoded, err = decode_block(encoded)
    assert decoded == data and err == 0
    for flip_idx in range(7):
        corrupted = encoded.copy()
        corrupted[flip_idx] ^= 1
        fixed, err_pos = decode_block(corrupted)
        assert fixed == data
        assert err_pos == flip_idx + 1
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
