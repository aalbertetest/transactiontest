package cache

import "sync"

type ReplicationMessage struct {
	Op        string
	Key       string
	Value     any
	ExpiresAt *int64
	Version   uint64
	Channel   string
	Payload   any
}

type ReplicationHandler func(message ReplicationMessage)

type Transport interface {
	Send(peerID string, message ReplicationMessage) error
}

type InMemoryTransport struct {
	mu       sync.RWMutex
	handlers map[string]ReplicationHandler
}

func NewInMemoryTransport() *InMemoryTransport {
	return &InMemoryTransport{
		handlers: map[string]ReplicationHandler{},
	}
}

func (t *InMemoryTransport) Register(peerID string, handler ReplicationHandler) {
	t.mu.Lock()
	defer t.mu.Unlock()
	t.handlers[peerID] = handler
}

func (t *InMemoryTransport) Send(peerID string, message ReplicationMessage) error {
	t.mu.RLock()
	handler := t.handlers[peerID]
	t.mu.RUnlock()
	if handler != nil {
		handler(message)
	}
	return nil
}
