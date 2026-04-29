package pebbletoy

import (
	"errors"
	"fmt"
	"os"
	"path/filepath"
	"sort"
	"strings"
	"sync"
	"sync/atomic"
)

// ErrNotFound is returned when a key does not exist.
var ErrNotFound = errors.New("key not found")

// Options controls database behavior.
type Options struct {
	// MemTableSizeLimit triggers a flush when the active memtable exceeds this
	// size in bytes. Default: 4 MB.
	MemTableSizeLimit int64

	// MaxL0SSTables triggers compaction when there are this many L0 SSTables.
	// Default: 8.
	MaxL0SSTables int
}

func (o *Options) applyDefaults() {
	if o.MemTableSizeLimit <= 0 {
		o.MemTableSizeLimit = 4 * 1024 * 1024
	}
	if o.MaxL0SSTables <= 0 {
		o.MaxL0SSTables = 8
	}
}

// DB is the main key-value database handle.
type DB struct {
	mu     sync.RWMutex
	opts   Options
	dir    string
	wal    *WAL
	mem    *MemTable      // active memtable
	imm    []*MemTable    // immutable memtables awaiting flush
	l0     []*SSTableReader
	seq    atomic.Uint64  // global sequence counter
	txnSeq atomic.Uint64  // monotonic transaction ID
	closed atomic.Bool

	flushCh chan struct{} // send to request a flush
	compCh  chan struct{} // send to request compaction
	stopCh  chan struct{} // closed to stop background goroutines
	wg      sync.WaitGroup
}

// Open opens or creates the database at dir with the given options.
func Open(dir string, opts Options) (*DB, error) {
	opts.applyDefaults()
	if err := os.MkdirAll(dir, 0o755); err != nil {
		return nil, fmt.Errorf("Open: mkdir %s: %w", dir, err)
	}

	wal, err := openWAL(filepath.Join(dir, "wal"))
	if err != nil {
		return nil, fmt.Errorf("Open: WAL: %w", err)
	}

	db := &DB{
		opts:    opts,
		dir:     dir,
		wal:     wal,
		mem:     newMemTable(),
		flushCh: make(chan struct{}, 4),
		compCh:  make(chan struct{}, 1),
		stopCh:  make(chan struct{}),
	}
	db.seq.Store(1)

	if err := db.loadSSTables(); err != nil {
		return nil, fmt.Errorf("Open: loadSSTables: %w", err)
	}
	if err := db.recoverWAL(); err != nil {
		return nil, fmt.Errorf("Open: recoverWAL: %w", err)
	}

	db.wg.Add(2)
	go db.flushWorker()
	go db.compactionWorker()

	return db, nil
}

func (db *DB) loadSSTables() error {
	entries, err := os.ReadDir(db.dir)
	if err != nil {
		return err
	}
	var maxSeq uint64
	for _, e := range entries {
		name := e.Name()
		if !strings.HasPrefix(name, "sst-") || !strings.HasSuffix(name, ".sst") {
			continue
		}
		sr, err := openSSTable(filepath.Join(db.dir, name))
		if err != nil {
			return err
		}
		db.l0 = append(db.l0, sr)
		// Parse the seq embedded in the filename: "sst-{seq:016x}-{counter:016x}.sst"
		var seq, ctr uint64
		if n, _ := fmt.Sscanf(name, "sst-%016x-%016x.sst", &seq, &ctr); n >= 1 {
			if seq > maxSeq {
				maxSeq = seq
			}
		}
	}
	// Newest SSTable first.
	sort.Slice(db.l0, func(i, j int) bool {
		return db.l0[i].path > db.l0[j].path
	})
	if maxSeq > db.seq.Load() {
		db.seq.Store(maxSeq + 1)
	}
	return nil
}

