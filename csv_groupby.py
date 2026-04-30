#!/usr/bin/env python3
"""Aggregate CSV data by grouping on one or more columns and summing a value column."""

import argparse
import sys
import textwrap
from collections import defaultdict
from pathlib import Path

import pandas as pd


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        prog="csv_groupby",
        description="Group rows in a CSV file by one or more columns and sum a numeric column.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            examples:
              %(prog)s -i sales.csv -g category -v amount
              %(prog)s -i sales.csv -g category -v amount -o summary.csv
              %(prog)s -i data.tsv  -g region   -v revenue -d '\\t'
              %(prog)s -i orders.csv -g region country -v total --agg mean
              cat data.csv | %(prog)s -g category -v amount
        """),
    )

    parser.add_argument(
        "-i", "--input",
        metavar="FILE",
        help=(
            "Path to the input CSV file. "
            "If omitted, data is read from stdin."
        ),
    )
    parser.add_argument(
        "-o", "--output",
        metavar="FILE",
        help=(
            "Path to write the output CSV. "
            "If omitted, results are printed to stdout."
        ),
    )
    parser.add_argument(
        "-d", "--delimiter",
        default=",",
        metavar="CHAR",
        help="Field delimiter for both input and output (default: ',').",
    )
    parser.add_argument(
        "-g", "--group-by",
        required=True,
        nargs="+",
        metavar="COL",
        help="One or more column names to group by.",
    )
    parser.add_argument(
        "-v", "--value",
        required=True,
        metavar="COL",
        help="Numeric column to aggregate.",
    )
    parser.add_argument(
        "--agg",
        default="sum",
        choices=["sum", "mean", "median", "min", "max", "count", "std"],
        help="Aggregation function to apply (default: sum).",
    )

    return parser.parse_args(argv)


def resolve_delimiter(raw: str) -> str:
    """Interpret common escape sequences so users can pass '\\t' on the command line."""
    return raw.encode("utf-8").decode("unicode_escape")


def read_input(path: str | None, delimiter: str) -> pd.DataFrame:
    source = path if path else sys.stdin
    try:
        return pd.read_csv(source, delimiter=delimiter)
    except FileNotFoundError:
        sys.exit(f"error: input file not found: {path}")
    except pd.errors.EmptyDataError:
        sys.exit("error: input file is empty")
    except pd.errors.ParserError as exc:
        sys.exit(f"error: failed to parse CSV: {exc}")


def validate_columns(df: pd.DataFrame, group_cols: list[str], value_col: str):
    missing = [c for c in group_cols if c not in df.columns]
    if missing:
        sys.exit(
            f"error: group-by column(s) not found: {', '.join(missing)}\n"
            f"  available columns: {', '.join(df.columns)}"
        )
    if value_col not in df.columns:
        sys.exit(
            f"error: value column not found: {value_col}\n"
            f"  available columns: {', '.join(df.columns)}"
        )


def aggregate(df: pd.DataFrame, group_cols: list[str], value_col: str, agg: str) -> pd.DataFrame:
    return (
        df.groupby(group_cols, sort=True)[value_col]
        .agg(agg)
        .reset_index()
    )


def write_output(result: pd.DataFrame, path: str | None, delimiter: str):
    if path:
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(path, index=False, sep=delimiter)
    else:
        sys.stdout.write(result.to_csv(index=False, sep=delimiter))


def main(argv=None):
    args = parse_args(argv)
    delimiter = resolve_delimiter(args.delimiter)

    df = read_input(args.input, delimiter)
    validate_columns(df, args.group_by, args.value)
    result = aggregate(df, args.group_by, args.value, args.agg)
    write_output(result, args.output, delimiter)


if __name__ == "__main__":
    main()
