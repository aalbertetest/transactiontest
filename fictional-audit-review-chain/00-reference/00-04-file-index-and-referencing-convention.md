# 00-04 — File Index and Referencing Convention

---

## 1. The firm's indexing convention

Ashcroft Vane LLP indexes audit files by section letter and a three-digit number.

| Section | Contents |
|---|---|
| **A** | Planning, risk assessment, acceptance, independence, materiality, strategy |
| **B** | Internal control — understanding, evaluation and testing |
| **C** | Substantive procedures, by financial statement area |
| **D** | Completion, reporting and archiving |
| **E** | Component auditor instructions and returns (not reproduced in this repository) |
| **F** | Permanent file (constitution, contracts, prior year comparatives) |

A reference of the form `C-100/6` means **schedule 6 within workpaper C-100**. A reference of the
form `C-100 ¶14` means paragraph 14 of the narrative of that workpaper.

Review notes are prefixed by the reviewing level:

| Prefix | Level | Raised by | Example |
|---|---|---|---|
| `MRN-nnn` | 2 | Manager | `MRN-014` |
| `PRN-nn` | 3 | Engagement Partner | `PRN-06` |
| `EQR-nn` | — | Engagement Quality Reviewer | `EQR-03` |
| `INSP-Fnn` | 4 | Internal inspection (finding) | `INSP-F03` |
| `INSP-IPnn` | 4 | Internal inspection (improvement point) | `INSP-IP02` |
| `FRAOA-Fnn` | 5 | Regulator (finding) | `FRAOA-F07` |
| `FRAOA-RAnn` | 5 | Regulator (required action) | `FRAOA-RA09` |

`ISS-nn` is **not** a firm convention. It is a device of this repository for tracing one matter
across five levels that in reality would each number things differently. The mapping between all
of these systems is at
[`99-appendices/99-01-five-level-traceability-matrix.md`](../99-appendices/99-01-five-level-traceability-matrix.md).

---

## 2. Level 1 — the audit file

### A — Planning

| Ref | Title | Prepared | Reviewed | Issues |
|---|---|---|---|---|
| [`A-100`](../01-audit-file/A-planning/A-100-acceptance-and-continuance.md) | Engagement acceptance and continuance | S. Lindqvist | R. Belliveau | — |
| [`A-200`](../01-audit-file/A-planning/A-200-independence-and-ethics.md) | Independence, ethics and non-audit services | S. Lindqvist | R. Belliveau | Fee ratio breach |
| [`A-300`](../01-audit-file/A-planning/A-300-materiality.md) | Materiality determination | D. Ramanathan | S. Lindqvist | `ISS-02` |
| [`A-400`](../01-audit-file/A-planning/A-400-risk-assessment-and-significant-risks.md) | Understanding the entity; risk assessment; significant risks | D. Ramanathan | S. Lindqvist | `ISS-01`, `ISS-06`, `ISS-07` |
| [`A-500`](../01-audit-file/A-planning/A-500-fraud-risk-assessment.md) | Fraud risk assessment and team discussion | D. Ramanathan | S. Lindqvist | `ISS-01`, `ISS-08` |
| [`A-600`](../01-audit-file/A-planning/A-600-group-scoping.md) | Group audit scoping and component instructions | S. Lindqvist | R. Belliveau | Scoping coverage |
| [`A-700`](../01-audit-file/A-planning/A-700-audit-strategy-and-plan.md) | Overall audit strategy and detailed plan | S. Lindqvist | R. Belliveau | Resourcing |

### B — Controls

| Ref | Title | Prepared | Reviewed | Issues |
|---|---|---|---|---|
| [`B-100`](../01-audit-file/B-controls/B-100-control-environment-and-entity-level-controls.md) | Control environment and entity-level controls | D. Ramanathan | S. Lindqvist | Tone at the top |
| [`B-200`](../01-audit-file/B-controls/B-200-itgc-and-erp-migration.md) | IT general controls and the Aventine migration | Y. Demirci | **not reviewed** | `ISS-04` |
| [`B-300`](../01-audit-file/B-controls/B-300-controls-testing-and-deficiency-log.md) | Process controls testing and deficiency log | C. Nakamura | S. Lindqvist | `ISS-04` |

### C — Substantive procedures

