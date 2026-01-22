from __future__ import annotations

import re
from typing import Iterable, List, Tuple

DEFAULT_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "but",
    "by",
    "for",
    "if",
    "in",
    "into",
    "is",
    "it",
    "no",
    "not",
    "of",
    "on",
    "or",
    "such",
    "that",
    "the",
    "their",
    "then",
    "there",
    "these",
    "they",
    "this",
    "to",
    "was",
    "will",
    "with",
}

TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def normalize_token(token: str) -> str:
    return token.lower()


def tokenize(text: str, stopwords: Iterable[str] = DEFAULT_STOPWORDS) -> List[str]:
    stopword_set = set(stopwords)
    tokens: List[str] = []
    for match in TOKEN_RE.finditer(text):
        token = normalize_token(match.group(0))
        if token and token not in stopword_set:
            tokens.append(token)
    return tokens


def tokenize_with_positions(
    text: str, stopwords: Iterable[str] = DEFAULT_STOPWORDS
) -> List[Tuple[str, int]]:
    stopword_set = set(stopwords)
    positions: List[Tuple[str, int]] = []
    position = 0
    for match in TOKEN_RE.finditer(text):
        token = normalize_token(match.group(0))
        if token and token not in stopword_set:
            positions.append((token, position))
        position += 1
    return positions
