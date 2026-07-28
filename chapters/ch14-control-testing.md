# Chapter 14 — Testing Controls and Evaluating Deficiencies

> A test of controls asks a narrow question — did this control operate as designed, throughout the period, with enough
> precision to matter — and the apparatus of nature, timing, extent, attributes, sample sizes, and deviation evaluation
> exists only to answer it defensibly. The harder half of the chapter begins after the answer is "no." A control that
> failed is a deficiency; a deficiency has a magnitude and a likelihood; a combination can be worse than the sum of its
> parts; and at some point on that continuum you stop describing findings and start writing an adverse opinion on
> internal control over financial reporting. AtlasFlow's FY2025 audit turns on where that point sits, because internal
> audit handed Brightline fourteen open information technology weaknesses and none of them, alone, is obviously a
> material weakness.

## Learning Objectives

- **LO 14.1** Distinguish the objective of a test of controls from that of a test of details.
- **LO 14.2** Design a test of a control by defining the population, proving its completeness, specifying the attributes,
  and stating what constitutes a deviation.
- **LO 14.3** Compute a sample size from control frequency and assessed risk and explain the statistical basis of the
  standard table.
- **LO 14.4** Design roll-forward procedures from an October 31 interim date to December 31 and compute the
  incremental extent.
- **LO 14.5** Evaluate benchmarking eligibility and conclude on the effect of an information technology general
  control (ITGC) failure on an automated control conclusion.
- **LO 14.6** Test a management review control, including a precision analysis comparing the investigation criteria to
  performance materiality.
- **LO 14.7** Test the completeness and accuracy of information produced by the entity (IPE) that a control consumes.
- **LO 14.8** Compute an upper deviation limit and conclude whether a deviation may be treated as isolated.
- **LO 14.9** Grade a deficiency on magnitude, likelihood, and the prudent official standard, aggregate deficiencies
  sharing a cause, and conclude on material weakness.
- **LO 14.10** Draft the deficiency communication an integrated audit requires and revise the substantive plan for a
  conclusion of "not effective."

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2201 | Testing operating effectiveness, evidence as of the as-of date, severity on magnitude and likelihood, the prudent official standard, the material weakness indicators, and the three deficiency definitions. |
| PCAOB | AS 2301 | Nature, timing, and extent of responses to assessed risk; interim testing; inquiry alone is not sufficient evidence of operating effectiveness. |
| PCAOB | AS 1105 | Reliability of evidence and evaluation of information produced by the entity. |
| PCAOB | AS 2315 | Sampling: population, tolerable rate, evaluation of deviations. |
| PCAOB | AS 1305 | Material weaknesses and significant deficiencies in writing to the audit committee before the report is issued; other deficiencies in writing to management. |
| PCAOB | AS 2401 | Journal entry testing and the risk of management override. |
| AICPA | AU-C 330 | Tests of controls and roll-forward for non-issuers; permits reliance on prior-audit evidence for unchanged controls tested at least every third audit, which AS 2201 does not. |
| AICPA | AU-C 265 | Written communication of significant deficiencies and material weaknesses no later than 60 days after the report release date. |
| AICPA | AU-C 315, AU-C 500, AU-C 530, AU-C 402 | Identifying controls (SAS 145 form effective for periods ending on or after December 15, 2021), evidence and IPE, sampling, service organizations. |
| SEC | Exchange Act Rule 13a-15; Item 308 of Regulation S-K | Management's ICFR assessment, disclosure controls, and disclosure of material weaknesses in Item 9A. |
| FASB | ASC 450-20 | Supplies "reasonable possibility" — probable or reasonably possible. |
| COSO | *Internal Control — Integrated Framework* (2013), Principles 10–12 and 16–17 | Control activities and monitoring, and the requirement to consider deficiencies in combination. |

AtlasFlow is an SEC issuer and FY2025 is its first integrated audit, so PCAOB standards govern. The frameworks diverge in
three ways: rotational reliance on prior-year testing, the communication deadline, and the existence of an opinion at all —
in a private-company audit a material weakness changes your substantive plan and your communication, but no one publishes a
grade.

## Prerequisites and Chapter Dependencies

Read Chapter 2 (identifying controls that address assessed risks), Chapter 3 (materiality — this chapter uses overall
materiality of $1,450, performance materiality of $940, and a clearly trivial threshold of $72), Chapters 11 and 12 (what
AtlasFlow's ITGCs and application controls are), and Chapter 13 (how a walkthrough shows that documented and performed
controls differ). This chapter supplies the mechanics and severity methodology that Chapter 19 applies in the final as-of
evaluation and Chapter 20 turns into report language.

## 14.1 What a test of controls is for

A test of controls obtains evidence about whether a control operated effectively throughout the period of intended
reliance; its sampling unit is an *occurrence of the control*, and its failure is a **deviation**. A test of details
detects misstatement in a recorded amount; its unit is a transaction, balance, or dollar, and its failure is a
**misstatement**.

**Exhibit 14-1. Test of controls compared with test of details.**

| Dimension | Test of controls | Test of details |
| --- | --- | --- |
| Population and unit | Occurrences of the control (12 monthly reviews; 250 daily clearances) | Recorded items or dollars ($38,600 of gross receivables) |
| Tolerable failure | Effectively zero for a key control at conventional sample sizes | Tolerable misstatement, tied to $940 performance materiality |
| Consequence of failure | The control cannot be relied on; a deficiency exists and must be graded | The item is accumulated on the summary of audit differences |
| What failure does **not** prove | That the financial statements are misstated | That any control is deficient |

The last row is the point. Brightline's December sample of order forms produced six contracts whose signature dates could
not be corroborated — six deviations, but only $150 of income effect (U-3), because those contracts started so late in
December that only days of revenue were at stake. Misstatement U-1, the $(185) projected cut-off error from the
receivable confirmation sample, arose where the control performed exactly as documented.

In the financial statement audit, testing controls is instrumental: it justifies lower assessed control risk and reduced
substantive extent. In the ICFR audit the conclusion is the product, because AS 2201 requires an opinion on effectiveness
*as of* December 31, 2025. So you test controls you would not otherwise rely on, and a control that worked for eleven
months and failed in December is worse for the ICFR opinion than for the financial statement audit, while one that failed
in February and was remediated in March is the reverse.

## 14.2 Nature, timing, and extent

**Nature** is which technique you use and whether you test the control directly. AS 2301 establishes that as assessed
risk rises the evidence must become more persuasive, which means moving from inquiry and observation toward inspection
and re-performance. **Timing** is when you test and what period the test covers (§14.6). **Extent** is how many
occurrences you examine (§14.5). The three trade against each other only within limits: twenty-five inquiries are the
same weak evidence twenty-five times, and extent cannot cure a late implementation date, because the occurrences do not
exist.

## 14.3 The four techniques and their evidential strength

**Exhibit 14-2. Testing techniques ranked by evidential strength.**

| Rank | Technique and AtlasFlow illustration | What it cannot establish |
| --- | --- | --- |
| 4 (weakest) | **Inquiry** — Jordan Pike states he clears every I-2 exception within one business day | That the control operated on any occasion, or throughout the period |
| 3 | **Observation** — watching the Billing Analyst work the I-1 queue on November 12, 2025 | Operation when you were not watching; anything about past occurrences |
| 2 | **Inspection** — the FloQast sign-off and variance report for the September I-3 journal | That the reviewer evaluated anything, where the artifact is a signature |
| 1 (strongest) | **Re-performance** — recomputing the December I-3 variance analysis from the RevPro summary | That the owner would reach that result unaided on different inputs |

**Inquiry alone is never sufficient to test operating effectiveness.** AS 2301 states the principle and AS 2201 repeats
it for ICFR. A workpaper reading "per discussion with R. Sandoval, access reviews are performed quarterly" is a note,
not a test — and at AtlasFlow it would also have been wrong, because inspection established annual reviews with the Q2
review 41 days late (W-3). **Corroborated inquiry is still inquiry.**

For most manual controls the working combination is inquiry (the criteria), inspection (operation on the selected
occurrences), and re-performance on a subset (competent operation). For a management review control, re-performance of
at least one occurrence is close to mandatory, because inspection cannot distinguish a review that examined the numbers
from one that examined the signature line.

## 14.4 Designing a test for a specific control

Four questions must be answered before you select an item. **Frequency**: not how often transactions occur but how often the
control operates. **Population and its proof**: completeness comes from an independent count — for a monthly control agree the
count to twelve and the amounts to the ledger; for a daily control derive the expected occurrences from the calendar (250 US
business days in 2025 after holidays) and reconcile to the system log. **Attribute**: "review evidenced" is not one; "the
approver's signature in FloQast is dated on or before the NetSuite posting date" is. **Deviation**: write it down first,
including what is *not* a deviation, or the definition drifts once testing begins.

**Exhibit 14-3. Control test design sheet — OTC-04, daily review and clearance of the I-1 error queue.**

| Field | Content |
| --- | --- |
| Control and owner | OTC-04; two Billing Analysts share the queue. Each business day the analyst reviews the Salesforce CPQ-to-Zuora Billing (I-1) error queue and records a disposition for every item |
| WCGW and assertions | An activated order creates no subscription record, so the customer is not billed; completeness and accuracy of subscription revenue (4100, 4110) |
| Type and frequency | IT-dependent manual, relying on the completeness of the queue report; daily — 250 business days |
| Population and proof | 250 clearance events covering 1,463 error items. Zuora error log extracted via API on January 8, 2026 with no date filter; 250 distinct dates present; 1,463 items agreed to the Zuora "Integration Error Summary" |
| Unit and extent | One business day's clearance; 40 dates (daily, higher risk — §14.5) |
| Attributes | (1) every item for that date has a recorded disposition; (2) dated no later than the next business day; (3) for items resolved by creating a subscription, the subscription exists and its start date equals the order-form service commencement date; (4) the recorder is one of the two authorized analysts |
| Deviation defined | Any item on a selected date failing attributes 1–4; a date with one failed item is one deviated sampling unit |
| Not a deviation | An item open beyond one business day because it was escalated to Zuora support, if the escalation is recorded by the next business day and the item is later resolved |

## 14.5 Extent: sample sizes for tests of controls

