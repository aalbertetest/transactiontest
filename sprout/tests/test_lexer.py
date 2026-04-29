"""Tests for the Sprout lexer."""

import pytest
from sprout.lexer import Lexer, LexerError
from sprout.tokens import TokenType


def tokenize(src):
    return Lexer(src).tokenize()


def types(src):
    return [t.type for t in tokenize(src) if t.type != TokenType.EOF]


def values(src):
    return [t.value for t in tokenize(src) if t.type != TokenType.EOF]


class TestLiterals:
    def test_integer(self):
        toks = tokenize("42")
        assert toks[0].type == TokenType.INTEGER
        assert toks[0].value == 42

    def test_float(self):
        toks = tokenize("3.14")
        assert toks[0].type == TokenType.FLOAT
        assert abs(toks[0].value - 3.14) < 1e-9

    def test_float_exponent(self):
        toks = tokenize("1e10")
        assert toks[0].type == TokenType.FLOAT
        assert toks[0].value == 1e10

    def test_float_negative_exponent(self):
        toks = tokenize("2.5e-3")
        assert toks[0].type == TokenType.FLOAT
        assert abs(toks[0].value - 2.5e-3) < 1e-15

    def test_string_double_quote(self):
        toks = tokenize('"hello"')
        assert toks[0].type == TokenType.STRING
        assert toks[0].value == "hello"

    def test_string_single_quote(self):
        toks = tokenize("'world'")
        assert toks[0].type == TokenType.STRING
        assert toks[0].value == "world"

    def test_string_escapes(self):
        toks = tokenize(r'"line1\nline2\ttab"')
        assert toks[0].value == "line1\nline2\ttab"

    def test_true_false(self):
        t = tokenize("true false")
        assert t[0].type == TokenType.TRUE
        assert t[0].value is True
        assert t[1].type == TokenType.FALSE
        assert t[1].value is False

    def test_nil(self):
        t = tokenize("nil")
        assert t[0].type == TokenType.NIL
        assert t[0].value is None


class TestKeywords:
    def test_all_keywords(self):
        kw_source = "let fn return if else while for in break continue and or not import"
        expected = [
            TokenType.LET, TokenType.FN, TokenType.RETURN,
            TokenType.IF, TokenType.ELSE, TokenType.WHILE,
            TokenType.FOR, TokenType.IN, TokenType.BREAK,
            TokenType.CONTINUE, TokenType.AND, TokenType.OR,
            TokenType.NOT, TokenType.IMPORT,
        ]
        assert types(kw_source) == expected

    def test_identifier_not_keyword(self):
        t = tokenize("letter")
        assert t[0].type == TokenType.IDENTIFIER
        assert t[0].value == "letter"


class TestOperators:
    def test_arithmetic(self):
        assert types("+ - * / % **") == [
            TokenType.PLUS, TokenType.MINUS, TokenType.STAR,
            TokenType.SLASH, TokenType.PERCENT, TokenType.POWER,
        ]

    def test_comparison(self):
        assert types("== != < <= > >=") == [
            TokenType.EQ, TokenType.NEQ,
            TokenType.LT, TokenType.LTE,
            TokenType.GT, TokenType.GTE,
        ]

    def test_assignment(self):
        assert types("= += -= *= /=") == [
            TokenType.ASSIGN, TokenType.PLUS_ASSIGN, TokenType.MINUS_ASSIGN,
            TokenType.STAR_ASSIGN, TokenType.SLASH_ASSIGN,
        ]

    def test_delimiters(self):
        assert types("( ) { } [ ] , ; : .") == [
            TokenType.LPAREN, TokenType.RPAREN,
            TokenType.LBRACE, TokenType.RBRACE,
            TokenType.LBRACKET, TokenType.RBRACKET,
            TokenType.COMMA, TokenType.SEMICOLON,
            TokenType.COLON, TokenType.DOT,
        ]


class TestComments:
    def test_hash_comment(self):
        toks = tokenize("42 # this is a comment\n99")
        vals = [t.value for t in toks if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        assert vals == [42, 99]

    def test_double_slash_comment(self):
        toks = tokenize("42 // comment\n99")
        vals = [t.value for t in toks if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        assert vals == [42, 99]

    def test_block_comment(self):
        toks = tokenize("1 /* block\ncomment */ 2")
        vals = [t.value for t in toks if t.type not in (TokenType.NEWLINE, TokenType.EOF)]
        assert vals == [1, 2]


class TestLineNumbers:
    def test_line_tracking(self):
        toks = tokenize("a\nb\nc")
        idents = [t for t in toks if t.type == TokenType.IDENTIFIER]
        assert [t.line for t in idents] == [1, 2, 3]


class TestErrors:
    def test_unterminated_string(self):
        with pytest.raises(LexerError):
            tokenize('"unterminated')

    def test_unexpected_character(self):
        with pytest.raises(LexerError):
            tokenize("@")

    def test_empty_source(self):
        toks = tokenize("")
        assert toks[-1].type == TokenType.EOF
