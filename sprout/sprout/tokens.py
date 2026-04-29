"""Token definitions for the Sprout language."""

from enum import Enum, auto
from dataclasses import dataclass
from typing import Any


class TokenType(Enum):
    # Literals
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()
    TRUE = auto()
    FALSE = auto()
    NIL = auto()

    # Identifiers & keywords
    IDENTIFIER = auto()
    LET = auto()
    FN = auto()
    RETURN = auto()
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    FOR = auto()
    IN = auto()
    BREAK = auto()
    CONTINUE = auto()
    AND = auto()
    OR = auto()
    NOT = auto()
    IMPORT = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    PERCENT = auto()
    POWER = auto()

    EQ = auto()       # ==
    NEQ = auto()      # !=
    LT = auto()       # <
    LTE = auto()      # <=
    GT = auto()       # >
    GTE = auto()      # >=

    ASSIGN = auto()   # =
    PLUS_ASSIGN = auto()   # +=
    MINUS_ASSIGN = auto()  # -=
    STAR_ASSIGN = auto()   # *=
    SLASH_ASSIGN = auto()  # /=

    # Delimiters
    LPAREN = auto()
    RPAREN = auto()
    LBRACE = auto()
    RBRACE = auto()
    LBRACKET = auto()
    RBRACKET = auto()
    COMMA = auto()
    SEMICOLON = auto()
    COLON = auto()
    DOT = auto()

    # Special
    NEWLINE = auto()
    EOF = auto()


KEYWORDS: dict[str, TokenType] = {
    "let":      TokenType.LET,
    "fn":       TokenType.FN,
    "return":   TokenType.RETURN,
    "if":       TokenType.IF,
    "else":     TokenType.ELSE,
    "while":    TokenType.WHILE,
    "for":      TokenType.FOR,
    "in":       TokenType.IN,
    "break":    TokenType.BREAK,
    "continue": TokenType.CONTINUE,
    "and":      TokenType.AND,
    "or":       TokenType.OR,
    "not":      TokenType.NOT,
    "true":     TokenType.TRUE,
    "false":    TokenType.FALSE,
    "nil":      TokenType.NIL,
    "import":   TokenType.IMPORT,
}


@dataclass
class Token:
    type: TokenType
    value: Any
    line: int
    col: int

    def __repr__(self) -> str:
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.col})"
