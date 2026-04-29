package pebbletoy

import (
	"bytes"
	"fmt"
	"math/rand"
	"os"
	"sort"
	"testing"
)

// ─── Helpers ─────────────────────────────────────────────────────────────────

func openTestDB(t *testing.T) (*DB, string) {
	t.Helper()
	dir := t.TempDir()
	db, err := Open(dir, Options{MemTableSizeLimit: 512 * 1024})
	if err != nil {
		t.Fatalf("Open: %v", err)
	}
	t.Cleanup(func() { _ = db.Close() })
	return db, dir
}

func mustPut(t *testing.T, db *DB, k, v string) {
	t.Helper()
	if err := db.Put([]byte(k), []byte(v)); err != nil {
		t.Fatalf("Put(%q): %v", k, err)
	}
}

func mustGet(t *testing.T, db *DB, k, want string) {
	t.Helper()
	v, err := db.Get([]byte(k))
	if err != nil {
		t.Fatalf("Get(%q): %v", k, err)
	}
	if string(v) != want {
		t.Fatalf("Get(%q)=%q, want %q", k, v, want)
	}
}

func mustNotFound(t *testing.T, db *DB, k string) {
	t.Helper()
	_, err := db.Get([]byte(k))
	if err != ErrNotFound {
		t.Fatalf("Get(%q)=%v, want ErrNotFound", k, err)
	}
}

// ─── Basic CRUD ───────────────────────────────────────────────────────────────

func TestPutGet(t *testing.T) {
	db, _ := openTestDB(t)
	mustPut(t, db, "hello", "world")
	mustGet(t, db, "hello", "world")
}

func TestOverwrite(t *testing.T) {
	db, _ := openTestDB(t)
	mustPut(t, db, "k", "v1")
	mustPut(t, db, "k", "v2")
	mustGet(t, db, "k", "v2")
}

func TestDelete(t *testing.T) {
	db, _ := openTestDB(t)
	mustPut(t, db, "k", "v")
	if err := db.Delete([]byte("k")); err != nil {
		t.Fatal(err)
	}
	mustNotFound(t, db, "k")
}

func TestDeleteNonExistent(t *testing.T) {
	db, _ := openTestDB(t)
	// Deleting a non-existent key should not error.
	if err := db.Delete([]byte("ghost")); err != nil {
		t.Fatal(err)
	}
	mustNotFound(t, db, "ghost")
}

func TestGetNotFound(t *testing.T) {
	db, _ := openTestDB(t)
	mustNotFound(t, db, "absent")
}

// ─── Range Scan ───────────────────────────────────────────────────────────────

func TestScan(t *testing.T) {
	db, _ := openTestDB(t)
	keys := []string{"a", "b", "c", "d", "e"}
	for _, k := range keys {
		mustPut(t, db, k, k+"-val")
	}

	it, err := db.Scan([]byte("b"), []byte("e"))
	if err != nil {
		t.Fatal(err)
	}
	var got []string
	for it.Next() {
		got = append(got, string(it.Key()))
	}
	want := []string{"b", "c", "d"}
	if fmt.Sprint(got) != fmt.Sprint(want) {
		t.Fatalf("Scan got %v, want %v", got, want)
	}
}

func TestScanNilEnd(t *testing.T) {
	db, _ := openTestDB(t)
	for i := 0; i < 5; i++ {
		mustPut(t, db, fmt.Sprintf("key%02d", i), "v")
	}
	it, err := db.Scan([]byte("key02"), nil)
	if err != nil {
		t.Fatal(err)
	}
	var got []string
	for it.Next() {
		got = append(got, string(it.Key()))
	}
	if len(got) != 3 {
		t.Fatalf("Scan got %v", got)
	}
}

