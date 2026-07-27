# Chapter 8 — Cash and Treasury

> Cash at AtlasFlow is $96,400 — 30.3% of total assets, and 47.4% with the $54,200 investment portfolio. Almost none
> of it is at risk of being *misstated*, because a bank balance is set by a third party and reconciled monthly. Nearly
> all of it is at risk of being *stolen*, and what can be misstated is not the balances but the classification lines,
> the completeness of the list of accounts you chose to confirm, and the $180 bank charge nobody posted.

## Learning Objectives

- **LO 8.1** Distinguish the risk of material misstatement in cash from the risk of misappropriation, and
  assign each relevant assertion to the procedure that addresses it.
- **LO 8.2** Test a bank reconciliation line by line, including completeness of the outstanding check list and
  existence of deposits in transit, with a defensible tick-mark legend.
- **LO 8.3** Draft a bank confirmation request, state what the standard form does and does not cover, and
  design procedures for the unknown-account risk.
- **LO 8.4** Construct an interbank transfer schedule, identify a kite from it, and quantify the
  overstatement.
- **LO 8.5** Apply the three-month cash equivalent criterion to money market funds, Treasury bills, and
  processor balances, and conclude on restricted cash and compensating balances.
- **LO 8.6** Classify a short-term debt portfolio, assign each position to a fair value level, and measure
  credit losses on available-for-sale debt securities.
- **LO 8.7** Recompute compliance with a board investment policy and evaluate an unescalated exception.
- **LO 8.8** Verify the US-dollar equivalent of foreign-currency cash and substantiate the exchange-rate
  effect.
- **LO 8.9** Test positive pay, dual wire authorization, payment-file integrity, and vendor bank-detail change
  verification, grading the resulting deficiencies with arithmetic.
- **LO 8.10** Reconcile the cash total in the statement of cash flows and recompute a minimum-liquidity
  covenant.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2310, *The Auditor's Use of Confirmation* (effective for fiscal years ending on or after June 15, 2025, the first AtlasFlow audit it governs) | Confirmation of cash held by third parties; auditor control over requests and responses; non-responses |
| AICPA | AU-C 505; AU-C 501 | Confirmation mechanics containing **no** requirement to confirm cash; evidence over investments and property held by a custodian |
| PCAOB | AS 1105 | Reliability of information produced by the entity: every reconciliation, check list, and portfolio extract here is IPE |
| PCAOB | AS 2110; AS 2301 / AICPA AU-C 315, AU-C 330 | Assertion-level inherent and control risk, producing the pattern in §8.1; nature, timing, and extent, including testing cash wholly at year end |
| PCAOB | AS 2401 / AICPA AU-C 240 | Responses to misappropriation risk and to kiting, lapping, and window dressing |
| PCAOB | AS 2501 / AICPA AU-C 540 | Fair value measurements and the credit-loss estimate on AFS debt securities |
| PCAOB | AS 2201; AS 1305 / AICPA AU-C 265 | The ICFR opinion, which makes the §8.12 tests dual-purpose, and communication of deficiencies |
| PCAOB | AS 2810; AS 2710 / AICPA AU-C 720 | Evaluating presentation; other information such as the Item 7A compliance representation |
| FASB ASC | 305-10; 230-10-20 | Cash equivalents limited to original maturities of three months or less measured from the acquisition date |
| FASB ASC | 230-10-45, as amended by ASU 2016-18 | Restricted cash included in the statement of cash flows totals, with a reconciliation to the balance sheet captions |
| FASB ASC | 320-10-25; 326-30 | Classification at acquisition; for AFS securities, intent and requirement to sell, then the credit component (allowance through earnings) split from the non-credit component (OCI) |
| FASB ASC | 820-10; 825-10-50; 830-30 | Fair value hierarchy and disclosure by level; credit risk concentrations; translation at the closing rate through CTA |
| SEC | S-X Rule 5-02.1; S-K Items 303 and 305 | Identification of cash subject to withdrawal restrictions; liquidity, constraints on transferring cash between entities, and market-risk disclosure |

AtlasFlow is an SEC issuer, so PCAOB standards govern, and two differences matter for private SaaS companies.
AS 2310 requires cash confirmation where the AICPA framework does not, so a private-company auditor who
obtains statements directly from the institution and tests the reconciliation has satisfied AU-C 330 without
one. And absent an internal control attestation, the §8.12 deficiencies feed only the AU-C 265 communication
rather than an ICFR opinion.

## Prerequisites and Chapter Dependencies

Read Chapter 3 first for the materiality figures used throughout ($1,450 overall, $940 performance
materiality, $72 clearly trivial threshold) and Chapter 2 for the assertion-level risk framework. Chapter 6
supplies the $162,450 of FY2025 net invoicing that Exercise 8-12 starts from, and Chapter 7 owns the
receivable side of the cash receipts cut-off. Chapter 9 develops equity and financing cash flows, Chapter 10
the disbursement controls inside the expenditure cycle, Chapter 11 treasury system access, and Chapter 17 the
payment fraud schemes.

## 8.1 Why Cash Is a Low-Misstatement, High-Fraud Account

**Exhibit 8-1. Cash, cash equivalents, and short-term investments at December 31, 2025 (in thousands).**

| Account | Description | Bank / custodian | Currency | Balance |
| --- | --- | --- | --- | --- |
| 1010 | Cash — operating | First Meridian Bank | USD | 41,300 |
| 1015 | Cash — payroll | First Meridian Bank | USD | 3,900 |
| 1020 | Cash — concentration | JPMorgan | USD | 38,100 |
| 1030 | Cash — UK operating | Barclays | GBP | 7,600 |
| 1035 | Cash — AU operating | NAB | AUD | 3,200 |
| 1040 | Cash — India operating | HDFC | INR | 1,100 |
| 1045 | Money market funds | JPMorgan | USD | 1,200 |
| | **Cash and cash equivalents** | | | **96,400** |
| 1100 | Short-term investments — US Treasury bills | JPMorgan (custody) | USD | 31,400 |
| 1110 | Short-term investments — commercial paper and corporate notes | JPMorgan (custody) | USD | 22,800 |
| | **Short-term investments** | | | **54,200** |
| | **Total liquidity** | | | **150,600** |

Cash of $96,400 is 30.32% of total assets of $317,900, and overall materiality of $1,450 is 1.50% of the
caption. On those proportions a staff auditor expects cash to be the most heavily tested account in the file.
It is not.

**Inherent risk for existence and accuracy is low because the balance is externally determined, homogeneous,
and self-correcting.** JPMorgan computes the balance in account 1020; AtlasFlow does not estimate it, there is
no allocation or cut-off convention, and a misstatement survives only until the next reconciliation. Contrast
deferred revenue (Chapter 6), where no external party maintains a competing figure.

**Inherent risk for misappropriation is high because cash is the only asset whose theft requires no conversion
step.** $150,600 sits behind two bank portals on which the Treasury Manager, Nate Oyelaran, is sole
administrator. A fraudulent wire is not a misstatement; it is a completed loss recorded accurately.

**The misstatement risk that does exist lives in classification and population completeness.** Four questions
produce essentially all real cash misstatements: is every account in the caption (§8.2); is the caption right
for a money market fund, a 168-day bill with 22 days left, a $214 Stripe balance, and $310 of collateral
(§8.7, §8.8); do the reconciliations reconcile or merely foot (§8.3); and was cash counted twice (§8.6)?

**Exhibit 8-2. Assertion-level risk assessment, cash and short-term investments (FY2025).**

| Relevant assertion | Inherent risk | Control risk | Principal procedure |
| --- | --- | --- | --- |
| Existence and accuracy of recorded balances | Low | Low | Confirmation under AS 2310; recomputation of the seven reconciliations |
| **Completeness of the account population** | **Moderate** | Moderate | The seven procedures in Exhibit 8-4 |
| Cut-off of receipts and disbursements | Moderate | Moderate | Outstanding check and deposit-in-transit testing (§8.5); interbank transfer schedule (§8.6) |
| Accuracy of foreign-currency balances | Low–Moderate | Moderate | Independent retranslation (§8.11); translation runs through the consolidation workbook (weakness W-8) |
| Valuation of short-term investments | Moderate | Moderate | Independent pricing of all 15 positions; ASC 326-30 analysis (§8.9) |
| **Classification and presentation** | **Moderate** | **Moderate** | §8.7, §8.8, §8.13, §8.14 |
| Rights, including restrictions | Moderate | Moderate | Supplemental confirmation letter (§8.4); agreement reading (§8.8) |
| **Occurrence of disbursements (misappropriation)** | **High** | **Moderate** | Treasury control tests (§8.12) |

Two consequences follow: cash is tested wholly at year end rather than rolled forward from the October 31
interim date, and the extent of tests of details is small while control testing is extensive, because the
residual risk after substantive testing is a fraud risk that testing a year-end balance cannot reduce.

## 8.2 Multi-Bank, Multi-Entity Cash and the Completeness of the Account Population

**Exhibit 8-3. Bank and custodian account population and confirmation plan (in thousands).**

| Accounts | Entity | Institution | Balance | Group-audit scope | Who confirms |
| --- | --- | --- | --- | --- | --- |
| 1010, 1015 | AtlasFlow, Inc. | First Meridian Bank | 45,200 | Full scope | Group team, standard form |
| 1020, 1045 | AtlasFlow, Inc. | JPMorgan | 39,300 | Full scope | Group team, standard form |
| 1100, 1110 | AtlasFlow, Inc. | JPMorgan (custody) | 54,200 | Full scope | Group team, custodian position confirmation |
| 1030 | AtlasFlow Software Ltd | Barclays | 7,600 | Full scope component (materiality 580, PM 380) | Brightline UK LLP |
| 1035 | AtlasFlow Pty Ltd | NAB | 3,200 | Specified procedures (materiality 420) | Group team, direct request |
| 1040 | AtlasFlow India Private Limited | HDFC | 1,100 | Analytical procedures only at entity level | **Group team, directly** |
| | **Total** | | **150,600** | | |

The total foots: $45,200 + $39,300 + $54,200 + $7,600 + $3,200 + $1,100 = $150,600. Agree it to the two
balance sheet captions separately rather than to a combined figure, because a schedule mixing deposit accounts
with custody positions at one institution is where double-counting enters: the $1,200 money market sweep sits
inside the $39,300 and also appears on the JPMorgan custodian statement alongside the securities.

The India row is the instructive one. The group audit plan performs analytical procedures only on AtlasFlow
India Private Limited, whose total assets are $2,300, but cash in account 1040 is $1,100 — **117% of group
performance materiality of $940**. An entity-level scope decision does not license leaving a single account
balance above performance materiality untested, so the group team confirmed HDFC directly and tested the 1040
reconciliation. *That procedure is an extension of the continuing case.*

### 8.2.1 The unknown-account risk

The population of bank accounts is asserted by management: treasury produces a listing, the auditor confirms
what is on it, the confirmations agree, the workpaper concludes. Nothing in that sequence tests whether the
listing is complete.

**Exhibit 8-4. Procedures addressing the completeness of the bank account population, FY2025.**

| # | Procedure | Result |
| --- | --- | --- |
| P-1 | Test the treasury account listing as IPE: agree each row to a bank statement and to the ledger, and foot it | 8 accounts, footed to $150,600 |
| P-2 | Read each standard form response for other accounts coming to the institution's attention | First Meridian noted the $50,000 undrawn revolver and a $310 standby letter of credit; JPMorgan noted none |
| P-3 | Extract every ledger account in the 1000–1099 range, including nil-balance and closed accounts, and every account named "cash," "bank," "deposit," "escrow," or "sweep" | 9 accounts: the 7 above plus 1050 (Silicon Ridge Bank, closed March 2025, nil at year end, $1,940 of activity) and 1060 (petty cash, nil) |
| P-4 | Extract distinct originating routing and account numbers from every FY2025 ACH file and wire confirmation | 4 originating accounts, all in the confirmed population |
| P-5 | Independently recompute interest income and compare to account 7100 | $5,110 recomputed against $5,110 recorded (Exhibit 8-5) |
| P-6 | Search FY2025 disbursements for payments to financial institutions and for "bank," "wire fee," or "account analysis" descriptions | Payees limited to the five confirmed institutions and Silicon Ridge through March 2025 |
| P-7 | Read board and audit committee minutes for account authorizations; inspect the banking resolutions on file | Two authorizations, both reflected: Silicon Ridge closed February 2025, HDFC opened January 2025 |

P-3 found the account that mattered. Account 1050 had $1,940 of FY2025 activity and a nil year-end balance —
not a misstatement, but a population §8.12's disbursement testing had not covered, so the team extended the
wire authorization test to the 19 disbursements made before closure. **The unexpected result is almost always
an account with activity and no balance;** the next step is full-period statements, reconciliation of the
activity to the ledger, and determination of who held authority. *Accounts 1050 and 1060 and the Exhibit 8-4
results are extensions of the continuing case.*

