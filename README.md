# PayHub

A minimal production-style payment API with double-entry ledger, fraud rules, idempotency, and observability.

## Setup

```bash
cd /workspace
pip install -e ".[dev]"
```

## Run API

```bash
uvicorn payhub.main:app --reload --app-dir src
```

Default admin API key (development only): set `PAYHUB_BOOTSTRAP_ADMIN_KEY` or use the value printed on first bootstrap.

## Tests

```bash
pytest src/../tests -q --tb=short
```

Environment variables are documented in `src/payhub/config.py`.
