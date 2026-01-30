package engine

import "time"

type TimeoutManager struct {
	OnTaskTimeout      func(taskID string)
	OnHeartbeatTimeout func(taskID string)
	OnRunTimeout       func(runID string)
}

func (t *TimeoutManager) Sweep(taskTimeoutIDs []string, heartbeatTimeoutIDs []string, runTimeoutIDs []string) {
	for _, id := range taskTimeoutIDs {
		t.OnTaskTimeout(id)
	}
	for _, id := range heartbeatTimeoutIDs {
		t.OnHeartbeatTimeout(id)
	}
	for _, id := range runTimeoutIDs {
		t.OnRunTimeout(id)
	}
}

func NowSeconds() float64 {
	return float64(time.Now().UnixNano()) / 1e9
}
