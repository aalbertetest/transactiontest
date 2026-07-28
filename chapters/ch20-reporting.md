# Chapter 20 — Reporting

> Everything in the preceding nineteen chapters exists to support a few hundred words of opinion language and
> a few thousand words of description around it. The report is the only part of the audit the public ever
> reads, the only part that carries legal consequence in its own right, and the part most often drafted last,
> fastest, and from a template that was right for a different company in a different year. This chapter treats
> the report as an engineered artifact: every element has a function, every function has a source in the
> evidence file, and every sentence must survive the question "how do you know that?" You will draft Brightline
> LLP's FY2025 report on AtlasFlow, Inc. — an unqualified opinion on the financial statements alongside an
> adverse opinion on internal control over financial reporting, two material weaknesses, and three critical
> audit matters — and see why the hardest drafting in a modern report is not the opinion but the paragraphs
> around it.

## Learning Objectives

- **LO 20.1** Identify each element of the auditor's report under PCAOB AS 3101 and state what that element
  accomplishes for a reader of the financial statements.
- **LO 20.2** Draft the addressee, date, signature, city and state, and auditor tenure statement for an
  issuer report, and reconcile each to a specific source in the engagement file.
- **LO 20.3** Apply the two-part critical audit matter (CAM) determination to a list of candidate matters,
  document the accept/reject reasoning, and defend the resulting count.
- **LO 20.4** Draft a CAM containing all four required elements without introducing original information
  about the company and without language that reads as a piecemeal opinion.
- **LO 20.5** Draft an adverse opinion on internal control over financial reporting under AS 2201, including
  a material weakness description that states the deficiency, the accounts affected, and the potential effect.
- **LO 20.6** Distinguish the PCAOB report form from the AICPA form under AU-C 700 and enumerate the
  substantive, not merely cosmetic, differences.
- **LO 20.7** Select among an unqualified, qualified, adverse, and disclaimer opinion for a given
  combination of subject matter and pervasiveness, and draft the required report modifications.
- **LO 20.8** Draft explanatory, emphasis-of-matter, and other-matter paragraphs for going concern, a
  restatement, and a change in accounting principle.
- **LO 20.9** Evaluate whether Item 9A disclosure controls and procedures conclusions are consistent with an
  adverse ICFR opinion, and describe the auditor's role in Form 10-K assembly.
- **LO 20.10** Determine the auditor's obligations when facts are discovered after the report release date or
  when a necessary procedure is found to have been omitted.

## Standards and Guidance Map

| Source | Reference | What it requires that matters here |
| --- | --- | --- |
| PCAOB | AS 3101 | The form and content of the auditor's report on financial statements: title, addressee, opinion, basis for opinion, CAMs, tenure, signature, city and state, date |
| PCAOB | AS 3105 | Departures from the unqualified opinion: qualified, adverse, disclaimer, and other reporting circumstances |
| PCAOB | AS 2201 | The ICFR audit and its report: unqualified and adverse forms, the material weakness description, reference to management's report, combined versus separate reports |
| PCAOB | AS 2415 | Going concern: when substantial doubt requires an explanatory paragraph and what that paragraph says |
| PCAOB | AS 1301 | Communications with the audit committee, including draft CAMs and the report before issuance |
| PCAOB | AS 2710 | Other information in a document containing audited financial statements; reading the Form 10-K for material inconsistency |
| PCAOB | AS 4105 | Reviews of interim financial information and the form of the review report |
| PCAOB | AS 6101 | Letters for underwriters and certain other requesting parties (comfort letters) |
| PCAOB | AS 2905 | Subsequent discovery of facts existing at the date of the auditor's report |
| PCAOB | AS 2901 | Consideration of omitted procedures after the report date |
| AICPA | AU-C 700 | The unmodified opinion for a nonissuer: required sections and headings, management and auditor responsibility language (SAS 134, effective for periods ending on or after December 15, 2021) |
| AICPA | AU-C 701 | Key audit matters — reported only when the auditor is engaged to do so |
| AICPA | AU-C 705 | Modifications to the opinion: qualified, adverse, disclaimer |
| AICPA | AU-C 706 | Emphasis-of-matter and other-matter paragraphs |
| AICPA | AU-C 570 | Going concern, including the required separate report section |
| AICPA | AU-C 560 | Subsequent events and subsequently discovered facts |
| AICPA | AU-C 930 | Interim financial information review reports for nonissuers |
| SEC | Rules 13a-15(e) and 13a-15(f); Item 9A of Form 10-K | Disclosure controls and procedures versus ICFR; management's report and the auditor's attestation |
| SEC | Regulation S-K Item 308; Securities Act Section 7 | Management's ICFR report and the auditor's attestation report; the consent requirement |
| COSO | *Internal Control — Integrated Framework* (2013) | The criteria named in both management's report and the auditor's ICFR opinion |
| FASB | ASC 606; ASC 326; ASC 340-40 | The accounting subject matter of the three AtlasFlow CAMs |

