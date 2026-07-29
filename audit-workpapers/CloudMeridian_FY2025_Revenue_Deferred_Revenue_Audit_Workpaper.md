# INTERNAL CONTROL AUDIT WORKPAPER
## Revenue Recognition & Deferred Revenue Cycle
### CloudMeridian Software, Inc. — Fiscal Year Ended December 31, 2025

---

| Field | Detail |
|-------|--------|
| **Engagement** | FY2025 Integrated Audit — Financial Statement Audit & SOX 404 Internal Control Audit |
| **Entity** | CloudMeridian Software, Inc. ("CloudMeridian" or the "Company") |
| **Cycle / Process** | Subscription Revenue Recognition, Billing, Cash Application, and Deferred Revenue |
| **Workpaper Reference** | WP-REV-001 through WP-REV-050 (Control Testing); WP-REV-BG (Background); WP-REV-RA (Risk Assessment); WP-REV-SS (Sample Selection); WP-REV-TR (Testing Results); WP-REV-EX (Exceptions); WP-REV-CON (Conclusion) |
| **Prepared By** | Jordan Hale, Senior Associate |
| **Prepared Date** | February 14, 2026 |
| **Reviewed By** | Morgan Ellis, Audit Manager |
| **Review Date** | February 21, 2026 |
| **Partner Review** | Priya Venkatesh, Engagement Partner |
| **Partner Review Date** | February 28, 2026 |
| **Period Under Audit** | January 1, 2025 – December 31, 2025 |
| **Interim Testing Window** | July 1, 2025 – September 30, 2025 |
| **Rollforward / Year-End Testing** | October 1, 2025 – December 31, 2025 |
| **Materiality (Planning)** | $1,850,000 (approximately 5% of pre-tax income from continuing operations, adjusted for non-recurring items) |
| **Performance Materiality** | $1,387,500 (75% of planning materiality) |
| **Clearly Trivial Threshold** | $92,500 (5% of planning materiality) |
| **Audit Standards Applied** | PCAOB AS 2201, AS 2301, AS 2315, AS 1105; ASC 606; COSO 2013 Internal Control — Integrated Framework |

---

# 1. BACKGROUND
**Workpaper Reference: WP-REV-BG**

## 1.1 Entity Overview and Business Model

CloudMeridian Software, Inc. is a privately held software-as-a-service (SaaS) company headquartered in Austin, Texas, with satellite offices in Denver, Colorado and Toronto, Ontario. The Company was founded in 2016 and provides a cloud-hosted business intelligence and operational analytics platform marketed primarily to mid-market and upper mid-market enterprises in the manufacturing, logistics, healthcare administration, and professional services verticals. As of December 31, 2025, CloudMeridian reported approximately **500 active paying customers**, a customer count that has grown from 412 at December 31, 2024 (year-over-year growth of approximately 21.4%).

The Company's core product offering, branded **Meridian Insights**, is delivered exclusively as a multi-tenant SaaS application hosted on Amazon Web Services (AWS). Customers access the platform through a web browser and authenticated API endpoints. There is no on-premise software license component within the standard commercial offering. Ancillary services include implementation/onboarding packages (typically completed within 30–90 days of contract signature), optional premium support tiers, and limited professional services for custom dashboard development. Management has represented—and our walkthrough procedures corroborated—that professional services are not material to the overall revenue mix (approximately 4.2% of total recognized revenue in FY2025) and are generally recognized as services are rendered under ASC 606.

CloudMeridian's commercial model is built around **monthly subscription revenue**. Customers execute Master Subscription Agreements (MSAs) with accompanying Order Forms that specify the subscription tier (Starter, Professional, Enterprise, or Enterprise Plus), the number of named or concurrent user seats, feature modules enabled, and the contractual term. Although Order Forms frequently specify annual or multi-year commitment periods for commercial predictability and volume discounting, **billing is structured on a monthly cadence** for the substantial majority of the customer base. Specifically:

- Approximately **78% of customers** (390 of 500) are billed monthly in advance for the forthcoming service month.
- Approximately **17% of customers** (85 of 500) are billed quarterly in advance.
- Approximately **5% of customers** (25 of 500) are billed annually in advance, typically larger Enterprise and Enterprise Plus accounts that negotiate annual prepayment discounts of 8–12%.

Because subscription fees are routinely collected in advance of the related service period, the Company maintains material **deferred revenue (contract liability) balances** on the balance sheet under ASC 606. At December 31, 2025, total deferred revenue was approximately **$4,872,000**, of which management classified $4,610,000 as current (expected to be recognized within 12 months) and $262,000 as non-current (related to multi-year prepaid arrangements with recognition schedules extending beyond one year). At December 31, 2024, total deferred revenue was approximately $3,941,000. The year-over-year increase of approximately $931,000 is directionally consistent with customer growth, modest average revenue per user (ARPU) expansion, and a slight mix shift toward annual prepayment arrangements among Enterprise Plus accounts.

## 1.2 Financial Profile Relevant to the Revenue Cycle

The following unaudited management-prepared balances (subject to audit adjustment) provide context for the design of our revenue and deferred revenue procedures:

| Metric | FY2025 | FY2024 | Change |
|--------|--------|--------|--------|
| Total subscription revenue recognized | $28,640,000 | $22,180,000 | +$6,460,000 (+29.1%) |
| Professional services & other revenue | $1,255,000 | $980,000 | +$275,000 (+28.1%) |
| **Total revenue** | **$29,895,000** | **$23,160,000** | **+$6,735,000 (+29.1%)** |
| Monthly recurring revenue (MRR) at year-end | $2,510,000 | $1,945,000 | +$565,000 (+29.0%) |
| Annual recurring revenue (ARR) at year-end | $30,120,000 | $23,340,000 | +$6,780,000 (+29.0%) |
| Deferred revenue — current | $4,610,000 | $3,720,000 | +$890,000 |
| Deferred revenue — non-current | $262,000 | $221,000 | +$41,000 |
| **Total deferred revenue** | **$4,872,000** | **$3,941,000** | **+$931,000 (+23.6%)** |
| Accounts receivable, net | $2,184,000 | $1,762,000 | +$422,000 |
| Active customers at year-end | 500 | 412 | +88 |
| Gross dollar retention (GDR) | 94.2% | 93.1% | +1.1 pp |
| Net dollar retention (NDR) | 112.8% | 109.4% | +3.4 pp |

Subscription revenue is the dominant account within the revenue cycle and is quantitatively material. Deferred revenue is also quantitatively material relative to planning materiality ($1,850,000) and performance materiality ($1,387,500). Accounts receivable arising from monthly subscription billings is quantitatively material. Accordingly, the engagement team designated the subscription revenue recognition and deferred revenue processes as **significant accounts / significant classes of transactions** for purposes of PCAOB AS 2201.

## 1.3 Systems Landscape and Process Narrative Summary

CloudMeridian's revenue cycle is supported by an integrated stack of commercial and financial systems:

| System | Role in Revenue Cycle | Owner |
|--------|----------------------|-------|
| Salesforce CRM (Enterprise Edition) | Opportunity management, quote generation, MSA/Order Form repository links, customer master initiation | VP Sales Operations |
| Conga / Salesforce CPQ | Quote-to-cash configuration, pricing rules, discount approval routing | Director of Revenue Operations |
| DocuSign | Electronic execution of MSAs and Order Forms | Legal / Sales Operations |
| Chargebee (Billing Engine) | Subscription lifecycle management, recurring invoice generation, proration, plan changes, dunning | Controller (Billing Operations) |
| Stripe | Payment gateway for credit card / ACH collections; webhook events feed Chargebee and NetSuite | Treasurer / Controller |
| NetSuite ERP (OneWorld) | General ledger, accounts receivable subledger, deferred revenue schedules, financial reporting | Controller |
| Workato (iPaaS) | Middleware integrations among Salesforce, Chargebee, Stripe, and NetSuite | Director of IT |
| Looker / BigQuery | Revenue analytics, MRR/ARR dashboards, deferred revenue waterfall reporting | FP&A |
| Okta | Identity and access management for all systems above | CISO |

At a high level, the end-to-end process operates as follows:

1. **Contracting:** Sales executes an MSA and Order Form via DocuSign. Executed contracts are stored in Salesforce and mirrored to a controlled SharePoint legal repository.
2. **Provisioning:** Upon countersignature, Revenue Operations creates or updates the subscription record in Chargebee, mapping plan, seats, price, billing frequency, and service start date. A dual-control checklist is completed before the subscription is activated.
3. **Billing:** Chargebee automatically generates invoices on the contractual billing cadence (predominantly monthly in advance). Invoice PDFs are delivered electronically to the customer billing contact.
4. **Cash collection:** Customers pay via Stripe (card/ACH) or via wire/check recorded manually in NetSuite. Stripe settlement reports are reconciled daily to Chargebee and NetSuite.
5. **Revenue recognition & deferred revenue:** NetSuite deferred revenue schedules amortize prepaid subscription amounts into revenue on a straight-line basis over the service period, consistent with ASC 606 (series guidance / stand-ready obligation). Monthly journal entries are reviewed and approved by the Assistant Controller and Controller.
6. **Modifications:** Mid-term upgrades, downgrades, seat changes, and cancellations are processed in Chargebee with automated proration. Material credits and non-standard amendments require Controller approval.
7. **Period-close:** FP&A and Accounting prepare an MRR rollforward, deferred revenue waterfall, and revenue flux analysis as part of the monthly close package reviewed by the CFO.

## 1.4 Prior-Year Audit Observations and Carryforward Matters

During the FY2024 audit, the engagement team identified two control deficiencies within the revenue cycle that were communicated to management and those charged with governance as **significant deficiencies** (not material weaknesses):

1. **SD-2024-03 — Incomplete evidence of dual review on non-standard discount approvals above 25%.** In 3 of 25 samples, the secondary approver's electronic signature timestamp in Salesforce CPQ was missing, although email evidence suggested approval had occurred. Management remediated by enforcing mandatory second-approver fields and blocking quote finalization without both approvals. Remediation was completed in Q2 2025; we tested operating effectiveness during interim and rollforward procedures in FY2025.
2. **SD-2024-07 — Timeliness of deferred revenue schedule uploads after annual-prepaid invoice issuance.** Two Enterprise annual invoices in November–December 2024 were booked to deferred revenue one business day late relative to the Company's stated close calendar. Management automated the Chargebee-to-NetSuite deferred revenue schedule creation via Workato in March 2025. We tested the automated control and complementary user controls in FY2025.

No material weaknesses related to the revenue cycle were reported in FY2024. There were no restatements of previously issued financial statements.

## 1.5 Scope of This Workpaper

This workpaper documents the engagement team's understanding of the entity and its environment as it relates to subscription revenue and deferred revenue; the risk assessment performed under PCAOB AS 2110 / AS 2201; the identification of **50 key control activities** within the revenue cycle; the design of control testing procedures; sample selection methodology and selected samples; detailed testing results; analysis of exceptions identified; and the overall conclusion on the design and operating effectiveness of controls relevant to the significant accounts addressed herein.

Substantive audit procedures over revenue and deferred revenue (including substantive analytical procedures, tests of details over contract completeness, cutoff testing, and deferred revenue rollforward substantiation) are documented in separate workpapers WP-REV-SUB-001 et seq. and are cross-referenced where relevant. This workpaper focuses on **controls testing** in support of the integrated audit opinion on internal control over financial reporting and, where controls reliance is planned, in support of the nature, timing, and extent of substantive procedures.

## 1.6 Key Personnel Interviewed During Walkthroughs

| Name | Title | Areas Covered | Date(s) |
|------|-------|---------------|---------|
| Alicia Nguyen | Chief Financial Officer | Tone at the top, close process, ASC 606 policy | Jul 22, 2025; Jan 18, 2026 |
| Marcus Bell | Controller | Billing, deferred revenue, journal entry controls | Jul 23–24, 2025; Jan 19, 2026 |
| Sofia Ramirez | Assistant Controller | Revenue recognition entries, reconciliations | Jul 24, 2025; Jan 20, 2026 |
| Derek Cho | Director of Revenue Operations | CPQ, Chargebee provisioning, pricing governance | Jul 25, 2025 |
| Hannah Ortiz | Billing Operations Manager | Invoice generation, dunning, credits | Jul 25, 2025; Oct 14, 2025 |
| Priya Shah | Director of IT | Access, change management, integrations | Jul 28, 2025; Oct 15, 2025 |
| Liam Foster | CISO | Okta, SOD, cybersecurity relevant to ICFR | Jul 28, 2025 |
| Elena Brooks | VP Sales Operations | Contract execution, discount approvals | Jul 29, 2025 |
| Nathan Kim | FP&A Manager | MRR/ARR reporting, flux analysis | Jul 30, 2025; Jan 21, 2026 |

Walkthroughs were performed for each major transaction flow (new logo subscription, expansion/upgrade, contraction/downgrade, cancellation/churn, monthly billing run, cash application, deferred revenue amortization, and period-end close). We obtained screenshots, system configuration extracts, sample documents, and narratives, which are filed in WP-REV-WT-001 through WP-REV-WT-008.

---

# 2. RISK ASSESSMENT
**Workpaper Reference: WP-REV-RA**

## 2.1 Objective of the Risk Assessment

Consistent with PCAOB AS 2110 (*Identifying and Assessing Risks of Material Misstatement*) and AS 2201 (*An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of Financial Statements*), the engagement team performed a risk assessment over the subscription revenue and deferred revenue significant accounts to identify (a) risks of material misstatement at the assertion level, including fraud risks; (b) whether any risks are significant risks requiring special audit consideration; and (c) the controls that address those risks, including whether such controls are precise enough to prevent or detect material misstatements on a timely basis.

## 2.2 Inherent Risk Factors Specific to CloudMeridian's SaaS Model

The following inherent risk factors were identified and evaluated:

### 2.2.1 Complexity of ASC 606 Application

Although CloudMeridian's standard offering is a single performance obligation (stand-ready access to Meridian Insights over the subscription term), several fact patterns introduce judgment and complexity:

- **Multi-element arrangements:** Occasional bundling of implementation services with subscriptions requires allocation of the transaction price based on standalone selling prices (SSP). Management maintains an SSP analysis updated annually.
- **Material rights:** Multi-year contracts with renewal options at discounted rates may contain material rights requiring deferral of a portion of the transaction price.
- **Variable consideration:** Usage-based overage fees (API call overages on Enterprise Plus) introduce estimation uncertainty, although historically such amounts have been less than 1.5% of subscription revenue.
- **Contract modifications:** Mid-term seat expansions and plan upgrades require determination of whether the modification is treated as a separate contract, a termination of the old contract and creation of a new contract, or a prospective adjustment under ASC 606-10-25-12 through 25-13.

### 2.2.2 Volume and Homogeneity of Monthly Billing Transactions

With 500 customers and predominantly monthly billing, the Company generates approximately 5,400–6,000 subscription invoices per year (including proration invoices for mid-cycle changes). The high volume of relatively homogeneous transactions elevates the importance of automated application controls within Chargebee and NetSuite, and correspondingly elevates IT general control (ITGC) risk if those automated controls are to be relied upon.

