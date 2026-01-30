package engine

import "testing"

func sampleWorkflow(ctx *WorkflowContext, input map[string]interface{}) (interface{}, error) {
	greeting, err := ctx.ExecuteActivity("compose", map[string]interface{}{"name": input["name"]}, nil)
	if err != nil {
		return nil, err
	}
	_ = ctx.Sleep(1)
	approval, err := ctx.WaitSignal("approve")
	if err != nil {
		return nil, err
	}
	return map[string]interface{}{
		"greeting":    greeting,
		"approved_by": approval["user"],
	}, nil
}

func TestWorkflowReplayCompletes(t *testing.T) {
	history := []HistoryEvent{
		{
			EventID:   1,
			EventType: EventActivityTaskScheduled,
			EventTime: 1,
			Attributes: map[string]interface{}{
				"activity_id":   "activity-1",
				"activity_name": "compose",
				"input":         map[string]interface{}{"name": "Ada"},
			},
		},
		{
			EventID:   2,
			EventType: EventActivityTaskCompleted,
			EventTime: 2,
			Attributes: map[string]interface{}{
				"activity_id": "activity-1",
				"result":      "Hello, Ada",
			},
		},
		{
			EventID:   3,
			EventType: EventTimerScheduled,
			EventTime: 3,
			Attributes: map[string]interface{}{
				"timer_id": "timer-1",
				"fire_at":  10,
			},
		},
		{
			EventID:   4,
			EventType: EventTimerFired,
			EventTime: 4,
			Attributes: map[string]interface{}{
				"timer_id": "timer-1",
			},
		},
		{
			EventID:   5,
			EventType: EventSignalReceived,
			EventTime: 5,
			Attributes: map[string]interface{}{
				"signal_name": "approve",
				"payload":     map[string]interface{}{"user": "bob"},
			},
		},
	}
	runner := NewWorkflowRunner(sampleWorkflow, map[string]interface{}{"name": "Ada"}, history, RetryPolicy{
		InitialIntervalSeconds: 1,
		MaxIntervalSeconds:     10,
		BackoffCoefficient:     2.0,
		MaxAttempts:            3,
	})
	result := runner.Run()
	if result.Status != "COMPLETED" {
		t.Fatalf("expected completed got %s", result.Status)
	}
	output := result.Result.(map[string]interface{})
	if output["greeting"].(string) != "Hello, Ada" {
		t.Fatalf("unexpected greeting")
	}
	if output["approved_by"].(string) != "bob" {
		t.Fatalf("unexpected approval")
	}
}
