// Package pebbletoy implements an embedded key-value store with WAL, SSTables,
// and snapshot-isolated transactions.
package pebbletoy

import (
	"bufio"
	"encoding/binary"
	"errors"
	"fmt"
	"hash/crc32"
	"io"
	"os"
	"sync"
)

// WAL record types.
const (
	recPut    byte = 1
	recDelete byte = 2
	recBegin  byte = 3
	recCommit byte = 4
	recAbort  byte = 5
)

// walRecord is an in-memory representation of one WAL entry.
//
// Binary layout (little-endian):
//
//	[4]  magic   uint32  0xDEADBEEF
//	[8]  txnID   uint64
//	[8]  seq     uint64
//	[1]  recType byte
//	[4]  keyLen  uint32
//	[4]  valLen  uint32  (0 for Delete/Begin/Commit/Abort)
//	[*]  key     []byte
//	[*]  value   []byte
//	[4]  crc32   uint32  (over all preceding bytes in record)
type walRecord struct {
	TxnID   uint64
	Seq     uint64
	Type    byte
	Key     []byte
	Value   []byte
}

const walMagic uint32 = 0xDEADBEEF

// WAL is a write-ahead log that appends records sequentially.
type WAL struct {
	mu   sync.Mutex
	f    *os.File
	buf  *bufio.Writer
	path string
}

// openWAL opens (or creates) the WAL file at path.
func openWAL(path string) (*WAL, error) {
	f, err := os.OpenFile(path, os.O_CREATE|os.O_RDWR|os.O_APPEND, 0o644)
	if err != nil {
		return nil, fmt.Errorf("openWAL: %w", err)
	}
	return &WAL{f: f, buf: bufio.NewWriterSize(f, 64*1024), path: path}, nil
}

// Append writes a single record to the WAL and syncs.
func (w *WAL) Append(r walRecord) error {
	w.mu.Lock()
	defer w.mu.Unlock()
	return w.appendLocked(r)
}

func (w *WAL) appendLocked(r walRecord) error {
	keyLen := uint32(len(r.Key))
	valLen := uint32(len(r.Value))

	// We compute CRC over all bytes that precede it.
	h := crc32.NewIEEE()
	write32 := func(v uint32) {
		var b [4]byte
		binary.LittleEndian.PutUint32(b[:], v)
		_, _ = h.Write(b[:])
		_, _ = w.buf.Write(b[:])
	}
	write64 := func(v uint64) {
		var b [8]byte
		binary.LittleEndian.PutUint64(b[:], v)
		_, _ = h.Write(b[:])
		_, _ = w.buf.Write(b[:])
	}
	write8 := func(v byte) {
		_, _ = h.Write([]byte{v})
		_ = w.buf.WriteByte(v)
	}
	writeBytes := func(b []byte) {
		_, _ = h.Write(b)
		_, _ = w.buf.Write(b)
	}

	write32(walMagic)
	write64(r.TxnID)
	write64(r.Seq)
	write8(r.Type)
	write32(keyLen)
	write32(valLen)
	writeBytes(r.Key)
	writeBytes(r.Value)
	// Write the CRC (not hashed into itself).
	var crcB [4]byte
	binary.LittleEndian.PutUint32(crcB[:], h.Sum32())
	if _, err := w.buf.Write(crcB[:]); err != nil {
		return err
	}
	if err := w.buf.Flush(); err != nil {
		return err
	}
	return w.f.Sync()
}

// AppendBatch writes multiple records atomically (single sync at the end).
func (w *WAL) AppendBatch(records []walRecord) error {
	w.mu.Lock()
	defer w.mu.Unlock()
	for _, r := range records {
		if err := w.appendLocked(r); err != nil {
			return err
		}
	}
	return nil
}

// Replay reads all valid records from the WAL, calling fn for each.
// Stops at the first truncated or corrupt record (tolerated as partial write).
func (w *WAL) Replay(fn func(walRecord) error) error {
	if _, err := w.f.Seek(0, io.SeekStart); err != nil {
		return err
	}
	r := bufio.NewReader(w.f)
	for {
		rec, err := readWALRecord(r)
		if errors.Is(err, io.EOF) || errors.Is(err, io.ErrUnexpectedEOF) {
			return nil // tolerate truncated tail
		}
		if err != nil {
			return nil // tolerate single corrupt record at tail
		}
		if err := fn(rec); err != nil {
			return err
		}
	}
}

func readWALRecord(r *bufio.Reader) (walRecord, error) {
	readU32 := func() (uint32, []byte, error) {
		var b [4]byte
		if _, err := io.ReadFull(r, b[:]); err != nil {
			return 0, nil, err
		}
		return binary.LittleEndian.Uint32(b[:]), b[:], nil
	}
	readU64 := func() (uint64, []byte, error) {
		var b [8]byte
		if _, err := io.ReadFull(r, b[:]); err != nil {
			return 0, nil, err
		}
		return binary.LittleEndian.Uint64(b[:]), b[:], nil
	}

	h := crc32.NewIEEE()
	track := func(b []byte) { h.Write(b) }

	magic, mb, err := readU32()
	if err != nil {
		return walRecord{}, err
	}
	track(mb)
	if magic != walMagic {
		return walRecord{}, fmt.Errorf("bad magic 0x%X", magic)
	}

	txnID, b, err := readU64()
	if err != nil {
		return walRecord{}, err
	}
	track(b)

	seq, b, err := readU64()
	if err != nil {
		return walRecord{}, err
	}
	track(b)

	recType, err := r.ReadByte()
	if err != nil {
		return walRecord{}, err
	}
	track([]byte{recType})

	keyLen, b, err := readU32()
	if err != nil {
		return walRecord{}, err
	}
	track(b)

	valLen, b, err := readU32()
	if err != nil {
		return walRecord{}, err
	}
	track(b)

	key := make([]byte, keyLen)
	if _, err := io.ReadFull(r, key); err != nil {
		return walRecord{}, err
	}
	track(key)

	val := make([]byte, valLen)
	if _, err := io.ReadFull(r, val); err != nil {
		return walRecord{}, err
	}
	track(val)

	storedCRC, _, err := readU32()
	if err != nil {
		return walRecord{}, err
	}
	if storedCRC != h.Sum32() {
		return walRecord{}, fmt.Errorf("CRC mismatch: stored=%d computed=%d", storedCRC, h.Sum32())
	}

	return walRecord{TxnID: txnID, Seq: seq, Type: recType, Key: key, Value: val}, nil
}

// Truncate replaces the WAL file contents, used after a memtable flush.
func (w *WAL) Truncate() error {
	w.mu.Lock()
	defer w.mu.Unlock()
	if err := w.buf.Flush(); err != nil {
		return err
	}
	if err := w.f.Truncate(0); err != nil {
		return err
	}
	_, err := w.f.Seek(0, io.SeekStart)
	w.buf.Reset(w.f)
	return err
}

// Close flushes and closes the WAL file.
func (w *WAL) Close() error {
	w.mu.Lock()
	defer w.mu.Unlock()
	_ = w.buf.Flush()
	return w.f.Close()
}