// recoverWAL replays committed transactions from the WAL into the active memtable.
func (db *DB) recoverWAL() error {
	pending := make(map[uint64][]walRecord)
	var maxSeq uint64

	err := db.wal.Replay(func(r walRecord) error {
		switch r.Type {
		case recBegin:
			pending[r.TxnID] = nil
		case recPut, recDelete:
			pending[r.TxnID] = append(pending[r.TxnID], r)
		case recCommit:
			for _, rec := range pending[r.TxnID] {
				if rec.Type == recPut {
					db.mem.Put(rec.Key, rec.Value, rec.Seq)
				} else {
					db.mem.Delete(rec.Key, rec.Seq)
				}
				if rec.Seq > maxSeq {
					maxSeq = rec.Seq
				}
			}
			delete(pending, r.TxnID)
		case recAbort:
			delete(pending, r.TxnID)
		}
		if r.Seq > maxSeq {
			maxSeq = r.Seq
		}
		return nil
	})
	if err != nil {
		return err
	}
	if maxSeq > 0 {
		db.seq.Store(maxSeq + 1)
	}
	return nil
}

// ─── Public API ───────────────────────────────────────────────────────────────

// Put stores key=value.
func (db *DB) Put(key, value []byte) error {
	t, err := db.Begin(false)
	if err != nil {
		return err
	}
	if err := t.Put(key, value); err != nil {
		_ = t.Rollback()
		return err
	}
	return t.Commit()
}

// Get retrieves the current value for key.
func (db *DB) Get(key []byte) ([]byte, error) {
	db.mu.RLock()
	seq := db.seq.Load()
	db.mu.RUnlock()
	return db.getAtSeq(key, seq)
}

// Delete removes key.
func (db *DB) Delete(key []byte) error {
	t, err := db.Begin(false)
	if err != nil {
		return err
	}
	if err := t.Delete(key); err != nil {
		_ = t.Rollback()
		return err
	}
	return t.Commit()
}

// Scan returns an iterator over keys in [start, end).
// Pass nil for end to scan to the end of the keyspace.
func (db *DB) Scan(start, end []byte) (Iterator, error) {
	db.mu.RLock()
	seq := db.seq.Load()
	db.mu.RUnlock()
	return db.scanAtSeq(start, end, seq, nil)
}

// Begin starts a snapshot-isolated transaction.
func (db *DB) Begin(readOnly bool) (*Txn, error) {
	if db.closed.Load() {
		return nil, errors.New("database closed")
	}
	db.mu.RLock()
	snapSeq := db.seq.Load()
	db.mu.RUnlock()

	txn := &Txn{
		db:       db,
		txnID:    db.txnSeq.Add(1),
		readSeq:  snapSeq,
		readOnly: readOnly,
	}
	if !readOnly {
		txn.writeSet = newMemTable()
	}
	return txn, nil
}

// Close flushes and closes the database.
func (db *DB) Close() error {
	if !db.closed.CompareAndSwap(false, true) {
		return nil
	}

	// Stop background workers.
	close(db.stopCh)
	db.wg.Wait()

	// Flush active memtable (no goroutines running now, no lock needed).
	if db.mem.Size() > 0 {
		if err := db.flushMemTable(db.mem); err != nil {
			return err
		}
	}

	for _, sr := range db.l0 {
		_ = sr.Close()
	}
	return db.wal.Close()
}

// ─── Internal reads ───────────────────────────────────────────────────────────

func (db *DB) getAtSeq(key []byte, seq uint64) ([]byte, error) {
	db.mu.RLock()
	mem := db.mem
	imm := db.imm
	l0 := db.l0
	db.mu.RUnlock()

	if v, ok := mem.Get(key, seq); ok {
		return v, nil
	}
	for i := len(imm) - 1; i >= 0; i-- {
		if v, ok := imm[i].Get(key, seq); ok {
			return v, nil
		}
	}
	for _, sr := range l0 {
		v, ok, err := sr.Get(key, seq)
		if err != nil {
			return nil, err
		}
		if ok {
			return v, nil
		}
	}
	return nil, ErrNotFound
}

func (db *DB) scanAtSeq(start, end []byte, seq uint64, txnWrites *MemTable) (Iterator, error) {
	db.mu.RLock()
	mem := db.mem
	imm := db.imm
	l0 := db.l0
	db.mu.RUnlock()

	var iters []Iterator
	if txnWrites != nil {
		iters = append(iters, txnWrites.Scan(start, end, ^uint64(0)))
	}
	iters = append(iters, mem.Scan(start, end, seq))
	for i := len(imm) - 1; i >= 0; i-- {
		iters = append(iters, imm[i].Scan(start, end, seq))
	}
	for _, sr := range l0 {
		it, err := sr.NewIterator(start, end, seq)
		if err != nil {
			return nil, err
		}
		iters = append(iters, it)
	}
	return NewMergeIterator(iters), nil
}

