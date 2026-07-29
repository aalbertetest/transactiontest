# 00-01 — Fact Pattern and Entity Background

**Purpose of this document.** This is the shared factual foundation for all five review levels.
Every workpaper, review note, inspection finding and regulatory determination in this repository is
consistent with the facts set out here. Where a later level discovers something the engagement team
did not know, that fact is flagged in §9 (Information arising after the audit report date) so that
you can tell hindsight from contemporaneous knowledge.

**All facts below are fictional.** See the disclaimer in the top-level `README.md`.

---

## 1. The entity

**Auburn Ridge Group plc** ("ARG", "the Group", "the Company")

| | |
|---|---|
| Incorporation | Meridia, company number 03418872 |
| Listing | Meridian Stock Exchange, Premium Segment, ticker `ARG.MX` |
| Index membership | Meridia Mid-250 (constituent since 20W9) |
| Registered office | Auburn Ridge House, 14 Calloway Street, Verrastown, Meridia VR2 8QN |
| Financial year end | 31 December |
| Reporting framework | IFRS as adopted in Meridia; Meridian Companies Act 20W1; MSE Listing Rules |
| Market capitalisation | £1.16bn (at 31 December 20X4) |
| Employees | 6,842 (20X3: 6,109) |
| Auditor | Ashcroft Vane LLP (appointed 20X1; first year of the current partner's tenure is 20X3) |

### 1.1 What the Group does

ARG designs, manufactures, installs and maintains heavy industrial and rail systems, and — since
around 20X1 — sells software that monitors those systems in service. It reports three segments.

**Equipment & Systems (£742.8m revenue, 57.8% of Group).** Design-and-build contracts for rail
operators, port authorities and process industries. Contracts run 18 to 48 months. Revenue is
recognised **over time** under IFRS 15 using an input method (costs incurred as a proportion of
total estimated costs). This segment is where the Group's accounting judgement is concentrated:
every reporting date requires an estimate of costs to complete on 61 open contracts. It is also
where the audit went wrong (see `ISS-01`).

**Aftermarket Services (£358.4m revenue, 27.9%).** Spares, refurbishment, on-site maintenance and
call-out. Mostly point-in-time revenue on despatch, with some over-time maintenance contracts.
Low judgement, high volume — which is why the cut-off risk here is a sampling problem rather than
an estimation problem (`ISS-02`).

**Software & Subscriptions (£183.4m revenue, 14.3%).** The `Meridian Telemetry Suite` platform,
sold direct and through a reseller channel. Term licences and SaaS subscriptions, some bundled with
hardware and implementation services. Multi-element arrangements, principal-versus-agent questions,
and the fastest-growing part of the Group — the part management talks about on earnings calls
(`ISS-03`).

### 1.2 Structure

```
                        Auburn Ridge Group plc  (Meridia)
                                    │
        ┌───────────────┬───────────┴───────────┬────────────────────┐
        │               │                       │                    │
  ARG Systems Ltd   ARG Polska        ARG Aftermarket Inc     ARG Software Ltd
    (Meridia)       sp. z o.o.            (Delrado)              (Meridia)
   Equipment &       (Poland)          Aftermarket, Americas    Telemetry Suite
     Systems      Manufacturing                                       │
        │          & assembly                              Kestrel Dynamics Ltd
        │                                                      (acq. 1 May 20X4)
  ARG Systems GmbH
     (Germany)
```

Eleven further dormant or immaterial entities are not shown. Group scoping is at `A-600`.

### 1.3 Key people at the entity

| Name | Role | Relevant to |
|---|---|---|
| Duncan Whitmore-Achebe | Chief Executive Officer | Tone at the top; earnings guidance |
| **Imogen Castellanos-Reyes** | **Chief Financial Officer** (appointed Mar 20X3) | `ISS-01`, `ISS-07`, `ISS-08` |
| Peter Aylesworth | Group Financial Controller | Prepares the ETC schedules and the going concern model |
| Marcus Delaney-Obi | Group Treasurer | Refinancing (`ISS-07`) |
| Dame Rosemary Ndlovu-Frost | Audit Committee Chair (independent NED) | Recipient of `D-400` |
| Sanjay Bhattacharya | Head of Internal Audit | Reported the ERP access issues (`ISS-04`) |
| Fiona Meredith-Kaur | Project Director, Rail Programmes | Source of the CN-4471 estimate (`ISS-01`) |
| Gerald Thwaite-Marchant | Sole director, Larkspur Freight Ltd | Brother-in-law of the CFO (`ISS-08`) |

The CFO joined in March 20X3 from a competitor and is widely credited internally with the Group's
re-rating. Her personal remuneration includes an LTIP with an adjusted-EPS vesting condition
measured over FY20X3–FY20X5, with a threshold at 138.0p and a maximum at 156.0p. Reported adjusted
EPS for FY20X4 is 149.2p. **The engagement team documented this LTIP in `A-500` and correctly
identified it as a fraud risk factor. No procedure in the file is linked back to it.**

---

## 2. The financial year in one paragraph

FY20X4 was, on the face of it, a good year: revenue up 10.0%, profit before tax up 8.1%, a
strategically important acquisition completed in May, and the Software segment growing at 31%.
Underneath that, three things were straining. The Group migrated its ERP mid-year and the migration
went badly. Net debt rose to fund the acquisition, bringing the leverage covenant within visible
reach. And the Rail programme — the segment's flagship — was running late, with the Group's largest
contract, CN-4471, disputed by the customer within five weeks of the year end. Every one of the ten
audit issues in this repository sits at the intersection of those three strains.

---

## 3. The transactions and balances that matter

### 3.1 Contract CN-4471 — Northline Rolling Stock Retrofit  → `ISS-01`

The Group's single largest open contract, with the Meridian Rail Authority (MRA).

| | Q3 position (30 Sep 20X4) | Year end (31 Dec 20X4) |
|---|---:|---:|
| Total contract price | £96.4m | £96.4m |
| Costs incurred to date | £38.9m | £52.1m |
| **Estimated total contract costs** | **£78.9m** | **£74.8m** |
| Percentage complete (input method) | 49.3% | **69.7%** |
| Percentage complete at *unrevised* Q3 cost estimate | — | 66.0% |
| Cumulative revenue recognised | £47.5m | £67.2m |
| Forecast contract margin | 18.2% | 22.4% |

In Q4, management **reduced the estimate of total costs to complete by £4.1m**, from £78.9m to
£74.8m. The stated reason was "value engineering savings realised on the bogie assembly workstream
and a reduction in expected third-party certification costs following the MRA's acceptance of a
revised test protocol."

Arithmetic consequence of that £4.1m reduction, in isolation:

- Percentage complete moves from 66.0% to 69.7%
- Cumulative revenue moves from £63.7m to £67.2m
- **Revenue and profit before tax each increase by £3.5m**
- £3.5m is **5.6% of reported PBT** and **113% of Group materiality**

**Evidence on the audit file supporting the £4.1m reduction:**

1. Management's spreadsheet `CN-4471 ETC v7.xlsx`, obtained by email 21 January 20X5
2. One email from the Project Director dated 8 January 20X5, three sentences long
3. A file note recording a 25-minute telephone inquiry with the Project Director

**Not on the audit file:**

- Any corroboration from the Group's quantity surveyors or engineering function
- Any look-back comparing prior ETC estimates on this or other contracts to actual outcomes
- Any analysis of why savings of this size emerged only in Q4
- Any review of contract variations, the MRA's correspondence, or the programme schedule
- Any site visit (the retrofit depot is 90 minutes from the audit team's office)
- Any linkage to the delay claim described at §3.9 below, which was on the same audit file

### 3.2 Revenue cut-off in Aftermarket Services  → `ISS-02`

| | |
|---|---:|
| Population: despatches 15 Dec 20X4 – 15 Jan 20X5 | 2,317 items, £312.4m |
| Sample tested (monetary unit sampling) | 40 items, £84.6m |
| **Errors identified** | **3 items, £1.90m** |
| Nature | Goods despatched 2–5 January 20X5, revenue recorded December 20X4 |

The three errors were added to the schedule of uncorrected misstatements at their **factual** value
of £1.90m. **The sample error was never projected to the population.** Ratio projection gives
£1.90m ÷ £84.6m × £312.4m = **£7.0m**, which is 3.2× performance materiality and 2.3× Group
materiality.

### 3.3 Reseller channel revenue  → `ISS-03`

Of £183.4m Software & Subscriptions revenue, **£38.2m** is sold through third-party resellers and
recognised **gross**. If ARG is an agent, revenue would be the £11.4m commission retained — a
**£26.8m revenue overstatement** with no effect on profit.

The reseller contracts contain terms pointing both ways: ARG sets a recommended list price but
resellers may discount; resellers hold no inventory (licences are provisioned on order); ARG
provides all support to the end customer; resellers bear the credit risk on the end customer but
have a 90-day right of return on unactivated licences.

The Group's accounting memorandum on this question is **one paragraph**. It concludes gross
presentation is appropriate because "ARG is the primary obligor for the software and controls its
functionality." It does not work through the IFRS 15 control indicators.

Firm policy `AV-TAP-04` requires **mandatory consultation with the National Technical Panel** on
any principal-versus-agent conclusion where the gross amount exceeds 1% of group revenue. £38.2m is
**3.0%** of revenue. **No consultation took place.**

### 3.4 The Aventine ERP migration  → `ISS-04`

The Group migrated from legacy systems to **Aventine ERP** with go-live on **1 July 20X4** — six
months before the year end, and in the middle of the audit period.

| Deficiency | Detail |
|---|---|
| User access provisioning | 14 users granted access exceeding their role definition; **2 finance users could both create and approve journal entries and amend vendor master data** |
| Change management | 47 of 312 post-go-live changes lacked documented approval |
| Interface reconciliation | Legacy-to-Aventine migration left an **unexplained £1.8m difference**, posted to a suspense account and written off to operating expenses in Q4 |
| Privileged access | 4 IT staff retained "superuser" access to the production financial ledger throughout H2 |

The Group's own internal audit function reported the access issues to the Audit Committee in
October 20X4. **The engagement team obtained that internal audit report and filed it.** The
engagement team's conclusion at `B-200` was nonetheless that **controls reliance remained
appropriate for the full year**, and the audit approach did not revert to fully substantive.

### 3.5 Acquisition of Kestrel Dynamics Ltd  → `ISS-05`

Acquired **1 May 20X4**. A predictive-maintenance analytics business, 41 employees, complementary
to the Telemetry Suite.

| Consideration | £m |
|---|---:|
| Cash | 68.0 |
| Equity (2.1m ARG shares) | 6.5 |
| **Contingent consideration at fair value** | **11.5** |
| **Total** | **86.0** |

| Identifiable net assets acquired | £m |
|---|---:|
| Developed technology (8-year life) | 21.4 |
| Customer relationships (12-year life) | 14.6 |
| Brand (5-year life) | 3.2 |
| Other net liabilities | (4.4) |
| **Net identifiable assets** | **34.8** |
| **Goodwill** | **51.2** |

The contingent consideration is an earn-out of up to **£18.0m** payable on FY20X5–FY20X6 annual
recurring revenue thresholds. Management's expert (Halloran Peake Valuation LLP) fair-valued it at
£11.5m using a probability-weighted model with a **62% probability of full achievement**. It is a
Level 3 fair value.

The engagement team engaged the firm's own valuation specialist, Dr Helena Brasseur. **Her scope
letter, on the file at `C-500/4`, is limited to "the identification and valuation of acquired
intangible assets" and expressly excludes contingent consideration.** Her deliverable is a
one-page reasonableness note. No one — not the specialist, not the team, not the manager, not the
partner — performed any procedure on the £11.5m contingent consideration liability beyond agreeing
it to the expert's report.

At an 85% probability, which the FY20X5 run-rate at the date of the audit report would support, the
liability would be **£15.9m** — an **understatement of £4.4m**.

### 3.6 Goodwill and the Industrial Systems CGU  → `ISS-06`

Group goodwill of £412.3m is allocated across five CGUs. Four have headroom above 40%. The fifth
does not.

| Industrial Systems CGU | £m |
|---|---:|
| Carrying amount | 186.4 |
| — of which goodwill | 112.7 |
| Recoverable amount (value in use) | 190.3 |
| **Headroom** | **3.9 (2.1%)** |

Management's model uses a **post-tax discount rate of 9.1%** and a terminal growth rate of 2.0%.

The firm's own valuation specialist, asked to review the discount rate, concluded that an
appropriate post-tax WACC for this CGU lay in the range **10.2% to 11.6%**. That conclusion is on
the audit file at `C-600/6`.

At 10.2% the value in use falls to £164.3m, producing an **impairment of £22.1m**. A rise of only
0.2 percentage points, to 9.3%, is enough to eliminate the headroom entirely.

The team's workpaper records the specialist's range and then concludes: *"Management's rate of 9.1%
is at the low end but within a reasonable range given the Group's actual cost of borrowing.
Acceptable."* The specialist's range does not include 9.1%. Nothing on the file addresses the
contradiction.

Separately, IAS 36 requires sensitivity disclosure where a reasonably possible change in a key
assumption would cause impairment. **The FY20X4 financial statements contain no such disclosure.**

### 3.7 Going concern and the refinancing  → `ISS-07`

| | |
|---|---:|
| Cash | £96.3m |
| Revolving credit facility (RCF) | £220.0m committed, **£142.0m drawn**, **matures 27 Feb 20X6** |
| Senior notes | £300.0m, mature 20X7 |
| Lease liabilities | £78.0m |
| **Net debt** | **£423.7m** |
| Covenant 1 | Net debt / Adjusted EBITDA **≤ 3.00×**, tested 31 Mar / 30 Jun / 30 Sep / 31 Dec |
| Covenant 2 | Interest cover **≥ 3.50×** |

Position and forecast:

| Test date | Base case | Downside case |
|---|---:|---:|
| 31 Dec 20X4 (actual) | 2.47× | — |
| 31 Mar 20X5 | 2.58× | 2.79× |
| 30 Jun 20X5 | 2.63× | 2.96× |
| **30 Sep 20X5** | **2.61×** | **3.08× — BREACH** |
| 31 Dec 20X5 | 2.44× | 2.91× |

Two problems:

1. **The assessment period.** Management assessed going concern for **12 months from the balance
   sheet date**, i.e. to 31 December 20X5. The requirement is at least 12 months from the **date the
   financial statements are approved** — 12 March 20X5 — i.e. to at least 31 March 20X6. **The
   RCF maturity of 27 February 20X6 falls inside the required period and outside the period used.**

2. **The downside case breaches the covenant.** The 3.08× figure at 30 September 20X5 is present in
   management's model on the audit file. It is in **column AK, which is hidden in the version
   filed** at `C-900/3`. It is visible if the sheet is unhidden.

Work performed by the team: review of the base case; recalculation of the base case covenant
compliance; a management representation. **No reverse stress test. No evidence of refinancing
progress — no term sheet, no bank credit committee paper, no correspondence.** No consideration of
the downside case's covenant outcome.

The conclusion at `C-900` is that **no material uncertainty exists**. The financial statements
contain no material uncertainty disclosure.

### 3.8 Larkspur Freight Ltd  → `ISS-08`

During journal entry testing (`C-700`), audit assistant Emeka Balewa identified payments totalling
**£2.4m** during FY20X4 to **Larkspur Freight Ltd**, a logistics provider not previously known to
the team and not on the Group's approved-supplier list at the start of the year.

A companies-registry search performed by Mr Balewa and filed at `C-800/2` shows the sole director
and shareholder of Larkspur Freight Ltd to be **Gerald Thwaite-Marchant**. A second search, also on
file, records that Mr Thwaite-Marchant's registered address matches that of Ms Castellanos-Reyes's
sister. **He is the CFO's brother-in-law.**

Three payments totalling **£680k** were authorised outside the standard procurement system, by
manual payment run, in the weeks either side of the ERP go-live.

The specific materiality set for related party transactions and directors' remuneration is
**£100k**. £2.4m is **24 times** that amount.

The workpaper conclusion reads in full: *"Discussed with CFO who confirmed Larkspur is a
long-standing haulage supplier engaged on arm's length terms following competitive tender.
Relationship is by marriage and not a close family member per the CFO. No disclosure required.
Cleared."*

**The FY20X4 related party note discloses no transaction with Larkspur Freight Ltd.**

### 3.9 The MRA delay claim  → connects to `ISS-01`

On **4 February 20X5** — during fieldwork, five weeks after the year end and five weeks before the
audit report — the Meridian Rail Authority served notice of a claim for **liquidated damages of
£6.8m** in respect of programme delays on **contract CN-4471**.

The engagement team documented this at `C-950`, obtained a legal letter, accepted management's
assessment that the claim was "without merit and will be resisted", agreed that no provision was
required, and checked that a contingent liability disclosure was made.

That work is, in isolation, adequate.

**No one on the file, at any of the first three review levels, connected a customer's £6.8m delay
claim to management's decision, in the same quarter, to reduce the estimated cost of completing the
same contract by £4.1m.**

### 3.10 Non-audit services  → contributes to `ISS-04` and root cause analysis

| Service | £m | Assessment |
|---|---:|---|
| Statutory audit | 1.42 | — |
| Half-year review | 0.11 | Permitted |
| Tax compliance | 0.18 | Permitted |
| **"Operational efficiency review", H2 20X4** | **0.32** | **Self-review and management threat** |
| **Total non-audit** | **0.61** | **43% of audit fee** |

The £0.32m engagement, performed by the firm's consulting arm between July and November 20X4,
included **advice on the configuration of approval workflows in Aventine ERP** — the same controls
the audit team then tested and relied upon at `B-200`.

Firm policy caps non-audit fees at **40%** of audit fees for listed audit clients. The actual ratio
is **43%**. The breach was identified in the independence workpaper `A-200`, escalated to the Ethics
Partner, and cleared on the basis that the ratio "will normalise in FY20X5". The safeguards
recorded are (a) different personnel, and (b) audit committee approval.

---

## 4. Materiality

| Measure | £m | Basis |
|---|---:|---|
| Benchmark: profit before tax | 62.4 | |
| **Group materiality** | **3.10** | 5.0% of PBT |
| **Performance materiality** | **2.17** | 70% of Group materiality |
| **Clearly trivial threshold** | **0.155** | 5% of Group materiality |
| Specific materiality — related parties, directors' remuneration | **0.100** | Qualitative |
| Component materiality range | 0.60 – 2.30 | See `A-600` |

Full derivation and the challenge to the 70% performance materiality percentage is at `A-300`.

---

## 5. Audit scope and coverage

| Component | Scope | Revenue coverage | PBT coverage |
|---|---|---:|---:|
| ARG Systems Ltd (Meridia) | Full | 44% | 41% |
| ARG Polska sp. z o.o. | Full (component auditor) | 19% | 21% |
| ARG Software Ltd + Kestrel | Full | 8% | 6% |
| ARG Systems GmbH | Specified procedures | 12% | 14% |
| ARG Aftermarket Inc (Delrado) | Analytical procedures only | 15% | 16% |
| Other / eliminations | Analytical procedures only | 2% | 2% |
| **Full-scope total** | | **71%** | **68%** |

29% of revenue and 32% of PBT received only specified or analytical procedures. Scoping rationale
is at `A-600`; the inspection team's challenge to it is at `I-300`, finding `INSP-F09`.

---

## 6. Engagement economics

| | FY20X4 | FY20X3 |
|---|---:|---:|
| Audit fee | £1.42m | £1.29m |
| Budgeted hours | 2,860 | 2,740 |
| **Actual hours** | **3,140** | 2,801 |
| Recovery rate | 82% | 94% |
| Total workpapers in the e-file | 4,127 | 3,688 |

The engagement overran its budget by 9.8% and recovered 82% of standard rates. The engagement
partner's practice unit was, per `I-400`, 6% behind its profitability target for FY20X5 at the date
the ARG file was being completed.

---

## 7. The four reviews, in summary

| Level | Reviewer | Hours | Coverage | Notes raised | Outcome |
|---|---|---:|---:|---:|---|
| 2 — Manager | Sasha Lindqvist | 118.0 | 1,842 of 4,127 workpapers (44.6%) | 49 | All closed by 11 Mar 20X5 |
| 3 — Partner | Ronan Belliveau | 11.5 (review) | 312 of 4,127 workpapers (7.6%) | 19 (13 acknowledgement-only) | Authorised signature 12 Mar 20X5 |
| 4 — Internal inspection | Nathaniel Ferreira-Osei | 141.0 | Targeted | 6 findings + 8 improvement points (draft) → 2 findings + 12 improvement points (final) | Draft grade 3 → **final grade 2** |
| 5 — Regulator | Ingrid Halvorsen-Duffy | 402.0 | File + firm systems | 14 findings, 14 required actions | **Grade D**; enforcement referral |

---

## 8. What each level knew

This matters for judging the reviews fairly.

| Fact | Team (Mar 20X5) | Manager | Partner | Inspection (Jul 20X5) | Regulator (20X6) |
|---|:-:|:-:|:-:|:-:|:-:|
| CN-4471 ETC reduced £4.1m | ✔ | ✔ | ✔ | ✔ | ✔ |
| MRA £6.8m delay claim | ✔ | ✔ | ✖ not escalated | ✔ | ✔ |
| Cut-off errors not projected | ✔ | ✔ | ✖ | ✔ | ✔ |
| Hidden column showing 3.08× covenant breach | ✖ present but unopened | ✖ | ✖ | ✔ | ✔ |
| Larkspur / CFO connection | ✔ | ✔ | ✖ not escalated | ✔ | ✔ |
| Specialist WACC range excludes 9.1% | ✔ | ✔ | ✖ | ✔ | ✔ |
| EQR sign-offs dated after report date | ✖ | ✖ | ✖ | ✔ | ✔ |
| Post-archive modification of C-100 | ✖ | ✖ | ✖ | ✖ **not detected** | ✔ |
| Q1 20X5: CN-4471 costs revised **up** £3.2m | ✖ | ✖ | ✖ | ✔ | ✔ |
| H1 20X5: £16.2m impairment of Industrial Systems CGU | ✖ | ✖ | ✖ | ✖ | ✔ |
| FY20X5: CN-4471 costs revised **up** a further £5.9m | ✖ | ✖ | ✖ | ✖ | ✔ |

**Nothing in the first three columns depends on hindsight.** Every issue in the spine was capable of
being identified from evidence physically present on the audit file on 12 March 20X5.

---

## 9. Information arising after the audit report date

Used by Levels 4 and 5. Flagged so that hindsight can be discounted where appropriate.

| Date | Event | Bears on |
|---|---|---|
| 22 Apr 20X5 | RCF refinancing indicative term sheet received from lead bank | `ISS-07` — was not available at the report date |
| 28 Apr 20X5 | CN-4471 forecast costs to complete **increased by £3.2m** at Q1 review | `ISS-01` |
| 12 May 20X5 | Audit file assembly completed — **61 days** after the report date | `ISS-10` |
| 19 May 20X5 | Nine workpapers modified **after archive lock**, including a two-page "look-back analysis" added to `C-100` that was not present on 12 March | `ISS-01`, `ISS-10` |
| 6 Aug 20X5 | FY20X5 interim results recognise a **£16.2m goodwill impairment** in the Industrial Systems CGU | `ISS-06` |
| 14 Nov 20X5 | MRA delay claim settled at **£4.1m** against ARG | `ISS-01`, `C-950` |
| 3 Mar 20X6 | FY20X5 results: CN-4471 cumulative cost overrun of a **further £5.9m**; contract margin restated to 11.4% | `ISS-01` |
| 3 Mar 20X6 | FY20X5 accounts include a **material uncertainty related to going concern** | `ISS-07` |

The FY20X5 audit was performed by a different engagement partner following the firm's rotation of
Mr Belliveau off the engagement in November 20X5.

---

## 10. Why the file failed — the one-paragraph version

Every issue in this repository has the same shape. Evidence that pointed one way was on the file.
Evidence that pointed the other way was also on the file, and was either not looked at, not
connected to anything, or acknowledged in a sentence and then set aside. The engagement team did not
lack information. It lacked the habit of asking what the information it already had was telling it,
and the reviews above it were structured to check that boxes were filled rather than that
conclusions were supported. The firm's inspection function then identified this correctly and
graded it away. That last step is what turned an audit failure into a regulatory finding about the
firm.