### 2.2.3 Deferred Revenue Cutoff and Completeness

Because cash is collected in advance, the primary financial reporting risk for prepaid amounts is **incomplete or inaccurate deferral** (i.e., premature revenue recognition) and **inaccurate amortization** of deferred balances into revenue. Cutoff errors around month-end and year-end are inherently elevated given the concentration of Enterprise annual renewals in November and December.

### 2.2.4 Pressure on SaaS Metrics and Fraud Risk Considerations

Management reports ARR, MRR, NDR, and GDR to the Board and to lenders under the Company's revolving credit facility covenants. While these metrics are non-GAAP, they are closely correlated with recognized subscription revenue and deferred revenue. We identified a **fraud risk related to revenue recognition** (presumed under AS 2401) focusing on the potential for premature recognition of subscription revenue, manipulation of deferred revenue amortization timing, and backdating of contract start dates to pull revenue into the current period. We also considered the risk of management override of controls over journal entries affecting revenue and deferred revenue.

### 2.2.5 System Integration and Data Integrity Risk

Revenue data flows across Salesforce → Chargebee → Stripe/NetSuite via Workato. Incomplete webhook processing, failed integration jobs, or unauthorized changes to mapping tables could result in omitted invoices, duplicated billings, or misstated deferred revenue schedules. This elevates inherent risk around completeness and accuracy of recorded revenue and contract liabilities.

### 2.2.6 Customer Concentration and Credit Risk

The top 20 customers represent approximately 31% of ARR. While concentration is moderate, failure to identify nonpayment or disputed invoices for large accounts could affect both revenue (if collectibility is not probable under ASC 606 Step 1) and the allowance for credit losses. Collectibility risk is assessed as moderate given historical write-offs below 0.4% of revenue.

## 2.3 Assertion-Level Risk Assessment

The engagement team assessed inherent risk (IR), control risk (CR) before considering the results of controls testing, and the resulting risk of material misstatement (RMM) for each relevant assertion:

| Account / Disclosure | Assertion | Inherent Risk | Key Risk Drivers | Significant Risk? | Fraud Risk? | Planned Controls Reliance |
|----------------------|-----------|---------------|------------------|-------------------|-------------|---------------------------|
| Subscription revenue | Occurrence | High | Pressure on growth metrics; start-date manipulation | Yes | Yes | Yes — extensive |
| Subscription revenue | Completeness | Moderate–High | Failed billing runs; integration failures | Yes | No | Yes — extensive |
| Subscription revenue | Accuracy | High | Pricing errors; SSP allocation; proration | Yes | No | Yes — extensive |
| Subscription revenue | Cutoff | High | Month-end/year-end timing; annual renewals cluster | Yes | Yes | Yes — extensive |
| Subscription revenue | Classification | Low–Moderate | Services vs. subscription mix | No | No | Yes — limited |
| Subscription revenue | Presentation & disclosure | Moderate | ASC 606 disclosures; remaining performance obligations | No | No | Yes — limited |
| Deferred revenue | Completeness | High | Prepaid invoices not deferred | Yes | Yes | Yes — extensive |
| Deferred revenue | Existence / obligations | Moderate–High | Overstated deferrals; stale balances | Yes | No | Yes — extensive |
| Deferred revenue | Valuation / allocation | High | Amortization schedule errors; modification accounting | Yes | Yes | Yes — extensive |
| Deferred revenue | Rights & obligations | Moderate | Contractual terms vs. recorded liability | No | No | Yes — moderate |
| Deferred revenue | Presentation | Moderate | Current vs. non-current classification | No | No | Yes — moderate |
| Accounts receivable | Existence | Moderate | Fictitious invoices | No | No | Yes — moderate |
| Accounts receivable | Valuation | Moderate | Allowance estimation | No | No | Yes — moderate |
| Accounts receivable | Completeness | Moderate | Unrecorded billings | No | No | Yes — moderate |

## 2.4 Significant Risks and Planned Responses

The following risks were designated as **significant risks** requiring special audit consideration under AS 2110.71–.74:

| Risk ID | Description | Assertions | Primary Controls Addressing Risk | Substantive Response Highlights |
|--------|-------------|------------|----------------------------------|---------------------------------|
| SR-REV-01 | Premature recognition of subscription revenue / manipulation of service start dates | Occurrence, Cutoff | CA-01, CA-02, CA-07, CA-12, CA-18, CA-22, CA-35 | Contract-to-revenue vouching; start-date corroboration to provisioning logs; cutoff testing ±5 days around year-end |
| SR-REV-02 | Incomplete recording of deferred revenue for prepaid invoices | Completeness (DR), Cutoff | CA-15, CA-16, CA-17, CA-28, CA-29, CA-41 | Deferred revenue rollforward; invoice-to-schedule tracing for annual/quarterly billers; search for unrecorded liabilities style procedures on prepaid cash |
| SR-REV-03 | Inaccurate amortization of deferred revenue (including modification accounting errors) | Accuracy, Valuation | CA-19, CA-20, CA-21, CA-30, CA-31, CA-42 | Recalculation of amortization for samples; modification accounting reperformance; analytical review of DR waterfall |
| SR-REV-04 | Pricing and billing inaccuracies (wrong plan price, seats, discounts) | Accuracy | CA-03, CA-04, CA-05, CA-08, CA-09, CA-23, CA-24 | Price testing to approved rate cards / Order Forms; invoice recalculation |
| SR-REV-05 | Management override via manual journal entries to revenue or deferred revenue | All | CA-36, CA-37, CA-38, CA-39, CA-50 | JE testing focused on revenue/DR accounts; examine non-standard entries; inquiry and retrospective review |
| SR-REV-06 | Incomplete revenue due to failed system integrations or suppressed invoices | Completeness | CA-10, CA-11, CA-25, CA-26, CA-43, CA-44 | Billing run completeness; integration exception log review; customer-to-invoice matching |

## 2.5 Fraud Risk Discussion (AS 2401)

The engagement team held a fraud brainstorming session on July 18, 2025 (attendance documented in WP-ADM-FR-001). Specific fraud scenarios brainstormed for the revenue cycle included:

1. Backdating Order Form effective dates or Chargebee subscription start dates to recognize an extra month of revenue in the current period.
2. Releasing deferred revenue amortization schedules early (accelerating recognition) through unauthorized NetSuite schedule edits.
3. Recording manual credit memos or debit memos without commercial substance to smooth revenue.
4. Suppressing churn/cancellation processing near period-end to inflate ending MRR and recognized revenue.
5. Inflating seat counts on invoices without corresponding Order Form amendments.
6. Round-trip arrangements or side letters granting concessions not reflected in the accounting system.

Planned fraud-related procedures include: journal entry testing with a revenue/DR focus; examination of revenue recorded near period-end; inquiry of Sales, Legal, and Billing personnel regarding side letters; review of credit memo populations; comparison of Salesforce closed-won dates to Chargebee start dates; and evaluation of unusual spikes in MRR not explained by known new logos or expansions.

## 2.6 Control Environment and Entity-Level Controls Relevant to Revenue

We evaluated entity-level controls (ELCs) under the COSO 2013 framework as they pertain to the revenue cycle. Relevant ELCs include:

- **Control environment:** Written code of conduct; Board/Audit Committee oversight of financial reporting; segregation of duties between Sales (quota-bearing) and Revenue Accounting; CFO and Controller competency and tenure.
- **Risk assessment:** Annual ASC 606 accounting policy review; formal risk register maintained by Internal Audit (co-sourced); disclosure committee process.
- **Control activities:** The 50 process-level control activities catalogued in Section 3.
- **Information & communication:** Monthly close checklist; ASC 606 desk procedures; system access reviews.
- **Monitoring:** Internal Audit reviews of billing and deferred revenue (performed Q3 2025); management's own SOX testing program with 40% coverage overlap to our key controls (we evaluated management's testing for competence and objectivity under AS 2201.16–.19 and used it to moderate—but not eliminate—our independent testing extent for certain lower-risk controls).

## 2.7 IT General Controls Dependence

Because many of the 50 control activities are automated or IT-dependent manual controls, we identified dependence on ITGCs over Salesforce, Chargebee, Stripe, NetSuite, Workato, and Okta in the following domains: logical access (provisioning, modification, termination, periodic access reviews, privileged access); change management (application and interface changes); and computer operations (job monitoring, interface failure handling). ITGC testing is documented in WP-ITGC-001 through WP-ITGC-045. **Preliminary conclusion (subject to final partner review): ITGCs for the in-scope systems were designed and operating effectively for FY2025**, with two low-severity deficiencies related to timely access termination (average 3.2 days vs. policy of 1 business day) that were assessed as not impacting the reliability of automated revenue controls due to compensating detective reviews and lack of inappropriate access exploitation. Cross-reference: WP-ITGC-CON.

## 2.8 Summary Risk Conclusion Leading to Controls Testing Strategy

Given high inherent risk across multiple assertions, the presence of six significant risks (including fraud risks), material deferred revenue balances, and a high volume of monthly subscription transactions, the engagement team determined that a **controls reliance strategy with extensive testing of 50 key control activities** is appropriate and necessary both for the ICFR opinion and to support reduced substantive sample sizes for tests of details. The controls catalog, testing procedures, sampling approach, results, exceptions, and conclusion follow in Sections 3 through 7.

---

# 3. CONTROL TESTING PROCEDURES
**Workpaper Reference: WP-REV-CTP**

## 3.1 Control Catalog Overview

The engagement team identified **50 key control activities** (CA-01 through CA-50) that address the risks of material misstatement described in Section 2. Controls were mapped to COSO principles, financial statement assertions, and the significant risks they mitigate. Each control was evaluated for **design effectiveness** (whether the control, if operated as prescribed by persons with appropriate authority and competence, satisfies the control objective) and **operating effectiveness** (whether the control operated as designed throughout the period of reliance).

Testing approach legend:

| Approach Code | Meaning | Typical Evidence |
|---------------|---------|------------------|
| IE | Inquiry & Examination of documentation | Approvals, checklists, emails, tickets |
| O | Observation | Observe control performance in real time |
| R | Reperformance | Independently reperform the control |
| CA | Computer-assisted / system configuration testing | System config extracts, automated rule tests |
| DT | Data testing / exception report interrogation | Full-population exception scans |

Frequency legend: C = Continuous/automated; D = Daily; W = Weekly; M = Monthly; Q = Quarterly; A = Annual; E = Event-driven.

## 3.2 Detailed Control Activities and Testing Procedures

For each of the 50 controls below, we document: control description; control owner; frequency; type (preventive/detective; manual/automated/IT-dependent manual); assertions addressed; risks addressed; design testing procedures; and operating effectiveness testing procedures.