| Ref | Title | Prepared | Reviewed | Issues |
|---|---|---|---|---|
| [`C-100`](../01-audit-file/C-substantive/C-100-contract-revenue-over-time.md) | Contract revenue recognised over time | D. Ramanathan | S. Lindqvist | **`ISS-01`** |
| [`C-200`](../01-audit-file/C-substantive/C-200-revenue-cutoff-and-sampling.md) | Revenue cut-off testing | C. Nakamura | S. Lindqvist | **`ISS-02`** |
| [`C-300`](../01-audit-file/C-substantive/C-300-subscription-revenue-principal-vs-agent.md) | Subscription revenue; principal versus agent | D. Ramanathan | S. Lindqvist | **`ISS-03`** |
| [`C-400`](../01-audit-file/C-substantive/C-400-inventory.md) | Inventories and provisioning | C. Nakamura | S. Lindqvist | — (clean) |
| [`C-500`](../01-audit-file/C-substantive/C-500-business-combination-kestrel.md) | Business combination — Kestrel Dynamics | A. Brennan-Sutton | **not reviewed** | **`ISS-05`** |
| [`C-600`](../01-audit-file/C-substantive/C-600-goodwill-impairment.md) | Goodwill impairment testing | D. Ramanathan | S. Lindqvist | **`ISS-06`** |
| [`C-700`](../01-audit-file/C-substantive/C-700-journal-entry-testing.md) | Journal entry testing | E. Balewa | S. Lindqvist | `ISS-04`, `ISS-08` |
| [`C-800`](../01-audit-file/C-substantive/C-800-related-parties.md) | Related parties | E. Balewa | S. Lindqvist | **`ISS-08`** |
| [`C-900`](../01-audit-file/C-substantive/C-900-going-concern.md) | Going concern | D. Ramanathan | S. Lindqvist | **`ISS-07`** |
| [`C-950`](../01-audit-file/C-substantive/C-950-subsequent-events-and-litigation.md) | Subsequent events and litigation | A. Brennan-Sutton | S. Lindqvist | Feeds `ISS-01` |

### D — Completion

| Ref | Title | Prepared | Reviewed | Issues |
|---|---|---|---|---|
| [`D-100`](../01-audit-file/D-completion/D-100-summary-of-audit-differences.md) | Summary of corrected and uncorrected misstatements | D. Ramanathan | R. Belliveau | `ISS-02` |
| [`D-200`](../01-audit-file/D-completion/D-200-audit-completion-memorandum.md) | Audit completion memorandum | S. Lindqvist | R. Belliveau | All |
| [`D-300`](../01-audit-file/D-completion/D-300-engagement-quality-review-record.md) | Engagement quality review record | P. Anand-Vasquez | — | **`ISS-09`** |
| [`D-400`](../01-audit-file/D-completion/D-400-audit-committee-report.md) | Report to the Audit Committee | S. Lindqvist | R. Belliveau | Communication |
| [`D-500`](../01-audit-file/D-completion/D-500-auditors-report.md) | Independent auditor's report | R. Belliveau | — | Key audit matters |
| [`D-600`](../01-audit-file/D-completion/D-600-file-assembly-and-archive-log.md) | File assembly and archive log | D. Ramanathan | — | **`ISS-10`** |

---

## 3. Levels 2 to 5

| Ref | Title |
|---|---|
| [`M-100`](../02-manager-review/M-100-review-approach-scope-and-coverage.md) | Manager review — approach, scope and coverage |
| [`M-200`](../02-manager-review/M-200-review-notes-register.md) | Manager review notes register (`MRN-001` – `MRN-049`) |
| [`M-300`](../02-manager-review/M-300-review-conclusion-memorandum.md) | Manager review conclusion memorandum |
| [`M-400`](../02-manager-review/M-400-coaching-and-performance-feedback.md) | Coaching notes and performance feedback |
| [`M-500`](../02-manager-review/M-500-matters-escalated-to-partner.md) | Matters escalated to the engagement partner |
| [`P-100`](../03-partner-review/P-100-partner-review-of-the-manager-review.md) | Partner review of the manager's review |
| [`P-200`](../03-partner-review/P-200-note-by-note-assessment-of-manager-clearances.md) | Note-by-note assessment of manager clearances |
| [`P-300`](../03-partner-review/P-300-partner-review-notes-and-additional-procedures.md) | Partner review notes (`PRN-01` – `PRN-19`) |
| [`P-400`](../03-partner-review/P-400-consultation-and-eqr-interaction-record.md) | Consultation and EQR interaction record |
| [`P-500`](../03-partner-review/P-500-partner-conclusion-and-authorisation-to-sign.md) | Partner conclusion and authorisation to sign |
| [`I-100`](../04-inspection-review/I-100-scope-methodology-and-inspector-independence.md) | Inspection scope, methodology and inspector independence |
| [`I-200`](../04-inspection-review/I-200-assessment-of-the-partner-review.md) | Assessment of the partner review |
| [`I-300`](../04-inspection-review/I-300-findings-register.md) | Inspection findings register |
| [`I-400`](../04-inspection-review/I-400-root-cause-analysis.md) | Root cause analysis |
| [`I-500`](../04-inspection-review/I-500-grading-determination-and-draft-to-final-changes.md) | Grading determination and draft-to-final changes |
| [`I-600`](../04-inspection-review/I-600-engagement-team-response.md) | Engagement team response |
| [`I-700`](../04-inspection-review/I-700-remediation-plan.md) | Remediation plan |
| [`R-100`](../05-regulator-review/R-100-mandate-scope-and-methodology.md) | Mandate, scope and methodology |
| [`R-200`](../05-regulator-review/R-200-assessment-of-the-firms-internal-inspection.md) | Assessment of the firm's internal inspection |
| [`R-300`](../05-regulator-review/R-300-independent-re-review-of-the-engagement-file.md) | Independent re-review of the engagement file |
| [`R-400`](../05-regulator-review/R-400-findings-and-severity-classification.md) | Findings and severity classification |
| [`R-500`](../05-regulator-review/R-500-systemic-root-cause-and-isqm1-conclusions.md) | Systemic root cause and ISQM 1 conclusions |
| [`R-600`](../05-regulator-review/R-600-required-actions-monitoring-and-sanctions.md) | Required actions, monitoring and sanctions |
| [`R-700`](../05-regulator-review/R-700-firm-response-and-regulator-reply.md) | Firm response and regulator reply |
| [`R-800`](../05-regulator-review/R-800-public-report-extract.md) | Public report extract |

