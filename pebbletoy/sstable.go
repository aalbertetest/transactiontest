package pebbletoy

import (
	"bytes"
	"encoding/binary"
	"fmt"
	"hash/crc32"
	"io"
	"os"
)

// SSTable (Sorted String Table) file layout:
//
//	┌─────────────────────────────────────────────┐
//	│  Data Blocks (variable count)               │
//	│    Each block:                              │
//	│      [4]  numEntries  uint32                │
//	│      for each entry:                        │
//	│        [4]  keyLen    uint32                │
//	│        [4]  valLen    uint32 (0=tombstone)  │
//	│        [1]  flags     byte   (1=deleted)    │
//	│        [8]  seq       uint64                │
//	│        [*]  key       []byte                │
//	│        [*]  value     []byte                │
//	│      [4]  blockCRC   uint32                 │
//	├─────────────────────────────────────────────┤
//	│  Index Block                                │
//	│    [4]  numBlocks  uint32                   │
//	│    for each block:                          │
//	│      [4]  keyLen   uint32                   │
//	│      [*]  firstKey []byte                   │
//	│      [8]  offset   uint64 (byte offset)     │
//	│      [8]  length   uint64 (block byte size) │
//	├─────────────────────────────────────────────┤
//	│  Footer (fixed 24 bytes)                    │
//	│    [8]  indexOffset  uint64                 │
//	│    [8]  indexLength  uint64                 │
//	│    [4]  magic        uint32  0xF00DC0DE     │
//	│    [4]  footerCRC    uint32                 │
//	└─────────────────────────────────────────────┘

const (
	sstMagic        uint32 = 0xF00DC0DE
	sstBlockMaxKeys        = 256 // entries per data block
	footerSize             = 24
)

// sstEntry is one key/value record inside an SSTable.
type sstEntry struct {
	Key     []byte
	Value   []byte
	Seq     uint64
	Deleted bool
}

// indexEntry describes a data block inside the SSTable.
type indexEntry struct {
	FirstKey []byte
	Offset   uint64
	Length   uint64
}

// ─── Writer ──────────────────────────────────────────────────────────────────

// SSTableWriter builds an immutable SSTable file from a sorted stream of entries.
type SSTableWriter struct {
	path   string
	f      *os.File
	w      *countingWriter
	idx    []indexEntry
	block  []sstEntry
}

type countingWriter struct {
	w      io.Writer
	offset uint64
}

func (c *countingWriter) Write(p []byte) (int, error) {
	n, err := c.w.Write(p)
	c.offset += uint64(n)
	return n, err
}

func newSSTableWriter(path string) (*SSTableWriter, error) {
	f, err := os.OpenFile(path, os.O_CREATE|os.O_WRONLY|os.O_TRUNC, 0o644)
	if err != nil {
		return nil, err
	}
	return &SSTableWriter{
		path: path,
		f:    f,
		w:    &countingWriter{w: newBufWriter(f, 256*1024)},
	}, nil
}

// Add appends one entry; flushes a data block when it reaches sstBlockMaxKeys.
func (sw *SSTableWriter) Add(e sstEntry) error {
	sw.block = append(sw.block, e)
	if len(sw.block) >= sstBlockMaxKeys {
		return sw.flushBlock()
	}
	return nil
}

func (sw *SSTableWriter) flushBlock() error {
	if len(sw.block) == 0 {
		return nil
	}
	startOff := sw.w.offset
	h := crc32.NewIEEE()
	hw := io.MultiWriter(sw.w, h)

	if err := writeU32(hw, uint32(len(sw.block))); err != nil {
		return err
	}
	for _, e := range sw.block {
		if err := writeU32(hw, uint32(len(e.Key))); err != nil {
			return err
		}
		if err := writeU32(hw, uint32(len(e.Value))); err != nil {
			return err
		}
		flag := byte(0)
		if e.Deleted {
			flag = 1
		}
		if _, err := hw.Write([]byte{flag}); err != nil {
			return err
		}
		if err := writeU64(hw, e.Seq); err != nil {
			return err
		}
		if _, err := hw.Write(e.Key); err != nil {
			return err
		}
		if _, err := hw.Write(e.Value); err != nil {
			return err
		}
	}
	// CRC goes directly to output (not hashed into itself)
	if err := writeU32(sw.w, h.Sum32()); err != nil {
		return err
	}
	blockLen := sw.w.offset - startOff
	sw.idx = append(sw.idx, indexEntry{
		FirstKey: cloneBytes(sw.block[0].Key),
		Offset:   startOff,
		Length:   blockLen,
	})
	sw.block = sw.block[:0]
	return nil
}