// ─── Transaction commit ───────────────────────────────────────────────────────

func (db *DB) commitTxn(t *Txn) error {
	entries := t.writeSet.Entries()
	if len(entries) == 0 {
		return nil
	}

	db.mu.Lock()
	commitSeq := db.seq.Add(1)
	db.mu.Unlock()

	// Deduplicate: the write-set Entries() are sorted (UserKey ASC, Seq DESC).
	// For same-key entries with equal seq (within a transaction), the LAST
	// operation per key appears LAST in the list (insertion appends after
	// same-seq entries). We iterate in reverse to pick the last-written entry.
	effective := make([]internalEntry, 0, len(entries))
	seen := make(map[string]struct{}, len(entries))
	for i := len(entries) - 1; i >= 0; i-- {
		e := entries[i]
		k := string(e.Key.UserKey)
		if _, ok := seen[k]; ok {
			continue
		}
		seen[k] = struct{}{}
		effective = append(effective, e)
	}

	// Write WAL records for the deduplicated effective write set.
	recs := make([]walRecord, 0, len(effective)+2)
	recs = append(recs, walRecord{TxnID: t.txnID, Seq: commitSeq, Type: recBegin})
	for _, e := range effective {
		r := walRecord{TxnID: t.txnID, Seq: commitSeq}
		if e.Key.Deleted {
			r.Type = recDelete
			r.Key = e.Key.UserKey
		} else {
			r.Type = recPut
			r.Key = e.Key.UserKey
			r.Value = e.Value
		}
		recs = append(recs, r)
	}
	recs = append(recs, walRecord{TxnID: t.txnID, Seq: commitSeq, Type: recCommit})

	if err := db.wal.AppendBatch(recs); err != nil {
		return fmt.Errorf("WAL write: %w", err)
	}

	// Apply effective writes to the active memtable.
	db.mu.Lock()
	for _, e := range effective {
		if e.Key.Deleted {
			db.mem.Delete(e.Key.UserKey, commitSeq)
		} else {
			db.mem.Put(e.Key.UserKey, e.Value, commitSeq)
		}
	}
	needFlush := db.mem.Size() > db.opts.MemTableSizeLimit
	db.mu.Unlock()

	if needFlush {
		select {
		case db.flushCh <- struct{}{}:
		default:
		}
	}
	return nil
}

// ─── MemTable flush ───────────────────────────────────────────────────────────

func (db *DB) flushWorker() {
	defer db.wg.Done()
	for {
		select {
		case <-db.stopCh:
			return
		case <-db.flushCh:
			db.mu.Lock()
			if db.mem.Size() <= db.opts.MemTableSizeLimit {
				db.mu.Unlock()
				continue
			}
			old := db.mem
			db.imm = append(db.imm, old)
			db.mem = newMemTable()
			db.mu.Unlock()

			if err := db.flushMemTable(old); err != nil {
				continue
			}

			db.mu.Lock()
			for i, m := range db.imm {
				if m == old {
					db.imm = append(db.imm[:i], db.imm[i+1:]...)
					break
				}
			}
			needComp := len(db.l0) >= db.opts.MaxL0SSTables
			db.mu.Unlock()

			if needComp {
				select {
				case db.compCh <- struct{}{}:
				default:
				}
			}
		}
	}
}

// flushMemTable writes m to a new SSTable file.
// Must NOT be called while holding db.mu.
func (db *DB) flushMemTable(m *MemTable) error {
	entries := m.Entries()
	if len(entries) == 0 {
		return nil
	}

	name := db.newSSTName()
	w, err := newSSTableWriter(filepath.Join(db.dir, name))
	if err != nil {
		return err
	}

	seen := make(map[string]struct{})
	for _, e := range entries {
		k := string(e.Key.UserKey)
		if _, ok := seen[k]; ok {
			continue
		}
		seen[k] = struct{}{}
		if err := w.Add(sstEntry{
			Key:     e.Key.UserKey,
			Value:   e.Value,
			Seq:     e.Key.Seq,
			Deleted: e.Key.Deleted,
		}); err != nil {
			_ = w.Close()
			return err
		}
	}
	if err := w.Finish(); err != nil {
		_ = w.Close()
		return err
	}
	_ = w.Close()

	sr, err := openSSTable(filepath.Join(db.dir, name))
	if err != nil {
		return err
	}

	db.mu.Lock()
	db.l0 = append([]*SSTableReader{sr}, db.l0...)
	db.mu.Unlock()

	return db.wal.Truncate()
}

