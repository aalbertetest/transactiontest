package cache

import "sync"

type Entry struct {
	Value     any
	ExpiresAt int64
	HasExpiry bool
	Version   uint64
}

type Store struct {
	mu       sync.Mutex
	entries  map[string]Entry
	eviction EvictionPolicy
	capacity int
	version  uint64
	clock    func() int64
}

func NewStore(capacity int, eviction EvictionPolicy, clock func() int64) *Store {
	if eviction == nil {
		eviction = NewLRUEviction()
	}
	return &Store{
		entries:  map[string]Entry{},
		eviction: eviction,
		capacity: capacity,
		clock:    clock,
	}
}

func (s *Store) Set(key string, value any, ttlMs *int64, version *uint64) (uint64, []string) {
	s.mu.Lock()
	defer s.mu.Unlock()
	expiresAt := int64(0)
	hasExpiry := false
	if ttlMs != nil {
		expiresAt = s.clock() + *ttlMs
		hasExpiry = true
	}
	if version == nil {
		s.version++
		version = &s.version
	}
	s.entries[key] = Entry{
		Value:     value,
		ExpiresAt: expiresAt,
		HasExpiry: hasExpiry,
		Version:   *version,
	}
	s.eviction.OnSet(key)
	evicted := s.evictIfNeeded()
	return *version, evicted
}

func (s *Store) Get(key string) (any, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	entry, ok := s.entries[key]
	if !ok {
		return nil, false
	}
	if s.isExpired(entry) {
		delete(s.entries, key)
		s.eviction.OnDelete(key)
		return nil, false
	}
	s.eviction.OnGet(key)
	return entry.Value, true
}

func (s *Store) GetEntry(key string) (Entry, bool) {
	s.mu.Lock()
	defer s.mu.Unlock()
	entry, ok := s.entries[key]
	if !ok {
		return Entry{}, false
	}
	if s.isExpired(entry) {
		delete(s.entries, key)
		s.eviction.OnDelete(key)
		return Entry{}, false
	}
	return entry, true
}

func (s *Store) Delete(key string) bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	_, ok := s.entries[key]
	if ok {
		delete(s.entries, key)
		s.eviction.OnDelete(key)
	}
	return ok
}

func (s *Store) Expire(key string, ttlMs int64, version *uint64) bool {
	s.mu.Lock()
	defer s.mu.Unlock()
	entry, ok := s.entries[key]
	if !ok {
		return false
	}
	if version == nil {
		s.version++
		version = &s.version
	}
	entry.ExpiresAt = s.clock() + ttlMs
	entry.HasExpiry = true
	entry.Version = *version
	s.entries[key] = entry
	return true
}

func (s *Store) SweepExpired() []string {
	s.mu.Lock()
	defer s.mu.Unlock()
	expired := []string{}
	for key, entry := range s.entries {
		if s.isExpired(entry) {
			delete(s.entries, key)
			s.eviction.OnDelete(key)
			expired = append(expired, key)
		}
	}
	return expired
}

func (s *Store) Items() map[string]Entry {
	s.mu.Lock()
	defer s.mu.Unlock()
	out := make(map[string]Entry, len(s.entries))
	for k, v := range s.entries {
		out[k] = v
	}
	return out
}

func (s *Store) Now() int64 {
	return s.clock()
}

func (s *Store) isExpired(entry Entry) bool {
	return entry.HasExpiry && s.clock() >= entry.ExpiresAt
}

func (s *Store) evictIfNeeded() []string {
	if s.capacity <= 0 {
		return nil
	}
	if len(s.entries) <= s.capacity {
		return nil
	}
	evicted := s.eviction.Evict(s.capacity, len(s.entries))
	for _, key := range evicted {
		delete(s.entries, key)
	}
	return evicted
}
