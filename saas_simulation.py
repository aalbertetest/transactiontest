#!/usr/bin/env python3
"""
SaaS customer simulation (2M rows) and analytics: cohorts, LTV, churn model, anomalies.

Run: python saas_simulation.py

Outputs: printed methodology, metrics, and ./outputs/ directory with CSV summaries
when SAVE_OUTPUTS=1 (default).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    average_precision_score,
    classification_report,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

# ---------------------------------------------------------------------------
# Reproducibility and scale
# ---------------------------------------------------------------------------
RNG = np.random.default_rng(42)
N_CUSTOMERS = 2_000_000
AS_OF = date(2026, 4, 1)  # "today" for tenure and cohort views
SAVE_OUTPUTS = os.environ.get("SAVE_OUTPUTS", "1") == "1"
OUT_DIR = Path(__file__).resolve().parent / "outputs"


@dataclass(frozen=True)
class PlanSpec:
    name: str
    quota_units: float  # included usage per month (same units as usage)
    price_mrr: float  # monthly subscription (USD)
    overage_per_unit: float
    weight: float  # sampling weight for plan mix


PLANS = (
    PlanSpec("Starter", 1_000, 49.0, 0.02, 0.55),
    PlanSpec("Growth", 10_000, 199.0, 0.015, 0.30),
    PlanSpec("Enterprise", 100_000, 999.0, 0.01, 0.15),
)
PLAN_NAMES = [p.name for p in PLANS]
PLAN_QUOTAS = np.array([p.quota_units for p in PLANS])
PLAN_MRR = np.array([p.price_mrr for p in PLANS])
PLAN_OVERAGE_RATE = np.array([p.overage_per_unit for p in PLANS])
PLAN_WEIGHTS = np.array([p.weight for p in PLANS])
PLAN_WEIGHTS = PLAN_WEIGHTS / PLAN_WEIGHTS.sum()

GEO_REGIONS = ["NA", "EU", "APAC", "LATAM", "MEA"]
GEO_WEIGHTS = np.array([0.45, 0.28, 0.18, 0.06, 0.03], dtype=float)


def _print_section(title: str) -> None:
    bar = "=" * len(title)
    print(f"\n{bar}\n{title}\n{bar}")


def simulate_customers(n: int) -> pd.DataFrame:
    """
    Simulate one row per customer at a snapshot date AS_OF.

    **Signup date**
    - Drawn uniformly over a 730-day window ending the day before AS_OF.
    - *Assumption*: Uniform arrivals approximate steady marketing spend; real SaaS
      often has seasonality and growth tilt—we keep uniform for clarity.

    **Plan type**
    - Multinomial with weights (Starter-heavy), reflecting a typical PLG funnel.

    **Monthly usage** (same abstract "units" for all plans, e.g. API calls / GB)
    - Log-normal around a plan-specific mean so usage is right-skewed (typical).
    - *Formula*: usage = exp(μ_plan + σ * Z), Z ~ N(0,1).
    - Enterprise customers get higher μ; σ controls tail heaviness.

    **Overages**
    - *Formula*: overage_units = max(0, usage - quota_plan).
    - *Formula*: overage_charge_usd = overage_units * overage_rate_plan.
    - *Assumption*: Single monthly bucket (no rollover credits).

    **Churn risk** (latent 0–1 propensity, not observed by the product in full)
    - Combines: usage pressure (usage / quota), tenure (younger = riskier here),
      geography noise, and random frailty.
    - Mapped through a logistic *construction* so risk stays in (0,1):
      risk = sigmoid( β_usage * (usage/quota - 1) + β_new * I(tenure<3mo)
                      + β_geo + ε ), with ε ~ Logistic(0, scale).
    - **Interpretation**: Higher usage than quota and short tenure increase risk
      in this toy world; calibrate on real data.

    **Churned label** (outcome for supervised learning)
    - Bernoulli with p = churn_risk perturbed by noise so AUC is not trivial.
    - *Assumption*: Observed churn realizes latent risk with extra noise.

    **Geography**
    - Categorical NA/EU/APAC/LATAM/MEA with fixed mix.
    """
    # Signup: integer days before AS_OF
    max_days = 730
    days_ago = RNG.integers(1, max_days + 1, size=n)
    signups = np.array([AS_OF - timedelta(int(d)) for d in days_ago], dtype="datetime64[D]")

    plan_idx = RNG.choice(len(PLANS), size=n, p=PLAN_WEIGHTS)
    quota = PLAN_QUOTAS[plan_idx]
    mrr = PLAN_MRR[plan_idx]
    overage_rate = PLAN_OVERAGE_RATE[plan_idx]

    # Log-normal usage: μ scales with log quota so Starter isn't always maxed
    mu = np.log(np.maximum(quota * 0.35, 50.0)) + np.array([0.0, 0.4, 0.9])[plan_idx]
    sigma = np.array([0.85, 0.75, 0.65])[plan_idx]
    usage = RNG.lognormal(mean=mu, sigma=sigma, size=n)

    overage_units = np.maximum(0.0, usage - quota)
    overage_usd = overage_units * overage_rate

    tenure_days = (np.datetime64(AS_OF) - signups).astype("timedelta64[D]").astype(int)
    tenure_months = np.clip(tenure_days / 30.4375, 0.01, 120.0)
    usage_ratio = usage / np.maximum(quota, 1.0)

    geo_idx = RNG.choice(len(GEO_REGIONS), size=n, p=GEO_WEIGHTS / GEO_WEIGHTS.sum())
    geo = np.array(GEO_REGIONS)[geo_idx]
    # Small geography effect on risk (one-hot style coefficients)
    geo_effect = (
        (geo == "LATAM").astype(float) * 0.25
        + (geo == "MEA").astype(float) * 0.20
        + (geo == "APAC").astype(float) * 0.05
    )

    # Standard logistic noise: Z = log(U/(1-U)), U ~ Uniform(0,1)
    u = np.clip(RNG.random(n), 1e-9, 1.0 - 1e-9)
    z = np.log(u / (1.0 - u))
    logit = (
        0.9 * (usage_ratio - 1.0)
        + 0.45 * (tenure_months < 3).astype(float)
        - 0.35 * np.log1p(tenure_months)
        + geo_effect
        + 0.35 * z
    )
    churn_risk = 1.0 / (1.0 + np.exp(-np.clip(logit, -20, 20)))

    # Realized churn: noisy draw from risk
    churn_draw = RNG.random(n) < np.clip(0.25 * churn_risk + 0.12 * RNG.random(n), 0, 0.95)

    signup_month = pd.to_datetime(signups).to_period("M")

    df = pd.DataFrame(
        {
            "customer_id": np.arange(n, dtype=np.int64),
            "signup_date": signups,
            "signup_month": signup_month,
            "plan": np.array(PLAN_NAMES)[plan_idx],
            "plan_idx": plan_idx,
            "quota": quota,
            "monthly_usage": usage,
            "overage_units": overage_units,
            "overage_usd": overage_usd,
            "mrr_usd": mrr,
            "churn_risk": churn_risk,
            "churned": churn_draw,
            "geography": geo,
            "tenure_days": tenure_days,
            "tenure_months": tenure_months,
            "usage_ratio": usage_ratio,
        }
    )
    return df


def cohort_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    **Cohort**: customers grouped by `signup_month` (calendar month of signup).

    **Metrics per cohort**
    - *cohort_size*: number of signups.
    - *retention_proxy*: share with `churned == False` in this snapshot.
      *Assumption*: Single snapshot—"retention" is really 1 - churned so far, not
      true month-N retention curves without panel data.
    - *avg_mrr*, *avg_usage_ratio*: descriptive quality of each vintage.

    **Interpretation**
    - If older cohorts show higher retention_proxy, newer signups may be lower fit
      (or simulation tenure effect). Compare with avg_usage_ratio for product stress.
    """
    g = df.groupby("signup_month", observed=True)
    out = g.agg(
        cohort_size=("customer_id", "count"),
        retention_proxy=("churned", lambda s: 1.0 - s.mean()),
        avg_mrr_usd=("mrr_usd", "mean"),
        avg_overage_usd=("overage_usd", "mean"),
        avg_churn_risk=("churn_risk", "mean"),
        avg_usage_ratio=("usage_ratio", "mean"),
    ).reset_index()
    out["signup_month"] = out["signup_month"].astype(str)
    return out


