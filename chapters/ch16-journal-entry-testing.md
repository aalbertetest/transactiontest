# Chapter 16 — Journal Entry Testing

> Journal entry testing is required whether or not you have identified a fraud risk in the accounts it touches, which
> makes it easy to perform badly: run a query, print 30 rows, write "no exceptions noted." AtlasFlow posted 41,610
> entries to NetSuite in FY2025 across 118,442 lines. Of those, 4,912 were flagged manual, 3,847 of them fell below the
> $250,000 approval threshold with no evidence of independent review, 27 more never touched NetSuite at all, and 53 the
> client calls automated were typed by a human. This chapter is the work a 30-row printout does not do: proving you have
> the whole population, proving the client's labels are true, designing criteria that select the right hundred entries,
> and writing a conclusion that survives the question of how you know the file was complete.

## Learning Objectives

- **LO 16.1** State what AS 2401 and AU-C 240 require for journal entries and other adjustments, and distinguish the
  requirement from firm methodology.
- **LO 16.2** Draft a journal entry data request specifying fields, grain, and format, and the questions to put to the
  data owner before the extract is produced.
- **LO 16.3** Reconcile a journal entry file to trial balance movement at the statement and account level, and test the
  completeness of the client's manual-entry flag.
- **LO 16.4** Design risk-based criteria as executable queries and evaluate whether a criterion selects nothing,
  everything, or the intended risk.
- **LO 16.5** Build a weighted scoring model, stratify the scored population, and defend the selection basis.
- **LO 16.6** Test a selected entry against support, business purpose, authorization, and the accounting conclusion.
- **LO 16.7** Identify and test the entry populations outside the general ledger, including top-side entries and
  subledger adjustments.
- **LO 16.8** Evaluate completeness of period-end adjusting entries against the close calendar, and interpret reversal
  data.
- **LO 16.9** Draft the sufficiency conclusion, including the effect of unresolved data reliability issues.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 2401.58–.62 | Examining entries and other adjustments regardless of assessed risk; characteristics of entries to select; emphasis on period end; unpredictability; business rationale of significant unusual transactions |
| PCAOB | AS 2110; AS 2201 | The period-end reporting process and how entries are initiated, authorized, and recorded outside the routine flow; controls over it, which feed the ICFR opinion |
| PCAOB | AS 1105; AS 2810 | Reliability of information used as evidence, including IPE; evaluating accumulated misstatements and whether they indicate fraud |
| PCAOB | AS 1215; AS 1305 | Documentation an experienced auditor could follow, including the source of extracted data; written communication of deficiencies |
| AICPA | AU-C 240; AU-C 330; AU-C 265; AU-C 315 (SAS 145); AU-C 500 (SAS 142) | Entry testing as a response to management override; substantive responses; deficiency communication; the period-end process and general IT controls; attributes of information used as evidence |
| FASB ASC; SEC | 718-10-25; 830-30; Exchange Act Rule 13a-15 | Performance-condition probability behind the case study entry; translation top-sides; disclosure controls reaching the spreadsheet consolidation |

AtlasFlow is an SEC issuer, so PCAOB standards govern. AU-C 240's requirements are substantively the same, but three
differences matter under AICPA standards: there is no ICFR opinion, so the 45 entries in §16.11 lacking review evidence
produce an AU-C 265 communication rather than a potential adverse opinion; AU-C 500 as amended by SAS 142 is more
explicit than AS 1105 about the attributes of information used as evidence; and private-company general IT controls are
often untested, so the §16.3 reconciliations become the whole of the extract's reliability evidence.

## Prerequisites and Chapter Dependencies

Read Chapters 11 and 12 first: an extract is IPE, and the general IT controls (W-1, W-2, W-5, W-13) and
report-reliability techniques there are what allow you to treat 118,442 rows of NetSuite output as evidence rather than
an assertion. Chapter 3 supplies overall materiality of $1,450, performance materiality of $940, and the clearly trivial
threshold of $72; Chapter 13 the close walkthrough behind §16.9; Chapter 15 the sampling vocabulary. Chapters 17 and 18
cover the schemes this testing detects and the general analytics; Chapters 14 and 19 grade the deviations and accumulate
the misstatements.

## 16.1 What the requirement actually says, and what it does not

AS 2401.58 through .62 require the auditor to test the appropriateness of journal entries recorded in the general
ledger and of other adjustments made in preparing the financial statements. Four features are routinely misread.

**It is not risk-contingent.** The requirement responds to the risk of management override, which the standards treat
as present in every audit. A team documenting "fraud risk in revenue addressed through cut-off testing; therefore no
separate journal entry procedures" has failed to perform a required procedure.

**It reaches "other adjustments."** The consolidation top-side entries (§16.8), the Zuora Revenue subledger
adjustments that reach the ledger only inside a monthly summary journal, and reclassifications made in the drafting
file are all adjustments made in preparing the financial statements. AtlasFlow's 27 top-sides totaling $6,200 are inside
the requirement and outside NetSuite, so a population defined as the extract is incomplete by construction.

**Period end is required; the rest of the period is judgment.** The standard directs selection of entries made at period
end and consideration of testing throughout it — for AtlasFlow, four quarter ends, the December close, and the
post-close window through the February 20, 2026 report date.

**The output is an appropriateness conclusion, not an exception count.** Appropriateness is a four-part question —
support, business purpose, authorization, accounting — and the answers diverge.

The requirement prescribes no sample size, scoring model, or number of criteria; those are firm methodology, and the
workpaper should say which is which.

## 16.2 Obtaining the population: the data request and the source-system landscape

The highest-leverage half hour on this procedure is the conversation before the extract is produced. A file at the wrong
grain, in the wrong currency, or filtered to exclude voided entries costs two weeks to diagnose, and the second request
lands during the close.

**Exhibit 16-1. Journal entry data request — field list for the FY2025 NetSuite extract.**

| Group | Fields requested (format) | Why the group is needed |
| --- | --- | --- |
| Keys and grain | Entry number (text); line number (integer) | Joins lines to support; fixes grain |
| Dates | Posting date and period; effective or document date; created date-time to the minute with time zone | The three differ on accruals; only the timestamp reveals weekend, after-hours, and post-cut-off work |
| People | Preparer ID; approver ID and approval timestamp; last-modified user ID and timestamp | Conflicts; tests W-12; detects editing of interface entries |
| Classification | Source / journal type code; account number and name; subsidiary; department, class, or location | Origin, plus what criteria and the reconciliation need |
| Amounts | Transaction-currency amount with ISO code; functional amount; reporting amount (all signed); debit/credit indicator | Round-amount tests run in transaction currency; the reporting column ties to the trial balance |
| Narrative | Header description; line memo; reference or source document number | Line memos are often populated where headers are blank |
| Flags | Reversal flag, date, and reversed-entry ID; attachment indicator and count; status and void indicator | Reversal pairing; support retention; voided entries count |

Specify pipe-delimited UTF-8, one row per line, no subtotals, a control-total page showing record count and total debits,
and the trial balance at both period ends by account and subsidiary from the same system. Then put these eleven questions
to the data owner — the NetSuite administrator, with Ray Sandoval present:

1. Which saved search produced this file, and will you re-run it with us watching?
2. Is the grain one row per line or per entry, and are there subtotal rows?
3. Are voided, deleted, and pending entries included, and what happens on deletion rather than voiding?
4. Which date field defined the FY2025 filter?
5. Which user IDs are service accounts, and who can log in as each?
6. Which accounts are statistical or non-posting, and are they included?
7. Is the amount column transaction, functional, or reporting currency, and which rate table was used?
8. Are intercompany eliminations here or only in the consolidation workbook?
9. Are all five subsidiaries included, including Kestrel activity after August 4, 2025?
10. Were any entries loaded by CSV import or web services rather than keyed, and how would the file show it?
11. What does the source or type field key off — the transaction's origin, the posting user, or a checkbox?

Question 10 mattered: 1,164 manual entries were loaded by CSV import, which records the importing user as creator, and
whether an import passes approval routing is settled by re-performance, not inquiry.

### 16.2.1 How automated entries reach the general ledger

Criteria over manual entries cannot be designed until you know what the automated ones are. The §2.2 interface inventory
documents nine integrations; the file contains twelve source types, three of them undocumented — the Zuora Billing
invoice feed, the SAP Concur expense feed, and NetSuite's depreciation schedule.

**Exhibit 16-2. Automated (interface- and system-generated) entry population, FY2025 (counts and absolute value in
thousands of USD).**

| Source type in NetSuite | Origin | Count | Absolute value |
| --- | --- | --- | --- |
| Cash Receipt / Payment / Transfer | Bank feed I-9; daily sweeps and investment rollovers | 12,460 | 1,240,000 |
| Invoice / Credit Memo | Zuora Billing feed (undocumented) | 11,904 | 178,300 |
| Vendor Bill / Bill Payment; Expense Report | Coupa I-7 matched postings (9,840); SAP Concur feed, undocumented (2,021) | 11,861 | 45,300 |
| Journal — Stripe daily summary | I-4 Lambda job (W-7) | 365 | 12,400 |
| Journal — payroll | I-5; ADP semi-monthly (24), Deel monthly (12) | 36 | 84,300 |
| Journal — Zuora Revenue summary | I-3 monthly revenue journal | 12 | 112,300 |
| Five other monthly journals: depreciation and amortization (11,900), deferred commission amortization (8,600), FX revaluation (3,600), indirect tax (2,900), India cost-plus (1,800) | NetSuite schedules, Avalara, recurring template | 60 | 28,800 |
| **Total automated** | | **36,698** | **1,701,400** |
| Manual entries (§16.4) | | 4,912 | 140,900 |
| **Total FY2025 journal entries** | | **41,610** | **1,842,300** |

