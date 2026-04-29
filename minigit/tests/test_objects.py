"""Tests for the content-addressed object store."""

import pytest
from pathlib import Path

from minigit.objects import write_object, read_object, object_exists


class TestWriteReadRoundtrip:
    def test_blob_roundtrip(self, tmp_path):
        data = b"hello, world\n"
        digest = write_object(tmp_path, "blob", data)
        assert len(digest) == 64  # SHA-256 hex
        obj_type, out = read_object(tmp_path, digest)
        assert obj_type == "blob"
        assert out == data

    def test_empty_blob(self, tmp_path):
        digest = write_object(tmp_path, "blob", b"")
        obj_type, out = read_object(tmp_path, digest)
        assert obj_type == "blob"
        assert out == b""

    def test_commit_type_stored(self, tmp_path):
        data = b"tree abc\n\nfirst commit"
        digest = write_object(tmp_path, "commit", data)
        obj_type, out = read_object(tmp_path, digest)
        assert obj_type == "commit"
        assert out == data

    def test_tree_type_stored(self, tmp_path):
        data = b"\x00\x01\x02some raw tree bytes"
        digest = write_object(tmp_path, "tree", data)
        obj_type, out = read_object(tmp_path, digest)
        assert obj_type == "tree"
        assert out == data

    def test_idempotent_write(self, tmp_path):
        data = b"same content"
        d1 = write_object(tmp_path, "blob", data)
        d2 = write_object(tmp_path, "blob", data)
        assert d1 == d2

    def test_different_content_different_digest(self, tmp_path):
        d1 = write_object(tmp_path, "blob", b"foo")
        d2 = write_object(tmp_path, "blob", b"bar")
        assert d1 != d2

    def test_same_content_different_type_different_digest(self, tmp_path):
        data = b"payload"
        d1 = write_object(tmp_path, "blob", data)
        d2 = write_object(tmp_path, "commit", data)
        assert d1 != d2


class TestObjectExists:
    def test_exists_after_write(self, tmp_path):
        digest = write_object(tmp_path, "blob", b"data")
        assert object_exists(tmp_path, digest)

    def test_not_exists_before_write(self, tmp_path):
        assert not object_exists(tmp_path, "a" * 64)


class TestReadMissing:
    def test_raises_key_error(self, tmp_path):
        with pytest.raises(KeyError):
            read_object(tmp_path, "b" * 64)

    def test_partial_digest_raises(self, tmp_path):
        write_object(tmp_path, "blob", b"x")
        with pytest.raises(KeyError):
            read_object(tmp_path, "c" * 64)
