package engine

import (
	"os"
	"testing"
)

func TestQueueEnqueuePollAck(t *testing.T) {
	_ = os.Remove("queue_test.db")
	store, err := NewSQLiteStore("queue_test.db")
	if err != nil {
		t.Fatalf("store init error: %v", err)
	}
	queue := NewDBTaskQueue(store.DB(), nil)

	taskID, err := queue.Enqueue("default", "workflow", map[string]interface{}{"workflow_id": "wf1"}, nil, 1)
	if err != nil {
		t.Fatalf("enqueue error: %v", err)
	}
	if taskID == 0 {
		t.Fatalf("expected task id")
	}

	task, err := queue.Poll("default", "workflow", 5, "worker-1")
	if err != nil {
		t.Fatalf("poll error: %v", err)
	}
	if task == nil {
		t.Fatalf("expected task")
	}
	if task.Payload["workflow_id"].(string) != "wf1" {
		t.Fatalf("unexpected payload")
	}

	if err := queue.Ack(task.ID); err != nil {
		t.Fatalf("ack error: %v", err)
	}
	task, err = queue.Poll("default", "workflow", 5, "worker-1")
	if err != nil {
		t.Fatalf("poll error: %v", err)
	}
	if task != nil {
		t.Fatalf("expected no task after ack")
	}
	_ = os.Remove("queue_test.db")
}
