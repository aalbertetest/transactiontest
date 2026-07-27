# Chapter 3 — Materiality

> Materiality is the only number in the audit file that every other number is measured against, and it is set
> before most of those other numbers exist. For AtlasFlow, Inc. the problem is acute: the company lost $21,400
> in FY2025, so the earnings benchmark auditors reach for first is unusable; its equity is $7,100, so a
> percentage of equity would produce a threshold of $71; and the number management, the board, and the sell
> side actually talk about — annual recurring revenue of $172.0 million — is not in the financial statements at
> all. This chapter derives Brightline LLP's FY2025 materiality set from first principles, shows the
> alternatives that were rejected and why, and then works a $310 misstatement that is 0.21% of revenue and
> nonetheless had to be corrected.

## Learning Objectives

- **LO 3.1** Compute overall (financial statement) materiality for a loss-making SaaS registrant from at least
  four candidate benchmarks, defend the benchmark selected, and articulate the argument against annual
  recurring revenue in terms a national office would accept.
- **LO 3.2** Derive performance materiality from overall materiality and quantify the aggregation risk that
  the haircut is designed to control.
- **LO 3.3** Compute a clearly trivial threshold and distinguish it from performance materiality and from a
  sampling threshold.
- **LO 3.4** Determine specific materiality for particular classes of transactions, balances, and disclosures,
  and identify the disclosures for which no quantitative threshold applies.
- **LO 3.5** Allocate group materiality to components, compute the resulting aggregation check, and explain
  why the sum of component materialities exceeds overall materiality.
- **LO 3.6** Distinguish tolerable misstatement from performance materiality and compute the effect of each on
  a sample size.
- **LO 3.7** Evaluate whether materiality must be revised during an engagement and document the consequences
  of revision in both directions.
- **LO 3.8** Apply qualitative materiality factors to a quantitatively immaterial misstatement and conclude on
  whether it must be corrected.
- **LO 3.9** Contrast the use of materiality in the financial statement audit with its use in the audit of
  internal control over financial reporting, including the role of interim materiality.
- **LO 3.10** Draft the materiality section of a planning memorandum that satisfies the documentation
  requirements.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2105, *Consideration of Materiality in Planning and Performing an Audit* | Establish materiality for the financial statements as a whole using a percentage of an appropriate benchmark; determine tolerable misstatement at the account and disclosure level; consider whether misstatements of lesser amounts than overall materiality could influence users' judgments about particular items; reevaluate materiality as the audit progresses. |
| PCAOB | AS 2101, *Audit Planning* | Materiality is an input to the audit strategy and the audit plan; the 2022 amendments (effective for fiscal years ending on or after December 15, 2024) also govern planning and supervision of audits involving other auditors, which is where component thresholds are communicated. |
| PCAOB | AS 1206, *Dividing Responsibility for the Audit with Another Accounting Firm* | Effective for fiscal years ending on or after December 15, 2024; relevant because Brightline UK LLP performs the UK component work under the group team's supervision rather than under divided responsibility. |
| PCAOB | AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of Financial Statements* | Directs the auditor to use the same materiality considerations as in the financial statement audit; defines a material weakness by reference to a reasonable possibility of material misstatement of the **annual or interim** financial statements, which imports a smaller threshold than annual materiality. |
| PCAOB | AS 2810, *Evaluating Audit Results* | Accumulate identified misstatements and evaluate them individually and in the aggregate, quantitatively and qualitatively, against materiality. Chapter 19 owns the evaluation; this chapter owns the threshold. |
| PCAOB | AS 1215, *Audit Documentation* | The materiality determination, the benchmark, the percentage, the reasons, and any revision are documentation requirements. |
| AICPA | AU-C 320, *Materiality in Planning and Performing an Audit* | Requires determination of (a) materiality for the financial statements as a whole, (b) materiality levels for particular classes of transactions, account balances, or disclosures where applicable, and (c) **performance materiality**; requires revision when the auditor becomes aware of information that would have changed the initial determination; requires documentation of all of these amounts and the factors considered. |
| AICPA | AU-C 450, *Evaluation of Misstatements Identified During the Audit* | Requires accumulation of misstatements "other than those that are clearly trivial" — the authoritative hook for the clearly trivial threshold. |
| AICPA | AU-C 600, *Special Considerations — Audits of Group Financial Statements* | Requires determination of component materiality and component performance materiality; expressly contemplates that the aggregate of component materialities may exceed group materiality. |
| SEC staff | Staff Accounting Bulletin No. 99, *Materiality* | Exclusive reliance on a percentage rule of thumb is not acceptable; enumerates the qualitative considerations that can make a quantitatively small misstatement material. |
| SEC staff | Staff Accounting Bulletin No. 108 | Requires consideration of the effect of prior-year uncorrected misstatements on the current period using both the rollover and iron-curtain perspectives. |
| SEC | Regulation S-K, Item 404(a) | Sets a $120 thousand threshold for related-person transaction disclosure, which is a user-expectation anchor for specific materiality. |
| SEC | Regulation G and Regulation S-K, Item 10(e) | Govern presentation of non-GAAP measures; relevant because ARR and NRR appear alongside the audited statements. |
| FASB | Concepts Statement No. 8, Chapter 3, *Qualitative Characteristics of Useful Financial Information* | Defines materiality as an entity-specific aspect of relevance: information is material if omitting or misstating it could reasonably be expected to influence the decisions users make on the basis of the financial statements. |
| FASB | ASC 606-10-50 | The revenue disclosure requirements whose individual materiality must be assessed. |

**Where the two frameworks differ substantively.** AtlasFlow is an SEC issuer, so PCAOB standards govern the
continuing case. Three differences matter for a reader auditing a private SaaS company under AICPA standards:

1. **Terminology and mechanics of the haircut.** AU-C 320 defines *performance materiality* and requires the
   auditor to determine it. AS 2105 does not use the term; it instead requires the auditor to determine
   *tolerable misstatement* at the level of individual accounts and disclosures, in an amount less than
   overall materiality. In practice firms apply a single entity-wide haircut under both frameworks and call it
   performance materiality, but the AICPA requirement is explicit and the PCAOB requirement is expressed
   account by account. Do not write "AS 2105 requires performance materiality"; it does not.
2. **Component materiality.** AU-C 600 contains explicit requirements to determine component materiality and
   component performance materiality. The PCAOB framework addresses other auditors through AS 2101 and
   AS 1206 and does not codify "component materiality" as a defined term, although the amended standards
   require the lead auditor to determine and communicate the materiality levels the other auditor is to use.
   The arithmetic in §3.10 is the same under both.
3. **ICFR materiality.** AS 2201 has no AICPA analogue for an integrated audit of an issuer. A private company
   engaged to have its ICFR examined would be performing an attestation engagement under the AICPA
   attestation standards, and the interim-materiality logic in §3.14 would not apply in the same form.

## Prerequisites and Chapter Dependencies

Read Chapter 1 first for the SaaS business model vocabulary (ARR, ACV, NRR, RPO) and for the group audit
scoping decisions that this chapter attaches numbers to, and Chapter 2 for the assertion-level risk
assessments that determine where the thresholds derived here will bind hardest. This chapter is a prerequisite
for every substantive testing chapter, because every sample size and every investigation threshold in
Chapters 4 through 10 is a function of the $940 derived in §3.5. Chapter 15 applies these numbers to sampling
mechanics, and Chapter 19 evaluates the accumulated misstatements against them.

## 3.1 What materiality is, and where the auditor's version of it comes from

Materiality is not an auditing concept that auditors invented for their own convenience. It originates in the
financial reporting framework and, for a registrant, in the securities laws. FASB Concepts Statement No. 8,
Chapter 3, describes materiality as entity-specific: information is material if omitting, misstating, or
obscuring it could reasonably be expected to influence the decisions that the primary users of a specific
reporting entity's general purpose financial statements make on the basis of those statements. SAB 99 adopts
the same formulation and adds the point practitioners most often forget: a matter is material if there is a
substantial likelihood that a reasonable investor would consider it important, and that determination cannot
be made by applying a percentage alone.

Three consequences follow, and they structure everything else in this chapter.

**Materiality is about users, not about the auditor's workload.** The threshold answers the question "how
wrong could these financial statements be and still be useful to a reasonable investor in AtlasFlow?" It does
not answer "how much testing can we afford?" When a materiality memorandum reads as though the percentage was
selected to produce a workable budget, a reviewer should reject it.

**The auditor's threshold is deliberately lower than the reporting threshold.** Management's question is
whether the statements *are* materially misstated. The auditor's question is whether they *might be*, and the
auditor must answer it with incomplete information obtained by sampling. That gap is why performance
materiality exists (§3.5), and why the clearly trivial threshold exists below that (§3.6).

**Quantitative materiality is a screen, not a conclusion.** SAB 99 is explicit that a misstatement below any
numerical threshold may still be material. Section 3.13 sets out the factor list and the Extended Case Study
works an item that fails the qualitative screen while passing the quantitative one by a wide margin.

### 3.1.1 The four thresholds and how they relate

**Exhibit 3-1. The AtlasFlow FY2025 materiality set, with the question each threshold answers (in thousands).**

| Threshold | Amount | The question it answers | Where it is used |
| --- | --- | --- | --- |
| Overall (financial statement) materiality | $1,450 | How wrong can the FY2025 statements be before a reasonable investor is misled? | Evaluating accumulated misstatements (Chapter 19); evaluating deficiency magnitude (Chapter 14) |
| Performance materiality | $940 | How wrong can any one population be before the risk that all populations together exceed $1,450 becomes unacceptable? | Designing the nature, timing, and extent of procedures; setting tolerable misstatement |
| Specific materiality | $150 | For which items would a smaller misstatement still influence a user? | Related-party, executive compensation, and sensitivity-driven disclosures |
| Clearly trivial threshold | $72 | Below what amount is an identified misstatement not worth accumulating on the summary of audit differences? | Accumulation, not scoping |

Note the ordering: $1,450 > $940 > $150 > $72. The specific materiality of $150 sits between performance
materiality and the clearly trivial threshold because it is not a haircut on $1,450 at all; it is a separate
determination driven by the nature of particular items, and it happens to land there.

## 3.2 Overall materiality: choosing the benchmark

AS 2105 directs the auditor to use a percentage of an appropriate benchmark. It does not name the benchmark,
because the appropriate one depends on what users of the specific entity's statements are looking at. For a
mature profitable manufacturer, that is usually pre-tax income. For AtlasFlow it cannot be, and the reason is
worth stating precisely rather than gesturing at: AtlasFlow reported a pre-tax loss of $(20,860) in FY2025,
$(18,100) in FY2024, and $(21,560) in FY2023. Five percent of the FY2025 pre-tax loss is $1,043; five percent
of the FY2024 loss is $905; five percent of the FY2023 loss is $1,078. Those numbers are not absurd in
magnitude, but they move 16% year over year on a company whose revenue grew 29.9% and then 24.6% — the
benchmark moves in the wrong direction relative to the size of the business, and a loss is the residual of two
large numbers, so a small percentage change in either revenue or operating expense swings it violently. A
benchmark whose year-over-year movement is uncorrelated with the scale of the entity is a bad benchmark.

The right question is what a reasonable investor in a high-growth, loss-making SaaS company is using the
financial statements to assess. The answer, supported by AtlasFlow's own MD&A, its earnings call script, and
the sell-side models the engagement team read during planning, is: the top line and its growth rate, the gross
margin, the operating leverage trend, and the liquidity runway. That points to revenue as the primary
benchmark, with gross profit, total assets, and total expenses as corroborating measures.

### 3.2.1 The four benchmarks compared

**Exhibit 3-2. Candidate benchmarks for FY2025 overall materiality (in thousands).**

| # | Benchmark | FY2025 amount | Customary range | Range low | Range high | Illustrated % | Illustrated amount | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Total revenue | 148,200 | 0.5%–1.0% | 741 | 1,482 | 1.00% | 1,482 | **Selected as primary** |
| 2 | Gross profit | 109,260 | 1.0%–2.0% | 1,093 | 2,185 | 1.30% | 1,420 | Corroborating |
| 3 | Total assets | 317,900 | 0.5%–1.0% | 1,590 | 3,179 | 0.45% | 1,431 | Corroborating |
| 4 | Total expenses (cost of revenue + operating expenses) | 172,440 | 0.5%–1.0% | 862 | 1,724 | 0.85% | 1,466 | Corroborating |
| 5 | Annual recurring revenue (non-GAAP operating metric) | 172,000 | n/a | 860 | 1,720 | — | — | **Rejected — see §3.4** |
| 6 | Adjusted EBITDA (non-GAAP) | 18,260 | 5%–10% | 913 | 1,826 | — | — | Rejected |
| 7 | Loss before income taxes | (20,860) | 5% | 1,043 | 1,043 | — | — | Rejected |
| 8 | Total stockholders' equity | 7,100 | 1%–5% | 71 | 355 | — | — | Rejected |

Notes on the arithmetic in Exhibit 3-2:

- Total expenses of $172,440 is total cost of revenue of $38,940 plus total operating expenses of $133,500.
- Adjusted EBITDA of $18,260 is the loss from operations of $(24,240) plus depreciation and amortization of
  $11,900, plus stock-based compensation of $28,700, plus the restructuring charge of $1,900. Amortization of
  deferred contract acquisition costs of $8,600 is **not** added back, because AtlasFlow's own non-GAAP
  reconciliation does not add it back.
- Total revenue, gross profit, total assets, cost of revenue, operating expenses, and the loss before income
  taxes are taken directly from the FY2025 statements.

The result that decides the question is the clustering. Benchmarks 1 through 4 — one income-statement measure
of scale, one measure of the economics of the product, one measure of the size of the balance sheet, and one
measure of the cost base — produce $1,482, $1,420, $1,431, and $1,466 respectively. The spread across four
independent measures is $62, or 4.2% of the mean of $1,450. When four unrelated benchmarks converge that
tightly, the auditor is not choosing a number so much as observing one. Brightline set overall materiality at
**$1,450**, which is 0.978% of total revenue, and documented the convergence rather than a single percentage.

**Exhibit 3-3. $1,450 expressed as a percentage of each candidate benchmark.**

| Benchmark | FY2025 amount | $1,450 as a % | Is that percentage within the customary range? |
| --- | --- | --- | --- |
| Total revenue | 148,200 | 0.978% | Yes — upper half of 0.5%–1.0% |
| Gross profit | 109,260 | 1.327% | Yes — lower half of 1.0%–2.0% |
| Total assets | 317,900 | 0.456% | Marginally below 0.5%–1.0%, i.e. conservative |
| Total expenses | 172,440 | 0.841% | Yes |
| Annual recurring revenue | 172,000 | 0.843% | Not applicable — not a financial statement measure |
| Adjusted EBITDA | 18,260 | 7.941% | Within 5%–10%, but see §3.4 |
| Loss before income taxes | (20,860) | 6.951% | Above the customary 5% |
| Total stockholders' equity | 7,100 | 20.417% | Far outside any range |

Exhibit 3-3 does the work that Exhibit 3-2 cannot. Read the last row: $1,450 is 20.4% of AtlasFlow's total
equity of $7,100. A reader might conclude that materiality is therefore too high. That conclusion would be
wrong, and the reason is instructive. AtlasFlow's equity of $7,100 is the residual of $317,900 of assets and
$310,800 of liabilities, of which $170,600 is a convertible note that the market values as a
quasi-equity instrument. Equity is 2.2% of total assets. It is a residual so thin that it carries no
information about the scale of the enterprise; the same company with $10,000 more of accumulated deficit would
have negative equity and no benchmark at all. Equity is a valid benchmark for an entity whose users care about
net asset value. AtlasFlow's users do not, and the engagement team documented that.

### 3.2.2 Rejecting the loss benchmark, with the arithmetic

The most common wrong answer on a loss-making company is to use the absolute value of the loss with the
income percentage. Here is why the engagement team rejected it in writing.

**Exhibit 3-4. Stability of candidate benchmarks across FY2023–FY2025 (in thousands).**

| Benchmark | FY2023 | FY2024 | FY2025 | FY2024 growth | FY2025 growth |
| --- | --- | --- | --- | --- | --- |
| Total revenue | 91,500 | 118,900 | 148,200 | 29.9% | 24.6% |
| Gross profit | 63,260 | 85,370 | 109,260 | 34.9% | 28.0% |
| Total operating expenses | 86,600 | 107,400 | 133,500 | 24.0% | 24.3% |
| Loss before income taxes | (21,560) | (18,100) | (20,860) | (16.1)% | 15.2% |
| Implied materiality at 5% of loss before tax | 1,078 | 905 | 1,043 | (16.1)% | 15.2% |
| Implied materiality at 1% of revenue | 915 | 1,189 | 1,482 | 29.9% | 24.6% |

The loss-based threshold falls 16.1% in a year in which revenue grew 29.9% and then rises 15.2% in a year in
which revenue growth decelerated. An auditor using it would have done *more* work in FY2024, when the company
grew faster and its systems were under more strain, than in FY2023 — for no reason connected to risk. The
revenue-based threshold rises monotonically with the scale of the business, which is what a benchmark is for.
Prior-year overall materiality was $1,190 (1% of FY2024 revenue of $118,900, rounded down), and the FY2025
figure of $1,450 is 21.8% higher against revenue growth of 24.6% — the small divergence is rounding, and the
team documented that it had reviewed whether the rounding convention produced a threshold that drifted upward
faster than the business. It did not.

## 3.3 Choosing the percentage

Once the benchmark is revenue, the percentage looks like the whole judgment. It is not, because the percentage
and the benchmark have to be chosen jointly: the test of a percentage is whether the amount it produces is
defensible against *every* benchmark, not just the one in the denominator.

Apply that test in both directions. Suppose the team had chosen 0.5% of revenue, the conservative end of the
customary band, producing $741. That amount is 0.233% of total assets and 0.678% of gross profit — below the
customary floor for both measures. A threshold that low is not merely expensive; it is unsupportable, because
it asserts that a reasonable investor in AtlasFlow would be misled by a misstatement of two-tenths of one
percent of the balance sheet. Now suppose the team had chosen 1.2% of revenue, producing $1,778. That exceeds
the top of the revenue range outright, and it is 1.63% of gross profit and 8.5% of the pre-tax loss.

**Exhibit 3-5. The defensible range for AtlasFlow FY2025 overall materiality (in thousands).**

| Benchmark | Customary range | Implied floor | Implied ceiling |
| --- | --- | --- | --- |
| Total revenue, 0.5%–1.0% | applied to 148,200 | 741 | 1,482 |
| Gross profit, 1.0%–2.0% | applied to 109,260 | 1,093 | 2,185 |
| Total expenses, 0.5%–1.0% | applied to 172,440 | 862 | 1,724 |
| Total assets, 0.5%–1.0% | applied to 317,900 | 1,590 | 3,179 |
| **Intersection of benchmarks 1–3** | | **1,093** | **1,482** |

The intersection of the revenue, gross profit, and total-expense ranges is $1,093 to $1,482. There is no amount
that satisfies all four ranges, because the total-assets floor of $1,590 is above the revenue ceiling of
$1,482. The engagement team resolved that conflict by giving total assets the least weight, and the reason is
specific: $150,600 of AtlasFlow's $317,900 of total assets — 47.4% — is cash, cash equivalents, and short-term
investments, and a further $26,900 is goodwill. A total-assets benchmark therefore assigns nearly half its
weight to a treasury portfolio that presents very little risk of material misstatement and that no user of
AtlasFlow's statements is analyzing. Total assets is the right benchmark for an asset-heavy entity. AtlasFlow
is not one.

**The defensible range is $1,093 to $1,482, and the illustrated answer of $1,450 sits at the 92nd percentile of
that range.** What would move it down? A restatement in the prior three years; a covenant within 10% of breach;
a material weakness already identified at planning that the team knew would not be remediated; documented
evidence of management bias in prior-period estimates; or a significantly narrower shareholder base. What
would move it up? Very little, because $1,482 is a hard ceiling once revenue is the benchmark.

### 3.3.1 Why the risk response belongs in performance materiality, not in overall materiality

A common reviewer challenge on this file was: given that FY2025 is AtlasFlow's first integrated audit, that the
CFO started in September 2025, that the VP of Revenue Accounting has been on a performance plan since March
2025, and that two revenue accountants resigned in Q2 2025, should overall materiality not have been set at the
lower end of the range — say $1,150?

The answer is no, and the reasoning is the conceptual core of this chapter. **Overall materiality is a
judgment about users. It is not a judgment about risk.** The question it answers — how wrong can these
statements be before a reasonable investor in AtlasFlow is misled — has the same answer whether AtlasFlow's
controls are excellent or terrible. A weak control environment does not make investors more sensitive to small
errors; it makes it more likely that errors exist and less likely that the auditor's procedures will find them.
That is precisely and only a matter of how much work to do, and the threshold that governs how much work to do
is performance materiality. Brightline therefore set overall materiality at $1,450 on user grounds and applied
a 65% haircut rather than the 75% it uses on lower-risk engagements. Section 3.5 shows the arithmetic
consequence: 124 sample items in the receivable population instead of 107.

Rounding convention: the team rounds overall materiality down to the nearest $50 and performance materiality
down to the nearest $10. One percent of $148,200 is $1,482, which rounds down to $1,450. Always round in the
direction that increases work; a memorandum that rounds $1,482 up to $1,500 has increased the threshold by
1.2% for the auditor's convenience and invites the question of what else was rounded favorably.

## 3.4 Why annual recurring revenue is not a materiality benchmark

The engagement team had a genuine disagreement about this, and it is worth reproducing because the wrong
answer is superficially attractive. AtlasFlow's ARR at December 31, 2025 was $172.0 million. Management runs
the company on ARR, the CEO's performance stock units vest on ARR, the audit committee's quarterly package
leads with ARR, and every sell-side model builds revenue from ARR. If materiality is about what users care
about, and users care about ARR, why is ARR not the benchmark?

