# Chapter 11 — Information Technology General Controls

> An information technology general control is never relevant for its own sake. It is relevant only because
> something else you intend to rely on — an automated calculation, a system-enforced approval, a report you are
> using as audit evidence — would be worthless if the general control failed. That makes the ITGC audit an
> exercise in dependency reasoning rather than in checklist completion, and it makes the most common ITGC
> workpaper in practice a defect: a matrix of thirty-four controls tested with no statement anywhere of what
> would break if any of them failed. AtlasFlow's FY2025 file contains fourteen known IT and control weaknesses
> and one shared administrator password held by six people, one of whom left the company in June. Deciding what
> those facts cost the audit requires you to trace, in both directions, the chain that runs from a financial
> statement assertion down through an application control to the general control beneath it.

## Learning Objectives

- **LO 11.1** Trace the dependency chain from a relevant assertion through an automated control or item of
  information produced by the entity (IPE) to the general information technology controls it relies on, and
  state the consequence when a link in the chain fails.
- **LO 11.2** Distinguish the five ITGC domains, identify which are professional requirements and which are firm
  methodology, and state the control objective each domain serves.
- **LO 11.3** Scope an IT environment by reaching and documenting an in-scope or out-of-scope conclusion, with a
  rationale, for every application in an inventory.
- **LO 11.4** Apply the IT layers concept to a vendor-hosted application and determine which layers the entity
  controls and which are covered by a service organization report.
- **LO 11.5** Map the risks arising from the use of information technology, as those risks are described in
  AS 2110 and in AU-C 315 as amended by SAS 145, to the general IT controls that address them.
- **LO 11.6** Design and evaluate tests of access provisioning, modification, and de-provisioning, including
  proving the completeness of the user and termination populations.
- **LO 11.7** Evaluate privileged access, system-enforced segregation of duties, and the periodic user access
  review, and compute the deviation rates each test produces.
- **LO 11.8** Distinguish the control design appropriate to vendor SaaS configuration changes from the design
  appropriate to in-house code, and construct an auditable population from a continuous-deployment pipeline.
- **LO 11.9** Evaluate the controls over an implementation project, including data conversion and the removal of
  legacy access at go-live.
- **LO 11.10** Evaluate a SOC 1 report — its scope, its opinion, its deviations, its gap period, its
  complementary user entity controls, and its treatment of subservice organizations — and conclude on the extent
  of reliance it supports.
- **LO 11.11** Determine whether benchmarking of an automated control is available, and state why it is
  unavailable in a first-year internal control over financial reporting (ICFR) audit.
- **LO 11.12** Convert an ITGC deficiency into a specific, quantified change in the substantive audit plan, and
  document the ITGC conclusion so that a reviewer can trace each conclusion to the reliance it supports.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2110 | Requires the auditor to obtain an understanding of how IT affects the flow of transactions, to identify the risks of material misstatement arising from the entity's use of IT, and to identify the controls that address them |
| PCAOB | AS 2201 | Governs the audit of ICFR: requires a top-down, risk-based scope; establishes that automated controls depend on general IT controls; addresses testing at an interim date and roll-forward; its appendix addresses benchmarking of automated application controls |
| PCAOB | AS 2301 | Requires the nature, timing, and extent of further procedures to respond to assessed risk, including the extent of substantive testing when controls cannot be relied upon |
| PCAOB | AS 1105 | Establishes sufficiency and appropriateness of evidence, including the requirement to evaluate the reliability of information produced by the entity — every access listing, change log, and deployment extract in this chapter is IPE |
| PCAOB | AS 2601 | Governs the auditor's consideration of an entity's use of a service organization, including the use of a service auditor's report and the evaluation of complementary user entity controls |
| PCAOB | AS 2401 | Requires consideration of management override and of the risk that individuals with privileged access can circumvent controls; the shared administrator account in §11.7 is squarely within its scope |
| PCAOB | AS 1305; AS 1215 | Require communication of control deficiencies identified in a financial statement audit, and documentation sufficient for an experienced auditor with no previous connection to the engagement to understand the work performed and the conclusions reached — the standard the §11.16 documentation package must satisfy |
| AICPA | AU-C 315, as amended by SAS 145 (effective for periods ending on or after December 15, 2023) | Introduced explicit requirements to identify the risks arising from the use of IT and the general IT controls that address them, and defined "general information technology controls" in the AICPA literature |
| AICPA | AU-C 402 | The AICPA analogue to AS 2601, governing the use of a service organization and of a Type 1 or Type 2 report |
| AICPA | AU-C 265 | Requires communication of significant deficiencies and material weaknesses to management and those charged with governance in a financial statement audit |
| AICPA | AU-C 330, AU-C 500 (AU-C 500 as revised by SAS 142, effective for periods ending on or after December 15, 2022) | Further audit procedures and the attributes of audit evidence, including the reliability of information from an external source and of information produced by the entity |
| AICPA | AT-C 320 | The attestation standard under which a service auditor examines and reports on controls at a service organization relevant to user entities' ICFR — the standard that produces the SOC 1 reports in §2.5 of the continuing case |
| COSO | *Internal Control — Integrated Framework* (2013), Principle 11 | States that the entity selects and develops general control activities over technology to support the achievement of objectives; the framework management uses for its Section 404(a) assessment |
| SEC | Section 404 of the Sarbanes-Oxley Act; Exchange Act Rules 13a-15; Item 9A of Form 10-K | Establish management's assessment, the auditor attestation requirement applicable to AtlasFlow for the first time in FY2025, and the disclosure of material weaknesses |
| FASB | ASC 350-40 | Internal-use software capitalization, which is why the source-control and project-management systems in §11.9 and §11.10 are financially relevant beyond their change-management role |

Because AtlasFlow is an SEC issuer and a large accelerated filer for FY2025, PCAOB standards govern and
Brightline LLP must express an opinion on ICFR. Readers auditing private SaaS companies apply the AICPA analogues,
with three differences that matter here. First, there is no ICFR opinion, so an ITGC deficiency affects the audit
only through the reliance it removes and through the AU-C 265 communication; it never produces an adverse opinion.
Second, AU-C 315 as amended by SAS 145 is more explicit than AS 2110 about the mechanics — identify the risks
arising from the use of IT for each application in which controls are relied upon, then identify the general IT
controls addressing those risks. The PCAOB reaches the same place through AS 2110 and AS 2201 without supplying the
same vocabulary. Third, SAS 145 contemplates an IT environment simple enough that general IT controls may not be
relevant at all because no automated controls are relied upon — available for a twelve-person company, and not for
AtlasFlow, whose revenue subledger is a configured third-party rules engine.

## Prerequisites and Chapter Dependencies

Read Chapter 2 first: this chapter responds to the risks arising from IT that Chapter 2 identifies, and it
assumes you already know how to state a risk of material misstatement at the assertion level. Chapter 1's
integrated-audit scoping and Chapter 3's materiality figures ($1,450 overall, $940 performance materiality, $72
clearly trivial threshold) are used without re-derivation. Chapter 12 owns the application-level automated
controls, the interface controls, and the completeness and accuracy of IPE that sit on top of everything
concluded here; Chapter 13 owns walkthrough technique; Chapter 14 owns test design mechanics, sample sizes, and
the deficiency severity framework, including the aggregation conclusion that turns AtlasFlow's ITGC deficiencies
into a material weakness. This chapter states deficiency conclusions where they are necessary to explain the
consequence for the audit plan, and defers the severity methodology to Chapter 14 in every case.

## 11.1 The Dependency Chain: Why an ITGC Is Relevant

An ITGC is a control over the IT environment rather than over a transaction. It never prevents or detects a
misstatement by itself. Its entire audit relevance is derivative: it makes something else trustworthy.

That "something else" is one of exactly three things.

1. **An automated control**, which processes transactions without human intervention — the CPQ discount approval
   matrix, the automated three-way match in Coupa, the RevPro allocation engine. You can test such a control
   once and conclude it operated consistently only if you can also conclude that nobody changed it and that it
   ran when it was supposed to. Those are ITGC conclusions.
2. **An IT-dependent manual control**, in which a person exercises judgment using a system-generated report.
   The person's diligence is a manual matter; the report's integrity is not.
3. **Information produced by the entity used directly as audit evidence** — the aged trial balance, the deferred
   revenue roll-forward, the journal entry population, the contract-level extract behind the $214,000 remaining
   performance obligation disclosure. AS 1105 requires you to evaluate its reliability, and reliability has a
   general-controls component that no amount of footing and re-adding addresses.

The discipline this imposes is directional. You do not begin with a list of ITGCs and ask which apply. You begin
with the reliance you intend to place, and you derive the ITGCs from it. Exhibit 11-1 is the FY2025 reliance
inventory for AtlasFlow, prepared before any ITGC testing was designed. It is the document that makes the rest
of the chapter's scope decisions defensible, and its absence is the single most common structural defect in an
ITGC file.

**Exhibit 11-1. FY2025 reliance inventory — what depends on general IT controls (amounts in thousands).**

| # | Reliance placed | Type | Application | Significant account / disclosure | Amount exposed | Relevant assertions |
| --- | --- | --- | --- | --- | --- | --- |
| R-1 | RevPro allocation and revenue-scheduling configuration (27 rules) | Automated | Zuora Revenue | 4100/4110/4120 revenue; 2400/2405/2410 deferred revenue | 135,800 revenue; 78,200 liability | Accuracy, cut-off, completeness |
| R-2 | CPQ discount approval matrix | Automated | Salesforce CPQ | Revenue | 148,200 | Occurrence, accuracy |
| R-3 | I-2 Billing-to-Revenue record-count and amount reconciliation | IT-dependent manual | Zuora Billing / Revenue | Revenue, deferred revenue | 163,750 of billings | Completeness, accuracy |
| R-4 | I-3 monthly revenue journal reviewed by the Controller | IT-dependent manual | Zuora Revenue / NetSuite | Revenue | 135,800 | Accuracy, classification |
| R-5 | Automated three-way match | Automated | Coupa | 2000 accounts payable; operating expenses | 7,600 | Occurrence, accuracy |
| R-6 | Journal entry second-approver configuration above $250 | Automated | NetSuite | All | 140,900 of manual entries | Occurrence, accuracy |
| R-7 | Aged trial balance used for the credit-loss estimate | IPE | NetSuite / Zuora Billing | 1200/1205/1210 | 38,600 gross AR | Valuation, existence |
| R-8 | Journal entry population extract (41,610 entries) | IPE | NetSuite | All | 1,842,300 absolute value | All |
| R-9 | Contract-level extract behind the RPO disclosure | IPE | Zuora Revenue / Snowflake | RPO disclosure | 214,000 | Presentation and disclosure |
| R-10 | Carta grant extract behind the SBC computation | IPE | Carta | 3100; SBC expense | 28,700 | Accuracy, completeness |
| R-11 | Payroll registers by entity | IPE | ADP, Deel | 2100/2105/2110; personnel costs | 16,400 accrued | Completeness, accuracy |
| R-12 | Workflow-run metering data behind usage overage | IPE | AtlasFlow platform (AWS) | 4120 | 4,200 | Completeness, accuracy |
| R-13 | FloQast reconciliation sign-off dates as evidence of close controls | IPE | FloQast | All | n/a — evidence of control operation | n/a |
| R-14 | ARR and NRR presented in MD&A | IPE | Snowflake RevOps datamart | Other information | 172,000 ARR | Consistency with the statements |

Account counts, user populations, job failure counts, and the FY2024 opening headcount of 731 used in this chapter
are extensions to the continuing case, invented for the illustration and internally consistent with it; every
figure drawn from the continuing case — the balances, the 3,100 deployments, the weaknesses W-1 through W-14, and
the §2.5 service organization reports — is used exactly as recorded there.

Read across any row and the ITGC question writes itself. Row R-1 relies on a configured rules engine, so
somebody must be prevented from changing the rules without authorization (program change), somebody must be
prevented from reaching the configuration screen at all (logical access), and the nightly job that feeds it must
run and be monitored (computer operations). Row R-8 relies on a data extract, so the query that produced it must
be what you think it is and the underlying table must not have been edited outside the application. Row R-12
relies on a metering pipeline that AtlasFlow itself wrote, deploys continuously, and runs on infrastructure it
manages — the only row in the inventory where all four IT layers belong to the client.

Now run the chain in the other direction, because that is the direction a deficiency travels.

**Exhibit 11-2. The dependency chain read backwards, from an ITGC failure to an audit consequence.**

| ITGC that failed | Immediate consequence | Reliance lost | Audit consequence |
| --- | --- | --- | --- |
| Access to the RevPro configuration is not restricted to authorized individuals and cannot be attributed to a person (W-1, W-6) | Any of at least six people could have changed an allocation rule, and the log cannot say who did | R-1, R-3, R-4, R-9 | The revenue subledger's output is not reliable as processed; revenue must be recomputed from contract data rather than tested by exception |
| Changes to in-house interface code are not approved (W-7) | The Stripe-to-NetSuite journal logic could have changed without review | R-5 is unaffected; the daily $6,100 self-serve revenue stream and account 1205 are | The daily cash-to-revenue reconciliation must be re-performed for a period rather than inspected for evidence of review |
| Terminated users' access is not removed timely (W-5) | Former employees retained the ability to transact | R-2, R-6, and every application control in Salesforce and NetSuite | Cannot conclude that only authorized individuals initiated transactions; expand cut-off and occurrence testing |
| The user access review is annual, not quarterly, and omits privileged accounts (W-3) | Inappropriate access persists undetected for up to a year | The detective control that would otherwise mitigate provisioning failures | Removes the fallback; provisioning deviations cannot be argued down by pointing to a review |
| Backup restoration was tested once and failed (W-14) | Recoverability of the metering data set is unproven | R-12, but only if a loss event occurred | No FY2025 loss event occurred, so no assertion is affected; the deficiency's severity turns on likelihood, not magnitude |

The fifth row is there deliberately. Not every ITGC failure costs the audit anything, and an ITGC file that
treats all five domains as equally consequential is not risk-based. The way to tell the difference is to ask
what reliance in Exhibit 11-1 the failure removes. If the answer is "none," say so and say why; do not pad the
deficiency list to look thorough.

## 11.2 The Five Domains

Practice organizes general IT controls into domains. Four of them are near-universal; the fifth is firm
methodology and should be described as such.

**Exhibit 11-3. The ITGC domains, their control objectives, and their status.**

| Domain | Control objective | Status | Typical controls | AtlasFlow weaknesses in the domain |
| --- | --- | --- | --- | --- |
| Logical access | Access to applications, data, and privileged functions is granted only to authorized individuals, is appropriate to their role, and is removed when no longer needed | Addressed by AS 2110 and AU-C 315 as a risk arising from IT; universally in scope where automated controls are relied upon | Provisioning approval, modification approval, de-provisioning, privileged access restriction and monitoring, periodic access review, authentication | W-1, W-2, W-3, W-5, W-6, W-13 |
| Program change | Changes to applications and configurations are authorized, tested, and approved before being placed in production | Same | Change request and approval, testing and user acceptance, segregation of development from production deployment, emergency change procedures | W-4, W-7 |
| Program development | New systems and major implementations are authorized, developed or configured to requirements, tested, converted accurately, and approved for go-live | Same | Project authorization, requirements sign-off, conversion reconciliation, user acceptance testing, go-live approval, post-implementation review, legacy access removal | W-2 (the September 2025 NetSuite upgrade) |
| Computer operations | Production processing is scheduled, executed, and monitored; failures are detected and resolved; data can be recovered | Same | Job scheduling and restriction of scheduler access, failure monitoring and alerting, incident management, backup, restoration testing | W-14 |
| Data management | Direct changes to data outside the application's normal processing are prevented or detected | **Firm methodology**, not a separate professional requirement; most firms treat it as a sub-domain of logical access or as a fifth domain in their own methodology | Restriction of direct database write access, logging and review of direct data changes, restriction of data-fix scripts | W-6 in part; the Snowflake access breadth noted in §2.1 |

Two clarifications matter before you write a scoping memo.

First, no professional standard prescribes this taxonomy. AS 2110 and AU-C 315 describe risks arising from the
use of IT and require you to identify the controls that address them; they do not require you to file those
controls under five headings. The taxonomy is useful because it is how client documentation, internal audit
reports, and SOC 1 reports are organized, and because it is a completeness check on your own thinking. It is not
authority for anything. If your firm's methodology names a sixth domain, use it and say it is methodology.

Second, data management is where the most consequential SaaS-specific gap hides, and it is easy to miss because
in a vendor-hosted application the client usually has no database access at all. That is a genuine strength: the
absence of an SQL prompt is a control. But it is not the whole population of out-of-application data change.
AtlasFlow has three:

- **Snowflake**, where 47 users have read access to replicated NetSuite, Zuora, and Salesforce tables and 6 have
  write access to the RevOps schemas. Read access does not change the general ledger, but write access to a
  schema that produces the ARR figure in MD&A changes reported information (W-11, developed in Chapter 12).
- **The consolidation workbook**, where a spreadsheet held on SharePoint carries 27 top-side entries totaling
  $6,200 outside NetSuite entirely (W-8).
- **Data-fix requests to vendors**, the population everybody forgets. AtlasFlow raised 9 support tickets with
  Zuora in FY2025 requesting direct data corrections; 4 were executed by Zuora support in the production tenant.
  Those are changes to the revenue subledger's data made by neither an AtlasFlow user nor an AtlasFlow program.
  Ask for the vendor support ticket history. It is the shortest high-yield ITGC request there is.

## 11.3 Scoping the IT Environment

Scoping has three steps, performed in this order, and the order is not cosmetic. Reversing it produces the
familiar file in which twenty applications are tested because they exist.

1. **Identify the population of applications.** Management's inventory is a starting point, not the population.
2. **Determine, for each, whether any reliance from Exhibit 11-1 runs through it.** This is the in-scope
   question, and the answer is a conclusion about reliance, not about size.
3. **For each in-scope application, determine the IT layers and who operates each one.** This decides which
   controls you test at the client and which you obtain from a service auditor.

### 11.3.1 Proving the inventory is complete

You cannot conclude on a population you have not proved. Brightline reconciled management's twenty-item
inventory to three independent sources:

- **The Okta application catalog**, listing 34 applications with an active single sign-on integration.
- **The Vanta system inventory**, listing 29 systems management has designated in scope for compliance
  monitoring.
- **A Coupa vendor-spend scan** of FY2025 disbursements coded to software, subscriptions, and IT services,
  identifying 46 distinct vendors.

The union of the three sources, after eliminating duplicates and non-systems (professional services vendors,
hardware resellers), was 51 distinct systems. Applying the reliance test in step 2 narrowed the field to
management's 20 plus 2 the team identified and management had not:

- **DocuSign**, holding the executed order forms for enterprise contracts. Chapter 4's existence testing traces
  to the signed order form; if the e-signature repository's integrity is unproven, so is the evidence. Concluded
  in scope for logical access only.
- **A Workato tenant** used from January to March 2025 to move subscription data between Zuora and Snowflake
  before Fivetran was implemented, decommissioned in April 2025 and therefore absent from every current-state
  inventory. Concluded out of scope, because the Q1 Snowflake data it produced was superseded by the Fivetran full
  historical reload in April 2025 — a conclusion that required the reload log as evidence, not an assumption.
  Current-state inventories systematically omit systems retired during the period, and a system retired in April
  was in production for a quarter of the year you are auditing.

### 11.3.2 The in-scope conclusion for all twenty applications

Exhibit 11-4 is the deliverable. Every row reaches a conclusion and gives a rationale, because a scoping memo
that lists ten in-scope applications and says nothing about the other ten has not documented a scope; it has
documented a subset.

**Exhibit 11-4. FY2025 IT scoping conclusions (WP 8100-01). Amounts in thousands.**

