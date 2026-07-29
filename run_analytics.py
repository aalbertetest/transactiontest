#!/usr/bin/env python3
"""Run the ERP analytics pack and write a Markdown report."""

from __future__ import annotations

import argparse
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "data" / "fictional_erp.sqlite"
DEFAULT_SQL = ROOT / "analytics" / "erp_analytics.sql"
DEFAULT_REPORT = ROOT / "analytics" / "analytics_report.md"


def parse_queries(sql_text: str) -> list[tuple[str, str]]:
    matches = list(re.finditer(r"^-- name: (.+)$", sql_text, flags=re.MULTILINE))
    queries = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(sql_text)
        query = sql_text[start:end].strip()
        if query:
            queries.append((match.group(1).strip(), query))
    return queries


def markdown_table(columns: list[str], rows: list[tuple[object, ...]]) -> str:
    def text(value: object) -> str:
        return "" if value is None else str(value).replace("|", "\\|")

    output = [
        "| " + " | ".join(columns) + " |",
        "| " + " | ".join("---" for _ in columns) + " |",
    ]
    output.extend("| " + " | ".join(text(value) for value in row) + " |" for row in rows)
    return "\n".join(output)


def run(database: Path, sql_path: Path, report_path: Path) -> None:
    queries = parse_queries(sql_path.read_text(encoding="utf-8"))
    conn = sqlite3.connect(f"file:{database}?mode=ro", uri=True)
    try:
        sections = [
            "# Fictional ERP analytics report",
            "",
            f"Database: `{database.name}`  ",
            f"Generated: {datetime.now(timezone.utc).date().isoformat()}  ",
            "Functional currency: USD; transaction-currency totals remain grouped by currency.",
            "",
        ]
        for title, sql in queries:
            cursor = conn.execute(sql)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            sections.extend([f"## {title}", "", markdown_table(columns, rows), ""])
    finally:
        conn.close()
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(sections), encoding="utf-8")
    print(f"Wrote {len(queries)} analyses to {report_path}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--database", type=Path, default=DEFAULT_DB)
    parser.add_argument("--sql", type=Path, default=DEFAULT_SQL)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run(args.database, args.sql, args.report)
