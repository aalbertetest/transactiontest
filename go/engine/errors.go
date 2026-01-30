package engine

import "fmt"

// PendingActivity is returned to suspend workflow execution until activity completes.
type PendingActivity struct {
	ActivityID string
}

func (p PendingActivity) Error() string {
	return fmt.Sprintf("pending activity %s", p.ActivityID)
}

// PendingTimer is returned to suspend workflow execution until timer fires.
type PendingTimer struct {
	TimerID string
}

func (p PendingTimer) Error() string {
	return fmt.Sprintf("pending timer %s", p.TimerID)
}

// DeterminismError indicates workflow replay mismatch.
type DeterminismError struct {
	Message string
}

func (d DeterminismError) Error() string {
	return d.Message
}

// WorkflowApplicationError wraps activity/workflow errors.
type WorkflowApplicationError struct {
	Message string
}

func (w WorkflowApplicationError) Error() string {
	return w.Message
}
