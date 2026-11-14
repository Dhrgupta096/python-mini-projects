#!/usr/bin/env python3
"""Modular exponentiation Diffie-Hellman cryptographic key exchange."""
from __future__ import annotations


class DiffieHellman:
    def __init__(self, p: int = 23, g: int = 5):
        self.p = p
        self.g = g

    def generate_keypair(self, private_key: int) -> tuple[int, int]:
        public_key = pow(self.g, private_key, self.p)
        return private_key, public_key

    def compute_shared_secret(self, private_key: int, remote_public_key: int) -> int:
        return pow(remote_public_key, private_key, self.p)


def self_check() -> None:
    dh = DiffieHellman(p=9973, g=5)
    alice_priv, alice_pub = dh.generate_keypair(123)
    bob_priv, bob_pub = dh.generate_keypair(456)
    alice_shared = dh.compute_shared_secret(alice_priv, bob_pub)
    bob_shared = dh.compute_shared_secret(bob_priv, alice_pub)
    assert alice_shared == bob_shared
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
