"""
Inverted index with positional information and persistence.

The index stores:
- A forward store: doc_id -> DocumentRecord (metadata + term frequencies)
- An inverted index: term -> PostingList (doc_ids with positions)

Persistence is via a single gzip-compressed JSON file.
"""

from __future__ import annotations

import gzip
import json
import math
import os
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class DocumentRecord:
    """Metadata and term-frequency data for one indexed document."""

    doc_id: int
    url: str
    title: str
    snippet: str          # first ~200 chars of plain text
    plain_text: str       # full text for phrase-matching and explanations
    term_freq: dict[str, int] = field(default_factory=dict)
    length: int = 0       # total token count (for BM25)

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> "DocumentRecord":
        return cls(**d)


@dataclass
class Posting:
    """One entry in a posting list: document id + sorted positions."""

    doc_id: int
    positions: list[int] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"doc_id": self.doc_id, "positions": self.positions}

    @classmethod
    def from_dict(cls, d: dict) -> "Posting":
        return cls(doc_id=d["doc_id"], positions=d["positions"])


class InvertedIndex:
    """
    In-memory inverted index.

    Attributes
    ----------
    postings:
        term -> list[Posting], sorted by doc_id.
    docs:
        doc_id -> DocumentRecord.
    """

    def __init__(self) -> None:
        self.postings: dict[str, list[Posting]] = {}
        self.docs: dict[int, DocumentRecord] = {}
        self._next_id: int = 0

    # ------------------------------------------------------------------
    # Indexing
    # ------------------------------------------------------------------

    def add_document(
        self,
        url: str,
        title: str,
        plain_text: str,
        token_stream,   # TokenStream from tokenizer
    ) -> int:
        """Index one document; returns its assigned doc_id."""
        doc_id = self._next_id
        self._next_id += 1

        snippet = plain_text[:300].strip()

        # Build term-freq and position maps from the stream
        tf: dict[str, int] = {}
        positions_map: dict[str, list[int]] = {}
        for pos, token in token_stream.tokens:
            tf[token] = tf.get(token, 0) + 1
            positions_map.setdefault(token, []).append(pos)

        length = len(token_stream.tokens)

        record = DocumentRecord(
            doc_id=doc_id,
            url=url,
            title=title,
            snippet=snippet,
            plain_text=plain_text,
            term_freq=tf,
            length=length,
        )
        self.docs[doc_id] = record

        # Update inverted index
        for term, positions in positions_map.items():
            posting = Posting(doc_id=doc_id, positions=sorted(positions))
            self.postings.setdefault(term, []).append(posting)

        return doc_id

    def remove_document(self, doc_id: int) -> bool:
        """Remove a document from the index (soft delete)."""
        if doc_id not in self.docs:
            return False
        del self.docs[doc_id]
        for term in list(self.postings.keys()):
            self.postings[term] = [p for p in self.postings[term] if p.doc_id != doc_id]
            if not self.postings[term]:
                del self.postings[term]
        return True

    # ------------------------------------------------------------------
    # Retrieval helpers
    # ------------------------------------------------------------------

    def get_postings(self, term: str) -> list[Posting]:
        return self.postings.get(term, [])

    @property
    def num_docs(self) -> int:
        return len(self.docs)

    def avg_doc_length(self) -> float:
        if not self.docs:
            return 0.0
        return sum(r.length for r in self.docs.values()) / len(self.docs)

    def doc_frequency(self, term: str) -> int:
        return len(self.postings.get(term, []))

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def save(self, path: str) -> None:
        """Persist the index to a gzip-compressed JSON file."""
        data = {
            "next_id": self._next_id,
            "docs": {str(k): v.to_dict() for k, v in self.docs.items()},
            "postings": {
                term: [p.to_dict() for p in pl]
                for term, pl in self.postings.items()
            },
        }
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with gzip.open(path, "wt", encoding="utf-8") as fh:
            json.dump(data, fh, separators=(",", ":"))

    def load(self, path: str) -> None:
        """Load a previously saved index file (replaces current state)."""
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            data = json.load(fh)
        self._next_id = data["next_id"]
        self.docs = {
            int(k): DocumentRecord.from_dict(v) for k, v in data["docs"].items()
        }
        self.postings = {
            term: [Posting.from_dict(p) for p in pl]
            for term, pl in data["postings"].items()
        }

    @classmethod
    def from_file(cls, path: str) -> "InvertedIndex":
        idx = cls()
        idx.load(path)
        return idx

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def stats(self) -> dict:
        return {
            "num_docs": self.num_docs,
            "num_terms": len(self.postings),
            "avg_doc_length": round(self.avg_doc_length(), 2),
        }
