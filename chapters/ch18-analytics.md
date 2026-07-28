# Chapter 18 — Audit Data Analytics

> An analytic is not a chart. It is a prediction. Before you run a query you must be able to say what number you
> expect, where that expectation comes from, how wrong it could be, and how large a difference you will refuse to
> accept without a corroborated explanation. Defective analytics work rarely fails on the code; it fails because
> nobody wrote the expectation down, nobody derived the threshold, and nobody tested the input data.

## Learning Objectives

- **LO 18.1** Distinguish descriptive, diagnostic, predictive, and prescriptive analytics and the audit use each
  is suited to.
- **LO 18.2** Distinguish the three roles an analytic can play — risk assessment procedure, substantive analytical
  procedure, and full-population test of details — and the evidentiary requirements of each.
- **LO 18.3** Design an expectation for SaaS subscription revenue from operational data and evaluate it against the
  four elements of a valid expectation.
- **LO 18.4** Derive a threshold for investigation from performance materiality and defend the range within which
  it could reasonably fall.
- **LO 18.5** Compute the ARR waterfall, the ARR-to-revenue bridge, the billings bridge, and the three-way
  reconciliation, and conclude which can carry substantive evidence.
- **LO 18.6** Decompose a change in net revenue retention and in days sales outstanding into dollars.
- **LO 18.7** Evaluate the completeness and accuracy of the data used in an analytic.
- **LO 18.8** Design an outlier rule set that controls the false-positive rate, and evaluate a Benford's law test
  on a subscription population.
- **LO 18.9** Document an analytic so a reviewer can re-perform it, and conclude on its effect on planned sample
  sizes and on the sufficiency of audit evidence.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2305, *Substantive Analytical Procedures* | Develop an expectation, fix the difference acceptable without investigation, compare, and investigate significant differences. |
| PCAOB | AS 2110 and AS 2401 | Analytics are a required risk assessment procedure; revenue analytics and evaluation of unusual relationships are required in the fraud response. |
| PCAOB | AS 1105 | Reliability of information used as evidence, including information produced by the company; requires testing accuracy and completeness. |
| PCAOB | AS 2810 and AS 1215 | Overall review analytics near the end of the audit; documentation must let an unconnected experienced auditor re-perform the work. |
| AICPA | AU-C 520, AU-C 315, AU-C 500, AU-C 240, AU-C 230 | Analogues of the above; AU-C 520 states the data-reliability requirement more directly. |
| FASB / SEC | ASC 606-10 (incl. 606-10-50); ASC 326-20; Item 303 of Regulation S-K and the 2020 MD&A key-performance-indicator guidance; AS 2710 / AU-C 720 | What the recorded amount should be; management's disclosed disaggregation is a starting point for, not a substitute for, the auditor's. ARR and NRR sit in the Form 10-K as other information. |

All standards cited are in force for the year ended December 31, 2025.

## Prerequisites and Chapter Dependencies

Read Chapter 3 (materiality) first, because every threshold here derives from its $940 performance materiality
figure; Chapters 5 and 6, which own the revenue and deferred revenue subject matter the analytics predict; and
Chapter 12, which owns the reliability of the Snowflake extracts. Chapter 15 owns sampling and Chapter 16 journal
entry analytics; this chapter defers to both. Chapters 7, 10, and 19 build on the receivable, payroll, and
final-review analytics developed here.

## 18.1 What an Analytic Is, and the Four Families

An **audit data analytic** is the application of a computational technique to a population of data to produce
audit evidence. The definition turns on purpose, not tooling: a two-column comparison in Excel is an analytic if
it produces evidence, and a thirty-panel dashboard is not if it does not.

**Exhibit 18-1. The four families of analytics mapped to audit uses (AtlasFlow FY2025 examples).**

| Family | Question | AtlasFlow example | Audit use, and the limit |
| --- | --- | --- | --- |
| Descriptive | What happened? | Revenue by stream by quarter (§3.1); the aged trial balance | Risk assessment and population profiling. No substantive assurance — it restates rather than predicts |
| Diagnostic | Why? | Decomposing the NRR decline from 118% to 112% into expansion, contraction, and churn | Risk assessment and difference investigation. A driver that explains a difference is not corroboration |
| Predictive | What should the number be? | Expected monthly Core revenue = average paid seats × average price per seat | **Substantive analytical procedure** — the only family carrying substantive evidence alone. Blind to misstatement below its achieved precision |
| Prescriptive | What do we do about it? | Ranking 4,912 manual journal entries to select 60 | Directs effort. A selection rule tests nothing until you test what it selects |

Labelling a descriptive or diagnostic analytic a substantive analytical procedure is the most common defect in this
area of the file.

## 18.2 The Three Roles an Analytic Can Play

The same query can serve three purposes, and the requirements differ so sharply that conflating them is the source of
most defective analytics work.

**Exhibit 18-2. The three roles an analytic can play.**

| Attribute | Risk assessment procedure | Substantive analytical procedure | Test of details, full population |
| --- | --- | --- | --- |
| Governing standard | AS 2110 / AU-C 315 | AS 2305 / AU-C 520 | AS 1105 / AU-C 500 |
| Required? | Yes | No; audit strategy | No; audit strategy |
| Precision required | Low — enough to flag something | High — below the threshold | N/A; you recompute |
| Independent expectation? | No | **Yes** | No |
| Data reliability | Source may be unaudited | C&A tested | C&A tested |
| AtlasFlow application | ARR bridge (§18.5); DSO decomposition (§18.9) | Monthly Core revenue from seats and price (§18.4); cohort test (§18.7) | Deferred revenue roll-forward (§18.6); all 3,140 enterprise revenue schedules |
| What a "pass" gets you | Documented conclusion that nothing further was identified | Substantive evidence over named assertions at a stated assurance level | Substantive evidence with no sampling risk |
| What a "fail" gets you | A risk requiring a response | An unexplained difference, or a misstatement | A misstatement quantified without projection |

The practical test is one question: *did I predict the number from something other than the number itself?* A
schedule of Core revenue of 24,100, 25,700, 26,900, and 28,200 across FY2025 quarters (§3.1) restates the general
ledger; it becomes a substantive analytical procedure only when those four numbers are predicted from independently
obtained seats, prices, and contract dates. Note the third column: a full-population recomputation is a **test of
details** even in SQL, so AS 2305 does not apply while AS 1105 applies in full.

## 18.3 The Requirements for a Substantive Analytical Procedure

### 18.3.1 The four elements of a valid expectation

AS 2305 and AU-C 520 both require an expectation precise enough to identify a misstatement that, alone or with
others, could be material. Four elements must be present: **an independent and reliable source** (outside the account
tested, C&A tested — §18.13); **disaggregation** to the level at which the relationship holds; **precision** smaller
than the threshold, the element that fails most often (§18.3.2); and **a predictable relationship** grounded in the
business and stable over the period.

**Exhibit 18-3. The four elements applied to Core subscription revenue, FY2025.**

| Element | How it is satisfied | Where it could break |
| --- | --- | --- |
| Independent source | Paid seats from Zuora rate-plan charges and the provisioning database; prices from the Salesforce CPQ price book | The extract sits in the Snowflake datamart, unreconciled to the GL for three quarters (W-11) |
| Disaggregation | Monthly, Core only | Aggregating Core with Insight: Insight launched January 2025 with no comparative |
| Precision | Monthly dispersion of $22 implies ±$45 monthly and ±$152 annually against a $135 threshold | A single annual average degrades precision to about ±$600 |
| Predictable relationship | Core is priced per seat per month and recognized straight-line, so seats × price × months *is* the revenue model | Ramped contracts (34% of ACV) and the April 8% increase with one-cycle grandfathering perturb price |

### 18.3.2 Why most failed analytics fail on precision, demonstrated numerically

Core subscription revenue for FY2025 was **$104,900** (account 4100); for FY2024, Core was **$105,500** and usage
overage **$2,800**, together the $108,300 of FY2024 subscription revenue. (That split extends the continuing case.)
Four auditors could build four expectations for the FY2025 figure.

**Exhibit 18-4. Four expectations for the same account (in thousands).**

| # | Basis of expectation | Expected | Actual | Difference | Precision | Detects $940? |
| --- | --- | --- | --- | --- | --- | --- |
| E1 | FY2024 Core of $105,500 grown at the 25.4% FY2025 subscription growth rate | 132,300 | 104,900 | (27,400) | ±$14,000 | No |
| E2 | FY2024 Core rebased for management's $12,600 Insight reclassification, grown at management's 12.8% budget: $92,900 × 1.128 | 104,800 | 104,900 | 100 | ±$4,000 | No |
| E3 | FY2025 average seats of 251.1 thousand × average price of $34.75 × 12 | 104,709 | 104,900 | 191 | ±$600 | No |
| E4 | Sum over twelve months of (monthly average seats × monthly average price) | 104,770 | 104,900 | 130 | ±$152 | **Yes** |

E1 fails on predictability: the January 2025 unbundling moved revenue out of Core, so Core fell 0.6% while
subscription revenue grew 25.4%. E3 fails on parameter sensitivity — a $0.10 error in average price moves the
expectation by $301, and the $34.10–$35.45 monthly range makes ±$0.20 unavoidable.

E2 is the dangerous one. Its difference is the smallest of the four, and a reviewer sees $100 against $940 of
performance materiality and signs off. But both of E2's parameters come from management, so it would have produced a
$100 difference whether or not revenue was misstated. **A small difference from an imprecise expectation is not
evidence.** The general rule is an inequality:

```text
achieved precision  <  threshold for investigation  <=  tolerable difference  <=  performance materiality
```

If achieved precision exceeds the threshold, a difference below the threshold is indistinguishable from a material
misstatement masked by imprecision. E3 fails: with ±$600 of precision against a $470 tolerable difference, a $940
misstatement confined to one month is entirely consistent with the $191 observed.

### 18.3.3 The threshold for investigation and how to set it from performance materiality

Performance materiality for the FY2025 AtlasFlow audit is **$940** and overall materiality is **$1,450**
(Chapter 3). The threshold is derived in three moves.

**Exhibit 18-5. Threshold derivation for the Core subscription revenue analytic (in thousands).**

| Step | Computation | Result | Judgment range and what would move it |
| --- | --- | --- | --- |
| 1. Start from performance materiality | Chapter 3 | 940 | An input, not a judgment |
| 2. Choose the share of assurance the analytic carries (k) | k × 940 | k = 0.50 → **470** tolerable difference | Practice ranges from k = 0.10 (corroborative) to k = 0.75 (primary substantive procedure); 0.50 here because tests of details over the December cut-off population and the 47 RevPro overrides carry the balance. Ineffective revenue controls push k toward 0.20; a clean control conclusion supports 0.65 |
| 3. Adjust for disaggregation into n = 12 monthly cells | 470 ÷ √12 = 135.7 | **135** monthly threshold | √n assumes monthly differences are largely independent. Conservative alternative 470 ÷ 12 = $39; looser, 2% of the monthly balance ($175–$190) |

