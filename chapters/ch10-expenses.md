# Chapter 10 — Expenses, Accruals, and the Expenditure Cycle

> AtlasFlow spent $172,440 in FY2025, and the audit risk in that number is almost entirely the risk that something
> is *missing*. A revenue test asks whether what is recorded should be; an expense test asks what should be recorded
> and is not. That inversion changes the population, the direction of sampling, the confirmation form, and the date
> you stop looking — and it sits alongside three consequential judgments: the four-year amortization of $24,000 of
> capitalized commissions, the $10,900 capitalized into internal-use software on Jira codes restaged on 22% of the
> hours, and a 4.6-point gross margin expansion that turns on which side of a line each dollar was posted to.

## Learning Objectives

- **LO 10.1** Map the expenditure cycle across Coupa and NetSuite and identify where each relevant assertion is first
  at risk.
- **LO 10.2** Explain why completeness dominates the cycle and design a test whose direction of sampling follows from
  that assertion.
- **LO 10.3** Design a search for unrecorded liabilities: population, cut-off date, a scope threshold derived from
  performance materiality of $940, and the evidence sources.
- **LO 10.4** Recompute the bonus, commission, and paid-time-off accruals, state the sensitive input in each, and give
  a defensible range.
- **LO 10.5** Reconcile a payroll register to the 812-employee headcount and execute a substantive analytical
  procedure on personnel cost.
- **LO 10.6** Evaluate the ASC 340-40 capitalization decision, including the commensurate-renewal analysis, and
  reconcile the $1,900 churned-customer exposure to the $620 recorded adjustment.
- **LO 10.7** Audit capitalized internal-use software additions when stage designations were changed retroactively,
  quantifying the exposure in dollars rather than percentages of hours.
- **LO 10.8** Distinguish research and development cost, capitalizable internal-use software cost, hosting fees, and
  capitalizable implementation costs of a hosting arrangement.
- **LO 10.9** Test recognition, measurement, and classification of a $1,900 ASC 420-10 restructuring charge.
- **LO 10.10** Compute the gross margin effect of a classification error and grade the deviations arising from travel,
  purchase-card, related-party, and vendor-master analytics.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2110; AS 2301 / AU-C 315, 330 | Understanding the process, including the 3,604 non-PO invoices; procedures must address completeness |
| PCAOB | AS 2305; AS 2315 / AU-C 520, 530 | Analytical expectation and precision; sampling and direction of testing |
| PCAOB | AS 1105; AS 2501 / AU-C 500, 540 | Reliability of IPE; estimates: bonus funding, PTO balances, period of benefit |
| PCAOB | AS 2401; AS 2410; AS 2801 / AU-C 240, 550, 560 | Understated accruals as a fraud pattern; related parties; the February 3, 2026 bonus approval |
| PCAOB | AS 2201; AS 1305; AS 2810 / AU-C 265, 700 | Dual-purpose testing; deficiency grading; evaluating U-5 |
| FASB ASC | 340-40 | Incremental costs of obtaining a contract; period of benefit; impairment |
| FASB ASC | 350-40 (ASU 2018-15); 730-10 | Software stages; hosting implementation costs; R&D expensed as incurred |
| FASB ASC | 420-10; 712-10; 710-10-25 | One-time termination benefits versus ongoing arrangements; compensated absences |
| FASB ASC | 450-20; 360-10-35; 842; 850-10 | The disputed invoice; the abandoned Australia lease asset; related-party disclosure |
| SEC | SAB Topic 5-P; Reg. S-X Rule 5-03; Reg. S-K Item 404 | Restructuring presentation; captions; the $120,000 threshold |

AtlasFlow is an SEC issuer, so PCAOB standards govern. Two differences matter for a private SaaS company: AS 2310
imposes confirmation requirements AU-C 505 does not, though neither requires accounts payable confirmation; and absent
an integrated audit the §10.8 and §10.12 deficiencies feed only the AU-C 265 communication.

## Prerequisites and Chapter Dependencies

Read Chapter 3 for the materiality figures used throughout — overall materiality $1,450, performance materiality
$940, clearly trivial threshold $72 — and Chapter 2 for the assertion-level risk framework. Chapter 12, §12.4
established the Coupa match configuration and invoice volumes; Chapter 8 owns cash disbursement controls; Chapter 9
owns stock-based compensation, including the $900 capitalized here; Chapter 11 owns the Coupa and Concur IT general
controls; Chapter 16 owns journal entry testing; Chapter 19 accumulates U-5.

## 10.1 The Expenditure Cycle at AtlasFlow: Systems, Volumes, and Where Money Leaves

Expense is not one account; it is thirteen accounts fed by four processes with different controls, so plan by
process rather than by caption.

**Exhibit 10-1. FY2025 expenses by nature and by financial statement line (in thousands).**

| Nature of cost | Cost of revenue | R&D | S&M | G&A | Restr. | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Cash personnel cost (salary, bonus, commission, taxes, benefits) | 13,300 | 23,600 | 27,900 | 6,300 | — | 71,100 |
| Stock-based compensation (Chapter 9) | 2,100 | 11,400 | 7,600 | 7,600 | — | 28,700 |
| Cloud hosting and production infrastructure | 13,400 | — | — | — | — | 13,400 |
| Depreciation and amortization | 4,560 | 2,300 | 1,900 | 3,140 | — | 11,900 |
| Amortization of deferred contract acquisition costs (6210) | — | — | 8,600 | — | — | 8,600 |
| Contractors and outsourced services | 2,400 | 3,100 | 1,300 | 1,400 | — | 8,200 |
| Professional fees | — | 200 | 400 | 5,300 | — | 5,900 |
| Marketing programs and events | — | — | 7,400 | — | — | 7,400 |
| Travel and entertainment | 400 | 300 | 2,100 | 300 | — | 3,100 |
| Software subscriptions, internal IT, facilities, and other | 2,780 | 3,000 | 4,100 | 2,360 | — | 12,240 |
| Restructuring (6400) | — | — | — | — | 1,900 | 1,900 |
| **Total** | **38,940** | **43,900** | **61,300** | **26,400** | **1,900** | **172,440** |

Three features drive the plan. Personnel cost of $99,800 is 57.9% of total expense, so payroll procedures carry more
of the assurance than accounts payable procedures do. Non-cash and estimate-driven amounts are $49,200, or 28.5%, and
none will appear in a subsequent-disbursements file. And $10,900 of cost was capitalized into internal-use software
rather than expensed, which is why §10.8 and §10.9 exist.

**Exhibit 10-2. The FY2025 expenditure flow and volumes.**

| Stage in Coupa unless noted | Control point | Volume |
| --- | --- | --- |
| Requisition and approval | Commodity code and cost center; budget check; two approvers above $50 | 9,240 |
| Purchase order | Vendor must exist in the vendor master | 8,116 |
| Receipt | Goods receipt; services on requester milestone confirmation | 5,940 |
| Invoice | Supplier portal, OCR email capture, or manual AP entry | 18,410: 14,806 PO-backed, 3,604 non-PO |
| Three-way match | Quantity 0%, unit price 5% or $500, invoice total $1,000 | 14,806 matched; 1,214 auto-released |
| Post to GL (NetSuite, I-7) | Nightly API; monthly AP subledger-to-GL reconciliation | 18,410 |
| Payment (NetSuite, First Meridian) | Positive pay; dual wire authorization (Chapter 8) | 1,912 batches |

Two structural facts are the audit story. First, 3,604 invoices — 19.6% of the population — have no purchase order and
therefore no three-way match; approved by a cost-center owner after the fact, they carry the professional fees, hosting
true-ups, recruiting fees, and sponsorships most likely to be received in December and invoiced in January. Second, the
configured tolerances are looser than the March 2024 procurement policy (2% or $250 on unit price, $250 on invoice
total), which Chapter 12, §12.4 concluded is a deficiency: 1,214 invoices auto-released on an invoice-total variance
between $250 and $1,000, aggregate absolute variance $412, or 43.8% of performance materiality — so the match cannot be
the sole control over accuracy.

## 10.2 Why Completeness Inverts the Testing Instinct

The instinct brought from revenue testing is: get the population, sample it, vouch each item. Applied to expense
that tests existence, accuracy, and classification — and existence is the assertion least likely to be misstated,
because recording an expense you did not incur reduces reported income.

**Exhibit 10-3. Relevant assertions for the expenditure cycle at December 31, 2025.**

| Assertion | Risk | Why, and the responsive procedure |
| --- | --- | --- |
| Completeness | **Significant** | Unidirectional incentive to defer cost; 3,604 non-PO invoices. Search for unrecorded liabilities; accrual completeness; GR/IR analysis |
| Cut-off | **Significant** | Obligating event and invoice date differ by weeks for services. Subsequent disbursements; unvouchered invoice file |
| Valuation of capitalized cost | **Significant** | $10,900 of software additions, $13,920 of contract acquisition costs. §10.7, §10.8, case study |
| Accuracy | Moderate | 1,214 invoices auto-released on a $1,000 tolerance. Recomputation and tests of details |
| Classification | Moderate, qualitatively elevated | A $940 shift moves gross margin 63 basis points. Reperform the cost-center mapping |
| Existence | Low | A fictitious expense reduces income. Vouching within the accuracy test |

Three consequences follow. Every completeness procedure starts outside the accounting records: cash paid after year end,
goods receipted without an invoice, purchase orders open past their delivery date, engagement letters, and the knowledge
of the people who ordered the work. The direction of testing reverses, the finding being the absence of a record. And
small balances become the interesting ones — you confirm vendors with nil recorded balances.

## 10.3 Designing the Search for Unrecorded Liabilities

The search is a design problem with four decisions. This section makes them; the walkthrough executes them.

**The cut-off date.** Go far enough forward that the ordinary invoice-to-payment lag has run, and no further than the
date fieldwork is substantially complete. AtlasFlow's FY2025 median lag was 34 days and the 90th percentile 52 days, and
the planned report date is February 20, 2026, so choose **February 13, 2026** — 44 days out, past the median, a week
before the report. A January 31 cut-off would have excluded roughly 10% of December obligations by count.

**The scope threshold.** Performance materiality of $940 is an aggregation tolerance for the statements as a whole; used
to select items it would let twelve unrecorded $900 invoices pass untested. Set it at **$70**, just below the $72 clearly
trivial threshold, because a search designed above the accumulation floor is designed to miss misstatements the team must
accumulate. The defensible range runs to about $235 (25% of performance materiality) where a larger below-threshold sample
compensates, and a clean prior-year search would support that end — but AtlasFlow's FY2024 search produced an $88
exception. At $70 the count is manageable: 58 of 1,842 subsequent payments, 3.1% by count and 63.5% by value.

**The sources.** No single source is sufficient; each misses a different kind of obligation, so the design is the
combination.

