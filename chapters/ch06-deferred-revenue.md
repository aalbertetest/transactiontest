# Chapter 6 — Deferred Revenue, Contract Liabilities, and RPO

> Deferred revenue is the only large liability on a SaaS balance sheet that management has an incentive to
> understate, and it is the only account where the auditor's instinct — test what is recorded — points in
> exactly the wrong direction. AtlasFlow's $78,200 thousand contract liability at December 31, 2025 is not a
> population you can select from; it is the residue of 14,392 contract-level balances, and the balance that
> matters most is the one that should be there and is not. The same population, extended to include amounts not
> yet billed, produces the $214,000 thousand remaining performance obligation disclosure, a figure investors
> read more closely than any line in the statements and that most engagement teams treat as a footnote instead
> of as a recomputable population.

## Learning Objectives

- **LO 6.1** Explain what a contract liability is and distinguish it from a refund liability, a customer
  deposit, and unearned interest.
- **LO 6.2** Justify why completeness is the dominant relevant assertion for deferred revenue and redesign
  procedures accordingly.
- **LO 6.3** Construct and test a deferred revenue roll-forward, identifying and substantiating each component
  of the movement.
- **LO 6.4** Compute the billings bridge from revenue and the change in deferred revenue, and extend it to cash
  collected from customers.
- **LO 6.5** Recompute the current and noncurrent split of a deferred revenue balance and state the drivers of
  the split.
- **LO 6.6** Recompute a contract-level deferred revenue balance from the contract document and evaluate the
  differences.
- **LO 6.7** Design and perform a test that amounts released from deferred revenue were earned.
- **LO 6.8** Apply the contract-level netting rule to determine whether a contract's position is a contract
  asset or a contract liability, and reconcile the gross-up.
- **LO 6.9** Measure deferred revenue assumed in a business combination under ASC 805 as amended by
  ASU 2021-08, and test it when the acquiree had no revenue recognition policy.
- **LO 6.10** Explain why a foreign-currency contract liability is a non-monetary item and test that it has not
  been remeasured.
- **LO 6.11** Recompute a remaining performance obligation disclosure from a contract population, evaluate the
  practical expedients elected and their disclosure consequences, and quantify the effect of contract-term
  judgments.
- **LO 6.12** Evaluate deferred revenue analytics — coverage of forward revenue, the deferred-revenue-to-ARR
  ratio, and the aging of deferred revenue — and state the threshold for investigation.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| FASB ASC | 606-10-45 (presentation) | Requires an unconditional right to consideration to be presented as a receivable and a conditional right as a contract asset; requires the net contract position to be determined at the contract level, not by account |
| FASB ASC | 606-10-50-8 through 50-10 | Requires disclosure of opening and closing contract balances, revenue recognized in the period that was included in the opening contract liability, and an explanation of significant changes |
| FASB ASC | 606-10-50-13 through 50-15 | Requires disclosure of the aggregate transaction price allocated to remaining performance obligations and when it is expected to be recognized; permits the practical expedients for contracts with an original expected duration of one year or less and for certain variable consideration; requires disclosure of which expedients were applied and qualitative information about excluded consideration |
| FASB ASC | 606-10-32-2 through 32-27 | Determines the transaction price, including the constraint, that becomes the measured amount of the contract liability |
| FASB ASC | 606-10-25-1 through 25-3 | Establishes when a contract exists and the enforceable rights and obligations that define the contract term — the driver of the termination-for-convenience analysis |
| FASB ASC | 606-10-55-46 through 55-49 | Refund liabilities and rights of return, distinguished from contract liabilities |
| FASB ASC | 805-20 as amended by ASU 2021-08 (effective for public business entities for fiscal years beginning after December 15, 2022) | Requires contract assets and contract liabilities acquired in a business combination to be measured in accordance with ASC 606 as if the acquirer had originated the contracts, rather than at fair value |
| FASB ASC | 830-10-45 | Distinguishes monetary from non-monetary items; a contract liability is non-monetary and is not remeasured for subsequent exchange rate changes |
| SEC | Regulation S-X Rule 5-02 | Requires classification of liabilities as current and noncurrent based on the operating cycle, driving the $71,300 / $6,900 split |
| SEC | Regulation S-K Items 101 and 303 | Require disclosure of order-book and backlog information where material to an understanding of the business, and MD&A discussion of known trends — where AtlasFlow discusses RPO growth |
| PCAOB | AS 2110 | Requires identification of risks of material misstatement at the assertion level, including completeness of liabilities |
| PCAOB | AS 2301 | Requires the nature, timing, and extent of further procedures to respond to assessed risk; addresses testing that responds to a completeness risk |
| PCAOB | AS 2305 | Governs substantive analytical procedures, including the four elements of a valid expectation and the threshold for investigating differences — the standard the roll-forward and billings bridge analytics must satisfy |
| PCAOB | AS 1105 | Sets the sufficiency and appropriateness framework, including the reliability of information produced by the entity (IPE) — the roll-forward and the RPO schedule are both IPE |
| PCAOB | AS 2810 | Requires evaluation of the presentation of the financial statements, including whether disclosures are informative and comply with the framework |
| PCAOB | AS 2401 | Requires responsive procedures to the presumed fraud risk in revenue recognition, which in a subscription business runs through the release of deferred revenue |
| AICPA | AU-C 315 (as amended by SAS 145, effective for periods ending on or after December 15, 2023) | The AICPA analogue to AS 2110 |
| AICPA | AU-C 330 | The AICPA analogue to AS 2301, including the requirement to design procedures responsive to a completeness risk |
| AICPA | AU-C 520 | The AICPA analogue to AS 2305; substantively equivalent for the analytics in §6.14 |
| AICPA | AU-C 240, AU-C 230, AU-C 700 | Fraud, documentation, and the evaluation of financial statement presentation and disclosure |

Because AtlasFlow is an SEC issuer, PCAOB standards govern. Readers auditing private SaaS companies apply the
AICPA analogues, with two differences that matter in this chapter. First, there is no auditor attestation on
internal control, so the deficiency evaluation in §6.6 and §6.11 feeds only the AU-C 265 communication rather
than an ICFR opinion. Second, private companies frequently elect the one-year practical expedient for the RPO
disclosure or, as non-public entities, do not present the maturity disclosure at all — which removes the single
richest recomputable population in the file and requires the completeness of deferred revenue to be tested
without it.

## Prerequisites and Chapter Dependencies

Read Chapter 5 first: the allocation of the transaction price across performance obligations determines the
amounts that sit in the contract liability, and the walkthrough in this chapter picks up contract C-1's
$3,647.56 net position where Chapter 5's walkthrough left it. Chapter 4 supplies the order-to-cash process and
the cut-off procedures, and Chapter 3 the materiality figures ($1,450 overall, $940 performance materiality,
$72 clearly trivial threshold). Chapter 7 owns the receivable side of the netting mechanics and the credit-loss
model; Chapter 18 develops the analytics technique that §6.14 applies; Chapter 20 drafts the disclosure
language that this chapter tests.

## 6.1 What a Contract Liability Is

A **contract liability** is an entity's obligation to transfer goods or services to a customer for which the
entity has received consideration, or for which the amount is due, from the customer. Three features follow and
each is a source of error in practice.

**It is measured by allocation, not by invoicing.** The amount of the liability is the allocated transaction
price for the unsatisfied portion of each performance obligation, adjusted for what has been billed. On a
multi-element contract the liability bears no fixed relationship to the invoice. Chapter 5, §5.7 allocated
contract C-1's $3,120 transaction price to four obligations; the liability at December 31, 2025 is a function of
those four allocations and of two invoices, and it is $3,647.56 on a contract that has been invoiced $960,000.

**It is non-monetary.** It will be extinguished by delivering service, not by paying currency. That is why it is
not remeasured for exchange rate changes (§6.10) and why it is not discounted for the time value of money unless
a significant financing component exists.

**It is not the same as a refund liability or a customer deposit.** A **refund liability** is an obligation to
return consideration in cash; it is measured at the amount the entity expects to refund and is not part of the
transaction price allocated to performance obligations. AtlasFlow keeps refund liabilities in account 2230
($1,200 at December 31, 2025) precisely so that they are not confused with the contract liability in accounts
2400, 2405, and 2410 (§6.13). A **customer deposit** held against future orders that have not been specified is
not a contract liability at all until a contract exists.

**Exhibit 6-1. AtlasFlow's contract liability accounts at December 31, 2025 (in thousands).**

| Account | Description | 12/31/2025 | 12/31/2024 | Change |
| --- | --- | --- | --- | --- |
| 2400 | Deferred revenue — subscription, current | 66,800 | 53,600 | 13,200 |
| 2405 | Deferred revenue — professional services, current | 4,500 | 3,300 | 1,200 |
| 2410 | Deferred revenue — noncurrent | 6,900 | 5,400 | 1,500 |
| | **Total contract liability** | **78,200** | **62,300** | **15,900** |
| 2230 | Customer credits and refunds payable (a refund liability, not a contract liability) | 1,200 | 940 | 260 |

The FY2024 split of the $56,900 current balance between subscription and professional services ($53,600 and
$3,300) is an extension for purposes of the illustrations in this chapter; the continuing case records only the
$56,900 total. The FY2024 refund liability of $940 is likewise an extension.

## 6.2 Why Completeness Is the Dominant Assertion

For revenue, the presumed direction of misstatement is overstatement, and the assertions that matter are
occurrence, accuracy, and cut-off. Turn the same transaction around and look at the liability, and the direction
reverses: a liability that is too small is the mirror image of revenue that is too large. Every mechanism that
overstates revenue understates deferred revenue by the same amount.

This has three practical consequences, and getting them wrong is the single most common design failure on this
account.

**First, you cannot sample from the recorded balance to test completeness.** Selecting 30 of the 14,392 recorded
contract-level balances and agreeing each to its contract tests existence and accuracy. It provides no evidence
about a contract that has been invoiced and whose entire balance was released to revenue, because that contract
has a zero balance and is not in the population you selected from. The population you need is the population of
*contracts*, not the population of *balances*.

**Second, the procedures that provide completeness evidence are population-level, not sample-level.** Four do
most of the work:

1. **The roll-forward** (§6.3), which forces every movement to be explained and is the only procedure that
   directly addresses whether the ending balance is the beginning balance plus billings less earned revenue.
2. **The billings bridge** (§6.4), which independently derives billings from revenue and the change in the
   liability and reconciles the result to the invoice register — closing the loop between three populations.
3. **Reciprocal-population testing**: start from the *billing* population and prove that every invoice created
   either revenue or a contract liability. An invoice that created neither is a completeness error in one or the
   other.
4. **The RPO recomputation** (§6.11), which builds the liability and the unbilled remainder from the contract
   population and therefore cannot miss a contract that has been zeroed out.

**Third, the tests of details you do perform must be directional.** When you recompute a contract's balance and
find a difference, the direction tells you what happened. A recorded balance *below* your recomputation means
revenue was released early — the error management has an incentive to make. A recorded balance *above* your
recomputation means revenue was released late, or an invoice was recorded against the wrong contract, and it is
usually an error of execution rather than of bias. Sort your exceptions by direction before you evaluate them.

**Exhibit 6-2. Mapping deferred revenue risks to procedures.**

| What could go wrong | Direction | Assertion | Procedure that addresses it |
| --- | --- | --- | --- |
| Revenue released before the service period begins | DR understated | Completeness | Contract-level recomputation (§6.6); the RPO recomputation (§6.11) |
| Revenue released for services not delivered (training, professional services milestones) | DR understated | Completeness | Delivery-evidence testing (§6.7) |
| An invoice issued but not recorded as a liability or as revenue | DR understated | Completeness | Billings bridge and reciprocal testing from the invoice register (§6.4) |
| The full ramped contract fee spread evenly rather than the allocated amount | DR misstated either way | Accuracy | Contract-level recomputation (§6.6); Chapter 5, §5.9 |
| Balances left in deferred revenue after the service period ended | DR overstated | Existence | Aging of deferred revenue (§6.14) |
| Amounts recognizable beyond twelve months classified as current | Classification | Classification | Recomputation of the split (§6.5) |
| A contract with a net asset position netted against another contract's liability | Presentation | Presentation | Contract-level netting test (§6.8) |
| Acquired deferred revenue measured at the acquiree's unreliable carrying amount | DR misstated either way | Accuracy | ASC 805 / ASU 2021-08 recomputation (§6.9) |
| A foreign-currency liability remeasured at the closing rate | DR misstated either way | Accuracy | Revaluation job account-list inspection and recomputation (§6.10) |
| Non-enforceable contract portions included in the RPO disclosure | RPO overstated | Presentation and disclosure | Contract-term analysis on the termination clause population (§6.11) |

## 6.3 The Deferred Revenue Roll-Forward as the Central Audit Vehicle

The roll-forward is the organizing document for this account for the same reason the bank reconciliation is the
organizing document for cash: every number in the balance has to have arrived from somewhere, and the
roll-forward is where you make each arrival prove itself. It is also information produced by the entity, so its
completeness and accuracy must be tested rather than assumed.

**Exhibit 6-3. AtlasFlow deferred revenue roll-forward, FY2025 (in thousands).**

| Component | Amount | Tick | Source and how it is substantiated |
| --- | --- | --- | --- |
| Deferred revenue, January 1, 2025 (current $56,900 + noncurrent $5,400) | 62,300 | (a) | Agreed to the FY2024 audited balance sheet |
| Billings recorded through deferred revenue, net of credit memos | 163,750 | (b) | Derived independently in the billings bridge (§6.4) and reconciled to the Zuora Billing invoice register |
| Revenue recognized from the January 1, 2025 balance | (54,900) | (c) | RevPro contract-level schedules filtered to pre-2025 billing dates; this figure is also the ASC 606-10-50-8 disclosure |
| Revenue recognized from FY2025 billings | (93,300) | (c) | RevPro contract-level schedules filtered to FY2025 billing dates |
| Deferred revenue assumed in the Kestrel Labs acquisition | 610 | (d) | Recomputed from 61 acquired contracts under ASC 805 as amended (§6.9) |
| Foreign currency translation of the UK and Australian balances | (260) | (e) | Recomputed from the CONSOL_FY25_v14.xlsx translation tab (§6.10) |
| **Deferred revenue, December 31, 2025** | **78,200** | (f) | Agreed to the trial balance, accounts 2400 + 2405 + 2410 |
| Of which: current | 71,300 | (g) | Recomputed in §6.5 |
| Of which: noncurrent | 6,900 | (g) | Recomputed in §6.5 |

Tick mark legend: (a) agreed to prior-year audited financial statements; (b) see Exhibit 6-4; (c) agreed to the
RevPro "Revenue Contract Summary" and, in total, to revenue per the statement of operations of $148,200; (d) see
Exhibit 6-12; (e) see Exhibit 6-13; (f) agreed to the NetSuite trial balance and to the balance sheet; (g)
recomputed, Exhibit 6-6.

Four proofs must be run on this schedule before you use it for anything else.

**Proof 1 — the roll-forward foots.** $62,300 + $163,750 − $54,900 − $93,300 + $610 − $260 = $78,200. Run it.
A roll-forward that does not foot has a plug in it, and the plug is where the audit is.

**Proof 2 — total revenue released equals total revenue.** $54,900 + $93,300 = $148,200, which equals total
revenue per the statement of operations. That equality is not automatic: it holds at AtlasFlow because every
revenue transaction passes through deferred revenue in the RevPro subledger, including revenue recognized in
advance of invoicing, which is then reclassified to account 1220 as an unbilled receivable (§6.8). At an entity
where unbilled revenue is credited directly to revenue and debited to a contract asset without passing through
deferred revenue, this proof will not hold and you must establish the correct identity before you rely on it. Ask
how revenue in advance of billing is recorded; do not infer it.

