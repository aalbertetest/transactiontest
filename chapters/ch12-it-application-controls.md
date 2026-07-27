# Chapter 12 — IT Application Controls and Automated Processing

> Nearly every defective test of controls in a first-year integrated audit fails for one of two reasons: the team
> misclassified the control, or the team accepted a system-generated report without testing it. Both failures are
> invisible in the workpaper, because a test designed for the wrong kind of control still produces a tick mark and
> a conclusion. AtlasFlow's FY2025 file contains 27 Zuora Revenue configuration rules changed once during the year
> with abbreviated user acceptance testing, a Salesforce CPQ approval matrix administered by the Vice President of
> Sales Operations whose own deals it governs, an interface error queue whose records can be deleted, a
> consolidation workbook on its fourteenth version, a 178-line Python function deployed twice without approval,
> and a Snowflake view that produces the annual recurring revenue (ARR) figure disclosed in Item 7. Not one of those is
> tested by a procedure that begins "obtained the report from the client."

## Learning Objectives

- **LO 12.1** Classify a control you have just been shown as a fully automated application control, an
  IT-dependent manual control, a configurable control, an interface control, or a producer of information produced
  by the entity, applying a four-question decision rule.
- **LO 12.2** Distinguish how a control operates from how it is tested, and state why the two are not the same
  document.
- **LO 12.3** Evaluate the design of input validation and edit checks, including identifying an edit check that
  constrains the wrong field.
- **LO 12.4** Re-perform an automated calculation using constructed test conditions and boundary values.
- **LO 12.5** Test a configured approval workflow, including the completeness of the exception population and the
  effect of mid-period configuration changes.
- **LO 12.6** Reconcile an interface on both record count and amount, and evaluate the error queue as a population.
- **LO 12.7** State the conditions that must hold about general IT controls before a test of one supports a
  full-period conclusion, and conclude whether they hold at AtlasFlow.
- **LO 12.8** Design and execute a completeness-and-accuracy test over a system-generated report, addressing its
  source, query, parameters, filters, reproducibility, and integrity in transit.
- **LO 12.9** Assess the risk in a spreadsheet in the financial reporting chain and select proportionate controls.
- **LO 12.10** Evaluate a script or robotic process automation routine as a change-management population and
  quantify the effect of unapproved modifications.
- **LO 12.11** Determine whether a metric produced in an uncontrolled reporting layer is within the scope of
  internal control over financial reporting, and design the audit response.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2201 | Requires testing of controls important to the conclusion on whether controls sufficiently address the assessed risk, and consideration of whether general IT control failures undermine reliance on automated application controls |
| PCAOB | AS 2201, Appendix B | Sets the conditions for benchmarking automated application controls, and excludes controls subject to human intervention |
| PCAOB | AS 1105 | Requires the auditor to test the accuracy and completeness of information produced by the entity (IPE) used as audit evidence |
| PCAOB | AS 2110 | Requires an understanding of the flow of transactions, the extent of automation, and risks arising from information technology |
| PCAOB | AS 2301 | Requires testing of the controls over, or the accuracy and completeness of, information produced by the entity that is used in performing a control |
| PCAOB | AS 2401 | Requires responsiveness to management override; unapproved configuration and script changes are an override vector |
| PCAOB | AS 1215 | Requires documentation an experienced auditor could follow — why an undated configuration screenshot is not evidence |
| PCAOB | AS 2710 | Requires the auditor to read other information and consider material inconsistency — the hook for the ARR figure in management's discussion and analysis (MD&A) |
| PCAOB | AS 1305 | Requires written communication of significant deficiencies and material weaknesses to the audit committee |
| AICPA | AU-C 315 (as amended by SAS 145, effective for periods ending on or after December 15, 2023) | Requires understanding of the IT environment, identification of risks arising from the use of IT, and identification of the general IT controls addressing them |
| AICPA | AU-C 500 (as amended by SAS 142, effective for periods ending on or after December 15, 2022) | Sets the attributes of information used as evidence — source, completeness, accuracy, authenticity, susceptibility to bias; more explicit than AS 1105 on IPE |
| AICPA | AU-C 330, AU-C 265, AU-C 720 | The analogues to AS 2301, AS 1305, and AS 2710 |
| SEC | Exchange Act Rule 13a-15 | Requires evaluation of disclosure controls and procedures, which reach MD&A metrics that ICFR alone may not |
| SEC | Regulation S-K Item 303 | Requires MD&A discussion of material trends and, per SEC staff interpretive guidance on key performance indicators, disclosure of how a presented metric is calculated |
| COSO | *Internal Control — Integrated Framework* (2013), Principles 10 and 11 | Control activities including general controls over technology; the framework used for management's Section 404(a) assessment |
| FASB ASC | 606-10-32-28 through 32-41 | The allocation requirements the Zuora Revenue rules RC-07 through RC-12 implement, and therefore the criteria for evaluating the configuration |
| FASB ASC | 718-10-25 and 718-10-30 | Requires accrual for performance conditions when achievement is probable — how the ARR metric enters the audited statements |

AtlasFlow is an SEC issuer, so PCAOB standards govern and Brightline LLP must opine on ICFR. Private-company
auditors apply the AICPA analogues with three differences that matter here. There is no ICFR opinion, so
misclassifying a control produces an unsupported reliance conclusion rather than a reportable material weakness.
AU-C 500 as amended by SAS 142 is more explicit than AS 1105 about the attributes of information used as evidence,
and the IPE schedule in §12.10 is organized around those attributes for that reason. And benchmarking has no
named AICPA analogue; a private-company auditor rolling forward automated control evidence relies instead on the
AU-C 330 provisions on evidence obtained in previous audits, which require establishing its continued relevance.

## Prerequisites and Chapter Dependencies

Read Chapter 11 first: every conclusion here is conditional on the general IT controls it scopes and tests, and
§12.9 is unintelligible without its conclusions on logical access (W-1, W-2, W-3, W-5, W-6) and program change
(W-4). Chapter 2 supplies the assessed risks that determine which automated controls are in scope and Chapter 3
the materiality figures used throughout ($1,450 overall, $940 performance materiality, $72 clearly trivial
threshold). Chapter 13 owns walkthrough technique and Chapter 14 owns test design mechanics, evidence
sufficiency, and deficiency severity; this chapter identifies deficiencies and states the team's conclusions but
does not grade them. Chapters 5, 6, 7, 9, 10, and 16 consume this chapter's output, because each relies on a
system-generated report or an automated calculation whose reliability is established here.

## 12.1 A Taxonomy, and a Decision Rule for Using It

Five kinds of control live at the application layer. They fail differently, are tested differently, and evidence
adequate for one is inadequate for another.

A **fully automated application control** operates entirely within the application, without human participation,
every time the triggering condition occurs. Zuora Revenue's allocation of a transaction price using a configured
standalone-selling-price table is fully automated. Its failure mode is systematic: if it is wrong it is wrong for
every transaction, which is why one well-designed test can support a conclusion and why an untested
misconfiguration is expensive.

An **IT-dependent manual control** has an irreducible human step, and that step consumes system-generated
information. The Controller's review and approval of the monthly Zuora Revenue-to-NetSuite summary journal
(interface I-3) is IT-dependent manual: Elena Vasquez performs the review, but against the RevPro "Revenue
Contract Summary" report. It fails in two ways — she does not review, or she reviews a report that omits
transactions. This is the category engagement teams misidentify most often, and the cost is precise: a team that
calls it a manual control tests the signature and never tests the report.

A **configurable control** is automated but its behavior is set by a value a business user can change without a
code deployment. NetSuite's requirement of a second approver at or above $250,000 (weakness W-12) is
configurable, as is every Coupa match tolerance and every CPQ discount threshold. Configurable controls have two
attributes to test rather than one: whether the mechanism works, and whether the value in it is the value it
should be, for the whole period.

An **interface control** operates on data moving between applications; AtlasFlow has nine (I-1 through I-9). It
addresses completeness first — did every record that left system A arrive in system B — then accuracy, then the
disposition of records that failed. The error-handling mechanism is part of the control, and an error queue
nobody owns is not a control.

A **system-generated report**, and more broadly **information produced by the entity (IPE)**, is not a control at
all. It is an input to controls and to audit procedures, and its reliability is established by testing
completeness and accuracy, not by testing whether somebody signed it.

### 12.1.1 The decision rule

Apply four questions in order, to the control as it actually operates rather than as its description reads.

**Question 1. Remove every person from the sequence. Is the misstatement still prevented or detected?** If yes,
the control is fully automated. If no, go to Question 2.

**Question 2. Does the irreducible human step consume information the system produced — a report, a queue, an
exception list, a calculated field?** If yes, it is an IT-dependent manual control and that information is IPE
whose completeness and accuracy are attributes of your test. If no, it is a manual control and this chapter does
not own it.

**Question 3. Is the automation's behavior driven by a value or rule a business user can change through the user
interface, without a code deployment?** If yes, the control is also configurable, and the configured value and
its change history for the period are attributes of your test.

**Question 4. Does the control operate on data crossing an application boundary?** If yes, it is also an
interface control, and your test must address completeness of the transfer and the disposition of failures.

Questions 3 and 4 are overlays, not alternatives. A control can be fully automated, configurable, and an
interface control at once, and the test must satisfy all three.

**Exhibit 12-1. The decision rule applied to eleven AtlasFlow controls.**

| # | Control as described by management | Q1 | Q2 | Q3 | Q4 | Classification | What the test must cover |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | CPQ prevents an order form reaching "Activated" until every required approval step is complete | Yes | — | Yes | No | Automated, configurable | Routing logic, threshold values, configuration change history, population completeness |
| 2 | Billing Analyst reviews the I-1 error queue daily and clears items | No | Yes | No | Yes | IT-dependent manual, interface | Evidence of review, plus completeness of the queue as a population |
| 3 | Zuora Revenue allocates the transaction price using configured SSP tables | Yes | — | Yes | No | Automated, configurable | Re-performance against ASC 606-10-32, SSP values, configuration change log |
| 4 | Controller reviews and approves the monthly I-3 journal before posting | No | Yes | No | Yes | IT-dependent manual, interface | Evidence and precision of review, plus completeness and accuracy of the RevPro report reviewed |
| 5 | NetSuite requires a second approver on entries of $250,000 or more | Yes | — | Yes | No | Automated, configurable | Whether the mechanism blocks posting, and whether $250,000 is defensible against $940 of performance materiality |
| 6 | Coupa performs a three-way match within configured tolerances | Yes | — | Yes | Yes | Automated, configurable, interface | Tolerance values, exempted categories, completeness of the invoice population reaching the match |
| 7 | Revenue Manager works exceptions on the I-2 nightly reconciliation | No | Yes | No | Yes | IT-dependent manual, interface | Evidence exceptions were worked, plus whether the reconciliation's parameters capture every record |
| 8 | The Stripe-to-NetSuite Lambda job posts a daily summary journal | Yes | — | No | Yes | Not a control — a process step | Nothing as a control; tested as change management and as a source of misstatement |
| 9 | Staff Accountant performs a daily Stripe cash-to-revenue reconciliation | No | Yes | No | Yes | IT-dependent manual, interface | Evidence of performance and reliability of the Stripe payout and NetSuite activity reports |
| 10 | The Snowflake RevOps datamart computes ARR and net revenue retention (NRR) for MD&A | n/a | n/a | n/a | n/a | Not a control — a producer of IPE | Completeness, accuracy, parameters, reproducibility, and reconciliation to the general ledger |
| 11 | Formulas in CONSOL_FY25_v14.xlsx translate FX and eliminate intercompany balances | Yes | — | Yes | Yes | End-user computing; no application-layer control exists | Formula integrity, version identification, access, review of output (§12.11) |

Items 8 and 10 carry the instruction. A script is not a control merely because it is automated; a control prevents
or detects a misstatement, and a script that posts entries *creates* the exposure a control must address. A
datamart is not a control either. A matrix whose key-control row reads "the Lambda job posts the daily journal"
has a hole in it exactly where the risk is.

## 12.2 How the Control Works Versus How You Test It

*How the control works* is a design statement: what the risk is, where in the transaction flow the mechanism
intervenes, what it does, what value governs it, who can change that value, and what happens to rejected items.
It is evaluated against a criterion — a GAAP requirement, a policy, an authority matrix approved by someone
entitled to approve it. *How you test it* is an evidence statement: what population, what attribute, what
technique, what sample, what constitutes a deviation, and what you do next if you find one. Three consequences
follow.

**A design conclusion and an operating-effectiveness conclusion do not substitute for each other.** The CPQ matrix
is well designed as to discount percentage and defective as to commercial terms that produce an economic discount
without touching the `Discount__c` field (§12.5). No amount of operating-effectiveness testing surfaces that;
reading the configuration against the policy does. Conversely, the matrix's defect as to *who* may satisfy the
Regional Sales Director step was introduced on November 7, 2025 and would be missed by a design evaluation
performed at the interim date.

**The criterion must exist before you test.** You cannot evaluate a configurable threshold without an approved
statement of what it should be. At AtlasFlow the discount authority matrix approved by the board's compensation
and pricing subcommittee in January 2025 is the criterion for CPQ, and the March 2024 delegation-of-authority
policy is the criterion for Coupa and journal entry approval. Where no criterion exists — the Coupa freight and
tax exemption in §12.7 — the finding is that design cannot be evaluated, which is itself a control environment
deficiency.

**The test must be capable of failing.** "Inspected the configuration and noted a second approver is required
above $250,000" is a description with a tick mark. A test states the attribute — the system does not permit an
entry of $250,000 or more to post with one approver — and the deviation condition — any entry in the population
of 1,065 at or above the threshold that posted with one approver, or any successful attempt in the constructed
test set. That can fail. The description cannot.

## 12.3 Input Controls: Validation and Edit Checks

Input controls address whether transactions entering the system are authorized, complete, accurate, and recorded
in the right period. In a SaaS order-to-cash flow they live in Salesforce CPQ and Zuora Billing and are almost
entirely configurable. There are eight recurring types, and naming the type tells you the test: **validity**
confines a field to a set; **format** to a pattern; **range and limit** to bounds; **dependency** requires field B
when field A takes a value; **duplicate** prevents a second record on the same key; **sequence** detects a gap;
**batch or control total** proves the parts equal the whole; **reasonableness** flags rather than blocks.

**Exhibit 12-2. Input validation configuration tested at December 31, 2025. Amounts in whole dollars.**

| Ref | Field | Configured rule | Type | Constructed test condition | Expected | Actual |
| --- | --- | --- | --- | --- | --- | --- |
| V-01 | `Subscription_Start_Date__c` | On or after signature date, not more than 90 days after | Range, dependency | Signature 12/15/2025, start 12/01/2025 | Blocked | Blocked |
| V-02 | `Term_Months__c` | Picklist 12, 24, 36 | Validity | Entered 18 | Blocked | Blocked |
| V-03 | `Discount__c` | 0.00 to 60.00, two decimals | Range | Entered 60.01 | Blocked | Blocked |
| V-04 | `Billing_Frequency__c` | Required where `Charge_Type` = Recurring | Dependency | Recurring charge, frequency blank | Blocked | Blocked |
| V-05 | Zuora billing account | Duplicate blocked on legal name plus tax identification number | Duplicate | Second account, identical name and TIN | Blocked | **Warned only, saved** |
| V-06 | Invoice run | Sum of invoice items must equal the header or the run aborts | Batch total | Re-performed the total on the December 2025 runs (4,118 invoices, $18,940 thousand) | Equal | Equal |
| V-07 | `PO_Number__c` | Required where `Requires_PO__c` = TRUE | Dependency | Requires PO true, number blank | Blocked | Blocked |
| V-08 | Overage rate per 1,000 runs | Greater than $0, not more than $50 | Range | Entered $0; entered $51 | Blocked both | Blocked both |

