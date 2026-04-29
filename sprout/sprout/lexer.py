"""Lexer for the Sprout language."""

from typing import Iterator
from .tokens import Token, TokenType, KEYWORDS


class LexerError(Exception):
    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"LexerError at {line}:{col}: {message}")
        self.line = line
        self.col = col


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.col = 1

    def _peek(self, offset: int = 0) -> str:
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else "\0"

    def _advance(self) -> str:
        ch = self.source[self.pos]
        self.pos += 1
        if ch == "\n":
            self.line += 1
            self.col = 1
        else:
            self.col += 1
        return ch

    def _skip_whitespace_and_comments(self) -> None:
        while self.pos < len(self.source):
            ch = self._peek()
            if ch in (" ", "\t", "\r"):
                self._advance()
            elif ch == "#":
                while self.pos < len(self.source) and self._peek() != "\n":
                    self._advance()
            elif ch == "/" and self._peek(1) == "/":
                while self.pos < len(self.source) and self._peek() != "\n":
                    self._advance()
            elif ch == "/" and self._peek(1) == "*":
                self._advance()
                self._advance()
                while self.pos < len(self.source):
                    if self._peek() == "*" and self._peek(1) == "/":
                        self._advance()
                        self._advance()
                        break
                    self._advance()
            else:
                break

    def _read_string(self, quote: str) -> Token:
        line, col = self.line, self.col
        self._advance()  # opening quote
        buf: list[str] = []
        while self.pos < len(self.source):
            ch = self._peek()
            if ch == "\\" :
                self._advance()
                esc = self._advance()
                mapping = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\",
                           "'": "'", '"': '"', "0": "\0"}
                buf.append(mapping.get(esc, esc))
            elif ch == quote:
                self._advance()
                break
            elif ch == "\n":
                raise LexerError("Unterminated string literal", line, col)
            else:
                buf.append(self._advance())
        else:
            raise LexerError("Unterminated string literal", line, col)
        return Token(TokenType.STRING, "".join(buf), line, col)

    def _read_number(self) -> Token:
        line, col = self.line, self.col
        buf: list[str] = []
        is_float = False
        while self._peek().isdigit():
            buf.append(self._advance())
        if self._peek() == "." and self._peek(1).isdigit():
            is_float = True
            buf.append(self._advance())  # dot
            while self._peek().isdigit():
                buf.append(self._advance())
        if self._peek() in ("e", "E"):
            is_float = True
            buf.append(self._advance())
            if self._peek() in ("+", "-"):
                buf.append(self._advance())
            if not self._peek().isdigit():
                raise LexerError("Invalid numeric literal", line, col)
            while self._peek().isdigit():
                buf.append(self._advance())
        text = "".join(buf)
        if is_float:
            return Token(TokenType.FLOAT, float(text), line, col)
        return Token(TokenType.INTEGER, int(text), line, col)

    def _read_identifier(self) -> Token:
        line, col = self.line, self.col
        buf: list[str] = []
        while self._peek().isalnum() or self._peek() == "_":
            buf.append(self._advance())
        text = "".join(buf)
        ttype = KEYWORDS.get(text, TokenType.IDENTIFIER)
        if ttype == TokenType.TRUE:
            return Token(ttype, True, line, col)
        if ttype == TokenType.FALSE:
            return Token(ttype, False, line, col)
        if ttype == TokenType.NIL:
            return Token(ttype, None, line, col)
        return Token(ttype, text, line, col)

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while True:
            self._skip_whitespace_and_comments()
            if self.pos >= len(self.source):
                tokens.append(Token(TokenType.EOF, None, self.line, self.col))
                break

            line, col = self.line, self.col
            ch = self._peek()

            if ch == "\n":
                self._advance()
                tokens.append(Token(TokenType.NEWLINE, "\n", line, col))
                continue

            if ch in ('"', "'"):
                tokens.append(self._read_string(ch))
                continue

            if ch.isdigit():
                tokens.append(self._read_number())
                continue

            if ch.isalpha() or ch == "_":
                tokens.append(self._read_identifier())
                continue

            # Multi-char operators
            two = ch + self._peek(1)
            single_map = {
                "+": TokenType.PLUS, "-": TokenType.MINUS,
                "*": TokenType.STAR, "%": TokenType.PERCENT,
                "(": TokenType.LPAREN, ")": TokenType.RPAREN,
                "{": TokenType.LBRACE, "}": TokenType.RBRACE,
                "[": TokenType.LBRACKET, "]": TokenType.RBRACKET,
                ",": TokenType.COMMA, ";": TokenType.SEMICOLON,
                ":": TokenType.COLON, ".": TokenType.DOT,
            }
            two_map = {
                "==": TokenType.EQ, "!=": TokenType.NEQ,
                "<=": TokenType.LTE, ">=": TokenType.GTE,
                "+=": TokenType.PLUS_ASSIGN, "-=": TokenType.MINUS_ASSIGN,
                "*=": TokenType.STAR_ASSIGN, "/=": TokenType.SLASH_ASSIGN,
                "**": TokenType.POWER,
            }
            if two in two_map:
                self._advance(); self._advance()
                tokens.append(Token(two_map[two], two, line, col))
            elif ch == "<":
                self._advance()
                tokens.append(Token(TokenType.LT, "<", line, col))
            elif ch == ">":
                self._advance()
                tokens.append(Token(TokenType.GT, ">", line, col))
            elif ch == "=":
                self._advance()
                tokens.append(Token(TokenType.ASSIGN, "=", line, col))
            elif ch == "/":
                self._advance()
                tokens.append(Token(TokenType.SLASH, "/", line, col))
            elif ch in single_map:
                self._advance()
                tokens.append(Token(single_map[ch], ch, line, col))
            else:
                raise LexerError(f"Unexpected character {ch!r}", line, col)

        return tokens
