#!/usr/bin/env python3
"""Rivest RC4 symmetric stream cipher keystream generator and encryptor/decryptor."""
from __future__ import annotations


class RC4:
    def __init__(self, key: bytes):
        if not key:
            raise ValueError("Key must not be empty")
        self.s = list(range(256))
        j = 0
        for i in range(256):
            j = (j + self.s[i] + key[i % len(key)]) % 256
            self.s[i], self.s[j] = self.s[j], self.s[i]
        self.i = 0
        self.j = 0

    def _generator(self):
        while True:
            self.i = (self.i + 1) % 256
            self.j = (self.j + self.s[self.i]) % 256
            self.s[self.i], self.s[self.j] = self.s[self.j], self.s[self.i]
            k = self.s[(self.s[self.i] + self.s[self.j]) % 256]
            yield k

    def crypt(self, data: bytes) -> bytes:
        gen = self._generator()
        return bytes(b ^ next(gen) for b in data)


def self_check() -> None:
    key = b"SecretKey"
    plaintext = b"Hello, Python Mini-Projects!"
    cipher = RC4(key)
    ciphertext = cipher.crypt(plaintext)
    assert ciphertext != plaintext
    decipher = RC4(key)
    decrypted = decipher.crypt(ciphertext)
    assert decrypted == plaintext

    test_rc4 = RC4(b"Key")
    assert test_rc4.crypt(b"Plaintext").hex() == "bbf316e8d940af0ad3"
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
