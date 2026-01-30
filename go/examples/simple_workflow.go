package main

import (
	"fmt"
	"os"
	"time"

	"workflowengine/engine"
)

func greetingWorkflow(ctx *engine.WorkflowContext, input map[string]interface{}) (interface{}, error) {
	version, err := ctx.GetVersion("greeting-change", 1, 2)
	if err != nil {
		return nil, err
	}
	name := input["name"].(string)
	greeting, err := ctx.ExecuteActivity("compose_greeting", map[string]interface{}{"name": name}, nil)
	if err != nil {
		return nil, err
	}
	_ = ctx.Sleep(1)
	approval, err := ctx.WaitSignal("approval")
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"greeting":    greeting,
		"approved_by": approval["user"],
		"version":     version,
	}, nil
}

func composeGreeting(ctx *engine.ActivityContext, input map[string]interface{}) (interface{}, error) {
	_ = ctx.Heartbeat(map[string]interface{}{"stage": "starting"})
	return "Hello, " + input["name"].(string) + "!", nil
}

func main() {
	if _, err := os.Stat("example.db"); err == nil {
		_ = os.Remove("example.db")
	}
	config := engine.DefaultConfig()
	config.DBPath = "example.db"
	config.TaskQueueName = "default"
	config.WorkerID = "go-worker"

	store, err := engine.NewSQLiteStore(config.DBPath)
	if err != nil {
		panic(err)
	}
	metrics := engine.NewMetricsRegistry()
	queue := engine.NewDBTaskQueue(store.DB(), metrics)
	engineSvc := engine.NewWorkflowEngine(store, queue, config, metrics)
	worker := engine.NewWorker(store, queue, config, metrics)
	scheduler := engine.NewTimerScheduler(store, queue, config, metrics)

	worker.RegisterWorkflow("GreetingWorkflow", greetingWorkflow)
	worker.RegisterActivity("compose_greeting", composeGreeting)

	worker.Start()
	scheduler.Start()

	runID, err := engineSvc.StartWorkflow("greeting-workflow-1", "GreetingWorkflow", map[string]interface{}{"name": "Temporal"}, "")
	if err != nil {
		panic(err)
	}
	time.Sleep(2 * time.Second)
	_ = engineSvc.SignalWorkflow("greeting-workflow-1", runID, "approval", map[string]interface{}{"user": "admin@example.com"})

	for {
		exec, _ := store.GetWorkflowExecution("greeting-workflow-1", runID)
		if exec != nil && exec.State == engine.WorkflowStateCompleted {
			fmt.Println("Workflow result:", exec.Result.String)
			break
		}
		time.Sleep(500 * time.Millisecond)
	}
	fmt.Println("Metrics:", metrics.Snapshot())
}
