# Chapter 9 — Equity, Stock-Based Compensation, and Convertible Instruments

> Equity is the section of a SaaS balance sheet where the captions are small and the exposure is not. AtlasFlow's
> common stock line is $5; its additional paid-in capital moved $60,700, its stock-based compensation charge of
> $28,700 exceeds the operating loss, and one change in one estimate produced a $1,340 credit in the quarter that
> most needed it. Nothing here is testable from a bank statement; everything here is testable by rebuilding a
> schedule from unit-level records.

## Learning Objectives

- **LO 9.1** Build a footing equity roll-forward and reconcile it to the general ledger and the statement of
  stockholders' equity.
- **LO 9.2** Reconcile the capitalization table to the general ledger, the transfer agent, and the earnings per share
  denominator.
- **LO 9.3** Distinguish grant date, service inception date, measurement date, and requisite service period, and
  determine the attribution period each implies.
- **LO 9.4** Evaluate expected term, volatility, risk-free rate, and dividend yield, and quantify expense sensitivity
  to each.
- **LO 9.5** Compute the accounting and cash-flow consequences of net share settlement of restricted stock units.
- **LO 9.6** Distinguish a performance condition from a market condition, select the correct measurement mechanic
  for each, and compute the cumulative catch-up for a change in expected payout.
- **LO 9.7** Recompute employee stock purchase plan expense under a six-month look-back with a 15% discount and
  identify the events that constitute a modification.
- **LO 9.8** Reconcile stock-based compensation by expense line and evaluate its capitalization into internal-use
  software.
- **LO 9.9** Recompute effective-interest amortization of convertible note issuance costs and conclude on the
  classification of capped calls.
- **LO 9.10** Compute basic and diluted earnings per share under the treasury stock and if-converted methods and
  conclude on antidilution in a loss year.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| FASB ASC | ASC 718-10 | Grant-date measurement, service inception date, attribution over the requisite service period, probable-outcome accrual for performance conditions, and market conditions in fair value |
| FASB ASC | ASC 718-20 | Equity-classified awards, including modifications, cancellations, and replacements |
| FASB ASC | ASC 718-740 | Income tax effects; excess benefits and deficiencies run through the provision, not APIC |
| FASB ASC | ASC 470-20 and ASU 2020-06 | A single liability unit of account unless separation is required, with issuance costs amortized to interest expense; AtlasFlow's September 2024 notes were never subject to the cash conversion model |
| FASB ASC | ASC 815-40 | Indexed-to-own-stock analysis for capped calls, warrants, and conversion features |
| FASB ASC | ASC 260-10 | Treasury stock and if-converted methods, and the requirement to exclude antidilutive securities |
| SEC | Regulation S-X Rules 5-02 and 3-04 | Capital account captions and the statement of changes in stockholders' equity |
| SEC staff | Staff Accounting Bulletin Topic 14 | Staff views on valuation assumptions, including the conditions for the simplified method and peer-group volatility |
| PCAOB | AS 2501 | Auditing estimates and fair value measurements: the method, data, and significant assumptions, and indicators of bias |
| PCAOB | AS 1210 and AS 1105 | Using an auditor-engaged specialist for the Monte Carlo work, and the Carta extract as information produced by the entity |
| PCAOB | AS 2110 and AS 2201 | Risks in the equity process and controls over grant approval, Carta access, and the calculation |
| AICPA | AU-C 540, AU-C 620, AU-C 500 | Private-company analogues for estimates, specialists, and information produced by the entity |

Because AtlasFlow is an SEC issuer, PCAOB standards govern; for a private SaaS company substitute AU-C 540 for
AS 2501 and AU-C 620 for AS 1210. AU-C 540 requires the auditor to assess inherent risk by separately considering
estimation uncertainty, complexity, and subjectivity, where AS 2501 frames the same evidence around method, data, and
assumptions; and a private company lacks the observable share price that makes AtlasFlow's measurement easy, so
valuing the underlying share becomes the dominant issue.

## Prerequisites and Chapter Dependencies

Read Chapter 2 (risk assessment), Chapter 3 (materiality — this chapter uses overall materiality of $1,450,
performance materiality of $940, and a clearly trivial threshold of $72), and Chapters 11 and 12 (general and
application controls over Carta and NetSuite) first. Chapter 10 owns payroll, Chapter 8 owns financing cash flows, and
Chapter 12 owns the Carta application controls. Chapters 16, 17, and 19 build on the case study developed here.

## 9.1 The Equity Roll-Forward as the Organizing Document

Build the roll-forward yourself, from the prior-year audited balances forward, before you look at management's
version. It is the population definition for the whole section, and once it foots, every remaining procedure is a
test of one line in it.

**Exhibit 9-1. AtlasFlow, Inc. — FY2025 statement of stockholders' equity, as rebuilt by the engagement team
(in thousands; shares in thousands).**

| Line | Shares | Common stock | APIC | AOCI | Accumulated deficit | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Balance, December 31, 2024 (a) | 49,610 | 5 | 351,600 | (1,455) | (382,700) | (32,550) |
| Net loss | — | — | — | — | (21,400) | (21,400) |
| Other comprehensive income (b) | — | — | — | 350 | — | 350 |
| Stock-based compensation expense (c) | — | — | 28,700 | — | — | 28,700 |
| Stock-based compensation capitalized into internal-use software (d) | — | — | 1,900 | — | — | 1,900 |
| Option exercises, 610 shares at $19.20 weighted-average exercise price (e) | 610 | — | 11,712 | — | — | 11,712 |
| RSU vesting, net of 117 shares withheld for taxes (f) | 1,489 | — | (3,973) | — | — | (3,973) |
| ESPP issuances, two purchase dates (g) | 133 | — | 3,561 | — | — | 3,561 |
| Pre-funded warrants issued April 2025, net of $180 of issuance costs (h) | — | — | 18,800 | — | — | 18,800 |
| Capped call transactions (i) | — | — | — | — | — | — |
| **Balance, December 31, 2025** | **51,842** | **5** | **412,300** | **(1,105)** | **(404,100)** | **7,100** |

Tick marks: (a) agreed to the FY2024 audited statements; (b) agreed to the translation adjustment schedule, WP 5100-06;
(c) agreed to accounts 5110, 6100, 6200, and 6300 and recomputed at WP 5100-14; (d) agreed to additions to account 1560;
(e) recomputed as 610 x $19.20; (f) recomputed as 117 x $33.96 average vest-date fair value; (g) recomputed at
Exhibit 9-10; (h) agreed to the offering documents and the equity-classification memo, WP 5100-26; (i) charged to APIC in
FY2024 — no FY2025 activity.

The roll-forward foots in two directions: the APIC column ($351,600 + $28,700 + $1,900 + $11,712 − $3,973 +
$3,561 + $18,800 = $412,300) and the total column ($(32,550) − $21,400 + $350 + $60,700 = $7,100). If either
fails, stop and find the difference; a roll-forward that does not foot is usually missing a transaction rather
than containing an arithmetic error.

Two observations follow. The accumulated deficit column changes by exactly the net loss, establishing that nothing was
charged directly to it — no retrospective adjustment, no prior-period correction, no deemed dividend. And the common
stock caption does not move: at $0.0001 par, 51,842 thousand shares produce $5.18 thousand and 49,610 thousand produce
$4.96 thousand, both rounding to $5. Staff frequently propose an adjustment there. There is none.

Foot the FY2024 comparative column the same way and note its shape: AtlasFlow recognized $22,900 of expense while APIC
rose only $12,200, because the $14,700 capped call premium absorbed more than half the increase. That is why the change
in APIC is never a proxy for stock-based compensation.

## 9.2 The Cap Table as Information Produced by the Entity

AtlasFlow maintains its capitalization table in Carta, the system of record for grants, exercises, vesting, and the
outstanding share count, and the source of the extract from which the stock-based compensation entry is calculated. The
cap table is therefore **information produced by the entity (IPE)**, and AS 1105 requires you to test its completeness
and accuracy before relying on it. Chapter 12, §12.6 owns the application controls inside Carta; your job is the
reconciliation, and you do it four ways because the four sources fail differently: Carta from a grant entered late or an
exercise entered twice, the general ledger from an entry posted with no corresponding equity event, the transfer agent
from settlement timing or shares issued outside the Carta process, and the EPS denominator from weighting even when the
period-end count is right.

**Exhibit 9-2. Four-way share reconciliation at December 31, 2025 (shares in thousands).**

| Source | Document | Shares | Difference | Explanation |
| --- | --- | --- | --- | --- |
| Carta | "Outstanding securities" report, run 1/9/2026 | 51,842 | — | Base population |
| General ledger | Account 3000, $5 at $0.0001 par | n/a | n/a | Par is not precise enough to reconcile shares; reconcile APIC instead |
| Transfer agent | Registered and book-entry holder statement | 51,780 | (62) | December 31 ESPP purchase settled January 2, 2026 |
| EPS denominator | Weighted-average basic shares | 50,952 | (890) | Weighting, not a share difference — see Exhibit 9-3 |

The transfer agent difference is the one to insist on. Sixty-two thousand shares is trivial, but the same difference
in the other direction — the transfer agent showing *more* shares than Carta — would mean shares were issued outside
the Carta process. Set the threshold at zero: the population is small enough that every difference is explainable.