**Exhibit 14-4. Sample sizes for tests of controls by frequency and assessed risk (firm methodology).**

| Frequency | Occurrences | Lower risk | Higher risk | Coverage and upper deviation limit at the higher-risk size |
| --- | --- | --- | --- | --- |
| Annual | 1 | 1 | 1 | 100%; tested in full |
| Quarterly | 4 | 2 | 2 | 50%; evaluate qualitatively |
| Monthly | 12 | 2 | 5 | 41.7%; evaluate qualitatively |
| Weekly | 52 | 5 | 15 | 28.8%; 15.1% limit |
| Daily | 250 | 20 | 40 | 16.0%; 6.4% limit |
| Many times per day | 5,000+ | 25 | 60 | 1.2%; 4.9% limit at 95% one-sided confidence |
| Automated configuration | 1 state | 1 | 1 | Test of one, conditioned on effective ITGCs |

The endpoints of the "many times per day" row are not arbitrary. For a large population, an attribute sample
designed to accept zero deviations has size

```text
n = ln(1 - confidence) / ln(1 - tolerable deviation rate)
```

At 90% confidence and a 9% tolerable rate, n = ln(0.10)/ln(0.91) = (−2.3026)/(−0.0943) = 24.4, rounded to **25**. At
95% and 5%, n = ln(0.05)/ln(0.95) = (−2.9957)/(−0.0513) = 58.4, rounded to **60**. The two ends are one calculation at
two assurance-and-tolerance pairs. Reversing it gives the limit column: with zero deviations in 60 at 95%, the limit
is 1 − 0.05^(1/60) = 4.9%. For the daily population apply the finite-population correction n / (1 + n/N):
58.4 / (1 + 58.4/250) = 47.3, which firm methodology rounds down to 40 on the judgment that 16% coverage of a
homogeneous process supported by effective ITGCs suffices — a choice, not a derivation, and one to state in the
workpaper. The weekly and lower-frequency rows are conventions calibrated to hold the tolerable number of deviations at
zero, not statistical results; the correction applied to the weekly population would give 27.5, not 15.

**Neither the PCAOB nor the AICPA prescribes a sample size for a test of controls.** AS 2201, AS 2315, AU-C 330, and
AU-C 530 require sufficient appropriate evidence and stop there. Exhibit 14-4 is firm methodology. That matters when a
population has no row in the table — 27 RevPro configuration rules, 3,100 deployments, 96 terminations — and when a
reviewer challenges a sample of 25, because the defense is the confidence-and-tolerance pair it represents.

Three adjustments are routine and each must be documented: increase for a significant risk, as revenue is here; increase
where the control depends on deficient ITGCs (§14.10), which undermine the homogeneity assumption that lets 40 days speak
for 250; and decrease only for automated controls, only through benchmarking (§14.7).

## 14.6 Testing at an interim date and designing the roll-forward

Brightline performed its principal controls testing as of **October 31, 2025**, leaving 61 days and two close cycles to
December 31. AS 2301 permits interim testing, but the ICFR opinion speaks as of December 31, so evidence about the
remaining period is not optional. Brightline's proportional method computes the incremental extent as the full-period size
times the fraction of occurrences remaining, rounded up.

**Exhibit 14-5. Roll-forward plan from the October 31, 2025 interim date (item counts).**

| Control | Occurrences: year / to Oct 31 / after | Full-period extent | Interim | Roll-forward | Basis |
| --- | --- | --- | --- | --- | --- |
| OTC-04 I-1 error queue clearance (daily) | 250 / 208 / 42 | 40 | 33 | 7 | 40 × 42/250 = 6.7 |
| FIN-CLS-04 bank reconciliation review (monthly) | 12 / 10 / 2 | 5 | 4 | 1 | 5 × 2/12 = 0.8 (a) |
| ITGC-CM-01 change approval (many/day) | 3,100 / 2,570 / 530 | 60 | 50 | 10 | 60 × 530/3,100 = 10.3 |
| FIN-TRE-01 investment policy review (quarterly) | 4 / 3 / 1 | 3 | 2 | 1 | Q4 occurrence (b) |
| **Total items** | | **108** | **89** | **19** | |

Tick marks: (a) December rather than November, because the as-of date falls in December and Q4 close is the higher-risk
month. (b) The Q4 investment policy review occurs in mid-January 2026, after the as-of date. Obtain evidence that the
control existed and was designed to operate at December 31 and test the January occurrence as evidence of the process,
while recording that no Q4 occurrence exists to inspect at the as-of date — a design limitation, not something extent
cures.

Three failure modes recur. **Inquiry-only roll-forward** is defensible for a lower-risk unchanged control with no interim
deviations, not for one addressing a significant risk. **Ignoring a change in the performer**: the October restructuring
eliminated 41 positions, including (for this illustration) one of the two Billing Analysts on the I-1 queue, and the
post-change period is a *new* population — Brightline tested 15 of the 39 post-change clearance dates rather than the 7 the
proportional method gives. **Rolling forward a control that failed at interim**: there is nothing to roll forward, and the
next step is remediation and a fresh test (§14.14) or a conclusion of not effective.

## 14.7 Benchmarking automated controls

Benchmarking establishes that an automated control's configuration produced a correct result at a point in time and then,
in later periods, tests only that the configuration has not changed. It works because a purely automated control has no
performance variability.

**Exhibit 14-6. Benchmarking eligibility — the 27 Zuora Revenue (RevPro) configuration rules.**

| Condition | AtlasFlow assessment at December 31, 2025 |
| --- | --- |
| Entirely automated, no manual component | Met — the 27 rules execute without human intervention |
| A documented baseline test exists from a prior period | **Not met** — FY2025 is the first integrated audit |
| Program change controls are effective | **Not met** — W-4 (6 undocumented emergency changes), W-6 (standing production write access) |
| Logical access prevents unauthorized configuration change | **Not met** — W-1 (four local admins, `revpro_admin` held by six people) |
| The configuration did not change during the period | **Not met** — the February 2025 ramped-contract change, deployed with abbreviated user acceptance testing |

Four of the five conditions fail, so each assertion-relevant rule must be tested currently. Brightline
scoped 9 of the 27 rules as relevant to allocation and timing and re-performed each with three test cases — nominal,
boundary, exception — for 27 test cases, run against the December 31 configuration and repeated against the pre- and
post-February configurations for the three rules the February change touched. Benchmarking is never available in a
first-year integrated audit, which makes FY2025 the peak year for automated-control effort.

## 14.8 Management review controls: the hardest controls to test

A **management review control (MRC)** is one in which a person compares recorded information to an expectation and
investigates differences: flux reviews, reasonableness reviews of estimates, reviews of a reconciliation, and the review of a
journal before posting. They are hard to test because the only artifact is usually a signature, and a signature is silent
about what was compared and how large a difference would have prompted action.

**Exhibit 14-7. The five questions of a management review control test.**

| # | Question | An answer of the wrong shape |
| --- | --- | --- |
| 1 | What is the reviewer comparing to what, and is the expectation independent of the recorded amount? | "She compares it to the prior month" — a prior month carrying the same error is not independent |
| 2 | What is the criterion for investigation, and how does it compare to $940 performance materiality? | "Anything unusual," or a stated threshold above $940 |
| 3 | At what level of aggregation is the review performed? | Total revenue only — $700 in Core and $(700) in Insight net to zero |
| 4 | Is there evidence of what the review examined, not merely that it happened? | An electronic sign-off with no attachment |
| 5 | What happened to the items identified, and were any identified? | Zero items in twelve months on a population where you would expect some |

Question 2 is the precision analysis, and it separates a review that *could* detect a material misstatement from one
that could not. State it arithmetically: if the criterion is $1,000 per account line and performance materiality is
$940, a $999 single-line error passes by design and the control cannot be the sole control over that assertion.
Practice varies — some firms require the threshold at or below performance materiality, others accept performance
materiality divided by the number of independent line items reviewed. Say which you apply.

Question 5 most often produces the finding: a review that identified no items in twelve months, over a population where
the auditor's analytics found variances, either never triggers or is not operating.

Question 1 hides a SaaS trap. Revenue reviews at AtlasFlow are keyed to month-over-month change, but a subscription
business recognizes ratably, so a misstatement embedded in the beginning balance — a wrong standalone selling price
allocation applied consistently since January — produces *no* period-over-period variance. A change-based review is
structurally blind to a constant error; detecting it requires an independently derived expectation, such as revenue
computed from the subscription base and the contractual rate.

## 14.9 Testing the information produced by the entity that a control consumes

Nearly every MRC and most IT-dependent manual controls consume a report, and if the report is wrong the control cannot work
however diligently performed. AS 1105 requires you to evaluate the completeness and accuracy of information produced by the
entity (IPE) used as audit evidence, and the same logic applies to information the *entity* uses inside its own control: a
control that reconciles to an incomplete report reconciles to nothing.

**Exhibit 14-8. IPE completeness and accuracy test — RevPro "Revenue Contract Summary," September 2025.**

| Element | Procedure and result |
| --- | --- |
| Parameters observed | Observed Jordan Pike generate the report on November 14, 2025: period 2025-09; book US GAAP; entity ATLF-US; contract status Active and Closed; posting status Posted only |
| Completeness | 11,842 contract lines; an independent API query with the same filter returned 11,842 rows. Report revenue of $11,930 agreed to NetSuite 4100 ($9,100) + 4110 ($2,460) + 4120 ($370). Re-run with posting status All returned $11,930 plus $0 unposted, so the parameter excluded nothing |
| Accuracy | 10 lines selected; contract number, service start date, monthly recognizable amount, and remaining balance agreed to the Zuora Billing subscription record and the executed order form, 10 of 10. Recomputed the monthly amount as annual contract value ÷ 12 adjusted for mid-month starts; largest difference $0.4 |
| Dependency and conclusion | Depends on RevPro logical access (W-1) and configuration change controls (W-6), so the §14.10 exceptions apply. Complete and accurate as evidence and as an input to FIN-REV-03, subject to that qualification |

Two shortcuts to refuse: a screenshot emailed by the control owner, because you have not seen the parameters and the
parameter set is where a report goes wrong; and a Vanta dashboard tile stating that a control passed, which is a third
party's conclusion rather than evidence of operation.

