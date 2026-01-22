from mini_search.indexer import Indexer
from mini_search.models import Document
from mini_search.searcher import Searcher
from mini_search.storage import Storage


def test_index_and_search(tmp_path) -> None:
    storage = Storage(str(tmp_path / "search.db"))
    storage.init_schema()
    indexer = Indexer(storage)

    docs = [
        Document(
            url="https://example.com/search",
            title="Search Engines",
            content="Search engines crawl, index, and rank documents.",
        ),
        Document(
            url="https://example.com/bm25",
            title="BM25 Ranking",
            content="BM25 is a ranking function used in information retrieval.",
        ),
    ]
    indexer.index_documents(docs)

    searcher = Searcher(storage)
    results = searcher.search("search", top_k=5)
    assert results
    assert results[0].url == "https://example.com/search"

    phrase_results = searcher.search('"search engines"', top_k=5)
    assert phrase_results
    assert phrase_results[0].url == "https://example.com/search"