**V-05 warns rather than blocks.** The Zuora duplicate-account rule permits the save and writes an audit-trail
entry. The consequence is measurable: the 3,140-account enterprise population contains 26 pairs sharing a tax
identification number, of which 19 are legitimate affiliate structures and 7 are duplicates; 2 of the 7 carry
active subscriptions with aggregate ARR of $118, so that ARR and the related deferred revenue sit twice in the
subscription population although invoicing was issued once. When a result of this kind appears, do not expand the
sample — quantify the population effect and decide whether that population is one you rely on elsewhere. Here it
is, in §12.13.

**V-01 constrains the wrong field, which is the more serious finding.** AtlasFlow's policy (§4.1 of the
continuing case) recognizes subscription revenue "from the later of contract start date and provisioning date."
V-01 constrains the contractual start date against the signature date. Nothing in CPQ or Zuora Billing carries
the provisioning date; provisioning is recorded in the platform's own AWS tenant log, integrated with neither
system. There is therefore no automated control, and no IT-dependent manual control, capable of enforcing the
policy the company wrote. For purposes of this illustration, the absence of a provisioning-date field is the
mechanism by which corrected misstatement C-1 in Part 7 of the continuing case arose — $410 of revenue recognized
from March 15 rather than the April 2 provisioning date on 14 Q1 2025 contracts. When you evaluate an edit check,
do not ask whether it works. Ask what field it constrains, what field the accounting policy depends on, and
whether they are the same field.

## 12.4 Processing Controls and the Revenue Engine as a Rule Set

Processing controls address whether accepted transactions are calculated, allocated, scheduled, aggregated, and
posted correctly. In a subscription business the dominant set is the revenue engine's configuration. AtlasFlow runs
Zuora Revenue (RevPro) with **27 configuration rules**, and those 27 rules — not any person and not any narrative
— determine reported revenue of $148,200.

**Exhibit 12-3. The 27 Zuora Revenue configuration rules at December 31, 2025.**

| Group | Rule range | Count | What it determines | Criterion |
| --- | --- | --- | --- | --- |
| Performance obligation identification | RC-01 to RC-06 | 6 | Charge combination, the series treatment, separation of services | ASC 606-10-25-14 through 25-22; policy §4.1 |
| SSP and allocation | RC-07 to RC-12 | 6 | SSP tables by SKU and geography, allocation, discount allocation, residual test | ASC 606-10-32-28 through 32-41; the Insight SSP memo |
| Revenue schedule and timing | RC-13 to RC-19 | 7 | Straight-line spreading, daily versus monthly convention, ramps, start-date derivation | ASC 606-10-25-27 through 25-37 |
| Modification handling | RC-20 to RC-24 | 5 | Prospective, cumulative-catch-up, and separate-contract treatment | ASC 606-10-25-10 through 25-13 |
| Netting, FX, and GL mapping | RC-25 to RC-27 | 3 | Contract-level netting, functional currency, mapping to 4100/4110/4120/2400/2410 | ASC 606-10-45; ASC 830 |
| **Total** | | **27** | | |

Three observations shape the strategy. **The rules are the control and the schedule is the output**: testing 40
contract schedules tests the output 40 times and the rule set zero times, and if RC-16 spreads monthly where the
policy is daily, a sample of 40 shows 40 immaterial differences that look like rounding. **A rule can be right and
applied to the wrong population**: RC-20 correctly implements cumulative catch-up, but whether an amendment is
flagged as a ramp restructuring is a picklist value a Billing Analyst sets from nine amendment reason codes, so
the attribute you test is the accuracy of the reason code, not the arithmetic. **The February 2025 change is the
most important IT event in the revenue cycle**: change ticket CHG-2025-0188, deployed February 14, 2025, modified
RC-13, RC-14, RC-20, and RC-21 to accommodate ramped contracts, which matter because roughly 34% of ACV sits in
multi-year contracts with escalators or ramps. The change was deployed with abbreviated user acceptance testing
(UAT). Quantify "abbreviated" rather than repeating the adjective: the
plan listed 22 test cases, the signed results document 6 executed, all six positive-path cases with a straight
ramp and no amendment, zero negative or boundary cases, and the UAT approver was Daniel Kim, who owns the
configuration and requested the change.

### 12.4.1 Re-performing a configured calculation

Inspection tells you RC-13 says "recognize the allocated amount ratably over the performance period, daily
convention." Re-performance tells you it does. The test runs in the RevPro non-production instance after
confirming, by comparing a configuration export of all 27 rules across the 41 attributes exported per rule, that
the instances are identical (27 records, zero field-level differences).

**Exhibit 12-4. Constructed test conditions for the ramp rules. Amounts in thousands.**

| Case | Construction | Expected | Actual | Pass |
| --- | --- | --- | --- | --- |
| TC-RAMP-01 | 36-month subscription, ramped $100 / $140 / $160, total $400, starts on the first | $11.11 in months 1–35, $11.15 in month 36; total $400.00 | Agreed | Yes |
| TC-RAMP-02 | As above but starting on the 15th | First and last months prorated by days (17/31 and 14/31); total $400.00 | Agreed | Yes |
| TC-RAMP-03 | TC-RAMP-01 amended in month 13 to extend 12 months for $180 at SSP | Prospective; no adjustment to months 1–12 | Agreed | Yes |
| TC-RAMP-04 | TC-RAMP-01 amended in month 13 to raise years 2 and 3 to $165 each; revised total $430 | Cumulative catch-up of $10.00 in month 13, then $11.94 per month for 24 months | **Prospective applied; no catch-up** | **No** |
| TC-RAMP-05 | TC-RAMP-01 amended in month 13 to reduce year 3 to $120; revised total $360 | Cumulative catch-up of $(13.33) in month 13, then $10.00 per month for 24 months | **Prospective applied** | **No** |
| TC-RAMP-06 | Ramp with a zero-dollar first year | Total spread over 36 months; no revenue-free period | Agreed | Yes |

The TC-RAMP-01 arithmetic is worth checking rather than accepting: $400 ÷ 36 = $11.1111; $11.11 × 35 = $388.85;
$400.00 − $388.85 = $11.15 in the final month, and the rounding residue lands in one place. Had the final month
shown $11.11 and the schedule totaled $399.96, the $0.04 leak across 14,392 contracts would be $576, or 39.7% of
overall materiality. Rounding conventions are worth ten minutes. The TC-RAMP-04 expectation derives the same way:
the revised total of $430 over 36 months is $11.9444 per month, cumulative revenue through month 12 should be
$143.33, revenue actually recognized on the original price was $133.33, so the catch-up in month 13 is $10.00 and
the remaining $286.67 spreads over 24 months at $11.94.

TC-RAMP-04 and TC-RAMP-05 failed. Both failures are in RC-20 and RC-21, both rules were touched by CHG-2025-0188,
and both are the negative cases the abbreviated UAT did not execute. The next step after an unexpected
re-performance result is fixed: determine whether the defect exists in production, and quantify. The team
reproduced both failures against a copy of the production configuration and then queried the FY2025 amendment
population.

**Exhibit 12-5. FY2025 amendments and the quantified effect of the defect. Amounts in thousands.**

| Amendment reason code | Count | Contract value | Correct treatment | Applied | FY2025 revenue effect |
| --- | --- | --- | --- | --- | --- |
| 04 — Ramp restructuring | 31 | 8,410 | Cumulative catch-up | Prospective | 218 |
| 07 — Mid-term price concession | 19 | 3,260 | Cumulative catch-up | Prospective | (104) |
| 09 — Term extension at SSP | 146 | 24,900 | Prospective | Prospective | — |
| 02 — Quantity increase at SSP | 289 | 41,700 | Prospective | Prospective | — |
| **Total** | **485** | **78,270** | | | **114** |

Counts foot to 485 and values to $78,270. The net effect of $114 is immaterial, but $218 and $(104) each exceed
the $72 clearly trivial threshold, so both are accumulated even though they substantially offset. The control
conclusion matters more than the amount: a processing control was changed during the period, tested by the person
who requested the change, and the resulting defect was found by the auditor rather than the company. Chapter 14
grades that.

## 12.5 Workflow and Approval Configuration: the Salesforce CPQ Discount Approval Matrix

Approval workflow is where authorization becomes automated. CPQ holds the discount approval matrix that governs
whether a quote can become an order form, and the order form initiates everything downstream — the Zuora
subscription through I-1, the revenue schedule through I-2, the journal through I-3.

**Exhibit 12-6. Approval process AP-CPQ-01 as configured, exported December 31, 2025, against the discount
authority policy approved January 2025.**

| Tier | Policy discount band | Policy approver(s) | Configured entry criterion | Configured approver | Agrees? |
| --- | --- | --- | --- | --- | --- |
| T0 | 0.00% to 10.00% | None | `Discount__c <= 10` | None | Yes |
| T1 | 10.01% to 20.00% | Regional Sales Director | `Discount__c > 10 AND <= 20` | Step 1: any member of `Sales_Leadership` | **No** |
| T2 | 20.01% to 30.00% | Regional Sales Director and VP Sales Operations | `Discount__c > 20 AND <= 30` | Steps 1 and 2: `Sales_Leadership`, then B. Hallowell | Partially |
| T3 | 30.01% to 40.00% | Chief Revenue Officer | `Discount__c > 30 AND <= 45` | Step 3: S. Marchetti | **No — upper bound 45%** |
| T4 | Above 40.00% | Chief Revenue Officer and Chief Financial Officer | `Discount__c > 45` | Steps 3 and 4: S. Marchetti, then T. Okafor | **No** |
| Non-standard terms | Payment terms beyond net 60, non-standard legal terms, any ramp | Deal Desk and Corporate Controller | `Non_Standard_Terms__c = TRUE` | Step 5: Deal Desk queue | **Partially — Controller absent** |

Four findings come from one configuration export read against one policy, which is the best evidence-per-hour
ratio in the chapter.

**The T3/T4 boundary moved from 40% to 45% on December 18, 2025.** The Salesforce Setup Audit Trail records
"Approval Process AP-CPQ-01 — changed entry criteria on step 3 and step 4," user `bhallowell`, December 18, 2025,
19:42 CT. No Jira ticket, no approval by anyone other than the person who made the change. Twenty-three order
forms activated December 18–31 carried discounts of 40.01% to 45.00% with aggregate ACV of $4,180; 21 of them
would have required CFO approval before the change and did not obtain it, and 2 obtained it anyway.

**The Regional Sales Director step can be satisfied by 14 people, 3 of whom carry quotas.** The November 7, 2025
change replaced the named-role assignment on step 1 with the `Sales_Leadership` public group, whose membership at
year end is 14 users. Salesforce prevents a submitter from approving their own record, so nobody self-approved,
but reciprocal approval is not prevented: two of the three quota-carrying members approved each other's quotes on
11 order forms with aggregate ACV of $2,940. The mechanism enforced the rule it was configured to enforce, and the
configuration expressed the wrong rule.

**The matrix governs a field that does not capture economic discount.** CPQ computes `Discount__c` as one minus
net price over list price on the quote lines. A 24-month contract quoted as 21 paid months plus 3 free months
carries `Discount__c` of 0.00%, because the free months are zero-price lines outside the list basis; the economic
discount is 3 ÷ 24 = 12.50%, which under policy requires Regional Sales Director approval. A query for order forms
with a zero-price line and positive quantity returns 31 order forms, aggregate ACV $6,720, effective discounts
from 4.17% (1 free month of 24) to 20.83% (5 of 24), none approved, and 26 that would have required at least T1
approval on an effective-discount basis. This is a design deficiency, undetectable by operating-effectiveness
testing, because the control operated exactly as designed on all 31.

**The Corporate Controller is not in the non-standard-terms path.** Step 5 routes only to the Deal Desk queue —
four members, all in Sales Operations reporting to B. Hallowell. Every ramped contract in FY2025, the population
that drove CHG-2025-0188, was therefore approved for commercial terms with no accounting review.

### 12.5.1 The population and the exception population

Two populations are required, and teams routinely obtain only the first.

**Exhibit 12-7. FY2025 CPQ order forms in Activated status by configured tier. Amounts in thousands.**

| Tier | `Discount__c` range | Order forms | Order-form ACV |
| --- | --- | --- | --- |
| T0 | 0.00% to 10.00% | 902 | 18,240 |
| T1 | 10.01% to 20.00% | 1,148 | 37,610 |
| T2 | 20.01% to 30.00% | 796 | 44,180 |
| T3 | 30.01% to 40.00% | 431 | 33,290 |
| T4 | Above 40.00% | 135 | 18,580 |
| **Total** | | **3,412** | **151,900** |

Counts sum to 3,412 and ACV to $151,900, of which the $61,400 of Q4 bookings in §3.1 of the continuing case is a
component. The C-4 Cirrus Retail Group reseller order form, at a 28% discount to list to Tessera Partners, sits in
T2. The exception population is produced by a query you run, not by a sample.

```sql
-- Exception query: activated order forms lacking an approval required by POLICY.
WITH ordf AS (
  SELECT q.id AS quote_id, q.order_form_number__c, q.activated_date__c,
         q.discount__c, q.acv__c,
         CASE WHEN q.discount__c <= 10 THEN 0
              WHEN q.discount__c <= 20 THEN 1
              WHEN q.discount__c <= 30 THEN 2
              WHEN q.discount__c <= 40 THEN 3
              ELSE 4 END AS policy_tier        -- policy tiers, not configured tiers
  FROM   sfdc.quote q
  WHERE  q.status = 'Activated'
    AND  q.activated_date__c BETWEEN '2025-01-01' AND '2025-12-31'
    AND  q.isdeleted = FALSE
),
appr AS (
  SELECT pi.targetobjectid AS quote_id,
         MAX(CASE WHEN ps.stepname = 'RSD'  THEN 1 ELSE 0 END) AS rsd,
         MAX(CASE WHEN ps.stepname = 'VPSO' THEN 1 ELSE 0 END) AS vpso,
         MAX(CASE WHEN ps.stepname = 'CRO'  THEN 1 ELSE 0 END) AS cro,
         MAX(CASE WHEN ps.stepname = 'CFO'  THEN 1 ELSE 0 END) AS cfo
  FROM   sfdc.processinstance pi
  JOIN   sfdc.processinstancestep ps ON ps.processinstanceid = pi.id
  WHERE  ps.stepstatus = 'Approved'
  GROUP BY 1
)
SELECT o.order_form_number__c, o.activated_date__c, o.discount__c, o.acv__c, o.policy_tier,
       COALESCE(a.rsd,0) rsd, COALESCE(a.vpso,0) vpso,
       COALESCE(a.cro,0) cro, COALESCE(a.cfo,0) cfo
FROM   ordf o LEFT JOIN appr a ON a.quote_id = o.quote_id
WHERE (o.policy_tier >= 1 AND COALESCE(a.rsd,0)  = 0)
   OR (o.policy_tier >= 2 AND COALESCE(a.vpso,0) = 0)
   OR (o.policy_tier >= 3 AND COALESCE(a.cro,0)  = 0)
   OR (o.policy_tier  = 4 AND COALESCE(a.cfo,0)  = 0)
ORDER BY o.acv__c DESC;
```

Three features are the reason for showing it. It classifies against **policy** tiers, so a configuration that
disagrees with policy produces exceptions instead of disappearing. It filters `isdeleted = FALSE`, which obliges
you to consider deleted quotes separately. And it reads approvals from `ProcessInstanceStep`, the system's record
of what happened, rather than from a status field a user can set.

**Exhibit 12-8. Exception query results and disposition. Amounts in thousands.**

| Category | Order forms | ACV | Disposition |
| --- | --- | --- | --- |
| Effective discount from zero-price free months; `Discount__c` = 0.00 | 31 | 6,720 | Design deficiency; no operating deviation |
| Activated 12/18–12/31 at 40.01%–45.00% without CFO approval | 21 | 3,760 | Deviation and an unauthorized configuration change |
| Approved by email outside CPQ and force-activated by the administrator | 9 | 2,180 | Deviation |
| Reciprocal approval between two quota-carrying `Sales_Leadership` members | 11 | 2,940 | Design deficiency |
| Subscriptions created directly in Zuora Billing with no CPQ order form | 177 | 9,340 | Control not applied |
| **Total** | **249** | **24,940** | |