Absolute value is the sum of debits, which equals the sum of credits. The cash line dominates because the daily sweep
among accounts 1010, 1020, and 1045 and the Treasury bill rollovers in account 1100 move gross amounts many times any
income statement figure, so a value-weighted criterion selects treasury mechanics, not judgments.

## 16.3 Proving the population is complete

Completeness is established by reconciling the file to something you have audited separately, not by the client's
assertion or the record count on the cover page. Run these five tests in order, documenting the number obtained.

**Exhibit 16-3. Completeness and integrity tests over the FY2025 journal entry extract (in thousands of USD
except counts).**

| Test | What you compare | Result | Difference |
| --- | --- | --- | --- |
| T-1 Record integrity | File counts versus the administrator's control-total page | 118,442 lines / 41,610 entries both sides | 0 |
| T-2 Internal balance | Debits versus credits, reporting currency, line grain | $1,842,300 each side | 0 |
| T-3 Income statement movement | Net file activity in accounts 4100–8000 versus the audited net loss | $21,400 net debit | 0 |
| T-4 Account-level movement | Opening balance plus file activity versus closing trial balance | 187 of 187 accounts agree | 0 |
| T-5 Bridge to the statements | NetSuite trial balance versus the statement trial balance in CONSOL_FY25_v14.xlsx | 27 top-sides, $6,200 absolute value | Explained in full |

T-3 is the test most teams skip and the strongest of the five, because it ties the file to a figure audited from the
other direction. Net file activity by range: revenue 4100–4210 $(148,200); cost of revenue 5100–5200 $38,940; operating
expenses 6100–6400 $133,500; interest income 7100 $(5,110); interest expense 7200 $1,340; other expense 7300 $390;
income taxes 8000 $540. Check the arithmetic: (148,200) + 38,940 + 133,500 + (5,110) + 1,340 + 390 + 540 = **21,400
debit**, the audited net loss. Had the file come to $21,340, you would have a $60 hole — trivial against the $72 clearly
trivial threshold but not in meaning, because a $60 gap means entries are missing and you do not know which or how many.

T-4 runs for every account and the workpaper carries the full schedule. Three representative rows:

**Exhibit 16-4. Account-level movement reconciliation, selected accounts (in thousands of USD).**

| Account | 12/31/2024 | Net FY2025 activity in the file | Computed closing | 12/31/2025 trial balance | Difference |
| --- | --- | --- | --- | --- | --- |
| 1700 Goodwill | 12,400 | 14,500 | 26,900 | 26,900 | — |
| 2500 Convertible senior notes, net | (169,900) | (700) | (170,600) | (170,600) | — |
| 3100 Additional paid-in capital | (351,600) | (60,700) | (412,300) | (412,300) | — |

Credits are in parentheses, and each movement is separately corroborated: $14,500 is the Kestrel goodwill allocation,
$700 the amortization of issuance costs, $60,700 the equity roll-forward tested in Chapter 9.

**What an unexpected result looks like.** A difference equal to one large round amount usually means the date filter
excluded an entry; re-request on a different date field. A difference equal to an account's full prior-year balance means
an opening-balance conversion or renumbering. A difference in exactly two accounts with opposite signs is a mapping
problem, not missing data. Resolve differences before designing any criterion — selections from an incomplete population
look identical to selections from a complete one.

## 16.4 Manual versus automated, and why the client's flag is not evidence

A **manual journal entry** is one whose amount, accounts, or existence was determined by a person rather than by a
configured process operating on transaction data; an **automated entry** is generated by an interface or a system schedule
without a person choosing either. The manual population is where override lives, and the selection exercise is scoped to
it.

NetSuite has no field called "manual." It has a source type (Exhibit 16-2) and a created-by user, and the client's 4,912
is the count of records whose source type is `Journal` and whose creator is a named user. Three things break that: a
person creating an entry under a service account (a manual entry labeled automated); a recurring template firing under a
named user (an automated entry labeled manual, which merely inflates the population); and — the dangerous case — a person
editing an interface-generated entry, which keeps the interface's source type and takes the editor's amount. Test the
flag's completeness with three queries and a matrix.

```sql
-- Test A: automated source type, creator is not a service account.
select l.source_type, l.preparer_id, count(distinct l.entry_no) as entries,
       sum(case when l.amount_rpt > 0 then l.amount_rpt else 0 end) as gross_debits
from   je_line l
join   dim_user u on u.user_id = l.preparer_id
where  l.source_type <> 'Journal'
  and  u.is_service_account = false
group by 1, 2 order by entries desc;

-- Test B: created by a service account, last modified by a named user.
select distinct l.entry_no, l.source_type, l.preparer_id, l.last_modified_by, l.last_modified_ts
from   je_line l
join   dim_user m on m.user_id = l.last_modified_by
where  l.preparer_id in (select user_id from dim_user where is_service_account)
  and  m.is_service_account = false;

-- Test C: scheduled interface journals by source and month, against expected frequency.
select source_type, date_trunc('month', posting_date) as period, count(distinct entry_no)
from   je_line where source_type like 'Journal — %' group by 1, 2 order by 1, 2;
```

**Exhibit 16-5. Manual-entry flag completeness test — results.**

| Test | Population examined | Exceptions | Disposition |
| --- | --- | --- | --- |
| A — automated source, human creator | 36,225 transaction-level entries | 41 | Reclassified as manual; all are `Invoice`-source entries created by two revenue accountants for off-cycle billings |
| B — service-account creator, human last modifier | 473 scheduled journals | 12 | 9 Stripe journals rebuilt by hand after Lambda failures; 3 I-3 journals with a line added before posting |
| C — expected versus actual scheduled journals | 12 source types | 0 | Monthly sources have 12 each; Stripe 365; payroll 36 |
| **Total reclassified as manual in substance** | | **53** | Criteria population becomes 4,965 |

The nine recreated Stripe journals are the instructive exception. The Lambda job (W-7) failed on three dates and the
Revenue Manager rebuilt the entries by hand from the Stripe dashboard; because they carry the interface's source type,
nobody reviewed them as manual entries — $1,240 of hand-built revenue postings the client called automated.

## 16.5 Designing selection criteria

A criterion is a hypothesis about how an inappropriate entry would look, expressed as a query. Write each one with the
risk it addresses, the query, and the expected hit count before you run it.

**Exhibit 16-6. The eight scoring criteria applied to the manual population, with weights and hit counts.**

| ID | Criterion | Risk addressed | Weight | Hits |
| --- | --- | --- | --- | --- |
| C1 | Prepared or posted by a user with a segregation-of-duties conflict | Override without a second party | 3 | 214 |
| C2 | Posted after the close cut-off for the period it affects | Adjustment made once the result was known | 4 | 61 |
| C3 | Header description blank or single-word | Concealment of purpose | 2 | 388 |
| C4 | Created on a weekend or after 8:00 p.m. local | Preparation outside supervision | 2 | 172 |
| C5 | Round-dollar amount of $100,000 or more | Estimated or plugged amount | 3 | 96 |
| C6 | Touches a revenue account with a non-standard offset | Revenue recorded outside the subledger | 5 | 34 |
| C7 | Uses an account with five or fewer manual entries in FY2025 | Accounts nobody reviews | 3 | 143 |
| C8 | Prepared by a user with an IT administrative role | Technical access used to post entries | 4 | 26 |
| | **Total criterion hits** | | | **1,134** |

The 1,134 hits fall on 902 distinct entries, so 232 hit more than one criterion — the overlap the §16.6 scoring model
exploits. C1 through C5 are one pass over the file at header grain:

```sql
with hdr as (
  select entry_no,
         min(posting_date)                                  as posting_date,
         min(entry_ts)                                      as entry_ts,
         min(preparer_id)                                   as preparer_id,
         max(coalesce(nullif(trim(description), ''), ''))   as description,
         sum(case when amount_rpt > 0 then amount_rpt end)  as gross_debits
  from   je_line
  where  is_manual_in_substance
  group by entry_no
)
select h.entry_no,
       case when u.sod_conflict then 3 else 0 end                             as c1,
       case when h.entry_ts > cc.cutoff_ts then 4 else 0 end                  as c2,
       case when h.description = '' or h.description !~ '\s' then 2 else 0 end as c3,
       case when extract(dow from h.entry_ts) in (0, 6)
             or extract(hour from h.entry_ts) >= 20 then 2 else 0 end          as c4,
       case when mod(h.gross_debits, 10) = 0
             and h.gross_debits >= 100 then 3 else 0 end                      as c5
from   hdr h
join   dim_user u  on u.user_id = h.preparer_id
join   close_cutoff cc on cc.period = to_char(h.posting_date, 'YYYY-MM');
```

