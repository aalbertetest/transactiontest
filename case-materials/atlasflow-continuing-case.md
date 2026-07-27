# The AtlasFlow Continuing Case

**Canonical fact pattern for *Auditing Software-as-a-Service Companies: A Practitioner's Textbook*.**

Every chapter of this textbook draws its extended examples, walkthroughs, exercises, and case studies from a
single fictional audit client, **AtlasFlow, Inc.** This file is the authoritative source of facts about
AtlasFlow, its auditor **Brightline LLP**, and the fiscal 2025 integrated audit. Chapter authors must not
contradict the facts recorded here. Where a chapter needs facts that are not recorded here, the chapter may
invent them, provided they are (a) internally consistent, (b) consistent with everything below, and (c)
labeled as an extension in the chapter text (for example, "For purposes of this illustration, assume...").

> **All entities, people, systems configurations, financial figures, and events in this textbook are
> fictional.** Any resemblance to real companies, real audit firms, or real individuals is coincidental.
> Vendor and product names that do exist in the real world (NetSuite, Salesforce, Zuora, AWS, Okta, and so
> on) are used only to make the illustrations recognizable to practitioners; the described configurations,
> control deficiencies, and report contents are invented and should not be taken as statements about those
> products or their actual control environments.

---

## Part 1 — The company

### 1.1 Identity and history

| Attribute | Fact |
| --- | --- |
| Legal name | AtlasFlow, Inc. |
| State of incorporation | Delaware |
| Headquarters | Austin, Texas (leased, 84,000 sq. ft., lease expires 2031) |
| Business | Cloud-based workflow-automation and process-orchestration platform sold to mid-market and enterprise customers |
| Founded | March 2014 |
| IPO | April 2022, NASDAQ Global Select Market, ticker **ATLF** |
| Fiscal year end | December 31 (calendar) |
| Fiscal year under audit | FY2025 (year ended December 31, 2025) |
| Comparative periods in the FY2025 Form 10-K | FY2024 and FY2023 (statements of operations, comprehensive loss, stockholders' equity, cash flows); FY2025 and FY2024 balance sheets |
| Filer status, FY2024 | Accelerated filer; emerging growth company (EGC) |
| Filer status, FY2025 | **Large accelerated filer; no longer an EGC** |
| Employees at 12/31/2025 | 812 (US 604, UK 71, Australia 38, India 99) |
| Auditor | Brightline LLP (PCAOB-registered), engaged since the FY2021 audit |

### 1.2 The single most important fact about FY2025

AtlasFlow's public float measured on **June 30, 2025** (the last business day of its most recently completed
second fiscal quarter) was **$983.6 million**, exceeding the $700 million large-accelerated-filer threshold.
Because AtlasFlow also completed its fifth fiscal year following its April 2022 IPO-registration statement
and its float exceeded $700 million, **AtlasFlow ceased to qualify as an emerging growth company effective
December 31, 2025**.

Consequences that drive much of this textbook:

1. **FY2025 is AtlasFlow's first integrated audit.** Brightline LLP must, for the first time, express an
   opinion on the effectiveness of AtlasFlow's internal control over financial reporting (ICFR) under
   PCAOB AS 2201, in addition to its opinion on the financial statements. In FY2022–FY2024 AtlasFlow was
   exempt from the auditor attestation requirement of Section 404(b) of the Sarbanes-Oxley Act.
2. **Management's first Section 404(a) assessment covering a full control population** must be supported by
   documentation and testing at a depth AtlasFlow has never previously produced.
