# PebbleToy File Format Reference

PebbleToy writes two types of files to its data directory:

```
<dir>/
  wal                                   – Write-Ahead Log (single file)
  sst-<seq:016x>-<counter:016x>.sst     – Sorted String Table (zero or more)
```

All multi-byte integers are **little-endian** unless stated otherwise.
All CRC checksums use **CRC-32/IEEE** (polynomial 0xEDB88320).

---

## 1. Write-Ahead Log (`wal`)

The WAL is an append-only file that records every committed transaction
before any in-memory state is mutated. On reopening a database the WAL is
replayed to reconstruct the active MemTable.

### 1.1 File structure

The WAL file is a contiguous sequence of variable-length records with no
file-level header. Parsing stops at the first record whose magic bytes are
missing or whose CRC does not match (treating the tail as a torn write).

### 1.2 Record layout

```
Offset  Size  Type     Field
──────  ────  ───────  ──────────────────────────────
  0      4    uint32   magic      = 0xDEADBEEF
  4      8    uint64   txnID      monotonically increasing transaction ID
 12      8    uint64   seq        global sequence number at commit time
 20      1    byte     recType    see §1.3
 21      4    uint32   keyLen     byte length of key (0 for Begin/Commit/Abort)
 25      4    uint32   valLen     byte length of value (0 for Delete/markers)
 29      *    []byte   key        raw key bytes  (keyLen bytes)
 29+k    *    []byte   value      raw value bytes (valLen bytes)
 29+k+v  4    uint32   crc32      CRC-32/IEEE over all preceding bytes in record
```

Total record size = `29 + keyLen + valLen + 4` bytes.

### 1.3 Record types

| Value | Name   | Meaning                                              |
|-------|--------|------------------------------------------------------|
| 1     | Put    | Insert or overwrite key with value                   |
| 2     | Delete | Mark key as deleted (tombstone)                      |
| 3     | Begin  | Start of a transaction group                         |
| 4     | Commit | End of a committed transaction group                 |
| 5     | Abort  | End of a rolled-back transaction (records discarded) |

### 1.4 Recovery semantics

On startup the WAL is replayed linearly. Records are grouped by `txnID`.
A group is applied to the MemTable only when its `Commit` record is seen.
Groups without a `Commit` (e.g. after a crash mid-transaction) are silently
discarded. The highest `seq` value seen during replay becomes the starting
point for the global sequence counter.

After a MemTable flush the WAL is truncated to zero length; the flushed
data is now durable in an SSTable.

---

## 2. SSTable (`sst-*.sst`)

Each SSTable is an immutable, sorted, read-only file. SSTables are created
when the active MemTable is flushed and merged during compaction.

### 2.1 Overall file layout

```
┌──────────────────────────────────────────────────┐
│  Data Block 0                                    │
├──────────────────────────────────────────────────┤
│  Data Block 1                                    │
├──────────────────────────────────────────────────┤
│  …                                               │
├──────────────────────────────────────────────────┤
│  Data Block N-1                                  │
├──────────────────────────────────────────────────┤
│  Index Block                                     │
├──────────────────────────────────────────────────┤
│  Footer (24 bytes, fixed)                        │
└──────────────────────────────────────────────────┘
```

A reader always begins by reading the **Footer** to locate the **Index Block**,
then uses the index to find the relevant **Data Block(s)** for a query.

### 2.2 Data block layout

Each data block holds up to 256 entries (the `sstBlockMaxKeys` constant).

```
Offset  Size  Type     Field
──────  ────  ───────  ────────────────────────────
  0      4    uint32   numEntries   number of entries in this block
  ─── repeated numEntries times ──────────────────
  +0     4    uint32   keyLen
  +4     4    uint32   valLen       0 for tombstone entries
  +8     1    byte     flags        0x00=live, 0x01=tombstone (deleted)
  +9     8    uint64   seq          sequence number when this version was written
 +17     *    []byte   key          raw key bytes (keyLen bytes)
 +17+k   *    []byte   value        raw value bytes (valLen bytes)
  ─── end of entries ────────────────────────────
  -4     4    uint32   blockCRC     CRC-32/IEEE over all preceding bytes in block
```

Entries within a block are sorted by `key ASC`. A block stores at most one
version per key (the newest visible version at flush time). Tombstone entries
(`flags=0x01`) are preserved so that they can hide older versions in lower
levels; they are removed during compaction.

### 2.3 Index block layout

The index block immediately follows the last data block.

```
Offset  Size  Type     Field
──────  ────  ───────  ────────────────────────────
  0      4    uint32   numBlocks    number of data blocks
  ─── repeated numBlocks times ───────────────────
  +0     4    uint32   keyLen       byte length of firstKey
  +4     *    []byte   firstKey     first (smallest) key in the block
  +4+k   8    uint64   offset       byte offset of data block from file start
 +12+k   8    uint64   length       byte length of data block (including CRC)
```

The index is not CRC-protected as a whole; individual block integrity is
guaranteed by per-block CRCs. (A production implementation would add an
index CRC.)

### 2.4 Footer layout (24 bytes, fixed)

```
Offset  Size  Type     Field
──────  ────  ───────  ────────────────────────────
  0      8    uint64   indexOffset  byte offset of index block from file start
  8      8    uint64   indexLength  byte length of index block
 16      4    uint32   magic        = 0xF00DC0DE
 20      4    uint32   footerCRC    CRC-32/IEEE over bytes 0–19 of the footer
```

### 2.5 Filename encoding

```
sst-<seq:016x>-<counter:016x>.sst
```

`seq` is the global sequence number at the time the SSTable was created.
`counter` is a monotonically increasing file counter. Both are zero-padded
16-digit lowercase hexadecimal numbers. Lexicographic sort of filenames
gives files in creation order (newest last), which is reversed when loading
so that newer SSTables shadow older ones.

---

## 3. Sequence numbers and MVCC

Every write operation (Put or Delete) is assigned a monotonically increasing
**sequence number** (`seq`). Sequence numbers are:

- Assigned by `db.seq.Add(1)` under the write lock at transaction commit time.
- Stored in WAL records and in SSTable entries.
- Used by readers: a read at sequence `s` sees only entries whose `seq <= s`.

This gives **snapshot isolation**: a transaction's snapshot is the value of
`db.seq` at `Begin` time. Writes committed after `Begin` are invisible.

---

## 4. Compaction

When the number of L0 SSTables reaches `MaxL0SSTables` (default 8), a
compaction merges all L0 files into a single new SSTable. Tombstone entries
and shadowed versions are discarded. The old SSTable files are deleted after
the new file is durably written.

This is a simplified **levelled** design with only one level; a production
system would add L1/L2 levels and more sophisticated compaction strategies.