Four tests dispose of the question.

**Exhibit 3-6. Four tests applied to ARR as a candidate materiality benchmark.**

| Test | Requirement | ARR | Total revenue |
| --- | --- | --- | --- |
| 1. Is it a measure of the financial statements? | Materiality under AS 2105 and AU-C 320 is materiality *for the financial statements*; the benchmark must be an element of them. | No. ARR appears nowhere in the financial statements. It is presented in Item 7 MD&A and is "other information" for AS 2710 / AU-C 720 purposes. | Yes. It is the first line of the statement of operations. |
| 2. Is it defined by the framework? | The benchmark's definition must not be at management's discretion. | No. AtlasFlow defines ARR itself and could change the definition next quarter — for example, by including or excluding usage overage, or by annualizing December MRR rather than contracted ACV. | Yes. ASC 606 defines it. |
| 3. Is it audited? | The benchmark must be subject to the procedures that make the rest of the file reliable. | No. ARR is computed in the Snowflake RevOps datamart, which became the source for the MD&A metric only in November 2025 and was not reconciled to the general ledger for the first three quarters of FY2025 (W-11). | Yes. |
| 4. Does it measure the period, or a point in time? | A benchmark for a period's financial statements should measure that period. | No. ARR is a point-in-time annualized run rate that describes the *forward* twelve months. | Yes. |

The arithmetic makes the consequence concrete. One percent of ARR of $172,000 is $1,720. One percent of
FY2025 revenue is $1,482. ARR exceeds revenue by 16.1% ($172,000 ÷ $148,200), so using ARR as the benchmark
would raise the auditor's threshold by 16.1% — that is, would reduce the amount of testing — on the strength of
a number that management defines, computes outside the controlled financial reporting chain, and is
compensated on. That is the single most damaging feature of the proposal: **the auditor's threshold would move
upward exactly in proportion to management's success in inflating the metric it is most motivated to inflate.**
A materiality benchmark must be immune to the incentive it is being used to police.

Two follow-on points, because rejecting ARR as a benchmark is not the same as ignoring it.

- Users' interest in ARR is real and the audit must respond to it. It responds through §3.7 (specific
  materiality), §3.9 (materiality for non-GAAP and operating metrics), and the Extended Case Study, in which a
  $310 financial statement misstatement is corrected precisely because of its effect on the ARR-derived
  metrics. The response is a lower threshold for metric-sensitive items, not a higher threshold for everything.
- The same reasoning disposes of adjusted EBITDA, which is why Exhibit 3-2 rejects it despite producing an
  amount ($913 at 5%) inside the defensible range. Adjusted EBITDA is management-defined, it reconciles to a
  GAAP loss, and it is unstable: the FY2025 figure of $18,260 is dominated by the $28,700 stock-based
  compensation add-back, which is 157% of the resulting measure. A benchmark whose largest single component is
  an add-back exceeding the benchmark itself is not a measure of the business.

## 3.5 Performance materiality and the aggregation-risk rationale for the 65% haircut

**Performance materiality** is the amount, less than overall materiality, that the auditor uses when designing
procedures, in order to reduce to an appropriately low level the probability that the aggregate of undetected
and uncorrected misstatements exceeds overall materiality (AU-C 320.09). It exists because of **aggregation
risk**: the audit is not one test against one threshold but twenty-one tests against twenty-one thresholds, and
misstatements that are individually far below $1,450 can sum to more than $1,450.

Brightline set performance materiality at **$940**, which is 64.8% of $1,450 (65% of $1,450 is $942.5, rounded
down to the nearest $10).

### 3.5.1 The aggregation demonstration

Suppose the auditor had used $1,450 as the design threshold for every population — that is, no haircut. Each
population's procedures would then be designed to detect misstatement of $1,450 and would be indifferent to
anything smaller. Now consider a plausible pattern of undetected misstatement across nine of the FY2025
populations, in which no single amount is anywhere near $1,450.

**Exhibit 3-7. Aggregation risk: nine populations, no individual misstatement above $240 (in thousands).**

| Population | Illustrative undetected misstatement | % of overall materiality | % of performance materiality |
| --- | --- | --- | --- |
| Subscription revenue — cut-off at December 31 | 210 | 14.5% | 22.3% |
| Professional services — percentage-of-completion input estimate | 95 | 6.6% | 10.1% |
| Deferred revenue — accuracy of the release from the opening balance | 180 | 12.4% | 19.1% |
| Allowance for credit losses — position within the acceptable range | 240 | 16.6% | 25.5% |
| Deferred contract acquisition costs — churned-customer write-off | 140 | 9.7% | 14.9% |
| Capitalized internal-use software — stage designation | 120 | 8.3% | 12.8% |
| Accrued compensation — bonus and commission true-up | 130 | 9.0% | 13.8% |
| Stock-based compensation — PSU probability | 160 | 11.0% | 17.0% |
| Accrued indirect taxes — VAT completeness | 90 | 6.2% | 9.6% |
| **Simple sum** | **1,365** | **94.1%** | **145.2%** |
| Quadratic combination (square root of the sum of squares) | 477 | 32.9% | 50.7% |

Nine items, none of which exceeds 16.6% of overall materiality, sum to 94.1% of overall materiality. A tenth
item of $86 would breach it. And this is only nine of twenty-one significant populations in the FY2025 audit.
The simple sum of $1,365 is the worst case, which assumes every misstatement runs in the same direction; the
quadratic combination of $477 is the realistic case, which assumes the errors are independent and offset.
Performance materiality is calibrated between those poles. A 65% haircut is a statement that the engagement
team expects the aggregate to behave closer to the quadratic case than to the worst case, but not so close that
it can be ignored.

**The empirical check.** The FY2025 audit is over, so the answer is available. AtlasFlow's corrected
misstatements were $410, $290, $620, $180, and $240 (absolute values summing to $1,740). Its uncorrected
misstatements were $185, $240, $150, $95, $110, and $130 (absolute values summing to $910). The gross absolute
total of misstatements identified in the audit was **$2,650, or 182.8% of overall materiality**, and the
largest single item was $620 — which is 42.8% of overall materiality but 66.0% of performance materiality.
Procedures designed to a $1,450 tolerable misstatement would have had a materially lower probability of
detecting a $620 error in capitalized commissions. The haircut earned its keep.

### 3.5.2 The factors that set the percentage at 65% rather than 50% or 75%

Firm methodologies typically place performance materiality between 50% and 75% of overall materiality. That is
methodology, not a professional requirement; AU-C 320 requires the auditor to determine performance materiality
and says nothing about the percentage.

**Exhibit 3-8. Factors considered in setting the FY2025 haircut at 65%.**

| Factor | Direction | AtlasFlow FY2025 assessment |
| --- | --- | --- |
| Number of separately tested significant populations | More populations → lower percentage | 21 |
| History of identified misstatements | More history → lower percentage | Misstatements were identified and corrected in each of FY2022–FY2024; a $130 FY2024 accrued-commission item turns around in FY2025 (U-6) |
| Expected misstatement in the current period | Higher expectation → lower percentage | High in revenue cut-off, given the December 24–31 bookings concentration |
| Known effectiveness of ICFR | Unknown → lower percentage | FY2025 is the first year ICFR is audited; 14 gaps identified in the July 2025 internal audit readiness assessment |
| Management competence and turnover in the financial reporting function | Turnover → lower percentage | CFO started September 2025; VP Revenue Accounting on a performance plan since March 2025; two revenue accountants resigned in Q2 2025 |
| Complexity of the accounting | Higher complexity → lower percentage | ASC 606 allocation with a thinly supported SSP, ASC 340-40, a business combination, convertible notes, market-condition PSUs |
| Number and subjectivity of estimates | More → lower percentage | Five estimates identified as highly judgmental |
| Fraud risk | Higher → lower percentage | Presumed fraud risk in revenue plus the Q4 bookings concentration |
| Restatement history | None → supports a higher percentage | No restatement in FY2022–FY2024 |
| Prior-year aggregate uncorrected misstatement | Small → supports a higher percentage | FY2024 aggregate uncorrected effect was well below FY2024 materiality of $1,190 |

The last two rows are why the team did not go to 50%. The first eight are why it did not stay at 75%. Reasonable
practitioners would defend anything from 55% to 70% on these facts; the illustrated answer of 65% is in the
middle of that narrower band. Evidence that would move it to 55%: identification of a material weakness in the
revenue process before the substantive plan was finalized, or discovery that FY2024 uncorrected misstatements
had been understated. Evidence that would move it to 75%: two consecutive years of clean ICFR opinions and an
aggregate identified misstatement history below 25% of materiality — neither of which AtlasFlow has.

### 3.5.3 What the haircut costs, in sample items

**Exhibit 3-9. Sensitivity of one sample size to the performance materiality percentage.**

Population: gross accounts receivable of $38,600 at December 31, 2025. Method: monetary-unit sampling with a
reliability factor of 3.0 (no misstatement expected, 5% risk of incorrect acceptance). Sample size equals the
population divided by the sampling interval, where the interval is tolerable misstatement divided by 3.0.
Chapter 15, §15.6 owns the derivation of these formulas.

| Haircut | Performance materiality | Sampling interval | Computed sample size | Sample size used |
| --- | --- | --- | --- | --- |
| None (100%) | 1,450 | 483.3 | 38,600 ÷ 483.3 = 79.9 | 80 |
| 75% | 1,087 | 362.5 | 38,600 ÷ 362.5 = 106.5 | 107 |
| **65% (illustrated)** | **940** | **313.3** | **38,600 ÷ 313.3 = 123.2** | **124** |
| 50% | 725 | 241.7 | 38,600 ÷ 241.7 = 159.7 | 160 |

The 65% haircut costs 44 additional confirmation requests on this one population relative to no haircut, and it
saves 36 relative to a 50% haircut. Multiply that across twenty-one populations and the percentage in a
materiality memorandum becomes the single most expensive number in the audit plan. It should be documented
accordingly.

## 3.6 The clearly trivial threshold

The **clearly trivial threshold** is the amount below which an identified misstatement need not be accumulated
on the summary of audit differences. AU-C 450.05 requires the auditor to accumulate misstatements "other than
those that are clearly trivial," and the standard is explicit that clearly trivial is not a synonym for "not
material" — a clearly trivial item is one that is of a wholly different order of magnitude from materiality,
such that no accumulation of similar items could matter. Firm methodologies operationalize that idea with a
percentage of overall materiality, commonly 3% to 8%. That percentage is methodology, not a requirement.

Brightline set the FY2025 threshold at **$72**, which is 5% of $1,450 ($72.5, rounded down).

Four points that cause more audit-file problems than the arithmetic does:

1. **The clearly trivial threshold is not a scoping threshold.** It does not license the team to ignore
   populations below $72, to skip procedures over accounts below $72, or to decline to investigate a $60
   difference whose cause is unknown. It governs one thing: whether an already-quantified misstatement goes on
   the schedule. An unexplained difference of any size is a scope matter, not an accumulation matter.
2. **A qualitatively significant item is never clearly trivial.** A $9 payment to an entity controlled by a
   director is not clearly trivial, because the relevant magnitude is not the $9. The threshold applies only
   after the qualitative screen in §3.13 has been passed.
3. **The threshold applies to the misstatement, not to the individual transaction.** Ten $30 errors caused by
   the same control failure in the same population are one $300 misstatement, not ten clearly trivial ones. The
   test is applied at the level of the aggregated error arising from a single cause. This is where teams most
   often go wrong: the self-serve channel processes 11,400 accounts through Stripe, and a systematic $4-per-
   account error would produce a $46 misstatement that is genuinely below $72, while a systematic $12-per-
   account error would produce $137, which is not.
4. **A projected misstatement is compared to the threshold, not the known one.** If a sample yields $18 of known
   misstatement that projects to $185 across the population (as U-1 did), the accumulated amount is $185.

**Exhibit 3-10. The clearly trivial threshold at alternative percentages, and the practical consequence.**

| Percentage of overall materiality | Threshold | Approximate number of FY2025 identified items excluded from the summary of audit differences | Comment |
| --- | --- | --- | --- |
| 3% | 43 | 4 | Defensible; increases schedule clutter with items that cannot matter |
| **5% (illustrated)** | **72** | **9** | Illustrated answer |
| 8% | 116 | 14 | Defensible, but $116 is 12.3% of performance materiality, which is high enough that a reviewer should ask whether excluded items were tested for a common cause |
| 10% | 145 | 17 | Not defensible on this engagement: ten such items would equal overall materiality |

The last row is the discipline. If the threshold is set at a level where ten excluded items would equal overall
materiality, the threshold is not "clearly trivial." At $72, it takes 21 excluded items to reach $1,450, and 14
to reach $940.

## 3.7 Specific materiality for particular classes, balances, and disclosures

AS 2105 and AU-C 320 both require the auditor to consider whether, in the specific circumstances of the entity,
misstatements of amounts *less than* overall materiality could reasonably be expected to influence users'
judgments about particular classes of transactions, account balances, or disclosures. Where that is the case,
the auditor determines a lower amount for those items. Brightline calls it **specific materiality**; other
firms call it a lower materiality level for particular items. The concept is not optional and it is not the same
as performance materiality: performance materiality is a haircut on a user-based threshold to control
aggregation risk, whereas specific materiality is a *different user-based threshold* for items where users are
more sensitive.

Brightline determined specific materiality of **$150** for FY2025.

**Exhibit 3-11. Specific materiality determinations and the items considered and rejected (in thousands).**

| Item | Threshold applied | Basis |
| --- | --- | --- |
| Related-party transactions and balances — measurement | 150 | Users of a registrant's statements read related-party amounts as an integrity signal rather than as an economic amount; the amount that would influence that reading is small |
| Related-person transactions — identification and completeness for the proxy disclosure | 120 | The Regulation S-K Item 404(a) threshold itself; the team tests for completeness at the SEC's own threshold, which is lower than specific materiality |
| Executive compensation disclosures | 150 | Same reasoning; also the interaction with the ARR-based PSUs in §3.13 |
| Contingencies, legal matters, and loss accruals — disclosure | 150 | A user's assessment of a contingency turns on its existence and range, not on the accrued amount |
| Liquidity and covenant disclosures | 150 | The revolver's $40,000 minimum-liquidity covenant is disclosed; an error of $150 in the covenant computation would be read as a control failure |
| Revenue — considered, not set | 940 (performance materiality applies) | See discussion below |
| Segment disclosure — not applicable | n/a | AtlasFlow has a single reportable segment; there is no allocation for a user to be misled about |
| Cash and short-term investments — considered, not set | 940 | The $3,100 Harborview policy exception is a control and disclosure matter, not a measurement matter (Chapter 8, §8.9) |

The row that generated debate on the engagement was revenue. Given that AtlasFlow's users read revenue through
the ARR and NRR lenses, and given the Extended Case Study in this chapter, should specific materiality of, say,
$500 have been set for revenue?

Brightline concluded no, for two reasons. First, a specific materiality for revenue would flow into tolerable
misstatement for every revenue population and would roughly double the revenue sample sizes: at $500, the
monetary-unit sample over the $148,200 revenue population would be $148,200 ÷ ($500 ÷ 3.0) = 889 items rather
than the 473 items indicated by $940. That is an enormous expenditure to address a sensitivity that is
qualitative rather than quantitative. Second, the qualitative evaluation required by AS 2810 and SAB 99 already
addresses it, and it addresses it better, because it looks at the *character* of the misstatement rather than
its size — which is exactly what the Extended Case Study demonstrates. **Practice varies here**, and a firm that
sets specific materiality of $500 to $750 for revenue on a metric-driven SaaS registrant has a defensible
position; the argument against it is cost and the argument for it is that a documented threshold is harder to
rationalize away at 11 p.m. on the day before the report date than a qualitative screen is.

Arithmetic check on the sample sizes quoted: $148,200 ÷ ($940 ÷ 3.0) = $148,200 ÷ $313.3 = 473.0; $148,200 ÷
($500 ÷ 3.0) = $148,200 ÷ $166.7 = 889.2. Chapter 15, §15.6 explains why these are upper bounds that
stratification and full-population testing reduce substantially in practice.

## 3.8 Materiality for disclosures

Disclosure materiality divides cleanly into two cases, and the second is the one that gets missed.

**Case 1: the disclosure contains an amount.** Apply the same thresholds. AtlasFlow's deferred revenue
roll-forward, the RPO disclosure of $214,000, the revenue disaggregation, the equity award tables, and the
credit-loss allowance roll-forward all contain amounts that can be compared to $1,450 and $940.

There is a real judgment inside Case 1: is the relevant threshold materiality *to the financial statements as a
whole*, or materiality *to the disclosure*? Consider the geographic revenue disaggregation: United States
$109,400, United Kingdom $26,300, Australia $12,500, totalling $148,200. Suppose $1,600 of revenue is
classified to the United States that belongs to Australia. That is 1.1% of total revenue and 1.5% of the US
category — plainly immaterial to either. But it is 12.8% of the Australia category. Practice varies. The
stricter pole holds that a disclosure category is a piece of information in its own right and a 12.8% error in
it is material. The more common pole holds that materiality is determined for the financial statements taken as
a whole and a $1,600 reclassification between geographic categories, with no effect on any total, subtotal,
margin, or trend, is immaterial. Brightline took the second position and documented it, while noting that its
conclusion would change if the misclassification affected the geography whose growth rate management highlights
in MD&A. Chapter 4, §4.12 tests this disclosure.

**Case 2: the disclosure contains no amount.** Materiality still applies, and it cannot be assessed by
arithmetic. Concepts Statement No. 8 speaks of omitting, misstating, **or obscuring** information. The framework
below is Brightline methodology, not a professional requirement, but it produces documentation a reviewer can
follow.

**Exhibit 3-12. Five-question framework for the materiality of a narrative disclosure.**

1. Is the disclosure required by the framework, by SEC rule, or by Rule 12b-20 (information necessary to make
   required statements not misleading)? If required, omission is a departure regardless of amount.
2. What is the amount, transaction, or condition to which the disclosure *relates*? That amount, not the length
   of the narrative, is the magnitude for materiality purposes.
3. If the narrative were absent or wrong, what decision would a reasonable investor make differently?
4. Does the narrative obscure? Is a material fact buried in boilerplate, or aggregated with dissimilar items?
5. Is the subject matter one where users' expectations are set by something other than amount — integrity,
   compliance, control effectiveness, or management's own emphasis?

**Exhibit 3-13. The framework applied to four FY2025 AtlasFlow disclosures.**

| Disclosure | Amount it relates to | Conclusion |
| --- | --- | --- |
| Exclusion of Kestrel Labs from management's Section 404(a) assessment | Kestrel contributed $340 of FY2025 revenue but the goodwill and intangibles recognized are $14,500 and $8,000 | Material. Question 5 governs: the disclosure concerns the *scope of an assertion about control effectiveness*, and a user's reliance on management's ICFR conclusion depends on knowing what it excludes. The $340 of revenue is irrelevant to the analysis. |
| Description of the standalone selling price methodology for the Insight module | Insight revenue of $26,700 and the allocation across nearly every FY2025 multi-element contract | Material. Question 2 governs: the amount to which it relates is the whole allocation, not the Insight line. Chapter 5, §5.7 tests it. |
| Concentration of credit risk | Top ten enterprise receivables of $13,230, being 35.9% of enterprise accounts receivable of $36,900 | Material. No single customer exceeds 10% of revenue, so the ASC 280 concentration threshold is not met, but a 35.9% concentration in ten names is decision-useful and AtlasFlow discloses it. |
| Description of the workflow-run overage pricing mechanism | Usage overage revenue of $4,200, being 2.8% of total revenue | Not material on amount alone. However, question 4 applies: usage overage grew from $780 in Q1 to $1,390 in Q4, a 78.2% increase, and MD&A attributes part of the revenue growth to it. Aggregating it into "subscription revenue" without describing the mechanism obscures. Brightline requested and obtained a description. |

Arithmetic check: $13,230 ÷ $36,900 = 35.9%; $1,390 ÷ $780 = 1.782, a 78.2% increase; $4,200 ÷ $148,200 = 2.8%.

## 3.9 Materiality for non-GAAP measures and operating metrics

AtlasFlow discloses, outside the financial statements, ARR of $172.0 million, NRR of 112%, dollar-based gross
retention of 91%, 604 customers with ARR of $100 thousand or more, 3,140 enterprise and mid-market customers,
11,400 self-serve accounts, and Q4 average DSO of 68 days. It also discloses RPO of $214.0 million, of which
$138.9 million (64.9%) is expected to be recognized within twelve months.

The first discipline is to separate three categories that practitioners routinely conflate.

**Exhibit 3-14. Three categories of measure, and the auditor's responsibility for each.**

| Category | AtlasFlow examples | Governing framework | Auditor's responsibility | Threshold that applies |
| --- | --- | --- | --- | --- |
| Financial statement disclosure | RPO of $214,000 and the 64.9% twelve-month portion; deferred revenue roll-forward; revenue disaggregation | ASC 606-10-50 | Audited. Included in the opinion. | Overall materiality $1,450; performance materiality $940 |
| Non-GAAP financial measure | Adjusted EBITDA; non-GAAP operating margin; free cash flow | Regulation G; Regulation S-K Item 10(e) | Not audited. Read as other information under AS 2710 / AU-C 720; consider material inconsistency with the audited statements and with knowledge obtained; consider whether the presentation complies with Item 10(e) | No audit threshold; inconsistency assessed against the reconciling GAAP amount |
| Operating metric | ARR; NRR; gross retention; customer counts; DSO | None. Management-defined | Not audited. Read as other information; consider material inconsistency and whether it reveals a financial statement misstatement | Assessed against the metric's own scale and the user's sensitivity, not against $1,450 |

Three practical consequences.

