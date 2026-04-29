"""Flask web application for the local search engine."""

from __future__ import annotations

import os
import json
import threading
from pathlib import Path
from typing import Optional

from flask import (  # type: ignore
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for,
    flash,
)

from .engine import SearchEngine, DEFAULT_INDEX_PATH

app = Flask(
    __name__,
    template_folder=str(Path(__file__).parent.parent / "templates"),
    static_folder=str(Path(__file__).parent.parent / "static"),
)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")

# Global engine instance (thread-safe for reads; indexing is protected by a lock)
_engine: Optional[SearchEngine] = None
_engine_lock = threading.Lock()


def get_engine() -> SearchEngine:
    global _engine
    if _engine is None:
        index_path = os.environ.get("INDEX_PATH", DEFAULT_INDEX_PATH)
        _engine = SearchEngine(index_path=index_path)
    return _engine


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    engine = get_engine()
    stats = engine.stats()
    query = request.args.get("q", "").strip()
    results = []
    error = None

    if query:
        try:
            results = [r.to_dict() for r in engine.search(query, top_k=20)]
        except SyntaxError as exc:
            error = f"Query parse error: {exc}"
        except Exception as exc:
            error = f"Search error: {exc}"

    return render_template(
        "index.html",
        query=query,
        results=results,
        stats=stats,
        error=error,
    )


@app.route("/api/search")
def api_search():
    query = request.args.get("q", "").strip()
    top_k = min(int(request.args.get("k", 20)), 100)
    if not query:
        return jsonify({"error": "Missing query parameter 'q'"}), 400
    try:
        engine = get_engine()
        results = [r.to_dict() for r in engine.search(query, top_k=top_k)]
        return jsonify({"query": query, "results": results, "count": len(results)})
    except SyntaxError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": str(exc)}), 500


@app.route("/api/stats")
def api_stats():
    return jsonify(get_engine().stats())


@app.route("/admin", methods=["GET", "POST"])
def admin():
    engine = get_engine()
    message = None

    if request.method == "POST":
        action = request.form.get("action")
        if action == "index_folder":
            folder = request.form.get("folder", "").strip()
            if not folder or not os.path.isdir(folder):
                flash(f"Folder not found: {folder!r}", "error")
            else:
                with _engine_lock:
                    count = engine.index_folder(folder, on_progress=None)
                    engine.save()
                flash(f"Indexed {count} document(s) from {folder!r}", "success")

        elif action == "crawl_urls":
            raw_urls = request.form.get("urls", "").strip()
            max_pages = int(request.form.get("max_pages", 20))
            seed_urls = [u.strip() for u in raw_urls.splitlines() if u.strip()]
            if not seed_urls:
                flash("No URLs provided.", "error")
            else:
                with _engine_lock:
                    count = engine.crawl(seed_urls, max_pages=max_pages, delay=0.3)
                    engine.save()
                flash(f"Crawled and indexed {count} page(s)", "success")

        elif action == "save":
            with _engine_lock:
                engine.save()
            flash("Index saved.", "success")

        return redirect(url_for("admin"))

    return render_template("admin.html", stats=engine.stats())


def create_app(index_path: Optional[str] = None) -> Flask:
    """Application factory."""
    if index_path:
        os.environ["INDEX_PATH"] = index_path
    return app


def run_dev(host: str = "127.0.0.1", port: int = 5000, debug: bool = True) -> None:
    app.run(host=host, port=port, debug=debug)
