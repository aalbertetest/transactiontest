# Chapter 5 — Auditing Subscription Revenue

> A subscription contract looks simple: one customer, one platform, one annual fee. The revenue schedule that
> comes out of the subledger is not simple. Between the order form and the general ledger sit five judgments —
> how many performance obligations exist, what each is worth on a standalone basis, how the negotiated
> discount is spread across them, when each begins and ends, and what happens when the contract changes
> mid-term. Get any one of them wrong and the amount and the period are both wrong. AtlasFlow's FY2025
> subscription revenue of $135,800 thousand is the output of 27 configuration rules operating on roughly 3,140
> enterprise contract records; your job in this chapter is to learn how to reproduce that output from the
> contracts themselves and to know what to do when your number and the engine's number disagree.

## Learning Objectives

- **LO 5.1** Identify the performance obligations in a SaaS contract by applying the "capable of being
  distinct" and "distinct within the context of the contract" tests to hosting, support, updates, setup
  activities, implementation, training, and customization.
- **LO 5.2** Explain and apply the series guidance to conclude whether a SaaS subscription is a single
  performance obligation satisfied over time, and document the conclusion.
- **LO 5.3** Compute the standalone selling price of a material right using an expected-value model with an
  explicit breakage assumption, and evaluate whether the right is material.
- **LO 5.4** Distinguish the four standalone selling price (SSP) estimation approaches, state the narrow
  conditions under which the residual approach is permitted, and reject it when it produces an unreasonable
  result.
- **LO 5.5** Evaluate an SSP analysis quantitatively using price bands, quartiles, interquartile range,
  concentration analysis, and a sample-sufficiency computation.
- **LO 5.6** Allocate a transaction price across four performance obligations on a relative-SSP basis to the
  cent-equivalent, and evaluate whether the discount-allocation exception applies.
- **LO 5.7** Classify a contract modification as a separate contract, a prospective modification, or a
  cumulative catch-up, and compute the cumulative catch-up adjustment.
- **LO 5.8** Recompute revenue on a ramped, non-coterminous, multi-element contract from the contract
  document and reconcile the result to a revenue engine's schedule.
- **LO 5.9** Design procedures over the completeness and accuracy of usage data and recompute overage revenue
  against a committed volume.
- **LO 5.10** Distinguish testing a revenue engine's configuration from testing its output, and conclude which
  combination provides sufficient appropriate audit evidence.
- **LO 5.11** Measure a foreign-currency subscription contract at contract inception and explain which
  components of the subsequent currency movement affect earnings.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| FASB ASC | 606-10-25 (identifying performance obligations) | Requires a promised good or service to be accounted for separately only if it is capable of being distinct and is distinct within the context of the contract; treats setup and fulfillment activities that transfer nothing to the customer as non-obligations |
| FASB ASC | 606-10-25-14(b) and 25-15 (the series guidance) | Permits — and where the criteria are met, requires — a series of distinct goods or services that are substantially the same with the same pattern of transfer to be treated as a single performance obligation |
| FASB ASC | 606-10-25-10 through 25-13 (contract modifications) | Sets the three modification outcomes: separate contract, prospective (terminate-and-replace), and cumulative catch-up |
| FASB ASC | 606-10-32 (transaction price and allocation) | Requires allocation on a relative standalone selling price basis; establishes the SSP estimation approaches and the discount-allocation exception at 606-10-32-37; governs variable consideration and its allocation |
| FASB ASC | 606-10-55 (implementation guidance) | Addresses customer options for additional goods or services and material rights, and the right-to-invoice measure of progress for usage-based consideration |
| FASB ASC | 606-10-50 | Requires disaggregated revenue and significant-judgment disclosures, including the judgments used in determining SSP and timing of satisfaction |
| FASB ASC | 340-40 | Costs to obtain a contract; the amortization period is a separate judgment from the ASC 606 contract term (developed in Chapter 10, §10.6) |
| FASB ASC | 830-10 and 830-30 | Measurement of a foreign-currency-denominated transaction at the spot rate on the transaction date; remeasurement of monetary items; translation of a foreign entity's statements |
| PCAOB | AS 2110 | Requires the auditor to obtain an understanding of the company's selection and application of accounting principles, including revenue, and to identify risks of material misstatement (RMM) at the assertion level |
| PCAOB | AS 2301 | Requires the nature, timing, and extent of further audit procedures to respond to the assessed RMM; addresses testing controls that depend on IT |
| PCAOB | AS 2305 | Governs substantive analytical procedures, including the precision of the expectation and the investigation of differences |
| PCAOB | AS 2501 (as amended, effective for fiscal years ending on or after December 15, 2020) | Governs auditing accounting estimates, including fair value; requires evaluating the method, data, and significant assumptions, and permits testing management's process, developing an independent expectation, or evaluating subsequent events |
| PCAOB | AS 1105 | Sets the sufficiency and appropriateness framework for audit evidence, including the reliability of information produced by the entity (IPE) |
| PCAOB | AS 2401 | Establishes the presumption that improper revenue recognition is a fraud risk and requires responsive procedures |
| PCAOB | AS 2601 | Governs the auditor's consideration of the company's use of a service organization, relevant to the Zuora SOC 1 reports |
| AICPA | AU-C 315 (as amended by SAS 145, effective for periods ending on or after December 15, 2023) | The AICPA analogue to AS 2110; requires inherent risk and control risk to be assessed separately and adds an explicit "stand-back" evaluation |
| AICPA | AU-C 330 | The AICPA analogue to AS 2301 |
| AICPA | AU-C 540 (as revised, effective for periods ending on or after December 15, 2023) | The AICPA analogue to AS 2501; requires a separate inherent risk assessment for each estimate and an explicit evaluation of indicators of management bias — a more prescriptive structure than AS 2501, and the principal substantive difference practitioners encounter on SSP work |
| AICPA | AU-C 402 | The AICPA analogue to AS 2601 for service organizations |
| AICPA | AU-C 520, AU-C 240, AU-C 230 | Analytical procedures, fraud, and documentation |
| SEC | Regulation S-K Item 303 | Requires MD&A discussion of results of operations and known trends, which is where AtlasFlow discusses the revenue effect of pricing and mix |

Because AtlasFlow is an SEC issuer, PCAOB standards govern the continuing case. Readers auditing private SaaS
companies apply the AICPA analogues in the right-hand rows. The difference that matters most in this chapter
is estimate auditing: AU-C 540 (revised) requires you to assess inherent risk for the SSP estimate separately
from control risk, to consider explicitly whether the estimate is subject to estimation uncertainty and
complexity, and to evaluate indicators of possible management bias. AS 2501 reaches similar territory but
organizes it around the three testing approaches rather than around a separate inherent risk assessment. In
practice a well-executed SSP file satisfies both; a file that only documents "we agreed management's
schedule" satisfies neither.

## Prerequisites and Chapter Dependencies

Read Chapter 4 first: it establishes the order-to-cash process, contract existence and enforceability, the
transaction price including variable consideration, and period-end cut-off, all of which this chapter assumes.
Chapter 2 supplies the assertion-level risk assessments and Chapter 3 the materiality figures ($1,450 overall,
$940 performance materiality, $72 clearly trivial threshold) used throughout. Chapter 6 takes the allocated
amounts produced here and audits the resulting contract liability and the remaining performance obligation
(RPO) disclosure; Chapter 12 tests the Zuora Revenue configuration as an application control; Chapter 18
develops the substantive analytical procedures that complement the tests of details described here.

## 5.1 What You Are Actually Auditing

AtlasFlow's subscription revenue of $135,800 does not originate in the general ledger. It originates in
Salesforce CPQ, where an order form is generated; it is converted into a subscription record in Zuora Billing;
that record is pushed nightly to Zuora Revenue (RevPro) through interface I-2; RevPro applies 27 configuration
rules to identify performance obligations, allocate the transaction price, and build a revenue schedule; and
interface I-3 posts a monthly summary journal to NetSuite accounts 4100, 4110, 4120, 2400, 2405, and 2410. By
the time a number reaches account 4100, six systems and four judgments have acted on it.

The consequence for audit design is that "vouching revenue to the invoice" tests almost nothing that matters.
An invoice proves that AtlasFlow billed $600 to Meridian Health Systems in March 2025. It does not prove that
$600 was the amount allocated to the Core performance obligation, that $600 was the amount recognizable in
FY2025, or that the period over which it is spread is correct. On a ramped contract the invoice is
systematically the wrong number, by construction.

**Exhibit 5-1. Where the assertions live in the subscription revenue process.**

| Process point | System | Relevant assertion most at risk | Chapter that owns it |
| --- | --- | --- | --- |
| Order form generated and approved | Salesforce CPQ | Occurrence; cut-off (contract date) | Chapter 4 |
| Subscription record created; service dates set | Zuora Billing | Cut-off; accuracy (service start date) | Chapter 4, this chapter §5.11 |
| Performance obligations identified | Zuora Revenue | Accuracy; classification | This chapter, §5.2–5.3 |
| SSP assigned and transaction price allocated | Zuora Revenue | Accuracy (measurement) | This chapter, §5.5–5.7 |
| Revenue schedule built and released monthly | Zuora Revenue | Cut-off; accuracy | This chapter, §5.9–5.11 |
| Amendment processed | Zuora Billing → Zuora Revenue | Accuracy; completeness of modification population | This chapter, §5.8 |
| Usage measured and rated | AtlasFlow platform → Zuora Billing | Completeness; accuracy | This chapter, §5.10 |
| Monthly summary journal posted | Zuora Revenue → NetSuite | Completeness; accuracy | Chapter 6, §6.3 |
| Contract liability classified and disclosed | NetSuite | Classification; presentation | Chapter 6 |

The two assertions that dominate subscription revenue are **accuracy** (is the measured amount right, given
the allocation and the term?) and **cut-off** (is it in the right period?). Existence is a lesser concern for
recurring revenue on a signed multi-year contract, and completeness of revenue is rarely the direction of
management bias — but see Chapter 6, §6.2, where completeness becomes dominant the moment you turn the
transaction around and look at the liability.

## 5.2 Identifying Performance Obligations in a SaaS Contract

ASC 606-10-25-19 sets two conditions. A promised good or service is a performance obligation only if it is
(a) **capable of being distinct** — the customer can benefit from it on its own or together with resources
readily available to the customer — and (b) **distinct within the context of the contract** — the promise is
separately identifiable from other promises, which ASC 606-10-25-21 elaborates through three indicators: the
entity does not provide a significant integration service, the good or service does not significantly modify
or customize another good or service in the contract, and the good or service is not highly interdependent
with or highly interrelated to others in the contract.

Two further concepts do a great deal of work in SaaS. First, **setup and administrative activities that
transfer nothing to the customer are not performance obligations** (ASC 606-10-25-17); provisioning a tenant
in a multi-tenant environment is such an activity, even when it is separately invoiced. A separately invoiced
non-refundable setup fee is therefore part of the transaction price allocated to the subscription, not its own
obligation. Second, **hosting is a fulfillment activity, not a promise**: the customer is buying access to
functioning software, and the infrastructure on which it runs is how AtlasFlow delivers it.

### 5.2.1 The C-1 Meridian analysis, worked

Contract C-1 with Meridian Health Systems was signed March 12, 2025 for a 36-month term running March 15,
2025 through March 14, 2028. Its commercial terms, taken from the order form and its Exhibit B, are:

- Core subscription for 500 automation seats, ramped: year 1 $600, year 2 $840, year 3 $960 (total $2,400),
  billed annually in advance on each anniversary.
- AtlasFlow Insight add-on at $180 per year for contract years 2 and 3 only (total $360).
- Fixed-fee professional services of $360, comprising an Implementation and Configuration statement of work
  and an Administrator Training package of five instructor-led sessions. *For purposes of this illustration,
  assume the order form's Exhibit B separately describes and separately scopes these two items; the continuing
  case records only the aggregate $360 fixed fee.* Billed 50% on signature and 50% on go-live.
- 200,000 workflow runs per contract year included; overage at $12 per 1,000 runs (a rate stated in whole
  dollars, not thousands).

Total fixed consideration is $2,400 + $360 + $360 = **$3,120**.

**Exhibit 5-2. Performance obligation identification for contract C-1.**

| Promised good, service, or activity | Capable of being distinct? | Distinct in the context of the contract? | Conclusion |
| --- | --- | --- | --- |
| Access to the hosted Core platform | Yes | — | Component of PO 1 |
| Standard technical support included in the subscription | No — not sold separately; the customer cannot benefit from support without platform access | — | Combined into PO 1 |
| Unspecified updates, upgrades, and new features | No — delivered automatically to all tenants; the customer cannot decline or benefit separately | — | Combined into PO 1 |
| Hosting infrastructure (AWS us-east-1) | No — a fulfillment activity | — | Not a performance obligation |
| Tenant provisioning and account activation | No — a setup activity that transfers no good or service (ASC 606-10-25-17) | — | Not a performance obligation |
| Uptime commitment | No — a warranty-type assurance of the service already promised | — | Not a performance obligation; variable consideration if credits are earned (Chapter 4, §4.9) |
| AtlasFlow Insight analytics module | Yes — a separate SKU, sold on a standalone basis 31 times in FY2025 | Yes — Insight consumes a read-only data feed from Core; AtlasFlow provides no significant integration service, Insight does not modify Core, and Core operates fully without Insight | **PO 2** |
| Implementation and configuration services | Yes — comparable work is performed by third parties, including Tessera Partners on the C-4 arrangement | Yes — configuration uses supported administrative tooling and does not modify the Core code base | **PO 3** |
| Administrator training, five sessions | Yes — sold as a catalog SKU at $10 per session | Yes — not required to operate Core; deliverable before, during, or after go-live | **PO 4** |
| Workflow-run capacity above 200,000 per contract year | Not a separate promise — the capacity is part of the same stand-ready service | — | Variable consideration attributable to PO 1 (§5.10) |

Four performance obligations, then: PO 1 Core subscription, PO 2 Insight subscription, PO 3 implementation and
configuration, PO 4 training.

### 5.2.2 When implementation is not distinct

The C-1 conclusion is not universal. Implementation services fail the "distinct in the context of the
contract" test when they significantly customize or modify the subscribed software, or when the customer
cannot obtain the promised functionality without them. Two diagnostics separate the cases:

1. **Could a competent third party perform the work?** If AtlasFlow's own engineering team must write code
   into the platform for the arrangement to function, the answer is no and PO 3 collapses into PO 1.
2. **Does the subscription have standalone utility on day one without the services?** If the customer's
   contracted use case is unattainable until AtlasFlow builds a bespoke connector, the services are an input
   to a combined output.

*For purposes of this illustration, assume* Brightline's manager, Omar Haddad, scoped the professional
services population and identified 11 FY2025 contracts, with aggregate professional services fees of $2,180,
in which the statement of work included construction of a customer-specific integration adapter maintained in
AtlasFlow's own code base. On those 11 contracts the services were combined with the subscription and
recognized over the subscription term rather than as delivered. The population and the conclusion are a
required part of the file, because the direction of the error is toward earlier revenue: separating a
non-distinct implementation accelerates $2,180 of fees into the delivery period instead of spreading them
over 12 to 36 months. If management had treated all 11 as distinct, and if the average acceleration were
eight months of a twelve-month term, the overstatement would be roughly $2,180 × 8/12 = $1,453 — above
overall materiality of $1,450. That arithmetic is the reason this test is not optional.

## 5.3 The Series Guidance and Why a Subscription Is One Performance Obligation

ASC 606-10-25-14(b) treats as a single performance obligation "a series of distinct goods or services that are
substantially the same and that have the same pattern of transfer," where each distinct good or service in the
series would be satisfied over time and the same method would be used to measure progress (ASC 606-10-25-15).

Applied to AtlasFlow Core: each day of platform availability is a distinct service — the customer benefits
from Monday's availability independently of Tuesday's. The days are substantially the same, each is satisfied
over time, and a time-elapsed measure of progress applies to each. The series criteria are met, so the 1,096
days of C-1's Core term are one performance obligation rather than 1,096, and revenue is recognized ratably.

Three consequences follow, and they are the reason this apparently technical conclusion is worth auditing:

1. **Variable consideration can be allocated to a distinct service within the series** rather than across the
   whole contract (ASC 606-10-32-40), which is what allows usage overage to be recognized in the month
   consumed rather than spread over the term. This is the mechanism, not the "right to invoice" expedient, and
   the two are often confused.
2. **A mid-term modification affects the remaining days but not the delivered days**, which is why most SaaS
   upsells are prospective rather than cumulative catch-up (§5.8).
3. **The measure of progress must be time**, not seats, not usage, and not invoicing. AtlasFlow's policy
   (case §4.1) recognizes Core and Insight straight-line from the later of the contract start date and the
   provisioning date. That policy is consistent with the series conclusion.

Where the series conclusion breaks down is where the daily service is *not* substantially the same across the
term. Two AtlasFlow fact patterns test it. First, C-1's Insight element begins in contract year 2: the
Core-only days in year 1 differ from the Core-plus-Insight days in years 2 and 3. That is not a problem for
the series conclusion, because Core and Insight are separate performance obligations with separate terms — but
it is fatal to any shortcut that recognizes the total contract fee of $3,120 evenly over 36 months. Second, a
contract that grants a phased functionality roll-out — module A in months 1 to 6, module A plus module B
thereafter — has two series, not one.

**Documentation test.** Your working paper on this point should state the promises, the two ASC 606-10-25-19
tests for each, the series criteria, and the conclusion, with a reference to the order form section relied on.
A one-line assertion that "the subscription is a single performance obligation per company policy" is not
audit documentation; it is a restatement of management's conclusion.

## 5.4 Material Rights and Their Valuation

A customer option to acquire additional goods or services gives rise to a performance obligation only if it
provides the customer with a **material right** — a right the customer would not have received without
entering into the contract, typically a discount incremental to the range of discounts ordinarily given for
those goods or services to that class of customer in that market (ASC 606-10-55-42 and 55-43). The test is
incrementality, not size. A 20% renewal discount offered to every customer in a price list is not a material
right; a 20% discount available only to customers who sign a 24-month term is.

Contract C-2 with Voltaire Logistics S.A. is a renewal signed October 1, 2025 for 24 months with a total fixed
fee of $1,600, and it includes a "renewal credit" of $200 usable only toward a future purchase of Insight. The
credit is not available on AtlasFlow's price list, is not offered to customers who do not renew, and can be
applied on top of whatever discount Voltaire negotiates on the eventual Insight order. It is a material right.