def ltv_modeling(df: pd.DataFrame, monthly_discount: float = 0.01) -> dict:
    """
    **Gross monthly revenue per customer**
    - *Formula*: revenue_m = mrr_usd + overage_usd.

    **Gross margin assumption**
    - *Assumption*: 78% gross margin after COGS/support (typical B2B SaaS ballpark).
    - *Formula*: margin_m = 0.78 * revenue_m.

    **Per-customer expected LTV (discounted geometric survival)**
    - Let π_i = churn_risk (used as *monthly churn probability proxy*).
    - *Assumption*: Churn each month is Bernoulli with p = π_i, independent
      (memoryless). Real life: churn hazards vary by month—this is a teaching model.
    - Expected lifetime in months: E[T] = 1 / π_i (mean of Geometric starting at 1).
    - *Undiscounted LTV* (margin per month × expected months):
      `LTV_undisc = margin_m / π_i`.
    - *Discounted LTV* with monthly discount rate d (cost of capital / time value):
      Sum_{t=1..∞} margin_m * (1-π_i)^(t-1) / (1+d)^t
      = margin_m / (π_i + d + π_i*d)  (standard closed form for constant margin).
      We use the closed form with small floor on π to avoid division blowups:
      π' = max(π_i, 0.005).

    **Cohort LTV (back-of-envelope)**
    - Mean of per-customer discounted LTV within each signup_month.

    **Interpretation**
    - Higher π_i shrinks LTV sharply; lowering churn or raising MRR moves LTV linearly
      in margin but nonlinearly in π when π is small.
    """
    revenue_m = df["mrr_usd"].to_numpy() + df["overage_usd"].to_numpy()
    margin_m = 0.78 * revenue_m
    pi = np.clip(df["churn_risk"].to_numpy(), 0.005, 0.95)
    d = monthly_discount
    ltv_disc = margin_m / (pi + d + pi * d)
    ltv_undisc = margin_m / pi

    summary = {
        "monthly_discount_rate_d": d,
        "gross_margin_assumption": 0.78,
        "mean_revenue_m": float(revenue_m.mean()),
        "median_ltv_disc": float(np.median(ltv_disc)),
        "mean_ltv_disc": float(ltv_disc.mean()),
        "p90_ltv_disc": float(np.quantile(ltv_disc, 0.9)),
    }

    df = df.assign(
        revenue_monthly_usd=revenue_m,
        contribution_margin_monthly_usd=margin_m,
        ltv_discounted_usd=ltv_disc,
        ltv_undiscounted_usd=ltv_undisc,
    )

    cohort_ltv = (
        df.groupby("signup_month", observed=True)["ltv_discounted_usd"]
        .mean()
        .reset_index()
        .rename(columns={"ltv_discounted_usd": "mean_ltv_discounted_usd"})
    )
    cohort_ltv["signup_month"] = cohort_ltv["signup_month"].astype(str)

    return {"summary": summary, "cohort_ltv": cohort_ltv, "frame_with_ltv": df}


