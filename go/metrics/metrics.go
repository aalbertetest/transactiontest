package metrics

import "sync"

// Counter is a thread-safe counter metric.
type Counter struct {
	name  string
	value int64
	mu    sync.Mutex
}

func (c *Counter) Inc(amount int64) {
	c.mu.Lock()
	defer c.mu.Unlock()
	c.value += amount
}

func (c *Counter) Value() int64 {
	c.mu.Lock()
	defer c.mu.Unlock()
	return c.value
}

// Gauge is a thread-safe gauge metric.
type Gauge struct {
	name  string
	value float64
	mu    sync.Mutex
}

func (g *Gauge) Set(value float64) {
	g.mu.Lock()
	defer g.mu.Unlock()
	g.value = value
}

func (g *Gauge) Value() float64 {
	g.mu.Lock()
	defer g.mu.Unlock()
	return g.value
}

// Histogram is a thread-safe histogram metric.
type Histogram struct {
	name    string
	buckets []float64
	counts  []int64
	mu      sync.Mutex
}

func NewHistogram(name string, buckets []float64) *Histogram {
	return &Histogram{name: name, buckets: buckets, counts: make([]int64, len(buckets))}
}

func (h *Histogram) Observe(value float64) {
	h.mu.Lock()
	defer h.mu.Unlock()
	for idx, bucket := range h.buckets {
		if value <= bucket {
			h.counts[idx]++
			return
		}
	}
	if len(h.counts) > 0 {
		h.counts[len(h.counts)-1]++
	}
}

// Registry stores metrics in a thread-safe map.
type Registry struct {
	mu         sync.Mutex
	counters   map[string]*Counter
	gauges     map[string]*Gauge
	histograms map[string]*Histogram
}

func NewRegistry() *Registry {
	return &Registry{
		counters:   make(map[string]*Counter),
		gauges:     make(map[string]*Gauge),
		histograms: make(map[string]*Histogram),
	}
}

func (r *Registry) Counter(name string) *Counter {
	r.mu.Lock()
	defer r.mu.Unlock()
	if c, ok := r.counters[name]; ok {
		return c
	}
	c := &Counter{name: name}
	r.counters[name] = c
	return c
}

func (r *Registry) Gauge(name string) *Gauge {
	r.mu.Lock()
	defer r.mu.Unlock()
	if g, ok := r.gauges[name]; ok {
		return g
	}
	g := &Gauge{name: name}
	r.gauges[name] = g
	return g
}

func (r *Registry) Histogram(name string, buckets []float64) *Histogram {
	r.mu.Lock()
	defer r.mu.Unlock()
	if h, ok := r.histograms[name]; ok {
		return h
	}
	h := NewHistogram(name, buckets)
	r.histograms[name] = h
	return h
}
