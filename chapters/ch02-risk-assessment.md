# Chapter 2 — Risk Assessment in a Subscription Business

> Risk assessment fails in two characteristic ways, and both look like work. The first is the risk register that
> says "revenue recognition" in the risk column and "test revenue" in the response column, which is a table of
> contents pretending to be an analysis. The second is the assessment that rates everything high, which spends
> the engagement's entire budget defending against risks that were never there and leaves nothing for the ones
> that were. What separates a real assessment from either failure is specificity: a named account, a named
> assertion, a named direction, a named reason the reason exists, and a response that would not have been
> designed if the risk had been assessed one notch lower. This chapter builds that assessment for AtlasFlow's
> FY2025 audit — thirty-eight risks across seven areas, with inherent risk and control risk assessed separately,
> nine significant risks identified, and a response designed for each.

## Learning Objectives

After completing this chapter you will be able to:

- **LO 2.1** Apply the audit risk model to compute the detection risk implied by a given assessment of inherent
  and control risk, and explain the directional consequence for the extent of substantive testing.
- **LO 2.2** Assess inherent risk and control risk separately at the assertion level, and state where the PCAOB
  and AICPA frameworks differ on whether separate assessments are required.
- **LO 2.3** Place a risk on the spectrum of inherent risk by identifying which inherent risk factors are
  present and how they affect the likelihood and magnitude of misstatement.
- **LO 2.4** Design and document the required risk assessment procedures for a subscription business, including
  the inquiries that must be made of people outside the finance function.
- **LO 2.5** Plan, conduct, and document an engagement team discussion that produces assertion-level output
  rather than a list of topics.
- **LO 2.6** Identify risks of material misstatement at the assertion level for each of AtlasFlow's seven
  highest-risk areas and state the direction of each potential misstatement.
- **LO 2.7** Determine whether an identified risk is a significant risk, distinguish that determination from a
  "high risk" label, and state the consequences that follow from it.
- **LO 2.8** Identify risks arising from the use of information technology and distinguish them from the general
  IT controls that address them.
- **LO 2.9** Describe the five components of the system of internal control and identify which controls are
  relevant to the audit for a given assertion.
- **LO 2.10** Convert an assessed risk of material misstatement into a specific decision about the nature,
  timing, and extent of further audit procedures.
- **LO 2.11** Recognize the events during an audit that require reassessment of risk, and document the
  reassessment and its consequences.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 1101, *Audit Risk* | Describes audit risk as a function of the risk of material misstatement and detection risk, and describes the risk of material misstatement as consisting of inherent risk and control risk. It does not require separately documented inherent and control risk ratings. |
| PCAOB | AS 2110, *Identifying and Assessing Risks of Material Misstatement* | Requires performing risk assessment procedures to obtain an understanding of the company and its environment, including internal control over financial reporting; requires a discussion among key engagement team members; requires identifying and assessing risks of material misstatement at the financial statement and assertion levels; and requires identifying significant risks. |
| PCAOB | AS 2301, *The Auditor's Responses to the Risks of Material Misstatement* | Requires the nature, timing, and extent of further procedures to be responsive to assessed risk, and requires specific responses for significant risks, including substantive procedures directly related to the significant risk. |
| PCAOB | AS 2401, *Consideration of Fraud in a Financial Statement Audit* | Requires a fraud-specific engagement team discussion, inquiries of management, the audit committee, internal audit, and others, the presumption of a fraud risk in revenue recognition, and required procedures regardless of assessed risk. Chapter 17 owns the fraud subject matter; this chapter owns the integration point. |
| PCAOB | AS 2305, *Substantive Analytical Procedures* | Governs the analytical procedures used as risk assessment procedures in §2.5 and, at a higher evidential standard, the substantive analytics that Chapter 18 develops. |
| PCAOB | AS 2110 and AS 2201 together | The understanding of internal control obtained for risk assessment purposes is the same understanding that begins the top-down ICFR scoping; on an integrated audit the two are one exercise with two outputs. |
| PCAOB | AS 1215, *Audit Documentation* | Requires documentation of the risk assessment, the identified significant risks, and the linkage between assessed risks and the procedures performed. |
| PCAOB | AS 1301, *Communications with Audit Committees* | Requires communication of the significant risks identified. |
| AICPA | AU-C 315 (as revised by SAS 145), *Understanding the Entity and Its Environment and Assessing the Risks of Material Misstatement* | Effective for periods ending on or after December 15, 2023. Requires *separate* assessment of inherent risk and control risk at the assertion level; introduces "inherent risk factors" and the "spectrum of inherent risk"; requires that control risk be assessed at the maximum unless controls are expected to be tested for operating effectiveness; restates the system of internal control as five components; and requires identifying the risks arising from the use of information technology and the general IT controls that address them. This is the most substantive divergence from PCAOB standards in this chapter. |
| AICPA | AU-C 330, *Performing Audit Procedures in Response to Assessed Risks* | Private-company equivalent of AS 2301, including the requirement for substantive procedures specifically responsive to each significant risk. |
| AICPA | AU-C 240, *Consideration of Fraud in a Financial Statement Audit* | Private-company equivalent of AS 2401. |
| AICPA | AU-C 402, *Audit Considerations Relating to an Entity Using a Service Organization* | Relevant because eight of AtlasFlow's financially relevant systems are vendor-hosted; Chapter 11 owns the SOC 1 mechanics. |
| AICPA | AU-C 520, *Analytical Procedures*; AU-C 300; AU-C 230 | Analytical procedures, planning, and documentation equivalents. |
| FASB | ASC 606, *Revenue from Contracts with Customers* | The source of the subjectivity, complexity, and change inherent risk factors in the revenue rows of the matrix: performance obligation identification, standalone selling price allocation, variable consideration, contract modification accounting, and contract-term determination. |
| FASB | ASC 340-40 | Capitalization of incremental costs of obtaining a contract and the amortization period — the estimate underlying risks R-22 through R-25. |
| FASB | ASC 350-40 | Internal-use software capitalization and the project-stage judgment underlying R-26 through R-28. |
| FASB | ASC 718 | Stock-based compensation, including performance-condition probability assessment and market-condition valuation — R-29 through R-33. |
| FASB | ASC 805 and ASC 820 | Business combinations and fair value measurement — R-34 through R-38. |
| FASB | ASC 326 | Current expected credit losses — R-18. |

The divergence in the AU-C 315 row is worth stating plainly rather than in a footnote. Under AICPA standards you
**must** assess inherent risk and control risk separately at the assertion level, and you **must** assess control
risk at the maximum if you do not intend to test controls for operating effectiveness. Under PCAOB standards you
must assess the risk of material misstatement, and AS 1101 tells you that risk consists of inherent risk and
control risk, but the standards do not compel two separately documented ratings. Most firms, including
Brightline, require the separate ratings as a matter of methodology on both PCAOB and AICPA engagements, because
a single blended rating cannot be reviewed: a reviewer cannot tell whether "high" means the account is hard or
the controls are broken, and those two conditions call for different responses. When you present the separate
ratings on a PCAOB engagement, present them as firm methodology, not as a professional requirement.

## Prerequisites and Chapter Dependencies

Read Chapter 1 first. This chapter takes as given the business understanding developed in Chapter 1, §1.5 — the
metric vocabulary, the bookings-to-cash bridge, the ARR waterfall, the cohort deterioration, and the
metric-to-account pressure map in Exhibit 1-11 — and converts it into assertion-level risk assessments. It also
takes the scoping conclusions from Chapter 1, §1.6 and §1.7 as the boundary of what must be assessed. Chapter 3
supplies the materiality amounts used throughout ($1,450 overall, $940 performance, $72 clearly trivial) and
this chapter uses them without deriving them. Chapter 17 owns fraud risk assessment; this chapter covers only
the point at which the fraud assessment enters the general risk assessment. Chapters 11 through 14 develop the
control-side response, and Chapter 18 develops the analytics that this chapter introduces as risk assessment
procedures. Every chapter from 4 onward begins from the matrix in §2.12.

## 2.1 The Audit Risk Model and What It Actually Does

The model is a statement of relationships, not a calculator. Audit risk is the risk that the auditor expresses
an unmodified opinion on materially misstated financial statements. It is a function of the risk of material
misstatement (RMM) and detection risk (DR), and RMM is itself a function of inherent risk (IR) and control risk
(CR):

```text
Audit risk  =  RMM  ×  DR
            =  (IR × CR) × DR
```

Two properties of the model do real work in practice, and one does not.

**Property 1: RMM exists independently of the auditor.** Inherent risk and control risk are attributes of the
entity. The auditor assesses them; the auditor does not set them. If the RevPro configuration is wrong, the
misstatement exists whether or not Brightline finds it. This is why "we performed extensive testing, so risk is
low" is an inversion: testing changes detection risk, never RMM.

**Property 2: detection risk is the auditor's only lever, and it is set by the nature, timing, and extent of
further procedures.** Given a target audit risk and an assessed RMM, the acceptable detection risk follows. That
is the whole mechanism connecting §2.12 to Chapters 4 through 16.

**The property that does not work: arithmetic precision.** Assessments of "high," "moderate," and "low" are not
probabilities, and multiplying words produces nothing. The arithmetic below is illustrative of direction and
magnitude, not a computation any engagement performs.

**Exhibit 2-1. Illustrative effect of assessed risk on detection risk and testing extent, using the AtlasFlow
receivable population.**

| Scenario | IR | CR | RMM | Acceptable DR at 5% audit risk | Illustrative MUS sample size on the $38,600 gross receivable population at $940 tolerable misstatement |
| --- | --- | --- | --- | --- | --- |
| A. Controls tested and relied upon; account not estimate-heavy | 0.60 | 0.40 | 0.24 | 0.05 ÷ 0.24 = 20.8% | Reliability factor 1.9 at a 15% risk of incorrect acceptance: 38,600 × 1.9 ÷ 940 = **78 items** |
| B. Controls tested and relied upon; estimate-heavy account | 0.90 | 0.40 | 0.36 | 0.05 ÷ 0.36 = 13.9% | Reliability factor 2.3: 38,600 × 2.3 ÷ 940 = **95 items** |
| C. Controls not relied upon (CR at maximum); estimate-heavy account — **AtlasFlow's actual FY2025 position** | 0.90 | 1.00 | 0.90 | 0.05 ÷ 0.90 = 5.6% | Reliability factor 3.0 at a 5% risk of incorrect acceptance: 38,600 × 3.0 ÷ 940 = **123 items** |

Chapter 15 owns the sample size mechanics and the reliability factors; the point here is the shape of the
consequence. Moving from scenario A to scenario C increases the sample by 58% — 45 additional items — and that is
before considering that scenario C also changes the *nature* of the procedures (external confirmation rather
than examination of internal documents) and their *timing* (year end rather than interim). AtlasFlow lands in
scenario C for receivables because the aggregate ITGC deficiencies (W-1 through W-14) eliminated reliance on the
automated and IT-dependent controls in the order-to-cash cycle. That single conclusion, reached in Chapter 14,
costs the engagement several hundred hours across the revenue, receivable, and deferred revenue programs. It is
worth understanding early that control conclusions are not a compliance exercise separate from the substantive
audit; they are the largest single driver of substantive extent.

One further clarification of vocabulary, because it is a persistent source of error. **Audit risk** is
engagement-level and is not "assessed" at the assertion level. **RMM** is what you assess at the assertion
level. Writing "audit risk is high for revenue occurrence" is wrong; the correct statement is "the risk of
material misstatement for revenue occurrence is high."

## 2.2 Assessing Inherent Risk and Control Risk Separately

**Exhibit 2-2. What the two frameworks require.**

| Question | AICPA (AU-C 315, as revised by SAS 145) | PCAOB (AS 1101, AS 2110) |
| --- | --- | --- |
| Must inherent risk be assessed separately? | Yes, at the assertion level, for each identified risk of material misstatement | Not expressly required as a separate documented rating; AS 1101 identifies inherent risk as a component of RMM |
| Must control risk be assessed separately? | Yes | Not expressly required as a separate documented rating |
| Is there a floor on control risk when controls are not tested? | Yes. If the auditor does not plan to test operating effectiveness, control risk is assessed at the maximum, so RMM equals inherent risk | The same conclusion follows logically, and AS 2301 requires substantive procedures for all relevant assertions regardless, but it is not framed as a control risk floor |
| Is there a defined concept of a spectrum of inherent risk? | Yes | No equivalent defined term, though AS 2110 requires evaluating the likelihood and magnitude of potential misstatement |
| Are "inherent risk factors" defined? | Yes: subjectivity, complexity, uncertainty, change, and susceptibility to misstatement due to management bias or other fraud risk factors | Not as a defined list; AS 2110 enumerates factors to evaluate that overlap substantially |
| Practical consequence | The matrix in §2.12 is a required form of documentation | The matrix in §2.12 is firm methodology that satisfies the AS 2110 requirement to document the assessment and its basis |

The reason the separation matters is diagnostic. Consider two AtlasFlow assertions that both carry an RMM of
high:

- **Revenue, occurrence, for December-signed contracts.** Inherent risk is at the upper end of the spectrum:
  the accounting depends on a signature date and a provisioning date, the incentive to misstate is direct and
  large, and 41% of Q4 ACV was signed in five days. Control risk is also high, because Brett Hallowell can
  modify the order-form date field in Salesforce CPQ and there is no independent review of the change.
- **Convertible senior notes, accuracy, for the $170,600 carrying amount.** Inherent risk is low: a single
  instrument, a contractual coupon of 0.25%, straight-line-equivalent effective interest amortization of $5,400
  of issuance costs over five years, no separation of a conversion feature under ASU 2020-06, and no incentive.
  Control risk is high only in the trivial sense that AtlasFlow has few controls over an instrument it accounts
  for once a quarter.

If both are recorded as "high RMM," the audit plan will treat them alike, which is absurd. The revenue assertion
needs a redesigned test with external corroboration of dates; the notes assertion needs a recomputation that
takes two hours and will be right. Recording IR separately from CR makes the difference visible and makes the
response reviewable.

A second reason: the two components have different remedies. High control risk can be *reduced* by testing
controls and finding them effective. High inherent risk cannot be reduced at all — it is a property of the
transaction — and can only be responded to. Teams that blend the two frequently propose "more control testing"
as a response to an inherent risk, which cannot work.

## 2.3 The Inherent Risk Spectrum and the Inherent Risk Factors

AU-C 315 asks the auditor to place each identified inherent risk on a spectrum, using the combination of the
likelihood and the magnitude of a potential misstatement. The five inherent risk factors are the characteristics
of the underlying event or condition that drive that placement.

**Exhibit 2-3. The five inherent risk factors, with AtlasFlow examples.**

| Factor | What it means | AtlasFlow instance | Effect on likelihood and magnitude |
| --- | --- | --- | --- |
| **Subjectivity** | The accounting requires management to choose among acceptable alternatives, and the choice is not determinable from the transaction | Standalone selling price for the Insight module: 31 standalone sales across a price band with an interquartile range of 22% of list | Likelihood high (many acceptable answers), magnitude high (the SSP allocates revenue across nearly every FY2025 multi-element contract) |
| **Complexity** | The accounting or the process for producing the amount involves numerous or intricate steps | The RevPro engine's 27 configuration rules translating order forms into revenue schedules, including ramps, modifications, and multi-currency contracts | Likelihood high, magnitude high; a single mis-specified rule can misstate a whole class |
| **Uncertainty** | The amount depends on future events or conditions not yet knowable | The four-year period of benefit for capitalized commissions, the CECL reasonable-and-supportable forecast, the Kestrel earn-out's revenue-and-retention milestone | Likelihood moderate to high, magnitude bounded by the recorded amount |
| **Change** | The condition, the accounting, the system, or the personnel changed during the period | Insight launched January 2025; RevPro reconfigured February 2025; two revenue accountants resigned in Q2; Kestrel acquired August 2025; NetSuite upgraded September 2025; CFO changed September 2025 | Likelihood raised across the board; magnitude depends on the affected population |
| **Susceptibility to management bias or other fraud risk factors** | An incentive, opportunity, or attitude exists that could cause the amount to be biased or misstated intentionally | CRO compensated on bookings, CEO compensated on ARR-based PSUs, Q4 "close the quarter" incentives, the ARR-based PSU tranche revised from 100% to 85% probable, and the January 2026 whistleblower allegation | Likelihood high for revenue cut-off and for the estimates management controls; magnitude potentially large |

Placement on the spectrum is a judgment, and it is worth being explicit about how Brightline expressed it,
because the four-point scale in the matrix is a firm convention and not a standard requirement.

| Position | Label used in this chapter | Meaning | Typical AtlasFlow example |
| --- | --- | --- | --- |
| Lower end | **Low** | No inherent risk factor is present to a meaningful degree; the amount is determinable from the transaction | Convertible note coupon accrual |
| Lower middle | **Moderate** | One factor is present, and the population is homogeneous | Operating lease liability remeasurement |
| Upper middle | **Elevated** | Two or more factors are present, or one factor is present acutely, but the combination of likelihood and magnitude falls short of the top of the spectrum | Current/noncurrent split of deferred revenue |
| Upper end | **High** | The combination of likelihood and magnitude places the risk close to the top of the spectrum; this is the population from which significant risks are drawn | Insight SSP; December revenue cut-off; CECL allowance |

Two disciplines keep this honest. First, if more than roughly a quarter of the assessed risks land at the upper
end, the scale has collapsed and the assessment carries no information; on the AtlasFlow matrix, 9 of 38 risks
are assessed at the upper end, and those nine are precisely the nine significant risks — not a coincidence but a
definitional consequence, because a significant risk is defined by its position on the inherent risk spectrum.
Second, the placement must be justified by *which factors* are present,
not by the size of the account. Convertible notes of $170,600 are 117.7 times materiality and sit at the lower
end of the inherent risk spectrum. Contingent consideration of $2,500 is 1.7 times materiality and sits at the
upper end.

## 2.4 Understanding the Entity, Its Environment, and the Applicable Framework

The understanding required is not general knowledge; it is the specific knowledge that lets you predict what the
financial statements should look like and identify what could make them look different. AS 2110 organizes it into
categories. What follows is those categories populated for AtlasFlow, with the risk each one generates.

**Exhibit 2-4. Understanding obtained and the risk it identifies.**

| Category | AtlasFlow understanding | Risk it points to |
| --- | --- | --- |
| Industry, regulatory, and other external factors | Mid-market and enterprise workflow automation; competitive pricing pressure evidenced by the April 2025 list-price increase of 8% with existing customers grandfathered for one renewal cycle; SEC reporting as a large accelerated filer for the first time | Grandfathering creates a population of renewals priced below current list, which is direct evidence bearing on standalone selling price and on discount allocation |
| Nature of the entity — operations | Four revenue streams with four different recognition models: Core and Insight (ratable series), usage overage (as consumed), professional services (input-method over time); a self-serve channel of 11,400 accounts processed through Stripe on an entirely separate system path | Four models means four sets of assertions; the self-serve channel is individually immaterial and collectively material at $6,100, and cannot be excluded by magnitude |
| Nature of the entity — ownership and governance | Founder-CEO with compensation weighted to ARR-based PSUs; audit committee chaired by a designated financial expert and former public-company CFO; internal audit reporting to the committee | The CEO's compensation creates a direct incentive at the ARR metric, which flows into the PSU probability estimate — an accounting estimate the CEO's own compensation depends on |
| Nature of the entity — investments and financing | $175,000 of convertible senior notes at 0.25% due 2029, capped calls of $14,700 recorded against APIC, an undrawn $50,000 revolver with a $40,000 minimum-liquidity covenant, and $150,600 of cash and short-term investments | Covenant compliance is not currently at risk ($150,600 against a $40,000 floor), which lowers the going-concern and covenant-manipulation risk relative to a leveraged company. Say so; a risk assessment that never rules anything out is not an assessment |
| Objectives, strategies, and related business risks | Growth strategy dependent on expansion within the installed base, with NRR falling from 118% to 112% and GRR from 93% to 91%; a January 2025 new SKU; an August 2025 acquisition | Expansion-dependent growth under pressure is the pressure source behind revenue cut-off, SSP allocation, and metric manipulation |
| Measurement and review of financial performance | ARR, NRR, GRR, RPO, customers with ARR ≥ $100K, and bookings, all reviewed monthly by the board; ARR and NRR produced from a Snowflake datamart not reconciled to the general ledger for the first three quarters | The measures management is judged on are computed outside the system of internal control over financial reporting |
| The applicable financial reporting framework | US GAAP. The framework choices that matter: the "series" conclusion under ASC 606 making a subscription a single performance obligation; the ASC 340-40 four-year amortization period; the ASU 2020-06 single-liability treatment of the notes; forfeitures of equity awards recognized as they occur | Each framework choice is a place where a change in facts would require a change in accounting that management has an incentive not to make |
| The entity's system of internal control | See §2.10. Twenty financially relevant applications, nine interfaces, a spreadsheet consolidation, and 14 identified gaps | Control risk at or near maximum for most revenue-cycle assertions |
| Personnel and capacity | Elena Vasquez is the single point of failure in the close; Daniel Kim, who owns the RevPro configuration, has been on a performance plan since March 2025; two revenue accountants resigned in Q2 2025; Tom Okafor is in his first public-company CFO role | Capacity and competence risk concentrated precisely in the revenue cycle, which is where the highest inherent risks sit |

The last row is the one that most often gets written as an observation and never converted into a risk. Two
revenue accountants resigning in Q2 from a team whose VP is on a performance plan is not a human resources fact;
it is evidence about the operating effectiveness of every manual revenue control for the remainder of the year,
about the completeness of the RevPro exception clearing performed by Jordan Pike, and about whether the
February 2025 configuration change was ever validated by someone who understood it. Chapter 13's case study is a
control that turned out not to exist as documented; that is the shape this risk takes when it materializes.

## 2.5 The Required Risk Assessment Procedures

AS 2110 requires the auditor to perform risk assessment procedures, and it specifies the types: inquiry,
analytical procedures, and observation and inspection, together with reading minutes, considering information
from client acceptance and continuance and from prior audits, and performing preliminary engagement activities.
The requirement is often satisfied on paper by three memoranda and no evidence. What follows is what Brightline
actually did, with dates and outputs.

**Exhibit 2-5. Risk assessment procedures performed, FY2025 (WP 2100 series).**

| Procedure type | What was done | Date | Output that changed the assessment |
| --- | --- | --- | --- |
| Inquiry — management | Structured interviews with Tom Okafor (CFO), Elena Vasquez (CAO/Controller), Daniel Kim (VP Revenue Accounting), Aisha Bello (Technical Accounting), Jordan Pike (Revenue Manager) | Aug 18–29, 2025 | Kim disclosed that the February 2025 RevPro configuration change went live with abbreviated user acceptance testing because the ramp-contract deadline was driven by a Q1 close date. This raised R-4 from moderate to elevated |
| Inquiry — outside the financial reporting function | Brett Hallowell (VP Sales Operations), Sofia Marchetti (CRO), Vikram Shah (CTO), Ray Sandoval (IT and Information Security), Nate Oyelaran (Treasury) | Aug 25 – Sep 12, 2025 | Marchetti described the Q4 "close the quarter" incentive structure and confirmed commissions are paid on signature date rather than start date. Hallowell confirmed he can modify the order-form date field in CPQ and that no one reviews such changes. Both feed the case study in this chapter |
| Inquiry — audit committee | Dr. Helen Ashford, in executive session with no management present | Sep 30, 2025 | Ashford disclosed that the committee had asked management in July for a bookings-quality analysis and had not received one. This is a control environment observation with direct bearing on R-1 and R-2 |
| Inquiry — internal audit | Michelle Fong; read the July 2025 ITGC readiness assessment in full | Sep 4, 2025 | The 14 gaps, and the fact that no revenue-cycle process controls were within internal audit's FY2025 plan |
| Inquiry — others | Two revenue accountants who resigned in Q2 2025 were not available. Brightline inquired of the two replacements hired in August 2025 about the completeness of the RevPro exception queue | Sep 15, 2025 | Neither replacement could describe the population of open interface exceptions at the time they joined, which is evidence about the completeness of exception clearing between April and August |
| Analytical procedures | Preliminary analytics on FY2025 year-to-date and annualized results against FY2024, disaggregated by quarter and revenue stream (Exhibit 2-6) | Sep 2, 2025, updated Dec 15, 2025 | Identified the Q4 usage overage anomaly and the subscription gross margin improvement |
| Observation and inspection | Observed the December 2025 month-end close in FloQast; inspected 27 RevPro configuration rules with Ben Osei; inspected the CPQ approval matrix; inspected the consolidation workbook's formula structure | Sep 8–19 and Dec 15, 2025 | Inspection of the consolidation workbook identified 4 hard-keyed cells overriding formulas in the FX translation tab, which is the concrete form of W-8 |
| Reading minutes | Board and audit committee minutes, January 2025 through September 2025, plus the compensation committee minutes for the PSU tranche assessment | Aug 26, 2025 | The compensation committee discussed the ARR-based PSU tranche in July 2025 and recorded that achievement was "tracking behind plan" — two months before management assessed the tranche as 100% probable in Q3. This is the single most important document the risk assessment produced |
| Prior-period information | FY2024 uncorrected misstatements, the FY2024 summary of audit differences, and the FY2024 retrospective review of estimates | Aug 20, 2025 | The FY2024 accrued commission misstatement that turns around as U-6 ($130) |
| Preliminary engagement activities | Continuance (Chapter 1, §1.1), independence (§1.2), engagement letter (§1.3) | Jun–Jul 2025 | Four conditions attached to continuance |

Two comments on Exhibit 2-5. First, note how many of the assessment-changing outputs came from inquiries of
people outside the finance function and from reading documents rather than from asking the Controller what the
risks were. The July compensation committee minute recording that the ARR-based PSU tranche was "tracking behind
plan" is directly contradictory to management's Q3 assessment of 100% probability, and no amount of inquiry of
management would have produced it. Second, note that one inquiry produced nothing usable — the resigned revenue
accountants were unavailable — and that this is itself documented. A risk assessment file that shows only
successful procedures is not a record of what happened.

**Exhibit 2-6. Preliminary analytical procedures, FY2025 versus FY2024 (dollars in thousands). Investigation
flag: relative change above 5% combined with an absolute effect above $940, or any relationship inconsistent
with the business model.**

| Relationship | FY2024 | FY2025 | Change | Flag | Risk implication |
| --- | --- | --- | --- | --- | --- |
| Total revenue | 118,900 | 148,200 | +24.6% | — | Consistent with ARR growth of 25.2%; no flag |
| Subscription revenue | 108,300 | 135,800 | +25.4% | — | Consistent |
| Professional services revenue | 10,600 | 12,400 | +17.0% | — | Grows more slowly than subscription, consistent with the reseller-performed implementations described in §4.4 |
| Subscription gross margin | 78.6% | 80.0% | +1.4 pp | **Flag** | A 1.4-point improvement on $135,800 is $1,901 of margin, above performance materiality. Candidate causes: hosting efficiency, or reclassification of support and DevOps personnel from account 5110 to R&D. R-32 and Chapter 10 |
| Professional services gross margin | 2.0% | 5.0% | +3.0 pp | Flag, small | $372 of effect; below performance materiality but relevant to the input-method estimate (R-8) |
| Deferred revenue | 62,300 | 78,200 | +25.5% | — | Tracks subscription revenue growth of 25.4% almost exactly, which is corroborative of both. Deferred revenue growing *more slowly* than revenue is the classic indicator of pulled-forward recognition, and it is absent here |
| Gross accounts receivable | 30,500 | 38,600 | +26.6% | Flag | Grows 2.0 points faster than revenue; combined with the DSO move, points to R-17 and R-18 |
| Allowance as a percentage of gross receivables | 4.43% | 4.92% | +0.49 pp | — | The allowance rose, which is the direction one would expect; the question is whether it rose enough. At FY2024's rate the allowance would be $1,710, so the increase beyond proportionality is $190 |
| Q4 days sales outstanding | 61 days | 68 days | +11.5% | **Flag** | Implies roughly $4,000 of receivables that would not exist at prior-year collection velocity. R-17, R-18 |
| Deferred contract acquisition costs | 19,500 | 24,000 | +23.1% | — | Grows slightly more slowly than revenue, which is consistent with the practical-expedient expensing of self-serve commissions |
| Implied remaining amortization period of the commission asset (closing balance ÷ current-year amortization) | 3.05 years | 2.79 years | −0.26 years | Flag | The implied remaining life is shortening while the stated period of benefit stays at four years. Not a misstatement, but an indicator worth carrying into R-23 |
| Capitalized internal-use software, net | 13,400 | 18,600 | +38.8% | **Flag** | Grows 14.2 points faster than revenue and 19.2 points faster than R&D expense (+19.6%). Capitalized additions of $10,900 are 24.8% of R&D expense against 20.7% in FY2024. R-26 |
| Stock-based compensation as a percentage of revenue | 19.3% | 19.4% | +0.1 pp | — | Stable; no flag at the aggregate level. The risk is in the PSU probability, not the total |
| General and administrative as a percentage of revenue | 16.7% | 17.8% | +1.1 pp | — | Expected: first-year public-company compliance costs, the CFO transition, and higher audit fees |
| Revenue per employee | 174.1 | 182.5 | +4.8% | — | Modest improvement; consistent with a 24.6% revenue increase against headcount growth from 683 to 812 (+18.9%) |