### 5.4.1 Valuing the right: an expected-value model with breakage

The standalone selling price of a material right is the discount the customer would obtain when exercising the
option, adjusted for both any discount the customer could receive without exercising it and the likelihood of
exercise (ASC 606-10-55-44). The likelihood adjustment is the **breakage** assumption, and it is where the
estimate lives.

*For purposes of this illustration, assume* AtlasFlow's technical accounting group, Aisha Bello's team, built
the redemption history from the 148 renewal credits issued between January 2023 and December 2024 whose
redemption windows had closed by June 30, 2025.

**Exhibit 5-3. Redemption experience on 148 closed renewal credits (whole counts and percentages).**

| Outcome | Count | Weight applied | Weighted redemption |
| --- | --- | --- | --- |
| Redeemed in full | 96 | 100% | 96.00 |
| Redeemed in part | 18 | 55% (average share of face redeemed) | 9.90 |
| Expired unused | 34 | 0% | 0.00 |
| **Total** | **148** | | **105.90** |

Expected redemption rate = 105.90 ÷ 148 = **71.55%**. Implied breakage = 28.45%.

Standalone selling price of the C-2 material right = $200 × 71.55% = **$143.10**, rounded to **$143** for
allocation. Two checks before you accept that number:

- **Is the right material?** $143 ÷ $1,600 = 8.9% of the transaction price. Many firms use a rule of thumb
  that a right whose SSP is below roughly 3% to 5% of the transaction price is not material for allocation
  purposes; $143 is comfortably above any such threshold, and the conclusion does not depend on the threshold
  chosen.
- **Is the incremental-discount adjustment needed?** If the credit could only be used *instead of* the
  standard Insight discount, its incremental value would be the excess over that discount and would be far
  smaller. The C-2 order form provides that the credit applies to the net invoiced amount after standard
  discounting, so the full $143 is incremental. Read the clause; do not assume.

### 5.4.2 Allocating C-2 and the range of defensible answers

**Exhibit 5-4. Contract C-2 allocation, relative standalone selling price basis (in thousands).**

| Performance obligation | SSP | % of total SSP | Allocated transaction price |
| --- | --- | --- | --- |
| PO 1 — Core subscription, 24 months (Oct 1, 2025 – Sep 30, 2027) | 1,748.000 | 92.438% | 1,479.006 |
| PO 2 — Material right (future Insight credit) | 143.000 | 7.562% | 120.994 |
| **Total** | **1,891.000** | **100.000%** | **1,600.000** |

Allocation factor: $1,600 ÷ $1,891 = 0.846113. Applied to each SSP: $1,748 × 0.846113 = $1,479.006 and
$143 × 0.846113 = $120.994. The allocated amounts sum to $1,600.000.

PO 1 is recognized over the 730 days from October 1, 2025 to September 30, 2027, a daily rate of
$1,479,005.82 ÷ 730 = $2,026.04. FY2025 revenue on PO 1 covers the 92 days from October 1 to December 31,
2025: 92 × $2,026.04 = **$186,395.68**, or $186.4. The $120.994 allocated to the material right stays in the
contract liability until the option is exercised or expires unexercised.

The breakage rate is the assumption to press. **The range of defensible answers** runs from roughly 60% to
80% redemption, and here is what moves it:

| Redemption rate | SSP of the right | Allocated to PO 1 | Allocated to the right | FY2025 PO 1 revenue | Difference from illustration |
| --- | --- | --- | --- | --- | --- |
| 60.0% | 120.000 | 1,497.216 | 102.784 | 188.690 | 2.294 |
| 71.55% (illustrated) | 143.100 | 1,479.006 | 120.994 | 186.396 | — |
| 80.0% | 160.000 | 1,465.828 | 134.172 | 184.734 | (1.662) |

Evidence that would move the estimate toward the low end: Insight's list price rose 8% in April 2025, making
the credit a smaller proportional discount and reducing the incentive to redeem; and Voltaire has declined
Insight twice in prior renewal cycles. Evidence toward the high end: 96 of 148 historical credits were redeemed
in full, and AtlasFlow's account teams are compensated on expansion bookings and actively market the credit.
Because the whole range moves FY2025 revenue on C-2 by less than $4 against performance materiality of $940,
you would not spend more time on C-2's breakage rate — but you must know the range before you can say that,
and the same estimate applied to the population of 214 material rights outstanding at December 31, 2025 is a
different question, addressed in Chapter 6, §6.11 where the rights enter the RPO disclosure.

## 5.5 Standalone Selling Price: The Four Approaches

ASC 606-10-32-32 requires SSP to be determined at contract inception, and defines it as the price at which the
entity would sell a promised good or service *separately* to a customer. The best evidence is an observable
price in a standalone sale. Where no observable price exists, ASC 606-10-32-33 and 32-34 require an estimate,
and describe three approaches (they are not a hierarchy, but observable evidence is not optional where it
exists):

1. **Adjusted market assessment.** Evaluate the market into which the good or service is sold and estimate the
   price a customer would be willing to pay, which may include reference to competitors' prices adjusted for
   differences in cost and margin.
2. **Expected cost plus a margin.** Forecast the costs of satisfying the obligation and add an appropriate
   margin.
3. **Residual approach.** Deduct the sum of the observable standalone selling prices of the other promises
   from the total transaction price. Permitted only if the good or service is sold to different customers for a
   broad range of amounts (that is, the selling price is highly variable) or if the entity has not yet
   established a price for it and it has not previously been sold on a standalone basis.

Two constraints on the residual approach are routinely ignored in practice and should be the first thing you
look for. First, the residual approach may not be used for a good or service for which an observable or
otherwise estimable price exists simply because it is arithmetically convenient. Second, if applying the
residual approach produces an amount that is not within a reasonable range of the observable evidence, or if
it produces little or no consideration, the entity must use another approach (ASC 606-10-32-35). The residual
approach also cannot be applied to more than one performance obligation in the same contract without a further
allocation step.

### 5.5.1 The residual approach on C-1, and why it fails

Apply it mechanically. Observable or otherwise supported SSPs for the other three obligations are Core
$2,700, implementation $310, and training $50 — a total of $3,060. The transaction price is $3,120.

Residual attributable to Insight = $3,120 − $3,060 = **$60** for 24 months, or $30 per year. Against Insight's
list price of $240 per year for Meridian's 500-seat configuration, that is 12.5% of list. The lowest observed
standalone Insight sale in FY2025 was at 58.0% of list. A residual SSP of 12.5% of list is not within a
reasonable range of the observable evidence, so the residual approach is prohibited here and management must
use an estimation approach. Note what would have happened had it been used: C-1's FY2025 revenue would have
been $1,059.3 rather than $956.4, an overstatement of $103 on a single contract, because starving the
not-yet-commenced Insight obligation of allocated consideration pushes consideration onto the obligation that
is already being satisfied. That directional insight generalizes — **understating the SSP of a
later-commencing obligation accelerates revenue** — and it is why the residual approach is a fraud vector in
SaaS, not merely a technical error.

### 5.5.2 How AtlasFlow actually built the Insight SSP

Case §4.1 records that AtlasFlow established Core's SSP from observable standalone sales, and Insight's SSP
using the expected-cost-plus-a-margin and adjusted-market-assessment approaches. The construction, per
management's memo (Aisha Bello, workpaper reference PBC-SSP-2025-03), is:

**Exhibit 5-5. Management's Insight SSP derivation (annual amounts per 500-seat configuration, in thousands).**

| Approach | Input | Computation | Result | As % of $240 list |
| --- | --- | --- | --- | --- |
| Adjusted market assessment | Competitor analytics modules and AtlasFlow's win/loss pricing file indicate a willingness-to-pay band of 86% to 92% of AtlasFlow list | Midpoint of the band | 213.60 | 89.0% |
| Expected cost plus a margin | Annual directly attributable cost to serve an Insight tenant of 36.50; target subscription gross margin of 80.0%, being AtlasFlow's FY2025 actual (27,160 ÷ 135,800 = 20.0% cost ratio) | 36.50 ÷ (1 − 0.800) | 182.50 | 76.0% |
| **Weighted conclusion** | Equal weighting of the two approaches | (213.60 + 182.50) ÷ 2 | **198.05, rounded to 198.00** | **82.5%** |

Management then corroborated 82.5% against the 31 standalone Insight sales in FY2025, whose median was
82.5% of list — an exact match. **That exact match is a skepticism trigger, not a comfort.** An equal weighting
of two approaches is a choice, and a choice that lands precisely on the corroborating statistic invites the
question whether the weighting was selected to reach it. The audit response is to ask for the version history
of the memo and the underlying weighting analysis, and to test whether any weighting other than 50/50 was
considered and documented. Brightline asked; the answer appears in the case study at the end of this chapter.

## 5.6 Auditing an SSP Analysis Quantitatively

An SSP conclusion is an accounting estimate. Under AS 2501 you may test management's process, develop an
independent expectation, or evaluate subsequent events; in practice on an SSP you do the first two together.
Testing management's process on an SSP means testing four things: the population of observations, the
qualification of each observation as genuinely standalone, the statistics computed from the population, and
whether the population is sufficient to support a point estimate at all.

### 5.6.1 The price band and its statistics

AtlasFlow's 31 FY2025 standalone Insight sales, expressed as the ratio of the negotiated price to Insight list
price for that customer's seat configuration, are (sorted, in percent of list):

```text
58.0  61.5  63.0  65.0  66.5  68.0  69.5  71.0  72.5  74.0  75.5  77.0  78.5  80.0  81.0  82.5
84.0  85.0  86.5  88.0  89.0  90.5  92.0  93.0  94.5  96.0  97.0  98.0  100.0  100.0  100.0
```

**Exhibit 5-6. Insight standalone-sale price band, FY2025.**

| Statistic | All 31 observations | 23 qualifying observations (see §5.6.2) |
| --- | --- | --- |
| Count | 31 | 23 |
| Minimum | 58.0% | 61.5% |
| First quartile (Q1) | 71.0% | 71.0% |
| Median | 82.5% | 81.0% |
| Third quartile (Q3) | 93.0% | 92.0% |
| Maximum | 100.0% | 100.0% |
| Interquartile range | 22.0 points | 21.0 points |
| Mean | 81.8% | 81.4% |
| Standard deviation | 12.7 points | — |
| Coefficient of variation | 15.5% | — |
| Observations within ±15% of the median (70.1% to 94.9%) | 18 of 31 (58.1%) | — |

The interquartile range of 22.0 points is the figure the continuing case records, and it is the figure that
decides the audit. A price band whose middle half spans 22 points of list is not a "consistent" price; it is a
distribution. Firms differ on the threshold — a common but non-authoritative benchmark is that a single-point
SSP is supportable when a substantial majority (often expressed as 80%) of standalone observations fall within
±15% of the proposed point. Here only 58.1% do. Management's own conclusion that observable standalone prices
were insufficient for Insight is therefore correct, and it is corroborated by the statistics rather than
contradicted by them. Say so in the file; auditors sometimes treat management's decision to estimate as a
weakness when it is in fact the required answer.

### 5.6.2 Testing whether an observation is actually standalone

An observation belongs in the population only if the price was set without the influence of a bundled sale.
Brightline's data and analytics specialist, Tara Iyer, extracted all 31 order forms and applied three
disqualifying criteria: the Insight order form was signed within 90 days of a Core order or renewal by the same
customer; the Insight line appeared on the same order form as a Core renewal; or the price was set by a
reseller rather than by AtlasFlow.

**Exhibit 5-7. Disqualified observations.**

| Observation (% of list) | Disqualifying criterion |
| --- | --- |
| 100.0 | Same order form as a Core renewal |
| 100.0 | Same order form as a Core renewal |
| 96.0 | Insight signed 41 days after a Core renewal |
| 88.0 | Insight signed 22 days after a Core order |
| 84.0 | Price set by reseller Tessera Partners |
| 74.0 | Insight signed 68 days after a Core order |
| 65.0 | Same order form as a Core renewal |
| 58.0 | Insight signed 9 days after a Core order |

Eight of 31 observations (25.8%) failed. Removing them moves the median from 82.5% to 81.0% and narrows the
interquartile range from 22.0 to 21.0 points. The direction matters less than the fact that the population
management represented as standalone was one-quarter not standalone; that is a finding about the reliability of
the IPE underlying the estimate, and it belongs in your evaluation of control risk over the SSP process
regardless of the small effect on the point estimate.

### 5.6.3 Concentration analysis

A median is only as good as the homogeneity behind it. Disaggregate.

**Exhibit 5-8. Concentration in the 31-observation population.**

| Dimension | Concentration | Why it matters |
| --- | --- | --- |
| Signed in H2 2025 | 24 of 31 (77.4%); H2 mean 77.2% of list versus H1 mean 97.9% | The band is not random dispersion around a stable price; it is a declining trend as a new SKU was discounted. A median across the whole year overweights stale, high early prices. |
| Sold by three account executives | 14 of 31 (45.2%) | Individual negotiating behavior, not market price, may drive nearly half the observations |
| Mid-market segment | 22 of 31 (71.0%) | AtlasFlow's Insight revenue is weighted to enterprise contracts; the population is not representative of the contracts being allocated |
| United States | 24 of 31 (77.4%) | The UK and Australian entities allocate using the same SSP with five and two observations respectively |
| Annual contract value below $60 | 19 of 31 (61.3%) | Small deals are discounted differently from large ones |
| Failed the standalone qualification test | 8 of 31 (25.8%) | See §5.6.2 |

The H1/H2 finding is the substantive one. The median of the seven H1 sales is 98.0% of list; the median of the
24 H2 sales is 77.8%. If the SSP is meant to represent the price at which AtlasFlow *would* sell Insight
separately — a forward-looking, contract-inception concept applied to contracts signed throughout the year —
then a single annual median is imprecise for both halves of the year. The defensible responses are a
time-weighted SSP, a semi-annual SSP refresh, or a demonstration that the annual figure is not materially
different from a period-specific one. Management did none of the three; §5.6.4 quantifies whether it matters.

### 5.6.4 Is 31 observations enough?

Sufficiency is answerable arithmetically. With a mean of 81.8% and a standard deviation of 12.7 points, the
standard error of the mean is 12.7 ÷ √31 = 2.28 points. A two-sided 95% confidence interval on the mean is
81.8 ± (1.96 × 2.28) = 81.8 ± 4.5, or **77.4% to 86.3%** of list — a span of 8.9 points.

Translate the span into dollars using the population sensitivity developed in the case study below: FY2025
subscription revenue moves approximately $10.71 for each one-point change in the Insight SSP. An 8.9-point span
therefore corresponds to approximately $95 of FY2025 revenue, which is 10.1% of performance materiality of
$940 and 6.6% of overall materiality of $1,450. On that basis 31 observations, even with 8 disqualified, are
sufficient to support a conclusion that the estimate does not give rise to a material misstatement in FY2025.
State the arithmetic; do not assert sufficiency.

**What an unexpected result looks like.** If the same computation had produced a span worth $1,100 of revenue
— which it would if AtlasFlow's Insight-bearing contract population were seven times larger, as it plausibly
will be in FY2027 — 31 observations would be insufficient. Your next steps would then be: request the FY2026
year-to-date standalone population to extend the observation set, develop an independent expectation using
competitor pricing and AtlasFlow's own win/loss data, consult the national office (Priya Chandrasekhar, per
case §5.2), and if a supportable point estimate still could not be reached, evaluate whether the range of
reasonable estimates itself exceeds materiality — which is an audit difference to be accumulated, not a
disagreement to be argued.

## 5.7 Allocating the Transaction Price

Allocation is arithmetic once the inputs are settled, which is why the inputs are where the audit effort goes.
The four SSPs for contract C-1, and their support, are:

**Exhibit 5-9. Contract C-1 standalone selling prices and their basis.**

| Performance obligation | SSP | Basis | Evidence inspected |
| --- | --- | --- | --- |
| PO 1 — Core subscription, 36 months | 2,700.000 | Observable standalone selling price of $1,800 per automation seat per year × 500 seats × 3 years. The $1,800 rate is the median of 1,180 FY2025 standalone Core sales, 93.8% of the March 2025 list price of $1,920 per seat per year, with an interquartile range of 6.0 points | Zuora Billing standalone-sale extract; March 2025 price list |
| PO 2 — Insight subscription, 24 months | 396.000 | Estimated SSP of 82.5% of list (Exhibit 5-5) × Insight list of $480 per seat per year × 500 seats × 2 years = $198 per year | Management's SSP memo; the 31-observation population |
| PO 3 — Implementation and configuration | 310.000 | Expected cost plus a margin: 1,240 estimated hours × $250 per hour blended standard billing rate | Professional services rate card; the C-1 statement of work estimate |
| PO 4 — Administrator training, 5 sessions | 50.000 | Observable catalog price of $10.000 per instructor-led session | FY2025 services catalog |
| **Total** | **3,456.000** | | |

The transaction price of $3,120 is 90.278% of aggregate SSP of $3,456, an overall discount of $336. Note where
the discount sits commercially: the professional services lines were sold at exactly their SSPs ($310 + $50 =
$360, the contracted fee), so the entire $336 discount was negotiated on the subscription lines.

### 5.7.1 The proportionate allocation

**Exhibit 5-10. Contract C-1 allocation of the transaction price (in thousands, to three decimal places —
that is, to the dollar).**

| Performance obligation | SSP | Relative SSP % | Allocation factor | Allocated transaction price | Discount absorbed |
| --- | --- | --- | --- | --- | --- |
| PO 1 — Core subscription | 2,700.000 | 78.1250% | 0.9027778 | 2,437.500 | (262.500) |
| PO 2 — Insight subscription | 396.000 | 11.4583% | 0.9027778 | 357.500 | (38.500) |
| PO 3 — Implementation | 310.000 | 8.9699% | 0.9027778 | 279.861 | (30.139) |
| PO 4 — Training | 50.000 | 1.4468% | 0.9027778 | 45.139 | (4.861) |
| **Total** | **3,456.000** | **100.0000%** | | **3,120.000** | **(336.000)** |