**RPO is not in the same category as ARR.** RPO is a required ASC 606 disclosure inside the audited financial
statements. It is recomputed and tested (Chapter 6, §6.9), and a misstatement of it is a financial statement
misstatement measured against $1,450. ARR is not. Teams that treat the two as interchangeable "SaaS metrics"
under-audit RPO and over-claim on ARR. Note also that the two are not reconcilable to each other by
arithmetic: RPO of $214,000 reflects contracted but unsatisfied performance obligations over the whole
remaining term, while ARR of $172,000 annualizes a point-in-time run rate; the ratio of $214,000 to $172,000 is
1.24, which is a statement about weighted-average remaining contract term, not an identity.

**A metric can be materially wrong at a dollar amount that is quantitatively trivial.** ARR of $172,000 divided
by NRR's cohort denominator produces a ratio quoted to a whole percentage point. The Extended Case Study works
an ARR error of $792 — 0.46% of ARR — that moves the disclosed NRR from 111% to 112%. Ratios amplify. When the
auditor reads other information for material inconsistency, the arithmetic to perform is not "is $792 material
against $1,450" but "what does $792 do to the ratio as disclosed."

**The metric may be produced outside the financial reporting chain.** AtlasFlow's ARR and NRR are computed in
the Snowflake RevOps datamart (system 13), which became the reporting source in November 2025 and was not
reconciled to the general ledger for the first three quarters of FY2025 (W-11). Access to Snowflake is broader
than access to the source systems. That does not change the auditor's reporting responsibility, but it changes
the plausibility of the metric and therefore the extent of reading and inquiry required. Chapter 12, §12.13
owns the datamart; Chapter 19, §19.11 owns the other-information conclusion.

## 3.10 Component and group materiality

AtlasFlow consolidates four legal entities. Chapter 1, §1.9 owns the scoping decision; this section owns the
numbers that follow from it.

**Exhibit 3-15. Component materiality allocation, FY2025 (in thousands).**

| Component | FY2025 revenue | Revenue share | FY2025 total assets | Scope | Square-root indication | Component materiality | % of group overall materiality | Component performance materiality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AtlasFlow, Inc. (US) | 109,400 | 73.8% | 271,100 | Audited by the group engagement team | n/a | 1,450 (group figure applies) | 100.0% | 940 |
| AtlasFlow Software Ltd (UK) | 26,300 | 17.7% | 31,600 | Full scope — Brightline UK LLP | 611 | **580** | 40.0% | **380** |
| AtlasFlow Pty Ltd (Australia) | 12,500 | 8.4% | 12,900 | Specified procedures — group team | 421 | **420** | 29.0% | 420 used as the design threshold |
| AtlasFlow India Private Limited | — | — | 2,300 | Analytical procedures — group team | n/a | None determined | — | — |
| **Total** | **148,200** | **100.0%** | **317,900** | | | | | |

### 3.10.1 How the $580 and the $420 were derived

**Step one: reject pro-rata allocation.** Allocating $1,450 in proportion to revenue gives the UK 17.7% ×
$1,450 = $257 and Australia 8.4% × $1,450 = $122. Notice what that produces: $257 is 0.98% of the UK's own
revenue of $26,300 — the identical percentage the group team applied to consolidated revenue. Pro-rata
allocation on a size measure is therefore mathematically equivalent to auditing each component to its own
stand-alone materiality, which is the wrong objective. The UK entity does not issue financial statements to
UK users; its numbers matter only to the extent they affect the group. A $580 misstatement in the UK is a $580
misstatement in the group, and $580 is 40% of group overall materiality.

**Step two: apply a concave allocation.** Brightline's methodology indicates component materiality as the
square root of the component's share of the chosen benchmark, multiplied by group overall materiality:

- UK: √(26,300 ÷ 148,200) × $1,450 = √0.17746 × $1,450 = 0.42126 × $1,450 = $611
- Australia: √(12,500 ÷ 148,200) × $1,450 = √0.08435 × $1,450 = 0.29042 × $1,450 = $421

The square root is not magic; it is a way of producing a threshold that falls as the component gets smaller but
falls more slowly than size does, which is the economic property required. Firm methodologies differ — some use
a fixed band of 20% to 75% of group materiality with judgmental placement inside it, some use a fraction of the
component's own benchmark subject to a group cap. All of them share the property that the allocation is concave
and that the sum exceeds the group figure.

**Step three: overlay risk.** Australia was set at $420, essentially the indicated $421 rounded down, because
the Australian entity is a straightforward sales-and-contracting entity, the October 2025 restructuring
consolidated its office, and no misstatement had been identified there in prior years.

The UK was set at $580 — 5.1% below the indicated $611 — for three documented reasons: (a) corrected
misstatement C-4 was a $180 understatement of accrued VAT in the UK entity, so the component has a live error
history; (b) the UK entity's functional currency is GBP and its balances are translated in the
consolidation workbook (system 20), which has no version control and is emailed among four people (W-8), so
misstatements arising at the component can be compounded on translation; and (c) FY2025 is the first year the
component auditor performs work supporting an integrated audit opinion.

**Step four: apply the haircut at the component.** Component performance materiality for the UK is 65% × $580 =
$377. The engagement team documented **$380**, rounding to the nearest $10. This is the one place in the
FY2025 file where a rounding convention rounds *upward*, by $3 or 0.8%, and the team documented why it did not
matter: the UK entity's gross trade receivables are $5,600, and the indicated monetary-unit sample is
$5,600 ÷ ($377 ÷ 3.0) = 44.6 → 45 items at $377 and $5,600 ÷ ($380 ÷ 3.0) = 44.2 → 45 items at $380, so no
procedure changed. A team that rounds only downward would document $370, and that is the more defensible
convention. Do not let a rounding convention silently raise a threshold.

Australia is a specified-procedures component, so no separate component performance materiality is determined;
the group team designs the specified procedures over Australian revenue, receivables, and cash to the $420
threshold directly. This produces an apparent anomaly that a reviewer should be able to explain: **Australia's
design threshold of $420 is higher than the UK's design threshold of $380, even though Australia is less than
half the UK's size.** The reason is that the two numbers sit at different steps of the two-step process — $420
is a component materiality and $380 is a component materiality that has already had a 65% haircut applied. The
comparable UK number is $580.

### 3.10.2 Why the sum of component materialities exceeds overall materiality

**Exhibit 3-16. The component aggregation check (in thousands).**

| Measure | US | UK | Australia | Simple sum | Quadratic combination | Group overall materiality | Simple sum as % of group |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Component materiality | 1,450 | 580 | 420 | 2,450 | 1,617 | 1,450 | 169.0% |
| Component performance materiality / design threshold | 940 | 380 | 420 | 1,740 | 1,098 | 1,450 | 120.0% |

Quadratic combinations: √(1,450² + 580² + 420²) = √(2,102,500 + 336,400 + 176,400) = √2,615,300 = 1,617.
√(940² + 380² + 420²) = √(883,600 + 144,400 + 176,400) = √1,204,400 = 1,098.

The sum of component materialities is $2,450, or 169.0% of group overall materiality of $1,450. **That is
correct and expected, not an error, and a reviewer who challenges it has misunderstood what component
materiality is.** Three reasons, in order of importance:

1. **Component materiality is a design threshold, not an allowance for misstatement.** It is the amount below
   which the component auditor's procedures are permitted to be insensitive. It is not a budget of permitted
   error that has to add to a group total. The group total that matters is the aggregate of misstatements
   actually identified, which is evaluated against $1,450 in Chapter 19.
2. **Allocating so the sum equals the group figure produces absurd results.** If $1,450 had to be allocated
   exactly, the UK and Australia would be audited to $257 and $122 (see step one above), and the US to $1,071 —
   thresholds so low that the aggregate cost of the group audit could not be justified by any assessment of
   risk. Worse, the allocation would depend on the number of components: bringing a fifth trivial entity into
   the group would require lowering the thresholds at the other four, which is nonsense.
3. **The correct test is probabilistic, and it passes.** For the simple sum of $1,740 to become an actual
   aggregate misstatement of $1,740, all three components would have to harbour undetected misstatement at
   exactly their full design threshold, in the same direction, simultaneously. The quadratic combination of
   $1,098 — which assumes the errors are independent — is 75.7% of overall materiality. The engagement team
   documented that the realistic aggregate sits between $1,098 and $1,740, that the lower end is comfortably
   inside $1,450, and that the higher end requires a coincidence it assessed as remote given that the US
   component's own $940 is itself subdivided across twenty-one populations.

AU-C 600 expressly contemplates this outcome, requiring only that component materiality be *lower* than group
materiality and acknowledging that the aggregate of component materialities may exceed it. What AU-C 600 does
*not* permit is setting component materiality equal to or above group materiality for a component whose
financial information is being audited for group purposes.

## 3.11 Tolerable misstatement: related to performance materiality, and not the same thing

These two terms are used interchangeably in conversation and should not be.

**Performance materiality** is an entity-level amount, determined once, that expresses how much room the
engagement leaves between the design threshold and overall materiality in order to control aggregation risk.
**Tolerable misstatement** is a procedure-level amount, determined separately for each population subjected to
a test of details, that expresses the maximum misstatement the auditor is willing to leave undetected in *that*
population. AS 2105 requires the determination of tolerable misstatement at the account and disclosure level
and describes it as an amount less than overall materiality; AU-C 530 uses it as the sampling input.

Tolerable misstatement is never higher than performance materiality. It is often equal to it, and it is set
lower when more than one sampling procedure addresses the same population (because the individual procedures'
undetected misstatements aggregate within the population) or when the population is subject to a significant
risk.

**Exhibit 3-17. Tolerable misstatement by revenue-cycle population, FY2025 (in thousands).**

| Population | FY2025 amount | Assessed risk of material misstatement | Tolerable misstatement | Basis | Indicated MUS sample size at a reliability factor of 3.0 |
| --- | --- | --- | --- | --- | --- |
| Core subscription revenue — occurrence and cut-off | 104,900 | Significant risk (presumed fraud risk in revenue) | 705 | 75% of performance materiality | 447 |
| Insight subscription revenue — accuracy of allocation | 26,700 | Significant risk (SSP) | 705 | 75% of performance materiality | 114 |
| Usage overage revenue — completeness of usage data | 4,200 | Higher, not significant | 940 | = performance materiality | 14 |
| Professional services revenue — accuracy of the input measure | 12,400 | Higher, not significant | 940 | = performance materiality | 40 |
| Accounts receivable, gross | 38,600 | Moderate | 940 | = performance materiality | 124 |
| Deferred revenue — completeness | 78,200 | Higher (Chapter 6 owns it) | 705 | 75% of performance materiality | 333 |

Sample sizes are population ÷ (tolerable misstatement ÷ 3.0), rounded up: $104,900 ÷ $235 = 446.4 → 447;
$26,700 ÷ $235 = 113.6 → 114; $4,200 ÷ $313.3 = 13.4 → 14; $12,400 ÷ $313.3 = 39.6 → 40; $38,600 ÷ $313.3 =
123.2 → 124; $78,200 ÷ $235 = 332.8 → 333. These are unstratified upper bounds; Chapter 15 shows how testing
individually significant items at 100% and sampling only the residual reduces them by roughly two thirds in
practice, and Chapter 18 shows where a full-population analytic replaces the sample entirely.

Two warnings that a reviewer should look for in any file:

- **Tolerable misstatement is not the amount of misstatement the auditor accepts.** Finding $700 of misstatement
  in a population with tolerable misstatement of $705 is not a pass. The $700 is accumulated and evaluated
  against $1,450 together with everything else. Tolerable misstatement governs the *design* of the procedure;
  AS 2810 governs the *evaluation* of what the procedure finds.
- **Tolerable misstatement must be set before the sample is selected.** A file in which tolerable misstatement
  was raised after a misstatement was found is indefensible.

## 3.12 Revising materiality during the engagement

Materiality is determined at planning using the best information then available, which for a December year-end
engagement planned in August means forecast full-year results. AU-C 320.12 requires the auditor to revise
materiality if the auditor becomes aware, during the audit, of information that would have caused the auditor to
determine a different amount initially. AS 2105 requires the auditor to reevaluate the established materiality
level as the audit progresses. Neither standard permits leaving a materiality figure in place that the auditor
knows to be wrong.

Brightline set planning materiality on August 18, 2025 using AtlasFlow's July board-approved FY2025 revenue
forecast of $144,000. Actual FY2025 revenue was $148,200 — the Q4 bookings came in at record levels, and
Q4 revenue of $40,790 exceeded the $36,590 implied by the forecast net of the first three quarters' actual
results of $107,410.

**Exhibit 3-18. FY2025 materiality revision (in thousands).**

| Threshold | Planning (Aug 18, 2025) | Basis | Final (Jan 14, 2026) | Basis | Change | % change |
| --- | --- | --- | --- | --- | --- | --- |
| Benchmark: FY2025 total revenue | 144,000 | Board-approved forecast | 148,200 | Draft consolidated trial balance | 4,200 | 2.9% |
| Overall materiality | 1,400 | 1% of 144,000 = 1,440, rounded down to the nearest $50 | 1,450 | 1% of 148,200 = 1,482, rounded down to the nearest $50 | 50 | 3.6% |
| Performance materiality | 910 | 65% of 1,400 = 910 | 940 | 65% of 1,450 = 942.5, rounded down to the nearest $10 | 30 | 3.3% |
| Clearly trivial threshold | 70 | 5% of 1,400 | 72 | 5% of 1,450 = 72.5, rounded down | 2 | 2.9% |
| Specific materiality | 150 | Unchanged | 150 | Unchanged | — | — |
| UK component materiality | 560 | 40% of 1,400 | 580 | 40% of 1,450 | 20 | 3.6% |

### 3.12.1 Consequences of revising upward

**Exhibit 3-19. Consequences of a materiality revision, by direction.**

| Consequence | Upward revision (1,400 → 1,450) | Downward revision (illustrative: 1,400 → 1,350) |
| --- | --- | --- |
| Procedures already performed | Remain sufficient; they were designed to a stricter threshold | May be insufficient; interim samples must be extended |
| Illustrative effect on the accounts receivable sample | 38,600 ÷ (940 ÷ 3.0) = 124 items, down from 38,600 ÷ (910 ÷ 3.0) = 128 | 38,600 ÷ (870 ÷ 3.0) = 134 items, up from 128 — six additional confirmations, plus roll-forward implications |
| Items previously accumulated | An item between $70 and $72 could be removed from the summary of audit differences | Items previously judged clearly trivial between $67 and $70 must be recovered and accumulated |
| ICFR deficiency evaluation | Magnitude assessments recomputed against 1,450; a deficiency previously sized at 1,420 of potential magnitude changes category | Recomputed against 1,350; deficiencies previously below the threshold may now exceed it |
| Component thresholds | Must be recomputed and re-communicated to Brightline UK LLP | Same, plus the component auditor must extend work already performed |
| Documentation | The revision, its date, and its reason must be documented (AU-C 320.14) | Same, plus documentation of the extension of procedures |

Two disciplines make an upward revision defensible rather than suspicious.

**Sequence and date the revision.** The single most scrutinized entry in a materiality memorandum is an increase
recorded after misstatements were identified. Brightline documented the revision on **January 14, 2026**, the
day the draft consolidated trial balance was received, and the workpaper records that the only item then
accumulated on the summary of audit differences was U-1 (the $185 projected receivable cut-off misstatement),
which is 13.2% of the pre-revision overall materiality of $1,400. Uncorrected misstatement U-3 — the $150
revenue effect of the six December contracts whose signature dates could not be corroborated — was not
quantified until February 2, 2026, three weeks after the revision.

**Do not harvest the benefit.** Brightline's methodology forbids increasing overall materiality after receipt of
the year-end trial balance if the aggregate accumulated misstatement then exceeds 20% of the existing threshold,
and forbids removing any previously accumulated item from the summary of audit differences as a consequence of an
increase. At January 14, 2026 the accumulated aggregate was 13.2%, so the increase was permitted; no item was
removed; and no sample size was reduced, even though the arithmetic in Exhibit 3-19 would have permitted the
receivable sample to fall from 128 items to 124. Reducing already-completed work to the new minimum captures a
benefit the auditor did not earn and is the fastest way to make an increase look calibrated to a result.

### 3.12.2 The harder case: revising downward

A downward revision is the case that actually damages engagements, because it invalidates completed work.
Suppose Q4 revenue had come in at $30,000 rather than $40,790, giving FY2025 revenue of $137,410, overall
materiality of $1,350 (1% is $1,374, rounded down), performance materiality of $870 (65% is $877.5), and a
clearly trivial threshold of $67. Four things must happen, and the third is the one most files cannot do:

1. Every test of details performed at the October 31, 2025 interim date to a tolerable misstatement of $910 must
   be evaluated for sufficiency at $870 and extended where necessary — six additional receivable confirmations
   on that population alone, and proportionate extensions across the other twenty.
2. Every substantive analytical procedure's threshold for investigation must be recomputed, because that
   threshold is a function of performance materiality (Chapter 18, §18.4).
3. Every item the team judged clearly trivial at $70 must be recovered and reconsidered at $67. **This is
   possible only if the team kept a log of items it declined to accumulate.** Most files do not, and the
   engagement then has no way to demonstrate that the accumulated total is complete. Keep the log; it costs
   nothing during fieldwork and is unreconstructable afterward.
4. The ICFR deficiency evaluation must be redone, because magnitude is measured against materiality.

There is also a risk-assessment consequence that teams miss. A revenue shortfall large enough to move
materiality is itself a fraud risk factor: it increases the pressure on the December bookings population that
Chapter 17 examines. A downward materiality revision should therefore trigger a reconsideration of assessed
risk, not merely a recomputation of sample sizes.

## 3.13 Qualitative materiality factors

SAB 99 states the governing proposition: the use of a percentage as a numerical threshold may provide a starting
point for assessing materiality, but it cannot appropriately be used as a substitute for a full analysis of all
relevant considerations. AS 2810 and AU-C 450 both require the auditor to evaluate misstatements qualitatively
as well as quantitatively.

**Exhibit 3-20. Qualitative factor screen applied to three FY2025 items (in thousands).**

The three items are U-1 (projected receivable cut-off misstatement, $185), U-2 (allowance for credit losses at
the optimistic end of the acceptable range, $240), and the Extended Case Study item ($310 of understated
subscription revenue arising from seven unprocessed expansion amendments).

| # | Factor (SAB 99 unless noted) | U-1: $185 | U-2: $240 | Case study: $310 |
| --- | --- | --- | --- | --- |
| 1 | Masks a change in earnings or other trends | No | Partly — the allowance rate trend | **Yes — moves disclosed NRR from 111% to 112%** |
| 2 | Hides a failure to meet analysts' expectations | No | No | **Yes — draft ARR of $171.2M was below the sell-side consensus of $171.5M; corrected ARR of $172.0M is above it** |
| 3 | Changes a loss into income or vice versa | No | No | No |
| 4 | Concerns a segment or other portion of the business identified as playing a significant role | No | No | Yes — the enterprise and mid-market cohort |
| 5 | Affects compliance with regulatory requirements | No | No | No |
| 6 | Affects compliance with loan covenants or other contractual requirements | No | No | No — the $40,000 minimum-liquidity covenant is unaffected |
| 7 | Has the effect of increasing management's compensation | No | No | **Yes — crosses an ARR step in the 2025 PSU vesting scale, changing the payout from 75% to 85%** |
| 8 | Involves concealment of an unlawful transaction | No | No | No |
| 9 | Intentional (AS 2810 / AU-C 450) | No — sample-based cut-off errors | No — within an acceptable range | Undetermined; the one-directional pattern is a flag (see the case study) |
| 10 | Capable of precise measurement, versus an estimate (AS 2810) | Projected, not precise | An estimate; the range is $1,780 to $2,410 | Precise — $310 computed contract by contract |
| 11 | Recurring versus isolated | Recurring — the same cut-off cause as prior years | Recurring | Recurring — the amendment backlog is a process condition |
| 12 | Effect on gross margin or on a subtotal management emphasizes | No | No | Increases gross profit by $310 and gross margin by 0.06 percentage points |
| 13 | Identified by the auditor rather than by management's controls (ICFR signal) | Auditor | Neither | **Auditor** |
| 14 | Arises from a population subject to an allegation or investigation | No | No | No — the amendments are mid-year, not December |

Note factor 10. A misstatement that can be measured precisely is harder to defend leaving uncorrected than one
that falls inside a defensible estimation range. U-2's $240 is the difference between management's $1,900
allowance and the auditor's best point estimate; the case-study item's $310 is arithmetic. Note also factor 9:
intent is rarely known, but the *pattern* of a misstatement is observable, and a population of errors that all
run in the direction that helps a metric is evidence about the process even when it is not evidence about
anyone's state of mind.

Factor 7 deserves emphasis because it is the one that most often decides these questions in practice. Where a
misstatement moves a number on which management is compensated across a contractual threshold, the SEC staff's
position and the weight of practice both treat the misstatement as material almost without regard to amount. The
reason is not that the compensation dollars are large; it is that the existence of the threshold creates a motive,
and a misstatement that happens to fall on the profitable side of a motive is exactly the kind of item a
reasonable investor would want to know about.

## 3.14 Materiality in the audit of internal control over financial reporting

AS 2201 directs the auditor to use the same materiality considerations in the ICFR audit as in the financial
statement audit. Overall materiality for AtlasFlow's FY2025 ICFR audit is therefore also **$1,450**. Everything
else about how materiality operates is different, in five ways.

**Exhibit 3-21. How materiality operates differently in the two audits.**

