package pebbletoy

import (
	"errors"
	"sync/atomic"
)

// Snapshot isolation model:
//
//  - Every read inside a transaction sees the state at the snapshot sequence
//    number captured at Begin time.
//  - Writes are buffered locally in a private write-set MemTable.
//  - On Commit the write set is applied to the global MemTable with a new
//    monotonically increasing commit sequence number, and WAL records for the
//    batch are appended before any in-memory mutation.
//  - Read-your-writes: Get/Scan first check the transaction's own write-set
//    before falling through to the snapshot.

var (
	ErrTxnClosed     = errors.New("transaction already committed or rolled back")
	ErrReadOnlyWrite = errors.New("write on read-only transaction")
)

// Txn is a snapshot-isolated transaction.
type Txn struct {
	db       *DB
	txnID    uint64
	readSeq  uint64     // snapshot point
	writeSet *MemTable  // local buffered writes
	readOnly bool
	done     atomic.Bool
}

// Get reads a key, checking the local write-set first then the snapshot.
func (t *Txn) Get(key []byte) ([]byte, error) {
	if t.done.Load() {
		return nil, ErrTxnClosed
	}
	// Check own writes first (read-your-writes).
	if !t.readOnly {
		if v, ok := t.writeSet.Get(key, ^uint64(0)); ok {
			return v, nil
		}
		// A local delete shows as a tombstone in writeSet.Get returning false,
		// but we need to distinguish "key in write-set as deleted" vs "key not in write-set".
		if t.writeSet.hasKey(key) {
			return nil, ErrNotFound
		}
	}
	return t.db.getAtSeq(key, t.readSeq)
}

// Put stages a write in the local write-set.
func (t *Txn) Put(key, value []byte) error {
	if t.done.Load() {
		return ErrTxnClosed
	}
	if t.readOnly {
		return ErrReadOnlyWrite
	}
	t.writeSet.Put(key, value, ^uint64(0)) // internal seq; replaced on commit
	return nil
}

// Delete stages a deletion in the local write-set.
func (t *Txn) Delete(key []byte) error {
	if t.done.Load() {
		return ErrTxnClosed
	}
	if t.readOnly {
		return ErrReadOnlyWrite
	}
	t.writeSet.Delete(key, ^uint64(0))
	return nil
}

// Scan returns an iterator over keys in [start, end) visible to this transaction.
// Keys written by this transaction are visible too.
func (t *Txn) Scan(start, end []byte) (Iterator, error) {
	if t.done.Load() {
		return nil, ErrTxnClosed
	}
	return t.db.scanAtSeq(start, end, t.readSeq, t.writeSet)
}

// Commit applies the write-set to the database atomically.
func (t *Txn) Commit() error {
	if !t.done.CompareAndSwap(false, true) {
		return ErrTxnClosed
	}
	if t.readOnly {
		return nil
	}
	return t.db.commitTxn(t)
}

// Rollback discards all pending writes.
func (t *Txn) Rollback() error {
	t.done.Store(true)
	return nil
}