**Proof 3 — the split of released revenue is not arbitrary.** The $54,900 released from the opening balance is
the ASC 606-10-50-8 disclosure ("revenue recognized in the reporting period that was included in the contract
liability balance at the beginning of the period") and appears in the AtlasFlow revenue footnote. Test it by
independent recomputation, not by inquiry: filter the RevPro revenue-schedule detail to lines whose funding
invoice predates January 1, 2025 and sum. A common error is to compute it as the *entire* opening balance less
whatever remains, which overstates it whenever any opening balance is still deferred at year end. Sanity-check
it: $54,900 released from a $62,300 opening balance means 88.1% of the opening balance was earned during the
year, which is consistent with a contract population dominated by annual terms billed in advance, and
$62,300 − $54,900 = $7,400 of the opening balance remained deferred at year end, which is consistent with the
$6,900 noncurrent balance plus a portion of long-dated current amounts.

**Proof 4 — non-billing movements are separately substantiated.** The $610 acquired balance and the $(260) of
translation are the two components that did not arise from a customer invoice. Both are the kind of item that
gets buried in a "billings" line to make a schedule foot. Insist on seeing them separately, and recompute both
(§6.9 and §6.10).

**What an unexpected result looks like.** If the roll-forward's billings line is presented as a plug — that is,
if management computes billings as the ending balance less the beginning balance plus revenue — the schedule
proves nothing, because it cannot fail to foot. The tell is that management cannot produce the invoice register
total that agrees to it. In that situation the billings line must be independently sourced from Zuora Billing
before the roll-forward has any evidential value.

## 6.4 The Billings Bridge

Billings are not a GAAP measure and do not appear in the financial statements, which is exactly why the bridge is
useful: it is an identity that connects three separately maintained populations — the revenue subledger, the
contract liability, and the invoice register — and any break in it must be explained.

The identity, stated carefully:

```text
Total invoicing, net of credit memos
    = Revenue recognized
      + Increase (- decrease) in deferred revenue
      - Increase (+ decrease) in contract assets and unbilled receivables
      - Deferred revenue assumed in a business combination
      + Reduction (- increase) of deferred revenue from foreign currency translation

Cash collected from customers
    = Total invoicing, net of credit memos
      + Beginning gross accounts receivable
      - Ending gross accounts receivable
      - Receivables written off against the allowance
      + Reduction (- increase) of receivables from foreign currency translation
```

**Exhibit 6-4. AtlasFlow billings bridge, FY2025 (in thousands).**

| Line | Component | Amount | Tick |
| --- | --- | --- | --- |
| 1 | Total revenue per the statement of operations | 148,200 | (a) |
| 2 | Deferred revenue, December 31, 2025 | 78,200 | (b) |
| 3 | Deferred revenue, January 1, 2025 | (62,300) | (b) |
| 4 | Increase in deferred revenue (line 2 + line 3) | 15,900 | |
| 5 | Less: deferred revenue assumed in the Kestrel acquisition (non-billing) | (610) | (c) |
| 6 | Add back: reduction of deferred revenue from foreign currency translation (non-billing) | 260 | (d) |
| 7 | **Billings recorded through deferred revenue (lines 1 + 4 + 5 + 6)** | **163,750** | (e) |
| 8 | Less: increase in contract assets and unbilled receivables ($3,400 − $2,100) | (1,300) | (f) |
| 9 | **Total invoicing, net of credit memos** | **162,450** | (g) |

Arithmetic: $148,200 + $15,900 − $610 + $260 = $163,750, which agrees to the roll-forward's billings line in
Exhibit 6-3; $163,750 − $1,300 = $162,450.

Line 8 requires explanation because it is the step most teams omit. In AtlasFlow's subledger, revenue recognized
in advance of invoicing is credited to revenue and debited to deferred revenue, producing a negative
contract-level deferred revenue balance that is reclassified to account 1220 in the general ledger (§6.8).
Consequently the $163,750 in the roll-forward includes $1,300 of "billings" that were never invoiced. Total
actual invoicing is therefore $1,300 lower. Agree the $162,450 to the Zuora Billing invoice register for the year:

```sql
SELECT SUM(CASE WHEN i.document_type = 'Invoice'    THEN i.amount ELSE 0 END)  AS gross_invoiced,
       SUM(CASE WHEN i.document_type = 'CreditMemo' THEN i.amount ELSE 0 END)  AS credit_memos,
       SUM(CASE WHEN i.document_type = 'Invoice'    THEN i.amount
                WHEN i.document_type = 'CreditMemo' THEN -i.amount END)        AS net_invoiced,
       COUNT(*)                                                                AS document_count
FROM   zuora_billing.invoice i
WHERE  i.posted_date BETWEEN '2025-01-01' AND '2025-12-31'
  AND  i.status = 'Posted';
```

*For purposes of this illustration, assume* the query returned gross invoiced amounts of $166,290, credit memos
of $3,840, net invoicing of $162,450, and a document count of 158,412 — the count driven by the 11,400 self-serve
accounts billed monthly. The $162,450 agrees to line 9 exactly.

### 6.4.1 Extending the bridge to cash

**Exhibit 6-5. Extension of the bridge to cash collected from customers, FY2025 (in thousands).**

| Line | Component | Amount | Tick |
| --- | --- | --- | --- |
| 1 | Total invoicing, net of credit memos (Exhibit 6-4, line 9) | 162,450 | (g) |
| 2 | Gross accounts receivable, January 1, 2025 ($29,150 net + $1,350 allowance) | 30,500 | (b) |
| 3 | Gross accounts receivable, December 31, 2025 ($36,900 + $1,700) | (38,600) | (b) |
| 4 | Receivables written off against the allowance ($1,350 + $1,780 provision − $1,900) | (1,230) | (h) |
| 5 | Reduction of receivables from foreign currency translation | (110) | (d) |
| 6 | **Cash collected from customers** | **153,010** | (i) |

Arithmetic: $162,450 + $30,500 − $38,600 − $1,230 − $110 = $153,010. The write-off figure is derived from the
allowance roll-forward: opening allowance $1,350 plus the FY2025 provision for credit losses of $1,780 per the
statement of cash flows, less the closing allowance of $1,900, equals $1,230 of write-offs net of recoveries.
The $(110) of translation is an extension for purposes of this illustration.

Agree the $153,010 to customer cash receipts posted to accounts 1010, 1020, and 1205 through the bank feed
(interface I-9) and the Stripe daily journal (interface I-4). Two cautions. First, cash receipts include items
that are not collections of trade receivables — interest income of $5,110 is posted to 7100 and must not be
swept into the comparison. Second, the Stripe self-serve channel collects cash at the moment of billing, so its
receipts and its invoicing are nearly equal and a difference there points to a failure in the Lambda job
(weakness W-7), not to a collection issue.

**What an unexpected result looks like.** *For purposes of this illustration, assume* the bridge had produced
$153,010 against actual receipts of $151,430, a difference of $1,580, or 1.0% of collections and 109% of overall
materiality. That difference is not a rounding matter and there are only four candidate explanations: invoicing
recorded that was never issued (a revenue and receivable overstatement); receivables written off without going
through the allowance; a receivable balance in the wrong period; or receipts posted somewhere other than the
three accounts you queried. Test them in that order, because the first is the one management has an incentive to
create. The bridge does not tell you which; it tells you that one of four things is true, which is far more than
you knew before you built it.

## 6.5 Current Versus Noncurrent Classification

The split is driven by a single question asked contract by contract: of the amounts already billed and not yet
earned, how much will be recognized as revenue within twelve months of the balance sheet date? Everything else is
noncurrent. Three facts about a SaaS contract population determine the answer.

**Driver 1 — the billing frequency, not the contract term.** A 36-month contract billed annually in advance
generates a *current* liability of twelve months or less at every measurement date, because only one year has
been billed. C-1 Meridian's 36-month term contributes nothing to the noncurrent balance at December 31, 2025 for
this reason. A 36-month contract billed once up front generates two years of noncurrent liability.

**Driver 2 — mid-period billings.** A contract invoiced on November 1, 2025 for twelve months has ten months
remaining at December 31, 2025 and is entirely current. A contract invoiced on November 1, 2025 for twenty-four
months has twenty-two months remaining, of which twelve are current and ten noncurrent.

**Driver 3 — multi-year prepayments and services.** AtlasFlow's $6,900 noncurrent balance comes almost entirely
from a small number of customers who negotiated a multi-year prepayment for a discount, plus long-dated training
packages and implementation milestones.

**Exhibit 6-6. Recomputation of the current and noncurrent split at December 31, 2025 (in thousands).**

| Scheduled recognition period of amounts already billed and unearned | Amount | Classification |
| --- | --- | --- |
| January – March 2026 | 27,600 | Current |
| April – June 2026 | 20,700 | Current |
| July – September 2026 | 13,600 | Current |
| October – December 2026 | 9,400 | Current |
| **Subtotal — recognizable within twelve months (current)** | **71,300** | |
| January – December 2027 | 5,600 | Noncurrent |
| January 2028 and later | 1,300 | Noncurrent |
| **Subtotal — recognizable after twelve months (noncurrent)** | **6,900** | |
| **Total deferred revenue** | **78,200** | |

The quarterly pattern is itself audit evidence. In a population dominated by annual contracts billed in advance
at dates distributed roughly evenly through the year, the amount releasing in each successive quarter should
decline, because a contract billed in February 2025 has only one month of liability left at year end while one
billed in November 2025 has ten. A declining series of approximately 4 : 3 : 2 : 1 is what you expect. AtlasFlow's
$27,600 : $20,700 : $13,600 : $9,400 has that shape, with Q4 2026 slightly above the pure geometry because
multi-year contracts contribute to the far end of the current window.

**How to recompute it.** Run the RevPro revenue schedule for every contract, restricted to scheduled revenue
funded by invoices already issued at December 31, 2025, and sum by scheduled recognition month:

```sql
SELECT DATE_TRUNC('quarter', s.scheduled_period)                      AS recognition_quarter,
       SUM(s.scheduled_revenue)                                       AS amount
FROM   revpro.revenue_schedule s
JOIN   revpro.performance_obligation po ON po.po_id = s.po_id
WHERE  s.scheduled_period          >  '2025-12-31'
  AND  s.funding_invoice_date      <= '2025-12-31'
  AND  s.schedule_status            = 'Active'
GROUP BY 1
ORDER BY 1;
```

Then test the extract's completeness and accuracy: the sum of all rows with `scheduled_period > '2025-12-31'` and
`funding_invoice_date <= '2025-12-31'` must equal $78,200, and the sum of all rows with
`scheduled_period <= '2025-12-31'` must equal FY2025 revenue plus prior-period revenue on active contracts.
Without that reconciliation the query result is an unsupported number in a spreadsheet.

**What an unexpected result looks like.** A noncurrent balance that is a round percentage of the total — 8.8% of
$78,200 is $6,882, uncomfortably close to $6,900 — is a warning that the split may have been estimated as a
percentage rather than computed. Ask for the query. If management computed the split by applying the prior-year
ratio, the classification is an estimate and you must recompute it, because the mix of multi-year prepayments
changes every year. Misclassification does not affect the income statement, but it affects working capital, the
current ratio, and the liquidity discussion in MD&A, and Regulation S-X Rule 5-02 requires the classification to
be right.

## 6.6 Contract-Level Recomputation

The roll-forward and the bridge establish that the aggregate movement is explained. They do not establish that
any individual balance is right. Contract-level recomputation does, and it is the test of details that carries
the accuracy assertion.

### 6.6.1 Defining the population and stratifying it

**Exhibit 6-7. Deferred revenue population at December 31, 2025 (in thousands).**

| Stratum | Definition | Contracts | Balance | % of balance | Testing approach |
| --- | --- | --- | --- | --- | --- |
| 1 | Individually significant: balance greater than performance materiality of $940 | 12 | 18,640 | 23.8% | 100% recomputation |
| 2 | Balance $250 to $940 | 96 | 41,120 | 52.6% | Sample of 25 |
| 3 | Balance below $250, enterprise and mid-market | 2,884 | 17,820 | 22.8% | Sample of 15 |
| 4 | Self-serve accounts billed monthly through Stripe | 11,400 | 620 | 0.8% | Population-level analytic; no sample |
| **Total** | | **14,392** | **78,200** | **100.0%** | |

Stratum 4 deserves a note. Eleven thousand four hundred accounts holding $620 in aggregate — an average of $54 in
whole dollars each — cannot be sampled usefully and do not need to be. Monthly billing in advance means each
account's liability is a fraction of one month's fee, so the entire stratum can be tested by recomputing the
expected balance from the account count, the average monthly fee, and the distribution of billing dates: 11,400
accounts × an average monthly fee of $44.60 in whole dollars × an average of 1.22 months unearned = $620. If the
recorded balance were $2,100, the arithmetic tells you immediately that something other than one month of
prepayment is sitting in the account.

### 6.6.2 What "recompute" means

For each selected contract, build the balance from the contract, not from the system:

1. Obtain the executed order form and all amendments.
2. Determine the performance obligations and the allocated transaction price for each (Chapter 5, §5.7).
3. Determine each obligation's service period and measure of progress.
4. Compute cumulative revenue that should have been recognized through December 31, 2025.
5. Obtain the invoice history from the Zuora Billing invoice register and total amounts invoiced through
   December 31, 2025.
6. Expected contract balance = cumulative invoicing less cumulative revenue. A positive result is a contract
   liability; a negative result is a contract asset (§6.8).
7. Compare to the recorded contract-level balance in RevPro and to the reclassified amount in the general ledger.

**Exhibit 6-8. Extract from the contract-level recomputation, five of the 52 contracts tested (in thousands).**

| Contract | Cumulative invoicing | Recomputed cumulative revenue | Recomputed balance | Recorded balance | Difference | Direction |
| --- | --- | --- | --- | --- | --- | --- |
| C-1 Meridian Health Systems | 960.000 | 956.352 | 3.648 | 3.648 | — | — |
| C-3 Northgate Financial Group | 1,920.000 | 960.000 | 960.000 | 960.000 | — | — |
| C-5 Pemberton Manufacturing | 720.000 | 240.000 | 480.000 | 480.000 | — | — |
| Halloran Energy | 1,080.000 | 540.000 | 540.000 | 540.000 | — | — |
| Aeropath Group (Q1 2025 contract) | 1,200.000 | 878.000 | 322.000 | 289.000 | 33.000 | DR understated |
| Calderon Foods (Q1 2025 contract) | 940.000 | 663.000 | 277.000 | 249.000 | 28.000 | DR understated |

C-1's $3.648 is carried forward from Chapter 5's walkthrough, Step 22. C-3's balance reflects a 12-month contract
beginning July 1, 2025 at $1,920 invoiced in full, six months earned. C-5's reflects the enforceable-term
conclusion in §6.11.3: a transaction price of $720 for the enforceable twelve months, four months earned.
Halloran's reflects the cumulative catch-up in Chapter 5, §5.8.1: a revised transaction price of $1,080, twelve of
twenty-four months earned, with $1,080 invoiced across two annual invoices.

### 6.6.3 Evaluating the differences

Two of the 52 contracts tested showed deferred revenue understated, by $33.000 and $28.000 — a total of $61.000,
both in the same direction. Both arose from the same cause: revenue began on the contractual start date rather
than on the later provisioning date, in contravention of AtlasFlow's own stated policy.

That is not two isolated differences; it is a pattern with a mechanical cause, and the correct response is to
define the population in which the cause can operate and test all of it. Brightline queried all Q1 2025 contracts
in which the provisioning date followed the contractual start date — 127 contracts — and identified 14 with
revenue recognized from the earlier date. The aggregate income effect was $410, and management recorded the
adjustment. It appears in the FY2025 file as corrected misstatement C-1.

Three further differences totaling a net $22 were identified in strata 2 and 3, arising from invoice-to-contract
mapping errors that offset. Projected across the untested portion of those strata the effect is approximately
$31, below the $72 clearly trivial threshold, and no further adjustment was proposed.

**What an unexpected result looks like.** Had the 127-contract query returned 90 exceptions rather than 14, the
$410 would have been something closer to $2,600, above overall materiality, and the conclusion would have been
that the revenue start-date control does not operate at all. The audit response would then be a full-population
recomputation of revenue start dates against provisioning records — feasible, since both populations are in
Snowflake — and a probable material weakness conclusion under Chapter 14, §14.9. The lesson is that a two-item
exception is a signal to define a population, not a signal to project a sample.

## 6.7 Testing That Amounts Released from Deferred Revenue Were Earned

The roll-forward releases $148,200 to revenue. Release for a subscription obligation is a function of elapsed
time and is straightforward to recompute. Release for an obligation satisfied by *delivery* — training sessions,
implementation milestones, data migration — depends on a fact about the world that no system knows unless someone
records it.

The three release mechanisms and the evidence that supports each:

| Release mechanism | Obligations it applies to | FY2025 amount released | Evidence that the amount was earned |
| --- | --- | --- | --- |
| Time elapsed | Core and Insight subscriptions | 131,600 | Service dates agreed to the order form and the platform provisioning log; the platform's availability record |
| As consumed | Usage overage above the committed volume | 4,200 | Platform event logs reconciled to the Zuora Billing usage records; see Chapter 5, §5.10 |
| Input measure (hours incurred ÷ estimated hours) | Fixed-fee professional services, including training sessions bundled into a fixed fee | 9,300 | Timesheet detail from the professional services application; signed attendance sheets and milestone acceptance certificates; the estimate's basis and its revisions |
| As delivered | Time-and-materials services and separately contracted training packages | 3,100 | Approved timesheets; signed session attendance sheets or the customer's written acknowledgment |

The amounts released by mechanism total $148,200 and tie to the roll-forward: $131,600 + $4,200 = $135,800 of
subscription revenue (Core $104,900, Insight $26,700, usage overage $4,200) and $9,300 + $3,100 = $12,400 of
professional services revenue. The professional services split of $9,300 fixed-fee and $3,100 time-and-materials
agrees to accounts 4200 and 4210.

The delivery-evidenced population is the one to work, because it is the only one where the fact that triggers
release is recorded by an AtlasFlow employee rather than computed. *For purposes of this illustration, assume*
AtlasFlow released $1,840 of deferred training revenue in FY2025 across 612 sessions, spanning both accounts 4200
and 4210. Brightline selected 25 sessions and requested, for each, the attendance sheet or the customer's written
acknowledgment.

**Exhibit 6-9. Results of the training-delivery test (25 sessions selected from 612).**

| Result | Sessions | Amount | Disposition |
| --- | --- | --- | --- |
| Signed customer attendance sheet obtained; date agrees to the delivery log | 19 | 58.4 | No exception |
| Internal trainer calendar entry only; no customer signature; delivery corroborated by customer inquiry | 4 | 12.1 | Alternative evidence obtained; no misstatement, evidence-quality observation noted |
| Session recorded as delivered in December 2025; trainer calendar shows delivery on January 6, 2026 | 1 | 3.2 | Cut-off misstatement of $3.2 |
| Session recorded as delivered; customer confirms it was cancelled and not rescheduled | 1 | 3.4 | Misstatement of $3.4; revenue released with no delivery |
| **Total selected** | **25** | **77.1** | **$6.6 of misstatement identified** |

Projection: $6.6 of misstatement in a sample of $77.1 from a population of $1,840 gives a projected misstatement
of $6.6 ÷ $77.1 × $1,840 = **$157**, which exceeds the $72 clearly trivial threshold and must be accumulated and
discussed with management. Two of 25 items — an 8% deviation rate on an attribute basis — also ends any reliance
on the control over the delivery log.

The two exceptions are different in kind and must be evaluated separately. The December-versus-January session is
a cut-off error: the revenue exists but belongs to FY2026. The cancelled session is revenue that does not exist at
all, and it is the more serious finding, because it means the delivery log records deliveries that did not occur.
Ask how a cancelled session comes to be marked delivered. If the answer is that the trainer marks the session
complete when the calendar entry passes, unattended, the control does not exist and the population is unreliable
rather than merely imprecise.

**What an unexpected result looks like.** If management cannot produce customer-signed evidence for a majority of
the sample, you have not found a misstatement — you have found that the population cannot be tested by inspection.
The response is to change the nature of the procedure: direct confirmation with a sample of customers as to
sessions received during FY2025, which is slow and imperfect but is evidence from outside the entity. Do not
substitute inquiry of the trainer for inspection; inquiry alone is never sufficient.

## 6.8 Contract Assets, Unbilled Receivables, and the Contract-Level Netting Rule

ASC 606-10-45 draws two distinctions that must both be applied, and they are frequently collapsed into one.

**Distinction 1 — receivable versus contract asset.** A **receivable** is an unconditional right to
consideration: nothing but the passage of time stands between the entity and payment. A **contract asset** is a
right to consideration that is conditional on something else — typically on the entity performing further, or on
a milestone being certified. The distinction matters because a receivable is subject to the credit-loss model in
its own right and a contract asset is subject to impairment considerations under ASC 606 and to credit-loss
measurement once recognized (Chapter 7, §7.8 owns this).

**Distinction 2 — netting is determined at the contract level.** A single contract has a single net position: it
is either a contract asset or a contract liability, never both. But positions on *different* contracts are not
netted, even with the same customer, unless the contracts are combined under ASC 606-10-25-9.

That second rule produces a gross-up that engagement teams routinely fail to test.

**Exhibit 6-10. Contract-level netting at December 31, 2025 (in thousands).**

| Component | Amount |
| --- | --- |
| Sum of contract-level positions that are net liabilities (14,241 contracts) | 78,200 |
| Sum of contract-level positions that are net assets (151 contracts) | (3,400) |
| **Net position across all contracts (not the reported presentation)** | **74,800** |
| Presented as deferred revenue (accounts 2400, 2405, 2410) | 78,200 |
| Presented as unbilled receivables and contract assets (account 1220) | 3,400 |

The reported balance sheet grosses the $74,800 net position back up to $78,200 of liability and $3,400 of asset,
because the netting is done contract by contract and then the two aggregates are presented separately. The
procedure is to obtain the contract-level balance file, confirm the count and the two sums, and confirm that no
contract appears in both aggregates. A contract appearing in both means the entity has netted at the *performance
obligation* level rather than at the contract level — which understates both the asset and the liability.

**Exhibit 6-11. Composition of contract assets and unbilled receivables at December 31, 2025 (in thousands).**

| Component | Amount | Receivable or contract asset? | Why |
| --- | --- | --- | --- |
| Fixed-fee professional services revenue recognized on the input measure ahead of milestone billing | 1,780 | Contract asset | The right to bill is conditional on reaching a contractual milestone |
| Ramped subscription contracts where cumulative straight-line revenue exceeds cumulative invoicing | 1,240 | Contract asset | The right to the next annual invoice is conditional on continued performance through the anniversary |
| Time-and-materials services delivered in December 2025 and invoiced in January 2026 | 380 | Receivable | The right is unconditional; only invoicing mechanics remain |
| **Total, account 1220** | **3,400** | | |

Two points about this exhibit. First, $380 of the $3,400 is properly a receivable rather than a contract asset,
and AtlasFlow presents the combined caption "Unbilled receivables / contract assets, current" on the balance
sheet. That combined presentation is common and is acceptable if the components are disclosed, but it must not
obscure the credit-loss analysis: the $380 receivable belongs in the CECL pool (Chapter 7, §7.9) and the $3,020
of contract assets require their own assessment. Second, the $1,240 of ramp-driven contract assets is the direct
consequence of Chapter 5, §5.9: recognizing the allocated total rather than the invoiced amount necessarily
creates this asset, and its absence on a population with 34% of ACV in ramped contracts would itself be the
exception.

**Reconcile the movement.** Contract assets rose from $2,100 to $3,400, an increase of $1,300, which is line 8 of
the billings bridge in Exhibit 6-4. That is the third place the same $1,300 appears — the roll-forward, the
bridge, and here — and all three must agree.

## 6.9 Deferred Revenue Acquired in a Business Combination

Before ASU 2021-08, contract assets and contract liabilities acquired in a business combination were measured at
fair value, which for deferred revenue usually meant the cost to fulfill the remaining obligation plus a normal
profit margin — a figure lower than the acquiree's book balance, producing the familiar "deferred revenue
haircut" and a step-down in post-acquisition revenue. ASU 2021-08 changed the answer. Contract assets and
contract liabilities acquired in a business combination are now measured **in accordance with ASC 606, as if the
acquirer had originated the contracts**. The amendment is effective for public business entities for fiscal years
beginning after December 15, 2022, so it is in force for AtlasFlow's FY2025 and for the August 4, 2025 Kestrel
Labs acquisition.

"As if the acquirer had originated the contracts" is not the same as "carry over the acquiree's balance." It means
apply ASC 606 to the acquired contracts and measure what the balance *should* be. Where the acquiree applied
ASC 606 correctly, the two are the same and carryover is the practical answer. Kestrel is the case where they are
not: Kestrel had no formal revenue recognition policy, kept its billing in a spreadsheet, and prepared its
historical financial statements on a modified cash basis.

**Exhibit 6-12. Recomputation of Kestrel Labs deferred revenue at August 4, 2025 (in thousands).**

| Component | Amount | Explanation |
| --- | --- | --- |
| Deferred revenue per Kestrel's billing spreadsheet at August 4, 2025 | 740 | Computed by Kestrel as one-twelfth of each annual invoice for each month remaining from the invoice date |
| Less: adjustment for invoices deferred from the invoice date rather than the service start date | (84) | 19 contracts where the invoice preceded the service start by 11 to 46 days; deferral began too early, overstating the liability |
| Less: amounts invoiced for services already delivered before the invoice date | (31) | 7 contracts billed in arrears and deferred as though billed in advance |
| Less: monthly contracts invoiced in arrears and recorded as deferred | (15) | 4 contracts where the amount was earned before it was billed; the correct balance is nil, with an unbilled receivable |
| **Deferred revenue measured under ASC 606, recorded in the purchase price allocation** | **610** | Agreed to the roll-forward in Exhibit 6-3 |

The $130 reduction is not a bargain-purchase adjustment or a measurement-period revision to goodwill in the
ordinary sense; it is the measurement of the acquired liability itself, and it flowed into the $200 of net working
capital acquired in the Kestrel purchase price allocation. For purposes of this illustration, the $200 comprises
receivables of $690, prepaid expenses of $80, cash of $180, accounts payable and accrued liabilities of $(140),
and deferred revenue of $(610), which sum to $200.

Three procedures follow, and the third is the one that gets missed.

1. **Recompute the acquired balance from the acquired contracts.** Sixty-one contracts is a testable population;
   test all of them, or test the largest 20 covering the majority of the balance and analytically corroborate the
   remainder. Do not accept a carryover of an unreliable balance because ASU 2021-08 permits carryover in
   principle.
2. **Test the post-acquisition revenue.** $340 of Kestrel revenue was recognized in the consolidated statements
   for the period from August 4 to December 31, 2025. Recompute it from the same 61 contracts and reconcile the
   acquired liability, post-acquisition billings, and post-acquisition revenue as a miniature roll-forward.
3. **Determine whether the acquired contracts are inside the ICFR scope.** Management scoped Kestrel out of its
   FY2025 Section 404(a) assessment. The exclusion, if properly supported and disclosed, covers Kestrel's
   *processes*. It does not follow that the acquired balances are outside the financial statement audit, and it
   does not follow that the exclusion still holds once Kestrel's contracts were migrated into Zuora in October
   2025 — after migration, those contracts are processed by AtlasFlow's own in-scope controls. That timing point
   is a recurring exercise in this textbook and is developed in Chapter 11, §11.11.

**What an unexpected result looks like.** If the recomputation had produced $980 rather than $610 — that is, if
Kestrel had *understated* its liability by $240 — the effect would be to reduce net working capital acquired and
increase goodwill, and to reduce post-acquisition revenue relative to what was recorded. A $240 error in
post-acquisition revenue is 16.6% of overall materiality and would require adjustment. The direction is not
predictable in advance, which is why the recomputation must actually be performed rather than reasoned about.

## 6.10 Foreign-Currency Deferred Revenue

AtlasFlow's UK entity (functional currency GBP) and Australian entity (functional currency AUD) both hold
deferred revenue, and the UK entity holds a contract denominated in a third currency: contract C-2 with Voltaire
Logistics S.A., invoiced in euros.

The rule that decides everything here is that **a contract liability is a non-monetary item.** ASC 830-10-45
distinguishes monetary items — those representing a fixed number of units of currency to be received or paid —
from non-monetary items. Deferred revenue will be settled by delivering service. It is therefore recorded at the
functional-currency amount determined on the transaction date and is **not remeasured** for later exchange rate
movements.

**Exhibit 6-13. Foreign currency effects on deferred revenue, FY2025 (in thousands).**

| Entity or contract | Component | Amount | Where it goes |
| --- | --- | --- | --- |
| AtlasFlow Software Ltd (UK) | Deferred revenue in GBP at 12/31/2025, translated at the closing rate of 1.2680 USD/GBP | 14,820 | Balance sheet at the closing rate |
| AtlasFlow Software Ltd (UK) | Translation effect on the opening and current-year GBP balances | (190) | Cumulative translation adjustment in accumulated other comprehensive loss (account 3200) |
| AtlasFlow Pty Ltd (Australia) | Deferred revenue in AUD at 12/31/2025, translated at the closing rate of 0.6410 USD/AUD | 5,640 | Balance sheet at the closing rate |
| AtlasFlow Pty Ltd (Australia) | Translation effect | (70) | Cumulative translation adjustment |
| | **Total translation effect on deferred revenue, per the roll-forward** | **(260)** | |
| Contract C-2 (EUR-denominated, held by the UK entity) | Contract liability at 12/31/2025 in GBP, measured at the October 1, 2025 inception rate | £489.0 | Not remeasured; non-monetary |
| Contract C-2 | Effect of remeasuring the liability at the 12/31/2025 EUR/GBP rate — an error, if recorded | £5.4 | Would create a fictitious £5.4 (approximately $6.8) loss |

The UK and Australian deferred revenue amounts, and the $(190) and $(70) split of the $(260), are extensions for
purposes of this illustration; the continuing case records only the $(260) total. The two components sum to the
$(260) in Exhibit 6-3.

Note the two distinct mechanisms and keep them separate in your documentation. **Translation** of the UK entity's
GBP-denominated deferred revenue into USD at the closing rate produces a difference that goes to other
comprehensive income and *is* the $(260) in the roll-forward. **Remeasurement** of a EUR-denominated liability
into the UK entity's GBP functional currency would produce an earnings item — and must not happen, because the
liability is non-monetary. Chapter 5, §5.12 develops the revenue-side measurement of C-2 and shows that only £7.0
of the £-measured movement on the EUR receivable is an earnings item.

**How to test it.** Two procedures, both quick and both frequently skipped:

1. **Obtain the account list used by the month-end FX revaluation job in NetSuite** and confirm that accounts
   2400, 2405, and 2410 are excluded. Revaluation jobs are configured by account range, and deferred revenue is
   a liability, so its inclusion is the default failure mode.
2. **Recompute one foreign-currency contract's liability from the inception rate.** For C-2: €740 invoiced,
   measured at the October 1, 2025 EUR/GBP rate of 0.8615 = £637.5; cumulative revenue for the 92 days from
   October 1 to December 31, 2025 = £148.5; liability = £489.0. Then agree £489.0 × 1.2680 = **$620.0** to the
   consolidated deferred revenue detail. If the recorded USD amount is $627 rather than $620, the £5.4
   remeasurement error has been recorded and you have found it with one calculation.

**What an unexpected result looks like.** A month-over-month movement in translated deferred revenue that
correlates with the exchange rate rather than with billings and revenue is the population-level tell. Regress the
monthly USD deferred revenue balance against the closing rate; a strong relationship after controlling for the
GBP balance indicates remeasurement is occurring somewhere. This is faster than reading the configuration and it
covers all currencies at once.

## 6.11 The Remaining Performance Obligation Disclosure

RPO is the aggregate amount of the transaction price allocated to performance obligations that are unsatisfied or
partially unsatisfied at the reporting date, together with an explanation of when the entity expects to recognize
it. AtlasFlow disclosed **$214,000** at December 31, 2025, of which **$138,900 (64.9%)** is expected to be
recognized within twelve months, against $168,500 and $110,100 at December 31, 2024.

Treat it as a recomputable population, because it is one. It is also the disclosure investors and analysts model
most closely, it is discussed in Item 7 of the Form 10-K, and it is the only place in the financial statements
where the enforceable term of every contract is implicitly asserted.

### 6.11.1 Recomputing the disclosure

**Exhibit 6-14. Recomputation of the RPO disclosure at December 31, 2025 (in thousands).**

| Line | Component | Amount |
| --- | --- | --- |
| 1 | Total contracted value of active subscription rate-plan charges per Zuora Billing (charge end date after 12/31/2025) | 356,000 |
| 2 | Less: cumulative subscription revenue recognized to date on those subscriptions | (144,960) |
| 3 | **Remaining contracted subscription amounts** | **211,040** |
| 4 | Less: non-enforceable amounts on 23 termination-for-convenience contracts (§6.11.3) | (1,860) |
| 5 | Less: usage-based overage consideration excluded under the practical expedient | (1,120) |
| 6 | Less: self-serve subscriptions with no enforceable term beyond the current month | (380) |
| 7 | Add: unsatisfied professional services performance obligations | 6,180 |
| 8 | Add: allocated amounts of unexercised material rights | 140 |
| 9 | **Remaining performance obligations per recomputation** | **214,000** |

Arithmetic: $211,040 − $1,860 − $1,120 − $380 + $6,180 + $140 = $214,000, which agrees to the disclosure.

The $6,180 of professional services obligations reconciles to the balance sheet: $4,500 has been billed and sits
in account 2405, and $1,680 is contracted and not yet billed. The $140 of material rights includes the $120.994
allocated to C-2's Insight credit (Chapter 5, §5.4.2) plus $19 across 213 smaller rights.

The disclosure must also reconcile to the deferred revenue balance, because deferred revenue is a subset of RPO:

**Exhibit 6-15. Reconciliation of RPO to deferred revenue at December 31, 2025 (in thousands).**

| Component | Amount |
| --- | --- |
| Deferred revenue included in RPO (billed and unearned on contracts with enforceable remaining terms) | 77,820 |
| Deferred revenue excluded from RPO (self-serve monthly subscriptions, no enforceable term beyond the current month) | 380 |
| **Total deferred revenue per the balance sheet** | **78,200** |
| Contracted amounts not yet billed and included in RPO | 136,180 |
| **Total remaining performance obligations** | **214,000** |

Arithmetic: $77,820 + $136,180 = $214,000, and $77,820 + $380 = $78,200. Of the disclosed RPO, 36.4% is on the
balance sheet and 63.6% is not — which is the single most useful sentence you can put in the file, because it
tells the reviewer that nearly two-thirds of the disclosed amount has no accounting entry behind it and can only
be tested against contracts.

**Exhibit 6-16. Expected timing of recognition of the $214,000 RPO.**

| Period of expected recognition | Amount | % of total |
| --- | --- | --- |
| Within 12 months | 138,900 | 64.9% |
| 13 to 24 months | 51,400 | 24.0% |
| 25 to 36 months | 19,300 | 9.0% |
| Beyond 36 months | 4,400 | 2.1% |
| **Total** | **214,000** | **100.0%** |

The $138,900 twelve-month portion and the $51,400 / $19,300 / $4,400 detail beyond it are consistent with a
population in which approximately 34% of ACV sits in multi-year contracts: a pure 12-month population would show
close to 100% in the first bucket.

### 6.11.2 The practical expedients and their disclosure consequences

ASC 606-10-50-14 through 50-15 permit two categories of exclusion, and require disclosure of which were used.

**The one-year expedient.** An entity need not disclose the RPO for performance obligations that are part of a
contract with an original expected duration of one year or less. **AtlasFlow did not elect it.** The consequence
is a much larger and more informative disclosure: had AtlasFlow excluded its 12-month contracts, the disclosed
amount would have fallen to a fraction of $214,000 and would have ceased to be comparable to its ARR. The cost is
that the population to be recomputed is the whole contract base, which is why the recomputation in Exhibit 6-14
starts from all active subscriptions. Where an entity *does* elect the expedient, you must test the *exclusion*:
a contract with an original expected duration of 13 months excluded from the disclosure is a disclosure error, and
"original expected duration" is measured at contract inception, not at the reporting date.

**The variable-consideration expedient.** An entity need not disclose amounts of variable consideration that are
a sales-based or usage-based royalty, or that are allocated entirely to a wholly unsatisfied performance
obligation or to a distinct good or service in a series that forms part of a single performance obligation.
AtlasFlow applies this to usage overage, excluding **$1,120** of estimated future overage. That exclusion is
correct, and it has a disclosure consequence: ASC 606-10-50-15 requires the entity to explain, qualitatively,
whether any consideration is not included in the transaction price and therefore not in the disclosed RPO. A
disclosure that excludes usage without saying so is incomplete, and it matters commercially, because a reader
comparing AtlasFlow's $214,000 RPO to a competitor that includes estimated usage is comparing different things.

**The self-serve exclusion is not an expedient.** The $380 excluded at line 6 of Exhibit 6-14 is excluded because
no enforceable right exists beyond the current month, not because an expedient was applied. Keep the two reasons
distinct in the disclosure and in your file; conflating them makes the disclosure wrong even where the amount is
right.

### 6.11.3 Contract-term judgments: the C-5 Pemberton analysis

Contract C-5 with Pemberton Manufacturing Co. is a 24-month term beginning September 1, 2025, $1,440 total, billed
annually in advance, with a clause allowing Pemberton to terminate for convenience on 30 days' notice with no
penalty. The contract term for ASC 606 purposes is the period over which enforceable rights and obligations exist
(ASC 606-10-25-1 through 25-3), and a termination right without penalty limits it.

**Practice varies, and here are the poles.**

*Pole 1 — the enforceable term is 30 days.* The customer can walk away at any time on 30 days' notice with no
consequence, so no enforceable obligation extends beyond the notice period. On this view the transaction price is
one month's fee, the contract is effectively month-to-month, and each month's continuation is a new contract.
RPO at December 31, 2025 would be approximately $60.

*Pole 2 — the enforceable term is the prepaid period.* Pemberton paid $720 in advance on September 1, 2025 and
the prepayment is non-refundable. A customer that terminates forfeits the unused portion, which is an economic
disincentive to terminate — a substantive termination penalty in substance, even though the contract calls it no
penalty. On this view the enforceable term runs through August 31, 2026, the transaction price is $720, and the
second year is not enforceable until invoiced.

*Pole 3 — the enforceable term is 24 months.* The parties signed a 24-month contract and the termination clause
is a commercial accommodation rarely exercised. This view is the weakest: it substitutes expected behavior for
enforceable rights, which is precisely the substitution ASC 606-10-25-3 forbids.

**Management's conclusion, and Brightline's, is Pole 2**, which is the prevailing view in practice where a
non-refundable prepayment covers a substantial period. The consequences:

| Item | Pole 1 (30 days) | Pole 2 (prepaid period) — as recorded | Pole 3 (24 months) |
| --- | --- | --- | --- |
| Transaction price at December 31, 2025 | 60.0 | 720.0 | 1,440.0 |
| FY2025 revenue (September 1 – December 31, 2025) | 240.0 | 240.0 | 240.0 |
| Deferred revenue at December 31, 2025 | 480.0 | 480.0 | 480.0 |
| RPO at December 31, 2025 | 60.0 | 480.0 | 1,200.0 |
| Amortization period for the $86 commission (ASC 340-40) | 4 years | 4 years | 4 years |

Two features of that table are worth stating explicitly because they are counterintuitive. **First, FY2025
revenue and deferred revenue are identical under all three views.** Pemberton has paid $720 for twelve months of
service and four months have elapsed, so $240 is earned and $480 is deferred regardless of how the enforceable
term is characterized — the cash is in and the service is being delivered. The contract-term conclusion changes
only the *disclosure*. That is why the RPO disclosure, not the income statement, is where the termination-clause
population must be tested.

**Second, the commission amortization period is 4 years under all three views.** The ASC 340-40 amortization
period is the expected period of benefit, which AtlasFlow supports with an average customer life of 4.3 years and
the fact that renewal commissions average 3.1% of ACV against 11.8% on new business and are therefore not
commensurate (case §4.2). Conflating the ASC 606 contract term with the ASC 340-40 benefit period is a common
error and would, here, also make the ASC 340-40-25-4 practical expedient appear available (amortization period of
one year or less, permitting immediate expense) when it is not. Chapter 10, §10.6 owns this.

## 6.12 Deferred Professional Services Revenue

Account 2405 holds $4,500 at December 31, 2025. It is 5.8% of the contract liability and it carries a
disproportionate share of the risk, because professional services revenue is released on estimates and on
delivery events rather than on the calendar.

**Exhibit 6-17. Composition of deferred professional services revenue at December 31, 2025 (in thousands).**

| Component | Cumulative billed | Cumulative revenue recognized | Deferred | Basis of recognition |
| --- | --- | --- | --- | --- |
| Fixed-fee implementations in progress (48 engagements) | 9,860 | 6,120 | 3,740 | Input measure: hours incurred ÷ estimated total hours |
| Training packages sold and not yet delivered (112 packages) | 640 | 190 | 450 | Sessions delivered ÷ sessions contracted |
| Milestone billings on 6 large engagements ahead of delivery | 1,020 | 710 | 310 | Input measure; billing is ahead of performance |
| **Total, account 2405** | **11,520** | **7,020** | **4,500** | |

Three tests carry this balance.

**Test 1 — the estimate of total hours.** The input measure's denominator is an estimate, and an estimate that is
too high defers revenue while an estimate that is too low accelerates it. Perform a retrospective review: for the
31 fixed-fee engagements completed during FY2025, compare the original estimated hours to actual hours. *For
purposes of this illustration, assume* actual hours exceeded original estimates by an average of 8.4%, with 22 of
31 engagements over-running. A consistent one-directional bias in the estimate produces a consistent
one-directional bias in revenue — here, revenue recognized too early, because the denominator was too small and
the percentage complete too high. Quantify it: if estimated total hours on the 48 in-progress fixed-fee engagements
are understated by 8.4%, the $6,120 of cumulative revenue recognized on them is overstated by
$6,120 × (1 − 1 ÷ 1.084) = **$474**, which is 50.4% of performance materiality and must be evaluated rather than
noted. Uncorrected misstatement U-4 in the FY2025 file ($95, contract asset understated) is the residue of this
analysis after management revised the estimates on the largest engagements.

**Test 2 — the disputed engagement.** Meridian Health Systems notified AtlasFlow on February 9, 2026 of a dispute
over a $1,240 professional services invoice. That is a subsequent event and Chapter 19, §19.8 owns the recognized
versus non-recognized determination. From this chapter's perspective the question is narrower: does the dispute
indicate that revenue released from deferred revenue in FY2025 was not earned? If the dispute concerns the
quality or completeness of work performed during 2025, the answer may be yes, and the correct treatment is a
reduction of the FY2025 transaction price for variable consideration rather than a FY2026 event. Read the dispute
correspondence; do not classify it by its date.

**Test 3 — the dormant engagements.** An engagement with deferred revenue and no recorded hours for six months is
either complete and unrecognized, cancelled, or stalled. Each has a different answer, and none of them is "leave
the balance." §6.14 quantifies AtlasFlow's dormant population at $620.

## 6.13 Customer Credits and Refund Liabilities

Account 2230 holds $1,200 at December 31, 2025. It is not a contract liability, and the distinction is not
cosmetic: a contract liability will be settled by delivering service and enters the RPO disclosure, whereas a
refund liability will be settled in cash and does not.

**Exhibit 6-18. Composition of customer credits and refunds payable, account 2230 (in thousands).**

| Component | Amount | Nature | In RPO? |
| --- | --- | --- | --- |
| Credit memos issued and approved, refundable in cash at the customer's election | 410 | Refund liability | No |
| Estimated refunds under the 30-day money-back provision on self-serve accounts | 180 | Refund liability (variable consideration) | No |
| Service-level agreement credits earned and accrued at December 31, 2025 (Northgate and six others) | 290 | Reduction of the transaction price, accrued as a liability | No |
| Termination refunds due on three contracts cancelled in December 2025 | 320 | Refund liability | No |
| **Total, account 2230** | **1,200** | | |

The $290 of SLA credits is corrected misstatement C-2 in the FY2025 file: credits had been earned but not accrued,
and management recorded the adjustment. The mechanism matters — an earned SLA credit is a reduction of the
transaction price, so the entry is a debit to revenue (through contra account 4900) and a credit to account 2230,
not a debit to an expense. Contract C-3 with Northgate is the illustration: two incidents in FY2025 triggered
credit eligibility, Northgate claimed $180 in December 2025, and AtlasFlow originally recorded nothing pending
"commercial discussions." "Pending commercial discussions" is not a measurement basis. Chapter 4, §4.9 owns the
variable-consideration analysis; the balance sheet consequence lands here.

**The classification test that catches the common error.** Ask, for each item: if the customer never buys anything
again, does AtlasFlow owe cash? If yes, it is a refund liability. If AtlasFlow instead owes future service, it is a
contract liability. Applying that question to AtlasFlow's population moved $680 of unapplied credits *out* of
account 2230 and into deferred revenue in prior years, because those credits are usable only against future
invoices for future service and lapse if unused. That $680 appears in the deferred revenue aging in §6.14 and is
correctly a contract liability.

**What an unexpected result looks like.** A refund liability that grows faster than revenue is a leading indicator
of customer dissatisfaction and of a churn problem that has not yet reached the retention metrics. Account 2230
rose from $940 to $1,200, an increase of 27.7% against revenue growth of 24.6% — directionally similar, so no
investigation is triggered. Had it risen to $2,400, the 155% increase would require you to test the completeness of
the accrual and to reconsider the credit-loss estimate and the retention disclosures in MD&A.

## 6.14 Deferred Revenue Analytics

Four analytics are worth running on this account. Each is useful; only one of them is capable of being a
substantive analytical procedure, and knowing which is which is the point of this section. AS 2305 requires that
an analytical procedure used as substantive evidence be based on an expectation precise enough to identify a
misstatement that, individually or aggregated, could be material.

**Exhibit 6-19. Deferred revenue analytics, FY2025 versus FY2024 (in thousands except ratios).**

| Metric | FY2025 | FY2024 | Change | Use |
| --- | --- | --- | --- | --- |
| Deferred revenue ÷ ARR | 78,200 ÷ 172,000 = 45.5% | 62,300 ÷ 137,400 = 45.3% | +0.2 pts | Risk assessment |
| Current subscription deferred revenue ÷ next year's planned subscription revenue | 66,800 ÷ 166,000 = 40.2% | 53,600 ÷ 135,800 = 39.5% | +0.7 pts | Risk assessment |
| Deferred revenue growth | 25.5% | — | — | Risk assessment |
| Total revenue growth | 24.6% | — | — | Comparison basis |
| Billings growth ($163,750 vs $131,400) | 24.6% | — | — | Comparison basis |
| ARR growth | 25.2% | — | — | Comparison basis |
| RPO growth ($214,000 vs $168,500) | 27.0% | — | — | Risk assessment |
| RPO expected within 12 months, as a percentage of RPO | 64.9% | 65.3% | (0.4) pts | Risk assessment and disclosure corroboration |

The FY2026 planned subscription revenue of $166,000, the FY2024 billings figure of $131,400, and the FY2023
opening deferred revenue balance of $49,800 from which it is derived are extensions for purposes of this
illustration.

### 6.14.1 Why the ratio analytics are risk assessment and not substantive evidence

Compute the precision. One percentage point of the deferred-revenue-to-ARR ratio is $1,720 — that is 119% of
overall materiality of $1,450 and 183% of performance materiality of $940. An analytic whose smallest meaningful
unit of measurement is larger than materiality cannot detect a material misstatement. Even a threshold of half a
point ($860) is only marginally below performance materiality, and the ratio is legitimately affected by
billing-timing mix, contract duration mix, and the acquisition, none of which you can hold constant.

The ratio's stability — 45.3% to 45.5% — is therefore genuinely useful information about whether something has
changed structurally, and it is genuinely incapable of substantiating the balance. Say both things in the file.
Writing "we performed a substantive analytical procedure over deferred revenue by comparing the
deferred-revenue-to-ARR ratio to the prior year and noted no significant fluctuation" claims evidence that has
not been obtained. The corresponding useful statement is: the ratio's stability, together with billings growth of
24.6% tracking revenue growth of 24.6%, is consistent with the absence of a structural change in billing terms,
and provides risk assessment evidence supporting the assessed level of inherent risk over completeness.

The billings bridge in §6.4 *is* capable of being substantive, because it is an identity reconciled to an
independent population (the invoice register) rather than a ratio compared to an expectation. Its precision is
limited only by the accuracy of the four populations it connects.

### 6.14.2 Aging of deferred revenue

This is the analytic that finds errors, and it takes twenty minutes.

**Exhibit 6-20. Aging of the deferred revenue balance at December 31, 2025 (in thousands).**

| Category | Amount | % of total | What it should be | Action |
| --- | --- | --- | --- | --- |
| Active subscriptions with a term end date after December 31, 2025 | 76,410 | 97.7% | The balance | None |
| Subscriptions whose term ended on or before December 31, 2025 | 490 | 0.6% | Nil | Investigate all 41 contracts |
| Professional services engagements with no recorded hours in the last 180 days | 620 | 0.8% | Nil, or supported by a documented delivery plan | Investigate all 17 engagements |
| Unapplied customer credits usable only against future service | 680 | 0.9% | A contract liability, correctly classified | Test the lapse terms and the expiry dates |
| **Total deferred revenue** | **78,200** | **100.0%** | | |

The $490 of deferred revenue on expired subscriptions is the highest-value line on the page. A liability to deliver
service on a contract whose term has ended is either revenue that should have been recognized, a renewal that was
mis-dated, or a credit that should have been refunded. All 41 contracts are testable. *For purposes of this
illustration, assume* the investigation found 33 contracts ($390) where the subscription had been renewed and the
renewal's start date had been entered one to three months late, so the balance was legitimate and the
*classification* by term end date was wrong; 6 contracts ($74) where revenue should have been recognized in
FY2025; and 2 contracts ($26) where the customer was owed a refund. The identified misstatement is $74 of
understated revenue and $26 of misclassification between accounts 2400 and 2230 — the first above the $72 clearly
trivial threshold and requiring accumulation.

The $620 of dormant professional services deferral tests the same way and is where a stalled implementation hides.
An engagement with billed-and-unearned revenue and no hours for six months should have either a documented
restart plan or a cancellation. If it has neither, the deferral has become a cookie jar: it can be released to
revenue in any future period with no external event, which is precisely the condition AS 2401 directs you to look
for.

**Query the aging directly rather than asking for it.**

```sql
SELECT c.contract_number,
       c.customer_name,
       c.subscription_term_end_date,
       SUM(b.deferred_balance)                                            AS deferred_balance,
       DATEDIFF('day', c.subscription_term_end_date, '2025-12-31')        AS days_past_term_end
FROM   revpro.contract_balance b
JOIN   revpro.revenue_contract c ON c.contract_id = b.contract_id
WHERE  b.balance_date              = '2025-12-31'
  AND  b.deferred_balance          > 0
  AND  c.subscription_term_end_date <= '2025-12-31'
GROUP BY 1, 2, 3
HAVING SUM(b.deferred_balance) > 0
ORDER BY deferred_balance DESC;
```

## Step-by-Step Walkthrough: Building and Testing the Deferred Revenue Roll-Forward and Recomputing the $214,000 RPO

Objective: substantiate the $78,200 contract liability at December 31, 2025 and independently recompute the
$214,000 RPO disclosure and its 64.9% twelve-month portion. Workpaper reference WP 6100-02. Performed by
Jae-won Park (staff) and Tara Iyer (data and analytics), reviewed by Omar Haddad (manager).

**Step 1.** Obtain the trial balance detail for accounts 2400, 2405, and 2410 at December 31, 2025 and agree the
total to the balance sheet. Amounts: $66,800 + $4,500 = $71,300 current and $6,900 noncurrent, totaling $78,200.
*What you compare it to:* the audited balance sheet and the FloQast reconciliation signed off by Jordan Pike.
*Conclusion supported:* the recorded balance is the balance you must substantiate. *If unexpected:* a difference
between the trial balance and the FloQast reconciliation means a post-reconciliation entry; obtain it and
determine who posted it, because weakness W-12 means entries below $250 have no evidence of independent review.

**Step 2.** Obtain the RevPro contract-level balance file at December 31, 2025 with fields
`contract_id`, `customer_name`, `contract_number`, `deferred_balance`, `contract_asset_balance`,
`subscription_term_start_date`, `subscription_term_end_date`, `cumulative_billed`, `cumulative_revenue`, and
`currency`. Confirm the record count (14,392 revenue contracts in total, of which 14,241 carry a net liability
position and 151 a net asset position) and that the sum of liability positions equals $78,200 and the sum of asset
positions equals $(3,400).
*If unexpected:* if the sums do not agree to the general ledger, obtain the reconciliation between the RevPro
subledger and NetSuite; the difference is either an unposted interface item (interface I-3) or a manual entry
posted directly to 2400, and the second is the one to test.

**Step 3.** Test the completeness and accuracy of the balance file as IPE. Three checks: reconcile the record
count to the Zuora Billing count of active subscriptions plus terminated subscriptions with a residual balance;
confirm that `cumulative_billed` in total agrees to cumulative invoicing per the Zuora Billing invoice register;
and confirm that `cumulative_revenue` in total agrees to inception-to-date revenue on those contracts. Document
each of the three numbers. Without this step every subsequent step rests on an untested spreadsheet.

**Step 4.** Build the roll-forward (Exhibit 6-3) and prove it foots: $62,300 + $163,750 − $54,900 − $93,300 +
$610 − $260 = $78,200. Agree the opening balance of $62,300 to the FY2024 audited balance sheet ($56,900 +
$5,400).

**Step 5.** Substantiate the two revenue-release lines independently. Filter the RevPro revenue-schedule detail
for FY2025 recognized revenue by the date of the funding invoice: lines funded by pre-2025 invoices total
$54,900; lines funded by FY2025 invoices total $93,300. Prove that the two sum to $148,200, equal to total revenue
per the statement of operations. *Conclusion supported:* every dollar of FY2025 revenue passed through the
contract liability, so the roll-forward is complete with respect to revenue. *If unexpected:* if the two lines sum
to less than $148,200, some revenue bypassed deferred revenue; identify the entries and determine whether they
were manual (weakness W-12) and whether they had support.

**Step 6.** Agree the $54,900 to the revenue footnote's ASC 606-10-50-8 disclosure of revenue recognized from the
opening contract liability. Cross-foot the plausibility: $54,900 ÷ $62,300 = 88.1% of the opening balance was
earned during FY2025, leaving $7,400, which is consistent with the $6,900 noncurrent closing balance plus
long-dated current amounts.

**Step 7.** Build the billings bridge (Exhibit 6-4) from revenue and the change in deferred revenue and derive
total invoicing of $162,450. Run the invoice-register query in §6.4 and agree the result: gross invoiced $166,290,
credit memos $3,840, net $162,450, 158,412 documents. *If unexpected:* a difference here is one of four things
(§6.4) and must be resolved, not noted.

**Step 8.** Extend the bridge to cash (Exhibit 6-5) and derive cash collected from customers of $153,010. Agree it
to customer receipts posted through the bank feed (interface I-9) and the Stripe daily journal (interface I-4),
excluding interest income of $5,110 posted to account 7100.

**Step 9.** Substantiate the $610 of Kestrel acquired deferred revenue by recomputing it from the 61 acquired
contracts (Exhibit 6-12). Agree the $610 to the purchase price allocation's $200 of net working capital acquired
and to the roll-forward.

**Step 10.** Substantiate the $(260) of foreign currency translation (Exhibit 6-13) from the translation tab of
CONSOL_FY25_v14.xlsx, and separately obtain the NetSuite month-end FX revaluation job's account list to confirm
accounts 2400, 2405, and 2410 are excluded. Recompute contract C-2's liability from the inception rate: €740 at
0.8615 = £637.5, less £148.5 of revenue for 92 days, equals £489.0, translated at 1.2680 = $620.0.

**Step 11.** Recompute the current and noncurrent split. Run the query in §6.5 and confirm the quarterly amounts
$27,600 / $20,700 / $13,600 / $9,400 summing to $71,300 current, and $5,600 + $1,300 = $6,900 noncurrent. Test the
extract by confirming that all scheduled revenue funded by invoices issued through December 31, 2025 sums to
$78,200. *If unexpected:* if the noncurrent balance was computed as a percentage of the total, recompute it
yourself and treat management's figure as an estimate.

**Step 12.** Stratify the population (Exhibit 6-7) and select the sample: 12 individually significant contracts at
100%, 25 from stratum 2, 15 from stratum 3, and a population-level recomputation of stratum 4. Document the
selection method for strata 2 and 3 — systematic selection with a random start over the balance-sorted file —
and cross-reference the sample size determination to Chapter 15, §15.7.

**Step 13.** Recompute each selected contract's balance from the contract document, following the seven steps in
§6.6.2. Record cumulative invoicing, recomputed cumulative revenue, the recomputed balance, the recorded balance,
and the direction of any difference (Exhibit 6-8).

**Step 14.** Evaluate the differences by direction and cause, not by size. Two contracts showed deferred revenue
understated by $33.000 and $28.000 with the same cause — revenue recognized from the contractual start date rather
than the later provisioning date. Define the population in which the cause can operate (Q1 2025 contracts where
provisioning followed the contract start date: 127 contracts) and test all of it. Result: 14 contracts, $410
income effect, recorded by management as corrected misstatement C-1.

**Step 15.** Test the release of delivery-based obligations. Select 25 training sessions from the 612 delivered in
FY2025 and obtain the signed attendance sheet or written customer acknowledgment for each (Exhibit 6-9). Result:
two exceptions, $6.6 of misstatement in a $77.1 sample, projected to $157 across the $1,840 population. Accumulate
$157 on the summary of audit differences and end reliance on the delivery-log control.

**Step 16.** Age the balance (Exhibit 6-20). Run the aging query in §6.14.2. Investigate all 41 contracts with a
positive balance and a term end date on or before December 31, 2025 ($490) and all 17 dormant professional services
engagements ($620). Result: $74 of revenue that should have been recognized in FY2025 and $26 of misclassification
between accounts 2400 and 2230.

**Step 17.** Test the contract-level netting (Exhibit 6-10). Confirm that no `contract_id` appears in both the
liability and the asset aggregate, that the two aggregates sum to the net $74,800, and that the balance sheet
presents $78,200 and $3,400 rather than the net. Then decompose the $3,400 (Exhibit 6-11) and confirm the $380 of
unconditional amounts is included in the credit-loss pool tested in Chapter 7.

**Step 18.** Move to the RPO. Obtain management's RPO computation and the query behind it. Confirm which practical
expedients were elected: the one-year expedient was not elected; the variable-consideration expedient was applied
to $1,120 of estimated usage overage. Read the draft footnote and confirm it discloses the expedient applied and
the qualitative information about excluded consideration required by ASC 606-10-50-15.

**Step 19.** Recompute the RPO from the contract population (Exhibit 6-14). Start from total contracted value on
active subscription rate-plan charges of $356,000; deduct cumulative revenue recognized on those subscriptions of
$144,960 to reach remaining contracted subscription amounts of $211,040; deduct $1,860 of non-enforceable amounts,
$1,120 of usage consideration, and $380 of self-serve amounts; add $6,180 of unsatisfied professional services
obligations and $140 of unexercised material rights. Result: $214,000.

**Step 20.** Reconcile the RPO to the balance sheet (Exhibit 6-15). Deferred revenue included in RPO $77,820 plus
deferred revenue excluded from RPO $380 equals the $78,200 balance; $77,820 plus $136,180 of unbilled contracted
amounts equals $214,000. Document that 63.6% of the disclosed figure has no corresponding accounting entry, which
sets the extent of contract-level testing required.

**Step 21.** Recompute the twelve-month portion. Sum the recomputed contract-level revenue schedules by expected
recognition period (Exhibit 6-16): $138,900 within twelve months, $51,400 in months 13 to 24, $19,300 in months 25
to 36, and $4,400 beyond, totaling $214,000. Compute the percentage: $138,900 ÷ $214,000 = 64.906%, disclosed as
64.9%. Agree the prior-year comparatives of $168,500 and $110,100 (65.3%) to the FY2024 file.

**Step 22.** Test the enforceable-term population, which is the step that produced the case study below. Query all
active contracts containing a termination-for-convenience clause, reconcile the query's contract count to the
legal department's clause register, and recompute the enforceable remaining amount for each. Result: 23 contracts
with $4,120 of remaining contracted amounts included in management's draft computation against $2,260 of
enforceable amounts — an overstatement of $1,860.

**Step 23.** Evaluate the disclosure as a whole under AS 2810. Confirm the footnote states the aggregate amount,
the expected timing, the expedient elected, and the qualitative explanation of excluded consideration; confirm the
MD&A discussion of RPO growth of 27.0% is consistent with the footnote and with billings growth of 24.6%; and
confirm that the RPO figure in the Item 7 discussion equals the figure in the footnote. A mismatch between the two
is an "other information" matter under AS 2710 and is a surprisingly common finding.

**Step 24.** Conclude. Document the aggregate misstatements identified ($157 projected on training delivery, $74 on
expired-term deferrals, and the $410 corrected by management), the deficiencies identified (the delivery-log
control and the RPO enforceable-term omission), and the sufficiency conclusion, cross-referencing the roll-forward,
the bridge, the contract-level testing, the aging, and the RPO recomputation as the five procedures that together
support the completeness assertion.

## Extended Case Study: An $1,860 Overstatement of the RPO Disclosure

### Background

AtlasFlow's remaining performance obligation disclosure is the operating metric most closely read by the analysts
who cover the stock, and management's Q4 2025 earnings materials led with RPO growth. Management prepared the
FY2025 disclosure using a Snowflake query written in January 2026 by the RevOps team against the RevOps datamart
— the same datamart identified in weakness W-11 as unreconciled to the general ledger for the first three quarters
of FY2025. The query summed remaining contracted value across all active subscription rate-plan charges. It
contained no filter for termination provisions.

### The Facts

- Management's draft footnote disclosed RPO of **$215,860** at December 31, 2025, of which **$139,700 (64.7%)** was
  expected to be recognized within twelve months.
- Twenty-three active contracts contain a clause permitting the customer to terminate for convenience on 30 days'
  notice with no penalty other than forfeiture of any unused prepayment. Contract C-5 with Pemberton Manufacturing
  Co. is one of them.
- On each of those 23 contracts, only the currently billed and prepaid period is supported by enforceable rights
  and obligations. Amounts relating to periods beyond the prepaid period are not enforceable and were nevertheless
  included in the draft computation.
- The FY2024 disclosure had been prepared by the corporate accounting team using a manually maintained contract
  schedule that did include a termination-clause filter. The FY2025 disclosure was the first prepared from the
  datamart.
- No contract in the 23 has a balance above performance materiality of $940. The largest, Pemberton, contributed
  $1,200 to the draft computation.

### What the Engagement Team Did

1. Requested the query behind management's RPO computation, read it, and observed that it contained no
   termination-provision logic.
2. Obtained the legal department's contract clause register and identified all active contracts flagged as
   containing a termination-for-convenience provision: 26 contracts. Reconciled that count to a full-text search of
   the Salesforce contract repository for the phrase "terminate for convenience" and its common variants, which
   returned 31 contracts.
3. Read all 31 clauses. Five imposed a termination penalty equal to 50% of the remaining contract value, which is
   a substantive penalty, so the enforceable term for those five is the full contract term and no adjustment is
   required. Three had expired or been superseded by an amendment removing the clause. Twenty-three had no penalty
   other than forfeiture of any unused prepayment.
4. For each of the 23, determined the currently billed and prepaid period from the Zuora Billing invoice register
   and recomputed the enforceable remaining amount at December 31, 2025.
5. Determined how much of the excess fell within twelve months of the balance sheet date, in order to correct the
   maturity table as well as the total.
6. Evaluated whether the omission of the filter is a control deficiency, and its severity.

### Analysis

**Exhibit 6-21. Recomputation of the enforceable remaining amount on the 23 termination-for-convenience contracts
(in thousands).**

| Contract | Remaining contracted amount included in the draft RPO | Enforceable remaining amount | Excess included | Prepaid period ends |
| --- | --- | --- | --- | --- |
| C-5 Pemberton Manufacturing Co. | 1,200 | 480 | 720 | Aug 31, 2026 |
| Halcyon Freight Systems | 640 | 320 | 320 | Jun 30, 2026 |
| Arbor Point Health Partners | 520 | 260 | 260 | Sep 30, 2026 |
| Westmark Utilities | 480 | 240 | 240 | Apr 30, 2026 |
| 19 other contracts, none individually above $160 | 1,280 | 960 | 320 | Various, Feb 2026 – Nov 2026 |
| **Total** | **4,120** | **2,260** | **1,860** | |

The columns foot: $1,200 + $640 + $520 + $480 + $1,280 = $4,120; $480 + $320 + $260 + $240 + $960 = $2,260;
$720 + $320 + $260 + $240 + $320 = $1,860; and $4,120 − $2,260 = $1,860.

Pemberton is the arithmetic in miniature. The contract is 24 months from September 1, 2025 at $1,440 total, billed
annually in advance. The year-1 invoice of $720 was issued September 1, 2025 and four months had been earned by
December 31, 2025, leaving $480 of enforceable remaining amount through August 31, 2026. The draft computation
included $1,440 − $240 = $1,200, picking up the entire second year, which Pemberton has no enforceable obligation
to pay and can avoid by giving 30 days' notice at any point before September 1, 2026.

**Correcting the maturity table.** The excess amounts are not evenly distributed across the buckets, because they
all relate to periods *after* the prepaid period ends. Only the portion of a post-prepaid period falling before
December 31, 2026 belongs in the twelve-month bucket.

**Exhibit 6-22. Allocation of the $1,860 excess between maturity buckets (in thousands).**

| Contract | Excess included | Prepaid period ends | Monthly rate of the excess period | Within 12 months | Beyond 12 months |
| --- | --- | --- | --- | --- | --- |
| C-5 Pemberton Manufacturing Co. | 720 | Aug 31, 2026 | 60.000 | 240 | 480 |
| Halcyon Freight Systems | 320 | Jun 30, 2026 | 26.667 | 160 | 160 |
| Arbor Point Health Partners | 260 | Sep 30, 2026 | 21.667 | 65 | 195 |
| Westmark Utilities | 240 | Apr 30, 2026 | 20.000 | 160 | 80 |
| 19 other contracts, weighted | 320 | Feb 2026 – Nov 2026 | various | 175 | 145 |
| **Total** | **1,860** | | | **800** | **1,060** |

Pemberton's $240 is the four months from September 1 to December 31, 2026 at $60 per month; Halcyon's $160 is the
six months from July 1 to December 31, 2026 at $26.667 per month; Arbor Point's $65 is three months at $21.667;
Westmark's $160 is eight months at $20. The columns foot: $240 + $160 + $65 + $160 + $175 = $800 and
$480 + $160 + $195 + $80 + $145 = $1,060, summing to $1,860.

**Exhibit 6-23. Effect on the disclosure (in thousands).**

| Line | As drafted by management | Adjustment | As corrected and filed |
| --- | --- | --- | --- |
| Remaining performance obligations | 215,860 | (1,860) | 214,000 |
| Expected to be recognized within 12 months | 139,700 | (800) | 138,900 |
| Expected to be recognized after 12 months | 76,160 | (1,060) | 75,100 |
| Twelve-month portion as a percentage of the total | 64.7% | | 64.9% |

The columns foot: $139,700 + $76,160 = $215,860 and $138,900 + $75,100 = $214,000; $(800) + $(1,060) = $(1,860).
The percentages: $139,700 ÷ $215,860 = 64.72%, and $138,900 ÷ $214,000 = 64.91%. Removing amounts that were
disproportionately long-dated *raises* the twelve-month percentage, which is a useful reminder that a correction
can improve a metric management is judged on and still be a correction.

**Materiality and its limits.** The $1,860 overstatement is 128% of overall materiality of $1,450 and 198% of
performance materiality of $940, so on its face it is quantitatively material. But it is a disclosure of an amount
that appears nowhere in the primary statements: no asset, no liability, no revenue, and no cash flow is affected,
and the deferred revenue balance of $78,200 is correct under all three contract-term views (§6.11.3). Materiality
for a disclosure of this kind is assessed against the disclosure itself and against the decisions of users who rely
on it. Here the analysis is straightforward: 0.87% of the disclosed RPO is a small relative error, but the
disclosure is a specific, quantified, forward-looking figure that investors use to model revenue, and it asserts
enforceability. A figure that includes amounts the company cannot enforce misstates the disclosure's substance,
not merely its magnitude. Brightline concluded the adjustment was required and management recorded it.

### Resolution and Conclusion

Management corrected the disclosure before filing. The Form 10-K filed February 20, 2026 discloses RPO of $214,000
with a twelve-month portion of $138,900, or 64.9%, which are the figures in the continuing case.

The engagement team evaluated the control implications separately. The control as described by management is a
review of the RPO computation by the Chief Accounting Officer against the prior-period computation and against
underlying contract data. The control did not detect the omission of the termination-clause filter, because the
review compared the FY2025 output to the FY2024 output at an aggregate level — RPO growth of 28.1% as drafted
against 27.0% as corrected, a difference no aggregate review would surface — and did not re-perform the query
logic. The deficiency was evaluated as follows: the control is a management review control whose precision is
insufficient to detect a misstatement of the magnitude that occurred; the misstatement that did occur exceeded
overall materiality; the deficiency arose in the first period in which the computation was produced from an
unreconciled data source (weakness W-11). Under Chapter 14's severity framework the engagement team concluded a
**significant deficiency**, aggregated with the other observations relating to the RevOps datamart, and reported
it in writing to the audit committee. It was not concluded to be a material weakness in isolation, on the grounds
that the disclosure does not affect the primary statements and that the compensating detective control — the
disclosure checklist and the external counsel review of the Form 10-K — operated, albeit after the auditor raised
the matter. Chapter 14, §14.11 examines whether "the auditor found it" undermines the compensating-control
argument; the honest answer is that it substantially does, and the conclusion here was a close one.

### Workpaper Extract

```text
================================================================================
BRIGHTLINE LLP                                              WP REF:  6300-07
AtlasFlow, Inc.                                             PERIOD:  FY2025
Audit of the financial statements and of ICFR                YEAR END: 12/31/2025
--------------------------------------------------------------------------------
SUBJECT:  Recomputation of the remaining performance obligation (RPO)
          disclosure and evaluation of the enforceable contract term on
          contracts containing a termination-for-convenience provision

PREPARED BY:  J. Park (JWP)            DATE PREPARED:  01/22/2026
              T. Iyer (TRI)                            01/23/2026
REVIEWED BY:  O. Haddad (OMH)          DATE REVIEWED:  01/29/2026
              G. Lindqvist (GRL)                       02/03/2026
PARTNER:      D. Whitcombe (DGW)                       02/09/2026
EQR:          L. Herrera (LXH)                         02/17/2026
--------------------------------------------------------------------------------
PURPOSE
To recompute the RPO disclosure required by ASC 606-10-50-13 at December 31,
2025 from the underlying contract population, to evaluate the enforceable
contract term for contracts containing a termination-for-convenience provision,
and to conclude on the presentation and disclosure assertion for the revenue
footnote and the related Item 7 discussion.

SOURCE OF INFORMATION
(1) Management's RPO computation and the supporting Snowflake query
    RPO_FY25_V3.sql, obtained 01/15/2026 from D. Kim.                        (a)
(2) Zuora Billing active subscription and rate-plan charge extract at
    12/31/2025; record count 14,392 enterprise and mid-market contracts plus
    11,400 self-serve accounts.                                              (b)
(3) RevPro contract-level revenue schedules at 12/31/2025.                    (b)
(4) Legal department contract clause register at 12/31/2025 (26 contracts
    flagged) and full-text search of the Salesforce contract repository
    (31 contracts returned).                                                 (c)
(5) All 31 executed contracts containing termination language, read in full.
(6) Zuora Billing invoice register for FY2025, net invoicing $162,450.        (b)
(7) Draft Form 10-K revenue footnote and Item 7, version dated 01/30/2026.

PROCEDURES PERFORMED
1. Read management's query. Confirmed it summed remaining contracted value on
   active rate-plan charges with no filter for termination provisions.        (d)
2. Recomputed RPO independently from the contract population:
       Total contracted value, active subscription charges        356,000
       Less cumulative revenue recognized on those charges      (144,960)
       Remaining contracted subscription amounts                 211,040
       Less non-enforceable amounts, 23 TFC contracts             (1,860)    (d)
       Less usage consideration under the practical expedient     (1,120)
       Less self-serve amounts with no enforceable term             (380)
       Add unsatisfied professional services obligations           6,180
       Add allocated amounts of unexercised material rights          140
       RPO per recomputation                                     214,000
3. Reconciled RPO to the balance sheet: deferred revenue in RPO 77,820 plus
   deferred revenue excluded from RPO 380 = 78,200 per the balance sheet;
   77,820 + 136,180 unbilled = 214,000.
4. Identified the population of contracts containing a termination-for-
   convenience provision by two independent methods (clause register: 26;
   full-text search: 31) and read all 31 clauses. 5 contained a substantive
   penalty (50% of remaining value); 3 were expired or superseded; 23 had no
   penalty other than forfeiture of an unused prepayment.                    (c)
5. Recomputed the enforceable remaining amount for each of the 23 from the
   prepaid period per the invoice register. Excess included in management's
   draft: 1,860.                                                            (d)
6. Allocated the 1,860 between maturity buckets: 800 within 12 months and
   1,060 beyond, and recomputed the corrected maturity table.
7. Recomputed the 12-month percentage: 138,900 / 214,000 = 64.906%.
8. Agreed the corrected figures to the revenue footnote and to the Item 7
   discussion in the Form 10-K as filed 02/20/2026.

RESULTS
- Management's draft RPO of 215,860 was overstated by 1,860 (0.87% of the
  disclosed amount; 128% of overall materiality of 1,450).                  (d)
- The 12-month portion of 139,700 was overstated by 800; the corrected
  percentage is 64.9% rather than 64.7%.
- Management corrected the disclosure to 214,000 / 138,900 before filing.
- The clause register was incomplete: 31 contracts contain termination
  language against 26 flagged in the register.                              (c)
- Control deficiency: the CAO's review of the RPO computation compared the
  aggregate output to the prior period and did not re-perform the query
  logic; the review's precision is insufficient to detect a misstatement of
  the magnitude identified. Evaluated as a significant deficiency at
  WP 8400-05 and aggregated with the RevOps datamart observations (W-11).   (d)

CONCLUSION
Following management's correction, the RPO disclosure of 214,000 at
December 31, 2025, and the disclosed expectation that 138,900 (64.9%) will be
recognized within twelve months, are consistent with the underlying contract
population and with ASC 606-10-50-13 through 50-15. The practical expedient
applied to usage-based consideration is disclosed. The presentation and
disclosure assertion for contract balances and remaining performance
obligations is supported. The related control deficiency is reported at
WP 8400-05 and was communicated to the audit committee on 02/13/2026.

TICK MARK LEGEND
(a) Obtained from management; query logic read and re-performed.
(b) Completeness and accuracy of the extract tested at WP 1800-06.
(c) Population completeness tested by a second independent method; exception
    noted.
(d) Exception or misstatement identified; see RESULTS.
================================================================================
```

### Lessons

1. **A disclosure computed by a query is a control, and the query is the control's operation.** Reviewing the
   output tells you nothing about the logic. Ask for the SQL and read it.
2. **Establish a clause population two ways.** The legal register held 26 contracts and a full-text search found
   31. Neither is authoritative alone, and the five contracts the register missed included four of the 23 that
   mattered.
3. **A correction can improve the metric.** The twelve-month percentage rose from 64.7% to 64.9%. Do not assume
   management will resist an adjustment, and do not assume an adjustment that helps management is therefore
   uncontroversial.
4. **Enforceability is asserted by the disclosure even though it is not asserted by the balance sheet.** Deferred
   revenue on Pemberton is $480 under every contract-term view; RPO is $60, $480, or $1,200 depending on the view.
   The place to test a contract-term judgment is the disclosure.
5. **The precision of a management review control is testable and is usually where these failures live.** RPO
   growth of 28.1% as drafted against 27.0% as corrected is a 1.1-point difference; no review conducted at that
   level of aggregation could have caught $1,860.

## Common Mistakes

### Mistake 6.1 — Auditing deferred revenue for existence instead of completeness

**What it looks like.** The workpaper program for account 2400 consists of a selection of 40 contract-level
balances from the deferred revenue detail, agreed to invoices and to the RevPro schedule, with a conclusion that
"deferred revenue is fairly stated." Every item selected exists, agrees, and is correctly measured.

**Why it happens.** Sampling from a listing is the default habit for every other balance sheet account, and for
assets it is the right habit. The auditor's mental model — "select from the population and vouch it" — is imported
into a liability without asking which direction the risk runs.

**What goes wrong.** Selecting from the recorded population cannot detect an amount that is not in the recorded
population. If a contract was invoiced and the entire invoice was credited to revenue, that contract never appears
in the deferred revenue detail, so it has a zero probability of selection no matter how large the sample. The
overstatement of revenue and the understatement of the liability are invisible to the procedure performed.

**How to avoid it.** Drive the population from the other side. Start from the Zuora Billing invoice register and
the Salesforce order population, not from the deferred revenue detail; reconcile the roll-forward's billings line
of $163,750 to an independently derived invoice total (§6.4); recompute RPO from the contract population and tie
the $77,820 of RPO represented by billed amounts back to the balance sheet (§6.11.1). At least one procedure on
this account must have a population that includes contracts with a recorded balance of nil.

### Mistake 6.2 — Accepting a roll-forward in which billings are a plug

**What it looks like.** The roll-forward foots perfectly. Opening balance, plus billings, less revenue, equals the
closing balance. It has always footed, in every year of the engagement's history.

**Why it happens.** Management computes the billings line as closing balance less opening balance plus revenue
recognized, because that is the fastest way to produce a schedule that agrees to the general ledger. The auditor
runs the footing check, it passes, and the check feels like evidence.

**What goes wrong.** A derived billings line cannot fail to foot, so the footing check has zero diagnostic power.
Any error in the closing balance, in revenue, or in the opening balance simply reappears in the billings line, and
the roll-forward reports a self-consistent set of wrong numbers.

**How to avoid it.** Ask for the invoice register total before you ask for the roll-forward, and independently
derive billings from Zuora Billing: gross invoiced $166,290 less credit memos $3,840 equals net invoicing
$162,450, plus the $1,300 increase in contract assets, equals $163,750. If management cannot produce a register
total that agrees, the billings line is a plug and you should document that fact and source the line yourself.

### Mistake 6.3 — Computing the ASC 606-10-50-8 disclosure as the opening balance less the closing balance

**What it looks like.** The revenue footnote discloses "revenue recognized in the period from amounts included in
the contract liability at the beginning of the period" as $62,300 — the entire opening balance — or as
$62,300 − $78,200, which is negative, or as some other subtraction of two balances.

**Why it happens.** The disclosure is worded in a way that invites subtraction, and the correct figure requires
filtering revenue-schedule detail by the date of the funding invoice, which most reporting packages do not do out
of the box.

**What goes wrong.** The disclosure is wrong, and it is wrong in a direction that overstates how much of the
opening liability was earned, which flatters the apparent velocity of revenue conversion. At AtlasFlow the correct
figure is $54,900 of the $62,300 opening balance, leaving $7,400 of the opening balance still deferred at year end.
Disclosing $62,300 would assert full conversion and would be inconsistent with the $6,900 noncurrent balance.

**How to avoid it.** Recompute it from the subledger by filtering RevPro revenue-schedule lines to those whose
funding invoice predates January 1, 2025, and sum. Then sanity-check the implied conversion rate:
$54,900 ÷ $62,300 = 88.1%, which is what a population of annual-in-advance contracts should produce. A rate at or
near 100% on such a population, or above it, is arithmetically impossible and is the tell.

### Mistake 6.4 — Splitting current and noncurrent by contract term rather than by scheduled release date

**What it looks like.** A schedule that classifies the deferred revenue on every contract with a remaining term
beyond twelve months as noncurrent. C-1 Meridian, with 24 months remaining on a 36-month term, contributes its
entire balance to the noncurrent caption.

**Why it happens.** Contract term is a field in Salesforce and Zuora; scheduled release month requires the revenue
schedule. The available field is used because it is available.

**What goes wrong.** The classification is wrong whenever billing frequency differs from contract term, which in a
SaaS population is most of the time. C-1 is billed annually in advance, so at December 31, 2025 only nine months of
the first annual invoice remain deferred and the entire balance is current. Using contract term would move that
balance to noncurrent, understating the current liability, overstating working capital, and distorting every
current-ratio-based covenant computation and analyst model.

**How to avoid it.** Recompute the split from the RevPro revenue schedule aggregated by scheduled recognition
month, restricted to amounts funded by invoices already issued (§6.5). AtlasFlow's $71,300 current and $6,900
noncurrent came from summing scheduled release by quarter — $27,600, $20,700, $13,600, $9,400 for 2026 — and the
declining 4 : 3 : 2 : 1 shape of that series is itself corroborating evidence.

### Mistake 6.5 — Netting contract assets against contract liabilities at the customer or performance-obligation level

**What it looks like.** The balance sheet shows deferred revenue of $74,800 and no contract asset caption, or a
contract asset of $3,400 netted against the deferred revenue of a different contract with the same customer.

**Why it happens.** The reporting package aggregates by customer account rather than by revenue contract, and the
netting rule in ASC 606-10-45 is read as a general offsetting rule rather than as a contract-level rule.

**What goes wrong.** Both the asset and the liability are understated — at AtlasFlow by $3,400 each — and the
credit-loss analysis over the $380 of unconditional unbilled receivable inside that $3,400 is never performed
because the receivable has disappeared into a liability caption.

**How to avoid it.** Obtain the contract-level balance file, confirm that the 14,241 net-liability positions sum to
$78,200 and the 151 net-asset positions to $3,400, and confirm that no contract identifier appears in both
aggregates. A contract in both aggregates means the netting is happening at the performance-obligation level, which
is wrong in the opposite direction.

### Mistake 6.6 — Carrying over an acquiree's deferred revenue balance because ASU 2021-08 permits carryover

**What it looks like.** The purchase price allocation records Kestrel Labs deferred revenue at the $740 shown in
Kestrel's closing spreadsheet, with a memo citing ASU 2021-08 and concluding that no fair value measurement is
required.

**Why it happens.** ASU 2021-08 is correctly understood to have eliminated the fair value "haircut," and the
elimination is then over-read as a carryover election.

**What goes wrong.** "Measure in accordance with ASC 606 as if the acquirer had originated the contracts" is a
measurement instruction, not a carryover permission. Kestrel had no revenue recognition policy and reported on a
modified cash basis: it deferred from the invoice date rather than the service start date on 19 contracts ($84),
deferred amounts billed in arrears for delivered service on 7 contracts ($31), and deferred monthly arrears
billings on 4 contracts ($15). The correct balance is $610. Recording $740 overstates the acquired liability by
$130, understates net working capital acquired, overstates goodwill, and understates post-acquisition revenue.

**How to avoid it.** Recompute the acquired balance from the acquired contracts — 61 contracts is a fully testable
population — and reconcile the acquired liability, post-acquisition billings, and the $340 of post-acquisition
revenue as a miniature roll-forward. Do not let a management scope-out of the acquiree from the Section 404(a)
assessment become a scope-out from the financial statement audit.

### Mistake 6.7 — Remeasuring foreign-currency deferred revenue at the closing rate

**What it looks like.** A foreign-exchange gain or loss in the income statement arising from deferred revenue, or a
NetSuite month-end revaluation job whose account range includes 2400, 2405, and 2410.

**Why it happens.** Revaluation jobs are configured by account range and default to including all liability
accounts. A contract liability looks like an amount owed, and amounts owed are usually monetary.

**What goes wrong.** A fictitious earnings item is created. On contract C-2, the £489.0 liability measured at the
October 1, 2025 inception rate would become £494.4 if remeasured at the December 31, 2025 EUR/GBP rate, producing a
£5.4 (approximately $6.8) loss that has no economic content — AtlasFlow will settle the obligation by delivering
service, not by paying euros. The error also contaminates the translation analysis, because the earnings item is
then mixed with the genuine $(260) of translation that belongs in other comprehensive income.

**How to avoid it.** Read the revaluation job's account list and confirm 2400, 2405, and 2410 are excluded; then
recompute one contract from the inception rate (€740 invoiced × 0.8615 EUR/GBP at inception = £637.5, less £148.5
earned over the 92 days from October 1 to December 31, 2025, equals £489.0; £489.0 × 1.2680 USD/GBP = $620.0) and
agree it to the consolidation detail. As a population-level check, regress monthly USD deferred revenue against the closing rate
after controlling for the local-currency balance.

### Mistake 6.8 — Treating the RPO disclosure as a footnote rather than as a recomputable population

**What it looks like.** The disclosure workpaper consists of management's schedule, a tie-out of the total to the
draft footnote, a comparison to the prior year, and a disclosure checklist sign-off. No independent computation
exists.

**Why it happens.** RPO does not appear in the primary financial statements, so it inherits a "disclosure only"
risk assessment. The computation is also genuinely laborious, and management's schedule looks authoritative.

**What goes wrong.** Every error that lives in the query survives the audit. AtlasFlow's draft $215,860 included
$1,860 of amounts the company has no enforceable right to receive, because the Snowflake query contained no filter
for termination-for-convenience provisions. That is 128% of overall materiality of $1,450, in a disclosure that
implicitly asserts enforceability, and no amount of tie-out to the footnote would have found it.

**How to avoid it.** Build the number from the contract population: total contracted value on active charges of
$356,000, less cumulative revenue recognized of $144,960, less non-enforceable amounts of $1,860, less usage
consideration under the practical expedient of $1,120, less self-serve amounts with no enforceable term of $380,
plus unsatisfied services obligations of $6,180, plus $140 of allocated unexercised material rights, equals
$214,000. Then reconcile it to the balance sheet: $77,820 of RPO already billed plus $380 excluded equals the
$78,200 liability, and $77,820 plus $136,180 unbilled equals $214,000.

### Mistake 6.9 — Electing a practical expedient without disclosing it, or eliding what it removes

**What it looks like.** The footnote states RPO of $214,000 with no statement that variable consideration allocated
to wholly unsatisfied performance obligations, or amounts under contracts with an original expected duration of one
year or less, have been excluded.

**Why it happens.** The expedients in ASC 606-10-50-14 and 50-14A are elected by the accounting team as a
computational convenience and the corresponding disclosure requirement in ASC 606-10-50-15 is treated as optional
boilerplate.

**What goes wrong.** The disclosure becomes uninterpretable and, on a usage-heavy population, misleading. A reader
comparing AtlasFlow's $214,000 to a competitor that includes estimated usage is not comparing like with like. The
$1,120 of usage consideration excluded here is small, but the point of the disclosure of the election is that the
reader, not the preparer, decides whether it is small.

**How to avoid it.** Confirm which expedients are elected, quantify what each removes, and confirm the election is
described in the footnote. Then confirm the election is applied consistently: an entity cannot exclude usage
consideration from RPO under the expedient while including estimated usage in the transaction price for revenue
recognition purposes without explaining how both are true.

### Mistake 6.10 — Leaving deferred revenue on expired subscriptions and dormant engagements uninvestigated

**What it looks like.** The aging shows $490 on 41 contracts whose subscription term ended on or before
December 31, 2025 and $620 on 17 professional services engagements with no recorded hours in 180 days. The
workpaper notes that both are below performance materiality of $940 and passes on.

**Why it happens.** Each line is individually immaterial, and the aging is treated as an analytic whose purpose is
to identify material amounts rather than as a diagnostic whose purpose is to identify impossible ones.

**What goes wrong.** A liability to deliver service under a contract that has ended is not a small balance; it is
an arithmetically impossible one, and each such balance is a signal with a different cause. At AtlasFlow the
investigation of the $490 found $390 of legitimately renewed contracts with mis-entered start dates (a
classification error), $74 of revenue that should have been recognized in FY2025 (a misstatement above the $72
clearly trivial threshold, requiring accumulation), and $26 owed to customers as refunds (a misclassification
between accounts 2400 and 2230). The dormant services deferral is worse: a balance releasable to revenue in any
future period with no external trigger is the cookie jar AS 2401 directs you to look for.

**How to avoid it.** Query the aging yourself rather than requesting it, using the subscription term end date and
the last recorded hour date. Investigate every item in the two impossible categories regardless of amount, and
document the disposition of each. The cost is a few hours; the finding rate on this procedure is high.

## Practice Exercises

All exercises use AtlasFlow facts. Amounts are in thousands of US dollars unless stated otherwise. FY2025 overall
materiality is $1,450, performance materiality is $940, and the clearly trivial threshold is $72.

### Exercise 6-1

**[Foundational]** Using only the following figures, construct the FY2025 deferred revenue roll-forward and prove
that it foots: deferred revenue at January 1, 2025 of $56,900 current and $5,400 noncurrent; billings recorded
through deferred revenue of $163,750; revenue recognized from the opening balance of $54,900; revenue recognized
from FY2025 billings of $93,300; deferred revenue assumed in the Kestrel Labs acquisition of $610; foreign currency
translation of $(260). State the closing balance and state which two components did not arise from a customer
invoice.

### Exercise 6-2

**[Foundational]** AtlasFlow's FY2025 revenue was $148,200 and deferred revenue rose from $62,300 to $78,200.
Contract assets and unbilled receivables rose from $2,100 to $3,400. Deferred revenue of $610 was assumed in the
Kestrel acquisition and $260 of the movement was foreign currency translation. Compute (a) billings recorded
through deferred revenue and (b) total invoicing net of credit memos. Then compute cash collected from customers
given gross accounts receivable of $30,500 at January 1, 2025 and $38,600 at December 31, 2025, write-offs against
the allowance of $1,230, and a $110 reduction of receivables from translation.

### Exercise 6-3

**[Foundational]** For each of the following, state whether the December 31, 2025 balance is a contract liability, a
refund liability, or neither, and state whether it enters the RPO disclosure: (a) $410 of approved credit memos that
the customer may take in cash; (b) $680 of unapplied customer credits usable only against future invoices for future
service, lapsing if unused; (c) $290 of earned but unclaimed service-level agreement credits; (d) $320 of
termination refunds on three contracts cancelled in December 2025; (e) $3,740 of billed and unearned fixed-fee
implementation fees; (f) $1,240 of ramp-driven amounts where cumulative straight-line revenue exceeds cumulative
invoicing.

### Exercise 6-4

**[Intermediate]** Recompute the current and noncurrent split of the $78,200 deferred revenue balance from the
following scheduled release amounts and state the classification of each: January–March 2026 $27,600; April–June
2026 $20,700; July–September 2026 $13,600; October–December 2026 $9,400; calendar 2027 $5,600; January 2028 and
later $1,300. Then explain in two to three sentences why C-1 Meridian Health Systems, which has 24 months remaining
on a 36-month term at December 31, 2025, contributes nothing to the noncurrent balance.

### Exercise 6-5

**[Intermediate]** Contract C-2 with Voltaire Logistics S.A. is held by AtlasFlow's UK entity (functional currency
GBP) and is denominated in euros. The year-1 invoice of €740 was issued October 1, 2025, when the EUR/GBP spot rate
was 0.8615. Cumulative revenue recognized on the contract through December 31, 2025 per the RevPro schedule is
£148.5. The EUR/GBP rate at December 31, 2025 is 0.8710 and the closing USD/GBP rate is 1.2680. Compute (a) the
invoiced amount in GBP, (b) the contract liability in GBP at December 31, 2025 as correctly measured, (c) the amount
reported in consolidated USD, and (d) the misstatement, in GBP and in USD, if the liability were remeasured at the
closing EUR/GBP rate. State the authoritative basis for the correct answer and state which financial statement line
the erroneous amount would hit.

