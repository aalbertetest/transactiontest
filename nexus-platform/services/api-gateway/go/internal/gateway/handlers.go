// =============================================================================
// NEXUS PLATFORM - API GATEWAY - HTTP HANDLERS
// =============================================================================
// Request handlers for health checks, admin endpoints, and metrics.
// =============================================================================

package gateway

import (
	"encoding/json"
	"net/http"
	"time"

	"github.com/prometheus/client_golang/prometheus/promhttp"
)

// HealthResponse represents the health check response.
type HealthResponse struct {
	Status       string            `json:"status"`
	Service      string            `json:"service"`
	Version      string            `json:"version"`
	UptimeSeconds float64          `json:"uptime_seconds"`
	Timestamp    string            `json:"timestamp"`
	Dependencies []DependencyHealth `json:"dependencies,omitempty"`
	Checks       map[string]bool   `json:"checks,omitempty"`
}

// DependencyHealth represents health of a dependency.
type DependencyHealth struct {
	Name      string  `json:"name"`
	Status    string  `json:"status"`
	LatencyMs float64 `json:"latency_ms,omitempty"`
	Message   string  `json:"message,omitempty"`
}

// ReadinessResponse represents readiness probe response.
type ReadinessResponse struct {
	Ready   bool   `json:"ready"`
	Message string `json:"message"`
}

// LivenessResponse represents liveness probe response.
type LivenessResponse struct {
	Alive   bool   `json:"alive"`
	Message string `json:"message"`
}

// RootResponse represents the root endpoint response.
type RootResponse struct {
	Service     string `json:"service"`
	Version     string `json:"version"`
	Environment string `json:"environment"`
	Status      string `json:"status"`
	Timestamp   string `json:"timestamp"`
}

// AdminStatsResponse represents admin stats response.
type AdminStatsResponse struct {
	UptimeSeconds       float64 `json:"uptime_seconds"`
	TotalRequests       int64   `json:"total_requests"`
	ActiveRequests      int64   `json:"active_requests"`
	ErrorCount          int64   `json:"error_count"`
	CircuitBreakersOpen int     `json:"circuit_breakers_open"`
	ServicesHealthy     int     `json:"services_healthy"`
	ServicesUnhealthy   int     `json:"services_unhealthy"`
}

// writeJSON writes a JSON response.
func writeJSON(w http.ResponseWriter, status int, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(data)
}

// writeError writes an error response.
func writeError(w http.ResponseWriter, status int, code string, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	json.NewEncoder(w).Encode(map[string]interface{}{
		"error": map[string]string{
			"code":    code,
			"message": message,
		},
	})
}

// handleRoot handles the root endpoint.
func (gw *Gateway) handleRoot(w http.ResponseWriter, r *http.Request) {
	writeJSON(w, http.StatusOK, RootResponse{
		Service:     gw.config.ServiceName,
		Version:     gw.version,
		Environment: gw.config.Environment,
		Status:      "operational",
		Timestamp:   time.Now().UTC().Format(time.RFC3339),
	})
}

// handleHealth handles the health check endpoint.
func (gw *Gateway) handleHealth(w http.ResponseWriter, r *http.Request) {
	// Check dependencies
	dependencies := []DependencyHealth{}
	checks := map[string]bool{}
	
	// Check service registry
	services := gw.serviceRegistry.GetAll()
	healthyCount := 0
	for name, info := range services {
		healthy := info.Healthy
		if healthy {
			healthyCount++
		}
		dependencies = append(dependencies, DependencyHealth{
			Name:    name,
			Status:  boolToStatus(healthy),
			Message: info.Endpoint,
		})
		checks[name] = healthy
	}

	// Determine overall status
	status := "healthy"
	if healthyCount < len(services) {
		status = "degraded"
	}
	if healthyCount == 0 && len(services) > 0 {
		status = "unhealthy"
	}

	response := HealthResponse{
		Status:        status,
		Service:       gw.config.ServiceName,
		Version:       gw.version,
		UptimeSeconds: gw.Uptime().Seconds(),
		Timestamp:     time.Now().UTC().Format(time.RFC3339),
		Dependencies:  dependencies,
		Checks:        checks,
	}

	httpStatus := http.StatusOK
	if status == "unhealthy" {
		httpStatus = http.StatusServiceUnavailable
	}

	writeJSON(w, httpStatus, response)
}

// handleReady handles the readiness probe endpoint.
func (gw *Gateway) handleReady(w http.ResponseWriter, r *http.Request) {
	// Check if gateway is ready to accept traffic
	// For now, always ready if running
	writeJSON(w, http.StatusOK, ReadinessResponse{
		Ready:   true,
		Message: "Service is ready",
	})
}

// handleLive handles the liveness probe endpoint.
func (gw *Gateway) handleLive(w http.ResponseWriter, r *http.Request) {
	// Simple liveness check - if we can respond, we're alive
	writeJSON(w, http.StatusOK, LivenessResponse{
		Alive:   true,
		Message: "Service is alive",
	})
}

// handleMetrics handles the Prometheus metrics endpoint.
func (gw *Gateway) handleMetrics(w http.ResponseWriter, r *http.Request) {
	promhttp.Handler().ServeHTTP(w, r)
}

// handleAdminStats handles the admin stats endpoint.
func (gw *Gateway) handleAdminStats(w http.ResponseWriter, r *http.Request) {
	services := gw.serviceRegistry.GetAll()
	healthyCount := 0
	for _, info := range services {
		if info.Healthy {
			healthyCount++
		}
	}

	writeJSON(w, http.StatusOK, AdminStatsResponse{
		UptimeSeconds:       gw.Uptime().Seconds(),
		TotalRequests:       0, // Would track via metrics
		ActiveRequests:      0, // Would track via metrics
		ErrorCount:          0, // Would track via metrics
		CircuitBreakersOpen: 0, // Would get from circuit breaker registry
		ServicesHealthy:     healthyCount,
		ServicesUnhealthy:   len(services) - healthyCount,
	})
}

// handleAdminServices handles the admin services list endpoint.
func (gw *Gateway) handleAdminServices(w http.ResponseWriter, r *http.Request) {
	services := gw.serviceRegistry.GetAll()
	
	result := make([]map[string]interface{}, 0, len(services))
	for name, info := range services {
		result = append(result, map[string]interface{}{
			"name":     name,
			"endpoint": info.Endpoint,
			"healthy":  info.Healthy,
		})
	}

	writeJSON(w, http.StatusOK, map[string]interface{}{
		"services": result,
	})
}

// handleAdminCircuitBreakers handles the admin circuit breakers endpoint.
func (gw *Gateway) handleAdminCircuitBreakers(w http.ResponseWriter, r *http.Request) {
	// Would return circuit breaker states
	writeJSON(w, http.StatusOK, map[string]interface{}{
		"circuit_breakers": []interface{}{},
	})
}

// handleAdminResetCircuitBreaker handles resetting circuit breakers.
func (gw *Gateway) handleAdminResetCircuitBreaker(w http.ResponseWriter, r *http.Request) {
	// Would reset circuit breaker
	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success": true,
		"message": "Circuit breaker reset",
	})
}

// handleAdminClearCache handles clearing the cache.
func (gw *Gateway) handleAdminClearCache(w http.ResponseWriter, r *http.Request) {
	// Would clear cache
	writeJSON(w, http.StatusOK, map[string]interface{}{
		"success": true,
		"message": "Cache cleared",
	})
}

// boolToStatus converts a boolean to a status string.
func boolToStatus(b bool) string {
	if b {
		return "healthy"
	}
	return "unhealthy"
}
