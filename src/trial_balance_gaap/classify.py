from __future__ import annotations

import re
from typing import Optional

from .models import AccountCategory


def normalize_category(value: Optional[str]) -> Optional[AccountCategory]:
    if not value or not str(value).strip():
        return None
    key = str(value).strip().lower().replace(" ", "_").replace("-", "_")
    aliases = {
        "ca": AccountCategory.CURRENT_ASSET,
        "current_assets": AccountCategory.CURRENT_ASSET,
        "nca": AccountCategory.NONCURRENT_ASSET,
        "long_term_asset": AccountCategory.NONCURRENT_ASSET,
        "fixed_asset": AccountCategory.NONCURRENT_ASSET,
        "cl": AccountCategory.CURRENT_LIABILITY,
        "current_liabilities": AccountCategory.CURRENT_LIABILITY,
        "ncl": AccountCategory.NONCURRENT_LIABILITY,
        "long_term_liability": AccountCategory.NONCURRENT_LIABILITY,
        "ltl": AccountCategory.NONCURRENT_LIABILITY,
        "eq": AccountCategory.EQUITY,
        "capital": AccountCategory.EQUITY,
        "apic": AccountCategory.EQUITY,
        "treasury": AccountCategory.EQUITY,
        "re": AccountCategory.RETAINED_EARNINGS,
        "retained_earnings": AccountCategory.RETAINED_EARNINGS,
        "beginning_re": AccountCategory.BEGINNING_RETAINED_EARNINGS,
        "beginning_retained_earnings": AccountCategory.BEGINNING_RETAINED_EARNINGS,
        "opening_retained_earnings": AccountCategory.BEGINNING_RETAINED_EARNINGS,
        "sales": AccountCategory.REVENUE,
        "income": AccountCategory.REVENUE,
        "cogs": AccountCategory.COGS,
        "cost_of_sales": AccountCategory.COGS,
        "cost_of_goods_sold": AccountCategory.COGS,
        "opex": AccountCategory.OPERATING_EXPENSE,
        "sga": AccountCategory.OPERATING_EXPENSE,
        "ga": AccountCategory.OPERATING_EXPENSE,
        "rent": AccountCategory.OPERATING_EXPENSE,
        "wages": AccountCategory.OPERATING_EXPENSE,
        "salary": AccountCategory.OPERATING_EXPENSE,
        "depreciation": AccountCategory.OPERATING_EXPENSE,
        "amortization": AccountCategory.OPERATING_EXPENSE,
        "other_income": AccountCategory.OTHER_INCOME,
        "interest_income": AccountCategory.OTHER_INCOME,
        "other_expense": AccountCategory.OTHER_EXPENSE,
        "interest_expense": AccountCategory.OTHER_EXPENSE,
        "tax": AccountCategory.INCOME_TAX,
        "income_tax": AccountCategory.INCOME_TAX,
        "dividend": AccountCategory.DIVIDENDS,
        "dividends": AccountCategory.DIVIDENDS,
        "other": AccountCategory.OTHER,
    }
    if key in aliases:
        return aliases[key]
    try:
        return AccountCategory(key)
    except ValueError:
        return None


def infer_category(account_name: str) -> AccountCategory:
    """Best-effort keyword mapping; unknown accounts go to OTHER."""
    s = account_name.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    tokens = s.split()

    def has(*words: str) -> bool:
        return any(w in s for w in words)

    if has("beginning", "opening") and has("retained"):
        return AccountCategory.BEGINNING_RETAINED_EARNINGS
    if has("retained") and has("earning"):
        return AccountCategory.RETAINED_EARNINGS
    if has("dividend"):
        return AccountCategory.DIVIDENDS
    if has("income tax", "income taxes", "tax expense", "provision for tax"):
        return AccountCategory.INCOME_TAX
    if has("interest income", "investment income", "other income", "gain on"):
        return AccountCategory.OTHER_INCOME
    if has("interest expense", "other expense", "loss on"):
        return AccountCategory.OTHER_EXPENSE
    if has(
        "revenue",
        "sales",
        "fees earned",
        "service revenue",
        "subscription",
        "licensing",
    ):
        return AccountCategory.REVENUE
    if has("cost of goods", "cost of sales", "cogs"):
        return AccountCategory.COGS
    if has(
        "payable",
        "accrued",
        "deferred revenue",
        "unearned",
        "current portion",
        "short-term",
        "line of credit",
        "credit card",
    ) and not has("long", "bond", "note payable due"):
        return AccountCategory.CURRENT_LIABILITY
    if has("bond", "long-term debt", "mortgage", "lease liability", "note payable"):
        return AccountCategory.NONCURRENT_LIABILITY
    if has("cash", "receivable", "inventory", "prepaid", "deposit"):
        return AccountCategory.CURRENT_ASSET
    if has("ppe", "equipment", "furniture", "building", "land", "intangible", "goodwill", "long-term investment"):
        return AccountCategory.NONCURRENT_ASSET
    if has("common stock", "preferred stock", "paid-in", "apic", "additional paid", "treasury"):
        return AccountCategory.EQUITY
    if has("wage", "salary", "rent", "utilities", "insurance", "marketing", "professional", "legal", "office", "depreciation", "amortization", "bad debt", "research", "development", "r&d", "general", "admin"):
        return AccountCategory.OPERATING_EXPENSE

    # Single-token hints
    if "cash" in tokens or "bank" in tokens:
        return AccountCategory.CURRENT_ASSET
    if "receivable" in s:
        return AccountCategory.CURRENT_ASSET
    if "payable" in s:
        return AccountCategory.CURRENT_LIABILITY

    return AccountCategory.OTHER
