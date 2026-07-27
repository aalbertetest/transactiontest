# Chapter 1 — Audit Planning for SaaS Engagements

> A software-as-a-service company converts a signature into cash over three years, recognizes revenue over a
> fourth, capitalizes the commission it paid on the signature over a fifth, and reports to investors a set of
> operating metrics — annual recurring revenue, net revenue retention, remaining performance obligations — that
> are computed outside the general ledger from data the accounting department does not own. Planning such an
> audit is therefore not a paperwork exercise. It is the point at which you decide whether you understand the
> business well enough to know which of those five timelines can go wrong, by how much, and where the evidence
> lives. This chapter plans the FY2025 integrated audit of AtlasFlow, Inc. — a company that in the same year
> lost its emerging growth company accommodation, hired a first-time public-company CFO, acquired a business
> with no revenue recognition policy, and signed 41% of its fourth-quarter contract value in the last five
> business days of December.

## Learning Objectives

After completing this chapter you will be able to:

- **LO 1.1** Evaluate an engagement continuance decision for a SaaS issuer whose filer status, management
  team, and control environment changed during the year, and document the conclusion and the conditions
  attached to it.
- **LO 1.2** Identify the independence threats that arise specifically from auditing a cloud software vendor,
  including business relationships in which the audit firm is the client's customer, and apply the SEC and
  PCAOB partner rotation requirements to a named engagement team.
- **LO 1.3** Draft the scope paragraphs of an engagement letter for a first-year integrated audit and
  distinguish what the letter must establish from what it merely records.
- **LO 1.4** Distinguish the audit strategy from the audit plan by content, author, timing, and approval, and
  place a given planning decision in the correct document.
- **LO 1.5** Compute and interpret ARR, ACV, TCV, bookings, billings, RPO, NRR, GRR, CAC payback, the magic
  number, and the Rule of 40 from a SaaS company's financial statements, and reconcile bookings to billings to
  revenue to cash.
- **LO 1.6** Explain, metric by metric, the specific accounting pressure each disclosed metric creates, naming
  the account, the assertion, and the direction of the likely misstatement.
- **LO 1.7** Scope an integrated audit by identifying significant accounts and disclosures and their relevant
  assertions, and reconcile the resulting coverage to the financial statements.
- **LO 1.8** Determine the scope of work at each component of a group and draft the component auditor
  instructions that follow from that determination.
- **LO 1.9** Design an interim/year-end timing strategy including the roll-forward procedures required by the
  choice of interim date.
- **LO 1.10** Decide whether and how to use the work of internal audit and of specialists, and document the
  basis for that decision.
- **LO 1.11** Prepare the audit committee planning communication and identify which of its contents are
  required by standard and which are firm practice.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2101, *Audit Planning* | The engagement partner is responsible for the engagement and its performance; requires an audit strategy and an audit plan, consideration of the knowledge obtained from prior audits, and evaluation of whether the firm can perform the engagement with the required competence. Amendments addressing planning and supervision when other auditors participate are effective for audits of financial statements for fiscal years ending on or after December 15, 2024, so FY2025 is the second year they apply to AtlasFlow. |
| PCAOB | AS 1201, *Supervision of the Audit Engagement* | Requires the engagement partner to inform team members of their responsibilities, direct the work, and review it, with the extent of review responsive to risk. |
| PCAOB | AS 1215, *Audit Documentation* | Documentation must permit an experienced auditor with no previous connection to the engagement to understand the work performed and the conclusions reached; the 45-day completion window and the retention period apply. |
| PCAOB | AS 1206, *Dividing Responsibility for the Audit with Another Accounting Firm* | Governs the (rare) decision to divide responsibility and make reference to another firm in the report. Effective for fiscal years ending on or after December 15, 2024. Brightline LLP does not divide responsibility for AtlasFlow. |
| PCAOB | AS 1301, *Communications with Audit Committees* | Requires establishing an understanding of the terms of the engagement with the audit committee and recording it in writing, and requires specified planning-stage communications including the overall audit strategy, timing, and significant risks. |
| PCAOB | AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of Financial Statements* | Requires the top-down, risk-based scoping of the ICFR audit; identification of significant accounts and disclosures and their relevant assertions; and the use of the same materiality as the financial statement audit. FY2025 is AtlasFlow's first year subject to this standard. |
| PCAOB | AS 2110, *Identifying and Assessing Risks of Material Misstatement* | Requires the risk assessment procedures whose *outputs* the strategy documents. Chapter 2 owns the mechanics. |
| PCAOB | AS 1210, *Using the Work of an Auditor-Engaged Specialist*; AS 1105 Appendix A on company-engaged specialists | Governs Brightline's use of Dr. Igor Petrov on the Kestrel contingent consideration and the TSR PSU valuation. |
| PCAOB | AS 2605, *Consideration of the Internal Audit Function* | Permits use of internal audit work after assessing competence and objectivity; the extent of use varies inversely with risk. |
| PCAOB | QC 1000, *A Firm's System of Quality Control* | Requires firm-level acceptance and continuance policies, resource sufficiency, and monitoring. Effective December 15, 2025, so it is in force for the AtlasFlow FY2025 engagement, and the engagement-level consequence is a documented, evidenced continuance decision rather than a checkbox. |
| SEC | Regulation S-X Rule 2-01 | Independence: prohibited non-audit services, business relationships, employment relationships, and the five-consecutive-year rotation requirement for the lead and concurring partners (seven years for other audit partners). |
| SEC | Exchange Act Rule 12b-2 | Definitions of accelerated and large accelerated filer, measured on public float at the last business day of the second fiscal quarter. AtlasFlow's June 30, 2025 float of $983.6 million is measured under this rule. |
| SEC | Sarbanes-Oxley Act Sections 404(a) and 404(b); Item 308 of Regulation S-K | Management's assessment and the auditor's attestation, and the disclosures that carry them. Loss of EGC status removes AtlasFlow's exemption from 404(b). |
| SEC | Division of Corporation Finance frequently asked questions on management's report on internal control over financial reporting | The staff position permitting exclusion of a recently acquired business from management's assessment, on which AtlasFlow relies for Kestrel Labs. |
| FASB | ASC 606, *Revenue from Contracts with Customers*; ASC 340-40, *Other Assets and Deferred Costs — Contracts with Customers* | The framework that makes the bookings-to-revenue gap an accounting question rather than a sales question. Chapters 4–6 own the application. |
| FASB | ASC 350-40, ASC 718, ASC 805, ASC 326 | The four other estimate-heavy areas that drive planning decisions on specialists and timing. |
| AICPA | AU-C 210, *Terms of Engagement* | Private-company equivalent of the engagement letter requirement; preconditions for an audit. |
| AICPA | AU-C 220 (as revised by SAS 146), *Quality Management for an Engagement Conducted in Accordance With Generally Accepted Auditing Standards* | Engagement-level quality management; effective for periods ending on or after December 15, 2025. |
| AICPA | AU-C 300, *Planning an Audit* | Strategy and plan requirements; substantively parallel to AS 2101 but without the PCAOB's engagement-partner-specific language. |
| AICPA | AU-C 600 (as revised), *Special Considerations — Audits of Group Financial Statements* | Risk-based approach to determining the scope of work at components; the revision removed the "significant component" classification. Effective for periods ending on or after December 15, 2023. |
| AICPA | AU-C 610, *Using the Work of Internal Auditors*; AU-C 620, *Using the Work of an Auditor's Specialist* | Private-company equivalents of AS 2605 and AS 1210. AU-C 610 permits using internal auditors to provide *direct assistance*; PCAOB standards do not contemplate direct assistance in the same way, which is the most important substantive difference for a reader auditing a private SaaS company. |
| AICPA | AU-C 260, *The Auditor's Communication With Those Charged With Governance* | Private-company equivalent of AS 1301. |

Two differences between the PCAOB and AICPA frameworks matter enough to state plainly. First, an AICPA
engagement has no ICFR opinion unless separately engaged, so the entire integrated-audit scoping discussion in
§1.6 collapses to "obtain an understanding of internal control sufficient to assess risk and design further
procedures." Second, AU-C 610 permits internal auditors to provide direct assistance under the auditor's
direction, subject to conditions; a PCAOB engagement uses internal audit's *work product* as evidence under
AS 2605 but does not staff the audit with the client's employees. Everything else discussed in this chapter
runs in parallel.

## Prerequisites and Chapter Dependencies

Read this chapter first. It assumes only that you know what an audit opinion is, what debits and credits do,
and that revenue is recognized when a performance obligation is satisfied. It does not assume you know what
net revenue retention is. Chapter 2 (risk assessment) and Chapter 3 (materiality) both depend on this
chapter: Chapter 2 takes the business understanding developed in §1.5 as its input and converts it into
assertion-level risk assessments, and Chapter 3 takes the scoping decisions in §1.6 and §1.7 and attaches
numbers to them. Chapters 11 through 14 develop the ICFR mechanics that §1.6 only scopes. Chapter 19 covers
the completion-stage audit committee communication that is the bookend to §1.11.

## 1.1 Engagement Acceptance and Continuance

Continuance is not acceptance with less work. It is a decision made with more information and therefore held
to a higher standard: the firm knows what went wrong last year and cannot claim surprise. Brightline LLP has
audited AtlasFlow since FY2021, and the FY2025 continuance decision was made on June 12, 2025 — eighteen days
before the float measurement date that would change the engagement's character.

**Exhibit 1-1. Brightline LLP FY2025 continuance evaluation for AtlasFlow, Inc. (WP 1010-01, extract).**

| Factor | FY2024 conclusion | FY2025 change | Effect on the decision |
| --- | --- | --- | --- |
| Integrity of management | Satisfactory | Founding CFO resigned July 2025; Tom Okafor joined September 2025 in his first public-company CFO role | Elevates risk; does not preclude continuance. Requires partner-level involvement in the close and an assessment of whether the CFO can supervise a first-year 404(b) process. |
| Competence of the engagement team | Adequate for a financial-statement-only audit | Integrated audit adds an ICFR opinion; 3,100 production deployments and 20 financially relevant applications | Requires the addition of Farrah Nazari (IT audit senior manager) and Ben Osei, and 940 budgeted IT audit hours versus 240 in FY2024. Resource sufficiency is a QC 1000 firm-level requirement, not a nicety. |
| Ability to complete the engagement on time | 10-K filed within the 75-day accelerated-filer deadline | Large accelerated filer deadline is 60 days: March 2, 2026. Management targets a February 20, 2026 report date | Fifteen days of slack disappear. The timing strategy in §1.8 exists because of this line. |
| Client's control environment | Not opined on; deficiencies communicated informally | Internal audit's July 2025 ITGC readiness assessment identified 14 gaps (W-1 through W-14) | A first-year integrated audit with 14 known gaps and a five-month remediation runway has a realistic probability of an adverse ICFR opinion. Continuance is acceptable only if the firm is prepared to issue one. |
| Related-party and fee pressure | Fees $1,180 thousand | FY2025 fee proposal $2,310 thousand, reflecting the integrated audit | Fee increase is proportionate to the 2,700 additional budgeted hours; no indication of a low-balled fee creating scope pressure. |
| Independence | No exceptions | Brightline's internal operations team subscribes to AtlasFlow Core (see §1.2) | Requires evaluation under Rule 2-01; concluded permissible with conditions. |
| Litigation, regulatory, or reputational exposure | None identified | None identified as of June 12, 2025 | Neutral. The January 2026 whistleblower allegation postdates the decision and is a *reassessment* trigger, not a continuance factor. |

**Conclusion recorded:** continue, with four conditions — (a) partner and EQR involvement in the ICFR scoping
decision by August 31, 2025; (b) a written communication to the audit committee by September 30, 2025 on the
remediation runway; (c) reassessment of continuance if management declines to expand the 404(a) population;
and (d) engagement of the firm's valuation specialist for the Kestrel purchase accounting. Prepared by
G. Lindqvist, June 12, 2025; approved by D. Whitcombe, June 16, 2025; concurred by L. Herrera, June 17, 2025.

The discipline worth internalizing is the fourth column. A continuance memo that lists factors and concludes
"continue" has documented nothing. A continuance memo that says *what changes in the audit because of the
factor* has documented a decision. Conditions (a) through (d) each generated a specific workpaper later in
the year, and each is traceable.

### 1.1.1 What would have made this a decline

Practice varies on where the line sits, and it is worth being explicit about the poles. A firm at the
conservative pole declines or resigns when three conditions coincide: a first-year 404(b) requirement, a
finance leadership team with no public-company reporting experience at the CFO level, and a control
environment with known pervasive IT deficiencies. A firm at the permissive pole continues on any facts short
of integrity concerns, on the reasoning that the audit response — more hours, more senior time, a
substantive-only strategy — can absorb any level of control risk. Brightline sat between the poles: it
continued, but it priced and staffed for an adverse ICFR opinion and told the audit committee so in September.
The facts that would have moved Brightline to decline were (i) management refusing to accept an expanded
404(a) population, because that refusal would signal that the scope of the ICFR audit would be contested all
year, or (ii) evidence that the founding CFO's July 2025 resignation followed a disagreement over accounting.
Brightline inquired specifically about the second point and documented the answer.

## 1.2 Independence in a SaaS Context

Independence questions on a software client have a characteristic shape: the client sells something the audit
firm might want to buy, and the audit firm sells something the client might want to buy. Both directions
create threats, and they are governed by different parts of Rule 2-01.

**Exhibit 1-2. Independence threats evaluated on the AtlasFlow FY2025 engagement (WP 1020-04, extract).**

| # | Fact | Rule 2-01 category | Evaluation | Conclusion |
| --- | --- | --- | --- | --- |
| 1 | Brightline's internal operations group subscribes to AtlasFlow Core, 140 automation seats, $84 thousand annual subscription, purchased at list less the standard 12% volume discount | Business relationship / direct financial interest analysis | A purchase of the audit client's product in the ordinary course of business on the same terms available to other customers of comparable size is a consumer relationship, not a business relationship of the kind Rule 2-01 prohibits. The discount is standard and documented. | Permissible. Documented annually with the order form attached and the discount schedule corroborated. Condition: no co-marketing, no case study, no reference-customer arrangement. |
| 2 | Brightline's advisory practice was asked in March 2025 to assist AtlasFlow with SOX readiness documentation | Prohibited non-audit service (internal control design and implementation) | Designing or implementing the ICFR that Brightline must then audit impairs independence. Assisting management to *write* control descriptions is implementation. | Declined. AtlasFlow engaged a separate third-party provider, co-sourced with internal audit under Michelle Fong. |
| 3 | Brightline provides tax provision assistance | Permitted with pre-approval | Preparing the provision that Brightline audits is a management function if it becomes the client's provision. Brightline provides tax compliance and advisory work; Rebecca Stein audits the provision but does not prepare it. | Permissible with audit committee pre-approval, documented in the minutes. |
| 4 | Dana Whitcombe is in her fourth consecutive year as engagement partner | Partner rotation | Lead partner may serve five consecutive years and must then rotate off for five. FY2026 is Whitcombe's fifth year; FY2027 requires a new lead partner. | Compliant for FY2025. Succession planning starts now, because a first-year lead partner arriving in FY2027 immediately after a possible adverse ICFR opinion is a transition worth managing early. |
| 5 | Luis Herrera is the engagement quality reviewer and is not otherwise involved | Concurring partner rotation and involvement restrictions | Same five-year limit applies to the concurring/EQR partner. Herrera performs no other work on the engagement. | Compliant. |
| 6 | A Brightline senior manager (not on the engagement) interviewed for AtlasFlow's Director of SOX role in May 2025 and withdrew | Employment relationship | The revolving-door provisions and the one-year cooling-off period apply to members of the audit engagement team who become employed by the issuer in a financial reporting oversight role. The individual was never on the AtlasFlow engagement and did not take the role. | No impairment. Documented, with confirmation that the individual had no access to AtlasFlow audit workpapers. |
| 7 | AtlasFlow's Snowflake data warehouse is the source of most audit data extracts, and Brightline requested read-only access to defined views | Not an independence matter but frequently mistaken for one | Read-only access to client data, granted by the client for audit purposes and logged, is evidence gathering. It becomes a problem only if the auditor writes or modifies data. | Permissible. Access request documented in Jira, provisioned by Ray Sandoval, revoked at archive. |

Item 1 is the one staff auditors get wrong, in both directions. Some conclude reflexively that the firm cannot
be a customer of its audit client, which is wrong and would make it impossible to audit any company selling
office software, telecommunications, or cloud infrastructure. Others document nothing, which is also wrong,
because the analysis turns on facts — ordinary course, comparable terms, no promotional entanglement — that
must be evidenced. Attach the order form.

One further SaaS-specific point: audit firms increasingly use their clients' products inside audit delivery
tooling. If Brightline had built its own confirmation-tracking workflow on top of AtlasFlow Core, the firm
would be dependent on the audit client's platform for the operation of the audit itself, and the analysis
changes materially. Ask the question during acceptance, not in February.

## 1.3 The Engagement Letter and the Scope of an Integrated Audit

AS 1301 requires the auditor to establish an understanding of the terms of the engagement with the audit
committee and to record that understanding in writing. Two words carry the weight. *Establish* means the
understanding is reached with the audit committee, not with the CFO who negotiates the fee. *Record* means the
letter is evidence of an agreement that already exists, not the agreement itself. A letter signed in November
for a December year end has failed the first requirement even if it satisfies the second.

For AtlasFlow's first integrated audit, the scope paragraphs changed substantively from FY2024. Here is the
FY2025 language, with the new content marked.

**Exhibit 1-3. Engagement letter scope extract, Brightline LLP to the Audit Committee of AtlasFlow, Inc.,
dated July 21, 2025 (WP 1030-01).**

```text
SCOPE OF SERVICES

1.  We will audit the consolidated balance sheets of AtlasFlow, Inc. and subsidiaries as of
    December 31, 2025 and 2024, and the related consolidated statements of operations,
    comprehensive loss, stockholders' equity, and cash flows for each of the three years in the
    period ended December 31, 2025, and the related notes.

2.  [NEW FOR FY2025] We will also audit the effectiveness of the Company's internal control over
    financial reporting as of December 31, 2025. Our audit of internal control over financial
    reporting will be integrated with our audit of the consolidated financial statements. Because
    the Company ceased to qualify as an emerging growth company effective December 31, 2025 and
    is a large accelerated filer for the fiscal year then ended, the auditor attestation
    requirement of Section 404(b) of the Sarbanes-Oxley Act applies for the first time.

3.  [NEW FOR FY2025] Our opinion on internal control over financial reporting will address
    internal control over financial reporting as of December 31, 2025 only, and will not extend to
    internal control over financial reporting at Kestrel Labs, Inc. to the extent management
    excludes that business from its assessment in reliance on the position of the staff of the
    Securities and Exchange Commission permitting exclusion of a recently acquired business, and
    to the extent that exclusion is appropriately supported and disclosed. Management is
    responsible for determining and disclosing the scope of its assessment. We will evaluate
    whether the scope and the related disclosure are appropriate, and whether the excluded
    business gives rise to a risk of material misstatement of the financial statements that we
    must address regardless of the ICFR scope decision.

4.  Management's responsibilities include: preparing the financial statements in conformity with
    accounting principles generally accepted in the United States of America; designing,
    implementing, and maintaining internal control over financial reporting; evaluating the
    effectiveness of internal control over financial reporting and providing us with its written
    assessment; providing us with all financial records and related information; and providing a
    written representation letter at the conclusion of the audit.

5.  [NEW FOR FY2025] Management's written assessment must be provided to us in sufficient time to
    permit our evaluation. We will not begin our as-of-date testing conclusion until management's
    assessment process has produced its own conclusion. If management's assessment is not
    completed, we are unable to complete our audit of internal control over financial reporting.

6.  Our audits will be conducted in accordance with the standards of the Public Company
    Accounting Oversight Board (United States). Those standards require that we plan and perform
    the audits to obtain reasonable assurance about whether the financial statements are free of
    material misstatement, whether caused by error or fraud, and whether effective internal
    control over financial reporting was maintained in all material respects. An audit is not
    designed to detect all misstatements, and because of inherent limitations, an audit of
    internal control over financial reporting is not designed to detect all deficiencies.

7.  Our reports will be addressed to the shareholders and the Board of Directors. We may issue a
    combined report on the financial statements and internal control over financial reporting or
    separate reports; we will inform the Audit Committee of our intended presentation before
    issuance.
```

Paragraph 5 is the paragraph nobody writes and everybody needs. In a first-year 404(b) engagement, management
frequently believes the auditor's testing *is* the assessment. It is not. If management's assessment is
incomplete, the auditor cannot render an opinion on ICFR — a scope limitation, not an adverse opinion. Putting
the dependency in the engagement letter in July gives you the conversation in July rather than in February.
Paragraph 3 does the same work for the Kestrel exclusion: it separates the *ICFR scope* question from the
*financial statement risk* question, which are distinct and are routinely conflated. Kestrel contributed $340
of revenue to the consolidated statements and $19,400 of acquisition-date balances including $14,500 of
goodwill; those balances are audited whether or not Kestrel's controls are in the 404(a) population.

## 1.4 Audit Strategy Versus Audit Plan

These are not synonyms, and the distinction is testable in the sense that a reviewer can look at a decision and
say it is in the wrong document.

**Exhibit 1-4. Strategy and plan compared.**

