package cache

import (
	"os"
	"path/filepath"
	"testing"
)

func TestSetGetTTL(t *testing.T) {
	now := int64(0)
	clock := func() int64 { return now }
	node := NewNode("n1", 128, clock, nil, nil)
	ttl := int64(10)
	node.Set("a", "value", &ttl, nil)
	if value, ok := node.Get("a"); !ok || value != "value" {
		t.Fatalf("expected value, got %v", value)
	}
	now = 11
	if _, ok := node.Get("a"); ok {
		t.Fatalf("expected expired value")
	}
}

func TestLRUEviction(t *testing.T) {
	node := NewNode("n1", 2, func() int64 { return 0 }, nil, nil)
	node.Set("a", 1, nil, nil)
	node.Set("b", 2, nil, nil)
	node.Get("a")
	node.Set("c", 3, nil, nil)
	if _, ok := node.Get("b"); ok {
		t.Fatalf("expected b to be evicted")
	}
	if value, ok := node.Get("a"); !ok || value != 1 {
		t.Fatalf("expected a to be present")
	}
}

func TestReplication(t *testing.T) {
	transport := NewInMemoryTransport()
	nodeA := NewNode("a", 128, func() int64 { return 0 }, transport, nil)
	nodeB := NewNode("b", 128, func() int64 { return 0 }, transport, nil)
	cluster := NewCluster([]*Node{nodeA, nodeB}, 2)
	cluster.Set("k1", "v1", nil)
	if value, ok := nodeB.Get("k1"); !ok || value != "v1" {
		t.Fatalf("expected replica to have value")
	}
}

func TestPersistenceSnapshotAndLog(t *testing.T) {
	dir, err := os.MkdirTemp("", "cache")
	if err != nil {
		t.Fatalf("temp dir: %v", err)
	}
	defer os.RemoveAll(dir)
	snapshot := filepath.Join(dir, "snapshot.json")
	logPath := filepath.Join(dir, "aof.log")
	persistence := NewPersistence(snapshot, logPath)

	now := int64(1000)
	clock := func() int64 { return now }
	node := NewNode("n1", 128, clock, nil, persistence)
	node.Set("a", "value", nil, nil)
	if err := node.Snapshot(); err != nil {
		t.Fatalf("snapshot: %v", err)
	}
	ttl := int64(100)
	node.Set("b", "value2", &ttl, nil)

	node2 := NewNode("n2", 128, clock, nil, persistence)
	if err := node2.Load(); err != nil {
		t.Fatalf("load: %v", err)
	}
	if value, ok := node2.Get("a"); !ok || value != "value" {
		t.Fatalf("expected snapshot value")
	}
	if value, ok := node2.Get("b"); !ok || value != "value2" {
		t.Fatalf("expected log value")
	}
	now += 200
	if _, ok := node2.Get("b"); ok {
		t.Fatalf("expected b to expire")
	}
}

func TestPubSubCluster(t *testing.T) {
	transport := NewInMemoryTransport()
	nodeA := NewNode("a", 128, nil, transport, nil)
	nodeB := NewNode("b", 128, nil, transport, nil)
	cluster := NewCluster([]*Node{nodeA, nodeB}, 2)
	received := []any{}
	nodeB.Subscribe("news", func(payload any) {
		received = append(received, payload)
	})
	cluster.Publish("news", map[string]string{"hello": "world"})
	if len(received) != 1 {
		t.Fatalf("expected pubsub delivery")
	}
}