| # | System | Reliance from Exhibit 11-1 | Amount / volume anchor | Conclusion | Rationale |
| --- | --- | --- | --- | --- | --- |
| 1 | Salesforce Sales Cloud + CPQ | R-2 | 148,200 of revenue initiated; 3,140 enterprise customers | **In scope** — full ITGC set | Transactions are initiated and authorized here; the CPQ approval matrix is a relied-upon automated control; order-form data is the source for contract-term and pricing testing |
| 2 | Zuora Billing | R-3 | 163,750 of FY2025 billings | **In scope** — full ITGC set | Invoicing completeness and accuracy; the invoice register is the reciprocal population for deferred revenue completeness (Chapter 6, §6.4) |
| 3 | Zuora Revenue (RevPro) | R-1, R-3, R-4, R-9 | 135,800 subscription revenue; 78,200 deferred revenue | **In scope** — full ITGC set; highest risk | The revenue subledger; 27 configuration rules are relied upon as automated controls; changed February 2025 |
| 4 | NetSuite | R-6, R-7, R-8 | All balances; 41,610 journal entries; 1,842,300 absolute value posted | **In scope** — full ITGC set | The general ledger of record; upgraded September 2025 with segregation-of-duties roles rebuilt |
| 5 | Stripe | Supports R-7 | 6,100 of revenue; 11,400 accounts; account 1205 balance 1,700 | **In scope** — logical access and the I-4 interface only | AtlasFlow configures products and prices and holds dashboard access; processing is the service organization's, covered by a SOC 1 for the full fiscal year; the in-house Lambda job that posts the journal is AtlasFlow's code and is in scope for program change |
| 6 | Coupa | R-5 | Account 2000 balance 7,600; three-way match configuration | **In scope** — full ITGC set | The automated three-way match is relied upon; approval workflow configuration is an application control (Chapter 12) |
| 7 | SAP Concur | None | 2,900 of FY2025 T&E within operating expenses (extension) | **Out of scope** | No automated control or IPE is relied upon; T&E is tested substantively (Chapter 10) and the balance is below performance materiality of 940 in any plausible misstatement scenario. Logical access is reviewed only to the extent Concur can create payments, which it cannot — reimbursements are disbursed through ADP |
| 8 | ADP Workforce Now | R-11 | 96,300 of FY2025 US gross payroll (extension); 604 US employees | **In scope** — logical access at the entity; processing via SOC 1 | AtlasFlow controls who can add an employee and change pay rates; calculation is ADP's and is covered by an unqualified SOC 1 for January 1 – September 30, 2025 |
| 9 | Deel | R-11 | 19,000 of FY2025 UK, AU, and India personnel cost (extension); 208 employees | **In scope** — logical access at the entity; **no reliance on the service organization's change management** | Same design as ADP, but the SOC 1 is qualified as to change management, so the processing accuracy that ADP's report supports must be obtained substantively here (§11.13.6) |
| 10 | Carta | R-10 | 28,700 of SBC; account 3100 balance 412,300 | **In scope** — logical access and change (configuration) | Grant data drives the SBC computation; who can create or modify a grant record is a financially relevant access question; the SBC workbook itself is end-user computing (Chapter 12) |
| 11 | FloQast | R-13 | Evidence for 43 monthly reconciliation sign-offs | **In scope** — logical access only | Sign-off dates are audit evidence of the operation of close controls; if a user can back-date a sign-off, the evidence is worthless. Tested by inspecting the immutability configuration and the sign-off audit trail |
| 12 | Avalara | None | Account 2210 balance 2,900 | **Out of scope** | Tax determination output is not relied upon as an automated control; the sales/use and VAT accrual is recomputed substantively (Chapter 10). Rate-table changes affect an amount below performance materiality and are addressed by the accrual recomputation |
| 13 | Snowflake | R-9, R-14, and the source of most audit extracts | ARR of 172,000 and NRR of 112% reported in MD&A | **In scope** — logical access (including write access to RevOps schemas) and change (dbt model deployments) | Reporting layer producing other information and audit evidence; access is broader than access to the source systems; W-11 |
| 14 | AWS | R-12; hosting for Snowflake and the I-4 Lambda | Account 5100 hosting cost 13,400; 10,900 of FY2025 capitalized software | **In scope** — IAM administration and infrastructure-as-code change only | AtlasFlow operates the operating system, database, and network layers for its own platform, including the metering pipeline behind 4,200 of overage revenue. AWS's own controls over the physical and virtualization layers are covered by SOC 1 |
| 15 | Okta | Pervasive; supports every access conclusion | 812 employees; 34 integrated applications, of which 14 are financially relevant | **In scope** — full ITGC set; treated as a pervasive application | The authentication chokepoint. A failure here is a failure in every federated application simultaneously, which is why its own administrative access is tested at a higher extent |
| 16 | GitHub + CircleCI + Terraform | R-12; supports program change for all in-house code | 3,100 FY2025 production deployments; 10,900 of capitalized software | **In scope** — full ITGC set | The program change control set for everything AtlasFlow writes, including the I-4 Lambda job and the metering pipeline; also the source of the Jira/time data supporting capitalization under ASC 350-40 |
| 17 | Jira | Evidence for change and access controls | 3,100 deployments; the access-request workflow; the epic structure behind 10,900 of capitalization | **In scope** — logical access only | Holds the evidence for two other control sets. Ticket integrity — who can create, edit, or delete a ticket and its approval field — determines whether that evidence means anything. §2.1 records that ticket quality is uneven, which is a separate matter from ticket integrity |
| 18 | Vanta | None | n/a | **Out of scope** | An evidence aggregator, not a system of record and not the operator of any control. Vanta output offered as control evidence is IPE produced by a tool whose configuration and coverage must be verified before use; the team declined to use Vanta screenshots as primary evidence (§11.16) |
| 19 | First Meridian / JPMorgan bank portals | Supports cash testing | Account balances totaling 96,400; the 50,000 revolver | **In scope** — logical access and payment authorization only | Entitlement configuration determines who can release a payment; there is no change management or program development at the entity. Positive pay configuration is an application control (Chapter 8). The Treasury Manager is the sole administrator on two portals, a design point tested at §11.7.3 |
| 20 | Consolidation workbook (CONSOL_FY25_v14.xlsx) | Supports the consolidation | 27 top-side entries totaling 6,200 | **In scope as end-user computing, not as an application** | It has no application layer, no user administration, and no change management in any conventional sense. The relevant controls are access to the SharePoint location, version control, and formula-integrity checking, all of which are absent (W-8). Chapter 12 owns the spreadsheet control framework |

Fourteen in scope, three out of scope, one in scope as end-user computing, and two systems added to the
inventory. Three features of the exhibit are where scoping memos go wrong.

**Scope is per domain, not per application.** Writing "Stripe: in scope" and testing four domains wastes budget;
writing "Stripe: out of scope" because it is vendor-hosted loses $6,100 of revenue and 11,400 accounts. The middle
answer is right and must be documented at the domain level.

**A large balance is not a scoping criterion.** Concur touches $2,900 of expense and is out of scope; FloQast
touches no balance and is in scope. The criterion is whether reliance runs through the application.

**"Indirectly relevant" is not a conclusion.** The continuing case's inventory marks Avalara and AWS
"Indirectly." That is a useful flag in a client document and unusable in an audit file. Each must resolve to in or
out, and the resolutions differ: Avalara out, AWS in for two domains.

### 11.3.3 The IT layers

Every application runs on a stack. The conventional decomposition is four layers, and each layer is a separate
opportunity to change data or logic without passing through the application's own controls.

**Exhibit 11-5. IT layers for the in-scope applications, and who operates each.**

| Application | Application layer | Database layer | Operating system layer | Network layer | Entity-controlled layers |
| --- | --- | --- | --- | --- | --- |
| Salesforce CPQ | AtlasFlow (configuration, users, profiles) | Salesforce | Salesforce | Salesforce | 1 of 4 |
| Zuora Billing | AtlasFlow | Zuora (subservice: AWS) | Zuora | Zuora | 1 of 4 |
| Zuora Revenue | AtlasFlow | Zuora (subservice: AWS) | Zuora | Zuora | 1 of 4 |
| NetSuite | AtlasFlow | Oracle | Oracle | Oracle | 1 of 4 |
| Coupa | AtlasFlow | Coupa | Coupa | Coupa | 1 of 4 |
| Okta | AtlasFlow | Okta | Okta | Okta | 1 of 4 |
| Snowflake | AtlasFlow (roles, warehouses, schemas) | AtlasFlow (schema and object privileges) | Snowflake | Snowflake (with AtlasFlow-configured network policies) | 2.5 of 4 |
| AtlasFlow platform on AWS (metering, entitlement) | AtlasFlow | AtlasFlow (RDS) | AtlasFlow (EC2, container images) | AtlasFlow (VPC, security groups) | 4 of 4 |
| Consolidation workbook | none | none | AtlasFlow (SharePoint) | AtlasFlow | n/a |

The last two rows are why "it's all SaaS, so there's nothing to test" is wrong at a SaaS company. AtlasFlow is a
SaaS *vendor*; the platform it sells runs on infrastructure it operates, and the metering data that generates
$4,200 of overage revenue lives in a database its own engineers can reach. The full four-layer ITGC set applies
to that stack and to nothing else in the environment.

## 11.4 The Vendor-Hosted SaaS Scoping Problem

For twelve of AtlasFlow's fourteen in-scope applications, the entity controls exactly one layer. This is the
defining scoping problem of a SaaS-era audit, and it has a clean structure once you separate three questions
that are usually collapsed into one.

**Question 1: what does the entity actually control?** In a multi-tenant vendor-hosted application the entity
controls the tenant configuration and nothing else. Concretely, for Zuora Revenue, AtlasFlow controls: user
accounts and their roles; the 27 configuration rules; the report definitions; the API credentials; and the
tenant's integration settings. It does not control the application code, the database, the operating system, the
network, patching, backup, or the physical facility. Its own ITGCs therefore address one domain fully (logical
access), one domain in a modified form (program change, meaning configuration change rather than code change),
and two domains barely at all (program development, only when the entity implements or upgrades the tenant;
computer operations, only for jobs the entity schedules).

**Question 2: who covers the rest, and how do you know?** The layers beneath the application are covered by the
service organization's own controls, and your evidence about those controls is a SOC 1 report (§11.13). This is a
substitution of evidence, not an elimination of the requirement. If no SOC 1 exists, the requirement does not go
away; you either perform procedures at the service organization, obtain other evidence, or conclude that you
cannot rely on the automated controls in that application.

**Question 3: what falls between the two, and who owns it?** This is the gap that produces findings. The service
organization's report describes controls it operates *and* controls it assumes you operate. The latter are
complementary user entity controls, and W-10 records that AtlasFlow never mapped them. A CUEC is not the service
organization's control and not, until you map it, anybody's.

**Exhibit 11-6. Division of ITGC responsibility for a vendor-hosted application (Zuora Revenue).**

| Control activity | Operated by | Auditor's evidence | AtlasFlow status |
| --- | --- | --- | --- |
| Creation, modification, and removal of tenant user accounts | AtlasFlow | Test at the entity | Deficient (W-1, W-3, W-5) |
| Restriction of the Administrator role | AtlasFlow | Test at the entity | Deficient (W-1, W-6) |
| Authentication strength for tenant users | Shared — Okta federation is AtlasFlow's; the tenant's local-login option is a Zuora feature AtlasFlow chose not to disable | Test at the entity | Deficient — 4 local accounts bypass Okta (W-1) |
| Approval of configuration rule changes | AtlasFlow | Test at the entity | Deficient — cannot attribute 26 of 43 change events to a person |
| Approval and testing of Zuora's own application code releases | Zuora | SOC 1 Type 2 | Unqualified opinion, 1 deviation (2 of 25 change tickets lacked approval evidence) |
| Database, operating system, and network access at Zuora | Zuora | SOC 1 Type 2 | Covered, no deviations |
| Physical and environmental controls at the hosting facility | AWS as a subservice organization to Zuora | Carve-out in Zuora's report; covered by AWS's own SOC 1 | Covered, but only because AtlasFlow separately obtained AWS's report (§11.13.5) |
| Backup and recoverability of the tenant database | Zuora | SOC 1 Type 2 | Covered |
| Restriction of Zuora support personnel's access to the AtlasFlow tenant | Zuora | SOC 1 Type 2 | Covered by Zuora's controls, but the 4 data-fix tickets executed in production are AtlasFlow's authorization question, not Zuora's |

The last row repays reading twice. Zuora's controls tell you its support staff's access was restricted and logged.
They tell you nothing about whether AtlasFlow authorized the four data corrections Zuora support executed inside
the revenue subledger. That authorization is AtlasFlow's control, it sits in no domain in management's matrix, and
Brightline tested it by obtaining the four tickets and tracing each to an approval from Daniel Kim or Jordan Pike.
Three had one; one — a correction to 11 revenue contracts' start dates in May 2025 — was requested by a Larkspur
Consulting implementation consultant with no AtlasFlow approval in the thread.

Resist scope creep in the other direction: the extent should track the reliance. Brightline tested six logical
access controls each in Zuora Revenue, NetSuite, and Salesforce; two in Carta and FloQast; one in the bank
portals. The differentiator is Exhibit 11-1, where four reliance items run through Zuora Revenue and one through
FloQast.

## 11.5 Risks Arising from the Use of IT

AS 2110 requires you to identify risks of material misstatement arising from the entity's use of IT. AU-C 315 as
amended by SAS 145 makes the same requirement operational: identify the risks arising from the use of IT for the
applications in which you are relying on controls, then identify the general IT controls that address those
risks. The risks themselves are stable across engagements and there are five of them. What varies is their
manifestation.

**Exhibit 11-7. Risks arising from the use of IT, mapped to general IT controls and to AtlasFlow facts.**

| Risk arising from IT | How it manifests at AtlasFlow | ITGC domain addressing it | Specific control tested | FY2025 result |
| --- | --- | --- | --- | --- |
| Unauthorized access to data results in destruction or improper changes, including recording unauthorized or non-existent transactions | Six people share the `revpro_admin` credential; 2 developers hold standing write access to production RevPro configuration; 47 Snowflake users can read replicated GL data | Logical access; data management | Provisioning approval; privileged access restriction; periodic review; authentication | Not effective (W-1, W-3, W-5, W-6) |
| Unauthorized changes to systems or programs | 26 of 43 RevPro configuration change events cannot be attributed; 2 Lambda modifications have no approval; 6 of 3,100 deployments bypassed the pipeline | Program change | Change approval; testing; segregation of deployment from development; emergency change procedure | Not effective (W-4, W-7) |
| Failure to make necessary changes to systems or programs | The Q1 2025 metering counter defect went 6 weeks before an emergency fix; the RevOps datamart reconciliation was not built until December 2025 | Program change; computer operations | Incident management; monitoring | Partially effective; see §11.10 |
| Inappropriate manual intervention in automated processing | 91 manual revenue-schedule adjustments in RevPro; 27 top-side consolidation entries outside NetSuite; 3,847 manual journal entries below the second-approver threshold | Logical access; data management; application controls (Chapter 12) | Restriction of override capability; review of overrides | Not effective (W-12, W-13) |
| Loss of data or inability to access data as needed | One restoration test in FY2025, which failed; retest completed January 2026 | Computer operations | Backup configuration; restoration testing | Not effective (W-14), but see the consequence analysis in Exhibit 11-2 |

Two disciplines make this exhibit useful rather than decorative.

**State the risk at the level of the application, not the environment.** "Unauthorized access" as an
environment-wide risk generates an environment-wide control matrix and no insight. The risk that matters is
"unauthorized access to the RevPro configuration could change the allocation of transaction price across
performance obligations for the entire subscription population, affecting the accuracy assertion for $135,800 of
revenue" — a sentence that names the application, the mechanism, the population, the amount, and the assertion,
and thereby justifies testing six controls in one application and one in another.

**Do not stop at the ITGC.** If no control addresses an identified risk, that is the answer, and it is a design
rather than an operating deficiency — a distinction that matters here because a design deficiency cannot be
remediated by testing more.

## 11.6 Logical Access: Provisioning, Modification, and De-provisioning

Logical access is where roughly 60% of ITGC testing effort goes and where more than half of reported ITGC
material weaknesses originate. The reason is structural: it is the only domain whose population is generated by
human resources events rather than by IT events, which means its completeness depends on a reconciliation across
two organizations that do not report to each other.

### 11.6.1 The control design

There are four controls, and they are separate controls with separate populations. Collapsing them into "access
is appropriately managed" makes the test undesignable.

| Control | Population | Nature | Frequency |
| --- | --- | --- | --- |
| C-ITGC-01 Provisioning | New access grants in the period | Preventive; authorization before creation | Per event |
| C-ITGC-02 Modification | Role or entitlement changes to existing accounts | Preventive; authorization before change | Per event |
| C-ITGC-03 De-provisioning | Separations and role exits | Preventive/corrective; removal within the SLA | Per event |
| C-ITGC-04 Periodic review | The full active user listing | Detective; recertification by the data owner | Quarterly per documentation |

AtlasFlow's documented design, obtained by walkthrough with Ray Sandoval (Director, IT and Information
Security), is: a Jira Service Management request is raised on the "IT Access" project; the requester's manager
approves; for financially relevant applications the designated data owner also approves (Elena Vasquez for
NetSuite, Daniel Kim for Zuora Revenue, Brett Hallowell for Salesforce); the IT Operations Analyst provisions;
the ticket is closed with the role granted recorded in a custom field.

Three design questions to ask before testing anything, each of which has produced a design deficiency on real
engagements:

1. **Is the approver independent of the requester and of the provisioner?** At AtlasFlow the data owner for
   Salesforce is Brett Hallowell, who is also the Salesforce administrator. He therefore approves and provisions
   his own application's access, and he can grant himself entitlements without any second party. That is a design
   deficiency in a control the client believes operates, and it connects to the Chapter 17 fraud scenario in
   which he can modify order-form dates.
2. **Does the ticket record what was actually granted, or what was requested?** If it records the request, the
   test cannot detect over-provisioning, because the evidence and the assertion are the same document. AtlasFlow's
   custom field records the request. Brightline therefore tested the granted role from the application's own
   audit trail rather than from the ticket — a change in the *source* of evidence, not in the sample.