## 14.10 The effect of ITGC failures on automated control conclusions

An automated control is a test of one because the computer does the same thing every time. That inference rests
entirely on ITGCs: change management makes "the same thing" stable, and logical access makes it *the* thing management
configured. When an ITGC fails, the inference fails. The error to avoid is mechanical inheritance — an ITGC deficiency
does not automatically make every dependent application control ineffective; it removes the *basis* for concluding
from one test that the control operated all period, and you must then ask what direct evidence remains.

**Exhibit 14-9. Effect of AtlasFlow ITGC deficiencies on dependent automated controls.**

| ITGC deficiency | Dependent controls | Effect on the automated conclusion | Brightline's incremental response |
| --- | --- | --- | --- |
| W-1 four local RevPro admins, `revpro_admin` shared among six | 9 in-scope RevPro allocation and timing rules | Configuration could have been changed by an unidentifiable person | Extract configuration change history for all 27 rules; re-perform the 9 rules at December 31 and at the pre- and post-February states (27 test cases) |
| W-4 6 of 3,100 deployments with no Jira ticket; 2 never documented | All Zuora, NetSuite, and RevPro automated controls | The population of changes is not demonstrably complete | Obtain the CI/CD deployment log independently; test the 6 for financial reporting impact |
| W-12 second approval only above $250,000 | Automated journal approval | The control does not exist below the threshold — a design, not operating, deficiency | 100% analytic scan of the 3,847 sub-threshold entries; targeted testing of 60 |
| W-2 11 users kept legacy Full Access 27 days after go-live | NetSuite segregation of duties | Restriction absent for 27 days | Test all entries posted by the 11 in the window (41 entries, $2,900) |

Three questions convert an ITGC deficiency into a scoping decision: *which* application controls it touches — a list, not
"everything IT"; whether it affects the whole period or a window, because 27 days is a far smaller exposure than a year; and
whether direct evidence exists independent of the general control, such as re-performance at the as-of date. Where it does,
the *application* control can be effective at December 31 while the ITGC remains a deficiency graded on its own.

## 14.11 Evaluating deviations

A **deviation** is a failure of the control; a **misstatement** is an error in the financial statements (§14.1). The first
question after a deviation is not "how big is it" but "what is the deviation rate, and what does it do to the conclusion."

At conventional sample sizes the tolerable number of deviations for a key control is zero, because the sample was
designed on that assumption. One deviation in 25 gives an observed rate of 4% and an upper deviation limit of roughly
13.4% at 90% one-sided confidence, against a 9% tolerable rate. The test fails arithmetically, which is why one
deviation in 25 usually ends the test: the sample cannot be rescued by inspecting the deviation more closely.

**Exhibit 14-10. Deviation evaluation.**

| Result | Upper deviation limit | Tolerable rate | Conclusion and next step |
| --- | --- | --- | --- |
| 0 of 25, 90% confidence | 8.8% | 9% | Effective; document coverage and the confidence-tolerance pair |
| 1 of 25, 90% confidence | 13.4% | 9% | Not effective at the planned assurance. Options: extend, treat as isolated (rarely), or conclude deficient |
| 2 of 5 monthly | Not meaningful; 40% observed | Zero | Not effective; a small population forecloses projection, so evaluate qualitatively |

Extending the sample is legitimate only if you decided in advance what result would satisfy you and the extension is
drawn from the same population. Extending because you did not like the first answer, then stopping when the answer
improves, is not sampling.

A deviation may be treated as **isolated** only when all of these hold: the cause is identified and specific to the
occurrence; the cause could not recur for other population items; the population can be redefined to exclude the
affected items and that redefined population is separately complete; and the excluded items are tested in full.
AtlasFlow supplies a genuine example and a false one. Genuine: an I-1 clearance date worked by a contractor whose Zuora role
was provisioned for one day during a November outage — one identifiable occurrence, a cause that cannot recur because the
role was removed, and Brightline tested that date in full. False: the late Q2 access review (W-3), which management
attributed to "the readiness project consuming the team's time" — a cause that applied to every review in the year.

## 14.12 From deviation to deficiency: severity

A **control deficiency** exists when a control is missing or fails to operate so that the objective is not met.
Severity is graded on two dimensions and one overlay.

**Magnitude** is the potential misstatement the deficiency could permit, not the misstatement that occurred. AS 2201 directs
you to the exposed account balance or transaction volume and the volume of activity subject to the deficiency. For W-12 the
exposed population is 3,847 manual journal entries with no independent review, whose gross absolute value dwarfs $1,450;
that a scan found only $180 of error does not reduce the magnitude, which is what could have passed.

**Likelihood** is whether the misstatement is *reasonably possible* — more than remote, borrowing ASC 450-20. This is a low
bar, and auditors habitually record likelihood as "unlikely" when they mean "we did not find it." Absence of detected
misstatement is weak evidence, because a deficient control means you cannot know what it let through.

**Exhibit 14-11. Severity grading grid.**

| | Magnitude: below $940 (PM) | Magnitude: $940 to $1,450 | Magnitude: at or above $1,450 |
| --- | --- | --- | --- |
| **Likelihood remote** | Deficiency | Deficiency | Deficiency; reconsider whether "remote" is defensible |
| **Likelihood reasonably possible** | Deficiency | Significant deficiency | **Material weakness** |
| **Likelihood probable** | Deficiency, but investigate whether a misstatement already exists | Significant deficiency | **Material weakness** |

The grid is a starting point, not the answer, because of the third element. The **prudent official standard** asks whether
a prudent official, knowing the same facts, would conclude the deficiency is a material weakness. It is a one-way ratchet:
it can raise a grade but never lower one. It matters most where the arithmetic is inconclusive and a qualitative feature is
decisive — a deficiency in an area management has publicly described as remediated, or one that lets the Controller both
prepare and post entries (W-13). One question operationalizes it: would you reach the same conclusion if the deficiency had
produced a $2,000 misstatement rather than none, given that the control's design is identical either way?

## 14.13 Aggregation, indicators, and compensating controls

Deficiencies are evaluated individually **and in combination** (AS 2201; COSO Principle 17). Two deficiencies aggregate
when a single misstatement could pass through both undetected — when they share an exposed population, a cause, or a
control objective. Six deficiencies in six unrelated processes do not aggregate merely by being numerous; six that leave
the same revenue stream unprotected do.

Aggregation follows three steps: cluster by shared cause or exposed population; compute each cluster's combined exposed
population once, rather than adding magnitudes across deficiencies that expose the same dollars; and ask whether the
*combination* removes protection that any single member left standing. That last step is where severity jumps, because
the compensating control you relied on for deficiency A is often impaired by deficiency B.

A **compensating control** mitigates severity only if it meets four conditions: it addresses the *same* relevant
assertion at the same or greater precision; it operates frequently enough to catch a misstatement before it becomes
material; **it has itself been tested and found effective**; and it is not impaired by the same or a related deficiency.
The fourth is where AtlasFlow's findings collapse most proposed mitigation: the Controller's review is offered as
compensating for weak journal-entry approval, but W-13 gives the Controller preparation, posting, and interface-mapping
access, so the reviewer is inside the risk.

AS 2201 lists indicators of a material weakness, each a presumption to overcome rather than a factor to weigh: fraud, whether
or not material, involving senior management; restatement to correct a material misstatement; identification by the auditor of
a material misstatement that management's controls would not have detected; and ineffective audit committee oversight.
AtlasFlow triggers the third squarely: Brightline identified the December cut-off misstatements underlying U-3, and the
documented order-validation control FIN-REV-07/OTC-05 did not exist (Chapter 13). The others are not present.

## 14.14 Remediation and testing remediated controls

Remediation is management's work, and your only question is whether the *new* control was in place and operating
effectively at December 31, 2025. Three tests: has the design changed so the original deficiency cannot recur; have
enough occurrences accumulated to test; and is that evidence sufficient given the assessed risk? The second is where
most late remediation fails, and the arithmetic is unforgiving.

**Exhibit 14-12. Sufficient-time analysis for remediation before December 31, 2025.**

| Deficiency and remediation | Implemented | Occurrences to Dec 31 | Extent needed | Sufficient? |
| --- | --- | --- | --- | --- |
| W-2 legacy Full Access role removed | Oct 6, 2025 | Configuration state; 3 monthly reviews | 1 state test + 3 | Yes — test the state and the three reviews |
| W-5 termination workflow automated in Okta | Nov 17, 2025 | 11 terminations | 11 (in full) | Yes for the post-change period; the year's 96 earlier terminations remain deficient |
| W-3 quarterly access review reinstated | Dec 1, 2025 | 1 review (December) | 2 quarterly minimum | **No** — one occurrence cannot support a quarterly conclusion |
| W-12 journal approval threshold lowered to $10,000 | Jan 5, 2026 | 0 | — | **No** — after the as-of date; irrelevant to the FY2025 opinion |

Two rules follow. A control implemented after the as-of date cannot support the opinion however good it is, though you
may describe it in the deficiency communication. And remediating part of the period does not cure the period: W-5's
automated workflow makes the control effective in December, but 96 terminations were processed at an average of 6.2 days
against a 24-hour SLA before that, and the financial statement audit covers the year even though the ICFR opinion speaks
as of December 31.

## 14.15 Feedback into substantive testing, and communication

A control conclusion of "not effective" is not merely a reporting event: control risk rises to maximum for the affected
assertions, and the substantive plan must absorb the difference within the same audit deadline.

**Exhibit 14-13. Substantive plan revisions driven by FY2025 control conclusions.**

| Control conclusion | Affected assertion | Planned procedure | Revised procedure |
| --- | --- | --- | --- |
| FIN-REV-03 I-3 journal review not effective (walkthrough) | Accuracy of subscription revenue | Test 25 revenue contracts; rely on the review for journal accuracy | Recompute the monthly RevPro-to-NetSuite journal for all 12 months from contract-level data — full recomputation, no sampling |
| Order-validation control does not exist (FIN-REV-07/OTC-05) | Cut-off and occurrence of revenue | Dual-purpose test of 40 orders | Test 100% of 218 contracts with a service commencement date in the last 10 days of December; extend to Q3; result: U-3 |
| W-12 sub-threshold entries unreviewed | All assertions; fraud risk | Journal entry analytics with 4 criteria | Add 3 criteria (round dollars, post-close entries by the Controller, entries to 2400 by preparers outside revenue); raise targeted selections from 40 to 60 |
| ITGC cluster not effective | Reliability of system-generated reports | Accept system reports as IPE with parameter observation | Test completeness and accuracy of every system report used as evidence (§14.9) |

