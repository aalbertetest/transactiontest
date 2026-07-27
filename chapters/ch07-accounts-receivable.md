# Chapter 7 — Accounts Receivable, Contract Assets, and Credit Losses

> A SaaS receivable looks like the easiest balance in the file: short-dated, invoice-supported, converting to cash within
> weeks. Yet AtlasFlow's $38,600 gross receivable is 26.6 times the $940 performance materiality, its aged trial balance
> is a report no one had re-performed before January 2026, and the $1,900 allowance stapled to the bottom of it has a
> defensible range $630 wide.

## Learning Objectives

- **LO 7.1** Identify the relevant assertions for a SaaS receivable portfolio, assess inherent and control risk separately, and
  state which carry a significant risk.
- **LO 7.2** Test an aged trial balance as information produced by the entity: agreement to the general ledger, independent
  re-aging, and the aging cut-off.
- **LO 7.3** Apply the current PCAOB confirmation requirements — positive and blank-form design, control over the process,
  electronic intermediaries, second requests, and nonresponses.
- **LO 7.4** Perform a subsequent-cash-receipts test that matches receipts to specific invoices, and evaluate and project
  confirmation exceptions stratum by stratum.
- **LO 7.5** Distinguish a receivable from a contract asset and determine which balances enter the credit-loss pool.
- **LO 7.6** Compute expected credit losses by the loss-rate, roll-rate, and vintage methods; develop the current-conditions
  and forecast components; resolve reversion; and quantify overlays.
- **LO 7.7** Build an auditor range for an allowance, evaluate management's recorded amount against it, and measure the resulting
  misstatement.
- **LO 7.8** Design procedures over credit memos, disputes, write-offs, recoveries, concentrations, presentation, and 11,400
  low-value self-serve balances.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2310, *The Auditor's Use of Confirmation* (effective for fiscal years ending on or after June 15, 2025 — FY2025 is its first application to AtlasFlow) | AS 2310.24: confirm receivables from the transfer of goods or services, or directly access information held by a knowledgeable external source; .25 permits indirect external information only on a documented feasibility determination |
| PCAOB | AS 2310.08–.13 | Request design, the blank-form reliability trade-off, knowledgeable confirming parties, and the rule that negatives alone are never sufficient |
| PCAOB | AS 2310.14–.17, Appendix B | The auditor selects, sends, and receives; an intermediary's controls over interception and alteration must be understood, tested, and assessed for company override |
| PCAOB | AS 2310.18–.23, .27–.28, Appendices A and C | Response reliability, exceptions, nonresponses, alternative procedures, and audit committee communication where significant-risk receivables were not confirmed |
| PCAOB | AS 2501 (effective for fiscal years ending on or after December 15, 2023) | Test the process, develop an independent expectation, or examine subsequent events; evaluate each significant assumption and indicators of bias |
| PCAOB | AS 2810 | Accumulate and evaluate misstatements, including projections and an estimate at one end of a range of reasonable amounts |
| PCAOB | AS 1105, AS 2305, AS 2110, AS 2401 | Reliability of IPE; substantive analytics; assertion-level risk; the presumed revenue fraud risk, for which confirming terms and the absence of side agreements is a listed response |
| FASB ASC | 326-20, including 326-20-50 | Lifetime expected-loss allowance on trade receivables and contract assets, measured collectively where risk characteristics are similar, from historical loss information adjusted for current conditions and forecasts with reversion thereafter; roll-forward, past-due and credit-quality disclosure |
| FASB ASC | 606-10-45; 606-10-32 | Distinguishes a receivable from a contract asset and requires contract-level netting; an expected price concession is variable consideration, not a credit loss |
| FASB ASC | 275-10-50; SEC Regulation S-X Rules 5-02, 12-09 | Disclosure of concentrations of credit risk; separate presentation of the allowance and the valuation-account schedule |
| AICPA | AU-C 330, AU-C 505, AU-C 540 | AU-C 330 retains a rebuttable *presumption* that receivables will be confirmed; AU-C 505 governs design and evaluation; AU-C 540 is the estimates analogue to AS 2501 |

AtlasFlow is an SEC issuer, so PCAOB standards govern. Two differences matter in private-company work: AU-C 330's presumption is
rebuttable, whereas AS 2310.24 is an affirmative requirement with only a documented feasibility exception; and with no ICFR
opinion, the deviations in §7.8 and §7.11 feed an AU-C 265 communication rather than the Chapter 14 conclusion.

## Prerequisites and Chapter Dependencies

Read Chapter 4 (order-to-cash and revenue cut-off) and Chapter 6 (contract liabilities and the billings bridge) first; the
receivable is the mirror of deferred revenue, and account 1220 is split between the two chapters at the
receivable/contract-asset line. Chapter 3 supplies materiality: $1,450 overall, $940 performance materiality, $72 clearly
trivial. Sample-size derivation is deferred to Chapter 15, cash-receipt cut-off to Chapter 8, predictive analytics to
Chapter 18, and the accumulation of U-1 and U-2 to Chapter 19.

## 7.1 The Receivable Population and Its Risks

**Exhibit 7-1. Accounts receivable lead schedule at December 31, 2025 (in thousands).**

| Account | Description | 12/31/2025 | 12/31/2024 | % change |
| --- | --- | --- | --- | --- |
| 1200 | Accounts receivable — trade (enterprise) | 36,900 | 28,800 | 28.1% |
| 1205 | Accounts receivable — Stripe self-serve | 1,700 | 1,700 | 0.0% |
| | **Gross accounts receivable** | **38,600** | **30,500** | **26.6%** |
| 1210 | Allowance for credit losses | (1,900) | (1,350) | 40.7% |
| | **Net accounts receivable** | **36,700** | **29,150** | **25.9%** |
| 1220 | Unbilled receivables / contract assets | 3,400 | 2,100 | 61.9% |

The FY2024 split between accounts 1200 and 1205 is an extension for this chapter; the continuing case records the $30,500
total, the $1,350 allowance, and the $29,150 net figure.

Three features drive the design. Gross receivables are 26.6 times performance materiality, yet 2,876 of the 3,140 enterprise
customers carry less than $10 each and the 11,400 self-serve accounts average $149, so stratification is the only workable
design. Billing is annual and in advance, so a large invoice goes past due while the customer is being served and is satisfied,
making past-due status a weaker signal of credit distress than of a billing dispute — the reason §7.9 pools by cause as well as
by age. And the $1,900 allowance is 1.31 times overall materiality, so an estimate 40% wrong is material.

**Exhibit 7-2. Assertion-level risk assessment for accounts receivable and contract assets.** Significant risks in bold.

| Relevant assertion | IR / CR | Why, and the primary response |
| --- | --- | --- |
| **Existence** (late-December originations) | Moderate / High (W-3, W-12) | 41% of Q4 ACV signed December 24–31; a whistleblower alleged December deals were papered after the fact. Confirm with a side-agreement paragraph; blank forms there |
| Accuracy — gross | Moderate / Moderate | Amount, timing, and currency, not fabrication. Confirmation, subsequent receipts, re-performance of the aging |
| **Valuation — allowance** (estimation uncertainty) | High / High | Lifetime expected loss on a growing portfolio; gross retention down from 93% to 91%; a CFO in his fourth month. Independent expectation and range (§7.9) |
| Cut-off (within the existence risk) | High / High (W-12) | A December invoice for January performance overstates revenue and the receivable together. Exceptions, subsequent receipts, invoice scan |
| Rights | Low / Low | No factoring or pledged receivables; the revolver is undrawn. Read the revolver agreement |
| Presentation and disclosure | Moderate / Moderate | Netting, concentration, roll-forward, past-due disclosure (§7.12) |

The allowance is a significant risk for estimation uncertainty, not suspected fraud: the subjectivity sits in the loss rates,
the forecast overlay, and the treatment of distressed accounts, and a reasonable person can move the answer by $630. Existence
is significant only for the late-December subpopulation, which is what lets blank forms and side-agreement questions go where
they earn their cost.

## 7.2 The Aged Trial Balance as Information Produced by the Entity

The aged trial balance (**ATB**) supports the sampling population, the aging disclosure, and the entire loss-rate
computation. Under AS 1105 you must test its completeness and accuracy, and "agreed the total to the general ledger" is
not that test. Three properties are separable.

**Property 1 — it reconciles to the general ledger.** The Zuora aged receivable report ($36,900) plus the Stripe
uncollected-charges report ($1,700) equal $38,600, agreeing to accounts 1200 and 1205. Run the report yourself, capturing the
"as of" date, entity filter, currency basis, and the "include unapplied credits" toggle, and reconcile account counts (3,140 and
11,400) as well as dollars: a report that ties in dollars but holds 2,900 accounts has been filtered, usually to exclude the
credit balances §7.12 needs. A real difference is unapplied cash or a manual journal to 1200 with no subledger counterpart (a
W-12 matter) — substantiate it, never plug it.

**Property 2 — the buckets are computed correctly.** Re-age the population from invoice date plus contractual terms.

```sql
-- Re-age the enterprise receivable population independently of management's report.
-- Source: Snowflake replica of Zuora Billing (interface I-8), snapshot as of 2026-01-09.
SELECT CASE WHEN d <=  0 THEN '1 Current' WHEN d <= 30 THEN '2 1-30'
            WHEN d <= 60 THEN '3 31-60'   WHEN d <= 90 THEN '4 61-90'
            WHEN d <=180 THEN '5 91-180'  ELSE '6 Over 180' END AS bucket,
       COUNT(DISTINCT i.account_id) AS accounts,
       SUM(i.balance_usd)           AS open_balance_usd
FROM  (SELECT *, DATEDIFF(day, DATEADD(day, term_days, invoice_date),
                          DATE '2025-12-31') AS d
       FROM   zuora.invoice
       WHERE  posted_date <= DATE '2025-12-31'
         AND  balance_as_of_20251231 <> 0
         AND  entity IN ('ATLASFLOW_US','ATLASFLOW_UK','ATLASFLOW_AU')) i
GROUP BY 1 ORDER BY 1;
```

The due date is recomputed rather than read, because the stored field is editable; and because the snapshot is taken in January
for a December 31 position, the filter is on the balance *as of* December 31 using payment application dates. The tell that you
got the second point wrong is a re-aged population smaller than management's.

**Exhibit 7-3. Independent re-aging, and its effect on the pooled loss computation (in thousands).**

| Bucket (loss rate) | Draft ATB 01/06/2026 | Auditor re-aging | Loss on draft | Loss on re-aged |
| --- | --- | --- | --- | --- |
| Current, not yet due (0.4%) | 22,962 | 22,550 | 91.8 | 90.2 |
| 1–30 days past due (1.6%) | 8,190 | 8,190 | 131.0 | 131.0 |
| 31–60 days past due (6.0%) | 3,569 | 3,740 | 214.1 | 224.4 |
| 61–90 days past due (18.0%) | 1,879 | 1,970 | 338.2 | 354.6 |
| 91–180 days past due (42.0%) | 1,290 | 1,440 | 541.8 | 604.8 |
| Over 180 days past due (85.0%) | 710 | 710 | 603.5 | 603.5 |
| **Total** | **38,600** | **38,600** | **1,920.4** | **2,008.5** |

The total is unaffected, which is why a mis-aging survives a reconciliation-only test. The cause was mechanical: 26 invoices
carried terms other than net 30 (net 45 for three resellers, net 60 for four public-sector customers, net 15 on nineteen services
invoices) and the report applied one global 30-day assumption, understating the mechanical loss computation by $88.1. Management
re-ran the report with per-invoice terms on January 9, 2026, and the corrected aging is the one at §3.3. The deficiency is not a
significant one: the maximum plausible effect ($88, 6.1% of overall materiality) is below the level at which a reasonable
possibility of material misstatement arises. Document that magnitude analysis, because management's correction is not the
reason.

**Property 3 — the aging cut-off.** Two directional tests, performed at steps 3 and 11 of the walkthrough: invoices posted after
December 31 carrying a December invoice date (41 items, $612), and cash applications posted after December 31 with a December
value date (27 items, $304). The second direction is the one teams omit — an application *reduces* the receivable, so a
manipulated application date understates it — and cut-off on the receipts themselves belongs to Chapter 8, §8.4. Two of the ten
invoices vouched relate to contracts signed December 29–30 and form part of U-3.

