```
ASHCROFT VANE LLP                                              WP REF:  C-700
Auburn Ridge Group plc                                         PERIOD:  FY20X4
JOURNAL ENTRY TESTING AND MANAGEMENT OVERRIDE                  YEAR END: 31.12.X4
────────────────────────────────────────────────────────────────────────────────
SIGNIFICANT RISK 4 — Management override of controls (presumed fraud risk)
Prepared by:  E. Balewa (Assistant)           Date: 20X5-02-19
Reviewed by:  S. Lindqvist (Manager)          Date: 20X5-03-03
Reviewed by:  R. Belliveau (Partner)          Date: 20X5-03-10
```

---

## 1. Purpose

To test the appropriateness of journal entries and other adjustments recorded in the preparation of
the financial statements, in response to the presumed risk of management override of controls under
ISA 240.

## 2. Population

| | |
|---|---:|
| Total journal entries posted in FY20X4, all entities | **1,284,306** |
| — System-generated (automated postings from sub-ledgers and interfaces) | 1,242,188 |
| — **Manual journal entries** | **42,118** |
| Manual journals posted in the legacy environment (Jan–Jun) | 18,204 |
| Manual journals posted in Aventine (Jul–Dec) | **23,914** |
| Manual journals posted after the reporting calendar deadline | **187** (FY20X3: 61) |

### 2.1 Completeness and integrity of the population

| Procedure | Result |
|---|---|
| Reconcile the sum of all journal entries to the movement in the trial balance | Agreed to £nil for both environments |
| Agree the record count to the system control total | Agreed |
| Test the completeness and accuracy of the journal extract used | **Performed.** The journal entry extract is one of the four system-generated reports tested at `B-200` §7. Reconciled to the general ledger; 25 entries traced back to the source system. |
| Confirm both environments are covered | Confirmed. Two extracts obtained and combined; the combined file reconciles to the full-year movement. |

## 3. CAAT selection criteria

The full manual journal population was interrogated using the following criteria. The value
threshold was reduced from the prior year £500k to **£250k** as an unpredictability measure
(`A-500` §5).

| # | Criterion | Items |
|---|---|---:|
| 1 | Value above £250k posted to a revenue account | 41 |
| 2 | Value above £250k posted to a contract asset or contract liability account | 28 |
| 3 | Posted by a user in the Group finance function directly to a P&L account above £250k | 34 |
| 4 | **Posted by a member of the Executive Committee** | **7** |
| 5 | Posted outside normal business hours (before 07:00 or after 20:00) above £250k | 22 |
| 6 | Posted at a weekend or public holiday above £250k | 11 |
| 7 | Round-sum entries above £250k (ending in three or more zeros) | 31 |
| 8 | Posted to a suspense, clearing or migration account above £250k | 18 |
| 9 | Entries with a blank or generic narrative ("adjustment", "reclass", "per FD") above £250k | 26 |
| 10 | Entries reversing within 5 days | 9 |
| 11 | **New vendors created in the period with total payments above £250k** | **14** |
| 12 | **Payments made outside the standard payment run above £100k** | **9** |
| 13 | Vendor bank details amended within 30 days before a payment | 6 |
| 14 | Posted using the shared `AVN_SUPPORT` account | 34 |
| | **Gross items meeting one or more criteria** | **290** |
| | Less duplicates (items meeting multiple criteria) | (76) |
| | **Distinct items selected** | **214** |

Criteria 11, 12 and 13 were added in response to the point raised by the preparer at the fraud
discussion (`A-500` §2.2) and the access deficiencies at `B-200`.

## 4. Items tested

| Selection | Items | Value £m |
|---|---:|---:|
| All items meeting criterion 4 (Executive Committee) | 7 | 4.2 |
| All items meeting criteria 11, 12 or 13 | 24 | 6.1 |
| All items above £1.0m | 14 | 31.4 |
| Judgemental selection from the remainder, weighted to criteria 1, 2, 8 and 9 | 15 | 8.7 |
| **Total tested** | **60** | **50.4** |
| Coverage of the 214 selected items | 28.0% by count | 61.2% by value |

For each item tested: the narrative was read, the supporting documentation was obtained and
inspected, the business rationale was assessed, the poster and approver were identified, and the
entry was agreed to the general ledger.

## 5. Results

| Result | Items | Value £m |
|---|---:|---:|
| Supported, appropriate business rationale, correctly recorded | 52 | 42.8 |
| **Exception — no supporting documentation** | **3** | **1.70** |
| **Exception — posted and approved by the same individual** | **4** | **2.90** |
| **Matter requiring further investigation** | **1** | **0.90** |
| **Total** | **60** | **50.4** |

