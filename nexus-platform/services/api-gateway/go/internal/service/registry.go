// =============================================================================
// NEXUS PLATFORM - API GATEWAY - SERVICE REGISTRY
// =============================================================================
// Service discovery and registry for backend services.
// =============================================================================

package service

import (
	"sync"
	"time"

	"github.com/nexus-platform/api-gateway/internal/config"
)

// Info holds information about a registered service.
type Info struct {
	Name       string
	Endpoint   string
	Healthy    bool
	LastCheck  time.Time
	LastUpdate time.Time
}

// Registry is a service registry for backend services.
type Registry struct {
	config   config.BackendConfig
	services map[string]*Info
	mu       sync.RWMutex
}

// NewRegistry creates a new service registry.
func NewRegistry(cfg config.BackendConfig) *Registry {
	r := &Registry{
		config:   cfg,
		services: make(map[string]*Info),
	}

	// Register static services from configuration
	r.registerStaticServices()

	return r
}

// registerStaticServices registers services from static configuration.
func (r *Registry) registerStaticServices() {
	r.mu.Lock()
	defer r.mu.Unlock()

	now := time.Now()

	// Register each service from configuration
	services := map[string]string{
		"auth-service":       r.config.AuthServiceURL,
		"user-service":       r.config.UserServiceURL,
		"payment-service":    r.config.PaymentServiceURL,
		"workflow-engine":    r.config.WorkflowServiceURL,
		"distributed-queue":  r.config.QueueServiceURL,
		"streaming-platform": r.config.StreamingServiceURL,
		"cache-layer":        r.config.CacheServiceURL,
		"websocket-service":  r.config.WebSocketServiceURL,
		"scheduler-service":  r.config.SchedulerServiceURL,
		"worker-fleet":       r.config.WorkerServiceURL,
	}

	for name, endpoint := range services {
		if endpoint != "" {
			r.services[name] = &Info{
				Name:       name,
				Endpoint:   endpoint,
				Healthy:    true, // Assume healthy until proven otherwise
				LastUpdate: now,
			}
		}
	}
}

// Register registers a service endpoint.
func (r *Registry) Register(name, endpoint string) {
	r.mu.Lock()
	defer r.mu.Unlock()

	r.services[name] = &Info{
		Name:       name,
		Endpoint:   endpoint,
		Healthy:    true,
		LastUpdate: time.Now(),
	}
}

// Deregister removes a service from the registry.
func (r *Registry) Deregister(name string) {
	r.mu.Lock()
	defer r.mu.Unlock()

	delete(r.services, name)
}

// GetEndpoint returns the endpoint for a service.
func (r *Registry) GetEndpoint(name string) string {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if info, ok := r.services[name]; ok && info.Healthy {
		return info.Endpoint
	}
	return ""
}

// GetInfo returns the service info.
func (r *Registry) GetInfo(name string) *Info {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if info, ok := r.services[name]; ok {
		// Return a copy
		return &Info{
			Name:       info.Name,
			Endpoint:   info.Endpoint,
			Healthy:    info.Healthy,
			LastCheck:  info.LastCheck,
			LastUpdate: info.LastUpdate,
		}
	}
	return nil
}

// GetAll returns all registered services.
func (r *Registry) GetAll() map[string]*Info {
	r.mu.RLock()
	defer r.mu.RUnlock()

	result := make(map[string]*Info, len(r.services))
	for name, info := range r.services {
		result[name] = &Info{
			Name:       info.Name,
			Endpoint:   info.Endpoint,
			Healthy:    info.Healthy,
			LastCheck:  info.LastCheck,
			LastUpdate: info.LastUpdate,
		}
	}
	return result
}

// SetHealthy sets the health status of a service.
func (r *Registry) SetHealthy(name string, healthy bool) {
	r.mu.Lock()
	defer r.mu.Unlock()

	if info, ok := r.services[name]; ok {
		info.Healthy = healthy
		info.LastCheck = time.Now()
	}
}

// HealthyEndpoints returns all healthy endpoints for a service.
func (r *Registry) HealthyEndpoints(name string) []string {
	r.mu.RLock()
	defer r.mu.RUnlock()

	var endpoints []string
	if info, ok := r.services[name]; ok && info.Healthy {
		endpoints = append(endpoints, info.Endpoint)
	}
	return endpoints
}

// Count returns the number of registered services.
func (r *Registry) Count() int {
	r.mu.RLock()
	defer r.mu.RUnlock()

	return len(r.services)
}

// HealthyCount returns the number of healthy services.
func (r *Registry) HealthyCount() int {
	r.mu.RLock()
	defer r.mu.RUnlock()

	count := 0
	for _, info := range r.services {
		if info.Healthy {
			count++
		}
	}
	return count
}
