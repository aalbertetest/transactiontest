"""
Query parser supporting:
- Bare terms:           python web
- Phrase search:        "hello world"
- Boolean AND/OR/NOT:   python AND web OR java NOT ruby
- Implicit AND between consecutive terms (default behaviour)
- Parentheses for grouping: (python OR java) AND web

Grammar (simplified):
    query    := expr EOF
    expr     := term (( AND | OR ) term)*
    term     := NOT? atom
    atom     := PHRASE | WORD | LPAREN expr RPAREN

Tokens:
    AND, OR, NOT, PHRASE("..."), WORD, LPAREN, RPAREN
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Union


class TokenType(Enum):
    WORD = auto()
    PHRASE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    LPAREN = auto()
    RPAREN = auto()
    EOF = auto()


@dataclass
class QToken:
    type: TokenType
    value: str = ""


# ---------------------------------------------------------------------------
# Lexer
# ---------------------------------------------------------------------------

_PHRASE_RE = re.compile(r'"([^"]*)"')
_WORD_RE = re.compile(r'[^\s()]+')


def lex(query: str) -> list[QToken]:
    tokens: list[QToken] = []
    i = 0
    text = query.strip()
    n = len(text)
    while i < n:
        # skip whitespace
        if text[i].isspace():
            i += 1
            continue
        # phrase
        if text[i] == '"':
            m = _PHRASE_RE.match(text, i)
            if m:
                tokens.append(QToken(TokenType.PHRASE, m.group(1)))
                i = m.end()
                continue
            else:
                i += 1
                continue
        if text[i] == '(':
            tokens.append(QToken(TokenType.LPAREN, '('))
            i += 1
            continue
        if text[i] == ')':
            tokens.append(QToken(TokenType.RPAREN, ')'))
            i += 1
            continue
        # word / keyword
        m = _WORD_RE.match(text, i)
        if m:
            word = m.group()
            i = m.end()
            upper = word.upper()
            if upper == "AND":
                tokens.append(QToken(TokenType.AND, "AND"))
            elif upper == "OR":
                tokens.append(QToken(TokenType.OR, "OR"))
            elif upper == "NOT":
                tokens.append(QToken(TokenType.NOT, "NOT"))
            else:
                tokens.append(QToken(TokenType.WORD, word))
            continue
        i += 1
    tokens.append(QToken(TokenType.EOF))
    return tokens


# ---------------------------------------------------------------------------
# AST nodes
# ---------------------------------------------------------------------------


@dataclass
class TermNode:
    """A single keyword or phrase."""
    value: str
    is_phrase: bool = False


@dataclass
class NotNode:
    operand: "ASTNode"


@dataclass
class AndNode:
    left: "ASTNode"
    right: "ASTNode"


@dataclass
class OrNode:
    left: "ASTNode"
    right: "ASTNode"


ASTNode = Union[TermNode, NotNode, AndNode, OrNode]


# ---------------------------------------------------------------------------
# Recursive-descent parser
# ---------------------------------------------------------------------------


class QueryParser:
    def __init__(self, tokens: list[QToken]) -> None:
        self._tokens = tokens
        self._pos = 0

    @property
    def _current(self) -> QToken:
        return self._tokens[self._pos]

    def _consume(self, *types: TokenType) -> QToken:
        tok = self._current
        if types and tok.type not in types:
            raise SyntaxError(
                f"Expected {types}, got {tok.type!r} ({tok.value!r})"
            )
        self._pos += 1
        return tok

    def parse(self) -> Optional[ASTNode]:
        if self._current.type == TokenType.EOF:
            return None
        node = self._parse_expr()
        self._consume(TokenType.EOF)
        return node

    def _parse_expr(self) -> ASTNode:
        """expr := term (( AND | OR ) term)*  with implicit AND."""
        left = self._parse_not()

        while self._current.type not in (TokenType.EOF, TokenType.RPAREN):
            op = self._current.type
            if op == TokenType.AND:
                self._consume(TokenType.AND)
                right = self._parse_not()
                left = AndNode(left, right)
            elif op == TokenType.OR:
                self._consume(TokenType.OR)
                right = self._parse_not()
                left = OrNode(left, right)
            else:
                # implicit AND
                right = self._parse_not()
                left = AndNode(left, right)

        return left

    def _parse_not(self) -> ASTNode:
        if self._current.type == TokenType.NOT:
            self._consume(TokenType.NOT)
            operand = self._parse_atom()
            return NotNode(operand)
        return self._parse_atom()

    def _parse_atom(self) -> ASTNode:
        tok = self._current
        if tok.type == TokenType.PHRASE:
            self._consume(TokenType.PHRASE)
            return TermNode(tok.value, is_phrase=True)
        if tok.type == TokenType.WORD:
            self._consume(TokenType.WORD)
            return TermNode(tok.value, is_phrase=False)
        if tok.type == TokenType.LPAREN:
            self._consume(TokenType.LPAREN)
            node = self._parse_expr()
            self._consume(TokenType.RPAREN)
            return node
        raise SyntaxError(
            f"Unexpected token {tok.type!r} ({tok.value!r}) at position {self._pos}"
        )


def parse_query(query_string: str) -> Optional[ASTNode]:
    """Parse *query_string* into an AST.  Returns ``None`` for empty input."""
    tokens = lex(query_string)
    parser = QueryParser(tokens)
    return parser.parse()


def extract_terms(node: Optional[ASTNode]) -> list[str]:
    """Return all literal terms (not negated) from the AST."""
    if node is None:
        return []
    if isinstance(node, TermNode):
        return [node.value]
    if isinstance(node, NotNode):
        return []
    if isinstance(node, (AndNode, OrNode)):
        return extract_terms(node.left) + extract_terms(node.right)
    return []


def extract_all_terms(node: Optional[ASTNode]) -> list[str]:
    """Return ALL literal terms including those inside NOT nodes."""
    if node is None:
        return []
    if isinstance(node, TermNode):
        return [node.value]
    if isinstance(node, NotNode):
        return extract_all_terms(node.operand)
    if isinstance(node, (AndNode, OrNode)):
        return extract_all_terms(node.left) + extract_all_terms(node.right)
    return []
