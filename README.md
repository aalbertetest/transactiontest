# Trial balance → GAAP statements

Small CLI: read a **trial balance CSV**, emit **income statement**, **statement of retained earnings**, and **balance sheet** (Markdown).

## Install

```bash
pip install -e ".[dev]"
```

## CSV format

Header row with:

- **account** (or `account_name`, `name`, `description`)
- **debit** and **credit** (or a single **amount** column: positive = debit, negative = credit)
- optional **category** for explicit GAAP grouping (recommended)

Categories (examples): `current_asset`, `noncurrent_asset`, `current_liability`, `noncurrent_liability`, `equity`, `retained_earnings`, `beginning_retained_earnings`, `revenue`, `cogs`, `operating_expense`, `other_income`, `other_expense`, `income_tax`, `dividends`, `other`.

If `category` is omitted, accounts are inferred from keywords (rough).

## Run

```bash
tb-gaap path/to/trial_balance.csv
tb-gaap path/to/trial_balance.csv -o statements.md
cat trial_balance.csv | tb-gaap
```

Example file: `examples/sample_trial_balance.csv`.

## Tests

```bash
python3 -m pytest
```