Amounts are in thousands, so `gross_debits >= 100` is $100,000 and `mod(gross_debits, 10) = 0` a multiple of $10,000.
Run the test in transaction currency too: a £100,000 entry at 1.2680 is $126,800 and will not look round. That added 11
entries to the 96, tested separately. C6 and C7 need the chart of accounts:

```sql
-- C6: revenue entries with a non-standard offset. Standard offsets are the deferred revenue
-- and receivable accounts used by I-3 and the Zuora Billing feed.
select r.entry_no, sum(abs(r.amount_rpt)) as gross
from   je_line r
where  r.is_manual_in_substance
  and  r.account between '4100' and '4900'
  and  exists (
        select 1 from je_line o
        where  o.entry_no = r.entry_no
          and  o.account not between '4100' and '4900'
          and  o.account not in ('1200','1205','1220','2400','2405','2410','2230'))
group by r.entry_no;

-- C7: seldom-used accounts, defined from the manual population itself.
with usage as (
  select account, count(distinct entry_no) as n
  from   je_line where is_manual_in_substance group by account)
select l.entry_no, l.account, u.n
from   je_line l join usage u on u.account = l.account
where  l.is_manual_in_substance and u.n <= 5;
```

C6 returned 34 entries totaling $3,900. Six are the manual entries totaling $158 posted directly to revenue accounts in
December 2025 that Chapter 12 found when it tested the I-3 interface; two independent procedures reaching the same six
entries corroborates both.

### 16.5.1 Criteria that select nothing and criteria that select everything

**Exhibit 16-7. Candidate criteria rejected or recalibrated, with the reason.**

| Candidate criterion | Hits | Disposition |
| --- | --- | --- |
| No evidence of a second approver (W-12) | 3,847 | Rejected: 78.3% of the population. Kept as a control observation, quantified in §16.11 |
| Blank or single-word description, any amount | 388 | Retained at weight 2; 7.9% is a workable rate |
| Posted on December 31 after 11:00 p.m. | 0 | Rejected: the December cut-off is January 9, so the risk window is in January |
| Entries to account 1700 (goodwill) by a non-Controller | 0 | Rejected: the account had two entries all year |
| Amount over $940 (performance materiality) | 1,881 | Recalibrated: value alone is not a fraud indicator where treasury entries are largest. Kept for stratification |
| Preparer left the company during FY2025 | 3 | Retained outside the model, tested 100% |

A zero-hit criterion is not wrong, but it is not evidence either. Ask whether the zero means the risk is absent or the
criterion is misspecified. The December 31 criterion returned zero for the second reason — "late" was defined wrongly for a
company whose books stay open until January 9 — and rewritten against the close calendar it became C2 with 61 hits. The
goodwill criterion returned zero for the first, which is legitimate negative evidence.

## 16.6 Scoring and stratifying

When criteria overlap, ranking by score concentrates work on entries that look wrong in more than one way. Weight each
criterion 2 to 5 by how strongly it discriminates — C6 at 5 because a manual revenue entry with a non-standard offset has
almost no legitimate explanation in a company with a revenue subledger; C3 and C4 at 2 because thousands of legitimate
entries have terse descriptions and busy people work at night. State the alternative: an unweighted count would move 19
entries into or out of the top stratum.

**Exhibit 16-8. Score distribution over the 902 entries hitting at least one criterion.**

| Score | Entries | Weighted points |
| --- | --- | --- |
| 2 | 331 | 662 |
| 3 | 268 | 804 |
| 4 | 149 | 596 |
| 5 | 68 | 340 |
| 6 | 42 | 252 |
| 7 to 14 (24 at 7, 12 at 8, 5 at 9, 2 at 10, 1 at 14) | 44 | 343 |
| **Total** | **902** | **2,997** |

The points cross-check to Exhibit 16-6: (214 × 3) + (61 × 4) + (388 × 2) + (172 × 2) + (96 × 3) + (34 × 5) + (143 × 3) +
(26 × 4) = 2,997. Disagreement means an entry was double-counted, usually because a multi-line entry hit a line-grain
criterion twice.

**Exhibit 16-9. Selection schedule, FY2025 journal entry testing (WP 3200-12).**

| Stratum | Population | Selection basis | Selected |
| --- | --- | --- | --- |
| A — score 6 or higher | 86 | 100% | 86 |
| B — post-close (C2), scoring exactly 4 on a single hit | 18 | 100% | 18 |
| C — score 4 or 5, excluding stratum B | 200 | Random, seed documented | 25 |
| D — score 2 or 3 | 598 | Random, seed documented | 10 |
| E — manual entries hitting no criterion | 4,051 | Random, seed documented | 15 |
| F — reclassified as manual in substance (§16.4), at least one hit | 12 | 100% | 12 |
| G — consolidation top-sides outside NetSuite (§16.8) | 27 | 100% | 27 |
| **Total** | **4,992** | | **193** |

Strata A through F sum to the 4,965-entry manual-in-substance population; stratum G never touched NetSuite. Stratum E
tests the criteria rather than the entries: if the residual produces a finding, the criteria are misspecified. Fifteen
items cannot prove the residual clean, so claim only that no evidence of misspecification was identified. Stratum D
serves unpredictability.

## 16.7 Testing a selected entry

Every selected entry is tested against the same four attributes. Obtain the support before asking the preparer what the
entry was for, so the explanation is corroborated rather than adopted.

**Exhibit 16-10. Attribute testing grid — four attributes and the evidence that satisfies each.**

| Attribute | What satisfies it | What does not | Failure response |
| --- | --- | --- | --- |
| Support | The calculation, invoice, contract, or model from the system of record, reconciled to the entry to the dollar | A spreadsheet retyped from the entry; a screenshot; a task with no attachment | Request the source document; if none exists, the entry is unsupported |
| Business purpose | An explanation a person outside accounting would accept, consistent with the support and the economics | "To true up the accrual"; "per Elena"; the description field | Inquire of the preparer and one person outside finance; document both |
| Authorization | A competent person independent of the preparer reviewed the entry and its support before posting, precisely enough to catch a misstatement | Approval four minutes after posting; approval by the preparer's report; one sign-off covering 40 entries | Record a deviation, evaluate severity, extend substantive work |
| Accounting conclusion | The answer US GAAP requires, re-performed by you, period tested separately from amount | Agreement to management's memo or to last period's treatment | Quantify and accumulate the misstatement; consider bias |

The attributes fail independently, and the most common combination — this chapter's case study — is a correct accounting
conclusion with a failed authorization. Collapsing the grid into one "appropriate? Y/N" column loses that finding: the
accounting was right and the column says Y.

## 16.8 The entries that are not in the general ledger

Two populations sit outside NetSuite, and both are inside the requirement.

**Consolidation top-side entries.** AtlasFlow consolidates in CONSOL_FY25_v14.xlsx, a workbook with no version control,
no formula-integrity check, and four people emailing it (W-8). FY2025 contains 27 top-side entries with $6,200 of
absolute value. Obtain them as a schedule — entry number, date, preparer, accounts, amounts, purpose — then agree the
schedule to the workbook's adjustment columns and the workbook's consolidated trial balance to the statements.

**Exhibit 16-11. Consolidation top-side entry population, FY2025 (in thousands of USD).**

| Type | Count | Absolute value | Tested |
| --- | --- | --- | --- |
| Intercompany revenue and expense elimination | 8 | 2,140 | 8 |
| Intercompany receivable and payable elimination | 6 | 1,780 | 6 |
| Translation adjustment and FX true-up (ASC 830-30) | 5 | 1,490 | 5 |
| Reclassification between statement captions | 4 | 480 | 4 |
| Consolidated-only accruals | 3 | 260 | 3 |
| Deferred tax and valuation allowance | 1 | 50 | 1 |
| **Total** | **27** | **6,200** | **27** |

Test all 27: the population is small, its control environment is the company's weakest, and the preparers have the most
complete view of the consolidated result. Four procedures matter here that do not in NetSuite — agree each elimination to
both sides of the intercompany balance, so the eight revenue eliminations remove the same amount from the parent's revenue
and the component's expense; recompute the translation entries at the §3.4 rates (1.2680 USD/GBP, 0.6410 USD/AUD, 0.01172
USD/INR); confirm no top-side has a one-sided income statement effect; and confirm the adjustment column equals the sum of
the 27 with no plug.

**Subledger entries in Zuora Revenue.** Interface I-3 delivers one summary journal a month — twelve entries totaling
$112,300 — but everything determining those amounts happens in the subledger, whose FY2025 adjustment log holds 1,847
manual contract-level adjustments that never appear as a NetSuite entry and that general ledger criteria cannot reach.
Reconcile the twelve journals to the RevPro "Revenue Contract Summary" totals, stratify the log by reason code, test 100%
of the codes permitting a manual revenue override, and check whether the four local administrator accounts (W-1) appear
among the adjusters — they do, on 61 adjustments totaling $780 under the shared `revpro_admin` credential, so those 61
fail authorization automatically.

## 16.9 Completeness of period-end adjusting entries

