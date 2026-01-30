package main

import (
	"fmt"
	"time"

	"example.com/workflowengine/engine"
)

type OrderWorkflow struct{}

func (w OrderWorkflow) Name() string {
	return "order-workflow"
}

func (w OrderWorkflow) InitialState() string {
	return "START"
}

func (w OrderWorkflow) Decide(ctx *engine.WorkflowContext, state string, stateData map[string]interface{}, history []engine.HistoryEvent) engine.DecisionResult {
	commands := []engine.Command{}
	if state == "START" {
		activityID := ctx.EnsureCommandID("activity", "validate_activity_id")
		if ctx.ActivityCompleted(activityID) {
			state = "VALIDATED"
		} else {
			commandID := ctx.EnsureCommandID("cmd", "validate_cmd")
			commands = append(commands, engine.ScheduleActivity(commandID, activityID, "validate_order", ctx.WorkflowInput(), 10, 5, engine.DefaultRetryPolicy()))
			return engine.DecisionResult{NextState: "WAIT_VALIDATE", StateData: stateData, Commands: commands}
		}
	}
	if state == "WAIT_VALIDATE" || state == "VALIDATED" {
		activityID := getString(stateData["validate_activity_id"])
		if activityID != "" && !ctx.ActivityCompleted(activityID) {
			return engine.DecisionResult{NextState: "WAIT_VALIDATE", StateData: stateData}
		}
		state = "CHARGE"
	}
	if state == "CHARGE" {
		activityID := ctx.EnsureCommandID("activity", "charge_activity_id")
		if ctx.ActivityCompleted(activityID) {
			state = "CHARGED"
		} else {
			commandID := ctx.EnsureCommandID("cmd", "charge_cmd")
			input := map[string]interface{}{"amount": ctx.WorkflowInput()["amount"]}
			commands = append(commands, engine.ScheduleActivity(commandID, activityID, "charge_card", input, 10, 5, engine.DefaultRetryPolicy()))
			return engine.DecisionResult{NextState: "WAIT_CHARGE", StateData: stateData, Commands: commands}
		}
	}
	if state == "WAIT_CHARGE" || state == "CHARGED" {
		activityID := getString(stateData["charge_activity_id"])
		if activityID != "" && !ctx.ActivityCompleted(activityID) {
			return engine.DecisionResult{NextState: "WAIT_CHARGE", StateData: stateData}
		}
		state = "SLEEP"
	}
	if state == "SLEEP" {
		timerID := ctx.EnsureCommandID("timer", "receipt_timer_id")
		if ctx.TimerFired(timerID) {
			state = "SEND_RECEIPT"
		} else {
			commandID := ctx.EnsureCommandID("cmd", "sleep_cmd")
			commands = append(commands, engine.ScheduleTimer(commandID, timerID, 1))
			return engine.DecisionResult{NextState: "WAIT_TIMER", StateData: stateData, Commands: commands}
		}
	}
	if state == "WAIT_TIMER" {
		timerID := getString(stateData["receipt_timer_id"])
		if timerID != "" && !ctx.TimerFired(timerID) {
			return engine.DecisionResult{NextState: "WAIT_TIMER", StateData: stateData}
		}
		state = "SEND_RECEIPT"
	}
	if state == "SEND_RECEIPT" {
		activityID := ctx.EnsureCommandID("activity", "receipt_activity_id")
		if ctx.ActivityCompleted(activityID) {
			return engine.DecisionResult{NextState: "DONE", StateData: stateData, Complete: true}
		}
		commandID := ctx.EnsureCommandID("cmd", "receipt_cmd")
		input := map[string]interface{}{"email": ctx.WorkflowInput()["email"]}
		commands = append(commands, engine.ScheduleActivity(commandID, activityID, "send_receipt", input, 10, 5, engine.DefaultRetryPolicy()))
		return engine.DecisionResult{NextState: "WAIT_RECEIPT", StateData: stateData, Commands: commands}
	}
	if state == "WAIT_RECEIPT" {
		activityID := getString(stateData["receipt_activity_id"])
		if activityID != "" && !ctx.ActivityCompleted(activityID) {
			return engine.DecisionResult{NextState: "WAIT_RECEIPT", StateData: stateData}
		}
		return engine.DecisionResult{NextState: "DONE", StateData: stateData, Complete: true}
	}
	return engine.DecisionResult{NextState: state, StateData: stateData}
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

func validateOrder(ctx *engine.ActivityContext, input map[string]interface{}) (map[string]interface{}, error) {
	ctx.Heartbeat()
	return map[string]interface{}{"valid": true, "order_id": input["order_id"]}, nil
}

func chargeCard(ctx *engine.ActivityContext, input map[string]interface{}) (map[string]interface{}, error) {
	ctx.Heartbeat()
	return map[string]interface{}{"charged": true, "amount": input["amount"]}, nil
}

func sendReceipt(ctx *engine.ActivityContext, input map[string]interface{}) (map[string]interface{}, error) {
	ctx.Heartbeat()
	return map[string]interface{}{"sent": true, "email": input["email"]}, nil
}

func main() {
	config := engine.DefaultConfig()
	config.DBPath = "example_engine.sqlite"
	eng, err := engine.NewWorkflowEngine(config)
	if err != nil {
		panic(err)
	}
	eng.RegisterWorkflow(OrderWorkflow{})
	eng.RegisterActivity("validate_order", validateOrder, nil, nil, nil)
	eng.RegisterActivity("charge_card", chargeCard, nil, nil, nil)
	eng.RegisterActivity("send_receipt", sendReceipt, nil, nil, nil)

	scheduler := engine.NewScheduler(eng)
	workflowWorker := engine.NewWorkflowWorker(eng)
	activityWorker := engine.NewActivityWorker(eng, 2)
	timerWorker := engine.NewTimerWorker(eng)

	scheduler.Start()
	workflowWorker.Start()
	activityWorker.Start()
	timerWorker.Start()

	runID, err := eng.StartWorkflow("order-workflow", "order-123", map[string]interface{}{
		"order_id": "order-123",
		"amount":   25,
		"email":    "user@example.com",
	}, nil)
	if err != nil {
		panic(err)
	}
	fmt.Println("Started run", runID)

	for {
		run, err := eng.Persistence.GetRun(runID)
		if err == nil && run["status"] == "COMPLETED" {
			fmt.Println("Workflow completed")
			break
		}
		if err == nil && run["status"] == "FAILED" {
			fmt.Println("Workflow failed")
			break
		}
		time.Sleep(500 * time.Millisecond)
	}

	scheduler.Stop()
	workflowWorker.Stop()
	activityWorker.Stop()
	timerWorker.Stop()
}