Where the two frameworks differ substantively — the tenure statement, CAMs, the ICFR opinion, and the
placement of going-concern language — §20.9 sets the differences out element by element.

## Prerequisites and Chapter Dependencies

Read Chapter 19 first: the report is a conclusion, and Chapter 19 owns the evidence and the evaluation that
support it, including the summary of audit differences, the subsequent-events review, the going concern
evaluation, and the final sufficiency-of-evidence conclusion. Read Chapter 14 for the deficiency-severity
methodology that produces the two material weaknesses reported here, and Chapter 11 for the IT general
control (ITGC) population those weaknesses come from. Chapter 17 owns communications about fraud to the
audit committee and to regulators; this chapter does not repeat them. Nothing builds on Chapter 20 — it is
the last chapter — but §20.10 points forward to the post-issuance obligations that outlive the engagement.

## 20.1 The report as an engineered artifact

An auditor's report is not prose with a conclusion in it. It is a set of elements, each of which exists
because a reader would otherwise have to guess at something. Exhibit 20-1 lists the elements the PCAOB form
requires and, for each, the question it answers and the file location that supports it. When you draft, you
draft against this table; when you review, you tie against it.

**Exhibit 20-1. Elements of the issuer auditor's report under AS 3101 and what each accomplishes.**

| # | Element | The question it answers | Where the support lives |
| --- | --- | --- | --- |
| 1 | Title containing "Report of Independent Registered Public Accounting Firm" | Is this an audit by a PCAOB-registered firm, and is the firm independent? | Independence documentation; PCAOB registration |
| 2 | Addressee — stockholders and board of directors | Who engaged the auditor and to whom is the report directed? | Engagement letter |
| 3 | Opinion paragraph identifying each statement and each period | Exactly what was audited, and what is the conclusion? | The F-pages as filed |
| 4 | Reference to the applicable financial reporting framework | Against what criteria was fairness judged? | Note 1 basis of presentation |
| 5 | Basis for opinion: management's responsibility, the auditor's responsibility, PCAOB standards, independence, Section 10A(b) | Who is responsible for what, and under whose rules was the work done? | Engagement letter; independence file |
| 6 | Statement that the audit provides reasonable, not absolute, assurance | What is the inherent limit of the assurance? | n/a — standardized |
| 7 | Critical audit matters | Which matters were hardest, and what did the auditor do about them? | CAM determination memo; the underlying testing sections |
| 8 | Signature of the firm | Who is accountable? | Firm policy; partner authorization |
| 9 | City and state of the issuing office | Which office issued it? | Engagement administration |
| 10 | Auditor tenure — "We have served as the Company's auditor since 20XX" | How long has this firm been in the seat? | Original engagement letter or firm records |
| 11 | Date of the report | As of what date had sufficient appropriate evidence been obtained? | Completion checklist, rep letter, EQR sign-off |

Two of these are worth dwelling on because they are the most frequently botched.

