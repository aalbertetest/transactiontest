# Chapter 15 — Audit Sampling

> A sample is a bet that the part resembles the whole, and sampling design exists to make that bet defensible: define
> the whole, give every part of it a chance of selection, choose enough, and — the step most files omit — say how wrong
> the bet could still be. Brightline LLP's FY2025 file holds a sample of 25 order forms that produced one deviation and
> a conclusion of "isolated." The arithmetic in this chapter shows why that conclusion was wrong.

## Learning Objectives

- **LO 15.1** Distinguish populations for which sampling is the right extent from those calling for 100% examination,
  selection of specific items, or a substantive analytical procedure.
- **LO 15.2** Identify what changes, and what does not, when a file moves from non-statistical to statistical sampling.
- **LO 15.3** Name the two components of sampling risk in each testing context and classify each as an effectiveness or
  an efficiency concern.
- **LO 15.4** Reconcile a sampling frame to the ledger, select by three acceptable methods, and explain why block
  selection is not one of them.
- **LO 15.5** Compute an attribute sample size and a computed upper deviation limit and conclude against a tolerable
  deviation rate.
- **LO 15.6** Compute a monetary-unit sample size and interval, select with a random start, compute taints, and compute
  projected misstatement, basic precision, the incremental allowance, and the upper misstatement limit.
- **LO 15.7** Compute projected misstatement under mean-per-unit, difference, and ratio estimation and choose the
  estimator the misstatement pattern supports.
- **LO 15.8** Set an individually-significant-item threshold, reconcile tolerable misstatement to performance
  materiality, and compute the effect of each on extent.
- **LO 15.9** Evaluate a sample result qualitatively as well as quantitatively and draft the documentation AS 1215 and
  AU-C 230 require.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2315, *Audit Sampling* | Governs the FY2025 AtlasFlow audit: relate the sample to the relevant assertion; define the population appropriately; select so the sample can be expected to be representative; project misstatement found to the population; consider sampling risk in evaluating the result. |
| AICPA | AU-C 530, *Audit Sampling* | The private-company equivalent. Two differences matter: AU-C 530 expressly addresses treating an item as an **anomaly** on a demanding condition, and expressly requires investigation of the nature and cause of deviations and misstatements. AS 2315 reaches similar results through AS 2810. |
| PCAOB / AICPA | AS 2105 / AU-C 320 | Require tolerable misstatement at the account level. Chapter 3 set overall materiality $1,450, performance materiality $940, clearly trivial $72, and tolerable misstatement of $705 for significant-risk revenue populations and $940 elsewhere. |
| PCAOB / AICPA | AS 2301 / AU-C 330 | Extent must respond to assessed risk. Sample size is that requirement expressed arithmetically. |
| PCAOB / AICPA | AS 2810 / AU-C 450 | Require accumulation of identified misstatements, projection of misstatements found in a sample, and evaluation of uncorrected misstatements individually and in aggregate. |
| PCAOB | AS 2201 | A deviation is evaluated as a control deficiency whether or not the sampling conclusion can be rescued. |
| PCAOB / AICPA | AS 2305 / AU-C 520 | Substantive analytical procedures. An analytic meeting them at sufficient precision reduces or replaces a sample; one that does not, cannot. |
| PCAOB / AICPA | AS 1215 / AU-C 230 | Documentation sufficient for an experienced auditor with no prior connection to re-perform the work. |
| AICPA | Audit Guide covering audit sampling | Non-authoritative. Source of the reliability factors, expansion factors, and attribute tables used here; firm methodology is not a professional requirement. |

## Prerequisites and Chapter Dependencies

Read Chapter 3 first: this chapter consumes its materiality figures and never re-derives them. Chapter 2 supplies the
assessed risks that decide which populations carry $705 rather than $940, and Chapter 14 what a test of controls is
trying to establish. Chapter 7 applies these mechanics to the receivable confirmation, Chapter 18 to the analytics that
sometimes displace sampling, and Chapter 19 to the final evaluation.

## 15.1 What Sampling Is, and When It Is the Wrong Technique

**Audit sampling** is applying an audit procedure to fewer than 100% of the items in a population, selected so as to
give a reasonable basis for a conclusion about the *entire* population. Both halves matter. If you do not intend to
conclude on the whole population you are not sampling; you are examining specific items and obtain no evidence about
the rest. If the selection method denies some items any chance of selection, the population conclusion is unsupported
however many items you examined. Sampling is one of four extents, the others being 100% examination, selection of
specific items, and a substantive analytical procedure.

**Exhibit 15-1. Extent decision for five FY2025 AtlasFlow populations (in thousands).**

| Population | Size | Extent | Why not sampling |
| --- | --- | --- | --- |
| Enterprise receivables at or above $470 | 22 accounts, $20,290 | 100% examination | Any one item could hold half of performance materiality. |
| Enterprise receivables below $470 | 644 accounts, $16,610 | Sampling | Many items, each too small to matter alone; the aggregate matters. |
| Self-serve (Stripe) receivables | 11,400 accounts, $1,700 | 100% match to the Stripe settlement file | One automated attribute covers the population more cheaply and precisely than a sample. |
| Manual entries with a revenue line and a non-standard offset | 34 entries, $3,900 | Selection of specific items | Risk-selected, not representative; supports no conclusion about the other 4,878 entries. |
| Monthly Controller review of the RevPro-to-GL journal (I-3) | 12 occurrences | 100% of the interim population | With 12 occurrences, sampling theory contributes nothing. |

Three failure modes recur: projecting from a risk-based selection; sampling a population that cannot contain the
misstatement, as when invoices are tested for accuracy but the assertion at risk is completeness; and calling a query
"100% testing" when only one of several necessary attributes was machine-testable (§15.10).

## 15.2 Statistical Versus Non-Statistical Sampling

An application is **statistical** if it has both random-based selection and sampling risk measured with probability
theory. Absent either it is **non-statistical**. AS 2315 and AU-C 530 permit both, and neither is more rigorous as a
matter of requirement.

**Exhibit 15-2. What changes and what does not.**

| Element | Non-statistical | Statistical |
| --- | --- | --- |
| Population reconciled; tolerable and expected misstatement set before selection; every exception investigated; projection; qualitative evaluation | Required | Required |
| Selection method | Expected to be representative; haphazard permitted | Must be random-based |
| Sample size | Firm table with an embedded "assurance factor" | Computed from an explicit reliability factor |
| Allowance for sampling risk | Not quantified; addressed by leaving margin | Quantified, producing an upper limit |

The practical difference is the last row. A non-statistical evaluation says "projected misstatement of $29 against
tolerable misstatement of $940 leaves a wide margin." A statistical evaluation says "the upper misstatement limit is
$748 against $940." The second is falsifiable and the first is not. The corollary matters more: §15.7 shows that a
non-statistical sample sized at an assurance factor of 3.0 is numerically identical to a monetary-unit sample at a 5%
risk of incorrect acceptance with zero expected misstatement. Non-statistical sampling in a modern methodology is
statistical sampling with the vocabulary removed.

## 15.3 Sampling Risk and Non-Sampling Risk

**Sampling risk** is the risk that the conclusion from the sample differs from the conclusion the same procedure would have
produced on the whole population; it falls only with more items or with stratification. **Non-sampling risk** is every
other reason the conclusion can be wrong — the wrong population, the wrong procedure, careless execution, an exception seen
and not recognised, an extract missing 400 rows — and it is reduced by supervision, review, and testing the data. A sample
of 500 drawn from an incomplete aged trial balance has negligible sampling risk and unbounded non-sampling risk.

**Exhibit 15-3. The four sampling risks.**

| Context | Risk | The error | Consequence | Class |
| --- | --- | --- | --- | --- |
| Controls | **Overreliance** | Sample says rely; true rate exceeds the tolerable rate | Substantive extent too low, misstatement undetected; an ineffective control reported as effective | **Effectiveness** |
| Controls | **Underreliance** | Sample says do not rely; the control is effective | Unnecessary substantive work; a deficiency reported that does not exist | **Efficiency** |
| Details | **Incorrect acceptance** | Sample says not materially misstated; it is | An unmodified opinion on materially misstated financial statements | **Effectiveness** |
| Details | **Incorrect rejection** | Sample says materially misstated; it is not | Unnecessary procedures; an adjustment the evidence does not support | **Efficiency** |

The asymmetry drives design. Sample size formulas control the effectiveness risks directly — the reliability factor is
a function of the risk of incorrect acceptance and nothing else. The efficiency risks are controlled indirectly, by
setting expected misstatement realistically so a normal level of misstatement does not breach the limit, and by
extending rather than concluding on a failed result.

The percentages are conventions. Brightline sets the risk of incorrect acceptance at 5% where no control reliance is
planned and 10% where a tested, effective control and a corroborating analytic both exist. At AtlasFlow the second
condition is almost never met, because the unremediated deficiencies W-1, W-2, W-5, W-6, W-7, W-12 and W-13 leave the
revenue and receivable ITGCs unreliable. Nearly every FY2025 test of details is therefore designed at 5%, which the case
study prices at 103 additional selections in one population.

## 15.4 The Population, the Sampling Unit, and the Frame

The **population** is the set of data you intend to conclude on; the **sampling frame** is the list you actually select
from. Any difference caps the value of the work, so the first workpaper reconciles the frame to the ledger.

**Exhibit 15-4. Sampling frame reconciliation, gross accounts receivable at December 31, 2025 (in thousands).**

| Step | Amount | Source |
| --- | --- | --- |
| Account 1200, receivables — trade (enterprise) | 36,900 | NetSuite trial balance (a) |
| Account 1205, receivables — Stripe self-serve | 1,700 | NetSuite trial balance (a) |
| **Gross receivables per the general ledger** | **38,600** | Ties to the continuing case, §3.3 |
| Total of the aged trial balance extract used as the frame | 38,600 | Snowflake `AR_AGING_20251231`; 3,140 enterprise + 11,400 self-serve rows (b) |
| **Unreconciled difference** | **—** | |
| Less: self-serve subpopulation tested 100% by subsequent settlement | (1,700) | Chapter 7, §7.10 |
| Less: 31 credit balances of $310 held in a separate view, tested as liabilities | — | Not within the $36,900 (c) |
| **Enterprise frame subject to selection** | **36,900** | |

Tick marks: (a) agreed to the account detail report and to the balance sheet caption of $36,700 net of the $1,900
allowance. (b) Row count and total agreed to the source system; bucket totals re-added to §3.3
($22,550 + $8,190 + $3,740 + $1,970 + $1,440 + $710 = $38,600). (c) An extension to the continuing case.

Two exclusions are deliberate. Account 1210, the $1,900 allowance, is an estimate, not a population of items. Account
1220, the $3,400 of unbilled receivables and contract assets, is a separate population with its own tolerable
misstatement (Chapter 7, §7.6).

