# PebbleToy

An embedded key-value store written in Go, built for learning and
experimentation. It implements a subset of the design patterns found in
production engines like LevelDB, RocksDB, and Pebble.

## Features

| Feature | Details |
|---|---|
| **API** | `Put`, `Get`, `Delete`, `Scan` (range iteration) |
| **Persistence** | Data written to SSTables (Sorted String Tables) on disk |
| **Write-Ahead Log** | Every commit is durable before the memtable is updated |
| **Crash recovery** | WAL is replayed on restart; partial writes are tolerated |
| **Transactions** | `Begin` / `Commit` / `Rollback` with snapshot isolation |
| **Compaction** | Background merging of L0 SSTables |

## Language choice

Go was chosen because:
- Its standard library covers all needed primitives (`encoding/binary`, `hash/crc32`, `sync`, `bufio`, `os`)
- First-class benchmark support (`testing.B`) makes performance measurement straightforward
- Goroutines and channels map cleanly to the background flush/compaction worker pattern
- The existing production database Pebble (used by CockroachDB) is written in Go, making the design patterns well-understood

## Architecture

```
  ┌──────────────────────────────────────────┐
  │                   DB                     │
  │  ┌────────┐  ┌──────────┐  ┌─────────┐  │
  │  │  WAL   │  │MemTable  │  │ImmMem[] │  │
  │  │(append)│  │(active)  │  │(flushing│  │
  │  └────────┘  └──────────┘  └─────────┘  │
  │                                          │
  │  ┌──────────────────────────────────┐    │
  │  │  L0 SSTables (newest → oldest)  │    │
  │  └──────────────────────────────────┘    │
  └──────────────────────────────────────────┘
```

**Write path**: WAL append → MemTable insert → (async) flush to SSTable  
**Read path**: MemTable → Immutable MemTables → L0 SSTables (newest first)  
**Scan path**: MergeIterator over all layers, deduplicated by sequence number

## Quick start

```go
import pt "github.com/pebbletoy/pebbletoy"

db, err := pt.Open("/tmp/mydb", pt.Options{})
if err != nil { log.Fatal(err) }
defer db.Close()

// Basic operations
db.Put([]byte("hello"), []byte("world"))
val, _ := db.Get([]byte("hello"))  // → "world"
db.Delete([]byte("hello"))

// Range scan
it, _ := db.Scan([]byte("a"), []byte("z"))
for it.Next() {
    fmt.Printf("%s = %s\n", it.Key(), it.Value())
}

// Transactions
txn, _ := db.Begin(false)
txn.Put([]byte("counter"), []byte("1"))
txn.Put([]byte("name"),    []byte("alice"))
if err := txn.Commit(); err != nil {
    txn.Rollback()
}
```

## Options

```go
type Options struct {
    // Flush memtable to SSTable when it exceeds this many bytes.
    // Default: 4 MB
    MemTableSizeLimit int64

    // Run compaction when L0 has this many SSTables.
    // Default: 8
    MaxL0SSTables int
}
```

## File format

See [FILE_FORMAT.md](FILE_FORMAT.md) for the complete binary format
documentation for WAL records and SSTable files.

## Running tests

```bash
cd pebbletoy
go test ./...                  # all tests
go test -v -run TestRandom     # randomized/fuzz-style tests
go test -v -run TestCrash      # crash recovery test
```

## Running benchmarks

```bash
go test -bench=. -benchmem -benchtime=5s
```

Sample results on an Intel Xeon:

| Benchmark | Ops/sec | Latency | Allocs/op |
|---|---|---|---|
| PutSequential | ~1,400/s | ~721 µs | 42 |
| PutRandom | ~1,500/s | ~672 µs | 42 |
| GetSequential (hot) | ~4M/s | ~252 ns | 2 |
| GetRandom (hot) | ~4M/s | ~254 ns | 1 |
| WalAppend (raw) | ~3,500/s | ~280 µs | 8 |
| TxnCommit (10 ops) | ~258/s | ~3.9 ms | 227 |

Put/WAL latency is dominated by `fsync`. GetSequential/Random are in-memory
MemTable lookups (binary search on sorted slice).

## Limitations (not production-ready)

- MemTable uses a sorted slice (O(n) insertions); a production engine uses a
  skip-list or B-tree for O(log n).
- Only one compaction level (L0); multi-level compaction would control space
  amplification better.
- No bloom filters; every SSTable Get reads the index + at least one block.
- No compression (snappy/zstd).
- No concurrent transaction conflict detection (no write-write conflict check).
- Single WAL file; no log recycling.
