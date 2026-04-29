"""Tests for the line-based diff algorithm and blob-diff helpers."""

import pytest
from pathlib import Path

from minigit.objects import write_object
from minigit.diff import unified_diff, diff_blobs, diff_index_vs_commit


class TestUnifiedDiff:
    def test_identical_files_empty_output(self):
        lines = ["line1\n", "line2\n"]
        assert unified_diff(lines, lines) == ""

    def test_single_addition(self):
        a = ["line1\n"]
        b = ["line1\n", "line2\n"]
        out = unified_diff(a, b)
        assert "+line2" in out
        assert "-line2" not in out

    def test_single_deletion(self):
        a = ["line1\n", "line2\n"]
        b = ["line1\n"]
        out = unified_diff(a, b)
        assert "-line2" in out
        assert "+line2" not in out

    def test_modification(self):
        a = ["hello\n"]
        b = ["world\n"]
        out = unified_diff(a, b)
        assert "-hello" in out
        assert "+world" in out

    def test_header_lines_present(self):
        out = unified_diff(["a\n"], ["b\n"], fromfile="old.py", tofile="new.py")
        assert out.startswith("--- old.py")
        assert "+++ new.py" in out

    def test_hunk_header_present(self):
        out = unified_diff(["a\n"], ["b\n"])
        assert "@@" in out

    def test_context_lines_included(self):
        a = [f"line{i}\n" for i in range(10)]
        b = list(a)
        b[5] = "CHANGED\n"
        out = unified_diff(a, b, context=2)
        # Should include 2 context lines around the change
        assert " line3" in out
        assert " line4" in out
        assert "+CHANGED" in out
        assert " line6" in out
        assert " line7" in out

    def test_empty_a(self):
        out = unified_diff([], ["new\n"])
        assert "+new" in out

    def test_empty_b(self):
        out = unified_diff(["old\n"], [])
        assert "-old" in out

    def test_both_empty(self):
        assert unified_diff([], []) == ""

    def test_multiple_hunks(self):
        a = [f"line{i}\n" for i in range(20)]
        b = list(a)
        b[1] = "CHANGE_A\n"
        b[18] = "CHANGE_B\n"
        out = unified_diff(a, b, context=1)
        # Each hunk line looks like "@@ … @@", so 2 hunks → 4 "@@" tokens
        assert out.count("@@") == 4

    def test_no_trailing_newline_handled(self):
        a = ["no newline"]
        b = ["no newline changed"]
        out = unified_diff(a, b)
        assert "-no newline" in out
        assert "+no newline changed" in out


class TestDiffBlobs:
    def test_no_change_empty_string(self, tmp_path):
        data = b"same\n"
        d = write_object(tmp_path, "blob", data)
        assert diff_blobs(tmp_path, d, d, "file.txt") == ""

    def test_new_file(self, tmp_path):
        d = write_object(tmp_path, "blob", b"hello\n")
        out = diff_blobs(tmp_path, None, d, "new.txt")
        assert "+hello" in out
        assert "/dev/null" in out

    def test_deleted_file(self, tmp_path):
        d = write_object(tmp_path, "blob", b"bye\n")
        out = diff_blobs(tmp_path, d, None, "old.txt")
        assert "-bye" in out

    def test_modified_file(self, tmp_path):
        da = write_object(tmp_path, "blob", b"v1\n")
        db = write_object(tmp_path, "blob", b"v2\n")
        out = diff_blobs(tmp_path, da, db, "f.txt")
        assert "-v1" in out
        assert "+v2" in out


class TestDiffIndexVsCommit:
    def test_no_changes(self, tmp_path):
        d = write_object(tmp_path, "blob", b"content\n")
        index = {"a.txt": d}
        tree = {"a.txt": d}
        assert diff_index_vs_commit(tmp_path, index, tree) == {}

    def test_added_file_detected(self, tmp_path):
        d = write_object(tmp_path, "blob", b"new\n")
        result = diff_index_vs_commit(tmp_path, {"new.txt": d}, {})
        assert "new.txt" in result
        assert "+new" in result["new.txt"]

    def test_deleted_file_detected(self, tmp_path):
        d = write_object(tmp_path, "blob", b"old\n")
        result = diff_index_vs_commit(tmp_path, {}, {"old.txt": d})
        assert "old.txt" in result
        assert "-old" in result["old.txt"]

    def test_modified_file_detected(self, tmp_path):
        da = write_object(tmp_path, "blob", b"before\n")
        db = write_object(tmp_path, "blob", b"after\n")
        result = diff_index_vs_commit(tmp_path, {"f.txt": db}, {"f.txt": da})
        assert "f.txt" in result
        out = result["f.txt"]
        assert "-before" in out
        assert "+after" in out
