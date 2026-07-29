#!/usr/bin/env python3
"""Generate a deterministic, relational fictional ERP database."""

from __future__ import annotations

import argparse
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "data" / "fictional_erp.sqlite"
DEFAULT_SCHEMA = ROOT / "schema" / "erp_schema.sql"

COUNTRIES = {
    "North America": [("United States", "USD"), ("Canada", "CAD")],
    "Europe": [("United Kingdom", "GBP"), ("Germany", "EUR"), ("France", "EUR")],
    "Asia Pacific": [("Australia", "AUD"), ("Japan", "JPY"), ("Singapore", "SGD")],
    "Latin America": [("Brazil", "BRL"), ("Mexico", "MXN")],
}
INDUSTRIES = [
    "Technology", "Manufacturing", "Healthcare", "Retail", "Financial Services",
    "Energy", "Transportation", "Education", "Media", "Professional Services",
]
VENDOR_CATEGORIES = [
    "Cloud Services", "Facilities", "Logistics", "Professional Services",
    "Hardware", "Marketing", "Office Supplies", "Insurance",
]
PREFIXES = [
    "Apex", "Blue", "Cedar", "Delta", "Evergreen", "Frontier", "Global", "Harbor",
    "Ironwood", "Juniper", "Keystone", "Lighthouse", "Meridian", "Northstar",
    "Orchard", "Pioneer", "Quantum", "Redwood", "Summit", "Vertex",
]
SUFFIXES = [
    "Systems", "Industries", "Group", "Partners", "Holdings", "Labs", "Works",
    "Solutions", "Enterprises", "Network",
]
FX_TO_USD = {
    "USD": 1.0, "CAD": 0.74, "GBP": 1.28, "EUR": 1.09, "AUD": 0.66,
    "JPY": 0.0067, "SGD": 0.75, "BRL": 0.20, "MXN": 0.059,
}


GL_ACCOUNTS = [
    ("1000", "Cash and Cash Equivalents", "ASSET", "DEBIT", None),
    ("1010", "Operating Bank Account", "ASSET", "DEBIT", 1),
    ("1020", "Payroll Bank Account", "ASSET", "DEBIT", 1),
    ("1100", "Accounts Receivable", "ASSET", "DEBIT", None),
    ("1110", "Allowance for Doubtful Accounts", "ASSET", "CREDIT", 4),
    ("1200", "Inventory", "ASSET", "DEBIT", None),
    ("1210", "Raw Materials Inventory", "ASSET", "DEBIT", 6),
    ("1220", "Finished Goods Inventory", "ASSET", "DEBIT", 6),
    ("1300", "Prepaid Expenses", "ASSET", "DEBIT", None),
    ("1400", "Property and Equipment", "ASSET", "DEBIT", None),
    ("1410", "Accumulated Depreciation", "ASSET", "CREDIT", 10),
    ("1500", "Intangible Assets", "ASSET", "DEBIT", None),
    ("1510", "Accumulated Amortization", "ASSET", "CREDIT", 12),
    ("2000", "Accounts Payable", "LIABILITY", "CREDIT", None),
    ("2100", "Accrued Expenses", "LIABILITY", "CREDIT", None),
    ("2110", "Accrued Payroll", "LIABILITY", "CREDIT", 15),
    ("2200", "Sales Tax Payable", "LIABILITY", "CREDIT", None),
    ("2300", "Deferred Revenue", "LIABILITY", "CREDIT", None),
    ("2400", "Short-Term Debt", "LIABILITY", "CREDIT", None),
    ("2500", "Long-Term Debt", "LIABILITY", "CREDIT", None),
    ("3000", "Common Stock", "EQUITY", "CREDIT", None),
    ("3100", "Additional Paid-In Capital", "EQUITY", "CREDIT", None),
    ("3200", "Retained Earnings", "EQUITY", "CREDIT", None),
    ("3300", "Current Year Earnings", "EQUITY", "CREDIT", None),
    ("4000", "Product Revenue", "REVENUE", "CREDIT", None),
    ("4010", "Software Revenue", "REVENUE", "CREDIT", 25),
    ("4020", "Hardware Revenue", "REVENUE", "CREDIT", 25),
    ("4030", "Services Revenue", "REVENUE", "CREDIT", 25),
    ("4040", "Support Revenue", "REVENUE", "CREDIT", 25),
    ("4050", "Other Revenue", "REVENUE", "CREDIT", None),
    ("5000", "Cost of Goods Sold", "EXPENSE", "DEBIT", None),
    ("5010", "Software Hosting Costs", "EXPENSE", "DEBIT", 31),
    ("5020", "Hardware Costs", "EXPENSE", "DEBIT", 31),
    ("5030", "Services Delivery Costs", "EXPENSE", "DEBIT", 31),
    ("5100", "Payroll Expense", "EXPENSE", "DEBIT", None),
    ("5110", "Benefits Expense", "EXPENSE", "DEBIT", 35),
    ("5200", "Rent and Facilities", "EXPENSE", "DEBIT", None),
    ("5210", "Utilities Expense", "EXPENSE", "DEBIT", 37),
    ("5300", "Sales and Marketing", "EXPENSE", "DEBIT", None),
    ("5310", "Advertising Expense", "EXPENSE", "DEBIT", 39),
    ("5400", "Research and Development", "EXPENSE", "DEBIT", None),
    ("5500", "General and Administrative", "EXPENSE", "DEBIT", None),
    ("5510", "Professional Fees", "EXPENSE", "DEBIT", 42),
    ("5520", "Insurance Expense", "EXPENSE", "DEBIT", 42),
    ("5530", "Office Supplies Expense", "EXPENSE", "DEBIT", 42),
    ("5600", "Depreciation Expense", "EXPENSE", "DEBIT", None),
    ("5700", "Interest Expense", "EXPENSE", "DEBIT", None),
    ("5800", "Foreign Exchange Gain or Loss", "EXPENSE", "DEBIT", None),
    ("5900", "Income Tax Expense", "EXPENSE", "DEBIT", None),
    ("5990", "Other Expense", "EXPENSE", "DEBIT", None),
]


