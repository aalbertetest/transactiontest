# Chapter 13 — Walkthroughs and Documenting Process Understanding

> A walkthrough is the cheapest procedure in the integrated audit and the one most often wasted. It costs two
> hours of a senior's time and produces, when it is done well, the entire architecture of the controls audit:
> where the transactions enter, where they can go wrong, what management does about it, and whether what
> management does about it could possibly work. Done badly it produces a nine-page narrative that recites the
> client's policy manual back to the client, a control matrix in which eleven of nineteen "controls" are process
> steps, and a false sense that the process is understood. On October 7, 2025, two members of the Brightline
> engagement team sat down with AtlasFlow's VP of Sales Operations and its Revenue Manager for a walkthrough of
> order-to-cash. In ninety minutes they learned that the quarterly user access review described in management's
> documentation is performed once a year, and they failed to learn — because they did not ask one more question —
> that a control central to revenue cut-off does not exist. This chapter is about the difference between those
> two outcomes.

## Learning Objectives

- **LO 13.1** Distinguish the three objectives a walkthrough is used to pursue — obtaining an understanding of
  the process, evaluating the design effectiveness of a control, and testing operating effectiveness — and state
  what evidence a walkthrough does and does not produce for each.
- **LO 13.2** Identify the points in a transaction flow at which transactions are initiated, authorized,
  processed, and recorded, and mark those points on a process map.
- **LO 13.3** Document the same process in narrative, flowchart, control matrix, and hybrid form, and select the
  format appropriate to a given process and audit purpose.
- **LO 13.4** Identify what could go wrong (WCGW) at each process point and link each WCGW to the specific
  relevant assertions it would affect.
- **LO 13.5** Distinguish a control from a process step, rewrite a defective control description so that it names
  a performer, a criterion, a disposition, and a population, and evaluate whether the control operates at a level
  of precision sufficient to address the WCGW it is mapped to, quantifying the misstatement that could pass
  through it undetected.
- **LO 13.6** Sequence and phrase walkthrough inquiry so that it corroborates rather than solicits, including
  the handling of the "we always do it correctly" answer and of an interviewee describing policy rather than
  practice.
- **LO 13.7** Trace a single transaction from origination through to the financial statement line item and
  document the trace with the field names, record identifiers, and amounts obtained at each stage.
- **LO 13.8** Identify undocumented controls and documented controls that do not exist, and determine the
  consequences of each for the control conclusion and for testing already performed.
- **LO 13.9** Apply defined criteria to choose between an annual walkthrough refresh and a full re-walkthrough,
  and document the choice.
- **LO 13.10** Design walkthrough procedures for remote, offshore, automated, and vendor-hosted processes where
  no human performs the control, and draft walkthrough documentation that permits an experienced auditor with no
  prior connection to the engagement to evaluate the sufficiency of the understanding obtained.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of Financial Statements*, paragraphs 34 and 37 (Understanding Likely Sources of Potential Misstatement) | Requires the auditor to understand the flow of transactions relating to relevant assertions, including how they are initiated, authorized, processed, and recorded; to verify that the points at which misstatement could arise have been identified; and to identify management's controls over those points and over unauthorized acquisition, use, or disposition of assets. Identifies walkthroughs as frequently the most effective way of achieving those objectives |
| PCAOB | AS 2201 (Testing Design Effectiveness; Testing Operating Effectiveness) | Establishes design and operating effectiveness as separate evaluations, and states that procedures performed to evaluate design may *also* provide evidence about operating effectiveness in some circumstances. That "may" is the hinge of §13.2 |
| PCAOB | AS 2110 | Requires an understanding of the system of internal control sufficient to identify types of potential misstatement, and evaluation of whether controls relevant to the audit are suitably designed and have been implemented |
| PCAOB | AS 1105 | Ranks evidence reliability; inquiry alone does not provide sufficient appropriate evidence about a control's operating effectiveness. Also governs the reliability of information produced by the entity (IPE) used in a walkthrough |
| PCAOB | AS 2301 | Requires the nature, timing, and extent of further procedures to respond to assessed risk; a design deficiency found in a walkthrough changes the planned substantive response |
| PCAOB | AS 1215 and AS 1201 | Documentation sufficient for an experienced auditor with no previous connection to the engagement, and the reviewer's obligation to evaluate whether the understanding supports the conclusions — the specification §13.13 is written against |
| PCAOB | AS 2401 | Requires inquiry of employees involved in processing transactions about knowledge of fraud, suspected fraud, or allegations of fraud — most efficiently made during the walkthrough |
| PCAOB | AS 2601 | Frames what can and cannot be learned about a vendor-hosted process, and directs the auditor to the service auditor's report |
| PCAOB | AS 1305 | Requires communication of significant deficiencies and material weaknesses; Chapter 14 owns the severity framework this chapter's findings feed |
| AICPA | AU-C 315 (as amended by SAS 145, effective for periods ending on or after December 15, 2023) | Requires evaluation of the design of controls in the control activities component and a determination that they have been *implemented*; states that risk assessment procedures alone do not provide sufficient appropriate evidence of operating effectiveness |
| AICPA | AU-C 230, AU-C 240, AU-C 265, AU-C 330, AU-C 402 | Documentation; fraud inquiries; communication of deficiencies where there is no ICFR opinion; the requirement for tests of controls where reliance is intended; and service organizations |
| FASB ASC | 606-10-25-1 through 25-3 | A contract exists only when the parties have approved it and it creates enforceable rights and obligations — what makes the CPQ signature-date field financially relevant and produces WCGW-3 |
| FASB ASC | 606-10-25-23 through 25-30 | Revenue is recognized as control transfers, which for a hosted service begins on provisioning — the requirement behind WCGW-6 and this chapter's case study |
| COSO | *Internal Control — Integrated Framework* (2013), Principles 10 and 12 | Control activities must be selected to mitigate risks and deployed through policies that establish what is expected and procedures that put them into action. Principle 12 is the authority for treating a documented-but-unperformed control as a deficiency rather than a documentation problem |
| SEC | Release No. 33-8810 (June 2007), *Commission Guidance Regarding Management's Report on Internal Control Over Financial Reporting* | Frames management's own risk-based identification of financial reporting risks and the controls that address them, which makes management's documentation a testable artifact |

Because AtlasFlow is an SEC issuer, PCAOB standards govern, and FY2025 is its first ICFR opinion. Readers auditing
private SaaS companies apply the AICPA analogues, with three differences. Without an ICFR opinion the walkthrough
inventory is shorter, covering only processes where controls will be relied on or where the understanding is needed
to identify risks. AU-C 315 frames the requirement as evaluating design and determining *implementation*, which a
single traced transaction discharges completely, whereas under AS 2201 the same procedure leaves operating
effectiveness entirely untouched. And findings like this chapter's case study feed an AU-C 265 written
communication rather than an adverse opinion — which changes the stakes but not the analysis.

## Prerequisites and Chapter Dependencies

Read Chapter 2 first: risk assessment determines which processes are walked and which relevant assertions the
walkthrough must cover, and this chapter takes that scoping as given. Chapters 11 and 12 own the controls being
walked through — Chapter 11 the IT general controls over Okta, Salesforce, Zuora, and NetSuite, and Chapter 12
the automated application controls, the CPQ approval configuration, the RevPro rule set, and the I-1 through I-9
interfaces — and this chapter neither describes nor evaluates those controls except as objects of walkthrough
technique. Chapter 14 owns everything that happens after the walkthrough: designing tests of operating
effectiveness, sample sizes, evaluating deviations, and grading deficiencies. Chapter 4 supplies the
order-to-cash accounting and the cut-off procedures that the WCGWs in §13.5 threaten.

## 13.1 What a Walkthrough Is, and What It Is Not

A **walkthrough** is a procedure in which the auditor follows a transaction from its origination through the
entity's processes, including its information systems, to the point at which it is reflected in the financial
records, using a combination of inquiry of the personnel who perform each step, observation of the activity,
inspection of the documents and system records produced, and — where the auditor chooses — re-performance of
the step. AS 2201 identifies it as frequently the most effective way to achieve four objectives: understanding
the flow of transactions, verifying that the auditor has identified the points at which misstatement could
arise, identifying the controls management has implemented at those points, and identifying controls over the
prevention or timely detection of unauthorized acquisition, use, or disposition of assets.

Four things follow, and each is routinely misunderstood.

**A walkthrough is a procedure, not a document.** The narrative is the record; the walkthrough is the ninety
minutes in which a person who performs the work answers questions and shows you a screen. An engagement that
"updated the walkthroughs" by emailing last year's narratives to the client for confirmation performed a single
inquiry, of the wrong person, about a document.

**A walkthrough follows one transaction, not the process in the abstract.** Asking Jordan Pike how the interface
reconciliation operates produces a description. Asking him to open the September 30, 2025 reconciliation report,
show you the 14 exceptions it listed, and show you what he did with exception 9 produces evidence. Pick the
transaction before the meeting.

**A walkthrough is performed by the auditor, on the auditor's own behalf.** Internal audit's July 2025 readiness
assessment produced a process narrative for each significant AtlasFlow process. Those narratives are useful
inputs, not substitutes — and they are precisely the documents that were wrong in this chapter's case study.

**A walkthrough is not a test of controls.** This is where the most audit time is wasted and the most audit risk
created, and §13.2 is devoted to it.

What a walkthrough does *not* accomplish needs saying plainly:

1. It does not establish that a control operated throughout the period, or on any occasion other than the one
   the auditor looked at.
2. It does not establish that the population the control was applied to was complete.
3. It does not establish that the control operated when it mattered — walkthroughs are conducted in September
   and October and the transactions that matter most were signed on December 29.
4. It does not establish that the person you interviewed performs the control the way she described it, unless
   you inspected evidence that she did.
5. It does not, on its own, support a conclusion that a control is designed effectively, if the auditor did not
   articulate the WCGW the control is supposed to address. A control cannot be evaluated against nothing.

## 13.2 The Three Objectives That Get Conflated

Three distinct objectives are pursued with substantially the same-looking procedures, and practitioners slide
between them without noticing. Naming them separately is the single highest-value habit in the controls audit.

**Objective 1 — obtaining an understanding of the process.** The output is knowledge: the flow, the systems, the
people, and the points at which the flow could produce a misstatement in a relevant assertion. Inquiry plus one
traced transaction plus inspection of the documents that transaction generated is sufficient. Required by AS 2110
and AU-C 315 regardless of whether the auditor intends to rely on any control.

**Objective 2 — evaluating design effectiveness.** The output is a conclusion: *if this control operated as
described, by a person with the competence and authority described, on the complete population described, it
would prevent or detect on a timely basis a misstatement in the relevant assertion that could be material.*
Sufficient evidence is the understanding from Objective 1, plus an articulated WCGW, plus an assessment of
precision (§13.7), plus enough inspection to establish that the control exists in operation at all. A walkthrough
is a fully sufficient procedure here, which is what practitioners correctly mean when they say the walkthrough
supports design effectiveness.

**Objective 3 — testing operating effectiveness.** The output is a different conclusion: *this control operated
as designed, throughout the period of intended reliance, on the population it was supposed to be applied to,
with a deviation rate low enough to support reliance.* That requires a defined population, a defined attribute, a
selection representative of the whole period, and inspection or re-performance of each item selected. Chapter 14
owns it.

**Exhibit 13-1. What a single walkthrough produces for each objective.**

| Evidence element the objective requires | Understanding (Obj. 1) | Design effectiveness (Obj. 2) | Operating effectiveness (Obj. 3) |
| --- | --- | --- | --- |
| Flow of transactions described by the performer | Sufficient | Necessary | Not relevant |
| One transaction traced end to end | Sufficient | Necessary | Contributes one item |
| WCGW articulated at each process point | Required for completeness of the understanding | Necessary — the control is evaluated against it | Presupposed |
| Precision of the control assessed | Not required | Necessary | Presupposed |
| Evidence the control exists in operation | Not required | Necessary | Presupposed |
| Population of control occurrences defined and its completeness tested | Not required | Not required | Necessary |
| Representative selection across the period of intended reliance | Not required | Not required | Necessary |
| Inspection or re-performance of each selected occurrence | Not required | Not required | Necessary |
| Deviation evaluation and conclusion on reliance | Not required | Not required | Necessary |
| **Walkthrough alone is sufficient?** | **Yes** | **Yes** | **No** |

The arithmetic is worth doing once. Take OTC-04, the daily review of the I-1 Salesforce-to-Zuora error queue
performed by Billing Analyst Marcus Delgado. The control operates on each of 251 business days in the period of
intended reliance, and a walkthrough inspects the queue for one day. Under the attribute-sampling logic
Chapter 14, §14.5 develops, a sample of one from a population of 251 supports, at a 10% risk of overreliance, an
upper deviation limit of roughly 90% — one clean observation is consistent with the control having failed nine
days out of ten. For a high-frequency control the walkthrough does not provide *weak* operating-effectiveness
evidence; it turns a sample of 25 into a sample of 26 and nothing else. For a *low*-frequency control the picture
inverts: for an annual control with a population of one, a walkthrough that inspects the single occurrence with
its supporting documents and re-performs the reviewer's comparison is the whole test. That is the circumstance
AS 2201 has in mind when it says design procedures "may" provide operating-effectiveness evidence. The rule of
thumb: the lower the frequency, the more of the test the walkthrough performs — and for a control that operates
once, the two can be the same procedure, provided the auditor documents it as both, obtains the population of
one, and inspects rather than discusses.

The corollary trap is the walkthrough workpaper concluding "the control is operating effectively." That sentence
is a review comment every time. The permitted conclusions are "the process is understood and the points at which
misstatement could arise have been identified" and "the control as designed would, if it operated, address
WCGW-6 at a level of precision sufficient to detect a misstatement of $940 or more."

## 13.3 Initiation, Authorization, Processing, and Recording

AS 2201's phrase "how these transactions are initiated, authorized, processed, and recorded" is not decoration.
Marking those four points on a process map is a mechanical discipline that finds gaps, because the points are
where the transaction changes state and therefore where a misstatement can enter without contradicting anything
that came before. In this book they are abbreviated **IAPR**.

- **Initiation.** The event that first creates a record with accounting consequence. In AtlasFlow's enterprise
  channel this is not the customer's signature; it is the creation of an opportunity and quote in Salesforce
  CPQ, because that is the record from which every downstream field is inherited.
- **Authorization.** The point at which a person or a configured rule with the requisite authority approves the
  transaction or its terms. There is usually more than one: pricing authorization is separate from the
  authorization to activate, which is separate from the authorization to invoice.
- **Processing.** Every transformation between authorization and recording: the interface transfers, the
  allocation of the transaction price in RevPro, the generation of the revenue schedule, the amortization run.
- **Recording.** The point at which the transaction enters the general ledger and therefore the financial
  statements, which for AtlasFlow's subscription revenue is one monthly summary journal (I-3), not 14,392
  entries.

**Exhibit 13-2. IAPR map — AtlasFlow enterprise order-to-cash (extension for this chapter; system facts per
continuing case §2.1 and §2.2).**

| Seq | Process point | System | IAPR classification | Record created | Performer / rule |
| --- | --- | --- | --- | --- | --- |
| 1 | Opportunity and quote created; product, term, seats, start date entered | Salesforce Sales Cloud + CPQ | Initiation | Quote record `Q-#####` | Account Executive |
| 2 | Required-field validation on quote submission | CPQ | Processing (automated) | Validation rule | Configured rule |
| 3 | Discount routed for approval per the CPQ approval matrix | CPQ | **Authorization** (pricing) | Approval record with approver, timestamp | Configured matrix; approver by tier |
| 4 | Order form generated and sent for signature | CPQ / DocuSign | Processing | Order form PDF, envelope ID | Account Executive |
| 5 | Executed order form received; signature date recorded; opportunity set to Closed Won | CPQ | **Authorization** (contract existence) | `Contract_Signed_Date__c`, `Service_Start_Date__c` | Account Executive; Deal Desk |
| 6 | Deal Desk compares executed PDF to CPQ record and activates the order | CPQ | **Authorization** (activation) | `Deal_Desk_Validated__c`, activation timestamp | Deal Desk Analyst |
| 7 | Order transfers to Zuora Billing; subscription and rate-plan charges created | I-1 (real time, API) | Processing (interface) | Subscription `A-S#####` | Zuora CPQ connector; error queue |
| 8 | Tenant provisioned in the AtlasFlow platform; provisioning-complete timestamp written | Platform admin console | Processing | `provisioned_at` | Provisioning engineer / automation |
| 9 | Invoice generated per billing schedule | Zuora Billing | Recording (receivable) | Invoice `INV-######` | Bill run (scheduled) |
| 10 | Nightly batch transfers billing data to Zuora Revenue | I-2 (02:00 CT) | Processing (interface) | Revenue contract, POB records | Native connector; reconciliation report |
| 11 | RevPro identifies performance obligations, allocates price, builds schedule | Zuora Revenue | Processing (automated) | Revenue schedule lines | 27 configuration rules |
| 12 | Monthly summary journal posted to accounts 4100/4110/4120/2400/2410 | I-3 → NetSuite | **Recording** | Journal `RP-2025-MM-01` | Scheduled integration; Controller approval |
| 13 | Cash applied; receivable relieved | Zuora Billing / I-9 bank feed | Processing | Payment record | Bank feed; Staff Accountant |

Two observations from the map, both from the October 7 walkthrough. There are three distinct authorization points
and management's own narrative described only one of them (the discount approval at seq. 3), which is why the
activation authorization at seq. 6 was documented in a way nobody had tested. And the *recording* point is a
single monthly journal, which makes the control at seq. 12 the last opportunity to catch anything that happened
upstream and therefore the highest-value control in the process; Chapter 14's walkthrough tests it.

## 13.4 The Same Process in Four Formats

Practitioners argue about narrative versus flowchart versus matrix as though one were correct. They answer
different questions. Below is the same sub-process — enterprise order origination through activation, seq. 1
through 8 of Exhibit 13-2 — documented four ways, so the trade-offs are visible rather than asserted.

### 13.4.1 Format 1 — Narrative

**Exhibit 13-3. Narrative documentation of enterprise order origination through activation.**

