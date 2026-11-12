#!/usr/bin/env python3
"""BitTorrent Bencode encoder and decoder for integers, strings, lists, and dicts."""
from __future__ import annotations
from typing import Any


def bencode_decode(data: bytes) -> Any:
    pos = 0

    def parse() -> Any:
        nonlocal pos
        b = data[pos : pos + 1]
        if b == b"i":
            pos += 1
            end = data.index(b"e", pos)
            num = int(data[pos:end])
            pos = end + 1
            return num
        elif b == b"l":
            pos += 1
            res = []
            while data[pos : pos + 1] != b"e":
                res.append(parse())
            pos += 1
            return res
        elif b == b"d":
            pos += 1
            res = {}
            while data[pos : pos + 1] != b"e":
                k = parse()
                v = parse()
                res[k.decode("utf-8") if isinstance(k, bytes) else str(k)] = v
            pos += 1
            return res
        elif b.isdigit():
            colon = data.index(b":", pos)
            length = int(data[pos:colon])
            pos = colon + 1
            raw = data[pos : pos + length]
            pos += length
            return raw
        raise ValueError(f"Invalid bencode token at {pos}: {b}")

    return parse()


def bencode_encode(obj: Any) -> bytes:
    if isinstance(obj, int):
        return f"i{obj}e".encode("ascii")
    if isinstance(obj, bytes):
        return f"{len(obj)}:".encode("ascii") + obj
    if isinstance(obj, str):
        b = obj.encode("utf-8")
        return f"{len(b)}:".encode("ascii") + b
    if isinstance(obj, list):
        return b"l" + b"".join(bencode_encode(x) for x in obj) + b"e"
    if isinstance(obj, dict):
        items = sorted(obj.items())
        return b"d" + b"".join(bencode_encode(k) + bencode_encode(v) for k, v in items) + b"e"
    raise TypeError(f"Cannot bencode type: {type(obj)}")


def self_check() -> None:
    data = {"announce": "udp://tracker.open.org:1337", "info": {"length": 1048576, "name": "sample.iso"}}
    encoded = bencode_encode(data)
    decoded = bencode_decode(encoded)
    assert decoded["info"]["length"] == 1048576
    assert decoded["info"]["name"] == b"sample.iso"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