def random_date(rng: random.Random, start: date, end: date) -> date:
    return start + timedelta(days=rng.randrange((end - start).days + 1))


def company_name(rng: random.Random, number: int) -> str:
    return f"{rng.choice(PREFIXES)} {rng.choice(SUFFIXES)} {number:04d}"


def insert_master_data(
    conn: sqlite3.Connection, rng: random.Random, customers: int, vendors: int
) -> None:
    customer_rows = []
    for customer_id in range(1, customers + 1):
        region = rng.choice(list(COUNTRIES))
        country, currency = rng.choice(COUNTRIES[region])
        customer_rows.append((
            customer_id, f"CUST-{customer_id:05d}", company_name(rng, customer_id),
            rng.choice(INDUSTRIES), region, country, currency,
            rng.choice([5_000_00, 10_000_00, 25_000_00, 50_000_00, 100_000_00]),
            rng.choice([15, 30, 30, 30, 45, 60]),
            rng.choices(["ACTIVE", "ON_HOLD", "INACTIVE"], [92, 5, 3])[0],
            random_date(rng, date(2015, 1, 1), date(2023, 12, 31)).isoformat(),
        ))
    conn.executemany(
        "INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", customer_rows
    )

    vendor_rows = []
    for vendor_id in range(1, vendors + 1):
        region = rng.choice(list(COUNTRIES))
        country, currency = rng.choice(COUNTRIES[region])
        vendor_rows.append((
            vendor_id, f"VEND-{vendor_id:05d}", company_name(rng, vendor_id + 5000),
            rng.choice(VENDOR_CATEGORIES), region, country, currency,
            rng.choice([15, 30, 30, 45, 60]),
            rng.choices(["ACTIVE", "ON_HOLD", "INACTIVE"], [94, 4, 2])[0],
            random_date(rng, date(2014, 1, 1), date(2023, 12, 31)).isoformat(),
        ))
    conn.executemany(
        "INSERT INTO vendors VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", vendor_rows
    )

    conn.executemany(
        """INSERT INTO gl_accounts
           (account_id, account_number, name, account_type, normal_balance,
            parent_account_id, is_active)
           VALUES (?, ?, ?, ?, ?, ?, 1)""",
        [
            (i, number, name, account_type, balance, parent)
            for i, (number, name, account_type, balance, parent)
            in enumerate(GL_ACCOUNTS, 1)
        ],
    )

    categories = [
        ("Software", 26, 32), ("Hardware", 27, 33),
        ("Services", 28, 34), ("Support", 29, 32),
    ]
    product_rows = []
    for product_id in range(1, 101):
        category, revenue_account, expense_account = categories[(product_id - 1) % 4]
        product_rows.append((
            product_id, f"SKU-{product_id:04d}", f"{category} Offering {product_id:03d}",
            category, rng.randint(25, 2500) * 100, revenue_account, expense_account,
        ))
    conn.executemany("INSERT INTO products VALUES (?, ?, ?, ?, ?, ?, ?)", product_rows)