### Exercise 6-6

**[Intermediate]** Kestrel Labs' closing spreadsheet showed deferred revenue of $740 at August 4, 2025. Your
recomputation from the 61 acquired contracts identifies: 19 contracts where deferral began at the invoice date
rather than the service start date, overstating the liability by $84; 7 contracts billed in arrears for services
already delivered, deferred as though billed in advance, $31; 4 monthly arrears contracts recorded as deferred where
the correct balance is nil, $15. Compute the amount to record in the purchase price allocation. State the effect of
recording $740 instead on (a) net working capital acquired, (b) goodwill, and (c) post-acquisition revenue. Cite the
governing guidance and state its effective date.

### Exercise 6-7

**[Intermediate]** Recompute the RPO disclosure at December 31, 2025 from the following: total contracted value of
active subscription rate-plan charges $356,000; cumulative revenue recognized on those charges $144,960;
non-enforceable amounts on 23 termination-for-convenience contracts $1,860; usage consideration excluded under the
practical expedient $1,120; self-serve amounts with no enforceable term $380; unsatisfied professional services
obligations $6,180; allocated amounts of unexercised material rights $140. Then reconcile your answer to the balance
sheet given that $77,820 of RPO has already been billed and $380 of deferred revenue is excluded from RPO.

### Exercise 6-8

