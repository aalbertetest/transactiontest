#!/usr/bin/env python3
"""
LocalSearch CLI

Usage examples:
    # Index a folder
    python cli.py index /path/to/docs

    # Crawl URLs
    python cli.py crawl https://example.com --max-pages 30

    # Search from the command line
    python cli.py search "python web framework"

    # Start the web server
    python cli.py serve --port 5000
"""

import argparse
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from searchengine.engine import SearchEngine, DEFAULT_INDEX_PATH


def cmd_index(args):
    engine = SearchEngine(index_path=args.index)
    print(f"Indexing folder: {args.folder}")

    def progress(msg):
        print(f"  {msg}")

    count = engine.index_folder(args.folder, on_progress=progress)
    engine.save()
    print(f"\nDone. Indexed {count} document(s).")
    print(f"Index saved to: {args.index}")
    stats = engine.stats()
    print(f"Stats: {stats}")


def cmd_crawl(args):
    engine = SearchEngine(index_path=args.index)
    print(f"Crawling {len(args.urls)} seed URL(s), max {args.max_pages} pages...")

    def progress(msg):
        print(f"  {msg}")

    count = engine.crawl(
        args.urls,
        max_pages=args.max_pages,
        same_domain=not args.allow_external,
        delay=args.delay,
        on_progress=progress,
    )
    engine.save()
    print(f"\nDone. Indexed {count} page(s).")
    print(f"Index saved to: {args.index}")


def cmd_search(args):
    engine = SearchEngine(index_path=args.index)
    if engine.index.num_docs == 0:
        print("Index is empty. Run 'index' or 'crawl' first.")
        return
    results = engine.search(args.query, top_k=args.top_k)
    if not results:
        print(f"No results for: {args.query!r}")
        return
    print(f"\n{len(results)} result(s) for: {args.query!r}\n")
    for i, r in enumerate(results, 1):
        print(f"{i}. [{r.score:.4f}] {r.title}")
        print(f"   {r.url}")
        snippet = r.snippet.replace("<mark>", ">>").replace("</mark>", "<<")
        print(f"   {snippet[:120]}...")
        if args.explain:
            for line in r.explanation:
                print(f"     • {line}")
        print()


def cmd_serve(args):
    from searchengine.app import create_app
    app = create_app(index_path=args.index)
    print(f"Starting LocalSearch at http://{args.host}:{args.port}")
    app.run(host=args.host, port=args.port, debug=args.debug)


def cmd_stats(args):
    engine = SearchEngine(index_path=args.index)
    stats = engine.stats()
    print(f"Documents  : {stats['num_docs']}")
    print(f"Terms      : {stats['num_terms']}")
    print(f"Avg length : {stats['avg_doc_length']} tokens")


def main():
    parser = argparse.ArgumentParser(
        prog="searchengine",
        description="LocalSearch — a local full-text search engine",
    )
    parser.add_argument(
        "--index",
        default=DEFAULT_INDEX_PATH,
        help="Path to the index file (default: %(default)s)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # index
    p_index = sub.add_parser("index", help="Index a local folder")
    p_index.add_argument("folder", help="Folder to index")
    p_index.set_defaults(func=cmd_index)

    # crawl
    p_crawl = sub.add_parser("crawl", help="Crawl and index URLs")
    p_crawl.add_argument("urls", nargs="+", help="Seed URLs")
    p_crawl.add_argument("--max-pages", type=int, default=50, dest="max_pages")
    p_crawl.add_argument("--allow-external", action="store_true", dest="allow_external")
    p_crawl.add_argument("--delay", type=float, default=0.5)
    p_crawl.set_defaults(func=cmd_crawl)

    # search
    p_search = sub.add_parser("search", help="Search the index")
    p_search.add_argument("query", help='Query string, e.g. "python web" OR java')
    p_search.add_argument("--top-k", type=int, default=10, dest="top_k")
    p_search.add_argument("--explain", action="store_true", help="Show BM25 explanation")
    p_search.set_defaults(func=cmd_search)

    # serve
    p_serve = sub.add_parser("serve", help="Start the web UI")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=5000)
    p_serve.add_argument("--debug", action="store_true")
    p_serve.set_defaults(func=cmd_serve)

    # stats
    p_stats = sub.add_parser("stats", help="Show index statistics")
    p_stats.set_defaults(func=cmd_stats)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