3. **Is there a path to access that does not pass through the control?** There are always at least two: local
   accounts created directly in the application (W-1's four in Zuora Revenue) and accounts created by an
   integration or by the vendor during implementation. Both must be enumerated, because the control's population
   is defined by the ticket queue and those accounts are not in it.

### 11.6.2 De-provisioning and the completeness problem

De-provisioning is the control most often tested wrongly, because the natural population — the list of accounts
IT disabled — is the wrong population. It proves that what was removed was removed. The assertion is that
everything that should have been removed was.

The correct population is the population of *separation events*, sourced from outside IT. Building it at
AtlasFlow required reconciling two payroll systems, a contractor population, and an acquisition.

**Exhibit 11-8. FY2025 termination population build and completeness proof (WP 8200-04).**

| Step | Source | Count | Tick |
| --- | --- | --- | --- |
| US separations, January 1 – December 31, 2025 | ADP Workforce Now termination report | 214 | (a) |
| UK, Australia, and India separations | Deel separation report, 3 entities | 54 | (a) |
| **Subtotal — separations per payroll systems** | | **268** | |
| Less: internal transfers recorded as a termination and rehire in the same entity | ADP transfer report; corroborated to the Okta deactivate/recreate log | (7) | (b) |
| Add: contractors and consultants with application access, not on any payroll | Coupa vendor master, individuals with an Okta account | 19 | (c) |
| Add: former Kestrel Labs employees separated after August 4, 2025 while still on Kestrel's pre-migration payroll | Kestrel payroll file provided by the acquisition integration lead | 4 | (c) |
| **Total population of access-removal events** | | **284** | |

Tick mark legend:
(a) Report parameters inspected; date range and status filter agreed to the request; report regenerated in the
    auditor's presence and record count agreed.
(b) Each of the 7 traced to a continuing employee record with an unbroken service date; excluded because no
    access removal was required, but Okta shows a deactivation and recreation, which is why they appear in the
    Okta log reconciliation below.
(c) Population identified by the auditor, not by management; management's original termination listing contained
    268 items and omitted all 23.

Three independent corroborations of the 284, because one reconciliation to one source proves nothing about that
source:

1. **Headcount roll-forward.** 731 employees at December 31, 2024, plus 349 hires, less 268 separations, equals
   812 employees at December 31, 2025, which agrees to the headcount disclosed in the Form 10-K (US 604, UK 71,
   Australia 38, India 99). The roll-forward proves the payroll-sourced 268, not the full 284.
2. **Okta deactivation log.** 291 deactivation events in FY2025, reconciling to 284 access-removal events plus
   the 7 transfer-related deactivate-and-recreate pairs. This is the strongest of the three because it is sourced
   from the access system itself and runs in the opposite direction to the payroll build.
3. **Final-paycheck report.** 268 final payments, agreeing to the payroll-sourced separations, and corroborating
   that the ADP and Deel termination reports were not filtered.

If the three do not reconcile, the difference is the finding: an excess of identity-provider deactivations over
payroll separations is usually a missing worker category, and an excess of separations over deactivations is
usually a set of individuals provisioned directly in the applications, which is W-1 in another guise.

### 11.6.3 Testing the 284

The metric is days from the separation effective date to removal of the last financially relevant entitlement.
AtlasFlow's documented service level is 24 hours. Because the population is 284 and the extract is machine-
generated, the team tested 100% rather than sampling; Chapter 14, §14.5 explains when a full-population test is
available and what it costs.

**Exhibit 11-9. Access removal timeliness, all 284 events (WP 8200-05).**

| Days from separation to final entitlement removal | Events | Aggregate days | Average days | Within 24-hour SLA? |
| --- | --- | --- | --- | --- |
| 0 to 1 day | 74 | 52 | 0.7 | Yes |
| 2 to 3 days | 55 | 139 | 2.5 | No |
| 4 to 7 days | 78 | 428 | 5.5 | No |
| 8 to 14 days | 50 | 528 | 10.6 | No |
| 15 to 30 days | 24 | 476 | 19.8 | No |
| Over 30 days | 3 | 138 | 46.0 | No |
| **Total** | **284** | **1,761** | **6.2** | |

The average of 1,761 ÷ 284 = 6.20 days agrees to W-5. The deviation rate is 210 of 284, or 73.9%. A control with
a 73.9% deviation rate is not a control that failed on occasion; it is a control that does not operate, and the
correct conclusion is available without any sampling theory. Note what the average conceals and the distribution
reveals: 74 events were compliant, which means the process *can* work, and the failures are not uniformly
distributed. Cross-tabulating by month showed 41 of the 74 compliant removals occurred in November and December
2025, after Brightline's interim testing put the client on notice — evidence of remediation activity in the
fourth quarter that Chapter 14 must consider in the as-of evaluation, and evidence that the control was worse
than 73.9% for the first ten months.

The three events over 30 days are the three Salesforce cases in W-5, and the mechanism is worth stating because
it recurs. All three employees were deactivated in Okta within 3 days. Salesforce, however, was configured to
permit both single sign-on and local username-and-password login, and the Salesforce user records were not
deactivated. Okta deactivation therefore removed the front door and left a side door open for 34, 41, and 63
days respectively.

**What an unexpected result looks like, and the next step.** For a de-provisioning exception the question is
never merely "how late was it." It is "did anything happen during the window." The procedure is to obtain the
application's login history for each exception and, where logins occurred, the activity log for the session:

- Of the three, one — a former Sales Operations analyst, separated August 12, 2025, Salesforce access removed
  October 14, 2025 — logged in 4 times after separation, most recently 19 days after. The activity log showed
  report execution only: 6 report runs, no record creates, updates, or deletes. Brightline obtained the
  Salesforce field-history for all opportunity records the user could reach in that period and confirmed no
  changes. Conclusion: a control deviation with no identified misstatement.
- The other two showed no post-separation login activity.

Had the activity log shown record modifications, the next steps would have been: identify the records changed,
quantify the effect on revenue and receivables, evaluate whether the change indicates fraud under AS 2401,
notify the engagement partner and consider notification to the audit committee, and reassess the fraud risk
assessment. The distinction between "no logins occurred" and "we did not look" is the entire evidential value of
the procedure, and files routinely contain the second while asserting the first.

## 11.7 Privileged Access, Segregation of Duties, and Authentication

### 11.7.1 Privileged access

A privileged account can change the configuration that constitutes the automated control, grant itself further
access, alter or delete the audit log, and in many applications modify posted data. Every conclusion you reach
about an automated control is conditional on the size and composition of the privileged population. The test is
therefore not "was privileged access approved" but "who has it, is it justified by a job requirement, and can
what they did be attributed to them."

**Exhibit 11-10. Privileged access inventory for the in-scope applications at December 31, 2025 (WP 8210-02).**

| Application | Privileged role | Accounts | Named individuals | Shared or service accounts | MFA enforced | Attributable? | Conclusion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NetSuite | Administrator | 6 | 6 (Ray Sandoval, the IT Operations Analyst, a Senior Systems Analyst, the Director of Financial Systems, Elena Vasquez, and one NetSuite implementation partner consultant) | — | Yes, via Okta | Yes | Elena Vasquez's Administrator role is a segregation-of-duties conflict (W-13); the partner consultant's account should have been removed at the September 2025 go-live |
| NetSuite | Integration/API roles | 12 | — | 12 | n/a — key-based | Yes, per key | 3 of 12 keys had no documented owner; 1 key had not been rotated since the FY2023 implementation |
| Zuora Revenue | Administrator (federated) | 3 | 3 (Daniel Kim, Jordan Pike, Ray Sandoval) | — | Yes | Yes | Jordan Pike's Administrator role conflicts with his performance of the RevPro-to-GL reconciliation |
| Zuora Revenue | Administrator (local, non-federated) | 4 | 2 (`d.kim.local`, `zuora_support_ta`) | 2 (`revpro_admin` shared with 6 vault holders; `svc_revpro_integration`) | **No** | **No for `revpro_admin`** | W-1; the subject of the case study |
| Zuora Billing | Administrator | 4 | 4 | — | Yes | Yes | 1 of 4 is a Billing Analyst whose role requirement is credit-memo issuance, not administration |
| Salesforce | System Administrator | 5 | 4 (including Brett Hallowell) | 1 (integration) | Yes | Yes | 5 System Administrators in a 3,140-customer org is not itself excessive; the design defect is Hallowell's combination of administration and approval authority |
| Okta | Super Administrator | 3 | 2 (Ray Sandoval, 1 IT Operations Analyst) | 1 (break-glass account) | Yes | Yes | The break-glass account's credential is in the same shared vault as `revpro_admin`; its use is alerted but the alert had no documented disposition |
| Snowflake | ACCOUNTADMIN / write to RevOps schemas | 6 | 5 | 1 (Fivetran service) | Yes | Yes | 2 of the 5 are RevOps analysts outside the finance organization; relevant to W-11 |
| AWS | IAM users with console access | 34 | 34 | — | **No — 7 of 34** | Yes | Fails an AWS SOC 1 complementary user entity control (§11.13.4) |
| Coupa | Administrator | 2 | 2 | — | Yes | Yes | No exception |
| Carta | Administrator | 3 | 3 | — | Yes | Yes | No exception |
| Bank portals | Administrator | 2 | 1 (Nate Oyelaran, on both) | — | Yes, token-based | Yes | Sole administrator on two portals with no second administrator and no compensating review of entitlement changes; a design deficiency independent of any deviation |

Three observations follow from the exhibit.

**Count shared and service accounts separately from named ones.** A named privileged account is a question of
appropriateness; a shared account is a question of attribution, and attribution failure defeats every downstream
test; a service account is a question of credential management. AtlasFlow's 12 NetSuite integration accounts
include 3 with no documented owner, so no human is accountable and no personnel change will ever trigger rotation.

**Ask whether the population you are examining can alter the audit log.** NetSuite and Salesforce system notes and
field history are not editable by an Administrator, which preserves their evidential value. In the Snowflake
RevOps schemas an ACCOUNTADMIN can drop and recreate a table, and the query history records the DDL but not the
prior contents. Document the difference rather than assuming it away.

**Test what the privileged accounts did.** Brightline extracted FY2025 activity for the 6 NetSuite Administrator
accounts: 1,847 logged administrative actions, of which 214 were role or permission changes, 38 were approval
workflow configuration changes, and 9 were chart-of-accounts changes. The 38 matter most, because the $250,000
second-approver threshold (W-12) is a workflow configuration. All 38 traced to a change ticket; 2 were the
September 2025 upgrade rebuild, covered by the project testing in §11.11.

### 11.7.2 Segregation of duties within an application

Segregation of duties is a control objective, not a control. The control is the role design plus whatever
enforces it. In an application the enforcement mechanism is the permission model, and the audit procedure is a
conflict analysis: define incompatible function pairs, map roles to functions, and identify users holding both
sides of a pair.

**Exhibit 11-11. NetSuite segregation-of-duties conflict analysis at December 31, 2025 (WP 8210-04).**

| Conflict pair | Why incompatible | Users holding both | Names / notes | Mitigation asserted by management | Auditor's evaluation |
| --- | --- | --- | --- | --- | --- |
| Create vendor + approve payment | Enables payment to a fictitious vendor | 1 | AP Supervisor | Bank positive pay on account 1010 | Partially effective; positive pay is not enabled on 1015 (Chapter 8) |
| Prepare journal entry + post journal entry | Enables an unreviewed entry | 9 | Includes Elena Vasquez (W-13) | Second approver above $250,000 | Ineffective for the 3,847 entries below the threshold (W-12) |
| Post journal entry + modify interface mapping | Enables an entry that reconciles to a manipulated feed | 1 | Elena Vasquez (W-13) | Monthly reconciliation reviewed by the CFO | Not tested by management; the reconciliation's preparer is in the conflict |
| Administer users + provision own access | Enables self-granted entitlements | 2 | IT Operations Analyst; Brett Hallowell in Salesforce | Quarterly access review | Ineffective — the review is annual (W-3) |
| Enter customer master + issue credit memo | Enables concealment of a receivable | 3 | Billing Analysts | Credit memos above $50 require Controller approval | Effective by design; tested in Chapter 12 |
| Change RevPro configuration + perform the revenue reconciliation | Enables a configuration change that self-reconciles | 2 | Daniel Kim, Jordan Pike | None asserted | Ineffective; central to the case study |
| **Total distinct users in at least one conflict** | | **14** | | | |

The count of 14 distinct users reconciles to the 214 manual journal entries posted by users with segregation-of-
duties conflicts recorded in §3.6 of the continuing case; Chapter 16 uses that population as a journal entry
selection criterion, which is the standard response when the conflict cannot be eliminated.

Two technique points. Define the conflict pairs before you look at the roles, or you will define them to match what
you find; use the client's matrix, your firm's ruleset, or the vendor's published conflict library, and document
which. And a conflict is a design condition, not a deviation: it exists on day one and every day after, so there is
no sample. The test is inspection of the role-to-user mapping at a point in time plus a determination that the
mapping did not change during the period — which at AtlasFlow it did, in September 2025, which is why §11.11 exists.

### 11.7.3 Administrative access outside the ERP

Two populations sit outside the finance applications and are routinely missed.

**The identity provider.** An Okta Super Administrator can add themselves to any federated application's group and
inherit its entitlements without touching that application's user administration. AtlasFlow's 3 Super
Administrators are defensible in number; the defects are that the break-glass credential lives in the same shared
vault as `revpro_admin` and that the alert on its use fired twice in FY2025 (March 4 and the September 20 NetSuite
go-live) with no documented disposition. Brightline obtained the Okta system log for the March 4 session: the
account restored access for the IT Operations Analyst after a lockout, corroborated by a Jira incident ticket the
same afternoon. That is an adequate answer arrived at after the fact, not evidence that a control operated.

**Payment portals.** Nate Oyelaran is the sole administrator on two bank portals. There is no deviation to find,
because a sole administrator cannot deviate from a procedure that does not exist; the finding is a design
deficiency, since entitlement changes are unreviewed and the person who can make them can also initiate payments.
The FY2025 response was to obtain the entitlement change reports (3 changes, all traced to a documented request)
and to test the payment population for unauthorized disbursements (Chapter 8).

### 11.7.4 Authentication: single sign-on, MFA, and the non-federated population

Federation through an identity provider is the strongest access control most SaaS companies have, because it
centralizes the join, move, and leave events that otherwise have to be executed correctly fourteen times. It also
concentrates risk, and — critically for the audit — it is never complete.

**Exhibit 11-12. Authentication coverage for the in-scope applications at December 31, 2025 (WP 8210-06).**

| Application | Accounts | Federated through Okta | Local accounts | MFA on local accounts | Local-login path disabled at the application? |
| --- | --- | --- | --- | --- | --- |
| Salesforce | 318 | 318 | 0 | n/a | **No** — local password login remained enabled, which is the mechanism behind the three over-30-day exceptions in §11.6.3 |
| Zuora Billing | 41 | 41 | 0 | n/a | Yes |
| Zuora Revenue | 27 | 23 | **4** | **No** | **No** (W-1) |
| NetSuite | 214 | 202 | 12 (integration/API, key-based) | n/a | Yes for interactive login |
| Coupa | 96 | 96 | 0 | n/a | Yes |
| Carta | 11 | 11 | 0 | n/a | Yes |
| FloQast | 18 | 18 | 0 | n/a | Yes |
| Snowflake | 47 | 41 | 6 (5 service, 1 break-glass) | Key-pair authentication | Yes for human users |
| AWS | 34 console users | 0 — AWS IAM is not federated to Okta | 34 | **27 of 34** | n/a |
| Stripe | 7 | 7 | 0 | n/a | Yes |
| **Total accounts across the above** | **813** | **757** | **56** | | |

The exhibit foots: 757 federated plus 56 local equals 813. The audit-relevant number is 56, not 813, because the
56 are the population that bypasses every control the identity provider provides — the joiner approval, the
leaver deactivation, the MFA enforcement, and the session policy.

Work the 56 down to the ones that matter:

- **12 NetSuite integration accounts** and **5 Snowflake service accounts**: no interactive login, key-based, so
  the leaver risk does not apply. The relevant control is key ownership and rotation, tested at §11.7.1, where 3
  of 12 failed on ownership.
- **2 break-glass accounts** (Okta and Snowflake): justified by design, but the credential custody and the alert
  disposition failed.
- **34 AWS IAM console users**: 7 without MFA, which fails an AWS complementary user entity control. Brightline
  determined that all 7 were engineers without permissions to the metering database or the billing pipeline, which
  limits the magnitude but does not remedy the CUEC failure.
- **4 Zuora Revenue local administrators**, of which one is shared. This is the population with the shortest path
  to a material misstatement in the financial statements, and §11.15 and the case study develop it.

The exception population, not the federated population, is where the work is. The question that opens it is
specific: *for each in-scope application, list every account that can authenticate without passing through Okta,
including service accounts, API keys, vendor support accounts, and any account created before federation.*

## 11.8 The Periodic User Access Review

The access review is the detective control that catches what provisioning and de-provisioning miss. When it
works, a provisioning deviation is contained to at most one review cycle. When it does not, every access
deficiency compounds, which is why W-3 is more consequential than its description suggests.

AtlasFlow's documentation describes a quarterly review of Salesforce, Zuora, and NetSuite by the data owner, with
a deadline of 15 days after quarter end. Chapter 13's walkthrough is where the discrepancy surfaced: the
documented control is quarterly and the performed control is annual.

**Exhibit 11-13. Access review instances expected and performed, FY2025 (WP 8210-08).**

| Application | Instances expected per documentation | Instances performed | Date performed | Documented deadline | Days late | Deviation |
| --- | --- | --- | --- | --- | --- | --- |
| Salesforce | 4 | 1 | August 25, 2025 | July 15, 2025 (Q2 instance) | 41 | Frequency and timeliness |
| Zuora Billing and Revenue | 4 | 1 | August 25, 2025 | July 15, 2025 (Q2 instance) | 41 | Frequency and timeliness |
| NetSuite | 4 | 1 | November 7, 2025 | October 15, 2025 (Q3 instance) | 23 | Frequency and timeliness |
| **Total** | **12** | **3** | | | | 9 instances not performed |

Frequency is only the first failure. Test the quality of the instances that did occur, because a review performed
on an incomplete population or with no evidence of investigation is a deficiency even at the documented
frequency. Four attributes, tested on the November 7 NetSuite review:

1. **Completeness of the reviewed population.** The listing reviewed contained 196 accounts. The NetSuite user
   listing at the review date contained 214. The 18 omitted accounts were the 12 integration accounts and the 6
   Administrator accounts — precisely the highest-risk accounts in the application, excluded because the saved
   search that generated the listing filtered on employee records.
2. **Evidence of what the reviewer considered.** Elena Vasquez's evidence was an email stating "reviewed and
   approved" with the spreadsheet attached. There was no annotation, no per-user disposition, and no record of the
   criteria applied. A reviewer who returns an unmarked listing has provided evidence of receipt, not of review.
   Chapter 14, §14.9 develops the precision analysis for review controls generally.
3. **Disposition of items identified.** 9 accounts were flagged for removal. 6 were removed within 10 business
   days. 3 remained active at December 31, 2025 — 55, 55, and 54 days after being flagged. A detective control
   whose findings are not actioned does not detect anything in the sense that matters.
4. **Appropriateness of the roles retained.** For 25 of the 196 accounts Brightline independently evaluated the
   role against the individual's job description. 23 agreed. 2 did not: an FP&A analyst held the "Journal Approver"
   role and a sales-operations contractor held "A/R Clerk," neither of which the review had questioned.

Aggregating: 9 of 12 instances not performed, 18 of 214 accounts omitted from the one instance tested, 3 of 9
identified items unresolved, and 2 of 25 roles inappropriate. There is no version of this control that can be
relied upon, and it follows that the provisioning and de-provisioning deficiencies have no detective backstop —
which is the analysis that drives severity in Chapter 14 rather than the raw count of deviations.

**What effective looks like, for calibration.** The listing is generated by IT from the application rather than by
the reviewer; it includes every account type, service and privileged accounts included; the reviewer records a
per-user decision (retain, modify, remove) with a date; and removals are tracked to completion with an aging
report escalated to the control owner. With all four present the control is testable by inspecting the listing, the
annotations, and the removal tickets. With only the first two, you are testing a distribution, not a review.

## 11.9 Change Management: Vendor Configuration versus In-House Code

AtlasFlow has two change populations with two different control designs, and treating them as one is the most
common program-change failure in a SaaS environment. The distinction is not cosmetic: one population is small,
high-impact, and made through a user interface with no build pipeline; the other is large, mostly irrelevant, and
made through a pipeline that can itself enforce the control.

**Exhibit 11-14. Two change populations, two control designs.**

| Attribute | Vendor SaaS configuration | In-house code |
| --- | --- | --- |
| Example | The 27 RevPro configuration rules; the CPQ approval matrix; the NetSuite $250,000 approval threshold | The I-4 Stripe Lambda job; the metering pipeline; the dbt RevOps models; Terraform infrastructure definitions |
| FY2025 population | 43 RevPro configuration change events; 38 NetSuite workflow-configuration changes | 3,100 production deployments, of which 583 are financially relevant |
| Made by | A privileged application user, through a screen | A developer, through a pull request and a pipeline |
| Separate development environment? | Usually a sandbox that is not a true copy and cannot be promoted automatically | Yes, with automated promotion |
| Who can promote to production | Anyone with the privileged role — there is no technical separation of "develop" from "deploy" | Restricted by branch protection and pipeline credentials |
| Control that fits | Documented request, approval by the process owner, evidence of testing in sandbox, and a log of production changes reconciled to approvals | Branch protection requiring an independent reviewer plus a passing pipeline; the control is automated and testable by configuration |
| Why the other design fails | A pipeline cannot be imposed on a vendor's configuration screen; requiring one produces a control nobody performs | A ticket-and-approval control applied to 3,100 deployments produces 3,100 tickets of no evidential value |
| AtlasFlow status | Deficient — 26 of 43 RevPro events made under a shared account and unattributable | Partially effective — the pipeline control operates, with 11 documented bypasses (§11.10) |

The consequence is that the configuration population is tested item by item and the code population is tested by
testing the pipeline. For the 43 RevPro configuration change events, Brightline requested the tenant's
configuration audit log with the fields `change_id`, `object_type`, `object_name`, `field_changed`, `old_value`,
`new_value`, `changed_by`, `changed_datetime`, and traced each to a Jira ticket: the 17 events made under named
accounts all had an approved ticket; of the 26 made under `revpro_admin`, 21 had a ticket and 5 did not, and for
all 26 the approval could not be evaluated because the actor is unknown. The February 2025 ramp change comprised 5
of the 26. Chapter 12, §12.6 owns the configuration's substance; this chapter owns only whether the change was
authorized, and the answer is that it cannot be determined.

## 11.10 DevOps, CI/CD, and Auditing 3,100 Deployments

A population of 3,100 production deployments is not a sampling problem; it is a scoping and configuration
problem. Three moves make it auditable.

**Move 1: stratify and eliminate.** Most deployments cannot affect the financial statements. Establish which can,
by repository, and document the basis.

**Exhibit 11-15. FY2025 production deployment population (WP 8300-02).**

| Stratum | Deployments | Financially relevant | Basis for relevance | What it could affect |
| --- | --- | --- | --- | --- |
| Platform application code (`atlasflow-platform` and 14 service repositories) | 1,848 | 96 | Only the metering and entitlement services, identified from the repository list and corroborated by tracing the data lineage of the workflow-run counter | 4,200 of usage overage revenue; the 244,000-run overage on contract C-1 |
| Integration and interface code (`atlasflow-billing-sync`, connector configurations) | 214 | 214 | All touch interfaces I-4 and I-8 | 6,100 of self-serve revenue; account 1205 balance of 1,700; every Snowflake-sourced extract |
| Infrastructure as code (`terraform-prod`) | 806 | 41 | Changes to the metering RDS instance, the billing-pipeline IAM roles, and the Snowflake network policy | Data integrity and access for the above |
| Analytics models (`dbt-revops`) | 232 | 232 | Produce the RevOps datamart | ARR of 172,000 and NRR of 112% in MD&A (W-11) |
| **Total** | **3,100** | **583** | | |

**Move 2: test the automated preventive control by configuration, then prove nobody bypassed it.** The control is
GitHub branch protection on the `main` branch of each in-scope repository, requiring at least one approving review
from a designated code owner and a passing CircleCI pipeline before merge, with force-push and direct-push
disabled. Brightline inspected the protection settings for all 17 in-scope repositories and the audit log of
changes to those settings (4 changes in FY2025, all to add reviewers, all documented). That is a test of one, and
it is sufficient only because the settings-change log establishes the configuration could not have differed
earlier in the year.

Then query for bypasses rather than sampling for compliance. Using the GitHub API the team extracted all merges to
protected branches in the 17 repositories and filtered for `review_count = 0` or an administrative override in
`merged_by`. Result: 11 of 583 — the highest-value procedure in the domain, because it tests the whole population
for the specific condition the control exists to prevent, at the cost of one query.

**Move 3: sample the residual for what configuration cannot enforce.** Branch protection enforces that *someone*
approved; it does not enforce that the approver was independent of the author, that testing occurred, or that a
business owner authorized the change. Brightline selected 25 of the remaining 572 and tested three attributes: an
approving reviewer other than the author (25 of 25), evidence of automated test execution in the CircleCI record
(25 of 25), and a linked Jira ticket describing the business purpose (23 of 25; the 2 exceptions had commit
messages only and were both `terraform-prod` logging changes, evaluated as documentation deviations with no
financial statement consequence).

### 11.10.1 Emergency changes

Emergency changes are the designed exception to the control, and the design must include a compensating
requirement: post-hoc documentation and approval within a stated period. W-4 records 6 of 3,100 deployed without a
Jira ticket, documented after the fact for 4 and never for 2.

**Exhibit 11-16. FY2025 emergency deployments (WP 8300-05).**

| # | Date | Repository | Change | Ticket at deployment | Documentation created | Financially relevant | Auditor's procedure and result |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | Mar 14, 2025 | `atlasflow-billing-sync` | Retry logic in the I-4 Stripe posting job | None | Mar 19, 2025 (5 days) | Yes | Re-performed the daily cash-to-revenue reconciliation for March 14–21; agreed to the GL with no unexplained difference |
| 2 | May 2, 2025 | `atlasflow-metering` | Fix to a workflow-run counter overflow affecting accounts above 4.3 million monthly runs | None | May 6, 2025 (4 days) | Yes | Recomputed billed overage for the 11 affected accounts for March–May; identified 4,120 thousand under-counted runs, an under-billing of 49, below the clearly trivial threshold of 72 |
| 3 | Jun 27, 2025 | `atlasflow-platform` | Session timeout defect | None | **Never** | No | Read the diff; no effect on metering, entitlement, or billing data |
| 4 | Aug 11, 2025 | `terraform-prod` | RDS parameter group change to the metering database | None | Aug 14, 2025 (3 days) | Indirect | Confirmed no schema or data change; row counts before and after agreed |
| 5 | Oct 3, 2025 | `atlasflow-billing-sync` | Currency rounding in the I-4 job | None | **Never** | Yes | Re-performed the reconciliation for October; identified a 0.4 rounding difference, corrected by management |
| 6 | Nov 19, 2025 | `dbt-revops` | ARR model fix in the RevOps datamart | None | Nov 21, 2025 (2 days) | Yes | Effect is on MD&A metrics, not the statements; referred to Chapter 12 (W-11) |

Items 1 and 5 are the two undocumented Stripe Lambda modifications recorded as W-7, so W-4 and W-7 describe the
same changes from the change-management and interface perspectives. The deviation rate is 2 of 6 for the
documentation requirement and 6 of 6 for pre-approval. You test every emergency change rather than sampling because
the population is small and self-selected for risk: made under time pressure, by whoever was available, with the
pipeline's controls disabled.

## 11.11 Program Development and the September 2025 NetSuite Upgrade

Program development controls apply to implementations and major upgrades. There is usually one such project a
year, so the population is the project, not a sample, and the test is a checkpoint review.

**Exhibit 11-17. NetSuite release upgrade, September 2025 — project control checkpoints (WP 8320-01).**

| Checkpoint | Expected evidence | Obtained | Result |
| --- | --- | --- | --- |
| Project authorization | Approved project charter and budget | Charter approved by Tom Okafor's predecessor, June 2025 | Effective |
| Requirements and role design sign-off | Documented role-to-permission design approved by process owners | Role design matrix approved by Elena Vasquez, August 29, 2025 | Effective, but the matrix omitted the 12 integration accounts |
| Segregation-of-duties validation before go-live | Conflict analysis on the rebuilt roles | **Not performed** | Design deficiency — the roles were rebuilt with no conflict analysis, which is why the §11.7.2 analysis identified 14 conflicted users after the upgrade |
| User acceptance testing | Test scripts, results, and defect log | 84 scripts executed, 79 passed, 5 defects, all closed before go-live | Effective |
| Data conversion reconciliation | Pre- and post-conversion balance comparison | Trial balance at August 31, 2025 compared before and after; 62 accounts agreed to the cent | Effective |
| Go-live approval | Documented approval by the business owner | Approved September 19, 2025; go-live September 20, 2025 | Effective |
| Removal of legacy access at go-live | Legacy roles disabled at cutover | **11 users retained the legacy "Full Access" role until October 17, 2025 — 27 days** | Not effective (W-2) |
| Post-implementation review | Documented review of issues within 60 days | Not performed | Deficiency; firm methodology rather than a professional requirement |

The interesting work is quantifying W-2's exposure, because a 27-day window of over-entitlement is a control
deficiency whose magnitude is bounded by what the 11 users could and did do. The procedure, in order:

1. **Identify the 11.** Four in Revenue Accounting, three in Financial Reporting, two in FP&A, one in Sales
   Operations, and one offshore support contractor.
2. **Determine what the legacy role permitted that the new role did not.** Journal entry posting without a second
   approver in any subsidiary, chart-of-accounts modification, and approval workflow modification.
3. **Extract the activity.** The 11 posted 312 journal entries totaling $18,400 in absolute value during
   September 20 – October 17, 2025, a window that contains the entire September close.
4. **Filter to what the correct role would have blocked.** 47 entries totaling $2,900 — entries the users'
   intended roles could not have posted.
5. **Test all 47.** Every entry traced to supporting documentation and to a business purpose. Two, totaling $310,
   were both prepared and approved by the same FP&A analyst, both below the $250,000 second-approver threshold and
   therefore consistent with W-12 rather than with W-2. No misstatement identified.
6. **Conclude on both dimensions.** The control failed; the magnitude of misstatement that did occur is nil; the
   magnitude that could have occurred is the $2,900 of entries plus the unbounded chart-of-accounts and workflow
   modification capability. Chapter 14 owns whether that combination is a significant deficiency or a material
   weakness.

One consequence is easy to miss and expensive to discover late. When roles are rebuilt mid-year, a point-in-time
segregation-of-duties analysis at December 31 says nothing about the first eight months, and the evidence for the
earlier period is the pre-upgrade role export, which exists only if someone kept it. Ask for it before the project,
not after.

## 11.12 Computer Operations: Scheduling, Monitoring, Backup, and Recovery

Computer operations is the domain where scope discipline pays the largest dividend, because most of what an IT
department does under this heading has no financial reporting consequence. The controls that matter are the ones
over jobs that move or create accounting data.

**Exhibit 11-18. Financially relevant scheduled jobs, FY2025 (WP 8500-02).**

| Job | Interface | Schedule | Who can modify the schedule | Monitoring | FY2025 failures | Unresolved beyond one business day |
| --- | --- | --- | --- | --- | --- | --- |
| `ZBILL_TO_REV` | I-2 | Nightly 02:00 CT | 3 Zuora administrators | Reconciliation report worked by the Revenue Manager | 9 | 2 |
| `REVPRO_GL_POST` | I-3 | Monthly | 2 | Controller review before posting | 0 | 0 |
| `STRIPE_DAILY_JE` | I-4 | Daily 01:15 CT | 2 AWS engineers | PagerDuty alert | 17 | 1 |
| `COUPA_NS_SYNC` | I-7 | Nightly | 2 | Error queue | 4 | 0 |
| `FIVETRAN_SNOWFLAKE` | I-8 | Hourly | 4 | **None with financial escalation** | 63 | not tracked |
| `BANK_FEED` | I-9 | Daily | 2 | Unmatched-items report | 2 | 0 |
| **Total failures** | | | | | **95** | **3** |

Three procedures, and what each is capable of proving:

- **Restriction of scheduler access.** Inspect who can create, modify, or disable each job. The exposure is not
  that a job runs wrong but that a job is silently disabled and an interface stops posting — a completeness failure
  with no error message. Test by inspecting the job-definition change log: 7 changes in FY2025, all traced to a
  ticket.
- **Failure detection and resolution.** Obtain the failure log for the year and reconcile it to the incident
  tickets. The 17 `STRIPE_DAILY_JE` failures produced 17 PagerDuty alerts and 14 tickets; 3 alerts were
  acknowledged with no ticket. One failure on July 8, 2025 resulted in a duplicate posting of $41 that was
  identified by the daily reconciliation and corrected on July 11 — evidence that the detective control works,
  which is worth as much as the deficiency is worth.
- **Completeness of the failure log itself.** The log is IPE. Corroborate it independently: for
  `STRIPE_DAILY_JE`, count the days in FY2025 on which no summary journal posted to NetSuite. Expected 365
  postings; found 361 postings and 4 days with none, each matching a logged failure with a catch-up posting the
  next day. The 13 remaining logged failures were partial and self-recovered. This is the procedure that turns a
  client-provided failure count into evidence.

**Backup and recovery (W-14).** AtlasFlow's documented recovery point objective is 1 hour and its recovery time
objective is 8 hours for the production platform. One restoration test was performed, on June 12, 2025, on the
metering database snapshot. It failed: 3 of 14 tables restored with row-count differences, the metering event
table short 41,200 rows of 8.4 million (0.49%), and the restoration completed in 11.5 hours against the 8-hour
objective. The retest was deferred twice and completed successfully on January 22, 2026 — after the balance sheet
date, which means it is not evidence about FY2025 operating effectiveness.

Be precise about what this costs the audit, because the honest answer is unusual for an ITGC. No FY2025 loss event
occurred, and the metering data supporting $4,200 of overage revenue was available and was tested, so no assertion
in the FY2025 financial statements is unsupported because of W-14. Severity turns entirely on likelihood, which is
why many firms scope backup and restoration in only where a recovery failure would affect the completeness of
recorded transactions, and document that decision explicitly. Say which position your file takes. Brightline's was
that the control is in scope because the metering event table is the only record of the workflow runs generating
overage revenue, and that the deficiency is individually a deficiency rather than a significant deficiency.

## 11.13 Service Organizations and SOC 1 Reports

### 11.13.1 What a SOC 1 report is, and what it is not

A **service organization** performs processing that is part of the user entity's information system. A **SOC 1
report** is a service auditor's examination report under AT-C 320 on the design of that organization's controls
(Type 1) or on their design and operating effectiveness over a period (Type 2). AS 2601 and AU-C 402 govern its
use. Three properties determine what it can do for you.

- **It is evidence about the service organization's controls, not about yours.** It never covers who at AtlasFlow
  was given access to the tenant, who approved the configuration, or whether AtlasFlow reviewed the interface
  error report. Those are AtlasFlow's controls, and a SOC 1 is not evidence about them.
- **Only a Type 2 report supports reliance on operating effectiveness.** A Type 1 supports design only, and
  therefore cannot support control reliance in an ICFR audit.
- **A SOC 1 is not a scope substitute.** Obtaining reports for eight providers does not make eight applications
  in scope or out. Scope is decided in §11.3 by reliance; the report is how you get evidence for the layers you do
  not control.

### 11.13.2 Evaluating the reports on hand

Reading a SOC 1 means reading five things in this order: the service auditor's opinion; the scope statement (which
systems, which locations, which control objectives); the period covered; the description of tests and results,
including every deviation; and the complementary user entity controls. Everything else is background.

