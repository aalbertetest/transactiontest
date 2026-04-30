#!/usr/bin/env python3
"""Generate fake KPI metrics with overly optimistic board-deck commentary."""

import random
import datetime
import json
import argparse
import sys

METRIC_DEFS = [
    {
        "name": "Monthly Active Users (MAU)",
        "unit": "",
        "base": 125_000,
        "drift": (0.03, 0.12),
        "fmt": "{:,.0f}",
    },
    {
        "name": "Annual Recurring Revenue (ARR)",
        "unit": "$",
        "base": 18_500_000,
        "drift": (0.04, 0.15),
        "fmt": "${:,.0f}",
    },
    {
        "name": "Net Revenue Retention (NRR)",
        "unit": "%",
        "base": 112,
        "drift": (0.01, 0.06),
        "fmt": "{:.1f}%",
    },
    {
        "name": "Customer Acquisition Cost (CAC)",
        "unit": "$",
        "base": 320,
        "drift": (-0.10, -0.02),
        "fmt": "${:,.0f}",
    },
    {
        "name": "Gross Margin",
        "unit": "%",
        "base": 72,
        "drift": (0.005, 0.04),
        "fmt": "{:.1f}%",
    },
    {
        "name": "Logo Churn Rate",
        "unit": "%",
        "base": 3.2,
        "drift": (-0.15, -0.01),
        "fmt": "{:.2f}%",
    },
    {
        "name": "Net Promoter Score (NPS)",
        "unit": "",
        "base": 58,
        "drift": (0.02, 0.10),
        "fmt": "{:.0f}",
    },
    {
        "name": "Pipeline Coverage Ratio",
        "unit": "x",
        "base": 3.1,
        "drift": (0.03, 0.12),
        "fmt": "{:.1f}x",
    },
    {
        "name": "Burn Multiple",
        "unit": "x",
        "base": 1.8,
        "drift": (-0.12, -0.02),
        "fmt": "{:.2f}x",
    },
    {
        "name": "Employee Headcount",
        "unit": "",
        "base": 215,
        "drift": (0.02, 0.08),
        "fmt": "{:,.0f}",
    },
]

COMMENTARY_TEMPLATES = {
    "up_strong": [
        "Exceptional momentum — {metric} surged {delta}, far exceeding internal targets.",
        "A breakout quarter for {metric}. The team delivered a stunning {delta} improvement, "
        "validating our strategic thesis.",
        "{metric} is up {delta} QoQ — a testament to disciplined execution and market tailwinds.",
        "We're thrilled to report {metric} grew {delta}. This inflection point signals "
        "massive white-space ahead.",
        "{metric} accelerated {delta}, firmly placing us in best-in-class territory.",
    ],
    "up_moderate": [
        "{metric} improved by a healthy {delta}, tracking ahead of plan.",
        "Steady gains in {metric} ({delta}) reflect the compounding value of our platform moat.",
        "{metric} rose {delta} — consistent, durable growth that the market will reward.",
        "An encouraging {delta} lift in {metric} gives us high conviction heading into next quarter.",
        "We continue to see strong traction: {metric} is up {delta}, right on our glide-path.",
    ],
    "down_is_good": [
        "{metric} dropped {delta} — exactly the efficiency unlock we were targeting.",
        "Incredible leverage story: {metric} improved by {delta} as unit economics continue "
        "to compound.",
        "{metric} declined {delta} this quarter, underscoring the scalability of our operating model.",
        "Best-in-class {metric} improvement of {delta}. Investors should note this is "
        "a structural advantage.",
        "Pleased to report a {delta} reduction in {metric}, well ahead of the cohort benchmarks.",
    ],
    "flat_spin": [
        "{metric} held steady — demonstrating resilience in a turbulent macro environment.",
        "Despite industry headwinds, {metric} remained stable, showcasing the anti-fragility "
        "of our model.",
        "{metric} was essentially flat, which we view as a strong result given broad-based "
        "market softness.",
        "Stability in {metric} reflects disciplined execution. We expect inflection in the "
        "coming quarter as recent investments mature.",
    ],
}

OVERALL_SUMMARIES = [
    "In summary, this was a landmark quarter. The business is firing on all cylinders, "
    "and we are well-positioned to capture an outsized share of a rapidly expanding TAM.",
    "Q{q} results reaffirm our conviction that we are building a generational company. "
    "Every leading indicator points to accelerating momentum.",
    "The data speaks for itself: durable growth, improving efficiency, and a world-class "
    "team executing at the highest level. We have never been more excited about the road ahead.",
    "These results place us in rarefied air among our peer set. We look forward to "
    "discussing our plans to build on this momentum at the upcoming board offsite.",
    "Another quarter of relentless progress. We are in a category of one — and this is "
    "only the beginning.",
]


def _quarter_label(date: datetime.date) -> tuple[int, int]:
    q = (date.month - 1) // 3 + 1
    return date.year, q