The **sampling unit** is the item selected. If it is the customer account, each of 644 accounts has an equal chance
regardless of size; if the individual dollar (§15.8), larger balances are proportionally more likely to be selected,
which is what you want when the risk is overstatement. For a completeness assertion the unit must sit outside the
accounting records — sampling the deferred revenue subledger to test whether deferred revenue is complete is circular,
because an unrecorded contract liability is not in the subledger. There the unit is the order form or the provisioning
record.

**Exhibit 15-5. Selection methods applied to the 644-account residual receivable frame.**

| Method | Mechanics on this frame | Acceptable? |
| --- | --- | --- |
| Unrestricted random | Number the rows 1–644; draw 54 without replacement with a seeded generator; retain seed and list | Statistical. The default. |
| Systematic with a random start | Interval 644 ÷ 54 = 11.93 → 12; a random start from 1–11 gives 7; select rows 7, 19, 31, ... 643 | Statistical, unless the frame's order is periodic with the interval. Sort by account number, never by balance. |
| Monetary-unit | Cumulate $16,610; interval $233.33; random start $18.40; take the account holding each hit | Statistical, and preferred where the risk is overstatement (§15.8). |
| Haphazard | Scroll and pick 54 without conscious bias | Non-statistical only; no selection probability is known. |
| Block | All accounts whose only invoice was issued December 22–31, 2025 | **Not acceptable.** |

Block selection fails for a specific reason: clusters in accounting data differ systematically, and the December 22–31
block is dominated by the 41% of Q4 ACV signed in the final five business days — a subpopulation with a different cut-off
risk, approval path, and customer mix than the year. A block of 54 accounts yields roughly one observation and gives
every account outside it a zero probability of selection. It remains an excellent *risk-based selection*, and Chapter 4
tests the December 24–31 population for that reason; what you may not do is project from it. Haphazard selection is
measurably biased toward the top and bottom of a list, round numbers, and familiar names, so prefer a random draw.

## 15.5 Attribute Sampling for Tests of Controls

Attribute sampling estimates the rate of occurrence of a binary condition. In a test of controls that condition is a
**control deviation**: an instance in which the control did not operate as described. A deviation is not a misstatement. A
missing approval on a correctly priced, correctly dated order form is a deviation only; a properly approved order form
recorded a month early is a misstatement only. Both are evaluated, on different scales.

Five inputs determine the sample size. The **population** is all occurrences of the control in the period — for RC-3, the
Deal Desk verification of each order activated in Salesforce CPQ, the January 1 to October 31, 2025 population is 3,940
activated orders; population size is nearly irrelevant to sample size above a few thousand items. The **sampling unit** is
one occurrence. The **tolerable deviation rate (TDR)** is the maximum rate consistent with the planned reliance, and
practice clusters at 5% to 10% where significant reliance is placed and 10% to 20% where reliance is limited. The
**expected deviation rate (EDR)** comes from prior-year and interim results, inquiry, and design, and must be well below
the TDR — if your expectation approaches your tolerance, this is not a control to plan on. The **risk of overreliance** is
5% or 10%.

The design rule, using Poisson reliability factors, is that the sample must be large enough that if the expected number
of deviations occurs, the computed upper deviation limit still does not exceed the tolerable rate: **n = RF(k) ÷ TDR**,
where k is the number of deviations allowed. Then confirm n × EDR ≤ k.

**Exhibit 15-6. Attribute sample sizes from n = RF(k) ÷ TDR, rounded up.**

| TDR | 10% risk, allow 0 (RF 2.31) | 10%, allow 1 (RF 3.89) | 5%, allow 0 (RF 3.00) | 5%, allow 1 (RF 4.75) |
| --- | --- | --- | --- | --- |
| 5% | 47 | 78 | 60 | 95 |
| 9% | 26 | 44 | 34 | 53 |
| 10% | 24 | 39 | 30 | 48 |
| 20% | 12 | 20 | 15 | 24 |

The Poisson rule is a conservative approximation of the exact binomial, and the difference sources a number every
practitioner has seen and few can explain: 25. The exact binomial upper limit for zero deviations in 25 at a 10% risk
of overreliance is 8.80%, because 0.10^(1/25) = 0.9120 and 1 − 0.9120 = 0.0880. That is below 9%, so 25 items support a
9% tolerable rate on the binomial, while Poisson gives 2.31 ÷ 25 = 9.24% and would require 26. Firm tables specifying
25 for a manual control operating many times per day at moderate reliance are built on the binomial and a 9% tolerable
rate with zero expected deviations — defensible, with no room in it, since it fails on the first deviation.

**Evaluating the result.** The **computed upper deviation limit (CUDL)** is the upper bound of a one-sided interval on
the population deviation rate, approximated as RF(deviations found) ÷ n. If CUDL ≤ TDR the result supports the planned
reliance; if not, it does not, and the sample deviation rate is irrelevant to that comparison. One deviation in 25 is a
4% sample rate, and a 4% sample rate is entirely consistent with a population rate above 9%.

**Exhibit 15-7. Evaluation of four FY2025 control tests, risk of overreliance 10%.**

| Control | Frequency | Population, Jan 1 – Oct 31 | n | Deviations | TDR | CUDL | Conclusion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| RC-3 Deal Desk verification of an activated order | Many per day | 3,940 orders | 25 | 1 | 9% | 3.89 ÷ 25 = **15.6%** (binomial 14.7%) | Does not support reliance — see the case study |
| RC-12 Billing Analyst clears the CPQ-to-Zuora error queue (I-1) | Daily | 214 business days | 30 | 0 | 9% | 2.31 ÷ 30 = **7.7%** | Supports reliance |
| RC-7 Controller approves the RevPro-to-GL journal (I-3) | Monthly | 10 occurrences | 10 | 0 | n/a | n/a | 100% of the interim population; not a sampling application |
| RC-19 Quarterly user access review (W-3) | Quarterly | 4 occurrences | 4 | 2 | n/a | n/a | 100% examined. Performed annually, not quarterly, and Q2 was 41 days late: a design failure, not a sampling question |

The bottom two rows carry two lessons. Low-frequency controls are not sampled — with 4 or 12 occurrences you examine all
of them. And where the control as performed differs from the control as described, no sample size saves the conclusion:
you have tested a control that does not exist.

**When the result is unexpected.** A CUDL above the tolerable rate has four responses, in descending order of preference:
test the exposed subpopulation 100% and conclude separately on the remainder, where the cause is identifiable and
bounded; extend randomly from the untested remainder, which for a 9% rate with one deviation at 10% risk of overreliance
requires 3.89 ÷ 0.09 = 43.2, so 44 items on Poisson and 42 on the binomial; test a different control addressing the same
risk; or abandon reliance and increase substantive extent. What you may not do is raise the tolerable rate after seeing
the result, re-characterise the deviation as "not applicable," or replace the deviating item.

## 15.6 Tolerable Misstatement, Stratification, and Individually Significant Items

**Tolerable misstatement** is the sampling input corresponding to materiality: set for each population subjected to a
test of details, before selection, never higher than performance materiality. Chapter 3, §3.11 set it — $705 for
significant-risk populations (Core and Insight subscription revenue, deferred revenue completeness), being 75% of the
$940 performance materiality, and $940 elsewhere including gross receivables. Performance materiality is an
entity-level amount set once to control aggregation risk *across* populations; tolerable misstatement is a
procedure-level amount that also controls aggregation *within* a population when more than one procedure addresses it.
It is the denominator of every sample size formula here, so lowering it raises extent roughly proportionally, and a file
in which it moved after a misstatement was found cannot be defended.

**Stratification** divides a population into subpopulations more homogeneous than the whole. Its purpose is precision:
the allowance for sampling risk depends on the variability of what is sampled, and balances ranging from $1 to $2,410 are
wildly variable while balances from $100 to $470 are not. The limiting case is a stratum sampled at 100% — the
**individually significant items**, whose size makes any sampling conclusion about them worthless.

The threshold is the highest-leverage judgment in the design. Brightline used 50% of performance materiality, $470, on the
stated test that after removal no single untested item can hold half of performance materiality alone. Defensible practice
runs from about 25% of performance materiality ($235, sweeping in more items) to 100% ($940, which at AtlasFlow would
capture only 9 accounts and $12,150, leaving $24,750 to be sampled). It moves down when the population is skewed or the
largest items carry risk indicators; up when 100% testing of the key stratum costs more than the sample it displaces.

**Exhibit 15-8. Stratification of gross receivables (in thousands).**

| Stratum | Accounts | Balance | Treatment |
| --- | --- | --- | --- |
| Self-serve, all balances | 11,400 | 1,700 | 100% match to the Stripe settlement file |
| 1 — enterprise, at or above $470 | 22 | 20,290 | 100% examination (individually significant) |
| 2 — enterprise, $100 to under $470 | 74 | 12,610 | Sampled |
| 3 — enterprise, $10 to under $100 | 168 | 3,290 | Sampled |
| 4 — enterprise, above nil to under $10 | 402 | 710 | Sampled |
| 5 — enterprise, nil balance | 2,474 | — | Not sampled; no assertion at risk on a nil balance |
| **Gross receivables** | **14,540** | **38,600** | |
| **Residual frame (strata 2 + 3 + 4)** | **644** | **16,610** | 72 monetary-unit hits (§15.8) |

Check: 20,290 + 12,610 + 3,290 + 710 = 36,900 enterprise, plus 1,700 self-serve = 38,600; 12,610 + 3,290 + 710 = 16,610
and 74 + 168 + 402 = 644.

The payoff is computable. Sampling the undivided $36,900 enterprise frame at the walkthrough's $233.33 interval would take
$36,900 ÷ $233.33 = 158.1, so 159 hits. Stratifying reduces that to 22 items examined at 100% plus 72 hits on the
residual, falling on 68 distinct accounts — 90 items rather than 159, a 43% reduction, with *higher* precision because the
22 largest balances contribute no sampling risk. Each exclusion making the reduction possible is a scope decision to be
stated and supported, not a quiet deletion from a spreadsheet.

## 15.7 Non-Statistical Sampling for Tests of Details

Most tests of details in most firms are non-statistical, sized by a formula of this shape:

**n = (population book value − individually significant items) ÷ tolerable misstatement × assurance factor**

**Exhibit 15-9. Non-statistical sample sizes on the $16,610 residual frame, tolerable misstatement $940.**

| Evidence and risk profile | Assurance factor | Computation | n |
| --- | --- | --- | --- |
| Lower RMM; a tested, effective control; a corroborating analytic | 0.7 | 16,610 ÷ 940 = 17.67; × 0.7 = 12.37 | 13 |
| Moderate RMM; no control reliance; a corroborating analytic at acceptable precision | 1.5 | 17.67 × 1.5 = 26.51 | 27 |
| Moderate RMM; no control reliance; no other substantive evidence | 2.0 | 17.67 × 2.0 = 35.34 | 36 |
| Significant risk; no control reliance; no other substantive evidence | 3.0 | 17.67 × 3.0 = 53.01 | 54 |