**Exhibit 11-19. Evaluation of the eight SOC 1 Type 2 reports on hand (WP 8600-01).**

| Provider | Period covered | FY2025 days covered | Gap days to 12/31/2025 | Opinion | Deviations | Bridge letter | Reliance conclusion |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Zuora (Billing and Revenue) | Oct 1, 2024 – Sep 30, 2025 | 273 | 92 | Unqualified | 2 of 25 change tickets lacked approval evidence | **Not obtained (W-9)** | Reliance limited to January 1 – September 30, 2025; gap period unaddressed |
| Oracle NetSuite | Nov 1, 2024 – Oct 31, 2025 | 304 | 61 | Unqualified | None | Obtained January 16, 2026 | Full-year reliance supported |
| AWS | Oct 1, 2024 – Sep 30, 2025 | 273 | 92 | Unqualified | None | Obtained | Full-year reliance supported |
| ADP | Jan 1, 2025 – Sep 30, 2025 | 273 | 92 | Unqualified | None | Obtained | Full-year reliance supported |
| Deel | Oct 1, 2024 – Sep 30, 2025 | 273 | 92 | **Qualified** as to one control objective related to change management | 1 qualification | **Not obtained (W-9)** | No reliance on change management; substantive response required (§11.13.6) |
| Carta | Oct 1, 2024 – Sep 30, 2025 | 273 | 92 | Unqualified | None | Obtained | Full-year reliance supported |
| Stripe | Jan 1, 2025 – Dec 31, 2025 | 365 | 0 | Unqualified | None | Not required | Full-year reliance supported |
| Coupa | Jul 1, 2024 – Jun 30, 2025 | 181 | **184** | Unqualified | 2 deviations in access recertification | Obtained | Bridge letter alone is insufficient for a 184-day gap; see below |

Each row's "FY2025 days covered" plus its gap days equals 365, which is the arithmetic check that catches the
mistake of reading a report period as though it were a fiscal year. Two conclusions in the exhibit deserve their
reasoning stated.

**Coupa's 184-day gap.** A bridge letter is management's written representation that nothing changed. It is not
audit evidence about operating effectiveness; it is a representation, and its persuasiveness decays with the length
of the period it purports to bridge. Practice varies on the tolerable gap, and the defensible range is roughly 60
to 90 days for a report on which meaningful reliance is placed, with some firms setting a bright line at three
months and others requiring an assessment in every case. A 184-day gap — half the fiscal year — is outside that
range under any policy. Brightline's response was to obtain the bridge letter, and additionally to test the two
Coupa-related automated controls directly for the July–December period: the three-way match tolerance
configuration (inspected, unchanged from the June screenshot) and the approval hierarchy (re-performed for 15
invoices spanning September to December). That converts an unbridgeable gap into direct evidence.

**Coupa's 2 access-recertification deviations.** Deviations in the service auditor's testing are not
automatically your problem. Evaluate three things: whether the control objective is one you rely on, whether the
deviation's nature could affect your relied-upon processing, and what the service organization's management
response says. Coupa's access recertification affects who at Coupa can reach the AtlasFlow tenant; AtlasFlow relies
on the three-way match configuration and the approval hierarchy, which the report tested without exception.
Brightline concluded the deviations did not affect its reliance and documented that conclusion rather than leaving
the deviation unaddressed — the second most common SOC 1 file defect after failing to read the CUECs at all.

### 11.13.3 The gap period

The gap period is the interval between the end of the service auditor's reporting period and the entity's balance
sheet date. Four responses are available, in descending order of strength:

1. **Obtain a report that covers the full period**, if a second report or an extended period is available.
2. **Test the user entity's own controls that would detect a service organization failure** — for Zuora, the I-2
   reconciliation and the I-3 journal review, both of which AtlasFlow performs monthly and Brightline tested for
   October, November, and December.
3. **Obtain a bridge letter** covering the gap, ideally stating that the controls described in the report continued
   to operate, that no changes were made, and that no control failures or security incidents occurred.
4. **Perform procedures at the service organization**, which is rarely practical with a large vendor.

For the two providers where no bridge letter was obtained (W-9), the responses differ because the reliance
differs. For Zuora, Brightline relied on option 2: the monthly reconciliations for the 92-day gap period were
tested and no unexplained differences arose, which provides evidence that Zuora's processing continued to operate
as described. For Deel, option 2 was unavailable at the necessary precision because AtlasFlow's payroll review
control is a variance review against the prior month, which would not detect a systematic error introduced by a
change-management failure. Deel therefore required substantive testing regardless of the bridge letter.

### 11.13.4 Complementary user entity controls

A **complementary user entity control** is a control the service organization assumes the user entity operates,
without which the service organization's controls cannot achieve the stated control objective. CUECs are listed in
the report, usually in a section readers skip. W-10 records that AtlasFlow never mapped them.

**Exhibit 11-20. CUEC mapping for the AWS and Zuora SOC 1 reports (WP 8600-04).**

| # | Report | CUEC (summarized) | AtlasFlow control | Owner | Tested at | Conclusion |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | AWS | User entity manages creation and removal of its own IAM users and roles | C-ITGC-01 / 03 as applied to AWS | Ray Sandoval | WP 8200-05 | Mapped; control not effective (W-5) |
| 2 | AWS | User entity enables MFA for all IAM users with console access | Okta MFA policy — does not extend to AWS IAM | Ray Sandoval | §11.7.4 | **Unmapped and failing — 7 of 34 without MFA** |
| 3 | AWS | User entity configures security groups and network access controls appropriately | Terraform-managed security groups with peer review | CTO organization | WP 8300-02 | Mapped; effective |
| 4 | AWS | User entity selects backup frequency and retention and tests restoration | Backup policy and annual restoration test | Ray Sandoval | §11.12 | Mapped; not effective (W-14) |
| 5 | AWS | User entity reviews CloudTrail logs for unauthorized activity | **None** | — | — | **Unmapped; no control exists** |
| 6 | AWS | User entity manages its own encryption keys and key rotation | KMS key policy; annual rotation enabled | CTO organization | Inspection | Mapped; effective |
| 7 | Zuora | User entity administers its own tenant users and roles | C-ITGC-01 / 02 / 03 | Ray Sandoval | WP 8200-05 | Mapped; not effective (W-1, W-5) |
| 8 | Zuora | User entity periodically reviews the list of users with privileged access | C-ITGC-04 access review | Daniel Kim | §11.8 | Mapped; not effective (W-3) — and the review omitted privileged accounts |
| 9 | Zuora | User entity authorizes and tests configuration changes before production | Configuration change approval | Daniel Kim | §11.9 | Mapped; not effective — 26 of 43 unattributable |
| 10 | Zuora | User entity reviews interface error and exception reports | I-2 exception clearing by the Revenue Manager | Jordan Pike | Chapter 12 | Mapped; effective (Chapter 12) |
| 11 | Zuora | User entity ensures the accuracy and completeness of data it submits | I-1 field-mapping and error queue review | Billing Analyst | Chapter 12 | Mapped; effective (Chapter 12) |
| 12 | Zuora | User entity restricts and manages API credentials | Key management for `svc_revpro_integration` | Ray Sandoval | §11.7.1 | Mapped; deficient — key not rotated, no documented owner |
| | | **Total CUECs identified: 12; mapped to an AtlasFlow control: 10; unmapped: 2; mapped but not effective: 6** | | | | |

The arithmetic matters: 10 mapped plus 2 unmapped equals 12, and of the 10 mapped, 6 relied on AtlasFlow controls
that Brightline concluded were not effective. That is the sentence that converts W-10 from a documentation
observation into an audit consequence. Where a CUEC is unmapped or is mapped to an ineffective control, the service
organization's control objective is not achieved *for AtlasFlow*, notwithstanding the unqualified opinion. The
report's clean opinion is conditional on the CUECs, and the condition is not satisfied.

### 11.13.5 Subservice organizations, carve-out, and inclusive

A **subservice organization** is a service organization used by another service organization. Zuora hosts on AWS;
Zuora's report therefore has to say something about AWS. Two methods exist:

- **Carve-out method.** The subservice organization's controls are excluded from the description and from the
  service auditor's opinion, and the report identifies the CUECs the subservice organization is assumed to satisfy.
  You are left with a hole, which you fill by obtaining the subservice organization's own report.
- **Inclusive method.** The subservice organization's relevant controls are included in the description and in the
  scope of the opinion. There is no hole.

Zuora's report uses the carve-out method for AWS. That is why AtlasFlow's separate AWS SOC 1 is doing double duty:
it covers the layers beneath AtlasFlow's own platform, and it fills the carve-out in Zuora's report. Had AtlasFlow
not hosted on AWS itself, the team would have had to obtain the AWS report solely to complete the Zuora chain, and
it is common to find that nobody did. The procedure is short: for each SOC 1, read the subservice organization
paragraph, note the method, and for every carve-out either obtain the subservice report or document why the
carved-out controls are not relevant to your reliance. AtlasFlow's chain has three carve-outs — AWS in Zuora's
report, AWS in Carta's report, and a payment processor in Deel's report. The first two are covered by the AWS
report on hand. The third is not, and Brightline documented that the carved-out processor affects the movement of
cash rather than the measurement of payroll expense, and that cash movement is tested substantively through the
bank reconciliations (Chapter 8).

