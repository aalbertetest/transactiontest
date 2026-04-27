# Self-Improving Coding-Prompt Generator — Evolution Log

Three iterations of the loop are run in order. After each iteration the evaluator's diagnosis is used to motivate the next generator. The fourth file, `generator_v4`, is the final improved generator emitted after iteration 3.

## Iteration 1 — `generator_v1`

**Generated prompts**

1. Write a number guesser that works.
2. Create a number guesser in Python.
3. Create a fizzbuzz .
4. Write a fizzbuzz .
5. Build a fizzbuzz .

**Per-prompt evaluation**

| # | tokens | complexity | creativity | token_usage | useful | total |
|---|--------|------------|------------|-------------|--------|-------|
| 1 | 7 | 0.4 | 0.0 | 1.4 | 1.5 | 3.3 |
| 2 | 7 | 0.4 | 0.0 | 1.4 | 1.5 | 3.3 |
| 3 | 3 | 0.4 | 0.0 | 0.6 | 1.5 | 2.5 |
| 4 | 3 | 0.4 | 0.0 | 0.6 | 1.5 | 2.5 |
| 5 | 3 | 0.4 | 0.0 | 0.6 | 1.5 | 2.5 |

**Averages** — complexity: 0.4, creativity: 0.0, token_usage: 0.92, useful: 1.5, **total: 2.82**

**Diagnosis (feeds the next generator)**

- Prompts skew too simple — inject systems-level concerns (concurrency, persistence, fault tolerance, scaling).
- Prompts feel templated — add unusual framings, simulations, or cross-domain inspirations.
- Token usage is suboptimal — tighten wording, drop fluff ('please', 'robust'), aim for ~60-140 tokens per prompt.
- Prompts feel academic — anchor in concrete deliverables (API surface, CLI flags, file formats, test expectations).

## Iteration 2 — `generator_v2`

**Generated prompts**

1. Design a in-memory cache with optional disk spillover. It must support implements LRU + TTL eviction and exposes a context-manager API plus async getters. Include unit tests and a short README.
2. Implement a diff and patch tool for structured YAML configs. It must support is whitespace-insensitive, preserves comments, and produces a minimal patch script. Include unit tests and a short README.
3. Build a rate limiter for a public HTTP API. It must support supports token-bucket and sliding-window strategies, is thread-safe, and exposes Prometheus metrics. Include unit tests and a short README.
4. Design a feature-flag service with gradual rollout support. It must support exposes a gRPC API, persists rules in Postgres, and evaluates flags in under 1ms p99. Include unit tests and a short README.
5. Build a job scheduler that runs cron-like tasks across a worker pool. It must support guarantees at-least-once delivery, persists state to SQLite, and supports retries with exponential backoff. Include unit tests and a short README.

**Per-prompt evaluation**

| # | tokens | complexity | creativity | token_usage | useful | total |
|---|--------|------------|------------|-------------|--------|-------|
| 1 | 36 | 5.2 | 0.0 | 8.2 | 8.5 | 21.9 |
| 2 | 36 | 2.2 | 0.0 | 8.2 | 8.5 | 18.9 |
| 3 | 36 | 5.2 | 0.0 | 8.2 | 8.5 | 21.9 |
| 4 | 39 | 3.7 | 0.0 | 8.3 | 9.7 | 21.7 |
| 5 | 43 | 6.7 | 0.0 | 7.83 | 7.3 | 21.83 |

**Averages** — complexity: 4.6, creativity: 0.0, token_usage: 8.146, useful: 8.5, **total: 21.246**

**Diagnosis (feeds the next generator)**

- Prompts skew too simple — inject systems-level concerns (concurrency, persistence, fault tolerance, scaling).
- Prompts feel templated — add unusual framings, simulations, or cross-domain inspirations.

## Iteration 3 — `generator_v3`

**Generated prompts**

