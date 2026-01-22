package cache

import (
	"bufio"
	"encoding/json"
	"os"
	"path/filepath"
	"sync"
)

type Persistence struct {
	snapshotPath string
	logPath      string
	mu           sync.Mutex
}

type snapshotEntry struct {
	Value     any    `json:"value"`
	ExpiresAt *int64 `json:"expires_at"`
	Version   uint64 `json:"version"`
}

type logRecord struct {
	Op        string `json:"op"`
	Key       string `json:"key"`
	Value     any    `json:"value,omitempty"`
	ExpiresAt *int64 `json:"expires_at,omitempty"`
	Version   uint64 `json:"version"`
}

func NewPersistence(snapshotPath, logPath string) *Persistence {
	return &Persistence{snapshotPath: snapshotPath, logPath: logPath}
}

func (p *Persistence) AppendSet(key string, value any, expiresAt *int64, version uint64) {
	p.append(logRecord{Op: "set", Key: key, Value: value, ExpiresAt: expiresAt, Version: version})
}

func (p *Persistence) AppendDelete(key string, version uint64) {
	p.append(logRecord{Op: "del", Key: key, Version: version})
}

func (p *Persistence) AppendExpire(key string, expiresAt int64, version uint64) {
	p.append(logRecord{Op: "expire", Key: key, ExpiresAt: &expiresAt, Version: version})
}

func (p *Persistence) Snapshot(store *Store) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	items := store.Items()
	data := map[string]snapshotEntry{}
	for key, entry := range items {
		var expiresAt *int64
		if entry.HasExpiry {
			exp := entry.ExpiresAt
			expiresAt = &exp
		}
		data[key] = snapshotEntry{
			Value:     entry.Value,
			ExpiresAt: expiresAt,
			Version:   entry.Version,
		}
	}
	if err := os.MkdirAll(filepath.Dir(p.snapshotPath), 0o755); err != nil {
		return err
	}
	raw, err := json.Marshal(data)
	if err != nil {
		return err
	}
	if err := os.WriteFile(p.snapshotPath, raw, 0o644); err != nil {
		return err
	}
	_ = os.WriteFile(p.logPath, []byte{}, 0o644)
	return nil
}

func (p *Persistence) Load(store *Store) error {
	if _, err := os.Stat(p.snapshotPath); err == nil {
		raw, err := os.ReadFile(p.snapshotPath)
		if err != nil {
			return err
		}
		if len(raw) > 0 {
			var snapshot map[string]snapshotEntry
			if err := json.Unmarshal(raw, &snapshot); err != nil {
				return err
			}
			p.applySnapshot(store, snapshot)
		}
	}
	if _, err := os.Stat(p.logPath); err == nil {
		file, err := os.Open(p.logPath)
		if err != nil {
			return err
		}
		defer file.Close()
		scanner := bufio.NewScanner(file)
		for scanner.Scan() {
			line := scanner.Bytes()
			if len(line) == 0 {
				continue
			}
			var record logRecord
			if err := json.Unmarshal(line, &record); err != nil {
				return err
			}
			p.applyLogRecord(store, record)
		}
		if err := scanner.Err(); err != nil {
			return err
		}
	}
	return nil
}

func (p *Persistence) append(record logRecord) {
	p.mu.Lock()
	defer p.mu.Unlock()
	if err := os.MkdirAll(filepath.Dir(p.logPath), 0o755); err != nil {
		return
	}
	file, err := os.OpenFile(p.logPath, os.O_CREATE|os.O_APPEND|os.O_WRONLY, 0o644)
	if err != nil {
		return
	}
	defer file.Close()
	writer := bufio.NewWriter(file)
	raw, err := json.Marshal(record)
	if err != nil {
		return
	}
	writer.Write(raw)
	writer.Write([]byte("\n"))
	writer.Flush()
}

func (p *Persistence) applySnapshot(store *Store, snapshot map[string]snapshotEntry) {
	now := store.Now()
	for key, entry := range snapshot {
		if entry.ExpiresAt != nil && now >= *entry.ExpiresAt {
			continue
		}
		ttlMs := (*int64)(nil)
		if entry.ExpiresAt != nil {
			value := *entry.ExpiresAt - now
			ttlMs = &value
		}
		if existing, ok := store.GetEntry(key); ok && entry.Version <= existing.Version {
			continue
		}
		version := entry.Version
		store.Set(key, entry.Value, ttlMs, &version)
	}
}

func (p *Persistence) applyLogRecord(store *Store, record logRecord) {
	if record.Key == "" {
		return
	}
	if existing, ok := store.GetEntry(record.Key); ok && record.Version <= existing.Version {
		return
	}
	switch record.Op {
	case "set":
		ttlMs := (*int64)(nil)
		if record.ExpiresAt != nil {
			value := *record.ExpiresAt - store.Now()
			ttlMs = &value
		}
		version := record.Version
		store.Set(record.Key, record.Value, ttlMs, &version)
	case "del":
		store.Delete(record.Key)
	case "expire":
		if record.ExpiresAt == nil {
			return
		}
		ttlMs := *record.ExpiresAt - store.Now()
		version := record.Version
		store.Expire(record.Key, ttlMs, &version)
	}
}