Two rules keep this honest. **Set the threshold before you compute the difference.** And **the threshold is not
performance materiality**; using $940 unallocated for every analytic is the defect that hides the misstatement in
the extended case study. Because Core and Insight cover disjoint populations whose unexplained differences are
accumulated at completion (Chapter 19), 50% of performance materiality for each does not double-count; performance
materiality for each would.

### 18.3.4 The investigation of differences

AS 2305 is explicit that investigating a difference means obtaining *corroborated* explanations — not
management's explanation, and not a plausible narrative the auditor constructs. Apply a four-part sequence to
every difference over the threshold.

1. **Quantify the difference** and confirm it is real, not a units, sign, or period-boundary artifact in your query.
2. **Test your own expectation first.** Most differences over the threshold are defects in the auditor's independent
   data; both December items in the walkthrough are of this kind.
3. **Obtain an explanation and corroborate it independently of the person who gave it.** An explanation accounting
   for $118 of a $180 difference has explained $118, not $180.
4. **Conclude on the residual.** Below the $72 clearly trivial threshold, document and move on; above $72 but below
   the threshold, accumulate it; still above it, extend the procedure or conclude a misstatement exists.

Concentration is the signal. A difference that grows rather than shrinks as you disaggregate, or that sits in one
period, segment, or entity, is the unexpected result to look for: $780 spread evenly over twelve months is usually
a modelling error, while the same $780 in three consecutive months at one entity is usually a misstatement.

## 18.4 Developing an Expectation for SaaS Subscription Revenue from Operational Data

SaaS is unusually favourable ground for substantive analytical procedures because the revenue model is arithmetic:
a committed number of seats at a contracted price for a contracted term, recognized ratably. Four independent
operational sources are available. Paid automation seats from Zuora Billing, corroborated to the provisioning
database, support the monthly Core expectation at ±$45 per month on a $9,000 balance. Cohort customer counts from
Salesforce and Stripe support the §18.7 cohort test and the case study's attach-rate analytic. The ARR waterfall from
the Snowflake datamart supports only the low-precision bridge in §18.5. Workflow run volumes from platform telemetry
support the usage overage expectation and the §18.10 hosting unit economics. For each month, expected Core revenue
equals the month's average paid seat count times its average contracted price per seat:

```sql
-- Independent expectation for Core subscription revenue by month, FY2025.
-- Source: Zuora rate-plan charges replicated to Snowflake (I-8). Touches no REVPRO_* or GL table.
WITH daily_seats AS (
    SELECT  d.calendar_date,
            SUM(rpc.quantity)                              AS paid_seats,
            SUM(rpc.quantity * rpc.mrr_per_unit)           AS contracted_mrr
    FROM    RAW.ZUORA.RATE_PLAN_CHARGE_DAILY rpc
    JOIN    REF.DIM_DATE d
              ON d.calendar_date BETWEEN rpc.effective_start_date
                                     AND COALESCE(rpc.effective_end_date, DATE '9999-12-31')
    WHERE   rpc.product_code IN ('CORE-SEAT','CORE-SEAT-RAMP','CORE-SEAT-KESTREL')   -- see 18.13
      AND   rpc.charge_type   = 'Recurring'
      AND   rpc.subscription_status IN ('Active','Cancelled')  -- cancelled mid-period still earns revenue
      AND   d.calendar_date BETWEEN DATE '2025-01-01' AND DATE '2025-12-31'
    GROUP BY d.calendar_date
)
SELECT  DATE_TRUNC('month', ds.calendar_date)                        AS fiscal_month,
        ROUND(AVG(ds.paid_seats) / 1000.0, 1)                        AS avg_paid_seats_000,
        ROUND(AVG(ds.contracted_mrr) / AVG(ds.paid_seats), 2)        AS avg_price_per_seat,
        ROUND(AVG(ds.contracted_mrr) / 1000.0, 0)                    AS expected_revenue_000
FROM    daily_seats ds
GROUP BY 1
ORDER BY 1;
```

Three design points are where practitioners go wrong. The seat count is a **daily average**, not a month-end snapshot,
which overstates seats in a growing book. `subscription_status` includes `Cancelled`, because a subscription cancelled
on December 20 still earned twenty days of revenue. And the `product_code` filter is the largest completeness risk;
§18.13 shows one omitted code moving December by $118.

## 18.5 The ARR-to-Revenue Bridge

Annual recurring revenue is a point-in-time run rate, not a revenue measure, and the bridge between the two is the
most requested and most misunderstood analytic on a SaaS engagement. Build the waterfall first.

**Exhibit 18-6. ARR waterfall, FY2025 (in thousands).**

| Component | Amount | Note |
| --- | --- | --- |
| ARR at December 31, 2024 | 137,400 | §1.4 |
| Less: self-serve ARR at December 31, 2024 | (5,400) | Outside the retention cohort (Chapter 3) |
| **Retention cohort denominator** | **132,000** | |
| Expansion ARR | 27,720 | 21.0% |
| Contraction ARR | (7,410) | (5.6)% |
| Gross churn ARR | (4,470) | (3.4)% |
| **Cohort closing ARR (NRR numerator)** | **147,840** | ÷ 132,000 = **112.0%** |
| New logo ARR — enterprise and mid-market | 14,460 | 612 first-time Zuora subscriptions |
| Kestrel Labs acquired ARR | 2,100 | Migrated October 2025 (§1.6) |
| Self-serve ARR at December 31, 2025 | 7,600 | 11,400 accounts |
| **ARR at December 31, 2025** | **172,000** | §1.4 |

Two checks fall out at no cost. Gross retention is (132,000 − 7,410 − 4,470) ÷ 132,000 = **91.0%**, agreeing with the
disclosure. And $172,000 is the *corrected* closing ARR: Chapter 12 established four defects in
`REVOPS.MART.V_ARR_MONTHLY` and five corrections reducing the draft 10-K figure of $175,900. **Never run an ARR
bridge on the pre-correction figure.** Q4 2025 recurring revenue was Core $28,200 plus Insight $7,800 = $36,000.

**Exhibit 18-7. ARR-to-revenue bridge at December 31, 2025 (in thousands).**

| Line | Amount | Tick |
| --- | --- | --- |
| Recurring subscription revenue recognized, Q4 2025 | 36,000 | (a) |
| Annualized (× 4) | 144,000 | |
| Reported ARR at December 31, 2025 | 172,000 | (b) |
| **Gap requiring explanation** | **28,000** | |
| Explained by: ARR on subscriptions contracted at 12/31/25 with service commencement after 12/31/25 | 15,700 | (c) |
| Explained by: annualization effect for subscriptions that went live during Q4 (revenue is a partial quarter; ARR is the full run rate) | 8,100 | (d) |
| Explained by: contra-revenue in account 4900 netted against Q4 revenue but not deducted from ARR | 1,900 | (e) |
| Explained by: Kestrel ARR at the full run rate but recognized only from the October migration | 900 | (f) |
| **Subtotal explained** | **26,600** | |
| **Unexplained residual** | **1,400** | |

Tick marks: (a) §3.1. (b) §1.4, agreed to the corrected ARR schedule. (c) Zuora extract with
`contract_effective_date <= 2025-12-31` and `service_activation_date > 2025-12-31`; 341 subscriptions.
(d) Recomputed from daily seat data as Q4 average MRR × 4 less December MRR × 12. (e) Account 4900 per §2.3.
(f) $2,100 acquired ARR less $1,200 annualized Q4 Kestrel revenue.

The $1,400 residual exceeds performance materiality of $940, and it would be a mistake to treat that as a finding.
Items (c), (d), and (f) are estimates whose tolerances the team assessed in combination at roughly **±$1,900** — four
times the $470 tolerable difference, so the §18.3.2 inequality fails badly. **The ARR-to-revenue bridge cannot be a
substantive analytical procedure.** Documented under AS 2110 it still does useful work: it confirms the disclosed
metric and recorded revenue move together for nameable reasons, and it would flag an ARR figure sweeping in
professional services. It cannot detect $940, and the workpaper must say so. Had the residual been $6,000, the next
step is not a fifth reconciling item but to obtain the ARR logic and re-perform it against the MD&A definition.

## 18.6 The Billings and Deferred Revenue Bridges, and the Three-Way Reconciliation

Unlike the ARR bridge, the deferred revenue roll-forward is an **identity**. Every term is an amount somebody
recorded, which makes it a full-population test of details rather than a prediction — precise to the dollar, with
no expectation and no threshold.

**Exhibit 18-8. The deferred revenue roll-forward as an analytic identity, FY2025 (in thousands).**

| Term | Amount | Source |
| --- | --- | --- |
| Deferred revenue at January 1, 2025 | 62,300 | §3.2; prior-year audited balance |
| Add: billings, net of credits | 163,750 | Zuora invoice register, tested for completeness |
| Add: deferred revenue acquired with Kestrel | 610 | §1.6; purchase accounting |
| Add: foreign currency translation | (260) | Consolidation workbook |
| Less: deferred revenue at December 31, 2025 | (78,200) | Accounts 2400 + 2405 + 2410 = 66,800 + 4,500 + 6,900 |
| **Implied total revenue** | **148,200** | |
| Total revenue per the statement of operations | 148,200 | §1.4 |
| **Difference** | **—** | |

The identity ties exactly, and run in reverse it gives the billings bridge: revenue of $148,200 plus the deferred
revenue movement of $15,900, less the $610 acquired and plus the $260 of translation, equals $163,750 of billings —
the disclosed figure.

One warning. AtlasFlow's §3.2 roll-forward keeps unbilled contract assets inside the same subledger, so no separate
term appears for their movement; where they sit outside it the identity needs one, and at AtlasFlow contract assets
rose from $2,100 to $3,400, so it would be $(1,300). **A bridge that misses by exactly the contract asset movement
has omitted this term.** Extending the identity to cash produces the three-way reconciliation.

**Exhibit 18-9. Three-way reconciliation of revenue, receivables, and cash, FY2025 (in thousands).**

| Line | Amount | Derivation |
| --- | --- | --- |
| Gross accounts receivable at January 1, 2025 | 30,500 | $29,150 net + $1,350 allowance |
| Add: billings | 163,750 | Per Exhibit 18-8 |
| Less: write-offs charged against the allowance | (1,230) | $1,350 + $1,780 provision − $1,900 closing |
| Less: gross accounts receivable at December 31, 2025 | (38,600) | §3.3 |
| **Expected cash receipts from customers** | **154,420** | |
| Actual receipts per the cash receipts ledger (accounts 1010, 1020, 1030, 1035 plus Stripe settlements) | 154,190 | |
| **Difference** | **(230)** | Threshold $470; within |

