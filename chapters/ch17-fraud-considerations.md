# Chapter 17 — Fraud Considerations

> On January 14, 2026 an email reached AtlasFlow's audit committee mailbox from an address the company could
> not identify, alleging that "December deals were papered after the fact." The engagement team had already
> tested revenue cut-off, already brainstormed fraud risks in November, already concluded that period-end
> revenue recognition was a significant risk. None of that told the team what to do at 9:00 a.m. on
> January 15 — whom to tell, what to obtain before it changed, which population to define, and how $150 of
> revenue on six contracts could drive an adverse opinion on internal control. This chapter is about the gap
> between knowing that fraud risk exists and running the procedures that would find the fraud that exists.

## Learning Objectives

- **LO 17.1** Distinguish the auditor's responsibility for fraud from management's and from that of those
  charged with governance, and state the three limits on the auditor's responsibility.
- **LO 17.2** Apply the fraud triangle to a named SaaS company in quantities, including computing the effect
  of one booking on an executive's performance-share payout.
- **LO 17.3** Design an engagement team fraud discussion and a fraud inquiry set that produce a fraud risk
  register naming schemes, actors, systems, and assertions.
- **LO 17.4** Evaluate whether the presumed fraud risk in revenue recognition can be rebutted, and specify
  that risk to schemes and assertions across four SaaS revenue streams.
- **LO 17.5** Execute the three responses required regardless of assessed risk, including a retrospective
  review of estimates that tests for bias in both directions.
- **LO 17.6** Design overall responses, including unpredictability elements specified to the point that a
  staff auditor could perform them.
- **LO 17.7** Diagnose thirteen SaaS fraud schemes from their red flags, name the detection procedure for
  each, and explain why routine procedures miss each one.
- **LO 17.8** Distinguish operating-metric manipulation that misstates the financial statements from
  manipulation that does not, and state the auditor's differing responsibility for each.
- **LO 17.9** Conclude on and communicate a suspected fraud, and evaluate deficiency severity when the amount
  is immaterial.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2401, *Consideration of Fraud in a Financial Statement Audit* | The governing standard: the engagement team discussion, fraud inquiries, fraud risk factors, unusual or unexpected analytical relationships, the revenue-recognition presumption, the three responses required regardless of assessed risk, and the end-of-audit evaluation |
| AICPA | AU-C 240 | The substantively parallel private-company equivalent. Requires documenting the reasons if improper revenue recognition is not identified as a fraud risk; routes communications to those charged with governance |
| PCAOB | AS 2110; AICPA AU-C 315 (as amended by SAS 145, effective for periods ending on or after December 15, 2023) | Fraud risks are significant risks; inherent and control risk are assessed separately, so incentive and opportunity are documented as inherent risk factors and the control gap as a control risk conclusion |
| PCAOB | AS 2301 | Overall responses: assignment of personnel, supervision, and an element of unpredictability |
| PCAOB | AS 2201 | Fraud on the part of senior management, whether or not material, is an indicator of a material weakness — the hook that converts $150 into a reporting matter |
| PCAOB | AS 1301; AICPA AU-C 260 and AU-C 265 | Communication of fraud, illegal acts, significant unusual transactions, and control deficiencies, timed to permit appropriate action |
| PCAOB | AS 2810; AICPA AU-C 450; AS 1215; AU-C 230 | Evaluate whether identified misstatements indicate fraud; document the discussion, the risks, and the responses |
| PCAOB | AS 2405, *Illegal Acts by Clients*; SEC Exchange Act Section 10A(b) and Rule 10A-3 | Escalation when a possible illegal act is detected. For issuers: inform management, be satisfied the audit committee is informed, and escalate to the board — which must notify the Commission within one business day — if timely remedial action is not taken and the effect is material. Rule 10A-3 requires the complaint procedures the whistleblower mailbox exists to satisfy |
| PCAOB | AS 2410; AICPA AU-C 550 | Related-party and significant unusual transaction procedures, including evaluation of business purpose |
| FASB | ASC 606-10-25-1 | A contract exists only when the parties have approved it — why an unverifiable signature date is a recognition question, not a paperwork question |

The frameworks differ substantively in two ways. An integrated audit under AS 2201 forces the fraud finding
through an ICFR severity evaluation and into a public report, and Section 10A(b) creates a reporting path with
no private-company analogue: a private SaaS auditor reaching the same conclusion would communicate under
AU-C 240 and AU-C 265, evaluate the effect on the opinion, and consider withdrawal, but issue no control report.

## Prerequisites and Chapter Dependencies

Read Chapter 2 first: this chapter assumes the risk assessment matrix and the inherent-versus-control-risk
distinction. Chapter 13's finding that control FIN-REV-07 (the team's OTC-05) does not exist as documented, and
Chapter 12's analysis of the Salesforce CPQ approval configuration, supply facts used here without re-derivation.
Chapter 16 performs the journal entry testing this chapter requires, Chapter 18 supplies the analytical technique,
and Chapter 19 evaluates the resulting misstatements.

## 17.1 The auditor's responsibility, and the three limits on it

The obligation is one sentence, and it is narrower than most clients believe: plan and perform the audit to
obtain reasonable assurance about whether the financial statements are free of material misstatement, **whether
caused by error or fraud**. Fraud is not an engagement bolted onto the audit; it is the reason the audit is
designed the way it is. Three limits follow, and you should be able to state all three to an audit committee
without hedging.

1. **Reasonable, not absolute, assurance.** Procedures are effective against misstatements that leave evidence.
   Concealment, collusion, forgery, and management override defeat well-designed procedures. A subsequently
   discovered misstatement does not establish that the audit was deficient; the question is whether it was
   planned and performed with due care in response to the risks identified.
2. **Material, not any.** You are not engaged to find a $9 expense-report abuse. The exception, developed in
   §17.9, is that immateriality in dollars does not make a fraud irrelevant: fraud by senior management is an
   ICFR indicator regardless of amount.
3. **Fraud is harder to detect than error.** Error leaves a symmetrical trail. Fraud is directional, concealed,
   and usually located where the evidence is weakest — in a SaaS company, a date field in a sales system.

**Exhibit 17-1. Who is responsible for what.**

| Party | Responsibility | Evidence it was discharged | What you do with it |
| --- | --- | --- | --- |
| Management | Design and maintain controls that prevent and detect fraud; set the tone; investigate allegations | Code of conduct, fraud risk assessment, hotline, disciplinary record, Section 404(a) assessment | Test it. Management's fraud risk assessment is an input to yours, never a substitute |
| Audit committee | Oversee management's process; maintain Rule 10A-3 complaint procedures; oversee investigations | Charter, minutes, complaint log, records of commissioned investigations | Inquire directly and separately from management. A passive committee is itself a fraud risk factor |
| Internal audit (Michelle Fong, co-sourced) | Perform work management or the committee directs | The July 2025 readiness assessment with 14 gaps | Inquire about known or suspected fraud; use the work only after evaluating competence and objectivity |
| The auditor | Reasonable assurance about material misstatement from fraud; the required procedures; communication | The fraud risk register, the required-response workpapers, the AS 1301 communication | This chapter |

Asked in November 2025 what fraud risks management had identified, the CFO described the code of conduct and the
anonymous hotline. That answer established that management's fraud risk assessment was a compliance artifact —
no scheme, no owner, no quantified exposure — which raised assessed inherent risk on management override and
left the team's scheme-level analysis as the only one in existence.

## 17.2 The fraud triangle, quantified

The fraud triangle — incentive or pressure, opportunity, and rationalization or attitude — is useful only when
each leg is expressed in the client's own numbers. "The sales organization is under pressure" is not a risk
assessment. The following is.

**Incentive, computed.** The 2025 tranche of the Chief Executive Officer's annual recurring revenue (ARR) based
performance share units (PSUs) is 240 thousand units at a grant-date fair value of $34.10 (continuing case §3.5).
*For this illustration, assume* the payout scale is linear from 0% of target at ARR of $160.0M to 100% at
$174.0M. Reported ARR at December 31, 2025 was $172.0M, so:

- Payout = ($172.0M − $160.0M) ÷ ($174.0M − $160.0M) = 12.0 ÷ 14.0 = **85.7%**, the arithmetic behind
  management's Q4 revision of the probability assessment from 100% to 85% and the $1,340 catch-up credit.
- Marginal sensitivity = 100% ÷ $14.0M = **7.14 percentage points of payout per $1.0M of ARR**.
- The six December contracts whose signature dates could not be corroborated carry $2,340 of annual contract
  value: 2.34 × 7.14 = **16.7 percentage points**, which on 240 thousand units at $34.10 is 40 thousand units,
  or **$1,364 of grant-date value**.

Six contracts producing $150 of revenue — 10.3% of overall materiality of $1,450 — move an executive's equity
outcome by roughly $1,364, nine times the revenue effect. A fraud risk assessment that sizes incentives by the
income statement effect will systematically underestimate them in a SaaS company, because the metric that pays
people is ARR, and ARR does not care what day in December a contract was signed.

**Exhibit 17-2. Fraud triangle applied to AtlasFlow, FY2025.**

| Leg | Condition | Quantification | Source |
| --- | --- | --- | --- |
| Incentive | CEO compensation weighted to ARR-based PSUs | 7.14 pp of payout per $1.0M of ARR; $1,364 on the six contracts | §3.5; computed above |
| Incentive | Chief Revenue Officer compensated on bookings | *Illustration:* FY2025 plan $196,000 against reported bookings $201,300. Without the $25,174 signed December 24–31, bookings of $176,126 would have missed plan by **$19,874** | §5.1; illustration |
| Opportunity | VP Sales Operations administers CPQ and can edit order-form dates after activation, and the documented order-validation control FIN-REV-07 / OTC-05 does not exist | 41 post-activation edits to `Contract_Signed_Date__c` / `Service_Start_Date__c` in FY2025, 9 in the final week of a quarter, against no functioning preventive control | Chapter 13 |
| Opportunity | Unapproved change to the CPQ approval configuration by the same person | Discount boundary moved 40% → 45% on December 18 at 19:42 CT; 23 order forms activated December 18–31 in that band, ACV $4,180, of which 21 escaped required CFO approval | Chapter 12 |
| Rationalization | Management's position: the deals were agreed in December and the paperwork is a formality | Recorded verbatim, because the belief that timing is administrative is the belief that makes backdating feel permissible | Chapter 4, §4.9 |
| Rationalization | VP Revenue Accounting on a performance plan since March 2025; two revenue accountants resigned in Q2 | Personnel pressure in the function that would have to detect the scheme | §1.8, §5.1 |

The exhibit does not say anyone at AtlasFlow is dishonest. Every row is an observable condition; the discipline
is to record conditions and let procedures answer questions about conduct.

## 17.3 The required fraud risk assessment procedures

### 17.3.1 The engagement team discussion

The discussion is not a meeting at which the manager reads last year's risks aloud. Its purpose is to pool what
different people know: the IT auditor knows who can edit which field, the data specialist knows what the
population looks like, the partner knows what management told the audit committee. Brightline held it on
**November 12, 2025**, for 90 minutes, before the fraud risk register was drafted.