func TestScanAfterDelete(t *testing.T) {
	db, _ := openTestDB(t)
	for _, k := range []string{"a", "b", "c"} {
		mustPut(t, db, k, k)
	}
	if err := db.Delete([]byte("b")); err != nil {
		t.Fatal(err)
	}
	it, err := db.Scan([]byte("a"), nil)
	if err != nil {
		t.Fatal(err)
	}
	var got []string
	for it.Next() {
		got = append(got, string(it.Key()))
	}
	if fmt.Sprint(got) != fmt.Sprint([]string{"a", "c"}) {
		t.Fatalf("want [a c], got %v", got)
	}
}

// ─── Transactions ─────────────────────────────────────────────────────────────

func TestTxnCommit(t *testing.T) {
	db, _ := openTestDB(t)
	txn, err := db.Begin(false)
	if err != nil {
		t.Fatal(err)
	}
	if err := txn.Put([]byte("a"), []byte("1")); err != nil {
		t.Fatal(err)
	}
	if err := txn.Put([]byte("b"), []byte("2")); err != nil {
		t.Fatal(err)
	}
	if err := txn.Commit(); err != nil {
		t.Fatal(err)
	}
	mustGet(t, db, "a", "1")
	mustGet(t, db, "b", "2")
}

func TestTxnRollback(t *testing.T) {
	db, _ := openTestDB(t)
	mustPut(t, db, "existing", "val")

	txn, _ := db.Begin(false)
	_ = txn.Put([]byte("existing"), []byte("new"))
	_ = txn.Put([]byte("newkey"), []byte("v"))
	_ = txn.Rollback()

	mustGet(t, db, "existing", "val")
	mustNotFound(t, db, "newkey")
}

func TestTxnReadYourWrites(t *testing.T) {
	db, _ := openTestDB(t)
	txn, _ := db.Begin(false)
	_ = txn.Put([]byte("k"), []byte("v"))
	v, err := txn.Get([]byte("k"))
	if err != nil {
		t.Fatal(err)
	}
	if string(v) != "v" {
		t.Fatalf("read-your-write: got %q", v)
	}
	_ = txn.Rollback()
}

func TestTxnSnapshotIsolation(t *testing.T) {
	db, _ := openTestDB(t)
	mustPut(t, db, "k", "original")

	// Start a long-running read-only transaction.
	snap, _ := db.Begin(true)

	// Concurrent write that should not be visible to snap.
	mustPut(t, db, "k", "updated")

	v, err := snap.Get([]byte("k"))
	if err != nil {
		t.Fatal(err)
	}
	if string(v) != "original" {
		t.Fatalf("snapshot isolation violated: got %q, want 'original'", v)
	}
	_ = snap.Rollback()
}

func TestTxnDoubleCommit(t *testing.T) {
	db, _ := openTestDB(t)
	txn, _ := db.Begin(false)
	_ = txn.Put([]byte("k"), []byte("v"))
	_ = txn.Commit()
	if err := txn.Commit(); err != ErrTxnClosed {
		t.Fatalf("expected ErrTxnClosed, got %v", err)
	}
}

func TestReadOnlyTxnWrite(t *testing.T) {
	db, _ := openTestDB(t)
	txn, _ := db.Begin(true)
	if err := txn.Put([]byte("k"), []byte("v")); err != ErrReadOnlyWrite {
		t.Fatalf("expected ErrReadOnlyWrite, got %v", err)
	}
	_ = txn.Rollback()
}

func TestTxnScan(t *testing.T) {
	db, _ := openTestDB(t)
	mustPut(t, db, "a", "1")
	mustPut(t, db, "c", "3")

	txn, _ := db.Begin(false)
	_ = txn.Put([]byte("b"), []byte("2")) // local write

	it, err := txn.Scan([]byte("a"), nil)
	if err != nil {
		t.Fatal(err)
	}
	var got []string
	for it.Next() {
		got = append(got, string(it.Key()))
	}
	if fmt.Sprint(got) != fmt.Sprint([]string{"a", "b", "c"}) {
		t.Fatalf("txn scan: got %v", got)
	}
	_ = txn.Rollback()
}

// ─── Persistence & Crash Recovery ────────────────────────────────────────────