| Dimension | Audit strategy (WP 1100-02) | Audit plan (WP 1200 series) |
| --- | --- | --- |
| Question answered | What kind of audit is this, and what resources does it require? | What procedures will be performed, by whom, on what population, when? |
| Content | Scope, reporting objectives, timing, materiality (preliminary), the direction of the audit, significant risks identified at planning, resource allocation, the roles of specialists and component auditors, supervision approach | Nature, timing, and extent of risk assessment procedures, tests of controls, and substantive procedures at the assertion level; sample sizes; the assignment of each procedure |
| Level | Engagement | Assertion |
| Author | Senior manager (Grace Lindqvist), approved by the engagement partner | Manager and senior for their areas (Omar Haddad for revenue, deferred revenue, and AR; Chris Nwosu for cash, equity, and controls coordination), approved by the manager and reviewed by the senior manager |
| First dated | July 2025, updated August 29, 2025, October 14, 2025, and January 16, 2026 | Initially October 2025; the revenue programs were revised January 14, 2026 after the whistleblower allegation |
| Communicated to the audit committee | Yes — AS 1301 requires communication of the overall audit strategy, timing, and significant risks | No — the audit committee receives the strategy and the significant risks, not the sample sizes |
| Changes when | Scope, timing, or resources change | Assessed risk at an assertion changes, or a procedure produces an unexpected result |

The strategy for AtlasFlow FY2025 fits on four pages. The plan runs to eighty. If your strategy memo contains
the phrase "we will select a sample of 25 order forms," the sample size has migrated up one level and the
strategy has stopped being readable as a statement of engagement direction. If your plan says "we will respond
to the heightened control risk," the response has migrated down without becoming a procedure.

A practical test: hand the strategy memo to the engagement quality reviewer and the plan to a new staff member.
If the reviewer cannot tell from the strategy how the engagement is shaped, or the staff member cannot execute
from the plan without asking a question, the two documents are wrong regardless of their length.

## 1.5 SaaS Business Model Literacy

You cannot assess the risk of material misstatement in a subscription business you do not understand, and the
understanding required is specific. It is not enough to know that customers pay in advance. You need to know
which number the CEO is compensated on, which number the sell-side analysts model, which number the sales
organization is paid on, and which of those numbers touches the general ledger. In AtlasFlow's case those are
four different numbers.

### 1.5.1 The vocabulary, with AtlasFlow's values

**Exhibit 1-5. SaaS metrics defined and computed for AtlasFlow, FY2025.**

| Metric | Definition | AtlasFlow value | Where the number comes from | In the audited statements? |
| --- | --- | --- | --- | --- |
| **Annual recurring revenue (ARR)** | The annualized contractual run rate of subscriptions active as of a point in time, excluding professional services and usage overage | $172.0M at 12/31/2025; $137.4M at 12/31/2024 | Snowflake RevOps datamart (W-11), not the general ledger | No — MD&A only; other information under AS 2710 |
| **Annual contract value (ACV)** | The subscription value of a single contract expressed on an annualized basis | C-1 Meridian: $600 in year 1, $800 average over the 36-month term | Salesforce CPQ order form | No |
| **Total contract value (TCV)** | Everything the customer has committed to over the full term | C-1: $3,120 ($2,400 subscription + $360 Insight for years 2–3 + $360 implementation) | Order form | No |
| **Bookings** | ACV or TCV of contracts signed in a period. Not a GAAP measure and not consistently defined between companies or, sometimes, within one | Q4 FY2025 new and expansion ACV: $61,400, of which $25,174 (41.0%) signed December 24–31 | Salesforce CPQ, "Closed Won" opportunities | No |
| **Billings** | Amounts invoiced in the period, net of credits | FY2025: $163,750 | Zuora Billing; reconcilable to the deferred revenue roll-forward | Indirectly — it is a derived figure, not a caption |
| **Revenue** | ASC 606 revenue | FY2025: $148,200 | Zuora Revenue → NetSuite via interface I-3 | Yes |
| **Remaining performance obligations (RPO)** | The transaction price allocated to unsatisfied (or partially unsatisfied) performance obligations | $214.0M at 12/31/2025, of which $138.9M (64.9%) expected within 12 months | Zuora Revenue contract population | Yes — a required ASC 606 disclosure, and therefore auditable to a disclosure standard, unlike ARR |
| **Net revenue retention (NRR)** | Current-period recurring revenue from a prior-period cohort, including expansion, divided by that cohort's prior-period recurring revenue | 112% for FY2025; 118% for FY2024 | Snowflake datamart | No |
| **Dollar-based gross retention (GRR)** | The same ratio excluding expansion; it can never exceed 100% | 91% for FY2025; 93% for FY2024 | Snowflake datamart | No |
| **CAC payback** | Months of gross-profit contribution from new ARR required to recover the sales and marketing spend that produced it | 19.6 months (see §1.5.4) | Derived | No |
| **Magic number** | Net new ARR divided by prior-period sales and marketing expense | 0.68 (see §1.5.4) | Derived | No |
| **Rule of 40** | Revenue growth percentage plus a profitability margin | 8.2% on GAAP operating margin; 29.9% on a non-GAAP operating margin; 47.8% on operating cash flow margin | Derived | No |

The single most important column is the last one. RPO is a required disclosure and is therefore inside the
audited financial statements, subject to materiality, and recomputable from a defined population. ARR, NRR,
GRR, and bookings are outside them. That does not make the outside numbers irrelevant — they are other
information under AS 2710 and AU-C 720, they drive the PSU vesting conditions in AtlasFlow's own compensation
plans, and they are the pressure source for most of the accounting risk in this book. But it does mean the
evidence standard differs, and confusing the two is the error described in Mistake 1.6.

### 1.5.2 The bookings → billings → revenue → cash bridge

This is the single most useful planning exhibit for a subscription business, because every gap in it is a place
where a misstatement can hide. Four different numbers describe the same customer commitment at four different
moments, and the differences between them are entirely composed of accounting judgments.

**Exhibit 1-6. AtlasFlow FY2025 bookings → billings → revenue → cash bridge (in thousands).**

| Leg | Line | Amount | Source |
| --- | --- | --- | --- |
| **A. Bookings to live ARR** | New and expansion ACV signed during FY2025 (a) | 98,700 | Salesforce CPQ |
| | Less: ACV with subscription start dates after December 31, 2025 (a) | (51,700) | CPQ start-date field |
| | **ACV live and included in ending ARR** | **47,000** | Ties to Exhibit 1-7 |
| **B. Billings to deferred revenue** | Deferred revenue at January 1, 2025 | 62,300 | §3.2 of the case file |
| | Add: billings, net of credits | 163,750 | Zuora Billing |
| | Add: deferred revenue acquired with Kestrel Labs | 610 | Purchase accounting |
| | Less: foreign currency translation | (260) | Consolidation workbook |
| | Less: revenue recognized from the January 1 balance | (54,900) | Zuora Revenue |
| | Less: revenue recognized from current-period billings | (93,300) | Zuora Revenue |
| | **Deferred revenue at December 31, 2025** | **78,200** | Accounts 2400 + 2405 + 2410 |
| **C. Billings to cash** | Billings, net of credits | 163,750 | Zuora Billing |
| | Less: increase in gross accounts receivable (38,600 − 30,500) | (8,100) | Accounts 1200 + 1205 |
| | Less: write-offs charged against the allowance (b) | (1,230) | Allowance roll-forward |
| | Add: receivables acquired with Kestrel and FX translation, net | 60 | Purchase accounting; consolidation workbook |
| | **Cash collected from customers** | **154,480** | Derived |

Tick marks: (a) FY2025 full-year bookings and the split by start date are not recorded in the continuing-case
file; the figures shown are an illustrative extension, independently corroborated in Exhibit 1-8 against the
deferred commission asset roll-forward, which does tie to the case file. (b) Write-offs are derived as the
opening allowance of $1,350 plus the FY2025 provision of $1,780 less the closing allowance of $1,900.

Three observations to carry into risk assessment.

First, leg B foots exactly: $62,300 + $163,750 + $610 − $260 − $54,900 − $93,300 = $78,200, and the two revenue
lines sum to $148,200, total FY2025 revenue. That is not a coincidence and it is not proof of anything. The
"billings" line in a client-prepared deferred revenue roll-forward is very often computed as a plug — revenue
plus the change in deferred revenue — rather than extracted from the billing system. If it is a plug, the
roll-forward cannot provide evidence about billings, and any analytic built on it is circular. Chapter 6 owns
the procedure that proves it is not a plug; the planning-stage action is to add the independent extraction of
billings from Zuora to the prepared-by-client request list.

Second, leg A is where the pressure lives. Of the $98,700 of new and expansion ACV signed during FY2025, only
$47,000 was live at year end. The other $51,700 produced commissions, quota credit, and a bookings headline in
the Q4 board deck, and produced no revenue at all. A December 30 signature with a January 1 start date is
worth zero FY2025 revenue and full FY2025 commission. That asymmetry tells you where to look: the incentive to
move a signature date across December 31 is enormous in the bookings and commission accounts and small in the
revenue account. AtlasFlow's uncorrected misstatement U-3 is exactly this shape — six December contracts whose
signature dates could not be corroborated, with a revenue effect of only $150 against overall materiality of
$1,450. Chapter 17 develops the scheme. The planning consequence is that you cannot scope the December
signature-date risk by revenue magnitude alone, because the revenue magnitude understates the control failure
it evidences.

Third, leg C reconciles to a number nobody at AtlasFlow computes: cash collected from customers of $154,480.
Compare it to billings of $163,750 and the gap of $9,270 is the year's deterioration in working capital.
Divide the year-end gross receivable of $38,600 by Q4 billings of $52,200 — a figure not recorded in the
continuing-case file, and derived here from the disclosed DSO on AtlasFlow's stated convention of gross
receivables divided by trailing-quarter billings times 92 — and you get 68.0 days of sales outstanding,
precisely the figure AtlasFlow discloses. At the prior year's 61-day velocity,
the same Q4 billings would have supported a receivable of $52,200 × 61 ÷ 92 = $34,604, so approximately $3,996
of the year-end receivable would not have existed. That number — call it $4,000 — is 2.8 times overall
materiality and is the reason the allowance for credit losses is a planned significant risk.

### 1.5.3 The ARR waterfall, NRR, and GRR

ARR moves for five reasons and only five. Decomposing the movement is the fastest way to test whether the
disclosed retention metrics are arithmetically possible, and it takes ten minutes.

**Exhibit 1-7. AtlasFlow FY2025 ARR waterfall (in thousands).**

| Component | Amount | Note |
| --- | --- | --- |
| ARR at December 31, 2024 | 137,400 | Disclosed |
| New customer ARR (642 new logos) | 18,100 | Average landed ARR per new logo $28.2 |
| Expansion ARR from the December 31, 2024 customer base | 28,900 | Seat growth, Insight cross-sell, ramp step-ups |
| Contraction ARR (downgrades, seat reductions) | (6,100) | |
| Churn ARR (192 customers non-renewed) | (6,300) | Average churned ARR per customer $32.8 |
| **ARR at December 31, 2025** | **172,000** | Disclosed |

Recompute the two disclosed retention metrics from the waterfall:

- Retained ARR from the opening base = $137,400 − $6,100 − $6,300 = $125,000.
- GRR = $125,000 ÷ $137,400 = **90.98%**, which rounds to the disclosed 91%.
- NRR = ($125,000 + $28,900) ÷ $137,400 = $153,900 ÷ $137,400 = **112.01%**, which rounds to the disclosed 112%.
- Net new ARR = $172,000 − $137,400 = $34,600, which equals $18,100 + $28,900 − $6,100 − $6,300.

Note what the recomputation does and does not establish. It establishes that the disclosed 112% and 91% are
internally consistent with a decomposition that also ties to the disclosed opening and closing ARR. It does not
establish that the underlying ARR figures are right, because ARR is computed in Snowflake from data that was
not reconciled to the general ledger for the first three quarters of FY2025 (W-11). A metric can be perfectly
consistent and entirely wrong.

The analytical signal is the *composition* of the retention decline. NRR fell 6 percentage points, from 118% to
112%. GRR fell 2 points, from 93% to 91%. So two of the six points came from customers leaving or shrinking,
and four came from the surviving base expanding less. Those two causes have different accounting consequences.
Deteriorating gross retention pressures the allowance for credit losses (account 1210), the impairment
assessment for capitalized commissions on churned customers (§4.2 of the case file records a $1,900 balance
relating to non-renewed customers), and the estimated period of benefit that supports the four-year commission
amortization. Deteriorating expansion pressures the *metric itself*, and therefore pressures the definitional
choices inside the Snowflake calculation, the ARR-based PSU probability assessment, and the temptation to
accelerate expansion signatures into December.

### 1.5.4 Unit economics and the corroboration of bookings

**Exhibit 1-8. Independent corroboration of FY2025 bookings through the deferred contract acquisition cost
roll-forward (in thousands).**

| Line | Amount | Basis |
| --- | --- | --- |
| Deferred contract acquisition costs at January 1, 2025 ($7,900 current + $11,600 noncurrent) | 19,500 | Case file balance sheet |
| New and expansion commissions at 11.8% of $98,700 of ACV | 11,647 | §4.2 commission rate applied to the Exhibit 1-6 bookings figure |
| Renewal commissions at 3.1% of $74,600 of renewed ACV | 2,313 | §4.2 rate; renewed ACV is an illustrative extension |
| Sales manager overrides capitalized | 590 | §4.2 policy |
| Employer payroll taxes at 7.65% of capitalized commissions and overrides | 1,113 | §4.2 policy |
| Less: amounts expensed under the one-year practical expedient (self-serve and monthly contracts) | (1,943) | ASC 340-40 practical expedient |
| **Total FY2025 additions** | **13,720** | |
| Amortization charged to sales and marketing (account 6210) | (8,600) | Case file cash flow statement |
| Write-off of costs relating to churned customers (corrected misstatement C-3) | (620) | Case file Part 7 |
| **Deferred contract acquisition costs at December 31, 2025 ($9,800 + $14,200)** | **24,000** | Case file balance sheet |

Check the footing: $19,500 + $13,720 − $8,600 − $620 = $24,000. The additions line was not given; it was solved
for, and then decomposed using the commission rates and the payroll tax rate. The decomposition reproduces the
$13,720 requirement to the dollar. That is why the $98,700 bookings figure in Exhibit 1-6 is usable: it is not
asserted, it is corroborated against a balance that does tie to the audited financial statements. This is a
technique worth acquiring. When a client gives you an operating metric with no ledger anchor, look for a
balance sheet account whose movement is a known percentage of that metric. Commissions anchor bookings.
Hosting cost anchors usage. Payroll anchors headcount.

Now the unit economics, computed with every input shown.

**Exhibit 1-9. AtlasFlow FY2025 unit economics (dollars in thousands except ratios and months).**

| Metric | Formula | Computation | Result |
| --- | --- | --- | --- |
| Subscription gross margin | (Subscription revenue − cost of subscription revenue) ÷ subscription revenue | ($135,800 − $27,160) ÷ $135,800 = $108,640 ÷ $135,800 | **80.0%** |
| Professional services gross margin | (PS revenue − cost of PS revenue) ÷ PS revenue | ($12,400 − $11,780) ÷ $12,400 = $620 ÷ $12,400 | **5.0%** |
| Total gross margin | Gross profit ÷ total revenue | $109,260 ÷ $148,200 | **73.7%** |
| Revenue growth | FY2025 revenue ÷ FY2024 revenue − 1 | $148,200 ÷ $118,900 − 1 | **24.6%** |
| ARR growth | Closing ARR ÷ opening ARR − 1 | $172,000 ÷ $137,400 − 1 | **25.2%** |
| CAC payback, gross-ARR basis | S&M expense ÷ (new + expansion ARR × subscription gross margin), converted to months | $61,300 ÷ ($47,000 × 0.800) = $61,300 ÷ $37,600 = 1.630 years × 12 | **19.6 months** |
| CAC payback, net-ARR basis | S&M expense ÷ (net new ARR × subscription gross margin) | $61,300 ÷ ($34,600 × 0.800) = $61,300 ÷ $27,680 = 2.214 years × 12 | **26.6 months** |
| Magic number, ARR basis | Net new ARR ÷ prior-year S&M expense | $34,600 ÷ $50,900 | **0.68** |
| Magic number, revenue basis | Change in revenue ÷ prior-year S&M expense | ($148,200 − $118,900) ÷ $50,900 = $29,300 ÷ $50,900 | **0.58** |
| Rule of 40, GAAP operating margin | Revenue growth + operating margin | 24.6% + (−$24,240 ÷ $148,200 = −16.4%) | **8.2%** |
| Rule of 40, non-GAAP operating margin | Revenue growth + (operating loss + SBC + restructuring + intangible amortization) ÷ revenue | 24.6% + ($−24,240 + $28,700 + $1,900 + $1,400 = $7,760; ÷ $148,200 = 5.2%) | **29.9%** |
| Rule of 40, operating cash flow margin | Revenue growth + operating cash flow ÷ revenue | 24.6% + ($34,400 ÷ $148,200 = 23.2%) | **47.8%** |

The Rule of 40 rows are the lesson. The same company, in the same year, scores 8.2, 29.9, and 47.8 depending on
which profitability measure is chosen. The spread of 39.6 points is not noise; it is the sum of the items the
non-GAAP measures exclude. AtlasFlow's $28,700 of stock-based compensation alone is 19.4% of revenue. Its
operating cash flow of $34,400 exceeds its GAAP operating loss of $24,240 by $58,640, composed of $28,700 of
stock-based compensation, $11,900 of depreciation and amortization, $8,600 of amortization of deferred contract
acquisition costs, $4,120 of favorable working capital movement, $1,780 of credit-loss provision, $700 of debt
issuance cost amortization, and $2,840 of net non-operating income — in other words, the cash flow figure is
flattered by the same capitalization policies (commissions under ASC 340-40, internal-use software under
ASC 350-40) that create three of the audit's estimate risks.

The CAC payback rows matter for a specific accounting reason. AtlasFlow amortizes initial commissions over four
years on the basis of an average customer life of 4.3 years. A CAC payback of 19.6 months on the gross basis
supports that. A CAC payback of 26.6 months on the net basis, in a year when gross retention fell to 91%,
supports it less comfortably: at 91% gross retention the implied average customer life is 1 ÷ 0.09 = 11.1
years on a naive calculation, but the *observed* average life is 4.3 years, and the gap between those two
figures is where the estimate is fought. Chapter 10 owns the audit of the amortization period. What planning
owes it is the observation that the input moved adversely this year.

### 1.5.5 Cohort analysis

A cohort table groups customers by the period in which they were acquired and follows each group forward. It
answers a question no aggregate metric answers: is the *newest* business as good as the business it replaced?

**Exhibit 1-10. AtlasFlow enterprise and mid-market ARR by acquisition cohort (in thousands).**

| Cohort | Customers at 12/31/2025 | ARR at cohort landing | ARR at 12/31/2025 | Net retention since landing | Cohort age |
| --- | --- | --- | --- | --- | --- |
| 2020 and earlier | 388 | 20,800 | 27,300 | 131.3% | 6+ years |
| 2021 | 361 | 18,600 | 23,500 | 126.3% | 5 years |
| 2022 | 476 | 24,500 | 29,900 | 122.0% | 4 years |
| 2023 | 573 | 26,800 | 31,600 | 117.9% | 3 years |
| 2024 | 700 | 31,400 | 34,200 | 108.9% | 2 years |
| 2025 | 642 | 18,100 | 18,600 | 102.8% | 1 year |
| Self-serve (11,400 accounts, not cohorted) | n/a | n/a | 6,900 | n/a | n/a |
| **Total ARR at December 31, 2025** | **3,140** | | **172,000** | | |

The customer count foots to the disclosed 3,140 enterprise and mid-market customers and the ARR column foots
to the disclosed $172.0M. The cohort landing ARR and the cohort splits are an illustrative extension; the
totals are not.

Read the fifth column downward and then read it across ages. The 2022 cohort has reached 122.0% of its landing
ARR in four years. The 2024 cohort has reached 108.9% in two. Interpolating the 2022 cohort's trajectory, a
two-year-old cohort of 2022 vintage would have been around 112%. The 2024 cohort is therefore expanding more
slowly than its predecessor did at the same age, by roughly three points. Combine that with the 2025 cohort's
average landed ARR of $28.2 per new logo against a portfolio average of $52.6 ($165,100 of enterprise ARR ÷
3,140 customers) and the picture is a company adding more customers of smaller size that expand more slowly.

That picture has four specific accounting consequences, all of which belong in the planning file:

1. The four-year commission amortization period is supported by a 4.3-year average customer life derived from
   history. If the newest cohorts churn faster, the period is too long and the deferred cost asset of $24,000
   is overstated. Direction of misstatement: assets overstated, expense understated.
2. The CECL allowance's reasonable-and-supportable forecast overlay should reflect a customer base whose
   composition is shifting toward smaller, less sticky accounts. Direction: allowance understated.
3. The ARR-based PSU probability assessment becomes harder to support at 100%, which is precisely what
   happened — management revised it to 85% in Q4 2025, producing a $1,340 catch-up credit.
4. RPO growth of $45.5 million (from $168.5M to $214.0M) against ARR growth of $34.6 million implies the
   average contract is getting longer, not shorter. If cohort quality is falling while contract length is
   rising, either the sales organization is buying length with discounts — which affects the transaction price
   and the discount allocation under ASC 606-10-32-37 — or the contract-term determination is aggressive, which
   affects both revenue and the RPO disclosure. C-5 Pemberton, with its 30-day termination-for-convenience
   clause, is the test case; Chapter 6 develops it.