Communication is mandatory and separately timed. Under AS 1305, material weaknesses and significant deficiencies must be
communicated in writing to the audit committee **before the auditor's report is issued**, and other deficiencies in writing to
management; AU-C 265 sets the non-issuer deadline at 60 days after the report release date. Three practical rules: the
communication states the grade, because "we observed" is not a grade; it is not conditional on management agreeing; and it
goes out even where management remediated during the period.

## Step-by-Step Walkthrough: Testing the Controller's Monthly Review of the RevPro-to-NetSuite Journal (FIN-REV-03, interface I-3)

**Control.** Each month the Controller (Elena Vasquez, CAO and Controller) reviews the Zuora Revenue–to–NetSuite summary
journal before it posts, agrees interface totals to the RevPro "Revenue Contract Summary," reviews the variance analysis
against her expectation, and approves the journal in FloQast. The journal posts to 4100, 4110, 4120, 2400, and 2410.
Workpaper: **WP 3200-14**.

**Step 1. Confirm what you are testing and why.** The risk addressed is inaccurate revenue and deferred revenue arising from
an interface mapping or configuration error. The control is IT-dependent and manual, is the only control between RevPro output
and the general ledger, and covers accuracy and cut-off of revenue and existence and valuation of deferred revenue. If the
control description does not state the criteria for investigation, that is your first finding, recorded now rather than at the
end.

**Step 2. Establish the frequency and define the population.** The control operates monthly, so 12 occurrences exist for
FY2025. Do not accept management's list. Query NetSuite for all journals with source `RevPro_Interface` and period
2025-01 through 2025-12, requesting `internalId`, `tranDate`, `postingPeriod`, `createdDate`, `createdBy`, `approvedBy`,
and `total`. Expect 12 rows.

**Step 3. Prove the population is complete.** The query returned **13** rows: twelve monthly journals plus a supplemental
September journal (`JE-2025-09-441`, $310) posted on October 8 to correct a mapping error found after the original
posting. The population is 13, not 12, and the thirteenth is the occurrence most exposed to the risk the control
addresses. Foot the 13 totals to interface-posted revenue and agree to ledger activity for 4100, 4110, and 4120.

**Step 4. Determine the extent.** Monthly, higher risk (revenue is a significant risk), so 5 of 13 from Exhibit 14-4:
February, May, July, September, and December. Documented rationale: February covers the ramped-contract configuration
change; September covers the corrected journal and the NetSuite upgrade; December is the as-of month and the
roll-forward occurrence (§14.6); May and July are random.

**Step 5. Specify the attributes before looking at anything.** (1) The FloQast approval is recorded by the Controller or
her documented delegate; (2) the approval date is on or before the NetSuite `createdDate`; (3) the journal total agrees
to the RevPro "Revenue Contract Summary" total for the period; (4) a variance analysis is attached showing the current
month, the expectation, and the variance by account; (5) every variance above the stated investigation criterion has a
documented explanation and, where applicable, a correcting entry.

**Step 6. Define a deviation and what is not one.** A deviation is any selected month failing any of attributes 1–5. Not
a deviation: an approval recorded on the same calendar day as posting but at a later timestamp, where the FloQast audit
log shows the approval preceded the posting event — timestamp, not date, governs. Not a deviation: a variance below the
criterion with no explanation, because the control does not require one.

**Step 7. Test the IPE the control consumes.** Perform the §14.9 procedure on the September "Revenue Contract Summary":
observe generation, record the parameters, reconcile the line count to an independent API extraction (11,842 = 11,842), and
agree $11,930 to 4100 + 4110 + 4120. If the report is incomplete, stop — the finding is then a design deficiency rather than
an operating one.

**Step 8. Obtain the criteria for investigation in writing.** Ask the Controller what variance would cause her to investigate
and corroborate the answer against the desk procedure and her behavior in the months tested. Her answer: any variance above
**$500** on any account line. The desk procedure says "material variances." Use the operative number for the precision
analysis and record that the documentation is imprecise.

**Step 9. Perform the precision analysis.** This step decides whether the control could detect a material misstatement.
The journal has five account lines subject to review. At a $500 threshold the maximum single-line misstatement that
passes undetected is $499, below performance materiality of $940, so the control is precise enough at the line level.
Across five independently reviewed lines the maximum aggregate undetected misstatement is 5 × $499 = **$2,495**, which
exceeds both $940 and overall materiality of $1,450.

**Exhibit 14-14. Precision analysis of the FIN-REV-03 review threshold.**

| Measure | Amount | Comparison |
| --- | --- | --- |
| Investigation threshold per account line | $500 | Stated by the owner; corroborated by behavior in 4 of 5 months tested |
| Maximum undetected single-line misstatement | $499 | Below performance materiality of $940 — adequate at the line level |
| Lines reviewed | 5 | 4100, 4110, 4120, 2400, 2410 |
| Maximum undetected aggregate misstatement | $2,495 | Exceeds performance materiality ($940) and overall materiality ($1,450) |
| Threshold under the PM ÷ lines convention | $188 | $940 ÷ 5; the operative threshold is 2.7× this |
| Smallest line's implicit precision (4120, $370 monthly) | 135% of the line | The review can never trigger on usage overage revenue |

Practice varies on the aggregate test: some firms require only that the threshold be below performance materiality at the
level the reviewer works, others apply the PM ÷ lines convention shown. State which you apply. Under either convention the
last row is fatal — a threshold larger than the account's monthly balance is not a control. Evidence that would
move the conclusion: a documented per-line percentage threshold (say 3% of the prior-month balance), or evidence that the
Controller in fact investigated variances well below $500.

**Step 10. Inspect the five selected months against the attribute grid.**

**Exhibit 14-15. WP 3200-14 attribute grid — FIN-REV-03, all sample rows.**

| # | Month | Journal ID | Total | A1 approver | A2 approval ≤ posting | A3 ties to RevPro | A4 variance analysis attached | A5 variances investigated | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Feb 2025 | JE-2025-02-118 | $10,940 | Y — E. Vasquez | **N** — approval 3/6, posted 3/5 (a) | Y | Y | Y | **Deviation** |
| 2 | May 2025 | JE-2025-05-206 | $11,310 | Y — E. Vasquez | Y — 6/4 ≤ 6/4 | Y | Y | Y | Pass |
| 3 | Jul 2025 | JE-2025-07-289 | $11,620 | Y — E. Vasquez | Y — 8/5 ≤ 8/6 | Y | Y | Y | Pass |
| 4 | Sep 2025 | JE-2025-09-352 | $11,930 | Y — E. Vasquez | Y — 10/6 ≤ 10/6 | Y (b) | Y | Y | Pass |
| 4a | Sep 2025 supplemental | JE-2025-09-441 | $310 | **N** — J. Pike (c) | **N** — no approval record | n/a | **N** — none | n/a | **Deviation** |
| 5 | Dec 2025 | JE-2025-12-503 | $12,410 | Y — E. Vasquez | Y — 1/7 ≤ 1/7 | Y | Y | **N** — $612 in 4110 unexplained (d) | **Deviation** |

Tick marks: (a) FloQast approval timestamp 2025-03-06 09:41; NetSuite `createdDate` 2025-03-05 18:22 — posted before
approved. (b) The September journal agreed to the Revenue Contract Summary only after the supplemental journal; the
original was $310 below the report while the variance analysis showed $0, so the reviewer did not perform attribute 3 as
documented. (c) Prepared and posted by the Revenue Manager with no independent approval, which W-13 permits. (d) Insight
revenue (4110) exceeded expectation by $612 against a $500 threshold, with no explanation and no correcting entry.

**Step 11. Re-perform one occurrence.** Take December. Recompute the variance analysis from the RevPro contract-level extract:
expected 4110 revenue of $2,566 (prior month $2,510 plus $56 of net new subscription value recognized ratably) against
recorded $3,178 — a $612 variance, agreeing to the client's own schedule. Trace it: three Insight contracts whose allocated
transaction price was loaded at list rate rather than the contractual discounted rate, a consequence of the February change.

**Step 12. Evaluate the deviations.** Three deviations across 5 tested months plus the supplemental journal. With a
population of 13 no upper deviation limit is meaningful, so evaluate qualitatively. The three are not variants of one
clerical slip: a sequencing failure, the absence of the control entirely on a journal correcting the very error the control
exists to catch, and a failure to investigate a variance above the owner's own threshold. Extending is pointless.

**Step 13. Consider whether any deviation is isolated.** None qualifies. The February sequencing failure recurs
structurally, since nothing prevents posting before approval; the September supplemental journal is not identifiable in
advance as a separate population, and W-13 permits the pattern in any month; and a precision failure applies to every
month.

**Step 14. Conclude, grade, and state the consequences.** The control was not effective at December 31, 2025 on two
independent grounds: precision (Exhibit 14-14) and operation (Exhibit 14-15). Magnitude: the exposed population is
interface-posted revenue of $135,800 and deferred revenue of $73,700; demonstrated error is $612 in one month and $310 in
another, and the maximum undetected aggregate misstatement is $2,495 per month against $1,450. Likelihood: reasonably
possible — demonstrated twice. Under Exhibit 14-11 this is at least a significant deficiency. Whether it is a material
weakness turns on the compensating control: Jordan Pike's monthly RevPro-to-GL reconciliation addresses the same assertion
and was tested effective, satisfying conditions one through three, but it is performed by the person who prepared the
unapproved September journal, so condition four fails. **Brightline's grade: significant deficiency, individually.** Chapter
19 evaluates whether it aggregates with the revenue cut-off material weakness (FIN-REV-07/OTC-05 plus U-3), which it
plausibly does. Consequences: control risk at maximum for revenue accuracy; full recomputation of all 12 monthly journals
from contract-level data (Exhibit 14-13); and written communication to the audit committee before the report is issued.

