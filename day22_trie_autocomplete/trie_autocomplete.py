#!/usr/bin/env python3
"""Prefix tree (Trie) dictionary with fast autocompletion."""
from __future__ import annotations


class TrieNode:
    def __init__(self):
        self.children: dict[str, TrieNode] = {}
        self.is_word = False


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for ch in word:
            if ch not in curr.children:
                curr.children[ch] = TrieNode()
            curr = curr.children[ch]
        curr.is_word = True

    def autocomplete(self, prefix: str) -> list[str]:
        curr = self.root
        for ch in prefix:
            if ch not in curr.children:
                return []
            curr = curr.children[ch]

        results: list[str] = []

        def dfs(node: TrieNode, path: list[str]) -> None:
            if node.is_word:
                results.append("".join(path))
            for char, next_node in sorted(node.children.items()):
                path.append(char)
                dfs(next_node, path)
                path.pop()

        dfs(curr, list(prefix))
        return results


def self_check() -> None:
    trie = Trie()
    for w in ["python", "pyramid", "pytorch", "pyspark", "rust", "ruby"]:
        trie.insert(w)
    matches = trie.autocomplete("pyr")
    assert matches == ["pyramid"]
    py_matches = trie.autocomplete("py")
    assert py_matches == ["pyramid", "pyspark", "python", "pytorch"]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
