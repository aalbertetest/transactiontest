---
> **IMPORTANT NOTICE — FICTIONAL ILLUSTRATIVE DOCUMENT**
> Nexora Technologies, Inc., all subsidiaries, personnel, financial results, risk factors, and events referenced in this memo are **entirely fictional** and created solely for illustrative, educational, and training purposes. This document does not describe, and should not be attributed to, any real company, auditor, or individual, living or dead. It is not investment, accounting, legal, or audit advice and should not be relied upon as such. Any resemblance to actual companies, engagements, or persons is coincidental.
---

# AUDIT PLANNING MEMORANDUM

**Client:** Nexora Technologies, Inc. and Subsidiaries ("Nexora," "the Company," or "the Group")
**Engagement:** Integrated Audit of Financial Statements and Internal Control Over Financial Reporting
**Fiscal Year End:** December 31, 2025
**Audit Firm:** Harrow & Vance LLP, Independent Registered Public Accounting Firm
**Office:** Austin, Texas — Technology, Media & Telecommunications Practice
**Engagement Code:** NXRA-FY25-001
**Memo Date:** December 15, 2025 (Planning Phase — Interim)
**Distribution:** Engagement Partner, Engagement Quality Reviewer, Audit Manager, Senior Associates, IT Audit Specialist, National Office (Complex Accounting Matters Group)

**Prepared by:** J. Alvarez, Senior Manager
**Reviewed by:** T. Okafor, Engagement Partner
**Concurring Review:** M. Chen, Engagement Quality Reviewer

---

## TABLE OF CONTENTS

1. Executive Summary
2. Engagement Background and Terms of Engagement
3. Overview of Nexora Technologies, Inc.
4. Audit Objectives, Scope, and Overall Strategy
5. Materiality and Performance Materiality
6. Industry Analysis
7. Economic Outlook and Macro-Environmental Factors
8. Artificial Intelligence Trends and Their Effect on the Audit
9. Revenue Recognition Risks
10. Fraud Risk Assessment
11. Information Technology Risks
12. Cybersecurity Risk Assessment
13. Control Environment Assessment (COSO Framework)
14. Walkthrough Observations
15. Significant Accounting Estimates
16. Overall Audit Response, Timeline, and Staffing
17. Appendices

---

## 1. EXECUTIVE SUMMARY

This planning memorandum documents Harrow & Vance LLP's ("the Firm," "we," "our") understanding of Nexora Technologies, Inc. ("Nexora" or "the Company"), its industry, its economic environment, and the risks of material misstatement (whether due to error or fraud) relevant to the audit of the Company's consolidated financial statements and internal control over financial reporting ("ICFR") for the fiscal year ending December 31, 2025. This memo is prepared in accordance with PCAOB Auditing Standards, including AS 1101 (Audit Risk), AS 1105 (Audit Evidence), AS 2101 (Audit Planning), AS 2105 (Consideration of Materiality in Planning and Performing an Audit), AS 2110 (Identifying and Assessing Risks of Material Misstatement), AS 2201 (An Audit of Internal Control Over Financial Reporting That Is Integrated with An Audit of Financial Statements), and AS 2401 (Consideration of Fraud in a Financial Statement Audit).

Nexora is a publicly traded (NASDAQ: NXRA) enterprise software company headquartered in Austin, Texas, that designs, develops, and sells artificial-intelligence-enabled data analytics, cybersecurity, and cloud infrastructure software to mid-market and enterprise customers globally. For the year ending December 31, 2025, management's preliminary (unaudited) estimates indicate consolidated revenue of approximately $2.41 billion, up from $1.98 billion in fiscal 2024, driven substantially by growth in the Company's generative-AI-enabled analytics product, "NexoraIQ Copilot," and by the July 2025 acquisition of ShieldNex Corporation, a cybersecurity posture-management vendor.

Based on our preliminary risk assessment procedures — including inquiry of management, the audit committee, and internal audit; analytical review of interim financial information; walkthroughs of significant processes; and our understanding of the industry and regulatory environment — we have identified the following as the **fraud risk (presumed) and significant risk areas** that will receive heightened audit attention during fiscal 2025:

1. **Revenue recognition** under ASC 606, particularly (a) standalone selling price ("SSP") determination and allocation across multiple performance obligations in bundled arrangements combining subscription, usage-based AI compute, and professional services; (b) the presumed fraud risk related to management override of controls in revenue recognition (a rebuttable presumption under AS 2401.44 that we have not rebutted); (c) channel partner and distributor sell-through arrangements; and (d) the accounting for the ShieldNex acquisition's deferred revenue haircut and its effect on post-acquisition revenue trends.
2. **Business combination accounting** for the ShieldNex acquisition (purchase price allocation, valuation of acquired intangible assets, contingent consideration, and goodwill).
3. **Goodwill and long-lived asset impairment**, given softening in certain legacy on-premises product lines and a sustained decline in Nexora's market capitalization relative to book value during Q3 2025.
4. **Capitalized internal-use software and AI model development costs**, an area with significant management judgment regarding the technological feasibility threshold and useful life estimates, and evolving practice regarding the capitalization of costs to train and fine-tune large language models.
5. **Stock-based compensation**, including a new AI-talent retention award program with market-condition vesting tied to NexoraIQ Copilot annual recurring revenue ("ARR") milestones, requiring complex Monte Carlo valuation.
6. **Income taxes**, including the realizability of deferred tax assets, the Company's transfer pricing arrangements for its Irish and Indian AI research subsidiaries, and the impact of the OECD Pillar Two global minimum tax rules effective for the Company beginning in fiscal 2025.
7. **Information technology general controls ("ITGCs")** across the Company's hybrid multi-cloud environment (AWS and Microsoft Azure), including access provisioning following the ShieldNex acquisition integration, change management over AI model deployment pipelines, and the timeliness of user access reviews.
8. **Cybersecurity**, including the Company's obligations under the SEC's cybersecurity disclosure rules (Item 1.05 of Form 8-K and Item 106 of Regulation S-K), a disclosed but immaterial security incident in April 2025 involving a third-party SaaS vendor, and the completeness of the Company's cybersecurity risk management disclosures.

Our overall audit strategy contemplates a **combined (controls-reliance) approach** for the majority of financially significant processes, supplemented by substantive procedures over areas of significant judgment and estimation uncertainty. We have set overall (planning) materiality for the consolidated financial statements at **$36.2 million** (approximately 1.5% of forecasted pre-tax income adjusted for non-recurring items, cross-checked against 0.5% of total revenue and 3% of forecasted EBITDA), with performance materiality of **$27.1 million** (75% of overall materiality) and a nominal (trivial) threshold for accumulating uncorrected misstatements of **$1.81 million** (5% of overall materiality). These thresholds are discussed further in Section 5.

No matters have come to our attention during planning that would preclude us from accepting or continuing the engagement. This memo should be read together with the engagement team's risk assessment summary (Appendix A), the fraud brainstorming session minutes (Appendix B), the IT audit scoping memo (Appendix C), and the group audit instructions issued to component auditors (Appendix D).

### 1.1 Summary of Key Planning Conclusions

For ease of reference, the table below summarizes the principal planning conclusions detailed throughout this memo:

| Planning Element | Conclusion | Section |
|---|---|---|
| Overall audit strategy | Combined (controls-reliance) approach for routine transaction cycles; fully substantive for judgmental/non-routine balances | Section 4.3 |
| Overall materiality | $36.2 million | Section 5.2 |
| Performance materiality | $27.1 million | Section 5.2 |
| Nominal/trivial threshold | $1.81 million | Section 5.2 |
| Significant risks identified | Revenue recognition (SSP, variable consideration, ShieldNex deferred revenue, principal/agent); business combination accounting; goodwill/intangible impairment; capitalized software; stock-based compensation; income taxes | Sections 9, 15 |
| Fraud risks identified | Improper revenue recognition (presumed); management override (presumed); non-GAAP/KPI manipulation; EMEA side-letter risk; improper capitalization; purchase accounting manipulation; related-party matters | Section 10.5 |
| Likely critical audit matters | Revenue recognition; ShieldNex business combination; goodwill impairment (preliminary, subject to completion-stage confirmation) | Section 16.5 |
| Prior-year significant deficiencies | Two identified in FY2024; management asserts remediation; independent retesting planned | Sections 11.6, 13.6 |
| New-year control observations | ShieldNex access/identity integration gaps; delayed UAR; DOA policy lag; DR test gap for ShieldNex environment | Sections 11.3, 11.5.1, 13.6 |
| Going concern | No indicators identified as of planning date; will be reassessed each period | Section 7.4 |
| Use of specialists | IT audit, valuation, and tax specialists; National Office consultation planned on two matters | Section 4.4 |
| Group audit scope | Nexora India — specified procedures via component auditor; all other entities — full scope or analytical procedures only | Section 4.2 |

### 1.2 Basis of Preparation and Limitations

This memorandum is based on information available to the engagement team as of the planning date, including preliminary and unaudited management forecasts, interim financial information, and the results of planning-stage risk assessment procedures, including walkthroughs performed through early December 2025. It does not constitute a final assessment of any account balance, disclosure, or control, and all preliminary conclusions expressed herein (including as to the design or operating effectiveness of controls, the adequacy of specific accounting treatments, or the classification of identified matters as deficiencies, significant deficiencies, or material weaknesses) remain subject to change based on the results of further audit procedures performed during interim and year-end fieldwork. This memo is prepared solely for the internal use of the Harrow & Vance LLP engagement team, the EQR, and, where relevant matters are summarized for communication purposes, the Nexora audit committee, and is not intended for any other purpose or distribution.

---

## 2. ENGAGEMENT BACKGROUND AND TERMS OF ENGAGEMENT

### 2.1 Engagement History

Harrow & Vance LLP has served as Nexora's independent registered public accounting firm since the Company's initial public offering in March 2019. T. Okafor has served as engagement partner since fiscal year 2023, rotating in accordance with the Firm's five-year partner rotation policy and Rule 3211 of PCAOB standards on partner rotation. The prior engagement partner, R. Whitfield, rotated off after the fiscal 2022 audit and remains available for consultation during a two-year cooling-off period, consistent with independence requirements.

This is the third year of our current engagement letter, which was renewed on January 10, 2025, and covers the audit of the fiscal 2025, 2026, and 2027 consolidated financial statements and ICFR. The audit committee reappointed Harrow & Vance at the Company's annual meeting on May 14, 2025, following a competitive tender process conducted in fiscal 2022 in which the Firm was selected over two other Big Four-adjacent firms.

### 2.2 Nature of the Engagement

We have been engaged to:

- Express an opinion on whether Nexora's consolidated financial statements are presented fairly, in all material respects, in accordance with U.S. GAAP;
- Express an opinion on the effectiveness of Nexora's internal control over financial reporting as of December 31, 2025, in accordance with the framework established by the Committee of Sponsoring Organizations of the Treadway Commission (COSO, 2013 Internal Control — Integrated Framework);
- Perform an integrated audit under PCAOB standards, given Nexora's status as an accelerated filer required to obtain an ICFR opinion under Section 404(b) of the Sarbanes-Oxley Act;
- Review the Company's interim financial information for each of the first three quarters of fiscal 2025 in accordance with AS 4105;
- Issue a consent and comfort letter in connection with a shelf registration statement the Company filed on Form S-3 in September 2025; and
- Communicate required matters to the audit committee in accordance with AS 1301.

### 2.3 Independence and Ethical Requirements

The engagement team has confirmed independence in accordance with the SEC's independence rules, PCAOB Rule 3520, and the Firm's internal independence policies. All partners and covered persons on the engagement have completed independence affirmations for fiscal 2025. We noted no prohibited financial relationships, business relationships, or non-audit services performed for Nexora during the period that would impair independence. Non-audit services performed during fiscal 2025 were limited to (a) audit-related services (comfort letters, consents, and a Type 2 SOC report readiness assessment for a Nexora subsidiary that provides payment-processing services to third parties), and (b) permissible tax compliance services for two dormant foreign subsidiaries, all of which were pre-approved by the audit committee in accordance with its pre-approval policy.

### 2.4 Client Acceptance and Continuance

The engagement quality reviewer and the engagement partner completed the annual client continuance evaluation on November 3, 2025. Factors considered included: the integrity and reputation of management and those charged with governance; the Company's financial stability (Nexora maintains an investment-grade-adjacent credit profile with a leverage ratio of 1.4x net debt to EBITDA); the reasonableness of fee arrangements; the absence of any unresolved regulatory inquiries (see Section 6.6 regarding a routine, non-material SEC comment letter); and the results of the fiscal 2024 audit, which was completed with an unqualified opinion on the financial statements and an unqualified opinion on ICFR, with two significant deficiencies identified and remediated during fiscal 2025 (discussed in Section 13.6). We concluded that continuance is appropriate.

---

## 3. OVERVIEW OF NEXORA TECHNOLOGIES, INC.

### 3.1 Corporate History and Structure

Nexora Technologies, Inc. was founded in 2011 in Austin, Texas, by co-founders Priya Mehta (current Chief Executive Officer) and David Kessler (current Chief Technology Officer), originally as a business-intelligence dashboarding tool for mid-market retailers. The Company completed its initial public offering on the Nasdaq Global Select Market on March 21, 2019, raising net proceeds of approximately $412 million. Nexora's fiscal year ends December 31.

As of the date of this memo, Nexora comprises the following material legal entities, all of which are included within the scope of the group audit:

| Entity | Jurisdiction | Function | Component Materiality Classification |
|---|---|---|---|
| Nexora Technologies, Inc. (Parent) | Delaware, USA | Corporate HQ, U.S. sales, R&D | Significant — full scope |
| Nexora Software Ireland Ltd. | Ireland | EMEA sales, AI research, IP licensing hub | Significant — full scope |
| Nexora India Private Limited | India | R&D, engineering, customer support | Significant — specified procedures |
| ShieldNex Corporation | Delaware, USA | Cybersecurity posture management (acquired July 2025) | Significant — full scope |
| Nexora Pay Solutions LLC | Delaware, USA | Embedded payment processing for marketplace customers | Non-significant — analytical procedures |
| Nexora K.K. | Japan | APAC sales and support | Non-significant — analytical procedures |
| Nexora Brasil Tecnologia Ltda. | Brazil | LATAM sales and support | Non-significant — analytical procedures |

Nexora's headcount as of September 30, 2025, was approximately 8,240 employees globally, of which roughly 3,100 are in research and development (including approximately 640 employees added through the ShieldNex acquisition and approximately 210 machine learning engineers and data scientists dedicated to the Company's foundation-model fine-tuning and AI infrastructure teams).

### 3.2 Products and Service Lines

Nexora organizes its business into three reportable segments for financial reporting purposes, consistent with the information regularly reviewed by the Company's chief operating decision maker (the CEO), per ASC 280:

**(a) Platform & Subscription Segment (approximately 74% of FY2025 forecasted revenue).** This segment includes the Company's core software-as-a-service offerings:
- *NexoraIQ* — a cloud-based data analytics and business-intelligence platform sold on a subscription basis, typically under one- to three-year contracts with annual or upfront billing.
- *NexoraIQ Copilot* — a generative-AI add-on module, launched in beta in Q3 2024 and generally available since February 2025, that allows customers to query enterprise data using natural language, powered by a combination of a licensed third-party large language model (via API arrangements with a major foundation-model provider) and Nexora's proprietary fine-tuned retrieval-augmented generation ("RAG") layer. Copilot is priced on a hybrid basis: a fixed subscription uplift plus consumption-based pricing for compute-intensive "agentic" workflows measured in "Nexora AI Credits."
- *ShieldNex Cloud Security Posture Management ("CSPM")* — acquired July 1, 2025, providing continuous cloud misconfiguration scanning and compliance monitoring, sold on subscription terms consistent with Nexora's other SaaS offerings.

**(b) Marketplace & Usage-Based Segment (approximately 16% of FY2025 forecasted revenue).** The Nexora AI Marketplace allows customers to access, within the NexoraIQ platform, a curated set of third-party and proprietary machine learning models for tasks such as demand forecasting, anomaly detection, and document extraction. Revenue is generated primarily on a consumption (usage-based) model, with Nexora acting as principal for proprietary models and generally as agent (net presentation) for certain third-party models, a distinction discussed further in Section 9.

**(c) Professional Services & Support Segment (approximately 10% of FY2025 forecasted revenue).** Includes implementation services, custom AI model fine-tuning engagements, training, and premium support arrangements, typically billed on a time-and-materials or fixed-fee basis.

### 3.3 Customers, Market Position, and Competition

Nexora serves approximately 6,400 enterprise and mid-market customers across financial services, retail, healthcare, and manufacturing verticals. The Company's largest customer accounted for approximately 3.1% of FY2025 forecasted revenue; no single customer exceeds 10% of revenue or accounts receivable, and management does not consider the Company to have significant customer concentration risk at the consolidated level, although we will independently evaluate this assertion (see Section 9.6). Net revenue retention for the trailing twelve months ended September 30, 2025, was reported by management at 118%, and gross revenue retention (excluding upsell) was reported at 91%.

Nexora competes against large, diversified enterprise software vendors with substantially greater financial resources, as well as a growing number of well-funded, venture-backed "AI-native" analytics startups. Management has identified the pace of foundation-model innovation and the risk of platform disintermediation (i.e., customers building similar natural-language analytics capabilities directly atop foundation-model APIs, bypassing specialized vendors like Nexora) as a principal competitive risk, which we discuss further in Sections 6 and 8.

### 3.4 Capital Structure and Financing