func TestPersistenceReopen(t *testing.T) {
	dir := t.TempDir()
	func() {
		db, err := Open(dir, Options{})
		if err != nil {
			t.Fatalf("open1: %v", err)
		}
		for i := 0; i < 100; i++ {
			if err := db.Put([]byte(fmt.Sprintf("key%04d", i)), []byte(fmt.Sprintf("val%04d", i))); err != nil {
				t.Fatal(err)
			}
		}
		if err := db.Close(); err != nil {
			t.Fatal(err)
		}
	}()

	db, err := Open(dir, Options{})
	if err != nil {
		t.Fatalf("open2: %v", err)
	}
	defer db.Close()

	for i := 0; i < 100; i++ {
		k := fmt.Sprintf("key%04d", i)
		v := fmt.Sprintf("val%04d", i)
		mustGet(t, db, k, v)
	}
}

func TestCrashRecovery(t *testing.T) {
	dir := t.TempDir()

	// Write data and force a flush so it's in an SSTable.
	func() {
		db, _ := Open(dir, Options{})
		for i := 0; i < 50; i++ {
			_ = db.Put([]byte(fmt.Sprintf("k%03d", i)), []byte(fmt.Sprintf("v%03d", i)))
		}
		_ = db.ForceFlush()
		// Write more data to WAL only (no flush = simulated crash state).
		for i := 50; i < 100; i++ {
			_ = db.Put([]byte(fmt.Sprintf("k%03d", i)), []byte(fmt.Sprintf("v%03d", i)))
		}
		// Simulate crash: do NOT call db.Close() – just let it go.
		_ = db.wal.f.Sync()
	}()

	// Reopen and verify crash recovery from WAL.
	db, err := Open(dir, Options{})
	if err != nil {
		t.Fatalf("reopen after crash: %v", err)
	}
	defer db.Close()

	for i := 0; i < 100; i++ {
		k := fmt.Sprintf("k%03d", i)
		v := fmt.Sprintf("v%03d", i)
		mustGet(t, db, k, v)
	}
}

func TestPersistenceAfterFlush(t *testing.T) {
	dir := t.TempDir()
	func() {
		db, _ := Open(dir, Options{})
		mustPut(t, db, "persistent", "yes")
		_ = db.ForceFlush()
		_ = db.Close()
	}()
	db, _ := Open(dir, Options{})
	defer db.Close()
	mustGet(t, db, "persistent", "yes")
}

// ─── WAL unit tests ───────────────────────────────────────────────────────────

func TestWALRoundTrip(t *testing.T) {
	dir := t.TempDir()
	w, err := openWAL(dir + "/test.wal")
	if err != nil {
		t.Fatal(err)
	}
	recs := []walRecord{
		{TxnID: 1, Seq: 100, Type: recPut, Key: []byte("foo"), Value: []byte("bar")},
		{TxnID: 1, Seq: 101, Type: recDelete, Key: []byte("baz")},
		{TxnID: 2, Seq: 102, Type: recBegin},
		{TxnID: 2, Seq: 102, Type: recCommit},
	}
	for _, r := range recs {
		if err := w.Append(r); err != nil {
			t.Fatal(err)
		}
	}

	var got []walRecord
	if err := w.Replay(func(r walRecord) error {
		got = append(got, r)
		return nil
	}); err != nil {
		t.Fatal(err)
	}
	if len(got) != len(recs) {
		t.Fatalf("replayed %d records, want %d", len(got), len(recs))
	}
	for i, r := range recs {
		if !bytes.Equal(r.Key, got[i].Key) || !bytes.Equal(r.Value, got[i].Value) {
			t.Fatalf("record %d mismatch", i)
		}
	}
	_ = w.Close()
}

