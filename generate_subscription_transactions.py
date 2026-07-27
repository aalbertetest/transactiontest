#!/usr/bin/env python3
"""Generate a synthetic but realistic subscription billing export.

The generator models customers, the contracts they sign and the invoices those
contracts produce, so the resulting rows hang together the way a real billing
export does: a contract keeps its product and currency for life, invoices repeat
on the contract's billing cadence, renewal dates line up with term boundaries,
and amounts derive from a per-currency price book.

Output columns: customer_id, contract_id, invoice_date, renewal_date, product,
amount, currency, region.
"""

from __future__ import annotations

import argparse
import calendar
import csv
import random
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import date, timedelta
from decimal import Decimal, ROUND_HALF_UP

DATASET_START = date(2019, 1, 1)
DATASET_END = date(2026, 6, 30)

# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------

REGIONS = {
    "North America": 0.44,
    "EMEA": 0.31,
    "APAC": 0.18,
    "LATAM": 0.07,
}

# List prices are maintained in USD and published in local currency, so each
# region/currency combination carries its own multiplier and rounding rules.
REGION_CURRENCIES = {
    "North America": {"USD": 0.86, "CAD": 0.14},
    "EMEA": {"EUR": 0.52, "GBP": 0.24, "CHF": 0.07, "SEK": 0.07, "ZAR": 0.05, "AED": 0.05},
    "APAC": {"JPY": 0.28, "INR": 0.22, "AUD": 0.22, "SGD": 0.18, "NZD": 0.10},
    "LATAM": {"BRL": 0.46, "MXN": 0.34, "USD": 0.20},
}

REGION_PRICE_INDEX = {
    "North America": 1.00,
    "EMEA": 1.03,
    "APAC": 0.92,
    "LATAM": 0.84,
}


@dataclass(frozen=True)
class Currency:
    code: str
    per_usd: float
    decimals: int
    price_step: float  # list prices are published on this grid


CURRENCIES = {
    c.code: c
    for c in [
        Currency("USD", 1.00, 2, 1),
        Currency("CAD", 1.36, 2, 1),
        Currency("EUR", 0.93, 2, 1),
        Currency("GBP", 0.79, 2, 1),
        Currency("CHF", 0.89, 2, 1),
        Currency("SEK", 10.60, 2, 10),
        Currency("ZAR", 18.40, 2, 10),
        Currency("AED", 3.67, 2, 1),
        Currency("JPY", 152.0, 0, 100),
        Currency("INR", 83.50, 2, 50),
        Currency("AUD", 1.52, 2, 1),
        Currency("NZD", 1.65, 2, 1),
        Currency("SGD", 1.35, 2, 1),
        Currency("BRL", 5.40, 2, 5),
        Currency("MXN", 17.50, 2, 10),
    ]
}

SEGMENTS = {
    "SMB": 0.62,
    "Mid-Market": 0.28,
    "Enterprise": 0.10,
}

SEGMENT_PROFILE = {
    # seats: range for the primary platform subscription
    # contracts: how many separate contracts the account carries
    # discount: negotiated discount off list
    # term_churn: chance the account walks away at a term boundary
    "SMB": {
        "seats": (3, 45),
        "contracts": (1, 2),
        "discount": (0.00, 0.08),
        "term_churn": 0.20,
        "monthly_churn": 0.035,
    },
    "Mid-Market": {
        "seats": (30, 350),
        "contracts": (1, 4),
        "discount": (0.04, 0.20),
        "term_churn": 0.11,
        "monthly_churn": 0.020,
    },
    "Enterprise": {
        "seats": (200, 4200),
        "contracts": (2, 6),
        "discount": (0.14, 0.38),
        "term_churn": 0.055,
        "monthly_churn": 0.012,
    },
}


@dataclass(frozen=True)
class Product:
    name: str
    per_seat: bool
    # Monthly USD list price: per seat, or flat per segment.
    price: float | dict
    segments: tuple
    weight: float
    seat_ratio: float = 1.0  # add-ons are usually bought for a subset of seats


PLATFORM_PRODUCTS = [
    Product("Core Platform - Starter", True, 19.0, ("SMB",), 1.0),
    Product("Core Platform - Professional", True, 49.0, ("SMB", "Mid-Market"), 1.0),
    Product("Core Platform - Enterprise", True, 89.0, ("Mid-Market", "Enterprise"), 1.0),
]