// ─── Compaction ───────────────────────────────────────────────────────────────

func (db *DB) compactionWorker() {
	defer db.wg.Done()
	for {
		select {
		case <-db.stopCh:
			return
		case <-db.compCh:
			db.mu.RLock()
			need := len(db.l0) >= db.opts.MaxL0SSTables
			db.mu.RUnlock()
			if need {
				_ = db.compact()
			}
		}
	}
}

// compact merges all L0 SSTables into one, discarding tombstones and
// shadowed entries. Must NOT be called while holding db.mu.
func (db *DB) compact() error {
	db.mu.RLock()
	srCopy := make([]*SSTableReader, len(db.l0))
	copy(srCopy, db.l0)
	db.mu.RUnlock()

	if len(srCopy) < 2 {
		return nil
	}

	iters := make([]Iterator, len(srCopy))
	for i, sr := range srCopy {
		it, err := sr.NewIterator(nil, nil, ^uint64(0))
		if err != nil {
			return err
		}
		iters[i] = it
	}

	name := db.newSSTName()
	w, err := newSSTableWriter(filepath.Join(db.dir, name))
	if err != nil {
		return err
	}

	merge := NewMergeIterator(iters)
	for merge.Next() {
		if err := w.Add(sstEntry{
			Key:   merge.Key(),
			Value: merge.Value(),
			Seq:   db.seq.Load(),
		}); err != nil {
			_ = w.Close()
			return err
		}
	}
	if err := w.Finish(); err != nil {
		_ = w.Close()
		return err
	}
	_ = w.Close()

	sr, err := openSSTable(filepath.Join(db.dir, name))
	if err != nil {
		return err
	}

	db.mu.Lock()
	db.l0 = []*SSTableReader{sr}
	db.mu.Unlock()

	for _, old := range srCopy {
		_ = old.Close()
		_ = os.Remove(old.path)
	}
	return nil
}

// ─── Helpers & optional methods ───────────────────────────────────────────────

var sstCounter atomic.Uint64

func (db *DB) newSSTName() string {
	n := sstCounter.Add(1)
	seq := db.seq.Load()
	return fmt.Sprintf("sst-%016x-%016x.sst", seq, n)
}

// hasKey returns true if any entry (including tombstone) exists for key in m.
func (m *MemTable) hasKey(key []byte) bool {
	m.mu.RLock()
	defer m.mu.RUnlock()
	idx := sort.Search(len(m.entries), func(i int) bool {
		return string(m.entries[i].Key.UserKey) >= string(key)
	})
	return idx < len(m.entries) && string(m.entries[idx].Key.UserKey) == string(key)
}

// ForceFlush flushes the active memtable to an SSTable synchronously.
func (db *DB) ForceFlush() error {
	db.mu.Lock()
	if db.mem.Size() == 0 {
		db.mu.Unlock()
		return nil
	}
	old := db.mem
	db.imm = append(db.imm, old)
	db.mem = newMemTable()
	db.mu.Unlock()

	if err := db.flushMemTable(old); err != nil {
		return err
	}

	db.mu.Lock()
	for i, m := range db.imm {
		if m == old {
			db.imm = append(db.imm[:i], db.imm[i+1:]...)
			break
		}
	}
	db.mu.Unlock()
	return nil
}

// ForceCompact triggers a synchronous compaction.
func (db *DB) ForceCompact() error {
	return db.compact()
}

// Stat returns basic statistics.
func (db *DB) Stat() map[string]int64 {
	db.mu.RLock()
	defer db.mu.RUnlock()
	return map[string]int64{
		"memtable_size_bytes": db.mem.Size(),
		"l0_sstable_count":    int64(len(db.l0)),
		"imm_count":           int64(len(db.imm)),
	}
}