---

## 4. Significant risks and the workpapers that address them

The firm's methodology requires the engagement partner to review every workpaper addressing a
significant risk. There are nine. The e-file audit trail records that **the partner opened five**.

| # | Significant risk | Workpaper | Partner opened? |
|---|---|---|:-:|
| 1 | Revenue recognition — contract estimates | `C-100` | ✔ |
| 2 | Revenue recognition — cut-off (presumed fraud risk) | `C-200` | ✖ |
| 3 | Revenue recognition — multi-element and agency | `C-300` | ✖ |
| 4 | Management override of controls | `C-700` | ✔ |
| 5 | Business combination accounting | `C-500` | ✖ |
| 6 | Goodwill impairment | `C-600` | ✔ |
| 7 | Going concern | `C-900` | ✔ |
| 8 | Related party completeness | `C-800` | ✖ |
| 9 | IT general controls following the ERP migration | `B-200` | ✔ (20 minutes) |

Four of the five workpapers the partner did not open contain issues in the spine
(`ISS-02`, `ISS-03`, `ISS-05`, `ISS-08`).

---

## 5. Coverage heat map

Who looked at what. `●` reviewed in substance · `○` opened only · `✖` not opened.

| Workpaper | Manager | Partner | EQR | Inspection | Regulator |
|---|:-:|:-:|:-:|:-:|:-:|
| `A-100` Acceptance | ● | ○ | ● | ○ | ● |
| `A-200` Independence | ● | ● | ○ | ● | ● |
| `A-300` Materiality | ● | ○ | ● | ● | ● |
| `A-400` Risk assessment | ● | ○ | ● | ● | ● |
| `A-500` Fraud | ● | ○ | ○ | ● | ● |
| `A-600` Group scoping | ● | ● | ○ | ● | ● |
| `A-700` Strategy | ● | ● | ○ | ○ | ● |
| `B-100` Control environment | ● | ✖ | ✖ | ● | ● |
| **`B-200` ITGC** | **✖** | ○ | ✖ | ● | ● |
| `B-300` Controls testing | ● | ✖ | ✖ | ● | ● |
| **`C-100` Contract revenue** | ● | ● | ● (late) | ● | ● |
| **`C-200` Cut-off** | ● | ✖ | ✖ | ● | ● |
| **`C-300` Agency** | ● | ✖ | ✖ | ● | ● |
| `C-400` Inventory | ● | ✖ | ✖ | ● | ○ |
| **`C-500` Business combination** | **✖** | ✖ | ✖ | ● | ● |
| **`C-600` Goodwill** | ● | ● | ● (late) | ● | ● |
| `C-700` Journals | ● | ● | ○ | ● | ● |
| **`C-800` Related parties** | ● | ✖ | ✖ | ● | ● |
| **`C-900` Going concern** | ● | ● | ● (late) | ● | ● |
| `C-950` Subsequent events | ● | ○ | ○ | ● | ● |
| `D-100` Misstatements | ● | ● | ● | ● | ● |
| `D-200` Completion memo | ● | ● | ● | ● | ● |
| `D-300` EQR record | — | ○ | ● | ● | ● |
| `D-400` AC report | ● | ● | ● | ● | ● |
| `D-500` Auditor's report | ● | ● | ● | ● | ● |
| `D-600` Archive log | ✖ | ✖ | ✖ | ○ | ● |

Two workpapers were reviewed by **nobody** at Levels 2 or 3 before the report was signed: `B-200`
and `C-500`. Both contain issues in the spine.
