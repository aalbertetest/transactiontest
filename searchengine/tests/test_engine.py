"""Integration tests for the SearchEngine facade."""

import os
import pytest
from searchengine.engine import SearchEngine


@pytest.fixture
def engine(tmp_path):
    idx_path = str(tmp_path / "test.json.gz")
    return SearchEngine(index_path=idx_path)


@pytest.fixture
def sample_folder(tmp_path):
    docs = {
        "doc1.html": "<html><head><title>Python Guide</title></head><body><p>Python is great for scripting and web development.</p></body></html>",
        "doc2.md": "# Java Basics\n\nJava is a compiled language running on the JVM.",
        "doc3.txt": "Machine learning and artificial intelligence are transforming technology.",
        "doc4.html": "<html><body><p>Flask and Django are Python web frameworks.</p></body></html>",
    }
    for fname, content in docs.items():
        (tmp_path / fname).write_text(content, encoding="utf-8")
    return str(tmp_path)


class TestSearchEngine:
    def test_starts_empty(self, engine):
        assert engine.stats()["num_docs"] == 0

    def test_index_folder_counts(self, engine, sample_folder):
        count = engine.index_folder(sample_folder)
        assert count == 4

    def test_stats_after_index(self, engine, sample_folder):
        engine.index_folder(sample_folder)
        stats = engine.stats()
        assert stats["num_docs"] == 4
        assert stats["num_terms"] > 0

    def test_search_returns_results(self, engine, sample_folder):
        engine.index_folder(sample_folder)
        results = engine.search("python")
        assert len(results) > 0

    def test_search_no_match(self, engine, sample_folder):
        engine.index_folder(sample_folder)
        results = engine.search("xyznonexistentterm123")
        assert results == []

    def test_search_boolean_and(self, engine, sample_folder):
        engine.index_folder(sample_folder)
        results_python = engine.search("python")
        results_java = engine.search("java")
        results_and = engine.search("python AND java")
        ids_p = {r.doc_id for r in results_python}
        ids_j = {r.doc_id for r in results_java}
        ids_a = {r.doc_id for r in results_and}
        assert ids_a.issubset(ids_p | ids_j)

    def test_search_phrase(self, engine, sample_folder):
        engine.index_folder(sample_folder)
        results = engine.search('"machine learning"')
        assert len(results) > 0

    def test_save_and_reload(self, engine, sample_folder, tmp_path):
        engine.index_folder(sample_folder)
        engine.save()

        engine2 = SearchEngine(index_path=engine.index_path)
        assert engine2.stats()["num_docs"] == engine.stats()["num_docs"]
        results = engine2.search("python")
        assert len(results) > 0

    def test_results_have_explanations(self, engine, sample_folder):
        engine.index_folder(sample_folder)
        results = engine.search("python")
        assert all(isinstance(r.explanation, list) for r in results)
        assert any(r.explanation for r in results)

    def test_results_have_urls(self, engine, sample_folder):
        engine.index_folder(sample_folder)
        results = engine.search("python")
        assert all(r.url.startswith("file://") for r in results)
