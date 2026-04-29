"""
High-level SearchEngine facade that wires together all components.
"""

from __future__ import annotations

import os
from typing import Optional, Callable

from .index import InvertedIndex
from .ranker import BM25Ranker, SearchResult
from .query_parser import parse_query
from .crawler import index_folder, crawl_urls

DEFAULT_INDEX_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "index.json.gz")


class SearchEngine:
    def __init__(self, index_path: Optional[str] = None) -> None:
        self.index_path = index_path or DEFAULT_INDEX_PATH
        self.index = InvertedIndex()
        self._ranker: Optional[BM25Ranker] = None

        if os.path.exists(self.index_path):
            self.index.load(self.index_path)

    @property
    def ranker(self) -> BM25Ranker:
        if self._ranker is None:
            self._ranker = BM25Ranker(self.index)
        return self._ranker

    def search(self, query_string: str, top_k: int = 20) -> list[SearchResult]:
        """Parse and execute a query, returning ranked results."""
        ast = parse_query(query_string)
        return self.ranker.search(ast, top_k=top_k)

    def index_folder(
        self,
        folder: str,
        *,
        on_progress: Optional[Callable[[str], None]] = None,
    ) -> int:
        n = index_folder(folder, self.index, on_progress=on_progress)
        self._ranker = None  # reset so next search gets fresh ranker
        return n

    def crawl(
        self,
        seed_urls: list[str],
        *,
        max_pages: int = 50,
        same_domain: bool = True,
        delay: float = 0.5,
        on_progress: Optional[Callable[[str], None]] = None,
    ) -> int:
        n = crawl_urls(
            seed_urls,
            self.index,
            max_pages=max_pages,
            same_domain=same_domain,
            delay=delay,
            on_progress=on_progress,
        )
        self._ranker = None
        return n

    def save(self, path: Optional[str] = None) -> None:
        self.index.save(path or self.index_path)

    def stats(self) -> dict:
        return self.index.stats()
