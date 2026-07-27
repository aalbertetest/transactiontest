# Synthetic subscription transaction data

`data/subscription_transactions.csv` holds **100,000 subscription invoice rows** for a
fictional B2B SaaS vendor, covering **2019-01-01 through 2026-06-30**. The data is
generated, not sampled from any real system, so it is safe to publish, share and load
into demos or test environments.

```
customer_id,contract_id,invoice_date,renewal_date,product,amount,currency,region
CUST-001312,CTR-2019-002466,2019-01-01,2020-01-01,Core Platform - Starter,552.29,USD,North America
CUST-002003,CTR-2019-003752,2019-01-01,2019-02-01,Core Platform - Professional,132.14,EUR,EMEA
CUST-003198,CTR-2019-006010,2019-01-01,2021-01-01,Core Platform - Professional,82048.48,GBP,EMEA
```

## Schema

| Column | Type | Notes |
| --- | --- | --- |
| `customer_id` | string | `CUST-######`. 3,721 distinct accounts. A customer keeps one region and one billing currency. |
| `contract_id` | string | `CTR-<signing year>-######`. 6,969 distinct contracts. One contract covers exactly one product and belongs to one customer. |
| `invoice_date` | date (`YYYY-MM-DD`) | Date the invoice was raised, i.e. the start of the billing period it covers. |
| `renewal_date` | date (`YYYY-MM-DD`) | End of the contract term the invoice falls in — the date the contract next comes up for renewal. Always after `invoice_date`. |
| `product` | string | One of 13 catalogue items (3 platform editions plus 10 add-ons). |
| `amount` | decimal | Net invoiced amount in `currency`, excluding tax. Two decimals, or whole units for JPY. |
| `currency` | string | ISO 4217 code, one of 15. |
| `region` | string | `North America`, `EMEA`, `APAC` or `LATAM`. |

Rows are sorted by `invoice_date`, then `customer_id`, then `contract_id`, the way a
billing-system export usually arrives.

## What makes the rows hang together

The generator models customers and contracts rather than emitting independent random
rows, so the usual subscription-analytics questions have real answers in this data.

- **Contracts have a life.** A contract starts, bills on its cadence, renews at term
  boundaries, and eventually churns. Invoice counts per contract run from 1 to 89
  (median 7).
- **Billing cadence follows the term.** Contracts are month-to-month, annual or
  multi-year (24/36 months), billed monthly, quarterly or up front. A monthly-billed
  annual contract emits twelve invoices that all share one `renewal_date`; that date
  then rolls forward a year.
- **Two invoicing conventions.** About 42% of contracts are co-termed to the 1st of a
  month and picked up by a scheduled billing run that skips to the next business day.
  The rest bill on their anniversary day, clamped to the length of short months
  (a 31st anniversary bills on 28 or 29 February).
- **Prices come from a per-currency price book.** USD list prices are adjusted by a
  regional price index and the currency's rate, then rounded to a publishing grid
  (nearest ¥100, ₹50, R$5, kr10, and so on) — so amounts look like they came from a
  real price list rather than an FX conversion.
- **Amounts move for the reasons they move in practice.** Negotiated discounts widen
  with account size, prepayment earns 5–20% off, list prices escalate 0–7% at renewal,
  seat counts expand more often than they contract, and usage true-ups nudge roughly a
  third of invoices by a few percent. A small share of invoices are prorated mid-term
  seat top-ups, which is why some amounts are much smaller than the contract's usual
  invoice.
- **The vendor grows.** Volume rises from 1,445 invoices in 2019 to 23,357 in 2025,
  with new business clustering in Q4 and at quarter ends.
- **Account sizes are skewed.** SMB, mid-market and enterprise accounts are mixed
  62/28/10, and seat counts are right-skewed inside each segment. In USD-equivalent
  terms the median invoice is about $500, the 95th percentile about $27,000 and the
  largest a $4.0M annual prepayment.

Mix: North America 45%, EMEA 29%, APAC 19%, LATAM 7%; USD 40% of rows, then EUR, GBP,
CAD, JPY, INR, AUD, SGD, BRL, CHF, MXN, SEK, NZD, AED, ZAR.

## Regenerating

Pure standard library, no dependencies, and deterministic for a given seed:

```bash
python3 generate_subscription_transactions.py                     # rewrites the committed CSV
python3 generate_subscription_transactions.py --rows 5000 --seed 42 --output sample.csv
python3 validate_dataset.py data/subscription_transactions.csv    # invariants + profile
```

`validate_dataset.py` exits non-zero if any invariant breaks: the header, no empty
fields, `invoice_date < renewal_date`, positive amounts, correct minor units, and
customer/product/currency/region staying stable within a contract.

## Simplifications worth knowing

The file is a clean billing export, not a messy one. There are no duplicates, no
credit notes or negative amounts, no tax or invoice-level identifiers, and no partial
or failed payments. FX rates are fixed points in time rather than a daily series.
Renewal dates are recorded on every invoice in a term, including the last invoice of a
contract that ultimately churned, so churn has to be inferred from the absence of
later invoices — the same inference the real export requires.