**Exhibit 10-4. Sources for the December 31, 2025 search, and what each alone would miss.**

| Source | Population at the cut-off | Items ≥ $70 | Value | Blind to |
| --- | --- | --- | --- | --- |
| S — Subsequent disbursements, Jan 1 – Feb 13, 2026 | 1,842 payments, $14,830 | 58 | 9,410 | Anything uninvoiced or disputed and unpaid |
| R — Unmatched receipts (Coupa GR/IR at 12/31) | 34 receipts, $1,180 | 9 | 760 | Services, rarely receipted; non-PO orders |
| P — Open POs, delivery on or before 12/31/2025, no receipt | 27 POs, $2,340 | 12 | 1,690 | Non-PO spend — 19.6% of invoice count |
| V — Unvouchered invoice file (dated 12/31 or earlier, unposted) | 46 invoices, $1,620 | 11 | 840 | Obligations never invoiced |
| F — Professional fee and contingent arrangements | 11 engagement letters, $1,845 | 11 | 1,845 | Everything outside professional services |
| I — Inquiry of seven budget owners; December minutes | Not quantified | n/a | n/a | Nothing in principle; everything in practice |

Source P is the one staff skip and the one that catches the interesting item: an open purchase order promising December
15 delivery with no receipt means the vendor was late, the requester failed to receipt, or the goods arrived and nobody
told accounting — and the third case is where the disputed Halverson invoice surfaces.

**Below the threshold.** The stratum under $70 is 1,784 payments totaling $5,420, which could aggregate if the accrual
process omitted a category systematically; select 30 at random ($412) and perform the same procedure.

## 10.4 Accruals: Testing Estimates You Cannot Confirm

An accrual is an estimate of an obligation for which no invoice exists. Under AS 2501 you test how management built it,
test the data behind it, or test it against what actually happened — and the third route is available for nearly every
AtlasFlow accrual, because January and February activity is known before the report date.

**Exhibit 10-5. Accrued liability inventory at December 31, 2025 (in thousands).**

| Account | Description | Balance | Primary procedure |
| --- | --- | --- | --- |
| 2000 | Accounts payable | 7,600 | Subledger-to-GL; subsequent disbursements; confirm nil balances |
| 2100 | Accrued compensation — salaries and bonus | 9,100 | Recompute; February 3, 2026 committee approval |
| 2105 | Accrued commissions | 4,800 | Recompute from December bookings; trace to January payroll |
| 2110 | Accrued paid time off | 2,500 | Recompute from the ADP and Deel accrual reports |
| 2200 | Accrued expenses — other | 6,400 | Subsequent invoices; standing-accrual list completeness |
| 2210 | Accrued sales and use / VAT | 2,900 | Avalara recomputation; misstatement C-4 of $180 arose here |
| 2220 | Accrued professional fees | 1,400 | Engagement letters and statements of account (source F) |
| 2230 | Customer credits and refunds payable | 1,200 | Chapter 6, §6.7 (revenue-side) |
| | **Total excluding AP and leases** | **28,300** | |

The total foots (9,100 + 4,800 + 2,500 + 6,400 + 2,900 + 1,400 + 1,200 = 28,300), and with accounts payable the tested
population is $35,900, or 32.4% of current liabilities of $110,800.

Account 2200 is the residual and the highest risk, because it is built from a "standing accrual list" management
maintains in Excel. The test is not the accuracy of the amounts on the list but the *completeness of the list itself* —
compare it to the FY2024 list, to the commodity codes with FY2025 Coupa spend, and to the subsequent-disbursements
population. Two commodity codes with spend above $70 appeared nowhere on it: outside translation ($112) and penetration
testing ($196). Both proved fully invoiced and paid before December 31, so no accrual was required — but that
verification, not the absence of a line, is the evidence. Three lines within 2200 also matched December 31, 2024 to the
dollar, and one, a $74 franchise tax plug, recomputed at $71.

## 10.5 Accounts Payable Confirmations and Disbursement Cut-Off

Neither AS 2310 nor AU-C 505 requires accounts payable confirmation, and in most SaaS audits it is not the efficient
procedure: the vendor statement, the subsequent disbursement, and the open purchase order are cheaper and at least as
reliable. Four situations make it better evidence, and AtlasFlow presents three: the vendor issues no statements
(contingent recruiters, litigation counsel billing by matter); the recorded balance is nil while the relationship is
active, so only a request to the vendor tests completeness at *its* end; an invoice is disputed, making the vendor's
claimed amount the measurement input; and the vendor is a related party. Use the **blank form** — ask what AtlasFlow owed
rather than presenting the amount you doubt.

**Exhibit 10-6. Accounts payable confirmation results (in thousands; blank form; 8 sent, 8 returned).**

| # | Vendor | Recorded | Confirmed | Difference | Reconciling item | Disposition |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Amazon Web Services, Inc. | 1,190 | 1,190 | — | — | Agrees (a) |
| 2 | Snowflake Inc. | 205 | 214 | (9) | December 28 invoice received January 5 | Below CTT (b) |
| 3 | Halverson Consulting Group | — | 110 | (110) | Invoice 4471-B dated 12/19/2025, disputed | **U-5** (c) |
| 4–8 | Cascade 148; Vantage 132; Ridgeline 96; Fairmont 84; Orion 76 | 536 | 536 | — | — | Agree (a) |
| | **Total** | **1,931** | **2,050** | **(119)** | | |

Tick marks: (a) agreed to the vendor response and the accrual detail at WP 3200-06. (b) Below the $72 clearly trivial
threshold; not accumulated. (c) Understatement of $110; see below.

The total cross-foots: recorded $1,931 plus $119 equals confirmed $2,050, decomposing as $9 plus $110. Source P, not the
confirmation, discovered Halverson — open purchase order 20-4471 had a past delivery date and no receipt; what the
confirmation added was the vendor's own statement that it claims $110, converting "the amount is unknown" into a
measurable amount.

**Measuring the disputed liability.** Halverson performed data-migration subcontract work on the Kestrel conversion
between November 24 and December 18, 2025 under purchase order 20-4471 and invoiced $110 on December 19. AtlasFlow's
project manager rejected the deliverable on January 8, 2026 and management recorded nothing. Existence is settled: the
Jira work log for epic ATLF-3311 shows 640 subcontractor hours in that window, and the purchase order is
time-and-materials with no acceptance condition, so rejection does not extinguish the obligation. The measurement range
is $50 to $110 — contractual entitlement against a settlement at roughly 45%, the outcome of two prior subcontractor
disputes — and ASC 450-20 directs you to the low end only when no amount is a better estimate, whereas here a discount is
a future negotiation rather than measurement uncertainty at the balance sheet date. Propose $110, 11.7% of performance
materiality, which becomes **U-5, $(110)**. A settlement executed at $50 before the report date would make $50 the answer.

**Disbursement cut-off.** A payment recorded in the wrong period misstates cash and accounts payable and never touches
income, which is why it is easy to under-test. Compare the recorded date of the last 15 payments of FY2025 and the first
15 of FY2026 across the three USD accounts to the positive-pay transmission date, ACH file timestamp, or wire
confirmation. Result: 29 of 30 agreed; one $58 wire released at 4:52 p.m. Central on December 31, 2025 was recorded
January 2, 2026 from the next day's bank feed — clearly trivial, but documented, because a *pattern* of such items is the
signature of window dressing.

## 10.6 Payroll and Personnel Costs

Personnel cost is 57.9% of total expense, and unlike accounts payable it has a third-party population to reconcile to:
the registers from ADP Workforce Now (US) and Deel (UK, Australia, India). Start with headcount, which tests
completeness of the register and supports the 812-employee figure in Item 1 of the Form 10-K.

**Exhibit 10-7. Headcount reconciliation, December 31, 2025.**

| Reconciling item | US | UK | Australia | India | Total |
| --- | --- | --- | --- | --- | --- |
| Active per the ADP register, pay period ended December 26, 2025 | 611 | — | — | — | 611 |
| Active per the Deel December 2025 worker roster | — | 73 | 41 | 99 | 213 |
| **Subtotal per payroll systems** | **611** | **73** | **41** | **99** | **824** |
| Less: separations effective on or before 12/31 with final pay in December | (9) | (2) | (3) | — | (14) |
| Add: hires starting December 29–31, first paid in January 2026 | 2 | — | — | — | 2 |
| **Headcount at December 31, 2025 per the Form 10-K** | **604** | **71** | **38** | **99** | **812** |

The exhibit foots by column (611 − 9 + 2 = 604; 73 − 2 = 71; 41 − 3 = 38) and in total. The 14 separations are the
termination test: agree each to a dated separation notice and confirm the final pay date and that no pay followed. The 2
late-December hires are the ghost-employee test in reverse, resolved by the offer letter and the Okta account creation
date.

**Substantive analytical procedure.** Cash personnel cost *incurred* in FY2025 was $79,600: $71,100 expensed plus $8,500
capitalized (§10.8). Average monthly headcount was 621 in FY2024 and 738 in FY2025, and FY2024 cash personnel cost was
$65,100, or $104.83 per average head; adjusted for the 3.0% April 2025 merit cycle at a stable country mix, $104.83 ×
1.030 = $107.97. Expectation: 738 × $107.97 = **$79,700** against recorded $79,600, a difference of $(100), or 0.13%. The
investigation threshold is $470, 0.6% of the expectation — precise only because headcount is independently verified and the
merit rate documented. Disaggregate a larger difference by country, then by functional line, where it points at
capitalization.

### 10.6.1 The bonus accrual

Account 2100 of $9,100 is accrued salaries for the December 27–31 stub period of $1,940, employer taxes and benefits
on that stub of $560, and the FY2025 corporate bonus plan of $6,600.

**Exhibit 10-8. Recomputation of the FY2025 corporate bonus accrual (in thousands except headcount).**

| Input | Amount | Source and test |
| --- | --- | --- |
| Bonus-eligible population | 812 less 170 quota-carrying sales staff = 642 | ADP and Deel compensation-type field |
| Target pool at 100% funding | 8,800 | Target percentages × base salary, recomputed |
| Funding metrics | Revenue $148,200 v. plan $151,000 (98.1%); ARR $172.0M v. $176.0M (97.7%) | Plan agreed to the board-approved operating plan |
| Funding curve outcome | 75% | Plan document: 95% funds 50%, 100% funds 100%, interpolated |
| **Accrual** | **8,800 × 0.75 = 6,600** | Agreed to account 2100 detail at WP 3200-11 |

The sensitive input is the funding percentage, not the pool. Five points is $440, so the defensible range of 70% to
80% spans $6,160 to $7,040 — nearly one performance materiality. Two items narrow it: the compensation committee
approved 75% funding on February 3, 2026, a subsequent event under AS 2801 confirming a condition existing at the
balance sheet date, and bonuses were paid February 27, 2026 at $6,570, within $30 of the accrual.