func TestWALTruncatedTolerance(t *testing.T) {
	dir := t.TempDir()
	path := dir + "/truncated.wal"
	w, _ := openWAL(path)
	_ = w.Append(walRecord{TxnID: 1, Seq: 1, Type: recPut, Key: []byte("k"), Value: []byte("v")})
	_ = w.Close()

	// Append garbage bytes simulating a torn write.
	f, _ := os.OpenFile(path, os.O_APPEND|os.O_WRONLY, 0o644)
	_, _ = f.Write([]byte{0xFF, 0xFE, 0xFD})
	_ = f.Close()

	w2, _ := openWAL(path)
	var count int
	_ = w2.Replay(func(r walRecord) error { count++; return nil })
	if count != 1 {
		t.Fatalf("expected 1 valid record, got %d", count)
	}
	_ = w2.Close()
}

// ─── SSTable unit tests ───────────────────────────────────────────────────────

func TestSSTableRoundTrip(t *testing.T) {
	dir := t.TempDir()
	path := dir + "/test.sst"
	w, err := newSSTableWriter(path)
	if err != nil {
		t.Fatal(err)
	}
	for i := 0; i < 300; i++ {
		_ = w.Add(sstEntry{Key: []byte(fmt.Sprintf("key%04d", i)), Value: []byte(fmt.Sprintf("val%04d", i)), Seq: uint64(i)})
	}
	if err := w.Finish(); err != nil {
		t.Fatal(err)
	}
	_ = w.Close()

	r, err := openSSTable(path)
	if err != nil {
		t.Fatal(err)
	}
	defer r.Close()

	for i := 0; i < 300; i++ {
		k := fmt.Sprintf("key%04d", i)
		v, ok, err := r.Get([]byte(k), ^uint64(0))
		if err != nil {
			t.Fatal(err)
		}
		if !ok {
			t.Fatalf("key%04d not found", i)
		}
		if string(v) != fmt.Sprintf("val%04d", i) {
			t.Fatalf("wrong value for %s: %s", k, v)
		}
	}
}

func TestSSTableTombstone(t *testing.T) {
	dir := t.TempDir()
	path := dir + "/tomb.sst"
	w, _ := newSSTableWriter(path)
	_ = w.Add(sstEntry{Key: []byte("a"), Value: []byte("v"), Seq: 1})
	_ = w.Add(sstEntry{Key: []byte("b"), Deleted: true, Seq: 2})
	_ = w.Finish()
	_ = w.Close()

	r, _ := openSSTable(path)
	defer r.Close()

	_, ok, _ := r.Get([]byte("b"), ^uint64(0))
	if ok {
		t.Fatal("tombstone key should not be found")
	}
	v, ok, _ := r.Get([]byte("a"), ^uint64(0))
	if !ok || string(v) != "v" {
		t.Fatal("key 'a' not found correctly")
	}
}

func TestSSTableIterator(t *testing.T) {
	dir := t.TempDir()
	path := dir + "/iter.sst"
	w, _ := newSSTableWriter(path)
	for i := 0; i < 50; i++ {
		_ = w.Add(sstEntry{Key: []byte(fmt.Sprintf("%03d", i)), Value: []byte("v"), Seq: 1})
	}
	_ = w.Finish()
	_ = w.Close()

	r, _ := openSSTable(path)
	defer r.Close()

	it, err := r.NewIterator([]byte("010"), []byte("020"), ^uint64(0))
	if err != nil {
		t.Fatal(err)
	}
	var got []string
	for it.Next() {
		got = append(got, string(it.Key()))
	}
	if len(got) != 10 {
		t.Fatalf("expected 10 entries in [010,020), got %d: %v", len(got), got)
	}
}

// ─── MemTable unit tests ──────────────────────────────────────────────────────

func TestMemTableSeqVisibility(t *testing.T) {
	m := newMemTable()
	m.Put([]byte("k"), []byte("v1"), 10)
	m.Put([]byte("k"), []byte("v2"), 20)

	v, ok := m.Get([]byte("k"), 15)
	if !ok || string(v) != "v1" {
		t.Fatalf("at seq 15 got (%q, %v), want (v1, true)", v, ok)
	}
	v, ok = m.Get([]byte("k"), 25)
	if !ok || string(v) != "v2" {
		t.Fatalf("at seq 25 got (%q, %v), want (v2, true)", v, ok)
	}
}