### 11.13.6 A qualified report: Deel

A qualification is not a reason to stop reading; it is a reason to read one section closely. Deel's report is
qualified as to one control objective related to change management. The analysis has four steps.

1. **Determine what the qualification removes.** Reliance on Deel's controls over changes to its payroll
   calculation logic. Everything else in the report — access, processing, output review — remains supported by the
   unqualified portion of the opinion.
2. **Determine what depends on the removed reliance.** AtlasFlow's UK, Australia, and India personnel cost of
   $19,000 for FY2025 (extension), against performance materiality of $940. A systematic calculation error of 5%
   in any one entity would exceed the clearly trivial threshold; in the UK alone it would exceed performance
   materiality. Reliance on calculation accuracy cannot be assumed.
3. **Design the substantive response.** Brightline (a) reconciled all 36 monthly payroll registers to the general
   ledger by entity, obtaining an aggregate unexplained difference of $14, below the $72 clearly trivial threshold;
   (b) recomputed gross-to-net pay for 15 employees, 5 in each entity, from the employment contract, the statutory
   rate tables, and the register, agreeing 15 of 15; and (c) recomputed the FY2025 movement in accrued
   compensation for the three entities and agreed it to the accrual in account 2100.
4. **Consider whether the qualification implies anything about the user entity.** It does. If Deel's change
   management is unreliable, the CUEC requiring AtlasFlow to review the payroll register for unexpected changes
   becomes load-bearing. Brightline tested that review for 6 of the 36 register cycles and found evidence of
   variance investigation in 4 and a bare sign-off in 2.

## 11.14 Benchmarking

**Benchmarking** is the practice of carrying forward evidence about an automated application control from a prior
period, on the reasoning that a purely automated control that has not changed will operate consistently. AS 2201's
appendix addresses it. It is available only if all of the following hold:

1. The control is entirely automated, with no manual element and no judgment.
2. General IT controls over program change, access to programs, and computer operations are effective for the
   intervening period.
3. The auditor has established a baseline by testing the control's operation in a prior period.
4. The auditor determines the control has not changed, ordinarily by testing the program-change population for
   the specific object.
5. The risk associated with the control does not require annual testing.

AtlasFlow fails on two independent grounds, and the second is the more instructive.

Condition 2 fails outright: the program change and logical access controls over Zuora Revenue are not effective,
so 26 of 43 configuration change events cannot be attributed to a person and there is no basis for concluding the
27 rules did not change. Even for the 22 rules unchanged since FY2024 by management's own log, the log is the
output of the failed control.

Condition 3 fails for a reason that applies to every first-year ICFR audit: **there is no baseline.** FY2025 is
AtlasFlow's first integrated audit. Brightline did not test the operating effectiveness of the RevPro
configuration in FY2024 because it had no reason to; benchmarking carries forward a test that was never performed.
This is worth stating in the planning file of any first-year 404(b) engagement, because the efficiency assumption
that automated controls are cheap to test relies on benchmarking in later years and is simply unavailable in
year one. The consequence at AtlasFlow: 0 of the 27 configuration rules were eligible for benchmarking, and all 27
required current-year testing, which Chapter 12 performs.

## 11.15 Evaluating ITGC Deficiencies: The Pervasive Effect

An ITGC deficiency has no direct effect on the financial statements. Its effect is transmitted: it removes the
basis for relying on something else, and the audit has to buy that evidence somewhere more expensive. The
evaluation therefore has two outputs, and a file that produces only the first is incomplete.

The first output is the severity conclusion, which Chapter 14 owns. The second is the change to the audit plan,
which is Chapter 11's, and which must be specific enough that someone can execute it.

**Exhibit 11-21. ITGC deficiencies and their consequences for the FY2025 plan (WP 8400-02, prepared for the
Chapter 14 aggregation).**

| Ref | Deficiency | Reliance removed (Exhibit 11-1) | Change to the plan | Incremental hours |
| --- | --- | --- | --- | --- |
| W-1, W-6 | Unattributable and shared administrative access to Zuora Revenue | R-1, R-3, R-4, R-9 | Revenue recomputed from contract data rather than tested by exception; all 91 manual schedule adjustments tested; RevPro reports reconciled to a source outside RevPro | 255 |
| W-2 | 11 users retained legacy Full Access for 27 days | R-6 for the September 20 – October 17 window | All 47 entries the correct role would have blocked tested; pre-upgrade role design evidence requested | 34 |
| W-3 | Access review annual rather than quarterly, population incomplete | The detective backstop for R-2, R-6, and all access controls | No direct substantive change; removes the argument that provisioning deviations were caught | 0 |
| W-4, W-7 | Emergency and undocumented changes to interface code | R-12 and the I-4 posting | Reconciliation re-performed for the affected periods; overage recomputed for 11 accounts | 46 |
| W-5 | Terminated access removal averaging 6.2 days | R-2, R-6 | Post-separation activity logs obtained for the 3 over-30-day exceptions; occurrence testing extended for Q4 order forms | 28 |
| W-9 | Missing bridge letters for Zuora and Deel | Service organization reliance for the 92-day gap | I-2 and I-3 reconciliations tested for October–December; Deel payroll tested substantively | 52 |
| W-10 | CUECs not mapped | Two AWS control objectives | CloudTrail activity reviewed directly for the metering account; MFA gap quantified | 18 |
| W-11 | RevOps datamart unreconciled | R-14 | Chapter 12 owns; ARR and NRR recomputed from source for the MD&A consistency read | referred |
| W-12, W-13 | Journal entry approval threshold and preparer/poster conflict | R-6 | Chapter 16's journal entry criteria expanded to include all 214 conflicted-user entries | referred |
| W-14 | Failed restoration test | None for FY2025 | No change; documented as having no assertion-level consequence | 0 |
| W-8 | Consolidation workbook end-user computing | The consolidation | Chapter 12 owns; all 27 top-side entries tested | referred |
| | **Total incremental hours attributed to ITGC deficiencies** | | | **433** |

Three principles govern the conversion.

**Reliance is lost at the level of the application, for the period affected.** W-2's window is 27 days, so the
response is bounded to 27 days. W-1 runs the whole year, so the response does. Writing "we cannot rely on
automated controls" without a period is both wrong and unaffordable.

**A pervasive ITGC deficiency removes the "test of one" for automated controls.** An automated control can be
tested with a single item only because it is expected to operate identically every time — and the basis for that
expectation is program change and access control. Without them, an automated control has to be tested like a
manual control, at a frequency-based sample size, or the automated processing has to be re-performed on a
population. Chapter 12, §12.7 develops the alternatives; Chapter 14 owns the sample sizes.

**IPE reliability is affected differently from automated control reliability, and more broadly.** Every report out
of the affected application becomes information whose source system's integrity is unproven. The response is not
more testing of the report's arithmetic; it is reconciling the report to a population outside the affected system.
For AtlasFlow the outside populations are the Zuora Billing invoice register, the Salesforce order forms, and cash
receipts — none of which passes through RevPro.

## 11.16 Documenting the ITGC Conclusion

AS 1215 requires documentation from which an experienced auditor with no previous connection to the engagement can
understand the work performed and the conclusions reached. For ITGCs that means the file must answer four
questions in a form a reviewer can trace, and most ITGC files answer only the third.

**Exhibit 11-22. The ITGC documentation package (WP 8100 through 8600).**

| WP | Content | The question it answers |
| --- | --- | --- |
| 8100-01 | IT scoping memo, including Exhibits 11-4 and 11-5 and the inventory completeness reconciliation | Which applications and layers are in scope, and why each of the 20 items is in or out |
| 8110-01 | Reliance inventory (Exhibit 11-1) and the risks-arising-from-IT mapping (Exhibit 11-7) | What depends on the ITGCs, and which risk each control addresses |
| 8200 series | Logical access testing: user listing completeness, provisioning, modification, de-provisioning, the 284-event population | Did access controls operate |
| 8210 series | Privileged access, segregation of duties, authentication, the access review | Who can override the controls, and who checks |
| 8300 series | Program change: configuration changes, the deployment population, emergency changes | Was every production change authorized |
| 8320 series | Program development: the NetSuite upgrade checkpoints | Was the project controlled |
| 8500 series | Computer operations: job inventory, failures, backup and restoration | Did processing run and can data be recovered |
| 8600 series | Service organizations: report evaluation, gap periods, CUEC mapping, subservice chains | What did the service auditors' reports support, and where do they stop |
| 8400-02 | Deficiency schedule with the consequence mapping (Exhibit 11-21) | What did the deficiencies cost the audit |

Four drafting rules that reviewers enforce and that save rework.

