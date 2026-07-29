#!/usr/bin/env python3
"""Validate the structure and per-section word counts of the finding files.

Each file under findings/ must contain the seven required level-two sections, in the
required order, and every section must contain at least MIN_WORDS words of body text.
Exits non-zero and prints a report if any file fails.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

MIN_WORDS = 300

REQUIRED_SECTIONS = [
    "Background",
    "Condition",
    "Criteria",
    "Cause",
    "Effect",
    "Recommendation",
    "Management Response",
]

FINDINGS_DIR = Path(__file__).resolve().parent.parent / "findings"

HEADING_RE = re.compile(r"^##\s+(.*?)\s*$", re.MULTILINE)
WORD_RE = re.compile(r"[0-9A-Za-z][0-9A-Za-z'’./%$,-]*")


def split_sections(text: str) -> list[tuple[str, str]]:
    """Return [(heading, body), ...] for every level-two heading, in document order."""
    matches = list(HEADING_RE.finditer(text))
    sections = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        sections.append((match.group(1), text[start:end]))
    return sections


def count_words(body: str) -> int:
    """Count words in a section body, ignoring markdown table rows and list markers."""
    cleaned_lines = []
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            continue
        cleaned_lines.append(re.sub(r"^\s*(?:[-*+]|\d+\.)\s+", "", line))
    return len(WORD_RE.findall(" ".join(cleaned_lines)))


def check_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    problems: list[str] = []

    sections = split_sections(text)
    headings = [heading for heading, _ in sections]

    if headings != REQUIRED_SECTIONS:
        missing = [s for s in REQUIRED_SECTIONS if s not in headings]
        unexpected = [h for h in headings if h not in REQUIRED_SECTIONS]
        if missing:
            problems.append(f"missing section(s): {', '.join(missing)}")
        if unexpected:
            problems.append(f"unexpected section(s): {', '.join(unexpected)}")
        if not missing and not unexpected:
            problems.append(f"sections out of order: {' > '.join(headings)}")

    for heading, body in sections:
        if heading not in REQUIRED_SECTIONS:
            continue
        words = count_words(body)
        if words < MIN_WORDS:
            problems.append(f"'{heading}' has {words} words (minimum {MIN_WORDS})")

    if not text.startswith("# RR-"):
        problems.append("title line must start with '# RR-'")

    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help="specific finding files to check (default: every RR-*.md under findings/)",
    )
    parser.add_argument(
        "--expected",
        type=int,
        default=100,
        help="number of finding files expected in findings/ (0 disables the check)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="print per-section word counts for every file",
    )
    args = parser.parse_args()

    if args.paths:
        paths = sorted(args.paths)
        args.expected = 0
    else:
        paths = sorted(FINDINGS_DIR.glob("RR-*.md"))
    if not paths:
        print(f"no finding files found in {FINDINGS_DIR}")
        return 1

    failures = 0
    total_words = 0
    for path in paths:
        problems = check_file(path)
        text = path.read_text(encoding="utf-8")
        sections = split_sections(text)
        total_words += sum(count_words(body) for _, body in sections)
        if args.verbose:
            counts = ", ".join(f"{h}={count_words(b)}" for h, b in sections)
            print(f"{path.name}: {counts}")
        if problems:
            failures += 1
            print(f"FAIL {path.name}")
            for problem in problems:
                print(f"     - {problem}")

    print(f"\nchecked {len(paths)} file(s); {failures} failed")
    print(f"total section word count: {total_words:,}")

    if args.expected and len(paths) != args.expected:
        print(f"expected {args.expected} finding files, found {len(paths)}")
        return 1

    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