| Dimension | Financial statement audit | ICFR audit |
| --- | --- | --- |
| The amount compared to materiality | The misstatement that *actually occurred*, known or projected | The misstatement that *could occur* — the potential magnitude of the control's failure |
| Threshold used for evaluation | Overall materiality, $1,450, applied to the accumulated aggregate | Overall materiality of $1,450 **and** interim materiality, because AS 2201 defines a material weakness by reference to the annual **or interim** financial statements |
| Role of performance materiality | Central — it drives the design of every procedure | None in evaluation. Performance materiality is a design concept; deficiency magnitude is assessed against materiality |
| Role of the clearly trivial threshold | Governs accumulation on the summary of audit differences | None. Every identified deficiency must be evaluated; a deficiency of trivial magnitude is still a deficiency, and its severity depends on likelihood as well as magnitude |
| Relevance of an actual misstatement | It is the subject matter | Evidence, but neither necessary nor sufficient. A material weakness can exist with no misstatement; an immaterial misstatement can be a strong indicator of one |
| Aggregation | Misstatements are summed and compared to $1,450 | Deficiencies are aggregated by process, account, and assertion and evaluated in combination (Chapter 14, §14.11) |

### 3.14.1 Interim materiality, computed

Because AS 2201's definition of a material weakness reaches misstatement of the **interim** financial statements,
a deficiency can be a material weakness even though its potential magnitude is comfortably below annual
materiality. The threshold that matters is then quarterly.

**Exhibit 3-22. Interim materiality by quarter, FY2025 (in thousands).**

| Quarter | Revenue | 1% of quarterly revenue | Interim materiality used (rounded down to the nearest $10) | As % of annual overall materiality |
| --- | --- | --- | --- | --- |
| Q1 | 32,980 | 329.8 | 320 | 22.1% |
| Q2 | 36,040 | 360.4 | 360 | 24.8% |
| Q3 | 38,390 | 383.9 | 380 | 26.2% |
| Q4 | 40,790 | 407.9 | 400 | 27.6% |
| **FY2025** | **148,200** | **1,482.0** | **1,450** | **100.0%** |

Practice varies on how interim materiality is computed. The illustration above applies the annual percentage to
the quarter's own revenue. An alternative approach annualizes interim results and applies the annual percentage,
which for AtlasFlow's Q4 would give 1% × ($40,790 × 4) = $1,632 — higher than annual materiality, which is why
Brightline does not use it for a business with sequential quarterly growth. A third approach applies annual
materiality to interim periods on the theory that the annual statements are the ones subject to the opinion; that
approach is inconsistent with AS 2201's express reference to interim financial statements and Brightline rejects
it.

### 3.14.2 Potential magnitude, worked on the December cut-off control

The control at issue is the authorization and dating of order forms in Salesforce CPQ. VP Sales Operations Brett
Hallowell can modify order-form dates, 41% of Q4 ACV — **$25,174** — was signed between December 24 and 31, 2025,
and six December contracts had signature dates the engagement team could not corroborate, with a revenue effect
of $150 if reversed (U-3).

The financial statement audit's question is: what is the misstatement? Answer: $150, which is 10.3% of $1,450.
Immaterial.

The ICFR audit's question is different: if this control failed, how large a misstatement could result, and is
there a reasonable possibility that it would not be prevented or detected?

**Exhibit 3-23. Potential magnitude of a failure of the order-form dating control (in thousands).**

| Assumption about the average number of days by which recognition is accelerated | Revenue effect = $25,174 × days ÷ 365 | Compared to Q4 interim materiality of $400 | Compared to annual materiality of $1,450 |
| --- | --- | --- | --- |
| 8 days (the maximum wholly inside the December 24–31 window) | 552 | 138% — exceeds | 38% |
| 15 days | 1,035 | 259% — exceeds | 71% |
| 21 days | 1,448 | 362% — exceeds | 99.9% — at materiality |
| 30 days (contracts signed in January dated into December) | 2,069 | 517% — exceeds | 143% — exceeds |
| Actual identified effect (U-3) | 150 | 37.5% | 10.3% |

Two conclusions follow, and they are the reason this section exists.

First, **on the most benign assumption available — that no contract was dated outside the December 24–31 window
at all — the potential magnitude of $552 already exceeds Q4 interim materiality of $400 by 38%.** A deficiency in
this control therefore has a reasonable possibility of resulting in a material misstatement of the interim
financial statements, which is the AS 2201 definition of a material weakness, without any need to assume
backdating across a period boundary.

Second, backdating by an average of only 21 days across the same population reaches annual overall materiality
of $1,450. That is not a remote hypothesis on facts that include a January 2026 whistleblower email alleging that
"December deals were papered after the fact." Chapter 14, §14.12 reaches the severity conclusion and Chapter 20
drafts the resulting report language; the point here is only that the arithmetic that gets you there is
materiality arithmetic, applied to a potential rather than an actual amount.

## 3.15 Documentation

AU-C 320.14 requires the auditor to include in the audit documentation the amounts of, and the factors
considered in determining, materiality for the financial statements as a whole, materiality levels for
particular classes of transactions, account balances, or disclosures, performance materiality, and any revision
of these. AS 1215 imposes the general requirement that the documentation support the conclusions reached. A
reviewer of the materiality workpaper should be able to answer eleven questions from the file without asking one:

1. What benchmark, and why that benchmark rather than each of the alternatives considered?
2. What percentage, and where does the resulting amount sit within the defensible range?
3. What amounts did the rejected benchmarks produce?
4. What haircut percentage, and which factors moved it up and which moved it down?
5. What clearly trivial threshold, and what is the arithmetic that shows it is genuinely trivial?
6. For which items is a lower threshold used, and why those items?
7. What component thresholds, how were they derived, and when were they communicated to the component auditor?
8. Does the aggregation check pass, and on what assumption?
9. What tolerable misstatement applies to each population subjected to a test of details, and when was it set?
10. Was materiality revised, on what date, in response to what information, and what was then accumulated?
11. How does each threshold connect to a specific procedure in the audit plan?

The Step-by-Step Walkthrough below produces exactly that file.

## Step-by-Step Walkthrough: Determining the FY2025 AtlasFlow Materiality Set

You are Chris Nwosu, the audit senior, and Grace Lindqvist has asked you to prepare WP 1300-01, the FY2025
materiality determination, for Dana Whitcombe's approval. It is January 14, 2026 and the draft consolidated trial
balance has just been received. Work in thousands of US dollars throughout.

**Step 1. Fix the benchmark data and prove it.** Obtain the draft consolidated statement of operations and
balance sheet from the FloQast close package for period 2025-12 (final), and the NetSuite trial balance export
`TB_CONSOL_2025-12_FINAL.csv`. Agree total revenue of $148,200 to the sum of accounts 4100 ($104,900), 4110
($26,700), 4120 ($4,200), 4200 ($9,300), and 4210 ($3,100). *What you compare it to:* the sum of the five
accounts, which is $148,200. *Conclusion supported:* the benchmark is drawn from the population that will be
audited, not from a management schedule. *If unexpected:* if the account sum does not agree to the reported
total, do not proceed. The difference is either account 4900 (sales returns, credits, and SLA credits of
$(1,900), which is netted within 4100–4120 and must not be deducted twice) or a top-side entry in the
consolidation workbook. Resolve it before setting materiality; Chapter 16, §16.10 owns the top-side population.

**Step 2. Compute each candidate benchmark and record the arithmetic.** Total revenue $148,200. Gross profit
$109,260 = $148,200 − $38,940. Total assets $317,900. Total expenses $172,440 = $38,940 + $133,500. Loss before
income taxes $(20,860). Total stockholders' equity $7,100. Adjusted EBITDA $18,260 = $(24,240) + $11,900 +
$28,700 + $1,900, taking depreciation and amortization and stock-based compensation from the statement of cash
flows and the restructuring charge from the statement of operations. ARR $172,000, from the Q4 2025 metrics
package. *If unexpected:* if adjusted EBITDA as you compute it does not agree to management's own non-GAAP
reconciliation in the draft earnings release, use management's definition and note the difference — you are
testing whether the measure is a suitable benchmark, and the relevant version is the one users see.

**Step 3. Apply the customary ranges and build Exhibit 3-2.** Compute the low and high of each range: revenue
0.5%–1.0% gives $741 to $1,482; gross profit 1.0%–2.0% gives $1,093 to $2,185; total assets 0.5%–1.0% gives
$1,590 to $3,179; total expenses 0.5%–1.0% gives $862 to $1,724. *Conclusion supported:* a defensible range,
not a single answer. *If unexpected:* if the ranges do not overlap at all, you have chosen benchmarks that do
not describe the same entity; revisit which of them users actually use.

**Step 4. Determine the intersection and state the defensible range.** The intersection of the revenue, gross
profit, and total-expense ranges is $1,093 to $1,482. Document why total assets receives the least weight:
$150,600 of $317,900, or 47.4%, is cash, cash equivalents, and short-term investments. *If unexpected:* if the
intersection is empty across the three benchmarks you intend to rely on, you must select one primary benchmark
and justify the departure explicitly rather than picking a number in the gap.

**Step 5. Select the percentage and the amount, and round down.** Select 1.0% of total revenue: $1,482. Round
down to the nearest $50: **$1,450**. Record that $1,450 sits at the 92nd percentile of the $1,093–$1,482 range,
and record what would move it lower (a restatement history, a covenant within 10% of breach, a material weakness
known at planning). *If unexpected:* if the rounded figure falls outside the defensible range, the rounding
convention is wrong, not the range.

**Step 6. Cross-check against every rejected benchmark.** Build Exhibit 3-3: $1,450 is 0.978% of revenue,
1.327% of gross profit, 0.456% of total assets, 0.841% of total expenses, 6.951% of the pre-tax loss, and
20.417% of equity. *Conclusion supported:* the selected amount is inside the customary range for three
benchmarks, marginally conservative against one, and outside for two that have been rejected on documented
grounds. *If unexpected:* if $1,450 is *above* the customary range for two or more benchmarks that you have not
expressly rejected, lower it.

**Step 7. Dispose of ARR in writing.** Apply the four tests in Exhibit 3-6 and record the arithmetic: 1% of ARR
is $1,720 against 1% of revenue of $1,482, a 16.1% higher threshold derived from a measure that management
defines, computes in the Snowflake RevOps datamart, and is compensated on. *If unexpected:* if a partner or a
client argues for ARR, the answer is not "firm policy"; it is test 1 — materiality is materiality for the
financial statements, and ARR is not in them.

**Step 8. Determine performance materiality.** Score the ten factors in Exhibit 3-8. Eight point toward a lower
percentage and two toward a higher one. Select 65%: 65% × $1,450 = $942.5, rounded down to the nearest $10 =
**$940**. *What you compare it to:* the firm's 50%–75% band and the prior-year percentage, which was 70% in
FY2024. *Conclusion supported:* the aggregation risk arising from twenty-one populations, a first-year ICFR
audit, and turnover in the financial reporting function. *If unexpected:* if the factor scoring points
overwhelmingly to 50% and the engagement cannot absorb the sample sizes, the answer is to escalate the resourcing
problem, not to raise the percentage.

**Step 9. Demonstrate the aggregation arithmetic.** Build Exhibit 3-7. Nine illustrative undetected
misstatements, none above $240, sum to $1,365, or 94.1% of overall materiality; their quadratic combination is
$477. Record the empirical check: the FY2025 audit ultimately identified $2,650 of gross misstatement (corrected
$1,740 plus uncorrected $910), being 182.8% of overall materiality, with a largest single item of $620 equal to
66.0% of performance materiality.

**Step 10. Determine the clearly trivial threshold.** 5% × $1,450 = $72.5, rounded down to **$72**. Record the
discipline test: 21 items at $72 are required to reach $1,450 and 14 to reach $940. Record that the threshold
governs accumulation only, and open the "below-threshold log" that §3.12.2 requires. *If unexpected:*
if the team is routinely declining to accumulate items in the $60–$72 range, aggregate them by cause before
concluding; ten $65 errors from one control failure are a $650 misstatement.

**Step 11. Determine specific materiality.** Set $150 for related-party measurement, executive compensation
disclosures, contingency disclosures, and liquidity and covenant disclosures. Separately record $120 — the
Regulation S-K Item 404(a) threshold — as the completeness threshold for identifying related-person transactions
requiring proxy disclosure. Document the consideration and rejection of a specific materiality for revenue,
including the sample-size arithmetic: at $500, the unstratified revenue sample would be 889 items against 473
at $940.

**Step 12. Allocate to components.** Compute the square-root indications: UK √(26,300 ÷ 148,200) × $1,450 =
$611; Australia √(12,500 ÷ 148,200) × $1,450 = $421. Overlay risk: reduce the UK to **$580** (40.0% of group) for
the C-4 VAT error history, the GBP translation exposure through the consolidation workbook (W-8), and the
component auditor's first integrated-audit year. Set Australia at **$420**. Compute UK component performance
materiality: 65% × $580 = $377, documented as **$380**. Record that Australia's $420 is a design threshold used
directly because Australia is a specified-procedures component.

**Step 13. Run the aggregation check on the components.** Simple sum of component materialities $1,450 + $580 +
$420 = $2,450, or 169.0% of group overall materiality. Simple sum of design thresholds $940 + $380 + $420 =
$1,740, or 120.0%. Quadratic combinations: $1,617 and $1,098 respectively. Document that $1,098 is 75.7% of
$1,450 and that the simple sum requires a coincidence assessed as remote. *If unexpected:* if the quadratic
combination of the design thresholds exceeds overall materiality, the component allocation is too generous;
reduce the largest component's threshold first.

**Step 14. Communicate the component thresholds.** Issue the group instructions to Brightline UK LLP recording
component materiality of $580, component performance materiality of $380, the clearly trivial threshold of $72
(the group figure applies — the reporting threshold to the group team is not scaled to the component), and the
requirement to report all misstatements above $72 regardless of the component thresholds. Date and retain the
transmittal. *If unexpected:* if the component auditor has already begun work to a different threshold, obtain
its threshold in writing and evaluate whether completed work must be extended.

**Step 15. Set tolerable misstatement population by population.** Build Exhibit 3-17. Set $705 (75% of
performance materiality) for Core subscription revenue, Insight subscription revenue, and deferred revenue
completeness, because each is subject to a significant risk or to more than one sampling procedure. Set $940 for
usage overage revenue, professional services revenue, and accounts receivable. Record the resulting indicated
sample sizes and the date the thresholds were set — before selection.

**Step 16. Compute interim materiality for the ICFR audit.** Build Exhibit 3-22: 1% of each quarter's revenue,
rounded down — $320, $360, $380, $400. *Conclusion supported:* the threshold against which deficiency magnitude
will be evaluated under AS 2201's "annual or interim" formulation. *If unexpected:* if a team member uses annual
materiality to conclude that a deficiency's magnitude is immaterial, send them back to this exhibit; on the
December cut-off control the two thresholds give opposite answers.

**Step 17. Document the revision.** Record the planning figures ($1,400 / $910 / $70 / $560), the final figures
($1,450 / $940 / $72 / $580), the date of the revision (January 14, 2026), the information that caused it
(actual FY2025 revenue of $148,200 against the $144,000 forecast), the aggregate then accumulated ($185, being
13.2% of $1,400), and the express statements that no accumulated item was removed and no sample size was
reduced.

**Step 18. Link each threshold to a procedure.** Add a column to the audit plan showing, for each planned test
of details, the tolerable misstatement applied and the resulting extent. A materiality memorandum that is not
referenced by any other workpaper has not been used.

**Step 19. Obtain approval and record it.** Grace Lindqvist reviews and Dana Whitcombe approves. Both signatures
and dates are required before the substantive plan is released for execution, because Step 18's extents depend on
Step 8's percentage.

**Step 20. Re-read at each subsequent reporting milestone.** Reassess after the Q4 close, after the summary of
audit differences is first populated, and before the engagement quality review. *If unexpected:* if any
reassessment indicates a lower amount, apply §3.12.2 in full rather than concluding that the difference is small.

## Extended Case Study: A $310 Understatement That Moved Net Revenue Retention from 111.4% to 112.0%

### Background

AtlasFlow discloses dollar-based net revenue retention in Item 7 of its Form 10-K and leads with it on every
earnings call. Reported NRR fell from 118% at December 31, 2024 to 112% at December 31, 2025 — a six-point
deceleration that dominated the sell-side commentary. NRR is not a GAAP measure, is not in the financial
statements, and is not covered by Brightline's opinion. It is nonetheless the number that decides whether the
CEO's performance stock units vest at 75% or 85%, because the 2025 PSU tranche is measured on the ARR that also
drives NRR's numerator.

*For purposes of this illustration, assume the following extensions to the continuing case, none of which
contradicts it.* AtlasFlow defines NRR for a period as (a) ARR at the end of the period attributable to
enterprise and mid-market customers that were customers at the beginning of the period, divided by (b) ARR at
the beginning of the period attributable to those same customers, with self-serve accounts and ARR acquired in a
business combination excluded from both the numerator and the denominator. Self-serve ARR was $5,400 at
December 31, 2024 and $7,600 at December 31, 2025. The 2025 tranche of the ARR-based PSUs vests on a stepped
scale measured against ARR at December 31, 2025 as certified by the Chief Financial Officer in whole thousands.
Sell-side consensus for December 31, 2025 ARR, as compiled by AtlasFlow's investor relations function on
January 6, 2026, was $171.5 million.

### The Facts

**Exhibit 3-24. The NRR cohort denominator and numerator, December 31, 2025 (in thousands).**

| Component | Amount |
| --- | --- |
| Total ARR, December 31, 2024 | 137,400 |
| Less self-serve ARR, December 31, 2024 | (5,400) |
| **Cohort ARR, December 31, 2024 — the NRR denominator** | **132,000** |
| Churn: cohort customers with zero ARR at December 31, 2025 | (4,470) |
| Contraction: reductions in ARR of retained cohort customers | (7,410) |
| Expansion: seat growth, Insight add-ons, and price uplift on retained cohort customers | 27,720 |
| **Cohort ARR, December 31, 2025 — the NRR numerator** | **147,840** |

**Exhibit 3-25. Reconciliation of cohort ARR to total reported ARR, December 31, 2025 (in thousands).**

| Component | Amount |
| --- | --- |
| Cohort ARR (Exhibit 3-24) | 147,840 |
| ARR from enterprise and mid-market customers acquired during FY2025 | 14,460 |
| Self-serve ARR | 7,600 |
| ARR acquired in the Kestrel Labs acquisition | 2,100 |
| **Total ARR, December 31, 2025** | **172,000** |

Both metrics compute from Exhibit 3-24:

- NRR = $147,840 ÷ $132,000 = 1.12000 = **112.0%**, disclosed as 112%.
- Dollar-based gross retention = ($132,000 − $4,470 − $7,410) ÷ $132,000 = $120,120 ÷ $132,000 = 0.91000 =
  **91.0%**, disclosed as 91%.

Now the error. During the December 2025 close, the Revenue Manager, Jordan Pike, worked the FloQast checklist item
requiring reconciliation of the Salesforce CPQ amendment population to the Zuora Billing amendment population — a
step added in November 2025 in response to the internal audit readiness assessment. Of **1,847** CPQ amendment
records with FY2025 dates, **1,809** matched a Zuora Billing amendment and **38** did not. The 38 were sitting in
the I-1 (Salesforce CPQ → Zuora Billing) error queue. Each had failed the connector's validation because the
amendment effective date preceded the last invoiced service period, producing a "backdated amendment" rejection.
The Billing Analyst who reviews the I-1 error queue daily had dispositioned each item as "resolved — manual
follow-up" and had never created the amendment.

The 38 items break down as follows:

| Category | Count | Aggregate ARR increment | FY2025 revenue effect |
| --- | --- | --- | --- |
| Quantity increases with FY2025 effective dates | 7 | 792 | 310 understated |
| Quantity increases with effective dates in January 2026 or later | 4 | 186 | — (no FY2025 service period) |
| Quantity decreases, all with effective dates of January 1, 2026 or later | 6 | (243) | — (no FY2025 service period) |
| Non-financial amendments (billing contact, purchase order number, remit-to address) | 21 | — | — |
| **Total** | **38** | | **310** |

The seven quantity increases are the misstatement. In each case the customer signed an amendment adding
automation seats, AtlasFlow provisioned the seats in the platform, the customer used them, and AtlasFlow never
invoiced and never recognized revenue.

**Exhibit 3-26. The seven unprocessed expansion amendments (in thousands, except day counts).**

| Customer | Amendment | Effective date | Annualized ARR increment (a) | Days from effective date through 12/31/2025 (b) | FY2025 revenue effect (c) |
| --- | --- | --- | --- | --- | --- |
| Calderon Foods | AMD-2025-0884 | Aug 15, 2025 | 186 | 139 | 70.8 |
| BlueRidge Insurance | AMD-2025-0791 | Aug 1, 2025 | 144 | 153 | 60.4 |
| Aeropath Group | AMD-2025-0946 | Sep 1, 2025 | 132 | 122 | 44.1 |
| Halloran Energy | AMD-2025-0703 | Jul 15, 2025 | 108 | 170 | 50.3 |
| Larkspur Dental Partners | AMD-2025-0887 | Aug 15, 2025 | 96 | 139 | 36.6 |
| Kilbourne Transit Authority | AMD-2025-1012 | Oct 1, 2025 | 78 | 92 | 19.7 |
| Westmere Credit Union | AMD-2025-0602 | Jun 1, 2025 | 48 | 214 | 28.1 |
| **Total** | | | **792** | | **310.0** |

Tick marks: (a) incremental seats per the executed amendment × the contracted monthly rate per seat × 12.
(b) inclusive of the effective date and December 31, 2025. (c) column (a) × column (b) ÷ 365.

Larkspur Dental Partners, Kilbourne Transit Authority, and Westmere Credit Union are customers introduced for
this illustration; the other four appear in the continuing case's ten largest receivable balances.

### What the Engagement Team Did

Management posted the correction itself. Journal entry **JE-2025-12-0417**, dated January 9, 2026 and posted as
part of the December close, recorded:

```text
Dr  1220  Unbilled receivables / contract assets                     310
      Cr  4100  Subscription revenue — Core                                  310
Description: Q4-25 close adj — 7 unprocessed CPQ seat-increase amendments per I-1 queue
             reconciliation; see FloQast task CL-2025-12-118 and schedule REV-AMD-Q4.
Prepared by: J. Pike    Approved by: E. Vasquez
```