The factors are firm methodology, not a requirement, and they vary across firms; the structure does not, because the
mathematics forces it. The bottom row is the tell: 16,610 × 3.00 ÷ 940 = 53.01 is exactly the monetary-unit size at a
5% risk of incorrect acceptance with zero expected misstatement, because 3.00 is the Poisson reliability factor for
zero misstatements at 5%. The assurance factor is a reliability factor.

Selection must still be representative and evaluation must still project. Only the quantified allowance is given up, and
the compensating discipline is to leave visible margin: projected misstatement of $500 against tolerable misstatement of
$940 is not a pass, because the unquantified sampling risk could easily be $400.

## 15.8 Monetary-Unit Sampling

**Monetary-unit sampling (MUS)**, also called probability-proportional-to-size or dollar-unit sampling, treats each
recorded dollar as a sampling unit and selects dollars systematically from the cumulated population; the account holding a
selected dollar is examined. Larger items are proportionally more likely to be selected, any item at least as large as the
sampling interval is certain to be selected, and no weighting arithmetic is needed.

MUS is built for overstatement and is the natural design for existence of receivables and occurrence of revenue. It is
poor in three situations: it cannot select an item recorded at zero or omitted entirely, so it gives no evidence on
completeness; it handles understatement badly, because a taint can exceed 100% and the evaluation formulas assume it
does not; and it becomes inefficient when misstatements are numerous, because each adds an incremental allowance.

**Sample size: n = (BV × RF) ÷ (TM − (EM × EF))**, where BV is the book value sampled, RF the reliability factor for
zero misstatements at the chosen risk of incorrect acceptance, TM tolerable misstatement, EM expected misstatement, and
EF the expansion factor. The interval is **J = (TM − (EM × EF)) ÷ RF**, and BV ÷ J = n identically.

**Exhibit 15-10. Poisson reliability factors and expansion factors.**

| Misstatements | Reliability factor, 5% risk of incorrect acceptance | Incremental factor, 5% | Reliability factor, 10% | Incremental factor, 10% |
| --- | --- | --- | --- | --- |
| 0 | 3.00 | — | 2.31 | — |
| 1 | 4.75 | 1.75 | 3.89 | 1.58 |
| 2 | 6.30 | 1.55 | 5.33 | 1.44 |
| 3 | 7.76 | 1.46 | 6.69 | 1.36 |
| 4 | 9.16 | 1.40 | 8.00 | 1.31 |
| **Expansion factor** | **1.6** | | **1.5** | |

The incremental factor for the kth misstatement is RF(k) − RF(k−1). The expansion factor inflates expected misstatement
in the denominator because expected misstatement is itself an estimate and the design must survive being a little wrong
about it.

**Evaluation** has four components, and a file reporting only the first has not evaluated anything.

1. **Projected misstatement.** For an item smaller than the interval, compute the **taint** — misstatement ÷ book value —
   and multiply by the interval. For an item at least as large as the interval, which was certain to be selected and
   represents only itself, take the misstatement at face value with no extrapolation.
2. **Basic precision.** RF(0) × J: the allowance for misstatement the sample did not encounter. Present in every MUS
   evaluation including a clean one, and the most commonly omitted number in practice.
3. **Incremental allowance.** Rank the projected misstatements of below-interval items descending and sum (incremental
   factor − 1) × projected misstatement, taking the incremental factors in order. Items at or above the interval receive
   none.
4. **Upper misstatement limit (UML)** = the sum of the three. If UML ≤ TM, the sample supports the conclusion that the
   population is not overstated by more than tolerable misstatement at the chosen risk.

Component 2 has a structural implication the walkthrough and Exercise 15-7 both exploit. When expected misstatement is
zero, basic precision equals RF(0) × (TM ÷ RF(0)) = TM exactly, so a zero-expectation design passes only if the sample
finds nothing at all. Setting expected misstatement above zero buys room at the cost of a larger sample; that trade-off
is the whole of MUS planning judgment.

## 15.9 Classical Variables Sampling

Classical variables sampling estimates a population amount from the sample mean using normal-theory intervals. Assume a
random — not monetary-unit — sample of 100 of the 644 residual receivable accounts, with a sample book value of $2,480,
an audited value of $2,452, and a standard deviation of the 100 per-unit differences of $1.49.

**Exhibit 15-11. Three classical estimators on the same sample (in thousands).**

| Estimator | Computation | Estimated audited value | Projected misstatement |
| --- | --- | --- | --- |
| Mean-per-unit | 2,452 ÷ 100 = 24.52; × 644 accounts | 15,790.88 | 16,610.00 − 15,790.88 = **819.12** |
| Difference | (2,480 − 2,452) ÷ 100 = 0.28; × 644 = 180.32 | 16,429.68 | **180.32** |
| Ratio | 2,452 ÷ 2,480 = 0.988710; × 16,610 | 16,422.46 | 16,610.00 − 16,422.46 = **187.54** |

The three answers differ by a factor of four because they use different information. Mean-per-unit ignores book value
and estimates the population from audited amounts alone, so its precision depends on the variability of the balances,
which is enormous. Difference and ratio estimation use each item's book value as a covariate and estimate only the
*misstatement*, whose variability is tiny.

**Allowance for sampling risk, difference estimation** = Z × N × (s_d ÷ √n) × √(1 − n ÷ N), where Z is the one-sided
normal deviate for the risk of incorrect acceptance (1.645 at 5%) and the final term is the finite-population correction.

- s_d ÷ √n = 1.49 ÷ 10 = 0.149; correction = √(1 − 100 ÷ 644) = √0.844720 = 0.919086
- Allowance = 1.645 × 644 × 0.149 × 0.919086 = 1,059.38 × 0.149 = 157.85; × 0.919086 = **145.08**
- Upper limit = 180.32 + 145.08 = **325.40** against tolerable misstatement of $940. Accept.
- On mean-per-unit, where the standard deviation of audited values is $58.40, the allowance is **5,686.2** — an upper
  limit of $819 + $5,686 says nothing about a $940 threshold.

**Difference or ratio?** Difference estimation assumes misstatement is unrelated to item size — a $12 cut-off error is
$12 whether the balance is $185 or $1,850. Ratio estimation assumes proportionality. AtlasFlow's cut-off misstatements
are whole invoices or invoice lines in the wrong period, so they scale with the invoice, and Chapter 7, §7.5 accordingly
used ratio projection. Fixed-amount errors — a flat misposted charge, a rounding convention, a repeated transposition —
call for difference estimation. Where the pattern is unclear, compute both and carry the more conservative, here ratio
at $187.54 against difference at $180.32.

The classical planning formula, n = [N × s_d × Z ÷ (TM − EM)]², is unusable in advance for the same reason it looks
attractive: on these figures it returns [644 × 1.49 × 1.645 ÷ 790]² = 1.998² = **4**, because s_d must be guessed before
sampling and is unstable when 94 of 100 differences are zero. Hence the default to MUS and firm minimum sample sizes.

## 15.10 Projection, Qualitative Evaluation, Full-Population Testing, and Documentation

**Known versus projected.** A **known misstatement** is one whose amount is determined for a specific item; in a stratum
tested at 100%, every misstatement is known and none is projected. A **projected misstatement** estimates the
misstatement in the untested portion of a sampled population, and AS 2810 and AU-C 450 require the projected amount to be
accumulated. A file carrying the $85.9 found in a sample covering $23,590 of a $36,900 population, but not the $184.9 it
projects to, has understated accumulated misstatement by $99 — and every sample in the file understates it the same way,
which is how an immaterial file becomes a material one.

**Every misstatement is evaluated qualitatively as well as quantitatively.** A $46 misstatement is 3.2% of overall
materiality and quantitatively trivial; if its cause is an order form signed after the service start date, it is also
evidence about occurrence, about a control, and possibly about intent. Ask of every misstatement: what caused it; is the
cause systematic; is the exposed subpopulation identifiable and bounded; is it a control failure as well as a
misstatement; and does it change the assessed risk. AU-C 530 makes investigation of cause explicit; under PCAOB standards
the obligation arrives through AS 2810 and AS 2401.

**Anomalies.** AU-C 530 permits treating an item as an **anomaly** — demonstrably not representative — only on a high
degree of certainty, on affirmative evidence. A plausible narrative is a hypothesis about cause, and a cause that
operated for a period is a reason to expect *more* deviations in that period, not fewer. AS 2315 has no anomaly concept,
so on a PCAOB engagement the answer to "can we call it isolated" is almost always no.

**When full-population testing replaces sampling.** Three conditions must hold. The data must be complete and accurate,
which means reconciling the extract to the ledger and testing the fields used — at AtlasFlow weakness W-11 means a
Snowflake extract cannot be assumed reliable without agreeing it to NetSuite. The attribute must be fully
machine-evaluable: whether cash cleared is, whether an approval was appropriate is not. And every exception must be
examined, because a query returning 47 exceptions and a workpaper examining 10 of them is a sample with no design. Where
the conditions fail, the usual outcome is that the query shrinks the population still to be sampled rather than
eliminating the sample.

**Documentation.** AS 1215 and AU-C 230 require that an experienced auditor with no prior connection be able to re-perform
the work. For a sample that means recording the objective and assertion; the population and its reconciliation; the
sampling unit; the individually-significant-item threshold; tolerable misstatement, the risk of incorrect acceptance or
overreliance, and expected misstatement, each with its basis; the sample size computation showing every input; the
selection method including seed, random start, and interval; the procedures and results with a tick-mark legend; and the
evaluation — projection, the allowance for sampling risk, the qualitative assessment of each exception, and the
conclusion.

## Step-by-Step Walkthrough: Designing and Evaluating a Monetary-Unit Sample of AtlasFlow's Gross Receivables

Brightline's FY2025 receivable test of details was the stratified non-statistical confirmation sample in Chapter 7. This
walkthrough designs the *same population* as a formal monetary-unit sample, at WP 3200-27, because two evaluations of one
population show what a statistical design adds. Amounts are in thousands.

**Step 1. Confirm that sampling is the right technique.** The assertion is existence of gross receivables at moderate
assessed risk, with no control reliance available because W-1, W-2, W-5 and W-7 are unremediated. The population of
14,540 accounts and $38,600 is too large to examine and too dispersed for an analytic to be precise at a $940 threshold.
If the assertion were completeness, stop: the design would be circular.

**Step 2. Reconcile the frame to the ledger.** Accounts 1200 and 1205 give $36,900 + $1,700 = $38,600, no difference
(Exhibit 15-4). Because W-11 makes the Snowflake datamart unreliable, agree the extract's total and row count to the
NetSuite AR detail report, not to another Snowflake object.

