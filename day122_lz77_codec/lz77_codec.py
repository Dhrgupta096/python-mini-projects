#!/usr/bin/env python3
"""LZ77 sliding-window dictionary compressor and decompressor."""
from __future__ import annotations

Token = tuple[int, int, str]


def lz77_compress(text: str, window_size: int = 32, lookahead: int = 16) -> list[Token]:
    tokens: list[Token] = []
    i = 0
    n = len(text)
    while i < n:
        best_dist = 0
        best_len = 0
        start = max(0, i - window_size)
        max_l = min(lookahead, n - i)
        for j in range(start, i):
            length = 0
            while length < max_l and text[j + length] == text[i + length]:
                length += 1
            if length > best_len:
                best_len = length
                best_dist = i - j
        if i + best_len < n:
            next_char = text[i + best_len]
            tokens.append((best_dist, best_len, next_char))
            i += best_len + 1
        else:
            tokens.append((best_dist, best_len, ""))
            i += best_len
    return tokens


def lz77_decompress(tokens: list[Token]) -> str:
    out: list[str] = []
    for dist, length, ch in tokens:
        if length > 0:
            start = len(out) - dist
            for k in range(length):
                out.append(out[start + k])
        if ch:
            out.append(ch)
    return "".join(out)


def self_check() -> None:
    msg = "ABRACADABRA_ABRACADABRA_ABRA!"
    toks = lz77_compress(msg)
    assert len(toks) < len(msg)
    assert lz77_decompress(toks) == msg
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
