package scheduler

import (
	"os"
	"strconv"
	"strings"
	"time"
)

// Config holds runtime configuration for the scheduler.
type Config struct {
	DatabaseURL   string
	SchedulerID   string
	ShardCount    int
	OwnedShards   map[int]bool
	LeaderKey     int64
	PollInterval  time.Duration
	LeaseTTL      time.Duration
	MaxRunsPerLoop int
}

// LoadConfig constructs Config from environment variables.
func LoadConfig() Config {
	dbURL := getenv("DATABASE_URL", "postgres://postgres:postgres@localhost:5432/workflow")
	schedulerID := getenv("SCHEDULER_ID", "scheduler-1")
	shardCount := getenvInt("SHARD_COUNT", 16)
	ownedShards := parseShardList(getenv("SHARDS", ""), shardCount)
	leaderKey := int64(getenvInt("LEADER_LOCK_KEY", 10001))
	pollInterval := time.Duration(getenvInt("POLL_INTERVAL_MS", 2000)) * time.Millisecond
	leaseTTL := time.Duration(getenvInt("LEASE_TTL_MS", 6000)) * time.Millisecond
	maxRuns := getenvInt("MAX_RUNS_PER_LOOP", 100)

	return Config{
		DatabaseURL:   dbURL,
		SchedulerID:   schedulerID,
		ShardCount:    shardCount,
		OwnedShards:   ownedShards,
		LeaderKey:     leaderKey,
		PollInterval:  pollInterval,
		LeaseTTL:      leaseTTL,
		MaxRunsPerLoop: maxRuns,
	}
}

func getenv(key, fallback string) string {
	if value := os.Getenv(key); value != "" {
		return value
	}
	return fallback
}

func getenvInt(key string, fallback int) int {
	if value := os.Getenv(key); value != "" {
		parsed, err := strconv.Atoi(value)
		if err == nil {
			return parsed
		}
	}
	return fallback
}

func parseShardList(raw string, shardCount int) map[int]bool {
	if raw == "" {
		return ParseShards(shardCount, nil)
	}
	parts := strings.Split(raw, ",")
	list := make([]int, 0, len(parts))
	for _, part := range parts {
		trimmed := strings.TrimSpace(part)
		if trimmed == "" {
			continue
		}
		if value, err := strconv.Atoi(trimmed); err == nil {
			list = append(list, value)
		}
	}
	return ParseShards(shardCount, list)
}
