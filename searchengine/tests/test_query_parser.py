"""Tests for the query parser module."""

import pytest
from searchengine.query_parser import (
    parse_query,
    lex,
    TokenType,
    TermNode,
    AndNode,
    OrNode,
    NotNode,
    extract_terms,
    extract_all_terms,
)


# ---------------------------------------------------------------------------
# Lexer
# ---------------------------------------------------------------------------

class TestLexer:
    def test_single_word(self):
        tokens = lex("python")
        types = [t.type for t in tokens]
        assert types == [TokenType.WORD, TokenType.EOF]

    def test_phrase(self):
        tokens = lex('"hello world"')
        assert tokens[0].type == TokenType.PHRASE
        assert tokens[0].value == "hello world"

    def test_operators(self):
        tokens = lex("a AND b OR c NOT d")
        types = [t.type for t in tokens]
        assert TokenType.AND in types
        assert TokenType.OR in types
        assert TokenType.NOT in types

    def test_parentheses(self):
        tokens = lex("(a OR b) AND c")
        types = [t.type for t in tokens]
        assert TokenType.LPAREN in types
        assert TokenType.RPAREN in types

    def test_operators_case_insensitive(self):
        tokens = lex("a and b or c not d")
        types = [t.type for t in tokens]
        assert TokenType.AND in types
        assert TokenType.OR in types
        assert TokenType.NOT in types

    def test_empty_string(self):
        tokens = lex("")
        assert len(tokens) == 1
        assert tokens[0].type == TokenType.EOF


# ---------------------------------------------------------------------------
# Parser — structure
# ---------------------------------------------------------------------------

class TestParser:
    def test_empty_returns_none(self):
        assert parse_query("") is None
        assert parse_query("   ") is None

    def test_single_term(self):
        node = parse_query("python")
        assert isinstance(node, TermNode)
        assert node.value == "python"
        assert node.is_phrase is False

    def test_phrase_node(self):
        node = parse_query('"hello world"')
        assert isinstance(node, TermNode)
        assert node.value == "hello world"
        assert node.is_phrase is True

    def test_implicit_and(self):
        node = parse_query("python web")
        assert isinstance(node, AndNode)

    def test_explicit_and(self):
        node = parse_query("python AND web")
        assert isinstance(node, AndNode)
        assert isinstance(node.left, TermNode)
        assert isinstance(node.right, TermNode)

    def test_or_node(self):
        node = parse_query("python OR java")
        assert isinstance(node, OrNode)

    def test_not_node(self):
        node = parse_query("NOT java")
        assert isinstance(node, NotNode)

    def test_and_not(self):
        node = parse_query("python NOT java")
        assert isinstance(node, AndNode)
        assert isinstance(node.right, NotNode)

    def test_operator_precedence_and_over_or(self):
        # "a AND b OR c" should be (a AND b) OR c  due to left-to-right
        node = parse_query("a AND b OR c")
        assert isinstance(node, OrNode)

    def test_parentheses_grouping(self):
        node = parse_query("(python OR java) AND web")
        assert isinstance(node, AndNode)
        assert isinstance(node.left, OrNode)

    def test_nested_not(self):
        node = parse_query("(python OR java) AND NOT ruby")
        assert isinstance(node, AndNode)
        assert isinstance(node.right, NotNode)

    def test_complex_query(self):
        node = parse_query('"machine learning" AND (python OR r) NOT java')
        assert node is not None

    def test_multiple_terms_implicit_and_chain(self):
        node = parse_query("a b c")
        # a AND b AND c — left-associative
        assert isinstance(node, AndNode)


# ---------------------------------------------------------------------------
# extract_terms helpers
# ---------------------------------------------------------------------------

class TestExtractTerms:
    def test_single_term(self):
        node = parse_query("python")
        assert extract_terms(node) == ["python"]

    def test_and_extracts_both(self):
        node = parse_query("python AND web")
        terms = extract_terms(node)
        assert "python" in terms
        assert "web" in terms

    def test_not_excluded(self):
        node = parse_query("python NOT java")
        terms = extract_terms(node)
        assert "python" in terms
        assert "java" not in terms

    def test_extract_all_includes_not(self):
        node = parse_query("python NOT java")
        terms = extract_all_terms(node)
        assert "python" in terms
        assert "java" in terms

    def test_none_input(self):
        assert extract_terms(None) == []
        assert extract_all_terms(None) == []

    def test_phrase_terms(self):
        node = parse_query('"hello world"')
        terms = extract_terms(node)
        assert terms == ["hello world"]
