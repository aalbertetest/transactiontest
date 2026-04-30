"""Tests for transactions.load and transactions.summarize."""

from __future__ import annotations

import csv
import os
import textwrap
from pathlib import Path

import pytest

from transactions import Transaction, load, summarize


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture()
def csv_file(tmp_path: Path) -> Path:
    """Write a minimal CSV with a header and three data rows."""
    p = tmp_path / "data.csv"
    p.write_text(
        textwrap.dedent("""\
            id,amt,cat
            1,10.50,food
            2,20.00,transport
            3,5.25,food
        """)
    )
    return p


@pytest.fixture()
def csv_no_header(tmp_path: Path) -> Path:
    """CSV without a header row."""
    p = tmp_path / "no_header.csv"
    p.write_text(
        textwrap.dedent("""\
            1,10.50,food
            2,20.00,transport
        """)
    )
    return p


@pytest.fixture()
def csv_with_blanks(tmp_path: Path) -> Path:
    """CSV containing blank lines interspersed with data."""
    p = tmp_path / "blanks.csv"
    p.write_text("id,amt,cat\n\n1,7.00,food\n\n2,3.00,transport\n\n")
    return p


@pytest.fixture()
def csv_empty(tmp_path: Path) -> Path:
    """Completely empty CSV file."""
    p = tmp_path / "empty.csv"
    p.write_text("")
    return p


@pytest.fixture()
def csv_header_only(tmp_path: Path) -> Path:
    """CSV with only a header row and no data."""
    p = tmp_path / "header_only.csv"
    p.write_text("id,amt,cat\n")
    return p


# ---------------------------------------------------------------------------
# Tests for load()
# ---------------------------------------------------------------------------

class TestLoad:
    def test_basic_load(self, csv_file: Path) -> None:
        rows = load(str(csv_file))
        assert len(rows) == 3
        assert rows[0] == {"id": 1, "amt": 10.50, "cat": "food"}
        assert rows[1] == {"id": 2, "amt": 20.00, "cat": "transport"}
        assert rows[2] == {"id": 3, "amt": 5.25, "cat": "food"}

    def test_no_header(self, csv_no_header: Path) -> None:
        rows = load(str(csv_no_header))
        assert len(rows) == 2
        assert rows[0]["cat"] == "food"
        assert rows[1]["cat"] == "transport"

    def test_blank_rows_skipped(self, csv_with_blanks: Path) -> None:
        rows = load(str(csv_with_blanks))
        assert len(rows) == 2

    def test_empty_file(self, csv_empty: Path) -> None:
        assert load(str(csv_empty)) == []

    def test_header_only(self, csv_header_only: Path) -> None:
        assert load(str(csv_header_only)) == []

    def test_types(self, csv_file: Path) -> None:
        row = load(str(csv_file))[0]
        assert isinstance(row["id"], int)
        assert isinstance(row["amt"], float)
        assert isinstance(row["cat"], str)

    def test_file_not_found(self) -> None:
        with pytest.raises(FileNotFoundError):
            load("/nonexistent/path.csv")


# ---------------------------------------------------------------------------
# Tests for summarize()
# ---------------------------------------------------------------------------

class TestSummarize:
    def test_basic_summary(self, csv_file: Path) -> None:
        rows = load(str(csv_file))
        result = summarize(rows)
        assert result == pytest.approx({"food": 15.75, "transport": 20.00})

    def test_empty_list(self) -> None:
        assert summarize([]) == {}

    def test_single_category(self) -> None:
        rows: list[Transaction] = [
            {"id": 1, "amt": 5.0, "cat": "food"},
            {"id": 2, "amt": 3.0, "cat": "food"},
        ]
        assert summarize(rows) == pytest.approx({"food": 8.0})

    def test_many_categories(self) -> None:
        rows: list[Transaction] = [
            {"id": i, "amt": float(i), "cat": f"cat{i}"} for i in range(1, 6)
        ]
        result = summarize(rows)
        assert len(result) == 5
        assert result == pytest.approx({f"cat{i}": float(i) for i in range(1, 6)})

    def test_negative_amounts(self) -> None:
        rows: list[Transaction] = [
            {"id": 1, "amt": -10.0, "cat": "refund"},
            {"id": 2, "amt": 5.0, "cat": "refund"},
        ]
        assert summarize(rows) == pytest.approx({"refund": -5.0})

    def test_zero_amounts(self) -> None:
        rows: list[Transaction] = [
            {"id": 1, "amt": 0.0, "cat": "misc"},
        ]
        assert summarize(rows) == pytest.approx({"misc": 0.0})
