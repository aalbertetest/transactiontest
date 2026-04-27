"""Heuristic evaluator for coding-prompt quality.

Scores along four axes on a 0-10 scale:
    - complexity         : how non-trivial the asked-for system is
    - creativity         : how novel / non-boilerplate the framing is
    - token_usage        : efficiency (concise but complete -> high score)
    - real_world_useful  : maps to recognizable real engineering work

The evaluator is intentionally deterministic and lexicon-driven so that
successive generations of the generator can be compared apples-to-apples.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, asdict
from statistics import mean
from typing import Dict, List


COMPLEXITY_SIGNALS = {
    # multi-component / systems-level work
    "distributed", "concurrent", "concurrency", "parallel", "async",
    "scheduler", "pipeline", "stream", "streaming", "queue",
    "cache", "caching", "shard", "sharded", "replicate", "replication",
    "consensus", "raft", "paxos", "transaction", "transactional",
    "compiler", "interpreter", "parser", "lexer", "ast", "bytecode",
    "optimizer", "profiler", "benchmark",
    "rate-limit", "rate limiter", "backpressure", "retry", "idempotent",
    "graph", "tree", "dag", "topological", "trie",
    "kubernetes", "container", "docker",
    "encryption", "cryptographic", "signing", "tls",
    "fault-tolerant", "fault tolerant", "resilient", "recover",
    "schema", "migration", "indexing", "query planner",
    "websocket", "grpc", "protobuf",
    "observability", "metrics", "tracing", "logging",
}

CREATIVITY_SIGNALS = {
    "simulate", "simulation", "evolve", "evolutionary", "genetic",
    "agent", "agents", "self-", "self ", "meta",
    "game", "puzzle", "art", "visualiz", "fractal", "procedural",
    "music", "poetry", "story", "narrative",
    "constraint", "constraints", "novel", "unusual", "quirky",
    "inspired by", "as if", "in the style of",
    "differentiable", "neural", "embedding", "latent",
    "swarm", "flock", "cellular automaton", "automata",
    "bio-inspired", "physics", "chaos",
}

USEFULNESS_SIGNALS = {
    "api", "rest", "http", "cli", "library", "sdk", "package",
    "service", "microservice", "endpoint", "webhook",
    "auth", "authentication", "authorization", "oauth", "jwt",
    "database", "postgres", "sqlite", "mysql", "redis", "mongo",
    "test", "tests", "unit test", "integration test",
    "deploy", "ci", "cd", "pipeline",
    "config", "configurable", "logging", "monitoring",
    "performance", "memory", "throughput", "latency",
    "user", "users", "customer", "production",
    "file", "csv", "json", "yaml", "parser",
    "search", "index", "ranking",
    "frontend", "backend", "react", "node", "typescript",
    "scaling", "load", "load balancer",
}

# words that indicate a bloated / ceremony-heavy prompt
FLUFF_WORDS = {
    "please", "kindly", "very", "really", "just", "simply", "basically",
    "amazing", "robust", "world-class", "state-of-the-art", "leverage",
}

VAGUE_WORDS = {
    "thing", "stuff", "something", "somehow", "etc", "and so on",
}


@dataclass
class Score:
    complexity: float
    creativity: float
    token_usage: float
    real_world_useful: float

    @property
    def total(self) -> float:
        return round(
            self.complexity
            + self.creativity
            + self.token_usage
            + self.real_world_useful,
            3,
        )

    def as_dict(self) -> Dict[str, float]:
        d = asdict(self)
        d["total"] = self.total
        return d


_WORD_RE = re.compile(r"[A-Za-z][A-Za-z\-]+")


def _approx_tokens(text: str) -> int:
    # cheap, model-agnostic token approximation: ~0.75 words per token
    words = _WORD_RE.findall(text)
    return max(1, math.ceil(len(words) / 0.75))


def _signal_hits(text_lc: str, lexicon: set) -> int:
    hits = 0
    for token in lexicon:
        if token in text_lc:
            hits += 1
    return hits


def _has_clear_deliverable(text_lc: str) -> bool:
    for cue in (
        "write", "build", "implement", "design", "create",
        "given", "return", "produce", "must", "should support",
    ):
        if cue in text_lc:
            return True
    return False


def _has_constraints(text_lc: str) -> bool:
    for cue in (
        "constraint", "must", "should", "without", "no external",
        "only", "at most", "at least", "within", "limit",
    ):
        if cue in text_lc:
            return True
    return False


def evaluate_prompt(prompt: str) -> Score:
    text_lc = prompt.lower()
    tokens = _approx_tokens(prompt)

    # ---- complexity --------------------------------------------------
    cx_hits = _signal_hits(text_lc, COMPLEXITY_SIGNALS)
    sentences = max(1, prompt.count(".") + prompt.count("\n"))
    complexity = min(10.0, 1.5 * cx_hits + 0.4 * sentences)
    if _has_constraints(text_lc):
        complexity += 1.0
    complexity = max(0.0, min(10.0, complexity))

    # ---- creativity --------------------------------------------------
    cr_hits = _signal_hits(text_lc, CREATIVITY_SIGNALS)
    creativity = min(10.0, 2.0 * cr_hits)
    # cliched problems penalize creativity
    for cliche in ("fizzbuzz", "todo app", "hello world", "calculator"):
        if cliche in text_lc:
            creativity = max(0.0, creativity - 3.0)

    # ---- token usage -------------------------------------------------
    # ideal window ~50-160 tokens.  Score falls off outside that.
    if tokens < 20:
        token_usage = max(0.0, tokens / 20.0 * 4.0)
    elif tokens <= 160:
        token_usage = 10.0 - abs(tokens - 90) / 90.0 * 3.0
    else:
        token_usage = max(0.0, 10.0 - (tokens - 160) / 40.0)
    fluff = _signal_hits(text_lc, FLUFF_WORDS) + _signal_hits(text_lc, VAGUE_WORDS)
    token_usage = max(0.0, token_usage - 0.6 * fluff)
    token_usage = min(10.0, token_usage)

    # ---- real-world usefulness --------------------------------------
    us_hits = _signal_hits(text_lc, USEFULNESS_SIGNALS)
    usefulness = min(10.0, 1.2 * us_hits)
    if _has_clear_deliverable(text_lc):
        usefulness += 1.5
    if _has_constraints(text_lc):
        usefulness += 1.0
    if _signal_hits(text_lc, VAGUE_WORDS):
        usefulness -= 1.5
    usefulness = max(0.0, min(10.0, usefulness))

    return Score(
        complexity=round(complexity, 2),
        creativity=round(creativity, 2),
        token_usage=round(token_usage, 2),
        real_world_useful=round(usefulness, 2),
    )


def evaluate_batch(prompts: List[str]) -> List[Dict]:
    out = []
    for i, p in enumerate(prompts, 1):
        s = evaluate_prompt(p)
        out.append({
            "index": i,
            "prompt": p,
            "tokens": _approx_tokens(p),
            "scores": s.as_dict(),
        })
    return out


def aggregate(results: List[Dict]) -> Dict[str, float]:
    keys = ("complexity", "creativity", "token_usage", "real_world_useful", "total")
    return {k: round(mean(r["scores"][k] for r in results), 3) for k in keys}


def diagnose(results: List[Dict]) -> List[str]:
    """Produce human-readable feedback for the next generator generation."""
    agg = aggregate(results)
    notes: List[str] = []
    if agg["complexity"] < 6:
        notes.append(
            "Prompts skew too simple — inject systems-level concerns "
            "(concurrency, persistence, fault tolerance, scaling)."
        )
    if agg["creativity"] < 6:
        notes.append(
            "Prompts feel templated — add unusual framings, simulations, "
            "or cross-domain inspirations."
        )
    if agg["token_usage"] < 7:
        notes.append(
            "Token usage is suboptimal — tighten wording, drop fluff "
            "('please', 'robust'), aim for ~60-140 tokens per prompt."
        )
    if agg["real_world_useful"] < 7:
        notes.append(
            "Prompts feel academic — anchor in concrete deliverables "
            "(API surface, CLI flags, file formats, test expectations)."
        )
    # diversity check
    starts = [r["prompt"].split()[0].lower() for r in results if r["prompt"].split()]
    if len(set(starts)) < max(2, len(starts) // 2):
        notes.append(
            "Prompts start with the same verb too often — vary opening "
            "structure (Given…, Design…, Build…, Refactor…, Optimize…)."
        )
    if not notes:
        notes.append("Quality is solid; push the high-end ceiling further.")
    return notes