### 10.6.2 The paid-time-off accrual

**Exhibit 10-9. Recomputation of accrued paid time off (in thousands except days and rates).**

| Country | Employees | Avg. accrued days | Avg. daily cost | Base accrual | Employer burden | Total |
| --- | --- | --- | --- | --- | --- | --- |
| US | 604 | 6.4 | 0.532 | 2,057 | 8.0% = 164 | 2,221 |
| UK | 71 | 2.8 | 0.470 | 93 | 13.8% NI = 13 | 106 |
| Australia | 38 | 8.6 | 0.301 | 98 | 11.5% super = 11 | 109 |
| India | 99 | 3.9 | 0.163 | 63 | — (encashment only) | 63 |
| **Total** | **812** | | | **2,311** | **188** | **2,500** |

The exhibit foots to account 2110 of $2,500 and cross-foots (2,311 + 188 = 2,499, with $1 of rounding). Three tests:
agree the day balances to the ADP and Deel accrual reports and reperform the report total against the 812 headcount;
agree the daily rates to the compensation master; and confirm the ASC 710-10-25 criteria. That last is real — the US
policy pays unused balances on separation, so the obligation vests even though Texas law does not compel payout, while
India permits encashment of earned leave only.

## 10.7 Commissions: The Accrual and the ASC 340-40 Capitalization Decision

Commissions generate two problems: a liability that must be complete and a deferred asset that must be recoverable
over a defensible period.

**Exhibit 10-10. Composition and recomputation of account 2105 (in thousands).**

| Component | Recorded | Recomputation | Difference |
| --- | --- | --- | --- |
| Commissions on December 2025 bookings, paid January 30, 2026 | 3,240 | 3,199 | 41 |
| FY2025 annual accelerator true-up, paid February 27, 2026 | 980 | 980 | — |
| Employer payroll taxes at 7.65% | 323 | 323 | — |
| Non-US plans and draw balances net of clawbacks | 257 | 257 | — |
| **Total** | **4,800** | **4,759** | **41** |

Recomputing the December component: December ACV bookings were $34,200, of which $25,174 was signed December 24–31
(§3.1). New and expansion ACV was 69% of the month ($23,598) and renewals 31% ($10,602). Applying the §4.2 plan rates and
the 0.25% override on all December ACV: $23,598 × 11.8% = $2,784.6; $10,602 × 3.1% = $328.7; $34,200 × 0.25% = $85.5;
total **$3,199**. The recorded amount exceeds the recomputation by $41, or 1.3% — below the clearly trivial threshold and
directionally expected, because the plan pays 1.5× accelerators above quota while the recomputation uses blended base
rates; confirm that by recomputing two above-quota representatives at their accelerated rates. The unexpected result is a
recorded amount *below* the recomputation, meaning the December 24–31 bookings were excluded — the natural error when 41%
of Q4 ACV closes in five days. Trace the January 30, 2026 payment file back to bookings month.

### 10.7.1 The capitalization decision and the four-year period of benefit

ASC 340-40 requires capitalization of the *incremental* costs of obtaining a contract — those that would not have
been incurred had the contract not been obtained — amortized consistently with transfer of the related services.
AtlasFlow capitalizes commissions, overrides, and employer payroll taxes on both, and expenses base salary and
sales-engineer time, which are not incremental.

**Exhibit 10-11. Deferred contract acquisition cost roll-forward, FY2025 (in thousands).**

| Component | Amount |
| --- | --- |
| Balance, December 31, 2024 (current $7,900 + noncurrent $11,600) | 19,500 |
| Costs capitalized in FY2025 | 13,920 |
| Amortization (account 6210, within sales and marketing) | (8,600) |
| Write-off of costs relating to churned customers (misstatement C-3, recorded) | (620) |
| Foreign currency translation | (200) |
| **Balance, December 31, 2025 (current $9,800 + noncurrent $14,200)** | **24,000** |

The roll-forward foots (19,500 + 13,920 − 8,600 − 620 − 200 = 24,000) and the closing balance agrees to accounts 1300
and 1305. The $13,920 comprises commissions and overrides of $12,610, employer payroll taxes of $965, and non-US plan
equivalents of $345; of $13,940 earned, $1,330 failed the incremental test and was expensed.

The hard part is the amortization period, which turns on the **commensurate** test. If the renewal commission is
commensurate with the initial commission, the initial commission relates only to the initial contract and amortizes over
its term; if not, it relates to anticipated renewals as well and the period extends to the expected period of benefit.
AtlasFlow's renewal commissions average 3.1% of ACV against 11.8% on new business — a ratio of 26.3%, not commensurate on
any reasonable reading — so four years is required rather than optional, and the question is whether four is right.
Corroborate the §4.2 support (average customer life of 4.3 years) from retention: 91% gross retention implies 9% annual
churn and an 11.1-year average life, so four years is if anything conservative. Accept three to six years; extending from
four to five would reduce FY2025 amortization by roughly $1,050, or 72% of overall materiality.

### 10.7.2 The $1,900 churned-customer exposure and its reconciliation to C-3

Section 4.2 records $1,900 of capitalized costs relating to customers whose contracts were not renewed at year end;
corrected misstatement C-3 is $620. They differ because the $1,900 is a *query result* and the $620 is an *impairment
conclusion*. Under ASC 340-40 you impair a capitalized contract cost when its carrying amount exceeds the remaining
consideration expected less the direct costs of providing the services — in substance, when the period of benefit has
ended.

**Exhibit 10-12. Disaggregation of the $1,900 of costs relating to non-renewed contracts (in thousands).**

| Cohort | Customers | Carrying amount | Evidence obtained | Impairment |
| --- | --- | --- | --- | --- |
| A. Written non-renewal on or before 12/31; service terminated | 61 | 620 | Non-renewal notices; Zuora "Cancelled"; no FY2026 invoicing | 620 |
| B. Term expired Nov–Dec 2025; renewal executed after year end | 58 | 430 | 41 executed FY2026 order forms, $2,140 ACV, dated Jan 6 – Feb 11, 2026; 17 at "Contract Sent" | — |
| C. Continuing month to month; still invoiced and consuming | 74 | 510 | December 2025 Zuora invoices; workflow-run telemetry | — |
| D. *Renewal* commissions whose renewal term expires in 2026 | 21 | 340 | Order form end dates in 2026; Salesforce opportunity left "Open" | — |
| **Total** | **214** | **1,900** | | **620** |

The exhibit foots ($620 + $430 + $510 + $340 = $1,900; 61 + 58 + 74 + 21 = 214) and the impairment column ties to C-3.
Cohort B is the judgmental one: 17 of the 58 customers had no executed renewal at the report date, carrying $178, and
impairing them in full would be defensible; the team accepted them because the period of benefit is the *expected* rather
than contractual period, and even wholesale reversal is 12.3% of overall materiality. Cohort D, swept in by a Salesforce
opportunity-stage defect, shows that management's population definition is itself IPE: propose the $1,900 query result and
you have proposed a $1,280 overstatement of expense.

## 10.8 Capitalized Internal-Use Software and Research and Development

**Exhibit 10-13. Capitalized internal-use software roll-forward, FY2025 (in thousands).**

| Component | Gross cost (1560) | Accumulated amortization (1565) | Net |
| --- | --- | --- | --- |
| Balance, December 31, 2024 | 21,700 | (8,300) | 13,400 |
| Additions — costs capitalized in FY2025 | 10,900 | — | 10,900 |
| Retirements of fully amortized assets | (1,400) | 1,400 | — |
| Amortization expense | — | (5,700) | (5,700) |
| **Balance, December 31, 2025** | **31,200** | **(12,600)** | **18,600** |

Every line foots and ties: gross of $31,200 and accumulated amortization of $(12,600) agree to the chart of accounts, net
of $18,600 to the balance sheet, and opening net to the FY2024 comparative. Amortization of $5,700 is derived ($13,400 +
$10,900 − $18,600) and corroborated by its disaggregation — $4,000 to cost of revenue, $1,100 to research and development,
$600 to general and administrative — which with $4,800 of depreciation and $1,400 of acquired intangible amortization
foots to the $11,900 row of Exhibit 10-1. A client-provided amortization figure that does not fall out of the roll-forward
means an unrecorded impairment or a missing addition.

**Exhibit 10-14. Composition of the $10,900 of FY2025 additions (in thousands).**

| Component | Amount | Capitalizable under ASC 350-40? |
| --- | --- | --- |
| Internal engineering payroll coded to capitalizable epics | 7,200 | Yes, if the hours are in the application development stage |
| Employer payroll taxes and benefits on the above | 1,300 | Yes |
| Stock-based compensation on the above (Chapter 9) | 900 | Yes; ASC 350-40 does not exclude share-based payment |
| Third-party contractor fees (Cascade Contract Engineering) | 900 | Yes, direct external costs of services |
| Cloud infrastructure for development and test environments | 600 | Judgmental; only to the extent directly attributable |
| **Total** | **10,900** | |

The $600 of cloud infrastructure is the line to challenge. AWS account tagging shows $470 in accounts used exclusively by
the two capitalized project teams and $130 allocated from a shared non-production account on a headcount basis. That
allocation is weak — a shared environment supports maintenance as much as development — but it is 9.0% of the clearly
trivial threshold; quantify it rather than passing it without a number.

### 10.8.1 Research and development versus capitalizable cost

Under ASC 730-10 research and development is expensed as incurred; under ASC 350-40 preliminary-project-stage and
post-implementation-stage costs are expensed and application-development-stage costs are capitalized. The two frameworks
intersect at one question — has the preliminary project stage ended? — which requires evidence that the project is
authorized, the technology selected, and the evaluation of alternatives complete.

**Exhibit 10-15. Capitalization rate trend (in thousands).**

| Measure | FY2025 | FY2024 | FY2023 |
| --- | --- | --- | --- |
| Research and development expense (6100) | 43,900 | 36,700 | 29,800 |
| Costs capitalized as internal-use software | 10,900 | 7,900 | 6,100 |
| **Total development spend** | **54,800** | **44,600** | **35,900** |
| Capitalization rate | 19.9% | 17.7% | 17.0% |
| R&D expense as a percentage of total revenue | 29.6% | 30.9% | 32.6% |

The rate rose 2.2 percentage points after 0.7 points in FY2024. Quantify rather than describe: at the FY2024 rate
additions would have been $9,700, so $1,200 more would have been expensed — 82.8% of overall materiality — which is what
justifies treating capitalization as a significant risk. FY2025 is also the first year of the Kestrel integration and a
re-architected execution engine, so a rising rate is not itself a misstatement indicator. Whether the *hours* behind it
are correctly staged is the extended case study.