The §16.5 criteria find entries that exist; they cannot find an entry that should have been made and was not. For that,
work from the close calendar: obtain the December FloQast checklist — 148 tasks, 62 expected to produce an entry — match
each of the 62 to an entry by number, and investigate every task with a sign-off and no entry.

**Exhibit 16-12. Close-calendar completeness test, December 2025 close (WP 3200-19).**

| Result | Tasks | Disposition |
| --- | --- | --- |
| Entry located; amount agrees to the task's support | 55 | No exception |
| Entry located; amount differs from the support | 3 | Two revised after review with the revision documented; one is the $41 R&D/G&A misclassification in §16.11 |
| Signed off, no entry required; nil balance corroborated | 3 | No exception |
| Signed off, no entry posted although a balance existed | 1 | Exception: the UK indirect-tax true-up, the $180 accrued VAT understatement (C-4) |
| **Total tasks expected to produce an entry** | **62** | |

Coverage: 61 of 62 tasks produced an entry, and the single failure produced a $180 misstatement management corrected. This
is the only procedure in the chapter capable of finding an omitted accrual, and it works because a signed-off task with no
entry is a contradiction inside management's own records.

**When the calendar itself is incomplete.** No task exists for AtlasFlow's service-level-agreement credit accrual, which
is how the $290 in corrected misstatement C-2 escaped. A missing task is a design deficiency in the close process, and
the conclusion must say so rather than reporting 62 of 62.

## 16.10 Reversals and how to read them

The reversal flag is the most misread field in the file. AtlasFlow's manual population contains 1,204 flagged records,
24.5% of the population — not a red flag but what accrual accounting looks like, because every reversing accrual
generates two flagged records. Screen on the pattern instead.

**Exhibit 16-13. Reversal analysis of the manual population, FY2025.**

| Pattern | Count | Interpretation and action |
| --- | --- | --- |
| Accrual reversed next month, same template, same amount, opposite sign | 1,046 | Routine; confirm the pairing exists |
| Accrual reversed next month at a different amount | 98 | Estimate revision: 61 reduced expense, 37 increased it — a 62/38 split supporting a bias inquiry but not a conclusion |
| Entry reversed within five business days by a different user | 37 | Investigate all 37; 34 were keying corrections, 3 re-posted to a different account |
| Entry reversed after the period it affected was reported | 14 | Investigate all 14; the highest-value reversals in the file |
| Future reversal date set on a non-accrual entry | 9 | Investigate all 9 — the case study pattern, a permanent adjustment set to auto-reverse |
| **Total flagged records** | **1,204** | |

Memorize the last row. NetSuite lets a preparer set a reversal date at creation and a copied entry inherits it, so a
permanent adjustment silently undoes itself in the next period. Nine existed in FY2025, one for $1,340.

## 16.11 Whole-population analysis, sampling, documentation, and the sufficiency conclusion

Journal entry testing is not sampling, and calling it sampling in the workpaper creates a problem you do not need. Every
criterion runs against 100% of the population, so the criterion-driven strata carry no sampling risk; their risk is that
the criteria do not describe how an inappropriate entry would look, which more testing within the same criteria does not
reduce — only a differently-shaped criterion, the residual stratum, and the flag-completeness test do. Strata C, D, and E
are non-statistical samples supporting no projection.

**Exhibit 16-14. Results of testing 193 selected entries and adjustments (WP 3200-14).**

| Result | Count |
| --- | --- |
| Support, purpose, review, and accounting all satisfied — no exception | 129 |
| Accounting appropriate; no evidence of independent review before posting (deviation) | 45 |
| Accounting appropriate; description inadequate or support not retained | 14 |
| Classification misstatement identified | 4 |
| Support not provided on request; escalated and later obtained | 1 |
| **Total selected** | **193** |

Of the 193, 88 were close-calendar entries whose FloQast sign-off identified the specific entry, accepted as review
evidence; 60 carried an approver ID corroborated by inquiry; 45 had neither. The 23.3% is consistent with W-12 in
direction but far below its 78.3%, because scoring selects toward the larger entries the threshold catches. The
population rate is W-12's.

The four classification misstatements total $103 with no effect on the net loss: $62 recorded to 4100 (Core) belonged in
4110 (Insight), affecting the revenue disaggregation disclosure, and $41 recorded to 6100 (R&D) belonged in 6300 (G&A).
Each is individually below the $72 clearly trivial threshold and above it in aggregate; both were corrected and
accumulated rather than waived, because a small classification error can still matter to a disclosure.

**Quantifying the exposure.** The 3,847 entries below the approval threshold carry $46,300 of absolute value and the
1,065 above it carry $94,600, together the $140,900 manual population. Since the threshold is $250,000, no single
unreviewed entry can be material alone; the exposure is aggregation — $46,300 of gross posting activity, 49 times
performance materiality, with no independent review. That is the computation Chapter 14's severity evaluation needs.

**Documentation.** AS 1215 requires that an experienced auditor with no previous connection to the engagement follow the
work: retain the extract, the request and the eleven answers, the file name and row count and receipt date, the Exhibit
16-3 reconciliations, the queries as executed with their seeds, each criterion's weight and hit count, the selection
schedule, and the testing grid for every item. A file documenting selections but not the population documents the least
important part of the work.

**The sufficiency conclusion.** Never let it be broader than the population you proved:

```text
Conclusion. We obtained the complete FY2025 NetSuite journal entry population (41,610 entries, 118,442
lines, $1,842,300 of debits), established its completeness by reconciling income statement activity to the
audited net loss of $21,400 and account-level activity for 187 of 187 accounts to the trial balance, and
bridged the NetSuite trial balance to the financial statements through the 27 consolidation top-side
entries, all of which we tested. We reclassified 53 entries the client had called automated into the manual
population, applied eight risk-based criteria to the resulting 4,965 entries, and tested 193 entries and
adjustments, identifying four classification misstatements aggregating $103, all corrected, and no
misstatement affecting the net loss. We identified 45 entries with no evidence of independent review before
posting, corroborating W-12; severity is evaluated at WP 4100-30. Subject to that control conclusion, the
procedures required by AS 2401 have been performed and we identified no evidence of material misstatement
due to fraud arising from journal entries and other adjustments.
```

## 16.12 The seven data pitfalls

Each produces a wrong conclusion invisibly: the output looks reasonable.

**Exhibit 16-15. Data pitfalls in journal entry analysis, with the symptom and the fix.**

| Pitfall | Symptom | Fix |
| --- | --- | --- |
| Multi-line entries | One entry counts as 4.5 hits; the largest "entry" is a 340-line allocation | Test at header grain; report line results as line counts |
| Header versus line grain | Counts that will not reconcile; a score total that will not cross-foot | Build both views once, label every number, reconcile them |
| Sign conventions | Credits appear as positives, so a revenue-debit criterion returns all revenue | Confirm the convention on a known entry first |
| Statistical accounts | Counts inflate while debits still equal credits, so nothing looks wrong | Identify and exclude them, disclosing the exclusion |
| Intercompany accounts | Eliminations look like one-sided postings, generating false positives | Analyze separately, pairing each posting to its counterpart |
| Currency fields | Value criteria behave differently in three amount columns | Run in transaction and reporting currency; test the delta |
| Entries netting to zero at the header | A $2,400 gross entry with offsetting lines escapes every value criterion | Write criteria on gross debits: 138 manual entries exceeded $250,000 gross with no line above $100,000 |

## Step-by-Step Walkthrough: Obtaining, Validating, and Analyzing the FY2025 NetSuite Journal Entry Population

Performed by Tara Iyer (data and analytics) with Chris Nwosu, January 14–30, 2026. Workpaper series WP 3200.

**Step 1.** Define the population in writing before requesting anything: all entries and adjustments affecting the FY2025
consolidated financial statements, all five entities, posted in NetSuite through the February 20, 2026 report date, plus
all adjustments in CONSOL_FY25_v14.xlsx. Compare the definition to the statement caption list; two captions are produced
outside NetSuite, so the definition must reach them.

**Step 2.** Issue the Exhibit 16-1 request with the format specification and the trial balance at both period ends from
the same system, on a five-business-day deadline. Decline a report the client already runs for management: those are
filtered and you cannot see the filter.

**Step 3.** Sit with the administrator while the saved search runs, screenshot the definition including every filter and
the date field, and ask the eleven questions in §16.2. The answer that mattered: the search filtered on posting date, so
January 2026 postings to the December 2025 period were included, which you want, and 29 FY2025 postings to the December
2024 period were too, which you do not. Those 29 were excluded.

**Step 4.** Validate mechanically: 118,442 rows against the control page, 41,610 distinct entry numbers, posting dates
inside FY2025, no null account, amount, or entry number, no duplicated (entry number, line number) pair.

**Step 5.** Establish the grain. The file is line grain: 2.85 lines per entry overall, and 22,180 lines belong to the
4,912 manual entries at 4.5 lines each. Build a header view and label every count with its grain.

**Step 6.** Prove the file balances: debits $1,842,300 against credits $1,842,300 at both grains and by subsidiary, then
test the balance within each entry. At AtlasFlow 41 entries balanced only in reporting currency, which is correct for a
multi-currency entry and is documented rather than treated as an error.