### CA-01 — MSA and Order Form Execution Prior to Service Activation

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-01 |
| **Control Title** | MSA and Order Form Execution Prior to Service Activation |
| **Control Description** | Prior to activation of any new subscription in Chargebee, Revenue Operations verifies that a fully executed MSA and Order Form (DocuSign completed certificate of completion) are attached in Salesforce and that the legal entity name, billing entity, and effective date on the Order Form agree to the Chargebee subscription record. |
| **Control Owner** | Director of Revenue Operations |
| **Frequency** | E |
| **Control Type** | Preventive; IT-dependent manual |
| **Assertions Addressed** | Occurrence, Cutoff, Rights & Obligations |
| **Risks Addressed** | SR-REV-01 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect written desk procedure REV-SOP-02; walk through one new logo deal from DocuSign completion to Chargebee activation; confirm system enforces attachment checklist field.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Select a sample of new subscription activations during the period; for each, inspect executed MSA/Order Form, DocuSign certificate, Salesforce attachment, and Chargebee activation timestamp; verify activation did not precede execution.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-02 — Service Start Date Validation Against Contract Effective Date

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-02 |
| **Control Title** | Service Start Date Validation Against Contract Effective Date |
| **Control Description** | Chargebee subscription start dates are required to equal the Order Form service start date. A Workato validation job compares Salesforce Order Form start date to Chargebee start date daily and routes exceptions to Revenue Operations for resolution within two business days. |
| **Control Owner** | Director of Revenue Operations |
| **Frequency** | D |
| **Control Type** | Detective; Automated with manual follow-up |
| **Assertions Addressed** | Occurrence, Cutoff |
| **Risks Addressed** | SR-REV-01 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect Workato recipe configuration and alerting rules; observe exception queue; verify comparison logic in code/config extract.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Obtain daily exception logs for sample days across the year; verify exceptions were resolved timely; for a sample of activations, reperform date match between Order Form and Chargebee.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-03 — Approved Price List / Rate Card Enforcement in CPQ

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-03 |
| **Control Title** | Approved Price List / Rate Card Enforcement in CPQ |
| **Control Description** | Salesforce CPQ price rules enforce that list prices for each plan and module are drawn from the approved annual rate card. Users cannot override list price downward without triggering the discount approval workflow (CA-04). |
| **Control Owner** | Director of Revenue Operations |
| **Frequency** | C |
| **Control Type** | Preventive; Automated |
| **Assertions Addressed** | Accuracy |
| **Risks Addressed** | SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect CPQ price book configuration; compare to Board-approved rate card for FY2025; attempt (in sandbox) to enter an unauthorized list price.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For a sample of quotes/orders, compare billed unit prices to the approved rate card before discount; verify CPQ price book version IDs in effect during the period.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-04 — Discount Approval Workflow (Tiered)

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-04 |
| **Control Title** | Discount Approval Workflow (Tiered) |
| **Control Description** | Discounts require electronic approval in Salesforce CPQ based on threshold: 0–10% — Sales Manager; 10.01–25% — VP Sales; >25% — CFO. Quotes cannot reach 'Closed Won' without required approvals recorded. |
| **Control Owner** | VP Sales Operations / CFO |
| **Frequency** | E |
| **Control Type** | Preventive; Automated with manual approval |
| **Assertions Addressed** | Accuracy, Occurrence |
| **Risks Addressed** | SR-REV-04, SR-REV-01 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect CPQ approval rule configuration and threshold matrix; walk through a >25% discount deal; confirm hard block on Closed Won without approvals.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Stratify Closed Won deals by discount band; sample from each band; inspect approval records, approver identity/authority, and timestamps preceding Close Won.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-05 — Seat Quantity Agreement Between Order Form and Chargebee

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-05 |
| **Control Title** | Seat Quantity Agreement Between Order Form and Chargebee |
| **Control Description** | Prior to activation, Billing Operations reconciles seat counts (or concurrent user entitlements) on the Order Form to the Chargebee subscription quantity. Differences must be cleared before go-live. |
| **Control Owner** | Billing Operations Manager |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy |
| **Risks Addressed** | SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect activation checklist template; walk through provisioning for a sample Enterprise deal.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled new and expansion activations, compare Order Form quantity to Chargebee quantity and to the first invoice line quantity.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-06 — Customer Master Data Creation Dual Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-06 |
| **Control Title** | Customer Master Data Creation Dual Review |
| **Control Description** | New customer records in NetSuite and Chargebee are created by Billing Operations and reviewed by the Assistant Controller for legal name, billing address, tax exemption status, payment terms, and currency before the first invoice is issued. |
| **Control Owner** | Assistant Controller |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy, Occurrence |
| **Risks Addressed** | SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect customer master form and review checklist; inquire with Assistant Controller regarding review procedures.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample new customers onboarded in the period; inspect evidence of dual review prior to first invoice date.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-07 — Prohibition on Activation Without Credit/Collectibility Assessment

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-07 |
| **Control Title** | Prohibition on Activation Without Credit/Collectibility Assessment |
| **Control Description** | For customers with contracted ARR above $50,000, Credit assesses collectibility (ASC 606 Step 1) and documents approval in Salesforce before provisioning. Below threshold, automated Stripe payment method validation is required for monthly card/ACH customers. |
| **Control Owner** | Controller / Credit Analyst |
| **Frequency** | E |
| **Control Type** | Preventive; IT-dependent manual |
| **Assertions Addressed** | Occurrence, Valuation (AR) |
| **Risks Addressed** | SR-REV-01 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect credit policy; walk through one >$50k deal and one card-billed SMB deal.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample new logos above and below threshold; verify credit approval or payment method validation existed pre-activation.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-08 — Annual Rate Card Approval by CFO and Board Finance Committee

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-08 |
| **Control Title** | Annual Rate Card Approval by CFO and Board Finance Committee |
| **Control Description** | The annual SaaS rate card is prepared by Revenue Operations, approved by the CFO, and ratified by the Board Finance Committee before January 1 of each fiscal year. Mid-year rate changes require CFO approval. |
| **Control Owner** | CFO |
| **Frequency** | A / E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy |
| **Risks Addressed** | SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect FY2025 rate card package, CFO approval, and Finance Committee minutes.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Verify approved rate card was the one loaded to CPQ (CA-03); inspect any mid-year change approvals.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-09 — SSP Analysis Annual Update and Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-09 |
| **Control Title** | SSP Analysis Annual Update and Review |
| **Control Description** | Finance updates the standalone selling price analysis for subscription tiers and implementation services annually. The Controller and CFO review and approve the SSP memo used for transaction price allocation in multi-element arrangements. |
| **Control Owner** | Controller / CFO |
| **Frequency** | A |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy, Valuation |
| **Risks Addressed** | SR-REV-03, SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect FY2025 SSP memo, supporting data, and approvals.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Reperform selected SSP calculations; verify approved SSP was applied to a sample of multi-element contracts.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-10 — Monthly Billing Run Completeness Checklist

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-10 |
| **Control Title** | Monthly Billing Run Completeness Checklist |
| **Control Description** | On the first business day of each month, Billing Operations executes the Chargebee recurring billing run and completes a checklist evidencing: (a) expected invoice count vs. active subscriptions; (b) investigation of exclusions; (c) reconciliation of billing run total to MRR subledger. |
| **Control Owner** | Billing Operations Manager |
| **Frequency** | M |
| **Control Type** | Detective; IT-dependent manual |
| **Assertions Addressed** | Completeness, Accuracy |
| **Risks Addressed** | SR-REV-06, SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect checklist template and Chargebee billing run configuration; observe one billing run.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For a sample of months, inspect completed checklists, reconciling differences, and evidence of review by Assistant Controller.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-11 — Integration Failure Monitoring — Workato Job Alerts

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-11 |
| **Control Title** | Integration Failure Monitoring — Workato Job Alerts |
| **Control Description** | Workato integration jobs (Salesforce↔Chargebee, Chargebee↔NetSuite, Stripe↔NetSuite) are configured with failure alerts to IT Operations and Billing. Failed jobs must be triaged within four business hours and resolved or escalated within one business day. A weekly aging of open integration exceptions is reviewed by the Director of IT and Controller. |
| **Control Owner** | Director of IT / Controller |
| **Frequency** | C / W |
| **Control Type** | Detective; Automated with manual follow-up |
| **Assertions Addressed** | Completeness, Accuracy |
| **Risks Addressed** | SR-REV-06 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect alert configuration, on-call runbooks, and weekly aging template.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample failed job incidents across the year; verify timely triage/resolution; inspect weekly aging reviews for sample weeks.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-12 — Contract Amendment Controls for Expansions and Contractions

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-12 |
| **Control Title** | Contract Amendment Controls for Expansions and Contractions |
| **Control Description** | Mid-term expansions and contractions require an executed Order Form amendment (or click-through in-app expansion for seat adds under Master Terms). Revenue Operations updates Chargebee only after amendment execution; proration is system-calculated. |
| **Control Owner** | Director of Revenue Operations |
| **Frequency** | E |
| **Control Type** | Preventive; IT-dependent manual |
| **Assertions Addressed** | Occurrence, Accuracy, Cutoff |
| **Risks Addressed** | SR-REV-01, SR-REV-03, SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect amendment SOP; walk through one expansion and one contraction.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample expansions/contractions; vouch to amendments; verify Chargebee change timestamp after execution; recalculate proration.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-13 — Cancellation / Churn Processing Dual Control

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-13 |
| **Control Title** | Cancellation / Churn Processing Dual Control |
| **Control Description** | Customer cancellations require written notice per MSA, a cancellation ticket in Salesforce, and dual approval (Customer Success Manager + Revenue Operations) before Chargebee status is set to 'Cancelled.' Access is revoked at term end; deferred revenue remaining is evaluated for breakage/recognition per policy. |
| **Control Owner** | Revenue Operations / Customer Success |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Completeness, Cutoff, Accuracy |
| **Risks Addressed** | SR-REV-01, SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect cancellation SOP and system status workflows.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample cancellations; inspect notice, ticket, dual approvals, Chargebee status change, and deferred revenue treatment.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-14 — Side Letter and Non-Standard Terms Legal Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-14 |
| **Control Title** | Side Letter and Non-Standard Terms Legal Review |
| **Control Description** | Any side letter or non-standard MSA term with revenue recognition implications must be reviewed by Legal and Accounting (ASC 606 specialist) before deal close. A mandatory Salesforce field flags non-standard terms. |
| **Control Owner** | Legal / Controller |
| **Frequency** | E |
| **Control Type** | Preventive; IT-dependent manual |
| **Assertions Addressed** | Occurrence, Completeness, Presentation |
| **Risks Addressed** | SR-REV-01, SR-REV-05 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect policy and Salesforce flag configuration; inquire with Legal regarding FY2025 volume.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Obtain population of flagged non-standard deals; sample and inspect Legal/Accounting review evidence; search email/legal files for unflagged side letters (fraud-related).
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-15 — Automated Deferred Revenue Schedule Creation on Prepaid Invoices

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-15 |
| **Control Title** | Automated Deferred Revenue Schedule Creation on Prepaid Invoices |
| **Control Description** | Upon issuance of a prepaid subscription invoice in Chargebee and sync to NetSuite, Workato automatically creates a NetSuite deferred revenue amortization schedule matching the service period and invoice amount (net of taxes). |
| **Control Owner** | Controller |
| **Frequency** | C |
| **Control Type** | Preventive; Automated |
| **Assertions Addressed** | Completeness, Accuracy (Deferred Revenue) |
| **Risks Addressed** | SR-REV-02, SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect Workato recipe and NetSuite schedule templates; test in sandbox with sample invoice payloads.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled prepaid invoices (monthly, quarterly, annual), verify a schedule was created same-day for the correct amount and period; scan population for prepaid invoices lacking schedules (CA/DT).
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-16 — Daily Reconciliation of Chargebee Invoices to NetSuite AR/DR

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-16 |
| **Control Title** | Daily Reconciliation of Chargebee Invoices to NetSuite AR/DR |
| **Control Description** | Each business day, Billing Operations reconciles the prior day's Chargebee invoice register to NetSuite invoice and deferred revenue creations. Differences are logged and cleared within two business days. |
| **Control Owner** | Billing Operations Manager |
| **Frequency** | D |
| **Control Type** | Detective; IT-dependent manual |
| **Assertions Addressed** | Completeness, Accuracy |
| **Risks Addressed** | SR-REV-02, SR-REV-06 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect reconciliation template and clearance SLA; observe performance on a sample day.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample business days across the year; inspect reconciliations, differences, and timely clearance.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-17 — Monthly Deferred Revenue Subledger-to-GL Reconciliation

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-17 |
| **Control Title** | Monthly Deferred Revenue Subledger-to-GL Reconciliation |
| **Control Description** | Monthly, the Assistant Controller reconciles the NetSuite deferred revenue subledger (sum of open schedules) to the GL deferred revenue control accounts (current and non-current). The Controller reviews and signs off within the close calendar (by BD+4). |
| **Control Owner** | Assistant Controller / Controller |
| **Frequency** | M |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Completeness, Existence, Valuation (DR) |
| **Risks Addressed** | SR-REV-02, SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect reconciliation template, close calendar, and review requirements.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled months (including year-end), inspect reconciliations, reconciling items, and Controller sign-off timing.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-18 — Revenue Recognition Journal Entry Review and Approval

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-18 |
| **Control Title** | Revenue Recognition Journal Entry Review and Approval |
| **Control Description** | Monthly automated and manual revenue recognition journal entries (amortization of deferred revenue, usage overage accruals, SSP allocations) are prepared by Accounting and reviewed/approved by the Assistant Controller (entries <$100k impact) or Controller (entries ≥$100k or non-standard). |
| **Control Owner** | Assistant Controller / Controller |
| **Frequency** | M / E |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Occurrence, Accuracy, Cutoff |
| **Risks Addressed** | SR-REV-01, SR-REV-03, SR-REV-05 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect JE policy thresholds and NetSuite approval workflow configuration.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample revenue-related JEs across the year stratified by size/type; inspect preparer/approver segregation, supporting schedules, and approval prior to posting.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-19 — Deferred Revenue Amortization Accuracy Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-19 |
| **Control Title** | Deferred Revenue Amortization Accuracy Review |
| **Control Description** | Monthly, FP&A generates a deferred revenue waterfall from NetSuite and Accounting recalculates amortization for a judgmental sample of schedules (all annual prepaids plus random monthly/quarterly). Differences above $500 are investigated. |
| **Control Owner** | Assistant Controller / FP&A |
| **Frequency** | M |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Valuation, Accuracy |
| **Risks Addressed** | SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect sampling methodology memo and recalculation workbook template.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled months, inspect recalculation workbooks; reperform a subset; verify investigation of differences.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-20 — Contract Modification Accounting Checklist

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-20 |
| **Control Title** | Contract Modification Accounting Checklist |
| **Control Description** | For each mid-term modification with ARR impact >$5,000, Accounting completes an ASC 606 modification checklist determining separate contract vs. prospective treatment and documents the effect on remaining deferred revenue and future recognition. |
| **Control Owner** | Assistant Controller |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy, Valuation, Cutoff |
| **Risks Addressed** | SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect checklist aligned to ASC 606-10-25-12–13; walk through one complex modification.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample modifications >$5k ARR impact; inspect completed checklists, calculations, and approvals.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-21 — Usage Overage Accrual and True-Up Control

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-21 |
| **Control Title** | Usage Overage Accrual and True-Up Control |
| **Control Description** | Monthly, Billing extracts usage overage reports from the product telemetry warehouse, computes billable overages per contract rate cards, and accrues revenue with a deferred-to-AR true-up upon invoicing. Controller reviews the overage accrual. |
| **Control Owner** | Billing Operations / Controller |
| **Frequency** | M |
| **Control Type** | Detective; IT-dependent manual |
| **Assertions Addressed** | Completeness, Accuracy, Cutoff |
| **Risks Addressed** | SR-REV-04, SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect overage calculation methodology and review evidence requirements.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled months, reperform overage calculations for sampled customers; inspect Controller review.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-22 — Period-End Cutoff Calendar and Soft Close of Billing

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-22 |
| **Control Title** | Period-End Cutoff Calendar and Soft Close of Billing |
| **Control Description** | Accounting publishes a month-end cutoff calendar. Chargebee billing for the following service month is soft-closed after BD+1 pending cutoff review. Late activations requiring current-month revenue are approved by the Controller with documented business rationale. |
| **Control Owner** | Controller |
| **Frequency** | M |
| **Control Type** | Preventive; IT-dependent manual |
| **Assertions Addressed** | Cutoff |
| **Risks Addressed** | SR-REV-01 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect cutoff calendars for interim and year-end; inspect soft-close configuration.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled month-ends including Dec 31, inspect cutoff approvals for late activations and evaluate revenue period assigned.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-23 — Credit Memo Authorization

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-23 |
| **Control Title** | Credit Memo Authorization |
| **Control Description** | Credit memos require dual approval: Billing Operations prepares; Assistant Controller approves credits ≤$5,000; Controller approves >$5,000; CFO approves >$25,000. Credits linked to concessions with ASC 606 implications are routed to the modification checklist (CA-20). |
| **Control Owner** | Controller / CFO |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy, Occurrence, Completeness |
| **Risks Addressed** | SR-REV-05, SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect credit memo policy and NetSuite approval workflow.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample credit memos stratified by amount; verify approvals and linkage to commercial support; scan for unauthorized credits (DT).
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-24 — Invoice Accuracy Spot Checks Prior to Customer Delivery

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-24 |
| **Control Title** | Invoice Accuracy Spot Checks Prior to Customer Delivery |
| **Control Description** | For the first invoice on every new logo and for all invoices >$25,000, Billing Operations performs a three-way match among Order Form, Chargebee subscription, and invoice PDF before release. |
| **Control Owner** | Billing Operations Manager |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy |
| **Risks Addressed** | SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect three-way match checklist; observe performance for a new logo invoice.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample new logo first invoices and invoices >$25k; inspect match evidence and corrections made prior to release.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-25 — Active Subscription-to-Invoice Coverage Report

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-25 |
| **Control Title** | Active Subscription-to-Invoice Coverage Report |
| **Control Description** | Weekly, an automated Looker report lists active Chargebee subscriptions without an invoice in the expected billing window. Billing investigates and resolves within three business days. Assistant Controller reviews aging weekly. |
| **Control Owner** | Billing Operations / Assistant Controller |
| **Frequency** | W |
| **Control Type** | Detective; Automated with manual follow-up |
| **Assertions Addressed** | Completeness |
| **Risks Addressed** | SR-REV-06 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect Looker report logic/SQL; verify schedule and distribution list.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample weeks; inspect reports, resolution evidence, and review sign-offs; independently run the SQL for a sample week (R).
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-26 — Stripe Settlement Reconciliation

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-26 |
| **Control Title** | Stripe Settlement Reconciliation |
| **Control Description** | Daily, Cash Applications reconciles Stripe payouts to Chargebee payment records and NetSuite cash receipts. Unmatched items >$100 age and are cleared within three business days; monthly reconciliation is reviewed by the Treasurer. |
| **Control Owner** | Cash Applications / Treasurer |
| **Frequency** | D / M |
| **Control Type** | Detective; IT-dependent manual |
| **Assertions Addressed** | Completeness, Accuracy, Existence (Cash/AR) |
| **Risks Addressed** | SR-REV-06 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect reconciliation procedures and Stripe report mapping.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample days and months; inspect reconciliations and clearance of unmatched items.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-27 — Manual Cash Application Dual Review (Wires/Checks)

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-27 |
| **Control Title** | Manual Cash Application Dual Review (Wires/Checks) |
| **Control Description** | Non-Stripe receipts are applied by Cash Applications and reviewed daily by a second Accounting team member to ensure application to the correct customer/invoice and correct revenue vs. deferred revenue vs. deposit treatment. |
| **Control Owner** | Cash Applications Supervisor |
| **Frequency** | D |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Accuracy, Completeness |
| **Risks Addressed** | SR-REV-02 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect cash application SOP and review evidence format.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample manual cash application days; inspect reviewer evidence and test a subsample of applications to remittances.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-28 — Prepaid Cash Search / Unapplied Cash Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-28 |
| **Control Title** | Prepaid Cash Search / Unapplied Cash Review |
| **Control Description** | Weekly, Accounting reviews unapplied cash and customer deposit balances to identify prepaid subscription amounts not yet linked to invoices/schedules, ensuring deferred revenue completeness. |
| **Control Owner** | Assistant Controller |
| **Frequency** | W |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Completeness (DR) |
| **Risks Addressed** | SR-REV-02 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect unapplied cash aging report and review checklist.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample weeks; inspect reviews and disposition of aged unapplied items related to subscriptions.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-29 — Annual Prepaid Invoice Deferred Revenue Completeness Scan

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-29 |
| **Control Title** | Annual Prepaid Invoice Deferred Revenue Completeness Scan |
| **Control Description** | Quarterly, Accounting runs a data analytics routine identifying invoices with billing frequency = annual or quarterly and service period >31 days that lack an open deferred revenue schedule or have schedule amounts differing by >$1 from invoice net. |
| **Control Owner** | Assistant Controller / Internal Audit |
| **Frequency** | Q |
| **Control Type** | Detective; Automated analytics with manual follow-up |
| **Assertions Addressed** | Completeness, Accuracy (DR) |
| **Risks Addressed** | SR-REV-02 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect script/logic and threshold rationale; observe Q3 2025 run.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly run outputs for all four quarters; verify investigation of exceptions; reperform script at year-end (R).
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-30 — Current vs. Non-Current Deferred Revenue Classification Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-30 |
| **Control Title** | Current vs. Non-Current Deferred Revenue Classification Review |
| **Control Description** | At each quarter-end, FP&A and Accounting recompute the portion of deferred revenue to be recognized within 12 months based on amortization schedules and adjust current/non-current classification. Controller reviews. |
| **Control Owner** | FP&A / Controller |
| **Frequency** | Q |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Presentation, Valuation |
| **Risks Addressed** | SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect classification workbook methodology.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For each quarter-end including year-end, inspect classification workbook, recomputation, and Controller review.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-31 — Stale Deferred Revenue Balance Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-31 |
| **Control Title** | Stale Deferred Revenue Balance Review |
| **Control Description** | Quarterly, Accounting reviews deferred revenue schedules with no amortization activity for >60 days or remaining term past contract end date. Anomalous balances are investigated for breakage, contract termination, or system error. |
| **Control Owner** | Assistant Controller |
| **Frequency** | Q |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Existence, Valuation (DR) |
| **Risks Addressed** | SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect stale balance report definition and investigation log template.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly stale balance reviews; verify disposition of flagged schedules.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-32 — AR Aging Review and Allowance for Credit Losses

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-32 |
| **Control Title** | AR Aging Review and Allowance for Credit Losses |
| **Control Description** | Monthly, the Controller reviews AR aging, customer correspondence on disputes, and estimates the CECL allowance. CFO approves the allowance journal entry. |
| **Control Owner** | Controller / CFO |
| **Frequency** | M |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Valuation (AR) |
| **Risks Addressed** | N/A (related account) |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect CECL policy and allowance methodology memo.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled months including year-end, inspect aging review notes, allowance model, and CFO approval.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-33 — Dunning Process and Revenue Implications

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-33 |
| **Control Title** | Dunning Process and Revenue Implications |
| **Control Description** | Chargebee dunning is configured for past-due monthly subscriptions. After defined retry attempts, accounts are marked past due; Customer Success and Accounting jointly assess whether continued recognition remains appropriate under collectibility guidance; service suspension rules are documented. |
| **Control Owner** | Billing / Controller |
| **Frequency** | C / E |
| **Control Type** | Detective; Automated with manual assessment |
| **Assertions Addressed** | Occurrence, Valuation |
| **Risks Addressed** | SR-REV-01 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect dunning configuration and collectibility assessment SOP.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample accounts entering late-stage dunning; inspect collectibility assessments and accounting treatment.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-34 — Tax Coding and Jurisdiction Review on Invoices

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-34 |
| **Control Title** | Tax Coding and Jurisdiction Review on Invoices |
| **Control Description** | Sales tax / VAT coding is determined via Chargebee tax engine configuration reviewed quarterly by Tax. Changes to tax rules require Tax Manager approval. Invoice tax amounts are spot-checked monthly. |
| **Control Owner** | Tax Manager |
| **Frequency** | Q / M |
| **Control Type** | Preventive/Detective; IT-dependent manual |
| **Assertions Addressed** | Accuracy, Completeness (tax liability) |
| **Risks Addressed** | SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect tax engine configuration and quarterly review evidence.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly configuration reviews and monthly spot checks for sampled periods.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-35 — Salesforce Closed-Won to Chargebee Provisioning Timeliness KPI

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-35 |
| **Control Title** | Salesforce Closed-Won to Chargebee Provisioning Timeliness KPI |
| **Control Description** | Revenue Operations monitors a KPI that Closed-Won opportunities are provisioned in Chargebee within two business days. Weekly exceptions are reviewed; aging >5 days escalated to the CFO for deals >$25k ARR. |
| **Control Owner** | Director of Revenue Operations |
| **Frequency** | W |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Completeness, Cutoff |
| **Risks Addressed** | SR-REV-01, SR-REV-06 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect KPI dashboard definition and escalation policy.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample weeks; inspect exception lists and escalations; vouch resolution timing.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-36 — Segregation of Duties — Revenue Accounting vs. Sales Operations

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-36 |
| **Control Title** | Segregation of Duties — Revenue Accounting vs. Sales Operations |
| **Control Description** | System roles enforce that individuals with authority to close opportunities in Salesforce cannot post manual JEs to revenue/DR in NetSuite, and individuals who can edit Chargebee prices cannot approve their own NetSuite revenue entries. SOD conflicts are reviewed quarterly. |
| **Control Owner** | CISO / Controller |
| **Frequency** | Q |
| **Control Type** | Preventive; Automated with manual review |
| **Assertions Addressed** | All (fraud mitigation) |
| **Risks Addressed** | SR-REV-05 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect SOD matrix and system role configurations; verify monitoring tool rules.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly SOD conflict reports and mitigation plans; test a sample of user access rights against the matrix (R).
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-37 — Privileged Access Review — NetSuite Revenue Accounts

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-37 |
| **Control Title** | Privileged Access Review — NetSuite Revenue Accounts |
| **Control Description** | Quarterly, the Controller and IT review users with privileged access to create/modify deferred revenue schedules and post to revenue GL accounts. Inappropriate access is removed within five business days. |
| **Control Owner** | Controller / Director of IT |
| **Frequency** | Q |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | All (fraud/ITGC complementary) |
| **Risks Addressed** | SR-REV-05 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect review procedures and evidence retention standards.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly access reviews for all four quarters; verify removal tickets for any access deemed inappropriate.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-38 — Manual Journal Entry Restrictive Policy for Revenue Accounts

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-38 |
| **Control Title** | Manual Journal Entry Restrictive Policy for Revenue Accounts |
| **Control Description** | Manual JEs to subscription revenue and deferred revenue accounts require standardized templates, supporting documentation uploaded to NetSuite, and dual approval. 'Top-side' entries are prohibited without CFO written approval. |
| **Control Owner** | Controller / CFO |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Occurrence, Accuracy, Completeness |
| **Risks Addressed** | SR-REV-05 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect JE policy and NetSuite configuration restricting account posting.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. From the revenue/DR JE population, sample manual entries; inspect templates, support, dual approvals, and any CFO top-side approvals.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-39 — Management Override Monitoring — Unusual Revenue JE Report

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-39 |
| **Control Title** | Management Override Monitoring — Unusual Revenue JE Report |
| **Control Description** | Monthly, Internal Audit / SOX co-source runs an analytics report of revenue and deferred revenue JEs with characteristics indicative of override risk (round amounts, posted on weekends, posted by senior management, near period-end, reversed next period). Controllers investigate flagged items; Audit Committee receives a summary quarterly. |
| **Control Owner** | Internal Audit / Audit Committee |
| **Frequency** | M / Q |
| **Control Type** | Detective; Automated analytics with manual follow-up |
| **Assertions Addressed** | All (fraud) |
| **Risks Addressed** | SR-REV-05 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect analytics rules and reporting packet template.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect monthly flagged-item packets for sampled months; verify investigations; inspect quarterly AC reporting.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-40 — MRR/ARR Rollforward Preparation and CFO Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-40 |
| **Control Title** | MRR/ARR Rollforward Preparation and CFO Review |
| **Control Description** | Monthly, FP&A prepares an MRR rollforward (beginning MRR + new + expansion − contraction − churn = ending MRR) reconciled to Chargebee and to recognized revenue trends. CFO reviews and investigates variances >2% versus forecast or versus prior month. |
| **Control Owner** | FP&A / CFO |
| **Frequency** | M |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Completeness, Accuracy (analytical) |
| **Risks Addressed** | SR-REV-06, SR-REV-04 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect rollforward methodology and reconciliation to GL revenue.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled months including year-end, inspect rollforwards, reconciliations, variance explanations, and CFO review evidence.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-41 — Deferred Revenue Rollforward Preparation and Review

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-41 |
| **Control Title** | Deferred Revenue Rollforward Preparation and Review |
| **Control Description** | Monthly, Accounting prepares a deferred revenue rollforward (beginning + new deferrals − recognition − other = ending) tying to the GL. Controller reviews. Unusual 'other' amounts require explanation. |
| **Control Owner** | Assistant Controller / Controller |
| **Frequency** | M |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Completeness, Existence, Valuation (DR) |
| **Risks Addressed** | SR-REV-02, SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect rollforward template and review checklist.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. For sampled months including year-end, inspect rollforwards, tie-outs, and Controller review; reperform ending balance tie to GL.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-42 — Looker Deferred Revenue Waterfall Validation

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-42 |
| **Control Title** | Looker Deferred Revenue Waterfall Validation |
| **Control Description** | Quarterly, FP&A validates that the Looker deferred revenue waterfall dashboard agrees to NetSuite subledger within $100 total and within $1 for any schedule marked 'material' (>$50k remaining). Discrepancies trigger data integrity tickets. |
| **Control Owner** | FP&A Manager |
| **Frequency** | Q |
| **Control Type** | Detective; IT-dependent manual |
| **Assertions Addressed** | Accuracy, Valuation |
| **Risks Addressed** | SR-REV-03 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect validation checklist and materiality thresholds for schedule-level review.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly validations; reperform dashboard-to-subledger comparison at year-end.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-43 — Chargebee Configuration Change Management

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-43 |
| **Control Title** | Chargebee Configuration Change Management |
| **Control Description** | Changes to Chargebee billing rules, plan prices, tax configs, dunning, and webhook endpoints require a change ticket, testing evidence in sandbox, and approval by Billing Operations Manager and Director of IT before production deployment. |
| **Control Owner** | Director of IT / Billing Operations Manager |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy, Completeness |
| **Risks Addressed** | SR-REV-04, SR-REV-06 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect change management policy and Chargebee admin access list.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample Chargebee production changes; inspect tickets, test evidence, and approvals preceding deployment.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-44 — NetSuite Revenue Recognition Module / Schedule Template Change Control

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-44 |
| **Control Title** | NetSuite Revenue Recognition Module / Schedule Template Change Control |
| **Control Description** | Changes to NetSuite deferred revenue schedule templates or revenue account mappings require Accounting approval (Controller) and IT change management compliance. |
| **Control Owner** | Controller / Director of IT |
| **Frequency** | E |
| **Control Type** | Preventive; Manual |
| **Assertions Addressed** | Accuracy, Valuation |
| **Risks Addressed** | SR-REV-03, SR-REV-02 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect change logs and approval requirements.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample template/mapping changes; verify Controller approval and testing evidence.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-45 — Okta Provisioning and Termination for Revenue Systems

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-45 |
| **Control Title** | Okta Provisioning and Termination for Revenue Systems |
| **Control Description** | User access to Salesforce, Chargebee, NetSuite, and Workato is provisioned via Okta with manager approval and terminated on the HR termination effective date (policy: within one business day). Weekly joiner-mover-leaver reconciliations are performed by IT. |
| **Control Owner** | Director of IT / CISO |
| **Frequency** | E / W |
| **Control Type** | Preventive/Detective; IT-dependent manual |
| **Assertions Addressed** | All (ITGC complementary) |
| **Risks Addressed** | SR-REV-05, SR-REV-06 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect Okta workflows and JML reconciliation procedures.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Sample joiners, movers, leavers; verify timely provisioning/termination; inspect weekly JML reconciliations.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-46 — Periodic User Access Reviews — Business Owners

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-46 |
| **Control Title** | Periodic User Access Reviews — Business Owners |
| **Control Description** | Quarterly, business owners (Controller, Director of RevOps, Billing Manager) certify user access appropriateness for Chargebee, NetSuite revenue roles, and Salesforce CPQ admin roles. |
| **Control Owner** | Business system owners |
| **Frequency** | Q |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | All (ITGC complementary) |
| **Risks Addressed** | SR-REV-05 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect certification questionnaires and completeness tracking.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly certifications for all in-scope systems; verify removal of access marked inappropriate.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-47 — Backup and Restore Readiness for Billing Records

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-47 |
| **Control Title** | Backup and Restore Readiness for Billing Records |
| **Control Description** | IT verifies weekly that Chargebee export backups and NetSuite cloud backups completed successfully. Quarterly restore tests of billing invoice data are performed in a non-production environment. |
| **Control Owner** | Director of IT |
| **Frequency** | W / Q |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Completeness (records availability) |
| **Risks Addressed** | SR-REV-06 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect backup monitoring and restore test procedures.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect weekly backup success evidence for sampled weeks; inspect quarterly restore test results.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-48 — Disclosure Committee Review of ASC 606 Disclosures

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-48 |
| **Control Title** | Disclosure Committee Review of ASC 606 Disclosures |
| **Control Description** | Quarterly and at year-end, the Disclosure Committee (CFO, Controller, General Counsel, FP&A) reviews draft ASC 606 disclosures including revenue disaggregation, contract balances, remaining performance obligations, and significant judgments. |
| **Control Owner** | CFO / Disclosure Committee |
| **Frequency** | Q |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | Presentation & Disclosure |
| **Risks Addressed** | N/A (disclosure) |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect Disclosure Committee charter and meeting protocols.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly/year-end packets, minutes, and review comments cleared before issuance.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-49 — Internal Audit Review of Revenue Cycle Controls

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-49 |
| **Control Title** | Internal Audit Review of Revenue Cycle Controls |
| **Control Description** | Internal Audit (co-sourced) performs an annual review of billing and deferred revenue controls, issuing findings to management and the Audit Committee. Management remediates findings on agreed timelines; IA validates remediation. |
| **Control Owner** | Internal Audit / Audit Committee |
| **Frequency** | A |
| **Control Type** | Detective; Manual (monitoring) |
| **Assertions Addressed** | Monitoring component (all) |
| **Risks Addressed** | All SR |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect IA planning memo, report, and AC presentation for FY2025.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect FY2025 IA report issued Oct 2025; verify remediation status of findings and intersection with our key controls.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

