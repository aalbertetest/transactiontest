from __future__ import annotations

import hashlib
from bisect import bisect
from dataclasses import dataclass
from typing import Dict, Iterable, List

import httpx
from fastapi import FastAPI
from pydantic import BaseModel

from .models import Document


@dataclass(frozen=True)
class Shard:
    shard_id: str
    base_url: str


class ShardRouter:
    def __init__(self, shards: Iterable[Shard], replicas: int = 64) -> None:
        self._ring: List[int] = []
        self._nodes: Dict[int, Shard] = {}
        for shard in shards:
            for replica in range(replicas):
                key = f"{shard.shard_id}:{replica}"
                digest = int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)
                self._ring.append(digest)
                self._nodes[digest] = shard
        self._ring.sort()

    def route(self, key: str) -> Shard:
        if not self._ring:
            raise ValueError("No shards configured")
        digest = int(hashlib.md5(key.encode("utf-8")).hexdigest(), 16)
        idx = bisect(self._ring, digest)
        if idx == len(self._ring):
            idx = 0
        return self._nodes[self._ring[idx]]


@dataclass(frozen=True)
class ShardSearchResult:
    doc_id: str
    url: str
    title: str
    snippet: str
    score: float
    source: str


class Coordinator:
    def __init__(self, shards: Iterable[Shard], timeout: float = 10.0) -> None:
        self.shards = list(shards)
        self.router = ShardRouter(self.shards)
        self.client = httpx.Client(timeout=timeout)

    def close(self) -> None:
        self.client.close()

    def index_documents(self, documents: Iterable[Document]) -> Dict[str, List[int]]:
        buckets: Dict[str, List[Document]] = {}
        for doc in documents:
            shard = self.router.route(doc.url)
            buckets.setdefault(shard.shard_id, []).append(doc)

        results: Dict[str, List[int]] = {}
        for shard in self.shards:
            docs = buckets.get(shard.shard_id, [])
            if not docs:
                results[shard.shard_id] = []
                continue
            payload = {
                "documents": [
                    {
                        "url": doc.url,
                        "title": doc.title,
                        "content": doc.content,
                        "fetched_at": doc.fetched_at,
                    }
                    for doc in docs
                ]
            }
            resp = self.client.post(f"{shard.base_url}/documents", json=payload)
            resp.raise_for_status()
            results[shard.shard_id] = resp.json().get("doc_ids", [])
        return results

    def search(self, query: str, top_k: int = 10, ranking: str = "bm25") -> List[ShardSearchResult]:
        payload = {"query": query, "top_k": top_k, "ranking": ranking}
        results: List[ShardSearchResult] = []
        for shard in self.shards:
            resp = self.client.post(f"{shard.base_url}/search", json=payload)
            resp.raise_for_status()
            data = resp.json().get("results", [])
            for item in data:
                results.append(
                    ShardSearchResult(
                        doc_id=f"{shard.shard_id}:{item['doc_id']}",
                        url=item["url"],
                        title=item["title"],
                        snippet=item["snippet"],
                        score=float(item["score"]),
                        source=shard.shard_id,
                    )
                )
        results.sort(key=lambda item: item.score, reverse=True)
        return results[:top_k]


class CoordinatorIndexRequest(BaseModel):
    documents: List[dict]


class CoordinatorSearchRequest(BaseModel):
    query: str
    top_k: int = 10
    ranking: str = "bm25"


class CoordinatorResultOut(BaseModel):
    doc_id: str
    url: str
    title: str
    snippet: str
    score: float
    source: str


class CoordinatorSearchResponse(BaseModel):
    results: List[CoordinatorResultOut]


def create_coordinator_app(shards: Iterable[Shard]) -> FastAPI:
    coordinator = Coordinator(shards)
    app = FastAPI(title="Mini Search Coordinator", version="1.0")
    app.state.coordinator = coordinator

    @app.post("/documents")
    def index_documents(request: CoordinatorIndexRequest) -> dict:
        documents = [
            Document(
                url=doc["url"],
                title=doc.get("title", ""),
                content=doc["content"],
                fetched_at=doc.get("fetched_at"),
            )
            for doc in request.documents
        ]
        results = coordinator.index_documents(documents)
        return {"shards": results}

    @app.post("/search", response_model=CoordinatorSearchResponse)
    def search(request: CoordinatorSearchRequest) -> CoordinatorSearchResponse:
        results = coordinator.search(request.query, top_k=request.top_k, ranking=request.ranking)
        payload = [CoordinatorResultOut(**result.__dict__) for result in results]
        return CoordinatorSearchResponse(results=payload)

    return app