**[Intermediate]** The following analytics are proposed as substantive analytical procedures over the completeness
of deferred revenue. For each, state whether it can serve as substantive evidence, and support your answer with a
precision computation. (a) Deferred revenue ÷ ARR, 45.5% in FY2025 against 45.3% in FY2024, where ARR is $172,000.
(b) The billings bridge reconciling revenue and the change in deferred revenue to net invoicing of $162,450 per the
Zuora Billing invoice register. Overall materiality is $1,450 and performance materiality is $940.

### Exercise 6-9

**[Advanced]** Management's draft RPO disclosure is $215,860, of which $139,700 is expected to be recognized within
twelve months. Twenty-three contracts contain a termination-for-convenience clause with no penalty beyond forfeiture
of an unused prepayment; the draft included $4,120 of remaining contracted amounts on them, of which only $2,260 is
enforceable. Of the non-enforceable excess, $800 relates to periods falling within twelve months of the balance
sheet date. Produce the corrected disclosure, including the total, both maturity buckets, and the twelve-month
percentage to one decimal place, and prove that each column foots. Then explain in three to four sentences why
removing amounts *raises* the twelve-month percentage.

### Exercise 6-10

**[Advanced]** A retrospective review of the 31 fixed-fee implementation engagements completed in FY2025 shows that
actual hours exceeded original estimates by an average of 8.4%, with 22 of the 31 over-running. Cumulative revenue
recognized on the 48 fixed-fee engagements still in progress at December 31, 2025 is $6,120 against cumulative
billings of $9,860 and deferred revenue of $3,740. Compute the indicated misstatement in cumulative revenue on the
in-progress engagements if the same 8.4% understatement of estimated total hours applies, state the direction of the
misstatement, express it as a percentage of performance materiality of $940, and state the two things the pattern of
22 of 31 tells you that the average alone does not.