func TestMemTableTombstone(t *testing.T) {
	m := newMemTable()
	m.Put([]byte("k"), []byte("v"), 1)
	m.Delete([]byte("k"), 2)
	_, ok := m.Get([]byte("k"), 5)
	if ok {
		t.Fatal("deleted key visible")
	}
}

// ─── Merge Iterator unit tests ────────────────────────────────────────────────

func TestMergeIteratorDedup(t *testing.T) {
	a := &sliceIter{data: []kv{{"a", "1"}, {"b", "1"}, {"c", "1"}}}
	b := &sliceIter{data: []kv{{"b", "2"}, {"d", "2"}}}
	m := NewMergeIterator([]Iterator{a, b})
	var got []string
	for m.Next() {
		got = append(got, string(m.Key())+":"+string(m.Value()))
	}
	// b:1 should win (a has higher priority), d:2 from b.
	want := []string{"a:1", "b:1", "c:1", "d:2"}
	if fmt.Sprint(got) != fmt.Sprint(want) {
		t.Fatalf("MergeIterator: got %v, want %v", got, want)
	}
}

type kv struct{ k, v string }

type sliceIter struct {
	data []kv
	pos  int
}

func (s *sliceIter) Next() bool  { s.pos++; return s.pos <= len(s.data) }
func (s *sliceIter) Key() []byte { return []byte(s.data[s.pos-1].k) }
func (s *sliceIter) Value() []byte { return []byte(s.data[s.pos-1].v) }

// ─── Randomized / Fuzz-style Tests ───────────────────────────────────────────

// TestRandomOpsConsistency performs a series of random put/delete/get
// operations and verifies results against a reference Go map.
func TestRandomOpsConsistency(t *testing.T) {
	db, _ := openTestDB(t)
	ref := make(map[string]string)
	rng := rand.New(rand.NewSource(42))

	const (
		numOps  = 2000
		keySpace = 50
	)

	for i := 0; i < numOps; i++ {
		k := fmt.Sprintf("k%02d", rng.Intn(keySpace))
		op := rng.Intn(3)
		switch op {
		case 0: // put
			v := fmt.Sprintf("v%d", rng.Intn(1000))
			mustPut(t, db, k, v)
			ref[k] = v
		case 1: // delete
			_ = db.Delete([]byte(k))
			delete(ref, k)
		case 2: // get (verify)
			expected, exists := ref[k]
			v, err := db.Get([]byte(k))
			if exists {
				if err != nil || string(v) != expected {
					t.Fatalf("Get(%q)=(%q,%v), want (%q,nil)", k, v, err, expected)
				}
			} else {
				if err != ErrNotFound {
					t.Fatalf("Get(%q)=%v, want ErrNotFound", k, err)
				}
			}
		}
	}

	// Final consistent check.
	for k, v := range ref {
		mustGet(t, db, k, v)
	}
}

// TestRandomTransactions performs random transactions and verifies atomicity.
func TestRandomTransactions(t *testing.T) {
	db, _ := openTestDB(t)
	ref := make(map[string]string)
	rng := rand.New(rand.NewSource(99))

	const (
		numTxns  = 200
		keySpace = 20
		batchSize = 5
	)

	for i := 0; i < numTxns; i++ {
		txn, _ := db.Begin(false)
		// Apply batch to local reference copy and to txn.
		type op struct{ k, v string; del bool }
		ops := make([]op, batchSize)
		for j := range ops {
			k := fmt.Sprintf("k%02d", rng.Intn(keySpace))
			if rng.Intn(3) == 0 {
				ops[j] = op{k: k, del: true}
				_ = txn.Delete([]byte(k))
			} else {
				v := fmt.Sprintf("v%d", rng.Intn(1000))
				ops[j] = op{k: k, v: v}
				_ = txn.Put([]byte(k), []byte(v))
			}
		}

		if rng.Intn(5) == 0 { // 20% rollback
			_ = txn.Rollback()
			continue
		}
		if err := txn.Commit(); err != nil {
			t.Fatalf("commit: %v", err)
		}
		// Apply to reference only on commit.
		for _, op := range ops {
			if op.del {
				delete(ref, op.k)
			} else {
				ref[op.k] = op.v
			}
		}
	}

	// Verify consistency with reference.
	for k, v := range ref {
		got, err := db.Get([]byte(k))
		if err != nil {
			t.Fatalf("Get(%q): %v", k, err)
		}
		if string(got) != v {
			t.Fatalf("Get(%q)=%q, want %q", k, got, v)
		}
	}
}

