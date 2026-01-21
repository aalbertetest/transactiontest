package scheduler

// WorkflowSpec describes a versioned workflow definition.
// Steps are a DAG; each step may depend on zero or more prior steps.
type WorkflowSpec struct {
	Steps []WorkflowStep `json:"steps"`
}

// WorkflowStep describes a unit of work.
type WorkflowStep struct {
	ID        string                 `json:"id"`
	Type      string                 `json:"type"`
	Params    map[string]interface{} `json:"params"`
	DependsOn []string               `json:"depends_on"`
}
