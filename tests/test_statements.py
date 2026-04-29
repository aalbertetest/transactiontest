from pathlib import Path

import pytest

from trial_balance_gaap.csv_io import parse_trial_balance_csv
from trial_balance_gaap.statements import build_statements, compute_net_income


def test_sample_ties():
    path = Path(__file__).resolve().parent.parent / "examples" / "sample_trial_balance.csv"
    lines = parse_trial_balance_csv(path)
    pack = build_statements(lines)
    assert abs(pack.trial_balance_out_of_balance) < 0.05


def test_net_income():
    path = Path(__file__).resolve().parent.parent / "examples" / "sample_trial_balance.csv"
    lines = parse_trial_balance_csv(path)
    ni = compute_net_income(lines)
    assert abs(ni - 7000) < 0.01


def test_parse_amount_column():
    csv = "account,amount\nCash,1000\nRevenue,,-5000\n"
    lines = parse_trial_balance_csv(csv)
    assert len(lines) == 2