**Exhibit 17-3. Engagement team fraud discussion agenda, November 12, 2025 (WP 2100-01).**

| Item | Minutes | Owner | Required output |
| --- | --- | --- | --- |
| 1. Ground rule: assume the misstatement happened and work backward to how | 5 | Whitcombe (partner) | Recorded verbatim in the minutes |
| 2. Changes since FY2024 that create opportunity: NetSuite upgrade and SoD rebuild, RevPro February configuration change, Snowflake datamart, Kestrel integration | 15 | Nazari, Iyer | Each condition mapped to a system and a person |
| 4. "How would you do it?" — each attendee proposes a scheme and its concealment step | 25 | All | 11 candidate schemes with concealment steps |
| 6. Rebuttal test for the revenue presumption; misappropriation schemes including purchase cards | 15 | Whitcombe, Nwosu | Exhibit 17-6; two schemes carried to the register |
Item 4 is where the value is. Three of the 11 candidate schemes had not appeared in the FY2024 file: the
post-activation date edit that does not push back to Zuora, reclassification of committed workflow runs into
billable overage, and the October 2025 migration of Kestrel's spreadsheet-billed contracts into Zuora. Two of the
three produced procedures that found something. Treat the discussion as continuing: the team reconvened
January 15, 2026, documented as a continuation entry.

### 17.3.2 Inquiries — and the answers, which are the evidence

Inquiries of management alone are nearly worthless as fraud evidence, because the person most likely to be
involved is the person answering. Their value is a baseline representation you can later contradict, plus the
responses of people whose incentives differ.

**Exhibit 17-4. Fraud inquiry set and responses received (WP 2100-02, extract).**

| # | Person | Question | Response received | Evaluation and follow-up |
| --- | --- | --- | --- | --- |
| 1 | Okafor (CFO) | What fraud risks has management identified, with schemes and owners? | The code of conduct and the hotline; no scheme-level analysis exists | Management's assessment is not risk-based; raises assessed risk on override. No document to inspect |
| 3 | Kim (VP Revenue Accounting) | Has anyone asked you to recognize revenue on a contract you thought was not signed? | "Asked, no. Pushed on timing, yes — every quarter end. Sales Ops sends the file at 6:00 p.m. on the last day" | Specific, testable, adverse to his own function. Obtain the December 31 transmittal and compare to the activated population |
| 5 | Hallowell (VP Sales Ops) | Who can change the signature date after activation, and does it flow to Zuora? | "I can. Deal Desk can. It does not push back to Zuora automatically" | A volunteered admission of capability. Obtain the field-history extract |
| 7 | Dr. Ashford (Audit committee chair) | How do complaints reach you, who screens them, and what has arrived this year? | Rule 10A-3 mailbox monitored by outside counsel; nothing as of November | Establishes the baseline that makes the January email a change in condition |
| 9 | Sales representative (auditor-selected) | What happens to a deal that slips past the last day of a quarter? | "It counts next quarter. Sometimes the date gets fixed. I have seen it" | The most valuable answer obtained: unrehearsed corroboration that capability is practice. Escalated to the partner the same day |

Two disciplines make this table work. **Ask people outside the financial reporting function, chosen by you**,
because "what happens to a deal that slips" cannot be answered defensively by someone who does not know it is a
fraud inquiry. And **write down the answer, not your summary of it**: row 9 is evidence because it is a quotation.

### 17.3.3 Fraud risk factors and unusual or unexpected analytical relationships

You must consider the fraud risk factors in the appendices to AS 2401 / AU-C 240 and evaluate whether analytical
relationships identified during risk assessment indicate a fraud risk. The second requirement is performed badly
because teams run analytics designed to detect error, not concealment.

**Exhibit 17-5. Unusual or unexpected relationships considered (in thousands).**

| Relationship | Computation | Observed against expected | Fraud interpretation and next step |
| --- | --- | --- | --- |
| Q4 bookings concentration in the final five business days | $25,174 ÷ $61,400 | **41.0%** against 27% a year earlier | At 27% the last-week ACV would be $16,578; excess $8,596. Not a misstatement; it defines the cut-off test population (Chapter 4, §4.9) |
| Usage overage versus subscription growth, Q4 | Overage $1,390 ÷ $1,090 = +27.5%; Core $28,200 ÷ $26,900 = +4.8% | +27.5% against +4.8% | Flagged. Overage is computed from metering data with no independent recomputation. Recompute overage from raw run counts and test the committed-volume field for edits (§17.8.3) |
| Deferred revenue relationship | Revenue from current-period billings $93,300 ÷ billings $163,750 = 57.0% | 57.0% against an expectation of 55%–58% | **Passes — and that is the point.** Backdating six contracts adds $2,100 of billings and $150 of revenue, or 0.37% of Q4 revenue, far inside any achievable precision |

The last row is the most important analytic in the chapter because it is the one that finds nothing. State in the
workpaper which schemes your analytics cannot detect: a fraud risk no analytic can reach requires a test of
details against evidence from outside management's control.

## 17.4 The revenue presumption, and why you cannot rebut it here

You must presume a risk of material misstatement due to fraud relating to revenue recognition. The presumption is
rebuttable in principle; in a SaaS company it is not rebuttable in practice, and "we never rebut it" is not
documentation.

**Exhibit 17-6. Rebuttal test applied to AtlasFlow's revenue streams (in thousands).**

| Condition that would need to hold | Core / Insight enterprise ($131,600) | Usage overage ($4,200) | Professional services ($12,400) | Self-serve Stripe ($6,100) |
| --- | --- | --- | --- | --- |
| Recognition depends on no date or estimate a person can set | Fails — signature and start dates are editable | Fails — metering and committed-volume fields | Fails — estimated total hours | Holds — recognition follows the card charge |
| No incentive attaches to the reported amount | Fails — bookings compensation, ARR PSUs | Fails — feeds ARR expansion and retention | Fails — services attainment | Largely holds |
| Nobody outside accounting can initiate or alter a revenue record | Fails — see Exhibit 17-2 | Fails | Fails | Fails — the Stripe-to-NetSuite Lambda job is in-house code with two unapproved FY2025 changes (W-7) |
| Conclusion | Presumption stands | Presumption stands | Presumption stands | Presumption stands, on the last condition alone |

The self-serve column is instructive: one condition holds and a second largely does, the presumption still stands
on the third because of W-7, and the *specification* differs completely. For enterprise revenue the scheme is period-end date manipulation and the
assertions are occurrence and cut-off; for self-serve it is manipulation of the summarization job or of refund
processing, and the assertion is accuracy. That is the useful move — not rebutting the presumption but specifying
it. "Revenue recognition" generates no procedure; "the CPQ administrator alters the signature date on enterprise
order forms activated in the final week of a quarter" generates four.

**Exhibit 17-7. Fraud risk register, FY2025 (WP 2100-03, extract).**

| Ref | Scheme, stated as an action by a person | Type | Accounts | Assertion | Significant risk | Response |
| --- | --- | --- | --- | --- | --- | --- |
| F-1 | The CPQ administrator edits `Contract_Signed_Date__c` or `Service_Start_Date__c` after activation so a January contract falls in December | FFR | 4100, 4110, 1200, 2400 | Occurrence, cut-off | Yes | 100% test of December stratum A with three external evidence sources; full-year field-history extract (WP 3200-15) |
| F-2 | A sales representative grants a concession in a side letter never entered in Zuora | FFR | 4100, 2400, 2230 | Occurrence, accuracy | Yes | Terms confirmations with 8 customers; DocuSign envelope inventory against the repository; specific representation |
| F-3 | Committed workflow runs are reclassified as billable overage, or committed volume is reduced | FFR | 4120 | Accuracy | Yes | Recompute overage from metering data for 12 accounts; field-history test of committed volume |
| F-5 | The allowance for credit losses is built in a good quarter and released in a bad one | FFR | 1210, 6300 | Valuation | Yes | Retrospective review of the FY2024 allowance; recomputation of the CECL overlay (Chapter 7) |
| F-6 | Deferred revenue is released without delivery by shortening a term or accelerating a start date in RevPro | FFR | 2400, 2410, 4100 | Completeness of the liability | Yes | RevPro modification report reconciled to executed amendments (Chapter 6) |
| F-9 | ARR, retention, or RPO is computed on a definition changed mid-year in the Snowflake datamart | Metric | RPO only | Presentation (RPO); other information (ARR, retention) | Yes for RPO | Recompute RPO from the contract population; AS 2710 / AU-C 720 procedures on the metrics (§17.8.4) |
| F-11 | Management override, including an expense-reimbursement scheme by a manager with approval authority and top-side entries in the consolidation workbook outside NetSuite | MoA and FFR | 6200, 6300, any | Occurrence, any | Yes | Full-population Concur analytics (Exhibit 17-11); 100% test of the 27 top-side entries (Chapter 16) |

Legend: FFR = fraudulent financial reporting; MoA = misappropriation of assets; Metric = manipulation of a
disclosed metric that may or may not misstate the statements (§17.8.4). An entry is treated as a significant risk
unless the team can articulate why the scheme could not produce a material misstatement — F-9 is the only partial
exception, and only because ARR and retention appear outside the statements. Every entry names an action, not a
topic. A register you can read aloud as "someone in role X does Y in system Z" produces procedures.

## 17.5 The three responses required regardless of assessed risk

**Journal entry testing.** Chapter 16 owns the mechanics; what belongs here is why the requirement exists and
what it cannot do. It exists because the last step of most financial-reporting frauds is a manual entry that
bypasses the process. At AtlasFlow the required testing covered 4,912 manual entries and 27 top-side entries and
**did not detect the December backdating**, because the scheme required no entry: the altered date flowed from
Salesforce through Zuora into the routine monthly interface journal (I-3), which looked exactly like the other
eleven. Journal entry testing covers schemes that end in an entry, not schemes that end in a field.

**Retrospective review of estimates for bias.** Look back at significant prior-period estimates and evaluate
whether the judgments indicate bias, in both directions and across the full set.

**Exhibit 17-8. Retrospective review of FY2024 estimates (WP 3800-07, in thousands).**

| Estimate | FY2024 recorded | Outcome known in FY2025 | Direction | Interpretation |
| --- | --- | --- | --- | --- |
| Allowance for credit losses | 1,350 | Write-offs of 1,230 against it; 90 released | Income-favorable | Defensible alone; the pattern matters more |
| Estimated total hours on fixed-fee PS engagements open at 12/31/2024 | Implied 92% complete on 31 engagements | Final hours exceeded estimate on 24 of 31; revenue accelerated about 185 | Income-favorable | 24 of 31 in one direction is not random. This is the finding |
| Commission benefit period | 4 years | Average customer life computed on FY2025 data: 4.3 years | Income-unfavorable | Conservative; evidence that management is not uniformly aggressive |
| SLA credit accrual | Nil | $290 of FY2024 credits identified in FY2025 | Income-favorable | Systematic non-accrual; corrected as C-2 |