// TestRandomScanConsistency writes random data, does a range scan, and verifies
// the scan results match what a map-based reference returns for the same range.
func TestRandomScanConsistency(t *testing.T) {
	db, _ := openTestDB(t)
	ref := make(map[string]string)
	rng := rand.New(rand.NewSource(7))

	for i := 0; i < 500; i++ {
		k := fmt.Sprintf("%04d", rng.Intn(200))
		v := fmt.Sprintf("val%d", i)
		mustPut(t, db, k, v)
		ref[k] = v
	}

	startK := "0050"
	endK := "0150"

	it, err := db.Scan([]byte(startK), []byte(endK))
	if err != nil {
		t.Fatal(err)
	}

	// Collect expected from ref.
	var expected []string
	for k := range ref {
		if k >= startK && k < endK {
			expected = append(expected, k)
		}
	}
	sort.Strings(expected)

	var got []string
	for it.Next() {
		got = append(got, string(it.Key()))
	}

	if fmt.Sprint(got) != fmt.Sprint(expected) {
		t.Fatalf("scan mismatch:\ngot:  %v\nwant: %v", got, expected)
	}
}

// TestFlushAndReadBack forces a flush to SSTable and ensures data is readable.
func TestFlushAndReadBack(t *testing.T) {
	db, _ := openTestDB(t)
	for i := 0; i < 100; i++ {
		mustPut(t, db, fmt.Sprintf("k%04d", i), fmt.Sprintf("v%04d", i))
	}
	if err := db.ForceFlush(); err != nil {
		t.Fatal(err)
	}
	for i := 0; i < 100; i++ {
		mustGet(t, db, fmt.Sprintf("k%04d", i), fmt.Sprintf("v%04d", i))
	}
}

// TestCompaction writes many keys, flushes multiple SSTables, compacts, and verifies.
func TestCompaction(t *testing.T) {
	db, _ := openTestDB(t)
	ref := make(map[string]string)

	for round := 0; round < 5; round++ {
		for i := 0; i < 50; i++ {
			k := fmt.Sprintf("k%04d", i)
			v := fmt.Sprintf("v%d-%d", round, i)
			mustPut(t, db, k, v)
			ref[k] = v
		}
		if err := db.ForceFlush(); err != nil {
			t.Fatal(err)
		}
	}

	if err := db.ForceCompact(); err != nil {
		t.Fatal(err)
	}

	for k, v := range ref {
		mustGet(t, db, k, v)
	}
}

// ─── Benchmarks ───────────────────────────────────────────────────────────────

// BenchmarkPutSequential measures sequential writes with increasing keys.
func BenchmarkPutSequential(b *testing.B) {
	dir := b.TempDir()
	db, err := Open(dir, Options{MemTableSizeLimit: 64 * 1024 * 1024})
	if err != nil {
		b.Fatal(err)
	}
	defer db.Close()

	val := bytes.Repeat([]byte("v"), 100)
	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		k := []byte(fmt.Sprintf("%016d", i))
		if err := db.Put(k, val); err != nil {
			b.Fatal(err)
		}
	}
}

// BenchmarkPutRandom measures random writes.
func BenchmarkPutRandom(b *testing.B) {
	dir := b.TempDir()
	db, err := Open(dir, Options{MemTableSizeLimit: 64 * 1024 * 1024})
	if err != nil {
		b.Fatal(err)
	}
	defer db.Close()

	rng := rand.New(rand.NewSource(42))
	val := bytes.Repeat([]byte("v"), 100)
	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		k := []byte(fmt.Sprintf("%016d", rng.Int63()))
		if err := db.Put(k, val); err != nil {
			b.Fatal(err)
		}
	}
}

