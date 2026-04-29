"""Tests for commit graph: serialisation, write/read, parent chain."""

import time
import pytest
from pathlib import Path

from minigit.objects import write_object
from minigit.commit import (
    CommitData,
    serialise_commit,
    deserialise_commit,
    write_commit,
    read_commit,
    iter_commits,
)
from minigit.tree import write_tree_from_index


def _make_tree(objects_dir: Path, files: dict[str, bytes] = None) -> str:
    files = files or {"README.md": b"# hello\n"}
    index = {}
    for path, data in files.items():
        digest = write_object(objects_dir, "blob", data)
        index[path] = digest
    return write_tree_from_index(objects_dir, index)


class TestSerialisationRoundtrip:
    def test_basic_commit(self, tmp_path):
        c = CommitData(
            tree="a" * 64,
            message="Initial commit",
            author_name="Alice",
            author_email="alice@example.com",
            timestamp=1_700_000_000,
        )
        raw = serialise_commit(c)
        c2 = deserialise_commit(raw)
        assert c2.tree == c.tree
        assert c2.message == c.message
        assert c2.author_name == c.author_name
        assert c2.author_email == c.author_email
        assert c2.timestamp == c.timestamp
        assert c2.parents == []

    def test_commit_with_parent(self, tmp_path):
        parent_digest = "b" * 64
        c = CommitData(
            tree="c" * 64,
            message="Second commit",
            author_name="Bob",
            author_email="bob@example.com",
            parents=[parent_digest],
            timestamp=1_700_000_100,
        )
        raw = serialise_commit(c)
        c2 = deserialise_commit(raw)
        assert c2.parents == [parent_digest]

    def test_multiline_message(self, tmp_path):
        msg = "Subject line\n\nDetailed body\nspanning lines."
        c = CommitData(
            tree="d" * 64,
            message=msg,
            author_name="Carol",
            author_email="carol@example.com",
        )
        raw = serialise_commit(c)
        c2 = deserialise_commit(raw)
        assert c2.message == msg


class TestWriteReadCommit:
    def test_write_and_read(self, tmp_path):
        tree = _make_tree(tmp_path)
        c = CommitData(
            tree=tree,
            message="first",
            author_name="Dev",
            author_email="dev@test.com",
            timestamp=1_000_000,
        )
        digest = write_commit(tmp_path, c)
        assert len(digest) == 64
        c2 = read_commit(tmp_path, digest)
        assert c2.tree == tree
        assert c2.message == "first"

    def test_type_error_on_wrong_object(self, tmp_path):
        digest = write_object(tmp_path, "blob", b"not a commit")
        with pytest.raises(TypeError, match="expected commit"):
            read_commit(tmp_path, digest)


class TestCommitGraph:
    def _chain(self, objects_dir: Path, n: int) -> list[str]:
        """Build a linear chain of n commits; return digests oldest-first."""
        digests = []
        parent = []
        for i in range(n):
            tree = _make_tree(objects_dir, {f"file{i}.txt": f"version {i}".encode()})
            c = CommitData(
                tree=tree,
                message=f"commit {i}",
                author_name="T",
                author_email="t@t.com",
                parents=parent,
                timestamp=1_000_000 + i,
            )
            d = write_commit(objects_dir, c)
            digests.append(d)
            parent = [d]
        return digests

    def test_single_commit_no_parents(self, tmp_path):
        chain = self._chain(tmp_path, 1)
        c = read_commit(tmp_path, chain[0])
        assert c.parents == []

    def test_linear_chain_parents(self, tmp_path):
        chain = self._chain(tmp_path, 3)
        c2 = read_commit(tmp_path, chain[2])
        assert c2.parents == [chain[1]]
        c1 = read_commit(tmp_path, chain[1])
        assert c1.parents == [chain[0]]

    def test_iter_commits_order(self, tmp_path):
        chain = self._chain(tmp_path, 4)
        walked = [digest for digest, _ in iter_commits(tmp_path, chain[-1])]
        # iter_commits walks newest→oldest
        assert walked == list(reversed(chain))

    def test_iter_commits_messages(self, tmp_path):
        chain = self._chain(tmp_path, 3)
        messages = [c.message for _, c in iter_commits(tmp_path, chain[-1])]
        assert messages == ["commit 2", "commit 1", "commit 0"]
