# The Five-Level Audit Review Chain

### A complete fictional audit file and its escalating chain of review

---

> ## ⚠️ THIS IS ENTIRELY FICTIONAL
>
> Every entity, person, firm, regulator, jurisdiction, transaction, balance and event in this
> repository is invented. **Auburn Ridge Group plc**, **Ashcroft Vane LLP**, the **Financial
> Reporting & Audit Oversight Authority** and the jurisdiction of **Meridia** do not exist. Any
> resemblance to a real company, audit firm, regulator or individual is coincidental and
> unintended.
>
> The financial statements, workpapers, review notes, inspection findings and regulatory
> determinations reproduced here have never existed. Nothing in this repository is, or should be
> relied upon as, professional, accounting, auditing, legal or regulatory advice. The named
> individuals are fictional; the failings attributed to them are illustrative devices, not
> allegations about any real person.
>
> References to real auditing and accounting standards (ISAs, ISQMs, IFRSs, the IESBA Code) are
> used because the point of the exercise is to show how real standards bite on a set of facts.
> Paragraph-level citations are indicative and written for narrative plausibility — see
> `00-reference/00-05-glossary-and-standards.md` before treating any citation as authoritative.

---

## What this is

This is a single audit engagement documented five times over, from five different vantage points,
each one looking down at the layer beneath it:

| Level | Who is reviewing | What they are reviewing | Folder |
|---|---|---|---|
| **1** | The engagement team | Auburn Ridge Group plc, FY20X4 | [`01-audit-file/`](01-audit-file/) |
| **2** | The audit manager | The engagement team's audit file | [`02-manager-review/`](02-manager-review/) |
| **3** | The engagement partner | The manager's review | [`03-partner-review/`](03-partner-review/) |
| **4** | The firm's internal inspection team | The partner's review | [`04-inspection-review/`](04-inspection-review/) |
| **5** | The statutory regulator | The inspection team's comments | [`05-regulator-review/`](05-regulator-review/) |

Each level is written *in the voice and format of that level*. The audit file reads like working
papers. The manager review reads like a review-note register. The partner review reads like a memo
from someone who is short of time and about to sign an opinion. The inspection report reads like an
internal quality report with a grade attached. The regulator's report reads like a statutory
inspection with required actions and an enforcement referral.

## The point of the exercise

The interesting thing is not that the audit was bad. The interesting thing is **what each level of
review does and does not catch, and why.**

The same ten issues sit in the file from the beginning. They are visible, in principle, to everyone.
What changes as you move up the chain is not the evidence — it is the reviewer's incentives,
time budget, distance from the client, and willingness to look. The chain therefore surfaces a
progression:

- **The manager** finds real problems and then accepts weak answers to them, because the answers
  come from people she works with every day and the deadline is fixed.
- **The partner** reviews the manager's *conclusions* rather than the manager's *review*, and so
  inherits every error the manager cleared. He spends 11.5 hours reviewing a 3,140-hour engagement.
- **The inspection team** catches most of the substantive audit failures — and then downgrades four
  of them between draft and final report after the partner objects.
- **The regulator** finds that the audit was deficient, but concludes that the *more serious*
  problem is that the firm's own inspection function found the deficiencies and then neutralised
  them. The regulator's harshest findings are about the reviewers, not the auditors.

By Level 5 the subject matter has shifted entirely. The regulator is barely interested in Auburn
Ridge Group plc. It is interested in whether a firm that can detect its own failures and then
grade them away has a functioning system of quality management at all.

## The ten issues

Every level engages with the same numbered issue spine. This is what makes the chain traceable.

| ID | Issue | Quantified effect |
|---|---|---|
| **ISS-01** | Contract CN-4471: unsupported Q4 reduction in estimated costs to complete | PBT overstated up to £3.5m |
| **ISS-02** | Revenue cut-off sample errors not projected to the population | Projected misstatement £7.0m vs recorded £1.9m |
| **ISS-03** | Reseller channel recognised gross without principal-vs-agent analysis or mandatory consultation | Revenue overstated up to £26.8m (no PBT effect) |
| **ISS-04** | ERP migration ITGC deficiencies; controls reliance retained without support | Pervasive to revenue, journals, procurement |
| **ISS-05** | Business combination: contingent consideration fell outside the valuation specialist's scope and nobody owned it | Liability understated up to £4.4m |
| **ISS-06** | Goodwill: discount rate below the specialist's own range; sensitivity disclosure omitted | Impairment of up to £22.1m not recognised |
| **ISS-07** | Going concern assessed for 12 months from the balance sheet date, not from approval; refinancing falls outside the window | Material uncertainty disclosure potentially omitted |
| **ISS-08** | £2.4m paid to an entity connected to the CFO; undisclosed | 24× the specific materiality for related parties |
| **ISS-09** | Audit report signed two days before the engagement quality review was completed | ISQM 2 breach |
| **ISS-10** | File assembled 61 days after signing; nine workpapers modified after archive lock | Document integrity |