## Extended Case Study: Aggregating AtlasFlow's Fourteen ITGC Deficiencies into a Material Weakness

### Background

Internal audit's July 2025 readiness assessment, supplemented by Brightline's November testing, produced fourteen open
information technology weaknesses, W-1 through W-14. Management's memo of January 12, 2026 asserted that each was "a control
deficiency that does not rise to the level of a significant deficiency," because none had produced an identified
misstatement and each was scheduled for FY2026 remediation.

### The Facts

The fourteen weaknesses appear in the continuing case at §2.4 and are not restated. Four external facts bear on the grading.
First, WP 3200-14: the Controller's review of the I-3 journal — the control management offers as compensating for RevPro
configuration and interface accuracy — was not effective. Second, Brightline identified the December cut-off misstatements
underlying U-3 ($150) itself, management's controls did not detect them, and the documented order-validation control
FIN-REV-07/OTC-05 did not exist. Third, interface-posted revenue was $135,800 (4100 $104,900, 4110 $26,700, 4120 $4,200) and
deferred revenue $73,700 (2400 $66,800, 2410 $6,900). Fourth, of 4,912 manual journal entries, 3,847 fell below the $250,000
second-approver threshold, with gross absolute value of $412,600.

### What the Engagement Team Did

Brightline graded each weakness on magnitude and likelihood (§14.12), clustered by shared cause and exposed population
(§14.13), tested each proposed compensating control against the four conditions, and applied the prudent official standard
and the AS 2201 indicators to the clusters and to the whole.

**Exhibit 14-16. Individual severity grading of W-1 through W-14 (magnitudes in thousands).**

| Ref | Exposed population and magnitude | Likelihood | Grade |
| --- | --- | --- | --- |
| W-1 | All RevPro configuration: revenue $135,800, deferred $73,700. A change by any of six credential holders is untraceable | Reasonably possible — February proves configuration changes | **SD** |
| W-2 | 41 entries, $2,900 gross, posted by the 11 over-privileged users in the 27-day window | Reasonably possible; window and user set bounded | **D**, upper end (a) |
| W-3 | All three key systems, whole year; the detective control over W-1, W-2, W-5, and W-6 ran once, 41 days late | Annual frequency lets inappropriate access persist up to 12 months | **SD** |
| W-4 | 6 deployments, 2 never documented; the population of 3,100 changes is not demonstrably complete | An undocumented change to revenue logic would go undetected | **SD** |
| W-5 | 96 terminations averaging 6.2 days; 3 kept Salesforce access beyond 30 days, and Salesforce does not post to the ledger | Low; no post-termination activity for 2 of the 3, 4 read-only sessions for the third | **D** |
| W-6 | Same population as W-1; standing write access bypasses change approval | Reasonably possible | **SD** |
| W-7 | Stripe cash application through I-4; 2 unapproved code modifications | Reasonably possible | **D** (b) |
| W-8 | The entire consolidation — 3 entities, all accounts; no version control, no formula check, emailed among four | Formula error is the classic end-user computing failure | **SD**, upper end (c) |
| W-9 | Zuora and Deel for the 92-day gap period containing the as-of date | Reasonably possible | **D** |
| W-10 | AWS and Zuora CUECs unmapped; AtlasFlow cannot show it performs the controls the SOC 1 reports assume | Unmapped means unknown, and unknown is not remote | **SD** |
| W-11 | ARR and NRR in MD&A; the datamart does not post to the ledger, so financial statement magnitude is nil | Remote as to the statements | **D** in ICFR (d) |
| W-12 | 3,847 entries, $412,600 gross, with no independent review of any kind | Reasonably possible; override risk concentrates here | **SD**, top of range (e) |
| W-13 | All accounts. The Controller prepares, posts, alters the interface mapping, and is the FIN-REV-03 reviewer | Reasonably possible | **SD** |
| W-14 | No financial reporting accuracy exposure; the failed restore bears on availability | Remote | **D** |

Tick marks: (a) Brightline tested all 41 exposed entries and found no misstatement. That is evidence for the financial
statement audit and is **not** mitigation of severity — the auditor's own work is not a control (§14.13). The grade rests on
the bounded window and user set; a reviewer grading it a significant deficiency is within the range. (b) W-7 belongs to the
treasury and cash cluster, which Chapter 8 graded a significant deficiency in the aggregate. (c) A material weakness argument
is available, since the exposed population is the consolidated statements. Brightline resolved it downward because it
recomputed the consolidation for all three entities with $0 difference and because a monthly tie-out review of the workbook to
the entity trial balances was tested effective. (d) Not every ITGC deficiency has financial statement magnitude; say so rather
than inflating the schedule. (e) Standing alone W-12 is defensibly a material weakness. Brightline graded it a significant
deficiency because the scan of all 3,847 entries plus targeted testing of 60 found $180 of error, and because the aggregate
conclusion makes the distinction immaterial to the opinion.

### Analysis

**Exhibit 14-17. Aggregation by shared cause and shared exposed population.**

| Cluster | Members | Combined exposed population (counted once) | What the combination removes | Grade |
| --- | --- | --- | --- | --- |
| A — Access and accountability | W-1, W-2, W-3, W-5, W-6 | Revenue $135,800; deferred revenue $73,700; all NetSuite postings | Preventive access restriction *and* the detective review that would have caught its failure (W-3); no control remains at either layer | **MW** |
| B — Change management | W-4, W-6, W-7 | RevPro configuration governing allocation and timing for 11,842 contract lines | Approval before deployment and after-the-fact detection, since the change population itself is incomplete | **MW** |
| C — Journal entries and management override | W-12, W-13, W-1 | 3,847 entries, $412,600 gross, plus the interface mapping | Independent approval, segregation of preparer from poster, and traceability; the Controller is at once the only reviewer and an unconstrained preparer | **MW** |
| D — Monitoring and end-user computing | W-8, W-9, W-10, W-11, W-14 | Consolidated statements; service-organization gap period | Independent verification of information outside the core systems | **SD** |

Clusters A, B, and C are not independent problems. They share the same exposed dollars — interface-posted revenue and the
manual entries that adjust it — and each disables the mitigation the others would rely on. Two chains make this concrete.
**Chain one:** an unauthorized change to a RevPro allocation rule is possible (W-1, W-6), would not be approved or documented
(W-4), would not be detected by an access review that runs annually (W-3), and would not be caught by the only downstream
control, the I-3 review found ineffective on both precision and operation (WP 3200-14) — four layers, none standing. **Chain
two:** a manual entry below $250,000 requires no approval (W-12) and can be prepared and posted by the same person, who can
also alter the interface mapping and review the journal it produces (W-13).

Magnitude of the combination, counted once: revenue of $135,800 and manual entries of $412,600, either of which alone is
more than 90 times overall materiality of $1,450. Likelihood: reasonably possible and partly demonstrated — the February
configuration change produced the $612 December variance, and the September supplemental journal of $310 was a mapping error
that reached the ledger and was corrected without approval. AS 2201's third indicator is present. Prudent official: an
official told that revenue configuration can be changed by six people sharing one password, that the change would not be
documented, that the access review runs once a year, and that the only downstream review has a threshold larger than one of
the accounts it covers, would not call the combination merely a significant deficiency.

Management's two arguments fail. "No misstatement was identified" addresses neither magnitude, which is potential, nor
likelihood, which is a threshold rather than a finding — and it is factually wrong, since $310 reached the ledger.
"Remediation is scheduled for FY2026" is irrelevant to an opinion as of December 31, 2025 (§14.14).

### Resolution and Conclusion

W-1 through W-14 include no individual material weakness, but clusters A, B, and C aggregate to a single **material weakness
in information technology general controls over the revenue and financial reporting systems**, and cluster D is a
significant deficiency. That conclusion is separate from and additional to the revenue cut-off material weakness arising
from the non-existent order-validation control FIN-REV-07/OTC-05 and uncorrected misstatement U-3, and from the treasury and
cash significant deficiency established in Chapter 8. Two material weaknesses and two significant deficiencies were
communicated in writing to the audit committee on February 4, 2026 (AS 1305). Chapter 19 performs the final as-of
evaluation; Chapter 20 drafts the adverse ICFR opinion.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                          WP 3200-90
AtlasFlow, Inc. — FY2025 Integrated Audit                    Period: 12/31/2025
ICFR DEFICIENCY AGGREGATION AND SEVERITY CONCLUSION — ITGC

Prepared by:  M. Okafor, Senior            Date: 01/22/2026
Reviewed by:  D. Ferreira, Manager         Date: 01/26/2026
Reviewed by:  A. Whitfield, Partner        Date: 02/02/2026

PURPOSE
To grade individually and in combination the fourteen ITGC deficiencies identified in
FY2025 (W-1 to W-14) and conclude whether a material weakness exists as of 12/31/2025.

SOURCE OF INFORMATION
Internal Audit ICFR Readiness Assessment dated 07/18/2025; ITGC testing at WP 3100-10
through 3100-64; FIN-REV-03 test of controls at WP 3200-14; journal entry analytics at
WP 4400-20; management memo dated 01/12/2026.

PROCEDURES PERFORMED
1. Graded each of W-1 to W-14 on magnitude (exposed balance or transaction volume) and
   likelihood (reasonably possible per ASC 450-20), per AS 2201. See Exhibit A.
2. Clustered by shared cause and shared exposed population; computed each cluster's
   exposed population once to avoid double counting. See Exhibit B.
3. Tested each compensating control management proposed against the four conditions.
4. Applied the AS 2201 material weakness indicators and the prudent official standard.

RESULTS
- Individual grades: 8 significant deficiencies (W-1, W-3, W-4, W-6, W-8, W-10, W-12,
  W-13), 6 deficiencies (W-2, W-5, W-7, W-9, W-11, W-14), no individual material weakness.