### 1.5.6 From metric to accounting pressure

Every metric a company publishes creates an incentive at a specific account. Planning is the moment to write
that mapping down, because the mapping *is* the fraud risk assessment's raw material and the risk assessment
matrix's row headings.

**Exhibit 1-11. Metric-to-account pressure map for AtlasFlow FY2025.**

| Metric under pressure | Who is compensated on it | The lever that moves it | Account affected | Assertion | Direction |
| --- | --- | --- | --- | --- | --- |
| Q4 bookings ACV | Sofia Marchetti (CRO) and the sales organization; Q4 "close the quarter" incentives | Signature date on the Salesforce CPQ order form; Brett Hallowell can modify order-form dates | 4100/4110 revenue; 1200 AR; 2105 accrued commissions; 1300/1305 deferred commissions | Occurrence, cut-off, accuracy | Revenue and commission assets overstated |
| ARR | Priya Raghunathan (CEO), whose compensation is weighted to ARR-based PSUs; the ARR-based PSU tranche itself | Definitional choices inside the Snowflake RevOps datamart; inclusion of not-yet-started contracts; annualization of monthly self-serve | Not a ledger account, but drives 3100/SBC expense through PSU probability | Occurrence and accuracy of SBC; accuracy of MD&A | SBC understated if probability is overstated, and vice versa |
| NRR | Sales leadership and the equity story | Cohort definition, treatment of churned customers' prior-year ARR, currency conversion timing | Same as ARR | Accuracy of other information | Metric overstated |
| Revenue growth | All of management | Cut-off; SSP allocation between Core and the new Insight SKU; contract-term determination | 4100, 4110, 4120, 2400, 2410 | Occurrence, accuracy, cut-off, allocation | Revenue overstated, deferred revenue understated |
| Gross margin | The equity story; analysts model subscription gross margin closely | Classification of personnel between cost of subscription (5110) and R&D (6100); capitalization of internal-use software (1560) | 5100, 5110, 5120, 6100, 1560 | Classification, accuracy | Cost of revenue understated, gross margin overstated |
| Operating cash flow and free cash flow | The equity story; convertible note investors watching the $40,000 liquidity covenant | Capitalization rather than expensing; timing of billings and collections; classification within the cash flow statement | 1300/1305, 1560, operating vs. investing classification | Classification, accuracy | Operating cash flow overstated |
| RPO | Disclosed metric watched as a growth indicator | Contract-term determination for termination-for-convenience contracts; inclusion of unenforceable periods | Disclosure only, but the same judgment drives 4100 and 2400 | Completeness and accuracy of disclosure | RPO overstated |
| Rule of 40 and non-GAAP operating margin | Management's public narrative | Which items are excluded from non-GAAP; classification of the $1,900 restructuring charge | 6400 and the non-GAAP reconciliation | Classification, presentation | Non-GAAP margin overstated |

This exhibit is the bridge from Chapter 1 to Chapter 2. Chapter 2 takes each row, states what could go wrong at
the assertion level, assesses inherent risk and control risk separately, and designs a response.

## 1.6 Scoping the Integrated Audit

AS 2201 requires a top-down approach: start at the financial statements, identify significant accounts and
disclosures and their relevant assertions, understand the likely sources of potential misstatement, and select
controls to test. Materiality for the ICFR audit is the same financial statement materiality used in the
financial statement audit — $1,450 for AtlasFlow — which is one of the most frequently misunderstood points in
practice. There is no separate, smaller "ICFR materiality."

An account is significant if there is a reasonable possibility that it could contain a misstatement that,
individually or in combination with others, would be material. Magnitude relative to materiality is the
starting screen, not the test. Contingent consideration of $2,500 is only 1.7 times materiality, but it is
measured by Monte Carlo simulation with a 32% volatility assumption and an 11.5% discount rate, so its
potential misstatement is a large fraction of its carrying amount. Prepaid expenses of $8,100 are 5.6 times
materiality but consist mostly of software subscriptions amortized on a schedule.

**Exhibit 1-12. FY2025 significant account and disclosure scoping (in thousands). Overall materiality $1,450;
performance materiality $940.**

| Account or disclosure | Balance or amount | Multiple of materiality | Relevant assertions | Significant? | Basis |
| --- | --- | --- | --- | --- | --- |
| Revenue (4100, 4110, 4120, 4200, 4210) | 148,200 | 102.2× | Occurrence, completeness, accuracy, cut-off, allocation, presentation | Yes | Magnitude; fraud presumption in revenue recognition; five distinct revenue streams with different recognition models |
| Deferred revenue (2400, 2405, 2410) | 78,200 | 53.9× | Completeness, existence, accuracy, classification (current/noncurrent) | Yes | Completeness is the dominant assertion; the mirror image of revenue overstatement |
| Accounts receivable, net (1200, 1205, 1210) | 36,700 | 25.3× | Existence, accuracy, valuation, cut-off | Yes | Magnitude; DSO deterioration from 61 to 68 days; CECL estimate |
| Contract assets / unbilled receivables (1220) | 3,400 | 2.3× | Existence, accuracy, classification | Yes | Netting rules at contract level; PS input-method estimate |
| Deferred contract acquisition costs (1300, 1305) | 24,000 | 16.6× | Existence, accuracy, valuation | Yes | Estimate-driven (four-year period); impairment exposure on non-renewed customers |
| Capitalized internal-use software, net (1560, 1565) | 18,600 | 12.8× | Existence, accuracy, valuation | Yes | 22% of FY2025 capitalized hours coded to retroactively restaged Jira epics |
| Goodwill and intangibles (1700, 1710, 1715) | 36,600 | 25.2× | Existence, accuracy, valuation, presentation | Yes | Kestrel purchase price allocation; first-time acquirer of scale |
| Contingent consideration (2600) | 2,500 | 1.7× | Accuracy, valuation, presentation | Yes | High measurement uncertainty relative to carrying amount |
| Cash and cash equivalents (1010–1045) | 96,400 | 66.5× | Existence, completeness, accuracy, presentation | Yes | Magnitude; six accounts, four currencies, two banks |
| Short-term investments (1100, 1110) | 54,200 | 37.4× | Existence, accuracy, valuation, classification | Yes | Magnitude; classification and the Harborview policy exception |
| Accrued compensation, commissions, and PTO (2100, 2105, 2110) | 16,400 | 11.3× | Completeness, accuracy | Yes | Commission accrual interacts with the Q4 bookings concentration |
| Accounts payable and accrued expenses (2000, 2200–2230) | 19,500 | 13.4× | Completeness, accuracy | Yes | Completeness; search for unrecorded liabilities |
| Convertible senior notes (2500) | 170,600 | 117.7× | Existence, accuracy, presentation, disclosure | Yes | Magnitude, but a single instrument with contractual terms; low inherent risk, high magnitude |
| Operating leases (1600, 2300, 2305) | 21,700 / 23,400 | 15.0× / 16.1× | Existence, accuracy, classification | Yes | Two leases; low judgment |
| Additional paid-in capital and stock-based compensation (3100; $28,700 of expense) | 412,300 / 28,700 | 284.3× / 19.8× | Occurrence, accuracy, completeness, classification | Yes | Four award types including PSUs with market and performance conditions |
| Income taxes (8000, valuation allowance) | 540 | 0.4× | Accuracy, presentation, disclosure | Yes (disclosure) | Amount is below materiality, but the valuation allowance disclosure and the Kestrel deferred tax liability of $1,300 are significant disclosures |
| Restructuring (6400) | 1,900 | 1.3× | Occurrence, accuracy, completeness | Yes | Discrete, non-recurring, excluded from non-GAAP measures |
| Prepaid expenses and other (1400, 1410) | 8,100 | 5.6× | Existence, accuracy | No | Magnitude exceeds materiality but composition is schedule-driven amortization of software subscriptions with no estimate; substantive analytical coverage is sufficient |
| Other assets and other long-term liabilities | 3,900 / 2,700 | 2.7× / 1.9× | Existence, accuracy | No | Composition tested by scanning; individually below performance materiality |
| RPO disclosure | 214,000 disclosed | n/a | Completeness, accuracy, presentation | Yes | Required ASC 606 disclosure; recomputable from a defined population; contract-term judgment |
| Revenue disaggregation disclosure | 148,200 | n/a | Completeness, accuracy, presentation | Yes | Required; five streams and three geographies |
| Segment disclosure | n/a | n/a | Completeness, accuracy | No | Single reportable segment; conclusion documented, not scoped for testing |

Coverage reconciliation, which every scoping memo should contain and most do not:

| Measure | Amount covered by accounts scoped as significant | Total | Coverage |
| --- | --- | --- | --- |
| Total revenue | 148,200 | 148,200 | 100.0% |
| Total assets | 305,900 | 317,900 | 96.2% |
| Total liabilities | 308,100 | 310,800 | 99.1% |

Total assets covered is $317,900 less prepaid and other current assets of $8,100 less other assets of $3,900,
which equals $305,900. Total liabilities covered is $310,800 less other long-term liabilities of $2,700, which
equals $308,100. Both foot.

The scoping decisions to notice are the two "No" rows. A reviewer will ask why an $8,100 balance is not
significant when materiality is $1,450, and the answer must be about the *reasonable possibility of material
misstatement*, not about magnitude. Prepaid expenses at AtlasFlow consist of $6,300 in account 1400, of which
$4,900 is prepaid software and hosting amortized on straight-line schedules established at invoice date, and
$1,400 is prepaid insurance. There is no estimate, no allocation judgment, and no incentive. The conclusion is
defensible. It would not be defensible if prepaid expenses contained a $3,000 prepaid marketing balance whose
amortization depended on campaign delivery estimates.

Chapters 11 through 14 own everything that follows from this exhibit: the identification of controls to test,
the ITGC scoping, the testing methodology, and the deficiency evaluation. What planning owns is the exhibit
itself, and the resource conclusion that follows from it: 760 hours of process-level control testing and 940
hours of IT audit work, against 90 and 240 respectively in FY2024.

## 1.7 Group Audit Scoping

The FY2025 audit is AtlasFlow's second under the PCAOB's amended group audit requirements, which took effect
for fiscal years ending on or after December 15, 2024. The amendments to AS 2101 require the engagement partner
to determine the extent of the group engagement team's involvement in the work of other auditors and to plan
and supervise that work; AS 1206 governs the separate decision to divide responsibility and make reference to
another firm, which Brightline does not do. The AICPA's revised AU-C 600 reaches a similar destination by a
different route: it removed the "significant component" label and requires a risk-based determination of the
scope of work at each component.

The practical consequence of both frameworks is that you no longer classify components and then apply a
standard scope to each class. You determine, component by component, what work is needed to address the
identified risks of material misstatement in the group financial statements.

**Exhibit 1-13. FY2025 group audit scoping (in thousands).**

| Component | Revenue | % of group revenue | Total assets | % of group assets | Component materiality | Scope determined | Auditor |
| --- | --- | --- | --- | --- | --- | --- | --- |
| AtlasFlow, Inc. (US) | 109,400 | 73.8% | 271,100 | 85.3% | Group materiality applies | Full audit procedures on all significant accounts | Brightline LLP (Austin) — group engagement team |
| AtlasFlow Software Ltd (UK) | 26,300 | 17.8% | 31,600 | 9.9% | 580 (component performance materiality 380) | Full scope: audit procedures on all significant accounts of the component | Brightline UK LLP, London |
| AtlasFlow Pty Ltd (Australia) | 12,500 | 8.4% | 12,900 | 4.1% | 420 | Specified procedures on revenue, deferred revenue, accounts receivable, and payroll; no opinion on component financial information | Group engagement team |
| AtlasFlow India Private Limited | — | 0.0% | 2,300 | 0.7% | n/a | Analytical procedures on the cost-plus intercompany charge; substantive testing of the transfer-pricing markup at the parent | Group engagement team |
| Kestrel Labs, Inc. (merged into parent August 4, 2025) | included in US | — | included in US | — | Group materiality applies | Purchase accounting, opening balance sheet, and post-acquisition revenue of $340 audited at the parent | Group engagement team |
| **Total** | **148,200** | **100.0%** | **317,900** | **100.0%** | | | |

Revenue foots: $109,400 + $26,300 + $12,500 = $148,200. Assets foot: $271,100 + $31,600 + $12,900 + $2,300 =
$317,900. Chapter 3 owns the derivation of the $580 and $420 component amounts; note only that component
materiality is set below group materiality to leave room for aggregation risk across components, and that the
UK's $580 is 40% of the group's $1,450.

Three group-audit planning matters deserve specific attention on a SaaS engagement.

**The consolidation is not in the ERP.** Intercompany balances and FX translation run through
CONSOL_FY25_v14.xlsx, a spreadsheet on SharePoint with no version control, no formula-integrity check, and four
people emailing it (W-8). The consolidation is therefore a *group-level process* with its own risks of material
misstatement, and 27 manual top-side entries totaling $6,200 were posted in it, outside NetSuite, during
FY2025. Those entries are not in the 41,610-entry NetSuite journal population and will be missed by any journal
entry analytic that starts from NetSuite. Add the top-side population to the group audit instructions and to
the Chapter 16 journal entry scope explicitly.

**Contracting entity is not the same as customer location.** C-2 Voltaire Logistics is contracted in EUR
through the UK entity, whose functional currency is GBP, and reported in USD. Three currencies and two
translations sit between the order form and the income statement. When you instruct the UK component auditor,
instruct them on the *contract* population by contracting entity, not by customer geography, or you will get a
population that does not reconcile.

**Specified procedures are instructions, not a scope reduction you announce.** The Australia decision is
developed as this chapter's extended case study, including the actual instruction language.

## 1.8 Timing, Interim Procedures, and Roll-Forward

AtlasFlow's filing deadline compressed from 75 days to 60 days when it became a large accelerated filer: the
FY2025 Form 10-K is due March 2, 2026 rather than March 16, and management targets a February 20 report date. At
the same time the audit's hour requirement roughly doubled. The only way both facts coexist is to move work
earlier, which means interim testing and roll-forward.

**Exhibit 1-14. FY2025 audit calendar (WP 1100-05).**

| Date | Activity | Deliverable or workpaper |
| --- | --- | --- |
| June 12, 2025 | Continuance evaluation | WP 1010-01 |
| July 21, 2025 | Engagement letter signed by the audit committee chair | WP 1030-01 |
| August 18–29, 2025 | Update of entity and environment understanding; preliminary analytical procedures on Q1–Q2 results | WP 2100 series |
| September 8–19, 2025 | Process walkthroughs: order-to-cash, close, procure-to-pay, payroll, equity | WP 3100 series (Chapter 13) |
| September 30, 2025 | Audit committee planning communication | WP 1400-01 |
| October 7, 2025 | Engagement team discussion, including fraud brainstorming | WP 2200-01 (Chapter 2 walkthrough) |
| October 14, 2025 | Audit strategy memo finalized and approved | WP 1100-02 |
| October 20 – November 21, 2025 | Interim tests of controls covering January 1 – October 31, 2025 | WP 4000 series |
| November 3–14, 2025 | Interim substantive procedures: revenue testing for January–September; capitalized software additions through September 30 | WP 5100, 5600 series |
| December 1–12, 2025 | ITGC testing; Kestrel purchase accounting and valuation specialist review | WP 4200, 5800 series |
| December 15, 2025 | Review of the November 30 hard close; early look at Q4 bookings pacing | WP 2100-09 |
| January 5, 2026 | Accounts receivable confirmations mailed under Brightline control | WP 5300-02 |
| January 12–30, 2026 | Year-end fieldwork | WP 5000 series |
| January 14, 2026 | Revenue audit programs revised following the audit committee's receipt of the whistleblower email | WP 1200-04 rev. 2 |
| February 2–13, 2026 | Roll-forward of controls testing for November 1 – December 31; completion procedures | WP 4900, 6000 series |
| February 16, 2026 | Engagement quality review completed | WP 7000-01 |
| February 18, 2026 | Audit committee meeting: results, uncorrected misstatements, ICFR conclusion | WP 6800-01 |
| February 20, 2026 | Report date; Form 10-K filed | WP 7100 series |
| April 6, 2026 | Documentation completion date, 45 days after the report date | Archive log |

### 1.8.1 Choosing the interim date

October 31 was chosen for controls testing, not September 30 and not November 30, for four reasons that are
worth making explicit because the reasoning generalizes.

1. **Remaining-period length.** Testing as of October 31 leaves a 61-day roll-forward period. AS 2201 requires
   the auditor to update testing to the as-of date, and the extent of the update varies with the length of the
   remaining period. Sixty-one days is short enough that roll-forward inquiry plus limited re-testing is
   defensible for most controls; a June 30 interim date, leaving 184 days, would not be.
2. **Control population availability.** The quarterly user access reviews (W-3) and the monthly RevPro-to-GL
   reconciliations both have an October instance, so an October 31 date captures a full set of instances for
   both frequencies without waiting.
3. **Known change events.** The NetSuite upgrade occurred in September 2025 and the segregation-of-duties roles
   were rebuilt during it. Testing access controls as of a date *after* the rebuild tests the configuration that
   will exist at year end. Testing as of August 31 would have tested a configuration that no longer exists, and
   the entire population would need retesting.
4. **Client capacity.** AtlasFlow's finance team is thin and the CFO started in September. Loading control
   evidence requests into November leaves the December close and the Q4 reporting cycle clear.

### 1.8.2 Roll-forward procedures actually performed

Roll-forward is not a formality and is not satisfied by inquiry alone. Brightline's approach, calibrated to the
control's significance and to what happened at interim:

| Control category | Interim result | Roll-forward procedure for November 1 – December 31 | Why |
| --- | --- | --- | --- |
| Monthly RevPro-to-GL reconciliation (Jordan Pike prepares, Controller reviews) | No deviations in 10 monthly instances | Inspect the November and December instances and re-perform the December reconciliation | Significant control over a significant account; two of twelve instances is proportionate to a 61-day remaining period |
| Quarterly user access reviews for Salesforce, Zuora, NetSuite | Deviation: performed annually, not quarterly; Q2 completed 41 days late (W-3) | No roll-forward. The control did not operate as designed at interim, so there is nothing to roll forward; the deficiency is evaluated under Chapter 14 and the substantive strategy is designed without reliance | A failed control is not rolled forward. Testing it again at year end does not repair the interim result |
| NetSuite journal entry approval configuration ($250,000 threshold, W-12) | Configuration confirmed; design deficiency identified because 3,847 of 4,912 manual entries fell below the threshold | Confirm the configuration was unchanged at December 31 by inspecting the configuration screen and the change log | Design deficiency, not an operating failure; the roll-forward question is only whether the configuration changed |
| Terminated-user access removal (W-5, 6.2-day average against a 24-hour SLA) | Deviation | Obtain the November–December termination list and test 100% of it (11 terminations, including 4 from the October restructuring) | Small population; the October restructuring eliminated 41 positions, so the year-end population is both larger and higher risk |
| Salesforce CPQ discount approval configuration | No deviations in 25 order forms | Test 8 additional order forms from November–December, biased toward December 24–31 signatures | The population changed character in the roll-forward period; extent responds to that, not to the calendar |
| Substantive revenue testing (January–September tested at interim) | 14 contracts with a provisioning-date error, corrected as C-1 ($410) | Extend testing to October–December with an increased sample, plus a full-population cut-off analytic on December contracts | An interim misstatement of $410 against performance materiality of $940 means the interim conclusion does not extend to the untested period by assumption |

The third row is the one to internalize. Roll-forward extent is a function of what interim testing found, not
of the number of days remaining. Two deviations at interim generally mean the roll-forward is a fresh test, not
an update.

## 1.9 Using Specialists and the Work of Internal Audit

### 1.9.1 Specialists

Three distinct roles get called "specialist" and they are governed differently. An **auditor-engaged
specialist** is engaged by Brightline and works under AS 1210: the engagement team evaluates the specialist's
knowledge, skill, and objectivity, informs the specialist of the work required, and evaluates the work. A
**company-engaged specialist** is engaged by AtlasFlow and produces evidence the auditor evaluates under
AS 1105 Appendix A. An **engagement team member with specialized skill** — Farrah Nazari on IT, Tara Iyer on
data analytics — is not a specialist at all; they are audit staff and are supervised under AS 1201.

**Exhibit 1-15. Specialist and internal audit planning decisions (WP 1100-07).**

| Area | Who | Role | Scope of work planned | How Brightline evaluates it |
| --- | --- | --- | --- | --- |
| Kestrel contingent consideration, $2,500 fair value | Dr. Igor Petrov, Brightline valuation | Auditor-engaged specialist (AS 1210) | Independent reasonableness range for the earn-out using the 32% revenue volatility and 11.5% risk-adjusted discount rate, plus sensitivity to each; evaluation of the Monte Carlo model's calibration to the $4,000 maximum payout | Engagement team defines the objective in writing, provides the contract and forecast, reviews the model logic, and evaluates whether Petrov's range covers management's point estimate |
| TSR market-condition PSUs, 210 thousand units, $4,100 unrecognized | Dr. Igor Petrov | Auditor-engaged specialist | Recompute the Monte Carlo grant-date fair value for the two grant tranches; test the peer group and the correlation inputs | Same |
| Developed technology and customer relationship intangibles, $6,900 and $1,100 | AtlasFlow's third-party valuation firm | Company-engaged specialist | Brightline evaluates the report: methodology, discount rate, revenue and attrition assumptions, and consistency with the forecast used for goodwill | AS 1105 Appendix A: assess competence and objectivity of the company's specialist and test the data and assumptions |
| Income tax provision and valuation allowance | Rebecca Stein, Brightline tax partner | Engagement team member with specialized skill | Audit the $540 provision, the $1,300 Kestrel deferred tax liability, and the valuation allowance assessment | Supervised under AS 1201 as part of the engagement team |
| SSP for Insight and the reseller principal-versus-agent conclusion | Priya Chandrasekhar, national office | Consultation, not a specialist engagement | Concurrence on the technical conclusions before the report date | Consultation documented, including the facts presented and the conclusion reached, per AS 1215 |
| ITGC and IT-dependent controls | Farrah Nazari, Ben Osei | Engagement team members with specialized skill | 940 budgeted hours across 20 applications, 9 interfaces, and the 14 known gaps | Supervised under AS 1201; conclusions reviewed by the senior manager and partner |

