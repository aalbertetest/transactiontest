package engine

import (
	"os"
	"testing"
)

func TestQueueEnqueueLease(t *testing.T) {
	tmp, err := os.CreateTemp("", "engine-*.sqlite")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmp.Name())
	_ = tmp.Close()

	cfg := DefaultConfig()
	cfg.DBPath = tmp.Name()
	eng, err := NewWorkflowEngine(cfg)
	if err != nil {
		t.Fatal(err)
	}

	taskID, err := eng.Queue.EnqueueTask("run-1", "workflow_task", cfg.WorkflowTaskQueue, map[string]interface{}{"run_id": "run-1"}, nil, intPtr(10), nil, 2)
	if err != nil {
		t.Fatal(err)
	}
	tasks, err := eng.Queue.LeaseTasks(cfg.WorkflowTaskQueue, 1, cfg.TaskLeaseSeconds)
	if err != nil {
		t.Fatal(err)
	}
	if len(tasks) != 1 || tasks[0].TaskID != taskID {
		t.Fatalf("unexpected lease result %+v", tasks)
	}
	_ = eng.Queue.CompleteTask(taskID)
}

func intPtr(v int) *int {
	return &v
}