**Exhibit 9-3. Weighted-average basic share reconciliation, FY2025 (shares in thousands).**

| Component | Shares | Weighting | Weighted shares |
| --- | --- | --- | --- |
| Outstanding, January 1, 2025 | 49,610 | 365/365 | 49,610 |
| Option exercises | 610 | Various dates | 337 |
| RSU vesting, net of shares withheld | 1,489 | Various dates | 969 |
| ESPP purchase, June 30, 2025 | 71 | 184/365 | 36 |
| ESPP purchase, December 31, 2025 | 62 | 0/365 | — |
| **Weighted-average basic shares** | **51,842** | | **50,952** |

The total agrees to the disclosed $(0.42): $21,400 ÷ 50,952 = $0.4200. Recompute from the daily share position rather
than monthly averages, which drift from the reported figure and leave you unable to tell whether the drift is your
approximation or a real error. A difference above about 25 thousand shares should send you to the daily position file
to reconcile it to the Carta event log by date.

## 9.3 Stock-Based Compensation Fundamentals

Five dates control the accounting and staff routinely conflate them. The **grant date** is when employer and employee
reach a mutual understanding of the key terms, which at AtlasFlow requires committee approval, communication to the
employee, and no remaining employer-side condition. The **service inception date** is when the requisite service period
begins; it usually coincides with the grant date but does not when an award is approved before targets are set or service
begins before formal approval, in which case cost begins at the service inception date and is remeasured at the eventual
grant date. The **measurement date** for an equity-classified award is the grant date,
and fair value is not remeasured for later share-price changes. The **vesting date** is when the award becomes
nonforfeitable. The **requisite service period**, derived from the award's terms rather than the stated vesting period,
is the attribution period.

For an award with graded vesting and only a service condition, ASC 718-10 permits either **straight-line** recognition
over the total requisite service period or **graded attribution** treating each tranche as a separate award. It is a
policy election applied consistently, and it matters more than staff expect.

**Exhibit 9-4. Straight-line versus graded attribution — one RSU grant of 48 thousand units at $31.70, four-year
annual graded vesting, granted January 1, 2025 (in thousands).**

| Year | Straight-line | Graded | Difference |
| --- | --- | --- | --- |
| 2025 | 380 | 634 | (254) |
| 2026 | 380 | 380 | — |
| 2027 | 380 | 253 | 127 |
| 2028 | 381 | 254 | 127 |
| **Total** | **1,521** | **1,521** | **—** |

Total cost is 48 x $31.70 = $1,522, shown as $1,521 after rounding. Graded attribution front-loads 41.7% of cost into
year one against 25.0%, so across AtlasFlow's $20,600 of restricted stock unit cost the election moves thousands of
dollars a year: confirm the elected method, confirm Carta applies it, and test one grant of each vesting shape.

AtlasFlow accounts for **forfeitures as they occur**, a permitted election. There is then no forfeiture-rate assumption
to test, but there is a completeness problem: every termination must reach Carta with the correct last day of service,
or unvested awards keep accruing expense for employees who have left. Agree award status in Carta for the termination
population per the human resources system — 41 positions in the October 2025 restructuring alone — using Chapter 10's
listing rather than building a second one.

**Modifications** are measured by comparing the modified award's fair value immediately after to the original award's
immediately before, with the incremental amount recognized over the remaining service period. **Cancellations** with a
concurrent replacement are modifications; without replacement they are settlements. AtlasFlow recorded no repricings in
FY2025; confirm that from minutes for the year and subsequent period and from the Carta audit log of changes to
exercise price, vesting schedule, or expiration date — nine entries, all data-entry corrections within days of grant.

## 9.4 Auditing Option Valuation Inputs

AtlasFlow granted 340 thousand options in FY2025, mostly to employees hired with the Kestrel Labs acquisition, struck at
the $32.10 closing price on the May 15, 2025 grant date and measured with a Black-Scholes-Merton model.

**Exhibit 9-5. FY2025 option grant — valuation inputs and the engagement team's evaluation.**

| Input | Management | Basis | Supportable range | Conclusion |
| --- | --- | --- | --- | --- |
| Share price at grant | $32.10 | Closing price, May 15, 2025 | Observable | Agreed to an independent price source |
| Exercise price | $32.10 | Grant instrument | Observable | Agreed to the committee resolution |
| Expected term | 6.02 years | Simplified method | 5.5 to 6.5 years | Reasonable; see below |
| Expected volatility | 52.0% | Six-company peer group, 6.0-year historical | 48% to 58% | Within range, near the low end |
| Risk-free rate | 4.15% | Interpolated six-year constant-maturity Treasury | 4.05% to 4.25% | Reasonable |
| Dividend yield | 0.0% | None declared or expected | 0.0% | Reasonable; corroborated by the credit agreement's restricted-payment covenant |
| **Grant-date fair value per option** | **$17.37** | Black-Scholes-Merton | **$16.48 to $18.68** | **Within range** |

The **simplified method** averages the vesting term and the contractual term — for a four-year annual graded vest and a
ten-year contract, ((1+2+3+4)/4 + 10)/2 = 6.25 years, adjusted to 6.02 years for monthly vesting. SAB Topic 14 permits it
only where historical exercise data are insufficient to provide a reasonable basis for an estimate. AtlasFlow's history
spans about 1,900 thousand exercises since its 2022 initial public offering, which is approaching sufficiency; document
the conditions relied on and set a planning trigger for FY2026.

**Expected volatility** is the peer-group problem. Three years of AtlasFlow's own history is shorter than the 6.02-year
term, so management blends it with a six-company peer group, and the peer set is where bias enters: one low-volatility
large-cap moves the assumption several points. Test the group by criteria (revenue scale, growth, gross margin, float),
re-derive the median independently, and ask whether the set is last year's. A changed peer set in a year in which lower
expense is convenient is a bias indicator under AS 2501.

**Exhibit 9-6. Sensitivity of the FY2025 option grant to each significant assumption (340 thousand options; $ in
thousands).**

| Scenario | Fair value per option | Total grant-date cost | FY2025 expense (7.5 of 48 months) | Change |
| --- | --- | --- | --- | --- |
| Management's assumptions | $17.37 | 5,906 | 923 | — |
| Volatility at 48% | $16.48 | 5,603 | 875 | (48) |
| Volatility at 58% | $18.68 | 6,351 | 992 | 69 |
| Expected term 5.5 years | $16.68 | 5,671 | 886 | (37) |
| Expected term 6.5 years | $17.99 | 6,117 | 956 | 33 |
| Risk-free rate 4.25% | $17.43 | 5,926 | 926 | 3 |

The sensitivity table earns its place by telling you where to stop. The widest defensible movement in any single
assumption changes FY2025 expense by $69, below the clearly trivial threshold of $72; combining the low ends of
volatility and term gives about $(85). Option valuation is therefore low risk here and does not warrant a specialist,
while restricted stock unit completeness and the performance share unit estimate — which move expense by thousands —
warrant most of your hours. State that reallocation in the workpaper so the reviewer sees a decision rather than an
omission.

## 9.5 Restricted Stock Units and Net Share Settlement

Restricted stock units dominate at AtlasFlow: 4,320 thousand units outstanding at a $31.70 weighted-average grant-date
fair value, $41,300 of unrecognized cost, and $20,600 of FY2025 cost. Measurement is easy — the closing price on the
grant date — so the risk sits in the population and the settlement mechanics.

At vesting a unit becomes a share and the employer incurs a statutory withholding obligation. AtlasFlow settles it
two ways. For most employees a broker sells shares on the employee's behalf, so the gross count is issued and
AtlasFlow remits cash received from the broker: no company-funded outflow and no APIC charge. For Section 16
officers AtlasFlow **net share settles**, withholding shares, issuing only the net, and remitting the tax from its
own funds.

**Exhibit 9-7. FY2025 restricted stock unit settlement (shares in thousands; $ in thousands).**

| Item | Shares | Amount |
| --- | --- | --- |
| Units vested during FY2025 (gross) | 1,606 | |
| Shares withheld on officer awards | (117) | 3,973 |
| **Shares issued, net** | **1,489** | |
| Weighted-average fair value on the vest dates | | $33.96 |

The $3,973 is charged to APIC — withheld shares are a reacquisition of equity, not compensation — and presented as
a financing outflow captioned as taxes paid related to net share settlement. Chapter 8, §8.9 owns the financing
section; note only that the classification is financing rather than operating and that sell-to-cover produces no
line at all. A common error is presenting the entire remittance, including sell-to-cover, as a financing outflow
with an offsetting operating inflow: the amounts net to nothing but both subtotals are overstated.

Three procedures do most of the work. Recompute the gross-to-net bridge: 1,606 less 117 equals 1,489, and 117 x $33.96
equals $3,973. Agree shares withheld on a sample of officer vests to the supplemental wage rate in the payroll system,
using Chapter 10's testing; a rate above the statutory maximum indicates over-withholding, which can raise a
liability-classification question. And prove completeness from the other direction: take the vesting schedule Carta
produced at December 31, 2024 for awards scheduled to vest in 2025, add FY2025 grants vesting within the year, subtract
terminations, and confirm the expectation reproduces 1,606 gross units. If it fails by more than about 20 thousand
units, the usual cause is a retroactively edited vesting schedule; pull the audit log and evaluate each change as a
potential modification under §9.3.