The judgment worth flagging: the case for engaging Petrov on the contingent consideration is not the $2,500
magnitude, which is 1.7 times materiality. It is that the measurement is model-based with unobservable inputs,
that AtlasFlow has never done this before, and that a 500-basis-point change in the discount rate or a 10-point
change in the volatility assumption moves the fair value by more than the clearly trivial threshold of $72. A
defensible alternative is to have the engagement team test the model with a documented sensitivity analysis and
no specialist. That alternative is weaker here because nobody on the engagement team can independently assess
whether a Monte Carlo simulation of a revenue-and-retention earn-out is calibrated correctly, and the firm's
policy requires specialist involvement for Level 3 measurements above a threshold. Say which of those two
reasons is driving you; the second is firm methodology, not a professional requirement.

### 1.9.2 Internal audit

Michelle Fong heads a co-sourced internal audit function that reports to the audit committee and issued the
July 2025 ITGC readiness assessment identifying the 14 gaps. AS 2605 permits Brightline to use internal audit's
work after assessing competence and objectivity, with the extent of use varying inversely with the risk of the
assertion involved. Under AICPA standards, AU-C 610 additionally permits internal auditors to provide direct
assistance under the auditor's direction; that route is not available on a PCAOB engagement and readers
auditing private SaaS companies should not assume the two frameworks are interchangeable here.

Brightline's conclusions:

- **Objectivity: acceptable.** Fong reports functionally to the audit committee, not to the CFO. The
  co-sourcing provider is not Brightline and has no other engagement with AtlasFlow. The July readiness
  assessment was critical of management, which is corroborative evidence of objectivity rather than a
  representation about it.
- **Competence: acceptable for ITGC documentation, not for revenue.** The co-source team includes two IT
  auditors with relevant certifications. It includes nobody with ASC 606 experience, and the readiness
  assessment did not address revenue recognition.
- **Extent of use.** Brightline uses internal audit's process documentation as a *starting point* for its own
  walkthroughs (which reduces walkthrough hours but produces no audit evidence), and uses internal audit's
  testing of low-risk ITGCs — specifically, computer operations controls over job scheduling and backup — as
  evidence after re-performing a subset. Brightline does **not** use internal audit's work for any control over
  revenue, deferred revenue, or the RevPro configuration, because those assertions carry the highest assessed
  risk and AS 2605's inverse relationship therefore requires the auditor to do the work.
- **Re-performance.** For the ITGC areas where internal audit's work is used, Brightline re-performs 25% of
  internal audit's tested items, and if any re-performed item does not reproduce internal audit's conclusion,
  Brightline abandons the use of internal audit's work in that area entirely rather than expanding the
  re-performance sample. State that decision rule in advance; deciding it after you find a discrepancy is how
  scope creep becomes rationalization.

## 1.10 Supervision, Review, Resources, and Documentation

AS 1201 assigns the engagement partner responsibility for the engagement, requires that team members be
informed of their responsibilities and of the matters that could affect the procedures they perform, and
requires that the review of work be responsive to risk. The word "responsive" is doing real work: a uniform
review standard applied to every workpaper is a failure of supervision, because it spends the same reviewer
attention on the prepaid expense rollforward and on the Insight SSP memo.

**Exhibit 1-16. FY2025 hours budget by workstream, compared to FY2024 actual.**

| Workstream | FY2024 actual hours | FY2025 budget hours | Change |
| --- | --- | --- | --- |
| Planning, risk assessment, and scoping | 210 | 340 | 130 |
| Revenue and deferred revenue | 620 | 880 | 260 |
| Accounts receivable and credit losses | 180 | 240 | 60 |
| Cash and investments | 90 | 110 | 20 |
| Equity and stock-based compensation | 150 | 220 | 70 |
| Expenses, accruals, and capitalized costs | 260 | 380 | 120 |
| Business combination (Kestrel) | — | 190 | 190 |
| Income taxes | 120 | 150 | 30 |
| IT audit (ITGC and application controls) | 240 | 940 | 700 |
| Process-level control testing (non-IT) | 90 | 760 | 670 |
| Group audit: instructions, review, component coordination | 110 | 180 | 70 |
| Journal entry testing and required fraud procedures | 130 | 210 | 80 |
| Completion, reporting, and engagement quality review | 340 | 520 | 180 |
| Specialists (valuation and tax specialist hours) | 100 | 220 | 120 |
| **Total** | **2,640** | **5,340** | **2,700** |

The budget more than doubles, and 1,370 of the 2,700 additional hours — 50.7% — are control testing. That is the
arithmetic of a first-year 404(b) audit, and it is the number the audit committee needs in September, not in
February.

Review responsiveness, expressed as a rule rather than an aspiration:

| Area | Preparer | Detail reviewer | Second-level review | Partner review |
| --- | --- | --- | --- | --- |
| Insight SSP conclusion | Omar Haddad (manager) | Grace Lindqvist (senior manager) | National office consultation (Chandrasekhar) | Yes, plus EQR |
| December revenue cut-off testing | Amelia Trent (staff) | Omar Haddad | Grace Lindqvist | Yes, plus EQR |
| Allowance for credit losses | Omar Haddad | Grace Lindqvist | — | Yes, plus EQR |
| Kestrel purchase accounting | Chris Nwosu (senior) | Omar Haddad | Petrov (specialist input) | Yes, plus EQR |
| ITGC conclusions and aggregate deficiency evaluation | Ben Osei | Farrah Nazari | Grace Lindqvist | Yes, plus EQR |
| Prepaid expenses, other assets, leases | Jae-won Park (staff) | Chris Nwosu | — | Risk-based sample of workpapers only |
| Cash and bank reconciliations | Amelia Trent | Chris Nwosu | — | Risk-based sample only |

Documentation is governed by AS 1215 and its standard is behavioral: an experienced auditor with no previous
connection to the engagement must be able to understand the nature, timing, extent, and results of the work,
who performed it and when, who reviewed it and when, and the conclusions reached. Two planning-specific
documentation requirements are routinely missed. First, the strategy and plan must be documented, and *changes*
to them must be documented along with the reasons — which is why WP 1100-02 exists in four dated versions and
WP 1200-04 exists in two. Second, the reasons for significant judgments must be recorded, not merely the
judgments; "we concluded the Australia component requires specified procedures" is a conclusion, and the
scoring in Exhibit 1-19 is the reason.

## 1.11 The Audit Committee Planning Communication

AS 1301 requires communications with the audit committee at the planning stage, including the overall audit
strategy, the timing of the audit, and significant risks identified. It also requires establishing an
understanding of the terms of the engagement. What it does not require is a slide deck, and the most common
failure of this communication is that the required content gets buried in one.

**Exhibit 1-17. Audit committee planning communication, September 30, 2025 (WP 1400-01, agenda and content
map).**

| Item | Content communicated | Required by AS 1301, or firm practice? |
| --- | --- | --- |
| 1 | Terms of the engagement, including the first-year ICFR scope and the dependency on management's completed assessment | Required |
| 2 | Overall audit strategy: an integrated audit; interim controls testing as of October 31 with a 61-day roll-forward; full-scope work at the US and UK, specified procedures in Australia, analytical procedures in India | Required |
| 3 | Timing: interim October 20 – November 21; year-end fieldwork January 12–30; targeted report date February 20, 2026; the 60-day statutory deadline of March 2, 2026 | Required |
| 4 | Significant risks identified at planning: revenue occurrence and cut-off (including the Q4 signature-date concentration); Insight standalone selling price; deferred revenue completeness; allowance for credit losses; capitalized software stage classification; PSU probability; Kestrel contingent consideration; management override of controls | Required |
| 5 | Planned use of Dr. Petrov as a valuation specialist and the limited planned use of internal audit's ITGC work | Firm practice; AS 1301 requires communication about other auditors, and Brightline extends the same transparency to specialists |
| 6 | The 14 ITGC gaps from internal audit's July assessment, the remediation runway, and Brightline's statement that on the facts known in September an adverse ICFR opinion was a realistic outcome | Firm practice, and the single most valuable item on the agenda |
| 7 | Independence: the Brightline subscription to AtlasFlow Core, the declined SOX readiness engagement, tax service pre-approval, and Whitcombe's rotation clock | Required for the annual independence communication |
| 8 | Fees: $2,310, of which $760 relates to the ICFR opinion | Firm practice; audit committee pre-approval is an SEC requirement |
| 9 | Request: the committee's views on fraud risk, and any knowledge of allegations | Required — inquiry of the audit committee about fraud risk is a required risk assessment procedure |
| 10 | Executive session with no management present | Firm practice, and where item 9 actually gets answered |

Item 6 is the item that changes outcomes. Telling an audit committee in September that an adverse ICFR opinion
is on the table gives the committee five months to hold management accountable for remediation and eliminates
the February conversation in which the committee says it was never warned. Item 9 must be asked in executive
session; the answer to "are you aware of any allegations of fraud" is different when the CFO is at the table.
The January 2026 whistleblower email came to the audit committee, and the committee's willingness to route it
to Brightline within days was a consequence of the September conversation.

Chapter 19 owns the completion-stage communication: uncorrected misstatements, significant accounting
practices, difficulties encountered, and the ICFR conclusion.

## Step-by-Step Walkthrough: Building the FY2025 Audit Strategy Memo from the Prior-Year File

Grace Lindqvist has the FY2024 audit strategy memo (WP 1100-02, dated August 8, 2024, six pages) and the
FY2024 archive. She has to produce WP 1100-02 for FY2025 by October 14, 2025. What follows is what she actually
does, in order. The trap this walkthrough is designed to defeat is the one every senior manager knows: opening
last year's memo, changing the dates, and calling it planning.

**Step 1. Retrieve the prior-year strategy memo and the prior-year "significant matters and lessons learned"
memo, and read the second one first.** Open WP 1100-02 (FY2024) and WP 6900-02 (FY2024 completion memo,
significant matters section). Reading the completion memo first inverts the natural order and is the whole
trick: it tells you what the FY2024 strategy got wrong. FY2024's significant matters recorded three items — the
SSP analysis for Core took four weeks longer than budgeted because the client's supporting population was
unusable; the RevPro-to-GL reconciliation was provided nine days late in three of twelve months; and the
capitalized software testing found a $310 error that management corrected. Each becomes an FY2025 strategy
input. *If the completion memo has no significant matters section, that is itself a finding about the prior
year's documentation, and you must reconstruct from the review notes and the summary of audit differences.*

**Step 2. Build the change register: what is different about the entity this year.** Create a two-column
schedule, "FY2024 condition" and "FY2025 condition," and populate it from the client's Q1–Q3 10-Qs, the board
and audit committee minutes for January through August 2025, the July 2025 internal audit readiness
assessment, and inquiry of Elena Vasquez. Fourteen rows result, of which nine change the audit: EGC status
lost; large accelerated filer; first 404(b) year; CFO replaced; VP Revenue Accounting on a performance plan and
two revenue accountants resigned; the Insight SKU launched; the RevPro February 2025 configuration change; the
Kestrel acquisition; the September NetSuite upgrade. *If the change register has fewer than five rows for a
company of this profile, you have not read the minutes.*

**Step 3. Recompute the filer status yourself.** Do not accept management's conclusion. Obtain the June 30,
2025 closing price and the share count held by non-affiliates from the transfer agent report and the Section 16
filings, compute the float, and compare to $700,000. Brightline's recomputation produced $983.6 million against
the $700 million threshold, a 40.5% cushion, and confirmed that AtlasFlow also completed its fifth fiscal year
after the April 2022 IPO registration statement. Conclusion: large accelerated filer for FY2025, EGC status
lost effective December 31, 2025, and Section 404(b) applies. *If the float had come in between $560 million
and $700 million, the answer changes and so does the entire engagement; recompute rather than rely, because the
consequence of being wrong is an unnecessary or a missing ICFR opinion.*

**Step 4. Update the understanding of the business model and refresh the metric exhibits.** Rebuild
Exhibits 1-5 through 1-11 with FY2025 data. Concretely: pull ARR and NRR from the Snowflake RevOps datamart,
pull the deferred revenue roll-forward from Elena Vasquez, extract billings from Zuora Billing independently of
the roll-forward, and recompute GRR and NRR from the waterfall. Brightline's recomputation produced 90.98% and
112.01% against disclosed 91% and 112%. *If your recomputed NRR differs from the disclosed figure by more than
half a point, do not adjust your calculation to match; find out which definitional choice explains the
difference and document it, because that choice is the risk.*

**Step 5. Draw the bookings-to-cash bridge and identify the gaps.** Produce Exhibit 1-6. The output that
matters is not the bridge but the observation that $51,700 of FY2025 signed ACV produced zero FY2025 revenue and
full FY2025 commissions, which sets up the significant risk in §1.11 item 4. *If the bridge does not foot,
you have either the wrong billings figure or an unidentified reconciling item; a bridge that requires a plug is
a bridge that has told you where the audit issue is.*

**Step 6. Corroborate the operating metrics against a ledger anchor.** Produce Exhibit 1-8. Solve for the
required additions to deferred contract acquisition costs ($13,720) from the roll-forward, then decompose it
using the 11.8% and 3.1% commission rates and the 7.65% payroll tax rate. *If the decomposition misses by more
than the clearly trivial threshold of $72, either the bookings figure is wrong or the commission rates are not
what the policy says; both are worth knowing in October.*

**Step 7. Set preliminary materiality and record it as preliminary.** Chapter 3 owns the derivation. For the
strategy memo, record overall materiality of $1,450 based on approximately 1% of forecast FY2025 revenue of
$148,200, performance materiality of $940 (65%), and a clearly trivial threshold of $72 (5%), and record the
FY2024 comparatives of $1,190 and the reason for the increase. Record the *trigger* for revision: a revenue
outcome outside the range $141,000 to $155,000. *If Q4 revenue comes in above $155,000, revisit materiality
before completing year-end testing, not after; Chapter 3, §3.9 covers the consequences of late revision.*

**Step 8. Perform the scoping analysis for significant accounts and disclosures.** Produce Exhibit 1-12 from
the September 30, 2025 trial balance annualized, then update it for actual year-end balances in January. Include
the coverage reconciliation. *If your coverage of total revenue is below 100%, name the excluded stream and
justify it; for AtlasFlow the self-serve $6,100 is individually immaterial and collectively material and cannot
be excluded.*

**Step 9. Determine the scope of work at each component.** Produce Exhibit 1-13. Score Australia explicitly
(see the extended case study). Issue the group audit instructions to Brightline UK LLP by October 24, 2025,
specifying component materiality of $580, component performance materiality of $380, the reporting deadline of
January 23, 2026, the required deliverables, and the specific risks the UK team must address — the EUR-contracted
C-2 Voltaire renewal with its $200 material right, the accrued VAT understatement that became corrected
misstatement C-4 ($180), and the GBP functional currency translation. *If the component auditor's report
arrives without a completed memorandum on the risks you specified, the group team performs the work itself; do
not accept a clean summary with no support.*

**Step 10. Decide the ICFR scope at a high level and confirm it with management in writing.** Establish that
management's 404(a) assessment population excludes Kestrel and obtain management's written support for the
exclusion, its disclosure draft, and the quantification of what is excluded — $340 of revenue, $19,400 of
acquisition-date balances. Confirm that the exclusion does not extend to controls at the parent over the
purchase accounting, which management is asserting on. *If management's excluded scope is larger than the
recently acquired business — for example if it also excludes the Australian entity — challenge it immediately;
the staff position covers recent acquisitions, not inconvenient locations.*

**Step 11. Set the timing and build the calendar.** Produce Exhibit 1-14, working backward from February 20,
2026. Fix the interim date at October 31 and record the four reasons in §1.8.1. *If management cannot commit to
a November 30 hard close, move the interim substantive procedures earlier rather than compressing year-end
fieldwork; compressed fieldwork is where review quality fails.*

**Step 12. Build the hours budget by workstream and reconcile it to the fee.** Produce Exhibit 1-16. Compare
each line to FY2024 actual and explain every change above 20%. The output that matters is that 1,370 of the
2,700 incremental hours are control testing. *If the budget does not increase by at least 60% for a first-year
404(b) audit of a company with 20 financially relevant applications and 14 known ITGC gaps, the budget is
wrong, and an underbudgeted engagement produces documentation shortfalls, not savings.*

**Step 13. Staff the engagement and record the competence conclusion.** Name every role, as in the case file
roster. Record specifically that Farrah Nazari and Ben Osei were added, that Tara Iyer's analytics work is
budgeted at 180 hours within the workstreams above, and that Amelia Trent and Jae-won Park require the firm's
ASC 606 training module before revenue testing begins. *If the team lacks a specific competence — nobody with
Monte Carlo experience — the response is a specialist, not optimism.*

**Step 14. Determine the specialist and internal audit strategy.** Produce Exhibit 1-15. Send Dr. Petrov the
written scope for the contingent consideration by November 14, 2025, so the work is complete before year-end
fieldwork rather than during it. Record the 25% re-performance rule for internal audit's ITGC work and the
decision rule for abandoning that use. *If the specialist's scope letter is undated or the objective is
described as "assist with valuation," rewrite it; AS 1210 requires the auditor to inform the specialist of the
work to be performed.*

**Step 15. Write down the significant risks identified at planning, at the assertion level.** This is the
handoff to Chapter 2, and the strategy memo carries the list, not the analysis. Eight risks were listed in
§1.11 item 4. Each names an account and an assertion; none is described as "revenue risk." *If a risk on the
list cannot be stated as an account plus an assertion plus a direction, it is a concern, not a risk, and it
belongs in the change register instead.*

**Step 16. Define the supervision and review approach.** Produce the review responsiveness table in §1.10.
Assign a second-level reviewer to the four areas with the highest assessed risk, and record that the EQR
reviews all four plus the ICFR aggregation conclusion. *If the same person is the detail reviewer for every
area, the engagement has one point of failure and the reviewer will be the constraint in February.*

**Step 17. Draft the audit committee planning communication and calendar it.** Produce Exhibit 1-17.
Distinguish required content from firm practice in the workpaper itself, so a reviewer can confirm the required
items were covered. *If the audit committee meeting slips past the interim start date, communicate the strategy
in writing and confirm receipt; the requirement is a communication, not a meeting.*

**Step 18. Assemble the memo and check it against the standard, item by item.** The finished memo runs four
pages plus exhibits. Its section headings are: scope and reporting objectives; changes since the prior year;
business and metric understanding; materiality (preliminary); significant accounts and disclosures; components
and group scope; significant risks identified at planning; timing and roll-forward; resources, specialists, and
internal audit; supervision and review; audit committee communication; and approval. Tie each heading to the
AS 2101 and AS 1301 requirement it satisfies in a marginal reference column. *If a required element has no
home, you have found a gap; add the section rather than assuming it is covered elsewhere.*

**Step 19. Obtain approval and record it.** Whitcombe approves WP 1100-02 on October 14, 2025. Herrera, as
engagement quality reviewer, reads the strategy memo at that date — not in February — because an EQR who first
sees the engagement's direction after the work is done cannot influence it. *If the partner's approval is dated
after interim procedures began, the memo documented a decision that had already been made without it; fix the
sequence next year and note the exception this year.*

**Step 20. Set the update triggers and actually update.** Record in the memo the events that require a strategy
update: a change in the ICFR scope; a revenue outcome outside the $141,000 to $155,000 range; identification of
a fraud risk not previously identified; a component auditor scope change; or an ITGC conclusion that eliminates
reliance on automated controls. Three triggers fired. WP 1100-02 was updated August 29, 2025 for the Kestrel
acquisition scope, October 14, 2025 at finalization, and — in a fourth version issued January 16, 2026 — for the
whistleblower allegation, which required revising the revenue programs (WP 1200-04 rev. 2) and adding
procedures on the December signature population. *If no trigger ever fires on an engagement of this profile,
the triggers were written to be unfireable.*

## Extended Case Study: The Scoping Decision on AtlasFlow Pty Ltd (Australia)

### Background

AtlasFlow Pty Ltd is the APAC sales and contracting entity, incorporated in New South Wales, with 38 employees
at December 31, 2025 after the October 2025 restructuring consolidated its Sydney and Melbourne offices into
one location. It contracts with APAC customers in AUD, its functional currency, and reports into consolidation
translated at 0.6410 USD/AUD. It generated FY2025 revenue of $12,500 and holds total assets of $12,900. It has
no separate statutory audit report. Its entire finance function is one person: Wei Tan, Financial Controller —
APAC, who prepares the local trial balance, posts local journal entries directly into the AtlasFlow Pty Ltd
subsidiary in NetSuite, and reports to Elena Vasquez in Austin.