As of September 30, 2025, Nexora had approximately 168.4 million shares of common stock outstanding, a market capitalization of approximately $9.1 billion (implying a revenue multiple of approximately 3.8x forecasted FY2025 revenue, below the Company's five-year historical average multiple of 6.2x — a trend discussed in the context of goodwill impairment indicators in Section 15.3). The Company has $600 million of 2.25% convertible senior notes due 2029, issued in June 2024, and an undrawn $250 million revolving credit facility. The ShieldNex acquisition (total consideration of approximately $740 million) was funded through a combination of $450 million cash on hand, $150 million drawn and subsequently repaid under the revolver, and $140 million in Nexora common stock issued to ShieldNex equity holders.

### 3.5 Selected Preliminary Financial Highlights (Management Forecast, Unaudited)

The following selected financial data, drawn from management's Q3 2025 forecast package, informed our planning-stage analytical procedures and materiality determination (Section 5):

| ($ in millions, except per share and ratios) | FY2023 (Actual) | FY2024 (Actual) | FY2025 (Forecast) |
|---|---|---|---|
| Total revenue | 1,612.4 | 1,984.7 | 2,410.0 |
| Revenue growth % | 24.1% | 23.1% | 21.4% |
| Gross profit | 1,225.4 | 1,469.1 | 1,712.1 |
| Gross margin % | 76.0% | 74.0% | 71.1% |
| GAAP operating income (loss) | 42.3 | 61.5 | 58.9 |
| Non-GAAP operating income | 289.8 | 367.2 | 434.0 |
| Net income (loss) attributable to common stockholders | 11.7 | 33.4 | 29.2 |
| Diluted EPS | 0.07 | 0.20 | 0.17 |
| Cash, cash equivalents, and short-term investments | 742.6 | 823.9 | 890.4 |
| Total assets | 3,890.2 | 4,415.6 | 5,180.3 |
| Total stockholders' equity | 2,240.8 | 2,617.3 | 2,981.5 |
| Cash flow from operations | 241.9 | 278.4 | 310.2 |
| Stock-based compensation expense | 178.3 | 214.6 | 268.9 |
| Deferred revenue (current + long-term) | 612.4 | 748.2 | 891.7 |
| Days sales outstanding | 52 | 57 | 61 |
| Net revenue retention | 112% | 115% | 118% |

We noted the widening gap between GAAP operating income and non-GAAP operating income (driven principally by stock-based compensation, amortization of acquired intangibles following the ShieldNex acquisition, and acquisition/integration costs) as a specific area for continued analytical monitoring, given its relevance to the fraud risk indicators discussed in Section 10.2 regarding the market's and management's own incentive focus on non-GAAP metrics.

### 3.6 Governance

Nexora's board of directors comprises nine members, seven of whom are independent under Nasdaq listing standards. The audit committee consists of four independent directors, including Chair L. Fitzgerald (a former CFO of a publicly traded semiconductor company, qualifying as the audit committee financial expert), and meets at least quarterly, with additional sessions as needed. The Company maintains an internal audit function of twelve professionals led by the Chief Audit Executive, S. Ramirez, who reports functionally to the audit committee and administratively to the CFO. We have evaluated the objectivity and competence of internal audit in accordance with AS 2605 and plan to use their work, to a limited extent, over certain lower-risk operational controls, as discussed in Section 16.4.

---

## 4. AUDIT OBJECTIVES, SCOPE, AND OVERALL STRATEGY

### 4.1 Objectives

The objectives of this engagement are to obtain reasonable assurance about whether the consolidated financial statements are free of material misstatement, whether due to fraud or error, and to form an opinion on the operating effectiveness of ICFR as of the balance sheet date. We will also comply with our responsibilities to communicate with the audit committee regarding critical accounting estimates, significant unusual transactions, and other matters required under AS 1301, and to evaluate the Company's compliance, in all material respects, with the SEC's cybersecurity disclosure requirements to the extent they intersect with the financial statements and related disclosures (Section 12.7).

### 4.2 Scope of the Group Audit

We are acting as the group engagement team with respect to all entities listed in Section 3.1. Nexora India Private Limited will be subject to specified audit procedures performed by our component auditor, Harrow & Vance India LLP (a network firm), under our direct supervision, given its role in R&D cost accumulation relevant to capitalized software costs and its December 31 statutory fiscal year-end alignment. We have reviewed the component team's independence, qualifications, and the results of our oversight procedures, including a planned visit by the U.S. engagement manager to the Bangalore office in February 2026 to review capitalized software cost support.

### 4.3 Overall Audit Strategy

We have elected a **combined approach**, relying on the operating effectiveness of controls for the following significant classes of transactions, supplemented with substantive analytical procedures and tests of details: order-to-cash (subscription billing and revenue recognition), procure-to-pay, payroll and stock compensation, and the financial statement close process. We have elected a **fully substantive approach** for the following areas, given either the nature of the balances (non-routine, judgmental) or cost-benefit considerations: business combination accounting (ShieldNex), goodwill and intangible asset impairment testing, income taxes, and legal contingencies.

Our overall audit strategy reflects a **top-down, risk-based approach** consistent with AS 2201, beginning with entity-level controls, followed by significant accounts and disclosures, relevant assertions, and, for each relevant assertion, the identification of likely sources of potential misstatement before selecting controls to test.

### 4.4 Use of Specialists

The engagement will involve the following internal and external specialists:
- **IT Audit Specialists** (2 FTE) — ITGC testing across AWS/Azure environments, data extraction and analytics, and testing of automated controls within the NetSuite ERP and Salesforce CPQ/billing systems.
- **Valuation Specialists** — review of management's ShieldNex purchase price allocation, the Monte Carlo valuation model for market-condition stock awards, and the discounted cash flow models supporting goodwill impairment testing.
- **Tax Specialists** — evaluation of the Company's transfer pricing documentation, the Pillar Two global minimum tax computation, and the realizability of deferred tax assets.
- **National Office Consultation** — planned consultations on (a) the accounting for the AI Marketplace principal-versus-agent evaluation under ASC 606-10-55, and (b) the capitalization boundary for AI model training costs, an area lacking specific authoritative guidance.

---

## 5. MATERIALITY AND PERFORMANCE MATERIALITY

### 5.1 Basis for Materiality

In accordance with AS 2105, we determined planning materiality using multiple benchmarks, reflecting the fact that Nexora is a growth-oriented technology company where investors and analysts focus not only on GAAP net income but also on revenue growth, non-GAAP operating income, and annual recurring revenue. The engagement team considered the following benchmarks based on management's Q3 2025 forecast:

| Benchmark | Amount ($M) | Rate Applied | Resulting Materiality ($M) |
|---|---|---|---|
| Total revenue | 2,410.0 | 0.5% – 1.0% | 12.1 – 24.1 |
| Forecasted pre-tax income (adjusted for acquisition and restructuring costs) | 241.0 | 5% – 10% (lower end given volatility) | 12.1 – 24.1 |
| Forecasted non-GAAP EBITDA | 434.0 | 5% – 8% | 21.7 – 34.7 |
| Total assets | 5,180.0 | 0.5% – 1.0% | 25.9 – 51.8 |
| Market capitalization | 9,100.0 | 0.3% – 0.5% | 27.3 – 45.5 |

Given (a) the volatility and non-recurring items affecting pre-tax income (acquisition costs, restructuring), (b) the primacy of revenue and EBITDA as key metrics used by the market and by the Company's own incentive compensation plans (a fraud risk indicator discussed in Section 10.4), and (c) consistency with the approach used in the fiscal 2024 audit, we determined that a **blended revenue/EBITDA-weighted approach**, cross-checked to total assets, was most appropriate.

### 5.2 Materiality Determination

- **Overall (Planning) Materiality:** $36.2 million, representing approximately 1.5% of total revenue and approximately 8.3% of forecasted non-GAAP EBITDA.
- **Performance Materiality:** $27.1 million (75% of overall materiality), reflecting a moderate-to-elevated aggregation risk given the number of components, the pervasiveness of estimation uncertainty (Section 15), and the identified fraud risk related to revenue recognition and management override.
- **Specific Materiality — Related Party and Executive Compensation Disclosures:** $5.0 million, reflecting heightened sensitivity of these disclosures notwithstanding their quantitative immateriality to the financial statements as a whole.
- **Nominal (Trivial) Threshold:** $1.81 million (5% of overall materiality); individual misstatements below this threshold will generally not be accumulated on the summary of unadjusted differences, subject to qualitative override.

### 5.3 Qualitative Factors

Consistent with SEC Staff Accounting Bulletin No. 99 and No. 108, we will evaluate identified misstatements not only by magnitude but also with regard to qualitative factors, including: (a) whether a misstatement changes a loss into income or vice versa; (b) whether it affects compliance with debt covenants under the revolving credit facility (which include a maximum net leverage ratio and a minimum liquidity covenant); (c) whether it affects the achievement of analyst consensus revenue or EPS estimates (Nexora has met or beaten consensus revenue estimates in 15 of the last 16 quarters, a pattern discussed further as a fraud risk indicator in Section 10.3); (d) whether it relates to a key performance indicator disclosed to investors, such as ARR or net revenue retention; and (e) whether it involves concealment of an unlawful transaction.

### 5.4 Materiality Will Be Reassessed

We will revisit materiality at the completion stage using actual (rather than forecasted) fiscal 2025 results and will document any changes and their rationale in the completion memorandum.

---

## 6. INDUSTRY ANALYSIS

Understanding the industry in which Nexora operates is a required component of our risk assessment under AS 2110.07–.09. This section documents our understanding of the enterprise software, data analytics, and cybersecurity industries, the competitive dynamics affecting Nexora, and the implications for the audit.

### 6.1 Industry Structure and Segmentation

Nexora operates at the intersection of three overlapping software sub-industries:

**(a) Enterprise data analytics and business intelligence ("BI").** This is a mature, consolidating market historically dominated by a small number of large vendors offering visualization and reporting tools, alongside a "long tail" of specialized analytics vendors. Total addressable market estimates compiled by management, sourced from a third-party industry research report (which we will evaluate for reliability as management's specialist information under AS 1105.16–.20 to the extent used to support disclosures or estimates), place the global BI/analytics software market at approximately $58 billion in calendar 2025, growing at a compound annual growth rate of approximately 9–11% through 2029. Growth in this segment has decelerated over the past three years as the market matures, making the AI-driven expansion into adjacent categories (see 6.1(c)) strategically important to Nexora's continued growth narrative.

**(b) Cloud cybersecurity posture management and compliance monitoring.** The market Nexora entered via the ShieldNex acquisition is younger and more fragmented, characterized by rapid product iteration, frequent M&A consolidation among point-solution vendors, and increasing convergence with broader cloud-native application protection platform ("CNAPP") offerings. Industry sources estimate this sub-market at approximately $9 billion in calendar 2025, growing at 22–27% annually, reflecting continued enterprise migration to multi-cloud architectures and heightened regulatory attention to cloud misconfigurations following several high-profile industry breaches in calendar 2023–2024.

**(c) Generative AI-enabled enterprise applications ("agentic AI" and "copilot" categories).** This is the newest and most rapidly evolving segment, in which Nexora's Copilot product competes. Because this category did not meaningfully exist prior to calendar 2023, there is limited reliable historical industry data, and forecasts among industry analysts vary widely — a factor we consider relevant both to our evaluation of management's use of this data in strategic disclosures (e.g., Risk Factors in the Form 10-K) and to our skepticism regarding management's own internal forecasts used in impairment and going-concern-adjacent analyses.

### 6.2 Competitive Dynamics and Business Risk Implications

We identified the following industry-level dynamics as most relevant to our risk assessment:

1. **Compressed sales cycles and increased discounting.** Industry commentary and Nexora's own management indicate that enterprise software buyers have become more price-sensitive amid a multi-year environment of scrutinized IT budgets, resulting in longer sales cycles for large multi-year commitments but increased willingness among vendors, including Nexora, to offer significant discounts, extended payment terms, and "ramp" pricing (lower fees in contract year one, escalating in later years) to close deals near quarter-end. This dynamic is directly relevant to our revenue recognition risk assessment (Section 9), particularly with respect to variable consideration, SSP determination, and the risk of side letters or non-standard terms that are not appropriately reflected in the revenue recognition system of record.

2. **Vendor consolidation and "platform" purchasing behavior.** Enterprise customers increasingly prefer to consolidate spend with fewer, broader platform vendors rather than "best of breed" point solutions, which is the strategic rationale management has articulated for the ShieldNex acquisition and for planned further tuck-in acquisitions disclosed in the Company's Q3 2025 earnings call. This trend elevates the importance of our review of business combination accounting (Section 15.2) and increases the likelihood of further material acquisitions during the remainder of the audit period requiring subsequent-events consideration.

3. **Usage-based ("consumption") pricing models.** The shift from purely subscription-based to hybrid or fully consumption-based pricing — driven by the variable cost structure of AI compute (large language model inference costs charged by cloud and foundation-model providers) — is an industry-wide trend that Nexora has adopted for Copilot and the AI Marketplace. This is a newer revenue model for the Company (first material usage-based revenue recognized in Q1 2025) and introduces estimation and systems risk not present in the Company's historical, predominantly ratable subscription revenue base (Section 9.2).

4. **Margin pressure from AI infrastructure costs.** Because Nexora both licenses third-party foundation models (variable, usage-linked cost) and operates its own GPU-based infrastructure for fine-tuning and inference (fixed and depreciating cost), the Company's cost of revenue mix is shifting, and gross margin on the Platform & Subscription segment has declined from 82% in fiscal 2023 to a forecasted 76% in fiscal 2025. This is consistent with broader industry commentary regarding AI infrastructure margin compression and informs our analytical expectations for cost of revenue (Section 15.6) and our fraud risk consideration regarding potential misclassification of AI infrastructure costs between cost of revenue and R&D (which would affect gross margin, a closely watched analyst metric).

5. **Regulatory attention to AI.** The industry is subject to an evolving and fragmented regulatory landscape, including the EU AI Act (phased obligations beginning August 2025 for general-purpose AI model providers and continuing through 2026–2027 for high-risk AI systems), evolving U.S. state-level AI legislation (e.g., Colorado's AI Act and similar statutes under consideration in California, Texas, and other states), and continued attention from the Federal Trade Commission regarding AI-related consumer protection and competition matters. While Nexora's products are not currently classified as "high-risk" AI systems under the EU AI Act's current guidance, we will monitor developments given the Company's expanding use of AI in customer-facing decision-support contexts (e.g., a beta "AI-driven credit risk scoring" module offered to financial-services customers), which could affect classification, compliance costs, and associated contingency/disclosure considerations.

6. **Talent competition and key-person dependency.** Enterprise software and AI companies compete intensely for machine learning research talent. Nexora disclosed in its Q2 2025 earnings call the departure of its Chief AI Officer, who joined a competitor, and management indicated this contributed to the design of the new AI-talent retention equity program discussed in Section 15.5. Elevated employee turnover in a company's technical leadership can be a relevant fraud risk factor under the "opportunities" component of the fraud triangle if it correlates with control gaps (e.g., production access rationalization), and we will consider this in our IT risk assessment (Section 11).

### 6.3 Regulatory Environment

Nexora is subject to (a) SEC reporting and disclosure requirements applicable to accelerated filers, including the cybersecurity disclosure rules effective for fiscal years ending on or after December 15, 2023; (b) data privacy regulations including the EU General Data Protection Regulation, the California Consumer Privacy Act as amended by the California Privacy Rights Act, and a growing number of state comprehensive privacy statutes; (c) export control regulations relevant to the Company's AI model technology, given Bureau of Industry and Security rules restricting export of certain advanced computing items and AI model weights to specified countries; and (d) sector-specific regulation applicable to certain Nexora customers (e.g., financial services customers subject to model risk management guidance such as SR 11-7, which indirectly affects Nexora's contractual obligations regarding AI model documentation and explainability). We considered the Company's compliance with laws and regulations having a direct and material effect on the financial statements (principally tax and, to a lesser extent, export control and data privacy) in accordance with AS 2405.

### 6.4 Industry Benchmarking

We obtained and will continue to update, through the audit, benchmarking data for a peer group of eight publicly traded companies with comparable business models (mid-cap, high-growth, AI-enabled enterprise SaaS with a cybersecurity or analytics focus). Key metrics benchmarked include revenue growth rate, gross margin, net revenue retention, days sales outstanding, deferred revenue growth relative to billings growth, and stock-based compensation as a percentage of revenue. Nexora's metrics are broadly consistent with peer medians, with two notable exceptions requiring further audit attention: (a) Nexora's days sales outstanding (61 days) is meaningfully higher than the peer median (46 days), consistent with the extended payment terms discussed in 6.2(1) and warranting expanded procedures over accounts receivable collectability and the allowance for credit losses (Section 15.7); and (b) Nexora's ratio of capitalized software costs to R&D expense (18%) is at the high end of the peer range (peer range 6%–19%), consistent with our identification of capitalized software as a significant estimate (Section 15.4).

### 6.5 Industry-Specific Financial Reporting Considerations

We considered industry practice and emerging positions taken by peer companies, as reported in public filings and by the AICPA Software Entities Revenue Recognition Task Force successor guidance, regarding: (a) accounting for AI compute costs embedded in subscription arrangements; (b) the principal-versus-agent evaluation for AI model marketplaces; and (c) capitalization of costs associated with fine-tuning third-party foundation models versus training proprietary models from scratch, an area we understand the FASB's Emerging Issues Task Force and the AICPA are monitoring but for which no industry consensus or authoritative guidance currently exists. Given this lack of specific guidance, we plan to consult with our National Office (see Section 4.4) and evaluate management's accounting policy for reasonableness, consistency of application, and adequacy of disclosure.

### 6.6 Regulatory and Litigation Matters Noted During Industry Research

During our industry and entity research we noted that Nexora received a routine SEC comment letter in June 2025 regarding the clarity of its non-GAAP "Adjusted EBITDA" reconciliation and its disclosure of AI-related risk factors; the Company responded in July 2025, and the matter was closed by the SEC Division of Corporation Finance without further comment in August 2025. We reviewed the correspondence and concluded it does not, in itself, indicate a heightened fraud risk, but we will read the final correspondence in full during fieldwork and evaluate whether any resulting changes to non-GAAP disclosure practices affect our understanding of management's incentives (Section 10).

### 6.7 Competitive Landscape Profile

To calibrate our understanding of the competitive pressures referenced throughout Section 6.2, we profiled Nexora's four principal competitors, each representing a different strategic archetype relevant to our risk assessment:

| Competitor (fictional) | Archetype | Relevance to Audit Risk Assessment |
|---|---|---|
| Vantorix Systems, Inc. | Large, diversified incumbent enterprise software vendor bundling analytics into a broader ERP/CRM suite | Pricing pressure; bundling-driven discounting dynamics referenced in Section 9.2 |
| Loomlight AI, Inc. | Venture-backed, AI-native analytics startup with no legacy product debt, pricing aggressively to win logos | Competitive displacement risk relevant to goodwill impairment growth assumptions (Section 15.3) and to the patent litigation matter (Section 15.8) |
| Cirrus Defense Cloud, Inc. | Cybersecurity-focused competitor to ShieldNex, larger scale, broader CNAPP feature set | Relevant to ShieldNex reporting unit fair value assumptions (Section 15.3) |
| Meridian Data Partners LLC | Private-equity-owned, mature BI vendor pursuing roll-up acquisition strategy in the legacy on-premises analytics space | Relevant to Legacy On-Premises reporting unit decline assumptions (Section 15.3) and the sunset/migration narrative |

We considered public disclosures, industry analyst commentary, and management's own competitive positioning materials (win/loss reports maintained by the sales operations team) in developing this profile. Notably, management's win/loss data indicates Nexora's win rate against Loomlight AI declined from 61% in the first half of fiscal 2025 to 48% in the third quarter, a trend management attributes to Loomlight's aggressive discounting rather than product capability gaps; we will independently corroborate this explanation, as an alternative (and less favorable) explanation — that Nexora's own product differentiation is eroding — would be directly relevant to the long-term growth assumptions underlying the goodwill impairment analysis in Section 15.3 and to the sustainability of the pricing/discounting assumptions embedded in the SSP corridor analysis in Section 9.2.

### 6.8 Barriers to Entry and Switching Costs

We considered the durability of Nexora's competitive position by evaluating barriers to entry and customer switching costs, both relevant to the long-term cash flow projections underlying goodwill impairment testing (Section 15.3) and business combination valuation (Section 15.2). Historically, Nexora's core BI/analytics platform has benefited from moderately high switching costs (data pipeline integration, user training, and workflow embedding within customer organizations), reflected in the Company's 91% gross revenue retention rate (Section 3.3). However, industry commentary and our own inquiry of the CTO indicate that the emergence of foundation-model-native "build vs. buy" alternatives (Section 3.3, Section 8.1) may be gradually eroding these switching costs, since a sophisticated enterprise customer with in-house AI engineering talent can increasingly construct a bespoke natural-language analytics layer directly atop a foundation-model API without a specialized vendor like Nexora. Management's long-range plan assumes this disintermediation risk remains limited to a narrow segment of the largest, most technically sophisticated customers; we will evaluate the reasonableness of this assumption against customer cohort retention data disaggregated by customer size and technical sophistication, to the extent such data is maintained by the Company.

---

## 7. ECONOMIC OUTLOOK AND MACRO-ENVIRONMENTAL FACTORS

AS 2110 requires us to obtain an understanding of relevant economic conditions affecting the entity. The following reflects our understanding, informed by publicly available macroeconomic data, Federal Reserve communications, and management's own disclosures regarding the operating environment, as of the planning date.

### 7.1 Interest Rate and Credit Environment

The Federal Reserve's federal funds target range stood at 3.75%–4.00% as of the most recent Federal Open Market Committee meeting prior to this memo's preparation, following a gradual easing cycle from the peak levels of 2023–2024. This is relevant to Nexora in several respects: (a) the fair value of the Company's $600 million convertible notes and the assessment of any embedded derivative or bifurcation considerations; (b) the discount rates used in the Company's goodwill and intangible asset impairment models (Section 15.3), where a moderating rate environment has partially offset multiple compression from softer growth assumptions; (c) the present value of operating lease liabilities; and (d) customers' cost of capital and IT budget decisions, which management has cited as a continued (though moderating) headwind to the pace of net-new enterprise software purchasing decisions and a contributing factor to lengthening sales cycles.

### 7.2 Inflation and Labor Cost Trends

Headline inflation has moderated toward the Federal Reserve's long-run target but wage growth in specialized technical labor markets — particularly for machine learning engineers and data scientists — has remained elevated, with industry compensation surveys indicating total compensation growth of 8–11% year-over-year for senior AI research roles in calendar 2025, materially above broader private-sector wage growth. This directly affects Nexora's cost structure (R&D headcount costs, representing approximately 34% of total operating expenses) and reinforces the strategic and financial-reporting significance of the AI-talent retention stock compensation program discussed in Section 15.5. We will evaluate whether the Company's compensation expense forecasts and related accruals appropriately reflect this cost environment.

### 7.3 Foreign Currency Exposure

Approximately 31% of Nexora's revenue is denominated in currencies other than the U.S. dollar, principally the Euro, British Pound, and Japanese Yen, arising from the EMEA and APAC sales operations. The U.S. dollar has experienced moderate depreciation against the Euro (approximately 4%) and appreciation against the Yen (approximately 3%) during the trailing twelve months, creating a net favorable-to-modestly-mixed translation effect on reported revenue that management has quantified in its non-GAAP "constant currency" revenue growth disclosures. We will test the mechanical accuracy and consistency of these constant-currency reconciliations as part of our procedures over non-GAAP measures furnished in earnings releases (which, while outside the scope of the financial statement audit opinion, are relevant to our consideration of the entity's control environment and the tone set by management regarding external reporting rigor).

Nexora does not currently use derivative instruments to hedge foreign currency exposure, a policy decision reaffirmed by the board's finance committee in Q2 2025 notwithstanding the growing foreign-currency-denominated revenue base; we will evaluate whether this remains an appropriate disclosure matter and whether the absence of hedging creates any accounting complexity (it does not create hedge accounting risk, given the absence of hedging instruments, but is relevant to our understanding of earnings volatility and the "quality of earnings" lens applied by the audit committee).

### 7.4 Capital Markets Conditions and Access to Financing

Nexora's convertible notes trade at a moderate premium to par, and the Company's revolving credit facility remains undrawn, indicating adequate liquidity and capital markets access. We considered whether current capital markets conditions raise any substantial doubt about the Company's ability to continue as a going concern under ASC 205-40 and AS 2415; based on the Company's liquidity position (cash and short-term investments of approximately $890 million as of September 30, 2025), positive operating cash flow (approximately $310 million trailing twelve months), and absence of near-term debt maturities (convertible notes mature 2029), we do not currently identify substantial doubt indicators, though we will reassess this conclusion at each interim period and at year-end, particularly in light of the acquisition activity discussed in Section 6.2(2) and any further debt-funded M&A.

### 7.5 Technology Sector-Specific Economic Indicators

We monitored the following sector-specific indicators as part of our understanding of the economic environment: (a) enterprise software IT spending growth forecasts from industry research organizations, indicating continued but moderating growth in overall enterprise software budgets (approximately 8–10% projected for calendar 2026, down from double-digit growth in 2021–2022), with AI-related line items representing a disproportionate and growing share of incremental budget allocation; (b) venture capital funding trends for AI-native startups, which remain robust and elevate competitive risk as discussed in Section 6.2; (c) cloud infrastructure pricing trends, where major hyperscale providers have both reduced list prices for certain compute instances and simultaneously introduced premium pricing tiers for AI-optimized GPU instances, creating offsetting effects on Nexora's cost of revenue; and (d) public technology company valuation multiples, which have compressed for profitability-lagging, high-growth SaaS companies relative to 2021 peak levels but remain elevated for companies demonstrating durable AI-driven revenue acceleration — directly relevant to our fraud risk consideration regarding management's incentive to characterize revenue growth as "AI-driven" (Section 10.3) and to our goodwill impairment analysis (Section 15.3).

### 7.5.1 Government and Public-Sector Spending Trends

Approximately 7% of Nexora's forecasted fiscal 2025 revenue derives from U.S. federal, state, and local government customers, principally through the ShieldNex cybersecurity product line, which is increasingly marketed toward public-sector cloud-security-compliance mandates (e.g., FedRAMP-adjacent state government requirements). We noted that federal procurement cycles have experienced periodic disruption in recent budget cycles due to continuing-resolution funding mechanisms and, at times, lapses in appropriations, which management has cited as a contributor to elongated sales cycles for this customer segment. We will evaluate whether government receivables exhibit distinct collection patterns warranting separate consideration within the allowance for credit losses analysis (Section 15.7) and whether any government contract-specific revenue recognition considerations (e.g., termination-for-convenience clauses common in U.S. government contracts) require distinct performance obligation or variable consideration analysis beyond the commercial-contract framework described in Section 9.

### 7.5.2 Commodity and Energy Cost Trends Affecting Cloud Infrastructure

Because Nexora's GPU-based AI infrastructure costs (Section 8.1(b)) are indirectly sensitive to the energy costs borne by its hyperscale cloud providers (which are, in turn, partially passed through in compute pricing over time), we monitored broader trends in industrial electricity pricing and semiconductor (GPU) supply availability. Reports of continued tightness in advanced GPU supply, driven by industry-wide demand for AI training and inference capacity, support management's expectation that GPU-linked infrastructure costs will not meaningfully decline in the near term, an assumption embedded in the cost of revenue forecasts underlying both the goodwill impairment model (Section 15.3) and the gross margin trends discussed in Section 6.2(4). We will evaluate this assumption against the most recent actual vendor pricing data available as of our substantive testing dates.

### 7.6 Implications for the Audit

We concluded that the current economic environment, while broadly stable, presents the following implications for our audit approach: (a) heightened importance of scrutinizing the reasonableness of long-term growth and margin assumptions used in discounted cash flow models supporting goodwill impairment and business combination valuations, given continued uncertainty regarding the durability of AI-driven demand and the pace of any further IT spending moderation; (b) continued monitoring of customer credit quality and days sales outstanding trends given extended payment terms noted in Section 6.2; (c) evaluation of foreign currency translation and constant-currency disclosure mechanics; and (d) no identified going-concern indicators at this time, subject to reassessment.

---

## 8. ARTIFICIAL INTELLIGENCE TRENDS AND THEIR EFFECT ON THE AUDIT

Given that AI-related products now represent management's stated primary growth driver (Copilot ARR grew from approximately $38 million at the start of fiscal 2025 to a forecasted $310 million by year-end, representing approximately 13% of total ARR), we devoted a dedicated planning work stream to understanding AI trends and their financial reporting implications. This section documents that understanding.

### 8.1 Technology Landscape

Nexora's AI strategy rests on three technical pillars, each with distinct risk implications:

**(a) Third-party foundation model licensing.** Nexora licenses API access to a leading third-party large language model provider under a multi-year, minimum-commitment contract (approximately $85 million minimum annual commitment, true-up based on token consumption). This creates (i) a significant vendor concentration and business continuity risk if the provider's pricing, availability, or terms change adversely; (ii) a cost of revenue estimation matter, given that actual token consumption must be accrued and reconciled to vendor invoices with a billing lag; and (iii) a contractual risk-allocation question regarding intellectual property indemnification and data usage rights that Nexora's legal department monitors and that we will consider in our contingency assessment (Section 15.8).

**(b) Proprietary fine-tuning and retrieval-augmented generation ("RAG").** Nexora fine-tunes smaller, task-specific models and builds RAG pipelines that ground foundation-model outputs in customer-specific data, aiming to differentiate Copilot from generic chatbot interfaces and to address enterprise concerns about hallucination and data governance. The costs of this engineering effort (data scientist compensation, GPU infrastructure) are partially capitalized as internal-use software (Section 15.4) and partially expensed as R&D, with the capitalization boundary requiring significant judgment given the iterative, sometimes non-linear nature of AI model development relative to traditional software development lifecycles.

**(c) Proprietary and third-party models within the AI Marketplace.** As described in Section 3.2(b), Nexora offers both self-developed models (e.g., a proprietary demand-forecasting model) and third-party models from independent software vendors, with revenue recognized on a principal or agent basis depending on facts and circumstances (Section 9.5).

### 8.2 AI-Specific Financial Reporting and Estimation Considerations

We identified the following AI-driven financial reporting matters as most significant to the fiscal 2025 audit:

1. **Capitalization of AI development costs** (Section 15.4) — determining the point of "technological feasibility" for AI models, which do not follow the discrete "working model" milestones common in traditional software, given that model performance improves incrementally and continuously through iterative training, and given that some capabilities (emergent behaviors of large models) are not fully specified or predictable in advance, complicating the ASC 985-20 / ASC 350-40 feasibility and probable-future-benefit analyses.

2. **Useful life estimates for capitalized AI assets** — foundation-model dependency and the rapid pace of model obsolescence (a new, materially more capable foundation model generation has been released by leading providers roughly every 12–18 months industry-wide) raise the question of whether historical useful-life assumptions (typically three years for internal-use software at Nexora) remain appropriate for AI-specific capitalized assets, an area where we will challenge management's assumptions and consider whether shorter useful lives or impairment indicators are warranted.

3. **Variable consideration and usage-based revenue estimation** (Section 9.2) — Nexora must estimate customers' expected AI Credit consumption for financial reporting purposes in certain contract structures (e.g., minimum-commitment-with-overage arrangements), a new source of estimation uncertainty.

4. **Vendor cost accrual risk** — the reconciliation lag between actual foundation-model token consumption and vendor invoicing (Section 8.1(a)) creates a risk of understated or overstated cost of revenue accruals, which we will test through vendor confirmation and recalculation procedures.

5. **Disclosure of AI-related risk factors and use of AI terminology in non-GAAP or KPI disclosures.** We noted that the Company's marketing and investor relations materials, and to some extent its earnings release commentary, use the term "AI-driven" broadly to describe revenue growth. We will evaluate, as part of our understanding of the control environment (Section 13) and fraud risk (Section 10), whether internal decomposition of revenue growth between "AI-attributable" and "core platform" growth is supportable and consistently applied, given known industry tendencies (sometimes referred to in the press as "AI-washing") to overstate the AI attribution of revenue growth for investor relations purposes. While this labeling issue is not itself a GAAP matter, it is relevant to our assessment of management's tone and the reliability of representations made regarding the drivers of revenue recognized under ASC 606.

6. **Internal use of AI in the Company's own financial reporting processes.** Nexora's finance organization has begun piloting an internal AI tool (built on the Company's own Copilot technology, "eating their own cooking") to assist with account reconciliation anomaly detection and journal entry drafting in the general ledger close process. While full production deployment for financial-close purposes is not planned until fiscal 2026, a limited pilot was used in Q3 2025 for a subset of intercompany reconciliations. We will (a) understand the design of this tool and any automated controls embedded within it, (b) evaluate segregation of duties and review controls over AI-drafted journal entries (all AI-suggested entries currently require manager review and approval before posting, per management's description), and (c) consider whether this pilot use constitutes a new IT application requiring inclusion in our ITGC scoping (Section 11.4).

7. **Use of AI tools by the audit team.** Consistent with Firm policy and PCAOB guidance on the use of technology-based tools in the audit, the engagement team may use Firm-approved AI-assisted analytics tools for document review and risk-flagging purposes during fieldwork. Any such use will be subject to the Firm's professional skepticism, supervision, and review protocols, and will not substitute for the engagement team's own judgment regarding sufficiency and appropriateness of audit evidence.

### 8.3 Benchmarking Against Industry AI Adoption Trends

Industry surveys indicate that median enterprise software companies in Nexora's peer group derive between 8% and 22% of incremental annual revenue growth from generative-AI-enabled features, with wide variance driven by differences in go-to-market maturity. Nexora's disclosed Copilot contribution to incremental growth (management estimates approximately 61% of fiscal 2025 net-new ARR is attributable to Copilot, either as new-logo driver or expansion driver) is at the higher end of this range, which we will corroborate through disaggregated revenue analysis (Section 9.7) rather than accepting management's attribution methodology at face value.

### 8.3.1 Model Risk and Output Reliability Considerations

Beyond the financial-reporting-specific considerations in Section 8.2, we considered "model risk" — the risk that Copilot's AI-generated outputs (natural-language answers to customer queries against enterprise data) are inaccurate, biased, or misleading — as a business and reputational risk with potential financial statement consequences. Nexora's terms of service include disclaimers limiting liability for AI-generated output accuracy, and the Company maintains a "human-in-the-loop" design principle for high-stakes use cases (e.g., the financial-services credit-risk-scoring beta module referenced in Section 6.3), requiring a qualified human reviewer to approve any customer-facing decision informed by the AI output. We inquired of the General Counsel regarding any customer complaints, contractual disputes, or claims arising from Copilot output reliability during fiscal 2025 and were informed of two customer complaints, both resolved through standard customer-support escalation without financial settlement or litigation. We will continue to monitor this area, as a material model-reliability failure could give rise to a loss contingency (Section 15.8) or reputational damage relevant to goodwill impairment assumptions (Section 15.3).

### 8.3.2 AI Governance Committee

Nexora established a cross-functional "Responsible AI Governance Committee" in January 2025, comprising representatives from Legal, Engineering, Product, Security, and Finance, chaired by the Chief Legal Officer, tasked with reviewing new AI feature launches against a documented responsible-AI framework (covering bias testing, data privacy compliance, explainability requirements for regulated-industry customers, and export control screening, Section 6.3). We reviewed the committee's charter and a sample of meeting minutes and consider its establishment a positive governance development; we will evaluate whether its review process appropriately covers financial-reporting-adjacent AI use cases, including the internal AI-assisted journal entry pilot tool (Section 8.2(6)), which we noted was in fact reviewed and approved by the committee in Q3 2025 prior to pilot deployment — a positive indicator regarding the pilot's governance rigor.

### 8.4 Conclusion

AI trends are pervasive to this audit — they affect the revenue model (Section 9), the cost structure and margin profile (Sections 6.2(4), 15.6), capitalized asset judgments (Section 15.4), stock compensation design (Section 15.5), IT and cybersecurity risk (Sections 11–12), and the overall tone of external communications relevant to fraud risk (Section 10). We have accordingly integrated AI-specific considerations throughout the risk assessment rather than treating AI as a standalone or segregable risk area.

---

## 9. REVENUE RECOGNITION RISKS

Consistent with the presumption in AS 2401.44 that improper revenue recognition is a fraud risk, and given the complexity introduced by Nexora's multiple revenue streams, we have identified revenue recognition as a **significant risk and a fraud risk** requiring specially designed audit procedures, heightened professional skepticism, and increased persuasiveness of audit evidence.

### 9.1 Overview of Revenue Streams and Contract Types

Nexora recognizes revenue under ASC 606 through the following principal streams:

| Revenue Stream | Recognition Pattern | % of FY2025E Revenue | Key Judgments |
|---|---|---|---|
| Subscription (NexoraIQ core platform) | Ratable, over contract term | 58% | SSP, contract term, renewal options |
| Copilot fixed subscription uplift | Ratable, over contract term | 9% | Bundling with core platform, SSP |
| Copilot / Marketplace usage-based (AI Credits) | Point-in-time, as consumed | 16% | Variable consideration estimation, principal vs. agent |
| Professional services (fixed-fee) | Over time, % completion (input method) | 6% | Measure of progress, loss contract assessment |
| Professional services (time & materials) | Over time, as services rendered | 4% | Cut-off |
| ShieldNex CSPM subscription | Ratable, over contract term | 7% | Deferred revenue fair value haircut, integration of billing systems |

### 9.2 Significant Risk: Standalone Selling Price and Multiple Performance Obligation Allocation

Nexora's typical enterprise contract bundles core platform subscription, Copilot uplift, a minimum AI Credit commitment, and implementation services into a single arrangement with a blended contract value, often subject to significant discounting (Section 6.2(1)). Management uses a residual approach for certain performance obligations lacking observable standalone sales (an allowable method under ASC 606-10-32-34 only when specific criteria are met, including highly variable or uncertain pricing) and an adjusted market assessment approach for others, informed by a periodically updated SSP corridor analysis maintained by the revenue accounting team.

We identified the following specific risks: (a) inconsistent or stale SSP corridors that no longer reflect actual observable transactions, particularly for the newer Copilot and AI Marketplace offerings, which have limited transaction history (first full year of at-scale sales); (b) sales personnel incentives (accelerators once quota is achieved, often concentrated near quarter-end) that create pressure to structure deals with non-standard terms, side letters, or verbal modifications that may not be fully captured in the Salesforce CPQ (configure-price-quote) system of record, resulting in a risk that recognized revenue does not reflect the true substance of the arrangement; and (c) the risk that discounts are disproportionately allocated to already-delivered performance obligations (e.g., implementation services or first-year subscription) to accelerate revenue recognition, rather than allocated proportionately as required.

**Planned response:** Detailed test of controls over the SSP governance process (quarterly SSP corridor recalculation and approval by the VP of Revenue Accounting); a sample of contracts, weighted toward quarter-end and disproportionately large or unusual transactions, tested for appropriate identification of performance obligations, SSP allocation, and agreement with underlying legal contract terms (not merely the CPQ-generated order form); confirmation of a sample of significant new and renewal contract terms directly with customers, including specific confirmation of the absence of side letters; and analysis of all contracts with negotiated non-standard terms flagged in the legal contract repository, cross-referenced to the revenue system.

### 9.3 Significant Risk: Variable Consideration for Usage-Based AI Revenue

For minimum-commitment-with-overage contract structures, Nexora must estimate expected total AI Credit consumption to determine whether cumulative revenue recognized would be subject to a "significant reversal" constraint under ASC 606-10-32-11 through 32-13. Given limited historical usage data (the product has been generally available for less than twelve months), management's estimation approach relies heavily on a combination of limited historical trend data and customer-provided usage forecasts, which we consider inherently less reliable than a mature historical base. We will evaluate the reasonableness of management's estimation methodology, test the completeness and accuracy of the underlying usage data extracted from the Company's metering/telemetry system (an IT-dependent process, see Section 11.5), and perform a retrospective review comparing prior-period estimates to actual subsequent consumption to assess estimation bias (either consistently optimistic or conservative), which could itself indicate a systematic risk requiring further investigation.

### 9.4 Significant Risk: ShieldNex Acquisition Deferred Revenue and Revenue Trend Distortion

Under acquisition accounting (ASC 805), acquired deferred revenue is remeasured to fair value as of the acquisition date, typically representing the cost to fulfill remaining performance obligations plus a normal profit margin, rather than the historical carrying amount of deferred revenue on ShieldNex's pre-acquisition books. This routinely results in a "deferred revenue haircut," meaning post-acquisition revenue recognized from pre-existing ShieldNex contracts is lower than it would have been absent the acquisition, creating a mechanical, non-economic revenue growth headwind in the post-acquisition periods that must be properly disclosed and not obscured within consolidated organic growth metrics. We will test management's fair value determination for acquired deferred revenue (in conjunction with our review of the overall purchase price allocation, Section 15.2) and evaluate whether the Company's disclosed organic/inorganic revenue growth decomposition appropriately isolates this effect, given its relevance to the fraud risk discussed in Section 10.3 regarding growth-narrative pressure.

### 9.5 Significant Risk: Principal versus Agent Determination for AI Marketplace

For third-party models offered through the AI Marketplace, we will evaluate whether Nexora controls the specified good or service (the AI model output) before it is transferred to the customer, per the indicators in ASC 606-10-55-36 through 55-40, including whether Nexora is primarily responsible for fulfillment, bears inventory or performance risk, and has discretion in establishing pricing. Management currently presents approximately 60% of third-party Marketplace transactions on a gross (principal) basis and 40% on a net (agent) basis, based on a model-by-model contractual analysis. Given the financial statement impact of principal-versus-agent classification on both revenue and cost of revenue (though not on gross profit), and given this is a newer product area without an established audit history, we will independently reperform the indicator analysis for a sample of third-party model arrangements, including all arrangements individually exceeding $2 million in annual transaction volume, and will specifically consult National Office on any borderline conclusions (Section 4.4).

### 9.6 Other Revenue Risks

- **Channel and distributor sell-through arrangements** — Nexora sells a portion of Japanese and Brazilian revenue (approximately 6% of total revenue) through local distributors. We will evaluate whether distributor arrangements involve a right of return, price protection, or extended payment terms that would preclude revenue recognition upon sell-in, and will test a sample of sell-through data reported by distributors.
- **Customer concentration and credit risk** — notwithstanding management's assertion of low concentration (Section 3.3), we will independently test customer concentration calculations and will pay particular attention to any customers exhibiting both high revenue significance and elevated days-sales-outstanding, which can be an indicator of collectability concerns masked by continued revenue recognition.
- **Cut-off** — given known incentives to accelerate deal closing near quarter-end (Section 6.2(1)), we will perform detailed cut-off testing for a sample of transactions recorded in the five business days before and after each quarter-end, including inspection of contract execution dates, delivery/access-provisioning dates (for subscription commencement), and evidence of any post-period-end contract modifications (a "hold and release" or improper channel-stuffing risk indicator).
- **Contract modifications** — testing of a sample of mid-term contract modifications (upsells, downsells, and renegotiated terms) for appropriate accounting treatment (prospective versus cumulative catch-up) under ASC 606-10-25-10 through 25-13.
- **Refunds, credits, and contract terminations** — analytical review of the trend in customer credit memos and early-termination provisions, benchmarked against historical experience and industry norms, as an indicator of potential channel stuffing or premature revenue recognition in prior periods.

### 9.6.1 Assertion-Level Risk Mapping for Revenue

To ensure our procedures are properly linked to specific relevant assertions, as required by AS 2110.59–.65, we mapped each identified revenue risk to the relevant assertion(s):

| Risk | Existence/Occurrence | Completeness | Accuracy/Valuation | Cutoff | Rights & Obligations | Presentation & Disclosure |
|---|---|---|---|---|---|---|
| SSP allocation (9.2) | | | X | | | X |
| Variable consideration (9.3) | | X | X | | | X |
| ShieldNex deferred revenue (9.4) | | X | X | | | X |
| Principal vs. agent (9.5) | | | X | | X | X |
| Channel/distributor sell-through (9.6) | X | X | | X | X | |
| Cut-off near quarter-end (9.6) | X | X | | X | | |
| Contract modifications (9.6) | X | | X | X | | |
| Customer concentration/collectability (9.6) | | | X | | | X |

This mapping directly informs the design of our tests of details (e.g., completeness testing for variable consideration requires a different population and direction of testing — from source usage data forward to recognized revenue — than existence testing for channel sell-through, which requires tracing from recorded revenue back to supporting evidence).

### 9.7 Analytical Procedures Planned

We will perform disaggregated revenue analytics comparing recognized revenue by product line, geography, and customer cohort against (a) billings and cash collections, (b) deferred revenue rollforward, (c) headcount in customer-facing sales roles (as a leading indicator of bookings capacity), and (d) third-party data where available (e.g., customer web-traffic or usage proxies for select large customers, to the extent obtainable). We will specifically analyze the relationship between quarterly revenue recognized and quarterly deferred revenue balances to identify any unusual or unexplained divergence from the historical ratable pattern that might indicate premature recognition.

### 9.8 Conclusion on Revenue Risk

We conclude that revenue recognition, taken as a whole, represents both a **significant risk** (requiring specially tailored substantive procedures regardless of the assessed control risk, per AS 2110.68–.70) and the presumed **fraud risk** under AS 2401.44. Our audit response combines: (i) tests of the operating effectiveness of relevant automated and manual controls over contract review, SSP determination, and revenue system interfaces; (ii) extensive substantive tests of details over a risk-weighted sample of contracts, with oversampling near period-end and among non-standard/negotiated arrangements; (iii) rigorous analytical procedures; and (iv) unpredictable audit procedures (e.g., an unannounced count/observation of a sample of usage-metering source data extracts) designed specifically to address the presumed fraud risk, in accordance with AS 2401.55.

---

## 10. FRAUD RISK ASSESSMENT

This section documents the engagement team's fraud risk assessment performed in accordance with AS 2401, including the results of our fraud brainstorming session held on November 18, 2025 (attended by the engagement partner, EQR, manager, senior associates, IT audit specialist, and a forensic accounting specialist on a consultative basis), our inquiries of management, the audit committee, internal audit, and other personnel, and our evaluation of fraud risk factors organized by the three elements of the fraud triangle: incentives/pressures, opportunities, and attitudes/rationalizations.

### 10.1 Inquiries Performed

We made inquiries of the following individuals regarding their knowledge of actual, suspected, or alleged fraud: the CEO, CFO, General Counsel, Chief Audit Executive, Controller, VP of Revenue Accounting, VP of Human Resources, the audit committee chair (in executive session, without management present), and the ethics hotline administrator. No one reported knowledge of actual fraud affecting Nexora during fiscal 2025. The Chief Audit Executive reported that internal audit's whistleblower hotline received 14 reports during the trailing twelve months, of which 11 related to employee relations/HR matters (unrelated to financial reporting), 2 related to expense reimbursement policy violations by mid-level employees (investigated and remediated; amounts individually and in aggregate clearly trivial, approximately $6,400 total), and 1 anonymous report alleging that a regional sales director in EMEA had "pressured" a customer to sign a contract before quarter-end with an informal verbal understanding that certain terms would be revisited afterward. This last item is discussed further in Section 10.5 as a specific fraud risk response item.

### 10.2 Fraud Risk Factors — Incentives/Pressures

- Nexora's executive officers, including the CEO and CFO, receive a substantial portion of annual incentive compensation tied to revenue growth, non-GAAP operating margin, and (new for fiscal 2025) Copilot ARR attainment, creating a direct financial incentive to achieve specific, disclosed metrics.
- The Company has a public track record of meeting or exceeding analyst consensus revenue estimates in 15 of the last 16 quarters (Section 5.3), an unusually consistent pattern for a company of this size and growth profile that we consider, in itself, a fraud risk indicator warranting professional skepticism (consistent with observations frequently noted in academic and regulatory literature regarding "just barely beating estimates" patterns).
- Significant unvested equity awards for key executives, including the CEO, CFO, and CTO, with market-price-sensitive vesting/value characteristics, creating a personal financial stake in the Company's stock price performance, particularly around the fiscal year-end reporting date and subsequent equity offering activity (Form S-3 shelf, Section 2.2).
- Margin pressure from rising AI infrastructure costs (Section 6.2(4)) and elevated technical talent compensation costs (Section 7.2) create pressure on reported profitability metrics closely monitored by investors.
- The competitive narrative regarding AI-driven growth (Section 8.2(5)) creates pressure to attribute revenue growth to AI products specifically, which — while primarily an investor relations and non-GAAP disclosure matter — could create pressure to misclassify revenue between product lines in a manner inconsistent with underlying contract terms.
- Debt covenant compliance under the revolving credit facility (Section 5.3) creates an incentive to manage leverage and liquidity metrics, though covenant headroom is currently substantial (no covenant breach risk identified).

### 10.3 Fraud Risk Factors — Opportunities

- The complexity and judgment inherent in SSP determination, variable consideration estimation, and principal-versus-agent evaluation (Section 9) create opportunities for management to influence reported revenue through selection of assumptions within a range that may appear individually defensible.
- The ShieldNex acquisition integration is ongoing, with certain ShieldNex financial processes (billing, revenue recognition) not yet fully migrated onto Nexora's standard systems and controls as of the planning date, creating a temporary period of potentially weaker process standardization and oversight (Section 13.6, Section 14).
- Elevated employee turnover in technical and finance leadership roles (Section 6.2(6); we also noted the Corporate Controller departed in August 2025 and was replaced on an interim basis pending a permanent search) can create transitional control gaps and reduced institutional knowledge that could be exploited, whether intentionally or through error that goes undetected.
- The whistleblower report described in Section 10.1 regarding EMEA sales practices indicates at least the possibility of side-letter or informal arrangements not fully reflected in the system of record, which, if pervasive, could represent an opportunity for premature revenue recognition.
- Journal entries can be posted by a relatively broad population of finance personnel (approximately 46 users with journal entry posting access in the NetSuite ERP as of our preliminary ITGC scoping), and our preliminary walkthrough (Section 14.4) noted that segregation-of-duties conflict reports are reviewed quarterly rather than continuously, creating a window of opportunity for inappropriate entries to go temporarily undetected.
- The pilot use of AI tools in the financial close process (Section 8.2(6)) is new and its control environment, while designed with a "human in the loop" review requirement, has limited operating history and has not yet been subject to a full audit cycle of scrutiny.

### 10.4 Fraud Risk Factors — Attitudes/Rationalizations

- We did not identify a generally poor "tone at the top"; our observations of the CEO, CFO, and audit committee interactions indicated an appropriate emphasis on ethical conduct and support for the internal audit and compliance functions. However, we noted that the CFO, in an earnings call, characterized a competitor's accounting practices for AI revenue recognition as "aggressive" while describing Nexora's own practices as conservative — a comparison we will independently evaluate rather than accept as a self-assessment, consistent with professional skepticism.
- Sales compensation plan documents reviewed during walkthroughs include language permitting "management discretion" to credit sales representatives for deals that slip past quarter-end if the deal was "substantially negotiated" prior to period-end — a policy that, while intended for compensation purposes only, creates a cultural signal that quarter-end deal timing is flexible and could rationalize inappropriate cut-off practices if not clearly firewalled from the actual revenue recognition determination (which must be based on when control transfers, not sales compensation policy).
- No history of prior-period financial restatements was identified; the Company's fiscal 2024 financial statements were not restated, and the two significant deficiencies identified in fiscal 2024 (Section 13.6) did not result in a material misstatement.

### 10.5 Specific Fraud Risks Identified and Planned Responses

| # | Fraud Risk | Risk Level | Planned Response |
|---|---|---|---|
| FR-1 | Improper revenue recognition through manipulation of SSP, variable consideration estimates, or cut-off (presumed fraud risk) | Significant / Elevated | See Section 9.8; expanded substantive testing, unpredictable procedures, confirmation of contract terms |
| FR-2 | Management override of controls (presumed fraud risk, all engagements) | Significant / Elevated | Extended journal entry testing (100% population data analytics using IT-audit-assisted extraction, with risk-based filtering for entries posted by senior finance personnel, entries posted on weekends/holidays, entries lacking narrative description, and entries affecting revenue or reserve accounts near period-end); retrospective review of significant prior-year estimates for management bias; heightened scrutiny of significant unusual transactions, including the EMEA whistleblower matter |
| FR-3 | Manipulation of non-GAAP metrics / KPI disclosures to support growth narrative (indirect financial statement relevance) | Moderate | Recalculation of non-GAAP reconciliations; corroboration of Copilot ARR attribution methodology against underlying contract and billing data; comparison of disclosed KPIs (net revenue retention, ARR) to source data |
| FR-4 | Side letters or undisclosed contract modifications, particularly in EMEA sales region following whistleblower report | Elevated (specific) | Direct confirmation of complete contract terms with a sample of EMEA customers (including customers not otherwise selected for standard confirmation procedures); interview of the EMEA regional sales director and relevant sales operations personnel; inspection of the sales director's and relevant sales representatives' email correspondence for a risk-based keyword search (subject to appropriate legal/HR coordination and any works council or data privacy constraints applicable in the EU) |
| FR-5 | Improper capitalization of costs that should be expensed (software development, AI training costs) to inflate earnings/EBITDA | Moderate-Elevated | Detailed testing of capitalized cost populations against capitalization policy criteria; inquiry of engineering personnel (not just finance) regarding the nature of capitalized projects; trend analysis of capitalization rate over time |
| FR-6 | Manipulation of purchase accounting (ShieldNex) to shift value between goodwill (not amortized) and other categories, or to establish "cookie jar" reserves | Moderate | Independent challenge of valuation specialist's work; review of acquisition reserves established and their subsequent utilization/release, including any change to the reserve during the measurement period |
| FR-7 | Related-party transactions not properly identified or disclosed | Low-Moderate | Inquiry, review of D&O questionnaires, review of board and committee minutes, review of new-vendor onboarding data for matches to related-party registry |

### 10.6 Consideration of Management Override of Controls

Consistent with the mandatory presumption in AS 2401.65, we will perform, at a minimum, the following procedures irrespective of our other risk assessments: (a) testing of journal entries and other adjustments for evidence of possible material misstatement due to fraud, using data analytics tools to examine the entire population of journal entries rather than a sample, with risk-based criteria as described in FR-2 above; (b) review of accounting estimates for biases that could result in material misstatement due to fraud, including a retrospective review of significant estimates and judgments reflected in the fiscal 2024 financial statements (Section 15); and (c) evaluation of the business rationale (or lack thereof) for significant unusual transactions, specifically including the timing, structure, and rationale for the ShieldNex acquisition, the stock-based component of acquisition consideration, and any transactions with related parties.

### 10.6.1 Fraud Triangle Summary Diagram

The following summarizes how the fraud risk factors identified in Sections 10.2 through 10.4 map onto the classic fraud triangle framework, which we use to structure our brainstorming and ensure balanced consideration of all three elements rather than over-indexing on any single dimension:

| Element | Key Indicators Identified | Overall Assessment |
|---|---|---|
| Incentives/Pressures | Revenue/margin-linked executive compensation; consistent consensus-beating track record; equity value sensitivity ahead of shelf offering; margin pressure from AI costs; AI growth narrative pressure; covenant considerations (limited) | Moderate-to-Elevated |
| Opportunities | Judgmental revenue estimates; ShieldNex integration transition state; leadership turnover (Controller, Chief AI Officer); broad journal entry access population; EMEA whistleblower report; new/unproven AI pilot tool controls | Elevated |
| Attitudes/Rationalizations | Generally positive tone at the top; one notable CFO public comparative statement warranting corroboration; sales compensation policy language creating a soft cultural signal around quarter-end timing; no restatement history | Low-to-Moderate |

Considered together, we assess the overall fraud risk environment as **moderate-to-elevated**, driven primarily by the "opportunities" dimension (transitional/integration-related control gaps) combined with real but not extreme incentive pressures, and only modest attitude/rationalization indicators. This overall assessment supports our conclusion that revenue recognition and management override warrant the specific, elevated responses described in Sections 9.8 and 10.6, while we do not believe the overall environment is indicative of pervasive, entity-wide fraud risk requiring, for example, withdrawal consideration or a going-concern-adjacent skepticism posture.

### 10.7 Communication of Fraud Risk Assessment

This fraud risk assessment, including the specific risks identified in Section 10.5, will be communicated to the audit committee as part of our audit planning communications required under AS 1301, and any changes to our fraud risk assessment identified during fieldwork will be promptly communicated to the engagement partner and, as appropriate, escalated to the EQR and audit committee.

---

## 11. INFORMATION TECHNOLOGY RISKS

Nexora's financial reporting is heavily dependent on IT systems, and the Company's core products are themselves technology offerings, resulting in a dual layer of IT risk: (a) IT general controls and application controls supporting the reliability of financial reporting, and (b) product/platform technology risk that, while not itself part of ICFR, informs our understanding of the business and certain disclosure and estimation matters (e.g., cybersecurity incident disclosure, Section 12).

### 11.1 IT Environment Overview

Nexora's financial-reporting-relevant IT environment includes:

- **Enterprise Resource Planning:** NetSuite (cloud-hosted, SaaS), used for general ledger, accounts payable, fixed assets, and consolidation (via a bolt-on consolidation tool, OneStream, implemented in Q1 2024).
- **Revenue and Billing:** Salesforce (CRM) integrated with a Salesforce-native CPQ and billing module (Salesforce Revenue Cloud), which generates contract and invoicing data that interfaces to NetSuite via a middleware integration platform (MuleSoft).
- **Usage Metering/Telemetry:** A proprietary, internally developed metering pipeline (built on AWS, using Kafka streaming and a Snowflake data warehouse) that captures AI Credit consumption events and feeds both customer-facing usage dashboards and the revenue recognition variable consideration calculation (Section 9.3) — a critical IT-dependent process given its direct role in revenue measurement.
- **Payroll and Stock Administration:** ADP Workforce Now (payroll) and Shareworks by Morgan Stanley (equity administration), both third-party hosted.
- **ShieldNex Legacy Systems:** ShieldNex's pre-acquisition billing and subscription management system (Chargebee) and its separate instance of NetSuite remain operational as of the planning date, pending a planned migration to Nexora's standard systems targeted for completion in Q2 2026 — creating a temporary dual-system environment for the ShieldNex component (Section 14.6).
- **Cloud Infrastructure:** Hybrid multi-cloud, primarily AWS (approximately 70% of compute workloads) and Microsoft Azure (approximately 30%, largely inherited from ShieldNex and not yet consolidated).

### 11.2 IT Risk Assessment Summary

| IT Risk Area | Description | Financial Reporting Relevance | Risk Level |
|---|---|---|---|
| Access management / user provisioning and deprovisioning | Risk that inappropriate or excessive access to financially significant applications is granted or not timely revoked, particularly following the ShieldNex acquisition and elevated technical staff turnover | Unauthorized transaction initiation, segregation of duties conflicts | Elevated |
| Change management over the metering/telemetry pipeline | Risk that changes to the Kafka/Snowflake usage-metering pipeline are not adequately tested, approved, or documented, potentially resulting in inaccurate usage data flowing into revenue recognition calculations | Revenue misstatement (Section 9.3) | Elevated |
| System interfaces (Salesforce → MuleSoft → NetSuite) | Risk of incomplete or inaccurate data transfer between systems, particularly for complex bundled contracts | Revenue and deferred revenue misstatement | Elevated |
| Dual-system environment (ShieldNex legacy systems) | Risk of inconsistent control design/operation, manual workaround reliance, and consolidation errors during the transition period | Completeness/accuracy of ShieldNex-related balances | Elevated |
| Program change management (NetSuite, OneStream) | Risk that configuration changes to the ERP or consolidation tool are not appropriately tested and approved | Pervasive — affects multiple financial statement line items | Moderate |
| IT operations (batch processing, job scheduling) | Risk of incomplete or failed data processing (e.g., failed nightly revenue recognition batch jobs) not being detected timely | Completeness of financial data | Moderate |
| Cloud infrastructure management / vendor dependency | Risk of service disruption or misconfiguration at AWS/Azure affecting system availability | Business continuity; indirect financial reporting relevance | Moderate |
| Data governance over AI training data | Risk that customer data used in AI model training/fine-tuning does not comply with contractual and privacy restrictions | Contingency/legal risk (Section 15.8), not direct financial misstatement | Moderate |
| Third-party/foundation-model vendor dependency | Concentration risk and cost-accrual accuracy (Section 8.1(a)) | Cost of revenue accuracy; business continuity | Moderate |

### 11.3 Access Management

We noted in our preliminary walkthrough that user access provisioning for the Salesforce, NetSuite, and AWS production environments follows a documented request-and-approval workflow (via the Company's IT service management tool, Jira Service Management), but that the ShieldNex environment, as of the acquisition date, used a separate, less mature access request process (email-based approvals, no centralized ticketing) that had not yet been fully integrated into Nexora's standard process as of September 30, 2025. We identified this as a specific deficiency candidate (Section 13.6) and will perform expanded testing of ShieldNex user access provisioning, termination, and periodic access review controls for the post-acquisition period.

We also noted that quarterly user access reviews ("UARs") for NetSuite and Salesforce are performed by application owners, but our preliminary inquiry indicated that the Q3 2025 UAR for NetSuite was completed 11 business days after its target due date because of the interim Controller transition (Section 10.3), and evidence of remediation for identified inappropriate access (2 instances noted by management's own Q3 UAR) was not finalized until after the UAR review was substantively complete. We will test the timeliness and evidence of remediation for all UARs performed during fiscal 2025.

### 11.4 Change Management

We will test change management controls over: (a) the metering/telemetry pipeline (given its direct revenue relevance, Section 9.3), including code review, testing (including a sample of test evidence for changes affecting usage-calculation logic), and approval prior to production deployment; (b) NetSuite configuration changes, including any changes to revenue recognition rule configurations, chart of accounts, or automated workflow rules; (c) the Salesforce CPQ/billing configuration, particularly changes to product catalog, pricing rules, and approval workflow thresholds; and (d) the new AI-assisted journal entry pilot tool (Section 8.2(6)), including the controls governing any updates to its underlying logic or training data.

We noted that Nexora's engineering organization has adopted a continuous integration/continuous deployment ("CI/CD") model with multiple production deployments per day for its core product codebase. While this deployment cadence applies primarily to the customer-facing product (not the financial-reporting systems, which follow a more traditional change management cadence with scheduled release windows), the metering/telemetry pipeline sits at the intersection of "product" and "financial reporting" infrastructure, is subject to the faster-paced product deployment cadence, and therefore requires us to specifically evaluate whether the standard, less-frequent change management control procedures are actually operating as designed given the much higher change frequency in practice — a risk of control design/operating mismatch that we will specifically test.

### 11.5 Data Reliability of System-Generated Reports and IT-Dependent Data

Given our extensive reliance on system-generated data (e.g., the deferred revenue rollforward, the usage-metering variable consideration calculation, the accounts receivable aging), we will test the accuracy and completeness of key reports and data extracts used as audit evidence, in accordance with AS 1105.10, through a combination of (a) testing relevant general and application controls over the system(s) that produce the report, (b) testing the completeness and accuracy of the information itself (e.g., recalculating report totals, tracing to source documents, testing report logic/query criteria), or (c) a combination of both, as appropriate to the significance of the data.

### 11.5.1 Business Continuity and Disaster Recovery

We evaluated Nexora's business continuity and disaster recovery ("BC/DR") posture as a component of our understanding of IT risk, given its relevance to the going-concern assessment (Section 7.4) and to the completeness/availability of financial data. Nexora's AWS-hosted production environment employs a documented multi-availability-zone architecture with automated failover, and the Company conducts a semi-annual disaster recovery test (most recent test conducted in August 2025, achieving a recovery time objective of 3.5 hours against a stated target of 4 hours, and a recovery point objective of under 15 minutes). ShieldNex's Azure-hosted environment, by contrast, relies on a single-region deployment with a manual (non-automated) failover runbook that has not yet been tested since the acquisition; management has represented that a formal DR test for the ShieldNex environment is scheduled for Q1 2026. We consider the absence of a tested DR capability for the ShieldNex environment a business continuity risk that, while not itself a financial-statement misstatement risk, is relevant to our overall risk assessment regarding the pace and rigor of the ShieldNex integration (a theme recurring throughout Sections 11, 13, and 14) and will be discussed with the audit committee as an observation, separate from our formal control deficiency reporting.

### 11.5.2 Data Center and Cloud Configuration Management

We reviewed Nexora's cloud configuration management practices, including its use of infrastructure-as-code (Terraform) to provision and manage AWS resources, which provides a version-controlled, auditable history of infrastructure changes — a positive control design feature. We noted the ShieldNex Azure environment does not yet use infrastructure-as-code tooling and instead relies on manual console-based configuration changes by a small team of ShieldNex-origin engineers, consistent with the broader pattern of less mature, less standardized controls in the acquired environment pending full integration (Section 11.3, Section 14.6). We will specifically test whether any manual Azure configuration changes made during the post-acquisition period followed an appropriate change approval process, notwithstanding the absence of automated tooling.

### 11.6 ITGC Deficiencies Carried Forward

Two significant deficiencies were identified in the fiscal 2024 audit related to (a) inadequate segregation of duties for a subset of NetSuite "system administrator" role assignments (11 users identified with excessive access combining transaction initiation and approval capabilities) and (b) insufficiently documented evidence of code review for a sample of emergency ("hotfix") changes to the revenue recognition rules engine. Management represented that both deficiencies were remediated during Q2 2025 (role redesign completed and evidenced; emergency change documentation procedures updated and evidenced through a sample of Q2–Q3 2025 hotfixes). We will independently test the operating effectiveness of the remediated controls for a sufficient period (at least six months of operation) before concluding on remediation.

---

## 12. CYBERSECURITY RISK ASSESSMENT

Cybersecurity risk is relevant to this audit both as an ITGC/business-continuity matter affecting the reliability of financial reporting systems (overlapping with Section 11) and, separately, as a specific area of SEC disclosure subject to our procedures under AS 2705 (auditor's responsibilities with respect to other information) and our broader responsibilities regarding disclosure controls to the extent they intersect with financial statement matters.

### 12.1 Regulatory Framework

Nexora is subject to the SEC's cybersecurity disclosure rules (Release No. 33-11216), requiring: (a) disclosure under Item 1.05 of Form 8-K of material cybersecurity incidents within four business days of a materiality determination (subject to a limited national-security delay exception); and (b) annual disclosure under Item 106 of Regulation S-K describing the Company's processes for assessing, identifying, and managing material cybersecurity risks, management's role in that process, and the board's oversight of cybersecurity risk. We will review the Company's draft Item 106 disclosure for the fiscal 2025 Form 10-K for consistency with our understanding of the Company's actual practices developed through this audit, though we note that Item 106 disclosures are not part of the audited financial statements and are subject to a different (lower) level of auditor involvement than the financial statements themselves — principally a "other information" read-for-consistency procedure rather than substantive testing, absent indicators suggesting the disclosure is materially inconsistent with our audit knowledge.

### 12.2 Governance and Oversight

Nexora's board has delegated primary oversight of cybersecurity risk to the audit committee, which receives quarterly briefings from the Chief Information Security Officer ("CISO"), M. Torres, who was hired in March 2024 (following a predecessor's departure) and reports administratively to the CTO and has a direct reporting line to the audit committee for cybersecurity matters. We reviewed the CISO's quarterly board presentations for the trailing four quarters and noted appropriate coverage of threat landscape updates, key risk indicators (mean time to detect, mean time to remediate critical vulnerabilities, phishing simulation click rates, and third-party risk assessment status), and incident summaries, including the April 2025 incident discussed in Section 12.4.

### 12.3 Security Program and Control Framework

Nexora's information security program is aligned to the NIST Cybersecurity Framework 2.0 and maintains SOC 2 Type II certification for its core NexoraIQ platform (report period covering the trailing twelve months, issued by an unrelated accounting firm, "Whitmore & Associates LLP," which we will evaluate under AS 2601 to the extent we plan to use it as audit evidence regarding relevant IT controls, principally logical access and change management controls over the AWS-hosted production environment). ShieldNex's Azure-hosted environment does not yet have an independent SOC 2 report covering the post-acquisition period; a Type I report is targeted for Q1 2026, and no Type II report will be available before our audit opinion date, which is a gap we will address through direct testing rather than reliance on a third-party report (Section 11.3).

### 12.4 The April 2025 Security Incident

In April 2025, a third-party SaaS vendor used by Nexora's marketing department (a customer webinar/event-registration platform, unrelated to the Company's production systems, financial systems, or customer data processing environments) experienced a data breach that exposed a database containing names, business email addresses, and job titles of individuals who had registered for Nexora-hosted webinars (approximately 41,000 records; no financial account information, passwords, or sensitive personal information was involved). Nexora's incident response team, upon notification by the vendor, engaged outside counsel and a third-party forensic firm, notified affected individuals in accordance with applicable state breach-notification laws, and determined, based on the nature of the exposed data and the limited scope of affected individuals, that the incident was **not material** and therefore did not require an Item 1.05 Form 8-K filing. The Company disclosed the incident briefly in its Item 106 discussion as an example of the incident response process in action.

We independently evaluated management's materiality determination, considering both quantitative factors (estimated direct costs of approximately $180,000 for forensic investigation, notification, and credit monitoring services — well below any materiality threshold, Section 5.2) and qualitative factors (no customer production data or financial data involved, no evidence of reputational impact reflected in customer retention metrics, no litigation threatened as of the planning date, no regulatory inquiry received). We concur that the incident, based on facts known as of the planning date, does not appear to rise to the level of a material misstatement risk for the financial statements, but we will continue to monitor for developments (e.g., litigation, regulatory action, or a broader scope of compromise identified through ongoing forensic work) through the completion of fieldwork and will reassess as a subsequent event if warranted.

### 12.5 Third-Party and Supply Chain Risk

Given the Company's dependency on third-party cloud infrastructure (AWS, Azure) and the foundation-model provider (Section 8.1(a)), we evaluated Nexora's third-party risk management program, which includes a vendor security assessment questionnaire, contractual security and data-processing requirements, and, for critical vendors, review of the vendor's own SOC 2 report. We noted that the foundation-model provider's SOC 2 report was last reviewed by Nexora's vendor risk team in January 2025 (within the trailing twelve months, consistent with policy), but that a similar review for a newly onboarded sub-processor used within the ShieldNex product (a specialized vulnerability-scanning data provider) had not yet been completed as of September 30, 2025, exceeding the Company's own 90-day-post-onboarding policy target — noted as a minor control gap for follow-up.

### 12.6 Ransomware and Business Continuity Considerations

We inquired about the Company's ransomware preparedness, including backup and recovery procedures, tabletop exercise history (most recent exercise conducted in September 2025, with the CFO, General Counsel, CISO, and CTO participating, results documented and remediation items tracked), and cyber insurance coverage ($50 million primary cyber liability policy, with a $75 million excess layer, subject to standard exclusions). No ransomware or business-continuity-triggering event occurred during fiscal 2025. We consider the Company's business continuity posture adequate to support the going-concern assessment in Section 7.4, absent new information.

### 12.6.1 Vulnerability Management and Penetration Testing

We reviewed the Company's vulnerability management program, which includes continuous automated scanning of production infrastructure (using, notably, ShieldNex's own CSPM technology, now applied internally — a "dogfooding" practice management highlighted favorably) and an annual third-party penetration test. The most recent penetration test (conducted in May 2025 by an independent security firm) identified 3 high-severity and 14 medium-severity findings, all of which management represented were remediated within the Company's internal SLA targets (30 days for high-severity, 90 days for medium-severity), with remediation evidenced in the security team's ticketing system. We reviewed remediation evidence for the 3 high-severity findings and confirmed timely closure. We noted that ShieldNex's Azure environment was not included in the scope of the May 2025 penetration test (which predated the acquisition's close) and that a dedicated ShieldNex-scope penetration test is planned for Q1 2026 — another integration-timing gap consistent with the pattern noted throughout Section 11.