## 9.6 Performance and Market-Condition Awards

A **performance condition** relates to the entity's own operations — revenue, annual recurring revenue (ARR),
bookings, a product milestone. A **market condition** relates to the share price or to total shareholder return
(TSR). ASC 718-10 treats them oppositely, and the difference is the most tested concept in this area.

A performance condition is *not* in grant-date fair value: fair value is measured as though the condition will be met,
and the units expected to vest are estimated and revised each period with a cumulative catch-up. A market condition *is*
in grant-date fair value: it is valued once with a model capable of simulating share-price paths, and cost is recognized
over the derived service period whether or not the condition is met. You never adjust a market-condition award for
outcome; you adjust a performance-condition award every quarter.

AtlasFlow's ARR-based performance share units (PSUs) show the performance-condition mechanics. The 2025 tranche is 262
thousand units at a $34.10 grant-date fair value, with a requisite service period that ended December 31, 2025. Payout
is set by **Plan ARR** — contracted subscription ARR at the measurement date, excluding usage-based overage and ARR from
businesses acquired during the performance period — on a linear scale from 0% at $160,000 to 100% at $170,000, the level
Chapter 12, §12.7 states as required for full vesting.

**Exhibit 9-8. ARR-based PSU 2025 tranche — expected payout and cumulative measurement (in thousands).**

| Item | Q3 2025 | Q4 2025 |
| --- | --- | --- |
| Forecast or actual Plan ARR | 171,200 | 168,500 |
| Reported ARR per Item 7 | n/a | 172,000 |
| Less Kestrel Labs ARR acquired August 4, 2025 | | (2,100) |
| Less annualized usage-based overage | | (1,400) |
| **Plan ARR** | **171,200** | **168,500** |
| Expected payout: (Plan ARR − 160,000) ÷ 10,000, capped at 100% | 100.0% | 85.0% |
| Fully probable cumulative cost: 262 units x $34.10 | 8,934 | 8,934 |
| **Cumulative cost required** | **8,934** | **7,594** |
| Catch-up credit recorded (JE-14962) | | **(1,340)** |

Chapter 12, §12.7 reports the fully probable measure as $8,933 and the 85% measure as $7,593; the $1 difference is
unit-level rounding in the Carta extract. The mechanics matter more: because the requisite service period ended on the
measurement date, the whole tranche was attributable at December 31, 2025, so the change in expected payout produced a
credit equal to the full 15% of $8,934 rather than 15% of a partially attributed balance. FY2025 expense is $7,594 less
the $5,955 recognized through December 31, 2024, or $1,639 — $2,979 of gross attribution less the $1,340 credit.

The market-condition awards differ in kind. The 210 thousand TSR-based PSUs carry a $39.60 grant-date fair value — above
the $32.10 share price at grant, normal for an award that can pay out at 200% — because the payout multiplier is embedded
in the valuation. Management engaged a valuation firm to run a Monte Carlo simulation; Brightline engaged Dr. Igor Petrov
under AS 1210.

**Exhibit 9-9. TSR PSU Monte Carlo assumptions and the specialist's evaluation.**

| Assumption | Management | Specialist's range | Fair value per unit at the endpoints |
| --- | --- | --- | --- |
| AtlasFlow expected volatility | 52% | 48% to 58% | $38.90 to $40.40 |
| Index expected volatility | 24% | 22% to 26% | $39.10 to $40.10 |
| Correlation to the index | 0.58 | 0.50 to 0.65 | $39.20 to $40.00 |
| Three-year risk-free rate 4.05%; dividend yields 0.0% and 1.6%; 250,000 paths | Observable | Observable | Immaterial |
| **Grant-date fair value per unit** | **$39.60** | **$38.60 to $40.60** | Cost range $8,106 to $8,526 |

Do not ask whether the TSR condition was achieved. Ask whether the model simulates the correct payout function, including
the cap and any negative-absolute-TSR modifier; whether the volatility, correlation, and dividend inputs come from the
correct historical window; and whether the result is stable when re-seeded. If a different seed moves fair value by more
than about 0.5%, the path count is too low.

## 9.7 The Employee Stock Purchase Plan

AtlasFlow's ESPP has two six-month offering periods a year, a 15% discount, and a six-month **look-back**: the purchase
price is 85% of the lower of the fair market value on the first day of the period and on the purchase date. That makes
the plan compensatory, and grant-date fair value equals the discount on a share plus a call on 85% of a share plus a put
on 15% of a share.

**Exhibit 9-10. FY2025 ESPP purchases and expense (shares in thousands; per-share amounts in dollars).**

| Item | Period ending 6/30/2025 | Period ending 12/31/2025 |
| --- | --- | --- |
| Fair market value, first day | 29.40 (1/2/2025) | 33.90 (7/1/2025) |
| Fair market value, purchase date | 33.80 | 41.20 |
| Purchase price: 85% x lower of the two | 24.99 | 28.82 |
| Shares purchased | 71 | 62 |
| **Proceeds** | **1,774** | **1,787** |
| Grant-date fair value per share: 0.15S + 0.85 call + 0.15 put | 8.88 | 10.24 |
| Estimated participating shares at the grant date | 71 | 64.5 |
| **FY2025 expense** | **630** | **660** |

Proceeds of $3,561 agree to Exhibit 9-1 and expense of $1,290 carries to Exhibit 9-11. Recompute the purchase price from
an independent price source; the look-back means the relevant price is four to six months before the purchase, exactly
the kind of stale input that gets copied forward incorrectly. The December 31 purchase priced off the July 1 opening
price of $33.90 rather than the year-end $41.20, a 30.0% discount that makes expense per share far higher than the
nominal 15% suggests.

The **modification traps** are where ESPPs generate restatements. Increasing the discount, extending the look-back,
adding a period, resetting a period after a share-price decline, or raising the contribution limit mid-period all modify
outstanding awards and require incremental fair value. An employee-initiated withdrawal is not a modification; a
company-wide change in withdrawal terms is. Ask the administrator whether any term changed, then corroborate against the
plan document and committee minutes. AtlasFlow made no changes in FY2025, and the procedure was still required, because
"no changes" is a conclusion that must rest on evidence.

## 9.8 Classification Across Expense Lines and Capitalization

Total stock-based compensation cost recognized in FY2025 was $30,600, of which $28,700 was expensed and $1,900 capitalized
into internal-use software. The by-line allocation is not a disclosure detail: it lands in gross margin, so
misclassification between cost of revenue and operating expense is a plausible manipulation with no effect on the loss.

**Exhibit 9-11. FY2025 stock-based compensation by award type and financial statement line (in thousands).**

| Award type | Cost of revenue (5110) | R&D (6100) | S&M (6200) | G&A (6300) | Capitalized (1560) | Total |
| --- | --- | --- | --- | --- | --- | --- |
| Stock options | 210 | 1,550 | 780 | 890 | 150 | 3,580 |
| Time-based RSUs | 1,480 | 7,420 | 5,300 | 4,700 | 1,700 | 20,600 |
| ARR-based PSUs, 2025 tranche, net of the $1,340 credit | 98 | 758 | 367 | 415 | — | 1,638 |
| ARR-based PSUs, later tranche | 110 | 860 | 420 | 472 | — | 1,862 |
| TSR market-condition PSUs | — | 300 | 380 | 950 | — | 1,630 |
| ESPP | 202 | 512 | 353 | 173 | 50 | 1,290 |
| **Total cost recognized** | **2,100** | **11,400** | **7,600** | **7,600** | **1,900** | **30,600** |
| Less capitalized into internal-use software | | | | | (1,900) | (1,900) |
| **Expense per the statement of operations** | **2,100** | **11,400** | **7,600** | **7,600** | **—** | **28,700** |

Every row and column foots, and the four expense columns agree to the $2,100 / $11,400 / $7,600 / $7,600 disclosed and
to accounts 5110, 6100, 6200, and 6300. Build the matrix from the Carta extract's cost-center field mapped to the general
ledger department hierarchy rather than from management's summary, and reconcile the mapping table itself: an employee
who moved from engineering to support mid-year should appear in both columns, and a cost center mapping to no line is a
completeness gap.

Capitalization follows the underlying labor: if an engineer's salary is capitalized into internal-use software under
ASC 350-40, the stock-based compensation for the same hours is capitalized on the same basis, with no separate election.
AtlasFlow capitalized $1,900 within $10,900 of FY2025 additions to account 1560. Recompute it by multiplying each
employee's capitalized hours from the Jira data Chapter 10, §10.7 tested by that employee's cost per hour; the team
obtained $1,840 against $1,900 recorded, a $60 difference below the clearly trivial threshold. Two failure modes recur:
capitalizing compensation for employees whose time was never capitalized, and applying an average department rate to
hours worked by junior engineers with smaller awards. Any conclusion that the underlying hours are unreliable — see the
22% of retroactively restaged Jira epics in Chapter 10 — flows straight through to this $1,900.

## 9.9 Convertible Debt After ASU 2020-06

