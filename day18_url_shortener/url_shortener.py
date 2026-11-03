#!/usr/bin/env python3
"""URL Shortener service with Base62 encoding and decoding."""
from __future__ import annotations

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
BASE = len(ALPHABET)


def encode_base62(num: int) -> str:
    if num == 0:
        return ALPHABET[0]
    chars = []
    while num > 0:
        chars.append(ALPHABET[num % BASE])
        num //= BASE
    return "".join(reversed(chars))


def decode_base62(s: str) -> int:
    num = 0
    for char in s:
        num = num * BASE + ALPHABET.index(char)
    return num


class URLShortener:
    def __init__(self, prefix: str = "https://short.io/"):
        self.prefix = prefix
        self.url_to_id: dict[str, int] = {}
        self.id_to_url: dict[int, str] = {}
        self.counter = 1000

    def shorten(self, url: str) -> str:
        if url in self.url_to_id:
            code = encode_base62(self.url_to_id[url])
            return self.prefix + code
        self.counter += 1
        self.url_to_id[url] = self.counter
        self.id_to_url[self.counter] = url
        return self.prefix + encode_base62(self.counter)

    def restore(self, short_url: str) -> str | None:
        code = short_url[len(self.prefix):]
        idx = decode_base62(code)
        return self.id_to_url.get(idx)


def self_check() -> None:
    service = URLShortener()
    short = service.shorten("https://docs.python.org/3/")
    assert short.startswith("https://short.io/")
    assert service.restore(short) == "https://docs.python.org/3/"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