The $(230) difference is below the $470 tolerable difference and was documented as unexplained without further
work — defensible *only* because each input was independently tested: billings to the invoice register, write-offs to
the allowance roll-forward and approved write-off log, and gross receivables to the aged trial balance tested as
information produced by the entity (Chapter 7). An unexpected result — $3,000 or more with no offsetting input
movement — almost always traces to one of the three causes listed at RQ 18-11, tested in that order.

## 18.7 Cohort-Based Predictive Testing of Subscription Revenue

The obstacle to a precise revenue expectation is in-period movement: customers who start, expand, contract, or churn
mid-year break the arithmetic. Stratify by movement pattern, predict only where the relationship is tight, and test
the rest by other means.

**Exhibit 18-10. Recurring subscription revenue by cohort, FY2025 (in thousands).**

| Cohort | Customers | FY2025 revenue | Procedure applied |
| --- | --- | --- | --- |
| Stable — live for all of FY2024 and FY2025 | 1,894 | 84,070 | Substantive analytical procedure (below) |
| Partial-period FY2024 starts | 796 | 26,540 | Contract-level recomputation of a sample (Chapter 5) |
| FY2025 new logos | 612 | 9,340 | Full-population recomputation from start dates and seats |
| Churned during FY2025 | 438 | 5,210 | Full-population recomputation of the stub period |
| Self-serve (Stripe) | 11,400 | 6,100 | Cash-to-revenue reconciliation of the I-4 daily journal |
| Kestrel migrated base | 61 | 340 | Test of details, 100% |
| **Total recurring revenue** | | **131,600** | Plus usage overage of $4,200 = $135,800 |

For the stable cohort, the same 1,894 customers generated **$80,140** in FY2024. The expectation is that base adjusted
for two changes measured independently from the Zuora amendment file — **+2.7%** in seats and **+2.0%** in price:

```text
Expected FY2025 stable-cohort revenue = 80,140 x 1.027 x 1.020 = 80,140 x 1.0475 = 83,947
Actual FY2025 stable-cohort revenue                                             = 84,070
Difference                                                                      =    123
Threshold (470 x 84,070 / 131,600 = 300)                                        =    300  -> within
```

The expectation is precise because the population is closed. Had the difference been $900, the next step is to rank
the 1,894 customers by absolute difference; a closed-population analytic usually fails on a few accounts.

## 18.8 Churn and Retention Analytics

Net revenue retention fell from **118%** to **112%**. Six points is not a misstatement, but it is a risk assessment
finding of the first order because four FY2025 accounting conclusions depend on retention: the 4-year commission
amortization period (§4.2, supported by a 4.3-year average customer life), the CECL forecast overlay, the ARR-based
PSU probability revised to 85% in Q4, and the absence of an impairment indicator.

**Exhibit 18-11. NRR decomposition, FY2024 versus FY2025.**

| Component | FY2024 | FY2025 | Change in points | FY2025 dollar effect at the FY2024 rate (in thousands) |
| --- | --- | --- | --- | --- |
| Cohort denominator (opening ARR excluding self-serve) | 100,600 | 132,000 | | |
| Expansion rate | 25.0% | 21.0% | (4.0) | $5,280 of expansion ARR not earned |
| Contraction rate | (4.1)% | (5.6)% | (1.5) | $1,999 of additional contraction ARR |
| Gross churn rate | (2.9)% | (3.4)% | (0.5) | $641 of additional churn ARR |
| **Net revenue retention** | **118.0%** | **112.0%** | **(6.0)** | |
| Gross retention (100% − contraction − churn) | 93.0% | 91.0% | (2.0) | |

Two-thirds of the decline is an expansion shortfall, not deterioration in the existing base — which matters because
expansion bears on the PSU probability and forward ARR forecasts, while contraction and churn bear on the commission
amortization period and the credit-loss forecast. Gross retention of 91% implies a mean customer life of about 11.1
years on a constant-hazard assumption, comfortably longer than the 4.3 years supporting §4.2's 4-year commission
period. Contraction rising 1.5 points does tighten the case for testing the $1,900 of capitalized costs on non-renewed
customers. (The FY2024 denominator extends the case: ARR at December 31, 2023 of $104,200 less self-serve of $3,600.)

## 18.9 Receivable and Collection Analytics

Days sales outstanding rose from **61.0** to **68.0** days. AtlasFlow computes DSO on Q4 billings, and the
computation reproduces the disclosure exactly:

```text
FY2025:  38,600 / 52,240 x 92 = 67.98  -> 68.0 days
FY2024:  30,500 / 46,000 x 92 = 61.00  -> 61.0 days
```

Q4 billings of $52,240 and $46,000 are Chapter 7's figures. Seven days of DSO is not an adjective; it is a dollar
amount. At FY2024 velocity, gross receivables would have been $52,240 × 61 ÷ 92 = **$34,637** against the actual
$38,600, so **$3,963** would not have existed — 4.2 times performance materiality.

**Exhibit 18-12. Decomposition of the $3,963 receivable increase attributable to slower collection (in
thousands).**

| Driver | Amount | Days | Evidence obtained |
| --- | --- | --- | --- |
| Invoices dated December 24–31, 2025, none due at year end | 2,180 | 3.8 | Invoice register aged by invoice date; agreed to the $25,174 of ACV signed December 24–31 (§3.1) |
| Deterioration in the over-60-day buckets: $4,120 against $2,610 | 1,510 | 2.7 | §3.3 aging; prior-year aging |
| Extended payment terms (net 45 on 118 FY2025 renewals) | 610 | 1.1 | Zuora payment-term field |
| Kestrel receivables migrated October 2025, no dunning until January 2026 | 340 | 0.6 | Kestrel subledger aging |
| Offset: improved self-serve collection after Stripe card-retry remediation | (677) | (1.2) | Stripe settlement data |
| **Total** | **3,963** | **7.0** | |

The first driver is a timing consequence of the bookings concentration, not a collection problem; the second is. The
analytic does not conclude on the allowance — Chapter 7 owns that — but it hands Chapter 7 a quantified start: $1,510
of the increase sits in buckets carrying 18% to 85% loss rates, implying roughly $340 of incremental expected credit
loss at the §3.3 rates.

## 18.10 Payroll, Gross Margin, and Unit Economics Analytics

**Payroll from headcount.** Average FY2025 headcount was 748 — the mean of quarterly averages of 706, 731, 764, and
791 — against 812 employees at December 31, 2025 (§1.1). Cost per head comes from the compensation plan, not the ledger.

**Exhibit 18-13. Headcount-based personnel cost expectation, FY2025 (in thousands except per-head amounts).**

| Geography | Average heads | Cost per head | Expected |
| --- | --- | --- | --- |
| United States | 555 | $168.0 | 93,240 |
| United Kingdom | 68 | $132.0 | 8,976 |
| Australia | 39 | $124.0 | 4,836 |
| India | 86 | $41.0 | 3,526 |
| **Total** | **748** | | **110,578** |
| Less: labour capitalized into software (§4.3) | | | (9,400) |
| **Expected cost charged to expense** | | | **101,178** |
| Actual per GL personnel accounts, ex-SBC and commissions | | | 101,640 |
| **Difference** | | | **462** |

The $462 difference is inside performance materiality but the achieved precision is not: a 1% error in cost per head
moves the expectation by $1,106, so this is filed as a risk assessment procedure. The precise version is India, which
§1.5 assigns to analytical-procedures-only scope as a cost-plus entity with a homogeneous workforce: 86 × $41.0 =
$3,526 expected against $3,510 actual, $(16) against a $120 threshold. That analytic *is* substantive, and the entire
difference in precision comes from population homogeneity.

**Gross margin and unit economics.** Subscription gross margin was 80.0% (($135,800 − $27,160) ÷ $135,800) against
78.6% and 77.5% in FY2024 and FY2023. A 140-basis-point improvement is a risk signal until explained at the unit
level, because Chapter 17 treats misclassification out of cost of revenue as a fraud scheme.

**Exhibit 18-14. Hosting cost per thousand workflow runs (account 5100).**

| Measure | FY2025 | FY2024 |
| --- | --- | --- |
| Hosting cost (in thousands) | 13,400 | 11,600 |
| Workflow runs executed (millions) | 4,820 | 3,610 |
| Cost per thousand runs | $2.78 | $3.21 |
| Expected FY2025 hosting cost at FY2024 unit cost: 4,820 × $3.21 | 15,472 | |
| Favourable variance to explain | 2,072 | |
| Expected cost at the rates in the three-year AWS savings plan signed February 2025: 4,820 × $2.76 | 13,303 | |
| Difference from actual | 97 | Threshold $300; within |

Reconciling the cost-centre-to-account mapping then identified six employees remapped from account 5110 to 6100 in
July 2025, moving roughly $370 of half-year cost out of cost of revenue — 27 basis points. Below performance
materiality, but it must be reclassified or disclosed as a comparability matter, and it is exactly what the unit
analytic exists to find.

## 18.11 Process Mining on the Order-to-Cash Event Log

Process mining reconstructs actual event sequences from system timestamps and compares them to the documented process.
The event log is assembled from Salesforce CPQ (`OpportunityHistory`, `Quote`, `Approval`), Zuora (`Subscription`,
`Invoice`), and NetSuite (`CustomerPayment`), keyed on opportunity, over 4,806 FY2025 activations.

**Exhibit 18-15. Order-to-cash process variants, FY2025.**

| Variant | Description | Count | ACV | Audit significance |
| --- | --- | --- | --- | --- |
| V1 | Standard eight-event path in sequence | 3,914 | 138,200 | None |
| V2 | Order form signed before discount approval | 61 | 9,240 | CPQ deviation; cut-off risk |
| V3 | Activated before order form signature | 34 | 4,110 | Revenue start-date risk |
| V4 | Order form modified after Closed Won | 118 | 12,600 | Modification accounting (Ch. 5) |
| V5 | Invoice issued before activation | 212 | 8,900 | Deferred revenue completeness |
| V6 | Quote re-approved three or more times | 289 | 21,300 | Side-letter risk |
| V7 | Order-form date changed after Closed Won | 19 | 3,180 | Backdating (Ch. 17) |
| V8 | All other sequences | 159 | 6,470 | Reviewed; none significant |
| **Total** | | **4,806** | **204,000** | ACV in thousands |

Cycle time is the second output and often the more useful one. Median opportunity-to-activation cycle time was 18 days
for orders closed in Q1 through Q3 and **4 days** for the 41% of Q4 ACV signed December 24–31. A 14-day compression is
impossible without skipping events, which is why the December cohort became the target population for the test of
details rather than a random sample. All 19 V7 contracts were tested: 13 corroborated, and 6 December contracts whose
signature dates could not be — the six Chapter 17 develops and U-3 quantifies at $150.

## 18.12 Outlier Detection, Benford's Law, and Visualization