```sql
select  customer_id, customer_name, currency, doc_amount_usd,
        invoice_date, due_date, days_past_due, invoice_number, gl_account
from    finance.ar.aging_snapshot
where   snapshot_date = date '2025-12-31'
  and   gl_account in ('1200','1205')
order by customer_id, invoice_number;
```

**Step 3. Test the completeness and accuracy of the IPE.** Re-add the aging buckets to $38,600 and agree each to §3.3.
Re-perform the aging on 25 invoices; two Halcyon Freight invoices were aged from the invoice *entry* date, a one-bucket
difference on $34 with no effect on the frame. Confirm no null customer identifiers and that the 3,140 enterprise
customer count agrees to §1.4. An unreconciled frame stops the procedure here.

**Step 4. Remove subpopulations addressed by other procedures.** Remove the self-serve $1,700 (100% settlement-tested,
Chapter 7 §7.10) and the 31 credit balances of $310 (tested as liabilities), recording both as scope decisions. Frame:
$36,900.

**Step 5. Set tolerable misstatement and the risk of incorrect acceptance before selecting.** Tolerable misstatement is
$940, performance materiality per Chapter 3 §3.11; gross receivables is not a significant-risk population, so $705 does
not apply. The risk of incorrect acceptance is 5%: no control reliance is planned and Chapter 7's collection analytics
are corroborative rather than precise. Reliability factor **3.00**; expansion factor **1.6**.

**Step 6. Remove individually significant items.** Threshold 50% of performance materiality = **$470**. Twenty-two
accounts at or above it total $20,290 and are tested at 100%; misstatement in them is known, not projected. Residual
frame: $36,900 − $20,290 = **$16,610** across 644 accounts.

**Step 7. Set expected misstatement.** FY2024 projected $95 on a gross enterprise population of $29,150, a rate of
0.33%, implying $55 on $16,610. Two FY2025 conditions argue for more: the December cut-off risk from the 41% of Q4 ACV
signed December 24–31, and the two revenue accountant resignations in Q2. Brightline set **$150**, 0.9% of the frame.
The defensible range is $55 to $250 — below $55 ignores prior experience, above $250 asserts that nearly 1.5% of the
population is wrong. Zero guarantees failure on the first misstatement (§15.8).

**Step 8. Compute the sample size and interval.** Apply n = (BV × RF) ÷ (TM − (EM × EF)):

- Denominator: $940 − ($150 × 1.6) = $940 − $240 = **$700.00**
- n = ($16,610 × 3.00) ÷ $700.00 = $49,830 ÷ $700.00 = 71.19 → **72 sampling-interval hits**
- Interval J = $700.00 ÷ 3.00 = **$233.3333**, shown in the workpaper as $233.33
- Proof: $16,610 ÷ $233.3333 = 71.19, consistent with 72

**Step 9. Draw the random start and cumulate.** Sort the 644 accounts by customer identifier — never by balance — and
cumulate. A random start drawn uniformly from $0.01 to $233.33 returned **$18.40**, so hits fall at $18.40, $251.73,
$485.06 and every $233.33 thereafter; hit 72 falls at $18.40 + 71 × $233.3333 = **$16,585.06**, inside the $16,610 frame,
and a 73rd at $16,818.40 would fall outside. Retain seed, generator, and start so the selection can be re-performed.

**Step 10. Select.** The account holding each cumulative dollar hit is selected.

**Exhibit 15-12. MUS selection: rows 1–6 of the frame plus the three rows producing misstatements (in thousands). Full 72-hit list at WP 3200-27A.**

| Row | Customer | Balance | Cumulative from | Cumulative to | Hit no. | Hit position |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Alderwood Clinics | 312.0 | 0.01 | 312.00 | 1, 2 | 18.40; 251.73 |
| 2 | Bramble & Co. | 188.5 | 312.01 | 500.50 | 3 | 485.06 |
| 3 | Caldwell Aviation | 142.0 | 500.51 | 642.50 | — | — |
| 4 | Dunmore Textiles | 265.0 | 642.51 | 907.50 | 4 | 718.39 |
| 5 | Ellerbeck Systems | 118.0 | 907.51 | 1,025.50 | 5 | 951.72 |
| 6 | Fernhill Media | 96.5 | 1,025.51 | 1,122.00 | — | — |
| 143 | Ashgrove Retail | 240.0 | 8,341.10 | 8,581.09 | 37 | 8,418.40 |
| 197 | Cormorant Bioscience | 185.0 | 10,902.40 | 11,087.39 | 48 | 10,985.07 |
| 268 | Vantage Kinetics | 155.0 | 13,470.15 | 13,625.14 | 59 | 13,551.73 |

Rows 1–6 total $1,122.0 and capture hits 1 through 5. Row 1 is hit twice because its $312.0 balance exceeds the $233.33
interval; it is examined once. Across all 72 hits, 4 accounts were hit twice, so **68 distinct accounts** totalling
**$9,975** were examined. Dollar coverage of the enterprise population: ($20,290 + $9,975) ÷ $36,900 = **82.0%**.

**Step 11. Execute the procedure.** For each of the 68 accounts, agree the balance to the Zuora invoice, the invoice to
the executed order form and the provisioning record for the service start date, and trace subsequent cash settlement to
the *specific* invoices in the December 31 balance. The audited value is what the evidence supports at December 31, not
what was collected — a short payment is the customer stating in cash which part of the balance it rejects.

**Step 12. Compute taints.** Three accounts were misstated, all below the interval, all for one cause: revenue and a
receivable recorded in December for a performance obligation satisfied in January.

**Exhibit 15-13. Taint schedule (in thousands, except taints).**

| Ref | Account | Book value | Audited value | Misstatement | Taint | Projected misstatement |
| --- | --- | --- | --- | --- | --- | --- |
| D-1 | Ashgrove Retail | 240.0 | 232.5 | 7.5 | 7.5 ÷ 240.0 = 3.1250% | 0.031250 × 233.3333 = 7.2917 |
| D-2 | Cormorant Bioscience | 185.0 | 173.0 | 12.0 | 12.0 ÷ 185.0 = 6.4865% | 0.064865 × 233.3333 = 15.1351 |
| D-3 | Vantage Kinetics | 155.0 | 150.5 | 4.5 | 4.5 ÷ 155.0 = 2.9032% | 0.029032 × 233.3333 = 6.7742 |
| | **Total** | **580.0** | **556.0** | **24.0** | | **29.2010** |

**Step 13. Project.** Projected misstatement in the sampled residual is **$29.20**. Had any misstated item reached
$233.33 its misstatement would have entered at face value. Separately, the 100%-tested stratum produced one known
misstatement: Calderon Foods, $60.0 (Chapter 7 exception X-1 — an invoice dated December 30, 2025 for services whose
acceptance certificate was signed January 9, 2026). Known misstatement is never projected.

**Step 14. Compute the allowance for sampling risk and the upper misstatement limit.**

**Exhibit 15-14. Upper misstatement limit, residual receivable frame (in thousands).**

| Component | Computation | Amount |
| --- | --- | --- |
| Projected misstatement | Exhibit 15-13 | 29.2010 |
| Basic precision | RF(0) × J = 3.00 × 233.3333 | 700.0000 |
| Incremental allowance, 1st (largest projection, D-2) | (1.75 − 1) × 15.1351 | 11.3513 |
| Incremental allowance, 2nd (D-1) | (1.55 − 1) × 7.2917 | 4.0104 |
| Incremental allowance, 3rd (D-3) | (1.46 − 1) × 6.7742 | 3.1161 |
| **Upper misstatement limit** | 29.2010 + 700.0000 + 18.4778 | **747.68** |
| Allowance for sampling risk | 747.68 − 29.20 | 718.48 |

**Step 15. Conclude, and say what would have changed the conclusion.** The upper misstatement limit of $747.68 is below
tolerable misstatement of $940, so the sample supports the conclusion that the residual frame is not overstated by more
than $940 at a 5% risk of incorrect acceptance. Adding the known $60.0 in the 100%-tested stratum, the upper bound on
overstatement of the $36,900 enterprise population is **$807.68**, leaving $132.32 of headroom; most likely misstatement
is $60.00 + $29.20 = **$89.20**.

That headroom is thin and the file should say so. A fourth misstatement would enter the incremental allowance at a factor
of 1.40, so it could project no more than $132.32 ÷ 1.40 = $94.5 before the limit was breached — a taint of
$94.5 ÷ $233.33 = 40.5%, meaning one account 40% overstated would have failed the test. Had the limit exceeded $940 the
responses, in order, would be: ask management to correct the identified misstatements and recompute (which removes
$29.20 of projection and $18.48 of allowance, dropping the limit to $700.00); extend by selecting further hits from the
untested remainder at the same interval; or, if the cut-off cause is systematic, query all 4,102 December invoices for
service start dates after December 31.

**Exhibit 15-15. The same population, two evaluations (in thousands).**

| Measure | Chapter 7 non-statistical sample | This MUS design |
| --- | --- | --- |
| Items examined | 50 accounts, $23,590 | 90 accounts, $30,265 |
| Coverage of enterprise AR | 63.9% | 82.0% |
| Most likely misstatement | 184.9, recorded as U-1 | 89.2 |
| Quantified upper limit | none | 807.68 |

The two projections differ by $95.7 on one population: Chapter 7 sampled only $240 of the $3,290 stratum 3 and found $1.9
there, which a ratio of 13.71 multiplied into $26.0, while the MUS design selected 14 of that stratum's accounts weighted
by size and found nothing. A point estimate of projected misstatement carries imprecision of the same order as the
estimate itself — what basic precision makes explicit. U-1 remains at $(185): where two defensible projections differ, the
file carries the more conservative.

## Extended Case Study: One Deviation in Twenty-Five, and the Word "Isolated"

### Background

Control **RC-3** is a manual application control in AtlasFlow's order-to-cash cycle. On each order activated in
Salesforce CPQ, a Deal Desk analyst verifies that the order form bears a customer signature dated on or before the
contractual service start date, that the discount is within the CPQ approval matrix, and that the billing schedule agrees
to the order form, recording the verification in the approval history. RC-3 is the principal preventive control over the
occurrence and cut-off of subscription revenue, a significant risk with tolerable misstatement of $705. Brightline tested
it at the October 31, 2025 interim date over 3,940 activated orders.

### The Facts

The methodology specified a sample of 25 for a manual control operating many times per day at moderate planned reliance
— statistically, a 9% tolerable deviation rate, a 10% risk of overreliance, and zero expected deviations. The staff
member selected 25 orders randomly and found one deviation: order form OF-2025-3318, Halcyon Freight Systems, annual
contract value $118, activated July 3, 2025, with no Deal Desk entry in the approval history and a customer signature
dated July 8, 2025 — five days after activation. On inquiry, the Deal Desk manager explained that the assigned analyst
was on leave from July 1 to July 18 and no backup had been designated. The workpaper recorded: "Deviation attributable
to a one-time vacation coverage gap. Isolated instance; control otherwise operating effectively. Sample rate
1/25 = 4.0%, below the 9% tolerable rate. Conclusion: rely on RC-3."

