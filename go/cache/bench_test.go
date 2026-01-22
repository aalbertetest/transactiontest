package cache

import "strconv"

func BenchmarkNodeSet(b *testing.B) {
	node := NewNode("n1", 1000000, nil, nil, nil)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		key := "k" + strconv.Itoa(i)
		node.Set(key, i, nil, nil)
	}
}

func BenchmarkNodeGet(b *testing.B) {
	node := NewNode("n1", 1000000, nil, nil, nil)
	for i := 0; i < b.N; i++ {
		key := "k" + strconv.Itoa(i)
		node.Set(key, i, nil, nil)
	}
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		key := "k" + strconv.Itoa(i)
		node.Get(key)
	}
}

func BenchmarkClusterSet(b *testing.B) {
	transport := NewInMemoryTransport()
	nodeA := NewNode("a", 1000000, nil, transport, nil)
	nodeB := NewNode("b", 1000000, nil, transport, nil)
	cluster := NewCluster([]*Node{nodeA, nodeB}, 2)
	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		key := "k" + strconv.Itoa(i)
		cluster.Set(key, i, nil)
	}
}