### 12.6.2 Identity and Access Management Architecture

Nexora employs single sign-on ("SSO") via Okta for substantially all corporate and production system access, with multi-factor authentication ("MFA") enforced for all users accessing financially significant systems. We noted that ShieldNex's legacy environment, prior to acquisition, used a separate identity provider (Azure Active Directory / Entra ID) that has not yet been federated with Nexora's Okta instance, meaning ShieldNex employees currently authenticate through a parallel identity system with separate password policy and MFA enforcement configurations (which we confirmed, through inquiry and inspection of ShieldNex's Entra ID configuration, does enforce MFA, though with a different conditional-access policy set than Nexora's standard). This parallel-identity-system condition is directly relevant to our access management risk assessment in Section 11.3 and will be specifically considered in scoping our ITGC testing of the ShieldNex environment.

### 12.7 Financial Statement and Disclosure Implications

Based on our procedures to date, cybersecurity risk does not currently give rise to an accrued liability or disclosed loss contingency beyond the amounts already reflected for the April 2025 incident (expensed as incurred, approximately $180,000, immaterial). We will continue to: (a) inquire of the CISO and General Counsel at each subsequent interim period and at year-end regarding any new incidents or developments; (b) read board and audit committee minutes for cybersecurity-related discussion; (c) review the Company's cyber-incident disclosure controls and procedures as part of our understanding of the broader control environment (Section 13); and (d) evaluate whether any cybersecurity matter identified during the remainder of the audit requires reassessment of loss contingencies under ASC 450, disclosure controls evaluation, or subsequent-events consideration under ASC 855.