**The false-positive problem.** An outlier rule is a hypothesis about how a misstatement would look. A rule selecting
a large fraction of the population is a filter with no discriminating power.

**Exhibit 18-16. Outlier rule performance over the FY2025 revenue transaction population.**

| Rule | Selected | True findings | False-positive rate |
| --- | --- | --- | --- |
| Revenue start date more than 5 days before order-form date | 214 | 9 | 95.8% |
| Discount greater than 45% of list | 96 | 3 | 96.9% |
| No invoice within 45 days of activation | 61 | 4 | 93.4% |
| Revenue amount within 0.5% of a $10,000 multiple | 1,842 | 0 | 100.0% |
| Manual revenue schedule override in RevPro | 47 | 12 | 74.5% |
| Credit memo exceeding 25% of the original invoice | 38 | 7 | 81.6% |
| **Total, rules run independently** | **2,298** | **35** | **98.5%** |
| Reworked set: every rule required to co-occur with a December activation date or a manual RevPro override | 128 | 31 | 75.8% |

At 20 minutes per item the original set costs 766 hours to find 35 items; the reworked set costs 43 hours and finds 31
of the same 35. The round-dollar rule selected 38% of a population priced in $12,000 and $24,000 increments and found
nothing — a criteria-design failure, not a clean population.

**Benford's law.** Benford's law describes leading-digit frequencies in populations spanning several orders of
magnitude that are not generated by human-chosen price points. The first-digit test on 9,412 Q4 2025 invoices:

**Exhibit 18-17. Benford first-digit test, Q4 2025 invoice amounts (n = 9,412).**

| Digit | Expected % | Expected | Observed | χ² contribution |
| --- | --- | --- | --- | --- |
| 1 | 30.1% | 2,833 | 2,614 | 16.9 |
| 2 | 17.6% | 1,657 | 1,903 | 36.7 |
| 3 | 12.5% | 1,177 | 1,208 | 0.8 |
| 4 | 9.7% | 913 | 1,041 | 18.0 |
| 5 | 7.9% | 744 | 702 | 2.3 |
| 6 | 6.7% | 631 | 588 | 2.9 |
| 7 | 5.8% | 546 | 496 | 4.6 |
| 8 | 5.1% | 480 | 471 | 0.2 |
| 9 | 4.6% | 433 | 389 | 4.4 |
| **Total** | **100.0%** | **9,412** | **9,412** | **86.8** |

```python
import numpy as np
from scipy.stats import chisquare

benford = np.array([.301,.176,.125,.097,.079,.067,.058,.051,.046])
observed = np.array([2614,1903,1208,1041,702,588,496,471,389])
expected = benford * observed.sum()
stat, p = chisquare(observed, f_exp=expected)
print(f"chi-square = {stat:,.1f}  p = {p:.3g}  critical(8 df, .05) = 15.51")
```

A statistic of 86.8 against a critical value of 15.51 at 8 degrees of freedom is overwhelmingly "significant," and
worth nothing. The excess of leading 2s and 4s is fully explained by the price list: standard Core bundles invoice at
$24,000 and $48,000 annually, and the April 2025 8% increase moved invoices from the low 20-thousands into the mid-20s
and from the high 30s into the 40s. Honest documentation records that the test was performed, that the deviation is
attributable to identified price points, and that **no audit evidence was obtained**. The test can earn its place on
populations with a wide range and no price points — expense reimbursements, vendor invoices below an approval
threshold — but even there it identifies a population characteristic, never a misstatement.

**Visualization.** A chart earns its place only if it changes a conclusion. State the question above the chart, draw
the threshold as a line, and prefer small multiples to an aggregate series, because aggregation conceals. Twelve
panels of segment difference with the $135 threshold drawn across each make the case study's misstatement visible in
seconds.

## 18.13 The Completeness and Accuracy of the Data

This is where most analytics collapse. An analytic built on an untested extract reaches a conclusion conditional on an
assumption nobody tested, and AS 1105 does not permit that. Four reconciliations are required.
**Completeness:** reconcile the extract's record count and a control total to an independent count or total in the
source system. **Accuracy:** re-perform the transformation logic on a sample of records back to source.
**Cut-off:** prove the date filter captured the whole period and nothing outside it. **Authenticity:** establish the
extract came from the system of record rather than a spreadsheet.

**Exhibit 18-18. Completeness and accuracy of the seat population at December 31, 2025 (seats in thousands).**

| Reconciliation | Seats | Difference | Disposition |
| --- | --- | --- | --- |
| Snowflake `V_SEATS_DAILY`, as first drafted | 268.9 | | |
| Zuora rate-plan charge quantity, extracted with the auditor observing | 271.8 | 2.9 | The view's `product_code` filter omitted `CORE-SEAT-KESTREL`, created at the October 2025 migration. **Analytic corrected** |
| Provisioning database, active automation seats | 274.6 | 2.8 | Provisioned but unbilled seats under 63 trials; agreed to the trial register. No revenue effect |
| Record count, `V_SEATS_DAILY` for FY2025 | 1,268,940 rows | | 3,477 subscriptions × 365 days = 1,269,105; 165 rows missing, traced to the December 31 Fivetran sync error |

The second row is the point of this section: the omitted product code changed the December expectation by **$118**,
87% of the $135 monthly threshold. The fourth row is the second point: the sync failure meant the December seat series
came from a December 1 snapshot rather than a daily average, understating the expectation by a further $46. Both
defects made the *auditor's* expectation too low, pushing the difference toward investigation; a defect the other way
shrinks the difference and gives no signal at all.

## 18.14 Documenting an Analytic, Tooling, and the Effect on Sample Sizes

**Documentation.** AS 1215 requires that an experienced auditor with no previous connection to the engagement be able
to understand and re-perform the work. For an analytic that means nine items; anything less and the reviewer is
accepting the preparer's word.

**Exhibit 18-19. Analytic documentation checklist.**

| # | Item | AtlasFlow reference |
| --- | --- | --- |
| 1 | Assertion and account | Occurrence and accuracy, account 4100 |
| 2 | Expectation, in words and as a formula | Monthly average paid seats × monthly average price |
| 3 | Source of every input: system, table, extract date, extractor | `RAW.ZUORA.RATE_PLAN_CHARGE_DAILY`, extracted January 9, 2026 by T. Iyer with B. Osei observing |
| 4 | C&A work on those inputs | Exhibit 18-18 |
| 5 | Threshold and its derivation | Exhibit 18-5 |
| 6 | Query or script, verbatim, with parameters | §18.4 SQL; the script below |
| 7 | Comparison table, all cells, unsummarized | Exhibit 18-20 |
| 8 | Each difference over threshold: explanation, corroboration, residual | Exhibit 18-21 |
| 9 | Conclusion naming assertions and assurance obtained | Walkthrough Step 14 |

**Tooling.** SQL belongs where the data lives and the joins are heavy; Python where the comparison and threshold
logic live; spreadsheets belong nowhere in the computation chain of a significant analytic, because a formula
overwritten in cell F19 leaves no trace. The comparison and flagging step is nine lines.

```python
import pandas as pd

TOLERABLE_DIFFERENCE = 470          # 50% of performance materiality of 940
MONTHS = 12
threshold = round(TOLERABLE_DIFFERENCE / MONTHS ** 0.5)     # 135

wp = pd.read_csv("core_revenue_expectation_fy25.csv")       # month, seats_000, price, actual
wp["expected"] = (wp.seats_000 * wp.price).round(0)
wp["difference"] = wp.actual - wp.expected
wp["investigate"] = wp.difference.abs() > threshold
print(wp.to_string(index=False))
print(f"threshold = {threshold}; annual difference = {wp.difference.sum():,.0f} "
      f"vs tolerable difference {TOLERABLE_DIFFERENCE}")
```

**Effect on sample sizes and the sufficiency conclusion.** Chapter 15 owns sampling mechanics; what matters here is
the interaction. Without the analytic, a monetary-unit sample over the $104,900 Core population at a tolerable
misstatement of $940, zero expected misstatement, and a 5% risk of incorrect acceptance requires
$104,900 × 3.0 ÷ $940 = **335** sampling units. With an analytic achieving ±$152 of precision and carrying 50% of the
assurance, the team instead tested two targeted populations 100% — the 341 subscriptions with post-year-end service
commencement and the 47 manual RevPro overrides — plus a 60-item sample over the residual. Only the precision
*actually achieved* justifies a reduction, and if the analytic fails the planned sample returns, late. Non-sampling
risk survives a full-population analytic: an incomplete population or a wrong expectation is not cured by more rows.

## Step-by-Step Walkthrough: A Substantive Analytical Procedure Over Core Subscription Revenue by Month

Objective: substantive evidence over the occurrence and accuracy of the $104,900 of FY2025 Core subscription revenue
in account 4100, predicted monthly from seat counts and price per seat. Performer T. Iyer (data and analytics
specialist), reviewed by O. Haddad (manager). Workpaper index **WP 3200-18**.

**Step 1. Fix the assertions and the account before touching data.** Occurrence and accuracy of account 4100,
$104,900. Completeness is *not* covered — an expectation built from billed seats cannot detect unbilled service — and
cut-off only so far as the seat and price series are date-accurate. Record that scope limitation now.

**Step 2. Confirm the recorded amount.** Agree account 4100 to $104,900 per the trial balance and the monthly detail
to Exhibit 18-20, with quarterly subtotals tying to §3.1 ($24,100, $25,700, $26,900, $28,200). Unexpected result:
detail that does not foot to the account is a subledger-to-GL problem (Chapter 12) to resolve first.

**Step 3. Choose the disaggregation.** Monthly, Core only. Monthly rather than quarterly because a one-month cut-off
misstatement is diluted three-to-one by quarterly aggregation. Core only because Insight launched in January 2025
with no comparative, overage is consumption-based, and professional services follows an input measure. Segment
disaggregation was rejected: Core is homogeneously priced across segments.

**Step 4. Derive the threshold and write it down.** Performance materiality $940; k = 0.50 because tests of details
carry the balance of the assurance; tolerable difference $470; monthly threshold $470 ÷ √12 = **$135**. Document the
rejected alternatives ($39 and $175–$190 per Exhibit 18-5). Unexpected result: a threshold smaller than the precision
you can achieve means redesigning or selecting a different procedure.

**Step 5. Request the independent data and specify the fields.** From Zuora: `subscription_id`, `product_code`,
`charge_type`, `quantity`, `mrr_per_unit`, `effective_start_date`, `effective_end_date`, `subscription_status`,
`currency`, `fx_rate`. Ask the data owner which statuses earn revenue, whether `quantity` is point-in-time or
as-amended, and whether every Core product code is enumerated. The third is the one that mattered.

**Step 6. Test completeness and accuracy before computing anything.** Perform the four reconciliations in
Exhibit 18-18. Resolve the 2.9-thousand-seat difference to the omitted `CORE-SEAT-KESTREL` code and **correct the
analytic before proceeding**; an unresolved completeness difference of any size stops the analytic.