// Finish flushes remaining entries, writes the index block and footer, then syncs.
func (sw *SSTableWriter) Finish() error {
	if err := sw.flushBlock(); err != nil {
		return err
	}

	idxOffset := sw.w.offset
	if err := writeU32(sw.w, uint32(len(sw.idx))); err != nil {
		return err
	}
	for _, ie := range sw.idx {
		if err := writeU32(sw.w, uint32(len(ie.FirstKey))); err != nil {
			return err
		}
		if _, err := sw.w.Write(ie.FirstKey); err != nil {
			return err
		}
		if err := writeU64(sw.w, ie.Offset); err != nil {
			return err
		}
		if err := writeU64(sw.w, ie.Length); err != nil {
			return err
		}
	}
	idxLength := sw.w.offset - idxOffset

	// Footer: 8+8+4+4 = 24 bytes.
	h := crc32.NewIEEE()
	hfw := io.MultiWriter(sw.w, h)
	if err := writeU64(hfw, idxOffset); err != nil {
		return err
	}
	if err := writeU64(hfw, idxLength); err != nil {
		return err
	}
	if err := writeU32(hfw, sstMagic); err != nil {
		return err
	}
	if err := writeU32(sw.w, h.Sum32()); err != nil {
		return err
	}

	// Flush the buffered writer.
	if bw, ok := sw.w.w.(interface{ Flush() error }); ok {
		if err := bw.Flush(); err != nil {
			return err
		}
	}
	return sw.f.Sync()
}

func (sw *SSTableWriter) Close() error {
	if bw, ok := sw.w.w.(interface{ Flush() error }); ok {
		_ = bw.Flush()
	}
	return sw.f.Close()
}

// ─── Reader ───────────────────────────────────────────────────────────────────

// SSTableReader reads an immutable SSTable file using its embedded index.
type SSTableReader struct {
	path   string
	f      *os.File
	idx    []indexEntry
	minKey []byte
}

func openSSTable(path string) (*SSTableReader, error) {
	f, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	sr := &SSTableReader{path: path, f: f}
	if err := sr.loadIndex(); err != nil {
		_ = f.Close()
		return nil, err
	}
	return sr, nil
}

func (sr *SSTableReader) loadIndex() error {
	fi, err := sr.f.Stat()
	if err != nil {
		return err
	}
	size := fi.Size()
	if size < footerSize {
		return fmt.Errorf("sstable %s too small (%d bytes)", sr.path, size)
	}

	var footer [footerSize]byte
	if _, err := sr.f.ReadAt(footer[:], size-int64(footerSize)); err != nil {
		return err
	}
	h := crc32.NewIEEE()
	h.Write(footer[:footerSize-4])
	if binary.LittleEndian.Uint32(footer[footerSize-4:]) != h.Sum32() {
		return fmt.Errorf("footer CRC mismatch in %s", sr.path)
	}
	if binary.LittleEndian.Uint32(footer[16:20]) != sstMagic {
		return fmt.Errorf("bad magic in %s", sr.path)
	}
	idxOffset := binary.LittleEndian.Uint64(footer[0:8])
	idxLength := binary.LittleEndian.Uint64(footer[8:16])

	idxData := make([]byte, idxLength)
	if _, err := sr.f.ReadAt(idxData, int64(idxOffset)); err != nil {
		return err
	}
	br := bytes.NewReader(idxData)
	numBlocks, err := readU32R(br)
	if err != nil {
		return err
	}
	sr.idx = make([]indexEntry, numBlocks)
	for i := range sr.idx {
		kl, err := readU32R(br)
		if err != nil {
			return err
		}
		key := make([]byte, kl)
		if _, err := io.ReadFull(br, key); err != nil {
			return err
		}
		off, err := readU64R(br)
		if err != nil {
			return err
		}
		ln, err := readU64R(br)
		if err != nil {
			return err
		}
		sr.idx[i] = indexEntry{FirstKey: key, Offset: off, Length: ln}
	}
	if len(sr.idx) > 0 {
		sr.minKey = sr.idx[0].FirstKey
	}
	return nil
}

