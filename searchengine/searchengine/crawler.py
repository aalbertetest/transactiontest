"""
Document ingestion:
- Crawl a list of seed URLs (breadth-first, respects robots.txt optionally)
- Index a local folder of HTML/Markdown/text files
"""

from __future__ import annotations

import os
import re
import time
from pathlib import Path
from typing import Callable, Iterator, Optional
from urllib.parse import urljoin, urlparse

try:
    import requests  # type: ignore
    _HAS_REQUESTS = True
except ImportError:
    _HAS_REQUESTS = False

from .tokenizer import extract_text, tokenize
from .index import InvertedIndex


def _detect_content_type(url_or_path: str) -> str:
    lower = url_or_path.lower()
    if lower.endswith(".md") or lower.endswith(".markdown"):
        return "markdown"
    if lower.endswith(".html") or lower.endswith(".htm"):
        return "html"
    return "text"


def _extract_title(text: str, url_or_path: str) -> str:
    """Try to grab a title from HTML <title> or first # heading."""
    title_match = re.search(r"<title[^>]*>([^<]+)</title>", text, re.IGNORECASE)
    if title_match:
        return title_match.group(1).strip()
    heading_match = re.search(r"^#{1,2}\s+(.+)$", text, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()
    # Fall back to last path segment
    return Path(url_or_path).stem or url_or_path


def index_folder(
    folder: str,
    index: InvertedIndex,
    *,
    extensions: tuple[str, ...] = (".html", ".htm", ".md", ".markdown", ".txt"),
    on_progress: Optional[Callable[[str], None]] = None,
) -> int:
    """Walk *folder* and index every matching file.  Returns number indexed."""
    count = 0
    for root, _dirs, files in os.walk(folder):
        for fname in sorted(files):
            if not any(fname.lower().endswith(ext) for ext in extensions):
                continue
            fpath = os.path.join(root, fname)
            try:
                with open(fpath, "r", encoding="utf-8", errors="replace") as fh:
                    raw = fh.read()
                ct = _detect_content_type(fname)
                plain = extract_text(raw, ct)
                title = _extract_title(raw, fpath)
                stream = tokenize(plain)
                url = Path(fpath).as_uri()
                index.add_document(url=url, title=title, plain_text=plain, token_stream=stream)
                count += 1
                if on_progress:
                    on_progress(fpath)
            except Exception as exc:
                if on_progress:
                    on_progress(f"ERROR {fpath}: {exc}")
    return count


def crawl_urls(
    seed_urls: list[str],
    index: InvertedIndex,
    *,
    max_pages: int = 50,
    same_domain: bool = True,
    delay: float = 0.5,
    on_progress: Optional[Callable[[str], None]] = None,
) -> int:
    """BFS crawl from *seed_urls*, indexing each page.  Returns pages indexed."""
    if not _HAS_REQUESTS:
        raise RuntimeError(
            "The 'requests' package is required for URL crawling. "
            "Install it with: pip install requests"
        )

    visited: set[str] = set()
    queue: list[str] = list(seed_urls)
    allowed_domains: set[str] = {urlparse(u).netloc for u in seed_urls} if same_domain else set()
    count = 0

    headers = {
        "User-Agent": "LocalSearchEngine/1.0 (educational crawler)",
        "Accept": "text/html,text/plain,text/markdown",
    }

    while queue and count < max_pages:
        url = queue.pop(0)
        if url in visited:
            continue
        visited.add(url)

        if same_domain and urlparse(url).netloc not in allowed_domains:
            continue

        try:
            resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            resp.raise_for_status()
            content_type_header = resp.headers.get("Content-Type", "")
            if "html" in content_type_header:
                ct = "html"
            elif "markdown" in content_type_header:
                ct = "markdown"
            else:
                ct = "auto"

            raw = resp.text
            plain = extract_text(raw, ct)
            title = _extract_title(raw, url)
            stream = tokenize(plain)
            index.add_document(url=url, title=title, plain_text=plain, token_stream=stream)
            count += 1
            if on_progress:
                on_progress(f"Indexed: {url}")

            # Extract links for further crawling
            if ct == "html":
                for href in _extract_links(raw, url):
                    if href not in visited:
                        queue.append(href)

            time.sleep(delay)

        except Exception as exc:
            if on_progress:
                on_progress(f"SKIP {url}: {exc}")

    return count


def _extract_links(html: str, base_url: str) -> list[str]:
    """Return absolute URLs found in <a href=...> tags."""
    links = []
    for m in re.finditer(r'<a\s[^>]*href=["\']([^"\'#?]+)["\']', html, re.IGNORECASE):
        href = m.group(1).strip()
        if not href:
            continue
        absolute = urljoin(base_url, href)
        p = urlparse(absolute)
        if p.scheme in ("http", "https"):
            links.append(absolute)
    return links
