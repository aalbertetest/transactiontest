from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

from .models import Document, Posting


class Storage:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None

    def connect(self) -> sqlite3.Connection:
        if self._conn is None:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._conn.row_factory = sqlite3.Row
            self._conn.execute("PRAGMA journal_mode=WAL;")
            self._conn.execute("PRAGMA foreign_keys = ON;")
        return self._conn

    def init_schema(self) -> None:
        conn = self.connect()
        schema_path = Path(__file__).with_name("schema.sql")
        schema_sql = schema_path.read_text(encoding="utf-8")
        conn.executescript(schema_sql)
        conn.commit()

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _remove_document(self, cur: sqlite3.Cursor, doc_id: int) -> None:
        term_rows = cur.execute(
            "SELECT DISTINCT term_id FROM postings WHERE doc_id = ?",
            (doc_id,),
        ).fetchall()
        for row in term_rows:
            cur.execute(
                "UPDATE terms SET doc_freq = doc_freq - 1 WHERE term_id = ?",
                (row["term_id"],),
            )
        cur.execute("DELETE FROM postings WHERE doc_id = ?", (doc_id,))
        cur.execute("DELETE FROM documents WHERE doc_id = ?", (doc_id,))
        cur.execute("DELETE FROM terms WHERE doc_freq <= 0")

    def upsert_document(self, doc: Document, term_positions: Dict[str, List[int]]) -> int:
        conn = self.connect()
        with conn:
            cur = conn.cursor()
            existing = cur.execute(
                "SELECT doc_id FROM documents WHERE url = ?",
                (doc.url,),
            ).fetchone()
            if existing is not None:
                self._remove_document(cur, int(existing["doc_id"]))

            doc_len = sum(len(pos) for pos in term_positions.values())
            cur.execute(
                """
                INSERT INTO documents (url, title, content, length, fetched_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (doc.url, doc.title, doc.content, doc_len, doc.fetched_at),
            )
            doc_id = int(cur.lastrowid)

            for term, positions in term_positions.items():
                if not positions:
                    continue
                cur.execute(
                    "INSERT OR IGNORE INTO terms (term, doc_freq) VALUES (?, 0)",
                    (term,),
                )
                term_row = cur.execute(
                    "SELECT term_id FROM terms WHERE term = ?",
                    (term,),
                ).fetchone()
                term_id = int(term_row["term_id"])
                cur.execute(
                    """
                    INSERT INTO postings (term_id, doc_id, term_freq, positions)
                    VALUES (?, ?, ?, ?)
                    """,
                    (term_id, doc_id, len(positions), json.dumps(positions)),
                )
                cur.execute(
                    "UPDATE terms SET doc_freq = doc_freq + 1 WHERE term_id = ?",
                    (term_id,),
                )

        return doc_id

    def get_document(self, doc_id: int) -> Optional[Document]:
        conn = self.connect()
        row = conn.execute(
            "SELECT url, title, content, fetched_at FROM documents WHERE doc_id = ?",
            (doc_id,),
        ).fetchone()
        if row is None:
            return None
        return Document(
            url=row["url"],
            title=row["title"] or "",
            content=row["content"] or "",
            fetched_at=row["fetched_at"],
        )

    def get_document_meta(self, doc_id: int) -> Optional[Tuple[int, str, str, str, int]]:
        conn = self.connect()
        row = conn.execute(
            "SELECT doc_id, url, title, content, length FROM documents WHERE doc_id = ?",
            (doc_id,),
        ).fetchone()
        if row is None:
            return None
        return (int(row["doc_id"]), row["url"], row["title"] or "", row["content"] or "", int(row["length"]))

    def get_documents_by_ids(self, doc_ids: Sequence[int]) -> List[Tuple[int, str, str, str, int]]:
        if not doc_ids:
            return []
        placeholders = ",".join("?" for _ in doc_ids)
        conn = self.connect()
        rows = conn.execute(
            f"""
            SELECT doc_id, url, title, content, length
            FROM documents
            WHERE doc_id IN ({placeholders})
            """,
            tuple(doc_ids),
        ).fetchall()
        return [
            (int(row["doc_id"]), row["url"], row["title"] or "", row["content"] or "", int(row["length"]))
            for row in rows
        ]

    def get_postings(self, term: str) -> List[Posting]:
        conn = self.connect()
        rows = conn.execute(
            """
            SELECT t.term, p.doc_id, p.term_freq, p.positions
            FROM postings p
            JOIN terms t ON t.term_id = p.term_id
            WHERE t.term = ?
            """,
            (term,),
        ).fetchall()
        postings: List[Posting] = []
        for row in rows:
            postings.append(
                Posting(
                    term=row["term"],
                    doc_id=int(row["doc_id"]),
                    term_freq=int(row["term_freq"]),
                    positions=json.loads(row["positions"]),
                )
            )
        return postings

    def get_doc_ids_with_term(self, term: str) -> List[int]:
        conn = self.connect()
        rows = conn.execute(
            """
            SELECT p.doc_id
            FROM postings p
            JOIN terms t ON t.term_id = p.term_id
            WHERE t.term = ?
            """,
            (term,),
        ).fetchall()
        return [int(row["doc_id"]) for row in rows]

    def get_positions(self, term: str, doc_id: int) -> List[int]:
        conn = self.connect()
        row = conn.execute(
            """
            SELECT p.positions
            FROM postings p
            JOIN terms t ON t.term_id = p.term_id
            WHERE t.term = ? AND p.doc_id = ?
            """,
            (term, doc_id),
        ).fetchone()
        if row is None:
            return []
        return json.loads(row["positions"])

    def get_doc_stats(self) -> Tuple[int, float]:
        conn = self.connect()
        row = conn.execute(
            "SELECT COUNT(*) AS total_docs, AVG(length) AS avg_len FROM documents"
        ).fetchone()
        total_docs = int(row["total_docs"] or 0)
        avg_len = float(row["avg_len"] or 0.0)
        return total_docs, avg_len

    def get_doc_freq(self, term: str) -> int:
        conn = self.connect()
        row = conn.execute(
            "SELECT doc_freq FROM terms WHERE term = ?",
            (term,),
        ).fetchone()
        return int(row["doc_freq"]) if row is not None else 0

    def get_all_doc_ids(self) -> List[int]:
        conn = self.connect()
        rows = conn.execute("SELECT doc_id FROM documents").fetchall()
        return [int(row["doc_id"]) for row in rows]

    def bulk_get_doc_lengths(self, doc_ids: Sequence[int]) -> Dict[int, int]:
        if not doc_ids:
            return {}
        placeholders = ",".join("?" for _ in doc_ids)
        conn = self.connect()
        rows = conn.execute(
            f"SELECT doc_id, length FROM documents WHERE doc_id IN ({placeholders})",
            tuple(doc_ids),
        ).fetchall()
        return {int(row["doc_id"]): int(row["length"]) for row in rows}