**Step 7.** Run the income statement reconciliation: net activity in accounts 4100 through 8000 is a $21,400 debit,
agreeing to the audited net loss. If it does not agree, stop — the likely causes are an excluded period, excluded
statistical accounts, or the omitted year-end closing entry.

**Step 8.** Run the account-level reconciliation for all 187 active accounts: opening balance plus net file activity
equals the closing trial balance, 187 of 187 agreed. This is the workpaper a reviewer asks for when they ask how you know
the population was complete.

**Step 9.** Bridge the NetSuite trial balance to the financial statements through the 27 top-side entries. An unexplained
residual is the walkthrough's most serious result: figures are then created between the ledger and the statements by a
mechanism nobody has described to you.

**Step 10.** Enumerate every source type and preparer and build the source-by-preparer matrix. Twelve source types
appeared, three absent from the interface documentation. Notify the IT audit team: an undocumented interface is untested.

**Step 11.** Test the manual flag with Tests A, B, and C: 53 entries reclassified as manual in substance, a population of
4,965. If Test A returns hundreds of exceptions, the source type field is not a manual indicator and you must build the
classification from service-account status yourself.

**Step 12.** Calibrate before scoring. Run each candidate, compare its hit count to your pre-run expectation, and dispose
of the misfires (Exhibit 16-7): the December 31 criterion returned zero and, rewritten against the January 9 cut-off,
returned 61.

**Step 13.** Run the eight criteria: 1,134 hits on 902 distinct entries. Cross-check the weighted point total from the
criterion counts and from the score distribution and confirm both equal 2,997.

**Step 14.** Stratify and select per Exhibit 16-9: 193 items — 86 scoring 6 or higher, 18 single-hit post-close entries,
50 random selections with documented seeds, 12 reclassified entries, and 27 top-sides. Issue one support request listing
entry number, date, amount, and preparer, with a deadline and named escalation.

**Step 15.** Test each item against the four attributes, aggregate the results (Exhibit 16-14), accumulate the four
classification misstatements totaling $103, quantify the review-evidence exposure at $46,300, and draft the §16.11
conclusion. Support never provided for a selected item is a scope matter for the engagement partner and the audit
committee, not an exception noted in a table.

## Extended Case Study: The $1,340 Entry Described as "Reclass"

### Background

The scoring model produced one entry with a score of 14, the highest in the population. JE-14962 was posted January 12,
2026 at 21:14 Central, effective December 31, 2025, for $1,340, description "reclass," no reference, no attachment,
prepared and posted by Controller Elena Vasquez and approved by CFO Tom Okafor at 21:18 — four minutes later. It hit C1
(preparation-and-posting conflict, W-13), C2 (after the January 9 cut-off), C3 (single-word description), C4 (after 8:00
p.m.), and C5 (round amount above $100,000).

### The Facts

The entry had five lines: a $1,340 debit to account 3100 (additional paid-in capital) and credits of $620 to 6100
(research and development), $340 to 6300 (general and administrative), $300 to 6200 (sales and marketing), and $80 to
5110 (cost of subscription — personnel), footing to $1,340.

Two attributes made it look like something it was not. The reversal flag was Y with a reversal date of January 1, 2026,
and the audit trail showed it had been created with NetSuite's "make copy" function from JE-14203, the November reversal
of the usage-overage revenue accrual — the source of the description, the inherited reversal date, and its filing in
FloQast against close task R-118, "reverse November usage overage accrual." From the data alone, the first hypothesis was
a $1,340 revenue accrual reversed after the close.

### What the Engagement Team Did

The team requested support before interviewing the preparer. What came back was a tab from the stock compensation
workbook: the entry was the catch-up credit from revising the probability of the 2025 annual-recurring-revenue-based
performance stock unit (PSU) tranche from 100% to 85%. Jae-won Park re-performed it from the Carta grant extract — 262
thousand units at a $34.10 grant-date fair value is $8,934; the service period ended December 31, 2025, so cumulative
expense at 100% probability was $8,934 and at 85% is $7,594, a $1,340 credit — and traced the allocation to the PSU
holders' departments.

### Analysis

Attribute by attribute, using Exhibit 16-10:

| Attribute | Conclusion | Basis |
| --- | --- | --- |
| Support | Satisfied, late | Reconciles to the entry to the dollar, but not attached and located only on request |
| Business purpose | Satisfied | ASC 718-10-25 requires accrual on the probable outcome; the revision is supported by the November 14, 2025 revised ARR forecast |
| Authorization | **Failed** | Approval four minutes after posting, no support held, and the approver recalled only being asked to "approve the equity entry." Nothing in the review would have caught an error in amount, period, or accounts |
| Accounting conclusion | Satisfied for the annual amount | Re-performed. The equity workpapers separately concluded $240 of the revision belonged in the third quarter, which management corrected (C-5) |

Neither the description nor the inherited reversal date is cosmetic. With the reversal date still set on a permanent
adjustment, the $1,340 credit would have reversed into January 2026, debiting expense with no entry, no preparer, and no
review — a next-period misstatement $400 above performance materiality, manufactured by a control failure in this period.
And because the entry was filed against a revenue close task, the reviewer of equity entries never saw it.

The team then quantified the practice rather than the instance: 1,880 of the 4,912 manual entries (38.3%) were created with
the copy function, 61 retained the copied description, and 9 retained an inherited reversal date on a non-accrual entry.
The single entry is an anecdote; the 1,880 and the 9 are the finding.

### Resolution and Conclusion

Management removed the reversal date on February 2, 2026; the team inspected January 2026 activity in accounts 3100, 5110,
6100, 6200, and 6300 and confirmed no reversal posted. The description could not be amended after posting, so management
documented the purpose in FloQast and re-filed the entry against the equity close task. No misstatement of the FY2025
annual financial statements arose.

The control conclusion is worse: approval applied without support, four minutes after posting, by a person who could not
describe what he had reviewed, over an entry prepared and posted by the Controller (W-13). With W-12 and the 45 entries
lacking review evidence, this is at minimum a significant deficiency in the period-end reporting process; aggregation and
the material weakness determination belong to Chapter 14.

### Workpaper Extract

```text
BRIGHTLINE LLP                                                              WP 3200-14.7
AtlasFlow, Inc. — FY2025 integrated audit
JOURNAL ENTRY TESTING — ENTRY JE-14962

Prepared by:  J. Park (JP)          Date: 1/27/2026
Reviewed by:  C. Nwosu (CN)         Date: 1/29/2026
2nd review:   G. Lindqvist (GL)     Date: 2/3/2026

PURPOSE
To test the appropriateness of JE-14962 (support, purpose, authorization, accounting conclusion)
as required by AS 2401. Selected in stratum A of WP 3200-12 at a score of 14 (C1-C5), the
highest in the FY2025 manual population.

SOURCE OF INFORMATION
(a) NS_JE_FY25_20260114.txt, 118,442 lines, reconciled at WP 3200-04.
(b) NetSuite audit trail for JE-14962, screenshot 1/26/2026; FloQast close task R-118.
(c) SBC_PSU_Q4_2025.xlsx tab "ARR PSU catch-up"; Carta grant extract at 12/31/2025
    (WP 5100-11); revised ARR forecast 11/14/2025.
(d) Inquiries of E. Vasquez 1/26/2026 and T. Okafor 1/27/2026.

ENTRY AS POSTED (USD thousands; effective 12/31/2025; entered 1/12/2026 21:14 CT)
  Dr 3100 Additional paid-in capital                            1,340
  Cr 5110 Cost of subscription - personnel                              80
  Cr 6100 Research and development                                     620
  Cr 6200 Sales and marketing                                          300
  Cr 6300 General and administrative                                   340
  Description: "reclass"   Reference: blank   Attachments: 0
  Reversal flag: Y   Reversal date: 1/1/2026   Created by copy of JE-14203

PROCEDURES PERFORMED AND RESULTS
1. Re-performed the amount from source (c):
     262 units x $34.10 GDFV                        = 8,934  (a)
     Cumulative expense at 100% probability          = 8,934  (service period ended 12/31/2025)
     Cumulative expense at 85% probability           = 7,594  (8,934 x 0.85)
     Catch-up credit required                        = 1,340  (b)
   Agrees to the entry. No difference.
2. Purpose corroborated to the 11/14/2025 revised ARR forecast and Q4 probability memo;
   consistent with ASC 718-10-25. Satisfied.
3. Authorization: approval by T. Okafor 1/12/2026 21:18 CT, 4 minutes after posting, no support
   attached, approver could not describe what he reviewed. CONTROL DEVIATION - see WP 4100-30.
4. Reversal date 1/1/2026, inherited from JE-14203, would have reversed a permanent adjustment
   into Q1 2026 ($1,340 against $940 performance materiality). Removed by management 2/2/2026;
   January 2026 activity in 3100/5110/6100/6200/6300 inspected, no reversal. (c)
5. Practice quantified: 1,880 of 4,912 manual entries created by copy, 61 retaining the copied
   description and 9 an inherited reversal date (WP 3200-16).

TICK MARK LEGEND
(a) Agreed to Carta grant extract, WP 5100-11.  (b) Recomputed by JP, no difference.
(c) Agreed to NetSuite screenshot 2/2/2026 and the January 2026 trial balance.

CONCLUSION
The accounting conclusion and amount are appropriate and no misstatement of the FY2025 annual
financial statements arises from this entry. Its authorization was not effective and its
description and retained support were inadequate. The deviation is reported to WP 4100-30 for
severity evaluation with W-12 and W-13. The inherited-reversal condition affected 9 entries and
has been communicated to management in writing.
```