Counts sum to 249 and ACV to $24,940. The 21 order forms are the subset of the 23 above that did not obtain CFO
approval, $3,760 of the $4,180. The last line changes the audit: **proving the completeness of the exception
population requires proving the completeness of the base population**, and the base population is not the order
forms in CPQ but the subscriptions in Zuora Billing that generate revenue.

**Exhibit 12-9. Completeness reconciliation, CPQ order forms to Zuora Billing subscriptions, FY2025.**

| Item | Records |
| --- | --- |
| Zuora Billing subscriptions and amendments created 01/01/2025 – 12/31/2025 | 3,589 |
| Less: created by the I-1 integration user `svc_sfdc_zuora` (traceable to a CPQ order form) | (3,412) |
| **Created directly by named human users** | **177** |
| Of which: created by Billing Analysts to correct an I-1 mapping failure, order form on file | 132 |
| Of which: created for the October 2025 Kestrel migration under a documented plan | 34 |
| Of which: created with no order form identifiable in Salesforce | 11 |
| **Total accounted for** | **177** |

The 177 reconcile (132 + 34 + 11) and 3,412 + 177 = 3,589. The 11 with no identifiable order form, aggregate ARR
$640, generate revenue and never passed through the authorization control, which makes the statement "all revenue
transactions are authorized through the CPQ approval matrix" false and requires revisiting any conclusion that
relied on it. The team traced all 11 to executed agreements, obtaining contracts for 9 and, for 2 ($112 of ARR),
only an email from a sales representative; those 2 were referred into the whistleblower procedures in Chapter 17.

## 12.6 System-Enforced Segregation of Duties and Thresholds That Defeat the Control

A system can enforce segregation of duties by denying one user two conflicting permissions, by preventing a user
from acting twice on a record, or by requiring a second party above a configured value. All three are
configurable, and all three can be configured into uselessness.

Weakness W-12 is the clearest case. NetSuite requires a second approver only at or above **$250,000**, and of the
**4,912** manual entries posted in FY2025, **3,847** fell below the threshold with no evidence of independent
review; 1,065 were at or above it. Do not stop at reciting the weakness — evaluate the threshold against
materiality, because that is what determines severity.

**Exhibit 12-10. Precision analysis of the $250,000 approval threshold. Amounts in thousands.**

| Measure | Amount | Derivation |
| --- | --- | --- |
| Manual entries at or above the threshold (reviewed) | 1,065 entries, 118,700 | Absolute value posted |
| Manual entries below the threshold (unreviewed) | 3,847 entries, 22,200 | Absolute value posted |
| **Total manual entries** | **4,912 entries, 140,900** | Agrees to §3.6 of the continuing case |
| Average unreviewed entry | 5.77 | 22,200 ÷ 3,847 |
| One unreviewed entry at the cap, as a percentage of performance materiality | 26.6% | 250 ÷ 940 |
| Entries at the cap required to exceed overall materiality | 6 | 1,450 ÷ 250 = 5.8, rounded up |

A threshold permitting six unreviewed entries to aggregate above overall materiality is not set at a level of
precision that would prevent or detect a material misstatement on a timely basis. Given $940 of performance
materiality a defensible threshold is $50 to $100; the evidence that would move that range is the actual amount
distribution of the 3,847 entries, which here does not help, because 96 manual entries carried round-dollar
amounts of $100,000 or more (§3.6).

W-13 is the other half. The Controller can prepare and post journal entries and can modify the RevPro-to-NetSuite
interface mapping. Where one person can prepare an entry, post it, and change the mapping that determines which
account automated entries hit, segregation of duties over the manual path is irrelevant because the automated path
is open. That is why Question 4 exists: an interface is a posting channel, and access to configure it is access to
post.

## 12.7 The Automated Three-Way Match

Coupa matches purchase order, receipt, and supplier invoice and blocks payment where they disagree beyond a
configured tolerance. It is the archetypal fully automated configurable control and is almost always configured
more loosely than the policy it implements.

**Exhibit 12-11. Coupa match configuration at December 31, 2025 against the March 2024 procurement policy.
Tolerances in whole dollars.**

| Match attribute | Configured | Policy | Assessment |
| --- | --- | --- | --- |
| Quantity variance, receipt to invoice | 0% | 0% | Agrees |
| Unit price variance, PO to invoice | Lesser of 5% or $500 | Lesser of 2% or $250 | Exceeds policy |
| Invoice total variance | $1,000 absolute | $250 | Exceeds policy |
| Freight and tax lines | Excluded from matching | Not addressed | Design cannot be evaluated |
| Non-PO invoices permitted | 14 expense categories | 6 categories | Exceeds policy |
| Duplicate invoice check | Supplier, invoice number, amount; hard block | Required | Agrees |

Of **18,410** supplier invoices processed in FY2025, **14,806** were PO-backed and matched automatically and
**3,604** were non-PO requiring manual approval (14,806 + 3,604 = 18,410). Within the 14,806, **2,318** matched
with a variance above the $250 policy tolerance but within the $1,000 configured tolerance, aggregating **$86**
thousand, an average of $37 per invoice in whole dollars. Nobody reviewed any of them. The aggregate is 5.9% of
overall materiality and would not change an opinion; the deficiency is that 2,318 invoices at the configured cap
is $2,318 thousand of theoretical exposure, 160% of overall materiality, and the company cannot demonstrate it
would detect systematic overbilling below $1,000 per invoice. The freight-and-tax exclusion is a different
finding: there is no policy statement, so there is no criterion, so design cannot be evaluated. Record that rather
than defaulting to "appears reasonable," size the excluded population ($1,840 thousand of freight and tax lines in
FY2025), and identify whether a compensating control exists — Avalara for the tax component, nothing for freight.

## 12.8 Interface Controls, Error Queues, and Cross-System Reconciliation

Interface risk is fundamentally a completeness risk, and completeness failures in an interface have three distinct
sources: records never selected for transfer, records selected that failed, and records transferred and transformed
incorrectly. A reconciliation on amount alone detects only the third; only a record-count reconciliation detects
the first two.

**Exhibit 12-12. The nine AtlasFlow interfaces, the control on each, and the test.**

| Ref | Path | Classification | Principal "what could go wrong" | Test performed |
| --- | --- | --- | --- | --- |
| I-1 | CPQ → Zuora Billing | Interface plus IT-dependent manual queue review | Activated order form creates no subscription; billing and deferred revenue understated | Queue completeness reconciliation to the Zuora API log; 25 cleared items; year-end open-item follow-through |
| I-2 | Zuora Billing → Zuora Revenue | Interface plus IT-dependent manual exception process | Billing transactions never reach the revenue engine | Independent re-performance of the December record-count and amount reconciliation (walkthrough) |
| I-3 | Zuora Revenue → NetSuite | Interface plus IT-dependent manual review | Subledger total ≠ journal posted; wrong account mapping | Output control totals for 12 months; mapping test to 4100/4110/4120/2400/2410 |
| I-4 | Stripe → NetSuite | Interface via in-house code; the control is the daily reconciliation | Self-serve revenue and cash misstated by an unapproved code change | Change population; re-execution in a sandbox (§12.12) |
| I-5 | ADP / Deel → NetSuite | Interface via templated CSV plus manual reconciliation | Register does not agree to the GL; template columns shift | Register-to-GL reconciliation, two periods; template comparison |
| I-6 | Carta → SBC workbook | Manual export; end-user computing downstream | Grant population incomplete; roll-forward breaks | Grant count and total, Carta to workbook, at three dates |
| I-7 | Coupa → NetSuite | Interface, fully automated | Approved invoices not posted, or posted twice | Nightly control totals for one month; full-year duplicate query |
| I-8 | NetSuite, Zuora, Salesforce → Snowflake | Interface with **no reconciliation control for three quarters** (W-11) | Every downstream extract, analytic, and metric unreliable | Row-count and control-total comparison, source to replica, at 12/31/2025 |
| I-9 | Bank → NetSuite | Interface plus manual clearing | Cash transactions unmatched and unrecorded | Unmatched item aging at 12/31/2025 (Chapter 8) |

### 12.8.1 An error queue is a population before it is a control

The I-1 control is "automated field mapping; error queue reviewed daily by Billing Analyst." The review is worth
nothing if the queue is incomplete, so test the queue first.

**Exhibit 12-13. I-1 integration error queue, FY2025. Amounts in thousands.**

| Item | Records | ACV affected |
| --- | --- | --- |
| Error records in the Salesforce object `Integration_Error__c` | 1,246 | |
| Cleared within 1 business day | 1,081 | |
| Cleared in 2 to 5 business days | 141 | |
| Cleared after more than 5 business days | 20 | |
| Open at December 31, 2025 | 4 | 412 |
| **Total, agreeing to the object record count** | **1,246** | |
| Failed API responses in the Zuora inbound audit log, FY2025 | 1,258 | |
| **Difference — error records absent from the Salesforce object** | **12** | 214 |

The clearing categories sum to 1,246. The 12-record difference is the finding: the records were hard-deleted on
July 18, 2025 by the shared integration account `svc_zuora_api` during a bulk cleanup, so the company cannot
demonstrate they were reviewed and the deletion is not attributable to a person. The consequence is precise:
evidence that the analyst reviewed the queue daily supports a conclusion about the records *in* the queue and
cannot support a conclusion about the completeness of billing, because the population the sample was drawn from is
incomplete. Extending the sample does not help; you need a different population. Using the Zuora audit log as the
population, the team traced all 12 deleted records — 10 became subscriptions within four days, and 2 (ACV $56)
were not created at all until the auditor raised them in November 2025. The 4 items open at year end required
direct follow-through: 3 relate to order forms activated December 29–31 with combined ACV of $412 for which no
subscription, invoice, receivable, or deferred revenue existed at year end, and 1 is a zero-dollar amendment.

### 12.8.2 Output controls: control totals and the subledger-to-ledger tie

**Exhibit 12-14. I-3 summary journal JE-2025-12-0417, posted January 6, 2026, and the December output control
totals. Amounts in thousands.**

| Account | Description | Debit | Credit |
| --- | --- | --- | --- |
| 2400 | Deferred revenue — subscription, current | 12,760 | |
| 4100 | Subscription revenue — Core | | 9,540 |
| 4110 | Subscription revenue — Insight | | 2,690 |
| 4120 | Usage overage revenue | | 530 |
| 2410 | Deferred revenue — noncurrent | 1,180 | |
| 2400 | Deferred revenue — current (reclassification to current) | | 1,180 |
| | **Totals** | **13,940** | **13,940** |

| Tie-out | Amount |
| --- | --- |
| RevPro "Revenue Contract Summary," December 2025, subscription revenue recognized | 12,760 |
| Credits to accounts 4100, 4110, 4120 in JE-2025-12-0417 | 12,760 |
| **Interface difference** | **—** |
| NetSuite general ledger activity in 4100, 4110, 4120 for December 2025 | 12,918 |
| **Difference — manual entries posted directly to revenue accounts** | **158** |

Revenue credits foot to $12,760 and the journal balances at $13,940. The interface ties exactly, which is the
expected result and worth only the time it takes to check. The informative number is the $158: six manual entries
were posted directly to revenue accounts in December, bypassing the subledger. An output control reconciling the
interface to the subledger cannot detect them by construction, which is why the subledger-to-ledger reconciliation
must be performed at the account level rather than at the interface level. Those six entries are selections for
Chapter 16.

## 12.9 Inspection, Re-performance, and the Test of One

Three techniques are available for a configured automated control and they are not interchangeable. **Inspection**
of the configuration establishes what the setting is; it is the only technique that finds a design defect such as
the T3 boundary at 45%, and it establishes nothing about operation. **Re-performance** with constructed conditions
establishes that the mechanism operates as configured; it is the only technique that finds TC-RAMP-04. **A test of
one** — inspecting a single actual transaction that passed through the control — establishes that the control
operated on at least one real transaction. Its attraction is that automated logic does not tire, so one item can
support a full-period conclusion. Its danger is that the inference from one to all rests entirely on conditions
outside the test.

Four conditions must hold. State them in the workpaper and conclude on each.

1. **The control is wholly automated**, with no human judgment in its operation. Otherwise sample size is driven by
   control frequency under Chapter 14's tables.
2. **Program change controls were effective for the entire period**, so a change could not have been made and
   reversed between your test date and the period boundaries.
3. **Logical access to the configuration was appropriately restricted for the entire period**, so the set of people
   who could have changed it is known and small.
4. **You hold independent evidence of the configuration's stability across the period** — a change log covering
   January 1 to December 31 in which every change is identified, attributable to a named individual, and approved.

Condition 4 is a substantive procedure, not a restatement of 2 and 3, and it is where AtlasFlow fails.

**Exhibit 12-15. Configuration changes to the 27 Zuora Revenue rules, FY2025, per the RevPro configuration audit
log.**

| Source | Changes | Rules touched | Attributable? | Approved? |
| --- | --- | --- | --- | --- |
| CHG-2025-0188, deployed February 14, 2025 | 4 | RC-13, RC-14, RC-20, RC-21 | Yes (D. Kim) | Requested, tested, and approved by the same person |
| Changes with a Jira ticket and independent approval | 5 | RC-07, RC-09, RC-11, RC-25, RC-27 | Yes | Yes |
| Changes made by the shared `revpro_admin` account | 2 | RC-16, RC-22 | **No (W-1)** | **No ticket** |
| **Total FY2025 changes** | **11** | | | |

Two of eleven changes cannot be attributed, because the `revpro_admin` password sits in a shared vault entry
accessible to six people (W-1) and two developers hold standing write access to production configuration (W-6).
Conditions 3 and 4 fail. A test of one performed in December on RC-16 supports a conclusion about RC-16 in December
and nothing else.

The response is to convert the test of one into **a test of one per configuration state**. For AP-CPQ-01 the Setup
Audit Trail shows changes on November 7 and December 18, producing three states — January 1 to November 6,
November 7 to December 17, and December 18 to December 31 — and therefore three tests, each supporting a conclusion
only for its own window. For the RevPro rules the same logic applies, but two state boundaries are undocumented, so
no test establishes what the configuration was before them. Where that is true the automated control cannot be
relied on for the period and the evidence must be obtained substantively, here by recomputing revenue for a sample
of contracts in each quarter (Chapter 5, §5.11).

**Benchmarking** — carrying forward prior-period evidence about an automated control without retesting — is
addressed in AS 2201, Appendix B. It requires that the control be automated, that general IT controls over program
change, access to programs, and computer operations be effective, and that the auditor verify the program or
configuration has not changed, ordinarily by comparing a current configuration export to the one tested; it is not
appropriate where the control is subject to human intervention or where the application changes frequently.
Benchmarking is unavailable to Brightline in FY2025 for two independent reasons: FY2025 is AtlasFlow's first
integrated audit, so no baseline exists at the depth an ICFR audit requires, and the general IT controls the
technique depends on are not effective (W-1 through W-6). Note the sequencing this implies: the benefit accrues
only to teams that establish a documented baseline in year one, so the FY2025 configuration exports must be
archived in a form that supports a field-level comparison in FY2026.

## 12.10 System-Generated Reports and the Completeness and Accuracy of IPE

This is the area where the most control testing and the most substantive testing fails, and the mechanism is
always the same: the report is treated as a given rather than as an output whose properties must be established.
Whenever a report is used — as the basis for a control, as a sampling population, as the schedule you tie the
statements to, as the input to an analytic — the same eight attributes must be addressed, and each has its own
evidence.

**Exhibit 12-16. The eight attributes of a system-generated report, applied to the RevPro "Revenue Contract
Summary" used in the I-3 control.**

