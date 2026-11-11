#!/usr/bin/env python3
"""Minimalist UStar TAR archive generator and extractor."""
from __future__ import annotations


def make_tar_header(name: str, size: int) -> bytes:
    name_bytes = name.encode("utf-8").ljust(100, b"\x00")
    mode = b"0000644\x00"
    uid = b"0001000\x00"
    gid = b"0001000\x00"
    size_oct = f"{size:011o}\x00".encode("ascii")
    mtime = b"00000000000\x00"
    chksum_placeholder = b"        "
    typeflag = b"0"
    magic = b"ustar\x0000"
    header_pre = (
        name_bytes + mode + uid + gid + size_oct + mtime + chksum_placeholder + typeflag
    ).ljust(257, b"\x00") + magic
    header_full = header_pre.ljust(512, b"\x00")
    chksum = sum(header_full)
    chksum_bytes = f"{chksum:06o}\x00 ".encode("ascii")
    return header_full[:148] + chksum_bytes + header_full[156:]


def create_archive(files: dict[str, bytes]) -> bytes:
    chunks = []
    for filename, content in files.items():
        header = make_tar_header(filename, len(content))
        chunks.append(header)
        chunks.append(content)
        pad = (512 - (len(content) % 512)) % 512
        if pad:
            chunks.append(b"\x00" * pad)
    chunks.append(b"\x00" * 1024)
    return b"".join(chunks)


def extract_archive(archive_bytes: bytes) -> dict[str, bytes]:
    files = {}
    pos = 0
    while pos + 512 <= len(archive_bytes):
        header = archive_bytes[pos : pos + 512]
        if header == b"\x00" * 512:
            break
        name = header[:100].rstrip(b"\x00").decode("utf-8")
        size_str = header[124:136].rstrip(b"\x00 ").decode("ascii")
        size = int(size_str, 8) if size_str else 0
        pos += 512
        content = archive_bytes[pos : pos + size]
        files[name] = content
        pad = (512 - (size % 512)) % 512
        pos += size + pad
    return files


def self_check() -> None:
    data = {"hello.txt": b"Hello World!\n", "test.py": b"print(42)\n"}
    tar = create_archive(data)
    extracted = extract_archive(tar)
    assert extracted == data
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
