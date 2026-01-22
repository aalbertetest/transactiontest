from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Set

from .models import SearchResult
from .query_parser import AndNode, NotNode, OrNode, PhraseNode, QueryNode, QueryParser, TermNode
from .ranking import bm25_score, tfidf_score
from .storage import Storage
from .tokenizer import DEFAULT_STOPWORDS


@dataclass(frozen=True)
class SearchConfig:
    ranking: str = "bm25"
    top_k: int = 10


class Searcher:
    def __init__(self, storage: Storage, stopwords: Iterable[str] = DEFAULT_STOPWORDS) -> None:
        self.storage = storage
        self.parser = QueryParser(stopwords=stopwords)

    def search(self, query: str, top_k: int = 10, ranking: str = "bm25") -> List[SearchResult]:
        parsed = self.parser.parse(query)
        if parsed.ast is None:
            return []
        candidates = self._evaluate_query(parsed.ast)
        if not candidates:
            return []

        total_docs, avg_doc_len = self.storage.get_doc_stats()
        doc_lengths = self.storage.bulk_get_doc_lengths(list(candidates))
        term_freqs: Dict[int, Dict[str, int]] = {doc_id: {} for doc_id in candidates}
        term_doc_freqs: Dict[str, int] = {}

        for term in set(parsed.terms):
            postings = self.storage.get_postings(term)
            term_doc_freqs[term] = self.storage.get_doc_freq(term)
            for posting in postings:
                if posting.doc_id in candidates:
                    term_freqs[posting.doc_id][term] = posting.term_freq

        results: List[SearchResult] = []
        for doc_id in candidates:
            score = 0.0
            doc_len = doc_lengths.get(doc_id, 0)
            for term, tf in term_freqs.get(doc_id, {}).items():
                df = term_doc_freqs.get(term, 0)
                if ranking == "tfidf":
                    score += tfidf_score(tf, df, total_docs)
                else:
                    score += bm25_score(tf, df, total_docs, doc_len, avg_doc_len)

            for phrase in parsed.phrases:
                if self._phrase_match(doc_id, phrase):
                    score += 0.5

            doc_meta = self.storage.get_document_meta(doc_id)
            if doc_meta is None:
                continue
            _, url, title, content, _ = doc_meta
            snippet = self._build_snippet(content, parsed.terms)
            results.append(SearchResult(doc_id=doc_id, url=url, title=title, snippet=snippet, score=score))

        results.sort(key=lambda item: item.score, reverse=True)
        return results[:top_k]

    def _evaluate_query(self, node: QueryNode) -> Set[int]:
        if isinstance(node, TermNode):
            return set(self.storage.get_doc_ids_with_term(node.term))
        if isinstance(node, PhraseNode):
            return self._docs_with_phrase(node.terms)
        if isinstance(node, NotNode):
            all_docs = set(self.storage.get_all_doc_ids())
            return all_docs - self._evaluate_query(node.child)
        if isinstance(node, AndNode):
            return self._evaluate_query(node.left) & self._evaluate_query(node.right)
        if isinstance(node, OrNode):
            return self._evaluate_query(node.left) | self._evaluate_query(node.right)
        return set()

    def _docs_with_phrase(self, terms: Iterable[str]) -> Set[int]:
        term_list = list(terms)
        if not term_list:
            return set()
        doc_sets = [set(self.storage.get_doc_ids_with_term(term)) for term in term_list]
        candidate_docs = set.intersection(*doc_sets) if doc_sets else set()
        matches: Set[int] = set()
        for doc_id in candidate_docs:
            positions_lists = [self.storage.get_positions(term, doc_id) for term in term_list]
            if self._positions_match_phrase(positions_lists):
                matches.add(doc_id)
        return matches

    def _positions_match_phrase(self, positions_lists: List[List[int]]) -> bool:
        if not positions_lists:
            return False
        base_positions = set(positions_lists[0])
        for offset, positions in enumerate(positions_lists[1:], start=1):
            position_set = set(positions)
            base_positions = {pos for pos in base_positions if (pos + offset) in position_set}
            if not base_positions:
                return False
        return True

    def _phrase_match(self, doc_id: int, phrase: Iterable[str]) -> bool:
        terms = list(phrase)
        if not terms:
            return False
        positions_lists = [self.storage.get_positions(term, doc_id) for term in terms]
        return self._positions_match_phrase(positions_lists)

    def _build_snippet(self, content: str, terms: Iterable[str], width: int = 180) -> str:
        lowered = content.lower()
        index = None
        for term in terms:
            pos = lowered.find(term.lower())
            if pos != -1:
                index = pos
                break
        if index is None:
            return content[:width].strip()
        start = max(index - width // 3, 0)
        end = min(start + width, len(content))
        return content[start:end].strip()
