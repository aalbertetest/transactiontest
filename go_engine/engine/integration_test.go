package engine

import (
	"os"
	"testing"
	"time"
)

type TimerWorkflow struct{}

func (w TimerWorkflow) Name() string {
	return "timer-workflow"
}

func (w TimerWorkflow) InitialState() string {
	return "START"
}

func (w TimerWorkflow) Decide(ctx *WorkflowContext, state string, stateData map[string]interface{}, history []HistoryEvent) DecisionResult {
	if state == "START" {
		timerID := ctx.EnsureCommandID("timer", "timer_id")
		if ctx.TimerFired(timerID) {
			return DecisionResult{NextState: "TIMER_DONE", StateData: stateData}
		}
		commandID := ctx.EnsureCommandID("cmd", "timer_cmd")
		return DecisionResult{
			NextState: "WAIT_TIMER",
			StateData: stateData,
			Commands:  []Command{ScheduleTimer(commandID, timerID, 1)},
		}
	}
	if state == "WAIT_TIMER" {
		timerID := getString(stateData["timer_id"])
		if timerID != "" && ctx.TimerFired(timerID) {
			return DecisionResult{NextState: "TIMER_DONE", StateData: stateData}
		}
		return DecisionResult{NextState: "WAIT_TIMER", StateData: stateData}
	}
	if state == "TIMER_DONE" {
		activityID := ctx.EnsureCommandID("activity", "activity_id")
		if ctx.ActivityCompleted(activityID) {
			return DecisionResult{NextState: "DONE", StateData: stateData, Complete: true}
		}
		commandID := ctx.EnsureCommandID("cmd", "activity_cmd")
		return DecisionResult{
			NextState: "WAIT_ACTIVITY",
			StateData: stateData,
			Commands: []Command{
				ScheduleActivity(commandID, activityID, "step", map[string]interface{}{"value": "integration"}, 5, 2, DefaultRetryPolicy()),
			},
		}
	}
	if state == "WAIT_ACTIVITY" {
		activityID := getString(stateData["activity_id"])
		if activityID != "" && ctx.ActivityCompleted(activityID) {
			return DecisionResult{NextState: "DONE", StateData: stateData, Complete: true}
		}
		return DecisionResult{NextState: "WAIT_ACTIVITY", StateData: stateData}
	}
	return DecisionResult{NextState: state, StateData: stateData}
}

func stepActivity(ctx *ActivityContext, input map[string]interface{}) (map[string]interface{}, error) {
	ctx.Heartbeat()
	return map[string]interface{}{"value": input["value"]}, nil
}

func TestTimerWorkflowIntegration(t *testing.T) {
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
	eng.RegisterWorkflow(TimerWorkflow{})
	eng.RegisterActivity("step", stepActivity, nil, nil, nil)

	scheduler := NewScheduler(eng)
	workflowWorker := NewWorkflowWorker(eng)
	activityWorker := NewActivityWorker(eng, 1)
	timerWorker := NewTimerWorker(eng)
	scheduler.Start()
	workflowWorker.Start()
	activityWorker.Start()
	timerWorker.Start()

	runID, err := eng.StartWorkflow("timer-workflow", "wf-integration", map[string]interface{}{"input": "x"}, nil)
	if err != nil {
		t.Fatal(err)
	}
	deadline := time.Now().Add(10 * time.Second)
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
	timerWorker.Stop()

	if status != "COMPLETED" {
		t.Fatalf("expected COMPLETED, got %s", status)
	}
}