### What the Engagement Team Did

The team relied on RC-3, assessed control risk for occurrence and cut-off of subscription revenue below maximum, designed
its substantive revenue test of details at a 10% risk of incorrect acceptance, and rolled RC-3 forward over November and
December by inquiry plus inspection of five orders, all clean.

### Analysis

**Exhibit 15-16. Correct evaluation of the RC-3 attribute sample.**

| Item | Value |
| --- | --- |
| Sample size | 25 (firm table, many-times-per-day manual control, moderate reliance) |
| TDR / risk of overreliance / expected deviations | 9% / 10% / 0 |
| Deviations found | 1 (OF-2025-3318) |
| Sample deviation rate | 1 ÷ 25 = 4.0% — not the basis for any conclusion |
| CUDL, Poisson | 3.89 ÷ 25 = **15.6%** |
| CUDL, exact binomial | **14.7%**, since P(X ≤ 1 \| n = 25, p = 0.147) = 0.0996 |
| Comparison | 14.7% > 9% — **does not support reliance** |
| n needed to support 9% with 1 deviation | 3.89 ÷ 0.09 = 43.2 → 44 (Poisson); 42 (binomial), against a design of 25 |

**First, 4.0% is the wrong comparison.** The sample rate is a point estimate; the risk of overreliance is expressed as a
bound, and the bound given one deviation in 25 is 14.7%. A population rate of 12% would produce one or fewer deviations in
25 about 19% of the time, so the sample is consistent with a control failing three times as often as tolerable. A sample
of 25 designed for zero deviations fails on the first one — not a defect in the design, but what the design means.

**Second, "isolated" was asserted, not tested.** AU-C 530 permits the anomaly treatment only on a high degree of
certainty that the item is unrepresentative, and AS 2315, which governs this engagement, has no anomaly concept at all.
More important, the explanation points the other way: an unstaffed control for an 18-day window is a *condition*, and it
applied to every order activated in that window. A cause operating across a defined subpopulation makes further
deviations more likely, not less. The team had a testable proposition and did not test it.

**Third, the deviation was never evaluated as a deficiency.** Under AS 2201 a deviation is evidence the control did not
operate as designed, and the absence of a designated backup for a daily control is a design matter independent of the
sampling conclusion, belonging in Chapter 14's severity framework. **Fourth, the roll-forward compounded the error:**
inquiry plus five items is not a roll-forward of a control whose interim test failed; there is nothing to roll forward.

### Resolution and Conclusion

1. **Recomputed the limit.** CUDL 14.7% against a 9% tolerable rate. Reliance withdrawn.
2. **Sized the exposed subpopulation.** The presence of a Deal Desk entry is machine-testable, so the team queried all
   3,940 interim orders rather than extending the sample. Forty-seven had no approval-history entry, 1.19% of the
   population. Of those, **31 fell in the July 1–18 window**, in which 214 orders were activated — a rate of
   31 ÷ 214 = **14.5%** — while the other 16 were spread across the remaining 3,726 orders, a rate of **0.43%**.
   "Isolated" was false.
3. **Tested all 47 at 100%.** Three had a service start date preceding the customer signature date, causing **$46** of
   FY2025 revenue recognised before an enforceable contract existed — below the $72 clearly trivial threshold, so not
   accumulated, but recorded in the memo because a quantitatively trivial misstatement can still be qualitatively
   significant. The other 44 were correctly priced and scheduled.
4. **Repriced the substantive plan.** With no reliance on RC-3, the risk of incorrect acceptance for the Core
   subscription revenue test of details moves from 10% (factor 2.31) to 5% (3.00). At tolerable misstatement of $705 the
   interval falls from $705 ÷ 2.31 = $305.19 to $705 ÷ 3.00 = $235.00, and the sample size rises from
   $104,900 ÷ $305.19 = 343.7 → 344 selections to $104,900 ÷ $235.00 = 446.4 → **447**: the failed control test costs
   **103 additional selections**.

The deficiency was graded a significant deficiency rather than a material weakness. The 214 orders in the window carried
$2,140 of annual contract value, which if every one were unauthorised and reversed would remove roughly
$2,140 × 5.5 ÷ 12 = **$981** of FY2025 revenue — material against overall materiality of $1,450 — but 100% testing of the
47 exceptions found only $46, so the likelihood of a material misstatement is low. Chapter 14 performs the aggregation
with W-1 through W-14 that determines the ICFR opinion.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                          WP 2450-11
AtlasFlow, Inc. — Integrated audit, year ended December 31, 2025

CONTROL RC-3 — DEAL DESK VERIFICATION OF ACTIVATED ORDERS
EVALUATION OF DEVIATION AND SUPERSEDING CONCLUSION

Prepared by:  C. Nwosu (CN)  11/24/2025
Reviewed by:  O. Haddad (OH) 11/26/2025    G. Lindqvist (GL) 12/01/2025
Supersedes:   WP 2450-10 dated 11/07/2025 (conclusion withdrawn)

PURPOSE. Evaluate the single deviation in the interim test of RC-3, determine whether the
sample result supports the planned reliance, and conclude on operating effectiveness for
January 1 to October 31, 2025.

SOURCE OF INFORMATION. Salesforce CPQ order and approval-history extract, activations
01/01/2025 to 10/31/2025, 3,940 records, total agreed to the Zuora subscription-creation
log (WP 2450-04, tick (a)); executed order forms; Deal Desk leave calendar for July 2025.

DESIGN INPUTS RECORDED BEFORE SELECTION (WP 2450-10)
  Population 3,940 activated orders     Sampling unit  one activated order
  Tolerable deviation rate  9%          Risk of overreliance  10%
  Expected deviation rate   0%          Sample size  25 (firm table)
  Selection  unrestricted random, seed 20251031, list at WP 2450-10A

RESULTS
  Deviations found  1 -- OF-2025-3318, Halcyon Freight Systems, ACV $118: no Deal Desk
                    entry in the approval history; signature 07/08/2025, activation
                    07/03/2025.
  Sample deviation rate             4.0%   -- not the basis for the conclusion
  Computed upper deviation limit   14.7%   (exact binomial, 1 deviation in 25 at 10% risk
                                          of overreliance); 15.6% on Poisson  (b)
  Comparison                       14.7% > 9% tolerable deviation rate

EXTENDED PROCEDURES
  Full-population query of the approval-history attribute, all 3,940 orders:
      No Deal Desk approval-history entry               47      (1.19%)
        activated 07/01/2025 - 07/18/2025               31  of    214   (14.49%)
        activated outside that window                   16  of  3,726    (0.43%)
  Re-performance of RC-3 on all 47 exceptions:
      Service start date preceding signature date        3   ($46 of FY2025 revenue; below
                                                             the $72 clearly trivial
                                                             threshold)
      Discount outside the CPQ approval matrix           0
      Billing schedule disagreeing with the order form   0

CONCLUSION. The sample result does not support the planned reliance on RC-3. The deviation
is not an anomaly: the identified cause (no designated backup for the Deal Desk analyst
from 07/01 to 07/18/2025) applied to 214 orders, of which 31 (14.49%) exhibited the same
deviation, against 0.43% outside the window. Reliance on RC-3 is withdrawn, and RC-3 did
not operate effectively for orders activated 07/01 - 07/18/2025. The 47 exceptions were
tested at 100%; the $46 misstatement is below the clearly trivial threshold and is not
accumulated, but the control failure is carried to WP 5100-03 for severity evaluation. The
Core subscription revenue test of details is redesigned at a 5% risk of incorrect
acceptance (factor 3.00, interval $235.00, 447 selections) rather than 10% (2.31, $305.19,
344); see WP 4100-12.

Tick marks: (a) record count and creation-date range agreed; no unmatched records.
            (b) 0.10^(1/25) = 0.9120, so the zero-deviation limit is 8.80%; the one-
                deviation limit of 14.7% satisfies P(X <= 1 | n=25, p=0.147) = 0.0996.