### Exercise 6-11

**[Advanced]** Find the errors. A staff auditor submits the following workpaper conclusion for review. Identify at
least five distinct defects, and for each state the correct treatment.

```text
WP 6100-02  DEFERRED REVENUE — SUMMARY OF PROCEDURES AND CONCLUSION
1. Obtained management's deferred revenue roll-forward. Recomputed the billings
   line as ending balance 78,200 less beginning balance 62,300 plus revenue
   148,200 = 164,100. Schedule foots. No exceptions.
2. Selected 40 contracts from the 12/31/2025 deferred revenue detail using
   monetary unit sampling and agreed each to the customer invoice and to the
   RevPro schedule. All 40 agreed. Deferred revenue is therefore complete.
3. Performed a substantive analytical procedure by comparing the deferred
   revenue to ARR ratio (45.5%) to the prior year (45.3%). No significant
   fluctuation noted; completeness assertion supported.
4. Agreed the current/noncurrent split of 71,300 / 6,900 to the classification
   in management's schedule, which classifies by remaining contract term.
5. Agreed RPO of 214,000 per management's Snowflake query output to the draft
   footnote. Agreed the prior-year figure of 168,500 to the FY2024 10-K.
6. Noted 490 of deferred revenue on subscriptions whose term ended before
   12/31/2025 and 620 on dormant services engagements. Both below performance
   materiality of 940; no further procedures.
CONCLUSION: Deferred revenue of 78,200 is fairly stated in all material
respects. All relevant assertions are supported.
```

