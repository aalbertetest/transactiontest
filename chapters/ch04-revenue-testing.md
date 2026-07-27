# Chapter 4 — Revenue Testing: Foundations and the Order-to-Cash Cycle

> A SaaS subscription is the easiest revenue stream in the world to recognize and one of the hardest to audit.
> Once the contract exists and the tenant is provisioned, the accounting is arithmetic: a fixed amount divided
> by a number of days. That is precisely the problem. Every judgment that matters has been made before the
> revenue engine is touched — whether the contract existed on December 31, whether the signature date on the
> order form is the date it was signed, whether a side letter grants a termination right nobody entered into
> Zuora, whether the $9,700 sold through resellers belongs in revenue at $9,700 or at $13,472, and whether the
> service credits Northgate is entitled to have been recorded at all. AtlasFlow signed 41% of its Q4 annual
> contract value — $25,174 — in the last eight days of December 2025, and in January 2026 the audit committee
> received an email alleging that December deals were papered after the fact. This chapter is about the eight
> days, and about the order-to-cash process that produced them.

## Learning Objectives

- **LO 4.1** Explain the presumption of a fraud risk in revenue recognition and identify the specific
  procedures the presumption requires beyond those the assessed risk would otherwise indicate.
- **LO 4.2** Rank the revenue assertions by importance for a SaaS registrant and defend the ranking, including
  the different treatment of completeness for revenue and for contra-revenue.
- **LO 4.3** Map the order-to-cash cycle from opportunity to cash receipt, identifying at each point the system,
  the field, the control, and what could go wrong.
- **LO 4.4** Apply the ASC 606 contract-existence and enforceability criteria to a specific order form, conclude
  on the contract term, design a search for side agreements, and evaluate whether two contracts with the same
  customer must be combined.
- **LO 4.5** Determine the transaction price of a SaaS contract, including variable consideration, the
  constraint, significant financing, and consideration payable to a customer.
- **LO 4.6** Recompute a service-level-agreement credit population from availability data and evaluate the
  completeness of contra-revenue.
- **LO 4.7** Conclude on gross versus net presentation in a reseller arrangement and quantify the effect of the
  alternative conclusion.
- **LO 4.8** Compute revenue on a fixed-fee professional services engagement using an input measure and
  evaluate the effect of a change in the estimate of total hours.
- **LO 4.9** Design a period-end cut-off test, including the population, stratification, attributes, evidence
  sources outside management's control, and the projection of identified misstatements.
- **LO 4.10** Reconcile the revenue subledger to the general ledger and to cash, design a dual-purpose test, and
  audit the revenue disaggregation disclosure including the basis on which categories are assigned.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2110, *Identifying and Assessing Risks of Material Misstatement* | The auditor **should presume** that there is a fraud risk involving improper revenue recognition, and must evaluate which types of revenue and which assertions give rise to it. |
| PCAOB | AS 2301, *The Auditor's Responses to the Risks of Material Misstatement* | Responses to significant risks must include substantive procedures specifically responsive to the risk, including tests of details; requires an element of unpredictability in the procedures performed. |
| PCAOB | AS 2401, *Consideration of Fraud in a Financial Statement Audit* | Required responses irrespective of assessed risk: journal entry testing, retrospective review of estimates, and evaluation of the business rationale of significant unusual transactions. Chapter 17 owns the fraud schemes; Chapter 16 owns journal entries. |
| PCAOB | AS 1105, *Audit Evidence* | Evidence obtained from a knowledgeable source outside the entity, and evidence not subject to management alteration, is more reliable — the reason this chapter uses DocuSign completion certificates and tenant-provisioning logs rather than Salesforce date fields. |
| PCAOB | AS 2305, *Substantive Analytical Procedures* | The requirements a revenue analytic must meet; Chapter 18 develops them. |
| PCAOB | AS 2310, *The Auditor's Use of Confirmation* | Effective for audits of fiscal years ending on or after June 15, 2025, so in force for FY2025; relevant to confirming with the reseller rather than the end customer. Chapter 7 owns confirmations. |
| AICPA | AU-C 240, *Consideration of Fraud in a Financial Statement Audit* | Requires the auditor, **based on a presumption** that there are risks of fraud in revenue recognition, to evaluate which types of revenue, revenue transactions, or assertions give rise to such risks; permits a conclusion that no such risk exists, with documented reasons. |
| AICPA | AU-C 315, *Understanding the Entity and Its Environment and Assessing the Risks of Material Misstatement* (as amended by SAS 145) | Requires separate assessment of inherent risk and control risk; requires understanding the information system and the flow of transactions, which is what §4.3 documents. |
| AICPA | AU-C 330, *Performing Audit Procedures in Response to Assessed Risks* | Requires substantive procedures for each material class of transactions regardless of assessed risk; where the response to a significant risk consists only of substantive procedures, they must include tests of details. |
| AICPA | AU-C 505, *External Confirmations* | Design and control of confirmation requests, including the identity of the confirming party. |
| FASB | ASC 606-10-25 | Step 1 (contract existence: approval, identifiable rights, payment terms, commercial substance, probable collection), the combination criteria, contract modifications, and the transfer-of-control criteria. |
| FASB | ASC 606-10-32 | Step 3: the transaction price, including variable consideration and the constraint, significant financing components, noncash consideration, and consideration payable to a customer. |
| FASB | ASC 606-10-55 | Implementation guidance, including principal-versus-agent, the sales- and usage-based royalty exception for licenses of intellectual property, and the right-to-invoice practical expedient. |
| FASB | ASC 606-10-50 | Disaggregation of revenue, contract balances, and the disclosure of performance obligations. |
| FASB | ASC 340-40 | Costs to obtain a contract; the C-5 termination clause affects the amortization period. Chapter 10 owns the expense. |
| SEC | Regulation S-X, Rule 5-03 | Requires classes of revenue exceeding 10% of total revenue to be stated separately on the face of the income statement. |
| SEC staff | Staff Accounting Bulletin No. 116 | Rescinded portions of SAB Topic 13 on revenue recognition upon adoption of ASC 606; cited to make the point that pre-606 SEC staff revenue guidance should not be relied on. |

**Where the two frameworks differ substantively.** Three differences matter for a reader auditing a private SaaS
company.

1. **The fraud presumption is stated differently, and the difference is real.** AS 2110 directs the auditor to
   presume that there *is* a fraud risk involving improper revenue recognition; the PCAOB standard does not
   provide a mechanism for rebutting the presumption at the revenue-caption level, only for identifying which
   revenue streams and assertions it attaches to. AU-C 240 requires the auditor to *evaluate*, based on a
   presumption of fraud risks in revenue recognition, which types of revenue give rise to them, and it
   contemplates a documented conclusion that a fraud risk does not exist. In practice the difference rarely
   changes the work in a SaaS engagement — §4.1.2 explains why you essentially never rebut it in a subscription
   business — but the documentation differs.
2. **Confirmation requirements.** PCAOB AS 2310 became effective for audits of fiscal years ending on or after
   June 15, 2025 and applies to the FY2025 AtlasFlow audit. It retains a presumption that the auditor will
   confirm accounts receivable, adds requirements addressing cash held by third parties, and addresses the use
   of intermediaries. AU-C 505 and AU-C 330 contain a presumption for receivable confirmation with stated
   exceptions. Chapter 7 develops both.
3. **Group audit mechanics.** AU-C 600 governs component auditor involvement for a private group; PCAOB AS 2101
   as amended and AS 1206 govern audits involving other auditors for an issuer, effective for fiscal years
   ending on or after December 15, 2024. Chapter 3, §3.10 covers the materiality consequence.

## Prerequisites and Chapter Dependencies

Read Chapter 1 for the SaaS business model and the order-to-cash vocabulary, Chapter 2 for the assertion-level
risk assessments this chapter responds to, and Chapter 3 for the thresholds — overall materiality of $1,450,
performance materiality of $940, tolerable misstatement of $705 for the significant-risk revenue populations,
and the clearly trivial threshold of $72 — that determine every extent decision here. This chapter is the
foundation for Chapter 5 (performance obligations, standalone selling price, allocation, modifications, and
usage revenue), Chapter 6 (the deferred revenue balance and the RPO disclosure), Chapter 12 (the revenue
application controls themselves), Chapter 17 (revenue fraud schemes), and Chapter 18 (revenue analytics). Where
this chapter reaches a boundary it says so and stops rather than duplicating.

## 4.1 The presumption of a fraud risk in revenue recognition

### 4.1.1 What the presumption is, and what it is not

AS 2110 requires the auditor to presume that there is a fraud risk involving improper revenue recognition. That
is a presumption about the *existence of a risk*, not a presumption that fraud has occurred, and not a
presumption that the risk attaches to every revenue stream equally. The auditor's job is to determine which
revenue streams, which transactions, and which assertions the risk attaches to, and then to respond.

For AtlasFlow the risk was identified at the assertion level in Chapter 2's risk assessment matrix as follows,
and this chapter's design flows from it.

**Exhibit 4-1. Where the revenue fraud risk attaches, FY2025 (in thousands).**

| Revenue stream | FY2025 amount | Assertion carrying the fraud risk | Why | Tolerable misstatement (Chapter 3, §3.11) |
| --- | --- | --- | --- | --- |
| Core subscription (account 4100) | 104,900 | Occurrence and cut-off | 41% of Q4 ACV signed December 24–31; the VP Sales Operations can modify order-form dates in CPQ; the CRO is compensated on bookings | 705 |
| Insight subscription (account 4110) | 26,700 | Accuracy (allocation) | New SKU with 31 standalone sales and an interquartile price range of 22% of list; a lower Insight standalone selling price accelerates revenue into the current period. Chapter 5 owns it | 705 |
| Usage overage (account 4120) | 4,200 | Completeness and occurrence of the usage data | Usage volumes are produced by the platform, not by a financial system; Q4 overage rose 27.5% sequentially from $1,090 to $1,390. Chapter 5 owns the usage mechanics | 940 |
| Professional services (accounts 4200, 4210) | 12,400 | Accuracy of the input measure | Percentage of completion depends on an estimate of total hours that the delivery manager both prepares and approves | 940 |
| Contra-revenue (account 4900) | (1,900) | **Completeness** | Understating credits overstates revenue; SLA credits require the auditor to build the population from availability data rather than from the ledger | 705 |

Note the last row. In most revenue audits completeness of revenue is a low-risk assertion, because management is
not motivated to understate the top line. That reasoning does not carry over to the contra-revenue account, where
the direction of management's incentive reverses: every dollar of unrecorded credit is a dollar of overstated
revenue. Section 4.6 builds the contra-revenue population from AWS availability data.

### 4.1.2 What the presumption requires

The presumption converts revenue into a **significant risk** for the assertions identified, and a significant risk
carries specific consequences.

1. **Substantive procedures specifically responsive to the risk, including tests of details.** AS 2301 requires
   this and AU-C 330 requires it where the response consists only of substantive procedures. A controls-reliance
   strategy supplemented by a substantive analytical procedure is not a sufficient response to the December
   cut-off risk, however precise the analytic. Section 4.9 designs the test of details.
2. **Evidence from outside management's control.** AS 1105's reliability hierarchy is not merely advisory when the
   risk is that management has altered a date field. The FY2025 cut-off test uses DocuSign envelope completion
   timestamps, AtlasFlow platform tenant-provisioning timestamps, and Salesforce field-history records — all three
   of which record something management did rather than something management asserts.
3. **Unpredictability.** AS 2301 requires an element of unpredictability in the nature, timing, or extent of
   procedures. For FY2025 Brightline (a) performed an unannounced examination of the December 29–31 order-form
   population on January 6, 2026 before management had completed the close, (b) extended cut-off testing to the
   professional services and usage streams, which the prior-year plan had not covered, and (c) confirmed contract
   terms directly with eight customers who had not been part of the receivable confirmation sample.
4. **Procedures that cannot be satisfied by inquiry.** The side-agreement search in §4.4.4 has five elements, only
   one of which is inquiry, because a side letter is precisely the kind of arrangement management would not
   volunteer.
5. **The required fraud responses that apply regardless.** Journal entry testing (Chapter 16), the retrospective
   review of prior-year estimates (Chapter 19), and evaluation of the business rationale for significant unusual
   transactions (Chapter 17). These are additive, not alternatives.

**Can the presumption be rebutted?** In a subscription business, essentially never, and the reason is structural
rather than judgmental. Rebuttal requires the auditor to conclude that improper revenue recognition presents no
fraud risk. AtlasFlow's revenue is recognized ratably from a start date, which means that the single most
consequential input — the date — is a field in a customer relationship management system that a sales operations
executive can edit, and that the amount of revenue produced by moving it is $69 per day for every $25,174 of ACV.
Add compensation tied to bookings, a metric-driven equity plan, and a quarter in which 41% of the value arrived in
eight days, and there is no version of the analysis that concludes the risk is absent. Arithmetic: $25,174 ÷ 365 =
$68.97 of revenue per day.

## 4.2 Revenue assertions and which ones matter in SaaS

**Exhibit 4-2. Revenue assertions ranked for a SaaS registrant.**

