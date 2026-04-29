package pebbletoy

import "bytes"

// Iterator is the common interface for all iterators (MemTable, SSTable, Merge).
type Iterator interface {
	Next() bool
	Key() []byte
	Value() []byte
}

// MergeIterator merges multiple sorted iterators into a single sorted stream,
// resolving duplicates by preferring the iterator with the lowest index
// (memtable entries beat older SSTables).
//
// This implements a simple N-way merge using a linear scan over the current
// heads. For small N (typically 2–8) this is faster than a heap.
type MergeIterator struct {
	iters   []Iterator
	heads   []mergeHead // current head of each non-exhausted iterator
	current int         // index of iterator serving the current key
}

type mergeHead struct {
	valid bool
	key   []byte
	value []byte
}

// NewMergeIterator creates a merge iterator. iters[0] has highest priority
// (memtable); later entries are older SSTables.
func NewMergeIterator(iters []Iterator) *MergeIterator {
	m := &MergeIterator{
		iters:   iters,
		heads:   make([]mergeHead, len(iters)),
		current: -1, // -1 = not yet positioned
	}
	// Prime all heads.
	for i, it := range iters {
		if it.Next() {
			m.heads[i] = mergeHead{valid: true, key: it.Key(), value: it.Value()}
		}
	}
	return m
}

// Next advances to the next unique key, skipping duplicates from lower-priority
// iterators, and returns false when exhausted.
func (m *MergeIterator) Next() bool {
	// If we served a key, advance all iterators that were at that key.
	if m.current >= 0 {
		servedKey := m.heads[m.current].key
		for i, it := range m.iters {
			if m.heads[i].valid && bytes.Equal(m.heads[i].key, servedKey) {
				if it.Next() {
					m.heads[i] = mergeHead{valid: true, key: it.Key(), value: it.Value()}
				} else {
					m.heads[i].valid = false
				}
			}
		}
	}
	m.current = -1

	// Find smallest key among valid heads; prefer lowest index on tie.
	var minKey []byte
	for i, h := range m.heads {
		if !h.valid {
			continue
		}
		if minKey == nil || bytes.Compare(h.key, minKey) < 0 {
			minKey = h.key
			m.current = i
		}
	}
	return m.current >= 0
}

func (m *MergeIterator) Key() []byte   { return m.heads[m.current].key }
func (m *MergeIterator) Value() []byte { return m.heads[m.current].value }