ADDON_PRODUCTS = [
    Product("Advanced Analytics", True, 22.0, ("SMB", "Mid-Market", "Enterprise"), 1.00, 0.55),
    Product("Workflow Automation", True, 15.0, ("SMB", "Mid-Market", "Enterprise"), 0.85, 0.70),
    Product("Mobile Field App", True, 12.0, ("SMB", "Mid-Market", "Enterprise"), 0.55, 0.35),
    Product(
        "Premium Support",
        False,
        {"SMB": 250.0, "Mid-Market": 900.0, "Enterprise": 3500.0},
        ("SMB", "Mid-Market", "Enterprise"),
        0.95,
    ),
    Product(
        "API Gateway",
        False,
        {"SMB": 200.0, "Mid-Market": 650.0, "Enterprise": 1800.0},
        ("SMB", "Mid-Market", "Enterprise"),
        0.70,
    ),
    Product(
        "Data Warehouse Sync",
        False,
        {"SMB": 150.0, "Mid-Market": 500.0, "Enterprise": 1400.0},
        ("SMB", "Mid-Market", "Enterprise"),
        0.60,
    ),
    Product(
        "Single Sign-On",
        False,
        {"SMB": 90.0, "Mid-Market": 250.0, "Enterprise": 600.0},
        ("SMB", "Mid-Market", "Enterprise"),
        0.50,
    ),
    Product(
        "Sandbox Environment",
        False,
        {"SMB": 80.0, "Mid-Market": 180.0, "Enterprise": 450.0},
        ("SMB", "Mid-Market", "Enterprise"),
        0.40,
    ),
    Product(
        "Security & Compliance Suite",
        False,
        {"Mid-Market": 1200.0, "Enterprise": 3200.0},
        ("Mid-Market", "Enterprise"),
        0.55,
    ),
    Product(
        "Dedicated Infrastructure",
        False,
        {"Enterprise": 4500.0},
        ("Enterprise",),
        0.35,
    ),
]

# (term length in months, billing interval in months, prepay discount)
TERM_PLANS = {
    "SMB": [
        ((1, 1, 0.00), 0.34),
        ((12, 1, 0.00), 0.30),
        ((12, 12, 0.12), 0.24),
        ((12, 3, 0.05), 0.09),
        ((24, 12, 0.16), 0.03),
    ],
    "Mid-Market": [
        ((1, 1, 0.00), 0.12),
        ((12, 1, 0.00), 0.28),
        ((12, 3, 0.05), 0.16),
        ((12, 12, 0.12), 0.30),
        ((24, 12, 0.16), 0.10),
        ((36, 12, 0.20), 0.04),
    ],
    "Enterprise": [
        ((12, 1, 0.00), 0.14),
        ((12, 3, 0.05), 0.16),
        ((12, 12, 0.12), 0.32),
        ((24, 12, 0.16), 0.22),
        ((36, 12, 0.20), 0.16),
    ],
}

# New-logo volume by year: the modelled company grows, and new business lands
# disproportionately in Q4 and at quarter ends.
SIGNUP_YEAR_WEIGHTS = {
    2019: 0.09,
    2020: 0.10,
    2021: 0.12,
    2022: 0.13,
    2023: 0.14,
    2024: 0.15,
    2025: 0.17,
    2026: 0.10,
}

MONTH_WEIGHTS = [0.7, 0.8, 1.15, 0.85, 0.9, 1.25, 0.8, 0.75, 1.2, 0.95, 1.0, 1.55]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def weighted_choice(rng: random.Random, weights: dict):
    return rng.choices(list(weights), weights=list(weights.values()), k=1)[0]


def add_months(anchor: date, months: int, day: int | None = None) -> date:
    total = anchor.month - 1 + months
    year = anchor.year + total // 12
    month = total % 12 + 1
    target_day = day if day is not None else anchor.day
    return date(year, month, min(target_day, calendar.monthrange(year, month)[1]))


def round_to_step(value: float, step: float) -> float:
    return max(step, round(value / step) * step)


def quantize(value: float, decimals: int) -> Decimal:
    exp = Decimal(1).scaleb(-decimals)
    return Decimal(str(value)).quantize(exp, rounding=ROUND_HALF_UP)


def next_business_day(day: date) -> date:
    """Scheduled billing runs execute on the next business day."""
    if day.weekday() < 5:
        return day
    return day + timedelta(days=7 - day.weekday())


def pick_signup_date(rng: random.Random) -> date:
    year = weighted_choice(rng, SIGNUP_YEAR_WEIGHTS)
    months = list(range(1, 13)) if year != 2026 else list(range(1, 7))
    month = rng.choices(months, weights=[MONTH_WEIGHTS[m - 1] for m in months], k=1)[0]
    last_day = calendar.monthrange(year, month)[1]
    # Deals cluster at month end, with a secondary bump on the 1st.
    roll = rng.random()
    if roll < 0.22:
        day = rng.randint(last_day - 3, last_day)
    elif roll < 0.38:
        day = rng.randint(1, 3)
    else:
        day = rng.randint(1, last_day)
    return date(year, month, day)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


@dataclass
class Customer:
    customer_id: str
    segment: str
    region: str
    currency: str
    signup_date: date
    seats: int
    discount: float


