#!/usr/bin/env python3
"""Aho-Corasick trie automaton for linear-time multi-pattern string matching."""
from __future__ import annotations
from collections import deque


class AhoCorasick:
    def __init__(self, patterns: list[str]):
        self.goto: list[dict[str, int]] = [{}]
        self.fail: list[int] = [0]
        self.out: list[list[str]] = [[]]
        for pat in patterns:
            if not pat:
                continue
            state = 0
            for ch in pat:
                if ch not in self.goto[state]:
                    self.goto[state][ch] = len(self.goto)
                    self.goto.append({})
                    self.fail.append(0)
                    self.out.append([])
                state = self.goto[state][ch]
            self.out[state].append(pat)
        q: deque[int] = deque(self.goto[0].values())
        while q:
            r = q.popleft()
            for ch, s in self.goto[r].items():
                q.append(s)
                f = self.fail[r]
                while f and ch not in self.goto[f]:
                    f = self.fail[f]
                self.fail[s] = self.goto[f].get(ch, 0)
                self.out[s].extend(self.out[self.fail[s]])

    def search(self, text: str) -> list[tuple[int, str]]:
        state = 0
        hits: list[tuple[int, str]] = []
        for idx, ch in enumerate(text):
            while state and ch not in self.goto[state]:
                state = self.fail[state]
            state = self.goto[state].get(ch, 0)
            for pat in self.out[state]:
                hits.append((idx - len(pat) + 1, pat))
        return hits


def self_check() -> None:
    ac = AhoCorasick(["he", "she", "his", "hers"])
    assert ac.search("ushers") == [(1, "she"), (2, "he"), (2, "hers")]
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