The engagement team's task was therefore not to propose an adjustment but to evaluate one, which is the harder
job. Omar Haddad and Amelia Trent performed nine procedures.

1. Obtained the CPQ-to-Zuora amendment reconciliation and tested its completeness by independently extracting
   all FY2025 CPQ amendment records from Snowflake and all FY2025 Zuora Billing amendments, and reperforming the
   match. Result: 1,847 CPQ records, 1,809 matched, 38 unmatched — agreed.
2. For each of the seven items, obtained the executed amendment from Salesforce and agreed the incremental seat
   count and per-seat rate to the document.
3. Agreed each effective date to the DocuSign completion certificate rather than to the Salesforce field, because
   Brett Hallowell has the ability to modify order-form dates in CPQ.
4. Agreed the incremental seats to the AtlasFlow platform tenant provisioning log, establishing that the service
   was delivered and that the revenue is earned rather than merely contracted.
5. Confirmed from the Zuora invoice register that no invoice had been issued for any of the seven, supporting the
   debit to contract assets rather than to accounts receivable.
6. Recomputed the ARR increment and the FY2025 revenue effect for all seven items — the arithmetic in
   Exhibit 3-26 — and agreed the total of $310.0 to the journal entry.
7. **Searched for the opposite direction.** Tested all 38 queue items, not just the 7, to determine whether any
   unprocessed amendment *reduced* consideration for a FY2025 service period. Result: the 6 quantity decreases in
   the queue all had effective dates of January 1, 2026 or later, so none had a FY2025 effect. Inquired why
   decreases appear in the queue with future dates while increases appear with past dates; the Billing Analyst
   explained that customers chase credits and therefore decreases are escalated and processed, whereas an
   unbilled increase generates no customer complaint. The team corroborated the explanation by inspecting the
   queue's disposition timestamps: median days open for the 6 decreases was 4, versus 96 for the 7 increases.
8. Evaluated the effect on the ARR and NRR figures in the draft Form 10-K, recomputing both with and without the
   correction.
9. Evaluated the effect on the 2025 PSU probability assessment and on the related stock-based compensation
   expense.

### Analysis

**Quantitative.** The misstatement is $310 of understated subscription revenue and understated contract assets.
It is 21.4% of overall materiality of $1,450, 33.0% of performance materiality of $940, and 4.3 times the clearly
trivial threshold of $72. It is 0.209% of total revenue. Had it not been corrected, it would have been an
*understatement* of the loss-reducing kind, so it would have offset the uncorrected overstatements: the FY2025
uncorrected net effect of $(460) would have become $(150). No quantitative analysis makes $310 material.

**Effect on the metrics.**

**Exhibit 3-27. Effect of the correction on the disclosed metrics (in thousands, except percentages).**

| Measure | Without the correction (draft) | With the correction (as filed) | Movement |
| --- | --- | --- | --- |
| Cohort expansion ARR | 26,928 | 27,720 | 792 |
| Cohort ARR, December 31, 2025 (NRR numerator) | 147,048 | 147,840 | 792 |
| Cohort ARR, December 31, 2024 (NRR denominator) | 132,000 | 132,000 | — |
| Net revenue retention, computed | 111.400% | 112.000% | 0.600 pp |
| Net revenue retention, as it would be disclosed | 111% | 112% | 1 pp |
| Dollar-based gross retention | 91.0% | 91.0% | — |
| Total ARR, December 31, 2025 | 171,208 | 172,000 | 792 |
| Total ARR as disclosed, to the nearest $0.1 million | $171.2M | $172.0M | $0.8M |
| ARR versus sell-side consensus of $171.5M | Below by $0.3M | Above by $0.5M | — |
| 2025 PSU tranche payout under the stepped scale | 75% | 85% | 10 pp |

**Exhibit 3-28. The 2025 ARR-based PSU vesting scale and the resulting expense (in thousands).**

| ARR at December 31, 2025, as certified | Payout as a percentage of target | Cumulative expense on the 2025 tranche |
| --- | --- | --- |
| Below $165,000 | 0% | — |
| $165,000 to $169,999 | 50% | 4,467 |
| $170,000 to $171,999 | 75% | 6,700 |
| $172,000 to $174,999 | 85% | 7,593 |
| $175,000 or more | 100% | 8,933 |

The cumulative expense column derives from the continuing case. Management revised the 2025 tranche probability
from 100% to 85% in Q4 2025, producing a $1,340 catch-up credit. A 15-percentage-point reduction producing $1,340
implies $89.33 of cumulative expense per percentage point and therefore $8,933 at a 100% payout; 85% of $8,933 is
$7,593 and 75% is $6,700.

Three arithmetical facts drive the analysis.

**Fact 1: the metric's sensitivity is an order of magnitude below materiality.** NRR is disclosed to the nearest
whole percentage point, so the rounding boundary between 111% and 112% is 111.5%, which corresponds to cohort ARR
of 1.115 × $132,000 = $147,180. Draft cohort ARR was $147,048 — **$132 below the boundary**. An error of $133
would therefore have changed the disclosed metric. That amount is 9.1% of overall materiality and 1.8 times the
clearly trivial threshold. Any framework that evaluates metric-affecting misstatements against $1,450 will fail
to detect a class of errors two orders of magnitude smaller.

**Fact 2: the PSU step is exactly $792 away.** The 85% step begins at certified ARR of $172,000 and draft ARR was
$171,208. The correction is precisely the amount required to reach the step, to the thousand. That is a
coincidence in the sense that no one engineered it; it is not a coincidence the auditor may pass over without
procedures, which is why procedure 7 above exists.

**Fact 3: the correction increased the reported loss.** Recording the correction added $310 of revenue but also
sustained $893 of stock-based compensation expense ($7,593 at 85% versus $6,700 at 75%) that would otherwise have
been reversed. On a combined basis the FY2025 pre-tax loss is **$583 larger** with the correction than without it
($893 − $310). Management advocated for an adjustment that worsened its reported earnings, because the metric
mattered more than the earnings. Note the magnitudes: the $893 stock-based compensation consequence is 61.6% of
overall materiality and 95.0% of performance materiality — nearly three times the size of the revenue
misstatement that caused it.

**Qualitative.** Applying Exhibit 3-20, the item triggers factors 1, 2, 4, 7, 10, 11, and 13: it masks a trend
(the disclosed NRR decline would have been seven points rather than six), it converts a consensus miss into a
consensus beat, it concerns the cohort of the business management emphasizes, it increases management's
compensation by crossing a contractual threshold, it is capable of precise measurement, it is recurring in cause,
and it was surfaced by a reconciliation control that had existed for six weeks rather than by the control that
was supposed to prevent it. Under SAB 99 the item is material notwithstanding that it is 0.209% of revenue.

**The bias question.** AS 2810 requires the auditor to evaluate whether the audit evidence indicates bias in
management's judgments. Here the evidence cuts both ways and the team documented both sides. Against bias: the
correction is arithmetically exact and independently verifiable; management identified it without prompting; it
increased the reported loss; the queue-disposition timestamps corroborate an innocent explanation for the
directional pattern; and the mirror-image search found nothing. Consistent with bias: the amount lands exactly
on a compensation step, and the population searched — the I-1 error queue — is defined by a system rejection,
which means a *complete* search for unbilled amendments requires looking beyond the queue. The team therefore
extended its procedures to compare provisioned seat counts in the platform to billed seat counts in Zuora for the
whole enterprise population at December 31, 2025, independently of the queue. That test identified a further $41
of unbilled seats, which is below the clearly trivial threshold and was logged rather than accumulated.

**The control deficiency.** The disposition of the I-1 error queue is a control that failed. Thirty-eight of
1,847 amendment records — a 2.06% failure rate — did not process, and the daily reviewer closed them without
resolution. Applying the 2.06% rate to the $27,720 of FY2025 cohort expansion ARR indicates $571 of ARR that
could go unrecorded in a year, with a revenue effect depending on timing. The team concluded this is at least a
significant deficiency and referred it to the aggregate ICFR evaluation in Chapter 14, §14.11, where it is
considered together with W-11 (the unreconciled Snowflake datamart), because the two share a root cause: metric
and billing data flowing between systems without a reconciliation control.

### Resolution and Conclusion

The correction was appropriately supported and Brightline accepted it. Because management recorded it during the
close, it appears on neither the corrected nor the uncorrected schedule in the continuing case's summary of audit
differences — it is simply part of the $148,200 of FY2025 revenue. That fact is worth stating plainly, because a
reader who looked only at the summary of audit differences would never know this happened.

Three consequences followed:

1. **Reporting.** The team confirmed that the ARR of $172.0 million and NRR of 112% in Item 7 are consistent with
   the audited financial statements and with knowledge obtained in the audit, discharging the AS 2710 other-
   information responsibility. Had management corrected the financial statements but not the metrics, the
   disclosed NRR of 111% would have been materially inconsistent with the audited revenue, and the team would
   have requested revision.
2. **Stock-based compensation.** The team documented that management's 85% PSU probability assessment is
   *dependent* on the revenue correction and would be 75% without it, and satisfied itself that the correction
   was supported on its own merits before accepting the 85% assessment. Chapter 9, §9.9 audits the assessment.
3. **Controls.** The deficiency was communicated to the audit committee and included in the aggregate severity
   evaluation.

**Where a defensible answer could differ.** If management had *declined* to record the $310, the range of
defensible auditor positions would be narrower than the arithmetic suggests. A team concluding "immaterial, pass
it" would have to explain why crossing a compensation threshold and converting a consensus miss into a beat are
not the SAB 99 factors they plainly are. A team requiring correction — the illustrated position — is on solid
ground. The genuinely difficult variant is the one in which the correction is *not* arithmetically exact, for
example if the seat counts had to be estimated from usage telemetry, giving a range of $240 to $380: the auditor
would then be requiring correction of an estimate whose midpoint happens to cross a compensation step, and the
conversation with management becomes materially harder. What would move the conclusion: evidence that the seven
amendments were selected from a larger unbilled population, which would make the correction a choice rather than
a completeness finding.

### Workpaper Extract

```text
================================================================================
BRIGHTLINE LLP
AtlasFlow, Inc. — Audit of the financial statements and ICFR
Year ended December 31, 2025

WORKPAPER INDEX:  WP 1300-07
TITLE:            Qualitative materiality evaluation — December 2025 amendment
                  backlog correction (JE-2025-12-0417, $310)
PREPARED BY:      A. Trent (AT)              DATE PREPARED:  January 30, 2026
REVIEWED BY:      O. Haddad (OH)             DATE REVIEWED:  February 2, 2026
2ND LEVEL REVIEW: G. Lindqvist (GL)          DATE REVIEWED:  February 4, 2026
PARTNER APPROVAL: D. Whitcombe (DW)          DATE APPROVED:  February 6, 2026
CROSS-REFERENCES: WP 1300-01 (materiality determination); WP 3200-22 (revenue
                  cut-off); WP 4100-09 (ICFR deficiency log, item D-27);
                  WP 6100-03 (PSU probability assessment)
--------------------------------------------------------------------------------
1. PURPOSE

To evaluate whether the $310 understatement of FY2025 subscription revenue
corrected by management in JE-2025-12-0417 is material, and to conclude on the
sufficiency of support for the correction and on the related control deficiency.

2. SOURCE OF INFORMATION

  - Snowflake extract SF_CPQ_AMD_FY25 (1,847 records) and SF_ZBILL_AMD_FY25
    (1,809 matched records), extracted by T. Iyer on January 22, 2026; extraction
    parameters and row counts at WP 1300-07a.
  - Zuora Billing I-1 connector error queue export, 38 open items at 12/31/2025.
  - Seven executed amendment order forms retrieved from Salesforce (opportunity
    IDs at WP 1300-07b) with DocuSign completion certificates.
  - AtlasFlow platform tenant provisioning log, seat-count history, 12/31/2025.
  - Zuora invoice register FY2025.
  - NetSuite JE-2025-12-0417 and supporting schedule REV-AMD-Q4.
  - FY2025 metrics package (RevOps datamart, Snowflake) and draft Form 10-K
    Item 7, pages 48-51.
  - 2025 PSU award agreement, Exhibit A (vesting scale); Carta grant extract.
  - WP 1300-01: overall materiality $1,450; performance materiality $940;
    clearly trivial threshold $72; specific materiality $150.

3. PROCEDURES PERFORMED

  P1  Reperformed the CPQ-to-Zuora amendment match from independent extracts.
  P2  Agreed seat counts and per-seat rates to the seven executed amendments.   (a)
  P3  Agreed each effective date to the DocuSign completion certificate.        (b)
  P4  Agreed incremental seats to the platform provisioning log.                (c)
  P5  Confirmed no invoice issued (Zuora invoice register).                     (d)
  P6  Recomputed the ARR increment and FY2025 revenue effect for all seven.     (e)
  P7  Tested all 38 queue items for opposite-direction (revenue-reducing) items.
  P8  Recomputed NRR, gross retention, and total ARR with and without the
      correction; agreed the disclosed figures to the recomputation.
  P9  Recomputed the 2025 PSU cumulative expense at the 75% and 85% steps.
  P10 Compared provisioned seats to billed seats for the full enterprise
      population at 12/31/2025, independently of the error queue.

4. RESULTS

4.1 The correction, recomputed (in thousands, except day counts):

  Customer                       Amdt ARR   Days    Revenue
  ---------------------------------------------------------
  Calderon Foods                     186     139       70.8   (a)(b)(c)(d)(e)
  BlueRidge Insurance                144     153       60.4   (a)(b)(c)(d)(e)
  Aeropath Group                     132     122       44.1   (a)(b)(c)(d)(e)
  Halloran Energy                    108     170       50.3   (a)(b)(c)(d)(e)
  Larkspur Dental Partners            96     139       36.6   (a)(b)(c)(d)(e)
  Kilbourne Transit Authority         78      92       19.7   (a)(b)(c)(d)(e)
  Westmere Credit Union               48     214       28.1   (a)(b)(c)(d)(e)
  ---------------------------------------------------------
  Total                              792              310.0
  Per JE-2025-12-0417                                 310.0
  Difference                                            0.0

  Tick-mark legend
  (a) Agreed to executed amendment order form; incremental seats x contracted
      monthly rate per seat x 12 = ARR increment.
  (b) Effective date agreed to DocuSign envelope completion certificate, not to
      the Salesforce field (see WP 3200-22: order-form dates are modifiable by
      the VP Sales Operations).
  (c) Incremental seats agreed to platform tenant provisioning log; service
      delivered from the effective date.
  (d) No invoice in the Zuora invoice register; debit to account 1220 (contract
      assets) rather than 1200 (trade receivables) is correct.
  (e) Revenue effect recomputed as ARR increment x days / 365; day count
      inclusive of the effective date and December 31, 2025.

4.2 Quantitative comparison:
      $310 / overall materiality $1,450          =  21.4%
      $310 / performance materiality $940        =  33.0%
      $310 / clearly trivial threshold $72       =  4.3x
      $310 / FY2025 total revenue $148,200       =  0.209%

4.3 Metric effect: NRR 111.400% before, 112.000% after; as disclosed, 111% vs
    112%. Gross retention 91.0%, unaffected. Total ARR $171,208 vs $172,000.
    Minimum error required to move the disclosed NRR = $132 (the distance from
    draft cohort ARR of $147,048 to the 111.5% rounding boundary of $147,180).

4.4 Compensation effect: 2025 PSU tranche payout step 75% (ARR $170,000-171,999)
    vs 85% (ARR $172,000-174,999). Cumulative expense $6,700 vs $7,593;
    difference $893, being 61.6% of overall materiality and 95.0% of performance
    materiality. Combined pre-tax effect of recording the correction: loss
    $583 larger ($893 expense sustained less $310 revenue added).

4.5 Opposite-direction search (P7): 6 unprocessed quantity decreases, all
    effective January 1, 2026 or later; no FY2025 effect. Median days open:
    4 (decreases) vs 96 (increases). Explanation corroborated by timestamps.

4.6 Independent completeness test (P10): $41 of additional unbilled seats
    identified; below the $72 clearly trivial threshold; logged at WP 1300-07c
    (below-threshold log) and not accumulated.

4.7 Control deficiency: 38 of 1,847 FY2025 CPQ amendment records (2.06%) failed
    to process and were closed without resolution by the daily I-1 error-queue
    review. Applying 2.06% to FY2025 cohort expansion ARR of $27,720 indicates
    $571 of ARR at risk annually. Referred to WP 4100-09 as deficiency D-27 for
    aggregate severity evaluation with W-11.

5. CONCLUSION

The $310 correction is arithmetically supported and appropriately recorded in
FY2025. Although quantitatively immaterial (21.4% of overall materiality), the
misstatement is qualitatively material under SAB 99: uncorrected, it would have
changed a disclosed operating metric (NRR 112% to 111%), converted an ARR
consensus beat into a miss, and reduced the 2025 PSU payout step from 85% to
75%. We are satisfied that management's correction is supported on its own
merits and is not calibrated to the PSU step, based on P7 and P10. The
underlying control deficiency is at least a significant deficiency and is
referred for aggregate evaluation.

We further confirm that the ARR and NRR figures in draft Form 10-K Item 7 are
consistent with the audited financial statements and with knowledge obtained in
the audit (AS 2710).

                                                  AT  1/30/26   OH  2/2/26
                                                  GL  2/4/26    DW  2/6/26
================================================================================
```

### Lessons

1. **Ratios amplify.** A $132 error would have moved a disclosed metric. Nothing in a $1,450 materiality
   framework is calibrated to detect that, which is why §3.9's separate treatment of operating metrics is not
   academic.
2. **The direction of the earnings effect is not the test.** Management pushed for a correction that increased
   its reported loss by $583 on a combined basis, because the metric and the compensation step mattered more than
   the loss. An auditor who screens misstatements by asking "does this help or hurt earnings" will misclassify
   this item entirely.
3. **Evaluating a management-identified correction is harder than proposing one.** The population searched was
   defined by a system rejection. A complete answer required a test that did not depend on the queue at all
   (procedure 10), and that test is the only evidence in the file that the correction is a completeness finding
   rather than a selection.
4. **Search the other direction, and document that you did.** The strongest evidence against bias in this file is
   a negative result: six unprocessed decreases, none with a FY2025 effect, with timestamps that explain why.
5. **Corrections recorded during the close leave no trace on the summary of audit differences.** A reviewer
   reading only Chapter 19's schedules would not see this item. Materiality evaluation has to reach corrections
   as well as passed adjustments.
6. **A qualitatively material misstatement of $310 does not make the audit's $1,450 wrong.** Overall materiality
   is still $1,450. The lesson is that the quantitative threshold is a screen with a specific, known blind spot,
   not that it should have been lower.

## Common Mistakes

### Mistake 3.1 — Using the absolute value of a loss as the benchmark on a loss-making company

**What it looks like.** "Overall materiality is $1,043, being 5% of the pre-tax loss of $20,860."
**Why it happens.** Pre-tax income is the default benchmark in every textbook and every firm template, and the
template's formula does not care about the sign.
**What goes wrong.** The threshold becomes uncorrelated with the scale of the entity and moves in the wrong
direction: AtlasFlow's loss-based threshold *fell* 16.1% in FY2024, the year revenue grew 29.9%. Worse, the
threshold becomes hostage to a single reclassification — moving $2,000 of expense between cost of revenue and
research and development leaves the loss unchanged, but a $2,000 change in an expense accrual moves the
threshold by 9.6%.
**How to avoid it.** On any entity with a loss, a near-break-even result, or a volatile result, compute at least
four benchmarks (Exhibit 3-2), state the range each produces, and select from the intersection. If a
loss-based figure happens to land in that intersection, use the intersection as the justification, not the loss.

### Mistake 3.2 — Setting materiality on a management-defined metric

**What it looks like.** "Given that users focus on annual recurring revenue, overall materiality is $1,720, being
1% of ARR of $172.0 million."
**Why it happens.** It is genuinely true that users focus on ARR, and the reasoning "materiality is about users"
appears to lead there.
**What goes wrong.** Materiality is materiality *for the financial statements*, and ARR is not in them. Because
ARR exceeds revenue by 16.1%, the threshold rises 16.1% — the auditor does less work — on the strength of a
number management defines, computes in an unreconciled data warehouse (W-11), and is compensated on. The
threshold then moves upward in proportion to management's success in inflating the metric the auditor is
policing.
**How to avoid it.** Apply the four tests in Exhibit 3-6. Respond to users' interest in the metric through
specific materiality (§3.7) and the other-information procedures (§3.9), never through the benchmark.

### Mistake 3.3 — Lowering overall materiality to compensate for a weak control environment

**What it looks like.** "Because FY2025 is the first integrated audit and the CFO started in September 2025,
overall materiality has been set at $1,150 rather than $1,450."
**Why it happens.** It feels conservative, and conservatism is rarely challenged.
**What goes wrong.** It confuses two different judgments. Overall materiality answers a question about users,
whose sensitivity to error does not change because a client's controls are weak. Risk belongs in performance
materiality. Conflating them produces a file in which the same fact is counted twice — once in overall
materiality and again in the haircut — and in which the evaluation threshold in Chapter 19 is understated, so
that a $1,300 aggregate misstatement is reported as material when it is not.
**How to avoid it.** Set overall materiality on user grounds and document that risk was addressed in the haircut.
If the haircut is already at the bottom of the band and the risk is still not addressed, the answer is a change
in the nature of procedures, not a change in the threshold.

### Mistake 3.4 — Treating the clearly trivial threshold as a scoping or investigation threshold

**What it looks like.** A memo stating "differences below $72 will not be investigated," or a lead schedule with
a note that accounts below $72 were not tested.
**Why it happens.** The threshold is the smallest number in the memorandum, so it gets read as a floor for
everything.
**What goes wrong.** An unexplained difference of $60 whose cause is unknown may be the visible edge of a
systematic error. The self-serve population is 11,400 accounts; a $4-per-account error is $46 and a
$12-per-account error is $137. Declining to investigate the cause forfeits the only information that
distinguishes them.
**How to avoid it.** Write the threshold's scope into the memorandum in one sentence: "This threshold governs
whether an identified and quantified misstatement is accumulated on the summary of audit differences. It does
not govern scoping, sample selection, or the investigation of differences."