```text
WP 3100-04A   ATLASFLOW, INC. — FY2025
PROCESS NARRATIVE: ENTERPRISE ORDER ORIGINATION THROUGH ACTIVATION
Prepared by C. Nwosu (CJN) 10/08/2025; source: walkthrough 10/07/2025 with
B. Hallowell (VP Sales Operations) and T. Brandt (Deal Desk Analyst),
inspection of order Q-48117 / A-S30412, and observation of activation.
--------------------------------------------------------------------------------
An Account Executive ("AE") creates an opportunity in Salesforce Sales Cloud and
builds a quote in CPQ, selecting products from the price book and entering the
subscription term, automation seat count, committed workflow-run volume, and
requested service start date. CPQ will not permit a quote to be submitted for
approval unless term, seat count, price book entry, and requested start date are
populated; the submission is blocked with a validation message. [OTC-01]

Discounting is governed by the CPQ approval matrix. A quote whose aggregate
discount to list is 15.0% or less requires no approval beyond the AE. Discounts
above 15.0% and up to 25.0% route to the Regional Vice President; above 25.0% and
up to 40.0% to the Chief Revenue Officer; above 40.0%, and any non-standard legal
term flagged by the legal-terms picklist, to the Chief Financial Officer. Routing
is by configured rule, not by request; the quote cannot advance to order-form
generation while an approval is outstanding, and the approver's user ID and
timestamp are written to the approval record. [OTC-02]

On approval, CPQ generates the order form PDF and the AE sends it for signature
through DocuSign. When the executed document is returned, the AE records the
signature date in the Contract_Signed_Date__c field, attaches the executed PDF to
the opportunity, and sets the stage to Closed Won.

Before the order is activated, the Deal Desk Analyst opens the attached executed
PDF and compares it to the CPQ order record for five attributes: legal entity,
subscription term start and end dates, contract signature date, total contract
value, and seat count. Differences are returned to the AE for correction; the
Analyst does not correct them. When the five attributes agree, the Analyst sets
Deal_Desk_Validated__c to TRUE, which is the system prerequisite for activation.
Activation writes the order to Zuora Billing over the I-1 API connection in real
time. [OTC-03]

Field mapping across I-1 is automated. Records that fail to transfer, or that
transfer with a mapping error, land in the Zuora integration error queue. The
Billing Analyst reviews the queue each business morning, works each item to
resolution, and records the resolution in the queue comment field; unresolved
items more than one business day old are escalated by email to the Revenue
Manager. [OTC-04]

Provisioning is independent of billing. A provisioning request is created
automatically on activation; the platform writes a provisioned_at timestamp when
the customer tenant is live. Per AtlasFlow's revenue policy, subscription revenue
begins on the later of the contract start date and the provisioning date. The
mechanism by which that is reflected in RevPro is addressed at WP 3100-04C.
[OTC-05 — see WP 3100-09]
--------------------------------------------------------------------------------
```

The narrative's virtue is that it expresses conditionality, exception, and judgment: "the Analyst does not correct
them" is a segregation statement no flowchart box holds. Its vice is that a reader cannot tell whether it is
complete, and control descriptions hide inside prose. The paragraph beginning "On approval, CPQ generates the
order form" carries no control tag, correctly — it is a sequence of process steps — but a reader has to notice the
absence to know it.

### 13.4.2 Format 2 — Flowchart

**Exhibit 13-4. Process flow diagram, same sub-process, with swimlanes and control points.**

```text
        SALES (AE)          |   SALES OPS / DEAL DESK   |    SYSTEM (CPQ/ZUORA)     |  PLATFORM
 ---------------------------+---------------------------+---------------------------+-------------
  (1) Create opportunity    |                           |                           |
      and CPQ quote         |                           |                           |
            |               |                           |                           |
            v               |                           |                           |
  (2) Submit for approval --------------------------->  [OTC-01] Required-field     |
                            |                           validation; block on fail   |
                            |                                     |                 |
                            |                                     v                 |
                            |                          [OTC-02] Discount tier       |
                            |                          routing:  <=15% none         |
                            |                                   >15-25% RVP         |
                            |                                   >25-40% CRO         |
                            |                                     >40% CFO          |
                            |                                     |                 |
            <---------------|-------- rejected --------- <decision: approved?>       |
            |               |                                     | yes             |
            v               |                                     v                 |
  (3) Send order form  <-------------------------------  Generate order form PDF     |
      via DocuSign          |                           |                           |
            |               |                           |                           |
            v               |                           |                           |
  (4) Record signature      |                           |                           |
      date; attach PDF;     |                           |                           |
      set Closed Won        |                           |                           |
            |               |                           |                           |
            +-------------> (5) [OTC-03] Compare        |                           |
                                executed PDF to CPQ     |                           |
                                record, 5 attributes    |                           |
                                     |                  |                           |
            <--- differences --------+                   |                           |
                                     | agree            |                           |
                                     v                  |                           |
                                (6) Set Deal_Desk_      |                           |
                                    Validated = TRUE ------> Activate order          |
                                                        |         |                 |
                                                        |         +---> I-1 API ---> |
                                                        |         |                 |
                                                        |         v                 |
                                                        |  Zuora subscription       |
                                                        |  A-S#####  created        |
                                                        |         |                 |
                                (7) [OTC-04] Daily <----+--- error queue (fail)     |
                                    error-queue review  |                           |
                                                        |                           |
                                                        |  provisioning request ---> (8) Tenant
                                                        |                           |     provisioned;
                                                        |                           |     provisioned_at
                                                        |                           |     written
 ---------------------------+---------------------------+---------------------------+-------------
  LEGEND:  [OTC-nn] control point.  <decision> branch.  ---> data or document flow.
  WCGW references keyed to Exhibit 13-8 are shown in the matrix, not on the flow.
```

The flowchart exposes structure: swimlane boundaries are handoffs, and every handoff is a candidate WCGW. Reading
Exhibit 13-4 you see immediately that the signature date is recorded by the person whose compensation depends on
the deal closing in the period, and that one Deal Desk comparison stands between that field and the revenue
subledger. The same fact is in the narrative and almost nobody notices it there. The flowchart's vice is that it
cannot express precision, frequency, or criteria; "[OTC-03] Compare executed PDF to CPQ record" is one box whether
the comparison covers five attributes or one.

### 13.4.3 Format 3 — Control matrix

**Exhibit 13-5. Control matrix, same sub-process.**

| Ref | Process point (Exh. 13-2 seq.) | Control description | WCGW addressed | Relevant assertion(s) | P/D | Type | Frequency | Performer (title) | Evidence of operation |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| OTC-01 | 2 | CPQ blocks submission of a quote for approval unless subscription term, seat count, price book entry, and requested service start date are populated | WCGW-4 | Accuracy | Prevent | Automated application control | Each quote | None (configured rule) | Configuration screenshot; test-of-one on a quote with a blank term |
| OTC-02 | 3 | CPQ routes a quote whose aggregate discount exceeds 15.0% to the tier of approver specified in the approval matrix and blocks order-form generation until the approval record is written | WCGW-2 | Occurrence, accuracy | Prevent | Configurable automated control | Each quote above threshold | Approval record: approver user ID, timestamp | Configuration inspection plus re-performance; see Chapter 12, §12.6 |
| OTC-03 | 6 | Deal Desk Analyst compares the executed order form PDF to the CPQ order record for legal entity, term start and end dates, signature date, total contract value, and seat count; returns differences to the AE for correction; sets Deal_Desk_Validated__c to TRUE only when all five agree, which is the system prerequisite for activation | WCGW-1, WCGW-3, WCGW-4 | Occurrence, accuracy, cut-off | Prevent | IT-dependent manual | Each order | Deal_Desk_Validated__c flag with user ID and timestamp; no record of the differences identified | Inspection of the flag; inspection of the PDF and CPQ record for a selection |
| OTC-04 | 7 | Billing Analyst reviews the Zuora integration error queue each business morning, resolves each item, records the resolution in the queue comment, and escalates items unresolved after one business day to the Revenue Manager | WCGW-5 | Completeness, accuracy | Detect | IT-dependent manual | Daily | Queue comment with user ID and timestamp; escalation emails | Inspection of the queue export for the period and of resolutions for a selection |
| OTC-05 | 8, 11 | *As documented by management:* Revenue Manager compares the Zuora Billing subscription service start date to the platform provisioning-complete date for all subscriptions activated in the month and adjusts the RevPro revenue start date where provisioning is later | WCGW-6 | Cut-off, occurrence | Detect | IT-dependent manual | Monthly | *See WP 3100-09 — the control as documented does not exist* | *n/a* |

The matrix is auditable — every column is a question the auditor must answer, and a blank cell is a finding — and
it forces the WCGW-to-assertion linkage that narratives let you skip. Its vices are that it destroys sequence (you
cannot tell from Exhibit 13-5 that activation precedes provisioning) and that it invites the auditor to treat the
row as the understanding. A matrix with nothing behind it produces the characteristic failure of large ICFR
programs: nineteen well-documented control rows and no idea how a transaction moves.

### 13.4.4 Format 4 — The hybrid

The hybrid is what competent practice produces: a flow diagram for the shape, a narrative keyed to the diagram for
the conditionality, and a matrix keyed to both for the control attributes, with one reference scheme running
through all three. The keying matters more than the choice of tool.

**Exhibit 13-6. Hybrid documentation — reference architecture and a worked fragment.**

```text
WP 3100-04    ORDER-TO-CASH — PROCESS UNDERSTANDING (HYBRID)
  .04A  Narrative, keyed [OTC-nn] and (seq n)          <- Exhibit 13-3
  .04B  Flow diagram, swimlanes, keyed [OTC-nn]        <- Exhibit 13-4
  .04C  Control matrix, keyed OTC-nn / WCGW-n / seq n  <- Exhibit 13-5
  .04D  WCGW-to-assertion matrix, keyed WCGW-n         <- Exhibit 13-8
  .04E  Transaction trace, one order, all seq points   <- Exhibit 13-15
  .04F  Walkthrough record: attendees, dates, questions asked, documents
        inspected, observations made, open items       <- Exhibit 13-18
--------------------------------------------------------------------------------
WORKED FRAGMENT — seq 6, control OTC-03

FLOW (from .04B):  [AE: set Closed Won] --> [Deal Desk: OTC-03 compare 5
                   attributes] --(agree)--> [set Deal_Desk_Validated = TRUE]
                   --> [activate to Zuora via I-1]
                   --(differ)--> [return to AE; no Deal Desk correction]

NARRATIVE (from .04A): "Before the order is activated, the Deal Desk Analyst
opens the attached executed PDF and compares it to the CPQ order record for five
attributes ... the Analyst does not correct them."

MATRIX (from .04C): OTC-03 | prevent | IT-dependent manual | each order |
Deal Desk Analyst | evidence = Deal_Desk_Validated__c flag only |
WCGW-1, WCGW-3, WCGW-4 | occurrence, accuracy, cut-off

WCGW LINK (from .04D): WCGW-3 "signature date recorded in CPQ is not the date the
contract was executed" -> revenue occurrence and cut-off -> also a fraud risk;
see Chapter 17.

PRECISION NOTE (per the analysis at Exhibit 13-10): the comparison is to the executed
PDF only. If the PDF itself bears a signature date that is not the true execution
date, OTC-03 cannot detect it: the control compares two representations of the
same assertion. The DocuSign envelope completion timestamp is the independent
attribute and is not part of the comparison.                            (a)

TRACE (from .04E): Q-48117 -> approval rec. 10/02/2025 14:07 by S. Marchetti
(28.4% discount, CRO tier) -> order form PDF -> executed 10/03/2025 ->
Contract_Signed_Date__c = 10/03/2025; DocuSign envelope completed 10/03/2025
16:22 CT -> agree -> Deal_Desk_Validated__c TRUE 10/06/2025 09:14 by T. Brandt
-> A-S30412 in Zuora 10/06/2025 09:14 -> provisioned_at 10/08/2025 11:40.

(a) This precision observation is the finding that should have been made on
    10/07/2025 and was not; see §13.9, Annotation 13-9.
--------------------------------------------------------------------------------
```

**Exhibit 13-7. Choosing a format.**

| Situation | Preferred primary format | Why |
| --- | --- | --- |
| Process with many handoffs between functions or systems (order-to-cash, procure-to-pay) | Flowchart, with matrix | Handoffs are where WCGWs live and a diagram makes every handoff visible |
| Process that is mostly judgment performed by one or two people (the close, an estimate) | Narrative, with matrix | The content is criteria and thresholds, which boxes cannot hold |
| Process already stable and documented, being refreshed | Matrix with a change log | The question in a refresh year is "what changed," and a matrix diff answers it |
| Highly automated process with no human step (RevPro allocation, the Stripe Lambda job) | Matrix plus configuration inventory | There is no sequence of human activity to narrate; the control *is* the configuration |
| Offshore or remote process | Narrative plus a screen-by-screen observation record | You cannot stand behind the person; the record of what you watched them do carries the weight |
| First-year ICFR program with an inexperienced client | Hybrid, all five components | The documentation is doing double duty as the auditor's understanding and as the reference against which management's own documentation is evaluated |

## 13.5 What Could Go Wrong, and the Link to Relevant Assertions

The **WCGW** is the pivot of the whole exercise. It is a statement, at a specific process point, of a specific
way in which a transaction could be recorded wrongly, expressed so that it can be linked to a relevant assertion
and so that a control can be evaluated against it. Three disciplines separate a usable WCGW from a useless one.

**Be specific about the mechanism.** "Revenue may be misstated" is the audit objective restated. "The signature
date recorded in `Contract_Signed_Date__c` is earlier than the date the order form was actually executed, so
revenue and the receivable are recorded in a period before the contract existed" is a WCGW: it names a field, a
direction, and a consequence.

**Locate it at a process point.** Every WCGW attaches to a sequence number in Exhibit 13-2. A WCGW that cannot be
located has usually been written at the account level, and account-level WCGWs cannot be mapped to controls.

**Derive it from the flow, not from a library.** Firm WCGW libraries are a reasonable completeness check and a poor
starting point; used first they produce documentation describing a generic company. WCGW-6 — revenue beginning
before provisioning — appears in no generic order-to-cash library, because it arises from AtlasFlow's own policy
and from the fact that activation in Zuora and provisioning in the platform are independent events (seq. 6 and 8).

**Exhibit 13-8. WCGW-to-assertion-to-control matrix, AtlasFlow enterprise order-to-cash.** Assertion
abbreviations: O = occurrence, C = completeness, A = accuracy, CO = cut-off, CL = classification, P&D =
presentation and disclosure.

| WCGW | Seq. | Statement of what could go wrong | Account(s) affected | Relevant assertion(s) | Control(s) mapped | Design conclusion |
| --- | --- | --- | --- | --- | --- | --- |
| WCGW-1 | 5 | An order is recorded and activated for a contract the customer never executed, or executed by a person without authority to bind it | 4100, 4110, 1200, 2400 | O, A | OTC-03 | Effective as designed |
| WCGW-2 | 3 | A discount, non-standard legal term, or price outside the price book is granted without approval at the required authority level, so the transaction price recorded is not the approved price | 4100, 4110, 1200 | O, A | OTC-02 | Effective as designed; precision analyzed at §13.7 |
| WCGW-3 | 5 | The signature date recorded in CPQ is earlier than the date the order form was actually executed, recording revenue in a period before enforceable rights existed | 4100, 4110, 1200, 2400 | O, CO | OTC-03 | **Deficient** — control compares two representations of the same asserted date; see §13.7 and Chapter 17 |
| WCGW-4 | 1, 5 | Contract data (term, start and end dates, seats, total contract value, legal entity) is keyed into CPQ inconsistently with the executed document, so billing and the revenue schedule are built on wrong terms | 4100, 4110, 2400, 2410 | A | OTC-01, OTC-03 | Effective as designed |
| WCGW-5 | 7 | An activated order fails to transfer across I-1, or transfers with fields dropped, so the subscription is never billed or is billed on wrong terms | 4100, 4110, 1200, 2400 | C, A | OTC-04 | Effective as designed |
| WCGW-6 | 8, 11 | Revenue begins on the contract start date although the customer tenant was not provisioned until later, recognizing revenue before control of the service transferred | 4100, 4110, 2400 | CO, O | OTC-05 *(as documented)* | **Deficient — control does not exist as described; see the case study** |
| WCGW-7 | 11 | RevPro applies an out-of-date standalone selling price or the wrong performance-obligation template, misallocating the transaction price across obligations | 4100, 4110, 4200, 2400 | A, CL | RevPro configuration controls (Chapter 12, §12.7) | Out of scope here |
| WCGW-8 | 10 | The nightly I-2 batch fails or partially loads, so revenue contracts exist in Billing with no counterpart in Revenue | 4100, 4110, 2400 | C | OTC-07 (I-2 reconciliation) | Effective as designed |
| WCGW-9 | 12 | The monthly summary journal posts amounts that do not agree to the RevPro subledger, or posts to the wrong revenue or deferred revenue account | 4100–4120, 2400, 2410 | A, CL | OTC-08 (Controller review of the I-3 journal) | Effective as designed; precision tested in Chapter 14 |
| WCGW-10 | 9, 12 | A credit memo or SLA credit is issued without authorization, or is recorded in a period later than the period in which the obligation arose | 4900, 1200, 2230 | O, A, CO | OTC-09 | Precision insufficient; see §13.7 |

Two features of Exhibit 13-8 matter. The assertion column is the mechanism by which the controls audit and the
substantive audit are connected: WCGW-6 is a cut-off WCGW, so when its control turned out not to exist the
substantive response was a cut-off procedure — a full-population comparison of provisioning timestamps to revenue
start dates — not a larger sample of contract terms. And the design conclusion column is filled in *during* the
walkthrough phase, not later. Two of ten WCGWs at AtlasFlow have no effective control mapped to them, which is the
output of this phase and the input to Chapter 14's testing plan.

A WCGW with no control mapped to it is a design deficiency, not a documentation gap, and belongs on the deficiency
log the day it is identified, with severity left to Chapter 14. Engagement teams routinely leave such rows blank
pending "further discussion with management," and the blank is then closed six weeks later by a control management
describes in an email. The discipline: if the answer to "what addresses this?" is a control you have not seen
operate, log the WCGW as unaddressed until you have.

## 13.6 Distinguishing a Control from a Process Step

This is the single most common documentation defect in first-year ICFR programs, and it is the defect that most
reliably produces an untestable control matrix. AtlasFlow's internal audit function documented 19 "controls" in
the enterprise order-to-cash process in its July 2025 readiness assessment; Brightline's evaluation concluded
that 8 of the 19 were process steps.

A control has four properties. Something that lacks any one of them is a process step.

1. **A performer or a rule.** A named role, or a configured system rule. "Orders are activated in CPQ" has no
   performer; someone or something performs it, but the description does not say who, which means the auditor
   cannot ask that person how it works or test whether they did it.
2. **A criterion.** Something is compared to something else, or evaluated against a threshold. Activation is not
   a comparison. "Compare the five attributes on the executed PDF to the CPQ record" is.
3. **A disposition.** Something happens when the criterion is not met. If nothing happens on failure, nothing is
   being controlled. "The Analyst returns differences to the AE and does not set the validated flag" is a
   disposition; "the Analyst reviews the order" is not.
4. **A frequency and a population.** How often, over what set of items. Without a population there is nothing to
   sample from, which is why an untestable control is almost always one whose population was never articulated.

**Exhibit 13-9. Diagnosing eight descriptions from management's July 2025 order-to-cash documentation.**

