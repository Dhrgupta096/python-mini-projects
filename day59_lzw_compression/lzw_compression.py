#!/usr/bin/env python3
"""Lempel-Ziv-Welch (LZW) dictionary compression and decompression."""
from __future__ import annotations


def lzw_compress(uncompressed: str) -> list[int]:
    dict_size = 256
    dictionary = {chr(i): i for i in range(dict_size)}
    w = ""
    result = []
    for c in uncompressed:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return result


def lzw_decompress(compressed: list[int]) -> str:
    dict_size = 256
    dictionary = {i: chr(i) for i in range(dict_size)}
    if not compressed:
        return ""
    w = chr(compressed[0])
    result = [w]
    for k in compressed[1:]:
        if k in dictionary:
            entry = dictionary[k]
        elif k == dict_size:
            entry = w + w[0]
        else:
            raise ValueError(f"Bad compressed k: {k}")
        result.append(entry)
        dictionary[dict_size] = w + entry[0]
        dict_size += 1
        w = entry
    return "".join(result)


def self_check() -> None:
    text = "TOBEORNOTTOBEORTOBEORNOT"
    comp = lzw_compress(text)
    decomp = lzw_decompress(comp)
    assert decomp == text
    assert len(comp) < len(text)
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