| # | Attribute | What must be true | Evidence obtained | Result |
| --- | --- | --- | --- | --- |
| 1 | **Source** | The report reads the system of record, not a copy | Report definition shows it reads `RC_SCHEDULE` and `RC_POB` in the production schema; no intermediate table | Satisfied |
| 2 | **Query or logic** | The logic selects and aggregates what the title claims | Obtained the definition export (RPRO_RPT_0114, 3 pages); read the join and grouping logic; recomputed one grouping level from the detail extract | Satisfied |
| 3 | **Parameters** | The parameters for this instance are known and reproducible | Footer prints period = 2025-12, entity = four legal entities, basis = "recognized"; captured in the workpaper | Satisfied |
| 4 | **Filters and exclusions** | Every filter is identified and appropriate | Three filters: contract status ≠ Cancelled, POB status ≠ On Hold, legal entity IN (4). **"On Hold" excludes 41 performance obligations carrying $196 of December revenue** | **Not satisfied** |
| 5 | **Completeness at source** | The source table holds all transactions for the period | Reconciled `RC_SCHEDULE` December activity to the I-2 interface load (Exhibit 12-21) and to Zuora Billing | Satisfied after adjustment |
| 6 | **Reproducibility** | Re-running with the same parameters returns the same result | Re-ran January 19 and February 3, 2026; identical totals; as-of-parameter driven rather than `CURRENT_DATE` driven | Satisfied |
| 7 | **Integrity in transit** | The file you hold is the file the system produced | Generated in a screen-share session with J. Pike, exported in the auditor's presence; record count 14,392 and control total $12,760 noted at receipt | Satisfied |
| 8 | **Change control** | The definition has not changed in a way affecting comparability | Report audit log shows one change on March 3, 2025 adding a column; no change to filters or logic | Satisfied |

Attribute 4 is the finding, and it shows why filters are the highest-yield attribute. Forty-one performance
obligations were "On Hold" at December 31, 2025 — a status Revenue Accounting applies to contracts under
commercial dispute — and the report excludes them, so their $196 of December revenue is absent from the report the
Controller reviews, from the I-3 journal, and from the general ledger. Whether the $196 should have been
recognized is an ASC 606 question for Chapter 5; the point here is that the control's information source is
silently incomplete, so the control could not have detected the omission however carefully it was performed. When
a filter of this kind appears, obtain the excluded population, quantify it, and re-perform the control with the
filter removed to see whether the conclusion changes.

Three disciplines separate real IPE testing from its imitation. **Obtain the report yourself, or watch it being
produced**; a CSV emailed by the client is a file, not a report, and the record count and control total must be
recorded at the moment of receipt so a later version can be compared. **Test the query, not the total**: a report
that ties to the general ledger can still be incomplete, because both can be missing the same transactions —
Exhibit 12-14's journal ties perfectly and both exclude the same 41 obligations, so tying two outputs of one query
to each other is circular, and completeness requires an independent population. **Distinguish the report's
reliability from the underlying accounting**: IPE testing establishes that the schedule faithfully represents what
is in the system and says nothing about whether what is in the system is right. Teams that write "IPE tested"
and then perform no substantive work have confused a precondition for evidence with evidence.

## 12.11 Spreadsheets and End-User Computing in the Financial Reporting Chain

A spreadsheet in the reporting chain is an application with no change management, no access control, no audit
trail, and one user. `CONSOL_FY25_v14.xlsx` is item 20 of the application inventory and weakness W-8: no version
control, no formula-integrity check, emailed among four people. It performs FX translation, intercompany
elimination, and the 27 top-side entries that never touch NetSuite. Assess the risk on four axes before selecting
controls, so the response is proportionate.

**Exhibit 12-17. Risk assessment of CONSOL_FY25_v14.xlsx. Score 1 (low) to 3 (high).**

| Axis | Measurement | Score |
| --- | --- | --- |
| Complexity | 26 worksheets; 18,942 formula cells; 1,204 external links to 3 files; 14 array formulas; 8 nested `IF`/`VLOOKUP` combinations more than four levels deep | 3 |
| Use | Produces the consolidated trial balance that becomes the primary financial statements; no downstream check | 3 |
| Judgment content | 27 top-side entries, $6,200 of absolute value, prepared and reviewed within a four-person group | 3 |
| Exposure to change | 14 saved versions in FY2025; 4 users with edit rights; SharePoint version history retained but never used as a control; no cell protection | 3 |

A workbook scoring 3 on all four axes requires the full set: restricted write access, locked formula cells, a
documented change log, independent formula-integrity review after each structural change, input reconciliation to
source, and output reconciliation to an independent expectation. AtlasFlow has none of them.

**Exhibit 12-18. The 27 top-side consolidation entries, FY2025. Absolute value in thousands.**

| Type | Count | Absolute value |
| --- | --- | --- |
| Intercompany elimination | 9 | 2,410 |
| FX translation and cumulative translation adjustment true-up | 6 | 1,140 |
| Kestrel purchase accounting | 4 | 1,290 |
| Reclassification between captions | 5 | 890 |
| Accrual and estimate adjustment | 3 | 470 |
| **Total, agreeing to §3.6 of the continuing case** | **27** | **6,200** |

Counts sum to 27 and values to $6,200. The workbook produced a real misstatement through the most common
spreadsheet failure there is. The `TB_Load` tab imports each entity's trial balance from a saved NetSuite report;
the `MAP` tab assigns accounts to captions using `VLOOKUP` against the static range `$A$2:$C$413`. When the UK
trial balance was refreshed on January 14, 2026, its row count had grown from 412 to 418 because six accounts were
opened in Q4 2025, and the lookup range was not extended. The six accounts, totaling **$312**, fell out of the
mapped consolidated trial balance into a line labeled "Unmapped — to review," which nobody reviewed. The $312
comprises accrued VAT of $180, accrued professional fees of $74, and other accrued expenses of $58 (180 + 74 + 58
= 312). For purposes of this illustration, this mapping failure is the mechanism by which corrected misstatement
C-4 — the $180 understatement of accrued VAT in the UK entity — arose. Management corrected the range in version
15.

At $312 the misstatement is 21.5% of overall materiality and 33.2% of performance materiality: too small to change
an opinion, too large to ignore, above the $72 clearly trivial threshold, and therefore accumulated. The control
conclusion is independent of the amount. A workbook in which a static lookup range silently drops six accounts,
in which no formula-integrity check would have caught it, and whose plug line is titled "to review" and is not
reviewed, is a deficiency in the close process regardless of what this year's error happened to total.

## 12.12 Scripts and Robotic Process Automation

Interface I-4 is not a vendor product. It is **178 lines of Python** in the repository `atlasflow/fin-integrations`,
deployed as an AWS Lambda function named `stripe-netsuite-daily-je`, triggered by EventBridge at 04:15 CT, which
reads the prior day's Stripe balance transactions and posts a summary journal entry to NetSuite. It carries $6,100
of annual revenue across 11,400 self-serve accounts. Weakness W-7 records that two FY2025 modifications have no
documented change approval. Treat the script as a change-management population first and as a source of
misstatement second.

**Exhibit 12-19. Change population for `stripe-netsuite-daily-je`, FY2025.**

| Item | Count |
| --- | --- |
| Commits to the function's source path | 14 |
| Commits never deployed to production (feature branches, reverted) | 5 |
| Production deployments with an approved pull request and a Jira ticket | 7 |
| **Production deployments with neither an approved pull request nor a ticket (W-7)** | **2** |
| **Total commits accounted for** | **14** |

The counts foot. The procedure matters as much as the table: the population came from the Git log for the function's
path, cross-checked to the CircleCI deployment history and the Lambda version history in AWS, because a deployment
can occur without a commit and a commit without a deployment. Reconciling all three is how you establish the change
population is complete. Then read the two unapproved changes and quantify them.

**Commit `a7f3c21`, deployed March 6, 2025**, changed fee handling from gross presentation — revenue at the gross
charge with Stripe processing fees in account 5100 — to netting fees against revenue. Self-serve billings for
March 6 through December 31 were $5,002 (82% of the $6,100 annual figure) at a blended fee rate of 2.96%, giving
**$148** of understatement in both revenue and cost of subscription revenue, with no effect on the net loss.
Netting a processor's fee against revenue is not supportable: AtlasFlow is the principal in the transaction with
the customer and the fee is a cost of collecting, not a reduction of the transaction price.

**Commit `e91b40d`, deployed September 22, 2025**, added a retry loop around the NetSuite posting call with no
idempotency key. Three duplicate daily journals resulted, totaling **$57**; the daily cash-to-revenue
reconciliation caught and reversed two within the same month, and one duplicate of **$21** posted November 4, 2025
remained unreversed at year end. The reconciliation therefore operated at a detection rate of two of three, which
is a control deviation rather than a design failure.

The re-performance procedure for a script is direct: obtain the input file for a specific day, execute the
production version of the function against it in a sandbox with the NetSuite endpoint mocked, and compare the
generated journal to the journal actually posted. For November 4 the team did that, reproduced the duplicate, and
so demonstrated the defect existed in the deployed code rather than inferring it from the symptom.

Two generalizations apply to any scripted routine in the reporting chain. The bot is a user: it holds credentials
that need the same provisioning, review, and least-privilege treatment as a person's, and `svc_stripe_lambda`
holds a NetSuite role permitting both journal creation and posting — a conflict no human at AtlasFlow is permitted
to hold. And the bot has no judgment, so every exception it cannot handle either fails loudly or is silently
absorbed; establish which, and find the queue.

## 12.13 The Data Warehouse and Cloud Configuration Drift

Snowflake is item 13 of the application inventory and the source of most audit data extracts, of the ARR and NRR
figures in MD&A, and of reports several accounting processes now rely on. Access to it is broader than access to
the source systems, it is fed hourly by Fivetran through I-8, and until December 2025 there was no reconciliation
to the general ledger (W-11). A reporting layer with those properties is an uncontrolled production environment
producing numbers that carry the appearance of system generation. The extended case study develops the
consequences; two structural points precede it. A replica is not the source: `_fivetran_deleted` and
`_fivetran_synced` metadata mean a Snowflake table can contain rows deleted upstream and omit rows created since
the last sync, so a query that ignores those columns returns a population that is neither the source population nor
a defined subset of it. And when audit extracts come from the warehouse, the warehouse is part of your evidence
chain, so you must reconcile it to source — row count and control total, at the extract date — for the specific
tables you use, whether or not management does.

**Cloud configuration drift** is the tendency of vendor-hosted application settings to change between the date you
test and the date your conclusion covers, without a code deployment and often without a ticket. It has three
sources: administrators changing settings through the user interface (AP-CPQ-01 on November 7 and December 18);
vendor releases that alter defaults or add settings (the September 2025 NetSuite upgrade, during which the
segregation-of-duties roles were rebuilt); and infrastructure-as-code applies that overwrite manual changes or are
overwritten by them. The response is mechanical: for every configurable control you rely on, obtain the
application's own configuration audit trail for the full period rather than a point-in-time export, and reconcile
every change in it to a ticket. Where the trail is not retained for the full period — Salesforce retains Setup
Audit Trail entries for a limited window — obtain it early and say so in the workpaper. A team first requesting a
configuration audit trail in February 2026 for the year ended December 31, 2025 may find the January and February
2025 entries are simply gone, and no subsequent effort recovers them.

## Step-by-Step Walkthrough: Testing the Salesforce CPQ Discount Approval Configuration and the I-2 Zuora Billing-to-Zuora Revenue Interface Reconciliation

One continuous procedure performed by C. Nwosu and B. Osei between December 8, 2025 and January 22, 2026,
documented at WP 4100-22 (CPQ) and WP 4100-31 (I-2). Tick marks: **(a)** agreed to a system-generated report the
auditor obtained; **(b)** recomputed by the auditor; **(c)** traced to an executed source document; **(d)** inquiry
corroborated by inspection; **(e)** exception, documented at WP 4100-49.

**Step 1. Obtain the criterion before looking at the system.** Request the discount authority policy in force during
FY2025 and the minutes approving it. You obtain the "Global Discount and Deal Approval Authority Matrix," version
4.0, and the subcommittee minutes of January 22, 2025. **(c)** If the only policy provided is undated or dated after
year end, stop: there is no criterion, design cannot be evaluated, and that is the finding.

**Step 2. Export the configuration; do not screenshot it.** In Salesforce Setup, open Approval Processes, select
AP-CPQ-01, and request the full definition — entry criteria, step criteria, approver assignment per step, approval
and final approval actions, and the "allow submitter to approve" flag — as a PDF printed in your presence with the
footer showing user and timestamp, plus the Metadata API export if the client will run it. What you need is the six
thresholds and six approver assignments in Exhibit 12-6. **(a)**

**Step 3. Compare configuration to policy line by line and record every difference.** Do not summarize. This
produces four differences: the T3 upper bound at 45% against a policy 40%; the T4 criterion at above 45%; step 1
assigned to a 14-member public group rather than a named role; and the omission of the Corporate Controller from the
non-standard-terms path. **(a) (e)**

**Step 4. Obtain the configuration audit trail for the full period.** Request the Setup Audit Trail filtered to the
approval process and the `Sales_Leadership` group for January 1 through December 31, 2025. Two entries are relevant:
November 7, step 1 approver changed from role to public group; and December 18 at 19:42 CT, step 3 and step 4 entry
criteria changed, both by `bhallowell`. Cross-reference each to Jira; neither has a ticket. **(a) (e)** If the trail
returns nothing, confirm the retention window rather than concluding the configuration was stable.

**Step 5. Convert the change dates into configuration states and size each.** Three states: January 1 to November 6
(310 days), November 7 to December 17 (41 days), December 18 to December 31 (14 days). Order forms activated in each
are 2,704, 431, and 277, totaling 3,412 **(b)**, agreeing to Exhibit 12-7. A test of one now means one test per
state, and the third state is the one in which the December bookings concentration occurred.

**Step 6. Re-perform the routing with constructed boundary conditions in the CPQ full sandbox.** First prove the
sandbox matches production by comparing AP-CPQ-01 metadata field by field (41 fields, zero differences). Then build
eight quotes on one product bundle with a list price of $412,000 in whole dollars, varying only net price: $370,900
(9.98%), $370,800 (10.00%), $370,760 (10.01%), $329,600 (20.00%), $329,560 (20.01%), $286,340 (30.50%), $247,200
(40.00%), and $226,600 (45.00%). Verify the arithmetic on at least one: $412,000 − $286,340 = $125,660, and
$125,660 ÷ $412,000 = 30.50%. **(b)** Expected results follow the configured criteria, not policy. All eight routed
as configured: the mechanism works and the configuration is wrong.

**Step 7. Test the escape hatches, because that is where the control fails.** Attempt to approve your own submission
as a `Sales_Leadership` member — blocked, as expected. Have a second `Sales_Leadership` member approve a 22% quote —
permitted, so reciprocal approval is available. **(e)** Build a 24-month quote priced as 21 paid months plus 3
zero-price months and observe `Discount__c` — it returns 0.00% and routes to no approver although the economic
discount is 12.50%. **(b) (e)** That third test is the design finding in §12.5 and took eleven minutes.

**Step 8. Prove the completeness of the population you will draw exceptions from.** Do not accept the CPQ order-form
count as the population of revenue-generating arrangements. Reconcile the 3,589 Zuora Billing subscriptions and
amendments created in FY2025, obtained directly from Zuora, to the 3,412 created by the I-1 integration user, and
account for the 177 difference by creator and reason (Exhibit 12-9). Trace the 11 with no identifiable order form to
executed contracts. **(a) (b) (c)** Nine produced contracts; two did not, and those go to the engagement partner the
same day, because a revenue-generating subscription with no order form and no contract is a matter for Chapter 17,
not for a control workpaper.