| # | Description as written by management | Performer? | Criterion? | Disposition? | Population? | Verdict | Rewritten |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | "Orders are entered into Salesforce CPQ by the account executive." | Yes | No | No | Yes | Process step | Not a control; delete from the matrix and retain in the narrative |
| 2 | "Discounts are approved in accordance with the approval matrix." | Implicit | Implicit | No | No | Weak control description | "CPQ routes quotes with an aggregate discount above 15.0% to the approver tier specified in the matrix and blocks order-form generation until an approval record exists" |
| 3 | "The Deal Desk reviews the order for accuracy prior to activation." | Yes | No | No | Yes | Untestable — "reviews for accuracy" states no criterion | "…compares the executed order form to the CPQ record for legal entity, term start and end dates, signature date, total contract value, and seat count; returns differences to the AE; sets Deal_Desk_Validated__c only when all five agree" |
| 4 | "Invoices are generated automatically by Zuora based on the billing schedule." | Rule | No | No | Yes | Process step (an automated *process*, not an automated *control*) | Retain in the narrative; the control over billing accuracy is the OTC-03 comparison upstream |
| 5 | "Interface errors are monitored." | No | No | No | No | Not a control description at all | See OTC-04 in Exhibit 13-5 |
| 6 | "Revenue is recognized in accordance with the Company's revenue recognition policy." | No | No | No | No | A policy restatement | Delete; policies are not controls (COSO Principle 12 distinguishes the policy from the procedures that put it into action) |
| 7 | "The Revenue Manager reconciles Zuora Billing to Zuora Revenue." | Yes | Implicit | No | No | Control, under-specified | "…reviews the nightly I-2 reconciliation report, investigates every record-count or amount exception, clears it within two business days, and evidences the clearance in the exception log" |
| 8 | "Segregation of duties is maintained between sales and billing." | No | No | No | No | An objective, not a control | The controls that achieve it are the CPQ role configuration and the Zuora role configuration; see Chapter 11 |

The consequence is not cosmetic. Each row becomes a control the auditor must test, and testing a process step
produces a workpaper whose attribute is that the step occurred — which it always did, because the transaction
exists. Twenty-five of twenty-five orders were entered into CPQ; the test passes, no evidence is obtained, and the
genuine controls get less attention because the budget was consumed. Reduce the matrix before testing is planned,
and tell management why: the control population it asserts on should not contain items that cannot fail.

The mirror-image error: a process step *can* be part of a control when the system enforces a sequence. "Activation
is not possible unless `Deal_Desk_Validated__c` is TRUE" is a genuine automated control, because something is
prevented. The test is whether failure is possible and whether anything prevents or detects it.

## 13.7 Precision: Does the Control Actually Address the WCGW?

Design effectiveness is not "a control exists at this process point." It is "this control, operating as
described, would prevent or detect a misstatement in the relevant assertion that could be material." The gap
between those two sentences is **precision**, and precision is where design evaluations fail. Three questions
answer it, and each is arithmetic rather than adjective.

**Question 1 — What is the largest misstatement that could pass through the control undetected?** Work the
threshold. **Question 2 — Does the control operate on the complete population of items exposed to the WCGW?**
A control applied to 62% of the population addresses the WCGW for 62% of the population. **Question 3 — Is the
attribute compared genuinely independent of the assertion at risk?** A control that compares a number to itself
detects nothing.

**Exhibit 13-10. Precision analysis of three AtlasFlow order-to-cash controls (extension; order counts and
thresholds are illustrative extensions of the continuing case).**

| Control | WCGW | Threshold or scope of the control | Population exposed | Population covered | Largest misstatement that can pass | Precision conclusion |
| --- | --- | --- | --- | --- | --- | --- |
| OTC-02 discount approval | WCGW-2 | Routes above 15.0% aggregate discount to the specified approver tier | 1,842 FY2025 enterprise orders | 1,842 (every order is assessed by the rule) | A concession of up to 15.0% of list granted with no approval above the account executive. On the largest FY2025 order priced within that band ($2,400 of ACV), that is $360 of unapproved concession, below performance materiality of $940 | Sufficient as an authorization control at the order level. Note that it controls *authorization* of the price, not the *accuracy* of what is recorded: the recorded transaction price is controlled by OTC-03, so WCGW-2 and WCGW-4 must not be treated as one risk |
| OTC-03 Deal Desk five-attribute comparison | WCGW-3 | Compares CPQ record to the executed PDF | 1,842 orders | 1,842 | Unlimited. The PDF and the CPQ field are two representations of the same asserted signature date; if the date on the executed document is itself wrong, the comparison agrees | **Insufficient for WCGW-3.** Sufficient for WCGW-1 and WCGW-4, where the PDF is an independent source |
| OTC-09 credit memo approval | WCGW-10 | Controller approves credit memos above $25 | 412 FY2025 credit memos totaling $2,180 | 96 memos above $25, totaling $1,690 (77.5%) | 316 memos below $25 totaling $490 in aggregate, plus the possibility of splitting a credit into memos below the threshold | Sufficient for individually material credits; insufficient in aggregate, because $490 exceeds the $72 clearly trivial threshold and approaches performance materiality if the population grows. Mitigated by the monthly contra-revenue analytic; see Chapter 4, §4.9 |

The OTC-03 row is the finding the October 7 walkthrough should have produced. AtlasFlow's Q4 concentration — 41% of
Q4 ACV, $25,174, signed in the final five business days — means the signature-date assertion carries a large amount
of revenue, and a control that compares the CPQ date field to the date typed on the order form controls
transcription error, not date manipulation. The independent attribute exists: DocuSign writes an envelope
completion timestamp the AE cannot edit, and adding "agree `Contract_Signed_Date__c` to the envelope completion
timestamp" converts a transcription control into a cut-off control. The team identified this in January 2026 while
investigating the whistleblower allegation (Chapter 17), by which point six December contracts could not be
corroborated and became uncorrected misstatement U-3 of $150. The lesson is narrow: when a control compares A to B,
ask whether B is independent of the assertion at risk, and if it is not, ask what is.

Precision has a second dimension for review controls: the threshold at which the reviewer investigates. A
Controller who reviews the monthly revenue journal against the prior month and investigates variances above 10%
cannot detect a $500 error in a $12,000 journal, because $500 is 4.2%. Chapter 14, §14.9 develops the testing; in
the walkthrough your job is to obtain the threshold as a number from the person who applies it. If the answer is
"I look at whether anything seems unusual," you have obtained the precision: there is none.

## 13.8 Interview Technique in Operational Detail

The walkthrough is an interview, and interviewing is a skill with mechanics.

### 13.8.1 Interview the performer, not the owner

Owners wrote or approved the documentation and describe the control as documented, because that is their honest
belief. The performer knows what happens. Interview the performer; interview the owner separately if you need to
know why the control was designed as it was.

At AtlasFlow the distinction is concrete. Ray Sandoval, Director of IT and Information Security, owns the access
control set and will tell you the user access reviews are quarterly, because that is what he designed. Brett
Hallowell receives and completes the Salesforce portion, and he will tell you when he last received it. The second
answer is the fact (§13.9, Annotation 13-6). Where several people perform the control, interview the one with the
highest volume and corroborate with a second. Where the performer has left — two revenue accountants resigned in
Q2 2025 — interview the replacement about the current process and inspect the evidence of operation for the earlier
period, because the control you conclude on for FY2025 is not the control you were shown.

### 13.8.2 Sequence: funnel, then probe, then corroborate, then close

Open broadly to obtain the shape of the process in the interviewee's own words; the vocabulary matters, because you
will need their field names later. Then probe each step with closed questions for the specifics the open answer
omitted. Then corroborate by asking to see the artifact and asking questions you can verify against it while it is
on screen. Then close with the exception questions — what happens when it goes wrong, when did that last happen,
show me — and with the AS 2401 fraud inquiry.

**Exhibit 13-11. Question types, with AtlasFlow examples.**

| Type | Function | Example | Failure mode if overused |
| --- | --- | --- | --- |
| Open | Obtains the shape of the process and the interviewee's vocabulary; surfaces steps you did not know existed | "Walk me through what happens between the customer signing and the first invoice going out." | Produces a description you cannot test; consumes time |
| Closed / specific | Pins a fact: a number, a field, a threshold, a date, a name | "What is the discount percentage at which the quote stops going to the RVP and starts going to the CRO?" | Confirms your assumptions rather than discovering theirs; leads the witness |
| Corroborative | Asks for the artifact that would exist if the answer is true | "Show me the last three orders where the Deal Desk found a difference and sent it back." | None, if the request is specific; if vague, produces a curated example |
| Hypothetical / negative | Tests the boundary of the control | "Suppose an AE typed the seat count wrong and the Deal Desk missed it. Where would that show up next?" | Invites speculation presented as fact; label the answer as the interviewee's expectation |
| Repeat-back | Verifies your understanding in their words | "So the flag can only be set by someone in the Deal Desk role, and the AE cannot set it themselves — is that right?" | Becomes leading if you supply the answer you want |
| Fraud inquiry (AS 2401) | Required inquiry of those who process transactions | "Has anyone ever asked you to change a signature date or a start date after an order was activated?" | None; ask it of everyone, in every walkthrough, and record the answer verbatim |

Three sequencing rules earn their keep. Never ask the closed question first where an open question would have
revealed a step you do not know about; the closed question defines the universe of the answer. Never ask for the
artifact before you have the description, because once it is on screen the interviewee describes the artifact
rather than the process. And ask the exception questions last, because they shift the register from cooperative
description to accountability.

### 13.8.3 The "we always do it correctly" answer

The most common obstruction asserts the outcome instead of describing the activity: "we always check that," "the
system wouldn't allow it," "the reconciliation always ties." It is rarely evasion — usually it is a competent person
compressing a routine performed without conscious thought — but it contains no criterion, frequency, or
disposition, and it must be converted. Four conversions work, in escalating order:

1. **Ask for the last instance.** "When did it last not tie?" A performer who genuinely operates a detective
   control can name an occasion with detail. If the answer is "never," ask how long they have been doing it: never
   in seven months is plausible for a monthly control; never in three years across 251 daily occurrences is not,
   and the explanations are that the control does not detect, or that exceptions are resolved upstream or outside
   the control and never recorded.
2. **Ask for the mechanism, not the outcome.** Not "do you check" but "what would you be looking at, on which
   screen, that would tell you?"
3. **Ask for a walk-forward on a real item.** Hand them a transaction you selected in advance and have them
   perform the step while you watch. This converts assertion into observation.
4. **Ask the negative-population question.** "In the last three months, how many orders went back to the AE?"
   Then compare the answer to the system record. Brett Hallowell's "maybe two a month" against a rejection log
   showing 38 in September is a finding about the reliability of inquiry evidence generally, not just that answer.

### 13.8.4 Policy versus practice

An interviewee describing policy uses a distinctive register: the passive voice ("orders are reviewed"), the
normative present ("the analyst should compare"), the institutional subject ("we require"), and the vocabulary of
the documentation rather than of the screen. Practice names the screen, the report, the person, and the annoyance.
Three moves recover practice:

- **Move from the general to the last one.** "Tell me about the most recent one you did — was that Friday?"
- **Ask about the exception rather than the norm.** "What happens when the PDF and the CPQ record don't match and
  it's the last day of the quarter?" The process that operates on December 29 is the process that matters.
- **Ask who does it when they are on vacation.** The answer is a name (interview that person, and ask about the
  delegation), or "it waits" (the frequency is not what the documentation says), or "nobody" (a gap in a specific
  period you can now test).

Two habits close this section. Record answers in the interviewee's words, in quotation marks, where the answer will
bear weight; a paraphrase is your inference and a reviewer cannot distinguish the two. And separate what you were
*told* from what you *saw*, because they carry different weight under AS 1105 and a workpaper that blends them will
not support a design conclusion under review.

## 13.9 Annotated Transcript: The Order-to-Cash Walkthrough

The following is the record of the FY2025 enterprise order-to-cash walkthrough, performed at AtlasFlow's Austin
office on **October 7, 2025**, from 9:05 a.m. to 10:40 a.m. Central. Present: Grace Lindqvist (**GRL**, senior
manager) leading, Chris Nwosu (**CJN**, audit senior) documenting and driving the screen share, Brett Hallowell
(**BH**, VP Sales Operations) for seq. 1 through 7, and Jordan Pike (**JP**, Revenue Manager) for seq. 7 through
12. The dialogue is reconstructed to illustrate technique; the control facts it establishes are the facts used
throughout this chapter. Each annotation records three things: what the auditor concluded, what follow-up the
answer triggered, and — where applicable — where the auditor should have pushed harder.

### 13.9.1 Segment A — Brett Hallowell, order origination and authorization

**Q-1 (open).** *GRL:* "Before we get into any documentation, walk me through what happens from the moment a rep
thinks they have a deal to the moment the customer is live. Use whatever names you use internally."

*BH:* "So the rep builds a quote in CPQ off the price book. They pick Core, seats, term, and whether Insight is
in. If they're discounting they'll get routed for approval — that's automatic, they don't choose. Once it's
approved CPQ spits out the order form, they send it through DocuSign, customer signs, rep marks it Closed Won and
attaches the PDF. Then Deal Desk validates it and flips it live. Zuora picks it up basically instantly and
provisioning gets kicked off."

**Annotation 13-1.** *Concluded:* the flow matches Exhibit 13-2 seq. 1 through 8, and BH's own vocabulary supplies
the terms to use for the rest of the interview ("routed," "flips it live," "picks it up"). *Follow-up triggered:*
"flips it live" and "validates" are both undefined and both sit at an authorization point; each needs a criterion.
*Note:* BH described provisioning as a consequence of activation rather than a prerequisite for revenue. Nothing
in the open answer connected provisioning to the accounting, which is the first signal of the WCGW-6 problem.

**Q-2 (closed).** *GRL:* "At what discount percentage does approval stop being the RVP and become the CRO?"

*BH:* "Twenty-five. Under 25 it's the regional VP, over 25 it's Sofia. Over 40 it goes to finance — that used to
be the old CFO, now it's Tom. And anything under 15 the rep just does themselves."

**Annotation 13-2.** *Concluded:* the tiers in Exhibit 13-3 are confirmed by the performer and are consistent with
the configuration Chapter 12 tested. *Follow-up triggered:* whether the routing is on the aggregate contract
discount or per line — a distinction that determines whether a 40% discount on Insight inside a lightly discounted
Core deal routes at all. Asked, and the answer ("aggregate on the order") was corroborated against configuration
at Chapter 12, §12.6.

**Q-3 (probe).** *CJN:* "Who can edit the signature date field on the opportunity?"

*BH:* "The rep enters it. Deal Desk can change it. I can change it — I've got the admin profile. Honestly if a rep
fat-fingers it we just fix it, it's not a big deal."

**Annotation 13-3.** *Concluded:* `Contract_Signed_Date__c` is editable post-entry by at least three roles
including the process owner, so no system control preserves it. This is a design observation about WCGW-3
independent of anyone's intent. *Follow-up triggered:* (a) is Salesforce field history tracking enabled on that
field, and for how long is history retained; (b) can it be edited *after* activation, i.e. after the record has
already fed Zuora. *Cross-reference:* the fraud implications of the same fact are Chapter 17's, and the
walkthrough's job here is to record the capability and route it to the fraud risk assessment, not to investigate.

**Q-4 (probe, negative).** *CJN:* "Can you change it after the order has been activated and Zuora already has
it?"

*BH:* "Yeah. It doesn't push back to Zuora automatically, though, so if it actually matters we have to have Deal
Desk amend the subscription too."

**Annotation 13-4.** *Concluded:* a change to the signature date after activation produces a divergence between
Salesforce and Zuora unless a manual amendment follows, meaning the two systems can disagree and nothing detects
it. That is a new WCGW the auditor did not bring into the room. It was added to the matrix as WCGW-3(b) and mapped
to no control. *Follow-up triggered:* request a report of all post-activation edits to `Contract_Signed_Date__c`
and `Service_Start_Date__c` in FY2025 — obtained on October 21 (41 edits, 9 of them in the last week of a
quarter) and carried to the fraud risk assessment.

**Q-5 (corroborative).** *GRL:* "Let's pick one. Pull up Q-48117 — Nova Grid Utilities, the October first order.
Show me the approval record and the field history."

*BH:* [screen share] "Right, 28.4% discount so it went to Sofia — approved October 2 at 2:07 p.m. Field history
shows the signature date set once, October 3, by the rep. Never changed."

**Annotation 13-5.** *Concluded:* this is the walkthrough's evidential core: one transaction, inspected, with
approver identity and timestamp visible on screen. It supports (i) that OTC-02 operated on this order, (ii) that
history tracking is enabled on the field, and (iii) that the approval preceded order-form generation. *Follow-up
triggered:* CJN screenshotted both records into WP 3100-04E and recorded the DocuSign envelope completion
timestamp (October 3, 4:22 p.m. CT) — which is what made the Exhibit 13-6 precision note possible.

**Q-6 (probe, moving from owner to performer).** *GRL:* "Ray Sandoval told us there's a quarterly review of who
has the CPQ administrator profile. You're on the distribution for that — what does it look like when it reaches
you?"

*BH:* "Ray sends me a spreadsheet of everybody in Sales Ops with elevated Salesforce access and I go through and
say keep or remove, then I sign it and send it back. It's once a year — it came around in the summer. July or
August, I think. This year it was tied to the audit readiness thing."

*GRL:* "Once a year, or once a quarter?"

*BH:* "Once a year. I'd remember doing it four times."

**Annotation 13-6.** *Concluded:* this is the discovery of weakness **W-3** from the performer's side. Management's
documentation describes a quarterly user access review for Salesforce, Zuora, and NetSuite; the performer states
the review reached him once, in mid-year. The control as documented did not operate at the documented frequency,
which is a deficiency in operation, not a documentation defect — the documented frequency is the frequency
management asserted on. *Follow-up triggered:* (a) obtain the completed review documents for all four quarters
from Ray Sandoval and inspect the dates on their face rather than accepting either party's description; (b) obtain
the equivalent for Zuora and NetSuite, since a frequency failure in one application predicts the same failure in
the others; (c) determine how many quarters of the period of intended reliance are covered by a review at all;
(d) route to Chapter 11 for the ITGC conclusion and to Chapter 14 for the severity evaluation, since a failure of
periodic access review affects the reliance placed on every automated control in CPQ, including OTC-01 and
OTC-02. *Where the auditor should have pushed harder:* GRL should have asked BH to open his sent-mail and produce
the signed spreadsheet in the room. The team instead requested it through Ray Sandoval, and the completed
documents — which established that the Q2 2025 review was completed 41 days late and that no Q1, Q3, or Q4 review
existed — did not arrive until December 18, ten weeks later. Nothing was lost in this instance, but a
corroborating artifact requested while the interviewee is at the keyboard costs thirty seconds and a request
routed through a control owner costs weeks and arrives filtered.

**Q-7 (negative population).** *CJN:* "Roughly how often does Deal Desk send an order back to a rep because the
PDF and the CPQ record don't agree?"

*BH:* "Not often. A couple a month, maybe."

**Annotation 13-7.** *Concluded:* nothing yet — this is an estimate, and estimates by process owners about volumes
they do not personally count are unreliable. Its purpose is comparison. *Follow-up triggered:* obtain the Deal
Desk rejection log for July through September. The log showed 26, 31, and 38 rejections respectively, against an
estimate of "a couple a month." *Implication:* the divergence is not itself a finding about the control — a
rejection rate of 38 in a month with 173 orders means the control is working — but it is a finding about the
reliability of *this interviewee's* volume estimates, and it means every other volume figure obtained by inquiry
in this walkthrough must be corroborated to a system record before it is used.

**Q-8 (quarter-end variant).** *GRL:* "Take me through December 30 and 31. Does anything about this process work
differently in the last two days of a quarter?"

*BH:* "It's a war room. Deal Desk is on until the last signature comes in. If something lands at eleven at night
we'll activate it so it's in the quarter and Tessa validates it the next morning. Nobody's going to sit on a live
deal because the paperwork check hasn't happened yet."