**Step 7. Run the expectation query.** Execute the §18.4 SQL against the corrected product-code list for twelve rows
of average seats and average price. Save the query text, execution timestamp, and row count; a screenshot of a result
grid cannot be re-performed.

**Step 8. Sanity-check the parameters before comparing.** Average seats rise monotonically from 231.6 thousand in
January to 266.3 thousand in December (+15.0%) and average price from $34.10 to $35.45 (+4.0%), consistent with the
April 2025 8% list increase applied only to new and renewing customers (§1.8). Unexpected result: a price series
stepping up the full 8% in April would mean grandfathering was not applied — a finding about the data, not revenue.

**Step 9. Compute the comparison and apply the threshold** using the pandas script in §18.14.

**Exhibit 18-20. Core subscription revenue: expectation versus actual, FY2025 (in thousands except price).**

| Month | Avg paid seats (000s) | Avg price per seat | Expected | Actual | Difference | Over $135 threshold? |
| --- | --- | --- | --- | --- | --- | --- |
| January | 231.6 | $34.10 | 7,898 | 7,920 | 22 | No |
| February | 235.8 | $34.15 | 8,053 | 8,020 | (33) | No |
| March | 238.1 | $34.20 | 8,142 | 8,160 | 18 | No |
| April | 244.6 | $34.35 | 8,402 | 8,380 | (22) | No |
| May | 248.2 | $34.55 | 8,575 | 8,590 | 15 | No |
| June | 252.4 | $34.70 | 8,758 | 8,730 | (28) | No |
| July | 253.2 | $34.80 | 8,811 | 8,830 | 19 | No |
| August | 257.1 | $34.95 | 8,986 | 8,960 | (26) | No |
| September | 259.1 | $35.10 | 9,094 | 9,110 | 16 | No |
| October | 262.6 | $35.25 | 9,257 | 9,240 | (17) | No |
| November | 264.6 | $35.35 | 9,354 | 9,340 | (14) | No |
| December | 266.3 | $35.45 | 9,440 | 9,620 | **180** | **Yes** |
| **Total** | | | **104,770** | **104,900** | **130** | Annual tolerable difference $470 |

**Step 10. Assess the precision actually achieved.** The eleven non-December differences have a mean of $(4.5) and a
standard deviation of **$22**; at two standard deviations, ±$45 monthly and ±$152 annually ($22 × √12 × 2), inside the
$135 and $470 thresholds. Record it — it is the evidence that the §18.3.2 inequality holds.

**Step 11. Investigate the December difference, starting with your own expectation.** Two defects surfaced.

**Exhibit 18-21. Investigation of the December difference (in thousands).**

| Item | Amount | Evidence obtained |
| --- | --- | --- |
| Difference to be explained | 180 | Exhibit 18-20 |
| Kestrel seats first billed on `CORE-SEAT-KESTREL` in the December 1 billing run, 2.9 thousand seats at $40.70 | (118) | Zuora December invoice run; 61 subscriptions agreed to the migration listing; price agreed to the Kestrel order forms |
| December seat series populated from a December 1 snapshot rather than a daily average after the December 31 sync job failed; recomputed daily average 267.6 thousand against 266.3 used, at $35.45 | (46) | Fivetran job log; re-extracted daily series direct from Zuora |
| **Residual, unexplained** | **16** | Below the $135 threshold and the $72 clearly trivial threshold |

**Step 12. Re-run with corrected inputs and confirm the residual.** Corrected December expectation:
$9,440 + $118 + $46 = $9,604 against actual of $9,620, a difference of $16. Confirm neither correction touches
another month: the Kestrel code first billed in December, and the sync failure was specific to December 31.
Unexpected result: a correction affecting earlier months requires every month to be recomputed.

**Step 13. Consider whether the explained items are themselves findings.** They are. The `V_SEATS_DAILY` product-code
omission is a further instance of the W-11 datamart weakness and goes to the Chapter 12 evaluation; the December 31
sync failure is a computer-operations matter for the Chapter 11 ITGC conclusion. Neither is a misstatement.

**Step 14. Draft the conclusion, naming the assertions and the assurance obtained.** Model language:

```text
Procedure and result.  We developed an independent expectation of monthly Core subscription revenue as the
product of average daily paid automation seats and average contracted price per seat, from Zuora rate-plan
charge records whose completeness and accuracy we tested at WP 3200-18/6.  Our FY2025 expectation was
$104,770 against recorded revenue of $104,900, a difference of $130 against a tolerable difference of $470
(50% of performance materiality of $940).  Eleven of twelve monthly differences were below the $135 monthly
threshold; December's $180 was investigated and $164 explained by two defects in our own extract, leaving an
unexplained residual of $16.  Empirical precision, two standard deviations of the non-exception monthly
differences, was +/- $45 monthly.

Conclusion.  Core subscription revenue of $104,900 is consistent with our independent expectation.  This
procedure provides substantive evidence over occurrence and accuracy and carries 50% of the planned assurance
for those assertions; it provides no evidence over completeness or the December 2025 cut-off, addressed at
WP 3200-24 and WP 3200-31.
```

**Step 15. Place tick marks and cross-reference.** On Exhibit 18-20: (a) recorded amounts agreed to the account 4100
monthly detail at WP 3200-02; (b) seat figures agreed to the tested extract at WP 3200-18/6; (c) December, see
Exhibit 18-21. Cross-reference the two data defects to the Chapter 11 and Chapter 12 workpapers, and the $16 residual
to the summary of audit differences as below the clearly trivial threshold.

## Extended Case Study: The Insight Revenue Analytic That Passed at the Annual Level

*This case study extends the continuing case. The $780 EMEA Insight cut-off misstatement described here is a
hypothetical variation introduced to demonstrate the effect of aggregation; it does not appear in the Part 7
misstatement schedules and Chapter 19 does not carry it.*

### Background

AtlasFlow Insight launched as a separate SKU in January 2025 and generated $26,700 of FY2025 subscription revenue
(account 4110). With no FY2024 comparative, the team planned a substantive analytical procedure built from the attach
base: Core customers holding an Insight subscription, times average annual Insight contract value. A. Trent (staff)
performed it at the Q3 interim date and rolled it forward in the week before the report date.

### The Facts

**Exhibit 18-22. The Insight analytic as originally performed (in thousands except counts).**

| Line | Amount |
| --- | --- |
| Customers with an Insight subscription at December 31, 2025 | 1,412 |
| Average annual Insight contract value | $21.9 |
| Insight ACV in force at December 31, 2025 | 30,920 |
| Average fraction of FY2025 live, from Salesforce opportunity close dates | 0.859 |
| **Expected FY2025 Insight revenue** | **26,560** |
| Recorded Insight revenue (account 4110) | 26,700 |
| **Difference** | **140** |
| Threshold used by the preparer | 940 (performance materiality, unallocated) |
| Conclusion recorded | "Difference of $140 is well below performance materiality. No exceptions noted." |

### What the Engagement Team Did

G. Lindqvist (senior manager) raised three review notes: the analytic is not disaggregated; the threshold is
performance materiality rather than a derived tolerable difference; and the 0.859 time factor comes from Salesforce
close dates while revenue starts on the Zuora service commencement date. The analytic was rebuilt by segment from
Zuora attach counts and prices, with a $470 tolerable difference and a segment threshold of $470 ÷ √4 = **$235**.
Both computations are shown so the effect of aggregation is visible.

**Exhibit 18-23. Insight revenue by segment, FY2025 (in thousands except counts).**

| Segment | Avg attached customers | Avg annual Insight price | Expected | Actual | Difference | Over $235? |
| --- | --- | --- | --- | --- | --- | --- |
| Enterprise (US) | 401 | $34.60 | 13,875 | 13,900 | 25 | No |
| Mid-market (US) | 566 | $11.20 | 6,339 | 6,300 | (39) | No |
| EMEA (AtlasFlow Software Ltd) | 154 | $26.75 | 4,120 | 4,900 | **780** | **Yes** |
| APAC (AtlasFlow Pty Ltd) | 65 | $24.90 | 1,619 | 1,600 | (19) | No |
| **Total** | **1,186** | | **25,953** | **26,700** | **747** | Annual tolerable difference $470 — **exceeded** |

The EMEA difference was then disaggregated by month against a threshold of $235 ÷ √12 = **$68**.

**Exhibit 18-24. EMEA Insight revenue by month, FY2025 (in thousands except counts and price).**

| Month | Attached customers | Avg monthly price | Expected | Actual | Difference | Over $68? |
| --- | --- | --- | --- | --- | --- | --- |
| January | 112 | $2,230 | 250 | 250 | — | No |
| February | 119 | $2,240 | 267 | 265 | (2) | No |
| March | 124 | $2,265 | 281 | 280 | (1) | No |
| April | 132 | $2,275 | 300 | 300 | — | No |
| May | 140 | $2,290 | 321 | 320 | (1) | No |
| June | 148 | $2,300 | 340 | 340 | — | No |
| July | 156 | $2,315 | 361 | 360 | (1) | No |
| August | 161 | $2,325 | 374 | 375 | 1 | No |
| September | 167 | $2,340 | 391 | 390 | (1) | No |
| October | 170 | $2,355 | 400 | 660 | **260** | **Yes** |
| November | 173 | $2,370 | 410 | 670 | **260** | **Yes** |
| December | 180 | $2,362 | 425 | 690 | **265** | **Yes** |
| **Total** | | | **4,120** | **4,900** | **780** | |

### Analysis

Three independent defects concealed the misstatement, and each alone was sufficient.

1. **The wrong system supplied a parameter.** Salesforce Closed-Won dates precede Zuora service commencement by an
   average of 7.2 days, inflating the time factor by $30,920 × 7.2 ÷ 365 = **$610** — substantially all of the $607
   gap between the original $26,560 expectation and the properly built $25,953. The expectation was overstated by
   almost exactly the misstatement, so the two cancelled.
2. **The threshold was unallocated performance materiality.** Even with the correct expectation, $747 is below $940
   and would have been accepted. The derived $470 tolerable difference flags it.
3. **No disaggregation.** Aggregating four segments netted the $780 EMEA overstatement against $33 of offsets and gave
   no signal about *where* to look.

### Resolution and Conclusion

The October, November, and December differences of $260, $260, and $265 pointed to one population. Testing it
identified **47 EMEA Insight add-on subscriptions with aggregate annual contract value of $3,120** entered in Zuora
with a service commencement date of **October 1, 2025**, while the countersigned order forms and the provisioning
records both showed service commencing **January 1, 2026**. Three months of revenue on $3,120 of ACV is
$3,120 × 3 ÷ 12 = **$780**, $260 a month — matching the analytic to the dollar.

