"""
Text extraction, normalization, and tokenization.

Handles HTML, Markdown, and plain text. Produces a normalized token list
suitable for inverted index construction and query processing.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field
from typing import Iterator

# Optional: heavier HTML parsing
try:
    from bs4 import BeautifulSoup  # type: ignore

    _HAS_BS4 = True
except ImportError:
    _HAS_BS4 = False

# Optional: Markdown rendering
try:
    import markdown  # type: ignore

    _HAS_MARKDOWN = True
except ImportError:
    _HAS_MARKDOWN = False

# Minimal English stopwords; deliberately small to keep phrase search useful.
STOPWORDS: frozenset[str] = frozenset(
    {
        "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "it", "its", "be", "was", "are",
        "were", "been", "has", "have", "had", "do", "does", "did", "will",
        "would", "could", "should", "may", "might", "this", "that", "these",
        "those", "i", "you", "he", "she", "we", "they", "not", "as", "up",
        "out", "about", "into", "so", "if", "no", "my", "your", "his", "her",
        "our", "their", "than", "then", "also",
    }
)

_WORD_RE = re.compile(r"[a-z0-9]+(?:'[a-z]+)*")


@dataclass
class TokenStream:
    """A sequence of (position, token) pairs derived from a document."""

    tokens: list[tuple[int, str]] = field(default_factory=list)

    # Positional index: token -> sorted list of positions
    @property
    def positions(self) -> dict[str, list[int]]:
        pos: dict[str, list[int]] = {}
        for position, token in self.tokens:
            pos.setdefault(token, []).append(position)
        return pos

    @property
    def term_list(self) -> list[str]:
        return [t for _, t in self.tokens]


def extract_text(content: str, content_type: str = "auto") -> str:
    """Return raw text from HTML, Markdown, or plain text content.

    Parameters
    ----------
    content:
        Raw file/response content.
    content_type:
        One of ``"html"``, ``"markdown"``, ``"text"``, or ``"auto"``
        (default: detect by sniffing).
    """
    if content_type == "auto":
        stripped = content.lstrip()
        if stripped.startswith("<"):
            content_type = "html"
        elif re.search(r"^#{1,6}\s", content, re.MULTILINE):
            content_type = "markdown"
        else:
            content_type = "text"

    if content_type == "html":
        return _extract_html(content)
    if content_type == "markdown":
        return _extract_markdown(content)
    return content


def _extract_html(html: str) -> str:
    if _HAS_BS4:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript", "head"]):
            tag.decompose()
        return soup.get_text(separator=" ", strip=True)
    # Fallback: strip tags with regex (good enough for indexing)
    text = re.sub(r"<(script|style)[^>]*>.*?</(script|style)>", " ", html, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"&#\d+;", " ", text)
    return text


def _extract_markdown(md: str) -> str:
    if _HAS_MARKDOWN:
        html = markdown.markdown(md)
        return _extract_html(html)
    # Fallback: strip common MD syntax
    text = re.sub(r"^#{1,6}\s+", "", md, flags=re.MULTILINE)
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"`{1,3}[^`]*`{1,3}", " ", text)
    text = re.sub(r"[*_~]{1,2}", "", text)
    text = re.sub(r"^\s*[-*+]\s+", "", text, flags=re.MULTILINE)
    return text


def normalize(text: str) -> str:
    """Unicode-normalise and lowercase a text string."""
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    return text.lower()


def tokenize(
    text: str,
    *,
    remove_stopwords: bool = True,
    stem: bool = True,
) -> TokenStream:
    """Tokenize *text* into a :class:`TokenStream`.

    Parameters
    ----------
    text:
        Pre-extracted plain text.
    remove_stopwords:
        Drop tokens that are in :data:`STOPWORDS`.
    stem:
        Apply a simple suffix-stripping stemmer.
    """
    normalized = normalize(text)
    stream = TokenStream()
    position = 0
    for match in _WORD_RE.finditer(normalized):
        raw_token = match.group()
        if remove_stopwords and raw_token in STOPWORDS:
            position += 1
            continue
        token = _stem(raw_token) if stem else raw_token
        stream.tokens.append((position, token))
        position += 1
    return stream


# ---------------------------------------------------------------------------
# Minimal suffix-stripping stemmer (Porter-lite, no external dependency)
# ---------------------------------------------------------------------------

_VOWELS = frozenset("aeiou")


def _has_vowel(word: str) -> bool:
    return any(c in _VOWELS for c in word)


def _stem(word: str) -> str:  # noqa: C901
    """Very light stemmer: removes common English suffixes."""
    if len(word) <= 3:
        return word

    # Step 1: plurals / past tense
    if word.endswith("sses"):
        word = word[:-2]
    elif word.endswith("ies"):
        word = word[:-2]
    elif word.endswith("ss"):
        pass  # keep
    elif word.endswith("s") and not word.endswith("ss"):
        word = word[:-1]

    # Step 2: -ing, -ed
    if word.endswith("ing") and _has_vowel(word[:-3]):
        word = word[:-3]
        if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
            word += "e"
    elif word.endswith("ed") and _has_vowel(word[:-2]):
        word = word[:-2]
        if word.endswith("at") or word.endswith("bl") or word.endswith("iz"):
            word += "e"

    # Step 3: -ational, -izer, -ation, -ness, -ment, -ful, -ous, -ive
    for suffix, replacement in [
        ("ational", "ate"),
        ("izer", "ize"),
        ("ation", "ate"),
        ("fulness", "ful"),
        ("ousness", "ous"),
        ("iveness", "ive"),
        ("ness", ""),
        ("ment", ""),
        ("ful", ""),
        ("ous", ""),
        ("ive", ""),
        ("ly", ""),
    ]:
        if word.endswith(suffix) and len(word) - len(suffix) > 2:
            word = word[: -len(suffix)] + replacement
            break

    return word if len(word) > 1 else word


def tokenize_query_text(text: str) -> list[str]:
    """Tokenize a query string; preserves unstemmed tokens for display."""
    normalized = normalize(text)
    tokens = []
    for match in _WORD_RE.finditer(normalized):
        token = match.group()
        tokens.append(token)
    return tokens
