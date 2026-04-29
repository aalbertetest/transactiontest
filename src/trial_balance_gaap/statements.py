from __future__ import annotations

from dataclasses import dataclass

from .models import AccountCategory, TrialBalanceLine


@dataclass
class StatementPack:
    income_statement_md: str
    retained_earnings_md: str
    balance_sheet_md: str
    net_income: float
    ending_retained_earnings: float
    trial_balance_out_of_balance: float


def _lines_for(cats: set[AccountCategory], lines: list[TrialBalanceLine]) -> list[TrialBalanceLine]:
    return [ln for ln in lines if ln.category in cats]


def _sum_signed(lines: list[TrialBalanceLine]) -> float:
    return sum(ln.signed_amount for ln in lines)


def _sum_category(lines: list[TrialBalanceLine], cat: AccountCategory) -> float:
    return _sum_signed([ln for ln in lines if ln.category == cat])


def compute_net_income(lines: list[TrialBalanceLine]) -> float:
    rev = _sum_category(lines, AccountCategory.REVENUE) + _sum_category(lines, AccountCategory.OTHER_INCOME)
    exp = (
        _sum_category(lines, AccountCategory.COGS)
        + _sum_category(lines, AccountCategory.OPERATING_EXPENSE)
        + _sum_category(lines, AccountCategory.OTHER_EXPENSE)
        + _sum_category(lines, AccountCategory.INCOME_TAX)
    )
    return rev - exp


def _detail_table(title: str, lines: list[TrialBalanceLine]) -> str:
    if not lines:
        return ""
    rows = []
    for ln in sorted(lines, key=lambda x: x.account.lower()):
        v = ln.signed_amount
        rows.append(f"| {ln.account} | {_fmt(v)} |")
    body = "\n".join(rows)
    return f"**{title}**\n\n| Account | Amount |\n| --- | ---: |\n{body}\n"


def _fmt(x: float) -> str:
    if abs(x - round(x)) < 1e-9:
        return f"{int(round(x)):,}"
    return f"{x:,.2f}"


def build_statements(lines: list[TrialBalanceLine]) -> StatementPack:
    ni = compute_net_income(lines)

    beg_lines = _lines_for({AccountCategory.BEGINNING_RETAINED_EARNINGS}, lines)
    re_lines = _lines_for({AccountCategory.RETAINED_EARNINGS}, lines)
    div_lines = _lines_for({AccountCategory.DIVIDENDS}, lines)

    tb_ending_re = _sum_signed(re_lines)
    div_total = _sum_signed(div_lines)

    if beg_lines:
        beg = _sum_signed(beg_lines)
    elif re_lines:
        # Trial balance "Retained earnings" is treated as ending balance; back into beginning.
        beg = tb_ending_re - ni + div_total
    else:
        beg = 0.0

    ending = beg + ni - div_total
    variance = ending - tb_ending_re if re_lines else 0.0

    # Income statement
    is_parts = [
        "## Income Statement",
        "",
        _detail_table("Revenue", _lines_for({AccountCategory.REVENUE}, lines)),
        _detail_table("Cost of goods sold", _lines_for({AccountCategory.COGS}, lines)),
        _detail_table("Operating expenses", _lines_for({AccountCategory.OPERATING_EXPENSE}, lines)),
        _detail_table("Other income", _lines_for({AccountCategory.OTHER_INCOME}, lines)),
        _detail_table("Other expenses", _lines_for({AccountCategory.OTHER_EXPENSE}, lines)),
        _detail_table("Income tax expense", _lines_for({AccountCategory.INCOME_TAX}, lines)),
        "",
        f"| **Net income** | **{_fmt(ni)}** |",
        "",
    ]
    income_statement_md = "\n".join(p for p in is_parts if p)

    # Statement of retained earnings
    re_md_lines = [
        "## Statement of Retained Earnings",
        "",
        "| | |",
        "| --- | ---: |",
        f"| Beginning retained earnings | {_fmt(beg)} |",
        f"| Net income | {_fmt(ni)} |",
        f"| Dividends | ({_fmt(div_total)}) |" if div_total else "| Dividends | — |",
        f"| **Ending retained earnings** | **{_fmt(ending)}** |",
        "",
    ]
    if re_lines and abs(variance) > 0.005:
        re_md_lines.extend(
            [
                f"*Note: Trial balance retained earnings totals {_fmt(tb_ending_re)}; "
                f"variance vs. rollforward is {_fmt(variance)}. Review classifications or opening balances.*",
                "",
            ]
        )
    retained_earnings_md = "\n".join(re_md_lines)

    # Balance sheet
    ca = _lines_for({AccountCategory.CURRENT_ASSET}, lines)
    nca = _lines_for({AccountCategory.NONCURRENT_ASSET}, lines)
    cl = _lines_for({AccountCategory.CURRENT_LIABILITY}, lines)
    ncl = _lines_for({AccountCategory.NONCURRENT_LIABILITY}, lines)
    eq_only = _lines_for({AccountCategory.EQUITY}, lines)
    other_assets = _lines_for({AccountCategory.OTHER}, lines)

    total_assets = _sum_signed(ca) + _sum_signed(nca) + _sum_signed(other_assets)
    total_liab = _sum_signed(cl) + _sum_signed(ncl)
    equity_from_accounts = _sum_signed(eq_only)
    total_equity = equity_from_accounts + ending
    total_liab_equity = total_liab + total_equity

    bs_parts = [
        "## Balance Sheet",
        "",
        "### Assets",
        "",
        _detail_table("Current assets", ca),
        _detail_table("Non-current assets", nca),
    ]
    if other_assets:
        bs_parts.append(_detail_table("Other (review classification)", other_assets))
    bs_parts.extend(
        [
            "",
            f"| **Total assets** | **{_fmt(total_assets)}** |",
            "",
            "### Liabilities",
            "",
            _detail_table("Current liabilities", cl),
            _detail_table("Non-current liabilities", ncl),
            "",
            f"| **Total liabilities** | **{_fmt(total_liab)}** |",
            "",
            "### Stockholders' equity",
            "",
            _detail_table("Contributed capital and other equity", eq_only),
            f"| Retained earnings (from rollforward) | {_fmt(ending)} |",
            "",
            f"| **Total stockholders' equity** | **{_fmt(total_equity)}** |",
            "",
            f"| **Total liabilities and stockholders' equity** | **{_fmt(total_liab_equity)}** |",
            "",
        ]
    )
    balance_sheet_md = "\n".join(p for p in bs_parts if p)

    tb_check = total_assets - total_liab_equity

    return StatementPack(
        income_statement_md=income_statement_md,
        retained_earnings_md=retained_earnings_md,
        balance_sheet_md=balance_sheet_md,
        net_income=ni,
        ending_retained_earnings=ending,
        trial_balance_out_of_balance=tb_check,
    )
