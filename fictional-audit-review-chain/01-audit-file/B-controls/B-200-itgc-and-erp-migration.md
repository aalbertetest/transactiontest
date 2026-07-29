```
ASHCROFT VANE LLP                                              WP REF:  B-200
Auburn Ridge Group plc                                         PERIOD:  FY20X4
IT GENERAL CONTROLS AND THE AVENTINE ERP MIGRATION             YEAR END: 31.12.X4
────────────────────────────────────────────────────────────────────────────────
Prepared by:  Y. Demirci (IT Audit, Assistant Manager)    Date: 20X5-03-03
Reviewed by:  —                                            Date: —
────────────────────────────────────────────────────────────────────────────────
REVIEW STATUS: This workpaper was not opened in the e-file by the audit manager.
The engagement partner opened it on 20X5-03-10 for 20 minutes. No review notes
were raised on it by either reviewer.
```

*(The review status block above was added by the internal inspection team in July 20X5 from the
e-file audit trail. It did not form part of the workpaper as archived.)*

---

## 1. Purpose

To evaluate the general IT controls over the applications relevant to financial reporting in both
the legacy and the Aventine environments, to conclude on whether reliance may be placed on
automated controls and system-generated information, and to assess the completeness and accuracy of
the data migrated.

## 2. Scope

| Application | Period in scope | Relevance |
|---|---|---|
| Sentinel Financials 8.2 (legacy) | 1 Jan – 30 Jun 20X4 | General ledger, AP, AR, fixed assets |
| **Aventine ERP** | **1 Jul – 31 Dec 20X4** | General ledger, AP, AR, fixed assets, project accounting, consolidation |
| Cornerstone PM | Full year | Contract cost capture; interfaced to both |
| Kestros TMS | Full year | Treasury |
| Payrolink (outsourced) | Full year | Covered by ISAE 3402 — see `B-100/8` |

ITGC domains tested: access to programs and data; program changes; program development; computer
operations.

## 3. The migration

| | |
|---|---|
| Go-live | 1 July 20X4 |
| Approach | Big bang for Meridia, Poland and Germany; Delrado migrated 1 October 20X4 |
| Implementation partner | Voltaris Consulting Ltd |
| Data migrated | Master data (customers, vendors, materials, projects); open items; opening trial balance at 30 June 20X4 |
| Parallel running | 4 weeks planned; **2 weeks actual** |
| Post-implementation review | Performed by ARG internal audit, reported October 20X4, **rated RED** |

## 4. Findings — access to programs and data

### 4.1 User access provisioning

| Test | Population | Sample | Exceptions |
|---|---|---:|---:|
| New user access requests approved by the appropriate line manager and role owner | 218 new/changed accesses since go-live | 25 | **6** |
| Access consistent with the documented role definition | 218 | 25 | **4** |
| Leavers' access revoked within 5 working days | 74 leavers | 25 | 3 |

**Full-population analysis** was subsequently performed on the access extract at 31 December 20X4
using the role definition matrix.

> **Result: 14 users hold access exceeding their documented role definition.**
>
> | Function | Users | Nature of excess access |
> |---|---:|---|
> | Finance — Meridia | **2** | **Able to create AND approve journal entries; able to amend vendor master data AND release payments** |
> | Finance — Poland | 3 | Able to create and approve journal entries |
> | Operations | 4 | Read/write access to project cost fields beyond their assigned projects |
> | Procurement | 3 | Able to create vendors and raise purchase orders |
> | IT | 2 | Application administrator rights combined with a business role |
>
> The two Meridian finance users are a Financial Reporting Manager and a Treasury Analyst.

### 4.2 Privileged access

| Test | Result |
|---|---|
| Number of accounts with superuser access to the Aventine production financial ledger | **4** throughout H2 |
| Are these accounts individually attributable? | 3 yes; **1 is a shared account (`AVN_SUPPORT`)** used by Voltaris Consulting |
| Is privileged activity logged? | Yes, logging is enabled |
| **Is privileged activity reviewed?** | **No. No review of the privileged access log has been performed since go-live.** |
| Number of transactions posted using the shared `AVN_SUPPORT` account in H2 | **1,247**, of which 34 are journal entries to the general ledger |

