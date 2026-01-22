# Mini Search Engine

This project implements a mini search engine from scratch with:

- Crawling (HTML fetch + link discovery)
- Tokenization (stopwords + normalization + positions)
- Indexing (SQLite-based inverted index)
- Ranking (TF-IDF and BM25)
- Query parsing (AND/OR/NOT, parentheses, phrases)
- Storage schema + stats
- HTTP APIs (FastAPI)
- Distributed scaling (shard router + coordinator)
- Examples and tests

## Architecture

```
Crawler -> Tokenizer -> Indexer -> SQLite (docs, terms, postings)
                                           |
                                           v
                                   Query Parser + Searcher
                                           |
                                           v
                                          API
```

## Storage Schema

Schema is defined in `mini_search/schema.sql`:

```sql
CREATE TABLE documents (
  doc_id INTEGER PRIMARY KEY,
  url TEXT UNIQUE,
  title TEXT,
  content TEXT,
  length INTEGER NOT NULL,
  fetched_at TEXT
);

CREATE TABLE terms (
  term_id INTEGER PRIMARY KEY,
  term TEXT UNIQUE,
  doc_freq INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE postings (
  term_id INTEGER NOT NULL,
  doc_id INTEGER NOT NULL,
  term_freq INTEGER NOT NULL,
  positions TEXT NOT NULL,
  PRIMARY KEY (term_id, doc_id)
);
```

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn mini_search.api:create_app --factory --port 8000
```

Index documents:

```bash
curl -X POST http://localhost:8000/documents \
  -H "Content-Type: application/json" \
  -d '{
    "documents": [
      {"url": "https://example.com/a", "title": "Doc A", "content": "Search engines index text"},
      {"url": "https://example.com/b", "title": "Doc B", "content": "BM25 is a ranking function"}
    ]
  }'
```

Search:

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "ranking AND BM25", "top_k": 5, "ranking": "bm25"}'
```

Crawl + index:

```bash
curl -X POST http://localhost:8000/crawl \
  -H "Content-Type: application/json" \
  -d '{"seeds": ["https://example.com"], "max_pages": 10, "max_depth": 1}'
```

Stats:

```bash
curl http://localhost:8000/stats
```

## Query Language

- `AND`, `OR`, `NOT` operators
- Parentheses for grouping
- Quoted phrases for proximity, e.g. `"search engine"`
- Implicit `AND` between adjacent terms

Examples:

- `search AND engine`
- `bm25 OR tfidf`
- `search AND (engine OR crawler)`
- `"search engine" NOT ads`

## Distributed Scaling

Distributed mode uses consistent hashing to route documents to shards and a coordinator
that fans out search requests across shard APIs.

Run two shards:

```bash
uvicorn mini_search.api:create_app --factory --port 8001 --env-file shard1.env
uvicorn mini_search.api:create_app --factory --port 8002 --env-file shard2.env
```

You can pass a shard-specific DB path by exporting `MINI_SEARCH_DB` and using a wrapper:

```bash
MINI_SEARCH_DB=./data/shard1.db uvicorn mini_search.api:create_app --factory --port 8001
MINI_SEARCH_DB=./data/shard2.db uvicorn mini_search.api:create_app --factory --port 8002
```

Then run the coordinator (example in `examples/distributed_coordinator.py`):

```bash
python examples/distributed_coordinator.py
```

Search via coordinator:

```bash
curl -X POST http://localhost:9000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "search engine", "top_k": 10}'
```

## Examples

- `examples/quickstart.py`: index two docs and search
- `examples/distributed_coordinator.py`: coordinator proxy with shards

## Tests

```bash
pip install -r requirements-dev.txt
pytest
```
