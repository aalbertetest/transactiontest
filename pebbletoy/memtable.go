package pebbletoy

import (
	"bytes"
	"sort"
	"sync"
)

// internalKey is a key decorated with a sequence number.
// Higher sequence numbers are "newer". Deleted entries carry a tombstone value.
type internalKey struct {
	UserKey []byte
	Seq     uint64
	Deleted bool
}

// internalEntry pairs an internalKey with a value.
type internalEntry struct {
	Key   internalKey
	Value []byte
}

// MemTable is an in-memory sorted table backed by a sorted slice.
// Writes are O(log n) via binary search insertion; iteration is O(n).
// For production use this would be a skip-list, but a sorted slice keeps
// the implementation self-contained.
type MemTable struct {
	mu      sync.RWMutex
	entries []internalEntry
	size    int64 // approximate bytes
}

func newMemTable() *MemTable {
	return &MemTable{}
}

// Put inserts or overwrites a key with the given sequence number.
func (m *MemTable) Put(key, value []byte, seq uint64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.insert(internalEntry{
		Key:   internalKey{UserKey: cloneBytes(key), Seq: seq},
		Value: cloneBytes(value),
	})
	m.size += int64(len(key) + len(value) + 16)
}

// Delete inserts a tombstone entry for the given key.
func (m *MemTable) Delete(key []byte, seq uint64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.insert(internalEntry{
		Key: internalKey{UserKey: cloneBytes(key), Seq: seq, Deleted: true},
	})
	m.size += int64(len(key) + 16)
}

// insert places e in sorted order. Entries are sorted by (UserKey ASC, Seq DESC)
// so that newer versions of a key appear before older ones.
func (m *MemTable) insert(e internalEntry) {
	// Find the first index where the existing entry should come AFTER e:
	//   either its UserKey > e.UserKey
	//   or same UserKey and its Seq < e.Seq (smaller seq = older = comes after)
	idx := sort.Search(len(m.entries), func(i int) bool {
		cmp := bytes.Compare(m.entries[i].Key.UserKey, e.Key.UserKey)
		if cmp != 0 {
			return cmp > 0
		}
		// Same key: existing entry should be after e when its seq is smaller.
		return m.entries[i].Key.Seq < e.Key.Seq
	})
	m.entries = append(m.entries, internalEntry{})
	copy(m.entries[idx+1:], m.entries[idx:])
	m.entries[idx] = e
}

// Get returns the most recent value visible at readSeq.
// Returns (nil, false) if key is not present or is deleted.
func (m *MemTable) Get(key []byte, readSeq uint64) ([]byte, bool) {
	m.mu.RLock()
	defer m.mu.RUnlock()

	// Find the first entry with UserKey >= key
	idx := sort.Search(len(m.entries), func(i int) bool {
		return bytes.Compare(m.entries[i].Key.UserKey, key) >= 0
	})
	for i := idx; i < len(m.entries); i++ {
		e := m.entries[i]
		if !bytes.Equal(e.Key.UserKey, key) {
			break
		}
		if e.Key.Seq <= readSeq {
			if e.Key.Deleted {
				return nil, false
			}
			return cloneBytes(e.Value), true
		}
	}
	return nil, false
}

// Scan returns an iterator over keys in [start, end) visible at readSeq.
// If end is nil, iterates to the end of the table.
func (m *MemTable) Scan(start, end []byte, readSeq uint64) *MemIterator {
	m.mu.RLock()
	defer m.mu.RUnlock()
	// Snapshot entries into a deduplicated view
	seen := make(map[string]struct{})
	var snap []internalEntry
	for _, e := range m.entries {
		if e.Key.Seq > readSeq {
			continue
		}
		k := string(e.Key.UserKey)
		if _, ok := seen[k]; ok {
			continue // older version already captured
		}
		seen[k] = struct{}{}
		if e.Key.Deleted {
			continue
		}
		snap = append(snap, e)
	}
	// Filter range
	var filtered []internalEntry
	for _, e := range snap {
		if start != nil && bytes.Compare(e.Key.UserKey, start) < 0 {
			continue
		}
		if end != nil && bytes.Compare(e.Key.UserKey, end) >= 0 {
			continue
		}
		filtered = append(filtered, e)
	}
	// Already sorted; return iterator
	return &MemIterator{entries: filtered, pos: -1}
}

// Size returns approximate bytes consumed.
func (m *MemTable) Size() int64 {
	m.mu.RLock()
	defer m.mu.RUnlock()
	return m.size
}

// Entries returns a snapshot of all entries sorted by (UserKey, Seq DESC).
func (m *MemTable) Entries() []internalEntry {
	m.mu.RLock()
	defer m.mu.RUnlock()
	out := make([]internalEntry, len(m.entries))
	copy(out, m.entries)
	return out
}

// MemIterator iterates over a deduplicated, range-filtered snapshot.
type MemIterator struct {
	entries []internalEntry
	pos     int
}

func (it *MemIterator) Next() bool {
	it.pos++
	return it.pos < len(it.entries)
}

func (it *MemIterator) Key() []byte {
	return it.entries[it.pos].Key.UserKey
}

func (it *MemIterator) Value() []byte {
	return it.entries[it.pos].Value
}

func cloneBytes(b []byte) []byte {
	if b == nil {
		return nil
	}
	c := make([]byte, len(b))
	copy(c, b)
	return c
}
