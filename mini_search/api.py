from __future__ import annotations

import os
from typing import List, Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .crawler import Crawler
from .indexer import Indexer
from .models import Document
from .searcher import Searcher
from .storage import Storage


class DocumentIn(BaseModel):
    url: str
    title: str = ""
    content: str
    fetched_at: Optional[str] = None


class IndexRequest(BaseModel):
    documents: List[DocumentIn]


class IndexResponse(BaseModel):
    indexed: int
    doc_ids: List[int]


class CrawlRequest(BaseModel):
    seeds: List[str] = Field(..., min_length=1)
    max_pages: int = 50
    max_depth: int = 2
    same_domain: bool = True
    index: bool = True


class SearchRequest(BaseModel):
    query: str
    top_k: int = 10
    ranking: str = "bm25"


class SearchResultOut(BaseModel):
    doc_id: int
    url: str
    title: str
    snippet: str
    score: float


class SearchResponse(BaseModel):
    results: List[SearchResultOut]


class StatsResponse(BaseModel):
    total_docs: int
    avg_doc_len: float


def create_app(db_path: str = "data/search.db") -> FastAPI:
    db_path = os.environ.get("MINI_SEARCH_DB", db_path)
    storage = Storage(db_path)
    storage.init_schema()
    indexer = Indexer(storage)
    searcher = Searcher(storage)
    crawler = Crawler()

    app = FastAPI(title="Mini Search Engine", version="1.0")
    app.state.storage = storage
    app.state.indexer = indexer
    app.state.searcher = searcher
    app.state.crawler = crawler

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/documents", response_model=IndexResponse)
    def index_documents(request: IndexRequest) -> IndexResponse:
        documents = [
            Document(
                url=doc.url,
                title=doc.title,
                content=doc.content,
                fetched_at=doc.fetched_at,
            )
            for doc in request.documents
        ]
        doc_ids = indexer.index_documents(documents)
        return IndexResponse(indexed=len(doc_ids), doc_ids=doc_ids)

    @app.post("/crawl", response_model=IndexResponse)
    def crawl_and_index(request: CrawlRequest) -> IndexResponse:
        crawler.max_depth = request.max_depth
        crawler.same_domain = request.same_domain
        docs = crawler.crawl(request.seeds, max_pages=request.max_pages)
        if not request.index:
            return IndexResponse(indexed=0, doc_ids=[])
        doc_ids = indexer.index_documents(docs)
        return IndexResponse(indexed=len(doc_ids), doc_ids=doc_ids)

    @app.post("/search", response_model=SearchResponse)
    def search(request: SearchRequest) -> SearchResponse:
        results = searcher.search(request.query, top_k=request.top_k, ranking=request.ranking)
        payload = [SearchResultOut(**result.__dict__) for result in results]
        return SearchResponse(results=payload)

    @app.get("/documents/{doc_id}", response_model=DocumentIn)
    def get_document(doc_id: int) -> DocumentIn:
        doc = storage.get_document(doc_id)
        if doc is None:
            raise HTTPException(status_code=404, detail="Document not found")
        return DocumentIn(url=doc.url, title=doc.title, content=doc.content, fetched_at=doc.fetched_at)

    @app.get("/stats", response_model=StatsResponse)
    def stats() -> StatsResponse:
        total_docs, avg_doc_len = storage.get_doc_stats()
        return StatsResponse(total_docs=total_docs, avg_doc_len=avg_doc_len)

    return app
