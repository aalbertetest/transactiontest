package main

import (
	"fmt"
	"time"

	"workflow/config"
	"workflow/engine"
	"workflow/persistence"
	"workflow/scheduler"
	"workflow/worker"
)

func transferWorkflow(ctx *engine.WorkflowContext, input map[string]any) (any, error) {
	amount := input["amount"].(float64)
	fromAccount := input["from"].(string)
	toAccount := input["to"].(string)
	_, err := ctx.RunActivity("debit_account", map[string]any{
		"account_id": fromAccount,
		"amount":     amount,
	}, ptrInt(30), ptrInt(3), ptrInt(2))
	if err != nil {
		return nil, err
	}
	if err := ctx.Sleep(1.0); err != nil {
		return nil, err
	}
	_, err = ctx.RunActivity("credit_account", map[string]any{
		"account_id": toAccount,
		"amount":     amount,
	}, ptrInt(30), ptrInt(3), ptrInt(2))
	if err != nil {
		return nil, err
	}
	return map[string]any{
		"status": "ok",
	}, nil
}

func debitAccount(ctx *engine.ActivityContext, input map[string]any) (any, error) {
	for i := 0; i < 3; i++ {
		ctx.Heartbeat(map[string]any{"step": i})
		time.Sleep(500 * time.Millisecond)
	}
	return map[string]any{"status": "debited"}, nil
}

func creditAccount(ctx *engine.ActivityContext, input map[string]any) (any, error) {
	for i := 0; i < 2; i++ {
		ctx.Heartbeat(map[string]any{"step": i})
		time.Sleep(500 * time.Millisecond)
	}
	return map[string]any{"status": "credited"}, nil
}

func main() {
	cfg := config.DefaultConfig()
	cfg.DBPath = "workflow.db"
	p, err := persistence.NewSQLitePersistence(cfg.DBPath)
	if err != nil {
		panic(err)
	}
	eng := engine.NewWorkflowEngine(cfg, p)
	eng.RegisterWorkflow("transfer_workflow", transferWorkflow)
	eng.RegisterActivity("debit_account", debitAccount)
	eng.RegisterActivity("credit_account", creditAccount)

	w := worker.New(eng, cfg)
	s := scheduler.New(eng, cfg)

	stop := make(chan struct{})
	go w.Run(stop)
	go s.Run(stop)

	execution, err := eng.StartWorkflow("transfer_workflow", map[string]any{
		"workflow_id": "transfer-001",
		"amount":      100.0,
		"from":        "A",
		"to":          "B",
	})
	if err != nil {
		panic(err)
	}
	fmt.Printf("Started workflow %s/%s\n", execution.WorkflowID, execution.RunID)

	time.Sleep(5 * time.Second)
	close(stop)
	time.Sleep(1 * time.Second)
}

func ptrInt(value int) *int {
	return &value
}
