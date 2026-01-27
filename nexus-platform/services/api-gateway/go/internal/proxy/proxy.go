// =============================================================================
// NEXUS PLATFORM - API GATEWAY - REVERSE PROXY
// =============================================================================
// Reverse proxy implementation for routing requests to backend services.
// =============================================================================

package proxy

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"strings"
	"time"

	"github.com/rs/zerolog"

	"github.com/nexus-platform/api-gateway/internal/config"
	"github.com/nexus-platform/api-gateway/internal/middleware"
	"github.com/nexus-platform/api-gateway/internal/service"
)

// Config holds proxy configuration.
type Config struct {
	HTTPClient      *http.Client
	ServiceRegistry *service.Registry
	Logger          zerolog.Logger
	Config          *config.Config
}

// Handler is the reverse proxy handler.
type Handler struct {
	httpClient      *http.Client
	serviceRegistry *service.Registry
	logger          zerolog.Logger
	config          *config.Config
}

// ServiceRoutes maps URL prefixes to backend services.
var ServiceRoutes = map[string]string{
	"/auth":      "auth-service",
	"/users":     "user-service",
	"/payments":  "payment-service",
	"/workflows": "workflow-engine",
	"/queue":     "distributed-queue",
	"/stream":    "streaming-platform",
	"/cache":     "cache-layer",
	"/scheduler": "scheduler-service",
	"/workers":   "worker-fleet",
}

// ForwardHeaders are headers to forward from client to backend.
var ForwardHeaders = map[string]bool{
	"accept":           true,
	"accept-encoding":  true,
	"accept-language":  true,
	"content-type":     true,
	"content-length":   true,
	"user-agent":       true,
	"x-request-id":     true,
	"x-correlation-id": true,
	"x-forwarded-for":  true,
	"x-forwarded-proto": true,
	"x-real-ip":        true,
	"authorization":    true,
}

// ExcludedHeaders are hop-by-hop headers to exclude.
var ExcludedHeaders = map[string]bool{
	"connection":       true,
	"keep-alive":       true,
	"transfer-encoding": true,
	"te":               true,
	"trailer":          true,
	"upgrade":          true,
	"host":             true,
}

// NewHandler creates a new proxy handler.
func NewHandler(cfg Config) *Handler {
	return &Handler{
		httpClient:      cfg.HTTPClient,
		serviceRegistry: cfg.ServiceRegistry,
		logger:          cfg.Logger,
		config:          cfg.Config,
	}
}

// ServeHTTP handles proxy requests.
func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	ctx := r.Context()
	requestID := middleware.GetRequestID(ctx)

	// Determine target service
	serviceName := h.getTargetService(r.URL.Path)
	if serviceName == "" {
		h.writeError(w, http.StatusNotFound, "NOT_FOUND", "No service found for path")
		return
	}

	// Get service endpoint
	endpoint := h.serviceRegistry.GetEndpoint(serviceName)
	if endpoint == "" {
		h.logger.Error().
			Str("request_id", requestID).
			Str("service", serviceName).
			Msg("Service endpoint not found")
		h.writeError(w, http.StatusServiceUnavailable, "SERVICE_UNAVAILABLE", fmt.Sprintf("Service '%s' not available", serviceName))
		return
	}

	// Transform path
	targetPath := h.transformPath(r.URL.Path, serviceName)

	// Build target URL
	targetURL := endpoint + targetPath
	if r.URL.RawQuery != "" {
		targetURL = targetURL + "?" + r.URL.RawQuery
	}

	// Create proxy request
	proxyReq, err := http.NewRequestWithContext(ctx, r.Method, targetURL, r.Body)
	if err != nil {
		h.logger.Error().
			Err(err).
			Str("request_id", requestID).
			Msg("Failed to create proxy request")
		h.writeError(w, http.StatusInternalServerError, "INTERNAL_ERROR", "Failed to create proxy request")
		return
	}

	// Copy headers
	h.copyHeaders(proxyReq, r)

	// Add gateway headers
	h.addGatewayHeaders(proxyReq, r)

	// Log proxy request
	h.logger.Debug().
		Str("request_id", requestID).
		Str("service", serviceName).
		Str("method", r.Method).
		Str("target_url", targetURL).
		Msg("Proxying request")

	startTime := time.Now()

	// Execute request
	resp, err := h.httpClient.Do(proxyReq)
	if err != nil {
		duration := time.Since(startTime)
		h.logger.Error().
			Err(err).
			Str("request_id", requestID).
			Str("service", serviceName).
			Dur("duration", duration).
			Msg("Upstream request failed")
		h.writeError(w, http.StatusBadGateway, "BAD_GATEWAY", "Failed to connect to upstream service")
		return
	}
	defer resp.Body.Close()

	duration := time.Since(startTime)

	h.logger.Debug().
		Str("request_id", requestID).
		Str("service", serviceName).
		Int("status", resp.StatusCode).
		Dur("duration", duration).
		Msg("Upstream response received")

	// Copy response headers
	h.copyResponseHeaders(w, resp)

	// Add gateway response headers
	w.Header().Set("X-Gateway-Request-Id", requestID)
	w.Header().Set("X-Upstream-Service", serviceName)
	w.Header().Set("X-Upstream-Duration-Ms", fmt.Sprintf("%.2f", float64(duration.Microseconds())/1000))

	// Write status code
	w.WriteHeader(resp.StatusCode)

	// Copy response body
	io.Copy(w, resp.Body)
}