---

## 13. CONTROL ENVIRONMENT ASSESSMENT (COSO FRAMEWORK)

We evaluated Nexora's control environment using the five interrelated components of the COSO 2013 Internal Control — Integrated Framework: (1) Control Environment, (2) Risk Assessment, (3) Control Activities, (4) Information and Communication, and (5) Monitoring Activities, and the framework's 17 supporting principles.

### 13.1 Control Environment (COSO Component 1)

**Principle 1 — Commitment to integrity and ethical values.** Nexora maintains a written Code of Business Conduct and Ethics, last updated in January 2025, requiring annual certification by all employees (98.7% completion rate as of the certification deadline, with remaining employees on approved leave) and by all board members. The Company maintains an independent, third-party-administered ethics hotline (available in 12 languages, accessible via web and phone), with reports routed to both the General Counsel and the Chief Audit Executive to preserve an independent escalation path. We consider this principle to be appropriately designed and, based on our inquiries and review of hotline statistics (Section 10.1), operating as intended.

**Principle 2 — Board independence and oversight.** As described in Section 3.6, the board is majority independent, and the audit committee meets the financial literacy and financial expertise requirements of applicable listing standards. We reviewed board and audit committee meeting minutes for the trailing twelve months and noted appropriate engagement with management on risk topics, including a dedicated session on AI risk governance held in June 2025 and a dedicated session on the ShieldNex integration held in September 2025.

