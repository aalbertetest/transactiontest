#!/usr/bin/env python3
"""
Simulate 2M SaaS customers and run cohort analysis, LTV modeling,
churn-scoring logic, and usage anomaly detection.

Run: python saas_customer_simulation.py [--rows N] [--seed S]
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass
from typing import Tuple

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ---------------------------------------------------------------------------
# Constants (assumptions documented in module docstring and printouts)
# ---------------------------------------------------------------------------
PLANS = ["starter", "growth", "enterprise"]
GEOGRAPHIES = ["NA", "EU", "APAC", "LATAM", "MEA"]
RNG = np.random.default_rng


def simulate_customers(n: int, seed: int) -> pd.DataFrame:
    """
    Vectorized simulation of n customers.

    Assumptions:
    - Signup dates are uniform between 2019-01-01 and 2025-12-01 (synthetic
      window so cohorts have depth). Real SaaS would use empirical signup
      distributions (often heavy-tailed / seasonal).
    - Plan is drawn from a multinomial; enterprise is rarer. In reality,
      plan correlates with sales motion and company size.
    - Base usage (abstract “units” per month) is lognormal, scaled by plan.
      Lognormal captures right-skewed usage common in SaaS.
    - Overages are a fraction of usage above an implicit allowance, with
      noise—proxy for metered billing.
    - Churn risk is a *latent* score used to label synthetic “churned” for
      modeling demos; we then expose noisy observables. Real churn is
      observed departure, not a field in a CRM.
    """
    rng = RNG(seed)

    # Signup: integer days since epoch for memory, convert at end
    start = np.datetime64("2019-01-01")
    end = np.datetime64("2025-12-01")
    days_span = (end - start).astype("timedelta64[D]").astype(int)
    signup_day_offset = rng.integers(0, days_span + 1, size=n, dtype=np.int32)
    signup = start + signup_day_offset.astype("timedelta64[D]")

    # Plan probabilities skew toward starter
    plan_probs = np.array([0.55, 0.30, 0.15], dtype=np.float64)
    plan_idx = rng.choice(3, size=n, p=plan_probs).astype(np.int8)
    plan_scale = np.array([1.0, 3.5, 12.0], dtype=np.float64)  # usage multiplier

    # Geography independent of plan for simplicity (often correlated IRL)
    geo_probs = np.array([0.45, 0.28, 0.15, 0.08, 0.04], dtype=np.float64)
    geo_idx = rng.choice(5, size=n, p=geo_probs).astype(np.int8)

    # Monthly usage ~ lognormal, scaled by plan
    log_mu = np.log(50.0) + np.log(plan_scale[plan_idx])
    log_sigma = 0.65
    usage = rng.lognormal(mean=log_mu, sigma=log_sigma, size=n).astype(np.float32)

    # Implicit monthly allowance by plan (units); overage = max(0, usage - cap) * noise
    allowance = np.array([80.0, 250.0, 800.0], dtype=np.float64)[plan_idx]
    raw_overage = np.maximum(usage.astype(np.float64) - allowance, 0.0)
    overage = (raw_overage * rng.uniform(0.85, 1.15, size=n)).astype(np.float32)

    # Latent churn propensity: higher with low usage relative to plan, high overage,
    # certain geos (synthetic effect), and random frailty
    usage_ratio = usage.astype(np.float64) / (allowance * 0.4 + 1e-6)
    geo_churn_effect = np.array([0.0, 0.15, 0.1, 0.2, 0.25], dtype=np.float64)[geo_idx]
    linear_score = (
        -0.8 * np.log1p(usage_ratio)
        + 0.002 * overage.astype(np.float64)
        + 0.4 * (plan_idx == 0).astype(np.float64)
        + geo_churn_effect
        + rng.normal(0, 0.35, size=n)
    )
    churn_risk = 1.0 / (1.0 + np.exp(-linear_score))  # logistic transform to (0,1)
    churn_risk = np.clip(churn_risk, 0.001, 0.999).astype(np.float32)

    # Observed churn label for supervised learning: Bernoulli draw using churn_risk
    churned = (rng.random(n) < churn_risk).astype(np.int8)

    df = pd.DataFrame(
        {
            "customer_id": np.arange(n, dtype=np.int64),
            "signup_date": signup.astype("datetime64[ns]"),
            "plan": pd.Categorical.from_codes(plan_idx, categories=PLANS),
            "geography": pd.Categorical.from_codes(geo_idx, categories=GEOGRAPHIES),
            "monthly_usage": usage,
            "overages": overage,
            "churn_risk_score": churn_risk,
            "churned": churned,
        }
    )
    return df


def cohort_retention_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cohort analysis: aggregate by signup month (signup_cohort).

    Each row is one customer at a synthetic cross-section. We group by calendar
    month of signup_date and report:

    - customers: cohort size N
    - churn_rate: (1/N) * sum(churned) — fraction labeled churned in the snapshot
    - avg_usage, avg_overages, avg_churn_risk: cohort means

    This is *not* classic retention R(c, m) = active at period m / cohort size,
    because we do not have panel subscription history. For true R(c, m) you need
    event data (renewals/cancellations) per customer-month.

    Formula used here: churn_rate(cohort) = mean_i churned_i for i in cohort.
    """
    df = df.copy()
    df["signup_cohort"] = df["signup_date"].dt.to_period("M")

    cohort_stats = (
        df.groupby("signup_cohort", observed=True)
        .agg(
            customers=("customer_id", "count"),
            churn_rate=("churned", "mean"),
            avg_usage=("monthly_usage", "mean"),
            avg_overages=("overages", "mean"),
            avg_churn_risk=("churn_risk_score", "mean"),
        )
        .reset_index()
    )
    cohort_stats["signup_cohort"] = cohort_stats["signup_cohort"].astype(str)
    return cohort_stats


