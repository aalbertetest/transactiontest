from __future__ import annotations

import time
from collections import deque
from html.parser import HTMLParser
from typing import Deque, Iterable, List, Optional, Set, Tuple
from urllib.parse import urldefrag, urljoin, urlparse
from urllib.request import Request, urlopen

from .models import Document


class HtmlTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._texts: List[str] = []
        self._title_parts: List[str] = []
        self._in_title = False
        self.links: List[str] = []

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, Optional[str]]]) -> None:
        if tag.lower() == "a":
            for name, value in attrs:
                if name.lower() == "href" and value:
                    self.links.append(value)
        if tag.lower() == "title":
            self._in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data.strip())
        else:
            text = data.strip()
            if text:
                self._texts.append(text)

    def text(self) -> str:
        return " ".join(self._texts)

    def title(self) -> str:
        return " ".join(self._title_parts).strip()


class Crawler:
    def __init__(
        self,
        user_agent: str = "MiniSearchBot/1.0",
        timeout: int = 10,
        same_domain: bool = True,
        max_depth: int = 2,
    ) -> None:
        self.user_agent = user_agent
        self.timeout = timeout
        self.same_domain = same_domain
        self.max_depth = max_depth

    def crawl(self, seeds: Iterable[str], max_pages: int = 50) -> List[Document]:
        queue: Deque[Tuple[str, int]] = deque()
        seen: Set[str] = set()
        docs: List[Document] = []

        allowed_domains = {
            urlparse(seed).netloc for seed in seeds if urlparse(seed).scheme
        }
        for seed in seeds:
            queue.append((seed, 0))

        while queue and len(docs) < max_pages:
            url, depth = queue.popleft()
            normalized = self._normalize_url(url)
            if not normalized or normalized in seen:
                continue
            if self.same_domain and not self._allowed_domain(normalized, allowed_domains):
                continue

            seen.add(normalized)
            html = self._fetch(normalized)
            if html is None:
                continue

            extractor = HtmlTextExtractor()
            extractor.feed(html)
            text = extractor.text()
            title = extractor.title() or normalized
            docs.append(
                Document(url=normalized, title=title, content=text, fetched_at=self._now_iso())
            )

            if depth < self.max_depth:
                for link in extractor.links:
                    absolute = urljoin(normalized, link)
                    if absolute and absolute not in seen:
                        queue.append((absolute, depth + 1))

        return docs

    def _fetch(self, url: str) -> Optional[str]:
        try:
            req = Request(url, headers={"User-Agent": self.user_agent})
            with urlopen(req, timeout=self.timeout) as resp:
                content_type = resp.headers.get("Content-Type", "")
                if "text/html" not in content_type:
                    return None
                charset = resp.headers.get_content_charset() or "utf-8"
                data = resp.read()
                return data.decode(charset, errors="ignore")
        except Exception:
            return None

    def _normalize_url(self, url: str) -> Optional[str]:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            return None
        cleaned, _ = urldefrag(url)
        return cleaned

    def _allowed_domain(self, url: str, allowed_domains: Set[str]) -> bool:
        if not allowed_domains:
            return True
        return urlparse(url).netloc in allowed_domains

    def _now_iso(self) -> str:
        return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
