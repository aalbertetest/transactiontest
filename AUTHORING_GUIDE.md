# Authoring Guide — Fictional Revenue Recognition Audit Findings

All content in this repository is **fictional**. Entity names, people, dates, dollar
amounts, contract numbers, and quotations are invented for training, template, and
methodology-demonstration purposes. Nothing here describes a real audit, a real client,
or a real person, and nothing here is accounting or auditing advice for a live engagement.

## Scope of the collection

100 findings, `RR-001` through `RR-100`, each in its own file under `findings/`.
Each finding is a self-contained written audit finding covering a distinct revenue
recognition failure mode. The register of assigned topics is in `TOPICS.md`.

## Required file structure

Every finding file follows exactly this structure. Header fields and heading text must
match character for character so the validator in `scripts/check_word_counts.py` can
parse the file.

```markdown
# RR-0NN — <Title from TOPICS.md>

| Field | Detail |
| --- | --- |
| Finding reference | RR-0NN |
| Entity (fictional) | <invented entity name> |
| Sector / industry | <sector> |
| Fiscal year audited | <FY> |
| Framework(s) | <e.g. ASC 606; IFRS 15; GASB 33; GAGAS 2024; Uniform Guidance 2 CFR 200> |
| Assertion(s) affected | <e.g. occurrence, cutoff, accuracy, classification> |
| Quantified effect | <dollar amount and direction of misstatement> |
| Risk rating | <High / Moderate / Low> |
| Repeat finding | <Yes (prior-year ref) / No> |

## Background

## Condition

## Criteria

## Cause

## Effect

## Recommendation

## Management Response
```

## Section content requirements

**Every one of the seven sections must be at least 300 words.** This is a hard floor, not
a target. Aim for 320–420 words per section so that minor edits cannot push a section
under the limit. A finding therefore runs roughly 2,300–2,900 words.

Each section has a specific job, and the jobs must not bleed into one another:

- **Background** — Orient a reader who knows nothing about the entity. Describe the
  business or program, the revenue streams and their relative size, the contracting or
  billing model, the systems that process revenue, the organizational structure and who
  owns the process, the relevant history (system conversions, acquisitions, growth,
  prior-year findings), and why the auditor selected this area for testing. Describe the
  audit scope and procedures performed, including population sizes and sampling approach.
  Background sets the stage; it does not state the deficiency.
- **Condition** — The factual "what is." State precisely what the auditor observed,
  with sample sizes, exception counts, exception rates, dollar amounts, contract and
  invoice identifiers, dates, and the specific mechanics of what went wrong. Include
  detail on how the exceptions were identified and how they were corroborated
  (documents inspected, reperformance, confirmations, interviews). Condition is evidence,
  not judgment about causes.
- **Criteria** — The authoritative "what should be." Cite specific standards, paragraphs,
  regulations, contract clauses, or entity policies, and explain what each requires and
  how it applies to these facts. Use realistic citations (for example ASC 606-10-25-1,
  ASC 606-10-32-11, IFRS 15.31, GASB Statement No. 33 paragraph 21, 2 CFR 200.305,
  AU-C 240, GAGAS 2024 8.116, COSO 2013 Principle 10). Explain the internal control
  criteria as well as the accounting criteria where relevant.
- **Cause** — Why the condition arose. Distinguish root cause from symptom. Cover
  process design gaps, control gaps, information and communication breakdowns, staffing
  and competence, system configuration and access, incentive structures, tone at the top,
  and monitoring failures. Explain what the entity's existing controls were designed to
  do and precisely where the design or operation broke down.
- **Effect** — The consequence. Quantify the misstatement and its direction, describe the
  effect on the financial statements and on specific line items and ratios, on interim and
  comparative periods, on covenants, on incentive compensation, on regulatory filings and
  grant compliance, and on the auditor's report and opinion. Address the severity
  evaluation (deficiency, significant deficiency, or material weakness) and the reasoning
  behind that conclusion, including potential magnitude as distinct from actual
  misstatement.
- **Recommendation** — Specific, actionable, and testable corrective actions. Recommend
  process and control changes, system and configuration changes, documentation and
  policy changes, training, monitoring and metrics, an owner and a target date for each
  action, and how management should validate that the remediation operated effectively.
  Address both correcting the identified misstatement and preventing recurrence.
- **Management Response** — Written in management's voice, first person plural, as a
  realistic response letter excerpt. State agreement, partial agreement, or disagreement;
  where management partially disagrees, give management's reasoning. Include a
  remediation plan with named fictional role titles, milestones, dates, and any
  resources being committed. Realistic responses sometimes push back on scope, magnitude,
  or characterization while still committing to corrective action.

## Style rules

- Professional audit-report register: precise, neutral, and impersonal. Avoid
  sensationalism and avoid accusatory language; describe conduct and evidence, not motive,
  unless the finding is explicitly about fraud risk, in which case use the language of
  suspicion and referral rather than conclusion.
- Prose paragraphs are the default. Bulleted or numbered lists are acceptable inside
  **Condition** (exception schedules) and **Recommendation** (numbered corrective actions),
  but each section must still read as substantive written analysis rather than a list of
  fragments.
- Use consistent, invented identifiers within a finding: contract numbers, invoice
  numbers, customer codes, journal entry numbers, and system names should recur coherently
  across sections of the same finding.
- Vary entity names, sectors, geographies, fiscal year-ends, and dollar magnitudes across
  findings. Do not reuse an entity name across two findings.
- Do not name real companies, real people, real auditors, or real audit firms. Do not
  reuse the names of well-known accounting scandals or their participants.
- Keep dollar amounts internally consistent: the amount in the header table must agree
  with the amounts discussed in Condition and Effect.
- Do not use em dashes inside body prose; use commas, semicolons, or parentheses. Em
  dashes are used only in the title line of each file.

## Validation

Run the validator before committing:

```bash
python3 scripts/check_word_counts.py
```

It fails if any file is missing a required section, if sections appear out of order, or
if any section falls below 300 words.
