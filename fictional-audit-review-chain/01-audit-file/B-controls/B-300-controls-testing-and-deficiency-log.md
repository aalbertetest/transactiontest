```
ASHCROFT VANE LLP                                              WP REF:  B-300
Auburn Ridge Group plc                                         PERIOD:  FY20X4
PROCESS CONTROLS TESTING AND DEFICIENCY LOG                    YEAR END: 31.12.X4
────────────────────────────────────────────────────────────────────────────────
Prepared by:  C. Nakamura (Assistant)         Date: 20X4-11-28
Reviewed by:  S. Lindqvist (Manager)          Date: 20X4-12-04
Updated:      C. Nakamura                     Date: 20X5-03-02 (roll-forward)
```

---

## 1. Purpose

To document the testing of the operating effectiveness of controls on which the audit intends to
rely, to roll forward interim testing to the year end, and to aggregate all control deficiencies
identified across the audit for evaluation and reporting under ISA 265.

## 2. Controls on which reliance is planned

Only two cycles are planned for controls reliance (`A-700` §4). All other cycles are fully
substantive.

| Cycle | Control | Frequency | Interim sample | Exceptions | Roll-forward |
|---|---|---|---:|---:|---|
| **Aftermarket revenue** | R1 — Despatch note matched to sales order before invoicing (automated three-way match) | Automated | 25 | 0 | Inquiry + 5 items |
| | R2 — Daily review of the unmatched despatch exception report by the Sales Operations Manager | Daily | 25 | **3** | See §3.1 |
| | R3 — Monthly reconciliation of the despatch log to revenue recorded, reviewed by the Financial Controller | Monthly | 5 | 1 | 2 further months |
| | R4 — Credit note authorisation within delegated limits | Per transaction | 25 | 0 | 5 items |
| **Payroll** | P1 — Starters and leavers authorised by HR before entry into Payrolink | Per event | 25 | 0 | 5 items |
| | P2 — Monthly payroll reconciliation reviewed and signed by the Financial Controller | Monthly | 5 | 0 | 2 further months |
| | P3 — Exception report of payments above a threshold reviewed | Monthly | 5 | 0 | 2 further months |

## 3. Exceptions identified

### 3.1 Control R2 — daily review of the unmatched despatch exception report

Three exceptions in a sample of 25. In each case the exception report for the day was generated but
no evidence of review is retained.

| Date | Items on report | Evidence of review |
|---|---:|---|
| 20X4-08-14 | 11 | None |
| 20X4-09-02 | 6 | None |
| 20X4-11-19 | 19 | None |

Discussed with the Sales Operations Manager, who states the review was performed but that the
practice of initialling the printed report lapsed after the Aventine migration, since the report is
now viewed on screen and the system does not record who has opened it.

**Evaluation.** Three exceptions in 25 exceeds the tolerable rate for a control on which reliance is
planned. **Reliance on control R2 is not supportable.**

**Effect.** R2 is a detective control over the completeness of revenue recorded from despatches. Its
failure means the risk it addresses must be covered substantively. The substantive response is the
cut-off testing at `C-200` and the analytical review of Aftermarket revenue by month and by site.

*Note: control R2 is one of the controls whose evidencing practice changed as a result of the
Aventine migration. It is not one of the controls affected by the consulting recommendations at
`A-200` §4.3.*

### 3.2 Control R3 — monthly despatch log to revenue reconciliation

One exception in five. The October 20X4 reconciliation was prepared but not signed as reviewed by
the Financial Controller. The reconciliation itself was arithmetically correct and no reconciling
item exceeded £41k.

**Evaluation.** One exception in five is a high rate but the sample is small. Extended testing was
performed on three further months (May, July, December). All three were prepared and reviewed.
Concluded that R3 operates effectively; the October instance is an isolated documentation lapse
attributable to the Financial Controller's absence in that month.

## 4. Roll-forward to the year end

Interim testing covered 1 January to 31 October 20X4. Roll-forward procedures for November and
December:

| Procedure | Result |
|---|---|
| Inquiry of process owners as to whether any change in the control occurred | No changes reported |
| Inspection of evidence of operation for a sample of 5 items per control (excluding R2) | No exceptions |
| Consideration of whether ITGC deficiencies affect the roll-forward | **See §5** |

## 5. Interaction with the IT general control deficiencies at `B-200`

The controls on which reliance is placed include one fully automated control (R1, the three-way
match) and several manual controls that depend on system-generated information (R2, R3, P2, P3).

`B-200` identifies eight ITGC deficiencies in the Aventine environment, four of them significant,
and concludes at `B-200` §8.2 that reliance on IT general controls remains appropriate for the full
year.

**On the basis of that conclusion**, the automated control R1 and the system-generated information
underpinning R3, P2 and P3 are treated as reliable, and the interim testing is rolled forward to
the year end as set out at §4.

*(If the conclusion at `B-200` §8.2 were not available, reliance on R1, R3, P2 and P3 could not be
supported and the Aftermarket revenue and payroll cycles would revert to fully substantive. The
substantive effect would be an increase in the Aftermarket revenue sample and the addition of a
substantive payroll recalculation. This has not been costed.)*

## 6. Consolidated deficiency log

All deficiencies identified anywhere in the audit, aggregated for ISA 265 evaluation.