**The opinion paragraph is an inventory.** It must name each statement and each period covered. AtlasFlow
files balance sheets as of two dates and statements of operations, comprehensive loss, stockholders' equity,
and cash flows for three years. A report that says "for the year ended December 31, 2025" when three years of
operating statements are presented is wrong on its face, and it is wrong in a way that a careful reader of the
F-pages will catch. Tie the sentence to the table of contents of Item 8, not to last year's report.

**The tenure statement is a fact, not a courtesy.** Brightline LLP was engaged for the FY2021 audit, so the
sentence reads "We have served as the Company's auditor since 2021." The year stated is the year of the
earliest period audited under an uninterrupted engagement, not the year the engagement letter was signed for
the current audit and not the year of the first report issued. Where a predecessor firm was acquired, or the
registrant was a subsidiary of another registrant the firm audited, the determination requires firm-level
records; the PCAOB has issued staff guidance on those fact patterns, and a two-line memo in the file citing
the source is cheap insurance.

### 20.1.1 Dating and the report release date

The report date is the date on which the auditor obtained sufficient appropriate evidence to support the
opinion. For AtlasFlow that date is **February 20, 2026** — the date on which the management representation
letter is signed, the engagement quality reviewer has completed his review and provided concurring approval
of issuance, the legal letters are in, and the Form 10-K is in final form. The **report release date** is the
date the auditor grants permission to use the report, which for a 10-K is the filing date. Chapter 19 owns the
completion sequence that produces both dates; what matters here is that no element of the report may be dated
earlier than the completion of the work it depends on, and that the subsequent-events review runs through the
report date.

Dual dating arises when the auditor's responsibility for subsequent events is extended for one matter only.
The Meridian Health Systems dispute of February 9, 2026 falls *before* February 20, 2026, so it requires no
dual dating; it is simply part of the audit. If instead management amended its filing on March 4, 2026 to
disclose a new event, the auditor would either redate the entire report to March 4 (extending responsibility
for all subsequent events to that date) or dual date:

```text
February 20, 2026, except for Note 18, as to which the date is March 4, 2026
```

The first alternative is safer for the reader and more expensive for the auditor; the second confines the
extended responsibility to the identified note. Practice varies with the significance of the event, and the
choice is a partner decision that should be documented with the reason.

## 20.2 The opinion on the financial statements

The unqualified opinion is the easiest paragraph in the report to write and the easiest to write carelessly.
Illustrative language for AtlasFlow, in the PCAOB form:

```text
Opinion on the Financial Statements

We have audited the accompanying consolidated balance sheets of AtlasFlow, Inc. and subsidiaries (the
"Company") as of December 31, 2025 and 2024, the related consolidated statements of operations,
comprehensive loss, stockholders' equity, and cash flows for each of the three years in the period ended
December 31, 2025, and the related notes (collectively referred to as the "financial statements"). In our
opinion, the financial statements present fairly, in all material respects, the financial position of the
Company as of December 31, 2025 and 2024, and the results of its operations and its cash flows for each of
the three years in the period ended December 31, 2025, in conformity with accounting principles generally
accepted in the United States of America.
```

Four drafting checks on that paragraph. The entity name must match the cover page of the Form 10-K exactly,
including the comma before "Inc." The phrase "and subsidiaries" belongs there because AtlasFlow consolidates
four legal entities (§1.5 of the continuing case). The period phrase "each of the three years in the period
ended December 31, 2025" must match the periods actually presented. And "in all material respects" is not
decoration — it is the entire reason the report can be issued when $460 of uncorrected misstatement remains
on the summary of audit differences against overall materiality of $1,450 (Chapter 19, §19.3).

The basis-for-opinion section that follows allocates responsibility: it states that the financial statements
are management's responsibility, that the auditor's responsibility is to express an opinion, that the firm is
PCAOB-registered and required to be independent under the federal securities laws and the rules of the SEC and
the PCAOB, that the audit was conducted under PCAOB standards, that those standards require reasonable rather
than absolute assurance about material misstatement whether due to error or fraud, and that the procedures
performed provide a reasonable basis for the opinion. For an integrated audit the section is written in the
plural — "our audits," "our opinions" — and adds language about the ICFR audit and about obtaining an
understanding of internal control over financial reporting. §20.6 presents the combined form in full rather
than repeating it here.