def ltv_model(df: pd.DataFrame, monthly_margin: float = 0.72) -> Tuple[pd.DataFrame, dict]:
    """
    Simple LTV model (contract / heuristic):

    Assumptions:
    - Average revenue per user (ARPU) by plan from a fixed tariff table
      (synthetic). Real LTV uses historical ARPU, discounts, expansion, support cost.
    - Gross margin `monthly_margin` applies uniformly (default 72%).
    - Expected lifetime in months L = 1 / monthly_churn_probability at cohort level
      or individual level. Relationship: if churn probability per month is p,
      mean geometric lifetime E[T] = 1/p months (discrete time), for small p.

    Formula (per customer i):
        margin_i = ARPU(plan_i) * monthly_margin
        L_i = 1 / max(churn_risk_score_i, epsilon)   # risk score as proxy for p
        LTV_i = margin_i * L_i

    Interpretation: higher churn risk shrinks expected lifetime; higher plan
    raises ARPU. This is a *structural* shortcut, not a causal model—churn_risk
    was simulated from usage; circularity is acceptable for synthetic demo only.

    For cohort LTV we aggregate mean(LTV) by signup_cohort.
    """
    arpu_by_plan = {"starter": 29.0, "growth": 99.0, "enterprise": 499.0}
    eps = 0.02

    df = df.copy()
    df["arpu"] = df["plan"].map(arpu_by_plan).astype(np.float32)
    df["monthly_margin_dollars"] = df["arpu"] * monthly_margin
    # Expected lifetime from risk score treated as monthly churn probability
    df["expected_lifetime_months"] = 1.0 / np.maximum(df["churn_risk_score"].astype(np.float64), eps)
    df["ltv_estimate"] = df["monthly_margin_dollars"] * df["expected_lifetime_months"]

    summary = {
        "monthly_margin_assumption": monthly_margin,
        "arpu_by_plan": arpu_by_plan,
        "mean_ltv": float(df["ltv_estimate"].mean()),
        "median_ltv": float(df["ltv_estimate"].median()),
        "total_implied_ltv": float(df["ltv_estimate"].sum()),
    }

    cohort_ltv = (
        df.assign(signup_cohort=df["signup_date"].dt.to_period("M"))
        .groupby("signup_cohort", observed=True)
        .agg(mean_ltv=("ltv_estimate", "mean"), median_ltv=("ltv_estimate", "median"))
        .reset_index()
    )
    cohort_ltv["signup_cohort"] = cohort_ltv["signup_cohort"].astype(str)
    return cohort_ltv, summary