// BenchmarkGetSequential measures sequential reads after sequential writes.
func BenchmarkGetSequential(b *testing.B) {
	dir := b.TempDir()
	db, err := Open(dir, Options{MemTableSizeLimit: 64 * 1024 * 1024})
	if err != nil {
		b.Fatal(err)
	}
	defer db.Close()

	const N = 10000
	val := bytes.Repeat([]byte("v"), 100)
	for i := 0; i < N; i++ {
		_ = db.Put([]byte(fmt.Sprintf("%016d", i)), val)
	}

	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		k := []byte(fmt.Sprintf("%016d", i%N))
		if _, err := db.Get(k); err != nil {
			b.Fatal(err)
		}
	}
}

// BenchmarkGetRandom measures random reads from a pre-populated database.
func BenchmarkGetRandom(b *testing.B) {
	dir := b.TempDir()
	db, err := Open(dir, Options{MemTableSizeLimit: 64 * 1024 * 1024})
	if err != nil {
		b.Fatal(err)
	}
	defer db.Close()

	const N = 10000
	val := bytes.Repeat([]byte("v"), 100)
	keys := make([][]byte, N)
	rng := rand.New(rand.NewSource(1))
	for i := 0; i < N; i++ {
		k := []byte(fmt.Sprintf("%016d", rng.Int63()))
		keys[i] = k
		_ = db.Put(k, val)
	}

	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		k := keys[i%N]
		if _, err := db.Get(k); err != nil && err != ErrNotFound {
			b.Fatal(err)
		}
	}
}

// BenchmarkScanSequential measures a range scan over 100 sequential keys.
func BenchmarkScanSequential(b *testing.B) {
	dir := b.TempDir()
	db, err := Open(dir, Options{MemTableSizeLimit: 64 * 1024 * 1024})
	if err != nil {
		b.Fatal(err)
	}
	defer db.Close()

	val := bytes.Repeat([]byte("v"), 100)
	for i := 0; i < 10000; i++ {
		_ = db.Put([]byte(fmt.Sprintf("%016d", i)), val)
	}

	b.ResetTimer()
	b.ReportAllocs()

	start := []byte(fmt.Sprintf("%016d", 1000))
	end := []byte(fmt.Sprintf("%016d", 1100))
	for i := 0; i < b.N; i++ {
		it, err := db.Scan(start, end)
		if err != nil {
			b.Fatal(err)
		}
		for it.Next() {
		}
	}
}

// BenchmarkTxnCommit measures transaction commit latency for small batches.
func BenchmarkTxnCommit(b *testing.B) {
	dir := b.TempDir()
	db, err := Open(dir, Options{MemTableSizeLimit: 64 * 1024 * 1024})
	if err != nil {
		b.Fatal(err)
	}
	defer db.Close()

	val := bytes.Repeat([]byte("v"), 100)
	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		txn, _ := db.Begin(false)
		for j := 0; j < 10; j++ {
			_ = txn.Put([]byte(fmt.Sprintf("%016d", i*10+j)), val)
		}
		if err := txn.Commit(); err != nil {
			b.Fatal(err)
		}
	}
}

// BenchmarkWALAppend measures raw WAL append throughput.
func BenchmarkWALAppend(b *testing.B) {
	dir := b.TempDir()
	w, err := openWAL(dir + "/bench.wal")
	if err != nil {
		b.Fatal(err)
	}
	defer w.Close()

	rec := walRecord{TxnID: 1, Seq: 1, Type: recPut, Key: []byte("benchkey"), Value: bytes.Repeat([]byte("v"), 100)}
	b.ResetTimer()
	b.ReportAllocs()

	for i := 0; i < b.N; i++ {
		rec.Seq = uint64(i)
		if err := w.Append(rec); err != nil {
			b.Fatal(err)
		}
	}
}