**Annotation 13-8.** *Concluded:* OTC-03, a *preventive* control whose design depends on validation occurring
before activation, is inverted at quarter end for an unquantified subset of orders. The design conclusion in
Exhibit 13-8 therefore holds for the population outside the last two days of each quarter and does not hold
inside it — which is precisely the population where 41% of Q4 ACV ($25,174) sits. *Follow-up triggered:* (a)
extract activation timestamps and `Deal_Desk_Validated__c` timestamps for FY2025 and quantify the orders where
the flag postdates activation; (b) stratify the Chapter 14 test population so that the last five business days of
each quarter are tested separately rather than being sampled at their 8% share of the population; (c) record the
observation as a design limitation of OTC-03 on the deficiency log. *Comment:* one open question — "does anything
work differently at quarter end" — produced the most consequential answer in the interview. Ask it in every
walkthrough of every revenue process.

**Q-9 (fraud inquiry, AS 2401).** *GRL:* "Has anyone ever asked you to change a signature date, a start date, or
an activation date after the fact?"

*BH:* "Change it to what? People ask me to fix typos all the time. Nobody's ever asked me to backdate anything, if
that's what you mean."

**Annotation 13-9.** *Concluded:* the required inquiry was made of a person who processes revenue transactions and
the answer was recorded verbatim, including its structure — a clarifying question, then a denial narrower than the
question asked. *Follow-up triggered:* none in October. *Where the auditor should have pushed harder:* two things.
First, "fix typos all the time" is a volume assertion about edits to a financially relevant date field and it
should have been converted immediately ("how many, this quarter, and show me one"). Second, and more important,
the auditor had by this point established that (i) the signature date is editable by three roles, (ii) it is not
protected after activation, and (iii) the only control over it compares it to a document bearing the same date.
The missing question is the one in Exhibit 13-6: *is there any record of the execution date that a person inside
AtlasFlow cannot edit?* The answer — the DocuSign envelope completion timestamp — was on CJN's screen at Q-5. Had
that question been asked on October 7, the comparison of `Contract_Signed_Date__c` to envelope completion
timestamps for all 1,842 FY2025 orders could have been run in October rather than in January, when the
whistleblower allegation forced it (Chapter 17), and the six contracts that became uncorrected misstatement U-3
would have surfaced with three months of runway instead of three weeks.

### 13.9.2 Segment B — Jordan Pike, processing and recording

**Q-10 (open).** *GRL:* "Pick it up where Brett left off. The subscription exists in Zuora Billing. What happens
between there and revenue in the general ledger?"

*JP:* "Billing bills it — the bill run is nightly, invoices go out on the schedule in the subscription. Overnight
at two in the morning the connector pushes everything into RevPro, and RevPro does the 606 work: it identifies
the POBs, allocates, builds the schedule. Then at month end I pull the Revenue Contract Summary out of RevPro and
the interface posts the summary journal into NetSuite, and Elena approves it."

**Annotation 13-10.** *Concluded:* seq. 9 through 12 confirmed, and JP identifies the four artifacts that will
carry the audit: the bill run, the I-2 connector load, the Revenue Contract Summary report, and the monthly
journal. *Follow-up triggered:* who prepares and who approves — JP prepares, Elena Vasquez approves, which is the
segregation described in the continuing case and the segregation that weakness W-13 partially undermines because
the Controller can both prepare and post. Chapter 11 owns that.

**Q-11 (corroborative, artifact in the room).** *CJN:* "Open last night's I-2 reconciliation report. Then open
September 30's."

*JP:* [screen share] "September 30 had 14 exceptions. Most of them are amendments where the connector doesn't like
a date. Number nine here — that's a subscription where the rate plan charge came over with a zero amount, I
reopened it in Billing and re-pushed it the next night."

*CJN:* "Show me the re-push and the cleared status."

**Annotation 13-11.** *Concluded:* the control exists, produces a report with a count, generates an exception
list, and the performer can navigate to a specific item and demonstrate its resolution without preparation. That
is strong design evidence for OTC-07 against WCGW-8 and it is also *one* item of operating-effectiveness evidence
for a control that operates 251 times. *Follow-up triggered:* the aging question — "how long can an exception sit
open?" — answered "two days, usually same night," and the population question for Chapter 14: the exception log
export for the full period, with completeness tested by agreeing the report's record counts to the Billing and
Revenue record counts independently.

**Q-12 (probe on the accounting).** *GRL:* "Where does RevPro get the date revenue starts?"

*JP:* "Service start date off the subscription in Billing."

**Q-13 (probe).** *GRL:* "Your policy says revenue begins on the later of the contract start date and the date
the customer is provisioned. If provisioning runs late, how does RevPro know?"

*JP:* "There's a variance report I look at every month. If the dates don't line up I put a manual revenue start
date on the contract in RevPro."

**Q-14 (closed).** *GRL:* "What two dates does the variance report compare?"

*JP:* "The Zuora start date and the date on the order form. If the rep put March 1 on the order form and Billing
has March 15, that shows up and I look at it."

**Annotation 13-12.** *Concluded — and this is the pivotal exchange in the chapter.* The answer to Q-14 does not
answer Q-13. The documented control OTC-05 is a comparison of the billed service start date to the *provisioning*
date; what JP described is a comparison of the billed service start date to the *order form* date. Those are
different controls addressing different WCGWs. The comparison JP performs cannot detect WCGW-6 at all, because
neither of the two dates it compares is the date control of the service transferred. *Follow-up that was
triggered:* GRL noted "confirm OTC-05 report definition" as open item 7 on the walkthrough record and moved on.
*Where the auditor should have pushed harder — the whole point of this exhibit:* the next question was one
sentence long and was not asked. *"Show me the report."* Sixty seconds of screen share on October 7 would have
established that the Activation Variance Report contains no provisioning field, that the provisioning timestamp
is not replicated into Snowflake at all, and that the control described in management's documentation and
asserted on in its Section 404(a) assessment does not exist. Instead the open item sat, was reallocated when
staff rotated onto year-end fieldwork, and was cleared on December 10 — three weeks before year end — by the
walkthrough recorded in the case study below. Two costs followed: the interim control testing performed as of
October 31 was worthless and had to be voided, and the substantive procedure that ultimately identified corrected
misstatement C-1 ($410 of revenue recognized from March 15 rather than the April 2 provisioning date on 14 Q1
contracts) was performed under year-end time pressure. *Diagnostic to take away:* when an interviewee's answer
names different objects than your question named, the mismatch is the finding. Do not translate it into your own
words and do not write it down in your own words. Ask them to show you.

**Q-15 (fraud inquiry and close).** *GRL:* "Anyone ever ask you to hold a revenue adjustment, or to post
something you weren't comfortable with?"

*JP:* "Not post something, no. There's pressure on the close — we're supposed to have the schedule out by day
three and in Q1 that slipped and it wasn't fun. But nobody's asked me to change a number."

**Annotation 13-13.** *Concluded:* required inquiry made and recorded; the volunteered detail about close
timetable pressure is a risk assessment input (two revenue accountants resigned in Q2 2025 and the VP of Revenue
Accounting has been on a performance plan since March 2025) and was routed to the engagement team discussion
rather than developed here. *Follow-up triggered:* the day-3 deadline became a specific question in the close
walkthrough of October 14 (see the Step-by-Step Walkthrough below), where the FloQast sign-off timestamps make
timetable slippage measurable rather than anecdotal.

**Exhibit 13-12. Walkthrough findings and disposition, WP 3100-04 (October 7, 2025).**

| # | Finding | Source | Type | Disposition |
| --- | --- | --- | --- | --- |
| 1 | Approval tiers confirmed to configuration; OTC-02 designed effectively | Q-2, Q-5 | Design conclusion | Chapter 12 tests configuration; Chapter 14 tests operation |
| 2 | `Contract_Signed_Date__c` editable by three roles, including post-activation, with no downstream detection | Q-3, Q-4 | New WCGW-3(b), unaddressed | Deficiency log; fraud risk assessment (Chapter 17) |
| 3 | OTC-03 compares the CPQ date to a document bearing the same date; not independent | Q-5 + Exhibit 13-6 | Design deficiency (precision) | Deficiency log; substantive cut-off procedure designed |
| 4 | Salesforce access review performed annually, not quarterly (**W-3**) | Q-6 | Deficiency in operation of an ITGC | Chapter 11 conclusion; Chapter 14 severity; extend to Zuora and NetSuite |
| 5 | Inquiry-based volume estimates unreliable (2/month stated, 95/quarter actual) | Q-7 | Evidence quality | All volume figures corroborated to system records |
| 6 | OTC-03 validation follows activation at quarter end | Q-8 | Design limitation | Stratify Chapter 14 population; quantify from timestamps |
| 7 | OTC-05 as described by the performer does not address WCGW-6 | Q-13, Q-14 | **Open item — unresolved** | Cleared December 10; see the Extended Case Study |

## 13.10 Observation, Inspection, and Tracing a Transaction to the Financial Statements

Inquiry produces a description. Observation and inspection produce evidence, and they are what make a walkthrough
a procedure rather than a conversation. The practical rule: for every control in the matrix, the walkthrough
record must state at least one thing the auditor *saw*.

**Exhibit 13-13. What to observe and inspect during the order-to-cash walkthrough.**

| Control | Observe (the activity, live) | Inspect (the record it produced) | What it proves that inquiry does not |
| --- | --- | --- | --- |
| OTC-01 | Attempt to submit a quote with a blank term in a sandbox and watch the validation block | The validation rule definition | That the block exists and cannot be bypassed by the person who would want to bypass it |
| OTC-02 | Approval routing on a live quote at 28.4% discount | Approval record: approver user ID, timestamp, discount at approval | That routing is by rule and precedes order-form generation |
| OTC-03 | Tessa Brandt performing the five-attribute comparison on the next order in her queue | `Deal_Desk_Validated__c` with user and timestamp; the rejection log | That the comparison is five attributes, in that order, from those two sources |
| OTC-04 | Marcus Delgado opening the error queue at 8:40 a.m. and working the first item | Queue export with comments and resolution timestamps | That the queue is worked daily rather than at month end |
| OTC-07 | Jordan Pike navigating from the exception count to item 9 and its resolution | The September 30 reconciliation report and the cleared exception | That the report exists, produces exceptions, and the performer can use it unrehearsed |
| OTC-08 | Elena Vasquez's review of the monthly journal in NetSuite and FloQast | Journal `RP-2025-09-01`, the Revenue Contract Summary, the FloQast sign-off | That the approval precedes posting, which the journal's own audit trail settles |

Two practical notes on observation. First, observation evidences that the activity occurred while you watched,
which is why AS 1105's ranking treats it as weaker than inspection for concluding on a period; its value in the
walkthrough is that it exposes steps the description omitted — the second screen the performer opens, the
spreadsheet on the side, the colleague they ask. Second, when the process is nonrecurring or seasonal (the
quarter-end war room in Annotation 13-8), you cannot observe it in October at all. Say so in the workpaper and
substitute inspection of the artifacts from the last occurrence.

**Tracing** is the spine of the walkthrough. Trace forward, from the source document to the financial statement
line, to test completeness and to see the whole flow; trace backward, from a recorded amount to its source, to
test occurrence. In a walkthrough you trace forward, and one transaction is enough.

**Exhibit 13-14. Forward trace, contract C-1 Meridian Health Systems, origination to financial statements (in
thousands).**

| Seq. | Artifact obtained | Key fields and values | Tied to |
| --- | --- | --- | --- |
| 1 | CPQ quote `Q-41022` | Term 36 months; start 03/15/2025; Core ramp 600 / 840 / 960; Insight 180 in years 2–3; implementation 360 | Order form |
| 3 | Approval record | Approver: S. Marchetti, 03/11/2025 10:52 CT; aggregate discount 26.4%, above the 25.0% tier boundary and therefore routed to the CRO | Approval matrix, Exhibit 13-3 |
| 5 | Executed order form PDF; DocuSign envelope `9F2C-…-4471` | Signature date 03/12/2025; envelope completed 03/12/2025 15:08 CT; total contract value 3,120 | CPQ record: 600 + 840 + 960 (Core ramp) + 180 + 180 (Insight, years 2–3) + 360 (implementation) = 3,120 (a) |
| 6 | `Deal_Desk_Validated__c` | TRUE, T. Brandt, 03/13/2025 08:31 CT | Five-attribute comparison |
| 7 | Zuora subscription `A-S27194` | Service start 03/15/2025; rate plan charges: Core annual 600, implementation 360 | I-1 transfer log, no error-queue entry |
| 8 | Platform `provisioned_at` | **04/02/2025 09:14 CT** | — (b) |
| 9 | Invoices `INV-104882` (600, subscription) and `INV-104883` (180, implementation 50%) | Invoice date 03/12/2025; due 04/11/2025 | AR subledger, account 1200 |
| 11 | RevPro revenue contract `RC-88317` | Four performance obligations; revenue start **03/15/2025** | Revenue schedule lines |
| 12 | Journal `RP-2025-03-01`, line detail | Core revenue for March allocated from 03/15/2025 | Accounts 4100, 4110, 2400, 2410 |
| FS | Consolidated statement of operations, subscription revenue 135,800 | C-1's contribution is included in the 4100 balance of 104,900 | Trial balance to financial statements |

Tick marks: (a) the allocation of the $3,120 transaction price across four performance obligations is Chapter 5,
§5.7; this trace tests the *dates and terms* that feed the allocation, not the allocation itself. (b) The
provisioning date is 18 days after the revenue start date recorded in RevPro. This single cell is the finding.
Under AtlasFlow's own policy (continuing case §4.1) revenue begins on the later of the contract start date and
the provisioning date, so revenue on C-1 began 18 days early. C-1 was one of the 14 Q1 contracts that produced
corrected misstatement C-1 of $410.

The trace found the misstatement on October 7 and nobody noticed, because `provisioned_at` was recorded in the
workpaper as a data point rather than compared to the revenue start date. That is the argument for the two-column
discipline in the trace exhibit: every row must state what the value was **tied to**, and a row with a blank in
that column is an unexamined fact.

**Exhibit 13-15. Trace workpaper header, WP 3100-04E.**

```text
WP 3100-04E   TRANSACTION TRACE — ENTERPRISE ORDER-TO-CASH
Item traced:  C-1 Meridian Health Systems / Q-41022 / A-S27194 / RC-88317.
Selected:  judgmentally, as a multi-element contract with a ramp, an Insight
          component, and a services component (i.e. exercising the maximum number
          of configuration rules). NOT a representative selection; supports the
          understanding and design evaluation only (see §13.2).
Performed by: C. Nwosu (CJN) 10/07/2025.  Reviewed: G. Lindqvist (GRL) 10/13/2025.
Exceptions:  provisioned_at 04/02/2025 vs RevPro revenue start 03/15/2025.
             Open item 7 at .04F.  (See WP 3100-09 and WP 8400-11.)
```

## 13.11 Undocumented Controls and Controls That Do Not Exist

Two asymmetric discoveries come out of walkthroughs, and they have opposite consequences.

An **undocumented control** is an activity the auditor observes that mitigates a WCGW but appears nowhere in
management's documentation. Finding one is good news for the process and a problem for management's Section 404(a)
assessment: management cannot assert on a control it has not identified, and if the auditor's conclusion depends
on that control, management's documentation is incomplete — which is itself a deficiency in the control
environment and in the monitoring component. The auditor may still rely on the control. The auditor must tell
management it exists.

A **control that does not exist as documented** — informally a *phantom control* — is a documented control that
either is not performed, is performed at a lower frequency, is performed by someone without the authority or
information to perform it, or is performed on different objects than the documentation describes. It is a
deficiency, and the fact that management's documentation describes it is what makes it one: the documented control
is the control management asserted on, and Principle 12 of the COSO framework treats the deployment of the policy
through actual procedures as part of the control, not as commentary on it.

**Exhibit 13-16. Dispositions, AtlasFlow FY2025.**

| Observation | Category | Consequence for management | Consequence for the audit |
| --- | --- | --- | --- |
| Marcus Delgado emails the Revenue Manager a list of subscriptions activated with a start date more than 30 days in the past; not in any control matrix | Undocumented control (detective, partial) | Add to the control population or stop relying on it; documentation gap reported | May be relied on if tested; population completeness must be established, and the 30-day parameter analyzed for precision |
| Access review performed annually against documented quarterly frequency (**W-3**) | Phantom frequency | Deficiency; remediation required; frequency in the documentation cannot simply be edited to "annual" retrospectively | ITGC deficiency (Chapter 11); affects reliance on automated controls; severity in Chapter 14 |
| OTC-05 compares the billed start date to the order-form date, not to the provisioning date | Phantom control | Design deficiency; the WCGW is unaddressed for the full year | Interim testing voided; substantive cut-off procedure required; see the case study |
| "Segregation of duties is maintained between sales and billing" | Not a control at all | Replace with the role configurations that achieve it | Nothing to test; test the configurations instead |

The instinct to let management "correct the documentation" is the error to avoid. Where the practice is better
than the documentation, correcting the documentation is right. Where the practice is *weaker* than the
documentation, editing the documentation to match practice converts a deficiency into a design that leaves the
WCGW unaddressed — a different deficiency, not the absence of one. Say which of the two you are looking at, in
writing, before management redlines anything.

## 13.12 The Annual Refresh Versus the Full Re-Walkthrough

In a recurring engagement the question each year is whether to refresh last year's understanding or rebuild it.
Refreshing means confirming that the documented flow and control set are unchanged, corroborating the confirmation
against evidence, and updating for identified changes. Rebuilding means performing the walkthrough as though for
the first time, with a fresh trace. There is no professional requirement to do one or the other; AS 2201 requires
the understanding to be current and sufficient, and firm methodologies convert that into rotation policies. What
is *not* acceptable in either case is confirming the prior-year narrative by inquiry of a control owner and
signing it.

**Exhibit 13-17. Criteria for a full re-walkthrough.**

| Indicator | Present at AtlasFlow FY2025? | Effect |
| --- | --- | --- |
| First year of ICFR auditor attestation | Yes — EGC status lost at 12/31/2025 | Decisive on its own; there is no prior-year auditor understanding to refresh |
| System implementation, upgrade, or migration affecting the process | Yes — NetSuite upgraded September 2025 with SoD roles rebuilt; RevPro configuration changed February 2025 | Full re-walkthrough of the affected sub-processes |
| Change in the personnel who perform the control | Yes — two revenue accountants resigned in Q2 2025; new CFO September 2025 | Re-walk with the new performer; do not carry forward the prior performer's description |
| Business combination integrated into the process | Yes — Kestrel contracts migrated into Zuora October 2025 | Walk the migrated population separately, even where scoped out of the 404(a) assessment |
| Prior-year deficiency in the process | Yes — 14 gaps in the July 2025 readiness assessment | Re-walk; a refresh cannot evidence remediation |
| Significant risk at the assertion level affected by the process | Yes — revenue cut-off | Re-walk annually as a matter of policy |
| None of the above; stable process, stable people, stable systems, no deficiencies | — | Refresh is defensible: confirm with the performer, inspect one current artifact per control, document the change analysis, and trace one transaction if the process touches a significant risk |