In FY2024 Brightline performed analytical procedures only on the Australian entity, on the basis that revenue
of $9,300 was 7.8% of the group and the entity used the parent's systems. In FY2025 the engagement team had to
revisit that decision, for three reasons: the group is now subject to an ICFR opinion; the amended AS 2101
group audit requirements are in their second year of application; and the October restructuring produced
Australia-specific accounting.

### The Facts

**Exhibit 1-18. AtlasFlow Pty Ltd — FY2025 component data (in thousands).**

| Item | Amount | Multiple of group materiality ($1,450) | % of group total |
| --- | --- | --- | --- |
| Revenue | 12,500 | 8.6× | 8.4% |
| Deferred revenue at 12/31/2025 | 6,300 | 4.3× | 8.1% |
| Accounts receivable at 12/31/2025 | 2,900 | 2.0× | 7.5% |
| Cash (account 1035, AUD) | 3,200 | 2.2× | 3.3% |
| Intercompany receivable from parent | 4,100 | 2.8× | n/a — eliminated |
| Other assets | 2,700 | 1.9× | n/a |
| **Total assets** | **12,900** | **8.9×** | **4.1%** |
| Restructuring charge attributable to the Australia consolidation | 480 | 0.3× | 25.3% of the $1,900 group charge |
| — of which redundancy payments under Australian law | 310 | | |
| — of which lease and site exit costs | 170 | | |
| Manual journal entries posted to the AU subsidiary in NetSuite during FY2025 | 84 entries, $3,100 absolute value | | 1.7% of the 4,912 group manual entries |
| Component materiality determined | 420 | 29.0% of group materiality | |

Total assets foot: $3,200 + $2,900 + $4,100 + $2,700 = $12,900. The revenue, asset, and materiality figures come
from the continuing-case file; the account-level composition, the $480 restructuring allocation, and the journal
entry count are illustrative extensions.

Four further facts drove the analysis:

1. **The Australian entity has no separate systems.** APAC opportunities are quoted in the same Salesforce CPQ
   instance, activated into the same Zuora Billing tenant, and processed by the same Zuora Revenue
   configuration as US and UK contracts. The process-level revenue controls that apply to an Australian
   contract are the *group's* controls, operated in Austin, and they are in the ICFR scope regardless of the
   component scoping decision.
2. **Wei Tan can post unapproved journal entries.** NetSuite requires a second approver only above $250,000
   (W-12). All 84 AU manual entries are below that threshold and none carries evidence of independent review.
3. **One APAC arrangement raises a principal-versus-agent question.** Aeropath Group, with a year-end
   receivable of $740, is sold through a global systems integrator. AtlasFlow's §4.4 conclusion is that it is
   the principal for the subscription; whether the same conclusion holds for the APAC integrator's
   implementation services is a component-specific question.
4. **Payroll runs through Deel**, whose SOC 1 Type 2 report for October 1, 2024 – September 30, 2025 is
   *qualified* as to one control objective related to change management, and for which no bridge letter was
   obtained for the October 1 – December 31, 2025 gap period (W-9).

### What the Engagement Team Did

Chris Nwosu prepared a scoring analysis rather than a narrative, so that the reasoning could be reviewed and
so that next year's team can see what would change the answer.

**Exhibit 1-19. Component scope decision analysis — AtlasFlow Pty Ltd (WP 1250-03).**

| Criterion | Evidence | Points toward analytical procedures only | Points toward specified procedures | Points toward full scope |
| --- | --- | --- | --- | --- |
| Magnitude of revenue relative to group materiality | 8.6× | — | Revenue materially exceeds group materiality; analytical procedures cannot reduce RMM to an acceptable level on its own | Not decisive: 8.4% of group revenue does not by itself require a full component audit |
| Magnitude of total assets | 8.9× materiality, 4.1% of group | — | Yes | — |
| Existence of a separate control environment | None — same CPQ, Zuora Billing, Zuora Revenue, and NetSuite instances as the parent | Supports a reduced scope: there is no separate revenue process to walk or test | Yes: the *local* activities that are not covered by group controls are narrow and enumerable | Against: a full component audit would re-test group controls already tested in Austin |
| Component-specific accounting judgments | AUD translation; GST; the $480 restructuring accrual including $310 of statutory redundancy; the Aeropath integrator arrangement | Against — these require substantive work | Yes: four identifiable areas, each testable by specified procedures | Only if the judgments were pervasive rather than enumerable |
| Local statutory audit requirement | None; no separate report is issued | Neutral | Neutral | Against: no local deliverable to leverage |
| Local journal entry risk | 84 manual entries, $3,100, no independent review evidence | Against | Yes: examine 100% | Not required to examine 100% |
| Availability of a component auditor | Brightline has no Australian member firm; the nearest office is Brightline UK LLP | Neutral | Supports group-team execution | Against: engaging an unaffiliated firm introduces its own supervision burden |
| Prior-year approach and prior-year findings | FY2024: analytical procedures only; no misstatements identified in Australia | Supports continuity | Yes: prior-year cleanliness supports a moderate rather than maximum scope | Against |
| Change during the year | Restructuring; first ICFR year; second year of the amended group audit requirements | Against | Yes | Neutral |

The team also computed what analytical procedures alone could achieve. A substantive analytical procedure over
AU subscription revenue built from APAC customer counts and average ACV would have to be precise to better than
$420 — component materiality — on a $12,500 base, or 3.4%. AU revenue grew 34.4% year over year (from $9,300 to
$12,500) with a customer count that grew 21.8%, and the residual is price and mix. Nothing in the available
operational data supports a 3.4% expectation. The analytical-only option therefore fails on precision, which is
where most failed analytics fail; Chapter 18, §18.4 develops the precision requirement in full.

### Analysis

The decision is not "how big is Australia." It is "what risks of material misstatement in the *group* financial
statements arise at or from this component, and what work addresses them." Framed that way, the answer separates
into two buckets.

**Risks addressed by group controls and group testing, requiring nothing at the component.** Subscription
revenue recognition for APAC contracts is performed by the same Zuora Revenue configuration, tested centrally.
The order-to-cash controls, the CPQ discount approval matrix, and the RevPro-to-GL reconciliation all operate
in Austin. Testing them again in Sydney would produce duplicate evidence.

**Risks that exist only at the component and would go untested under an analytical-only scope.** Four:
translation of an AUD trial balance into USD through a spreadsheet with no version control; the $480
restructuring accrual, including $310 of statutory redundancy amounts computed under Australian law by a
one-person finance function; 84 unreviewed manual journal entries; and the Aeropath integrator arrangement's
gross-versus-net conclusion.

Those four risks are enumerable, and each is testable with a defined procedure. That is the definition of a
specified-procedures scope: the group engagement team performs identified procedures on identified balances
without auditing the component's financial information as a whole and without expressing any conclusion on it.
The scope is not a compromise between full and nothing; it is the response that matches the risk profile.

The range of defensible answers is genuinely two wide, not three. Full scope is defensible and would not be
criticized — it is simply more work than the risk requires, and it consumes hours that Exhibit 1-16 shows are
needed elsewhere. Analytical procedures only is *not* defensible in FY2025, because revenue of 8.6 times group
materiality now sits in an entity with four untested component-specific risks and an ICFR opinion attached to
the group. The illustrated answer, specified procedures, sits between them and closer to full scope than the
prior year's approach. What would move it to full scope: Australia adopting its own billing system; APAC
revenue exceeding roughly 15% of the group; the discovery of a misstatement above $420 in any specified
procedure; or the local controller gaining the ability to post consolidation-level entries.

### Resolution and Conclusion

Brightline determined a specified-procedures scope with component materiality of $420, executed by the group
engagement team with two site visits (a remote walkthrough on October 2, 2025 and on-site work January 19–22,
2026). The specified procedures were:

1. Recompute the AUD-to-USD translation of the AtlasFlow Pty Ltd trial balance at the 0.6410 closing rate and
   the average rate for the income statement, and agree the cumulative translation adjustment to the $(1,105)
   accumulated other comprehensive loss roll-forward.
2. Examine 100% of the 84 manual journal entries posted to the AU subsidiary, testing support, business
   purpose, and accounting.
3. Test the $480 restructuring accrual, including agreeing the $310 of redundancy amounts to the statutory
   entitlement calculations for the affected employees and to the cash paid in November and December 2025.
4. Confirm the year-end NAB bank balance of $3,200 directly and test the reconciliation.
5. Test the accuracy and aging of the $2,900 AU receivable balance and include the two largest APAC balances,
   including Aeropath's $740, in the group confirmation population.
6. Read the Aeropath order form and the integrator's implementation contract, and evaluate the
   gross-versus-net conclusion against §4.4.
7. Recompute AU deferred revenue of $6,300 from the Zuora Revenue contract population for the 25 largest APAC
   subscriptions.
8. Test the GST accrual within the $2,900 accrued sales and use / VAT balance for AU-attributable amounts.

Results: no misstatements above $420 were identified in Australia. Two matters were reported to the group team.
The 84 manual entries included 6 with single-word descriptions, which fed the Chapter 16 journal entry
criteria. The Aeropath implementation is performed by the integrator using its own resources, so no
professional services revenue is recorded — consistent with §4.4 and with the two arrangements identified
there.

### Workpaper Extract

```text
================================================================================
BRIGHTLINE LLP                                                    WP 1250-03
AtlasFlow, Inc. — FY2025 Integrated Audit
COMPONENT SCOPING CONCLUSION — ATLASFLOW PTY LTD (AUSTRALIA)

Prepared by:   C. Nwosu (CN)          Date prepared:  September 22, 2025
Reviewed by:   O. Haddad (OH)         Date reviewed:  September 24, 2025
Reviewed by:   G. Lindqvist (GL)      Date reviewed:  September 26, 2025
Approved by:   D. Whitcombe (DW)      Date approved:  October 14, 2025
Updated:       CN, January 26, 2026 — results of specified procedures added

PURPOSE
To determine and document the scope of audit work at AtlasFlow Pty Ltd for the
year ended December 31, 2025, and the group engagement team's involvement, in
accordance with AS 2101 as amended for audits of fiscal years ending on or after
December 15, 2024.

SOURCE OF INFORMATION
(a) NetSuite subsidiary trial balance, AtlasFlow Pty Ltd, 12/31/2025, extracted
    by C. Nwosu on January 14, 2026 (report parameters at WP 1250-03A).
(b) CONSOL_FY25_v14.xlsx, tabs "AU_TB" and "FX_TRANS".
(c) Inquiry of W. Tan (Financial Controller — APAC), October 2, 2025 and
    January 19, 2026; inquiry of E. Vasquez, September 18, 2025.
(d) Internal audit ITGC readiness assessment, July 2025 (observations W-3, W-12).
(e) Salesforce CPQ opportunity extract, APAC territory, FY2025.

PROCEDURES PERFORMED (SCOPING)
1. Quantified component revenue ($12,500), total assets ($12,900), deferred
   revenue ($6,300), and AR ($2,900) and compared each to group overall
   materiality of $1,450.                                              (a) ✓
2. Determined whether the component operates a separate control environment.
   Confirmed through inquiry (c) and inspection of the Zuora Billing tenant
   configuration that APAC contracts are processed in the group's Salesforce
   CPQ, Zuora Billing, and Zuora Revenue instances.                       ✓
3. Identified component-specific accounting judgments: AUD translation; the
   $480 restructuring accrual ($310 redundancy, $170 site exit); 84 unreviewed
   manual journal entries ($3,100); the Aeropath integrator arrangement.   ✓
4. Evaluated whether substantive analytical procedures alone could reduce the
   risk of material misstatement to an acceptably low level. Required
   precision of $420 on a $12,500 base (3.4%) is not achievable from
   available APAC operational data; year-over-year revenue growth of 34.4%
   against customer growth of 21.8% leaves an unexplained price-and-mix
   residual larger than component materiality.                            ✓
5. Determined component materiality of $420 (see WP 1300-02, Chapter 3).    ✓

RESULTS
Specified procedures — not a full component audit and not analytical procedures
only — address the four component-specific risks identified in step 3. The
group engagement team performs the work; no component auditor is engaged.
Component materiality: $420.

Specified procedures 1 through 8 (detailed at WP 1250-04 through 1250-11) were
completed January 22, 2026. No misstatements exceeding $420 were identified.
Two matters reported to the group team: (i) 6 of 84 manual journal entries had
single-word descriptions — referred to WP 6200 (journal entry testing);
(ii) the Aeropath implementation is performed by the integrator on its own
account, and no professional services revenue is recorded, consistent with
management's §4.4 conclusion.

CONCLUSION
The scope of work at AtlasFlow Pty Ltd is appropriate to address the risks of
material misstatement of the group financial statements arising at this
component. Together with full-scope work at AtlasFlow, Inc. and AtlasFlow
Software Ltd and analytical procedures at AtlasFlow India Private Limited,
group audit coverage is 100.0% of consolidated revenue and 96.2% of
consolidated total assets scoped as significant. No matters arising at this
component affect the group ICFR conclusion, because the process-level controls
over APAC transactions are group controls tested centrally.

Tick mark legend:
  ✓  Procedure performed; no exceptions unless noted.
  (a) Agreed to the source identified above without exception.
================================================================================
```

### Lessons

1. **The scoping question is about risk, not size.** Australia is 8.4% of revenue in both FY2024 and FY2025 —
   the percentage barely moved. What moved was the presence of component-specific risks that group controls do
   not reach, and the addition of an ICFR opinion. Reciting last year's percentage would have produced last
   year's answer to a different question.
2. **"Shared systems" is a powerful argument, and it cuts both ways.** It removes the need to test the revenue
   process locally, and it means the local controller's NetSuite access is a *group* control weakness with a
   local manifestation. Do not use shared systems to conclude that nothing local needs testing.
3. **Test the analytical-only option numerically before rejecting it.** "Analytical procedures are not
   sufficient" is an assertion. "Analytical procedures would need to be precise to 3.4% and the available data
   cannot support better than roughly 8%" is a conclusion.
4. **Specified procedures require specified procedures.** The scope conclusion is worthless without the list.
   Eight numbered procedures, each with a population and a threshold, is a scope; "we will perform specified
   procedures over revenue" is a label.
5. **Write down what would change the answer.** Four triggers are recorded in the Analysis section. Next
   year's team will read them in twenty seconds, which is twenty seconds better than rebuilding the reasoning.
6. **Update the workpaper with results.** WP 1250-03 was reopened on January 26, 2026 to record the outcome of
   the procedures it scoped. A scoping memo that is never revisited cannot demonstrate that the scope was
   executed.

## Common Mistakes

### Mistake 1.1 — Rolling forward the prior-year strategy memo without building a change register

**What it looks like.** WP 1100-02 for FY2025 is the FY2024 memo with the dates changed, the materiality figure
updated from $1,190 to $1,450, and a new paragraph headed "Kestrel acquisition." Everything else is identical,
including the sentence describing AtlasFlow as an emerging growth company.

**Why it happens.** The prior-year memo is the most efficient starting point, and efficiency is a virtue right
up to the point where it substitutes for thought. Reviewers also reinforce it: a memo that looks like last
year's raises no questions.

**What goes wrong.** The FY2025 audit's defining fact — the first ICFR opinion — enters the file as an
afterthought rather than as the organizing principle. Downstream, the hours budget is set at prior-year plus
20%, the interim date is chosen by habit, and the audit committee hears about a possible adverse ICFR opinion in
February.

**How to avoid it.** Build the change register (walkthrough Step 2) before opening last year's memo, from the
minutes, the 10-Qs, the internal audit reports, and inquiry. Then open last year's memo and ask, row by row,
what each change does to it. Nine of AtlasFlow's fourteen changes altered the audit.

### Mistake 1.2 — Treating ARR as if it were an audited revenue figure

**What it looks like.** A planning analytic that "reconciles" revenue of $148,200 to ARR of $172.0M, concludes
the 16% difference is explained by "timing," and treats the ARR figure as corroborative evidence about revenue.

**Why it happens.** Both numbers are large, both are labeled revenue-ish, and the client's own MD&A places them
next to each other.

**What goes wrong.** ARR and revenue are not reconcilable without a full bridge, because ARR is a point-in-time
annualized run rate of active subscriptions, excludes professional services and usage overage, includes
contracts whose service period has barely begun, and is computed in a Snowflake datamart that was not
reconciled to the general ledger for three quarters of FY2025 (W-11). Using it as corroboration imports an
uncontrolled number into the audit file as evidence.

**How to avoid it.** Keep the two numbers in separate columns, as in Exhibit 1-5, and label which are inside
the audited financial statements. Use ARR to identify *pressure*, not to corroborate revenue. If you want a
substantive analytic from operational data, build it from seat counts and price per seat, which Chapter 18,
§18.6 develops.

### Mistake 1.3 — Designing the December cut-off test around revenue magnitude

**What it looks like.** The revenue program sizes the December cut-off test using performance materiality of
$940 against the revenue that December contracts would generate in FY2025. Because a December 28 start date
generates only three days of revenue, the computed exposure is tiny and the test is scoped at five contracts.

**Why it happens.** Sizing a substantive test by the magnitude of potential misstatement in the account is
normally correct.

**What goes wrong.** It misses the point of the December population. The $25,174 of ACV signed December 24–31
produced roughly $71 of FY2025 revenue and full FY2025 commission expense, quota credit, and bookings headline.
The financial statement exposure is in accrued commissions ($4,800), capitalized commissions ($24,000), and the
control environment — and the control implication of a fabricated signature date is a potential material
weakness regardless of the revenue amount. AtlasFlow's U-3 is $150 of revenue on six contracts, and it drove a
material weakness conclusion.

**How to avoid it.** Scope the December population by *control significance and fraud risk*, not by revenue
magnitude, and say so in the program. Chapter 2's extended case study designs the response; Chapter 14 evaluates
the deficiency.

### Mistake 1.4 — Using the client's deferred revenue roll-forward as evidence about billings

**What it looks like.** The planning file contains AtlasFlow's roll-forward showing billings of $163,750 and a
tick mark agreeing it to the roll-forward. The billings figure is then used in the DSO analytic, the billings
bridge, and the substantive analytical procedure over deferred revenue.

**Why it happens.** The roll-forward foots, and a schedule that foots feels tested.

**What goes wrong.** In most client-prepared roll-forwards, "billings" is computed as revenue plus the change
in deferred revenue plus reconciling items — that is, it is derived from the two numbers it is being used to
corroborate. Every analytic built on it is circular, and the roll-forward will foot no matter how wrong
billings are.

**How to avoid it.** Extract billings independently from Zuora Billing, agree the extraction to the invoice
register control totals, and reconcile the independent figure to the roll-forward line. Put the extraction on
the prepared-by-client list in October with the field names specified. Treat the roll-forward as information
produced by the entity whose completeness and accuracy must be tested, not as a schedule.

### Mistake 1.5 — Fixing the interim date before finding out when the client changed its systems

**What it looks like.** The engagement calendar sets interim controls testing as of August 31, 2025, because
that is when the team has capacity.

**Why it happens.** Interim dates get set from the firm's resource calendar rather than from the client's event
calendar.

**What goes wrong.** AtlasFlow upgraded NetSuite in September 2025 and rebuilt its segregation-of-duties roles
during the upgrade. Access controls tested as of August 31 test a configuration that no longer exists at
December 31. The entire access-control population requires retesting, and the interim work is wasted — 
approximately 180 hours on this engagement.

**How to avoid it.** Build the client's change calendar first: system upgrades, configuration changes,
reorganizations, acquisitions. Set the interim date after the largest change and long enough before year end to
leave a manageable roll-forward. AtlasFlow's October 31 date satisfies both constraints; §1.8.1 records the four
reasons.

### Mistake 1.6 — Applying the wrong evidence standard to metrics inside and outside the financial statements

**What it looks like.** Two symmetrical failures. In the first, the team recomputes ARR and NRR from the
Snowflake datamart with the rigor of a substantive test of details, spending 60 hours on numbers that appear
only in MD&A. In the second, the team treats the RPO disclosure of $214.0M as a narrative and agrees it to a
client schedule without recomputation.

**Why it happens.** Both numbers look like "metrics," and the distinction between a required ASC 606 disclosure
and a voluntary operating metric is not visible on the page.

**What goes wrong.** The first misallocates hours the ICFR audit needs. The second leaves a required disclosure
untested. RPO is inside the financial statements, is subject to materiality, and is recomputable from a defined
contract population — and AtlasFlow's contract-term judgments on termination-for-convenience contracts like C-5
Pemberton make it a genuine risk. Chapter 6's case study is an $1,860 RPO overstatement.

**How to avoid it.** Use the last column of Exhibit 1-5. Inside the statements: audit to a disclosure standard.
Outside: read for consistency with the audited statements and with your knowledge, under AS 2710 or AU-C 720,
and use it as a pressure indicator in risk assessment.

### Mistake 1.7 — Assuming the ICFR scope exclusion also excludes balances from the financial statement audit

**What it looks like.** The scoping memo records that management excluded Kestrel Labs from its Section 404(a)
assessment, and the audit plan contains no procedures over the Kestrel purchase price allocation, the $610 of
acquired deferred revenue, or the $340 of post-acquisition revenue.

**Why it happens.** The word "excluded" is doing two jobs, and the staff auditor reads it as excluding Kestrel
from the audit.