### Exercise 6-12

**[Advanced]** Drafting. Write the paragraph of the audit file memorandum, 180 to 240 words, that documents the
engagement team's conclusion on the materiality of the $1,860 RPO overstatement. It must state the quantitative
comparison to overall materiality of $1,450 and to the $215,860 disclosed amount, address the fact that no primary
statement line is affected, address the qualitative factors that made the item material notwithstanding, and state
the conclusion and its basis.

### Exercise 6-13

**[Advanced]** Drafting. Write the description of a management review control, 120 to 180 words, over the RPO
disclosure that would be precise enough to detect a $1,860 misstatement arising from a missing termination-clause
filter in the underlying query. Your description must identify the control owner, the frequency, the specific
information used, the criteria for investigation, and the evidence of operation, and must be written so that a
tester could design a test of operating effectiveness from it without asking a question.

### Exercise 6-14

**[Advanced]** Cross-chapter. Chapter 5, §5.9 concludes that revenue on a ramped contract is recognized ratably over
the total allocated transaction price rather than on the invoiced amount, and Chapter 3 establishes overall
materiality of $1,450 and performance materiality of $940. AtlasFlow's population has 34% of annual contract value
in ramped contracts, and the December 31, 2025 balance sheet shows $1,240 of ramp-driven contract assets within the
$3,400 total. State (a) why the $1,240 is a contract asset rather than a receivable, (b) what its *absence* from a
population with 34% ramped ACV would indicate and what you would do about it, and (c) how you would design a
population-level test of the $1,240 given performance materiality of $940 and 34% ramped ACV.

## Solutions to Practice Exercises

### Solution 6-1

Opening balance $56,900 + $5,400 = **$62,300**.

| Component | Amount |
| --- | --- |
| Deferred revenue, January 1, 2025 | 62,300 |
| Billings recorded through deferred revenue | 163,750 |
| Revenue recognized from the opening balance | (54,900) |
| Revenue recognized from FY2025 billings | (93,300) |
| Deferred revenue assumed in the Kestrel Labs acquisition | 610 |
| Foreign currency translation | (260) |
| **Deferred revenue, December 31, 2025** | **78,200** |

Footing: $62,300 + $163,750 = $226,050; $226,050 − $54,900 − $93,300 = $77,850; $77,850 + $610 − $260 = **$78,200**.

The two components that did not arise from a customer invoice are the **$610 assumed in the Kestrel acquisition**
and the **$(260) of foreign currency translation**. Both must be separately substantiated (§6.9, §6.10) because
both are the kind of item that is otherwise absorbed into a billings line to make a schedule foot.

Two additional proofs are available on these figures: $54,900 + $93,300 = $148,200, which equals total revenue per
the statement of operations, and $54,900 ÷ $62,300 = 88.1%, the implied conversion of the opening balance, which is
consistent with a population dominated by annual-in-advance contracts.

### Solution 6-2

(a) Billings recorded through deferred revenue:

$148,200 revenue + ($78,200 − $62,300) increase in deferred revenue $15,900 − $610 Kestrel (non-billing) + $260
translation (non-billing) = **$163,750**.

(b) Total invoicing, net of credit memos:

$163,750 − $1,300 increase in contract assets ($3,400 − $2,100) = **$162,450**.

The $1,300 deduction is the step most often omitted. Revenue recognized in advance of invoicing passes through
deferred revenue in the RevPro subledger and is reclassified to account 1220, so the $163,750 includes $1,300 of
"billings" that were never invoiced.

(c) Cash collected from customers:

$162,450 + $30,500 opening gross accounts receivable − $38,600 closing gross accounts receivable − $1,230
write-offs − $110 translation = **$153,010**.

Check: $162,450 + $30,500 = $192,950; $192,950 − $38,600 = $154,350; $154,350 − $1,230 − $110 = $153,010.

### Solution 6-3

| Item | Classification | In RPO? | Reason |
| --- | --- | --- | --- |
| (a) $410 refundable credit memos | Refund liability, account 2230 | No | Settled in cash at the customer's election, not by delivering service |
| (b) $680 unapplied credits usable only against future service | Contract liability, deferred revenue | Yes | AtlasFlow owes service, not cash; the credits lapse if unused |
| (c) $290 earned SLA credits | Neither; a reduction of the transaction price accrued in account 2230 | No | Recorded as a debit to contra revenue account 4900 and a credit to 2230, not as an expense |
| (d) $320 termination refunds | Refund liability, account 2230 | No | The contracts are cancelled; no performance obligation remains |
| (e) $3,740 billed and unearned implementation fees | Contract liability, account 2405 | Yes | An unsatisfied performance obligation for services |
| (f) $1,240 ramp-driven excess of revenue over invoicing | Contract asset, account 1220 | The unsatisfied portion of the contract is in RPO; the $1,240 asset itself is not an RPO amount | The right to the next annual invoice is conditional on continued performance |

The operative test is the one in §6.13: if the customer never buys anything again, does AtlasFlow owe cash? If yes,
refund liability. If AtlasFlow instead owes future service, contract liability. Item (b) is the item most often
misclassified, and applying the test moves it out of account 2230 and into deferred revenue.

### Solution 6-4

| Scheduled release period | Amount | Classification |
| --- | --- | --- |
| January – March 2026 | 27,600 | Current |
| April – June 2026 | 20,700 | Current |
| July – September 2026 | 13,600 | Current |
| October – December 2026 | 9,400 | Current |
| **Current** | **71,300** | |
| Calendar 2027 | 5,600 | Noncurrent |
| January 2028 and later | 1,300 | Noncurrent |
| **Noncurrent** | **6,900** | |
| **Total** | **78,200** | |

Footing: $27,600 + $20,700 + $13,600 + $9,400 = $71,300; $5,600 + $1,300 = $6,900; $71,300 + $6,900 = $78,200.

C-1 Meridian contributes nothing to the noncurrent balance because classification is driven by **billing frequency,
not contract term**. C-1 is a 36-month contract billed annually in advance, so at December 31, 2025 the only amount
in deferred revenue is the unearned portion of the first annual invoice, all of which releases within twelve months.
The second and third annual invoices have not been issued and are therefore not in the liability at all — they are
in RPO as unbilled amounts.

### Solution 6-5

(a) The invoiced amount in GBP: €740 × 0.8615 EUR/GBP at the October 1, 2025 transaction date = **£637.5**.

(b) The liability at December 31, 2025, correctly measured: £637.5 invoiced less £148.5 of cumulative revenue
recognized = **£489.0**, and it is **not remeasured**. (The £148.5 is the 92-day portion of the £1,178.6 allocated
to the subscription performance obligation over the 731-day term — £1,178.6 × 92 ÷ 731 = £148.3, the small
difference arising from RevPro's daily-rate rounding on the two rate-plan charges. The £96.4 allocated to the
material right remains fully deferred; see Chapter 5, §5.12.)

(c) Reported in consolidated USD: £489.0 × 1.2680 USD/GBP closing rate = **$620.0**. Note that the closing rate *is*
used for translation from the UK entity's functional currency into the USD reporting currency; that is a different
mechanism from remeasurement.

(d) If remeasured at the closing EUR/GBP rate the liability would be £489.0 × (0.8710 ÷ 0.8615) = **£494.4**, a
misstatement of £494.4 − £489.0 = **£5.4**, or £5.4 × 1.2680 = **$6.8**.

The authoritative basis is that a contract liability is a **non-monetary item** under ASC 830-10-45: it does not
represent a fixed number of currency units to be paid but an obligation to deliver service, so it is recorded at
the functional-currency amount determined on the transaction date and is not remeasured for later rate movements.
The erroneous £5.4 would hit **earnings**, as a foreign exchange loss in other income and expense, and would
contaminate the translation analysis by mixing an income statement item with the $(260) of genuine translation that
belongs in other comprehensive income (account 3200).

### Solution 6-6

Amount to record: $740 − $84 − $31 − $15 = **$610**.

Effect of recording $740 instead:

- **(a) Net working capital acquired** would be $130 lower — $200 as recorded becomes $70 — because the acquired
  liability is $130 larger.
- **(b) Goodwill** would be $130 higher, since consideration transferred is unchanged and the net identifiable
  assets acquired are $130 lower.
- **(c) Post-acquisition revenue** would be higher by up to $130 as the excess liability unwound over the remaining
  service periods, most of it in the period from August 4 to December 31, 2025. Recorded Kestrel revenue for that
  period is $340; the excess would inflate it.

The governing guidance is **ASU 2021-08**, which amended ASC 805 to require contract assets and contract
liabilities acquired in a business combination to be measured in accordance with ASC 606 as if the acquirer had
originated the contracts, replacing fair value measurement. It is effective for public business entities for fiscal
years beginning after December 15, 2022, so it is in force for FY2025 and for the August 4, 2025 acquisition.

The trap is reading "as if the acquirer had originated the contracts" as permission to carry over the acquiree's
balance. It is a measurement instruction. Where the acquiree applied ASC 606 correctly the two coincide; Kestrel had
no revenue recognition policy and reported on a modified cash basis, so they do not.

### Solution 6-7

| Line | Component | Amount |
| --- | --- | --- |
| 1 | Total contracted value, active subscription rate-plan charges | 356,000 |
| 2 | Less cumulative revenue recognized on those charges | (144,960) |
| 3 | Remaining contracted subscription amounts | 211,040 |
| 4 | Less non-enforceable amounts, 23 termination-for-convenience contracts | (1,860) |
| 5 | Less usage consideration excluded under the practical expedient | (1,120) |
| 6 | Less self-serve amounts with no enforceable term | (380) |
| 7 | Add unsatisfied professional services obligations | 6,180 |
| 8 | Add allocated amounts of unexercised material rights | 140 |
| 9 | **RPO per recomputation** | **214,000** |

Arithmetic: $356,000 − $144,960 = $211,040; $211,040 − $1,860 − $1,120 − $380 = $207,680; $207,680 + $6,180 + $140 =
$214,000.

Reconciliation to the balance sheet, which is the step that gives the recomputation its power:

- $77,820 of RPO consists of amounts already billed, and $380 of deferred revenue is excluded from RPO because the
  self-serve accounts have no enforceable term beyond the current month. $77,820 + $380 = **$78,200**, the deferred
  revenue balance.
- $77,820 billed + $136,180 unbilled = **$214,000**, the RPO. The unbilled portion is 63.6% of RPO, which is what
  a population of annual-in-advance billing on multi-year terms produces.

### Solution 6-8

**(a) Deferred revenue ÷ ARR: cannot serve as substantive evidence.** Compute the precision. One percentage point of
the ratio is $172,000 × 1% = **$1,720**, which is 119% of overall materiality of $1,450 and 183% of performance
materiality of $940. The smallest movement the analytic can meaningfully resolve is larger than materiality, so the
procedure cannot detect a material misstatement. Even a half-point threshold of $860 is only marginally below
performance materiality, and the ratio is legitimately affected by billing-frequency mix, contract-duration mix, and
the Kestrel acquisition, none of which can be held constant. AS 2305 requires an expectation precise enough to
identify a misstatement that could be material; this expectation is not. Its correct use is **risk assessment**:
stability at 45.3% to 45.5%, with billings growth of 24.6% tracking revenue growth of 24.6%, is consistent with no
structural change in billing terms.

