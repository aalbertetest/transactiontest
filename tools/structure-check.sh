#!/usr/bin/env bash
# Verify that each chapter contains the sections required by docs/style-guide.md and meets the
# minimum counts for exercises, review questions, definitions, and common mistakes.
#
# Usage:
#   tools/structure-check.sh                 # all chapters
#   tools/structure-check.sh chapters/ch07-accounts-receivable.md

set -uo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

REQUIRED_SECTIONS=(
  "## Learning Objectives"
  "## Standards and Guidance Map"
  "## Prerequisites and Chapter Dependencies"
  "## Step-by-Step Walkthrough"
  "## Extended Case Study"
  "## Common Mistakes"
  "## Practice Exercises"
  "## Solutions to Practice Exercises"
  "## Review Questions"
  "## Answers to Review Questions"
  "## Key Definitions"
  "## Chapter Summary"
  "## Cross-References"
  "## Further Reading"
)

MIN_EXERCISES=12
MIN_SOLUTIONS=12
MIN_REVIEW_Q=15
MIN_DEFINITIONS=20
MIN_MISTAKES=10
MIN_WALKTHROUGH_STEPS=12

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  mapfile -t files < <(find "$repo_root/chapters" -maxdepth 1 -name 'ch*.md' | sort)
fi

overall=0

for f in "${files[@]}"; do
  base=$(basename "$f")
  problems=()

  if [ ! -f "$f" ]; then
    echo "== $base: MISSING FILE"
    overall=1
    continue
  fi

  for section in "${REQUIRED_SECTIONS[@]}"; do
    if ! grep -qF "$section" "$f"; then
      problems+=("missing section: $section")
    fi
  done

  words=$(wc -w < "$f" | tr -d ' ')
  [ "$words" -lt 5000 ] && problems+=("word count $words is below 5000")

  exercises=$(grep -cE '^### Exercise ' "$f")
  [ "$exercises" -lt "$MIN_EXERCISES" ] && problems+=("$exercises exercises (need $MIN_EXERCISES)")

  solutions=$(grep -cE '^### Solution ' "$f")
  [ "$solutions" -lt "$MIN_SOLUTIONS" ] && problems+=("$solutions solutions (need $MIN_SOLUTIONS)")

  if [ "$exercises" -ne "$solutions" ]; then
    problems+=("exercise count ($exercises) does not equal solution count ($solutions)")
  fi

  reviewq=$(grep -cE '^\*\*RQ [0-9]+-[0-9]+\.?\*\*|^RQ [0-9]+-[0-9]+\.' "$f")
  [ "$reviewq" -lt "$MIN_REVIEW_Q" ] && problems+=("$reviewq review questions detected (need $MIN_REVIEW_Q)")

  mistakes=$(grep -cE '^### Mistake ' "$f")
  [ "$mistakes" -lt "$MIN_MISTAKES" ] && problems+=("$mistakes common mistakes (need $MIN_MISTAKES)")

  # Definitions are bold-lead terms inside the Key Definitions section.
  defs=$(awk '/^## Key Definitions/{flag=1;next}/^## Chapter Summary/{flag=0}flag' "$f" | grep -cE '^\*\*[^*]+\.?\*\*')
  [ "$defs" -lt "$MIN_DEFINITIONS" ] && problems+=("$defs key definitions (need $MIN_DEFINITIONS)")

  steps=$(awk '/^## Step-by-Step Walkthrough/{flag=1;next}/^## Extended Case Study/{flag=0}flag' "$f" \
    | grep -cE '^\*\*Step [0-9]+|^### Step [0-9]+|^[0-9]+\. ')
  [ "$steps" -lt "$MIN_WALKTHROUGH_STEPS" ] && problems+=("$steps walkthrough steps (need $MIN_WALKTHROUGH_STEPS)")

  # Unbalanced code fences.
  fences=$(grep -cE '^```' "$f")
  if [ $((fences % 2)) -ne 0 ]; then
    problems+=("odd number of code fences ($fences) — likely unclosed block")
  fi

  if [ "${#problems[@]}" -eq 0 ]; then
    printf '== %-42s OK  (%s words, %s exercises, %s RQs, %s defs)\n' \
      "$base" "$words" "$exercises" "$reviewq" "$defs"
  else
    overall=1
    printf '== %-42s PROBLEMS\n' "$base"
    for p in "${problems[@]}"; do
      echo "     - $p"
    done
  fi
done

exit "$overall"