### Mistake 3.5 — Applying the clearly trivial threshold item by item rather than to the aggregated error

**What it looks like.** Fourteen $58 errors arising from the same misconfigured proration rule, each documented
as clearly trivial, none accumulated.
**Why it happens.** The threshold is applied at the point where each error is found, which is transaction by
transaction.
**What goes wrong.** Fourteen items at $58 is $812 — 86.4% of performance materiality — and the audit file records
nothing.
**How to avoid it.** Aggregate by cause before applying the threshold. The unit of analysis is the misstatement
arising from a single root cause across the whole population, not the individual transaction. Ask of every
below-threshold item: what caused this, and how many other items share that cause?

### Mistake 3.6 — Allocating group materiality pro rata so the component amounts sum to the group figure

**What it looks like.** "Group materiality of $1,450 has been allocated: US $1,071, UK $257, Australia $122;
total $1,450."
**Why it happens.** The word "allocate" implies a fixed quantity being divided, and a total that foots looks
correct.
**What goes wrong.** Pro-rata allocation on a size measure is mathematically identical to auditing each component
to its own stand-alone materiality — $257 is 0.98% of the UK's own revenue, the same percentage the group team
applied to consolidated revenue. That is the wrong objective, because the UK entity's numbers matter only
through the group. The allocation also becomes dependent on the number of components: adding a fifth trivial
entity would force the thresholds at the other four downward.
**How to avoid it.** Use a concave allocation (§3.10.1), accept that the sum exceeds the group figure, and
document the aggregation check in Exhibit 3-16 — including the quadratic combination, which is the number that
demonstrates the allocation is defensible.

### Mistake 3.7 — Confusing performance materiality with tolerable misstatement, or setting tolerable misstatement after selection

**What it looks like.** A sampling workpaper whose "tolerable misstatement" field is populated with $1,450; or a
field populated with $940 for every population regardless of risk; or a field that was completed after the
sample results were evaluated.
**Why it happens.** The two terms are used interchangeably in conversation, and sampling templates often
auto-populate.
**What goes wrong.** Using $1,450 abandons the haircut and reduces the receivable sample from 124 items to 80.
Using $940 uniformly ignores that two sampling procedures over the same population aggregate within it.
Populating the field after evaluation is indefensible and is the kind of finding that ends an inspection well.
**How to avoid it.** Set tolerable misstatement population by population, before selection, in a single schedule
(Exhibit 3-17), with the date it was set. Record the basis: equal to performance materiality, or a stated
percentage of it, and why.

### Mistake 3.8 — Evaluating an ICFR deficiency's magnitude against annual materiality only

**What it looks like.** "The potential magnitude of this deficiency is $552, which is below overall materiality of
$1,450. The deficiency is not a material weakness."
**Why it happens.** Annual materiality is the number in the file, and AS 2201 says to use the same materiality
considerations as the financial statement audit.
**What goes wrong.** AS 2201 defines a material weakness by reference to a reasonable possibility of material
misstatement of the **annual or interim** financial statements. AtlasFlow's Q4 interim materiality is $400. A
$552 potential magnitude is 138% of it. The conclusion reverses.
**How to avoid it.** Compute interim materiality at the start of the engagement (Exhibit 3-22) and put it in the
same workpaper as annual materiality, so no one has to remember it exists. Every deficiency magnitude assessment
should show both comparisons.

### Mistake 3.9 — Measuring deficiency magnitude by the misstatement that occurred

**What it looks like.** "We identified a $150 misstatement from this control failure. Magnitude is $150."
**Why it happens.** The financial statement audit measures actual misstatement, and the habit carries over.
**What goes wrong.** The ICFR audit measures *potential* magnitude — what could occur, not what did. The general
rule is that the maximum amount by which an account could be overstated is the recorded amount of the account or
of the transaction population the control governs. The order-form dating control governs $25,174 of December
24–31 ACV; a 21-day average acceleration reaches $1,448. The $150 that happened to be found is evidence about
likelihood, not a measure of magnitude.
**How to avoid it.** For every deficiency, state the population the control governs, state the mechanism by
which failure produces misstatement, and compute the amount at two or three plausible failure severities, as in
Exhibit 3-23.

### Mistake 3.10 — Increasing materiality after misstatements are identified, and then harvesting the benefit

**What it looks like.** A revision memo dated after the summary of audit differences is populated, raising
materiality from $1,400 to $1,750, accompanied by the removal of two accumulated items and a reduction in three
sample sizes.
**Why it happens.** The actual benchmark turned out higher than forecast, and the template recomputes
mechanically.
**What goes wrong.** Even where the revision is substantively correct, the sequence destroys its credibility. The
file now shows a threshold that moved in the direction that made an identified problem disappear.
**How to avoid it.** Revise at the moment the new information arrives, date it, and record what was accumulated on
that date. Adopt and follow a rule that forbids increasing materiality if the accumulated aggregate exceeds a
stated percentage of the existing threshold, and never remove a previously accumulated item or reduce a
completed sample as a consequence of an increase. Brightline's FY2025 file records the revision on January 14,
2026, the accumulated aggregate of $185 (13.2%), and the express statement that nothing was removed or reduced.

### Mistake 3.11 — Not keeping a log of items declined as clearly trivial

**What it looks like.** No log at all. The team knows it saw small items and passed them; the file records
nothing.
**Why it happens.** Logging items you have decided not to record feels like make-work.
**What goes wrong.** Two things, both fatal in review. First, if materiality is revised downward, there is no way
to reconsider the items now above the threshold, so the accumulated total cannot be shown to be complete. Second,
Mistake 3.5's aggregation-by-cause analysis is impossible: you cannot aggregate items you did not write down.
**How to avoid it.** One row per item: amount, account, cause, population, date, who decided. In the AtlasFlow
file this is WP 1300-07c, and it is where the $41 of additional unbilled seats from the Extended Case Study
lives.

### Mistake 3.12 — Treating a disclosure with no amount as automatically immaterial

**What it looks like.** A disclosure checklist entry reading "N/A — no dollar amount, therefore not material."
**Why it happens.** Materiality is taught as arithmetic, and there is no arithmetic available.
**What goes wrong.** AtlasFlow's disclosure that Kestrel Labs is excluded from management's Section 404(a)
assessment carries $340 of revenue and controls the meaning of management's entire ICFR conclusion. Its
materiality has nothing to do with $340. Concepts Statement No. 8 speaks of omitting, misstating, **or
obscuring**, and obscuring is the failure mode with no arithmetic.
**How to avoid it.** Apply the five questions in Exhibit 3-12. Question 2 — what amount, transaction, or condition
does the disclosure relate to — converts most narrative disclosures into a quantifiable magnitude. Question 5
catches the rest.

### Mistake 3.13 — Rounding upward

**What it looks like.** "1% of revenue is $1,482; overall materiality is set at $1,500." Or performance
materiality of $942.5 recorded as $950.
**Why it happens.** Round numbers look tidier, and the amounts involved seem immaterial to materiality.
**What goes wrong.** Rounding $1,482 up to $1,500 raises the threshold 1.2% for no reason connected to users, and
it invites the reviewer's next question, which is what else in the file was rounded favorably. The cumulative
effect compounds: rounding overall materiality up and then the haircut up raises the design threshold by 2% to
3%, which is a real number of sample items.
**How to avoid it.** Adopt a convention that rounds down at every step, state it in the memorandum, and apply it
even where it is inconvenient. Where a rounding must go up — as the UK's $377 to $380 did — say so explicitly and
demonstrate that no procedure changed.

## Practice Exercises

All amounts are in thousands of US dollars. Where an exercise varies a continuing-case fact, the variation is
hypothetical and stated as such.

### Exercise 3-1

**[Foundational]** *Hypothetically*, assume AtlasFlow's FY2025 results had been: total revenue $132,600, total
cost of revenue $35,900, total operating expenses $123,000, total assets $291,400, and a pre-tax loss of
$(24,300). Using ranges of 0.5%–1.0% for revenue, 1.0%–2.0% for gross profit, 0.5%–1.0% for total expenses, and
0.5%–1.0% for total assets:

1. Compute gross profit and total expenses.
2. Compute the low and high of each of the four ranges.
3. State the intersection of the revenue, gross profit, and total-expense ranges.
4. Select overall materiality at 1.0% of revenue, rounded down to the nearest $50, and state where it falls
   within the intersection as a percentile.
5. State $1,450 — the actual FY2025 figure — as a percentage of the hypothetical revenue, and say whether it
   would still have been defensible.

### Exercise 3-2

**[Foundational]** Using overall materiality of $1,300 from Exercise 3-1:

1. Compute performance materiality at 60%, 65%, and 70%, rounding down to the nearest $5.
2. Compute the clearly trivial threshold at 3%, 5%, and 8%, rounding down to the nearest $1.
3. For a gross receivable population of $28,400, compute the monetary-unit sampling interval and sample size at
   each of the three performance materiality figures, using a reliability factor of 3.0 and rounding sample sizes
   up to the next whole item.
4. State how many items at the 5% clearly trivial threshold would be required to reach performance materiality
   at 65%, and to reach overall materiality.

### Exercise 3-3

**[Intermediate]** Continuing the hypothetical from Exercises 3-1 and 3-2, assume the group comprises a parent
with revenue of $88,000, Subsidiary A with revenue of $29,600, and Subsidiary B with revenue of $15,000. Group
overall materiality is $1,300 and group performance materiality is $845 (65%). Subsidiaries A and B are both
full-scope components audited by other auditors.

1. Compute the square-root indication of component materiality for A and B: √(component revenue ÷ group revenue)
   × group overall materiality.
2. Set component materiality for each, rounded down to the nearest $10.
3. Compute component performance materiality for each at 65%, rounded down to the nearest $10.
4. Compute the simple sum and the quadratic combination of (i) the three component materialities, treating the
   parent's as the group figure, and (ii) the three design thresholds.
5. Express each simple sum and each quadratic combination as a percentage of group overall materiality, and state
   whether the aggregation check passes.

### Exercise 3-4

**[Intermediate]** AtlasFlow's NRR cohort denominator at December 31, 2024 is $132,000 and the metric is disclosed
to the nearest whole percentage point. For each of the following draft cohort ARR figures at December 31, 2025,
compute (i) NRR to three decimal places, (ii) NRR as it would be disclosed, (iii) the minimum overstatement that
would raise the disclosed figure by one percentage point, and (iv) the minimum understatement that would lower it
by one percentage point. Then state which of the eight amounts in (iii) and (iv) are below the clearly trivial
threshold of $72.

- (a) $147,048
- (b) $148,000
- (c) $145,900
- (d) $151,140

### Exercise 3-5

**[Intermediate]** Grace Lindqvist receives the following challenge from the engagement quality reviewer: "FY2025
is the first year AtlasFlow's internal control over financial reporting is audited; the July 2025 internal audit
readiness assessment identified fourteen gaps; the CFO has been in post four months; the VP of Revenue Accounting
has been on a performance plan since March; and two revenue accountants resigned in Q2. In those circumstances I
do not see how overall materiality of $1,450 — the very top of the revenue range — is supportable. I would expect
$1,150." Write a conclusion of 150 to 250 words responding to the challenge. State your conclusion, the
reasoning, the authoritative hook, and what would change your answer.

### Exercise 3-6

**[Intermediate]** The group engagement team performs specified procedures over AtlasFlow Pty Ltd (Australia) to a
design threshold of $420. Those procedures identify a $780 overstatement of Australian professional services
revenue caused by an error in the percentage-of-completion input measure on three engagements. Group overall
materiality is $1,450, group performance materiality is $940, and the clearly trivial threshold is $72. Answer,
with reasons:

1. Is the misstatement material to the Australian component?
2. Is it material to the group financial statements?
3. Must it be accumulated on the group summary of audit differences, and against which threshold is it evaluated?
4. Does the fact that $780 exceeds the $420 Australian design threshold change the answer to (2)?
5. What does the $780 tell you that the group team must now do beyond accumulating it?

### Exercise 3-7

**[Advanced]** *Hypothetically*, assume that on February 5, 2026 — after all fieldwork was complete and the
summary of audit differences had been populated — the engagement team discovered that $6,300 of Q4 subscription
revenue had been recognized on contracts that fail the enforceability criterion, so that FY2025 revenue is
$141,900 rather than $148,200. Overall materiality would be recomputed at 1% of $141,900 = $1,419, rounded down to
$1,400; performance materiality at $910; the clearly trivial threshold at $70. List, in the order you would
perform them, the eight things the engagement team must now do, and for each state what evidence would demonstrate
completion. Include at least one item that is a risk-assessment consequence rather than a recomputation.

### Exercise 3-8

**[Intermediate]** Draft the paragraph of WP 1300-01 that records the consideration and rejection of ARR as the
materiality benchmark. Write 130 to 200 words. Your paragraph must name the benchmark considered, state the
amount it would have produced, give at least three distinct reasons for rejection, and record who was consulted.

### Exercise 3-9

**[Advanced]** During the search for related-party transactions the team identifies a payment of $138 made in
August 2025 to Ashford Advisory LLC, a consulting firm wholly owned by the spouse of Dr. Helen Ashford, the audit
committee chair and designated financial expert. The payment was for "board effectiveness advisory services," was
approved by the CEO, was recorded in account 6300, and is not disclosed in the draft proxy statement or in the
related-party footnote. Specific materiality is $150; the Regulation S-K Item 404(a) threshold is $120; the
clearly trivial threshold is $72; overall materiality is $1,450. Draft the qualitative materiality evaluation and
conclusion for the workpaper, 180 to 260 words, ending with a clear conclusion on whether the item is material and
what you require of management.

### Exercise 3-10

**[Advanced]** The extract below is a junior staff member's first draft of the FY2025 materiality workpaper.
Identify every defect, state why each is a defect, and give the correct treatment.

```text
WP 1300-01 (DRAFT)  AtlasFlow, Inc. — FY2025 Materiality

Benchmark:              Annual recurring revenue, $172,000 (the metric users follow)
Percentage:             1.0%
Computed:               $1,720
Overall materiality:    $1,750  (rounded up for ease of use)
Performance materiality: $1,400 (80% of overall; management's controls are
                        expected to be effective)
Clearly trivial:        $175 (10% of overall). Differences below $175 will not
                        be investigated.
Specific materiality:   Not required — AtlasFlow has no related-party
                        transactions.
Component materiality:  UK $1,450; Australia $600.
Tolerable misstatement: To be determined for each population at the time the
                        sample is selected.
Revision:               Materiality was revised from $1,450 to $1,750 on
                        February 12, 2026 after the summary of audit differences
                        showed an aggregate uncorrected effect of $1,510.
```

### Exercise 3-11

**[Intermediate]** *This exercise spans Chapter 2 and Chapter 3.* Chapter 2's FY2025 risk assessment matrix
records the following assertion-level conclusions for the revenue cycle: Core subscription revenue — occurrence
and cut-off: **significant risk** (presumed fraud risk in revenue plus the December 24–31 bookings
concentration); Insight subscription revenue — accuracy: **significant risk** (thin standalone selling price
evidence); usage overage revenue — completeness: higher but not significant; professional services revenue —
accuracy: higher but not significant. Performance materiality is $940.

1. Determine tolerable misstatement for each of the four populations, applying the convention that a significant
   risk or the presence of more than one sampling procedure over the same population reduces tolerable
   misstatement to 75% of performance materiality.
2. Compute the indicated unstratified monetary-unit sample size for each population at a reliability factor of
   3.0, using FY2025 amounts of $104,900, $26,700, $4,200, and $12,400.
3. State the total indicated sample items, and explain in two or three sentences why the actual FY2025 revenue
   testing did not involve anything like that number of items.
4. Explain how the assessed risk affects the threshold, and how it separately affects the *nature* of the
   procedures in a way that the threshold does not capture.

### Exercise 3-12

**[Advanced]** The daily Stripe-to-NetSuite reconciliation (interface I-4) was not performed at all during the 92
days of Q3 2025; the control owner was on leave and no backup was assigned. Stripe self-serve revenue for FY2025
was $6,100, earned approximately evenly across the year. Overall materiality is $1,450 and interim materiality is
$320 for Q1, $360 for Q2, $380 for Q3, and $400 for Q4.

1. Compute the amount of self-serve revenue that flowed through the unreconciled interface during Q3 2025.
2. Express that amount as a multiple of Q3 interim materiality and of annual overall materiality.
3. Compute the number of days of unreconciled Stripe activity that would be required to reach annual overall
   materiality.
4. State the potential magnitude of the deficiency and explain why it is not $0 even though no misstatement was
   identified.
5. Conclude on whether the deficiency meets the AS 2201 definition of a material weakness on magnitude grounds
   alone, and state what additional determination is required before that conclusion can be reached.

## Solutions to Practice Exercises

### Solution 3-1

1. Gross profit = $132,600 − $35,900 = **$96,700**. Total expenses = $35,900 + $123,000 = **$158,900**.
2. Revenue: 0.5% × 132,600 = $663.0; 1.0% = $1,326.0. Gross profit: 1.0% × 96,700 = $967.0; 2.0% = $1,934.0.
   Total expenses: 0.5% × 158,900 = $794.5; 1.0% = $1,589.0. Total assets: 0.5% × 291,400 = $1,457.0; 1.0% =
   $2,914.0.
3. Intersection low = the highest floor = max($663.0, $967.0, $794.5) = **$967**. Intersection high = the lowest
   ceiling = min($1,326.0, $1,934.0, $1,589.0) = **$1,326**. Defensible range **$967 to $1,326**. Note that total
   assets again fails to overlap: its floor of $1,457 is above the revenue ceiling of $1,326, for the same reason
   as in §3.3 — the balance sheet is dominated by treasury assets.
4. 1.0% × $132,600 = $1,326.0, rounded down to the nearest $50 = **$1,300**. Percentile within the range:
   ($1,300 − $967) ÷ ($1,326 − $967) = $333 ÷ $359 = 92.8%, so the **93rd percentile**.
5. $1,450 ÷ $132,600 = **1.094%**, which is above the 1.0% ceiling of the revenue range. It is 1.500% of gross
   profit (inside the range), 0.913% of total expenses (inside), and 0.498% of total assets (marginally below the
   floor). Conclusion: $1,450 would **not** be defensible on the same rationale, because the documented primary
   benchmark is revenue and $1,450 exceeds its ceiling. It could only be supported by making gross profit the
   primary benchmark, which would be a different memorandum requiring a different justification — and one that is
   harder to make, because gross profit is not what AtlasFlow's users lead with.

### Solution 3-2

1. Performance materiality: 60% × $1,300 = $780.0 → **$780**; 65% × $1,300 = $845.0 → **$845**; 70% × $1,300 =
   $910.0 → **$910**.
2. Clearly trivial threshold: 3% × $1,300 = **$39**; 5% = **$65**; 8% = **$104**.
3. Sampling interval = performance materiality ÷ 3.0; sample size = $28,400 ÷ interval, rounded up.

| Performance materiality | Interval | Computed sample size | Sample size used |
| --- | --- | --- | --- |
| 780 | 260.00 | 28,400 ÷ 260.00 = 109.23 | 110 |
| 845 | 281.67 | 28,400 ÷ 281.67 = 100.83 | 101 |
| 910 | 303.33 | 28,400 ÷ 303.33 = 93.63 | 94 |

4. At the 5% threshold of $65: $845 ÷ $65 = **13 items exactly** to reach performance materiality, and $1,300 ÷
   $65 = **20 items exactly** to reach overall materiality. Twenty excluded items reaching overall materiality is
   at the outer edge of defensible; 13 reaching performance materiality is the number that should make the team
   keep the below-threshold log carefully.

### Solution 3-3

1. Subsidiary A: √($29,600 ÷ $132,600) × $1,300 = √0.223228 × $1,300 = 0.472470 × $1,300 = **$614.21**.
   Subsidiary B: √($15,000 ÷ $132,600) × $1,300 = √0.113122 × $1,300 = 0.336336 × $1,300 = **$437.24**.
2. Rounded down to the nearest $10: A = **$610** (46.9% of group overall materiality); B = **$430** (33.1%).
3. Component performance materiality: A = 65% × $610 = $396.50 → **$390**; B = 65% × $430 = $279.50 → **$270**.
4. and 5.

| Measure | Parent | Sub A | Sub B | Simple sum | % of group | Quadratic combination | % of group |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Component materiality | 1,300 | 610 | 430 | 2,340 | 180.0% | 1,499 | 115.3% |
| Design threshold | 845 | 390 | 270 | 1,505 | 115.8% | 969 | 74.5% |

Quadratic arithmetic: √(1,300² + 610² + 430²) = √(1,690,000 + 372,100 + 184,900) = √2,247,000 = 1,499.0.
√(845² + 390² + 270²) = √(714,025 + 152,100 + 72,900) = √939,025 = 969.0.

**The aggregation check passes.** The quadratic combination of the three design thresholds is $969, being 74.5%
of group overall materiality of $1,300 — comfortably inside. The simple sum of $1,505 exceeds group materiality
by 15.8%, which is the expected result and requires the documented judgment that all three components harbouring
undetected misstatement at full design threshold in the same direction simultaneously is remote. The simple sum
of component materialities at 180.0% of the group figure is likewise expected and is not a defect.

### Solution 3-4

One percentage point of NRR equals $1,320 of cohort ARR (1% × $132,000) and the rounding boundary for a disclosed
integer of X% is at X.5%, or $132,000 × (X + 0.5) ÷ 100. Amounts are the minimum change needed to alter the
disclosed integer, assuming round-half-up.