*(Items may fall into more than one category; the table counts each item once, in the most severe
category. Two of the three items with no supporting documentation were also self-approved.)*

### 5.1 Exceptions — no supporting documentation

| Ref | Date | Value £m | Narrative | Account | Explanation obtained |
|---|---|---:|---|---|---|
| JE-08814 | 20X4-10-31 | 0.72 | "Reclass per FD" | Administrative expenses / accruals | Reclassification of an accrual between categories. No P&L effect. Explained by the Financial Reporting Manager as a presentational correction. |
| JE-09912 | 20X4-11-28 | 0.61 | "Adjustment" | Cost of sales / inventory | Correction of an overhead absorption misposting. Recalculated by the audit team and found to be arithmetically correct. |
| JE-11204 | 20X4-12-19 | 0.37 | "Reclass" | Distribution costs / administrative expenses | Reclassification between expense categories. No effect on operating profit. |

**Assessment recorded:** *"In each case the entry has been explained and, where testable, verified.
None affects profit before tax. The absence of documented support is a control deficiency rather than
an indication of override. Reported to management."*

### 5.2 Exceptions — posted and approved by the same individual

| Ref | Date | Value £m | Poster / approver | Account |
|---|---|---:|---|---|
| JE-07741 | 20X4-09-05 | 1.14 | Financial Reporting Manager | Accruals / administrative expenses |
| JE-10188 | 20X4-11-14 | 0.68 | Financial Reporting Manager | Contract liabilities / revenue |
| JE-11876 | 20X4-12-28 | 0.72 | Treasury Analyst | Interest accrual / finance costs |
| JE-11904 | 20X4-12-29 | 0.36 | Treasury Analyst | FX revaluation |

**These are the two users identified at `B-200` §4.1 as holding both journal creation and journal
approval rights.**

**Assessment recorded:** *"The four entries have each been tested to supporting documentation and are
appropriate. The self-approval arises from the access configuration deficiency reported at `B-200`
and `B-300` (D-01) and not from an attempt to circumvent a control. Reported to the Audit
Committee as part of D-01."*

### 5.3 Matter requiring further investigation — JE-12047

| Attribute | Detail |
|---|---|
| Reference | **JE-12047** |
| Date and time posted | **31 December 20X4, 23:47** |
| **Posted by** | **I. Castellanos-Reyes, Chief Financial Officer** |
| Approved by | **Not approved.** The entry was posted using an account with combined create-and-post authority. |
| Value | **£0.90m** |
| Debit | Contract assets — CN-4471 |
| Credit | **Revenue — Equipment & Systems** |
| Narrative | **"Yr end true-up per contract review — IC-R"** |
| Criteria met | 1 (revenue above £250k), 3, 4 (Executive Committee), 5 (outside business hours), 6 (public holiday period), 7 (round sum) |

**This entry met six of the fourteen CAAT criteria — more than any other item in the population.**

#### Procedures performed

| # | Procedure | Result |
|---|---|---|
| 5.3.1 | Obtain the CFO's explanation | **See below** |
| 5.3.2 | Obtain supporting documentation | **A one-line calculation on a printed contract summary sheet, initialled "IC-R". No further support.** |
| 5.3.3 | Agree the entry to the CN-4471 contract records | The £0.90m is not separately identifiable in the `CN-4471 ETC v7.xlsx` schedule at `C-100/6`. The percentage-complete calculation at `C-100` §6.2 produces cumulative revenue of £67.2m, which **includes** this entry. |
| 5.3.4 | Consider whether the entry duplicates or overlaps with the change in estimate at `C-100` | **Not performed** |
| 5.3.5 | Inquire whether the Contract Review Board approved the amount | The December CRB minutes record the change in estimated costs. They do not refer to a revenue true-up of £0.90m. |
| 5.3.6 | Consider the entry against the fraud risk factors at `A-500` | See below |

#### The CFO's explanation

Obtained by telephone on 20 February 20X5, file note at `C-700/8`:

> *"That is the year-end true-up on 4471. When the December contract review concluded, the
> percentage-complete calculation in the system had not picked up the revised cost forecast because
> the project accounting module updates on a monthly cycle and the review landed after the cut. So the
> system was carrying the old percentage. I posted the difference manually so the ledger agreed to
> the reviewed position. It is not a new judgement, it is a mechanical catch-up. Peter [Aylesworth]
> was on leave that week."*

#### Assessment recorded by the preparer

