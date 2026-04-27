"""Generator v2 — domain-aware templates.

Improvements driven by v1 evaluation:
    * v1 was templated, simplistic, and clichéd (calculator/fizzbuzz/todo).
    * v2 introduces real engineering domains, concrete deliverables, and
      explicit constraints to lift complexity and real-world usefulness.
"""
from __future__ import annotations

import random
from typing import List


DOMAINS = [
    {
        "noun": "rate limiter",
        "context": "for a public HTTP API",
        "constraint": "supports token-bucket and sliding-window strategies, "
                      "is thread-safe, and exposes Prometheus metrics",
    },
    {
        "noun": "job scheduler",
        "context": "that runs cron-like tasks across a worker pool",
        "constraint": "guarantees at-least-once delivery, persists state to "
                      "SQLite, and supports retries with exponential backoff",
    },
    {
        "noun": "log query CLI",
        "context": "for newline-delimited JSON files",
        "constraint": "supports filtering by field, time-range, and regex, "
                      "with streaming output and a --follow flag",
    },
    {
        "noun": "in-memory cache",
        "context": "with optional disk spillover",
        "constraint": "implements LRU + TTL eviction and exposes a "
                      "context-manager API plus async getters",
    },
    {
        "noun": "diff and patch tool",
        "context": "for structured YAML configs",
        "constraint": "is whitespace-insensitive, preserves comments, and "
                      "produces a minimal patch script",
    },
    {
        "noun": "feature-flag service",
        "context": "with gradual rollout support",
        "constraint": "exposes a gRPC API, persists rules in Postgres, and "
                      "evaluates flags in under 1ms p99",
    },
]

OPENERS = ["Build", "Design", "Implement", "Write"]


def generate(n: int = 5, seed: int | None = None) -> List[str]:
    rng = random.Random(seed)
    out: List[str] = []
    chosen = rng.sample(DOMAINS, k=min(n, len(DOMAINS)))
    while len(chosen) < n:
        chosen.append(rng.choice(DOMAINS))
    for d in chosen[:n]:
        opener = rng.choice(OPENERS)
        prompt = (
            f"{opener} a {d['noun']} {d['context']}. "
            f"It must support {d['constraint']}. "
            f"Include unit tests and a short README."
        )
        out.append(prompt)
    return out


if __name__ == "__main__":
    for p in generate(5, seed=1):
        print("-", p)
