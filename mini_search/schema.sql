PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS documents (
    doc_id INTEGER PRIMARY KEY,
    url TEXT UNIQUE,
    title TEXT,
    content TEXT,
    length INTEGER NOT NULL,
    fetched_at TEXT
);

CREATE TABLE IF NOT EXISTS terms (
    term_id INTEGER PRIMARY KEY,
    term TEXT UNIQUE,
    doc_freq INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS postings (
    term_id INTEGER NOT NULL,
    doc_id INTEGER NOT NULL,
    term_freq INTEGER NOT NULL,
    positions TEXT NOT NULL,
    PRIMARY KEY (term_id, doc_id),
    FOREIGN KEY (term_id) REFERENCES terms(term_id),
    FOREIGN KEY (doc_id) REFERENCES documents(doc_id)
);

CREATE INDEX IF NOT EXISTS idx_postings_term ON postings(term_id);
CREATE INDEX IF NOT EXISTS idx_postings_doc ON postings(doc_id);

CREATE TABLE IF NOT EXISTS meta (
    key TEXT PRIMARY KEY,
    value TEXT
);