> *"The explanation is consistent with the timing of the December Contract Review Board meeting
> (16 December) and with the monthly update cycle of the project accounting module, which the IT audit
> team has confirmed. The entry is directional with the change in estimate approved by the CRB.
>
> The entry has three features that would ordinarily cause concern: it was posted by the CFO, at
> 23:47 on the last day of the year, to revenue, in a round sum, without approval and with minimal
> support. Against that, the explanation is plausible, the mechanism is verifiable, and the amount is
> below performance materiality.
>
> I have discussed this with SL, who has discussed it with RB. **Conclusion: the entry is accepted.
> No further procedures.**"*

*(Manager's note recorded on the workpaper: "Agree. The substance is the same change in estimate we
have already audited at C-100. Do not double-count it as a separate issue. SL 03/03/X5.")*

#### Cross-reference not made

`C-100` §6.2 records cumulative revenue on CN-4471 of £67.2m and attributes the £3.5m uplift to the
change in the cost estimate. `C-700` records a £0.90m manual entry to CN-4471 revenue posted by the
CFO. **No workpaper reconciles the two, and neither workpaper cross-refers to the other.** The
question of whether the £0.90m is part of the £3.5m or additional to it is not addressed anywhere in
the file.

## 6. New vendor and payment testing (criteria 11–13)

| Criterion | Items | Tested | Exceptions |
|---|---:|---:|---:|
| 11 — New vendors with payments above £250k | 14 | 14 | **1** |
| 12 — Payments outside the standard payment run above £100k | 9 | 9 | **3** |
| 13 — Vendor bank details amended within 30 days of payment | 6 | 6 | 0 |

### 6.1 New vendors — the exception

| Vendor | Payments in FY20X4 £m | First payment | Nature |
|---|---:|---|---|
| **Larkspur Freight Ltd** | **2.40** | 20X4-03-14 | Road haulage and logistics |

| Test | Result |
|---|---|
| Vendor on the approved supplier list at 1 January 20X4? | **No.** Created 6 March 20X4. |
| Evidence of competitive tender or approved single-source justification? | **A single-source justification form dated 6 March 20X4, signed by the Head of Logistics.** No tender documentation. |
| Purchase orders raised for the payments? | 11 of 14 invoices had a purchase order. **3 did not.** |
| Goods received / service delivery evidence? | Delivery notes obtained for 11 of 14 invoices. |
| Rates benchmarked against other hauliers? | **Not evidenced.** Rates appear to be 4–7% above the two comparable hauliers on the approved list, per the audit team's own comparison at `C-700/11`. |
| Companies registry search performed | **Yes — see below** |

**Companies registry search.** Performed by the preparer on 13 February 20X5 as a standard step for
new vendors above £250k. Results filed at `C-700/12` and at `C-800/2`:

| | |
|---|---|
| Larkspur Freight Ltd, company number 09241188 | Incorporated 20X1 |
| **Sole director and sole shareholder** | **Gerald Thwaite-Marchant** |
| Registered office | 4 Rowan Court, Ashley Vale, Meridia AV1 3RQ |
| Note recorded by the preparer | *"Registered office address matches the address given for Ms Castellanos-Reyes's sister (Mrs H. Thwaite-Marchant) on the ARG directors' related party questionnaire. Mr Thwaite-Marchant appears to be the CFO's brother-in-law. Referred to `C-800`."* |

**This matter is carried to `C-800` (related parties).** No further procedure is recorded in `C-700`.

### 6.2 Payments outside the standard payment run — the three exceptions

| Date | Payee | Value £k | Authorised by | Documented exception approval? |
|---|---|---:|---|---|
| 20X4-06-27 | **Larkspur Freight Ltd** | **310** | Head of Logistics | **No** |
| 20X4-07-04 | **Larkspur Freight Ltd** | **215** | Head of Logistics | **No** |
| 20X4-07-11 | **Larkspur Freight Ltd** | **155** | Financial Reporting Manager | **No** |
| | **Total** | **680** | | |

All three payments were made by manual bank transfer in the two weeks either side of the Aventine
go-live on 1 July 20X4.

**Explanation obtained** from the Head of Logistics: *"During the cutover the payment run was
suspended for eight days. Several suppliers were paid manually to avoid breaching payment terms.
Larkspur was one of them."*

**Verification performed:** the audit team obtained the list of all manual payments made during the
cutover window. There were **31 manual payments totalling £4.2m to 19 suppliers**, which corroborates
the explanation that manual payment was a general cutover measure rather than specific to this
vendor. Larkspur received 3 of the 31 payments, representing 16.2% of the value.

**Assessment recorded:** *"The manual payments are explained by the system cutover and are corroborated
by the pattern across 19 suppliers. The absence of documented exception approval is a control
deficiency, reported as D-13. No indication of override."*

## 7. Review of estimates for bias

Required by ISA 240 as part of the override response.

| Estimate | Direction of the FY20X4 judgement | Effect on PBT | Assessment |
|---|---|---|---|
| **CN-4471 costs to complete** | **Favourable — reduced £4.1m** | **+£3.5m** | See `C-100` §6.5 |
| Other contract cost estimates | 7 increased, 4 decreased by less than £0.1m each | −£1.8m | Mixed direction; no bias |
| Inventory provision | Increased following audit challenge | −£1.24m | Adjusted; management accepted |
| Warranty provision | Increased £1.1m | −£1.1m | Unfavourable |
| Expected credit loss | Increased £0.4m | −£0.4m | Unfavourable |
| Contract loss provisions | Increased £0.4m | −£0.4m | Unfavourable |
| **Goodwill — discount rate** | **Favourable — 9.1% against a specialist range of 10.2–11.6%** | Avoids £22.1m impairment | See `C-600` §5.3 |
| **Contingent consideration probability** | **Favourable — 62% retained despite ARR ahead of plan** | Avoids up to £4.4m charge | See `C-500` §5.5 |

> **Recorded conclusion on bias:**
>
> *"Estimates have moved in both directions during FY20X4. Four provisions were increased, reducing
> profit by £3.14m in aggregate, including one increase of £1.24m accepted following audit challenge.
> Management's willingness to accept that adjustment is evidence of an absence of bias.
>
> Where judgements have been favourable, each has been separately audited in the relevant workpaper
> and concluded upon. We do not consider that the pattern of estimates, taken as a whole, indicates
> management bias."*

*(The three favourable judgements listed above total £30.0m of avoided charges. The four unfavourable
provisions total £3.14m. This comparison is not drawn in the workpaper.)*

## 8. Significant transactions outside the normal course of business

| Transaction | Business rationale assessed |
|---|---|
| Acquisition of Kestrel Dynamics Ltd | Strategic; approved by the Board; consistent with the stated software growth objective. Rationale accepted. |
| Write-off of the £1.4m migration suspense balance | See `B-200` §6.1. Rationale accepted. |
| **Engagement of Larkspur Freight Ltd** | **Referred to `C-800`** |
| Disposal of the Bracknell Park freehold | £4.1m proceeds, £0.8m gain. Independent valuation obtained; arm's length purchaser confirmed by registry search. Rationale accepted. |

## 9. Consolidation journals

47 consolidation journals were posted. All 31 above £0.155m were tested.

| Result | Items |
|---|---:|
| Supported and appropriate | 30 |
| **Exception** | **1** |

The exception is an intercompany elimination of £4.6m posted twice and subsequently reversed. Net
effect nil. Reported at `A-600` §8 and recorded as corrected misstatement C3 at `D-100` (the
reversal was posted after the draft financial statements were prepared).

## 10. Uncorrected misstatements arising

None.

## 11. Conclusion

Journal entry testing covering 60 items with a value of £50.4m, selected from 214 items identified by
fourteen CAAT criteria applied to a population of 42,118 manual journals, identified seven control
exceptions and one matter requiring further investigation. All have been explained. One matter — the
identification of Larkspur Freight Ltd as a vendor connected to the Chief Financial Officer — has
been referred to `C-800`.

No indication of management override of controls has been identified. Sufficient appropriate audit
evidence has been obtained in respect of significant risk 4.

```
Signed:  E. Balewa, Assistant                       20X5-02-19
Signed:  S. Lindqvist, Manager                      20X5-03-03
Signed:  R. Belliveau, Engagement Partner           20X5-03-10
```

---

## Schedules

| Ref | Content |
|---|---|
| `C-700/1` | Journal population extract and reconciliation |
| `C-700/2` | CAAT criteria and interrogation output |
| `C-700/3` | Testing schedule, 60 items |
| `C-700/4` | Exception detail — undocumented entries |
| `C-700/5` | Exception detail — self-approved entries |
| `C-700/6` | **JE-12047 — entry detail and supporting sheet** |
| `C-700/7` | *(not used)* |
| `C-700/8` | **File note of telephone discussion with the CFO, 20 February 20X5** |
| `C-700/9` | New vendor analysis |
| `C-700/10` | Manual payment analysis, cutover window |
| `C-700/11` | **Haulage rate comparison** |
| `C-700/12` | **Companies registry search — Larkspur Freight Ltd** |
| `C-700/13` | Review of estimates for bias |
| `C-700/14` | Consolidation journal testing |
