package engine

import "sync"

type Counter struct {
	values map[string]float64
	mu     sync.Mutex
}

func (c *Counter) Inc(label string, v float64) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.values[label] = c.values[label] + v
}

func (c *Counter) Snapshot() map[string]float64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	out := make(map[string]float64, len(c.values))
	for k, v := range c.values {
		out[k] = v
	}
	return out
}

type Histogram struct {
	counts map[string]int
	sums   map[string]float64
	mu     sync.Mutex
}

func (h *Histogram) Observe(label string, v float64) {
	h.mu.Lock()
	defer h.mu.Unlock()
	h.counts[label] = h.counts[label] + 1
	h.sums[label] = h.sums[label] + v
}

func (h *Histogram) Snapshot() map[string]map[string]float64 {
	h.mu.Lock()
	defer h.mu.Unlock()
	out := make(map[string]map[string]float64, len(h.counts))
	for k, count := range h.counts {
		out[k] = map[string]float64{
			"count": float64(count),
			"sum":   h.sums[k],
		}
	}
	return out
}

type MetricsRegistry struct {
	counters   map[string]*Counter
	histograms map[string]*Histogram
	mu         sync.Mutex
}

func NewMetricsRegistry() *MetricsRegistry {
	return &MetricsRegistry{
		counters:   map[string]*Counter{},
		histograms: map[string]*Histogram{},
	}
}

func (m *MetricsRegistry) Counter(name string) *Counter {
	m.mu.Lock()
	defer m.mu.Unlock()
	if _, ok := m.counters[name]; !ok {
		m.counters[name] = &Counter{values: map[string]float64{}}
	}
	return m.counters[name]
}

func (m *MetricsRegistry) Histogram(name string) *Histogram {
	m.mu.Lock()
	defer m.mu.Unlock()
	if _, ok := m.histograms[name]; !ok {
		m.histograms[name] = &Histogram{
			counts: map[string]int{},
			sums:   map[string]float64{},
		}
	}
	return m.histograms[name]
}

func (m *MetricsRegistry) Snapshot() map[string]interface{} {
	m.mu.Lock()
	defer m.mu.Unlock()
	out := map[string]interface{}{}
	counterSnapshot := map[string]map[string]float64{}
	for name, counter := range m.counters {
		counterSnapshot[name] = counter.Snapshot()
	}
	histSnapshot := map[string]map[string]map[string]float64{}
	for name, hist := range m.histograms {
		histSnapshot[name] = hist.Snapshot()
	}
	out["counters"] = counterSnapshot
	out["histograms"] = histSnapshot
	return out
}