**Exhibit 8-5. Independent recomputation of interest income for FY2025 (in thousands; rates annualized).**

| Source | Average balance | Rate | Computed interest |
| --- | --- | --- | --- |
| Short-term investments (1100, 1110) | 47,750 | 4.551% | 2,173 |
| Cash — concentration (1020) | 36,000 | 4.300% | 1,548 |
| Cash — operating (1010) | 38,000 | 3.300% | 1,254 |
| Money market funds (1045) | 1,150 | 4.435% | 51 |
| Cash — payroll (1015) | 3,700 | 1.811% | 67 |
| Foreign accounts 1030, 1035, 1040 | 11,300 | 0.150% | 17 |
| **Recomputed against $5,110 per account 7100** | | | **5,110** |

A residual of $140 would imply roughly $3,300 of unidentified average interest-bearing balances at the
concentration account's 4.3% rate; the next step is each institution's annual interest statement.

## 8.3 The Bank Reconciliation as the Central Document

Every substantive assertion about a cash account except rights and classification is proved by one document,
and between its two sides sits only a list of timing differences, each of which must be true, complete, and
correctly signed. Two disciplines govern the test. **Prove both sides independently:** the bank balance from
the institution, the book balance from the trial balance. **Know which side each item belongs on:** an item
recorded by the bank and not the entity adjusts the *book* balance and requires a journal entry; the reverse
adjusts the *bank* balance and requires nothing. Placing the first kind on the bank side produces a schedule
that foots to an unadjusted ledger balance, which is how a required adjusting entry disappears.

**Exhibit 8-6. Account 1010 bank reconciliation at December 31, 2025, as adjusted (in thousands).**

| Line | Description | Amount | Tick |
| --- | --- | --- | --- |
| 1 | Balance per First Meridian Bank statement, account ending 4417 | 42,890 | (a) |
| 2 | Add: deposits in transit | — | (b) |
| 3 | Less: outstanding checks (43 checks per the check register) | (1,410) | (c) |
| 4 | Less: December account-analysis charges recorded in the general ledger, debited by the bank January 2, 2026 | (180) | (d) |
| 5 | **Balance per general ledger, account 1010, as adjusted** | **41,300** | (e) |

Tick-mark legend: (a) Agreed to the First Meridian confirmation received January 21, 2026 and to the statement
obtained through the auditor's read-only portal credential on January 8, 2026. (b) Nil corroborated by
examining all 14 deposits credited January 2 through January 8, 2026. (c) Footed to the NetSuite check
register; 39 of 43 checks totalling $1,347 traced to January clearance; the 4 remaining totalling $63 resolved
at Step 7. (d) Misstatement identified by the engagement team; management recorded AJE 12 (Steps 10 through
12). (e) Agreed to the adjusted NetSuite trial balance.

Line 4 is placement discipline in its hardest form. The charge belongs on the bank side only *because
management recorded it*, which it did after the team established it had not been recorded at all; before the
adjustment the schedule footed at $41,480 with no line 4 and the charge sat in neither balance — internally
consistent and wrong.

**Exhibit 8-7. Reconciliation testing matrix, all seven cash accounts at December 31, 2025 (in thousands).**

| Account | Bank balance | Deposits in transit | Outstanding checks | Other items | Book balance | Items > 30 days old | Misstatement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1010 First Meridian operating | 42,890 | — | (1,410) | (180) | 41,300 | 4 checks, $63 | $180 unrecorded charge |
| 1015 First Meridian payroll | 4,120 | — | (220) | — | 3,900 | 9 checks, $56 | None |
| 1020 JPMorgan concentration | 38,100 | — | — | — | 38,100 | None | None |
| 1030 Barclays UK (GBP) | 7,600 | — | — | — | 7,600 | None | None |
| 1035 NAB Australia (AUD) | 3,200 | — | — | — | 3,200 | None | None |
| 1040 HDFC India (INR) | 1,100 | — | — | — | 1,100 | None | None |
| 1045 JPMorgan money market | 1,200 | — | — | — | 1,200 | None | None |
| **Total** | **98,210** | **—** | **(1,630)** | **(180)** | **96,400** | | |

The total foots: $98,210 − $1,630 − $180 = $96,400, agreeing to the caption. Four accounts have no reconciling
items, normal for a concentration account, a sweep, and wire-funded foreign accounts — and a reason to be
suspicious of one that suddenly acquires them. Account 1015's nine checks totalling $56 aged past 180 days are
an unclaimed property exposure below the $72 clearly trivial threshold, recorded as an observation.

## 8.4 Bank Confirmations: What the Standard Form Does and Does Not Do

The AICPA's standard form to confirm account balance information with financial institutions asks for three
things: the balance of each **deposit account** the auditor lists at a stated date; the balance, due date,
rate, and collateral of each **direct liability** the auditor lists; and a note of **any additional deposit or
loan accounts that come to the institution's attention while completing the form**, expressly without a
comprehensive detailed search of its records.

That last clause is the most frequently misread sentence in the cash audit: it is an invitation to volunteer,
not an undertaking to search. When First Meridian returned the form noting the $50,000 revolver and the $310
standby letter of credit, the team obtained information it valued and no assurance that there is not a ninth
account. **Confirming a balance confirms a balance. It does not confirm the population,** which is proved, if
at all, by the seven procedures in Exhibit 8-4 — of which the confirmation contributes only P-2, the weakest.

Four categories the form does not cover, each of which this audit needed: **contingent liabilities** (the $310
standby letter of credit, which appeared only because the bank volunteered it); **restrictions and
compensating balance arrangements** (the form asks for a balance, not whether you may withdraw it); **facility
terms** including covenants; and **securities held for safekeeping** (the $54,200 portfolio, confirmed through
a custodian position confirmation listing each security by identifier, par, and position date).

**Exhibit 8-8. Supplemental confirmation letter to First Meridian Bank (extract).**

```text
                                                          [AtlasFlow letterhead]
January 6, 2026

First Meridian Bank
Commercial Banking - Client Service
Attn: Relationship Manager, AtlasFlow, Inc.

In connection with the audit of our financial statements for the year ended
December 31, 2025, please confirm directly to our independent auditors,
Brightline LLP (contact: C. Nwosu, audit senior), the following as of the close
of business December 31, 2025.  Please respond even if the answer is "none."

1.  DEPOSIT ACCOUNTS.  For each deposit account of AtlasFlow, Inc. or any
    subsidiary: account number, title, type, ledger balance, collected balance,
    interest rate, and whether the account is subject to positive pay or an ACH
    debit block.  Also list any account closed during the year.

2.  CREDIT FACILITIES.  For each facility: commitment, amount outstanding,
    letters of credit issued under it, unused availability, rate, maturity, and
    each financial covenant with its measurement date and required level.  State
    whether you delivered any notice of default or reservation of rights.

3.  CONTINGENT LIABILITIES.  Each standby or documentary letter of credit,
    guarantee, endorsement, or bankers acceptance, with beneficiary, face
    amount, expiry, and collateral pledged.

4.  RESTRICTIONS AND COMPENSATING BALANCES.  Any restriction on our ability to
    withdraw funds from any account; any minimum, average, or compensating
    balance arrangement, contractual or informal, with the required level and
    measurement period; any right of setoff, lien, or account control agreement.

5.  SAFEKEEPING.  Any securities, instruments, or other property held by you for
    our account, whether in custody, safekeeping, collateral, or escrow.

6.  AUTHORITY.  The current list of individuals authorized to (i) open or close
    accounts, (ii) originate wires, (iii) approve wires, and (iv) administer
    user entitlements in your online banking portal.

Please send your response directly to Brightline LLP and not to AtlasFlow, Inc.

Very truly yours,
/s/ Tom Okafor
Tom Okafor, Chief Financial Officer
AtlasFlow, Inc.
```

Item 6 is the one staff auditors omit: the confirmed authority list is the population for the
dual-authorization test in §8.12, and the only version of that list not maintained by the person it describes.

AS 2310 requires control over requests and responses, and control is a set of specific acts: the team verified
each addressee against the institution's published commercial banking directory rather than a client-supplied
contact, called JPMorgan's published relationship line to validate the responder, and logged request and
response dates on WP 3100-02 for all five institutions. **If a confirmation is not returned,** obtain the
statement through auditor-held read-only portal credentials, examine the cut-off statement, and re-perform the
reconciliation.

## 8.5 Outstanding Checks and Deposits in Transit

These two items are manipulated in opposite directions. An *understated* outstanding check list is the vehicle
for a disbursement fraud, because a check written and never recorded appears on neither the register nor the
outstanding list and the reconciliation still foots; a *fictitious* deposit in transit overstates cash
directly. AtlasFlow reports nil deposits in transit, and "nil" is as testable as "$2,400."

Five tests run on any outstanding check list, applied to account 1010's 43 checks totalling $1,410 at Steps 5
through 8 of the walkthrough: footing and agreement to the check register including the issued-number
sequence; subsequent clearance; **completeness in the reverse direction**, from the January statement back to
the list, the only one that detects an unrecorded disbursement; held checks, of which AtlasFlow has none,
checks issuing through a bank-hosted print service with same-day mailing; and ageing, which here produced four
checks totalling $63 aged 31 to 96 days. "Four items did not clear" is not a conclusion; it is four
investigations.

For deposits in transit the procedure runs from the bank side, examining every credit in the first several
business days of the new period and tracing each to its originating receipt event. **Had one originated
December 31,** cash and the deposits-in-transit line would both be *understated*.

Cut-off of receipts connects to Chapter 7, which owns the receivable side. The team agreed the recorded date
to the bank value date for the last five FY2025 and first five FY2026 receipts in accounts 1010 and 1020, and
all ten agreed. Two do double duty — the $1,120 Halloran Energy wire is the subsequent collection of the
year-end receivable and the $214 Stripe payout is the processor balance §8.7 resolves — so select cut-off
items that are also evidence for something else.

## 8.6 Kiting and the Interbank Transfer Schedule

**Kiting** overstates cash by recording a transfer between two accounts as a receipt in one period and a
disbursement in a later one. It needs only two accounts under common control and a float interval, and its
defining property is the dangerous one: **a kite leaves both bank reconciliations in balance.** Suppose on
December 30, 2025 AtlasFlow draws check 10442 for $2,400 on the JPMorgan concentration account (1020), payable
to AtlasFlow, and deposits it into First Meridian account 1010 the same day. The receipt is recorded December
30 and credited December 31, so both receiving balances include the $2,400; the check clears January 2 and is
not recorded until then, so neither disbursing balance includes it — and a check never *recorded* never
reaches the outstanding check list.

Only a schedule examining both sides of the *same transfer* detects it. The **interbank transfer schedule**
records, for every transfer between the entity's own accounts in a window straddling the period end, the
amount and four dates: disbursement per books and per bank, receipt per books and per bank. **Period test:**
are the two book dates in the same period? If not, cash is misstated by the amount of the transfer. **Side
test:** where the bank dates straddle the period end, does the item appear as a deposit in transit on the
receiving reconciliation and an outstanding check on the disbursing one? Build the population from the bank
statements of all seven accounts, because a kited transfer is not in a client-prepared population.

**Exhibit 8-9. Interbank transfer schedule, December 22, 2025 through January 9, 2026, as performed (in
thousands).**

| # | Description | From | To | Amount | Disb. per books | Disb. per bank | Rec. per books | Rec. per bank | Method |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T-1 | Sweep to money market | 1010 | 1045 | 6,000 | 12/22/2025 | 12/22/2025 | 12/22/2025 | 12/22/2025 | Internal sweep |
| T-2 | Operating funding | 1020 | 1010 | 9,500 | 12/23/2025 | 12/23/2025 | 12/23/2025 | 12/23/2025 | Fedwire |
| T-3 | Payroll funding | 1010 | 1015 | 4,300 | 12/24/2025 | 12/24/2025 | 12/24/2025 | 12/24/2025 | Book transfer |
| T-4 | Operating funding | 1020 | 1010 | 7,200 | 12/29/2025 | 12/29/2025 | 12/29/2025 | 12/29/2025 | Fedwire |
| T-5 | Payroll funding | 1010 | 1015 | 3,800 | 12/30/2025 | 12/30/2025 | 12/30/2025 | 12/30/2025 | Book transfer |
| T-6 | Year-end sweep | 1010 | 1045 | 1,200 | 12/31/2025 | 12/31/2025 | 12/31/2025 | 12/31/2025 | Internal sweep |
| T-7 | Operating funding | 1020 | 1010 | 5,600 | 01/02/2026 | 01/02/2026 | 01/02/2026 | 01/02/2026 | Fedwire |
| T-8 | Sweep redemption | 1045 | 1010 | 2,000 | 01/06/2026 | 01/06/2026 | 01/06/2026 | 01/06/2026 | Internal sweep |
| | **Total transfers in the window** | | | **39,600** | | | | | |

