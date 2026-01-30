package main

import (
	"os"
	"time"

	"workflowengine/engine"
)

func greetingWorkflow(ctx *engine.WorkflowContext, input map[string]interface{}) (interface{}, error) {
	version, err := ctx.GetVersion("greeting-change", 1, 2)
	if err != nil {
		return nil, err
	}
	name := "world"
	if raw, ok := input["name"].(string); ok {
		name = raw
	}
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
	config := engine.LoadConfigFromEnv()
	if path := os.Getenv("WF_CONFIG_FILE"); path != "" {
		if loaded, err := engine.LoadConfigFromFile(path); err == nil {
			config = loaded
		}
	}
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

	if os.Getenv("WF_RUN_EXAMPLE") == "1" {
		runID, err := engineSvc.StartWorkflow("greeting-workflow-1", "GreetingWorkflow", map[string]interface{}{"name": "Temporal"}, "")
		if err != nil {
			panic(err)
		}
		time.Sleep(2 * time.Second)
		_ = engineSvc.SignalWorkflow("greeting-workflow-1", runID, "approval", map[string]interface{}{"user": "admin@example.com"})
		for {
			exec, _ := store.GetWorkflowExecution("greeting-workflow-1", runID)
			if exec != nil && exec.State == engine.WorkflowStateCompleted {
				break
			}
			time.Sleep(500 * time.Millisecond)
		}
	}

	select {}
}