## 10.9 Hosting Costs, Hosting-Arrangement Implementation Costs, and Leases

Account 5100 is $13,400 — 34.4% of cost of revenue and the largest third-party expense — and it carries low risk for
existence and accuracy (AWS invoices monthly, machine-generated, paid by wire) and moderate risk for cut-off and
classification. Hosting cost was $13,400, $11,300, and $9,400 in FY2025, FY2024, and FY2023 against subscription revenue
of $135,800, $108,300, and $82,100 — 9.87%, 10.43%, and 11.45%. Hosting grew 18.6% against 25.4% subscription growth, the
expected pattern for a maturing multi-tenant platform and corroboration for the gross margin improvement in §10.11. The
cut-off risk is concrete: the December 2025 AWS invoice of $1,190 was dated January 3, 2026 and paid January 6, so the
entire December cost is an accrual and the largest item on the walkthrough's follow-up schedule. Also recompute the
reserved-instance prepayment straight-line over its 36-month term ($2,400 paid January 2025, $1,600 amortized, $800
remaining in prepaid expenses).

**Implementation costs of a hosting arrangement.** ASC 350-40, as amended by ASU 2018-15, applies the internal-use
software model to these costs and requires the amortization to be presented in the *same line item* as the hosting fee
rather than in depreciation and amortization. AtlasFlow incurred $860 on the September 2025 NetSuite upgrade:
configuration and interface development capitalized $610, data conversion expensed $196, training expensed $54. Test the
split by agreeing each invoice line on the integrator's statements of work to a work-stream code. The $610 amortizes over
the 4.2-year remaining term at $145 per year within general and administrative expense.

**Leases, briefly.** Operating lease liabilities of $23,400 stand against a right-of-use asset of $21,700; the $1,700 gap
is tenant improvement allowances of $1,050, net accrued-versus-prepaid rent of $270, and the $380 Australia impairment.
The 6.4% incremental borrowing rate cannot be benchmarked to the 0.25% convertible note coupon, which is priced for the
conversion option; 100 basis points moves the liability roughly $620, below performance materiality.

## 10.10 The Restructuring Charge