Allocation factor = $3,120 ÷ $3,456 = 65/72 = 0.9027778. The allocated column sums to $3,120.000 and the
discount column sums to $(336.000). Zuora Revenue carries these amounts to the cent: PO 3 is $279,861.11 and
PO 4 is $45,138.89, which sum to $325,000.00 against the $360 contracted professional services fee.

Contrast the allocated column with the contracted line amounts. The order form prices Core at $2,400 and
Insight at $360; allocation assigns Core $2,437.500 and Insight $357.500. The differences are small here but
they are not zero, and they are the reason the invoice is never the answer.

### 5.7.2 The discount-allocation exception

ASC 606-10-32-37 permits — and where its criteria are met, requires — a discount to be allocated to one or more
but not all performance obligations. All three criteria must be satisfied: the entity regularly sells each
distinct good or service in the contract on a standalone basis; it also regularly sells on a standalone basis a
bundle of some of those goods or services at a discount to their standalone selling prices; and the discount
attributable to that bundle is substantially the same as the discount in the contract, with an analysis of the
bundle's standalone selling prices providing observable evidence of the performance obligation or obligations
to which the entire discount belongs.

Applied to C-1: the contract discount of $336 relates entirely, in commercial substance, to the Core-and-Insight
bundle, a discount of $336 ÷ $3,096 = 10.85% of the combined subscription SSP. *For purposes of this
illustration, assume* AtlasFlow's FY2025 population contains 214 Core-plus-Insight bundle sales with a median
discount to aggregate SSP of 10.4% and an interquartile range of 4.2 points, so 10.85% does fall inside the
observed band. Criterion three is arguably met. Criterion one is not: Insight was sold on a standalone basis
only 31 times (23 after qualification) against 1,180 Insight-bearing contracts — 2.6% of the population — which
does not support a conclusion that AtlasFlow "regularly" sells Insight separately. Management concluded the
exception was unavailable and allocated proportionately. Brightline concurred.

The conclusion has consequences worth quantifying, because a reader who accepts "management allocated
proportionately" without testing the alternative does not know what is at stake:

**Exhibit 5-11. Contract C-1 under the discount-allocation exception (in thousands).**

| Performance obligation | Allocation under the exception | Allocation as illustrated (proportionate) | Difference |
| --- | --- | --- | --- |
| PO 1 — Core subscription | 2,406.977 | 2,437.500 | (30.523) |
| PO 2 — Insight subscription | 353.023 | 357.500 | (4.477) |
| PO 3 — Implementation | 310.000 | 279.861 | 30.139 |
| PO 4 — Training | 50.000 | 45.139 | 4.861 |
| **Total** | **3,120.000** | **3,120.000** | **—** |
| FY2025 revenue recognized on C-1 | 981.276 | 956.352 | 24.924 |

Applying the exception would have accelerated $24.9 of revenue on this one contract, because it moves
consideration onto the professional services obligations that are satisfied inside FY2025 and away from the
subscription obligations spread over 36 months. Across the 214 bundle contracts the direction is the same, and
the aggregate would not be trivial. Whether the exception applies is therefore a judgment worth a documented
conclusion, not a footnote.

### 5.7.3 Where the recognition pattern comes from

Allocation answers "how much." The measure of progress answers "when."

**Exhibit 5-12. Contract C-1 recognition pattern by performance obligation.**

| PO | Allocated amount | Service period | Days in period | Measure of progress | Rate |
| --- | --- | --- | --- | --- | --- |
| PO 1 — Core | 2,437.500 | Mar 15, 2025 – Mar 14, 2028 | 1,096 | Time elapsed (series) | $2,224.00 per day |
| PO 2 — Insight | 357.500 | Mar 15, 2026 – Mar 14, 2028 | 731 | Time elapsed (series) | $489.06 per day |
| PO 3 — Implementation | 279.861 | Apr 1 – Jul 31, 2025 | n/a | Input measure: hours incurred ÷ 1,240 estimated hours | $225.6944 per hour |
| PO 4 — Training | 45.139 | Sessions delivered Jun 2025 – Apr 2026 | n/a | Output measure: sessions delivered ÷ 5 | $9,027.78 per session |

PO 1's daily rate is $2,437,500 ÷ 1,096 = $2,223.9964, which rounds to $2,224.00 per day. Zuora Revenue clears
the resulting $4.00 cumulative rounding residual in the final period of the schedule (March 2028); check that
behavior in the configuration rather than assuming it, because an engine that clears rounding in the *first*
period overstates early revenue.

## 5.8 Contract Modifications

A modification is a change in scope, price, or both that the parties approve. ASC 606-10-25-10 through 25-13
produce three outcomes, and the decision sequence is strict.

**Exhibit 5-13. Contract modification decision tree.**

```text
1. Have the parties approved a change in the scope or price of the contract
   (in writing, orally, or by customary business practice)?
      NO  -> Not a modification. If the change is a change in the estimate of variable
             consideration, adjust the transaction price and reallocate (no modification
             accounting).
      YES -> go to 2.

2. Does the modification add promised goods or services that are DISTINCT, AND is the
   price increase equal to the standalone selling price of the added goods or services
   (adjusted for contract-specific circumstances)?
      YES -> SEPARATE CONTRACT. Account for the addition on its own; leave the original
             contract untouched. (ASC 606-10-25-12)
      NO  -> go to 3.

3. Are the remaining goods or services after the modification DISTINCT from those
   transferred on or before the modification date?
      YES -> PROSPECTIVE. Terminate the existing contract and create a new one:
             remaining unrecognized consideration + new consideration, allocated to the
             remaining performance obligations over the remaining term.
             (ASC 606-10-25-13(a))
      NO  -> CUMULATIVE CATCH-UP. Treat the modification as part of the existing
             contract; adjust revenue already recognized at the modification date.
             (ASC 606-10-25-13(b))

4. Mixed case: some remaining goods or services distinct, some not
      -> Apply 25-13(a) and 25-13(b) to the respective parts, consistent with the
         objectives of paragraph 25-13.
```

For a SaaS subscription treated as a series, step 3 almost always answers "yes": the remaining days of platform
access are distinct from the days already delivered. That is why the great majority of SaaS amendments are
prospective, and why an engine configured to default to cumulative catch-up produces systematic error.

### 5.8.1 The three outcomes, worked

**Separate contract.** Contract C-3 with Northgate Financial Group runs 12 months from July 1, 2025 at $1,920
fixed, or $160 per month. *For purposes of this illustration, assume* that on November 1, 2025 Northgate added
Insight for the remaining eight months at $128 total ($16 per month), a price equal to Insight's SSP for
Northgate's configuration. Insight is distinct and is priced at SSP, so the addition is a separate contract:
Core continues at $160 per month untouched, and Insight is recognized at $16 per month from November 1. FY2025
revenue is $960 of Core (six months at $160) plus $32 of Insight (two months at $16) = **$992.0**.

**Prospective.** *For purposes of this illustration, assume* BlueRidge Insurance holds a 36-month contract
beginning April 1, 2024 at $2,160 total ($60 per month) for 300 automation seats, and that on July 1, 2025 it
added 100 seats for the remaining 21 months at $315 total against an SSP for those incremental seats of $420.
The added seats are not priced at SSP, so this is not a separate contract; the remaining days of service are
distinct from the days already delivered, so it is prospective.

| Step | Computation | Amount |
| --- | --- | --- |
| Original transaction price | 36 months × $60 | 2,160.0 |
| Revenue recognized through June 30, 2025 | 15 months × $60 | 900.0 |
| Remaining unrecognized consideration at modification date | 2,160.0 − 900.0 | 1,260.0 |
| Add: additional consideration from the modification | | 315.0 |
| Revised remaining consideration | 1,260.0 + 315.0 | 1,575.0 |
| Remaining term | Jul 1, 2025 – Mar 31, 2027 | 21 months |
| Revised monthly rate | 1,575.0 ÷ 21 | 75.0 |
| **FY2025 revenue** | (6 months × $60) + (6 months × $75) = 360.0 + 450.0 | **810.0** |

No adjustment is made to the $900 already recognized. That is the defining feature of prospective treatment and
the easiest thing to check in a subledger: a prospective amendment should generate no catch-up entry.

**Cumulative catch-up.** *For purposes of this illustration, assume* Halloran Energy holds a 24-month contract
beginning January 1, 2025 at $1,200 total ($50 per month), and that on October 1, 2025 AtlasFlow granted a
$120 price concession applying to the whole contract, with no change in scope. Nothing distinct is added, and
the concession reprices services already delivered as well as those remaining, so the remaining services are
not distinct from those already transferred in the sense required by 25-13(a). Cumulative catch-up applies.

| Step | Computation | Amount |
| --- | --- | --- |
| Revenue recognized through September 30, 2025 under the original price | 9 months × $50 | 450.0 |
| Revised total transaction price | 1,200.0 − 120.0 | 1,080.0 |
| Measure of progress at September 30, 2025 | 9 of 24 months elapsed | 37.5% |
| Cumulative revenue that should be recognized at September 30, 2025 | 1,080.0 × 37.5% | 405.0 |
| **Cumulative catch-up adjustment recorded in October 2025** | 405.0 − 450.0 | **(45.0)** |
| Remaining consideration | 1,080.0 − 405.0 | 675.0 |
| Remaining term | Oct 1, 2025 – Dec 31, 2026 | 15 months |
| Revised monthly rate | 675.0 ÷ 15 | 45.0 |
| **FY2025 revenue** | 450.0 − 45.0 + (3 months × $45.0) | **540.0** |

Prove the answer independently: 12 of 24 months elapsed by December 31, 2025, so cumulative revenue should be
$1,080.0 × 12/24 = $540.0. The two computations agree, which is the check you run on every catch-up before you
accept it.

### 5.8.2 Auditing the modification population

The modification risk is not that any single amendment is misclassified; it is that the classification is made
by a configuration rule keyed to an amendment type code selected by a salesperson in Salesforce CPQ.

*For purposes of this illustration, assume* Zuora Billing processed 1,412 amendments in FY2025, classified by
RevPro as follows.

**Exhibit 5-14. FY2025 amendment population by RevPro treatment.**

| Amendment category | Count | RevPro treatment | Inherent risk of misclassification |
| --- | --- | --- | --- |
| Renewal at or near SSP with no change to the remaining term | 604 | Separate contract | Low |
| Addition of a distinct service priced at SSP | 318 | Separate contract | Moderate — depends on the SSP conclusion |
| Addition of a distinct service not priced at SSP | 187 | Prospective | Moderate |
| Seat or quantity increase mid-term | 214 | Prospective | Low |
| Price concession or ramp restructuring with no added services | 61 | Cumulative catch-up | High — judgmental and income-affecting |
| Term extension with repricing of the remaining term | 28 | Cumulative catch-up or prospective, by judgment | High |
| **Total** | **1,412** | | |

Design the test around the risk, not the count. The 604 renewals carry low risk and can be covered by a
population-level analytic: confirm that no renewal amendment generated a catch-up entry in the subledger, which
is a single query. The 89 amendments in the last two rows generate the catch-up entries and warrant a test of
details. The completeness question is separate and more important: **can a modification exist that never became
an amendment record?** A side letter, an email price concession, or a credit memo issued in lieu of a
repricing all modify the contract without touching Zuora. Your procedures must reach those populations —
credit memos over a threshold, the legal department's contract file, and the December 2025 approval exceptions
in CPQ. Chapter 17, §17.7 develops the side-letter search; Chapter 4, §4.3 owns contract existence.

**What an unexpected result looks like.** If your query of catch-up entries returns entries on contracts
classified as renewals, either the classification or the configuration is wrong. Trace three such entries to
the amendment document. If the amendment repriced the remaining term of an existing contract rather than
starting a new one, the classification was wrong and the population of 604 is contaminated; expand testing and
reassess whether the amendment-type field is reliable IPE at all.

## 5.9 Ramped Contracts and Non-Coterminous Elements

Approximately 34% of AtlasFlow's annual contract value sits in multi-year contracts with escalators or ramps
(case §1.3). A ramp is a contractual price that rises over the term. C-1 is the canonical example: $600, then
$840, then $960.

The governing principle is that the transaction price is the total consideration for the performance
obligation, and the measure of progress for a series satisfied ratably over time is time elapsed. Neither
concept has anything to do with the invoicing schedule. Recognizing the invoiced amount is therefore wrong
unless the ramp happens to track the pattern of transfer — which, for a stand-ready service that is identical
on every day of the term, it does not.

**Exhibit 5-15. Contract C-1 Core performance obligation: invoiced versus recognized (in thousands).**

| Contract year | Period | Days | Core amount invoiced | Core revenue recognized | Annual difference | Cumulative difference |
| --- | --- | --- | --- | --- | --- | --- |
| Year 1 | Mar 15, 2025 – Mar 14, 2026 | 365 | 600.000 | 811.760 | (211.760) | (211.760) |
| Year 2 | Mar 15, 2026 – Mar 14, 2027 | 365 | 840.000 | 811.760 | 28.240 | (183.520) |
| Year 3 | Mar 15, 2027 – Mar 14, 2028 | 366 | 960.000 | 813.980 | 146.020 | (37.500) |
| **Total** | | **1,096** | **2,400.000** | **2,437.500** | **(37.500)** | |

Annual recognized amounts are 365 or 366 days at the $2,224.00 daily rate, with the $4.00 rounding residual
absorbed in year 3 ($813,984 computed less $4 = $813,980). The residual cumulative difference of $(37.500)
is not a ramp effect at all: it is the $37.5 of consideration reallocated *onto* the Core obligation from the
Insight and professional services lines by the allocation in Exhibit 5-10.

Two things follow. First, at every measurement date before the crossover, the contract has a **contract asset**
— revenue recognized in excess of amounts billed and unconditionally receivable. C-1's Core element reaches a
$211.8 contract asset by March 14, 2026. Chapter 6, §6.8 develops the presentation and the contract-level
netting rule that determines whether it appears as a contract asset or is netted against the deferred revenue
on the same contract. Second, the ramp is an inherent risk factor for the *directional* error: recognizing the
invoiced amount in year 1 understates revenue by $211.8, and management has no incentive to make that error.
Recognizing the *average* invoiced amount ($800 per year) rather than the allocated amount overstates year-1
revenue relative to the correct answer only marginally, but a configuration that spreads the total *invoiced*
fee of $2,400 rather than the *allocated* $2,437.500 understates the Core obligation by $37.5 over the term. In
FY2025, that error alone is 292 days × ($2,189.78 − $2,224.00) = 292 × $(34.22) = $(10.0). The
February 2025 RevPro configuration change was made specifically to accommodate ramps (case §1.8) and was
deployed with abbreviated user acceptance testing, which is why this is the arithmetic you should be running.

### 5.9.1 When straight-line is wrong

Straight-line recognition of the total fee is the general answer, not a universal one. Three fact patterns
displace it:

1. **The quantity of service changes materially over the term.** A contract for 100 seats in year 1 and 400
   seats in years 2 and 3 does not deliver substantially the same service each day; the daily services are not
   substantially the same, the series criteria fail for the combined term, and the appropriate answer is
   generally to treat the incremental seats as a separate performance obligation with its own service period.
2. **A material right is embedded in the ramp.** A first-year price far below SSP, recoverable through
   above-SSP pricing in later years, can be a material right that requires separate allocation rather than
   averaging. Test it by comparing year-1 pricing to the standalone band, not to the contract average.
3. **A significant financing component exists.** Where the customer pays materially in advance or in arrears
   of performance, ASC 606-10-32-15 through 32-20 require adjustment for the time value of money, subject to
   the one-year practical expedient. AtlasFlow bills annually in advance on each anniversary, so no payment is
   more than twelve months ahead of the related service and the expedient applies. Document the expedient's
   availability; do not simply omit the topic.

## 5.10 Usage-Based Revenue and the Completeness of Usage Data

Usage overage produced $4,200 of FY2025 revenue, growing from $780 in Q1 to $1,390 in Q4. It is 2.8% of total
revenue and would be immaterial on its own; it is on the audit plan because its data source is the production
platform rather than a financial system, and because the assertion at risk is **completeness of a data
population no financial control touches**.

### 5.10.1 The mechanism, not the expedient

AtlasFlow's policy (case §4.1) recognizes overage in the month the runs are consumed. The correct authority for
that treatment is the allocation of variable consideration to a distinct service within a series
(ASC 606-10-32-40): the overage relates specifically to the days on which the excess runs were consumed. The
"right to invoice" measure of progress in ASC 606-10-55-18 is a different provision that permits recognizing
revenue equal to the amount invoiced where that amount corresponds directly to the value transferred; it is
sometimes available for usage arrangements but is not the mechanism when a committed volume must be exhausted
first. Get the authority right in the memo, because the two provisions produce different answers in the first
period of a contract with a minimum commitment.

### 5.10.2 Recomputing C-1's overage

Contract C-1 includes 200,000 workflow runs per contract year with overage at $12 per 1,000 runs, and Meridian
consumed 244,000 runs in the first contract year (March 15, 2025 – March 14, 2026). The naive computation is
(244,000 − 200,000) ÷ 1,000 × $12 = $528 in whole dollars, and the naive question is why AtlasFlow recorded no
FY2025 overage revenue for its largest customer. Both are wrong, and the reason is the measurement period.

**Exhibit 5-16. Meridian workflow-run consumption, contract year 1 (runs in thousands; revenue in whole
dollars).**

| Month | Runs consumed | Cumulative runs | Cumulative commitment consumed | Overage runs | Overage revenue |
| --- | --- | --- | --- | --- | --- |
| Mar 15–31, 2025 | 8 | 8 | 8 | — | — |
| Apr 2025 | 14 | 22 | 22 | — | — |
| May 2025 | 16 | 38 | 38 | — | — |
| Jun 2025 | 17 | 55 | 55 | — | — |
| Jul 2025 | 18 | 73 | 73 | — | — |
| Aug 2025 | 19 | 92 | 92 | — | — |
| Sep 2025 | 21 | 113 | 113 | — | — |
| Oct 2025 | 23 | 136 | 136 | — | — |
| Nov 2025 | 24 | 160 | 160 | — | — |
| Dec 2025 | 26 | 186 | 186 | — | — |
| **FY2025 subtotal** | **186** | **186** | **186** | **—** | **—** |
| Jan 2026 | 27 | 213 | 200 | 13 | 156 |
| Feb 2026 | 26 | 239 | 200 | 26 | 312 |
| Mar 1–14, 2026 | 5 | 244 | 200 | 5 | 60 |
| **Contract year 1 total** | **244** | **244** | **200** | **44** | **528** |