Three of the four estimates resolved income-favorably and the services hours did so in 24 of 31 individual cases,
though no item is material. The documented conclusion is a **tendency toward income-favorable estimation**, which
raises assessed risk on the FY2025 estimates — particularly the CECL overlay, where U-2 of $(240) sits at the
optimistic end of the acceptable range. A 15-of-31 split would have been noise, and the conclusion would have read
"no indication of bias."

**Business rationale for significant unusual transactions.** For each significant transaction outside the
normal course, evaluate whether the form appears designed to obscure the substance.

**Exhibit 17-9. Significant unusual transactions evaluated (WP 4100-02).**

| Transaction | Rationale asserted | Auditor's evaluation |
| --- | --- | --- |
| The December 18, 19:42 CT change to the CPQ approval thresholds | "Aligning the tool with practice" | Not credible. A control configuration changed nine business days before year end, by the person whose approvals it governs, with no ticket, permitting 21 order forms to bypass CFO approval. Treated as a fraud risk factor and an ICFR deficiency |
| Two revenue arrangements with a vendor from whom AtlasFlow simultaneously purchased services | "Independent commercial negotiations" | Tested by benchmarking pricing to third-party quotes and examining the negotiation sequence (Exhibit 17-11) |

## 17.6 Overall responses: staffing, supervision, and unpredictability

**Assignment of personnel.** The data and analytics specialist was assigned to the revenue cut-off population
rather than to general analytics, because the procedure that mattered was a full-population field-history
extract; the interviews of non-financial personnel went to the manager rather than to staff, because an
unrehearsed answer must be recognized as important in the moment.

**Supervision.** The senior manager reviewed the December order-form selection before management was told which
items were selected, and the engagement quality reviewer was briefed on January 15, 2026, the day after the team
learned of the allegation.

**Unpredictability.** The requirement is an element of unpredictability in the nature, timing, or extent of
procedures. It is not increasing a sample from 25 to 30 items, and it is not "a different sample than last year,"
which is what sampling does anyway.

**Exhibit 17-10. FY2025 unpredictability elements.**

| Element | What was done | Why the client cannot anticipate it | Result |
| --- | --- | --- | --- |
| Timing | Unannounced examination of the December 24–31 order-form population on **January 6, 2026**, before the close was complete and before management had assembled the auditor's file | The documents were obtained in the state they were in, not the state they would be in once someone knew which 43 items were selected | Two of the six eventual exceptions came from documents later re-uploaded |
| Population | An extract of *all* FY2025 post-activation edits to the date fields, not a sample of December | The client's model was that auditors test December | 41 edits, 9 in the final week of a quarter |
| Account | 20 entries in account 2230, customer credits and refunds payable, below performance materiality and untested in FY2024 | A seldom-tested account is where a concession gets parked | 3 January 2026 credits for FY2025 service, $61 |

## 17.7 Management override of controls

Every required response above exists because management can override the controls it designed. AtlasFlow has five
override pathways, and only the first is reached by journal entry testing: the Controller can post entries and
modify the RevPro-to-NetSuite mapping (W-13) below the $250,000 approval threshold (W-12); two developers hold
standing write access to production RevPro configuration (W-6), and configuration changes are not journal
entries; the date fields that drive recognition are editable by three roles; four local admin accounts exist in
RevPro, one shared (W-1), and the consolidation workbook sits outside NetSuite (W-8); and a superior can direct a
subordinate, which no control detects. The procedures that reach the last four are configuration audit trails,
field-history extracts, reconciliation of the workbook plus 100% testing of the 27 top-side entries, and separate
inquiry of the subordinate — which is how Exhibit 17-4 row 3 was obtained.

## 17.8 A catalogue of SaaS fraud schemes

Thirteen schemes follow, each stated as mechanics, red flags, detection, and why routine procedures miss it. The
fourth element is the substantive content: knowing a scheme exists is worthless if your program cannot reach it.
Four are developed in full because the walkthrough and case study turn on them; the remaining nine are
catalogued to the same specification in Exhibit 17-11.

### 17.8.1 Quarter-end holdover and backdating

**Mechanics.** A contract agreed in December is signed in January; the signature date, the service start date,
or both are entered or edited as December dates, and the subledgers behave correctly on incorrect inputs.
**Red flags.** Bookings concentration in the final days (41% of Q4 ACV against 27% a year earlier); wet-ink PDFs
replacing electronic signature on high-value deals; post-activation date edits; tenant provisioning after the
contract start. **Detection.** Three sources outside management's control per contract: the DocuSign completion
certificate (signer email, IP address, timestamp), the platform tenant-creation log, and Salesforce field history.
Where all three are absent, confirm the execution date itself, not the balance. **Why routine procedures miss it.**
Vouching the order form to the invoice to the revenue schedule is internally consistent whatever the true date,
because every document in that chain is inside the client's control — and the revenue effect, 0.37% of Q4 revenue,
is invisible to any analytic.

### 17.8.2 Side letters

**Mechanics.** A separate document or email grants a right the order form does not disclose — termination,
refund, contingent concession, extended acceptance, a free extension — and is never entered in Zuora.
**Red flags.** Credits issued shortly after period end (three January 2026 credits, $61, for FY2025 service);
disputes at collection; DocuSign envelopes to the customer's domain absent from the repository. **Detection.**
Compare the full envelope inventory for an account to the repository; confirm *terms*, asking whether any
agreements, understandings, or amendments exist other than those listed; read the customer-success and legal
ticket queues for 60 days after period end; obtain a representation naming side letters. **Why routine procedures
miss it.** A side letter is a document the client does not give you, and a balance confirmation returns "agreed"
because the receivable is genuinely owed — the misstatement is in the transaction price.

### 17.8.3 Usage-data manipulation

**Mechanics.** Consumption revenue depends on data generated by the product, not by the accounting system.
Overage can be inflated by reducing a customer's committed run volume, re-running a metering job, redefining a
billable run, or including internal and test traffic. **Red flags.** Overage growing far faster than platform
volume (Q4: +27.5% against Core +4.8%); metering jobs re-run near period end; edits to the committed-volume
field. **Detection.** Recompute overage for a sample of accounts from raw event counts in the platform database —
not the billing system — against committed volumes on the executed order forms at the contractual rate, and agree
to the invoice; extract full-year field history for the committed-volume field. **Why routine procedures miss it.**
The trail from invoice to revenue is clean, and the usage number is information produced by the entity from a
system most audit teams never touch.

### 17.8.4 Operating metric manipulation — and where your responsibility ends

**Mechanics.** ARR, retention, customer counts, and remaining performance obligations (RPO) are computed in the
Snowflake RevOps datamart, unreconciled to the general ledger for the first three quarters of FY2025 (W-11).
Manipulation takes three forms: changing a definition mid-period without disclosure (excluding small churned
customers from the retention denominator), changing the data (including an unsigned contract), and changing the
computation (annualizing a month containing one-time consideration). **The distinction that matters.** RPO is a
**financial statement disclosure** under ASC 606 and is audited like any other: you recompute it from the
contract population and test the enforceable-term judgments, and a misstatement of RPO is a misstatement. ARR and
retention are **not** GAAP measures and sit outside the statements; they are other information under
AS 2710 / AU-C 720, which requires you to read them, consider whether they are materially inconsistent with the
statements or with knowledge obtained in the audit, and respond if they are — not to audit them.
**Operationally.** A definitional change raising reported retention from 108% to 112% is not a misstatement. It is
a first-order fraud risk factor, because it evidences an attitude toward reported results, and it changes your
assessment of whether that attitude reached the statements. Say both things in the workpaper, separately.
**Why routine procedures miss it.** The metric is not in the trial balance, so nobody tests it — and the team that
does often either audits it, implying assurance it has not obtained, or ignores the inconsistency.

### 17.8.5 The remaining nine schemes

**Exhibit 17-11. SaaS fraud scheme catalogue (in thousands where amounts appear).**

| Scheme | Mechanics | Red flags | Detection procedure | Why routine procedures miss it |
| --- | --- | --- | --- | --- |
| Channel stuffing through resellers | Order forms booked with a reseller holding no end customer, on terms making it whole through return rights or extended payment | Period-end concentration; reseller receivables aging beyond the population | Tie each of the 41 reseller order forms ($9,700) to end-customer provisioning in the tenant log; confirm return rights with Tessera Partners | The order form is genuine and the reseller creditworthy; principal-versus-agent analysis answers gross-versus-net, not whether demand exists |
| Round-tripping / reciprocal arrangements | A $400 subscription sale paired with a $400 purchase from the same party: both legs real, neutral in substance, revenue inflated | A customer that is also a vendor at similar amounts on contemporaneous dates | Join customer master to vendor master on tax identification number; test each matched pair for independent negotiation; benchmark the purchase to a third-party quote | Revenue testing looks at revenue and expenditure testing at expense; neither sees the pair |
| Standalone selling price manipulation | SSP set to move consideration out of services, recognized as delivered, into the subscription, recognized ratably | Insight's thin standalone population (31 sales); an SSP memo dated after the quarter it governs | Recompute the allocation using *your* SSP range and quantify the effect at each end; test whether management's observable-price population excludes low outliers | The RevPro arithmetic is correct; the judgment is the input, so recomputing the engine confirms the engine |
| Cookie-jar reserves | An allowance built above the supportable range in a strong period and released in a weak one | Allowance as a percentage of receivables moving inversely to earnings; a release unexplained by the aging | Recompute the allowance from the aging and loss rates as a range against the recorded $1,900; test support for every release entry to account 1210 | Each period's balance is defensible alone; the scheme appears only across periods, and only if both directions are examined |
| Deferred revenue released without delivery | A term shortened or a modification processed so the same consideration is recognized over fewer days | Modifications with no executed amendment; term changes clustered at period end | Reconcile the RevPro modification report item by item to executed amendments and recompute each catch-up | Customers do not confirm your liability, and the roll-forward ties because it is built from the same altered data |
| Capitalization abuse — commissions and software | Costs that should be expensed are capitalized, benefit periods stretched, or hours coded to a capitalizable stage after the fact | 22% of FY2025 capitalized hours on retroactively restaged Jira epics; $1,900 of commissions for non-renewed customers (produced C-3, $620) | Test hours on restaged epics against the Jira change history; ask two developers what they built in a named sprint; test the churn file against capitalized commissions | Recomputing amortization confirms arithmetic; whether the cost belonged in the balance needs evidence from the engineering system |
| Expense misclassification to protect gross margin | Support engineers recoded from account 5110 to 6100, or hosting allocated to R&D: net loss unchanged, subscription margin improved | Margin improving faster than scale explains (80.0% against 78.6%); mid-year departmental recoding | Obtain the FY2025 departmental change history from ADP and Deel and quantify each recoding; each $1,000 out of 5110 adds 0.74 pp | Net loss is unaffected, so a bottom-line-oriented program never looks, and classification is rarely a relevant assertion |
| Related-party revenue | Revenue from an entity in which an officer, director, or investor has an interest, on non-arm's-length terms or undisclosed | A customer address matching a director's affiliation; a deal closed outside the approval path | Join the directors-and-officers questionnaires and investor list to the customer master; test terms against the population's pricing distribution | The usual procedure is a representation plus a questionnaire — both assertions by the party with the incentive |
| Expense reimbursement and purchase-card schemes | Duplicate Concur submissions, personal expenses coded to an unscrutinized department, splits below a receipt threshold | Amounts clustered below the receipt threshold; one amount and date submitted twice under different categories | Full-population Concur analytics: duplicate amount-date-vendor triples, items within 5% below the threshold, approvals by a subordinate | Amounts sit below any materiality threshold, so the population is never sampled — yet misappropriation by a manager with approval authority matters qualitatively |