// getTargetService determines the target service based on path.
func (h *Handler) getTargetService(path string) string {
	for prefix, service := range ServiceRoutes {
		if strings.HasPrefix(path, prefix) {
			return service
		}
	}
	return ""
}

// transformPath transforms the request path for the backend.
func (h *Handler) transformPath(path string, serviceName string) string {
	for prefix, svc := range ServiceRoutes {
		if svc == serviceName && strings.HasPrefix(path, prefix) {
			// Remove the prefix
			transformed := strings.TrimPrefix(path, prefix)
			if transformed == "" {
				transformed = "/"
			}
			return transformed
		}
	}
	return path
}

// copyHeaders copies headers from the original request to the proxy request.
func (h *Handler) copyHeaders(proxyReq *http.Request, r *http.Request) {
	for key, values := range r.Header {
		keyLower := strings.ToLower(key)
		if ExcludedHeaders[keyLower] {
			continue
		}
		if ForwardHeaders[keyLower] {
			for _, value := range values {
				proxyReq.Header.Add(key, value)
			}
		}
	}
}

// addGatewayHeaders adds gateway-specific headers to the request.
func (h *Handler) addGatewayHeaders(proxyReq *http.Request, r *http.Request) {
	ctx := r.Context()
	requestID := middleware.GetRequestID(ctx)

	proxyReq.Header.Set("X-Gateway-Request-Id", requestID)

	// Add user info if authenticated
	if user := middleware.GetUser(ctx); user != nil {
		proxyReq.Header.Set("X-User-Id", user.ID)
		if user.TenantID != "" {
			proxyReq.Header.Set("X-Tenant-Id", user.TenantID)
		}
		if len(user.Roles) > 0 {
			proxyReq.Header.Set("X-User-Roles", strings.Join(user.Roles, ","))
		}
	}

	// Add forwarding headers
	if xff := r.Header.Get("X-Forwarded-For"); xff != "" {
		proxyReq.Header.Set("X-Forwarded-For", xff)
	} else if r.RemoteAddr != "" {
		proxyReq.Header.Set("X-Forwarded-For", strings.Split(r.RemoteAddr, ":")[0])
	}

	proxyReq.Header.Set("X-Forwarded-Proto", h.getScheme(r))
	proxyReq.Header.Set("X-Forwarded-Host", r.Host)
}

// getScheme returns the request scheme.
func (h *Handler) getScheme(r *http.Request) string {
	if r.TLS != nil {
		return "https"
	}
	if proto := r.Header.Get("X-Forwarded-Proto"); proto != "" {
		return proto
	}
	return "http"
}

// copyResponseHeaders copies headers from the upstream response.
func (h *Handler) copyResponseHeaders(w http.ResponseWriter, resp *http.Response) {
	for key, values := range resp.Header {
		keyLower := strings.ToLower(key)
		if ExcludedHeaders[keyLower] {
			continue
		}
		for _, value := range values {
			w.Header().Add(key, value)
		}
	}
}

// writeError writes an error response.
func (h *Handler) writeError(w http.ResponseWriter, status int, code, message string) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	fmt.Fprintf(w, `{"error":{"code":"%s","message":"%s"}}`, code, message)
}