Cumulative consumption at December 31, 2025 was 186,000 runs against an annual commitment of 200,000. The
commitment had not been exhausted, so no overage had been earned and none should be recognized. The $528 of
overage arises entirely in FY2026, and $156 of it in January 2026 alone.

The answer depends on a contract term you must read. If the C-1 order form had stated the included volume as a
monthly allowance of 200,000 ÷ 12 = 16,667 runs, overage would have been earned in seven FY2025 months:

| Month | Runs | Monthly allowance | Overage runs | Overage revenue |
| --- | --- | --- | --- | --- |
| Jun 2025 | 17,000 | 16,667 | 333 | 4 |
| Jul 2025 | 18,000 | 16,667 | 1,333 | 16 |
| Aug 2025 | 19,000 | 16,667 | 2,333 | 28 |
| Sep 2025 | 21,000 | 16,667 | 4,333 | 52 |
| Oct 2025 | 23,000 | 16,667 | 6,333 | 76 |
| Nov 2025 | 24,000 | 16,667 | 7,333 | 88 |
| Dec 2025 | 26,000 | 16,667 | 9,333 | 112 |
| **Total** | | | **31,331** | **376** |

Overage revenue of $376 in whole dollars under the monthly reading against nil under the annual reading. On one
contract the difference is far below the $72 thousand clearly trivial threshold. Across the 1,842 accounts that
exceeded a committed volume in FY2025, the same contract-term question determines the timing of a material
portion of the $4,200 balance, and AtlasFlow's contract templates changed in April 2025. The procedure is
therefore: read the commitment clause on a sample stratified by template version, and confirm that the
Zuora Billing rate plan's usage-accumulation setting ("annual, cumulative" versus "monthly, non-cumulative")
matches the clause.

### 5.10.3 Completeness and accuracy of the usage data

The run counts come from the AtlasFlow platform's event log in AWS, are aggregated hourly into Snowflake through
Fivetran (interface I-8), and are pushed to Zuora Billing as usage records. No accounting control operates on
the event log. Four procedures address completeness:

1. **Reconcile record counts and totals end to end** for a selected month: platform event-log aggregate for
   December 2025 to the Snowflake usage table to the Zuora Billing usage records to account 4120. State each
   number and the difference. An unexplained shortfall in the Zuora leg means unbilled usage — a completeness
   error in revenue and in receivables.
2. **Test the aggregation logic**, not just its output. The event log records individual runs; the usage record
   is a monthly total per subscription. Re-perform the aggregation for one subscription from raw events.
3. **Test for gaps** in the time series. A missing hour in the Fivetran load is invisible in a monthly total.
   Query for hours with zero events across the year and investigate each.
4. **Analytically corroborate** run volumes against an independent operational measure — AWS Lambda invocation
   counts or hosting cost per run — and against the customer's own consumption dashboard, which Meridian can
   see and would dispute if wrong. The customer's visibility into the meter is a genuine control, and it is
   worth saying so in the file.

**What an unexpected result looks like.** *For purposes of this illustration, assume* the December 2025
reconciliation showed platform events of 1.284 billion runs, a Snowflake usage table total of 1.284 billion, and
Zuora Billing usage records of 1.271 billion — a shortfall of 13 million runs, or approximately 1.0%. The
shortfall must be evaluated at the population level rather than contract by contract: if 1.0% of run volume
never reaches billing in a typical month, unbilled overage across FY2025 is on the order of 1.0% × $4,200 =
$42, below the $72 clearly trivial threshold but indicative of an interface control that does not work. You
would obtain the Zuora load-error log, quantify the FY2025 effect, and evaluate whether the daily error-queue review
described in interface I-1's control description actually covers usage loads.

## 5.11 Auditing the Revenue Engine: Configuration Versus Output

Zuora Revenue is a rules engine with 27 configuration rules covering performance obligation templates, SSP
tables, allocation methods, revenue-start-date derivation, modification handling, and the release schedule. You
can obtain evidence about revenue two ways, and the distinction is not academic.

**Testing the configuration** is a test of controls. You inspect the rule as configured, re-perform it on a
test case, and conclude that the rule operates as designed. The conclusion is only as good as the general
controls that keep the configuration stable — which at AtlasFlow is precisely the problem. Weakness W-1
(four local, non-Okta-federated administrator accounts in Zuora Revenue, one a shared `revpro_admin` account
whose password sits in a vault entry accessible to six people) and W-6 (two developers with standing write
access to production RevPro configuration) mean you cannot assume the configuration you inspect in January 2026
is the configuration that processed March 2025 transactions. Chapter 11, §11.9 evaluates W-1's severity;
Chapter 12, §12.7 owns the configuration testing technique and the benchmarking concept.

**Testing the output** is a test of details. You take contracts, compute the answer yourself, and compare. The
conclusion does not depend on the configuration's stability, but its extent does depend on how much precision
you need: a sample of 30 contracts out of 3,140 supports a conclusion about accuracy only in combination with
either control reliance or a population-level analytic.

**Exhibit 5-17. What each strategy does and does not support.**

| Strategy | Evidence obtained | What it cannot support | Prerequisite |
| --- | --- | --- | --- |
| Inspect the 27 configuration rules | Design effectiveness of the allocation and scheduling logic | That the rules were unchanged during the period, or that inputs (SSP tables, service dates) are right | Effective ITGCs over RevPro change management and privileged access |
| Test of one, per rule, with re-performance | Operating effectiveness of an automated control | Anything, if ITGCs are ineffective | The same |
| Recompute revenue for a sample of contracts | Accuracy of output for the sampled contracts | Population-level accuracy without projection or an analytic | Reliable contract data (the order form, not the system record) |
| Recompute revenue for the full population from contract data | Accuracy of output for the population | Cut-off, if service dates come from the same system | Complete and accurate contract-terms extract |
| Reconcile RevPro to the GL | Completeness and accuracy of posting | Anything about the subledger's own correctness | Complete interface I-3 reconciliation |

Because AtlasFlow's ITGCs over RevPro are deficient, Brightline's FY2025 strategy is substantive: recompute
revenue for the full subscription population from a contract-terms extract, reconcile the recomputation to the
RevPro schedule, investigate every contract whose difference exceeds a threshold, and support the extract's
completeness and accuracy by agreeing 40 contracts' key fields to the signed order forms. Note the residual
limitation in Exhibit 5-17's fourth row: if your contract-terms extract draws service start dates from the same
Zuora record RevPro used, your recomputation cannot detect a wrong start date. That is why the walkthrough below
agrees the start date to the order form and to the provisioning log, not to Zuora.

## 5.12 Multi-Currency Subscription Revenue

AtlasFlow contracts through three selling entities with three functional currencies: the parent in USD, the UK
entity in GBP, and the Australian entity in AUD. Contract C-2 with Voltaire Logistics S.A. is denominated in a
fourth currency — €1,480 — and is held by the UK entity. Three measurement questions follow, and they are
frequently answered wrongly in sequence.

**First, measure the transaction in the functional currency at the transaction date.** ASC 830-10 requires a
foreign-currency transaction to be recorded in the functional currency using the exchange rate on the
transaction date. At the October 1, 2025 EUR/GBP spot rate of 0.8615, €1,480 is **£1,275**. The allocation from
Exhibit 5-4 is applied to the GBP amount: £1,275 × 92.438% = £1,178.6 to the subscription and £1,275 × 7.562% =
£96.4 to the material right, summing to £1,275.0.

**Second, the transaction price is not remeasured for later currency movements.** The subscription revenue
recognized each month is a fraction of a fixed GBP amount established at inception. If the EUR strengthens, the
GBP-measured revenue does not change; what changes is the GBP value of the EUR receivable, which is a monetary
item and is remeasured through earnings.

**Third, translation into USD is a separate step and does not touch earnings.** The UK entity's GBP statements
are translated for consolidation: revenue at the rate in effect when recognized (in practice an appropriate
average), assets and liabilities at the December 31, 2025 rate of 1.2680 USD/GBP, with the difference to the
cumulative translation adjustment in accumulated other comprehensive loss (account 3200, $(1,105)).

**Exhibit 5-18. C-2 currency effects, October 1 to December 31, 2025.**

| Item | Oct 1, 2025 | Dec 31, 2025 | Change | Where it goes |
| --- | --- | --- | --- | --- |
| EUR/GBP spot | 0.8615 | 0.8710 | +1.10% | — |
| GBP/USD spot | 1.2549 | 1.2680 | +1.04% | — |
| Contract transaction price, EUR | €1,480 | €1,480 | — | Fixed by contract |
| Transaction price measured in GBP | £1,275.0 | £1,275.0 | — | Fixed at inception; not remeasured |
| Year-1 invoice, EUR | €740 | €740 | — | — |
| Carrying amount of the EUR receivable, GBP | £637.5 | £644.5 | £7.0 | Transaction gain in the UK entity's earnings (account 7300) |
| USD equivalent of the EUR receivable | $800.0 | $817.2 | $17.2 | £7.0 gain translated ($8.9) plus $8.3 of translation adjustment to OCI |

The trap is the fourth row. A contract liability is a **non-monetary** item: it will be settled by delivering
service, not currency, so ASC 830-10-45 does not remeasure it. If AtlasFlow had remeasured C-2's contract
liability of £489.0 at the December 31 EUR/GBP rate, it would have restated the balance to £489.0 × (0.8710 ÷
0.8615) = £494.4 and recorded a £5.4 loss — approximately $6.8 — that does not exist. Chapter 6, §6.10 develops
the liability-side mechanics and the population-level test; here the point is that the *revenue* recognized each
month is fixed in the functional currency at inception and is therefore recomputable without any reference to
later rates.

## Step-by-Step Walkthrough: Independently Recomputing FY2025 Revenue for Contract C-1 and Reconciling to the Zuora Revenue Schedule

Objective: form an independent expectation of FY2025 revenue for contract C-1 (Meridian Health Systems) from
the contract document, and reconcile it to the Zuora Revenue schedule and to the general ledger. Workpaper
reference WP 5200-11. Performed by Amelia Trent (staff), reviewed by Omar Haddad (manager).

**Step 1. Obtain the signed contract, not the system record.** Request from Brett Hallowell's team the executed
order form dated March 12, 2025, its Exhibit A (subscription schedule), its Exhibit B (professional services
statement of work and training package), the master subscription agreement in force, and every amendment
through December 31, 2025. Confirm the document is fully executed by both parties. *What you compare it to:* the
Salesforce opportunity record and the Zuora Billing subscription record. *Conclusion supported:* the contract
exists and its terms are the terms you will use. *If unexpected:* if the Zuora record's terms differ from the
order form, stop and treat the difference as a potential misstatement, not a data-entry note; the order form
governs. If no countersignature exists, escalate to Chapter 4, §4.3's enforceability analysis.

**Step 2. Extract the contract terms onto a schedule and have a second person agree them.** Fields to capture:
contract signature date (March 12, 2025); subscription start and end dates (March 15, 2025 and March 14, 2028);
seat count (500); Core annual amounts (600 / 840 / 960); Insight annual amount and its start (180, contract
years 2 and 3 only); professional services fee and its two components ($360, split between implementation and
five training sessions); billing schedule (annually in advance on each anniversary; services 50% on signature,
50% on go-live); included run volume and basis (200,000 per contract year, cumulative annual); overage rate
($12 per 1,000 runs); termination provisions (none for convenience); currency (USD). *If unexpected:* a
termination-for-convenience clause discovered here changes the transaction price and the RPO — see §5.10 and
Chapter 6, §6.11.

**Step 3. Establish the revenue start date from evidence outside Zuora.** Obtain the provisioning record from
the AtlasFlow platform administration log showing the date Meridian's production tenant was activated. For C-1
the tenant was activated March 15, 2025, which equals the contractual start date, so the later of the two is
March 15, 2025. *Why this step exists:* corrected misstatement C-1 in the FY2025 file arose on 14 Q1 contracts
where revenue began on the contractual start date of March 15 rather than the April 2 provisioning date, a $410
income effect. C-1 Meridian is not among those 14. *If unexpected:* if the provisioning date is later than the
contract date, the revenue start date moves and every subsequent step recomputes.

**Step 4. Identify the performance obligations and document the two ASC 606-10-25-19 tests.** Reproduce
Exhibit 5-2. Four performance obligations. *If unexpected:* if the statement of work in Exhibit B describes
construction of a customer-specific integration maintained in AtlasFlow's code base, PO 3 is not distinct and
collapses into PO 1, which moves $279.9 of allocated consideration from a four-month recognition pattern to a
1,096-day one. Holding the allocation constant, FY2025 revenue on PO 3 would fall from $279.9 to
$279.861 × 292/1,096 = $74.6, a reduction of approximately $205 on this contract alone. Read Exhibit B; do not
skim it.

**Step 5. Determine each SSP and document the evidence.** Reproduce Exhibit 5-9. For PO 1, agree the $1,800 per
seat per year to the standalone-sale extract and to the March 2025 price list; for PO 2, obtain management's SSP
memo and perform the §5.6 procedures; for PO 3, agree the 1,240-hour estimate to the statement of work and the
$250 blended rate to the services rate card; for PO 4, agree $10.000 per session to the FY2025 services
catalog. *If unexpected:* if any SSP in the RevPro SSP table differs from management's memo, you have an input
error affecting every contract that uses it, not a single-contract issue. Query the SSP table's effective-dated
history.

**Step 6. Compute the transaction price.** $2,400 + $360 + $360 = $3,120. Confirm there is no variable
consideration to include at inception: the overage is usage-based and is allocated to the distinct daily
services as consumed (§5.10), there are no SLA credits in C-1, and there are no rebates or penalties. *If
unexpected:* a performance bonus, an early-adopter rebate, or a most-favored-pricing clause is variable
consideration that must be estimated and constrained (Chapter 4, §4.6).

**Step 7. Allocate on a relative SSP basis and prove the total.** Reproduce Exhibit 5-10. Allocation factor
$3,120 ÷ $3,456 = 0.9027778. Allocated amounts $2,437.500 / $357.500 / $279.861 / $45.139 summing to
$3,120.000. Place a tick mark on the total confirming it equals the transaction price; an allocation that does
not sum to the transaction price is an arithmetic failure, and it happens.

**Step 8. Evaluate the discount-allocation exception explicitly.** Apply the three criteria of
ASC 606-10-32-37. Conclude, with the 2.6% standalone-sale frequency as the reason, that criterion one fails.
Document the $24.9 FY2025 effect of the alternative (Exhibit 5-11) so the reviewer can see the amount at risk.

**Step 9. Build the recognition pattern for each obligation.** Reproduce Exhibit 5-12. For PO 1 compute the
daily rate: $2,437,500 ÷ 1,096 days = $2,223.9964, or $2,224.00 rounded to the cent. Verify the day count: from
March 15, 2025 to March 14, 2028 is 365 + 365 + 366 = 1,096 days, the third year including February 29, 2028.

**Step 10. Compute FY2025 revenue for PO 1 as a monthly waterfall.** Count days of service in each calendar
month from March 15 to December 31, 2025.

| Month | Days of service | Daily rate | Revenue |
| --- | --- | --- | --- |
| March 2025 (15th–31st) | 17 | 2,224.00 | 37,808 |
| April 2025 | 30 | 2,224.00 | 66,720 |
| May 2025 | 31 | 2,224.00 | 68,944 |
| June 2025 | 30 | 2,224.00 | 66,720 |
| July 2025 | 31 | 2,224.00 | 68,944 |
| August 2025 | 31 | 2,224.00 | 68,944 |
| September 2025 | 30 | 2,224.00 | 66,720 |
| October 2025 | 31 | 2,224.00 | 68,944 |
| November 2025 | 30 | 2,224.00 | 66,720 |
| December 2025 | 31 | 2,224.00 | 68,944 |
| **FY2025 total, PO 1** | **292** | | **649,408** |

Amounts are in whole dollars. Cross-check: 292 × $2,224.00 = $649,408.

**Step 11. Compute FY2025 revenue for PO 2.** The Insight service period begins March 15, 2026. FY2025 revenue
is **nil**, and $357,500 of allocated consideration relates to an obligation not yet commenced. *If unexpected:*
if the RevPro schedule shows Insight revenue in FY2025, the engine has taken the subscription start date from
the contract header rather than from the Insight rate-plan charge's own effective date — a configuration error
affecting every contract with a non-coterminous element.

**Step 12. Compute FY2025 revenue for PO 3 from the hours records.** Obtain the professional services time
detail from the PSA time export for engagement ENG-2025-0417. Hours incurred: April 300, May 420, June 330,
July 190; total 1,240 against an estimate of 1,240, so the engagement is complete and 100% of the allocated
amount is recognized.

| Month | Hours | Cumulative % complete | Revenue at $225.6944 per hour |
| --- | --- | --- | --- |
| April 2025 | 300 | 24.19% | 67,708.33 |
| May 2025 | 420 | 58.06% | 94,791.67 |
| June 2025 | 330 | 84.68% | 74,479.17 |
| July 2025 | 190 | 100.00% | 42,881.94 |
| **Total** | **1,240** | | **279,861.11** |

*If unexpected:* if actual hours exceed the estimate, the input measure denominator changes and cumulative
revenue must be recomputed on the revised estimate; if hours were incurred in FY2026, part of the fee belongs
to FY2026. Uncorrected misstatement U-4 in the FY2025 file ($95, contract asset understated) arose from exactly
this input-estimate mechanic on other engagements.

**Step 13. Compute FY2025 revenue for PO 4 from the training delivery log.** Sessions delivered: June 18, 2025;
August 12, 2025; October 7, 2025. Two sessions remained scheduled for February and April 2026. Revenue = 3 ÷ 5
× $45,138.89 = **$27,083.33**; $18,055.56 remains deferred. *If unexpected:* if the delivery log shows a
session on December 30, 2025 that the trainer's calendar shows on January 6, 2026, you have a cut-off error
worth $9,027.78 on this contract and a control question about the delivery log.

**Step 14. Compute FY2025 usage overage.** Reproduce Exhibit 5-16. Cumulative runs at December 31, 2025 of
186,000 against a cumulative annual commitment of 200,000; overage revenue **nil**. Agree the 186,000 to the
Zuora Billing usage records and to the Snowflake usage table.