**What goes wrong.** The Kestrel acquisition contributed $14,500 of goodwill, $8,000 of acquired intangibles,
a $2,500 contingent consideration liability measured by Monte Carlo simulation, and a $1,300 deferred tax
liability — collectively $26,300, or 18.1 times materiality — all of which are audited balances. Kestrel also had no formal
revenue recognition policy and a homegrown billing spreadsheet, which is a completeness and accuracy risk for
the $340 of recognized revenue and for the acquired deferred revenue.

**How to avoid it.** Write the distinction into the engagement letter, as Exhibit 1-3 paragraph 3 does, and into
the scoping memo. Then confirm the boundary of the exclusion: it covers a recently acquired business, and it
does not cover the parent's controls over the purchase accounting, which management is asserting on.

### Mistake 1.8 — Scoping components from a percentage-of-revenue table

**What it looks like.** A one-page schedule listing each component's revenue as a percentage of the group, with
a firm-methodology threshold — full scope above 15%, specified procedures 5% to 15%, analytical below 5% —
applied mechanically. Australia at 8.4% receives specified procedures.

**Why it happens.** The threshold approach is fast, produces consistent answers across engagements, and
survived from an era when AU-C 600 classified "significant components."

**What goes wrong.** It reaches the right answer for the wrong reason, which means it will reach the wrong
answer whenever the risk profile diverges from the size profile. It also fails to identify the four
Australia-specific risks that determine what the specified procedures actually are. And it presents firm
methodology as a professional requirement, which neither AS 2101 as amended nor the revised AU-C 600 supports —
both require a risk-based determination.

**How to avoid it.** Score the criteria, as Exhibit 1-19 does, and let the percentage be one input among nine.
Then enumerate the component-specific risks and derive the procedures from them.

### Mistake 1.9 — Establishing the terms of the engagement with the CFO

**What it looks like.** The engagement letter is negotiated with Tom Okafor in July, signed by him, and
presented to the audit committee for information in the September meeting.

**Why it happens.** The CFO owns the fee, and the fee is what gets negotiated.

**What goes wrong.** AS 1301 requires the auditor to *establish an understanding of the terms of the
engagement with the audit committee*. A letter signed by management and reported to the committee has not
established anything with the committee. Substantively, the two conversations differ: management will not
volunteer the paragraph 5 dependency on its own completed 404(a) assessment, and it is the audit committee that
needs to hear it.

**How to avoid it.** Address the letter to the audit committee, have the chair sign it — Dr. Helen Ashford
signed the AtlasFlow letter on July 21, 2025 — and walk the committee through the scope paragraphs in a meeting
before signature.

### Mistake 1.10 — Handling the firm-as-customer relationship without documentation

**What it looks like.** Either a one-line conclusion ("no independence issues noted") or a reflexive
prohibition ("the firm cannot purchase from an audit client").

**Why it happens.** The analysis feels obvious in whichever direction the preparer's instinct points.

**What goes wrong.** The conclusion in Exhibit 1-2 item 1 depends on facts: 140 seats, $84 of annual
subscription, purchased at list less the standard 12% volume discount available to comparable customers, no
co-marketing, no reference-customer arrangement. Without those facts documented, the file cannot support the
conclusion, and the fact pattern can drift — a co-marketing case study signed by the firm's marketing
department in March changes the answer and nobody will tell the engagement team.

**How to avoid it.** Attach the order form and the vendor's standard discount schedule. Confirm annually, in
writing, that no promotional, referral, or co-marketing arrangement exists. Ask the same question of the firm's
marketing function, not only of the engagement team.

### Mistake 1.11 — Budgeting a first-year integrated audit as prior year plus a percentage

**What it looks like.** FY2024 actual was 2,640 hours; FY2025 is budgeted at 3,300, a 25% increase "for SOX."

**Why it happens.** Fee negotiations are anchored on the prior year, and a doubling is a hard conversation.

**What goes wrong.** Exhibit 1-16 shows that control testing alone accounts for 1,370 incremental hours. A
3,300-hour budget means the ICFR work is performed in roughly 500 hours across 20 financially relevant
applications, 9 interfaces, and 14 known gaps. The consequence is not lower fees; it is unreviewed workpapers,
inquiry-only control testing, and an ICFR conclusion the file cannot support.

**How to avoid it.** Build the budget bottom-up from the scoping exhibit — count the controls, count the
applications, apply the firm's sample-size tables — and reconcile the total to the fee. If the fee will not
support the hours, that is an acceptance-and-continuance matter, not a scoping matter.

### Mistake 1.12 — Deferring the "adverse ICFR opinion is possible" conversation

**What it looks like.** The September audit committee communication describes the ICFR audit approach and notes
that internal audit identified some gaps. The words "material weakness" first appear in the February 18, 2026
communication.

**Why it happens.** Nobody wants to predict an adverse opinion in September on incomplete evidence, and there
is a real professional concern about appearing to have concluded before performing the work.

**What goes wrong.** The audit committee loses five months of remediation leverage over management, and the
February meeting becomes a dispute about warning rather than a discussion about facts. The auditor also loses
the ability to say the committee was informed.

**How to avoid it.** Communicate the *conditional* structure without concluding: on the facts known in
September — 14 identified gaps, a five-month runway, a first-year assessment, and the thin accounting staff — an
adverse opinion is a realistic outcome, and here are the specific gaps whose remediation would change that.
That is a description of the evidence, not a conclusion.

### Mistake 1.13 — Using internal audit's readiness assessment as evidence that controls operated

**What it looks like.** The ITGC workpapers cite the July 2025 internal audit readiness assessment as evidence
about the design and operation of access controls, and the team tests only the gaps internal audit did not
identify.

**Why it happens.** The readiness assessment is thorough, recent, and free.

**What goes wrong.** A readiness assessment identifies gaps; it does not conclude that the remaining controls
operated effectively throughout the period, it was performed as of July rather than as of December 31, and it
predates the September NetSuite upgrade that rebuilt the segregation-of-duties roles. Using it as evidence of
operating effectiveness also skips the AS 2605 assessment of competence and objectivity and the re-performance
that must follow.

**How to avoid it.** Use it as a *risk assessment input* and as a starting point for walkthroughs, both of which
are legitimate and both of which save hours. Use it as evidence only in the areas where competence and
objectivity have been assessed, where the period covered matches, and where Brightline re-performs a subset —
which on this engagement means computer operations controls and nothing touching revenue.

## Practice Exercises

### Exercise 1-1 — ARR waterfall completion [Foundational]

AtlasFlow's FY2024 figures were: ARR at December 31, 2023 of $106,000; ARR at December 31, 2024 of $137,400;
dollar-based gross retention of 93%; net revenue retention of 118%; contraction ARR of $3,420; churn ARR of
$4,000. Compute (a) retained ARR from the opening base, (b) expansion ARR, (c) new customer ARR, and (d) net new
ARR. Show that the waterfall reconciles. All amounts in thousands.

### Exercise 1-2 — ACV, TCV, and overage on contract C-1 [Foundational]

Contract C-1, Meridian Health Systems, was signed March 12, 2025 for a 36-month term running March 15, 2025
through March 14, 2028. Core subscription is on an annual ramp: year 1 $600, year 2 $840, year 3 $960. The
Insight add-on is $180 per year for years 2 and 3 only. Fixed-fee implementation is $360. The contract includes
200,000 workflow runs per year with overage at $12 per 1,000 runs. Meridian consumed 244,000 runs in the first
contract year. Amounts in thousands except the run rate and the overage computation, which are in whole dollars.

Compute: (a) total contract value; (b) ACV on a year-1 basis, subscription only; (c) ACV on an average-of-term
basis, subscription only; (d) ACV on an average-of-term basis including Insight; (e) the exit run-rate ACV at the
end of the term including Insight; (f) the first-year overage charge in whole dollars. Then state the ratio of
the highest ACV measure to the lowest, and one sentence on why the spread matters to the auditor.

### Exercise 1-3 — Cash collected from customers [Intermediate]

For FY2024, AtlasFlow reported: billings net of credits of $131,600; gross accounts receivable of $24,300 at
January 1, 2024 and $30,500 at December 31, 2024; an allowance for credit losses of $1,010 at January 1, 2024
and $1,350 at December 31, 2024; and a provision for credit losses of $1,240. There were no acquisitions and
foreign currency effects on receivables were nil. Compute (a) write-offs charged against the allowance and
(b) cash collected from customers. Then compute (c) the change in cash collected as a percentage of billings
compared with FY2025, for which the corresponding figures are in Exhibit 1-6, and state what the change tells
you.

### Exercise 1-4 — CAC payback and the magic number, two bases each [Intermediate]

For FY2024: sales and marketing expense of $50,900; FY2023 sales and marketing expense of $41,200; subscription
revenue of $108,300 and cost of subscription revenue of $23,140; new plus expansion ARR that went live during
FY2024 of $38,820; net new ARR of $31,400; FY2024 revenue of $118,900 and FY2023 revenue of $91,500. Compute
(a) FY2024 subscription gross margin; (b) CAC payback in months on the gross-ARR basis; (c) CAC payback in
months on the net-ARR basis; (d) the magic number on the ARR basis; (e) the magic number on the revenue basis.
Then compare (b) and (c) with the FY2025 figures in Exhibit 1-9 and explain in three sentences why the two bases
move in opposite directions.

### Exercise 1-5 — Rule of 40 under three profitability measures [Intermediate]

For FY2024: revenue $118,900; FY2023 revenue $91,500; loss from operations $(22,030); stock-based compensation
$22,900; restructuring nil; amortization of acquired intangible assets $900; net cash provided by operating
activities $28,900. Compute the Rule of 40 score using (a) GAAP operating margin, (b) a non-GAAP operating
margin that adds back stock-based compensation, restructuring, and acquired intangible amortization, and (c)
operating cash flow margin. Compare each with the FY2025 result in Exhibit 1-9 and state which single item
explains most of the spread between measures.

### Exercise 1-6 — Corroborating a bookings figure through the commission asset [Advanced]

Management tells you FY2024 new and expansion ACV bookings were "roughly $79 million" but cannot produce a
supporting extract. You have the following FY2024 facts, all in thousands: deferred contract acquisition costs
of $14,900 at January 1, 2024 and $19,500 at December 31, 2024; amortization charged to sales and marketing of
$6,400; write-offs of costs relating to churned customers of $180; renewed ACV of $61,200; new-business
commission rate 11.8% of ACV; renewal commission rate 3.1% of ACV; capitalized sales manager overrides of $480;
employer payroll taxes of 7.65% applied to capitalized commissions and overrides; and amounts expensed under
the one-year practical expedient of $1,465.

Compute (a) the required FY2024 additions to deferred contract acquisition costs and (b) the implied new and
expansion ACV bookings. State whether management's "roughly $79 million" is corroborated, and state what you
would do if your computed figure had come out at $94,000 instead.

### Exercise 1-7 — Continuance with a changed fact [Judgment, Intermediate]

Change one fact in the Exhibit 1-1 continuance evaluation. Assume that when Brightline inquired about the
founding CFO's July 2025 resignation, the audit committee chair disclosed that the CFO had resigned after
disagreeing with Elena Vasquez over whether $1,100 of contracts signed in the last week of December 2024 should
have been recognized in FY2024, that the CFO's position was that they should not, that management recognized
them, and that the audit committee did not investigate because the amount was below the FY2024 materiality of
$1,190.

Write a conclusion of 200 to 300 words on whether Brightline should continue, and if so with what conditions.
Address the FY2024 audit implications as well as FY2025.

### Exercise 1-8 — Independence when the firm builds on the client's platform [Judgment, Advanced]

Brightline's national audit innovation group has built a confirmation-tracking workflow for all of the firm's
engagements on top of AtlasFlow Core, using 40 automation seats and approximately 1.2 million workflow runs per
year. The build was performed by Brightline staff using AtlasFlow's published configuration tooling; AtlasFlow
personnel provided two hours of standard onboarding support. Annual subscription cost is $310 at list less the
standard 12% volume discount.

Analyze the independence consequences under Regulation S-X Rule 2-01 and state your conclusion. Identify at
least three specific facts that would change your answer, and state what the engagement team should do in the
next thirty days.

### Exercise 1-9 — Interim date selection with a late system change [Judgment, Advanced]

Assume the NetSuite upgrade, including the rebuild of segregation-of-duties roles, is scheduled for November 14,
2025 rather than September 2025, and management will not move it. All other facts are unchanged: a February 20,
2026 target report date, a March 2, 2026 statutory deadline, a 5,340-hour budget, and the quarterly access
review and monthly reconciliation control frequencies.

Recommend an interim date or dates, specify what is tested at each, specify the roll-forward procedures, and
state the incremental hours you would add and to which workstream. Then state the one condition under which you
would recommend testing no controls at interim at all.

### Exercise 1-10 — Draft the group audit instruction paragraphs [Drafting, Intermediate]

Draft the "component-specific risks" section of Brightline LLP's group audit instructions to Brightline UK LLP,
dated October 24, 2025. It must be 180 to 240 words, must state component materiality and component performance
materiality, must address the C-2 Voltaire Logistics renewal (signed October 1, 2025, 24 months, total fixed fee
$1,600, contracted in EUR at €1,480 through the UK entity, including a $200 renewal credit usable only toward a
future Insight purchase), must address the risk that became corrected misstatement C-4 (understatement of
accrued VAT, $180), must state the reporting deadline, and must specify the deliverable.

### Exercise 1-11 — Draft the audit committee paragraph on a possible adverse ICFR opinion [Drafting, Advanced]

Draft the paragraph Brightline delivered to the AtlasFlow audit committee on September 30, 2025 addressing the
realistic possibility of an adverse opinion on internal control over financial reporting. It must be 170 to 220
words, must be conditional rather than conclusory, must reference specific evidence, must identify at least
three of the 14 identified gaps by substance, must state what would change the outcome, and must not use the
phrase "we have concluded."

### Exercise 1-12 — Find the errors in a scoping memo extract [Advanced; spans Chapter 1 and Chapter 3]

The following extract is from a draft FY2025 scoping memo prepared by a first-year staff auditor. Identify every
error, state why each is wrong, and give the correction. There are six.

```text
WP 1240-01 (DRAFT) — SCOPE OF THE INTEGRATED AUDIT

1. Financial statement materiality is $1,450. For purposes of the audit of internal
   control over financial reporting we have applied an ICFR materiality of $725,
   being 50% of financial statement materiality, in order to identify a larger
   population of significant accounts.

2. Contingent consideration of $2,500 is 1.7 times materiality and is therefore not
   a significant account.

3. Because management has excluded Kestrel Labs, Inc. from its Section 404(a)
   assessment, the $14,500 of goodwill and $8,000 of acquired intangible assets
   arising in that acquisition are outside the scope of our audit.

4. Coverage: accounts scoped as significant represent 91.6% of consolidated revenue
   ($109,400 + $26,300 = $135,700 divided by $148,200).

5. Total assets scoped as significant are $305,900, or 95.2% of consolidated total
   assets of $317,900.

6. Segment disclosure: not applicable.
```

### Exercise 1-13 — Strategy or plan? [Foundational]

For each of the following ten decisions, state whether it belongs in the audit strategy memo (WP 1100-02) or in
the audit plan (WP 1200 series), and give a one-clause reason.

1. Interim controls testing will be performed as of October 31, 2025.
2. Twenty-five order forms will be selected for the CPQ discount approval attribute test.
3. Dr. Igor Petrov will be engaged as a valuation specialist for the Kestrel contingent consideration.
4. Accounts receivable confirmations will be sent to the ten largest enterprise balances plus a monetary-unit
   sample of the remainder.
5. Overall materiality is preliminarily $1,450, subject to revision if FY2025 revenue falls outside $141,000 to
   $155,000.
6. Deferred revenue completeness is a significant risk.
7. The substantive analytical procedure over Core subscription revenue will be disaggregated monthly by customer
   segment with an investigation threshold of $470.
8. Australia will receive specified procedures with component materiality of $420.
9. Brightline will not use internal audit's work over any control relating to revenue.
10. The RPO recomputation will be performed by Tara Iyer using the Zuora Revenue contract extract as of
    December 31, 2025, with 100% population coverage.

## Solutions to Practice Exercises

### Solution 1-1

(a) Retained ARR from the opening base = opening ARR × GRR = $106,000 × 0.93 = **$98,580**. Cross-check:
$106,000 − $3,420 contraction − $4,000 churn = $98,580. The two routes agree, which confirms that contraction
and churn are the only components excluded from gross retention.

(b) Expansion ARR. NRR × opening ARR = 1.18 × $106,000 = $125,080. Expansion = $125,080 − $98,580 =
**$26,500**.

(c) New customer ARR = closing ARR − retained − expansion = $137,400 − $98,580 − $26,500 = **$12,320**.

(d) Net new ARR = $137,400 − $106,000 = **$31,400**. Cross-check: $12,320 + $26,500 − $3,420 − $4,000 = $31,400.

Reconciliation: $106,000 − $3,420 − $4,000 + $26,500 + $12,320 = $137,400. The waterfall foots.

The comparison worth drawing: in FY2024 new customer ARR of $12,320 was 39.2% of expansion ARR of $26,500; in
FY2025 (Exhibit 1-7) new customer ARR of $18,100 was 62.6% of expansion ARR of $28,900. Growth is shifting from
the installed base to new logos while the new logos are smaller. That is the composition change the cohort table
in Exhibit 1-10 makes visible.

### Solution 1-2

(a) TCV = subscription $2,400 + Insight ($180 × 2 years) $360 + implementation $360 = **$3,120**.

(b) Year-1 ACV, subscription only = **$600**.

(c) Average-of-term ACV, subscription only = $2,400 ÷ 3 = **$800**.

(d) Average-of-term ACV including Insight = ($2,400 + $360) ÷ 3 = $2,760 ÷ 3 = **$920**.

(e) Exit run-rate ACV including Insight = year-3 subscription $960 + Insight $180 = **$1,140**.

(f) Overage = (244,000 − 200,000) ÷ 1,000 × $12 = 44 × $12 = **$528 in whole dollars**, or $0.5 thousand.

Ratio of highest to lowest ACV measure = $1,140 ÷ $600 = **1.90**, a 90% spread on the same contract.

Why the spread matters: the commission is paid on "booked ACV" and capitalized under ASC 340-40, so which ACV
definition the commission plan uses changes the capitalized amount on this contract by up to $64 at an 11.8%
rate ($1,140 × 11.8% = $135 versus $600 × 11.8% = $71). More importantly, an ACV metric reported to investors is
not comparable across companies or, if the definition is not fixed in a system, across quarters within one
company. Ask which definition the Salesforce CPQ ACV field implements, and test that it implements it
consistently. Note also that the $528 overage is far below the clearly trivial threshold of $72 thousand for this
single contract — but the aggregate usage overage stream is $4,200, and completeness of the underlying
workflow-run data is a distinct risk developed in Chapter 5.

### Solution 1-3

(a) Write-offs = opening allowance + provision − closing allowance = $1,010 + $1,240 − $1,350 = **$900**.

(b) Cash collected = opening gross AR + billings − write-offs − closing gross AR
= $24,300 + $131,600 − $900 − $30,500 = **$124,500**.

(c) FY2024 collections as a percentage of billings = $124,500 ÷ $131,600 = **94.60%**. FY2025 = $154,480 ÷
$163,750 = **94.34%**. The ratio deteriorated by only **0.26 percentage points**.

What it tells you, and this is the point of the exercise: almost nothing. The annual collection ratio moved a
quarter of a point while Q4 DSO moved seven days, from 61 to 68. An annual, undisaggregated ratio is too
imprecise to detect a deterioration concentrated in the fourth quarter, because eleven months of normal
collection swamp one month of abnormal billing. The lesson generalizes to every analytical procedure: precision
comes from disaggregation, and an analytic performed at the annual level will pass while the same analytic
performed monthly fails. Chapter 18's case study is exactly this failure, concealing a $780 cut-off
misstatement.

### Solution 1-4

(a) FY2024 subscription gross margin = ($108,300 − $23,140) ÷ $108,300 = $85,160 ÷ $108,300 = **78.6%**.

(b) CAC payback, gross-ARR basis. Gross profit contribution from new and expansion ARR = $38,820 × 0.786 =
$30,512. Payback in years = $50,900 ÷ $30,512 = 1.668. In months = 1.668 × 12 = **20.0 months**.

(c) CAC payback, net-ARR basis. Contribution = $31,400 × 0.786 = $24,680. Payback = $50,900 ÷ $24,680 = 2.062
years = **24.7 months**.

(d) Magic number, ARR basis = net new ARR ÷ prior-year S&M = $31,400 ÷ $41,200 = **0.76**.

(e) Magic number, revenue basis = ($118,900 − $91,500) ÷ $41,200 = $27,400 ÷ $41,200 = **0.67**.

Comparison with FY2025: gross-basis CAC payback improved from 20.0 to 19.6 months; net-basis CAC payback
worsened from 24.7 to 26.6 months. The two bases move in opposite directions because the gross basis measures
only how efficiently sales and marketing spend produces *new* annual recurring revenue, and that efficiency
held; the net basis is the gross basis less churn and contraction, and churn plus contraction rose from $7,420
in FY2024 to $12,400 in FY2025 while the base grew only 29.6%. The divergence between the two measures is
therefore a direct read on retention deterioration, and it is the same deterioration that shows up as gross
retention falling from 93% to 91%. For the auditor, the net-basis figure is the one that bears on the four-year
commission amortization period, because the four years must be earned by customers who stay.

