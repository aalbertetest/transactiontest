from __future__ import annotations

import math


def bm25_idf(doc_freq: int, total_docs: int) -> float:
    if total_docs <= 0:
        return 0.0
    return math.log(1.0 + (total_docs - doc_freq + 0.5) / (doc_freq + 0.5))


def bm25_score(
    term_freq: int,
    doc_freq: int,
    total_docs: int,
    doc_len: int,
    avg_doc_len: float,
    k1: float = 1.5,
    b: float = 0.75,
) -> float:
    if term_freq <= 0 or total_docs == 0:
        return 0.0
    idf = bm25_idf(doc_freq, total_docs)
    norm = k1 * (1.0 - b + b * (doc_len / max(avg_doc_len, 1e-9)))
    tf = (term_freq * (k1 + 1.0)) / (term_freq + norm)
    return idf * tf


def tfidf_score(term_freq: int, doc_freq: int, total_docs: int) -> float:
    if term_freq <= 0 or total_docs == 0:
        return 0.0
    idf = math.log((total_docs + 1.0) / (doc_freq + 1.0)) + 1.0
    tf = 1.0 + math.log(term_freq)
    return tf * idf