## 7.3 Confirming Receivables

### 7.3.1 What the standard requires

AS 2310.24 requires the auditor either to confirm receivables from the transfer of goods or services or to obtain evidence by
directly accessing information held by a knowledgeable external source — Brightline read the customer supplier portal, with
authorization, for four of the fourteen AtlasFlow customers that operate one. Indirect external information is permitted by
AS 2310.25 only on a documented determination that direct evidence is not feasible; "the client asked us not to send
confirmations" is not such a determination. AS 2310.28 requires audit committee communication where significant-risk receivables
were confirmed by neither route.

**Negative confirmations.** AS 2310.12 makes negatives alone insufficient; AS 2310.13 allows them alongside other
substantive procedures where risk is low *and* controls are shown effective, items are many, small, and homogeneous, and a
low exception rate is expected. For the 11,400 self-serve accounts the second condition holds and the first does not: the
unremediated ITGC deficiencies (W-1, W-2, W-5, W-7) prevent any conclusion on controls over the Stripe path, and the only contact
data is a customer-supplied email address changeable without authentication. Brightline sent none there and relied on 100%
subsequent-settlement testing (§7.10).

### 7.3.2 Designing the sample

**Exhibit 7-4. Stratification of the enterprise population and the confirmation sample (in thousands, except counts).**

| Stratum (balance criterion) | Accounts | Balance | Selected | Balance selected | Coverage |
| --- | --- | --- | --- | --- | --- |
| 1 — at or above 470, being 50% of performance materiality | 22 | 20,290 | 22 | 20,290 | 100.0% |
| 2 — 100 to under 470 | 74 | 12,610 | 18 | 3,060 | 24.3% |
| 3 — 10 to under 100 | 168 | 3,290 | 10 | 240 | 7.3% |
| 4 — above nil to under 10 | 402 | 710 | — | — | — |
| 5 — nil or credit balance | 2,474 | — | — | — | — |
| **Total enterprise** | **3,140** | **36,900** | **50** | **23,590** | **63.9%** |

Chapter 15, §15.7 derives the sizes. Four design decisions carry the exhibit. The stratum 1 threshold is 50% of performance
materiality, so no untested balance can hold half of performance materiality alone; at $940 it would have held 9 accounts and
$12,610, leaving a larger and less precise projection. Stratum 4 is not sampled because all 402 accounts total $710 — 75.5% of
performance materiality even if every one were fictitious — and is covered by the subsequent-receipts scan in step 11; state and
quantify that scope decision. Stratum 5 is examined rather than ignored: 31 credit balances totaling $310 are liabilities
(§7.12). And three accounts were selected for risk indicators: the two channel balances and Northgate Financial Group with its
$180 SLA claim. AS 2310.09's knowledgeable, properly addressed party is decisive for the channel — AtlasFlow's receivable is from
Tessera, so a Cirrus response is evidence about a different asset.

### 7.3.3 The request

Brightline used a balance-stated positive request for 38 accounts and a **blank form** for the 12 whose balances arose
from contracts signed after December 15, 2025 — the subpopulation carrying the existence significant risk. The Note to
AS 2310.08 records the trade-off: a blank form can be more reliable because the confirming party must produce the
amount, but response rates fall. Brightline's blank forms returned 7 of 12 (58.3%) against 27 of 38 (71.1%).

**Exhibit 7-5. Text of the positive confirmation request (balance-stated form), FY2025.**

```text
[ATLASFLOW, INC. LETTERHEAD]
                                                                     January 12, 2026

Meridian Health Systems
Attn: Ms. Delia Fournier, Accounts Payable Manager
1400 Cypress Bend Parkway
Sacramento, CA 95814

Dear Ms. Fournier:

Our independent registered public accounting firm, Brightline LLP, is performing an audit of
our financial statements as of and for the year ended December 31, 2025. Please confirm
directly to Brightline LLP the information set out below regarding your account with
AtlasFlow, Inc. as of the close of business on December 31, 2025.

This is not a request for payment. Please do not send payment to Brightline LLP.

  Customer account number:                 AF-100418
  Amount owed to AtlasFlow, Inc. at
  December 31, 2025:                       USD 2,410,000

  Composition of the amount:

    Invoice        Invoice date   Due date       Amount (USD)   Description
    INV-0088214    12/05/2025     01/04/2026     1,240,000      Services, SOW-2 milestone 2
    INV-0087655    11/14/2025     12/14/2025       870,000      Services, SOW-2 milestone 1
    INV-0087102    11/30/2025     12/30/2025       150,000      Overage, November 2025
    INV-0086640    10/31/2025     11/30/2025       150,000      Overage, October 2025
                                                 ---------
    Total                                        2,410,000

Please complete and return this letter directly to Brightline LLP using the secure link in the
electronic request you have received, or by email to atlasflow.confirmations@brightlinellp.com,
or by mail to Brightline LLP, Attn: A. Trent, 600 Congress Avenue, Suite 2100, Austin, TX 78701.
Please do not return this letter to AtlasFlow, Inc.

Sincerely,

/s/ Elena Vasquez
Elena Vasquez
Chief Accounting Officer and Controller
AtlasFlow, Inc.

--------------------------------------------------------------------------------------------
TO BE COMPLETED BY THE CUSTOMER

[ ] The information above is correct as of December 31, 2025.

[ ] The information above does not agree with our records. Our records show an amount owed to
    AtlasFlow, Inc. at December 31, 2025 of USD ____________. Please describe the difference
    (for example, payments made, credits claimed, invoices not recorded, or amounts disputed):

    ______________________________________________________________________________________

Please also indicate:

  Do you have any agreement with AtlasFlow, Inc. relating to the amounts above other than the
  invoices and the written order forms and statements of work referenced on them - including
  any oral or written understanding as to extended payment terms, a right of return or
  cancellation, a price adjustment, or a contingency affecting your obligation to pay?

      [ ] No such agreement       [ ] Yes (please describe below)

    ______________________________________________________________________________________

Signature: ______________________________  Title: __________________________________

Printed name: ___________________________  Date: ___________________________________

Business email address: _________________  Telephone: ______________________________
--------------------------------------------------------------------------------------------
```

Five features are deliberate. The letter is on client letterhead and signed by the client, but the *return* is to the auditor,
stated three times, because AS 2310.15–.16 require direct receipt and AS 2310.22 makes an item a nonresponse if a reply sent to
the company is not re-sent to you. The invoice-level composition is listed, because a customer given four invoice numbers tells
you which one it disputes — every exception in §7.5 was identified at the invoice level. Amounts are in whole dollars, because
"2,410" invites a response confirming $2,410. The side-agreement paragraph is the AS 2401 response to the presumed revenue fraud
risk. And the request asks for the respondent's email and telephone, which is how the Castellan Freight reply was caught.

### 7.3.4 Controlling the process and the electronic platform

AS 2310.14–.15 require the auditor to select, send, and receive; the control log is the evidence that you did. Brightline sent 38
requests through an electronic confirmation intermediary and 12 by auditor-controlled email and courier. An intermediary triggers
Appendix B: understand its controls over interception and alteration, determine they operate effectively, and assess company
override. Brightline read the platform's calendar-2025 SOC 1 Type 2 report, tested five requests end to end through its audit
trail, and established that AtlasFlow personnel cannot amend a registered address; the two requests whose contact records an
AtlasFlow analyst had created were couriered to the order-form address.

**Exhibit 7-6. Confirmation control log — extract, 8 of 50 requests (balances in thousands; all sent 01/12/2026; "2nd/resp."
gives the second-request and response dates).**

| # | Customer | Balance | Form | Address source | Channel | 2nd/resp. | Disposition |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 01 | Meridian Health Systems | 2,410 | Stated | AP contact on SOW-2; domain matched | Platform | —/01/16 | Reliable; agreed |
| 02 | Voltaire Logistics S.A. | 1,880 | Stated | Renewal order form; domain verified | Platform | —/01/21 | Reliable; agreed (a) |
| 03 | Northgate Financial Group | 1,640 | Stated | Treasury contact on order form | Platform | 01/26, 02/02 | Reliable; $180 claim noted |
| 04 | Tessera Partners (for Cirrus Retail) | 1,510 | Stated | Reseller master agreement notice clause | Platform | —/01/19 | Reliable; agreed |
| 05 | Pemberton Manufacturing Co. | 1,290 | Stated | AP portal contact | Platform | —/01/23 | Reliable; exception X-2 |
| 07 | Sundown Media Holdings | 980 | Blank | Order form; CFO office | Courier | 01/26, none | Nonresponse |
| 09 | Calderon Foods | 790 | Blank | AP contact on SOW | Platform | —/01/20 | Reliable; exception X-1 |
| 12 | Castellan Freight | 480 | Stated | Record created 01/08/2026 by an AtlasFlow analyst (b) | Email | 01/26, 01/28 | Reliability **not established** (b) |

Tick marks: (a) EUR balance of €1,640 confirmed; recomputed at the December 31, 2025 rate of 1.1463 USD/EUR to $1,879.9,
agreeing to the recorded $1,880 within rounding. (b) Reply from a gmail.com address not matching the request; see X-6 in
Exhibit 7-8.

AS 2310.21 requires follow-up on a nonresponse, so a file showing one mailing and then alternative procedures has skipped a
step.

## 7.4 Nonresponses, Alternative Procedures, and Subsequent Cash Receipts

Of the 50 requests sent, covering $23,590: 31 agreed with the recorded balance ($15,880, 67.3% of the requested balance), 7
contained an exception ($4,610, 19.5%), and 12 did not respond even to a second request ($3,100, 13.1%) — 76.0% by count, 86.9%
by value. Two exceptions became nonresponses under AS 2310.19 and .22 (Castellan Freight, $480, unreliable response; Harwell
Municipal Systems, $415, "unable to confirm"), so alternative procedures covered 14 accounts totaling $3,995. AS 2310 Appendix A
counts an oral-only response as a nonresponse: "they said it's fine" is nothing.

The procedure carrying the most weight matches subsequent cash receipts to the *specific* invoices comprising the December 31
balance; a customer that owed $240 and paid $240 in January has substantiated nothing if the payment settled January invoices.
Brightline used a cut-off of February 13, 2026.

**Exhibit 7-7. Alternative procedures on the 14 nonresponses (in thousands).**

| Customer | Balance 12/31 | Cash by 02/13/2026 | Residue procedure and result |
| --- | --- | --- | --- |
| Castellan Freight | 480 | 480.0 | Matched to remittance |
| Harwell Municipal Systems | 415 | 415.0 | Matched to remittance |
| Sundown Media Holdings | 980 | 200.0 | Residue 780.0; forbearance letter 01/20/2026; individually evaluated (§7.9.5) |
| Fairmount Public Schools | 505 | 505.0 | Purchase order and remittance matched |
| Delacroix Cosmetics | 330 | 330.0 | Settled |
| Ironbark Mining Pty | 295 | 295.0 | Settled (AUD, retranslated) |
| Kellerman Legal | 240 | 240.0 | Settled |
| Ashgrove Retail | 240 | 232.5 | **M-2**, 7.5: short-paid overage; usage file included January runs |
| Cormorant Bioscience | 185 | 173.0 | **M-3**, 12.0: December invoice for a January hosting uplift |
| Vantage Kinetics | 155 | 150.5 | **M-4**, 4.5: T&M invoice for January 2–6 hours |
| Solstice Apparel | 120 | 120.0 | Settled |
| Pell & Rowe LLP | 22 | 20.1 | **M-5**, 1.9: as M-4 |
| Northwind Analytics | 18 | 18.0 | Settled |
| Quill & Vale Publishing | 10 | 10.0 | Settled |
| **Total** | **3,995** | **3,189.1** | Residue **805.9** |

Cash settled 79.8% of the nonresponse balance, and the test produced what no confirmation could: four short-payments totaling
$25.9 on accounts that never responded, each a cut-off misstatement. A short-payment is the customer telling you in cash which
part of the balance it does not accept, so never write "customer paid, agreed" where the amount received differs from the amount
recorded. For an unpaid residue, AS 2310 Appendix C points to the order form, provisioning record, and December usage log, with
collectibility left to the allowance; a residue unpaid *and* undocumented is projected as a misstatement.

## 7.5 Evaluating Exceptions and Projecting the Misstatement