### Solution 1-5

Revenue growth for FY2024 = $118,900 ÷ $91,500 − 1 = **29.9%**.

(a) GAAP operating margin = $(22,030) ÷ $118,900 = (18.5)%. Rule of 40 = 29.9% − 18.5% = **11.4%**.

(b) Non-GAAP operating income = $(22,030) + $22,900 + $0 + $900 = $1,770. Margin = $1,770 ÷ $118,900 = 1.5%.
Rule of 40 = 29.9% + 1.5% = **31.4%**.

(c) Operating cash flow margin = $28,900 ÷ $118,900 = 24.3%. Rule of 40 = 29.9% + 24.3% = **54.2%**.

FY2025 comparatives from Exhibit 1-9 are 8.2%, 29.9%, and 47.8%. All three measures declined, by 3.2, 1.5, and
6.4 points respectively, and the direction is consistent across measures — which matters, because when different
profitability measures move in opposite directions the cause is usually a classification change rather than an
operating change.

The single item explaining most of the spread is **stock-based compensation**: $22,900 in FY2024, which is 19.3%
of revenue, and $28,700 in FY2025, 19.4% of revenue. It alone accounts for 19.3 of the 20.0-point FY2024 gap
between measures (a) and (b). The spread between (b) and (c) is explained by depreciation and amortization plus
the amortization of deferred contract acquisition costs, both of which are non-cash and both of which arise from
capitalization policies that are themselves audit risks.

### Solution 1-6

(a) Required additions. Rearrange the roll-forward: closing = opening + additions − amortization − write-offs.
Additions = $19,500 − $14,900 + $6,400 + $180 = **$11,180**.

(b) Implied bookings. Build the additions from the bottom up, letting B be new and expansion ACV:

- Renewal commissions = 3.1% × $61,200 = $1,897.2
- Overrides = $480
- Commission and override subtotal before payroll taxes = 0.118B + $1,897.2 + $480 = 0.118B + $2,377.2
- Add employer payroll taxes at 7.65%: multiply the subtotal by 1.0765
- Deduct amounts expensed under the practical expedient: $1,465

So 1.0765 × (0.118B + $2,377.2) − $1,465 = $11,180.

1.0765 × (0.118B + $2,377.2) = $12,645.0
0.118B + $2,377.2 = $12,645.0 ÷ 1.0765 = $11,746.4
0.118B = $9,369.2
B = $9,369.2 ÷ 0.118 = **$79,400**

Management's "roughly $79 million" is corroborated to within $400, or 0.5%, by a computation that anchors on
two audited balance sheet amounts and the client's own documented commission rates. That is a usable planning
conclusion.

If the computation had produced $94,000 against management's assertion of $79,000, the $15,000 gap — 19% of the
asserted figure — would have to be explained before either number could be used. The three candidate
explanations, in the order you would test them, are: (i) the effective commission rate is below the 11.8% stated
policy because of quota underperformance, in which case the policy rate is not the right input and you obtain the
actual commission expense from the payroll and commission records; (ii) more cost is being capitalized than
policy permits, for example base salary or sales-engineer time, which is a misstatement of the $24,000 asset and
sends you directly to the Chapter 10 capitalization test; or (iii) the bookings figure management gave you is
wrong. The point of the technique is that it converts an unauditable operating metric into a testable
proposition about an audited balance.

### Solution 1-7

**Conclusion: continue, but only with a defined set of conditions, and treat the disclosure as a matter
requiring immediate procedures rather than as a continuance input to be weighed.**

The disclosed facts change the character of the decision because they are about *integrity and governance*, not
about capacity. A CFO resigning after a disagreement over the period in which $1,100 of last-week-of-December
contracts should be recognized is, on its face, an allegation of an accounting disagreement resolved in favor of
the aggressive answer. The audit committee's stated reason for not investigating — that $1,100 was below the
FY2024 materiality of $1,190 — is itself the more serious problem. Quantitative immateriality does not dispose
of a matter that bears on the integrity of management or on the reliability of the signature-date controls, and
an audit committee that applies a materiality screen to an allegation of improper period-end recognition has
misunderstood its role. Under any framework, qualitative factors can make a quantitatively small misstatement
material, and a deliberate cut-off error is the paradigm case.

Conditions for continuance: (1) Brightline evaluates whether the FY2024 audit was deficient, whether the FY2024
opinion can still be associated with the financial statements, and whether the matter requires consultation with
the national office and the firm's general counsel — the December 2024 population is the same population and the
same control that FY2025's Q4 concentration implicates. (2) The audit committee engages independent counsel or
directs internal audit to investigate the December 2024 contracts, and Brightline receives the results.
(3) Brightline assesses a fraud risk relating to revenue cut-off in FY2025 at the outset rather than at
year end, and designs the December response accordingly. (4) The engagement letter and the September audit
committee communication record the matter explicitly.

The alternative and also defensible conclusion is to resign. It is the right answer if the audit committee
declines to investigate, because at that point the auditor is relying on a governance body that has demonstrated
it will not act on evidence of improper recognition, and no amount of substantive testing compensates for that.
The weaker answer is to continue and simply "increase skepticism," which is not a procedure.

### Solution 1-8

**Conclusion: this is materially different from the ordinary-course subscription in Exhibit 1-2 item 1, and it
requires escalation and almost certainly remediation.**

The relevant analysis under Rule 2-01 is not the purchase itself — a subscription at list less a standard
discount remains an ordinary-course consumer transaction. It is the *dependency and entanglement* the build
creates. Three specific concerns:

1. **Self-interest and self-review through operational dependence.** Every Brightline engagement's confirmation
   process now depends on the continued availability, performance, and pricing of an audit client's platform. If
   AtlasFlow suffers an outage, Brightline's audits are disrupted. That creates a firm-level interest in the
   client's operational and commercial success that a reasonable investor would question, and it is exactly the
   kind of mutual dependence the business relationship provisions address.
2. **The service-availability and SLA question becomes self-interested.** AtlasFlow's contracts include uptime
   SLAs with graduated service credits (see C-3 Northgate). Brightline would be a customer with an SLA claim
   against its audit client, negotiating credits with client personnel, while auditing the completeness of the
   SLA credit accrual — the very balance at issue in corrected misstatement C-2 ($290).
3. **Usage scale changes the character of the relationship.** Approximately 1.2 million workflow runs per year
   makes Brightline a substantial usage customer, potentially a reference account, and a source of overage
   revenue in account 4120. It is no longer a back-office subscription.

Three facts that would change the answer: (i) whether AtlasFlow personnel performed any of the configuration
work, which would convert this into a joint development arrangement; (ii) whether Brightline's contract contains
non-standard terms, custom pricing, a co-marketing clause, or a reference-customer commitment; and (iii)
whether Brightline's usage is material to AtlasFlow — 1.2 million runs is not, against a $4,200 overage revenue
stream and 3,140 customers, but a firm-wide rollout might become so.

Actions in the next thirty days: notify the firm's independence group and the engagement partner in writing;
obtain the contract and the build documentation; determine whether the workflow can be migrated to a
non-client platform before the FY2025 report date; and if it cannot be migrated, obtain a firm-level
independence conclusion and communicate the facts and the conclusion to the audit committee as part of the
annual independence communication. Do not resolve this at the engagement team level.

### Solution 1-9

**Recommendation: two interim dates — August 31, 2025 and November 30, 2025 — with the population split by
whether the control depends on the NetSuite configuration.**

The single-date approach fails in both directions. An October 31 date now precedes the upgrade, so every
NetSuite access and segregation-of-duties control tested would be tested on a configuration that ceases to exist
on November 14. A single November 30 date leaves only 31 days of roll-forward, which is comfortable, but it
compresses all control testing into the four weeks before the December close, when the client's one-person-deep
accounting function is least able to produce evidence, and it leaves no time to expand testing if deviations
appear.

The split:

- **August 31, 2025 interim date** for controls that do not depend on the NetSuite configuration: the Salesforce
  CPQ discount approval matrix, the Zuora Billing-to-Revenue interface reconciliation (I-2), the Stripe daily
  cash-to-revenue reconciliation (I-4), the RevPro-to-GL reconciliation, the Coupa three-way match, and the
  FloQast close checklist sign-offs. Roll-forward for these covers September 1 to December 31 — four months —
  and therefore requires re-testing rather than inquiry: two additional instances of each monthly control and
  eight additional order forms for the CPQ test.
- **November 30, 2025 interim date** for everything NetSuite-dependent: user access provisioning and
  de-provisioning, the segregation-of-duties role configuration, the journal entry approval threshold
  configuration, and the automated three-way match posting. Roll-forward covers 31 days and is satisfied by
  inspecting the December configuration change log and testing the December termination population 100%.
- **Program development and implementation controls over the upgrade itself** become a separate scoped area
  tested in December: project approval, user acceptance testing, data conversion validation, and post-implementation
  access review. This is not a roll-forward matter; it is a new control objective created by the event.