Every row passes both tests, the total foots to $39,600, and all eight transfers settled same-day, which is
the structural reason AtlasFlow's kiting exposure is low: Fedwire and same-bank book transfers have no float.
**The float kiting needs comes from paper checks and, to a lesser degree, from ACH.** Now the worked kite;
*the following two transfers are hypothetical.*

**Exhibit 8-10. Interbank transfer schedule with a hypothetical kited transfer (in thousands).**

| # | Description | From | To | Amount | Disb. per books | Disb. per bank | Rec. per books | Rec. per bank | Tick |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **T-9** | **"Concentration true-up," check 10442 drawn on 1020 payable to AtlasFlow, deposited at First Meridian 12/30** | **1020** | **1010** | **2,400** | **01/02/2026** | **01/02/2026** | **12/30/2025** | **12/31/2025** | **(a)** |
| T-10 | Check 10451 drawn on 1020, deposited at First Meridian 12/31 | 1020 | 1010 | 900 | 12/31/2025 | 01/05/2026 | 12/31/2025 | 01/02/2026 | (b) |

(a) **Kite.** The receipt is recorded in FY2025 and the disbursement in FY2026, so cash is overstated by
$2,400. (b) Not a kite. Both sides are recorded in FY2025 and the bank dates straddle the year end, so a $900
outstanding check belongs on the 1020 reconciliation and a $900 deposit in transit on the 1010 reconciliation;
if either is missing, the reconciliation is wrong even though the accounting is right.

Quantify T-9 before characterizing it. A $2,400 overstatement is 165.5% of overall materiality and 255.3% of
performance materiality; corrected cash would be $94,000 and certified liquidity $148,200. The disbursement
side having never been recorded, the correcting entry reverses the December 30 receipt — debit a clearing
account, credit account 1010 $2,400 — rather than netting the two accounts. Three features of the row separate
misstatement from fraud: the transfer serves no commercial purpose between two accounts of one entity; it was
effected by check when every other transfer in the window was a wire or book transfer; and the disbursement
was recorded in a period chosen by the person who wrote the check. Under AS 2401 that pattern requires
treating the item as a possible intentional act, extending the window (the team's practice is 10 business days
either side of the period end, and on a kite indication each of the four preceding quarter ends), and
communicating to the audit committee.

**Window dressing** belongs in the same workpaper: it misstates nothing and may still be a disclosure matter.
AtlasFlow's December 31 cash of $96,400 against a monthly average of approximately $90,150 is a 6.9%
elevation, unremarkable for a company collecting annual-prepay invoices in late December. Lapping is owned by
Chapter 7 and Chapter 17.

## 8.7 Cash Equivalents, the Three-Month Criterion, and Processor Balances

ASC 230-10-20 defines **cash equivalents** as short-term, highly liquid investments readily convertible to
known amounts of cash and so near maturity that they present insignificant interest-rate risk. Both halves are
conditions, and the operative test is **original maturity of three months or less measured from the date the
entity acquires the instrument** — not the issue date and not the balance sheet date. That convention decides
the case that trips staff auditors every year: AtlasFlow's $6,800 Treasury bill maturing January 22, 2026 was
purchased August 7, 2025, so at December 31 it has 22 days to run and is about as liquid an instrument as
exists. It is nevertheless **not** a cash equivalent, because its original maturity from AtlasFlow's
acquisition date is 168 days.

**Exhibit 8-11. Classification decisions on the cash and near-cash population (in thousands).**

| Item | Amount | Facts examined | Conclusion | Authority |
| --- | --- | --- | --- | --- |
| Account 1045, JPMorgan government money market fund | 1,200 | Prospectus obtained: government fund, daily redemption at $1.00, no liquidity fee or gate | Cash equivalent | ASC 305-10; ASC 230-10-20 |
| Treasury bill maturing 1/22/2026, acquired 8/7/2025 | 6,800 | Trade confirmation shows 168-day original maturity | Short-term investment | ASC 230-10-20 |
| Overnight sweep balances within account 1010 | — | Swept nightly to and from account 1045 | No separate caption; inside 1045 | ASC 305-10 |
| Stripe balance settled but not yet paid out | 214 | Analyzed below | Receivable from processor within account 1410 | ASC 305-10; ASC 210-10-45 |
| Standby letter of credit collateral | 310 | Cash-secured; see §8.8 | Restricted cash, noncurrent other assets | ASU 2016-18; S-X Rule 5-02.1 |
| Account 1040, HDFC India cash | 1,100 | Repatriation requires exchange-control filings; no restriction on use in India | Cash and cash equivalents | S-K Item 303 |

**Read the prospectus, not the statement caption.** Institutional prime and municipal funds may impose
liquidity fees or redemption gates, and practice on a gated fund ranges from cash equivalent to short-term
investment. AtlasFlow's is a government fund, which removes the question.

### 8.7.1 Are Stripe processor balances cash?

AtlasFlow's self-serve channel collects through Stripe, which settles to account 1010 on a rolling
two-business-day payout cycle. At December 31, 2025, $214 of captured transactions had settled to AtlasFlow's
Stripe balance and had not been paid out, the payout arriving January 2, 2026. This is not account 1205,
accounts receivable — Stripe self-serve, $1,700, which is customer receivable for amounts Stripe has not yet
collected and which Chapter 7 owns.

Four facts from the merchant agreement and the Stripe balance report decide it. AtlasFlow cannot direct the
timing or use of the funds before payout; they sit in Stripe's pooled account, not a segregated one; AtlasFlow
is exposed to Stripe's credit, precisely the exposure a cash caption asserts away; and there is no reserve or
holdback. The balance is therefore a **receivable from a payment processor**, agreed to account 1410. The
contrary conclusion — cash equivalent, the funds being collected and convertible within two days — is
defensible and common for large processor balances; what is not defensible is concluding without reading the
agreement. **Had the classification been cash,** the $96,400 caption and the §8.14 covenant certificate would
each increase by $214.

## 8.8 Restricted Cash, Compensating Balances, and Rights

Rights over cash is the assertion the confirmation does not reach, and it is proved by reading agreements —
here the First Meridian revolving credit and treasury services agreements, the Austin office lease, and the
JPMorgan custody agreement. What you look for is a sentence that limits withdrawal, creates a lien or right of
setoff, requires a balance to be maintained, or subjects an account to a control agreement.

**Restricted cash.** The Austin lease required a $310 standby letter of credit, which First Meridian issued
cash-secured, and the collateral is unavailable while the letter of credit runs to 2029. The team traced $310
to the noncurrent other assets caption ($3,900), agreed the amount and expiry to the letter of credit and to
First Meridian's confirmation, and confirmed it is not inside the $96,400. *The standby letter of credit and
the $310 of collateral are extensions of the continuing case, which records no restricted cash.* S-X Rule
5-02.1 requires the balance sheet to identify cash subject to withdrawal restrictions, and ASU 2016-18
requires restricted cash to be **included** in the statement of cash flows totals (§8.13). Restriction does
not by itself make a balance noncurrent — the period of restriction does, which is why a 2029 expiry lands the
$310 in noncurrent assets.

**Compensating balances.** First Meridian prices account 1010 through account analysis, offsetting monthly
service charges with an earnings credit computed on the average collected balance, so a higher balance reduces
fees. That is an economic incentive, not a legal restriction, and it becomes a disclosure matter only where
the arrangement requires a minimum or average balance; the team read Section 4 of the treasury services
agreement and relied on item 4 of Exhibit 8-8, to which First Meridian answered "none." **Had the bank
answered that a $5,000 average collected balance is required,** compute the average collected balance by month
from the analysis statements, determine whether the level was met, and draft the disclosure — the amount
staying in the cash caption, because a compensating balance constrains behavior, not access.

**Cash held by foreign subsidiaries.** Account 1040's $1,100 is subject to Indian exchange-control procedures
on repatriation. That is not restricted cash under US GAAP, but S-K Item 303 addresses constraints on
transferring cash among entities, so the liquidity discussion should state the $11,900 held outside the United
States — 12.3% of the caption — and identify the $1,100.

## 8.9 The Short-Term Investment Portfolio: Classification, Fair Value, and Credit Losses

### 8.9.1 Classification under ASC 320-10

Every debt security is classified at acquisition, and classification drives measurement: held-to-maturity at
amortized cost, trading at fair value through earnings, and available-for-sale (AFS) at fair value with
unrealized gains and losses in other comprehensive income (OCI) — which is why accumulated other comprehensive
loss of $1,105 has an investment component.

AtlasFlow classifies the entire $54,200 as AFS, and the classification is testable. AtlasFlow sold $6,300 of
securities before maturity during FY2025 to help fund the Kestrel Labs acquisition, direct evidence against
positive intent to hold to maturity and the reason a treasury portfolio that exists to be spent is almost
always AFS. *That pre-maturity sale is an extension of the continuing case.* Trading is contradicted by the
absence of any sale for gain.

**Exhibit 8-12. Short-term investment portfolio at December 31, 2025 (in thousands; days measured from
December 31, 2025).**

| Position | Rating | Maturity | Days | Amortized cost | Fair value | Gross unrealized loss | % of portfolio |
| --- | --- | --- | --- | --- | --- | --- | --- |
| US Treasury bill | n/a | 01/22/2026 | 22 | 6,802 | 6,800 | (2) | 12.55% |
| US Treasury bill | n/a | 02/19/2026 | 50 | 7,404 | 7,400 | (4) | 13.65% |
| US Treasury bill | n/a | 03/26/2026 | 85 | 6,206 | 6,200 | (6) | 11.44% |
| US Treasury bill | n/a | 05/14/2026 | 134 | 5,309 | 5,300 | (9) | 9.78% |
| US Treasury bill | n/a | 06/25/2026 | 176 | 5,713 | 5,700 | (13) | 10.52% |
| **Account 1100 — US Treasury bills** | | | | **31,434** | **31,400** | **(34)** | **57.93%** |
| Harborview Capital Funding CP | A-1 | 03/06/2026 | 65 | 3,104 | 3,100 | (4) | 5.72% |
| Ardsley Funding CP | A-1 | 02/13/2026 | 44 | 2,703 | 2,700 | (3) | 4.98% |
| Calverton Energy CP | A-1 | 01/22/2026 | 22 | 2,601 | 2,600 | (1) | 4.80% |
| Pinewood Mutual CP | A-1 | 04/09/2026 | 99 | 2,306 | 2,300 | (6) | 4.24% |
| Thornbury Capital CP | A-2 (A-1 at purchase) | 02/27/2026 | 58 | 1,912 | 1,900 | (12) | 3.51% |
| Vantage Grove CP | A-1 | 01/16/2026 | 16 | 500 | 500 | — | 0.92% |
| Northwind Industrial 4.15% notes | A | 09/30/2026 | 273 | 2,528 | 2,500 | (28) | 4.61% |
| Deverell Bancorp 4.60% notes | A- | 11/20/2026 | 324 | 2,441 | 2,400 | (41) | 4.43% |
| Sablefield Holdings 4.35% notes | A- | 10/15/2026 | 288 | 2,234 | 2,200 | (34) | 4.06% |
| Marchmont Retail 4.05% notes | A- | 12/04/2026 | 338 | 2,668 | 2,600 | (68) | 4.80% |
| **Account 1110 — commercial paper and corporate notes** | | | | **22,997** | **22,800** | **(197)** | **42.07%** |
| **Total portfolio** | | | | **54,431** | **54,200** | **(231)** | **100.00%** |

The totals foot: $31,434 + $22,997 = $54,431 of amortized cost, $31,400 + $22,800 = $54,200 of fair value
agreeing to the caption, and $34 + $197 = $231 of gross unrealized loss with no gains. The $231 ties to
equity: accumulated other comprehensive loss of $1,105 comprises $231 of AFS unrealized loss and $874 of
cumulative translation adjustment, with no deferred tax on either given the full valuation allowance. *The
position-level detail, the $54,431, and the $231 / $874 split are extensions built to agree to the case's
$54,200 and $1,105.*

### 8.9.2 Fair value hierarchy and independent pricing

**Exhibit 8-13. Fair value measurements at December 31, 2025 (in thousands).**

| Measurement | Level 1 | Level 2 | Level 3 | Total |
| --- | --- | --- | --- | --- |
| Money market funds (within cash equivalents) | 1,200 | — | — | 1,200 |
| US Treasury bills | 31,400 | — | — | 31,400 |
| Commercial paper | — | 13,100 | — | 13,100 |
| Corporate notes | — | 9,700 | — | 9,700 |
| **Total assets measured at fair value** | **32,600** | **22,800** | **—** | **55,400** |