### Lessons

1. An entry can be right and still be a control failure; authorization failed here on an entry approved in four minutes.
2. The data will mislead you about what an entry is. Description, reversal flag, and close task all pointed at a revenue
   accrual reversal; only the support identified it.
3. Convert the instance into a population: the workpaper's value is the 1,880 copied entries and the 9 inherited reversal
   dates, not the one entry that scored 14.

## Common Mistakes

### Mistake 16.1 — Taking the manual-entry flag at face value

**What it looks like.** "Obtained the population of 4,912 manual entries per the client's extract," then criteria.
**Why it happens.** The field's name is plausible and testing it requires understanding service accounts.
**What goes wrong.** The flag was wrong by 53 entries, including nine hand-built Stripe revenue journals of $1,240.
**How to avoid it.** Run Tests A, B, and C in §16.4 and reconcile scheduled journal counts to interface frequency.

### Mistake 16.2 — Selecting entries before reconciling the population

**What it looks like.** Criteria run in week one; the reconciliation drafted in week four, if at all.
**Why it happens.** Selection feels like progress, and support requests have long lead times.
**What goes wrong.** If the reconciliation later fails, every selection came from an unknown population.
**How to avoid it.** Treat Exhibit 16-3 as a gate: no criterion runs until T-1 through T-5 are signed.

### Mistake 16.3 — Mixing header and line grain

**What it looks like.** 388 blank descriptions at line grain reported beside 4,912 header-grain entries.
**Why it happens.** The extract arrives at line grain and nobody labels which grain a number uses.
**What goes wrong.** Manual entries average 4.5 lines, so hits overstate fourfold and the score stops cross-footing.
**How to avoid it.** Build a header view immediately, label every count, run the Exhibit 16-8 cross-check.

### Mistake 16.4 — Using the approval threshold as a selection criterion

**What it looks like.** A criterion "no second approver" returning 3,847 items, then a selection of 25.
**Why it happens.** The condition is real, easy to query, and feels like the biggest risk in the file.
**What goes wrong.** Selecting 78.3% discriminates nothing, and the real finding is buried rather than quantified.
**How to avoid it.** Estimate the hit count first; above roughly 15% of the population it is a finding, not a filter.

### Mistake 16.5 — Defining the population as the general ledger extract

**What it looks like.** "Population: all FY2025 journal entries per NetSuite."
**Why it happens.** The requirement is remembered as being about journal entries; "other adjustments" drops out.
**What goes wrong.** The 27 top-sides and 1,847 Zuora Revenue adjustments are excluded — the populations with the weakest
controls and the shortest route to the reported result.
**How to avoid it.** Build the population backwards from the financial statement captions.

### Mistake 16.6 — Substituting a control test for examining the entries

**What it looks like.** A sample of 25 entries tested for evidence of approval, cited as the AS 2401 procedure.
**Why it happens.** The control test is already in the ICFR program and appears to cover the same population.
**What goes wrong.** It answers whether an approver ID is populated, not whether the entry was appropriate.
**How to avoid it.** Keep two procedures and two workpapers, cross-referencing deviations.

### Mistake 16.7 — Running amount-based criteria only in the reporting currency

**What it looks like.** A round-amount criterion applied to the USD column of a four-currency ledger.
**Why it happens.** The reporting column is the one that ties to the financial statements.
**What goes wrong.** A £100,000 entry at 1.2680 is $126,800 and passes; the transaction-currency run surfaced 11 misses.
**How to avoid it.** Run amount criteria in both columns, score on one, test the extra items the other surfaces.

### Mistake 16.8 — Accepting the description as the business purpose

**What it looks like.** A grid whose business purpose column reads "to reclass accrual per description."
**Why it happens.** The description is present, free, and reads like an explanation.
**What goes wrong.** It is unverified and blank or single-word in 388 cases. JE-14962's description pointed at a revenue
accrual; the entry was a stock compensation catch-up credit.
**How to avoid it.** Corroborate purpose against support and one person outside accounting; a description contradicting
support is itself a finding.

### Mistake 16.9 — Screening on the reversal flag rather than the pattern

**What it looks like.** A criterion "reversal flag = Y" returning 1,204 entries and a conclusion that the client reverses
unusually often.
**Why it happens.** The field is binary and available.
**What goes wrong.** Accruals generate two flagged records each, so the flag selects 24.5% of the population while the
nine anomalous items stay invisible inside it.
**How to avoid it.** Pair reversals to originals on entry, amount, and account, classify by pattern (Exhibit 16-13), and
test the anomalous classes at 100%.

### Mistake 16.10 — Projecting a risk-based selection's deviation rate onto the population

**What it looks like.** "45 of 193 entries tested lacked evidence of review, a 23.3% deviation rate."
**Why it happens.** Rates computed from tested items look like population rates.
**What goes wrong.** Selection was biased toward larger, high-scoring entries, so 23.3% understates the 78.3% population
condition threefold.
**How to avoid it.** Compute population conditions from all 4,912 entries and report tested-item results as such.

## Practice Exercises

### Exercise 16-1 — Population arithmetic [Foundational]

The extract contains 41,610 entries and 118,442 lines with $1,842,300 of debits; automated sources account for 36,698
entries and $1,701,400; manual entries occupy 22,180 lines. Compute the manual entry count and absolute value, average
lines per manual and per automated entry, and average absolute value per manual entry.

### Exercise 16-2 — Manual or automated [Foundational]

Classify each as manual in substance, automated, or requiring inquiry, and name the §16.4 test that finds it: (a) source
`Journal — Stripe daily summary`, creator `svc_stripe_lambda`, last modified by `jpike`; (b) source `Invoice`, creator
`abello`; (c) source `Journal`, creator `svc_netsuite_integration`, 12 identical entries, one per month; (d) source
`Journal — payroll`, creator `svc_adp`, unmodified; (e) source `Journal`, creator `revpro_admin` (shared credential).

### Exercise 16-3 — Income statement completeness reconciliation [Intermediate]

A first-draft extract shows net FY2025 activity of $(148,200) revenue, $38,940 cost of revenue, $133,500 operating
expenses, $(5,110) interest income, $1,340 interest expense, and $390 other expense. The audited net loss is $21,400.
Compute the file's net activity and the difference, identify the account most likely excluded, and state your next step.

### Exercise 16-4 — Scoring [Intermediate]

Using the Exhibit 16-6 weights, score each entry and state its Exhibit 16-9 stratum. P: conflicted preparer, blank
description, $340. Q: posted after the cut-off, uses account 1700 (2 manual entries all year), $180. R: posted Saturday
10:00 p.m., exactly $500,000, prepared by an IT administrator. S: credits 4110 with an offset to 6300, conflicted
preparer, posted after the cut-off. T: description "adjustment," $47.

### Exercise 16-5 — Criteria calibration [Intermediate]

Four candidates return these hit counts against the 4,965-entry population: (a) attachment count of zero — 4,118; (b)
posted December 31 after 11:00 p.m. — 0; (c) entries to account 2600 — 1; (d) absolute value above $940 — 1,881. For
each, state whether you retain it as a scoring criterion, convert it, or reject it, and why.

### Exercise 16-6 — Top-side population [Advanced]

The workbook schedule lists 27 entries: 8 intercompany revenue and expense eliminations ($2,140), 6 balance eliminations
($1,780), 5 translation entries ($1,490), 4 caption reclassifications ($480), 3 consolidated-only accruals ($260), and 1
deferred tax adjustment. The Controller states the population totals $6,200. Compute the deferred tax amount, state two
procedures testing whether the 27 are complete, and state what would contradict the Controller.

### Exercise 16-7 — Find the errors [Intermediate]

Identify four defects: "We obtained the client's listing of 4,912 manual journal entries and selected 40 entries using
our firm's high-risk criteria, representing 0.8% of the population. All 40 were approved in NetSuite and agreed to
management's supporting schedules. Based on our sample, we conclude that manual journal entries were appropriate and
that the population of journal entries is complete. Sampling risk was assessed as low."

### Exercise 16-8 — Draft a sufficiency conclusion with an unresolved difference [Advanced]

The account-level reconciliation agrees for 186 of 187 accounts. Account 2200 shows opening $5,900 plus net file activity
$440 against a closing trial balance of $6,400 — a $60 difference the client cannot explain by the report date. Overall
materiality is $1,450 and the clearly trivial threshold is $72. Draft the conclusion paragraph.

### Exercise 16-9 — Extend the data request [Intermediate]

The first extract has one amount column labeled "Amount," no time component on any date, and no last-modified fields, and
the administrator mentions that "about a quarter of the manual entries come in through CSV import." Draft the follow-up:
the fields to add with the reason for each, and three questions to answer before the re-run.

