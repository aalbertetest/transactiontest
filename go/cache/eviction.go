package cache

type EvictionPolicy interface {
	OnGet(key string)
	OnSet(key string)
	OnDelete(key string)
	Evict(capacity int, size int) []string
}

type lruNode struct {
	key  string
	prev *lruNode
	next *lruNode
}

type LRUEviction struct {
	nodes map[string]*lruNode
	head  *lruNode
	tail  *lruNode
}

func NewLRUEviction() *LRUEviction {
	return &LRUEviction{nodes: map[string]*lruNode{}}
}

func (l *LRUEviction) OnGet(key string) {
	node, ok := l.nodes[key]
	if !ok {
		return
	}
	l.moveToHead(node)
}

func (l *LRUEviction) OnSet(key string) {
	node, ok := l.nodes[key]
	if ok {
		l.moveToHead(node)
		return
	}
	node = &lruNode{key: key}
	l.nodes[key] = node
	l.addToHead(node)
}

func (l *LRUEviction) OnDelete(key string) {
	node, ok := l.nodes[key]
	if !ok {
		return
	}
	delete(l.nodes, key)
	l.remove(node)
}

func (l *LRUEviction) Evict(capacity int, size int) []string {
	evicted := []string{}
	for size > capacity && l.tail != nil {
		key := l.tail.key
		evicted = append(evicted, key)
		l.OnDelete(key)
		size--
	}
	return evicted
}

func (l *LRUEviction) addToHead(node *lruNode) {
	node.prev = nil
	node.next = l.head
	if l.head != nil {
		l.head.prev = node
	}
	l.head = node
	if l.tail == nil {
		l.tail = node
	}
}

func (l *LRUEviction) remove(node *lruNode) {
	if node.prev != nil {
		node.prev.next = node.next
	} else {
		l.head = node.next
	}
	if node.next != nil {
		node.next.prev = node.prev
	} else {
		l.tail = node.prev
	}
	node.prev = nil
	node.next = nil
}

func (l *LRUEviction) moveToHead(node *lruNode) {
	if node == l.head {
		return
	}
	l.remove(node)
	l.addToHead(node)
}