func (sr *SSTableReader) readBlock(ie indexEntry) ([]sstEntry, error) {
	data := make([]byte, ie.Length)
	if _, err := sr.f.ReadAt(data, int64(ie.Offset)); err != nil {
		return nil, err
	}
	if len(data) < 4 {
		return nil, fmt.Errorf("block too small in %s", sr.path)
	}
	h := crc32.NewIEEE()
	h.Write(data[:len(data)-4])
	if binary.LittleEndian.Uint32(data[len(data)-4:]) != h.Sum32() {
		return nil, fmt.Errorf("block CRC mismatch in %s at offset %d", sr.path, ie.Offset)
	}
	br := bytes.NewReader(data[:len(data)-4])
	numEntries, err := readU32R(br)
	if err != nil {
		return nil, err
	}
	entries := make([]sstEntry, 0, numEntries)
	for i := uint32(0); i < numEntries; i++ {
		kl, err := readU32R(br)
		if err != nil {
			return nil, err
		}
		vl, err := readU32R(br)
		if err != nil {
			return nil, err
		}
		var flag [1]byte
		if _, err := io.ReadFull(br, flag[:]); err != nil {
			return nil, err
		}
		seq, err := readU64R(br)
		if err != nil {
			return nil, err
		}
		key := make([]byte, kl)
		if _, err := io.ReadFull(br, key); err != nil {
			return nil, err
		}
		val := make([]byte, vl)
		if _, err := io.ReadFull(br, val); err != nil {
			return nil, err
		}
		entries = append(entries, sstEntry{Key: key, Value: val, Seq: seq, Deleted: flag[0] == 1})
	}
	return entries, nil
}

// Get returns the newest value for key visible at readSeq, searching by block index.
func (sr *SSTableReader) Get(key []byte, readSeq uint64) ([]byte, bool, error) {
	if len(sr.idx) == 0 {
		return nil, false, nil
	}
	if bytes.Compare(key, sr.minKey) < 0 {
		return nil, false, nil
	}

	// Find the rightmost block whose firstKey <= key.
	bi := sstBinarySearch(sr.idx, key) - 1
	if bi < 0 {
		bi = 0
	}
	for ; bi < len(sr.idx); bi++ {
		if bytes.Compare(sr.idx[bi].FirstKey, key) > 0 {
			break
		}
		entries, err := sr.readBlock(sr.idx[bi])
		if err != nil {
			return nil, false, err
		}
		for _, e := range entries {
			if bytes.Equal(e.Key, key) && e.Seq <= readSeq {
				if e.Deleted {
					return nil, false, nil
				}
				return cloneBytes(e.Value), true, nil
			}
		}
	}
	return nil, false, nil
}

// NewIterator returns an iterator over entries in [start, end) visible at readSeq.
func (sr *SSTableReader) NewIterator(start, end []byte, readSeq uint64) (*SSTableIterator, error) {
	var result []sstEntry
	seen := make(map[string]struct{})

	for _, ie := range sr.idx {
		if end != nil && bytes.Compare(ie.FirstKey, end) >= 0 {
			break
		}
		entries, err := sr.readBlock(ie)
		if err != nil {
			return nil, err
		}
		for _, e := range entries {
			if e.Seq > readSeq {
				continue
			}
			k := string(e.Key)
			if _, ok := seen[k]; ok {
				continue
			}
			seen[k] = struct{}{}
			if e.Deleted {
				continue
			}
			if start != nil && bytes.Compare(e.Key, start) < 0 {
				continue
			}
			if end != nil && bytes.Compare(e.Key, end) >= 0 {
				continue
			}
			result = append(result, e)
		}
	}
	return &SSTableIterator{entries: result, pos: -1}, nil
}

func (sr *SSTableReader) Close() error { return sr.f.Close() }

// sstBinarySearch returns the first index where idx[i].FirstKey > key.
func sstBinarySearch(idx []indexEntry, key []byte) int {
	lo, hi := 0, len(idx)
	for lo < hi {
		mid := (lo + hi) >> 1
		if bytes.Compare(idx[mid].FirstKey, key) <= 0 {
			lo = mid + 1
		} else {
			hi = mid
		}
	}
	return lo
}

// ─── SSTable Iterator ────────────────────────────────────────────────────────

// SSTableIterator iterates over a filtered, deduplicated snapshot of SSTable entries.
type SSTableIterator struct {
	entries []sstEntry
	pos     int
}

func (it *SSTableIterator) Next() bool {
	it.pos++
	return it.pos < len(it.entries)
}
func (it *SSTableIterator) Key() []byte   { return it.entries[it.pos].Key }
func (it *SSTableIterator) Value() []byte { return it.entries[it.pos].Value }

// ─── Encoding helpers ────────────────────────────────────────────────────────

func writeU32(w io.Writer, v uint32) error {
	var b [4]byte
	binary.LittleEndian.PutUint32(b[:], v)
	_, err := w.Write(b[:])
	return err
}

func writeU64(w io.Writer, v uint64) error {
	var b [8]byte
	binary.LittleEndian.PutUint64(b[:], v)
	_, err := w.Write(b[:])
	return err
}

func readU32R(r io.Reader) (uint32, error) {
	var b [4]byte
	_, err := io.ReadFull(r, b[:])
	return binary.LittleEndian.Uint32(b[:]), err
}

func readU64R(r io.Reader) (uint64, error) {
	var b [8]byte
	_, err := io.ReadFull(r, b[:])
	return binary.LittleEndian.Uint64(b[:]), err
}