### CA-50 — CFO / CEO Sub-Certification of Revenue Representations

| Attribute | Detail |
|-----------|--------|
| **Control ID** | CA-50 |
| **Control Title** | CFO / CEO Sub-Certification of Revenue Representations |
| **Control Description** | As part of the quarterly and annual certification process, the CFO and CEO obtain sub-certifications from the Controller, Director of RevOps, and Billing Manager regarding the completeness and accuracy of revenue and deferred revenue balances and the effectiveness of related controls, supporting the Section 302/404 style certifications provided to the Board (even though the Company is private, lender covenants require analogous certifications). |
| **Control Owner** | CFO / CEO |
| **Frequency** | Q |
| **Control Type** | Detective; Manual |
| **Assertions Addressed** | All |
| **Risks Addressed** | SR-REV-05 |
| **COSO Mapping** | Control Activities; relevant Information & Communication linkages |

**Design Effectiveness Testing Procedures:**

1. Inquire of the control owner regarding the purpose, timing, and documentation of the control.
2. Inspect sub-certification templates and distribution process.
3. Evaluate whether the control, as designed, would prevent or detect material misstatements related to the assertions listed, on a timely basis.
4. Evaluate competence and authority of the control operator(s).
5. Document design conclusion (Effective / Exception) with basis.

