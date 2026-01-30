package engine

import "fmt"

// ValidateTransition ensures workflow state transitions are valid.
func ValidateTransition(current WorkflowState, target WorkflowState) error {
	allowed := map[WorkflowState]map[WorkflowState]bool{
		StateCreated: {
			StateRunning:   true,
			StateCanceled:  true,
			StateTerminated: true,
		},
		StateRunning: {
			StateCompleted: true,
			StateFailed:    true,
			StateTimedOut:  true,
			StateCanceled:  true,
			StateTerminated: true,
		},
		StateCompleted: {},
		StateFailed:    {},
		StateTimedOut:  {},
		StateCanceled:  {},
		StateTerminated: {},
	}
	if targets, ok := allowed[current]; ok {
		if targets[target] {
			return nil
		}
	}
	return fmt.Errorf("invalid workflow transition %s -> %s", current, target)
}