### 4.3 Legacy environment (1 Jan – 30 Jun 20X4)

| Test | Sample | Exceptions | Conclusion |
|---|---:|---:|---|
| User access provisioning | 25 | 1 | Operating effectively |
| Leaver revocation | 25 | 0 | Operating effectively |
| Privileged access review | 6 monthly reviews | 0 | Operating effectively |
| Password and authentication parameters | Configuration inspected | 0 | Operating effectively |

**The legacy environment's ITGCs operated effectively for the first six months.** Controls reliance
for the period to 30 June 20X4 is supportable.

## 5. Findings — program changes

| Test | Population | Result |
|---|---|---|
| Changes to the Aventine production environment since go-live | **312** | |
| Changes with documented approval by the change advisory board | 265 | |
| **Changes without documented approval** | **47 (15.1%)** | Of which 11 affected financial reporting configuration |
| Changes tested to evidence of user acceptance testing | 25 sampled | 5 exceptions |
| Segregation between development and deployment | Configuration inspected | **Not enforced.** 2 developers hold deployment rights to production. |
| Emergency changes | 19 | 14 retrospectively approved; 5 not approved at all |

The 11 unapproved changes affecting financial reporting configuration were reviewed individually.
Nine are cosmetic (report layouts, field labels). **Two altered posting logic**: a change on
14 September 20X4 to the automatic revenue accrual routine in Project Accounting, and a change on
2 November 20X4 to the default cost centre allocation for indirect labour.

Both were discussed with the IT Applications Manager, who confirmed they were requested by finance
and tested informally. The financial effect has not been quantified.

## 6. Findings — data migration

| Test | Result |
|---|---|
| Opening trial balance at 1 July 20X4 agreed to the closing legacy trial balance at 30 June 20X4 | Agreed **except as below** |
| Master data record counts reconciled | Customers agreed; vendors agreed; **materials: 218 records not migrated, all obsolete, confirmed by inspection** |
| Open AR and AP items reconciled | Agreed |
| **Unreconciled difference on migration** | **£1.8m** |

### 6.1 The £1.8m migration difference

An unreconciled difference of £1.8m arose on migration of the opening trial balance. It was posted
to a suspense account (`99100 — Migration Suspense`) on 1 July 20X4.

| Date | Movement | Balance |
|---|---|---:|
| 1 Jul 20X4 | Difference recognised on migration | 1.8 |
| Jul – Nov 20X4 | Partial analysis by the finance team; £0.4m identified as a duplicated accrual and reversed | 1.4 |
| **31 Dec 20X4** | **Balance written off to administrative expenses** | **nil** |

Discussed with the Group Financial Controller. Explanation:

> *"The residual £1.4m could not be analysed to individual items within a reasonable time. The
> analysis performed indicated it related principally to accrual and prepayment balances in the
> legacy system that had not been properly maintained. We took the view that carrying an
> unexplained suspense balance into the year end was worse than writing it off, and the amount is
> below materiality."*

**Audit work performed:** the write-off journal was inspected and traced to the general ledger. The
partial analysis performed by the finance team was read. The amount, £1.4m, is below performance
materiality of £2.17m.

**Conclusion:** the write-off is accepted. The £1.8m gross difference has not been analysed by the
audit team to determine whether it indicates that any specific balance is misstated.

## 7. Application controls and system-generated reports

| Item | Position |
|---|---|
| Automated controls identified as relevant | 11 (three-way match; credit limit block; duplicate invoice check; contract percentage-complete calculation; others) |
| Automated controls tested | **0** |
| System-generated reports used as audit evidence | 14 |
| **Completeness and accuracy of those reports tested** | **Partially — 4 of 14** |

The four reports tested for completeness and accuracy are the general ledger detail extract, the
journal entry extract used for `C-700`, the aged receivables report and the fixed asset register.
The remaining ten, including the contract cost report used at `C-100` and the despatch report used
at `C-200`, were not tested.

Rationale recorded: *"Reliance on these reports is indirect; the underlying data is corroborated by
other substantive procedures."*

