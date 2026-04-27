"""Generator v3 — composable scenario graph with creative twists.

Improvements driven by v2 evaluation:
    * v2 lifted complexity & usefulness but creativity stayed mid because
      every prompt followed the same "Build X that supports Y" mold.
    * v3 mixes a *core system* with a *creative twist* and varies prompt
      shape (Given… / Refactor… / Optimize… / Design…) to diversify
      openers and push creativity without bloating tokens.
"""
from __future__ import annotations

import random
from typing import List


CORE_SYSTEMS = [
    "a streaming aggregator that ingests JSON events over TCP",
    "a SQL query planner for a toy column-store",
    "a distributed key-value store with Raft-based replication",
    "a graph-based task DAG executor with caching of intermediate nodes",
    "a content-addressed storage layer over the local filesystem",
    "an HTTP/2 reverse proxy with adaptive backpressure",
    "a deterministic record-and-replay debugger for asyncio programs",
    "a differential-dataflow engine for incremental view maintenance",
]

TWISTS = [
    "but the only allowed dependency is the Python standard library",
    "while keeping p99 latency under 5ms on a single core",
    "designed so each subsystem can be hot-swapped at runtime",
    "with a property-based test suite that fuzzes invariants",
    "where every public function is total and side-effect free",
    "such that the entire core fits in fewer than 400 lines",
    "with first-class support for crash-only restart semantics",
    "exposing both a CLI and a Python API mirroring each other",
]

SHAPES = [
    "Design and implement {core}, {twist}.",
    "Given an existing prototype, refactor {core} so that it now satisfies: {twist}.",
    "Build {core}. Constraint: {twist}.",
    "Optimize {core} for production: {twist}.",
    "Write {core} from scratch — {twist}.",
]


def generate(n: int = 5, seed: int | None = None) -> List[str]:
    rng = random.Random(seed)
    out: List[str] = []
    cores = rng.sample(CORE_SYSTEMS, k=min(n, len(CORE_SYSTEMS)))
    twists = rng.sample(TWISTS, k=min(n, len(TWISTS)))
    shapes = rng.sample(SHAPES, k=min(n, len(SHAPES)))
    while len(shapes) < n:
        shapes.append(rng.choice(SHAPES))
    for i in range(n):
        core = cores[i % len(cores)]
        twist = twists[i % len(twists)]
        shape = shapes[i]
        prompt = shape.format(core=core, twist=twist)
        prompt += " Deliver code, tests, and a 5-line design rationale."
        out.append(prompt)
    return out


if __name__ == "__main__":
    for p in generate(5, seed=1):
        print("-", p)