The totals foot: $1,200 + $31,400 = $32,600 in Level 1, $13,100 + $9,700 = $22,800 in Level 2, and $55,400
overall, being the $54,200 portfolio plus the money market fund. Management's draft split Level 2 as
commercial paper $11,200 and corporate notes $11,600, an error the Level 2 total concealed until the team
recomputed both figures from Exhibit 8-12: a disclosure that foots is not a disclosure that is right.

Level 1 for the Treasury bills is the judgment, the vendor delivering prices from an evaluated-pricing service
rather than as trade prints. The team obtained the vendor's methodology document and confirmed the prices are
quoted market prices for the identical CUSIP in the active secondary Treasury market. **Had the methodology
described interpolation from benchmark curves,** the answer would be Level 2, moving $31,400 between levels —
no balance sheet change, a material disclosure change, and an AS 2810 matter. Independent pricing covered all
15 positions: thirteen agreed within 0.05%, Thornbury differed by $4 and Sablefield by $3, a net $7 or 0.01%
of the portfolio. **A difference above roughly 1% on a position, or a net difference above $145, is where you
stop reconciling and ask which source is right.** There were no Level 3 measurements and no transfers between
levels.

### 8.9.3 Credit losses on AFS debt securities under ASC 326-30

The AFS model is not the expected credit loss model applied to loans; it runs in a fixed order, and the order
is the whole procedure. First, does the entity **intend to sell**? If yes, write down to fair value through
earnings. Second, is it **more likely than not that the entity will be required to sell** before recovery of
amortized cost? If yes, same result. Third, if neither, decompose the unrealized loss: the credit portion
becomes an **allowance for credit losses** through earnings, capped at the excess of amortized cost over fair
value, and the remainder stays in OCI.

Step one is answered by the treasury report and board minutes, which designate no security for sale. Step two
is answered with arithmetic: $150,600 of cash and investments against a $40,000 covenant, $34,400 of FY2025
operating cash inflow, and an undrawn $50,000 revolver, against a maximum identified FY2026 committed outflow
of the $2,500 Kestrel earn-out. **The unexpected result would be a forecast showing a covenant breach**,
forcing write-downs through earnings on every loss position and constituting a going-concern indicator.

**Exhibit 8-14. ASC 326-30 credit loss assessment (in thousands).**

| Group | Amortized cost | Unrealized loss | Credit component | Non-credit component (OCI) | Basis |
| --- | --- | --- | --- | --- | --- |
| US Treasury bills | 31,434 | (34) | — | (34) | Explicit US government guarantee; zero-credit-loss expectation documented |
| Commercial paper, A-1 rated | 11,214 | (14) | — | (14) | Weighted-average 50 days to maturity; liquidity backstops per rating reports |
| Thornbury Capital CP, A-2 | 1,912 | (12) | — | (12) | Decomposed below |
| Corporate notes, A/A- rated | 9,871 | (171) | — | (171) | Duration and spread driven |
| **Total** | **54,431** | **(231)** | **—** | **(231)** | Allowance for credit losses recorded: nil |

The totals foot: $31,434 + $11,214 + $1,912 + $9,871 = $54,431, and $34 + $14 + $12 + $171 = $231. The A-1
group is the five remaining A-1 positions ($3,104 + $2,703 + $2,601 + $2,306 + $500 = $11,214).

Thornbury Capital requires the work, being the only position whose credit quality changed: S&P lowered it from
A-1 to A-2 on November 14, 2025, and its $12 unrealized loss is 0.63% of amortized cost against 0.13% for the
A-1 group. Decompose the $12. At purchase on September 3, 2025 the paper yielded 38 basis points over the
matched Treasury and at December 31 the spread is 96 basis points, so the 58-basis-point widening applied to
$1,912 over 58 remaining days gives roughly $1.8 of spread-attributable loss, leaving about $10 from the
general rise in short-term rates. Then measure the credit component as amortized cost less the present value
of expected cash flows at the effective rate: AtlasFlow expects to collect $1,925 of par on February 27, 2026
and the issuer's backup liquidity facility covers 100% of outstanding paper, so present value is not less than
amortized cost and **the credit component is nil, leaving the entire $12 in OCI.**

Give the sensitivity rather than asserting comfort. Stressing the whole $22,997 non-Treasury book at a 0.5%
cumulative default probability and 55% loss given default indicates $63, 4.3% of overall materiality and below
the $72 clearly trivial threshold. **What would move it:** a downgrade below investment grade, a missed
payment, a decline beyond roughly 5% of amortized cost, or a backup facility draw.

## 8.10 Testing Compliance with the Board Investment Policy

Policy compliance is not a financial statement assertion, and a breach of a board limit does not by itself
misstate anything. It matters because the limits feed the ASC 825-10-50 concentration disclosure, the §8.9.3
credit-loss conclusion, and management's Item 7A representation — and because the quarterly compliance report
is a monitoring control management represents to the audit committee, which puts it inside the AS 2201
opinion.

```text
EXTRACT - AtlasFlow, Inc. Investment Policy Statement (adopted by the Board March 9, 2023;
amended April 24, 2025)

3.1  Permitted instruments.  Obligations of the US Treasury and of US government
     agencies; commercial paper rated A-1 by S&P or P-1 by Moody's at the time of
     purchase; money market funds; and, as added by the April 24, 2025 amendment,
     corporate notes rated A- or better at the time of purchase with a remaining
     maturity not exceeding 18 months.
3.2  Maximum weighted-average maturity of the portfolio: 12 months.
3.3  Maximum single-issuer concentration: 5% of the portfolio.  Obligations of the
     US Treasury and of US government agencies are excluded from this limit.
3.4  Execution.  The Treasury Manager executes purchases within policy.  The CFO
     approves any exception.  Treasury prepares a quarterly compliance report,
     reviewed by the CFO and delivered to the Audit Committee.
```

*The April 24, 2025 amendment permitting corporate notes, the Treasury exclusion in §3.3, and the §3.4
reporting requirement are extensions of the continuing case; the permitted-instrument list, the 12-month
maturity limit, and the 5% concentration limit are case facts.* A staff auditor testing account 1110 against
the March 2023 policy raises nine exceptions where one testing against the amendment raises none, so **obtain
the version in force at the measurement and purchase dates, from board minutes rather than the treasury shared
drive.**

**Exhibit 8-15. Independent recomputation of investment policy compliance at December 31, 2025 (in
thousands).**

| Policy limit | Recomputed result | Limit | Compliant | Source |
| --- | --- | --- | --- | --- |
| §3.1 Permitted instruments | 5 Treasury bills $31,400; 6 commercial paper $13,100, all A-1 at purchase; 4 corporate notes $9,700, all A- or better at purchase | Enumerated list | Yes | Trade confirmations; rating reports at each purchase date |
| §3.2 Weighted-average maturity | 6,455,900 thousand-days ÷ $54,200 = **119 days** | 365 days | Yes, 246 days of margin | Exhibit 8-12 |
| §3.3 Largest non-Treasury issuer | **Harborview Capital Funding, $3,100 = 5.72%** | 5.00% | **No** | Exhibit 8-12 |
| §3.3 Second largest non-Treasury | Ardsley Funding, $2,700 = 4.98% | 5.00% | Yes, by $11 | Exhibit 8-12 |
| §3.1 Rating after purchase (not a policy requirement) | Thornbury downgraded A-1 to A-2 on 11/14/2025 | Tested at purchase only | Not a breach | S&P action; minutes of 12/9/2025 |
| §3.4 Quarterly compliance reporting | Q4 2025 report dated January 14, 2026 reported no exceptions | Report exceptions | **No** | Case study below |

Two points of technique. **Recompute the weighted-average maturity from position-level data:** $54,200
weighted by days gives 119.1 days, where a simple average of the fifteen maturities reports 1,994 ÷ 15 = 133
days and is still compliant, so the error would never surface. And **distinguish limits tested at purchase from limits
tested continuously:** §3.1 says "at the time of purchase," so Thornbury's downgrade is not a breach, while
§3.3 says nothing about timing — and that silence is the heart of the case study.

## 8.11 Foreign-Currency Cash and the Exchange-Rate Effect

Foreign-currency cash is a monetary asset translated at the closing rate under ASC 830-30, the adjustment
running to the cumulative translation adjustment rather than earnings because GBP, AUD, and INR are the
functional currencies of the respective subsidiaries. The audit question is arithmetic: does the recorded
US-dollar amount equal the confirmed local-currency balance multiplied by an independently sourced closing
rate?

The continuing case presents §3.4 already translated into US dollars, so **the exhibit below derives the
local-currency balances from the recorded US-dollar amounts and the §3.4 rates, and those derived figures are
extensions of the case.** On a real engagement the local balance comes from the confirmation, the rate from an
independent source, and the dollar amount is your own computation.

**Exhibit 8-16. Independent retranslation of foreign-currency cash at December 31, 2025.**

| Account | Currency | Local balance (000s, derived) | Rate per §3.4 | Independent rate | Recomputed USD (000s) | Recorded USD (000s) | Difference |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1030 Barclays, UK entity | GBP | 5,993.7 | 1.26800 | 1.26800 | 7,600 | 7,600 | — |
| 1035 NAB, AU entity | AUD | 4,992.2 | 0.64100 | 0.64100 | 3,200 | 3,200 | — |
| 1040 HDFC, India entity | INR | 93,856.7 | 0.01172 | 0.01172 | 1,100 | 1,100 | — |
| **Total foreign-currency cash** | | | | | **11,900** | **11,900** | **—** |

Rounding runs to the nearest $1: £5,993.7 × 1.26800 = $7,600.01, A$4,992.2 × 0.64100 = $3,200.00, and
₹93,856.7 × 0.01172 = $1,100.00. Two procedures beyond the multiplication matter. **Agree the local balance to
the confirmation in local currency,** because a component team confirming a US-dollar equivalent has confirmed
the bank's translation rather than its balance. And **test the rate table as IPE:** translation runs through
the consolidation workbook — weakness W-8 — so the team re-performed all three translations outside it.

Then substantiate the $(100) effect of exchange rates in the statement of cash flows rather than accepting it
as a residual, because a spreadsheet that plugs the residual makes the statement foot while concealing a
misclassified flow. Retranslating the opening local balances at the closing rates and adding the rate effect
on each currency's FY2025 net cash movement gives $48 on GBP, $(132) on AUD, and $(16) on INR, which sum to
$(100) and agree to the reported line. *The prior-year allocation of the case's $88,700 and the opening rates
of 1.26000, 0.66760, and 0.01191 used in that computation are extensions built to agree to the reported
$(100).*

## 8.12 Treasury Controls

The tests below are dual-purpose: they support the AS 2201 opinion and respond to the high inherent risk of
misappropriation in Exhibit 8-2. Grade what you find with arithmetic — magnitude is the exposure the failure
permits, not the loss that happened.

**Exhibit 8-17. Treasury control tests, FY2025.**

| Ref | Control | Population and sample | Result |
| --- | --- | --- | --- |
| C-1 | Positive pay on 1010: issued-check file sent daily; non-matching items require a pay/return decision | 12 monthly exception reports; all 14 FY2025 exceptions | Operating. All 14 decided within one business day, 3 returned. No deviation |
| C-2 | Positive pay on 1015 (payroll) | n/a | **Not enabled.** 118 checks totalling $986 issued; 31 outstanding at year end totalling $220; largest $34. Deficiency CT-1 |
| C-3 | Dual authorization: wires over $100 require a second portal approver | 268 wires over $100 (of 1,847 totalling $312,600); sample of 25 | **1 deviation:** the Treasury Manager approved a $340 wire he initiated. Extended to all 268 via the portal audit log: 4 self-approved wires, $2,140. Deficiency CT-2 |
| C-4 | Payment-file integrity between NetSuite and the bank | Batch PR-2025-1142 (312 payments, $4,318) re-performed end to end; control totals for all 26 ACH batches | Entry count, entry hash, and total debit amount in the NACHA batch control record agreed to the payment register for all 26 batches. No deviation |
| C-5 | Vendor bank-detail changes in Coupa verified by callback to a number already on file, not one supplied with the request | 147 FY2025 changes; sample of 25 | **3 deviations** with no documented callback, all traced to later payments; the largest, $186 to Larkspur Consulting, verified with the vendor's controller. Deficiency CT-3 |
| C-6 | Reconciliation preparation and independent review in FloQast | All 84 monthly reconciliations (7 accounts × 12 months) | All 84 prepared and signed off; 9 reviewed more than 15 business days after month end; the December 1010 review missed the $180 charge. Deficiency CT-4 |