| Rank | Assertion | Why it ranks here for AtlasFlow | Where it is tested |
| --- | --- | --- | --- |
| 1 | **Cut-off** (sometimes presented within occurrence) | The ratable model makes the start date the whole answer, and the bookings distribution concentrates the exposure into eight days. Every dollar of ACV dated one month early produces $2.74 of FY2025 revenue per $1,000 of ACV | §4.9 |
| 2 | **Occurrence** (the transaction happened and pertains to the entity) | Fictitious contracts, contracts with no enforceable rights, contracts subject to an undisclosed contingency in a side letter, and contracts where collection is not probable | §4.4 |
| 3 | **Accuracy** (recorded at the appropriate amount) | The transaction price (§4.5) and the allocation across performance obligations (Chapter 5). For AtlasFlow the allocation is the larger exposure because of the Insight standalone selling price | §4.5 and Chapter 5 |
| 4 | **Classification** (recorded in the proper accounts) | Subscription versus professional services drives gross margin, which is the metric SaaS investors use to judge product quality; gross versus net drives the top line by 2.5% | §4.7, §4.12 |
| 5 | **Presentation and disclosure** | Disaggregation (§4.12), contract balances and RPO (Chapter 6) | §4.12 |
| 6 | **Completeness of revenue** | Low risk: management is not motivated to omit revenue. Two exceptions — usage overage, where the population originates in the platform, and unprocessed expansion amendments (Chapter 3's Extended Case Study) | §4.10 as a by-product of the reconciliation |
| 6= | **Completeness of contra-revenue** | High risk, for the reason in §4.1.1. Ranked jointly with completeness of revenue to make the point that the same word carries opposite risk depending on the account's sign | §4.6 |

Two consequences for planning. First, a revenue programme that allocates its effort in proportion to the dollar
size of the assertions will over-test accuracy and under-test cut-off, because accuracy is where the recomputation
work lives and cut-off is where the risk lives. Second, "completeness" cannot be assessed as a single assertion
across the revenue caption; it must be assessed account by account, because account 4900 carries a
completeness risk that accounts 4100 through 4210 do not.

## 4.3 The order-to-cash cycle, end to end

The cycle has ten steps at AtlasFlow. The auditor's interest at each is: which system holds the record, which
field carries the accounting consequence, who can change it, what control addresses that, and what evidence exists
outside the system.

**Exhibit 4-3. The AtlasFlow order-to-cash cycle.**

| # | Process step | System | Fields that carry the accounting consequence | Who can change them | Control | What could go wrong |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Opportunity creation and qualification | Salesforce Sales Cloud | Account, Opportunity Amount, Close Date (forecast) | Account executive | None that matters — this is a forecast | Nothing accounting-relevant yet |
| 2 | Quote configuration and pricing | Salesforce CPQ | Product/SKU, seat quantity, list rate, Discount %, term months, ramp schedule | Account executive; VP Sales Operations (Brett Hallowell) has administrative rights | CPQ price book and the configured discount approval matrix (Chapter 12, §12.6) | Non-catalogue SKU, off-price-book rate, or a ramp entered as three separate lines that the revenue engine treats as three contracts |
| 3 | Approval | Salesforce CPQ approval workflow | Approver identity and timestamp | Configured; the administrator can reassign approvers | Discount thresholds: to 15% Regional VP, 15–25% Chief Revenue Officer, above 25% Chief Financial Officer | Self-approval; approval after signature; approval matrix modified for one deal |
| 4 | Order form generation and execution | Salesforce CPQ → DocuSign | **Signature date**, counterparty signatory, Contract Start Date, Contract End Date | AE uploads wet-ink PDFs; the CPQ date fields are editable | DocuSign envelope completion certificate is system-generated and not editable in Salesforce | Backdating; wet-ink execution outside DocuSign to avoid the timestamp; a side letter executed separately |
| 5 | Order activation and provisioning | Salesforce CPQ → AtlasFlow platform | Tenant creation timestamp, seat entitlement, workflow-run allowance | Platform operations | Provisioning is triggered by activation and logged immutably | Revenue recognized from the contract start date when the customer could not access the service until later — corrected misstatement C-1, $410 across 14 Q1 contracts |
| 6 | Subscription creation and invoicing | Zuora Billing (interface I-1) | Subscription Number, Contract Effective Date, Service Activation Date, rate plan charges, invoice date and amount | Billing Analyst; Revenue Manager | Automated field mapping; I-1 error queue reviewed daily | Amendment fails validation and sits in the error queue unprocessed (Chapter 3, Extended Case Study, $310); invoice date manually overridden |
| 7 | Revenue contract creation and scheduling | Zuora Revenue / RevPro (interface I-2) | Revenue start and end dates, performance obligation identification, allocation, schedule | Daniel Kim owns the configuration; two developers have standing write access (W-6); four local admin accounts exist including a shared one (W-1) | 27 configuration rules; nightly record-count and amount reconciliation | Configuration changed mid-year (February 2025, abbreviated user acceptance testing); manual override of a revenue schedule |
| 8 | Monthly posting to the general ledger | Zuora Revenue → NetSuite (interface I-3) | Journal amount by account: 4100, 4110, 4120, 2400, 2405, 2410 | The Controller can modify the interface mapping and also prepare and post entries (W-13) | Controller reviews and approves the journal before posting; interface totals tie to the RevPro Revenue Contract Summary | Mapping change routes revenue to the wrong account; manual top-side entry outside the interface |
| 9 | Collection and cash application | Zuora Billing; bank feed (interface I-9) | Payment date, amount applied, credit memos | Staff Accountant clears unmatched items | Automated matching; daily reconciliation | Credit memo used to clear an aged balance rather than to record an earned credit; unapplied cash held in suspense |
| 10 | Metric computation | Snowflake RevOps datamart | ARR, NRR, gross retention, customer counts | Broader access than the source systems | No reconciliation to the general ledger for the first three quarters of FY2025 (W-11) | Metrics diverge from the audited statements. Chapter 12, §12.13 |

The three steps that produce almost all of the audit evidence in this chapter are 4, 5, and 6 — execution,
provisioning, and subscription creation — because they are the only three that generate a timestamp AtlasFlow's
finance and sales functions cannot edit.

## 4.4 Step 1 of the five-step model: identifying the contract

### 4.4.1 The five-step model and who owns each step in this book

**Exhibit 4-4. The five-step model applied to contract C-1 (Meridian Health Systems), with ownership.**

| Step | ASC 606 reference | The question | C-1 answer | Owned by |
| --- | --- | --- | --- | --- |
| 1. Identify the contract | 606-10-25-1 to 25-8; combination at 25-9 | Is there an approved arrangement creating enforceable rights and obligations, with identifiable payment terms, commercial substance, and probable collection? | Yes. Order form executed March 12, 2025; 36-month non-cancellable term March 15, 2025 to March 14, 2028; collection probable | **Chapter 4, §4.4** |
| 2. Identify the performance obligations | 606-10-25-14 to 25-22; series guidance at 25-15 | What distinct goods or services has AtlasFlow promised? | Four: Core subscription (a series), Insight subscription (a series, years 2–3 only), implementation, and the workflow-run overage right | Chapter 5, §5.2 |
| 3. Determine the transaction price | 606-10-32-2 to 32-27 | What consideration does AtlasFlow expect to be entitled to? | $3,120 of fixed consideration; the overage is variable and excluded at inception | **Chapter 4, §4.5** |
| 4. Allocate the transaction price | 606-10-32-28 to 32-41 | How is $3,120 allocated across four performance obligations at relative standalone selling price? | Depends on the Insight standalone selling price, which is the FY2025 critical audit matter | Chapter 5, §5.7 |
| 5. Recognize revenue as obligations are satisfied | 606-10-25-23 to 25-37 | When does recognition begin, and over what measure of progress? | Subscription: ratably from the April 2, 2025 provisioning date. Implementation: over time on an hours input measure | **Chapter 4, §4.8 and §4.9** for the start date and the input measure; Chapter 5 for the subscription schedule |

This chapter develops steps 1, 3, and the cut-off and input-measure aspects of step 5. It does not develop
steps 2 and 4, and it does not develop the deferred revenue balance or the remaining performance obligation
disclosure. Where a number in this chapter depends on the allocation, it is computed on the *stated contract
prices* and labelled as such, deliberately, so that the cut-off conclusion does not depend on an allocation
judgment that Chapter 5 has not yet made.

### 4.4.2 The five criteria, applied

ASC 606-10-25-1 requires all five criteria to be met before a contract exists for accounting purposes. Each maps
to a specific procedure.

**Exhibit 4-5. Contract-existence criteria and the evidence that supports each.**

| Criterion | What you inspect | C-1 result | What an unexpected result looks like and what you do next |
| --- | --- | --- | --- |
| The parties have approved the contract and are committed to perform | Executed order form; DocuSign completion certificate; signatory title against the customer's delegation-of-authority evidence; the CPQ approval record | Signed by Meridian's SVP Information Technology on March 12, 2025 at 14:07 CT per the DocuSign certificate; countersigned by AtlasFlow the same day; CPQ approval by Sofia Marchetti, Chief Revenue Officer, March 11, 2025 at 16:42 CT for the 18.0% discount | A wet-ink PDF with no DocuSign envelope: obtain the email transmittal, the counterparty's own copy through confirmation, or the provisioning record; if none exists, the item is an exception. Six of the 57 December items tested had no envelope (§4.9) |
| Each party's rights regarding the goods or services are identifiable | The order form's SKU, seat quantity, workflow-run allowance, and the incorporated master subscription agreement | 320 automation seats; Insight in years 2 and 3; 200,000 workflow runs per year; implementation scope per the statement of work | A "to be determined" scope or an unquantified professional services commitment: no enforceable right exists for that element; exclude it from the transaction price and consider whether the remainder is a contract |
| The payment terms can be identified | Billing schedule and net terms | Core billed annually in advance on each anniversary; implementation 50% on signature and 50% on go-live; net 30 | "Payment terms to be agreed": step 1 fails |
| The contract has commercial substance | Whether the risk, timing, or amount of cash flows will change as a result | Yes | A round-trip: AtlasFlow buys services from the customer in a related transaction of similar amount. Escalate under AS 2401 as a significant unusual transaction; see §4.5.5 and Chapter 17 |
| It is probable AtlasFlow will collect the consideration to which it will be entitled | Credit approval record; payment history; the customer's own financial information; aged balance at the contract date | Meridian is investment grade with a clean payment history | Sundown Media Holdings — see below |

**The collectibility criterion, worked.** *For purposes of this illustration, assume* Sundown Media Holdings
renewed for twelve months on November 1, 2025 at ACV of $640 while $980 of prior invoices sat 94 days past due
and in collections. AtlasFlow recognized $107 of revenue on the renewal in November and December ($640 × 61 ÷ 365
= $106.9) and collected nothing against it.

Step 1 fails. Where collection of the consideration to which the entity will be entitled is not probable at
inception, no contract exists under ASC 606-10-25-1(e), and the guidance in ASC 606-10-25-7 directs the entity to
recognize consideration received as revenue only when specified criteria are met. The $107 is a misstatement. It
exceeds the clearly trivial threshold of $72 (Chapter 3, §3.6) and is accumulated. Note that the *credit loss*
answer is different from the *contract existence* answer: an entity that concludes a contract exists and then
provides for expected credit losses has reached a different conclusion from an entity that concludes no contract
exists, and only one of the two reduces revenue. Chapter 7, §7.8 develops the distinction from the receivable
side.

What would change the conclusion: a prepayment; a parent guarantee; a materially reduced scope with monthly
billing and a termination right on non-payment, which limits AtlasFlow's exposure to one month of consideration
and can make collection of *that amount* probable.

### 4.4.3 Enforceable rights and the contract term: C-5 Pemberton

The contract term for ASC 606 purposes is the period for which enforceable rights and obligations exist — not the
period stated on the order form. C-5 makes the point.

Contract C-5, Pemberton Manufacturing Co., is a 24-month arrangement beginning September 1, 2025 with total
consideration of $1,440, billed annually in advance, containing a clause permitting Pemberton to terminate for
convenience on 30 days' notice with no penalty.

**Exhibit 4-6. C-5 under two views of the contract term (in thousands).**

| Item | Stated 24-month term | Enforceable term of 30 days |
| --- | --- | --- |
| Monthly consideration ($1,440 ÷ 24) | 60 | 60 |
| Transaction price of the accounting contract | 1,440 | 60 |
| FY2025 revenue (September 1 – December 31, 122 days) | 240 | 240 |
| Deferred revenue at December 31, 2025 | 480 (12 months billed less 4 recognized) | 480 |
| Amount included in the RPO disclosure at December 31, 2025 | 1,200 | 60 |
| Amortization period for the $86 capitalized commission | 24 months (contract term) | Period of benefit, 4 years |

The revenue number is identical under both views — $240 either way, because $1,440 over 24 months and $60 per
month describe the same straight line. That is why a termination-for-convenience clause is so often missed: it
does not move revenue. It moves three other things, each owned elsewhere: the RPO disclosure by $1,140
(Chapter 6, §6.11.3, which works an $1,860 RPO overstatement caused by exactly this issue), the commission
amortization period (Chapter 10), and the deferred revenue classification between current and noncurrent
(Chapter 6, §6.5). Verification: 12 months billed × $60 = $720 billed; 4 months recognized × $60 = $240; $720 − $240 =
$480 deferred. RPO under the stated term is $1,440 − $240 = $1,200.

The audit procedure is a population procedure, not a contract procedure: extract the termination clause from all
FY2025 contracts and quantify the exposure. *For purposes of this illustration, assume* the team's contract
review identified 87 FY2025 contracts with unilateral termination-for-convenience rights exercisable on 90 days'
notice or less, with aggregate remaining consideration at December 31, 2025 of $6,140. That population is
four times overall materiality and is handed to Chapter 6.

### 4.4.4 Side agreements

A side agreement is any arrangement that modifies the enforceable rights or obligations in the order form and is
not reflected in the systems that produce revenue. The five-part search below is designed on the premise that
inquiry is the weakest element and must never be the only one.

1. **Read the whole contract file, not the order form.** For C-1 that is the order form, the incorporated master
   subscription agreement, the statement of work, the data processing addendum, and the security exhibit. Look
   for acceptance clauses, contingent effectiveness, most-favoured-customer clauses, unilateral termination
   rights, and future credits. The C-2 Voltaire contract's "renewal credit" of $200 usable only toward a future
   Insight purchase is exactly the kind of clause that lives in an exhibit and creates a material right —
   Chapter 5, §5.4 values it.
2. **Query for documents outside the contract repository.** Extract the Salesforce Files and Notes objects and
   the DocuSign envelope inventory for the customer, and compare the envelope list to the documents in the
   contract repository. An envelope executed on the same day as the order form and not filed with it is the
   single highest-yield indicator of a side letter.
3. **Inquire of people whose incentives differ.** Inquire of the deal desk, of legal, and of the account
   executive separately, and ask about the *deal* rather than about side letters: "what did Meridian ask for that
   is not in the order form, and what did we say?" Then inquire of Brett Hallowell (VP Sales Operations) and
   Sofia Marchetti (Chief Revenue Officer) about the December population as a whole.
4. **Obtain a written representation and make it specific.** A generic representation that there are no side
   agreements is nearly worthless. The FY2025 representation letter names the mechanism: that there are no
   agreements, understandings, or communications, written or oral, that modify the terms of any customer contract
   or grant any right of return, cancellation, acceptance, extension, credit, or price concession not recorded in
   Zuora Billing.
5. **Confirm terms, not just balances, with a sample of customers.** For FY2025 the team confirmed contract term,
   start date, cancellation rights, and the existence of any separate agreement with eight December customers,
   using AS 2310 confirmation procedures, deliberately selecting customers who were *not* in the receivable
   confirmation sample so that the request would not be routed to the same accounts payable clerk. Chapter 7,
   §7.5 owns confirmation mechanics.

If a side agreement is found, the response is not limited to correcting that contract. A single side letter
signed by an account executive with authority to bind AtlasFlow means the population of contracts is not what the
systems say it is, and the team must reconsider whether any controls-reliance conclusion over the revenue cycle
survives.

### 4.4.5 Combining contracts

ASC 606-10-25-9 requires two or more contracts entered into at or near the same time with the same customer, or
with related parties of the customer, to be combined and accounted for as a single contract if any of three
criteria is met. The gateway condition — at or near the same time — is not itself one of the three criteria and
is often overlooked.

**Exhibit 4-7. Combination analysis: C-1 and the Meridian Ambulatory Division order form.**

*For purposes of this illustration, assume* Meridian Health Systems – Ambulatory Division, a separate legal
entity within the Meridian group, executed order form MHS-AMB-2025 on October 6, 2025 with year-one annual
contract value of $1,080 at a 12.0% discount to list, invoiced in full on October 6, 2025.

| Test | Analysis | Conclusion |
| --- | --- | --- |
| Gateway: entered into at or near the same time with the same customer or a related party of the customer | Signed March 12, 2025 and October 6, 2025 — 208 days apart. Different contracting entities within one group, which does satisfy the "related parties" element | **Gateway not met on timing.** The analysis could stop here, but the team performed the three criteria anyway because "at or near the same time" is a judgment and 208 days is not a bright line in the guidance |
| (a) Negotiated as a package with a single commercial objective | Different Meridian sponsor (Chief Nursing Informatics Officer versus SVP Information Technology); different AtlasFlow account executive; neither document references the other; no co-termination and no cross-default | Not met |
| (b) The consideration in one contract depends on the price or performance of the other | C-1 discount 18.0%; Ambulatory discount 12.0%. Neither price is expressed by reference to the other; the CPQ approval records show independent approvals at different authority levels (Chief Revenue Officer for 18.0%, Regional VP for 12.0%) | Not met |
| (c) The goods or services are a single performance obligation | Separate tenants, separate seat pools, separate workflow-run allowances; neither is an input to a combined output | Not met |

**Conclusion: do not combine.** What would change it: an email or a master agreement amendment showing the
October pricing was conditional on the March deal; a single purchase order covering both; a most-favoured-customer
clause in C-1 that the Ambulatory pricing triggers; or a group-level commitment schedule. The team specifically
searched the Meridian Salesforce account for a group commitment document and for any amendment to C-1 dated
between September and November 2025, and found none.

Why it matters arithmetically: had the two been combined, the consideration would have been allocated across the
combined set of performance obligations at relative standalone selling price, and a single blended discount would
have replaced the two contract-specific discounts. The C-1 subscription's CPQ quote shows list consideration of
$2,927 against net consideration of $2,400 — a discount of $527, or 18.0%. The Ambulatory net price of $1,080 at a
12.0% discount implies list consideration of $1,227 ($1,080 ÷ 0.88). Combined, list consideration of $4,154
against net consideration of $3,480 is a blended discount of $674, or 16.2%. Combining would therefore have moved
consideration away from the Ambulatory subscription, which began October 6, 2025, and toward the C-1 elements,
some of which begin in 2026 — accelerating revenue out of FY2025 rather than into it. Chapter 5, §5.7 works
discount allocation.

## 4.5 Step 3: determining the transaction price

### 4.5.1 Fixed consideration

**Exhibit 4-8. Transaction price of contract C-1 at inception (in thousands).**

| Element | Stated consideration | Fixed or variable | In the transaction price at inception? |
| --- | --- | --- | --- |
| Core subscription, year 1 (March 15, 2025 – March 14, 2026) | 600 | Fixed | Yes |
| Core subscription, year 2 (March 15, 2026 – March 14, 2027) | 840 | Fixed | Yes |
| Core subscription, year 3 (March 15, 2027 – March 14, 2028) | 960 | Fixed | Yes |
| Insight subscription, year 2 | 180 | Fixed | Yes |
| Insight subscription, year 3 | 180 | Fixed | Yes |
| Fixed-fee implementation (delivered April – July 2025) | 360 | Fixed | Yes |
| **Total fixed consideration — the transaction price at inception** | **3,120** | | |
| Workflow-run overage above the 200,000-run annual allowance, at $12 per 1,000 runs | Not determinable at inception | Variable | No — see §4.5.3 |

The procedure that supports Exhibit 4-8 is not "agree the total to the order form." It is: agree each line to the
order form, agree the sum to the CPQ quote's net consideration, agree the same total to the Zuora Billing
subscription's aggregate rate plan charge value, and agree it again to the Zuora Revenue contract's total
transaction price. Four systems, one number. If the four do not agree, the difference is where the audit is.

*What an unexpected result looks like.* The most common break is that the Zuora Revenue transaction price differs
from the order form because the ramp was entered as three separate rate plan charges with three effective dates
and the revenue engine treated them as three contracts rather than one. That is not a footing error; it changes
the recognition pattern, because $600 recognized over year one and $840 over year two is not the same as $2,400
recognized ratably over 36 months. Difference in FY2025: $600 × 274 ÷ 365 = $450 under the three-contract view,
against $610 under the single-contract view — a $160 difference on one contract. The February 2025 RevPro
configuration change was deployed specifically to handle ramped contracts, and it was deployed with abbreviated
user acceptance testing, so this is a live risk on 34% of AtlasFlow's ACV. Chapter 12, §12.8 tests the
configuration; Chapter 5, §5.9 tests the ramp recognition.

### 4.5.2 Variable consideration and the constraint

ASC 606-10-32-5 requires an entity to estimate variable consideration using either the expected value method or
the most likely amount method, whichever better predicts the amount of consideration to which the entity will be
entitled, applied consistently to similar contracts. ASC 606-10-32-11 then constrains the estimate to the amount
for which it is probable that a significant revenue reversal will not subsequently occur.

The constraint operates asymmetrically, and this is the point practitioners most often get backwards. Where
variable consideration would *increase* the transaction price — a performance bonus, a volume rebate earned by the
customer's counterparty — the constraint holds the estimate down. Where variable consideration would *decrease* the
transaction price — a service credit, a price concession, a right of return — the constraint has the opposite
practical effect: it requires the entity to reduce the transaction price by the amount it expects to give up, and
optimism about not giving it up is what the constraint is guarding against.

**Exhibit 4-9. Variable consideration in AtlasFlow's FY2025 contract population (in thousands).**

| Type | Where it arises | Population | Estimation method used | FY2025 amount recorded | Where tested |
| --- | --- | --- | --- | --- | --- |
| Service level credits | Uptime SLA with a graduated credit schedule | 214 contracts; C-3 Northgate | Expected value in aggregate; most likely amount for individually identified claims | (780) | §4.6 |
| Price concessions on renewal | Negotiated reductions granted after the renewal is signed | 61 renewals in FY2025 | Expected value using the historical concession rate | (640) | §4.6, within account 4900 |
| Billing corrections and duplicate-invoice credits | Post-invoice adjustments | 412 credit memos | Actual, plus a subsequent-events sweep | (410) | §4.6 |
| Self-serve refunds | 30-day Stripe refund window | 11,400 accounts | Historical refund rate | (70) | Chapter 7, §7.11 |
| Rights of return / satisfaction guarantee | 30-day money-back clause | *For illustration*, 12 contracts with FY2025 revenue of $260; historical exercise rate 2.1% | Expected value: $260 × 2.1% = $5.5 | Nil recorded | Below the $72 clearly trivial threshold; logged, not accumulated |
| Workflow-run overage | Consumption above the contractual allowance | Core contracts | Not estimated at inception; recognized as consumed | 4,200 | Chapter 5, §5.10 |

### 4.5.3 The usage exception that does not apply, and the one that does

AtlasFlow's policy summary describes usage overage as recognized in the month the runs are consumed, citing both a
"right to invoice" practical expedient and treatment as usage-based consideration allocated to the distinct daily
service to which it relates. Both routes exist; one commonly cited route does not apply, and the auditor must know
which one management took.

- **The sales- and usage-based royalty exception in ASC 606-10-55-65 does not apply.** That exception is available
  only for consideration in exchange for a **license of intellectual property**. AtlasFlow's Core offering is a
  hosted multi-tenant service, not a license of intellectual property; the customer never obtains the software.
  A memorandum that cites 55-65 for a SaaS overage has cited the wrong paragraph, and the conclusion may
  nonetheless be right for a different reason — which is worse than being wrong, because it cannot be reviewed.
- **The variable-consideration allocation exception in ASC 606-10-32-40 does apply** if the criteria are met:
  the variable payment relates specifically to a distinct service within a series, and allocating it to that
  distinct service is consistent with the allocation objective. Because AtlasFlow's subscription is a series of
  distinct daily services, overage earned in a given month relates to that month's services.
- **The right-to-invoice practical expedient in ASC 606-10-55-18 also applies** where the amount invoiced
  corresponds directly to the value transferred to date.

Chapter 5, §5.10 tests the usage population, the completeness of the platform's run counts, and the timing of
allowance exhaustion. This chapter's only concern is that the overage is correctly excluded from the transaction
price at inception, which it is: including an estimate of Meridian's overage in the March 2025 transaction price
would have allocated it across all four performance obligations and recognized part of it before any run was
consumed.

### 4.5.4 Significant financing component

ASC 606-10-32-15 requires the promised consideration to be adjusted for the time value of money if the timing of
payments provides the customer or the entity with a significant benefit of financing. ASC 606-10-32-18 provides a
practical expedient: no adjustment where the period between transfer of the good or service and payment is one
year or less.

**The ramp is not a financing component, and here is the computation that tempts people to think it is.**
Discounting C-1's Core payments of $600 at signature, $840 one year later, and $960 two years later at an 8.0%
rate gives $600 + $840 ÷ 1.08 + $960 ÷ 1.1664 = $600 + $777.78 + $822.98 = $2,200.76, which is $199 less than the
$2,400 stated. That $199 is not a financing component. Meridian pays each annual instalment *in advance* of the
service it covers, so at no point is either party extended credit for more than twelve months, and the expedient
in 32-18 applies to every instalment. The ramp exists because the customer's seat adoption ramps; ASC 606-10-32-17
identifies circumstances in which a difference between the promised consideration and the cash selling price
arises for reasons other than financing, and a phased adoption schedule is one of them.

**Where a financing component genuinely could arise.** *For purposes of this illustration, assume* 11 FY2025
contracts were paid fully in advance for 36-month terms, with total upfront payments of $4,860.

**Exhibit 4-10. Quantification of the potential financing component on prepaid multi-year contracts (in thousands).**

| Step | Computation | Amount |
| --- | --- | --- |
| Total upfront payments received | Per the Zuora invoice register, 11 contracts | 4,860 |
| Unearned balance at inception | Equal to the payment | 4,860 |
| Unearned balance at the end of the term | Declines linearly to zero over 36 months | — |
| Average outstanding advance | (4,860 + 0) ÷ 2 | 2,430 |
| AtlasFlow's incremental borrowing rate | Per the revolving credit facility pricing grid | 8.0% |
| Imputed interest over the 36-month term | 2,430 × 8.0% × 3 | 583 |
| Annual effect on revenue and on interest expense | 583 ÷ 3 | 194 |
| Effect on the FY2025 net loss | Revenue +194, interest expense +194 | — |
| Average per contract | 4,860 ÷ 11 = 442 of consideration; 583 ÷ 11 = 53 of imputed interest | 12.0% of contract consideration |

**This is a live judgment and the illustrated answer sits at the permissive end of the defensible range.**
ASC 606-10-32-16 frames significance at the contract level, and imputed interest of 12.0% of contract
consideration is not obviously insignificant to the contract. Management concluded no adjustment was required and
disclosed the policy. Brightline accepted the conclusion on the basis that the aggregate FY2025 effect of $194 is
0.13% of revenue, 20.6% of performance materiality, and has no effect on the net loss — but documented the
computation rather than the conclusion alone, and documented that the answer changes if the prepaid population
grows. **What would move the conclusion:** a longer prepayment period, an incremental borrowing rate above 12%, an
increase in the prepaid population beyond roughly $23,500 (at which point $194 scales to $940 and reaches
performance materiality), or an individual contract large enough that the contract-level significance test
plainly fails. Scaling check: $940 ÷ $194 × $4,860 = $23,545.

### 4.5.5 Consideration payable to a customer

ASC 606-10-32-25 requires consideration payable to a customer to be accounted for as a reduction of the
transaction price unless the payment is in exchange for a distinct good or service transferred to the entity, and
then only to the extent the payment does not exceed the fair value of that distinct good or service. This is the
most frequently missed element of step 3 in a channel business, because the payments are made by marketing, are
coded to sales and marketing expense, and never pass through the revenue process at all.

The audit procedure has to start outside the revenue cycle. Extract the vendor master file and the accounts
payable population, match vendor names and tax identification numbers against the customer master, and examine
every payment to a matched counterparty.

**Exhibit 4-11. Consideration payable to a customer, FY2025 (in thousands).**

| Payment | Counterparty (also a customer) | Amount | Distinct good or service received? | Supported at fair value | Not supported | Correct treatment |
| --- | --- | --- | --- | --- | --- | --- |
| Market development funds | Tessera Partners and six other resellers | 240 | Partly — lead-generation campaigns with deliverable evidence for some programmes | 152 | 88 | $152 in account 6200; **$88 to account 4900** |
| Joint marketing programme | Aeropath Group | 340 | Partly — logo placement and a conference sponsorship | 215 | 125 | $215 in account 6200; **$125 to account 4900** |
| Catering and event services purchased | Calderon Foods | 180 | Yes — three competitive quotes obtained | 180 | — | Account 6300 |
| Cloud security assessment purchased | BlueRidge Insurance | 96 | Yes — priced against a published rate card | 96 | — | Account 6300 |
| **Total examined** | | **856** | | **643** | **213** | |

Arithmetic check: $152 + $88 = $240; $215 + $125 = $340; $643 + $213 = $856; the potential contra-revenue
reclassification is $88 + $125 = **$213**.

Evaluation. The $213 is a **classification** misstatement between revenue and sales and marketing expense with no
effect on the net loss. It is 14.7% of overall materiality of $1,450, 22.7% of performance materiality of $940,
and 2.96 times the clearly trivial threshold of $72, so it is accumulated. Its effect on gross margin is
negligible: gross profit falls to $109,047 and revenue to $147,987, giving 73.687% against the reported 73.725% —
a movement of 0.04 percentage points. Its effect on the channel disaggregation in §4.12 is to reduce the reseller
and systems integrator category by $213, or 1.6% of that category's $12,966. Management declined to reclassify and the item was
accumulated as a classification misstatement; Chapter 19 evaluates it.

*What an unexpected result looks like.* If the unsupported portion had been $2,400 rather than $213, the
conclusion changes in kind, not just in degree: a large unsupported payment to a customer, contemporaneous with a
revenue transaction, is a round-tripping indicator and must be evaluated as a significant unusual transaction
under AS 2401, with the business rationale documented and the matter escalated. Chapter 17, §17.9 develops
reciprocal arrangements.

### 4.5.6 Noncash consideration

ASC 606-10-32-21 requires noncash consideration to be measured at fair value. AtlasFlow received no noncash
consideration in FY2025. The procedure that supports that statement is not inquiry: the team queried the Zuora
payment-method field for any value other than ACH, wire, card, or check across all FY2025 invoices (result: none)
and read the 42 non-standard order forms flagged by legal for any barter, data-sharing, or equity element (result:
none).

## 4.6 Service level credits, rights of return, and contra-revenue

Account 4900 — sales returns, credits, and SLA credits — carries a balance of $(1,900) for FY2025 and is netted
within accounts 4100 through 4120 in the reported subscription revenue figure. It is the account with the highest
completeness risk in the revenue cycle, for the reason given in §4.1.1, and it is the account where the audit
population cannot be built from the ledger.

### 4.6.1 The contractual mechanics: C-3 Northgate

Contract C-3, Northgate Financial Group, is a 12-month arrangement beginning July 1, 2025 with fixed consideration
of $1,920, so the monthly subscription fee is $1,920 ÷ 12 = $160. The uptime service level commitment is 99.9%,
with a graduated credit schedule: 10% of the monthly fee for measured availability between 99.0% and 99.9%, and
25% of the monthly fee for availability below 99.0%. Two incidents in FY2025 triggered credit eligibility, in
August and November. Northgate submitted a claim for $180 in December 2025 and AtlasFlow recorded nothing,
pending "commercial discussions."

**Exhibit 4-12. The Northgate credit measured five ways (in thousands).**

| Measurement | Computation | Amount |
| --- | --- | --- |
| Contractual entitlement, August 2025 | us-east-1 availability 99.42%, in the 99.0%–99.9% band → 10% × $160 | 16 |
| Contractual entitlement, November 2025 | us-east-1 availability 98.71%, below 99.0% → 25% × $160 | 40 |
| **Total contractual entitlement** | | **56** |
| Amount claimed by Northgate | Per the December 2025 claim letter | 180 |
| Expected value | 25% × $56 + 45% × $120 + 30% × $180 = $14 + $54 + $54 | 122 |
| Most likely amount | The $120 outcome, being the single most probable | 120 |
| **Amount recorded on audit (part of corrected misstatement C-2)** | | **120** |

**The range of defensible answers is $56 to $180.** The illustrated answer of $120 sits at the middle. The
reasoning: AtlasFlow's own concession history shows it has settled SLA claims above the contractual schedule when
a renewal was within six months, and Northgate's renewal date is June 30, 2026; the amount AtlasFlow "expects to
be entitled to" under ASC 606-10-32-2 is therefore less than the gross fee by more than the contractual credit,
because an expected price concession reduces the transaction price whether or not it is contractually required.
An entity with no history of granting concessions above schedule would record $56 and be right.

Note that the difference between the expected value of $122 and the most likely amount of $120 is $2, which is
2.8% of the clearly trivial threshold. The method choice did not matter here. It would matter if the outcomes
were $56 with 70% probability and $480 with 30% probability, where expected value is $183 and the most likely
amount is $56 — a $127 spread that exceeds the threshold. ASC 606-10-32-8 requires the method to be applied
consistently to similar contracts, so the team tested that the same method was used across the SLA population
rather than selected contract by contract.

**Presentation.** The credit is a reduction of the transaction price, so it is contra-revenue in account 4900 with
the liability in account 2230 (customer credits and refunds payable, $1,200 at December 31, 2025). It is not an
operating expense and it does not belong in account 2200. The team inspected the FY2025 activity in account 2230
to confirm the routing and found the $290 correction posted there.

### 4.6.2 Building the population from availability data

The completeness of account 4900 cannot be tested by examining what is in it. The population must be built from
outside the accounting records.

**Exhibit 4-13. FY2025 monthly platform availability by region (percent).**

| Month | us-east-1 | eu-west-1 | Below the 99.9% commitment? |
| --- | --- | --- | --- |
| January | 99.98 | 99.99 | No |
| February | 99.99 | 99.97 | No |
| March | 99.97 | 99.98 | No |
| April | 99.99 | 99.96 | No |
| May | 99.96 | 99.99 | No |
| June | 99.98 | 99.95 | No |
| July | 99.95 | 99.98 | No |
| **August** | **99.42** | **99.88** | **Yes — both regions (one multi-region incident)** |
| September | 99.97 | 99.99 | No |
| October | 99.99 | 99.97 | No |
| **November** | **98.71** | 99.96 | **Yes — us-east-1 only** |
| December | 99.96 | 99.98 | No |

**Exhibit 4-14. Recomputation of the maximum contractual credit entitlement, FY2025 (in thousands).**

| Region | Contracts with the standard SLA schedule | Aggregate monthly subscription fee | August band | August credit | November band | November credit | Total |
| --- | --- | --- | --- | --- | --- | --- | --- |
| us-east-1 | 168 | 4,180 | 99.42% → 10% | 418 | 98.71% → 25% | 1,045 | 1,463 |
| eu-west-1 | 46 | 960 | 99.88% → 10% | 96 | 99.96% → none | — | 96 |
| **Total** | **214** | **5,140** | | **514** | | **1,045** | **1,559** |

Arithmetic: $4,180 × 10% = $418; $4,180 × 25% = $1,045; $960 × 10% = $96; $418 + $96 = $514; $514 + $1,045 =
$1,559. The aggregate monthly fee of $5,140 across 214 contracts is 35.9% of AtlasFlow's monthly recurring
revenue implied by ARR of $172,000 ÷ 12 = $14,333, which is a reasonableness check the team performed and
documented.

**Exhibit 4-15. The independent expectation compared to the recorded amount (in thousands).**

| Component | Maximum entitlement | Basis for the expected amount | Expected credit |
| --- | --- | --- | --- |
| 25 contracts providing automatic credits with no customer claim required | 122 | 100% — the credit is owed whether or not the customer asks | 122 |
| 189 contracts requiring a written claim within 30 days of month end | 1,437 | Historical claim rate of 46%, computed over the 11 prior breach months in FY2023–FY2025 | 661 |
| **Total** | **1,559** | | **783** |

| Component of the FY2025 SLA credit charge recorded in account 4900 | Amount |
| --- | --- |
| Credit memos actually issued during FY2025 for FY2025 service periods (management's pre-audit position) | 490 |
| Claims received and unresolved at December 31, 2025, recorded on audit — Northgate $120 and six others $170 (corrected misstatement C-2) | 290 |
| **Total SLA credit charge, FY2025** | **780** |
| Auditor's independent expectation (above) | 783 |
| **Difference** | **3** |

The $3 difference is 4.2% of the clearly trivial threshold of $72 and requires no further work. Note that the
$122 of automatic credits is fully reflected in the $490 of credit memos actually issued, which the team agreed
contract by contract for all 25.

**Exhibit 4-16. Composition of account 4900, FY2025 (in thousands).**

| Component | Amount |
| --- | --- |
| Service level agreement credits (§4.6.1 and §4.6.2) | (780) |
| Goodwill credits and price concessions granted in renewal negotiations | (640) |
| Billing error corrections and duplicate-invoice credits | (410) |
| Self-serve refunds processed through Stripe | (70) |
| **Total account 4900** | **(1,900)** |

### 4.6.3 The eight completeness procedures, and what an unexpected result means

1. **Build the population from availability data, not from the ledger.** Obtain the monthly availability report
   and Exhibit 4-13.
2. **Test the availability data as information produced by the entity.** Agree the monthly figures to the
   underlying AWS CloudWatch availability history and to the incident records in Jira. Then do the procedure
   that is usually skipped: **test that the uptime calculation uses the contractual definition of downtime.**
   Management's availability report excludes all scheduled maintenance windows; the contracts exclude only
   windows notified at least 72 hours in advance and not exceeding four hours per month. The team compared the
   maintenance-window log to the notification records for the August and November months and confirmed that no
   excluded window failed the contractual test. *If unexpected:* if a window had failed the test, availability
   would be lower than reported and the entitlement would rise, potentially moving contracts from the 10% band to
   the 25% band — a change with a leverage factor of 2.5 on the credit.
3. **Extract the SLA clause from all contracts, not a sample.** Confirm that 214 contracts use the standard
   schedule and quantify any negotiated variants separately. *If unexpected:* a negotiated schedule with a lower
   threshold or a higher credit percentage must be computed individually.
4. **Recompute the maximum entitlement** (Exhibit 4-14).
5. **Test the historical claim rate.** Obtain the claim population for the 11 prior breach months, agree the
   numerator to claim correspondence and the denominator to the recomputed entitlement for those months, and
   recompute 46%. *If unexpected:* a claim rate that has risen over time (because customers have become more
   sophisticated or because a customer success team now proactively notifies customers) makes the historical
   average a biased estimator; use the most recent periods.
6. **Sweep subsequent credit memos.** Extract all Zuora credit memos issued between January 1 and February 6,
   2026 and identify those relating to FY2025 service periods. Result: $214 of such credit memos, of which $198
   was already within the $780 accrual and $16 was not. The $16 is below the clearly trivial threshold.
7. **Read the support ticket population for credit requests that never reached billing.** Result: 31 tickets
   tagged "credit request" in FY2025; 27 map to recorded credits and 4 relate to amounts below $10 each.
8. **Inspect account 2230 activity** to confirm credits are routed to contra-revenue rather than to expense, and
   that the year-end balance of $1,200 is supported by identified claims rather than being a general reserve.

*The single most important unexpected result.* If the recomputed entitlement exceeds the recorded amount by more
than the clearly trivial threshold, the next question determines the ICFR conclusion: is the difference a
**measurement** issue (the claim rate is wrong) or a **completeness** issue (contracts were omitted from the
population)? A measurement difference is an estimate matter evaluated within a range. A completeness difference
means AtlasFlow does not know which of its contracts contain an SLA, which is a control deficiency whose
potential magnitude is the whole $1,559 rather than the difference — and Chapter 3, §3.14 explains why potential
magnitude is the relevant measure in the ICFR audit.

## 4.7 Gross versus net: principal versus agent

Nine percent of AtlasFlow's annual contract value is sold through resellers and one global systems integrator. The
presentation question this creates is worth $3,772 of revenue — 2.5% of the reported top line — and it is decided
by two questions asked in strict order. Practitioners who ask only the second question get the right answer by
accident, which is the failure mode the Extended Case Study dissects.

**Question 1: who is the customer?** ASC 606-10-15-3 defines a customer as a party that has contracted with the
entity to obtain goods or services that are an output of the entity's ordinary activities. If the reseller has
contracted to obtain the subscription in order to resell it, the reseller is the customer, the transaction price is
what the reseller has agreed to pay, and the principal-versus-agent guidance is not reached at all. The reseller
discount is not a cost; it is the price.

**Question 2, reached only if the end customer is the customer: does AtlasFlow control the specified service
before it is transferred?** ASC 606-10-55-36 through 55-40 governs. The unit of account is the **specified good or
service** — here the right to the subscription for a stated term and seat count, not "the subscription" in the
abstract. If AtlasFlow controls that right before transfer it is the principal and records the gross end-customer
consideration; if it does not, it is an agent and records the net fee.

**Exhibit 4-17. The control indicators of ASC 606-10-55-39 applied to the Tessera arrangement.**

| Indicator | What you inspect | Tessera facts | Points to |
| --- | --- | --- | --- |
| Primary responsibility for fulfilling the promise | The end-user terms; who owes the uptime commitment; who receives support tickets | AtlasFlow's master subscription agreement is passed through to Cirrus and AtlasFlow owes the 99.9% uptime commitment directly to Cirrus; Cirrus raises support tickets in AtlasFlow's portal | AtlasFlow as principal *if* Cirrus is the customer |
| Inventory risk before transfer | Not meaningful for a hosted service; the analogous question is whether the intermediary is obliged to pay irrespective of resale | Tessera's payment obligation to AtlasFlow is unconditional on the order form's effective date and does not depend on collection from Cirrus | Tessera as the customer |
| Discretion in establishing the price | The reseller agreement's price clause; the sell-through report | Tessera sets the price to Cirrus with no floor, no ceiling, and no most-favoured-customer obligation. AtlasFlow's discretion runs only to the price it charges Tessera | Tessera as the customer |

The three indicators do not vote. ASC 606-10-55-39 describes them as indicators that *may* support the control
assessment; they are not a checklist and they do not override the control conclusion. The reason two of the three
here point to Tessera as the customer while the first points the other way is instructive: the pass-through of
AtlasFlow's own terms is a *product* fact, not a *contracting* fact. Software vendors nearly always pass their
terms through the channel, because they will not host a tenant under someone else's warranty. That does not make
the end customer their customer.

**Exhibit 4-18. AtlasFlow's three channel structures and the presentation each requires (in thousands).**

| Structure | Count | FY2025 revenue as originally recorded | Who is the customer | Subscription presentation | Professional services presentation | Evidence that decides it |
| --- | --- | --- | --- | --- | --- | --- |
| **A. Reseller of record** — the partner contracts with the end customer, sets the price, and owes AtlasFlow irrespective of collection | 39 (C-4 Cirrus/Tessera and 38 similar) | 8,646 | The reseller | Net of the reseller discount: revenue equals the consideration from the reseller | AtlasFlow records none where the reseller delivers implementation under its own contract | The reseller agreement's payment and price clauses; the absence of recourse to the end customer |
| **B. Referral / agency** — AtlasFlow contracts directly with the end customer and pays the partner a referral fee | 3 | 1,054 | The end customer | **Gross** end-customer consideration | Gross, where AtlasFlow delivers | AtlasFlow's own order form signed by the end customer; the referral fee invoice |
| **C. Global systems integrator** — the integrator resells the subscription and separately contracts with the end customer for implementation | 1 (Aeropath Group) | 3,080 | The integrator, for the subscription | Net | None — the integrator's implementation revenue is not AtlasFlow's | The integrator's statement of work with the end customer, obtained through inquiry and confirmation |
| **Total channel revenue** | **43** | **12,780** | | | | |

Arithmetic: $8,646 + $1,054 + $3,080 = $12,780. The reseller population that management analysed in its memorandum
is structures A and B combined — 42 arrangements with $9,700 of FY2025 revenue ($8,646 + $1,054 = $9,700), which
is the population the Extended Case Study works. The Aeropath integrator arrangement is analysed separately
because its facts differ.

**Structure B is recorded incorrectly.** In the three referral arrangements the end customer signed AtlasFlow's
order form, AtlasFlow invoiced the end customer, and AtlasFlow bore the credit risk; the partner earned a 15%
referral fee. Revenue of $1,240 was netted against $186 of referral fees and recorded at $1,054. The correct
presentation is $1,240 of revenue in account 4100 and $186 in account 6200 as an incremental cost of obtaining a
contract, capitalized and amortized under ASC 340-40 (Chapter 10 owns the cost). Management posted the
reclassification, so total revenue as finally reported includes the $1,240 rather than the $1,054, and sales and
marketing expense is $186 higher; the net loss is unchanged. Because the item has no income effect it is recorded on
the classification section of the summary of audit differences rather than in the pre-tax loss subtotal that
Chapter 19 evaluates. Arithmetic: $1,240 × 15% = $186; $1,240 − $186 = $1,054. After the correction the channel
revenue in Exhibit 4-18 is $8,646 + $1,240 + $3,080 = $12,966, which is the figure disclosed in the channel
disaggregation in §4.12.

### 4.7.1 Sell-in versus sell-through

A separate question, frequently conflated with principal-versus-agent: when a reseller is the customer, has a
contract come into existence before the reseller has found an end customer? It has, if the reseller's payment
obligation is unconditional. It has not, if the order form makes the obligation contingent on end-customer
acceptance, because ASC 606-10-25-1 then fails on approval and on enforceable rights.

*For purposes of this illustration, assume* 9 of the 39 structure-A arrangements contain a sell-through clause
under which the reseller owes nothing until the end customer accepts. For 7 of the 9 the end-customer acceptance
date preceded the reseller order date, so nothing turns on the clause. For 2 arrangements with aggregate annual
contract value of $480, AtlasFlow began recognizing revenue on the reseller order date, 46 days before end-customer
acceptance.

Misstatement: $480 × 46 ÷ 365 = $60.5, or **$61**. That is below the clearly trivial threshold of $72 and is
logged rather than accumulated. It is worth logging anyway, because the leverage is visible: the same defect
across all 9 sell-through arrangements, whose aggregate annual contract value is $2,180, would be
$2,180 × 46 ÷ 365 = $275, which is 3.8 times the threshold. *What you do next if the population grows:* extract the
sell-through clause as an attribute for the whole channel population rather than sampling it, and reconcile the
reseller revenue start dates to end-customer acceptance evidence obtained from the reseller.

### 4.7.2 The five procedures that decide the question

1. **Read the reseller agreement, not the order form.** The order form states price and term; the master reseller
   agreement states who owes whom, whether there is recourse, and whether stock rotation or return rights exist.
   For Tessera the team read the 2023 master reseller agreement and its two amendments.
2. **Test the legal-obligor attribute across the whole population.** Extract the counterparty on the executed
   order form for all 43 channel arrangements and compare it to the customer name recorded in NetSuite. Result:
   in 40 of 43 the NetSuite customer is the **end customer** while the legal obligor is the partner — including
   Cirrus Retail Group's $1,510, which appears as the fourth largest receivable at December 31, 2025 but is owed
   by Tessera Partners. That mismatch has two consequences the team followed up: the receivable confirmation must
   be addressed to Tessera (AS 2310 requires the confirming party to be the party with knowledge of the balance;
   Chapter 7, §7.5), and the expected credit loss must be assessed on Tessera's credit standing rather than on
   Cirrus's (Chapter 7, §7.9).
3. **Obtain the sell-through report and test price discretion with numbers.** The partners' quarterly sell-through
   reports show aggregate end-customer consideration for the 42-arrangement population of $13,472 against
   AtlasFlow's recorded $9,700, an average partner margin of 28.0% — and it is the $13,472 that the alternative
   presentation conclusion would put on the top line. Across the population end-customer prices ranged from 6%
   below AtlasFlow's list price to 3% above it, which corroborates genuine discretion. *If unexpected:*
   end-customer prices that equal AtlasFlow's list price on every arrangement suggest the reseller has no
   discretion, which weakens the conclusion that it is a customer rather than an agent. Arithmetic: $9,700 ÷ 0.72 =
   $13,472; $13,472 − $9,700 = $3,772.
4. **Test for recourse in the collection history.** Query the cash application records for any receipt from an
   end customer of a structure-A arrangement. Result: none in FY2025 or FY2024. A single direct collection from an
   end customer would be evidence that AtlasFlow, not the reseller, bears the credit risk.
5. **Confirm the arrangement's terms with the reseller.** The confirmation asks Tessera to confirm that it, not
   Cirrus, owes the balance; that it sets the end-customer price; and that AtlasFlow has granted no return or
   stock-rotation right. This is a terms confirmation, not a balance confirmation, and it is the only procedure in
   the list that obtains evidence from outside the entity.

## 4.8 Professional services revenue and the input method

Professional services is 8.4% of revenue and 30.3% of cost of revenue, so it is small on the top line and large on
gross margin. It is also the only AtlasFlow revenue stream whose recognition depends on an estimate that a single
employee both prepares and approves.

### 4.8.1 Establishing that over-time recognition is available at all

ASC 606-10-25-27 permits over-time recognition only if one of three criteria is met. For an implementation
engagement the relevant one is usually 25-27(c): the entity's performance does not create an asset with an
alternative use to the entity, **and** the entity has an enforceable right to payment for performance completed to
date. Both limbs must hold, and the second is a contract-reading procedure, not an accounting judgment.

AtlasFlow's standard statement of work provides that on termination for convenience the customer will pay for
hours incurred through the termination date at the contracted rates. That is an enforceable right to payment for
performance completed to date and 25-27(c) is met. *What an unexpected result looks like:* a statement of work
that is silent on partial performance, or that provides for payment only on milestone acceptance, fails the second
limb. Revenue on such an engagement is recognized at the point in time control transfers — normally acceptance —
and an engagement 70% complete at year end carries no revenue at all. The team tested this attribute on all 34
fixed-fee engagements in progress at December 31, 2025 and found 2 statements of work with milestone-acceptance
payment terms and no right to payment for partial performance, with cumulative revenue recognized of $118. Those 2
are excluded from the recomputation in Exhibit 4-20 and are dealt with as a separate $118 exception, which
management corrected by deferring the revenue to the 2026 acceptance dates.

### 4.8.2 The input measure, worked: the C-1 Meridian implementation

C-1 includes a fixed-fee implementation of $360, delivered April through July 2025, with an estimate at inception
of 1,600 hours. Revenue is recognized on hours incurred as a percentage of estimated total hours.

**Exhibit 4-19. C-1 implementation revenue by month under the input method (dollars in thousands; hours in whole hours).**

| Month | Hours incurred in the month | Cumulative hours | Estimated total hours | Percentage complete | Cumulative revenue | Revenue for the month |
| --- | --- | --- | --- | --- | --- | --- |
| April 2025 | 320 | 320 | 1,600 | 20.00% | 72.0 | 72.0 |
| May 2025 | 400 | 720 | 1,600 | 45.00% | 162.0 | 90.0 |
| June 2025 | 430 | 1,150 | **1,700** (revised) | 67.65% | 243.5 | 81.5 |
| July 2025 | 590 | 1,740 | 1,740 (complete) | 100.00% | 360.0 | 116.5 |
| **Total** | **1,740** | | | | | **360.0** |

Arithmetic: $360 × 320 ÷ 1,600 = $72.0; $360 × 720 ÷ 1,600 = $162.0, so May's revenue is $162.0 − $72.0 = $90.0;
$360 × 1,150 ÷ 1,700 = $243.5, so June's revenue is $243.5 − $162.0 = $81.5; on completion cumulative revenue is
the full $360.0, so July's revenue is $360.0 − $243.5 = $116.5. The monthly amounts sum to $360.0.

Three features of this schedule are worth more attention than the total.

**The June estimate revision is a change in estimate, not an error.** ASC 606-10-25-35 requires the measure of
progress to be updated to reflect changes in the outcome, and ASC 250 accounts for the change prospectively
through a cumulative catch-up in the period of change. The revision from 1,600 to 1,700 hours *reduced* June's
percentage complete relative to what the old estimate would have produced — $360 × 1,150 ÷ 1,600 = $258.8, so June
revenue would have been $96.8 rather than $81.5, a $15.3 difference. An estimate revision that always moves
revenue in the direction management wants is the pattern to look for; a single revision that reduces revenue is
evidence of a functioning estimate process.

**The overrun does not change the total.** Actual hours of 1,740 exceeded the revised estimate of 1,700. On a
fixed-fee engagement that is a margin problem, not a revenue problem: revenue is capped at the $360 transaction
price. At a fully loaded cost of $196 per hour, cost is 1,740 × $196 = $341, giving a margin of $19, or 5.3% —
consistent with AtlasFlow's overall professional services margin of ($12,400 − $11,780) ÷ $12,400 = 5.0%.

**Not every hour counts.** ASC 606-10-55-21 requires the measure of progress to exclude costs, and by extension
inputs, that do not depict performance. Rework caused by AtlasFlow's own error, and hours incurred on activities
outside the statement of work, must come out of the numerator. The team obtained the engagement's time detail by
activity code and identified 60 hours coded to "remediation — data migration rework." Excluding them from the June
cumulative figure gives $360 × 1,090 ÷ 1,700 = $230.8 against the recorded $243.5, a difference of $12.7 on one
engagement. That is below the clearly trivial threshold, but the attribute matters at the population level, and
§4.8.3 tests it there.

### 4.8.3 Recomputing the population, and where the independent estimate comes from

The estimate of total hours is prepared by the delivery manager who runs the engagement and approved by the same
delivery manager. There is no second approver, and the incentive runs one way: a lower estimate of total hours
raises the percentage complete and pulls revenue forward. Inquiry of the delivery manager is therefore not
evidence about the estimate; it is evidence about what the delivery manager is willing to say.

The independent source exists, and it exists because it was built for another purpose. AtlasFlow's delivery
organization maintains an **estimate-to-complete** field in its resource-management system, updated weekly by
delivery managers so that the staffing forecast is right. It is not an input to the revenue computation, nobody in
finance looks at it, and it is prepared by people whose incentive is to have enough consultants rather than to have
enough revenue. Revised estimated total hours equal cumulative hours incurred plus the estimate-to-complete hours
as of December 31, 2025.

**Exhibit 4-20. Recomputation of percentage-of-completion revenue, fixed-fee engagements in progress at December 31, 2025 (dollars in thousands; hours in whole hours).**

| Engagement | Customer | Fixed fee | Cumulative hours | Estimated total hours per management | Percentage complete per management | Cumulative revenue per management | Revised estimated total hours | Revised percentage complete | Recomputed cumulative revenue | Difference |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PS-2025-041 | Halloran Energy | 420 | 1,120 | 1,600 | 70.00% | 294.0 | 1,480 | 75.68% | 317.8 | 23.8 |
| PS-2025-047 | BlueRidge Insurance | 300 | 640 | 1,000 | 64.00% | 192.0 | 940 | 68.09% | 204.3 | 12.3 |
| PS-2025-052 | Calderon Foods | 260 | 500 | 900 | 55.56% | 144.4 | 840 | 59.52% | 154.8 | 10.4 |
| PS-2025-055 | Winterhill Transit Authority | 240 | 430 | 800 | 53.75% | 129.0 | 760 | 56.58% | 135.8 | 6.8 |
| PS-2025-058 | Voltaire Logistics S.A. | 220 | 300 | 760 | 39.47% | 86.8 | 700 | 42.86% | 94.3 | 7.5 |
| PS-2025-061 | Sundown Media Holdings | 180 | 210 | 600 | 35.00% | 63.0 | 640 | 32.81% | 59.1 | (3.9) |
| PS-2025-063 | Northgate Financial Group | 160 | 180 | 520 | 34.62% | 55.4 | 500 | 36.00% | 57.6 | 2.2 |
| PS-2025-066 | Pemberton Manufacturing Co. | 140 | 120 | 460 | 26.09% | 36.5 | 440 | 27.27% | 38.2 | 1.7 |
| **Eight largest engagements** | | **1,920** | | | | **1,001.1** | | | **1,061.9** | **60.8** |
| 24 other engagements in progress | | 1,142 | | | | 740.9 | | | 775.1 | 34.2 |
| **Total, 32 engagements recomputed** | | **3,062** | | | | **1,742.0** | | | **1,837.0** | **95.0** |

Worked example of one row, PS-2025-041: management's percentage complete is 1,120 ÷ 1,600 = 70.00%, giving
$420 × 70.00% = $294.0. The resource-management system shows 360 estimate-to-complete hours at December 31, so
revised estimated total hours are 1,120 + 360 = 1,480, percentage complete is 1,120 ÷ 1,480 = 75.68%, and
recomputed revenue is $420 × 75.68% = $317.8. The difference is $23.8.

**Evaluation.** Revenue is understated by $95, and the offsetting entry is to the contract asset in account 1220,
which is understated by the same amount because the engagements are billed on milestones rather than on progress.
The misstatement is 1.3 times the clearly trivial threshold and 10.1% of performance materiality. Management
declined to record it on the grounds that the revenue schedule should use the estimate that passed its own
governance process. That is a defensible position about *which* estimate is better, but it is not a reason the
difference is not a misstatement, and the item is accumulated as **U-4** with an income effect of $95.

**The direction of the differences matters more than their size.** Of the 32 engagements recomputed, 27 produced a
difference that increases revenue and 5 produced a difference that decreases it. If management's estimates were
unbiased the split would be closer to even. A 27-to-5 split says management's estimated total hours are
systematically stale in the direction that suppresses the percentage complete only when a downward revision would
be needed — that is, delivery managers revise estimates upward when an engagement is going badly and do not revise
them downward when an engagement is going well. AS 2810 and AU-C 450 require the auditor to evaluate whether the
uncorrected misstatements, individually or in aggregate, indicate possible bias in the preparation of the financial
statements, and this pattern is exactly what that requirement is for. Chapter 19 carries the bias evaluation
forward; Chapter 5, §5.6 shows the same analysis applied to standalone selling price.

**Testing the hours as information produced by the entity.** The numerator is as important as the denominator, and
it is easier to test.

| Attribute | Procedure | FY2025 result |
| --- | --- | --- |
| Completeness | Reconcile hours in the revenue computation to total hours coded to billable project codes in the resource-management system for the year: 61,240 hours | Agreed; 340 hours coded to a closed project code were excluded from both populations |
| Accuracy | Agree a sample of 40 timesheet lines to the individual consultant's approved weekly timesheet and to the engagement's activity-code structure | 40 of 40 agreed |
| Cut-off | Extract the entry timestamp and the work date for every timesheet line with a December 2025 work date; identify lines entered after January 9, 2026 | 1,180 hours entered between January 10 and January 26, 2026 for December work dates, of which 1,140 were included in the December percentage-of-completion computation and 40 were not; effect below the clearly trivial threshold |
| Classification | Test that hours coded to "remediation" and "pre-sales" activity codes are excluded from the numerator | 2,410 remediation hours identified across the population; 1,860 were excluded and 550 were not, which is one of the drivers of the $95 |

### 4.8.4 Time-and-materials revenue and the Meridian dispute

Account 4210 carries $3,100 of time-and-materials revenue. The computation is hours multiplied by the contracted
rate, so the audit is a recomputation plus two attributes: was the rate the contracted rate, and were the hours
authorized.

**Exhibit 4-21. Time-and-materials testing, FY2025 (dollars in thousands unless stated).**

| Attribute | Population and extent | Procedure | Result |
| --- | --- | --- | --- |
| Rate agrees to the statement of work | All 1,842 time-and-materials invoice lines, tested by joining the invoice rate to the statement-of-work rate card in a single query | Recompute rate × hours and compare to the invoiced amount | 1,839 agreed. 3 lines were billed at a senior-consultant rate of $310 per hour against a contracted rate of $265 per hour on 760 hours, overstating revenue by 760 × $45 = $34 (whole dollars: $34,200) |
| Hours authorized by the customer | 60 invoices selected across 22 customers | Inspect the customer-signed timesheet or portal approval | 58 approved; 2 approved by email only, which the statements of work permit |
| Hours are within the contract's not-to-exceed cap | All engagements with a cap, 31 of 74 | Compare cumulative billings to the cap | 2 engagements exceeded the cap by $46 in aggregate; amounts above a not-to-exceed cap are not enforceable and were reversed by management |
| Unbilled hours at year end are recorded | Hours with a December work date not invoiced by January 31, 2026 | Recompute and agree to the contract asset in account 1220 | Agreed; Chapter 6, §6.8 tests the account 1220 balance |

The $34 overstatement is below the clearly trivial threshold and was logged. The $46 above the not-to-exceed caps
was corrected. Both are worth the query time because the query is cheap: joining an invoice rate to a rate card
tests 100% of a population that a sample of 40 would have covered at 2.2%.

**The Meridian invoice, analysed as a transaction-price question.** On February 9, 2026, eleven days before the
planned report date, Meridian Health Systems notified AtlasFlow of a dispute over a $1,240 professional services
invoice. *For purposes of this illustration, assume* the invoice relates to statement of work SOW-2025-118, a
fixed-fee engagement for the Ambulatory Division rollout invoiced in full on December 19, 2025 on the assertion
that phase 1 was complete, and that at December 31, 2025 AtlasFlow had incurred 2,480 hours against an estimate of
6,200, giving cumulative revenue of $1,240 × 40.00% = $496 and a contract liability of $1,240 − $496 = $744.

**Exhibit 4-22. The four questions a disputed invoice raises, and the account each one touches (in thousands).**

| Question | Authority | Answer for SOW-2025-118 | Account affected |
| --- | --- | --- | --- |
| Does the invoice date drive revenue? | ASC 606-10-25-23 | No. Revenue follows progress, so the December 19 invoice produced $496 of revenue and $744 of deferred revenue, not $1,240 of revenue. A team that starts from the invoice will find a misstatement that does not exist | 4200 and 2405 |
| Is the transaction price still $1,240, or does AtlasFlow expect to grant a concession? | ASC 606-10-32-2 and 32-11 | The transaction price is the amount AtlasFlow expects to be entitled to. If it expects to concede $300, the transaction price is $940, cumulative revenue becomes $940 × 40.00% = $376, and revenue falls by $120 | 4200, 2405, and a refund liability in 2230 |
| Is the $496 supported by performance? | ASC 606-10-25-31 | Yes if the 2,480 hours are real, the 6,200-hour estimate is sound, and the statement of work gives an enforceable right to payment for performance to date. All three were tested | 4200 |
| Is the $1,240 receivable collectible? | ASC 326 | A separate question with a separate answer and a different account | 1200 and the allowance |

The last row is the point of the exhibit. A $300 expected price concession and a $300 expected credit loss have
identical cash consequences and completely different financial statements: the concession reduces revenue by $120
and creates a $300 refund liability, while the credit loss leaves revenue untouched and increases the provision
for credit losses by $300. Practitioners reach for the allowance because the receivable is where they noticed the
problem. ASC 606 requires the concession question to be asked first, because a concession the entity expects to
grant is not a credit loss at all.

At the February 20, 2026 report date the matter was unresolved. Management's position — no concession expected,
based on the contemporaneous acceptance evidence for phase 1 and Meridian's investment-grade credit standing — was
accepted for revenue purposes on the evidence obtained, and the receivable-side judgment sits inside the allowance
range that Chapter 7, §7.10 develops and that produces uncorrected misstatement U-2. Chapter 19, §19.4 owns the
subsequent-event evaluation and the disclosure question. **What would move the revenue conclusion:** a written
settlement offer from AtlasFlow before the report date, a credit memo issued in February 2026, or an internal
email quantifying an expected concession. Any of the three would make a concession estimable and would put the
$120 back into the summary of audit differences.

Composition of the Meridian receivable, for orientation: the $2,410 balance at December 31, 2025 comprises the
disputed $1,240 SOW-2025-118 invoice, the $1,080 Ambulatory Division subscription invoice dated October 6, 2025
(86 days after its invoice date at year end and, on net 30 terms, 56 days past due, so it falls in the 31–60 day
bucket of the aging Chapter 7 works; paid January 22, 2026), and $90 of Q4 workflow-run overage invoices. Check:
$1,240 + $1,080 + $90 = $2,410.

## 4.9 Period-end cut-off testing, designed in detail

This is the section the rest of the chapter exists to support. It is documented at WP 3200-22 in the FY2025 file.

### 4.9.1 What the misstatement actually is, and why it is smaller than it looks

AtlasFlow signed $25,174 of annual contract value between December 24 and 31, 2025 — 41% of Q4 bookings. Before
designing anything, compute the exposure, because the number surprises people.

**Exhibit 4-23. Maximum FY2025 revenue exposure of the December 24–31, 2025 bookings population (in thousands).**

| Component | Annual contract value | Days of FY2025 service | FY2025 revenue recognized |
| --- | --- | --- | --- |
| 112 order forms whose recognition start date is on or after the stated execution date | 22,834 | 1 to 8, averaging 5.0 | 312 |
| 6 order forms whose recognition start date precedes the stated execution date (December 1–20 starts) | 2,340 | 12 to 31 | 150 |
| **Total** | **25,174** | | **462** |

Arithmetic: $22,834 × 5.0 ÷ 365 = $313, recorded at $312 on the contract-by-contract computation; the six items are
computed individually in Exhibit 4-26 and sum to $150. Total FY2025 revenue from the entire population is $462,
which is 31.9% of overall materiality of $1,450 and 49.1% of performance materiality of $940. **If every one of the
118 order forms were fictitious, FY2025 revenue would be overstated by less than performance materiality.**

A team that stops there and reduces its extent has made a serious error, because the revenue effect is not where
the exposure lives.

| Exposure | Amount | Multiple of overall materiality | Why |
| --- | --- | --- | --- |
| FY2025 revenue | 462 | 0.3× | Eight days of a twelve-month subscription |
| Remaining performance obligations disclosed at December 31, 2025 | 25,174 | 17.4× | The full annual contract value enters the $214,000 RPO disclosure. Chapter 6, §6.11 |
| Accounts receivable and deferred revenue | 12,840 | 8.9× | The portion invoiced on or before December 31, 2025 grosses up both sides of the balance sheet; $12,840 is 33.3% of gross receivables of $38,600 |
| Capitalized commissions | 1,510 | 1.0× | Commissions at 11.8% of new-business annual contract value are capitalized under ASC 340-40: $12,800 of new business × 11.8% = $1,510. Chapter 10 |
| Disclosed annual recurring revenue and bookings | 25,174 of ACV within ARR of 172,000 | n/a | ARR and the Q4 bookings figure appear in MD&A and drive the ARR-based performance stock units. Chapter 3's Extended Case Study and Chapter 20 |
| Potential magnitude for the ICFR conclusion | 25,174 | 17.4× | A control that does not ensure an order form is executed before revenue begins has a potential magnitude of the whole population, not of the difference found. Chapter 3, §3.14 |

That table is the justification for testing 80.9% of the population by value in a year when the revenue effect
alone would have justified almost nothing.

### 4.9.2 Defining the population — three populations, not one

The risk has three shapes and each needs its own population. Testing only the first is the most common design
defect in cut-off work.

**Population 1 — "was it signed when they say?"** Order forms with a stated execution date between December 24 and
31, 2025. This is the backdating population.

```sql
SELECT o.order_form_id,
       a.account_name,
       o.signature_date,                    -- the alterable field
       o.contract_start_date,
       o.contract_end_date,
       o.annual_contract_value,
       o.total_contract_value,
       o.discount_pct,
       o.approval_user, o.approval_timestamp,
       d.envelope_id, d.envelope_completed_at, -- DocuSign; null means wet ink
       p.tenant_created_at,                    -- platform provisioning log
       z.subscription_number, z.contract_effective_date, z.service_activation_date
FROM   salesforce.order_form o
JOIN   salesforce.account       a ON a.id = o.account_id
LEFT   JOIN docusign.envelope   d ON d.order_form_id = o.order_form_id
LEFT   JOIN platform.tenant     p ON p.order_form_id = o.order_form_id
LEFT   JOIN zuora.subscription  z ON z.order_form_id = o.order_form_id
WHERE  o.signature_date BETWEEN '2025-12-24' AND '2025-12-31'
  AND  o.status = 'Activated'
ORDER  BY o.annual_contract_value DESC;
```

Reconcile the query output to something management did not prepare for you: the row count and the sum of annual
contract value must agree to the Q4 bookings figure the Chief Revenue Officer reported to the board. Result: 118
rows, $25,174, agreeing to the board deck and to the 41% statistic in the draft MD&A ($25,174 ÷ $61,400 = 41.0%).
*If the query returns less than the reported bookings figure*, the difference is either bookings that were reported
but not activated, or an activation status the query excluded — and either answer changes what you test.

**Population 2 — "did it start when they say?"** Contracts with a revenue recognition start date in December 2025,
irrespective of signature date. This catches the contract signed on January 8, 2026 with a December 1, 2025 start
date, which population 1 misses entirely because its signature date is not in the window. Extent: 100% comparison
of the Zuora Revenue start date to the platform provisioning timestamp for all 341 contracts with a December start
date, performed as a data comparison rather than as a sample. Result: 9 contracts with a revenue start date
preceding the provisioning date by more than 3 days, aggregate FY2025 revenue effect $54 — below the clearly
trivial threshold, and a much smaller version of the $410 corrected misstatement C-1, which arose from the same
defect on 14 Q1 contracts.

**Population 3 — "did they hold the door open?"** Order forms executed between January 1 and January 31, 2026 with
a contract start date on or before December 31, 2025. Extent: 100%. Result: 31 order forms executed January 1–15
and 46 executed January 16–31; of the 77, four had December 2025 start dates with aggregate annual contract value of
$1,840 and FY2025 revenue of $46. Because no contract exists before approval under ASC 606-10-25-1, the $46 is a
misstatement; it is below the clearly trivial threshold and was logged, and management corrected all four
recognition start dates prospectively.

### 4.9.3 Stratification, extent, and the variable you stratify on

**Stratify on annual contract value, not on the FY2025 revenue effect.** The revenue effect of every item in
population 1 is between $1 and $31, so stratifying on it produces a single stratum and no information. The
exposures that make the population a significant risk — RPO, receivables, deferred revenue, capitalized
commissions, and the disclosed metrics — all scale with annual contract value.

**Exhibit 4-24. Population 1 stratification and extent.**

| Stratum | Definition | Items | Annual contract value | Items tested | Value tested | Coverage | Basis for the extent |
| --- | --- | --- | --- | --- | --- | --- | --- |
| A | Annual contract value ≥ $180 | 43 | 19,240 | 43 | 19,240 | 100.0% | Individually significant relative to tolerable misstatement of $705 for the significant-risk revenue population (Chapter 3, §3.11) when measured against the RPO and receivable exposures |
| B | Annual contract value < $180 | 75 | 5,934 | 14 | 1,120 | 18.9% | Attribute sample; 90% confidence, tolerable deviation rate 10%, zero expected deviations |
| **Total** | | **118** | **25,174** | **57** | **20,360** | **80.9%** | |

Arithmetic: 43 + 75 = 118 items; $19,240 + $5,934 = $25,174; 43 + 14 = 57 items tested; $19,240 + $1,120 = $20,360;
$20,360 ÷ $25,174 = 80.9%.

**The unpredictability element.** The stratum A population was examined on **January 6, 2026**, unannounced, before
management had completed the December close and before the order-form file had been assembled for the auditors. The
purpose was not efficiency; it was to obtain the documents in the state they were in rather than in the state they
would be in once someone knew which 43 the auditors had selected. AS 2301 requires an element of unpredictability
and this is what it looks like when it is real rather than performative.

### 4.9.4 The eight attributes and the evidence source for each

**Exhibit 4-25. Cut-off attributes, evidence sources, and results for the 57 items tested.**

| # | Attribute | Evidence source | Inside or outside management's control | Exceptions |
| --- | --- | --- | --- | --- |
| 1 | The customer executed the order form on or before December 31, 2025 | DocuSign envelope completion certificate: signer email, IP address, completion timestamp | Outside — the certificate is generated by DocuSign and cannot be edited in Salesforce | **6** |
| 2 | AtlasFlow countersigned on or before December 31, 2025 | Same certificate | Outside | 6 (the same items) |
| 3 | The customer signatory had authority to bind the customer | Signatory title on the order form compared to the customer's published officer list or delegation-of-authority schedule; for 8 items, confirmation | Partly outside | 1 — an order form signed by a procurement analyst; the customer confirmed ratification |
| 4 | Internal approval preceded execution and was at the correct authority level | Salesforce CPQ approval record: approver, timestamp, discount percentage against the approval matrix | Inside — the matrix is administered by the VP Sales Operations | 3 — approval timestamp after the signature timestamp on 3 items; a control deviation, not a misstatement (see §4.9.6) |
| 5 | The revenue recognition start date is the later of the contract start date and the provisioning date | AtlasFlow platform tenant-creation log | Inside, but immutable once written | 0 within population 1; 9 in population 2 |
| 6 | The order-form date fields were not modified after record creation | Salesforce field history for `Signature_Date__c` and `Contract_Start_Date__c` | Outside the reach of the person who made the change, because field history records the old value, the new value, the user, and the timestamp | 4 — all within the 6 exceptions at attribute 1 |
| 7 | No side agreement modifies the arrangement | Salesforce Files and Notes; the DocuSign envelope inventory for the account compared to the contract repository; terms confirmation with 8 customers; the specific representation in the management letter (§4.4.4) | Partly outside | 0 |
| 8 | The Zuora Billing subscription and the Zuora Revenue contract agree to the order form on term, start date, and consideration | Four-way comparison run as a data query on all 118 items | Inside | 2 — term entered as 12 months against 24 on the order form; corrected, no FY2025 revenue effect |

Attribute 6 deserves a note, because it is the attribute most teams do not know exists. Salesforce records field
history for audited fields, including the prior value, the new value, the user, and the timestamp, and a user with
the ability to change a date cannot ordinarily delete the history of having changed it. That makes attribute 6 the
single most efficient procedure in the list: one extract, run across the whole population, tests directly for the
act the fraud risk contemplates.

### 4.9.5 Results, evaluation, and projection

**Exhibit 4-26. The six order forms whose execution date could not be corroborated (in thousands).**

| Order form | Customer | Annual contract value | Stated execution date | Recognition start date | Days in FY2025 | FY2025 revenue | Invoiced by 12/31/2025 | Corroborating evidence sought and result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OF-2025-11842 | Larkspur Diagnostics | 660 | Dec 24, 2025 | Dec 1, 2025 | 31 | 56.1 | 660 | Wet-ink PDF only; field history shows `Contract_Start_Date__c` changed from Jan 1, 2026 to Dec 1, 2025 on Dec 30; no email transmittal located; confirmation not returned |
| OF-2025-11857 | Kelso Freight Systems | 480 | Dec 29, 2025 | Dec 8, 2025 | 24 | 31.6 | 480 | Wet-ink PDF only; email transmittal located but dated Jan 5, 2026; tenant provisioned Jan 9, 2026 |
| OF-2025-11863 | Vantage Point Legal | 420 | Dec 30, 2025 | Dec 10, 2025 | 22 | 25.3 | 420 | Wet-ink PDF only; no email transmittal; confirmation returned confirming the balance but not the execution date |
| OF-2025-11871 | Ridgeline Utilities | 360 | Dec 31, 2025 | Dec 12, 2025 | 20 | 19.7 | 360 | Wet-ink PDF only; field history shows `Signature_Date__c` changed on Jan 2, 2026; tenant provisioned Jan 14, 2026 |
| OF-2025-11884 | Copperline Foods | 240 | Dec 26, 2025 | Dec 15, 2025 | 17 | 11.2 | 180 | Wet-ink PDF only; field history shows a date change on Dec 31; tenant provisioned Dec 22, 2025 |
| OF-2025-11890 | Marsh & Teller LLP | 180 | Dec 31, 2025 | Dec 20, 2025 | 12 | 5.9 | — | Wet-ink PDF only; field history shows a date change on Jan 2, 2026; tenant provisioned Dec 18, 2025 |
| **Total** | | **2,340** | | | | **149.8** | **2,100** | |

Individual arithmetic: $660 × 31 ÷ 365 = $56.1; $480 × 24 ÷ 365 = $31.6; $420 × 22 ÷ 365 = $25.3;
$360 × 20 ÷ 365 = $19.7; $240 × 17 ÷ 365 = $11.2; $180 × 12 ÷ 365 = $5.9. Sum $149.8, carried at **$150** as
uncorrected misstatement **U-3**.

**Provisioning is not corroboration of approval.** Two of the six tenants were provisioned in December 2025, and it
is tempting to treat that as evidence the contract existed. It is not. Provisioning is an act AtlasFlow performs
unilaterally; it evidences that the service was made available, not that the customer had approved a contract.
Under ASC 606-10-25-1 the criterion is approval by both parties, and the only evidence of approval that is not
within AtlasFlow's control is the counterparty's own record — a DocuSign certificate, an email from the customer's
domain, or a confirmation. For these six, none of the three was obtained.

**Evaluation and projection.** All six exceptions fall in stratum A, which was tested at 100%, so $150 is a **known**
misstatement and no projection is required for it. Stratum B produced zero exceptions in 14 items. The upper
deviation limit at 90% confidence with zero observed deviations in a sample of 14 is
1 − 0.10^(1÷14) = 1 − 0.8483 = **15.2%**, which applied to stratum B's $5,934 of annual contract value implies up to
$902 of annual contract value that could be affected — a revenue effect of $902 × 5 ÷ 365 = $12, immaterial, but an
RPO exposure of $902, which Chapter 6 carries. That asymmetry is the whole lesson of §4.9.1 restated
statistically: the sampling risk that matters is not the sampling risk on revenue.

**Management's position and the resolution.** Management declined to reverse the six, asserting that the contracts
were negotiated in December and that the documentation is a formality. The team's response was that the assertion
is unauditable — there is no evidence available that distinguishes a contract negotiated in December and signed in
December from a contract negotiated in December and signed in January — and that the absence of evidence, not the
presence of contrary evidence, is what drives the conclusion. The $150 was accumulated on the summary of audit
differences as U-3 with the note that the amount is the *revenue* effect only, and that $2,340 of annual contract
value and $2,100 of receivables and deferred revenue rest on the same evidence. Chapter 19, §19.6 evaluates it,
including in combination with the January 2026 whistleblower allegation that December deals were papered after the
fact, which Chapter 17 develops.

### 4.9.6 Two things that are not misstatements, and must not be called misstatements

**Attribute 4's three items are control deviations.** An internal approval recorded after the customer's signature
means the discount approval control did not operate for those three items. The contracts are enforceable, the
consideration is correct, and there is no misstatement. What there is instead is a control deviation that feeds the
deficiency evaluation: three deviations in 57 items is a 5.3% observed rate against a 10% tolerable rate, and with
a 90% confidence requirement the upper deviation limit on three deviations in 57 exceeds 10%, so the control cannot
be relied upon at the planned level. Chapter 14 owns the evaluation and Chapter 12 owns the control. Calling a
deviation a misstatement, or a misstatement a deviation, is the single most common terminology error in revenue
workpapers and it produces the wrong conclusion in both directions.

**The wet-ink population is a policy and control matter with its own population.** AtlasFlow's policy requires
execution through DocuSign. The team asked for the FY2025 population of order forms executed outside DocuSign and
received 214 order forms with $9,840 of annual contract value — 6.8% of contracts and 5.7% of annual contract
value. That is not a misstatement of anything. It is a population within which attribute 1 cannot be satisfied from
system evidence, which means the potential magnitude of the related control deficiency is $9,840 rather than $150,
and which means the FY2026 audit plan needs a designed response for wet-ink execution rather than an exception
list. Chapter 3, §3.14 explains why potential magnitude rather than actual misstatement drives the ICFR severity
assessment.

## 4.10 Reconciling the revenue subledger, the general ledger, and cash

### 4.10.1 Subledger to general ledger

Zuora Revenue is the revenue subledger and NetSuite is the general ledger of record. Interface I-3 posts a monthly
summary journal from one to the other. Two things are therefore true and both must be tested: the subledger's total
must reach the ledger, and everything in the ledger that did not come from the subledger must be identified and
explained. The second is where the audit findings are.

**Exhibit 4-27. Revenue subledger to general ledger reconciliation, FY2025 (in thousands).**

| Line | Component | 4100 Core | 4110 Insight | 4120 Usage | 4200 PS fixed | 4210 PS T&M | 4900 Contra | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Zuora Revenue "Revenue Contract Summary," FY2025 | 100,230 | 26,950 | 4,240 | 9,300 | 3,100 | (1,540) | 142,280 |
| 2 | Stripe self-serve daily summary journals (interface I-4), which never pass through Zuora Revenue | 6,100 | — | — | — | — | (70) | 6,030 |
| 3 | Kestrel Labs revenue recognized on the acquired billing spreadsheet before the October 2025 migration to Zuora | 180 | — | — | — | — | — | 180 |
| 4 | Manual journal entry: service level credits accrued on audit (corrected misstatement C-2) | — | — | — | — | — | (290) | (290) |
| 5 | **Total expected in the general ledger (lines 1 + 2 + 3 + 4)** | **106,510** | **26,950** | **4,240** | **9,300** | **3,100** | **(1,900)** | **148,200** |
| 6 | Per the NetSuite trial balance at December 31, 2025 | 106,510 | 26,950 | 4,240 | 9,300 | 3,100 | (1,900) | 148,200 |
| 7 | **Difference** | **—** | **—** | **—** | **—** | **—** | **—** | **—** |

Arithmetic: line 5 for account 4100 is $100,230 + $6,100 + $180 = $106,510; for 4900 it is $(1,540) + $(70) + $(290)
= $(1,900); the total column is $142,280 + $6,030 + $180 − $290 = $148,200. Note that accounts 4100 through 4120 are
stated gross in this reconciliation and the contra-revenue in 4900 is stated separately, whereas the reported
subscription revenue of $135,800 is net: $106,510 + $26,950 + $4,240 − $1,900 = $135,800. Reported total revenue is
$135,800 + $9,300 + $3,100 = $148,200.

Four procedures make the reconciliation evidence rather than arithmetic.

1. **Test the subledger total as information produced by the entity.** The Revenue Contract Summary is a report
   generated by Zuora Revenue from a report definition that Daniel Kim can modify and that two developers have
   standing write access to (weakness W-6). Obtain the report parameters, re-run the report with the auditor
   observing, and reconcile the record count as well as the amount: 3,140 enterprise revenue contracts plus the
   Kestrel contracts migrated in October.
2. **Identify every revenue posting that did not come from interface I-3.** Query the general ledger for postings to
   accounts 4100–4900 by source. Result: interface I-3 accounted for 12 monthly journals; interface I-4 for 365
   daily journals; and **41 manual entries** posted by four users. Of the 41, 34 are the entries the journal entry
   analytics identified as hitting revenue and a non-standard offset account, with absolute value posted of $3,900
   (Chapter 16 owns the analytics). Every one of the 41 was examined. Result: 37 were reclassifications between
   revenue accounts with no net revenue effect, 3 were the C-2 accrual and its two components, and 1 was a $46
   reversal of amounts above a not-to-exceed cap (§4.8.4).
3. **Reconcile by quarter, not only for the year.** A reconciliation that ties for the year and not for each quarter
   conceals an interim misstatement corrected by a later one. Result: Q1 $32,980, Q2 $36,040, Q3 $38,390,
   Q4 $40,790, summing to $148,200 and each agreeing to the quarterly reporting package. Because AtlasFlow is a
   large accelerated filer with quarterly reviews, an interim difference is not merely an internal matter.
4. **Reconcile the disclosure inputs to the same subledger.** The disaggregation table (§4.12), the deferred revenue
   roll-forward (Chapter 6, §6.3), and the ARR and NRR metrics in MD&A (Chapter 20) must all reconcile to the same
   subledger. The ARR and NRR metrics come from the Snowflake RevOps datamart, which was not reconciled to the
   general ledger for the first three quarters of FY2025 (weakness W-11), so this is the reconciliation with the
   highest failure probability in the set.

*What an unexpected result looks like.* A difference at line 7 has exactly four possible causes and they should be
tested in this order: a manual entry the query missed because it was posted to a revenue account through a
non-revenue source; a mapping change to interface I-3, which the Controller can make and which weakness W-13
identifies as unsegregated; a subledger report run with different parameters than the posting; and a top-side entry
made in the consolidation workbook outside NetSuite, of which there were 27 in FY2025 with $6,200 of absolute value.
The fourth is the one that will not appear in any NetSuite query at all, and it is the reason the reconciliation must
end at the reported financial statements rather than at the trial balance.

### 4.10.2 Revenue to cash

Chapter 6, §6.4 builds the billings bridge in full and extends it to cash; this chapter uses it as a completeness
procedure over revenue and states what it can and cannot prove.

**Exhibit 4-28. Revenue to cash collected, FY2025, condensed (in thousands).**

| Line | Component | Amount |
| --- | --- | --- |
| 1 | Total revenue recognized | 148,200 |
| 2 | Increase in deferred revenue ($78,200 − $62,300) | 15,900 |
| 3 | Less deferred revenue assumed with Kestrel, which was not billed | (610) |
| 4 | Add back the foreign currency reduction of deferred revenue, which was not billed | 260 |
| 5 | Less increase in contract assets and unbilled receivables ($3,400 − $2,100) | (1,300) |
| 6 | **Total invoicing, net of credit memos** | **162,450** |
| 7 | Beginning gross accounts receivable ($29,150 + $1,350) | 30,500 |
| 8 | Ending gross accounts receivable ($36,900 + $1,700) | (38,600) |
| 9 | Receivables written off against the allowance ($1,350 + $1,780 − $1,900) | (1,230) |
| 10 | Foreign currency reduction of receivables | (110) |
| 11 | **Cash collected from customers** | **153,010** |

Arithmetic: $148,200 + $15,900 − $610 + $260 − $1,300 = $162,450; $162,450 + $30,500 − $38,600 − $1,230 − $110 =
$153,010. Agree line 11 to customer receipts posted to accounts 1010, 1020, and 1205 through interfaces I-9 and I-4,
excluding interest income of $5,110 posted to account 7100.

**What the reconciliation proves.** It is a genuine completeness procedure in one direction only. Cash collected
that cannot be traced to invoicing, deferred revenue, or a receivable is either unrecorded revenue or a liability,
and there is no third possibility. That makes the bridge the most efficient test available for the risk that an
expansion amendment was billed and collected but never recorded — which is precisely the $310 defect that
Chapter 3's Extended Case Study works, and which surfaces here as unapplied cash rather than as missing revenue.

**What it does not prove, and this is the more important half.** The bridge is blind to overstatement. A fictitious
December invoice creates revenue and a receivable in equal amounts, so line 1 and line 8 both rise and line 11 is
unchanged; the bridge balances perfectly on a population that includes every one of the six order forms in
Exhibit 4-26. A team that treats the bridge as evidence about cut-off has confused an identity for a test. The
bridge is a completeness procedure and the cut-off work in §4.9 is an occurrence and cut-off procedure, and neither
substitutes for the other.

## 4.11 Dual-purpose testing

A **dual-purpose test** uses one sample of items to obtain evidence about the operating effectiveness of a control
and evidence about the monetary correctness of the transactions in the same sample. It is efficient and it is
frequently designed wrongly, in three specific ways.

**Exhibit 4-29. Sample size determination for the FY2025 dual-purpose test over the order-form approval control.**

| Requirement | Basis | Items |
| --- | --- | --- |
| Test of operating effectiveness — the Salesforce CPQ discount approval control, a manual control operating many times per day | Firm methodology, not a professional requirement: 90% confidence, 10% tolerable deviation rate, zero expected deviations, giving 25 items; increased to 40 because the control addresses a significant risk and the population is not homogeneous across the year | 40 |
| Test of details — cut-off, population 1 | The stratified design in Exhibit 4-24 | 57 |
| **Dual-purpose sample size** | **The larger of the two requirements, never the average and never the sum** | **57** |
| Of which drawn from the December 24–31 window | Stratum A 43 items plus stratum B 14 items | 57 |
| Additional items required for the control test's period coverage | 40 control items less the 14 randomly selected stratum B December items that also serve the control test | 26 |
| **Total items examined** | | **83** |

**Design defect 1 — treating the sample size as an average.** The sample size is the larger of the two
requirements. Testing 48 items because 40 and 57 average to 48 satisfies neither objective: it is short of the
substantive design and it has no defensible relationship to any confidence level.

**Design defect 2 — ignoring period coverage.** A sample drawn entirely from December 24–31 provides evidence about
how a control operated during eight days. AS 2201 and AU-C 330 require evidence about operating effectiveness
throughout the period of intended reliance, so 26 additional items were selected from January through November 2025.
This is why the total items examined exceed both individual requirements. Teams that report "we performed a
dual-purpose test on 57 items" and rely on the control for the full year have not tested the control for the full
year.

**Design defect 3 — letting one conclusion contaminate the other.** The three attribute 4 deviations do not reduce
the substantive conclusion on those three contracts, whose consideration and dates were correct. Conversely, the six
attribute 1 misstatements are not automatically six control deviations: the control being tested is the discount
approval control, and it operated on all six. The evidentiary failure at attribute 1 relates to a *different*
control — the requirement that contracts be executed through DocuSign — whose deviation population is the 214
wet-ink order forms in §4.9.6, not the six.

One further consequence, and it is the one that changes audit plans. Where the response to a significant risk
consists only of substantive procedures, AU-C 330 requires those procedures to include tests of details, and AS 2301
requires substantive procedures specifically responsive to the risk. That means the substantive extent for the
December cut-off population was **not** set on an assumption of control reliance and cannot be reduced if the
control operates effectively. Dual-purpose testing on a significant-risk population buys documentation efficiency,
not extent reduction.

## 4.12 The revenue disaggregation disclosure

ASC 606-10-50-5 requires revenue to be disaggregated into categories that depict how the nature, amount, timing,
and uncertainty of revenue and cash flows are affected by economic factors, and ASC 606-10-55-89 through 55-91
illustrate candidate categories. Separately, Regulation S-X Rule 5-03 requires classes of revenue exceeding 10% of
total revenue to be stated separately on the face of the income statement. AtlasFlow's professional services
revenue is 8.4% of total revenue ($12,400 ÷ $148,200), so face presentation is not required by Rule 5-03; AtlasFlow
presents it separately anyway, and having done so must present the related cost of revenue on the same basis, which
it does.

**Exhibit 4-30. AtlasFlow FY2025 revenue disaggregation as disclosed (in thousands).**

| Category | Component | FY2025 | % of total |
| --- | --- | --- | --- |
| By offering | Core subscription | 104,900 | 70.8% |
| | Insight subscription | 26,700 | 18.0% |
| | Usage overage | 4,200 | 2.8% |
| | Professional services — fixed fee | 9,300 | 6.3% |
| | Professional services — time and materials | 3,100 | 2.1% |
| | **Total** | **148,200** | **100.0%** |
| By geography (customer billing address) | United States | 106,900 | 72.1% |
| | Europe, Middle East and Africa | 28,300 | 19.1% |
| | Asia-Pacific | 13,000 | 8.8% |
| | **Total** | **148,200** | **100.0%** |
| By channel | Direct | 135,234 | 91.3% |
| | Reseller and systems integrator | 12,966 | 8.7% |
| | **Total** | **148,200** | **100.0%** |
| By timing of transfer | Over time | 148,200 | 100.0% |
| | At a point in time | — | — |
| | **Total** | **148,200** | **100.0%** |

The totals foot in every category, which is the first thing to check and the least interesting. **The audit of a
disaggregation disclosure is an audit of the categorization attribute, not of the total**, because the total is the
audited revenue figure and cannot be wrong once §4.10 has been performed. Two procedures follow.

**Procedure 1 — reconcile each category to the subledger and identify the source of the tagging.** All four
categories in Exhibit 4-30 are produced from the Snowflake RevOps datamart rather than from Zuora Revenue, which
means each category total depends on a field populated by a Fivetran extract (interface I-8) into an environment
whose access is broader than the source systems and which was not reconciled to the general ledger for three
quarters of FY2025 (weakness W-11). Obtain the query, run it independently, and reconcile the sum to $148,200.

**Procedure 2 — test the attribute that assigns each transaction to a category.** This is where the FY2025 finding
was.

**Exhibit 4-31. Recomputation of the geographic disaggregation on the disclosed basis (in thousands).**

| Region | As originally prepared, on the contracting legal entity | Recomputed on the customer's billing address, which is the disclosed basis | Difference |
| --- | --- | --- | --- |
| United States | 109,400 | 106,900 | (2,500) |
| Europe, Middle East and Africa | 26,300 | 28,300 | 2,000 |
| Asia-Pacific | 12,500 | 13,000 | 500 |
| **Total** | **148,200** | **148,200** | **—** |

The original schedule was built by summing revenue by legal entity — AtlasFlow, Inc. $109,400, AtlasFlow Software
Ltd $26,300, and AtlasFlow Pty Ltd $12,500 — which is a fine basis if that is what the note says. The note said the
categories are based on the customer's billing address. Sixty-one customers headquartered in EMEA and eleven in
APAC contract with the US parent, moving $2,500 out of the United States category. The $2,000 EMEA difference is
1.35% of total revenue, 138% of overall materiality, and 213% of performance materiality; it is a disclosure
misstatement, and Chapter 3, §3.8 explains why a disclosure misstatement is measured against the disclosure it
distorts rather than only against overall materiality. Management corrected the note. Exhibit 4-30 shows the
corrected figures.

*What an unexpected result looks like.* Two variants. First, a category whose basis cannot be recomputed at all
because the tagging field is manually maintained: AtlasFlow's channel category is assigned by a Salesforce picklist
that account executives populate, and 214 contracts had a blank value that a Sales Operations analyst filled in
during the close. That is a manual, unreviewed control over a disclosure, and the response is to recompute the
category from the executed order form's counterparty for the whole channel population rather than to sample the
picklist. Second, a disaggregation that is technically accurate but does not satisfy ASC 606-10-50-5 because the
categories do not depict the economic factors affecting the revenue — for AtlasFlow, disaggregating only by
geography while the material economic distinction is between committed subscription and consumption-based overage.
Judgment varies here and practice varies with it; the question to ask is whether the categories in the note match
the categories management uses in its own MD&A and earnings materials, because a mismatch between the two is both
a disclosure weakness and a Regulation G question that Chapter 20 develops.

Finally, note the interaction with §4.5.5 and §4.7: the uncorrected $213 of unsupported consideration payable to
customers would reduce the reseller and systems integrator category, and the corrected $186 of referral fees
increased it. Neither changes the net loss by a dollar, because each has an equal and opposite effect on sales and
marketing expense, and both change total revenue and the disclosed category.

## Step-by-Step Walkthrough: Testing Contract C-1 (Meridian Health Systems) from the Salesforce Order Form to the General Ledger and Back

You are Amelia Trent, staff on the FY2025 AtlasFlow engagement. Omar Haddad has asked you to prepare WP 3200-08:
the end-to-end test of contract C-1, forward from source to the general ledger and backward from the general ledger
to source. The forward direction tests **completeness** of recording; the backward direction tests **occurrence**.
Staff commonly believe the reverse — get it wrong and you will document two tests and obtain one.

This walkthrough does not recompute the allocation of the $3,120 transaction price across the four performance
obligations. That is Chapter 5's walkthrough, and every figure below is computed on the **stated contract prices**
so that the tie-out does not depend on the Insight standalone selling price.

**Tick-mark legend.**

```text
(a)  Agreed to the executed order form, contract C-1, dated March 12, 2025.
(b)  Agreed to the DocuSign envelope completion certificate, envelope 8f2c-…-41a9.
(c)  Agreed to the Salesforce CPQ quote Q-2025-00418 and its approval record.
(d)  Agreed to the AtlasFlow platform tenant-provisioning log.
(e)  Agreed to the Zuora Billing subscription record and rate plan charges.
(f)  Agreed to the Zuora Billing invoice register.
(g)  Agreed to the Zuora Revenue (RevPro) revenue contract and schedule.
(h)  Agreed to the NetSuite general ledger detail or trial balance.
(i)  Recomputed by the auditor without reference to a client-prepared figure.
(j)  Agreed to the bank statement and cash application record.
(x)  Exception; see the exception summary at WP 3200-08a.
```

**Step 1. Establish the population and the basis of selection.** Obtain the FY2025 revenue contract listing from
Zuora Revenue (3,140 enterprise contracts) and reconcile the record count and total transaction price to the
Revenue Contract Summary used in Exhibit 4-27 before selecting anything. C-1 was selected as an individually
significant multi-element ramped contract, not randomly. *If the listing does not reconcile*, stop: you cannot
conclude anything about a selection from a population you have not established.

**Step 2. Obtain the Salesforce CPQ quote and agree the pricing build-up.** Request quote Q-2025-00418. Fields:
`Product`, `Quantity`, `List_Unit_Price`, `Discount_Pct`, `Net_Price`, `Term_Months`, `Ramp_Schedule`. Result: Core
at 320 automation seats, list consideration $2,927 over the term against net consideration of $2,400, a discount of
$527 or 18.0%; Insight $180 per year for years 2 and 3 at list; implementation $360 fixed fee. Total net
consideration $3,120. Tick (c) and (i). *If unexpected:* a `Net_Price` that is not `List_Unit_Price × Quantity ×
(1 − Discount_Pct)` means the price was overridden outside the price book, which is a control matter (Chapter 12,
§12.6) and a step-3 transaction-price matter.

**Step 3. Inspect the CPQ approval record.** Fields: `Approver`, `Approval_Timestamp`, `Discount_Pct_At_Approval`.
Result: Sofia Marchetti, Chief Revenue Officer, March 11, 2025 at 16:42 CT, 18.0%. Compare to the configured
approval matrix: to 15% Regional VP, 15–25% Chief Revenue Officer, above 25% Chief Financial Officer. Conclusion:
approved at the correct level, before execution. Tick (c). *If unexpected:* an approval timestamp after the
signature timestamp is a control deviation, not a misstatement (§4.9.6); an approval by someone below the matrix
level for the discount is a deviation and a reason to extend attribute 4 testing.

**Step 4. Obtain the DocuSign envelope completion certificate.** This is the only evidence in the walkthrough that
AtlasFlow cannot alter. Fields: signer name, signer email domain, IP address, and completion timestamp. Result:
signed by Meridian's SVP Information Technology on March 12, 2025 at 14:07 CT from a `meridianhealth.com` address;
AtlasFlow countersigned the same day. Tick (b). *If unexpected:* no envelope means the order form was executed
wet-ink, which puts the item in the 214-contract population of §4.9.6 and requires an email transmittal, a
confirmation, or the customer's own executed copy as an alternative.

**Step 5. Test signatory authority.** Compare the signatory's title on the order form to Meridian's published
officer list and to the master subscription agreement's notice-and-authority clause. Conclusion: an SVP of
Information Technology is within the authority the master agreement contemplates. *If unexpected:* an order form
signed by someone without authority is not an approved contract under ASC 606-10-25-1; seek ratification evidence
or a confirmation, and if neither exists, the contract does not exist.

**Step 6. Read the whole contract file, not the order form.** Obtain and read the order form, the incorporated
master subscription agreement, the statement of work, the data processing addendum, and the security exhibit.
Extract and record: the term (36 months), the termination provisions (termination for cause only; no
termination-for-convenience right, unlike C-5), the uptime commitment and credit schedule, the payment terms (net
30), the workflow-run allowance (200,000 per year) and overage rate ($12 per 1,000 runs, in whole dollars), and the
absence of acceptance, most-favoured-customer, and future-credit clauses. Tick (a). *If unexpected:* an acceptance
clause changes the transfer-of-control analysis; a future credit is a material right (Chapter 5, §5.4).

**Step 7. Run the Salesforce field history for the date fields.** Request the audit history for
`Signature_Date__c` and `Contract_Start_Date__c` on the C-1 record. Result: no modifications after record creation
on March 12, 2025. Tick (c). *If unexpected:* a change to either field, with the old value, new value, user, and
timestamp, is direct evidence about the attribute the fraud risk contemplates; four of the six exceptions in
Exhibit 4-26 were found this way.

**Step 8. Conclude on contract existence against all five criteria of ASC 606-10-25-1.** Document each criterion
and the evidence: approval (steps 4 and 5), identifiable rights (step 6), identifiable payment terms (step 6),
commercial substance, and probable collection. For the last, obtain the credit approval record and Meridian's
payment history: no balance more than 30 days past due in FY2024 or FY2023. Conclusion: a contract exists from
March 12, 2025. *If unexpected:* see the Sundown Media illustration in §4.4.2, where the collectibility criterion
fails and the answer is not an allowance but the absence of a contract.

**Step 9. Build the transaction price and agree it to four systems.** Recompute: $600 + $840 + $960 + $180 + $180 +
$360 = $3,120. Agree the $3,120 to the order form (a), the CPQ quote's net consideration (c), the aggregate Zuora
Billing rate plan charge value (e), and the Zuora Revenue contract's total transaction price (g). Confirm that the
overage is excluded at inception (§4.5.3) and that no financing adjustment applies because each instalment is paid
in advance (§4.5.4). *If unexpected:* the most common break is the RevPro transaction price differing because the
ramp was loaded as three rate plan charges with three effective dates and treated as three contracts, which changes
the pattern by $160 on this contract alone (§4.5.1).

**Step 10. Obtain the tenant-provisioning timestamp and determine the revenue start date.** Query the platform
provisioning log for the Meridian tenant. Result: tenant created **April 2, 2025**, 18 days after the March 15
contract start date. Under AtlasFlow's policy, revenue begins on the later of the two, so the revenue start date is
April 2. Tick (d). This is the defect behind corrected misstatement C-1, in which revenue on 14 Q1 contracts had
been recognized from the contract start date rather than the provisioning date, for a total of $410; C-1 Meridian's
share is $600 × 18 ÷ 365 = $30 measured on the year-one fee. *If unexpected:* a provisioning date **before** the
contract start date is not an error — the start date governs — but a provisioning date more than a few days after
it, repeated across a population, is a systematic revenue-acceleration pattern and belongs in population 2 of
§4.9.2.

**Step 11. Agree the Zuora Billing subscription record to the order form.** Fields: `Subscription_Number`,
`Contract_Effective_Date`, `Service_Activation_Date`, `Initial_Term`, `Rate_Plan_Charge` lines with
`Charge_Model`, `List_Price`, `Effective_Start_Date`, and `Effective_End_Date`. Result: three Core ramp charges,
two Insight charges effective from March 15, 2026 and March 15, 2027, one implementation charge, and one usage
charge with a 200,000-run included quantity. Tick (e). *If unexpected:* an Insight charge with an effective start
date in 2025 would recognize revenue for a service the customer did not buy until year 2.

**Step 12. Agree the invoices issued to the billing schedule.** Query the invoice register for the Meridian
account. Result: $600 dated March 12, 2025 (Core year 1, annual in advance); $180 dated March 12, 2025
(implementation, 50% on signature); $180 dated July 28, 2025 (implementation, 50% on go-live); and $90 of overage
invoices in November and December 2025. Total invoiced in FY2025: $1,050. Tick (f) and (i). *If unexpected:* an
invoice dated before the order form's execution date, or an invoice for the full 36-month consideration when the
order form provides for annual billing, changes the receivable and the deferred revenue and may indicate a manual
invoice override.

**Step 13. Confirm the item passed interface I-1 without exception.** Obtain the Salesforce-to-Zuora error queue
for March 2025 and confirm the C-1 activation is not in it. Result: not present. *If unexpected:* an item sitting
in the error queue unprocessed is exactly the failure mode behind the $310 unbilled-amendment misstatement in
Chapter 3's Extended Case Study; obtain the full unresolved queue for the year rather than only the item you were
looking at.

**Step 14. Agree the Zuora Revenue contract header.** Fields: `Revenue_Contract_ID`, `Total_Transaction_Price`,
`POB_Count`, `Revenue_Start_Date`, `Revenue_End_Date`. Result: transaction price $3,120, four performance
obligations, revenue start date April 2, 2025, end date March 14, 2028. Tick (g). *If unexpected:* a revenue start
date of March 15 tells you the provisioning-date correction was not applied to this contract.

**Step 15. Recompute FY2025 revenue on the stated contract prices.** Do this before looking at the RevPro schedule
amount, and write your number down first.

| Element | Computation | FY2025 revenue |
| --- | --- | --- |
| Core subscription | $2,400 straight-line over April 2, 2025 – March 14, 2028, a period of 1,078 days; $2,400 ÷ 1,078 = $2.2263 per day × 274 days | 610 |
| Insight subscription | The service is first provided in year 2, beginning March 15, 2026 | — |
| Fixed-fee implementation | Delivered and accepted April – July 2025; full fee earned (Exhibit 4-19) | 360 |
| Workflow-run overage | Invoiced as consumed in November and December 2025 | 90 |
| **Total FY2025 revenue, contract C-1** | | **1,060** |

Day count: April 2 – December 31, 2025 is 274 days; 2026 and 2027 are 365 each; January 1 – March 14, 2028 is 74
days in a leap year; 274 + 365 + 365 + 74 = 1,078. Tick (i).

**Step 16. Agree your number to the RevPro revenue schedule by account and by month.** Extract the schedule and
compare:

```sql
SELECT s.gl_account, s.period, SUM(s.recognized_amount) AS recognized
FROM   zuora_revenue.revenue_schedule s
WHERE  s.revenue_contract_id = 'RC-0001842'      -- contract C-1
  AND  s.period BETWEEN '2025-01' AND '2025-12'
GROUP  BY s.gl_account, s.period
ORDER  BY s.gl_account, s.period;
```

Result: account 4100 $610, account 4200 $360, account 4120 $90, total $1,060, agreeing to step 15. Tick (g).
*If unexpected:* a difference of a few dollars is a day-count convention (365 versus actual days in the month) and
should be quantified across the population rather than argued about on one contract; a difference of $160 is the
ramp defect from step 9; a difference equal to 18 days of fee is the provisioning defect from step 10.

**Step 17. Recognize that the trace to the general ledger is a summary trace, and do it properly.** Interface I-3
posts a *monthly summary journal*, so there is no C-1 line in NetSuite to agree to. The contract-level tie ends at
the subledger, and the subledger-to-ledger tie is the reconciliation in Exhibit 4-27. Obtain the December 2025
I-3 journal, agree its account-level amounts to the RevPro Revenue Contract Summary for December, and obtain the
Controller's approval evidence for the journal from FloQast. Tick (g) and (h). *If unexpected:* a summary journal
that does not tie to the subledger report for the month is the single highest-value finding available in a revenue
audit, because it means the ledger contains revenue the subledger does not support.

**Step 18. Determine the contract's balance sheet position and agree it.** Total invoiced $1,050 (step 12); total
revenue recognized $1,060 (step 15); the contract is therefore in a net **contract asset** position of $10, which
belongs in account 1220. Agree the $10 to the account 1220 contract-level detail. Tick (h) and (i).

**Step 19. Explain why a 36-month contract billed annually in advance has no deferred revenue at year end.** On a
year-one-fee basis you would expect a contract liability of $600 × 73 ÷ 365 = $120 at December 31, 2025, covering
January 1 through March 14, 2026. Straight-lining the whole $2,400 over the term instead recognizes $610 against
$600 billed, converting an expected $120 liability into a $10 asset — a $130 swing on one contract, entirely
attributable to the ramp. This is why the ramp population matters to Chapter 6 as well as to Chapter 5, and why
contract assets and contract liabilities must be netted at the contract level rather than offset across the
portfolio (Chapter 6, §6.8). *If unexpected:* a contract liability of $120 on this contract tells you the ramp was
not straightened, which is the three-contract error again.

**Step 20. Now reverse the direction, and start from the ledger.** Obtain the NetSuite account 4100 balance of
$106,510 and the general ledger detail behind it. Select the December 2025 I-3 journal line, drill into the RevPro
December detail supporting it, and select the C-1 line of $69.0 for December ($2.2263 per day × 31 days, agreed to
the schedule from step 16). From that single subledger line, work outward to the source documents *without using the
file you built going forward*: the Zuora Revenue contract, the Zuora Billing subscription, the Salesforce order
form, and the DocuSign certificate. Conclusion: the recorded amount originates in an executed contract with an
identified customer. *If unexpected:* a subledger line with no order form behind it is a fictitious revenue finding
and the response is immediate escalation under AS 2401, not an exception note.

**Step 21. Reverse-test the contract asset.** From the account 1220 balance of $3,400, obtain the contract-level
detail, select the C-1 position of $10, and agree it to the difference between the RevPro cumulative revenue and the
Zuora Billing cumulative invoicing for that contract. Tick (h). *If unexpected:* a contract asset that cannot be
expressed as cumulative revenue less cumulative billing for a specific contract is not a contract asset; it is a
plug, and Chapter 6, §6.8 explains what to do about it.

**Step 22. Reverse-test the cash.** From the bank statement for account 1010, select the Meridian receipt of $600
dated April 9, 2025 and the $180 dated April 11, 2025, and agree each to the Zuora invoice, the cash application
record, and the order form. Tick (j). This is the only step in the walkthrough whose evidence originates entirely
outside AtlasFlow, and it corroborates the existence of the customer and the enforceability of the arrangement more
convincingly than any internal document.

**Step 23. Document the conclusion, the exceptions, and the cross-references.** Record: the objective; the assertion
addressed by each step; the tick-mark legend above; the exception summary (none for C-1, other than the
provisioning-date matter within corrected misstatement C-1); cross-references to WP 3200-22 (cut-off), the Chapter 5
allocation workpaper, and Chapter 6's contract-balance testing; and the preparer and reviewer sign-off. A
walkthrough that ends without a stated conclusion on the assertions it addressed is a narrative, not a test.

## Extended Case Study: The Principal-Versus-Agent Conclusion on the Tessera/Cirrus Arrangement

### Background

Roughly 9% of AtlasFlow's annual contract value is sold through resellers and one global systems integrator. In
FY2025 the reseller population comprised 42 arrangements producing $9,700 of revenue as originally recorded. All 42
were recorded **net** of the partner discount. The FY2025 audit was the first in which the channel population
exceeded $9,000 of revenue, and the first in which Brightline was also opining on internal control over financial
reporting, so the accounting conclusion and the control that produced it were both in scope.

The engagement team's initial expectation was that this would be a short piece of work: management had a
technical accounting memorandum, the memorandum reached a conclusion, and the conclusion was the one the team
would have reached. What the team found was a right answer supported by reasoning that did not support it — a
condition that is more dangerous than a wrong answer, because a wrong answer gets corrected and an unreviewable
answer gets repeated.

### The Facts

**The Cirrus arrangement (contract C-4).** Tessera Partners resells AtlasFlow to Cirrus Retail Group. Tessera sets
the end-customer price, takes the credit risk, and holds the contract with Cirrus. AtlasFlow's order form is with
Tessera at a 28% discount to list. Tessera also performs the implementation, under its own statement of work with
Cirrus, using its own consultants.

*For purposes of this illustration, assume* the C-4 order form is a 12-month arrangement beginning December 1, 2025
at consideration to AtlasFlow of $1,510 against list consideration of $2,097 ($1,510 ÷ 0.72 = $2,097), invoiced in
full on December 1, 2025 on net 30 terms. FY2025 revenue is $1,510 × 31 ÷ 365 = $128; deferred revenue at
December 31, 2025 is $1,510 − $128 = $1,382; and the $1,510 receivable appears in the aged trial balance under the
name **Cirrus Retail Group** as the fourth largest enterprise balance, although the party that owes it is Tessera.

**Management's memorandum.** A memorandum authored by Aisha Bello, Director of Technical Accounting, dated
January 14, 2026, concludes: *"AtlasFlow is the principal in the arrangement because it controls the SaaS service
before transfer to the customer and has discretion in establishing the price charged to the reseller. Accordingly,
revenue is recorded net of the reseller discount, which is treated as a reduction of the transaction price rather
than as a cost. The same analysis applies to 41 similar reseller contracts."*

**The alternative conclusion's effect.** The partners' quarterly sell-through reports show aggregate end-customer
consideration for the 42 arrangements of $13,472 against AtlasFlow's recorded $9,700 — an average partner margin of
28.0%. If AtlasFlow's customer were the end customer and AtlasFlow were the principal, revenue would be $13,472 and
the $3,772 difference would be a cost.

### What the Engagement Team Did

The team did not sample. With 42 arrangements the population is small enough to test at 100% on the attributes that
decide the question, and sampling a conclusion that must be right for the whole population is a design error.

**Exhibit 4-32. The five decisive attributes, tested for all 42 arrangements (in thousands).**

| Attribute, and the evidence obtained | Structure A — 39 arrangements | Structure B — 3 arrangements |
| --- | --- | --- |
| Counterparty on AtlasFlow's executed order form, per the order form itself | The partner | The end customer |
| Party obliged to pay AtlasFlow, and whether the obligation is conditional, per the master reseller agreement | The partner, unconditionally on the order-form effective date | The end customer |
| Party that sets the end-customer price, per the price clause and the sell-through report | The partner, with no floor or ceiling; observed end-customer prices from 6% below list to 3% above | AtlasFlow, per its own order form |
| Recourse to the end customer if the partner does not pay, per the reseller agreement | None | Not applicable |
| Receipts collected directly from end customers in FY2025 and FY2024, per the cash application records | None | All |
| **FY2025 revenue as originally recorded** | **8,646** | **1,054** |
| Correct presentation | Net, as recorded — the partner is the customer and $8,646 is the transaction price | **Gross** — the end customer is the customer; revenue $1,240 and a $186 referral fee in sales and marketing |

Four further procedures supported the attribute testing. First, the team read the 2023 Tessera master reseller
agreement and both amendments, rather than only the order form, and specifically searched for stock-rotation and
return rights (none) and for a most-favoured-customer clause (none). Second, it confirmed the terms directly with
Tessera under AS 2310 — that Tessera and not Cirrus owes the balance, that Tessera sets the end-customer price, and
that no return right exists. Third, it tested the sell-through clause population described in §4.7.1, finding a $61
misstatement below the clearly trivial threshold. Fourth, it consulted the national office professional practice
director, Priya Chandrasekhar, on the reseller conclusion, which is documented in the file.

### Analysis

**The conclusion is right.** Tessera is AtlasFlow's customer. It has contracted to obtain the subscription in order
to resell it; its obligation to pay is unconditional and independent of collection from Cirrus; it sets the
end-customer price; and AtlasFlow has no recourse to Cirrus. Under ASC 606-10-15-3 Tessera is the party that has
contracted with AtlasFlow to obtain services that are an output of AtlasFlow's ordinary activities. The transaction
price is what Tessera has agreed to pay, which is $8,646 across the 39 arrangements and $1,510 on C-4. The
principal-versus-agent guidance in ASC 606-10-55-36 through 55-40 is never reached, because that guidance answers
whether an entity is a principal *with respect to its customer*, and AtlasFlow's customer is the reseller.

**The reasoning does not support the conclusion.** Six defects, in descending order of seriousness.

**Exhibit 4-33. Defects in the memorandum's reasoning.**

| # | Defect | Why it matters |
| --- | --- | --- |
| 1 | **The premise argues for the opposite conclusion.** "AtlasFlow is the principal, accordingly revenue is net." Being the principal is the reason to record **gross**. The memorandum's conclusion is inconsistent with its own stated premise | A reviewer who accepts this reasoning will accept net presentation in an arrangement where gross is required, which is what happened to the three structure-B arrangements |
| 2 | **The threshold question is not asked.** The memorandum never identifies who the customer is, which is the question that decides the answer | Without it there is no basis on which the 41 "similar" contracts can be assessed for similarity |
| 3 | **The price-discretion indicator is misstated.** ASC 606-10-55-39 refers to discretion in establishing the price *for the specified good or service to the customer*, not discretion over the price charged to one's own counterparty. Every seller has the latter | An indicator that is satisfied by every arrangement provides no evidence about any arrangement |
| 4 | **The specified good or service is never identified.** The control assessment is asserted rather than performed | The unit of account determines the control analysis; ASC 606-10-55-36 requires it to be identified first |
| 5 | **The population is asserted, not evidenced.** "41 similar contracts" states no attributes and cites no testing | Three of the 42 do not share the attributes, which is how a $186 misclassification survived management's review |
| 6 | **The alternative and its effect are not quantified.** A $3,772 alternative outcome, 2.5% of revenue, is not mentioned | A judgment memorandum that does not state what the other answer would produce cannot be evaluated by a reviewer, an audit committee, or a regulator |

**The effect of the alternative conclusion, quantified.**

**Exhibit 4-34. FY2025 statement of operations under net and gross presentation (in thousands).**

| Line item | As reported, net | Gross, partner margin in sales and marketing | Gross, partner margin in cost of revenue |
| --- | --- | --- | --- |
| Subscription revenue | 135,800 | 139,572 | 139,572 |
| Professional services revenue | 12,400 | 12,400 | 12,400 |
| **Total revenue** | **148,200** | **151,972** | **151,972** |
| Total cost of revenue | 38,940 | 38,940 | 42,712 |
| **Gross profit** | **109,260** | **113,032** | **109,260** |
| Gross margin | 73.7% | 74.4% | 71.9% |
| Sales and marketing | 61,300 | 65,072 | 61,300 |
| Total operating expenses | 133,500 | 137,272 | 133,500 |
| **Loss from operations** | **(24,240)** | **(24,240)** | **(24,240)** |
| **Net loss** | **(21,400)** | **(21,400)** | **(21,400)** |

Arithmetic: $135,800 + $3,772 = $139,572; $148,200 + $3,772 = $151,972; $151,972 − $38,940 = $113,032 and
$113,032 ÷ $151,972 = 74.4%; $38,940 + $3,772 = $42,712 and ($151,972 − $42,712) ÷ $151,972 = 71.9%;
$61,300 + $3,772 = $65,072; $133,500 + $3,772 = $137,272. The net loss is identical under all three presentations,
which is exactly why the question is easy to under-weight and why it must be evaluated against revenue and gross
margin rather than against the bottom line.

Three consequences beyond the income statement. First, disclosed annual recurring revenue: the 42-arrangement
population carries $12,400 of annual recurring revenue on the recorded basis, which grossed up at the 28.0% average
margin is $12,400 ÷ 0.72 = $17,222, raising disclosed ARR from $172,000 to $176,822, an increase of 2.8% — and the
ARR-based performance stock units make that consequential (Chapter 3's Extended Case Study and Chapter 15).
Second, gross margin: SaaS investors read subscription gross margin as a proxy for product quality, and a 0.7 or
1.8 percentage point movement in it is not noise at the multiples AtlasFlow trades on. Third, the receivable: the
$1,510 recorded under Cirrus's name is owed by Tessera, which changes the addressee of the confirmation (Chapter 7,
§7.5) and the counterparty whose credit is assessed under ASC 326 (Chapter 7, §7.9).

**The control implication.** AtlasFlow's control over non-routine accounting conclusions is described as "technical
accounting memoranda are prepared by the Director of Technical Accounting and reviewed by the Chief Accounting
Officer." The memorandum was prepared and it was reviewed, and it contains a conclusion inconsistent with its own
premise, an untested population assertion, and no quantification of the alternative. The control did not operate
effectively.

Severity is a judgment and practice varies. The team assessed it as a **significant deficiency**, and the range of
defensible answers runs from a control deficiency to a material weakness:

- *Deficiency only:* the accounting outcome for 39 of 42 arrangements was correct, and the misclassified $186 is
  well below overall materiality of $1,450.
- *Significant deficiency (the illustrated answer):* the potential magnitude is $3,772, which is 2.6 times overall
  materiality, and the deficiency lies in the review of accounting conclusions rather than in a single
  computation — so its potential effect is not confined to the channel population.
- *Material weakness:* if the same review process had also produced the standalone selling price memorandum that
  supports the FY2025 critical audit matter (Chapter 5), a reasonable person might conclude there is a reasonable
  possibility that a material misstatement would not be prevented or detected on a timely basis. The team
  considered this and concluded that the standalone selling price memorandum, whatever its other weaknesses,
  identified its population and quantified its alternatives, so the two did not aggregate to a material weakness.

*What would move the assessment to a material weakness:* a second memorandum in the same population with a
reasoning defect of the same kind, or a misclassification whose effect exceeded overall materiality.

### Resolution and Conclusion

1. **Presentation for the 39 structure-A arrangements is unchanged.** Net is correct, on reasoning the team
   documented independently rather than by reference to management's memorandum.
2. **The three structure-B arrangements were reclassified.** Revenue increased by $186 to $1,240 and sales and
   marketing expense increased by $186, with no effect on the net loss. Management posted the entry.
3. **The channel disaggregation category was corrected** to $12,966 (§4.12).
4. **The receivable confirmation for the channel population was addressed to the resellers**, not to the end
   customers whose names appear in the aged trial balance.
5. **Management rewrote the memorandum**, identifying the customer, the specified good or service, the attributes
   defining the population, the evidence that the population shares them, and the $3,772 effect of the alternative
   conclusion.
6. **A significant deficiency was communicated** in writing to the audit committee relating to the review of
   accounting conclusions for non-routine arrangements.
7. **The $61 sell-through misstatement was logged** below the clearly trivial threshold and the attribute was added
   to the FY2026 plan as a population-level extract.

### Workpaper Extract

```text
=====================================================================================
BRIGHTLINE LLP                                            WORKPAPER INDEX: WP 3200-14
AtlasFlow, Inc.  —  Integrated audit, year ended December 31, 2025
=====================================================================================
SUBJECT:   Principal versus agent and gross versus net presentation — reseller
           and systems integrator channel population (42 arrangements, $9,700)

PREPARED BY:   Jae-won Park (JP)                          DATE PREPARED:   02/02/2026
REVIEWED BY:   Omar Haddad (OH), Manager                  DATE REVIEWED:   02/06/2026
2nd REVIEW:    Grace Lindqvist (GL), Senior Manager       DATE REVIEWED:   02/11/2026
PARTNER:       Dana Whitcombe (DW)                        DATE REVIEWED:   02/17/2026
CONSULTATION:  Priya Chandrasekhar, National Office PPD   DATE:            02/09/2026

-------------------------------------------------------------------------------------
PURPOSE
-------------------------------------------------------------------------------------
To conclude on (1) whether AtlasFlow's customer in each channel arrangement is the
partner or the end customer, (2) whether subscription revenue is properly presented
net of the partner discount, (3) whether professional services performed by a partner
are properly excluded from revenue, and (4) the effect of the alternative conclusion.
Assertions addressed: classification; accuracy; presentation and disclosure.
Risk addressed: Chapter 2 risk assessment matrix, revenue classification (moderate
inherent risk, control risk not relied upon for non-routine accounting conclusions).

-------------------------------------------------------------------------------------
SOURCE OF INFORMATION
-------------------------------------------------------------------------------------
1. Executed order forms, all 42 arrangements (Salesforce contract repository).
2. Tessera Partners master reseller agreement dated 04/18/2023 and amendments 1 and 2.
3. Partner quarterly sell-through reports, Q1-Q4 2025 (obtained from the partners
   directly by the engagement team; not routed through AtlasFlow).
4. Cash application detail, accounts 1200 and 1205, FY2024 and FY2025 (Zuora Billing).
5. Zuora Revenue revenue contract listing for the 42 arrangements.
6. Management memorandum "Reseller Arrangements — ASC 606 Principal/Agent Analysis,"
   A. Bello, dated 01/14/2026.
7. Confirmation reply from Tessera Partners received 02/04/2026 (WP 3200-14a).

Information produced by the entity: items 1, 4, and 5. Completeness of item 1 tested by
agreeing the 42-arrangement count and $9,700 to the channel revenue category in the
Snowflake RevOps datamart and to account 4100 detail (WP 3200-14b). Accuracy tested by
agreeing 42 of 42 order-form counterparties to the executed PDF.

-------------------------------------------------------------------------------------
PROCEDURES PERFORMED
-------------------------------------------------------------------------------------
P1  Tested five decisive attributes for 42 of 42 arrangements (100%): order-form
    counterparty; conditionality of the partner's payment obligation; who sets the
    end-customer price; recourse to the end customer; direct end-customer receipts.
P2  Read the Tessera master reseller agreement and both amendments in full; searched
    specifically for stock-rotation rights, return rights, and MFC clauses. None found.
P3  Obtained partner sell-through reports; recomputed aggregate end-customer
    consideration of $13,472 and the implied average partner margin of 28.0%; analysed
    the dispersion of end-customer prices against AtlasFlow list (range: 6% below to
    3% above), corroborating genuine partner price discretion.
P4  Queried FY2024-FY2025 cash application for any receipt from an end customer of a
    structure-A arrangement. Result: none.
P5  Confirmed arrangement terms directly with Tessera Partners under AS 2310.
P6  Tested the sell-through-clause sub-population (9 arrangements) for revenue
    recognized before end-customer acceptance.
P7  Evaluated management's memorandum against ASC 606-10-15-3 and 606-10-55-36 to
    55-40; documented six reasoning defects (see Analysis at WP 3200-14c).
P8  Recomputed the gross-presentation alternative and its effect on revenue, gross
    margin, ARR, and the channel disaggregation category.
P9  Evaluated the severity of the related control deficiency (WP 4100-09, item D-31).

-------------------------------------------------------------------------------------
RESULTS
-------------------------------------------------------------------------------------
R1  39 arrangements ($8,646): partner is the customer. Net presentation correct.
R2  3 arrangements ($1,054 recorded): end customer is the customer; AtlasFlow bears
    credit risk and invoices the end customer; partner earns a 15% referral fee.
    Correct presentation: revenue $1,240; referral fee $186 to account 6200 (ASC
    340-40 incremental cost). Misclassification $186; no net loss effect. CORRECTED
    by management 02/12/2026 (JE 2026-0214).
R3  P6: 2 arrangements, $480 ACV, revenue started 46 days before end-customer
    acceptance. Misstatement $480 x 46 / 365 = $61. Below CTT of $72. Logged at
    WP 3200-14d.
R4  P8: gross presentation would increase FY2025 revenue by $3,772 to $151,972 (2.5%),
    move subscription gross margin by +0.7 pp or -1.8 pp depending on the
    classification of the partner margin, and increase disclosed ARR by $4,822 (2.8%).
    No effect on the net loss under any presentation.
R5  P7: management's memorandum reaches the correct conclusion on unsupportable
    reasoning. Not relied upon as audit evidence. Rewritten by management 02/16/2026.
R6  P9: significant deficiency. Potential magnitude $3,772 = 2.6x overall materiality
    of $1,450. Communicated in writing to the audit committee 02/18/2026.

-------------------------------------------------------------------------------------
CONCLUSION
-------------------------------------------------------------------------------------
Based on the procedures performed, subscription revenue from the channel population is
appropriately presented net of the partner discount for the 39 arrangements in which
the partner is AtlasFlow's customer, and no professional services revenue is
appropriately recorded where the partner contracts separately with the end customer
for implementation. Following the $186 correction at R2, revenue for the channel
population is fairly stated and the channel disaggregation category of $12,966 is
appropriately presented. The classification and presentation assertions for the
channel population are supported. One significant deficiency in the review of
accounting conclusions for non-routine arrangements is reported at WP 4100-09 (D-31).

CROSS-REFERENCES: WP 1300-01 (materiality: OM $1,450; PM $940; CTT $72);
                  WP 3200-08 (contract C-1 end-to-end test);
                  WP 3200-22 (December cut-off testing);
                  WP 3200-31 (revenue disaggregation disclosure);
                  WP 4100-09 (ICFR deficiency log, item D-31);
                  WP 5100-04 (accounts receivable confirmation — reseller addressees).
=====================================================================================
```

### Lessons

1. **A right answer with wrong reasoning is a control failure even when it is not a misstatement.** The financial
   statements were correct for 39 of 42 arrangements. The process that produced them could not distinguish the 39
   from the 3, and that is what the ICFR opinion is about.
2. **Ask who the customer is before asking whether you are the principal.** The principal-versus-agent guidance
   presupposes an identified customer. Reaching for it first inverts the analysis and, as here, produces a premise
   that contradicts the conclusion.
3. **A judgment memorandum that does not quantify the alternative cannot be reviewed.** The single most useful
   sentence management could have written was "the alternative conclusion would increase FY2025 revenue by $3,772,
   or 2.5%." Its absence is why nobody noticed that the reasoning pointed the other way.
4. **Test the population attribute, not the exemplar.** Management analysed C-4 and asserted 41 others were similar.
   Forty-two order-form counterparties can be extracted in an afternoon, and doing so found the three that were not.
5. **The name on the receivable is not always the name of the obligor.** A $1,510 balance recorded under Cirrus
   Retail Group and owed by Tessera Partners changes the confirmation addressee and the credit assessment, and
   neither error would have been caught by any procedure aimed at the revenue caption.
6. **The bottom line is the wrong yardstick for a presentation question.** Every presentation in Exhibit 4-34
   produces a net loss of $(21,400). The materiality of the question lives in revenue, gross margin, and the
   metrics investors use, which is the reasoning Chapter 3, §3.9 develops for non-GAAP and operating measures.

## Common Mistakes

### Mistake 4.1 — Responding to the revenue fraud presumption with a more precise analytic

**What it looks like.** The audit programme responds to the presumed fraud risk in revenue with a disaggregated
substantive analytical procedure — revenue by month by stream against an expectation built from ARR and churn — and
records that the analytic was precise to within 1.2%, so no further work was required.

**Why it happens.** The analytic is genuinely good, it is cheap, it covers 100% of the population, and it satisfies
the reviewer's instinct that precision equals evidence.

**What goes wrong.** AS 2301 requires substantive procedures specifically responsive to a significant risk, and
AU-C 330 requires tests of details where the response consists only of substantive procedures. An analytic built
from ARR cannot detect a backdated order form, because the backdated order form is inside the ARR the expectation
was built from. The procedure and the misstatement share a source.

**How to avoid it.** State, for each significant-risk assertion, which procedure obtains evidence from outside
management's control. If the answer for cut-off is not a DocuSign certificate, a provisioning log, a field-history
extract, or a confirmation, the response is not sufficient. Keep the analytic; do not let it carry the assertion.

### Mistake 4.2 — Testing the date field instead of the date

**What it looks like.** The cut-off workpaper records that 57 order forms were agreed to the "contract date per
Salesforce," with a tick mark and no exceptions.

**Why it happens.** Salesforce is the contract repository, the field is authoritative-looking, and it is the field
the revenue engine consumes.

**What goes wrong.** The VP Sales Operations administers Salesforce CPQ and can modify order-form dates. Agreeing a
recorded amount to the field that produced it is a circular procedure that will never find the misstatement the
risk assessment identified. Four of AtlasFlow's six FY2025 exceptions were found in field history — that is, in the
record of the field having been changed — not in the field.

**How to avoid it.** Rank your evidence before you plan: DocuSign completion certificate, customer confirmation,
email from the customer's domain, provisioning log, field history, then the field itself. Test downward from the top
of that list and stop when you have evidence outside AtlasFlow's control.

### Mistake 4.3 — Calling a control deviation a misstatement, or a misstatement a deviation

**What it looks like.** A workpaper that reports "9 exceptions" combining three approvals recorded after signature,
two Zuora term-entry errors with no revenue effect, and six order forms with no evidence of execution.

**Why it happens.** All nine feel like problems, and "exception" is the word that covers everything.

**What goes wrong.** The three approvals are control deviations feeding a deficiency evaluation with a tolerable
deviation rate; the six are misstatements feeding the summary of audit differences with a materiality threshold. The
two populations are evaluated against different criteria, communicated to different people, and aggregate
differently. A combined count of nine supports no conclusion about either.

**How to avoid it.** Three columns in the exception schedule: *control deviation*, *misstatement*, and *both*. Force
every item into exactly one. Then evaluate the columns separately, and never report a single count.

### Mistake 4.4 — Building the service level credit population from the ledger

**What it looks like.** Testing account 4900 by selecting a sample of the credit memos in it, agreeing each to a
customer claim, and concluding that credits are appropriately recorded.

**Why it happens.** It is the procedure every account gets, and the account has a natural population — the entries
in it.

**What goes wrong.** The assertion at risk for contra-revenue is **completeness**, and the entries in the account
are precisely the population that cannot provide evidence about it. AtlasFlow's independent expectation, built from
AWS availability data, was $783 against $490 that management had recorded before the audit; the $290 difference was
invisible to any procedure whose population came from the ledger.

**How to avoid it.** Build the population from the event that creates the obligation, not from the accounting for
it: the availability report for SLA credits, the return window for refunds, the renewal calendar for concessions.
Then reconcile that population to the account, in that direction.

### Mistake 4.5 — Sizing the period-end cut-off test on the revenue effect

**What it looks like.** A memorandum concluding that the December 24–31 population's maximum revenue effect of $462
is below performance materiality of $940, so testing is limited to a sample of ten items.

**Why it happens.** The arithmetic is correct and the logic is the standard extent logic.

**What goes wrong.** The revenue effect is eight days of a twelve-month subscription. The same population carries
$25,174 of the RPO disclosure, $12,840 of receivables and deferred revenue, $1,510 of capitalized commissions, the
bookings and ARR figures in MD&A, and a potential magnitude of $25,174 for the ICFR conclusion. The exposure is
17 times overall materiality, not 0.3 times.

**How to avoid it.** Before setting extent, list every financial statement amount, disclosure, metric, and control
conclusion that the population affects, and size on the largest. Exhibit 4-23 is that list for AtlasFlow.

### Mistake 4.6 — Asking whether you are the principal before asking who the customer is

**What it looks like.** A memorandum that opens with the ASC 606-10-55-39 indicators, works through them, and
concludes "we are the principal, therefore net."

**Why it happens.** Principal-versus-agent is the memorable part of the guidance and the indicators are a
convenient structure to write against.

**What goes wrong.** Being the principal is the reason to record **gross**. If the reseller is the customer, the
guidance is never reached and revenue is the consideration from the reseller. The conclusion may still be right, as
AtlasFlow's was, and a reviewer cannot tell whether it is right or lucky.

**How to avoid it.** Write the memorandum in the order the standard is structured: identify the customer under
ASC 606-10-15-3; identify the specified good or service; only then, and only if the end customer is the customer,
assess control under ASC 606-10-55-36 through 55-40. State the effect of the alternative in dollars.

### Mistake 4.7 — Treating provisioning as corroboration that a contract existed

**What it looks like.** An exception cleared on the basis that "the tenant was provisioned on December 22, so the
contract clearly existed at year end."

**Why it happens.** Provisioning is an immutable, system-generated timestamp, and it feels like the strongest
evidence in the file. For the *start date* assertion, it is.

**What goes wrong.** Provisioning is an act AtlasFlow performs unilaterally. It evidences that the service was made
available; it says nothing about whether the customer had approved a contract. ASC 606-10-25-1 requires approval by
both parties, and only the counterparty's own record evidences that.

**How to avoid it.** Match the evidence to the criterion. Provisioning corroborates the recognition start date.
Approval is corroborated only by a DocuSign certificate, an email from the customer's domain, a confirmation, or the
customer's executed counterpart.

### Mistake 4.8 — Accepting the estimate of total hours because there is no independent source

**What it looks like.** A workpaper recording that the estimated total hours on each fixed-fee engagement were
discussed with the delivery manager and appeared reasonable in light of the engagement's scope.

**Why it happens.** The estimate genuinely is the delivery manager's judgment, and there is no market price for it.

**What goes wrong.** The delivery manager prepares and approves the number that determines revenue, and a lower
number raises revenue. Inquiry of that person is evidence about their assertion, not about the estimate. At AtlasFlow
the difference was $95, and 27 of 32 engagements moved the same way — a pattern that inquiry cannot detect.

**How to avoid it.** Look for a contemporaneous estimate prepared for a different purpose. AtlasFlow's
resource-management system holds estimate-to-complete hours maintained weekly for staffing. Recompute with it, and
then evaluate the direction of the differences, not only their magnitude, because directional consistency is
evidence of bias under AS 2810 and AU-C 450.

### Mistake 4.9 — Using the billings bridge as evidence about cut-off

**What it looks like.** A revenue programme whose cut-off response is the revenue-to-billings-to-cash reconciliation,
on the reasoning that a reconciliation that ties for the full year leaves no room for a misstatement.

**Why it happens.** The bridge is elegant, it covers 100% of the population, and when it ties it feels conclusive.

**What goes wrong.** The bridge is an identity, and a fictitious invoice satisfies it: revenue rises, the receivable
rises, and cash is unchanged. AtlasFlow's bridge ties to the dollar on a population that includes all six
uncorroborated December order forms. The bridge is a completeness procedure and it is blind to overstatement.

**How to avoid it.** Label every reconciliation with the assertion it addresses. The bridge addresses completeness of
revenue and existence of deferred revenue. Cut-off and occurrence require the work in §4.9, and nothing in the
bridge substitutes for it.

### Mistake 4.10 — Citing the sales- and usage-based royalty exception for SaaS usage revenue

**What it looks like.** A revenue policy memorandum stating that workflow-run overage is recognized as consumed
under the exception in ASC 606-10-55-65.

**Why it happens.** The exception's outcome — recognize as the usage occurs — matches what the entity does, and the
paragraph is the one everyone remembers.

**What goes wrong.** That exception applies only to consideration in exchange for a **license of intellectual
property**. A hosted multi-tenant service is not a license; the customer never obtains the software. The accounting
is usually still right, reached under the variable-consideration allocation exception in ASC 606-10-32-40 or the
right-to-invoice expedient in ASC 606-10-55-18. A right answer under a wrong citation cannot be reviewed and will
not survive a regulatory comment.

**How to avoid it.** When a memorandum cites a paragraph, read the paragraph's scope, not its conclusion. Then
confirm the entity actually meets the criteria of the route it is relying on, and say which route that is.

### Mistake 4.11 — Auditing the disaggregation total instead of the categorization

**What it looks like.** Three tick marks confirming that each disaggregation category in the revenue note sums to
$148,200.

**Why it happens.** Footing a table is fast, verifiable, and reviewable.

**What goes wrong.** The total cannot be wrong once the revenue caption has been audited. Everything at risk in a
disaggregation disclosure is in the assignment of transactions to categories. AtlasFlow's geographic categories were
built by legal entity while the note said billing address, misstating the EMEA category by $2,000 — 138% of overall
materiality — in a table that footed perfectly.

**How to avoid it.** Read the note's stated basis first, then recompute the categories on that basis from the
underlying population. Where the basis is a manually maintained field, recompute rather than sample: AtlasFlow's
channel picklist had 214 blank values filled in by an analyst during the close.

### Mistake 4.12 — Treating a disputed invoice as a credit loss question

**What it looks like.** A disputed $1,240 professional services invoice evaluated entirely within the allowance for
credit losses, with a specific reserve proposed and revenue untouched.

**Why it happens.** The dispute surfaces on the receivable, the receivable is where the aging lives, and the
allowance is the account with an established mechanism for uncertainty.

**What goes wrong.** ASC 606-10-32-2 requires the transaction price to be the consideration the entity *expects to
be entitled to*, so an expected price concession reduces revenue and creates a refund liability. A $300 expected
concession reduces revenue by $120 on a 40%-complete engagement and creates a $300 refund liability; a $300 expected
credit loss leaves revenue alone and increases the provision by $300. Identical cash, different income statement,
and only one of the two is correct.

**How to avoid it.** Ask the concession question first and document the answer. The test is whether the entity
expects to accept less than the contractual amount — evidenced by settlement correspondence, credit memos issued
after the period end, or internal quantification — as distinct from whether the customer is unable to pay.

## Practice Exercises

All amounts are in thousands of US dollars unless stated otherwise. Use a 365-day convention and recognize revenue
from the start date through December 31 inclusive. AtlasFlow's FY2025 thresholds apply throughout: overall
materiality $1,450, performance materiality $940, clearly trivial threshold $72, specific materiality $150, and
tolerable misstatement for the significant-risk revenue populations $705.

### Exercise 4-1

**[Foundational]** Harborline Clinics signed an order form on June 10, 2025 for a 24-month term running July 1, 2025
through June 30, 2027. Terms: Core subscription $480 in year 1 and $600 in year 2; Insight add-on $120 in year 2
only; fixed-fee implementation $180 delivered July and August 2025; 150,000 included workflow runs per year with
overage at $12 per 1,000 runs (whole dollars); and a 30-day money-back guarantee expiring July 31, 2025, on which
AtlasFlow's historical exercise rate is 2.0% of contract consideration. The tenant was provisioned July 1, 2025 and
the guarantee was not exercised.

Required: (a) total fixed consideration; (b) each element of variable consideration and whether it enters the
transaction price at inception; (c) the transaction price at inception; (d) FY2025 revenue on the Core subscription
element, computed on stated contract prices with the subscription recognized straight-line over the term.

### Exercise 4-2

**[Foundational]** A customer's 12-month contract carries fixed consideration of $2,400 and the standard uptime
schedule: 99.9% commitment, a credit of 10% of the monthly fee for measured availability between 99.0% and 99.9%,
and 25% below 99.0%. Measured availability was 99.62% in March and 98.44% in September; every other month exceeded
99.9%. The customer claimed $260 in December. Management assesses the outcomes as: settlement at the contractual
entitlement, 30% probable; settlement at $150, 50% probable; settlement at the full claim of $260, 20% probable.

Required: (a) the contractual entitlement; (b) the expected value; (c) the most likely amount; (d) which method
better predicts the consideration to which the entity will be entitled, and what ASC 606 requires about applying it
across contracts.

### Exercise 4-3

**[Intermediate]** Recompute a service level credit population. Region 1 has 210 contracts on the standard schedule
with an aggregate monthly subscription fee of $3,600; region 2 has 58 contracts with an aggregate monthly fee of
$1,240. Measured availability was: region 1, 99.55% in May and 98.82% in October; region 2, 99.94% in May and 99.71%
in October. All other months exceeded 99.9%. Forty of the region 1 contracts, with an aggregate monthly fee of $700,
provide automatic credits requiring no customer claim; every other contract requires a written claim within 30 days
of month end, and the historical claim rate over prior breach months is 42%. The entity recorded $520 of credits.

Required: (a) the maximum contractual entitlement; (b) the auditor's independent expectation; (c) the difference
against the recorded amount, its relationship to the clearly trivial threshold, and the two candidate explanations
for the difference, stating what you would do next under each.

### Exercise 4-4

**[Intermediate]** A fixed-fee implementation carries a $540 fee. The estimate at inception was 2,000 total hours.
Hours incurred were 400 in Q1, 600 in Q2, 500 in Q3, and 450 in Q4. During Q3 the delivery manager revised the
estimate of total hours to 2,250. Of the Q3 hours, 80 were rework caused by AtlasFlow's own configuration error; the
revised 2,250-hour estimate includes those 80 hours.

Required: (a) cumulative and quarterly revenue for each quarter as management computed it, using 2,000 hours until
the Q3 revision and including the rework hours; (b) the same schedule computed correctly under ASC 606-10-55-21;
(c) the cumulative difference at December 31 and whether it is accumulated.

### Exercise 4-5

**[Intermediate]** Five order forms in the December cut-off population:

| Order form | Annual contract value | Stated execution date | Recognition start date |
| --- | --- | --- | --- |
| A | 900 | December 26, 2025 | December 5, 2025 |
| B | 640 | December 29, 2025 | December 1, 2025 |
| C | 500 | December 30, 2025 | December 30, 2025 |
| D | 320 | December 31, 2025 | December 14, 2025 |
| E | 180 | December 24, 2025 | November 15, 2025 |

Required: (a) FY2025 revenue recognized on each order form and in total; (b) the amount at risk in the remaining
performance obligation disclosure if none of the five execution dates can be corroborated; (c) how the total revenue
effect compares to the clearly trivial threshold and to performance materiality; (d) which exposure should drive the
extent of testing, and one sentence explaining why.

### Exercise 4-6

**[Advanced]** A registrant records 28 reseller arrangements net, at $6,400 of FY2025 revenue, at an average
reseller discount of 22% to list. The partners' sell-through reports show aggregate end-customer consideration of
$8,205.

Required: (a) demonstrate whether the sell-through total is arithmetically consistent with a 22% average discount;
(b) using AtlasFlow's reported FY2025 figures, compute total revenue, gross profit, and gross margin under gross
presentation with the partner margin classified first in sales and marketing and then in cost of revenue; (c) state
the effect on the net loss; (d) evaluate materiality, identifying the benchmark against which you evaluate it.

### Exercise 4-7

**[Intermediate]** Larkmead Retail signed a 12-month renewal on October 1, 2025 at annual contract value of $760.
At that date $890 of Larkmead's prior invoices were 120 days past due, no payment had been received for five months,
and Larkmead had publicly announced a restructuring. AtlasFlow provisioned the renewal on October 1, recognized
revenue from that date, and collected nothing against the renewal by December 31, 2025.

Required: conclude on whether a contract exists under ASC 606-10-25-1, compute the FY2025 misstatement if it does
not, identify the credible alternative conclusion and why it is weaker, and state two changes to the facts that would
make collection probable.

### Exercise 4-8

**[Advanced]** Fairmont Group Holdings executed an order form on November 3, 2025 with annual contract value of
$1,400 at a 22% discount to list. Fairmont Logistics, a wholly owned subsidiary of Fairmont Group Holdings, executed
a separate order form on November 19, 2025 with annual contract value of $600 at a 9% discount to list. Both were
negotiated with the same Fairmont VP of Procurement. The cover email transmitting the second order form states "as
discussed, the second order gets the pricing agreed in the group deal." The two entities receive separate tenants
with separate seat pools, and the contracts do not co-terminate.

Required: apply the gateway condition and each of the three criteria in ASC 606-10-25-9, state your conclusion, and
compute the combined list consideration, combined net consideration, and blended discount that would result from
combining.

### Exercise 4-9

**[Advanced]** Eighteen FY2025 contracts were prepaid in full at inception for 24-month terms, with total upfront
payments of $7,200. The entity's incremental borrowing rate is 9.5%. Management concluded no financing adjustment
was required and cited the practical expedient in ASC 606-10-32-18.

Required: (a) compute the average outstanding advance, the imputed interest over the term, the annual effect on
revenue and interest expense, and the imputed interest as a percentage of average contract consideration; (b) state
whether the cited practical expedient is available and why; (c) state where your conclusion falls in the range of
defensible answers and what would move it; (d) compute the size of the prepaid population at which the annual effect
reaches performance materiality.

### Exercise 4-10

**[Intermediate]** Draft the side-agreement paragraph for AtlasFlow's FY2025 management representation letter. It
must be specific enough that a false representation is identifiable, must name the systems in which arrangements are
required to be recorded, and must enumerate the kinds of rights it covers. Ninety to one hundred and thirty words.

### Exercise 4-11

**[Advanced]** Draft the "Results" and "Conclusion" sections of WP 3200-22, the FY2025 December cut-off workpaper,
from these facts: population 1 comprised 118 order forms with $25,174 of annual contract value; 57 items with
$20,360 of annual contract value were tested, being 43 items at 100% coverage in stratum A and 14 of 75 items in
stratum B; six stratum A items had no evidence of execution outside AtlasFlow's control, with $150 of FY2025 revenue
and $2,340 of annual contract value; three items had an internal approval timestamp after the customer signature
timestamp; no side agreements were identified; stratum B produced no exceptions; and a separate population of 214
FY2025 order forms with $9,840 of annual contract value was executed outside DocuSign. One hundred and eighty to two
hundred and forty words.

### Exercise 4-12

**[Advanced]** Find the errors in the following workpaper extract. Identify at least eight defects and state the
correction for each.

```text
WP 3200-22   AtlasFlow, Inc. — FY2025 revenue cut-off
Prepared by: R. Doyle  02/14/2026        Reviewed by: R. Doyle  02/14/2026

PURPOSE: To test December 2025 revenue.

POPULATION: December 2025 bookings per the Sales Operations report, $25,174.

SAMPLE: 25 items selected haphazardly. Coverage not computed.

PROCEDURES: For each item, agreed the signature date to the contract date field in
Salesforce and agreed the contract value to the Zuora subscription.

RESULTS: 9 exceptions noted, none material. The largest related to contracts totaling
$2,340 of annual contract value where documentation was incomplete.

THRESHOLD APPLIED: performance materiality of $1,450.

CONCLUSION: Revenue is fairly stated in all material respects. The order-form approval
control operated effectively throughout the year ended December 31, 2025.
```

### Exercise 4-13

**[Advanced]** This exercise spans Chapter 3 and Chapter 4. The $213 of consideration payable to customers in §4.5.5
is not supported by a distinct good or service and should be reclassified from sales and marketing expense to
contra-revenue in account 4900. Management declined.

Required: (a) compute reported subscription revenue growth from FY2024 to FY2025 and recompute it after the
reclassification, using $135,800 and $108,300; (b) state the effect on the net loss; (c) evaluate the misstatement
against overall materiality, performance materiality, the clearly trivial threshold, and specific materiality;
(d) apply the qualitative factors in SAB 99 to conclude whether the item is material notwithstanding its size,
referring to the reasoning Chapter 3's Extended Case Study applies to net revenue retention and the performance
stock unit threshold.

### Exercise 4-14

**[Intermediate]** Four FY2025 payments were made to counterparties that are also customers:

| # | Counterparty | Amount | Facts |
| --- | --- | --- | --- |
| 1 | Meltham Partners (reseller) | 160 | Market development funds. Campaign deliverables are evidenced for 60% of the spend; there is no rate card for the remainder |
| 2 | Corvin Integration Group | 90 | Conference sponsorship, priced at the sponsor's published rate card amount of $90 |
| 3 | Dunmore Foods | 220 | Purchase of catering services. Three competitive quotes support a fair value of $175 |
| 4 | Talbot Insurance | 140 | Described in the purchase order as a "partnership fee." No deliverable is identified |

Required: for each payment, state the amount that is a reduction of the transaction price and the amount that is an
expense; compute the totals; prove that the totals sum to the amount paid; and state which single payment you would
escalate under AS 2401 and why.

## Solutions to Practice Exercises

### Solution 4-1

(a) Fixed consideration: Core year 1 $480 + Core year 2 $600 + Insight year 2 $120 + implementation $180 = **$1,380**.

(b) Two elements are variable. The **workflow-run overage** is variable and is excluded from the transaction price at
inception because the amount is not determinable and, under AtlasFlow's policy, it relates specifically to the
distinct daily service in the month the runs are consumed (ASC 606-10-32-40). The **money-back guarantee** is
variable consideration in the form of a right of return; it *reduces* the transaction price by the amount expected to
be refunded, so at inception the expected refund is $1,380 × 2.0% = $27.6.

(c) Transaction price at inception: $1,380 − $27.6 = **$1,352** (rounded). Once the guarantee lapsed unexercised on
July 31, 2025, the constraint on that element was resolved and the transaction price became $1,380.

(d) The Core subscription total is $480 + $600 = $1,080 over the term July 1, 2025 to June 30, 2027, which is 730
days. Daily rate $1,080 ÷ 730 = $1.4795. July 1 to December 31, 2025 is 31 + 31 + 30 + 31 + 30 + 31 = 184 days.
FY2025 Core revenue = $1.4795 × 184 = **$272**. Note that straight-lining the two-year total recognizes more than the
$480 year-one fee would ($480 × 184 ÷ 365 = $242), so the ramp creates a $30 contract asset by year end on this
element — the same mechanic as C-1 in step 19 of the walkthrough. Insight contributes nothing because the service is
first provided in year 2.

### Solution 4-2

(a) Monthly fee = $2,400 ÷ 12 = $200. March availability of 99.62% falls in the 99.0%–99.9% band, giving
$200 × 10% = $20. September availability of 98.44% is below 99.0%, giving $200 × 25% = $50. **Contractual
entitlement $70.**

(b) Expected value = (30% × $70) + (50% × $150) + (20% × $260) = $21 + $75 + $52 = **$148**.

(c) The most likely amount is the single most probable outcome, which is the $150 settlement at 50% probability:
**$150**.

(d) The two methods differ by $2, which is 2.8% of the clearly trivial threshold, so the choice does not matter here
and either is supportable. Where the outcomes are dispersed, the expected value method better predicts the
consideration for a large population of similar contracts and the most likely amount better predicts it where there
are only two possible outcomes. ASC 606-10-32-8 requires the chosen method to be applied **consistently throughout
the contract and to similar contracts**, so the audit procedure is not to argue about the method on one contract but
to test that the same method was applied across the service level credit population rather than selected contract by
contract. Note also that the contractual entitlement of $70 is a floor, not the answer: an entity with a history of
settling above the schedule expects to be entitled to less than the gross fee by more than $70.

### Solution 4-3

(a) Maximum contractual entitlement:

| Region | Month | Availability | Band | Aggregate monthly fee | Credit |
| --- | --- | --- | --- | --- | --- |
| 1 | May | 99.55% | 10% | 3,600 | 360 |
| 1 | October | 98.82% | 25% | 3,600 | 900 |
| 2 | May | 99.94% | Above the commitment | 1,240 | — |
| 2 | October | 99.71% | 10% | 1,240 | 124 |
| **Total** | | | | | **1,384** |

(b) The 40 automatic-credit contracts, all in region 1 with an aggregate monthly fee of $700, are entitled to
$700 × 10% = $70 in May and $700 × 25% = $175 in October, or $245, and the full amount is expected because no claim
is required. The claim-required entitlement is $1,384 − $245 = $1,139, of which 42% is expected to be claimed:
$1,139 × 42% = $478. **Independent expectation = $245 + $478 = $723.**

(c) The difference is $723 − $520 = **$203**, which is 2.8 times the $72 clearly trivial threshold and must be
accumulated. Two candidate explanations, and they lead to different places. If the difference is a **measurement**
issue — the 42% claim rate is not the right estimator — it is an estimate matter, and the next step is to test
whether the claim rate has trended upward across the prior breach months and to recompute using the most recent
periods; a claim rate of 42% derived from years in which customers were less sophisticated is a biased estimator. If
the difference is a **completeness** issue — contracts were omitted from the 268-contract population — the next step
is to reconcile the SLA-bearing contract count to the total contract population, because an entity that does not
know which of its contracts contain a service level commitment has a control deficiency whose potential magnitude is
the full $1,384 rather than the $203.

### Solution 4-4

(a) As management computed it:

| Quarter | Hours in the quarter | Cumulative hours | Estimated total hours | Percentage complete | Cumulative revenue | Quarterly revenue |
| --- | --- | --- | --- | --- | --- | --- |
| Q1 | 400 | 400 | 2,000 | 20.00% | 108.0 | 108.0 |
| Q2 | 600 | 1,000 | 2,000 | 50.00% | 270.0 | 162.0 |
| Q3 | 500 | 1,500 | 2,250 | 66.67% | 360.0 | 90.0 |
| Q4 | 450 | 1,950 | 2,250 | 86.67% | 468.0 | 108.0 |
| **Total** | **1,950** | | | | | **468.0** |

Arithmetic: $540 × 20.00% = $108.0; $540 × 50.00% = $270.0, so Q2 is $162.0; $540 × 1,500 ÷ 2,250 = $360.0, so Q3 is
$90.0; $540 × 1,950 ÷ 2,250 = $468.0, so Q4 is $108.0.

(b) Correctly, excluding the 80 rework hours from both the numerator and the denominator, because ASC 606-10-55-21
requires the measure of progress to exclude inputs that do not depict performance. Productive cumulative hours become
1,420 in Q3 and 1,870 in Q4, and the productive estimate of total hours becomes 2,250 − 80 = 2,170.

| Quarter | Cumulative productive hours | Estimated productive total | Percentage complete | Cumulative revenue | Quarterly revenue |
| --- | --- | --- | --- | --- | --- |
| Q1 | 400 | 2,000 | 20.00% | 108.0 | 108.0 |
| Q2 | 1,000 | 2,000 | 50.00% | 270.0 | 162.0 |
| Q3 | 1,420 | 2,170 | 65.44% | 353.4 | 83.4 |
| Q4 | 1,870 | 2,170 | 86.18% | 465.4 | 112.0 |
| **Total** | | | | | **465.4** |

Arithmetic: $540 × 1,420 ÷ 2,170 = $353.4, so Q3 is $353.4 − $270.0 = $83.4; $540 × 1,870 ÷ 2,170 = $465.4, so Q4 is
$465.4 − $353.4 = $112.0.

(c) The cumulative difference at December 31 is $468.0 − $465.4 = **$2.6**, which is 3.6% of the clearly trivial
threshold and is logged rather than accumulated. Two observations matter more than the $2.6. First, the *quarterly*
differences are larger than the annual difference — Q3 is overstated by $6.6 and Q4 understated by $4.0 — which
matters for a large accelerated filer subject to quarterly review. Second, excluding rework from the numerator alone
while leaving it in the denominator, which is the error teams most often make when they attempt this correction,
would give $540 × 1,420 ÷ 2,250 = $340.8 and would understate revenue by $19.2. The exclusion has to be symmetric.

### Solution 4-5

(a)

| Order form | Annual contract value | Recognition start date | Days in FY2025 | FY2025 revenue |
| --- | --- | --- | --- | --- |
| A | 900 | December 5 | 27 | 66.6 |
| B | 640 | December 1 | 31 | 54.4 |
| C | 500 | December 30 | 2 | 2.7 |
| D | 320 | December 14 | 18 | 15.8 |
| E | 180 | November 15 | 47 | 23.2 |
| **Total** | **2,540** | | | **162.7** |

Arithmetic: $900 × 27 ÷ 365 = $66.6; $640 × 31 ÷ 365 = $54.4; $500 × 2 ÷ 365 = $2.7; $320 × 18 ÷ 365 = $15.8;
$180 × 47 ÷ 365 = $23.2. The unrounded sum is $162.64; the column of individually rounded amounts sums to $162.7,
which is the figure carried forward.

(b) The amount at risk in the remaining performance obligation disclosure is the full annual contract value of the
five order forms, **$2,540**, because if the contracts did not exist at December 31 none of their unsatisfied
consideration belongs in the disclosure.

(c) The $162.7 revenue effect is 2.3 times the $72 clearly trivial threshold, so it is accumulated, and it is 17.3%
of performance materiality of $940, so on the revenue caption alone it would not by itself require adjustment.

(d) The **RPO exposure of $2,540** should drive the extent: it is 1.75 times overall materiality of $1,450, against a
revenue effect that is a fraction of performance materiality. Testing sized on the revenue effect would leave a
disclosure exposure larger than overall materiality untested.

### Solution 4-6

(a) At a 22% average discount, AtlasFlow's recorded revenue is 78% of the end-customer consideration, so implied
end-customer consideration is $6,400 ÷ 0.78 = **$8,205**, which agrees to the sell-through reports. The gross-up
difference is $8,205 − $6,400 = **$1,805**. Consistency here is a necessary condition, not a sufficient one: it
demonstrates only that the reported margin is arithmetically coherent, and a team should still test the dispersion of
end-customer prices, because an average that ties while individual prices vary widely is evidence of genuine
reseller price discretion, and an average that ties because every price equals list is evidence of the opposite.

(b) Gross presentation, using AtlasFlow's reported figures:

| Line item | As reported, net | Gross, margin in sales and marketing | Gross, margin in cost of revenue |
| --- | --- | --- | --- |
| Total revenue | 148,200 | 150,005 | 150,005 |
| Total cost of revenue | 38,940 | 38,940 | 40,745 |
| **Gross profit** | **109,260** | **111,065** | **109,260** |
| Gross margin | 73.73% | 74.04% | 72.84% |

Arithmetic: $148,200 + $1,805 = $150,005; $150,005 − $38,940 = $111,065 and $111,065 ÷ $150,005 = 74.04%;
$38,940 + $1,805 = $40,745 and ($150,005 − $40,745) ÷ $150,005 = 72.84%. Gross margin moves by +0.31 percentage
points under the first classification and −0.89 under the second.

(c) **No effect on the net loss** under either classification. The gross-up increases revenue and an equal and
opposite amount of expense.

(d) The benchmark question is the point of the exercise. Against the net loss the difference is zero and the item
looks immaterial. Against revenue it is $1,805, which is 1.24 times overall materiality of $1,450 and 1.92 times
performance materiality of $940, and it moves the metric SaaS investors use to judge product quality. A presentation
misstatement must be evaluated against the line items and disclosures it distorts, not against the subtotal it
happens not to touch — the reasoning Chapter 3, §3.8 develops for disclosure materiality.

### Solution 4-7

**Conclusion: no contract exists.** ASC 606-10-25-1(e) requires it to be probable that the entity will collect the
consideration to which it will be entitled. At October 1, 2025 the customer had $890 outstanding at 120 days past
due, had made no payment in five months, and had announced a restructuring. On those facts collection of the $760 of
renewal consideration is not probable, the criteria in 25-1 are not met, and ASC 606-10-25-7 permits revenue only
when consideration is received and specified criteria are satisfied. Nothing was received.

**Misstatement:** October 1 to December 31, 2025 is 92 days, so FY2025 revenue of $760 × 92 ÷ 365 = **$192** should
not have been recognized, and the related receivable should not exist. The amount is 2.7 times the clearly trivial
threshold and is accumulated.

**The credible alternative** is that a contract exists and the collectibility concern is dealt with as an expected
credit loss under ASC 326, producing a $192 revenue balance and a provision against the receivable. It is weaker for
two reasons. First, ASC 606-10-25-1(e) is a recognition gate assessed **at inception**, and a conclusion that
collection is not probable at inception cannot be converted into a measurement adjustment later. Second, it produces
the wrong caption: revenue and receivables are both grossed up, so revenue, days sales outstanding, annual recurring
revenue, and the remaining performance obligation disclosure are all overstated even though the net income effect is
similar. The distinction is developed from the receivable side in Chapter 7, §7.8.

**Two changes that would make collection probable:** (i) prepayment of the renewal consideration, or a parent or
third-party guarantee, so that the amount to which AtlasFlow will be entitled is secured; (ii) restructuring the
renewal to monthly billing with a termination right on non-payment, which reduces the consideration to which
AtlasFlow will be entitled to one month at a time — $63 — and can make collection of *that* amount probable even
where collection of $760 is not. Note that the assessment is of the consideration to which the entity will be
entitled, not of the full contractual amount, which is why the second change works.

### Solution 4-8

**Gateway condition.** The two order forms were executed 16 days apart, and Fairmont Logistics is a wholly owned
subsidiary of Fairmont Group Holdings, so they were entered into at or near the same time with the same customer or
a related party of the customer. The gateway is met — unlike the Meridian Ambulatory illustration in §4.4.5, where
208 days separated the two documents.

**Criterion (a) — negotiated as a package with a single commercial objective.** Met. The same Fairmont VP of
Procurement negotiated both, and the transmittal email expressly ties the second order's pricing to "the pricing
agreed in the group deal." That email is the strongest evidence in the fact pattern and it is the kind of evidence
found only by reading the contract file rather than the order form.

**Criterion (b) — the consideration in one contract depends on the price or performance of the other.** Met on the
same evidence: the second order's price is expressed by reference to the first.

**Criterion (c) — a single performance obligation.** Not met. Separate tenants, separate seat pools, no
co-termination, and neither subscription is an input to a combined output.

**Conclusion: combine.** ASC 606-10-25-9 requires combination if **any one** of the three criteria is met, and two
are. The separate tenants and the absence of co-termination are the facts management is most likely to lead with, and
they are relevant only to criterion (c).

**Blended discount.** Order form 1: list consideration $1,400 ÷ 0.78 = $1,795. Order form 2: list consideration
$600 ÷ 0.91 = $659. Combined list $1,795 + $659 = **$2,454**; combined net $1,400 + $600 = **$2,000**; discount
$2,454 − $2,000 = $454, or **18.5%** ($454 ÷ $2,454). The consequence is not the discount percentage itself but that
the $454 is allocated across the combined set of performance obligations at relative standalone selling price rather
than being confined within each order form, which moves consideration between the two subscriptions and between
periods. Chapter 5, §5.7 works the allocation.

### Solution 4-9

(a) Computation:

| Step | Computation | Amount |
| --- | --- | --- |
| Total upfront payments | 18 contracts | 7,200 |
| Average outstanding advance over the term | (7,200 + 0) ÷ 2 | 3,600 |
| Imputed interest over the 24-month term | 3,600 × 9.5% × 2 | 684 |
| Annual effect on revenue and on interest expense | 684 ÷ 2 | 342 |
| Average contract consideration | 7,200 ÷ 18 | 400 |
| Imputed interest per contract | 684 ÷ 18 | 38 |
| Imputed interest as a percentage of contract consideration | 38 ÷ 400 | 9.5% |

(b) **The cited practical expedient is not available.** ASC 606-10-32-18 permits an entity not to adjust for the time
value of money where the period between the transfer of the good or service and the customer's payment is one year
or less. Payment here is made at inception for services delivered over 24 months, so for every service delivered
after the first twelve months the period exceeds one year. This is the substantive difference from the C-1 ramp in
§4.5.4, where each annual instalment is paid in advance of the twelve months it covers and the expedient does apply
to every instalment.

(c) The conclusion that an adjustment is required sits toward the conservative end of a genuinely contested range.
Against adjustment: the aggregate annual effect of $342 is 0.23% of revenue and 36.4% of performance materiality, and
there is no effect on the net loss because revenue and interest expense move together. For adjustment:
ASC 606-10-32-16 frames significance **at the contract level**, and imputed interest of 9.5% of contract
consideration is not obviously insignificant to the contract. The illustrated answer is that the computation must be
documented and the expedient may not be cited, and that whether the entity adjusts is a matter on which the auditor
should require support rather than an assertion. **What would move it:** a longer prepayment period; a higher
incremental borrowing rate; growth in the prepaid population; or a single contract large enough that the
contract-level test plainly fails.

(d) The annual effect scales linearly with the population: $940 ÷ $342 × $7,200 = **$19,789**, or about $19,800 of
prepaid consideration, at which point the annual effect reaches performance materiality.

### Solution 4-10

Model language, 118 words:

```text
We confirm that, other than the agreements recorded in Zuora Billing and reflected in
the revenue schedules maintained in Zuora Revenue, there are no agreements,
amendments, understandings, or communications, whether written or oral, with any
customer, reseller, or systems integrator that modify the terms of any customer
arrangement or that grant any right of return, refund, cancellation, termination for
convenience, acceptance, delivery contingency, extension of payment terms, future
credit, price concession, most-favoured-customer entitlement, or option to acquire
additional goods or services at a discount. No employee, officer, or agent of the
Company has entered into any such arrangement. All executed customer contracts,
amendments, and related correspondence have been made available to you, including
arrangements executed outside DocuSign.
```

Why each element is there. Naming Zuora Billing and Zuora Revenue converts a general assurance into a testable
statement about a specific record. Enumerating the rights prevents the reply "we did not consider that a
modification." Extending the representation to employees and agents closes the gap where an account executive binds
the company without the Chief Revenue Officer's knowledge. The final clause on wet-ink execution is included because
§4.9.6 identified 214 such order forms, and a representation that is silent on the population where the evidence is
weakest is silent where it matters.

### Solution 4-11

Model language, 214 words:

```text
RESULTS
Population 1 comprised 118 order forms with $25,174 of annual contract value, agreed
to the Q4 bookings figure reported to the board and to the 41% concentration statistic
in the draft MD&A. Stratum A (43 items, $19,240) was tested at 100%; stratum B (14 of
75 items, $1,120) was tested by attribute sample at 90% confidence with a 10%
tolerable deviation rate. Total coverage: 57 items and $20,360, or 80.9% by value.

Six stratum A items had no evidence of execution obtained from outside management's
control: no DocuSign envelope, no transmittal from the customer's domain, and no
confirmation of the execution date. Field history showed a post-creation change to a
date field on four of the six. FY2025 revenue on the six is $150 and annual contract
value is $2,340. Because all six fall in a stratum tested at 100%, $150 is a known
misstatement requiring no projection. Stratum B produced no exceptions; the upper
deviation limit at 90% confidence is 15.2%, implying up to $902 of stratum B annual
contract value affected.

Three items had an internal approval timestamp later than the customer signature
timestamp. These are control deviations, not misstatements, and are carried to the
deficiency evaluation. No side agreements were identified.

CONCLUSION
Except for the $150 accumulated as U-3, and subject to the deficiency evaluation of
the three approval-timing deviations and of the 214-order-form, $9,840 wet-ink
population, the occurrence and cut-off assertions for the December 24-31, 2025
bookings population are supported.
```

Two features to notice. The conclusion is stated at the **assertion** level for a defined population, not as an
opinion on revenue. And the exceptions are separated into misstatements and control deviations before the conclusion
is drawn, so the reader can see which threshold each was evaluated against.

### Solution 4-12

Eleven defects.

1. **The population is wrong.** "December 2025 bookings" is population 1 only. It omits contracts with a December
   recognition start date and a January signature date, and it omits January-executed order forms with December start
   dates. Correction: define the three populations in §4.9.2 and test each.
2. **The population source is management's report with no reconciliation.** Correction: reconcile the record count
   and value to the Q4 bookings figure reported to the board and to the MD&A concentration statistic.
3. **The sample size has no basis and the selection method is wrong for the objective.** Twenty-five haphazardly
   selected items is a control-testing convention applied to a test of details over a significant risk. Correction:
   stratify and set extent by reference to the exposures the population affects, not by convention.
4. **Coverage is not computed.** Correction: state items and value tested, and coverage as a percentage.
5. **The key procedure is circular.** Agreeing the signature date to the Salesforce contract date field tests the
   field against itself. Correction: agree to the DocuSign completion certificate, and run the field history extract.
6. **Exceptions are aggregated across incompatible categories.** "9 exceptions" mixes control deviations with
   misstatements. Correction: separate them and evaluate each against its own criterion.
7. **"None material" is asserted without a threshold or an amount.** Correction: quantify each misstatement and
   compare it to the clearly trivial threshold of $72 and to performance materiality.
8. **The misstatement is quantified in annual contract value rather than in revenue.** The $2,340 of annual contract
   value produces $150 of FY2025 revenue. Correction: quantify the revenue effect, and separately quantify the RPO,
   receivable, deferred revenue, and commission exposures.
9. **The threshold is mislabelled.** Performance materiality is $940; $1,450 is overall materiality. Correction: cite
   both, and cross-reference WP 1300-01.
10. **The conclusion is an audit opinion, not a workpaper conclusion.** "Revenue is fairly stated in all material
    respects" cannot be concluded from one procedure over one population. Correction: conclude on the occurrence and
    cut-off assertions for the defined population.
11. **A December-only sample cannot support a conclusion that the control operated throughout the year, and there is
    no independent review.** The preparer and reviewer are the same person and the review date equals the preparation
    date. Correction: add items from January through November for period coverage (§4.11), and obtain review by
    someone who did not prepare the workpaper.

### Solution 4-13

(a) Reported subscription revenue growth: ($135,800 ÷ $108,300) − 1 = 1.25392 − 1 = **25.39%**. After reclassifying
$213 out of revenue: ($135,587 ÷ $108,300) − 1 = 1.25196 − 1 = **25.20%**. Growth falls by 0.19 percentage points.

(b) **No effect on the net loss.** Revenue falls $213 and sales and marketing expense falls $213.

(c) Quantitative evaluation: $213 is 14.7% of overall materiality of $1,450, 22.7% of performance materiality of
$940, 2.96 times the clearly trivial threshold of $72, and 1.42 times the $150 specific materiality set for
sensitive disclosures. It exceeds the clearly trivial threshold, so it is accumulated; on the income statement alone
it is comfortably below any threshold that would compel adjustment.

(d) Qualitatively, the SAB 99 factors that apply are: whether the misstatement masks a change in earnings or other
trends; whether it changes a measure the registrant has told investors it manages against; whether it affects
compliance with contractual requirements; and whether it increases management's compensation. Applied here: the item
moves a *growth rate* AtlasFlow discusses in MD&A by 0.19 percentage points, which is small; it does not change the
net loss; and it does not by itself cross a compensation threshold. On these facts the $213 is **not** qualitatively
material, and the conclusion is that it is accumulated and passed, not that it must be corrected.

The instructive part is the contrast with Chapter 3's Extended Case Study, where a **smaller** amount — $310 — is
qualitatively material. The difference is not size; it is leverage. The $310 moved reported net revenue retention
from 111.4% to 112.0% and crossed a performance stock unit vesting threshold, so a quantitatively trivial amount
determined a disclosed metric and an executive compensation outcome. The $213 here has no such leverage: it changes
a growth rate in the third significant figure and touches no threshold. The lesson is that qualitative materiality
is not a general presumption that small revenue items matter; it is a specific question about whether *this* amount
determines *some* outcome, and it must be answered by identifying the outcome and computing the movement.

### Solution 4-14

| # | Counterparty | Paid | Distinct good or service, supported at fair value | Reduction of the transaction price (account 4900) | Reasoning |
| --- | --- | --- | --- | --- | --- |
| 1 | Meltham Partners | 160 | 96 | 64 | ASC 606-10-32-25 permits expense treatment only to the extent the payment is for a distinct good or service; deliverables evidence 60% of the spend, so $160 × 60% = $96 is an expense and the unevidenced $64 reduces revenue |
| 2 | Corvin Integration Group | 90 | 90 | — | A published rate card supports fair value; the payment does not exceed it |
| 3 | Dunmore Foods | 220 | 175 | 45 | A distinct service was received, but ASC 606-10-32-26 limits expense treatment to fair value; the $45 excess reduces revenue |
| 4 | Talbot Insurance | 140 | — | 140 | No deliverable is identified, so no distinct good or service was received and the entire payment reduces revenue |
| **Total** | | **610** | **361** | **249** | |

Proof: $96 + $90 + $175 = $361 of expense; $64 + $0 + $45 + $140 = $249 of contra-revenue; $361 + $249 = $610, which
equals $160 + $90 + $220 + $140 = $610.

**The payment to escalate is number 4.** A $140 payment to a customer described only as a "partnership fee," with no
identified deliverable, is a payment for which the business rationale has not been established. AS 2401 requires the
auditor to evaluate whether the business rationale for a significant unusual transaction suggests it was entered into
to engage in fraudulent financial reporting or to conceal misappropriation, and a payment to a customer
contemporaneous with a revenue transaction is the classic round-tripping pattern. The procedure is not to reclassify
$140 and move on: obtain the underlying agreement and the approval, determine who authorized it, compare its timing
to the revenue transactions with Talbot Insurance, and evaluate whether the revenue is genuine. Payment 3 also
requires an adjustment but raises no such question, because a competitive quote process evidences an arm's-length
purchase.

## Review Questions

**RQ 4-1.** What does the presumption of a fraud risk in revenue recognition presume, and what does it not presume?

**RQ 4-2.** State the substantive difference between AS 2110 and AU-C 240 on the revenue fraud presumption, and say
why it rarely changes the work in a subscription business.

**RQ 4-3.** Why is completeness normally a low-risk assertion for revenue accounts but a high-risk assertion for
account 4900?

**RQ 4-4.** Which three steps of AtlasFlow's order-to-cash cycle generate timestamps that its finance and sales
functions cannot edit, and why does that make those three steps the source of most of the chapter's evidence?

**RQ 4-5.** List the five criteria in ASC 606-10-25-1 that must be met before a contract exists for accounting
purposes.

**RQ 4-6.** Why does a termination-for-convenience clause usually not change reported revenue, and what three things
does it change?

**RQ 4-7.** What is the gateway condition for combining contracts under ASC 606-10-25-9, and what is its relationship
to the three criteria?

**RQ 4-8.** Explain how the constraint on variable consideration operates differently for consideration that would
increase the transaction price and consideration that would decrease it.

**RQ 4-9.** Why does the sales- and usage-based royalty exception not apply to AtlasFlow's workflow-run overage, and
what are the two routes that do support recognizing it as consumed?

**RQ 4-10.** When is the practical expedient in ASC 606-10-32-18 available, and why does it apply to every instalment
of C-1's ramped, annually billed consideration?

**RQ 4-11.** How is consideration payable to a customer accounted for, and what limits the amount that may be treated
as an expense?

**RQ 4-12.** Why must the service level credit population be built from availability data rather than from the
ledger, and which test of the availability data is most often skipped?

**RQ 4-13.** State, in the correct order, the two questions that decide presentation in a channel arrangement, and
explain why the order matters.

**RQ 4-14.** What are the two limbs of ASC 606-10-25-27(c), and which of them is answered by reading the contract
rather than by exercising accounting judgment?

**RQ 4-15.** Distinguish a control deviation from a misstatement, and give one example of each from December cut-off
testing.

**RQ 4-16.** Why is the revenue-to-billings-to-cash reconciliation blind to revenue overstatement, and which
assertion does it therefore address?

**RQ 4-17.** In a dual-purpose test, how is the sample size determined, and why may additional items be required
beyond that size?

**RQ 4-18.** What is the audit objective when testing a revenue disaggregation disclosure, and why is confirming that
each category foots to total revenue insufficient?

## Answers to Review Questions

**RQ 4-1.** It presumes the existence of a *risk* of material misstatement due to fraud in revenue recognition. It
does not presume that fraud has occurred, that the risk attaches to every revenue stream, or that it attaches to
every assertion. The auditor's obligation is to determine which types of revenue, which transactions, and which
assertions the risk attaches to, and to design a response for those. At AtlasFlow the risk attaches to occurrence
and cut-off for Core subscription, accuracy for Insight, and completeness for contra-revenue in account 4900.

**RQ 4-2.** AS 2110 directs the auditor to presume that a fraud risk involving improper revenue recognition exists
and provides no mechanism for rebutting the presumption at the revenue-caption level, only for identifying where it
attaches. AU-C 240 requires the auditor to *evaluate*, based on a presumption of fraud risks in revenue recognition,
which types of revenue give rise to them, and contemplates a documented conclusion that no such risk exists. In a
subscription business the difference rarely changes the work, because revenue is recognized ratably from a date held
in a field that a sales operations executive can edit, so the risk is structurally present.

**RQ 4-3.** Because the direction of management's incentive reverses with the sign of the account. Management is not
motivated to omit revenue from the top line, so completeness of accounts 4100 through 4210 is low risk. Every dollar
of credit omitted from account 4900 overstates revenue, so completeness of contra-revenue carries the same incentive
as overstatement of revenue. The practical consequence is that "completeness" cannot be assessed once for the revenue
caption; it must be assessed account by account.

**RQ 4-4.** Order form execution through DocuSign, tenant provisioning on the AtlasFlow platform, and subscription
creation in Zuora Billing. Each produces a timestamp written by a system outside the reach of the people whose
incentives bear on the accounting: the DocuSign completion certificate is generated by a third party, the
provisioning log is immutable once written, and the Zuora subscription carries its own creation audit trail. Since
the fraud risk is that a date was altered, evidence about dates is worth only as much as the alterability of its
source.

**RQ 4-5.** The parties have approved the contract and are committed to perform; each party's rights regarding the
goods or services to be transferred are identifiable; the payment terms are identifiable; the contract has commercial
substance; and it is probable that the entity will collect the consideration to which it will be entitled. All five
must be met.

**RQ 4-6.** Because the revenue pattern is the same either way: $1,440 recognized straight-line over 24 months and
$60 per month describe the same line, so C-5's FY2025 revenue is $240 under both the stated term and the 30-day
enforceable term. What changes is the remaining performance obligation disclosure (by $1,140 for C-5), the
amortization period for the related capitalized commission, and the split of deferred revenue between current and
noncurrent. Because it does not move revenue, it is routinely missed in a revenue-focused programme.

**RQ 4-7.** The gateway is that the contracts were entered into at or near the same time with the same customer or a
related party of the customer. It is a precondition, not one of the three criteria: if it is not met, no combination
is required regardless of the criteria; if it is met, combination is required if any one of the three criteria is
met. "At or near the same time" is a judgment with no bright line, which is why the Meridian Ambulatory analysis in
§4.4.5 worked all three criteria even though 208 days separated the documents.

**RQ 4-8.** Where variable consideration would increase the transaction price, the constraint holds the estimate
down: an amount may be included only to the extent it is probable that a significant revenue reversal will not
subsequently occur. Where variable consideration would decrease the transaction price — service credits, price
concessions, rights of return — the practical effect is the opposite: the entity must reduce the transaction price by
the amount it expects to give up, and the constraint guards against optimism that it will not have to. Practitioners
frequently apply the first logic to the second situation and end up overstating revenue.

**RQ 4-9.** The exception in ASC 606-10-55-65 applies only to consideration in exchange for a **license of
intellectual property**. AtlasFlow's Core offering is a hosted multi-tenant service; the customer never obtains the
software. The two routes that do work are the variable-consideration allocation exception in ASC 606-10-32-40, since
the overage relates specifically to the distinct daily service in the month the runs are consumed within a series,
and the right-to-invoice practical expedient in ASC 606-10-55-18 where the amount invoiced corresponds directly to
the value transferred to date.

**RQ 4-10.** The expedient is available where the period between the transfer of the good or service and the
customer's payment for it is one year or less. It applies to every instalment of C-1 because Meridian pays each
annual amount *in advance* of the twelve months of service it covers, so no instalment ever finances more than
twelve months. The ramp itself does not create a financing component: ASC 606-10-32-17 recognizes that a difference
between promised consideration and cash selling price can arise for reasons other than financing, and a phased seat
adoption schedule is such a reason.

**RQ 4-11.** Consideration payable to a customer is accounted for as a reduction of the transaction price unless the
payment is in exchange for a distinct good or service transferred to the entity. Expense treatment is limited to the
fair value of that distinct good or service; any excess reduces the transaction price. This is the most frequently
missed element of step 3 in a channel business, because the payments are made by marketing, coded to sales and
marketing expense, and never pass through the revenue process.

**RQ 4-12.** Because the assertion at risk is completeness, and the entries already in the account cannot provide
evidence about entries that are missing. The population must be built from the event that creates the obligation —
monthly availability by region — and then reconciled to the account. The test most often skipped is whether the
uptime calculation uses the **contractual** definition of downtime: management's availability report excluded all
scheduled maintenance, while the contracts exclude only windows notified 72 hours in advance and not exceeding four
hours per month. A window that fails that test lowers availability and can move contracts from the 10% credit band
to the 25% band.

**RQ 4-13.** First, who is the customer under ASC 606-10-15-3? Second, and only if the end customer is the customer,
does the entity control the specified good or service before transfer under ASC 606-10-55-36 through 55-40? The order
matters because being the principal is the reason to record **gross**. An analysis that starts from the
principal-versus-agent indicators and concludes "we are the principal, therefore net" states a premise that argues
for the opposite of its conclusion, which is exactly the defect in AtlasFlow's reseller memorandum.

**RQ 4-14.** The two limbs are that the entity's performance does not create an asset with an alternative use to the
entity, and that the entity has an enforceable right to payment for performance completed to date. The second is a
contract-reading procedure: you read the termination clause of the statement of work. AtlasFlow's standard statement
of work provides for payment of hours incurred to the termination date, so the limb is met; two of the 34 engagements
in progress at year end provided for payment only on milestone acceptance and failed it, which moved $118 of revenue
to the 2026 acceptance dates.

**RQ 4-15.** A control deviation is an instance in which a control did not operate as designed; it is evaluated
against a tolerable deviation rate and feeds the deficiency evaluation. A misstatement is a difference between a
recorded amount and the amount required by the framework; it is evaluated against materiality thresholds and feeds
the summary of audit differences. From December cut-off testing: the three items whose internal approval postdated
the customer signature are control deviations with no monetary effect; the six items with no evidence of execution
are misstatements totalling $150.

**RQ 4-16.** Because it is an identity that a fictitious transaction satisfies. A fictitious December invoice
increases revenue and increases the receivable by the same amount, so total invoicing rises, ending receivables
rise, and cash collected is unchanged — the bridge ties exactly. AtlasFlow's bridge ties to the dollar on a
population that includes all six uncorroborated order forms. The reconciliation addresses **completeness** of
revenue, and it is the most efficient procedure available for the risk that an amendment was billed and collected but
never recorded.

**RQ 4-17.** The sample size is the larger of the two individual requirements — the test of controls requirement and
the test of details requirement — never the average and never the sum. Additional items are required where the
control test needs coverage across the period of intended reliance and the substantive test is concentrated at the
period end. AtlasFlow's dual-purpose sample was 57 items drawn from December 24–31, and 26 further items were
selected from January through November so that the control conclusion covered the year, giving 83 items examined.

**RQ 4-18.** The objective is to audit the **categorization** — the attribute that assigns each transaction to a
disclosed category — not the total. The total is the audited revenue figure and cannot be wrong once the revenue
caption has been audited, so footing the table tests nothing that was at risk. AtlasFlow's geographic categories
footed perfectly to $148,200 while being built by contracting legal entity rather than on the disclosed basis of the
customer's billing address, misstating the EMEA category by $2,000, which is 138% of overall materiality.

## Key Definitions

**Agent.** An entity whose performance obligation is to arrange for another party to provide the specified good or
service to the customer. An agent recognizes revenue in the amount of the fee or commission to which it expects to
be entitled, which may be the net amount retained after paying the other party (ASC 606-10-55-38).

**Annual contract value (ACV).** The annualized committed subscription consideration under a contract, excluding
one-time fees and usage above committed volumes. It is not a GAAP measure and does not appear in the financial
statements, but it drives the remaining performance obligation disclosure, capitalized commissions, and the ARR
metric, which is why cut-off testing is stratified on it.

**Bookings.** The aggregate contract value signed in a period, whether or not invoiced or recognized as revenue. A
non-GAAP operating measure. AtlasFlow's Q4 FY2025 bookings were $61,400, of which $25,174, or 41%, was signed
December 24–31.

**Combination of contracts.** The requirement in ASC 606-10-25-9 to account for two or more contracts entered into at
or near the same time with the same customer, or with related parties of the customer, as a single contract if any
one of three criteria is met: the contracts were negotiated as a package with a single commercial objective; the
consideration in one depends on the price or performance of the other; or the promised goods or services are a single
performance obligation.

**Consideration payable to a customer.** Cash, credit, coupons, or vouchers payable to a customer or to the
customer's customer. Accounted for as a reduction of the transaction price unless the payment is in exchange for a
distinct good or service transferred to the entity, and then only up to the fair value of that good or service
(ASC 606-10-32-25 and 32-26).

**Constraint on variable consideration.** The requirement in ASC 606-10-32-11 to include variable consideration in
the transaction price only to the extent it is probable that a significant revenue reversal will not subsequently
occur. For consideration that would reduce the transaction price, its practical effect is to require recognition of
expected concessions rather than to defer them.

**Contra-revenue.** An account presented as a deduction from gross revenue rather than as an expense, comprising
amounts that reduce the transaction price: service credits, refunds, returns, and price concessions. AtlasFlow's
account 4900 carries $(1,900) for FY2025, netted within accounts 4100 through 4120.

**Contract asset.** An entity's right to consideration in exchange for goods or services it has transferred, when
that right is conditional on something other than the passage of time. It arises when cumulative revenue recognized
exceeds cumulative amounts invoiced for a contract, and it is measured at the contract level rather than by netting
across a portfolio.

**Cut-off.** The assertion that transactions have been recorded in the correct reporting period. In a subscription
business it is the dominant revenue assertion, because the recognition start date determines the amount recognized
and the date is the most easily altered input in the cycle.

**Dual-purpose test.** A single sample of items used both to test the operating effectiveness of a control and to
obtain substantive evidence about the monetary correctness of the transactions in the sample. The sample size is the
larger of the two individual requirements, and additional items may be needed to give the control conclusion coverage
across the period of intended reliance.

**Enforceable rights.** The rights and obligations that a party can compel through legal process. The contract term
for ASC 606 purposes is the period for which enforceable rights and obligations exist, which may be shorter than the
stated term — as with a contract terminable for convenience on 30 days' notice with no penalty.

**Expected value method.** A method of estimating variable consideration as the probability-weighted sum of the
possible consideration amounts. It is generally the better predictor where there is a large number of contracts with
similar characteristics (ASC 606-10-32-8).

**Field history.** A system-maintained record of changes to designated fields, capturing the prior value, the new
value, the user, and the timestamp. In Salesforce it is available for audited fields and cannot ordinarily be deleted
by the user who made the change, which makes it direct evidence about whether a date was altered.

**Gross versus net presentation.** Whether revenue is reported at the amount billed to the end customer, with the
intermediary's margin as a cost, or at the amount the entity is entitled to receive from the intermediary. It follows
from the identification of the customer and, where the end customer is the customer, from whether the entity is the
principal.

**Input method.** A method of measuring progress toward complete satisfaction of a performance obligation by
reference to the entity's inputs — labour hours, costs incurred, time elapsed — relative to total expected inputs.
Inputs that do not depict performance, such as rework caused by the entity's own error, must be excluded
(ASC 606-10-55-21).

**Most likely amount method.** A method of estimating variable consideration as the single most likely amount in a
range of possible amounts. It is generally the better predictor where the contract has only two possible outcomes
(ASC 606-10-32-8).

**Order form.** The transaction document that, together with an incorporated master subscription agreement, forms
the contract in an enterprise SaaS sale. It carries the SKUs, quantities, pricing, discount, term, start and end
dates, billing schedule, and signatures, and it is the document from which every downstream system is populated.

**Order-to-cash cycle.** The end-to-end process from opportunity creation through quotation, approval, execution,
provisioning, billing, revenue scheduling, general ledger posting, collection, and metric computation. At AtlasFlow
it spans Salesforce Sales Cloud and CPQ, DocuSign, the AtlasFlow platform, Zuora Billing, Zuora Revenue, NetSuite,
the bank feed, and the Snowflake RevOps datamart.

**Principal.** An entity that controls a specified good or service before it is transferred to the customer. A
principal recognizes revenue in the gross amount of consideration to which it expects to be entitled
(ASC 606-10-55-37). Indicators of control include primary responsibility for fulfilment, inventory risk, and
discretion in establishing the price to the customer, and they support rather than override the control assessment.

**Rate plan charge.** In Zuora Billing, the line-level construct that carries a charge model, list price, quantity,
and effective start and end dates for one element of a subscription. A ramped contract entered as three rate plan
charges with three effective dates can be treated by a revenue engine as three contracts, which changes the
recognition pattern without changing the transaction price.

**Revenue subledger.** The system that maintains contract-level performance obligations, allocations, and revenue
schedules and that posts summarized results to the general ledger. At AtlasFlow it is Zuora Revenue, which posts
monthly to NetSuite through interface I-3; the contract-level audit trail ends at the subledger, and the
subledger-to-ledger tie is a summary reconciliation.

**Sell-in and sell-through.** Sell-in recognition treats the intermediary's purchase as the revenue event, which is
appropriate where the intermediary's obligation to pay is unconditional. Sell-through recognition defers revenue
until the end customer commits, which is required where the intermediary owes nothing until the end customer accepts,
because until then the contract-existence criteria are not met.

**Service level agreement credit.** A contractual reduction in fees triggered when measured service availability
falls below a committed threshold. It is variable consideration reducing the transaction price, presented as
contra-revenue with a liability for amounts owed, and its audit population must be built from availability data
rather than from the accounting records.

**Side agreement.** Any arrangement, written or oral, that modifies the enforceable rights or obligations in the
contract documents and is not reflected in the systems that produce revenue. Common forms include acceptance rights,
contingent effectiveness, unilateral termination rights, future credits, and most-favoured-customer clauses.

**Significant financing component.** An implicit financing element arising where the timing of payments agreed by
the parties provides the customer or the entity with a significant benefit of financing the transfer of goods or
services. It requires adjustment of the promised consideration for the time value of money, subject to a practical
expedient where the period between transfer and payment is one year or less (ASC 606-10-32-15 and 32-18).

**Specified good or service.** The unit of account for the principal-versus-agent assessment: the distinct good or
service to be provided to the customer, identified before control is assessed (ASC 606-10-55-36). For a channel
subscription it is the right to the service for a stated term and quantity, not the service in the abstract.

**Transaction price.** The amount of consideration to which an entity expects to be entitled in exchange for
transferring promised goods or services, excluding amounts collected on behalf of third parties. It reflects
variable consideration and its constraint, any significant financing component, noncash consideration at fair value,
and consideration payable to a customer (ASC 606-10-32-2).

**Wet-ink execution.** Execution of a contract by physical signature outside an electronic signature platform. It is
not improper, but it removes the only evidence of the execution date that lies outside the entity's control, so a
wet-ink population requires a designed alternative procedure rather than an exception note.

## Chapter Summary

1. The presumption of a fraud risk in revenue recognition is a presumption about the existence of a risk, not about
   the occurrence of fraud, and the auditor's task is to determine which streams and assertions it attaches to —
   for AtlasFlow, occurrence and cut-off on Core subscription, accuracy on Insight, and completeness on
   contra-revenue.
2. Completeness carries opposite risk depending on the sign of the account: low for accounts 4100 through 4210,
   high for account 4900, because every unrecorded credit overstates revenue.
3. Only three steps in the order-to-cash cycle — execution, provisioning, and subscription creation — produce
   timestamps AtlasFlow cannot edit, and the cut-off response must be built on those three rather than on the
   Salesforce date fields that produced the accounting.
4. Contract existence is a five-criterion test, and the collectibility criterion is a recognition gate assessed at
   inception rather than a measurement question: concluding that a contract does not exist and concluding that a
   receivable is impaired produce different financial statements.
5. A termination-for-convenience clause does not move revenue, which is why it is missed; it moves the RPO
   disclosure, the commission amortization period, and the current/noncurrent split of deferred revenue.
6. The five-part side-agreement search works because only one part is inquiry; the highest-yield element is
   comparing the DocuSign envelope inventory for a customer to the documents filed in the contract repository.
7. The constraint on variable consideration operates in the opposite practical direction for amounts that reduce the
   transaction price: it requires recognition of the concessions the entity expects to grant, and the Northgate
   analysis puts the defensible range at $56 to $180 with the illustrated answer at $120.
8. The maximum FY2025 revenue exposure of the December 24–31 bookings population is $462 — less than performance
   materiality — while the same population carries $25,174 of RPO, $12,840 of receivables and deferred revenue, and
   a potential magnitude of $25,174 for the ICFR conclusion, which is why extent is sized on annual contract value
   rather than on the revenue effect.
9. Cut-off requires three populations, not one: order forms executed in the window, contracts with a start date in
   the period regardless of signature date, and order forms executed after the period end with a start date before
   it.
10. Provisioning corroborates the recognition start date and says nothing about contract approval, because
    provisioning is an act the entity performs unilaterally.
11. Control deviations and misstatements are evaluated against different criteria, communicated to different people,
    and aggregate differently; a combined exception count supports no conclusion about either.
12. The input method's denominator is the audit risk in professional services revenue, and the independent evidence
    exists in a system built for another purpose — the resource-management system's estimate-to-complete field —
    which produced a $95 difference and, more tellingly, a 27-to-5 directional split that is evidence of bias.
13. The billings bridge is an identity that a fictitious invoice satisfies; it addresses completeness of revenue and
    is blind to overstatement, so it cannot carry the cut-off assertion.
14. Presentation questions must be evaluated against the line items they distort rather than against the net loss:
    gross presentation of AtlasFlow's channel population would move revenue by $3,772, gross margin by 0.7 or 1.8
    percentage points, and disclosed ARR by 2.8%, while leaving the net loss at $(21,400) under every alternative.
15. A right answer supported by reasoning that does not support it is a control failure even when it is not a
    misstatement, and the remedy is a memorandum that identifies the customer, states the population attributes,
    evidences that the population shares them, and quantifies the alternative.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Assertion-level risk assessment for revenue, and the Q4 bookings concentration as a significant risk | Chapter 2, §2.12 and its case study | The risk assessments this chapter's procedures respond to |
| Overall materiality, performance materiality, the clearly trivial threshold, tolerable misstatement, and disclosure materiality | Chapter 3, §§3.2–3.11 | Every extent and evaluation decision in this chapter uses these numbers |
| Qualitative materiality and the NRR/performance stock unit interaction | Chapter 3, Extended Case Study | Why a $310 misstatement can matter more than a $213 one |
| Materiality in the ICFR audit and potential magnitude | Chapter 3, §3.14 | Why the wet-ink and SLA populations are measured by potential magnitude |
| Performance obligation identification, the series guidance, and material rights | Chapter 5, §§5.2–5.4 | Step 2 of the five-step model, deliberately not developed here |
| Standalone selling price and allocation, including the Insight critical audit matter | Chapter 5, §§5.5–5.7 | Step 4, and the allocation this chapter's figures deliberately avoid depending on |
| Contract modifications, ramped contracts, and usage revenue completeness | Chapter 5, §§5.8–5.10 | The recognition mechanics behind the revenue this chapter traces |
| Deferred revenue, the billings bridge in full, contract assets, and the RPO disclosure | Chapter 6, §§6.3–6.4, 6.8, 6.11 | The balance sheet consequences of everything in §4.9 and §4.10 |
| Receivable confirmations, including the reseller addressee question, and the CECL allowance | Chapter 7, §§7.5, 7.9–7.10 | The Cirrus/Tessera obligor point and the Meridian dispute's credit-loss half |
| Capitalized commissions and the ASC 340-40 amortization period | Chapter 10 | The commission exposure in Exhibit 4-23 and the referral fee in §4.7 |
| Revenue application controls, including the RevPro configuration and the CPQ approval matrix | Chapter 12, §§12.6, 12.8, 12.13 | The controls whose deviations this chapter identifies but does not evaluate |
| Evaluating control deficiencies and deviation rates | Chapter 14 | The severity assessment for the deviations and the significant deficiency |
| Sampling mechanics, including attribute sample sizes and upper deviation limits | Chapter 15 | The 15.2% upper deviation limit and the stratification arithmetic |
| Journal entry testing and the manual entries hitting revenue | Chapter 16 | The 41 manual revenue entries identified in §4.10.1 |
| Revenue fraud schemes, backdating, and the whistleblower allegation | Chapter 17 | What the six uncorroborated order forms look like as a scheme |
| Substantive analytical procedures over revenue | Chapter 18 | The analytic this chapter declines to let carry the cut-off assertion |
| Evaluating accumulated misstatements, bias, and subsequent events | Chapter 19, §§19.4, 19.6 | Where U-3, U-4, and the Meridian dispute are resolved |
| Non-GAAP measures, ARR and NRR, and the other-information requirements | Chapter 20 | Why the ARR effect of a presentation conclusion matters |

## Further Reading

- PCAOB AS 2110, *Identifying and Assessing Risks of Material Misstatement*, including the requirement to presume a
  fraud risk involving improper revenue recognition.
- PCAOB AS 2301, *The Auditor's Responses to the Risks of Material Misstatement*, on responses to significant risks
  and the requirement for an element of unpredictability.
- PCAOB AS 2401, *Consideration of Fraud in a Financial Statement Audit*, on required responses irrespective of
  assessed risk and on significant unusual transactions.
- PCAOB AS 1105, *Audit Evidence*, on the reliability of evidence and its sources.
- PCAOB AS 2310, *The Auditor's Use of Confirmation*, effective for audits of fiscal years ending on or after
  June 15, 2025.
- PCAOB AS 1215, *Audit Documentation*, for the documentation standard the workpapers in this chapter are written to.
- AICPA AU-C 240, *Consideration of Fraud in a Financial Statement Audit*, for the private-company formulation of the
  revenue fraud presumption.
- AICPA AU-C 315, *Understanding the Entity and Its Environment and Assessing the Risks of Material Misstatement*, as
  amended by SAS 145.
- AICPA AU-C 330, *Performing Audit Procedures in Response to Assessed Risks*, and AU-C 505, *External
  Confirmations*.
- AICPA AU-C 450, *Evaluation of Misstatements Identified During the Audit*, on accumulation and the evaluation of
  bias.
- FASB ASC 606, *Revenue from Contracts with Customers*, particularly 606-10-25 (contract existence, combination, and
  satisfaction of performance obligations), 606-10-32 (transaction price, variable consideration, financing,
  noncash consideration, and consideration payable to a customer), 606-10-50 (disaggregation and contract balances),
  and 606-10-55 (principal versus agent, the royalty exception, and the right-to-invoice expedient).
- FASB ASC 340-40, *Other Assets and Deferred Costs — Contracts with Customers*, for the treatment of referral fees
  and commissions.
- FASB ASC 326, *Financial Instruments — Credit Losses*, for the distinction between an expected concession and an
  expected credit loss.
- SEC Regulation S-X, Rule 5-03, on the separate statement of classes of revenue exceeding 10% of total revenue.
- SEC Staff Accounting Bulletin No. 116, which rescinded portions of SAB Topic 13 on adoption of ASC 606 and is worth
  reading to understand why pre-ASC 606 SEC staff revenue guidance should not be relied on.
- The AICPA audit and accounting guide covering revenue recognition, and the AICPA guide covering software and
  software-as-a-service entities, for industry implementation discussion of the topics in this chapter.