def insert_invoices(
    conn: sqlite3.Connection,
    rng: random.Random,
    count: int,
    customer_count: int,
    vendor_count: int,
) -> dict[int, int]:
    customer_info = {
        row[0]: (row[1], row[2])
        for row in conn.execute("SELECT customer_id, currency, payment_terms_days FROM customers")
    }
    vendor_info = {
        row[0]: (row[1], row[2])
        for row in conn.execute("SELECT vendor_id, currency, payment_terms_days FROM vendors")
    }
    products = list(conn.execute(
        "SELECT product_id, name, unit_price_cents, revenue_account_id FROM products"
    ))
    expense_accounts = [32, 33, 34, 37, 38, 40, 41, 43, 44, 45, 50]
    expense_descriptions = [
        "Cloud infrastructure", "Computer equipment", "Contractor services",
        "Office lease", "Utilities", "Advertising campaign", "Research services",
        "Legal and audit fees", "Insurance premium", "Office supplies",
    ]
    remaining: dict[int, int] = {}
    line_id = 1

    for invoice_id in range(1, count + 1):
        is_sales = rng.random() < 0.72
        invoice_type = "SALES" if is_sales else "PURCHASE"
        invoice_date = random_date(rng, date(2023, 1, 1), date(2025, 12, 31))
        lines = []
        subtotal = 0
        for line_number in range(1, rng.randint(1, 4) + 1):
            quantity = rng.randint(1, 12)
            if is_sales:
                product_id, description, list_price, account_id = rng.choice(products)
                unit_price = max(100, int(list_price * rng.uniform(0.75, 1.15)))
            else:
                product_id = None
                description = rng.choice(expense_descriptions)
                unit_price = rng.randint(50, 5000) * 100
                account_id = rng.choice(expense_accounts)
            amount = quantity * unit_price
            subtotal += amount
            lines.append((
                line_id, invoice_id, line_number, product_id, description,
                quantity, unit_price, amount, account_id,
            ))
            line_id += 1

        if is_sales:
            party_id = rng.randint(1, customer_count)
            currency, terms = customer_info[party_id]
            customer_id, vendor_id = party_id, None
            prefix = "SI"
        else:
            party_id = rng.randint(1, vendor_count)
            currency, terms = vendor_info[party_id]
            customer_id, vendor_id = None, party_id
            prefix = "PI"
        tax_rate = rng.choices([0, 5, 8, 10, 20], [15, 10, 25, 35, 15])[0]
        tax = subtotal * tax_rate // 100
        total = subtotal + tax
        exchange_rate = FX_TO_USD[currency] * rng.uniform(0.97, 1.03)
        functional_total = round(total * exchange_rate)
        due_date = invoice_date + timedelta(days=terms)
        conn.execute(
            """INSERT INTO invoices
               (invoice_id, invoice_number, invoice_type, customer_id, vendor_id,
                invoice_date, due_date, status, currency, subtotal_cents, tax_cents,
                total_cents, exchange_rate_to_usd, functional_total_cents, description)
               VALUES (?, ?, ?, ?, ?, ?, ?, 'OPEN', ?, ?, ?, ?, ?, ?, ?)""",
            (
                invoice_id, f"{prefix}-{invoice_id:07d}", invoice_type,
                customer_id, vendor_id, invoice_date.isoformat(), due_date.isoformat(),
                currency, subtotal, tax, total, exchange_rate, functional_total,
                "Customer billing" if is_sales else "Vendor procurement",
            ),
        )
        conn.executemany("INSERT INTO invoice_lines VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", lines)
        remaining[invoice_id] = total
    return remaining