| Draft cohort ARR | NRR computed | Disclosed | Upper boundary (cohort ARR) | Minimum overstatement to add 1 pp | Lower boundary (cohort ARR) | Minimum understatement to lose 1 pp |
| --- | --- | --- | --- | --- | --- | --- |
| (a) 147,048 | 111.400% | 111% | 147,180 (111.5%) | **132** | 145,860 (110.5%) | **1,189** |
| (b) 148,000 | 112.121% | 112% | 148,500 (112.5%) | **500** | 147,180 (111.5%) | **821** |
| (c) 145,900 | 110.530% | 111% | 147,180 (111.5%) | **1,280** | 145,860 (110.5%) | **41** |
| (d) 151,140 | 114.500% | 115% | 152,460 (115.5%) | **1,320** | 151,140 (114.5%) | **1** |

Two of the eight amounts are below the clearly trivial threshold of $72: case (c)'s understatement of **$41** and
case (d)'s understatement of **$1**. Case (d) is the extreme illustration — the draft figure sits exactly on the
rounding boundary, so any understatement at all changes the disclosed metric from 115% to 114%. Note also the
asymmetry within each case: at (a) it takes $132 to move the metric up and $1,189 to move it down, so the
metric's exposure to error is entirely direction-dependent, and an auditor who wants to know whether a metric is
fragile must compute both boundaries rather than reasoning from the metric's level.

### Solution 3-5

**Conclusion.** Overall materiality of $1,450 is appropriate and the reviewer's proposed $1,150 conflates two
distinct judgments.

**Reasoning.** Overall materiality answers a question about users: how large a misstatement of AtlasFlow's FY2025
financial statements could reasonably be expected to influence a reasonable investor's decisions. That question
has the same answer whether the company's controls are excellent or defective. Investors do not become more
sensitive to a $1,200 error because the CFO is four months into the role. Every fact the reviewer cites — the
first-year ICFR audit, the fourteen readiness gaps, the turnover in revenue accounting — bears on the
*likelihood that a misstatement exists and is not detected*, which is exactly what performance materiality
governs. Brightline responded to those facts by setting the haircut at 65% rather than the 75% it applies on
lower-risk engagements, which increases the indicated receivable sample from 107 items to 124 and produces
proportionate increases across twenty other populations. Addressing the same facts a second time through overall
materiality would double-count them and would also understate the Chapter 19 evaluation threshold, so that a
$1,300 aggregate misstatement would be reported to the audit committee as material when it is not.

**Authoritative hook.** AS 2105 and AU-C 320 both frame overall materiality by reference to the needs of users of
the financial statements; AU-C 320.09 frames performance materiality by reference to reducing the probability
that aggregate undetected and uncorrected misstatement exceeds overall materiality. The division of labour is in
the standards, not merely in firm methodology.

**What would change the answer.** A restatement in FY2022–FY2024; a covenant within 10% of breach; a material
weakness identified before the substantive plan was finalized that the team knew would not be remediated; or
documented evidence of bias in prior-period estimates. AtlasFlow has none of these at the planning date.

### Solution 3-6

1. **Not a meaningful question as posed.** The $420 is a *design threshold* for the group team's specified
   procedures, not a materiality determined for users of Australian financial statements — AtlasFlow Pty Ltd does
   not issue statements to external users. If it did, its own overall materiality would be roughly 1% of its
   $12,500 revenue, or $125, and $780 would plainly be material to it. But that is not the question the group
   audit is asking.
2. **Not material to the group on its own.** $780 is 53.8% of overall materiality of $1,450 and 83.0% of
   performance materiality of $940.
3. **Yes, it must be accumulated**, because $780 far exceeds the clearly trivial threshold of $72. It is
   evaluated against **group overall materiality of $1,450**, individually and in the aggregate with all other
   identified misstatements, under AS 2810 and AU-C 450. It is *not* evaluated against $420 or against $940 —
   those are design thresholds.
4. **No.** That $780 exceeds $420 tells you only that the procedures were designed sensitively enough to find it,
   which is what the threshold is for. A design threshold is not a materiality level for evaluation.
5. Five things. (i) At 83.0% of performance materiality, this single item consumes nearly all the room the
   haircut was designed to create; the team must reassess whether the aggregate of this item plus other
   identified and undetected misstatements can be kept below $1,450, and Exhibit 3-7's arithmetic says it is
   close. (ii) The cause — an error in the percentage-of-completion input measure — is not Australia-specific.
   Professional services revenue of $12,400 is recognized on the same basis in the US and UK, and the continuing
   case records uncorrected misstatement U-4 as a $95 professional services input estimate error. The team must
   extend testing to the other entities and quantify the total. (iii) The assessed risk of material misstatement
   for professional services accuracy must be reconsidered upward, with a consequent change to the nature and
   extent of procedures. (iv) The related control must be evaluated as a deficiency, with potential magnitude
   computed against annual materiality of $1,450 and against Q3 and Q4 interim materiality of $380 and $400 —
   where $780 is more than double either. (v) The team must request correction; a known, precisely measurable
   $780 misstatement left uncorrected against a $940 performance materiality is a difficult position to defend
   to an audit committee.

### Solution 3-7

In order, with the evidence of completion:

1. **Quantify the misstatement precisely and determine its nature.** Recompute the revenue effect contract by
   contract rather than relying on the $6,300 estimate, and determine whether the failure is one of
   enforceability, of cut-off, or of contract existence — the three have different implications. *Evidence:* a
   contract-level schedule agreeing to $6,300 and a conclusion memorandum on the ASC 606-10-25 criterion that
   fails.
2. **Reassess risk before recomputing anything.** A $6,300 revenue misstatement in the Q4 population, on facts
   that include 41% of Q4 ACV signed December 24–31 and a January 2026 whistleblower allegation that December
   deals were papered after the fact, is a fraud risk indicator. Reconvene the engagement team discussion,
   reconsider the assessed risk of material misstatement, expand the December population to 100% examination
   using evidence outside management's control, and consider whether the misstatement is intentional. *Evidence:*
   updated risk assessment, discussion minutes, and the AS 2401 documentation of the response. This is the
   risk-assessment consequence the exercise requires, and it comes before the arithmetic because it may change
   what the arithmetic is for.
3. **Revise and re-document the materiality set.** Overall materiality $1,400 (1% of $141,900 = $1,419, rounded
   down); performance materiality $910; clearly trivial threshold $70; specific materiality unchanged at $150;
   UK component materiality $560 (40%) with component performance materiality $364 → $360; Australia $400.
   *Evidence:* a revised WP 1300-01 recording the date, the information that caused the revision, and the
   aggregate then accumulated.
4. **Recompute interim materiality and redo the ICFR deficiency evaluation.** Q4 revenue becomes $34,490
   ($40,790 − $6,300), so Q4 interim materiality becomes $340 (1% of $34,490 = $344.9, rounded down). Every
   deficiency magnitude assessment must be recomputed against $1,400 annually and against the revised quarterly
   figures. *Evidence:* a revised deficiency log showing both comparisons for every item.
5. **Extend completed tests of details.** Every test designed to a tolerable misstatement derived from $940 must
   be evaluated at $910 and extended where the sample size is now insufficient — for the $38,600 receivable
   population, from 124 items to 128. *Evidence:* extension schedules identifying the incremental items, their
   selection basis, and their results.
6. **Recompute every substantive analytical procedure's investigation threshold**, which is a function of
   performance materiality, and reinvestigate differences that now exceed the lower threshold. *Evidence:*
   revised analytic workpapers with the recomputed thresholds and the additional investigation.
7. **Recover the below-threshold log and reconsider items between $70 and $72.** *Evidence:* the annotated log
   with a disposition for every affected item, and any resulting additions to the summary of audit differences.
8. **Re-communicate component thresholds and re-evaluate the summary of audit differences and the required
   communications.** Issue revised group instructions to Brightline UK LLP, obtain its assessment of whether
   completed work must be extended, re-evaluate the accumulated aggregate against $1,400, and update the AS 1301
   audit committee communication and the engagement quality reviewer's file. *Evidence:* the revised instructions
   and response, the revised summary of audit differences, and the dated communication.

### Solution 3-8

Model language, 176 words:

```text
Benchmark considered and rejected — annual recurring revenue (ARR). We considered
whether ARR of $172,000 at December 31, 2025 is an appropriate benchmark, on the
basis that ARR is the measure emphasised in Item 7, in the Company's earnings
materials, and in sell-side models. One percent of ARR would have produced overall
materiality of $1,720, compared with $1,482 on total revenue — a threshold 16.1%
higher. We rejected ARR for four reasons. First, materiality under AS 2105 is
materiality for the financial statements, and ARR is not a financial statement
measure; it is other information within the scope of AS 2710. Second, ARR is
defined by management and the definition is not fixed by the reporting framework.
Third, ARR is computed in the Snowflake RevOps datamart, which was not reconciled
to the general ledger for the first three quarters of FY2025 (deficiency W-11), so
the benchmark would be less reliable than the population it governs. Fourth, ARR
is the measure on which the CEO's performance stock units vest, so using it would
allow the audit threshold to rise with the metric the audit is designed to test.
Consulted: P. Chandrasekhar (national office), January 12, 2026. Concurred.
```

A weaker but defensible variant states only the first reason. The reason to include all four is that reason one
alone invites the response "then use ARR as a corroborating benchmark," which reasons three and four foreclose.

### Solution 3-9

Model language, 243 words:

```text
Qualitative materiality evaluation — Ashford Advisory LLC, $138.

The August 2025 payment of $138 to Ashford Advisory LLC is 9.5% of overall
materiality ($1,450), 14.7% of performance materiality ($940), and 92.0% of
specific materiality for related-party matters ($150). On amount alone it is
immaterial to the financial statements taken as a whole.

We conclude the item is nonetheless material, for four reasons. First, Ashford
Advisory LLC is wholly owned by the spouse of the audit committee chair, who is
also the designated financial expert; the counterparty is therefore a related
person under Regulation S-K Item 404(a), and $138 exceeds the $120 Item 404(a)
threshold at which the SEC has determined a reasonable investor's interest
attaches. Second, the disclosure's purpose is to permit users to assess the
independence of the director who chairs the committee that oversees this audit;
the decision a user would make differently is not an economic estimate but an
assessment of governance, for which the amount is close to irrelevant. Third, the
payment was approved by the CEO rather than by the audit committee or the board,
so the item also evidences a control matter. Fourth, the service described —
"board effectiveness advisory services" — is of a nature that makes the absence of
disclosure conspicuous rather than technical.

We require management to (a) disclose the transaction in the related-party
footnote and in the Item 404(a) proxy disclosure, (b) provide the audit
committee's ratification or an explanation of its absence, and (c) complete a
targeted search of the vendor master file for other entities affiliated with
directors and executive officers. We will not accept a conclusion that the amount
is below overall materiality as a basis for omission.
```

An alternative defensible position — that a single $138 payment below specific materiality may be aggregated with
other related-party items and evaluated at year end — is weaker here for one reason: the related-party
*disclosure* requirement is not a measurement matter subject to aggregation, and Item 404(a) sets a threshold that
the item exceeds on its own.

### Solution 3-10

Twelve defects.

| # | Defect | Why it is a defect | Correct treatment |
| --- | --- | --- | --- |
| 1 | Benchmark is ARR | ARR is not a financial statement measure; it is management-defined, computed in an unreconciled datamart (W-11), and forward-looking (Exhibit 3-6) | Total revenue of $148,200 |
| 2 | The threshold it produces | 1% of ARR is $1,720 against 1% of revenue of $1,482 — 16.1% higher, i.e. less audit work, derived from the metric management is compensated on | $1,482 before rounding |
| 3 | Rounded **up** to $1,750 | Rounding must never increase the threshold; here it adds a further 1.7% | Round down to the nearest $50: $1,450 |
| 4 | Performance materiality at 80% | Outside the 50%–75% band without support, and the haircut is the wrong place to reflect expected control effectiveness — control reliance affects the extent of substantive testing, not the aggregation-risk haircut | 65% × $1,450 = $942.5 → $940 |
| 5 | Rationale "management's controls are expected to be effective" | FY2025 is the first ICFR audit; 14 gaps were identified in July 2025. An expectation about untested controls cannot support a design threshold, and in any event the eight factors in Exhibit 3-8 point the other way | Document the ten-factor assessment |
| 6 | Clearly trivial threshold at 10% | Ten excluded items would equal overall materiality, so the threshold is not "clearly trivial" | 5% × $1,450 = $72.5 → $72 |
| 7 | "Differences below $175 will not be investigated" | Conflates accumulation with investigation and scoping. An unexplained difference of any amount is a scope matter | State expressly that the threshold governs accumulation only |
| 8 | "Specific materiality not required — no related-party transactions" | The auditor cannot assert the absence of related-party transactions before performing procedures to identify them; and specific materiality also applies to executive compensation, contingency, and liquidity disclosures | Specific materiality $150, plus the $120 Item 404(a) completeness threshold |
| 9 | UK component materiality of $1,450 | AU-C 600 requires component materiality to be **lower** than group materiality; $1,450 equals it | $580, being 40% of group, with component performance materiality of $380 |
| 10 | Australia at $600 | 41.4% of group, above the $421 square-root indication, with no basis stated, for a component subject only to specified procedures | $420 |
| 11 | "Tolerable misstatement to be determined at the time the sample is selected" | Tolerable misstatement must be set population by population *before* selection; setting it at or after selection is indefensible | Exhibit 3-17, dated before selection |
| 12 | Revision on February 12, 2026 raising materiality after the summary of audit differences showed $1,510 | AU-C 320.12 permits revision only in response to information that would have changed the initial determination. Nothing about revenue changed; the increase came from re-benchmarking and rounding up, and its effect is to make a $1,510 aggregate pass. The sequence alone destroys the file's credibility | No revision on these facts; the January 14, 2026 revision from $1,400 to $1,450 on actual revenue is the only supportable one |

The extract also omits every documentation element AU-C 320.14 requires beyond the amounts themselves: the
factors considered, the benchmarks rejected and the amounts they produced, the component aggregation check, and
interim materiality for the ICFR audit.

### Solution 3-11

1. Tolerable misstatement: Core subscription **$705** (significant risk); Insight subscription **$705**
   (significant risk); usage overage **$940**; professional services **$940**. Both $705 figures are 75% of the
   $940 performance materiality.
2. Sampling interval = tolerable misstatement ÷ 3.0, so $235.00 where tolerable misstatement is $705 and $313.33
   where it is $940.

| Population | FY2025 amount | Tolerable misstatement | Interval | Computed | Sample size |
| --- | --- | --- | --- | --- | --- |
| Core subscription revenue | 104,900 | 705 | 235.00 | 446.4 | 447 |
| Insight subscription revenue | 26,700 | 705 | 235.00 | 113.6 | 114 |
| Usage overage revenue | 4,200 | 940 | 313.33 | 13.4 | 14 |
| Professional services revenue | 12,400 | 940 | 313.33 | 39.6 | 40 |
| **Total** | **148,200** | | | | **615** |

3. **615 indicated items**, and the actual FY2025 revenue testing involved a small fraction of that, for four
   reasons: the unstratified monetary-unit formula is an upper bound that assumes no other evidence exists;
   individually significant contracts are examined at 100% and only the residual population is sampled;
   substantial parts of the population are recomputed in full from contract data rather than sampled (Chapter 5,
   §5.10) or covered by a full-population analytic (Chapter 18, §18.7); and effective tests of controls, where
   supported by effective ITGCs, permit a reduction in the extent of substantive testing.
4. The threshold effect of assessed risk is purely arithmetic: $705 instead of $940 raises the indicated Core
   sample from 335 items to 447. The **nature** effect is categorically different and the threshold does not
   capture any of it. For a significant risk, AS 2301 requires substantive procedures specifically responsive to
   the risk, including tests of details, and the auditor may not respond with controls reliance and analytical
   procedures alone. The presumed fraud risk in revenue additionally requires an element of unpredictability, the
   use of evidence outside management's control (DocuSign completion certificates and platform provisioning logs
   rather than Salesforce date fields), inquiry directed at side agreements, and consideration of whether
   identified misstatements are intentional. None of that follows from the number $705, which is why a file that
   documents only a lower threshold as its response to a significant risk has not responded to it. Arithmetic
   check on the comparison: $104,900 ÷ ($940 ÷ 3.0) = $104,900 ÷ $313.33 = 334.8 → 335 items.

### Solution 3-12

1. Self-serve revenue flowing through the unreconciled interface in Q3 2025 = $6,100 × 92 ÷ 365 = $561,200 ÷ 365
   = **$1,537.5**.
2. $1,537.5 ÷ $380 = **4.05 times Q3 interim materiality**. $1,537.5 ÷ $1,450 = **1.06 times annual overall
   materiality**.
3. Days required to reach annual overall materiality = $1,450 × 365 ÷ $6,100 = $529,250 ÷ $6,100 = 86.8 →
   **87 days**.
4. **Potential magnitude is $1,537.5.** It is not $0 because the ICFR audit measures the misstatement that *could*
   occur, not the one that did. The reconciliation is the control that would detect a difference between what
   Stripe collected and what the I-4 Lambda job posted to NetSuite; with the control not operating for 92 days,
   the maximum amount by which self-serve revenue and cash for the period could be misstated is bounded by the
   amount processed in the period. The absence of an identified misstatement is evidence about likelihood and
   about the effect of other controls; it is not evidence about magnitude. Note also that the I-4 job is in-house
   code with no documented change approval for two FY2025 modifications (W-7), which is directly relevant: the
   mechanism by which a misstatement could arise is not hypothetical.
5. **The magnitude element is met.** $1,537.5 exceeds Q3 interim materiality of $380 by 4.05 times and exceeds
   annual overall materiality of $1,450 by 6.0%, so a misstatement of material magnitude could have occurred. The
   additional determination required is **likelihood**: whether there is a *reasonable possibility* — more than
   remote — that a misstatement of that magnitude would not have been prevented or detected on a timely basis.
   That requires identifying and testing any compensating controls: the PagerDuty failure alerting on the I-4
   job, the monthly Stripe settlement-to-general-ledger reconciliation performed during the close, and the
   analytical review of self-serve revenue. A compensating control counts only if it operates at a level of
   precision sufficient to detect a misstatement of $1,538 and only if the auditor tests it; management's
   assertion that it exists is not sufficient. Chapter 14, §14.13 owns the compensating-control requirements, and
   Chapter 14, §14.11 owns the aggregation of this deficiency with W-7.

## Review Questions

**RQ 3-1.** State the question that overall materiality answers and the different question that performance
materiality answers.

**RQ 3-2.** Why did Brightline reject pre-tax income as the FY2025 benchmark, and what arithmetic supports the
rejection?

**RQ 3-3.** Name the four benchmarks Brightline computed for FY2025 and state the amount each produced at the
illustrated percentage.

**RQ 3-4.** State the single strongest argument against using annual recurring revenue as a materiality
benchmark, and state the argument that is second strongest.

**RQ 3-5.** Define aggregation risk and explain, with a number, why it makes a haircut necessary.

**RQ 3-6.** Distinguish performance materiality from tolerable misstatement. When would the two differ for a
particular population?

**RQ 3-7.** State what the clearly trivial threshold governs and three things it does not govern.

**RQ 3-8.** When does AS 2105 require the auditor to determine a materiality level lower than overall materiality
for a particular item, and give two AtlasFlow examples.

**RQ 3-9.** Explain in three sentences why the sum of AtlasFlow's component materialities is 169% of group
overall materiality and why that is not an error.

**RQ 3-10.** Under what circumstance does AU-C 320 require materiality to be revised during the engagement?

**RQ 3-11.** Why is a downward revision of materiality substantially harder to implement than an upward one, and
what single piece of documentation determines whether it is possible at all?

**RQ 3-12.** List five of the qualitative considerations enumerated in SAB 99.

**RQ 3-13.** How does the AS 2201 definition of a material weakness import a threshold lower than annual
materiality, and what is AtlasFlow's Q4 FY2025 figure?

**RQ 3-14.** In the ICFR audit, is a deficiency's magnitude measured by the misstatement that occurred or by the
one that could occur? Illustrate with the order-form dating control.

**RQ 3-15.** What is the auditor's responsibility with respect to the ARR and NRR figures in AtlasFlow's Form
10-K, and what is it not?

**RQ 3-16.** Identify three substantive differences between the AICPA and PCAOB frameworks as they bear on
materiality.

**RQ 3-17.** Why should every rounding convention in a materiality memorandum round downward?

**RQ 3-18.** What must the audit documentation contain regarding materiality under AU-C 320.14?

## Answers to Review Questions

**RQ 3-1.** Overall materiality answers a question about users: how large a misstatement of the financial
statements could reasonably be expected to influence the decisions of a reasonable investor in the entity.
Performance materiality answers a question about the auditor's procedures: how low the design threshold for each
individual population must be set so that the probability of the aggregate of undetected and uncorrected
misstatements exceeding overall materiality is appropriately low. The first is a judgment about investors and is
unaffected by the client's controls; the second is a judgment about risk and aggregation and is affected by
almost nothing else.

**RQ 3-2.** AtlasFlow reported pre-tax losses in each of FY2023–FY2025, and a loss is the residual of two large
numbers, so the benchmark moves in ways unrelated to the scale of the entity. Five percent of the loss produced
$1,078 for FY2023, $905 for FY2024, and $1,043 for FY2025 — a 16.1% fall in a year in which revenue grew 29.9%,
followed by a 15.2% rise in a year in which revenue growth decelerated to 24.6%. An auditor using it would have
done more work in the faster-growing year for no reason connected to risk.

**RQ 3-3.** Total revenue of $148,200 at 1.00% gives $1,482; gross profit of $109,260 at 1.30% gives $1,420;
total assets of $317,900 at 0.45% gives $1,431; and total expenses of $172,440 at 0.85% gives $1,466. The four
amounts span $62, or 4.2% of their mean of $1,450, and that convergence is the documented basis for the selected
figure.