```

### Lessons

1. Write the tolerable deviation rate and the risk of overreliance into the workpaper before selecting, so the comparison
   at the end is arithmetic rather than negotiation.
2. The sample deviation rate is never the basis for a conclusion. Compute the upper limit.
3. A cause is not an anomaly. If you can name the condition that produced a deviation, you can size the population that
   condition touched — so size it, and where the attribute is machine-testable query the whole population.
4. A deviation is a deficiency under AS 2201 whether or not the sampling conclusion can be rescued, and the price of the
   failed test — 103 extra selections — belongs in the memo.

## Common Mistakes

### Mistake 15.1 — Sampling from a frame never reconciled to the ledger

**What it looks like.** A selection made from a client spreadsheet with no total, no row count, and no agreement to
accounts 1200 and 1205.
**Why it happens.** The extract arrives formatted and looks authoritative.
**What goes wrong.** Every conclusion is capped by the frame; a frame missing 400 rows yields negligible sampling risk
and no evidence about the missing dollars.
**How to avoid it.** Make Exhibit 15-4 the first page — ledger total, frame total, nil difference, row count — before a
single item is selected.

### Mistake 15.2 — Taking tolerable misstatement from overall materiality, or setting it after selection

**What it looks like.** A tolerable misstatement field reading $1,450, or one changed from $940 to $1,450 after a
misstatement was found.
**Why it happens.** Overall materiality is the number everyone remembers, and a failed test creates pressure.
**What goes wrong.** On the walkthrough's frame, $1,450 rather than $940 cuts the sample from 72 hits to 42 and raises
basic precision from $700 to $1,210, so a population that fails at $940 appears to pass.
**How to avoid it.** Take it from the Chapter 3 schedule, record it with its derivation before selecting, and lock it.

### Mistake 15.3 — Block selection presented as haphazard selection

**What it looks like.** Fifty-four accounts, all with December invoice dates, described as "selected haphazardly."
**Why it happens.** Contiguous rows are easy to pull and the result looks superficially random.
**What goes wrong.** Items outside the block have a zero probability of selection, and a December block is dominated by the
41% of Q4 ACV signed in the final five business days.
**How to avoid it.** Use a seeded random draw; test the December population as a risk-based selection and project nothing.

### Mistake 15.4 — Replacing an inconvenient selection

**What it looks like.** "Item 31 was a voided invoice, so item 32 was substituted."
**Why it happens.** Replacement keeps the sample size intact and the schedule clean.
**What goes wrong.** Why an item is inconvenient usually correlates with why it is misstated, so replacement biases the
sample toward items with tidy support.
**How to avoid it.** Decide the treatment of voids, credits, and nil balances when you define the frame; if a selected item
belongs to the population, use alternative procedures or treat the residue as a misstatement.

### Mistake 15.5 — Calling a deviation isolated without sizing the exposed subpopulation

**What it looks like.** "One deviation caused by a vacation coverage gap; isolated; control effective."
**Why it happens.** A plausible cause feels like an explanation that closes the matter.
**What goes wrong.** A cause operating over a period makes deviations in that period more likely, not less: the
"isolated" instance was one of 31 in a 214-order window with a 14.5% deviation rate.
**How to avoid it.** Treat every cause as a hypothesis about a subpopulation — name the window, count the items, test
them 100% where the attribute is machine-testable.

### Mistake 15.6 — Reporting known misstatement and never projecting

**What it looks like.** "Misstatements identified: $85.9. Below tolerable misstatement of $940. No adjustment."
**Why it happens.** The found amount is concrete; the projection requires choosing an estimator.
**What goes wrong.** AS 2810 and AU-C 450 require the projected amount. The $85.9 found in a sample covering 63.9% of the
population projected to $184.9, understating the summary of audit differences by $99.
**How to avoid it.** Make projection a required field; carry 100%-tested strata at known amounts and project the rest.

### Mistake 15.7 — Concluding on projected misstatement without the allowance for sampling risk

**What it looks like.** "Projected misstatement $29.2 versus tolerable misstatement $940 — ample margin."
**Why it happens.** Basic precision has no intuitive counterpart, so it gets dropped.
**What goes wrong.** The relevant comparison is $747.68 against $940: the margin is $192, not $911, so headroom is
misjudged by a factor of five.
**How to avoid it.** Compute all four components of Exhibit 15-14 every time, and non-statistically treat projected
misstatement above a third of tolerable misstatement as a signal to quantify or extend.

### Mistake 15.8 — Using MUS where the risk is understatement, omission, or a nil balance

**What it looks like.** A monetary-unit sample of the deferred revenue subledger to test completeness.
**Why it happens.** MUS is the firm's default template and it is easy to run.
**What goes wrong.** MUS cannot select an item recorded at zero or not recorded at all, and a balance recorded at $10 and
audited at $180 has a taint of 1,700%, which the formulas assume cannot happen.
**How to avoid it.** Match the technique to the direction of the risk: for completeness, sample outside the accounting
records and consider difference estimation.

### Mistake 15.9 — Leaving individually significant items in the frame, and confusing hits with items

**What it looks like.** MUS run over the full $36,900 at a $233.33 interval, reporting "72 items tested, coverage
72 ÷ 644 = 11%."
**Why it happens.** MUS selects large items automatically, so removing them first looks redundant.
**What goes wrong.** Leaving the 22 large balances in inflates n from 72 hits to $36,900 ÷ $233.33 = 158.1, so 159, for no
gain in precision. And a hit is not an item: 72 hits fell on 68 accounts, and coverage is measured in dollars ($30,265 of
$36,900, 82.0%).
**How to avoid it.** Stratify explicitly, then report hits, distinct items, and dollar coverage as three figures.

### Mistake 15.10 — Treating a full-population query as though it eliminated the sample

**What it looks like.** "We tested 100% of the population," over a query evaluating one machine-readable attribute,
followed by examination of 10 of the 47 exceptions it returned.
**Why it happens.** "100%" is persuasive and exception populations are unbudgeted.
**What goes wrong.** Whether cash cleared is machine-testable; whether an approval was appropriate is not. And examining
10 of 47 exceptions is a sample with no design, no tolerable rate, and no projection.
**How to avoid it.** State which attribute the query tested and which it did not, establish the extract's completeness,
and examine every exception or design a documented sample of them.

## Practice Exercises

### Exercise 15-1 [Foundational]

Using Exhibit 15-10, compute the computed upper deviation limit for each and state whether it supports a 10% tolerable
deviation rate: (a) n = 25, 0 deviations, 10% risk of overreliance; (b) n = 25, 1 deviation, 10%; (c) n = 40, 1
deviation, 10%; (d) n = 60, 2 deviations, 5%.

### Exercise 15-2 [Foundational]

State whether each is an audit sampling application, with a one-sentence reason: (a) confirming all 22 enterprise
balances at or above $470; (b) inspecting 25 of 3,940 order forms for approval evidence; (c) recomputing remaining
performance obligations from the full subscription population; (d) inquiring about the close calendar; (e) re-performing
RC-3 on all 47 orders with no approval-history entry.

### Exercise 15-3 [Foundational]

Control RC-12 operates daily. Using n = RF(k) ÷ TDR, compute the required sample size for (a) a 10% tolerable deviation
rate, 10% risk of overreliance, zero expected deviations; (b) the same but a 2% expected deviation rate allowing 1
deviation, verifying n × EDR ≤ 1; (c) a 10% tolerable rate at a 5% risk of overreliance, zero expected.

### Exercise 15-4 [Intermediate]

Professional services revenue is $12,400 with tolerable misstatement of $940 and expected misstatement of $60. Compute
the MUS sample size and interval at (a) a 5% risk of incorrect acceptance and (b) 10%.

### Exercise 15-5 [Intermediate]

Using the interval from Exercise 15-4(a), compute projected misstatement from: item A, book value $180.0, audited
$171.0; item B, book value $96.0, audited $84.0; item C, book value $420.0, audited $399.0. Show each taint and state
which item is not extrapolated and why.

### Exercise 15-6 [Intermediate]

Continue Exercise 15-5. Compute basic precision, the incremental allowance, and the upper misstatement limit at a 5% risk
of incorrect acceptance; conclude against tolerable misstatement of $940; and state the limit if management corrects all
three misstatements.

### Exercise 15-7 [Intermediate]

Find and correct every error in this extract for the $16,610 residual receivable frame.

```text
Population (residual AR)                                 16,610
Tolerable misstatement                                    1,450
Reliability factor (5% risk of incorrect acceptance)       3.00
Sample size = 16,610 x 3.00 / 1,450 = 34.4                   35
Sampling interval = 1,450 / 3.00                         483.33
Misstatement found: Tarnwick Group, book value 600.0, audited 582.0
  Taint = 18.0 / 600.0 = 3.00%
  Projected misstatement = 3.00% x 483.33 =               14.50