| # | Deficiency | Source | Severity | Reported to management | Reported to the Audit Committee |
|---|---|---|---|:-:|:-:|
| D-01 | 14 users with access exceeding role definition; 2 with journal create-and-approve | `B-200` ITGC-01 | **Significant** | ✔ | ✔ |
| D-02 | Privileged access log not reviewed since go-live | `B-200` ITGC-02 | **Significant** | ✔ | ✔ |
| D-03 | Shared `AVN_SUPPORT` account used for 1,247 transactions | `B-200` ITGC-03 | **Significant** | ✔ | ✔ |
| D-04 | 47 of 312 changes without documented approval | `B-200` ITGC-04 | **Significant** | ✔ | ✔ |
| D-05 | Development and deployment not segregated | `B-200` ITGC-05 | Moderate | ✔ | ✖ |
| D-06 | 5 emergency changes never approved | `B-200` ITGC-06 | Moderate | ✔ | ✖ |
| D-07 | £1.8m migration difference not analysed; £1.4m written off | `B-200` ITGC-07 | Moderate | ✔ | ✖ |
| D-08 | 10 of 14 system-generated reports not tested | `B-200` ITGC-08 | Moderate | ✖ | ✖ |
| D-09 | Control R2 — no evidence of review of the daily exception report | `B-300` §3.1 | Moderate | ✔ | ✖ |
| D-10 | Control R3 — one month's reconciliation not evidenced as reviewed | `B-300` §3.2 | Minor | ✔ | ✖ |
| D-11 | Purchase orders raised after the invoice date in 8 of 40 items tested | Substantive P2P testing | Moderate | ✔ | ✖ |
| D-12 | Vendor master data changes not independently verified | Substantive P2P testing | **Significant** | ✔ | ✖ |
| D-13 | Three payments totalling £680k made outside the standard payment run without documented exception approval | `C-700` | Moderate | ✔ | ✖ |
| D-14 | Contract cost forecast look-back not implemented (internal audit recommendation overdue) | `B-100` §6.1 | Moderate | ✔ | ✖ |
| D-15 | Poland — journal approval access exceeding role definition (3 users) | Component return | Moderate | ✔ | ✖ |
| D-16 | Poland — bank reconciliation prepared and reviewed by the same individual in 2 of 12 months | Component return | Moderate | ✔ | ✖ |
| D-17 | Germany — bank reconciliations not completed within the reporting calendar in 4 of 12 months | Component return | Minor | ✔ | ✖ |

### 6.1 Evaluation of deficiencies in combination

ISA 265 requires deficiencies to be evaluated individually **and in combination**.

Groupings considered:

| Grouping | Deficiencies | Combined evaluation recorded |
|---|---|---|
| Access to the general ledger | D-01, D-02, D-03, D-15 | Four deficiencies concerning who can post and approve journals across two jurisdictions. Assessed in combination as **significant**. Reported. |
| Change management | D-04, D-05, D-06 | Assessed in combination as **significant**. Reported. |
| Vendor and payment integrity | D-11, D-12, D-13 | **Assessed individually. Not assessed in combination.** |
| Evidencing of manual review controls | D-09, D-10, D-16, D-17 | Assessed in combination as **moderate**. Common cause: post-migration change in working practice. |

*(On the vendor and payment grouping: D-12 permits vendor bank details to be changed without
independent verification; D-01 identifies two finance users who can amend vendor master data and
release payments; D-13 identifies £680k of payments made outside the standard payment run. These
three deficiencies were logged in three different workpapers by three different preparers and were
not brought together. `C-700` §5 identifies the payments concerned as being to Larkspur Freight
Ltd; `C-800` addresses that supplier from a related party perspective.)*

## 7. Effect on the audit approach

| Control | Reliance planned | Reliance achieved | Substantive response |
|---|---|---|---|
| R1 three-way match | Yes | **Yes** | — |
| R2 exception report review | Yes | **No** | Cut-off testing at `C-200`; monthly analytical review |
| R3 despatch to revenue reconciliation | Yes | Yes | — |
| R4 credit note authorisation | Yes | Yes | — |
| P1 starters and leavers | Yes | Yes | — |
| P2 payroll reconciliation | Yes | Yes | — |
| P3 payroll exception report | Yes | Yes | — |

No change to the overall audit strategy arises. The loss of reliance on R2 is absorbed by
procedures already planned.

## 8. Reporting under ISA 265

| Category | Number | Communicated |
|---|---:|---|
| Significant deficiencies communicated in writing to those charged with governance | 5 (D-01 to D-04 individually, plus the vendor and payment integrity deficiency D-12) | `D-400` §8 |
| Other deficiencies communicated to management | 12 | Management letter, `B-200/9` |

*Note: D-12 is listed as significant in the log at §6 and was communicated to management in the
management letter. `D-400` §8 reports four significant deficiencies to the Audit Committee (D-01 to
D-04). D-12 does not appear in `D-400`.*

## 9. Conclusion

Reliance is achieved on six of the seven controls tested. Seventeen deficiencies are logged, of
which five are assessed as significant. The audit strategy is unchanged.

```
Signed:  C. Nakamura, Assistant                     20X5-03-02
Signed:  S. Lindqvist, Manager                      20X5-03-05
```

---

## Schedules

| Ref | Content |
|---|---|
| `B-300/1` | Control matrix by cycle |
| `B-300/2` | Interim testing samples and results |
| `B-300/3` | Exception analysis — control R2 |
| `B-300/4` | Extended testing — control R3 |
| `B-300/5` | Roll-forward procedures |
| `B-300/6` | Consolidated deficiency log |
| `B-300/7` | ISA 265 evaluation and reporting decisions |