def make_customer(rng: random.Random, index: int) -> Customer:
    segment = weighted_choice(rng, SEGMENTS)
    region = weighted_choice(rng, REGIONS)
    currency = weighted_choice(rng, REGION_CURRENCIES[region])
    profile = SEGMENT_PROFILE[segment]
    low, high = profile["seats"]
    # Account sizes are heavily right-skewed inside every segment.
    seats = int(round(low * (high / low) ** (rng.random() ** 1.7)))
    lo_disc, hi_disc = profile["discount"]
    return Customer(
        customer_id=f"CUST-{index:06d}",
        segment=segment,
        region=region,
        currency=currency,
        signup_date=pick_signup_date(rng),
        seats=max(1, seats),
        discount=round(rng.uniform(lo_disc, hi_disc), 4),
    )


def local_unit_price(usd_monthly: float, customer: Customer) -> float:
    cur = CURRENCIES[customer.currency]
    listed = usd_monthly * REGION_PRICE_INDEX[customer.region] * cur.per_usd
    return round_to_step(listed, cur.price_step)


def choose_products(rng: random.Random, customer: Customer, count: int) -> list:
    eligible_platforms = [p for p in PLATFORM_PRODUCTS if customer.segment in p.segments]
    products = [rng.choice(eligible_platforms)]
    pool = [p for p in ADDON_PRODUCTS if customer.segment in p.segments]
    for _ in range(count - 1):
        if not pool:
            break
        pick = rng.choices(pool, weights=[p.weight for p in pool], k=1)[0]
        pool.remove(pick)
        products.append(pick)
    return products