Upper misstatement limit                                  14.50
Conclusion: 14.50 is below tolerable misstatement of 1,450. Accept.
```

### Exercise 15-8 [Intermediate]

A population of 480 professional services invoices totals $9,600. A random sample of 80 has a book value of $1,760 and
an audited value of $1,724; the standard deviation of the 80 per-unit differences is $2.10. Tolerable misstatement is
$705, the risk of incorrect acceptance 5% (Z = 1.645). Compute (a) projected misstatement under difference estimation,
(b) under ratio estimation, (c) the allowance for sampling risk and upper limit under difference estimation, and (d)
which estimator you would use and why.

### Exercise 15-9 [Advanced]

Control RC-31 (the Revenue Manager clears the Zuora-to-RevPro reconciliation exceptions from interface I-2) was tested
with n = 40 at a 9% tolerable deviation rate, a 10% risk of overreliance, and zero expected deviations. One deviation was
found. The cause was a six-hour Zuora outage on March 4, 2025 during which the reconciliation report did not generate;
Jira incident INC-1188 and the vendor status page corroborate the window; 19 records fell in it and all 19 were
re-performed with no exception. Conclude on reliance, draft the workpaper conclusion paragraph, and give one credible
alternative conclusion.

### Exercise 15-10 [Advanced]

Draft the design-and-evaluation paragraph (150–200 words) for WP 3200-27 documenting the walkthrough's monetary-unit
sample at the level AS 1215 requires, using the actual figures.

### Exercise 15-11 [Advanced]

Assume Chapter 3's performance materiality had been $780 rather than $940, with the same 75% convention for
significant-risk populations. Compute (a) revised tolerable misstatement for Core subscription revenue and for gross
receivables; (b) the revised MUS sample size for Core subscription revenue of $104,900 at a 5% risk of incorrect
acceptance with zero expected misstatement; (c) the revised size for the $16,610 residual frame on the same basis;
(d) the effect on the RC-3 attribute sample size of 25.

### Exercise 15-12 [Advanced]

The self-serve receivable population is $1,700 across 11,400 accounts, tested by matching the full Stripe settlement file
rather than by sampling. State the three conditions that must hold for a full-population test to replace a sample, and
compute the residue and required follow-up if (a) 96.4% of the $1,700 settled by February 13, 2026 and (b) only 88.0%
did. Write a two-sentence conclusion for each, using the $72 clearly trivial threshold.

## Solutions to Practice Exercises

### Solution 15-1

CUDL = RF ÷ n. (a) 2.31 ÷ 25 = **9.24%**, supports 10%. (b) 3.89 ÷ 25 = **15.56%**, does not. (c) 3.89 ÷ 40 = **9.73%**,
supports. (d) 6.30 ÷ 60 = **10.50%**, does not. From (a) to (b) the sample rate moved 0% to 4% but the limit moved 9.24%
to 15.56%; from (b) to (c) the same single deviation is tolerable at n = 40 and not at n = 25. Extent buys tolerance.

### Solution 15-2

(a) **Not sampling** — all items in the stratum are examined. (b) **Sampling** — fewer than 100% of a defined population,
selected to conclude on all 3,940. (c) **Not sampling** — full-population recomputation, provided the extract's
completeness and accuracy are established. (d) **Not sampling** — inquiry; no population, no projection. (e) **Not
sampling** — 100% of an identified subpopulation, though the completeness of the query that identified the 47 must itself
be established or the "100%" claim collapses.

### Solution 15-3

(a) n = 2.31 ÷ 0.10 = 23.1 → **24**. (b) n = 3.89 ÷ 0.10 = 38.9 → **39**; check 39 × 0.02 = 0.78 ≤ 1, so 39 suffices.
(c) n = 3.00 ÷ 0.10 = **30**. Allowing one expected deviation costs 15 items, a 63% increase — why an expected rate
approaching the tolerable rate is a signal not to plan on reliance.

### Solution 15-4

(a) Denominator = $940 − ($60 × 1.6) = **$844.00**; n = ($12,400 × 3.00) ÷ $844.00 = $37,200 ÷ $844 = 44.08 → **45**;
interval = $844.00 ÷ 3.00 = **$281.33**. Proof: $12,400 ÷ $281.33 = 44.08.
(b) Denominator = $940 − ($60 × 1.5) = **$850.00**; n = ($12,400 × 2.31) ÷ $850.00 = $28,644 ÷ $850 = 33.70 → **34**;
interval = $850.00 ÷ 2.31 = **$367.97**. Moving from 5% to 10% saves 11 selections and requires a tested, effective
control, which FY2025 AtlasFlow generally does not have.

### Solution 15-5

- Item A: misstatement $9.0; taint 9.0 ÷ 180.0 = 5.0000%; projected 0.05 × $281.33 = **$14.07**
- Item B: misstatement $12.0; taint 12.0 ÷ 96.0 = 12.5000%; projected 0.125 × $281.33 = **$35.17**
- Item C: book value $420.0 is at or above the $281.33 interval, so it was certain to be selected and represents only
  itself; no taint is computed and the misstatement enters at face value, **$21.00**
- Total projected misstatement = 14.07 + 35.17 + 21.00 = **$70.24**

### Solution 15-6

Basic precision = 3.00 × $281.33 = **$844.00**, equal to TM − EM × EF by construction. Incremental allowance,
extrapolated items only, ranked descending: item B, (1.75 − 1) × 35.17 = $26.38; item A, (1.55 − 1) × 14.07 = $7.74;
total **$34.12**. Item C receives none. UML = 70.24 + 844.00 + 34.12 = **$948.36**, exceeding $940 by $8.36, so the
sample does **not** support the conclusion — which is why the four components must be computed rather than eyeballed. If
management corrects all three misstatements, projection and incremental allowance fall to nil and the limit is basic
precision alone, **$844.00**. Accept.

### Solution 15-7

Four errors. **(1) Tolerable misstatement is overall materiality.** Gross receivables carries $940, so n =
($16,610 × 3.00) ÷ $940 = 53.01 → **54** and the interval is $940 ÷ 3.00 = **$313.33**. **(2) Individually significant
items were never removed.** At a $470 threshold the $600 Tarnwick balance belongs in the 100%-tested stratum. **(3) A
taint was applied to an item exceeding the interval.** $600.0 exceeds even the incorrect $483.33, so the misstatement
enters at face value, $18.0, not $14.50. **(4) No basic precision and no incremental allowance.** The upper misstatement
limit is not the projection.

Corrected: Tarnwick's $18.0 is a known misstatement in the 100%-tested stratum. If the sample of 54 finds nothing, the
limit on the residual is basic precision alone, 3.00 × $313.33 = **$940.00** — exactly tolerable misstatement, because
expected misstatement was set to zero. Setting it to $150 as in the walkthrough costs 18 selections and buys $240 of
room.

### Solution 15-8

(a) Mean difference = ($1,760 − $1,724) ÷ 80 = $0.45; projected = 480 × $0.45 = **$216.00**.
(b) Ratio = $1,724 ÷ $1,760 = 0.9795455; × $9,600 = $9,403.64; projected = $9,600 − $9,403.64 = **$196.36**.
(c) s_d ÷ √n = $2.10 ÷ 8.9443 = 0.234787; correction = √(1 − 80 ÷ 480) = √0.833333 = 0.912871; allowance =
1.645 × 480 × 0.234787 × 0.912871 = 789.60 × 0.234787 = 185.39; × 0.912871 = **$169.20**. Upper limit = $216.00 +
$169.20 = **$385.20**, below $705. Accept.
(d) The projections differ because the sample's mean book value ($22.00) exceeds the population's ($20.00), so ratio
estimation scales down. AtlasFlow's cut-off errors are whole invoices or invoice lines in the wrong period and therefore
proportional to size, so **ratio** is appropriate, consistent with Chapter 7, §7.5. A fixed-amount error pattern would
make difference estimation the better choice.

### Solution 15-9

**The sample does not support reliance, but reliance is supportable for the population excluding the outage window.**
CUDL = 3.89 ÷ 40 = 9.73% exceeds the 9% tolerable rate. What rescues the population conclusion is not the anomaly
argument (AU-C 530's high-certainty condition, and AS 2315 has no anomaly concept) but that the exposed subpopulation is
identifiable, independently corroborated, bounded at 19 items, and tested at 100%.

```text
The interim test of RC-31 (n = 40, tolerable deviation rate 9%, risk of overreliance 10%,
zero expected deviations) identified one deviation. The computed upper deviation limit of
9.73% (3.89 / 40) exceeds the tolerable rate, so the sample result alone does not support
reliance. The cause is established by independent evidence: a six-hour Zuora outage on
March 4, 2025 (Jira INC-1188; vendor status page) during which the reconciliation report
did not generate. The exposed subpopulation is bounded at 19 records, all re-performed with
no exception. We conclude that RC-31 operated effectively for FY2025 other than during the
March 4 window, and that the 19 records in that window are supported by 100%
re-performance. The absence of a documented procedure for regenerating the report after an
outage is carried to WP 5100-03 as a deficiency.
```

**Credible alternative.** Extend to 44 items (3.89 ÷ 0.09 = 43.2) drawn randomly from the untested remainder: with no
further deviation, CUDL = 3.89 ÷ 44 = 8.84% ≤ 9% and reliance is supported statistically — weaker here only because it
treats a bounded, externally corroborated cause as random.

### Solution 15-10

```text
Objective. Evidence over the existence of gross enterprise accounts receivable of $36,900
at December 31, 2025 (account 1200), a moderate risk of material misstatement with no
control reliance available (W-1, W-2, W-5, W-7).

Design. Tolerable misstatement $940, being performance materiality per WP 1200-03; this is
not a significant-risk population. Risk of incorrect acceptance 5% (no control reliance;
the collection analytic at WP 3200-09 is corroborative only), reliability factor 3.00,
expansion factor 1.6. Expected misstatement $150, from the FY2024 projection of $95 on
$29,150 (0.33%) increased for the December cut-off risk. Individually significant items are
the 22 balances at or above $470 (50% of performance materiality), $20,290, tested at 100%.
Monetary-unit sample of the $16,610 residual: n = (16,610 x 3.00) / (940 - 150 x 1.6) =
71.19, so 72 interval hits; interval $233.3333; random start $18.40 (seed 20251231A);
selection at WP 3200-27A. The 72 hits fell on 68 accounts of $9,975; coverage 82.0%.