def insert_payments(
    conn: sqlite3.Connection,
    rng: random.Random,
    count: int,
    remaining: dict[int, int],
) -> None:
    invoices = {
        row[0]: row[1:]
        for row in conn.execute(
            """SELECT invoice_id, invoice_type, customer_id, vendor_id,
                      invoice_date, currency, total_cents, exchange_rate_to_usd
               FROM invoices"""
        )
    }
    invoice_ids = list(invoices)
    for payment_id in range(1, count + 1):
        eligible = [i for i in invoice_ids if remaining[i] > 0]
        invoice_id = rng.choice(eligible or invoice_ids)
        (
            invoice_type, customer_id, vendor_id, invoice_date_text, currency, total,
            invoice_exchange_rate,
        ) = invoices[invoice_id]
        invoice_date = date.fromisoformat(invoice_date_text)
        status = rng.choices(["CLEARED", "PENDING", "FAILED"], [90, 7, 3])[0]
        available = remaining[invoice_id] if status == "CLEARED" else total
        fraction = rng.uniform(0.35, 1.0)
        amount = max(1, min(available, int(available * fraction)))
        if rng.random() < 0.45:
            amount = available
        payment_date = min(
            date(2026, 1, 31),
            invoice_date + timedelta(days=rng.randint(1, 100)),
        )
        payment_type = "RECEIPT" if invoice_type == "SALES" else "DISBURSEMENT"
        exchange_rate = invoice_exchange_rate * rng.uniform(0.98, 1.02)
        functional_amount = max(1, round(amount * exchange_rate))
        conn.execute(
            """INSERT INTO payments
               (payment_id, payment_number, payment_type, customer_id, vendor_id,
                payment_date, amount_cents, currency, exchange_rate_to_usd,
                functional_amount_cents, method, status, reference)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                payment_id, f"PAY-{payment_id:07d}", payment_type, customer_id, vendor_id,
                payment_date.isoformat(), amount, currency, exchange_rate, functional_amount,
                rng.choices(["ACH", "WIRE", "CHECK", "CARD"], [50, 20, 20, 10])[0],
                status, f"BANKREF-{rng.randint(10000000, 99999999)}",
            ),
        )
        conn.execute(
            "INSERT INTO payment_allocations VALUES (?, ?, ?)",
            (payment_id, invoice_id, amount),
        )
        if status == "CLEARED":
            remaining[invoice_id] -= amount

    conn.execute(
        """UPDATE invoices
           SET status = CASE
               WHEN (SELECT balance_cents FROM v_invoice_balances b
                     WHERE b.invoice_id = invoices.invoice_id) = 0 THEN 'PAID'
               WHEN (SELECT paid_cents FROM v_invoice_balances b
                     WHERE b.invoice_id = invoices.invoice_id) > 0 THEN 'PARTIAL'
               ELSE 'OPEN'
           END"""
    )


def insert_journals(conn: sqlite3.Connection, rng: random.Random, count: int) -> None:
    invoices = list(conn.execute(
        "SELECT invoice_id, invoice_type, invoice_date, subtotal_cents, tax_cents, "
        "total_cents, functional_total_cents "
        "FROM invoices"
    ))
    payments = list(conn.execute(
        "SELECT payment_id, payment_type, payment_date, functional_amount_cents FROM payments"
    ))
    line_id = 1
    for entry_id in range(1, count + 1):
        roll = rng.random()
        source_invoice = source_payment = None
        lines: list[tuple[int, int, int, int, int, int, str]] = []
        if roll < 0.58:
            (
                invoice_id, invoice_type, entry_date, subtotal, tax, total,
                functional_total,
            ) = rng.choice(invoices)
            functional_subtotal = round(functional_total * subtotal / total)
            functional_tax = functional_total - functional_subtotal
            source_invoice = invoice_id
            if invoice_type == "SALES":
                source, description = "AR", f"Post sales invoice SI-{invoice_id:07d}"
                lines.append((line_id, entry_id, 1, 4, functional_total, 0, "Accounts receivable"))
                lines.append((line_id + 1, entry_id, 2, rng.choice([26, 27, 28, 29]), 0, functional_subtotal, "Revenue"))
                if functional_tax:
                    lines.append((line_id + 2, entry_id, 3, 17, 0, functional_tax, "Sales tax"))
            else:
                source, description = "AP", f"Post purchase invoice PI-{invoice_id:07d}"
                lines.append((line_id, entry_id, 1, rng.choice([32, 33, 34, 37, 40, 43, 44, 45]), functional_subtotal, 0, "Expense"))
                if functional_tax:
                    lines.append((line_id + 1, entry_id, 2, 9, functional_tax, 0, "Recoverable tax"))
                lines.append((line_id + len(lines), entry_id, len(lines) + 1, 14, 0, functional_total, "Accounts payable"))
        elif roll < 0.84:
            payment_id, payment_type, entry_date, amount = rng.choice(payments)
            source_payment = payment_id
            source, description = "CASH", f"Post payment PAY-{payment_id:07d}"
            if payment_type == "RECEIPT":
                lines = [
                    (line_id, entry_id, 1, 2, amount, 0, "Cash receipt"),
                    (line_id + 1, entry_id, 2, 4, 0, amount, "Reduce receivable"),
                ]
            else:
                lines = [
                    (line_id, entry_id, 1, 14, amount, 0, "Reduce payable"),
                    (line_id + 1, entry_id, 2, 2, 0, amount, "Cash disbursement"),
                ]
        else:
            source = rng.choice(["MANUAL", "PAYROLL"])
            entry_date = random_date(rng, date(2023, 1, 1), date(2025, 12, 31)).isoformat()
            amount = rng.randint(100, 100_000) * 100
            if source == "PAYROLL":
                debit_account, credit_account = 35, 16
                description = "Monthly payroll accrual"
            else:
                debit_account, credit_account = rng.choice([
                    (46, 11), (47, 20), (43, 15), (49, 17), (50, 15)
                ])
                description = "Period-end adjusting entry"
            lines = [
                (line_id, entry_id, 1, debit_account, amount, 0, description),
                (line_id + 1, entry_id, 2, credit_account, 0, amount, description),
            ]

        status = rng.choices(["POSTED", "DRAFT", "REVERSED"], [94, 4, 2])[0]
        conn.execute(
            """INSERT INTO journal_entries
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                entry_id, f"JE-{entry_id:07d}", entry_date, source,
                source_invoice, source_payment, description, status,
                rng.choice(["alex.chen", "maria.garcia", "sam.taylor", "erp.batch"]),
            ),
        )
        conn.executemany("INSERT INTO journal_lines VALUES (?, ?, ?, ?, ?, ?, ?)", lines)
        line_id += len(lines)


