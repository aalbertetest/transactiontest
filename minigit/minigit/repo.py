"""
Repository abstraction: manages the .minigit directory layout and
exposes the high-level operations (init, add, commit, status, log,
diff, checkout) used by the CLI.

.minigit layout
---------------
    .minigit/
        objects/          – content-addressed object store
        HEAD              – text file: "ref: refs/heads/<branch>"
                           or a bare commit digest (detached HEAD)
        refs/
            heads/
                <branch>  – text file containing a commit digest
        index             – JSON: { "path": "blob-digest", ... }
        config            – JSON: { "user": { "name": ..., "email": ... } }
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Optional

from .commit import CommitData, iter_commits, read_commit, write_commit
from .diff import diff_index_vs_commit, diff_working_vs_index
from .objects import read_object, write_object
from .tree import read_tree_flat, write_tree_from_index


MINIGIT_DIR = ".minigit"


class RepoError(Exception):
    pass


class Repo:
    def __init__(self, work_dir: Path):
        self.work_dir = work_dir.resolve()
        self.minigit_dir = self.work_dir / MINIGIT_DIR
        self.objects_dir = self.minigit_dir / "objects"
        self.refs_dir = self.minigit_dir / "refs" / "heads"
        self.head_path = self.minigit_dir / "HEAD"
        self.index_path = self.minigit_dir / "index"
        self.config_path = self.minigit_dir / "config"

    # ------------------------------------------------------------------
    # Repository discovery (class method)
    # ------------------------------------------------------------------

    @classmethod
    def find(cls, start: Optional[Path] = None) -> "Repo":
        """Walk upward from *start* (default: cwd) to find a .minigit dir."""
        path = Path(start or os.getcwd()).resolve()
        for candidate in [path, *path.parents]:
            if (candidate / MINIGIT_DIR).is_dir():
                return cls(candidate)
        raise RepoError("not a minigit repository (no .minigit directory found)")

    # ------------------------------------------------------------------
    # Init
    # ------------------------------------------------------------------

    def init(self, author_name: str = "You", author_email: str = "you@example.com") -> None:
        if self.minigit_dir.exists():
            raise RepoError(f"repository already initialised at {self.work_dir}")
        self.objects_dir.mkdir(parents=True)
        self.refs_dir.mkdir(parents=True)
        self.head_path.write_text("ref: refs/heads/main\n")
        self._write_index({})
        self.config_path.write_text(
            json.dumps({"user": {"name": author_name, "email": author_email}}, indent=2)
        )

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _read_index(self) -> dict[str, str]:
        if not self.index_path.exists():
            return {}
        return json.loads(self.index_path.read_text())

    def _write_index(self, index: dict[str, str]) -> None:
        self.index_path.write_text(json.dumps(index, indent=2))

    def _read_config(self) -> dict:
        if not self.config_path.exists():
            return {"user": {"name": "Unknown", "email": "unknown@example.com"}}
        return json.loads(self.config_path.read_text())

    def _read_head_ref(self) -> tuple[bool, str]:
        """
        Return (is_symbolic, value).
        is_symbolic=True  → value is a branch name ("main")
        is_symbolic=False → value is a bare commit digest
        """
        text = self.head_path.read_text().strip()
        if text.startswith("ref: refs/heads/"):
            return True, text[len("ref: refs/heads/"):]
        return False, text

    def _resolve_head(self) -> Optional[str]:
        """Return the commit digest HEAD points to, or None if no commits yet."""
        is_sym, value = self._read_head_ref()
        if is_sym:
            ref_file = self.refs_dir / value
            if not ref_file.exists():
                return None
            return ref_file.read_text().strip()
        return value

    def _update_head(self, commit_digest: str) -> None:
        is_sym, value = self._read_head_ref()
        if is_sym:
            ref_file = self.refs_dir / value
            ref_file.write_text(commit_digest + "\n")
        else:
            self.head_path.write_text(commit_digest + "\n")

    def _head_tree_flat(self) -> dict[str, str]:
        """Return the flat path→blob-digest mapping for HEAD's tree."""
        head = self._resolve_head()
        if head is None:
            return {}
        c = read_commit(self.objects_dir, head)
        return read_tree_flat(self.objects_dir, c.tree)

    def _list_working_files(self) -> set[str]:
        """All non-.minigit files relative to work_dir."""
        result: set[str] = set()
        for p in self.work_dir.rglob("*"):
            if p.is_file():
                rel = p.relative_to(self.work_dir)
                if rel.parts[0] != MINIGIT_DIR:
                    result.add(str(rel))
        return result

    # ------------------------------------------------------------------
    # add
    # ------------------------------------------------------------------

    def add(self, paths: list[str]) -> None:
        index = self._read_index()
        for path_str in paths:
            p = Path(path_str)
            if not p.is_absolute():
                p = self.work_dir / p
            p = p.resolve()
            if not p.exists():
                raise RepoError(f"pathspec '{path_str}' did not match any files")
            if p.is_dir():
                for child in p.rglob("*"):
                    if child.is_file():
                        self._add_file(child, index)
            else:
                self._add_file(p, index)
        self._write_index(index)

    def _add_file(self, abs_path: Path, index: dict[str, str]) -> None:
        rel = str(abs_path.relative_to(self.work_dir))
        data = abs_path.read_bytes()
        digest = write_object(self.objects_dir, "blob", data)
        index[rel] = digest

    # ------------------------------------------------------------------
    # commit
    # ------------------------------------------------------------------

    def commit(self, message: str) -> str:
        index = self._read_index()
        if not index:
            raise RepoError("nothing to commit (index is empty)")

        head_tree = self._head_tree_flat()
        if index == head_tree:
            raise RepoError("nothing to commit, working tree clean")

        cfg = self._read_config()
        user = cfg.get("user", {})
        author_name = user.get("name", "Unknown")
        author_email = user.get("email", "unknown@example.com")

        tree_digest = write_tree_from_index(self.objects_dir, index)
        parents = []
        head = self._resolve_head()
        if head:
            parents = [head]

        c = CommitData(
            tree=tree_digest,
            message=message,
            author_name=author_name,
            author_email=author_email,
            parents=parents,
        )
        commit_digest = write_commit(self.objects_dir, c)
        self._update_head(commit_digest)
        return commit_digest

    # ------------------------------------------------------------------
    # status
    # ------------------------------------------------------------------

    def status(self) -> dict:
        """
        Return a dict with three lists of relative paths:
            staged   – tracked files changed vs HEAD
            unstaged – tracked files changed vs index (but not staged)
            untracked – files in working tree not in index
        """
        index = self._read_index()
        head_tree = self._head_tree_flat()

        # staged: diff between HEAD tree and current index
        staged: list[str] = []
        for path in sorted(set(index) | set(head_tree)):
            if index.get(path) != head_tree.get(path):
                staged.append(path)

        # unstaged: working-tree files that differ from index
        unstaged: list[str] = []
        for path, blob in sorted(index.items()):
            full = self.work_dir / path
            if not full.exists():
                unstaged.append(path)
            else:
                _, stored = read_object(self.objects_dir, blob)
                if full.read_bytes() != stored:
                    unstaged.append(path)

        # untracked
        working = self._list_working_files()
        untracked = sorted(working - set(index))

        return {"staged": staged, "unstaged": unstaged, "untracked": untracked}

    # ------------------------------------------------------------------
    # log
    # ------------------------------------------------------------------

    def log(self) -> list[dict]:
        head = self._resolve_head()
        if head is None:
            return []
        entries = []
        for digest, c in iter_commits(self.objects_dir, head):
            entries.append(
                {
                    "digest": digest,
                    "short": digest[:12],
                    "message": c.message,
                    "author": f"{c.author_name} <{c.author_email}>",
                    "timestamp": c.timestamp,
                    "parents": c.parents,
                }
            )
        return entries

    # ------------------------------------------------------------------
    # diff
    # ------------------------------------------------------------------

    def diff(self, staged: bool = False) -> dict[str, str]:
        """
        staged=False → diff working tree vs index (unstaged changes)
        staged=True  → diff index vs HEAD (staged changes)
        """
        index = self._read_index()
        if staged:
            head_tree = self._head_tree_flat()
            return diff_index_vs_commit(self.objects_dir, index, head_tree)
        return diff_working_vs_index(self.objects_dir, index, self.work_dir)

    # ------------------------------------------------------------------
    # checkout
    # ------------------------------------------------------------------

    def checkout(self, target: str) -> None:
        """
        Checkout a commit digest, branch name, or short digest prefix.

        1. Resolve *target* to a commit digest.
        2. Read that commit's tree.
        3. Overwrite tracked working-tree files.
        4. Update HEAD (symbolic or detached).
        """
        commit_digest = self._resolve_target(target)
        c = read_commit(self.objects_dir, commit_digest)
        new_tree = read_tree_flat(self.objects_dir, c.tree)

        # Remove files that were in the old tree but not the new one.
        old_tree = self._head_tree_flat()
        for path in old_tree:
            if path not in new_tree:
                full = self.work_dir / path
                if full.exists():
                    full.unlink()

        # Write the new tree files.
        for path, blob_digest in new_tree.items():
            full = self.work_dir / path
            full.parent.mkdir(parents=True, exist_ok=True)
            _, data = read_object(self.objects_dir, blob_digest)
            full.write_bytes(data)

        # Update index to match the new tree.
        self._write_index(new_tree)

        # Update HEAD.
        is_sym, branch = self._read_head_ref()
        ref_file = self.refs_dir / branch if is_sym else None

        # Is target a branch name?
        branch_ref = self.refs_dir / target
        if branch_ref.exists():
            self.head_path.write_text(f"ref: refs/heads/{target}\n")
        else:
            # Detached HEAD at the resolved digest.
            self.head_path.write_text(commit_digest + "\n")

    def _resolve_target(self, target: str) -> str:
        """Resolve a branch name, full digest, or short prefix to a full digest."""
        # Branch name?
        branch_ref = self.refs_dir / target
        if branch_ref.exists():
            return branch_ref.read_text().strip()

        # Full or partial digest: scan objects dir.
        if len(target) >= 4:
            prefix2 = target[:2]
            prefix_rest = target[2:]
            bucket = self.objects_dir / prefix2
            if bucket.is_dir():
                for entry in bucket.iterdir():
                    full = prefix2 + entry.name
                    if full.startswith(target):
                        # Verify it is a commit.
                        from .objects import read_object as _ro
                        obj_type, _ = _ro(self.objects_dir, full)
                        if obj_type == "commit":
                            return full
        raise RepoError(f"unknown revision: {target!r}")