**(b) The billings bridge: can serve as substantive evidence.** It is not a ratio compared to an expectation but an
**identity** connecting four separately maintained populations — the revenue subledger, the contract liability, the
contract asset, and the invoice register. Its precision is limited only by the accuracy of those populations, not by
a modelled expectation, and a break in the identity of any size is an unexplained difference requiring
investigation. At AtlasFlow the identity closes exactly: $148,200 + $15,900 − $610 + $260 = $163,750, less $1,300 =
$162,450, which agrees to the invoice register. A $1,580 break would be 109% of overall materiality and would
narrow the cause to four candidates: invoicing recorded but never issued, write-offs bypassing the allowance, a
receivable in the wrong period, or receipts posted outside the accounts queried.

### Solution 6-9

**Corrected disclosure (in thousands):**

| Line | As drafted | Adjustment | As corrected |
| --- | --- | --- | --- |
| Remaining performance obligations | 215,860 | (1,860) | 214,000 |
| Expected within 12 months | 139,700 | (800) | 138,900 |
| Expected after 12 months | 76,160 | (1,060) | 75,100 |
| Twelve-month portion | 64.7% | | 64.9% |

Footing: $139,700 + $76,160 = $215,860 and $138,900 + $75,100 = $214,000. The adjustment columns foot:
$(800) + $(1,060) = $(1,860). The beyond-twelve-month adjustment is derived: $1,860 total excess less $800 within
twelve months = $1,060. Percentages: $139,700 ÷ $215,860 = 64.72%, rounding to 64.7%; $138,900 ÷ $214,000 = 64.91%,
rounding to 64.9%.

**Why the percentage rises.** The excess amounts all relate to periods *after* each contract's prepaid period ends,
so they are disproportionately long-dated: $800 of the $1,860, or 43.0%, falls within twelve months, against 64.7%
for the draft disclosure as a whole. Removing a set of amounts with a lower-than-average twelve-month proportion
necessarily raises the twelve-month proportion of what remains. This matters practically: a team that expects a
correction to worsen every metric management is judged on may under-anticipate management's willingness to record
it, and may equally mistake management's agreement for confirmation that the adjustment is uncontroversial. It is
neither. The adjustment is required because the disclosure asserted enforceability it did not have.

### Solution 6-10

**Computation.** If estimated total hours are understated by 8.4%, the percentage-complete numerator is unchanged
and the denominator should be 1.084 times what was used. Cumulative revenue should therefore be
$6,120 ÷ 1.084 = $5,646, and the indicated overstatement is $6,120 − $5,646 = **$474**. Equivalently,
$6,120 × (1 − 1 ÷ 1.084) = $6,120 × 0.07749 = $474.

**Direction.** Revenue is **overstated** and deferred revenue **understated** by $474. A denominator that is too
small produces a percentage complete that is too high, which accelerates revenue.

**As a percentage of performance materiality:** $474 ÷ $940 = **50.4%**. That is well above the $72 clearly trivial
threshold and must be accumulated and evaluated, not noted and passed. (Uncorrected misstatement U-4 of $95 in the
FY2025 file is the residue of this analysis after management revised the estimates on the largest engagements.)

**What 22 of 31 tells you that the average does not.** First, the bias is **one-directional rather than dispersed**:
71% of engagements over-ran, so the 8.4% is not an average of offsetting errors around a neutral estimate but a
systematic understatement. A symmetric distribution around a small average error would be estimation noise, which
does not indicate misstatement; an asymmetric distribution indicates bias, which does. Second, a one-directional
bias in an estimate is a **management bias indicator** under AS 2501 and AU-C 540, and it must be evaluated for
whether it indicates a risk of material misstatement due to fraud, not merely corrected as an arithmetic matter.
The direction here favours earlier revenue, which is the direction the fraud risk assessment predicts.

### Solution 6-11

The workpaper contains at least six distinct defects.

1. **Step 1 — the billings line is a plug, and the arithmetic is also wrong.** Deriving billings as ending balance
   less beginning balance plus revenue guarantees the schedule foots and therefore proves nothing. It also produces
   $164,100 rather than $163,750, because it omits the $610 acquired balance and the $(260) of translation, which
   are not billings. *Correct treatment:* independently source billings from the Zuora Billing invoice register
   ($166,290 gross less $3,840 credit memos = $162,450 net, plus the $1,300 increase in contract assets = $163,750)
   and substantiate the acquired and translation lines separately.
2. **Step 2 — the conclusion does not follow from the procedure.** Selecting from the recorded deferred revenue
   detail tests existence, accuracy, and measurement. It cannot test completeness, because a contract omitted from
   the population has a zero probability of selection. *Correct treatment:* re-characterize the procedure as
   supporting existence and accuracy, and obtain completeness evidence from a population that includes contracts
   with a nil recorded balance — the invoice register, the Salesforce order population, and the RPO recomputation.
3. **Step 3 — the analytic is mislabelled as substantive.** One point of the deferred-revenue-to-ARR ratio is
   $1,720, which is 119% of overall materiality; the procedure cannot detect a material misstatement. *Correct
   treatment:* document it as risk assessment evidence and remove the assertion-level conclusion.
4. **Step 4 — the classification basis is wrong.** Classifying by remaining contract term rather than by scheduled
   release date misclassifies every contract whose billing frequency is shorter than its term, which in this
   population is most of them. *Correct treatment:* recompute from the RevPro revenue schedule aggregated by
   scheduled recognition month, restricted to amounts funded by invoices already issued, and agree to $71,300 and
   $6,900.
5. **Step 5 — RPO is tied out but never recomputed.** Agreeing management's query output to the footnote tests
   transcription only. Every error in the query survives, which is exactly how the $1,860 non-enforceable amount
   reached the draft disclosure. *Correct treatment:* recompute RPO from the contract population and reconcile it to
   the balance sheet ($77,820 + $380 = $78,200; $77,820 + $136,180 = $214,000).
6. **Step 6 — impossible balances are dismissed on quantitative grounds.** Deferred revenue on a subscription whose
   term has ended is not a small balance but an arithmetically impossible one, and a dormant services deferral is a
   releasable-at-will reserve of exactly the type AS 2401 directs the auditor to identify. *Correct treatment:*
   investigate all 41 expired-term contracts and all 17 dormant engagements regardless of amount. At AtlasFlow that
   investigation produced $74 of understated revenue, above the $72 clearly trivial threshold, and $26 of
   misclassification.

A seventh defect is the conclusion itself: "all relevant assertions are supported" is asserted for completeness,
classification, and presentation and disclosure when no procedure in the workpaper addresses any of the three.

### Solution 6-12

Model language, 213 words:

```text
Materiality of the identified misstatement of the RPO disclosure. Management's
draft footnote disclosed remaining performance obligations of $215,860 at
December 31, 2025, of which $1,860 represents amounts on 23 contracts
containing a termination-for-convenience provision that the customer is not
obligated to pay and that AtlasFlow has no enforceable right to receive. The
misstatement is 128% of overall materiality of $1,450 and 198% of performance
materiality of $940, and is 0.87% of the amount disclosed. No line item in the
primary financial statements is affected: deferred revenue of $78,200 is
correct under each of the three defensible contract-term views considered, and
no asset, liability, revenue, or cash flow amount changes. We therefore
assessed materiality against the disclosure itself and against the decisions of
the users who rely on it. Three qualitative factors were determinative. The
disclosure is a specific quantified forward-looking amount that investors use
to model future revenue; it is discussed in Item 7 and featured in management's
earnings materials, and management's compensation includes an RPO-linked
metric; and the disclosure implicitly asserts that the amounts disclosed are
enforceable, so the inclusion of non-enforceable amounts misstates its
substance rather than only its magnitude. We concluded that the misstatement is
material to the disclosure and requested correction. Management corrected the
disclosure to $214,000 before filing.
```

An alternative and defensible conclusion is that a 0.87% error in a disclosure with no primary-statement effect is
immaterial and should be passed as an uncorrected misstatement with a summary-of-uncorrected-misstatements entry.
That conclusion is weaker here for one reason: the error is not a measurement imprecision but the inclusion of
amounts that fail the enforceability condition, which is a qualitative defect that quantitative smallness does not
cure. It would be stronger if the amounts were enforceable but the timing estimate were imprecise.

### Solution 6-13

Model control description, 164 words:

```text
Control R-14 (annual, disclosure). Within ten business days of each year end,
the Corporate Controller re-performs the remaining performance obligation
computation independently of the RevOps team, using the Zuora Billing active
rate-plan charge extract, the RevPro cumulative revenue file, and the legal
department's contract clause register, and reconciles the independent result to
the RevOps query output. The Controller separately obtains a full-text search
of the Salesforce contract repository for termination language, reconciles the
resulting contract count to the clause register count, investigates every
difference, and confirms that each contract identified is either excluded from
RPO beyond its prepaid period or supported by documentation of a substantive
termination penalty. Any difference between the independent computation and the
query output exceeding $250 is investigated to the contract level and resolved
before the disclosure is finalized. The Controller reconciles RPO already
billed to the deferred revenue balance per the general ledger. Evidence of
operation is the completed reconciliation, the clause count reconciliation, the
list of investigated differences with dispositions, and the Controller's
signature and date.
```

Three features make this description testable and precise enough to detect $1,860. It specifies an **independent
re-performance** rather than a review of output, so the query's logic is exercised rather than assumed. It specifies
an **investigation threshold of $250**, well below the $940 performance materiality and below the $1,860 that
occurred, so the control's precision is stated and testable rather than left as "review for reasonableness." And it
requires a **second independent source for the clause population**, which is the specific failure that occurred at
AtlasFlow: the legal register held 26 contracts and the full-text search found 31, and four of the five missing from
the register were among the 23 that mattered. The description management actually provided — a comparison of the
current-year output to the prior-year output — could not detect $1,860, because at the aggregate level the error
moved RPO growth from 27.0% to 28.1%.

### Solution 6-14

**(a) Why the $1,240 is a contract asset rather than a receivable.** Under ASC 606-10-45 a receivable is an
*unconditional* right to consideration, with only the passage of time standing between the entity and payment. On a
ramped contract billed annually in advance, AtlasFlow's right to issue the next annual invoice is conditional on
continued performance through the anniversary date; if the contract terminates, the amount is not billable.
Consideration is therefore conditional on something other than the passage of time, which makes the balance a
contract asset. The $380 of December time-and-materials work invoiced in January 2026, by contrast, is a receivable:
the service is delivered and only invoicing mechanics remain. The distinction is not cosmetic — the $380 belongs in
the CECL pool and the contract assets require an ASC 606 impairment assessment (Chapter 7, §7.8 and §7.9).

**(b) What its absence would indicate.** A population with 34% of ACV in ramped contracts, recognized ratably over
the total allocated transaction price under Chapter 5, §5.9, must produce contract assets in the early years of
those contracts as a matter of arithmetic. A nil or trivial balance is therefore evidence that the entity is
recognizing the **invoiced** amount rather than the allocated total — that is, recognizing revenue on the billing
schedule. That is a revenue recognition error, not a balance sheet classification error, and its sign is
predictable: revenue is understated in the early periods of a ramped contract and overstated later. On discovering
it, you would stop treating the ramp population as a balance sheet matter, select the largest ramped contracts,
recompute revenue for each from the allocated total, and extrapolate; you would also reassess the risk of material
misstatement over accuracy of revenue and reconsider whether the RevPro configuration for ramped rate plans is a
control deficiency.

**(c) Designing a population-level test.** Do not sample. Recompute the expected balance for the whole ramped
population, because the data required is the same data required for one contract. Extract every subscription whose
rate-plan charge amounts differ across periods of the same contract, compute for each the cumulative straight-line
revenue at December 31, 2025 from the allocated total and the cumulative invoiced amount funded, and take the sum of
the positive differences at the contract level. That sum should equal $1,240. Set the investigation threshold below
performance materiality of $940 — $200 is a defensible choice, since the population is homogeneous and the
computation is fully automated so a tighter threshold costs nothing — and investigate every contract-level
difference above it. Because 34% of ACV is ramped, the population is large enough that a sample sized for $940 of
tolerable misstatement would be uneconomic and a full recomputation is cheaper. Reconcile the $1,240 to the three
places it must appear: the composition of account 1220 (Exhibit 6-11), the billings bridge line 8 within the
$1,300 movement (Exhibit 6-4), and the contract-asset movement in the roll-forward.

## Review Questions

**RQ 6-1.** Define a contract liability and state the two conditions under ASC 606-10-45 that give rise to one.

**RQ 6-2.** Why is completeness rather than existence the dominant relevant assertion for deferred revenue, and what
does that imply about the population from which you select?

**RQ 6-3.** State the billings bridge identity in both of its parts, including every non-billing adjustment
AtlasFlow required.

**RQ 6-4.** What is the diagnostic weakness of a deferred revenue roll-forward in which the billings line is derived
as the closing balance less the opening balance plus revenue?

**RQ 6-5.** What does the ASC 606-10-50-8 disclosure require, and how do you recompute it rather than derive it by
subtraction?

**RQ 6-6.** Name the three drivers of the current versus noncurrent split of deferred revenue in a SaaS population,
and state which of them is most often confused with contract term.

**RQ 6-7.** Explain the contract-level netting rule and describe the gross-up it produced on AtlasFlow's December 31,
2025 balance sheet.

**RQ 6-8.** Distinguish a receivable from a contract asset, and give the AtlasFlow example of each.

**RQ 6-9.** How did ASU 2021-08 change the measurement of deferred revenue acquired in a business combination, and
why does that change not amount to permission to carry over the acquiree's recorded balance?

**RQ 6-10.** Why is a contract liability a non-monetary item, and what is the practical consequence for the NetSuite
month-end revaluation job?

**RQ 6-11.** Distinguish translation from remeasurement as they apply to AtlasFlow's foreign-currency deferred
revenue, and state which financial statement caption each affects.

**RQ 6-12.** What does the RPO disclosure require, and what is the one thing the disclosure implicitly asserts about
every contract that no primary financial statement line asserts?

**RQ 6-13.** Name the two practical expedients available in computing RPO and state the disclosure consequence of
electing either.

**RQ 6-14.** Why does a contract terminable for convenience without a substantive penalty produce a smaller RPO than
its stated contract term implies, while its deferred revenue balance is unaffected?

**RQ 6-15.** Why can the deferred-revenue-to-ARR ratio not serve as a substantive analytical procedure at AtlasFlow,
and what is the arithmetic that establishes the point?

**RQ 6-16.** What two categories in the deferred revenue aging should mathematically be nil, and what are the
possible explanations for a balance in each?

**RQ 6-17.** Which balance sheet account holds customer credits and refund liabilities at AtlasFlow, what
distinguishes its contents from deferred revenue, and what is the one-question test?

**RQ 6-18.** How is an earned service-level agreement credit recorded, and why is a debit to operating expense wrong?

**RQ 6-19.** State the three tests that carry the deferred professional services revenue balance in account 2405 and
what each is designed to detect.

**RQ 6-20.** Why is the pattern of a retrospective estimate review — 22 of 31 engagements over-running — more
informative than the 8.4% average over-run alone?

## Answers to Review Questions

**RQ 6-1.** A contract liability is an entity's obligation to transfer goods or services to a customer for which the
entity has received, or has an unconditional right to receive, consideration. Under ASC 606-10-45 one arises when
the entity has been paid, or has an unconditional right to payment, before it has satisfied the related performance
obligation. The second condition is the one that surprises people: a liability arises when an invoice is due and
enforceable even if no cash has been received, which is why AtlasFlow's annual-in-advance billing creates deferred
revenue on the invoice date rather than on the collection date.

**RQ 6-2.** Deferred revenue is understated by omission, not overstated by fabrication, and the omission is
symmetrical with an overstatement of revenue — the direction management has an incentive to move. Existence
procedures start from the recorded population, and a contract that was billed and credited entirely to revenue never
enters that population, so its probability of selection is zero regardless of sample size. Completeness therefore
requires a population that includes contracts with a recorded balance of nil: the invoice register, the Salesforce
order population, or a recomputation of RPO from contract data.

**RQ 6-3.** Total invoicing net of credit memos equals revenue recognized, plus the increase in deferred revenue,
less the increase in contract assets and unbilled receivables, less deferred revenue assumed in a business
combination, plus the reduction of deferred revenue from foreign currency translation. At AtlasFlow: $148,200 +
$15,900 − $1,300 − $610 + $260 = $162,450. Cash collected from customers then equals total invoicing plus opening
gross receivables, less closing gross receivables, less receivables written off against the allowance, plus the
reduction of receivables from translation: $162,450 + $30,500 − $38,600 − $1,230 − $110 = $153,010.

**RQ 6-4.** A derived billings line cannot fail to foot, so the footing check has no diagnostic power at all. Any
error in the opening balance, revenue, or the closing balance is absorbed into the billings line and the schedule
reports a self-consistent set of wrong numbers. The remedy is to source the billings line independently from the
Zuora Billing invoice register before accepting the roll-forward; the tell that it is a plug is management's
inability to produce a register total that agrees.

**RQ 6-5.** It requires disclosure of revenue recognized in the reporting period that was included in the contract
liability balance at the beginning of the period — $54,900 for AtlasFlow's FY2025. Recompute it by filtering the
RevPro revenue-schedule detail to lines whose funding invoice predates January 1, 2025 and summing, not by
subtracting two balances. Then check the implied conversion of the opening balance: $54,900 ÷ $62,300 = 88.1%, which
is what an annual-in-advance population should produce, leaving $7,400 of the opening balance still deferred.

**RQ 6-6.** Billing frequency rather than contract term; the timing of mid-period billings; and multi-year
prepayments together with long-dated services and training packages. Billing frequency is the one confused with
contract term, and the confusion is consequential: C-1 Meridian has 24 months remaining on a 36-month term at
December 31, 2025 but contributes nothing to the noncurrent balance, because only the first annual invoice has been
issued.

**RQ 6-7.** A single revenue contract has a single net position — either a contract asset or a contract liability,
never both — but positions on different contracts are not netted, even with the same customer, unless the contracts
are combined under ASC 606-10-25-9. At AtlasFlow the 14,241 net-liability positions sum to $78,200 and the 151
net-asset positions to $3,400; the net across all contracts is $74,800, and the balance sheet grosses that back up to
a $78,200 liability and a $3,400 asset presented separately.

**RQ 6-8.** A receivable is an unconditional right to consideration, with only the passage of time remaining; a
contract asset is a right conditional on something further, typically further performance or milestone
certification. AtlasFlow's $380 of December time-and-materials work invoiced in January 2026 is a receivable; the
$1,780 of fixed-fee services revenue recognized ahead of milestone billing and the $1,240 of ramp-driven excess of
revenue over invoicing are contract assets. The distinction drives which balances enter the CECL pool.

**RQ 6-9.** ASU 2021-08 replaced fair value measurement — which produced the familiar deferred revenue "haircut" and
a post-acquisition revenue step-down — with measurement in accordance with ASC 606 as if the acquirer had originated
the contracts, effective for public business entities for fiscal years beginning after December 15, 2022. That is a
measurement instruction, not a carryover election. Where the acquiree applied ASC 606 correctly the two coincide;
Kestrel Labs had no revenue recognition policy and reported on a modified cash basis, so its $740 spreadsheet balance
required $130 of correction to reach $610.

**RQ 6-10.** Under ASC 830-10-45, a monetary item represents a fixed number of currency units to be received or
paid. A contract liability will be settled by delivering service, not currency, so it is non-monetary: it is recorded
at the functional-currency amount determined on the transaction date and is not remeasured. The practical
consequence is that accounts 2400, 2405, and 2410 must be excluded from the NetSuite month-end revaluation job's
account range — and because such jobs default to including all liability accounts, their inclusion is the expected
failure mode and should be tested by reading the account list.

**RQ 6-11.** Remeasurement restates a foreign-currency-denominated balance into the entity's functional currency at
the current rate and, for monetary items, produces an earnings item; it must not be applied to deferred revenue.
Translation restates the whole of a foreign entity's functional-currency financial statements into the USD reporting
currency at the closing rate, with the difference to the cumulative translation adjustment in accumulated other
comprehensive loss (account 3200). AtlasFlow's $(260) is translation and belongs in other comprehensive income; the
£5.4 that remeasuring C-2 would produce would be an erroneous earnings item.

**RQ 6-12.** ASC 606-10-50-13 requires disclosure of the aggregate transaction price allocated to performance
obligations that are unsatisfied or partially unsatisfied at the reporting date, together with an explanation of
when the entity expects to recognize it. The implicit assertion no primary statement line makes is
**enforceability**: RPO includes only amounts under enforceable rights and obligations, so the disclosure asserts
that every included amount is one the entity has a present enforceable right to receive. Pemberton's deferred
revenue is $480 under every contract-term view, but its RPO contribution is $480 rather than $1,200 only because the
enforceable term ends with the prepaid period.