## 8. Aggregation and evaluation

### 8.1 Deficiencies identified

| # | Deficiency | Domain | Severity assessed by preparer |
|---|---|---|---|
| ITGC-01 | 14 users with access exceeding role definition, including 2 with journal create-and-approve | Access | **Significant** |
| ITGC-02 | Privileged access log not reviewed since go-live | Access | **Significant** |
| ITGC-03 | Shared `AVN_SUPPORT` account used for 1,247 transactions | Access | Significant |
| ITGC-04 | 47 of 312 changes without documented approval | Change | Significant |
| ITGC-05 | Development and deployment not segregated | Change | Moderate |
| ITGC-06 | 5 emergency changes never approved | Change | Moderate |
| ITGC-07 | £1.8m migration difference not analysed; £1.4m written off | Migration | Moderate |
| ITGC-08 | 10 of 14 system-generated reports not tested for completeness and accuracy | Reporting | Moderate |

Six deficiencies are assessed as significant or moderate in the access and change domains, which
are the domains on which reliance on automated controls and system-generated information depends.

### 8.2 Conclusion on controls reliance

| Period | Environment | ITGC conclusion | Controls reliance |
|---|---|---|---|
| 1 Jan – 30 Jun 20X4 | Sentinel Financials (legacy) | **Effective** | **Supportable** |
| 1 Jul – 31 Dec 20X4 | Aventine ERP | **Deficiencies identified as above** | **See below** |

> **Conclusion recorded by the preparer:**
>
> *"The deficiencies identified relate to the administration of the IT environment rather than to
> the processing of transactions. No misstatement has been identified as arising from any of them.
> The users holding excessive access are known individuals in finance and IT functions, not
> unidentified parties, and there is no evidence that the excess access has been used
> inappropriately. Compensating controls exist in the form of the monthly CFO certification of the
> consolidation and the Board's review of management accounts against budget.*
>
> *On balance, reliance on IT general controls remains appropriate for the full year. The
> deficiencies will be reported to management and to the Audit Committee in accordance with
> ISA 265."*

**Reliance placed by the audit approach:** Aftermarket revenue (controls plus substantive) and
payroll (controls plus substantive), per `A-700` §4.

## 9. Independence safeguard — `A-200` §4.3(4)

The firm's consulting practice performed an operational efficiency review during FY20X4 that
included recommendations on Aventine approval workflows.

| Step | Result |
|---|---|
| Consulting report obtained and read | Yes — sections 4 and 6 are relevant |
| Controls affected by the recommendations identified | **Purchase-to-pay authorisation limits and the segregation of duties matrix for procurement** |
| Confirmation that no reliance is placed on affected controls | **Confirmed.** The purchase-to-pay cycle is audited on a fully substantive basis per `A-700` §4. |

## 10. Reporting

| Recipient | Deficiencies reported | Reference |
|---|---|---|
| Management | All eight, in a management letter dated 6 March 20X5 | `B-200/9` |
| Audit Committee | ITGC-01 to ITGC-04 reported as significant deficiencies | `D-400` §8 |

## 11. Conclusion

IT general controls in the legacy environment operated effectively to 30 June 20X4. In the Aventine
environment, eight deficiencies have been identified, of which four are significant. On the basis
set out at §8.2, reliance on IT general controls for the full year is concluded to remain
appropriate, and the audit approach at `A-700` is unchanged.

```
Signed:  Y. Demirci, IT Audit                       20X5-03-03
```

---

## Schedules

| Ref | Content |
|---|---|
| `B-200/1` | ITGC scoping and application inventory |
| `B-200/2` | Access provisioning testing — samples and exceptions |
| `B-200/3` | **Full-population access analysis at 31 December 20X4** |
| `B-200/4` | Privileged access listing and log extract |
| `B-200/5` | Change management population and testing |
| `B-200/6` | Data migration reconciliation and suspense account analysis |
| `B-200/7` | System-generated report testing |
| `B-200/8` | ARG internal audit — Aventine post-implementation review, October 20X4 (RED) |
| `B-200/9` | Management letter, 6 March 20X5 |
