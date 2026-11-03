#!/usr/bin/env python3
"""Huffman coding lossless text compression and decompression."""
from __future__ import annotations
import heapq
from collections import Counter


class HuffmanNode:
    def __init__(self, char: str | None, freq: int):
        self.char = char
        self.freq = freq
        self.left: HuffmanNode | None = None
        self.right: HuffmanNode | None = None

    def __lt__(self, other: HuffmanNode) -> bool:
        return self.freq < other.freq


def build_tree(text: str) -> HuffmanNode | None:
    if not text:
        return None
    counts = Counter(text)
    heap = [HuffmanNode(char, freq) for char, freq in counts.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        n1 = heapq.heappop(heap)
        n2 = heapq.heappop(heap)
        merged = HuffmanNode(None, n1.freq + n2.freq)
        merged.left = n1
        merged.right = n2
        heapq.heappush(heap, merged)

    return heap[0]


def build_codes(node: HuffmanNode | None, prefix: str = "", codes: dict[str, str] | None = None) -> dict[str, str]:
    if codes is None:
        codes = {}
    if node:
        if node.char is not None:
            codes[node.char] = prefix or "0"
        build_codes(node.left, prefix + "0", codes)
        build_codes(node.right, prefix + "1", codes)
    return codes


def compress(text: str) -> tuple[str, HuffmanNode | None]:
    tree = build_tree(text)
    codes = build_codes(tree)
    encoded = "".join(codes[ch] for ch in text)
    return encoded, tree


def decompress(encoded: str, tree: HuffmanNode | None) -> str:
    if not tree or not encoded:
        return ""
    if tree.left is None and tree.right is None:
        return (tree.char or "") * len(encoded)
    chars = []
    curr = tree
    for bit in encoded:
        curr = curr.left if bit == "0" else curr.right
        if curr and curr.char is not None:
            chars.append(curr.char)
            curr = tree
    return "".join(chars)


def self_check() -> None:
    text = "abracadabra"
    bits, tree = compress(text)
    assert len(bits) < len(text) * 8
    assert decompress(bits, tree) == text
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