def churn_prediction(df: pd.DataFrame, sample_for_train: int = 200_000) -> dict:
    """
    **Goal**: Predict `churned` from observable features (no peeking at churn_risk).

    **Features**
    - plan (encoded), geography (encoded), tenure_months, monthly_usage,
      overage_usd, usage_ratio, mrr_usd.

    **Models**
    - LogisticRegression: linear baseline, calibrated coefficients.
    - RandomForestClassifier: nonlinear interactions (plan × usage).

    **Train/test**
    - Stratified 80/20 split on `churned`.
    - *Assumption*: IID rows—ignores correlation within cohort month (fast baseline).

    **Metrics**
    - ROC-AUC, Average Precision (important if churn prevalence is low).

    **Interpretation**
    - Feature importances (RF) show which proxies drive churn in this synthetic world;
      on real data, use SHAP for production explanations.
    """
    work = df if len(df) <= sample_for_train else df.sample(sample_for_train, random_state=42)

    le_plan = LabelEncoder().fit(work["plan"])
    le_geo = LabelEncoder().fit(work["geography"])
    X = pd.DataFrame(
        {
            "plan_code": le_plan.transform(work["plan"]),
            "geo_code": le_geo.transform(work["geography"]),
            "tenure_months": work["tenure_months"],
            "monthly_usage": work["monthly_usage"],
            "overage_usd": work["overage_usd"],
            "usage_ratio": work["usage_ratio"],
            "mrr_usd": work["mrr_usd"],
        }
    )
    y = work["churned"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    log_reg = LogisticRegression(max_iter=200, class_weight="balanced", random_state=42)
    log_reg.fit(X_train_s, y_train)
    p_lr = log_reg.predict_proba(X_test_s)[:, 1]

    rf = RandomForestClassifier(
        n_estimators=120,
        max_depth=12,
        min_samples_leaf=50,
        class_weight="balanced_subsample",
        random_state=42,
        n_jobs=-1,
    )
    rf.fit(X_train, y_train)
    p_rf = rf.predict_proba(X_test)[:, 1]

    def _metrics(name: str, p: np.ndarray) -> dict:
        return {
            "model": name,
            "roc_auc": float(roc_auc_score(y_test, p)),
            "avg_precision": float(average_precision_score(y_test, p)),
        }

    feat_names = list(X.columns)
    importances = pd.Series(rf.feature_importances_, index=feat_names).sort_values(ascending=False)

    report_lr = classification_report(y_test, (p_lr >= 0.5).astype(int), digits=4)
    report_rf = classification_report(y_test, (p_rf >= 0.5).astype(int), digits=4)

    return {
        "metrics": [_metrics("logistic_regression", p_lr), _metrics("random_forest", p_rf)],
        "rf_feature_importance": importances,
        "classification_report_lr": report_lr,
        "classification_report_rf": report_rf,
        "n_train": int(len(X_train)),
        "n_test": int(len(X_test)),
    }


def usage_anomalies(df: pd.DataFrame, sample: int = 400_000) -> dict:
    """
    **Goal**: Flag unusual *monthly_usage* given plan (and optionally geography).

    **Method 1 — Robust z-score within plan**
    - For each plan, compute median m and IQR of usage.
    - *Robust z*: z* = (x - m) / (1.35 * IQR) (approx. comparable to z if normal).
    - Flag if |z*| > 3.5.
    - *Assumption*: Heavy tails—robust stats reduce false positives vs mean/std.

    **Method 2 — Isolation Forest**
    - Features: monthly_usage, usage_ratio, overage_usd, tenure_months (scaled).
    - contamination=0.02 (expect ~2% anomalies—tunable prior).
    - *Interpretation*: multivariate outliers; not causal "incidents".

    **Interpretation**
    - High usage_ratio with moderate absolute usage can still be "normal" for Starter;
      IF captures joint patterns.
    """
    work = df if len(df) <= sample else df.sample(sample, random_state=7)

    z_labels = pd.Series(0, index=work.index, dtype=int)
    for plan, sub in work.groupby("plan", observed=True):
        x = sub["monthly_usage"]
        med = x.median()
        q1, q3 = x.quantile([0.25, 0.75])
        iqr = max(q3 - q1, med * 1e-6)
        z_star = (x - med) / (1.35 * iqr)
        z_labels.loc[sub.index] = (np.abs(z_star) > 3.5).astype(int)

    X_if = work[["monthly_usage", "usage_ratio", "overage_usd", "tenure_months"]].to_numpy()
    X_if = StandardScaler().fit_transform(X_if)
    iforest = IsolationForest(
        n_estimators=200,
        contamination=0.02,
        random_state=42,
        n_jobs=-1,
    )
    pred = iforest.fit_predict(X_if)  # -1 anomaly, 1 inlier

    return {
        "n_scanned": len(work),
        "robust_z_anomaly_rate": float(z_labels.mean()),
        "isolation_forest_anomaly_rate": float((pred == -1).mean()),
        "example_anomalies_robust_z": work.loc[z_labels == 1]
        .nlargest(5, "monthly_usage")[["plan", "monthly_usage", "usage_ratio", "mrr_usd"]]
        .to_string(index=False),
    }


def main() -> int:
    _print_section("STEP 1 — Simulate 2,000,000 customers")
    print(
        "Assumptions are documented in simulate_customers() docstring.\n"
        f"Snapshot date AS_OF = {AS_OF.isoformat()}."
    )
    df = simulate_customers(N_CUSTOMERS)
    print(f"Rows: {len(df):,}, Memory ~ {df.memory_usage(deep=True).sum() / 1e9:.2f} GB (deep estimate).")

    _print_section("STEP 2 — Cohort analysis (by signup_month)")
    cohort_tbl = cohort_analysis(df)
    print(cohort_tbl.tail(12).to_string(index=False))

    _print_section("STEP 3 — LTV modeling (discounted geometric churn)")
    ltv = ltv_modeling(df)
    for k, v in ltv["summary"].items():
        print(f"  {k}: {v}")
    print("\nMean discounted LTV by signup_month (last 8 cohorts):")
    print(ltv["cohort_ltv"].tail(8).to_string(index=False))

    _print_section("STEP 4 — Churn prediction (supervised)")
    churn_res = churn_prediction(df)
    print(f"Train n={churn_res['n_train']:,}, test n={churn_res['n_test']:,} (subsample cap for speed).")
    for m in churn_res["metrics"]:
        print(f"  {m['model']}: ROC-AUC={m['roc_auc']:.4f}, AP={m['avg_precision']:.4f}")
    print("\nRandom Forest feature importances:")
    print(churn_res["rf_feature_importance"].to_string())
    print("\nLogistic regression report (threshold 0.5):")
    print(churn_res["classification_report_lr"])
    print("Random forest report (threshold 0.5):")
    print(churn_res["classification_report_rf"])

    _print_section("STEP 5 — Usage anomaly detection")
    anom = usage_anomalies(df)
    print(f"Scanned n={anom['n_scanned']:,}")
    print(f"Robust z-score anomaly rate: {anom['robust_z_anomaly_rate']*100:.2f}%")
    print(f"Isolation Forest anomaly rate: {anom['isolation_forest_anomaly_rate']*100:.2f}%")
    print("\nExample high-usage rows among robust-z anomalies:")
    print(anom["example_anomalies_robust_z"])

    if SAVE_OUTPUTS:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        cohort_tbl.to_csv(OUT_DIR / "cohort_summary.csv", index=False)
        ltv["cohort_ltv"].to_csv(OUT_DIR / "cohort_ltv.csv", index=False)
        # Optional: avoid writing 2M rows by default
        ltv["frame_with_ltv"].head(50_000).to_csv(OUT_DIR / "sample_customers_with_ltv.csv", index=False)
        print(f"\nWrote CSV summaries to {OUT_DIR}/")

    _print_section("SYNTHESIS — How to read results")
    print(
        """
1. Cohort table: compare retention_proxy and avg_usage_ratio across signup_month.
   Rising usage_ratio with falling retention_proxy suggests "bad fit" vintages.

2. LTV: discounted LTV is sensitive to the monthly churn proxy π_i (churn_risk).
   Changing gross margin or d moves LTV proportionally / structurally as in formulas.

3. Churn models: if RF beats logistic notably, nonlinearities (plan × usage) matter.
   Always calibrate thresholds for your cost matrix (false churn vs missed churn).

4. Anomalies: robust-z is univariate within plan; Isolation Forest finds multivariate
   outliers. Investigate overlap for highest-confidence operational alerts.
"""
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