A **confirmation exception** is neutral — any difference from the company's information — and AS 2310.20 requires you to
determine whether it indicates a misstatement, a control deficiency, or both.

**Exhibit 7-8. Exception evaluation schedule (in thousands).**

| Ref | Customer | Books / response / difference | Cause established | Misstatement |
| --- | --- | --- | --- | --- |
| X-1 | Calderon Foods | 790 / 730 / 60 | INV-0088997 dated 12/30/2025; acceptance certificate signed 01/09/2026, invoice refused as premature | **Yes**, 60.0 — no enforceable right at 12/31 |
| X-2 | Pemberton Manufacturing Co. | 1,290 / 980 / 310 | Check dated 12/29/2025, credited to account 1010 on 01/06/2026 | No — in transit; agreed to the bank credit |
| X-3 | BlueRidge Insurance | 870 / 725 / 145 | INV-0088410 dated 12/28/2025, received 01/05/2026; tenant provisioned 12/28/2025 | No — records lag; the right existed |
| X-4 | Larkspur Dental Group | 305 / 215 / 90 | Reported net of a $90 unapplied credit memo in account 2230 | No — a refund liability is not netted against AR |
| X-5 | Ridgeline Utilities | 460 / 520 / (60) | Credit memo CM-0002214 issued 12/30/2025, not yet received | No — records lag |
| X-6 | Castellan Freight | 480 / 480 / — | Unsigned reply from a gmail.com address not matching the request, no copy of it | Reliability not established (AS 2310.18); disregarded |
| X-7 | Harwell Municipal Systems | 415 / n/a | Customer's system cannot report by vendor | Nonresponse; alternative procedures performed |
| | **Total exceptions** | **4,610** | | **60.0** |

X-6 is the failure mode the current standard was written to address, and nothing about the response looked wrong — the amount
agreed exactly. The provenance was wrong: an address supplied by the audited company, a free email domain, no copy of the
request. The team disregarded the response, obtained full cash settlement of $480 on January 28, 2026, re-verified all 50
addresses, and reported the incident to the audit committee. Had the address proved to be controlled by an AtlasFlow employee,
the conclusion would have been a fraud-risk reassessment under AS 2401.

**Projection.** Five misstatements were identified — M-1 (Calderon Foods, $60.0) and M-2 through M-5 ($25.9, from subsequent
receipts) — sharing one cause: a receivable and revenue recorded in December for a performance obligation satisfied in January.
The misstatement is therefore systematic and projectable.

**Exhibit 7-9. Projection to the enterprise receivable population (in thousands).**

| Stratum | Population | Sample | Misstatement found | Basis | Projected misstatement |
| --- | --- | --- | --- | --- | --- |
| 1 (tested 100%) | 20,290 | 20,290 | 60.0 | None — known misstatement | 60.0 |
| 2 (sampled) | 12,610 | 3,060 | 24.0 | Ratio 12,610 ÷ 3,060 = 4.1209 | 98.9 |
| 3 (sampled) | 3,290 | 240 | 1.9 | Ratio 3,290 ÷ 240 = 13.7083 | 26.0 |
| 4 (subsequent-receipts scan) | 710 | 710 | — | None | — |
| 5 (nil balances) | — | — | — | n/a | — |
| **Total** | **36,900** | **24,300** | **85.9** | | **184.9** |

The $184.9 is recorded as **U-1, $(185)**, receivables overstated. The 100%-tested stratum is carried at its known amount.
Ratio projection fits because the
misstatements are proportional to size, whereas fixed-amount errors would call for difference projection (Chapter 15, §15.9). A
full-population query of all 4,102 December invoices was declined because establishing January performance requires reading the
SOW or timesheet for each line; the trigger for reversing that decision was a projection above roughly $470. The same cause in
another subpopulation would raise U-1 (§7.10 found none); payment of the four deducted amounts would lower it (none had been paid
by February 13, 2026).

## 7.6 Unbilled Receivables and Contract Assets

**Exhibit 7-10. Receivable-side treatment of account 1220 at December 31, 2025 (in thousands).**

| Component | Amount | Classification under ASC 606-10-45 | Procedure |
| --- | --- | --- | --- |
| Fixed-fee services recognized on the input measure ahead of milestone billing | 1,780 | Contract asset — conditional on a milestone | Recompute the input measure for 12 engagements; test milestone achievability |
| Ramped contracts where cumulative revenue exceeds cumulative invoicing | 1,240 | Contract asset — conditional on continued performance | Recompute from the contract; confirm the anniversary invoice issued or the contract live |
| December 2025 time-and-materials work invoiced in January 2026 | 380 | Receivable — only invoicing remains | Agree to the January invoice and timesheet; test collection |
| **Total, account 1220** | **3,400** | | |

Chapter 6, §6.8 establishes the composition and the contract-level netting rule. Contract assets are in the scope of ASC 326-20
and require an allowance — routinely missed because the balance sits under a different caption, and management measured nothing
against the $3,400. Brightline's expected credit losses on the $3,020 of contract assets, at the current-bucket rate of 0.4% plus
an increment for the risk that a milestone is never certified, range from $12 to $28, point estimate $18, below the $72
threshold. No misstatement was accumulated, but the scope omission was reported: a model that omits a category of in-scope assets
keeps omitting it as the balance grows, and this one grew 61.9%. The $380 was not in the ATB and so not confirmed; all of it was
invoiced by January 9, 2026 and $341 collected by February 13.

## 7.7 Disputes, Concessions, and the Meridian Invoice

A disputed receivable is an accounting question before it is a credit question. If the customer **cannot** pay, the
shortfall is a credit loss charged to the allowance and to general and administrative expense. If the customer **can** pay
but is expected to be granted a reduction, the shortfall is a **price concession** — variable consideration under
ASC 606-10-32 — which reduces revenue, not the allowance, and must be estimated for all contracts with similar
characteristics rather than only for the customer that complained.