## 17.9 Responding to identified or suspected fraud, and the communications

When you identify a misstatement that may result from fraud, or receive an allegation, four things change at
once and the sequence matters.

1. **Evaluate the implications, not just the item.** A possibly intentional misstatement is not an isolated
   exception even below the clearly trivial threshold. Ask what else the same person could have done, and whether
   the misstatement contradicts a control conclusion you have already reached.
2. **Reconsider the risk assessment and the reliability of representations.** If a date field was altered, every
   procedure that relied on it is suspect and every representation about contract completeness is weaker.
3. **Obtain evidence you do not have to ask management to assemble.** Once management is a possible subject,
   populations must come from immutable logs, the vendor, or counterparties.
4. **Escalate inside the firm before outside it** — partner, engagement quality reviewer, national office, and,
   where a possible illegal act arises, the firm's general counsel.

**Exhibit 17-12. Who must be told what, and when.**

| Recipient | Trigger | Requirement | Timing at AtlasFlow |
| --- | --- | --- | --- |
| Management, at least one level above those involved | Any identified or suspected fraud | Required; where senior management may be involved, communicate to the audit committee instead | CFO and Controller informed January 16, 2026, after the committee chair |
| Audit committee | Fraud involving senior management, or any fraud causing a material misstatement; uncorrected misstatements; significant unusual transactions; and, in writing, any material weakness or significant deficiency | Required under AS 2401, AS 1301, and AS 2201, with no dollar threshold for senior-management fraud | Chair January 15, 2026; full committee January 22; written communication February 12, including the revenue cut-off material weakness |
| Regulators | For an issuer, a likely illegal act with a material effect where remedial action is not taken | Section 10A(b) escalation to management, the committee, then the board, which must notify the Commission within one business day | Not triggered: the committee commissioned an investigation within one business day and management corrected the control |

Two judgment points. **Do not ask management's permission to tell the audit committee**; where senior management
may be implicated the committee is the first external recipient, and telling management first can defeat
procedures you have not yet run. **An investigation commissioned by the committee is not your evidence**; you may
read the report, interview its authors, and use it to direct your work, but you must obtain evidence yourself,
evaluate the investigators' objectivity and competence, and satisfy yourself the scope was not drawn to avoid
your question.

Document, at a minimum: the engagement team discussion (participants, timing, subjects, conclusions); the
identified fraud risks and their linkage to responses; the results of the required procedures; the fraud inquiries
and the responses received; the reasons for any conclusion that the revenue presumption did not give rise to an
identified fraud risk; and the nature of any fraud communications.

## 17.10 Professional skepticism as an operational discipline

Skepticism is not an attitude asserted in a memo; it is behavior visible in a transcript. The following exchange
occurred on January 20, 2026 and is recorded at WP 3200-14.

```text
GRL:  Six order forms have December signature dates and no DocuSign certificate. Why
      were these six signed on paper?
EV:   Some enterprise customers still print and sign. Legal is fine with it.
GRL:  How many of the 3,412 order forms activated in FY2025 were wet-ink? Nineteen.
      Six of the nineteen fall in the last eight days of December, and four of those
      six also show a date field edited after activation. What explains that?
EV:   The reps were racing the clock. It is a documentation issue, not an accounting
      issue — the deals were agreed in December.
GRL:  Then tell me what evidence exists that would let me distinguish a contract agreed
      and signed in December from one agreed in December and signed on January 3. Not
      what you believe happened; what document would show it.
EV:   ... There is the rep's email traffic.
GRL:  Then let us look at the email traffic for all six, through your counsel. If it
      shows customer assent in December, I will change my conclusion.
```

Four behaviors. The first turn asks a question with a factual answer instead of accepting a characterization. The
second puts the answer in a population — 19 of 3,412 — because "some customers still print" means something
different when the base rate is 0.6% and the December final-week rate is 32%. The third refuses the offered frame
("documentation issue, not an accounting issue") and converts it into an evidential question: what document would
distinguish the two states of the world? The fourth commits in advance to what would change the conclusion, which
forecloses retrospective rationalization and is fair to the client. The absence of skepticism is equally
diagnosable, and the diagnostic is not tone: it is a conclusion supported only by a management explanation, with no
statement of what evidence was sought and what would have changed the answer.

## Step-by-Step Walkthrough: Investigating the January 2026 Whistleblower Allegation

The allegation in full, as forwarded to Brightline on January 14, 2026: *"You should look at the December
deals. Several were papered after the fact. Sales Ops changed the dates."* Tick marks: **(a)** agreed to a
source outside management's control; **(b)** recomputed; **(c)** confirmed with a third party; **(d)** inquiry,
corroborated; **(e)** exception noted.

**Step 1. Log receipt and preserve the artifact.** Obtain the email with full headers from the committee chair's
counsel, not from management, and record the date received, the sender, the recipients, and that management was
not the source. *If it reached you from management first*, record that too — it bears on tone and means the
subject may already know.

**Step 2. Do not tell management yet, and record why.** The allegation names a function outside finance and the
evidence you need is editable, so the first communication is to the audit committee chair. Document the
reasoning; a reviewer must be able to follow the sequencing.

**Step 3. Reconvene the engagement team discussion within one business day.** Attendees: partner, senior manager,
manager, IT audit senior manager, data specialist. Output: three testable assertions — (i) date fields were
edited after the fact; (ii) the edits moved revenue into FY2025; (iii) the practice extended beyond December.
Brief the engagement quality reviewer the same day. **(d)**

**Step 4. Notify the chair and agree the division of work.** Obtain in writing whether the committee will
commission an investigation, who will conduct it, and its scope, and confirm your procedures are not contingent on
it. *If the committee declines to investigate*, that is a scope limitation with reporting and continuance
consequences; consult the national office first.

**Step 5. Obtain the data directly.** Request read-only access to Salesforce field history and the Setup Audit
Trail, the DocuSign envelope inventory with completion certificates, and the platform tenant-creation log. Ask
whether any retention window would expire and request a hold. *If the client offers only extracts prepared by
Sales Operations*, escalate — the preparer is the subject.

**Step 6. Define three populations, not one.** P1: the 118 order forms activated with signature dates
December 24–31, 2025, ACV $25,174. P2: the remaining December 1–23 activations. P3: all FY2025 post-activation
edits to `Contract_Signed_Date__c` and `Service_Start_Date__c`. Reconcile P1 to the bookings report and the
RevPro contract population so completeness is proven rather than asserted. **(b)**

**Step 7. Run the field-history query on P3**, requesting the parent record's activation timestamp with it.

```sql
SELECT ParentId, Field, OldValue, NewValue, CreatedById, CreatedDate
FROM   Opportunity_Field_History
WHERE  Field IN ('Contract_Signed_Date__c','Service_Start_Date__c')
AND    CreatedDate BETWEEN 2025-01-01 AND 2026-01-31
AND    CreatedDate > Activation_Timestamp__c
ORDER  BY CreatedDate;
```

**Step 8. Analyze the 41 records returned** by direction of the change, timing relative to quarter end, and
editing user.

**Exhibit 17-13. Post-activation date edits, FY2025 (41 records).**

| Attribute | Count | Of which in the final week of a quarter | Interpretation |
| --- | --- | --- | --- |
| Edits moving the date earlier | 26 | 9 | The direction that accelerates revenue |
| Edits moving the date later | 11 | 0 | Consistent with correcting a keying error |
| **Total** | **41** | **9** | |
| Edited by `bhallowell` (VP Sales Operations) | 22 | 7 | The admitted capability, exercised |
| Edited by Deal Desk users | 15 | 2 | |

Arithmetic: 26 + 11 + 4 (no net change) = 41; 22 + 15 + 4 (record owner) = 41. All nine final-week edits moved
dates earlier and seven were made by one user. **(a) (e)**

**Step 9. Test the nine edits, then all of P1, against three external sources.** For each item obtain the
DocuSign completion certificate, the tenant-creation timestamp, and a transmittal from the customer's own email
domain. Stratum A of P1 (43 items, ACV $19,240) was tested at 100% on January 6, 2026 before management
assembled the file; stratum B (75 items) by attribute sample of 14. **(a) (c)**

**Step 10. Isolate the items with no external corroboration.** Six order forms carry December signature dates
with no DocuSign certificate and no customer-domain transmittal (Exhibit 17-14), aggregate ACV $2,340. Four also
appear in the field-history extract. **(e)**

**Step 11. Compute the revenue effect, contract by contract**, as days recognized in FY2025 × ACV ÷ 365:
$660 × 31 ÷ 365 = $56.1; $480 × 24 ÷ 365 = $31.6; $420 × 22 ÷ 365 = $25.3; $360 × 20 ÷ 365 = $19.7;
$240 × 17 ÷ 365 = $11.2; $180 × 12 ÷ 365 = $5.9. Total **$149.8**, carried at $150 as uncorrected misstatement
U-3. Also quantify what is not revenue: $2,340 of ARR, $2,100 of billed receivables and deferred revenue, and
about $210 of capitalized commissions. **(b)**

**Step 12. Link the allegation to the control configuration.** The Setup Audit Trail records `bhallowell`
changing the AP-CPQ-01 step 3 and step 4 entry criteria on December 18, 2025 at 19:42 CT, moving the CRO/CFO
discount boundary from 40% to 45% with no Jira ticket. Twenty-three order forms activated December 18–31 fell
in the 40.01%–45.00% band, ACV $4,180, of which 21 would have required CFO approval and did not obtain it.
**(a) (e)**

**Step 13. Interview in the right order, after you have the data.** Take the two sales representatives and the
Deal Desk analyst first, then Jordan Pike, Daniel Kim, Brett Hallowell, and Sofia Marchetti, with the extract in
hand. Ask open questions before showing it, and record answers verbatim. *An explanation you cannot test is not
an answer*; convert it into a document request, as in §17.10.

**Step 14. Widen deliberately to adjacent schemes.** Because the mechanism is documentation created to fit a
period, test three further populations: January 2026 credits for FY2025 service (§17.8.2 — three items, $61);
December reseller activations with no provisioned tenant (none); and commissions accrued on the six contracts,
which did not reverse when the contracts were questioned ($210).

**Step 15. Conclude in three parts.** (i) *Financial statements:* a known uncorrected misstatement of $150,
10.3% of overall materiality, and six contracts that cannot be supported under ASC 606-10-25-1 because approval
by both parties is not evidenced. (ii) *Fraud:* date fields were edited after activation by a person with an
incentive, and the documented preventive control did not exist; intent is a legal conclusion you do not reach,
but the conditions suffice to treat the matter as suspected fraud for communication purposes. (iii) *Internal
control:* a material weakness, evaluated below. Then communicate under Exhibit 17-12, obtain a specific
representation, and document the AS 2810 reassessment.