**Principle 3 — Management's organizational structure, authority, and responsibility.** Nexora maintains a documented delegation of authority ("DOA") policy specifying approval thresholds for contracts, capital expenditures, and other commitments. We noted the DOA policy was last formally updated in 2023 and had not yet been updated to reflect the ShieldNex acquisition's organizational structure as of the planning date (e.g., approval authority for former ShieldNex executives is not yet formally documented in the DOA, though we understand informal reporting lines have been communicated). We will follow up on the status of the DOA update during fieldwork.

**Principle 4 — Commitment to competence.** The finance organization requires relevant professional certifications (CPA or equivalent) for senior technical accounting roles, and the Company provides an internal technical accounting training curriculum, including specific fiscal 2025 training modules on AI cost capitalization and business combination accounting (developed in response to the ShieldNex acquisition and Copilot product launch). We noted the interim Controller (Section 10.3) is a CPA with prior public company controllership experience at a comparably sized technology company, which partially mitigates the transition risk, though we will continue to monitor the permanent Controller search process.

**Principle 5 — Accountability.** Performance evaluations for finance personnel include specific internal control and compliance objectives, and the Company's incentive compensation clawback policy (adopted in 2023 in accordance with Nasdaq listing standards implementing SEC Rule 10D-1) applies to erroneously awarded incentive compensation in the event of an accounting restatement. No clawback has been triggered to date.

