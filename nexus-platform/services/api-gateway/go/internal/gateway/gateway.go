// =============================================================================
// NEXUS PLATFORM - API GATEWAY - GATEWAY
// =============================================================================
// Core gateway implementation with router setup and middleware configuration.
// =============================================================================

package gateway

import (
	"context"
	"net/http"
	"strings"
	"time"

	"github.com/go-chi/chi/v5"
	chimiddleware "github.com/go-chi/chi/v5/middleware"
	"github.com/go-chi/cors"
	"github.com/rs/zerolog"

	"github.com/nexus-platform/api-gateway/internal/config"
	"github.com/nexus-platform/api-gateway/internal/middleware"
	"github.com/nexus-platform/api-gateway/internal/proxy"
	"github.com/nexus-platform/api-gateway/internal/service"
)

// Config holds gateway configuration.
type Config struct {
	Config  *config.Config
	Logger  zerolog.Logger
	Version string
}

// Gateway represents the API Gateway instance.
type Gateway struct {
	config          *config.Config
	logger          zerolog.Logger
	version         string
	router          chi.Router
	httpClient      *http.Client
	serviceRegistry *service.Registry
	proxyHandler    *proxy.Handler
	startTime       time.Time
}

// New creates a new Gateway instance.
func New(cfg Config) (*Gateway, error) {
	gw := &Gateway{
		config:  cfg.Config,
		logger:  cfg.Logger,
		version: cfg.Version,
	}

	// Initialize HTTP client for backend requests
	gw.httpClient = &http.Client{
		Timeout: cfg.Config.GetReadTimeout(),
		Transport: &http.Transport{
			MaxIdleConns:        cfg.Config.Backend.MaxIdleConns,
			MaxIdleConnsPerHost: cfg.Config.Backend.MaxIdleConnsPerHost,
			IdleConnTimeout:     90 * time.Second,
		},
	}

	// Initialize service registry
	gw.serviceRegistry = service.NewRegistry(cfg.Config.Backend)

	// Initialize proxy handler
	gw.proxyHandler = proxy.NewHandler(proxy.Config{
		HTTPClient:      gw.httpClient,
		ServiceRegistry: gw.serviceRegistry,
		Logger:          gw.logger,
		Config:          cfg.Config,
	})

	// Setup router
	gw.setupRouter()

	return gw, nil
}