A refresh that is done properly still contains a trace and still contains inspection. The distinguishing feature
of a refresh is not that less evidence is obtained about the current period; it is that the *structural* work —
the flow, the IAPR map, the WCGW inventory — is carried forward and challenged rather than rebuilt.

## 13.13 Documenting the Walkthrough So a Reviewer Can Evaluate It

AS 1215 sets the standard: an experienced auditor with no previous connection to the engagement must be able to
understand the nature, timing, extent, and results of the work, who performed it and when, and the conclusions
reached. For a walkthrough that means the reviewer must be able to answer six questions from the workpaper alone:
who was interviewed and what is their role relative to the control; what was asked; what was seen; which facts
came from inquiry and which from inspection; which WCGWs are addressed and which are not; and what is unresolved.
The last is the one most often omitted, and it is the one that failed at AtlasFlow.

**Exhibit 13-18. Walkthrough record, WP 3100-04F (completed).**

```text
WP 3100-04F   WALKTHROUGH RECORD — ENTERPRISE ORDER-TO-CASH
Process: Order-to-cash, enterprise and mid-market channel (excludes self-serve;
         see WP 3100-05 for the Stripe channel).
Objectives addressed:  [X] understanding of the process (AS 2110)
                       [X] design effectiveness of controls OTC-01 to OTC-09
                       [ ] operating effectiveness — NOT addressed; see WP 3400
Date and place: 10/07/2025, 09:05–10:40 CT, AtlasFlow Austin HQ, with screen share.
Auditor attendees: G. Lindqvist (GRL), C. Nwosu (CJN).
Client attendees and role relative to the controls:
   B. Hallowell, VP Sales Operations — OWNER of OTC-01/02/03; PERFORMER of the
     Salesforce access review response; CPQ system administrator.
   J. Pike, Revenue Manager — PERFORMER of OTC-07 and of the control documented
     as OTC-05; preparer of the I-3 journal.
   T. Brandt, Deal Desk Analyst — PERFORMER of OTC-03; joined 10:05–10:25 for
     observation of the five-attribute comparison on order Q-48226.
   Not interviewed: M. Delgado (PERFORMER of OTC-04) — interviewed separately
     10/09/2025, WP 3100-06; R. Sandoval (OWNER, access reviews) — WP 4100-02.
Inquiry record: 15 questions and answers transcribed at .04G, including the
   AS 2401 fraud inquiry of both interviewees (answers recorded verbatim).
Observed:  (1) validation block on a quote with blank term (sandbox);
           (2) approval routing and approval record on Q-48117;
           (3) T. Brandt performing OTC-03 on Q-48226 (5 attributes, 2m 40s);
           (4) J. Pike navigating the 09/30 I-2 reconciliation to exception 9.
Inspected: Q-48117 approval record and field history; DocuSign envelope; Deal
           Desk rejection log Jul–Sep 2025 (26 / 31 / 38); I-2 reconciliation
           reports 09/30 and 10/06; C-1 trace artifacts at .04E.
Facts from inquiry only (not corroborated as of this date): access review
           frequency (Q-6); post-activation edit capability (Q-4); quarter-end
           activation-before-validation practice (Q-8); OTC-05 report contents
           (Q-14).
Design conclusions: OTC-01, OTC-02, OTC-03 (as to WCGW-1 and WCGW-4), OTC-04,
           OTC-07, OTC-08, OTC-09 (as to individually material credits) are
           suitably designed. NOT suitably designed: OTC-03 as to WCGW-3
           (precision — no independent date attribute); OTC-09 as to WCGW-10 in
           aggregate. UNADDRESSED WCGWs: WCGW-3(b), WCGW-6 (pending item 7).
OPEN ITEMS (owner / due):
   1. Obtain completed access reviews, 4 quarters, 3 applications (CJN / 10/17)
   2. Post-activation date-edit report, FY2025 (CJN / 10/21)
   3. Activation vs validation timestamp extract (B. Osei / 10/24)
   4. Deal Desk rejection log Oct–Dec (A. Trent / 01/09)
   5. Error queue export, full period (B. Osei / 11/07)
   6. Credit memo population and threshold analysis (A. Trent / 11/14)
   7. OBTAIN AND INSPECT THE ACTIVATION VARIANCE REPORT USED FOR OTC-05;
      CONFIRM WHICH TWO DATES IT COMPARES (GRL / 10/24)   <-- see WP 3100-09
Prepared by CJN 10/08/2025.  Reviewed by GRL 10/13/2025.  Partner: DGW 10/20/2025.
```

Open item 7 is reproduced as it appeared in the file, because the failure it records is not a documentation
failure. The item was written down, assigned, and dated. It was not cleared by its due date, was not escalated
when the staffing changed on November 3, and was closed on December 10. A walkthrough workpaper's open-items list
is a control over the audit, and like any control it needs a performer, a frequency, and a disposition.

## 13.14 Walkthroughs of Remote and Offshore Processes

AtlasFlow India Private Limited employs 99 people and performs no external revenue transactions, but the Bengaluru
team performs three activities inside the financial reporting chain: invoice quality review before bill runs, cash
application to the receivable subledger, and the first-level preparation of five balance sheet reconciliations
loaded into FloQast. A process performed 8,700 miles away by people you have never met is not a different process,
but the walkthrough of it is a different procedure, because the two techniques that carry the most weight —
observing the activity and watching an unrehearsed navigation — are the two that degrade most over a video link.

**Exhibit 13-19. Designing the offshore walkthrough (AtlasFlow India, cash application and reconciliation
preparation; the India roles are an extension of the continuing case).**

| Degradation | Why it happens remotely | Compensating procedure |
| --- | --- | --- |
| You cannot see the second screen, the side spreadsheet, or the colleague being asked | Camera framing; the performer controls what you see | Require full-desktop share, not window share; ask the performer to open every application they touch, in sequence, and name each |
| The interview becomes rehearsed | Time-zone scheduling means the agenda is circulated in advance and pre-walked with a manager | Send the process scope, not the questions; select the transaction to trace during the call from a population you extracted yourself |
| The wrong person appears | The local manager attends and answers on the performer's behalf | State by name and role who must be present; if a manager answers a performer's question, ask the performer to repeat it in their own words |
| Handoffs to the US team are invisible | Each side describes its own half and assumes the other | Walk the handoff explicitly: which report, sent how, at what time, and what the US recipient does if it does not arrive |
| Local-language documentation and screens | Screens and comments may not be in English | Request a translated screenshot and record that the translation is management's |
| Segregation assumptions do not hold | A three-person team covers roles a US chart assumes are separate | Obtain the local role assignment and the leave-cover arrangement; ask who performs each step when one of three is on leave |

Two further points. Time zones make the observation of a live activity expensive but not impossible: the Bengaluru
cash application run happens at 08:00 IST, which is 20:30 CT the previous evening, and one 45-minute evening call
in September is worth more than three daytime discussions. And where the offshore team performs part of a control
whose conclusion covers the whole, the walkthrough must cover both halves in the same workpaper; splitting them
across two files is how a handoff gap survives an audit.

## 13.15 Walkthroughs of Automated Processes and Vendor-Hosted Configuration

Some of AtlasFlow's most important controls have no performer to interview. The 27 RevPro configuration rules
allocate transaction price without human intervention. The I-1 field mapping runs on an API. The CPQ approval
matrix is a table of thresholds. The Stripe-to-NetSuite Lambda job (I-4, weakness W-7) is 340 lines of in-house
Python running on a schedule. And the applications are vendor-hosted: AtlasFlow cannot see Zuora's code, its
change tickets, or its database.

The walkthrough does not disappear; four of its elements are substituted.

**Exhibit 13-20. Substitutions for the automated and vendor-hosted walkthrough.**

| Element of a manual walkthrough | Substitute for an automated control | Substitute for vendor-hosted configuration you cannot see |
| --- | --- | --- |
| Inquiry of the performer | Inquiry of the person who *configured* it and the person who *monitors* its output — for RevPro, Daniel Kim (configuration) and Jordan Pike (output) | Inquiry of the entity's administrator about what is configurable versus what the vendor controls; the boundary is the scope of your work |
| Observation of the activity | Observation of a transaction processed through the rule in a test or sandbox instance, with inputs you choose | Not available; substitute the service auditor's description of the system in the SOC 1 report (AS 2601, AU-C 402) |
| Inspection of the evidence of operation | Inspection of the configuration itself: the rule table, the mapping, the threshold, the code, and the deployment record | Inspection of the entity's configuration screens and of the vendor's SOC 1 report, its period, and any bridge letter (weakness W-9: none obtained for Zuora or Deel for October–December 2025) |
| Re-performance | A test of one: process an input through the rule and recompute the expected output independently. Valid only if the ITGCs supporting the application are effective — see Chapter 12, §12.8, and note that at AtlasFlow they are not (weaknesses W-1, W-3, W-6) | Mapping of the CUECs in the vendor's report to the entity's own controls (weakness W-10: not performed) |

Three cautions specific to this environment. First, a screenshot of a configuration screen dated the day you asked
for it evidences the configuration on that day and nothing about January through September; the configuration
change record, not the screenshot, is what evidences stability, and the change record is an ITGC matter
(Chapter 11). Second, continuous-compliance tools generate attractive artifacts — management offered Vanta
screenshots during the FY2025 audit — and a Vanta dashboard is information produced by the entity whose
completeness and accuracy is untested until you test it; it is not a control and it is not a service auditor's
report. Third, the walkthrough of an automated process should still produce an IAPR map, because the interesting
question is almost always where a human *can* intervene: for RevPro, two developers hold standing write access to
the production configuration (weakness W-6), and that fact belongs in the process understanding even though there
is no activity to observe.

## Step-by-Step Walkthrough: The Financial Close Walkthrough with Elena Vasquez in FloQast

This is the FY2025 walkthrough of AtlasFlow's monthly financial close, performed on **October 14, 2025** with
Elena Vasquez, Chief Accounting Officer and Controller, covering the September 2025 close (completed on business
day 8, October 10, 2025). Workpaper reference **WP 3120-02**. Performed by Grace Lindqvist (GRL) and Chris Nwosu
(CJN); IT audit senior Ben Osei (BXO) attended for steps 11 and 13. The objectives are the understanding of the
close process and the design evaluation of the close controls. Operating effectiveness is not addressed; Chapter
14's walkthrough tests the Controller's review of the RevPro-to-GL journal as a management review control.

**Step 1. Obtain the close calendar and the FloQast task list before the meeting.** Request the September 2025
FloQast close checklist export with columns: task ID, task name, assignee, reviewer, due business day, completed
timestamp, reviewed timestamp, and control flag. You obtain 214 tasks, of which 41 are flagged by management as
controls. Compare the 41 to management's close-process control matrix, which lists 37. The difference is your first
inquiry: either FloQast contains four controls management has not asserted on, or the matrix contains controls the
close does not perform.

**Step 2. Establish that the task list is the complete population.** Ask who can add, delete, or reopen a task and
whether deletion is logged. Obtain the FloQast administrator list (three users: Vasquez, Pike, and a systems
accountant) and the September task-deletion log (two deletions, both duplicates), and compare the task count to
the prior two months (211 in July, 213 in August). If deletions are not logged, the population is unestablished and
every conclusion drawn from FloQast sign-off dates is unsupported — stop and address it, because those dates are
the evidence for most close controls.

**Step 3. Select the month and the specific artifact to walk.** Choose September 2025: it is the most recent
completed close, it follows the September NetSuite upgrade, and it is inside the period of intended reliance.
Choose journal **RP-2025-09-01**, the monthly RevPro-to-GL revenue journal (interface I-3), as the transaction to
trace, because it is the single recording point for $135,800 of annual subscription revenue. Tell Vasquez in
advance which month, and do not tell her which journal.

**Step 4. Open the interview with the funnel question.** Ask: "Take me through your September close from the last
day of the month to the day you closed the books, and tell me what you personally did." You obtain her sequence,
her vocabulary ("the flux," "the binder," "day three revenue"), and — critically — the list of things she does
personally, which is the boundary between the controls she performs and the controls she owns. Record the personal
list verbatim; it is the population for step 6 onward.

**Step 5. Reconcile the stated timetable to the actual sign-off timestamps.** Ask for the target close day, then
compare her answer to the FloQast export you obtained in step 1.

**Exhibit 13-21. September 2025 close: target versus actual (from the FloQast export, WP 3120-02A).**

| Task | Task name | Target BD | Actual completion | Actual review sign-off | Variance |
| --- | --- | --- | --- | --- | --- |
| CL-101 | Bank reconciliations, 7 accounts | BD 2 | 10/02/2025 16:41 | 10/03/2025 09:20 | On time |
| CL-210 | RevPro-to-GL journal prepared (J. Pike) | BD 3 | 10/06/2025 18:52 | — | **1 day late** |
| CL-215 | RevPro-to-GL journal reviewed and approved (E. Vasquez) | BD 3 | — | 10/07/2025 07:44 | **2 days late** |
| CL-305 | AR aging, allowance roll-forward | BD 4 | 10/06/2025 15:10 | 10/07/2025 11:05 | On time |
| CL-410 | Consolidation workbook, FX translation, top-side entries | BD 6 | 10/09/2025 21:33 | 10/10/2025 08:15 | On time |
| CL-500 | Flux analysis versus forecast and prior month | BD 7 | 10/09/2025 22:04 | 10/10/2025 08:47 | On time |
| CL-610 | Close binder complete; period locked in NetSuite | BD 8 | 10/10/2025 17:26 | 10/10/2025 17:29 | On time |

Conclusion supported: the close operates on the timetable described, with the revenue journal two days late — the
same slippage Jordan Pike volunteered in Annotation 13-13. If the review sign-off had preceded the preparation
timestamp, that is not a variance but a contradiction, and it means the sign-off is a formality; go to step 9
immediately and inspect the NetSuite audit trail rather than the FloQast dates.

**Step 6. Walk one reconciliation sign-off end to end.** Select the account 2400 deferred revenue reconciliation.
Ask who prepares it, who reviews it, what the reviewer compares, and what happens to an unexplained difference.
Obtain the September reconciliation PDF from the FloQast attachment and the two sign-off stamps, and compare the
reconciled balance to the trial balance ($63,140 at September 30, an extension for this illustration; $66,800 at
December 31, 2025). If a reconciliation is signed with an unexplained difference recorded as "immaterial," obtain
the threshold at which the reviewer would not sign; "immaterial" is not a criterion, and the answer is the
precision of the control.

**Step 7. Obtain the criteria for the Controller's review of the revenue journal (OTC-08).** Ask, in this order:
what do you receive; what do you compare it to; what specifically would make you send it back; and how much would
have to be wrong before you noticed. Vasquez's answers: she receives the journal and the RevPro Revenue Contract
Summary; she compares each revenue account to a rolling expectation she builds from beginning ARR plus signed new
ACV, and to the prior month; she investigates any account whose variance to her expectation exceeds **the greater
of $250 and 2%**. Record the number. A review with no number is a review with no precision (§13.7).

**Step 8. Observe the review being performed on the selected journal.** Ask her to do it now, on
RP-2025-09-01, while you watch, and record every artifact she opens. She opens: the journal in NetSuite, the
Revenue Contract Summary in RevPro, her own expectation spreadsheet, and the I-2 exception log. What you learn from
watching rather than asking: she checks the RevPro report's parameter dates before using it, which is an IPE
control nobody had documented (see §13.11).

**Exhibit 13-22. Journal RP-2025-09-01 as inspected (in thousands; monthly amounts are an extension consistent
with continuing case §3.1).**

| Account | Description | Debit | Credit |
| --- | --- | --- | --- |
| 2400 | Deferred revenue — subscription, current | 11,530 | |
| 1220 | Unbilled receivables / contract assets | 375 | |
| 4100 | Subscription revenue — Core | | 9,050 |
| 4110 | Subscription revenue — Insight | | 2,480 |
| 4120 | Usage overage revenue | | 375 |
| | **Total** | **11,905** | **11,905** |

**Step 9. Inspect the journal's own audit trail in NetSuite, not the FloQast sign-off.** Obtain the system fields
`created_by`, `created_date`, `approved_by`, `approved_date`, `posted_by`, `posted_date` for RP-2025-09-01.
Compare the approval timestamp to the posting timestamp: approval must precede posting or the control is
after-the-fact. You find approval by E. Vasquez at 10/07/2025 07:44 and posting by E. Vasquez at 10/07/2025 07:46.
Conclusion: the approval precedes posting, but the same person approves and posts — weakness **W-13**, already
identified in the July 2025 readiness assessment, now corroborated by inspection. If the posting timestamp had
preceded the approval, the control does not operate as designed and the design conclusion fails on its face.

**Step 10. Test the precision of the review arithmetically.** Vasquez's threshold is the greater of $250 and 2%.
On the September journal, 2% of the $9,050 Core line is $181, so the binding threshold on that line is $250; on the
$375 usage line it is $250. Compare the threshold to performance materiality of $940: a misstatement of $940 in any
single revenue account would exceed her threshold and be investigated, so the control's precision is sufficient
for the accuracy assertion at the account level. Compare it also to the aggregate: a $200 error in each of the
three revenue lines is $600 and passes. Conclusion: sufficient precision for individually material errors,
insufficient for compensating or spread errors — record both, and let Chapter 14 decide the extent of testing.

**Step 11. Walk the IPE.** Ask where the Revenue Contract Summary comes from, who can run it, what parameters it
takes, and whether the parameters print on the report face. Obtain a copy showing the parameter block (period
09/2025, all legal entities, all revenue contracts, include unposted = No), and compare the report total to the
journal total: $11,905 to $11,905. If the parameters do not print, the report is not self-evidencing and the only
control over the IPE is the person who ran it — the preparer. Chapter 12, §12.10 owns report testing.

**Step 12. Walk the consolidation and top-side step.** Ask Vasquez to open **CONSOL_FY25_v14.xlsx** on SharePoint.
Obtain the FX rate tab and its source, the intercompany elimination tab, and the top-side entry tab (27 entries
totaling $6,200 of absolute value for FY2025), and compare the workbook's consolidated revenue to the NetSuite
consolidated trial balance. Ask who else has edit access and how a formula change would be detected. The answer —
four people, emailed among them, no version control, no formula-integrity check — is weakness **W-8**; the
walkthrough's contribution is to establish that the workbook sits between the ledger and the financial statements
rather than beside them.

**Step 13. Walk the journal entry approval configuration as it applies to close entries.** With Ben Osei present,
have Vasquez post test journals below and above $250,000 in the sandbox, and obtain the approval routing
configuration. Compare to the population: of 4,912 FY2025 manual entries, 3,847 were below the threshold and carry
no evidence of independent review (weakness **W-12**). Conclusion: the close depends on the reconciliation and flux
controls to detect errors in sub-threshold entries, which makes the step 10 precision analysis load-bearing.

**Step 14. Walk the flux analysis and the close binder sign-off.** Obtain the September flux file and ask which
variances she investigated and what she did. She investigated three: usage overage revenue up 16.0% month over
month, hosting cost up 9%, accrued commissions up 11%. Obtain her documented explanation for the usage variance and
compare it to the Q4 usage trend the team is separately analyzing ($1,090 in Q3 to $1,390 in Q4). If the file flags
variances and records no disposition, the control is a preparation step and not a review.

