package engine

import (
	"sync"
	"time"
)

// MetricsRegistry is a lightweight in-process metrics registry.
type MetricsRegistry struct {
	mu         sync.Mutex
	counters   map[string]int64
	gauges     map[string]float64
	histograms map[string][]float64
}

func NewMetricsRegistry() *MetricsRegistry {
	return &MetricsRegistry{
		counters:   make(map[string]int64),
		gauges:     make(map[string]float64),
		histograms: make(map[string][]float64),
	}
}

func (m *MetricsRegistry) Inc(name string, delta int64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.counters[name] += delta
}

func (m *MetricsRegistry) SetGauge(name string, value float64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.gauges[name] = value
}

func (m *MetricsRegistry) Observe(name string, value float64) {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.histograms[name] = append(m.histograms[name], value)
}

func (m *MetricsRegistry) Snapshot() map[string]interface{} {
	m.mu.Lock()
	defer m.mu.Unlock()

	histograms := make(map[string]map[string]float64)
	for name, values := range m.histograms {
		if len(values) == 0 {
			histograms[name] = map[string]float64{"count": 0, "min": 0, "max": 0, "avg": 0}
			continue
		}
		min := values[0]
		max := values[0]
		sum := 0.0
		for _, v := range values {
			if v < min {
				min = v
			}
			if v > max {
				max = v
			}
			sum += v
		}
		histograms[name] = map[string]float64{
			"count": float64(len(values)),
			"min":   min,
			"max":   max,
			"avg":   sum / float64(len(values)),
		}
	}

	return map[string]interface{}{
		"timestamp":  time.Now().Unix(),
		"counters":   m.counters,
		"gauges":     m.gauges,
		"histograms": histograms,
	}
}
