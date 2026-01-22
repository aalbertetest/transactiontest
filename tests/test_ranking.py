from mini_search.indexer import Indexer
from mini_search.models import Document
from mini_search.searcher import Searcher
from mini_search.storage import Storage


def test_ranking_modes(tmp_path) -> None:
    storage = Storage(str(tmp_path / "rank.db"))
    storage.init_schema()
    indexer = Indexer(storage)
    indexer.index_documents(
        [
            Document(
                url="https://example.com/short",
                title="Short Doc",
                content="ranking bm25 ranking",
            ),
            Document(
                url="https://example.com/long",
                title="Long Doc",
                content="ranking " * 20,
            ),
        ]
    )
    searcher = Searcher(storage)
    bm25_results = searcher.search("ranking", ranking="bm25")
    tfidf_results = searcher.search("ranking", ranking="tfidf")
    assert bm25_results and tfidf_results
    assert bm25_results[0].score >= 0.0
    assert tfidf_results[0].score >= 0.0