3. **Critical audit matters (CAMs)** were first communicated in the FY2023 report (large accelerated and
   accelerated filers were subject to CAM reporting from fiscal years ending on or after December 15, 2020;
   AtlasFlow's first CAM year was FY2023 as an accelerated filer).
4. AtlasFlow's remediation runway is short, its accounting staff is thin relative to its transaction volume,
   and its **CFO started in September 2025** — three conditions that materially affect risk assessment.

### 1.3 Products, pricing, and go-to-market

AtlasFlow sells four things:

| Offering | Description | FY2025 revenue |
| --- | --- | --- |
| **AtlasFlow Core** | Multi-tenant SaaS subscription; priced per "automation seat" per month, billed annually in advance; committed annual contract value with an included volume of "workflow runs" | $104.9M |
| **AtlasFlow Insight** | Analytics add-on module; separate SKU, separately priced, can be bought without Core only by existing Core customers | $26.7M |
| **Usage overage** | Workflow runs consumed above the committed volume, billed monthly in arrears at a contractual per-1,000-run rate | $4.2M |
| **Professional services** | Implementation, configuration, data migration, and training; fixed-fee (75% of engagements) or time-and-materials (25%) | $12.4M |
| **Total FY2025 revenue** | | **$148.2M** |

Additional go-to-market facts:

- **Contract terms.** Standard term is 12, 24, or 36 months. Multi-year contracts are typically billed
  annually in advance on each anniversary. Approximately 34% of ACV sits in multi-year contracts with
  contractual escalators or ramps.
- **Self-serve channel.** A credit-card "AtlasFlow Launch" tier processed through Stripe generated $6.1M of
  the Core figure above across roughly 11,400 low-value monthly-billed accounts. Individually immaterial,
  collectively material, and processed through an entirely different system path than enterprise sales.
- **Channel/reseller.** Roughly 9% of ACV is sold through resellers and one global systems integrator.
  Principal-versus-agent analysis is required. See §4.4.
- **Sales incentives.** Commissions are paid on booked ACV, with accelerators above quota. Commissions and
  the associated payroll taxes are capitalized as costs to obtain a contract under ASC 340-40 and amortized
  over an estimated benefit period of **4 years** (initial commissions) or the renewal term (renewal
  commissions, which are not commensurate with initial commissions).
- **Key metrics disclosed outside the financial statements.** ARR, net revenue retention (NRR), dollar-based
  gross retention, customers with ARR > $100K, and remaining performance obligations (RPO). These are
  "other information" for AU-C 720/AS 2710 purposes when included in the Form 10-K and are frequently
  the subject of Item 7 MD&A discussion.

### 1.4 Selected FY2025 financial statement data

All figures in thousands of US dollars unless stated otherwise. These figures are the **final audited**
figures; several chapters work with pre-adjustment figures, and those chapters state so explicitly.

#### Condensed consolidated statements of operations

| Line item | FY2025 | FY2024 | FY2023 |
| --- | --- | --- | --- |
| Subscription revenue | 135,800 | 108,300 | 82,100 |
| Professional services revenue | 12,400 | 10,600 | 9,400 |
| **Total revenue** | **148,200** | **118,900** | **91,500** |
| Cost of subscription revenue | 27,160 | 23,140 | 18,510 |
| Cost of professional services revenue | 11,780 | 10,390 | 9,730 |
| **Total cost of revenue** | **38,940** | **33,530** | **28,240** |
| **Gross profit** | **109,260** | **85,370** | **63,260** |
| Research and development | 43,900 | 36,700 | 29,800 |
| Sales and marketing | 61,300 | 50,900 | 41,200 |
| General and administrative | 26,400 | 19,800 | 15,600 |
| Restructuring | 1,900 | — | — |
| **Total operating expenses** | **133,500** | **107,400** | **86,600** |
| **Loss from operations** | **(24,240)** | **(22,030)** | **(23,340)** |
| Interest income | 5,110 | 4,240 | 1,980 |
| Interest expense | (1,340) | (520) | (60) |
| Other income (expense), net | (390) | 210 | (140) |
| **Loss before income taxes** | **(20,860)** | **(18,100)** | **(21,560)** |
| Provision for income taxes | (540) | (410) | (300) |
| **Net loss** | **(21,400)** | **(18,510)** | **(21,860)** |
| Net loss per share, basic and diluted | $(0.42) | $(0.38) | $(0.47) |
| Weighted-average shares, basic and diluted (000s) | 50,952 | 48,711 | 46,510 |

Note: Subscription revenue of $135,800 comprises Core $104,900 + Insight $26,700 + usage overage $4,200.

#### Condensed consolidated balance sheets

| Line item | 12/31/2025 | 12/31/2024 |
| --- | --- | --- |
| Cash and cash equivalents | 96,400 | 88,700 |
| Short-term investments | 54,200 | 41,300 |
| Accounts receivable, net of allowance of $1,900 and $1,350 | 36,700 | 29,150 |
| Unbilled receivables / contract assets, current | 3,400 | 2,100 |
| Deferred contract acquisition costs, current | 9,800 | 7,900 |
| Prepaid expenses and other current assets | 8,100 | 6,400 |
| **Total current assets** | **208,600** | **175,550** |
| Property and equipment, net | 14,300 | 12,900 |
| Operating lease right-of-use assets | 21,700 | 24,600 |
| Capitalized internal-use software, net | 18,600 | 13,400 |
| Deferred contract acquisition costs, noncurrent | 14,200 | 11,600 |
| Goodwill | 26,900 | 12,400 |
| Intangible assets, net | 9,700 | 3,100 |
| Other assets | 3,900 | 3,300 |
| **Total assets** | **317,900** | **256,850** |
| Accounts payable | 7,600 | 6,100 |
| Accrued compensation and benefits | 16,400 | 13,200 |
| Accrued expenses and other current liabilities | 11,900 | 9,700 |
| Operating lease liabilities, current | 3,600 | 3,300 |
| Deferred revenue, current | 71,300 | 56,900 |
| **Total current liabilities** | **110,800** | **89,200** |
| Deferred revenue, noncurrent | 6,900 | 5,400 |
| Convertible senior notes, net | 170,600 | 169,900 |
| Operating lease liabilities, noncurrent | 19,800 | 22,600 |
| Other long-term liabilities | 2,700 | 2,100 |
| **Total liabilities** | **310,800** | **289,200** |
| Common stock, $0.0001 par; 500,000 authorized; 51,842 and 49,610 issued and outstanding | 5 | 5 |
| Additional paid-in capital | 412,300 | 351,600 |
| Accumulated other comprehensive loss | (1,105) | (1,455) |
| Accumulated deficit | (404,100) | (382,700) |
| **Total stockholders' equity** | **7,100** | **(32,550)** |
| **Total liabilities and stockholders' equity** | **317,900** | **256,850** |

#### Selected cash flow data, FY2025

| Line item | FY2025 |
| --- | --- |
| Net loss | (21,400) |
| Stock-based compensation | 28,700 |
| Depreciation and amortization | 11,900 |
| Amortization of deferred contract acquisition costs | 8,600 |
| Amortization of debt discount and issuance costs | 700 |
| Provision for credit losses | 1,780 |
| Changes in operating assets and liabilities (net) | 4,120 |
| **Net cash provided by operating activities** | **34,400** |
| Net cash used in investing activities | (37,900) |
| Net cash provided by financing activities | 11,300 |
| Effect of exchange rates | (100) |
| **Net increase in cash** | **7,700** |

#### Other key balances and metrics

| Item | 12/31/2025 | 12/31/2024 |
| --- | --- | --- |
| Annual recurring revenue (ARR) | $172.0M | $137.4M |
| Remaining performance obligations (RPO) | $214.0M | $168.5M |
| RPO expected to be recognized within 12 months | $138.9M (64.9%) | $110.1M |
| Net revenue retention (NRR) | 112% | 118% |
| Dollar-based gross retention | 91% | 93% |
| Customers with ARR ≥ $100K | 604 | 471 |
| Total enterprise/mid-market customers | 3,140 | 2,690 |
| Self-serve accounts | 11,400 | 8,900 |
| Stock-based compensation expense | $28.7M | $22.9M |
| Days sales outstanding (DSO), Q4 average | 68 days | 61 days |

### 1.5 Legal entity structure and FY2025 group audit facts

| Entity | Role | FY2025 revenue | FY2025 total assets | Auditor |
| --- | --- | --- | --- | --- |
| AtlasFlow, Inc. (US) | Parent, contracting entity for Americas | $109,400 | $271,100 | Brightline LLP (Austin) — group engagement team |
| AtlasFlow Software Ltd (UK) | EMEA sales and contracting entity | $26,300 | $31,600 | Brightline UK LLP (component auditor, London) |
| AtlasFlow Pty Ltd (Australia) | APAC sales and contracting entity | $12,500 | $12,900 | Group team performs specified procedures; not a full-scope component |
| AtlasFlow India Private Limited | Cost-plus R&D and support center; no external revenue | — | $2,300 | Group team performs analytical procedures only |
| Kestrel Labs, Inc. | Acquired August 4, 2025; merged into parent; no separate reporting | included above | included above | n/a |

Group audit notes: intercompany balances are eliminated in a consolidation workbook maintained in Excel
outside NetSuite (a known risk); the UK entity uses GBP as its functional currency, Australia uses AUD, and
India uses INR.

### 1.6 The Kestrel Labs acquisition (August 4, 2025)

Purchase price: $19,400 total consideration — $16,900 cash at closing, plus $2,500 fair value of contingent
consideration (an earn-out payable in Q1 2027 if a retention-and-revenue milestone is met, maximum payout
$4,000). Preliminary purchase price allocation:

| Component | Amount |
| --- | --- |
| Developed technology intangible (5-year life) | 6,900 |
| Customer relationships intangible (7-year life) | 1,100 |
| Net working capital acquired | 200 |
| Deferred tax liability | (1,300) |
| **Goodwill** | **14,500** |
| **Total** | **19,400** |

Kestrel had 22 employees, an unaudited historical financial statement set prepared on a modified cash basis,
no formal revenue recognition policy, and a homegrown billing spreadsheet. Kestrel's customer contracts
(annual recurring revenue of approximately $2,100) were migrated into Zuora in October 2025, and $340 of
Kestrel revenue was recognized in the AtlasFlow consolidated statements for the post-acquisition period.
**Management has scoped Kestrel out of its FY2025 Section 404(a) assessment**, relying on the SEC staff's
long-standing guidance permitting exclusion of a recently acquired business, and has disclosed the exclusion.
Whether that exclusion is appropriately supported, scoped, and disclosed is a recurring exercise in this
textbook.

### 1.7 The convertible notes (September 2024)

$175,000 aggregate principal, 0.25% cash coupon payable semi-annually, due September 15, 2029, initial
conversion price $48.20 per share (conversion rate 20.7469 shares per $1,000 principal), issued at par with
$5,400 of issuance costs. Accounted for as a single liability instrument under ASU 2020-06 (no separation of
a conversion feature; no beneficial conversion feature); issuance costs amortized to interest expense using
the effective interest method over five years. AtlasFlow also entered into **capped calls** costing $14,700,
recorded as a reduction of additional paid-in capital. The if-converted shares (3,631 thousand) are excluded
from diluted EPS because AtlasFlow reported a net loss for all periods presented.

### 1.8 FY2025 events, in chronological order

| Date | Event | Chapters most affected |
| --- | --- | --- |
| Jan 2025 | New "AtlasFlow Insight" SKU launched; standalone selling price (SSP) evidence for a new SKU is thin | 5, 4 |
| Feb 2025 | Zuora Revenue (RevPro) configuration change to accommodate ramped contracts; change deployed with abbreviated UAT | 11, 12, 6 |
| Mar 2025 | VP Revenue Accounting Daniel Kim placed on a performance plan; two revenue accountants resigned in Q2 | 1, 2, 17 |
| Apr 2025 | Annual pricing update; list price of Core raised 8%; existing customers grandfathered for one renewal cycle | 5, 4 |
| Jun 30, 2025 | Public float measurement date: $983.6M → large accelerated filer, EGC status lost at year end | 1, 11, 20 |
| Jul 2025 | Internal audit (co-sourced with a third-party provider) issues first ITGC readiness assessment; identifies 14 gaps | 11, 12, 14 |
| Aug 4, 2025 | Kestrel Labs acquisition closes | 1, 2, 19 |
| Sep 2025 | CFO Tom Okafor joins, replacing the founding CFO who resigned in July 2025 | 1, 2, 17 |
| Sep 2025 | NetSuite upgraded to a new release; segregation-of-duties roles rebuilt during the upgrade | 11, 14 |
| Oct 2025 | Restructuring: 41 positions eliminated, $1,900 charge; Australia office consolidated | 10, 19 |
| Nov 2025 | Snowflake-based "RevOps datamart" becomes the source for ARR and NRR metrics reported in MD&A; no formal reconciliation to the general ledger initially | 12, 18, 20 |
| Dec 2025 | Q4 closes with record bookings; 41% of Q4 ACV signed in the final 5 business days | 4, 5, 17, 18 |
| Dec 31, 2025 | Fiscal year end | all |
| Jan 2026 | Whistleblower email to the audit committee alleging that "December deals were papered after the fact" | 17, 19 |
| Feb 9, 2026 | Largest customer, Meridian Health Systems, notifies AtlasFlow of a dispute over a $1,240 professional services invoice | 7, 19 |
| Feb 20, 2026 | Planned report date / filing of Form 10-K | 19, 20 |

---

## Part 2 — Systems and IT environment

### 2.1 Application landscape

| # | System | Function | Hosting | Financially relevant? | Notes for auditors |
| --- | --- | --- | --- | --- | --- |
| 1 | **Salesforce Sales Cloud + CPQ** | Opportunity, quote, approval, order form generation, contract repository | Vendor SaaS | Yes — initiation and authorization of revenue transactions | Approval matrix configured in CPQ; discount thresholds; "Closed Won" triggers order-to-cash |
| 2 | **Zuora Billing** | Subscription catalog, subscription records, invoicing, amendments, credit memos | Vendor SaaS | Yes — billing completeness/accuracy | SOC 1 Type 2 available; period covered Oct 1, 2024 – Sep 30, 2025 |
| 3 | **Zuora Revenue (RevPro)** | ASC 606 engine: performance obligation identification, SSP allocation, revenue schedules, contract modifications | Vendor SaaS | Yes — the revenue subledger | Configuration is the key control; 27 configuration rules; changed in Feb 2025 |
| 4 | **NetSuite (Oracle)** | General ledger, AP, fixed assets, consolidation posting, financial reporting | Vendor SaaS | Yes — the GL of record | Upgraded Sep 2025; SoD roles rebuilt |
| 5 | **Stripe** | Self-serve credit-card billing and collection | Vendor SaaS | Yes — $6.1M of revenue, 11,400 accounts | Feeds a summarized daily journal entry to NetSuite |
| 6 | **Coupa** | Procurement, purchase orders, invoice matching, expense approvals | Vendor SaaS | Yes — expenditure cycle | Three-way match configuration |
| 7 | **SAP Concur** | Travel and entertainment expense, corporate card | Vendor SaaS | Yes — T&E expense | Policy limits, receipt thresholds, manager approval |
| 8 | **ADP Workforce Now** | US payroll | Vendor SaaS | Yes — payroll expense | SOC 1 Type 2 |
| 9 | **Deel** | UK, Australia, India payroll and contractor payments | Vendor SaaS | Yes | Bridge letter needed |
| 10 | **Carta** | Equity administration: options, RSUs, ESPP, cap table | Vendor SaaS | Yes — equity and SBC | Grant data feeds the SBC calculation |
| 11 | **FloQast** | Close checklist, reconciliation sign-off, journal entry support repository | Vendor SaaS | Yes — the close process control evidence | Sign-off dates are audit evidence for the close controls |
| 12 | **Avalara** | Sales/use and VAT tax determination | Vendor SaaS | Indirectly | Tax accrual completeness |
| 13 | **Snowflake** | Data warehouse; RevOps datamart; ARR/NRR/RPO metric computation; source of most audit data extracts | AWS-hosted | Yes — reporting and IUC | Access to Snowflake is broader than access to source systems |
| 14 | **AWS** | Production hosting of the AtlasFlow platform (us-east-1, eu-west-1) | AWS | Indirectly (service availability, SLA credits, capitalized software) | SOC 1/SOC 2 reports; CUECs |
| 15 | **Okta** | Single sign-on and MFA for items 1–13 | Vendor SaaS | Yes — the access control chokepoint | Not all applications are federated; Zuora Revenue has 4 local admin accounts |
| 16 | **GitHub + CircleCI + Terraform** | Source control, CI/CD, infrastructure as code for the platform and for integration jobs | Vendor SaaS / AWS | Yes — change management | Approx. 3,100 production deployments in FY2025 |
| 17 | **Jira** | Change tickets, incident tickets, and access-request workflow | Vendor SaaS | Yes — change and access evidence | Ticket quality is uneven |
| 18 | **Vanta** | Continuous compliance monitoring, evidence collection | Vendor SaaS | Evidence source only | Management sometimes offers Vanta screenshots as control evidence |
| 19 | **First Meridian Bank / JPMorgan** | Operating, payroll, and investment accounts; positive pay | Bank portals | Yes — cash | See §3.4 |
| 20 | **Consolidation workbook ("CONSOL_FY25_v14.xlsx")** | FX translation, intercompany elimination, top-side entries | Local Excel on SharePoint | Yes — a spreadsheet in the financial reporting chain | End-user computing control weakness |

### 2.2 Key integrations and interfaces

| Interface | From → To | Frequency | Mechanism | Control |
| --- | --- | --- | --- | --- |
| I-1 | Salesforce CPQ → Zuora Billing | Real time on order activation | API (Zuora CPQ connector) | Automated field mapping; error queue reviewed daily by Billing Analyst |
| I-2 | Zuora Billing → Zuora Revenue | Nightly batch, 02:00 CT | Native connector | Record-count and amount reconciliation report; exceptions worked by Revenue Manager |
| I-3 | Zuora Revenue → NetSuite | Monthly summary journal | Scheduled integration, posts to accounts 4100/4110/4120/2400/2410 | Journal is reviewed and approved by the Controller before posting; interface totals tie to the RevPro "Revenue Contract Summary" |
| I-4 | Stripe → NetSuite | Daily summary journal | Custom AWS Lambda job (in-house code) | Daily cash-to-revenue reconciliation; failure alerting via PagerDuty |
| I-5 | ADP / Deel → NetSuite | Semi-monthly / monthly | CSV import with template | Payroll register-to-GL reconciliation |
| I-6 | Carta → SBC calculation workbook | Monthly export | Manual CSV download | Roll-forward of grants; manual, high-judgment |
| I-7 | Coupa → NetSuite | Nightly | API | PO/invoice/receipt three-way match |
| I-8 | NetSuite, Zuora, Salesforce → Snowflake | Hourly via Fivetran | Managed ELT | No formal reconciliation of Snowflake to source until December 2025 |
| I-9 | Bank → NetSuite | Daily | Bank feed | Automated matching; unmatched items cleared by Staff Accountant |

### 2.3 Chart of accounts extract (accounts referenced throughout the textbook)

| Account | Description | 12/31/2025 balance (000s) |
| --- | --- | --- |
| 1010 | Cash — First Meridian operating (USD) | 41,300 |
| 1015 | Cash — First Meridian payroll (USD) | 3,900 |
| 1020 | Cash — JPMorgan concentration (USD) | 38,100 |
| 1030 | Cash — Barclays (GBP), UK entity | 7,600 |
| 1035 | Cash — NAB (AUD), AU entity | 3,200 |
| 1040 | Cash — HDFC (INR), India entity | 1,100 |
| 1045 | Money market funds (classified as cash equivalents) | 1,200 |
| 1100 | Short-term investments — US Treasury bills | 31,400 |
| 1110 | Short-term investments — commercial paper and corporate notes | 22,800 |
| 1200 | Accounts receivable — trade (enterprise) | 36,900 |
| 1205 | Accounts receivable — Stripe self-serve | 1,700 |
| 1210 | Allowance for credit losses | (1,900) |
| 1220 | Unbilled receivables / contract assets | 3,400 |
| 1300 | Deferred contract acquisition costs — current | 9,800 |
| 1305 | Deferred contract acquisition costs — noncurrent | 14,200 |
| 1400 | Prepaid expenses | 6,300 |
| 1410 | Other current assets | 1,800 |
| 1500 | Property and equipment, gross | 26,700 |
| 1510 | Accumulated depreciation | (12,400) |
| 1560 | Capitalized internal-use software, gross | 31,200 |
| 1565 | Accumulated amortization — internal-use software | (12,600) |
| 1600 | Operating lease right-of-use assets | 21,700 |
| 1700 | Goodwill | 26,900 |
| 1710 | Intangible assets, gross | 12,900 |
| 1715 | Accumulated amortization — intangibles | (3,200) |
| 2000 | Accounts payable | 7,600 |
| 2100 | Accrued compensation — salaries and bonus | 9,100 |
| 2105 | Accrued commissions | 4,800 |
| 2110 | Accrued paid time off | 2,500 |
| 2200 | Accrued expenses — other | 6,400 |
| 2210 | Accrued sales and use / VAT | 2,900 |
| 2220 | Accrued professional fees | 1,400 |
| 2230 | Customer credits and refunds payable | 1,200 |
| 2300 | Operating lease liabilities — current | 3,600 |
| 2305 | Operating lease liabilities — noncurrent | 19,800 |
| 2400 | Deferred revenue — subscription, current | 66,800 |
| 2405 | Deferred revenue — professional services, current | 4,500 |
| 2410 | Deferred revenue — noncurrent | 6,900 |
| 2500 | Convertible senior notes, net of unamortized issuance costs | 170,600 |
| 2600 | Contingent consideration — Kestrel earn-out | 2,500 |
| 3000 | Common stock | 5 |
| 3100 | Additional paid-in capital | 412,300 |
| 3200 | Accumulated other comprehensive loss | (1,105) |
| 3300 | Accumulated deficit | (404,100) |
| 4100 | Subscription revenue — Core | 104,900 |
| 4110 | Subscription revenue — Insight | 26,700 |
| 4120 | Usage overage revenue | 4,200 |
| 4200 | Professional services revenue — fixed fee | 9,300 |
| 4210 | Professional services revenue — time and materials | 3,100 |
| 4900 | Sales returns, credits, and SLA credits (contra) | (1,900) note: netted within 4100–4120 above |
| 5100 | Cost of subscription — hosting | 13,400 |
| 5110 | Cost of subscription — personnel (support, DevOps) | 9,200 |
| 5120 | Cost of subscription — amortization of capitalized software and developed technology | 4,560 |
| 5200 | Cost of professional services | 11,780 |
| 6100 | Research and development | 43,900 |
| 6200 | Sales and marketing | 61,300 |
| 6210 | Amortization of deferred contract acquisition costs (within 6200) | 8,600 |
| 6300 | General and administrative | 26,400 |
| 6400 | Restructuring | 1,900 |
| 7100 | Interest income | (5,110) |
| 7200 | Interest expense | 1,340 |
| 7300 | Other income (expense), net | 390 |
| 8000 | Provision for income taxes | 540 |

### 2.4 Known IT and control weaknesses identified before or during the FY2025 audit

These are the raw material for Chapters 11–14 and 19. Not all rise to the level of a material weakness; part
of the exercise is evaluating severity.

| Ref | Observation | First identified |
| --- | --- | --- |
| W-1 | Four local (non-Okta-federated) administrator accounts in Zuora Revenue, one of which is a shared "revpro_admin" account with the password stored in a shared vault entry accessible to six people | IA readiness assessment, July 2025 |
| W-2 | During the September 2025 NetSuite upgrade, 11 users retained the legacy "Full Access" role for 27 days after go-live | Auditor testing, November 2025 |
| W-3 | User access reviews for Salesforce, Zuora, and NetSuite were performed annually rather than the quarterly frequency described in management's control documentation; the Q2 2025 review was completed 41 days late | IA readiness assessment |
| W-4 | 6 of 3,100 production deployments in FY2025 were "emergency" changes deployed without a Jira ticket; documentation was created after the fact for 4 of them and never for 2 | Auditor testing |
| W-5 | Terminated-user access removal averaged 6.2 days against a documented 24-hour SLA; 3 terminated employees retained Salesforce access for more than 30 days | Auditor testing |
| W-6 | Two developers have standing write access to the production Zuora Revenue configuration | IA readiness assessment |
| W-7 | The Stripe-to-NetSuite Lambda job (I-4) is in-house code with no documented change approval for two FY2025 modifications | Auditor testing |
| W-8 | The consolidation workbook has no version control, no formula-integrity check, and is emailed among four people | Auditor testing |
| W-9 | Bridge letters were not obtained for Zuora and Deel for the October 1 – December 31, 2025 gap period | Auditor testing |
| W-10 | Complementary user entity controls (CUECs) listed in the AWS and Zuora SOC 1 reports were not mapped to AtlasFlow controls | IA readiness assessment |
| W-11 | The RevOps datamart in Snowflake, used to produce ARR and NRR for MD&A, was not reconciled to the GL for the first three quarters of FY2025 | Auditor testing |
| W-12 | Journal entry approval in NetSuite is configured to require a second approver only above $250,000; 3,847 of 4,912 manual entries in FY2025 were below the threshold and had no evidence of independent review | Auditor testing |
| W-13 | The Controller has the ability to both prepare and post journal entries and to modify the RevPro-to-NetSuite interface mapping | IA readiness assessment |
| W-14 | Backup restoration testing was performed once in FY2025 and failed; the retest was not completed until January 2026 | IA readiness assessment |

### 2.5 Service organization reports on hand

| Provider | Report type | Period covered | Opinion | Deviations noted |
| --- | --- | --- | --- | --- |
| Zuora (Billing and Revenue) | SOC 1 Type 2 | Oct 1, 2024 – Sep 30, 2025 | Unqualified | 1 deviation: 2 of 25 change tickets lacked evidence of approval |
| Oracle NetSuite | SOC 1 Type 2 | Nov 1, 2024 – Oct 31, 2025 | Unqualified | None |
| AWS | SOC 1 Type 2 | Oct 1, 2024 – Sep 30, 2025 | Unqualified | None |
| ADP | SOC 1 Type 2 | Jan 1, 2025 – Sep 30, 2025 | Unqualified | None |
| Deel | SOC 1 Type 2 | Oct 1, 2024 – Sep 30, 2025 | Qualified as to one control objective related to change management | 1 qualification |
| Carta | SOC 1 Type 2 | Oct 1, 2024 – Sep 30, 2025 | Unqualified | None |
| Stripe | SOC 1 Type 2 | Jan 1, 2025 – Dec 31, 2025 | Unqualified | None |
| Coupa | SOC 1 Type 2 | Jul 1, 2024 – Jun 30, 2025 | Unqualified | 2 deviations in access recertification |

---

## Part 3 — Selected detailed account data

### 3.1 Revenue by quarter and by stream (FY2025, 000s)

| Stream | Q1 | Q2 | Q3 | Q4 | FY |
| --- | --- | --- | --- | --- | --- |
| Core subscription | 24,100 | 25,700 | 26,900 | 28,200 | 104,900 |
| Insight subscription | 5,400 | 6,300 | 7,200 | 7,800 | 26,700 |
| Usage overage | 780 | 940 | 1,090 | 1,390 | 4,200 |
| Professional services | 2,700 | 3,100 | 3,200 | 3,400 | 12,400 |
| **Total** | **32,980** | **36,040** | **38,390** | **40,790** | **148,200** |

Q4 bookings (new and expansion ACV signed): $61,400, of which **$25,174 (41%)** was signed December 24–31,
2025. Q4 FY2024 comparative: $46,900, of which 27% was signed in the final five business days.

### 3.2 Deferred revenue roll-forward, FY2025 (000s)

| Component | Amount |
| --- | --- |
| Deferred revenue, January 1, 2025 (current + noncurrent) | 62,300 |
| Billings (invoiced amounts, net of credits) | 163,750 |
| Revenue recognized from beginning balance | (54,900) |
| Revenue recognized from current-period billings | (93,300) |
| Deferred revenue acquired in Kestrel acquisition | 610 |
| Foreign currency translation | (260) |
| **Deferred revenue, December 31, 2025** | **78,200** |
| Of which: current | 71,300 |
| Of which: noncurrent | 6,900 |

### 3.3 Accounts receivable aging at December 31, 2025 (000s)

| Bucket | Enterprise AR | Self-serve AR | Total | % of total | Historical loss rate applied |
| --- | --- | --- | --- | --- | --- |
| Current (not yet due) | 21,400 | 1,150 | 22,550 | 58.4% | 0.4% |
| 1–30 days past due | 7,900 | 290 | 8,190 | 21.2% | 1.6% |
| 31–60 days past due | 3,600 | 140 | 3,740 | 9.7% | 6.0% |
| 61–90 days past due | 1,900 | 70 | 1,970 | 5.1% | 18.0% |
| 91–180 days past due | 1,400 | 40 | 1,440 | 3.7% | 42.0% |
| Over 180 days past due | 700 | 10 | 710 | 1.8% | 85.0% |
| **Gross AR** | **36,900** | **1,700** | **38,600** | **100.0%** | |
| Allowance for credit losses | | | (1,900) | | |
| **Net AR** | | | **36,700** | | |

Ten largest customer balances at December 31, 2025 (enterprise):

| # | Customer | Balance | Notes |
| --- | --- | --- | --- |
| 1 | Meridian Health Systems | 2,410 | Includes the disputed $1,240 PS invoice (see §1.8, Feb 9, 2026) |
| 2 | Voltaire Logistics S.A. | 1,880 | Multi-element renewal with a material right |
| 3 | Northgate Financial Group | 1,640 | SLA credit claim of $180 pending at year end |
| 4 | Cirrus Retail Group | 1,510 | Sold through reseller Tessera Partners |
| 5 | Pemberton Manufacturing Co. | 1,290 | Contract has a 30-day termination-for-convenience clause |
| 6 | Halloran Energy | 1,120 | Paid February 3, 2026 |
| 7 | Sundown Media Holdings | 980 | 94 days past due; in collections |
| 8 | BlueRidge Insurance | 870 | — |
| 9 | Calderon Foods | 790 | — |
| 10 | Aeropath Group | 740 | Sold through global systems integrator |
| | **Top 10 total** | **13,230** | 35.9% of enterprise AR |

### 3.4 Cash and treasury detail at December 31, 2025

| Account | Bank | Currency | Book balance (USD 000s) | Bank balance (USD 000s) | Reconciling items |
| --- | --- | --- | --- | --- | --- |
| 1010 Operating | First Meridian | USD | 41,300 | 42,890 | Outstanding checks $1,410; deposits in transit $0; bank fee not recorded $180 (see below) |
| 1015 Payroll | First Meridian | USD | 3,900 | 4,120 | Outstanding payroll checks $220 |
| 1020 Concentration | JPMorgan | USD | 38,100 | 38,100 | None |
| 1030 UK operating | Barclays | GBP | 7,600 | 7,600 | Translated at 1.2680 USD/GBP |
| 1035 AU operating | NAB | AUD | 3,200 | 3,200 | Translated at 0.6410 USD/AUD |
| 1040 India operating | HDFC | INR | 1,100 | 1,100 | Translated at 0.01172 USD/INR |
| 1045 Money market | JPMorgan | USD | 1,200 | 1,200 | Sweep account |
| **Total cash and equivalents** | | | **96,400** | | |

Treasury facts: an investment policy approved by the board limits investments to US Treasuries, agency
paper, A-1/P-1 commercial paper, and money market funds, with a maximum weighted-average maturity of 12
months and a maximum single-issuer concentration of 5%. At December 31, 2025 one commercial paper position
(Harborview Capital, $3,100) represents 5.7% of the short-term investment portfolio — a policy exception that
was not escalated. AtlasFlow has a $50,000 revolving credit facility with First Meridian, undrawn at year
end, containing a minimum-liquidity covenant of $40,000 and a maximum-net-leverage covenant that is not
currently applicable. Positive pay is enabled on account 1010 but not on 1015.

### 3.5 Equity detail

Share activity, FY2025 (thousands of shares):

| Activity | Shares |
| --- | --- |
| Outstanding, January 1, 2025 | 49,610 |
| Option exercises | 610 |
| RSU vesting, net of shares withheld for taxes | 1,489 |
| ESPP issuances (two purchase dates: June 30 and December 31) | 133 |
| **Outstanding, December 31, 2025** | **51,842** |

Equity awards outstanding at December 31, 2025:

| Award type | Units (000s) | Weighted-average exercise price / grant-date fair value | Unrecognized cost (000s) | Weighted-average remaining period |
| --- | --- | --- | --- | --- |
| Stock options | 2,140 | $18.40 exercise price | 6,900 | 1.8 years |
| Time-based RSUs | 4,320 | $31.70 grant-date fair value | 41,300 | 2.4 years |
| Performance RSUs (PSUs) — ARR-based, 2 tranches | 480 | $34.10 | 8,200 | 1.6 years |
| Market-condition PSUs (TSR-based, Monte Carlo valued) | 210 | $39.60 | 4,100 | 2.1 years |
| ESPP | n/a (6-month look-back, 15% discount) | n/a | 900 | 0.5 years |

FY2025 stock-based compensation expense of $28,700 by line: cost of revenue $2,100; R&D $11,400; sales and
marketing $7,600; G&A $7,600. Forfeitures are accounted for as they occur. The ARR-based PSU tranche for
2025 was assessed as 100% probable in Q3 2025 and the estimate was revised to 85% in Q4 2025, producing a
$1,340 catch-up credit — a judgment the audit team must evaluate.

### 3.6 Journal entry population, FY2025

| Category | Count | Absolute value posted (000s) |
| --- | --- | --- |
| Total journal entries posted to NetSuite | 41,610 | 1,842,300 |
| Automated / interface-generated | 36,698 | 1,701,400 |
| Manual entries | 4,912 | 140,900 |
| Manual entries posted by users with SoD conflicts | 214 | 18,600 |
| Manual entries posted after the close cut-off (post-close adjustments) | 61 | 9,400 |
| Manual entries with blank or single-word descriptions | 388 | 12,100 |
| Manual entries posted on weekends or after 8:00 p.m. local | 172 | 7,300 |
| Manual entries with round-dollar amounts ≥ $100,000 | 96 | 21,400 |
| Manual entries hitting both revenue and a non-standard offset account | 34 | 3,900 |
| Manual top-side entries in the consolidation workbook (outside NetSuite) | 27 | 6,200 |

### 3.7 The five specific contracts used repeatedly in worked examples

| Contract | Facts |
| --- | --- |
| **C-1 Meridian Health Systems** | Signed March 12, 2025. 36-month term, March 15, 2025 – March 14, 2028. Core subscription with an annual ramp: Year 1 $600, Year 2 $840, Year 3 $960 (total $2,400). Insight add-on $180 per year for years 2 and 3 only. Fixed-fee implementation $360, delivered April–July 2025. Billed annually in advance on each anniversary; implementation billed 50% on signature and 50% on go-live. Includes 200,000 workflow runs per year; overage at $12 per 1,000 runs. Meridian consumed 244,000 runs in the first contract year. |
| **C-2 Voltaire Logistics S.A.** | Renewal signed October 1, 2025 for 24 months. Total fixed fee $1,600. Includes a "renewal credit" of $200 usable only toward a future Insight purchase — a material right. Contracted in EUR (€1,480) through the UK entity; functional currency GBP; reporting currency USD. |
| **C-3 Northgate Financial Group** | 12-month term beginning July 1, 2025, $1,920 fixed. Contains an uptime SLA of 99.9% with a graduated service-credit schedule (10% of monthly fee for 99.0–99.9%, 25% below 99.0%). Two incidents in FY2025 (August and November) triggered credit eligibility; Northgate claimed $180 in December 2025, and AtlasFlow recorded nothing pending "commercial discussions." |
| **C-4 Cirrus Retail Group / Tessera Partners (reseller)** | Tessera resells AtlasFlow to Cirrus. Tessera sets the end-customer price, takes credit risk, and holds the contract with Cirrus; AtlasFlow's order form is with Tessera at a 28% discount to list. Tessera also performs the implementation. Principal-versus-agent and gross-versus-net questions. |
| **C-5 Pemberton Manufacturing Co.** | 24-month term beginning September 1, 2025, $1,440 total, billed annually in advance, with a clause allowing Pemberton to terminate for convenience with 30 days' notice and no penalty. Contract-term determination under ASC 606 (enforceable rights and obligations) drives the transaction price, the RPO disclosure, and the amortization period for the related $86 commission. |

---

## Part 4 — Accounting policies and known judgment areas

### 4.1 Revenue recognition policy summary

- Core and Insight subscriptions: a series of distinct daily services constituting a single performance
  obligation satisfied ratably over the subscription term; revenue recognized straight-line from the later
  of contract start date and provisioning date.
- Usage overage: recognized in the month the runs are consumed, as a variable-consideration allocation
  exception ("right to invoice" / ASC 606-10-55-18 practical expedient where applicable) or as usage-based
  royalty-like consideration allocated to the distinct daily service to which it relates.
- Professional services: fixed-fee engagements recognized over time using an input measure (hours incurred
  as a percentage of estimated total hours); T&M recognized as hours are delivered.
- SSP: established by observable standalone sales where sufficient population exists (Core), and by the
  "expected cost plus a margin" and adjusted-market-assessment approaches for Insight, which launched in
  January 2025 and had only 31 standalone sales during FY2025 across a wide price band (interquartile range
  of 22% of list).
- Discounts are allocated proportionately to all performance obligations unless the "allocation of a discount
  to one or more but not all performance obligations" criteria in ASC 606-10-32-37 are met.
- Contract modifications: renewals at SSP are treated as separate contracts; mid-term upsells that add
  distinct services at SSP are prospective; ramp restructurings and mid-term price concessions are
  cumulative-catch-up modifications.

### 4.2 Costs to obtain a contract (ASC 340-40)

Commissions on new business are amortized over 4 years (the estimated period of benefit, supported by an
analysis of average customer life of 4.3 years and a technology-refresh cycle assessment). Renewal
commissions average 3.1% of ACV versus 11.8% on new business, so renewal commissions are not commensurate,
and the 4-year initial-commission period is retained rather than being limited to the contract term.
Sales-manager overrides and the employer portion of payroll taxes on commissions are capitalized;
non-incremental costs such as base salary and sales-engineer time are not. A $1,900 balance of capitalized
costs relates to customers whose contracts were not renewed as of year end, raising an impairment question.

### 4.3 Internal-use software capitalization

$31,200 gross capitalized cost, $10,900 of which was capitalized in FY2025. Capitalization begins at the end
of the preliminary project stage and stops at substantial completion. Support for FY2025 comes from Jira
time-tracking data allocated by project stage; 22% of the capitalized hours were coded to Jira epics whose
stage designation was changed retroactively during the year, and the developer time reports are approved by
the same engineering managers who own the projects' budgets.

### 4.4 Principal versus agent

For reseller arrangements (C-4 and 41 similar contracts totaling $9,700 of FY2025 revenue), management
concluded AtlasFlow is the principal for the subscription (it controls the SaaS service before transfer and
has discretion over price to the reseller) and records revenue net of the reseller discount, treating the
discount as a reduction of the transaction price rather than as a cost. For the two arrangements where the
reseller performs implementation using its own resources and contracts separately with the end customer for
those services, AtlasFlow records no professional services revenue.

### 4.5 The five most judgmental FY2025 estimates

1. SSP for the Insight module (affects allocation across nearly every 2025 multi-element contract).
2. Allowance for credit losses under CECL, including the reasonable-and-supportable forecast overlay.
3. The 4-year amortization period for capitalized commissions.
4. Probability assessment and expense attribution for the ARR-based PSUs, including the Q4 revision to 85%.
5. Fair value of the Kestrel contingent consideration ($2,500), which uses a Monte Carlo simulation with an
   assumed revenue volatility of 32% and a risk-adjusted discount rate of 11.5%.

---

## Part 5 — People

### 5.1 AtlasFlow

| Name | Role | Notes relevant to the audit |
| --- | --- | --- |
| Priya Raghunathan | Co-founder and CEO | Compensation heavily weighted to PSUs tied to ARR |
| Tom Okafor | Chief Financial Officer (since September 2025) | Previously CFO of a private company one-fifth the size; first public-company CFO role |
| Elena Vasquez | Chief Accounting Officer and Controller | 14 years' experience; the single point of failure in the close |
| Daniel Kim | VP, Revenue Accounting | On a performance plan since March 2025; owns the RevPro configuration |
| Aisha Bello | Director, Technical Accounting | Author of the SSP and ASC 340-40 memos |
| Jordan Pike | Revenue Manager | Performs the RevPro-to-GL reconciliation and clears interface exceptions |
| Brett Hallowell | VP, Sales Operations | Administers Salesforce CPQ; has the ability to modify order-form dates; central to the Chapter 17 fraud scenario |
| Sofia Marchetti | Chief Revenue Officer | Compensated on bookings; sets Q4 "close the quarter" incentives |
| Vikram Shah | Chief Technology Officer | Sponsor of the capitalized-software program |
| Ray Sandoval | Director, IT and Information Security | Owns Okta, access provisioning, and the ITGC control set |
| Nate Oyelaran | Treasury Manager | Sole administrator on two bank portals |
| Michelle Fong | Head of Internal Audit (co-sourced with an outside provider) | Reports to the audit committee; issued the July 2025 readiness assessment |
| Dr. Helen Ashford | Audit committee chair, designated financial expert | Former public-company CFO |
| Raymond Ito, Sandra Klopfer | Other audit committee members | |

### 5.2 Brightline LLP engagement team

| Name | Role | Notes |
| --- | --- | --- |
| Dana Whitcombe | Engagement partner | Fourth year on the engagement |
| Luis Herrera | Engagement quality reviewer | Not otherwise involved in the engagement |
| Grace Lindqvist | Senior manager | Day-to-day leadership; owns the audit plan |
| Omar Haddad | Manager | Revenue, deferred revenue, AR |
| Chris Nwosu | Audit senior | Controls testing coordination, cash, equity |
| Amelia Trent, Jae-won Park | Staff | Substantive testing, confirmations, sampling execution |
| Farrah Nazari | IT audit senior manager | ITGC scoping and conclusions |
| Ben Osei | IT audit senior | ITGC and IT-dependent control testing |
| Tara Iyer | Data and analytics specialist | Journal entry analytics, revenue analytics, RPO recomputation |
| Dr. Igor Petrov | Valuation specialist | Kestrel contingent consideration, TSR PSU Monte Carlo |
| Rebecca Stein | Tax partner | Income tax provision, valuation allowance |
| Priya Chandrasekhar | National office professional practice director | Consulted on the SSP and reseller conclusions |

---

## Part 6 — Materiality (as finally determined; see Chapter 3 for the derivation)

| Measure | Amount (000s) | Basis |
| --- | --- | --- |
| Overall (financial statement) materiality | **1,450** | Approximately 1% of total revenue of $148,200, rounded down |
| Performance materiality | **940** | 65% of overall materiality |
| Clearly trivial threshold (CTT / SUM threshold) | **72** | 5% of overall materiality |
| Specific materiality — related-party transactions, executive compensation, and certain disclosures | **150** | Qualitative sensitivity |
| Component materiality — AtlasFlow Software Ltd (UK) | **580** | 40% of overall materiality |
| Component performance materiality — UK | **380** | 65% of component materiality |
| Component materiality — AtlasFlow Pty Ltd (Australia) | **420** | Specified-procedures scope |
| Prior-year overall materiality (FY2024) | 1,190 | 1% of FY2024 revenue |

---

## Part 7 — Uncorrected and corrected misstatements identified in FY2025 (for Chapter 19)

Corrected (recorded by management):

| Ref | Description | Income effect (000s) |
| --- | --- | --- |
| C-1 | Revenue recognized from March 15 rather than the April 2 provisioning date on 14 Q1 contracts | (410) |
| C-2 | SLA credits earned but not accrued (Northgate and 6 others) | (290) |
| C-3 | Capitalized commissions relating to churned customers not written off | (620) |
| C-4 | Understatement of accrued VAT in the UK entity | (180) |
| C-5 | PSU probability revision recorded in the wrong period | 240 |

Uncorrected (proposed and passed by management, accumulated on the SAD):

| Ref | Description | Income effect (000s) | Balance sheet effect |
| --- | --- | --- | --- |
| U-1 | Projected misstatement from the AR confirmation sample — cut-off errors | (185) | AR overstated |
| U-2 | Allowance for credit losses at the optimistic end of the acceptable range | (240) | ACL understated |
| U-3 | Six December contracts with signature dates that could not be corroborated; revenue effect if reversed | (150) | Revenue and AR overstated |
| U-4 | Professional services percentage-of-completion input estimate error | 95 | Contract asset understated |
| U-5 | Unrecorded liability for a disputed vendor invoice | (110) | Accrued expenses understated |
| U-6 | Prior-year uncorrected misstatement turnaround effect (accrued commissions) | 130 | — |
| | **Net effect on FY2025 pre-tax loss** | **(460)** | |

---

## Part 8 — How chapters should use this file

1. Reference facts by their identifiers (C-1, W-3, I-2, U-1, account 2400) so a reader can navigate between
   chapters.
2. When a chapter needs a figure that appears here, use exactly the figure here.
3. When a chapter needs to change a fact to make a teaching point (for example, "suppose overall materiality
   had been set at $2,100 instead"), state clearly that the variation is hypothetical.
4. Chapters may introduce additional small customers, employees, vendors, or transactions freely.
5. Currency convention: figures are in thousands of US dollars unless a chapter states otherwise. Chapters
   that use whole dollars must say so explicitly at first use.