## 20.3 Critical audit matters

CAMs are the part of the report that requires actual writing. Everything else can be assembled; a CAM must be
composed, because it describes something that happened only on this engagement.

### 20.3.1 The two-part determination

A matter is a CAM only if **both** of the following hold:

1. It was communicated, or was required to be communicated, to the audit committee; **and**
2. It relates to accounts or disclosures that are material to the financial statements **and** involved
   especially challenging, subjective, or complex auditor judgment.

The first prong is a filter that almost everything passes: the AS 1301 communication agenda for a
public-company audit is long. The second prong is where the work is, and it has two independent conditions
joined by "and." Materiality of the account is necessary but not sufficient; auditor judgment being difficult
is necessary but not sufficient. Note also that the standard speaks of *auditor* judgment, not management
judgment. A management estimate can be highly subjective and still not produce a CAM if the auditor's response
was mechanical — for example, a discount-rate assumption that the auditor tests by reference to an observable
published curve.

Factors that push a matter toward CAM status include the auditor's assessment of the risks of material
misstatement, the degree of subjectivity in applying procedures or evaluating results, the nature and extent
of audit effort including whether specialized skill was needed, the nature of the evidence obtained, and
whether the matter involved a significant unusual transaction. Exhibit 20-2 records the FY2025 determination.

**Exhibit 20-2. FY2025 CAM determination — candidates considered (amounts in thousands).**

| Candidate | Account / disclosure | Material? | Especially challenging, subjective, or complex auditor judgment? | CAM? |
| --- | --- | --- | --- | --- |
| A. Standalone selling price of the Insight module | Revenue $148,200; Insight $26,700 (18.0% of revenue) | Yes | Yes — 31 standalone sales, interquartile range 22% of list; the auditor had to evaluate an estimation approach, not verify a price | **Yes** |
| B. Allowance for credit losses | Allowance $1,900 against gross AR $38,600 | Yes — allowance is 1.3× overall materiality | Yes — CECL forecast overlay; auditor's acceptable range was $1,900 to $2,300 and management recorded the low end | **Yes** |
| C. Revenue cut-off and contract term | Revenue $148,200; RPO $214,000 | Yes | Yes — 41% of Q4 ACV signed in five days; a whistleblower allegation; a control that did not exist as described | **Yes** |
| D. Kestrel Labs purchase price allocation | Goodwill $26,900; intangibles $9,700 | Yes | Considered — rejected; see below | No |
| E. Four-year amortization period for capitalized commissions | Deferred contract acquisition costs $24,000 | Yes | Considered — rejected; see below | No |
| F. Stock-based compensation and the PSU probability revision | SBC $28,700; catch-up credit $1,340 | Yes | No — the Q4 revision to 85% was tested against board-approved ARR reporting; judgment was bounded | No |
| G. Going concern | n/a | n/a — no substantial doubt identified (Chapter 19, §19.6) | n/a | No |

**Why D was rejected.** The Kestrel Labs acquisition is a significant unusual transaction, it was
communicated to the audit committee, and goodwill of $14,500 arising from it is material. The engagement team
nonetheless concluded that the auditor's judgment was not especially challenging: the two identifiable
intangibles total $8,000, the valuation specialist's independently developed ranges were narrow, management's
point estimates fell inside them, and the $2,000 consideration error was a factual omission of a
working-capital payment that was corroborated directly to the funds-flow memorandum rather than a matter of
judgment. Practice varies here, and reasonable partners disagree: a firm whose methodology treats every
material business combination as a presumptive CAM would report D as a fourth CAM, and that answer is
defensible. What is *not* defensible is failing to document the decision either way.

