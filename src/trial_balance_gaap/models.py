from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Optional


class AccountCategory(str, Enum):
    """GAAP-oriented grouping for trial balance lines."""

    CURRENT_ASSET = "current_asset"
    NONCURRENT_ASSET = "noncurrent_asset"
    CURRENT_LIABILITY = "current_liability"
    NONCURRENT_LIABILITY = "noncurrent_liability"
    EQUITY = "equity"
    RETAINED_EARNINGS = "retained_earnings"
    BEGINNING_RETAINED_EARNINGS = "beginning_retained_earnings"
    REVENUE = "revenue"
    COGS = "cogs"
    OPERATING_EXPENSE = "operating_expense"
    OTHER_INCOME = "other_income"
    OTHER_EXPENSE = "other_expense"
    INCOME_TAX = "income_tax"
    DIVIDENDS = "dividends"
    OTHER = "other"


DEBIT_NORMAL: frozenset[AccountCategory] = frozenset(
    {
        AccountCategory.CURRENT_ASSET,
        AccountCategory.NONCURRENT_ASSET,
        AccountCategory.COGS,
        AccountCategory.OPERATING_EXPENSE,
        AccountCategory.OTHER_EXPENSE,
        AccountCategory.INCOME_TAX,
        AccountCategory.DIVIDENDS,
        AccountCategory.OTHER,
    }
)


@dataclass(frozen=True)
class TrialBalanceLine:
    account: str
    category: AccountCategory
    debit: float
    credit: float

    @property
    def signed_amount(self) -> float:
        """Positive increases the natural side of the account (GAAP TB convention)."""
        raw = self.debit - self.credit
        if self.category in DEBIT_NORMAL:
            return raw
        return -raw


@dataclass
class ParsedTrialBalance:
    lines: list[TrialBalanceLine]

    def by_category(self) -> dict[AccountCategory, float]:
        out: dict[AccountCategory, float] = {}
        for line in self.lines:
            out[line.category] = out.get(line.category, 0.0) + line.signed_amount
        return out
