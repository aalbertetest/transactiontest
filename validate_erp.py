#!/usr/bin/env python3
"""Validate ERP row counts, relationships, and accounting invariants."""

from __future__ import annotations

import argparse
import sqlite3
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "data" / "fictional_erp.sqlite"
EXPECTED = {
    "customers": 1_000,
    "vendors": 500,
    "gl_accounts": 50,
    "invoices": 20_000,
    "payments": 10_000,
    "journal_entries": 5_000,
}


CHECKS = {
    "foreign key violations": "SELECT COUNT(*) FROM pragma_foreign_key_check",
    "invoice line totals differ from subtotal": """
        SELECT COUNT(*) FROM invoices i
        WHERE i.subtotal_cents <> (
            SELECT COALESCE(SUM(line_amount_cents), 0)
            FROM invoice_lines il WHERE il.invoice_id = i.invoice_id
        )
    """,
    "invoice parties do not match type": """
        SELECT COUNT(*) FROM invoices
        WHERE (invoice_type = 'SALES' AND (customer_id IS NULL OR vendor_id IS NOT NULL))
           OR (invoice_type = 'PURCHASE' AND (vendor_id IS NULL OR customer_id IS NOT NULL))
    """,
    "payment parties do not match type": """
        SELECT COUNT(*) FROM payments
        WHERE (payment_type = 'RECEIPT' AND (customer_id IS NULL OR vendor_id IS NOT NULL))
           OR (payment_type = 'DISBURSEMENT' AND (vendor_id IS NULL OR customer_id IS NOT NULL))
    """,
    "payment allocations do not match party or transaction type": """
        SELECT COUNT(*)
        FROM payment_allocations pa
        JOIN payments p ON p.payment_id = pa.payment_id
        JOIN invoices i ON i.invoice_id = pa.invoice_id
        WHERE (p.payment_type = 'RECEIPT'
               AND (i.invoice_type <> 'SALES' OR p.customer_id <> i.customer_id))
           OR (p.payment_type = 'DISBURSEMENT'
               AND (i.invoice_type <> 'PURCHASE' OR p.vendor_id <> i.vendor_id))
           OR p.currency <> i.currency
    """,
    "payments not fully allocated": """
        SELECT COUNT(*) FROM payments p
        WHERE p.amount_cents <> (
            SELECT COALESCE(SUM(allocated_cents), 0)
            FROM payment_allocations pa WHERE pa.payment_id = p.payment_id
        )
    """,
    "cleared payments over-allocate invoices": """
        SELECT COUNT(*) FROM v_invoice_balances WHERE balance_cents < 0
    """,
    "invoice status disagrees with cleared balance": """
        SELECT COUNT(*) FROM v_invoice_balances
        WHERE (balance_cents = 0 AND status <> 'PAID')
           OR (paid_cents > 0 AND balance_cents > 0 AND status <> 'PARTIAL')
           OR (paid_cents = 0 AND status <> 'OPEN')
    """,
    "journal entries have fewer than two lines": """
        SELECT COUNT(*) FROM journal_entries je
        WHERE (SELECT COUNT(*) FROM journal_lines jl
               WHERE jl.journal_entry_id = je.journal_entry_id) < 2
    """,
    "unbalanced journal entries": """
        SELECT COUNT(*) FROM (
            SELECT journal_entry_id
            FROM journal_lines
            GROUP BY journal_entry_id
            HAVING SUM(debit_cents) <> SUM(credit_cents)
        )
    """,
    "nonpositive functional currency amounts": """
        SELECT
          (SELECT COUNT(*) FROM invoices WHERE functional_total_cents <= 0)
          + (SELECT COUNT(*) FROM payments WHERE functional_amount_cents <= 0)
    """,
}


def validate(db_path: Path, expected: dict[str, int]) -> bool:
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    failures: list[str] = []
    try:
        print("Row counts")
        for table, expected_count in expected.items():
            actual = conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]
            result = "PASS" if actual == expected_count else "FAIL"
            print(f"  {result:4} {table:20} {actual:>8,} (expected {expected_count:,})")
            if actual != expected_count:
                failures.append(f"{table}: expected {expected_count}, found {actual}")

        print("\nIntegrity checks")
        for name, sql in CHECKS.items():
            violations = conn.execute(sql).fetchone()[0]
            result = "PASS" if violations == 0 else "FAIL"
            print(f"  {result:4} {name}: {violations:,}")
            if violations:
                failures.append(f"{name}: {violations} violation(s)")
    finally:
        conn.close()

    if failures:
        print("\nValidation failed:", file=sys.stderr)
        for failure in failures:
            print(f"  - {failure}", file=sys.stderr)
        return False
    print("\nAll validations passed.")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    for table, count in EXPECTED.items():
        parser.add_argument(
            f"--{table.replace('_', '-')}", type=int, default=count,
            help=f"Expected {table} count (default: {count})",
        )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    expected = {
        table: getattr(args, table)
        for table in EXPECTED
    }
    raise SystemExit(0 if validate(args.database, expected) else 1)