def generate_metrics(
    num_quarters: int = 4,
    end_date: datetime.date | None = None,
    seed: int | None = None,
) -> list[dict]:
    if seed is not None:
        random.seed(seed)
    if end_date is None:
        end_date = datetime.date.today()

    quarters: list[dict] = []
    for i in range(num_quarters - 1, -1, -1):
        qdate = end_date - datetime.timedelta(days=91 * i)
        year, q = _quarter_label(qdate)
        quarter_data: dict = {
            "label": f"Q{q} {year}",
            "year": year,
            "quarter": q,
            "metrics": [],
        }

        for mdef in METRIC_DEFS:
            scale = 1 + random.uniform(*mdef["drift"])
            elapsed = num_quarters - i
            value = mdef["base"] * (scale ** elapsed)
            value += random.gauss(0, abs(mdef["base"]) * 0.01)

            prev_scale = 1 + random.uniform(*mdef["drift"])
            prev_value = mdef["base"] * (prev_scale ** (elapsed - 1))
            pct_change = ((value - prev_value) / abs(prev_value)) * 100

            quarter_data["metrics"].append(
                {
                    "name": mdef["name"],
                    "value": value,
                    "formatted": mdef["fmt"].format(value),
                    "pct_change": round(pct_change, 2),
                }
            )

        quarters.append(quarter_data)

    return quarters


def _pick_commentary(pct_change: float, metric_name: str, lower_is_better: bool) -> str:
    abs_change = abs(pct_change)
    delta_str = f"{abs_change:.1f}%"

    if lower_is_better:
        if pct_change < -1:
            bucket = "down_is_good"
        else:
            bucket = "flat_spin"
    else:
        if pct_change > 5:
            bucket = "up_strong"
        elif pct_change > 1:
            bucket = "up_moderate"
        else:
            bucket = "flat_spin"

    template = random.choice(COMMENTARY_TEMPLATES[bucket])
    return template.format(metric=metric_name, delta=delta_str)


LOWER_IS_BETTER = {"Customer Acquisition Cost (CAC)", "Logo Churn Rate", "Burn Multiple"}


def build_deck_text(quarters: list[dict]) -> str:
    lines: list[str] = []
    lines.append("=" * 72)
    lines.append("  QUARTERLY KPI DASHBOARD — BOARD OF DIRECTORS REVIEW")
    lines.append("=" * 72)
    lines.append("")

    latest = quarters[-1]
    lines.append(f"  Reporting Period: {latest['label']}")
    lines.append(f"  Generated: {datetime.datetime.now():%B %d, %Y}")
    lines.append("")
    lines.append("-" * 72)

    for m in latest["metrics"]:
        lower_is_better = m["name"] in LOWER_IS_BETTER
        commentary = _pick_commentary(m["pct_change"], m["name"], lower_is_better)

        lines.append("")
        lines.append(f"  {m['name']}")
        lines.append(f"    Current Value : {m['formatted']}")
        direction = "▼" if m["pct_change"] < 0 else "▲"
        lines.append(f"    QoQ Change     : {direction} {abs(m['pct_change']):.1f}%")
        lines.append(f"    Commentary     : {commentary}")
        lines.append("")
        lines.append("  " + "- " * 35)

    lines.append("")
    lines.append("-" * 72)
    lines.append("  EXECUTIVE SUMMARY")
    lines.append("-" * 72)
    q = latest["quarter"]
    summary = random.choice(OVERALL_SUMMARIES).format(q=q)
    lines.append(f"  {summary}")
    lines.append("")

    lines.append("-" * 72)
    lines.append("  TREND TABLE (last {} quarters)".format(len(quarters)))
    lines.append("-" * 72)
    lines.append("")

    metric_names = [m["name"] for m in METRIC_DEFS]
    header = f"  {'Metric':<38}" + "".join(f"{q['label']:>12}" for q in quarters)
    lines.append(header)
    lines.append("  " + "-" * (38 + 12 * len(quarters)))

    for mname in metric_names:
        row = f"  {mname:<38}"
        for q in quarters:
            val = next(m for m in q["metrics"] if m["name"] == mname)
            row += f"{val['formatted']:>12}"
        lines.append(row)

    lines.append("")
    lines.append("=" * 72)
    lines.append("  CONFIDENTIAL — FOR BOARD USE ONLY")
    lines.append("=" * 72)
    return "\n".join(lines)


def build_json(quarters: list[dict]) -> str:
    return json.dumps(quarters, indent=2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate fake KPI metrics with optimistic board-deck commentary."
    )
    parser.add_argument(
        "-q", "--quarters", type=int, default=4, help="Number of quarters to generate (default: 4)"
    )
    parser.add_argument(
        "-s", "--seed", type=int, default=None, help="Random seed for reproducibility"
    )
    parser.add_argument(
        "-f",
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Write output to file instead of stdout"
    )
    args = parser.parse_args()

    quarters = generate_metrics(num_quarters=args.quarters, seed=args.seed)

    if args.format == "json":
        result = build_json(quarters)
    else:
        result = build_deck_text(quarters)

    if args.output:
        with open(args.output, "w") as f:
            f.write(result)
            f.write("\n")
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(result)


if __name__ == "__main__":
    main()