**Step 15. Sum the independent expectation.**

| Performance obligation | FY2025 revenue | GL account |
| --- | --- | --- |
| PO 1 — Core subscription | 649,408.00 | 4100 |
| PO 2 — Insight subscription | — | 4110 |
| PO 3 — Implementation | 279,861.11 | 4200 |
| PO 4 — Training | 27,083.33 | 4200 |
| Usage overage | — | 4120 |
| **Total FY2025 revenue, contract C-1** | **956,352.44** | |

**Step 16. Obtain the RevPro schedule and compare.** Run the "Revenue Contract Detail" report in Zuora Revenue
for revenue contract RC-0004182 (Meridian), periods January through December 2025, with columns for performance
obligation, allocated amount, revenue recognized in period, and cumulative revenue. RevPro reported FY2025
revenue of **$963,024.44** against your $956,352.44 — a difference of **$6,672.00**, which is 0.7% of the
contract's FY2025 revenue and 9.3% of the clearly trivial threshold of $72.

**Step 17. Decompose the difference by performance obligation before investigating it.**

| Performance obligation | Your computation | RevPro | Difference |
| --- | --- | --- | --- |
| PO 1 — Core | 649,408.00 | 656,080.00 | 6,672.00 |
| PO 2 — Insight | — | — | — |
| PO 3 — Implementation | 279,861.11 | 279,861.11 | — |
| PO 4 — Training | 27,083.33 | 27,083.33 | — |
| **Total** | **956,352.44** | **963,024.44** | **6,672.00** |

The difference is entirely in PO 1 and is exactly 3 × $2,224.00. Three days.

**Step 18. Identify the cause at the field level.** Query the Zuora Billing subscription record's
`ServiceActivationDate` and `ContractEffectiveDate` for subscription A-S00041823. `ContractEffectiveDate` is
2025-03-12, the order-form signature date; `ServiceActivationDate` is blank; RevPro's revenue-start-date rule
falls back to `ContractEffectiveDate` when `ServiceActivationDate` is null. Revenue therefore began March 12
instead of March 15. *Conclusion supported:* a $6,672 overstatement of FY2025 revenue on C-1 caused by a null
field, not by a configuration defect in the allocation logic.

**Step 19. Determine whether the condition is isolated.** Ask Tara Iyer to run the population query:

```sql
SELECT s.subscription_number,
       s.contract_effective_date,
       s.service_activation_date,
       s.subscription_start_date,
       DATEDIFF('day', s.contract_effective_date, s.subscription_start_date) AS days_early,
       r.allocated_amount / NULLIF(r.term_days, 0) AS daily_rate,
       DATEDIFF('day', s.contract_effective_date, s.subscription_start_date)
         * (r.allocated_amount / NULLIF(r.term_days, 0))                     AS potential_overstatement
FROM   zuora_billing.subscription       s
JOIN   revpro.performance_obligation    r ON r.subscription_number = s.subscription_number
WHERE  s.service_activation_date IS NULL
  AND  s.subscription_start_date > s.contract_effective_date
  AND  s.subscription_start_date BETWEEN '2025-01-01' AND '2025-12-31'
ORDER BY potential_overstatement DESC;
```

The query returned 27 subscriptions with a null `ServiceActivationDate` and a start date later than the
contract effective date. Aggregate potential overstatement: **$14** (in thousands), of which C-1 is $6.7. *If
unexpected:* had the query returned 700 subscriptions and $480, this would cease to be a clearly trivial item
and would become a probable material weakness in the revenue application controls, because the condition would
mean the revenue-start-date rule is systematically wrong.

**Step 20. Evaluate and dispose.** $14 is below the $72 clearly trivial threshold, so it is not accumulated on
the summary of audit differences (Chapter 19, §19.3). It is nonetheless a control matter: the RevPro fallback
rule combined with an unvalidated Zuora field means service dates are not controlled. Report it to management
in writing and evaluate it with the other revenue application control observations under Chapter 14, §14.9.
Do not let "below clearly trivial" end the analysis; the misstatement is trivial and the deficiency may not be.

**Step 21. Reconcile the contract to the general ledger.** Agree C-1's revenue by account to the RevPro
"Revenue Contract Summary" that supports the interface I-3 monthly journal, and confirm the contract's amounts
are included in the December 2025 journal reviewed and approved by the Controller before posting. Place tick
mark (a) on the amounts agreed to RevPro and tick mark (b) on the amounts agreed to the NetSuite account detail.

**Step 22. Compute the contract's balance-sheet position and hand it to the deferred revenue file.** Billings
through December 31, 2025: Core year 1 $600,000 (invoiced March 12, 2025) plus professional services $360,000
(50% March 2025, 50% July 2025) = $960,000. Revenue recognized (your computation) $956,352.44. Net contract
liability = **$3,647.56**. Cross-reference to WP 6100-08, the contract-level deferred revenue recomputation in
Chapter 6, §6.6.

## Extended Case Study: Auditing the AtlasFlow Insight Standalone Selling Price

### Background

AtlasFlow launched the Insight analytics module in January 2025 as a separately priced SKU. By December 31, 2025
Insight had generated $26,700 of FY2025 revenue and appeared in approximately 1,180 customer contracts. Because
Insight is a separate performance obligation in nearly every contract that contains it, its standalone selling
price drives the allocation of the transaction price in that entire population. The engagement team identified
the Insight SSP as one of the five most judgmental FY2025 estimates (case §4.5) and, in the audit plan, as a
significant risk at the accuracy assertion for subscription revenue.

### The Facts

- Insight list price is $480 per automation seat per year. Management's SSP for FY2025 is $396 per seat per
  year, or 82.5% of list.
- Management derived 82.5% by equally weighting an adjusted market assessment of 89.0% of list and an expected
  cost plus a margin of 76.0% of list (Exhibit 5-5).
- Thirty-one standalone Insight sales occurred in FY2025 with a median of 82.5% of list, a mean of 81.8%, and
  an interquartile range of 22.0 points of list (Exhibit 5-6). The median of the 31 sales is numerically
  identical to management's weighted conclusion.
- Eight of the 31 observations failed Brightline's standalone-qualification criteria (Exhibit 5-7). On the
  remaining 23, the median is 81.0% and the interquartile range 21.0 points.
- The price band is not stationary. The seven H1 2025 standalone sales averaged 97.9% of list; the 24 H2 sales
  averaged 77.2%.
- The SSP memo was authored by Aisha Bello, Director of Technical Accounting, and approved by Daniel Kim, VP
  Revenue Accounting, who has been on a performance plan since March 2025 and who owns the RevPro
  configuration. Two revenue accountants resigned in Q2 2025.

### What the Engagement Team Did

1. Obtained the SSP memo and its version history from the FloQast evidence repository. Three versions exist,
   dated October 14, November 3, and December 19, 2025. Version 1 weighted the adjusted market assessment at
   70% and cost-plus at 30%, producing 85.1% of list. Version 3 changed the weighting to 50/50, producing
   82.5%. The stated reason for the change was "alignment with observable standalone sales."
2. Obtained the full 31-observation population from Snowflake, agreed the count to Zuora Billing order records,
   and re-performed the percentile statistics independently in a spreadsheet controlled by the engagement team.
3. Inspected all 31 order forms and applied the three disqualification criteria, producing Exhibit 5-7.
4. Tested the two estimation approaches. For the adjusted market assessment, inspected the competitor pricing
   file and found three comparables, one of which was priced per user and two per data volume; requested
   management's normalization workings and found none for one comparable. For expected cost plus a margin,
   agreed the $36.50 annual cost to serve to a Snowflake query of Insight-attributable hosting and support cost
   divided by average Insight tenants, and agreed the 80.0% target margin to AtlasFlow's actual FY2025
   subscription gross margin of $108,640 ÷ $135,800 = 80.0%.
5. Stratified the FY2025 population of 412 multi-element contracts containing Insight by their sensitivity to
   the SSP, and measured the revenue effect of alternative SSPs.
6. Consulted the national office professional practice director, Priya Chandrasekhar, on the acceptability of
   an equal weighting whose result coincides exactly with the corroborating statistic.

### Analysis

The team first quantified the effect of alternative SSPs on a single contract to establish the mechanism, using
C-1 Meridian.

**Exhibit 5-19. Sensitivity of contract C-1 FY2025 revenue to the Insight SSP (in thousands).**

| Scenario | Insight SSP (% of list) | Insight SSP, 24 months | Allocated to Insight | Allocated to Core | C-1 FY2025 revenue | Difference from recorded |
| --- | --- | --- | --- | --- | --- | --- |
| A — Management, equal weighting | 82.5% | 396.00 | 357.500 | 2,437.500 | 956.352 | — |
| B — Median of the 23 qualifying standalone sales | 81.0% | 388.80 | 351.733 | 2,442.589 | 958.348 | 1.996 |
| C — Expected cost plus a margin alone | 76.0% | 364.80 | 332.334 | 2,459.706 | 965.064 | 8.712 |
| D — Adjusted market assessment alone | 89.0% | 427.20 | 382.216 | 2,415.692 | 947.795 | (8.557) |
| E — Residual approach (prohibited, §5.5.1) | 12.5% | 60.00 | 60.000 | 2,700.000 | 1,059.342 | 102.990 |

Each scenario's four allocated amounts sum to the $3,120.000 transaction price; the table shows two of the four
columns. Scenario C in full: Core $2,459.706, Insight $332.334, implementation $282.411, training $45.550, which
sum to $3,120.001 before the engine's final-period rounding adjustment.

The relationship is monotonic and counterintuitive: **a lower Insight SSP produces higher FY2025 revenue.**
Insight's service period on C-1 does not begin until March 15, 2026, so consideration allocated to Insight is
deferred in full, while consideration allocated away from Insight lands on obligations already being satisfied.
Between scenarios C and D — the two approaches management itself used, taken singly — FY2025 revenue on this one
contract moves by $17.3, or 1.8%.

The team then scaled the sensitivity to the population.

**Exhibit 5-20. FY2025 revenue sensitivity by contract stratum (in thousands, except per-point amounts).**

| Stratum | Description | Contracts | Aggregate transaction price | Sensitivity per 1 point of SSP | Effect of a 6.5-point SSP increase |
| --- | --- | --- | --- | --- | --- |
| 1 | Insight coterminous with Core; no professional services obligation | 214 | 22,600 | — | — |
| 2 | Insight coterminous with Core; a professional services obligation recognized earlier | 143 | 38,300 | (3.11) | (20.2) |
| 3 | Insight not coterminous with Core (starts later or ends earlier) | 55 | 18,000 | (7.60) | (49.4) |
| **Total** | | **412** | **78,900** | **(10.71)** | **(69.6)** |

Stratum 1 is insensitive by construction: Core and Insight are recognized ratably over the same period, so
moving consideration between them changes nothing in any period. Stratum 3's sensitivity of $(7.60) per point
was measured directly from C-1 ($8.557 ÷ 6.5 points = $1.316 per point on a $3,120 transaction price, or
0.04219% of transaction price per point, applied to $18,000). Stratum 2's $(3.11) per point was measured on a
sample of 12 contracts and equals 0.00812% of transaction price per point.

The defensible range for the Insight SSP is 76.0% to 89.0% of list — the two approaches management applied,
each taken alone. Management's 82.5% sits at the midpoint. Moving to either end changes FY2025 subscription
revenue by approximately $70 ($10.71 × 6.5 points = $69.6), a total spread of $139. Against performance
materiality of $940 that spread is 14.8%; against overall materiality of $1,450 it is 9.6%. A misstatement
cannot be material at any point in the defensible range.

Three further conclusions follow that the quantification alone does not deliver:

- **The memo's version history is an indicator of possible management bias, not an error.** Changing the
  weighting to reach a number that matches the corroborating statistic reverses the logic of corroboration.
  The national office's position was that a 50/50 weighting is defensible on its own terms — neither approach
  is demonstrably superior — but that the stated *reason* for the change is not, and that the team must
  evaluate the change alongside the other indicators of bias in the FY2025 file (Chapter 19, §19.4). The
  engagement team documented the memo history and concluded that the estimate falls within a range of
  reasonable estimates notwithstanding the process weakness.
- **The population management represented as standalone was 25.8% not standalone**, and management had
  performed no qualification testing. That is a deficiency in the control over the SSP estimate, evaluated
  under Chapter 14, §14.9.
- **The non-stationary price band is a FY2026 problem.** If H2's 77.2% average is the better estimate of the
  price at which AtlasFlow would sell Insight separately going forward, the FY2026 SSP will fall, and the
  FY2026 population of Insight-bearing contracts will be materially larger. The team included this in the
  matters carried forward to the FY2026 planning file.

### Resolution and Conclusion

Management retained its SSP of 82.5% of list. Brightline concluded the estimate is within a range of reasonable
estimates and that no misstatement requires accumulation. The team concluded that the SSP process contained a
control deficiency (no qualification testing of the standalone population; no documented basis for the change
in weighting) that, individually, is a deficiency rather than a significant deficiency, on the basis that the
maximum potential misstatement across the defensible range is $140 against performance materiality of $940 and
the deficiency was compensated in part by the Controller's review of the allocation output. The Insight SSP was
communicated to the audit committee as a significant estimate and became one of the FY2025 critical audit
matters (Chapter 20, §20.6). A CAM does not require an identified material misstatement; it requires a matter
involving especially challenging, subjective, or complex auditor judgment relating to a material account, and
the Insight allocation qualifies on both limbs even though the quantified exposure is well below materiality.

### Workpaper Extract

```text
================================================================================
BRIGHTLINE LLP                                              WP REF:  5400-12
AtlasFlow, Inc.                                             PERIOD:  FY2025
Audit of the financial statements and of ICFR                YEAR END: 12/31/2025
--------------------------------------------------------------------------------
SUBJECT:  Evaluation of the standalone selling price of the AtlasFlow Insight
          module and its effect on the allocation of transaction price

PREPARED BY:  A. Trent (AMT)          DATE PREPARED:  01/16/2026
              J. Park (JWP)                           01/19/2026
REVIEWED BY:  O. Haddad (OMH)         DATE REVIEWED:  01/23/2026
              G. Lindqvist (GRL)                      01/28/2026
PARTNER:      D. Whitcombe (DGW)                      02/04/2026
CONSULTED:    P. Chandrasekhar, National Office       01/26/2026
--------------------------------------------------------------------------------
PURPOSE
To evaluate whether management's standalone selling price (SSP) for the Insight
module, 82.5% of list price ($396 per automation seat per year), is reasonable
under ASC 606-10-32-32 through 32-35, and to quantify the effect on FY2025
subscription revenue of alternative SSPs within the range of reasonable
estimates. Relevant assertion: accuracy of subscription revenue (account 4110
and, through allocation, account 4100). Assessed as a significant risk per
WP 2100-04.

SOURCE OF INFORMATION
(1) Management SSP memorandum, versions 1-3 (10/14/2025, 11/03/2025, 12/19/2025),
    prepared by A. Bello, approved by D. Kim; obtained from FloQast, evidence
    ID FQ-2025-11487.
(2) Standalone Insight sales population, 31 records, Snowflake query
    BL_SSP_STANDALONE_FY25 executed 01/09/2026; record count agreed to Zuora
    Billing order report ZB-ORD-1188.                                       (a)
(3) All 31 executed order forms, obtained from the Salesforce contract
    repository 01/12/2026.
(4) Insight-attributable cost query BL_INSIGHT_COST_FY25; FY2025 subscription
    gross margin per audited statement of operations.                       (b)
(5) Population of 412 FY2025 multi-element contracts containing Insight,
    Snowflake query BL_MULTIELEMENT_FY25.                                   (a)

PROCEDURES PERFORMED
1. Re-performed all percentile statistics on the 31-observation population in an
   engagement-controlled workbook; agreed median 82.5%, mean 81.8%, Q1 71.0%,
   Q3 93.0%, interquartile range 22.0 points, standard deviation 12.7 points.
2. Inspected all 31 order forms against three standalone-qualification criteria
   (order form within 90 days of a Core order; same order form as a Core
   renewal; price set by a reseller). 8 of 31 failed.                        (c)
3. Recomputed the expected-cost-plus-a-margin approach: $36.50 annual cost to
   serve / (1 - 0.800) = $182.50 = 76.0% of $240 list per 500-seat
   configuration.                                                            (b)
4. Evaluated the adjusted market assessment: 3 comparables inspected; 1 lacked
   documented normalization for a per-data-volume pricing basis.             (d)
5. Recomputed the allocation of contract C-1 under five SSP scenarios; each
   allocation proved to the $3,120 transaction price.
6. Stratified the 412-contract population by SSP sensitivity and measured the
   per-point revenue effect (Exhibit 5-20 of the audit file).
7. Obtained and read the memo version history; inquired of A. Bello and D. Kim
   regarding the change in weighting from 70/30 to 50/50.                    (e)
8. Computed sample sufficiency: standard error of the mean 2.28 points;
   95% confidence interval on the mean 77.4% to 86.3% of list.

RESULTS
- Defensible SSP range: 76.0% to 89.0% of list. Management's 82.5% is at the
  midpoint of that range.
- FY2025 subscription revenue effect at the extremes of the range: +$70 / -$70,
  a spread of $139 (14.8% of performance materiality of $940).
- No misstatement identified requiring accumulation on the SAD.
- Deficiency identified: management performed no qualification testing of the
  standalone-sale population (8 of 31 observations, 25.8%, did not qualify), and
  the change in approach weighting in version 3 is documented only as
  "alignment with observable standalone sales."                             (c)(e)
- Bias indicator noted and carried to WP 9200-03 (evaluation of qualitative
  aspects of accounting practices).                                          (e)

CONCLUSION
Management's Insight SSP of 82.5% of list is within a range of reasonable
estimates and the allocation of transaction price using that SSP does not give
rise to a material misstatement of FY2025 revenue. The estimation process
contains a control deficiency that is not a significant deficiency
individually; it is aggregated with other revenue application control
observations at WP 8400-02. The matter is a critical audit matter candidate and
was communicated to the audit committee on 02/06/2026.

TICK MARK LEGEND
(a) Agreed record count and aggregate amount to the source system report;
    completeness and accuracy of IPE tested at WP 1800-06.
(b) Agreed to the audited statement of operations.
(c) Exception noted; see RESULTS.
(d) Inquiry made; management's response documented at WP 5400-12.3.
(e) Indicator of possible management bias; evaluated at WP 9200-03.
================================================================================
```

