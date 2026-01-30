package engine

import (
	"os"
	"testing"
	"time"
)

type SimpleWorkflow struct{}

func (w SimpleWorkflow) Name() string {
	return "simple-workflow"
}

func (w SimpleWorkflow) InitialState() string {
	return "START"
}

func (w SimpleWorkflow) Decide(ctx *WorkflowContext, state string, stateData map[string]interface{}, history []HistoryEvent) DecisionResult {
	if state == "START" {
		activityID := ctx.EnsureCommandID("activity", "hello_activity_id")
		if ctx.ActivityCompleted(activityID) {
			return DecisionResult{NextState: "DONE", StateData: stateData, Complete: true}
		}
		commandID := ctx.EnsureCommandID("cmd", "hello_cmd")
		return DecisionResult{
			NextState: "WAIT_ACTIVITY",
			StateData: stateData,
			Commands: []Command{
				ScheduleActivity(commandID, activityID, "hello", map[string]interface{}{"name": "unit"}, 5, 2, DefaultRetryPolicy()),
			},
		}
	}
	if state == "WAIT_ACTIVITY" {
		activityID := getString(stateData["hello_activity_id"])
		if activityID != "" && ctx.ActivityCompleted(activityID) {
			return DecisionResult{NextState: "DONE", StateData: stateData, Complete: true}
		}
		return DecisionResult{NextState: "WAIT_ACTIVITY", StateData: stateData}
	}
	return DecisionResult{NextState: state, StateData: stateData}
}

func helloActivity(ctx *ActivityContext, input map[string]interface{}) (map[string]interface{}, error) {
	ctx.Heartbeat()
	return map[string]interface{}{"message": "hello"}, nil
}

func TestWorkflowCompletes(t *testing.T) {
	tmp, err := os.CreateTemp("", "engine-*.sqlite")
	if err != nil {
		t.Fatal(err)
	}
	defer os.Remove(tmp.Name())
	_ = tmp.Close()

	cfg := DefaultConfig()
	cfg.DBPath = tmp.Name()
	cfg.WorkerPollInterval = 50 * time.Millisecond
	eng, err := NewWorkflowEngine(cfg)
	if err != nil {
		t.Fatal(err)
	}
	eng.RegisterWorkflow(SimpleWorkflow{})
	eng.RegisterActivity("hello", helloActivity, nil, nil, nil)

	scheduler := NewScheduler(eng)
	workflowWorker := NewWorkflowWorker(eng)
	activityWorker := NewActivityWorker(eng, 1)
	scheduler.Start()
	workflowWorker.Start()
	activityWorker.Start()

	runID, err := eng.StartWorkflow("simple-workflow", "wf-unit", map[string]interface{}{"input": "x"}, nil)
	if err != nil {
		t.Fatal(err)
	}
	deadline := time.Now().Add(5 * time.Second)
	status := ""
	for time.Now().Before(deadline) {
		run, err := eng.Persistence.GetRun(runID)
		if err == nil {
			if run["status"] == "COMPLETED" || run["status"] == "FAILED" {
				status = run["status"].(string)
				break
			}
		}
		time.Sleep(100 * time.Millisecond)
	}

	scheduler.Stop()
	workflowWorker.Stop()
	activityWorker.Stop()

	if status != "COMPLETED" {
		t.Fatalf("expected COMPLETED, got %s", status)
	}
}

func getString(value interface{}) string {
	if value == nil {
		return ""
	}
	if v, ok := value.(string); ok {
		return v
	}
	return ""
}
