"""Load and summarise transaction records from CSV files."""

from __future__ import annotations

import csv
from collections import defaultdict
from typing import TypedDict


class Transaction(TypedDict):
    id: int
    amt: float
    cat: str


def load(path: str) -> list[Transaction]:
    """Read a CSV file and return a list of transaction dicts.

    The CSV is expected to have columns ``id, amt, cat`` with an optional
    header row whose first cell is literally ``"id"``.  Blank rows are
    silently skipped.

    Args:
        path: Filesystem path to the CSV file.

    Returns:
        A list of :class:`Transaction` dicts, one per data row.
    """
    transactions: list[Transaction] = []
    with open(path, newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row or row[0] == "id":
                continue
            transactions.append(
                Transaction(id=int(row[0]), amt=float(row[1]), cat=row[2])
            )
    return transactions


def summarize(rows: list[Transaction]) -> dict[str, float]:
    """Aggregate transaction amounts by category.

    Args:
        rows: Transaction dicts as returned by :func:`load`.

    Returns:
        A mapping of category name to the total amount for that category.
    """
    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        totals[row["cat"]] += row["amt"]
    return dict(totals)