1. Design and implement a content-addressed storage layer over the local filesystem, where every public function is total and side-effect free. Deliver code, tests, and a 5-line design rationale.
2. Write a graph-based task DAG executor with caching of intermediate nodes from scratch — designed so each subsystem can be hot-swapped at runtime. Deliver code, tests, and a 5-line design rationale.
3. Given an existing prototype, refactor a deterministic record-and-replay debugger for asyncio programs so that it now satisfies: but the only allowed dependency is the Python standard library. Deliver code, tests, and a 5-line design rationale.
4. Optimize a distributed key-value store with Raft-based replication for production: such that the entire core fits in fewer than 400 lines. Deliver code, tests, and a 5-line design rationale.
5. Build a streaming aggregator that ingests JSON events over TCP. Constraint: with a property-based test suite that fuzzes invariants. Deliver code, tests, and a 5-line design rationale.

**Per-prompt evaluation**

| # | tokens | complexity | creativity | token_usage | useful | total |
|---|--------|------------|------------|-------------|--------|-------|
| 1 | 35 | 0.8 | 0.0 | 7.57 | 5.1 | 13.47 |
| 2 | 38 | 5.3 | 0.0 | 8.27 | 5.1 | 18.67 |
| 3 | 44 | 3.3 | 0.0 | 8.47 | 7.3 | 19.07 |
| 4 | 35 | 5.3 | 0.0 | 8.17 | 5.1 | 18.57 |
| 5 | 32 | 5.2 | 2.0 | 8.07 | 6.1 | 21.37 |

**Averages** — complexity: 3.98, creativity: 0.4, token_usage: 8.11, useful: 5.74, **total: 18.23**

**Diagnosis (feeds the next generator)**

- Prompts skew too simple — inject systems-level concerns (concurrency, persistence, fault tolerance, scaling).
- Prompts feel templated — add unusual framings, simulations, or cross-domain inspirations.
- Prompts feel academic — anchor in concrete deliverables (API surface, CLI flags, file formats, test expectations).

---

## Final Improved Generator — `generator_v4`

After three rounds of evaluate-and-rewrite, the final generator uses *candidate-and-select self-tuning*: it oversamples prompts, scores each one with the same evaluator used by the loop, and returns the top-scoring, opener-diverse subset.

**Sample output (5 prompts)**

1. Build a distributed key-value store with Raft-based replication with a simulation-mode that replays synthetic workloads; it must be memory bounded — no growth under steady load. Provide a CLI and unit tests.
2. Write a DAG executor that caches intermediate node outputs from scratch — with a simulation-mode that replays synthetic workloads — under the rule: crash-only: no graceful shutdown path. Provide a CLI and unit tests.
3. Design a distributed key-value store with Raft-based replication, designed to survive arbitrary process crashes mid-write. Constraint: memory bounded — no growth under steady load. Add a benchmark script.
4. Given a transactional in-process queue with crash recovery, optimize it: treating every operation as an idempotent algebraic event, fits in under 400 lines of code. Provide a CLI and unit tests.
5. Write a constraint solver for small SAT instances from scratch — as if the program were a tiny actor system with mailboxes — under the rule: crash-only: no graceful shutdown path. Provide a CLI and unit tests.

**v4 averages** — complexity: 5.88, creativity: 2.0, token_usage: 8.16, useful: 7.58, **total: 23.62**

## Score Trajectory

| iteration | generator | complexity | creativity | token_usage | useful | total |
|-----------|-----------|------------|------------|-------------|--------|-------|
| 1 | generator_v1 | 0.4 | 0.0 | 0.92 | 1.5 | 2.82 |
| 2 | generator_v2 | 4.6 | 0.0 | 8.146 | 8.5 | 21.246 |
| 3 | generator_v3 | 3.98 | 0.4 | 8.11 | 5.74 | 18.23 |
| final | generator_v4 | 5.88 | 2.0 | 8.16 | 7.58 | 23.62 |
