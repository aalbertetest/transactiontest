# Style Guide and Chapter Template

This guide is binding on every chapter of *Auditing Software-as-a-Service Companies: A Practitioner's
Textbook*. It exists so that twenty chapters written to a common specification read as one book rather than
as twenty essays.

---

## 1. Non-negotiable requirements for every chapter

| Requirement | Specification |
| --- | --- |
| Length | **Minimum 5,000 words; target 6,000–8,000 words.** Verify with `tools/wordcount.sh`. |
| File name | `chapters/chNN-slug.md` where `NN` is the zero-padded chapter number |
| Title line | `# Chapter N — Title` as the first line of the file |
| Continuing case | Draws its examples from AtlasFlow, Inc. (see `case-materials/atlasflow-continuing-case.md`) and does not contradict the facts recorded there |
| Numbers | Every numeric illustration must foot, cross-foot, and tie. If a table has a total row, the total must equal the sum of the components. |
| Voice | Second person for procedural instruction ("you", "the engagement team"), third person for exposition. Present tense. |
| No emojis | Anywhere. |
| No filler | Do not write "in today's fast-paced world," "it is important to note that," or similar padding. Length must come from substance: more worked detail, more numbers, more cases. |
| Tone | A senior manager teaching a competent second-year staff member. Assume the reader knows debits and credits and basic audit vocabulary but not SaaS specifics or advanced judgment. |

## 2. Required section structure

Sections must appear in this order, with these exact heading texts (substituting the chapter number for `N`):

```
# Chapter N — <Title>

> One-paragraph epigraph framing the chapter's central problem.

## Learning Objectives
## Standards and Guidance Map
## Prerequisites and Chapter Dependencies
## N.1 <first substantive section>
...  (as many substantive sections as the material requires; see §3)
## Step-by-Step Walkthrough: <specific procedure name>
## Extended Case Study: <specific title>
## Common Mistakes
## Practice Exercises
## Solutions to Practice Exercises
## Review Questions
## Answers to Review Questions
## Key Definitions
## Chapter Summary
## Cross-References
## Further Reading
```

### 2.1 Learning Objectives

Six to ten objectives, each an infinitive phrase beginning with an observable verb (compute, evaluate,
design, draft, distinguish, conclude, reconcile, document). Not "understand" or "appreciate." Number them
`LO N.1`, `LO N.2`, and so on.

### 2.2 Standards and Guidance Map

A table with columns: `Source | Reference | What it requires that matters here`. Include AICPA AU-C sections,
PCAOB Auditing Standards, and relevant FASB ASC topics. Because AtlasFlow is an SEC issuer, PCAOB standards
govern the continuing case, but every chapter must also state the AICPA equivalent for readers auditing
private SaaS companies, and must call out where the two differ substantively. Where a standard's effective
date is recent, state the effective date. Add a line to the table only if the chapter actually discusses the
requirement.

### 2.3 Prerequisites and Chapter Dependencies

Two or three sentences naming the chapters a reader should have read first and the chapters that build on
this one.

### 2.4 Substantive sections

Numbered `N.1`, `N.2`, ... Use third-level headings (`### N.3.2`) freely. Each substantive section must
contain at least one of: a worked numeric example, a decision framework, a sample workpaper extract, or an
exhibit. Prose-only sections longer than about 600 words are a defect.

### 2.5 Step-by-Step Walkthrough

A single procedure executed end to end, in numbered steps, at the level of detail a staff auditor could
follow without asking a question. Every step must state: what you do, what you obtain, what you compare it
to, what conclusion the result supports, and what you do if the result is unexpected. Include real artifacts:
the query you run, the field names you request, the screen you look at, the tick marks you place, the numbers
you get. Minimum 12 steps. Prefer 20.

### 2.6 Extended Case Study

Structure:

```
### Background
### The Facts
### What the Engagement Team Did
### Analysis
### Resolution and Conclusion
### Workpaper Extract
### Lessons
```

The `Workpaper Extract` subsection must present a realistic memo or schedule, formatted as a workpaper, with
a workpaper index reference (for example, `WP 3200-14`), preparer and reviewer initials, dates, purpose,
source of information, procedures performed, results, and conclusion.