**RQ 6-13.** An entity need not disclose RPO for performance obligations under contracts with an original expected
duration of one year or less, and need not disclose variable consideration allocated to a wholly unsatisfied
performance obligation (or to a distinct good or service within a series) — the second of which covers usage-based
consideration. Electing either requires disclosure of the election under ASC 606-10-50-15, together with a
description of the nature of the excluded obligations and of any variable consideration not included. The election
removed $1,120 of usage consideration and $380 of self-serve amounts from AtlasFlow's RPO, and the point of
disclosing the election is that the reader, not the preparer, decides whether those amounts matter.

**RQ 6-14.** RPO includes only amounts supported by enforceable rights and obligations. A customer who can terminate
on 30 days' notice with no penalty beyond forfeiting an unused prepayment has no enforceable obligation to pay for
periods beyond the currently prepaid period, so the enforceable term ends there. Deferred revenue is unaffected
because it measures only what has already been billed and not yet earned — an amount inside the prepaid period under
every view of the term. Pemberton illustrates both: $480 of deferred revenue and $480 rather than $1,200 of RPO.

**RQ 6-15.** Because its precision is worse than materiality. One percentage point of the ratio is $172,000 × 1% =
$1,720, which is 119% of overall materiality of $1,450 and 183% of performance materiality of $940; even a
half-point threshold of $860 is only marginally below performance materiality. AS 2305 requires an expectation
precise enough to identify a misstatement that could be material, and this one is not. The ratio's stability from
45.3% to 45.5% is genuine risk assessment evidence about the absence of a structural change in billing terms, and
the file should say exactly that rather than claiming substantive evidence.

**RQ 6-16.** Deferred revenue on subscriptions whose term ended on or before the balance sheet date ($490 across 41
contracts), and deferred professional services revenue on engagements with no recorded hours in 180 days ($620
across 17 engagements). For the first, the candidates are revenue that should have been recognized, a renewal whose
start date was mis-entered, or a credit that should have been refunded — AtlasFlow's investigation found $390, $74,
and $26 respectively. For the second, the engagement is either complete and unrecognized, cancelled, or stalled, and
a stalled engagement with billed unearned revenue is releasable to revenue in any future period with no external
event, which is the condition AS 2401 directs you to look for.

**RQ 6-17.** Account 2230, holding $1,200 at December 31, 2025. Its contents will be settled in cash rather than by
delivering service, so they are not contract liabilities and do not enter RPO. The one-question test is: if the
customer never buys anything again, does AtlasFlow owe cash? If yes, it is a refund liability; if AtlasFlow instead
owes future service, it is a contract liability. Applying that test moved $680 of credits usable only against future
service out of account 2230 and into deferred revenue.

**RQ 6-18.** An earned SLA credit is a reduction of the transaction price, so it is recorded as a debit to contra
revenue (account 4900) and a credit to account 2230. A debit to operating expense is wrong because the credit is not
a cost of providing service; it is consideration the entity is no longer entitled to, which under ASC 606-10-32 is
variable consideration reducing the transaction price. The distinction moves $290 between revenue and expense at
AtlasFlow — corrected misstatement C-2 in the FY2025 file — and therefore changes gross margin and every
revenue-derived metric, not merely a line within operating expenses.

**RQ 6-19.** Test 1, a retrospective review of the estimate of total hours, detects bias in the denominator of the
input measure, which biases the percentage complete and hence revenue. Test 2, reading the dispute correspondence on
the Meridian $1,240 services invoice, detects revenue released from deferred revenue that was not in fact earned and
distinguishes a FY2025 reduction of the transaction price from a FY2026 event. Test 3, investigating dormant
engagements, detects deferrals that have become releasable at management's discretion.

**RQ 6-20.** The average alone is consistent with estimation noise; the pattern is not. Twenty-two of 31 engagements
over-running — 71% — shows a one-directional bias rather than dispersion around a neutral estimate, and bias in an
estimate is an indicator that AS 2501 and AU-C 540 require you to evaluate for whether it points to a risk of
material misstatement due to fraud. The direction matters too: understated total hours accelerate revenue, which is
the direction the fraud risk assessment predicts, so the pattern corroborates the assessed risk rather than merely
sizing an adjustment.

## Key Definitions

**Aging of deferred revenue.** An analysis of a contract liability balance by the status of the underlying
obligation rather than by amount, isolating categories that should mathematically be nil — most importantly balances
on contracts whose term has ended and balances on engagements with no recent delivery activity. It is a diagnostic
rather than a measurement procedure and its finding rate is high relative to its cost.

**Annual recurring revenue (ARR).** The annualized value of the recurring subscription components of contracts in
force at a point in time, excluding one-time fees and, in AtlasFlow's definition, excluding usage overage. It is
not a GAAP measure and its definition varies between entities, so it must be read against the entity's own stated
definition before it is used in an analytic. AtlasFlow's ARR was $172,000 at December 31, 2025.

**Backlog.** A general commercial term for contracted work not yet performed, with no defined measurement basis
under US GAAP. It is not a synonym for the remaining performance obligation disclosure, which has a specific
measurement basis in ASC 606-10-50-13 and excludes amounts not supported by enforceable rights and obligations.

**Billings.** The aggregate amount invoiced to customers in a period, net of credit memos. It is not a GAAP measure
and does not appear in the financial statements, which is what makes the billings bridge useful: it connects the
revenue subledger, the contract liability, the contract asset, and the invoice register, four separately maintained
populations that must reconcile.

**Billings bridge.** The identity relating revenue, the change in deferred revenue, the change in contract assets,
and non-billing movements to net invoicing, extended to relate net invoicing and the change in gross receivables to
cash collected. Because it is an identity reconciled to independent populations rather than a ratio compared to an
expectation, it is capable of serving as substantive evidence.

**Clearly trivial threshold (CTT).** The amount below which misstatements are considered clearly inconsequential in
aggregate and need not be accumulated. AtlasFlow's FY2025 CTT is $72; the $74 of revenue identified in the aging
investigation exceeds it and therefore had to be accumulated.

**Contract asset.** An entity's right to consideration in exchange for goods or services already transferred, where
that right is conditional on something other than the passage of time — typically on further performance or on the
certification of a milestone (ASC 606-10-45). It is distinguished from a receivable, which is an unconditional
right.

**Contract liability.** An entity's obligation to transfer goods or services to a customer for which the entity has
received consideration, or for which consideration is due and unconditionally receivable (ASC 606-10-45). Commonly
captioned "deferred revenue." It is a non-monetary item, and it will be settled by performing rather than by paying.

**Contract-level netting.** The requirement that a single revenue contract be presented as either a net contract
asset or a net contract liability, never both, while positions on different contracts are not netted even with the
same customer unless the contracts are combined under ASC 606-10-25-9. At AtlasFlow it grosses a $74,800 net
position up to a $78,200 liability and a $3,400 asset.

**Deferred revenue haircut.** The reduction of an acquiree's recorded deferred revenue to fair value in a business
combination, historically measured as the cost to fulfil the remaining obligation plus a normal profit margin, which
produced a step-down in post-acquisition revenue. ASU 2021-08 eliminated it for public business entities for fiscal
years beginning after December 15, 2022.

**Deferred revenue roll-forward.** A schedule reconciling the opening contract liability balance to the closing
balance through billings, revenue recognized, business combinations, and foreign currency movements. It is the
organizing document for the account, and it is information produced by the entity, so its completeness and accuracy
must be tested rather than assumed.

**Enforceable rights and obligations.** The condition that determines the term over which a contract exists for
accounting purposes and therefore the amounts included in RPO. A contract terminable for convenience without a
substantive penalty is enforceable only through the currently committed period, notwithstanding a longer stated
term.

**Functional currency.** The currency of the primary economic environment in which an entity operates (ASC 830-10).
AtlasFlow's parent is USD, AtlasFlow Software Ltd is GBP, and AtlasFlow Pty Ltd is AUD; a transaction denominated in
a fourth currency, such as contract C-2 in euros, is measured into the holding entity's functional currency at the
transaction date rate.

**Information produced by the entity (IPE).** A schedule, report, or extract prepared by the client and used as
audit evidence, whose completeness and accuracy must themselves be tested. The deferred revenue roll-forward, the
contract-level balance file, the RPO computation, and every Snowflake or RevPro extract used in this chapter are IPE.

**Material right.** A customer option to acquire additional goods or services at a discount that the customer would
not receive without entering the contract, which constitutes a separate performance obligation to which transaction
price must be allocated (ASC 606-10-55). AtlasFlow's unexercised material rights contribute $140 to the December 31,
2025 RPO. Chapter 5, §5.4 owns the valuation.

**Monetary item.** An asset or liability representing a fixed or determinable number of units of currency to be
received or paid (ASC 830-10-45). Monetary items denominated in a currency other than the functional currency are
remeasured at each balance sheet date with the difference in earnings; a contract liability is not one.

**Practical expedient (RPO).** An election permitted by ASC 606-10-50-14 and 50-14A to exclude from the RPO
disclosure performance obligations under contracts with an original expected duration of one year or less, and
variable consideration allocated to a wholly unsatisfied performance obligation or to a distinct good or service
within a series. Election requires disclosure under ASC 606-10-50-15.

**Precision of an analytical procedure.** The smallest misstatement an analytical procedure is capable of
identifying, determined by the sensitivity of the expectation to the variables that drive it. AS 2305 requires that
a substantive analytical procedure's expectation be precise enough to identify a misstatement that could be
material; the deferred-revenue-to-ARR ratio, at $1,720 per percentage point, is not.

**Reciprocal-population testing.** A completeness procedure that selects from a population other than the recorded
balance and proves that each selected item produced the expected accounting consequence — here, starting from the
Zuora Billing invoice register and proving that every invoice created either revenue or a contract liability. An
invoice that created neither is a completeness error in one of the two.

**Refund liability.** An obligation to return consideration to a customer, settled in cash rather than by
performance, measured as the amount of consideration to which the entity does not expect to be entitled (ASC
606-10-32). It is not a contract liability and does not enter the RPO disclosure. AtlasFlow holds $1,200 in account
2230.

**Remaining performance obligation (RPO).** The aggregate amount of the transaction price allocated to performance
obligations that are unsatisfied or partially unsatisfied at the reporting date, disclosed with an explanation of
when the entity expects to recognize it (ASC 606-10-50-13). AtlasFlow disclosed $214,000 at December 31, 2025, of
which $138,900 (64.9%) is expected within twelve months. It is not the same as "backlog," which has no defined
measurement basis.

**Remeasurement.** The restatement of a balance denominated in a currency other than the reporting entity's
functional currency into that functional currency at the current exchange rate, with the resulting difference
recognized in earnings. It applies to monetary items only and must not be applied to deferred revenue.

**Translation.** The restatement of a foreign entity's functional-currency financial statements into the reporting
currency — assets and liabilities at the closing rate, revenue and expenses at rates in effect when recognized —
with the resulting difference recorded in the cumulative translation adjustment within accumulated other
comprehensive income. AtlasFlow's $(260) movement in deferred revenue is translation, not remeasurement.

**Unbilled receivable.** An amount of revenue recognized for which no invoice has yet been issued. Where the right
to consideration is unconditional it is a receivable; where it is conditional on further performance it is a
contract asset. AtlasFlow presents both in account 1220 under a combined caption of $3,400, of which $380 is a true
receivable.

## Chapter Summary

1. A contract liability arises when consideration has been received *or* is unconditionally receivable before the
   related performance obligation has been satisfied, which is why AtlasFlow's annual-in-advance invoicing creates
   deferred revenue on the invoice date rather than on the collection date.
2. Completeness, not existence, is the dominant relevant assertion for deferred revenue, because the account is
   understated by omission and the omission is the mirror image of a revenue overstatement; at least one procedure
   on the account must therefore run from a population that includes contracts whose recorded balance is nil.
3. The deferred revenue roll-forward — $62,300 opening, $163,750 of billings, $54,900 and $93,300 of revenue
   released, $610 acquired, $(260) of translation, $78,200 closing — is the organizing document for the account, and
   its billings line must be independently sourced rather than derived, or the footing check proves nothing.
4. Two proofs give the roll-forward its evidential force: total revenue released of $148,200 equals revenue per the
   statement of operations, and the $54,900 released from the opening balance is the ASC 606-10-50-8 disclosure,
   recomputable from the subledger and implying an 88.1% conversion of the opening balance.
5. The billings bridge is an identity, not an expectation: $148,200 of revenue plus $15,900 of deferred revenue
   growth, less $610 of acquired balance, plus $260 of translation, equals $163,750 of billings, and less the $1,300
   contract asset increase equals net invoicing of $162,450, which agrees to the Zuora Billing invoice register.
6. The current and noncurrent split is driven by billing frequency and by the scheduled release date, not by
   contract term; recomputing AtlasFlow's $71,300 and $6,900 from scheduled release by quarter produces a declining
   $27,600 : $20,700 : $13,600 : $9,400 series whose shape is itself corroborating evidence.
7. Netting is determined contract by contract, which grosses AtlasFlow's $74,800 net position up to a $78,200
   liability and a $3,400 asset, and the composition of that asset matters because $380 of it is an unconditional
   receivable belonging in the credit-loss pool while $3,020 is a contract asset requiring its own assessment.
8. ASU 2021-08 requires acquired contract liabilities to be measured under ASC 606 as if the acquirer had originated
   the contracts, which is a measurement instruction and not a carryover election: Kestrel Labs' $740 spreadsheet
   balance required $130 of correction to reach the $610 recorded, and recording $740 would have overstated goodwill
   and post-acquisition revenue.
9. A contract liability is non-monetary and is never remeasured, so the two procedures that matter are reading the
   NetSuite revaluation job's account range to confirm accounts 2400, 2405, and 2410 are excluded, and recomputing
   one foreign-currency contract from its inception rate — C-2's £489.0 at 1.2680 gives $620.0, against $627 if the
   £5.4 remeasurement error has been recorded.
10. RPO is a recomputable population, not a footnote: building AtlasFlow's $214,000 from $356,000 of contracted
    value through seven adjustments, and reconciling $77,820 of billed RPO plus $380 of excluded deferred revenue to
    the $78,200 balance sheet amount, is the only procedure capable of finding an error in the query that produced
    it.
11. RPO is the only place in the financial statements where the enforceable term of every contract is implicitly
    asserted, which is why a contract-term judgment must be tested at the disclosure rather than at the balance:
    Pemberton's deferred revenue is $480 under every view, while its RPO contribution is $480 or $1,200 depending on
    the view.
12. Management's draft RPO of $215,860 included $1,860 of non-enforceable amounts on 23 termination-for-convenience
    contracts, of which $800 fell within twelve months; correcting it produced $214,000 and $138,900, and raised the
    twelve-month percentage from 64.7% to 64.9% because the excluded amounts were disproportionately long-dated.
13. Ratio analytics on this account are risk assessment evidence and cannot be substantive, because one percentage
    point of the deferred-revenue-to-ARR ratio is $1,720 — 119% of overall materiality — and an analytic whose
    smallest resolvable unit exceeds materiality cannot detect a material misstatement.
14. The aging is where the errors are: $490 of deferred revenue on 41 expired subscriptions and $620 on 17 dormant
    services engagements are arithmetically impossible balances, and investigating all of them regardless of amount
    produced $74 of understated revenue above the $72 clearly trivial threshold and $26 of misclassification.
15. Account 2230's $1,200 of customer credits and refund liabilities is not a contract liability and does not enter
    RPO, and the one-question test — if the customer never buys again, does AtlasFlow owe cash? — resolves the
    classification, including the $290 of SLA credits that reduce the transaction price through contra revenue
    account 4900 rather than through operating expense.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Identifying performance obligations, standalone selling price, and allocation | Chapter 5 | The allocation determines what amount enters deferred revenue and RPO in the first place; §5.7 works C-1's four-obligation allocation in full |
| Ramped contracts and why the allocated total rather than the invoiced amount is recognized | Chapter 5, §5.9 | The direct cause of the $1,240 of ramp-driven contract assets in account 1220 |
| Contract-term analysis on C-5 Pemberton and its effect on the transaction price | Chapter 5, §5.10 | The revenue-side consequence of the same enforceability judgment that drives the RPO correction here |
| Multi-currency revenue measurement on C-2 | Chapter 5, §5.12 | Establishes the £1,275.0 GBP measurement and the £637.5 invoice from which this chapter's £489.0 liability derives |
| Cut-off testing of revenue transactions and the revenue population | Chapter 4 | The reciprocal test to deferred revenue completeness; a cut-off error appears in both accounts |
| Variable consideration, SLA credits, and refund estimates | Chapter 4, §4.9 | The measurement of the $290 of Northgate SLA credits whose balance sheet consequence lands in account 2230 |
| Accounts receivable, unbilled receivables, and the credit-loss estimate | Chapter 7 | Owns the CECL analysis over the $380 receivable and the impairment assessment over the $3,020 of contract assets |
| Materiality, performance materiality, and the clearly trivial threshold | Chapter 3 | The $1,450 / $940 / $72 framework applied throughout, and the evaluation of disclosure-only misstatements |
| Risk assessment and the identification of significant risks over revenue and deferred revenue | Chapter 2 | Where the assessed inherent risk over completeness that this chapter's procedures respond to is set |
| ITGCs, the RevOps datamart, and weakness W-11 | Chapter 11 | The control environment underlying every extract used here, and the Kestrel ICFR scope-out timing question |
| Evaluating deficiencies and the precision of management review controls | Chapter 14 | The severity framework applied to the RPO review control, and §14.11 on compensating controls the auditor triggered |
| Disclosure checklists, MD&A consistency, and Item 7 | Chapter 18 | The presentation and disclosure procedures over the revenue footnote and the RPO discussion |
| Subsequent events, including the Meridian services dispute of February 9, 2026 | Chapter 19 | The recognized versus non-recognized determination on the $1,240 disputed invoice |
| Auditing accounting estimates, including the input measure on fixed-fee services | Chapter 12 | The retrospective review methodology behind the 8.4% hours over-run and the evaluation of estimate bias |

## Further Reading

- FASB ASC 606, *Revenue from Contracts with Customers*, particularly ASC 606-10-45 on presentation of contract
  balances, ASC 606-10-50-8 through 50-10 on contract balance disclosures, and ASC 606-10-50-13 through 50-15 on
  remaining performance obligations and the practical expedients.
- FASB ASC 606-10-25-1 through 25-3 on the existence of a contract and on enforceable rights and obligations, which
  governs the contract-term analysis underlying the RPO disclosure.
- FASB Accounting Standards Update 2021-08, *Business Combinations (Topic 805): Accounting for Contract Assets and
  Contract Liabilities from Contracts with Customers*, together with ASC 805-20-30 as amended.
- FASB ASC 830, *Foreign Currency Matters*, particularly ASC 830-10-45 on the monetary/non-monetary distinction and
  ASC 830-30 on translation of foreign entity financial statements.
- FASB ASC 326-20 on the current expected credit loss model, for the receivable component of the combined unbilled
  receivable and contract asset caption.
- PCAOB AS 2110, *Identifying and Assessing Risks of Material Misstatement*, on assertion-level risk assessment and
  on understanding the flow of transactions through the revenue and billing systems.
- PCAOB AS 2301, *The Auditor's Responses to the Risks of Material Misstatement*, on designing procedures responsive
  to an assessed completeness risk, and on testing information produced by the entity.
- PCAOB AS 2305, *Substantive Analytical Procedures*, on the precision of the expectation and on the threshold for
  investigating differences.
- PCAOB AS 2401, *Consideration of Fraud in a Financial Statement Audit*, on the identification of accounts
  susceptible to manipulation, which is the framework for the dormant-deferral and expired-term analyses.
- PCAOB AS 2501, *Auditing Accounting Estimates, Including Fair Value Measurements*, as amended effective for audits
  of financial statements for fiscal years ending on or after December 15, 2020, on retrospective review and on
  evaluating indicators of management bias.
- PCAOB AS 2810, *Evaluating Audit Results*, on the accumulation and evaluation of misstatements, including
  qualitative factors relevant to disclosure-only misstatements.
- AICPA AU-C 315, AU-C 330, AU-C 520, and AU-C 540 as the private-company equivalents of the foregoing; AU-C 540 as
  revised is effective for audits of financial statements for periods ending on or after December 15, 2023 and
  imposes a more explicit requirement to evaluate inherent risk factors in an estimate than AS 2501 does.
- SEC Regulation S-X Rule 5-02 on balance sheet captions and the classification of current and noncurrent
  liabilities, and Regulation S-K Item 303 on management's discussion and analysis, which governs the MD&A
  discussion of RPO and billings growth.
- SEC Division of Corporation Finance guidance on the presentation of non-GAAP financial measures, relevant where
  billings, ARR, or RPO growth are presented outside the financial statements.
- The AICPA audit and accounting guide covering revenue recognition, and the AICPA practice aid material addressing
  revenue recognition for software and software-as-a-service entities.
- COSO, *Internal Control — Integrated Framework* (2013), for the evaluation of the precision of the management
  review control over the RPO computation.