Grade CT-1 with the check population, not with the fact that positive pay is a common control. The exposure is
bounded by $986 of annual check volume — 68.0% of overall materiality — with a largest single item of $34, and
payroll is 98.8% direct deposit, so on that arithmetic and given the Payroll Manager's monthly review of check
images the team graded CT-1 a **deficiency**. The contrary grading is defensible, positive pay being absent
entirely rather than operating imprecisely. **What would move it:** an unrecorded check clearing 1015, a rise
in check volume, or removal of the image review.

CT-2 is the more serious finding, and not because of the $2,140. One deviation in 25 produces an upper
deviation limit near 11% at 90% confidence against a 5% tolerable rate, so no reliance is available on that
sample; the team therefore tested all 268 wires from the portal audit log, converting a sampling conclusion
into a census of 4 wires totalling $2,140, all initiated and approved by Nate Oyelaran — who is also sole
portal administrator and can alter his own approval limits. That is a segregation-of-duties failure over
$312,600 of annual wire volume, graded a **significant deficiency** and communicated under AS 1305. It is not
a material weakness here, because the four wires traced to approved vendor invoices and the monthly
reconciliation review would surface an unsupported wire within about 20 days. Chapter 11 develops the portal
entitlement question and Chapter 17 the schemes CT-2 and CT-3 enable.

## 8.13 The Cash Reconciliation in the Statement of Cash Flows

ASU 2016-18 changed what the statement of cash flows reconciles to: the beginning and ending amounts must
include **restricted cash and restricted cash equivalents**, with a reconciliation to the balance sheet
captions where those amounts are not presented in a single line.

**Exhibit 8-18. Reconciliation of cash, cash equivalents, and restricted cash (in thousands).**

| Line | 12/31/2025 | 12/31/2024 |
| --- | --- | --- |
| Cash and cash equivalents, per the balance sheet | 96,400 | 88,700 |
| Restricted cash included in other assets (letter of credit collateral) | 310 | 310 |
| **Total cash, cash equivalents, and restricted cash in the statement of cash flows** | **96,710** | **89,010** |
| **Net increase in cash, cash equivalents, and restricted cash** | **7,700** | |

The reconciliation foots: $96,400 + $310 = $96,710, $88,700 + $310 = $89,010, and $96,710 − $89,010 = $7,700,
agreeing to the reported net increase. The restricted balance was unchanged, so including it changes nothing;
the trap is that had the letter of credit been issued during FY2025 the $310 would be a flow under the
pre-2016-18 model and no flow at all under the current one. Prove the total two ways: $34,400 + $(37,900) +
$11,300 + $(100) = $7,700, and $96,710 − $89,010 = $7,700. One boundary: the $1,200 money market fund is a
cash equivalent, so the sweeps in Exhibit 8-9 appear nowhere in the statement, and presenting them as
purchases and maturities grosses up investing activities without changing a total. The $11,300 financing
section and the Kestrel component of investing belong to Chapter 9.

## 8.14 The Minimum-Liquidity Covenant and the Liquidity Disclosure

AtlasFlow's $50,000 revolving credit facility with First Meridian was undrawn at December 31, 2025 and carries
a $40,000 minimum-liquidity covenant. An undrawn facility is no reason to skip the covenant, because a breach
permits the lender to terminate the commitment, removing $50,000 of stated liquidity from the going-concern
analysis and from the ASC 326-30 "required to sell" conclusion in §8.9.3.

**Exhibit 8-19. Minimum-liquidity covenant computation at December 31, 2025 (in thousands).**

| Definition tested | Components | Amount | Requirement | Headroom | Coverage |
| --- | --- | --- | --- | --- | --- |
| A. As certified by management January 30, 2026 | Cash and equivalents $96,400 + short-term investments $54,200 | 150,600 | 40,000 | 110,600 | 3.77× |
| B. Credit agreement: unrestricted cash of the Borrower and its domestic subsidiaries in controlled accounts, plus Permitted Investments | Domestic cash $84,500 + short-term investments $54,200 | 138,700 | 40,000 | 98,700 | 3.47× |
| C. Strictest reading: domestic unrestricted cash only | 1010 $41,300 + 1015 $3,900 + 1020 $38,100 + 1045 $1,200 | 84,500 | 40,000 | 44,500 | 2.11× |

Each row foots: $96,400 + $54,200 = $150,600; $84,500 + $54,200 = $138,700; and $41,300 + $3,900 + $38,100 +
$1,200 = $84,500, with foreign cash of $11,900 completing the $96,400 caption. Compliance is not in doubt on
any reading — the strictest measure exceeds the requirement by $44,500, a 52.7% decline in domestic cash,
against FY2025 operating cash inflow of $34,400. But the certificate delivered January 30, 2026 used
definition A, including $11,900 of foreign cash the agreement excludes: the right conclusion by a method the
agreement does not authorize. **Where headroom under the strictest reading falls below roughly 25% of the
requirement,** obtain a lender-signed definition confirmation, recompute monthly, and evaluate the
going-concern and debt-classification consequences. The liquidity discussion should state the facility size,
that it is undrawn, the covenant and the measured level, the $11,900 held outside the United States, and the
restricted $310. Item 7A's assertion of investment policy compliance is the case study, and under AS 2710 the
auditor reads other information for material inconsistency with audit knowledge.

## Step-by-Step Walkthrough: Testing the December 31, 2025 First Meridian Operating Account (1010) Reconciliation

Workpaper WP 3100-06. Inputs: book balance per the reconciliation as presented $41,480; bank balance $42,890;
outstanding checks $1,410 (43 checks); deposits in transit nil. Output: an audited balance of $41,300 and one
corrected misstatement of $180.

**Step 1.** Obtain the December 2025 package from FloQast rather than by email, capturing the metadata the
system stamps: prepared by S. Ferreira, Staff Accountant, January 6, 2026; reviewed by M. Delacroix, Assistant
Controller, January 9; attachments comprising the bank statement, the NetSuite outstanding check report, and
the reconciliation. A package signed off with no attachments is evidence of a signature and none of a
reconciliation.

**Step 2.** Agree the book balance. Account 1010 on the NetSuite trial balance reads $41,480 before the Step
12 adjustment, agreeing to the top of the reconciliation and to the December ledger detail. Tick as (e). **If
the two differ,** the difference is either a post-reconciliation journal entry or a plug.

**Step 3.** Obtain the bank balance from the institution. The team pulled the December statement for account
ending 4417 using its own read-only portal credential on January 8, 2026 and agreed the closing balance to
First Meridian's confirmation received January 21: $42,890 on both. Tick as (a). A client-supplied PDF is IPE,
not bank evidence.

**Step 4.** Recompute the reconciliation as presented: $42,890 − $1,410 + $0 = $41,480. It foots, and footing
proves nothing about the item list, because a reconciliation missing an item on both sides also foots.

**Step 5.** Test the outstanding check list. Foot it (43 items, $1,410), agree each item to the NetSuite check
register by number, date, payee, and amount, and confirm that the highest outstanding number, 10437, equals
the last issued per the register with no gaps. **A check on the list but not in the register is an unrecorded
disbursement:** obtain the cleared item image and the invoice, and quantify.

**Step 6.** Test subsequent clearance against the January 1–23, 2026 statement: 39 checks totalling $1,347
cleared. Tick the traced items as (c).

**Step 7.** Investigate the four that did not clear, $63 in total. Two ($41) cleared February 4 and 9, one
($14) was voided and reissued January 27 at the payee's request, and one ($8) is payable to an unresponsive
former employee. Document each resolution individually, the risk in each being a check that was never issued.

**Step 8.** Test completeness in the direction that matters. Filter the 1,184 debits in the January 1–23
statement for cleared checks bearing a 2025 check date: 61 items, of which 43 are on the outstanding list and
18 cleared December 29 through 31 and are correctly excluded. **An unaccounted item is either an unrecorded
disbursement or an omitted outstanding check, both of which overstate cash.**

**Step 9.** Test the nil deposits-in-transit assertion from the bank side. All 14 credits to account 1010
between January 2 and January 8, 2026, totalling $6,180, comprise nine ACH batches settling January 2 or
later, four lockbox deposits with January postmarks, and one wire received January 5 — none originating on or
before December 31. Tick as (b). **A credit originating December 31 means cash is understated.**

**Step 10.** Read the December statement line by line and mark every item that is not a routine receipt or
disbursement already in the ledger. This is the step that finds what the reconciliation does not show, and it
cannot be automated, because you are looking for the item nobody classified. Of 2,946 December lines, six were
service or analysis entries; five agreed to ledger postings and one did not — a $180 account-analysis charge
on the analysis summary page.

**Step 11.** Investigate the $180. First Meridian's December account-analysis statement shows gross service
charges of $180 offset by an earnings credit, settling on the second business day of January. Query account
6300: eleven monthly charges are recorded, November's at $168, December's absent. November's reconciliation
carries a bank-side deduction of $168 for charges recorded and not yet debited where December's carries no
such line. **The absent line in a recurring pattern is the finding.**

**Step 12.** Quantify and communicate. The $180 is 12.4% of overall materiality and 250% of the $72 clearly
trivial threshold, so it accumulates. Management recorded AJE 12 — debit account 6300 $180, credit account
1010 $180 — bringing the ledger to $41,300 and adding line 4 to Exhibit 8-6, a corrected misstatement because
the pre-adjustment December expense was understated. Document the alternative: accruing the charge rather than
reducing cash would leave cash at $41,480 and accrued expenses $180 higher. AtlasFlow's convention treats an
irrevocable bank-authorized debit like an outstanding check and was applied consistently in prior years, so
the team accepted it while noting that proposing the accrual presentation would also be defensible.

**Step 13.** Test the review control for precision, not existence. M. Delacroix confirmed agreement of the two
balances and inspected the outstanding check listing, and did not read the statement's analysis page. That is
deficiency CT-4: a control designed to detect differences between two balances cannot detect an item absent
from both. Test the NetSuite bank feed in the same step — the unmatched-items queue on interface I-9 held 22
items totalling $412 at December 31, all cleared by January 9 — because **an aged unmatched queue is where a
fraudulent debit sits.**

**Step 14.** Agree the audited balance to the confirmation and the caption: confirmed $42,890, less
outstanding checks $1,410, less the $180 charge not yet debited, equals $41,300, agreeing to the adjusted
trial balance and rolling into the $96,400 caption through Exhibit 8-7.

**Step 15.** Roll forward. Obtain the January 2026 reconciliation and confirm that the $1,410 of December
outstanding checks and the $180 charge cleared, that no December item was reversed in January, and that the
January book balance begins at $41,300. A December receipt reversed in January without a credit memo is the
signature of a period-end overstatement.

## Extended Case Study: The Harborview Capital Concentration — Deficiency, Disclosure, Both, or Neither

### Background

AtlasFlow's board adopted an investment policy on March 9, 2023 and amended it on April 24, 2025. Section 3.3
caps any single non-Treasury issuer at 5% of the portfolio; §3.4 gives execution to the Treasury Manager,
requires CFO approval of any exception, and requires a quarterly compliance report the CFO reviews and
delivers to the Audit Committee. Item 7A of the FY2025 Form 10-K states that the portfolio complied with the
policy throughout the year.

### The Facts

Harborview Capital Funding commercial paper of $3,100 was 5.72% of the $54,200 portfolio at December 31, 2025,
above the limit by $390 of position size. It was purchased October 9, 2025 at $3,104 when the portfolio stood
at $63,200, or 4.91%, and no purchase followed: the exception arose because the denominator fell, $9,000 of
Treasury bills and commercial paper maturing in November and December without full reinvestment while
AtlasFlow held cash ahead of January payroll and the Kestrel earn-out.

The Q4 2025 report, prepared January 14, 2026, reviewed by the CFO, and delivered to the Audit Committee
January 30, reported no exceptions, having computed every concentration against the September 30 portfolio of
$63,200. The numerator was right, the denominator was stale, and nobody in the review chain recomputed a
percentage.

### What the Engagement Team Did

The team recomputed all ten non-Treasury concentrations from the position-level extract (Exhibit 8-12),
finding Harborview at 5.72% and Ardsley at 4.98%; traced the Q4 denominator to the September 30 custodian
statement; read the policy in force from board minutes, confirming that §3.3 carries no "at the time of
purchase" qualifier where §3.1's rating limit does; recomputed Q1 through Q3, finding the same stale method in
Q3 with no limit exceeded; inspected the January 30 Audit Committee minutes; and read draft Item 7A against
the recomputed schedule.

### Analysis

**Is the balance sheet misstated?** No. Harborview is carried at fair value of $3,100 with a $4 unrealized
loss and a nil credit allowance, and a policy limit is not a measurement input.