Incremental hours: **220 to the IT audit workstream** (140 for the upgrade's program development and
implementation controls, 80 for the second interim visit's setup and population validation) and **60 to
process-level control testing** for the extra instances required by the four-month roll-forward on the
August-tested controls. Total budget moves from 5,340 to 5,620 hours.

The one condition under which I would test no controls at interim: if management cannot represent that the
segregation-of-duties role design has been finalized before the upgrade, so that the post-upgrade configuration
is itself expected to change during December. Testing a configuration that is still being built produces no
evidence about the as-of date. In that case all control testing moves to January, the substantive strategy is
designed without reliance on automated controls, and the audit committee is told in September that the
compressed timetable makes an unqualified ICFR opinion unlikely.

### Solution 1-10

```text
BRIGHTLINE LLP — GROUP AUDIT INSTRUCTIONS                          WP 1260-02
To:      Brightline UK LLP, London (Component Auditor)
From:    D. Whitcombe, Group Engagement Partner
Date:    October 24, 2025
Re:      AtlasFlow Software Ltd — component-specific risks, FY2025

Section 4 — Component-specific risks you must address

Component materiality is $580 thousand and component performance materiality is
$380 thousand. Use these amounts for all scoping, sample size, and evaluation
decisions; accumulate and report to us every misstatement above $72 thousand,
which is the group clearly trivial threshold, whether or not you propose it as an
adjustment.

Two component-specific risks require designed procedures and a written
conclusion.

(a) Contract C-2, Voltaire Logistics S.A., renewal signed October 1, 2025 for a
    24-month term, total fixed fee $1,600 thousand, contracted in EUR (EUR 1,480
    thousand) through AtlasFlow Software Ltd, whose functional currency is GBP.
    Determine and test (i) the identification and measurement of the $200
    thousand renewal credit usable only toward a future Insight purchase, which
    management has concluded is a material right and a separate performance
    obligation; (ii) the allocation of the transaction price to that material
    right; and (iii) the EUR-to-GBP and GBP-to-USD translation of both the
    revenue and the contract liability, including the rate used and its source.

(b) Accrued value added tax within the UK component's accrued liabilities.
    Perform a completeness-directed procedure over VAT on EMEA subscription and
    professional services billings for the four quarters of FY2025, reconciling
    the Avalara determination output to the amounts accrued and to the returns
    filed. We have identified a heightened risk of understatement.

Deliverables: a component auditor's report in our prescribed format, a
memorandum on each of risks (a) and (b) stating the procedures performed and the
conclusion reached, a summary of uncorrected and corrected misstatements, a
schedule of identified control deficiencies, and your completed group reporting
questionnaire. All deliverables are due to the group engagement team by
January 23, 2026. We will review your workpapers for risks (a) and (b) remotely
during the week of January 26, 2026.
```

The word count of Section 4 as drafted is 231 words, within the 180-to-240 requirement. Note three drafting
choices. The instructions state both component materiality *and* the group clearly trivial threshold, because a
component auditor who accumulates only to component performance materiality will not report the $180
misstatement that became corrected misstatement C-4. They name the contract and the amount rather than
describing a category, because "consider material rights" produces a paragraph and naming C-2 produces a test.
And they specify a workpaper review, because the amended AS 2101 requirements make the group engagement team
responsible for the involvement in and supervision of the other auditor's work.

### Solution 1-11

```text
Item 6 — Internal control over financial reporting: the range of possible outcomes

Fiscal 2025 is the first year in which we will express an opinion on the
effectiveness of AtlasFlow's internal control over financial reporting. We want
the Committee to understand, now rather than in February, what the evidence
currently available suggests about the range of possible outcomes.

Internal audit's July readiness assessment identified fourteen control gaps. On
the facts known to us today, three are of a character that, if unremediated at
December 31, would in our view be difficult to distinguish from a material
weakness: administrator access to the Zuora Revenue configuration through four
accounts that are not federated to Okta, one of them a shared credential
available to six people; the performance of user access reviews annually rather
than at the quarterly frequency management's own control documentation
describes, with one 2025 review completed forty-one days late; and a journal
entry approval configuration that requires a second approver only above
$250,000, with the result that approximately 78% of manual entries posted in
2025 carry no evidence of independent review.

We have performed no operating-effectiveness testing to date and we have reached
no conclusion. What would change the outcome is remediation that is designed,
implemented, and operating for a sufficient period before December 31 —
practically, before the end of October — together with evidence we can test. We
will report the status of each of the fourteen gaps at the November meeting.
```

The draft is 214 words. The design choices worth naming: it states the absence of a conclusion twice, once at
the top and once at the bottom; it uses "difficult to distinguish from a material weakness" rather than "is a
material weakness"; it quantifies (fourteen, four, six, forty-one days, $250,000, 78%) so the committee can hold
management to specifics; it gives an actionable deadline (end of October, derived from the need for a sufficient
period of operation before the as-of date); and it commits to a follow-up. The 78% figure is 3,847 ÷ 4,912 =
78.3%, from W-12.

### Solution 1-12

**Error 1 — paragraph 1, the invented "ICFR materiality" of $725.** AS 2201 requires the auditor to use the same
materiality for the audit of internal control over financial reporting as for the audit of the financial
statements. There is no lower ICFR materiality, and the stated purpose — "in order to identify a larger
population of significant accounts" — describes a firm's optional conservatism as a requirement. Correction: use
$1,450. If the team wants a lower screen for identifying accounts, that is performance materiality of $940 used
as a scoping aid, and it must be labeled as such. Chapter 3, §3.10 develops materiality in the ICFR audit.

**Error 2 — paragraph 2, significance determined by magnitude alone.** An account is significant if there is a
reasonable possibility that it could contain a misstatement that would be material. Contingent consideration of
$2,500 is measured by Monte Carlo simulation with unobservable inputs — 32% revenue volatility, an 11.5%
risk-adjusted discount rate, and a $4,000 maximum payout — so a reasonably possible misstatement is a large
fraction of the carrying amount and exceeds materiality. Correction: contingent consideration is a significant
account. The general error is treating the magnitude screen as the test.

**Error 3 — paragraph 3, conflating the ICFR scope exclusion with the audit scope.** Management's exclusion of a
recently acquired business from its Section 404(a) assessment, in reliance on the SEC staff's position, affects
only the ICFR assessment and opinion. The $14,500 of goodwill, $8,000 of acquired intangibles, $2,500 of
contingent consideration, and $1,300 deferred tax liability are all audited financial statement balances.
Correction: delete the sentence and replace it with the boundary of the exclusion and a statement that the
financial statement audit covers the acquisition in full.

**Error 4 — paragraph 4, coverage computed on the wrong basis.** The paragraph computes *component* coverage
(US plus UK revenue) and labels it *account* coverage. It also omits Australia's $12,500, which is within the
scope of the audit through specified procedures, and India, which has no external revenue. Correction: account
coverage of revenue is 100.0%, because all five revenue streams and all three revenue-generating entities are
scoped as significant. If the memo also wants to disclose component coverage, present it separately and
correctly: full-scope components represent 91.6% of consolidated revenue, with the remaining 8.4% addressed by
specified procedures.

**Error 5 — paragraph 5, arithmetic.** $305,900 ÷ $317,900 = 96.2%, not 95.2%. Every percentage in a scoping
memo should be recomputed by the reviewer; this one is off by a full point and the error is the kind that
survives four review levels because it looks plausible.

**Error 6 — paragraph 6, "not applicable" is not a conclusion.** AtlasFlow has one reportable segment, and the
memo must say so and record the basis: the chief operating decision maker reviews discrete financial information
at the consolidated level only. The conclusion then supports the decision not to scope the segment disclosure
for testing. "Not applicable" documents nothing and leaves an experienced auditor unable to understand what was
considered, which is the AS 1215 standard.

### Solution 1-13

| # | Document | Reason |
| --- | --- | --- |
| 1 | Strategy | Timing of the audit is an explicit strategy element and is communicated to the audit committee. |
| 2 | Plan | A sample size is the extent of a specific procedure at the assertion level. |
| 3 | Strategy | Resource allocation and the use of specialists is a strategy element; the specialist's written scope then lives in the plan and the working papers. |
| 4 | Plan | Selection methodology and extent for a specific test of details. |
| 5 | Strategy | Preliminary materiality, including the revision trigger, is a strategy element. |
| 6 | Strategy | Significant risks identified at planning are a required strategy element and a required audit committee communication; the *response* to the risk is in the plan. |
| 7 | Plan | Disaggregation level and investigation threshold are the design of a specific substantive analytical procedure. |
| 8 | Strategy | Scope of work at components and component materiality are strategy elements. |
| 9 | Strategy | The decision whether and where to use internal audit's work is a strategy element about the direction and resources of the audit. |
| 10 | Plan | The assignment of a named individual to a specific procedure over a specific population is plan-level detail. |

The recurring test: if the item answers "what kind of audit is this and what does it need," it is strategy. If it
answers "what exactly will be done to which population," it is plan. Items 6 and 9 are the ones most often
misfiled, in both directions.

## Review Questions

**RQ 1-1.** What distinguishes an engagement continuance decision from an acceptance decision, and why does the
distinction raise rather than lower the documentation standard?

**RQ 1-2.** AtlasFlow's public float at June 30, 2025 was $983.6 million. Name the three consequences of that
measurement for the FY2025 audit.

**RQ 1-3.** Why is a lead partner's fourth consecutive year on an engagement a planning matter rather than
purely an independence-monitoring matter?

**RQ 1-4.** AS 1301 requires the auditor to establish an understanding of the terms of the engagement with the
audit committee. What does "establish" add to "record in writing"?

**RQ 1-5.** State two items that belong in the audit strategy and two that belong in the audit plan, and give
the test that separates them.

**RQ 1-6.** Which of ARR, billings, revenue, and RPO appear inside the audited financial statements, and why
does the answer determine the evidence standard you apply?

**RQ 1-7.** Explain why a December 30 signature with a January 1 start date creates a larger exposure in the
commission accounts than in the revenue accounts.

**RQ 1-8.** Net revenue retention fell six points and gross retention fell two. What does the four-point
difference tell you, and which accounts does each of the two causes pressure?

**RQ 1-9.** Why can the Rule of 40 produce scores of 8.2%, 29.9%, and 47.8% for the same company in the same
year, and which item accounts for most of the spread at AtlasFlow?

**RQ 1-10.** What does a cohort table reveal that ARR growth, NRR, and GRR do not?

**RQ 1-11.** AtlasFlow's prepaid expenses of $8,100 are 5.6 times overall materiality but are not scoped as a
significant account. On what basis can that conclusion be supported?

**RQ 1-12.** What materiality does the auditor use in the audit of internal control over financial reporting,
and what is the most common error on this point?

**RQ 1-13.** Under the amended AS 2101 group audit requirements and the revised AU-C 600, what replaced the
practice of classifying components as significant or insignificant?

**RQ 1-14.** Give four reasons Brightline selected October 31, 2025 as the interim controls testing date, and
state which of the four would have been violated by an August 31 date.

**RQ 1-15.** When a control tested at interim was found not to operate as designed, what is the roll-forward
procedure for the remaining period?

**RQ 1-16.** Distinguish an auditor-engaged specialist, a company-engaged specialist, and an engagement team
member with specialized skill, and name the standard governing each on a PCAOB engagement.

**RQ 1-17.** What is the most important substantive difference between AS 2605 and AU-C 610 in how internal
audit may be used?

**RQ 1-18.** Why should the possibility of an adverse ICFR opinion be raised with the audit committee in
September rather than in February, and how can it be raised without concluding prematurely?

## Answers to Review Questions

**RQ 1-1.** Continuance is made with the benefit of the prior year's file, so the firm knows what went wrong,
which management representations proved unreliable, and where the client was late. It cannot claim surprise at
conditions it observed. The documentation standard rises because the memo must explain what changes in the audit
as a result of each identified condition, not merely that the condition was considered. Brightline's FY2025 memo
attached four specific conditions, each of which generated a later workpaper.

**RQ 1-2.** First, AtlasFlow becomes a large accelerated filer, so the Form 10-K deadline compresses from 75 days
to 60, making March 2, 2026 the statutory date. Second, combined with the completion of its fifth fiscal year
after the April 2022 IPO registration statement, the float above $700 million causes AtlasFlow to cease
qualifying as an emerging growth company effective December 31, 2025. Third, the loss of EGC status removes the
exemption from Section 404(b), so FY2025 is the first year Brightline must express an opinion on the
effectiveness of internal control over financial reporting under AS 2201.

**RQ 1-3.** Because the rotation clock determines when a new lead partner will inherit the engagement, and the
inheritance is a resource and continuity decision. Dana Whitcombe's fifth and final year is FY2026, so a new
lead partner arrives for FY2027 — potentially the year after an adverse ICFR opinion and a remediation cycle.
Planning for that transition, including an overlap year for the successor, is a planning matter. The independence
monitoring is only the compliance half of it.

**RQ 1-4.** "Record in writing" is satisfied by an engagement letter. "Establish with the audit committee" is
satisfied only if the committee, not management, agreed to the terms. The two are separable in practice: a
letter negotiated with the CFO and shown to the committee for information records an understanding without
establishing one. The substantive difference is which body hears the terms it would not otherwise be told, such
as the auditor's dependency on management's completed Section 404(a) assessment.

**RQ 1-5.** Strategy: the interim testing date, and component materiality of $420 for Australia. Plan: the sample
size for the CPQ discount approval attribute test, and the investigation threshold for the monthly Core revenue
analytic. The test: strategy answers "what kind of audit is this and what resources does it require"; the plan
answers "what exactly will be done, to which population, by whom, when."

**RQ 1-6.** Revenue and RPO appear inside the audited financial statements — revenue as a caption, RPO as a
required ASC 606 disclosure. Billings is a derived figure that is not a caption but is reconcilable to audited
balances. ARR appears only in MD&A. Inside-the-statements figures are audited to a disclosure or account
standard and are recomputable from defined populations; outside-the-statements figures are read for material
inconsistency as other information under AS 2710 or AU-C 720. Applying the wrong standard either wastes hours or
leaves a required disclosure untested.

**RQ 1-7.** A January 1 start date means no FY2025 revenue is recognized at all, but the commission is earned and
paid on the December signature, the quota credit and Q4 bookings headline are recorded, and the commission is
capitalized under ASC 340-40. At AtlasFlow, $51,700 of FY2025-signed ACV produced no FY2025 revenue and full
FY2025 commission cost. The exposure therefore sits in accrued commissions of $4,800, deferred contract
acquisition costs of $24,000, and the control environment, and the small revenue effect understates the severity
of the control failure a fabricated date evidences.

**RQ 1-8.** Gross retention excludes expansion, so its two-point decline is attributable to churn and
contraction. Net retention includes expansion, so the additional four points are attributable to the surviving
base expanding less. Deteriorating gross retention pressures the allowance for credit losses, the impairment of
capitalized commissions on non-renewed customers, and the four-year amortization period supported by a 4.3-year
average customer life. Deteriorating expansion pressures the metric itself, and therefore the ARR-based PSU
probability assessment and the incentive to accelerate expansion signatures.

**RQ 1-9.** Because the "40" combines a growth rate with a profitability margin, and the profitability margin is
undefined. GAAP operating margin, a non-GAAP operating margin, and operating cash flow margin differ at
AtlasFlow by 39.6 points. Stock-based compensation of $28,700, or 19.4% of revenue, accounts for most of the
spread; depreciation and amortization of $11,900 and amortization of deferred contract acquisition costs of
$8,600 account for much of the remainder.

**RQ 1-10.** Whether the newest business is as good as the business it replaced. Aggregate NRR and GRR are
weighted averages dominated by the large, old, well-retained cohorts, so a deterioration in recent vintages is
concealed. AtlasFlow's 2024 cohort reached 108.9% of landing ARR in two years where the 2022 cohort was around
112% at the same age, and the 2025 cohort's average landed ARR of $28.2 per logo is roughly half the portfolio
average of $52.6.

**RQ 1-11.** On the basis that there is no reasonable possibility of a material misstatement, not on the basis of
size. Prepaid expenses consist of $4,900 of prepaid software and hosting amortized on straight-line schedules
fixed at invoice date and $1,400 of prepaid insurance, with no estimate, no allocation judgment, and no
incentive. The conclusion would fail if the balance contained an amount whose amortization depended on a
delivery or performance estimate.

**RQ 1-12.** The same materiality used in the financial statement audit — $1,450 for AtlasFlow. The common error
is inventing a lower "ICFR materiality," often 50% of financial statement materiality, and presenting it as a
requirement. A lower figure may be used as a firm scoping aid, but it must be labeled as such, and performance
materiality of $940 already serves that function.

**RQ 1-13.** A risk-based determination of the scope of work at each component. Both frameworks now require the
auditor to identify the risks of material misstatement of the group financial statements arising at or from each
component and to determine the work that addresses them, rather than classifying components and applying a
standard scope to each class. AS 1206 separately governs the distinct decision to divide responsibility and
refer to another firm in the report.

**RQ 1-14.** The 61-day remaining period is short enough for a proportionate roll-forward; October captures a
full set of instances for both quarterly and monthly controls; the date follows the September NetSuite upgrade
and therefore tests the configuration that will exist at year end; and loading evidence requests into November
leaves the December close clear. An August 31 date violates the third reason outright, because the
segregation-of-duties roles were rebuilt in September, and would require the entire access-control population to
be retested.

**RQ 1-15.** There is none. A control that did not operate as designed at interim has nothing to roll forward;
the deficiency is evaluated for severity and the audit is designed without reliance on it. Testing the same
control again at year end does not repair the interim result, though it may be relevant to a remediation
assessment. AtlasFlow's annual-rather-than-quarterly user access reviews (W-3) are the example.

**RQ 1-16.** An auditor-engaged specialist is engaged by the audit firm and is governed by AS 1210, which requires
the auditor to evaluate the specialist's knowledge, skill, and objectivity and to inform the specialist of the
work required. A company-engaged specialist is engaged by the client, and the auditor evaluates the resulting
evidence under AS 1105 Appendix A. An engagement team member with specialized skill — an IT auditor or a data
analytics specialist — is audit staff, supervised under AS 1201, and is not a specialist for these purposes.

**RQ 1-17.** AU-C 610 permits internal auditors to provide direct assistance to the external auditor under the
external auditor's direction, supervision, and review, subject to conditions. PCAOB standards do not contemplate
staffing an audit with client employees in that way; AS 2605 addresses using internal audit's *work product* as
evidence after assessing competence and objectivity. A reader auditing a private SaaS company therefore has a
resourcing option that is unavailable on the AtlasFlow engagement.

**RQ 1-18.** Because the audit committee's leverage over management's remediation expires at December 31, and
five months of warning is the difference between remediation and an adverse opinion. It also prevents a February
dispute about whether the committee was informed. It is raised without concluding by describing the evidence and
the conditional structure — fourteen identified gaps, a five-month runway, three gaps whose character would be
difficult to distinguish from a material weakness if unremediated — while stating explicitly that no
operating-effectiveness testing has been performed and no conclusion reached.

## Key Definitions

**Accelerated filer.** An issuer that, among other conditions in Exchange Act Rule 12b-2, had a public float of
at least $75 million but less than $700 million as of the last business day of its most recently completed second
fiscal quarter. AtlasFlow was an accelerated filer for FY2024 and became a large accelerated filer for FY2025.

**Annual contract value (ACV).** The subscription value of a contract expressed on an annualized basis. It is
not a defined term and its computation varies: for ramped contract C-1, ACV is $600 on a year-1 basis, $800 on an
average-of-term basis, and $1,140 on an exit run-rate basis including the Insight add-on. Always establish which
definition the client's system implements.

**Annual recurring revenue (ARR).** The annualized contractual run rate of subscriptions active as of a point in
time, ordinarily excluding non-recurring items such as professional services and usage overage. It is not a GAAP
measure, appears in MD&A rather than the financial statements, and at AtlasFlow is computed in a Snowflake
datamart rather than in the general ledger. Do not use "revenue run rate" interchangeably with it.

**Audit plan.** The documentation of the nature, timing, and extent of the risk assessment procedures, tests of
controls, and substantive procedures to be performed, at the assertion level, including who performs each
procedure. Required by AS 2101 and AU-C 300.

**Audit strategy.** The documentation of the overall scope, reporting objectives, timing, direction, and
resources of the engagement, including preliminary materiality, the scope of work at components, significant
risks identified at planning, and the roles of specialists and other auditors. Required by AS 2101 and AU-C 300,
and communicated to the audit committee under AS 1301.

**Billings.** Amounts invoiced to customers in a period, net of credits. Not a financial statement caption, but
reconcilable to audited balances through the deferred revenue and receivable roll-forwards. AtlasFlow's FY2025
billings were $163,750.

**Bookings.** The contract value — on an ACV or TCV basis — of contracts signed in a period. It is neither a GAAP
measure nor a consistently defined one, and the treatment of renewals, expansions, and multi-year terms varies
by company and sometimes within a company. AtlasFlow's Q4 FY2025 new and expansion ACV bookings were $61,400.

**CAC payback period.** The number of months of gross-profit contribution from newly acquired recurring revenue
required to recover the sales and marketing spend that produced it, computed as sales and marketing expense
divided by the product of new recurring revenue and gross margin. AtlasFlow's FY2025 figure is 19.6 months on a
gross-ARR basis and 26.6 months on a net-ARR basis.

**Clearly trivial threshold.** The amount below which misstatements need not be accumulated because they are
clearly inconsequential individually and in aggregate. AtlasFlow's is $72, or 5% of overall materiality.
Chapter 3 owns the derivation.

**Cohort analysis.** The grouping of customers by the period in which they were acquired, followed forward over
time, so that the retention and expansion behavior of each vintage can be compared with that of earlier vintages
at the same age. It exposes deterioration in recent business that aggregate retention metrics conceal.

**Component materiality.** Materiality determined for a component of a group for purposes of the group audit,
set below group materiality to allow for aggregation of undetected misstatements across components. AtlasFlow's
UK component materiality is $580 and the Australian component amount is $420.

**Dollar-based gross retention (GRR).** Recurring revenue retained from a prior-period customer cohort,
excluding expansion, divided by that cohort's prior-period recurring revenue. It cannot exceed 100%. AtlasFlow's
FY2025 GRR is 91%, down from 93%.

**Emerging growth company (EGC).** An issuer qualifying for scaled disclosure and reporting accommodations under
the JOBS Act, including exemption from the auditor attestation requirement of Section 404(b), for up to five
fiscal years following its initial public offering and subject to revenue and float limits. AtlasFlow ceased to
qualify effective December 31, 2025.

**Engagement quality reviewer.** A partner or equivalent who performs an objective evaluation of the significant
judgments and conclusions of the engagement team, and who is not otherwise involved in the engagement. Luis
Herrera is Brightline's EQR on AtlasFlow, and the concurring-partner rotation limit applies to him as it does to
the lead partner.

**Group engagement team.** The partners and staff who establish the overall group audit strategy, communicate
with component auditors, perform work on the consolidation process, and evaluate the conclusions drawn from the
audit evidence as the basis for the group opinion. Brightline's Austin team performs this role for AtlasFlow.

**Integrated audit.** An audit in which the auditor's opinion on the effectiveness of internal control over
financial reporting is expressed in conjunction with the audit of the financial statements, with each audit
informing the other, under AS 2201. FY2025 is AtlasFlow's first.

**Large accelerated filer.** An issuer with a public float of $700 million or more as of the last business day
of its most recently completed second fiscal quarter, together with the other conditions in Exchange Act
Rule 12b-2. The status compresses the Form 10-K deadline to 60 days after fiscal year end.

**Magic number.** Net new annual recurring revenue divided by the prior period's sales and marketing expense, a
coarse measure of sales efficiency. AtlasFlow's FY2025 figure is 0.68 on an ARR basis and 0.58 on a revenue
basis.

**Net revenue retention (NRR).** Recurring revenue in the current period from a prior-period customer cohort,
including expansion, divided by that cohort's prior-period recurring revenue. It can exceed 100%. AtlasFlow's
FY2025 NRR is 112%, down from 118%.

**Performance materiality.** An amount set below overall materiality to reduce to an appropriately low level the
probability that the aggregate of uncorrected and undetected misstatements exceeds overall materiality.
AtlasFlow's is $940, or 65% of $1,450. Chapter 3 owns the derivation and the aggregation-risk rationale.

**Public float.** The aggregate worldwide market value of the voting and non-voting common equity held by
non-affiliates, measured for filer-status purposes as of the last business day of the issuer's most recently
completed second fiscal quarter. AtlasFlow's was $983.6 million at June 30, 2025.

**Remaining performance obligation (RPO).** The transaction price allocated to performance obligations that are
unsatisfied or partially unsatisfied at the reporting date, together with an explanation of when it is expected
to be recognized. It is a required ASC 606 disclosure and is therefore inside the audited financial statements.
Do not describe it as "backlog" without explaining the difference. AtlasFlow's was $214.0M at December 31, 2025,
of which $138.9M, or 64.9%, is expected within twelve months.

**Roll-forward procedures.** Procedures performed to extend a conclusion reached from testing at an interim date
to the period end, whose nature and extent depend on the length of the remaining period, the significance of the
control or balance, the results of interim testing, and whether the control or process changed. Not satisfied by
inquiry alone, and not available at all for a control that failed at interim.

**Rule of 40.** A heuristic that a software company's revenue growth percentage plus its profitability margin
should exceed 40. Because the profitability margin is undefined, the score is highly sensitive to the measure
chosen: AtlasFlow's FY2025 score is 8.2% on GAAP operating margin, 29.9% on a non-GAAP operating margin, and
47.8% on operating cash flow margin.

**Specified procedures.** A scope of work at a component in which the group engagement team or a component
auditor performs identified procedures over identified balances, classes of transactions, or disclosures,
without auditing the component's financial information as a whole and without expressing a conclusion on it. The
scope is meaningless without the enumerated list of procedures.

**Total contract value (TCV).** The aggregate amount a customer has committed to over the full contract term,
including non-recurring elements. C-1's TCV is $3,120 against a year-1 ACV of $600.

## Chapter Summary

1. A continuance memo documents a decision only if it states what changes in the audit because of each condition
   identified; Brightline's FY2025 memo attached four conditions, each of which generated a later workpaper.
2. AtlasFlow's $983.6 million public float at June 30, 2025 produced three consequences that shape every
   subsequent chapter: large accelerated filer status, loss of EGC status, and a first-year Section 404(b)
   auditor attestation requirement.
3. Independence on a software client runs in two directions, and the firm-as-customer analysis turns on
   documented facts — ordinary course, comparable terms, no promotional entanglement — rather than on instinct in
   either direction.
4. The engagement letter must be *established* with the audit committee, and it should contain the paragraph
   making the ICFR opinion expressly dependent on management's completed Section 404(a) assessment.
5. Strategy answers what kind of audit this is and what it requires; the plan answers what will be done to which
   population by whom. Significant risks and the use of internal audit are the two items most often misfiled.
6. Four different numbers describe the same customer commitment: bookings, billings, revenue, and cash. Every gap
   between them is composed of accounting judgments, and AtlasFlow's FY2025 bridge shows $98,700 of signed ACV
   producing $47,000 of live ARR, $163,750 of billings, $148,200 of revenue, and $154,480 of collections.
7. Operating metrics with no ledger anchor can be corroborated through a balance sheet account whose movement is
   a known percentage of the metric: AtlasFlow's $98,700 of bookings reproduces the $13,720 of required
   additions to the deferred commission asset to the dollar.
8. The composition of a retention decline matters more than its size: two of AtlasFlow's six points of NRR
   decline came from churn and contraction and pressure the credit-loss allowance and the commission
   amortization period, while four came from reduced expansion and pressure the metric itself and the ARR-based
   PSU probability.
9. The Rule of 40 spans 39.6 points at AtlasFlow depending on the profitability measure chosen, and stock-based
   compensation of 19.4% of revenue explains most of the spread — which is why "the company is above 40" is not
   an audit fact.
10. Scoping the integrated audit means identifying significant accounts and disclosures and their relevant
    assertions using the *same* materiality as the financial statement audit, and the significance test is the
    reasonable possibility of material misstatement, not magnitude.
11. Component scoping under the amended AS 2101 and the revised AU-C 600 is a risk-based determination, and the
    Australia conclusion rests on four enumerable component-specific risks rather than on an 8.4% revenue share.
12. The interim date is set from the client's change calendar, not the firm's resource calendar; roll-forward
    extent depends on what interim testing found, and a control that failed at interim is not rolled forward at
    all.
13. A first-year integrated audit of a company with 20 financially relevant applications and 14 known ITGC gaps
    roughly doubles the hours, and 1,370 of AtlasFlow's 2,700 incremental hours are control testing.
14. Internal audit's readiness assessment is a risk assessment input and a walkthrough starting point; it becomes
    evidence only where competence and objectivity have been assessed, the period matches, and the auditor
    re-performs a subset — which excludes everything touching revenue.
15. Telling the audit committee in September that an adverse ICFR opinion is a realistic outcome, with the
    specific gaps named and the remediation deadline stated, is a description of evidence rather than a
    conclusion, and it is the single highest-value item on the planning agenda.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Risk assessment procedures, the engagement team discussion, and assertion-level RMM | Chapter 2 | This chapter's business understanding and metric-pressure map are Chapter 2's inputs; Chapter 2 converts them into an assertion-level risk assessment matrix and identifies significant risks |
| Derivation of $1,450, $940, $72, $580, and $420 | Chapter 3 | This chapter uses the amounts and defers the arithmetic, the benchmark selection debate, and the revision analysis |
| The order-to-cash cycle and the December cut-off test | Chapter 4 | The response to the Q4 bookings concentration is designed in Chapter 2 and executed in Chapter 4 |
| Insight standalone selling price and contract modifications | Chapter 5 | The SSP significant risk identified at planning is audited here |
| Deferred revenue roll-forward, the billings bridge, and RPO recomputation | Chapter 6 | Proves that the $163,750 billings line is not a plug and recomputes the $214.0M RPO disclosure |
| CECL allowance and the DSO deterioration | Chapter 7 | The $4,000 of excess receivables implied by the 61-to-68-day DSO move is evaluated here |
| ITGC scoping, SOC 1 reports, bridge letters, and CUECs | Chapter 11 | The 940 budgeted IT audit hours are spent here; W-1 through W-14 are evaluated |
| Application controls, interfaces, and the Snowflake datamart | Chapter 12 | Why ARR computed outside the controlled environment is a control problem as well as a metric problem |
| Walkthrough technique | Chapter 13 | The September 8–19 walkthroughs referenced in the audit calendar |
| Control testing, roll-forward mechanics, and deficiency severity | Chapter 14 | Converts the interim and roll-forward strategy in §1.8 into tests, and evaluates the aggregate ITGC severity |
| Journal entry testing, including the 27 consolidation top-side entries | Chapter 16 | The top-side population identified in §1.7 is outside the NetSuite journal file |
| The December backdating scheme and the whistleblower allegation | Chapter 17 | Develops the fraud scheme the metric-pressure map in §1.5.6 anticipates |
| Precision, disaggregation, and the ARR-to-revenue bridge as a substantive analytic | Chapter 18 | Why the analytical-only option failed the Australia scoping test |
| Completion-stage audit committee communication and the ICFR conclusion | Chapter 19 | The bookend to the September planning communication in §1.11 |
| The report, including the adverse ICFR opinion and the CAMs | Chapter 20 | The outcome the September communication anticipated |

## Further Reading

- PCAOB AS 2101, *Audit Planning*, including the amendments addressing planning and supervision when other
  auditors participate in the audit, effective for audits of financial statements for fiscal years ending on or
  after December 15, 2024.
- PCAOB AS 1201, *Supervision of the Audit Engagement*, and AS 1215, *Audit Documentation*.
- PCAOB AS 1206, *Dividing Responsibility for the Audit with Another Accounting Firm*.
- PCAOB AS 1301, *Communications with Audit Committees*.
- PCAOB AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of
  Financial Statements*, particularly its treatment of materiality and of the top-down, risk-based scoping
  approach.
- PCAOB AS 1210, *Using the Work of an Auditor-Engaged Specialist*, and AS 2605, *Consideration of the Internal
  Audit Function*.
- PCAOB QC 1000, *A Firm's System of Quality Control*, effective December 15, 2025, and the Board's related
  release discussing engagement acceptance and continuance and resource sufficiency.
- SEC Regulation S-X Rule 2-01 and the SEC staff's published guidance on auditor independence in its Financial
  Reporting Manual and its Codification of Financial Reporting Policies.
- SEC Exchange Act Rule 12b-2 for the accelerated and large accelerated filer definitions, and Item 308 of
  Regulation S-K for the ICFR disclosures.
- The Division of Corporation Finance's frequently asked questions on management's report on internal control
  over financial reporting, for the position permitting exclusion of a recently acquired business.
- AICPA AU-C 210, *Terms of Engagement*; AU-C 220, *Quality Management for an Engagement Conducted in Accordance
  With Generally Accepted Auditing Standards*, effective for periods ending on or after December 15, 2025; and
  AU-C 300, *Planning an Audit*.
- AICPA AU-C 600, *Special Considerations — Audits of Group Financial Statements*, as revised, effective for
  periods ending on or after December 15, 2023.
- AICPA AU-C 610, *Using the Work of Internal Auditors*, and AU-C 620, *Using the Work of an Auditor's
  Specialist*.
- FASB ASC 606, *Revenue from Contracts with Customers*, particularly the disclosure requirements for remaining
  performance obligations, and ASC 340-40, *Other Assets and Deferred Costs — Contracts with Customers*.
- COSO, *Internal Control — Integrated Framework* (2013), for the control environment and monitoring components
  that the entity-level portion of the ICFR scope addresses.
- The Institute of Internal Auditors' *International Professional Practices Framework*, for the standards under
  which the internal audit function whose work you are evaluating operates.