### Lessons

1. **Quantify before you conclude.** "Highly judgmental" is not a conclusion. The range was 13 points of list;
   13 points was worth $139; $139 was 14.8% of performance materiality. That sentence is the audit.
2. **An exact match between an estimate and its corroboration is evidence about the process, not about the
   estimate.** Ask for version history on every judgmental memo.
3. **Test the population's qualification, not only its statistics.** A quarter of the observations were not
   standalone sales, and no amount of percentile arithmetic would have revealed it.
4. **Direction matters and is often counterintuitive.** A lower SSP on a later-commencing obligation increases
   current revenue. If you assume that conservatism runs one way, you will design the wrong test.
5. **A conclusion that the estimate is reasonable and a conclusion that the control is effective are different
   conclusions.** Both must be reached, and here they diverged.

## Common Mistakes

### Mistake 5.1 — Recognizing the invoiced amount on a ramped contract

**What it looks like.** FY2025 Core revenue on C-1 of $480.0 (the $600 year-1 invoice prorated for 292 of 365
days) instead of $649.4 — a $169.4 understatement on one contract — or a revenue schedule whose annual amounts are
600 / 840 / 960.

**Why it happens.** The invoice is the most visible document in the file, the billing system produces it, and
"revenue equals what we billed, spread over the year" is intuitive and usually harmless on flat contracts. On
34% of AtlasFlow's ACV it is not harmless.

**What goes wrong.** The measure of progress for a stand-ready service is time, and the amount to be spread is
the allocated transaction price for the whole obligation, not the current invoice. The error understates
early-year revenue and overstates late-year revenue, and it eliminates the contract asset that a ramp
necessarily creates.

**How to avoid it.** Build every recomputation from the total consideration for the performance obligation and
the total days of its service period. Then compare the result to invoicing as a *diagnostic*: a nonzero
cumulative difference is expected on a ramp, and a zero difference on a ramped contract is the error signal.

### Mistake 5.2 — Treating a separately invoiced setup fee as a performance obligation

**What it looks like.** A $40 "activation fee" line on an order form given its own SSP, its own allocation, and
point-in-time recognition on the provisioning date.

**Why it happens.** The fee is separately priced and separately invoiced, and separate pricing feels like
separate performance.

**What goes wrong.** ASC 606-10-25-17 excludes administrative setup activities that transfer no good or service
to the customer. Provisioning a tenant in a multi-tenant environment transfers nothing the customer did not
already contract for. Recognizing the fee up front accelerates revenue; the fee belongs in the transaction price
allocated across the real obligations.

**How to avoid it.** Ask what the customer receives that it would not receive without the activity. If the
answer is "nothing — the platform simply becomes usable," it is not a performance obligation regardless of how
it is priced.

### Mistake 5.3 — Using the residual approach because it is arithmetically convenient

**What it looks like.** A memo stating that Insight's SSP was determined "as the residual after deducting the
observable standalone selling prices of the other elements," with no analysis of whether Insight's selling
price is highly variable and no reasonableness check on the result.

**Why it happens.** The residual approach requires no estimate and always makes the allocation foot.

**What goes wrong.** On C-1 the residual is $60 for 24 months, 12.5% of list, against an observed standalone
band of 58% to 100%. ASC 606-10-32-35 prohibits the result. The error accelerated $103 of revenue on one
contract because it starved the not-yet-commenced obligation.

**How to avoid it.** Before applying the residual approach, document which of the two permitting conditions is
met. After applying it, compare the residual to the observable band and reject it if it falls outside.

### Mistake 5.4 — Testing the engine's configuration and calling it a test of revenue

**What it looks like.** A workpaper that inspects 27 RevPro configuration rules, re-performs a test of one on
each, concludes "the revenue engine operates as designed," and performs no recomputation of revenue.

**Why it happens.** Configuration testing is efficient and feels definitive. One test of one appears to cover
thousands of contracts.

**What goes wrong.** An automated control conclusion is only as good as the general controls over the
application. AtlasFlow has four local administrator accounts in Zuora Revenue, one shared (W-1), and two
developers with standing write access to production configuration (W-6). Neither the configuration's stability
nor the integrity of the inputs it consumes — SSP tables, service dates, amendment type codes — is established
by inspecting the rule.

**How to avoid it.** Decide the reliance question first (Chapter 12, §12.7). Where ITGCs are deficient, the
substantive strategy must stand alone: recompute from contract data, and support the extract's completeness and
accuracy against signed documents rather than against the same system.

### Mistake 5.5 — Accepting a standalone-sale population without qualifying each observation

**What it looks like.** A schedule of 31 "standalone sales" with quartiles computed to one decimal place and no
evidence that any order form was read.

**Why it happens.** The population arrives as a spreadsheet from management, statistics are easy to re-perform,
and re-performing them feels like testing.

**What goes wrong.** Eight of AtlasFlow's 31 observations were not standalone sales: two shared an order form
with a Core renewal, four were signed within 90 days of a Core order, one was priced by a reseller, and one was
signed nine days after a Core order. A quarter of the evidence base did not exist.

**How to avoid it.** Define disqualification criteria before you look at the data, apply them to 100% of the
population when it is small enough to permit it, and document each exclusion with the criterion that caused it.

### Mistake 5.6 — Computing overage as annual consumption less annual commitment at an interim date

**What it looks like.** A December 31 workpaper showing Meridian's overage as (244,000 − 200,000) ÷ 1,000 × $12
= $528, and a proposed misstatement because AtlasFlow recorded nothing.

**Why it happens.** The continuing case states annual consumption and an annual commitment; subtracting them is
the obvious move.

**What goes wrong.** The 244,000 runs span the contract year ending March 14, 2026. Cumulative consumption at
December 31, 2025 was 186,000, below the commitment, so nothing had been earned. Proposing $528 of revenue —
or, worse, proposing an accrual for a contract year not yet complete — asserts revenue that does not exist.

**How to avoid it.** Establish the measurement period from the contract clause first: annual cumulative,
annual with a true-up, or monthly non-cumulative. Then cut the consumption data at the balance sheet date, not
at the contract anniversary.

### Mistake 5.7 — Defaulting every amendment to a single treatment

**What it looks like.** A subledger in which every amendment produces a cumulative catch-up entry, or one in
which none does.

**Why it happens.** A configuration rule keyed to a single amendment type code is simpler to build and to
maintain than one that reflects three outcomes, and the person selecting the code in Salesforce CPQ is a
salesperson optimizing for speed.

**What goes wrong.** Renewals treated as cumulative catch-ups reprice services already delivered; concessions
treated as prospective leave overstated revenue in prior periods. Both distort the current period, and the
direction depends on the mix.

**How to avoid it.** Reconcile the amendment population by type code to the catch-up entries in the subledger.
Any catch-up on an amendment coded as a renewal, and any concession with no catch-up, is an exception to
investigate. Read the amendment, not the code.

### Mistake 5.8 — Recomputing revenue from the system's own service dates

**What it looks like.** A full-population recomputation that reproduces the engine's answer to the dollar and
concludes revenue is accurate.

**Why it happens.** A recomputation that agrees exactly is satisfying, and the contract-terms extract is easier
to obtain from Zuora than from 3,140 order forms.

**What goes wrong.** If the extract's service start date is the same field RevPro used, the recomputation
cannot detect a wrong start date. Brightline's $6,672 difference on C-1 was found only because Step 3 of the
walkthrough obtained the provisioning date from the platform administration log rather than from Zuora.

**How to avoid it.** Source at least one independent field for the recomputation, and agree service dates for a
sample to the signed order form and to a provisioning record outside the billing system. An exact
full-population agreement should raise your suspicion, not lower it.

### Mistake 5.9 — Remeasuring a foreign-currency contract liability

**What it looks like.** A month-end FX revaluation job that includes deferred revenue accounts 2400, 2405, and
2410, generating a translation gain or loss in account 7300.

**Why it happens.** The revaluation job is configured by account range, and deferred revenue is a liability.

**What goes wrong.** A contract liability is non-monetary: it is settled by delivering service, not currency.
Remeasuring C-2's £489.0 liability at the December 31 EUR/GBP rate would have produced a £5.4 (approximately
$6.8) loss that does not exist, and it would have made the remaining revenue on the contract irreconcilable to
the inception measurement.

**How to avoid it.** Obtain the revaluation job's account list and confirm deferred revenue is excluded. Then
prove it: recompute one foreign-currency contract's remaining revenue from the inception rate and agree it to
the schedule.

### Mistake 5.10 — Concluding on SSP reasonableness without quantifying the range

**What it looks like.** "We evaluated management's SSP methodology, inspected the supporting analysis, and
concluded the SSP is reasonable."

**Why it happens.** The estimate is genuinely judgmental, quantifying alternatives takes a day of work, and the
conclusion sounds finished.

**What goes wrong.** You cannot know whether the estimate matters without measuring what it is worth. Had the
Insight population been seven times larger, the same range would have exceeded performance materiality and the
same conclusion would have been unsupported. The file would look identical.

**How to avoid it.** Compute the range of defensible values, translate it into a revenue effect using a
population sensitivity, and compare that effect to performance materiality. Three numbers, one paragraph.

### Mistake 5.11 — Treating the series conclusion as a policy election

**What it looks like.** A policy memo stating "the Company accounts for its subscriptions as a single
performance obligation comprising a series of distinct daily services," with no analysis and no reconsideration
when contract shapes change.

**Why it happens.** The conclusion is correct for the standard 12-month flat contract, so it becomes boilerplate.

**What goes wrong.** The series criteria require the distinct services to be substantially the same with the
same pattern of transfer. A contract with a phased functionality roll-out, or one whose seat count quadruples in
year 2, does not meet them. Applying the boilerplate spreads consideration across a period in which the promised
service was materially different, which is a measurement error in every period of the contract.

**How to avoid it.** Test the criteria against the contract population's shapes, not against the standard
template. Query for contracts with mid-term quantity changes greater than a threshold or with more than one
subscription start date, and analyze those separately.

## Practice Exercises

### Exercise 5-1

**[Foundational]** Larkspur Analytics signs a 12-month contract on September 26, 2025 with a service period of
October 1, 2025 through September 30, 2026 (365 days). The total fixed fee is $1,000. Three performance
obligations have been identified with the following standalone selling prices: Core subscription (12 months)
$840; Insight subscription (12 months, coterminous) $210; implementation $150. Implementation was completed on
November 14, 2025. Allocate the transaction price and compute FY2025 revenue for each performance obligation and
in total. Amounts in thousands; show the daily rates to the cent.

### Exercise 5-2

**[Foundational]** For each of the following promises in a SaaS order form, state whether it is a separate
performance obligation, a component of the subscription performance obligation, or not a performance obligation
at all, and give the governing reason in one sentence: (a) access to the hosted platform; (b) a $30
non-refundable "onboarding fee" for tenant provisioning; (c) 24×7 premium support sold as a separately priced
SKU that customers may buy or decline; (d) unspecified future upgrades delivered automatically to all tenants;
(e) a commitment to maintain 99.9% uptime with service credits; (f) construction of a customer-specific
integration adapter that AtlasFlow will maintain in its own code base and without which the customer's
contracted use case cannot function.

### Exercise 5-3

**[Intermediate]** A renewal contract signed October 1, 2025 has a total fixed fee of $900 for a 12-month term
and includes a $150 credit usable only against a future Insight purchase. The subscription's standalone selling
price for the 12-month term is $940. Redemption history on 200 closed credits: 118 redeemed in full, 26 redeemed
in part at an average of 40% of face, and 56 expired unused. Compute (a) the expected redemption rate, (b) the
standalone selling price of the material right, and (c) the allocation of the $900 transaction price between the
subscription and the material right, to the dollar.

### Exercise 5-4

**[Intermediate]** Calderon Foods holds an 18-month subscription contract beginning May 1, 2025 with a total fee
of $900, or $50 per month, and a single performance obligation. On November 1, 2025 AtlasFlow granted a $90
price concession applying to the entire contract, with no change in scope and no additional promises. Compute
(a) the cumulative catch-up adjustment and the month in which it is recorded, (b) the revised monthly
recognition rate, and (c) FY2025 revenue. Prove your FY2025 answer a second way.

### Exercise 5-5

**[Intermediate]** Aeropath Group holds a 24-month subscription contract beginning February 1, 2025 with a total
fee of $1,200, or $50 per month. On September 1, 2025 Aeropath added 50 automation seats for the remaining 17
months for additional consideration of $221. The standalone selling price of 50 incremental seats for 17 months
is $340. Determine the modification treatment, state the authoritative basis, and compute FY2025 revenue.

### Exercise 5-6

**[Advanced]** Westmark Utilities signs a 24-month contract with a service period of July 1, 2025 through
June 30, 2027 (730 days). The contract is ramped: $480 for contract year 1 and $720 for contract year 2, billed
annually in advance on July 1. There is one performance obligation and the allocated transaction price equals
$1,200. Compute (a) the daily rate to the cent, (b) FY2025 revenue, (c) the contract's net balance sheet
position at December 31, 2025 and whether it is a contract asset or a contract liability, and (d) the position
at June 30, 2026 immediately before the year-2 invoice is issued.

### Exercise 5-7

**[Intermediate]** The following workpaper extract was prepared for contract with Ironvale Shipping, a 24-month
contract with a service period of April 1, 2025 through March 31, 2027 and a transaction price of $2,000.
Standalone selling prices per management's SSP table are: Core subscription (24 months) $1,600; Insight (24
months, coterminous) $400; implementation $250; administrator training, five sessions, $100. The implementation
was completed June 30, 2025. Two of the five training sessions were delivered in FY2025.

| Performance obligation | SSP | Allocated | FY2025 revenue |
| --- | --- | --- | --- |
| Core subscription | 1,600 | 1,422.222 | 533.333 |
| Insight subscription | 400 | 355.556 | 133.333 |
| Implementation | 250 | 222.222 | 83.333 |
| **Total** | **2,250** | **2,000.000** | **749.999** |

Identify every error and compute the corrected FY2025 revenue and the misstatement.

### Exercise 5-8

**[Advanced]** Management proposes to determine the SSP of a newly launched "AtlasFlow Guard" security module
using the residual approach in a contract with a transaction price of $1,500 whose other obligations have
observable standalone selling prices of $1,410 in aggregate. Guard has been sold on a standalone basis 4 times
since its launch, at 44%, 61%, 78%, and 95% of its $300 list price. Write a conclusion of no more than 200 words
stating whether the residual approach is permitted, what the residual amount is, and what approach you would
require instead. Identify the one additional fact that would change your answer.

### Exercise 5-9

**[Intermediate]** Draft the performance-obligation paragraph of a technical accounting memorandum for contract
C-1, of 120 to 180 words, that (i) identifies the four performance obligations, (ii) states the basis for
combining hosting, support, and updates into the Core obligation, (iii) states why tenant provisioning is not a
performance obligation, and (iv) states the series conclusion and its consequence for the measure of progress.
Include at least two subtopic-level citations.

### Exercise 5-10

**[Advanced]** Using the facts in the extended case study, draft a written communication to management of the
deficiency in the SSP estimation process, of 200 to 280 words. State the control that should exist, the
condition observed with its magnitude, the potential effect, and your recommendation. Do not use the words
"significant deficiency" or "material weakness," and do not state a severity conclusion.

### Exercise 5-11

**[Advanced]** Sundown Media Holdings holds a contract with a committed volume of 600,000 workflow runs per
contract year, a contract year running June 1, 2025 through May 31, 2026, and an overage rate of $9 per 1,000
runs (whole dollars). Monthly consumption, in thousands of runs, was: June 44, July 47, August 50, September 53,
October 58, November 61, December 67. Compute FY2025 overage revenue (a) if the commitment is annual and
cumulative, and (b) if the order form instead provides a monthly allowance of one-twelfth of the annual
commitment, non-cumulative. State which contractual fact determines the answer and the one procedure you would
perform to establish it.

### Exercise 5-12

**[Advanced]** This exercise spans Chapter 4 and Chapter 5. A December contract has a transaction price of
$1,200 for a single 12-month subscription performance obligation. The order form is dated December 15, 2025; the
Salesforce CPQ audit trail shows the record was created on December 22, 2025 and the customer's countersignature
is dated December 22, 2025; the platform administration log shows the tenant was provisioned on January 8, 2026.
Compute FY2025 revenue under each of the three candidate start dates, state the amount AtlasFlow should
recognize and why, and state the two procedures from Chapter 4 you would perform before accepting the order-form
date. Then state the projected effect if six December contracts with an aggregate transaction price of $7,200
share the same pattern and the average error is 17 days of a 365-day term.

## Solutions to Practice Exercises

### Solution 5-1

Aggregate SSP = $840 + $210 + $150 = $1,200. Allocation factor = $1,000 ÷ $1,200 = 0.8333333 (5/6).

| Performance obligation | SSP | Allocated | FY2025 recognition | FY2025 revenue |
| --- | --- | --- | --- | --- |
| Core subscription | 840.000 | 700.000 | 92 days at $1,917.81 | 176.439 |
| Insight subscription | 210.000 | 175.000 | 92 days at $479.45 | 44.109 |
| Implementation | 150.000 | 125.000 | Complete Nov 14, 2025 | 125.000 |
| **Total** | **1,200.000** | **1,000.000** | | **345.548** |

Daily rates: $700,000 ÷ 365 = $1,917.8082, rounded to $1,917.81; $175,000 ÷ 365 = $479.4521, rounded to
$479.45. Days from October 1 to December 31, 2025 = 31 + 30 + 31 = 92. Core revenue = 92 × $1,917.81 =
$176,438.52. Insight revenue = 92 × $479.45 = $44,109.40. Total = $176,438.52 + $44,109.40 + $125,000.00 =
$345,547.92.

### Solution 5-2

(a) **Component of the subscription obligation.** Access to the hosted platform is the substance of the promise;
hosting itself is a fulfillment activity.

(b) **Not a performance obligation.** Tenant provisioning is an administrative setup activity that transfers no
good or service to the customer (ASC 606-10-25-17); the $30 is added to the transaction price and allocated.

(c) **Separate performance obligation.** Premium support is capable of being distinct (separately priced and
declinable) and is separately identifiable in the context of the contract; the customer's ability to decline it
is the decisive fact.

