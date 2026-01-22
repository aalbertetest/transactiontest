from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional


@dataclass(frozen=True)
class Document:
    url: str
    title: str
    content: str
    fetched_at: Optional[str] = None


@dataclass(frozen=True)
class Posting:
    term: str
    doc_id: int
    term_freq: int
    positions: List[int]


@dataclass(frozen=True)
class SearchResult:
    doc_id: int
    url: str
    title: str
    snippet: str
    score: float
