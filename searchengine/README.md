# LocalSearch

A self-contained, local full-text search engine written in pure Python.

## Features

| Feature | Details |
|---|---|
| **Ingestion** | Index a local folder (HTML / Markdown / TXT) or crawl seed URLs |
| **Text extraction** | HTML tag stripping (BeautifulSoup or regex fallback), Markdown rendering |
| **Tokenisation** | Unicode normalisation, stopword removal, suffix-stripping stemmer |
| **Inverted index** | Positional posting lists for phrase search |
| **Query language** | Boolean `AND` / `OR` / `NOT`, phrase search `"..."`, parentheses grouping, implicit AND |
| **Ranking** | BM25 (Robertson–Zaragoza) + phrase-proximity bonus + title boost |
| **Explanations** | Per-result "Why this result?" panel showing TF, DF, IDF, BM25 per term, proximity bonus |
| **Persistence** | Index saved as gzip-compressed JSON; auto-loaded on startup |
| **Web UI** | Flask app with search page, result highlighting, and admin panel |
| **CLI** | `index`, `crawl`, `search`, `serve`, `stats` subcommands |
| **Tests** | 90 pytest tests covering tokenizer, query parser, ranker, index, and engine |

---

## Quick Start

### 1. Install

```bash
cd searchengine
pip install -r requirements.txt
```

### 2. Index a folder

```bash
python3 cli.py index /path/to/your/docs
```

### 3. Start the web UI

```bash
python3 cli.py serve --port 5000
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

---

## CLI Reference

```
python3 cli.py [--index INDEX_PATH] <command> [options]
```

| Command | Description |
|---|---|
| `index <folder>` | Walk folder and index all HTML/MD/TXT files |
| `crawl <url> [url…]` | BFS crawl from seed URLs (`--max-pages N`, `--delay S`) |
| `search "<query>"` | Search from the terminal (`--explain` for BM25 breakdown) |
| `serve` | Start Flask web server (`--host`, `--port`, `--debug`) |
| `stats` | Print index statistics |

### Example CLI session

```bash
# Index Python docs mirror
python3 cli.py index ~/docs/python

# Search with boolean operators
python3 cli.py search '"list comprehension" AND python NOT java' --explain

# Start the web UI
python3 cli.py serve --debug
```

---

## Query Language

| Syntax | Meaning |
|---|---|
| `python` | Documents containing *python* |
| `python web` | Implicit AND — both terms must appear |
| `python AND web` | Explicit AND |
| `python OR java` | Either term |
| `NOT ruby` | Exclude documents containing *ruby* |
| `"web framework"` | Exact phrase (positional match) |
| `(python OR java) AND web` | Grouped expression |

---

## Web UI

| Page | URL |
|---|---|
| Search | `http://localhost:5000/` |
| Admin (index/crawl) | `http://localhost:5000/admin` |
| JSON API | `http://localhost:5000/api/search?q=python&k=10` |
| Stats JSON | `http://localhost:5000/api/stats` |

---

## Architecture

```
searchengine/
├── searchengine/
│   ├── tokenizer.py      # Text extraction, normalisation, tokenisation, stemmer
│   ├── index.py          # InvertedIndex with positional postings + gzip persistence
│   ├── query_parser.py   # Lexer + recursive-descent parser → AST
│   ├── ranker.py         # BM25Ranker: boolean eval, scoring, phrase proximity, explanations
│   ├── crawler.py        # Folder indexer + BFS URL crawler
│   ├── engine.py         # SearchEngine facade
│   └── app.py            # Flask web application
├── templates/            # Jinja2 HTML templates
├── static/css/           # CSS stylesheet
├── tests/                # pytest test suite (90 tests)
├── cli.py                # Command-line interface
└── data/                 # Default index storage location
```

### Ranking details

BM25 score per term:

```
IDF(t) = log((N - df(t) + 0.5) / (df(t) + 0.5) + 1)
BM25(t, D) = IDF(t) × (tf(t,D) × (k1+1)) / (tf(t,D) + k1 × (1 - b + b × |D|/avgdl))
```

With defaults `k1 = 1.5`, `b = 0.75`.

Additional boosts applied on top of BM25:
- **Title boost** (`×2.0`): term appears in document title
- **Phrase proximity bonus** (`+50% of BM25 score`): adjacent query terms appear within 5 positions

---

## Running Tests

```bash
pip install -r requirements-dev.txt
python3 -m pytest tests/ -v
```

---

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `INDEX_PATH` | `data/index.json.gz` | Path to the persisted index file |
| `SECRET_KEY` | `dev-secret-change-me` | Flask session secret key |
