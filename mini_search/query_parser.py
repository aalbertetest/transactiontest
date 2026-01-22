from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Tuple

from .tokenizer import DEFAULT_STOPWORDS, tokenize


@dataclass(frozen=True)
class QueryToken:
    kind: str
    value: str


class QueryNode:
    pass


@dataclass(frozen=True)
class TermNode(QueryNode):
    term: str


@dataclass(frozen=True)
class PhraseNode(QueryNode):
    terms: Tuple[str, ...]


@dataclass(frozen=True)
class NotNode(QueryNode):
    child: QueryNode


@dataclass(frozen=True)
class AndNode(QueryNode):
    left: QueryNode
    right: QueryNode


@dataclass(frozen=True)
class OrNode(QueryNode):
    left: QueryNode
    right: QueryNode


@dataclass(frozen=True)
class ParsedQuery:
    ast: Optional[QueryNode]
    terms: List[str]
    phrases: List[Tuple[str, ...]]


class QueryParser:
    def __init__(self, stopwords: Iterable[str] = DEFAULT_STOPWORDS) -> None:
        self.stopwords = set(stopwords)

    def parse(self, query: str) -> ParsedQuery:
        tokens = self._tokenize_query(query)
        tokens = self._insert_implicit_and(tokens)
        rpn = self._to_rpn(tokens)
        ast = self._build_ast(rpn)
        terms, phrases = self._extract_positive_terms(ast, negated=False)
        return ParsedQuery(ast=ast, terms=terms, phrases=phrases)

    def _tokenize_query(self, query: str) -> List[QueryToken]:
        tokens: List[QueryToken] = []
        i = 0
        length = len(query)
        while i < length:
            ch = query[i]
            if ch.isspace():
                i += 1
                continue
            if ch == '"':
                end = query.find('"', i + 1)
                if end == -1:
                    end = length
                phrase = query[i + 1 : end]
                tokens.append(QueryToken("PHRASE", phrase))
                i = end + 1
                continue
            if ch == "(":
                tokens.append(QueryToken("LPAREN", ch))
                i += 1
                continue
            if ch == ")":
                tokens.append(QueryToken("RPAREN", ch))
                i += 1
                continue
            start = i
            while i < length and query[i].isalnum():
                i += 1
            word = query[start:i]
            if not word:
                i += 1
                continue
            upper = word.upper()
            if upper in {"AND", "OR", "NOT"}:
                tokens.append(QueryToken(upper, upper))
            else:
                tokens.append(QueryToken("WORD", word))
        return tokens

    def _insert_implicit_and(self, tokens: List[QueryToken]) -> List[QueryToken]:
        if not tokens:
            return []
        result: List[QueryToken] = []
        prev_is_operand = False
        for token in tokens:
            is_operand = token.kind in {"WORD", "PHRASE", "RPAREN"}
            if prev_is_operand and token.kind in {"WORD", "PHRASE", "LPAREN", "NOT"}:
                result.append(QueryToken("AND", "AND"))
            result.append(token)
            prev_is_operand = is_operand
        return result

    def _to_rpn(self, tokens: List[QueryToken]) -> List[QueryToken]:
        output: List[QueryToken] = []
        stack: List[QueryToken] = []
        precedence = {"NOT": 3, "AND": 2, "OR": 1}
        right_assoc = {"NOT"}

        for token in tokens:
            if token.kind in {"WORD", "PHRASE"}:
                output.append(token)
                continue
            if token.kind in {"AND", "OR", "NOT"}:
                while stack and stack[-1].kind in precedence:
                    top = stack[-1]
                    if (
                        precedence[top.kind] > precedence[token.kind]
                        or (
                            precedence[top.kind] == precedence[token.kind]
                            and token.kind not in right_assoc
                        )
                    ):
                        output.append(stack.pop())
                    else:
                        break
                stack.append(token)
                continue
            if token.kind == "LPAREN":
                stack.append(token)
                continue
            if token.kind == "RPAREN":
                while stack and stack[-1].kind != "LPAREN":
                    output.append(stack.pop())
                if stack and stack[-1].kind == "LPAREN":
                    stack.pop()
        while stack:
            output.append(stack.pop())
        return output

    def _build_ast(self, rpn: List[QueryToken]) -> Optional[QueryNode]:
        stack: List[QueryNode] = []
        for token in rpn:
            if token.kind == "WORD":
                term = self._normalize_term(token.value)
                if term:
                    stack.append(TermNode(term))
                continue
            if token.kind == "PHRASE":
                terms = tuple(self._normalize_terms(token.value))
                if terms:
                    stack.append(PhraseNode(terms))
                continue
            if token.kind == "NOT":
                if not stack:
                    continue
                stack.append(NotNode(stack.pop()))
                continue
            if token.kind in {"AND", "OR"}:
                if len(stack) < 2:
                    continue
                right = stack.pop()
                left = stack.pop()
                if token.kind == "AND":
                    stack.append(AndNode(left, right))
                else:
                    stack.append(OrNode(left, right))
        if not stack:
            return None
        return stack[-1]

    def _normalize_term(self, term: str) -> Optional[str]:
        tokens = tokenize(term, stopwords=self.stopwords)
        return tokens[0] if tokens else None

    def _normalize_terms(self, text: str) -> List[str]:
        return tokenize(text, stopwords=self.stopwords)

    def _extract_positive_terms(
        self, node: Optional[QueryNode], negated: bool
    ) -> Tuple[List[str], List[Tuple[str, ...]]]:
        if node is None:
            return [], []
        if isinstance(node, TermNode):
            return ([node.term] if not negated else []), []
        if isinstance(node, PhraseNode):
            return [], ([node.terms] if not negated else [])
        if isinstance(node, NotNode):
            return self._extract_positive_terms(node.child, not negated)
        if isinstance(node, AndNode) or isinstance(node, OrNode):
            left_terms, left_phrases = self._extract_positive_terms(node.left, negated)
            right_terms, right_phrases = self._extract_positive_terms(node.right, negated)
            return left_terms + right_terms, left_phrases + right_phrases
        return [], []
