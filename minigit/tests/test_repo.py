"""Integration tests: full repository workflow through Repo API."""

import pytest
from pathlib import Path

from minigit.repo import Repo, RepoError


@pytest.fixture
def repo(tmp_path) -> Repo:
    r = Repo(tmp_path)
    r.init(author_name="Tester", author_email="test@example.com")
    return r


def _write(repo: Repo, name: str, content: str) -> None:
    (repo.work_dir / name).write_text(content)


class TestInit:
    def test_creates_minigit_dir(self, tmp_path):
        r = Repo(tmp_path)
        r.init()
        assert (tmp_path / ".minigit").is_dir()
        assert (tmp_path / ".minigit" / "objects").is_dir()
        assert (tmp_path / ".minigit" / "HEAD").exists()

    def test_double_init_raises(self, tmp_path):
        r = Repo(tmp_path)
        r.init()
        with pytest.raises(RepoError, match="already initialised"):
            r.init()

    def test_head_points_to_main(self, tmp_path):
        r = Repo(tmp_path)
        r.init()
        head = (tmp_path / ".minigit" / "HEAD").read_text()
        assert "refs/heads/main" in head


class TestAddCommit:
    def test_add_and_commit(self, repo):
        _write(repo, "hello.txt", "hello\n")
        repo.add(["hello.txt"])
        digest = repo.commit("initial commit")
        assert len(digest) == 64

    def test_empty_commit_raises(self, repo):
        with pytest.raises(RepoError, match="nothing to commit"):
            repo.commit("empty")

    def test_no_change_commit_raises(self, repo):
        _write(repo, "f.txt", "data\n")
        repo.add(["f.txt"])
        repo.commit("first")
        with pytest.raises(RepoError, match="nothing to commit"):
            repo.commit("second")

    def test_log_grows_with_commits(self, repo):
        _write(repo, "a.txt", "a\n")
        repo.add(["a.txt"])
        repo.commit("commit 1")
        _write(repo, "b.txt", "b\n")
        repo.add(["b.txt"])
        repo.commit("commit 2")
        entries = repo.log()
        assert len(entries) == 2
        assert entries[0]["message"] == "commit 2"
        assert entries[1]["message"] == "commit 1"

    def test_parent_link(self, repo):
        _write(repo, "a.txt", "a\n")
        repo.add(["a.txt"])
        d1 = repo.commit("first")
        _write(repo, "b.txt", "b\n")
        repo.add(["b.txt"])
        d2 = repo.commit("second")
        entries = repo.log()
        assert entries[0]["parents"] == [d1]


class TestStatus:
    def test_untracked_file(self, repo):
        _write(repo, "new.txt", "content\n")
        s = repo.status()
        assert "new.txt" in s["untracked"]

    def test_staged_file(self, repo):
        _write(repo, "staged.txt", "x\n")
        repo.add(["staged.txt"])
        s = repo.status()
        assert "staged.txt" in s["staged"]

    def test_clean_after_commit(self, repo):
        _write(repo, "f.txt", "f\n")
        repo.add(["f.txt"])
        repo.commit("c")
        s = repo.status()
        assert s["staged"] == []
        assert s["unstaged"] == []
        # f.txt is now tracked, but the working-tree file still exists
        # (status only shows it as untracked if it's not in index)
        assert "f.txt" not in s["untracked"]

    def test_unstaged_modification(self, repo):
        _write(repo, "f.txt", "original\n")
        repo.add(["f.txt"])
        repo.commit("c1")
        _write(repo, "f.txt", "modified\n")
        s = repo.status()
        assert "f.txt" in s["unstaged"]


class TestDiff:
    def test_unstaged_diff(self, repo):
        _write(repo, "f.txt", "line1\n")
        repo.add(["f.txt"])
        repo.commit("c1")
        _write(repo, "f.txt", "line2\n")
        diffs = repo.diff(staged=False)
        assert "f.txt" in diffs
        assert "-line1" in diffs["f.txt"]
        assert "+line2" in diffs["f.txt"]

    def test_staged_diff(self, repo):
        _write(repo, "f.txt", "v1\n")
        repo.add(["f.txt"])
        repo.commit("c1")
        _write(repo, "f.txt", "v2\n")
        repo.add(["f.txt"])
        diffs = repo.diff(staged=True)
        assert "f.txt" in diffs
        assert "-v1" in diffs["f.txt"]
        assert "+v2" in diffs["f.txt"]

    def test_no_diff_on_clean_tree(self, repo):
        _write(repo, "f.txt", "x\n")
        repo.add(["f.txt"])
        repo.commit("c")
        assert repo.diff(staged=False) == {}
        assert repo.diff(staged=True) == {}


class TestCheckout:
    def test_checkout_restores_file(self, repo):
        _write(repo, "f.txt", "version1\n")
        repo.add(["f.txt"])
        d1 = repo.commit("v1")

        _write(repo, "f.txt", "version2\n")
        repo.add(["f.txt"])
        repo.commit("v2")

        repo.checkout(d1)
        assert (repo.work_dir / "f.txt").read_text() == "version1\n"

    def test_checkout_removes_deleted_files(self, repo):
        _write(repo, "a.txt", "a\n")
        _write(repo, "b.txt", "b\n")
        repo.add(["a.txt", "b.txt"])
        d1 = repo.commit("both")

        # Second commit removes b.txt from index
        _write(repo, "a.txt", "a2\n")
        repo.add(["a.txt"])
        index = repo._read_index()
        del index["b.txt"]
        repo._write_index(index)
        repo.commit("only a")

        # Go back to d1: b.txt should re-appear
        repo.checkout(d1)
        assert (repo.work_dir / "b.txt").exists()

    def test_checkout_unknown_raises(self, repo):
        with pytest.raises(RepoError, match="unknown revision"):
            repo.checkout("nonexistent")

    def test_checkout_by_short_digest(self, repo):
        _write(repo, "f.txt", "v1\n")
        repo.add(["f.txt"])
        d1 = repo.commit("first")

        _write(repo, "f.txt", "v2\n")
        repo.add(["f.txt"])
        repo.commit("second")

        # short (12-char) prefix should work
        repo.checkout(d1[:12])
        assert (repo.work_dir / "f.txt").read_text() == "v1\n"