AtlasFlow issued $175,000 of 0.25% convertible senior notes in September 2024, due September 15, 2029, at an
initial conversion price of $48.20 (a conversion rate of 20.7469 shares per $1,000 of principal), with $5,400 of
issuance costs. Under ASU 2020-06 there is no cash conversion model and no beneficial conversion feature to
separate, so the notes are a single liability recorded net of issuance costs and accreted to par through interest
expense using the effective interest method. Three questions remain: does an embedded derivative require separation
under ASC 815-15, does the conversion feature meet the ASC 815-40 scope exception, and does the schedule foot.

**Exhibit 9-12. Convertible senior notes — issuance cost amortization and carrying amount (in thousands).**

| Period | Beginning carrying amount | Interest expense | Cash coupon | Issuance cost amortization | Ending carrying amount |
| --- | --- | --- | --- | --- | --- |
| 9/15/2024 – 12/31/2024 | 169,600 | 428 | 128 | 300 | 169,900 (a) |
| FY2025 | 169,900 | 1,138 | 438 | 700 | 170,600 (b) |
| FY2026 | 170,600 | 1,437 | 437 | 1,000 | 171,600 |
| FY2027 | 171,600 | 1,538 | 438 | 1,100 | 172,700 |
| FY2028 | 172,700 | 1,637 | 437 | 1,200 | 173,900 |
| 1/1/2029 – 9/15/2029 | 173,900 | 1,410 | 310 | 1,100 | 175,000 (c) |
| **Total** | | **7,588** | **2,188** | **5,400** | |

Tick marks: (a) agreed to the FY2024 audited balance sheet; (b) agreed to account 2500 and to the $700 in the FY2025
statement of cash flows; (c) agrees to the $175,000 due at maturity, and total amortization agrees to the $5,400 of
capitalized issuance costs. The schedule was recomputed for semiannual interest periods beginning September 15,
2024. If your recomputation of FY2025 amortization differs from management's $700 by more than the clearly trivial
threshold, obtain the derivation of the effective rate and the period convention before proposing anything; the usual
innocent cause is a schedule built on annual periods.

**Exhibit 9-13. FY2025 interest expense reconciliation to account 7200 (in thousands).**

| Component | Amount |
| --- | --- |
| Convertible note cash coupon, 0.25% on $175,000 | 438 |
| Amortization of note issuance costs | 700 |
| Commitment fee on the undrawn revolving credit facility | 150 |
| Finance lease and other interest | 52 |
| **Total interest expense per account 7200** | **1,340** |

The **capped calls** are the equity side of the transaction. AtlasFlow paid $14,700 in September 2024 for purchased
call options on its own shares, struck at the conversion price and capped above it, to offset economic dilution on
conversion. Because they are indexed only to AtlasFlow's own shares and settle in them, they meet the ASC 815-40
scope exception, are equity-classified, and the premium is charged to APIC and never remeasured. Three consequences
follow: the premium was a FY2024 financing outflow, not an asset; there is no mark-to-market, so any FY2025 income
statement effect attributable to the capped calls is a misstatement; and they are ignored in diluted EPS entirely.

## 9.10 Earnings Per Share, Disclosures, and Equity ICFR Risks

Basic EPS is the $21,400 net loss over 50,952 thousand weighted-average shares, or $(0.42). Diluted is the same, because
every potentially dilutive security would reduce the loss per share.

**Exhibit 9-14. Potentially dilutive securities excluded from diluted EPS as antidilutive (shares in thousands).**

| Security | Shares | Basis |
| --- | --- | --- |
| Stock options outstanding | 2,140 | Treasury stock method |
| Time-based RSUs | 4,320 | Treasury stock method |
| PSUs, ARR-based and TSR-based, at the number expected to vest | 690 | Contingently issuable shares |
| ESPP shares issuable at the December 31 look-back price | 60 | Treasury stock method |
| Convertible senior notes, if-converted | 3,631 | $175,000 ÷ $1,000 x 20.7469 shares |
| **Total excluded** | **10,841** | |

Recompute the 3,631 rather than agreeing it: 175 thousand bonds x 20.7469 = 3,630.7, rounded to 3,631. Then confirm the
conversion rate has not been adjusted; rates change on stock splits, large dividends, and certain fundamental
transactions, and an unadjusted rate after such an event is a disclosure error.

Work the two methods on hypothetical income, because a reader who has only audited a loss year cannot check the
disclosure in the year the company turns profitable. On net income of $12,000 and an average share price of $34.60,
basic is $0.24; the **treasury stock method** adds 2,140 − (2,140 x $18.40 ÷ $34.60) = 1,002 option shares and 4,320 −
($41,300 ÷ $34.60) = 3,126 unit shares; the **if-converted method** adds $1,138 of coupon and amortization to the
numerator and 3,631 shares to the denominator; diluted is $13,138 ÷ 58,711 = $0.22. Rank securities from most to least
dilutive and add them one at a time, stopping when the incremental effect turns antidilutive.

Test the equity disclosures as recomputable populations rather than as prose: the option and unit roll-forwards, the
weighted-average assumptions, unrecognized cost and its recognition period ($6,900 over 1.8 years for options,
$41,300 over 2.4 years for restricted stock units, $8,200 over 1.6 years for ARR-based PSUs, $4,100 over 2.1 years
for TSR PSUs, $900 over 0.5 years for the ESPP), the by-line allocation in Exhibit 9-11, the note terms and
if-converted count, and the Rule 3-04 statement of changes in stockholders' equity.

Three ICFR risks dominate this cycle. Carta access: a user who can both create a grant and change a vesting schedule
can manufacture expense, and Chapter 12, §12.6 documents administrative access held by two people in Total Rewards
with no periodic review. Grant approval: a grant entered before approval creates a service-inception-date problem as
well as a control deviation. And completeness of minutes: request them from the corporate secretary, confirm the
meeting count against the audit committee calendar, and read the resolutions for delegated grant authority. Chapter 14
owns severity grading.

## Step-by-Step Walkthrough: Recomputing FY2025 Stock-Based Compensation from the Carta Grant Extract

The objective is an independent recomputation of the $28,700 expensed and $1,900 capitalized — $30,600 of total
cost — from unit-level records, with evidence that the records are complete. Documented at WP 5100-14.

**Step 1.** Request the extract with the team present at the screen, so you observe the parameters. Ask for one row per
grant per vesting tranche, with employee identifier, cost center, award type, grant identifier, board approval date,
grant date, service inception date, units granted, grant-date fair value per unit, vesting schedule code and tranche
dates, units vested, forfeited, and cancelled, termination date, expected payout percentage, and cumulative expense
recognized. You obtain a 14,206-row file, `CARTA_GRANTS_20251231.csv`. Compare the row count and "as of" stamp on screen
to the file you receive; if they differ, the file was regenerated and the observation must be repeated.

**Step 2.** Test the extract's integrity: 14,206 data rows, no blank grant-date fair values, no negative units, no vest
dates preceding grant dates. Four rows fail the last test by one to three days, each traceable to a correction logged
within 48 hours. An unexplained failure stops the recomputation, because an extract that contradicts itself cannot
support any expense figure.

**Step 3.** Prove completeness against independent counts. Agree outstanding awards to the disclosed 2,140 options, 4,320
RSUs, 480 ARR-based PSUs, and 210 TSR PSUs, and the share consequence to Exhibit 9-2. Then reconcile participants to
December 31, 2025 headcount: 1,062 employees, 1,004 holding an award, and 58 non-holders all hired after November 1, 2025
and appearing on the January 2026 grant list.

**Step 4.** Prove completeness a second way, from authorizations. Sum the units approved in every FY2025 board and
committee resolution — six meetings and two written consents, 3,410 thousand units — and agree the total to units
granted. An award without a resolution is unauthorized; a resolution without an award is an omitted grant. Both were
nil. This step is what distinguishes a recomputation from a tie-out: it addresses the possibility that Carta and
management's schedule are wrong together.

**Step 5.** Recompute the option cost. For each grant, derive the requisite service period from the service inception
date to the final vest date, apply AtlasFlow's straight-line election, and compute FY2025 cost as cumulative cost at
December 31, 2025 less cumulative cost at December 31, 2024, adjusted for forfeitures as they occurred. You obtain
$3,580, agreeing to Exhibit 9-11.

**Step 6.** Recompute time-based restricted stock unit cost the same way, agreeing 12 grant-date prices to an
independent source. You obtain $20,610 against $20,600 recorded; place tick mark (b), "recomputed, difference below the
$72 clearly trivial threshold."

**Step 7.** Recompute ARR-based PSU cost using the expected payout percentages in management's Q4 memo: $1,639 and $1,862
for the two tranches against $1,638 and $1,862 recorded. Hold the reasonableness of the 85% for the case study, and say so
in the workpaper so the reviewer does not read the tick mark as acceptance of the assumption.

**Step 8.** Agree TSR PSU cost of $1,630 to the specialist's $39.60 grant-date fair value and the derived service
period, and confirm no adjustment was made for expected or actual achievement of the market condition. Such an
adjustment is an error at any amount.

**Step 9.** Recompute ESPP cost of $1,290 from Exhibit 9-10, including the true-up of the second period's estimated
participating shares to the 62 thousand purchased.

**Step 10.** Sum the recomputation: $3,580 + $20,610 + $1,639 + $1,862 + $1,630 + $1,290 = $30,611 against $30,600
recorded. Split the recorded amount between the $28,700 expensed and $1,900 capitalized, agree the capitalized amount to
additions to account 1560, and agree the four expense columns to accounts 5110, 6100, 6200, and 6300.