**Exhibit 2-7. Quarterly disaggregation of FY2025 revenue and sequential growth (in thousands).**

| Stream | Q1 | Q2 | Q3 | Q4 | FY | Q2 seq. | Q3 seq. | Q4 seq. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Core subscription | 24,100 | 25,700 | 26,900 | 28,200 | 104,900 | +6.6% | +4.7% | +4.8% |
| Insight subscription | 5,400 | 6,300 | 7,200 | 7,800 | 26,700 | +16.7% | +14.3% | +8.3% |
| Usage overage | 780 | 940 | 1,090 | 1,390 | 4,200 | +20.5% | +16.0% | **+27.5%** |
| Professional services | 2,700 | 3,100 | 3,200 | 3,400 | 12,400 | +14.8% | +3.2% | +6.3% |
| **Total** | **32,980** | **36,040** | **38,390** | **40,790** | **148,200** | +9.3% | +6.5% | +6.3% |

The Q4 usage overage figure is the finding. Overage is consumption above a committed volume, so in a business
whose subscription base grew 4.8% sequentially in Q4, overage growing 27.5% sequentially requires an explanation.
There are three innocent ones — seasonality in customer workflow volumes, the Insight module driving incremental
run consumption, and a large customer crossing its committed threshold late in the year — and two that are not:
the workflow-run data feeding the overage calculation is produced by the platform rather than by a financial
system and is not subject to the ITGC set, and overage is billed in arrears, making it the one revenue stream
where recognition precedes billing and therefore where an accrual estimate exists. This is why R-5 is in the
matrix at an elevated inherent risk with completeness *and* occurrence as relevant assertions. Chapter 5 owns the
usage-data completeness procedures and Chapter 18, §18.4 owns the disaggregation principle that surfaced it.

A note on what these procedures are and are not. Analytical procedures performed for risk assessment need not
meet the precision requirements of AS 2305 or AU-C 520 that apply to a substantive analytical procedure, because
they are not being used to obtain substantive evidence. Their purpose is to identify unusual or unexpected
relationships. It follows that an unexplained flag in Exhibit 2-6 does not have to be resolved at the risk
assessment stage; it has to be converted into a risk in the matrix. Teams routinely make the opposite mistake and
spend interim hours "clearing" preliminary analytics, which produces neither risk assessment nor substantive
evidence.

## 2.6 The Engagement Team Discussion

AS 2110 requires a discussion among key engagement team members, including the engagement partner, about the
risks of material misstatement; AS 2401 requires a discussion directed at fraud. Brightline holds one meeting
covering both, which is permitted and which is better practice because the fraud discussion is unproductive when
severed from the discussion of how the business works.

The discussion is the single most commonly wasted three hours on an engagement. It fails when it becomes a
briefing — the manager describes the client, everyone nods, a memo is written — because the required output is not
a shared understanding, it is a set of assertion-level risks that nobody would have identified alone. The
walkthrough later in this chapter executes the meeting step by step. This section covers the design.

**Exhibit 2-8. FY2025 engagement team discussion — design (WP 2200-01).**

| Element | Brightline's choice | Why |
| --- | --- | --- |
| Date and duration | October 7, 2025, 3 hours 30 minutes | After the walkthroughs (September 8–19) and after the audit committee inquiry (September 30), so participants bring evidence rather than expectations; before interim controls testing begins October 20, so the output can shape the programs |
| Location and format | In person in Austin, with the UK component senior manager and Dr. Petrov by video | In-person for the core team; the discussion depends on people interrupting each other |
| Required attendees | Whitcombe (partner), Lindqvist (senior manager), Haddad (manager), Nwosu (senior), Nazari (IT senior manager), Osei (IT senior), Iyer (data and analytics), Stein (tax partner) | AS 2110 requires the engagement partner and key team members. The IT auditors are key members on this engagement, not guests |
| Attendees for part | Trent and Park (staff) for the full session; Petrov for 30 minutes on the Kestrel earn-out and the TSR PSUs; the Brightline UK senior manager for 45 minutes | Staff attend the whole session because they perform the procedures the discussion designs |
| Engagement quality reviewer | Herrera attended for 45 minutes as an observer and did not participate in the decisions | Permissible and useful; his objectivity depends on his not making the engagement's judgments, not on his ignorance of them |
| Pre-reading circulated October 2 | The FY2024 significant matters memo; the internal audit readiness assessment; the change register; Exhibits 2-6 and 2-7; the compensation committee minute on the PSU tranche; the metric-to-account pressure map (Exhibit 1-11) | A discussion in which people read the materials during the meeting produces the manager's views restated |
| Required outputs | (1) A list of candidate risks stated as account plus assertion plus direction; (2) an initial spectrum placement for each; (3) identification of candidate significant risks; (4) the specific procedures that would not otherwise have been performed; (5) an action list with owners and dates | Without output (4) the discussion cannot be shown to have changed anything |
| Documentation | A three-page memo with the participants, the matters discussed, the risks identified, the conclusions reached, and the action list; the memo names who raised each risk | Naming the source makes the record verifiable and, in practice, makes people contribute |

The design choice worth arguing about is holding one meeting rather than two. The argument for separating the
fraud discussion is that a dedicated session forces participants to think adversarially rather than
procedurally. The argument for combining, which Brightline follows, is that the fraud discussion has to be
grounded in the specific mechanics of the business to produce anything — you cannot brainstorm how AtlasFlow's
December revenue could be manipulated without first establishing that Brett Hallowell can modify the order-form
date field, that commissions are paid on signature date, and that a January 1 start date generates zero
current-year revenue. Combining works only if the agenda protects the adversarial segment; Brightline reserved
75 of the 210 minutes for it and required each participant to arrive with one written scheme.

## 2.7 Identifying Risks of Material Misstatement at the Assertion Level

A risk of material misstatement is not "revenue." It is a statement of the form: *this specific thing could go
wrong, in the [account], affecting the [assertion], in the [direction], because of [cause], and the amount could
be [magnitude]*. If any of the five slots is empty, the response cannot be designed.

An assertion is a **relevant assertion** if there is a reasonable possibility that a misstatement of that
assertion would be material. Relevance is not the same as applicability. Rights and obligations applies to every
receivable; it is relevant for AtlasFlow's receivables only in the narrow sense of the reseller arrangements,
where the question is whether AtlasFlow or Tessera Partners holds the right to consideration from Cirrus. Saying
"all assertions are relevant" is the same failure as rating everything high.

**Exhibit 2-9. Assertions and their relevance for AtlasFlow's principal accounts.**

