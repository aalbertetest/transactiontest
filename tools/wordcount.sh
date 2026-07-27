#!/usr/bin/env bash
# Report word counts for textbook chapters and flag any chapter below the 5,000-word minimum.
#
# Usage:
#   tools/wordcount.sh                 # all chapters
#   tools/wordcount.sh chapters/ch01-audit-planning.md [more files...]
#
# Exit status is 1 if any inspected chapter file is below the minimum.

set -uo pipefail

MINIMUM=${MINIMUM:-5000}
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

if [ "$#" -gt 0 ]; then
  files=("$@")
else
  mapfile -t files < <(find "$repo_root/chapters" -maxdepth 1 -name 'ch*.md' | sort)
fi

if [ "${#files[@]}" -eq 0 ]; then
  echo "No chapter files found."
  exit 0
fi

printf '%-46s %10s %8s\n' "FILE" "WORDS" "STATUS"
printf '%-46s %10s %8s\n' "----------------------------------------------" "----------" "--------"

failed=0
total=0
for f in "${files[@]}"; do
  if [ ! -f "$f" ]; then
    printf '%-46s %10s %8s\n' "$(basename "$f")" "-" "MISSING"
    failed=1
    continue
  fi
  words=$(wc -w < "$f" | tr -d ' ')
  total=$((total + words))
  if [ "$words" -lt "$MINIMUM" ]; then
    status="SHORT"
    failed=1
  else
    status="OK"
  fi
  printf '%-46s %10s %8s\n' "$(basename "$f")" "$words" "$status"
done

printf '%-46s %10s %8s\n' "----------------------------------------------" "----------" "--------"
printf '%-46s %10s\n' "TOTAL (${#files[@]} file(s))" "$total"
echo
echo "Minimum per chapter: ${MINIMUM} words."

exit "$failed"
