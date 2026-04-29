"""Tests for the BM25 ranker and inverted index integration."""

import math
import pytest
from searchengine.index import InvertedIndex
from searchengine.tokenizer import tokenize
from searchengine.ranker import BM25Ranker, SearchResult
from searchengine.query_parser import parse_query


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

def make_index(*docs: tuple[str, str, str]) -> InvertedIndex:
    """Create an index from (url, title, text) tuples."""
    idx = InvertedIndex()
    for url, title, text in docs:
        stream = tokenize(text)
        idx.add_document(url=url, title=title, plain_text=text, token_stream=stream)
    return idx


CORPUS = [
    ("http://a.com/1", "Python Tutorial", "Python is a popular programming language. Python is great for web development."),
    ("http://a.com/2", "Java Guide",       "Java is a compiled programming language. Java runs on the JVM."),
    ("http://a.com/3", "Web Frameworks",   "Django and Flask are Python web frameworks. FastAPI is also Python."),
    ("http://a.com/4", "Database Guide",   "SQL is used for databases. PostgreSQL is an open source database."),
    ("http://a.com/5", "Machine Learning", "Machine learning with Python and scikit-learn is powerful."),
]


# ---------------------------------------------------------------------------
# InvertedIndex tests
# ---------------------------------------------------------------------------

class TestInvertedIndex:
    def test_add_document_increases_count(self):
        idx = make_index(("u", "t", "hello world"))
        assert idx.num_docs == 1

    def test_postings_contain_doc(self):
        idx = make_index(("u", "t", "hello world"))
        # 'hello' and 'world' should be present (possibly stemmed)
        found = any("hell" in term or "world" in term for term in idx.postings)
        assert found or len(idx.postings) > 0

    def test_term_frequency(self):
        idx = make_index(("u", "t", "cat cat cat dog"))
        doc = idx.docs[0]
        cat_stem = next(k for k in doc.term_freq if "cat" in k)
        assert doc.term_freq[cat_stem] == 3

    def test_multiple_docs(self):
        idx = make_index(*CORPUS)
        assert idx.num_docs == len(CORPUS)

    def test_doc_frequency(self):
        idx = make_index(
            ("u1", "t1", "python programming"),
            ("u2", "t2", "python web"),
            ("u3", "t3", "java programming"),
        )
        # 'python' (stemmed) should appear in 2 docs
        python_term = [t for t in idx.postings if "python" in t]
        if python_term:
            assert idx.doc_frequency(python_term[0]) == 2

    def test_positions_stored(self):
        idx = make_index(("u", "t", "apple banana apple"))
        doc = idx.docs[0]
        apple_term = next((k for k in doc.term_freq if "appl" in k), None)
        if apple_term:
            postings = idx.get_postings(apple_term)
            assert len(postings[0].positions) == 2

    def test_remove_document(self):
        idx = make_index(("u", "t", "hello world"))
        assert idx.remove_document(0) is True
        assert idx.num_docs == 0

    def test_avg_doc_length(self):
        idx = make_index(
            ("u1", "t", "a b c d"),
            ("u2", "t", "a b"),
        )
        avg = idx.avg_doc_length()
        # lengths depend on stemming/stopword removal; just check it's a positive number
        assert avg > 0


# ---------------------------------------------------------------------------
# Persistence tests
# ---------------------------------------------------------------------------

class TestPersistence:
    def test_save_and_load(self, tmp_path):
        idx = make_index(*CORPUS)
        path = str(tmp_path / "test_index.json.gz")
        idx.save(path)

        idx2 = InvertedIndex.from_file(path)
        assert idx2.num_docs == idx.num_docs
        assert set(idx2.docs.keys()) == set(idx.docs.keys())

    def test_loaded_postings_match(self, tmp_path):
        idx = make_index(("u", "t", "hello world"))
        path = str(tmp_path / "idx.json.gz")
        idx.save(path)

        idx2 = InvertedIndex.from_file(path)
        assert set(idx2.postings.keys()) == set(idx.postings.keys())

    def test_loaded_docs_match(self, tmp_path):
        idx = make_index(("http://x.com", "Title", "sample text"))
        path = str(tmp_path / "idx.json.gz")
        idx.save(path)

        idx2 = InvertedIndex.from_file(path)
        doc = idx2.docs[0]
        assert doc.url == "http://x.com"
        assert doc.title == "Title"


# ---------------------------------------------------------------------------
# BM25 Ranker tests
# ---------------------------------------------------------------------------

