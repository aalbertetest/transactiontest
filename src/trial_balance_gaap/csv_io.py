from __future__ import annotations

import csv
import io
from pathlib import Path
from typing import TextIO

from .classify import infer_category, normalize_category
from .models import AccountCategory, TrialBalanceLine


def _float_cell(row: dict[str, str], *keys: str) -> float:
    for k in keys:
        if k in row and row[k] is not None and str(row[k]).strip() != "":
            return float(str(row[k]).replace(",", "").strip())
    return 0.0


def _norm_header(h: str) -> str:
    return h.strip().lower().replace(" ", "_")


def parse_trial_balance_csv(source: TextIO | Path | str) -> list[TrialBalanceLine]:
    if isinstance(source, Path):
        text = source.read_text(encoding="utf-8")
        stream: TextIO = io.StringIO(text)
    elif isinstance(source, str):
        stream = io.StringIO(source)
    else:
        stream = source

    reader = csv.DictReader(stream)
    if not reader.fieldnames:
        raise ValueError("CSV has no header row")

    field_map = {_norm_header(f): f for f in reader.fieldnames}

    def col(*names: str) -> str | None:
        for n in names:
            n2 = _norm_header(n)
            if n2 in field_map:
                return field_map[n2]
        return None

    acc_col = col("account", "account_name", "name", "description")
    if not acc_col:
        raise ValueError("CSV must include an account column: account, account_name, name, or description")

    debit_col = col("debit", "dr", "debits")
    credit_col = col("credit", "cr", "credits")
    amount_col = col("amount", "balance", "net")
    cat_col = col("category", "class", "type", "gaap_category")

    lines: list[TrialBalanceLine] = []
    for raw in reader:
        account = (raw.get(acc_col) or "").strip()
        if not account:
            continue

        debit = credit = 0.0
        if debit_col and credit_col:
            debit = _float_cell(raw, debit_col)
            credit = _float_cell(raw, credit_col)
        elif amount_col:
            amt = _float_cell(raw, amount_col)
            if amt >= 0:
                debit, credit = amt, 0.0
            else:
                debit, credit = 0.0, -amt
        else:
            raise ValueError("CSV needs debit+credit columns or a single amount column")

        cat: AccountCategory | None = None
        if cat_col:
            cat = normalize_category(raw.get(cat_col))
        if cat is None:
            cat = infer_category(account)

        lines.append(TrialBalanceLine(account=account, category=cat, debit=debit, credit=credit))

    if not lines:
        raise ValueError("No trial balance rows found")
    return lines