### Exercise 16-10 — Interpreting revised accruals [Advanced]

Of 98 accruals reversed at a different amount, 61 reduced expense by an aggregate $1,240 and 37 increased expense by
$410. Performance materiality is $940. State what the pattern does and does not support, what further information you
would obtain, and two conclusions a reasonable auditor could reach.

### Exercise 16-11 — Data reliability and the extract [Advanced]

Chapter 11 concluded that 11 users retained the legacy NetSuite "Full Access" role for 27 days after the September 2025
upgrade (W-2), and Chapter 12 identified six manual entries totaling $158 posted directly to revenue accounts in December
2025. State whether the saved-search extract can be relied on as IPE, the additional procedures you would perform, and
how your answer changes if the six entries had aggregated $1,580.

### Exercise 16-12 — Close-calendar completeness [Intermediate]

Of 62 close tasks expected to produce an entry, 55 matched an entry agreeing to the attached support, 3 matched with an
amount differing from the support, 3 were signed off as requiring no entry with the nil balance corroborated, and 1 was
signed off with no entry posted where a $180 balance existed. Compute the match and exception rates, state the
misstatement, and state one limitation of the test.

## Solutions to Practice Exercises

### Solution 16-1

(a) **4,912**. (b) **$140,900**. (c) Manual 22,180 ÷ 4,912 = **4.51 lines**; automated 96,262 ÷ 36,698 = **2.62 lines**.
(d) $140,900 ÷ 4,912 = **$28,690**. Manual entries are more complex and smaller than automated ones, which is why
value-weighted selection finds treasury mechanics.

### Solution 16-2

(a) Manual in substance — Test B; the nine rebuilt Stripe journals. (b) Manual in substance pending inquiry — Test A; the
41 such entries were off-cycle billings. (c) Automated — Test C confirms 12 of 12; still inspect for post-generation
editing. (d) Automated — Test C, no exception. (e) Manual, and the preparer cannot be identified because `revpro_admin` is
shared among six people (W-1), so it fails authorization automatically.

### Solution 16-3

(148,200) + 38,940 + 133,500 + (5,110) + 1,340 + 390 = **$20,860 debit**, **$540** short of the audited net loss —
exactly account 8000, income taxes, most likely excluded by an extract filter. Re-request, and run no criterion until the
difference is zero: you cannot know whether the missing $540 is tax entries or something else.

### Solution 16-4

P: C1 (3) + C3 (2) = **5**, stratum C. Q: C2 (4) + C7 (3) = **7**, stratum A. R: C4 (2) + C5 (3) + C8 (4) = **9**, stratum
A. S: C6 (5) + C1 (3) + C2 (4) = **12**, stratum A and the worst profile in the set. T: C3 (2) = **2**, stratum D; $47
does not meet the round-amount threshold.

### Solution 16-5

(a) 82.9% — reject, and convert into a quantified finding on attachment discipline; a usable refinement is "no attachment
and absolute value above $250,000." (b) Zero from a misspecified criterion: the December risk window runs through the
January 9 cut-off, and redefined it becomes C2 with 61 hits. (c) One hit — test it outside the model; account 2600 is a
$2,500 fair-value balance whose only entry is significant by definition. (d) 37.9% — reject; use value as a stratification
variable, because size here tracks treasury activity, not risk.

### Solution 16-6

$6,200 − $6,150 = **$50**. Two completeness procedures: recompute the workbook's consolidating adjustment column and agree
its total to the 27 scheduled entries with no residual plug; and compare the v13 and v14 adjustment columns cell by cell.
Contradicting results are a column that does not foot to $6,200, a v13-to-v14 delta absent from the schedule, or an
elimination that does not clear the component balance — each showing the schedule is a summary, not the population.

### Solution 16-7

The population is the client's listing accepted without reconciliation, yet the paragraph concludes it is complete and
ignores the top-side and subledger adjustments. The testing addressed only approval and agreement to management's
schedules, which are not source evidence, leaving business purpose and the accounting conclusion untested. The conclusion
is projected from a criteria-based selection, which supports no projection. And sampling risk is inapposite: the relevant
risk is criteria misspecification.

### Solution 16-8

Model language: "We reconciled net FY2025 activity to the audited net loss of $21,400 without difference and reconciled
opening balance plus file activity to the closing trial balance for 186 of 187 active accounts. For account 2200, accrued
expenses — other, an unexplained difference of $60 remains (opening $5,900 plus activity of $440 against a closing balance
of $6,400). The difference is below the $72 clearly trivial threshold, but it means the file may be incomplete by an
unknown number of entries rather than by $60. We therefore obtained account 2200 activity from the general ledger detail
report, identified the two omitted entries, confirmed neither met any criterion, and extended the reconciliation to
confirm no other account is affected." Waiving the $60 as clearly trivial is wrong: the amount is trivial, the
completeness implication is not.


### Solution 16-9

Fields to add: created date-time with time zone (the only field supporting C2 and C4); approver ID and approval timestamp
(tests W-12 and detects four-minute approvals); last-modified user and timestamp (Test B); transaction, functional, and
reporting amounts with an ISO currency code; a debit/credit indicator; and an origin indicator separating keyed entries,
CSV imports, and web services. Three questions: which date field defined the filter; how CSV import populates created-by,
and whether imports pass approval routing; which user IDs are service accounts.

### Solution 16-10

$1,240 − $410 = **$830 net reduction in expense**, 88.3% of performance materiality. The pattern supports inquiry and a
retrospective review of estimate bias under AS 2810 but not a conclusion: conservative accruals reverse favorably as a
matter of arithmetic, and a 61/37 split across 98 items is unremarkable. Obtain the reason codes, the original accrual
support, the preparer of each revision, and the FY2024 pattern. Two defensible conclusions: the pattern indicates bias,
requiring expanded testing and consideration of whether it indicates fraud; or it reflects a documented conservative
policy, supportable if the reversals concentrate in accounts whose accruals you tested. Treating the $830 as a
misstatement is the weakest answer — these are estimate revisions.

### Solution 16-11

It can be relied on, but not on the strength of the general IT controls, because for 27 days 11 users held a role
permitting data modification (W-2). Rely on evidence independent of those controls: T-3 and T-4 tie the file to a
separately audited net loss and to account-level movement, and the automated sources reconcile to payroll registers, bank
statements, and the Zuora Revenue contract summary. Then re-run the saved search with the team present, screenshot the
definition, test 100% of entries prepared or modified by the 11 users in the window, and confirm whether
privileged-activity monitoring operated. At $1,580 the amount exceeds performance materiality: test all direct-to-revenue
postings for the year, reconsider the I-3 conclusion, and reassess severity upward on magnitude.

### Solution 16-12

Match rate 61 of 62, **98.4%**. Exception rate: the omission plus the three amount differences is 4 of 62, **6.5%**;
counting only the omission gives **1.6%** — state which definition you used. The misstatement is the **$180 understatement
of accrued VAT** (C-4), found because a task was signed off with no entry posted. The limitation is that the test is
bounded by management's checklist: a required accrual with no task cannot be detected, which is how $290 of unaccrued
service-level-agreement credits (C-2) escaped.

## Review Questions

**RQ 16-1.** Is journal entry testing required when fraud risk is assessed as low in every account? Explain.

**RQ 16-2.** What does "other adjustments" add to the population, and name two such populations at AtlasFlow.

**RQ 16-3.** Name the four attributes a selected entry is tested against, and why one "appropriate?" column is inadequate.

**RQ 16-4.** Why is the account-level movement reconciliation stronger completeness evidence than the control-total page?

**RQ 16-5.** Define a manual journal entry and explain why a source type field is not a reliable indicator of one.

**RQ 16-6.** What is the difference between header grain and line grain, and give a criterion that differs at each?

**RQ 16-7.** Why is a criterion returning 3,847 of 4,912 entries useless for selection, and what should be done with
the condition it identifies?

**RQ 16-8.** What does a zero-hit criterion tell you, and how do you distinguish the two explanations?

**RQ 16-9.** Why is there no sampling risk in the criteria-based strata, and what risk applies instead?

**RQ 16-10.** Why must round-amount criteria run in transaction currency as well as reporting currency?

**RQ 16-11.** What is a consolidation top-side entry, and why are all 27 tested?

**RQ 16-12.** How does the close calendar test the completeness of period-end adjusting entries, and what can it never
find?

**RQ 16-13.** Why is the reversal flag a poor criterion, and which reversal pattern warrants 100% testing?

**RQ 16-14.** What is a statistical account, and what does including it do to the debit-equals-credit test?

**RQ 16-15.** A tested entry's accounting is correct but approval was applied four minutes after posting with no
support. What do you report, and to whom?

## Answers to Review Questions

**RQ 16-1.** Yes. AS 2401 and AU-C 240 respond to the risk of management override, treated as present in every audit. A
low assessed fraud risk affects the extent and emphasis of the work, not whether it is done.

**RQ 16-2.** It reaches adjustments made in preparing the statements that never appear as ledger entries: the 27
top-sides totaling $6,200 and the 1,847 contract-level adjustments in Zuora Revenue.