| Assertion | What it asserts | Where it is relevant at AtlasFlow, and where it is not |
| --- | --- | --- |
| Occurrence (transactions) | Recorded transactions occurred and pertain to the entity | Highly relevant to revenue: a December-signed contract that was actually signed in January did not occur in FY2025. Relevant to the $340 of Kestrel post-acquisition revenue |
| Completeness | All transactions and balances that should be recorded are recorded | The dominant assertion for deferred revenue, accrued liabilities, and SLA credits. Also the dominant assertion for usage overage, where the population of workflow runs originates outside the financial systems. Less relevant for revenue, where the incentive runs toward overstatement |
| Accuracy | Amounts and other data are recorded appropriately | Relevant everywhere; acute where an allocation drives the amount (SSP), where a configuration drives the amount (RevPro's 27 rules), or where a rate drives the amount (commission rates, FX) |
| Cut-off | Transactions are recorded in the correct period | The highest-risk assertion on the engagement, for revenue and for the commission accrual |
| Classification | Transactions are recorded in the proper accounts | Relevant to cost of revenue versus R&D (gross margin sensitivity), to current versus noncurrent deferred revenue, and to the cash flow statement's operating/investing split |
| Existence (balances) | Recorded assets, liabilities, and equity exist | Relevant to receivables, capitalized commissions on churned customers, and capitalized software for projects abandoned or restaged |
| Rights and obligations | The entity holds or controls the rights to assets, and liabilities are its obligations | Narrowly relevant: the reseller arrangements ($9,700 of FY2025 revenue), and the enforceability question on C-5 Pemberton's termination-for-convenience clause |
| Valuation and allocation | Balances are included at appropriate amounts and resulting adjustments are recorded | The dominant assertion for the CECL allowance, the commission amortization period, the Kestrel contingent consideration, and the acquired intangibles |
| Presentation and disclosure | Information is appropriately presented and described, and disclosures are relevant and understandable | Relevant to the RPO disclosure, revenue disaggregation, the Kestrel ICFR exclusion disclosure, and the going-concern and liquidity discussion |

The technique for populating the matrix is to work from the *process*, not from the account. For each point in
the order-to-cash cycle, ask what could go wrong and which assertion it would affect. A quote approved at a
non-permitted discount affects accuracy through the transaction price. An order form activated in Zuora with the
wrong start date affects cut-off and occurrence. A modification processed as a separate contract rather than a
cumulative catch-up affects accuracy and cut-off. An interface exception left uncleared affects completeness. A
manual journal entry to account 4100 with a non-standard offset affects occurrence and accuracy. Five process
points, five assertions, five rows.

The direction of the potential misstatement is the slot teams most often leave empty, and it is the slot that
determines the test. If the risk is that revenue is overstated, you test recorded revenue and you look for
recorded items that should not be there — a test that starts from the general ledger. If the risk is that
deferred revenue is understated, you cannot find it by testing what is recorded; you must start from a
population outside the accounting records, such as the complete order form population or the complete Zuora
subscription list. Completeness risks require a source-to-record direction. Occurrence risks require a
record-to-source direction. A program that tests only in one direction has responded to only one of the two.

## 2.8 Significant Risks

A **significant risk** is a defined term, and it is not a synonym for a high risk. Under AU-C 315, a significant
risk is an identified risk of material misstatement for which the assessment of inherent risk is close to the
upper end of the spectrum of inherent risk, because of the degree to which the inherent risk factors affect the
combination of the likelihood and the magnitude of a potential misstatement — or one that is required to be
treated as a significant risk by another AU-C section. Under PCAOB AS 2110 a significant risk is a risk of
material misstatement that requires special audit consideration. Note what the AICPA definition does *not*
include: control risk. A significant risk is determined from inherent risk alone. Effective controls do not
convert a significant risk into an ordinary one; they change the response, not the classification.

**Exhibit 2-10. Consequences that follow from designating a risk as significant.**

| Consequence | Source | What it means in practice at AtlasFlow |
| --- | --- | --- |
| Substantive procedures must be specifically responsive to the risk | AS 2301; AU-C 330 | The response to R-2 cannot be "our normal revenue testing"; it must be a procedure designed for signature-date corroboration |
| Reliance on evidence from prior periods for controls addressing the risk is limited | AS 2201; AU-C 330 | The CPQ approval configuration cannot be benchmarked from FY2024 because FY2025 is the first year of the ICFR audit and the configuration changed |
| Controls addressing the risk must be evaluated, and in an integrated audit tested | AS 2201 | The nine significant risks drive the control selection in Chapters 11 and 12 |
| Substantive analytical procedures alone are not sufficient | AS 2305; AU-C 330 | The Insight SSP risk cannot be addressed by a trend analysis |
| The risk must be communicated to the audit committee | AS 1301; AU-C 260 | Item 4 of the September 30, 2025 planning communication |
| The risk and the basis for the determination must be documented | AS 1215; AU-C 230 | The rationale column in §2.12 |

Brightline identified nine significant risks for FY2025:

| Ref | Significant risk | Why it reaches the upper end of the spectrum |
| --- | --- | --- |
| R-1 | Subscription revenue recognized before the service commences (occurrence, cut-off) | Change (Insight launch, RevPro reconfiguration), bias (bookings and ARR incentives), and a prior-year instance of the same error corrected as C-1 ($410) |
| R-2 | Contracts recorded in FY2025 that were not executed in FY2025 (occurrence, cut-off) | Bias acute: 41% of Q4 ACV signed in five days, commissions paid on signature date, an editable date field with no review, and a whistleblower allegation. Fraud risk under AS 2401 |
| R-3 | Standalone selling price for the Insight module misestimated, misallocating the transaction price (accuracy, allocation) | Subjectivity acute: 31 standalone sales, 22% interquartile range; change (SKU launched January 2025); affects nearly every FY2025 multi-element contract |
| R-10 | Manual journal entries used to adjust revenue or deferred revenue outside the normal process (occurrence, accuracy, cut-off) | Bias plus opportunity: 4,912 manual entries, 3,847 below the approval threshold, 34 hitting revenue with a non-standard offset. Management override is presumed a significant risk under AS 2401 |
| R-13 | Deferred revenue understated because billings were recognized as revenue prematurely or a performance obligation was omitted (completeness) | The mirror of R-1 and R-3, with a population that cannot be tested from the recorded balance |
| R-18 | Allowance for credit losses understated (valuation) | Subjectivity and uncertainty: a CECL forecast overlay, gross retention falling to 91%, DSO to 68 days, and management's estimate at the optimistic end of the acceptable range (U-2, $240) |
| R-26 | Internal-use software capitalized in the wrong project stage (existence, accuracy) | Subjectivity plus bias: 22% of capitalized hours coded to Jira epics restaged retroactively, with time reports approved by the managers who own the project budgets |
| R-29 | ARR-based PSU probability assessment (accuracy, occurrence, cut-off) | Subjectivity plus acute bias: the CEO's compensation depends on the same metric, the July compensation committee minute records "tracking behind plan," and the Q4 revision produced a $1,340 credit |
| R-34 | Kestrel contingent consideration fair value (valuation) | Subjectivity, uncertainty, and complexity: Monte Carlo simulation, 32% assumed revenue volatility, 11.5% discount rate, a first-time acquirer, and a $4,000 maximum payout against a $2,500 recorded amount |

Nine significant risks out of 38 identified risks is toward the high end of the range one sees in practice, which
runs from roughly three on a stable, single-product engagement to perhaps a dozen on a first-year integrated
audit with an acquisition and a fraud allegation. The number is not itself a quality measure, but two failure
modes bracket it. Designating two significant risks on an engagement with AtlasFlow's facts would mean the SSP
subjectivity or the December cut-off was not recognized. Designating twenty would drain the concept of meaning
and would trigger the AS 2301 requirement for specifically responsive substantive procedures in twenty places,
which the budget cannot absorb; the practical consequence would be twenty thin responses instead of nine strong
ones.

Note two designations that Brightline did *not* make. Revenue completeness is not a significant risk: the
incentive at AtlasFlow runs toward overstatement, subscription billing is system-generated from activated
subscriptions, and the deferred revenue growth of 25.5% tracking subscription revenue growth of 25.4% is
corroborative. And the convertible notes are not a significant risk despite a $170,600 carrying amount, because
none of the inherent risk factors is present. Both non-designations are documented with their reasons, because a
risk assessment that records only what was included cannot show that anything was considered and rejected.

## 2.9 Risks Arising from the Use of Information Technology

AU-C 315 requires the auditor to identify the risks arising from the use of information technology and the
general IT controls that address those risks. The distinction is the whole point, and it is routinely collapsed.
A risk arising from IT is a *risk* — a way in which the entity's use of technology could cause a financial
statement misstatement. A general IT control is a *control* that addresses such a risk. "There is no periodic
user access review" is not a risk arising from IT; it is a missing control. The risk is that a user with
inappropriate access initiates or records an unauthorized transaction or overrides a configured control.

**Exhibit 2-11. Risks arising from the use of IT at AtlasFlow, and the assertions they touch.**

| Ref | Risk arising from IT | How it could cause a misstatement | Accounts and assertions affected | Related gap |
| --- | --- | --- | --- | --- |
| IT-1 | Inappropriate access to the Zuora Revenue configuration | A change to any of the 27 configuration rules alters the revenue schedules for an entire class of contracts without a transaction-level trace | Revenue accuracy, cut-off; deferred revenue completeness, accuracy | W-1 (four non-federated admin accounts, one shared), W-6 (two developers with standing production write access) |
| IT-2 | Unauthorized or unvalidated program changes in the revenue and billing chain | The February 2025 RevPro configuration change deployed with abbreviated UAT could mis-specify ramp handling on the 34% of ACV in multi-year contracts | Revenue accuracy; deferred revenue accuracy | The February 2025 change; W-4 (6 of 3,100 deployments without a ticket) |
| IT-3 | Excessive or unsegregated access in the general ledger | 11 users retained the legacy Full Access role for 27 days after the September NetSuite upgrade; the Controller can both prepare and post entries and modify the interface mapping | All accounts, occurrence and accuracy; journal entry integrity | W-2, W-13 |
| IT-4 | Access not removed on termination | Terminated users averaged 6.2 days to removal against a 24-hour SLA; three retained Salesforce access beyond 30 days, and the October restructuring eliminated 41 positions | Revenue occurrence (CPQ), expenditure occurrence | W-5 |
| IT-5 | Reliance on an interface whose failures are not detected | I-4, the Stripe-to-NetSuite daily summary journal, is in-house Lambda code with two undocumented FY2025 modifications; I-2's exception queue is cleared by one person | Revenue completeness ($6,100 of self-serve revenue); cash completeness | W-7 |
| IT-6 | Reports and extracts used as audit evidence or in controls are not complete and accurate | The RevPro "Revenue Contract Summary," the Zuora aged trial balance, and every Snowflake extract are information produced by the entity whose parameters and underlying query must be tested | Every assertion that relies on an entity-produced report | W-11 |
| IT-7 | Financial reporting performed outside a controlled application | The consolidation workbook has no version control, no formula-integrity check, four hard-keyed overrides in the FX tab, and 27 top-side entries totaling $6,200 | Consolidation accuracy; FX translation accuracy; completeness of the journal entry population | W-8 |
| IT-8 | Metrics reported to investors produced outside the system of internal control over financial reporting | The Snowflake RevOps datamart produces ARR and NRR for MD&A and was not reconciled to the general ledger for three quarters | Presentation of other information; indirectly the PSU probability estimate | W-11 |
| IT-9 | Reliance on service organizations without coverage for the full period or mapping of user entity controls | Zuora's and Deel's SOC 1 reports cover periods ending September 30, 2025 with no bridge letters; the AWS and Zuora CUECs were never mapped to AtlasFlow controls; Deel's report is qualified as to change management | Revenue accuracy; payroll accuracy and completeness | W-9, W-10 |

The output of this section is not a control conclusion. It is the recognition that nine identified IT risks touch
almost every relevant assertion in the matrix, which is why the control risk column in §2.12 reads "High" or
"Maximum" for so many rows and why the substantive response in Chapters 4 through 10 is heavier than it would
otherwise be. Chapter 11 owns the ITGC response and Chapter 12 owns the application controls; Chapter 14 owns the
severity evaluation that ultimately concluded these deficiencies aggregate to a material weakness.

## 2.10 The System of Internal Control and Identifying Controls Relevant to the Audit

AU-C 315 as revised describes the system of internal control in five components. The PCAOB, following COSO, uses
the same five with slightly different names. Understanding all five is required; the depth of understanding
required differs, and only some controls within them are relevant to the audit.

**Exhibit 2-12. The five components at AtlasFlow.**

| Component (AICPA name / COSO name) | What the auditor must understand | AtlasFlow findings | Effect on the assessment |
| --- | --- | --- | --- |
| **Control environment** / Control environment | Management's commitment to integrity and ethical values, oversight by those charged with governance, organizational structure, commitment to competence, and accountability | Audit committee chaired by a designated financial expert who asked for a bookings-quality analysis and did not receive one; a first-time public-company CFO; the CAO as a single point of failure; the VP Revenue Accounting on a performance plan; two revenue accountants resigned; a whistleblower channel that functioned | Mixed. The governance layer is a strength; the competence-and-capacity layer is a weakness precisely where inherent risk is highest. A weak control environment cannot be compensated by process-level controls, so this finding raises RMM at the financial statement level, not just at particular assertions |
| **The entity's risk assessment process** / Risk assessment | How the entity identifies business risks relevant to financial reporting, estimates their significance, and addresses the risk of fraud and of change | Management performed its first full 404(a) risk assessment in FY2025, with internal audit's assistance. It did not identify the Snowflake datamart as within the financial reporting chain, and it scoped Kestrel out entirely | Management's risk assessment missed two areas the auditor identified. That is itself evidence about the component |
| **The entity's process to monitor the system of internal control** / Monitoring | How the entity evaluates the effectiveness of controls and remediates deficiencies | Internal audit's July 2025 readiness assessment identified 14 gaps; Vanta provides continuous compliance monitoring, and management sometimes offers Vanta screenshots as control evidence; backup restoration testing was performed once and failed, with the retest not completed until January 2026 | Monitoring identified the gaps but did not drive timely remediation. Offering a compliance-monitoring tool's output as control evidence indicates the entity does not distinguish monitoring from control operation |
| **Information system and communication** / Information and communication | How transactions are initiated, authorized, processed, recorded, and reported, including the accounting records, the IT environment, and the financial reporting process, and how roles are communicated | Twenty financially relevant applications, nine interfaces, a spreadsheet consolidation. The revenue subledger is a vendor-hosted engine whose configuration is the control. The close is managed in FloQast with dated sign-offs | This is where the audit is designed. The understanding must be at transaction-flow level, which is what the Chapter 13 walkthroughs produce |
| **Control activities** / Control activities | The controls that address the risks of material misstatement at the assertion level, including automated controls, IT-dependent manual controls, and general IT controls | Identified in Exhibit 2-13 | Only the controls relevant to the audit are identified and evaluated in detail |

The first component deserves emphasis because it operates differently from the other four. Deficiencies in the
control environment are *pervasive*: they raise the risk of material misstatement across the financial statements
rather than at particular assertions, and they cannot be compensated for by a strong process-level control.
AtlasFlow's specific control environment finding — that competence and capacity are thinnest in revenue
accounting, which is where inherent risk is highest — is the reason Brightline's FY2025 strategy contemplated an
adverse ICFR opinion in September rather than in February.

### 2.10.1 Which controls are relevant to the audit

A control is relevant to the audit if it addresses a risk of material misstatement at an assertion the auditor
has identified as relevant. On an integrated audit the population expands: AS 2201 requires testing controls
sufficient to support an opinion on ICFR effectiveness, which includes controls over all relevant assertions of
all significant accounts and disclosures, not only the ones on which the auditor intends to rely for substantive
purposes. That is one of the largest practical differences between a financial statement audit and an integrated
audit, and it is where 1,370 of AtlasFlow's 2,700 incremental hours go.

**Exhibit 2-13. Controls identified as relevant to the audit for the revenue cycle (extract; the full inventory
runs to 118 controls across nine processes).**

| Control ID | Control | Type | Risk addressed | Assertion | Frequency | Owner |
| --- | --- | --- | --- | --- | --- | --- |
| REV-01 | Salesforce CPQ enforces the discount approval matrix: quotes above defined discount thresholds cannot reach "Closed Won" without the configured approver's electronic approval | Automated / configurable | Transaction price recorded at an unauthorized amount | Revenue accuracy | Each transaction | B. Hallowell |
| REV-02 | The Zuora CPQ connector (I-1) error queue is reviewed daily by the Billing Analyst, who investigates and clears each item | IT-dependent manual | Order form activated in Zuora with wrong terms, or not activated at all | Revenue accuracy, completeness | Daily | Billing Analyst |
| REV-03 | The Zuora Billing-to-Zuora Revenue nightly batch (I-2) produces a record-count and amount reconciliation report; exceptions are worked by the Revenue Manager | IT-dependent manual | Subscriptions omitted from or duplicated in the revenue subledger | Revenue and deferred revenue completeness, accuracy | Daily | J. Pike |
| REV-04 | The Revenue Manager reconciles the RevPro "Revenue Contract Summary" to the general ledger monthly; the Controller reviews and approves the resulting summary journal before posting (I-3) | Management review / IT-dependent manual | Revenue subledger does not agree to the general ledger | Revenue and deferred revenue accuracy, completeness | Monthly | J. Pike / E. Vasquez |
| REV-05 | RevPro configuration rules (27) implement the ASC 606 model: performance obligation identification, SSP allocation, schedule generation, and modification treatment | Automated / configurable | Revenue recognized on the wrong pattern or in the wrong period for a class of contracts | Revenue accuracy, cut-off; deferred revenue accuracy | Continuous | D. Kim |
| REV-06 | Revenue is recognized from the later of contract start date and provisioning date, enforced by a Zuora provisioning-date field populated from the platform | Automated | Revenue recognized before the service commences | Revenue occurrence, cut-off | Each transaction | D. Kim |
| REV-07 | The Director of Technical Accounting reviews and documents the SSP analysis annually, and quarterly for new SKUs | Management review | SSP not supported by evidence, misallocating the transaction price | Revenue accuracy, allocation | Quarterly | A. Bello |
| REV-08 | The Stripe-to-NetSuite daily journal (I-4) is supported by a daily cash-to-revenue reconciliation with PagerDuty failure alerting | IT-dependent manual | Self-serve revenue or cash omitted | Revenue and cash completeness | Daily | Staff Accountant |
| REV-09 | Credit memos above a defined threshold require approval by the Controller; SLA credit eligibility is evaluated monthly against uptime reports | Manual | Contra-revenue not recorded, or recorded without authorization | Revenue accuracy; completeness of contra-revenue | Monthly | E. Vasquez |
| REV-10 | Manual journal entries to revenue accounts 4100–4210 require a second approver above $250,000 in NetSuite | Automated / configurable | Revenue adjusted outside the normal process | Revenue occurrence, accuracy | Each entry | E. Vasquez |

Read the last row against W-12. The control exists and is configured, and it is *designed* so that entries below
$250,000 require no independent approval — which means 3,847 of 4,912 FY2025 manual entries passed through it
without review. REV-10 is therefore a control that operates exactly as designed and does not address the risk
it is mapped to. That is a design deficiency, not an operating failure, and the distinction determines both the
test (inspect the configuration, do not sample entries for approval evidence) and the remediation. Chapter 14
owns the evaluation; the risk assessment consequence is that control risk for R-10 is at maximum from the outset,
which is why the Chapter 16 journal entry testing is scoped as heavily as it is.

Note also what REV-06 tells you about R-1. The control depends on a provisioning-date field populated from the
platform. If that field is blank, or is populated with the contract start date by default, the control silently
fails, and 14 Q1 2025 contracts is exactly what corrected misstatement C-1 ($410) records. When a control's
operation depends on the content of a data field, the completeness and accuracy of that field is part of the
control, and the test must address it.

## 2.11 A SaaS Inherent Risk Catalogue

The catalogue below is the generalized version of what the matrix instantiates. Its purpose is to be read at the
start of any subscription-business engagement, because the same twelve mechanisms recur with different names.

**Exhibit 2-14. Inherent risk mechanisms characteristic of subscription businesses.**

| # | Mechanism | Why it is inherent rather than control-driven | Dominant inherent risk factors | Accounts and assertions | AtlasFlow instance |
| --- | --- | --- | --- | --- | --- |
| 1 | **Period-end cut-off** | Recognition turns on two dates — execution and service commencement — neither of which is a cash event, and both of which are recorded in a sales system by sales people | Change, bias | Revenue occurrence and cut-off; deferred revenue completeness | 41% of Q4 ACV signed December 24–31; corrected misstatement C-1 ($410); uncorrected U-3 ($150) |
| 2 | **Standalone selling price** | ASC 606 requires allocation by relative SSP, and SSP for a new or bundled SKU frequently has no observable population | Subjectivity, change | Revenue accuracy and allocation; deferred revenue accuracy | Insight: 31 standalone sales, 22% interquartile range |
| 3 | **Contract modifications** | A single amendment can be a separate contract, a prospective modification, or a cumulative catch-up, and the difference changes the period of recognition | Complexity | Revenue accuracy and cut-off | Ramp restructurings; the February 2025 RevPro configuration change |
| 4 | **Usage and consumption data** | The measured quantity is produced by the product, not by the accounting system, and is often outside the ITGC boundary | Complexity, uncertainty | Revenue completeness and accuracy | $4,200 of overage; Q4 sequential growth of 27.5% against a 4.8% base increase |
| 5 | **Churn, retention, and credit losses** | The CECL estimate depends on a forward view of a customer base whose composition is changing | Subjectivity, uncertainty | Allowance valuation | GRR 91%, DSO 68 days, allowance $1,900 against an acceptable range |
| 6 | **Capitalized costs to obtain a contract** | The amortization period is an estimate of a period of benefit that extends beyond the contract | Subjectivity, uncertainty, bias | Deferred cost existence and valuation | $24,000 asset, four-year period, 4.3-year average life, $1,900 relating to non-renewed customers |
| 7 | **Capitalized internal-use software** | The capitalization trigger is a project-stage judgment made by the people whose budgets benefit | Subjectivity, bias | Capitalized software existence and accuracy | $10,900 of FY2025 additions; 22% of hours on retroactively restaged epics |
| 8 | **Stock-based compensation** | Performance conditions require probability estimates and market conditions require simulation | Subjectivity, complexity, bias | SBC accuracy, occurrence, cut-off; APIC | $28,700; the ARR-based PSU revision from 100% to 85% and the $1,340 credit |
| 9 | **Deferred revenue completeness** | The liability is understated by the same act that overstates revenue, and it cannot be found by testing the recorded balance | Complexity, bias | Deferred revenue completeness | $78,200 balance; the roll-forward's billings line of $163,750 |
| 10 | **Metric-driven pressure** | Compensation and valuation depend on measures computed outside the general ledger and outside GAAP | Bias | Every account the metric touches; presentation of other information | ARR-based PSUs; bookings-based CRO compensation; the Snowflake datamart |
| 11 | **Multi-element and multi-currency contracting** | Allocation, translation, and material rights compound | Complexity | Revenue accuracy; deferred revenue accuracy | C-2 Voltaire: EUR contract, GBP functional currency, USD reporting, $200 material right |
| 12 | **Gross versus net and principal versus agent** | Channel arrangements require a control assessment that determines whether revenue is recorded at all and at what amount | Subjectivity, complexity | Revenue accuracy, presentation; rights and obligations | $9,700 of reseller revenue; C-4 Tessera/Cirrus |

Two mechanisms in this list are frequently *missed* rather than mis-assessed. Mechanism 9 is missed because
completeness of a liability requires a source-to-record test and most revenue programs are built record-to-source.
Mechanism 10 is missed because the metric is not in the financial statements, so it appears to be somebody else's
problem — until you notice that the CEO's PSU vesting depends on it and the PSU expense is $8,200 of unrecognized
cost inside account 3100.

## 2.12 The FY2025 AtlasFlow Assertion-Level Risk Assessment Matrix

This is the working document the rest of the audit is built from. It is presented in seven parts, one per area,
with identical columns. Conventions:

- **Inherent risk factor codes:** S = subjectivity, C = complexity, U = uncertainty, Ch = change, B =
  susceptibility to management bias or other fraud risk factors.
- **IR and RMM scale:** Low, Moderate, Elevated, High, per the spectrum table in §2.3.
- **CR scale:** Low, Moderate, High, Maximum. "Maximum" means Brightline plans no reliance on controls for that
  assertion. Control risk here is the *planned* assessment as of the October 14, 2025 strategy date; the
  reassessment log in §2.14 records the changes made after control testing.
- **RMM** is the combination of IR and CR, and it is not an arithmetic product. Where CR is Maximum, RMM equals
  IR by construction.
- **Significant risk** is determined from inherent risk alone (§2.8).

**Exhibit 2-15. Risk assessment matrix — Part A: Revenue (accounts 4100, 4110, 4120, 4200, 4210; $148,200).**

| Ref | Risk — what could go wrong, and in which direction | Relevant assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-1 | Subscription revenue is recognized from the contract start date rather than the later provisioning date, overstating revenue and understating deferred revenue | Occurrence, cut-off | Ch, B, C | **High.** REV-06 depends on a data field populated from the platform; the same error occurred in FY2025 Q1 on 14 contracts and was corrected as C-1 ($410); the Insight launch and the February RevPro change altered provisioning workflows mid-year | High | High | **Yes** | Test the completeness and accuracy of the Zuora provisioning-date field for the full FY2025 activation population (4,118 subscriptions); recompute revenue commencement for 100% of the 214 subscriptions with start dates in the final ten days of a quarter; agree provisioning dates to platform tenant-creation logs |
| R-2 | Contracts are recorded as FY2025 transactions although execution occurred in FY2026, overstating revenue, receivables, bookings, and capitalized commissions | Occurrence, cut-off | B, Ch | **High.** Bias is acute and specific: commissions are paid on signature date, the CRO is compensated on bookings, 41% of Q4 ACV ($25,174) was signed December 24–31 against 27% in the prior year, the CPQ signature-date field is editable by the VP Sales Operations with no review, and a January 2026 whistleblower email alleges December deals were papered after the fact. Fraud risk presumption under AS 2401 | Maximum | High | **Yes** | See the extended case study. In summary: 100% examination of the 164 order forms signed December 19–31, 2025 ($29,294 of ACV) with third-party date corroboration; CPQ field-history analysis for the full 235-order-form December population; external confirmation of contract terms and dates for the 20 largest; inspection of DocuSign completion certificates |
| R-3 | The standalone selling price used for the Insight module is not supported, misallocating the transaction price between Core, Insight, and professional services and shifting revenue between periods | Accuracy, allocation | S, Ch, B | **High.** Subjectivity acute: only 31 standalone Insight sales in FY2025 across a band with a 22% interquartile range, in the SKU's first year, and the SSP conclusion allocates revenue on nearly every FY2025 multi-element contract | High | High | **Yes** | Build an independent SSP range from the 31 observable sales stratified by segment and deal size; compute the allocated-revenue sensitivity across the range; test the "expected cost plus a margin" and adjusted-market-assessment workpapers; national office concurrence (Chandrasekhar). Chapter 5 |
| R-4 | Contract modifications are processed under the wrong ASC 606 model in RevPro — treated as separate contracts or prospective when a cumulative catch-up is required — misstating revenue and deferred revenue in the period of modification | Accuracy, cut-off | C, Ch | **Elevated.** Complexity is high (three possible treatments) and the February 2025 configuration change addressing ramped contracts was deployed with abbreviated user acceptance testing because of a Q1 close deadline | High | High | No | Obtain the full FY2025 amendment population from Zuora (612 amendments); stratify by type; recompute revenue for 25 amendments covering all three treatments; inspect the 27 RevPro configuration rules with Ben Osei and re-perform the two rules governing ramps and mid-term upsells |
| R-5 | Usage overage revenue is incomplete or overstated because the workflow-run counts originate on the AtlasFlow platform, outside the financial systems and outside the ITGC boundary | Completeness, occurrence, accuracy, cut-off | C, U | **Elevated.** Q4 overage grew 27.5% sequentially against a 4.8% increase in the subscription base; the measured quantity is a product telemetry output, and overage is billed in arrears so recognition precedes billing | High | High | No | Reconcile platform run counts to Zuora usage records for October, November, and December; recompute overage for the 20 largest overage accounts including C-1 Meridian's 244,000 runs; develop an independent expectation for Q4 overage from committed-volume utilization data and investigate differences above $72 |
| R-6 | Reseller arrangements are recorded gross or net incorrectly, or revenue is recorded when AtlasFlow is an agent, misstating revenue and cost of revenue | Accuracy, presentation, rights and obligations | S, C | **Elevated.** Subjectivity in the control assessment; 42 arrangements totaling $9,700 of FY2025 revenue; two arrangements where the reseller performs implementation on its own account | Moderate | Moderate | No | Read C-4 Tessera and 5 further reseller contracts selected to cover each contractual variant; evaluate the three ASC 606 control indicators for each; confirm no professional services revenue is recorded on the two integrator-delivered engagements; national office concurrence. Chapter 4 |
| R-7 | Service-level-agreement credits and other contra-revenue earned in FY2025 are not accrued, overstating revenue | Completeness of contra-revenue, accuracy | U, B | **Elevated.** Northgate claimed $180 in December 2025 and AtlasFlow recorded nothing pending "commercial discussions"; two FY2025 incidents triggered credit eligibility; corrected misstatement C-2 ultimately recorded $290 across Northgate and six others | High | High | No | Obtain the FY2025 uptime reports for both hosting regions for all 12 months; identify every contract containing an SLA credit schedule (487 contracts); recompute credit eligibility independently of customer claims; agree the recorded contra-revenue in account 4900 |
| R-8 | The input-method percentage-of-completion estimate for fixed-fee professional services is wrong, misstating revenue and the contract asset | Accuracy, cut-off | S, U | **Elevated.** Estimated total hours is a management estimate; professional services gross margin moved from 2.0% to 5.0%; uncorrected misstatement U-4 ($95) arose here | Moderate | Moderate | No | Recompute percentage of completion for 12 of the 41 open fixed-fee engagements at December 31; perform a retrospective comparison of estimated to actual total hours on the 18 engagements completed during FY2025; investigate any pattern of systematic underestimation |
| R-9 | Self-serve revenue processed through Stripe is incomplete or inaccurate because it enters the general ledger through in-house Lambda code as a daily summary journal | Completeness, accuracy | C, Ch | **Elevated.** $6,100 of revenue across 11,400 accounts on a wholly separate system path; interface I-4 is in-house code with two undocumented FY2025 modifications (W-7) | High | High | No | Reconcile Stripe settlement reports to account 4100 and 1205 for all 12 months; re-perform the daily journal computation for 10 days selected around the two modification dates; test the two code modifications for authorization and for effect on the calculation |
| R-10 | Manual journal entries are used to adjust revenue or deferred revenue outside the normal process, overstating revenue | Occurrence, accuracy, cut-off | B | **High.** Management override is presumed a significant risk. 4,912 manual entries were posted in FY2025, 3,847 of them below the $250,000 threshold at which NetSuite requires a second approver, 34 of them hitting revenue with a non-standard offset account for $3,900, and 214 posted by users with segregation-of-duties conflicts | Maximum | High | **Yes** | Examine 100% of the 34 entries hitting revenue with a non-standard offset; apply eight scoring criteria to the full 4,912-entry population; examine the 27 consolidation top-side entries ($6,200) that are outside the NetSuite population entirely. Chapter 16 |
| R-11 | Multi-currency subscription revenue is translated at the wrong rate or on the wrong basis, misstating revenue and deferred revenue | Accuracy | C, Ch | **Elevated.** C-2 Voltaire is contracted in EUR through an entity with a GBP functional currency and reported in USD; the consolidation workbook has four hard-keyed overrides in the FX translation tab | High | High | No | Instruct Brightline UK LLP to test the EUR-to-GBP translation for the 10 largest EUR-denominated contracts (WP 1260-02, §4); recompute the GBP-to-USD translation of UK revenue; test the four hard-keyed FX cells to source |
| R-12 | Contract term is determined without regard to enforceable rights and obligations, overstating revenue, deferred revenue, and the RPO disclosure | Accuracy, cut-off, presentation and disclosure | S, U | **Elevated.** C-5 Pemberton has a 30-day termination-for-convenience clause with no penalty; the FY2025 population of such contracts is 96 arrangements; the judgment drives the transaction price, the RPO disclosure, and the amortization period for the related commissions | High | High | No | Identify the termination-for-convenience population from contract metadata and confirm completeness against a manual read of 20 contracts; evaluate the enforceable-rights conclusion; quantify the effect on revenue, deferred revenue, and RPO. Chapters 5 and 6 |

Rationale notes on the four Part A rows most likely to be challenged in review:

**R-1 versus R-2.** These are distinct risks with distinct responses and they are frequently merged into one row
called "revenue cut-off," which is a mistake. R-1 concerns a *date recorded in a system* being the wrong one of
two legitimate dates, and it is addressed by testing the provisioning-date field and comparing it to platform
logs. R-2 concerns a date being *fabricated*, and it is addressed by third-party corroboration and field-history
analysis. A test designed for R-1 will not detect R-2, because a backdated order form has an internally
consistent start date.

**R-5's inherent risk of Elevated rather than High.** The argument for High is that the underlying data is
entirely outside the ITGC boundary and the Q4 movement is unexplained at the risk assessment date. The argument
for Elevated, which Brightline adopted, is magnitude: the entire overage stream is $4,200, so even a 20%
misstatement of $840 is below performance materiality of $940, and the Q4 increment over a proportionate
expectation is roughly $250. Elevated is the defensible position given that magnitude constraint. What would move
it to High: evidence that the overage rate applied is a management input rather than a contractual rate, or a
finding that committed volumes in Zuora do not agree to the order forms, either of which would extend the
exposure beyond the overage stream into the Core subscription base.

**R-10's control risk of Maximum.** This is not a consequence of testing; it is a consequence of design. REV-10
requires a second approver only above $250,000, so 78.3% of manual entries pass through the control by design
rather than by failure. There is nothing to rely on, and control risk is at maximum from the strategy date.

**R-6's control risk of Moderate.** The only row in Part A where Brightline planned reliance. The reseller
population is small (42 arrangements), the conclusions are documented in a technical accounting memorandum
reviewed by the Director of Technical Accounting, and the arrangements did not change during FY2025. Reliance was
retained after testing.

**Exhibit 2-16. Risk assessment matrix — Part B: Deferred revenue and the RPO disclosure (accounts 2400, 2405,
2410; $78,200; RPO disclosed $214,000).**

| Ref | Risk — what could go wrong, and in which direction | Relevant assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-13 | Deferred revenue is understated because amounts billed were recognized as revenue before the performance obligation was satisfied, or because a performance obligation (a material right, an unactivated subscription, a professional services element) was never recorded | Completeness | C, B | **High.** This is the liability-side mirror of R-1, R-3, R-4, and R-12, and it cannot be detected by testing the recorded balance. The population that must be tested is the complete set of executed contracts, not the recorded liability. Bias is the same bias that drives revenue overstatement | High | High | **Yes** | Test source-to-record: obtain the complete Zuora Billing subscription population at December 31, 2025 (5,240 active subscriptions), prove its completeness against the CPQ "Closed Won" opportunity population, and recompute the deferred revenue balance for 40 subscriptions stratified by value and by contract type. Independently extract billings from Zuora and reconcile to the $163,750 roll-forward line to establish it is not a plug. Chapter 6 |
| R-14 | The current/noncurrent split of deferred revenue is wrong, misclassifying between $71,300 current and $6,900 noncurrent | Classification | C | **Elevated.** The split is a mechanical function of the revenue schedules, but 34% of ACV sits in multi-year contracts with ramps and escalators, and the ramped schedules are the ones the February 2025 configuration change touched | High | Moderate | No | Recompute the twelve-month portion of the December 31, 2025 revenue schedule population in full and agree to $71,300 and $6,900. The recomputation is a full-population procedure, so no sampling is required, and any difference above $72 is investigated |
| R-15 | Deferred revenue acquired in the Kestrel acquisition is measured on Kestrel's legacy basis rather than on the ASC 805 basis, misstating the $610 acquired liability and the post-acquisition revenue | Accuracy, completeness | C, U, Ch | **Elevated.** Kestrel maintained a homegrown billing spreadsheet and had no formal revenue recognition policy; its records were on a modified cash basis. The measurement basis for an acquired contract liability is a technical judgment a first-time acquirer is unlikely to have applied correctly | High | High | No | Obtain the Kestrel customer contract population at August 4, 2025 (74 contracts, approximately $2,100 of ARR); recompute the remaining performance obligation at the acquisition date; compare to the $610 recorded and evaluate the measurement basis; test the October 2025 migration into Zuora for completeness |
| R-16 | The RPO disclosure of $214,000, and the statement that $138,900 (64.9%) is expected within twelve months, are incomplete or inaccurate | Presentation and disclosure, completeness, accuracy | C, S | **Elevated.** RPO is a required ASC 606 disclosure computed from the same contract population and the same contract-term judgments as R-12, and the practical expedients and exclusions applied are elective | High | High | No | Recompute RPO in full from the Zuora Revenue contract extract; reconcile the recomputation to the disclosed $214,000 and the 64.9% split; test the practical expedients claimed and the completeness of the exclusions; quantify the effect of the termination-for-convenience population identified in R-12. Chapter 6 |

**Exhibit 2-17. Risk assessment matrix — Part C: Accounts receivable, contract assets, and credit losses
(accounts 1200, 1205, 1210, 1220; gross $38,600, allowance $1,900, contract assets $3,400).**

| Ref | Risk — what could go wrong, and in which direction | Relevant assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-17 | Receivables are recorded that do not exist, or are recorded in the wrong period because the underlying billing was accelerated, overstating receivables and revenue | Existence, accuracy, cut-off | B, Ch | **Elevated.** Gross receivables grew 26.6% against revenue growth of 24.6%, and Q4 DSO rose from 61 to 68 days, implying roughly $4,000 of receivables that would not have existed at prior-year collection velocity. Bias is present through the same Q4 incentives as R-2 | High | High | No | Positive confirmation of the ten largest enterprise balances ($13,230, 35.9% of enterprise receivables) plus a monetary-unit sample of the remainder; subsequent cash receipts testing through February 13, 2026; cut-off testing of the final ten business days of December billings. Uncorrected misstatement U-1 ($185) is the projected result. Chapter 7 |
| R-18 | The allowance for credit losses of $1,900 is understated, overstating net receivables and understating the provision | Valuation | S, U, B | **High.** Subjectivity and uncertainty are both acute: CECL requires a reasonable-and-supportable forecast overlay on historical loss rates applied to six aging buckets; gross retention fell from 93% to 91%; Sundown Media Holdings is 94 days past due at $980; Meridian's $1,240 professional services invoice is disputed; and management's estimate sits at the optimistic end of the range, producing uncorrected misstatement U-2 ($240) | High | High | **Yes** | Build an independent expectation using both the roll-rate and vintage methods, producing a range of $1,780 to $2,410; recompute the historical loss rates applied to each of the six aging buckets; challenge the forecast overlay against the cohort deterioration in Exhibit 1-10; evaluate management's $1,900 against the range and document where in the range it falls. Chapter 7 |
| R-19 | The self-serve receivable of $1,700 across 11,400 accounts is overstated or misaged | Existence, valuation | C | **Moderate.** Magnitude is 1.2 times materiality; the population is large but homogeneous and card-collected, so exposure is bounded and the loss experience is stable | High | Moderate | No | Recompute the aging of the full 11,400-account population from the Stripe transaction file; analyze subsequent card settlement for 100% of the balance through January 31, 2026; no sampling required because the procedure is full-population |
| R-20 | Contract assets of $3,400 do not exist, or are presented gross rather than netted against contract liabilities at the contract level | Existence, accuracy, classification | C | **Elevated.** Netting under ASC 606 is applied at the contract level, not at the entity level, and AtlasFlow's professional services and subscription elements frequently sit in the same contract with opposite balances | High | Moderate | No | Test the contract-level netting for the 25 contracts with the largest gross contract asset balances; agree each to the revenue schedule and the invoice history; recompute the net presentation |
| R-21 | Credit memos are issued without authorization or to conceal collectability problems, understating the provision and overstating revenue | Occurrence, accuracy; completeness of contra-revenue | B | **Elevated.** A credit memo can substitute for a write-off, which moves an item from the provision to contra-revenue and removes it from the aging; the population is large and the approval threshold is a management input | High | High | No | Obtain the full FY2025 credit memo population from Zuora (1,148 memos); score by amount, timing, issuing user, and reason code; examine 100% of memos above $72 issued in Q4 2025 and in January 2026, and all memos issued to customers in the 91-day-and-over aging buckets |

**Exhibit 2-18. Risk assessment matrix — Part D: Capitalized costs to obtain a contract (accounts 1300, 1305;
$24,000; amortization within 6210, $8,600).**

| Ref | Risk — what could go wrong, and in which direction | Relevant assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-22 | Costs that are not incremental to obtaining a contract — base salary, sales-engineer time, non-commission bonuses — are capitalized, overstating the asset and understating expense | Existence, accuracy | C, B | **Elevated.** ASC 340-40 permits capitalization only of incremental costs; AtlasFlow's policy correctly excludes base salary and sales-engineer time, so the risk is application rather than policy. Bias is present because capitalization improves both operating margin and operating cash flow | High | High | No | Test the composition of the $13,720 of FY2025 additions against the build in Exhibit 1-8; agree 30 individual commission payments to the commission plan, the payroll register, and the underlying order form; test that the practical-expedient exclusion of $1,943 covers only contracts with an amortization period of one year or less |
| R-23 | The four-year amortization period exceeds the period of benefit, overstating the asset and understating amortization | Valuation, accuracy | S, U, B | **Elevated.** The period is supported by a 4.3-year average customer life and a technology-refresh assessment. Gross retention fell to 91% and the newest cohorts expand more slowly (Exhibit 1-10). The implied remaining amortization period of the asset itself fell from 3.05 to 2.79 years | High | High | No | Recompute average customer life from the FY2025 churn population (192 customers) and from the cohort table; test the renewal-commensurability analysis (renewal commissions 3.1% of ACV versus 11.8% on new business) that supports using four years rather than the contract term; compute the sensitivity — on the $24,000 closing asset the annual charge is $6,000 at a four-year period and $8,000 at three years, so each one-year reduction in the period adds approximately $2,000 of annual amortization, and a retrospective change would require an immediate write-down |
| R-24 | Capitalized costs relating to customers who did not renew are not written off, overstating the asset | Valuation | U, B | **Elevated.** Management identified a $1,900 balance relating to customers not renewed as of year end. Following audit challenge, $620 was written off as corrected misstatement C-3, leaving $1,280 supported by asserted renewal negotiations — an assertion, not evidence | High | High | No | Obtain the FY2025 non-renewal population and match it to the deferred cost sub-ledger; test the $620 write-off for completeness and the remaining $1,280 for corroborating evidence of active renewal discussions (dated correspondence, opportunity records in Salesforce with a close date and stage); evaluate the residual as a potential misstatement |
| R-25 | Commissions on Q4 bookings are accrued and capitalized in FY2025 although the underlying contracts were not executed in FY2025, overstating the asset and the accrual | Cut-off, existence | B, Ch | **Elevated.** Commissions are paid on signature date, so the entire $25,174 of December 24–31 ACV generated FY2025 commission cost of approximately $2,971 before payroll taxes — 61.9% of the $4,800 accrued commission balance — with no FY2025 revenue on the $20,264 of it that starts in 2026 | Maximum | Elevated | No | Tie the December portion of the $4,800 accrued commission balance to the December 19–31 order form population tested for R-2; any contract whose execution date is not corroborated results in a corresponding reversal of accrued and capitalized commission, which is quantified alongside the revenue effect |

**Exhibit 2-19. Risk assessment matrix — Part E: Capitalized internal-use software (accounts 1560, 1565; gross
$31,200, net $18,600; FY2025 additions $10,900).**

| Ref | Risk — what could go wrong, and in which direction | Relevant assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-26 | Development costs are capitalized although the project was in the preliminary project stage or past substantial completion, overstating the asset and understating research and development expense | Existence, accuracy | S, B | **High.** Subjectivity and bias are both acute and they compound: 22% of the FY2025 capitalized hours were coded to Jira epics whose stage designation was changed retroactively during the year, and the developer time reports are approved by the same engineering managers who own the projects' budgets. Capitalized additions of $10,900 are 24.8% of R&D expense against 20.7% in FY2024, and capitalization improves both gross margin and operating cash flow | High | High | **Yes** | Identify and test 100% of the epics whose stage designation was changed after the first time entry was posted ($2,398 of the $10,900); for each, obtain the original stage designation, the change record, the changer's identity, and the business justification; perform an independent stage assessment for 15 projects representing $6,400 of additions by interviewing the developers who did the work rather than the managers who approved the time; recompute the capitalized amount. Chapter 10 |
| R-27 | Capitalized software is amortized over too long a period, or costs relating to abandoned or superseded functionality are not impaired | Valuation, accuracy | S, U | **Elevated.** The October 2025 restructuring eliminated 41 positions and the Kestrel platform consolidation supersedes some AtlasFlow functionality, both of which are impairment indicators. FY2025 amortization of $5,700 against a gross balance of $31,200 implies an average remaining life the useful-life policy must support | High | Moderate | No | Recompute FY2025 amortization from the asset register and agree to accumulated amortization of $12,600; obtain the list of projects affected by the restructuring and by the Kestrel consolidation; test whether any capitalized project was abandoned during FY2025 and remains on the register |
| R-28 | The Jira time-tracking extract used to support capitalization is incomplete or inaccurate as information produced by the entity | Accuracy | C | **Elevated.** The extract is the sole support for the $10,900; it is produced by a query against a ticketing system whose parameters management sets, and Jira ticket quality is described as uneven | High | High | No | Obtain the query, the parameters, and the extract date; reconcile total extracted developer hours to the payroll register headcount and available hours for the engineering population; test that the extract includes all engineering cost centers and excludes contractors whose costs are not capitalizable; re-run the query with Brightline-specified parameters and compare |

**Exhibit 2-20. Risk assessment matrix — Part F: Stock-based compensation and equity (account 3100; FY2025
expense $28,700).**

| Ref | Risk — what could go wrong, and in which direction | Relevant assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-29 | The probability assessment for the ARR-based performance RSUs is biased, and the Q4 revision from 100% to 85% probable was recognized in the wrong period, misstating expense between quarters and years | Accuracy, occurrence, cut-off | S, B | **High.** Bias is acute and documented: the CEO's compensation is weighted to these awards, the compensation committee recorded in July 2025 that achievement was "tracking behind plan," management nonetheless assessed the tranche as 100% probable in Q3 2025, and the Q4 revision to 85% produced a $1,340 catch-up credit. Corrected misstatement C-5 ($240) records that part of the revision belonged in an earlier period | High | High | **Yes** | Obtain every interim probability assessment prepared during FY2025 and the supporting ARR forecasts; compare each to the compensation committee and board materials of the same date; recompute the $1,340 catch-up and the expense that would have been recorded had the revision been made in Q3; evaluate the pattern for indications of estimate bias and refer the conclusion to the Chapter 19 evaluation of qualitative aspects of accounting practices. Chapter 9 |
| R-30 | The grant-date fair value of the market-condition (TSR) performance RSUs is misstated because the Monte Carlo inputs are unsupported | Valuation, accuracy | S, C | **Elevated.** 210 thousand units with $4,100 of unrecognized cost; the valuation requires a peer group, correlations, and volatilities that are not directly observable. Magnitude is bounded by the unrecognized cost | Moderate | Moderate | No | Dr. Petrov recomputes the grant-date fair value for both grant tranches independently; test the peer group against the compensation committee's approved group; test the correlation and volatility inputs to source data; compare Petrov's range to management's $39.60 weighted-average grant-date fair value |
| R-31 | The equity award population extracted from Carta is incomplete, understating expense and the share count | Completeness | C | **Elevated.** Interface I-6 is a manual monthly CSV download feeding a spreadsheet roll-forward; a grant omitted from the extract is omitted from expense with no compensating control | High | High | No | Reconcile the Carta grant population to 100% of FY2025 board and compensation committee grant approvals; recompute the share roll-forward from 49,610 to 51,842 (option exercises 610, RSU vesting net of shares withheld 1,489, ESPP 133) and agree to the transfer agent statement; test the completeness of the forfeiture population against the termination list, including the 41 restructuring terminations |
| R-32 | Stock-based compensation is misclassified between cost of revenue, R&D, sales and marketing, and G&A, or is capitalized into internal-use software without support, overstating gross margin | Classification | C, B | **Elevated.** The disclosed allocation is cost of revenue $2,100, R&D $11,400, sales and marketing $7,600, and G&A $7,600, which sums to $28,700. Subscription gross margin improved 1.4 points in FY2025, and moving $500 of stock-based compensation out of cost of revenue would account for 0.4 of that improvement | High | High | No | Recompute the four-way allocation from the grant-level employee department mapping in Carta; test 25 grantees' department coding to the human resources master; determine the amount of stock-based compensation capitalized into account 1560 and test its support against the R-26 hours population; reconcile the total to $28,700 |
| R-33 | The employee stock purchase plan expense is misstated because the six-month look-back and 15% discount are modeled incorrectly for the two FY2025 purchase dates | Accuracy | C | **Moderate.** Unrecognized cost is $900 and the plan mechanics, while intricate, are formulaic once the offering terms are established | Moderate | Moderate | No | Recompute the ESPP expense for the offering periods ending June 30 and December 31, 2025; agree the 133 thousand shares issued and the purchase prices to the Carta records and the bank receipts; confirm no plan modification occurred during FY2025 |

**Exhibit 2-21. Risk assessment matrix — Part G: The Kestrel Labs acquisition (accounts 1700, 1710, 1715, 2600;
total consideration $19,400; goodwill $14,500).**

| Ref | Risk — what could go wrong, and in which direction | Relevant assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-34 | The $2,500 fair value of the contingent consideration is misstated, understating the liability and overstating goodwill, or failing to reflect the probability of the $4,000 maximum payout | Valuation | S, U, C | **High.** All three of subjectivity, uncertainty, and complexity are present acutely: a Monte Carlo simulation of a retention-and-revenue milestone payable in Q1 2027, with an assumed revenue volatility of 32% and a risk-adjusted discount rate of 11.5%, prepared by a first-time acquirer. A reasonably possible misstatement is a large fraction of the $2,500 carrying amount and exceeds materiality | High | High | **Yes** | Dr. Petrov develops an independent fair value range and a sensitivity analysis on volatility (±10 points) and discount rate (±300 basis points); the engagement team tests the milestone definition against the purchase agreement, tests the revenue forecast used in the simulation against the Kestrel ARR of approximately $2,100 and the $340 of actual post-acquisition revenue, and evaluates whether the simulation is calibrated to the $4,000 cap. Chapter 9 for the valuation technique |
| R-35 | Acquired intangible assets are misidentified or misvalued — developed technology at $6,900 over five years and customer relationships at $1,100 over seven years — shifting amounts between intangibles and goodwill and misstating amortization | Valuation, existence, accuracy | S, C | **Elevated.** The valuation was prepared by a company-engaged specialist using a forecast management provided; the useful lives determine $1,380 of annual developed technology amortization and $157 of customer relationship amortization once fully in effect | High | High | No | Evaluate the company-engaged specialist's competence, capabilities, and objectivity; test the forecast underlying the income approach against the acquired customer contract population and against actual post-acquisition performance; test the useful-life conclusions; recompute the FY2025 partial-year amortization from August 4 and agree to the $3,200 accumulated intangible amortization balance |
| R-36 | Goodwill of $14,500 is misstated because it is a residual, or measurement-period adjustments were recorded incorrectly | Accuracy, valuation | C, U | **Elevated.** Goodwill is the plug, so every error in another component lands here — and management's preliminary allocation schedule does not currently foot. The identifiable components as presented (developed technology $6,900, customer relationships $1,100, net working capital acquired $200, less a deferred tax liability of $1,300) net to $6,900, which against recorded goodwill of $14,500 implies total consideration of $21,400 rather than the $19,400 in the purchase agreement — a $2,000 difference, 1.4 times overall materiality. Goodwill of $14,500 is independently corroborated by the movement in account 1700 ($26,900 less the opening $12,400), so the $2,000 sits in an identifiable component or in the measurement of consideration | High | Moderate | No | Obtain management's supporting allocation schedule and resolve the $2,000 difference between total consideration of $19,400 ($16,900 cash at closing plus $2,500 of contingent consideration recorded in account 2600) and the sum of the identifiable components and goodwill; recompute the residual once resolved; agree goodwill to the movement in account 1700; obtain and test the measurement-period adjustment log; confirm no adjustments were recorded outside the measurement period. Chapter 9 |
| R-37 | The acquired opening balance sheet is incomplete or inaccurate because Kestrel's historical records were unaudited and on a modified cash basis | Completeness, existence, accuracy | C, Ch, U | **Elevated.** Kestrel had 22 employees, no formal revenue recognition policy, and a homegrown billing spreadsheet. The recorded net working capital acquired is only $200, which is small enough that an omitted liability of $300 would be a misstatement of the purchase price allocation and of goodwill | Maximum | Elevated | No | Convert Kestrel's modified-cash records to an accrual basis for the 22 largest customers and the full accounts payable and accrued liability population at August 4, 2025; perform a search for unrecorded liabilities at the acquisition date using post-acquisition disbursements through December 31; test the $200 and the $610 of acquired deferred revenue |
| R-38 | The $340 of post-acquisition Kestrel revenue is recognized without an established policy, and the October 2025 migration of Kestrel contracts into Zuora was incomplete | Occurrence, accuracy, cut-off, completeness | Ch, C | **Elevated.** For the period August 4 to October 2025, Kestrel revenue was recognized outside the RevPro engine on the basis of a spreadsheet; the migration is a change event with no ITGC coverage | Maximum | Elevated | No | Recompute the $340 from the acquired contract population for the period August 4 to December 31, 2025; test the October migration for completeness by reconciling the 74 acquired contracts to the Zuora subscription records post-migration; examine the journal entries recording pre-migration Kestrel revenue |

### 2.12.1 What the matrix tells you in aggregate

Read the columns rather than the rows and three engagement-level conclusions emerge.

**Control risk is High or Maximum for 34 of the 38 risks.** Brightline planned reliance on controls for only four
of them — R-6 (reseller conclusions), R-8 (professional services estimate), R-30 (TSR PSU valuation), and R-33
(ESPP) — and each of those four sits in a small, stable population reviewed by a competent preparer. That is the
practical meaning of 14 identified ITGC gaps in a
first-year integrated audit: the substantive audit carries almost the entire evidential burden, which is why
Chapter 1's hours budget shows 880 hours on revenue and deferred revenue against 620 in FY2024 even though
control testing added 1,370 hours of its own.

**The nine significant risks cluster in two places: revenue cut-off and management estimates.** Four of the nine
(R-1, R-2, R-10, R-13) are cut-off and override risks; four (R-3, R-18, R-26, R-29) are estimates in which
management has both discretion and an incentive; one (R-34) is an estimate in which management has discretion but
a first-time acquirer's inexperience rather than an incentive. That distribution is characteristic of a
subscription business and it should be recognizable at the start of the next such engagement.

**Bias (factor B) appears in 17 of the 38 rows.** That is a high proportion, and it is the fingerprint of an
entity whose compensation and equity story depend on measures computed outside the general ledger. It is also the
formal link to Chapter 17: every row carrying factor B is an input to the fraud risk assessment, and the
AS 2401 discussion at the October 7 meeting used the B column as its agenda.

## 2.13 Linking Assessed Risk to the Nature, Timing, and Extent of Further Procedures

An assessment that does not change a procedure has changed nothing. The linkage is three-dimensional, and each
dimension responds to a different feature of the assessment.

**Exhibit 2-22. How each dimension responds, with AtlasFlow illustrations.**

| Dimension | Responds primarily to | Low-risk form | High-risk form | AtlasFlow illustration |
| --- | --- | --- | --- | --- |
| **Nature** | The assertion and the reason for the risk | Inspection of internal documents; substantive analytical procedures | External confirmation; examination of third-party evidence; re-performance; procedures the entity cannot influence | R-2 moves the nature from inspecting order forms held by the client to inspecting DocuSign completion certificates and CPQ field history, and to confirming contract dates directly with 20 customers |
| **Timing** | Bias, cut-off risk, and the availability of a reliable interim position | Interim testing with roll-forward inquiry | Testing at or after the period end; unpredictable timing; procedures directed at the period-end boundary | R-1 and R-2 are tested entirely at year end and extended into January 2026; R-6 (reseller conclusions) was tested at interim because the arrangements do not change |
| **Extent** | Magnitude and the tolerable misstatement | Sample of 10 to 25; substantive analytics with a wide threshold | Full-population testing; 100% examination of a defined stratum; sample sizes computed from performance materiality at a low risk of incorrect acceptance | R-10: 100% of the 34 revenue entries with non-standard offsets plus scoring of all 4,912 manual entries. R-14: full-population recomputation, because the population is machine-readable and the recomputation costs less than a sample |

Three points about the linkage that are easy to state and hard to do.

**Nature dominates for occurrence and existence risks; extent dominates for completeness risks.** If you suspect
recorded revenue did not occur, adding items to a sample of internally generated order forms does not help,
because every item in the population has an internally consistent order form. You need different evidence, from
outside the entity. If you suspect a liability is incomplete, no single item of better evidence helps; you need a
population from outside the accounting records and enough coverage of it.

**Full-population testing has replaced sampling wherever the data is machine-readable, and it changes the
extent conversation entirely.** R-14, R-16, R-19, and the R-10 scoring are all full-population procedures.
The binding constraint is no longer sample size; it is the completeness and accuracy of the extract. That is why
R-28 exists as a separate risk and why Chapter 12 treats information produced by the entity as the most commonly
deficient area in practice.

**A response must be traceable to the row that generated it.** Brightline's audit programs carry the risk
reference in the program step header — "5100-14 (R-2)" — so that a reviewer can confirm that every risk has a
response and every procedure has a reason. Programs without that linkage cannot be reviewed for sufficiency, and
they accumulate procedures that respond to risks that were removed years earlier.

## 2.14 Reassessment During the Audit, and Documentation

Risk assessment is continuous. AS 2110 and AU-C 315 both require the auditor to revise the assessment when
information obtained during the audit is inconsistent with the evidence on which the original assessment was
based. In practice the assessment is revised when a test produces an unexpected result, and the discipline that
matters is asking whether the unexpected result invalidates an *assessment* rather than merely producing a
misstatement to accumulate.

**Exhibit 2-23. FY2025 risk reassessment log (WP 2300-01).**

| Date | Trigger | Original assessment | Revised assessment | Consequence |
| --- | --- | --- | --- | --- |
| Nov 21, 2025 | Interim controls testing found that user access reviews for Salesforce, Zuora, and NetSuite were performed annually rather than quarterly, with the Q2 review 41 days late (W-3) | CR High for R-1, R-4, R-9; reliance planned on two IT-dependent controls | CR Maximum for R-1, R-4, R-9; no reliance | Substantive extent increased: the R-1 provisioning-date test moved from a sample of 60 to the full 4,118-subscription activation population; 40 hours added |
| Nov 24, 2025 | Testing of 25 order forms for REV-01 identified no deviations, and the CPQ approval configuration was confirmed unchanged since January 1, 2025 | CR High for revenue accuracy arising from unauthorized discounts | CR Moderate for that specific assertion | Extent of transaction-price testing reduced from 40 to 25 contracts; the reduction is documented with the control conclusion it depends on |
| Dec 15, 2025 | Inspection of the consolidation workbook identified four hard-keyed cells overriding formulas in the FX translation tab | R-11 CR High; no separate risk for the consolidation | R-11 CR Maximum; new risk added covering the completeness of the journal entry population for the 27 top-side entries | Chapter 16 scope expanded to include the top-side population; the four cells traced to source |
| Dec 19, 2025 | Q4 bookings data showed 41% of Q4 ACV signed December 24–31 against 27% in the prior year | R-2 IR Elevated, not designated a significant risk | R-2 IR High, designated a significant risk; fraud risk under AS 2401 | The extended case study in this chapter. Response designed December 22; 120 hours added |
| Jan 14, 2026 | The audit committee forwarded a whistleblower email alleging that "December deals were papered after the fact" | R-2 significant risk with a designed response | R-2 response expanded; R-25 CR moved to Maximum; the engagement team discussion was reconvened | WP 1100-02 revised to version 4; revenue programs revised as WP 1200-04 rev. 2; procedures extended to the full December population and to January 2026 signature activity. Chapter 17 |
| Jan 22, 2026 | Testing of R-26 confirmed the restaged-epic population at $2,398, consistent with management's assertion, but found that 3 of the 15 independently assessed projects had no contemporaneous evidence supporting the end of the preliminary project stage | R-26 significant risk; expected misstatement nil | R-26 significant risk; a probable misstatement identified | Referred to the Chapter 10 test extension and the Chapter 19 misstatement evaluation |
| Feb 6, 2026 | Petrov's independent range for the Kestrel contingent consideration was $2,300 to $3,100, containing management's $2,500 | R-34 significant risk | R-34 significant risk; no misstatement | Conclusion documented with the range and the position of management's estimate within it (28th percentile) |

Two features of this log deserve imitation. First, the revisions run in both directions. The November 24 entry
*reduces* an assessment and *reduces* testing, and it is documented as carefully as the increases, because a
reviewer needs to see what the reduction depends on — if the CPQ configuration conclusion later fails, the
transaction-price sample must be reconsidered. A log that only ever increases risk is a log that is not being
used for planning. Second, every row names the consequence. "Risk reassessed as high" with no consequence column
is a record of a thought, not of an audit decision.

Documentation requirements for the risk assessment, drawn from AS 1215 and AU-C 230, are specific: the
discussion among the engagement team, including the significant decisions reached; the key elements of the
understanding of the entity and its environment and of each of the five components of the system of internal
control, and the sources of that understanding; the identified and assessed risks of material misstatement at the
financial statement and assertion levels; the significant risks identified and the basis for the determination;
and the linkage between assessed risks and the procedures performed. The matrix in §2.12 discharges the third,
fourth, and fifth of those. Exhibits 2-4 through 2-13 discharge the second. The walkthrough that follows
discharges the first.

## Step-by-Step Walkthrough: Conducting and Documenting the Engagement Team Discussion and Converting It to Assertion-Level RMM

The output required is not a memo. It is a set of matrix rows and a set of procedures that would not otherwise
have been performed. What follows is how Grace Lindqvist ran the October 7, 2025 meeting and what came out of it.

**Step 1. Fix the date against the audit calendar and protect it.** The meeting must fall after the walkthroughs
(completed September 19) and after the audit committee inquiry (September 30), so that participants arrive with
evidence, and before interim controls testing begins (October 20), so the output can change the programs. Book
3.5 hours, one room, no competing commitments. *If the date slips past the start of interim testing, hold the
meeting anyway and treat the resulting changes as program revisions; a discussion held in December has produced
a memo rather than a plan.*

**Step 2. Set the attendee list and record why each person is required.** Whitcombe (engagement partner —
required by standard), Lindqvist, Haddad, Nwosu, Nazari, Osei, Iyer, Stein; Trent and Park for the full session;
Petrov for 30 minutes; the Brightline UK senior manager for 45 minutes; Herrera observing for 45 minutes without
participating in decisions. *If the IT auditors are treated as guests rather than key team members, nine of the
risks in Exhibit 2-11 will not be raised, and the ones that are will be raised in the wrong terms.*

**Step 3. Circulate the pre-reading five days ahead, and make it short enough to be read.** Brightline sent six
documents on October 2: the FY2024 significant matters memo (2 pages), the internal audit ITGC readiness
assessment (14 pages), the change register (1 page), Exhibits 2-6 and 2-7 (2 pages), the July 2025 compensation
committee minute extract on the ARR-based PSU tranche (1 page), and the metric-to-account pressure map from
Chapter 1, Exhibit 1-11 (1 page). *If the pre-reading exceeds about 25 pages it will not be read, and the meeting
will consist of the manager summarizing it.*

**Step 4. Require each participant to arrive with two written items.** One specific way AtlasFlow's FY2025
financial statements could be materially misstated by fraud, described mechanically; and one candidate risk of
material misstatement stated as account plus assertion plus direction. Collect them at the door. *If participants
arrive empty-handed the adversarial segment produces the two ideas the manager already had.*

**Step 5. Build a time-boxed agenda and publish it with the pre-reading.** Brightline's: business model and
metric pressure, 30 minutes; order-to-cash transaction flow and what-could-go-wrong, 40 minutes; adversarial
fraud segment, 75 minutes; risks arising from IT, 25 minutes; estimates and bias, 25 minutes; conversion to
assertion-level risks and significant risk determination, 15 minutes to open and completed offline. *If the
agenda has no adversarial segment with a protected time box, the segment will be compressed to ten minutes at the
end and will produce nothing.*

**Step 6. Open with the business, not the audit.** Lindqvist spent the first 12 minutes on one question: which
number is each executive paid on? The answers — Marchetti on bookings, Raghunathan on ARR-based PSUs, the sales
organization on Q4 signature-date quota credit, Shah on the capitalized-software program's delivery — are the
foundation of the entire fraud segment. *If the meeting opens with "let's go through the risk register," the
register's existing rows will constrain everything that follows.*

**Step 7. Draw the order-to-cash flow on the whiteboard and stop at each transition.** Opportunity → quote →
CPQ approval → order form → signature → activation in Zuora Billing (I-1) → provisioning on the platform →
invoice → nightly transfer to Zuora Revenue (I-2) → revenue schedule → monthly summary journal to NetSuite (I-3)
→ collection. Eleven transitions. At each, ask what could go wrong and which assertion it affects. This produced
seven of the twelve Part A rows. *If nobody can describe a transition, stop the meeting and go back to the
walkthrough; you cannot assess a process you cannot draw.*

**Step 8. Run the metric-pressure segment against the pressure map.** Take each row of Exhibit 1-11 and ask what
journal entry, field change, or estimate would move that metric. The bookings row produced R-2 and R-25; the ARR
row produced R-29; the gross margin row produced R-32 and the Chapter 10 personnel classification question.
*If a metric row produces no candidate risk, either the metric does not matter to management or the team has not
understood how it is computed; both are worth resolving.*

**Step 9. Run the adversarial segment under one rule: no participant may say "the control would catch it."** Each
of the eleven participants presented the scheme they brought. Nine were variants of four schemes; two were new.
Ben Osei's contribution — that a change to any of the 27 RevPro configuration rules would misstate an entire class
of contracts with no transaction-level trace, and that the shared `revpro_admin` credential is available to six
people — became IT-1 and reshaped R-4. Tara Iyer's contribution — that the CPQ order-form date field has a change
history that nobody reviews and that the history is extractable — became the central procedure in the response to
R-2. *If the segment produces only schemes the manager anticipated, the rule was not enforced; the phrase "the
control would catch it" ends analysis, which is why it is prohibited during the segment and required in Step 10.*

**Step 10. Test each surviving scheme against the control inventory, and record which controls would and would
not detect it.** For Iyer's date-field scheme: REV-01 (discount approval) would not detect it because the
discount is legitimate; REV-06 (provisioning date) would not detect it because a backdated order form has a
consistent start date; REV-04 (RevPro-to-GL reconciliation) would not detect it because the revenue reconciles
to the subledger, which is also wrong; and no control addresses it. That "no control addresses it" conclusion is
the reason R-2's control risk is at maximum and the reason the response required third-party evidence. *If every
scheme is met by an identified control, either the schemes are not adversarial enough or the control inventory is
being read optimistically; ask who performs the control and what they would actually see.*

**Step 11. Bring the IT auditors' risks arising from IT into the same list, in the same form.** Nazari and Osei
presented the nine risks in Exhibit 2-11, each stated as a risk rather than as a missing control, and each mapped
to the accounts and assertions it touches. *If the IT risks are recorded in a separate IT memorandum, they will
not reach the substantive programs, and the substantive team will plan reliance on controls the IT team has
already concluded cannot be relied upon.*

**Step 12. Run the estimate-and-bias segment from the prior-year retrospective review.** Compare each FY2024
estimate to the FY2025 outcome and look for direction. AtlasFlow's FY2024 allowance for credit losses of $1,350
proved insufficient against FY2025 write-offs of $1,230 plus a rising aging; the FY2024 professional services
percentage-of-completion estimates were systematically optimistic on three of the engagements completed in
FY2025. One-directional error across multiple estimates is evidence of bias, not of difficulty. *If every prior
estimate turned out approximately right, say so — that is a real and useful conclusion that reduces assessed
risk, and it should be documented as such.*

**Step 13. Run the change segment against the change register.** Six change events in FY2025: the Insight launch,
the February RevPro configuration change, the Q2 resignations, the Kestrel acquisition, the September NetSuite
upgrade, and the CFO transition. For each, ask which population it affected and whether any control was
re-validated afterward. The answer for the RevPro change — abbreviated user acceptance testing driven by a Q1
close deadline — is the single fact that raised R-4. *If a change event cannot be tied to an affected population,
you do not yet understand the change; ask for the ticket and the deployment record.*

**Step 14. Convert every captured item into the five-slot form, and reject the ones that will not convert.**
Account, assertion, direction, cause, magnitude. Forty-three items were captured in the meeting. Thirty-eight
converted. Five did not and were disposed of explicitly: "management is inexperienced" (a control environment
finding, recorded in Exhibit 2-12, not a risk of material misstatement at an assertion); "the consolidation
spreadsheet is risky" (converted into IT-7 and then into the R-11 response and the Chapter 16 scope);
"the whistleblower hotline may be underused" (no financial statement assertion; noted for the audit committee
communication); "Snowflake access is too broad" (IT-6 and IT-8); and "the Australia entity has one accountant"
(addressed by the Chapter 1 component scoping). *If an item will not convert, do not force it into a row and do
not discard it silently; record where it went.*

**Step 15. Place each converted risk on the inherent risk spectrum by naming the factors present.** Not by
naming the account balance. Use the four-position scale in §2.3 and record the factor codes. This is the step at
which the meeting's energy tempts the team to rate everything High; the discipline is that a High rating obligates
the team to a significant risk designation and everything that follows from it. *If more than about a quarter of
the rows land at the upper end, re-read them and ask which ones are High because of magnitude rather than because
of the factors; magnitude alone is never the reason.*

**Step 16. Test each candidate significant risk against the definition, and write down the ones you reject.**
Twelve candidates; nine designated. The three rejected were R-5 (magnitude constraint: the entire overage stream
is $4,200), R-7 (the population of SLA-bearing contracts is identifiable and the exposure is bounded at
approximately $600 based on FY2025 incident duration), and R-23 (elevated, but the estimate is supported by an
analysis that ties to observable renewal commission rates of 3.1% against 11.8%). *If you cannot articulate why a
candidate was rejected, designate it; the cost of an unnecessary significant risk is a redundant procedure, and
the cost of a missed one is an inadequate response.*

**Step 17. Identify the procedures that would not otherwise have been performed, and list them separately.** This
is the meeting's proof of value. Brightline's list had eleven items, of which five were new to the FY2025 audit:
the CPQ field-history extraction and analysis for the full December population; external confirmation of contract
dates rather than only balances for the 20 largest December contracts; the platform tenant-creation log
comparison for provisioning dates; obtaining every interim PSU probability assessment and comparing each to the
compensation committee materials of the same date; and interviewing developers rather than engineering managers
on project stage. *If the list is empty, the discussion was a briefing.*

**Step 18. Assign an owner and a date to every open item.** Nine open items, each with a name and a date, all
before November 21. *If an item has no owner it will be raised again at the next meeting as a new idea.*

**Step 19. Write the memo within 48 hours and circulate it for confirmation.** The memo records the participants,
the matters discussed, who raised each risk, the conclusions reached, the significant risk determinations and the
rejections, and the action list. Naming the person who raised each risk is what makes the record verifiable.

```text
================================================================================
BRIGHTLINE LLP                                                    WP 2200-01
AtlasFlow, Inc. — FY2025 Integrated Audit
ENGAGEMENT TEAM DISCUSSION MEMORANDUM (AS 2110 and AS 2401)

Date of discussion:  October 7, 2025, 9:00 a.m. – 12:30 p.m. CT, Austin office
Prepared by:         G. Lindqvist (GL)      Date prepared:  October 8, 2025
Reviewed by:         D. Whitcombe (DW)      Date reviewed:  October 9, 2025
Circulated for confirmation to all participants: October 9, 2025;
  confirmations received from all 11 required attendees by October 13, 2025

PARTICIPANTS
  D. Whitcombe, engagement partner (full session)
  G. Lindqvist, senior manager (full session, chair)
  O. Haddad, manager — revenue, deferred revenue, AR (full session)
  C. Nwosu, senior — controls coordination, cash, equity (full session)
  F. Nazari, IT audit senior manager (full session)
  B. Osei, IT audit senior (full session)
  T. Iyer, data and analytics specialist (full session)
  R. Stein, tax partner (full session)
  A. Trent, J. Park, staff (full session)
  Dr. I. Petrov, valuation specialist (10:45–11:15, Kestrel earn-out and TSR PSUs)
  M. Ellsworth, Brightline UK LLP senior manager (9:00–9:45, by video)
  L. Herrera, engagement quality reviewer (10:00–10:45, observer; did not
    participate in the conclusions reached)

MATTERS DISCUSSED
1. The AtlasFlow business model and the measures on which management is
   compensated: bookings (CRO), ARR-based performance RSUs (CEO), Q4
   signature-date quota credit (sales organization), capitalized-software
   program delivery (CTO).
2. The order-to-cash transaction flow, transition by transition, from
   opportunity through collection (11 transitions; whiteboard record retained
   at WP 2200-01A).
3. Fraud brainstorming (75 minutes). Eleven schemes presented, one per
   participant. Four distinct scheme families identified: (a) altering the
   order-form signature or start date; (b) altering RevPro configuration to
   change a class of revenue schedules; (c) using manual journal entries below
   the $250,000 approval threshold to adjust revenue or deferred revenue;
   (d) biasing management estimates (allowance, PSU probability, project
   stage). Each scheme was tested against the identified control inventory and
   the controls that would and would not detect it were recorded.
4. Risks arising from the use of information technology (F. Nazari, B. Osei):
   nine risks, IT-1 through IT-9, mapped to accounts and assertions.
5. Retrospective review of FY2024 estimates and indications of bias.
6. The six FY2025 change events and whether any control was re-validated after
   each.

RISKS IDENTIFIED — SOURCE ATTRIBUTION (selected)
  R-2   Contracts recorded in FY2025 not executed in FY2025 — raised by
        T. Iyer, who identified that the Salesforce CPQ order-form date field
        retains a change history that is extractable and is not reviewed.
  R-4   Modification model misapplied following the February 2025 RevPro
        configuration change — raised by B. Osei from the 27-rule inspection;
        corroborated by D. Kim's disclosure of abbreviated user acceptance
        testing.
  R-10  Manual journal entries below the approval threshold — raised by
        C. Nwosu from W-12.
  R-26  Project stage designation on retroactively restaged Jira epics —
        raised by F. Nazari; O. Haddad added that the time reports are
        approved by the managers who own the project budgets.
  R-29  ARR-based PSU probability — raised by D. Whitcombe from the July 2025
        compensation committee minute recording "tracking behind plan."
  R-34  Kestrel contingent consideration — raised by Dr. I. Petrov, who noted
        that a Monte Carlo simulation of a retention-and-revenue milestone
        must be calibrated to the $4,000 cap and that a first-time acquirer
        rarely does so.

CONCLUSIONS REACHED
1. Forty-three items were captured; 38 converted into risks of material
   misstatement stated at the assertion level and are recorded in the risk
   assessment matrix at WP 2250-01 through WP 2250-07. Five items did not
   convert and their disposition is recorded at WP 2200-01B.
2. Nine risks are designated significant risks: R-1, R-2, R-3, R-10, R-13,
   R-18, R-26, R-29, R-34. Three candidates were considered and rejected
   (R-5, R-7, R-23); the reasons are recorded at WP 2200-01B.
3. The presumption of a fraud risk in revenue recognition is not rebutted.
   Fraud risks are identified at revenue occurrence and cut-off (R-2) and at
   management override (R-10).
4. Eleven procedures were identified that would not otherwise have been
   performed; five are new to the FY2025 audit. Listed at WP 2200-01C.

ACTION ITEMS
  #  Item                                              Owner   Due
  1  Extract CPQ order-form date change history,       T. Iyer 10/17/2025
     full FY2025 population, with field-history fields
  2  Obtain platform tenant-creation logs and assess   B. Osei 10/24/2025
     their reliability as third-party-equivalent evidence
  3  Request all FY2025 interim PSU probability        C. Nwosu 10/24/2025
     assessments and the related board materials
  4  Obtain the Jira epic stage-change audit trail     F. Nazari 10/31/2025
  5  Draft the R-2 response for partner approval       O. Haddad 11/07/2025
  6  Update WP 1100-02 for the risks identified        G. Lindqvist 10/14/2025
  7  Issue UK component instructions incorporating     G. Lindqvist 10/24/2025
     R-11 and the VAT completeness risk
  8  Scope the Kestrel earn-out specialist engagement  D. Whitcombe 11/14/2025
  9  Cross-reference every program step to a risk ref  O. Haddad 11/21/2025
================================================================================
```

**Step 20. Convert the meeting output into matrix rows, and cross-reference the programs.** Each converted item
becomes a row in Exhibits 2-15 through 2-21, with the factor codes, the two ratings, the RMM, the significant risk
determination, and the planned response. Then every program step in the WP 1200 series receives the risk
reference in its header. The table below shows the conversion for six items, and it is worth studying because the
left column is what people actually say in meetings and the right column is what the audit file needs.

| What was said in the meeting | Converted risk | Account and assertion | Direction | Row |
| --- | --- | --- | --- | --- |
| "Forty-one percent of Q4 bookings came in the last week — that can't all be real" | Contracts recorded in FY2025 were not executed in FY2025 | Revenue 4100/4110, occurrence and cut-off; AR 1200; accrued and capitalized commissions 2105/1300 | Revenue, receivables, and commission assets overstated | R-2, R-25 |
| "The RevPro change in February went in fast" | Modifications processed under the wrong ASC 606 model for the 34% of ACV in multi-year ramped contracts | Revenue 4100, accuracy and cut-off; deferred revenue 2400, accuracy | Either direction; the error is one of period, not amount | R-4 |
| "The Insight SSP has almost no data behind it" | The relative-SSP allocation is unsupported | Revenue 4100 and 4110, accuracy and allocation | Overstates the higher-margin element and shifts revenue between periods | R-3 |
| "The overage number jumped in Q4" | Usage overage is overstated or the underlying run counts are unreliable | Revenue 4120, completeness, occurrence, accuracy, cut-off | Both directions possible; bounded by the $4,200 stream | R-5 |
| "Nobody reviews small journal entries" | Manual entries are used to adjust revenue outside the normal process | Revenue 4100–4210 and deferred revenue 2400, occurrence and accuracy | Revenue overstated | R-10 |
| "The PSU probability went to 85% only in Q4" | The probability estimate was biased and the revision was recognized in the wrong period | SBC within 6100/6200/6300 and APIC 3100, accuracy and cut-off | Expense understated in Q1–Q3 and overstated in Q4 | R-29 |

*If a meeting item cannot be placed in the right-hand columns, return to Step 14 rather than writing the row
loosely; a loosely written row generates a loosely designed procedure.*

**Step 21. Set the trigger for reconvening, and reconvene when it fires.** Brightline's triggers: identification
of a fraud risk not previously identified; an allegation of fraud from any source; a control conclusion that
eliminates planned reliance in a significant account; or a misstatement above performance materiality. The second
trigger fired on January 14, 2026 when the audit committee forwarded the whistleblower email, and the team
reconvened on January 15 for 90 minutes with the same participants plus the national office. *If a trigger fires
and the team does not reconvene, the file will show that the auditor learned of an allegation and did not revisit
the assessment on which the entire audit plan rests — which is the finding that turns a misstatement into an
inspection deficiency.*

## Extended Case Study: How the Q4 Bookings Concentration Became a Significant Risk

### Background

Every enterprise software company signs disproportionate business in the fourth quarter. AtlasFlow signed
$61,400 of new and expansion annual contract value in Q4 FY2025 against $46,900 in Q4 FY2024, a 30.9% increase
that is broadly in line with a 24.6% revenue increase and a 25.2% ARR increase. Q4 concentration is therefore
not the finding. It is the *intra-quarter* concentration that is the finding: $25,174, or 41.0%, of Q4 ACV was
signed in the six business days from December 24 to December 31, 2025, against 27% in the same window of the
prior year.

At the October 7, 2025 engagement team discussion, the Q4 pattern was raised as an expected feature of the
business and R-2 was assessed at an elevated inherent risk without a significant risk designation. This case
study traces how that assessment changed on December 19, 2025, what response was designed, and what the
response found. It is worth reading as a study in reassessment: nothing about AtlasFlow's business changed
between October and December. What changed was the arrival of data.

### The Facts

**Exhibit 2-24. December 2025 new and expansion order form population (in thousands, from the Salesforce CPQ
extract of January 6, 2026).**

| Signature window | Order forms | ACV | % of December ACV | Weighted average discount to list | FY2025 revenue recognized |
| --- | --- | --- | --- | --- | --- |
| December 1–18 | 71 | 2,306 | 7.3% | 20.9% | 190 |
| December 19–23 | 46 | 4,120 | 13.0% | 24.4% | 92 |
| December 24–31 | 118 | 25,174 | 79.7% | 34.2% | 71 |
| **Total December** | **235** | **31,600** | **100.0%** | **31.9%** | **353** |
| Comparative: October 1 – November 30, 2025 | 402 | 29,800 | n/a | 21.6% | 1,940 |

Order forms foot: 71 + 46 + 118 = 235. ACV foots: $2,306 + $4,120 + $25,174 = $31,600. Full-quarter ACV of
$61,400 equals $29,800 (October–November) plus $31,600 (December). The December subpopulation splits, the
discount percentages, and the revenue amounts are illustrative extensions; the $61,400, the $25,174, and the 41%
are from the continuing-case file.

Two features of Exhibit 2-24 are worth stopping on.

**The revenue and the ACV move in opposite directions.** The December 24–31 window carries 79.7% of December ACV
and produces $71 of FY2025 revenue — 20.1% of December's $353. The reason is arithmetic: of the $25,174 signed in
that window, only $4,910 across 26 order forms had subscription start dates on or before December 31, 2025, and
those started an average of 5.3 days before year end. The remaining $20,264 across 92 order forms starts on or
after January 1, 2026 and produces no FY2025 revenue whatever. ($4,910 + $20,264 = $25,174.)

**The commission consequence is an order of magnitude larger than the revenue consequence.** Commissions are
earned on signature date at 11.8% of new and expansion ACV. The December 24–31 window therefore generated
$25,174 × 11.8% = $2,971 of commission cost, of which $20,264 × 11.8% = $2,391 relates to contracts that produced
no FY2025 revenue. Against an accrued commission balance of $4,800 in account 2105, the December 24–31 window
accounts for 61.9%.

Three further facts assembled between December 15 and December 19, 2025:

1. **The discount pattern.** The weighted average discount to list rose from 21.6% in October and November to
   34.2% in the final six business days. Forty-two of the 118 order forms exceeded the 30% threshold at which the
   CPQ approval matrix requires the Chief Revenue Officer's approval. All 42 had a recorded approval. Eleven of
   the 42 had an approval timestamp *later than* the recorded customer signature date.
2. **The date field is editable and the edit is invisible.** Brett Hallowell, VP Sales Operations, administers
   Salesforce CPQ and confirmed in the September 12, 2025 inquiry that he can modify the Customer Signature Date
   field on an order form record and that no report or review addresses such changes.
3. **The controls that would have to catch this do not address it.** REV-01 tests discount approval, not dates.
   REV-06 uses the provisioning date, which on a backdated order form is internally consistent with the
   backdated signature date. REV-04 reconciles the revenue subledger to the general ledger, which would
   reconcile perfectly to a wrong subledger.

### What the Engagement Team Did

**Step one: extract the field history and prove the extract complete.** Tara Iyer ran the following query against
the Fivetran-replicated Salesforce tables in Snowflake, then reconciled the resulting order form population to
the ACV total management reported to the board.

```sql
-- WP 2210-06A: December 2025 order form population with signature-date field history
-- Source: Snowflake, SALESFORCE schema (Fivetran-replicated), extracted 2026-01-06 08:14 CT
-- Reconciled to management's Q4 bookings report of 2026-01-05: see WP 2210-06B

with dec_orders as (
    select  o.id                          as order_form_id,
            o.name                        as order_form_number,
            a.name                        as customer_name,
            o.createddate                 as record_created_ts,
            o.createdbyid                 as record_created_by,
            o.customer_signature_date__c  as signature_date,
            o.subscription_start_date__c  as start_date,
            o.acv_usd__c                  as acv_usd,
            o.discount_to_list_pct__c     as discount_pct,
            o.opportunity_type__c         as order_type
    from    salesforce.order_form__c o
    join    salesforce.account a on a.id = o.account_id__c
    where   o.customer_signature_date__c between '2025-12-01' and '2025-12-31'
      and   o.status__c = 'Activated'
      and   o.opportunity_type__c in ('New Business', 'Expansion')
),
sig_changes as (
    select  h.parentid                    as order_form_id,
            count(*)                      as sig_date_edits,
            min(h.createddate)            as first_edit_ts,
            max(h.createddate)            as last_edit_ts,
            max(h.createdbyid)            as last_edited_by,
            listagg(h.oldvalue::string || ' -> ' || h.newvalue::string, ' | ')
                                          as edit_trail
    from    salesforce.order_form__history h
    where   h.field = 'Customer_Signature_Date__c'
    group by 1
)
select  d.*,
        coalesce(s.sig_date_edits, 0)                          as sig_date_edits,
        s.first_edit_ts,
        s.last_edit_ts,
        u.name                                                 as last_edited_by_name,
        s.edit_trail,
        case when d.record_created_ts >= '2026-01-01' then 'CREATED IN FY2026'
             when s.sig_date_edits > 0                then 'SIG DATE EDITED'
             else 'NO FLAG' end                                as audit_flag
from    dec_orders d
left join sig_changes s on s.order_form_id = d.order_form_id
left join salesforce.user u on u.id = s.last_edited_by
order by d.acv_usd desc;
```

**Step two: apply the flags and quantify each stratum.**

**Exhibit 2-25. Field-history analysis of the 235 December order forms (in thousands).**

| Flag | Order forms | ACV | FY2025 revenue | Disposition |
| --- | --- | --- | --- | --- |
| Order form record created in FY2026 with a December 2025 signature date | 9 | 2,340 | 150 | 100% examined; see below |
| Customer Signature Date modified after record creation (record created in 2025) | 31 | 6,880 | 68 | 100% examined; DocuSign completion certificate obtained for each |
| No flag | 195 | 22,380 | 135 | Sampled: 30 order forms selected, weighted to the December 24–31 window |
| **Total** | **235** | **31,600** | **353** | |

Order forms foot: 9 + 31 + 195 = 235. ACV foots: $2,340 + $6,880 + $22,380 = $31,600. Revenue foots: $150 + $68
+ $135 = $353.

**Step three: obtain third-party evidence for the flagged strata.** For each of the 40 flagged order forms,
Amelia Trent requested the DocuSign envelope completion certificate, which is generated by the signature platform
and records the timestamp at which the last signer completed the envelope. The certificate is evidence AtlasFlow
personnel cannot alter after the fact, which is precisely the property the CPQ date field lacks.

Results:

- **31 order forms with post-creation date edits (ACV $6,880).** DocuSign completion certificates obtained for
  all 31. In 28 cases the certificate timestamp agreed with the recorded signature date, and the edit was an
  earlier data-entry correction (for example, a date recorded as 12/09/2025 corrected to 12/19/2025 with a
  certificate timestamp of December 19). In 3 cases the certificate agreed with the *edited* date and the
  original entry was a keying error. No exceptions.
- **9 order forms created in FY2026 with December 2025 signature dates (ACV $2,340).** For 3 (ACV $560), DocuSign
  certificates dated December 29 to December 31, 2025 were obtained; the CPQ record had been recreated in January
  after a connector failure, and Jira ticket ITSM-4417 corroborated the failure. Not exceptions. For the
  remaining **6 (ACV $1,780, FY2025 revenue $150)**, no DocuSign envelope existed at all. The order forms had
  been created in Salesforce between January 2 and January 8, 2026, with Customer Signature Date values between
  December 1 and December 12, 2025 and matching subscription start dates. Management represented that these
  contracts had been executed on paper and countersigned by email; the emails produced were dated in January.
  ($560 + $1,780 = $2,340.)
- **30 sampled unflagged order forms (ACV $9,410 of the $22,380 stratum).** DocuSign certificates agreed to the
  recorded signature dates in all 30 cases. The 11 order forms with a CRO approval timestamp later than the
  signature date were examined separately; in all 11 the approval was a documentation lag, the discount matched
  the executed order form, and the customer signature followed a verbally approved price. No misstatement, but a
  control deviation in REV-01's operation.

**Step four: extend the procedure across the period-end boundary in the other direction.** The mirror image of
backdating December contracts is *deferring* January contracts that were actually signed in December — which nobody
has an incentive to do — and, more importantly, recording January signatures as December. Iyer therefore ran the
same query for January 1 through January 31, 2026 and compared the January signature volume to the prior year.
January 2026 new and expansion ACV was $3,910 against $7,240 in January 2025, a 46.0% decline in a month
immediately following a record December. A depressed January following an inflated December is the pattern
consistent with pull-forward, and it is corroborative rather than conclusive.

### Analysis

The reassessment turned on three questions.

**Does the inherent risk sit close to the upper end of the spectrum?** Yes, and on the bias factor rather than on
magnitude. The likelihood of misstatement is elevated by a specific, documented combination: an incentive
(commission on signature date, CRO compensation on bookings, quarter-close incentives), an opportunity (an
editable date field administered by a single individual with no review), and an absence of any control addressing
the risk. The magnitude of the *revenue* misstatement is small — the entire December 24–31 window carries $71 of
FY2025 revenue — but the magnitude of the misstatement in accrued and capitalized commissions is $2,971 before
payroll taxes, more than twice overall materiality, and the magnitude in bookings and ARR, though outside the
financial statements, drives the PSU probability estimate inside them.

**Is the significant risk designation the right output, as opposed to simply testing more?** Yes, and the reason
is the consequences in Exhibit 2-10. Designating R-2 significant obliges Brightline to perform substantive
procedures specifically responsive to it, prohibits relying on prior-period control evidence, requires
evaluation and testing of the controls addressing it, prohibits satisfying it with analytical procedures alone,
and requires communication to the audit committee. Each of those obligations produced something: the DocuSign
procedure exists because of the first, the field-history extraction because of the third, and the December 19
audit committee call because of the fifth.

**Where does the illustrated conclusion fall in the range of defensible answers?** The range has three positions.
A team could conclude that Q4 concentration is a normal feature of enterprise software, that the revenue exposure
of $71 is trivial, and that no significant risk exists — the position Brightline itself held in October. That
position is defensible on the October information set and indefensible on the December one, because the
intra-quarter concentration rose 14 points year over year and the discount pattern moved 12.6 points, neither of
which was known in October. At the other end, a team could conclude that the pattern indicates pervasive
management override and that the entire revenue population must be tested with third-party corroboration; that is
not defensible because it ignores the magnitude constraint and would consume the budget for the eight other
significant risks. The illustrated conclusion — a significant risk over a defined December population, with
100% third-party corroboration of two flagged strata and a weighted sample of the third — sits between them and
closer to the aggressive end.

What would move the conclusion further: any one of the six uncorroborated contracts being large enough that its
reversal exceeded performance materiality of $940; evidence that a member of management directed the January
creation of December-dated order forms; or a finding that the same pattern existed in the prior year, which would
raise a restatement question about FY2024. Brightline tested the third by running the field-history query for
December 2024; three order forms were created in FY2025 with December 2024 signature dates, all three with
DocuSign certificates, aggregate ACV $190. The prior-year pattern is absent.

### Resolution and Conclusion

R-2 was designated a significant risk on December 19, 2025 and a fraud risk under AS 2401. The response was
designed December 22, approved by Whitcombe December 23, and executed between January 6 and January 28, 2026. It
was expanded on January 16, 2026 following the whistleblower email, to include the January 2026 comparison in
step four and an inquiry of each of the six affected account executives.

Outcome:

- **Known misstatement.** Six contracts, ACV $1,780, FY2025 revenue $150. Management declined to reverse the
  revenue, asserting that the contracts were validly executed in December. Brightline accumulated $150 as
  uncorrected misstatement **U-3**. Quantitatively it is 10.3% of overall materiality; the aggregate net effect of
  all uncorrected misstatements is $(460), or 31.7% of materiality. Chapter 19 evaluates the aggregate.
- **Related misstatement.** The commission and capitalized commission consequence of the same six contracts is
  $1,780 × 11.8% = $210 before payroll taxes, of which the FY2025 expense effect depends on the amortization
  period. Brightline quantified it and included it in the summary of audit differences.
- **Control conclusion.** No control addresses the risk that an order form's execution date is misstated. That is
  a control deficiency in the design of the revenue process, not an operating failure, and it is not compensated
  by REV-01, REV-04, or REV-06. Combined with the fact that a misstatement actually occurred and was not
  prevented or detected by management, Brightline concluded a material weakness in internal control over revenue
  cut-off. Chapter 14 develops the severity analysis; Chapter 20 drafts the report.
- **Qualitative evaluation.** A $150 misstatement arising from contracts papered after the fact is qualitatively
  material irrespective of its size, because it is intentional and because it concerns the integrity of period-end
  recognition. Chapter 19 owns the evaluation and Chapter 17 owns the fraud consequences.

### Workpaper Extract

```text
================================================================================
BRIGHTLINE LLP                                                    WP 2210-06
AtlasFlow, Inc. — FY2025 Integrated Audit
SIGNIFICANT RISK DETERMINATION AND PLANNED RESPONSE —
Q4 2025 REVENUE AND BOOKINGS CONCENTRATION (RISK R-2)

Prepared by:   O. Haddad (OH)         Date prepared:  December 22, 2025
Reviewed by:   G. Lindqvist (GL)      Date reviewed:  December 22, 2025
Approved by:   D. Whitcombe (DW)      Date approved:  December 23, 2025
Updated:       OH, January 16, 2026 — response expanded for the whistleblower
                 allegation (see WP 6400-01)
Updated:       OH, January 28, 2026 — results of procedures added
Cross-referenced to: WP 2250-01 (risk matrix, Part A); WP 1100-02 rev. 4
                 (audit strategy); WP 1200-04 rev. 2 (revenue programs)

PURPOSE
To document (a) the reassessment of risk R-2 from an elevated inherent risk to a
risk of material misstatement whose inherent risk is close to the upper end of
the spectrum, and therefore a significant risk and a fraud risk; (b) the
response designed; and (c) the results.

SOURCE OF INFORMATION
(a) Salesforce CPQ order form extract with field history, Snowflake
    SALESFORCE schema, extracted by T. Iyer 2026-01-06 08:14 CT. Query at
    WP 2210-06A. Completeness reconciled to management's Q4 bookings report of
    2026-01-05 at WP 2210-06B: extract ACV $61,400 for Q4 agrees without
    exception.
(b) Management Q4 bookings report presented to the Board, January 5, 2026.
(c) Inquiry of B. Hallowell (VP Sales Operations), September 12, 2025 and
    January 20, 2026; inquiry of S. Marchetti (CRO), August 25, 2025 and
    January 21, 2026; inquiry of six named account executives, January 21–23,
    2026 (WP 2210-06E).
(d) DocuSign envelope completion certificates obtained directly from the
    DocuSign administrative console in the presence of B. Osei (WP 2210-06D).
(e) Jira ticket ITSM-4417 (CPQ connector failure, December 31, 2025).
(f) Accrued commission detail, account 2105, at December 31, 2025.

BASIS FOR THE SIGNIFICANT RISK DETERMINATION
Inherent risk factors present: susceptibility to management bias or other fraud
risk factors (acute); change.

  1. Incentive.  Commissions are earned on signature date, not on service
     commencement.  The CRO is compensated on bookings.  Quarter-close
     incentives were in effect for December 2025.
  2. Opportunity.  The Customer Signature Date field on the CPQ order form is
     editable by the VP Sales Operations.  No report, review, or reconciliation
     addresses changes to it.                                          (c) ✓
  3. Pattern.  $25,174 of Q4 ACV (41.0% of $61,400) was signed December 24–31,
     2025, against 27% of $46,900 in the comparable FY2024 window — a 14.0
     percentage point increase.  Weighted average discount to list in the
     window was 34.2% against 21.6% for October–November 2025.      (a)(b) ✓
  4. No control addresses the risk.  REV-01 addresses discount authorization;
     REV-06 uses the provisioning date, which on a backdated order form is
     internally consistent; REV-04 reconciles the subledger to the general
     ledger and would reconcile to a misstated subledger.
  5. Allegation.  January 2026 whistleblower email to the Audit Committee
     alleging that "December deals were papered after the fact."

Magnitude:  FY2025 revenue in the December 24–31 window is $71, because $20,264
of the $25,174 has subscription start dates on or after January 1, 2026.  The
commission consequence is $2,971 (11.8% of $25,174), being 61.9% of the $4,800
accrued commission balance.                                              (f) ✓

CONCLUSION ON DESIGNATION:  R-2 is a significant risk (inherent risk High) and a
fraud risk under AS 2401.  Control risk is assessed at maximum; no reliance is
planned or possible.  RMM is High for revenue occurrence and cut-off.

PROCEDURES PERFORMED
1. Extracted the full December 2025 new and expansion order form population
   (235 order forms, ACV $31,600) with signature-date field history, and proved
   the extract complete against management's bookings report.        (a)(b) ✓
2. Stratified by audit flag: 9 order forms created in FY2026 (ACV $2,340);
   31 with post-creation signature-date edits (ACV $6,880); 195 unflagged
   (ACV $22,380).  Strata foot to 235 and $31,600.                        ✓
3. Obtained DocuSign completion certificates for 100% of the 40 flagged order
   forms.                                                              (d) ✓ Δ
4. Selected 30 of the 195 unflagged order forms (ACV $9,410), weighted to the
   December 24–31 window, and obtained DocuSign certificates for each.  (d) ✓
5. Examined the 11 order forms whose CRO discount approval timestamp postdated
   the recorded signature date.                                       (a) ✓ ○
6. Ran the same field-history query for December 2024 to test whether the
   pattern existed in the prior year.                                  (a) ✓
7. Ran the same query for January 2026 and compared new and expansion ACV to
   January 2025.                                                       (a) ✓ ○
8. Tied the December portion of accrued commissions to the tested order form
   population.                                                        (f) ✓

RESULTS
  Δ  Exception.  Six order forms (ACV $1,780; FY2025 revenue $150) were created
     in Salesforce between January 2 and January 8, 2026 with Customer
     Signature Date values between December 1 and December 12, 2025.  No
     DocuSign envelope exists for any of the six.  Management produced
     countersigning emails, all dated in January 2026.  The six account
     executives, interviewed separately, could not identify a December
     execution event for four of the six.  Accumulated as uncorrected
     misstatement U-3, $150, with a related commission effect of $210.
  ○  Observations, not misstatements.  (i) In all 11 cases at procedure 5 the
     discount matched the executed order form and the approval lag was
     documentary; recorded as a deviation in the operation of REV-01 and
     referred to WP 4100-07.  (ii) January 2026 new and expansion ACV of
     $3,910 compares with $7,240 in January 2025, a 46.0% decline; corroborative
     of pull-forward, not conclusive.
  No exceptions at procedures 1, 2, 4, 6, and 8.  Procedure 6 identified three
  December 2024 order forms created in FY2025 (ACV $190), all supported by
  DocuSign certificates dated in December 2024; the prior-year pattern is
  absent.

CONCLUSION
The response designed for R-2 was performed and is sufficient in extent and
appropriate in nature to address the significant risk.  A known misstatement of
$150 (revenue) and $210 (commission cost) was identified and is accumulated at
WP 6700-01.  No control prevents or detects the misstatement of an order form's
execution date; the deficiency is a design deficiency, a misstatement occurred,
and management did not detect it.  Referred to WP 4900-02 for severity
evaluation (material weakness conclusion) and to WP 6400-01 for the fraud
evaluation.

Tick mark legend:
  ✓  Procedure performed as described; no exception unless otherwise marked.
  Δ  Exception identified; see Results.
  ○  Observation identified that is not a misstatement; see Results.
  (a)–(f)  Agreed to the correspondingly lettered source of information above.
================================================================================
```

### Lessons

1. **Concentration is not the risk; the change in concentration is.** Q4 skew rose 30.9% year over year, which is
   in line with revenue growth and is uninformative. The last-six-days share rose from 27% to 41%, a 14-point
   move, and the discount rate in that window rose 12.6 points. Compute the second-order change, not the level.
2. **Size the risk on the account it actually hits.** The revenue exposure of the December 24–31 window is $71.
   The commission exposure is $2,971. A team that sized this risk on revenue would have scoped five contracts and
   found nothing; the response that found the misstatement was scoped on the control significance and the
   commission magnitude.
3. **Ask what evidence exists that the client cannot alter.** The entire response turns on the DocuSign
   completion certificate, which is generated by a third party and timestamped outside AtlasFlow's control. When
   the risk is fabrication, the response must be evidence with a chain of custody outside the entity. Everything
   inside CPQ, Zuora, and NetSuite is internally consistent with the fabrication.
4. **Field history is evidence, and it is almost always available.** Salesforce, NetSuite, and Zuora all retain
   change history on configured fields. Most engagements never extract it. It converted a population of 235 into
   two strata of 40 that could be tested 100% and one stratum of 195 that could be sampled.
5. **Test the boundary in both directions and test the prior year.** The January 2026 comparison and the
   December 2024 field-history run cost four hours between them and materially strengthened the conclusion — one
   corroborating the pull-forward inference, the other eliminating a prior-period restatement question.
6. **Reassessment is not an admission of error.** The October assessment was defensible on the October
   information. The failure mode is not assessing a risk as elevated in October; it is failing to revisit the
   assessment when the December data arrives, or revisiting it and not documenting the change and its
   consequences.
7. **A quantitatively immaterial misstatement can drive the report.** U-3 is $150 against $1,450 of materiality.
   It drove a material weakness conclusion, an adverse ICFR opinion, and a critical audit matter. The graded
   vocabulary matters here: $150 is a *misstatement*; the 11 late approvals are *control deviations*; the absent
   date control is a *deficiency* that aggregates to a *material weakness*. Chapters 14, 19, and 20 own those
   determinations.

## Common Mistakes

### Mistake 2.1 — Recording one blended risk rating instead of separate inherent and control risk assessments

**What it looks like.** The matrix has a single column headed "Risk" or "RMM" containing High, Moderate, or Low,
and no column for inherent risk. Where a reviewer asks why revenue accuracy is High, the answer is "because
controls are weak."

**Why it happens.** Firm templates written before SAS 145 and the corresponding PCAOB amendments carried a single
combined column, and combining is faster: one judgment instead of two. It also feels harmless, because the
extent of testing depends on the combination.

**What goes wrong.** Three things, all of them structural. First, the significant risk determination becomes
impossible, because a significant risk is determined from inherent risk alone (§2.8) and there is no inherent
risk column to read. Second, the assessment cannot be revised coherently: when control testing produces an
unexpected deviation, you cannot tell how much of the blended rating was already attributable to control risk.
Third, the blend hides the case that matters most — high inherent risk with effective controls — and in that case
the standards still require substantive procedures for a significant risk, which a blended "Moderate" will not
prompt you to perform. At AtlasFlow, R-6 has inherent risk Elevated and control risk Moderate; a single blended
"Moderate" would obscure that the reseller conclusions are subjective judgments that must be evaluated regardless
of how well the technical accounting memorandum was reviewed.

**How to avoid it.** Use two columns and populate the inherent risk column *before* you consider controls at all.
A useful discipline: draft the entire inherent risk column at the engagement team discussion, when no control
testing has been performed, and open the control risk column only afterwards.

### Mistake 2.2 — Writing the risk at the account level instead of the assertion level, with no direction

**What it looks like.** "Revenue may be misstated." "Deferred revenue may not be accurate." "Risk that
capitalized commissions are incorrect." Each row names an account and stops.

**Why it happens.** Account-level statements are unfalsifiable and therefore safe. They are also what a
financial statement caption looks like, so a matrix built from the trial balance produces them naturally.

**What goes wrong.** A risk statement that does not name the assertion cannot generate a procedure, because
procedures respond to assertions. "Revenue may be misstated" is equally consistent with a confirmation, a
provisioning-date recomputation, a credit memo analysis, and a completeness test on deferred revenue — which is
to say it directs none of them. Omitting the direction compounds the problem: a test designed for overstatement
of revenue (examine recorded items) will not detect understatement (find unrecorded items), and a reviewer
cannot judge sufficiency without knowing which one you were looking for. At AtlasFlow, a single row reading
"revenue cut-off risk" collapses R-1 and R-2: R-1 is the wrong one of two legitimate dates and is tested by
recomputing revenue commencement from provisioning data, while R-2 is a fabricated date and is tested by
third-party corroboration. The R-1 test cannot detect R-2, because a backdated order form has an internally
consistent provisioning record.

**How to avoid it.** Require every row to complete the sentence: "[Account] is [over/under]stated because [event],
affecting the [assertion] assertion." If a row cannot be written in that form, it is a topic, not a risk.

### Mistake 2.3 — Deriving the significant risk designation from the combined RMM

**What it looks like.** The matrix contains a rule such as "RMM High = significant risk," so every assertion with
maximum control risk becomes a significant risk, and an assertion with high inherent risk and effective controls
does not.

**Why it happens.** The pre-2021 vocabulary treated "significant risk" and "high risk" as near-synonyms, and the
combined rating is the number that drives sample sizes, so it feels like the operative conclusion.

**What goes wrong.** The designation is over-inclusive and under-inclusive at the same time. Over-inclusive
because control weaknesses in a first-year integrated audit push nearly everything to maximum control risk; at
AtlasFlow that rule would designate 34 of 38 risks significant, and a matrix with 34 significant risks provides
no prioritization at all. Under-inclusive because a genuinely subjective estimate with a well-controlled process
would escape designation and therefore escape the requirement to perform substantive procedures specifically
responsive to it and the prohibition on relying on prior-period control evidence.

**How to avoid it.** Read the inherent risk column, ask whether the combination of likelihood and magnitude
places the risk at the upper end of the spectrum, and record the answer in a separate column. Nine of AtlasFlow's
38 risks pass that test. Test your own matrix by asking what happens to the significant risk count if control
risk is set to Maximum everywhere: if the count changes, your determination is wrong.

### Mistake 2.4 — Assessing control risk below maximum without having tested the control

**What it looks like.** The control risk column reads Low or Moderate at the planning date, with a cross-reference
to a control description in the client's SOX narrative and no cross-reference to a test.

**Why it happens.** The planning matrix is prepared in September or October, before interim controls testing, and
the preparer records the assessment they expect to reach. Reducing planned control risk also reduces planned
substantive hours, which makes the budget work.

**What goes wrong.** Under both AS 2110 and AU-C 315, an assessment of control risk below maximum requires tests
of the operating effectiveness of the relevant controls; without them the substantive extent has been reduced on
the basis of a hope. The failure surfaces in February, when the control test fails and there is no time to expand
substantive testing. At AtlasFlow the November 21 reassessment is the honest version of this: reliance was
planned on two IT-dependent controls, the access review deficiency (W-3) removed the ITGC foundation, control
risk moved to Maximum for R-1, R-4, and R-9, and the R-1 provisioning-date test expanded from a sample of 60 to
the full 4,118-subscription population at a cost of 40 hours. Discovering that in November is survivable;
discovering it in February is not.

**How to avoid it.** Label the column "planned control risk" and require every entry below Maximum to name the
control, the ITGC on which it depends, and the planned test with a workpaper reference. Then set a date — at
AtlasFlow, November 30 — by which every planned reliance is either confirmed or withdrawn, and price the
withdrawal in hours in advance.

### Mistake 2.5 — Testing the recorded deferred revenue balance to address completeness

**What it looks like.** The deferred revenue program selects 40 items from the December 31 deferred revenue
subledger, agrees each to a contract and an invoice, recomputes the unrecognized portion, and concludes on
completeness.

**Why it happens.** Every other balance is tested this way, and the deferred revenue subledger is the obvious
population. Existence and completeness feel like two sides of the same test.

**What goes wrong.** The population is wrong for the assertion. Understated deferred revenue means an obligation
is *missing* from the subledger; a sample drawn from the subledger cannot select an item that is not in it. At
AtlasFlow the specific omissions the risk contemplates are the $200 material right in C-2 Voltaire, subscriptions
billed but not yet provisioned, and professional services elements never separately recorded — none of which
would appear in a subledger-based sample. R-13 is a significant risk precisely because it requires a
source-to-record test: the complete population of executed contracts from Zuora Billing (5,240 active
subscriptions), proved complete against the CPQ "Closed Won" population, and then tested for whether each
obligation is represented in the liability.

**How to avoid it.** For every completeness risk, write down the population you will test *from* before you write
the procedure, and require that population to originate outside the account being tested. If the population is
the account, you are testing existence and should say so.

### Mistake 2.6 — Documenting the five components as narrative and never naming a control relevant to the audit

**What it looks like.** Five well-written memoranda describing the control environment, the entity's risk
assessment process, monitoring, information and communication, and control activities, followed by an audit plan
that relies on no control and cites none of the five memoranda.

**Why it happens.** The standards require an understanding of all five components, and inspection findings
frequently concern missing documentation of the understanding, so teams document the understanding thoroughly and
treat it as a compliance deliverable rather than as an input.

**What goes wrong.** The understanding is severed from the assessment. The control environment memorandum notes a
new CFO, two revenue accountant resignations, and a VP of Revenue Accounting on a performance plan; the risk
matrix carries no consequence of any of it. The correct consequence is specific and traceable: those three facts
support the inherent risk ratings on the estimates in R-3, R-23, and R-29 and the control risk ratings on the
close controls, and each of those rows should cite the memorandum.

**How to avoid it.** Require every component memorandum to end with a section headed "Effect on the risk
assessment" listing the matrix rows it supports, and require the matrix to cite back. If a component memorandum
cannot name a row it affected, either the memorandum is not being used or a row is missing.

### Mistake 2.7 — Treating the ITGC conclusion as a global switch

**What it looks like.** Either "ITGCs are deficient, therefore control risk is maximum for every assertion and no
automated control can be relied upon," or the opposite, "the SOC 1 report is unqualified, therefore access and
change management are fine."

**Why it happens.** Both versions save work. A global conclusion avoids the mapping exercise, which is tedious:
you must connect each ITGC deficiency to the applications it touches, then to the automated controls and
IT-dependent manual controls within those applications, then to the assertions those controls address.

**What goes wrong.** The first version discards reliance that was available and inflates the substantive budget.
The second version relies on controls whose supporting ITGCs failed. At AtlasFlow both errors are available in
the same file. W-1 concerns four local administrator accounts in Zuora Revenue, which affects the revenue
subledger configuration and therefore R-1, R-4, and R-14 — but not the ADP payroll interface or the Coupa
three-way match, which the global version would also condemn. Conversely the Zuora SOC 1 report covers October 1,
2024 through September 30, 2025 and notes two of 25 change tickets without evidence of approval; no bridge letter
was obtained for the October to December gap (W-9), so the report cannot support the last quarter of the year at
all, which is the quarter containing the December risk.

**How to avoid it.** Build the mapping table — deficiency to application to control to assertion — and let the
control risk column be its output. Where a SOC 1 period does not cover the full audit period, state the gap in
months and say what covers it.

### Mistake 2.8 — Rolling forward last year's matrix and updating the numbers

**What it looks like.** The FY2025 matrix has the same rows as the FY2024 matrix, in the same order, with FY2025
balances substituted and one row added for the acquisition.

**Why it happens.** It is efficient, the prior year passed review, and the business genuinely has not changed
much. Continuity also looks like consistency to a reviewer.

**What goes wrong.** The rows that matter in a given year are the ones the prior year did not have. AtlasFlow's
FY2025 file has to carry the loss of emerging growth company status and the first integrated audit, a new SKU
whose standalone selling price has 31 observations, a February configuration change deployed with abbreviated
user acceptance testing, a September NetSuite upgrade during which segregation-of-duties roles were rebuilt, a
new CFO, an acquisition of an entity with modified-cash records, a restructuring, and a Snowflake datamart that
became the source of MD&A metrics in November without a reconciliation to the general ledger. A roll-forward
produces a matrix in which none of those appears as a *change* factor even though change is one of the five
inherent risk factors, and Ch is the factor most often absent from rolled-forward files.

**How to avoid it.** Build the change register first — every event in the year with an accounting or systems
consequence, dated — and require each entry to be dispositioned into a matrix row or explicitly excluded with a
reason. Then read the prior-year matrix, not the other way round.

### Mistake 2.9 — Sizing a risk on the account with the largest balance rather than the account the risk hits

**What it looks like.** The Q4 cut-off risk is scoped against revenue of $148,200 and materiality of $1,450,
producing a conclusion that the December 24–31 window carries $71 of revenue and is immaterial, and a sample of
five contracts.

**Why it happens.** Cut-off is filed under revenue, and revenue is the largest account. The exposure calculation
follows the filing.

**What goes wrong.** The misstatement lands somewhere else. Commissions are earned on signature date at 11.8% of
new and expansion ACV, so the December 24–31 window produced $2,971 of commission cost before payroll taxes,
61.9% of the $4,800 accrued commission balance, of which $2,391 relates to $20,264 of ACV that produces no
FY2025 revenue at all. A team that sized the risk on revenue would have designed a five-contract sample and
found nothing. The response that found the six uncorroborated contracts was scoped on the control significance
and on the commission magnitude.

**How to avoid it.** For every risk, list every account the underlying event touches — revenue, receivables,
deferred revenue, accrued commissions, capitalized commissions, bookings and the metrics derived from them — and
size the risk on the largest exposure, not the largest balance.

### Mistake 2.10 — Reassessing a risk without recording the consequence

**What it looks like.** A reassessment log with columns for date, trigger, and revised assessment, and entries
such as "R-2 elevated to significant risk." No column for what changed in the audit.

**Why it happens.** The log is understood as a record of compliance with the requirement to revise the
assessment, and the revision is what the requirement names.

**What goes wrong.** The assessment and the response drift apart, and the drift is invisible until a reviewer or
an inspector asks what the reassessment caused. If nothing changed, either the reassessment was cosmetic or the
original response was already sufficient — and if the latter, the original assessment was wrong. Both answers are
findings. AtlasFlow's log (Exhibit 2-23) names a consequence in every row, including the reductions: the November
24 entry reduces control risk for one assertion and reduces the transaction-price sample from 40 contracts to 25,
which is exactly the entry an inspector will test, because it is the one where the audit did less.

**How to avoid it.** Make the consequence column mandatory and make it quantitative: hours added, population
expanded from n to m, procedure added at workpaper reference, program revised to version k. A log entry with an
empty consequence column is not complete.

### Mistake 2.11 — Treating the management override fraud risk as satisfied by the journal entry program

**What it looks like.** The fraud risk section identifies management override, and the response is a
cross-reference to the journal entry testing program. The matrix contains no other row carrying the bias factor.

**Why it happens.** Journal entry testing is the visible, checklist-able response to override, and it is a real
requirement. Having performed it, a team feels it has addressed the risk.

**What goes wrong.** Override does not require a journal entry. At AtlasFlow the six uncorroborated December
contracts were recorded through the ordinary order-to-cash flow — Salesforce CPQ to Zuora Billing to Zuora
Revenue to a scheduled interface journal — and would not appear in any manual entry population. The PSU
probability revision from 100% to 85% is an estimate input, not an entry. The retroactive restaging of Jira
epics is a field change in a ticketing system. Journal entry testing addresses one channel; the other channels
are estimates, system configuration, and source-data manipulation, and each requires its own row.

**How to avoid it.** Enumerate the channels through which override can reach the financial statements — manual
entries, top-side consolidation entries outside the general ledger (27 entries, $6,200 at AtlasFlow), estimate
inputs, system configuration, and source-data fields — and require at least one matrix row per channel that is
present. Then check that each has a response other than the journal entry program.

### Mistake 2.12 — Excluding non-GAAP metrics from the risk assessment because they are outside the financial statements

**What it looks like.** ARR, net revenue retention, gross retention, and remaining performance obligation are
handled in the "other information" section of the file. The risk matrix contains no row about them.

**Why it happens.** The auditor's responsibility for other information under AS 2710 and AU-C 720 is narrower
than for the financial statements, and the metrics are not general ledger balances, so they read as somebody
else's problem.

**What goes wrong.** The metrics are inputs to amounts that *are* in the financial statements, and they are the
mechanism by which incentive becomes misstatement. ARR determines vesting of the performance RSUs, which carry
$8,200 of unrecognized cost and produced a $1,340 catch-up credit when the probability estimate moved from 100%
to 85%. Bookings determine the Chief Revenue Officer's compensation, which is the incentive underlying R-2 and
R-25. Remaining performance obligation of $214,000 is a required ASC 606 disclosure computed from the same
contract-term judgments as R-12, so it is not other information at all. And the metrics are computed in a
Snowflake datamart that was not reconciled to the general ledger for the first three quarters of FY2025 (W-11).

**How to avoid it.** For every disclosed metric, ask three questions: is it a required financial statement
disclosure (RPO is); does any recorded amount depend on it (ARR does, through the PSUs); and does anyone's
compensation depend on it (bookings do). A yes to any of the three puts it in the matrix.

## Practice Exercises

Every number you need is given. Figures are in thousands of US dollars.

### Exercise 2-1 — What the deferred revenue roll-forward does and does not prove [Foundational]

AtlasFlow's FY2025 deferred revenue roll-forward is: opening balance (current and noncurrent) $62,300; billings,
net of credits, $163,750; revenue recognized from the beginning balance $(54,900); revenue recognized from
current-period billings $(93,300); deferred revenue acquired from Kestrel $610; foreign currency translation
$(260); closing balance $78,200, split $71,300 current and $6,900 noncurrent. Total FY2025 revenue per the
statement of operations is $148,200, of which usage overage is $4,200 (billed monthly in arrears),
time-and-materials professional services is $3,100 (billed as delivered), and self-serve Core revenue is $6,100
(billed monthly by credit card through Stripe).

Required: (a) prove that the roll-forward foots; (b) compute total revenue explained by the roll-forward and
compare it to $148,200; (c) compute the percentage of the opening balance recognized during FY2025; (d) show that
the billings line can be derived arithmetically from the other five lines, and state what that implies for using
the roll-forward as evidence about billings.

### Exercise 2-2 — Naming the inherent risk factors [Foundational]

For each of the following AtlasFlow facts, name every inherent risk factor present using the codes S
(subjectivity), C (complexity), U (uncertainty), Ch (change), and B (susceptibility to management bias or other
fraud risk factors), and name the factor that dominates.

1. The Insight module launched in January 2025 and had 31 standalone sales during FY2025 across a price band with
   an interquartile range of 22% of list; its standalone selling price allocates the transaction price on nearly
   every FY2025 multi-element contract.
2. Contract C-5 Pemberton Manufacturing has a 24-month stated term and a clause allowing termination for
   convenience on 30 days' notice with no penalty.
3. The ARR-based performance RSU tranche was assessed 100% probable in Q3 2025 and revised to 85% in Q4 2025,
   producing a $1,340 catch-up credit; the CEO's compensation is weighted to these awards.
4. 22% of the FY2025 capitalized internal-use software hours were coded to Jira epics whose stage designation was
   changed retroactively during the year, and developer time reports are approved by the engineering managers who
   own the projects' budgets.
5. Zuora Revenue was reconfigured in February 2025 to accommodate ramped contracts, with abbreviated user
   acceptance testing.
6. The Kestrel contingent consideration of $2,500 is measured by Monte Carlo simulation of a
   retention-and-revenue milestone payable in Q1 2027, using an assumed revenue volatility of 32% and a
   risk-adjusted discount rate of 11.5%, with a maximum payout of $4,000.

### Exercise 2-3 — From the five components to a control relevant to the audit [Foundational]

Each item below is evidence Brightline obtained during risk assessment. For each, state which of the five
components of the system of internal control it informs, and state whether it identifies a *control relevant to
the audit* — meaning a control Brightline would either test for reliance or evaluate for ICFR purposes — or only
informs the assessment of risk.

1. CFO Tom Okafor joined in September 2025 in his first public-company role; two revenue accountants resigned in
   Q2 2025; VP Revenue Accounting Daniel Kim has been on a performance plan since March 2025.
2. NetSuite is configured to require a second approver on manual journal entries only above $250,000; 3,847 of
   4,912 FY2025 manual entries were below the threshold.
3. Internal audit, co-sourced with an outside provider and reporting to the audit committee, issued an ITGC
   readiness assessment in July 2025 identifying 14 gaps.
4. FloQast records the preparer and reviewer sign-off dates for each account reconciliation in the monthly close
   checklist.
5. The RevPro-to-NetSuite monthly summary journal (interface I-3) is reviewed and approved by Controller Elena
   Vasquez before posting, and the interface totals are agreed to the RevPro "Revenue Contract Summary."
6. AtlasFlow has no documented process for identifying and assessing the accounting consequences of new
   contractual terms introduced by the sales organization.

### Exercise 2-4 — An independent expectation for Q4 usage overage [Intermediate]

FY2025 revenue by quarter: Core subscription $24,100, $25,700, $26,900, $28,200; Insight subscription $5,400,
$6,300, $7,200, $7,800; usage overage $780, $940, $1,090, $1,390. Overall materiality is $1,450, performance
materiality $940, and the clearly trivial threshold $72.

Required: (a) compute Q4 sequential growth in overage and in Core subscription revenue; (b) develop an
expectation for Q4 overage by applying the Core growth rate to Q3 overage, and compute the difference from
recorded overage; (c) compute overage as a percentage of Core revenue for each quarter and develop a second
expectation from the quarterly trend in that ratio; (d) state the resulting range of unexplained difference and
compare each end of it to the clearly trivial threshold and to performance materiality.

### Exercise 2-5 — Does the arithmetic support inherent risk High on the allowance? [Intermediate]

The December 31, 2025 aging and the historical loss rates management applies are: current (not yet due) $22,550
at 0.4%; 1–30 days past due $8,190 at 1.6%; 31–60 days $3,740 at 6.0%; 61–90 days $1,970 at 18.0%; 91–180 days
$1,440 at 42.0%; over 180 days $710 at 85.0%. Gross accounts receivable is $38,600 and the recorded allowance is
$1,900. At December 31, 2024 gross receivables were $30,500 and the allowance was $1,350. Sundown Media Holdings
is $980 and 94 days past due. Brightline's independent range for the allowance is $1,780 to $2,410, and
uncorrected misstatement U-2 is $240.

Required: (a) prove the aging foots to $38,600; (b) compute the allowance implied by applying the stated loss
rates to each bucket; (c) compare it to the recorded $1,900; (d) compute the allowance as a percentage of gross
receivables for both years; (e) locate the recorded $1,900 and the auditor's implied point estimate within the
$1,780–$2,410 range; (f) conclude on whether the arithmetic supports the inherent risk rating of High in R-18,
and give the best argument on the other side.

### Exercise 2-6 — Sizing the December commission exposure [Intermediate]

Of the $25,174 of new and expansion annual contract value signed December 24–31, 2025, $4,910 across 26 order
forms has subscription start dates on or before December 31, 2025 (an average of 5.3 days before year end) and
$20,264 across 92 order forms starts on or after January 1, 2026. Commissions on new and expansion business are
11.8% of annual contract value, earned on the customer signature date, and are capitalized with the employer
portion of payroll taxes and amortized over four years. Accrued commissions (account 2105) are $4,800 and
deferred contract acquisition costs (accounts 1300 and 1305) total $24,000. For this exercise, assume an
effective employer payroll tax rate on these commissions of 6.2% — an illustrative extension, since the
continuing case does not state a rate. Overall materiality is $1,450 and the clearly trivial threshold is $72.

Required: (a) compute the commission cost generated by the December 24–31 window in total and split between the
contracts that start in 2025 and those that start in 2026; (b) compute the capitalizable amount including payroll
taxes; (c) compute the FY2025 amortization on the portion relating to contracts that commenced in 2025, using a
1,460-day amortization period and the stated average of 5.3 days of elapsed service; (d) express the window's
commission cost as a percentage of account 2105 and of the $24,000 asset; (e) compute the commission reversal
required if the six uncorroborated contracts with aggregate ACV of $1,780 were reversed, and compare it to
materiality and to the clearly trivial threshold.

### Exercise 2-7 — Should R-5 be reassessed to High and designated a significant risk? [Intermediate; judgment]

Using your answer to Exercise 2-4 and the following facts, write a conclusion of 150 to 250 words. Usage overage
revenue is $4,200 for FY2025. The workflow-run counts that drive it are produced by the AtlasFlow platform hosted
in AWS, which is outside the boundary of the ITGCs Brightline scoped for the financial reporting applications.
The contractual rate for contract C-1 Meridian is $12 per 1,000 runs against an included volume of 200,000 runs
per year, and Meridian consumed 244,000 runs in its first contract year. Overage is billed monthly in arrears, so
recognition precedes billing. Performance materiality is $940 and overall materiality is $1,450. The current
assessment is inherent risk Elevated, control risk High, RMM High, not a significant risk.

Required: state your conclusion on the inherent risk rating and on the significant risk designation, give the
range of defensible positions, say which evidence would move you, and state what you would do differently in the
audit program if the risk were designated significant.

### Exercise 2-8 — Find the errors in a risk matrix extract [Intermediate]

The extract below was prepared by a first-year staff member for a different SaaS engagement and submitted for
review. It contains at least eight defects. Identify them and state the correction for each.

**Exhibit 2-26. Defective risk assessment matrix extract submitted for review.**

| Ref | Risk | Assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| X-1 | Revenue may be misstated as a result of errors and irregularities in the revenue process, including cut-off, allocation, and the standalone selling price | All assertions | S, C, U, Ch, B | **High.** Control risk is high because the ITGC deficiencies identified by internal audit affect all revenue applications, and the entity has never been subject to an ICFR audit | Low — management's SOX narrative describes a monthly revenue review control performed by the Controller | High | **Yes** — RMM is High | Perform a substantive analytical procedure comparing monthly revenue to the prior year and to budget, and investigate variances exceeding 10% |
| X-2 | Capitalized commissions may be incorrect | Valuation | S | **Moderate.** The commission asset of $24,000 is 7.5% of total assets, which is below the 10% threshold in the firm's scoping guidance | Low | Low | No | Rely on the prior year's testing of the commission approval control, which was found effective, and perform a roll-forward analytic on the asset balance |

### Exercise 2-9 — Draft a matrix row for the Voltaire material right [Intermediate; drafting]

Contract C-2, Voltaire Logistics S.A., is a renewal signed October 1, 2025 for 24 months with a total fixed fee of
$1,600, contracted in EUR (€1,480) through AtlasFlow Software Ltd, whose functional currency is GBP, with USD as
the reporting currency. The contract includes a $200 "renewal credit" usable only toward a future purchase of the
Insight module. For this exercise assume — as an illustrative extension, since the continuing case does not give
the population — that 63 FY2025 contracts contain a credit or discount usable only on a future purchase, with an
aggregate face value of $1,940, and that management estimates a 60% likelihood of exercise. Component materiality
for the UK entity is $580 and component performance materiality is $380.

Required: (a) write the complete matrix row in the format of §2.12 — risk statement with direction, relevant
assertions, inherent risk factors, inherent risk rating with rationale, planned control risk, RMM, significant
risk determination, and planned response; (b) compute the FY2025 revenue effect on C-2 alone of accounting for
the material right as a separate performance obligation rather than ignoring it, assuming relative standalone
selling prices of $1,600 for the subscription and $120 for the material right; (c) state what evidence would move
your inherent risk rating.

### Exercise 2-10 — Draft the fraud paragraph of the engagement team discussion memorandum [Advanced; drafting]

Draft the paragraph of WP 2200-01 (the October 7, 2025 engagement team discussion memorandum) that documents the
fraud discussion required by AS 2110 and AS 2401. Write 150 to 200 words. It must name the incentives, the
opportunities, the attitudes or rationalizations discussed, the participants who contributed the facts, the risks
the discussion produced, and at least one risk that was considered and rejected with the reason. Use these facts:
commissions are paid on booked ACV with accelerators above quota; the CRO is compensated on bookings and sets
quarter-close incentives; the CEO's compensation is weighted to ARR-based performance RSUs; the CFO started in
September 2025; the VP Revenue Accounting has been on a performance plan since March 2025 and owns the RevPro
configuration; the VP Sales Operations can modify order-form dates in Salesforce CPQ; NetSuite requires a second
journal entry approver only above $250,000; AtlasFlow reported a net loss of $21,400 but positive operating cash
flow of $34,400; and the minimum-liquidity covenant on the undrawn $50,000 revolver is $40,000 against cash and
equivalents of $96,400.

### Exercise 2-11 — Mapping ITGC deficiencies to control risk by assertion [Advanced; judgment]

Six observations are relevant: W-1, four local non-federated administrator accounts in Zuora Revenue, one of them
a shared account whose password is in a vault entry accessible to six people; W-2, 11 users retained the legacy
NetSuite "Full Access" role for 27 days after the September 2025 upgrade; W-3, user access reviews for
Salesforce, Zuora, and NetSuite were annual rather than quarterly, with the Q2 2025 review 41 days late; W-5,
terminated-user access removal averaged 6.2 days against a 24-hour SLA, with three terminated employees retaining
Salesforce access for over 30 days; W-6, two developers have standing write access to the production Zuora Revenue
configuration; W-12, journal entry approval in NetSuite requires a second approver only above $250,000 and 3,847
of 4,912 manual entries were below it.

Required: (a) for each observation, name the applications affected and the specific matrix rows from §2.12 whose
control risk it bears on; (b) explain why an unqualified Oracle NetSuite SOC 1 report for November 1, 2024 through
October 31, 2025 does not mitigate W-2; (c) explain why W-12 is a design matter rather than an operating failure
and what that means for whether it can be remediated by testing more entries; (d) state which of the six is *not*
an ITGC at all and what that changes about how it is evaluated.

### Exercise 2-12 — Testing the internal consistency of RPO, ARR, and deferred revenue [Advanced]

Disclosed figures: remaining performance obligations $214,000 at December 31, 2025 and $168,500 at December 31,
2024; RPO expected to be recognized within twelve months $138,900 (64.9%) and $110,100; ARR $172,000 and
$137,400; deferred revenue $78,200 and $62,300. FY2025 subscription revenue is $135,800 and FY2024 subscription
revenue is $108,300. FY2025 revenue includes usage overage of $4,200, time-and-materials professional services of
$3,100, and self-serve Core revenue of $6,100 across 11,400 monthly-billed accounts. Ninety-six arrangements
contain a termination-for-convenience clause; assume, as an illustrative extension, that they carry $8,400 of
remaining contracted value at December 31, 2025, of which $310 falls within the 30-day notice window and $5,600
sits in the next-twelve-months portion of RPO.

Required: (a) verify the 64.9% split; (b) compute the unbilled contracted amount (RPO less deferred revenue) for
both years; (c) compute RPO as a multiple of ARR for both years; (d) compare next-twelve-months RPO at each
balance sheet date with the following year's subscription revenue, and explain why the relationship looks
alarming and is not; (e) recompute RPO and the twelve-month portion on the assumption that the enforceable term of
the 96 termination-for-convenience arrangements is 30 days, and express the reduction as a percentage and as a
multiple of overall materiality of $1,450.

### Exercise 2-13 — Selecting the risks that require Australia-specific procedures [Advanced; spans Chapter 1]

Chapter 1, §1.7 concluded that AtlasFlow Pty Ltd (Australia) is a specified-procedures component rather than a
full-scope component: FY2025 revenue $12,500, total assets $12,900, component materiality $420, no local
statutory audit requirement, all transactions processed in the same Salesforce CPQ, Zuora, and NetSuite instances
as the parent, functional currency AUD translated at 0.6410 USD/AUD, cash of $3,200 in account 1035, and an
office consolidation in the October 2025 restructuring.

Required: (a) from the 38 risks in §2.12, identify those for which the Australian component requires a
*component-specific* procedure rather than being covered by a centrally executed procedure, and explain the
distinction in each case; (b) compute component materiality as a percentage of overall materiality and of
Australian revenue; (c) draft the three instruction paragraphs Brightline would send to the group team member
performing the specified procedures, each naming the risk reference, the procedure, the population, and the
threshold for reporting a difference back to the group team.

## Solutions to Practice Exercises

### Solution 2-1

**(a) The roll-forward foots.** $62,300 + $163,750 = $226,050; less $54,900 = $171,150; less $93,300 = $77,850;
plus $610 = $78,460; less $260 = $78,200. The closing split cross-foots: $71,300 + $6,900 = $78,200.

**(b) Revenue explained.** $54,900 + $93,300 = $148,200, which equals total revenue exactly. That is not
reassurance; it is a warning. At least $7,300 of FY2025 revenue — usage overage of $4,200 billed monthly in
arrears and time-and-materials services of $3,100 billed as delivered — cannot have passed through a period-end
deferred revenue balance in any material amount, and if the self-serve tier is recognized in the month billed the
figure is $13,400. The line labeled "revenue recognized from current-period billings" therefore includes amounts
billed and recognized in the same period that were never a contract liability. The schedule is a presentation
derived from the general ledger, not a record of the movement of a liability, and its line labels do not describe
what they appear to describe.

**(c) Opening balance recognized.** $54,900 ÷ $62,300 = 88.1%. The residual $7,400 (11.9%) of the opening balance
was still deferred at December 31, 2025, which is consistent with the $5,400 of noncurrent deferred revenue in the
opening balance sheet plus the ramped and multi-year population.

**(d) Billings is a plug.** Rearranging: closing $78,200 less opening $62,300 less acquired $610 plus FX $260 plus
revenue $148,200 = $163,750. Every figure on the right side of that equation comes from somewhere other than the
billing system: two balance sheets, the acquisition accounting, the translation adjustment, and the income
statement. The billings line can therefore be produced without opening Zuora, and if it were produced that way it
would carry no information about billing completeness at all. That is why the planned response to R-13 requires
Brightline to extract billings independently from Zuora Billing and reconcile the extract to $163,750, rather than
accepting the roll-forward. *If the independent extraction differs from $163,750 by more than the clearly trivial
threshold of $72*, the difference is one of three things — revenue recognized without a billing, a credit memo not
reflected, or a billing recorded outside the subscription system — and you resolve it by reconciling invoice-level
detail to the accounts receivable subledger for the months carrying the difference.

### Solution 2-2

1. **S, Ch, B; dominant S.** Subjectivity is acute because the estimate rests on 31 observations across a band
   with a 22% interquartile range. Change is present because the SKU launched in January 2025. Bias is present
   because the allocation moves revenue between Core and Insight and between periods. This is R-3, assessed High.
2. **S, U, C; dominant S.** The judgment is whether the stated 24-month term creates enforceable rights and
   obligations given a 30-day termination right, which is a legal-substance judgment (S) with an uncertain outcome
   (U) under guidance that is genuinely intricate (C). This is R-12, assessed Elevated.
3. **S, B; dominant B.** The bias is documented rather than inferred: the compensation committee recorded in July
   2025 that achievement was tracking behind plan, and management nonetheless assessed the tranche 100% probable
   in Q3. This is R-29, assessed High.
4. **S, B; dominant B.** The stage judgment is subjective, but the fingerprint is the pattern — retroactive
   restaging of 22% of hours, approved by the managers whose budgets benefit. This is R-26, assessed High.
5. **Ch, C; dominant Ch.** Note the trap: the abbreviated user acceptance testing is a *control* consideration,
   not an inherent risk factor. The inherent factor is that a mid-year reconfiguration of the ASC 606 engine
   changes how the model is applied to a population of ramped contracts. Recording "abbreviated UAT" in the
   inherent risk column is exactly the contamination Mistake 2.1 describes. This is R-4, assessed Elevated.
6. **S, U, C; dominant U.** The milestone is payable in Q1 2027, so the outcome is genuinely unknowable at the
   measurement date; the volatility and discount rate are subjective inputs; and the Monte Carlo technique with a
   payout cap is complex. Bias is a weaker factor here than inexperience. This is R-34, assessed High.

### Solution 2-3

1. **Control environment**, with a secondary bearing on the entity's risk assessment process. It identifies no
   control. It supports the inherent risk ratings on the judgmental estimates (R-3, R-23, R-29) and the control
   risk ratings on the close controls, and the control environment memorandum should cite those rows.
2. **Control activities.** It identifies a control relevant to the audit, and one that must be evaluated for the
   ICFR opinion whether or not Brightline relies on it. But as designed the control does not address 78.3% of the
   entries (3,847 ÷ 4,912), so it cannot support a control risk below maximum for that stratum. Design, not
   operation, is the defect.
3. **Monitoring.** Internal audit is a monitoring activity, and its existence and reporting line to the audit
   committee are relevant to the control environment as well. The readiness assessment is not evidence that
   controls operated — it is evidence about design readiness at a point in time — and using it as operating
   evidence is the error described in Chapter 1, Mistake 1.13. Its work may be used under AS 2605 or AU-C 610 only
   after evaluating competence and objectivity and re-performing some of it.
4. **Information and communication**, and **monitoring** through the reconciliation review. It identifies controls
   relevant to the audit. The FloQast sign-off dates are audit evidence, and the test is not whether a sign-off
   exists but whether it preceded the reporting date and whether the reviewer had the underlying reconciliation.
5. **Control activities** and **information and communication.** It identifies a control relevant to the audit —
   the Controller's review and approval of interface I-3 — which is an IT-dependent manual control. Its
   reliability depends entirely on the completeness and accuracy of the RevPro "Revenue Contract Summary," which
   is information produced by the entity, so testing the control without testing the report tests nothing.
6. **The entity's risk assessment process.** It identifies an absence rather than a control, and the absence is
   itself a deficiency in a component of internal control. Its consequence in the matrix is upward pressure on
   inherent risk wherever a new contractual term drives an accounting outcome — SLA credits (R-7), material
   rights (R-13), and termination-for-convenience clauses (R-12).

### Solution 2-4

**(a) Sequential growth.** Overage: $1,390 ÷ $1,090 − 1 = 27.52%. Core subscription: $28,200 ÷ $26,900 − 1 =
4.83%.

**(b) Expectation from the base growth rate.** $1,090 × 1.0483 = $1,143. Recorded $1,390 less $1,143 = **$247**
unexplained.

**(c) Expectation from the ratio trend.** Overage as a percentage of Core revenue: Q1 $780 ÷ $24,100 = 3.24%; Q2
$940 ÷ $25,700 = 3.66%; Q3 $1,090 ÷ $26,900 = 4.05%; Q4 $1,390 ÷ $28,200 = 4.93%. The quarterly increments are
+0.42, +0.39, and +0.88 percentage points. Applying the average of the first two increments (0.41 points) gives an
expected Q4 ratio of 4.46%, and 4.46% × $28,200 = $1,256. Recorded $1,390 less $1,256 = **$134** unexplained.

**(d) The range and its significance.** The unexplained difference is $134 to $247. The low end is 1.9 times the
clearly trivial threshold of $72, 14.3% of performance materiality, and 9.2% of overall materiality; the high end
is 3.4 times, 26.3%, and 17.0%. Both ends exceed the clearly trivial threshold, so the difference must be
investigated and cannot be written off; neither end approaches performance materiality, so the difference does not
by itself indicate a material misstatement. The second expectation is the better one because it uses four data
points rather than two and because it captures the genuine upward drift in consumption intensity that a
one-period growth comparison attributes entirely to Q4.

One further framing matters for the risk assessment. If the ratio drift is a measurement error rather than genuine
consumption growth, the exposure is not confined to Q4: applying the Q1 ratio of 3.24% to full-year Core revenue
of $104,900 produces expected full-year overage of $3,399 against recorded $4,200, a difference of $801, or 85.2%
of performance materiality. The full-year framing is what keeps this risk from being dismissed on magnitude, and
it is what Exercise 2-7 turns on.

### Solution 2-5

**(a) The aging foots.** $22,550 + $8,190 = $30,740; + $3,740 = $34,480; + $1,970 = $36,450; + $1,440 = $37,890;
+ $710 = **$38,600**.

**(b) Allowance implied by the stated loss rates.**

| Bucket | Balance | Rate | Product |
| --- | --- | --- | --- |
| Current | 22,550 | 0.4% | 90.2 |
| 1–30 days | 8,190 | 1.6% | 131.0 |
| 31–60 days | 3,740 | 6.0% | 224.4 |
| 61–90 days | 1,970 | 18.0% | 354.6 |
| 91–180 days | 1,440 | 42.0% | 604.8 |
| Over 180 days | 710 | 85.0% | 603.5 |
| **Total** | **38,600** | | **2,008.5** |

The components sum to $2,008.5, rounded to **$2,009**.

**(c) Comparison to the recorded balance.** Recorded $1,900 is $109 (5.4%) *below* the balance produced by
management's own historical loss rates applied to management's own aging. That comparison is the single most
useful number in the exercise, because CECL requires a reasonable-and-supportable forecast overlay to be applied
*on top of* historical experience, and the direction of the available forecast evidence is adverse: dollar-based
gross retention fell from 93% to 91% and Q4 DSO rose from 61 to 68 days. Management's balance is below the
historical starting point before any overlay is considered.

**(d) Coverage ratios.** FY2025: $1,900 ÷ $38,600 = 4.92%. FY2024: $1,350 ÷ $30,500 = 4.43%. Coverage rose 0.49
percentage points.

**(e) Position within the range.** ($1,900 − $1,780) ÷ ($2,410 − $1,780) = $120 ÷ $630 = the **19th percentile**.
Uncorrected misstatement U-2 of $240 implies an auditor point estimate of $2,140, which is ($2,140 − $1,780) ÷
$630 = the **57th percentile**.

**(f) Conclusion.** The arithmetic supports inherent risk High. Four things combine: the recorded balance is below
management's own bucket computation; it sits at the 19th percentile of a range whose width ($630) is 43% of
overall materiality; two specific exposures are inadequately covered, since Sundown Media's $980 at 94 days past
due attracts only $412 at the 42% rate and Meridian's disputed $1,240 sits in the current bucket attracting $5;
and the reasonably possible misstatement to the top of the range is $510, or 54.3% of performance materiality.

The best argument on the other side, and it is a real one: the coverage ratio *rose* year over year, the aging
composition is stable with 79.6% of the balance current or less than 31 days past due ($30,740 ÷ $38,600), and a
reasonably possible misstatement of $510 is a fraction of performance materiality rather than a multiple of it.
On magnitude alone, Elevated is defensible. The illustrated conclusion of High rests on subjectivity and bias
rather than on magnitude: the estimate is a range whose width is material, management has selected the optimistic
end of it, and management's incentive to do so is documented. What would move the assessment down: evidence that
the forward-looking overlay was quantified and documented before the balance was selected, and a roll-rate
analysis showing that the historical rates overstate current loss experience.

### Solution 2-6

**(a) Commission cost generated by the December 24–31 window.**

| Component | ACV | Rate | Commission |
| --- | --- | --- | --- |
| Contracts commencing on or before December 31, 2025 (26 order forms) | 4,910 | 11.8% | 579.4 |
| Contracts commencing on or after January 1, 2026 (92 order forms) | 20,264 | 11.8% | 2,391.2 |
| **Total (118 order forms)** | **25,174** | **11.8%** | **2,970.6** |

Rounded, **$2,971**, of which **$2,391** relates to contracts that will produce no FY2025 revenue whatever.

**(b) Capitalizable amount.** Employer payroll taxes at 6.2%: $2,970.6 × 6.2% = $184.2. Total capitalizable
$2,970.6 + $184.2 = **$3,155**.

**(c) FY2025 amortization on the 2025-commencing portion.** Capitalized amount $579.4 × 1.062 = $615.3, amortized
over 1,460 days with an average of 5.3 days elapsed: $615.3 × 5.3 ÷ 1,460 = **$2**. Effectively nil. The entire
$3,155 sits in accounts 1300 and 1305 at December 31, 2025 with $2 of FY2025 expense, and the offsetting credit
sits in accrued commissions (account 2105) until the January and February payroll runs.

**(d) Proportions.** $2,970.6 ÷ $4,800 = **61.9%** of accrued commissions; $2,970.6 ÷ $24,000 = **12.4%** of the
deferred contract acquisition cost asset. Two thirds of a balance sheet liability arising from six business days
of activity is the kind of concentration that determines where testing goes.

**(e) The reversal on the six uncorroborated contracts.** $1,780 × 11.8% = **$210** of commission, plus payroll
taxes of $210 × 6.2% = $13, for **$223** of capitalized cost and accrued liability to be reversed. Against overall
materiality of $1,450 that is 14.5% and 15.4% respectively; against the clearly trivial threshold of $72 it is
2.9 and 3.1 times, so it is well above the accumulation threshold and must be recorded on the summary of audit
differences.

Two cautions. First, the six contracts carry signature dates of December 1 to 12, 2025, not December 24 to 31, so
their commission is *additional* to the $2,971 computed in part (a), not a subset of it. Second, the income
statement effect of the reversal is close to nil because the amount was capitalized rather than expensed; the
effect is a $223 gross-up of both an asset and a liability. That makes the item easy for management to dismiss and
easy for an audit team to deprioritize. Its importance is not its income effect but its character: it is
corroboration, computed from an independent system, that the underlying revenue cut-off misstatement occurred.

### Solution 2-7

**Conclusion.** Retain inherent risk at Elevated and do not designate R-5 a significant risk. Likelihood is
genuinely elevated — the measured quantity originates on the AtlasFlow platform outside the ITGC boundary
Brightline scoped, recognition precedes billing because overage is invoiced in arrears, and the unexplained Q4
difference of $134 to $247 exceeds the clearly trivial threshold. Magnitude is what constrains the assessment. The
entire stream is $4,200. Even the full-year framing in Solution 2-4 — applying the Q1 consumption ratio of 3.24%
to Core revenue of $104,900 and comparing the resulting $3,399 to recorded overage of $4,200 — produces $801,
which is 85.2% of performance materiality and 55.2% of overall materiality. A significant risk requires inherent
risk close to the upper end of the spectrum on the combination of likelihood and magnitude, and the magnitude
ceiling here sits just under performance materiality on the most aggressive plausible framing.

**Range of defensible positions.** Elevated without designation (illustrated) through High with designation. High
without designation is the least coherent position, because if you believe the exposure reaches materiality you
have concluded the risk is at the upper end of the spectrum, which is the designation test.

**Evidence that would move the conclusion.** Any of the following moves it to High and probably to a significant
risk, because each extends the exposure beyond the $4,200 stream into the $131,600 Core and Insight base: the
per-1,000-run rate applied in Zuora is a management-maintained input rather than a value populated from the order
form; the committed volumes recorded in Zuora do not agree to the order forms, which would misstate the *included*
volume and therefore the subscription allocation; or platform run counts cannot be reconciled to Zuora usage
records for any month, which converts a measurement question into a question about whether the assertion can be
audited at all. Concentration is also a factor: contract C-1 Meridian alone consumed 44,000 runs above its
200,000 included volume, which at $12 per 1,000 runs is $528, or 12.6% of the entire overage stream, so a single
large-account error is material relative to the population.

**What would change in the program.** Designation would prohibit satisfying the risk with substantive analytical
procedures alone, prohibit reliance on prior-period control evidence, require evaluation and testing of the
controls addressing the risk, and require audit committee communication. Concretely, the program would move from a
substantive analytic plus recomputation for the 20 largest overage accounts to a full reconciliation of platform
run counts to Zuora usage records for all twelve months, recomputation for every account whose overage exceeds
$72, and a test of the contractual rate and committed volume in Zuora against the executed order form for a
defined stratum.

### Solution 2-8

Thirteen defects, grouped by the column that carries them.

**Row X-1, the risk statement.** (1) It is stated at the account level with no direction of misstatement, so no
procedure follows from it. (2) It combines at least three distinct risks — cut-off, allocation, and standalone
selling price — each with a different response; the correction is three rows, each completing the sentence
"[account] is over- or understated because [event], affecting the [assertion] assertion." (3) "Errors and
irregularities" is obsolete vocabulary that conflates error with fraud; name the risk and, separately, whether it
is a fraud risk.

**Row X-1, the assertions.** (4) "All assertions" is not an identification. Relevance is the operative concept:
an SSP risk affects accuracy and allocation, a cut-off risk affects occurrence and cut-off, and a completeness
risk affects a different account entirely. A row claiming all assertions directs testing at none of them.

**Row X-1, inherent risk.** (5) Listing all five inherent risk factors without rationale is equivalent to listing
none; each factor asserted must be supported by a fact. (6) The rationale is entirely about control deficiencies
and the absence of a prior ICFR audit. Inherent risk is assessed before consideration of controls; importing
control weaknesses into the inherent risk rationale is the contamination described in Mistake 2.1 and it makes the
significant risk determination meaningless.

**Row X-1, control risk.** (7) Control risk of Low is supported only by a description in management's SOX
narrative. An assessment below maximum requires tests of operating effectiveness; a narrative is a description of
design at best. (8) The row is internally contradictory: the inherent risk rationale asserts that ITGC
deficiencies affect all revenue applications, which is an argument for high control risk, and the control risk
column says Low.

**Row X-1, significant risk.** (9) The designation is derived from RMM. It must be derived from inherent risk
alone, on the combination of likelihood and magnitude.

**Row X-1, the response.** (10) A substantive analytical procedure alone cannot address a significant risk; the
standards require substantive procedures specifically responsive to it, and for a fraud-related cut-off risk that
means evidence from outside the entity. (11) The 10% variance threshold has no power: at AtlasFlow's scale,
monthly revenue averages $12,350, so a 10% threshold is $1,235 — 85% of overall materiality — and a misstatement
smaller than that passes undetected by construction. (12) Comparing to budget uses an expectation management
prepared, which is not an independent expectation.

**Row X-2.** (13) The risk statement has no mechanism and no direction, and Valuation alone omits existence and
accuracy, which are the assertions affected by capitalizing non-incremental costs. The inherent risk rationale is
a scoping argument based on a percentage of total assets and a firm threshold, not a risk rationale, and it
presents firm methodology as though it were an authoritative requirement. Control risk of Low has no stated basis
at all. And the response fails twice: reliance on the prior year's control testing is not available in an
integrated audit, where controls must be tested in the current period, nor for any significant risk; and a
roll-forward analytic on the balance is not responsive to the amortization-period risk, which is a question about
an estimate rather than about arithmetic. The row also carries no program or workpaper reference, so the linkage
between the risk and the procedure cannot be reviewed.

### Solution 2-9

**(a) The matrix row.**

| Ref | Risk — what could go wrong, and in which direction | Relevant assertions | IR factors | IR and rationale | CR | RMM | Significant risk? | Planned response |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| R-39 | A credit or discount usable only toward a future purchase is not identified as a material right, so no portion of the transaction price is allocated to it; revenue is overstated and deferred revenue understated over the term of the current contract, with the misstatement reversing only when the right is exercised or expires | Accuracy, allocation; completeness of deferred revenue; presentation and disclosure | C, S, Ch | **Elevated.** Complexity: identifying a material right requires distinguishing a discount that a customer could obtain without the existing contract from one that is incremental, and C-2 compounds it with EUR contracting, a GBP functional currency, and USD reporting. Subjectivity: the standalone selling price of the right depends on an estimated exercise probability, here 60%. Change: the Insight SKU that the credit applies to launched in January 2025, so the population of such credits is new. The identified population is 63 contracts with $1,940 of face value, and the completeness of that population depends on contract metadata in a company with no documented process for identifying new contractual terms | High | High | No | Extract the population of contracts containing future-purchase credits from the CPQ order form text and the Zuora amendment records, and prove completeness by reading 20 contracts selected from the general population rather than from the identified list; recompute the allocation for the 10 largest, including C-2; test the 60% exercise probability against actual FY2025 exercise experience; instruct Brightline UK LLP to test the EUR-to-GBP translation of C-2 (component performance materiality $380) |

**(b) The FY2025 revenue effect on C-2.** Relative standalone selling prices are $1,600 for the subscription and
$120 for the material right, a total of $1,720. Allocation of the $1,600 transaction price: subscription $1,600 ×
($1,600 ÷ $1,720) = $1,488; material right $1,600 × ($120 ÷ $1,720) = $112. The $112 stays in deferred revenue
until the credit is exercised or expires. FY2025 covers three of the 24 months: correct revenue is $1,488 × 3 ÷ 24
= $186, against $1,600 × 3 ÷ 24 = $200 if the right is ignored. **FY2025 revenue is overstated by $14 and deferred
revenue is understated by $112 on this contract alone.** Scaling by the ratio of allocated deferral to face value
($112 ÷ $200 = 56%) across the $1,940 population gives approximately $1,086 of deferred revenue that should exist
— 74.9% of overall materiality and 2.9 times component performance materiality — which is why the row belongs in
the matrix even though a single contract produces $14.

**(c) What would move the inherent risk rating.** Upward to High, and plausibly to a significant risk: evidence
that the identified population of 63 contracts is incomplete, since the identification depends on reading contract
text rather than on a data field, and the absence of a process for identifying new contractual terms is a
documented deficiency in the entity's risk assessment process; or evidence that the credits are usable against a
broader set of purchases than Insight, which would increase both the exercise probability and the estimated
standalone selling price. Downward to Moderate: evidence that the credits expire unexercised at a high historical
rate and that the population is genuinely limited to the 63 contracts, which would cap the exposure well below
materiality.

### Solution 2-10

Model language, 187 words:

```text
FRAUD DISCUSSION (AS 2110 / AS 2401)

The team discussed how a fraud might be perpetrated and concealed.  Incentive:
commissions are paid on booked ACV with above-quota accelerators; the CRO is
compensated on bookings and set December quarter-close incentives; the CEO's
compensation is weighted to ARR-based PSUs.  Pressure is asymmetric — AtlasFlow
reports a $21,400 net loss but $34,400 of operating cash flow, and the $40,000
minimum-liquidity covenant on the undrawn $50,000 revolver is not close to
binding against $96,400 of cash — so the pressure runs to growth measures, not
to solvency.  Opportunity: B. Hallowell can modify order-form dates in CPQ with
no review (Osei); D. Kim owns the RevPro configuration and is on a performance
plan (Haddad); NetSuite requires a second journal approver only above $250,000
(Nwosu).  Attitude: a first-time public-company CFO since September 2025 and a
thin close, discussed with reference to the July internal audit assessment
(Fong).  The discussion produced R-2, R-10, R-25, R-26, and R-29.  Considered
and rejected: revenue recognized on fictitious customers, because billing and
cash collection run through Zuora and the bank feed and the self-serve channel
is card-settled, making a fictitious customer uneconomic to sustain.
```

Note two features. The rejected risk is documented with its reason, which is what makes the discussion reviewable
— a memorandum that records only the risks identified cannot be distinguished from a memorandum written after the
programs were drafted. And the pressure analysis reaches a conclusion about *direction*: at AtlasFlow the
incentive is to overstate growth measures, not to overstate liquidity, which is why the response concentrates on
cut-off and estimates rather than on cash and covenant compliance.

### Solution 2-11

**(a) Mapping.**

| Ref | Applications affected | Matrix rows whose control risk it bears on | Mechanism |
| --- | --- | --- | --- |
| W-1 | Zuora Revenue only | R-1, R-4, R-14, R-16, R-38 | The RevPro configuration is the key control over revenue schedules; four unfederated administrator accounts, one shared among six people, means configuration changes cannot be attributed to an individual |
| W-2 | NetSuite only | R-10, and any control performed in NetSuite during the 27 days after go-live | Eleven users with legacy Full Access could post and approve entries; the population of entries they could have posted in the window is the exposure, and the response is to extract and examine entries posted by those 11 users in the window |
| W-3 | Salesforce, Zuora, NetSuite | R-1, R-4, R-9 directly; indirectly every IT-dependent control in those three applications | Access review is the monitoring layer that supports reliance on any access-dependent control; annual instead of quarterly review with the Q2 review 41 days late removed the foundation, which is what the November 21 reassessment records |
| W-5 | Salesforce | R-1, R-2 | A terminated employee with continuing CPQ access for over 30 days can create or amend an order form; this is an occurrence risk, not merely an access hygiene matter |
| W-6 | Zuora Revenue | R-1, R-4, R-14, R-16 | Standing developer write access to production configuration means the configuration control is not protected against unauthorized change, compounding W-1 |
| W-12 | NetSuite | R-10 | Not an ITGC; a business process control activity configured in an application |

**(b) Why the NetSuite SOC 1 does not mitigate W-2.** The report addresses controls at Oracle, the service
organization. Assigning roles within AtlasFlow's own NetSuite instance is a user entity responsibility and
appears in the report, if at all, as a complementary user entity control. A SOC 1 opinion on the service
organization's controls cannot provide evidence about the user entity's own administration of its role
assignments — and CUECs listed in AtlasFlow's SOC 1 reports were never mapped to AtlasFlow controls (W-10), so
even the CUEC route is unavailable.

**(c) Why W-12 is a design matter.** The control, as designed, applies only above $250,000. The 3,847 entries
below that threshold — 78.3% of the 4,912 manual entries — never enter the control's scope, so their absence of
review is not a failure of the control's operation but the intended consequence of its design. Testing more
entries produces evidence about the *account balance*; it can quantify misstatement and it can support a
substantive conclusion, but it cannot make the control effective, because the auditor's testing is not a control
of the entity. Remediation requires lowering the threshold or adding a compensating review of the sub-threshold
population, and the remediated control must then operate for a period sufficient to test before reliance is
available. For the financial statement audit the consequence is that control risk for manual entries is at
maximum from the strategy date, not as a result of a test failure.

**(d) W-12 is not an ITGC.** It is an application-configured business process control. The distinction matters in
two ways. An ITGC deficiency is evaluated for its *indirect* effect — you ask which automated and IT-dependent
controls relied on it and whether their reliability is impaired — whereas a business process control deficiency is
evaluated *directly* against the assertions the control was meant to address. And remediation timelines differ: an
ITGC remediated in November leaves ten weeks to the February 20 report date, which is generally too short to
support reliance in the current year, whereas a business process control that operates monthly may produce two
observations of a remediated design before the report date. Chapter 14 develops the severity analysis.

### Solution 2-12

**(a) The split.** $214,000 × 64.9% = $138,886, which rounds to the disclosed $138,900; conversely $138,900 ÷
$214,000 = 64.91%. The disclosure is internally consistent.

**(b) Unbilled contracted amount.** FY2025: $214,000 − $78,200 = **$135,800**. FY2024: $168,500 − $62,300 =
**$106,200**. Growth of 27.9%, against subscription revenue growth of 25.4% ($135,800 ÷ $108,300 − 1) and ARR
growth of 25.2% ($172,000 ÷ $137,400 − 1). The three growth rates are within 2.7 percentage points of each other,
which is the consistency you want to see.

**(c) RPO as a multiple of ARR.** FY2025: $214,000 ÷ $172,000 = **1.244 years**. FY2024: $168,500 ÷ $137,400 =
**1.226 years**. The multiple rose 1.5%, consistent with 34% of ACV sitting in multi-year contracts and no
material change in contract duration mix.

**(d) Why the twelve-month comparison looks alarming and is not.** Next-twelve-months RPO at December 31, 2025 of
$138,900 exceeds FY2025 subscription revenue of $135,800 by only 2.3%, which read naively implies that FY2026
subscription revenue will barely grow. The prior-year figure behaves identically: $110,100 against FY2024
subscription revenue of $108,300 is 1.7%. A ratio that is stable across two years is a feature of the measure, not
a warning about the business.

The reason is that next-twelve-months RPO is a floor on *contracted* subscription revenue, not a forecast. It
excludes usage overage of $4,200, which is variable consideration on a wholly unsatisfied performance obligation
or is excluded under a practical expedient; self-serve Core revenue of $6,100 across 11,400 monthly-billed
accounts whose original expected duration is one year or less; time-and-materials professional services of $3,100;
and every dollar of FY2026 new business and expansion, which in Q4 FY2025 alone was $61,400 of ACV. Removing the
excluded streams gives RPO-eligible FY2025 revenue of $148,200 − $4,200 − $6,100 − $3,100 = $134,800, of which the
opening next-twelve-months RPO of $110,100 covered 81.7%. Applying that same coverage ratio to the closing figure
implies FY2026 RPO-eligible revenue of $138,900 ÷ 0.817 = $170,053, or growth of 26.2% over $134,800 — which
reconciles to ARR growth of 25.2%. That is how the disclosure should be used in a substantive analytical procedure,
and it is why an analytic built on the raw twelve-month RPO figure produces a false positive every year.

**(e) The termination-for-convenience recomputation.** If the enforceable term of the 96 arrangements is 30 days,
their remaining performance obligation is the $310 within the notice window rather than the $8,400 of stated
remaining value. RPO becomes $214,000 − $8,400 + $310 = **$205,910**, a reduction of $8,090, or 3.8% of the
disclosed figure and **5.6 times overall materiality** of $1,450. The twelve-month portion becomes $138,900 −
$5,600 + $310 = **$133,610**, a reduction of $5,290, or 3.8% and 3.6 times materiality.

That is the point of the exercise. The contract-term judgment in R-12 reads like a technical footnote and it moves
a required ASC 606 disclosure by more than five times materiality. It is also why R-12 and R-16 must be linked in
the matrix: the response to R-12 has to quantify the RPO effect, and the response to R-16 cannot conclude on the
disclosure until R-12 is resolved. *If the identified population of 96 arrangements is incomplete* — which is the
likely failure, because it depends on contract metadata rather than on a read of the contracts — the reduction is
larger, and the next step is to read 20 contracts selected from the general population and estimate the
misidentification rate.

### Solution 2-13

**(a) Which risks require component-specific procedures.** The organizing principle is that shared systems make
most testing central. Australia transacts in the same Salesforce CPQ, Zuora, and NetSuite instances as the parent,
so any procedure whose population is a system extract is executed centrally and simply includes the Australian
records. A component-specific procedure is required only where the data, the judgment, or the counterparty is
local.

| Risk | Central or component-specific | Why |
| --- | --- | --- |
| R-1, R-2, R-4, R-13, R-16, R-21 | **Central** | The populations are extracts from single instances of CPQ, Zuora Billing, and Zuora Revenue. The 235 December order forms already include Australian order forms; DocuSign is a single tenant. No separate Australian procedure adds evidence |
| R-11 (multi-currency translation) | **Component-specific** | AUD is the functional currency; revenue of $12,500 and cash of $3,200 (account 1035) are translated at 0.6410 USD/AUD. Translation is performed in the consolidation workbook, which has no version control and four hard-keyed FX cells (W-8) |
| R-17 and R-18 (receivables and credit losses) | **Both** | The confirmation population is selected centrally from the consolidated subledger, but the collectability assessment for Australian customers requires local inquiry of the local collections owner and local knowledge of the customers affected by the office consolidation |
| R-25 (commission cut-off) | **Central** | Commissions are computed from the same CPQ ACV data and accrued in account 2105 at the parent |
| R-26 to R-28, R-29 to R-33, R-34 to R-38 | **Central** | Capitalized software, equity, and the Kestrel acquisition are recorded at the parent; Australia holds none of them |

Two exposures fall outside the seven areas the matrix in §2.12 covers and must be added to the instruction rather
than assumed: the Australian portion of the October 2025 restructuring charge, including the right-of-use asset
and lease consequences of the office consolidation, and the Australian goods-and-services tax accrual determined
by Avalara and recorded in account 2210. A specified-procedures instruction that reproduces only the matrix rows
will omit both. Australian payroll runs through Deel, whose SOC 1 is qualified as to one change-management control
objective and for which no bridge letter was obtained for October through December (W-9), so payroll expense for
the 38 Australian employees also requires a local procedure.

**(b) Component materiality.** $420 ÷ $1,450 = **29.0%** of overall materiality; $420 ÷ $12,500 = **3.4%** of
Australian revenue. Note the contrast with the UK component at $580, or 40% of overall materiality: the Australian
figure is lower in absolute terms and, as a percentage of component revenue, materially tighter than the UK's
$580 ÷ $26,300 = 2.2%. Compare those two before finalizing, because a specified-procedures component with a
tighter relative threshold than a full-scope component is usually a sign that one of the two was set mechanically.

**(c) Instruction paragraphs.**

```text
================================================================================
BRIGHTLINE LLP                                                    WP 1265-01
AtlasFlow, Inc. — FY2025 Integrated Audit
SPECIFIED PROCEDURES INSTRUCTION — AtlasFlow Pty Ltd (Australia)
Issued by:  G. Lindqvist (GL)          Date:  October 20, 2025
Component materiality $420; report any difference above $72 to the group team.

1.  CURRENCY TRANSLATION (risk R-11).  Obtain the AUD trial balance of AtlasFlow
    Pty Ltd at December 31, 2025 directly from NetSuite, not from the
    consolidation workbook.  Recompute the USD translation of revenue of $12,500
    at the average rate for each month and of cash of $3,200 (account 1035) at
    the December 31 closing rate of 0.6410 USD/AUD.  Agree the translated
    amounts to the FX translation tab of CONSOL_FY25_v14.xlsx and separately
    trace each of the four hard-keyed cells in that tab to source.  Report any
    difference above $72, and report every hard-keyed cell irrespective of
    amount.  An unexpected result here is a translated amount that agrees to the
    workbook but not to the recomputation, which indicates the workbook is the
    source rather than the record; if that occurs, extend to all AUD accounts.

2.  RECEIVABLES AND COLLECTABILITY (risks R-17, R-18).  For the 100% of
    Australian trade receivables at December 31, 2025 that exceed $72
    individually, obtain the aging directly from Zuora, agree it to the
    consolidated subledger, and inquire of the Australian collections owner as
    to each balance over 60 days past due.  Specifically identify any customer
    affected by the October 2025 office consolidation and document whether the
    account relationship was transferred, and to whom.  Report the aggregate
    balance you would reserve and your basis, for inclusion in the group team's
    independent range of $1,780 to $2,410.  An unexpected result is a customer
    whose account owner changed and who has stopped paying; if that occurs,
    obtain the last three months of correspondence.

3.  RESTRUCTURING AND LOCAL TAXES (outside the §2.12 matrix; see Chapters 10
    and 19).  Obtain management's computation of the Australian portion of the
    $1,900 October 2025 restructuring charge and the supporting termination
    schedule for the affected positions.  Recompute severance, unused leave, and
    any lease-exit consequence for the consolidated office, and confirm whether
    the right-of-use asset was tested for impairment.  Separately, obtain the
    Avalara GST determination reports for FY2025, recompute the accrual in
    account 2210 attributable to Australia, and agree it to the lodged returns.
    Report any difference above $72 and any charge recorded in a period other
    than October 2025.
================================================================================
```

## Review Questions

**RQ 2-1.** State the audit risk model and identify which of its terms the auditor controls.

**RQ 2-2.** Why is it wrong to write "audit risk is high for revenue occurrence"? What is the correct statement?

**RQ 2-3.** Name the five inherent risk factors defined in AU-C 315 as revised by SAS 145.

**RQ 2-4.** What two dimensions position an inherent risk on the spectrum of inherent risk?

**RQ 2-5.** Give the definition of a significant risk under AU-C 315 and state whether control risk enters the
determination.

**RQ 2-6.** List four consequences that follow from designating a risk as a significant risk.

**RQ 2-7.** Which two risks are effectively presumed to exist on every engagement, and what is the source of each
presumption?

**RQ 2-8.** Name the categories of risk assessment procedures the auditor is required to perform.

**RQ 2-9.** What must be documented about the engagement team discussion?

**RQ 2-10.** Name the five components of the system of internal control as described in AU-C 315 as revised.

**RQ 2-11.** Why do control environment deficiencies operate differently from deficiencies in the other four
components?

**RQ 2-12.** Distinguish a risk arising from the use of information technology from a general IT control, and give
one AtlasFlow example of each.

**RQ 2-13.** What is a control relevant to the audit, and how does the population of such controls differ between
a financial statement audit and an integrated audit?

**RQ 2-14.** What does the qualifier "relevant" add to the word "assertion," and why does the distinction change
the audit program?

**RQ 2-15.** Why can the completeness of deferred revenue not be tested from the deferred revenue subledger?

**RQ 2-16.** Explain why control risk for AtlasFlow's manual journal entry risk (R-10) is at maximum from the
strategy date rather than as a result of a failed test of controls.

**RQ 2-17.** What is the difference between a control deviation and a misstatement, and why does the distinction
matter when reporting the results of the December order form testing?

**RQ 2-18.** When is the auditor required to revise the risk assessment, and what should a reassessment log entry
contain?

**RQ 2-19.** State the most substantive difference between AU-C 315 and PCAOB AS 2110 as it affects the
documentation in this chapter, and how a PCAOB-engagement workpaper should describe the separate inherent and
control risk ratings.

**RQ 2-20.** Brightline did not designate revenue completeness a significant risk, and did not designate the
$170,600 convertible note carrying amount a significant risk. Give the reason in each case.

## Answers to Review Questions

**RQ 2-1.** Audit risk is a function of the risk of material misstatement and detection risk, and the risk of
material misstatement is a function of inherent risk and control risk: AR = (IR × CR) × DR. The auditor controls
only detection risk, and controls it through the nature, timing, and extent of further audit procedures. Inherent
risk and control risk are attributes of the entity that the auditor assesses but does not set; performing more
testing changes detection risk and never changes the risk of material misstatement.

**RQ 2-2.** Audit risk is an engagement-level concept — the risk that the auditor expresses an unmodified opinion
on materially misstated financial statements — and it is not assessed at the assertion level. What is assessed at
the assertion level is the risk of material misstatement. The correct statement is "the risk of material
misstatement for revenue occurrence is high."

**RQ 2-3.** Subjectivity, complexity, uncertainty, change, and susceptibility to misstatement due to management
bias or other fraud risk factors.

**RQ 2-4.** The likelihood of a misstatement occurring and the magnitude of the misstatement that could occur.
Both are required: a highly likely error in a small balance and a remote error in a large balance can both sit in
the lower middle of the spectrum, and only the combination places a risk at the upper end.

**RQ 2-5.** A significant risk is an identified risk of material misstatement for which the assessment of inherent
risk is close to the upper end of the spectrum of inherent risk because of the degree to which the inherent risk
factors affect the combination of the likelihood and the magnitude of a potential misstatement, or a risk that
another AU-C section requires to be treated as significant. Control risk does not enter the determination.
Effective controls change the response to a significant risk; they do not remove the designation.

**RQ 2-6.** Any four of: substantive procedures must be specifically responsive to the risk; reliance on
prior-period evidence about the controls addressing the risk is limited; the controls addressing the risk must be
evaluated and, in an integrated audit, tested; substantive analytical procedures alone are not sufficient; the
risk must be communicated to the audit committee; and the risk and the basis for the determination must be
documented.

**RQ 2-7.** Improper revenue recognition is presumed to be a fraud risk under AS 2401 and AU-C 240, and the risk
of management override of controls is treated as present on every engagement, which is why journal entry testing
and the examination of estimates for bias are required regardless of the assessed level of risk. At AtlasFlow the
first presumption produced R-2 and the second produced R-10.

**RQ 2-8.** Inquiry of management and others within the entity, including people outside the finance function;
analytical procedures; observation and inspection; and, in an integrated audit, walkthroughs of significant
transaction flows. Reading minutes, contracts, and other external and internal information, and considering
information obtained from the client acceptance and continuance process and from prior audits, are also required
inputs.

**RQ 2-9.** The discussion among the engagement team, including the significant decisions reached. In practice
that means the participants and their roles, the date, the facts each contributed, the risks identified, the
assertion-level conclusions reached, the risks considered and rejected together with the reason, and the changes
made to the audit programs as a result. A memorandum that records only the topics discussed does not discharge the
requirement.

**RQ 2-10.** The control environment; the entity's risk assessment process; the entity's process to monitor the
system of internal control; the information system and communication; and control activities.

**RQ 2-11.** Control environment deficiencies are pervasive. They raise the risk of material misstatement at the
financial statement level rather than at particular assertions, and they cannot be compensated for by a strong
process-level control, because the process-level control depends on the competence and integrity of the people
operating it. At AtlasFlow the finding that competence and capacity are thinnest in revenue accounting — where
inherent risk is highest — is the reason the FY2025 strategy contemplated an adverse ICFR opinion from September.

**RQ 2-12.** A risk arising from the use of IT is a way in which the entity's use of technology could cause a
financial statement misstatement; a general IT control is a control that addresses such a risk. At AtlasFlow the
risk that a change to any of the 27 Zuora Revenue configuration rules alters the revenue schedules for an entire
class of contracts (IT-1) is a risk arising from IT; a periodic review of privileged access to the Zuora Revenue
configuration would be the general IT control addressing it, and its absence — four non-federated administrator
accounts including one shared account (W-1) — is a missing control, not a risk.

**RQ 2-13.** A control relevant to the audit is one that addresses a risk of material misstatement at an assertion
the auditor has identified as relevant. In a financial statement audit the auditor need only identify and evaluate
the controls on which reliance is planned, plus those necessary to understand the flow of transactions. In an
integrated audit under AS 2201 the population expands to the controls over all relevant assertions of all
significant accounts and disclosures, whether or not the auditor intends to rely on them, which is why 1,370 of
AtlasFlow's 2,700 incremental FY2025 hours are control-testing hours.

**RQ 2-14.** "Relevant" limits the assertions to those that have a reasonable possibility of containing a
misstatement that would cause the financial statements to be materially misstated. Marking every assertion
relevant for every account produces a program that tests classification of the convertible note with the same
effort as occurrence of December revenue. Identifying relevance concentrates the work: AtlasFlow's revenue rows
carry occurrence, cut-off, accuracy, and allocation, and do not carry completeness as a significant risk, and the
program reflects that.

**RQ 2-15.** Understated deferred revenue means an obligation is missing from the subledger. A sample drawn from
the subledger cannot select an item that is not in it, so a subledger-based test provides evidence about existence
and accuracy and none about completeness. The test must run source-to-record: from a complete population of
executed contracts — for AtlasFlow, the 5,240 active Zuora Billing subscriptions, proved complete against the CPQ
"Closed Won" population — to the recorded liability.

**RQ 2-16.** REV-10 requires a second approver only above $250,000, so 3,847 of 4,912 FY2025 manual entries —
78.3% — fall outside the control's scope by design. There is nothing to rely on and nothing that a test of
operating effectiveness could establish, because the control operates exactly as designed and still does not
address the risk. Control risk is therefore at maximum from the strategy date, and the correct test is inspection
of the configuration rather than a sample of entries for approval evidence.

**RQ 2-17.** A control deviation is an instance in which a control did not operate as designed; a misstatement is
an amount recorded in the financial statements that differs from the amount required by the applicable framework.
In the December testing, the six contracts with uncorroborated signature dates produced a misstatement of $150
accumulated as U-3, while the eleven order forms whose Chief Revenue Officer discount approval postdated the
signature date produced control deviations in REV-01 with no misstatement, because in every case the discount
matched the executed order form. Reporting the eleven as misstatements would overstate the summary of audit
differences; reporting the six as deviations would omit them from it.

**RQ 2-18.** Whenever information obtained during the audit is inconsistent with the evidence on which the
original assessment was based — which in practice means whenever a test produces an unexpected result. The entry
should record the date, the trigger, the original assessment, the revised assessment, and the consequence, and the
consequence should be quantitative: hours added, population expanded from n to m, procedure added at a workpaper
reference, program revised to a stated version. AtlasFlow's log records revisions in both directions, including
the November 24 entry that reduced a control risk assessment and reduced a sample from 40 contracts to 25.

**RQ 2-19.** AU-C 315 as revised by SAS 145 requires inherent risk and control risk to be assessed separately at
the assertion level and requires control risk to be assessed at the maximum where the auditor does not plan to
test operating effectiveness; PCAOB standards require an assessment of the risk of material misstatement and
identify inherent and control risk as its components in AS 1101 without compelling two separately documented
ratings. On a PCAOB engagement the separate ratings should be described in the workpaper as firm methodology that
satisfies the AS 2110 documentation requirement, not as a professional requirement — presenting methodology as
authority is itself a documentation defect.

**RQ 2-20.** Revenue completeness was not designated because the incentives at AtlasFlow run toward overstatement,
subscription billing is system-generated from activated subscriptions, and deferred revenue growth of 25.5% tracks
subscription revenue growth of 25.4%, which is corroborative. The convertible notes were not designated because
none of the inherent risk factors is present: a single instrument, a 0.25% contractual coupon, effective-interest
amortization of $5,400 of issuance costs over five years, no separation of a conversion feature under ASU 2020-06,
and no incentive — magnitude of 117.7 times materiality notwithstanding. Both non-designations are documented,
because an assessment that records only what was included cannot show that anything was considered and rejected.

## Key Definitions

**Assertion.** A representation, explicit or implicit, embodied in the financial statements about the recognition,
measurement, presentation, or disclosure of an item. Assertions about classes of transactions include occurrence,
completeness, accuracy, cut-off, and classification; assertions about account balances include existence, rights
and obligations, completeness, and valuation and allocation; presentation and disclosure assertions concern
occurrence, rights and obligations, completeness, classification and understandability, and accuracy and
valuation.

**Audit risk.** The risk that the auditor expresses an inappropriate audit opinion when the financial statements
are materially misstated. It is an engagement-level concept, a function of the risk of material misstatement and
detection risk (PCAOB AS 1101), and it is not assessed at the assertion level.

**Control activities.** The component of the system of internal control comprising the controls that address risks
of material misstatement at the assertion level, including automated application controls, IT-dependent manual
controls, management review controls, and general IT controls.

**Control deviation.** An instance in which a control did not operate as designed, identified in a test of
controls. A control deviation is not a misstatement, and the two are accumulated and evaluated separately: a
deviation is evaluated for its effect on the control conclusion and on planned reliance, a misstatement for its
effect on the financial statements.

**Control environment.** The component of the system of internal control comprising governance and management
functions and the attitudes, awareness, and actions of those charged with governance and management concerning
internal control. Deficiencies in this component are pervasive: they affect the risk of material misstatement at
the financial statement level and cannot be compensated for by process-level controls.

**Control risk.** The risk that a misstatement that could occur in an assertion and that could be material will
not be prevented or detected on a timely basis by the entity's internal control. Under AU-C 315 as revised by
SAS 145, control risk is assessed at the maximum unless the auditor plans to test the operating effectiveness of
the relevant controls.

**Detection risk.** The risk that the procedures performed by the auditor will not detect a misstatement that
exists and that could be material. It is the only term in the audit risk model the auditor controls, and it is
controlled through the nature, timing, and extent of further audit procedures.

**Engagement team discussion.** The discussion among key engagement team members, required by AS 2110 and AU-C 315
and with a fraud-specific element required by AS 2401 and AU-C 240, concerning the susceptibility of the financial
statements to material misstatement. The significant decisions reached must be documented.

**Entity's risk assessment process.** The component of the system of internal control describing how the entity
identifies business risks relevant to financial reporting objectives, assesses their significance, and addresses
them, including the risk of fraud and the effects of change. Its output can be compared with the auditor's own
assessment, and a divergence is evidence about the component.

**Fraud risk.** A risk of material misstatement due to fraud, arising from fraudulent financial reporting or from
misappropriation of assets. Improper revenue recognition is a presumed fraud risk under AS 2401 and AU-C 240, and
a fraud risk is treated as a significant risk.

**General IT control (ITGC).** A control over the entity's IT processes that supports the continued proper
operation of the IT environment, including controls over access, program change, program development, and computer
operations. ITGCs do not directly address assertions; they support the reliability of the automated and
IT-dependent controls and the entity-produced reports that do.

**Information and communication.** The component of the system of internal control comprising the information
system relevant to financial reporting — how transactions are initiated, authorized, processed, recorded, and
reported, including the accounting records, the IT environment, and the financial reporting process — and how
roles, responsibilities, and significant matters are communicated.

**Information produced by the entity (IPE).** A report, extract, query result, or schedule generated by the entity
that the auditor uses as audit evidence or that a control operator uses in performing a control. Its completeness
and accuracy, including the parameters and logic used to produce it, must be tested; testing a control that relies
on untested IPE tests nothing.

**Inherent risk.** The susceptibility of an assertion to a misstatement that could be material, before
consideration of any related controls. It is a property of the transaction, balance, or disclosure, and it cannot
be reduced by the auditor or, in the ordinary case, by the entity's controls — it can only be responded to.

**Inherent risk factors.** The characteristics of events or conditions that affect the susceptibility of an
assertion to misstatement before consideration of controls. AU-C 315 as revised by SAS 145 names five:
subjectivity, complexity, uncertainty, change, and susceptibility to misstatement due to management bias or other
fraud risk factors.

**Management override.** The circumvention by management of controls that otherwise appear to be operating
effectively. Because management is in a position to override, the risk is treated as present on every engagement,
which is the source of the required journal entry testing, the required review of estimates for bias, and the
required evaluation of significant unusual transactions.

**Monitoring of the system of internal control.** The component describing how the entity evaluates the
effectiveness of controls and identifies and remediates deficiencies, including internal audit activity and
continuous-monitoring tools. Monitoring output is not evidence that a control operated; a readiness assessment
addresses design at a point in time.

**Relevant assertion.** An assertion that has a reasonable possibility of containing a misstatement that would
cause the financial statements to be materially misstated. The qualifier does real work: it excludes assertions
that cannot produce a material misstatement and thereby concentrates the audit program.

**Risk arising from the use of information technology.** A way in which the entity's use of technology could
result in a financial statement misstatement — for example, that inappropriate access permits an unauthorized
change to a revenue engine's configuration. It is a risk, not a control, and it is distinct from the general IT
control that addresses it.

**Risk assessment procedures.** The procedures performed to obtain an understanding of the entity, its
environment, the applicable financial reporting framework, and its system of internal control, and to identify and
assess risks of material misstatement. They comprise inquiry of management and others, analytical procedures,
observation and inspection, and — in an integrated audit — walkthroughs of significant transaction flows. They do
not by themselves provide sufficient appropriate evidence about an assertion.

**Risk of material misstatement (RMM).** The risk that the financial statements are materially misstated prior to
audit, assessed at the financial statement level and at the assertion level. At the assertion level it consists of
inherent risk and control risk. It is what the auditor assesses at the assertion level; audit risk is not.

**Significant account or disclosure.** An account or disclosure for which there is a reasonable possibility of
containing a misstatement that, individually or in combination with others, would have a material effect on the
financial statements, determined before consideration of the effect of controls (AS 2201). Size is one input;
composition, susceptibility, complexity, and the existence of related-party or non-routine transactions are
others.

**Significant risk.** Under AU-C 315, an identified risk of material misstatement for which the assessment of
inherent risk is close to the upper end of the spectrum of inherent risk because of the degree to which the
inherent risk factors affect the combination of the likelihood and magnitude of a potential misstatement, or a
risk another AU-C section requires to be treated as significant. Under PCAOB AS 2110, a risk of material
misstatement that requires special audit consideration. Control risk does not enter the determination.

**Spectrum of inherent risk.** The continuum along which an assessed inherent risk is placed, using the
combination of the likelihood and the magnitude of a potential misstatement. It is a defined concept in AU-C 315
as revised; PCAOB standards require evaluating likelihood and magnitude without using the term. The point of the
spectrum is that inherent risk is a position, not one of two or three boxes.

**Substantive procedure.** A procedure designed to detect material misstatements at the assertion level,
comprising tests of details and substantive analytical procedures. For a significant risk, substantive procedures
specifically responsive to that risk are required, and substantive analytical procedures alone are not sufficient.

**System of internal control.** The system designed, implemented, and maintained by those charged with governance,
management, and other personnel to provide reasonable assurance about the achievement of objectives with regard to
reliability of financial reporting, effectiveness and efficiency of operations, and compliance with laws and
regulations. AU-C 315 as revised describes it in five components.

**Test of controls.** A procedure designed to evaluate the operating effectiveness of a control in preventing or
detecting misstatements at the assertion level. It answers a different question from a substantive procedure, its
exceptions are control deviations rather than misstatements, and in an integrated audit it must be performed in
the current period for the controls addressing significant risks.

**Walkthrough.** A procedure in which the auditor traces a transaction from initiation through the accounting
records to the financial statements, making inquiries at each step of the person performing it, to obtain and
confirm an understanding of the flow of transactions and to identify the points at which a misstatement could
arise and the controls addressing them.

## Chapter Summary

1. Audit risk is engagement-level and detection risk is the auditor's only lever; the risk of material
   misstatement is a property of the entity that the auditor assesses but does not set, and no amount of testing
   reduces it.
2. Assessing inherent risk and control risk separately is required under AU-C 315 as revised by SAS 145 and is
   firm methodology rather than a professional requirement under PCAOB standards — but it is worth doing on either
   framework, because a blended rating cannot tell a reviewer whether the account is hard or the controls are
   broken, and the two conditions call for different responses.
3. Inherent risk is placed on a spectrum using the combination of likelihood and magnitude, driven by five
   factors — subjectivity, complexity, uncertainty, change, and susceptibility to management bias or other fraud
   risk factors. Magnitude alone does not place a risk at the upper end: AtlasFlow's $170,600 of convertible notes
   sit at the lower end and its $2,500 of contingent consideration sits at the upper end.
4. A significant risk is determined from inherent risk alone. Deriving it from the combined risk of material
   misstatement would have designated 34 of AtlasFlow's 38 risks significant, which is the same as designating
   none.
5. A risk statement that does not name the account, the assertion, and the direction of misstatement cannot
   generate a procedure. Merging R-1 and R-2 into "revenue cut-off" produces a test that cannot detect the risk
   that actually occurred, because a backdated order form is internally consistent with its own provisioning
   record.
6. The five components of the system of internal control are an input to the assessment, not a compliance
   deliverable: each component memorandum should end by naming the matrix rows it supports, and each matrix row
   should cite back.
7. A risk arising from the use of information technology is a risk; a general IT control is a control. Mapping
   nine IT risks to specific applications, controls, and assertions is what makes the control risk column
   defensible, and it is what prevents both of the available global errors — condemning every automated control
   because ITGCs are deficient, and accepting an unqualified SOC 1 as coverage for a period the report does not
   cover.
8. A completeness risk requires a population from outside the account being tested. Deferred revenue completeness
   at AtlasFlow is a significant risk precisely because it must be tested source-to-record from the 5,240 active
   Zuora subscriptions, and the roll-forward's $163,750 billings line is arithmetically derivable from the other
   five lines and therefore carries no independent information.
9. Size the risk on the account the event actually hits. The December 24–31 window carries $71 of FY2025 revenue
   and $2,971 of commission cost, which is 61.9% of the accrued commission balance; a team that scoped the risk on
   revenue would have tested five contracts and found nothing.
10. Reassessment is continuous and runs in both directions. Nothing about AtlasFlow's business changed between
    October 7 and December 19, 2025; what changed was the arrival of data, and the reassessment log must record
    not just the revised rating but the quantified consequence — 120 hours added, a population expanded from 60 to
    4,118, a sample reduced from 40 to 25.
11. Concentration is not the finding; the change in concentration is. Q4 bookings grew 30.9% year over year,
    which is in line with revenue growth and uninformative; the final-six-days share rose from 27% to 41% and the
    discount rate in that window rose 12.6 percentage points, and those are the numbers that changed the
    assessment.
12. When the risk is fabrication, the response must be evidence with a chain of custody outside the entity.
    Everything inside Salesforce CPQ, Zuora, and NetSuite is internally consistent with the fabrication; the
    DocuSign completion certificate is not, and field history — retained by Salesforce, NetSuite, and Zuora and
    extracted on almost no engagement — converted a population of 235 order forms into two strata of 40 testable
    in full and one stratum of 195 that could be sampled.
13. A quantitatively immaterial misstatement can drive the report. The $150 accumulated as U-3 is 10.3% of
    overall materiality and it produced a material weakness conclusion, because no control addresses the risk that
    an order form's execution date is misstated, a misstatement occurred, and management did not detect it.
14. Nine significant risks out of 38 is toward the high end of practice and is characteristic of a first-year
    integrated audit with an acquisition and a fraud allegation. They cluster in two places — revenue cut-off and
    override (R-1, R-2, R-10, R-13) and management estimates (R-3, R-18, R-26, R-29, R-34) — and that distribution
    should be recognizable at the start of the next subscription-business engagement.
15. Every response must be traceable to the row that generated it. Brightline carries the risk reference in the
    program step header, so that a reviewer can confirm that every risk has a response and every procedure has a
    reason; programs without that linkage cannot be reviewed for sufficiency.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| SaaS metric vocabulary, the bookings-to-cash bridge, the ARR waterfall, cohort analysis | Chapter 1, §1.5 | The business understanding this chapter converts into assertion-level risks; the metric-to-account pressure map is the source of the bias factor in 17 matrix rows |
| Scoping of the integrated audit and of the group audit, including the Australia decision | Chapter 1, §1.6–§1.7 | The boundary of what must be assessed, and the basis for Exercise 2-13 |
| Derivation of the $1,450 overall, $940 performance, and $72 clearly trivial thresholds | Chapter 3 | This chapter uses those amounts without deriving them; every magnitude judgment in the matrix depends on them |
| Principal versus agent and the reseller conclusions (R-6) | Chapter 4 | The substantive response to the gross-versus-net risk |
| Standalone selling price, contract modifications, contract term, and material rights (R-3, R-4, R-12) | Chapter 5 | The three revenue significant risks whose response is a technical accounting evaluation |
| Deferred revenue completeness and the RPO recomputation (R-13, R-14, R-16) | Chapter 6 | The source-to-record testing this chapter specifies but does not perform |
| Receivable confirmation, subsequent receipts, and the CECL allowance range (R-17 to R-21) | Chapter 7 | The independent expectation of $1,780 to $2,410 and the projection producing U-1 |
| Capitalized commissions and the four-year period of benefit (R-22 to R-25) | Chapter 8 | The retrospective analysis of average customer life and the renewal-commensurability test |
| Stock-based compensation, the PSU probability estimate, and the Kestrel valuation (R-29 to R-38) | Chapter 9 | The valuation specialist's work and the evaluation of estimate bias |
| Capitalized internal-use software and the restaged Jira epics (R-26 to R-28) | Chapter 10 | The independent stage assessment and the IPE testing of the time-tracking extract |
| ITGCs, SOC 1 reports, bridge letters, and CUECs | Chapter 11 | The control-side response to IT-1 through IT-9 |
| Application controls, IT-dependent manual controls, and information produced by the entity | Chapter 12 | Why R-28 exists as a separate risk and how the RevPro configuration is tested |
| Walkthroughs of significant transaction flows | Chapter 13 | The procedure that produced the understanding summarized in §2.10 |
| Severity evaluation of deficiencies, and the material weakness conclusion | Chapter 14 | The aggregation of W-1 through W-14 and the design deficiency identified in the case study |
| Sampling, reliability factors, and the arithmetic behind Exhibit 2-1 | Chapter 15 | The sample size mechanics this chapter uses illustratively |
| Journal entry testing and the consolidation top-side entries (R-10) | Chapter 16 | The scoring criteria applied to the 4,912 manual entries and the 27 top-side entries |
| Fraud risk assessment, the whistleblower allegation, and the AS 2401 procedures | Chapter 17 | The fraud subject matter this chapter integrates but does not own |
| Substantive analytical procedures at an evidential standard | Chapter 18 | The difference between the risk assessment analytics in §2.5 and a substantive analytic |
| Evaluation of misstatements, including U-1 through U-6 and qualitative factors | Chapter 19 | Where the $150 of U-3 and the $(460) aggregate are evaluated |
| The audit report, the adverse ICFR opinion, and critical audit matters | Chapter 20 | The reporting consequence of the significant risks identified here |

## Further Reading

- PCAOB AS 1101, *Audit Risk*, and AS 1105, *Audit Evidence*.
- PCAOB AS 2110, *Identifying and Assessing Risks of Material Misstatement*, together with AS 2101, *Audit
  Planning*, and AS 2301, *The Auditor's Responses to the Risks of Material Misstatement*.
- PCAOB AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of
  Financial Statements*, for the top-down risk-based approach, significant accounts and disclosures, and the
  identification of controls to test.
- PCAOB AS 2401, *Consideration of Fraud in a Financial Statement Audit*, for the fraud discussion, the revenue
  presumption, and the required procedures addressing management override.
- PCAOB AS 1215, *Audit Documentation*, and AS 1301, *Communications with Audit Committees*.
- PCAOB staff guidance and inspection observations addressing auditors' identification and assessment of risks of
  material misstatement and their responses to those risks, published in the Board's staff guidance and staff
  inspection publication series.
- AICPA AU-C 315, *Understanding the Entity and Its Environment and Assessing the Risks of Material Misstatement*,
  as amended by SAS 145 (effective for periods ending on or after December 15, 2023), with particular attention to
  the definitions of inherent risk factors, the spectrum of inherent risk, significant risk, risks arising from the
  use of IT, and general IT controls.
- AICPA AU-C 330, *Performing Audit Procedures in Response to Assessed Risks and Evaluating the Audit Evidence
  Obtained*; AU-C 240, *Consideration of Fraud in a Financial Statement Audit*; AU-C 402, *Audit Considerations
  Relating to an Entity Using a Service Organization*; and AU-C 230, *Audit Documentation*.
- The AICPA audit guides covering audit sampling, revenue recognition, and the use of data analytics in an audit,
  for the extent decisions in §2.13.
- COSO, *Internal Control — Integrated Framework* (2013), for the five components and the seventeen principles,
  and COSO's supplemental guidance on internal control over external financial reporting.
- FASB ASC 606, *Revenue from Contracts with Customers*, in particular the subtopics addressing identifying
  performance obligations, determining the transaction price, allocating the transaction price, contract
  modifications, and the disclosure of remaining performance obligations; and ASC 340-40, ASC 350-40, ASC 718,
  ASC 805, ASC 820, and ASC 326.
- SEC Division of Corporation Finance guidance on the exclusion of a recently acquired business from management's
  assessment of internal control over financial reporting, relevant to the Kestrel scope exclusion underlying
  R-34 through R-38.
- Institute of Internal Auditors, *International Professional Practices Framework*, for the evaluation of internal
  audit competence and objectivity referred to in Solution 2-3.






