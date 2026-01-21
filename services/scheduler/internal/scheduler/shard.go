package scheduler

import "hash/fnv"

// HashToShard maps a string identifier to a shard in [0, shardCount).
func HashToShard(id string, shardCount int) int {
	h := fnv.New32a()
	_, _ = h.Write([]byte(id))
	return int(h.Sum32()) % shardCount
}

// ParseShards returns the shards owned by this instance.
// If shardList is empty, all shards are owned.
func ParseShards(shardCount int, shardList []int) map[int]bool {
	owned := map[int]bool{}
	if len(shardList) == 0 {
		for i := 0; i < shardCount; i++ {
			owned[i] = true
		}
		return owned
	}
	for _, shard := range shardList {
		if shard >= 0 && shard < shardCount {
			owned[shard] = true
		}
	}
	return owned
}