def generate(args: argparse.Namespace) -> None:
    if min(args.customers, args.vendors, args.invoices, args.payments, args.journals) < 1:
        raise ValueError("All requested row counts must be positive")
    if args.accounts != len(GL_ACCOUNTS):
        raise ValueError(f"This chart of accounts contains exactly {len(GL_ACCOUNTS)} accounts")

    rng = random.Random(args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(args.output)
    try:
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        conn.executescript(args.schema.read_text(encoding="utf-8"))
        with conn:
            insert_master_data(conn, rng, args.customers, args.vendors)
            remaining = insert_invoices(
                conn, rng, args.invoices, args.customers, args.vendors
            )
            insert_payments(conn, rng, args.payments, remaining)
            insert_journals(conn, rng, args.journals)
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        conn.execute("ANALYZE")
    finally:
        conn.close()
    print(f"Generated {args.output}")
    print(
        f"customers={args.customers:,}, vendors={args.vendors:,}, "
        f"accounts={args.accounts:,}, invoices={args.invoices:,}, "
        f"payments={args.payments:,}, journal_entries={args.journals:,}"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_DB)
    parser.add_argument("--schema", type=Path, default=DEFAULT_SCHEMA)
    parser.add_argument("--seed", type=int, default=20260729)
    parser.add_argument("--customers", type=int, default=1_000)
    parser.add_argument("--vendors", type=int, default=500)
    parser.add_argument("--accounts", type=int, default=50)
    parser.add_argument("--invoices", type=int, default=20_000)
    parser.add_argument("--payments", type=int, default=10_000)
    parser.add_argument("--journals", type=int, default=5_000)
    return parser.parse_args()


if __name__ == "__main__":
    generate(parse_args())