**Is there a control deficiency?** Yes, and it is not the breach but the report. The quarterly report is a
monitoring control management relies on and represents to the Audit Committee, and it failed to detect a
condition it exists to detect, for a reason that would make it miss any exception arising from portfolio
contraction. The same defect in Q3 makes it a recurring failure rather than a slip.

**Is there a disclosure matter?** Yes, but only because of Item 7A. Policy compliance is not a required
disclosure, and a 5.72% position in A-1 paper maturing in 65 days is not a significant concentration under ASC
825-10-50. What creates the matter is management's affirmative statement of compliance in other information,
which AS 2710 requires the auditor to read for inconsistency with audit knowledge.

**How severe is the deficiency?** A stressed 2% default probability and 60% loss given default on $3,104
maturing in 65 days indicates $37, or 2.6% of overall materiality — on magnitude alone a **deficiency**. Two
facts push toward **significant deficiency**: the control is management's reporting to the Audit Committee, so
its failure degrades the body overseeing the risk, and it aggregates with CT-1, CT-2, and CT-4 into a pattern
of treasury controls operating without independent recomputation. The team concluded **significant deficiency
on an aggregated basis**.

**What would move the answer?** An "at the time of purchase" qualifier in §3.3 would eliminate the breach, the
deficiency, and the Item 7A inconsistency together, and a documented CFO recomputation reaching that reading
would reduce it to an inadequate-documentation observation. A materially larger position, a
below-investment-grade issuer, an exception concealing a real credit loss, or the same stale denominator
applied to the maturity and credit-quality limits would move it toward material weakness, because no limit
would ever have been independently tested.

### Resolution and Conclusion

Two cures were available: selling $411 of Harborview, bringing it to 4.99% of a $53,789 portfolio, or
reinvesting to raise the denominator above $62,000. Management reinvested, purchasing $8,000 of Treasury bills
on January 6, 2026 and bringing the portfolio to $62,200, at which Harborview is 4.98%. That corrects the
condition prospectively and changes neither the December 31 condition nor the ICFR conclusion at that date;
had management sold, the team would have evaluated the sale against the AFS classification and recognized the
$4 realized loss in earnings.

Management amended Item 7A to state that one position was 5.7% of the portfolio at December 31, 2025 against a
5% limit, that it arose from contraction rather than purchase, and that it was cured January 6, 2026.
Treasury's template now computes concentrations from the measurement-date portfolio, and the CFO's review
requires recomputation of the two largest positions. The internal control report was unaffected, the
aggregated finding being a significant deficiency rather than a material weakness.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                   WP 3200-14
AtlasFlow, Inc. -- Audit of the financial statements and internal control
over financial reporting for the year ended December 31, 2025

INVESTMENT POLICY COMPLIANCE -- SINGLE-ISSUER CONCENTRATION

Prepared by:  C. Nwosu (CN), Audit senior             Date: 02/04/2026
Reviewed by:  G. Lindqvist (GL), Senior manager       Date: 02/07/2026
Reviewed by:  D. Whitcombe (DW), Engagement partner   Date: 02/11/2026
Cross-reference: WP 3200-11 (portfolio lead schedule); WP 8400-11
(deficiency evaluation); WP 3100-04 (cash and investments lead)

PURPOSE
To recompute compliance with Section 3.3 of the board-approved investment
policy at December 31, 2025, to evaluate the severity of the deficiency in the
quarterly compliance reporting control, and to evaluate the Item 7A statement
of policy compliance under AS 2710.

SOURCE OF INFORMATION
1. JPMorgan custodian position statement at 12/31/2025 (obtained directly from
   the custodian, 01/16/2026) -- 15 positions, fair value $54,200.
2. Investment Policy Statement adopted 03/09/2023, amended 04/24/2025, obtained
   from the board minutes of those dates.
3. Treasury quarterly compliance reports Q1-Q4 2025; Audit Committee minutes of
   01/30/2026; trade confirmation for the Harborview purchase, 10/09/2025.

PROCEDURES PERFORMED
1. Recomputed all ten non-Treasury issuer concentrations from the custodian
   statement.  Largest: Harborview $3,100 / $54,200 = 5.72%.  Second: Ardsley
   $2,700 / $54,200 = 4.98%.
2. Recomputed at the 10/09/2025 purchase date: $3,104 / $63,200 = 4.91%, and
   traced the $9,000 of November-December maturities to the custodian
   statements, confirming the exception arose from denominator contraction.
3. Read policy Section 3.3: no "at the time of purchase" qualifier, in contrast
   to Section 3.1, which contains one for ratings.
4. Traced the Q4 report denominator to the 09/30/2025 custodian statement
   ($63,200); recomputed Q1-Q3, finding the same method used in Q3.
5. Inspected Audit Committee minutes of 01/30/2026: no concentration
   discussion; report accepted as presented.
6. Agreed the 01/06/2026 purchase of $8,000 of US Treasury bills to the
   custodian statement and recomputed: $3,100 / $62,200 = 4.98%.
7. Read draft Item 7A against the recomputed schedule.

RESULTS
A. Policy exception at 12/31/2025: Harborview at 5.72% against a 5.00% limit;
   excess position size $390; not escalated and not reported.
B. No misstatement.  Carried at fair value $3,100 (amortized cost $3,104);
   credit allowance nil per ASC 326-30.
C. Deficiency: the quarterly report computes concentrations against a
   prior-quarter denominator and so cannot detect an exception arising from
   portfolio contraction.  Present in Q3 and Q4 2025.
D. Stressed exposure (2% default probability, 60% loss given default) on
   $3,104 = $37, or 2.6% of overall materiality of $1,450.
E. Item 7A as drafted was materially inconsistent with audit knowledge;
   management amended the disclosure on 02/09/2026.