// setupRouter configures the Chi router with all middleware and routes.
func (gw *Gateway) setupRouter() {
	r := chi.NewRouter()

	// ==========================================================================
	// GLOBAL MIDDLEWARE (order matters)
	// ==========================================================================

	// Panic recovery
	r.Use(chimiddleware.Recoverer)

	// Request ID
	r.Use(middleware.RequestID)

	// Real IP extraction
	r.Use(chimiddleware.RealIP)

	// Request logging
	if gw.config.Logging.LogRequests {
		r.Use(middleware.Logger(gw.logger))
	}

	// Metrics collection
	if gw.config.Metrics.Enabled {
		r.Use(middleware.Metrics())
	}

	// CORS
	if gw.config.Server.CORSEnabled {
		r.Use(cors.Handler(cors.Options{
			AllowedOrigins:   strings.Split(gw.config.Server.CORSAllowOrigins, ","),
			AllowedMethods:   strings.Split(gw.config.Server.CORSAllowMethods, ","),
			AllowedHeaders:   strings.Split(gw.config.Server.CORSAllowHeaders, ","),
			AllowCredentials: gw.config.Server.CORSAllowCredentials,
			MaxAge:           gw.config.Server.CORSMaxAge,
		}))
	}

	// Request timeout
	r.Use(chimiddleware.Timeout(time.Duration(gw.config.Server.RequestTimeout) * time.Second))

	// Request size limiter
	r.Use(middleware.RequestSizeLimiter(gw.config.Server.MaxRequestSize))

	// Rate limiting
	if gw.config.RateLimit.Enabled {
		r.Use(middleware.RateLimiter(middleware.RateLimiterConfig{
			RequestsPerMinute: gw.config.RateLimit.IPRequestsPerMinute,
			BurstSize:         int(float64(gw.config.RateLimit.IPRequestsPerMinute) * gw.config.RateLimit.BurstMultiplier),
		}))
	}

	// ==========================================================================
	// HEALTH CHECK ROUTES (unauthenticated)
	// ==========================================================================

	r.Group(func(r chi.Router) {
		r.Get("/", gw.handleRoot)
		r.Get("/health", gw.handleHealth)
		r.Get("/ready", gw.handleReady)
		r.Get("/live", gw.handleLive)
	})

	// Metrics endpoint (unauthenticated but can be restricted)
	if gw.config.Metrics.Enabled {
		r.Get(gw.config.Metrics.Endpoint, gw.handleMetrics)
	}

	// ==========================================================================
	// AUTHENTICATED ROUTES
	// ==========================================================================

	r.Group(func(r chi.Router) {
		// Authentication middleware
		r.Use(middleware.Authentication(middleware.AuthConfig{
			JWTSecretKey:   gw.config.Auth.JWTSecretKey,
			JWTAlgorithm:   gw.config.Auth.JWTAlgorithm,
			JWTIssuer:      gw.config.Auth.JWTIssuer,
			JWTAudience:    gw.config.Auth.JWTAudience,
			APIKeyHeader:   gw.config.Auth.APIKeyHeader,
			APIKeyPrefix:   gw.config.Auth.APIKeyPrefix,
			PublicPaths:    []string{"/auth/login", "/auth/register", "/auth/refresh", "/public"},
			Logger:         gw.logger,
		}))

		// Circuit breaker middleware
		if gw.config.CircuitBreaker.Enabled {
			r.Use(middleware.CircuitBreaker(middleware.CircuitBreakerConfig{
				FailureThreshold: uint32(gw.config.CircuitBreaker.FailureThreshold),
				SuccessThreshold: uint32(gw.config.CircuitBreaker.SuccessThreshold),
				Timeout:          time.Duration(gw.config.CircuitBreaker.Timeout) * time.Second,
				ResetTimeout:     time.Duration(gw.config.CircuitBreaker.ResetTimeout) * time.Second,
			}))
		}

		// Admin routes
		r.Route("/admin", func(r chi.Router) {
			r.Use(middleware.RequireRole("admin"))
			r.Get("/stats", gw.handleAdminStats)
			r.Get("/services", gw.handleAdminServices)
			r.Get("/circuit-breakers", gw.handleAdminCircuitBreakers)
			r.Post("/circuit-breakers/reset", gw.handleAdminResetCircuitBreaker)
			r.Post("/cache/clear", gw.handleAdminClearCache)
		})

		// Service-specific routes
		r.Route("/auth", func(r chi.Router) {
			r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
		})

		r.Route("/users", func(r chi.Router) {
			r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
		})

		r.Route("/payments", func(r chi.Router) {
			r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
		})

		r.Route("/workflows", func(r chi.Router) {
			r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
		})

		r.Route("/queue", func(r chi.Router) {
			r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
		})

		r.Route("/stream", func(r chi.Router) {
			r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
		})

		r.Route("/scheduler", func(r chi.Router) {
			r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
		})

		r.Route("/workers", func(r chi.Router) {
			r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
		})

		// Catch-all proxy
		r.HandleFunc("/*", gw.proxyHandler.ServeHTTP)
	})

	gw.router = r
}

// Start starts the gateway.
func (gw *Gateway) Start() error {
	gw.startTime = time.Now()
	gw.logger.Info().Msg("Gateway started")
	return nil
}

// Stop gracefully stops the gateway.
func (gw *Gateway) Stop(ctx context.Context) error {
	gw.logger.Info().Msg("Stopping gateway")

	// Close HTTP client connections
	gw.httpClient.CloseIdleConnections()

	return nil
}

// Handler returns the HTTP handler.
func (gw *Gateway) Handler() http.Handler {
	return gw.router
}

// Uptime returns the gateway uptime.
func (gw *Gateway) Uptime() time.Duration {
	return time.Since(gw.startTime)
}
