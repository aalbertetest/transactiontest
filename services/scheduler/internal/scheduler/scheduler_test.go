package scheduler

import "testing"

func TestHashToShardStable(t *testing.T) {
	shardA := HashToShard("run-123", 16)
	shardB := HashToShard("run-123", 16)
	if shardA != shardB {
		t.Fatalf("expected stable shard hash, got %d != %d", shardA, shardB)
	}
}

func TestReadySteps(t *testing.T) {
	spec := WorkflowSpec{
		Steps: []WorkflowStep{
			{ID: "a", Type: "echo"},
			{ID: "b", Type: "sleep", DependsOn: []string{"a"}},
		},
	}
	ready := readySteps(spec, map[string]string{})
	if len(ready) != 1 || ready[0].ID != "a" {
		t.Fatalf("expected only step a to be ready")
	}

	ready = readySteps(spec, map[string]string{"a": "succeeded"})
	if len(ready) != 2 {
		t.Fatalf("expected both steps to be ready after a succeeds")
	}
}
