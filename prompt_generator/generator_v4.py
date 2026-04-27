"""Generator v4 — final improved generator.

Improvements driven by v3 evaluation:
    * v3 was strong on complexity/creativity but its constant scaffolding
      ("Deliver code, tests, and a 5-line design rationale.") inflated
      token usage without adding signal.
    * v4 adds a self-tuning step: it samples candidate prompts, scores
      them with the same evaluator the loop uses, and only emits the
      top-N — making the generator itself an optimizer.
    * It also expands the creative axis with *cross-domain framings*
      (bio-inspired, simulation, agent-based, constraint-driven) and
      lets each prompt choose the deliverable that fits its scope, so
      tight prompts stay tight.
"""
from __future__ import annotations

import random
from typing import List, Sequence

from .evaluator import evaluate_prompt


CORE_SYSTEMS: Sequence[str] = (
    "a streaming aggregator that ingests JSON events over TCP",
    "a SQL query planner for a toy column-store",
    "a distributed key-value store with Raft-based replication",
    "a DAG executor that caches intermediate node outputs",
    "a content-addressed storage layer over the local filesystem",
    "an HTTP/2 reverse proxy with adaptive backpressure",
    "a record-and-replay debugger for asyncio programs",
    "a differential-dataflow engine for incremental views",
    "a constraint solver for small SAT instances",
    "an embedded vector index with on-disk persistence",
    "a transactional in-process queue with crash recovery",
    "a deterministic property-based fuzzer for HTTP handlers",
)

CREATIVE_FRAMINGS: Sequence[str] = (
    "modeled after how ant colonies route around obstacles",
    "as if the program were a tiny actor system with mailboxes",
    "with a simulation-mode that replays synthetic workloads",
    "treating every operation as an idempotent algebraic event",
    "where the public API mirrors a familiar UNIX tool",
    "so the system is debuggable purely by reading its log",
    "such that the data model is a single append-only Merkle log",
    "designed to survive arbitrary process crashes mid-write",
)

CONSTRAINTS: Sequence[str] = (
    "stdlib-only, no external packages",
    "p99 under 5ms on a single core",
    "fits in under 400 lines of code",
    "every public function is pure and total",
    "supports hot-swap of any subsystem at runtime",
    "ships with property-based tests and invariants",
    "memory bounded — no growth under steady load",
    "crash-only: no graceful shutdown path",
)

SHAPES: Sequence[str] = (
    "Design {core}, {framing}. Constraint: {constraint}.",
    "Build {core} {framing}; it must be {constraint}.",
    "Refactor {core} so it is {framing} and {constraint}.",
    "Given {core}, optimize it: {framing}, {constraint}.",
    "Write {core} from scratch — {framing} — under the rule: {constraint}.",
)

DELIVERABLES: Sequence[str] = (
    "Include tests.",
    "Provide a CLI and unit tests.",
    "Document the public API in a README.",
    "Add a benchmark script.",
    "",  # sometimes none — keeps token usage tight
)


def _candidate(rng: random.Random) -> str:
    core = rng.choice(CORE_SYSTEMS)
    framing = rng.choice(CREATIVE_FRAMINGS)
    constraint = rng.choice(CONSTRAINTS)
    shape = rng.choice(SHAPES)
    deliverable = rng.choice(DELIVERABLES)
    prompt = shape.format(core=core, framing=framing, constraint=constraint)
    if deliverable:
        prompt += " " + deliverable
    return prompt


def generate(n: int = 5, seed: int | None = None,
             oversample: int = 6) -> List[str]:
    """Generate ``n`` prompts via candidate-and-select self-tuning.

    The generator produces ``n * oversample`` candidates, scores them
    with the evaluator, then returns the top ``n`` while keeping the
    starting verbs diverse so the batch doesn't collapse onto one shape.
    """
    rng = random.Random(seed)
    candidates = {_candidate(rng) for _ in range(max(n, n * oversample))}

    scored = sorted(
        candidates,
        key=lambda p: evaluate_prompt(p).total,
        reverse=True,
    )

    chosen: List[str] = []
    seen_openers: set[str] = set()
    for p in scored:
        opener = p.split()[0].lower()
        if opener in seen_openers and len(seen_openers) < min(4, n):
            continue
        chosen.append(p)
        seen_openers.add(opener)
        if len(chosen) == n:
            break

    while len(chosen) < n and scored:
        chosen.append(scored.pop(0))

    return chosen


if __name__ == "__main__":
    for p in generate(5, seed=1):
        print("-", p)