**Step 9. Run the exception query yourself against data you have reconciled.** Execute the SQL in §12.5.1 against
the Snowflake Salesforce replica, then reconcile the replica's FY2025 activated-quote row count to the count from
Salesforce directly (3,412 in both) and confirm `_fivetran_deleted` is filtered. The query returns 249 exceptions and
$24,940 of ACV (Exhibit 12-8). **(a) (b) (e)** If the counts disagree, you cannot use the replica; go to the source.

**Step 10. Turn to I-2 and obtain the reconciliation as management performs it, before saying what you think it
should be.** You receive the December 2025 instance prepared by J. Pike on January 5, 2026 and initialed by D. Kim on
January 7, 2026. **(a)**

**Exhibit 12-20. Management's December 2025 I-2 reconciliation as prepared. Amounts in thousands.**

| Line | Records | Amount |
| --- | --- | --- |
| Zuora Billing transactions created 12/01–12/31/2025 eligible for transfer | 118,463 | 18,940 |
| Loaded to Zuora Revenue in batches run 12/01–12/31/2025 | (114,341) | (17,671) |
| Held in the interface error table `RPRO_STAGE_ERR` at 12/31/2025 | (412) | (196) |
| Rejected as duplicate keys and auto-suppressed by the connector | (65) | (32) |
| **Unexplained difference, annotated "timing, immaterial"** | **3,645** | **1,041** |

**Step 11. Establish what the two populations actually are.** Ask what date field defines each side, and corroborate
by reading the report definition: `transaction_created_date` for the source and `batch_run_date` for the loaded
side. **(d)** Those are different clocks. The nightly batch runs at 02:00 CT carrying the prior day's activity, so
comparing transactions created in December to batches run in December is offset by one day at each end. The $1,041 is
not an unexplained difference; it is an artifact of the reconciliation's own design, and its recurrence every month
is why nobody investigates it.

**Step 12. Re-perform the reconciliation with the windows aligned.** Re-run both sides yourself, matching batches run
December 2, 2025 through January 1, 2026 to transactions created in December.

```sql
-- Source side: Zuora Billing transactions eligible for transfer to Zuora Revenue.
SELECT COUNT(*) AS records, ROUND(SUM(amount)/1000, 0) AS amount_thousands
FROM   zuora.transaction_extract
WHERE  transaction_created_date >= '2025-12-01'
  AND  transaction_created_date <  '2026-01-01'
  AND  transfer_eligible_flag = 'Y';

-- Loaded side: records accepted by Zuora Revenue, matched on the source transaction key.
SELECT COUNT(*) AS records, ROUND(SUM(s.amount)/1000, 0) AS amount_thousands
FROM   rpro.rc_stage_loaded s
WHERE  s.batch_run_date       >= '2025-12-02' AND s.batch_run_date       < '2026-01-02'
  AND  s.source_created_date  >= '2025-12-01' AND s.source_created_date  < '2026-01-01';
```

**Exhibit 12-21. Auditor's re-performed December 2025 I-2 reconciliation. Amounts in thousands.**

| Line | Records | Amount |
| --- | --- | --- |
| Zuora Billing transactions created 12/01–12/31/2025 eligible for transfer | 118,463 | 18,940 |
| Loaded in batches run 12/02/2025–01/01/2026, source-created in December | (117,986) | (18,712) |
| Held in `RPRO_STAGE_ERR` at 12/31/2025 | (412) | (196) |
| Rejected as duplicate keys and auto-suppressed | (65) | (32) |
| **Unexplained difference** | **—** | **—** |

Both columns foot: 117,986 + 412 + 65 = 118,463 and 18,712 + 196 + 32 = 18,940. **(b)** The reconciliation can be
performed and does balance; management's version was not wrong in its arithmetic but was blind by construction.
That distinction drives severity: the design is deficient, and no diligence in performing it would compensate.

**Step 13. Interrogate the 65 auto-suppressed records, because the reconciliation is built to make them disappear.**
The connector suppresses records whose composite key already exists in the target. Obtain all 65 and test whether
each is genuinely a duplicate: 58 are re-sends of loaded records, and 7, with $4 of amount, are distinct credit memo
items that collided because the key omits the credit memo line number. **(b) (e)** The finding is not the $4; it is
that a suppression rule inside an interface is a silent deletion mechanism, so a reconciliation treating
suppressions as explained cannot detect a class of completeness failure.

**Step 14. Age the error table and follow the old items through.** Do not accept a total.

**Exhibit 12-22. `RPRO_STAGE_ERR` at December 31, 2025, aged by first error date. Amounts in thousands.**

| Age | Records | Amount | Disposition tested |
| --- | --- | --- | --- |
| 0 to 7 days | 168 | 41 | 25 selected; all cleared by January 14, 2026 |
| 8 to 30 days | 179 | 74 | 25 selected; all cleared by January 20, 2026 |
| 31 to 90 days | 51 | 58 | All 51 read; 44 cleared, 7 open |
| Over 90 days | 14 | 23 | All 14 read; 11 relate to a cancelled contract; 3 are unprocessed credit memos totaling $18 |
| **Total** | **412** | **196** | |

Both columns foot (168 + 179 + 51 + 14 = 412; 41 + 74 + 58 + 23 = 196). **(a) (b)** The three unprocessed credit
memos of $18 understate contra-revenue account 4900 and are accumulated. Fourteen items older than 90 days is prima
facie evidence that the "exceptions worked by the Revenue Manager" control did not operate for those items; the
count is the deviation, and one deviation is enough to require you to consider whether the control can be relied on
at all (Chapter 14).

**Step 15. Tie the interface output to the subledger and the subledger to the ledger, separately.** Perform
Exhibit 12-14's two-part tie. The interface-to-subledger tie is exact at $12,760; the subledger-to-ledger tie leaves
$158 of manual entries posted directly to revenue accounts. **(a) (b)** Had the interface tie *not* been exact, the
next step is to obtain the connector's load log and identify the failed records, not to plug the difference.

**Step 16. Roll interim conclusions forward, re-obtain the configuration, and write a conclusion that states what it
covers.** Controls tested at the October 31, 2025 interim date must be rolled forward, and for a configurable
automated control the roll-forward is a re-export of the configuration at December 31 compared to the October 31
export plus the audit trail for the intervening 61 days — which is what produced the December 18 finding. The
defensible conclusion is that the CPQ control operated as configured throughout FY2025 but the configuration did not
agree to the approved authority matrix from December 18, permitted reciprocal approval within a 14-member group from
November 7, and never captured discounts delivered through zero-price periods; and that the I-2 reconciliation
control is deficient in design because its comparison windows are misaligned and its suppression treatment is
unexamined. Neither control may be relied on to reduce substantive testing over revenue. If instead you write
"operates effectively," identify which of the five findings your conclusion asserts did not happen.

## Extended Case Study: The ARR Figure in MD&A Produced by an Unreconciled Snowflake Datamart

### Background

In November 2025 AtlasFlow moved the computation of annual recurring revenue and net revenue retention out of a
Revenue Operations spreadsheet into a Snowflake view in the RevOps datamart, so that the board deck, the investor
relations model, and Item 7 of the Form 10-K would draw on one source. The datamart is fed hourly from NetSuite,
Zuora, and Salesforce by Fivetran through interface I-8. Weakness W-11 records that it was not reconciled to the
general ledger for the first three quarters of FY2025.

### The Facts

The draft Form 10-K circulated to the audit committee on January 12, 2026 disclosed ARR at December 31, 2025 of
**$175.9 million**, described in Item 7 as 28.0% growth and cited in the earnings release as evidence that Q4
bookings had converted to recurring revenue. The figure came from `REVOPS.MART.V_ARR_MONTHLY` for month 2025-12.
Nobody outside Revenue Operations had recomputed it, four people hold roles permitting them to alter the view, and
the view is not under source control.

```sql
CREATE OR REPLACE VIEW REVOPS.MART.V_ARR_MONTHLY AS
SELECT DATE_TRUNC('month', CURRENT_DATE()) AS arr_month,
       a.account_id, a.account_name,
       SUM(rpc.mrr * 12)                   AS arr
FROM   FIVETRAN_ZUORA.SUBSCRIPTION_RATE_PLAN_CHARGE rpc
JOIN   FIVETRAN_ZUORA.SUBSCRIPTION s ON s.id = rpc.subscription_id
JOIN   FIVETRAN_ZUORA.ACCOUNT      a ON a.id = s.account_id
WHERE  s.status = 'Active'
  AND  rpc.effective_start_date <= CURRENT_DATE()
  AND  (rpc.effective_end_date  >= CURRENT_DATE() OR rpc.effective_end_date IS NULL)
GROUP BY 1, 2, 3;
```

Four defects are visible in eleven lines. There is no charge-type filter, so one-time services fees and usage
overage are annualized into a metric AtlasFlow's own definition excludes. `CURRENT_DATE()` appears three times, so
the view is not reproducible as of a past date and returns a different answer each day it is run.
`_fivetran_deleted` is not filtered on any of the three tables, so soft-deleted rows persist. And there is no
exclusion of Kestrel accounts migrated into Zuora in October 2025 while the legacy Kestrel feed remained active.

### What the Engagement Team Did

T. Iyer recomputed ARR independently from the Zuora Billing source — not the replica — as of December 31, 2025,
applying AtlasFlow's stated definition: the annualized value of recurring subscription charges in force at the
measurement date, excluding one-time fees and usage overage.

**Exhibit 12-23. Reconciliation of the draft MD&A ARR figure to the auditor's recomputation. Amounts in thousands.**

| Ref | Item | ARR |
| --- | --- | --- |
| | ARR per `V_ARR_MONTHLY` as disclosed in the January 12, 2026 draft | 175,860 |
| (a) | Subscriptions terminated effective 12/31/2025 whose amendment was booked 01/02/2026; still 'Active' in the replica | (1,840) |
| (b) | Usage overage annualized contrary to the stated definition | (1,260) |
| (c) | Kestrel accounts counted twice — migrated October 2025 with the legacy feed active | (740) |
| (d) | One-time professional services fixed fees on 19 contracts annualized | (410) |
| (e) | Multi-year escalators measured at the current rather than the next-twelve-month contracted rate | 390 |
| | **Auditor's recomputed ARR on the stated definition** | **172,000** |

The column foots: 175,860 − 1,840 − 1,260 − 740 − 410 + 390 = 172,000. The gross difference of $3,860 is 2.2% of
the draft figure. Items (a) through (d) are errors; item (e) is a definitional refinement management accepted.

The team then traced the metric forward into the financial statements. The ARR-based performance stock units contain
a tranche whose performance condition is ARR of at least **$170,000** at December 31, 2025. Management assessed
achievement as 100% probable in Q3 2025 and revised it to 85% in Q4, recording a **$1,340** catch-up credit (§3.5).
A 15-percentage-point revision producing $1,340 implies a fully-probable cumulative measure of $1,340 ÷ 0.15 =
**$8,933**, of which $8,933 × 0.85 = **$7,593** remains in accumulated expense at December 31, 2025.

### Analysis

**What kind of control failure is this?** Not a failure of an application control — there is no control. The ARR
computation is an uncontrolled query written by one team, changeable by four people, not under source control, not
reconciled to the general ledger for three quarters, and not independently reviewed before publication. Under
§12.1.1 the view is a producer of IPE, and the missing control is a review of that IPE precise enough to detect a
2.2% error. Because no reconciliation existed, this is a control that was never designed rather than one that failed
to operate.

**Is it within the scope of ICFR at all?** The instinct is no: ARR is not a GAAP measure, it appears in Item 7, and
ICFR is defined by reference to the reliability of financial reporting under GAAP. That instinct is wrong here for
two independent reasons, and separating them matters because they produce different responses. The first is the
ASC 718 link. Compensation cost for a performance condition is accrued when achievement is probable, so the
probability assessment is an estimate in the audited statements and its input is the ARR figure. The draft $175,860
cleared the $170,000 threshold with $5,860 of headroom; the corrected $172,000 clears it with **$2,000**, or 1.4
times overall materiality. If a further $2,000 of error existed in a population where $3,860 was found, the
condition is not met, probability is nil, and $7,593 of recognized expense reverses — **5.2 times overall
materiality** ($7,593 ÷ $1,450). A metric with that leverage over an estimate is inside ICFR whatever its GAAP
status, because ICFR extends to controls over the information used to prepare the statements. The second is
disclosure. ARR in Item 7 is other information under AS 2710, which Brightline must read and consider for material
inconsistency; separately, Exchange Act Rule 13a-15 requires evaluation of disclosure controls and procedures, which
are broader than ICFR, and the SEC staff's interpretive guidance on key performance indicators expects a registrant
presenting a metric to disclose how it is calculated and to control it. Both routes were documented; the team did
not have to choose.

**What is the audit response?** Five procedures. Test the ARR computation as IPE against the eight attributes in
Exhibit 12-16, which produced the four defects. Recompute the metric from the source system rather than the replica.
Reconcile the datamart to the general ledger for the tables the audit relies on, because W-11 means management had
done so only for December. Expand the procedures over the PSU probability estimate to include a sensitivity analysis
on the corrected figure. And evaluate W-11 as a deficiency, aggregated with W-8 and W-12 under Chapter 14's
framework.

### Resolution and Conclusion

Management accepted all four corrections and revised the view: charge-type filters added, `CURRENT_DATE()` replaced
with an `as_of_date` parameter, `_fivetran_deleted = FALSE` added to all three joins, and the Kestrel legacy feed
retired. The final Form 10-K discloses ARR of **$172.0 million** against prior-year $137.4 million, growth of 25.2%,
and adds a description of how ARR is calculated and what it excludes. The view was placed under source control and a
monthly ARR-to-general-ledger reconciliation was designed and performed for December 2025.

On the estimate, the team accepted management's 85% as within the range of reasonable outcomes but narrowed the
basis: with $2,000 of headroom against a metric that was materially wrong three weeks earlier, the assessment
depends on the reliability of that metric. Recomputing ARR excluding the $2,900 of contracts under churn notices
received in January 2026 produces $169,100 — below the threshold — and the team documented that a probability
between 60% and 85% would be defensible. Management's 85% sits at the optimistic end; the difference in cumulative
expense between 85% and 60% is $8,933 × 0.25 = $2,233, which exceeds overall materiality. It was not proposed as a
misstatement because 85% remains supportable, but it was communicated to the audit committee as an indicator of
estimate bias.

On ICFR, the team concluded that the absence of any control over the production of ARR and NRR, combined with the
metric's role in the PSU estimate, is at least a significant deficiency, and that W-11 aggregates with W-8 and W-12
in the group of deficiencies evaluated in Chapter 14 and reported in Chapter 20. Remediation was not tested for
operating effectiveness, because the reconciliation control was designed in December 2025 and had operated once.

### Workpaper Extract