**Why E was rejected.** The four-year period of benefit is subjective, but the auditor's response reduced to
testing two computations — average customer life of 4.3 years and the ratio of renewal commissions (3.1% of
ACV) to initial commissions (11.8% of ACV) — against underlying data, and the outcome was insensitive across
the plausible range of three to five years relative to overall materiality. Low sensitivity is a legitimate
reason to reject a candidate, and stating the sensitivity in the memo is what makes the rejection reviewable.

**How many CAMs is normal?** Published post-implementation analyses of the first several CAM reporting years
report that most large accelerated filers disclose one or two CAMs, with averages slightly above one and a
long right tail. Three CAMs for a $148.2 million SaaS registrant in its first integrated-audit year is above
the median but unremarkable, and the reason is visible on the face of Exhibit 20-2: two of the three arise
from a single account, revenue, that carries most of the company's estimation and cut-off risk. Zero CAMs is
possible but rare enough that it invites inspection scrutiny; a report with seven CAMs usually signals that
the team applied the first prong of the test and skipped the second.

### 20.3.2 The four required elements of a CAM description

Every CAM must:

1. **Identify** the critical audit matter.
2. **Describe the principal considerations** that led the auditor to determine the matter is a CAM.
3. **Describe how the CAM was addressed** in the audit — the auditor may describe the response or approach,
   the outcome, or the relevant accounts or disclosures, and in practice describes the procedures.
4. **Refer** to the relevant financial statement accounts or disclosures.

A useful drafting discipline is to write element 2 before element 3. Element 3 is only defensible if it
responds to element 2; teams that write procedures first end up with a list of things they did rather than a
description of how they attacked a specific difficulty.

### 20.3.3 What must not appear in a CAM

Two prohibitions matter, and both are violated regularly.

**No original information about the company.** A CAM cannot be the vehicle by which a number, a range, or a
fact about AtlasFlow reaches the market for the first time. "Management's estimated standalone selling price
for Insight is $184 per seat per month, at the 38th percentile of observed standalone sales" is original
information if it is not in the notes. The fix is to draft CAMs against the final note text and to cite it:
if the CAM needs a number, the number belongs in Note 2 first. This is why CAM drafting cannot finish before
the disclosures do.

**No language that reads as a piecemeal opinion.** A CAM describes procedures and difficulty; it does not
express a conclusion on the account. "We concluded that management's estimate of the standalone selling price
of Insight was reasonable" is a piecemeal opinion — an opinion on one element of the financial statements
inside a report expressing an opinion on the statements as a whole. So is "our procedures identified no
misstatements in revenue." Delete conclusions. The opinion paragraph is the only place a conclusion belongs.

Three further discipline points: do not describe a CAM in terms that imply the matter is unresolved or that
the auditor was uncomfortable issuing the report; do not describe reliance on controls in a CAM that overlaps
an area with a material weakness (see §20.6.3); and do not use the phrase "we tested" as a container for
procedures you did not perform at the level the sentence implies.

### 20.3.4 The drafting process

Exhibit 20-3 shows the sequence Brightline used, with the dates from the FY2025 engagement. The point of
showing dates is that CAM drafting has a critical path: it depends on the disclosures being final and on the
audit committee having seen the draft, and those two dependencies collide in the last ten days.

**Exhibit 20-3. CAM drafting and clearance sequence, FY2025.**

| Date | Step | Output |
| --- | --- | --- |
| Nov 14, 2025 | Preliminary CAM identification at the pre-year-end planning update | Candidate list A–G, no drafting |
| Jan 9, 2026 | Draft CAM text prepared by the manager who owned each area | First drafts, WP 9100-12 |
| Jan 16, 2026 | Senior manager and partner review; national office consultation on the Insight CAM | Second drafts |
| Jan 26, 2026 | Engagement quality reviewer reads drafts against the underlying testing sections | Third drafts |
| Feb 3, 2026 | Draft CAMs and draft report provided to the audit committee under AS 1301 | Audit committee package |
| Feb 11, 2026 | Audit committee meeting; management's Note 2 revised to support the Insight CAM's reference | Final note text |
| Feb 18, 2026 | Final tie-out of CAM text to notes, accounts, and the testing sections | Tie-out memo |
| Feb 20, 2026 | Report dated and signed | Issued report |