## Extended Case Study: The December 2025 Backdating Scheme

### Background

Q4 2025 bookings were $61,400, of which $25,174 (41.0%) was signed December 24–31 against 27% a year earlier.
AtlasFlow paid its CRO on bookings and its CEO substantially in ARR-linked performance shares, and one person —
the VP Sales Operations — administered the system where revenue originates and could edit, after activation, the
two date fields that determine the period of recognition.

### The Facts

Four moving parts, none requiring an accounting entry.

1. **A January contract was papered as December.** Six order forms carry December signature dates, none has a
   DocuSign completion certificate, and all six were uploaded as scanned wet-ink PDFs. Nineteen of the 3,412
   FY2025 activations were wet-ink (0.6%); six of the nineteen fall in the final eight days of December.
2. **The date fields were edited after activation.** Field history shows Larkspur's `Contract_Start_Date__c`
   changed from January 1, 2026 to December 1, 2025 on December 30, plus signature-date edits on the Ridgeline,
   Copperline, and Marsh & Teller records. A post-activation edit does not push back to Zuora, so no interface
   exception surfaced it.
3. **The approval configuration was changed to clear the way.** On December 18 at 19:42 CT the same user moved the
   discount approval boundary from 40% to 45%, letting 21 order forms inside $4,180 of ACV activate without the
   CFO approval policy required.
4. **The tenants told a different story.** Kelso was provisioned January 9 and Ridgeline January 14, both
   inconsistent with the recorded start dates.

**Exhibit 17-14. The six contracts (in thousands).**

| Order form | Customer | ACV | Stated signature date | Recognition start | Days in FY2025 | FY2025 revenue | Post-activation edit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OF-2025-11842 | Larkspur Diagnostics | 660 | Dec 24, 2025 | Dec 1, 2025 | 31 | 56.1 | Yes — Dec 30 |
| OF-2025-11857 | Kelso Freight Systems | 480 | Dec 29, 2025 | Dec 8, 2025 | 24 | 31.6 | No; transmittal dated Jan 5 |
| OF-2025-11863 | Vantage Point Legal | 420 | Dec 30, 2025 | Dec 10, 2025 | 22 | 25.3 | No |
| OF-2025-11871 | Ridgeline Utilities | 360 | Dec 31, 2025 | Dec 12, 2025 | 20 | 19.7 | Yes — Jan 2 |
| OF-2025-11884 | Copperline Foods | 240 | Dec 26, 2025 | Dec 15, 2025 | 17 | 11.2 | Yes — Dec 31 |
| OF-2025-11890 | Marsh & Teller LLP | 180 | Dec 31, 2025 | Dec 20, 2025 | 12 | 5.9 | Yes — Jan 2 |
| **Total** | | **2,340** | | | | **149.8** | 4 of 6 |

### What the Engagement Team Did

Three of the fifteen steps produced the evidence: the unannounced January 6 examination, the full-year
field-history extract, and three-source date corroboration.

### Analysis

**Why the standard controls did not catch it.**

| Control relied on | Why it failed |
| --- | --- |
| FIN-REV-07 / OTC-05, the documented order-validation control | It does not exist as documented (Chapter 13). What Jordan Pike performed compared the billed service start date to the order-form date — two fields one person can set. A control comparing A to B where one person controls both is a tautology |
| Journal entry approval | No entry was made. The altered date flowed through Zuora into the routine monthly interface journal I-3, so the $250,000 second-approver threshold (W-12) was irrelevant |
| Electronic signature discipline | No control requires DocuSign. The wet-ink path suppressed the one piece of evidence outside management's control, and nothing flagged the 0.6% taking it |

**Can an immaterial amount indicate a material weakness?** Yes, and that is the analytical heart of the case.
Severity depends on the magnitude the deficiency *could* allow and the likelihood of occurrence, not on the
misstatement found.

**Exhibit 17-15. Potential magnitude of the revenue cut-off deficiency (in thousands).**

| Scenario | Population exposed | Days accelerated | Computation | Potential misstatement | Against materiality of $1,450 |
| --- | --- | --- | --- | --- | --- |
| Observed | 2,340 | 20.9 | 2,340 × 20.9 ÷ 365 | 134 | 9.2% |
| Reasonably possible — modest shift | 25,174 | 14 | 25,174 × 14 ÷ 365 | 965 | 66.6% |
| Reasonably possible — the observed average | 25,174 | 20 | 25,174 × 20 ÷ 365 | 1,379 | 95.1% |
| Reasonably possible — one month | 25,174 | 30 | 25,174 × 30 ÷ 365 | 2,069 | 142.7% |

The deficiency is a material weakness on three grounds. **Magnitude:** the gap governs $25,174 of December ACV,
and an average acceleration of 21.0 days ($1,450 × 365 ÷ 25,174) reaches overall materiality. **Likelihood:** 41
edits occurred, 9 in final weeks, and nothing detected them, because the only control designed to do so did not
exist. **The AS 2201 indicator:** fraud on the part of senior management, material or not, indicates a material
weakness, and whether a VP of Sales Operations is "senior management" is a judgment. The team treated the
indicator as informing but not determining a conclusion resting on magnitude and likelihood. What would move
it: had the six contracts carried customer-domain transmittals and had all edits moved dates later, observed
magnitude would be near zero and a significant deficiency arguable.

### Resolution and Conclusion

Management declined to reverse the six contracts, asserting the deals were agreed in December and the
documentation is a formality. The team's position was that the assertion is unauditable: no evidence
distinguishes a contract agreed and signed in December from one agreed in December and signed in January. The
$150 was accumulated as U-3 and evaluated in Chapter 19 with the other five uncorrected items ($(460)
aggregate). Aggregated with the Chapter 13 finding, the deficiency was concluded to be a **material weakness
relating to revenue cut-off**, graded in Chapter 14 and reported in Chapter 20. The audit committee commissioned
an investigation through counsel on January 16, 2026; management removed the administrator's edit access,
restored the discount thresholds, and required DocuSign from February 1, 2026. Because remedial action was taken,
no Section 10A(b) escalation arose. The representation letter added a representation on the completeness of
contract documentation and the absence of undisclosed side agreements.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                     WP 3200-14
AtlasFlow, Inc. — FY2025 (period ended 12/31/2025)                  Page 1 of 4

MEMORANDUM — INVESTIGATION OF WHISTLEBLOWER ALLEGATION REGARDING
DECEMBER 2025 CONTRACT EXECUTION DATES

Prepared by:  G. R. Lindqvist (GRL), Senior Manager             02/02/2026
Assisted by:  T. Iyer (TI), Data & Analytics          01/16 – 01/28/2026
              B. Osei (BO), IT Audit Senior           01/16 – 01/22/2026
Reviewed by:  D. Whitcombe (DW), Engagement Partner             02/04/2026
              L. Herrera (LH), EQR — briefed 01/15/2026         02/06/2026

PURPOSE
To investigate an allegation received by the audit committee on 01/14/2026 that
December 2025 contracts were "papered after the fact," to determine the effect on
the FY2025 financial statements, and to evaluate the effect on the fraud risk
assessment and the ICFR conclusion.

SOURCE OF INFORMATION
(1) Allegation email with headers, provided 01/14/2026 by counsel to the audit
    committee chair; not obtained from management.
(2) Salesforce Opportunity_Field_History extract of all FY2025 post-activation
    edits to Contract_Signed_Date__c and Service_Start_Date__c; read-only extract
    taken by BO on 01/16/2026 (41 records).
(3) Salesforce Setup Audit Trail, 01/2025 – 01/2026; DocuSign envelope inventory
    and completion certificates; platform tenant-creation log (read-only).
(4) Bookings report; RevPro contract population; WP 3100-09.

PROCEDURES PERFORMED
1. Reconvened the team fraud discussion 01/15/2026 and briefed the EQR (WP 2100-01,
   continuation entry). Notified the audit committee chair 01/15/2026 and
   management 01/16/2026 (AS 1301 communication at WP 5100-03).
2. Defined and proved three populations: P1 (118 order forms, ACV $25,174, signed
   12/24–12/31/25), P2 (12/01–12/23 activations), P3 (41 post-activation edits).
   P1 reconciled to the bookings report and the RevPro population. (b)
3. Tested P1 stratum A at 100% (43 items, ACV $19,240) on 01/06/2026, unannounced,
   and stratum B by attribute sample (14 of 75), using three external sources per
   item: DocuSign completion certificate, tenant-creation timestamp, and customer-
   domain transmittal. (a) (c)
4. Analyzed all 41 records in P3 by direction, timing, and editing user; traced the
   12/18/2025 19:42 CT AP-CPQ-01 change to the 23 order forms activated 12/18–12/31
   with discounts of 40.01%–45.00%, ACV $4,180. (a)
5. Interviewed two sales representatives and a Deal Desk analyst (auditor-selected),
   then J. Pike, D. Kim, B. Hallowell, S. Marchetti; notes at WP 3200-14.3.
6. Tested adjacent populations: January 2026 credits for FY2025 service ($61);
   December reseller activations without a provisioned tenant (none); commissions
   accrued on the six contracts ($210, not reversed).

RESULTS
- 41 post-activation date edits; 26 moved dates earlier; 9 fell in the final week
  of a quarter, all moving dates earlier, 7 by user bhallowell. (e)
- Six order forms (ACV $2,340) carry December signature dates with no DocuSign
  certificate and no customer-domain transmittal; four also show a post-activation
  edit. Revenue effect $149.8, recomputed (b), carried at $150 as U-3.
- 21 of the 23 order forms in the 40.01%–45.00% band activated without the CFO
  approval required by policy before the 12/18 change. (e)
- Management declined to reverse the six contracts; position recorded verbatim.

CONCLUSION
The allegation is substantiated in its factual particulars. A known, uncorrected
misstatement of $150 exists (U-3), and $2,340 of ARR, $2,100 of receivables and
deferred revenue, and $210 of capitalized commissions rest on the same
uncorroborated evidence. The matter is treated as suspected fraud for AS 2401 and
AS 1301 purposes; no conclusion is reached on intent. The related deficiency,
aggregated with the WP 3100-09 finding that FIN-REV-07 does not exist, is a
MATERIAL WEAKNESS in ICFR relating to revenue cut-off (severity at WP 4200-01).
The fraud risk assessment was updated (WP 2100-03, F-1 rev. 2) and no reliance is
placed on any order-to-cash control.