- Compensating controls: FIN-REV-03 (Controller's I-3 journal review) FAILS conditions 1
  and 4 — maximum undetected aggregate misstatement of $2,495 per month exceeds overall
  materiality of $1,450, and the reviewer's access is the subject of W-13. Quarterly
  access review FAILS condition 3 (W-3). Monthly consolidation tie-out review MEETS all
  four conditions and mitigates W-8.
- Aggregate exposed population, counted once: revenue $135,800; deferred revenue
  $73,700; unreviewed manual entries $412,600. Materiality $1,450; PM $940.
- AS 2201 indicator present: auditor identified a material misstatement (U-3) that the
  entity's controls did not detect.

CONCLUSION
Clusters A (access), B (change management), and C (journal entries and management
override) aggregate to ONE MATERIAL WEAKNESS in ITGCs over the revenue and financial
reporting systems as of 12/31/2025. Cluster D (monitoring and end-user computing) is a
SIGNIFICANT DEFICIENCY. This is in addition to the revenue cut-off material weakness at
WP 3200-95 and the treasury and cash significant deficiency at WP 3600-40. ICFR is not
effective as of 12/31/2025. Communicated to the Audit Committee in writing 02/04/2026
(WP 1900-30). Final evaluation at WP 9100-10; report wording at WP 9500-20.
```

### Lessons

Grade every deficiency individually before you cluster, because the cluster argument is only as good as the magnitudes
underneath it, and a schedule padded with items that have no financial statement exposure (W-11, W-14) is easier to attack
than a shorter honest one. Aggregation is a causal argument, not a count: the sentence that carries the conclusion is "the
control we would have relied on to mitigate A is impaired by B." Never let your own testing mitigate severity, and test the
compensating control before accepting it.

## Common Mistakes

### Mistake 14.1 — Documenting inquiry as a test

**What it looks like.** "Per discussion with R. Sandoval, access reviews are performed quarterly; no exceptions noted,"
signed off as a test of operating effectiveness.
**Why it happens.** Inquiry is fast and the answer sounds like a conclusion.
**What goes wrong.** Inquiry alone is never sufficient (AS 2301), and here the answer was false: inspection showed annual
reviews with the Q2 review 41 days late (W-3).
**How to avoid it.** Name the technique for each attribute and show at least one inspected or re-performed occurrence.
Treat corroborated inquiry as inquiry.

### Mistake 14.2 — Accepting management's population

**What it looks like.** Selecting 5 of the 12 monthly journals from a list the Controller emailed.
**Why it happens.** The list is convenient and its count matches the expected frequency.
**What goes wrong.** The thirteenth journal — the September supplemental entry correcting a mapping error — is missing, and
it is the occurrence most likely to deviate. A test of an incomplete population supports no conclusion about the complete
one.
**How to avoid it.** Query the system with no filter beyond period and source, count the rows, and reconcile to the
general ledger before selecting anything.

### Mistake 14.3 — Confusing a deviation with a misstatement

**What it looks like.** "Six deviations, but the income effect is only $150, so the control is effective."
**Why it happens.** Both come out of sample testing and both get called "exceptions."
**What goes wrong.** The conclusions are independent. A 24% deviation rate makes the control unreliable regardless of
dollars, and a 0% rate coexisted with the $(185) projected misstatement U-1.
**How to avoid it.** Keep separate schedules — deviations on the test-of-controls workpaper, misstatements on the summary
of audit differences — and never let a dollar amount decide a control conclusion.

### Mistake 14.4 — Treating a deviation as isolated on management's explanation

**What it looks like.** "The late Q2 access review was caused by the readiness project consuming the team's time —
isolated; control otherwise effective."
**Why it happens.** The explanation is plausible and the alternative is a finding.
**What goes wrong.** The stated cause applied to every review in the year, so it proves recurrence rather than isolation.
**How to avoid it.** Write the four isolation conditions into the workpaper and answer them one at a time. If you cannot
redefine the population to exclude the cause, the deviation is not isolated.

### Mistake 14.5 — Inspecting the signature instead of the review

**What it looks like.** A management review control test whose only evidence is a FloQast sign-off screenshot and the note
"review evidenced."
**Why it happens.** The sign-off is the only artifact the system produces.
**What goes wrong.** The signature is silent on precision. September was signed off sitting $310 below the RevPro report,
and December carried a $612 unexplained variance above the reviewer's own $500 threshold. Both had valid signatures.
**How to avoid it.** Test what the reviewer compared, at what threshold, and what happened to the items found; re-perform
at least one occurrence from source data.

### Mistake 14.6 — Skipping the precision analysis

**What it looks like.** A review control concluded effective because the reviewer signed and investigated what she flagged,
with no comparison of her threshold to performance materiality.
**Why it happens.** Precision requires arithmetic and a stated convention, and the control "worked" on its own terms.
**What goes wrong.** A control that never triggers below $500 per line across five lines can pass $2,495, above overall
materiality of $1,450 — and a $500 threshold on account 4120, monthly balance $370, can never trigger.
**How to avoid it.** Compute the maximum undetected misstatement at the line level and in aggregate, compare both to $940
and $1,450, and state which convention you applied.

### Mistake 14.7 — Mechanically failing every control below a deficient ITGC

**What it looks like.** Concluding that all Zuora, NetSuite, and RevPro automated controls are ineffective because W-1,
W-4, and W-6 exist.
**Why it happens.** It feels conservative and saves the work of scoping.
**What goes wrong.** It overstates the finding, wastes the substantive budget, and obscures which controls actually lack
evidence. Re-performance at the as-of date can still support an effective conclusion.
**How to avoid it.** List the dependent controls, determine whether the exposure is a window or the year, and ask what
direct evidence exists independent of the general control.

### Mistake 14.8 — Rolling forward a control that failed at interim

**What it looks like.** A roll-forward workpaper adding 7 items to a daily control that deviated in the October interim
sample.
**Why it happens.** The roll-forward template is the same for every control and the interim result lives elsewhere.
**What goes wrong.** There is nothing to roll forward. Adding items either dilutes the deviation rate improperly or
produces an incoherent conclusion.
**How to avoid it.** Route a failed interim test one of two ways: test the remediated control over the post-remediation
population, or conclude not effective and grade the deficiency.

### Mistake 14.9 — Letting the auditor's own work mitigate severity

**What it looks like.** "We tested all 41 entries posted by the over-privileged users and found no misstatement, so W-2 is
only a deficiency."
**Why it happens.** The reasoning is intuitively appealing and the evidence is real.
**What goes wrong.** Severity is a property of the entity's controls. Your procedures are not a control and will not be
there next year; the same logic would let a thorough audit erase any material weakness.
**How to avoid it.** Grade severity on magnitude and likelihood before recording your substantive results, and state those
results separately as evidence for the financial statement audit.

### Mistake 14.10 — Counting deficiencies instead of tracing exposure

**What it looks like.** "Fourteen deficiencies is a lot, therefore a material weakness," or its mirror, "fourteen
deficiencies, none individually severe, therefore no material weakness."
**Why it happens.** Counting is easier than constructing the causal chain.
**What goes wrong.** Neither is supported. Fourteen unrelated deficiencies do not aggregate; three related ones over the
same revenue population do, because each disables the mitigation the others rely on.
**How to avoid it.** Write the chain in one sentence per cluster: the misstatement that could occur, the control that should
have prevented it, the control that should have detected it, and the deficiency that disabled each.

## Practice Exercises

### Exercise 14-1 [Foundational]

Compute the attribute sample size for a large population using `n = ln(1 − confidence) / ln(1 − tolerable rate)` at 95%
confidence and a 7% tolerable rate, accepting zero deviations, then state the upper deviation limit if you find zero
deviations.

### Exercise 14-2 [Foundational]

Rank these from strongest to weakest evidence of operating effectiveness and state what each cannot establish: (i)
observing the Billing Analyst clear the I-1 queue on November 12; (ii) recomputing the December I-3 variance analysis
from the RevPro extract; (iii) asking Jordan Pike whether exceptions are cleared daily; (iv) inspecting the FloQast
sign-off for the September journal.

### Exercise 14-3 [Foundational]

A weekly control operated 52 times, 43 of them on or before the October 31 interim date, and the full-period extent is
15. Compute the roll-forward extent under the proportional method, then recompute assuming the performer changed on
November 3 and methodology requires 15 selections from any post-change population.

### Exercise 14-4 [Intermediate]

You tested 40 occurrences of a daily control and found 1 deviation. Using a 90% one-sided Poisson factor of 3.89, compute
the upper deviation limit, compare it to a 5% tolerable rate, and state whether extending to 80 with no further
deviations would rescue the test.

### Exercise 14-5 [Intermediate]

A monthly reviewer investigates any variance above $1,200 on any of six independently reviewed account lines. Overall
materiality is $1,450, performance materiality $940, and the smallest line's monthly balance $840. Compute the maximum
undetected single-line and aggregate misstatements and the threshold the PM ÷ lines convention requires, and conclude on
precision.

### Exercise 14-6 [Intermediate]

An automated three-way-match control was baselined in FY2024 with a documented test. In FY2025 the configuration did not
change and change management was tested effective, but two developers have standing production write access. State
whether benchmarking is available and what you would do instead.

### Exercise 14-7 [Intermediate]

Find at least five defects in this extract: "Control: monthly bank reconciliation review (FIN-CLS-04). Population: 12
reviews per client-provided list. Extent: 2 (monthly, higher risk). Attribute: review evidenced. Results: 2 of 2 signed.
One review signed 9 days after the close was completed; per Controller, the reviewer was on vacation — isolated.
Conclusion: control effective."

### Exercise 14-8 [Intermediate]

In a sample of 25 change approvals you find one deployment with no approval. Management states it was pushed during a
November 8 AWS incident by an on-call engineer whose emergency access was granted and revoked that day, and that the
incident log identifies four such deployments. May the deviation be treated as isolated, and what further work is
required?

### Exercise 14-9 [Advanced]

A deficiency exposes accounts totaling $3,900 and the misstatement it could permit is reasonably possible. Management
offers as compensating a quarterly review with a $700 investigation threshold, tested and found effective, performed by
the person whose access created the deficiency. Grade the deficiency, testing all four conditions.

### Exercise 14-10 [Advanced]

Draft the paragraph (100–150 words) Brightline would include in its written communication to the audit committee
describing the aggregated ITGC material weakness: the grade, the deficiencies aggregated, the exposed population, and why
the combination is more severe than its parts.

### Exercise 14-11 [Advanced]

Draft a control test design sheet — population, proof of completeness, extent, three attributes, and the definition of a
deviation — for ITGC-LA-01, provisioning of new user access, which operated 168 times in FY2025 and is assessed higher
risk.

### Exercise 14-12 [Advanced]

Spanning Chapter 3. Suppose overall materiality had been $2,100 and performance materiality $1,365 (a hypothetical
variation). Re-examine the FIN-REV-03 precision analysis and the aggregate ITGC grading, and state which conclusion
changes, which does not, and why.

## Solutions to Practice Exercises

### Solution 14-1

n = ln(0.05) / ln(0.93) = (−2.9957) / (−0.07257) = 41.3, rounded up to **42**. With zero deviations in 42 at 95%
confidence the upper deviation limit is 1 − 0.05^(1/42) = **6.8%**, below the 7% tolerable rate — arithmetic
confirmation that the sample was designed correctly. Rounding down to 41 gives 6.96%, inside tolerance but with no
margin.

### Solution 14-2

Strongest to weakest: (ii) re-performance, (iv) inspection, (i) observation, (iii) inquiry. Re-performance cannot
establish that the owner would reach the same result unaided on other inputs. Inspection cannot establish that the
reviewer evaluated anything where the artifact is a signature. Observation says nothing about occasions you did not
watch or about the past. Inquiry says nothing about operation at all and is never sufficient alone (AS 2301).

### Solution 14-3

Remaining occurrences = 52 − 43 = 9. Proportional extent = 15 × 9/52 = 2.6, rounded up to **3**. With a performer change
on November 3, the post-change occurrences form a separate population — about 8 weekly occurrences to December 31 —
and methodology calling for 15 selections cannot be satisfied. Test all 8 and state the limitation: the post-change
conclusion rests on 8 occurrences, and one deviation makes the control ineffective at the as-of date.

### Solution 14-4

Upper deviation limit = 3.89 / 40 = **9.7%**, nearly double the 5% tolerable rate, so the test fails. Extending to 80
with no further deviations gives 3.89 / 80 = **4.9%**, marginally inside 5%. Arithmetically the extension rescues the
test, but only if it was planned in advance, drawn from the same population, and the deviation's cause does not itself
indicate a design problem. Extending after an unfavorable result and stopping when the number improves is not
sampling.

### Solution 14-5

Maximum undetected single-line misstatement = $1,199, which **exceeds** performance materiality of $940, so the control
fails at the line level before aggregation arises. Maximum aggregate = 6 × $1,199 = **$7,194**, 4.96 times overall
materiality. The PM ÷ lines convention would require $940 ÷ 6 = **$157**. The threshold also exceeds the smallest
line's balance of $840, so the review can never trigger there. The control cannot be the sole control over these
assertions, and no aggregation convention is needed to say so.

### Solution 14-6

Benchmarking is **not available**. All conditions must hold, and effective logical access is one: standing production write
access means the configuration could have been altered without passing through the change process, so the baseline no longer
proves the current state. Re-perform the match logic against the December configuration with nominal, boundary, and exception
cases, extract the year's configuration change history, and grade the access finding separately.

### Solution 14-7

At least five defects. (1) The population is management's list, not independently derived. (2) Extent of 2 is the lower-risk
column; higher risk requires 5. (3) "Review evidenced" is not an attribute — it specifies neither who, when, nor against
what. (4) The 9-day-late review is treated as a pass; if timeliness is a control requirement it is a deviation, and if not,
the attribute should have said so. (5) Isolation is asserted on a recurring cause. (6) December, the as-of month, was not
selected. (7) No deviation definition and no IPE testing of the bank statement.

### Solution 14-8

**Not isolated on these facts, though potentially isolatable.** The cause is identified and the emergency access was revoked,
which speaks to non-recurrence, but the incident log identifies four such deployments, so the affected items are a set of
four. Required work: confirm from the CI/CD deployment log, not the incident log, that exactly four used emergency access;
test all four for financial reporting impact and after-the-fact documentation; and conclude separately on the redefined
population of 3,096 normal-process changes. Because W-4 establishes 6 undocumented emergency changes, the "cannot recur"
condition is doubtful and the conservative answer treats the deviation as a deviation.

### Solution 14-9

Condition 1 (same assertion, adequate precision): met, since $700 is below performance materiality of $940. Condition 2
(frequency): quarterly is marginal where the misstatement must be caught within the period. Condition 3 (tested effective):
met. Condition 4 (not impaired): **failed** — the reviewer is the person whose access created the deficiency. With $3,900 of
exposure (2.7 times overall materiality), reasonably possible likelihood, and no effective compensating control, this is a
**material weakness**. Concluding significant deficiency would require a different compensating control performed by someone
else.

### Solution 14-10

Model language: "We identified a material weakness in internal control over financial reporting relating to
information technology general controls over the Company's revenue and financial reporting systems as of December
31, 2025. Individually, the deficiencies we identified in logical access (including four local administrator
accounts in Zuora Revenue and a shared administrative credential available to six individuals), in the frequency of
user access reviews, in change management (including six production deployments made without documented approval),
and in the segregation of journal entry preparation from posting and approval, were significant deficiencies. In
combination they are a material weakness, because the preventive controls over the revenue configuration, the
detective access review that would identify their failure, and the Controller's review of the revenue interface
journal on which management relies were each ineffective during the period. The deficiencies expose interface-posted
revenue of $135.8 million and $412.6 million of manual journal entries recorded without independent approval."

### Solution 14-11

**Control and frequency:** ITGC-LA-01, provisioning of new or modified user access in Okta following documented approval; 168
occurrences, as-occurring. **Population and proof:** extract all Okta access grants for the year from the system log with no
filter beyond date; reconcile the count to the Jira access-request queue and the HR new hire and transfer report (all three
should agree at 168, and a difference is itself a finding, because a grant with no request is unauthorized). **Extent:** 40
(higher risk, treating the population as daily-equivalent). **Attributes:** (1) a Jira request exists and predates the grant;
(2) the approver is the system's data owner and is not the requester; (3) the entitlements granted match those requested.
**Deviation:** any grant failing attributes 1–3. **Not a deviation:** a grant recorded up to one business day before the Jira
approval timestamp where an approval email predates it and is attached to the ticket.

### Solution 14-12

The **precision conclusion changes in part; the grading does not**. At performance materiality of $1,365 the maximum
undetected single-line misstatement of $499 remains well below it, and the aggregate $2,495 still exceeds both $1,365 and
overall materiality of $2,100, though by a smaller margin (1.19 times rather than 1.72). The PM ÷ lines threshold rises from
$188 to $273, still below the operative $500. The finding that $500 exceeds the $370 monthly balance of account 4120 is
unaffected. The aggregate ITGC conclusion is insensitive: $135,800 and $412,600 are 65 and 197 times $2,100. Magnitude
conclusions resting on order-of-magnitude differences are robust to materiality; precision conclusions resting on ratios
near one are not.

## Review Questions

**RQ 14-1.** State the sampling unit and the meaning of failure in a test of controls, and contrast both with a test
of details.

**RQ 14-2.** Why does the ICFR audit require testing controls that the financial statement audit alone would not
require you to test?

**RQ 14-3.** What does "inquiry alone is never sufficient" mean in practice, and does corroborating an inquiry with a
second person change the answer?

**RQ 14-4.** Name the four questions that must be answered before selecting the first item in a test of controls.

**RQ 14-5.** Show how a sample size of 25 follows from a confidence level and a tolerable deviation rate, and state
whether any standard requires that size.

**RQ 14-6.** What three objectives does a roll-forward procedure serve, and when is inquiry-only roll-forward
defensible?

**RQ 14-7.** List the conditions for benchmarking an automated control and explain why benchmarking is unavailable
in a first-year integrated audit.

**RQ 14-8.** What distinguishes a management review control that could detect a material misstatement from one that
could not?

**RQ 14-9.** Why does a review keyed to month-over-month change fail to detect a constant allocation error in a
subscription business?

**RQ 14-10.** What must you establish about information produced by the entity that a control consumes, and why is
an emailed screenshot insufficient?

**RQ 14-11.** Does an ITGC deficiency automatically make dependent automated controls ineffective? Explain.

**RQ 14-12.** Why does one deviation in a sample of 25 usually end the test?

**RQ 14-13.** State the two dimensions of severity and the overlay, and explain why the overlay can only raise a
grade.

**RQ 14-14.** When do two deficiencies aggregate, and what is the double-counting error to avoid when computing a
combined magnitude?

**RQ 14-15.** State the AS 1305 and AU-C 265 timing requirements for communicating deficiencies and identify the
substantive difference between them.

## Answers to Review Questions

**RQ 14-1.** In a test of controls the unit is an occurrence of the control and failure is a deviation; in a test of details
the unit is a transaction, balance, or dollar and failure is a misstatement. Tolerable failure is effectively zero
deviations for a key control, whereas tolerable misstatement is tied to performance materiality. Neither implies the
other.

**RQ 14-2.** AS 2201 requires an opinion on effectiveness as of the balance sheet date, so the control conclusion is the
product rather than a means of reducing substantive work. You test controls you would never rely on for evidence, and a
December failure is worse for the ICFR opinion than a February failure remediated in March.

**RQ 14-3.** A workpaper whose only evidence is what someone told you does not support a conclusion about operating
effectiveness; you must inspect or re-perform occurrences. Corroboration does not change the technique. At AtlasFlow
inquiry gave the wrong answer on access review frequency and inspection produced the finding.

**RQ 14-4.** How often the control operates (not the transaction frequency); what the population of occurrences is and how
its completeness is independently proven; what specific observable attribute you will inspect; and what constitutes a
deviation, including what does not.

**RQ 14-5.** For a large population with zero acceptable deviations, n = ln(1 − confidence)/ln(1 − tolerable rate); at 90%
and 9% this is ln(0.10)/ln(0.91) = 24.4, rounded to 25. No standard prescribes a size — AS 2201, AS 2315, AU-C 330, and
AU-C 530 require sufficient appropriate evidence, and the table is firm methodology.

**RQ 14-6.** It determines whether the control changed after the interim date, obtains evidence of continued operation through
the as-of date, and reconsiders the population. Inquiry-only roll-forward is defensible for a lower-risk unchanged control
with no interim deviations, and not for one addressing a significant risk.

**RQ 14-7.** The control must be entirely automated; a documented baseline test must exist; change management and logical
access must be effective; and the configuration must not have changed. In a first year no baseline exists, so the second
condition fails however good the general controls are.

**RQ 14-8.** Precision: the investigation threshold, the level of aggregation, and whether the expectation is independent of
the recorded amount. A review that investigates only variances above performance materiality cannot detect a material
misstatement by design, and one performed on a total alone is defeated by offsetting component errors.

**RQ 14-9.** Subscription revenue is recognized ratably, so an error embedded in the beginning balance recurs identically
each month and produces no period-over-period variance. Detecting it requires an independently derived expectation, such as
revenue computed from the subscription base and contractual rates.

**RQ 14-10.** Completeness and accuracy: that the parameters capture the whole population and that the values are right
(AS 1105). An emailed screenshot shows neither the parameters nor the extraction, and a posting-status or entity filter can
silently omit a population.

**RQ 14-11.** No. It removes the basis for inferring from one test that the control operated unchanged all period, but
direct evidence may remain. Identify the dependent controls, determine whether the exposure spans the year or a window, and
consider re-performance at the as-of date. The ITGC deficiency is still graded on its own.

**RQ 14-12.** Because the sample was designed assuming zero deviations. One in 25 is a 4% observed rate with an upper
deviation limit of roughly 13.4% at 90% confidence against a 9% tolerable rate, so the test fails arithmetically.

**RQ 14-13.** Magnitude — the potential misstatement, measured by exposed balance or transaction volume — and likelihood, met
at "reasonably possible," meaning more than remote. The overlay is the prudent official standard, which can only raise a
grade because it asks whether the mechanical result understates severity.

**RQ 14-14.** They aggregate when a single misstatement could pass through both undetected — when they share an exposed
population, a cause, or a control objective. The double-counting error is adding magnitudes of deficiencies that expose the
same dollars; compute the combined population once.

**RQ 14-15.** AS 1305 requires material weaknesses and significant deficiencies in writing to the audit committee before the
report is issued, and other deficiencies in writing to management. AU-C 265 sets the deadline at 60 days after the report
release date. The difference is timing: the PCAOB deadline precedes issuance.

## Key Definitions

**Aggregation of deficiencies.** Evaluation of two or more deficiencies in combination, required by AS 2201 where a single
misstatement could pass through each undetected because they share an exposed population, cause, or control objective.

**Attribute.** The specific, observable characteristic of a control occurrence that a test examines, stated so that two
auditors reach the same pass-or-fail answer. "The signature is dated on or before the posting date" is an attribute;
"review evidenced" is not.

**Benchmarking.** Reliance on a prior-period test of an entirely automated control, supported in later periods only by
evidence that the configuration has not changed. Available only where change management and logical access are effective
and a documented baseline test exists.

**Compensating control.** A control that mitigates the severity of a deficiency in another control, but only if it addresses
the same relevant assertion at the same or greater precision, operates frequently enough, has itself been tested
effective, and is not impaired by the same or a related deficiency.

**Control deficiency.** A condition in which the design or operation of a control does not permit personnel to prevent or
detect misstatements on a timely basis (AS 2201). A design deficiency would not work even if operated as intended; an
operating deficiency is a sound control that did not operate as designed.

**Deviation.** A failure of a control to operate as designed on a selected occurrence. A deviation is not a misstatement,
and the two are recorded on separate schedules.

**Dual-purpose test.** One procedure applied to a single selection to obtain evidence both about a control's operation and
about the monetary correctness of the transaction. The sample size is the larger of the two requirements.

**Extent.** The number of occurrences of a control examined, determined from the control's frequency and assessed risk and
increased for significant risks and for dependence on deficient general controls.

**Information produced by the entity (IPE).** A report, schedule, or extract generated by the entity and used as audit
evidence or as an input to a control. AS 1105 requires evaluation of its completeness and accuracy.

**Interim testing.** Testing of controls at a date before the balance sheet date, permitted by AS 2301 and AU-C 330 and
requiring roll-forward procedures to extend the conclusion to the as-of date.

**Isolated deviation.** A deviation excluded from the evaluation because its cause is identified and specific, cannot recur
for other population items, the affected items are separately identifiable and complete, and those items are tested in
full.

**Magnitude.** The potential misstatement a deficiency could permit, measured by the exposed account balance or transaction
volume and the volume of activity subject to the deficiency — not the misstatement actually found.

**Management review control (MRC).** A control in which a person compares recorded information to an expectation and
investigates differences. Effectiveness depends on precision, not on evidence that a review occurred.

**Material weakness.** A deficiency, or combination of deficiencies, such that there is a reasonable possibility that a
material misstatement will not be prevented or detected on a timely basis (AS 2201). Existence at the as-of date requires
an adverse ICFR opinion.

**Precision.** The smallest misstatement a control would identify, expressed as the investigation threshold and the level of
aggregation at which the control operates, compared to performance materiality.

**Prudent official standard.** The AS 2201 requirement to consider whether a prudent official, knowing the same facts, would
reach the same conclusion about a deficiency's severity. It can raise a grade but never lower one.

**Reasonably possible.** More than remote, borrowed from ASC 450-20 and used as the likelihood threshold in severity
grading. It is a low bar, and the absence of an identified misstatement is weak evidence against it.

**Re-performance.** Independent execution by the auditor of the control activity itself, using the inputs the control owner
used, to establish competent performance. The strongest of the four techniques.

**Roll-forward procedures.** Procedures extending an interim control conclusion to the as-of date: determining whether the
control changed, testing occurrences in the remaining period, and reconsidering the population.

**Significant deficiency.** A deficiency, or combination, less severe than a material weakness but important enough to merit
the attention of those responsible for oversight of financial reporting (AS 2201).

**Tolerable deviation rate.** The maximum population deviation rate the auditor will accept and still rely on the control.
For a key control it is set so the tolerable number of deviations is zero.

**Upper deviation limit.** The maximum population deviation rate consistent with the sample result at a stated confidence
level; with zero deviations it equals 1 − (1 − confidence)^(1/n).

## Chapter Summary

1. A test of controls asks whether an occurrence operated as designed; a test of details asks whether a recorded amount is
   right. Deviations and misstatements are separate scales, and neither implies the other.
2. In an ICFR audit the control conclusion is the product, not an input, which changes which controls you test and how much
   the timing of a failure matters.
3. Inquiry alone is never sufficient, and corroborated inquiry is still inquiry; re-performance of at least one occurrence
   is close to mandatory for a management review control.
4. Before selecting an item, fix the frequency, prove the population complete independently of management, state the
   attribute observably, and define a deviation.
5. The sample size table is firm methodology, not a requirement; 25 and 60 are two ends of one calculation,
   `n = ln(1 − confidence)/ln(1 − tolerable rate)`.
6. Roll-forward must determine whether the control changed, test the remaining period, and reconsider the population; a
   control that failed at interim cannot be rolled forward at all.
7. Benchmarking requires a documented baseline plus effective change management and logical access, so it is never
   available in a first-year integrated audit.
8. A management review control is tested on precision, and a threshold larger than the account balance it covers is not a
   control at all.
9. Information the control consumes must be tested for completeness and accuracy, because a control that reconciles to an
   incomplete report reconciles to nothing.
10. An ITGC deficiency removes the basis for the test-of-one inference but does not mechanically fail dependent controls.
11. One deviation in 25 usually ends the test because the sample was designed for zero, and isolation requires four
    conditions management's explanation rarely satisfies.
12. Severity is magnitude and likelihood, overlaid by the prudent official standard, and the auditor's own testing never
    mitigates it.
13. Deficiencies aggregate when they share an exposed population, cause, or objective; the argument that carries the
    conclusion is that the control relied on to mitigate one is impaired by another.
14. A compensating control mitigates only if it meets all four conditions, and the fourth — not impaired by a related
    deficiency — is where most proposed mitigation fails.
15. Remediation after the as-of date cannot support the opinion, and remediation shortly before it usually cannot
    accumulate enough occurrences; both belong in a written sufficient-time analysis.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Materiality: $1,450, $940, $72 | Chapter 3 | Every precision and magnitude comparison here uses these figures |
| ITGCs, SOC 1 reports, CUECs, and bridge letters | Chapter 11 | What W-1 through W-14 are deficiencies *in*; the basis for grading W-9 and W-10 |
| Application and interface controls, I-1 through I-9 | Chapter 12 | The control descriptions these tests execute against |
| Walkthroughs and controls that do not exist | Chapter 13 | The origin of the FIN-REV-07/OTC-05 finding |
| Sampling theory and the statistical tables | Chapter 15 | The derivations this chapter uses without proving |
| Journal entry testing and management override | Chapter 16 | The substantive response to W-12 and W-13 |
| Evaluating misstatements and the final ICFR conclusion | Chapter 19 | Where these gradings are aggregated with the revenue findings |
| The adverse ICFR opinion and its wording | Chapter 20 | How two material weaknesses are described |

## Further Reading

- PCAOB AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of Financial
  Statements* — testing operating effectiveness, severity, the indicators of material weakness, and the prudent official
  standard.
- PCAOB AS 2301, AS 1105, AS 2315, and AS 1305, for nature, timing, and extent; evidence and information produced by the
  entity; sampling; and the deficiency communication requirements. See also the PCAOB staff guidance on auditing internal
  control, including the practice alerts on evidence sufficiency in ICFR audits.
- AICPA AU-C 265, AU-C 330, AU-C 402, and AU-C 530 for the non-issuer equivalents, and the AICPA audit guides covering
  internal control and audit sampling.
- COSO, *Internal Control — Integrated Framework* (2013), Principles 10 through 12 and 16 through 17, with the COSO guidance
  on evaluating deficiencies in combination.
- SEC Exchange Act Rule 13a-15 and Item 308 of Regulation S-K, with the SEC's interpretive guidance for management's report
  on internal control.