**Step 11.** Reconcile from the entry side. Extract every FY2025 entry crediting account 3100 with a stock-compensation
source code: 12 monthly Carta-generated entries totaling $30,600 plus JE-14962 for $(1,340), which nets within the monthly
entries because December was posted at 100% before the catch-up. An entry crediting 3100 that does not come from the Carta
feed is the highest-value selection in this cycle.

**Step 12.** Conclude and document the failure paths. The $11 difference is 0.04% of the balance, and the population is
complete on two independent bases. Record the three results that would have changed the conclusion: a difference above
performance materiality of $940, requiring grant-level investigation; a completeness failure in Step 4, which would
force a controls-based alternative; and any audit-log entry modifying a grant's economics, which would require a
modification analysis under §9.3.

## Extended Case Study: The Q4 Revision of the ARR-Based PSU Expected Payout from 100% to 85%

### Background

The 2025 tranche of AtlasFlow's ARR-based performance share units — 262 thousand units at a $34.10 grant-date fair value,
requisite service period ending December 31, 2025 — was assessed at a 100% expected payout in the third quarter of 2025
and revised to 85% in the fourth, producing a $1,340 credit to expense equal to the full 15% of the tranche's $8,934
cost. Against performance materiality of $940 and specific materiality of $150 for executive compensation, it is
significant in a year with a $21,400 net loss.

### The Facts

The award pays out on a linear scale from 0% at Plan ARR of $160,000 to 100% at $170,000, where Plan ARR excludes
usage-based overage and ARR from businesses acquired during the performance period.

- **August 6, 2025.** The Q3 forecast package projects year-end Plan ARR of $172,600. Payout 100%.
- **September 30, 2025.** The Q3 close memo repeats 100%, citing the August forecast. Actual September ARR is $164,900
  reported, $163,400 on a Plan ARR basis.
- **October 21, 2025.** The restructuring eliminates 41 positions, including six enterprise account executives in the
  expansion motion; trailing net revenue retention has fallen from 118% to 113%.
- **November 14, 2025.** Finance issues a revised forecast: Plan ARR of $168,770, an 87.7% payout.
- **December 31, 2025.** Reported ARR is $172,000; Plan ARR is $168,500 after removing $2,100 of Kestrel ARR and $1,400
  of annualized overage, an 85.0% payout.
- **January 9, 2026.** The close cut-off. The December close records a $1,100 credit on the 87.7% forecast.
- **January 12, 2026, 21:14.** After the engagement team's challenge, Elena Vasquez reverses that entry and posts
  JE-14962 for the full $1,340 at 85.0%, effective December 31, 2025, described as "reclass" and created by copying
  JE-14203. Tom Okafor approves it at 21:18.

### What the Engagement Team Did

The team recomputed Plan ARR from the Zuora subscription population, independently removing Kestrel contracts by customer
identifier and overage by rate-plan code, obtaining $168,470 against management's $168,500. It read the award agreements
to confirm the exclusion definitions and the linear scale, and inspected the compensation committee's certification. It
performed a retrospective review of the Q3 assessment, asking what fourth-quarter net new Plan ARR the 100% conclusion
implied — $6,600, against $4,100 in the strongest prior quarter. It agreed the credit's line split (5110 $80, 6100 $620,
6200 $300, 6300 $340) to participant cost centers, and evaluated JE-14962 jointly with the Chapter 16 team, which had
selected the same entry independently.

### Analysis

Separate two questions. The measurement question — is 85.0% right at December 31, 2025 — is the easier one: the payout is
a formula applied to an audited period-end measure, so the only judgment is the Plan ARR definition, and the team's
$168,470 implies 84.7%, within rounding and not worth proposing.

The timing question is harder. A change in the estimated units expected to vest is recognized in the period of change,
and the retrospective review supports the view that evidence available at September 30 did not support 100%. Because
cumulative catch-up brings the balance to the right place by year end, an interim timing error of this kind has limited
annual effect; Chapter 19, §19.2 carries the resulting item as corrected misstatement C-5 at $240. The team concluded
that the Q3 assessment reflected optimism rather than error, that fourth-quarter recognition was acceptable, and that
the pattern — a favorable change in estimate landing in the quarter that most needed it, posted after the close cut-off
and approved in four minutes — is a bias indicator reportable to the audit committee whether or not it produces an
adjustment.

### Resolution and Conclusion

Management corrected its December entry, and the recorded $1,340 credit leaves cumulative cost at $7,594, which the team
recomputed. The $240 difference between the original 87.7% measure and the supported 85.0% measure was recorded as C-5,
and no misstatement of the annual financial statements remains from this award. The authorization and description
failures on JE-14962 went to Chapter 14's deficiency evaluation, where they aggregate with W-12 and W-13. The accounting
was right and the control was not; those are separate conclusions.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                              WP 5100-22
AtlasFlow, Inc. — FY2025 integrated audit
ARR-BASED PSU EXPECTED PAYOUT — 2025 TRANCHE

Prepared by:  A. Trent (AT)          Date: 1/23/2026
Reviewed by:  C. Nwosu (CN)          Date: 1/28/2026
2nd review:   G. Lindqvist (GL)      Date: 2/4/2026

PURPOSE
To evaluate management's 85.0% expected payout on the 2025 ARR-based PSU tranche at 12/31/2025,
the $1,340 catch-up credit, and the period in which the change in estimate was recognized
(AS 2501).

SOURCE OF INFORMATION
(a) Carta grant extract 12/31/2025, WP 5100-11 (completeness at WP 5100-14, Steps 3-4).
(b) 2023 PSU award agreements, sections 3(a) and 3(c) (payout scale and Plan ARR definition).
(c) Zuora subscription population 12/31/2025, ZUO_SUBS_20251231 (completeness at WP 2200-09).
(d) Q3 close memo 9/30/2025; revised forecast 11/14/2025; Q4 payout memo 1/8/2026.
(e) Compensation committee certification 2/5/2026; NetSuite audit trail for JE-14962.

PROCEDURES PERFORMED AND RESULTS
1. Recomputed Plan ARR from source (c):
     Reported ARR 12/31/2025                            172,000  (a)
     Less Kestrel Labs ARR (acquired 8/4/2025)           (2,100)  (b)
     Less annualized usage-based overage                 (1,400)  (b)
     Plan ARR, Brightline recomputation                 168,470  (c)
     Plan ARR per management                            168,500
     Difference                                              30  - below CTT of 72
2. Applied the scale in source (b): (168,470 - 160,000) / 10,000 = 84.7%; management 85.0%.
   Effect of 84.7%: 8,934 x 0.3% = 27. Below CTT. Management's 85.0% accepted.
3. Recomputed the cumulative measure and catch-up:
     262 units x $34.10 GDFV                             8,934  (a)
     Cumulative at 100% (service period ended 12/31/25)   8,934
     Cumulative required at 85.0%                         7,594
     Recognized through 12/31/2024                        5,955  (a)
     FY2025 expense, net of catch-up                      1,639
     Catch-up credit required                             1,340  (d)
4. Retrospective review of the Q3 100% assessment: September actual Plan ARR 163,400 implied
   required Q4 net new Plan ARR of 6,600 vs. 4,100 in the strongest prior quarter. The Q3
   assessment was optimistic on evidence then available. $240 recorded as C-5 (WP 8100-04).
5. Recomputed the credit's line allocation: 5110 80 / 6100 620 / 6200 300 / 6300 340 = 1,340.
6. JE-14962 authorization: approved 4 minutes after posting, after the 1/9/2026 cut-off,
   single-word description. CONTROL DEVIATION - see WP 3200-14.7 and WP 4100-30.

TICK MARK LEGEND
(a) Agreed to source (a).   (b) Agreed to source (c) by customer ID and rate-plan code.
(c) Recomputed by AT; reperformed by CN.   (d) Agreed to JE-14962 as posted.

