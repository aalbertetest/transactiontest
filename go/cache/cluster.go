package cache

type Cluster struct {
	nodes             map[string]*Node
	ring              *HashRing
	replicationFactor int
}

func NewCluster(nodes []*Node, replicationFactor int) *Cluster {
	nodeMap := map[string]*Node{}
	ids := []string{}
	for _, node := range nodes {
		nodeMap[node.ID] = node
		ids = append(ids, node.ID)
	}
	if replicationFactor < 1 {
		replicationFactor = 1
	}
	if replicationFactor > len(nodeMap) {
		replicationFactor = len(nodeMap)
	}
	return &Cluster{
		nodes:             nodeMap,
		ring:              NewHashRing(ids, 64),
		replicationFactor: replicationFactor,
	}
}

func (c *Cluster) AddNode(node *Node) {
	c.nodes[node.ID] = node
	c.ring.AddNode(node.ID)
	if c.replicationFactor > len(c.nodes) {
		c.replicationFactor = len(c.nodes)
	}
}

func (c *Cluster) RemoveNode(nodeID string) {
	delete(c.nodes, nodeID)
	c.ring.RemoveNode(nodeID)
	if c.replicationFactor > len(c.nodes) {
		c.replicationFactor = len(c.nodes)
	}
}

func (c *Cluster) Get(key string) (any, bool) {
	nodes := c.ring.GetNodes(key, c.replicationFactor)
	for _, nodeID := range nodes {
		if value, ok := c.nodes[nodeID].Get(key); ok {
			return value, true
		}
	}
	return nil, false
}

func (c *Cluster) Set(key string, value any, ttlMs *int64) uint64 {
	nodes := c.ring.GetNodes(key, c.replicationFactor)
	if len(nodes) == 0 {
		return 0
	}
	primary := nodes[0]
	replicas := nodes[1:]
	return c.nodes[primary].Set(key, value, ttlMs, replicas)
}

func (c *Cluster) Delete(key string) bool {
	nodes := c.ring.GetNodes(key, c.replicationFactor)
	if len(nodes) == 0 {
		return false
	}
	primary := nodes[0]
	replicas := nodes[1:]
	return c.nodes[primary].Delete(key, replicas)
}

func (c *Cluster) Expire(key string, ttlMs int64) bool {
	nodes := c.ring.GetNodes(key, c.replicationFactor)
	if len(nodes) == 0 {
		return false
	}
	primary := nodes[0]
	replicas := nodes[1:]
	return c.nodes[primary].Expire(key, ttlMs, replicas)
}

func (c *Cluster) Publish(channel string, payload any) int {
	if len(c.nodes) == 0 {
		return 0
	}
	primary := c.ring.GetNode(channel)
	replicas := []string{}
	for nodeID := range c.nodes {
		if nodeID != primary {
			replicas = append(replicas, nodeID)
		}
	}
	return c.nodes[primary].Publish(channel, payload, replicas)
}

func (c *Cluster) SweepExpired() {
	for _, node := range c.nodes {
		node.SweepExpired()
	}
}

func (c *Cluster) Snapshot() {
	for _, node := range c.nodes {
		_ = node.Snapshot()
	}
}