The cause was a UK billing convention: the EMEA billing analyst dated each quarter's amendments to the first day of
that quarter so renewals aligned to quarterly billing runs, and accounting had never reviewed it. Management recorded
the $780 reversal (reducing account 4110, increasing account 2400). The team evaluated the convention as a control
deficiency, aggregated it with the other revenue-cut-off findings under the Chapter 14 severity framework, and
extended testing to all 214 FY2025 EMEA amendments, finding no instances outside Q4.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                              WP 3200-21
AtlasFlow, Inc. — Year ended December 31, 2025
INSIGHT SUBSCRIPTION REVENUE — SUBSTANTIVE ANALYTICAL PROCEDURE (REPERFORMED)

Prepared by:  A. Trent          Date prepared:  February 4, 2026
Reviewed by:  O. Haddad         Date reviewed:  February 6, 2026
Reviewed by:  G. Lindqvist      Date reviewed:  February 7, 2026

PURPOSE
To obtain substantive evidence over the occurrence, accuracy, and cut-off of Insight subscription revenue of
$26,700 (account 4110), reperforming the analytic at WP 3200-20, which the manager concluded was imprecise.

SOURCE OF INFORMATION
(1) Zuora subscription and amendment records, product codes INSIGHT-BASE and INSIGHT-ADV, extracted January 12,
    2026 by T. Iyer with the auditor observing (C&A at WP 3200-21/3: record count 3,118 agreed to the Zuora
    subscription summary; ACV control total $30,920 agreed within $4 to the "Subscription ACV" report).
(2) Account 4110 monthly detail per the NetSuite trial balance, agreed to Sec. 3.1 quarterly revenue.
(3) Countersigned order forms and provisioning records for the 47 subscriptions selected below.

THRESHOLD
Performance materiality $940. Tolerable difference $470 (k = 0.50; tests of details carry the balance).
Segment threshold $470 / sqrt(4) = $235. Monthly threshold within a segment $235 / sqrt(12) = $68.

PROCEDURES PERFORMED AND RESULTS
1. Rebuilt the expectation by segment (Exhibit 18-23): expected $25,953 against recorded $26,700; difference
   $747, exceeding $470. Enterprise $25, mid-market $(39), and APAC $(19) were each below $235 - no exception.
2. EMEA difference of $780 exceeded $235. Disaggregated monthly (Exhibit 18-24): October $260, November $260,
   December $265, each exceeding $68; the nine other months were within $2 of expectation.
3. Selected all EMEA Insight amendments with a Q4 2025 service commencement date (n = 47, ACV $3,120) and
   compared the Zuora date to the countersigned order form and the provisioning activation record. All 47
   showed October 1, 2025 in Zuora against January 1, 2026 on both sources. Effect: $3,120 x 3/12 = $780,
   being $260 in each of October, November, and December 2025.
4. Obtained the UK billing procedure dated March 2025 describing quarter-start dating, and extended testing to
   all 214 FY2025 EMEA amendments; no instances outside Q4 2025.