TICK MARK LEGEND
(a) Agreed to a source outside management's control.  (b) Recomputed.
(c) Confirmed with a third party.  (e) Exception noted; see Results.
```

### Lessons

1. A control comparing two fields the same person can edit provides no evidence, however faithfully performed.
2. The last step of a fraud is not always a journal entry. Design at least one procedure per significant fraud
   risk that reaches the *input*.
3. Capability alone is a design observation; capability plus incentive plus 41 observed acts is a finding. Know
   which you have.
4. Materiality governs the misstatement and severity governs the deficiency; the two can diverge by an order of
   magnitude.
5. The most valuable procedure in the file cost one query and covered the whole year: full-population evidence
   from an immutable log beats a larger sample of client-assembled documents.

## Common Mistakes

### Mistake 17.1 — The brainstorming session as ceremony

**What it looks like.** A 20-minute meeting whose minutes list last year's three fraud risks, held after the risk
assessment was drafted.
**Why it happens.** It is scheduled to satisfy a documentation requirement, and the people who know the systems
are not in the room.
**What goes wrong.** Fraud risks end up at account level, no scheme-specific procedure is designed, and this
year's new schemes are never identified.
**How to avoid it.** Hold it before the register is drafted, require each attendee to propose a scheme and its
concealment step, and record the schemes rejected.

### Mistake 17.2 — A fraud risk with no actor, system, or verb

**What it looks like.** "Fraud risk: revenue recognition. Response: perform revenue testing."
**Why it happens.** Teams copy the standard's language into the register.
**What goes wrong.** The response cannot be evaluated for sufficiency, because the risk has no mechanism, so
vouching invoices appears responsive.
**How to avoid it.** Require every entry to read "person in role X does Y in system Z, affecting assertion A."
If that sentence cannot be written, the risk has not been identified.

### Mistake 17.3 — Testing management with a population management assembled

**What it looks like.** A December order-form folder prepared by Sales Operations, or an "unusual entries"
listing filtered by the Controller.
**Why it happens.** It is faster, and the client offers.
**What goes wrong.** If the risk is that a person altered records, a population that person can filter proves
nothing, whatever the sample size.
**How to avoid it.** Take the population from an immutable log or a read-only extract obtained under your
observation, and reconcile it to an independent total before sampling.

### Mistake 17.4 — Unpredictability implemented as a bigger sample

**What it looks like.** "Element of unpredictability: sample increased from 25 to 30 items."
**Why it happens.** Unpredictability is confused with extent, the easiest dial to turn.
**What goes wrong.** Nothing about the client's expectations changes, so whoever knows which accounts and
periods get tested still knows.
**How to avoid it.** Change the timing, the population, the interviewee, or the account tested, as in
Exhibit 17-10.

### Mistake 17.5 — "The amount is immaterial, so there is nothing to report"

**What it looks like.** A $150 misstatement logged on the summary of audit differences with no severity
evaluation and no fraud communication.
**Why it happens.** Materiality is applied to a question it does not answer.
**What goes wrong.** Severity turns on potential magnitude and likelihood, and fraud by senior management is an
ICFR indicator regardless of amount, so the team misses both a material weakness and a communication.
**How to avoid it.** For any possibly intentional misstatement, run three separate analyses: quantitative
effect, deficiency severity, and communication obligation.

### Mistake 17.6 — Tautological corroboration

**What it looks like.** Agreeing the revenue start date in RevPro to the start date on the order form and
concluding that cut-off is supported.
**Why it happens.** The two documents agree, and agreement feels like evidence.
**What goes wrong.** Both fields sit inside the client's systems and one person can edit both; consistency between
two representations by the same party is not corroboration.
**How to avoid it.** For every date and quantity driving recognition, name one evidence source outside
management's control and test against that.

### Mistake 17.7 — Fraud inquiries confined to the finance function

**What it looks like.** Inquiry memoranda covering the CFO, Controller, and revenue accountants, and nobody
else.
**Why it happens.** Those are the contacts the team already has.
**What goes wrong.** The people who know how a quarter actually closes are never asked, and the most probative
answers are never obtained.
**How to avoid it.** Select at least three interviewees outside financial reporting yourself, from a system user
list rather than a list management provides, and ask process questions rather than fraud questions.

### Mistake 17.8 — Confusing your responsibility for ARR with your responsibility for RPO

**What it looks like.** Either auditing ARR as though it were a financial statement caption, or ignoring a
mid-year change in the retention definition because "it is not GAAP."
**Why it happens.** Operating metrics sit in the same document as the audited statements.
**What goes wrong.** The first implies assurance you have not obtained; the second discards a first-order fraud
risk factor and fails the other-information requirement.
**How to avoid it.** Recompute and audit RPO as a disclosure; read ARR and retention under AS 2710 / AU-C 720
for material inconsistency; record any definitional change as a fraud risk factor.

### Mistake 17.9 — Adopting management's investigation as your evidence

**What it looks like.** A workpaper concluding "counsel's investigation found no intentional misconduct; no
further procedures performed."
**Why it happens.** The investigation is better resourced and reaches a comfortable conclusion.
**What goes wrong.** Someone else set the scope, possibly to avoid your question, and the report is a
representation rather than audit evidence.
**How to avoid it.** Read the report, interview the investigators, obtain the underlying documents, perform your
own procedures on populations you defined, and record what the investigation did not cover.

### Mistake 17.10 — Communicating late, or to the wrong person first

**What it looks like.** A fraud matter identified in January and first communicated in the February audit
committee package, after management was consulted on how to present it.
**Why it happens.** Teams want a complete answer before raising an incomplete one.
**What goes wrong.** Timing must permit the committee to act; telling management first can compromise evidence
and, where senior management may be involved, misroutes a required communication.
**How to avoid it.** Communicate the allegation and your plan to the committee chair within one business day,
document the sequencing decision, and deliver the written communication before the report is issued.

## Practice Exercises

### Exercise 17-1

[Foundational] Five order forms activated at December 31, 2025 have signature dates the team could not
corroborate. Compute the FY2025 revenue effect of each and in total (365-day year, straight-line, in
thousands), and express the total as a percentage of overall materiality of $1,450.

| Order form | ACV | Recognition start | Days in FY2025 |
| --- | --- | --- | --- |
| A | 900 | Dec 20, 2025 | 12 |
| B | 600 | Dec 15, 2025 | 17 |
| C | 480 | Dec 10, 2025 | 22 |
| D | 300 | Dec 1, 2025 | 31 |
| E | 240 | Dec 24, 2025 | 8 |

### Exercise 17-2

[Foundational] For each scheme state whether it is fraudulent financial reporting or misappropriation of assets
and name the primary relevant assertion: (a) a side letter granting an undisclosed refund right; (b) duplicate
expense reimbursements by a sales director; (c) reducing a customer's committed run volume to create overage;
(d) releasing $200 of allowance for credit losses with no change in the aging; (e) recoding support engineers
from cost of subscription to research and development; (f) recording a January contract with a December
signature date.

### Exercise 17-3

[Intermediate] The 2025 tranche of the CEO's ARR-based PSUs is 240 thousand units at a grant-date fair value of
$34.10. Payout is linear from 0% of target at ARR of $160.0M to 100% at $174.0M. Reported ARR is $172.0M.
Compute (a) the payout percentage; (b) the marginal payout per $1.0M of ARR; (c) units earned and their
grant-date value; (d) the change in (c) if $2.34M of ARR from uncorroborated December contracts is excluded.

### Exercise 17-4

[Intermediate] Write three unpredictability elements for the FY2026 audit, 40 to 60 words each, each naming the
procedure, the population or person, the timing, and why the client cannot anticipate it. None may be a change
in sample size, and none may repeat an element from Exhibit 17-10.

### Exercise 17-5

[Intermediate] The following post-activation date edits were returned for Q2 2025, which ended June 30. Identify
which warrant follow-up, state the follow-up procedure, and compute the aggregate revenue acceleration for those
that do (365-day year, in thousands), using the days between the old and new values of the edited field.

| # | Field | Old value | New value | User | Edit date | ACV |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `Service_Start_Date__c` | Jul 1, 2025 | Jun 1, 2025 | bhallowell | Jun 30, 2025 | 480 |
| 2 | `Contract_Signed_Date__c` | May 14, 2025 | May 4, 2025 | dealdesk2 | May 16, 2025 | 120 |
| 3 | `Service_Start_Date__c` | Jun 1, 2025 | Jul 1, 2025 | dealdesk1 | Jun 12, 2025 | 240 |
| 4 | `Contract_Signed_Date__c` | Jul 2, 2025 | Jun 30, 2025 | bhallowell | Jul 3, 2025 | 360 |
| 5 | `Service_Start_Date__c` | Jun 15, 2025 | Jun 15, 2025 | jpike | Jun 20, 2025 | 180 |
| 6 | `Service_Start_Date__c` | Jul 15, 2025 | Jun 20, 2025 | bhallowell | Jun 30, 2025 | 600 |

### Exercise 17-6

[Advanced] Spanning Chapters 13 and 17: FIN-REV-07 / OTC-05 does not exist as documented, leaving December
cut-off unaddressed for FY2025, and December 24–31 activations totaled $25,174 of ACV. Compute the potential
revenue misstatement at average accelerations of 10, 21, and 35 days; identify the days at which potential
magnitude equals overall materiality of $1,450; conclude on severity; and state one fact that would move your
conclusion in each direction.

### Exercise 17-7

[Intermediate] Find and correct every defect in this fraud risk register extract. There are five.

| Ref | Risk | Assessed risk | Response |
| --- | --- | --- | --- |
| F-A | Revenue recognition | High | Increase the revenue sample from 40 to 55 items |
| F-B | Error in the cut-off of December contracts | High | Test cut-off |
| F-C | Presumed revenue fraud risk — rebutted because the order-validation control is effective | n/a | None |
| F-D | Misappropriation of assets — not applicable; the company holds no inventory | n/a | None |
| F-E | Management override | Blended risk assessed as moderate after considering controls | Journal entry testing |

### Exercise 17-8

[Advanced] Draft the paragraph of the AS 1301 written communication to the audit committee reporting the
suspected fraud and the uncorrected misstatement, 150 to 180 words. It must state what was found, the amount and
its relationship to materiality, the auditor's position on intent, the control consequence, and what you ask of
the committee.

### Exercise 17-9

[Intermediate] Draft four fraud inquiry questions for Sofia Marchetti, Chief Revenue Officer. Each must be
answerable with a fact rather than a characterization, and for each state the answer that would raise your
assessed risk and the document you would request to corroborate it.

### Exercise 17-10

[Advanced] The self-serve channel is $6,100 of revenue across 11,400 accounts, billed monthly to credit cards at
list price with no negotiation and summarized into NetSuite by an in-house Lambda job with two undocumented
FY2025 changes (W-7). A staff auditor proposes rebutting the presumed fraud risk for this stream. Evaluate the
proposal, state your conclusion, and specify the fraud risk you would record if the presumption stands.

### Exercise 17-11

[Advanced] In whole dollars: usage overage revenue was $1,090,000 in Q3 2025 and $1,390,000 in Q4 2025 at $12 per
1,000 workflow runs. Total platform runs were 5,420 million in Q3 and 5,610 million in Q4. Compute billable
overage runs each quarter, the growth rate of each measure, and billable overage as a percentage of total runs.
State whether the result is expected and name two procedures that would distinguish growth from manipulation.

### Exercise 17-12

[Advanced] AtlasFlow computes net revenue retention as current-period ARR from the prior-year cohort divided by
prior-year cohort ARR. The FY2025 cohort began at $137.4M and ended at $148.4M. In November 2025 management
changed the definition to exclude from the denominator churned customers with beginning ARR below $10 thousand —
$4.7M of beginning ARR. Compute retention under both definitions, state whether the change misstates the
financial statements, and state your responsibility.

## Solutions to Practice Exercises

### Solution 17-1

A: 900 × 12 ÷ 365 = 29.6. B: 600 × 17 ÷ 365 = 27.9. C: 480 × 22 ÷ 365 = 28.9. D: 300 × 31 ÷ 365 = 25.5.
E: 240 × 8 ÷ 365 = 5.3. Total 29.6 + 27.9 + 28.9 + 25.5 + 5.3 = **$117**, or 117 ÷ 1,450 = **8.1%** of overall
materiality. What the computation misses: $2,520 of ACV and ARR, and the related receivables, deferred revenue, and
RPO.

### Solution 17-2

(a) Fraudulent financial reporting; accuracy of the transaction price. (b) Misappropriation; occurrence.
(c) Fraudulent financial reporting; accuracy. (d) Fraudulent financial reporting; valuation.
(e) Fraudulent financial reporting; classification. (f) Fraudulent financial reporting; cut-off and occurrence.

### Solution 17-3

(a) (172.0 − 160.0) ÷ (174.0 − 160.0) = 12.0 ÷ 14.0 = **85.7%**. (b) 100% ÷ 14.0 = **7.14 pp per $1.0M**.
(c) 240 × 0.857 = **205.7 thousand units**; × $34.10 = **$7,014**. (d) ARR of $169.66M gives
(169.66 − 160.0) ÷ 14.0 = 69.0%; 240 × 0.690 = 165.6 units; × $34.10 = $5,647; difference **$1,367** (the $1,364
in §17.2 is the same figure from the rounded sensitivity). So $150 of revenue moves about $1,367 of executive
equity value.

### Solution 17-4

Model elements. (i) "On the last business day of Q1 2026, before the close is complete, take a read-only extract
of all Zuora Revenue modifications processed in the preceding 10 days and reconcile each to an executed
amendment — the client expects year-end testing from a schedule it prepares, so a mid-close extract removes both
the timing and the preparer." (ii) "Select three implementation consultants from the Okta user list and ask each
for the go-live date of their last two projects; compare to the RevPro revenue start dates. Management cannot
anticipate which consultants." (iii) "Test 25 credit memos in account 2230 issued in the first 45 days of FY2026 —
an account below performance materiality never previously tested — for concessions granted after the period."

### Solution 17-5

Follow up on every edit that moved a recognition-relevant date **earlier**: items 1, 2, 4, and 6. Item 3 moved a
date later, consistent with correcting an error, and needs only corroboration to the executed document; item 5
shows no net change. Acceleration: #1 480 × 30 ÷ 365 = 39.5; #2 120 × 10 ÷ 365 = 3.3; #4 360 × 2 ÷ 365 = 2.0;
#6 600 × 25 ÷ 365 = 41.1; total **$85.9, or $86**. Item 4 is the most serious despite the smallest day count: a
two-day move carrying a contract across the quarter boundary, made by the administrator the day after quarter end.
Follow-up for each: obtain the DocuSign completion certificate, the tenant-creation timestamp, and a
customer-domain transmittal.

### Solution 17-6

10 days: 25,174 × 10 ÷ 365 = **$690**. 21 days: **$1,448**. 35 days: **$2,414**. Materiality is reached at
1,450 × 365 ÷ 25,174 = **21.0 days**. Conclusion: **material weakness**, because a reasonably possible 21-day
average acceleration across a population no other control covered equals overall materiality, and because a
missing control has no compensating control. Toward significant deficiency: evidence that an independent control —
a monthly comparison of RevPro start dates to tenant-provisioning timestamps outside sales — operated all year.
Toward a firmer material weakness: comparable edits in earlier quarters.

### Solution 17-7

(1) F-A states the risk at caption level with no scheme, actor, or assertion, and answers it with a sample-size
increase, which is neither responsive nor fraud-specific. (2) F-B calls the risk an "error," the opposite of a
fraud risk, and names no evidence source outside management's control. (3) F-C rebuts the presumption on control
effectiveness; controls respond to risk and never establish that the risk does not exist — and here the cited
control does not exist. (4) F-D dismisses misappropriation for want of inventory, when cash, purchase cards, and
reimbursements are all susceptible. (5) F-E blends inherent and control risk into one assessment recorded net of
controls, contrary to the separate-assessment requirement.

### Solution 17-8

Model paragraph (152 words): "In January 2026 the committee received an allegation that December 2025 contracts
had been executed after year end. We investigated independently of management's counsel. We identified 41
post-activation edits to contract signature or service start dates in FY2025, of which nine occurred in the final
week of a fiscal quarter; all nine moved the date earlier and seven were made by the administrator of Salesforce
CPQ. Six December order forms with aggregate annual contract value of $2,340 have no evidence of execution date
from any source outside the Company's control. The revenue effect is $150, or 10.3% of overall materiality of
$1,450; management has declined to correct it. We are required to report this matter to you as a suspected fraud,
and we express no conclusion on intent. The related control deficiency, aggregated with the absence of the
documented order-validation control, is a material weakness relating to revenue cut-off. We ask the committee to
advise us of remedial action taken."

### Solution 17-9

Model questions, each with the concerning answer and the corroborating document. (1) "What did you communicate to
the sales organization about December 31, in writing?" — a verbal-only answer; request the Slack and email
traffic. (2) "What was the FY2025 bookings plan and where did reported bookings land against it?" — a figure
within 3% of plan; request the compensation plan and commission calculation. (3) "Who may approve a discount above
40%, and did that change in December?" — an answer omitting the December 18 configuration change; request the
Setup Audit Trail. (4) "Has any customer asked for a concession not on the order form?" — "never"; request the
January credit memo listing and the customer-success ticket queue.

### Solution 17-10

Reject the proposal, but reframe it. Two conditions in Exhibit 17-6 largely hold: recognition follows a card
charge, and no individual incentive attaches. What defeats rebuttal is that a person outside
accounting can alter the revenue-bearing record — the Stripe-to-NetSuite summarization job is in-house code with
two undocumented FY2025 changes and no effective ITGC over it. Record the risk as: "a developer modifies the
Lambda summarization job so that gross charges, refunds, or chargebacks summarize incorrectly into accounts 4100
and 1205, affecting accuracy." Respond by recomputing the daily summary from the Stripe settlement file for
selected days and reconciling full-period Stripe charges, refunds, and payouts to recorded revenue and cash. A
defensible alternative identifies the fraud risk for enterprise revenue only; that is weaker, because the code
weakness is unremediated and the stream is more than four times overall materiality.

### Solution 17-11

Q3 billable overage runs: $1,090,000 ÷ $12 × 1,000 = **90,833,333**. Q4: $1,390,000 ÷ $12 × 1,000 =
**115,833,333**. Growth in billable overage runs: 115,833,333 ÷ 90,833,333 − 1 = **+27.5%**. Growth in total
runs: 5,610 ÷ 5,420 − 1 = **+3.5%**. Billable overage as a percentage of total runs: 90.8 ÷ 5,420 = **1.68%**
in Q3 and 115.8 ÷ 5,610 = **2.06%** in Q4. Not expected: billable overage grew nearly eight times as fast as the
volume generating it, so the change lies in the classification of runs as billable rather than in consumption. Two
procedures: (i) for 12 accounts, obtain committed volumes from executed order forms and raw run counts from the
platform database, recompute overage, and agree to the invoice; (ii) test every downward edit to the
committed-volume field to an executed amendment.

### Solution 17-12

Original: 148.4 ÷ 137.4 = **108.0%**. Revised: 148.4 ÷ (137.4 − 4.7) = 148.4 ÷ 132.7 = **111.8%**, reported as
112%. The change adds 3.8 percentage points with no change in economics, and it is **not** a misstatement of the
financial statements, because retention is not a GAAP measure and does not appear in them. Your responsibility
runs three ways. As other information under AS 2710 / AU-C 720, read the disclosure and consider whether it is
materially inconsistent with the statements or with knowledge obtained in the audit, and whether the change and its
effect are disclosed; an undisclosed change presented as a comparable metric is an inconsistency to pursue with
management and, unresolved, with the committee. Treat it as a fraud risk factor and reassess whether that attitude
reached revenue and the estimates. Communicate it under AS 1301 as a matter bearing on the quality of financial
reporting. What you do not do is audit the metric.

## Review Questions

**RQ 17-1.** State the three limits on the auditor's responsibility for detecting fraud.

**RQ 17-2.** How does management's responsibility for fraud differ from the audit committee's?

**RQ 17-3.** Name the three legs of the fraud triangle and give one AtlasFlow example of each.

**RQ 17-4.** What must the documentation of the engagement team fraud discussion contain?

**RQ 17-5.** Why are inquiries of personnel outside the financial reporting function more probative than
inquiries of the CFO?

**RQ 17-6.** What is the presumption regarding revenue recognition, and what would rebutting it require?

**RQ 17-7.** Name the three responses required regardless of the assessed level of fraud risk.

**RQ 17-8.** Why did journal entry testing fail to detect the AtlasFlow backdating scheme?

**RQ 17-9.** Give two examples of unpredictability that are not changes in sample size.

**RQ 17-10.** Distinguish fraudulent financial reporting from misappropriation of assets, and explain why an
immaterial misappropriation can still matter to your report.

**RQ 17-11.** What is a side letter, and what confirmation question detects one?

**RQ 17-12.** How does the auditor's responsibility for RPO differ from its responsibility for ARR and
retention metrics?

**RQ 17-13.** When must fraud be communicated to the audit committee even though the amount is immaterial?

**RQ 17-14.** What is the escalation path under Exchange Act Section 10A(b), and what triggers each step?

**RQ 17-15.** What does a retrospective review of estimates test, and why must it be performed in both
directions?

## Answers to Review Questions

**RQ 17-1.** Reasonable rather than absolute assurance, because concealment, collusion, and management override
defeat well-designed procedures; materiality, because the audit is directed at material misstatement; and the
greater difficulty of detecting fraud than error. None of the three excuses failing to design procedures
responsive to identified fraud risks.

**RQ 17-2.** Management designs and maintains the controls that prevent and detect fraud, sets the tone, and
investigates allegations. The audit committee oversees that process, maintains the Rule 10A-3 complaint
procedures, and oversees investigations that may involve management. The auditor tests rather than adopts both.

**RQ 17-3.** Incentive: the CEO's ARR-based PSUs, worth 7.14 percentage points of payout per $1.0M of ARR.
Opportunity: the VP Sales Operations can edit order-form dates after activation, and the documented
order-validation control does not exist. Rationalization: management's position that the December dates are a
documentation issue rather than an accounting issue.

**RQ 17-4.** Who participated, when it occurred, what was discussed, and the conclusions reached, including the
fraud risks identified and how they link to planned responses. Good practice adds who was absent and why, the
schemes rejected, and any continuation of the discussion later in the audit.

**RQ 17-5.** Their incentives differ and they are usually unaware that a process question is a fraud inquiry. A
sales representative's statement that a slipped deal "counts next quarter — sometimes the date gets fixed" is
evidence a CFO would never volunteer, and it is testable.

**RQ 17-6.** You must presume a risk of material misstatement due to fraud relating to revenue recognition.
Rebutting it requires documented reasons why improper revenue recognition is not a fraud risk — that recognition
depends on no manipulable date or estimate, that no incentive attaches to the reported amount, and that nobody
outside accounting can alter a revenue record. In SaaS those conditions do not hold together.

**RQ 17-7.** Testing journal entries and other adjustments for evidence of material misstatement; reviewing
accounting estimates for bias, including a retrospective review of prior-period estimates; and evaluating the
business rationale for significant unusual transactions.

**RQ 17-8.** The scheme required no journal entry. The altered date flowed through Zuora into the routine monthly
interface journal, indistinguishable from the other eleven. Journal entry testing reaches schemes that end in an
entry, not schemes that end in a field.

**RQ 17-9.** The unannounced January 6 examination of the December 24–31 order-form population, before the close
was complete; and the extract of all FY2025 post-activation date edits rather than a December sample, which
produced 41 records and 9 final-week edits.

**RQ 17-10.** Fraudulent financial reporting is intentional misstatement or omission in the financial statements;
misappropriation is theft of the entity's assets, usually with false records to conceal it. An immaterial
misappropriation matters because fraud by a person with authority indicates a material weakness under AS 2201,
bears on the reliability of representations, and must be communicated.

**RQ 17-11.** A separate undisclosed agreement granting a right the order form does not reflect — a refund,
termination right, extended acceptance, or contingent concession. The detecting procedure is a terms confirmation
asking whether any agreements, understandings, or amendments exist other than those listed, rather than a balance
confirmation, which returns "agreed" because the receivable is owed.

**RQ 17-12.** RPO is a financial statement disclosure under ASC 606 and is audited: you recompute it from the
contract population and test the enforceable-term judgments. ARR and retention are not GAAP measures and are other
information under AS 2710 / AU-C 720: you read them, consider material inconsistency, and respond if inconsistent.

**RQ 17-13.** When the fraud involves senior management, regardless of amount: the AS 2201 material weakness
indicator and the AS 1301 communication requirement both operate without a dollar threshold.

**RQ 17-14.** On detecting a likely illegal act, inform the appropriate level of management and be satisfied the
audit committee is adequately informed. If management does not take timely remedial action and the effect is
material, report to the board; the board must notify the Commission within one business day, and if it does not,
the auditor furnishes its report to the Commission or resigns.

**RQ 17-15.** It tests whether prior-period estimates, measured against known outcomes, reveal a pattern of
management bias. Both directions are necessary because one income-favorable difference is noise while a pattern is
evidence, and identifying conservative estimates alongside aggressive ones makes the conclusion credible.

## Key Definitions

**Annual recurring revenue (ARR).** The annualized value of committed subscription contracts in force at a
point in time. Not a GAAP measure; when disclosed in a document containing audited financial statements it is
other information under AS 2710 / AU-C 720.

**Backdating.** Altering a document date so a transaction appears to have occurred in an earlier period. In
SaaS the altered field is a signature or service start date, and the misstatement propagates through the
subledgers without a journal entry.

**Channel stuffing.** Inducing a reseller to accept more subscription volume than end-customer demand supports,
often with informal return rights, to accelerate reported revenue and bookings.

**Cookie-jar reserve.** An allowance or accrual established above the supportable range in a strong period and
released to earnings in a weak one. Detectable only across periods, because each period's balance is
individually defensible.

**Engagement team fraud discussion.** The required discussion among key engagement team members about how and
where the statements might be susceptible to fraud, including how assets could be misappropriated. It must occur,
be documented, and continue as the audit progresses (AS 2401; AS 2110; AU-C 240).

**Fraud.** An intentional act resulting in a material misstatement of the financial statements. Intent
distinguishes it from error; the auditor addresses the misstatement and makes no legal determination of intent.

**Fraud risk factor.** An event or condition indicating an incentive or pressure to commit fraud, an opportunity
to do so, or an attitude that justifies it. Presence does not indicate fraud; absence does not indicate its
absence.

**Fraud triangle.** The three conditions generally present when fraud occurs: incentive or pressure, opportunity,
and rationalization or attitude. Useful only when each leg is expressed in the entity's own quantities.

**Fraudulent financial reporting.** Intentional misstatement or omission of amounts or disclosures designed to
deceive users, including manipulation of records and intentional misapplication of accounting principles.

**Management override of controls.** Management's ability to circumvent controls that otherwise appear to operate
effectively, by directing subordinates, posting entries outside the process, or changing system configuration. The
reason certain procedures are required regardless of assessed risk.

**Misappropriation of assets.** Theft of an entity's assets, often with false records to conceal the loss;
includes embezzlement, expense reimbursement and purchase-card schemes, and payments for goods not received.

**Presumed fraud risk in revenue recognition.** The requirement to presume a risk of material misstatement due to
fraud relating to revenue recognition, and to document the reasons if that presumption does not result in an
identified fraud risk (AS 2401; AU-C 240).

**Professional skepticism.** A questioning mind and a critical assessment of evidence, operationalized as asking
questions with factual answers, placing answers in a population, refusing characterizations offered in place of
evidence, and specifying in advance what would change the conclusion.

**Reciprocal arrangement.** Two contemporaneous transactions between the same parties in opposite directions,
economically neutral in combination but inflating revenue and expense. Also called round-tripping.

**Related-party transaction.** A transaction with a party that can control or significantly influence the entity,
or is controlled or influenced by it or by a common party. Requires identification, evaluation of business
purpose, and disclosure; specific materiality is often set below overall materiality (AS 2410; AU-C 550).

**Retrospective review of estimates.** A required look back at significant prior-period estimates against
subsequently known outcomes, performed to detect a pattern of management bias rather than a prior-period
misstatement.

**Side letter.** A separate agreement, often by email, modifying rights and obligations in the executed contract
without appearing in the contract repository or the billing system. It affects both transaction price and
performance obligations.

**Significant unusual transaction.** A significant transaction outside the normal course of business, or one that
appears unusual given its timing, size, or nature. The auditor must evaluate its business rationale and whether
its form appears designed to obscure its substance.

**Unpredictability.** A required element in selecting procedures whereby the nature, timing, or extent cannot be
anticipated by the entity. Changing sample sizes does not satisfy it; changing timing, population, interviewee, or
account tested can.

**Whistleblower complaint procedures.** The procedures a listed issuer's audit committee must establish for the
receipt, retention, and treatment of complaints regarding accounting, internal accounting controls, and auditing
matters, including confidential anonymous employee submission (Exchange Act Rule 10A-3).

## Chapter Summary

1. The auditor's responsibility is reasonable assurance that the statements are free of material misstatement
   whether caused by error or fraud, subject to three limits: reasonable rather than absolute assurance,
   materiality, and the inherent difficulty of detecting intentional concealment.
2. A fraud risk assessment written in adjectives generates no procedures; one written in the client's
   quantities does. At AtlasFlow $1.0M of ARR is worth 7.14 percentage points of the CEO's PSU payout, so six
   contracts producing $150 of revenue move about $1,364 of executive equity value.
3. Fraud inquiries become evidence when directed at people whose incentives differ from management's, and
   recorded verbatim.
4. The presumed fraud risk in revenue recognition is not rebuttable in SaaS, because recognition depends on dates
   and estimates that incentivized people can set. The useful work is specifying the risk to a scheme, an actor, a
   system, and an assertion.
5. Analytics have no power against a scheme worth 0.37% of quarterly revenue, so say in the workpaper which
   fraud risks your analytics cannot reach and respond to those with tests of details.
6. The three required responses are necessary but not sufficient: a scheme that alters an input never touches a
   journal entry, which is why the AtlasFlow backdating survived a complete journal entry test.
7. Unpredictability means the client cannot anticipate what you will do — unannounced timing before the close is
   complete, full-year immutable-log populations, auditor-selected interviewees, and accounts below performance
   materiality.
8. A control comparing two fields the same person can edit is a tautology; the documented order-validation
   control here was both nonexistent and, as performed, tautological.
9. Materiality governs the misstatement and severity governs the deficiency: $150 coexists with a material
   weakness because the gap exposed $25,174 of December ACV and a 21.0-day average acceleration would equal
   overall materiality.
10. Operating metric manipulation may be no GAAP misstatement at all, in which case your responsibility runs
    through the other-information requirements, the fraud risk assessment, and the committee communication
    rather than through the opinion.
11. When an allegation arrives, the audit committee is the first external recipient, populations must come from
    sources the subject cannot filter, and management's investigation directs your work rather than supplying
    your evidence.
12. Professional skepticism is diagnosable in a transcript: a factual question, an answer placed in a
    population, a refusal of the offered frame, and a statement in advance of what would change the conclusion.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Risk assessment, the risk matrix, inherent versus control risk | Chapter 2 | The register in §17.4 extends the FY2025 risk assessment matrix |
| Materiality and the $150 specific materiality | Chapter 3 | The thresholds against which U-3 is measured |
| The December cut-off test of details and the six contracts | Chapter 4, §4.9 | The execution detail behind walkthrough steps 9 through 11 |
| Standalone selling price, deferred revenue modifications, CECL | Chapters 5, 6, 7 | The subject matter behind fraud risks F-5 and F-6 |
| ITGCs, access, and the December 18 CPQ configuration change | Chapters 11 and 12 | Why the opportunity leg is as wide as it is |
| The FIN-REV-07 / OTC-05 phantom control | Chapter 13 | Why no control detected the scheme |
| Deficiency severity and material weakness grading | Chapter 14 | Where the severity conclusion is graded |
| Journal entry testing mechanics | Chapter 16 | The required response this chapter mandates but does not perform |
| Analytics precision and expectation-setting | Chapter 18 | Why the deferred revenue bridge lacks power here |
| Evaluating misstatements for fraud indicators | Chapter 19 | Where U-3 and the $(460) aggregate are evaluated |
| The adverse ICFR opinion | Chapter 20 | How the revenue cut-off material weakness is reported |

## Further Reading

- PCAOB AS 2401, *Consideration of Fraud in a Financial Statement Audit*, including its appendices on fraud
  risk factors and examples of responses to assessed fraud risks.
- PCAOB AS 2110, AS 2301, AS 2405, AS 2410, AS 2810, AS 1301, and AS 2201, read together as the fraud
  architecture of a PCAOB audit.
- AICPA AU-C 240, with AU-C 260, AU-C 265, AU-C 315 (as amended by SAS 145), and AU-C 550.
- FASB ASC 606, particularly the contract-existence criteria in ASC 606-10-25 and the remaining performance
  obligation disclosure requirements; SEC guidance on key operating metrics in Management's Discussion and
  Analysis; Exchange Act Section 10A and Rule 10A-3; and COSO's *Internal Control — Integrated Framework*
  principle 8 on assessing fraud risk.