(d) **Component of the subscription obligation.** Unspecified upgrades delivered automatically to all tenants
are part of the stand-ready service; the customer cannot benefit from them separately or decline them.

(e) **Not a performance obligation.** An uptime commitment is an assurance that the promised service will
perform as specified, not an additional promise; earned credits are variable consideration reducing the
transaction price.

(f) **Not a separate performance obligation — combined with the subscription.** The adapter significantly
customizes the subscribed software and the customer cannot obtain the promised functionality without it, so the
promises are not separately identifiable in the context of the contract (ASC 606-10-25-21).

### Solution 5-3

(a) Weighted redemption = (118 × 100%) + (26 × 40%) + (56 × 0%) = 118.0 + 10.4 + 0.0 = 128.4. Expected
redemption rate = 128.4 ÷ 200 = **64.2%**. Implied breakage = 35.8%.

(b) SSP of the material right = $150 × 64.2% = **$96.30**.

(c) Aggregate SSP = $940.00 + $96.30 = $1,036.30. Allocation factor = $900 ÷ $1,036.30 = 0.8684744.

| Performance obligation | SSP | Relative SSP % | Allocated |
| --- | --- | --- | --- |
| Subscription, 12 months | 940.000 | 90.707% | 816.366 |
| Material right | 96.300 | 9.293% | 83.634 |
| **Total** | **1,036.300** | **100.000%** | **900.000** |

The right's allocated amount of $83.634 — 9.3% of the transaction price — remains a contract liability until the
option is exercised or expires unexercised. It is above any conventional threshold for treating a right as
immaterial, so it must be allocated rather than ignored.

### Solution 5-4

(a) Revenue recognized through October 31, 2025 = 6 months × $50 = $300.0. Revised transaction price =
$900 − $90 = $810.0. Measure of progress at October 31, 2025 = 6 ÷ 18 = 33.333%. Cumulative revenue that
should be recognized = $810.0 × 33.333% = $270.0. **Cumulative catch-up adjustment = $270.0 − $300.0 =
$(30.0), recorded in November 2025**, the period in which the modification was approved. The modification is a
cumulative catch-up because nothing distinct was added and the concession reprices services already
transferred as well as those remaining (ASC 606-10-25-13(b)).

(b) Remaining consideration = $810.0 − $270.0 = $540.0 over the remaining 12 months. **Revised monthly rate =
$45.0.**

(c) FY2025 revenue = $300.0 − $30.0 + (2 months × $45.0) = $300.0 − $30.0 + $90.0 = **$360.0**.

Second proof: 8 of the 18 months elapsed by December 31, 2025, so cumulative revenue = $810.0 × 8 ÷ 18 =
$360.0. The two computations agree.

### Solution 5-5

**Treatment: prospective.** The additional seats are priced at $221 against an SSP of $340 — 65.0% of SSP — so
the modification is not a separate contract under ASC 606-10-25-12, which requires the price increase to reflect
the standalone selling price of the added goods or services. The remaining goods or services after the
modification (the days of platform access from September 1, 2025 onward) are distinct from those transferred on
or before that date, so ASC 606-10-25-13(a) applies: terminate the existing contract and account for the
remainder as a new contract.

| Step | Computation | Amount |
| --- | --- | --- |
| Original transaction price | 24 months × $50 | 1,200.0 |
| Revenue recognized February 1 – August 31, 2025 | 7 months × $50 | 350.0 |
| Remaining unrecognized consideration | 1,200.0 − 350.0 | 850.0 |
| Additional consideration | | 221.0 |
| Revised remaining consideration | 850.0 + 221.0 | 1,071.0 |
| Remaining term | Sep 1, 2025 – Jan 31, 2027 | 17 months |
| Revised monthly rate | 1,071.0 ÷ 17 | 63.0 |
| **FY2025 revenue** | (7 × $50.0) + (4 × $63.0) = 350.0 + 252.0 | **602.0** |

No adjustment is made to the $350.0 already recognized. **A credible alternative** is to argue that the
incremental seats are a distinct performance obligation priced below SSP, requiring the unallocated discount to
be spread across the original and the incremental seats — which produces the same $1,071.0 over the same 17
months and therefore the same answer, because both obligations are recognized ratably over an identical
remaining period. The alternative is not weaker; it is arithmetically equivalent here, and stating that is
better documentation than asserting a single path.

### Solution 5-6

(a) Daily rate = $1,200,000 ÷ 730 days = $1,643.8356, rounded to the cent = **$1,643.84**. (730 × $1,643.84 =
$1,200,003.20, so a $3.20 cumulative rounding residual clears in the final period of the schedule.)

(b) Days from July 1 to December 31, 2025 = 31 + 31 + 30 + 31 + 30 + 31 = 184. FY2025 revenue = 184 ×
$1,643.84 = **$302,466.56**, or $302.5.

(c) Billings through December 31, 2025 = the $480 year-1 invoice issued July 1, 2025. Net position = $480.000 −
$302.467 = **$177.533, a contract liability** (deferred revenue), because cumulative billings exceed cumulative
revenue.

(d) Cumulative revenue at June 30, 2026 = 365 days × $1,643.84 = $600,001.60, or $600.0 after the rounding
residual. Cumulative billings remain $480.0. Net position = $480.0 − $600.0 = **$(120.0), a contract asset** of
$120.0. The ramp has flipped the contract from a liability to an asset, which is the defining balance-sheet
signature of a ramped contract and the reason Chapter 6, §6.8 must be read alongside this chapter.

### Solution 5-7

Three errors, one of which causes a fourth.

**Error 1 — the training performance obligation is omitted entirely.** Its SSP of $100 is excluded from the
denominator and it receives no allocation, and the two sessions delivered in FY2025 produce no revenue.

**Error 2 — the aggregate SSP is therefore $2,250 rather than $2,350**, which misallocates the transaction price
across all obligations. The allocation factor should be $2,000 ÷ $2,350 = 0.8510638, not $2,000 ÷ $2,250 =
0.8888889.

**Error 3 — the implementation obligation is recognized ratably over the 24-month subscription term** ($222.222
× 9 ÷ 24 = $83.333) although it was completed on June 30, 2025. A completed obligation is fully recognized.

**Corrected schedule:**

| Performance obligation | SSP | Allocated | Basis for FY2025 | FY2025 revenue |
| --- | --- | --- | --- | --- |
| Core subscription | 1,600.000 | 1,361.702 | 9 of 24 months | 510.638 |
| Insight subscription | 400.000 | 340.426 | 9 of 24 months | 127.660 |
| Implementation | 250.000 | 212.766 | Complete Jun 30, 2025 | 212.766 |
| Administrator training | 100.000 | 85.106 | 2 of 5 sessions | 34.042 |
| **Total** | **2,350.000** | **2,000.000** | | **885.106** |

**Misstatement: FY2025 revenue is understated by $885.106 − $749.999 = $135.107.** Against the $72 clearly
trivial threshold this is a reportable misstatement, and the direction (understatement) does not reduce your
obligation to accumulate it.

### Solution 5-8

Model conclusion (188 words), followed by the additional fact that would change the answer:

"The residual approach is not permitted for the Guard module in this contract. ASC 606-10-32-34(c) permits the
residual approach only where the entity sells the same good or service to different customers for a broad range
of amounts, or where it has not yet established a price and has not previously sold the item on a standalone
basis. Guard has been sold on a standalone basis four times, at 44%, 61%, 78%, and 95% of a $300 list price, so
the second condition is unavailable. The first condition is arguable on variability, but ASC 606-10-32-35
independently prohibits a residual result that is not within a reasonable range of the observable evidence. The
residual here is $1,500 − $1,410 = $90, which is 30.0% of list — below the lowest of the four observed
standalone prices. I would require an adjusted market assessment or expected cost plus a margin, corroborated
against the four observations, and would expect a point estimate within roughly 44% to 95% of list.

The one fact that would change this answer is the withdrawal of the four standalone sales from the population —
for example, if all four were sold in a bundle with a Core renewal and none qualified as standalone. Guard would
then have no established standalone price, the second permitting condition would be met, and the residual
approach would become available — subject still to the ASC 606-10-32-35 reasonableness constraint, which the
30.0% residual would likely still fail."

### Solution 5-9

Model paragraph (166 words):

"The Company has identified four performance obligations in the Meridian arrangement: (1) the AtlasFlow Core
subscription for 500 automation seats for the period March 15, 2025 through March 14, 2028; (2) the AtlasFlow
Insight subscription for contract years two and three; (3) implementation and configuration services; and (4) an
administrator training package of five instructor-led sessions. Standard technical support and unspecified
updates and upgrades are not separately identifiable from platform access in the context of the contract, as the
customer receives them automatically and cannot benefit from them independently, and they are therefore combined
into obligation (1) under ASC 606-10-25-19 and 25-21. Tenant provisioning and account activation transfer no
good or service to the customer and are accordingly not performance obligations (ASC 606-10-25-17). Each day of
platform availability within obligations (1) and (2) is a distinct service; the daily services are substantially
the same and have the same pattern of transfer, so each obligation is accounted for as a single performance
obligation satisfied over time under ASC 606-10-25-14(b), with progress measured by time elapsed."

### Solution 5-10

Model communication (262 words):

"During our audit of the FY2025 financial statements we identified a deficiency in the Company's process for
estimating the standalone selling price of the AtlasFlow Insight module.

The Company's control, as described to us, requires the Director of Technical Accounting to prepare an annual
standalone selling price analysis supported by observable standalone sales and by at least one estimation
approach, and requires the VP of Revenue Accounting to review and approve it.

We observed two conditions. First, the population of 31 transactions represented as standalone Insight sales and
used to corroborate the estimate had not been tested for qualification as standalone sales. Our inspection of
all 31 executed order forms identified 8 transactions (25.8% of the population) that did not qualify: two shared
an order form with a Core renewal, four were executed within 90 days of a Core order by the same customer, one
was priced by a reseller, and one was executed nine days after a Core order. Second, the weighting applied to
the two estimation approaches changed between the November 3 and December 19, 2025 versions of the supporting
memorandum, from 70/30 to 50/50, and the documented basis for the change is limited to the phrase 'alignment
with observable standalone sales.'

The standalone selling price of Insight affects the allocation of transaction price in approximately 412 FY2025
multi-element contracts with an aggregate transaction price of $78,900 thousand. Across the range of estimates
supportable by the Company's own two approaches, FY2025 subscription revenue would differ by approximately $139
thousand.

We recommend that the Company (a) define and apply documented qualification criteria to the standalone-sale
population before it is used as corroborating evidence, and (b) document the basis for the relative weighting of
estimation approaches independently of the corroborating statistic."

### Solution 5-11

(a) **Annual cumulative commitment: nil.** Cumulative consumption from June 1 to December 31, 2025 = 44 + 47 +
50 + 53 + 58 + 61 + 67 = 380 thousand runs, against a commitment of 600 thousand. The commitment was not
exhausted, so no overage was earned and none is recognized.

(b) **Monthly non-cumulative allowance: $351 in whole dollars.** The monthly allowance is 600,000 ÷ 12 = 50,000
runs.

| Month | Runs (000s) | Allowance (000s) | Overage runs (000s) | Overage at $9 per 1,000 |
| --- | --- | --- | --- | --- |
| June 2025 | 44 | 50 | — | — |
| July 2025 | 47 | 50 | — | — |
| August 2025 | 50 | 50 | — | — |
| September 2025 | 53 | 50 | 3 | 27 |
| October 2025 | 58 | 50 | 8 | 72 |
| November 2025 | 61 | 50 | 11 | 99 |
| December 2025 | 67 | 50 | 17 | 153 |
| **Total** | **380** | | **39** | **351** |

The determining fact is the wording of the included-volume clause: whether the 600,000 runs are an annual
allowance measured cumulatively over the contract year or a monthly allowance that does not roll forward. The
procedure: read the included-volume clause in the executed order form and the master subscription agreement, and
agree the Zuora Billing rate-plan charge's usage-accumulation setting ("annual, cumulative" versus "monthly,
non-cumulative") to the clause. Inquiry of the billing analyst is not sufficient; the clause and the
configuration must be inspected and must agree.

### Solution 5-12

Daily rate = $1,200,000 ÷ 365 = $3,287.6712, rounded to $3,287.67.

| Candidate start date | Days of service in FY2025 | FY2025 revenue |
| --- | --- | --- |
| December 15, 2025 (order-form date) | 17 | 55,890.39 |
| December 22, 2025 (countersignature and CPQ record creation) | 10 | 32,876.70 |
| January 8, 2026 (provisioning) | — | — |

**AtlasFlow should recognize nil.** Two independent reasons converge. First, a contract does not exist for
accounting purposes before the parties have approved it and it is enforceable; the countersignature and the CPQ
audit trail both point to December 22, so December 15 is not a supportable start date. Second, AtlasFlow's
policy (case §4.1) recognizes subscription revenue from the later of the contract start date and the
provisioning date, and provisioning occurred January 8, 2026. The later of the two dates is January 8, 2026, so
no FY2025 revenue arises.

The two Chapter 4 procedures to perform before accepting the order-form date are: (i) obtain the Salesforce CPQ
audit trail for the opportunity and order record, including record creation, field-modification history, and
approval timestamps, and compare them to the stated order-form date — Brett Hallowell has the ability to modify
order-form dates in CPQ (case §5.1), so the field history is the relevant evidence; and (ii) obtain the
customer's executed counterpart directly and inspect the countersignature date, together with the email
transmission metadata, rather than relying on the version filed in the contract repository.

Projected effect if six contracts with an aggregate transaction price of $7,200 share the pattern with an
average error of 17 days: $7,200 × 17 ÷ 365 = **$335 of overstated FY2025 revenue** — well above the $72 clearly
trivial threshold and above 35% of performance materiality of $940. Uncorrected misstatement U-3 in the FY2025
file is the actual outcome of this fact pattern, at $150; the difference between $335 and $150 is a reminder that
a projection is an estimate to be refined by testing each contract, not a substitute for testing them.

## Review Questions

**RQ 5-1.** State the two conditions in ASC 606-10-25-19 that a promised good or service must satisfy to be
accounted for as a separate performance obligation.

**RQ 5-2.** Why is hosting infrastructure not a performance obligation in a SaaS contract, and how does that
differ from the treatment of a separately priced premium support SKU that the customer may decline?

**RQ 5-3.** State the criteria for applying the series guidance and explain in one sentence why the criteria
are met for AtlasFlow Core.

**RQ 5-4.** What is a material right, and what makes a renewal discount a material right rather than an
ordinary price concession?

**RQ 5-5.** Name the three approaches to estimating a standalone selling price described in ASC 606-10-32-34,
and state which of them AtlasFlow used for Insight.

**RQ 5-6.** State the two circumstances in which the residual approach is permitted, and the circumstance in
which its result must be rejected even when one of those two is present.

**RQ 5-7.** Explain why a lower standalone selling price assigned to a performance obligation that has not yet
commenced increases current-period revenue.

**RQ 5-8.** State the three criteria of the discount-allocation exception in ASC 606-10-32-37, and which of the
three failed for contract C-1.

**RQ 5-9.** Distinguish a prospective contract modification from a cumulative catch-up, and state the fact that
decides between them for a SaaS subscription.

**RQ 5-10.** Why is a contract modification accounted for as a separate contract when the added goods or
services are distinct and priced at their standalone selling prices?

**RQ 5-11.** On a ramped contract, why does the invoiced amount for the first contract year understate the
revenue that should be recognized, and what balance sheet item does that difference create?

**RQ 5-12.** What is the authoritative basis for recognizing usage overage in the month the runs are consumed
rather than spreading it over the contract term, and how does that basis differ from the right-to-invoice
measure of progress?

**RQ 5-13.** Distinguish testing a revenue engine's configuration from testing its output, and state the
condition that must hold before a configuration test alone can support a conclusion about revenue.

**RQ 5-14.** Why is a contract liability a non-monetary item, and what is the consequence for a
foreign-currency subscription contract?

**RQ 5-15.** In a full-population recomputation of revenue, why does agreeing your answer exactly to the
engine's answer not establish that service start dates are correct?

**RQ 5-16.** Give two reasons why an interquartile range of 22 points of list price on a population of
standalone sales does not, by itself, mean an observable standalone selling price is unavailable — and state
what it does mean.

**RQ 5-17.** State two indicators, drawn from the FY2025 AtlasFlow facts, that would cause you to increase your
assessment of inherent risk over the Insight SSP estimate.

**RQ 5-18.** Why does a critical audit matter arising from the Insight standalone selling price not require the
engagement team to have identified a material misstatement?

## Answers to Review Questions

**RQ 5-1.** The promise must be capable of being distinct — the customer can benefit from it on its own or with
other readily available resources — and it must be distinct within the context of the contract, meaning it is
separately identifiable from the other promises. ASC 606-10-25-21 supplies three indicators for the second
test: no significant integration service, no significant modification or customization of another promised item,
and no high degree of interdependence or interrelation.

**RQ 5-2.** Hosting is how AtlasFlow delivers the promised service; the customer contracted for functioning
software, not for infrastructure, and cannot benefit from the infrastructure separately. A declinable,
separately priced premium support SKU is different because the customer's ability to buy or not buy it
demonstrates both that it is capable of being distinct and that AtlasFlow does not treat it as an inseparable
part of platform access.

**RQ 5-3.** The criteria (ASC 606-10-25-14(b) and 25-15) are that the goods or services are distinct and
substantially the same, that each would be a performance obligation satisfied over time, and that the same
method would be used to measure progress toward complete satisfaction of each. They are met for Core because
each day of platform availability is a distinct, substantially identical service satisfied over time and
measured by time elapsed.

**RQ 5-4.** A material right is an option to acquire additional goods or services that the customer would not
have received without entering into the contract, and it is a performance obligation to which consideration must
be allocated. A renewal discount becomes a material right when it is incremental to the range of discounts
ordinarily given for those goods or services to that class of customer in that market; a discount available to
everyone on the price list is not incremental and therefore is not a material right.

**RQ 5-5.** The adjusted market assessment approach, the expected cost plus a margin approach, and the residual
approach. AtlasFlow used the first two for Insight — an adjusted market assessment of 89.0% of list and an
expected cost plus a margin of 76.0% of list — weighted equally to reach 82.5%.