## 20.4 Key audit matters and how they differ from CAMs

Outside the PCAOB regime the closest analogue is the **key audit matter (KAM)**. Under AU-C 701 a KAM is
reported only when the auditor is *engaged* to communicate KAMs — it is opt-in for nonissuers, and in US
private-company practice it is rare. Under the international standards KAMs are required for listed entities.
The differences from a CAM are substantive, not stylistic:

| Dimension | CAM (AS 3101) | KAM (AU-C 701 / ISA 701) |
| --- | --- | --- |
| When reported | Required for issuer audits, subject to specified exemptions (including emerging growth companies) | Only when engaged to do so (AU-C 701); required for listed entities under the international standards |
| Selection screen | Communicated or required to be communicated to the audit committee, **and** relates to material accounts or disclosures, **and** involved especially challenging, subjective, or complex **auditor** judgment | Matters of most significance in the audit, selected from matters communicated with those charged with governance |
| Materiality gate | Explicit — the account or disclosure must be material | Implicit — significance to the audit |
| Going concern | Reported through the AS 2415 explanatory paragraph, not as a CAM | May be reported as a KAM in some frameworks, with cross-reference to the going-concern section |
| Number typically reported | Usually one or two | Often two to four, and the frameworks anticipate a range |

AtlasFlow, having lost emerging growth company status only at the end of FY2025, was never CAM-exempt on that
basis — the exemption applies to EGCs, and AtlasFlow reported its first CAMs for FY2023 as an accelerated
filer. Do not confuse the EGC exemption from CAM reporting with the EGC exemption from Section 404(b), which
is what changes for FY2025.

## 20.5 The ICFR opinion under AS 2201

### 20.5.1 The unqualified form

When ICFR is effective, the opinion is on the effectiveness of ICFR as of the balance sheet date, measured
against stated criteria:

```text
Opinion on Internal Control over Financial Reporting

In our opinion, the Company maintained, in all material respects, effective internal control over financial
reporting as of December 31, 2025, based on criteria established in Internal Control — Integrated Framework
(2013) issued by the Committee of Sponsoring Organizations of the Treadway Commission.
```

Three drafting points. The criteria must be named with the framework edition, because the 1992 and 2013
frameworks are different criteria and management's report names one of them; the auditor's report must name
the same one. The opinion is *as of* a date, not *for* a period — a control that failed in March and was
remediated in September does not by itself impair an as-of conclusion, which is why the timing of remediation
matters so much in Chapter 14's severity analysis. And "in all material respects" carries the same weight
here as in the financial statement opinion: the threshold for an adverse ICFR opinion is a material weakness,
not a deficiency.

### 20.5.2 The adverse form and the material weakness description

There is no "qualified" ICFR opinion for a material weakness. Either ICFR is effective or, because one or more
material weaknesses exist, it is not. A scope limitation is different: if the auditor cannot obtain sufficient
appropriate evidence about ICFR, the auditor disclaims or withdraws, and for an integrated audit a disclaimer
on ICFR is close to unworkable in practice.

The adverse report must, in addition to the adverse opinion: define a material weakness; describe each
material weakness identified; state whether each was included in management's assessment; refer to
management's report; and state that the material weaknesses were considered in determining the nature, timing,
and extent of the financial statement audit procedures. Exhibit 20-4 shows what a description must contain and
maps it to the two AtlasFlow weaknesses.

**Exhibit 20-4. Required content of a material weakness description, mapped to the FY2025 weaknesses.**