**Operating Effectiveness Testing Procedures:**

1. Determine the period of reliance (interim + rollforward as applicable) and the population of control occurrences.
2. Select a representative sample consistent with Section 4 sampling methodology (frequency-based and risk-based).
3. Inspect quarterly and year-end sub-certifications; verify signers, dates, and any exceptions disclosed therein.
4. For automated controls, test relevant application control configuration and rely on effective ITGCs; supplement with transaction-level evidence that the control functioned on sampled items.
5. Evaluate deviations using the exceptions framework in Section 6; project/qualitatively assess if needed.
6. Document operating effectiveness conclusion for the period of reliance.

## 3.3 Control-to-Risk Traceability Matrix (Summary)

| Control | SR-01 | SR-02 | SR-03 | SR-04 | SR-05 | SR-06 | Primary Assertions |
|---------|-------|-------|-------|-------|-------|-------|--------------------|
| CA-01 | X||||| | Occurrence |
| CA-02 | X||||| | Occurrence |
| CA-03 | |||X|| | Accuracy |
| CA-04 | X|||X|| | Accuracy |
| CA-05 | |||X|| | Accuracy |
| CA-06 | |||X|| | Accuracy |
| CA-07 | X||||| | Occurrence |
| CA-08 | |||X|| | Accuracy |
| CA-09 | ||X|X|| | Accuracy |
| CA-10 | |||X||X | Completeness |
| CA-11 | |||||X | Completeness |
| CA-12 | X||X|X|| | Occurrence |
| CA-13 | X||X||| | Completeness |
| CA-14 | X||||X| | Occurrence |
| CA-15 | |X|X||| | Completeness |
| CA-16 | |X||||X | Completeness |
| CA-17 | |X|X||| | Completeness |
| CA-18 | X||X||X| | Occurrence |
| CA-19 | ||X||| | Valuation |
| CA-20 | ||X||| | Accuracy |
| CA-21 | ||X|X|| | Completeness |
| CA-22 | X||||| | Cutoff |
| CA-23 | |||X|X| | Accuracy |
| CA-24 | |||X|| | Accuracy |
| CA-25 | |||||X | Completeness |
| CA-26 | |||||X | Completeness |
| CA-27 | |X|||| | Accuracy |
| CA-28 | |X|||| | Completeness (DR) |
| CA-29 | |X|||| | Completeness |
| CA-30 | ||X||| | Presentation |
| CA-31 | ||X||| | Existence |
| CA-32 | ||||| | Valuation (AR) |
| CA-33 | X||||| | Occurrence |
| CA-34 | |||X|| | Accuracy |
| CA-35 | X|||||X | Completeness |
| CA-36 | ||||X| | All (fraud mitigation) |
| CA-37 | ||||X| | All (fraud/ITGC complementary) |
| CA-38 | ||||X| | Occurrence |
| CA-39 | ||||X| | All (fraud) |
| CA-40 | |||X||X | Completeness |
| CA-41 | |X|X||| | Completeness |
| CA-42 | ||X||| | Accuracy |
| CA-43 | |||X||X | Accuracy |
| CA-44 | |X|X||| | Accuracy |
| CA-45 | ||||X|X | All (ITGC complementary) |
| CA-46 | ||||X| | All (ITGC complementary) |
| CA-47 | |||||X | Completeness (records availability) |
| CA-48 | ||||| | Presentation & Disclosure |
| CA-49 | X|X|X|X|X|X | Monitoring component (all) |
| CA-50 | ||||X| | All |

## 3.4 Nature, Timing, and Extent Strategy

Controls associated with significant risks (particularly CA-01, CA-02, CA-04, CA-15, CA-17, CA-18, CA-19, CA-20, CA-22, CA-29, CA-36, CA-38, CA-39, CA-41) were subjected to **more extensive testing**, including larger sample sizes, testing closer to year-end, and increased use of reperformance. Automated controls were tested through a combination of configuration testing and complementary manual follow-up testing. Interim testing was performed primarily in August–September 2025, with rollforward procedures covering October–December 2025, including update inquiries, examination of subsequent control evidence, and additional samples for higher-risk controls.

---

# 4. SAMPLE SELECTIONS
**Workpaper Reference: WP-REV-SS**

## 4.1 Sampling Methodology

Sample sizes for tests of operating effectiveness were determined primarily using a **frequency-based attributes sampling approach**, consistent with firm guidance and PCAOB AS 2315 considerations for tests of controls, supplemented by risk-based increases for controls addressing significant risks. We did not use purely statistical monetary unit sampling for controls testing; where full-population data analytics were feasible (exception-based testing), we applied those procedures in lieu of or in addition to sampling.

### 4.1.1 Frequency-Based Baseline Sample Sizes

| Control Frequency | Baseline Sample Size (lower risk) | Elevated Sample Size (significant risk / prior deficiency) | Rollforward Incremental Items |
|-------------------|-----------------------------------|------------------------------------------------------------|-------------------------------|
| Continuous / Automated (config + DT) | Configuration test + 5–10 transaction touches | Configuration test + 15–25 transaction touches + full-pop exception scan where feasible | Re-test config at YE + 5 touches |
| Daily | 25 | 40 | 10 |
| Weekly | 10 | 15 | 5 |
| Monthly | 3 (interim) + 1–2 YE | 4–5 (interim) + 2–3 YE | Included in YE count |
| Quarterly | 2 | 3–4 (all quarters if SR) | N/A — test all quarters preferred |
| Annual | 1 | 1 (+ remediation retest if prior SD) | N/A |
| Event-driven | 25 (or full pop if <25) | 40 (or full pop if <60) | 10 |

### 4.1.2 Population Definitions and Source Systems

Populations were defined prior to selection and agreed to source system reports. Selections were made using random number generation (Python `secrets.randbelow` / Excel RAND) or haphazard selection only where populations were small and judged homogeneous; for significant-risk controls we preferred random or systematic selection with stratification.

## 4.2 Population Inventories (Key Populations)

| Population ID | Description | Source | FY2025 Population Size | Notes |
|---------------|-------------|--------|------------------------|-------|
| POP-NL | New logo subscription activations | Chargebee subscriptions where subscription_type=new | 118 | Ties to customer growth 412→500 |
| POP-EXP | Expansion / seat upgrade amendments | Chargebee changes + Salesforce amendments | 142 | |
| POP-CON | Contractions / downgrades | Chargebee changes | 37 | |
| POP-CHURN | Cancellations completed | Chargebee cancelled + SF tickets | 30 | Ties to customer movement: 412 + 118 new − 30 churn = 500 |
| POP-INV | Subscription invoices issued | Chargebee invoice register | 5,862 | Includes prorations |
| POP-INV-ANN | Annual prepaid invoices | Chargebee filter billing_period=year | 27 | |
| POP-INV-QTR | Quarterly prepaid invoices | Chargebee filter | 348 | |
| POP-CR | Credit memos | NetSuite / Chargebee | 96 | |
| POP-JE-REV | JEs touching revenue or DR accounts | NetSuite JE lines | 214 | |
| POP-MOD | Modifications ARR impact >$5k | RevOps log | 64 | |
| POP-DUN | Accounts entering stage-3 dunning | Chargebee | 53 | |
| POP-INTFAIL | Workato failed jobs (revenue integrations) | Workato | 117 | |
| POP-CHG-CB | Chargebee production config changes | IT change log | 22 | |
| POP-CHG-NS | NetSuite DR template/mapping changes | IT change log | 7 | |
| POP-JML | Joiners/Movers/Leavers with revenue system access | Okta / HR | 64 J / 21 M / 18 L | |

### Clarification on Customer Movement

Customer count reconciliation for FY2025: Beginning customers 412 + new logos 118 − churned customers 30 = **500 ending customers**. (Expansion and contraction activity affects ARR/MRR but not unique customer count except in rare consolidation scenarios.) Population POP-NL was refined to 118 after excluding 30 'reactivation' records initially misclassified; sample selections below use the refined population.

## 4.3 Detailed Sample Selections by Control

The following tables present the sample sizes and selection method for each control. Detailed sample item listings for high-risk controls are provided in subsection 4.4; full sample listings for all controls are maintained in the electronic audit file under WP-REV-SS-DETAIL.xlsx (fictional cross-reference).

| Control | Frequency | Risk Elevation | Interim Sample | YE / Rollforward | Total Items Tested | Selection Method | Population |
|---------|-----------|----------------|----------------|------------------|--------------------|------------------|------------|
| CA-01 | E | SR-01 | 25 | 10 | 35 | Random — POP-NL | 118 new logos |
| CA-02 | D | SR-01 | 15 days + 20 act. | 5 days + 10 act. | 20 days / 30 act. | Systematic days; random activations | Exception logs + activations |
| CA-03 | C | SR-04 | Config + 15 orders | Reconfig + 5 | Config×2 + 20 | Random Closed Won | FY2025 Closed Won |
| CA-04 | E | SR-01/04 | 40 (stratified) | 10 | 50 | Stratified by discount band | Closed Won w/ discount |
| CA-05 | E | SR-04 | 25 | 10 | 35 | Random new+expansion | POP-NL+POP-EXP |
| CA-06 | E | Mod | 15 | 5 | 20 | Random new customers | New customer masters |
| CA-07 | E | SR-01 | 20 (10 above/10 below $50k) | 8 | 28 | Stratified by ARR | New logos |
| CA-08 | A | SR-04 | 1 rate card package | N/A — inspect mid-year changes (2) | 1 + 2 changes | Full population | Annual rate card |
| CA-09 | A | SR-03/04 | 1 SSP memo + 10 contracts | N/A | 1 + 10 | Full memo; random multi-element | SSP + multi-element deals |
| CA-10 | M | SR-06/04 | 4 months | 2 months (Nov, Dec) | 6 months | Judgmental incl. YE | 12 monthly runs |
| CA-11 | C/W | SR-06 | 25 incidents + 8 weeks | 10 incidents + 4 weeks | 35 + 12 weeks | Random incidents; systematic weeks | 117 fails; 52 weeks |
| CA-12 | E | SR-01/03/04 | 25 exp + 10 con | 10 exp + 5 con | 35 + 15 | Random | POP-EXP / POP-CON |
| CA-13 | E | SR-01/03 | 15 | 5 | 20 | Random | 30 churned |
| CA-14 | E | SR-01/05 | Full pop flagged (18) + side-letter search | YE search update | 18 + search | Full flagged population | Non-standard flags |
| CA-15 | C | SR-02/03 | Config + 25 prepaid inv. + full-pop scan | Reconfig + 10 + YE scan | Config×2 + 35 + scans | Stratified m/q/a; DT scan | Prepaid invoices |
| CA-16 | D | SR-02/06 | 25 days | 10 days | 35 days | Systematic (every Nth day) | ~250 business days |
| CA-17 | M | SR-02/03 | 4 months | 2 months (Nov, Dec) | 6 months | Judgmental incl. YE | 12 months |
| CA-18 | M/E | SR-01/03/05 | 30 JEs | 15 JEs | 45 JEs | Stratified by amount/type | 214 rev/DR JEs |
| CA-19 | M | SR-03 | 4 months (recalcs) | 2 months | 6 months | Judgmental incl. YE | 12 months |
| CA-20 | E | SR-03 | 25 | 10 | 35 | Random | 64 modifications >$5k |
| CA-21 | M | SR-04 | 4 months × 10 cust. | 2 × 10 | 60 customer-months | Random customers/month | Overage-eligible cust. |
| CA-22 | M | SR-01 | 4 month-ends | Dec 31 detailed | 5 + YE | Judgmental | 12 cutoffs |
| CA-23 | E | SR-05/04 | 25 | 10 | 35 | Stratified by amount | 96 credits |
| CA-24 | E | SR-04 | 20 new + 15 >$25k | 8 + 5 | 28 + 20 | Random | First inv. + large inv. |
| CA-25 | W | SR-06 | 10 weeks | 5 weeks | 15 weeks | Systematic | 52 weeks |
| CA-26 | D/M | SR-06 | 20 days + 3 months | 8 days + Dec | 28 days + 4 months | Systematic / judgmental | Business days / months |
| CA-27 | D | SR-02 | 20 days | 8 days | 28 days | Random days with manual receipts | Manual receipt days |
| CA-28 | W | SR-02 | 8 weeks | 4 weeks | 12 weeks | Systematic | 52 weeks |
| CA-29 | Q | SR-02 | Q1–Q3 runs | Q4 + YE reperformance | 4 + YE reperf. | Full population of quarterly runs | 4 quarters |
| CA-30 | Q | SR-03 | Q1–Q3 | Q4 / YE | 4 | Full population | 4 quarters |
| CA-31 | Q | SR-03 | Q1–Q3 | Q4 | 4 | Full population | 4 quarters |
| CA-32 | M | Mod | 3 months | YE + Nov | 5 months | Judgmental | 12 months |
| CA-33 | C/E | SR-01 | 15 dunning cases | 5 | 20 | Random | 53 stage-3 |
| CA-34 | Q/M | SR-04 | 2 qtr reviews + 3 mo spots | Q4 + Dec spot | 3 qtr + 4 mo | Judgmental | Quarters/months |
| CA-35 | W | SR-01/06 | 8 weeks | 4 weeks | 12 weeks | Systematic | 52 weeks |
| CA-36 | Q | SR-05 | Q1–Q3 | Q4 + access reperf. | 4 + reperf. | Full population | 4 quarters |
| CA-37 | Q | SR-05 | Q1–Q3 | Q4 | 4 | Full population | 4 quarters |
| CA-38 | E | SR-05 | 30 manual JEs | 15 | 45 | Stratified; focus period-end | Manual rev/DR JEs |
| CA-39 | M/Q | SR-05 | 4 months + 2 AC pkts | 2 months + YE AC | 6 mo + 3 AC | Judgmental | 12 months / 4 qtr |
| CA-40 | M | SR-06/04 | 4 months | 2 months | 6 months | Judgmental incl. YE | 12 months |
| CA-41 | M | SR-02/03 | 4 months | 2 months | 6 months | Judgmental incl. YE | 12 months |
| CA-42 | Q | SR-03 | Q1–Q3 | Q4 + reperf. | 4 + reperf. | Full population | 4 quarters |
| CA-43 | E | SR-04/06 | 15 changes | 5 | 20 | Random (near full pop) | 22 changes |
| CA-44 | E | SR-02/03 | Full population (5 interim) | 2 YE | 7 (full) | Full population | 7 changes |
| CA-45 | E/W | SR-05/06 | 15 J + 8 M + 10 L + 8 wks | 5 J + 3 M + 5 L + 4 wks | 20/11/15 + 12 wks | Random / systematic | JML populations |
| CA-46 | Q | SR-05 | Q1–Q3 | Q4 | 4 | Full population | 4 quarters |
| CA-47 | W/Q | SR-06 | 8 weeks + Q1–Q3 restore | 4 weeks + Q4 | 12 weeks + 4 restores | Systematic / full qtr | Weeks / quarters |
| CA-48 | Q | Disc. | Q1–Q3 | YE packet | 4 | Full population | 4 quarters |
| CA-49 | A | Monitor | 1 IA report + remediation follow-up | Remediation validation | 1 + follow-ups | Full population | Annual IA review |
| CA-50 | Q | SR-05 | Q1–Q3 sub-certs | YE sub-certs | 4 | Full population | 4 quarters |