CONCLUSION
The 85.0% expected payout and the $1,340 catch-up credit are supported and cumulative cost of
$7,594 is appropriate. The change in estimate should have been recognized in part at 9/30/2025;
$240 was recorded as C-5. The favorable direction and late timing are reported as a bias
indicator at WP 8100-06 and in the AS 1301 communication. The authorization deviation is
reported separately. No uncorrected misstatement arises from this award.
```

### Lessons

1. Separate the measurement question from the timing question and answer them in that order.
2. When a performance condition is a formula applied to an audited period-end measure, the issue is the definition of
   the measure, not the probability judgment — so read the award agreement before the memo.
3. A retrospective review of the prior interim assessment is the only procedure that detects optimism in a quarter
   already closed, and it costs an hour.
4. A change in estimate that improves results, in the quarter that needs it, recorded after the cut-off, is a bias
   indicator even when every number is right.

## Common Mistakes

### Mistake 9.1 — Using the change in APIC as a proxy for stock-based compensation

**What it looks like.** The workpaper agrees the $28,700 of expense to the APIC movement and stops.
**Why it happens.** In a simple year the two are close, and the tie feels like corroboration.
**What goes wrong.** APIC also moves for exercises, ESPP purchases, withholding, capped calls, and capitalized cost.
AtlasFlow's FY2024 movement was $12,200 against $22,900 of expense.
**How to avoid it.** Build the roll-forward with every component separately identified, as in Exhibit 9-1.

### Mistake 9.2 — Treating the Carta extract as evidence rather than as IPE

**What it looks like.** The recomputation is meticulous and the extract's completeness is never addressed.
**Why it happens.** Carta is a reputable vendor system and a SOC 1 report exists.
**What goes wrong.** A SOC 1 report addresses the service organization's controls, not whether AtlasFlow entered every
grant and termination. If a grant is missing, a perfect recomputation reproduces a wrong number.
**How to avoid it.** Prove completeness on two independent bases, as in Walkthrough Steps 3 and 4.

### Mistake 9.3 — Adjusting a market-condition award for whether the condition was met

**What it looks like.** A quarterly entry reversing TSR PSU expense because relative performance is below threshold.
**Why it happens.** The preparer applies the performance-condition model to every PSU.
**What goes wrong.** The market condition is already in grant-date fair value, and cost is recognized over the derived
service period regardless of outcome. Reversing it understates expense.
**How to avoid it.** Classify every PSU condition as service, performance, or market before testing any amount, and
confirm the remeasurement population excludes every market-condition award.

### Mistake 9.4 — Probability-weighting a binary performance condition

**What it looks like.** A performance condition that either is or is not met, accrued at 70% "probable."
**Why it happens.** Probability language in ASC 718-10 is read as an instruction to weight.
**What goes wrong.** For a binary condition the accrual is all or nothing; a weighted accrual is wrong either way and
hides the judgment. AtlasFlow's 85% is legitimate only because the award has a graduated payout scale.
**How to avoid it.** Read the payout mechanics. A scale supports interpolation; a cliff does not.

### Mistake 9.5 — Missing the modification in an ESPP change

**What it looks like.** A memo concluding that adding a mid-year offering period "does not change the economics of
existing awards."
**Why it happens.** ESPP changes are administered by benefits teams and never reach technical accounting.
**What goes wrong.** Resetting or extending a period, changing the discount, or raising the contribution limit modifies
outstanding awards, and incremental fair value must be recognized.
**How to avoid it.** Compare the plan document and committee resolutions to the prior year's, and ask about resets after
a price decline.

### Mistake 9.6 — Presenting withheld shares as compensation cost or an operating outflow

**What it looks like.** The $3,973 of withholding is charged to expense, or presented as an operating outflow.
**Why it happens.** It is a payroll tax remittance, and payroll taxes are operating.
**What goes wrong.** Withheld shares are a reacquisition of equity: the charge is to APIC and the outflow is
financing. Charging expense double-counts compensation already recognized over the vesting period.
**How to avoid it.** Recompute withheld shares times vest-date fair value and agree the product to both the APIC
charge and the financing caption.

### Mistake 9.7 — Applying the simplified method without documenting its conditions

**What it looks like.** "Expected term determined using the simplified method," unsupported, in the fourth year after an
initial public offering.
**Why it happens.** The method is easy and last year's memo said the same thing.
**What goes wrong.** SAB Topic 14 permits it only where historical exercise data are insufficient. With 1,900 thousand
cumulative exercises the data are approaching sufficiency, and an SEC comment would be hard to answer.
**How to avoid it.** Document and quantify the reasons the data are insufficient, and set a planning trigger for the year
the conclusion must change.

### Mistake 9.8 — Capitalizing stock-based compensation at an average rate

**What it looks like.** Capitalized stock-based compensation computed as total engineering cost times the ratio of
capitalized to total engineering hours.
**Why it happens.** It is one formula instead of an employee-level computation.
**What goes wrong.** Award values are not distributed like hours. Senior engineers hold larger awards and charge less time
to capitalizable stages, so the average rate usually overstates the capitalized asset.
**How to avoid it.** Compute at the employee level and compare; a difference above about 10% indicates a mix effect worth
quantifying.

### Mistake 9.9 — Reflecting capped calls in diluted EPS

**What it looks like.** A diluted share count reduced by the shares the capped calls would deliver, or a footnote
describing "net dilution after capped calls."
**Why it happens.** The economics are real and the investor deck presents them that way.
**What goes wrong.** ASC 260-10 prohibits reflecting antidilutive instruments in diluted EPS, and purchased calls are
always antidilutive. The exclusion must survive into the year AtlasFlow becomes profitable.
**How to avoid it.** Keep a schedule of every equity-linked instrument and its EPS treatment, and reconcile the earnings
release's dilution discussion to the footnote.

### Mistake 9.10 — Accepting "no grant modifications this year" on inquiry

**What it looks like.** A memo stating there were no repricings or accelerations, supported by inquiry of the Total
Rewards director.
**Why it happens.** Modifications are rare and the answer is usually true.
**What goes wrong.** Accelerations are frequently granted in separation agreements negotiated by human resources or
legal, never reach accounting, and are individually small but recurring — likely in a year with 41 restructuring
terminations.
**How to avoid it.** Run the Carta audit log for changes to exercise price, vesting schedule, and expiration date, read
the separation agreements for the terminated population, and reconcile both to the accounting conclusion.

## Practice Exercises

### Exercise 9-1 [Foundational]

APIC was $351,600 at December 31, 2024 and $412,300 at December 31, 2025. Identified components: expensed stock-based
compensation $28,700; capitalized $1,900; option exercise proceeds $11,712; ESPP proceeds $3,561; pre-funded warrants
$18,800. Compute the remaining component and state what it is.

### Exercise 9-2 [Foundational]

Par value is $0.0001. Shares moved from 49,610 thousand to 51,842 thousand through option exercises of 610, net RSU
shares of 1,489, and ESPP issuances of 133. Prove the share reconciliation, compute the common stock caption at both
dates to the nearest dollar, and state why the caption does not change.

### Exercise 9-3 [Intermediate]

A grant of 60 thousand RSUs at a $28.00 grant-date fair value vests 25% annually beginning one year after the
January 1, 2025 grant date. Compute 2025 through 2028 expense under straight-line and under graded attribution, and
state the 2025 difference.

### Exercise 9-4 [Intermediate]

During FY2026, 1,800 thousand RSUs vest. Officers hold 340 thousand and net settle at a 42% withholding rate; the
rest use sell-to-cover. Weighted-average vest-date fair value is $38.00. Compute shares withheld, net shares issued,
total shares issued, the APIC charge, and the financing outflow.

### Exercise 9-5 [Intermediate]

An ESPP period runs July 1 to December 31 with a 15% discount and a six-month look-back. Fair market value is $33.90 on
July 1 and $41.20 on December 31, and 62 thousand shares are purchased. Compute the purchase price, the proceeds, the
discount to the purchase-date price, and the aggregate intrinsic benefit.

### Exercise 9-6 [Intermediate]

A PSU tranche of 262 thousand units at a $34.10 grant-date fair value has a requisite service period ending
December 31, 2025. Cumulative expense of $5,955 was recognized through December 31, 2024 and the tranche was carried
at a 100% expected payout through the third quarter. Compute FY2025 expense and the fourth-quarter catch-up at a
year-end payout of (a) 85%, (b) 60%, and (c) 110%, and for (c) state one condition that must hold for an
above-target payout.

### Exercise 9-7 [Advanced]

Notes of $175,000 principal bear a 0.25% cash coupon, were issued at par in September 2024 with $5,400 of issuance costs,
and have FY2025 amortization of $700 and a December 31, 2025 carrying amount of $170,600. Compute FY2025 note interest
expense, unamortized issuance costs, and remaining amortization, then reconcile total interest expense to the $1,340 in
account 7200 given a $150 commitment fee and $52 of other interest.

### Exercise 9-8 [Advanced]

Assume FY2025 net income of $9,600, weighted-average basic shares of 50,952, an average share price of $34.60, options of
2,140 at an $18.40 weighted-average exercise price, RSUs of 4,320 with $41,300 of unrecognized cost, and notes
convertible into 3,631 shares with $438 of coupon and $700 of amortization. Compute basic and diluted EPS, ignoring
taxes, and state whether the notes are dilutive.

### Exercise 9-9 [Intermediate]

A staff workpaper reads: "SBC recomputed: options $3,580; RSUs $20,610; ARR PSUs $3,501; TSR PSUs $1,630 (reduced by
$410 because relative TSR is below the 30th percentile); ESPP $1,290. Total $30,611. Agreed to the $28,700 disclosed;
difference of $1,911 is capitalized SBC and rounding." Identify every error and state the corrected total and
reconciliation.

### Exercise 9-10 [Advanced]

AtlasFlow has used the simplified method since its 2022 initial public offering and now has about 1,900 thousand
exercises across 3,100 grants, a mean holding period of 4.1 years, and an interquartile range of 2.9 to 5.4 years.
Write a conclusion of no more than 120 words on whether the method remains available for FY2025, what further
evidence you would obtain, and what you would communicate about FY2026.

### Exercise 9-11 [Advanced]

Draft the concluding paragraph (100 to 140 words) of the memo on whether the $1,340 PSU catch-up belongs in the
fourth quarter of 2025, using September 30 Plan ARR of $163,400, required fourth-quarter net new Plan ARR of $6,600
against a $4,100 best prior quarter, the November 14 forecast of $168,770, and audited December 31 Plan ARR of
$168,500. State the conclusion, the standard relied on, and the bias implication.

### Exercise 9-12 [Advanced]

Chapter 16 established that JE-14962, the $1,340 PSU credit, was posted January 12, 2026 at 21:14 by the Controller,
approved by the CFO four minutes later with no support attached, described as "reclass," and created by copying an
unrelated entry, and that the accounting was correct. Draft a control deficiency description of 90 to 130 words: the
control, the deviation, magnitude and likelihood, and the deficiencies with which it aggregates.

## Solutions to Practice Exercises

### Solution 9-1

$412,300 − $351,600 = $60,700. Identified components net to $28,700 + $1,900 + $11,712 + $3,561 + $18,800 = $64,673,
so the missing component is $(3,973): cash remitted for taxes on shares withheld in net share settlement. It is
charged to APIC because withheld shares are a reacquisition of equity, not compensation.

### Solution 9-2

49,610 + 610 + 1,489 + 133 = 51,842, agreeing to the disclosed count. Common stock is 51,842,000 x $0.0001 = $5,184
and 49,610,000 x $0.0001 = $4,961. Both round to $5 thousand, so the caption does not move; the entire effect of the
2,232 thousand shares issued sits in APIC.

### Solution 9-3

Total cost = 60 x $28.00 = $1,680; straight-line is $420 a year. Graded treats each 15 thousand-unit tranche
separately: 2025 = 420 + 210 + 140 + 105 = $875; 2026 = $455; 2027 = $245; 2028 = $105. Both total $1,680. The 2025
difference is $455 — graded recognizes 52.1% of cost in year one against 25.0%.

### Solution 9-4

Officer vests of 340 at 42% give 142.8, rounded to 142 shares withheld, so net officer shares are 198. Sell-to-cover
vests of 1,460 are issued gross, so total shares issued = 1,658 thousand. APIC charge = 142 x $38.00 = $5,396, which is
also the financing outflow. Sell-to-cover produces neither, because the broker's proceeds fund the remittance.

### Solution 9-5

Purchase price = 85% x lower of $33.90 and $41.20 = $28.815, rounded to $28.82. Proceeds = 62 x $28.82 = $1,787.
Discount to the purchase-date price = ($41.20 − $28.82) ÷ $41.20 = 30.0%. Aggregate intrinsic benefit = 62 x $12.38 =
$767. The look-back, not the 15% discount, produces most of that benefit.

### Solution 9-6

Fully probable cost = 262 x $34.10 = $8,934. (a) Cumulative at 85% = $7,594; FY2025 expense = $7,594 − $5,955 =
$1,639; catch-up = $(1,340). (b) At 60%: cumulative $5,360; expense $(595); catch-up $(3,574). (c) At 110%:
cumulative $9,827; expense $3,872; catch-up $893. For (c) the award must permit above-target payout on a scale and
the incremental units must be authorized within the plan's share reserve.

### Solution 9-7

Note interest = coupon $175,000 x 0.25% = $438 plus $700 of amortization = $1,138. Unamortized issuance costs =
$175,000 − $170,600 = $4,400, so $1,000 of the $5,400 is amortized ($300 in FY2024, $700 in FY2025) and $4,400
remains through September 15, 2029. Reconciliation: $1,138 + $150 + $52 = $1,340, agreeing to account 7200.

### Solution 9-8

Basic = $9,600 ÷ 50,952 = $0.19. Options: 2,140 − (2,140 x $18.40 ÷ $34.60) = 1,002 incremental shares. RSUs: 4,320 −
($41,300 ÷ $34.60) = 3,126. Notes: numerator $9,600 + $1,138 = $10,738; denominator plus 3,631. Diluted = $10,738 ÷
58,711 = $0.18. The notes are dilutive because the $1,138 add-back spread over 3,631 shares is $0.31, and adding them
still reduces per-share income from $0.19.

### Solution 9-9

Three errors. The $410 reduction to TSR PSU cost is wrong, because a market condition is captured in grant-date fair
value and cost is recognized regardless of achievement; TSR cost is $2,040 and the recomputed total $31,021. The
reconciliation is backwards: the $28,700 disclosed is expense only, and the comparison should be recomputed total cost
against $30,600 recorded. And labelling a $1,911 difference "capitalized SBC and rounding" merges two unlike items; the
capitalized amount is a known $1,900. Corrected, $31,021 against $30,600 leaves $421 to investigate, above the $72
clearly trivial threshold.

### Solution 9-10

Model answer: "Continued use of the simplified method is no longer well supported. SAB Topic 14 permits it only where
historical exercise data are insufficient to provide a reasonable basis for estimating expected term. With 1,900
thousand exercises across 3,100 grants and a mean holding period of 4.1 years, the data appear sufficient and the
6.02-year assumption exceeds observed behavior. We will obtain the full exercise dataset, test its completeness, and
assess whether the distribution is representative given the 2022 initial public offering. Because moving to 5.5 years
changes FY2025 expense by $37, we propose no adjustment, and we will communicate that FY2026 requires a history-based
estimate." An answer accepting the method for FY2025 is defensible only if it quantifies why post-IPO behavior does
not represent a 6.02-year term.

### Solution 9-11

Model answer: "Recognition of the $1,340 catch-up in the fourth quarter of 2025 does not misstate the annual financial
statements, because the cumulative-catch-up mechanism of ASC 718-10 brings cumulative cost to the $7,594 supported by
audited December 31 Plan ARR of $168,500. Management's third-quarter 100% assessment was nonetheless optimistic:
September Plan ARR of $163,400 implied required fourth-quarter net new Plan ARR of $6,600 against a best prior quarter
of $4,100, and the November 14 forecast of $168,770 shows the trend was visible earlier. $240 has been recorded as
C-5. Under AS 2501 we treat a favorable change in estimate recognized in the quarter that most needed it as an
indicator of possible bias and report it in the AS 1301 communication." An answer defending the Q3 assessment on the
August forecast fails because it does not address the September actual.

### Solution 9-12

Model answer: "Control: manual journal entries above the review threshold require preparation and approval by
different individuals, with support attached and a description sufficient to identify the transaction (W-12, W-13).
Deviation: JE-14962, a $1,340 credit to stock-based compensation expense, was prepared and posted by the Controller on
January 12, 2026 at 21:14, after the January 9 close cut-off, described only as 'reclass,' created by copying an
unrelated revenue accrual entry, and approved by the CFO four minutes later with no support attached. Magnitude:
$1,340, above performance materiality of $940, and 1,880 manual entries were created by copy, so potential magnitude
exceeds the entry. Likelihood: more than remote, because approval occurred without evidence of review. Aggregate with
W-12, W-13, and the equity ITGC deficiencies." The description works because it separates correct accounting from the
failed control.

## Review Questions

**RQ 9-1.** Why is the change in additional paid-in capital not a reliable proxy for stock-based compensation
expense?

**RQ 9-2.** Name the four sources reconciled in a cap table reconciliation and one failure each detects that the
others do not.

**RQ 9-3.** Distinguish the grant date from the service inception date and state when they diverge.

**RQ 9-4.** What must be true for an entity to use the simplified method for expected term?

**RQ 9-5.** Why does accounting for forfeitures as they occur create a completeness risk rather than eliminate an
estimation risk?

**RQ 9-6.** How does the accounting for a performance condition differ from that for a market condition?

**RQ 9-7.** Why did the change in the ARR-based PSU expected payout produce a credit equal to the full 15% of the
tranche's cost?

**RQ 9-8.** What makes an employee stock purchase plan compensatory, and what three components make up its
grant-date fair value?

**RQ 9-9.** Name three ESPP changes that constitute modifications of outstanding awards.

**RQ 9-10.** On what basis is stock-based compensation capitalized into internal-use software, and what determines
the amount?

**RQ 9-11.** After ASU 2020-06, what happens to the conversion feature of a note like AtlasFlow's, and what audit
questions remain?

**RQ 9-12.** How are capped calls classified, and how are they reflected in diluted EPS?

**RQ 9-13.** What are the assumed proceeds under the treasury stock method for an option and for a restricted stock
unit?

**RQ 9-14.** Why are all potentially dilutive securities excluded from diluted EPS in a loss year?

**RQ 9-15.** Name three equity-cycle ICFR risks and the evidence you would obtain for each.

## Answers to Review Questions

**RQ 9-1.** APIC also moves for exercise and ESPP proceeds, taxes on withheld shares, capped calls, and capitalized
rather than expensed compensation. AtlasFlow's FY2024 APIC rose $12,200 against $22,900 of expense, because the
$14,700 capped call premium was charged to APIC.

**RQ 9-2.** Carta detects nothing about itself; the general ledger detects entries posted with no corresponding equity
event; the transfer agent detects settlement timing and shares issued outside Carta; the EPS denominator detects
weighting errors a correct period-end count conceals.

**RQ 9-3.** The grant date is when the parties reach a mutual understanding of key terms, requiring approval and
communication; the service inception date is when the requisite service period begins. They diverge when service begins
before approval or targets are set after it, and cost then starts at the service inception date.

**RQ 9-4.** SAB Topic 14 permits it only where historical exercise data are insufficient — a young plan, limited
exercise history, or a structural change making the history non-representative. Document the conditions and revisit
them annually.

**RQ 9-5.** There is no forfeiture rate to audit, but every termination must reach Carta with the correct last day of
service or unvested awards keep accruing expense for departed employees. The work becomes a reconciliation of the human
resources termination population to award status.

**RQ 9-6.** A performance condition is excluded from grant-date fair value and revised each period with a cumulative
catch-up, with no cost retained if it fails. A market condition is inside grant-date fair value, requires a
path-dependent model, and its cost is recognized whether or not the condition is met.

**RQ 9-7.** The tranche's requisite service period ended on the measurement date, so 100% of its $8,934 cost was
attributable at December 31, 2025 and the 15-point change applied to the whole tranche: $8,934 x 15% = $1,340.

**RQ 9-8.** A look-back combined with a discount greater than a reasonable issuance cost. Fair value is 15% of the share
price plus a call on 85% of a share plus a put on 15% of a share — $8.88 and $10.24 for AtlasFlow's two FY2025 periods.

**RQ 9-9.** Increasing the discount; extending the look-back or resetting a period after a price decline; adding a
period or raising the contribution limit mid-period. An employee-initiated withdrawal is not one.

**RQ 9-10.** It follows the labor: compensation for hours capitalized under ASC 350-40 is capitalized on the same basis,
measured as each employee's capitalized hours times that employee's cost per hour — $1,900 of AtlasFlow's $10,900 of
additions.

**RQ 9-11.** The feature is not separated: a single liability, net of issuance costs, accreted to par through interest
expense. What remains is bifurcation under ASC 815-15, the ASC 815-40 scope exception, and whether the schedule foots
to $5,400 and to par.

**RQ 9-12.** Indexed only to AtlasFlow's own shares and settled in them, they meet the ASC 815-40 scope exception, are
equity-classified, and the $14,700 premium is charged to APIC and never remeasured. They are excluded from diluted EPS
entirely, however the earnings release describes them.

**RQ 9-13.** For an option, the exercise price, so incremental shares equal the option count less the count
repurchasable at the average market price. For a restricted stock unit there is no exercise price, so assumed
proceeds are the unrecognized compensation cost.

**RQ 9-14.** Adding shares without changing the numerator reduces the loss per share, which is antidilutive, and
ASC 260-10 requires exclusion. Diluted equals basic, and the 10,841 thousand excluded shares are disclosed instead.

**RQ 9-15.** Carta access, evidenced by the administrator listing and the audit log of vesting and price changes; grant
approval, evidenced by reconciling units approved in resolutions to units granted; and completeness of minutes,
evidenced by requesting them from the corporate secretary and confirming the meeting count independently.

## Key Definitions

**Additional paid-in capital (APIC).** The account holding amounts credited in excess of par — AtlasFlow's account
3100, $412,300 at December 31, 2025.

**Antidilution.** The condition in which including a security would increase earnings per share or reduce the loss per
share; ASC 260-10 requires exclusion from diluted EPS.

**Capitalization table (cap table).** The record of issued equity and equity-linked instruments by holder, class, and
vesting status; entity-produced, so AS 1105 requires testing completeness and accuracy before use.

**Capped call.** A purchased call option on the issuer's own shares, struck at a note's conversion price and capped
above it; where it meets the ASC 815-40 scope exception it is equity-classified with its premium charged to APIC.

**Effective interest method.** Allocation of interest at a constant rate on the carrying amount, accreting a discount or
issuance costs to par; it produces AtlasFlow's $700 of FY2025 amortization.

**Employee stock purchase plan (ESPP).** A payroll-deduction purchase plan; a discount exceeding a reasonable issuance
cost, or a look-back, makes it compensatory under ASC 718-10.

**Expected volatility.** The standard deviation of continuously compounded returns expected over the expected term,
estimated from own history, peer-group history, implied volatility, or a blend.

**Forfeiture.** The loss of an unvested award, usually on termination; an entity elects to estimate forfeitures or
account for them as they occur, and AtlasFlow does the latter.

**Graded-vesting attribution.** Recognition of cost as though each tranche were a separate award, front-loading cost
relative to straight-line; a permitted election for service-condition awards.

**Grant date.** The date the parties reach a mutual understanding of key terms, requiring approvals and communication;
for an equity-classified award it is also the measurement date, and fair value is not remeasured afterward.

**If-converted method.** Measurement of a convertible instrument's dilutive effect by adding the shares issuable on
conversion to the denominator and the related interest, net of tax, to the numerator.

**Market condition.** A condition relating to share price or shareholder return; reflected in grant-date fair value,
with cost recognized whether or not it is satisfied.

**Modification.** A change in an award's terms, with incremental cost measured as the excess of the modified award's
fair value immediately after over the original award's immediately before.

**Monte Carlo simulation.** A technique simulating many share-price paths to value a path-dependent payoff; the usual
method for a relative total shareholder return award.

**Net share settlement.** Issuance of net shares after withholding shares for statutory taxes; the withheld shares are
a reacquisition of equity, so cash remitted is charged to APIC and presented as financing.

**Performance condition.** A condition relating to the entity's own operations; units expected to vest are revised each
period with a cumulative catch-up, and no cost is retained if it fails.

**Requisite service period.** The period over which service must be rendered to earn an award, derived from its terms
rather than the stated vesting period; it is the attribution period.

**Service inception date.** The date the requisite service period begins, usually but not always the grant date; where
service begins first, cost accrues from that date and is remeasured at the grant date.

**Simplified method.** The SAB Topic 14 estimate of expected term as the average of the vesting term and the contractual
term, available only where historical exercise data are insufficient.

**Treasury stock method.** Measurement of the dilutive effect of options and units by treating assumed proceeds — the
exercise price, or unrecognized cost for a unit — as repurchasing shares at the average market price.

## Chapter Summary

1. The equity roll-forward is the population definition for the section; build it from prior-year audited balances
   and do not proceed until it foots in both directions.
2. AtlasFlow's APIC rose $60,700 against $28,700 of stock-based compensation, which is why the change in APIC is
   never a proxy for expense.
3. The cap table is information produced by the entity; reconcile it to the general ledger, the transfer agent, and the
   EPS denominator, and investigate every difference regardless of size.
4. Cost begins at the service inception date, not the grant date, and the two diverge more often than staff expect.
5. Option valuation here is low risk — the widest defensible movement in any assumption changes expense by $69 — so
   hours belong on population completeness and the performance share unit estimate.
6. Net share settlement charges APIC for cash remitted on withheld shares and produces a financing outflow;
   sell-to-cover produces neither.
7. A performance condition is revised each period; a market condition is valued once and never adjusted for outcome,
   and confusing the two is the most common conceptual error in this cycle.
8. Because the 2025 PSU tranche's service period ended on the measurement date, a 15-point change in expected payout
   produced a credit equal to 15% of the tranche's entire $8,934 cost.
9. The ESPP look-back, not the 15% discount, produces most of the benefit and most of the expense, and any change in
   plan terms is a modification requiring incremental measurement.
10. Stock-based compensation must reconcile by expense line as well as in total, because the cost-of-revenue split
    moves gross margin without moving the loss.
11. After ASU 2020-06 the convertible note audit reduces to bifurcation, the scope exception, and whether the schedule
    foots to $5,400 and to par.
12. In a loss year diluted equals basic and the work moves to the excluded-securities disclosure, including 3,631
    thousand if-converted shares recomputed from the conversion rate.
13. A supportable estimate recognized in the wrong period, in the direction that helps, approved in four minutes after
    the cut-off, is simultaneously not a misstatement, a control deficiency, and a bias indicator.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Payroll, headcount, and non-equity compensation | Chapter 10 | The termination population behind forfeitures and the withholding rates behind net settlement |
| Financing activities in the cash flow statement | Chapter 8 | Presentation of exercise proceeds, ESPP proceeds, and taxes paid on net share settlement |
| Carta and NetSuite application controls and IPE reliability | Chapter 12 | Controls over grant entry, vesting schedules, and the walkthrough extract |
| Capitalized internal-use software and engineering time | Chapter 10 | The hours behind the $1,900 of capitalized stock-based compensation |
| Journal entry testing, including JE-14962 | Chapter 16 | The criteria that selected the entry examined in the case study |
| Deficiency severity and aggregation | Chapter 14 | Grading the authorization deviation and the Carta access deficiency |
| Executive incentives and fraud risk | Chapter 17 | The CEO's ARR-based PSU payout scale and the pressure it creates |
| Accumulating misstatements and bias indicators | Chapter 19 | The treatment of C-5 and the retrospective review of the estimate |

## Further Reading

- FASB ASC 718, *Compensation — Stock Compensation*, particularly ASC 718-10 on recognition and measurement and
  ASC 718-20 on equity-classified awards.
- FASB ASC 470-20 and ASC 815-40, read with ASU 2020-06, for convertible instruments and the own-equity scope
  exception, and FASB ASC 260 for the treasury stock and if-converted methods.
- SEC Staff Accounting Bulletin Topic 14 on valuation assumptions and the simplified method, and Regulation S-X
  Rules 5-02 and 3-04 for the capital account captions.
- PCAOB AS 2501, *Auditing Accounting Estimates, Including Fair Value Measurements*, and AS 1210, *Using the Work of
  an Auditor-Engaged Specialist*.
- AICPA AU-C 540 and AU-C 620 for private-company engagements, with the AICPA audit guides on share-based payment and
  the valuation of privately held company equity securities.
