package engine

import "encoding/json"

type RetryPolicy struct {
	InitialIntervalSeconds float64 `json:"initial_interval_seconds"`
	BackoffCoefficient     float64 `json:"backoff_coefficient"`
	MaxIntervalSeconds     float64 `json:"max_interval_seconds"`
	MaxAttempts            int     `json:"max_attempts"`
}

func DefaultRetryPolicy() RetryPolicy {
	return RetryPolicy{
		InitialIntervalSeconds: 1.0,
		BackoffCoefficient:     2.0,
		MaxIntervalSeconds:     60.0,
		MaxAttempts:            5,
	}
}

type HistoryEvent struct {
	EventID   int64
	RunID     string
	EventType string
	Timestamp float64
	Attributes map[string]interface{}
}

type Task struct {
	TaskID                  string
	RunID                   string
	TaskType                string
	QueueName               string
	Status                  string
	ScheduledAt             float64
	LeasedUntil             *float64
	CompletedAt             *float64
	Attempt                 int
	MaxAttempts             int
	Payload                 map[string]interface{}
	LastHeartbeatAt         *float64
	HeartbeatTimeoutSeconds *int
	TimeoutAt               *float64
	LastError               *string
}

func decodeJSON(data string) map[string]interface{} {
	if data == "" {
		return map[string]interface{}{}
	}
	var out map[string]interface{}
	_ = json.Unmarshal([]byte(data), &out)
	if out == nil {
		out = map[string]interface{}{}
	}
	return out
}
