# minigit

A minimal, Git-like version-control system written in pure Python (stdlib only).

## Features

| Command | Description |
|---------|-------------|
| `init` | Initialise a new repository |
| `add` | Stage files |
| `commit` | Record a snapshot |
| `status` | Show staged / unstaged / untracked files |
| `log` | Human-readable commit history |
| `diff` | Line-level unified diff (working tree or staged) |
| `checkout` | Restore working tree to a previous commit or branch |

---

## Quick start

```bash
pip install -e /path/to/minigit   # install from source
mkdir myproject && cd myproject

minigit init --name "Alice" --email "alice@example.com"

echo "# Hello" > README.md
minigit add README.md
minigit commit -m "Initial commit"

echo "First line" > notes.txt
minigit add notes.txt
minigit commit -m "Add notes"

# Edit a file without staging
echo "Second line" >> notes.txt
minigit status
minigit diff

# Stage the edit and inspect the staged diff
minigit add notes.txt
minigit diff --staged

# View history
minigit log

# Go back to the first commit (use the digest from log output)
minigit checkout <first-12-chars-of-digest>
```

---

## Repository layout

```
myproject/
├── .minigit/
│   ├── objects/          Content-addressed object store
│   │   └── <xx>/         First 2 hex chars of SHA-256 digest
│   │       └── <62-hex>  Remaining 62 chars; zlib-compressed payload
│   ├── refs/
│   │   └── heads/
│   │       └── main      Plain text file containing the tip commit digest
│   ├── HEAD              "ref: refs/heads/main" (or bare digest for detached)
│   ├── index             JSON: { "relative/path": "blob-digest", … }
│   └── config            JSON: { "user": { "name": …, "email": … } }
├── README.md
└── notes.txt
```

---

## Design decisions

### Content-addressed storage

Every stored piece of data (blob, tree, commit) is identified solely by the
SHA-256 hash of its content.  This mirrors Git's object model and provides
several properties for free:

* **Deduplication** – identical file content is stored once regardless of
  how many commits reference it.
* **Integrity** – reading an object and re-hashing it lets you detect
  on-disk corruption without extra bookkeeping.
* **Determinism** – the same sequence of operations always produces the
  same object digests, making tests reliable and reproducible.

SHA-256 (64-hex characters) was chosen over Git's SHA-1 to avoid the known
collision vulnerabilities.

### Object format

Inspired directly by Git's loose-object layout:

```
<type> <byte-length>\0<raw-content>
```

The header is prepended to the content before hashing so that a blob
containing `"blob 5\0hello"` as its bytes cannot collide with an actual blob
object whose content happens to start with that string.  The payload is then
zlib-compressed on disk to save space.

### Tree objects

A tree maps file names to `(mode, digest)` pairs in a binary record format
(mode + name as a NUL-terminated string, followed by the raw 32-byte digest).
Entries are sorted alphabetically before serialisation so the tree digest is
deterministic regardless of insertion order.

Sub-directory support is handled recursively: a path like `src/main.py` in
the index results in a nested tree object for `src/`.

### Index / staging area

The index (`index` JSON file) is a flat `path → blob-digest` dictionary.
`add` hashes the working-tree file into the object store and updates the
entry; `commit` builds a tree object from the full index snapshot.  This
intentionally mirrors Git's single-level index, keeping the implementation
simple while still supporting the staged-vs-unstaged distinction.

### Commit graph

A commit object stores:
* the root tree digest
* zero or more parent commit digests (first-parent chain for `log`)
* author / committer identity and a Unix timestamp
* a free-form text message

The format is plain UTF-8 text with a blank-line separator between header
fields and the message body, making commits human-readable with any text
editor.  The history graph is a directed acyclic graph (DAG); `iter_commits`
walks the first-parent chain from HEAD to the root.

### Diff algorithm

The diff engine uses a classic **Longest Common Subsequence (LCS)** dynamic-
programming table (O(mn) time, O(mn) space) to compute the edit script
between two sequences of lines.  The result is rendered as a **unified diff**
with configurable context lines (default: 3).

A production-grade implementation would use Myers' O(D) algorithm (which Git
uses) for large files, but LCS is easier to reason about and sufficient for a
teaching-oriented tool.

### Checkout

`checkout` resolves the target (branch name, full digest, or short prefix) to
a commit, reads its tree, and:

1. Deletes working-tree files that exist in the current HEAD tree but not the
   target tree (to avoid stale files).
2. Writes all files from the target tree to the working directory.
3. Resets the index to the target tree.
4. Updates HEAD (symbolic if a branch name was given, detached otherwise).

No merge logic is attempted; uncommitted changes will be silently overwritten,
matching the simplest possible semantics.

---

## Running the tests

```bash
pip install -e ".[dev]"   # or just: pip install pytest
pytest -v
```

The test suite covers:

* **`test_objects.py`** – write/read round-trips, idempotency, type
  separation, missing-object errors.
* **`test_commit.py`** – serialisation round-trips, multi-line messages,
  parent-chain integrity, `iter_commits` traversal order.
* **`test_diff.py`** – unified-diff output, hunk generation, blob-diff
  helpers, index-vs-commit diffs.
* **`test_repo.py`** – full integration scenarios: init, add, commit, status,
  diff, checkout, error conditions.
