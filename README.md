# Distributed In-Memory Cache (Mini-Redis)

This repository contains a reference implementation of a distributed in-memory
cache inspired by Redis. It provides a consistent architecture across Python,
Go, and TypeScript with the same core features:

- Key/value store with TTL support
- LRU eviction with capacity limits
- Sharding via consistent hashing
- Replication (primary + replicas)
- Persistence (append-only log + snapshot)
- Pub/Sub channels
- Cluster membership and routing

The implementations are intentionally minimal, dependency-light, and optimized
for clarity and testability rather than production hardening.

## Project Layout

```
docs/
  architecture.md
python/
  cache/
  tests/
  benchmarks/
go/
  cache/
  *_test.go
typescript/
  src/
  test/
  bench/
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for the full system design,
data structures, and trade-offs.

## Python

```bash
cd python
python -m unittest discover -s tests
python -m benchmarks.simple_bench
```

## Go

```bash
cd go
go test ./...
go test -bench=. ./...
```

## TypeScript

```bash
cd typescript
npm install
npm run test
npm run bench
```

## Notes

- The default persistence layer uses JSON snapshots and a line-delimited
  append-only log (AOF). Values must be JSON-serializable.
- The provided in-process transport simulates network replication and pub/sub
  fan-out. Replace it with a TCP/HTTP transport for real networking.
- TTL checks occur on read/write and via a periodic sweeper.