### 13.2 Risk Assessment (COSO Component 2)

Nexora's enterprise risk management ("ERM") function, which reports to the CFO with dotted-line reporting to the audit committee, maintains a formal risk register updated semi-annually, with the most recent update in October 2025 identifying AI/foundation-model dependency, cybersecurity, talent retention, and integration risk (ShieldNex) as top-tier enterprise risks — consistent with our own independent risk assessment in this memo, which we consider a positive corroborating indicator regarding the design of this COSO component. We noted the ERM process appropriately considers fraud risk as a distinct risk category (COSO Principle 8) and that management's own fraud risk assessment (last updated in Q3 2025) substantially overlaps with, though is somewhat less granular than, our independent fraud risk assessment in Section 10.

### 13.3 Control Activities (COSO Component 3)

We evaluated the design of key control activities across financially significant processes, including authorization and approval controls (contract approval matrix, purchase order approval thresholds), reconciliation controls (bank reconciliations, intercompany reconciliations, sub-ledger-to-general-ledger reconciliations), and segregation of duties, both manual and automated (system-enforced role-based access restrictions). Our detailed walkthrough observations, including specific control activity design and preliminary operating effectiveness observations, are documented in Section 14.

We separately evaluated general controls over technology (COSO Principle 11), which substantially overlaps with our ITGC risk assessment in Section 11, and controls related to policies and procedures documentation (COSO Principle 12) — we noted that the Company's global accounting policy manual is comprehensive and updated at least annually but that ShieldNex-specific process documentation (e.g., detailed procedure narratives for ShieldNex's legacy billing process, Section 11.1) remains incomplete as of the planning date, consistent with the broader integration-related risk theme running through this memo.

### 13.4 Information and Communication (COSO Component 4)

We evaluated the quality of information used to support internal control functioning (COSO Principle 13), including the reliability of system-generated reports discussed in Section 11.5, and internal communication channels (COSO Principle 14), including the ethics hotline (Section 13.1), a monthly all-hands "town hall" at which the CEO and CFO discuss Company performance and, periodically, control-related initiatives, and a dedicated Slack channel used by the accounting and FP&A teams to flag unusual transactions or accounting questions in real time — a practice we view favorably as it creates a documented (searchable) contemporaneous record of judgmental accounting discussions, which we will request access to review for the audit period as part of our procedures. External communication (COSO Principle 15) includes the Company's investor relations function, whose non-GAAP and KPI disclosure practices are discussed in Sections 9.4, 9.7, and 10.3.

### 13.5 Monitoring Activities (COSO Component 5)

Ongoing monitoring (COSO Principle 16) is performed through the internal audit function's risk-based annual audit plan (approved by the audit committee), which for fiscal 2025 included audits of the revenue recognition process, the ShieldNex integration (a dedicated post-acquisition integration audit completed in October 2025, which we obtained and reviewed), user access management, and expense reimbursement compliance. We evaluated internal audit's competence, objectivity, and the quality of its work in accordance with AS 2605 and determined we can place a moderate level of reliance on specific internal audit work products, principally the ShieldNex integration audit and select ITGC testing, subject to our own re-performance of a sample of internal audit's test work (Section 16.4). Deficiency evaluation and reporting (COSO Principle 17) is evidenced through internal audit's formal issue-tracking system, which we reviewed for open items as of the planning date (Section 13.6).

### 13.6 Summary of Control Deficiencies Identified to Date

| Ref | Description | COSO Component | Preliminary Severity | Status |
|---|---|---|---|---|
| CD-24-01 (prior year) | NetSuite system administrator role SoD conflicts (11 users) | Control Activities | Significant Deficiency (FY24) | Remediated; retest planned |
| CD-24-02 (prior year) | Insufficient documentation of emergency change code review | Control Activities / IT | Significant Deficiency (FY24) | Remediated; retest planned |
| CD-25-01 | ShieldNex user access provisioning process not integrated; less formal approval workflow | Control Activities / IT | Preliminary — Deficiency, severity TBD pending testing | Open; testing planned |
| CD-25-02 | Q3 2025 NetSuite user access review completed late; remediation evidence finalized after review substantively complete | Monitoring / Control Activities | Preliminary — Deficiency, severity TBD | Open; testing planned |
| CD-25-03 | Delegation of Authority policy not updated to reflect ShieldNex organizational structure | Control Environment | Preliminary — Deficiency, likely not significant | Open; monitoring |
| CD-25-04 | Vendor risk assessment for new ShieldNex sub-processor completed outside policy SLA | Control Activities (third-party risk) | Preliminary — Minor, likely not significant | Open; monitoring |

We will finalize our severity classification (deficiency, significant deficiency, or material weakness) for each item, including any newly identified items, at the completion stage, in accordance with AS 2201.62–.70, considering both quantitative (magnitude of potential misstatement) and qualitative factors (pervasiveness, compensating controls, and the nature of the accounts affected).

---

## 14. WALKTHROUGH OBSERVATIONS

Walkthroughs were performed by the engagement team between October 20, 2025, and December 5, 2025, for each significant process, following the standard walkthrough methodology of tracing one or more transactions from origination through the general ledger, corroborated by inquiry, observation, and inspection of documentation. This section summarizes our observations, noted control gaps, and the implications for our planned testing approach.

### 14.1 Order-to-Cash / Revenue Process Walkthrough

**Transactions traced:** (1) a new-logo enterprise contract bundling core platform, Copilot, and implementation services ($1.4 million total contract value); (2) a renewal-with-upsell contract; (3) a usage-based AI Marketplace transaction settled through the metering pipeline; (4) a professional-services fixed-fee milestone billing.

**Process narrative observed:** Opportunities are created and managed in Salesforce; deal desk review is triggered automatically for any opportunity with a discount exceeding 20% off list price, non-standard payment terms, or contract value exceeding $500,000, requiring approval from the VP of Sales and, above $2 million, the CFO. Upon contract execution (via DocuSign, with the fully executed agreement automatically attached to the Salesforce opportunity record), the CPQ system generates the order form, which is used to configure the billing schedule and to determine performance obligations and SSP allocation through a rules-based configuration (with manual override capability, logged and requiring supervisor approval for any override). Revenue is recognized ratably in NetSuite based on the CPQ-to-NetSuite interface data.

**Observations:**
- We confirmed the deal-desk review control operated as designed for the sampled new-logo contract, with documented approval evidence.
- For the renewal-with-upsell transaction, we noted the CPQ-generated SSP allocation for the "upsell" Copilot uplift used a standalone selling price corridor that had not been updated since Q4 2024 SSP corridor analysis, notwithstanding the quarterly-update policy described in Section 9.2 — we will investigate whether this reflects an isolated exception or a broader control operating effectiveness gap, and will expand our SSP corridor testing accordingly.
- For the usage-based transaction, we traced a sample of metering events from the Kafka event log through the Snowflake aggregation layer to the revenue recognized in NetSuite and noted the reconciliation was accurate for the transactions traced; however, we noted that the reconciliation between total metered usage and total usage billed is performed monthly by a single analyst without independent review, which we consider a control design gap warranting either a compensating control identification or classification as a deficiency, pending further evaluation.
- For the professional-services milestone billing, the percentage-of-completion calculation is maintained in a spreadsheet (not a system-enforced calculation), and we noted the spreadsheet lacked version control or a formal sign-off/lock mechanism after monthly close, a common risk in spreadsheet-dependent processes; we will test this control point specifically for a larger sample given the manual nature of the process.
- The manual SSP override log (referenced above) was reviewed for the trailing twelve months; we noted 34 overrides, of which supervisor approval evidence was present for 31; the 3 exceptions are individually and in aggregate below our nominal threshold but will be discussed with management as a control operation matter, and we will assess whether this is indicative of a broader population issue requiring an increased sample size.

### 14.2 Procure-to-Pay Walkthrough

**Transactions traced:** (1) a recurring AWS cloud infrastructure invoice (approximately $4.1 million monthly); (2) a one-time capital equipment purchase (GPU server hardware, $2.3 million); (3) a professional services vendor invoice related to the ShieldNex integration.

**Observations:** The three-way match control (purchase order, receipt/approval, invoice) operated as designed for all three items traced. We noted that the foundation-model provider invoice (Section 8.1(a)) is not processed through the standard three-way match workflow because it is a usage-based, non-PO-backed arrangement; instead, it is subject to a monthly manual reconciliation between vendor-reported token consumption and Nexora's internally metered consumption data, reviewed and approved by the Director of FP&A. We traced this reconciliation for two months in the walkthrough period and noted a variance of 2.1% and 3.4%, respectively, both within the Company's 5% tolerance threshold, but we will evaluate whether this tolerance threshold is appropriately calibrated given the materiality of this cost line (Section 8.2(4)) and will expand testing given the inherent estimation risk in vendor-reported usage data that Nexora cannot independently and fully verify.

### 14.3 Payroll and Stock-Based Compensation Walkthrough

**Transactions traced:** (1) a standard biweekly payroll run; (2) a new-hire equity grant; (3) a vesting event for the market-condition AI-talent retention award (Section 15.5).

**Observations:** Standard payroll processing controls (ADP interface reconciliation, management review and approval of the payroll register prior to funding) operated as designed. For the market-condition award, we noted that the underlying Monte Carlo valuation model is prepared by a third-party valuation firm engaged by the Company, with inputs (expected volatility, risk-free rate, correlation assumptions between ARR milestone achievement and stock price) reviewed and approved by the VP of Finance; we will engage our own valuation specialist to independently evaluate the reasonableness of these inputs and potentially develop an independent range (Section 15.5).

### 14.4 Financial Statement Close Process Walkthrough

**Observations:** The close process follows a documented close calendar with a target 6-business-day close. Journal entries above $500,000 require a secondary reviewer/approver in NetSuite's workflow engine (system-enforced). We noted, consistent with Section 10.3, that journal entry posting access is held by 46 users, a population we consider broad relative to peer benchmarks reviewed by our IT audit specialist, and that a formal, continuous segregation-of-duties conflict monitoring control (as opposed to the quarterly review noted in Section 10.3) is not currently in place — we will discuss this observation with management as a potential efficiency/control-design improvement opportunity, separate from our fraud-risk-driven journal entry testing (Section 10.6). We also observed the pilot use of the AI-assisted reconciliation tool (Section 8.2(6)) for a sample of intercompany reconciliations; all AI-suggested adjustments in our walkthrough sample were reviewed and separately approved by a reconciliation preparer's supervisor before posting, consistent with management's description, and we noted the tool's suggestions included an audit-trail annotation distinguishing AI-suggested from manually prepared entries, which we view as a positive control design feature supporting our ability to audit this new process.

### 14.5 Goodwill and Intangible Asset Impairment Process Walkthrough

**Observations:** We walked through management's Q3 2025 interim goodwill impairment triggering-event evaluation (performed in response to the market capitalization decline noted in Section 3.4), which concluded that while a triggering event existed for the legacy on-premises reporting unit, no impairment resulted from the quantitative test performed (fair value exceeded carrying value by approximately 8%). We noted the discounted cash flow model was prepared by FP&A with review by the Corporate Controller function (currently the interim Controller, Section 10.3) and validated by an external valuation specialist engaged by management. Given the relatively thin 8% headroom, we have identified this as a significant estimate requiring detailed substantive testing at year-end regardless of the interim conclusion (Section 15.3).

### 14.6 ShieldNex Integration and Legacy System Walkthrough

**Observations:** As discussed in Sections 11.1, 11.3, and 13.3, ShieldNex's legacy Chargebee billing system and separate NetSuite instance remain in operation, with a manual monthly consolidation entry recorded to incorporate ShieldNex's trial balance into Nexora's consolidated financial statements via OneStream. We traced the August and September 2025 consolidation entries and noted the mapping of ShieldNex's chart of accounts to Nexora's standard chart of accounts is maintained in a manually updated crosswalk spreadsheet, reviewed monthly by the Corporate Controller function, with no system-enforced control preventing an unmapped or miscoded ShieldNex account from being omitted from consolidation. We consider this a heightened risk area for completeness of the ShieldNex balances within the consolidated financial statements and will design expanded substantive procedures accordingly, including an independent recalculation of the full ShieldNex-to-consolidated mapping for the year-end trial balance.

### 14.7 Treasury and Cash Management Walkthrough

**Transactions traced:** (1) a wire transfer related to the ShieldNex acquisition closing payment; (2) a routine month-end investment sweep between operating cash and the Company's short-term investment portfolio (money market funds and investment-grade commercial paper); (3) the June 2025 draw and subsequent repayment of $150 million under the revolving credit facility used to partially fund the ShieldNex acquisition (Section 3.4).

**Observations:** Wire transfers above $1 million require dual approval within the Company's treasury management system (a system-enforced control, confirmed through inspection of the approval workflow configuration and a sample of approval logs). We noted the acquisition closing payment, given its size and one-time nature, was additionally reviewed by the CFO and General Counsel outside the standard treasury workflow, with a manual approval memo retained in the deal file — appropriate given the non-routine nature of the transaction. Bank reconciliations for all operating accounts are prepared monthly and reviewed by the Treasury Manager, with reconciling items over $50,000 requiring explanation; we tested the August and September 2025 reconciliations and noted no unresolved reconciling items outside policy tolerance. We consider treasury and cash management to be a lower-risk process, consistent with our overall combined audit approach for this area, and do not plan to expand procedures beyond our standard controls-reliance testing.

