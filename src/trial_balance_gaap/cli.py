from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .csv_io import parse_trial_balance_csv
from .statements import build_statements


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description="Build GAAP-style financial statements from a trial balance CSV.",
    )
    p.add_argument("input", nargs="?", help="Path to trial balance CSV (stdin if omitted)")
    p.add_argument("-o", "--output", help="Write combined Markdown to this file (default: stdout)")
    args = p.parse_args(argv)

    if args.input:
        lines = parse_trial_balance_csv(Path(args.input))
    else:
        lines = parse_trial_balance_csv(sys.stdin)

    pack = build_statements(lines)

    out = [
        "# Financial Statements (GAAP-style)",
        "",
        "_Generated from trial balance. Classify accounts with a `category` column for accuracy; "
        "otherwise keyword inference is used._",
        "",
        pack.income_statement_md,
        pack.retained_earnings_md,
        pack.balance_sheet_md,
        "## Checks",
        "",
        f"| Net income (income statement) | {_fmt(pack.net_income)} |",
        f"| Ending retained earnings | {_fmt(pack.ending_retained_earnings)} |",
        f"| Assets − Liabilities − Equity (should be 0) | {_fmt(pack.trial_balance_out_of_balance)} |",
        "",
    ]
    if abs(pack.trial_balance_out_of_balance) > 0.05:
        out.append(
            "**Warning:** Balance sheet does not tie. Check account categories (especially OTHER), "
            "or ensure debits equal credits in the trial balance.\n"
        )

    text = "\n".join(out)

    if args.output:
        Path(args.output).write_text(text, encoding="utf-8")
    else:
        sys.stdout.write(text)

    return 0


def _fmt(x: float) -> str:
    if abs(x - round(x)) < 1e-9:
        return f"{int(round(x)):,}"
    return f"{x:,.2f}"


if __name__ == "__main__":
    raise SystemExit(main())