def contract_invoices(
    rng: random.Random,
    customer: Customer,
    product: Product,
    contract_id: str,
    start: date,
) -> list:
    """Walk a contract through its terms and emit one row per invoice."""
    profile = SEGMENT_PROFILE[customer.segment]
    (term_months, bill_months, prepay_discount) = weighted_choice(
        rng, dict(TERM_PLANS[customer.segment])
    )
    cur = CURRENCIES[customer.currency]

    if product.per_seat:
        seats = max(1, int(round(customer.seats * product.seat_ratio * rng.uniform(0.8, 1.1))))
        unit_price = local_unit_price(product.price, customer)
    else:
        seats = 1
        unit_price = local_unit_price(product.price[customer.segment], customer)

    discount = min(0.55, customer.discount + prepay_discount + rng.uniform(-0.02, 0.03))
    discount = max(0.0, discount)

    # Some contracts are co-termed to a month boundary and picked up by the
    # scheduled billing run; the rest are invoiced on their anniversary day.
    aligned_to_month_start = rng.random() < 0.42
    if aligned_to_month_start:
        # Service starts on the 1st of the signing month, or of the next one if
        # the deal closed late in the month.
        start = add_months(start, 0 if start.day <= 15 else 1, day=1)
    billing_day = start.day

    rows = []
    term_start = start
    while term_start <= DATASET_END:
        renewal_date = add_months(term_start, term_months)
        periods = max(1, term_months // bill_months)
        for period in range(periods):
            invoice_date = add_months(term_start, period * bill_months, day=billing_day)
            if aligned_to_month_start:
                invoice_date = next_business_day(invoice_date)
            if invoice_date > DATASET_END:
                break
            if invoice_date < DATASET_START:
                continue

            gross = unit_price * seats * bill_months
            amount = gross * (1 - discount)
            # Usage true-ups and mid-period seat changes move the invoice a little.
            amount *= rng.uniform(0.995, 1.045) if rng.random() < 0.30 else 1.0
            rows.append(
                (
                    customer.customer_id,
                    contract_id,
                    invoice_date,
                    renewal_date,
                    product.name,
                    quantize(amount, cur.decimals),
                    customer.currency,
                    customer.region,
                )
            )

            # Mid-term expansions are billed as a prorated top-up invoice.
            if rng.random() < 0.04 and bill_months > 1:
                extra_seats = max(1, int(seats * rng.uniform(0.05, 0.25)))
                offset_days = rng.randint(20, max(21, bill_months * 28 - 10))
                top_up_date = next_business_day(invoice_date + timedelta(days=offset_days))
                remaining = max(0.15, 1 - offset_days / (bill_months * 30.4))
                if DATASET_START <= top_up_date <= DATASET_END:
                    top_up = unit_price * extra_seats * bill_months * (1 - discount) * remaining
                    rows.append(
                        (
                            customer.customer_id,
                            contract_id,
                            top_up_date,
                            renewal_date,
                            product.name,
                            quantize(top_up, cur.decimals),
                            customer.currency,
                            customer.region,
                        )
                    )

        churn = profile["monthly_churn"] if term_months == 1 else profile["term_churn"]
        if rng.random() < churn:
            break

        # Renewal: list price escalation plus net seat expansion or contraction.
        # Month-to-month accounts roll over every month, so their changes have to
        # be far smaller and rarer than a once-a-year committed renewal.
        term_start = renewal_date
        if not aligned_to_month_start:
            billing_day = term_start.day
        committed = term_months >= 12

        if committed:
            unit_price = round_to_step(unit_price * (1 + rng.uniform(0.0, 0.07)), cur.price_step)
        elif rng.random() < 0.08:
            unit_price = round_to_step(unit_price * (1 + rng.uniform(0.0, 0.04)), cur.price_step)

        if product.per_seat:
            if committed:
                growth = rng.gauss(1.12, 0.22) if rng.random() < 0.78 else rng.uniform(0.55, 0.95)
                seats = max(1, int(round(seats * max(0.3, growth))))
            elif rng.random() < 0.18:
                seats = max(1, int(round(seats * max(0.5, rng.gauss(1.02, 0.07)))))

        if committed and rng.random() < 0.10:
            discount = max(0.0, min(0.55, discount + rng.uniform(-0.03, 0.05)))

    return rows


def customer_rows(rng: random.Random, customer: Customer, contract_seq: list) -> list:
    lo, hi = SEGMENT_PROFILE[customer.segment]["contracts"]
    n_contracts = rng.randint(lo, hi)
    products = choose_products(rng, customer, n_contracts)

    rows = []
    for position, product in enumerate(products):
        # Add-ons are usually sold after the initial platform deal.
        if position == 0:
            start = customer.signup_date
        else:
            start = add_months(customer.signup_date, rng.choice([0, 0, 3, 6, 12, 12, 18, 24]))
            if start > DATASET_END:
                continue
        contract_seq[0] += 1
        contract_id = f"CTR-{start.year}-{contract_seq[0]:06d}"
        rows.extend(contract_invoices(rng, customer, product, contract_id, start))
    return rows


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------


def generate(target_rows: int, seed: int) -> list:
    rng = random.Random(seed)
    contract_seq = [0]
    rows: list = []
    customer_index = 0

    last_customer_start = 0
    while len(rows) < target_rows:
        customer_index += 1
        customer = make_customer(rng, customer_index)
        last_customer_start = len(rows)
        rows.extend(customer_rows(rng, customer, contract_seq))

    # Only the final account is trimmed to hit the row target exactly; dropping
    # its most recent invoices makes it look like a younger account and leaves
    # every other account's history intact.
    overflow = len(rows) - target_rows
    if overflow:
        tail = sorted(
            range(last_customer_start, len(rows)),
            key=lambda i: rows[i][2],
            reverse=True,
        )
        drop = set(tail[:overflow])
        rows = [row for i, row in enumerate(rows) if i not in drop]

    rows.sort(key=lambda r: (r[2], r[0], r[1]))
    return rows


def write_csv(rows: list, path: str) -> None:
    header = [
        "customer_id",
        "contract_id",
        "invoice_date",
        "renewal_date",
        "product",
        "amount",
        "currency",
        "region",
    ]
    with open(path, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        for row in rows:
            writer.writerow(
                [
                    row[0],
                    row[1],
                    row[2].isoformat(),
                    row[3].isoformat(),
                    row[4],
                    row[5],
                    row[6],
                    row[7],
                ]
            )


def summarize(rows: list) -> str:
    customers = {r[0] for r in rows}
    contracts = {r[1] for r in rows}
    regions = Counter(r[7] for r in rows)
    currencies = Counter(r[6] for r in rows)
    products = Counter(r[4] for r in rows)
    amounts = sorted(r[5] for r in rows)
    dates = [r[2] for r in rows]

    lines = [
        f"rows            : {len(rows):,}",
        f"customers       : {len(customers):,}",
        f"contracts       : {len(contracts):,}",
        f"invoice dates   : {min(dates)} -> {max(dates)}",
        f"amount min/med/max (mixed currency): "
        f"{amounts[0]} / {amounts[len(amounts) // 2]} / {amounts[-1]}",
        "regions         : "
        + ", ".join(f"{k} {v / len(rows):.1%}" for k, v in regions.most_common()),
        "currencies      : "
        + ", ".join(f"{k} {v / len(rows):.1%}" for k, v in currencies.most_common()),
        "top products    : "
        + ", ".join(f"{k} {v / len(rows):.1%}" for k, v in products.most_common(5)),
    ]
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rows", type=int, default=100_000, help="number of invoice rows")
    parser.add_argument("--seed", type=int, default=20260727, help="random seed")
    parser.add_argument(
        "--output",
        default="data/subscription_transactions.csv",
        help="destination CSV path",
    )
    args = parser.parse_args(argv)

    rows = generate(args.rows, args.seed)
    write_csv(rows, args.output)
    print(f"wrote {args.output}")
    print(summarize(rows))
    return 0


if __name__ == "__main__":
    sys.exit(main())
