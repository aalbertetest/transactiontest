package cache

import "time"

type Node struct {
	ID          string
	store       *Store
	pubsub      *PubSub
	replicator  *Replicator
	persistence *Persistence
	version     uint64
	clock       func() int64
}

func NewNode(id string, capacity int, clock func() int64, transport Transport, persistence *Persistence) *Node {
	if clock == nil {
		clock = func() int64 { return time.Now().UnixMilli() }
	}
	node := &Node{
		ID:          id,
		store:       NewStore(capacity, nil, clock),
		pubsub:      NewPubSub(),
		replicator:  NewReplicator(transport),
		persistence: persistence,
		clock:       clock,
	}
	if t, ok := transport.(*InMemoryTransport); ok {
		t.Register(id, node.ApplyReplication)
	}
	return node
}

func (n *Node) Load() error {
	if n.persistence == nil {
		return nil
	}
	if err := n.persistence.Load(n.store); err != nil {
		return err
	}
	n.syncVersion()
	return nil
}

func (n *Node) Get(key string) (any, bool) {
	return n.store.Get(key)
}

func (n *Node) Set(key string, value any, ttlMs *int64, replicaIDs []string) uint64 {
	version := n.nextVersion()
	version, evicted := n.store.Set(key, value, ttlMs, &version)
	entry, _ := n.store.GetEntry(key)
	if n.persistence != nil {
		var expiresAt *int64
		if entry.HasExpiry {
			expiresAt = &entry.ExpiresAt
		}
		n.persistence.AppendSet(key, value, expiresAt, version)
	}
	n.replicate(replicaIDs, ReplicationMessage{
		Op:        "set",
		Key:       key,
		Value:     value,
		ExpiresAt: expiresAtFromEntry(entry),
		Version:   version,
	})
	n.recordEvictions(evicted, replicaIDs)
	return version
}

func (n *Node) Delete(key string, replicaIDs []string) bool {
	ok := n.store.Delete(key)
	if !ok {
		return false
	}
	version := n.nextVersion()
	if n.persistence != nil {
		n.persistence.AppendDelete(key, version)
	}
	n.replicate(replicaIDs, ReplicationMessage{Op: "del", Key: key, Version: version})
	return true
}

func (n *Node) Expire(key string, ttlMs int64, replicaIDs []string) bool {
	version := n.nextVersion()
	ok := n.store.Expire(key, ttlMs, &version)
	if !ok {
		return false
	}
	entry, _ := n.store.GetEntry(key)
	if n.persistence != nil && entry.HasExpiry {
		n.persistence.AppendExpire(key, entry.ExpiresAt, version)
	}
	n.replicate(replicaIDs, ReplicationMessage{
		Op:        "expire",
		Key:       key,
		ExpiresAt: expiresAtFromEntry(entry),
		Version:   version,
	})
	return true
}

func (n *Node) Publish(channel string, payload any, replicaIDs []string) int {
	delivered := n.pubsub.Publish(channel, payload)
	n.replicate(replicaIDs, ReplicationMessage{Op: "pub", Channel: channel, Payload: payload})
	return delivered
}

func (n *Node) Subscribe(channel string, handler Subscriber) func() {
	return n.pubsub.Subscribe(channel, handler)
}

func (n *Node) SweepExpired() {
	n.store.SweepExpired()
}

func (n *Node) Snapshot() error {
	if n.persistence == nil {
		return nil
	}
	return n.persistence.Snapshot(n.store)
}

func (n *Node) ApplyReplication(message ReplicationMessage) {
	switch message.Op {
	case "set":
		if message.Key == "" {
			return
		}
		if n.shouldSkip(message.Key, message.Version) {
			return
		}
		ttlMs := (*int64)(nil)
		if message.ExpiresAt != nil {
			value := *message.ExpiresAt - n.clock()
			ttlMs = &value
		}
		version := message.Version
		n.store.Set(message.Key, message.Value, ttlMs, &version)
		n.bumpVersion(message.Version)
	case "del":
		if message.Key == "" {
			return
		}
		if n.shouldSkip(message.Key, message.Version) {
			return
		}
		n.store.Delete(message.Key)
		n.bumpVersion(message.Version)
	case "expire":
		if message.Key == "" || message.ExpiresAt == nil {
			return
		}
		if n.shouldSkip(message.Key, message.Version) {
			return
		}
		ttlMs := *message.ExpiresAt - n.clock()
		version := message.Version
		n.store.Expire(message.Key, ttlMs, &version)
		n.bumpVersion(message.Version)
	case "pub":
		if message.Channel == "" {
			return
		}
		n.pubsub.Publish(message.Channel, message.Payload)
	}
}

func (n *Node) shouldSkip(key string, version uint64) bool {
	if version == 0 {
		return false
	}
	if entry, ok := n.store.GetEntry(key); ok {
		return version <= entry.Version
	}
	return false
}

func (n *Node) replicate(replicaIDs []string, message ReplicationMessage) {
	if len(replicaIDs) == 0 {
		return
	}
	n.replicator.Replicate(replicaIDs, message)
}

func (n *Node) recordEvictions(evicted []string, replicaIDs []string) {
	for _, key := range evicted {
		version := n.nextVersion()
		if n.persistence != nil {
			n.persistence.AppendDelete(key, version)
		}
		n.replicate(replicaIDs, ReplicationMessage{Op: "del", Key: key, Version: version})
	}
}

func (n *Node) nextVersion() uint64 {
	n.version++
	return n.version
}

func (n *Node) bumpVersion(incoming uint64) {
	if incoming > n.version {
		n.version = incoming
	}
}

func (n *Node) syncVersion() {
	var max uint64
	for _, entry := range n.store.Items() {
		if entry.Version > max {
			max = entry.Version
		}
	}
	n.version = max
}

func expiresAtFromEntry(entry Entry) *int64 {
	if entry.HasExpiry {
		return &entry.ExpiresAt
	}
	return nil
}