CONCLUSION
The condition at 12/31/2025 is a policy exception, not a misstatement.  The
reporting control failure is a control deficiency; evaluated with CT-1, CT-2,
and CT-4 (WP 8400-11) it is a SIGNIFICANT DEFICIENCY in the treasury control
environment, communicated in writing to the Audit Committee on 02/13/2026 under
AS 1305.  It is not a material weakness: the maximum plausible misstatement is
$37 and the custodian statement independently records every position.  Amended
Item 7A resolves the AS 2710 matter.  Cash and short-term investments as
presented -- $96,400 and $54,200 -- are fairly stated.
```

### Lessons

Recompute the denominator, not just the numerator. Read the limit's timing qualifier: §3.1 and §3.3 of the
same policy are tested at different moments and only one says so. A monitoring control reporting "no
exceptions" is an assertion to be tested, and the cheapest test is to recompute the two largest positions. A
subsequent-period cure does not change an as-of-date ICFR conclusion. And when management asserts compliance
in other information, a treasury question becomes an AS 2710 matter with a disclosure consequence.

## Common Mistakes

### Mistake 8.1 — Treating a reconciliation that foots as a reconciliation that reconciles

**What it looks like.** The workpaper recomputes $42,890 − $1,410 = $41,480, agrees it to the trial balance,
and concludes. **Why it happens.** Footing takes a minute; testing the item list means reading a statement.
**What goes wrong.** The $180 charge is absent from both sides, so the schedule foots — and kites foot too.
**How to avoid it.** Read the statement line by line and investigate any recurring reconciling item that has
disappeared.

### Mistake 8.2 — Putting a book-side item on the bank side

**What it looks like.** A bank charge, returned item, or bank-credited interest adjusts the *bank* balance.
**Why it happens.** The preparer works backward from the ledger balance, placing items wherever the schedule
foots. **What goes wrong.** The schedule ties to an unadjusted ledger balance and the required entry is never
proposed. **How to avoid it.** Recorded by the bank and not the entity adjusts the *book* balance; the reverse
adjusts the *bank* balance.

### Mistake 8.3 — Believing the standard confirmation proves the account population

**What it looks like.** "Confirmations were received from all institutions; the account population is
complete." **Why it happens.** The form's promise to note other accounts coming to its attention reads like a
search. **What goes wrong.** An account at an unlisted institution is invisible to the whole confirmation
cycle. **How to avoid it.** Perform the Exhibit 8-4 procedures that do not depend on management's listing.

### Mistake 8.4 — Skipping the deposits-in-transit test because the balance is nil

**What it looks like.** The reconciliation shows nil deposits in transit and the workpaper says "none — not
tested." **Why it happens.** A nil balance looks like nothing to test. **What goes wrong.** Nil is an
assertion, and an omitted deposit originating December 31 understates cash undetected. **How to avoid it.**
Examine every credit in the first five to eight business days of the new period and trace each to its
originating receipt.

### Mistake 8.5 — Measuring the three-month criterion from the wrong date

**What it looks like.** A Treasury bill with 22 days remaining is classified as a cash equivalent. **Why it
happens.** "So near maturity that interest-rate risk is insignificant" reads as a remaining-maturity test.
**What goes wrong.** ASC 230-10 measures original maturity from the acquisition date, so a 168-day bill never
qualifies and the caption, the statement of cash flows, and any covenant computed on cash are wrong. **How to
avoid it.** Compute maturity less acquisition date from the trade confirmation.

### Mistake 8.6 — Concluding on the interbank transfer schedule using management's list

**What it looks like.** Treasury provides a schedule of eight transfers and the auditor agrees four dates on
each. **Why it happens.** The population looks self-evidently complete. **What goes wrong.** A kited transfer
is not on a list prepared by the person who kited it. **How to avoid it.** Build the population from the bank
statements of all accounts across the window, then reconcile it to management's schedule.

### Mistake 8.7 — Booking the kiting adjustment and closing the workpaper

**What it looks like.** A $2,400 overstatement is corrected, the reconciliation re-footed, and the section
signed off. **Why it happens.** Correcting the number answers the question the workpaper was opened to answer.
**What goes wrong.** A check transfer between the entity's own accounts recorded in a period chosen by the
person who wrote it is a fraud indicator. **How to avoid it.** Under AS 2401, extend the window, examine prior
quarter ends, identify who authorized both sides, and communicate to the audit committee.

### Mistake 8.8 — Testing the investment policy by reproducing management's computation

**What it looks like.** The workpaper agrees each percentage in Treasury's report to the report's own
schedule. **Why it happens.** Agreeing to a schedule feels like testing. **What goes wrong.** A stale
denominator, a simple rather than weighted maturity average, or an omitted position reproduces exactly. **How
to avoid it.** Recompute every limit from the custodian's position statement and the policy version in force
at each purchase date.

### Mistake 8.9 — Grading a treasury deficiency by how alarming it sounds

**What it looks like.** Missing positive pay graded a material weakness, or self-approved wires a deficiency,
with no arithmetic either way. **Why it happens.** Treasury controls carry fraud connotations that substitute
for magnitude analysis. **What goes wrong.** Severity under AS 2201 and AU-C 265 turns on the magnitude the
failure could permit and the likelihood of detection, not on the control's name. **How to avoid it.** Quantify
the exposure, state the compensating controls, and give the range.

### Mistake 8.10 — Computing the covenant using management's definition of liquidity

**What it looks like.** The workpaper agrees the certificate's $150,600 to the balance sheet and concludes.
**Why it happens.** The certificate ties to the financial statements and headroom is large. **What goes
wrong.** The agreement's definition may exclude foreign cash, restricted cash, or non-Permitted Investments,
so the conclusion is right and the method is not. **How to avoid it.** Read the defined term, compute each
component from the ledger, and present both computations with the reconciliation between them.

## Practice Exercises

### Exercise 8-1 [Foundational]

The account 1015 reconciliation at December 31, 2025 shows a bank balance of $4,120, outstanding payroll
checks of $220 (31 checks, 9 of them totalling $56 more than 180 days old), and no deposits in transit. (a)
Compute the book balance the reconciliation should support. (b) Do the 9 stale-dated checks require an
adjusting entry, and why? (c) Express the $56 as a percentage of the $72 clearly trivial threshold.

### Exercise 8-2 [Foundational]

Classify each item at December 31, 2025 as a cash equivalent, a short-term investment, or neither, with the
authority: (a) a government money market fund of $1,200 with daily redemption and no gates or fees; (b) a
$6,800 Treasury bill maturing January 22, 2026, acquired August 7, 2025; (c) a $2,000 Treasury bill acquired
November 14, 2025 maturing February 5, 2026; (d) $310 of cash collateral securing a standby letter of credit
expiring in 2029; (e) $214 held by Stripe under a two-business-day rolling payout with no reserve.

### Exercise 8-3 [Intermediate]

Recompute the weighted-average maturity of the commercial paper sub-portfolio from these fair values and days
to maturity: Harborview $3,100 / 65 days; Ardsley $2,700 / 44; Calverton $2,600 / 22; Pinewood $2,300 / 99;
Thornbury $1,900 / 58; Vantage Grove $500 / 16. Show the weighted-day total and the average, and the figure a
simple unweighted average would report.

### Exercise 8-4 [Intermediate]

Marchmont Retail 4.05% notes maturing December 4, 2026 have an amortized cost of $2,668 and a fair value of
$2,600. The issuer is rated A- and has made every scheduled payment, AtlasFlow has neither the intent nor an
expectation of being required to sell, and the present value of expected cash flows at the effective rate is
$2,671. Compute the allowance for credit losses and the amount in other comprehensive income, and state the
entry.

### Exercise 8-5 [Intermediate]

Recompute the US-dollar carrying amounts from these confirmed local-currency balances and independent December
31, 2025 rates, and compute the difference from the recorded $7,600, $3,200, and $1,100: GBP 5,993.7 at
1.26800; AUD 4,992.2 at 0.64100; INR 93,856.7 at 0.01172. Then state what you would do had the AUD account
been recorded at the FY2025 average rate of 0.65500.

### Exercise 8-6 [Advanced]

For each transfer below (in thousands), state whether cash is misstated and by how much, and what reconciling
item, if any, must appear on which reconciliation.

| # | Amount | From | To | Disb. per books | Disb. per bank | Rec. per books | Rec. per bank |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | 1,800 | 1020 | 1010 | 12/29/2025 | 12/29/2025 | 12/29/2025 | 12/29/2025 |
| B | 2,400 | 1020 | 1010 | 01/02/2026 | 01/02/2026 | 12/30/2025 | 12/31/2025 |
| C | 900 | 1020 | 1010 | 12/31/2025 | 01/05/2026 | 12/31/2025 | 01/02/2026 |
| D | 1,500 | 1010 | 1015 | 12/31/2025 | 12/31/2025 | 01/02/2026 | 01/02/2026 |

### Exercise 8-7 [Intermediate]

Find the errors in the following client-prepared reconciliation and state the correcting entries.

| Line | Description | Amount |
| --- | --- | --- |
| 1 | Balance per bank statement | 42,890 |
| 2 | Less: outstanding checks | (1,410) |
| 3 | Less: bank service charge per December statement, not recorded | (180) |
| 4 | Add: deposit in transit (lockbox batch received January 2, 2026) | 240 |
| 5 | Less: unreconciled difference — under investigation | (240) |
| 6 | Balance per general ledger | 41,300 |

### Exercise 8-8 [Advanced]

Assume the Stripe agreement is amended effective November 1, 2025 to impose a 10% rolling reserve held for 90
days, so that at December 31, 2025 Stripe holds $214 of settled funds payable within two business days plus
$186 of reserve. Conclude on the classification of each amount, state the authority and the disclosure
consequence, and express each as a percentage of overall materiality of $1,450.

### Exercise 8-9 [Advanced]

Grade the severity of the absence of positive pay on account 1015 on these revised facts: FY2025 volume of
1,340 checks totalling $9,460; largest single check $420; no monthly review of check images; the Treasury
Manager is sole portal administrator; 47 outstanding checks totalling $780 at year end. Compare each figure to
overall materiality of $1,450 and performance materiality of $940, conclude, and identify the further evidence
that would most change your answer.

### Exercise 8-10 [Intermediate]

Draft the two numbered request paragraphs of a supplemental confirmation letter that would elicit (i) every
restriction, minimum-balance, compensating-balance, right-of-setoff, and account-control-agreement arrangement
affecting any account, and (ii) every contingent liability including standby letters of credit. Use letter
language and specify the fields you require.

### Exercise 8-11 [Advanced]

Draft a memorandum paragraph of 120 to 180 words concluding on the $40,000 minimum-liquidity covenant from
these figures: cash and cash equivalents $96,400, of which domestic $84,500 and foreign $11,900; short-term
investments $54,200; restricted cash $310; revolver commitment $50,000, undrawn; FY2025 operating cash inflow
$34,400; management's certificate dated January 30, 2026 asserting liquidity of $150,600. State the result
under the agreement's definition, the certificate's defect, and your conclusion.

### Exercise 8-12 [Advanced]

Spanning Chapters 6, 7, and 8: recompute FY2025 cash collected from customers. Net invoicing per the Chapter 6
billings bridge is $162,450. Gross accounts receivable is $38,600 at December 31, 2025 (trade $36,900 plus
Stripe self-serve $1,700) and $30,500 at December 31, 2024 (net $29,150 plus allowance $1,350). The allowance
moved from $1,350 to $1,900 and the FY2025 provision for credit losses is $1,780. Compute write-offs and cash
collected, and give the two most likely explanations for a $400 difference from customer receipts posted to
accounts 1010 and 1020.

## Solutions to Practice Exercises

### Solution 8-1

(a) $4,120 − $220 = **$3,900**, agreeing to account 1015 in Exhibit 8-1. (b) No entry: an unpresented check
leaves both balances correct. The stale checks are an unclaimed property exposure, so the absence of an
escheatment process is an observation rather than an ICFR deficiency. (c) $56 ÷ $72 = **77.8%**.

### Solution 8-2

(a) **Cash equivalent** (ASC 305-10; ASC 230-10-20). (b) **Short-term investment:** original maturity from
acquisition is 168 days regardless of the 22 days remaining. (c) **Cash equivalent:** 83 days from
acquisition. (d) **Neither** — restricted cash, noncurrent because the restriction runs to 2029, in the
statement of cash flows totals under ASU 2016-18 and identified under S-X Rule 5-02.1. (e) **Neither** — a
receivable from a payment processor, though cash equivalent is a defensible alternative given two-day
convertibility.

### Solution 8-3

Weighted days: 201,500 + 118,800 + 57,200 + 227,700 + 110,200 + 8,000 = **723,400 thousand-days** on $13,100
of fair value, so the weighted-average maturity is **55.2 days**. The simple average is 304 ÷ 6 = **50.7
days**, understating it by 4.5 days because the shortest-dated position, Vantage Grove at 16 days, carries the
smallest weight ($500) yet one-sixth of an unweighted average. Against a 365-day limit the error never surfaces.

### Solution 8-4

The unrealized loss is $2,668 − $2,600 = $68. Neither the intent nor the more-likely-than-not requirement to
sell is present, so decompose: the credit component is amortized cost less the present value of expected cash
flows, and $2,668 − $2,671 is negative, so **the allowance is nil** and the full **$68 stays in other
comprehensive income** — debit accumulated other comprehensive loss $68, credit the securities valuation
account $68. The alternative answer, that a 2.55% decline warrants an allowance, is weaker because ASC 326-30
measures the credit component by expected cash flows.

### Solution 8-5

£5,993.7 × 1.26800 = **$7,600**; A$4,992.2 × 0.64100 = **$3,200**; ₹93,856.7 × 0.01172 = **$1,100**, so
recomputed $11,900 against recorded $11,900 and the **difference is nil**. At the average rate of 0.65500 the
AUD account would be $3,270, overstating cash by **$70** — below the clearly trivial threshold individually
but a systematic method error, so recompute every foreign account and test whether the same rate column was
used elsewhere in the consolidation workbook (weakness W-8).

### Solution 8-6

**A. No misstatement;** both book dates fall in FY2025 and both banks settled December 29. **B. Kite — cash
overstated by $2,400,** the receipt being in FY2025 and the disbursement in FY2026. Reverse the December 30
receipt; no reconciling item cures it, and AS 2401 requires fraud consideration. **C. No misstatement,** but a
$900 outstanding check must appear on the 1020 reconciliation and a $900 deposit in transit on 1010. **D. Cash
understated by $1,500** — the mirror image, the $1,500 being in neither account at December 31.

### Solution 8-7

Three errors. **Line 3 is on the wrong side:** a charge recorded by the bank and not the entity adjusts the
*book* balance and requires an entry — debit account 6300 $180, credit account 1010 $180. **Line 4 is not a
deposit in transit:** a lockbox batch received January 2, 2026 belongs in neither December balance, so
including it overstates cash by $240. **Line 5 is a plug**, an "unreconciled difference" equal to the improper
line 4 being the signature of a forced reconciliation. Corrected: $42,890 − $1,410 = $41,480 against a
corrected ledger balance of $41,300.

### Solution 8-8

The **$214** payable within two business days is a receivable from the processor, 14.8% of overall
materiality, for the §8.7.1 reasons. The **$186** reserve is neither cash nor available, because collection
depends on 90 days of chargeback experience, so present it in other current assets, disclose the arrangement,
and consider an allowance for expected chargebacks. Presenting both as cash would misclassify $400, or 27.6%
of materiality.

### Solution 8-9

A **significant deficiency**, with a defensible case for a material weakness. Check volume of $9,460 is 652%
of overall materiality and 1,006% of performance materiality, and the largest single check of $420 is 29% of
materiality. Unlike the actual facts there is no compensating detective control, so a fraudulent check is
detected only by the monthly reconciliation. **The most useful further evidence is the population of checks
clearing 1015 reconciled to the register:** an item that cleared but was never issued makes it a material
weakness.

### Solution 8-10

```text
4.  RESTRICTIONS, COMPENSATING BALANCES, AND SETOFF.  For each account of
    AtlasFlow, Inc. or any subsidiary, please state (i) any restriction on our
    ability to withdraw or transfer funds, with its source and the amount
    affected; (ii) any minimum, average, or compensating balance arrangement,
    contractual or informal, with the required level, the measurement period,
    and each month during the year ended December 31, 2025 in which the level
    was not met; (iii) any right of setoff, banker's lien, pledge, or security
    interest you hold in any account, with the obligation secured; and (iv) any
    deposit account control or blocked account agreement.  If none, please state
    "none" for each of (i) through (iv).

5.  CONTINGENT LIABILITIES.  Please list each standby or documentary letter of
    credit, guarantee, endorsement, banker's acceptance, or other contingent
    obligation issued by you for our account and outstanding at December 31,
    2025, stating the reference number, beneficiary, face amount, currency,
    issue and expiry dates, the collateral pledged, and the account holding any
    cash collateral.
