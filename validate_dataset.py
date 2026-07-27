#!/usr/bin/env python3
"""Check a generated subscription transaction CSV and print a profile of it.

Hard invariants (a failure exits non-zero):
  * expected header, no empty fields
  * invoice_date strictly before renewal_date
  * a contract keeps one customer, product, currency and region for its life
  * a customer keeps one region and currency
  * amounts are positive and respect the currency's minor units
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from datetime import date

EXPECTED_HEADER = [
    "customer_id",
    "contract_id",
    "invoice_date",
    "renewal_date",
    "product",
    "amount",
    "currency",
    "region",
]

# Indicative rates, only used to compare amounts across currencies in the profile.
USD_RATES = {
    "USD": 1.00,
    "CAD": 1.36,
    "EUR": 0.93,
    "GBP": 0.79,
    "CHF": 0.89,
    "SEK": 10.60,
    "ZAR": 18.40,
    "AED": 3.67,
    "JPY": 152.0,
    "INR": 83.50,
    "AUD": 1.52,
    "NZD": 1.65,
    "SGD": 1.35,
    "BRL": 5.40,
    "MXN": 17.50,
}

ZERO_DECIMAL_CURRENCIES = {"JPY"}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="data/subscription_transactions.csv")
    args = parser.parse_args(argv)

    with open(args.path, newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_HEADER:
            print(f"FAIL unexpected header: {reader.fieldnames}")
            return 1
        rows = list(reader)

    failures = Counter()
    by_contract = defaultdict(set)
    by_customer = defaultdict(set)
    usd_amounts = []
    invoice_dates = []
    per_contract_rows = Counter()

    for row in rows:
        if any(value == "" or value is None for value in row.values()):
            failures["empty_field"] += 1
            continue

        invoice_date = date.fromisoformat(row["invoice_date"])
        renewal_date = date.fromisoformat(row["renewal_date"])
        if invoice_date >= renewal_date:
            failures["renewal_not_after_invoice"] += 1
        invoice_dates.append(invoice_date)

        currency = row["currency"]
        if currency not in USD_RATES:
            failures["unknown_currency"] += 1
            continue

        amount = float(row["amount"])
        if amount <= 0:
            failures["non_positive_amount"] += 1
        if currency in ZERO_DECIMAL_CURRENCIES and not amount.is_integer():
            failures["minor_units"] += 1
        elif "." in row["amount"] and len(row["amount"].split(".")[1]) > 2:
            failures["minor_units"] += 1

        by_contract[row["contract_id"]].add(
            (row["customer_id"], row["product"], currency, row["region"])
        )
        by_customer[row["customer_id"]].add((row["region"], currency))
        per_contract_rows[row["contract_id"]] += 1
        usd_amounts.append(amount / USD_RATES[currency])

    for contract_id, attributes in by_contract.items():
        if len(attributes) > 1:
            failures["contract_attributes_change"] += 1
    for customer_id, attributes in by_customer.items():
        if len(attributes) > 1:
            failures["customer_attributes_change"] += 1

    print(f"file            : {args.path}")
    print(f"rows            : {len(rows):,}")
    print(f"customers       : {len(by_customer):,}")
    print(f"contracts       : {len(by_contract):,}")
    print(f"invoice dates   : {min(invoice_dates)} -> {max(invoice_dates)}")

    usd_amounts.sort()

    def percentile(fraction: float) -> float:
        return usd_amounts[min(len(usd_amounts) - 1, int(fraction * len(usd_amounts)))]

    print(
        "amount (USD-equiv) p25/p50/p75/p95/p99/max: "
        + " / ".join(
            f"{value:,.0f}"
            for value in (
                percentile(0.25),
                percentile(0.50),
                percentile(0.75),
                percentile(0.95),
                percentile(0.99),
                usd_amounts[-1],
            )
        )
    )
    print(f"billed total    : {sum(usd_amounts) / 1e6:,.1f}M USD-equiv")

    invoices_per_contract = sorted(per_contract_rows.values())
    print(
        "invoices/contract min/median/max: "
        f"{invoices_per_contract[0]} / "
        f"{invoices_per_contract[len(invoices_per_contract) // 2]} / "
        f"{invoices_per_contract[-1]}"
    )

    per_year = Counter(row["invoice_date"][:4] for row in rows)
    print("rows per year   : " + ", ".join(f"{y} {c:,}" for y, c in sorted(per_year.items())))

    for label, field in (("regions", "region"), ("currencies", "currency"), ("products", "product")):
        counts = Counter(row[field] for row in rows).most_common()
        print(
            f"{label:<16}: "
            + ", ".join(f"{name} {count / len(rows):.1%}" for name, count in counts)
        )

    if failures:
        print("\nFAILED checks: " + ", ".join(f"{k}={v}" for k, v in failures.items()))
        return 1
    print("\nall invariant checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
