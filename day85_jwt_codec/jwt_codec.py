#!/usr/bin/env python3
"""RFC 7519 JSON Web Token (JWT) Signer and Verifier using HMAC-SHA256."""
from __future__ import annotations
import base64
import hashlib
import hmac
import json
import time


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("utf-8").rstrip("=")


def _b64url_decode(s: str) -> bytes:
    rem = len(s) % 4
    if rem:
        s += "=" * (4 - rem)
    return base64.urlsafe_b64decode(s.encode("utf-8"))


def encode_jwt(payload: dict, secret: str) -> str:
    header = {"alg": "HS256", "typ": "JWT"}
    h_bytes = json.dumps(header, separators=(",", ":")).encode("utf-8")
    p_bytes = json.dumps(payload, separators=(",", ":")).encode("utf-8")
    h_b64 = _b64url_encode(h_bytes)
    p_b64 = _b64url_encode(p_bytes)
    signing_input = f"{h_b64}.{p_b64}".encode("utf-8")
    sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    return f"{h_b64}.{p_b64}.{_b64url_encode(sig)}"


def decode_jwt(token: str, secret: str) -> dict:
    parts = token.split(".")
    if len(parts) != 3:
        raise ValueError("Invalid JWT format")
    h_b64, p_b64, s_b64 = parts
    signing_input = f"{h_b64}.{p_b64}".encode("utf-8")
    expected_sig = hmac.new(secret.encode("utf-8"), signing_input, hashlib.sha256).digest()
    actual_sig = _b64url_decode(s_b64)
    if not hmac.compare_digest(expected_sig, actual_sig):
        raise ValueError("Invalid JWT signature")
    payload = json.loads(_b64url_decode(p_b64).decode("utf-8"))
    if "exp" in payload and payload["exp"] < time.time():
        raise ValueError("Token expired")
    return payload


def self_check() -> None:
    secret = "super-secret-key-123"
    claims = {"sub": "user_42", "role": "admin", "exp": int(time.time()) + 3600}
    token = encode_jwt(claims, secret)
    assert token.count(".") == 2
    decoded = decode_jwt(token, secret)
    assert decoded["sub"] == "user_42"
    assert decoded["role"] == "admin"
    try:
        decode_jwt(token, "wrong-key")
        assert False, "Should fail with wrong key"
    except ValueError:
        pass
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