```

### Solution 8-11

```text
Minimum-liquidity covenant -- conclusion.  The First Meridian revolving credit
agreement requires Liquidity of not less than $40,000 at each quarter end,
defined as unrestricted cash of the Borrower and its domestic subsidiaries held
in controlled accounts plus Permitted Investments.  On that definition at
December 31, 2025, Liquidity is $138,700 -- domestic unrestricted cash of
$84,500 (accounts 1010 $41,300, 1015 $3,900, 1020 $38,100, 1045 $1,200) plus
short-term investments of $54,200, all of which are Permitted Investments --
producing headroom of $98,700, or 3.47 times the requirement.  Under the
strictest reading, excluding investments, Liquidity is $84,500 and headroom is
$44,500; a breach would require a 52.7% decline in domestic cash against FY2025
operating cash inflow of $34,400 and an undrawn $50,000 commitment.  The
covenant is met on every reading.  Management's certificate dated January 30,
2026 asserted Liquidity of $150,600, which includes $11,900 of foreign
subsidiary cash and $310 of restricted cash that the definition excludes; the
certificate reached the correct conclusion by a method the agreement does not
authorize, which we have communicated to management and the Audit Committee.
```

### Solution 8-12

Write-offs: $1,350 + $1,780 − $1,900 = **$1,230**. Cash collected: $30,500 + $162,450 − $1,230 − $38,600 =
**$153,120**. The two most likely explanations for a $400 residual are an incomplete receipts population —
foreign-entity collections settle to Barclays (1030), NAB (1035), and HDFC (1040), and self-serve collections
arrive as Stripe payouts — and foreign-currency movement, since a receivable recorded at one rate is collected
at another and the difference lands in other income rather than in the roll-forward.

## Review Questions

**RQ 8-1.** Why is inherent risk for the existence of a bank balance low while inherent risk for
misappropriation of the same balance is high?

**RQ 8-2.** Name the three things the standard financial institution confirmation form asks for, and state
what it expressly does not undertake to do.

**RQ 8-3.** Give four categories of information the standard form does not cover that a supplemental letter
should request.

**RQ 8-4.** What is the most important difference between AS 2310 and AU-C 505 for a cash audit?

**RQ 8-5.** Explain the rule that determines whether a reconciling item adjusts the bank side or the book
side, and why misplacement matters.

**RQ 8-6.** Why does a kite leave both bank reconciliations in balance?

**RQ 8-7.** Which two dates on an interbank transfer schedule prove or disprove a kite, and which two
determine whether a reconciling item is required?

**RQ 8-8.** Distinguish kiting, lapping, and window dressing by what each misstates.

**RQ 8-9.** From what date is the three-month cash equivalent criterion measured, and why does that matter for
a Treasury bill with 22 days remaining?

**RQ 8-10.** State the difference between restricted cash and a compensating balance arrangement, and the
presentation consequence of each.

**RQ 8-11.** What evidence contradicts a held-to-maturity classification, and what changes if the
classification moves from available-for-sale to held-to-maturity?

**RQ 8-12.** Set out the order of the ASC 326-30 analysis for an available-for-sale debt security in an
unrealized loss position.

**RQ 8-13.** Why is a completed bank confirmation not evidence about the completeness of the bank account
population, and name three procedures that are?

**RQ 8-14.** Why does an independent recomputation of interest income help with the unknown-account risk, and
what is its principal limitation?

**RQ 8-15.** Under ASU 2016-18, what amounts must the statement of cash flows reconcile, and what disclosure
is required when they are not in a single balance sheet line?

**RQ 8-16.** Why does an undrawn credit facility's covenant still require testing?

## Answers to Review Questions

**RQ 8-1.** The balance is externally set, homogeneous, free of estimates, and compared to an external record
monthly, so a misstatement is unlikely to arise or persist. Misappropriation risk is high for an unrelated
reason: cash needs no conversion step, and a fraudulent disbursement is recorded accurately.

**RQ 8-2.** The balance of each deposit account the auditor lists at a stated date; the balance, due date,
rate, and collateral of each direct liability the auditor lists; and any additional deposit or loan accounts
coming to the institution's attention while completing the form — expressly without a comprehensive search of
its records.

**RQ 8-3.** Contingent liabilities such as standby letters of credit; restrictions, compensating balances,
rights of setoff, and account control agreements; facility terms including covenants; and property held in
safekeeping. A fifth worth requesting is the authorized-signer and portal-administrator list.

**RQ 8-4.** AS 2310 requires confirmation of cash held by third parties and AU-C 505 contains no such
requirement, so a private-company auditor can satisfy AU-C 330 by obtaining statements directly from the
institution and testing the reconciliation.

**RQ 8-5.** An item recorded by the bank and not the entity adjusts the book balance and requires an entry;
the reverse adjusts the bank balance and requires none. Misplacement makes the schedule foot to an unadjusted
ledger balance, so the required entry is never proposed.

**RQ 8-6.** On the receiving side the deposit is recorded and credited before period end, so both balances
include it; on the disbursing side the check has cleared neither the bank nor the books, an unrecorded
disbursement never reaching the outstanding check list.

**RQ 8-7.** The two book dates prove or disprove the kite: in different periods, cash is misstated by the
transfer amount. The two bank dates determine the reconciling items, because where they straddle the period
end an outstanding check belongs on the disbursing reconciliation and a deposit in transit on the receiving
one.

**RQ 8-8.** Kiting overstates cash by counting one amount in two accounts. Lapping misstates the composition
of receivables, not the cash total. Window dressing misstates nothing but may make the period-end balance
unrepresentative and therefore a disclosure matter.

**RQ 8-9.** From the acquisition date. A bill acquired 168 days before maturity is not a cash equivalent even
with 22 days left; remaining maturity matters to liquidity and maturity-limit testing, not to classification.

**RQ 8-10.** Restricted cash cannot be withdrawn because of a legal or contractual limitation, so it is
presented outside the cash caption or identified within it under S-X Rule 5-02.1, classified by the period of
restriction, and included in the statement of cash flows totals under ASU 2016-18. A compensating balance
leaves the cash available, so it stays in the caption and is disclosed where a level is required.

**RQ 8-11.** A sale before maturity for liquidity contradicts positive intent, as does a stated liquidity
purpose. Held-to-maturity would carry $54,431 of amortized cost rather than $54,200 of fair value, remove the
$231 unrealized loss from accumulated other comprehensive loss, and move the portfolio to ASC 326-20.

**RQ 8-12.** First, whether the entity intends to sell; if so, write down to fair value through earnings.
Second, whether it is more likely than not to be required to sell before recovery; if so, the same result.
Third, measure the credit component as amortized cost less the present value of expected cash flows, recognize
it as an allowance through earnings capped at amortized cost less fair value, and leave the remainder in OCI.

**RQ 8-13.** Because the auditor supplies the account list from management's records, and the form's
undertaking to note other accounts is an invitation to volunteer. Three procedures that do test completeness:
a ledger sweep of cash-named and nil-balance accounts, extraction of distinct originating routing numbers from
the ACH and wire files, and recomputation of interest income.

**RQ 8-14.** An unidentified interest-bearing account produces interest income the auditor cannot attribute,
so an unexplained residual points outside the confirmed population. Its limitation: a non-interest-bearing
account — the kind a disbursement fraud uses — leaves no residual.

**RQ 8-15.** The beginning and ending amounts must comprise cash, cash equivalents, and restricted cash and
restricted cash equivalents, with a reconciliation to the balance sheet captions where they are not in a
single line.

**RQ 8-16.** A breach permits the lender to terminate the commitment, removing the facility from stated
liquidity. That matters to the going-concern evaluation, to the ASC 326-30 "required to sell" conclusion, and
to the liquidity disclosure.

## Key Definitions

**Account analysis statement.** The monthly bank statement of services, per-item charges, the earnings credit
on average collected balances, and the net settled amount. It is the source document for charges appearing on
no other page.

**Available-for-sale (AFS) debt security.** A security classified under ASC 320-10 as neither held-to-maturity
nor trading: fair value, unrealized gains and losses in other comprehensive income, credit losses under ASC
326-30.

**Bank confirmation.** A request sent by the auditor to an institution and returned directly to the auditor.
Required for cash held by third parties under PCAOB AS 2310; not required by AICPA AU-C 505.

**Cash equivalent.** A short-term, highly liquid investment readily convertible to a known amount of cash and
so near maturity that interest-rate risk is insignificant — generally an original maturity of three months or
less from the acquisition date (ASC 230-10-20).

**Compensating balance.** A minimum, average, or informal balance maintained in connection with a borrowing or
banking relationship. It does not make the cash restricted; disclosure follows where a level is required.

**Deposit in transit.** A receipt recorded on or before the period end that the bank has not yet credited.
Added to the bank balance and requiring no entry; a fictitious one overstates cash directly.

**Fair value hierarchy.** The three-level ASC 820-10 ranking of inputs: Level 1 quoted prices in active
markets for identical assets, Level 2 other observable inputs including evaluated prices, Level 3 unobservable
inputs.

**Held-to-maturity (HTM) security.** A security the entity has the positive intent and ability to hold to
maturity, at amortized cost with credit losses under ASC 326-20. A sale before maturity for liquidity
contradicts the intent.

**Interbank transfer schedule.** A schedule of every transfer between the entity's own accounts in a window
straddling the period end, carrying four dates each — disbursement and receipt, per books and per bank — used
to detect kiting.

**Kiting.** Overstating cash by recording a transfer between accounts as a receipt in one period and a
disbursement in a later one, exploiting float. It leaves both bank reconciliations in balance.

**Minimum-liquidity covenant.** A covenant requiring liquidity, as defined in the credit agreement, at or
above a stated level at specified dates. The defined term governs and frequently excludes foreign and
restricted cash.

**Outstanding check.** A recorded disbursement the bank has not yet paid. Deducted from the bank balance and
requiring no entry; an understated list is the vehicle for a disbursement fraud.

**Payment-file integrity.** The control objective that the file transmitted to the bank holds the same items
and totals as the approved payment run, evidenced by agreeing entry count, entry hash, and amounts to the
register.

**Positive pay.** A bank service under which the entity transmits its issued-check file daily and the bank
presents any non-matching item for a pay or return decision. Its absence removes the only control over an item
never issued.

**Processor float.** Funds collected by a payment processor and not yet paid out. Whether it is cash turns on
whether the merchant controls timing and use and whether the funds are segregated; often a receivable.

**Restricted cash.** Cash whose withdrawal or use is limited by legal or contractual restriction, such as
letter-of-credit collateral. Identified under S-X Rule 5-02.1, classified by the period of restriction, and
included in the statement of cash flows totals under ASU 2016-18.

**Single-issuer concentration limit.** A policy limit on exposure to one issuer as a percentage of the
portfolio. Being a ratio, it can be breached by portfolio contraction with no purchase, so recompute the
denominator.

**Sweep account.** An arrangement moving balances automatically between an operating account and an investment
vehicle daily. If the vehicle is a cash equivalent, sweep movements are not investing activities.

**Vendor bank-change fraud.** A scheme in which a fraudster impersonating a vendor causes the entity to change
the vendor's remittance details, redirecting payments. The controlling procedure is callback to a number
already on file.

**Weighted-average maturity.** Position amount multiplied by days to maturity, summed and divided by the
portfolio total. A simple unweighted average is a different and generally smaller number.

**Window dressing.** Accelerating receipts and deferring disbursements around a period end so the reported
balance is unrepresentative. Nothing is misstated, but the practice may require disclosure.

## Chapter Summary

1. Cash carries low inherent risk for existence and accuracy — a third party sets the balance and a monthly
   reconciliation compares it to the ledger — and high inherent risk of misappropriation, because cash needs
   no conversion step. Small substantive testing, extensive control testing.
2. The misstatement risk that does exist sits in completeness of the account population, classification of
   near-cash items, whether reconciliations reconcile rather than merely foot, and double-counted transfers.
3. Confirming a balance does not confirm the population. Completeness needs independent procedures: the ledger
   sweep that found account 1050 with $1,940 of activity and a nil balance, and the $5,110 interest
   recomputation, which cannot detect a non-interest-bearing account.
4. Every reconciling item belongs on exactly one side. The $180 charge surfaced from reading the December
   statement line by line and comparing December's reconciliation to November's $168 item.
5. Testing outstanding checks from the January statement back to the list detects an unrecorded disbursement,
   and a nil deposits-in-transit balance is an assertion tested from the bank side.
6. A kite leaves both reconciliations in balance, so only an interbank transfer schedule built from bank
   statements detects it: the two book dates prove the kite, the two bank dates determine the reconciling
   items.
7. Cash equivalent classification turns on original maturity from acquisition, which is why a $6,800 bill with
   22 days left is a short-term investment and a $2,000 bill acquired with 83 days to run is a cash
   equivalent.
8. Classification precedes measurement, and ASC 326-30 measures the credit component against expected cash
   flows rather than the size of the decline, which is why all $231 of gross unrealized loss stayed in OCI.
9. Policy limits are recomputed, not reperformed. Harborview's 5.72% came from $9,000 of maturities shrinking
   the denominator, and the quarterly report missed it by using a prior-quarter portfolio.
10. Treasury deficiencies are graded with arithmetic — $986 of check volume, $312,600 of wire volume, four
    self-approved wires — and a covenant on an undrawn facility is still tested under the agreement's defined
    terms, the certified $150,600 having included $11,900 of foreign cash the definition excludes.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Materiality and the clearly trivial threshold | Chapter 3, §3.2 | The $1,450, $940, and $72 figures used throughout |
| The billings bridge and net invoicing of $162,450 | Chapter 6 | The starting figure for Exercise 8-12 |
| Receivables, cash receipts cut-off, and lapping detection | Chapter 7 | The receivable side of every receipt tested here, and account 1205's $1,700 |
| Equity and financing cash flows | Chapter 9 | The $11,300 financing section and the components of $(37,900) investing |
| Disbursement controls in the expenditure cycle | Chapter 10 | Purchase-to-pay authorization, held checks, and reversed disbursements |
| Treasury and bank portal system access | Chapter 11 | The design question behind CT-2 and sole portal administration |
| Payment fraud schemes | Chapter 17 | The taxonomy behind kiting, vendor bank-change fraud, and self-approved wires |
| Accumulating misstatements and communicating deficiencies | Chapter 19 | Where the corrected $180 and the aggregated significant deficiency are reported |

## Further Reading

- PCAOB AS 2310, *The Auditor's Use of Confirmation*, with the PCAOB staff implementation guidance, and AS
  2401 and AS 2201 for the fraud-response and internal control frameworks applied to the §8.12 findings.
- AICPA AU-C 505 and AU-C 501, the AICPA audit guide on investments in securities, and the standard financial
  institution confirmation form with its instructions.
- FASB ASC 305-10, ASC 230-10 including ASU 2016-18 (*Restricted Cash*), ASC 320-10, and ASC 326-30 with ASU
  2016-13 (*Financial Instruments — Credit Losses*).
- FASB ASC 820-10, ASC 825-10-50, and ASC 830-30, for hierarchy disclosures, credit risk concentrations, and
  translation.
- SEC Regulation S-X Rule 5-02 and Regulation S-K Items 303 and 305, with Division of Corporation Finance
  guidance on liquidity and capital resources disclosure.
- COSO *Internal Control — Integrated Framework*, for the monitoring component the quarterly compliance report
  occupies.