```text
================================================================================
BRIGHTLINE LLP                                              WP REF:  4300-16
AtlasFlow, Inc.                                             PERIOD:  FY2025
Audit of the financial statements and of ICFR                YEAR END: 12/31/2025
--------------------------------------------------------------------------------
SUBJECT:  Completeness and accuracy of the annual recurring revenue (ARR)
          metric produced by the Snowflake RevOps datamart; effect on the
          ASC 718 performance-condition probability assessment; evaluation
          of weakness W-11

PREPARED BY:  T. Iyer (TRI)             DATE PREPARED:  01/16/2026
              B. Osei (BAO)                             01/19/2026
REVIEWED BY:  F. Nazari (FMN)           DATE REVIEWED:  01/23/2026
              G. Lindqvist (GRL)                        01/28/2026
PARTNER:      D. Whitcombe (DGW)                        02/06/2026
EQR:          L. Herrera (LXH)                          02/17/2026
--------------------------------------------------------------------------------
PURPOSE
To test the completeness and accuracy of the ARR figure presented in Item 7
as information produced by the entity; to determine whether the process
producing it is within the scope of ICFR; to evaluate the effect of the
metric's reliability on the ASC 718-10-25 probability assessment for the
ARR-based PSU tranche; and to evaluate the severity of weakness W-11.

SOURCE OF INFORMATION
(1) View definition REVOPS.MART.V_ARR_MONTHLY, exported by the auditor from
    Snowflake INFORMATION_SCHEMA on 01/14/2026.                            (a)
(2) Zuora Billing subscription and rate-plan-charge extract at 12/31/2025,
    obtained in a screen-share session with J. Pike; 41,884 charges on
    14,392 contracts; control total of monthly recurring charge $14,333.   (a)
(3) Draft Form 10-K dated 01/12/2026, Item 7, page 44.
(4) Carta PSU grant extract; Q3 and Q4 2025 stock-compensation memoranda.
(5) Snowflake role grants for the REVOPS database at 12/31/2025 (4 users).
(6) Management's ARR-to-GL reconciliation for December 2025, dated 01/09/2026.

PROCEDURES PERFORMED
1. Read the view definition; identified four defects: no charge-type filter;
   CURRENT_DATE() in place of an as-of parameter; no _fivetran_deleted
   filter; no exclusion of migrated Kestrel accounts.                      (b)
2. Recomputed ARR at 12/31/2025 from the Zuora source population:
       Draft ARR per V_ARR_MONTHLY                        175,860
       Terminations booked 01/02/2026, still Active         (1,840)   (c)
       Usage overage annualized                            (1,260)   (c)
       Kestrel accounts counted twice                        (740)   (c)
       One-time PS fees annualized (19 contracts)            (410)   (c)
       Escalator measurement basis correction                  390   (c)
       Recomputed ARR                                      172,000
3. Reconciled replica row counts and control totals to the Zuora source for
   the three tables used: SUBSCRIPTION 14,392 / 14,392;
   SUBSCRIPTION_RATE_PLAN_CHARGE 41,902 before and 41,884 after excluding
   18 soft-deleted rows; ACCOUNT 3,140 / 3,140.                           (b)
4. Traced ARR into the ASC 718 estimate. Threshold $170,000; recomputed
   headroom $2,000 (1.4x overall materiality of $1,450). Fully-probable
   cumulative measure $8,933 (= $1,340 / 0.15); recognized at 85% = $7,593;
   full-reversal exposure 5.2x overall materiality.                        (b)
5. Recomputed ARR excluding $2,900 of contracts under January 2026 churn
   notice: $169,100, below the threshold. Documented a defensible
   probability range of 60% to 85%.                                       (b)
6. Read Item 7 for consistency with the audited statements (AS 2710) and
   agreed the revised metric and the added calculation description.        (a)
7. Inspected Snowflake role grants; 4 users can alter the view, which was
   not under source control until 02/02/2026.                             (a)

TICK-MARK LEGEND
(a) Obtained or inspected by the auditor directly from the system; export
    performed in the auditor's presence.
(b) Recomputed or independently derived by the auditor.
(c) Traced to the underlying source population or executed contract.

RESULTS
The draft ARR figure was overstated by $3,860, or 2.2%. All four errors were
corrected and the final disclosed figure of $172.0 million agrees to our
recomputation; no financial statement misstatement arose from the metric.
Management's 85% probability assessment remains within a defensible range but
sits at its optimistic end and is reported to the audit committee as an
indicator of possible estimate bias. No control existed over the production
of ARR and NRR for the first three quarters of FY2025.

CONCLUSION
The ARR metric was not reliable as originally produced and required auditor-
identified correction. The process producing it is within the scope of ICFR
because the metric is an input to an ASC 718 estimate recorded in the
financial statements, and is within disclosure controls and procedures under
Exchange Act Rule 13a-15 in any event. W-11 is evaluated as at least a
significant deficiency and is aggregated with W-8 and W-12 at WP 7100-04.
Reliance on any Snowflake-sourced population elsewhere in the file is
conditioned on the reconciliation at procedure 3 above.
================================================================================
```

### Lessons

An operating metric is not outside the audit because it is outside GAAP; trace it forward, and if it touches an
estimate, an incentive, a covenant, or an impairment trigger, it is inside. A query is an application: if four
people can change it and it is not in source control, there is no change management over a financially significant
computation. Reconciling a replica to its source is the auditor's job when the entity has not done it, and the
reconciliation is row count and control total, not a spot check. And note what saved the disclosure: not a control,
but an auditor who recomputed a number nobody had recomputed. That is a description of a control environment, not a
compliment to the audit team.

## Common Mistakes

### Mistake 12.1 — Testing the signature and calling it a test of an IT-dependent manual control

**What it looks like.** The workpaper for the Controller's review of the I-3 journal contains the FloQast sign-off
date, the initials, and a conclusion, and nothing about the RevPro Revenue Contract Summary.
**Why it happens.** The control description reads "reviewed and approved by the Controller," and the sign-off is the
easiest evidence in the file to obtain.
**What goes wrong.** The report excluded 41 on-hold performance obligations and $196 of December revenue. A perfect
review of an incomplete report detects nothing.
**How to avoid it.** Apply Question 2. If the reviewer looks at a screen or a file, that is IPE, and its
completeness and accuracy are attributes of your test rather than an optional extra procedure.

### Mistake 12.2 — Accepting a point-in-time screenshot as configuration evidence

**What it looks like.** An undated image of the CPQ approval matrix captioned "per client."
**Why it happens.** Screenshots are fast and the reviewer can see the thresholds, which feels like evidence.
**What goes wrong.** A screenshot documents one unknown instant. AP-CPQ-01 changed on November 7 and December 18,
2025, so a December 8 capture covers 41 days of 365 and an undated one covers nothing.
**How to avoid it.** Obtain a configuration export with a system-generated timestamp and user, plus the
application's configuration audit trail for the full period, and reconcile every change to a ticket.

### Mistake 12.3 — Proving a report is complete by tying it to the general ledger

**What it looks like.** "Agreed the revenue schedule total of $12,760 to the general ledger; report is complete and
accurate."
**Why it happens.** An agreeing tie-out feels conclusive and the ledger carries the authority of the books.
**What goes wrong.** The journal was generated from the same query as the report, and both exclude the same 41
performance obligations. Tying two outputs of one query proves only that the interface did not corrupt anything.
**How to avoid it.** Test completeness against an independent population — the Zuora Billing subscription and
invoice data or the executed contract file — and read the report's filters explicitly.

### Mistake 12.4 — Treating a test of one as self-justifying

**What it looks like.** "The control is fully automated; accordingly we tested one instance and concluded the
control operated effectively throughout the period."
**Why it happens.** Automated logic genuinely does not vary, and firm methodology permits a test of one, so the
sentence sounds like methodology.
**What goes wrong.** The inference rests on the configuration being unchanged. Two of the 27 RevPro rules were
changed in FY2025 through an unattributable shared account, so a December test supports a December conclusion.
**How to avoid it.** State the four conditions in §12.9 and conclude on each. Where condition 4 fails, test one item
per configuration state; where a state boundary is undocumented, conclude the control cannot be relied on.

### Mistake 12.5 — Reconciling an interface on amount only

**What it looks like.** "Agreed the interface total of $18,712 to the Zuora Revenue load; no differences noted."
**Why it happens.** Amount reconciliations are what accountants do, and the amount is what reaches the statements.
**What goes wrong.** Records never selected for transfer, and records suppressed as duplicates, are missing from
both sides of an amount comparison built from the loaded population. Only a record-count reconciliation against an
independently derived source count finds them — as it found the 65 suppressed records and 12 deleted queue records.
**How to avoid it.** Reconcile count and amount, define the source population from the source system, and account
for every rejected, held, and suppressed record by name.

### Mistake 12.6 — Accepting a configurable threshold without measuring it against materiality

**What it looks like.** "NetSuite requires dual approval above $250,000. Control designed effectively."
**Why it happens.** The control exists, the number is large, and comparing it to materiality is not a step in most
control matrices.
**What goes wrong.** Performance materiality is $940. Six unreviewed entries at the cap aggregate to $1,500, above
overall materiality of $1,450, and 3,847 of 4,912 manual entries fall below the threshold.
**How to avoid it.** For every configurable threshold, compute the unreviewed population and its value, express one
threshold-sized item as a percentage of performance materiality, and state the range you would accept.

### Mistake 12.7 — Sampling from an error queue without establishing that the queue is complete

**What it looks like.** Twenty-five items selected from the I-1 queue, each traced to evidence of clearing,
conclusion of effective operation.
**Why it happens.** The queue is tidy and has a record count, which makes it look like a population.
**What goes wrong.** Twelve error records were hard-deleted by a shared service account in July 2025. A sample from
an incomplete population cannot support a completeness conclusion, and expanding it adds cost without coverage.
**How to avoid it.** Derive the population independently — the count of failed API responses in the target system's
audit log — reconcile it to the queue, and investigate the difference before selecting anything.

### Mistake 12.8 — Listing a script, a bot, or a datamart as a key control

**What it looks like.** A matrix row reading "the Stripe-to-NetSuite Lambda job posts the daily journal entry —
automated — key control."
**Why it happens.** Automation is conflated with control, and the job is genuinely important.
**What goes wrong.** A posting mechanism creates the exposure a control must address, so the tick mark lands where
the risk is and the actual control — the daily cash-to-revenue reconciliation — goes untested. Two unapproved
modifications produced $148 of classification error and $21 of unreversed duplicate revenue.
**How to avoid it.** Ask what misstatement the item prevents or detects. If the answer is none, it is a process
step, tested as change management and as a source of misstatement.

### Mistake 12.9 — Testing an edit check that constrains the wrong field

**What it looks like.** Eight validation rules tested, all operating as configured, input controls concluded
effective.
**Why it happens.** The test is satisfying to perform, and the rule inventory comes from the client.
**What goes wrong.** V-01 constrains the contractual start date, but the policy recognizes revenue from the later of
start and provisioning, and no system carries the provisioning date. The $410 of misstatement C-1 arose in the gap
the edit checks do not cover.
**How to avoid it.** Start from the accounting policy and the "what could go wrong," identify the field the policy
depends on, then ask whether any rule constrains it. A working rule on an irrelevant field is not a mitigation.

### Mistake 12.10 — Treating an MD&A metric as outside the audit because it is not GAAP

**What it looks like.** "ARR is a non-GAAP operating metric outside the scope of ICFR; no procedures performed."
**Why it happens.** The general proposition is correct and it removes work from the plan.
**What goes wrong.** ARR is the input to the performance condition on the ARR-based PSUs. The corrected figure
clears the $170,000 threshold by $2,000, and failure of the condition reverses $7,593 of expense, 5.2 times overall
materiality. The metric was also overstated by $3,860 in the draft filing.
**How to avoid it.** Trace every prominent operating metric forward. If it feeds an estimate, a compensation
condition, a covenant, or an impairment trigger, it is inside ICFR through that link, and it is within disclosure
controls and procedures and AS 2710 regardless.

## Practice Exercises

### Exercise 12-1

**[Foundational]** Classify each of the following using the decision rule in §12.1.1 and state in one clause what
the test must cover: (i) Avalara determines the sales tax rate on each Zuora invoice from the ship-to state; (ii) the
Treasury Manager reviews the daily positive-pay exception file from First Meridian and approves or rejects each item;
(iii) Coupa blocks an invoice whose supplier and invoice number duplicate an existing record; (iv) the
stock-compensation workbook's `SUMIFS` formulas total monthly expense by income statement line from the Carta
export; (v) FloQast will not permit the close checklist to be marked complete until every reconciliation has a
sign-off.

### Exercise 12-2

**[Foundational]** Using the configured criteria in Exhibit 12-6, determine the approval steps CPQ will require for
each quote and whether that agrees to the January 2025 policy. Whole dollars. (i) List $300,000, net $270,000.
(ii) List $500,000, net $400,000. (iii) List $412,000, net $247,200. (iv) List $250,000, net $140,000. (v) List
$1,000,000 for 24 months quoted as 21 paid months at $41,666.67 per month plus 3 free months.

### Exercise 12-3

**[Intermediate]** For November 2025, Zuora Billing created 109,742 transactions eligible for transfer, amounting to
$17,410 thousand. Batches run November 2 through December 1 loaded 108,918 of those records and $17,166 thousand. The
error table held 741 records and $208 thousand at November 30, and the connector suppressed 83 records and $36
thousand as duplicate keys. Prepare the reconciliation in the format of Exhibit 12-21, compute the unexplained
difference on both columns, and state what you would do next.

### Exercise 12-4

**[Intermediate]** You are testing the Zuora Billing aged trial balance at December 31, 2025, which supports the
$38,600 gross receivable population in Chapter 7. For each of the eight attributes in Exhibit 12-16, state the
specific evidence you would obtain. Then identify which single attribute, if unaddressed, would most likely cause
the aging to be wrong, and why.

### Exercise 12-5

**[Advanced]** Find the errors in this workpaper conclusion and list them. "We inspected the NetSuite journal entry
approval configuration and noted that entries of $250,000 or more require a second approver. We selected 25 journal
entries from the FY2025 population of 4,912 manual entries and agreed each to supporting documentation and to
evidence of approval. No exceptions were noted. We also agreed the RevPro revenue schedule total for December of
$12,760 to the general ledger. Based on the above, controls over journal entries and the revenue subledger operated
effectively for the year ended December 31, 2025."

### Exercise 12-6

**[Intermediate]** Using Exhibit 12-10, compute (i) the percentage of manual entries by count and by absolute value
falling below the $250,000 threshold; (ii) the number of below-threshold entries at the average value of $5.77
thousand that would have to be misstated in the same direction to exceed performance materiality of $940; and
(iii) the number required if each were at the $250 thousand cap. State the threshold you would consider defensible
and the evidence that would change your view.

### Exercise 12-7

**[Advanced]** The Coupa configuration audit log shows: March 3, unit price tolerance raised from 2% to 5% by
`apmanager`, ticket CHG-2025-0221; July 19, invoice total tolerance raised from $250 to $1,000 by `coupa_admin`, a
shared account, no ticket; October 2, non-PO categories increased from 9 to 14 by `apmanager`, ticket CHG-2025-0904.
You tested the match on December 4, 2025 with a single transaction. State how many configuration states existed,
what your December test supports, and what further evidence you need to conclude on the full year.

### Exercise 12-8

**[Intermediate]** Draft the control description for the CPQ discount approval control in 90 to 130 words, suitable
for a control matrix. It must identify the risk addressed, the point in the process at which the control operates,
the mechanism, the configured criterion, the approvers, the frequency, the evidence the control leaves behind, and
the population over which it operates.

### Exercise 12-9

**[Advanced]** Draft the deficiency finding for W-11 in 150 to 200 words in the form used for audit committee
communication: condition, criterion, cause, effect including quantification, and recommendation. Do not grade the
severity, but state the facts a severity evaluation would need.

### Exercise 12-10

**[Intermediate]** AtlasFlow processed 18,410 supplier invoices in FY2025, of which 14,806 were PO-backed. Within
those, 2,318 matched with a variance above the $250 policy tolerance but within the $1,000 configured tolerance,
aggregating $86 thousand. Compute (i) the average variance per invoice in whole dollars; (ii) the aggregate as a
percentage of overall materiality of $1,450; (iii) the theoretical maximum exposure if all 2,318 had been at the
configured cap, and that amount as a percentage of overall materiality. Then state whether the tolerance is a design
deficiency and why the answer does not depend on part (i).

### Exercise 12-11

**[Advanced]** Chapter 6, §6.11 recomputes the $214,000 RPO disclosure using management's Snowflake query
`RPO_FY25_V3.sql` and an independent recomputation from the Zuora subscription population. Evaluate that evidence
against the eight IPE attributes in Exhibit 12-16, using the four defects found in `V_ARR_MONTHLY` as your checklist
of likely problems. Identify the two attributes most at risk for a query run against the Snowflake replica, state
the procedure that addresses each, and state whether Chapter 6's independent recomputation makes those procedures
unnecessary.

### Exercise 12-12

