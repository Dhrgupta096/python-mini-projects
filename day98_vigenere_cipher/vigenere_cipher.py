#!/usr/bin/env python3
"""Polyalphabetic Vigenere cipher encoder and decoder for ASCII letters."""
from __future__ import annotations


def _transform(text: str, key: str, decrypt: bool = False) -> str:
    clean_key = [ord(c.upper()) - ord("A") for c in key if c.isalpha()]
    if not clean_key:
        raise ValueError("Key must contain at least one alphabetic character")
    out: list[str] = []
    ki = 0
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            shift = clean_key[ki % len(clean_key)]
            if decrypt:
                shift = -shift
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            ki += 1
        else:
            out.append(ch)
    return "".join(out)


def encrypt(plaintext: str, key: str) -> str:
    return _transform(plaintext, key, decrypt=False)


def decrypt(ciphertext: str, key: str) -> str:
    return _transform(ciphertext, key, decrypt=True)


def self_check() -> None:
    ct = encrypt("ATTACKATDAWN", "LEMON")
    assert ct == "LXFOPVEFRNHR"
    assert decrypt(ct, "LEMON") == "ATTACKATDAWN"
    mixed = encrypt("Hello, World!", "Key")
    assert decrypt(mixed, "Key") == "Hello, World!"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