**RQ 3-4.** The strongest argument is that materiality under AS 2105 and AU-C 320 is materiality for the
financial statements, and ARR is not in them — it is other information under AS 2710. The second strongest is
that ARR exceeds revenue by 16.1%, so using it would *raise* the auditor's threshold, and therefore reduce audit
effort, in proportion to management's success in inflating the metric on which management is compensated and
which the audit is designed to test.

**RQ 3-5.** Aggregation risk is the risk that misstatements that are individually below overall materiality sum
to more than overall materiality. Exhibit 3-7 illustrates it: nine populations, none carrying an undetected
misstatement above $240, sum to $1,365 — 94.1% of the $1,450 threshold. Because the audit tests twenty-one
populations rather than one, a design threshold equal to overall materiality would leave the aggregate
uncontrolled.

**RQ 3-6.** Performance materiality is an entity-level amount, determined once, that expresses the haircut
between overall materiality and the design threshold. Tolerable misstatement is a procedure-level amount,
determined separately for each population subjected to a test of details, and never exceeds performance
materiality. The two differ when more than one sampling procedure addresses the same population, so that
undetected misstatements aggregate within it, or when the population is subject to a significant risk — for
AtlasFlow, Core subscription revenue carries tolerable misstatement of $705 against performance materiality of
$940.

**RQ 3-7.** It governs whether an identified and quantified misstatement is accumulated on the summary of audit
differences. It does not govern the scoping of populations or accounts; it does not govern whether an unexplained
difference is investigated; and it does not apply transaction by transaction — the unit of analysis is the
aggregated misstatement arising from a single root cause across the population. It also does not apply at all to
an item that is qualitatively significant.

**RQ 3-8.** When, in the specific circumstances of the entity, misstatements of amounts less than overall
materiality could reasonably be expected to influence users' judgments about a particular class of transactions,
account balance, or disclosure. For AtlasFlow, related-party transactions and executive compensation disclosures
carry specific materiality of $150, and related-person transactions are tested for completeness at the $120
Regulation S-K Item 404(a) threshold.

**RQ 3-9.** Component materiality is a design threshold below which the component auditor's procedures are
permitted to be insensitive; it is not a budget of permitted error that must add to a group total. Allocating
$1,450 so that the components summed to it would produce UK and Australian thresholds of $257 and $122, which is
equivalent to auditing each component to its own stand-alone materiality and would make the thresholds depend on
how many trivial entities the group contains. The correct test is probabilistic and it passes: the quadratic
combination of the three design thresholds is $1,098, or 75.7% of $1,450.

**RQ 3-10.** When the auditor becomes aware, during the audit, of information that would have caused the auditor
to determine a different amount initially. For AtlasFlow that information was actual FY2025 revenue of $148,200
against the $144,000 forecast used at planning, and the revision from $1,400 to $1,450 was documented on
January 14, 2026.

**RQ 3-11.** An upward revision leaves completed work sufficient, because it was designed to a stricter
threshold. A downward revision invalidates it: tests of details must be extended, analytical thresholds
recomputed, component instructions reissued, and ICFR deficiency magnitudes reassessed. The single piece of
documentation that determines whether it is possible is the log of items declined as clearly trivial — without it
the team cannot reconsider items now above the lower threshold and therefore cannot demonstrate that the
accumulated total is complete.

**RQ 3-12.** Any five of: whether the misstatement masks a change in earnings or other trends; whether it hides a
failure to meet analysts' expectations; whether it changes a loss into income or vice versa; whether it concerns a
segment or other portion of the business identified as playing a significant role in operations or profitability;
whether it affects compliance with regulatory requirements; whether it affects compliance with loan covenants or
other contractual requirements; whether it has the effect of increasing management's compensation; and whether it
involves concealment of an unlawful transaction.

**RQ 3-13.** AS 2201 defines a material weakness as a deficiency, or combination of deficiencies, such that
there is a reasonable possibility that a material misstatement of the company's **annual or interim** financial
statements will not be prevented or detected on a timely basis. Because interim statements are smaller, the
relevant threshold is smaller. AtlasFlow's Q4 FY2025 interim materiality is $400, being 1% of Q4 revenue of
$40,790 rounded down — 27.6% of annual overall materiality.

**RQ 3-14.** By the misstatement that could occur. On the order-form dating control the misstatement that
occurred was $150 (U-3), which is 10.3% of annual materiality; but the control governs the $25,174 of Q4 ACV
signed between December 24 and 31, 2025, and acceleration of recognition by an average of 8 days produces $552 —
138% of Q4 interim materiality — while 21 days produces $1,448, which is annual overall materiality. The $150 is
evidence about likelihood, not a measure of magnitude.

**RQ 3-15.** ARR and NRR are other information under AS 2710. The auditor reads them and considers whether they
are materially inconsistent with the audited financial statements or with knowledge obtained in the audit, and
whether a material misstatement of the other information exists; if a metric reveals a financial statement
misstatement, that misstatement is accumulated and evaluated. What the auditor does not do is audit the metric,
opine on it, or provide any assurance about it, and the auditor's ICFR opinion does not extend to controls over a
metric that is not derived from the financial reporting process.

**RQ 3-16.** First, AU-C 320 defines and requires *performance materiality*, whereas AS 2105 requires tolerable
misstatement at the account and disclosure level and does not use the term — so it is wrong to write that AS 2105
requires performance materiality. Second, AU-C 600 contains explicit component materiality requirements, whereas
the PCAOB addresses other auditors through AS 2101 as amended and AS 1206 (effective for fiscal years ending on
or after December 15, 2024) and does not codify component materiality as a defined term. Third, AS 2201's
integrated-audit materiality framework, including the annual-or-interim formulation, has no AICPA analogue for a
private company.

**RQ 3-17.** Because every rounding decision either increases or decreases the amount of work, and rounding
upward increases the threshold for the auditor's convenience rather than for any reason connected to users.
Rounding $1,482 up to $1,500 raises the threshold 1.2%, and compounding an upward rounding at the overall and
performance levels raises the design threshold by 2% to 3%, which is a real number of sample items. It also
invites the reviewer's next question, which is what else in the file was rounded favourably.

**RQ 3-18.** The amounts of, and the factors considered in determining, materiality for the financial statements
as a whole; materiality levels for particular classes of transactions, account balances, or disclosures where
applicable; performance materiality; and any revision of any of these as the audit progressed. AS 1215 adds the
general requirement that the documentation support the conclusions reached, which in practice means recording the
benchmarks rejected and the amounts they would have produced.

## Key Definitions

**Aggregation risk.** The risk that misstatements that are individually less than overall materiality combine to
exceed it. It is the reason performance materiality exists and the reason the design threshold for a single
population must be lower than the threshold at which the financial statements as a whole become misleading.

**Annual recurring revenue (ARR).** A management-defined operating metric expressing the annualized value of
committed recurring subscription contracts in effect at a point in time. It is not a GAAP measure, is not
presented in the financial statements, and is not audited. AtlasFlow's ARR at December 31, 2025 was $172.0
million against FY2025 GAAP revenue of $148.2 million.

**Below-threshold log.** A record of identified misstatements that the engagement team declined to accumulate
because they fell below the clearly trivial threshold, showing amount, account, cause, population, date, and the
person who decided. It is firm methodology rather than a professional requirement, and it is what makes a
downward revision of materiality and an aggregation-by-cause analysis possible.

**Benchmark.** The financial statement measure to which a percentage is applied to derive overall materiality.
AS 2105 requires the use of an appropriate benchmark but does not specify one; appropriateness turns on what
users of the specific entity's financial statements are analysing.

**Clearly trivial threshold.** The amount below which an identified misstatement need not be accumulated for
evaluation. AU-C 450 requires accumulation of misstatements "other than those that are clearly trivial," meaning
items of a wholly different order of magnitude from materiality. AtlasFlow's FY2025 threshold was $72, being 5%
of overall materiality.

**Component materiality.** The materiality level determined by the group engagement team for a component whose
financial information is included in the group financial statements, for use in the component auditor's
procedures. It must be lower than group materiality (AU-C 600). AtlasFlow's UK component materiality was $580.

**Component performance materiality.** The haircut applied to component materiality for the purpose of designing
procedures at the component. AtlasFlow's UK figure was $380, being 65% of $580 rounded to the nearest $10.

**Concave allocation.** An allocation method in which the threshold assigned to a component falls as the
component's relative size falls, but falls more slowly than size does — for example, in proportion to the square
root of the component's share of the group benchmark. It is the property that makes the sum of component
materialities exceed the group figure.

**Dollar-based gross retention.** A management-defined operating metric expressing the proportion of a beginning
cohort's ARR retained at the end of the period, counting churn and contraction but excluding expansion.
AtlasFlow's FY2025 figure was 91%, computed as ($132,000 − $4,470 − $7,410) ÷ $132,000.

**Group materiality.** Overall materiality determined for the group financial statements as a whole. For
AtlasFlow, $1,450.

**Interim materiality.** Materiality determined for an interim period rather than for the annual financial
statements. It matters chiefly in the ICFR audit, because AS 2201 defines a material weakness by reference to a
reasonable possibility of material misstatement of the annual **or interim** financial statements. AtlasFlow's
FY2025 quarterly figures were $320, $360, $380, and $400.

**Iron-curtain approach.** An approach to evaluating the effect of prior-period uncorrected misstatements that
measures the cumulative error existing in the balance sheet at the current period end, without regard to the
period in which it arose. Contrast the rollover approach. SAB 108 requires consideration of both.

**Material weakness.** A deficiency, or combination of deficiencies, in internal control over financial reporting
such that there is a reasonable possibility that a material misstatement of the company's annual or interim
financial statements will not be prevented or detected on a timely basis (AS 2201). Chapter 14 owns the severity
framework.

**Materiality.** An entity-specific aspect of relevance: information is material if omitting, misstating, or
obscuring it could reasonably be expected to influence the decisions that the primary users of a specific
reporting entity's general purpose financial statements make on the basis of those statements (FASB Concepts
Statement No. 8, Chapter 3). SAB 99 adopts the same formulation for registrants and adds that a percentage
threshold cannot substitute for a full analysis.

**Net revenue retention (NRR).** A management-defined operating metric equal to end-of-period ARR from a
beginning-of-period customer cohort divided by that cohort's beginning-of-period ARR, so that expansion,
contraction, and churn are all captured. AtlasFlow's FY2025 figure was 112%, computed as $147,840 ÷ $132,000.

**Other information.** Financial and non-financial information, other than the audited financial statements and
the auditor's report, included in a document containing the audited financial statements. The auditor reads it
and considers material inconsistency with the audited statements and with knowledge obtained, but expresses no
opinion on it (AS 2710; AU-C 720). ARR, NRR, and adjusted EBITDA are other information for AtlasFlow.

**Overall materiality.** Also financial statement materiality: the amount of misstatement of the financial
statements taken as a whole that could reasonably be expected to influence a reasonable user's decisions. For
AtlasFlow FY2025, $1,450.

**Performance materiality.** The amount or amounts, less than materiality for the financial statements as a
whole, set by the auditor to reduce to an appropriately low level the probability that the aggregate of
uncorrected and undetected misstatements exceeds materiality for the financial statements as a whole
(AU-C 320.09). For AtlasFlow FY2025, $940.

**Potential magnitude.** In the ICFR audit, the amount of misstatement that could result from a control
deficiency, generally bounded by the recorded amount of the account or the transaction population the control
governs. It is not the amount of any misstatement actually identified.

**Quadratic combination.** The square root of the sum of the squares of a set of thresholds, used as an estimate
of their combined effect on the assumption that the underlying errors are independent and therefore partially
offsetting. For AtlasFlow's three component design thresholds it is $1,098 against a simple sum of $1,740.

**Qualitative materiality factors.** The considerations, enumerated in SAB 99 and reflected in AS 2810 and
AU-C 450, that can make a quantitatively small misstatement material — including masking a trend, converting a
consensus miss into a beat, affecting covenant compliance, increasing management's compensation, concealing an
unlawful transaction, and being intentional.

**Reasonable possibility.** More than remote. The likelihood element of the material weakness and significant
deficiency definitions; the terms "reasonably possible" and "remote" carry the meanings used in ASC 450 for loss
contingencies.

**Remaining performance obligation (RPO).** The aggregate amount of the transaction price allocated to
performance obligations that are unsatisfied or partially unsatisfied at the reporting date, disclosed under
ASC 606-10-50-13. Unlike ARR, RPO is a financial statement disclosure and is audited. AtlasFlow's RPO at
December 31, 2025 was $214.0 million. Chapter 6 owns it.

**Rollover approach.** An approach to evaluating the effect of prior-period uncorrected misstatements that
measures the current-period income statement effect of the error, including the turnaround of prior-period
items. Contrast the iron-curtain approach.

**Sampling interval.** In monetary-unit sampling, tolerable misstatement divided by the reliability factor. It is
the amount of population value represented by each selected sampling unit; the sample size is the population
divided by the interval. Chapter 15 owns the derivation.

**Significant deficiency.** A deficiency, or combination of deficiencies, in internal control over financial
reporting that is less severe than a material weakness yet important enough to merit attention by those
responsible for oversight of the company's financial reporting (AS 2201; AU-C 265 uses an equivalent
formulation). Significant deficiencies must be communicated in writing.

**Specific materiality.** A materiality level lower than overall materiality, determined for a particular class
of transactions, account balance, or disclosure because misstatements of lesser amounts could reasonably be
expected to influence users' judgments about that item. For AtlasFlow FY2025, $150.

**Summary of audit differences.** The schedule on which identified misstatements above the clearly trivial
threshold are accumulated, separated into corrected and uncorrected items, and evaluated individually and in the
aggregate against overall materiality. Chapter 19 owns its preparation and evaluation.

**Tolerable misstatement.** The maximum misstatement the auditor is willing to leave undetected in a particular
population subjected to a test of details. It is determined at the account or disclosure level, never exceeds
performance materiality, and must be set before the sample is selected (AS 2105; AU-C 530).

## Chapter Summary

1. Materiality originates in the financial reporting framework and in the securities laws, not in auditing
   standards; the auditor's thresholds are derived from a user-based concept and are deliberately set below it.
2. AtlasFlow's overall materiality of $1,450 was derived from four converging benchmarks — total revenue at
   1.00% giving $1,482, gross profit at 1.30% giving $1,420, total assets at 0.45% giving $1,431, and total
   expenses at 0.85% giving $1,466 — whose $62 spread is the documented basis for the figure, rather than from a
   single percentage.
3. The defensible range on these facts is $1,093 to $1,482, being the intersection of the revenue, gross profit,
   and total-expense ranges; total assets does not overlap because 47.4% of AtlasFlow's balance sheet is treasury
   assets that no user is analysing and that carry little risk of material misstatement.
4. Pre-tax income, equity, and adjusted EBITDA all fail as benchmarks for AtlasFlow, and each fails for a
   different, statable reason: the loss moves inversely to the scale of the business, equity of $7,100 is a
   residual carrying no information about scale, and adjusted EBITDA of $18,260 is smaller than the $28,700
   stock-based compensation add-back that produces it.
5. ARR fails four tests — it is not a financial statement measure, it is management-defined, it is computed in an
   unreconciled data warehouse, and it describes a forward period — and using it would raise the auditor's
   threshold by 16.1% in proportion to management's success in inflating the metric on which management is
   compensated.
6. Overall materiality is a judgment about users and performance materiality is a judgment about risk; a weak
   control environment belongs in the haircut, not in the benchmark percentage, because investors' sensitivity to
   error does not change with the quality of a client's controls.
7. The 65% haircut to $940 is justified by aggregation risk, which Exhibit 3-7 quantifies: nine populations, none
   carrying an undetected misstatement above $240, sum to $1,365 or 94.1% of overall materiality, and the FY2025
   audit ultimately identified $2,650 of gross misstatement, being 182.8% of overall materiality.
8. The haircut has a price that should be documented: on the $38,600 receivable population alone it costs 44
   additional sample items relative to no haircut and saves 36 relative to a 50% haircut.
9. The clearly trivial threshold of $72 governs accumulation only, applies to the misstatement arising from a
   single cause rather than to individual transactions, and never applies to a qualitatively significant item.
10. Component materiality of $580 for the UK and $420 for Australia was derived from a concave allocation and a
    documented risk overlay, not from pro-rata allocation, which would have produced $257 and $122 — amounts
    equivalent to auditing each component to its own stand-alone materiality.
11. The sum of component materialities is 169% of group overall materiality and this is the expected result; the
    test that matters is the quadratic combination of design thresholds, which at $1,098 is 75.7% of $1,450.
12. Tolerable misstatement is a procedure-level threshold set population by population before selection, and it
    is set at 75% of performance materiality for AtlasFlow's significant-risk revenue populations, raising the
    indicated Core subscription sample from 335 items to 447.
13. Materiality must be revised when information emerges that would have changed the initial determination; an
    upward revision leaves completed work sufficient but must be dated and must not be harvested, while a
    downward revision invalidates completed work and is only implementable if a below-threshold log exists.
14. In the ICFR audit the same $1,450 applies, but magnitude is *potential* rather than actual and the relevant
    threshold is annual **or interim** — so the order-form dating control, whose potential magnitude of $552 on
    the most benign assumption is 138% of Q4 interim materiality of $400, reaches the material weakness
    definition on magnitude grounds even though the misstatement actually identified was $150.
15. A $310 misstatement that is 0.209% of revenue was corrected because it moved a disclosed operating metric
    from 111% to 112%, converted an ARR consensus miss into a beat, and crossed a PSU vesting step — and because
    only $132 of error was required to move the metric at all, no quantitative threshold in the file would have
    caught it.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| SaaS metric vocabulary (ARR, ACV, NRR, GRR, RPO) and the bookings-billings-revenue-cash bridge | Chapter 1, §1.4 | To understand what the metrics in §3.9 measure before deciding how materiality applies to them |
| Group audit scoping — which components are full scope, specified procedures, or analytical only | Chapter 1, §1.9 | The scoping decision that §3.10's numbers attach to |
| Assertion-level risk assessment for the revenue cycle | Chapter 2 | The assessed risks that determine which populations get tolerable misstatement of $705 rather than $940 |
| Order-to-cash cut-off testing and the December 24–31 population | Chapter 4, §4.9 | The population whose potential magnitude drives Exhibit 3-23 |
| Revenue disaggregation disclosure testing | Chapter 4, §4.12 | The disclosure whose materiality is discussed in §3.8, Case 1 |
| Standalone selling price for the Insight module | Chapter 5, §5.7 | The disclosure evaluated in Exhibit 3-13 and the source of the $705 tolerable misstatement |
| RPO recomputation and the deferred revenue roll-forward | Chapter 6 | RPO is an audited disclosure, unlike ARR; §3.9 explains the distinction and Chapter 6 does the work |
| Allowance for credit losses and the $1,780–$2,410 range | Chapter 7 | The source of uncorrected misstatement U-2, evaluated qualitatively in Exhibit 3-20 |
| Stock-based compensation and the PSU probability assessment | Chapter 9, §9.9 | The $893 consequence worked in the Extended Case Study |
| Interface controls, the I-1 error queue, and the Snowflake RevOps datamart | Chapter 12 | The control that failed in the Extended Case Study and the system that produces the metrics in §3.9 |
| Deficiency severity, compensating controls, and aggregation | Chapter 14, §14.11–§14.13 | Where the magnitude arithmetic in §3.14 is converted into a severity conclusion |
| Sampling mechanics, reliability factors, stratification, and projection | Chapter 15, §15.6 | The derivation of every sample size quoted in this chapter |
| Analytical procedure thresholds for investigation | Chapter 18, §18.4 | The other place performance materiality is consumed directly |
| Accumulating and evaluating misstatements; the iron-curtain and rollover approaches | Chapter 19 | Where $1,450 is actually used, and where the $(460) FY2025 aggregate is evaluated |
| Report language, critical audit matters, and the adverse ICFR opinion | Chapter 20 | The consequence of the §3.14 conclusions |

## Further Reading

- PCAOB AS 2105, *Consideration of Materiality in Planning and Performing an Audit*.
- PCAOB AS 2101, *Audit Planning*, including the amendments governing planning and supervision of audits
  involving other auditors, effective for fiscal years ending on or after December 15, 2024.
- PCAOB AS 1206, *Dividing Responsibility for the Audit with Another Accounting Firm*.
- PCAOB AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of
  Financial Statements*, in particular the definitions of material weakness and significant deficiency and the
  discussion of materiality in planning the ICFR audit.
- PCAOB AS 2810, *Evaluating Audit Results*.
- PCAOB AS 2710, *Other Information in Documents Containing Audited Financial Statements*.
- PCAOB AS 1215, *Audit Documentation*.
- AICPA AU-C 320, *Materiality in Planning and Performing an Audit*.
- AICPA AU-C 450, *Evaluation of Misstatements Identified During the Audit*.
- AICPA AU-C 530, *Audit Sampling*.
- AICPA AU-C 600, *Special Considerations — Audits of Group Financial Statements (Including the Work of Component
  Auditors)*.
- AICPA AU-C 720, *The Auditor's Responsibilities Relating to Other Information Included in Annual Reports*.
- SEC Staff Accounting Bulletin No. 99, *Materiality*.
- SEC Staff Accounting Bulletin No. 108, on considering the effects of prior year misstatements.
- SEC Regulation S-K, Item 10(e) (non-GAAP financial measures) and Item 404 (transactions with related persons).
- SEC Regulation G.
- SEC Rule 12b-20 under the Securities Exchange Act of 1934.
- FASB Concepts Statement No. 8, *Conceptual Framework for Financial Reporting*, Chapter 3, *Qualitative
  Characteristics of Useful Financial Information*.
- FASB ASC 606-10-50, *Revenue from Contracts with Customers — Disclosure*.
- The AICPA audit guide covering audit sampling, for the sample-size tables underlying the reliability factors
  used in this chapter.
- The AICPA audit and accounting guide covering revenue recognition, for the disclosure requirements whose
  materiality is assessed in §3.8.