Follow any one of them all the way up in
[`99-appendices/99-01-five-level-traceability-matrix.md`](99-appendices/99-01-five-level-traceability-matrix.md),
or read the full life story of a single issue in
[`99-appendices/99-02-escalation-case-study-cn-4471.md`](99-appendices/99-02-escalation-case-study-cn-4471.md).

## Suggested reading routes

**If you have ten minutes.** Read the traceability matrix (`99-01`), then the regulator's public
report extract (`05-regulator-review/R-800`). Those two documents bracket the whole story.

**If you want the narrative.** Read the CN-4471 case study (`99-02`). One contract, one estimate,
five reviews, and a delay claim nobody connected to it.

**If you want to see how review actually decays.** Read these four in order:

1. `02-manager-review/M-200-review-notes-register.md` — 45 notes, all closed. Look at the clearance dates.
2. `03-partner-review/P-200-note-by-note-assessment-of-manager-clearances.md` — the partner assessing those clearances.
3. `04-inspection-review/I-200-assessment-of-the-partner-review.md` — the inspection team assessing the partner.
4. `05-regulator-review/R-200-assessment-of-the-firms-internal-inspection.md` — the regulator assessing the inspection team.

**If you are here for the accounting.** Start with the fact pattern
(`00-reference/00-01`) and the financial statements extract (`00-reference/00-02`), then read the
substantive workpapers in `01-audit-file/C-substantive/`.

**If you are here for the quality-management angle.** `04-inspection-review/I-400` (root cause
analysis), `04-inspection-review/I-500` (how a grade 3 became a grade 2), and
`05-regulator-review/R-500` (why the regulator thinks the whole system is the problem).

## Repository map

```
fictional-audit-review-chain/
├── README.md                        ← you are here
├── 00-reference/                    Shared facts every level draws on
│   ├── 00-01-fact-pattern-and-entity-background.md
│   ├── 00-02-financial-statements-extract.md
│   ├── 00-03-engagement-team-and-chronology.md
│   ├── 00-04-file-index-and-referencing-convention.md
│   └── 00-05-glossary-and-standards.md
│
├── 01-audit-file/                   LEVEL 1 — the engagement team
│   ├── A-planning/                  A-100 … A-700
│   ├── B-controls/                  B-100 … B-300
│   ├── C-substantive/               C-100 … C-950
│   └── D-completion/                D-100 … D-600
│
├── 02-manager-review/               LEVEL 2 — M-100 … M-500
├── 03-partner-review/               LEVEL 3 — P-100 … P-500
├── 04-inspection-review/            LEVEL 4 — I-100 … I-700
├── 05-regulator-review/             LEVEL 5 — R-100 … R-800
│
└── 99-appendices/
    ├── 99-01-five-level-traceability-matrix.md
    └── 99-02-escalation-case-study-cn-4471.md
```

## Conventions

- **Dates** use the accounting convention of `20X4` for the year under audit, `20X5` for the audit
  and internal inspection year, and `20X6` for the regulatory inspection year.
- **Currency** is the Meridian pound, written `£`. All figures are in millions (`£m`) unless the
  unit says otherwise.
- **Workpaper references** follow the firm's index convention, described in `00-reference/00-04`.
  A reference such as `C-100/7` means schedule 7 within workpaper C-100.
- **Issue IDs** (`ISS-01` … `ISS-10`) are a device of this repository, not of the fictional firm.
  They let you trace a single matter across five levels that would, in real life, each use their
  own incompatible numbering. The levels' own reference systems (`MRN-014`, `PRN-06`, `INSP-F03`,
  `FRAOA-F07`) are also used and are cross-mapped in `99-01`.

## A note on realism

The engagement described here is bad, but it is not absurd. Nothing in the file is fraudulent on
the auditor's part. No one lies. Every individual failure is the kind that gets made by competent,
tired people working to a fixed reporting deadline with a client who is pleasant and cooperative
and whose numbers happen to be optimistic.

That is deliberate. Audit failures that look like conspiracies are rare and easy to dismiss.
Audit failures that look like a series of reasonable-at-the-time judgements are common, and they
are the ones worth learning to recognise.

The clean parts of the file are deliberate too. Inventory (`C-400`) is well audited. The group
scoping memorandum (`A-600`) is thoughtful. The audit committee report (`D-400`) is genuinely
informative. A file in which everything is wrong teaches nothing about how to spot the parts that
are.