def churn_prediction(df: pd.DataFrame, seed: int, max_fit_rows: int = 400_000) -> dict:
    """
    Churn prediction: logistic regression on features.

    Features: monthly_usage, overages, plan (one-hot), geography (one-hot).
    Target: churned.

    Steps:
    1. Optional stratified subsample for fitting when len(df) > max_fit_rows (speed).
    2. Train/test split stratified on churned
    3. Standardize continuous features (fit on train only)
    4. Fit LogisticRegression with L2, class_weight='balanced' to handle imbalance
    5. Report AUC, coefficients (interpret as log-odds change per 1 SD feature)

    Formula (logistic model):
        P(churn=1|x) = sigmoid(w^T x + b)
        sigmoid(z) = 1 / (1 + exp(-z))

    Interpretation: positive coefficient on overages → higher overage associated
    with higher churn probability holding other features fixed (association, not
    necessarily causal).
    """
    work = df
    subsampled = False
    if len(df) > max_fit_rows:
        work, _ = train_test_split(
            df,
            train_size=max_fit_rows,
            stratify=df["churned"],
            random_state=seed,
        )
        subsampled = True

    feature_df = pd.get_dummies(
        work[["monthly_usage", "overages", "plan", "geography"]],
        columns=["plan", "geography"],
        drop_first=True,
    )
    X = feature_df.to_numpy(dtype=np.float64)
    y = work["churned"].to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed, stratify=y
    )

    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    clf = LogisticRegression(
        max_iter=200,
        class_weight="balanced",
        random_state=seed,
        solver="lbfgs",
    )
    clf.fit(X_train_s, y_train)

    proba = clf.predict_proba(X_test_s)[:, 1]
    auc = roc_auc_score(y_test, proba)

    coefs = dict(zip(feature_df.columns, clf.coef_.ravel()))
    intercept = float(clf.intercept_[0])

    # High-risk bucket: top decile of predicted probability on the same frame used for training fit
    X_all_s = scaler.transform(feature_df.to_numpy(dtype=np.float64))
    p_all = clf.predict_proba(X_all_s)[:, 1]
    threshold = np.quantile(p_all, 0.9)
    high_risk_count = int((p_all >= threshold).sum())

    return {
        "roc_auc_holdout": float(auc),
        "intercept_log_odds": intercept,
        "coefficients_on_scaled_features": coefs,
        "high_risk_decile_threshold": float(threshold),
        "customers_flagged_high_risk_top_decile": high_risk_count,
        "n_train": int(len(y_train)),
        "n_test": int(len(y_test)),
        "churn_model_subsampled_to_rows": int(len(work)) if subsampled else int(len(df)),
        "subsampled_for_speed": subsampled,
    }


def usage_anomaly_detection(df: pd.DataFrame, z_threshold: float = 3.5) -> Tuple[pd.DataFrame, dict]:
    """
    Usage anomaly detection: robust z-score within (plan, geography) cells.

    Steps:
    1. For each (plan, geography), compute median m and MAD of monthly_usage.
    2. Robust z: z* = 0.6745 * (x - m) / MAD  (factor makes MAD comparable to SD
       for Normal data).

    Assumption: within segment, “typical” usage is symmetric-ish around median;
    heavy tails handled better than raw z-score.

    Flag anomaly if |z*| > z_threshold (default 3.5).

    Interpretation: flagged customers are extreme *relative to peers* in same
    plan and region—could be abuse, misconfiguration, or upsell opportunity
    (enterprise-like usage on starter plan).
    """
    def robust_z(group: pd.Series) -> pd.Series:
        x = group.astype(np.float64)
        med = np.median(x)
        mad = np.median(np.abs(x - med))
        if mad < 1e-9:
            mad = 1e-9
        return 0.6745 * (x - med) / mad

    df = df.copy()
    df["usage_robust_z"] = df.groupby(["plan", "geography"], observed=True)["monthly_usage"].transform(
        robust_z
    )
    df["usage_anomaly"] = (np.abs(df["usage_robust_z"]) > z_threshold).astype(np.int8)

    stats = {
        "z_threshold": z_threshold,
        "anomaly_count": int(df["usage_anomaly"].sum()),
        "anomaly_rate": float(df["usage_anomaly"].mean()),
    }
    anomalies = df.loc[df["usage_anomaly"] == 1, ["customer_id", "plan", "geography", "monthly_usage", "usage_robust_z"]].head(
        20
    )
    return anomalies, stats