In October 2025 AtlasFlow eliminated 41 positions and consolidated the Australia office, recording $1,900 in account
6400. Which standard applies is not automatic: ASC 420-10 governs one-time termination benefits under a plan for a
specified event, while ASC 712-10 governs benefits under an *ongoing* arrangement, including one arising from substantive
past practice, and accrues them earlier — so an ongoing practice would make part of the charge accruable before the
October communication. Evidence obtained: no severance schedule in the handbook; one prior reduction in force, in 2020,
on different terms (two weeks per year of service against the 2025 plan's flat eight weeks plus one week per year); and a
board-approved plan memorandum dated October 14, 2025. Conclusion: ASC 420-10.

**Exhibit 10-16. Composition of the charge and the year-end accrual (in thousands).**

| Component | Charge | Recognition basis | Paid | Accrual |
| --- | --- | --- | --- | --- |
| Termination benefits — 34 employees, no future service | 1,180 | In full at the October 17, 2025 communication date | 1,080 | 100 |
| Termination benefits — 7 employees serving to December 31 | 240 | Ratably over the retention period | — | 240 |
| Impairment of the Australia right-of-use asset (cease-use 12/12/25) | 380 | ASC 360-10-35; sublease market study | — | — |
| Contract termination — Australia facilities agreement | 100 | ASC 420-10; notice dated November 3, 2025 | — | 100 |
| **Total** | **1,900** | | **1,080** | **440** |

The exhibit foots and cross-foots ($1,900 − $380 non-cash − $1,080 paid = $440 accrued, within account 2200). Recompute
the benefit for 8 of the 41 employees from the plan formula, tenure, and base salary — the recomputation agreed within $2.
Agree the communication date to the email distribution log, because a date after year end would move the entire $1,420 of
termination benefits into FY2026, and test the 41 terminations against the Exhibit 10-7 separation list and the register
for post-separation payments. A separate caption is permitted under SAB Topic 5-P and Regulation S-X Rule 5-03, but the
disclosure must state amounts by major type of cost; check that it agrees to this exhibit and that the FY2026 reserve
roll-forward opens at $440.

## 10.11 Expense Classification and the Gross Margin Sensitivity

Classification is usually a low-priority assertion. In a SaaS audit it is not, because the number the market reads is
gross margin, and the line between cost of revenue and operating expense is drawn by a mapping table a controller can
change without a journal entry.

**Exhibit 10-17. Gross margin computed from the audited statements of operations (in thousands).**

| Measure | FY2025 | FY2024 | FY2023 |
| --- | --- | --- | --- |
| Total revenue | 148,200 | 118,900 | 91,500 |
| Total cost of revenue | 38,940 | 33,530 | 28,240 |
| **Gross profit** | **109,260** | **85,370** | **63,260** |
| **Total gross margin** | **73.72%** | **71.80%** | **69.14%** |
| Subscription gross margin | 80.00% | 78.63% | 77.45% |
| Professional services gross margin | 5.00% | 1.98% | (3.51%) |

Every figure is computed from the continuing case: 109,260 ÷ 148,200 = 73.72%; 85,370 ÷ 118,900 = 71.80%; 63,260 ÷ 91,500
= 69.14%, with the segment margins computed the same way from subscription revenue of $135,800, $108,300, and $82,100 and
professional services revenue of $12,400, $10,600, and $9,400. Total gross margin expanded 4.58 percentage points over two
years, and subscription gross margin landed at exactly 80.0%, a round number management discusses in MD&A. One basis point
of consolidated gross margin is $14.8 of cost, so an error of exactly performance materiality moves gross margin 63 basis
points, to 73.09%.

The consequence is a procedure. Compare the cost-center-to-caption mapping table at both year ends: six of AtlasFlow's 84
cost centers changed caption in FY2025, four mechanically as Kestrel cost centers mapped to equivalent functions. Two
require evidence — cost center 4120 "Platform Reliability" moved from cost of subscription to research and development in
March 2025 carrying $410, and 4260 "Customer Success Engineering" moved from sales and marketing to cost of subscription
in July 2025 carrying $290. Job descriptions and a sample of five employees' Jira and Zendesk activity support both moves:
Platform Reliability's work was 78% new-capability engineering, Customer Success Engineering's 91% post-go-live support.
Net effect on cost of revenue: $(120), or 8 basis points. Had Platform Reliability instead spent the year on incident
response, the $410 would be a misstatement improving the headline metric, and the AS 2810 qualitative evaluation would
matter more than the amount.

## 10.12 Travel, Purchase Cards, Related Parties, and the Vendor Master File

These areas carry $3,100 of expense, 1.8% of the total, and a disproportionate share of the fraud risk.

**Travel and entertainment (SAP Concur).** FY2025 T&E was $3,100 across 14,206 expense reports. Run five analytics over
the full population rather than sampling: hotel dates on Friday and Saturday nights in cities with no AtlasFlow customer
or office (71 reports, $84); clustering just below the $75 receipt threshold (118 items in the $70.00–$74.99 band
against 41 expected on a uniform distribution across $50–$100, a ratio of 2.9 to 1); duplicates matched on amount, date,
and merchant (24 items, $19); reports approved by a person reporting to the submitter (9 reports, $31); and
purchase-card transactions dated after the cardholder's separation (6 transactions on 6 of 212 cards, $11).

Aggregate quantified exposure is below the clearly trivial threshold, so the ICFR consequence is where the work pays.
Test the approval control on 45 reports: 3 deviations (2 self-approved through a delegate, 1 approved below the required
authority level). Three in 45 against a 5% tolerable rate gives an upper deviation limit of roughly 15% at a 5% risk of
overreliance, so the control cannot be relied on, and magnitude if it fails entirely is 6.7% of $3,100, or $208 — 22% of
performance materiality. Conclusion: a deficiency, not a significant deficiency, given the monthly budget-versus-actual
review by cost-center owners.

**Related-party expenses.** Match the vendor master against the director and officer questionnaires, the Carta shareholder
list, and the employee master on name and address. Two hits: Aurelia Design Studio, $84 of brand-design services, owned by
the spouse of the VP of Sales Operations; and Halstead Advisory LLC, $46 of market research, affiliated with a director's
family member. Aggregate $130 against specific materiality of $150 for related-party transactions, so no ASC 850-10
disclosure of individually significant transactions is required, and neither meets the $120,000 (whole dollars) Regulation
S-K Item 404 threshold. The absence of a disclosure is supportable under AS 2410 only if you performed and documented the
procedure.

**Vendor master file.** 4,182 vendor records, 1,096 with FY2025 activity. Six tests: duplicate tax identification numbers
(3 pairs, all parent and subsidiary billing separately); bank details matching an employee direct-deposit account (2, both
a converted contractor); bank-detail changes (47, callback verification retained for 41, so 6 deviations); P.O. box as
sole address (12, all lockboxes); vendors created and paid within 48 hours (9, all traced to an approved requisition); and
vendors with no tax identification number (23, $18 of spend, all foreign). The 6 bank-detail deviations are the finding,
graded within the Chapter 8, §8.12 payment fraud control set, and the magnitude is the largest payment that could have
been diverted — the $1,190 monthly AWS wire — not the historical loss.

## Step-by-Step Walkthrough: Performing the December 31, 2025 Search for Unrecorded Liabilities

Design decisions were made in §10.3: cut-off February 13, 2026; scope threshold $70; six sources; a 30-item sample
below the threshold. What follows is execution, at WP 3200-14.

**Step 1.** Prove the disbursement population before using it. Agree the NetSuite payment register for January 1 –
February 13, 2026 to debits to accounts 1010, 1015, and 1020 less identified non-vendor debits: register $14,830;
bank debits $47,210 less $32,380 = $14,830. A register *below* the reconciled bank figure means payments made outside
the payment run, and you extend to 100% of them.

**Step 2.** Extract the population with the fields you need rather than the report's defaults:

```sql
SELECT p.payment_date, p.amount_usd, v.vendor_name, b.invoice_number, b.invoice_date,
       b.gl_period_posted, b.po_number, b.cost_center, b.gl_account,
       b.service_period_start, b.service_period_end
FROM   ns_vendor_payment p
JOIN   ns_bill_payment_link l ON l.payment_id = p.payment_id
JOIN   ns_vendor_bill b       ON b.bill_id    = l.bill_id
JOIN   ns_vendor v            ON v.vendor_id  = b.vendor_id
WHERE  p.payment_date BETWEEN '2026-01-01' AND '2026-02-13';
```

The two fields that do the work are `gl_period_posted` and `service_period_end`: every exception is a row where the
second precedes December 31, 2025 and the first does not.

**Step 3.** Stratify. Items ≥ $70: 58 payments, $9,410, 63.5% of the population. Items < $70: 1,784 payments, $5,420.
Confirm the strata sum to $14,830 and tick mark (a) the stratification.

**Step 4.** Obtain the Coupa "Receipts Without Invoice" report at December 31 — 34 receipts, $1,180, of which 9 are ≥
$70 totaling $760 — and reperform it, because the standard report excludes receipts marked "closed short," the easiest
way to make a December obligation disappear. Reperformance produced the same 34 items.

**Step 5.** Obtain the open purchase order report filtered to a promised delivery date on or before December 31 with
no receipt and no invoice: 27 POs, $2,340 committed, 12 ≥ $70 totaling $1,690. Ask each requester one written
question — had the vendor performed by December 31? Eleven answered no with delivery confirmations dated January or
later; PO 20-4471 for Halverson came back as work done but deliverable rejected.

**Step 6.** Obtain the unvouchered invoice file — Coupa invoices dated on or before December 31 whose status is not
"Exported": 46 invoices, $1,620, of which 11 are ≥ $70 totaling $840. Read the 11 professional fee arrangements,
obtain a statement of account from each (aggregate FY2025 fees $1,845), and compare them to accrued professional fees
of $1,400 plus amounts already in accounts payable.

**Step 7.** Inquire of seven budget owners with a closed question: "list every good or service your team received on
or before December 31, 2025 for which you had not seen an invoice by January 15, 2026," and read the October and
December minutes. The General Counsel independently identified the Halverson dispute.

**Step 8.** Assemble the combined follow-up schedule. Of the 58 items ≥ $70, 48 ($6,908) cleared on the first pass by
agreeing the invoice date to on or before December 31 and the posting period to December 2025 or earlier.

**Exhibit 10-18. WP 3200-14 — items requiring follow-up (in thousands; source codes per Exhibit 10-4).**

| # | Src | Vendor | Amount | Service period | Recorded at 12/31 | Tick | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | S | Amazon Web Services | 1,190 | Dec 1–31, 2025 | 1,190 in 2200 | (b) | Cleared |
| 2 | S | Snowflake Inc. | 214 | Dec 2025 | 205 in 2200 | (b)(e) | $9; below CTT |
| 3 | S | Ridgeline Legal LLP | 96 | Nov 15 – Dec 31 | 96 in 2220 | (c) | Cleared |
| 4 | S | Brightline LLP | 310 | FY2025 audit | 240 in 2220 | (c)(d) | $70 is Jan 2026 fieldwork |
| 5 | S | Cascade Contract Eng. | 148 | Dec 2025 | 148 in 2200 | (b) | Cleared |
| 6 | S | Northwind Talent | 118 | Start date 01/12/26 | — | (d) | FY2026 obligating event |
| 7 | S | Fairmont Facilities | 84 | Dec 2025 | 84 in 2200 | (b) | Cleared |
| 8 | S | Corbett Media Buying | 172 | Jan 5 – Mar 31, 2026 | — | (d) | FY2026 service period |
| 9 | S | Datastride Analytics | 79 | Dec 2025 | 79 in the IT accrual | (b) | Cleared |
| 10 | S | Trellis Compliance | 91 | Oct 1 – Dec 31 | 91 in 2220 | (c) | Cleared |
| 11 | R | Vantage Hardware (GRN 44182) | 132 | Received 12/29/25 | 132 in GR/IR | (f) | Cleared |
| 12 | R | Orion Network (GRN 44207) | 76 | Received 12/30/25 | 76 via JE 48211 | (f) | Cleared; control operated |
| 13 | P | Halverson (PO 20-4471) | 110 | Nov 24 – Dec 18 | — | (g) | **U-5, $(110)** |
| 14 | V | Ellsworth Tax Advisors | 88 | Sep – Dec 2025 | 88 in 2220 | (c) | Cleared |
| 15 | V | Bramblewood Recruiting | 74 | Dec 2025 retainer | 74 in 2200 | (b) | Cleared |
| 16 | F | Sterling & Voss LLP | 145 | Oct 1 – Dec 31 | 145 in 2220 | (c) | Cleared |
| | | **Total** | **3,127** | | | | |

Tick marks: (a) stratification reperformed; strata foot to $14,830. (b) Agreed to the account 2200 accrual detail at
WP 3200-06 by vendor and amount. (c) Agreed to the firm's statement of account and the 2220 detail. (d) Service period
examined and determined to fall after December 31, 2025. (e) Below the $72 clearly trivial threshold. (f) Agreed to the
Coupa goods-receipt record and the GR/IR subledger. (g) See §10.5; adjustment declined.

**Step 9.** For every row, determine the *obligating event date* rather than the invoice date. Rows 4, 6, and 8 each look
like an unrecorded December liability until you read the document: the Brightline invoice covers interim review work plus
January fieldwork; the Northwind placement fee is earned when the candidate starts, January 12, 2026; the Corbett media
flight runs January through March 2026. Accruing all three would have overstated FY2025 expense by $360.

**Step 10.** For every cleared row, place tick mark (b), (c), or (f) and name the accrual line the item agrees to.
"Agreed to accrual" without naming the line is not evidence a reviewer can reperform.

**Step 11.** Investigate the exceptions. Row 2: the December 28 Snowflake invoice arrived January 5 against a run-rate
accrual, a $9 shortfall — clearly trivial, but scan the whole $412 IT services accrual for the same pattern, which produced
no further difference. Row 13: obtain the invoice, the purchase order, the Jira work log, and the January 8 rejection
email; confirm with the vendor; propose $110.

**Step 12.** Test the below-threshold stratum: 30 payments drawn at random from the 1,784 items under $70 ($412), Steps 9
and 10 performed on each. No misstatements; document the bound — a 1% undetected understatement rate across $5,420 is $54.

**Step 13.** Evaluate coverage and results.

**Exhibit 10-19. WP 3200-14 evaluation summary (in thousands).**

| Source | Population | Examined | Coverage | Misstatements |
| --- | --- | --- | --- | --- |
| S — subsequent disbursements | 14,830 | 9,822 | 66.2% | $9 (below CTT) |
| R — unmatched receipts | 1,180 | 760 | 64.4% | — |
| P — open POs | 2,340 | 1,690 | 72.2% | $110 (U-5) |
| V — unvouchered invoices | 1,620 | 840 | 51.9% | — |
| F — professional fee arrangements | 1,845 | 1,845 | 100.0% | — |
| **Total** | **21,815** | **14,957** | **68.6%** | **$119, of which $110 accumulated** |

The totals foot (14,830 + 1,180 + 2,340 + 1,620 + 1,845 = 21,815; 9,822 + 760 + 1,690 + 840 + 1,845 = 14,957; 14,957
÷ 21,815 = 68.6%); the S column comprises the 58 items ≥ $70 plus the 30-item sample. Against performance materiality
of $940 the $119 identified is tolerable, so completeness is supported.

**Step 14.** Conclude: "Based on the procedures above, covering 68.6% by value of the six populations at WP 3200-14.1
and all items above $70, we identified aggregate understatement of accrued liabilities of $119, of which $110 is
accumulated as U-5. We concluded that accrued liabilities and accounts payable at December 31, 2025 are complete within
performance materiality of $940."

**Step 15.** Communicate. Hand U-5 to whoever maintains the summary of uncorrected misstatements, with income and
balance sheet effects and the management response, and hand the row 12 observation — management's own GR/IR true-up
caught an item three weeks after year end — to the controls team, because a control that operates late is graded
differently from one that never operates.

## Extended Case Study: Auditing the $10,900 of FY2025 Capitalized Internal-Use Software When 22% of the Hours Were Restaged

### Background

AtlasFlow capitalized $10,900 of internal-use software cost in FY2025 (Exhibit 10-14). The capitalization rests on one
input: the project stage assigned to each Jira epic against which engineers log time, since application-development
hours are capitalized and preliminary-project and post-implementation hours are expensed. Section 4.3 records two facts
that make this a significant risk: 22% of the capitalized hours sat on epics whose stage designation was changed
*retroactively* during the year, and time reports are approved by the same engineering managers who own the projects'
budgets.

### The Facts

Engineers logged 498,200 hours in Jira during FY2025 across 286 time-reporting developers, of which 84,100 (16.9%)
were coded to capitalizable epics. The blended rate is $9,400 of capitalized personnel cost (payroll $7,200, taxes
and benefits $1,300, stock-based compensation $900) over 84,100 hours, or **$111.77 per hour**.

**Exhibit 10-20. Jira hours analysis, FY2025 capitalized internal-use software.**

| Measure | Hours | At $111.77/hour | % of additions |
| --- | --- | --- | --- |
| Total hours logged in Jira | 498,200 | n/a | n/a |
| Hours coded to capitalizable epics | 84,100 | 9,400 | 86.2% |
| Of which: epics restaged retroactively | 18,502 | 2,068 | 19.0% |
| Of which: stage unchanged since epic creation | 65,598 | 7,332 | 67.3% |
| Non-labor additions (contractors $900 + development cloud $600) | n/a | 1,500 | 13.8% |
| **Total FY2025 additions** | | **10,900** | **100.0%** |

The exhibit foots: 18,502 + 65,598 = 84,100 hours; $2,068 + $7,332 + $1,500 = $10,900. The restaged stratum of
$2,068 is 2.2 times performance materiality and 1.4 times overall materiality — the sentence that sets the scope. A
finding described as "22% of hours" is not auditable; "$2,068, or 143% of overall materiality" is. The self-review
characteristic compounds it: the manager who owns the project budget both sets the epic's stage and approves the time
reports that allocate hours to it, nobody reviews either input contemporaneously, and Jira does not require a
justification on a stage-field change.

### What the Engagement Team Did

The team requested the Jira epic change history (`issue_key`, `field`, `from_value`, `to_value`, `change_author`,
`change_timestamp`) for all epics with FY2025 capitalized hours, plus the worklog table. Because Jira is IPE, the IT audit
team first tested extract completeness against the Jira "Time Tracking" report and reperformed the pull two weeks later.

Forty-seven epics had a stage-field change dated after hours had been logged against them. The team selected 12 — the
largest by hours and the latest by change date, a risk-weighted rather than representative selection — covering 11,240
hours and $1,256, or 60.7% of the stratum, and for each requested the evidence that the preliminary project stage had ended
before the hours were incurred: a dated architecture decision record in Confluence, the CTO's stage-gate approval, and the
epic's GitHub commit history. Results: 7 epics (6,410 hours, $717) were supported by an architecture decision record
predating the first logged hour; 3 (3,180 hours, $355) had no contemporaneous evidence; and 2 (1,650 hours, $184) were
mixed. Unsupported: **$466 of the $1,256 examined, a 37.1% error rate**.

### Analysis

Projecting 37.1% across the $2,068 stratum gives $767 — 81.6% of performance materiality — and that forces three decisions.
Do not project a risk-weighted sample: the 12 epics were chosen because they looked worst, so $767 is a bound, not an
estimate. The result is not tolerable, so the team cannot conclude from the sample; under AS 2315 the response is to
extend, and where the stratum is small enough to examine entirely, extend to 100% rather than resample. And separate the
misstatement question from the control question.

### Resolution and Conclusion

The team examined 100% of the 47 restaged epics — 18,502 hours, $2,068. Management located dated architecture decision
records and CTO stage-gate approvals for 44 epics (16,092 hours, $1,799). For the remaining 3 (2,410 hours, $269), GitHub
commit history corroborated 1,890 hours as new functionality, and 520 hours ($58) were post-implementation maintenance,
which management reclassified to research and development before the trial balance was finalized. With the stratum examined
in full there is no projection, and $58 is below the clearly trivial threshold, so the $10,900 of additions is supported and
nothing is accumulated.

The control conclusion is a **significant deficiency**, not a material weakness. Maximum potential magnitude is the $10,900
of additions plus $5,700 of amortization, far above overall materiality, and likelihood is more than remote given
retroactive restaging with no required justification and a manager who both sets the stage and approves the hours. Three
factors keep it below a material weakness: the CTO's quarterly capitalization review operated in three of four quarters
over 82% of capitalized dollars; the Controller's review of capitalized cost per engineering hour caught two coding errors;
and the actual error on 100% examination was 4.0% of overall materiality. What would move the conclusion: failure of the
CTO review, an actual error above $1,450, restaging concentrated in the fourth quarter, or evidence that a restaging
decision followed a budget conversation.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                            WP 3400-22
AtlasFlow, Inc. — FY2025 Integrated Audit
Capitalized Internal-Use Software — Retroactively Restaged Jira Epics

Prepared by:  Jae-won Park (JP)            Date prepared:  February 4, 2026
Reviewed by:  Grace Lindqvist (GL)         Date reviewed:   February 9, 2026

PURPOSE
To conclude on valuation for the $10,900 of FY2025 additions to account 1560, and
specifically on the $2,068 of hours coded to epics whose ASC 350-40 stage designation
was changed after the hours were logged.

SOURCE OF INFORMATION
1. Jira epic change history extract, pulled January 14, 2026; completeness and accuracy
   tested at WP 3400-22.1. Jira worklog extract, FY2025, 498,200 hours.
2. Management's capitalization schedule "IUS_FY25_v6.xlsx" (IPE; tested at WP 3400-21).
3. Confluence architecture decision records; CTO stage-gate emails; GitHub commit logs.

PROCEDURES PERFORMED
1. Recomputed the blended capitalized labor rate: $9,400 / 84,100 hours = $111.77.   (a)
2. Identified 47 epics restaged after the first logged hour: 18,502 hours, $2,068
   (19.0% of additions; 143% of overall materiality of $1,450).                      (b)
3. Stage one - examined 12 risk-weighted epics (11,240 hours, $1,256; 60.7%).
   Unsupported $466 (37.1%). Bound on the stratum $767. Not tolerable.               (c)
4. Stage two - extended to 100% of the 47 epics, agreeing the end of the preliminary
   project stage to a dated architecture decision record and CTO stage-gate approval
   predating the first logged hour; where absent, examined GitHub commits to
   distinguish new functionality from maintenance.                                (d)(e)
5. Reperformed the hours-to-dollars extension; agreed to account 1560 additions.     (f)

RESULTS
                                                   Epics    Hours      Amount
   Restaged, supported by ADR + stage gate            44    16,092      1,799
   Restaged, supported by GitHub commit only           3     1,890        211
   Restaged, determined to be maintenance              -       520         58
                                                     ---    ------      -----
   Total restaged stratum                             47    18,502      2,068
   Non-restaged capitalized hours                            65,598      7,332
   Non-labor additions (contractors, development cloud)                  1,500
                                                                       ------
   Total FY2025 additions per account 1560                             10,900

   Misstatement identified 58; clearly trivial threshold 72; recorded by management in
   JE 48377 before finalization of the trial balance.

TICK MARKS
(a) Recomputed; agrees to WP 3400-21 payroll allocation.  (b) Change-history filter
reperformed independently in Python; 47 epics, no difference.  (c) Risk-weighted sample
not projected.  (d) 100% examination; no sampling risk.  (e) Exceptions at WP 3400-22.3.
(f) Footed to the Exhibit 10-13 roll-forward.

CONCLUSION
The $10,900 of additions is supported after the $58 reclassification. The retroactive
restaging, with no independent review of stage designations and time allocations
approved by the budget-owning engineering manager, is a control deficiency; weighing
maximum potential magnitude of $10,900 against overall materiality of $1,450 and the
mitigating CTO quarterly capitalization review and Controller cost-per-hour review, it
is a SIGNIFICANT DEFICIENCY and not a material weakness. Communicated at WP 1200-08.
```

### Lessons

Convert percentages into dollars before you scope. Do not project a risk-weighted sample — the result is a bound, and
the response is to extend, not extrapolate; where the suspect stratum is small enough, 100% examination is cheaper and
stronger than a second sample. And keep the misstatement conclusion separate from the control conclusion: here they
were $58 and a significant deficiency.

## Common Mistakes

### Mistake 10.1 — Testing completeness by sampling the recorded invoice population

**What it looks like.** A 45-item sample from the 18,410 supplier invoices, concluding on "existence, accuracy, and
completeness."
**Why it happens.** The revenue methodology applied by reflex.
**What goes wrong.** The frame excludes every unrecorded liability by construction; U-5 could not appear in it.
**How to avoid it.** Choose the population after naming the assertion, and start outside the accounting records.

### Mistake 10.2 — Using performance materiality as the search scope threshold

**What it looks like.** "We examined all subsequent disbursements above $940."
**Why it happens.** Confusing an aggregation tolerance with an item-selection rule.
**What goes wrong.** Twelve unrecorded $900 invoices aggregate to $10,800 and none is selected.
**How to avoid it.** Set the threshold at or just below the clearly trivial threshold and sample below it.

### Mistake 10.3 — Confirming the largest accounts payable balances

**What it looks like.** Requests to the eight largest recorded balances, presented at the recorded amount.
**Why it happens.** Habit from the receivable confirmation.
**What goes wrong.** Recorded balances are what you doubt least; a vendor with $0 recorded and $110 claimed is invisible.
**How to avoid it.** Use the blank form and select on activity and dispute history, including nil balances.

### Mistake 10.4 — Ending the search at January 31 because the close is done

**What it looks like.** A cut-off chosen to match the January close calendar.
**Why it happens.** Convenience, and no analysis of the payment lag.
**What goes wrong.** With a 52-day 90th-percentile lag it misses roughly 10% of December obligations by count.
**How to avoid it.** Compute the lag distribution, set the cut-off past the median, and document the statistic.

### Mistake 10.5 — Proposing management's query result as the adjustment

**What it looks like.** "Management identified $1,900 of capitalized commissions for churned customers; we propose a
$1,900 write-off."
**Why it happens.** Management's schedule looks like an answer.
**What goes wrong.** Only $620 was impaired, so the proposal overstates expense by $1,280.
**How to avoid it.** Treat the population definition as IPE — disaggregate into cohorts and test the period of
benefit in each.

### Mistake 10.6 — Leaving a finding expressed as a percentage of hours

**What it looks like.** A memo stating that "22% of capitalized hours were restaged," with no dollar amount.
**Why it happens.** The client's schedule presents the statistic that way.
**What goes wrong.** Nobody can scope from it; 18,502 hours at $111.77 is $2,068, or 143% of overall materiality.
**How to avoid it.** Convert every rate into dollars and compare it to materiality before deciding anything.

### Mistake 10.7 — Projecting a risk-weighted sample

**What it looks like.** "We tested 12 epics, found a 37.1% error rate, and project $767."
**Why it happens.** The projection arithmetic looks the same however items were chosen.
**What goes wrong.** The epics were selected because they looked worst, so the figure is a bound, not an estimate.
**How to avoid it.** Project only from representative selections; when a directed sample is intolerable, extend — to
100% where the stratum permits.

### Mistake 10.8 — Accepting a bonus accrual without the funding input

**What it looks like.** A workpaper tying the accrual to management's schedule and the prior-year ratio.
**Why it happens.** The pool arithmetic is easy; funding requires evidence from outside accounting.
**What goes wrong.** The plausible 70%–80% range spans $880, so you have audited the multiplication, not the estimate.
**How to avoid it.** Obtain the approved funding percentage, agree the metrics to audited results, and confirm the
subsequent payment.

### Mistake 10.9 — Testing the amounts on the standing accrual list instead of the list

**What it looks like.** Every line on the accrual schedule agreed to a calculation, concluding completeness.
**Why it happens.** The list is what management gives you.
**What goes wrong.** A category that never appears on the list is never tested; completeness is a property of the
list, not its lines.
**How to avoid it.** Reconcile the list to the prior-year list, the commodity codes with FY2025 spend, and the
subsequent-disbursements population.

### Mistake 10.10 — Dismissing classification because it does not change net loss

**What it looks like.** A $410 cost-center remapping passed as "no net income effect."
**Why it happens.** Quantitative materiality applied to the bottom line.
**What goes wrong.** $410 is 28 basis points of gross margin and moves the metric featured in MD&A; under AS 2810
that can be material below the quantitative threshold.
**How to avoid it.** Compute the gross margin effect of every classification change and evaluate it qualitatively.

## Practice Exercises

### Exercise 10-1 [Foundational]

Using Exhibit 10-17, compute total gross margin for FY2023, FY2024, and FY2025 to two decimals, and compute the cost
that must move from cost of revenue to operating expense in FY2025 to raise total gross margin to exactly 74.00%.

### Exercise 10-2 [Foundational]

A payroll register shows 618 active US employees and a Deel roster shows UK 74, Australia 40, India 101. Eleven US,
three UK, and two Australian employees separated on or before December 31, 2025 with final pay in the December run;
three US employees started December 30 and were first paid in January 2026. Prepare the headcount reconciliation.

### Exercise 10-3 [Foundational]

Recompute the US portion of the paid-time-off accrual at an average accrued balance of 7.1 days rather than 6.4,
holding the 604 headcount, $0.532 daily cost, and 8.0% burden constant. State the difference from the $2,221 in
Exhibit 10-9 and whether it exceeds the $72 clearly trivial threshold.

### Exercise 10-4 [Intermediate]

December 2025 ACV bookings were $34,200. Assume the new-and-expansion share was 74% rather than 69%, with rates of
11.8% on new business, 3.1% on renewals, and a 0.25% override on all December ACV. Recompute the December commission
component, compare it to the recorded $3,240, and state whether the difference requires investigation.

### Exercise 10-5 [Intermediate]

Capitalized internal-use software was $13,400 net at December 31, 2024 and $18,600 net at December 31, 2025. FY2025
additions were $10,900, retirements of fully amortized assets $1,400, and gross cost at year end $31,200. Prepare the
roll-forward and derive FY2025 amortization expense.

### Exercise 10-6 [Intermediate]

Cohort B in Exhibit 10-12 carries $430 across 58 customers, of which 17 carrying $178 had no executed renewal at the
report date but stood at Salesforce stage "Contract Sent." Conclude in three to five sentences on whether the $178
should be impaired, with the authoritative hook and one credible alternative view.

### Exercise 10-7 [Intermediate]

Halverson invoiced $110 on December 19, 2025 under a time-and-materials purchase order with no acceptance condition;
AtlasFlow rejected the deliverable on January 8, 2026; two prior disputes settled at roughly 45%. State the amount you
would propose, the ASC reference, and the evidence that would change your answer.

### Exercise 10-8 [Advanced]

Using the case study facts — 47 restaged epics, $2,068, a 100% examination producing $58 of misstatement, a CTO
quarterly review that operated in three of four quarters over 82% of dollars, and a Controller cost-per-hour review
that caught two errors — grade the deficiency under AS 2201, showing the magnitude and likelihood reasoning and two
facts that would change your conclusion.

### Exercise 10-9 [Intermediate]

Draft the conclusion paragraph for the search at WP 3200-14 from the Exhibit 10-19 figures, naming the assertion, the
populations, the coverage, the scope threshold, the identified misstatement, and the comparison to performance
materiality.

### Exercise 10-10 [Intermediate]

Draft a blank-form accounts payable confirmation request to Halverson Consulting Group at December 31, 2025, under
AtlasFlow letterhead with responses returned to Brightline LLP, including the reply-to instruction and what you want
to know about disputed invoices.

### Exercise 10-11 [Advanced]

A staff workpaper reads: "Search for unrecorded liabilities. We obtained the check register for January 2026 and
selected all 22 payments over $940. All 22 were traced to invoices dated in January 2026 and therefore relate to
FY2026. We also inquired of the Controller, who confirmed there are no unrecorded liabilities. Conclusion: accrued
liabilities are complete." Identify at least five defects and state the correction for each.

### Exercise 10-12 [Advanced]

Chapter 9 records FY2025 stock-based compensation *expense* of $28,700 (cost of revenue $2,100, R&D $11,400, S&M
$7,600, G&A $7,600); Exhibit 10-14 shows $900 capitalized into internal-use software. Compute total FY2025
stock-based compensation cost incurred, state where each component appears, and explain how the $900 would be tested
differently from the $28,700.

## Solutions to Practice Exercises

### Solution 10-1

FY2023: 63,260 ÷ 91,500 = **69.14%**. FY2024: 85,370 ÷ 118,900 = **71.80%**. FY2025: 109,260 ÷ 148,200 = **73.72%**.
For 74.00%, required gross profit is 148,200 × 0.7400 = $109,668, so cost of revenue must fall to $38,532 — a
reduction of **$408**, or 28% of overall materiality.

### Solution 10-2

| Item | US | UK | AU | India | Total |
| --- | --- | --- | --- | --- | --- |
| Per payroll systems | 618 | 74 | 40 | 101 | 833 |
| Less separations with final pay in December | (11) | (3) | (2) | — | (16) |
| Add late-December hires first paid in January | 3 | — | — | — | 3 |
| **Headcount at December 31, 2025** | **610** | **71** | **38** | **101** | **820** |

Columns foot (618 − 11 + 3 = 610; 74 − 3 = 71; 40 − 2 = 38) and the total is **820** (833 − 16 + 3).

### Solution 10-3

Base accrual: 604 × 7.1 = 4,288.4 days × $0.532 = $2,281; with the burden, 2,281 × 1.08 = **$2,463**. The difference
from $2,221 is **$242**, 3.4 times the clearly trivial threshold, so it would be accumulated. A 0.7-day change
producing a $242 swing tells you the day balances, not the rates, are the input to test hardest.

### Solution 10-4

New and expansion: 34,200 × 0.74 = $25,308 at 11.8% = $2,986. Renewals: 34,200 × 0.26 = $8,892 at 3.1% = $276.
Overrides: 34,200 × 0.0025 = $86. Total **$3,348**, so recorded $3,240 is $108 *below* the recomputation. That
exceeds the $72 threshold and runs the wrong direction — accelerators should make the recorded amount exceed a
base-rate recomputation — so investigate by tracing the January 30, 2026 payment file to bookings month and
confirming that commissions on the $25,174 of ACV signed December 24–31 were accrued.

### Solution 10-5

| Component | Gross | Accumulated amortization | Net |
| --- | --- | --- | --- |
| December 31, 2024 | 21,700 | (8,300) | 13,400 |
| Additions | 10,900 | — | 10,900 |
| Retirements | (1,400) | 1,400 | — |
| Amortization | — | (5,700) | (5,700) |
| **December 31, 2025** | **31,200** | **(12,600)** | **18,600** |

Derivation: opening gross = 31,200 − 10,900 + 1,400 = 21,700; opening accumulated = 21,700 − 13,400 = 8,300;
amortization = 13,400 + 10,900 − 18,600 = **$5,700**; closing accumulated = 8,300 − 1,400 + 5,700 = 12,600.

### Solution 10-6

Do not impair the $178. ASC 340-40 compares carrying amount to the remaining consideration expected less the direct
costs of providing the services, over the *expected* rather than contractual period of benefit; 17 customers at a late
renewal stage are evidence of expected consideration, and 91% gross retention makes non-renewal the exception. The
credible alternative — impair all $178 because no enforceable right exists at the report date — substitutes a contractual
test for the expected-benefit test. Either way $178 is 12.3% of overall materiality.

### Solution 10-7

Propose **$110** under ASC 450-20. The obligating event — receipt of 640 hours evidenced in the Jira work log —
occurred before December 31, 2025, and the purchase order is time-and-materials with no acceptance condition, so the
contractual entitlement is the full invoice; the $50 low end reflects a possible future negotiation rather than
measurement uncertainty at the balance sheet date. A settlement executed before the report date would change the
answer to the settlement amount.

### Solution 10-8

Magnitude: the control is the only one over the $10,900 of additions, 7.5 times overall materiality, and it also drives
the amortization those additions carry forward. Likelihood: more than remote, because 47 epics were
restaged with no required justification and the approving manager owns the budget. Together these clear the
significant deficiency threshold but stop short of a material weakness, because two independent controls operated
(the CTO quarterly review in three of four quarters over 82% of dollars and the Controller's cost-per-hour review,
which caught two errors) and 100% examination produced $58 of error, 4.0% of overall materiality. Conclusion:
**significant deficiency**, changing on failure of the CTO review in the fourth quarter or on evidence that a
restaging decision followed a budget conversation.

### Solution 10-9

"We performed a search for unrecorded liabilities at December 31, 2025 directed at the completeness of accounts payable
and accrued liabilities. We defined six populations at WP 3200-14.1 — subsequent disbursements through February 13, 2026,
unmatched Coupa receipts, open purchase orders with a delivery date on or before December 31, the unvouchered invoice
file, eleven professional fee arrangements, and inquiry of seven budget owners — aggregating $21,815, and examined all
items above a scope threshold of $70 plus a 30-item random sample below it, covering $14,957, or 68.6% by value. We
identified aggregate understatement of $119: a $9 difference on the December Snowflake invoice, below the clearly trivial
threshold of $72, and a $110 unrecorded liability to Halverson Consulting Group, accumulated as U-5. Against performance
materiality of $940, we concluded that accounts payable and accrued liabilities are complete."

### Solution 10-10

```text
[AtlasFlow, Inc. letterhead]                                     January 12, 2026

Halverson Consulting Group — Attention: Accounts Receivable

Our independent auditors, Brightline LLP, are auditing our financial statements
for the year ended December 31, 2025. Please provide directly to them, and not to
us, the following as of December 31, 2025:

  1. The total amount, if any, that AtlasFlow, Inc. owed your firm at the close of
     business on December 31, 2025, whether or not invoiced by that date.
  2. A statement of account listing each open invoice by number, date, and amount,
     and each unbilled amount for services performed on or before that date.
  3. For any invoice you understand to be disputed, the invoice number, the amount
     claimed, and the date of your most recent communication with us.
  4. Any deposits, retainers, or credits held on our account.

Please reply directly to Brightline LLP, Attention: Jae-won Park, 700 Congress
Avenue, Austin, Texas. Do not send your reply to AtlasFlow, Inc. This is not a
request for payment.

Elena Vasquez, Chief Accounting Officer and Controller
```

### Solution 10-11

Six defects. The population is one month rather than through the date fieldwork is substantially complete; extend to
February 13, 2026, because the 90th-percentile lag is 52 days. The $940 threshold is performance materiality, not a
scope threshold; lower it to $70. The check register omits ACH and wire payments, unmatched receipts, open purchase
orders, unvouchered invoices, and fee arrangements; add all five. The test applied is the *invoice* date, but the
obligating event is the service or delivery date — an invoice dated January 2026 for December services is exactly the
misstatement the procedure exists to find. Inquiry of one person is not sufficient, and the Controller is not the person
who knows what was received. And the conclusion states no coverage or threshold, so it cannot be reperformed.

### Solution 10-12

Total cost incurred is $28,700 + $900 = **$29,600**. The $28,700 appears across four captions in the statement of
operations and is added back in operating cash flow; the $900 sits inside capitalized internal-use software and
reaches the statement of operations only through the $5,700 of amortization, mostly in cost of subscription revenue.
Chapter 9 tests grant-date fair value, service inception, attribution, and forfeitures for the $28,700; for the $900
those inputs are already tested, so the incremental risk is entirely allocation — whether the hours to which the rate
was applied belong in the application development stage. Reperform the extension ($900 is part of the $9,400 pool at
$111.77 per hour over 84,100 hours) and agree the capitalizing employees to the Carta grant extract.

## Review Questions

**RQ 10-1.** Why is completeness rather than existence the dominant assertion for expenses and accrued liabilities?

**RQ 10-2.** Name the six sources used in the December 31, 2025 search and state which catches an obligation received
but never invoiced.

**RQ 10-3.** Why is the scope threshold set at $70 rather than at performance materiality of $940?

**RQ 10-4.** What determines how far past year end the subsequent-disbursements review extends?

**RQ 10-5.** Neither AS 2310 nor AU-C 505 requires accounts payable confirmation. Name three situations in which
sending one is nevertheless the better evidence.

**RQ 10-6.** Why does the confirmation use the blank form and target small or nil balances?

**RQ 10-7.** A payment recorded in the wrong period has no income statement effect. Why test disbursement cut-off?

**RQ 10-8.** What does the "commensurate" test in ASC 340-40 decide, and what does AtlasFlow's 3.1% versus 11.8%
comparison establish?

**RQ 10-9.** Why is the $1,900 of capitalized costs relating to non-renewed contracts not equal to the $620 recorded
as corrected misstatement C-3?

**RQ 10-10.** Under ASC 350-40, what event must have occurred before engineering hours become capitalizable, and what
evidence establishes it?

**RQ 10-11.** Distinguish ASC 420-10 from ASC 712-10 and state which governs AtlasFlow's October 2025 restructuring.

**RQ 10-12.** Why does the $380 Australia lease charge fall under ASC 360-10-35 rather than being a cease-use
liability?

**RQ 10-13.** How does ASU 2018-15 change the *presentation* of amortization of capitalized hosting implementation
costs, and why does that matter here?

**RQ 10-14.** Why is expense classification a relevant assertion at AtlasFlow when it has no effect on net loss?

**RQ 10-15.** What is the sensitive input in the FY2025 bonus accrual, and what evidence resolves it?

## Answers to Review Questions

**A 10-1.** Deferring cost improves earnings and gross margin, so the misstatement sought is an absent record, which
existence testing cannot detect.

**A 10-2.** Subsequent disbursements, unmatched receipts, open purchase orders, the unvouchered invoice file, fee
arrangements, and inquiry. Open purchase orders catch a service received but never invoiced, as Halverson was.

**A 10-3.** $940 is an aggregation tolerance for the statements as a whole; selecting on it would leave many
sub-threshold invoices untested.

**A 10-4.** The lag distribution and the date fieldwork is substantially complete: a 34-day median, a 52-day 90th
percentile, and a February 20, 2026 report date.

**A 10-5.** No vendor statements; a nil recorded balance on an active relationship; a disputed invoice whose claimed
amount is the measurement input.

**A 10-6.** The blank form does not present the amount in doubt, and missing liabilities hide behind small balances —
Halverson's $110 against $0 recorded.

**A 10-7.** It misstates cash, accounts payable, and the current ratio, and a pattern of such items signals window
dressing.

**A 10-8.** Whether the initial commission relates only to the initial contract; at 3.1% against 11.8% it does not,
so the four-year expected period of benefit applies.

**A 10-9.** The $1,900 is a query result and the $620 the impaired subset; the $1,280 difference is post-year-end
renewals ($430), month-to-month continuation ($510), and a Salesforce defect ($340).

**A 10-10.** The preliminary project stage must have ended — authorization, technology selection, alternatives
evaluated — evidenced by a dated architecture decision record, an independent stage gate, and commit history.

**A 10-11.** ASC 420-10 covers one-time benefits recognized on communication; ASC 712-10 covers ongoing arrangements
and accrues earlier. With no handbook schedule and one dissimilar 2020 precedent, ASC 420-10 governs.

**A 10-12.** Under ASC 842 the asset and liability are already recorded, so ceasing use creates no new obligation;
abandonment triggers an ASC 360-10-35 impairment, here $380.

**A 10-13.** In the same line as the hosting fee rather than depreciation and amortization; because hosting sits
partly in cost of revenue, misplacement shifts cost across the gross margin line.

**A 10-14.** Gross margin is the metric MD&A emphasizes, set by a mapping table that changes without a journal entry;
$408 moves it 28 basis points, which AS 2810 can make material below the quantitative threshold.

**A 10-15.** The funding percentage — five points is $440 — resolved by the February 3, 2026 approval at 75% and the
$6,570 paid February 27.

## Key Definitions

**Accrual.** A liability for goods or services received before the balance sheet date and not yet invoiced; an
estimate, and therefore subject to AS 2501.

**Accrued paid time off.** The liability for compensated absences meeting the ASC 710-10-25 criteria: services
rendered, rights vesting or accumulating, payment probable and estimable.

**Commensurate renewal commission.** A renewal commission bearing a reasonable relationship to the initial commission
relative to contract values; where it is not, the initial commission amortizes over the expected period of benefit.

**Disbursement cut-off.** The determination that a payment is recorded in the period it left the entity's control,
evidenced by the positive-pay date, ACH timestamp, or wire confirmation.

**Expenditure cycle.** Requisition, approval, purchase order, receipt, invoice, matching, posting, and payment — the
process by which an entity commits to and pays for goods and services.

**Goods received / invoice received (GR/IR) account.** A clearing account credited on receipt and debited when the
invoice posts; its reporting-date balance is a population of obligations received but not invoiced.

**Hosting arrangement that is a service contract.** A cloud arrangement conveying no software license, whose
implementation costs follow ASC 350-40 with amortization in the same line as the hosting fee.

**Incremental cost of obtaining a contract.** A cost that would not have been incurred had the contract not been
obtained — commission, override, employer taxes on both — as distinct from base salary.

**Internal-use software.** Software developed to meet the entity's internal needs, including a multi-tenant platform
used to deliver a hosted service, accounted for under ASC 350-40.

**Non-PO invoice.** A supplier invoice with no purchase order and therefore no three-way match — 3,604 of AtlasFlow's
18,410 FY2025 invoices.

**One-time termination benefit.** A benefit for involuntarily terminated employees under a plan for a specified event,
recognized under ASC 420-10 on communication or over a required service period.

**Period of benefit.** The ASC 340-40 amortization period for a capitalized contract cost, set by the expected rather
than contractual customer relationship; AtlasFlow uses four years.

**Preliminary project stage.** The ASC 350-40 stage of evaluating alternatives, selecting technology, and authorizing
the project; costs are expensed and capitalization begins when it ends.

**Restructuring.** Exit or disposal activities involving termination benefits and contract termination costs,
recognized under ASC 420-10 and, for affected assets, ASC 360-10-35.

**Search for unrecorded liabilities.** Procedures directed at completeness of accounts payable and accrued
liabilities that begin from populations outside the accounting records.

**Self-review characteristic in control design.** A design flaw in which the person who performs or benefits from a
transaction also approves it — here, a budget-owning manager setting an epic's stage.

**Subsequent disbursements review.** Examination of post-reporting-date payments to determine whether the obligating
event preceded it; the largest search source, but blind to a disputed unpaid item.

**Three-way match.** The automated comparison of purchase order, receipt, and invoice within configured tolerances;
it addresses accuracy and existence and does nothing for completeness.

**Unvouchered invoice file.** Supplier invoices dated on or before the reporting date, received but not posted — the
entity's own record of its own unrecorded liabilities.

**Vendor master file.** The repository of vendor identity, remittance, tax, and banking data, whose risks are
duplicates, unverified bank-detail changes, matches to employee data, and vendors created and paid at once.

## Chapter Summary

1. The $172,440 of FY2025 expense is $71,100 of cash personnel cost, $28,700 of stock-based compensation, $20,500 of
   depreciation and contract-cost amortization, and $52,140 of third-party spend; plan by process, not by caption.
2. Completeness dominates because the incentive to defer cost is unidirectional, so sampling the recorded population
   cannot address it.
3. Designing the search is four decisions, each defended with a number: February 13, 2026 from a 52-day
   90th-percentile lag, a $70 threshold from the $72 clearly trivial threshold, six sources, and a sample below it.
4. That search covered 68.6% of $21,815 and identified $119 of understatement, of which the $110 Halverson invoice is
   accumulated as U-5.
5. Accounts payable confirmation is required by neither AS 2310 nor AU-C 505; where used, the form is blank and the
   targets are nil or disputed balances.
6. Reconciling the ADP and Deel registers to the 812-employee disclosure (824 less 14 separations plus 2 hires) tests
   register completeness, terminations, and an Item 1 disclosure at once.
7. One judgment is sensitive in each compensation accrual: 75% bonus funding ($440 per five points), the PTO day
   balances ($242 per 0.7 days), and whether December 24–31 bookings sit in the $4,800 commission accrual.
8. Renewal commissions at 3.1% against 11.8% are not commensurate, making four years required rather than optional;
   three to six years is defensible, and a one-year extension moves amortization $1,050.
9. The $1,900 of non-renewed-contract costs reconciles to the $620 of C-3 through three cohorts — $430 renewed after
   year end, $510 still consuming, $340 a query defect — so the query result would have overstated expense by $1,280.
10. Converting "22% of hours" into $2,068, or 143% of overall materiality, makes the software risk scopable; the
    risk-weighted 37.1% error rate is a bound, and 100% examination produced $58 and a significant deficiency.
11. The restructuring is ASC 420-10: $1,180 at communication, $240 over the retention period, a $380 right-of-use
    impairment, and $100 of contract termination cost, leaving $440 accrued.
12. Gross margin of 69.14%, 71.80%, and 73.72% makes classification relevant at $14.8 per basis point; grading the
    T&E deficiency takes the same arithmetic — 3 deviations in 45, a 15% upper limit, $208 of magnitude.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Materiality figures ($1,450, $940, $72, $150) | Chapter 3 | Every threshold here derives from them |
| Cash disbursement controls, dual wire authorization | Chapter 8, §8.12 | The payment-side controls assumed tested |
| Stock-based compensation, including the $900 capitalized | Chapter 9 | Grant-date fair value; the $28,700 by line |
| Coupa and Concur IT general controls | Chapter 11 | Access, change management, SOC 1 deviations |
| Coupa match configuration and the March 2024 policy gap | Chapter 12, §12.4 | Tolerances and invoice volumes |
| Journal entries used to manipulate accruals | Chapter 16 | The W-12 approval threshold |
| Evaluation of U-5 and aggregation of misstatements | Chapter 19 | The summary of uncorrected misstatements |
| ARR, NRR, and other information in MD&A | Chapter 20 | Why gross margin classification is sensitive |

## Further Reading

- PCAOB AS 2110 and AS 2301 for the link between the completeness assertion and the design of the search; AS 2315 for
  the sampling and extension decisions; AS 2501 for the bonus, PTO, and period-of-benefit judgments; AS 2201 and AS 1305
  for grading the deficiencies; AU-C 330, 505, 520, 540, and 265 for the private-company equivalents.
- PCAOB AS 2310, *The Auditor's Use of Confirmation*, effective for fiscal years ending on or after June 15, 2025, for
  what it requires and, equally important, what it does not.
- FASB ASC 340-40 for costs to obtain a contract, with the ASU 2014-09 basis for conclusions on the period of benefit;
  ASC 350-40 and ASU 2018-15 for internal-use software and hosting implementation costs; ASC 420-10, 712-10, 710-10-25,
  and 450-20 for exit costs, ongoing-arrangement benefits, compensated absences, and the disputed invoice.
- SEC SAB Topic 5-P and Regulation S-X Rule 5-03 for restructuring presentation and captions; Regulation S-K Item 404
  for related-person transactions.