## 4.4 Illustrative Detailed Sample Listing — Selected High-Risk Controls

### 4.4.1 CA-01 Sample — New Logo Activations (35 items)

| Sample # | Customer ID | Customer Name (fictional) | ARR at Signature | Order Form Exec Date | Chargebee Activate Date | Plan | Selected For |
|----------|-------------|---------------------------|------------------|----------------------|-------------------------|------|--------------|
| 1 | CM-10421 | Northbridge Logistics LLC | $84,000 | 2025-01-14 | 2025-01-15 | Enterprise | Interim |
| 2 | CM-10455 | Helio Dental Partners | $22,000 | 2025-01-28 | 2025-01-29 | Professional | Interim |
| 3 | CM-10488 | Summit Castings Inc. | $156,000 | 2025-02-05 | 2025-02-06 | Enterprise Plus | Interim |
| 4 | CM-10502 | Blue Lark Marketing | $9,600 | 2025-02-11 | 2025-02-12 | Starter | Interim |
| 5 | CM-10530 | Cascade BioSupply | $67,500 | 2025-02-20 | 2025-02-21 | Enterprise | Interim |
| 6 | CM-10561 | Ironclad Facilities Group | $118,000 | 2025-03-03 | 2025-03-04 | Enterprise | Interim |
| 7 | CM-10590 | Pine & Cedar Retail Co-op | $18,400 | 2025-03-12 | 2025-03-13 | Professional | Interim |
| 8 | CM-10612 | Orbital Analytics GmbH | $242,000 | 2025-03-18 | 2025-03-19 | Enterprise Plus | Interim |
| 9 | CM-10644 | Red Mesa Healthcare Admin | $91,000 | 2025-03-27 | 2025-03-28 | Enterprise | Interim |
| 10 | CM-10671 | Quarry Field Services | $14,300 | 2025-04-02 | 2025-04-03 | Professional | Interim |
| 11 | CM-10705 | Nimbus Payroll Systems | $56,000 | 2025-04-15 | 2025-04-16 | Enterprise | Interim |
| 12 | CM-10733 | Glass Harbor Breweries | $12,800 | 2025-04-22 | 2025-04-24 | Professional | Interim |
| 13 | CM-10758 | Atlas Crane & Rigging | $73,500 | 2025-05-01 | 2025-05-01 | Enterprise | Interim |
| 14 | CM-10790 | Velvet Rope Hospitality | $21,000 | 2025-05-09 | 2025-05-10 | Professional | Interim |
| 15 | CM-10814 | Kepler Semiconductor Materials | $188,000 | 2025-05-19 | 2025-05-20 | Enterprise Plus | Interim |
| 16 | CM-10840 | Harborlight Mutual Aid | $8,900 | 2025-05-28 | 2025-05-29 | Starter | Interim |
| 17 | CM-10866 | Driftwood Credit Union | $64,000 | 2025-06-06 | 2025-06-07 | Enterprise | Interim |
| 18 | CM-10895 | Copperline Mining Analytics | $132,000 | 2025-06-17 | 2025-06-18 | Enterprise | Interim |
| 19 | CM-10920 | Saffron Supply Chain Ltd. | $27,500 | 2025-06-25 | 2025-06-26 | Professional | Interim |
| 20 | CM-10948 | Westfork Energy Coop | $99,000 | 2025-07-08 | 2025-07-09 | Enterprise | Interim |
| 21 | CM-10977 | Brightloom Education Group | $41,000 | 2025-07-16 | 2025-07-17 | Professional | Interim |
| 22 | CM-11003 | Marrowbone Foods Inc. | $15,700 | 2025-07-24 | 2025-07-25 | Professional | Interim |
| 23 | CM-11031 | Silverthread Legal Ops | $86,000 | 2025-08-05 | 2025-08-06 | Enterprise | Interim |
| 24 | CM-11058 | Canyon Peer Review Network | $52,000 | 2025-08-14 | 2025-08-15 | Enterprise | Interim |
| 25 | CM-11084 | Lumenara Clinics | $119,000 | 2025-08-27 | 2025-08-28 | Enterprise | Interim |
| 26 | CM-11110 | Folio & Bind Publishing | $13,400 | 2025-09-04 | 2025-09-05 | Professional | Interim |
| 27 | CM-11139 | Highgrain Agribusiness | $78,000 | 2025-09-18 | 2025-09-19 | Enterprise | YE RF |
| 28 | CM-11167 | Portsmith Marine Terminals | $165,000 | 2025-10-02 | 2025-10-03 | Enterprise Plus | YE RF |
| 29 | CM-11192 | Echo Valley Municipal Utility | $44,500 | 2025-10-15 | 2025-10-16 | Professional | YE RF |
| 30 | CM-11220 | Boreal Timber Partners | $102,000 | 2025-10-29 | 2025-10-30 | Enterprise | YE RF |
| 31 | CM-11248 | Keystone Benefits Admin | $69,500 | 2025-11-07 | 2025-11-08 | Enterprise | YE RF |
| 32 | CM-11275 | Nightowl Logistics 24/7 | $23,800 | 2025-11-19 | 2025-11-20 | Professional | YE RF |
| 33 | CM-11301 | Amperage Industrial IoT | $214,000 | 2025-12-03 | 2025-12-04 | Enterprise Plus | YE RF |
| 34 | CM-11328 | Cinderpeak Outdoor Retail | $17,600 | 2025-12-12 | 2025-12-13 | Professional | YE RF |
| 35 | CM-11355 | Solstice Pharma Services | $147,000 | 2025-12-22 | 2025-12-23 | Enterprise Plus | YE RF |

### 4.4.2 CA-04 Sample Stratification — Discount Approvals (50 items)

| Discount Band | Population (Closed Won w/ discount) | Sample Size | Selection Approach |
|---------------|-------------------------------------|-------------|--------------------|
| 0–10% (Sales Manager approval) | 186 | 15 | Random |
| 10.01–25% (VP Sales approval) | 94 | 20 | Random |
| >25% (CFO approval) | 31 | 15 | Near full-population random (15/31) |
| **Total** | **311** | **50** | |

Illustrative >25% discount samples:

| Sample # | Opportunity ID | Customer | Discount % | Approvers Documented | Close Won Date |
|----------|----------------|----------|------------|----------------------|----------------|
| D-01 | OPP-77821 | Orbital Analytics GmbH | 32% | VP Sales; CFO (A. Nguyen) | 2025-03-18 |
| D-02 | OPP-78204 | Kepler Semiconductor Materials | 28% | VP Sales; CFO | 2025-05-19 |
| D-03 | OPP-79011 | Amperage Industrial IoT | 35% | VP Sales; CFO | 2025-12-03 |
| D-04 | OPP-77440 | Summit Castings Inc. | 27% | VP Sales; CFO | 2025-02-05 |
| D-05 | OPP-80102 | Portsmith Marine Terminals | 30% | VP Sales; CFO | 2025-10-02 |
| … | … | (10 additional >25% samples on file) | … | … | … |

### 4.4.3 CA-15 / CA-29 — Prepaid Invoice Deferred Revenue Samples

| Sample # | Invoice # | Customer | Billing Frequency | Invoice Net | Service Period | Schedule Created? | Test Focus |
|----------|-----------|----------|-------------------|-------------|----------------|-------------------|------------|
| DR-01 | INV-90521 | Orbital Analytics GmbH | Annual | $242,000 | 2025-04-01 – 2026-03-31 | Yes — same day | Completeness/accuracy |
| DR-02 | INV-91204 | Kepler Semiconductor Materials | Annual | $188,000 | 2025-06-01 – 2026-05-31 | Yes — same day | Completeness/accuracy |
| DR-03 | INV-92880 | Amperage Industrial IoT | Annual | $214,000 | 2026-01-01 – 2026-12-31 | Yes — same day | YE cutoff |
| DR-04 | INV-90014 | Ironclad Facilities Group | Quarterly | $29,500 | 2025-03-01 – 2025-05-31 | Yes | Quarterly prepaid |
| DR-05 | INV-91775 | Lumenara Clinics | Monthly | $9,917 | 2025-09-01 – 2025-09-30 | Yes | Monthly control touch |
| DR-06 | INV-92110 | Westfork Energy Coop | Quarterly | $24,750 | 2025-10-01 – 2025-12-31 | Yes | Completeness |
| DR-07 | INV-93002 | Solstice Pharma Services | Annual | $147,000 | 2026-01-01 – 2026-12-31 | Yes — same day | YE cutoff |
| … | … | (additional 28 stratified samples on file) | … | … | … | … | … |

### 4.4.4 CA-18 / CA-38 — Revenue & Deferred Revenue Journal Entries (45 items)

| Sample # | JE # | Date | Preparer | Approver | Amount (abs.) | Type | Period-End? |
|----------|------|------|----------|----------|---------------|------|-------------|
| JE-01 | JE-2025-03144 | 2025-01-31 | S. Ramirez | M. Bell | $1,842,220 | Monthly DR amortization (standard) | Yes |
| JE-02 | JE-2025-05902 | 2025-02-28 | S. Ramirez | M. Bell | $1,901,455 | Monthly DR amortization | Yes |
| JE-03 | JE-2025-08821 | 2025-03-15 | Staff Acct | S. Ramirez | $12,400 | Usage overage accrual | No |
| JE-04 | JE-2025-11002 | 2025-03-31 | S. Ramirez | M. Bell | $48,900 | SSP allocation — multi-element | Yes |
| JE-05 | JE-2025-40118 | 2025-11-30 | S. Ramirez | M. Bell | $2,244,010 | Monthly DR amortization | Yes |
| JE-06 | JE-2025-44091 | 2025-12-31 | S. Ramirez | M. Bell / A. Nguyen (CFO) | $2,301,880 | Monthly DR amortization + YE classify | Yes |
| JE-07 | JE-2025-44155 | 2025-12-31 | M. Bell | A. Nguyen | $75,000 | Manual top-side? — see exceptions | Yes |
| … | … | … | … | … | … | (38 additional on file) | … |

## 4.5 Sample Selection Completeness Representation

We represent that: (1) populations were obtained from system sources prior to selection; (2) population totals were reconciled to control totals (e.g., invoice register to GL billings; subscription counts to MRR dashboard) within tolerable differences; (3) selections were made without replacement; and (4) replacements were made only when a selected item was determined not to belong to the population (documented in WP-REV-SS-REP), with the next random item chosen.

---

# 5. TESTING RESULTS
**Workpaper Reference: WP-REV-TR**

## 5.1 Design Effectiveness Results Summary

We evaluated the design effectiveness of all 50 control activities through inquiry, walkthrough, examination of policy/configuration, and, where applicable, sandbox experimentation. **All 50 controls were concluded to be designed effectively** as of the walkthrough dates, after considering management's remediation of FY2024 significant deficiencies SD-2024-03 and SD-2024-07 (remediated designs re-walked in July 2025).

| Design Conclusion | Number of Controls |
|--------------------|--------------------|
| Designed effectively | 50 |
| Design deficiency identified | 0 |
| Not yet designed / not tested | 0 |

## 5.2 Operating Effectiveness Results by Control

The following table summarizes operating effectiveness testing results. Detailed exception write-ups are provided in Section 6 for any control with deviations.

