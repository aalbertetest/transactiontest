from __future__ import annotations

from collections import defaultdict
from typing import Iterable, List, Optional

from .models import Document
from .storage import Storage
from .tokenizer import DEFAULT_STOPWORDS, tokenize_with_positions


class Indexer:
    def __init__(self, storage: Storage, stopwords: Iterable[str] = DEFAULT_STOPWORDS) -> None:
        self.storage = storage
        self.stopwords = set(stopwords)

    def index_document(self, document: Document) -> int:
        text = f"{document.title}\n{document.content}".strip()
        term_positions: dict[str, List[int]] = defaultdict(list)
        for term, position in tokenize_with_positions(text, stopwords=self.stopwords):
            term_positions[term].append(position)
        return self.storage.upsert_document(document, term_positions)

    def index_documents(self, documents: Iterable[Document]) -> List[int]:
        doc_ids: List[int] = []
        for doc in documents:
            doc_ids.append(self.index_document(doc))
        return doc_ids