**RQ 16-3.** Support, business purpose, authorization, and the accounting conclusion. They fail independently —
JE-14962 was correctly computed and improperly authorized — and a single column loses whichever attribute failed.

**RQ 16-4.** The control page comes from the same process and person as the extract, so agreeing to it tests only
transcription. The reconciliation compares the file to balances audited by other procedures, so it can detect entries the
extract never contained.

**RQ 16-5.** A manual entry is one whose existence, accounts, or amount a person determined. The source type records
where a record originated, not who decided its content, so a hand-rebuilt interface journal keeps an automated type.

**RQ 16-6.** Header grain is one row per entry; line grain one row per debit or credit. A description criterion counted
at line grain multiplies by the line count — 4.5 for manual entries — so 388 hits appear as well over a thousand.

**RQ 16-7.** It selects 78.3% of the population, so it discriminates nothing. Quantify the condition against the whole
population and communicate it as a deficiency.

**RQ 16-8.** Either the risk is absent or the criterion is misspecified, and the two look identical. Test the logic
against entries you know exist: the December 31 criterion returned zero because the books stay open until January 9.

**RQ 16-9.** Each criterion runs against 100% of the population, so nothing is extrapolated. The remaining risk is
misspecification, addressed by differently-shaped criteria, the flag-completeness test, and sampling the residual.

**RQ 16-10.** Translation destroys roundness: a £100,000 entry at 1.2680 is $126,800 and passes a round-USD test. The
transaction-currency run surfaced 11 entries the reporting-currency run missed.

**RQ 16-11.** An adjustment recorded in consolidation rather than in any entity's ledger. All 27 are tested because the
population is small and the workbook has no version control and is emailed among four people (W-8).

**RQ 16-12.** Each task expected to produce an entry is matched to an entry in the file, and a task signed off with no
entry is a contradiction inside management's own records. It cannot find an accrual for which no task exists, which is
how $290 of unaccrued SLA credits passed.

**RQ 16-13.** Every reversing accrual generates two flagged records, so the flag selects 24.5% of the manual population.
The pattern warranting 100% testing is a reversal date on a non-accrual entry — nine existed, one for $1,340.

**RQ 16-14.** A non-financial memorandum account holding units such as headcount. It carries no debit or credit, so it
leaves debits and credits equal but inflates counts and breaks account-level reconciliations unless excluded.

**RQ 16-15.** Report a control deviation in the substantive workpaper, cross-reference it to the control conclusion, and
state that no misstatement arose. A significant deficiency or material weakness — likely here with W-12 and W-13 — is
communicated in writing to the audit committee under AS 1305.

## Key Definitions

**Automated entry.** An entry generated by an interface or system schedule without a person determining its accounts or
amount; 36,698 of AtlasFlow's 41,610 FY2025 entries, from twelve source types.

**Business purpose.** The economic reason for an entry, corroborated against support and against someone outside
accounting who would know.

**Close calendar.** Management's task-level close schedule — 148 December tasks in FloQast, 62 expected to produce an
entry — and the population for testing completeness of period-end adjusting entries.

**Consolidation top-side entry.** An adjustment recorded in consolidation rather than in any entity's ledger:
eliminations, translation, reclassifications, consolidated-only accruals. AtlasFlow recorded 27, $6,200.

**Effective date.** The date determining the period an entry affects, as distinct from the posting date and the creation
timestamp, whose comparison to the cut-off identifies post-close entries.


**Entry grain.** Whether a data set carries one row per entry (header grain) or per debit or credit (line grain).

**Information produced by the entity (IPE).** Client-prepared information used as audit evidence, whose completeness and
accuracy must be tested under AS 1105 and AU-C 500. A journal entry extract is IPE.

**Journal entry.** A debit-and-credit posting to the general ledger, identified by an entry number, comprising lines that
sum to zero. AtlasFlow's population averages 2.85 lines per entry.

**Manual journal entry.** An entry whose existence, accounts, or amount was determined by a person rather than by a
configured process; the population where management override is recorded.

**Period-end financial reporting process.** The activities by which trial balances become financial statements:
adjusting entries, consolidation, translation, elimination, drafting.

**Post-close entry.** An entry created after the cut-off for the period it affects; AtlasFlow recorded 61, $9,400. The
risk is that the reported result was known when the entry was made.

**Reversal flag.** A field indicating that an entry reverses another or will reverse on a future date. Because normal
accruals reverse, it selects 24.5% of the manual population and is useful only by pattern.

**Round-dollar entry.** An entry whose amount is an exact multiple of a round unit — here $10,000, at $100,000 or more,
producing 96 hits. Roundness suggests an estimated or plugged figure.

**Scoring model.** A weighted sum of the criteria an entry hits, used to rank a population. Firm methodology, not a
requirement; the weights are judgments and must be disclosed as such.

**Segregation-of-duties conflict.** A user's ability to perform two functions that should be separated — here, preparing
and posting an entry unaided (W-13), present on 214 manual entries totaling $18,600.

**Seldom-used account.** An account with few manual postings in the period, here five or fewer, producing 143 hits.
Improper entries collect there because no analytical procedure covers them.

**Statistical account.** A non-financial memorandum account holding units such as headcount. It carries no debit or
credit and must be excluded from financial reconciliations.

**Sufficiency conclusion.** The conclusion that the required procedures were performed and the evidence is sufficient,
stated no more broadly than the population proved complete.

**Trial balance movement reconciliation.** The completeness test comparing opening balance plus net file activity to the
closing trial balance for every account, and net income statement activity to the audited net result.

**Whole-population testing.** Applying a criterion to every item rather than to a sample, eliminating sampling risk in
that stratum but not the risk that the criterion is misspecified.

## Chapter Summary

1. Journal entry testing is required in every audit under AS 2401 and AU-C 240, because it responds to the risk of
   management override rather than to an assessed risk in a particular account.
2. The requirement reaches "other adjustments": the 27 top-sides totaling $6,200 and the 1,847 Zuora Revenue subledger
   adjustments, neither of which appears in a NetSuite extract.
3. The population is complete not because the client says so but because income statement activity of $21,400 ties to
   the audited net loss and 187 of 187 account movements tie to the trial balance.
4. The manual-entry flag is a hypothesis. Testing it moved 53 entries into the manual population, including nine
   hand-rebuilt Stripe revenue journals carrying an interface source type.
5. Calibrate a criterion before trusting it: one returning zero may be misspecified rather than reassuring, and one
   returning 3,847 of 4,912 entries is a finding to quantify, not a filter to select with.
6. Weighted scoring concentrates work where entries look wrong in more than one way; disclose the weights, and draw a
   stratum from entries no criterion hit, which tests the criteria themselves.
7. The four attributes fail independently, which is why an entry correct in amount and approved in four minutes without
   support is a control failure rather than a misstatement — and why an inherited reversal date on a permanent $1,340
   adjustment is a next-period misstatement with no preparer.
8. The close calendar is the only practical route to completeness of period-end adjusting entries — it found the $180
   accrued VAT understatement — and it cannot find an accrual for which no task exists.
9. Criteria-based strata carry no sampling risk; the risk is criteria misspecification, which more testing within the
   same criteria does not reduce. Report population conditions from the population rather than from tested items, and keep
   the sufficiency conclusion no broader than the population proved complete.

## Cross-References

| Topic | Chapter | Why you would go there |
| --- | --- | --- |
| General IT controls behind the extract (W-1, W-2, W-5, W-13) | Chapter 11 | The predicate for treating an extract as evidence |
| IPE; the I-3 interface; the consolidation workbook | Chapter 12 | Report-reliability technique; the six direct-to-revenue entries |
| The close-process walkthrough | Chapter 13 | Where the 148 tasks and the cut-off date come from |
| Severity of the review-evidence deviations | Chapter 14 | Deficiency grading with W-12 and W-13 |
| Sampling vocabulary for strata C, D, and E | Chapter 15 | Why criteria-based selection is not a sample |
| Fraud schemes and the whistleblower allegation | Chapter 17 | The schemes behind the criteria |
| Analytics technique and precision | Chapter 18 | Generalizes the whole-population methods used here |
| Materiality of $1,450, $940, and $72 | Chapter 3 | Sizing and evaluating this work |
| Accumulating misstatements | Chapter 19 | Where the $103 and C-4 go |

## Further Reading

- PCAOB AS 2401, *Consideration of Fraud in a Financial Statement Audit*, particularly the paragraphs on examining
  journal entries and other adjustments and on responses to the risk of management override.
- PCAOB AS 2110 and AS 2201, on the period-end financial reporting process and controls over it; AS 1305, on
  communicating deficiencies.
- PCAOB AS 1105, *Audit Evidence*, and AS 1215, *Audit Documentation*, on the reliability of information used as
  evidence and on documenting the source of extracted data.
- AICPA AU-C 240, AU-C 315 (as amended by SAS 145), and AU-C 500 (as amended by SAS 142), plus the AICPA guidance on
  audit data analytics for the full-population techniques in §16.5.
- COSO, *Internal Control — Integrated Framework* (2013), Principles 10 through 13, for the control activities behind
  the journal entry review control.




