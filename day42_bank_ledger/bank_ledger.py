#!/usr/bin/env python3
"""Double-entry accounting transaction ledger with zero-sum validation."""
from __future__ import annotations


class AccountLedger:
    def __init__(self):
        self.accounts: dict[str, int] = {}
        self.journal: list[dict[str, int]] = []

    def get_balance(self, account: str) -> int:
        return self.accounts.get(account, 0)

    def record_entry(self, entry: dict[str, int]) -> bool:
        if sum(entry.values()) != 0:
            raise ValueError("Accounting equation violated: debits and credits must sum to zero")
        for acct, amount in entry.items():
            if self.get_balance(acct) + amount < 0 and not acct.startswith("equity:"):
                return False
        for acct, amount in entry.items():
            self.accounts[acct] = self.get_balance(acct) + amount
        self.journal.append(entry)
        return True


def self_check() -> None:
    ledger = AccountLedger()
    assert ledger.record_entry({"assets:cash": 1000, "equity:capital": -1000})
    assert ledger.record_entry({"assets:savings": 400, "assets:cash": -400})
    assert not ledger.record_entry({"assets:savings": 700, "assets:cash": -700})
    assert ledger.get_balance("assets:cash") == 600
    assert ledger.get_balance("assets:savings") == 400
    print("Self-check passed.")


if __name__ == "__main__":
    self_check()