**[Advanced]** Quantify and evaluate the two unapproved modifications to `stripe-netsuite-daily-je`. Self-serve
billings for March 6 through December 31, 2025 were $5,002 thousand at a blended processing fee rate of 2.96%. Three
duplicate journal entries totaling $57 thousand were produced, two reversed within the month and one of $21 thousand
not reversed. Compute the misstatement in revenue and in cost of subscription revenue, the effect on the net loss,
and the detection rate of the daily reconciliation. Then state whether each modification is a control deviation, a
design deficiency, or a change-management failure, and what evidence would move your conclusion.

## Solutions to Practice Exercises

### Solution 12-1

(i) Fully automated and configurable: no person is involved, and the rate tables and nexus settings are
configurable. Test rate determination for constructed ship-to states and the configuration change history. (ii)
IT-dependent manual and an interface control: the Treasury Manager is required, the exception file is
system-generated, and it crosses from the bank into NetSuite. Test evidence of review plus completeness of the
exception file against the bank's own record of items presented. (iii) Fully automated and configurable. Test by
attempting a duplicate and by querying the population for duplicate supplier and invoice-number pairs. (iv)
End-user computing, not an application control: automation without change management. Test formula integrity, the
completeness of the Carta export, and the review of the output. (v) Fully automated and configurable, but note what
it enforces — the presence of a sign-off, not the quality of the reconciliation. Test that the block operates and
state explicitly that it provides no evidence about the reconciliations themselves.

### Solution 12-2

(i) $30,000 ÷ $300,000 = 10.00%; configured `Discount__c <= 10`, no approval; policy T0. Agrees. (ii) $100,000 ÷
$500,000 = 20.00%; configured step 1, satisfiable by any `Sales_Leadership` member; policy T1 requires the Regional
Sales Director. Partially agrees — right tier, wrong approver population. (iii) $164,800 ÷ $412,000 = 40.00%;
configured step 3, CRO only; policy T3 at exactly 40.00% also requires only the CRO, so this agrees, and the
disagreement begins at 40.01%. (iv) $110,000 ÷ $250,000 = 44.00%; configured step 3, CRO only; policy T4 requires
CRO and CFO. Does not agree — the December 18 change in operation. (v) $41,666.67 × 21 = $875,000.07 against a
24-month list of $1,000,000, an effective discount of 12.50%; `Discount__c` computes as 0.00% because the free
months are zero-price lines, so no approval is required and policy T1 is not applied. Does not agree; a design
defect rather than an operating deviation.

### Solution 12-3

| Line | Records | Amount |
| --- | --- | --- |
| Source: created 11/01–11/30/2025, transfer eligible | 109,742 | 17,410 |
| Loaded, batches 11/02–12/01, source-created in November | (108,918) | (17,166) |
| Error table at 11/30/2025 | (741) | (208) |
| Suppressed as duplicate keys | (83) | (36) |
| **Unexplained difference** | **—** | **—** |

Records: 108,918 + 741 + 83 = 109,742. Amount: 17,166 + 208 + 36 = 17,410. Both reconcile with no unexplained
difference. Next step: do not stop at "reconciles." The November error table of 741 records is 80% larger than
December's 412, so age it and determine what caused the spike, and test whether any of the 83 suppressed records are
genuine distinct transactions, as 7 of December's 65 were.

### Solution 12-4

By attribute: (1) source — the definition showing the report reads the Zuora invoice and payment tables rather than
a saved extract; (2) query — the aging-bucket logic, plus recomputation of bucket assignment for 25 invoices from
invoice date and terms; (3) parameters — the as-of date printed on the report, confirmed as 12/31/2025 rather than
the run date; (4) filters — the invoice and account status filters, with the excluded population quantified; (5)
completeness at source — agreement of the gross total to $38,600 and of the record count to the invoice register,
plus reconciliation of the $1,700 self-serve balance to account 1205; (6) reproducibility — re-running with the same
as-of date later and obtaining the same total; (7) integrity in transit — generating the report yourself and
recording count and control total at receipt; (8) change control — the definition's change log for the period. The
attribute most likely to make the aging wrong is (3): an aged trial balance run with a system-date parameter after
year end ages every open invoice by the elapsed days, shifting balances into older buckets and changing the CECL
loss-rate application in Chapter 7. A defensible alternative is (4), since a status filter can drop disputed
invoices such as Meridian's $1,240 entirely; the discriminating test is whether the gross total still agrees to
$38,600.

### Solution 12-5

Six errors. Inspection establishes the setting and nothing about operation, and there is no re-performance or
attempted posting. The $250,000 threshold is never evaluated against performance materiality of $940, so the design
conclusion is unsupported. The sample of 25 was drawn from all 4,912 manual entries, but 3,847 fall below the
threshold and are outside the control's population, so "no exceptions" is meaningless for them. The procedure
confounds a test of controls with a test of details by agreeing entries to support without stating the attribute or
the deviation condition. Agreeing the RevPro December total to the general ledger is circular, because the ledger
amount came from the same query, and it covers one month rather than the year. And the conclusion covers "the
revenue subledger" for the full year on one month's tie-out with no test of the 27 configuration rules or the
February 2025 change. A seventh point is defensible: two different controls are merged into one sentence, so a
reader cannot tell which evidence supports which conclusion.

### Solution 12-6

(i) By count 3,847 ÷ 4,912 = 78.3%; by absolute value $22,200 ÷ $140,900 = 15.8%. (ii) $940 ÷ $5.77 = 162.9, so 163
average-sized entries. (iii) $940 ÷ $250 = 3.76, so 4 entries at the cap exceed performance materiality and 6 exceed
overall materiality ($1,450 ÷ $250 = 5.8). A defensible threshold is $50 to $100: at $100, ten entries at the cap are
needed to reach performance materiality, a plausible aggregation but a far narrower exposure. Evidence that would
change the view: the actual amount distribution of the 3,847 entries, particularly how many sit between $100 and
$250; the existence of a compensating detective control over the below-threshold population; and the results of the
Chapter 16 journal entry testing, which would show whether that population actually contains misstatement.

### Solution 12-7

Four states: January 1 to March 2, March 3 to July 18, July 19 to October 1, and October 2 to December 31. Your
December 4 test supports a conclusion about the fourth state only — 91 days of 365 — and only about a configuration
looser than policy on both tolerances. The July 19 change is fatal: made through a shared account, so not
attributable, and without a ticket, so not approved. Conditions 3 and 4 in §12.9 are not met, and additional
December transaction testing does not repair that. To conclude on the full year you need, at minimum, evidence of the
tolerance values in force in each of the four states, one re-performance test per state, evidence that the shared
`coupa_admin` account's FY2025 activity can be attributed, and quantification of the invoices that passed within the
wider tolerance after July 19. A defensible alternative conclusion is that the control cannot be relied on for
FY2025 and the expenditure cycle is tested substantively; that is the stronger answer if the shared-account activity
cannot be attributed.

### Solution 12-8

Model language, 118 words:

"To address the risk that a subscription is sold at a discount not authorized at the appropriate level of
management, thereby misstating the transaction price and the resulting revenue, Salesforce CPQ prevents a quote from
being converted to an activated order form until every approval step triggered by approval process AP-CPQ-01 has
been completed. The process computes `Discount__c` as one minus net price divided by list price on the quote lines
and routes the quote to the Regional Sales Director above 10.00%, additionally to the VP Sales Operations above
20.00%, to the Chief Revenue Officer above 30.00%, and additionally to the Chief Financial Officer above 45.00%. The
control operates on every order form activated (3,412 in FY2025) and leaves an approval-history record in
`ProcessInstanceStep` for each completed step."

A control description states the configuration as it is, not as policy says it should be. The disagreement between
the 45.00% here and the 40.00% in the policy is the finding, and hiding it in the description destroys it.

### Solution 12-9

Model language, 176 words:

"**Condition.** ARR and net revenue retention presented in Item 7 of the Form 10-K are computed by a Snowflake view
in the RevOps datamart that was not reconciled to the general ledger for the first three quarters of FY2025, is not
maintained under source control, and can be altered by four users. **Criterion.** Information used in external
reporting and as an input to accounting estimates should be produced by a process subject to controls over
completeness, accuracy, and change, consistent with COSO Principles 10 and 11 and with Exchange Act Rule 13a-15.
**Cause.** The computation was moved from Revenue Operations into the datamart in November 2025 without extending
the financial reporting control framework to it. **Effect.** The ARR figure in the January 12, 2026 draft was
overstated by $3,860 thousand, or 2.2%, from four independent defects. The metric is the input to the performance
condition on the ARR-based PSU tranche; the corrected figure of $172,000 thousand exceeds the $170,000 thousand
threshold by $2,000 thousand, and failure of the condition would reverse $7,593 thousand of recognized compensation
cost. **Recommendation.** Place the view under source control, restrict alter rights, add a monthly reconciliation of
the metric to the general ledger and to the Zuora source population, and require documented review before
publication."

### Solution 12-10

(i) $86,000 ÷ 2,318 = $37.10 per invoice. (ii) $86 ÷ $1,450 = 5.9%. (iii) 2,318 × $1,000 = $2,318 thousand, which is
159.9% of overall materiality. Yes, the tolerance is a design deficiency, and the answer does not depend on part (i)
because design effectiveness is evaluated against what the control permits rather than what happened to occur. A
control allowing $2,318 thousand of unreviewed variance — 160% of overall materiality — is not designed to prevent or
detect a material misstatement, and the fact that this year's variances averaged $37 is a statement about this
year's suppliers. The converse also holds: had the actual aggregate been $1,600 thousand, that would be a
misstatement question in addition to a design question.

### Solution 12-11

The two attributes most at risk are (5) completeness at source and (3) parameters. Completeness is at risk because a
query against the replica inherits the replica's state: rows soft-deleted upstream persist unless
`_fivetran_deleted` is filtered, and rows created since the last sync are absent. The procedure is a row-count and
control-total reconciliation of every table the query touches, replica to Zuora source, at the extract date — for
`SUBSCRIPTION` 14,392 to 14,392, and for `SUBSCRIPTION_RATE_PLAN_CHARGE` 41,884 after excluding 18 soft-deleted
rows. Parameters are at risk because an RPO computation must be as of December 31, 2025, and any use of
`CURRENT_DATE()` makes the figure move with the run date — precisely the defect in `V_ARR_MONTHLY`. The procedure is
to read the query for date functions and re-run it on two different dates with the same parameter, expecting
identical output. Chapter 6's independent recomputation does not make these procedures unnecessary, which is the
point: that recomputation was itself performed on a Snowflake-sourced population, so it inherits the same
completeness exposure. An independent recomputation from the same unreliable data corroborates arithmetic, not
completeness. It would suffice only if performed on a population obtained directly from Zuora and reconciled to the
invoice register.

### Solution 12-12

Commit `a7f3c21`: $5,002 × 2.96% = $148.06, so $148 thousand. Revenue is understated by $148 and cost of
subscription revenue (account 5100) by $148; the effect on the net loss is nil and gross margin is overstated.
Commit `e91b40d`: duplicates of $57 thousand, of which $36 thousand was reversed within the month and $21 thousand
was not, so revenue and the Stripe receivable in account 1205 are overstated by $21 thousand at December 31, 2025;
the reconciliation's detection rate is 2 ÷ 3 = 66.7%. Classification: `a7f3c21` is a change-management failure that
produced a misstatement but not a control deviation, because no control was designed to detect a change in the
presentation logic — the daily reconciliation ties net settlement to revenue and nets to the same amount either way,
so it cannot detect the netting. That is a design gap. `e91b40d` is both a change-management failure and a control
deviation, because the reconciliation was designed to detect duplicate postings and missed one of three. Evidence
that would move the conclusion: for `a7f3c21`, a documented control comparing the Stripe gross charge total to
recorded revenue would convert it into a deviation; for `e91b40d`, the early-November reconciliation papers would
show whether the item was identified and left open, a different and less severe finding than not identifying it.

## Review Questions

**RQ 12-1.** State the four questions of the classification decision rule, in order.

**RQ 12-2.** Why is an IT-dependent manual control the category most often misclassified, and what procedure is
omitted when it is?

**RQ 12-3.** Why does a configurable control require two attributes to be tested rather than one?

**RQ 12-4.** Give an AtlasFlow example of a control well designed as to one attribute and defective as to another,
and state which technique finds each.

**RQ 12-5.** Name the eight types of input validation check and give the AtlasFlow example of one configured as a
warning rather than a block.

**RQ 12-6.** Why does testing 40 revenue schedules provide no evidence about the 27 Zuora Revenue configuration
rules?

**RQ 12-7.** What must you establish about a non-production instance before re-performing a configured calculation
in it?

**RQ 12-8.** State the four conditions that must hold before a test of one supports a full-period conclusion.

**RQ 12-9.** What is a test of one per configuration state, and what determines the number of states?

**RQ 12-10.** State the conditions AS 2201 Appendix B attaches to benchmarking and two reasons it is unavailable to
Brightline for FY2025.

**RQ 12-11.** List the eight attributes of a system-generated report that must be addressed before it is used.

**RQ 12-12.** Why is tying a system-generated report to the general ledger not a test of its completeness?

**RQ 12-13.** Why must an interface reconciliation address record count, and what two failures does the count detect
that the amount cannot?

**RQ 12-14.** What makes an error queue a population before it is a control, and what independent source establishes
its completeness for I-1?

**RQ 12-15.** On what four axes is spreadsheet risk assessed, and what score profile requires the full control set?

**RQ 12-16.** Why is a script that posts journal entries not a control, and what is the control in the I-4 flow?

**RQ 12-17.** Define cloud configuration drift, name its three sources, and state the response.

**RQ 12-18.** When does a non-GAAP operating metric fall within the scope of internal control over financial
reporting?

## Answers to Review Questions

**RQ 12-1.** Remove every person and ask whether the misstatement is still prevented or detected; if yes, the
control is fully automated. If a human step is irreducible, ask whether it consumes system-generated information; if
yes, it is IT-dependent manual and that information is IPE. Ask whether the automation's behavior is driven by a
value a business user can change without a code deployment; if yes, it is configurable. Ask whether it operates on
data crossing an application boundary; if yes, it is an interface control. The last two are overlays on the first
two.

**RQ 12-2.** Because the description reads like a manual control — someone reviews and approves — and the sign-off is
the most accessible evidence in the file. The omitted procedure is the test of completeness and accuracy of the
system-generated information used. Testing the Controller's sign-off on the I-3 journal without testing the RevPro
report missed 41 on-hold performance obligations carrying $196 of December revenue.

**RQ 12-3.** Because the mechanism can operate perfectly while the value in it is wrong. The $250,000 journal entry
threshold is the example: the mechanism blocks single-approver posting above the value, and the value is set so high
that 3,847 of 4,912 manual entries escape review.

**RQ 12-4.** The CPQ approval matrix: well designed as to the discount bands, defective in that `Discount__c` does
not capture discounts delivered through zero-price free months and that the T3 upper bound was moved to 45%. The
zero-price defect is found by re-performance with a constructed quote, because the control operated as designed on
every affected order form; the 45% boundary is found by inspecting the configuration against the policy, and the date
it changed only by the configuration audit trail.

**RQ 12-5.** Validity, format, range or limit, dependency, duplicate, sequence, batch or control total, and
reasonableness. The Zuora duplicate-account rule (V-05) is a soft warning that permits the save; the consequence is
7 duplicate accounts, 2 carrying $118 of active ARR.

**RQ 12-6.** Because the schedules are the output of the rules. If a rule is systematically wrong — monthly spreading
where policy is daily, or prospective treatment where cumulative catch-up is required — every schedule is wrong the
same way and 40 small differences look like rounding. Output testing can corroborate a rule-level conclusion but
cannot substitute for one.

**RQ 12-7.** That it is identical to production for the configuration you are about to exercise. The team compared
all 27 RevPro rules across 41 exported attributes each and confirmed zero field-level differences, and separately
compared AP-CPQ-01 across 41 fields. Without that, a passing sandbox test says nothing about production and a failing
one cannot be attributed.