1. **Every control tested must trace to a reliance item.** If it does not, delete the test or document the reason
   for testing it (for example, that management asserted it as part of its Section 404(a) assessment and you are
   evaluating management's conclusion). An untraceable control is either scope creep or an undocumented dependency.
2. **Every population must have its completeness proved in the workpaper that uses it**, not by cross-reference to
   a general assertion. The 284-event build in Exhibit 11-8 is the model.
3. **Every conclusion must be stated at the domain and application level.** "ITGCs are effective" is not a
   conclusion. "Logical access controls over NetSuite were not effective for the period January 1 – December 31,
   2025 because de-provisioning deviated in 210 of 284 instances and the access review was not performed at the
   documented frequency" is.
4. **Tool-generated evidence is IPE.** Vanta continuously monitors and produces attractive screenshots. A Vanta
   screenshot showing "MFA enforced: pass" is a report produced by a tool whose scope, configuration, and coverage
   you have not tested. Brightline declined to use Vanta output as primary evidence and instead used it as a
   corroborative source and as a way to identify populations, obtaining the underlying Okta and AWS configuration
   exports directly. Where a team does intend to rely on a compliance-automation tool's output, the tool's own
   coverage configuration has to be tested — which is a fifteenth application nobody scoped.

## Step-by-Step Walkthrough: Scoping the FY2025 IT Environment and Testing NetSuite Access Provisioning and Termination

Objective: reach a documented scope conclusion for the FY2025 IT environment, then test NetSuite user access
provisioning and de-provisioning including the completeness of both populations. Workpapers WP 8100-01 and
WP 8200-01 through WP 8200-08. Performed by Ben Osei (IT audit senior), reviewed by Farrah Nazari (IT audit senior
manager). Interim testing October 31, 2025; roll-forward to December 31, 2025.

**Step 1.** Request management's application inventory and the three corroborating extracts: the Okta application
catalog, the Vanta system inventory, and a Coupa vendor-spend query for FY2025 disbursements coded to software,
subscriptions, and IT services. Compare the union (51 distinct systems) to management's 20. You are looking for
systems management omitted. Result: 2 omissions (DocuSign; a decommissioned Workato tenant). If the union produces
nothing new, corroborate by a different route — interview the CTO about systems retired during the year — before
concluding the inventory is complete.

**Step 2.** For each of the 22 systems, ask a single question: does any item in the reliance inventory (Exhibit
11-1) run through it? Record the answer with the reliance reference. Do not ask whether the system is "important."

**Step 3.** For each system where the answer is yes, determine the domains in scope. Stripe is in scope for
logical access and for the change management over the I-4 Lambda, and out of scope for program development.
Document scope at the domain level (Exhibit 11-4).

**Step 4.** For each in-scope application, identify the four IT layers and who operates each (Exhibit 11-5). The
output tells you which layers require a service auditor's report. Unexpected result: if the client claims to
operate the database layer of a vendor-hosted application, it usually means a replicated copy exists somewhere —
find it, because it is probably Snowflake.

**Step 5.** For each layer operated by a service organization, list the report required and check it against the
reports on hand. Result: 8 reports on hand covering 8 providers; DocuSign has a SOC 2 rather than a SOC 1, which
supports no ICFR reliance, so the conclusion for DocuSign is logical access at the entity only, with the integrity
of the executed document supported by the tamper-evident certificate on each envelope rather than by a report.

**Step 6.** Write the scoping conclusion for all 22 items, one row each, with a rationale. Have it reviewed before
any testing begins. A scope reopened in January costs three times what it costs in September.

**Step 7.** Obtain management's ITGC control matrix and compare it to the control set your scope requires.
Result: management documented 34 ITGCs; Brightline's required set was 41. The 7 gaps were: authorization of vendor
data-fix requests; removal of legacy access at implementation go-live; ownership and rotation of API credentials;
review of direct write activity in Snowflake RevOps schemas; monitoring of break-glass account use; the emergency
change post-hoc documentation requirement; and CUEC ownership. Each gap is a candidate design deficiency, and each
must be either tested as an undocumented control or reported as absent.

**Step 8.** Request the NetSuite user listing. Specify the fields rather than accepting a spreadsheet: `internal_id`,
`login_name`, `email`, `full_name`, `employee_record_id`, `role_name`, `subsidiary_access`, `status`,
`date_created`, `last_login`, `password_last_changed`, `sso_required_flag`, `two_factor_required_flag`,
`is_integration_role`. Ask how it was produced, and obtain the saved-search definition, not just its output.

**Exhibit 11-23. NetSuite user listing extract as received (WP 8200-01), first five rows, illustrative.**

```text
internal_id  login_name            full_name        employee_record_id  role_name              subsidiary_access  status    date_created  last_login   sso_required  2fa_required
------------ --------------------- ---------------- ------------------- ---------------------- ------------------ --------- ------------- ------------ ------------ ------------
1042         evasquez@atlasflow    Elena Vasquez    E-00114             Administrator          All                Active    2021-06-14    2025-12-31   Y            Y
1187         jpike@atlasflow       Jordan Pike      E-00298             Revenue Manager        US, UK             Active    2022-09-02    2025-12-30   Y            Y
1301         akhan@atlasflow       Amina Khan        E-00417            A/R Clerk              US                 Active    2023-03-20    2025-12-29   Y            Y
1455         svc_revpro_i3         (integration)    (none)              I-3 Integration Role   All                Active    2023-05-11    2025-12-31   N            N
1512         tbrandt@atlasflow     Tomas Brandt     E-00611             Journal Approver       US                 Inactive  2024-01-08    2025-09-04   Y            Y
```

**Step 9.** Test the completeness and accuracy of the listing by three independent routes, because the listing is
IPE and every subsequent conclusion rests on it. (a) Reconcile the count of enabled accounts to the Okta NetSuite
application assignment report: 202 federated accounts agreed. (b) Agree the total account count to the NetSuite
subscription invoice's licensed user count: 214 against 225 licensed, a difference explained by 11 unused
licenses. (c) Recompute the listing from the account-creation and account-status audit trail: 187 accounts at
January 1, 2025 plus 58 created less 31 disabled equals 214 at December 31, 2025. Unexpected result: if route (c)
does not agree, the difference is either accounts created outside the audit trail (impossible in NetSuite, so
suspect the extract's date filter) or accounts deleted rather than disabled, which destroys evidence and is itself
a finding.

**Step 10.** Stratify the 214: 187 named employee accounts, 9 contractor accounts, 12 integration accounts, 6
Administrator accounts. Confirm the strata sum to 214. Identify the two testing populations: 58 provisioning events
and 41 role-modification events for the year, both taken from the audit trail rather than from the Jira queue,
because the Jira queue is the control's output and cannot prove its own completeness.

**Step 11.** Build the termination population from outside IT, following Exhibit 11-8: 268 separations per ADP and
Deel, less 7 transfers, plus 19 contractors and 4 former Kestrel employees, equals 284 access-removal events.
Corroborate three ways: the headcount roll-forward (731 + 349 − 268 = 812, agreeing to the disclosed headcount),
the Okta deactivation log (291 = 284 + 7), and the final-paycheck report (268). Unexpected result: any unreconciled
difference is an omitted category; find it before proceeding, because a de-provisioning test on an incomplete
population proves nothing.

**Step 12.** Determine which of the 284 held NetSuite access at separation by joining the termination population
to the NetSuite user listing on `employee_record_id`, and for the 23 non-payroll individuals on `email`. Result:
46 of 284. Reconcile the join's failures: 3 records failed to match on either key and were resolved manually
(two name changes and one contractor with a personal email address). Never discard unmatched records silently; they
are the population the join was designed to lose.

**Step 13.** For all 46, obtain the NetSuite account-status change timestamp from the audit trail and compute days
from the separation effective date. Compare to the documented 24-hour service level. Result: 12 within 1 day, 9 at
2–3 days, 14 at 4–7 days, 8 at 8–14 days, 3 at 15–30 days, 0 beyond 30 days; 249 aggregate days over 46 events, an
average of 5.4 days, and a deviation rate of 34 of 46 (73.9%). Place tick mark (c) against each deviation.

**Step 14.** Investigate every deviation for activity during the exposure window. Obtain `last_login` and, where a
login post-dates separation, the user's transaction and system-note activity. Result: 2 of the 34 show a
post-separation login, both on the separation date itself before the close of business, with no transactions
posted. Unexpected result: a post-separation transaction requires you to quantify it, evaluate it under AS 2401,
and escalate to the engagement partner the same day.

**Step 15.** Extend the same test to the full 284 across all applications, using the Okta deactivation timestamp
and, for non-federated access, each application's own status change. Result: Exhibit 11-9 — 1,761 aggregate days
over 284 events, 6.2 days average, 3 exceptions beyond 30 days, all in Salesforce because local password login
remained enabled. Obtain post-separation login and field-history evidence for those 3.

**Step 16.** Select 25 of the 58 provisioning events for testing (Chapter 14, §14.6 owns the sizing; the sample was
drawn using a random start and a fixed interval over the audit-trail-ordered population). For each, obtain the Jira
ticket and test four attributes: a ticket exists; the requester's manager approved; the data owner approved; and
the role recorded in the NetSuite audit trail matches the role approved. Result: 25 tickets exist; 25 manager
approvals; 25 data-owner approvals; 24 role matches. The one deviation is an account created September 22, 2025
whose data-owner approval is time-stamped September 25, 2025 — approval three days after provisioning.

**Step 17.** Evaluate the Step 16 deviation on its merits rather than by its size. The control is preventive: its
objective is that access is authorized *before* it is granted. An approval recorded after the fact does not achieve
that objective, so it is a deviation and not a documentation matter. One deviation in 25 for a control tested at a
sample size premised on a low expected deviation rate ends the test; the control cannot be relied upon at the
planned level of assurance. Record it as an extension to the continuing case's weakness list, and note that
expanding the sample is not a remedy — Chapter 14, §14.10 explains why.

**Step 18.** Test the 41 modification events. Select 15 and test that the entitlement change was approved by the
data owner before the change and that the prior entitlement was removed rather than added to. Result: 15 of 15
approved; 3 of 15 were additive, leaving the prior role in place, of which 1 created a new segregation-of-duties
conflict (the FP&A analyst holding "Journal Approver" identified in §11.8). Additive role changes are the
mechanism by which conflicts accumulate invisibly, and the attribute that detects them is removal of the prior
role, which most test designs omit.

**Step 19.** Test privileged access and segregation of duties as of December 31, 2025 (Exhibits 11-10 and 11-11),
then address the mid-year role rebuild: request the pre-upgrade role export to support the January–September
period. Result: no export was retained, so the design of the roles that operated for the first 263 days of FY2025
cannot be evaluated directly. Compensating procedure: reconstruct role membership from the NetSuite role-assignment
audit trail, which retains the assignment history even though the role definitions were replaced, and evaluate
conflicts using the pre-upgrade permission definitions preserved in the August 29, 2025 role design matrix.

**Step 20.** Evaluate the results by control, state the conclusion at the domain and application level, and map
each conclusion to the reliance it removes (Exhibit 11-21). Then answer the roll-forward question: because the
controls tested at the October 31 interim date were not effective, there is nothing to roll forward, and the
December 31 procedures are extensions of the original test rather than roll-forward procedures. Had the controls
been effective at interim, the roll-forward would have consisted of inquiry, an update of the population for
November and December (14 provisioning events, 61 separations), and testing of a proportionate number of items —
which is what makes early interim testing worth doing and what an ineffective interim conclusion forfeits.

Tick mark legend for WP 8200-01 through WP 8200-08:
(a) Report parameters and query definition inspected; report regenerated in the auditor's presence.
(b) Population completeness proved by an independent method; see WP 8200-04.
(c) Control deviation; investigated at WP 8200-06.
(d) Agreed without exception to the underlying system record, not to a client-prepared schedule.

## Extended Case Study: The Shared `revpro_admin` Account

### Background

Zuora Revenue is AtlasFlow's revenue subledger. Its 27 configuration rules perform performance obligation
identification, standalone selling price allocation, revenue scheduling, and modification treatment for the whole
of the $135,800 subscription revenue balance and the $78,200 contract liability. Brightline's FY2025 plan relied on
those rules as automated controls (reliance items R-1, R-3, R-4, and R-9) and, on that basis, sized substantive
revenue testing at 45 contract selections.

Internal audit's July 2025 readiness assessment identified four local administrator accounts in Zuora Revenue that
do not authenticate through Okta. One of them, `revpro_admin`, is a shared account whose password is stored in a
shared vault entry accessible to six people.

### The Facts

The six vault holders were Daniel Kim (VP, Revenue Accounting), Jordan Pike (Revenue Manager), two RevPro
consultants from Larkspur Consulting (the implementation partner), Ray Sandoval (Director, IT and Information
Security), and Tobias Lund, a revenue accountant who resigned June 13, 2025 and whose vault entitlement was not
removed until October 2, 2025 — 111 days after separation.

The other three local accounts were `d.kim.local` (a named account for Daniel Kim), `svc_revpro_integration` (the
service account for interfaces I-2 and I-3, with no documented owner and no key rotation since the FY2023
implementation), and `zuora_support_ta` (a Zuora technical account manager's account).

FY2025 activity attributable to `revpro_admin`:

| Activity | Count | Notes |
| --- | --- | --- |
| Login sessions | 412 | From 5 distinct source IP ranges, 2 of which resolve to Larkspur Consulting |
| Configuration change events | 26 of the 43 logged in FY2025 | Includes 5 of the events comprising the February 2025 ramp configuration change |
| Configuration change events with a Jira ticket | 21 of 26 | 5 had no ticket |
| Manual revenue-schedule adjustments | 91, affecting 74 revenue contracts | Gross absolute value $3,180 |
| Multi-factor authentication | Not enforced | Local accounts bypass the Okta policy |
| Password last changed | March 2023 | 33 months before year end |

Management's position, stated by Daniel Kim and supported by Tom Okafor in a November 2025 meeting, was that the
shared account is an operational necessity because Larkspur's consultants require administrative access during
configuration work, that no unauthorized change occurred, and that five existing controls compensate.

### What the Engagement Team Did

Farrah Nazari's team performed five procedures.

1. **Established the population of activity.** Requested the tenant's configuration audit log and revenue-schedule
   adjustment log for the full year with the fields `event_id`, `event_type`, `object_name`, `field_changed`,
   `old_value`, `new_value`, `contract_id`, `amount_effect`, `performed_by`, `performed_datetime`, `source_ip`.
   Proved completeness by reconciling the log's monthly event counts to the tenant's login session count and by
   confirming with Zuora support that the log cannot be purged by a tenant administrator.
2. **Tested all 91 manual schedule adjustments.** 89 traced to an approved Jira ticket or to a documented item on
   the monthly I-2 exception report. 2, totaling $76, had no documentation; both were correcting entries whose
   effect Brightline recomputed independently from the underlying contracts and found accurate. No misstatement.
3. **Tested attribution.** For each of the 26 configuration change events and 91 adjustments made under
   `revpro_admin`, attempted to identify the individual. The log records only the account. Source IP narrowed 34 of
   the 117 events to Larkspur's ranges; the remaining 83 could have been performed by any of the six vault holders,
   including Tobias Lund during the 111 days after his separation.
4. **Evaluated each asserted compensating control** against three criteria: precision sufficient to detect the
   misstatement the failed control was designed to prevent; independence from the deficiency; and having itself
   been tested and found effective.
5. **Quantified the substantive consequence** and re-planned revenue testing.

### Analysis

**Exhibit 11-24. Evaluation of the five asserted compensating controls (WP 8220-07).**

| Asserted control | Precision | Independence | Tested and effective | Conclusion |
| --- | --- | --- | --- | --- |
| Monthly RevPro-to-GL reconciliation performed by Jordan Pike, reviewed by Elena Vasquez | **Fails.** The reconciliation ties RevPro's output to the journal RevPro generated. A configuration change alters both sides identically and reconciles perfectly | **Fails.** Jordan Pike is one of the six vault holders | Operating effectively as designed | Not a compensating control |
| Controller's review and approval of the monthly I-3 revenue journal | **Fails.** The journal is compared to the RevPro Revenue Contract Summary — the same source | **Fails.** Elena Vasquez holds interface-mapping access (W-13) | Operating effectively as designed | Not a compensating control |
| Zuora's unqualified SOC 1 Type 2 | **Fails on relevance.** Covers Zuora's controls, not AtlasFlow's tenant user administration, which is a CUEC (W-10, item 7) | n/a | Report evaluated at WP 8600-01 | Not a compensating control |
| Vanta alert on RevPro administrative logins | **Fails.** Fires on all 412 sessions; detects authentication, not the appropriateness of the action | Partially independent | **Not tested; no alert had a documented disposition** | Not a compensating control |
| Quarterly analytical review of revenue by stream | **Fails.** Core revenue of $28,200 in Q4; a 3% variance is $846, against performance materiality of $940. The smallest variance the review would investigate exceeds the misstatement that matters | Independent | Performed, evidence retained | Not a compensating control |

No control satisfies all three criteria, and four fail on precision alone. Precision is the argument that persuades
a national office: a compensating control must be capable of detecting a misstatement of the size that concerns
you, and a reconciliation between two outputs of the same engine has precision of zero as to errors inside it.

On severity, magnitude is the accounts exposed — 4100, 4110, and 4120 ($135,800) and 2400, 2405, and 2410
($78,200) — and because a change to an allocation rule affects the entire subscription population, the potential
magnitude is many multiples of the $1,450 overall materiality. Likelihood rests on six credential holders, no
multi-factor authentication, a password unchanged for 33 months, 5 configuration changes with no ticket, and a
separated employee retaining access for 111 days; on any reasonable reading it is more than remote. The deficiency
is at least a significant deficiency and a strong candidate for a material weakness individually; Chapter 14 owns
the severity framework and the aggregation with W-2 through W-14 that produces the adverse ICFR opinion in
Chapter 20.

### Resolution and Conclusion

Management's remediation, initiated December 2025: federate all four local accounts to Okta; delete `revpro_admin`
and issue named accounts to the two Larkspur consultants with expiry dates; enforce MFA; assign an owner to
`svc_revpro_integration` and rotate its key. Because remediation began in December and the ICFR opinion is as of
December 31, 2025, the remediation cannot support an effectiveness conclusion for FY2025 — a point Chapter 14
develops and Chapter 19 carries into the as-of evaluation.

The audit consequence was a re-planned substantive revenue strategy:

| Element | Original plan (with control reliance) | Revised plan | Basis |
| --- | --- | --- | --- |
| Contract selections for revenue recomputation | 45 | 100% of the 168 contracts with FY2025 recognized revenue of $200 or more, aggregating $71,400 (48.2% of $148,200), plus a monetary-unit sample of 62 from the residual $76,800 | Automated allocation cannot be relied upon; revenue must be recomputed from contract terms |
| RevPro manual adjustments | Sample of 10 | All 91 | Population is small, self-selected for risk, and made under an unattributable account |
| RevPro configuration rules | Test of one per rule, benchmarked where unchanged | All 27 tested in the current year; 0 eligible for benchmarking | §11.14 |
| RevPro-sourced reports used as evidence | Accepted with a completeness and accuracy check | Reconciled to the Zuora Billing invoice register and to Salesforce order forms — populations outside RevPro | §11.15 |
| Revenue testing hours | 210 | 465 | Incremental 255 hours |

$71,400 plus $76,800 equals $148,200, which is total FY2025 revenue; the coverage claim ties to the statement of
operations rather than to a subledger total, which is the point.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                    WP 8220-07
AtlasFlow, Inc. — Year ended December 31, 2025
ZUORA REVENUE PRIVILEGED ACCESS — EVALUATION OF THE SHARED
`revpro_admin` ACCOUNT AND OF MANAGEMENT'S COMPENSATING CONTROLS

Prepared by:  B. Osei (BO)              Date prepared: 01/14/2026
Reviewed by:  F. Nazari (FN)            Date reviewed:  01/19/2026
Reviewed by:  G. Lindqvist (GL)         Date reviewed:  01/22/2026
Partner:      D. Whitcombe (DW)         Date reviewed:  02/02/2026

PURPOSE
To evaluate the logical access deficiency identified as W-1, to assess
management's assertion that five existing controls compensate, and to
determine the consequence for the FY2025 revenue substantive strategy.

SOURCE OF INFORMATION
1. Zuora Revenue tenant user listing at 12/31/2025 (27 accounts).            (a)
2. Zuora Revenue configuration audit log, 01/01/2025-12/31/2025
   (43 events) and revenue-schedule adjustment log (91 events).              (a)(b)
3. 1Password shared vault entitlement report for entry "RevPro Admin"
   (6 holders).                                                              (a)
4. ADP termination report (T. Lund, separation date 06/13/2025).             (b)
5. Internal audit ITGC readiness assessment, July 2025, observation W-1.
6. Inquiry of D. Kim (VP Revenue Accounting) 11/06/2025 and 01/09/2026;
   R. Sandoval (Director IT) 11/07/2025; T. Okafor (CFO) 11/20/2025.

PROCEDURES PERFORMED
1. Identified all accounts able to authenticate to the tenant without
   passing through Okta: 4 of 27 (14.8%). MFA not enforced on any of
   the 4.                                                                    (c)
2. Obtained the shared vault entitlement report and traced each of the
   6 holders to an employment or contractor record. 1 holder (T. Lund)
   separated 06/13/2025; entitlement removed 10/02/2025, 111 days.           (c)
3. Tested attribution for all 117 events performed under `revpro_admin`
   (26 configuration changes, 91 schedule adjustments). Account name is
   the only actor recorded. Source IP narrowed 34 events to Larkspur
   Consulting; 83 events not attributable to any individual.                 (c)
4. Traced all 91 schedule adjustments to a Jira ticket or a documented
   I-2 exception item. 89 supported; 2 (total 76) unsupported, both
   recomputed independently from the underlying contracts and found
   accurate.                                                                (c)(d)
5. Traced all 26 configuration change events to a Jira ticket. 21
   supported; 5 with no ticket, including 2 of the 5 events comprising
   the February 2025 ramp configuration change.                              (c)
6. Evaluated each of the 5 compensating controls asserted by management
   against precision, independence, and tested effectiveness. See the
   evaluation table above; none satisfies all three criteria.                (c)

RESULTS
Access to the Zuora Revenue configuration and to the revenue schedules is
not restricted to authorized individuals and cannot be attributed to a
person. 117 privileged actions in FY2025, of which 83 cannot be traced to
any individual and 7 (5 configuration changes, 2 adjustments) have no
authorizing documentation. One credential holder was a separated employee
for 111 days. No misstatement was identified: all 91 adjustments were
recomputed or supported, and the 27 configuration rules were tested in full
at WP 7200-03 (Chapter 12) with no exception in the rules' current state.

CONCLUSION
The deficiency is a deficiency in both the design and the operation of
logical access over the revenue subledger. Potential magnitude is the whole
of subscription revenue (135,800) and the contract liability (78,200), each
a multiple of overall materiality of 1,450; likelihood is more than remote.
Individually evaluated as at least a significant deficiency and a candidate
for material weakness; the severity determination and the aggregation with
W-2 through W-14 are performed at WP 8400-05 (Chapter 14). Reliance on the
RevPro automated allocation and scheduling controls and on RevPro-sourced
information produced by the entity is withdrawn for the full year. The
revenue substantive plan is revised at WP 6000-01: 168 contracts recomputed
in full (71,400) plus a monetary-unit sample of 62 over the residual
(76,800), 255 incremental hours. Communicated to the audit committee
02/13/2026.

TICK MARK LEGEND
(a) Obtained directly from the system; extract parameters inspected and
    the report regenerated in the auditor's presence.
(b) Population completeness corroborated by an independent source.
(c) Deviation or condition constituting a control deficiency.
(d) Recomputed independently by the auditor without reliance on the
    system under examination.
```

### Lessons

1. **Attribution is a control objective in its own right.** A shared credential does not merely widen access; it
   destroys the evidence every other test of that application depends on. No misstatement was found and the
   deficiency is still severe, because the deficiency is the inability to know.
2. **Test the compensating control argument on precision first.** Independence failures are easy to dispute and
   easy to appear to fix by reassigning a person. Precision failures are arithmetic: a 3% analytical threshold on
   $28,200 is $846 against $940 of performance materiality.
3. **Quantify the consequence in the currency the engagement understands.** "We cannot rely on ITGCs" produces
   argument; "45 selections becomes 168 recomputations plus 62 sample items, and 210 hours becomes 465" produces
   decisions — including management's decision to remediate in December.
4. **Follow the credential, not the account.** The finding that made the severity conclusion unavoidable was in the
   password vault's entitlement report, not in the application. Ask for the vault report.

## Common Mistakes

### Mistake 11.1 — Testing ITGCs with no reliance inventory

**What it looks like.** A 34-row ITGC matrix, each row tested, with no document anywhere stating what depends on
any of them.
**Why it happens.** The matrix is copied from management's Section 404(a) documentation or from the prior year, so
the file inherits management's scope rather than deriving the auditor's.
**What goes wrong.** Two failures at once. Controls are tested that support no reliance, and controls that support
reliance are omitted — AtlasFlow's 7 gaps in Step 7 of the walkthrough are all of the second kind. When a
deficiency arises there is no way to say what it costs, so the deficiency evaluation becomes an argument about
adjectives.
**How to avoid it.** Build Exhibit 11-1 before designing a single test, and require every tested control to cite a
reliance reference.

### Mistake 11.2 — Testing de-provisioning from the list of accounts IT disabled

**What it looks like.** "Selected 25 of 187 terminated user accounts from the IT termination log and agreed each to
a separation date."
**Why it happens.** The IT log is the easiest population to obtain and it is already in the right format.
**What goes wrong.** The population is the control's own output. It contains every account that *was* removed and
by construction excludes every account that was not, which is the entire assertion. The test cannot fail.
**How to avoid it.** Source the population from human resources and contractor records, prove it three ways
(Exhibit 11-8), and join it to the application listings yourself.

### Mistake 11.3 — Treating "vendor-hosted" as equivalent to "out of scope"

**What it looks like.** A scoping memo concluding that because AtlasFlow runs no servers, general IT controls are
covered by SOC 1 reports and nothing is tested at the entity.
**Why it happens.** The observation that the entity controls only one layer is correct, and the inference from it
is wrong.
**What goes wrong.** The one layer the entity controls is the one where user access, roles, and configuration live —
which is where every ITGC deficiency at AtlasFlow actually is. W-1 through W-7 are all application-layer findings
in vendor-hosted systems.
**How to avoid it.** Scope per domain per application (Exhibit 11-4), and state explicitly which layers the SOC 1
covers and which remain with the entity (Exhibit 11-6).

### Mistake 11.4 — Applying a ticket-and-approval control design to a continuous-deployment pipeline

**What it looks like.** A change-management test that requests a Jira ticket for a sample of 25 from a population
of 3,100 deployments.
**Why it happens.** The test design is inherited from an environment with quarterly releases.
**What goes wrong.** Either the client creates 3,100 valueless tickets, or the test finds a 40% deviation rate that
reflects a mismatch between the documented control and the way software is actually shipped rather than a real
control failure. Both outcomes waste the engagement's credibility.
**How to avoid it.** Stratify to the financially relevant population (583 of 3,100), test the pipeline's automated
enforcement by configuration, query the whole population for bypasses, and sample only for the attributes
configuration cannot enforce.

### Mistake 11.5 — Reading the SOC 1 opinion and skipping the complementary user entity controls

**What it looks like.** A one-page SOC 1 memo recording the provider, the period, and "unqualified — reliance
supported."
**Why it happens.** The CUEC section sits near the end of a 90-page report and reads like boilerplate.
**What goes wrong.** The clean opinion is conditional on the CUECs. At AtlasFlow, 2 of 12 CUECs had no
corresponding control and 6 more mapped to controls that were not effective, so 8 of 12 control objectives are not
achieved for AtlasFlow despite two unqualified opinions.
**How to avoid it.** Produce Exhibit 11-20 for every report you intend to rely on: CUEC, mapped control, owner,
where tested, conclusion.

### Mistake 11.6 — Treating a bridge letter as evidence of operating effectiveness

**What it looks like.** A 184-day gap closed with a two-paragraph letter from the vendor and a note that "the gap
period is covered."
**Why it happens.** The letter looks like external evidence and arrives on the vendor's letterhead.
**What goes wrong.** A bridge letter is a representation that nothing changed, not an examination of anything. Its
persuasiveness decays with length, and beyond roughly 60 to 90 days it supports very little on its own.
**How to avoid it.** Compute the gap in days for every report (Exhibit 11-19), and for gaps beyond your firm's
threshold either test the entity's own detective controls for the gap period or test the automated controls
directly, as Brightline did for Coupa.

### Mistake 11.7 — Accepting a reconciliation between two outputs of the same system as a compensating control

**What it looks like.** "The monthly RevPro-to-GL reconciliation compensates for the access deficiency."
**Why it happens.** The reconciliation is real, it is performed, it is reviewed, and it always agrees — which feels
like assurance.
**What goes wrong.** It always agrees because both sides come from the same engine. A configuration change moves
both sides identically. The control's precision with respect to errors inside the system is zero.
**How to avoid it.** Test the three criteria in order — precision, independence, tested effectiveness — and start
with precision, because it is arithmetic rather than argument.

### Mistake 11.8 — Testing that the access review happened rather than what it consisted of

**What it looks like.** An inspected email with an attached spreadsheet and the reviewer's "reviewed and approved,"
concluded effective.
**Why it happens.** The control's documented description is "the data owner reviews the user listing quarterly,"
and an email evidences a review.
**What goes wrong.** Four things go untested: whether the listing was complete (AtlasFlow's omitted 18 of 214, all
privileged or integration accounts), whether the reviewer recorded per-user decisions, whether identified items
were removed (3 of 9 were not), and whether the retained roles were actually appropriate (2 of 25 were not).
**How to avoid it.** Test the four attributes in §11.8 explicitly, and reconcile the reviewed listing to a
listing you generate.

### Mistake 11.9 — Concluding "single sign-on with MFA" and never defining the exception population

**What it looks like.** A walkthrough note that all applications authenticate through Okta with MFA enforced, and a
test of the Okta policy configuration.
**Why it happens.** The client's answer is true for 757 of 813 accounts, and the auditor's question was about the
rule rather than about the exceptions.
**What goes wrong.** The 56 non-federated accounts bypass joiner approval, leaver deactivation, MFA, and session
policy simultaneously, and they include the shared administrator credential for the revenue subledger.
**How to avoid it.** Ask the specific question: for each in-scope application, list every account that can
authenticate without passing through the identity provider, including service accounts, API credentials, vendor
support accounts, and accounts predating federation. Then reconcile the total (Exhibit 11-12).

### Mistake 11.10 — Assuming a point-in-time segregation-of-duties analysis covers the year

**What it looks like.** A conflict analysis run on the December 31 role-to-user mapping, concluded for the period
January 1 to December 31.
**Why it happens.** The application shows current roles, and the extract is easy.
**What goes wrong.** AtlasFlow rebuilt its NetSuite roles in September 2025. The roles that operated for the first
263 days of the year no longer exist in the system, and a December analysis says nothing about them. Worse, nobody
retained the pre-upgrade export, so the evidence has to be reconstructed from the assignment audit trail.
**How to avoid it.** Ask whether roles changed during the period as a standing planning question, and request the
pre-change role export before the project goes live rather than after.

### Mistake 11.11 — Stating an ITGC conclusion without a period or a consequence

**What it looks like.** "ITGCs were not effective. Substantive testing was increased."
**Why it happens.** The severity conclusion feels like the end of the analysis, and Chapter 14 owns severity, so the
ITGC file stops.
**What goes wrong.** Nobody can execute the sentence. Which application, which domain, which period, which reliance
item, which procedure changes, by how much. W-2's window is 27 days and W-1's is a year; treating them identically
either over-audits or under-audits by a wide margin.
**How to avoid it.** End the ITGC file with Exhibit 11-21: deficiency, reliance removed, plan change, incremental
effort, per deficiency and per period.

## Practice Exercises

### Exercise 11-1 [Foundational]

For each report below, compute (a) the number of days of AtlasFlow's FY2025 (January 1 – December 31, 2025) covered
by the report period and (b) the gap days between the end of the report period and December 31, 2025. Confirm that
(a) plus (b) equals 365 for each. Reports: Provider A, October 1, 2024 – September 30, 2025; Provider B, November 1,
2024 – October 31, 2025; Provider C, July 1, 2024 – June 30, 2025; Provider D, January 1, 2025 – December 31, 2025;
Provider E, April 1, 2025 – March 31, 2026.

### Exercise 11-2 [Foundational]

Reach an in-scope or out-of-scope conclusion, per domain, with a one-sentence rationale, for each of the following.
(a) A vendor-hosted contract lifecycle management tool holding executed order forms, used by the audit team to
verify contract existence. (b) A vendor-hosted marketing automation platform whose only financial output is a lead
count used in a sales-productivity metric not disclosed in the Form 10-K. (c) A treasury portal at which the sole
administrator can both change entitlements and release payments, with $96,400 of cash across seven accounts.
(d) A tax determination engine whose output feeds invoices, where the $2,900 tax accrual is independently
recomputed by the audit team.

### Exercise 11-3 [Intermediate]

Salesforce access removal for the 137 separated individuals who held Salesforce entitlements produced the following
distribution: 0–1 day, 31 events, 22 aggregate days; 2–3 days, 27 events, 68 days; 4–7 days, 39 events, 214 days;
8–14 days, 24 events, 253 days; 15–30 days, 13 events, 258 days; over 30 days, 3 events, 138 days. The documented
service level is 24 hours. Compute the total event count, the total aggregate days, the average days to removal,
the count and rate of events within the service level, and the deviation rate. State the conclusion the deviation
rate supports and whether a larger sample would change it.

### Exercise 11-4 [Intermediate]

FY2025 production deployments by stratum: platform application code 1,848; integration and interface code 214;
infrastructure as code 806; analytics models 232. Relevance determinations: within platform code, only the metering
and entitlement services are financially relevant, comprising 96 deployments; all integration deployments are
relevant; within infrastructure as code, 41 deployments touched the metering database, the billing-pipeline IAM
roles, or the Snowflake network policy; all analytics model deployments are relevant. A query of merges to protected
branches identified 11 in-scope deployments merged with zero approving reviews or an administrative override.
Compute the total population, the in-scope population, the in-scope percentage, and the residual population from
which a sample for non-configurable attributes would be drawn.

### Exercise 11-5 [Intermediate]

Management asserts that the daily Stripe cash-to-revenue reconciliation, performed by a Staff Accountant and
reviewed monthly by the Controller, compensates for the absence of documented change approval on the two FY2025
modifications to the I-4 Lambda job (W-7). The reconciliation compares the Stripe settlement report to the summary
journal the Lambda job posted to NetSuite. Evaluate the assertion against the three criteria for a compensating
control and state your conclusion, including what evidence would change it.

### Exercise 11-6 [Intermediate]

Draft the in-scope conclusion paragraph for Snowflake for the FY2025 IT scoping memo, in 120 to 160 words. It must
state the reliance that runs through Snowflake, the domains in scope, the domains out of scope with a reason, the
layers AtlasFlow operates, and the known weakness that bears on the conclusion. Use only facts established in this
chapter and in the continuing case.

### Exercise 11-7 [Advanced]

Identify at least six defects in the following extract from a draft ITGC memo, and state the correct treatment of
each.

```text
WP 8100-01  IT GENERAL CONTROLS — SCOPE AND CONCLUSION (DRAFT)
1. Obtained management's list of 20 applications. All 20 are hosted by
   third-party vendors, so no ITGC testing is required at AtlasFlow.
2. Ten applications were determined to be significant based on the size of
   the account balances they support. The remaining ten were not tested.
3. SOC 1 reports were obtained for eight providers. All were reviewed and
   all opinions were unqualified, so reliance is supported for the full
   year.
4. De-provisioning was tested by selecting 25 users from the IT
   termination log; all 25 had been disabled. No exceptions.
5. Segregation of duties was evaluated using the role-to-user mapping
   downloaded on 12/31/2025. Fourteen conflicts were identified; management
   asserted compensating controls, which were accepted.
6. Program change was tested by selecting 25 of the 3,100 FY2025
   deployments and confirming each had a Jira ticket. Eleven did not; the
   deviation rate of 44% is attributable to documentation and no further
   work was performed.
7. Conclusion: ITGCs are effective and reliance on automated controls is
   supported.
```

### Exercise 11-8 [Advanced]

During the 27-day window from the September 20, 2025 NetSuite go-live to October 17, 2025, the 11 users who
retained the legacy Full Access role posted 312 journal entries totaling $18,400 in absolute value. Analysis of
those entries shows: 29 entries totaling $1,700 were posted to subsidiaries the users' intended roles could not
access; 26 entries totaling $1,540 were posted to accounts the users' intended roles could not reach; 8 entries
totaling $340 fall into both categories. Compute the distinct population of entries the correct role would have
blocked, and its absolute value. Then state the two dimensions on which you would conclude and what evidence would
be required to bound the second.

### Exercise 11-9 [Intermediate]

Three SOC 1 reports list complementary user entity controls as follows: Provider X, 6 CUECs; Provider Y, 6 CUECs;
Provider Z, 3 CUECs. Mapping to the user entity's control inventory shows 11 CUECs mapped to an existing control
and the remainder unmapped. Of the mapped CUECs, the auditor concluded 6 relied on controls that were not
effective. Compute the total CUECs, the unmapped count, the number of CUECs for which the related control objective
is not achieved for this user entity, and that number as a percentage of the total. State what the percentage means
for reliance on the three reports' unqualified opinions.

### Exercise 11-10 [Advanced]

Draft the deficiency description for W-3 (user access reviews performed annually rather than quarterly) at the
level of detail required for a written communication of control deficiencies, in 130 to 180 words. Include the
control as documented, the control as performed, the quantified deviations, the reliance affected, and the
compensating or mitigating factors considered. Do not conclude on severity.

### Exercise 11-11 [Advanced]

AtlasFlow's revenue engine has 27 configuration rules. Management's configuration log shows 22 unchanged since
December 31, 2024 and 5 changed in February 2025. FY2025 is AtlasFlow's first integrated audit. Program change and
logical access controls over the engine were concluded not effective. Determine how many of the 27 rules are
eligible for benchmarking and state every condition that fails, in order of how independently each one disposes of
the question.

### Exercise 11-12 [Advanced — spans Chapter 6]

Chapter 6 recomputed AtlasFlow's remaining performance obligation from a 14,392-row contract-level extract,
correcting management's draft of $215,860 to $214,000, of which $138,900 (64.9%) is expected within twelve months.
The reconciliation of billed RPO of $77,820 plus $380 of excluded deferred revenue to the $78,200 contract
liability supported the extract. The extract was produced from Zuora Revenue and delivered through the Snowflake
RevOps datamart. Given W-1 (unattributable administrative access to Zuora Revenue) and W-11 (the datamart was not
reconciled to the general ledger for the first three quarters of FY2025), compute the unbilled portion of RPO, and
state which reconciliations must be performed against populations outside Zuora Revenue and Snowflake before the
extract can support the disclosure.

## Solutions to Practice Exercises

### Solution 11-1

| Provider | FY2025 days covered | Gap days to 12/31/2025 | Check |
| --- | --- | --- | --- |
| A (Oct 1, 2024 – Sep 30, 2025) | Jan 1 – Sep 30, 2025 = 273 | Oct 1 – Dec 31 = 92 | 273 + 92 = 365 |
| B (Nov 1, 2024 – Oct 31, 2025) | Jan 1 – Oct 31, 2025 = 304 | Nov 1 – Dec 31 = 61 | 304 + 61 = 365 |
| C (Jul 1, 2024 – Jun 30, 2025) | Jan 1 – Jun 30, 2025 = 181 | Jul 1 – Dec 31 = 184 | 181 + 184 = 365 |
| D (Jan 1 – Dec 31, 2025) | 365 | 0 | 365 + 0 = 365 |
| E (Apr 1, 2025 – Mar 31, 2026) | Apr 1 – Dec 31, 2025 = 275 | 0 at the end | 275 covered; **90 days uncovered at the front** (Jan 1 – Mar 31, 2025) |

Provider E is the trap: a report period that begins inside your fiscal year leaves a gap at the beginning, which no
bridge letter addresses because bridge letters run forward. The response is the same as for an end gap — test the
entity's own detective controls for January through March, or obtain the prior report, which for E would cover
April 1, 2024 – March 31, 2025.

### Solution 11-2

(a) **In scope for logical access only.** Reliance runs through it because the audit team uses the executed order
form as evidence of contract existence; no automated control in the tool is relied upon, and AtlasFlow does not
develop or operate it, so program change, program development, and computer operations are out of scope. Note that
a SOC 2 report, if that is what the vendor provides, supports no ICFR reliance.
(b) **Out of scope, all domains.** No item of reliance runs through it; the lead count does not enter the financial
statements or the Form 10-K, so there is no assertion and no other information to be consistent with.
(c) **In scope for logical access and payment authorization; out of scope for program change, program development,
and computer operations.** The sole-administrator design is a design deficiency independent of any deviation
because entitlement changes are unreviewed and the administrator can also initiate payments.
(d) **Out of scope, all domains.** The engine's output is not relied upon as an automated control and the accrual is
recomputed substantively. The correct rationale is the absence of reliance, not the size of the $2,900 balance,
although the balance's relationship to performance materiality of $940 supports the decision not to build reliance.

### Solution 11-3

Total events: 31 + 27 + 39 + 24 + 13 + 3 = 137. Total aggregate days: 22 + 68 + 214 + 253 + 258 + 138 = 953.
Average: 953 ÷ 137 = 6.96 days, or 7.0 days rounded. Within the 24-hour service level: 31 events, 31 ÷ 137 = 22.6%.
Deviation rate: 137 − 31 = 106, and 106 ÷ 137 = 77.4%.

A 77.4% deviation rate supports the conclusion that the control does not operate, and the conclusion is available
without sampling theory because the test was performed on the entire population. A larger sample is not merely
unnecessary; there is no larger sample, since 137 is the population. The only remaining work is directed at
consequence rather than at conclusion: obtain post-separation login and activity evidence for the exceptions,
concentrating on the 3 events beyond 30 days and any event where the individual left involuntarily.

### Solution 11-4

Total population: 1,848 + 214 + 806 + 232 = 3,100. In-scope: 96 + 214 + 41 + 232 = 583. In-scope percentage:
583 ÷ 3,100 = 18.8%. Residual for sampling: 583 − 11 = 572.

The 11 bypasses are removed from the sampling frame because they are tested 100% — they are the population of
known control failures, and sampling from a frame that includes them either double-counts or dilutes. The
remaining 572 are sampled only for the attributes branch protection cannot enforce: reviewer independence from the
author, evidence of test execution, and a linked business authorization.

### Solution 11-5

**Conclusion: partial mitigation only, and the constraint is precision.** The reconciliation compares the Stripe
settlement report to the journal the Lambda job posted. The settlement report is external to both AtlasFlow and the
job, so this is *not* the two-outputs-of-one-engine failure that defeats the RevPro reconciliation: it has real
precision as to the total amount posted. What it cannot detect is misclassification — a modification posting the
correct total to the wrong revenue account, or mapping refunds to contra revenue rather than to the refund
liability, reconciles perfectly in total. The exposure is the accuracy *and* classification assertions for $6,100 of
revenue and the $1,700 in account 1205, so precision is sufficient for part of it and insufficient for the rest.
Independence passes: a Staff Accountant prepares and the Controller reviews, and neither can deploy code. Tested
effectiveness passes: the failure log shows 17 job failures and a duplicate posting of $41 that the reconciliation
caught and corrected within three days.

**What would move it.** To full mitigation: a reconciliation performed by revenue account and customer count rather
than by settlement total, with evidence that account-level differences were investigated. To no mitigation: any
month in which the reconciliation was not performed, or a difference cleared to suspense without investigation.

### Solution 11-6

Model answer (146 words):

> Snowflake is in scope for logical access and for program change, and out of scope for program development and for
> computer operations other than the scheduled loads described below. Reliance runs through it in two ways: it
> delivers the contract-level extract supporting the $214,000 remaining performance obligation disclosure and most
> other audit extracts, and its RevOps datamart produces the $172.0 million annual recurring revenue and 112% net
> revenue retention figures presented in management's discussion and analysis. AtlasFlow operates the application
> layer and, unusually for a hosted platform, the database layer: it defines roles, warehouses, schemas, and object
> privileges, and 6 users hold write access to the RevOps schemas while 47 hold read access to replicated general
> ledger, billing, and CRM data. Access is therefore broader than access to the source systems. Weakness W-11 — the
> absence of a reconciliation of the datamart to the general ledger for the first three quarters of FY2025 — bears
> directly on the reliability of datamart-sourced information and is developed in Chapter 12.

### Solution 11-7

1. **Paragraph 1 — "hosted by third-party vendors, so no ITGC testing is required."** Wrong inference. The entity
   controls the application layer, where user administration, roles, and configuration live, and that is where every
   AtlasFlow ITGC deficiency is. Correct treatment: scope per domain per application and state which layers the
   service organization covers.
2. **Paragraph 1 — the inventory is accepted as given.** Management's list is not the population. Correct
   treatment: reconcile to independent sources (identity provider catalog, compliance tool inventory, vendor spend)
   and address systems retired during the period.
3. **Paragraph 2 — significance determined by account balance size.** Scope is determined by whether reliance runs
   through the application, not by balance size. Correct treatment: apply the reliance inventory; document a
   conclusion and rationale for all 20, including the out-of-scope ones.
4. **Paragraph 3 — unqualified opinions equated with full-year reliance.** Ignores report periods and gap days
   (one report has a 184-day gap), deviations noted in the service auditor's testing, complementary user entity
   controls, and subservice carve-outs. Correct treatment: Exhibit 11-19 plus a CUEC mapping.
5. **Paragraph 4 — de-provisioning tested from the IT termination log.** The population is the control's own
   output and the test cannot fail. Correct treatment: build the population from HR, contractor, and acquired-entity
   records and prove it independently.
6. **Paragraph 5 — a December 31 role mapping used to conclude on the full year, and compensating controls
   accepted without evaluation.** Roles were rebuilt in September 2025, so the mapping covers 103 days. Correct
   treatment: reconstruct the earlier period from the assignment audit trail, and evaluate each asserted
   compensating control against precision, independence, and tested effectiveness.
7. **Paragraph 6 — an 11-in-25 deviation rate dismissed as documentation, with no further work.** A 44% deviation
   rate ends the test; it also signals that the documented control does not match how changes are actually
   deployed. Correct treatment: stratify to the financially relevant population, test the pipeline's automated
   enforcement, and query the whole population for bypasses.
8. **Paragraph 7 — an aggregate "ITGCs are effective" conclusion.** Conclusions must be stated by domain and
   application, for a period, and must be inconsistent with the deviations recorded in the same memo.

### Solution 11-8

Distinct entries: 29 + 26 − 8 = 47. Absolute value: $1,700 + $1,540 − $340 = $2,900. The subtraction of the overlap
is the whole exercise; adding the two categories would report 55 entries and $3,240, overstating the population by
17% and the value by 12%.

The two dimensions are the misstatement that *did* occur and the misstatement that *could* have occurred. The
first is bounded by testing all 47 entries to support and to business purpose, which at AtlasFlow identified no
misstatement (2 entries totaling $310 were prepared and approved by the same person, which is a W-12 condition
rather than a W-2 consequence). The second is not bounded by the $2,900, because the legacy role also permitted
chart-of-accounts and approval-workflow modification, whose potential effect is not limited to entries the users
happened to post. To bound it you would need the FY2025 chart-of-accounts change log and the approval-workflow
configuration change log for the 27-day window, tested to authorization — which at AtlasFlow showed 9
chart-of-accounts changes and 38 workflow changes for the year, 2 of which fell in the window and both of which
were the upgrade rebuild itself.

### Solution 11-9

Total CUECs: 6 + 6 + 3 = 15. Mapped: 11. Unmapped: 15 − 11 = 4. Control objectives not achieved for this user
entity: 4 unmapped + 6 mapped-but-ineffective = 10. As a percentage: 10 ÷ 15 = 66.7%.

The percentage means that two-thirds of the control objectives the service auditors opined on are not achieved for
this user entity, notwithstanding unqualified opinions, because the opinions are conditional on controls the user
entity was assumed to operate and did not. The reports remain reliable evidence about the service organizations'
own controls; they simply do not deliver the combined control objective. The practical consequence is that reliance
must be rebuilt at the user entity — either by remediating and testing the 10 controls, or by substantive
procedures over the affected processing.

### Solution 11-10

Model answer (168 words):

> **Periodic user access review — Salesforce, Zuora Billing, Zuora Revenue, and NetSuite.** Management's control
> documentation describes a quarterly review by the designated data owner of each application's active user listing,
> to be completed within 15 days of quarter end, with inappropriate access removed. As performed during FY2025, the
> review was executed once per application rather than quarterly: 3 of 12 expected instances were performed, and
> each was completed after its documented deadline — Salesforce and Zuora on August 25, 2025, 41 days after the
> July 15 deadline, and NetSuite on November 7, 2025, 23 days after the October 15 deadline. Testing of the
> NetSuite instance identified further conditions: the listing reviewed contained 196 of the 214 then-active
> accounts, omitting all 12 integration accounts and all 6 accounts holding the Administrator role; 3 of the 9
> accounts the reviewer flagged for removal remained active at December 31, 2025; and 2 of 25 retained roles
> independently evaluated by the engagement team were not consistent with the individual's responsibilities. The
> control is the detective control on which reliance for access provisioning and de-provisioning deviations would
> otherwise depend. No mitigating control was identified.

### Solution 11-11

**Zero of the 27 rules are eligible.** Four conditions fail, and they dispose of the question with decreasing
independence:

1. **No baseline (most independent).** Benchmarking carries forward a prior-period test of operating effectiveness.
   FY2025 is the first integrated audit, so no such test exists for any of the 27 rules. This alone ends the
   analysis, and it applies to every first-year Section 404(b) engagement regardless of the state of the ITGCs.
2. **General IT controls over program change are not effective.** Benchmarking is conditional on them, because they
   are what makes "the control has not changed" credible.
3. **General IT controls over access to programs are not effective.** The 26 unattributable configuration change
   events mean the change population itself is unreliable.
4. **Five rules changed in February 2025 (least independent, narrowest).** Even in a fully effective environment
   those 5 would require current-year testing; this condition would leave 22 eligible and is therefore the weakest
   of the four.

A weaker but defensible alternative answer is "22 eligible but for the ITGC failures," which is right about the
change population and wrong about the conclusion: it treats condition 4 as the operative constraint and never
reaches conditions 1 through 3. The reason it matters is efficiency planning — a team that believes 22 rules are
benchmarkable budgets for 5 tests and must find budget for 27.

### Solution 11-12

Unbilled RPO: $214,000 − $77,820 = $136,180.

Three reconciliations against populations outside both Zuora Revenue and Snowflake are required, because the
extract passes through two systems whose general controls are deficient and a reconciliation to either is
self-referential:

1. **Billed RPO to the contract liability, corroborated to the Zuora Billing invoice register.** The $77,820 plus
   $380 tie to $78,200 is necessary but insufficient alone, because deferred revenue is itself fed by the I-3
   interface from Zuora Revenue. The independent leg is the invoice register, upstream of Zuora Revenue, which
   produced $163,750 of FY2025 billings.
2. **Unbilled RPO of $136,180 to the contract population evidenced by executed order forms.** Nothing inside Zuora
   Revenue establishes that the contracted amounts and terms are what the customer signed, and the order forms are
   also where the termination-for-convenience enforceability judgment is evidenced.
3. **The Snowflake extract to a direct extract from Zuora Revenue**, which isolates the datamart's transformation
   layer (W-11) from the subledger's contents (W-1) so that a difference can be attributed to a cause.

Chapter 6's conclusion survives, because its recomputation was built from contract data and reconciled to the
invoice register rather than accepted from the datamart.

## Review Questions

**RQ 11-1.** Why is an information technology general control never relevant on its own, and what are the three
things it can make trustworthy?

**RQ 11-2.** Name the five ITGC domains and state which one is firm methodology rather than a separate professional
requirement.

**RQ 11-3.** What are the four IT layers, and how many does an entity typically control in a multi-tenant
vendor-hosted application?

**RQ 11-4.** Why is a large account balance not a criterion for including an application in ITGC scope?

**RQ 11-5.** Name the five risks arising from the use of information technology and state which ITGC domain
primarily addresses each.

**RQ 11-6.** Why is the list of accounts that IT disabled the wrong population for testing de-provisioning, and
what is the right one?

**RQ 11-7.** What is the difference between a segregation-of-duties conflict and a control deviation, and what
follows for the test design?

**RQ 11-8.** What four attributes must a periodic user access review satisfy before it can be relied upon?

**RQ 11-9.** Why does a shared administrator account defeat testing even when no misstatement is found?

**RQ 11-10.** Why does a ticket-and-approval control design fit vendor SaaS configuration changes but not
continuous deployment of in-house code?

**RQ 11-11.** What makes emergency changes a population you test in full rather than sample?

**RQ 11-12.** What is a complementary user entity control, and what is the consequence when one is unmapped?

**RQ 11-13.** Distinguish the carve-out method from the inclusive method, and state the auditor's procedure when a
report uses the carve-out method.

**RQ 11-14.** What is a bridge letter, what does it not provide, and what are the alternatives when the gap period
is too long to bridge?

**RQ 11-15.** State the five conditions for benchmarking an automated application control, and explain why
benchmarking is unavailable in a first-year ICFR audit.

**RQ 11-16.** Why can a failed backup restoration test be a real control deficiency and still have no effect on any
assertion in the current-year financial statements?

## Answers to Review Questions

**RQ 11-1.** An ITGC controls the IT environment rather than a transaction, so it cannot by itself prevent or detect
a misstatement. Its relevance is entirely derivative: it makes trustworthy an automated control, an IT-dependent
manual control, or information produced by the entity that is used as audit evidence. If none of the three is
relied upon, the ITGC is not relevant to the audit.

**RQ 11-2.** Logical access, program change, program development, computer operations, and data management. Data
management is firm methodology; most methodologies treat it either as a fifth domain or as a sub-domain of logical
access, and no professional standard prescribes the taxonomy at all.

**RQ 11-3.** Application, database, operating system, and network. In a multi-tenant vendor-hosted application the
entity controls one — the application layer, comprising tenant configuration, users, roles, report definitions, and
integration credentials. Snowflake is a partial exception because the entity also administers schema and object
privileges.

**RQ 11-4.** Because scope is a conclusion about reliance, not about magnitude. AtlasFlow's Concur touches $2,900
of expense and is out of scope because no automated control or item of IPE in it is relied upon, while FloQast
touches no balance and is in scope because its sign-off dates are the evidence that close controls operated.

**RQ 11-5.** Unauthorized access to data (logical access, and data management); unauthorized changes to systems or
programs (program change); failure to make necessary changes (program change and computer operations);
inappropriate manual intervention in automated processing (logical access and data management); and loss of or
inability to access data (computer operations).

**RQ 11-6.** Because that list is the control's own output: it contains every account that was removed and by
construction excludes every account that was not, which is the assertion being tested, so the test cannot fail. The
right population is the population of separation events sourced outside IT — payroll terminations for every entity,
contractors with application access, and separations at an acquired business still on its own payroll — with its
completeness proved independently.

**RQ 11-7.** A conflict is a design condition that exists continuously from the moment the roles are configured; a
deviation is a failure of a control to operate on a particular occasion. There is therefore no sample for a
conflict: you inspect the role-to-user mapping at a point in time and separately establish that the mapping did not
change during the period. If it did change, as at AtlasFlow in September 2025, the point-in-time analysis covers
only the period after the change.

**RQ 11-8.** The listing must be complete, including privileged, integration, and service accounts; it must be
generated independently of the reviewer; the reviewer's evidence must record a per-user decision rather than a
global approval; and items identified must be tracked to removal. AtlasFlow's one tested instance failed all four
to some degree, most seriously by omitting the 12 integration and 6 Administrator accounts from a 214-account
population.

**RQ 11-9.** Because the deficiency is the loss of attribution, not the loss of restriction. Every other test of
that application depends on knowing who performed an action; with a shared credential, 83 of 117 privileged actions
at AtlasFlow could have been performed by any of six people, including a separated employee. Testing the actions
and finding them supported bounds the misstatement that occurred; it does not restore the ability to conclude that
changes were authorized.

**RQ 11-10.** Configuration changes are few, high-impact, made through a screen with no build pipeline, and
promotable by anyone holding the privileged role, so the only available control is documented request, approval,
and reconciliation of the production change log to approvals. Code deployments number in the thousands and pass
through a pipeline that can enforce the control technically — branch protection requiring an independent reviewer
and a passing build — which is both stronger and testable by configuration. Imposing the first design on the second
produces thousands of valueless tickets; imposing the second on the first is impossible.

**RQ 11-11.** Because the population is small and self-selected for risk. Emergency changes are made under time
pressure, by whoever is available, with the pipeline's preventive controls deliberately bypassed, so they are the
highest-risk stratum in the change population and there are typically fewer than ten of them. Sampling from six
items is pointless.

**RQ 11-12.** A control the service organization assumes the user entity operates, without which the service
organization's stated control objective cannot be achieved. When it is unmapped, no one owns it: the service
auditor's unqualified opinion remains valid about the service organization's controls, but the combined control
objective is not achieved for that user entity, so the reliance the report appears to support is not in fact
available.

**RQ 11-13.** Under the carve-out method the subservice organization's controls are excluded from both the
description and the opinion, leaving a gap; under the inclusive method they are included in both. For every
carve-out the auditor must either obtain the subservice organization's own report or document why the carved-out
controls are not relevant to the reliance being placed. AtlasFlow's chain has three carve-outs, two of which are
covered by the AWS report already on hand.

**RQ 11-14.** A written representation from the service organization that the controls described in the report
continued to operate and that no changes or failures occurred during the gap period. It is a representation, not an
examination, so it provides no direct evidence of operating effectiveness. The alternatives are a report covering
the full period, testing the user entity's own detective controls for the gap, testing the automated controls
directly, or procedures at the service organization.

**RQ 11-15.** The control must be entirely automated with no manual or judgmental element; general IT controls over
program change, access to programs, and computer operations must be effective; a baseline test must have been
performed in a prior period; the auditor must determine the control has not changed; and the risk must not require
annual testing. In a first year the third condition cannot be met, because there is no prior-period test to carry
forward — which is why the efficiency benefit of automated controls does not arrive until year two.

**RQ 11-16.** Because backup and recovery affects the availability of data prospectively rather than the accuracy or
completeness of what has already been recorded. At AtlasFlow no FY2025 loss event occurred and the metering data
supporting $4,200 of overage revenue was available and tested, so no assertion is unsupported. The deficiency's
severity turns on likelihood — the chance that a future event produces unrecoverable data — which is why the
scoping decision to include or exclude the control should be stated explicitly in the file rather than assumed.

## Key Definitions

**Application layer.** The tier of an information system comprising the application's own configuration, user
accounts and roles, report definitions, and integration credentials. In a multi-tenant vendor-hosted application it
is normally the only layer the user entity controls, and it is where most SaaS-era ITGC deficiencies are found.

**Benchmarking.** Carrying forward evidence about the operating effectiveness of an entirely automated application
control from a prior period, on the basis that a control that has not changed will operate consistently. Addressed
in the appendix to AS 2201 and conditional on effective general IT controls, an established baseline test, and a
determination that the control has not changed.

**Bridge letter.** A written representation from a service organization covering the interval between the end of
its service auditor's reporting period and the user entity's balance sheet date, stating that the controls
described continued to operate without change or failure. It is a representation rather than an examination and
provides no direct evidence of operating effectiveness.

**Carve-out method.** The presentation in a service auditor's report under which a subservice organization's
controls are excluded from both the description of the system and the scope of the opinion, leaving the user
auditor to obtain evidence about those controls separately.

**Complementary user entity control (CUEC).** A control the service organization assumes the user entity operates,
and without which the service organization's stated control objective cannot be achieved. CUECs are listed in the
SOC 1 report and must be mapped to a control at the user entity, tested, and concluded upon; an unmapped CUEC means
the combined control objective is not achieved for that user entity.

**Computer operations.** The ITGC domain addressing the scheduling and execution of production processing, the
detection and resolution of failures, and the backup and recoverability of data. Its financially relevant
population is the jobs that create or move accounting data, not everything an IT department schedules.

**Data management controls.** Controls over changes to data made outside an application's normal processing —
direct database writes, data-fix scripts, and vendor-executed corrections. Treated as a fifth ITGC domain or as a
sub-domain of logical access as a matter of firm methodology rather than professional requirement.

**De-provisioning.** The removal of an individual's system access upon separation or role change. Its distinguishing
audit feature is that the population must be sourced from outside the IT function, because the list of accounts IT
disabled is the control's own output.

**Emergency change.** A production change deployed outside the normal approval and testing sequence to address an
urgent condition, permitted by design provided the control includes a requirement for documentation and approval
after the fact within a stated period. Because the population is small and self-selected for risk, it is tested in
full.

**Federated authentication.** Authentication performed by a central identity provider on behalf of an application,
so that joiner, mover, and leaver events and multi-factor requirements are enforced once rather than separately in
each application. Its audit significance lies in the exception population — the accounts that authenticate without
passing through the provider.

**General information technology control (ITGC).** A control over the information technology environment — access,
change, development, and operations — that supports the continued proper operation of automated controls, the
integrity of information produced by the entity, and the reliability of IT-dependent manual controls. Defined in
AU-C 315 as amended by SAS 145; addressed in PCAOB standards through AS 2110 and AS 2201 without the same
definitional vocabulary.

**Inclusive method.** The presentation in a service auditor's report under which a subservice organization's
relevant controls are included in the description of the system and within the scope of the service auditor's
opinion, so that no separate report is required.

**Infrastructure as code (IaC).** The practice of defining servers, networks, databases, and access policies in
version-controlled configuration files that are applied to the environment automatically. It converts
infrastructure changes into a reviewable, testable change population and makes the source-control approval control
the operative ITGC for the infrastructure layer.

**IT layers.** The decomposition of an information system into the application, database, operating system, and
network tiers. Each layer is a separate opportunity to change data or logic without passing through the
application's own controls, and the scoping question for each is who operates it and what evidence covers it.

**Logical access.** The ITGC domain addressing whether access to applications, data, and privileged functions is
granted only to authorized individuals, is appropriate to the role, and is removed when no longer required. It
comprises provisioning, modification, de-provisioning, privileged access restriction, the periodic review, and
authentication.

**Periodic user access review.** A detective control in which the data owner recertifies an application's active
user listing at a stated frequency and inappropriate access is removed. It is the backstop for provisioning and
de-provisioning failures, which is why its own failure compounds every other access deficiency.

**Privileged access.** Access permitting configuration change, entitlement grants, direct data modification, or
alteration of audit logs. Its audit significance is twofold: appropriateness of the individuals holding it, and
attribution of the actions taken under it, the second of which a shared credential destroys.

**Program change control.** The ITGC domain addressing whether changes to applications and configurations are
authorized, tested, and approved before being placed in production. Its appropriate design differs between vendor
configuration changes and in-house code deployed through a pipeline.

**Program development control.** The ITGC domain addressing new systems and major upgrades: project authorization,
requirements and role design approval, testing, data conversion reconciliation, go-live approval, removal of legacy
access, and post-implementation review. The population is the project, so the test is a checkpoint review rather
than a sample.

**Recovery point objective (RPO).** The maximum tolerable amount of data loss, expressed as a period of processing,
that a recovery capability is designed to accept. In an IT context RPO means this; in a revenue context the same
acronym means remaining performance obligation (Chapter 6), and files that use both must disambiguate.

**Risks arising from the use of information technology.** The risks of material misstatement created by an entity's
reliance on IT: unauthorized access to data, unauthorized changes to systems or programs, failure to make necessary
changes, inappropriate manual intervention in automated processing, and loss of or inability to access data. AS 2110
requires their identification; AU-C 315 as amended by SAS 145 requires their identification together with the
general IT controls that address them.

**Segregation of duties.** A control objective requiring that incompatible functions — such as preparing and
approving a journal entry, or changing a system's configuration and reconciling its output — be performed by
different individuals. Within an application it is enforced by the permission model, and it is tested by a conflict
analysis of the role-to-user mapping rather than by sampling.

**Service auditor.** The practitioner who examines and reports on controls at a service organization under
AT-C 320. The service auditor is not the user entity's auditor and expresses no opinion on the user entity's
controls.

**Service organization.** An organization that performs processing forming part of a user entity's information
system relevant to financial reporting. Its use is addressed by AS 2601 and AU-C 402, and the auditor's evidence
about its controls is normally a SOC 1 report.

**SOC 1 report.** A service auditor's report under AT-C 320 on controls at a service organization relevant to user
entities' internal control over financial reporting. It is evidence about the service organization's controls only,
is conditional on the complementary user entity controls it lists, and must be evaluated for scope, period,
opinion, deviations, and subservice organization treatment.

**Subservice organization.** A service organization used by another service organization to perform some of the
services provided to user entities — as AWS is to Zuora. Its controls are either carved out of or included in the
primary service auditor's report, and every carve-out requires the user auditor either to obtain the subservice
report or to document why those controls are not relevant.

**Type 2 report.** A service auditor's report expressing an opinion on both the fairness of the description and the
suitability of design of controls and on their operating effectiveness throughout a specified period, and including
the service auditor's tests and results. Only a Type 2 report supports reliance on operating effectiveness; a
Type 1 addresses design as of a point in time.

**User entity.** The organization whose financial reporting information system incorporates the service
organization's processing — here, AtlasFlow, with respect to eight service organizations.

## Chapter Summary

1. An ITGC has no direct effect on the financial statements; its relevance is entirely derivative of an automated
   control, an IT-dependent manual control, or an item of information produced by the entity, and the reliance
   inventory that records those dependencies must be written before any test is designed.
2. The dependency chain must be readable in both directions: from an assertion down to the general control, and
   from a general control failure up to the reliance removed and the substantive procedure that replaces it.
3. Not every ITGC failure costs the audit anything — AtlasFlow's failed restoration test affects no FY2025
   assertion — and a file that grades all five domains as equally consequential is not risk-based.
4. Scope is decided per domain per application on the basis of reliance, not on the basis of balance size, which is
   why Concur's $2,900 of expense is out of scope and FloQast's sign-off dates are in.
5. A scoping conclusion must exist for every item in the inventory, and the inventory itself must be proved: at
   AtlasFlow, reconciling to the Okta catalog, the Vanta inventory, and Coupa vendor spend produced 51 candidate
   systems and identified 2 that management's 20-item list omitted, one of which had been decommissioned in April.
6. In a multi-tenant vendor-hosted application the entity controls one of four IT layers, which is not a reason to
   test nothing but a reason to test the application layer precisely and to obtain a service auditor's report for
   the rest — and to identify the responsibilities, such as authorization of vendor-executed data fixes, that fall
   between the two.
7. De-provisioning is tested from a population built outside the IT function: 268 payroll separations less 7
   transfers plus 19 contractors plus 4 former Kestrel employees equals 284 events, corroborated by the headcount
   roll-forward, the 291 Okta deactivations, and 268 final paychecks.
8. Full-population testing of those 284 events produced 1,761 aggregate days over 284 events, an average of 6.2
   days against a 24-hour service level and a deviation rate of 73.9%, and the distribution — 41 of the 74
   compliant removals falling in November and December — carried more information than the average.
9. A shared administrator credential is a failure of attribution rather than of restriction, and it defeats every
   downstream test in the application: 83 of 117 privileged actions in Zuora Revenue could not be attributed to any
   of six credential holders, one of whom had separated 111 days earlier.
10. Vendor configuration changes and in-house code deployments require different control designs, and the 3,100
    deployment population becomes auditable only by stratifying to the 583 that are financially relevant, testing
    the pipeline's automated enforcement by configuration, querying the whole population for the 11 bypasses, and
    sampling only for what configuration cannot enforce.
11. An implementation project is tested as a set of checkpoints, and the checkpoint most often missed is the
    removal of legacy access at go-live: W-2's 27-day window exposed 47 journal entries totaling $2,900 that the
    intended roles could not have posted, plus unbounded chart-of-accounts and workflow modification capability.
12. A SOC 1 report is evidence about the service organization's controls only, is conditional on its complementary
    user entity controls, and must be evaluated on period coverage as well as opinion — AtlasFlow's eight reports
    range from full-year coverage to a 184-day gap that no bridge letter can close.
13. Mapping the AWS and Zuora CUECs produced 12 items, of which 2 had no corresponding AtlasFlow control and 6
    mapped to controls the engagement team concluded were not effective, so 8 of 12 control objectives are not
    achieved for AtlasFlow notwithstanding two unqualified opinions.
14. Benchmarking is unavailable in a first-year ICFR audit for a reason unrelated to the state of the controls:
    there is no prior-period baseline test to carry forward, which is why all 27 RevPro configuration rules
    required current-year testing.
15. The ITGC file's final output is not a severity grade but an executable plan change: for AtlasFlow, 433
    incremental hours, revenue testing moved from 45 selections to 168 full recomputations plus a monetary-unit
    sample of 62, and every RevPro-sourced report reconciled to a population outside RevPro.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| Risks arising from IT as part of the overall risk assessment | Chapter 2 | Where the assertion-level risks this chapter responds to are identified and documented |
| Integrated-audit scoping and the first-year 404(b) planning consequences | Chapter 1 | The engagement-level decisions that set the ITGC budget and timing |
| Materiality, performance materiality, and the clearly trivial threshold | Chapter 3 | The $1,450 / $940 / $72 framework used in every precision argument here |
| Application-level automated controls, the 27 RevPro configuration rules, and the CPQ approval matrix | Chapter 12 | What the ITGCs in this chapter support; the substance of the configuration this chapter only tests for authorization |
| Interface controls I-1 through I-9, IPE completeness and accuracy, and the Snowflake RevOps datamart (W-11) | Chapter 12 | The application-level and report-level testing that the ITGC conclusions here make necessary or unnecessary |
| Walkthrough technique, and the discovery that the quarterly access review is annual | Chapter 13 | How the W-3 discrepancy between documented and performed control was surfaced |
| Test design, sample sizes, roll-forward from interim, deficiency severity, and aggregation | Chapter 14 | The sizing of every sample referred to here, and the severity methodology this chapter deliberately does not develop |
| Journal entry testing criteria including the 214 conflicted-user entries and the $250,000 threshold | Chapter 16 | The substantive consequence of W-12 and W-13 |
| Cash, treasury access, and positive pay | Chapter 8 | The payment-authorization consequences of the bank portal access findings |
| Capitalized internal-use software and the Jira time data | Chapter 10 | Why the source-control and project systems are financially relevant beyond change management |
| The deferred revenue and RPO extracts whose reliability depends on these conclusions | Chapter 6 | The disclosure that Exercise 11-12 revisits |
| Management override, privileged access, and the fraud risk assessment | Chapter 17 | The Brett Hallowell access design and the December backdating scheme |
| The ICFR conclusion, the as-of evaluation, and the adverse opinion with its material weakness description | Chapters 19 and 20 | Where December remediation meets the as-of date, and the report language these deficiencies produce |

## Further Reading

- PCAOB AS 2110, *Identifying and Assessing Risks of Material Misstatement*, on understanding how IT affects the
  flow of transactions and on identifying risks arising from the entity's use of IT.
- PCAOB AS 2201, *An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of
  Financial Statements*, including its appendix addressing benchmarking of automated application controls and its
  guidance on the relationship between automated controls and general IT controls.
- PCAOB AS 2301, *The Auditor's Responses to the Risks of Material Misstatement*, on the extent of substantive
  procedures where controls cannot be relied upon, and AS 1105, *Audit Evidence*, on the reliability of information
  produced by the entity.
- PCAOB AS 2601, *Consideration of an Entity's Use of a Service Organization*, on the use of a service auditor's
  report and the evaluation of complementary user entity controls.
- PCAOB AS 2401, *Consideration of Fraud in a Financial Statement Audit*, on management override and on the risk
  presented by individuals with privileged access; AS 1305, *Communications About Control Deficiencies in an Audit
  of Financial Statements*; and AS 1215, *Audit Documentation*.
- PCAOB staff guidance addressing the audit of internal control, including the guidance directed at audits of
  smaller and less complex companies.
- AICPA AU-C 315 as amended by SAS 145, effective for periods ending on or after December 15, 2023, including its
  requirements and application material on risks arising from the use of IT and on general IT controls; AU-C 402 on
  entities using a service organization; AU-C 265 on communicating internal control related matters; and AU-C 500
  as revised by SAS 142.
- AICPA AT-C section 320, *Reporting on an Examination of Controls at a Service Organization Relevant to User
  Entities' Internal Control Over Financial Reporting*, and the AICPA guide addressing service organization control
  reporting, for the structure and content of a SOC 1 report and the meaning of its opinion.
- COSO, *Internal Control — Integrated Framework* (2013), particularly Principle 11 on general control activities
  over technology, and the COSO guidance on applying the framework in a cloud computing environment.
- SEC Exchange Act Rules 13a-15 and Item 9A of Form 10-K, together with the SEC's interpretive guidance for
  management regarding its evaluation of internal control over financial reporting, and the staff guidance
  permitting exclusion of a recently acquired business from that assessment.
- IIA guidance on auditing information technology general controls and on the co-sourced internal audit function,
  relevant to the evaluation and use of the July 2025 readiness assessment.
- FASB ASC 350-40, *Internal-Use Software*, for the capitalization consequences of the development environment
  described in §11.10.

