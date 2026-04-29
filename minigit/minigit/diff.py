"""
Line-based diff using the Longest Common Subsequence (LCS) algorithm.

The implementation is a classic Myers-diff-style unified diff produced
via the standard DP LCS table.  Output format mirrors unified diff so
it can be read by anyone familiar with ``patch(1)``.

The public API is intentionally small:

    unified_diff(a_lines, b_lines, fromfile, tofile) -> str
    diff_blobs(objects_dir, digest_a, digest_b, path)  -> str
    diff_working_vs_index(objects_dir, index, work_dir)-> dict[str, str]
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence

from .objects import read_object


# ---------------------------------------------------------------------------
# Core LCS / diff machinery
# ---------------------------------------------------------------------------

def _lcs_table(a: Sequence[str], b: Sequence[str]) -> list[list[int]]:
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp


def _diff_ops(a: Sequence[str], b: Sequence[str]) -> list[tuple[str, str]]:
    """
    Return a list of (op, line) where op is ' ' (context), '-' (removed),
    or '+' (added).
    """
    dp = _lcs_table(a, b)
    ops: list[tuple[str, str]] = []

    i, j = len(a), len(b)
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            ops.append((" ", a[i - 1]))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            ops.append(("+", b[j - 1]))
            j -= 1
        else:
            ops.append(("-", a[i - 1]))
            i -= 1

    ops.reverse()
    return ops


def unified_diff(
    a_lines: list[str],
    b_lines: list[str],
    fromfile: str = "a",
    tofile: str = "b",
    context: int = 3,
) -> str:
    """
    Produce a unified-diff string between *a_lines* and *b_lines*.
    Lines should include their trailing newline (or not – both work).
    """
    ops = _diff_ops(a_lines, b_lines)

    # Map each op back to its source line numbers.
    a_idx = 0  # current position in a
    b_idx = 0

    # Annotate ops with line numbers
    annotated: list[tuple[str, str, int, int]] = []
    for op, line in ops:
        if op == " ":
            annotated.append((op, line, a_idx + 1, b_idx + 1))
            a_idx += 1
            b_idx += 1
        elif op == "-":
            annotated.append((op, line, a_idx + 1, b_idx + 1))
            a_idx += 1
        else:  # "+"
            annotated.append((op, line, a_idx + 1, b_idx + 1))
            b_idx += 1

    # Group into hunks: regions containing at least one change, padded with
    # 'context' unchanged lines on each side.
    change_positions = [i for i, (op, *_) in enumerate(annotated) if op != " "]
    if not change_positions:
        return ""

    # Build hunk ranges (start, end) in annotated index space.
    hunks: list[tuple[int, int]] = []
    hunk_start = max(0, change_positions[0] - context)
    hunk_end = min(len(annotated), change_positions[0] + context + 1)

    for pos in change_positions[1:]:
        if pos - context <= hunk_end:
            hunk_end = min(len(annotated), pos + context + 1)
        else:
            hunks.append((hunk_start, hunk_end))
            hunk_start = max(0, pos - context)
            hunk_end = min(len(annotated), pos + context + 1)
    hunks.append((hunk_start, hunk_end))

    # Render
    out_lines: list[str] = [f"--- {fromfile}", f"+++ {tofile}"]

    for h_start, h_end in hunks:
        chunk = annotated[h_start:h_end]
        a_start = chunk[0][2]
        b_start = chunk[0][3]
        a_count = sum(1 for op, *_ in chunk if op in (" ", "-"))
        b_count = sum(1 for op, *_ in chunk if op in (" ", "+"))
        out_lines.append(f"@@ -{a_start},{a_count} +{b_start},{b_count} @@")
        for op, line, *_ in chunk:
            stripped = line.rstrip("\n")
            out_lines.append(f"{op}{stripped}")

    return "\n".join(out_lines) + "\n"


# ---------------------------------------------------------------------------
# Helpers that operate on the object store
# ---------------------------------------------------------------------------

def diff_blobs(
    objects_dir: Path,
    digest_a: str | None,
    digest_b: str | None,
    path: str,
) -> str:
    """Diff two blob digests (either may be None for new/deleted files)."""
    def load(digest: str | None) -> list[str]:
        if digest is None:
            return []
        _, data = read_object(objects_dir, digest)
        return data.decode(errors="replace").splitlines(keepends=True)

    a_lines = load(digest_a)
    b_lines = load(digest_b)
    fromfile = f"a/{path}" if digest_a else "/dev/null"
    tofile = f"b/{path}" if digest_b else "/dev/null"
    return unified_diff(a_lines, b_lines, fromfile=fromfile, tofile=tofile)


def diff_index_vs_commit(
    objects_dir: Path,
    index: dict[str, str],
    tree_flat: dict[str, str],
) -> dict[str, str]:
    """
    Return path → unified-diff for every file that differs between
    *index* (staged) and *tree_flat* (last commit's tree, already expanded).
    """
    all_paths = set(index) | set(tree_flat)
    results: dict[str, str] = {}
    for path in sorted(all_paths):
        da = tree_flat.get(path)
        db = index.get(path)
        if da != db:
            results[path] = diff_blobs(objects_dir, da, db, path)
    return results


def diff_working_vs_index(
    objects_dir: Path,
    index: dict[str, str],
    work_dir: Path,
) -> dict[str, str]:
    """
    Return path → unified-diff for every tracked file whose working-tree
    content differs from what is staged in *index*.
    """
    results: dict[str, str] = {}
    for path, blob_digest in sorted(index.items()):
        full = work_dir / path
        if not full.exists():
            results[path] = diff_blobs(objects_dir, blob_digest, None, path)
            continue
        working_content = full.read_bytes()
        _, stored = read_object(objects_dir, blob_digest)
        if working_content != stored:
            # Write a temporary blob for the working-tree version.
            from .objects import write_object  # avoid circular at module level
            wt_digest = write_object(objects_dir, "blob", working_content)
            results[path] = diff_blobs(objects_dir, blob_digest, wt_digest, path)
    return results
