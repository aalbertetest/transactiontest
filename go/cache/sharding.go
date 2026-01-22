package cache

import (
	"crypto/sha1"
	"encoding/binary"
	"sort"
)

type ringEntry struct {
	hash   uint64
	nodeID string
}

type HashRing struct {
	vnodes int
	ring   []ringEntry
}

func NewHashRing(nodes []string, vnodes int) *HashRing {
	ring := &HashRing{vnodes: vnodes}
	for _, node := range nodes {
		ring.AddNode(node)
	}
	return ring
}

func (r *HashRing) AddNode(nodeID string) {
	for i := 0; i < r.vnodes; i++ {
		hash := hashKey(nodeID + ":" + itoa(i))
		r.ring = append(r.ring, ringEntry{hash: hash, nodeID: nodeID})
	}
	sort.Slice(r.ring, func(i, j int) bool {
		return r.ring[i].hash < r.ring[j].hash
	})
}

func (r *HashRing) RemoveNode(nodeID string) {
	filtered := r.ring[:0]
	for _, entry := range r.ring {
		if entry.nodeID != nodeID {
			filtered = append(filtered, entry)
		}
	}
	r.ring = filtered
}

func (r *HashRing) GetNode(key string) string {
	if len(r.ring) == 0 {
		return ""
	}
	hash := hashKey(key)
	idx := sort.Search(len(r.ring), func(i int) bool {
		return r.ring[i].hash >= hash
	})
	if idx == len(r.ring) {
		idx = 0
	}
	return r.ring[idx].nodeID
}

func (r *HashRing) GetNodes(key string, count int) []string {
	if count <= 0 || len(r.ring) == 0 {
		return nil
	}
	hash := hashKey(key)
	idx := sort.Search(len(r.ring), func(i int) bool {
		return r.ring[i].hash >= hash
	})
	seen := map[string]struct{}{}
	nodes := []string{}
	for len(nodes) < count && len(seen) < len(r.ring) {
		if idx == len(r.ring) {
			idx = 0
		}
		nodeID := r.ring[idx].nodeID
		if _, ok := seen[nodeID]; !ok {
			seen[nodeID] = struct{}{}
			nodes = append(nodes, nodeID)
		}
		idx++
	}
	return nodes
}

func hashKey(value string) uint64 {
	sum := sha1.Sum([]byte(value))
	return binary.BigEndian.Uint64(sum[:8])
}

func itoa(v int) string {
	if v == 0 {
		return "0"
	}
	buf := [20]byte{}
	i := len(buf)
	for v > 0 {
		i--
		buf[i] = byte('0' + v%10)
		v /= 10
	}
	return string(buf[i:])
}