### 2.7 Common Mistakes

Minimum **ten** mistakes. Each formatted as:

```
### Mistake N.M — <short name>

**What it looks like.** ...
**Why it happens.** ...
**What goes wrong.** ...
**How to avoid it.** ...
```

Mistakes must be specific and diagnosable, not generic ("failing to plan properly" is not acceptable;
"treating the RPO disclosure as a footnote rather than as a recomputable population" is).

### 2.8 Practice Exercises

Minimum **twelve** exercises, numbered `Exercise N-1` through at least `Exercise N-12`, with an explicit
difficulty tag `[Foundational]`, `[Intermediate]`, or `[Advanced]`. The mix must include:

- at least four computational exercises requiring the reader to produce numbers;
- at least three judgment exercises requiring a written conclusion;
- at least two drafting exercises (write a memo paragraph, a confirmation request, a control description, a
  finding, a report paragraph);
- at least one exercise requiring the reader to find the error in a presented workpaper, memo, or
  calculation;
- at least one exercise that spans this chapter and a prior chapter.

Give the reader every number needed to solve the exercise. Never write "assume reasonable amounts."

### 2.9 Solutions to Practice Exercises

A complete worked solution for every exercise, in the same order, labeled `Solution N-1`. Computational
solutions must show the arithmetic, not just the answer. Judgment solutions must give the conclusion, the
reasoning, the authoritative hook, and at least one credible alternative answer with an explanation of why
it is weaker or why it is also defensible. Drafting solutions must contain actual model language of the
length requested.

### 2.10 Review Questions and Answers

Minimum **fifteen** short-answer review questions, numbered `RQ N-1`. Answers in a separate section, each two
to six sentences. Review questions test recall and comprehension; practice exercises test application. Do not
duplicate content between them.

### 2.11 Key Definitions

Minimum **twenty** terms, alphabetized, formatted as a definition list:

```
**Term.** Definition in one to four sentences, written so that it stands alone without the surrounding
chapter. Where the term has a technical definition in the professional literature, give it and cite the
source.
```

### 2.12 Chapter Summary

Eight to fifteen numbered takeaways, each a complete sentence carrying substantive content. Not a list of
topics covered.

### 2.13 Cross-References

A table with columns `Topic | Chapter | Why you would go there`.

### 2.14 Further Reading

