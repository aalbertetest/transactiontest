from mini_search.indexer import Indexer
from mini_search.models import Document
from mini_search.searcher import Searcher
from mini_search.storage import Storage


def main() -> None:
    storage = Storage("data/quickstart.db")
    storage.init_schema()

    indexer = Indexer(storage)
    documents = [
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
    indexer.index_documents(documents)

    searcher = Searcher(storage)
    results = searcher.search("ranking AND BM25", top_k=5, ranking="bm25")
    for result in results:
        print(f"{result.score:.3f} {result.title} -> {result.url}")


if __name__ == "__main__":
    main()