CONCLUSION
Insight subscription revenue is overstated by $780 because EMEA subscriptions were recognized from October 1,
2025 rather than January 1, 2026. The misstatement is factual, not projected, and has been communicated to
management. Following correction, recorded revenue of $25,920 is consistent with our expectation of $25,953
(difference $(33), within $470), and this procedure provides substantive evidence over occurrence, accuracy,
and cut-off for account 4110. The dating convention is a control deficiency referred to WP 4100-12.
```

### Lessons

1. A small difference proves nothing unless you know the precision behind it. The original $140 difference was
   smaller than the $747 the correct expectation produced, and the smaller number was the worse evidence.
2. Parameters must come from the system that determines the accounting outcome — Zuora, not Salesforce.
3. A threshold set at unallocated performance materiality guarantees that every misstatement below performance
   materiality passes — precisely the population the analytic exists to find.
4. Disaggregate along the dimensions on which a misstatement would be *concentrated* — legal entity, month, process
   owner — not those on which the financial statements happen to be presented.
5. Roll-forward is where interim analytics fail. The Q3 version was defensible because the misstatement had not yet
   occurred; rolling it forward mechanically imported a design Q4 events had invalidated.

## Common Mistakes

### Mistake 18.1 — Using the client's own revenue report as the "independent" source

**What it looks like.** The expectation is built from a Snowflake view or Zuora report drawing on the same
subscription records that generated the revenue entry.
**Why it happens.** That report is easier to obtain and gives a satisfyingly small difference.
**What goes wrong.** The expectation cannot disagree with the recorded amount, so the analytic cannot detect.
**How to avoid it.** Ask of every input whether a misstatement in revenue would also change it. If yes, it is not
independent.

### Mistake 18.2 — Calling a trend comparison a substantive analytical procedure

**What it looks like.** A workpaper titled "Substantive analytical procedure — revenue" showing FY2025 against FY2024
by quarter with variance percentages and management's explanations.
**Why it happens.** The template says "analytical procedure," and a procedure genuinely was performed.
**What goes wrong.** Nothing was predicted, so the assurance the plan assumed was never obtained.
**How to avoid it.** Apply the one-question test in §18.2; if you did not predict the number, retitle the workpaper
and design a real test.

### Mistake 18.3 — Setting the threshold at performance materiality without allocating

**What it looks like.** Every analytic in the file uses $940, regardless of account size or disaggregation.
**Why it happens.** Performance materiality is the number everyone knows; allocating requires judgment.
**What goes wrong.** Any misstatement below performance materiality passes by construction — defect two in the
extended case study.
**How to avoid it.** Derive the tolerable difference as a stated fraction of performance materiality, divide by √n
for n cells, and fix it before computing the difference.

### Mistake 18.4 — Disaggregating on a dimension with no causal relationship

**What it looks like.** Revenue split by sales region because the disclosure is by region, while the misstatement
risk sits in contract start dates.
**Why it happens.** The ASC 606-10-50 categories are available and feel authoritative.
**What goes wrong.** Cells multiply without adding precision, per-cell thresholds shrink, and the team investigates
false positives while the real concentration stays hidden.
**How to avoid it.** Choose the dimension along which a misstatement would concentrate — period, entity, process
owner, product code — and confirm pricing is homogeneous within each cell.

### Mistake 18.5 — Accepting management's explanation as the investigation

**What it looks like.** "Per discussion with the Revenue Manager, the December increase relates to the Q4 bookings
surge. No further work performed."
**Why it happens.** The explanation is plausible, the deadline is close, and corroboration takes a day.
**What goes wrong.** AS 2305 requires corroborated explanations; inquiry alone cannot support a substantive
conclusion, and an unquantified explanation leaves the residual unmeasured.
**How to avoid it.** Require every explanation to be quantified and traced to a source other than the person who
offered it, and evaluate the residual separately.

### Mistake 18.6 — Building on data whose completeness and accuracy was never tested

**What it looks like.** The workpaper documents the query and the result but no reconciliation to the source.
**Why it happens.** The extract came from the client's reporting warehouse, and the specialist and the in-charge each
assume the other tested it.
**What goes wrong.** One omitted product code moved AtlasFlow's December expectation by $118 against a $135
threshold; a defect the other way would have shrunk the difference and produced a false negative.
**How to avoid it.** Perform and document the four §18.13 reconciliations before any comparison, and name who
performed the extraction.

### Mistake 18.7 — Running the analytic first and setting the threshold second

**What it looks like.** The threshold is a round number slightly above the largest observed difference.
**Why it happens.** Nobody set a threshold at planning, and by review-note time the results are known.
**What goes wrong.** The procedure has no capacity to fail, and nothing in the file shows it could ever have detected
a material misstatement.
**How to avoid it.** Document the threshold and its derivation before the query execution timestamp.

### Mistake 18.8 — Treating the ARR bridge as substantive evidence over revenue

**What it looks like.** A workpaper reconciling $137,400 of opening ARR to $172,000 of closing ARR to $135,800 of
subscription revenue, concluding revenue is reasonable.
**Why it happens.** The bridge is the analytic management itself uses, and the reconciling items are real.
**What goes wrong.** Those items are estimates with a combined tolerance of about ±$1,900, four times the $470
tolerable difference; the file overstates the assurance obtained, which surfaces wherever a sample was reduced in
reliance on it.
**How to avoid it.** Estimate the tolerance of each reconciling item, sum them, compare to the threshold, and file
the bridge as a risk assessment procedure when it fails — which it usually will.

### Mistake 18.9 — Chasing every outlier hit instead of designing criteria

**What it looks like.** Six rules produce 2,298 hits, the team works them for three weeks, and 35 matter.
**Why it happens.** Rules are cheap to write, and "we looked at everything" sounds defensible.
**What goes wrong.** 766 hours buy what a co-occurrence design buys in 43, the December cut-off budget disappears,
and staff stop reading output carefully by hit 400.
**How to avoid it.** Measure each rule's false-positive rate, require co-occurrence of two independent risk
indicators, and document why a rule selecting 38% of a population was replaced rather than dropped.

### Mistake 18.10 — Reporting a Benford chi-square as a finding

**What it looks like.** "The first-digit distribution deviates significantly from Benford's law (χ² = 86.8,
p < 0.001), indicating potential manipulation of invoice amounts."
**Why it happens.** The statistic is easy to compute and significance reads as evidential weight.
**What goes wrong.** Subscription invoices come from a price list with $24,000 and $48,000 bundle points, so
Benford's assumptions fail; the "finding" is an artifact of pricing.
**How to avoid it.** Before running the test, confirm the population spans several orders of magnitude with no
built-in price points. If it does not, do not run it; if you did, document that no evidence was obtained.

## Practice Exercises

### Exercise 18-1 [Foundational]

For each of the following, state which of the four families it belongs to and which of the three roles it can play:
(a) revenue by stream by quarter per §3.1; (b) the deferred revenue roll-forward identity in Exhibit 18-8; (c) the
NRR decomposition in Exhibit 18-11; (d) the monthly Core seat-based expectation; (e) scoring 4,912 manual journal
entries to select 60 for testing.

### Exercise 18-2 [Foundational]

Using only these figures — opening deferred revenue $62,300, closing deferred revenue $78,200, Kestrel
acquired deferred revenue $610, foreign currency translation $(260), total revenue $148,200 — compute
FY2025 billings. Then state what the bridge would be if AtlasFlow's $1,300 increase in contract assets sat
outside the deferred revenue subledger.

### Exercise 18-3 [Foundational]

Q4 FY2025 billings were $52,240 and gross receivables at December 31, 2025 were $38,600; Q4 FY2024 billings were
$46,000 and gross receivables at December 31, 2024 were $30,500. Compute DSO for both years on a 92-day quarter, and
the dollar amount of receivables that would not exist at prior-year velocity, expressed as a multiple of performance
materiality of $940.

### Exercise 18-4 [Intermediate]

For three months of mid-market Insight revenue you obtain: April, 548 attached customers at an average monthly price
of $935; May, 556 at $940; June, 561 at $948. Recorded revenue was $512, $530, and $529. The segment tolerable
difference is $118 and the monthly threshold $34. Compute the expectation and the difference, and state which months
require investigation.

### Exercise 18-5 [Intermediate]

Performance materiality is $940. You are designing a substantive analytical procedure over the $12,400 of
professional services revenue, disaggregated into six two-month periods, carrying 40% of the planned assurance for
occurrence. Derive the tolerable difference and the per-period threshold, then give two defensible alternatives and
say what would move you to each.

### Exercise 18-6 [Intermediate]

FY2024: cohort denominator $100,600; expansion 25.0%; contraction (4.1)%; churn (2.9)%. FY2025: cohort denominator
$132,000; expansion $27,720; contraction $(7,410); churn $(4,470). Compute the FY2025 rates and NRR; decompose the
change in NRR into three components summing to the total; and compute the additional contraction ARR in FY2025
relative to the FY2024 rate.

### Exercise 18-7 [Intermediate]

Gross receivables were $30,500 at January 1, 2025 and $38,600 at December 31, 2025. The allowance moved from $1,350
to $1,900 with a provision of $1,780. Billings were $163,750. Compute write-offs and expected cash receipts. Actual
receipts were $154,190; conclude against a $470 tolerable difference and name the three most likely causes had the
difference been $3,400.

### Exercise 18-8 [Advanced]

Find the errors in this workpaper extract: "*Substantive analytical procedure — usage overage revenue. We expected
FY2025 usage overage revenue to be $4,300, computed as FY2024 usage overage of $2,800 grown at the 53.6% growth in
workflow runs reported by management in the Q4 board deck. Recorded revenue was $4,200, a difference of $(100),
below performance materiality of $940. Per the Revenue Manager the difference relates to timing. Conclusion: no
exceptions noted.*" Identify at least five defects. Quarterly overage revenue was $780, $940, $1,090, and $1,390.

### Exercise 18-9 [Advanced]

The ARR-to-revenue bridge in Exhibit 18-7 leaves a $1,400 unexplained residual against performance materiality of
$940. In three to five sentences, conclude on whether the bridge provides substantive evidence over subscription
revenue, state the authoritative basis, and give one credible contrary position and why it is weaker.

### Exercise 18-10 [Advanced]

Draft the investigation paragraph documenting the $180 December difference in Exhibit 18-20, in 120 to 180 words. It
must quantify each explanation, name the corroborating evidence, and evaluate the residual against both the threshold
and the clearly trivial threshold.

### Exercise 18-11 [Advanced]

*Spans Chapter 15.* Without an analytic, a monetary-unit sample over the $104,900 Core revenue population at a
tolerable misstatement of $940, zero expected misstatement, and a reliability factor of 3.0 requires 335 sampling
units. Assume the monthly analytic is completed but achieves precision of only ±$1,100 because the seat data could
not be reconciled. Draft a 100-to-150-word note to the engagement partner on the effect on planned testing and the
sufficiency conclusion.

### Exercise 18-12 [Advanced]

*Spans Chapter 12.* W-11 records that the Snowflake RevOps datamart producing ARR and NRR was not reconciled to the
general ledger for the first three quarters of FY2025, and Chapter 12 identified four defects in
`REVOPS.MART.V_ARR_MONTHLY` requiring five corrections that reduced draft ARR from $175,900 to $172,000. You intend
to source the seat data for the Core revenue analytic from the same instance. State whether you may, and specify the
procedures that would make the extract usable.

## Solutions to Practice Exercises

### Solution 18-1

(a) Descriptive; risk assessment only — it restates the ledger. (b) Descriptive in form but a full-population test of
details, because every term is a recorded amount and the identity is exact. (c) Diagnostic; risk assessment, and the
tool for investigating a difference found elsewhere. (d) Predictive; substantive analytical procedure.
(e) Prescriptive; none of the three — the evidence comes from testing the 60 items (Chapter 16).

### Solution 18-2

Deferred revenue movement = $78,200 − $62,300 = $15,900. Billings = $148,200 + $15,900 − $610 + $260 = **$163,750**.
Equivalently, revenue = $62,300 + $163,750 + $610 − $260 − $78,200 = $148,200. Had the $1,300 contract-asset increase
sat outside the subledger, the identity needs a $(1,300) term and billings would be $162,450 — so a bridge out by
exactly $1,300 has omitted that term rather than found a misstatement.

### Solution 18-3

FY2025: $38,600 ÷ $52,240 × 92 = 67.98 → **68.0 days**. FY2024: $30,500 ÷ $46,000 × 92 = 61.00 → **61.0 days**. At
FY2024 velocity receivables would be $52,240 × 61 ÷ 92 = **$34,637** against the actual $38,600, so **$3,963** would
not exist — **4.2 times** performance materiality of $940.

### Solution 18-4

April: 548 × $935 = $512,380 → $512; difference **nil**. May: 556 × $940 = $522,640 → $523; difference **$7**. June:
561 × $948 = $531,828 → $532; difference **$(3)**. All are below the $34 monthly threshold and the three-month total
of $4 is below the $118 segment tolerable difference. No investigation required.

### Solution 18-5

Tolerable difference = 0.40 × $940 = **$376**; per-period threshold = $376 ÷ √6 = **$153**. Alternative 1:
$376 ÷ 6 = **$63**, appropriate if the six differences are correlated — say one percentage-of-completion input drives
all six, so errors do not offset. Alternative 2: 5% of the $2,067 average two-month balance = **$103**, appropriate
with no basis for assuming independence. A weak estimation process moves you toward $63.

### Solution 18-6

FY2025 rates: expansion $27,720 ÷ $132,000 = **21.0%**; contraction **(5.6)%**; churn **(3.4)%**. NRR =
100.0 + 21.0 − 5.6 − 3.4 = **112.0%**, checked as $147,840 ÷ $132,000. The 6.0-point decline is expansion (4.0),
contraction (1.5) (5.614% − 4.100%), and churn (0.5) (3.386% − 2.900%), totalling **(6.0)**. Additional contraction
ARR at the FY2024 rate = 1.514% × $132,000 = **$1,999**.

### Solution 18-7

Write-offs = $1,350 + $1,780 − $1,900 = **$1,230**. Expected receipts = $30,500 + $163,750 − $1,230 − $38,600 =
**$154,420**; difference from actual = **$(230)**, within the $470 tolerable difference. Conclude that the three
populations are mutually consistent, provided all four inputs were independently tested. Had the difference been
$3,400, test intercompany receipts recorded gross in one entity and net in another; receipts posted to customer
deposits or unapplied cash; and contra-revenue recorded as an expense, in that order.

### Solution 18-8

Five defects. (1) **No independent source** — the 53.6% growth rate comes from management's board deck; obtain run
volumes from platform telemetry. (2) **The relationship is not predictable annually** — overage depends on consumption
against individual commitments, not total run growth; two customers doubling their runs while everyone else stays
inside their commitment produces no overage. (3) **No disaggregation** — quarterly overage of $780, $940, $1,090,
$1,390 shows Q4 up 27.5% on Q3 against 11.8% and 16.0% earlier, a spike invisible annually. (4) **Unallocated
threshold** — $940 against a $4,200 account means no misstatement short of 22% of the balance could be detected.
(5) **Uncorroborated, unquantified investigation** — "relates to timing" explains none of the $100. A sixth: the
conclusion names no assertion or assurance level.

### Solution 18-9

The bridge does **not** provide substantive evidence. AS 2305 requires an expectation precise enough to identify a
misstatement that could be material, and achieved precision here is roughly ±$1,900 — four times the $470 tolerable
difference — because items (c), (d), and (f) in Exhibit 18-7 are themselves estimates. Document it under AS 2110. The
credible contrary position is that a $1,400 residual on $172,000 is only 0.8% and therefore reasonable; that is
weaker because reasonableness is not the standard — the standard is whether the procedure could have detected a $940
misstatement, and with ±$1,900 of precision it could not.

### Solution 18-10

Model language (133 words): "*The December 2025 difference of $180 exceeded the $135 monthly threshold and was
investigated. First, we identified 2.9 thousand seats billed for the first time in the December 1 billing run under
product code CORE-SEAT-KESTREL, which our extract's filter omitted; at the contracted $40.70 per seat these account
for $118. We agreed the seat count to the Zuora December invoice run, the 61 subscriptions to the Kestrel migration
listing, and the price to the countersigned Kestrel order forms. Second, the December 31 Fivetran job failed, so the
December seat series came from a December 1 snapshot of 266.3 thousand seats rather than the daily average of 267.6
thousand; at $35.45 this accounts for a further $46. We agreed the failure to the Fivetran job log. The residual of
$16 is below both the $135 threshold and the $72 clearly trivial threshold.*"

### Solution 18-11

Model note (114 words): "*The seat-based analytic over Core subscription revenue achieved precision of only ±$1,100
because we could not reconcile the Snowflake seat extract to Zuora within 2.9 thousand seats. Because achieved
precision exceeds both the $470 tolerable difference and performance materiality of $940, the analytic cannot carry
the 50% of planned assurance assumed in the audit plan, and the observed $130 annual difference is uninformative. We
are reinstating the monetary-unit sample over account 4100 at 335 sampling units ($104,900 × 3.0 ÷ $940), with
individually significant items tested 100%. The additional effort is roughly 90 hours in the final two weeks. For
FY2026 these procedures must be performed at the interim date so a precision failure can be remediated.*"

### Solution 18-12

You may, but only after establishing the extract's reliability under AS 1105 independently of management's own
reconciliation, because W-11 means no reliance on a control over the datamart for the first three quarters. Four
procedures make it usable. Extract the same population directly from Zuora with the auditor observing, and reconcile
record counts and control totals to the Snowflake view — the step that found the omitted `CORE-SEAT-KESTREL` code.
Reconcile the row count against subscriptions × days to detect sync gaps. Inspect the view's SQL definition and
confirm its product-code and status filters against the full Zuora catalogue. And keep the seat data separate from the
ARR computation: the four `V_ARR_MONTHLY` defects and the corrections reducing draft ARR of $175,900 to $172,000
concern the ARR logic, not the subscription records.

## Review Questions

**RQ 18-1.** Name the four families of analytics and state which one can, by itself, provide substantive evidence.

**RQ 18-2.** State the one-question test distinguishing a substantive analytical procedure from a descriptive one.

**RQ 18-3.** List the four elements of a valid expectation.

**RQ 18-4.** Write the inequality relating achieved precision, the threshold, the tolerable difference, and
performance materiality, and explain why the first term must be smallest.

**RQ 18-5.** Why is a full-population recomputation in SQL a test of details rather than a substantive analytical
procedure, and which standard applies?

**RQ 18-6.** Why is a smaller observed difference not necessarily better evidence?

**RQ 18-7.** Explain the √n divisor used to convert a tolerable difference into a per-cell threshold, and name one
circumstance in which dividing by n is better.

**RQ 18-8.** What does AS 2305 require of an explanation obtained when investigating a difference?

**RQ 18-9.** Why can the ARR-to-revenue bridge not serve as a substantive analytical procedure at AtlasFlow?

**RQ 18-10.** Why is the deferred revenue roll-forward an identity rather than an expectation, and what follows for
the threshold?

**RQ 18-11.** In the three-way reconciliation, what are the three most common causes of a large unexplained
difference, and in what order should they be tested?

**RQ 18-12.** Why was AtlasFlow's stable-cohort analytic more precise than one over the whole population?

**RQ 18-13.** What are the four reconciliations required over an analytic's data, and why is a defect that reduces an
observed difference more dangerous than one that increases it?

**RQ 18-14.** State two conditions a population must satisfy before a Benford's law test can produce audit evidence,
and what a significant chi-square means when they are not.

**RQ 18-15.** When does a completed analytic justify reducing a planned sample size, and what happens if it fails?

## Answers to Review Questions

**RQ 18-1.** Descriptive (what happened), diagnostic (why), predictive (what the number should be), and
prescriptive (what to do). Only predictive analytics provide substantive evidence alone, because only they generate
an independent expectation.

**RQ 18-2.** Did I predict the number from something other than the number itself? If not, the procedure is
descriptive and cannot be substantive, however much data it processed.

**RQ 18-3.** An independent and reliable source; disaggregation to the level at which the relationship holds;
precision smaller than the threshold; and a predictable business relationship, stable over the period.

**RQ 18-4.** Achieved precision < threshold ≤ tolerable difference ≤ performance materiality. Precision must be
smallest, or a difference below the threshold is indistinguishable from a material misstatement masked by the
expectation's own imprecision.

**RQ 18-5.** It recomputes recorded amounts rather than predicting them, so there is no expectation and no threshold.
AS 2305 does not apply; AS 1105 applies in full.

**RQ 18-6.** A difference is meaningless without the precision behind it. E2 in Exhibit 18-4 produced $100 from two
offsetting management estimates and could never have disagreed with the ledger; the case study's correct expectation
produced $747 and was better evidence.

**RQ 18-7.** Dividing by √n assumes per-cell differences are largely independent. Divide by n where the cells share a
common driver, because errors then move together and do not offset.

**RQ 18-8.** That it be corroborated from a source other than the person who gave it, and quantified so the residual
can be evaluated separately. Inquiry alone cannot support a substantive conclusion.

**RQ 18-9.** Three of its four reconciling items are estimates, giving a combined tolerance of about ±$1,900 — four
times the $470 tolerable difference. File it under AS 2110 instead.

**RQ 18-10.** Every term is a recorded amount rather than a prediction, so it holds exactly. There is no threshold:
any non-zero difference is a misstatement, an omitted term, or an arithmetic error.

**RQ 18-11.** Intercompany receipts recorded gross in one entity and net in another; receipts applied to customer
deposits or unapplied cash; and contra-revenue recorded as an expense, in that order.

**RQ 18-12.** The stable cohort of 1,894 customers is closed, so revenue is fully determined by seats and price. The
whole population includes 612 new logos and 438 churned customers whose partial periods no aggregate expectation can
predict precisely.

**RQ 18-13.** Completeness, accuracy, cut-off, and authenticity. A defect that increases the difference pushes you
toward investigation and is self-correcting; one that reduces it produces a false negative with no signal.

**RQ 18-14.** The population must span several orders of magnitude and must not come from human-chosen price points
or thresholds. Where those fail — AtlasFlow's $24,000 and $48,000 bundles — a significant chi-square measures the
pricing structure, not manipulation.

**RQ 18-15.** Only where the completed analytic achieved the precision the plan assumed, and only for the assertions
it addresses. If it fails, the planned sample returns in full, and late.

## Key Definitions

**Annual recurring revenue (ARR).** The annualized value of recurring contracts in force at a point in time. An
operating metric with no US GAAP definition; not a revenue measure.

**Audit data analytic.** A computational technique applied to a population of data to produce audit evidence. Turns on
purpose, not tooling.

**Benford's law.** In populations spanning several orders of magnitude and not built from chosen price points, the
leading digit is 1 about 30.1% of the time, 2 about 17.6%, down to 4.6% for 9.

**Cohort analysis.** Partitioning customers by a shared starting characteristic, usually period of first contract, so
groups with homogeneous in-period movement can be compared.

**Completeness and accuracy of data (C&A).** Testing AS 1105 and AU-C 500 require before entity-produced information
may be used as evidence: counts and control totals to source, re-performance of transformation logic, cut-off, and
provenance.

**Days sales outstanding (DSO).** Gross receivables ÷ billings for a period × days in the period. AtlasFlow:
$38,600 ÷ $52,240 × 92 = 68.0 days.

**Descriptive analytic.** Summarizes what is recorded without predicting it. Supports risk assessment only.

**Diagnostic analytic.** Decomposes a change into drivers. It explains; it does not corroborate the recorded amount.

**Disaggregation.** Building and comparing an expectation below the level the financial statements present. Raises
precision only where the relationship is homogeneous within each cell.

**Expectation.** The auditor's independently developed prediction of a recorded amount, built from data outside the
account tested.

**False-positive rate.** The proportion of selected items that prove not to be findings. AtlasFlow's six-rule set ran
at 98.5%; the co-occurrence set at 75.8%.

**Gross revenue retention (GRR).** One hundred percent less contraction and churn rates on the NRR denominator.
AtlasFlow FY2025: (132,000 − 7,410 − 4,470) ÷ 132,000 = 91.0%.

**Net revenue retention (NRR).** Closing ARR of a fixed opening cohort, with expansion and net of contraction and
churn, over that cohort's opening ARR: $147,840 ÷ $132,000 = 112.0%, excluding self-serve and acquired ARR.

**Precision (of an expectation).** The range within which the expectation would fall were the recorded amount free of
misstatement. Estimable from dispersion of non-exception differences or parameter sensitivity.

**Predictive analytic.** Generates an expectation from independent data. The only family capable of constituting a
substantive analytical procedure under AS 2305 or AU-C 520.

**Prescriptive analytic.** Directs effort — a scoring model, selection rule, or stratification. Produces a selection,
not evidence.

**Process mining.** Reconstructing actual event sequences from system timestamps and comparing sequences and cycle
times to the documented process.

**Substantive analytical procedure.** Evaluation of financial information through analysis of plausible relationships
to obtain substantive evidence about assertions, requiring an independent expectation, a predetermined threshold,
comparison to the recorded amount, and corroborated investigation of differences (AS 2305; AU-C 520).

**Three-way reconciliation (revenue–receivables–cash).** Links revenue to billings through the deferred revenue
movement, and billings to cash through the receivable movement and write-offs.

**Threshold for investigation.** The difference accepted without investigation, fixed before the comparison and
derived from the tolerable difference adjusted for the number of cells.

**Tolerable difference.** The aggregate unexplained difference acceptable from one substantive analytical procedure,
set as a stated fraction of performance materiality reflecting the assurance it carries.

**Variant (process mining).** A distinct observed event sequence in an event log. AtlasFlow's order-to-cash log had
eight across 4,806 activations, the standard path accounting for 3,914.

## Chapter Summary

1. An analytic is a prediction; of the four families, only predictive analytics carry substantive evidence alone.
2. The same query can be a risk assessment procedure, a substantive analytical procedure, or a full-population test
   of details, and conflating those regimes causes most defective analytics work.
3. A valid expectation requires an independent and reliable source, disaggregation to the level at which the
   relationship holds, precision smaller than the threshold, and a predictable business relationship.
4. Most failures are precision failures: of four expectations for the same $104,900, only the monthly seat-based
   version, at ±$152, could detect $940. A small difference from an imprecise expectation is not evidence.
5. Derive the threshold from performance materiality by choosing the share of assurance carried and dividing by √n for
   n cells — $470 and $135 at AtlasFlow — and fix it before computing the difference.
6. Investigating a difference means testing your own expectation first, then obtaining a quantified explanation
   corroborated independently of its source: December's $180 resolved to $118, $46, and a $16 residual.
7. The ARR-to-revenue bridge, at ±$1,900 of precision, is a risk assessment procedure; the deferred revenue
   roll-forward and the three-way reconciliation are identities that tie exactly.
8. Metrics convert to dollars: six points of NRR is $5,280 of unearned expansion, $1,999 of contraction, and $641 of
   churn; seven days of DSO is $3,963 of receivables that would not exist at prior-year velocity.
9. Outlier rules must be judged by false-positive rate, and Benford's law yields no evidence on a price-listed
   population — a χ² of 86.8 on Q4 invoices is an artifact of $24,000 and $48,000 bundles.
10. Data completeness and accuracy is where analytics collapse: one omitted product code moved the December
    expectation by $118 against a $135 threshold.
11. Documentation must permit re-performance, and analytics reduce sample sizes only to the extent of the precision
    actually achieved — unknown until they are complete.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Performance materiality of $940, the $72 clearly trivial threshold, the $132,000 cohort denominator | Chapter 3 | Every threshold here derives from these figures |
| Subscription revenue recognition, ramped contracts, the deferred revenue roll-forward, RPO | Chapters 5 and 6 | The accounting the analytics predict |
| Q4 billings of $52,240 and $46,000, the DSO disclosure, the allowance | Chapter 7 | Inputs to §18.9 and the credit-loss work it feeds |
| Reliability of information produced by the entity; the Snowflake datamart and W-11 | Chapter 12 | The C&A framework §18.13 applies |
| Sample size determination and monetary-unit sampling | Chapter 15 | The 335-unit computation in §18.14 |
| Journal entry analytics and risk-based selection criteria | Chapter 16 | Criteria design, which §18.12 treats generally |
| Revenue fraud schemes and backdating | Chapter 17 | The V7 variant and misstatement U-3 |
| Accumulating differences; the final analytical review | Chapter 19 | Where the $16 and $(33) residuals are aggregated |

## Further Reading

- PCAOB AS 2305, *Substantive Analytical Procedures* — the governing standard; read it with AS 2110 and AS 2401 on
  the required revenue analytics.
- PCAOB AS 1105, *Audit Evidence*, on information produced by the company, and AS 1215, *Audit Documentation*, for
  the re-performance standard governing analytics documentation.
- PCAOB AS 2810, *Evaluating Audit Results*, for the overall review and accumulated differences.
- AICPA AU-C 520 and AU-C 500 for private-company engagements; AU-C 520 adds an explicit end-of-audit requirement.
- The AICPA's guide to audit data analytics and its practice aids on technology in the audit.
- FASB ASC 606-10 (incl. 606-10-50) and ASC 326-20; the SEC's 2020 MD&A guidance on key performance indicators such
  as ARR and NRR, with AS 2710 / AU-C 720 on other information.


