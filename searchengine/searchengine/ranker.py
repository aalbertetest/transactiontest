"""
BM25 ranker with phrase-proximity bonus and 'why this result' explanations.

BM25 formula (Robertson & Zaragoza, 2009):
    score(D, Q) = Σ IDF(qi) * (tf(qi,D) * (k1+1)) / (tf(qi,D) + k1*(1-b+b*|D|/avgdl))

IDF:
    log((N - df + 0.5) / (df + 0.5) + 1)   [smoothed BM25 IDF]

Enhancements beyond vanilla BM25:
- Phrase-proximity bonus: if adjacent query terms appear within a window of
  `phrase_window` positions, a score boost is added.
- Title boost: terms found in the document title get an extra multiplier.
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from typing import Optional

from .index import InvertedIndex, Posting
from .query_parser import ASTNode, AndNode, OrNode, NotNode, TermNode, extract_all_terms
from .tokenizer import tokenize, _stem, tokenize_query_text, STOPWORDS


BM25_K1 = 1.5
BM25_B = 0.75
PHRASE_WINDOW = 5        # positions within which adjacent terms count as "near"
PHRASE_BONUS = 0.5       # fraction of BM25 score added per phrase proximity hit
TITLE_MULTIPLIER = 2.0   # score multiplier when term appears in title


@dataclass
class SearchResult:
    doc_id: int
    url: str
    title: str
    snippet: str
    score: float
    explanation: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "url": self.url,
            "title": self.title,
            "snippet": self.snippet,
            "score": round(self.score, 4),
            "explanation": self.explanation,
        }


class BM25Ranker:
    def __init__(
        self,
        index: InvertedIndex,
        k1: float = BM25_K1,
        b: float = BM25_B,
        phrase_window: int = PHRASE_WINDOW,
        phrase_bonus: float = PHRASE_BONUS,
        title_multiplier: float = TITLE_MULTIPLIER,
    ) -> None:
        self.index = index
        self.k1 = k1
        self.b = b
        self.phrase_window = phrase_window
        self.phrase_bonus = phrase_bonus
        self.title_multiplier = title_multiplier

    # ------------------------------------------------------------------
    # Main search entry point
    # ------------------------------------------------------------------

    def search(
        self,
        ast: Optional[ASTNode],
        top_k: int = 20,
    ) -> list[SearchResult]:
        if ast is None:
            return []

        # 1. Collect candidate doc IDs from the AST (boolean filter)
        candidate_ids = self._evaluate_boolean(ast)

        if not candidate_ids:
            return []

        # 2. Get all non-negated query terms for scoring
        positive_terms = _positive_terms(ast)
        stemmed_terms = [_stem(t.lower()) for t in positive_terms if t.lower() not in STOPWORDS]

        # 3. Score each candidate
        results: list[SearchResult] = []
        avgdl = self.index.avg_doc_length() or 1.0
        N = self.index.num_docs or 1

        for doc_id in candidate_ids:
            doc = self.index.docs.get(doc_id)
            if doc is None:
                continue
            score, explanation = self._score_document(
                doc_id, doc, stemmed_terms, avgdl, N, positive_terms
            )
            results.append(
                SearchResult(
                    doc_id=doc_id,
                    url=doc.url,
                    title=doc.title,
                    snippet=self._highlight_snippet(doc.snippet, positive_terms),
                    score=score,
                    explanation=explanation,
                )
            )

        results.sort(key=lambda r: r.score, reverse=True)
        return results[:top_k]

    # ------------------------------------------------------------------
    # Boolean evaluation
    # ------------------------------------------------------------------

    def _evaluate_boolean(self, node: ASTNode) -> set[int]:
        if isinstance(node, TermNode):
            return self._docs_for_term(node)
        if isinstance(node, NotNode):
            all_ids = set(self.index.docs.keys())
            excluded = self._evaluate_boolean(node.operand)
            return all_ids - excluded
        if isinstance(node, AndNode):
            left = self._evaluate_boolean(node.left)
            right = self._evaluate_boolean(node.right)
            return left & right
        if isinstance(node, OrNode):
            left = self._evaluate_boolean(node.left)
            right = self._evaluate_boolean(node.right)
            return left | right
        return set()

    def _docs_for_term(self, node: TermNode) -> set[int]:
        if node.is_phrase:
            return self._docs_for_phrase(node.value)
        term = _stem(node.value.lower())
        return {p.doc_id for p in self.index.get_postings(term)}

    def _docs_for_phrase(self, phrase: str) -> set[int]:
        """Return doc IDs containing all phrase terms in order (positional)."""
        tokens = tokenize(phrase, remove_stopwords=False).term_list
        tokens = [_stem(t) for t in tokens if t]
        if not tokens:
            return set()
        if len(tokens) == 1:
            return {p.doc_id for p in self.index.get_postings(tokens[0])}

        # Start with postings for first token
        candidates: dict[int, list[int]] = {
            p.doc_id: p.positions for p in self.index.get_postings(tokens[0])
        }

        for offset, token in enumerate(tokens[1:], start=1):
            next_postings = {
                p.doc_id: p.positions for p in self.index.get_postings(token)
            }
            new_candidates: dict[int, list[int]] = {}
            for doc_id, start_positions in candidates.items():
                if doc_id not in next_postings:
                    continue
                next_positions = next_postings[doc_id]
                # Check if any start position has a matching next position at start+offset
                valid_starts = []
                j = 0
                for sp in start_positions:
                    target = sp + offset
                    # binary search-ish
                    while j < len(next_positions) and next_positions[j] < target:
                        j += 1
                    if j < len(next_positions) and next_positions[j] == target:
                        valid_starts.append(sp)
                if valid_starts:
                    new_candidates[doc_id] = valid_starts
            candidates = new_candidates

        return set(candidates.keys())

    # ------------------------------------------------------------------
    # Scoring
    # ------------------------------------------------------------------

    def _score_document(
        self,
        doc_id: int,
        doc,
        stemmed_terms: list[str],
        avgdl: float,
        N: int,
        original_terms: list[str],
    ) -> tuple[float, list[str]]:
        score = 0.0
        explanation: list[str] = []
        dl = doc.length or 1

        for term in stemmed_terms:
            tf = doc.term_freq.get(term, 0)
            if tf == 0:
                continue
            df = self.index.doc_frequency(term)
            if df == 0:
                continue

            idf = math.log((N - df + 0.5) / (df + 0.5) + 1)
            tf_norm = (tf * (self.k1 + 1)) / (
                tf + self.k1 * (1 - self.b + self.b * dl / avgdl)
            )
            term_score = idf * tf_norm

            # Title boost
            title_hit = term in _stem_text(doc.title)
            if title_hit:
                term_score *= self.title_multiplier

            score += term_score
            explanation.append(
                f'Term "{term}": tf={tf}, df={df}/{N}, '
                f'IDF={idf:.3f}, BM25={term_score:.3f}'
                + (" [title boost]" if title_hit else "")
            )

        # Phrase proximity bonus
        phrase_hits = self._count_proximity_hits(doc_id, stemmed_terms)
        if phrase_hits > 0:
            bonus = score * self.phrase_bonus * phrase_hits
            score += bonus
            explanation.append(
                f"Phrase proximity bonus: {phrase_hits} hit(s), +{bonus:.3f}"
            )

        return score, explanation

    def _count_proximity_hits(self, doc_id: int, terms: list[str]) -> int:
        """Count adjacent term pairs that appear within phrase_window positions."""
        if len(terms) < 2:
            return 0
        hits = 0
        pos_lists: list[list[int]] = []
        for term in terms:
            postings = self.index.get_postings(term)
            for p in postings:
                if p.doc_id == doc_id:
                    pos_lists.append(p.positions)
                    break
            else:
                pos_lists.append([])

        for i in range(len(pos_lists) - 1):
            a, b_ = pos_lists[i], pos_lists[i + 1]
            for pa in a:
                for pb in b_:
                    if 0 < pb - pa <= self.phrase_window:
                        hits += 1
                        break
        return hits

    # ------------------------------------------------------------------
    # Snippet highlighting
    # ------------------------------------------------------------------

    def _highlight_snippet(self, snippet: str, terms: list[str]) -> str:
        """Wrap query terms in the snippet with <mark> tags."""
        result = snippet
        for term in set(terms):
            pattern = re.compile(re.escape(term), re.IGNORECASE)
            result = pattern.sub(lambda m: f"<mark>{m.group()}</mark>", result)
        return result


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _positive_terms(node: ASTNode) -> list[str]:
    """Collect all non-negated leaf term values from the AST."""
    if isinstance(node, TermNode):
        if node.is_phrase:
            return node.value.split()
        return [node.value]
    if isinstance(node, NotNode):
        return []
    if isinstance(node, (AndNode, OrNode)):
        return _positive_terms(node.left) + _positive_terms(node.right)
    return []


def _stem_text(text: str) -> set[str]:
    """Return a set of stemmed tokens from a short text (e.g. title)."""
    stream = tokenize(text, remove_stopwords=False)
    return {t for _, t in stream.tokens}