### 14.8 Equity and Capital Markets Transactions Walkthrough

**Transactions traced:** (1) the issuance of approximately $140 million of Nexora common stock as partial consideration for the ShieldNex acquisition (Section 3.4); (2) the September 2025 Form S-3 shelf registration filing (Section 2.2); (3) a routine quarterly stock option exercise batch.

**Observations:** The valuation and accounting for the stock consideration issued in the ShieldNex acquisition (measured at the acquisition-date closing price per the definitive merger agreement's pricing mechanism) was reviewed by the Corporate Controller function and corroborated against the merger agreement's specified valuation methodology; we will independently recompute this valuation as part of our substantive procedures over the business combination (Section 15.2). We noted the S-3 shelf registration did not involve an actual securities issuance as of the planning date (it is a shelf "on the shelf" for potential future capital raises) and therefore has no direct current-period accounting impact, though it did require our issuance of a comfort letter (Section 2.2) subject to separate procedures under AS 6101. No control deficiencies were noted in this walkthrough.

### 14.9 Income Tax Process Walkthrough

**Observations:** The income tax provision is prepared quarterly by the Company's in-house tax team with support from an external tax advisory firm for complex matters (transfer pricing, Pillar Two). We noted the effective tax rate reconciliation and the deferred tax asset valuation allowance analysis are both reviewed by the VP of Tax and the CFO. Given the complexity introduced by Pillar Two (Section 15.9) and the transfer pricing arrangements between the U.S. parent and the Irish and Indian subsidiaries, we have identified income taxes as a significant estimate requiring specialist involvement (Section 4.4).

### 14.10 Summary of Walkthrough-Driven Scope Adjustments

Based on the observations above, we have made the following adjustments to our planned audit approach: (a) expanded SSP corridor and override testing (Section 14.1); (b) increased sample size and independent recalculation for the usage-metering-to-billing reconciliation (Section 14.1); (c) expanded testing of the ShieldNex chart-of-accounts mapping and consolidation completeness (Section 14.6); (d) expanded vendor cost reconciliation testing for the foundation-model provider (Section 14.2); and (e) a decision to treat the professional-services percentage-of-completion spreadsheet as a manual, non-automated control point requiring a larger sample size than would be applied to a system-enforced control, consistent with AS 2201.46's guidance on the nature of controls affecting the extent of testing.

---

## 15. SIGNIFICANT ACCOUNTING ESTIMATES

AS 2501 requires us to evaluate the reasonableness of accounting estimates, including fair value measurements, and to identify significant estimates with a high degree of estimation uncertainty. The following estimates have been identified as significant for the fiscal 2025 audit, ranked in order of the engagement team's assessed combination of estimation uncertainty, management judgment/subjectivity, and potential magnitude of misstatement.

### 15.1 Revenue-Related Estimates (Cross-Reference to Section 9)

Standalone selling price allocation, variable consideration for usage-based AI revenue, and the ShieldNex deferred revenue fair value haircut are each significant estimates in their own right, fully discussed in Section 9. We do not repeat that analysis here but note that, taken together, these revenue-related estimates represent the single largest source of aggregate estimation uncertainty in the financial statements, given the size of the revenue base and the number of distinct judgmental inputs involved.

### 15.2 Business Combination Accounting — ShieldNex Acquisition

**Nature of the estimate:** Under ASC 805, Nexora was required to recognize identifiable assets acquired and liabilities assumed at fair value as of the July 1, 2025 acquisition date, with any excess of consideration transferred over net identifiable assets recorded as goodwill. Management, with the assistance of an external valuation specialist, allocated the $740 million total purchase consideration as follows (preliminary, subject to the measurement period which remains open through June 30, 2026): developed technology intangible asset, $185 million (9-year useful life, relief-from-royalty method, 14% royalty rate assumption); customer relationships intangible asset, $95 million (10-year useful life, multi-period excess earnings method); trade name, $12 million (3-year useful life, relief-from-royalty method); acquired deferred revenue, $28 million fair value (Section 9.4); net working capital and other tangible assets/liabilities, $34 million; deferred tax liability on identified intangibles, $(71) million; and residual goodwill of $457 million (62% of total consideration).

**Key judgments and estimation uncertainty:** (a) the royalty rate and discount rate (14.5% weighted-average cost of capital) used in valuing developed technology and customer relationships; (b) the useful life assumptions, particularly for developed technology, given the AI/cybersecurity technology obsolescence risk discussed in Section 8.2(2); (c) the attrition rate assumption (12% annual) used in the customer relationships valuation; and (d) the completeness of identified intangible assets — we will specifically evaluate whether any acquired in-process research and development, assembled workforce (which does not qualify as a separately identifiable intangible asset and should be subsumed within goodwill), or other unrecorded intangibles (e.g., a data asset comprising ShieldNex's proprietary vulnerability database) were appropriately considered and, where appropriate, separately valued or explicitly excluded with adequate rationale.

**Planned procedures:** Our valuation specialist will independently evaluate the valuation methodology, assumptions, and mathematical accuracy of management's PPA model; we will test the completeness of the opening balance sheet through inspection of the acquisition agreement, disclosure schedules, and net working capital true-up settlement; we will evaluate the reasonableness of the goodwill residual (a high goodwill percentage, while not unusual for a technology acquisition, warrants specific scrutiny of whether any value was inappropriately shifted to unamortized goodwill rather than amortizable intangibles); and we will review any measurement-period adjustments recorded during the remainder of fiscal 2025 and evaluate whether they were properly identified as measurement-period adjustments (retrospective) versus post-measurement-period changes in estimate (prospective).

### 15.3 Goodwill and Long-Lived Asset Impairment

**Nature of the estimate:** Nexora tests goodwill for impairment annually as of October 1 (with the ShieldNex reporting unit's initial goodwill first tested as of October 1, 2025) and whenever a triggering event occurs, per ASC 350. The Company has three reporting units: NexoraIQ Core Platform, ShieldNex, and Legacy On-Premises. As discussed in Section 14.5, management identified a triggering event for the Legacy On-Premises reporting unit during Q3 2025 due to sustained revenue decline (this product line, representing approximately 3% of consolidated revenue, is being sunset in favor of cloud migration) and performed an interim quantitative impairment test, concluding fair value exceeded carrying value by approximately 8% (headroom of approximately $6.2 million on a reporting unit with $77.5 million of allocated goodwill).

**Key judgments and estimation uncertainty:** (a) revenue growth (decline) rate assumptions for the Legacy On-Premises unit through the explicit forecast period and terminal growth rate; (b) the discount rate (13.8% used for this reporting unit, reflecting higher risk than the Company's overall 11.5% weighted-average cost of capital); (c) the customer migration/attrition assumptions as customers transition to the cloud platform (with associated revenue recognized within the NexoraIQ Core Platform reporting unit rather than lost entirely — a reallocation assumption we will specifically scrutinize for consistency with actual historical migration experience); and (d) given the thin 8% headroom, the reasonable possibility that a change in a key assumption could result in a materially different conclusion, which triggers specific disclosure requirements under ASC 275 (Risks and Uncertainties) regarding estimates that are reasonably likely to change materially in the near term.

Additionally, we will evaluate whether the sustained decline in Nexora's overall market capitalization relative to book value (Section 3.4) constitutes a triggering event requiring interim impairment testing for the other two reporting units (NexoraIQ Core Platform and ShieldNex) as of any period prior to the annual October 1 test date, even though management's own assessment (which we will challenge) concluded no triggering event existed for those units.

**Planned procedures:** Independent evaluation by our valuation specialist of the discount rate, growth rate, and terminal value assumptions against external market data and the Company's own historical forecasting accuracy (a retrospective review comparing prior-year forecasts to actual results, as a test of management's forecasting bias); sensitivity analysis to quantify the change in key assumptions that would result in a different conclusion; evaluation of the reconciliation between the aggregate fair value of all reporting units and the Company's overall market capitalization (a required reasonableness check under ASC 350-20-35-22 through 35-24); and evaluation of the adequacy of ASC 275 disclosure given the thin headroom identified.

### 15.4 Capitalized Software and AI Development Costs

**Nature of the estimate:** Nexora capitalizes costs to develop internal-use software under ASC 350-40 (for internally used systems) and costs to develop software to be marketed externally under ASC 985-20 (for its NexoraIQ and Copilot products, following the "technological feasibility" model based on a working model). For fiscal 2025, management forecasts capitalized software development costs of approximately $94 million (including approximately $31 million specifically related to Copilot/AI feature development), against total R&D expense (including capitalized amounts) of approximately $520 million, representing an 18% capitalization rate (Section 6.4).

**Key judgments and estimation uncertainty:** (a) the determination of the point of technological feasibility, which as discussed in Section 8.2(1) is particularly judgmental for AI/machine learning features given their iterative, continuous-improvement development pattern rather than discrete "working model" milestones; (b) the allocation of individual engineer/data scientist time between capitalizable development activities and non-capitalizable activities (research, maintenance, and post-release bug fixes), which relies on a self-reported time-tracking system (Jira time-tracking labels) rather than an independently verified allocation; (c) the useful life assigned to capitalized costs (currently 3 years company-wide, including for AI-specific capitalized assets, which we will specifically challenge given foundation-model-driven obsolescence risk, Section 8.2(2)); and (d) whether costs incurred to fine-tune or retrain models on updated foundation-model versions (as opposed to costs to build new capabilities) should be capitalized as an enhancement or expensed as maintenance, an area lacking specific authoritative guidance (Section 6.5) where we will consult National Office.

**Planned procedures:** Testing of a sample of capitalized projects against the capitalization policy criteria, including inspection of project documentation (design specifications, technological feasibility assessment memos) and interview of engineering leads (not solely finance personnel) regarding the nature of the underlying development work; analytical testing of the capitalization rate trend over time and by product line, benchmarked against the peer data in Section 6.4, with specific inquiry into any significant period-over-period change; recalculation of amortization for a sample of capitalized asset pools; and an assessment of whether any previously capitalized AI-related assets show impairment indicators given foundation-model version changes that occurred during fiscal 2025 (specifically, the third-party foundation-model provider released a new model generation in Q2 2025, which management represented did not require substantial rework of Nexora's RAG layer — a representation we will independently corroborate with engineering personnel).

### 15.5 Stock-Based Compensation — Market-Condition AI Talent Retention Awards

**Nature of the estimate:** In response to the AI talent competition discussed in Section 6.2(6), Nexora's compensation committee approved, in March 2025, a new performance stock unit ("PSU") award program for approximately 140 employees in AI/ML technical roles, vesting based on the achievement of specified Copilot ARR milestones ($200 million, $350 million, and $500 million, each measured over a trailing-twelve-month period) combined with a relative total shareholder return ("TSR") modifier compared to a custom peer index (a market condition under ASC 718), requiring a Monte Carlo simulation valuation model at grant date (with no subsequent remeasurement, consistent with market-condition award accounting, though updated estimates of the derived service period and any change in the ARR-milestone performance-condition probability assessment continue to be required each reporting period, since the ARR milestone is treated as a performance condition subject to probability assessment, layered with the TSR market condition already embedded in grant-date fair value).

**Key judgments and estimation uncertainty:** (a) grant-date Monte Carlo model inputs, including expected volatility (32%, based on a blend of historical and implied volatility), the correlation assumption between Nexora's stock price and the custom peer index (0.71), and the risk-free rate; (b) the derived service period output from the Monte Carlo model, which determines the expense attribution pattern; (c) the ongoing quarterly reassessment of the probability of achieving each ARR milestone (a performance condition), which directly affects the timing and amount of compensation expense recognized and which is inherently linked to the same Copilot ARR growth assumptions relevant to revenue risk (Section 9) and impairment testing (Section 15.3) — creating an important consistency check across multiple significant estimates that we will specifically perform; and (d) forfeiture estimates given elevated technical talent turnover (Section 6.2(6), Section 7.2).

**Planned procedures:** Independent Monte Carlo model development by our valuation specialist to develop a reasonable range and compare to management's grant-date valuation; recalculation of the quarterly ARR-milestone probability assessment and corroboration against the same underlying Copilot ARR forecast data used in revenue analytics (Section 9.7) and impairment testing (Section 15.3), specifically testing for internal consistency (i.e., that management is not using an optimistic ARR forecast to support a lower stock compensation expense accrual while simultaneously using a more conservative forecast to support goodwill headroom, or vice versa); and testing of the population of award recipients for consistency with the compensation committee's approved grant list.

### 15.6 Cost of Revenue Estimates — Vendor Accruals

As discussed in Sections 8.1(a), 8.2(4), and 14.2, the estimation of accrued foundation-model API costs based on internally metered token consumption (pending vendor invoice reconciliation) is a significant estimate given the 5% variance tolerance observed in our walkthrough and the growing significance of this cost line (management forecasts foundation-model costs of approximately $210 million for fiscal 2025, representing a majority of total cost of revenue growth year-over-year). We will test the accrual methodology, obtain a vendor confirmation of cumulative billed amounts as of year-end, and evaluate the historical accuracy of quarter-end accrual estimates compared to subsequent actual vendor invoices (a retrospective look-back analysis).

### 15.7 Allowance for Credit Losses

Under ASC 326 (CECL), Nexora estimates expected credit losses on accounts receivable and contract assets using a loss-rate method based on historical collection experience, adjusted for current conditions and reasonable and supportable forecasts. Given the elevated days sales outstanding noted in Section 6.4 and the extended payment terms trend (Section 6.2(1)), we identified this as a significant estimate requiring specific attention to whether the historical loss-rate pool appropriately reflects the risk profile of recently originated receivables with longer payment terms (which may have inherently different, and potentially higher, loss characteristics than the shorter-term receivables that dominate the historical loss experience used to develop the model), and whether qualitative overlay adjustments (if any) are adequately supported. We will test a sample of aged receivables for collectability indicators, evaluate subsequent cash collection through the report date, and independently assess the reasonableness of the qualitative overlay, if any.

### 15.8 Loss Contingencies and Legal Matters

We inquired of the General Counsel and obtained a draft of the annual legal representation letter request, identifying the following matters requiring evaluation under ASC 450: (a) a routine, ordinary-course commercial contract dispute with a former channel partner in Brazil (approximately $4.5 million claimed, management assesses the likelihood of loss as reasonably possible but not probable, no accrual recorded, disclosure planned); (b) a patent infringement claim filed by a competitor in September 2025 alleging that certain Copilot RAG-layer functionality infringes a patent related to natural-language query processing (early stage, outside litigation counsel has not yet formed a view on the likelihood of an unfavorable outcome; we will evaluate the adequacy of disclosure given the early procedural stage and will follow developments through the completion of fieldwork); and (c) the intellectual property indemnification exposure related to the foundation-model licensing arrangement (Section 8.1(a)), where management represents no claims have been asserted and no accrual is considered necessary. We will send external legal confirmation letters to all law firms identified as handling matters for the Company and will evaluate responses in accordance with AS 2505.

### 15.9 Income Taxes

**Nature of the estimate:** Nexora's income tax provision involves significant judgment regarding (a) the realizability of net deferred tax assets, including U.S. federal and state net operating loss carryforwards and foreign tax credits, requiring a valuation allowance assessment under ASC 740-10-30 based on the four sources of taxable income and the weighting of positive and negative evidence (management's current forecast supports continued profitability sufficient to realize substantially all domestic deferred tax assets, with a valuation allowance maintained only against certain state NOLs with shorter carryforward periods and certain foreign NOLs in jurisdictions with a history of losses); (b) uncertain tax positions under ASC 740-10-25 (FIN 48), including the Company's transfer pricing methodology for intercompany arrangements between the U.S. parent and the Irish subsidiary (which holds certain non-U.S. IP rights and licenses them back to operating subsidiaries) and the Indian subsidiary (a cost-plus R&D services arrangement); and (c) for the first time in fiscal 2025, the impact of the OECD Pillar Two global minimum tax (15% minimum effective tax rate on a jurisdictional basis), which affects the Company's Irish subsidiary given Ireland's statutory rate structure and various incentives that may reduce the Irish effective tax rate below 15% before top-up tax considerations.

**Key judgments and estimation uncertainty:** the sufficiency and reliability of the Company's transfer pricing documentation and benchmarking studies (prepared by an external transfer pricing specialist firm); the appropriateness of the valuation allowance conclusion given the profitability forecast's alignment (or lack thereof) with the same growth assumptions used in goodwill impairment testing and stock compensation performance-condition assessments (another important cross-estimate consistency check, per Section 15.5); and the technical application of the Pillar Two rules, an area of continued regulatory evolution (including OECD administrative guidance updates issued throughout 2024–2025) where even experienced tax specialists have noted implementation complexity and interpretive uncertainty.

**Planned procedures:** Use of our tax specialists to evaluate the transfer pricing documentation, the valuation allowance analysis (including a specific cross-check of the profitability forecast against other uses of forecasts elsewhere in the financial statements, per above), the uncertain tax position analysis, and the Pillar Two computation methodology; and evaluation of the adequacy of related disclosures, including the effective tax rate reconciliation and any disclosed uncertainty regarding the impact of evolving international tax rules.

### 15.10 Operating Leases and Right-of-Use Assets

**Nature of the estimate:** Under ASC 842, Nexora recognizes right-of-use ("ROU") assets and lease liabilities for its corporate office leases (principal locations in Austin, San Francisco, and Dublin) and, following the ShieldNex acquisition, a data-center colocation lease in Northern Virginia assumed as part of the acquired liabilities. Measurement requires estimation of the discount rate (incremental borrowing rate, since the rate implicit in the lease is not readily determinable for substantially all of the Company's leases) and judgment regarding the lease term, including whether renewal options are reasonably certain to be exercised.

**Key judgments:** (a) the incremental borrowing rate methodology, which the Company derives using a synthetic credit rating approach combined with observable market yield curves for comparable-duration, comparable-credit-quality debt, given that Nexora does not have directly comparable collateralized borrowings; (b) the lease term assessment for the Austin headquarters lease, which includes a renewal option management has concluded is reasonably certain to be exercised (extending the lease term by five years) based on the Company's substantial build-out investment and stated intent to remain at the location, a judgment we will corroborate through inquiry and inspection of capital investment plans; and (c) the assumed useful life and any impairment indicators for leasehold improvements, particularly at any office location where the Company has reduced its real estate footprint following continued hybrid/remote work policies (Nexora reduced its San Francisco office footprint by approximately 40% in a sublease transaction completed in Q2 2025, which resulted in a partial ROU asset impairment of approximately $3.1 million, tested and recorded by management, that we will independently test for appropriateness of the impairment measurement).

**Planned procedures:** Recalculation of the incremental borrowing rate for a sample of leases; inspection of lease agreements and renewal option assessments; and testing of the San Francisco sublease impairment calculation, including the discount rate and sublease income assumptions used in the fair value measurement.

### 15.11 Segment Reporting Judgments

**Nature of the estimate/judgment:** While not a quantitative "estimate" in the traditional sense, the determination of Nexora's operating and reportable segments under ASC 280 involves significant judgment regarding the identification of the chief operating decision maker ("CODM"), the information regularly reviewed by the CODM, and the aggregation criteria applied to combine operating segments into reportable segments. Following the ShieldNex acquisition, management evaluated whether ShieldNex constitutes a separate operating segment or should be aggregated within the existing Platform & Subscription segment (Section 3.2), concluding that ShieldNex results are regularly reviewed by the CEO (the CODM) at a level of disaggregation consistent with treating it as a distinct component, but that it qualifies for aggregation with the Platform & Subscription segment under ASC 280-10-50-11 given similar economic characteristics (comparable gross margins, comparable customer base and sales channel, and comparable long-term growth expectations), resulting in continued presentation as a single reportable segment inclusive of ShieldNex, supplemented by voluntary disaggregated revenue disclosure (Section 9.1) to provide transparency without triggering separate segment reporting.

**Audit considerations:** We will evaluate the CODM information package (the monthly business review deck reviewed by the CEO) to independently assess whether the level of disaggregation and the nature of decisions made using this information are consistent with management's segment conclusion, and will specifically evaluate whether the aggregation criteria conclusion remains appropriate in light of the new ASU 2023-07 (Segment Reporting — Improvements to Reportable Segment Disclosures) requirements regarding disclosure of significant segment expenses regularly provided to the CODM, which are effective for Nexora's fiscal 2025 annual financial statements. We will test management's identification of "significant segment expenses" for completeness and consistency with the CODM reporting package.

### 15.12 Cross-Estimate Consistency Review

Given that several of the estimates above (goodwill impairment, Section 15.3; stock compensation performance conditions, Section 15.5; income tax valuation allowance, Section 15.9; and revenue variable consideration, Section 9.3) rely, directly or indirectly, on overlapping underlying management forecasts of Copilot ARR growth and overall Company profitability, we have specifically planned a **cross-estimate consistency procedure** as part of our completion-stage overall review: we will obtain and compare the specific growth and profitability assumptions used in each estimate, evaluate whether any inconsistencies exist that are not adequately explained by legitimate differences in the nature or time horizon of each estimate, and consider whether any such inconsistency indicates a broader indicator of management bias (Section 10.6) requiring escalation.

---

## 16. OVERALL AUDIT RESPONSE, TIMELINE, AND STAFFING

### 16.1 Overall Responses to Assessed Risks

Consistent with AS 2110.71–.73, our overall responses to the assessed risks documented throughout this memo include: (a) assigning more experienced, technically specialized team members (including the IT audit specialists, valuation specialists, and tax specialists described in Section 4.4) to the higher-risk areas identified in Sections 9, 10, 11, 12, and 15; (b) incorporating additional elements of unpredictability into our procedures, including the unannounced procedures described in Section 9.8 and unannounced site visits to two regional sales offices (including the EMEA office relevant to the whistleblower matter, Section 10.5); (c) increasing the overall extent of procedures, including sample sizes, for accounts and processes affected by the specific risks identified; and (d) maintaining a heightened degree of professional skepticism throughout the engagement, particularly in evaluating management's estimates and explanations for unusual or unexpected analytical relationships.

### 16.2 Engagement Timeline

| Phase | Period | Key Milestones |
|---|---|---|
| Planning | September – December 2025 | Risk assessment, walkthroughs (complete), this memo, audit committee planning communication (January 2026) |
| Interim fieldwork | January – February 2026 | ITGC testing, controls testing (revenue, procure-to-pay, payroll), interim substantive procedures |
| Year-end fieldwork | February – March 2026 | Substantive testing of year-end balances, significant estimates, confirmations, subsequent events review |
| Completion | March 2026 | EQR review, National Office consultation close-out, audit committee reporting, opinion issuance (target: March 2, 2026, ahead of the Form 10-K filing deadline) |

### 16.3 Staffing

The engagement team comprises: T. Okafor (Engagement Partner), M. Chen (Engagement Quality Reviewer), J. Alvarez (Senior Manager), two Managers (revenue/general ledger and ShieldNex/business combination workstreams, respectively), four Senior Associates, six Associates, two IT Audit Specialists, a Valuation Specialist team (2 professionals), a Tax Specialist team (2 professionals), and the Harrow & Vance India LLP component team (1 manager, 2 seniors) for the Nexora India specified procedures.

### 16.4 Use of the Work of Internal Audit and Others

As discussed in Section 13.5, we plan to use the work of internal audit to a moderate extent for the ShieldNex integration audit and select ITGC testing, subject to independent re-performance procedures on a sample of their work in accordance with AS 2605.16–.19. We will not use the work of internal audit for any procedures directly related to the significant risks identified in Sections 9 and 10 (revenue recognition and fraud), consistent with AS 2605.29's guidance limiting the use of internal audit's work for the significant risk areas of an engagement. We will evaluate the work of Whitmore & Associates LLP (SOC 2 auditor, Section 12.3) under AS 2601 for the limited purpose described in that section.

### 16.5 Communications with the Audit Committee

We will communicate the matters described in this memo, updated as necessary based on procedures performed, to the audit committee at the January 2026 planning session, including our assessment of fraud risk, significant risks, the planned use of specialists and component auditors, and our preliminary views on the areas of critical accounting estimates likely to be discussed in the critical audit matters section of our report, which we currently expect will include revenue recognition (Section 9), the ShieldNex business combination (Section 15.2), and goodwill impairment (Section 15.3), subject to final determination at completion in accordance with AS 3101.

### 16.6 Engagement Quality Review

M. Chen will perform an engagement quality review in accordance with AS 1220, including review of this planning memorandum, the fraud risk assessment, the materiality determination, significant estimates, and the overall conclusion, prior to release of our report.

### 16.7 Detailed Audit Program Cross-Reference

The table below cross-references each major risk area identified in this memo to the specific audit program section, lead specialist, and planned testing period, to support engagement team coordination and review:

| Risk Area | Memo Reference | Audit Program Section | Lead | Planned Testing Period |
|---|---|---|---|---|
| Revenue recognition (SSP, variable consideration, cut-off) | Section 9 | AP-400 series | Manager 1 / Senior Associates 1–2 | Interim (controls) + Year-end (substantive) |
| Fraud / management override | Section 10 | AP-100 series | Senior Manager / IT Audit | Year-end (JE testing), ongoing (skepticism) |
| ITGCs (access, change management) | Section 11 | AP-900 series | IT Audit Specialists | Interim |
| Cybersecurity disclosure read-for-consistency | Section 12 | AP-950 | Manager 1 | Completion |
| Business combination (ShieldNex PPA) | Section 15.2 | AP-700 | Manager 2 / Valuation Specialist | Year-end |
| Goodwill and intangible impairment | Section 15.3 | AP-710 | Manager 2 / Valuation Specialist | Year-end |
| Capitalized software / AI development costs | Section 15.4 | AP-720 | Senior Associate 3 | Interim + Year-end |
| Stock-based compensation (PSU market condition) | Section 15.5 | AP-730 | Manager 2 / Valuation Specialist | Year-end |
| Vendor cost accruals (foundation model) | Section 15.6 | AP-500 | Senior Associate 1 | Year-end |
| Allowance for credit losses | Section 15.7 | AP-410 | Senior Associate 2 | Year-end |
| Loss contingencies / legal | Section 15.8 | AP-800 | Senior Manager | Year-end |
| Income taxes / Pillar Two | Section 15.9 | AP-600 | Tax Specialists | Year-end |
| Leases | Section 15.10 | AP-810 | Senior Associate 4 | Year-end |
| Segment reporting | Section 15.11 | AP-950 | Manager 1 | Completion |
| ShieldNex consolidation completeness | Section 14.6 | AP-720 | Manager 2 | Year-end |

This cross-reference will be maintained as a living document in the audit file and updated as the engagement progresses from planning through completion, with any material changes to scope, staffing, or timing documented as a memo addendum and communicated to the full engagement team and the EQR.

---

## 17. APPENDICES

### Appendix A — Detailed Risk of Material Misstatement Summary by Significant Account

The following summarizes, at a high level, the significant accounts identified during planning, the relevant assertions most at risk, and whether each is designated a significant risk. The full working paper, including inherent risk and control risk ratings by assertion, is maintained in the audit file (index AP-050).

| Significant Account | Relevant Assertions at Elevated Risk | Significant Risk? | Cross-Reference |
|---|---|---|---|
| Revenue — Subscription | Accuracy (SSP), Cutoff | Yes | Section 9.2, 9.6 |
| Revenue — Usage-based AI | Completeness, Accuracy (variable consideration) | Yes | Section 9.3 |
| Deferred revenue | Completeness, Accuracy (ShieldNex fair value) | Yes | Section 9.4 |
| Goodwill | Valuation | Yes | Section 15.3 |
| Acquired intangible assets | Valuation, Existence | Yes | Section 15.2 |
| Capitalized software | Valuation, Existence (proper capitalization) | Yes | Section 15.4 |
| Accounts receivable / allowance for credit losses | Valuation | No (elevated, not designated significant risk) | Section 15.7 |
| Stock-based compensation liability/equity | Valuation | Yes | Section 15.5 |
| Income tax provision / deferred taxes | Valuation, Completeness (UTPs) | Yes | Section 15.9 |
| Accrued cost of revenue (vendor accruals) | Completeness, Accuracy | No (elevated, not designated significant risk) | Section 15.6 |
| Operating lease ROU assets/liabilities | Valuation (discount rate, term) | No | Section 15.10 |
| Cash and investments | Existence | No (low risk) | Section 14.7 |
| Legal contingencies | Completeness, Valuation | No (elevated, not designated significant risk) | Section 15.8 |

### Appendix B — Fraud Brainstorming Session Minutes (Summary)

**Date:** November 18, 2025. **Attendees:** T. Okafor (Partner), M. Chen (EQR), J. Alvarez (Senior Manager), 2 Managers, 4 Senior Associates, 2 IT Audit Specialists, 1 Forensic Accounting Specialist (consultative). **Key discussion points:** (1) walked through each element of the fraud triangle for the entity as a whole and for each significant class of transactions; (2) specifically discussed the risk of management override given the ShieldNex acquisition's judgmental purchase accounting and the CFO's equity incentives; (3) discussed the EMEA whistleblower report in detail, including a decision to expand confirmation procedures (Section 10.5, FR-4); (4) considered whether any indication of misconduct by the previous Corporate Controller contributed to that individual's August 2025 departure — management represented the departure was for personal/career reasons unrelated to any control or ethics concern, which we will corroborate through review of the individual's exit interview documentation and HR file, to the extent available and appropriate; (5) brainstormed specific "what could go wrong" scenarios for revenue recognition, capitalized software, and the AI-talent retention PSU program; and (6) agreed on the specific fraud risk register documented in Section 10.5 of this memo, to be revisited at the interim and year-end review stages.

### Appendix C — IT Audit Scoping Memorandum (Summary)

**In-scope applications for ITGC testing:**

| Application | Vendor/Hosting | In Scope Reason | Testing Approach |
|---|---|---|---|
| NetSuite | Oracle NetSuite, SaaS | General ledger, sub-ledgers, consolidation input | Full ITGC (access, change, operations) |
| OneStream | OneStream Software, SaaS | Consolidation | Full ITGC |
| Salesforce (CRM + CPQ + Revenue Cloud) | Salesforce, SaaS | Contract creation, billing, revenue interface | Full ITGC |
| MuleSoft | Salesforce, SaaS | System interface / middleware | Interface controls testing |
| Kafka / Snowflake metering pipeline | AWS-hosted, internally developed | Usage-based revenue measurement | Full ITGC + data reliability testing |
| ADP Workforce Now | ADP, SaaS | Payroll processing | Full ITGC (SOC 1 reliance + limited direct testing) |
| Shareworks | Morgan Stanley, SaaS | Equity administration | Full ITGC (SOC 1 reliance + limited direct testing) |
| Chargebee (ShieldNex legacy) | Chargebee, SaaS | ShieldNex billing (pre-migration) | Full ITGC, expanded scope given integration risk |
| AWS (production infrastructure) | Amazon Web Services | Underlying infrastructure for all above | SOC 2 reliance + direct configuration testing |
| Azure (ShieldNex infrastructure) | Microsoft Azure | Underlying infrastructure for ShieldNex | Direct testing (no mature SOC report available) |

**Data analytics planned:** full-population journal entry testing (NetSuite); full-population revenue transaction testing with risk-based stratification (Salesforce/NetSuite interface); Benford's Law analysis on manually entered accrual amounts; and reperformance of the usage-metering-to-revenue reconciliation for 100% of months in the audit period (rather than a sample), given the criticality of this IT-dependent process to the variable consideration estimate (Section 9.3).

### Appendix D — Group Audit Instructions to Harrow & Vance India LLP (Summary)

Instructions issued to the component team cover: scope of procedures (specified procedures over R&D cost accumulation and capitalized software time-tracking data supporting Section 15.4, plus standalone statutory-basis procedures required for local filings); component materiality ($9.8 million, based on an allocation of overall group materiality considering the component's relative size and risk); required communications back to the group team (a component reporting package due no later than February 20, 2026); and specific areas requiring group-team involvement (any identified fraud risk indicators, any proposed adjustments exceeding component materiality, and any change in component management's representations regarding capitalization policy compliance).

### Appendix E — Materiality Calculation Worksheet (Summary)

See Section 5 for the full narrative. Supporting calculation: Overall materiality of $36.2 million was derived as the midpoint of a range bounded by 1.4% of forecasted revenue ($33.7 million) and 8.5% of forecasted non-GAAP EBITDA ($37.3 million), cross-checked against 0.72% of total assets ($37.3 million), with the engagement partner exercising judgment to select $36.2 million as an appropriate point within this converging range. Performance materiality of $27.1 million reflects a 75% factor, selected (rather than a higher factor, e.g., 85%) given the moderate-to-elevated aggregation risk factors described in Section 5.2.

### Appendix F — Walkthrough Narratives and Flowcharts (Index)

Full process narratives and flowcharts (Visio-format swimlane diagrams depicting system touchpoints, control activities, and responsible roles) are maintained in the audit file for each process summarized in Section 14: (F-1) Order-to-Cash; (F-2) Procure-to-Pay; (F-3) Payroll and Stock Compensation; (F-4) Financial Statement Close; (F-5) Goodwill Impairment; (F-6) ShieldNex Integration/Consolidation; (F-7) Treasury and Cash Management; (F-8) Equity and Capital Markets Transactions; (F-9) Income Tax Provision.

### Appendix G — Significant Estimates Inventory and Specialist Engagement Letters (Index)

A consolidated inventory of all significant estimates identified in Section 15, including the specific management specialist (e.g., the external valuation firm for the ShieldNex PPA and the PSU Monte Carlo model) relied upon by management for each, our evaluation of that specialist's competence, capabilities, and objectivity under AS 1105.16–.19, and the corresponding engagement letters for our own specialists (valuation, tax) are maintained in the audit file (index AP-750). This inventory will be updated at completion to reflect final conclusions and any differences between our specialists' independently developed ranges and management's recorded amounts.

### Appendix H — Prior-Year Deficiency Remediation Testing Plan

For each of the two fiscal 2024 significant deficiencies (Section 11.6, Section 13.6, items CD-24-01 and CD-24-02), the remediation testing plan specifies: (1) inspection of the redesigned control documentation; (2) a walkthrough of the remediated control; (3) a sample-based operating effectiveness test covering a minimum six-month operating period (April through September 2025 for both items, given remediation completion in Q2 2025); and (4) evaluation of whether the remediation, if operating effectively, is sufficient to conclude the deficiency no longer rises to the level of a significant deficiency as of December 31, 2025, or whether a lesser (deficiency-only) or continued significant classification remains appropriate pending a longer operating history.

---

## SIGN-OFF

This planning memorandum reflects the engagement team's understanding and risk assessment as of the date noted below. This memo will be updated, as necessary, throughout the engagement as new information is obtained, and any significant changes to the risk assessment, materiality, or overall audit strategy will be documented as an amendment to this memo or in a subsequent memorandum, with appropriate re-communication to the audit committee and, where applicable, re-consultation with National Office.

**Prepared by:** J. Alvarez, Senior Manager — Date: December 15, 2025
**Reviewed by:** T. Okafor, Engagement Partner — Date: December 17, 2025
**Concurring Review:** M. Chen, Engagement Quality Reviewer — Date: December 18, 2025

---

*End of Audit Planning Memorandum — Nexora Technologies, Inc., Fiscal Year 2025. This is an entirely fictional illustrative document prepared for training and educational purposes; it does not describe any real company, audit firm, or engagement.*