Evaluation. Three misstatements, all below the interval, all December cut-off: taints
3.1250%, 6.4865%, 2.9032%; projected misstatement $29.20; basic precision $700.00;
incremental allowance $18.48; upper misstatement limit $747.68 against $940. One known
misstatement of $60.0 in the 100%-tested stratum. Conclusion: not overstated by more than
$940 at a 5% risk of incorrect acceptance. All four share one cause and are carried at $185
as U-1 (WP 5200-01).
```

### Solution 15-11

(a) Core subscription revenue 75% × $780 = **$585**; gross receivables **$780**. (b) Interval = $585 ÷ 3.00 =
**$195.00**; n = $104,900 ÷ $195.00 = 537.9 → **538**, against 447 at $705 — 91 more selections, a 20.4% increase.
(c) Interval = $780 ÷ 3.00 = **$260.00**; n = $16,610 ÷ $260.00 = 63.88 → **64**, against 54 at $940. (d) **No effect.**
An attribute sample size depends only on rates — the tolerable deviation rate, the expected deviation rate, and the risk
of overreliance. A materiality revision changes every test of details and no test of controls, a useful diagnostic: a
file in which it changed a control sample size has confused the two frameworks.

### Solution 15-12

Three conditions: the extract must be complete, accurate, and reconciled to the ledger (W-11 means agreeing a Snowflake
extract to NetSuite); the attribute must be fully machine-evaluable (cash clearing is, appropriateness of an approval is
not); and every exception returned must be examined, not sampled without a design.

(a) Residue = $1,700 × (1 − 0.964) = **$61.2**. "One hundred per cent of the $1,700 self-serve population was matched to
the Stripe settlement file through February 13, 2026, settling $1,638.8, or 96.4%. The unsettled residue of $61.2 is below
the $72 clearly trivial threshold and no further procedures are required."
(b) Residue = $1,700 × 0.12 = **$204.0**. "Settlement covered $1,496.0, or 88.0%, leaving an unsettled residue of $204.0
that exceeds the $72 clearly trivial threshold. The residue is stratified, accounts above $10 are examined against the
subscription record and provisioning log, and the remainder is treated as a misstatement unless supported." In (b) the
match has not replaced sampling; it has reduced the population to be sampled from $1,700 to $204.

## Review Questions

**RQ 15-1.** Give the two elements of the definition of audit sampling, and explain why a risk-based selection of 34
journal entries fails the second.

**RQ 15-2.** What distinguishes statistical from non-statistical sampling, and what does not differ between them?

**RQ 15-3.** Define sampling risk and non-sampling risk, and state which a larger sample reduces.

**RQ 15-4.** Name the two components of sampling risk in a test of controls and classify each as an effectiveness or an
efficiency concern.

**RQ 15-5.** Why must the sampling unit for a completeness assertion sit outside the accounting records?

**RQ 15-6.** Why is block selection unacceptable as a sampling method, and when is selecting a block nonetheless a good
idea?

**RQ 15-7.** Distinguish a control deviation from a misstatement, giving an example of each that is not also the other.

**RQ 15-8.** Why is the sample deviation rate not the basis for the conclusion in a test of controls?

**RQ 15-9.** What is basic precision, and why does it appear in the evaluation of a monetary-unit sample that found no
misstatement?

**RQ 15-10.** Why is a misstatement in an item at or above the sampling interval not extrapolated by a taint?

**RQ 15-11.** State the relationship between performance materiality and tolerable misstatement, and give the two
circumstances in which tolerable misstatement is set below performance materiality.

**RQ 15-12.** Why does mean-per-unit estimation require a far larger sample than difference estimation on the same
population?

**RQ 15-13.** Name the three population or assertion characteristics that make monetary-unit sampling the wrong
technique.

**RQ 15-14.** Distinguish known from projected misstatement, and state which must be accumulated.

**RQ 15-15.** Name five of the eleven items AS 1215 and AU-C 230 effectively require in the documentation of a sampling
application.

## Answers to Review Questions

**RQ 15-1.** Sampling applies a procedure to fewer than 100% of a population and does so in a way that gives a reasonable
basis for a conclusion about the *entire* population. Entries selected because they hit a non-standard offset account give
the other 4,878 manual entries no chance of selection, so no inference about them is available.

**RQ 15-2.** A statistical application uses random-based selection *and* measures sampling risk with probability theory.
Everything else is identical: definition and reconciliation of the population, tolerable and expected misstatement,
representativeness, investigation of every exception, and projection.

**RQ 15-3.** Sampling risk is the risk that the sample conclusion differs from the conclusion the same procedure would have
produced on the whole population; it falls with more items or with stratification. Non-sampling risk is every other source
of error — wrong population, wrong procedure, careless execution, an incomplete extract — and sample size does not reduce it.

**RQ 15-4.** Overreliance, an effectiveness concern because it produces insufficient substantive work and an ineffective
control reported as effective; and underreliance, an efficiency concern producing unnecessary work and possibly a reported
deficiency that does not exist.

**RQ 15-5.** Because the misstatement sought is an item missing from those records: sampling the deferred revenue
subledger cannot find a contract liability never recorded. The population must exist independently — order forms,
provisioning records, cash disbursements.

**RQ 15-6.** A block is effectively one observation of a cluster, clusters in accounting data differ systematically, and
items outside the block have a zero probability of selection. It is nonetheless an excellent risk-based selection —
Chapter 4 tests the December 24–31 population because it is different — provided nothing is projected from it.

**RQ 15-7.** A deviation is an instance in which a control did not operate as described; a misstatement is a difference
between a recorded amount and the amount the framework requires. A missing approval on a correctly priced, correctly
dated order form is a deviation only; a properly approved order form whose revenue was recorded early is a misstatement
only.

**RQ 15-8.** Because the sample rate is a point estimate while the risk of overreliance is expressed as a bound. One
deviation in 25 is a 4% sample rate but a 14.7% upper limit, so a control failing far more often than tolerable would
produce that result routinely.

**RQ 15-9.** Basic precision is RF(0) × the sampling interval: the allowance for misstatement the sample did not encounter.
A clean sample does not prove the population is clean; it bounds how unclean it can be. In a zero-expected-misstatement
design it equals tolerable misstatement exactly.

**RQ 15-10.** Because an item at least as large as the interval was certain to be selected. It represents only itself
rather than a slice of the population, so its misstatement is known, enters at face value, and receives no incremental
allowance.

**RQ 15-11.** Performance materiality is an entity-level amount set once to control aggregation risk across populations;
tolerable misstatement is a procedure-level amount for one population and never exceeds it. It is set lower when more
than one sampling procedure addresses the population and when the population carries a significant risk — why AtlasFlow's
revenue populations carry $705 against $940.

**RQ 15-12.** Mean-per-unit ignores book value and estimates the population from audited amounts alone, so its precision
depends on the variability of the balances, which in a portfolio spanning $1 to $2,410 is enormous. Difference estimation
uses book value as a covariate and estimates only the misstatement; the allowance falls from $5,686 to $145.

**RQ 15-13.** Completeness or omission, because MUS cannot select an item recorded at zero or not recorded at all;
understatement, because a taint can exceed 100% and the formulas assume it cannot; and populations with numerous
misstatements, because each adds an incremental allowance.

**RQ 15-14.** A known misstatement is determined for a specific item, as in a stratum tested at 100%; a projected
misstatement estimates misstatement in the untested portion of a sampled population. Both are accumulated, and AS 2810 and
AU-C 450 require the *projected* amount — why $85.9 found in the AtlasFlow sample became $185.

**RQ 15-15.** Any five from the §15.10 list, for example: the population and its reconciliation to the ledger; tolerable
misstatement and its derivation; the sample size computation showing every input; the selection method including seed,
random start, and interval; and the evaluation, including projection and the allowance for sampling risk.

## Key Definitions

**Allowance for sampling risk.** The amount by which the upper limit on misstatement or deviation exceeds the point
estimate. In monetary-unit sampling, basic precision plus the incremental allowance.

**Anomaly.** A misstatement or deviation demonstrably not representative of the population. AU-C 530 permits the treatment
only on a high degree of certainty; AS 2315 has no anomaly concept, so on an issuer audit it is effectively unavailable.

**Attribute sampling.** A sampling application estimating the rate of occurrence of a binary condition, which in a test of
controls is a control deviation.

**Basic precision.** The reliability factor for zero misstatements times the sampling interval: the allowance for
misstatement the sample did not encounter. Present in every monetary-unit evaluation, including a clean one.

**Block selection.** Selecting all items in a contiguous segment of the population — a date range, a document number range,
a ledger page. Not acceptable as a sampling method, because items outside the block have no chance of selection and the
block behaves as one observation.

**Classical variables sampling.** A family of applications estimating a population amount from the sample mean using
normal-theory confidence intervals: mean-per-unit, difference, and ratio estimation.

**Computed upper deviation limit.** The upper bound of a one-sided confidence interval on the population deviation rate at
the chosen risk of overreliance, approximated as the reliability factor for deviations found divided by n.

**Haphazard selection.** Selection without conscious bias but without a random mechanism. Permitted non-statistically;
unusable statistically because no selection probability is known, and measurably biased toward the visible, the familiar,
and the round.

**Incremental allowance.** In monetary-unit sampling, the additional allowance arising from misstatements found: the sum
over extrapolated items, ranked by projected amount descending, of (incremental reliability factor − 1) × projected
misstatement.

**Individually significant item.** An item large enough that the auditor examines it rather than sampling it, typically
25% to 100% of performance materiality. Its misstatement is known, and it contributes no sampling risk.

**Known misstatement.** A misstatement whose amount has been determined for a specific item examined. Every misstatement
in a stratum tested at 100% is known.

**Monetary-unit sampling.** An application in which each recorded dollar is a sampling unit and dollars are selected
systematically from the cumulated population, so items are selected with probability proportional to size. Also called
probability-proportional-to-size or dollar-unit sampling.

**Non-sampling risk.** The risk of an erroneous conclusion for any reason other than sampling — an inappropriate
population, a carelessly performed procedure, an unrecognised exception, an incomplete extract. Not reduced by sample
size.

**Projected misstatement.** The estimate of misstatement in the untested portion of a sampled population, by taint
extrapolation, ratio, or difference. AS 2810 and AU-C 450 require it to be accumulated, not merely the amount found.

**Reliability factor.** A Poisson-derived multiplier corresponding to a number of misstatements and a risk of incorrect
acceptance, used to compute sample size, the interval, basic precision, and the incremental allowance. 3.00 for zero
misstatements at 5%; 2.31 at 10%.

**Risk of incorrect acceptance.** The risk that a sample supports the conclusion that a balance is not materially
misstated when it is; an effectiveness concern, controlled through the reliability factor. Its counterpart, incorrect
rejection, is an efficiency concern.

**Risk of overreliance.** The risk that a sample supports reliance on a control whose true deviation rate exceeds the
tolerable rate; also called assessing control risk too low, and an effectiveness concern. Its counterpart, underreliance,
is an efficiency concern.

**Sampling interval.** In monetary-unit sampling, (tolerable misstatement − expected misstatement × expansion factor)
divided by the reliability factor for zero misstatements; equivalently, book value divided by sample size. Any item at
least this large is certain to be selected.

**Sampling risk.** The risk that the conclusion drawn from a sample differs from the conclusion that would have been drawn
had the procedure been applied to every item. Reduced only by more items or by stratifying.

**Taint.** The ratio of the misstatement in a selected item to its recorded book value, used to extrapolate the
misstatement of an item smaller than the sampling interval; multiplied by the interval it gives that item's projected
misstatement.

**Tolerable deviation rate.** The maximum rate of control deviation the auditor will accept and still place the planned
reliance on the control. A rate, not an amount, and therefore unaffected by revisions to materiality.

**Upper misstatement limit.** Projected misstatement plus basic precision plus the incremental allowance: the upper bound
on population overstatement at the chosen risk of incorrect acceptance, compared with tolerable misstatement.

## Chapter Summary

1. Sampling is one of four extents; the decision that most often goes wrong is sampling a population that should have
   been examined at 100%, addressed by an analytic, or attacked with a full-population query.
2. Statistical sampling adds random-based selection and a quantified allowance for sampling risk, nothing else; a firm
   "assurance factor" of 3.0 is the 5% reliability factor with the statistics removed.
3. Sampling risk falls with sample size and non-sampling risk does not, so a large sample from an unreconciled frame has
   traded a reducible risk for an unbounded one.
4. Overreliance and incorrect acceptance are effectiveness concerns controlled directly by the reliability factor;
   underreliance and incorrect rejection are efficiency concerns controlled by realistic expected misstatement and by
   extending rather than concluding on a failed result.
5. The conclusion in a test of controls rests on the computed upper deviation limit, never the sample deviation rate: one
   deviation in 25 is a 4% sample rate and a 14.7% upper limit, which fails a 9% tolerable rate.
6. Naming a cause begins the analysis rather than ending it — 31 deviations in 214 July orders against 0.43% elsewhere is
   what "isolated" looked like.
7. Tolerable misstatement is a procedure-level amount never exceeding performance materiality — $940 for gross
   receivables, $705 for significant-risk revenue — recorded before selection and never moved.
8. Stratification with 100% testing of individually significant items cut the receivable extent from 159 undivided
   monetary-unit hits to 22 items plus 72 hits on a $16,610 residual, with higher precision.
9. The walkthrough produced projected misstatement $29.20, basic precision $700.00, incremental allowance $18.48, and an
   upper misstatement limit of $747.68 against $940; because basic precision equals tolerable misstatement whenever
   expected misstatement is zero, $150 of expectation cost 18 selections and bought $240 of room.
10. Mean-per-unit, difference, and ratio estimation gave $819, $180, and $188 on one sample; choosing among them is a
    factual question about whether misstatements scale with item size.
11. Full-population testing displaces sampling only where the extract is complete and accurate, the attribute is fully
    machine-evaluable, and every exception is examined; otherwise it shrinks the population still to be sampled.
12. Projected misstatement, not the amount found, is accumulated — $85.9 became the $185 recorded as U-1 — every
    misstatement is also evaluated qualitatively, and the documentation test is re-performability.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Materiality and the tolerable misstatement schedule | Chapter 3, §3.11 | Source of $1,450, $940, $72, and $705 |
| Assessed risks deciding which populations carry $705 | Chapter 2 | Why Core and Insight subscription revenue are significant-risk populations |
| The receivable confirmation as a sampling application | Chapter 7, §§7.3–7.5 | The stratified sample and ratio projection that produced U-1 |
| Evaluating deviations as deficiencies | Chapter 14 | What happens to the RC-3 deviation once reliance is withdrawn |
| ITGC and application control conclusions | Chapters 11 and 12 | Why almost every FY2025 test of details is designed at 5% |
| Full-population analytics and analytic precision | Chapter 18 | When an analytic legitimately displaces a sample |
| Accumulation and final evaluation | Chapter 19 | Where U-1 is evaluated against $1,450 |

## Further Reading

- PCAOB AS 2315, *Audit Sampling*, with AS 2810, *Evaluating Audit Results*: the first for design, the second for what
  must be done with what the sample finds.
- PCAOB AS 2105, *Consideration of Materiality in Planning and Performing an Audit*, on tolerable misstatement at the
  account level, and AS 2201 on the evidence needed to conclude that a control operates effectively.
- AICPA AU-C 530, *Audit Sampling*, particularly its treatment of anomalies and its requirement to investigate cause;
  and AU-C 450, *Evaluation of Misstatements Identified During the Audit*.
- The AICPA Audit Guide covering audit sampling, the practical source of the attribute tables, reliability factors, and
  expansion factors used here. Non-authoritative.
- PCAOB AS 1215 and AICPA AU-C 230, *Audit Documentation*, for the re-performability standard applied to a sampling
  workpaper.