**RQ 12-8.** The control is wholly automated with no human judgment in its operation; program change controls were
effective for the entire period; logical access to the configuration was appropriately restricted for the entire
period; and you hold independent evidence of configuration stability across the period, in the form of a change log
in which every change is identified, attributable, and approved. The fourth is a substantive procedure, not a
restatement of the second and third.

**RQ 12-9.** One test of one transaction for each interval in which the configuration was constant. The number of
states is one more than the number of configuration changes shown by the application's own audit trail. AP-CPQ-01
changed twice, on November 7 and December 18, 2025, producing three states of 310, 41, and 14 days.

**RQ 12-10.** The control must be automated; general IT controls over program change, access to programs, and
computer operations must be effective; the auditor must verify the program or configuration has not changed since
testing; and the auditor must consider the risk associated with the control and whether the data or circumstances
have changed. It does not apply where the control is subject to human intervention. It is unavailable because
FY2025 is the first integrated audit, so no baseline exists, and because the general IT controls it depends on are
not effective (W-1 through W-6).

**RQ 12-11.** Source, query or logic, parameters, filters and exclusions, completeness at source, reproducibility,
integrity in transit, and change control over the definition. Each has its own evidence; addressing seven and
skipping the eighth is how the on-hold filter survived.

**RQ 12-12.** Because both sides can be produced by the same query and share the same omission. The I-3 journal ties
exactly to the RevPro report and both exclude the same 41 performance obligations. A completeness test requires an
independent population — the Zuora Billing subscription and invoice data, or the executed contract file.

**RQ 12-13.** Because an amount reconciliation built from the loaded population cannot see records never selected for
transfer or suppressed before loading; both are missing from both sides. Record counts detect exactly those two
failures. At AtlasFlow the count comparison surfaced 65 suppressed records, 7 of them genuine distinct credit memo
items, and 12 queue records deleted by a shared service account.

**RQ 12-14.** Because a sample from the queue supports a conclusion only about the records in it, and records can be
deleted. For I-1 the independent source is the Zuora inbound audit log's record of failed API responses: 1,258
against 1,246 in the Salesforce `Integration_Error__c` object, a difference of 12 hard-deleted on July 18, 2025.

**RQ 12-15.** Complexity, use, judgment content, and exposure to change. A workbook scoring high on all four — as
CONSOL_FY25_v14.xlsx does, with 18,942 formula cells, 1,204 external links, 27 top-side entries, 14 saved versions,
and 4 users with edit rights — requires restricted write access, locked formula cells, a change log, independent
formula-integrity review after structural changes, input reconciliation to source, and output reconciliation to an
independent expectation.

**RQ 12-16.** Because it prevents and detects nothing; it creates the postings a control must address. In I-4 the
control is the daily Stripe cash-to-revenue reconciliation performed by the Staff Accountant, an IT-dependent manual
control. The script is tested as a change-management population and as a source of misstatement, which is how the
$148 netting error and the $21 unreversed duplicate were identified.

**RQ 12-17.** The tendency of vendor-hosted application settings to change between the date the auditor tests and
the date the conclusion covers, without a code deployment and often without a ticket. Its sources are administrator
changes through the user interface, vendor releases that alter defaults or add settings, and infrastructure-as-code
applies that overwrite manual changes or are overwritten by them. The response is to obtain the application's
configuration audit trail for the full period rather than a point-in-time export, reconcile every change to a ticket,
and obtain the trail before the vendor's retention window closes.

**RQ 12-18.** When it is an input to something recognized or disclosed in the financial statements. ARR enters
AtlasFlow's statements through the ASC 718 probability assessment for the ARR-based PSU tranche, where $2,000 of
headroom against a $170,000 threshold governs $7,593 of recognized compensation cost. Independently, the metric is
within disclosure controls and procedures under Exchange Act Rule 13a-15 and is other information the auditor must
read under AS 2710, so procedures are required even where the ICFR link is absent.

## Key Definitions

**Batch total.** A control total computed over a group of records before processing and compared to the same total
after processing, so that a record lost or altered in transit produces a difference. Zuora Billing's requirement
that invoice items sum to the invoice header or the run aborts is a batch total control.

**Benchmarking.** Carrying forward evidence about an automated application control obtained in a prior period in
place of retesting it, after verifying the program or configuration has not changed. PCAOB AS 2201, Appendix B, sets
the conditions, which include effective general IT controls over program change, access to programs, and computer
operations, and exclude controls subject to human intervention.

**Cloud configuration drift.** The change of vendor-hosted application settings between the date of the auditor's
test and the period the conclusion covers, without a code deployment and often without a change ticket. It is
addressed by obtaining the application's configuration audit trail for the full period.

**Configurable control.** An automated control whose behavior is determined by a value or rule a business user can
change through the application interface without a code deployment. Both the mechanism and the configured value,
together with the value's change history, are attributes the auditor must test.

**Data warehouse.** A database populated by replication from operational systems and used for reporting rather than
transaction processing. Because it is a replica, it may contain rows deleted upstream and omit rows created since the
last synchronization, so any population drawn from it requires reconciliation to source.

**Edit check.** A configured rule constraining data at the point of entry, of one of eight types: validity, format,
range or limit, dependency, duplicate, sequence, batch total, or reasonableness. A check operating correctly on a
field the accounting policy does not depend on provides no control.

**End-user computing (EUC).** Applications built and maintained by business users outside the IT change and access
framework, principally spreadsheets. `CONSOL_FY25_v14.xlsx` is EUC in the financial reporting chain: it produces the
consolidated trial balance with no version control, no formula-integrity check, and four users holding edit rights.

**Error queue.** The repository of records that failed an interface's validation and were not loaded to the target. It
is a population before it is a control, so its completeness must be established against an independent source such
as the target system's audit log.

**Fully automated application control.** A control operating entirely within an application, without human
participation, every time the triggering condition occurs. Its failure mode is systematic rather than random, which
is why one well-designed test can support a period conclusion when the conditions in §12.9 hold.

**Information produced by the entity (IPE).** Information generated by the entity's systems or personnel and used
either as audit evidence or in the operation of a control. PCAOB AS 1105 requires the auditor to test its accuracy
and completeness; AU-C 500 as amended by SAS 142 frames the same requirement through relevance and reliability,
including source, completeness, accuracy, and authenticity.

**Input control.** A control addressing whether transactions entering an application are authorized, complete,
accurate, and recorded in the correct period. In a SaaS order-to-cash flow these are configured almost entirely in
the quoting and billing applications and are dominated by edit checks and approval routing.

**Interface control.** A control operating on data crossing an application boundary, addressing whether every record
that left the source arrived at the target, whether it arrived unaltered, and how failures are dispositioned. The
error-handling mechanism is part of the control.

**IT-dependent manual control.** A control with an irreducible human step in which the person acts on
system-generated information. It fails in two independent ways — the person does not perform the step, or the
information is incomplete or inaccurate — so a test addressing only the first is incomplete.

**Output control.** A control proving that what emerged from processing equals what entered and reached the intended
destination, typically by control totals, subledger-to-ledger reconciliation, and restriction of report
distribution. An output control tying an interface to a subledger cannot detect entries posted directly to the
ledger.

**Parameter.** A value supplied at report or query execution that determines the population returned, most often a
date, an entity, and a status. A report substituting the run date for an explicit as-of parameter is not
reproducible and cannot serve as evidence about a past date.

**Processing control.** A control addressing whether accepted transactions are calculated, allocated, scheduled,
aggregated, and posted correctly. In a subscription business the dominant set is the revenue engine's configuration —
for AtlasFlow, 27 Zuora Revenue rules.

**Re-performance.** Independently executing a control or calculation to determine whether it produces the result it
should, including by submitting constructed test conditions and boundary values. It is the only technique
establishing that a configured mechanism operates as configured.

**Robotic process automation (RPA).** Software performing a sequence of application actions a person would otherwise
perform, typically using its own credentials. A script or bot is a process step rather than a control, audited as a
change-management population, as a holder of access rights subject to segregation of duties, and as a source of
misstatement.

**Segregation of duties, system-enforced.** Prevention of incompatible activity by application configuration rather
than by supervision — by denying conflicting permissions, preventing a user acting twice on a record, or requiring a
second party above a configured value. It fails silently when the configuration expresses a rule that is not the
intended rule.

**System-generated report.** Output produced by an application from its own data according to a stored definition. It
is not a control but an input to controls and procedures, and its reliability rests on eight attributes: source,
query, parameters, filters, completeness at source, reproducibility, integrity in transit, and change control.

**Test of one.** Inspection of a single actual transaction that passed through an automated control, relied on to
support a full-period conclusion. Its validity depends on conditions external to the test: that the control is
wholly automated, that program change and access controls were effective throughout, and that the auditor holds
independent evidence the configuration did not change.

**Three-way match.** Automated comparison of purchase order, receipt, and supplier invoice, blocking payment where
they disagree beyond a configured tolerance. Its design is evaluated by comparing each tolerance and each exempted
category to the approved procurement policy and by sizing the population that passed without human review.

**Tolerance.** The configured amount or percentage by which two values may differ without the automated control
intervening. Because it defines what the control permits, it is evaluated against materiality: a tolerance allowing
aggregate unreviewed variance approaching materiality is a design deficiency regardless of the variances that
occurred.

**Validation rule.** A configured constraint that blocks or warns on data failing a condition. Whether it blocks or
warns determines whether it is a control: a rule configured as a warning that permits the save records an audit
trail entry and prevents nothing.

## Chapter Summary

1. Misclassification, not poor execution, causes most defective application control testing; the four-question rule
   in §12.1.1 makes classification a documented conclusion rather than an assumption.
2. An IT-dependent manual control fails in two ways, and testing the sign-off addresses only one; the
   system-generated information the reviewer uses is part of the control and is tested as IPE.
3. Design and operating effectiveness are separate conclusions reached by different techniques: inspection against
   an approved criterion finds AP-CPQ-01's 45% boundary, and re-performance finds RC-20's failure to apply
   cumulative catch-up.
4. A test that cannot fail is not a test; state the attribute and the deviation condition before performing it.
5. An edit check that works perfectly on the wrong field is not a control, which is why AtlasFlow has no automated
   control capable of enforcing its own policy of recognizing revenue from the later of contract start and
   provisioning.
6. Configurable thresholds are evaluated against materiality: $250,000 against $940 of performance materiality
   leaves 3,847 of 4,912 manual entries unreviewed and lets six threshold-sized items exceed overall materiality.
7. Interface completeness fails in three distinct ways, and only a record-count reconciliation against an
   independently derived source count detects records never selected and records suppressed.
8. An error queue and a suppression rule are the two places an interface loses records silently; both are
   populations whose completeness must come from the target system's audit log.
9. A test of one supports a full-period conclusion only when four conditions hold, of which the fourth —
   independent evidence of configuration stability — failed at AtlasFlow because 2 of 11 RevPro configuration
   changes were made through a shared account.
10. Where the configuration changed mid-period, a test of one becomes a test of one per state; where a boundary is
    undocumented, no test establishes the earlier state and the control cannot be relied on.
11. Filters are the highest-yield of the eight report attributes: one "POB status ≠ On Hold" filter removed 41
    performance obligations and $196 of December revenue from the report the Controller reviews and from the ledger.
12. Tying a report to the general ledger proves nothing about completeness when both came from the same query.
13. A spreadsheet in the reporting chain is an application without change management, and a static `VLOOKUP` range
    dropped six UK accounts totaling $312 into a plug line nobody reviewed.
14. A script is not a control but a change-management population, a holder of access rights, and a source of
    misstatement — $148 of gross-versus-net error and $21 of unreversed duplicate revenue at AtlasFlow.
15. An operating metric produced in an uncontrolled reporting layer is inside ICFR when it feeds a recognized
    amount; ARR reaches AtlasFlow's statements through the ASC 718 probability assessment, where $2,000 of headroom
    governs $7,593 of recognized compensation cost.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| General IT controls every conclusion here depends on | Chapter 11 | W-1 through W-6 determine whether a test of one, benchmarking, or any reliance on an automated control is available |
| SOC 1 reports, complementary user entity controls (CUECs), and bridge letters | Chapter 11 | The vendor-side change management behind Zuora, NetSuite, and Coupa configuration, and the unmapped CUECs in W-10 |
| Walkthrough technique and "what could go wrong" analysis | Chapter 13 | How to obtain the process understanding that identifies which automated controls exist |
| Test design, sample sizes, deviations, and deficiency severity | Chapter 14 | The methodology for grading every deficiency identified here and the aggregation behind the ICFR conclusion |
| Management review controls and their precision | Chapter 14 | The Controller's review of the I-3 journal tested as a review control, not only as an IPE consumer |
| Recomputing subscription revenue and testing the engine's output | Chapter 5, §5.11 | The substantive work required when the RevPro configuration cannot be relied on |
| Revenue cut-off and the order-to-cash flow | Chapter 4 | The accounting consequence of the three December 29–31 order forms stuck in the I-1 error queue |
| Deferred revenue completeness and the RPO recomputation as IPE | Chapter 6 | The population and query whose reliability Exercise 12-11 evaluates |
| The aged trial balance as IPE and the CECL loss rates | Chapter 7 | Where the parameter risk in Solution 12-4 changes a measurement rather than a disclosure |
| Stock-based compensation and the ARR-based PSU probability | Chapter 9 | The ASC 718 estimate through which the Snowflake ARR metric enters the audited statements |
| Coupa, Concur, and the expenditure cycle | Chapter 10 | The accounting consequence of the match tolerances and non-PO categories in §12.7 |
| Journal entry population completeness and the manual-versus-automated flag | Chapter 16 | The $158 of December entries posted directly to revenue, and the 3,847 unreviewed entries under W-12 |
| Management override and order-form date modification | Chapter 17 | The fraud implications of the December 18 configuration change and the two subscriptions with no contract |
| Reliability of data used in analytics | Chapter 18 | Why an analytic run on a Snowflake replica inherits the replica's completeness exposure |
| Other information, MD&A metrics, and estimate bias | Chapter 19 | The AS 2710 procedures and audit committee communication arising from the case study |
| The adverse ICFR opinion and the material weakness description | Chapter 20 | Where the aggregated deficiencies identified here are reported |

## Further Reading

- PCAOB AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of
  Financial Statements*, including Appendix B on benchmarking of automated application controls.
- PCAOB AS 1105, *Audit Evidence*, on sufficiency and appropriateness and on information produced by the company.
- PCAOB AS 2110, *Identifying and Assessing Risks of Material Misstatement*, on the flow of transactions and the
  extent of automation.
- PCAOB AS 2301, *The Auditor's Responses to the Risks of Material Misstatement*, on testing the accuracy and
  completeness of information produced by the entity used in performing a control.
- PCAOB AS 1215, *Audit Documentation*, on the standard a configuration export and a parameter list must meet.
- PCAOB AS 2710, *Other Information in Documents Containing Audited Financial Statements*.
- AICPA AU-C 315, as amended by SAS No. 145, on understanding the IT environment and identifying risks arising from
  the use of IT and the general IT controls that address them.
- AICPA AU-C 500, as amended by SAS No. 142, on the attributes of information used as audit evidence.
- AICPA AU-C 330 and AU-C 265, on responses to assessed risks and on communicating internal control related matters.
- COSO, *Internal Control — Integrated Framework* (2013), Principles 10 through 13, together with the COSO guidance
  on applying the framework in technology and cloud computing environments.
- SEC Exchange Act Rules 13a-15 and 15d-15 on disclosure controls and procedures and management's assessment of
  internal control over financial reporting, and the SEC staff's interpretive guidance on key performance indicators
  and metrics in MD&A.
- FASB ASC 606-10-32 on allocation of the transaction price, which supplies the criteria for evaluating revenue
  engine configuration, and FASB ASC 718-10-25 and 718-10-30 on performance conditions.