**Meridian Health Systems.** On February 9, 2026, before the report date, Meridian disputed the $1,240 professional services
invoice within its $2,410 balance — milestone 2 of SOW-2, a $2,110 data-migration statement of work signed October 3, 2025.
Meridian's average days-to-pay was 34 days and its ability to pay is not in question. Four procedures, in order. First,
establish whether the condition existed at December 31: the notice is a subsequent event, but whether the cut-over was accepted
is a year-end fact, so obtain the acceptance certificate (signed by Meridian's program director on December 3, 2025), the
runbook, and the Jira record of 41 post-cut-over defects logged in December. Second, read the correspondence — Meridian asserts
four data objects were outside the certificate; AtlasFlow says an unsigned change order added them. Third, quantify the range,
from full collection to a $620 concession (50%), anchored on 26 disputed services invoices settling at an average concession of
8.0%, implying $99. Fourth, obtain any resolution: the parties settled February 17 and Meridian paid in full on February 18.

No adjustment was required. Absent the settlement, the $99 estimated concession would have been a *revenue* misstatement with a
refund liability in account 2230, not an addition to the allowance; a signed change order would have supported $0. Northgate's
$180 SLA claim runs the same logic through a different mechanism: an earned service-level credit reduces the transaction price
and was recorded within corrected misstatement C-2 ($290 of SLA credits accrued). The receivable consequence is that $390 of
the $38,600 will be settled by credit memo, so reserving a credit loss against it double-counts account 2230 (§7.9.2).

## 7.8 Credit Memos and Their Authorization

**Exhibit 7-11. FY2025 credit memo population (in thousands, except counts).**

| Category | Count | Value |
| --- | --- | --- |
| Service-level agreement credits | 61 | 340 |
| Billing-error corrections and rebills | 412 | 780 |
| Cancellations and downgrades within the contractual window | 128 | 410 |
| Commercial concessions | 37 | 290 |
| Self-serve refunds and card chargebacks | 1,842 | 80 |
| **Total credit memos issued in FY2025** | **2,480** | **1,900** |

Every category lands in contra revenue through account 4900, to which the total agrees; the cancellation memos also relieve
deferred revenue, and the billing-error memos are offset by the corrected invoice.

Four tests. **Authorization:** Zuora requires a Billing Analyst below $10, the Revenue Manager for $10 to $50, and the
Controller above $50. Of 45 memos tested (sizing at Chapter 15, §15.5), three deviated: two of $62 and $118 approved one level
too low, one of $24 with no approval record. The 6.7% deviation rate exceeds the 5.0% tolerable rate and the achieved upper
limit is 14.2%, so the control cannot be relied on and testing was extended to all 19 memos above $50 ($640). These are
deviations, not misstatements. **Post-year-end memos against FY2025 invoices:** 214 memos, $460 — $290 accrued through C-2, $129
January billing errors misapplied to December invoices, and $41 of FY2025 performance not accrued, below the $72 threshold but
reported because the query runs against a larger base next year. **Memos reversing late-quarter revenue:** $210 credited across
9 of the contracts in the $25,174 of ACV signed December 24–31, six underlying U-3; 0.8% against 1.2% for the year is not a
finding, though a materially higher rate would be. **The unissued memo:** collections notes on the 31 balances over 90 days past
due showed four accounts totaling $310 that had asked for a credit.

## 7.9 The CECL Model for a SaaS Receivable Portfolio

### 7.9.1 What the model must do

Four requirements drive everything: the allowance is the **lifetime** expected credit loss, not a probable-and-estimable
amount, so a current, never-late receivable still carries one; measurement is **collective** where risk characteristics are
similar and individual where they are not; historical loss information is **adjusted** for current conditions and reasonable
and supportable forecasts; and the estimate **reverts** to historical loss information beyond the forecastable horizon.

### 7.9.2 Pooling, and getting the population right first

Aging is one risk characteristic, not the only one. A defensible structure separates the enterprise direct, channel, and
self-serve portfolios, whose loss drivers differ — customer insolvency, reseller failure, card declines — and ages within each.
Management pools on aging alone; challenge that, because the question is whether blended rates represent each subportfolio,
which §7.10 answers for self-serve.

**Exhibit 7-12. From the aged trial balance to the collectively evaluated pool (in thousands).** Each removal needs a reason:
the $390 will be extinguished by a credit memo, so reserving against it double-counts account 2230; the $1,240 is a concession
question, and leaving it in the pool at 0.4% ($5.0) understates the exposure and mislabels it; and the $980 no longer shares
risk characteristics with any pool.

| Line | Current | 1–30 | 31–60 | 61–90 | 91–180 | Over 180 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Gross accounts receivable per §3.3 | 22,550 | 8,190 | 3,740 | 1,970 | 1,440 | 710 | 38,600 |
| Less: balances to be settled by credit memo, accrued in account 2230 | (50) | (180) | (120) | (40) | — | — | (390) |
| Less: Meridian SOW-2 invoice under dispute, evaluated under ASC 606 | (1,240) | — | — | — | — | — | (1,240) |
| Less: Sundown Media Holdings, individually evaluated | — | — | — | — | (980) | — | (980) |
| **Collectively evaluated pool** | **21,260** | **8,010** | **3,620** | **1,930** | **460** | **710** | **35,990** |

### 7.9.3 Method 1 — the loss-rate (aging matrix) method

**Exhibit 7-13. Loss-rate method applied to the collectively evaluated pool (in thousands, to the nearest $0.1).**

| Bucket | Pool balance | Historical loss rate | Expected credit loss |
| --- | --- | --- | --- |
| Current (not yet due) | 21,260 | 0.4% | 85.0 |
| 1–30 days past due | 8,010 | 1.6% | 128.2 |
| 31–60 days past due | 3,620 | 6.0% | 217.2 |
| 61–90 days past due | 1,930 | 18.0% | 347.4 |
| 91–180 days past due | 460 | 42.0% | 193.2 |
| Over 180 days past due | 710 | 85.0% | 603.5 |
| **Total** | **35,990** | **4.4%** | **1,574.5** |

Audit the rates, not the multiplication. Obtain the derivation — a look-back over FY2021–FY2024 originations measuring ultimate
charge-offs as a percentage of each bucket at each month end — re-perform two of the six, and confirm the denominator includes
balances later written off rather than only still-open ones. Because a four-year window spanning faster growth dilutes later
charge-offs, recompute on recent originations: the over-180 rate on FY2023–FY2024 originations is 88.1% against the 85.0% used,
a $22 effect within tolerance.

### 7.9.4 Method 2 — the roll-rate method, and Method 3 — the vintage method

**Exhibit 7-14. Roll-rate method, monthly roll rates averaged over the 24 months ended December 31, 2025 (in thousands,
to the nearest $0.1).**

| Bucket | Monthly roll rate to the next bucket | Cumulative probability of charge-off | Pool balance | Expected credit loss |
| --- | --- | --- | --- | --- |
| Current → 1–30 | 14.0% | 0.230% | 21,260 | 48.9 |
| 1–30 → 31–60 | 22.0% | 1.644% | 8,010 | 131.6 |
| 31–60 → 61–90 | 34.0% | 7.471% | 3,620 | 270.4 |
| 61–90 → 91–180 | 47.0% | 21.973% | 1,930 | 424.1 |
| 91–180 → over 180 | 55.0% | 46.750% | 460 | 215.1 |
| Over 180 → charge-off | 85.0% | 85.000% | 710 | 603.5 |
| **Total** | | **4.7%** | **35,990** | **1,693.6** |

The cumulative column is the product of the downstream roll rates; for the 31–60 bucket,
34.0% × 47.0% × 55.0% × 85.0% = 7.471%. Re-perform two of those products by hand, because a transposed rate in a spreadsheet
cascade is invisible in the output. The roll-rate answer exceeds the loss-rate answer by $119.1 (7.6%) because roll rates over
the most recent 24 months embed FY2025's slower collections while the loss rates come from FY2021–FY2024 — the primary evidence
for the current-conditions adjustment.

**Exhibit 7-15. Vintage method by invoice quarter (in thousands, to the nearest $0.1).**

| Invoice vintage | Open balance at 12/31/2025 | Remaining cumulative loss rate, FY2021–FY2023 curve | Expected credit loss |
| --- | --- | --- | --- |
| Q4 2025 | 29,900 | 1.36% | 406.6 |
| Q3 2025 | 3,600 | 6.00% | 216.0 |
| Q2 2025 | 1,300 | 17.00% | 221.0 |
| Q1 2025 | 700 | 31.00% | 217.0 |
| FY2024 and earlier | 490 | 84.50% | 414.1 |
| **Total** | **35,990** | **4.1%** | **1,474.7** |

The curve comes from fully seasoned vintages, in which 98.6% of ultimate charge-offs occurred within 18 months of the invoice
date. The vintage method returns the lowest answer because 83.1% of the open balance was invoiced in the most recent quarter,
and it earns its place because it does not depend on the aging report at all. Do not average the three results; use the spread
of $218.9 as the pooled component of the range — vintage low, loss-rate as the point estimate (longest observed history,
applied to the corrected aging), roll-rate high.

### 7.9.5 Individually evaluated accounts

**Sundown Media Holdings, $980, 94 days past due.** In collections; tenant suspended January 8, 2026; forbearance letter executed
January 20 and $200 paid January 22, with $780 payable in six instalments from March 2026; the parent reported a covenant breach
in December 2025 lender reporting and retained restructuring advisers in January. Against a pooled 91–180 rate of $411.6,
Brightline's range is 25% ($245) if the instalment plan performs to 50% ($490) on a formal restructuring, point estimate 40%
($392). Two instalments paid before the report date would support the low end; a filing or a missed March instalment would
support 50% or more; neither occurred by February 20, 2026.

### 7.9.6 Current conditions, the forecast, reversion, and overlays

These are four separate adjustments, and collapsing them into one "qualitative" line is a documentation defect.

**Current conditions — what has happened but is not in the historical rates.** The FY2024 aging, an extension for this chapter,
was $18,900 current, $6,600 1–30, $2,600 31–60, $1,250 61–90, $850 91–180, and $300 over 180, so balances 31 days or more past
due rose from 16.4% of the portfolio to 20.4%. Applied to the pool that is $1,440 of receivables that would have sat in an
earlier bucket at FY2024 velocity. Multiply by an incremental loss rate: 1.4% ($20) low, 4.7% ($68) point — the rate implied by
the roll-rate/loss-rate gap — and 5.55% ($80) high.

**Reasonable and supportable forecast — what has not happened yet.** The driver is a commercial credit bureau's
small-and-mid-size-business insolvency rate, forecast to rise from 2.9% to 3.4% over twelve months. A forecast can only change
outcomes not already largely determined, so it applies to the current and 1–30 buckets ($21,260 + $8,010 = $29,270) rather than
the whole pool, at incremental rates of 0.092% ($27), 0.239% ($70), and 0.314% ($92).

**Reversion — computed, not assumed.** Weighting expected months to resolution by bucket (0.8, 1.5, 2.5, 3.5, 5.5, and 9.0) gives
a remaining life of 1.5 months, so the entire expected life falls inside a twelve-month supportable forecast period and no
reversion period arises. Say so in the workpaper rather than omitting it; multi-year instalment receivables would change the
answer.

**Quantified overlays.**

| Overlay | Basis | Low | Point | High |
| --- | --- | --- | --- | --- |
| Kestrel-acquired accounts, onboarded without credit screening before the October 2025 migration into Zuora | $840 × 1.2% / 3.0% / 4.0% | 10 | 25 | 34 |
| Self-serve card-decline exposure not captured by the blended pool rates (§7.10) | Subsequent-settlement analysis | 3 | 10 | 20 |
| **Total qualitative overlay** | | **13** | **35** | **54** |

An overlay that cannot be expressed as an identified balance times a rate is not an overlay, it is a plug. Ask for the balance
and the rate; if either is missing, the estimate has no auditable structure and the deficiency evaluation should say so.

## 7.10 Auditing 11,400 Self-Serve Balances

The self-serve portfolio is $1,700 across 11,400 accounts — 1.8 times performance materiality and impossible to confirm
economically. Replace item-level testing with a full-population test of the event that matters: whether the card settled.

**Exhibit 7-16. Self-serve subsequent-settlement test at February 13, 2026 (in thousands, except counts).**

| Dunning stage at 12/31/2025 | Accounts | Balance | Balance settled | Settlement rate |
| --- | --- | --- | --- | --- |
| No decline; charge scheduled | 9,980 | 1,150 | 1,142 | 99.3% |
| Decline 1 — automatic retry pending | 890 | 290 | 268 | 92.4% |
| Declines 2–3 — dunning email sent | 380 | 140 | 106 | 75.7% |
| Declines 4 or more — suspension pending | 130 | 70 | 33 | 47.1% |
| Suspended, balance retained | 20 | 50 | 5 | 10.0% |
| **Total** | **11,400** | **1,700** | **1,554** | **91.4%** |

That table does three jobs: it substantiates existence and gross accuracy for 91.4% of the balance by reference to cash; it
stratifies by the characteristic that actually predicts loss, since a self-serve invoice goes past due only because a card failed;
and it exposes the 20 suspended accounts whose 10.0% settlement rate shows the blended pool rates do not represent every sliver.
Historically 45.0% of balances unsettled 44 days after year end are ultimately charged off (40% to 52% over FY2022–FY2024), so the
$146 residue implies $65.7 against the $55.5 embedded in the blended matrix — the $10.2 shortfall that is the self-serve overlay
in §7.9.6, $2.9 and $20.4 at the ends. Recompute the $1,700 from the transaction-level Stripe file as well, because the daily
summary journal is in-house Lambda code with two unapproved FY2025 modifications (W-7).

## 7.11 Write-Offs, Recoveries, and the Roll-Forward

**Exhibit 7-17. Allowance for credit losses roll-forward, FY2025 (in thousands).**

| Component | Amount | Source and procedure |
| --- | --- | --- |
| Balance at January 1, 2025 | 1,350 | Prior-year audited balance |
| Provision charged to general and administrative expense | 1,780 | Agreed to account 6300 detail and the statement of cash flows |
| Write-offs charged against the allowance | (1,230) | Write-off register, 192 accounts |
| Recoveries of amounts previously written off | — | See below |
| Foreign currency translation | — | UK and Australia; below the rounding threshold |
| **Balance at December 31, 2025** | **1,900** | Agreed to account 1210 and the balance sheet caption |

The roll-forward is the control total for the account, tying the $1,780 in the statement of cash flows, the $1,900 in
account 1210, and the Rule 12-09 valuation-account disclosure. Recompute it first; if it does not foot, the cause is nearly
always a direct write-off charged to expense rather than to the allowance. The $1,230 comprises 192 accounts — $1,010
enterprise and $220 self-serve — rising each quarter from $180 in Q1 to $450 in Q4. Four procedures follow.

**Authorization.** Policy requires CFO approval above $50 and Controller approval below. All 17 enterprise write-offs
were tested; two, of $18 and $22, carried verbal approval only — control deviations reported with those in §7.8.

**Substance.** The test that earns its keep asks whether the customer *could* have paid. Three of the 17, totaling $65, were
disputed invoices for customers still active and paying at December 31, 2025 — price concessions, so revenue is overstated and
general and administrative expense understated by $65. The net income effect is nil and $65 is below the $72 threshold, so nothing
was accumulated; it was reported because writing off a concession as bad debt keeps a revenue-quality problem out of the revenue
line.

**Recoveries.** Recoveries credited to the allowance were nil, and $1,230 of write-offs with no recoveries deserves a question
rather than a tick; the two queries in RQ 7-15 produced no item, so the zero is real. One subsequent item bears on the estimate:
$95 received January 27, 2026 from Ridgemont Media, written off in September 2025 — evidence that write-off timing is aggressive,
and an argument toward the low end of the range.

**Q4 concentration.** Q4 write-offs of $450 are 36.6% of the annual total, a finding if those balances were current three months
earlier — a wrong aging, or a disputed balance removed quietly. All 12 were traced to their September 30, 2025 aging status, and
ten were already over 90 days past due.

## 7.12 Presentation, Netting, Concentrations, and Disclosure

**Netting.** Only contract assets and contract liabilities net, contract by contract (ASC 606-10-45; Chapter 6, §6.8 works the
mechanics). The corollary staff get backwards: a receivable never nets against a contract liability. Meridian's contract carries
both a $2,410 receivable and a deferred revenue balance, both presented gross — test by agreeing five such contracts to their
captions without offset. The 31 credit balances totaling $310 are liabilities, not offsets to other customers' debits.

**Exhibit 7-18. Customer concentration at December 31, 2025 (in thousands).**

| Customer | Balance | % of gross AR |
| --- | --- | --- |
| Meridian Health Systems | 2,410 | 6.2% |
| Voltaire Logistics S.A. | 1,880 | 4.9% |
| Northgate Financial Group | 1,640 | 4.2% |
| Cirrus Retail Group (via Tessera Partners) | 1,510 | 3.9% |
| Pemberton Manufacturing Co. | 1,290 | 3.3% |
| Halloran Energy | 1,120 | 2.9% |
| Sundown Media Holdings | 980 | 2.5% |
| BlueRidge Insurance | 870 | 2.3% |
| Calderon Foods | 790 | 2.0% |
| Aeropath Group | 740 | 1.9% |
| **Top ten** | **13,230** | **34.3%** |
| All other enterprise accounts | 23,670 | 61.3% |
| Self-serve accounts | 1,700 | 4.4% |
| **Gross accounts receivable** | **38,600** | **100.0%** |

No customer reaches 10% of receivables or revenue, so no major-customer disclosure arises, but ASC 275-10-50 still requires
disclosure of a concentration of credit risk where one exists. Recompute both ways: 6.2% of gross receivables, and Meridian's
revenue at 1.3% of $148,200. The concentration a customer test misses is the channel, where 9% of ACV and roughly $2,250 of
receivables depend on two intermediaries' solvency rather than the end customers'. Also test the past-due disclosure against the
*corrected* aging and management's ASC 326-20-50 conclusion that its receivables fall outside the credit-quality-indicator
requirement.

## 7.13 Receivable Analytics and DSO

**Exhibit 7-19. Receivable analytics, FY2025 versus FY2024 (in thousands except ratios and days).**

| Metric | FY2025 | FY2024 | Interpretation |
| --- | --- | --- | --- |
| Gross accounts receivable | 38,600 | 30,500 | Up 26.6%, outrunning revenue growth of 24.6% |
| Q4 billings (extension for this chapter) | 52,240 | 46,000 | Up 13.6%; the denominator of DSO |
| DSO (gross AR ÷ Q4 billings × 92) | 68.0 days | 61.0 days | Up 7.0 days; agrees to the disclosed metric |
| Allowance as a percentage of gross AR | 4.92% | 4.43% | Rose, but by less than delinquency did |
| Balances 31 days or more past due | 7,860 | 5,000 | Up 4.0 points of share; the strongest single indicator |
| Allowance ÷ balances 31+ days past due | 24.2% | 27.0% | Coverage of the delinquent tail *fell* 2.8 points |
| Dollar-based gross retention | 91% | 93% | Consistent with the delinquency trend |

These are risk-assessment and disclosure-corroboration procedures, not substantive analytical procedures under AS 2305: no ratio
on a $38,600 balance carries an expectation precise enough to detect $940. The arithmetic that makes DSO an audit fact rather than
a slogan: at FY2024's velocity of 61 days, Q4 2025 billings would have supported 61 ÷ 92 × $52,240 = $34,637 of receivables, so
roughly $3,963 exists that would not have at prior-year velocity — 2.7 times overall materiality. The sixth row is the finding,
and reconciling delinquency and coverage moving in opposite directions is the case study. Chapter 18, §18.6 develops predictive
collection-probability modelling here.

## Step-by-Step Walkthrough: Designing, Sending, Controlling, and Evaluating the FY2025 Accounts Receivable Confirmation

Performed by A. Trent and J. Park, supervised by O. Haddad, January 6 to February 16, 2026. Workpaper WP 7200-03.
Amounts in thousands.

**Step 1. Obtain the aged trial balance and agree it to the ledger.** Request the Zuora and Stripe reports at December 31, 2025
carrying account ID, legal name, invoice number and date, payment terms, due date, open amount, currency, entity, and
collections status. Received January 6: 3,140 enterprise accounts, $36,900; 11,400 self-serve, $1,700, tying to accounts 1200
and 1205. Absent payment terms you cannot re-age — stop and ask.

**Step 2. Re-age the population independently.** Run the §7.2 query: $412 sat in the current bucket that belonged in three
past-due buckets. Obtain the corrected report (January 9), re-run the comparison to nil, and quantify the $88.1 allowance
effect. If management declines to correct it, use your version and record the disagreement.

**Step 3. Test the aging cut-off both ways.** Vouch ten of the 41 invoices ($612) posted after December 31 with a December
invoice date to the order form and provisioning record, and all 27 cash applications ($304) posted after December 31 with a
December value date to the bank statement. An item outside the January 2–5 close window is not timing: obtain the Zuora audit
trail and escalate under AS 2401.

**Step 4. Remove what cannot or should not be confirmed, and say why.** Exclude the 11,400 self-serve accounts (the AS 2310.13
analysis in §7.3.1), the 2,474 nil balances, and the 31 credit balances, leaving $36,900 across 666 debit-balance accounts.

**Step 5. Stratify, set the extent, and select the items yourself.** Build Exhibit 7-4: stratum 1 at $470 tested in full,
samples of 18 and 10 in strata 2 and 3, stratum 4 excluded, 63.9% coverage documented. AS 2310.15 requires you to select; use
systematic selection with a random start, intervals of $700 and $329, seed in the workpaper.

**Step 6. Determine the confirming party and verify each address independently.** For all 50, take the accounts-payable contact
from the executed order form or SOW rather than the Zuora contact record, and compare the email domain to the customer's public
domain. Two mismatches traced to records an AtlasFlow analyst created in January 2026. For the channel the party is Tessera
Partners and the global systems integrator, not Cirrus or Aeropath.

**Step 7. Evaluate the electronic intermediary before using it.** Perform the three Appendix B procedures of §7.3.4 and courier
the two step 6 items instead. If the controls cannot be established, AS 2310.B2 bars the platform entirely.

**Step 8. Send under your own control and log every request.** Sent January 12. Maintain Exhibit 7-6 and monitor bounces daily
for a week; an undelivered request is a nonresponse immediately, not after the second request.

**Step 9. Follow up, then test the reliability of every response.** Second requests to the 16 outstanding accounts on
January 26, with telephone escalation to the five largest, always asking for a written reply to Brightline; five further
responses arrived by February 3. Then apply the AS 2310.18 indicators. Request 12 failed all three, so it was disregarded under
AS 2310.19, address verification was extended to all 50, and the audit committee was informed February 13.

**Step 10. Investigate every exception to root cause and classify it.** Build Exhibit 7-8: for each difference obtain the
document that explains it — the bank credit, the provisioning record, the account 2230 detail, the credit memo — and only then
decide between a records difference and a misstatement. One of seven, $60.0, was a misstatement.

**Step 11. Perform alternative procedures on all nonresponses, matching cash invoice by invoice.** Build Exhibit 7-7 for the 14
accounts, $3,995: $3,189.1 settled by February 13 and four short-payments totaling $25.9 were misstatements. For the unpaid
$805.9, examine the order form, provisioning record, and usage log. Separately scan stratum 4 ($710, 402 accounts) for
aggregate settlement: $648 by February 13.

**Step 12. Reconcile the sample, project, and conclude.** Confirm that the 50 selected accounts plus the untested residue equal
666 accounts and $36,900, and that every selected item ends in one of four dispositions — agreed, exception resolved,
misstatement quantified, or alternative procedures completed; none may end in "pending." Build Exhibit 7-9: $60.0 known plus
ratio projections of $98.9 and $26.0 give $184.9, 19.7% of performance materiality, so no extension is required.

**Step 13. Carry the results forward and obtain review.** Conclude that existence, rights, and gross accuracy are supported
subject to **U-1 of $(185)**. Carry U-1 to the summary of audit differences (Chapter 19, §19.3), the systematic cut-off cause to
the revenue conclusion (Chapter 4, §4.8) and the ICFR evaluation (Chapter 14), and the four short-paid accounts and the Sundown
forbearance into the allowance file, with reviewer sign-off before the February 20 report date.

## Extended Case Study: The Allowance for Credit Losses — Building a Range and Evaluating Management's $1,900

### Background

The allowance grew 40.7%, from $1,350 to $1,900, on a portfolio that grew 26.6%, so coverage rose from 4.43% to 4.92% of gross
receivables — which looks conservative until it is set against the 4.0-point deterioration in delinquency. FY2025 is also the
first year the estimate is subject to an ICFR opinion and the first year of a new CFO.

### The Facts

Management's memo, authored by A. Bello and approved by E. Vasquez and T. Okafor on January 21, 2026, builds the allowance in
four steps: apply the six historical loss rates in §3.3 to the corrected aged trial balance; replace the pooled rate on Sundown
Media Holdings with a specific 20% reserve; add a $100 qualitative overlay for "macroeconomic uncertainty and integration
risk"; and round to the nearest $50. It contains no forecast component, no current-conditions adjustment, no analysis of which
balances will be settled by credit memo, and no measurement of expected losses on the $3,020 of contract assets. Two facts
arrived after it was signed: Meridian disputed a $1,240 invoice on February 9 and settled in full on February 18, and Sundown
executed a forbearance letter on January 20 and paid $200 on January 22.

### What the Engagement Team Did

AS 2501 permits testing management's process, developing an independent expectation, or examining subsequent events. Because
the subjectivity sits in assumptions rather than data, Brightline did all three: replicated management's computation;
developed an independent expectation using three methods and four adjustments (§7.9); and used subsequent events — cash
receipts to February 13, the forbearance letter, and the Meridian settlement — to corroborate the individually evaluated
items. Specialist involvement was limited to a national-office consultation on whether the Meridian dispute is a concession
or a credit loss.

### Analysis

**Exhibit 7-20. Brightline's independent expectation and range for the allowance at December 31, 2025 (in thousands).**

| Ref | Component | Basis | Low | Point | High |
| --- | --- | --- | --- | --- | --- |
| A | Collectively evaluated pool of $35,990 | Vintage (low), loss-rate (point), roll-rate (high) — Exhibits 7-13 to 7-15 | 1,475 | 1,575 | 1,694 |
| B | Current-conditions adjustment | $1,440 of excess delinquency × 1.4% / 4.7% / 5.55% | 20 | 68 | 80 |
| C | Reasonable-and-supportable forecast overlay | $29,270 (current and 1–30 buckets) × 0.092% / 0.239% / 0.314% | 27 | 70 | 92 |
| D | Quantified qualitative overlays | Kestrel $840 × 1.2% / 3.0% / 4.0%; self-serve residue analysis | 13 | 35 | 54 |
| E | Sundown Media Holdings, individually evaluated | $980 × 25% / 40% / 50% | 245 | 392 | 490 |
| | **Total allowance** | | **1,780** | **2,140** | **2,410** |
| | Management's recorded allowance | | 1,900 | 1,900 | 1,900 |
| | **Difference from Brightline's estimate** | | **(120)** | **240** | **510** |

Management's $1,900 lies inside the range, 19.0% of the way up from the bottom: defensible on its own, and not where an
unbiased estimator would land.

**Exhibit 7-21. Reconciliation of management's $1,900 to Brightline's point estimate (in thousands, to the nearest $0.01).**

| Line | Amount | Running total |
| --- | --- | --- |
| Management's recorded allowance | 1,900.00 | 1,900.00 |
| Reverse management's rounding to the nearest $50 | (7.06) | 1,892.94 |
| Reverse management's $100 undifferentiated qualitative overlay | (100.00) | 1,792.94 |
| Reverse the specific Sundown reserve, restoring the pooled 42.0% rate | 215.60 | 2,008.54 |
| **Pooled loss-rate matrix on the unadjusted aged trial balance** | | **2,008.54** |
| Remove the Meridian disputed invoice from the pool ($1,240 × 0.4%) | (4.96) | 2,003.58 |
| Remove balances to be settled by credit memo ($390 across four buckets) | (17.48) | 1,986.10 |
| Remove Sundown for individual evaluation ($980 × 42.0%) | (411.60) | 1,574.50 |
| **Pooled matrix on the collectively evaluated pool (Exhibit 7-13)** | | **1,574.50** |
| Add current-conditions adjustment (B) | 68.00 | 1,642.50 |
| Add reasonable-and-supportable forecast overlay (C) | 70.00 | 1,712.50 |
| Add quantified qualitative overlays (D) | 35.00 | 1,747.50 |
| Add Sundown individually evaluated at 40.0% (E) | 392.00 | 2,139.50 |
| **Brightline point estimate** | | **2,139.50** |
| Management's recorded allowance | (1,900.00) | |
| **Uncorrected misstatement U-2** | **239.50** | |

The $1,900 is not one aggressive assumption; it is two conservative omissions ($138 of missing current-conditions and forecast
adjustments) offset by one aggressive judgment (Sundown at 20% rather than 40%, worth $196) and one undifferentiated overlay
($100) that is $65 larger than the exposures it purports to cover. Reaching a number inside the range through offsetting errors is
not a supported estimate, and AS 2501 asks about each significant assumption.

| Assumption | Management | Brightline | Evidence that decided it |
| --- | --- | --- | --- |
| Sundown recovery | 80% (20% reserve) | 60% (40% reserve) | Parent's December covenant breach; restructuring advisers retained January 2026; service suspended January 8; only $200 of $980 received |
| Forecast component | None | $70 | ASC 326-20 requires consideration of reasonable and supportable forecasts, and the bureau forecast of SMB insolvency rising from 2.9% to 3.4% was used in AtlasFlow's own FY2026 planning deck |
| Overlay for portfolio change | $100 undifferentiated | $35 quantified | $840 of Kestrel-acquired balances identified; $146 self-serve residue measured against a 45.0% ultimate charge-off rate |

**Indicators of bias.** Three of management's four judgment calls move the estimate the same way — the optimistic Sundown
assumption, the omitted forecast component, and rounding up from $1,892.94 to $1,900. With the FY2025 pattern in Chapter 19,
where four of the six uncorrected misstatements reduce the loss, that is an indicator to be evaluated in aggregate and
communicated, not resolved silently at the account level.

### Resolution and Conclusion

Brightline proposed an adjustment of $240 to raise the allowance to $2,140. Management declined on the ground that its amount is
within the auditor's own range. Brightline accepted that the recorded amount is within the range of reasonable amounts, and
therefore that the statements are not materially misstated by this item alone, and recorded the difference from its point estimate
as uncorrected misstatement **U-2, $(240)**, so that it participates in the aggregate evaluation. U-2 with U-1 and the other four
items produces a net effect on the FY2025 pre-tax loss of $(460), 31.7% of overall materiality. Two deficiencies were reported in
writing on February 13, 2026: the model omits a forecast component and does not distinguish current-conditions adjustments from
qualitative overlays, and it omits in-scope contract assets. Neither is a material weakness, because the maximum plausible
misstatement from each ($138 and $28) is far below overall materiality.

### Workpaper Extract

```text
================================================================================
BRIGHTLINE LLP                                              WP REF:  7300-11
AtlasFlow, Inc.                                             PERIOD:  FY2025
Audit of the financial statements and of ICFR               YEAR END: 12/31/2025
--------------------------------------------------------------------------------
SUBJECT:  Allowance for credit losses (account 1210) - independent expectation,
          range of reasonable amounts, and evaluation of management's recorded
          estimate of 1,900

PREPARED BY:  J. Park (JWP)            DATE PREPARED:  02/06/2026
              A. Trent (AMT)                           02/09/2026
REVIEWED BY:  O. Haddad (OMH)          DATE REVIEWED:  02/12/2026
              G. Lindqvist (GRL)                       02/14/2026
PARTNER:      D. Whitcombe (DGW)                       02/17/2026
EQR:          L. Herrera (LXH)                         02/18/2026
--------------------------------------------------------------------------------
PURPOSE
To evaluate whether the allowance of 1,900 at 12/31/2025 is reasonable under
ASC 326-20 by developing an independent expectation and a range of reasonable
amounts under AS 2501, and to conclude on the valuation assertion.

SOURCE OF INFORMATION
(1) Management's CECL memo dated 01/21/2026 and workbook ACL_FY25_v6.xlsx.  (a)
(2) Corrected aged trial balance at 12/31/2025, total 38,600; write-off
    register FY2021-FY2025; 48 monthly aging snapshots; cash application
    detail 01/01/2026 - 02/13/2026; account 2230 detail at 12/31/2025.     (b)
(3) Sundown forbearance letter 01/20/2026, parent lender reporting for
    December 2025, bank credit of 200 dated 01/22/2026; Meridian settlement
    02/17/2026 and bank credit of 1,240 dated 02/18/2026; credit bureau SMB
    insolvency forecast published 12/2025.

PROCEDURES PERFORMED
1. Replicated management's computation; recomputed the pooled matrix as
   2,008.54 and reconciled it to the recorded 1,900.00 (Exhibit 7-21).     (c)
2. Re-performed 2 of the 6 historical loss rates from the 48-month history;
   recomputed the over-180 rate on FY2023-FY2024 originations only
   (88.1% vs 85.0% used; effect 22).
3. Adjusted the population to the collectively evaluated pool of 35,990.   (c)
4. Computed expected credit losses by three independent methods:
       Loss-rate (aging matrix)                                  1,574.50
       Roll-rate (24-month migration, cascaded)                  1,693.60
       Vintage (invoice quarter, FY2021-FY2023 curve)            1,474.70
5. Current conditions: 1,440 of excess delinquency x 4.7% = 68.00.         (c)
6. Forecast overlay on the current and 1-30 buckets: 29,270 x 0.239% =
   70.00. Computed remaining life of 1.5 months; no reversion arises.      (c)
7. Quantified overlays: Kestrel 840 x 3.0% = 25.20; self-serve residue
   146 x 45.0% less 55.5 already embedded = 10.20.
8. Evaluated Sundown individually: range 25%-50%, point 40% (392.00).      (c)
9. Evaluated the Meridian dispute as variable consideration under ASC 606
   rather than as a credit loss; obtained the settlement and cash receipt.
10. Measured expected credit losses on the 3,020 of contract assets: range
    12 to 28, point 18. Below CTT of 72; model scope omission reported.    (c)
11. Back-tested the FY2024 allowance of 1,350 against write-offs of 1,230;
    evaluated bias indicators under AS 2501 and AS 2810.                   (c)

RESULTS
- Range of reasonable amounts 1,780 to 2,410; point estimate 2,139.50.
- Management's recorded 1,900.00 is within the range, at the 19th percentile,
  and 239.50 below our point estimate.
- Adjustment of 240 proposed 02/12/2026 and declined 02/13/2026; recorded as
  uncorrected misstatement U-2 on the SAD at WP 9100-02.                   (c)
- Two model deficiencies (omitted forecast component; omitted contract
  assets); maximum plausible misstatement 138 and 28. Neither is a material
  weakness. Reported at WP 8400-07 and to the audit committee 02/13/2026.  (c)

CONCLUSION
The allowance of 1,900 falls within the range developed above and is not, by
itself, materially misstated; the valuation assertion is supported. The 239.50
difference is accumulated as U-2 and considered in the aggregate evaluation of
uncorrected misstatements and bias at WP 9100-02.

TICK MARK LEGEND
(a) Obtained from management; recomputed and traced to the underlying workbook.
(b) Completeness and accuracy of the IPE tested at WP 1800-06 and WP 7100-02.
(c) Judgment, exception, or misstatement; see RESULTS.
================================================================================
```

### Lessons

1. **Replicate before you evaluate.** The $1,900 could not be understood until it was decomposed into $2,008.54 less $215.60 plus
   $100.00 plus $7.06. Two omissions worth $138 and one aggressive assumption worth $196 that net to a number inside the range is
   a coincidence, not an estimate.
2. **A range is not an excuse.** An estimate inside the range is not materially misstated, and the difference from your point
   estimate still goes on the summary of audit differences, because bias is evaluated in aggregate.
3. **Quantify every overlay, and classify before you measure.** "$100 for macroeconomic uncertainty" is not auditable; "$840 of
   Kestrel-acquired balances at an incremental 3.0%" is. And a defensible number in the wrong account is still wrong: the $1,240
   Meridian dispute belonged in revenue.

## Common Mistakes

### Mistake 7.1 — Testing the aged trial balance by agreeing it to the general ledger and stopping there

**What it looks like.** One tick mark: "agreed total to GL, no difference."
**Why it happens.** It is the only test that yields a satisfying nil.
**What goes wrong.** A mis-aging never changes the total; $412 was mis-aged and the allowance understated by $88.
**How to avoid it.** Re-age from invoice date plus contractual terms, and reconcile counts as well as dollars.

### Mistake 7.2 — Treating every confirmation exception as a misstatement, or as an explanation

**What it looks like.** All seven differences projected, or each dismissed as "per client, timing."
**Why it happens.** AS 2310 defines an exception as any difference.
**What goes wrong.** The first forces needless extension; the second conceals cut-off errors. One of seven differences, $60
of $4,610, was a misstatement.
**How to avoid it.** Resolve every difference to an external document before classifying it.

### Mistake 7.3 — Accepting a response whose provenance you have not established

**What it looks like.** An unsigned reply from a personal email address, no copy of the request, filed as "agreed."
**Why it happens.** The amount matches, so the response feels like evidence.
**What goes wrong.** The AS 2310.18 indicators are indicators of interception; a matching amount is what a manipulated
response looks like.
**How to avoid it.** Compare source address to request address, require a signature, and treat failure as a nonresponse.

### Mistake 7.4 — Using an electronic confirmation platform without the Appendix B evaluation

**What it looks like.** "Confirmations sent via [platform]," with its marketing page attached.
**Why it happens.** Firm approval feels like evidence of reliability.
**What goes wrong.** Appendix B requires testing the intermediary's controls *and* assessing company override; if the client
can amend a confirming party's address, AS 2310.B2 bars the platform for those items.
**How to avoid it.** Read the SOC 1 report, test requests end to end, and establish who can create a party record.

### Mistake 7.5 — Matching subsequent cash receipts in total instead of invoice by invoice

**What it looks like.** "Customer owed $240 at 12/31; $240 received in January; cleared."
**Why it happens.** Remittance advices take effort to obtain and the totals agree.
**What goes wrong.** The payment may have settled January invoices, and a short-payment is invisible in the total. Four of
five misstatements here were short-payments totaling $25.9.
**How to avoid it.** Obtain the remittance advice and match invoice by invoice.

### Mistake 7.6 — Extrapolating a misstatement across a stratum tested in full

**What it looks like.** One sample ratio applied to the whole population, significant items included.
**Why it happens.** A single ratio is easier than a stratified projection.
**What goes wrong.** Misstatement in a 100%-tested stratum is known, not projected; 85.9 ÷ 24,300 applied to $36,900 gives
$130, double-counting stratum 1.
**How to avoid it.** Project stratum by stratum, carrying the fully tested stratum at its known amount.

### Mistake 7.7 — Reserving for a credit loss on an amount that will be settled by a credit memo

**What it looks like.** The full aged trial balance run through the matrix with SLA claims still in it.
**Why it happens.** The matrix takes the ATB as its input, and the ATB is gross.
**What goes wrong.** The same exposure is carried twice, as a refund liability and as an expected credit loss — an overlap of
$390 and a double-counted allowance of $17.48.
**How to avoid it.** Reconcile the ATB to the credit-memo accrual and remove the overlap before applying any rate.

### Mistake 7.8 — Treating a disputed invoice as a credit-loss problem

**What it looks like.** A specific reserve in the allowance for the $1,240 Meridian invoice.
**Why it happens.** The balance may not be collected, and that sounds like a credit loss.
**What goes wrong.** A customer that can pay but expects a reduction is a concession under ASC 606-10-32: the answer reduces
revenue, not the allowance, and applies to all similar contracts.
**How to avoid it.** Ask whether the customer can pay before measuring anything.

### Mistake 7.9 — Accepting an undifferentiated qualitative overlay, or omitting in-scope assets

**What it looks like.** "Overlay for macroeconomic uncertainty and integration risk — $100," on a model that never mentions
the $3,020 of contract assets.
**Why it happens.** Challenging an overlay feels like second-guessing judgment.
**What goes wrong.** An overlay with no balance and no rate cannot be back-tested and absorbs whatever the model needs;
AtlasFlow's was $65 larger than the exposures it covered and masked a missing forecast component worth $138.
**How to avoid it.** Require every overlay to be a balance times a rate, and start from the in-scope asset list.

### Mistake 7.10 — Concluding that an estimate inside your range needs no further attention

**What it looks like.** "Management's $1,900 is within our range of $1,780 to $2,410; no misstatement."
**Why it happens.** It answers the materiality question and feels like the end of the analysis.
**What goes wrong.** AS 2501 requires evaluation of each assumption and of bias, and AS 2810 requires the difference from your
best estimate to be aggregated. The $1,900 sits at the 19th percentile and is the product of offsetting errors.
**How to avoid it.** Record the difference as U-2, evaluate each assumption separately, and state where in the range the
recorded amount sits and what would move it.

## Practice Exercises

### Exercise 7-1

[Foundational] Northwind Analytics reports this aging at December 31, 2025 (in thousands) with its loss rates: current
$12,400 at 0.5%; 1–30 days $4,100 at 2.0%; 31–60 days $1,800 at 7.0%; 61–90 days $900 at 20.0%; 91–180 days $600 at 45.0%;
over 180 days $300 at 88.0%. Compute the expected credit loss bucket by bucket, the total, and the allowance as a percentage
of gross receivables.

### Exercise 7-2

[Foundational] Bucket each open invoice at December 31, 2025 and state which would be mis-bucketed by an aging report using a
single global 30-day term: (a) November 25, 2025, net 45; (b) October 31, 2025, net 60; (c) September 15, 2025, net 15;
(d) December 20, 2025, net 30.

### Exercise 7-3

[Foundational] State whether each item is a receivable, a contract asset, or neither, and whether it is in the scope of
ASC 326-20: (a) $380 of December time-and-materials work invoiced January 9, 2026; (b) $1,240 of ramp-driven excess of
cumulative revenue over cumulative invoicing; (c) a $90 unapplied credit memo in account 2230; (d) $1,780 of fixed-fee
services revenue recognized ahead of a milestone invoice; (e) $610 of deferred revenue assumed in the Kestrel acquisition.

### Exercise 7-4

[Intermediate] Gross receivables were $38,600 at December 31, 2025 and $30,500 at December 31, 2024; Q4 billings were $52,240
and $46,000. Using gross receivables ÷ Q4 billings × 92, compute DSO for both years, the change, and the receivables that
would not exist at prior-year velocity. State whether the result is a substantive analytical procedure under AS 2305 and why.

### Exercise 7-5

[Intermediate] An $18,000 population is stratified: stratum A, $9,400, tested 100%, misstatement $41.0; stratum B, $6,200,
sample $1,550, misstatement $18.6; stratum C, $2,400, sample $300, misstatement $2.4. Compute the projected misstatement
against performance materiality of $940, state your conclusion, and name the one further piece of information you want first.

### Exercise 7-6

[Intermediate] For each confirmation difference state whether it is a misstatement, a records difference, or a nonresponse, and
the single document you would obtain to decide: (a) the customer confirms $310 less and says a check was mailed December 31;
(b) confirms $145 less and has no record of an invoice dated December 28; (c) confirms $60 less and says it refused an invoice
because the milestone was not met; (d) replies from a free email domain with no signature.

### Exercise 7-7

[Intermediate] A private SaaS company has 22,000 monthly-billed self-serve accounts totaling $2,100, no ITGC testing, and no
prior-year confirmation experience. The partner proposes negative confirmation requests to 300 of them. Evaluate the proposal
against AS 2310.12 and AS 2310.13, conclude, and describe the procedure you would perform instead.

### Exercise 7-8

[Intermediate] Draft the memo paragraph (100 to 140 words) concluding on the 14 nonresponses in Exhibit 7-7, stating the
procedures performed, the amount substantiated by cash, the treatment of the residue, and the conclusion.

### Exercise 7-9

[Advanced] AtlasFlow's $1,510 receivable from Cirrus Retail Group arises under reseller arrangement C-4 with Tessera Partners,
which holds the contract with Cirrus and takes credit risk. Identify the confirming party and say why; then state the two
substantive questions the request must ask beyond the balance, and what a "no" to either would mean.

### Exercise 7-10

[Advanced] Find the three errors in this extract from a client-prepared allowance workpaper.

```text
ALLOWANCE FOR CREDIT LOSSES - DECEMBER 31, 2025 (000s)
  Current          14,000  x 0.5%  =    70
  1-30 days         5,000  x 2.0%  =   100
  31-60 days        2,200  x 7.0%  =   154
  61-90 days        1,100  x 20.0% =   220
  91-180 days         700  x 45.0% =   315
  Over 180 days       400  x 88.0% =   352
  Subtotal, pooled                    1,271
  Specific reserve, disputed invoice
    (customer is current on all other invoices
     and is not in financial difficulty)  240
  Total allowance                     1,511
  Note: no adjustment for forecast conditions is required because the
  portfolio turns over in approximately 60 days.
```

### Exercise 7-11

[Advanced] A portfolio has these balances and average monthly roll rates: current $18,000 at 12.0%; 1–30 $5,000 at 25.0%;
31–60 $2,000 at 40.0%; 61–90 $800 at 50.0%; 91–180 $500 at 60.0%; over 180 $400 charging off at 90.0%. Compute the cumulative
probability of charge-off for each bucket and the total expected credit loss, and say what a result 31.0% above the loss-rate
answer of $958.0 tells you.

### Exercise 7-12

[Advanced] This exercise spans Chapters 6 and 7. Chapter 6, §6.4 derives FY2025 net invoicing of $162,450. Gross
receivables were $30,500 at January 1, 2025 and $38,600 at December 31, 2025; $1,230 was written off against the
allowance; translation reduced receivables by $110. (a) Compute cash collected from customers in FY2025. (b) Meridian's
contract carries a $2,410 receivable and a deferred revenue balance at December 31, 2025. State how each is presented
and why, and identify the one circumstance in which two contract balances would be netted.

## Solutions to Practice Exercises

### Solution 7-1

$62.0 + $82.0 + $126.0 + $180.0 + $270.0 + $264.0 = **$984.0** on gross receivables of $20,100, so the allowance is
**4.90%**. The two oldest buckets are 4.5% of the balance and 54.3% of the allowance, which is why the aging cut-off
matters more than the current-bucket rate.

### Solution 7-2

(a) Due January 9, 2026 → **current**; global 30 gives 6 days past due. **Mis-bucketed.** (b) Due December 30 → **1–30**;
global 30 gives 31 days. **Mis-bucketed.** (c) Due September 30 → 92 days → **91–180**; global 30 gives 77 days.
**Mis-bucketed.** (d) Due January 19, 2026 → **current**; identical. Three of four are wrong, and every error moves the balance
toward a *lower* loss rate — the direction that understates the allowance.

### Solution 7-3

(a) Receivable; unconditional right; in scope. (b) Contract asset; the right to the next annual invoice is conditional on
continued performance; in scope, because ASC 326-20 covers contract assets. (c) Neither; a refund liability, not netted
against the receivable. (d) Contract asset; the right to invoice is conditional on milestone certification; in scope.
(e) Neither; a contract liability (Chapter 6, §6.9), not in scope.

### Solution 7-4

FY2025: $38,600 ÷ $52,240 × 92 = **68.0 days**. FY2024: $30,500 ÷ $46,000 × 92 = **61.0 days**, up 7.0 days or 11.5%. At FY2024
velocity Q4 2025 billings would support 61 ÷ 92 × $52,240 = $34,637, so about **$3,963** of receivables exist that would not have
at prior-year velocity — 2.7 times overall materiality. It is **not** a substantive analytical procedure: plausible variation in
Q4 billing timing alone moves computed DSO by several days, so the expectation cannot detect $940.

### Solution 7-5

Stratum A is tested in full, so $41.0 is known and is not extrapolated. Stratum B: $6,200 ÷ $1,550 = 4.0, so $18.6 × 4.0 =
$74.4. Stratum C: $2,400 ÷ $300 = 8.0, so $2.4 × 8.0 = $19.2. Projected misstatement = **$134.6**, 14.3% of performance
materiality, requiring no extension subject to qualitative evaluation. Ask for the **cause** first: one systematic cause makes
the projection appropriate and may justify a full-population query, while unrelated one-off errors give sampling risk
(Chapter 15, §15.9) more weight.

### Solution 7-6

(a) Records difference — payment in transit; obtain the bank credit and remittance advice. (b) Records difference — the
customer's ledger lags; obtain the provisioning record showing service commenced before December 31, which establishes the
enforceable right. (c) **Misstatement** — no unconditional right existed at December 31; obtain the milestone acceptance
certificate and its date. (d) A **nonresponse**: reliability is not established under AS 2310.18, so the reply is disregarded
under AS 2310.19; obtain the request log showing the address used.

### Solution 7-7

The proposal fails. Negatives are never sufficient alone and work only alongside other substantive procedures where the
AS 2310.13 conditions hold. The second holds — 22,000 accounts averaging $95 are many small homogeneous items — but the first does
not, because no ITGC testing has been performed, and neither does the third, because no prior-year experience supports an
expectation of few exceptions. Perform instead a full-population subsequent-settlement test: match the processor's post-year-end
settlement file to open balances, stratify the residue by dunning stage, and measure expected credit losses on the unsettled
amounts at the historical ultimate charge-off rate for the same interval.

### Solution 7-8

> Alternative procedures were performed for all 14 accounts totaling $3,995 for which no reliable confirmation response was
> obtained, including the two items re-characterized as nonresponses under AS 2310.19 and AS 2310.22. For each we obtained the
> cash application detail and customer remittance advice for January 1 to February 13, 2026 and matched receipts to the
> specific invoices comprising the December 31, 2025 balance. Cash substantiated $3,189.1, or 79.8%. Four accounts short-paid
> by amounts totaling $25.9, each traced to a December 2025 invoice for a performance obligation satisfied in January 2026 and
> recorded as a misstatement. For the remaining $780.0, the Sundown Media Holdings balance, we examined the order form,
> provisioning record, December usage log, and forbearance letter dated January 20, 2026; existence and rights are supported
> and collectibility is addressed at WP 7300-11.

### Solution 7-9

The confirming party is Tessera Partners LLC, addressed to the controller at the notice-clause address in the reseller master
agreement, because AtlasFlow's receivable is from Tessera. Cirrus owes Tessera, so a Cirrus response would be evidence about a
different asset held by a different entity — the AS 2310.09 knowledgeable, properly addressed party requirement.

Beyond confirming the $1,510 and invoice INV-0087430, the request must ask (1) whether Tessera is obligated to pay irrespective of
whether it collects from Cirrus, and (2) whether any agreement, written or oral, provides for extended terms, a right of return or
cancellation, a price adjustment, or another contingency. A "no" to the first makes the receivable contingent on a collection
AtlasFlow does not control — a valuation and possibly a recognition problem, and evidence against the principal conclusion in
§4.4; a "yes" to the second is a side agreement for the AS 2401 discussion.

### Solution 7-10

**Error 1 — arithmetic.** $70 + $100 + $154 + $220 + $315 + $352 = $1,211, not $1,271; the pooled subtotal is overstated by $60.
Foot the column before evaluating any rate.

**Error 2 — classification.** The $240 is a disputed invoice for a customer current on everything else and not in financial
difficulty — an expected price concession under ASC 606-10-32. It reduces revenue and creates a refund liability; recording it
in the allowance overstates the allowance and bad-debt expense and overstates revenue equally.

**Error 3 — omitted forecast component.** A short life eliminates the need for a *reversion* period, not the requirement to
consider reasonable and supportable forecasts. Correct documentation computes the weighted-average remaining life, states that no
reversion arises, and applies the forecast to the portion of the portfolio whose outcome it can still change.

### Solution 7-11

Cumulative probabilities are the product of the downstream roll rates: over 180, 90.0%; 91–180, 54.0%; 61–90, 27.0%; 31–60,
10.8%; 1–30, 2.7%; current, 0.324%.

| Bucket | Balance | Cumulative rate | Expected loss |
| --- | --- | --- | --- |
| Current | 18,000 | 0.324% | 58.3 |
| 1–30 | 5,000 | 2.700% | 135.0 |
| 31–60 | 2,000 | 10.800% | 216.0 |
| 61–90 | 800 | 27.000% | 216.0 |
| 91–180 | 500 | 54.000% | 270.0 |
| Over 180 | 400 | 90.000% | 360.0 |
| **Total** | **26,700** | | **1,255.3** |

The $297.3 gap is not an error: roll rates come from recent migration behaviour and loss rates from a longer look-back, so a
positive gap measures deterioration the historical rates have not absorbed. The two answers bound the pooled component of a
range, and the gap is the quantified basis for a current-conditions adjustment.

### Solution 7-12

(a) Cash collected = net invoicing + opening receivables − closing receivables − write-offs − the translation reduction:
$162,450 + $30,500 − $38,600 − $1,230 − $110 = **$153,010**. The write-off and translation lines reduce receivables without
producing cash, so omitting them overstates collections by $1,340.

(b) Both are presented gross — the $2,410 in account 1200 and the deferred revenue in accounts 2400 and 2405. ASC 606-10-45 nets
a contract *asset* against a contract *liability* at the contract level, but a receivable is an unconditional right and is never
netted against a contract liability. Netting arises only where the contract's position is a contract asset, such as the $1,240 of
ramp-driven excess revenue on the *same* contract.

## Review Questions

**RQ 7-1.** State the three properties of an aged trial balance that must be established before you rely on it, and which one a
reconciliation to the general ledger does not test.

**RQ 7-2.** Why is past-due status a weaker indicator of credit distress in a portfolio billed annually in advance?

**RQ 7-3.** What does AS 2310.24 require, and how does that differ in architecture from the AU-C 330 presumption?

**RQ 7-4.** When may negative requests, combined with other substantive procedures, provide sufficient appropriate evidence,
and which condition fails at AtlasFlow?

**RQ 7-5.** State the four situations that constitute a nonresponse under AS 2310.

**RQ 7-6.** Name the three AS 2310.18 indicators of interception or alteration, and what you do when one is present.

**RQ 7-7.** What three procedures does Appendix B to AS 2310 require before using an electronic confirmation intermediary, and
what must you do if the company can override its controls?

**RQ 7-8.** Distinguish a confirmation exception from a misstatement and give one AtlasFlow example of each.

**RQ 7-9.** Why can a blank-form request be more reliable than a balance-stated request, and what is the cost?

**RQ 7-10.** Distinguish a receivable from a contract asset, and classify the three components of account 1220.

**RQ 7-11.** State the one question that determines whether an uncollected balance is a credit loss or a price concession, and
the accounts each answer leads to.

**RQ 7-12.** Name the four requirements of ASC 326-20 that drive a CECL model for trade receivables, and explain why reversion
is not operative at AtlasFlow.

**RQ 7-13.** Describe the loss-rate, roll-rate, and vintage methods in one sentence each, and state what the spread between
their results tells you.

**RQ 7-14.** Why is a recorded estimate inside the auditor's range still recorded on the summary of audit differences when it
differs from the auditor's point estimate?

**RQ 7-15.** Why does a portfolio with $1,230 of write-offs and no recoveries warrant investigation, and what two queries
would you run?

## Answers to Review Questions

**RQ 7-1.** Reconciliation to the general ledger in dollars *and* account counts; buckets computed from invoice date plus
contractual terms; and an aging cut-off capturing the right invoices and cash applications. The reconciliation tests only the
first, because a mis-aging redistributes the balance without changing the total.

**RQ 7-2.** The invoice precedes the service, so a large balance goes past due while delivery proceeds normally. Past-due status
then more often signals a purchase-order problem or a billing dispute than inability to pay, which is why §7.9.2 pools by cause
and dunning stage is the better characteristic for self-serve.

**RQ 7-3.** AS 2310.24 requires the auditor either to confirm or to obtain evidence by directly accessing information held by a
knowledgeable external source, with indirect information permitted only on a documented feasibility determination. AU-C 330
instead states a presumption, rebuttable where the balance is immaterial, confirmation would be ineffective, or risk is low and
other procedures address it.

**RQ 7-4.** AS 2310.12 makes negatives alone insufficient. Under AS 2310.13 they may suffice with other substantive procedures
where risk is low *and* controls operate effectively, items are many, small, and homogeneous, and a low exception rate is
expected. The first condition fails: unremediated ITGC deficiencies prevent any conclusion on the Stripe path.

**RQ 7-5.** A request returned undelivered; no response received directly from the intended party; a communication that the
party is unable or unwilling to respond; and an oral response only.

**RQ 7-6.** The response comes from an address other than the one on the request; it is unsigned or does not identify the
confirming party; and it does not include the original request or other evidence of responding to yours. Where reliability
cannot be established, AS 2310.19 requires the response to be disregarded and alternative procedures performed.

**RQ 7-7.** Understand the intermediary's controls over interception and alteration; determine that they are designed and
operating effectively; and assess whether the company can override them. If it can, AS 2310.B2 prohibits using the
intermediary.

**RQ 7-8.** An exception is information in a response differing from information obtained from the company. A misstatement is a
difference between what is recorded and what should be recorded. Pemberton's $310 was an exception only; Calderon's $60 was both.

**RQ 7-9.** A blank form makes the confirming party produce the amount from its own records rather than assent to one you
supplied. The cost is response rate — 58.3% against 71.1% — so alternative procedures, generally less persuasive, are performed
on more items.

**RQ 7-10.** A receivable is an unconditional right with only the passage of time remaining; a contract asset is conditional on
something further. Of the $3,400 in account 1220, the $380 invoiced in January is a receivable and the $1,780 of pre-milestone
services revenue and $1,240 of ramp-driven excess are contract assets, all three in the scope of ASC 326-20.

**RQ 7-11.** Can the customer pay? If not, the shortfall is a credit loss charged to the allowance and to general and
administrative expense. If it can but expects a reduction, the shortfall is variable consideration under ASC 606, reducing
revenue and creating a refund liability in account 2230 — and must then be estimated for all similar contracts.

**RQ 7-12.** Lifetime expected loss rather than a probable-and-estimable threshold; collective measurement where risk
characteristics are similar and individual where they are not; historical loss information adjusted for current conditions and
reasonable and supportable forecasts; and reversion beyond the forecastable period. Reversion is not operative because the
pool's remaining life is 1.5 months, inside a twelve-month horizon.

**RQ 7-13.** The loss-rate method multiplies each aging bucket by a historical ultimate-loss rate; the roll-rate method cascades
bucket-to-bucket migration probabilities to charge-off; the vintage method applies the cumulative loss curve of seasoned
vintages to balances grouped by origination period. The spread — $1,474.7, $1,574.5, and $1,693.6 — measures how far recent
behaviour departs from long-run history and sets the pooled component of the range.

**RQ 7-14.** Because materiality and bias are different questions. AS 2501 requires evaluation of each assumption and of bias,
and AS 2810 requires uncorrected differences to be aggregated; an estimate at the 19th percentile within a population of
uncorrected items that mostly reduce the loss is evidence about the statements as a whole.

**RQ 7-15.** A zero recovery rate on $1,230 of write-offs is implausible for active business customers, and the usual
explanation is that recovered cash was credited elsewhere. Query cash receipts applied to accounts with no open invoice at the
receipt date, and scan credits to revenue and to general and administrative expense referencing recovery or written-off
customers' account numbers.

## Key Definitions

**Aged trial balance.** Open customer balances grouped by days past due and reconciled to the general ledger control account;
IPE, testable under AS 1105 before reliance.

**Alternative procedures.** Procedures performed where confirmation yields no reliable evidence; AS 2310 Appendix C points to
subsequent cash receipts matched to the invoices paid, and to contracts and purchase orders.

**Blank form confirmation request.** A positive request omitting the amount; per the Note to AS 2310.08, potentially more
reliable at the cost of response rate.

**Confirmation exception.** Information in a response differing from information obtained from the company; a misstatement only
if the recorded amount proves wrong.

**Contract asset.** A right to consideration for goods or services already transferred, conditional on something other than the
passage of time (ASC 606-10-45); in the scope of ASC 326-20.

**Current expected credit loss (CECL).** The ASC 326-20 model requiring a lifetime expected-loss allowance from historical loss
information adjusted for current conditions and reasonable and supportable forecasts.

**Days sales outstanding (DSO).** Gross receivables ÷ billings for a period × days in that period; AtlasFlow's disclosed metric
is $38,600 ÷ $52,240 × 92 = 68.0 days.

**Dunning.** Automated retries, notifications, and service restrictions applied after a payment method fails; dunning stage, not
days past due, predicts loss in a card-billed portfolio.

**Electronic confirmation intermediary.** A third party transmitting requests and responses; AS 2310.17 and Appendix B require
its controls over interception and alteration to be tested and company override to be assessed.

**Individually evaluated receivable.** A receivable measured on its own facts because it no longer shares risk characteristics
with any pool — here the $980 Sundown Media Holdings balance.

**Information produced by the entity (IPE).** Company-generated data used as evidence, testable under AS 1105; the ATB,
credit-memo register, write-off register, and Stripe settlement file are all IPE.

**Loss-rate method.** Each aging bucket multiplied by a historical ultimate-loss rate; the most common method for trade
receivables and the most sensitive to the aging's accuracy.

**Negative confirmation request.** A request asking for a reply only on disagreement; under AS 2310.12 not sufficient
appropriate evidence on its own.

**Nonresponse.** A request returned undelivered, no reply from the intended confirming party, a communication that the party is
unable or unwilling to respond, or an oral response only.

**Pooling.** Grouping assets with similar risk characteristics for collective measurement; for SaaS, separate enterprise direct,
channel, and self-serve before applying aging as a second dimension.

**Price concession.** A reduction expected to be granted to a customer able to pay, treated as variable consideration under
ASC 606-10-32 and so as a reduction of the transaction price, not a credit loss.

**Projected misstatement.** Misstatement in a population extrapolated from a sample; misstatement in a stratum tested in full is
known and is not extrapolated.

**Reasonable and supportable forecast period.** The horizon over which forecasts of the relevant economic conditions can be
supported, and over which they must be reflected in the estimate.

**Reversion.** The ASC 326-20 requirement to revert to historical loss information beyond the forecast period; not operative
where expected life falls entirely inside it.

**Roll-rate method.** Bucket-to-bucket migration probabilities cascaded to charge-off; being drawn from recent behaviour, it
responds to deterioration faster than a long-run loss rate.

**Vintage method.** The cumulative loss curve of fully seasoned vintages applied to balances grouped by origination period;
insensitive to the aging report, so an independent check on Method 1.

**Write-off.** Removal of a receivable with no reasonable expectation of recovery, charged against the allowance; writing off a
disputed balance for a customer that can pay misclassifies a concession as a loss.

## Chapter Summary

1. Gross receivables of $38,600 are 26.6 times performance materiality, yet 2,876 of 3,140 enterprise accounts hold less than
   $10 each, so stratification is the only workable design.
2. The aged trial balance requires three tests — reconciliation, independent re-aging, and the aging cut-off — and only the
   second detects the $412 mis-aging that understated the pooled loss computation by $88.
3. AS 2310.24 requires confirmation or direct access to a knowledgeable external source; negatives alone never suffice, and the
   AS 2310.13 conditions fail at AtlasFlow, which is why 11,400 self-serve accounts were tested by settlement.
4. Control over the process is the requirement most often documented and least often performed: request 12 matched the recorded
   balance to the dollar and was worthless, because the address came from the audited company.
5. Of seven exceptions totaling $4,610 one was a $60 misstatement; of 14 nonresponses totaling $3,995, cash settled $3,189.1 and
   four short-payments revealed a further $25.9 no confirmation would have found. Projected stratum by stratum with the fully
   tested stratum at its known amount, $60.0 + $98.9 + $26.0 = $184.9, recorded as U-1 of $(185).
6. A disputed balance is a credit question only if the customer cannot pay; Meridian's $1,240 was a concession question that
   settled in full on February 18, 2026.
7. Three CECL methods on the same $35,990 pool give $1,474.7, $1,574.5, and $1,693.6, and adjusting the population matters more
   than the rates: it moves the mechanical answer from $2,008.54 to $1,574.50.
8. Management's $1,900 sits at the 19th percentile of the $1,780–$2,410 range and $239.50 below the $2,139.50 point estimate —
   two conservative omissions worth $138 net of one aggressive assumption worth $196 — so the difference is U-2 of $(240),
   evaluated for bias in aggregate. Every overlay must be an identified balance times a rate.
9. DSO rose from 61.0 to 68.0 days, implying about $3,963 of receivables that would not exist at prior-year velocity, while
   allowance coverage of balances 31 or more days past due *fell* from 27.0% to 24.2%.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Order-to-cash and revenue cut-off | 4, §4.6–§4.8 | The cause of the U-1 cut-off misstatements |
| Standalone selling price and allocation | 5 | The amounts invoiced on multi-element contracts |
| Contract liabilities and the billings bridge | 6, §6.4, §6.8 | The other side of account 1220; the $162,450 in Exercise 7-12 |
| Cash receipt cut-off and bank evidence | 8, §8.4 | Cut-off for the receipts substantiating this account |
| Sample size and the allowance for sampling risk | 15, §15.5–§15.9 | The sizes in Exhibit 7-4 and the projection mechanics |
| Manual journal entries to receivables and the allowance | 16 | W-12 leaves manual entries without evidence of review |
| Late-quarter contracts and side agreements | 17 | The existence significant risk |
| Severity of the credit-memo and write-off deviations | 14 | Whether the §7.8 and §7.11 deviations aggregate |
| Predictive receivable analytics | 18, §18.6 | Extends §7.13 beyond ratio analysis |
| Accumulation of U-1 and U-2 and the evaluation of bias | 19, §19.3 | Where $(185) and $(240) enter the net $(460) |
| Credit-quality and concentration disclosure drafting | 20 | Drafts the language that §7.12 tests |

## Further Reading

- PCAOB AS 2310, *The Auditor's Use of Confirmation*, with its appendices on definitions, intermediaries, and alternative
  procedures, and the PCAOB's implementation resources for the standard.
- PCAOB AS 2501, AS 2810, AS 1105, and AS 2315 on estimates, evaluation of results, evidence, and sampling; AICPA AU-C 330,
  AU-C 505, and AU-C 540.
- FASB ASC 326-20 and ASU 2016-13, including the basis for conclusions on the forecast and reversion requirements;
  ASC 606-10-45 and 606-10-32; ASC 275-10-50; and SEC Regulation S-X Rules 5-02 and 12-09.
- The AICPA audit guide on credit losses, for loss-rate, roll-rate, and vintage illustrations outside banking.