**Step 15. Ask the exception, quarter-end, and fraud questions.** In order: the largest post-close adjustment this
year and its cause; what happens differently in the year-end close; who closes the books when she is on leave;
whether anyone has asked her to record or not record something she was uncomfortable with; and — the question
Jordan Pike's answer generated — what slipped in the Q1 close and why. Record the answers verbatim. Vasquez's
answer to the leave question ("nobody — I have not taken the last two closes off") is the single-point-of-failure
fact in the continuing case and belongs in the control environment assessment (Chapter 2), not here.

**Step 16. Complete the record, evaluate design, and hand off.** Within two business days complete WP 3120-02 using
the Exhibit 13-18 template. Route each finding: W-8, W-12, and W-13 to the ITGC and entity-level files (Chapters 11
and 12); the OTC-08 precision analysis to Chapter 14's test design; the undocumented IPE parameter check to
management as a documentation gap; and the two-day revenue journal delay to the engagement team discussion as a
risk indicator. If any close control's design conclusion is "deficient," notify the manager the same day — three
weeks of the interim testing window can be lost while a finding sits in a draft workpaper, which is the subject of
the case study that follows.

## Extended Case Study: The Control That Did Not Exist — OTC-05 and the December 10 Walkthrough

### Background

Brightline's FY2025 controls strategy tested the revenue-cycle controls as of an interim date of **October 31,
2025**, with a roll-forward to December 31. Management's control documentation, prepared with the co-sourced
internal audit function during the July 2025 readiness assessment, described control **FIN-REV-07** (the audit
team's OTC-05) as follows:

> "Monthly, the Revenue Manager compares the subscription service start date recorded in Zuora Billing to the
> provisioning-complete date recorded in the AtlasFlow platform for all subscriptions activated during the month
> and records a manual revenue start date in Zuora Revenue where provisioning occurred after the contract start
> date."

The control is the only control mapped to WCGW-6 in Exhibit 13-8, and WCGW-6 is a cut-off WCGW on the account
that carries the presumed fraud risk. The October 7 walkthrough left open item 7: obtain and inspect the report
Jordan Pike said he used. The item was due October 24. Staff rotated onto year-end planning on November 3 and the
item was not reassigned.

### The Facts

On **December 10, 2025** — 21 days before year end — Grace Lindqvist cleared open item 7 in a 25-minute session
with Jordan Pike. The facts established, in the order they emerged:

1. The report Pike uses is the **Activation Variance Report**, a Snowflake view named `vw_activation_variance`,
   refreshed hourly through the I-8 Fivetran pipeline.
2. The view compares two columns: `zuora_subscription.service_start_date` and
   `salesforce_order.service_start_date__c`. It has 14 columns and none of them is a provisioning date.
3. The AtlasFlow platform's `provisioned_at` timestamp lives in the production application database. That
   database is not one of the sources Fivetran replicates into Snowflake, so the provisioning date is not
   available to Pike in any report and never had been. Confirmed the same day with Ray Sandoval.
4. Pike had never seen the text of FIN-REV-07. Asked what he understood the purpose of his monthly check to be,
   he said: "Making sure Billing has the same start date as the order form. If provisioning is late, honestly, I
   wouldn't know."
5. Interim testing at **WP 3400-12**, performed on November 6 by staff, had selected three months (March, June,
   September) from the ten-month interim population, obtained the Activation Variance Report for each, agreed the
   exceptions listed to Pike's dispositions, and concluded "no deviations noted." The attribute tested was
   "variance report reviewed and exceptions dispositioned." The attribute in the control description — comparison
   to the provisioning date — was never tested, and no one had noticed that the report inspected could not
   support the control described.

### What the Engagement Team Did

Same day: Lindqvist notified Omar Haddad and Dana Whitcombe, and asked Farrah Nazari to confirm independently
whether any AtlasFlow report contained a provisioning date (answer: only the platform admin console, one tenant at
a time, and a Postgres query available to two engineers).

December 11: the team met Elena Vasquez and Daniel Kim. Kim's position was that the documentation was "written
loosely" and that the intent had always been the order-form comparison; he offered to re-document FIN-REV-07 to
describe what Pike does. The team's response was that re-documenting changes which deficiency is reported and does
not eliminate one: if the control is as documented it did not operate for twelve months, and if it is what Pike
performs it cannot detect WCGW-6. Either way the deficiency exists as of December 31, 2025.

December 11–12: the team **voided WP 3400-12**. There is no roll-forward of a test of a control that does not
exist. The revenue-cycle control reliance assumption was withdrawn, changing the planned extent of substantive
cut-off testing. December 15–19: Tara Iyer obtained `provisioned_at` for all FY2025 subscription activations by
direct query of the platform database, reconciled the record count to the Zuora activation population, and compared
each to the RevPro revenue start date.

**Exhibit 13-23. Results of the full-population provisioning-date comparison (in thousands).**

| Category | Subscriptions | FY2025 revenue effect |
| --- | --- | --- |
| Provisioning on or before the revenue start date | 992 | — |
| Provisioning 1–3 days after the revenue start date | 187 | 41 |
| Provisioning 4–14 days after the revenue start date | 13 | 23 |
| Provisioning more than 14 days after the revenue start date (March 2025 provisioning backlog) | **14** | **410** |
| **Total activations requiring new provisioning** | **1,206** | **474** |

The 14 contracts in the last row are the 14 Q1 contracts of corrected misstatement C-1: revenue recognized from
March 15, 2025 rather than from the April 2, 2025 provisioning date, overstating FY2025 revenue and understating
deferred revenue by $410. Contract C-1, Meridian Health Systems, is one of the 14 — the same contract the
October 7 trace had walked (Exhibit 13-14), where `provisioned_at` of April 2 sat in the workpaper next to a
revenue start date of March 15 and was not compared to it. The residual $64 across the 200 contracts in the
middle two rows was evaluated against the $72 clearly trivial threshold and not accumulated.

### Analysis

Three questions had to be answered, and only the first has a clean answer.

**Is this a design deficiency or an operating deficiency?** Both descriptions are available and the team documented
it as a **design deficiency**, because the conclusion that matters is that WCGW-6 was unaddressed throughout
FY2025. Framing it as an operating failure of FIN-REV-07 would imply that reinstating the documented frequency
would fix it, and it would not: the data the documented control requires exists in no report.

**Can the interim testing be salvaged?** No. A test of controls is a test of a defined attribute over a defined
population, and the attribute tested at WP 3400-12 belonged to a different control. Even had it been the right
attribute, a control cannot be tested for operating effectiveness before it has been established to be suitably
designed. The three months of work were re-purposed as evidence about the *order-form* comparison, which addresses
WCGW-4, where OTC-03 already existed and reliance did not depend on it.

**How severe is it?** Chapter 14 owns the grading, and the honest answer at December 19 was a range from
**significant deficiency to material weakness**. Against severity: the actual misstatement of $474 is below
performance materiality of $940 and management corrected it. Toward severity: the magnitude that could have arisen
is not bounded by what did arise, since a provisioning backlog like March 2025's in a larger quarter scales
proportionally; the deficiency existed for the entire period; it was identified by the auditor rather than by
management, three weeks before year end, which is an indicator weighed under the AS 2201 framework; and it
aggregates with the other revenue cut-off deficiencies — the OTC-03 precision failure and quarter-end inversion
(Exhibit 13-12, findings 3 and 6) and the six December contracts of uncorrected misstatement U-3. Aggregated, the
team concluded a **material weakness in controls over revenue cut-off**, the weakness described in the adverse ICFR
opinion drafted in Chapter 20. What would have moved it the other way: a compensating detective control of
sufficient precision over the same WCGW — a monthly reconciliation of provisioned tenants to billed subscriptions,
which did not exist — or evidence that the exposure was structurally limited, which the March backlog contradicts.

### Resolution and Conclusion

Management recorded the $410 adjustment (corrected misstatement C-1). Management revised the FIN-REV-07 control
description, implemented a manual comparison of a provisioning extract to RevPro revenue start dates for Q4
activations (performed December 22, 2025 and January 12, 2026), and added the platform database to the Fivetran
replication scope in Q1 2026. The team concluded that a control implemented in the last three weeks of the period
could not, on the evidence available, support a conclusion that ICFR over revenue cut-off was effective as of
December 31, 2025. The deficiency was communicated in writing to the audit committee on December 18, 2025 and in
the final AS 1305 communication, and it is aggregated at WP 8400-11.

### Workpaper Extract

```text
================================================================================
BRIGHTLINE LLP                                              WP REF:  3100-09
AtlasFlow, Inc.                                             PERIOD:  FY2025
Audit of the financial statements and of ICFR               YEAR END: 12/31/2025
--------------------------------------------------------------------------------
SUBJECT:  Walkthrough of control FIN-REV-07 (OTC-05) over the revenue
          recognition start date; conclusion that the control does not exist as
          documented; consequences for interim control testing and for the
          substantive cut-off response.

PREPARED BY:  G. Lindqvist (GRL)        DATE PREPARED:  12/12/2025
              T. Iyer (TRI) — Sec. 4                     12/19/2025
REVIEWED BY:  O. Haddad (OMH)           DATE REVIEWED:  12/22/2025
PARTNER:      D. Whitcombe (DGW)                         12/23/2025
EQR:          L. Herrera (LXH)                           02/17/2026
--------------------------------------------------------------------------------
PURPOSE
To clear open item 7 of WP 3100-04F by inspecting the report used to perform the
control documented as FIN-REV-07, to evaluate that control's design against
WCGW-6 (revenue recognized before the customer tenant is provisioned), and to
determine the consequences for the interim test of controls at WP 3400-12 and for
the cut-off assertion over subscription revenue.

SOURCE OF INFORMATION
(1) Management control documentation FIN-REV-07, v2 dated 07/28/2025, obtained
    from M. Fong (Internal Audit) 08/04/2025.                              (a)
(2) Walkthrough of 12/10/2025, 14:00-14:25 CT, with J. Pike (Revenue Manager),
    screen share of Snowflake and Zuora Revenue.
(3) Definition of Snowflake view vw_activation_variance, 14 columns.        (b)
(4) Confirmation from R. Sandoval (Director, IT) 12/10/2025 that the platform
    application database is not replicated by the I-8 Fivetran pipeline.    (b)
(5) Direct query of the platform database for provisioned_at, all FY2025
    subscription activations; 1,206 records; reconciled to the Zuora activation
    population of 1,206.  RevPro revenue start dates, all FY2025 contracts.(c)
(6) WP 3400-12 (interim test of FIN-REV-07, performed 11/06/2025).

PROCEDURES PERFORMED
1. Asked J. Pike to open the report he uses for the monthly comparison and to
   identify, on screen, the two date fields compared.                       (d)
2. Read the view definition. No provisioning date column exists.            (d)
3. Corroborated the absence of provisioning data in any reporting layer with
   the IT owner, independently of Revenue Accounting.                       (d)
4. Recomputed the exposure: compared provisioned_at to the RevPro revenue start
   date for all 1,206 FY2025 activations requiring provisioning:
       provisioned on or before revenue start                 992      -
       1-3 days after                                         187     41
       4-14 days after                                         13     23
       more than 14 days after                                 14    410     (d)
       total                                                 1,206    474
5. Traced 5 of the 14 to the executed order form, the provisioning ticket, and
   the RevPro schedule, including C-1 Meridian (provisioned 04/02/2025,
   revenue start 03/15/2025).
6. Re-read WP 3400-12 and identified the attribute tested.                   (d)
7. Discussed with E. Vasquez and D. Kim 12/11/2025.

RESULTS
- The control described in FIN-REV-07 does not exist; the data it requires is
  not available in any report accessible to the control performer. The control
  actually performed compares the billed service start date to the order-form
  start date and cannot detect WCGW-6, which had no control mapped to it at any
  point during FY2025.                                                      (d)
- WP 3400-12 is VOIDED as a test of FIN-REV-07: the attribute tested was not an
  attribute of the documented control. Re-purposed as evidence over WCGW-4.  (d)
- Misstatement identified: FY2025 subscription revenue overstated and deferred
  revenue understated by 410 (14 contracts), recorded by management as corrected
  misstatement C-1. Residual 64 below the CTT of 72; not accumulated.
- Control deficiency: design deficiency over revenue cut-off. Preliminary
  severity range: significant deficiency to material weakness. Aggregated at
  WP 8400-11; final conclusion, material weakness over revenue cut-off.     (d)

CONCLUSION
Control FIN-REV-07 (OTC-05) is not suitably designed and did not exist as
documented during FY2025. No reliance is placed on it. The cut-off assertion
over subscription revenue is supported for FY2025 by the full-population
procedure at Section 4 above, and by the procedures at WP 3200-08, rather than
by control reliance. The related deficiency is evaluated at WP 8400-11 and was
communicated to the audit committee on 12/18/2025.

TICK MARK LEGEND
(a) Client-prepared documentation; read and retained in the file.
(b) Corroborated with a second source independent of the control performer.
(c) Population completeness reconciled between two independent systems.
(d) Exception, deficiency, or misstatement identified; see RESULTS.
================================================================================
```

### Lessons

1. **An open item on a walkthrough record is an audit risk with a due date.** Item 7 was correctly identified,
   assigned, and dated on October 8. Nothing about the identification failed; the follow-up failed. Open items
   arising from walkthroughs of controls over a significant risk should be escalated on the due date, not on the
   date someone next reads the workpaper.
2. **Ask to see the report.** The entire finding was 60 seconds of screen share. When an interviewee's answer
   names an artifact, obtain the artifact in the room; when it names different objects than the question named,
   treat the mismatch as the finding rather than translating it into your own words.
3. **Test the control's attribute, not the artifact's existence.** WP 3400-12 inspected a report and agreed
   dispositions. Both of those things were real. Neither was the control. Read the control description immediately
   before designing the test, and write the attribute in the test as a quotation from it.
4. **A trace whose values are not compared is not a trace.** `provisioned_at` of April 2 and a revenue start of
   March 15 both appear in the October 7 workpaper. The discipline that would have caught it is Exhibit 13-14's
   "tied to" column: a value in a trace with nothing in that column is an unexamined fact.
5. **Do not let re-documentation dissolve the finding.** Where practice is weaker than documentation, editing the
   documentation changes which deficiency you are reporting and never eliminates it. Write down which of the two
   you are looking at before management redlines anything.

## Common Mistakes

### Mistake 13.1 — Concluding on operating effectiveness in a walkthrough workpaper

**What it looks like.** The walkthrough memo ends "based on the procedures performed, we concluded that the
control is operating effectively."
**Why it happens.** The auditor did inspect one occurrence, and inspection feels like testing.
**What goes wrong.** The file now contains an unsupported conclusion that a reviewer may rely on when scoping
tests of controls, and the operating-effectiveness test is either skipped or reduced on a basis nobody wrote down.
**How to avoid it.** Restrict walkthrough conclusions to the two permitted forms in §13.2, and put the objectives
checkbox block (Exhibit 13-18) at the top of every walkthrough workpaper so the unaddressed objective is visible.

### Mistake 13.2 — Interviewing the control owner instead of the performer

**What it looks like.** The attendee list for the access-control walkthrough is the Director of IT; for revenue,
the VP of Revenue Accounting.
**Why it happens.** Owners are the audit's contacts, they are articulate, and scheduling one meeting is easier
than four.
**What goes wrong.** You obtain the control as designed, which is the control you already had in writing.
AtlasFlow's access review frequency (W-3) and the OTC-05 phantom control were both invisible from the owner's
chair.
**How to avoid it.** Record, in the walkthrough record, each attendee's role relative to each control as OWNER or
PERFORMER, and treat a control with no PERFORMER present as not walked.

### Mistake 13.3 — Leaving process steps in the control matrix

**What it looks like.** Nineteen "controls" in order-to-cash, eight of which are activities that cannot fail.
**Why it happens.** Management builds the matrix from a process narrative and the auditor accepts the client's
population.
**What goes wrong.** Testing budget is consumed by tests whose attribute is that the transaction exists; the
genuine controls get proportionally less attention; and management asserts on a control population containing
non-controls.
**How to avoid it.** Apply the four-property test in §13.6 — performer or rule, criterion, disposition, frequency
and population — before any test is designed, and reduce the matrix in writing.

### Mistake 13.4 — Writing the WCGW at the account level

**What it looks like.** "WCGW: revenue could be overstated." "WCGW: deferred revenue could be incomplete."
**Why it happens.** The WCGW column is completed after the fact, from the assertion column, by someone who was not
in the walkthrough.
**What goes wrong.** An account-level WCGW cannot be mapped to a process point, so any control appears to address
it, and precision cannot be evaluated at all. Every design conclusion built on it is unfalsifiable.
**How to avoid it.** Require every WCGW to name a field or record, a direction of error, and a sequence number on
the process map, as in Exhibit 13-8.

### Mistake 13.5 — The refresh by email

**What it looks like.** Last year's narrative is emailed to the controller with "please confirm no changes"; the
reply "confirmed, no changes" is filed as the walkthrough.
**Why it happens.** It is fast, and in a stable year most of the narrative is in fact unchanged.
**What goes wrong.** The procedure performed is a single inquiry of the wrong person about a document, which
evidences nothing about the current period and cannot detect a control that quietly stopped operating — the most
common way controls fail.
**How to avoid it.** Even in a refresh year, interview each performer, inspect one current artifact per control,
trace one transaction, and document the change analysis (§13.12).

### Mistake 13.6 — Blending what you were told with what you saw

**What it looks like.** A narrative in which "the Analyst compares five attributes" and "the approval record shows
the approver and timestamp" sit in the same paragraph with no indication that the first is inquiry and the second
is inspection.
**Why it happens.** Good writing merges sources; audit documentation must not.
**What goes wrong.** The design conclusion cannot be evaluated on review, because the reviewer cannot tell which
facts are corroborated. Under AS 1105 the two have materially different weight.
**How to avoid it.** Keep the three lists in Exhibit 13-18 separate: observed, inspected, and inquiry-only. The
inquiry-only list is the list of things you have not yet established.

### Mistake 13.7 — Accepting the "we always do it correctly" answer

**What it looks like.** The narrative says the reconciliation "always ties" and the control description contains no
threshold, no exception disposition, and no example.
**Why it happens.** The interviewee is competent and the answer sounds like assurance.
**What goes wrong.** No criterion has been obtained, so precision cannot be assessed and the test attribute cannot
be written. If the control genuinely never produces an exception, the likeliest explanations are that it does not
detect, or that exceptions are cleared upstream and never recorded — both findings you have missed.
**How to avoid it.** Run the four conversions in §13.8.3: last instance, mechanism, walk-forward on a real item,
negative-population count corroborated to a system record.

### Mistake 13.8 — Mapping a control to a WCGW it cannot detect

**What it looks like.** Every WCGW row in the matrix has a control reference in it, and the design column reads
"effective" throughout.
**Why it happens.** The matrix is completed by mapping controls that exist at the same process point, and
proximity is mistaken for coverage.
**What goes wrong.** OTC-03 is the example: a comparison of a date field to a document bearing the same date was
mapped to the WCGW that the date itself is wrong. The audit believed a cut-off WCGW was controlled for a year.
**How to avoid it.** For every mapping, ask whether the attribute the control compares is independent of the
assertion at risk, and quantify the largest misstatement that could pass (Exhibit 13-10). If the answer is
"unlimited," the mapping is wrong.

### Mistake 13.9 — Testing the artifact the client produced rather than the control's attribute

**What it looks like.** The test workpaper agrees the report the client supplied to the dispositions the client
recorded, and concludes no deviations.
**Why it happens.** The tester works from the prior-year test program or from the client's evidence package rather
than from the control description.
**What goes wrong.** WP 3400-12 at AtlasFlow: three months tested, no deviations, and the attribute tested belonged
to a different control. The work was void and the void was discovered 21 days before year end.
**How to avoid it.** Write the test attribute as a direct quotation from the control description, and identify the
independent source for each attribute before selecting anything.

### Mistake 13.10 — Never asking what happens at quarter end

**What it looks like.** A walkthrough conducted in October describes the process as it operates in October, and the
conclusion is applied to the whole year.
**Why it happens.** Nobody volunteers the exception to their own process, and the question is not on the standard
program.
**What goes wrong.** AtlasFlow activates orders before Deal Desk validation in the quarter-end war room, so a
preventive control operates as a detective control — or not at all — over the population containing 41% of Q4 ACV
($25,174 signed December 24–31).
**How to avoid it.** Ask "what is different in the last two days of a quarter, and who is doing it at 11 p.m.?" in
every revenue-process walkthrough, and stratify the test population accordingly.

## Practice Exercises

### Exercise 13-1

[Foundational] The following eight steps are taken from a self-serve (Stripe) order-to-cash process at AtlasFlow:
(1) customer enters card details on the pricing page; (2) Stripe authorizes the card; (3) the platform provisions
the trial-to-paid conversion automatically; (4) Stripe issues the receipt; (5) the daily Lambda job (I-4)
summarizes the day's charges; (6) the summary journal posts to NetSuite; (7) the Staff Accountant reconciles the
Stripe payout to account 1205; (8) failed charges enter a dunning sequence. Classify each step as initiation,
authorization, processing, or recording, and state how many distinct authorization points exist.

### Exercise 13-2

[Foundational] For each description, state whether it is a control or a process step, and for each process step
state whether a control could exist at that point: (a) "The Billing Analyst runs the monthly bill run in Zuora."
(b) "Credit memos over $25 thousand require Controller approval in Zuora before they can be applied." (c) "The
Revenue Manager prepares the RevPro-to-GL journal." (d) "NetSuite prevents posting to a closed period." (e) "The
consolidation workbook is saved to SharePoint." (f) "The Treasury Manager agrees the wire batch total to the
approved payment run report before releasing the batch."

### Exercise 13-3

[Intermediate] Write one WCGW, in the form required by §13.5, for each of these three process points, and state
the relevant assertion(s) each affects: (a) seq. 9, invoice generation from the Zuora billing schedule; (b) the
monthly Carta export used to prepare the stock-based compensation calculation (interface I-6); (c) the daily
bank-feed matching in NetSuite (interface I-9).

### Exercise 13-4

[Intermediate] AtlasFlow issued 412 credit memos in FY2025 totaling $2,180 thousand. Ninety-six memos totaling
$1,690 thousand exceeded the $25 thousand Controller-approval threshold. Overall materiality is $1,450,
performance materiality $940, and the clearly trivial threshold $72. Compute (a) the coverage of the control by
count and by value; (b) the aggregate value and average size of the unapproved population; (c) the ratio of the
unapproved aggregate to the clearly trivial threshold and to performance materiality; and (d) state whether the
control's precision is sufficient for WCGW-10, giving your reasoning in two sentences.

### Exercise 13-5

[Intermediate] Management's documentation describes a user access review performed quarterly for each of
Salesforce, Zuora, and NetSuite, to be completed within 30 days of each quarter end. In FY2025 one review was
performed: the Salesforce review, distributed July 21, 2025 and completed September 9, 2025. The most recent prior
review was completed August 12, 2024. Compute (a) the number of reviews expected in FY2025 and the number
performed, as a count and a percentage; (b) the number of days the Q2 2025 review was completed after its due
date; (c) the elapsed days between the last two completed Salesforce reviews. Then state, in one sentence, what
the arithmetic in (c) means for reliance on Salesforce automated controls during FY2025.

### Exercise 13-6

[Advanced] Six FY2025 subscription activations are listed below. AtlasFlow's policy recognizes subscription
revenue from the later of the contract start date and the provisioning date. Amounts are annual subscription value
in thousands; assume straight-line daily recognition on a 365-day basis and that each contract's first year falls
entirely within FY2025 unless the dates say otherwise.

| Contract | Annual value | Contract start | provisioned_at |
| --- | --- | --- | --- |
| A | 240 | 03/15/2025 | 04/02/2025 |
| B | 600 | 03/15/2025 | 04/02/2025 |
| C | 120 | 06/01/2025 | 06/03/2025 |
| D | 480 | 09/01/2025 | 09/01/2025 |
| E | 360 | 11/15/2025 | 12/20/2025 |
| F | 900 | 01/01/2025 | 01/08/2025 |

Compute the days of early recognition and the FY2025 revenue overstatement for each contract and in total, to one
decimal place, and evaluate the total against the clearly trivial threshold of $72 and performance materiality of
$940.

### Exercise 13-7

[Intermediate] Two controls: (a) the annual review and approval of the ASC 340-40 commission amortization period,
performed once in November by the Director of Technical Accounting; (b) the daily I-1 error-queue review, which
operated on 251 business days. For each, state whether a walkthrough that inspects one occurrence, with its
supporting documents, and re-performs the comparison can also serve as the test of operating effectiveness. Give
your reasoning and, for the control where the answer is no, state what would be required instead.

### Exercise 13-8

[Advanced] Management's documentation describes a monthly control in which the Revenue Manager compares billed
service start dates to provisioning dates. The performer compares billed service start dates to order-form start
dates, and no provisioning data is available to him. Management offers to amend the documentation to describe what
the performer does. Write a conclusion of no more than 150 words stating whether the deficiency is one of design
or of operation, whether amending the documentation changes your conclusion, and what the amendment would change.

### Exercise 13-9

[Intermediate] The Billing Analyst emails the Revenue Manager a monthly list of subscriptions activated with a
service start date more than 30 days in the past. The activity appears in no control matrix. Draft a control
description of 60 to 90 words that satisfies all four properties in §13.6, and state the one additional fact you
would need before you could rely on it.

### Exercise 13-10

[Advanced] Draft the paragraph, of 120 to 180 words, that you would put in the audit file on December 11, 2025 to
record the effect of the OTC-05 discovery on the interim test of controls at WP 3400-12. Your paragraph must state
what was tested, why the test does not support the control, what happens to the interim conclusion, and the
consequence for the substantive plan.

### Exercise 13-11

[Advanced] Identify at least seven defects in the following walkthrough workpaper extract.

```text
WP 5200-03  PAYROLL PROCESS WALKTHROUGH
Discussed the payroll process with the VP of People Operations on 09/18/2025.
The Company processes US payroll semi-monthly through ADP. Payroll is reviewed
for accuracy and approved before submission. Terminations are processed timely.
Access to ADP is restricted to authorized personnel. Payroll journal entries are
posted to NetSuite and reconciled monthly. We noted no exceptions and concluded
that controls over payroll are operating effectively. The Company's SOC 1 report
from ADP was obtained and no issues were noted.
```

### Exercise 13-12

[Advanced] This exercise spans Chapters 6 and 13. Before the OTC-05 correction, AtlasFlow's draft FY2025 total
revenue was $148,610 thousand and total deferred revenue at December 31, 2025 was $77,790 thousand. The correction
recorded was $410 thousand. (a) Compute the corrected revenue and deferred revenue figures and confirm they agree
to the continuing case. (b) State which relevant assertion in each account the misstatement affects, and in which
direction. (c) State which line of the Chapter 6 deferred revenue roll-forward changes, and by how much. (d)
Explain in two sentences why the walkthrough that found this misstatement provides evidence about deferred revenue
*completeness* and not merely about revenue cut-off.

## Solutions to Practice Exercises

### Solution 13-1

Initiation: step 1 (the card entry creates the record with accounting consequence). Authorization: step 2 only.
Processing: steps 3, 4, 5, 8. Recording: step 6. Step 7 is a detective control over recording rather than a point
in the flow. **One** genuine authorization point exists and it is performed outside the entity by the card issuer:
in the self-serve channel there is no internal authorization of the transaction, so the controls that matter are
the completeness controls at steps 5 through 7 — which is why weakness W-7 (undocumented changes to the I-4 Lambda
job) is more consequential here than the same weakness would be in the enterprise channel.

### Solution 13-2

(a) Process step; a control could exist over the completeness of the bill run (for example, comparing subscriptions
eligible for billing to invoices generated). (b) Control: rule, criterion ($25 thousand), performer (Controller),
disposition (cannot be applied), population (all credit memos). (c) Process step; preparation is never a control,
and the control at that point is the Controller's review (OTC-08). (d) Control: an automated preventive control
with a population (all postings), a criterion (period status), and a disposition (prevention). (e) Process step;
no control, and the absence of one is weakness W-8. (f) Control: performer, criterion (batch total to approved
payment run), disposition (does not release), population (all wire batches).

### Solution 13-3

(a) "A subscription is invoiced on terms that differ from the rate-plan charges created from the executed order
form — wrong amount, wrong period, or not invoiced at all — because the billing schedule was amended after
activation." Assertions: accuracy and completeness of revenue and of accounts receivable. (b) "The monthly Carta
export omits grants, cancellations, or modifications occurring late in the month, or is superseded by a later
export, so the SBC calculation is prepared on an incomplete grant population." Assertions: completeness and
accuracy of stock-based compensation expense and of additional paid-in capital. (c) "The bank feed
auto-matches a receipt to the wrong open invoice, relieving a receivable that was not paid and leaving the paid
receivable open." Assertions: accuracy of accounts receivable and, for the aging used in the credit-loss estimate,
accuracy of the allowance. Each names a record, a direction, and a consequence.

### Solution 13-4

(a) Coverage by count: 96 ÷ 412 = **23.3%**. By value: $1,690 ÷ $2,180 = **77.5%**. (b) Unapproved population:
412 − 96 = **316 memos**, $2,180 − $1,690 = **$490**; average $490 ÷ 316 = **$1.55**. (c) $490 ÷ $72 = **6.8
times** the clearly trivial threshold; $490 ÷ $940 = **52.1%** of performance materiality. (d) Precision is
sufficient against an individually material unauthorized credit and insufficient against the aggregate risk, since
$490 is 6.8 times the clearly trivial threshold and over half of performance materiality, and the threshold permits
a credit to be split into sub-threshold memos. A defensible alternative is that the design is adequate *provided* a
detective control operates over the aggregate — at AtlasFlow the monthly contra-revenue flux review — in which case
the conclusion depends on that control's precision, which Chapter 14 analyzes.

### Solution 13-5

(a) Expected: 3 applications × 4 quarters = **12 reviews**; performed: **1**; completion rate 1 ÷ 12 = **8.3%**, so
11 reviews (91.7%) were not performed. (b) The Q2 2025 review was due July 30, 2025 (June 30 plus 30 days) and was
completed September 9, 2025: **41 days late**. (c) August 12, 2024 to September 9, 2025 is 365 + 28 = **393 days**.
No access recertification occurred at any point in the FY2025 period of intended reliance until 113 days before
year end, so inappropriate access could have persisted all year — which removes the basis for relying on the CPQ
and Zuora automated controls absent direct testing of access, and is why Chapter 11 evaluates W-3 as pervasive
rather than as a discrete exception.

### Solution 13-6

| Contract | Days early | Computation | FY2025 overstatement |
| --- | --- | --- | --- |
| A | 18 | 240 × 18 ÷ 365 | 11.8 |
| B | 18 | 600 × 18 ÷ 365 | 29.6 |
| C | 2 | 120 × 2 ÷ 365 | 0.7 |
| D | 0 | — | 0.0 |
| E | 35 | 360 × 35 ÷ 365 | 34.5 |
| F | 7 | 900 × 7 ÷ 365 | 17.3 |
| | | **Total** | **93.9** |

The total of $93.9 thousand exceeds the $72 clearly trivial threshold and must be accumulated on the summary of
audit differences; at 10.0% of performance materiality and 6.5% of overall materiality it is not on its own
quantitatively material. A complete answer adds that days alone do not rank exposure — E's 35 days on a smaller
contract beats A's 18 days — and that two contracts sharing an identical 18-day delay is the signature of a
provisioning backlog rather than random error, so the population must be examined in full rather than sampled.

### Solution 13-7

(a) **Yes, with conditions.** The population is one occurrence, so a walkthrough that establishes the population is
one, inspects the memo and the underlying customer-life and renewal-commission analysis, and re-performs the
comparison of the 4-year period to the 4.3-year average customer life is the entire test. The conditions: document
it as serving both objectives, evidence the population's completeness, and inspect rather than discuss. (b) **No.**
One observation from 251 supports an upper deviation limit near 90% at a 10% risk of overreliance. What is required
instead is a defined population (the daily queue exports, with counts agreed to the source systems), a
representative selection across the period at the sample size Chapter 14, §14.5 specifies for a daily control, and
inspection of the resolution evidence for each item selected.

### Solution 13-8

Model answer: "The deficiency is one of design. The control as documented requires a comparison to the provisioning
date; that data is not available in any report accessible to the performer, so the control has never operated and
cannot be made to operate by insisting on the documented frequency. The control that is performed compares two
dates neither of which evidences the transfer of control of the service, so it cannot detect revenue recognized
before provisioning, and the WCGW is unaddressed. Amending the documentation does not change the conclusion; it
changes only which deficiency is reported — from a documented control that did not operate to a documented control
that is not capable of addressing the risk it is mapped to. In both formulations no control addressed the cut-off
WCGW during FY2025 and no reliance is available." A weaker but defensible alternative treats it as an operating
deficiency on the ground that management's asserted control simply did not run; that framing is acceptable only if
the memo also states that remediation requires new data, not renewed diligence.

### Solution 13-9

Model description (78 words): "Monthly, within five business days of month end, the Billing Analyst runs the
'Backdated Activations' query in Zuora Billing listing every subscription activated in the month with a service
start date more than 30 days before the activation date, and sends the list to the Revenue Manager. The Revenue
Manager investigates each item against the executed order form, records the disposition in the exception log, and
adjusts the RevPro revenue start date where the backdating is not supported. Items with no disposition are escalated
to the Controller." The additional fact required before relying on it: whether the 30-day parameter is the right
precision — that is, what population of backdated activations falls between 1 and 30 days and therefore never
appears on the list.

### Solution 13-10

Model paragraph (168 words): "WP 3400-12 tested control FIN-REV-07 as of the October 31, 2025 interim date by
selecting three of the ten months in the interim period, obtaining the Activation Variance Report for each month,
agreeing the exceptions listed to the Revenue Manager's recorded dispositions, and concluding that no deviations
were noted. The attribute tested was that a variance report was reviewed and its exceptions dispositioned. The
control description requires a comparison of the billed service start date to the platform provisioning date; the
report inspected contains no provisioning date, and provisioning data is not available in any report accessible to
the control performer. The attribute tested is therefore not an attribute of the documented control, and the test
provides no evidence about WCGW-6. WP 3400-12 is voided as a test of FIN-REV-07 and is retained as evidence over
WCGW-4 only. No reliance is placed on FIN-REV-07 for any period. The cut-off assertion over subscription revenue
will be supported by a full-population comparison of provisioning timestamps to RevPro revenue start dates for
FY2025, performed at WP 3100-09, Section 4."

### Solution 13-11

Defects: (1) the interviewee is the process owner and no control performer was interviewed; (2) "reviewed for
accuracy and approved" names no performer, criterion, or disposition, so no control is described and none can be
tested; (3) "terminations are processed timely" states an outcome with no timeframe, population, or evidence — the
actual AtlasFlow average was 6.2 days against a 24-hour SLA (W-5); (4) "access is restricted to authorized
personnel" is an objective, not a control; (5) nothing was observed or inspected, and the workpaper does not
disclose that it records inquiry only; (6) no transaction was traced and no register, journal, or reconciliation is
identified by name, amount, or period; (7) the conclusion asserts operating effectiveness, which a walkthrough
cannot support; (8) no WCGW is identified, so design is evaluated against nothing; (9) the SOC 1 report is cited
with no period, opinion, CUEC mapping, or bridge-letter consideration; (10) there is no preparer or reviewer
sign-off, no date, no reference to the control matrix, and no open items.

### Solution 13-12

(a) Corrected revenue: $148,610 − $410 = **$148,200**; corrected deferred revenue: $77,790 + $410 = **$78,200**,
agreeing to the continuing case and to the $71,300 / $6,900 split. (b) Revenue: cut-off (and occurrence),
overstated. Deferred revenue: completeness, understated. The two are the same error seen from either side of the
entry. (c) In the Chapter 6 roll-forward, "revenue recognized from current-period billings" changes from $(93,710)
to **$(93,300)**, a reduction of $410; billings of $163,750 and the opening balance of $62,300 are unaffected,
because nothing about the invoice changed. (d) Every dollar recognized early is a dollar of liability released
early, so a control failure over revenue timing is by construction a control failure over the completeness of the
contract liability. Chapter 6, §6.2 makes the point from the account side: completeness cannot be tested by
selecting from recorded balances, and a process-level cut-off deficiency is one of the few things that speaks to it
directly.

## Review Questions

**RQ 13-1.** State the four objectives AS 2201 identifies for the auditor's understanding of likely sources of
potential misstatement.

**RQ 13-2.** Distinguish evaluating the design effectiveness of a control from testing its operating
effectiveness, in terms of the conclusion each supports.

**RQ 13-3.** Why does a walkthrough of a daily control provide almost no evidence about operating effectiveness,
while a walkthrough of an annual control may provide all of it?

**RQ 13-4.** What does the AICPA framework mean by determining that a control has been *implemented*, and how does
that requirement differ from the PCAOB's design-effectiveness evaluation?

**RQ 13-5.** Name the four properties that distinguish a control from a process step.

**RQ 13-6.** Why is "revenue may be misstated" an unusable WCGW?

**RQ 13-7.** What are the three questions that determine whether a control operates at a sufficient level of
precision?

**RQ 13-8.** Why do you interview the person who performs a control rather than the person who owns it?

**RQ 13-9.** Give the four escalating conversions for an interviewee who answers "we always do it correctly."

**RQ 13-10.** Identify three linguistic signals that an interviewee is describing policy rather than practice.

**RQ 13-11.** State one virtue and one vice of each of the narrative, flowchart, and control matrix formats.

**RQ 13-12.** What is the difference between an undocumented control and a control that does not exist as
documented, and why do they have opposite consequences for management?

**RQ 13-13.** When is amending a control description the right response to a walkthrough finding, and when is it
the wrong one?

**RQ 13-14.** List four indicators that a full re-walkthrough is required rather than a refresh.

**RQ 13-15.** What six questions must a reviewer be able to answer from a walkthrough workpaper alone?

**RQ 13-16.** For a vendor-hosted application whose code and change tickets you cannot see, what replaces
observation of the control activity?

**RQ 13-17.** Why is a screenshot of a configuration screen insufficient evidence that the configuration operated
throughout the period?

## Answers to Review Questions

**RQ 13-1.** Understand the flow of transactions related to the relevant assertions, including how they are
initiated, authorized, processed, and recorded; verify that the auditor has identified the points at which a
misstatement could arise; identify the controls management has implemented to address those potential
misstatements; and identify the controls management has implemented over the prevention or timely detection of
unauthorized acquisition, use, or disposition of assets.

**RQ 13-2.** Design effectiveness supports the conclusion that the control, *if it operated as described on the
population described*, would prevent or detect on a timely basis a misstatement in the relevant assertion that
could be material. Operating effectiveness supports the conclusion that the control *did operate* as designed,
throughout the period of intended reliance, on the population it was supposed to be applied to, with a deviation
rate low enough to support reliance. The first is a hypothetical about a design; the second is an empirical claim
about a period.

**RQ 13-3.** Because a walkthrough obtains one occurrence, and its value depends on what fraction of the population
that occurrence represents. For a daily control the population is roughly 251 and one clean observation is
consistent with a very high deviation rate. For an annual control the population is one, so inspecting that
occurrence with its supporting documents and re-performing the comparison exhausts the population — provided the
auditor establishes that the population really is one and documents the procedure as serving both objectives.

**RQ 13-4.** Implementation means the control exists and is in use: the entity is actually applying the control whose
design the auditor evaluated. AU-C 315 requires both the design evaluation and the implementation determination for
controls relevant to the audit, and a walkthrough tracing one transaction discharges both. Under AS 2201 the same
procedure discharges design effectiveness only, and the ICFR opinion additionally requires operating-effectiveness
evidence for every control relied on — so the walkthrough leaves far more work behind it in a PCAOB integrated
audit.

**RQ 13-5.** A performer (a named role) or a configured rule; a criterion (something compared to something else,
or evaluated against a threshold); a disposition (what happens when the criterion is not met); and a frequency
together with a defined population.

**RQ 13-6.** It restates the audit objective rather than describing a mechanism. It names no field, record, or
process point, so it cannot be located on the process map, any control appears to address it, and precision cannot
be evaluated because there is no specific error whose magnitude can be bounded. A usable WCGW names a record, a
direction of error, and a consequence.

**RQ 13-7.** What is the largest misstatement that could pass through the control undetected; does the control
operate on the complete population of items exposed to the WCGW; and is the attribute the control compares
genuinely independent of the assertion at risk.

**RQ 13-8.** The owner describes the control as designed, because that is their honest belief and usually their own
documentation. The performer knows what happens — the frequency at which the review actually reaches them, the
report they actually open, what they do at 11 p.m. on the last day of a quarter. At AtlasFlow both the access review
frequency and the non-existence of the provisioning comparison were visible only from the performer's chair.

**RQ 13-9.** Ask for the last instance ("when did it last not tie?"); ask for the mechanism rather than the outcome
("what would you be looking at that would tell you?"); ask for a walk-forward on a real item you selected in
advance while you watch; and ask the negative-population question ("how many went back last quarter?") and compare
the answer to the system record.

**RQ 13-10.** The passive voice ("orders are reviewed"); the normative rather than the past tense ("the analyst
should compare"); the plural or institutional subject ("we require"); and vocabulary drawn from the control
documentation rather than from the screen — no report names, no field names, no complaints.

**RQ 13-11.** Narrative: expresses conditionality, exception, and segregation, but its completeness cannot be
assessed and control descriptions hide in prose. Flowchart: exposes handoffs and therefore WCGWs, but cannot carry
precision, frequency, or criteria. Matrix: auditable column by column and forces the WCGW-to-assertion linkage, but
destroys sequence and invites the auditor to mistake the row for the understanding.

**RQ 13-12.** An undocumented control mitigates a WCGW but appears in no documentation: the process is better than
described, and the problem belongs to management's Section 404(a) documentation and monitoring. A control that does
not exist as documented is one management asserted on that is not performed, is performed less often, or is performed
on different objects: the process is worse than described, and it is a deficiency. The first may be relied on once
tested; the second cannot be relied on at all.

**RQ 13-13.** Amending is right where practice is *better* than the documentation — the documentation is simply
incomplete or imprecise and the WCGW is addressed. Amending is wrong where practice is *weaker* than the
documentation, because the amendment converts a control that did not operate into a control that is not capable of
addressing the WCGW: a different deficiency, not the absence of one.

**RQ 13-14.** First year of ICFR auditor attestation; a system implementation, upgrade, or migration affecting the
process; a change in the personnel who perform the control; a business combination integrated into the process; a
prior-year deficiency in the process; and a significant risk at the assertion level that the process affects. Any
one of the first two is normally decisive on its own.

**RQ 13-15.** Who was interviewed and their role relative to each control; what was asked; what was seen; which facts
came from inquiry and which from inspection; which WCGWs are addressed and which remain unaddressed; and what is
unresolved, with an owner and a due date. AS 1215 supplies the standard: an experienced auditor with no previous
connection to the engagement must be able to understand the work, who performed it, when, and the conclusions.

**RQ 13-16.** Nothing performed directly at the service organization. Observation is replaced by the service
auditor's description of the system and the tests of controls in the SOC 1 report, considered under AS 2601 or
AU-C 402, together with inspection of the configuration the entity itself controls, attention to the report period
and any gap requiring a bridge letter, and mapping of the report's CUECs to the entity's own controls.

**RQ 13-17.** Because the screenshot evidences the configuration on the day it was taken and nothing about the
preceding months. Evidence about the period comes from the application's change management record — that the
configuration was not altered, or that any alteration was authorized and tested — which is an IT general control
matter rather than something the configuration screen can show.

## Key Definitions

**Annual walkthrough refresh.** The procedure in which the prior year's structural understanding — the flow, the
IAPR map, the WCGW inventory — is carried forward and challenged rather than rebuilt, while current-period evidence
is still obtained by interviewing each performer, inspecting one current artifact per control, and tracing a
transaction. Distinguished from confirming the prior-year narrative by inquiry, which is not a walkthrough.

**Authorization point.** A point in a transaction flow at which a person with the requisite authority, or a
configured rule acting in place of one, approves the transaction or its terms. A process typically has more than
one; AtlasFlow's enterprise order-to-cash has three (pricing approval, recording of contract execution, and
activation).

**Control matrix.** A tabular form of process documentation in which each row is a control and the columns are the
attributes needed to test it: process point, control description, WCGW addressed, relevant assertions, preventive
or detective, type, frequency, performer, and evidence of operation. Its value is that a blank cell is a finding;
its limitation is that it does not express sequence.

**Control owner.** The person accountable for a control's existence and design, typically the manager of the
function in which it operates. The owner is the right interviewee for why a control is designed as it is and the
wrong interviewee for what actually happens.

**Control performer.** The person who executes the control's steps. The performer's description of the activity is
the fact against which the documented control is evaluated.

**Corroborative inquiry.** Inquiry designed so that the answer can be verified against an artifact — "show me the
last three that were sent back" — rather than accepted on its own. It converts inquiry, the weakest form of
evidence, into a route to inspection.

**Design effectiveness.** The conclusion that a control, if it operated as described by a person with the described
competence and authority on the described population, would prevent or detect on a timely basis a misstatement in a
relevant assertion that could be material. It is evaluated *against an articulated WCGW*; a control cannot be
evaluated against nothing.

**Flowchart.** A diagrammatic representation of a process, preferably with swimlanes by function or system, in
which control points are marked and document and data flows are shown. Its diagnostic value lies in the visibility
of handoffs, which are where WCGWs concentrate.

**Hybrid documentation.** A documentation set combining a flow diagram, a keyed narrative, a control matrix, a
WCGW-to-assertion matrix, a transaction trace, and a walkthrough record under a single reference scheme. The keying
between components, not the choice of drawing tool, is what makes it work.

**Implementation of a control.** In the AICPA framework, the determination that a control exists and is being
applied by the entity, as distinct from evaluating whether its design would be capable of addressing the risk
(AU-C 315). Tracing one transaction through the control discharges the requirement.

**Information produced by the entity (IPE).** A report, schedule, or extract prepared by the entity and used as
audit evidence or used in the operation of a control, whose completeness and accuracy must themselves be
established. The RevPro Revenue Contract Summary, the FloQast task export, the Deal Desk rejection log, and the
Activation Variance Report are all IPE.

**Initiation, authorization, processing, and recording (IAPR).** The four states through which a transaction moves,
which AS 2201 requires the auditor to understand. Marking them on a process map is a mechanical discipline for
finding unaddressed risk, because they are the points at which a transaction changes state and a misstatement can
enter without contradicting anything upstream.

**Level of precision.** The smallest misstatement a control is capable of preventing or detecting, determined by
its threshold, the completeness of the population it operates on, and the independence of the attribute it
compares. A control mapped to a WCGW it cannot detect at a magnitude below materiality is not suitably designed
regardless of how faithfully it operates.

**Management review control.** A control whose operation consists of a person evaluating information against an
expectation or criterion and investigating differences. Its precision is a function of the level of aggregation
reviewed and the threshold for investigation; in a walkthrough the auditor's task is to obtain that threshold as a
number. Chapter 14 owns the testing.

**Narrative.** Process documentation in continuous prose, keyed to control references, describing the sequence of
activities, the conditions under which each occurs, and the disposition of exceptions. It is the only format that
carries conditionality and judgment well and the format in which incompleteness is hardest to detect.

**Observation.** Watching an activity being performed. It evidences that the activity occurred while the auditor
watched and nothing about other occasions, so its value in a walkthrough lies in exposing steps the description
omitted — the second screen, the side spreadsheet, the colleague consulted.

**Operating effectiveness.** The conclusion that a control operated as designed throughout the period of intended
reliance, on the population to which it should have been applied, with a deviation rate low enough to support
reliance. It requires a defined population whose completeness is established, a representative selection across the
period, and inspection or re-performance of each item selected.

**Phantom control.** Informal term for a control that appears in management's documentation but does not exist as
described — it is not performed, is performed at a lower frequency, is performed by someone lacking the authority
or information required, or is performed on different objects. It is a deficiency, and the documentation is what
makes it one, because the documented control is the control management asserted on.

**Process step.** An activity that lacks at least one of a performer or rule, a criterion, a disposition on failure,
and a frequency with a population. Entering an order, generating an invoice, and preparing a journal are process
steps; they cannot fail in a way a test could detect, and their presence in a control matrix consumes testing
capacity without producing evidence.

**Re-performance.** The auditor's independent execution of the control's procedure — recomputing the comparison the
reviewer says they made, or processing a chosen input through an automated rule and computing the expected output.
It is the strongest form of control evidence and, for a control that operates once, may constitute the entire test.

**Undocumented control.** An activity the auditor identifies that mitigates a WCGW but appears in no control
documentation. It may be relied on once its population and operation are tested, but its absence from management's
documentation is itself a deficiency in management's assessment process and must be communicated.

**Walkthrough.** A procedure in which the auditor follows a transaction from origination through the entity's
processes and information systems to the point at which it is recorded, combining inquiry of the personnel who
perform each step, observation, inspection of the records produced, and re-performance. AS 2201 identifies it as
frequently the most effective way to understand likely sources of potential misstatement. It is not a test of
operating effectiveness.

**What could go wrong (WCGW).** A statement, located at a specific process point, of a specific mechanism by which
a transaction could be recorded wrongly, expressed so that it can be linked to relevant assertions and so that a
control can be evaluated against it. A usable WCGW names a record or field, a direction of error, and an
accounting consequence.

## Chapter Summary

1. A walkthrough is a procedure performed on a transaction with the person who performs each step, not a document
   and not an update of last year's narrative; an engagement that "refreshed the walkthroughs" by email performed a
   single inquiry of the wrong person about a document.
2. Three objectives are constantly conflated. A walkthrough is sufficient for obtaining the understanding and for
   evaluating design effectiveness, and is close to worthless for operating effectiveness of a high-frequency
   control — one observation from a population of 251 supports an upper deviation limit near 90%.
3. The exception is the low-frequency control: for a control that operates once, a walkthrough that obtains the
   population of one, inspects the occurrence and its support, and re-performs the comparison can be the entire
   test, provided the workpaper says so.
4. Marking initiation, authorization, processing, and recording on the process map finds gaps mechanically.
   AtlasFlow's order-to-cash has three authorization points and management's documentation described one, which is
   how the activation control came to be documented in a way nobody had tested.
5. Narrative, flowchart, matrix, and hybrid answer different questions; documenting the same sub-process four ways
   shows that the narrative carries conditionality, the flowchart exposes handoffs, the matrix is auditable
   column by column, and only the hybrid does all three.
6. A WCGW must name a record, a direction, and a consequence, and must sit at a process point. A WCGW with no
   control mapped to it is a design deficiency the day it is identified, not a documentation gap awaiting further
   discussion with management.
7. Eight of the nineteen "controls" in AtlasFlow's order-to-cash documentation were process steps. A control has a
   performer or rule, a criterion, a disposition on failure, and a frequency with a population; anything missing
   one of the four cannot fail and therefore cannot be tested.
8. Design effectiveness turns on precision, and precision is arithmetic: the largest misstatement that can pass,
   the share of the exposed population covered, and whether the compared attribute is independent of the assertion
   at risk. OTC-03 compares a date field to a document bearing the same date and therefore cannot detect the
   WCGW it was mapped to.
9. Interview the performer, not the owner; funnel from open to closed to corroborative to exception questions; ask
   for the last instance when told "we always do it correctly"; and ask what happens in the last two days of a
   quarter, which at AtlasFlow revealed that a preventive control is inverted over the population containing
   $25,174 of Q4 ACV.
10. When an interviewee's answer names different objects than your question named, the mismatch is the finding.
    Jordan Pike's answer named the order-form date where the question named the provisioning date, and the missing
    follow-up — "show me the report" — cost the engagement the interim testing of a cut-off control and three
    weeks of runway.
11. A trace whose values are not compared to anything is not a trace: `provisioned_at` of April 2, 2025 and a
    revenue start of March 15, 2025 both sat in the October 7 workpaper, and the comparison that would have found
    $410 of misstatement was not made until December 19.
12. Where practice is better than documentation, correct the documentation; where practice is weaker, amending the
    documentation changes which deficiency you report and never eliminates it.
13. Automated and vendor-hosted processes still get walked: inquiry moves to the configurer and the monitor,
    observation moves to a sandbox transaction or to the service auditor's description of the system,
    inspection moves to the configuration and its change record, and re-performance becomes a test of one that is
    valid only if the ITGCs hold — which at AtlasFlow they do not.
14. The open-items list on a walkthrough record is a control over the audit, and like any control it needs a
    performer, a frequency, and a disposition; AtlasFlow's item 7 was identified correctly, assigned correctly,
    and then sat for 47 days.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Risk assessment, significant risks, and the selection of processes to walk | Chapter 2 | Determines which processes and which relevant assertions the walkthrough must cover; the engagement team discussion that receives the walkthrough's risk findings |
| ITGCs: access provisioning, periodic access review (W-3), change management, and SOC 1 reports | Chapter 11 | Owns the controls being walked in §13.15 and the evaluation of the access-review frequency finding in Annotation 13-6 |
| Automated application controls, the CPQ approval matrix, the RevPro rule set, interfaces I-1 to I-9, and IPE testing | Chapter 12 | Owns the configuration testing referenced in Exhibit 13-5 and the completeness and accuracy of the reports used in every control here |
| Tests of controls, sample sizes, management review controls, deviations, and deficiency severity | Chapter 14 | Owns everything after the walkthrough, including the grading of the deficiencies this chapter identifies and the aggregation at WP 8400-11 |
| Order-to-cash accounting, revenue cut-off testing, and contra revenue | Chapter 4 | The accounting consequences of the WCGWs in Exhibit 13-8 and the substantive cut-off procedures that replace failed control reliance |
| Allocation of the transaction price on contract C-1 across four performance obligations | Chapter 5, §5.7 | The trace in Exhibit 13-14 tests the dates and terms that feed the allocation; Chapter 5 recomputes the amounts |
| Deferred revenue completeness and the roll-forward | Chapter 6 | The mirror image of the cut-off deficiency in this chapter's case study; Exercise 13-12 spans the two |
| Fraud risk, the signature-date capability, and the six December contracts (U-3) | Chapter 17 | Owns the investigation the OTC-03 precision failure should have triggered in October |
| Journal entry testing, the $250,000 approval threshold (W-12), and top-side entries | Chapter 16 | Develops the close-process observations from step 12 and step 13 of the walkthrough |
| Materiality, performance materiality, and the clearly trivial threshold | Chapter 3 | The $1,450 / $940 / $72 framework used in every precision computation here |
| Accumulating misstatements and the ICFR conclusion | Chapter 19 | Where corrected misstatement C-1 and the aggregated deficiency conclusion are evaluated |
| Reporting the material weakness over revenue cut-off | Chapter 20 | The adverse ICFR opinion that the case study's deficiency ultimately supports |

## Further Reading

- PCAOB AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of
  Financial Statements*, particularly the section on understanding likely sources of potential misstatement
  (paragraphs 34 and 37) and the sections on testing design effectiveness and testing operating effectiveness.
- PCAOB AS 2110, *Identifying and Assessing Risks of Material Misstatement*, on obtaining an understanding of the
  system of internal control and on evaluating whether controls relevant to the audit are suitably designed and
  have been implemented.
- PCAOB AS 1105, *Audit Evidence*, on the relative reliability of inquiry, observation, inspection, and
  re-performance, and on information produced by the entity.
- PCAOB AS 1215, *Audit Documentation*, and AS 1201, *Supervision of the Audit Engagement*, which together
  specify what walkthrough documentation must permit a reviewer to do.
- PCAOB AS 2401, *Consideration of Fraud in a Financial Statement Audit*, on inquiries of employees involved in
  processing transactions.
- PCAOB AS 2601, *Consideration of an Entity's Use of a Service Organization*, on the limits of what can be
  learned about a process performed by a service organization.
- PCAOB AS 1305, *Communications About Control Deficiencies in an Audit of Financial Statements*, on the required
  communications arising from findings of the kind in this chapter's case study.
- PCAOB Staff Audit Practice Alert No. 11, *Considerations for Audits of Internal Control Over Financial
  Reporting* (October 2013), on recurring inspection findings including the identification of controls that address
  the risks of misstatement and the evaluation of the precision of management review controls.
- AICPA AU-C 315, as amended by SAS 145, on evaluating the design and determining the implementation of controls,
  and AU-C 330 on the requirement for tests of controls where reliance is intended.
- AICPA AU-C 265 on communicating internal control matters, and AU-C 402 on service organizations, for engagements
  performed under AICPA standards.
- COSO, *Internal Control — Integrated Framework* (2013), particularly Principles 10 and 12 on selecting and
  developing control activities and on deploying them through policies and procedures.
- SEC Release No. 33-8810, *Commission Guidance Regarding Management's Report on Internal Control Over Financial
  Reporting Under Section 13(a) or 15(d) of the Securities Exchange Act of 1934* (June 2007), on management's
  risk-based identification of financial reporting risks and of the controls that address them.
- The AICPA audit guide material on auditing internal control and on service organization control reports, for the
  private-company reader.
