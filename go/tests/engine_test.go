package tests

import (
	"os"
	"testing"
	"time"

	"workflow/config"
	"workflow/engine"
	"workflow/persistence"
	"workflow/scheduler"
	"workflow/worker"
)

func TestWorkflowEndToEnd(t *testing.T) {
	tmp, err := os.CreateTemp("", "workflow-*.db")
	if err != nil {
		t.Fatalf("failed to create temp db: %v", err)
	}
	defer os.Remove(tmp.Name())
	cfg := config.DefaultConfig()
	cfg.DBPath = tmp.Name()
	cfg.WorkerPollIntervalSeconds = 0.05
	cfg.SchedulerPollIntervalSeconds = 0.05
	cfg.LeaseSeconds = 5
	p, err := persistence.NewSQLitePersistence(cfg.DBPath)
	if err != nil {
		t.Fatalf("failed to init persistence: %v", err)
	}
	eng := engine.NewWorkflowEngine(cfg, p)

	eng.RegisterWorkflow("test_workflow", func(ctx *engine.WorkflowContext, input map[string]any) (any, error) {
		if err := ctx.Sleep(0.1); err != nil {
			return nil, err
		}
		_, err := ctx.RunActivity("echo", map[string]any{"value": input["value"]}, nil, nil, nil)
		if err != nil {
			return nil, err
		}
		return map[string]any{"status": "ok"}, nil
	})
	eng.RegisterActivity("echo", func(ctx *engine.ActivityContext, input map[string]any) (any, error) {
		return map[string]any{"echo": input["value"]}, nil
	})

	stop := make(chan struct{})
	go worker.New(eng, cfg).Run(stop)
	go scheduler.New(eng, cfg).Run(stop)

	execution, err := eng.StartWorkflow("test_workflow", map[string]any{"value": "hello"})
	if err != nil {
		t.Fatalf("start workflow failed: %v", err)
	}

	deadline := time.Now().Add(5 * time.Second)
	for time.Now().Before(deadline) {
		current, err := p.GetWorkflowExecution(execution.WorkflowID, execution.RunID)
		if err != nil {
			t.Fatalf("fetch workflow failed: %v", err)
		}
		if current.State == engine.StateCompleted {
			break
		}
		time.Sleep(100 * time.Millisecond)
	}

	close(stop)
	time.Sleep(200 * time.Millisecond)

	final, err := p.GetWorkflowExecution(execution.WorkflowID, execution.RunID)
	if err != nil {
		t.Fatalf("fetch workflow failed: %v", err)
	}
	if final.State != engine.StateCompleted {
		t.Fatalf("expected completed, got %s", final.State)
	}
}