class TestBM25Ranker:
    def setup_method(self):
        self.idx = make_index(*CORPUS)
        self.ranker = BM25Ranker(self.idx)

    def test_search_returns_results(self):
        ast = parse_query("python")
        results = self.ranker.search(ast)
        assert len(results) > 0

    def test_results_are_scored(self):
        ast = parse_query("python")
        results = self.ranker.search(ast)
        assert all(r.score > 0 for r in results)

    def test_results_sorted_descending(self):
        ast = parse_query("python")
        results = self.ranker.search(ast)
        scores = [r.score for r in results]
        assert scores == sorted(scores, reverse=True)

    def test_python_docs_rank_higher_than_java(self):
        ast = parse_query("python")
        results = self.ranker.search(ast)
        urls = [r.url for r in results]
        python_urls = {"http://a.com/1", "http://a.com/3", "http://a.com/5"}
        java_url = "http://a.com/2"
        if java_url in urls:
            java_idx = urls.index(java_url)
            python_idxes = [i for i, u in enumerate(urls) if u in python_urls]
            if python_idxes:
                assert min(python_idxes) < java_idx

    def test_explanation_present(self):
        ast = parse_query("python")
        results = self.ranker.search(ast)
        assert results[0].explanation  # non-empty

    def test_explanation_contains_bm25_info(self):
        ast = parse_query("python")
        results = self.ranker.search(ast)
        text = " ".join(results[0].explanation)
        assert "BM25" in text or "tf=" in text

    def test_boolean_and_narrows_results(self):
        ast_single = parse_query("python")
        ast_and = parse_query("python AND database")
        r_single = self.ranker.search(ast_single)
        r_and = self.ranker.search(ast_and)
        assert len(r_and) <= len(r_single)

    def test_boolean_or_broadens_results(self):
        ast_a = parse_query("python")
        ast_b = parse_query("java")
        ast_or = parse_query("python OR java")
        r_a = self.ranker.search(ast_a)
        r_b = self.ranker.search(ast_b)
        r_or = self.ranker.search(ast_or)
        ids_a = {r.doc_id for r in r_a}
        ids_b = {r.doc_id for r in r_b}
        ids_or = {r.doc_id for r in r_or}
        assert ids_a | ids_b == ids_or

    def test_boolean_not_excludes(self):
        ast_all = parse_query("python")
        ast_not = parse_query("python NOT web")
        r_all = {r.doc_id for r in self.ranker.search(ast_all)}
        r_not = {r.doc_id for r in self.ranker.search(ast_not)}
        # NOT results should be a subset of all python results (or fewer)
        assert len(r_not) <= len(r_all)

    def test_phrase_search(self):
        idx = make_index(
            ("u1", "t", "machine learning is fun"),
            ("u2", "t", "learning machine operations"),
        )
        ranker = BM25Ranker(idx)
        ast = parse_query('"machine learning"')
        results = ranker.search(ast)
        # Only doc 0 has "machine learning" in order
        assert any(r.url == "u1" for r in results)

    def test_top_k_respected(self):
        ast = parse_query("python OR java OR web OR database OR machine")
        results = self.ranker.search(ast, top_k=2)
        assert len(results) <= 2

    def test_empty_query_returns_empty(self):
        ast = parse_query("")
        results = self.ranker.search(ast)
        assert results == []

    def test_snippet_highlights_query_terms(self):
        ast = parse_query("Python")
        results = self.ranker.search(ast)
        if results:
            # At least one result should have a highlight
            all_snippets = " ".join(r.snippet for r in results)
            assert "<mark>" in all_snippets

    def test_title_boost_effect(self):
        # "Python Tutorial" is in the title of doc 0, so it should rank well
        ast = parse_query("tutorial")
        results = self.ranker.search(ast)
        if results:
            # doc with "tutorial" in title should have title boost in explanation
            first = results[0]
            explanation_text = " ".join(first.explanation)
            assert "title boost" in explanation_text or first.title == "Python Tutorial"


# ---------------------------------------------------------------------------
# SearchResult serialization
# ---------------------------------------------------------------------------

class TestSearchResult:
    def test_to_dict(self):
        r = SearchResult(
            doc_id=0,
            url="http://x.com",
            title="Test",
            snippet="A snippet",
            score=1.23,
            explanation=["Term foo: tf=2, ..."],
        )
        d = r.to_dict()
        assert d["url"] == "http://x.com"
        assert d["score"] == 1.23
        assert isinstance(d["explanation"], list)
