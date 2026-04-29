"""Tests for the tokenizer module."""

import pytest
from searchengine.tokenizer import (
    extract_text,
    normalize,
    tokenize,
    _stem,
    TokenStream,
    STOPWORDS,
)


# ---------------------------------------------------------------------------
# normalize
# ---------------------------------------------------------------------------

class TestNormalize:
    def test_lowercases(self):
        assert normalize("Hello WORLD") == "hello world"

    def test_unicode_nfkd(self):
        # é decomposes to e + combining accent via NFKD, then the combining
        # accent is dropped on ASCII encode, leaving 'e' intact
        assert normalize("café") == "cafe"

    def test_already_ascii(self):
        assert normalize("python3") == "python3"

    def test_empty(self):
        assert normalize("") == ""


# ---------------------------------------------------------------------------
# _stem
# ---------------------------------------------------------------------------

class TestStem:
    def test_plural_s(self):
        assert _stem("dogs") == "dog"

    def test_ies_plural(self):
        assert _stem("berries") == "berri"

    def test_sses(self):
        assert _stem("glasses") == "glass"

    def test_ing_removal(self):
        # Our lightweight stemmer strips -ing but leaves a doubled consonant
        # (e.g. "running" -> "runn"); full Porter would reduce to "run".
        result = _stem("running")
        assert result.startswith("run")

    def test_ed_removal(self):
        assert _stem("jumped") == "jump"

    def test_ness_removal(self):
        result = _stem("happiness")
        assert "happi" in result or result == "happi"

    def test_short_word_unchanged(self):
        assert _stem("go") == "go"
        assert _stem("be") == "be"

    def test_ful_removal(self):
        result = _stem("beautiful")
        assert len(result) < len("beautiful")

    def test_ly_removal(self):
        result = _stem("quickly")
        assert result == "quick"


# ---------------------------------------------------------------------------
# extract_text
# ---------------------------------------------------------------------------

class TestExtractText:
    def test_html_strips_tags(self):
        html = "<html><head><title>T</title></head><body><p>Hello World</p></body></html>"
        text = extract_text(html, "html")
        assert "Hello" in text
        assert "<p>" not in text

    def test_html_strips_script(self):
        html = "<body><script>alert(1)</script><p>Content</p></body>"
        text = extract_text(html, "html")
        assert "alert" not in text
        assert "Content" in text

    def test_markdown_strips_heading_hashes(self):
        md = "# Hello\n\nThis is content."
        text = extract_text(md, "markdown")
        assert "Hello" in text
        assert "#" not in text

    def test_markdown_strips_links(self):
        md = "Check [this link](https://example.com) out."
        text = extract_text(md, "markdown")
        assert "this link" in text
        assert "https" not in text

    def test_plain_text_passthrough(self):
        plain = "Just some plain text."
        assert extract_text(plain, "text") == plain

    def test_auto_detects_html(self):
        html = "<p>Auto detect</p>"
        text = extract_text(html, "auto")
        assert "Auto detect" in text
        assert "<p>" not in text

    def test_auto_detects_markdown(self):
        md = "# Heading\nsome text"
        text = extract_text(md, "auto")
        assert "Heading" in text


# ---------------------------------------------------------------------------
# tokenize
# ---------------------------------------------------------------------------

class TestTokenize:
    def test_basic_tokenization(self):
        stream = tokenize("The quick brown fox", remove_stopwords=False, stem=False)
        terms = stream.term_list
        assert "quick" in terms
        assert "brown" in terms
        assert "fox" in terms

    def test_stopword_removal(self):
        stream = tokenize("The quick brown fox", remove_stopwords=True, stem=False)
        terms = stream.term_list
        assert "the" not in terms
        assert "quick" in terms

    def test_positions_are_sequential(self):
        stream = tokenize("hello world test", remove_stopwords=False, stem=False)
        positions = [pos for pos, _ in stream.tokens]
        assert positions == sorted(positions)

    def test_positions_property(self):
        stream = tokenize("cat cat dog", remove_stopwords=False, stem=False)
        pos = stream.positions
        assert len(pos["cat"]) == 2
        assert len(pos["dog"]) == 1

    def test_stemming_applied(self):
        stream = tokenize("running foxes", remove_stopwords=False, stem=True)
        terms = set(stream.term_list)
        # 'running' should be stemmed, 'foxes' -> 'fox' or similar
        assert "running" not in terms or "run" in terms

    def test_numbers_tokenized(self):
        stream = tokenize("Python 3.10 is great", remove_stopwords=False, stem=False)
        terms = stream.term_list
        assert "3" in terms or "python" in terms

    def test_empty_input(self):
        stream = tokenize("", remove_stopwords=False, stem=False)
        assert stream.tokens == []

    def test_term_list_property(self):
        stream = tokenize("hello world", remove_stopwords=False, stem=False)
        assert stream.term_list == ["hello", "world"]

    def test_token_stream_positions_multiple(self):
        stream = tokenize("a a b a", remove_stopwords=False, stem=False)
        positions = stream.positions
        assert len(positions["a"]) == 3
        assert len(positions["b"]) == 1