**RQ 5-6.** The residual approach is permitted where the entity sells the same good or service to different
customers for a broad range of amounts, or where it has not yet established a price for the item and has not
previously sold it on a standalone basis. Even where one of those conditions is met, ASC 606-10-32-35 requires a
different approach if the residual produces an amount that is not within a reasonable range of the observable
evidence or produces little or no consideration.

**RQ 5-7.** Allocation is a zero-sum exercise: the transaction price is fixed, so consideration not allocated to
one obligation is allocated to the others. If the underweighted obligation has not begun — Insight on C-1 does
not begin until March 15, 2026 — the consideration taken from it lands on obligations already being satisfied
and is recognized now. On C-1, the prohibited residual approach would have moved $297.5 onto Core and the
professional services obligations and increased FY2025 revenue by $103.

**RQ 5-8.** The entity must regularly sell each distinct good or service in the contract on a standalone basis;
it must also regularly sell on a standalone basis a bundle of some of them at a discount to their aggregate
standalone selling prices; and the bundle discount must be substantially the same as the contract discount, with
the analysis providing observable evidence of the obligations to which the entire discount belongs. The first
criterion failed for C-1: Insight was sold standalone only 31 times against 1,180 Insight-bearing contracts.

**RQ 5-9.** A prospective modification terminates the existing contract and allocates the remaining
unrecognized consideration plus the new consideration over the remaining obligations, with no adjustment to
revenue already recognized; a cumulative catch-up adjusts revenue already recognized. The deciding fact is
whether the goods or services remaining after the modification are distinct from those transferred on or before
the modification date. For a SaaS subscription treated as a series they generally are, because future days of
access are distinct from delivered days, so most SaaS amendments are prospective.

**RQ 5-10.** Because the addition contains no interaction with the original contract's economics: the customer
is paying the standalone price for a distinct item, so nothing about the original contract's transaction price or
allocation has changed. ASC 606-10-25-12 accordingly leaves the original contract undisturbed.

**RQ 5-11.** The amount to be recognized is the transaction price allocated to the whole performance obligation
spread over the whole service period, and on a ramp the first year's invoice is below that average by
construction. On C-1, year 1 invoicing of $600 compares to allocated revenue of $811.8, a $211.8 difference at
the end of contract year 1. The difference creates a contract asset — revenue recognized in excess of amounts
billed — presented subject to the contract-level netting rule in Chapter 6, §6.8.

**RQ 5-12.** The basis is the allocation of variable consideration to a distinct good or service within a series
(ASC 606-10-32-40): the overage relates specifically to the days on which the excess runs were consumed. The
right-to-invoice measure of progress in ASC 606-10-55-18 is different: it permits recognizing revenue equal to
the amount invoiced where that amount corresponds directly to the value transferred to date, which is not the
case in the early months of a contract with an unexhausted minimum commitment.

**RQ 5-13.** Testing configuration is a test of controls that provides evidence about design and operating
effectiveness of the engine's logic; testing output is a test of details that provides evidence about the amount
recorded. A configuration test alone can support a conclusion about revenue only if the information technology
general controls over the application — privileged access, change management, and the integrity of the
configuration through the period — are effective. At AtlasFlow they are not (W-1 and W-6), so a substantive
recomputation is required.

**RQ 5-14.** A contract liability will be settled by transferring goods or services rather than a fixed amount
of currency, so it is non-monetary and is not remeasured for subsequent exchange rate movements under
ASC 830-10-45. The consequence is that a foreign-currency subscription's revenue is fixed in the functional
currency at inception: C-2's £1,275 measurement does not change when the EUR moves, and remeasuring the £489.0
liability at year end would create a £5.4 loss that does not exist.

**RQ 5-15.** Because the recomputation and the engine consumed the same field. If the service start date in the
contract-terms extract came from the Zuora subscription record, and the engine derived its schedule from that
same record, both will be wrong in the same way and will agree. Detecting the error requires an independent
source — the signed order form and the platform provisioning log — which is how Brightline found C-1's $6,672
difference.

**RQ 5-16.** First, an interquartile range measures dispersion, not the presence of an observable price; a wide
range can reflect genuine market segmentation, in which case segment-level observable prices may be available
even though the pooled population looks dispersed. Second, dispersion may be an artifact of a non-stationary
price — AtlasFlow's H1 average was 97.9% of list and its H2 average 77.2% — in which case period-specific
observable prices exist. What the 22-point range does mean is that a single pooled point estimate is imprecise
and must be either disaggregated or supported by an estimation approach.

**RQ 5-17.** First, Insight launched in January 2025, so the SSP is being set for a new SKU with a thin and
non-stationary evidence base, and the case file itself notes SSP evidence for a new SKU is thin. Second, the
control environment around the estimate is weak: the VP of Revenue Accounting who approves the memo has been on
a performance plan since March 2025 and owns the RevPro configuration, and two revenue accountants resigned in
Q2 2025. A third indicator is the version history of the memo, in which the weighting changed to match the
corroborating statistic.

**RQ 5-18.** A critical audit matter is a matter communicated or required to be communicated to the audit
committee that relates to accounts or disclosures material to the financial statements and involved especially
challenging, subjective, or complex auditor judgment. Neither limb requires a misstatement. Insight revenue of
$26,700 is material and the allocation judgment across 412 multi-element contracts was especially challenging
and subjective, so the matter qualifies even though the maximum exposure across the defensible SSP range was
$139.

## Key Definitions

**Adjusted market assessment approach.** An approach to estimating a standalone selling price in which the
entity evaluates the market into which it sells and estimates the price a customer in that market would be
willing to pay, which may include referring to competitors' prices for similar goods or services adjusted for
differences in cost and margin (ASC 606-10-32-34(a)).

**Allocation factor.** The ratio of the transaction price to the aggregate standalone selling price of a
contract's performance obligations, applied to each obligation's standalone selling price to determine its
allocated amount. For contract C-1 the factor is $3,120 ÷ $3,456 = 0.9027778.

**Breakage.** The portion of a customer option, credit, or prepayment that the entity expects will never be
exercised or redeemed. Breakage is the complement of the expected redemption rate and is a required input to
valuing a material right.

**Contract asset.** An entity's right to consideration in exchange for goods or services transferred to a
customer when that right is conditional on something other than the passage of time. On a ramped contract, the
excess of cumulative revenue recognized over cumulative amounts billed is a contract asset.

**Contract liability.** An entity's obligation to transfer goods or services to a customer for which it has
received, or is unconditionally entitled to receive, consideration. Deferred revenue is a contract liability.

**Contract modification.** A change in the scope or price of a contract, or both, that the parties to the
contract approve, whether in writing, orally, or by customary business practice (ASC 606-10-25-10).

**Cumulative catch-up modification.** A contract modification accounted for as part of the existing contract
because the remaining goods or services are not distinct from those already transferred; revenue recognized to
date is adjusted at the modification date to the amount that would have been recognized under the revised
transaction price (ASC 606-10-25-13(b)).

**Discount-allocation exception.** The provision permitting a contract discount to be allocated to one or more
but not all performance obligations where three conditions are met, including that the entity regularly sells
each distinct good or service on a standalone basis and regularly sells a bundle of some of them at a
substantially similar discount (ASC 606-10-32-37).

**Distinct.** A characteristic of a promised good or service that is both capable of being distinct — the
customer can benefit from it on its own or with readily available resources — and separately identifiable from
other promises in the contract (ASC 606-10-25-19).

**Expected cost plus a margin approach.** An approach to estimating a standalone selling price in which the
entity forecasts the costs of satisfying a performance obligation and adds an appropriate margin
(ASC 606-10-32-34(b)).

**Interquartile range.** The difference between the third quartile and the first quartile of a distribution,
covering the middle half of the observations. AtlasFlow's 31 standalone Insight sales have an interquartile
range of 22.0 percentage points of list price.

**Material right.** A customer option to acquire additional goods or services that provides the customer with a
right it would not have received without entering into the contract, typically a discount incremental to the
range of discounts ordinarily given for those goods or services to that class of customer in that market
(ASC 606-10-55-42).

**Measure of progress.** The method used to determine the extent to which a performance obligation satisfied
over time has been satisfied, either an output method or an input method; for a stand-ready SaaS service it is
generally time elapsed.

**Non-coterminous element.** A performance obligation in a multi-element contract whose service period begins
or ends on a date different from the other obligations in the same contract. Insight on contract C-1 is
non-coterminous, beginning 365 days after the Core obligation.

**Performance obligation.** A promise in a contract with a customer to transfer to the customer either a good or
service that is distinct, or a series of distinct goods or services that are substantially the same and that
have the same pattern of transfer (ASC 606-10-25-14).

**Prospective modification.** A contract modification accounted for by terminating the existing contract and
creating a new one, because the remaining goods or services are distinct from those transferred on or before the
modification date; the remaining unrecognized consideration plus the new consideration is allocated over the
remaining performance obligations, with no adjustment to revenue already recognized (ASC 606-10-25-13(a)).

**Ramp.** A contractual pricing pattern in which the periodic fee rises across the term of a contract.
Contract C-1's Core fee ramps from $600 in year 1 to $840 in year 2 to $960 in year 3.

**Residual approach.** An approach to estimating a standalone selling price by deducting the sum of the
observable standalone selling prices of the contract's other promises from the total transaction price,
permitted only where the selling price of the item is highly variable or has not been established, and
prohibited where the result is not within a reasonable range of observable evidence (ASC 606-10-32-34(c) and
32-35).

**Series guidance.** The provision treating a series of distinct goods or services that are substantially the
same and have the same pattern of transfer as a single performance obligation where each would be satisfied over
time and the same measure of progress would apply to each (ASC 606-10-25-14(b) and 25-15).

**Setup activity.** An administrative activity an entity must undertake to fulfill a contract that does not
transfer a good or service to the customer, and which is therefore not a performance obligation even when it is
separately priced (ASC 606-10-25-17).

**Standalone selling price (SSP).** The price at which an entity would sell a promised good or service
separately to a customer, determined at contract inception; the observable price in a standalone sale is the
best evidence, and where none exists the price must be estimated (ASC 606-10-32-32).

**Stand-ready obligation.** An obligation to make a service continuously available to the customer, satisfied by
the availability itself rather than by the customer's use. A SaaS subscription is a stand-ready obligation,
which is why the measure of progress is time rather than usage.

**Usage overage.** Consideration payable for consumption of a metered resource in excess of a committed volume,
which is variable consideration allocated to the distinct services in the series to which it relates.
AtlasFlow's FY2025 overage revenue was $4,200, recorded in account 4120.

**Workflow run.** AtlasFlow's unit of metered consumption, being a single execution of an automation on the
platform. Contract C-1 includes 200,000 runs per contract year with overage at $12 per 1,000 runs.

## Chapter Summary

1. Subscription revenue is the output of five sequential judgments — performance obligation identification,
   standalone selling price, allocation, service period, and modification treatment — and an audit that tests
   only the invoice tests none of them.
2. In a standard SaaS contract, hosting, standard support, unspecified upgrades, and tenant provisioning are
   not separate performance obligations; a declinable separately priced module, distinct implementation
   services, and a training package generally are, and contract C-1 has four obligations totaling a $3,120
   transaction price.
3. Implementation services are not distinct where they significantly customize the subscribed software; on
   AtlasFlow's 11 such FY2025 contracts, treating $2,180 of fees as distinct would have accelerated
   approximately $1,453 of revenue — above overall materiality of $1,450.
4. The series guidance makes a SaaS subscription one performance obligation satisfied over time, which fixes
   the measure of progress as time elapsed and permits usage overage to be allocated to the day it is consumed.
5. A material right must be valued on an expected-value basis with an explicit breakage assumption: C-2's $200
   Insight credit has a standalone selling price of $143.10 at a 71.55% expected redemption rate, and $120.994
   of the $1,600 transaction price is deferred against it.
6. The residual approach is prohibited where its result falls outside a reasonable range of observable
   evidence; on C-1 it produces an Insight SSP of 12.5% of list against an observed band of 58% to 100%, and
   using it would have overstated FY2025 revenue on that contract by $103.
7. An SSP conclusion must be audited quantitatively: AtlasFlow's 31 standalone Insight sales have an
   interquartile range of 22.0 points, only 58.1% of observations fall within ±15% of the median, 8 of 31 did
   not qualify as standalone, and the H1 mean of 97.9% of list against an H2 mean of 77.2% shows the band is a
   trend rather than dispersion.
8. Sample sufficiency for an estimate is computable: a 95% confidence interval on the mean of 77.4% to 86.3% of
   list translates, at $10.71 of revenue per point, to approximately $95 — 10.1% of performance materiality —
   which is what makes 31 observations sufficient in FY2025 and will not make them sufficient in FY2027.
9. Allocating C-1's $3,120 transaction price on a relative SSP basis produces $2,437.500 / $357.500 / $279.861
   / $45.139; applying the discount-allocation exception instead would have accelerated $24.9 of revenue on that
   single contract, so the exception's availability requires a documented conclusion.
10. The three modification outcomes are decided by a strict sequence, and for a SaaS series the answer is
    usually prospective; a $120 concession on a $1,200 24-month contract nine months in produces a $(45.0)
    cumulative catch-up and a revised rate of $45.0 per month, which must reconcile to $540.0 of FY2025 revenue
    computed independently.
11. Ramped contracts require straight-line recognition of the allocated total, not the invoiced amount: C-1's
    Core obligation recognizes $811.760 in contract year 1 against $600 invoiced, and the resulting difference
    is a contract asset, not an error.
12. Usage overage against an annual cumulative commitment does not arise until the commitment is exhausted:
    Meridian's cumulative 186,000 runs at December 31, 2025 against a 200,000-run commitment produce nil FY2025
    overage revenue, while a monthly-allowance reading of the same clause would produce $376 in whole dollars.
13. Where information technology general controls over the revenue engine are deficient — as AtlasFlow's are
    under W-1 and W-6 — configuration testing cannot support the revenue conclusion, and a substantive
    recomputation from contract data sourced independently of the engine is required.
14. A foreign-currency subscription is measured in the functional currency at the inception spot rate and the
    resulting contract liability is non-monetary; only the monetary receivable is remeasured through earnings,
    and only £7.0 of C-2's $17.2 of USD movement is an earnings item.
15. The walkthrough's outcome is the model for the chapter: an independent recomputation of $956,352.44 against
    a subledger figure of $963,024.44 isolated a $6,672 difference to three days of a single null field, and the
    population query that followed converted a trivial misstatement into a documented control matter.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Order-to-cash process, contract existence, and period-end cut-off | Chapter 4, §4.3–4.5 | This chapter assumes the contract exists and is dated correctly; Chapter 4 establishes both |
| Variable consideration, the constraint, and SLA credits | Chapter 4, §4.6 and §4.9 | The transaction price inputs this chapter allocates |
| Professional services percentage-of-completion mechanics | Chapter 4, §4.12 | The input measure applied to PO 3 in the walkthrough |
| Principal versus agent and the Tessera reseller arrangement | Chapter 4, §4.11 | Reseller-priced observations disqualified from the SSP population |
| Deferred revenue, contract assets, and the netting rule | Chapter 6, §6.6–6.8 | Where the allocated amounts computed here become balance sheet amounts |
| The RPO disclosure and contract-term judgments | Chapter 6, §6.11 | Material rights and non-enforceable contract portions enter the disclosure |
| Materiality figures used throughout | Chapter 3 | The derivation of $1,450, $940, and $72 |
| Assertion-level risk assessment for revenue | Chapter 2, §2.8 | Why the Insight SSP is a significant risk |
| Capitalized commissions and the ASC 340-40 amortization period | Chapter 10, §10.6 | Why the contract-term conclusion for revenue does not set the commission amortization period |
| RevPro configuration as an application control; IPE reliability | Chapter 12, §12.7 and §12.10 | How to test the 27 configuration rules and the reports this chapter relies on |
| ITGC deficiencies W-1 and W-6 and their effect on reliance | Chapter 11, §11.9 | Why the substantive strategy in §5.11 is required |
| Deficiency severity and aggregation | Chapter 14, §14.9 | Evaluating the SSP process deficiency identified in the case study |
| Substantive analytical procedures over subscription revenue | Chapter 18, §18.7 | The complement to the tests of details in this chapter |
| Sample size determination for the 40-contract attribute test | Chapter 15, §15.5 | How the extent of testing in §5.11 is set |
| Revenue fraud schemes, including SSP manipulation and backdating | Chapter 17, §17.6 | The fraud vectors the residual approach and the December contracts create |
| Evaluating indicators of estimate bias | Chapter 19, §19.4 | Where the SSP memo version history is evaluated |
| The Insight SSP critical audit matter | Chapter 20, §20.6 | Three successive drafts of the CAM and the reviewer's comments |

## Further Reading

- FASB Accounting Standards Codification Topic 606, *Revenue from Contracts with Customers*, in particular
  subtopics 606-10-25 (identifying performance obligations and contract modifications), 606-10-32 (transaction
  price and allocation), and 606-10-55 (implementation guidance, including customer options for additional goods
  or services).
- FASB Accounting Standards Update No. 2014-09, *Revenue from Contracts with Customers (Topic 606)*, including
  its Basis for Conclusions, which is the most useful source on why the series guidance and the
  discount-allocation exception were written as they were.
- FASB Accounting Standards Codification Subtopic 340-40, *Other Assets and Deferred Costs — Contracts with
  Customers*.
- FASB Accounting Standards Codification Topic 830, *Foreign Currency Matters*, subtopics 830-10 and 830-30.
- PCAOB Auditing Standard 2501, *Auditing Accounting Estimates, Including Fair Value Measurements*, and
  PCAOB Auditing Standard 2301, *The Auditor's Responses to the Risks of Material Misstatement*.
- PCAOB Auditing Standard 2401, *Consideration of Fraud in a Financial Statement Audit*, and its appendices on
  fraud risk factors.
- PCAOB Auditing Standard 2601, *Consideration of an Entity's Use of a Service Organization*.
- AICPA Statement on Auditing Standards No. 145 and the resulting AU-C 315, and AU-C 540 as revised, for
  readers applying AICPA standards to private SaaS companies.
- The AICPA audit and accounting guide covering revenue recognition, which includes industry-specific
  discussion of software and software-as-a-service arrangements.
- SEC Division of Corporation Finance guidance on Management's Discussion and Analysis under Regulation S-K
  Item 303, for the presentation of pricing and mix effects on subscription revenue.