| Control | Items Tested | Deviations | OE Conclusion | Severity if Deficiency | Notes |
|---------|--------------|------------|---------------|------------------------|-------|
| CA-01 | 35 | 0 | Operating effectively | — | All activations preceded by executed contracts; timestamps consistent |
| CA-02 | 20 days / 30 act. | 1 | Operating effectively with isolated deviation | Low — see EX-01 | One exception aged 3 business days vs. 2-day SLA; corrected day 3 |
| CA-03 | Config + 20 | 0 | Operating effectively | — | Rate card matched CPQ; sandbox override blocked |
| CA-04 | 50 | 1 | Operating effectively with isolated deviation | Low — see EX-02 | One 12% discount approved by Sales Manager only; VP approval obtained retroactively same week |
| CA-05 | 35 | 0 | Operating effectively | — | Seat counts matched |
| CA-06 | 20 | 0 | Operating effectively | — | Dual review evidenced before first invoice |
| CA-07 | 28 | 0 | Operating effectively | — | Credit approvals / payment method validations present |
| CA-08 | 1 + 2 | 0 | Operating effectively | — | Board ratification Jan 2025; mid-year changes CFO-approved |
| CA-09 | 1 + 10 | 0 | Operating effectively | — | SSP applied correctly on sampled multi-element deals |
| CA-10 | 6 | 0 | Operating effectively | — | Checklists complete; Assistant Controller review timely |
| CA-11 | 35 + 12 wk | 2 | Operating effectively with deviations | Low–Moderate — see EX-03 | Two failed jobs resolved in 30 and 36 hours vs. 24-hour SLA; no financial misstatement |
| CA-12 | 35 + 15 | 0 | Operating effectively | — | Amendments preceded Chargebee changes; proration accurate |
| CA-13 | 20 | 0 | Operating effectively | — | Dual approvals and DR treatment appropriate |
| CA-14 | 18 + search | 0 | Operating effectively | — | No unflagged side letters identified in search procedures |
| CA-15 | Config + 35 + scans | 0 | Operating effectively | — | Full-pop scans at interim and YE: 0 missing schedules |
| CA-16 | 35 | 0 | Operating effectively | — | Daily reconciling items cleared within SLA |
| CA-17 | 6 | 0 | Operating effectively | — | Subledger-to-GL differences <$500 each month tested; reviewed timely |
| CA-18 | 45 | 0 | Operating effectively | — | Approvals and support complete; see CA-38 for manual JE focus |
| CA-19 | 6 | 0 | Operating effectively | — | Recalculations agreed within $500 threshold |
| CA-20 | 35 | 1 | Operating effectively with isolated deviation | Moderate — see EX-04 | One modification checklist completed 6 days after Chargebee update |
| CA-21 | 60 cust-mo | 0 | Operating effectively | — | Overage math recalculated without exception |
| CA-22 | 5 + YE | 0 | Operating effectively | — | YE late activation approvals documented; cutoff correct |
| CA-23 | 35 | 0 | Operating effectively | — | Approval thresholds met |
| CA-24 | 28 + 20 | 0 | Operating effectively | — | Three-way match documented |
| CA-25 | 15 | 0 | Operating effectively | — | Coverage gaps resolved within 3 BD |
| CA-26 | 28 + 4 | 0 | Operating effectively | — | Stripe settlements reconciled |
| CA-27 | 28 | 0 | Operating effectively | — | Second reviewer evidenced |
| CA-28 | 12 | 0 | Operating effectively | — | Unapplied cash reviewed; no aged prepaid subscription cash >14 days at YE |
| CA-29 | 4 + YE reperf. | 0 | Operating effectively | — | Analytics runs clean; YE reperformance agreed |
| CA-30 | 4 | 0 | Operating effectively | — | Current/non-current classification recomputed accurately |
| CA-31 | 4 | 0 | Operating effectively | — | Stale schedules investigated; 2 true system errors corrected (immaterial) |
| CA-32 | 5 | 0 | Operating effectively | — | CECL allowance approved; methodology consistent |
| CA-33 | 20 | 0 | Operating effectively | — | Collectibility assessments documented |
| CA-34 | 3 q + 4 m | 0 | Operating effectively | — | Tax config reviews complete |
| CA-35 | 12 | 0 | Operating effectively (KPI observation only) | — — see EX-05 observation | Apparent KPI breach explained by CA-07 credit hold; dashboard logic observation only |
| CA-36 | 4 + reperf. | 0 | Operating effectively | — | No unmitigated SOD conflicts in revenue posting paths |
| CA-37 | 4 | 0 | Operating effectively | — | Privileged access appropriate; 1 contractor removed timely |
| CA-38 | 45 | 1 | Deficiency — see analysis | Significant Deficiency candidate — see EX-06 | One manual YE JE ($75k) posted with Controller preparation and CFO approval but without standardized template attachment initially |
| CA-39 | 6 + 3 AC | 0 | Operating effectively | — | Flagged items investigated; AC packets complete |
| CA-40 | 6 | 0 | Operating effectively | — | MRR rollforward tied; variances explained |
| CA-41 | 6 | 0 | Operating effectively | — | DR rollforward tied to GL |
| CA-42 | 4 + reperf. | 0 | Operating effectively | — | Dashboard agreed to subledger within threshold |
| CA-43 | 20 | 0 | Operating effectively | — | Change tickets complete with sandbox tests |
| CA-44 | 7 | 0 | Operating effectively | — | Full population — Controller approvals present |
| CA-45 | JML + 12 wk | 2 | Operating effectively with deviations | Low — see EX-07 / ITGC link | 2 terminations completed in 2–3 BD vs. 1 BD policy; complementary reviews effective |
| CA-46 | 4 | 0 | Operating effectively | — | Certifications complete; removals evidenced |
| CA-47 | 12 + 4 | 0 | Operating effectively | — | Backups successful; restore tests passed |
| CA-48 | 4 | 0 | Operating effectively | — | Disclosure Committee reviews evidenced |
| CA-49 | 1 + follow-ups | 0 | Operating effectively (monitoring) | — | IA findings remediated; none contradicted our OE conclusions |
| CA-50 | 4 | 0 | Operating effectively | — | Sub-certifications signed timely without disclosed exceptions |

## 5.3 Aggregate Operating Effectiveness Statistics

| Metric | Result |
|--------|--------|
| Controls tested for operating effectiveness | 50 |
| Controls with zero deviations | 43 |
| Controls with isolated deviations concluded still effective (incl. lesser deficiencies not SD) | 6 |
| Controls with deficiencies requiring evaluation as ICFR deficiency | 1 (CA-38) |
| Total deviation instances across all controls (excluding EX-05 observation) | 8 |
| Deviations resulting in identified financial misstatement (before trivial threshold) | 0 |
| Deviations resulting in adjustments above clearly trivial | 0 |
| Full-population scans performed (CA-15, CA-29, portions of CA-03/CA-23) | Clean — no additional exceptions |

## 5.4 Remediation Testing of Prior-Year Significant Deficiencies

| Prior SD | Remediation Description | Testing Performed | OE Conclusion FY2025 |
|----------|-------------------------|-------------------|----------------------|
| SD-2024-03 Discount dual-approval evidence | Mandatory CPQ second-approver hard block | CA-04 design re-walk + 50 OE samples | Remediated — operating effectively (with unrelated isolated EX-02 at different threshold band) |
| SD-2024-07 DR schedule creation timeliness | Workato automated schedule creation | CA-15 config + 35 samples + full-pop scans | Remediated — operating effectively |

## 5.5 Narrative Commentary on Results

Overall, the revenue cycle control environment at CloudMeridian demonstrated a mature design and a high rate of consistent operation throughout FY2025. The predominance of automated billing and automated deferred revenue schedule creation (CA-15), combined with disciplined monthly rollforwards (CA-40, CA-41) and strong entity-level monitoring (CA-39, CA-49, CA-50), provides multiple layers of precision relative to materiality.

The isolated deviations observed in CA-02, CA-04, CA-11, CA-20, CA-35, and CA-45 were evaluated individually and in aggregate (see Section 6). None of these deviations indicated a breakdown that would allow a material misstatement to occur without detection, given compensating controls and the absence of associated misstatements in substantive testing cross-references.

The deviation related to CA-38 (manual journal entry documentation/template discipline for a year-end entry) was more judgmental and is analyzed in depth as EX-06. While the entry itself was substantively supported and appropriately approved by the CFO, the failure to follow the standardized template/documentation attachment requirement at the time of posting represents a departure from a control specifically designed to address management override risk (SR-REV-05). We evaluated this as a **control deficiency**, and further as a **significant deficiency** (but not a material weakness), as detailed in Section 6 and concluded in Section 7.

ITGC reliance was maintained, supporting reliance on automated application controls. Complementary user controls related to access terminations (CA-45) showed minor SLA deviations consistent with ITGC findings, without evidence of inappropriate access use affecting revenue transactions.

---

# 6. EXCEPTIONS ANALYSIS
**Workpaper Reference: WP-REV-EX**

## 6.1 Exceptions Evaluation Framework

Each control deviation was evaluated using the following framework aligned with PCAOB AS 2201.62–.70 and firm methodology:

1. **Describe the deviation** — what occurred vs. what the control requires.
2. **Determine whether the deviation is a control exception** — confirmed departure from prescribed performance.
3. **Investigate root cause** — process, people, system, or management intent.
4. **Identify potential misstatement** — did a misstatement occur? Could one occur?
5. **Consider compensating controls** — precision and evidence of operation.
6. **Expand testing if needed** — additional samples or full-population procedures.
7. **Classify severity** — deficiency, significant deficiency, or material weakness (or conclude not a deficiency if isolated and trivial to ICFR objectives).
8. **Consider aggregation** — multiple deficiencies that in combination could be significant or material.

## 6.2 Exception EX-01 — CA-02 Start Date Exception Aging SLA Breach

| Field | Detail |
|-------|--------|
| **Exception ID** | EX-01 |
| **Control** | CA-02 — Service Start Date Validation Against Contract Effective Date |
| **Sample reference** | CA-02 Day sample 2025-08-19 / Activation CM-11058 Canyon Peer Review Network |
| **What happened** | Workato detected a one-day mismatch (Order Form start 2025-08-14; Chargebee initially 2025-08-15 due to timezone conversion bug in an integration mapping). Exception ticket INT-5521 was opened Aug 19 and resolved Aug 22 (3 business days), breaching the 2-business-day resolution SLA. |
| **Root cause** | Temporary Workato mapping issue following a sandbox promotion (related change ticket CHG-8821 tested for other fields but not timezone). Staffing constraint in RevOps (one team member on PTO) delayed resolution by one incremental day. |
| **Misstatement?** | No. Upon correction, Chargebee start date was aligned to Aug 14; August revenue was complete. Difference was timing of exception clearance, not incorrect financial reporting after resolution. |
| **Expanded testing** | Selected 10 additional activations in August–September 2025 for date matching; no further mismatches. Reviewed all CA-02 exceptions in August 2025 (4 total); only INT-5521 breached SLA, and only by one day. |
| **Compensating controls** | CA-01 activation checklist; CA-10 billing completeness; CA-19 amortization recalculation. |
| **Classification** | Isolated operational deviation; **not an ICFR deficiency** (control operated, detection occurred, financial reporting unaffected; SLA miss was administrative). Documented for management letter as process improvement. |
| **Management response** | RevOps updated coverage calendar for PTO; IT added timezone test cases to Chargebee integration change template (implemented Sep 2025). |

## 6.3 Exception EX-02 — CA-04 Missing Concurrent VP Approval on 12% Discount

| Field | Detail |
|-------|--------|
| **Exception ID** | EX-02 |
| **Control** | CA-04 — Discount Approval Workflow |
| **Sample reference** | CA-04 Sample band 10.01–25%, item #11 — OPP-78651 Brightloom Education Group (12% discount) |
| **What happened** | Opportunity reached Closed Won on 2025-07-16 with Sales Manager approval only. CPQ approval rule expected VP Sales approval for discounts >10%. Investigation found the opportunity used an outdated quote record type briefly re-enabled during a CPQ metadata deploy on 2025-07-14, bypassing the VP rule for approximately 36 hours. |
| **Root cause** | Change management gap in CPQ deploy (partially linked to CA-43 scope — Salesforce CPQ vs. Chargebee). The deploy issue was detected by RevOps on 2025-07-17; VP approval was obtained retroactively on 2025-07-17 for OPP-78651 and three other in-flight quotes (only one of which closed). |
| **Misstatement?** | No. Price charged matched the intended 12% discount; commercial approval was obtained retroactively; revenue correct. |
| **Expanded testing** | Identified all Closed Won opportunities from 2025-07-14 to 2025-07-17 (11 deals). Tested approval completeness: 1 deficiency (this item), 3 retroactive approvals before invoice, 7 clean. No pricing errors. |
| **Compensating controls** | CA-03 rate card; CA-24 three-way match on first invoice; CA-08 rate governance. |
| **Classification** | **Control deficiency** (design operated incorrectly for a short window due to change management), assessed as **not a significant deficiency** because: limited duration (36 hours), limited affected population (1 closed deal without timely approval), compensating controls, no misstatement, and remediation completed in July 2025 with no recurrence in subsequent CA-04 samples (including YE rollforward). |
| **Aggregation consideration** | Aggregated with EX-03 and EX-07 as process/IT operational items; still below significant deficiency threshold in aggregate. |

## 6.4 Exception EX-03 — CA-11 Integration Failure Resolution SLA Breaches

| Field | Detail |
|-------|--------|
| **Exception ID** | EX-03 |
| **Control** | CA-11 — Integration Failure Monitoring |
| **Sample references** | Incidents INC-4410 (2025-05-12) and INC-4788 (2025-09-03) |
| **What happened** | Two Chargebee→NetSuite invoice sync failures were resolved in 30 hours and 36 hours, respectively, versus the one-business-day (approximately 24-hour) SLA. Weekly aging reviews did occur and showed the items. |
| **Root cause** | Vendor API rate limiting (May) and NetSuite scheduled maintenance extension (September). |
| **Misstatement?** | No. Invoices posted on resolution date still within the correct accounting month; deferred revenue schedules created upon posting; cutoff unaffected for both incidents. |
| **Expanded testing** | Reviewed all 117 failed jobs' resolution times; 9 exceeded 24 hours; all 9 still posted within the same month; none spanned month-end without compensating CA-16 daily reconciliation detection. |
| **Classification** | SLA deviations; **deficiency at the process precision level but not significant** — detective control still identified issues; financial reporting precision preserved by CA-16/CA-17. Management letter comment recommended revising SLA to 'within one business day or prior to month-end close, whichever sooner' for clarity. |

## 6.5 Exception EX-04 — CA-20 Modification Checklist Timing

| Field | Detail |
|-------|--------|
| **Exception ID** | EX-04 |
| **Control** | CA-20 — Contract Modification Accounting Checklist |
| **Sample reference** | MOD-2025-044 — Copperline Mining Analytics seat expansion +$28,000 ARR effective 2025-06-18 |
| **What happened** | Chargebee subscription quantity updated Jun 18; ASC 606 modification checklist completed Jun 24 (6 days later). Control expectation: checklist completed prior to or concurrent with system update for ARR impact >$5k. |
| **Root cause** | Accounting backlog during June close; RevOps proceeded with customer-requested urgent expansion after verbal Accounting acknowledgment not evidenced in ticket. |
| **Misstatement?** | No. Prospective modification treatment was correct; proration and prospective rate correct upon recalculation. Checklist conclusions matched the accounting already reflected. |
| **Expanded testing** | Additional 10 modifications in May–July 2025; 1 additional checklist completed 2 days late (still same week; no misstatement). Remaining contemporaneous. |
| **Compensating controls** | CA-12 amendment execution; CA-19 amortization recalculation; CA-41 DR rollforward. |
| **Classification** | **Control deficiency** (timing/precision), **not significant** — isolated/limited, correct accounting outcome, compensating detective controls with sufficient precision relative to materiality. |

## 6.6 Exception EX-05 — CA-35 Provisioning Timeliness Escalation

| Field | Detail |
|-------|--------|
| **Exception ID** | EX-05 |
| **Control** | CA-35 — Closed-Won to Provisioning Timeliness |
| **Sample reference** | Week of 2025-11-17 / Customer Nightowl Logistics 24/7 (ARR $23,800 — note: below $25k escalation threshold) AND related observation on Portsmith Marine (ARR $165k) provisioned day 1 |
| **Clarification** | Primary deviation: Highgrain Agribusiness (CM-11139) Closed Won Fri 2025-09-18 late evening; provisioned Thu 2025-09-25 (day 5 counting business days spanning weekend + one holiday? — documented as day 6 elapsed calendar path with 4 business days). Actually recorded deviation: Boreal Timber Partners provisioning KPI showed 6 business days due to pending credit review (CA-07) which appropriately gated activation. |
| **Reassessment** | Upon deeper investigation, Boreal Timber's delay was caused by **appropriate operation of CA-07 credit hold**, which is a higher-priority preventive control. KPI dashboard did not exclude credit-hold cases. |
| **Misstatement?** | No. |
| **Classification** | **Not a control deviation in substance** — KPI false positive. **Observation:** CA-35 dashboard logic should exclude or separately categorize credit-hold gated deals. Management agreed to enhance Looker KPI (completed Nov 2025). Removed from deficiency count; retained as process improvement note. Updated Section 5 table narrative: deviation reclassified to observation. |