Authoritative sources only: PCAOB standards and staff guidance, AICPA AU-C sections and audit guides, FASB
ASC topics and ASUs, SEC rules and staff guidance (SAB, C&DIs, Division of Corporation Finance guidance),
COSO frameworks, and IIA guidance. Do not invent titles, document numbers, or URLs. If you are not certain a
document exists with the exact title you are about to write, describe it generically instead ("the AICPA
audit guide covering revenue recognition") rather than fabricating a citation.

---

## 3. Depth expectations

The single most common failure mode for a chapter like these is *breadth without depth* — naming twelve
procedures instead of performing two. Prefer:

- **Numbers over adjectives.** Not "a significant increase in DSO," but "DSO rose from 61 days at
  December 31, 2024 to 68 days at December 31, 2025, a 11.5% increase, which on a $38,600 gross receivable
  balance implies approximately $4,000 of receivables that would not have existed at prior-year collection
  velocity."
- **Artifacts over description.** Show the confirmation letter. Show the SQL. Show the tick-mark legend.
  Show the sample selection table with all rows. Show the memo.
- **Judgment made visible.** When there is a range of acceptable answers, say so, give the range, say where
  in the range the answer being illustrated falls, and say what would move it.
- **Failure modes.** For every procedure, state what an unexpected result looks like and the next step.

## 4. Formatting conventions

| Element | Convention |
| --- | --- |
| Currency | Thousands of USD by default; state "(in thousands)" in table captions. Use `$1,450` for $1,450 thousand. Where whole dollars are used, say so. |
| Exhibits | `**Exhibit N-1. Caption.**` immediately above the table or block. Number sequentially through the chapter. |
| Tables | GitHub-flavored Markdown pipe tables. Header row required. Right-alignment is not required. |
| Code, queries, extracts | Fenced blocks with a language tag (`sql`, `python`, `text`). Use `text` for workpaper extracts, letters, and report language. |
| Emphasis | `**bold**` for defined terms at first use and for workpaper field labels. Italics for standard titles and for emphasis, sparingly. |
| Standard citations | `AU-C 315.16`, `AS 2110.59`, `ASC 606-10-25-27`. Do not abbreviate inconsistently. |
| Tick marks | Use footnote-style markers `(a)`, `(b)` in tables with a legend beneath. |
| Cross-references | "Chapter 12, §12.4" format. |
| Lists | Use `-` for unordered lists and `1.` for ordered lists. Do not nest deeper than two levels. |
| Headings | ATX (`##`). Never skip a level. |
| Line length | Wrap prose at approximately 110 characters. Tables may exceed. |

## 5. Terminology discipline

Use these terms consistently and correctly:

| Use | Not |
| --- | --- |
| risk of material misstatement (RMM) | "audit risk" when you mean RMM |
| inherent risk and control risk as separate assessments | a single blended "risk" |
| significant risk | "high risk" (a significant risk is a defined term) |
| relevant assertion | "assertion" alone, where relevance matters |
| substantive analytical procedure | "analytic" as a noun for a substantive test |
| test of details | "substantive test" where the distinction matters |
| deficiency / significant deficiency / material weakness | "finding," "issue," "exception" as synonyms for these graded terms |
| control deviation (in a test of controls) | "misstatement" |
| misstatement (in a test of details) | "error" |
| information produced by the entity (IPE) | "client-prepared schedule" where completeness and accuracy testing is the point |
| complementary user entity control (CUEC) | "client control at the service provider" |
| remaining performance obligation (RPO) | "backlog" without explanation |
| annual recurring revenue (ARR) | "revenue run rate" used interchangeably |

Spell out an acronym at first use in each chapter, then use the acronym.

## 6. Accuracy rules

1. **Do not fabricate authority.** Never invent a paragraph number, a standard title, an SEC comment letter,
   or a court case. If you are unsure of the exact citation, cite at the standard level (`AU-C 330`) rather
   than the paragraph level, or describe the requirement without a pinpoint cite.
2. **State the framework.** US GAAP and either PCAOB or AICPA standards. Where IFRS or ISAs differ in a way
   that matters to the chapter, note it briefly; do not attempt full IFRS/ISA coverage.
3. **Effective dates.** The continuing case is the FY2025 audit, reported in February 2026. Standards
   effective for periods ending on or after December 15, 2025 or earlier are in force. Where a chapter relies
   on a standard whose effective date is close to that line, say so.
4. **Do not overstate certainty in judgment areas.** Where practice varies, say that practice varies and
   describe the poles.
5. **Distinguish requirement from good practice.** If a standard requires something, say "requires." If it is
   common practice or firm methodology, say so. Never present firm methodology as a professional requirement.

## 7. Disclaimer requirement

The book-level disclaimer lives in `README.md` and `frontmatter/00-preface.md`. Individual chapters do not
repeat it, but chapters must not contain language that reads as legal or professional advice for a specific
engagement.

## 8. Self-check before finishing a chapter

Run through this list. A chapter that fails any item is not finished.

1. `bash tools/wordcount.sh chapters/chNN-slug.md` reports at least 5,000 words.
2. All required sections are present, in order, with the exact heading texts from §2.
3. At least 12 practice exercises, each with a complete solution.
4. At least 15 review questions, each with an answer.
5. At least 20 key definitions, alphabetized.
6. At least 10 common mistakes in the required four-part format.
7. The walkthrough has at least 12 numbered steps and names real fields, systems, and numbers.
8. The case study includes a formatted workpaper extract with an index reference.
9. Every table with a total row foots.
10. Every figure taken from the continuing case matches `case-materials/atlasflow-continuing-case.md`.
11. Exhibits are numbered sequentially with no gaps or duplicates.
12. No invented citations.
13. No emojis, no filler sentences, no "in conclusion."
14. Markdown renders: no unclosed fences, no broken tables, no heading-level skips.