| Required content | MW-1: Information technology general controls | MW-2: Revenue cut-off |
| --- | --- | --- |
| What the control objective was | Restrict and monitor access to, and changes in, the systems that process revenue and produce financial reports | Validate contract effective dates and service commencement before revenue schedules are generated |
| The nature of the deficiency | Deficiencies in logical access and privileged account management, program change management, and controls over manual journal entries | A control described in management's documentation did not exist as described — a design deficiency, not an operating failure |
| Accounts and disclosures affected | Revenue, deferred revenue, accounts receivable, and substantially all accounts, because IT-dependent and automated controls throughout the financial reporting process could not be relied upon | Revenue, accounts receivable, contract assets, deferred revenue, and the remaining performance obligation disclosure |
| Actual or potential effect | Did not result in a material misstatement of the FY2025 financial statements; created a reasonable possibility that a material misstatement would not be prevented or detected on a timely basis | Same conclusion, with the additional statement that the deficiency related to contracts executed near period end |
| Whether included in management's assessment | Yes | Yes |

Note the sentence "did not result in a material misstatement." You may say that only if it is true and only if
you can support it. Here it is supported by Chapter 19's summary of audit differences: the aggregate
uncorrected effect on pre-tax loss is $(460), which is 31.7% of overall materiality of $1,450, and no
individual uncorrected item exceeds $240. Where a material weakness *did* produce a material misstatement, the
description says so, and the financial statement opinion usually stops being unqualified — which is why the
two opinions in a combined report must be drafted together, not sequentially by different people.

### 20.5.3 Combined or separate

The auditor may issue one combined report covering both opinions or two separate reports. Exhibit 20-5 sets
out the decision.

**Exhibit 20-5. Combined versus separate report — decision factors.**

| Factor | Favors combined | Favors separate |
| --- | --- | --- |
| Reader comprehension | One document; the reader cannot read one opinion without the other | — |
| Adverse ICFR opinion with an unqualified financial statement opinion | Combined makes the coexistence explicit and reduces the risk of a reader inferring a qualified financial statement opinion | Separate reports risk being quoted in isolation |
| Different report dates for the two opinions | — | Rare, but possible where ICFR work concludes later |
| Filing mechanics | One exhibit, one consent reference, one signature block | Two reports must both appear in Item 8 / Item 9A(c) |
| Firm methodology | Most firms default to combined for integrated audits | Some registrants request separate presentation |

Brightline issues a **combined** report for AtlasFlow. When the ICFR opinion is adverse, the combined form has
a specific drafting consequence: the sentence in the separate-report form that reads "this report does not
affect our report dated February 20, 2026, on those financial statements" has to be adapted, because there is
no other report to refer to. The combined form says instead that the material weaknesses were considered in
determining the nature, timing, and extent of audit procedures applied in the audit of the financial
statements and that the opinion on the financial statements expressed above is not affected. Getting this
sentence wrong — leaving in a reference to a nonexistent separate report — is the single most common defect in
first-year combined adverse reports.

### 20.5.4 Reference to management's report and the scope exclusion

The ICFR portion of the report refers to management's assessment, which for AtlasFlow appears in Item 9A(b)
of the Form 10-K. Management excluded Kestrel Labs, Inc. from its FY2025 assessment in reliance on the SEC
staff's long-standing position permitting exclusion of a recently acquired business, and disclosed the
exclusion. When management excludes an acquired business, the auditor's report must disclose the
corresponding scope exclusion. Illustrative language:

```text
We did not audit and, accordingly, do not express an opinion on the internal control over financial
reporting of Kestrel Labs, Inc., which was acquired on August 4, 2025, and whose internal control over
financial reporting was excluded from management's assessment as described in Item 9A(b). The total assets
and revenues of Kestrel Labs, Inc. excluded from management's assessment represent less than 1% of
consolidated total assets and revenues as of and for the year ended December 31, 2025.
```

Two cautions. First, the auditor must evaluate whether the exclusion is appropriate, whether the disclosure of
the excluded amounts is accurate, and whether the excluded business is nonetheless within the scope of the
financial statement audit — it always is. Second, the quantification in the paragraph must tie: Kestrel's
$340 of post-acquisition revenue is 0.23% of $148,200, and its identifiable assets are similarly small
relative to $317,900, so "less than 1%" is supportable. If the excluded business were 12% of assets, the
sentence would have to say 12%, and the audit committee would want to know why an exclusion of that size was
acceptable.

<!-- CONTINUE -->