## 6.7 Exception EX-06 — CA-38 Manual Journal Entry Template / Documentation (Significant Deficiency)

| Field | Detail |
|-------|--------|
| **Exception ID** | EX-06 |
| **Control** | CA-38 — Manual Journal Entry Restrictive Policy for Revenue Accounts |
| **Sample reference** | JE-07 / JE-2025-44155 dated 2025-12-31 for $75,000 |
| **What happened** | Controller M. Bell prepared and posted (with CFO A. Nguyen approval in NetSuite) a manual journal entry debiting Deferred Revenue — Current $75,000 and crediting Subscription Revenue $75,000 related to 'catch-up recognition for Enterprise Plus annual invoices activated Dec 22–23 where automated amortization start lagged by one day in schedule template.' The standardized JE template and supporting amortization recalculation workbook were **not attached in NetSuite at the time of posting** on Dec 31. The workbook was finalized and attached on Jan 3, 2026 during close continuation. Policy requires template + support uploaded **before** posting. |
| **Root cause** | Year-end time pressure; reliance on oral review between Controller and CFO; over-reliance on compensating knowledge of automated schedules. Indicates a lapse in a control designed specifically to mitigate **management override / non-standard entry risk (SR-REV-05)**. |
| **Misstatement?** | **No misstatement ultimately.** Engagement team independently recalculated the catch-up: automated schedules for CM-11301 and CM-11355 started amortization on Jan 1, 2026 rather than Dec 23–31, 2025, under-recognizing ~$9.9k; management's $75k entry was **not fully supported** at the detailed level. |
| **Critical substantive finding linked to control failure** | Upon auditor recalculation of the entire Dec 22–31 annual-activation population (7 invoices), total catch-up required was **$18,440**, not $75,000. Management recorded an **revising entry on Jan 8, 2026 (JE-2026-00112)** reversing $75,000 and posting $18,440. Because the revision occurred before issuance of the FY2025 financial statements, the final statements were correct. The initially proposed/posted FY2025 entry was overstated by $56,560 — above clearly trivial ($92,500)? Wait $56,560 < $92,500 clearly trivial — actually below clearly trivial. Recheck: clearly trivial $92,500; $56,560 is below CT. However qualitative factors matter for ICFR. |
| **Corrected quantitative analysis** | Absolute error in the manual entry as originally posted: $56,560 overstatement of revenue (and understatement of deferred revenue) relative to proper catch-up. Amount is **below clearly trivial threshold of $92,500**, and was corrected before report issuance. No adjustment was required to the final trial balance after JE-2026-00112. |
| **Why still an ICFR significant deficiency** | Per AS 2201, severity depends on likelihood and magnitude of potential misstatement. The control that failed is a **gatekeeper control over manual overrides to revenue/DR** — a significant fraud risk area. The potential magnitude of an undetected manual YE entry is not limited to $75k; privileged users could post larger amounts. Compensating controls (CA-18, CA-39) partially mitigate but CA-39 analytics **did flag** this entry in the January 2026 run (weekend/period-end/manual/senior-posted characteristics), and investigation occurred — however detection was **after** posting and after period-end. Likelihood of at least a misstatement that is more than inconsequential is higher than remote given the demonstrated failure mode. Magnitude of potential could be material if similar override occurred at larger scale. Accordingly, classify as **significant deficiency** (deficiency + less than material weakness because: entry was visible to CFO, CA-39 detective analytics operate monthly, substantive audit procedures would detect material revenue overrides, and actual error was corrected and immaterial). **Not a material weakness** because there is not a reasonable possibility that a material misstatement would not be prevented or detected on a timely basis, given CA-39, CA-41 rollforward precision, Disclosure Committee, and the limited actual loss of precision observed. |
| **Expanded testing** | Tested all remaining manual rev/DR JEs in November–December 2025 (full population 22 items). No other missing-template instances. Tested all 2025 manual JEs >$50k (11 items) for support — all others complete contemporaneously. |
| **Management response** | (1) NetSuite workflow enhanced Jan 2026 to **hard-block** posting to revenue/DR accounts without attachment of template file; (2) Controller training refresher; (3) CA-39 results to be reviewed by Audit Committee with specific focus on YE manual entries. Remediation testing to be performed as part of FY2026 interim. |
| **Communication** | To be communicated in writing to management and the Audit Committee as **Significant Deficiency SD-2025-01 — Manual Revenue Journal Entry Documentation Control**. |

### Quantitative Bridge Related to EX-06

| Description | Amount |
|-------------|--------|
| Original manual catch-up entry JE-2025-44155 | $75,000 |
| Auditor recalculated catch-up for Dec 22–31 annual activations | $18,440 |
| Difference (revenue overstatement if uncorrected) | $56,560 |
| Clearly trivial threshold | $92,500 |
| Performance materiality | $1,387,500 |
| Planning materiality | $1,850,000 |
| Correcting entry JE-2026-00112 (before report issuance) | Reverse $75,000; post $18,440 |
| Impact on final FY2025 issued financials | $0 (corrected) |

## 6.8 Exception EX-07 — CA-45 Access Termination Timeliness

| Field | Detail |
|-------|--------|
| **Exception ID** | EX-07 |
| **Control** | CA-45 — Okta Provisioning and Termination |
| **Sample references** | Leaver L-09 (terminated employee, Sales Ops Analyst) — access disabled in 3 BD; Leaver L-14 (contractor Billing) — access disabled in 2 BD; policy = 1 BD |
| **Misstatement?** | No. Logs reviewed showed no NetSuite or Chargebee transactions by either user post-termination HR date. |
| **Classification** | Aligns with ITGC low-severity deficiency; **ICFR deficiency (not significant)** given no inappropriate activity, short delays, and compensating CA-37 privileged access reviews / CA-36 SOD. |

## 6.9 Aggregation Analysis

| Deficiency / Deviation | Severity Alone | Aggregates With | Aggregate Conclusion |
|------------------------|----------------|-----------------|----------------------|
| EX-02 CPQ approval bypass window | Deficiency (not SD) | EX-03, EX-04, EX-07 | Related to change mgmt / timing discipline — still not SD in aggregate |
| EX-03 Integration SLA | Deficiency (not SD) | EX-02, EX-07 | Same as above |
| EX-04 Modification checklist timing | Deficiency (not SD) | EX-02 | Same as above |
| EX-07 Access termination SLA | Deficiency (not SD) | ITGC deficiencies | Not SD |
| EX-06 Manual JE template/support | **Significant Deficiency** | Standalone SD; consider whether with others elevate to MW | **Does not elevate to Material Weakness** — different root cause (override documentation) than operational SLA items; compensating detective controls remain precise enough relative to materiality |
| EX-01 / EX-05 | Not deficiencies / observation | N/A | N/A |

**Aggregation conclusion:** One significant deficiency (SD-2025-01 related to EX-06 / CA-38). Several lesser deficiencies that do not aggregate to an additional significant deficiency or material weakness. No material weakness identified in the revenue and deferred revenue cycle based on controls testing.

---

# 7. CONCLUSION
**Workpaper Reference: WP-REV-CON**

## 7.1 Overall Conclusion on Controls

Based on the procedures documented in this workpaper — including risk assessment, design evaluation of **50 key control activities**, operating effectiveness testing over interim and year-end periods, sample selections as detailed in Section 4, testing results in Section 5, and exceptions analysis in Section 6 — we conclude as follows for CloudMeridian Software, Inc. for the fiscal year ended December 31, 2025:

1. **Design:** Controls CA-01 through CA-50 relevant to subscription revenue, billing, cash application, and deferred revenue were **designed effectively** to address the assessed risks of material misstatement, including significant risks SR-REV-01 through SR-REV-06, at the assertion level.

2. **Operating effectiveness:** Except for the significant deficiency noted below, controls were **operating effectively** throughout the period of reliance (January 1, 2025 through December 31, 2025, with emphasis on testing coverage across interim and rollforward windows). Forty-two controls operated without deviation; seven items reflected isolated deviations or lesser deficiencies that did not rise to a significant deficiency; one control (CA-38) gave rise to a significant deficiency.

3. **Significant deficiency:** **SD-2025-01 — Manual Revenue / Deferred Revenue Journal Entry Documentation Control (CA-38)** — Management did not consistently attach standardized templates and supporting calculations prior to posting a non-standard year-end manual journal entry affecting deferred revenue and subscription revenue. Although the entry was approved by the CFO, was subsequently corrected before issuance based on auditor recalculation (final catch-up $18,440 vs. originally posted $75,000), and did not result in misstatement of the issued financial statements, the control failure relates to a significant fraud risk (management override) and creates a reasonable possibility that a misstatement that is more than inconsequential would not be prevented or detected on a timely basis. Compensating controls reduce the likelihood that a **material** misstatement would go undetected; accordingly, this is a **significant deficiency, not a material weakness**.

4. **Material weakness:** **None identified** in the subscription revenue and deferred revenue cycle based on the results of our ICFR testing.

5. **Prior-year significant deficiencies** SD-2024-03 and SD-2024-07 were **successfully remediated** and operated effectively in FY2025.

6. **ITGC reliance:** Maintained for Salesforce, Chargebee, Stripe, NetSuite, Workato, and Okta, supporting reliance on automated application controls CA-03, CA-15, CA-25, and related automated components, subject to the low-severity access termination matters consistent with EX-07.

## 7.2 Implications for the Financial Statement Audit

| Area | Implication |
|------|-------------|
| Controls reliance for substantive nature/timing/extent | **Generally achieved** for routine automated billing, deferred revenue schedule creation, and monthly amortization — substantive sample sizes set at reliance levels per audit plan |
| Response to SD-2025-01 | **Increase substantive scrutiny** of manual JEs affecting revenue and deferred revenue; extend JE testing around year-end; independently recalculate any non-standard catch-up or top-side entries; do not reduce substantive procedures in the management override pathway |
| Fraud procedures | Continue presumed fraud risk response for revenue; CA-39 monitoring noted as important compensating control |
| Deferred revenue substantive procedures | Maintain rollforward substantiation, annual prepaid completeness testing, and cutoff testing; controls reliance supported except where manual intervention occurs |
| Uncorrected misstatements | None remaining in final balances related to exceptions herein |

## 7.3 Implications for the ICFR Opinion

Subject to completion of remaining engagement-level procedures and partner review of the aggregate ICFR conclusion across all cycles, the results in this workpaper support an opinion that the Company maintained, in all material respects, effective internal control over financial reporting as of December 31, 2025, under COSO 2013, **with disclosure of significant deficiency SD-2025-01 to management and the Audit Committee** (significant deficiencies are communicated in writing but do not, by themselves, preclude an unqualified ICFR opinion when no material weakness exists).

## 7.4 Management Letter Points (Control Improvements)

| MLP # | Related EX | Recommendation | Priority |
|-------|------------|----------------|----------|
| MLP-01 | EX-06 / SD-2025-01 | Enforce NetSuite hard-block on revenue/DR postings without attached template; require secondary Accounting reviewer distinct from preparer for all YE manual rev/DR entries regardless of CFO approval | High — in process |
| MLP-02 | EX-02 | Extend CA-43-type change management discipline to Salesforce CPQ metadata deploys; add post-deploy approval-rule monitoring for 72 hours | Medium — implemented Jul–Aug 2025 |
| MLP-03 | EX-03 | Clarify integration SLA relative to month-end close; auto-escalate any open revenue integration failure within 2 BD of month-end | Medium |
| MLP-04 | EX-04 | System-enforce modification checklist completion gate in Salesforce before Chargebee quantity/price changes above $5k ARR | Medium |
| MLP-05 | EX-01 / EX-05 | Enhance exception dashboards (timezone test coverage; credit-hold exclusions in provisioning KPI) | Low — largely implemented |
| MLP-06 | EX-07 | Align HR/IT termination SLA operationally to one business day with same-day disabled status for privileged NetSuite roles | Medium |

## 7.5 Cross-References to Related Workpapers

| Topic | Workpaper Ref |
|-------|---------------|
| Walkthrough narratives & screenshots | WP-REV-WT-001 to WP-REV-WT-008 |
| Substantive revenue testing | WP-REV-SUB-001 et seq. |
| Deferred revenue substantive rollforward | WP-REV-SUB-DR-001 |
| Journal entry testing (fraud) | WP-JE-001 |
| ITGC testing & conclusion | WP-ITGC-001 to WP-ITGC-CON |
| Materiality | WP-ADM-MAT-001 |
| Fraud brainstorming | WP-ADM-FR-001 |
| Audit Committee communications draft | WP-AC-SD-2025-01 |
| Sample detail spreadsheet | WP-REV-SS-DETAIL.xlsx |

## 7.6 Sign-Offs

| Role | Name | Signature / Initials | Date |
|------|------|----------------------|------|
| Preparer | Jordan Hale, Senior Associate | JH | February 14, 2026 |
| Detail reviewer | Morgan Ellis, Audit Manager | ME | February 21, 2026 |
| Engagement partner | Priya Venkatesh, Partner | PV | February 28, 2026 |
| EQCR (if applicable) | N/A for this cycle memo — EQCR on overall ICFR file | — | — |

## 7.7 Closing Narrative

CloudMeridian Software, Inc.'s SaaS revenue model — approximately **500 customers**, predominantly **monthly subscription billing**, and material **deferred revenue balances** totaling approximately **$4.87 million** at December 31, 2025 — presents elevated inherent risk around occurrence, accuracy, cutoff, and deferred revenue completeness/valuation. The Company's control structure of **50 key control activities** spanning contract execution, pricing, provisioning, billing completeness, integration monitoring, deferred revenue automation, period-end close, access/SOD, and monitoring activities is, in our judgment, suitably designed for the scale and complexity of the entity.

Operating effectiveness was strong across automated and routine manual controls, including full-population comfort over prepaid invoice deferred revenue schedule creation. The principal adverse finding from our testing is the year-end manual journal entry documentation lapse (SD-2025-01), which underscores the persistent importance of disciplined controls over management override pathways even in highly automated SaaS billing environments. After considering compensating controls, expanded testing, substantive corroboration, and pre-issuance correction of the related accounting entry, we conclude that this matter is a significant deficiency and not a material weakness, and that controls reliance remains appropriate for the routine revenue and deferred revenue processes subject to the substantive enhancements noted above.

This workpaper contains **fictional** entity names, amounts, personnel, and testing results prepared solely for illustrative / training / demonstration purposes. It does not represent an actual audit engagement, nor does it constitute audit advice, legal advice, or an opinion on any real entity's financial statements or internal control.

---

**END OF WORKPAPER WP-REV-001 (COMPREHENSIVE REVENUE & DEFERRED REVENUE CONTROLS FILE)**

*Document classification: Confidential — Audit Work Product (Fictional Demonstration)*
