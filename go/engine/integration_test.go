package engine

import (
	"os"
	"testing"
	"time"
)

func addWorkflow(ctx *WorkflowContext, input map[string]interface{}) (interface{}, error) {
	result, err := ctx.ExecuteActivity("add", map[string]interface{}{
		"a": input["a"],
		"b": input["b"],
	}, nil)
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{"sum": result}, nil
}

func addActivity(ctx *ActivityContext, input map[string]interface{}) (interface{}, error) {
	_ = ctx.Heartbeat(map[string]interface{}{"stage": "adding"})
	return int(input["a"].(int)) + int(input["b"].(int)), nil
}

func TestIntegrationWorkflowExecutes(t *testing.T) {
	_ = os.Remove("integration_test.db")
	config := DefaultConfig()
	config.DBPath = "integration_test.db"
	config.TaskQueueName = "default"
	config.WorkerID = "worker-test"

	store, err := NewSQLiteStore(config.DBPath)
	if err != nil {
		t.Fatalf("store init error: %v", err)
	}
	queue := NewDBTaskQueue(store.DB(), nil)
	engineSvc := NewWorkflowEngine(store, queue, config, nil)
	worker := NewWorker(store, queue, config, nil)
	worker.RegisterWorkflow("AddWorkflow", addWorkflow)
	worker.RegisterActivity("add", addActivity)
	scheduler := NewTimerScheduler(store, queue, config, nil)

	runID, err := engineSvc.StartWorkflow("add-workflow-1", "AddWorkflow", map[string]interface{}{"a": 2, "b": 3}, "")
	if err != nil {
		t.Fatalf("start workflow error: %v", err)
	}

	for i := 0; i < 50; i++ {
		worker.RunOnce()
		scheduler.RunOnce()
		exec, _ := store.GetWorkflowExecution("add-workflow-1", runID)
		if exec != nil && exec.State == WorkflowStateCompleted {
			break
		}
		time.Sleep(50 * time.Millisecond)
	}
	exec, _ := store.GetWorkflowExecution("add-workflow-1", runID)
	if exec == nil || exec.State != WorkflowStateCompleted {
		t.Fatalf("workflow did not complete")
	}
	_ = os.Remove("integration_test.db")
}