def main() -> int:
    parser = argparse.ArgumentParser(description="Simulate SaaS customers and run analyses.")
    parser.add_argument("--rows", type=int, default=2_000_000, help="Number of customers")
    parser.add_argument("--seed", type=int, default=42, help="RNG seed")
    args = parser.parse_args()
    n = args.rows
    seed = args.seed

    print("=" * 72)
    print("STEP 0 — Simulation design")
    print("=" * 72)
    print(
        """
We simulate each row as one customer at a *cross-sectional* observation date.

Fields:
- signup_date: uniform over 2019–2025 (synthetic calendar depth for cohorts).
- plan: multinomial(starter/growth/enterprise) with enterprise rare.
- geography: multinomial across five regions.
- monthly_usage: lognormal, scale depends on plan (higher tiers use more).
- overages: positive when usage exceeds a plan-specific allowance, with jitter.
- churn_risk_score: logistic function of (low usage vs allowance, overages,
  starter plan indicator, region effects, noise). Values in (0,1), interpretable
  as a *synthetic propensity*, not observed in production.
- churned: Bernoulli draw with probability = churn_risk_score (so risk aligns
  with labels for ML demo).

Memory: categoricals + float32 where possible for ~2M rows.
"""
    )

    print(f"\nGenerating {n:,} customers (seed={seed})…")
    df = simulate_customers(n, seed)
    print(f"DataFrame shape: {df.shape}, memory ~{df.memory_usage(deep=True).sum() / 1e6:.1f} MB")

    print("\n" + "=" * 72)
    print("STEP 1 — Cohort analysis")
    print("=" * 72)
    print(
        """
Definition: signup_cohort = first day of calendar month of signup_date.

Metrics per cohort:
- customers: cohort size
- churn_rate: fraction with churned==1 (snapshot churn; not survival-based churn
  by tenure without event history)
- avg_usage, avg_overages, avg_churn_risk: descriptive

Interpretation: improving later cohorts (lower churn_rate, higher usage) might
suggest better PMF or product maturity—*but* here confounded by calendar time
and synthetic data generation.

Formula highlighted: churn_rate(cohort) = (1/N) * sum_i churned_i for i in cohort.
"""
    )
    cohort = cohort_retention_analysis(df)
    print(cohort.tail(12).to_string(index=False))

    print("\n" + "=" * 72)
    print("STEP 2 — LTV modeling")
    print("=" * 72)
    print(
        """
Model type: simplified *margin × expected lifetime*.

Assumptions:
- ARPU fixed by plan (starter $29, growth $99, enterprise $499) — placeholder.
- Gross margin ratio 72% applied to ARPU to get monthly contribution margin.
- Expected lifetime L = 1 / max(churn_risk_score, 0.02). Treating risk score as
  monthly churn probability p gives mean survival 1/p under geometric model.

LTV_i = monthly_margin_dollars_i * L_i

Caveat: churn_risk_score was built from the same features as usage; LTV uses it
directly, so do not treat as independent forecast in real life—replace with
predicted churn from a model held out in time.

Interpretation: cohort mean_ltv rising suggests higher-value signups over time
(in this synthetic world, noise dominates unless n is huge).
"""
    )
    cohort_ltv, ltv_summary = ltv_model(df)
    print("Global LTV summary:", ltv_summary)
    print("\nCohort LTV (last 8 cohorts):")
    print(cohort_ltv.tail(8).to_string(index=False))

    print("\n" + "=" * 72)
    print("STEP 3 — Churn prediction (supervised)")
    print("=" * 72)
    print(
        """
Algorithm: logistic regression with standardized numeric inputs + one-hot
categoricals. class_weight='balanced' adjusts for churn imbalance.

Evaluation: ROC-AUC on 20% stratified holdout.

Operational rule: flag customers in top decile of predicted churn probability
for proactive outreach.

Interpretation of coefficients: on the *standardized* scale, a one-unit change
in a feature (one standard deviation) shifts log-odds of churn by beta; odds
multiply by exp(beta) per +1 SD.
"""
    )
    churn_out = churn_prediction(df, seed)
    print(f"Holdout ROC-AUC: {churn_out['roc_auc_holdout']:.4f}")
    print(f"Intercept (log-odds): {churn_out['intercept_log_odds']:.4f}")
    print(f"High-risk decile threshold p>={churn_out['high_risk_decile_threshold']:.4f} "
          f"→ {churn_out['customers_flagged_high_risk_top_decile']:,} customers")
    sel = list(churn_out["coefficients_on_scaled_features"].items())[:8]
    print("Coefficients (selected):", {k: round(float(v), 4) for k, v in sel})

    print("\n" + "=" * 72)
    print("STEP 4 — Usage anomaly detection")
    print("=" * 72)
    print(
        """
Method: robust z-score per (plan, geography) using median and MAD.

Robust z* = 0.6745 * (x - median) / MAD

Flag if |z*| > threshold (default 3.5). 0.6745 makes MAD comparable to standard
deviation for Gaussian tails.

Interpretation: anomalies are *contextual*—high usage on enterprise in NA may
be normal while the same absolute usage on starter in MEA is anomalous.
"""
    )
    anomalies, ad_stats = usage_anomaly_detection(df)
    print("Anomaly detection summary:", ad_stats)
    print("\nSample anomalous customers (up to 20):")
    print(anomalies.to_string(index=False))

    print("\n" + "=" * 72)
    print("Done.")
    print("=" * 72)
    return 0


if __name__ == "__main__":
    sys.exit(main())
