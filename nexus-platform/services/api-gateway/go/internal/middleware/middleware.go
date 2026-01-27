// =============================================================================
// NEXUS PLATFORM - API GATEWAY - MIDDLEWARE
// =============================================================================
// HTTP middleware implementations for request processing.
// =============================================================================

package middleware

import (
	"context"
	"fmt"
	"net/http"
	"strings"
	"time"

	"github.com/go-chi/httprate"
	"github.com/golang-jwt/jwt/v5"
	"github.com/google/uuid"
	"github.com/rs/zerolog"
	"github.com/sony/gobreaker"
)

// ContextKey is a type for context keys.
type ContextKey string

const (
	// RequestIDKey is the context key for request ID.
	RequestIDKey ContextKey = "request_id"
	// CorrelationIDKey is the context key for correlation ID.
	CorrelationIDKey ContextKey = "correlation_id"
	// UserKey is the context key for authenticated user.
	UserKey ContextKey = "user"
	// StartTimeKey is the context key for request start time.
	StartTimeKey ContextKey = "start_time"
)

// User represents an authenticated user.
type User struct {
	ID          string   `json:"id"`
	Email       string   `json:"email"`
	Roles       []string `json:"roles"`
	Permissions []string `json:"permissions"`
	TenantID    string   `json:"tenant_id,omitempty"`
	TokenType   string   `json:"token_type"`
}

// RequestID middleware generates a unique request ID for each request.
func RequestID(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Check for existing request ID
		requestID := r.Header.Get("X-Request-ID")
		if requestID == "" {
			requestID = fmt.Sprintf("req_%s", uuid.New().String())
		}

		// Check for correlation ID
		correlationID := r.Header.Get("X-Correlation-ID")
		if correlationID == "" {
			correlationID = requestID
		}

		// Add to context
		ctx := context.WithValue(r.Context(), RequestIDKey, requestID)
		ctx = context.WithValue(ctx, CorrelationIDKey, correlationID)
		ctx = context.WithValue(ctx, StartTimeKey, time.Now())

		// Add to response headers
		w.Header().Set("X-Request-ID", requestID)
		w.Header().Set("X-Correlation-ID", correlationID)

		next.ServeHTTP(w, r.WithContext(ctx))
	})
}

// Logger middleware logs HTTP requests.
func Logger(log zerolog.Logger) func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Get request ID
			requestID, _ := r.Context().Value(RequestIDKey).(string)
			startTime, _ := r.Context().Value(StartTimeKey).(time.Time)
			if startTime.IsZero() {
				startTime = time.Now()
			}

			// Create response wrapper to capture status
			ww := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

			// Process request
			next.ServeHTTP(ww, r)

			// Calculate duration
			duration := time.Since(startTime)

			// Log request
			log.Info().
				Str("request_id", requestID).
				Str("method", r.Method).
				Str("path", r.URL.Path).
				Int("status", ww.statusCode).
				Dur("duration", duration).
				Str("client_ip", r.RemoteAddr).
				Str("user_agent", r.UserAgent()).
				Msg("HTTP request")
		})
	}
}

// responseWriter wraps http.ResponseWriter to capture status code.
type responseWriter struct {
	http.ResponseWriter
	statusCode int
}

func (rw *responseWriter) WriteHeader(code int) {
	rw.statusCode = code
	rw.ResponseWriter.WriteHeader(code)
}

// RequestSizeLimiter middleware limits request body size.
func RequestSizeLimiter(maxSize int64) func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			r.Body = http.MaxBytesReader(w, r.Body, maxSize)
			next.ServeHTTP(w, r)
		})
	}
}

// RateLimiterConfig holds rate limiter configuration.
type RateLimiterConfig struct {
	RequestsPerMinute int
	BurstSize         int
}

// RateLimiter middleware implements rate limiting.
func RateLimiter(cfg RateLimiterConfig) func(next http.Handler) http.Handler {
	return httprate.LimitByIP(cfg.RequestsPerMinute, time.Minute)
}

// AuthConfig holds authentication middleware configuration.
type AuthConfig struct {
	JWTSecretKey   string
	JWTAlgorithm   string
	JWTIssuer      string
	JWTAudience    string
	APIKeyHeader   string
	APIKeyPrefix   string
	PublicPaths    []string
	Logger         zerolog.Logger
}

// Authentication middleware handles JWT and API key authentication.
func Authentication(cfg AuthConfig) func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			// Check if path is public
			for _, path := range cfg.PublicPaths {
				if strings.HasPrefix(r.URL.Path, path) {
					next.ServeHTTP(w, r)
					return
				}
			}

			// Skip health endpoints
			if r.URL.Path == "/health" || r.URL.Path == "/ready" || r.URL.Path == "/live" || r.URL.Path == "/metrics" || r.URL.Path == "/" {
				next.ServeHTTP(w, r)
				return
			}

			var user *User

			// Try JWT authentication
			authHeader := r.Header.Get("Authorization")
			if strings.HasPrefix(authHeader, "Bearer ") {
				tokenString := strings.TrimPrefix(authHeader, "Bearer ")
				
				// Parse token
				token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
					// Validate algorithm
					if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
						return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
					}
					return []byte(cfg.JWTSecretKey), nil
				})

				if err != nil {
					http.Error(w, `{"error":{"code":"INVALID_TOKEN","message":"Invalid or expired token"}}`, http.StatusUnauthorized)
					return
				}

				if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
					user = &User{
						ID:        fmt.Sprintf("%v", claims["sub"]),
						Email:     fmt.Sprintf("%v", claims["email"]),
						TokenType: "jwt",
					}
					
					if roles, ok := claims["roles"].([]interface{}); ok {
						for _, role := range roles {
							user.Roles = append(user.Roles, fmt.Sprintf("%v", role))
						}
					}
				}
			}

			// Try API key authentication
			if user == nil {
				apiKey := r.Header.Get(cfg.APIKeyHeader)
				if apiKey != "" && strings.HasPrefix(apiKey, cfg.APIKeyPrefix) {
					// In production, validate API key against database
					// For now, accept any key with correct prefix
					user = &User{
						ID:        "api_key_user",
						TokenType: "api_key",
						Roles:     []string{"api"},
					}
				}
			}

			// If no authentication provided
			if user == nil {
				http.Error(w, `{"error":{"code":"AUTHENTICATION_REQUIRED","message":"Authentication required"}}`, http.StatusUnauthorized)
				return
			}

			// Add user to context
			ctx := context.WithValue(r.Context(), UserKey, user)
			next.ServeHTTP(w, r.WithContext(ctx))
		})
	}
}

// RequireRole middleware requires a specific role.
func RequireRole(role string) func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			user, ok := r.Context().Value(UserKey).(*User)
			if !ok || user == nil {
				http.Error(w, `{"error":{"code":"UNAUTHORIZED","message":"Unauthorized"}}`, http.StatusUnauthorized)
				return
			}

			// Check role
			hasRole := false
			for _, r := range user.Roles {
				if r == role {
					hasRole = true
					break
				}
			}

			if !hasRole {
				http.Error(w, `{"error":{"code":"FORBIDDEN","message":"Insufficient permissions"}}`, http.StatusForbidden)
				return
			}

			next.ServeHTTP(w, r)
		})
	}
}

// CircuitBreakerConfig holds circuit breaker configuration.
type CircuitBreakerConfig struct {
	FailureThreshold uint32
	SuccessThreshold uint32
	Timeout          time.Duration
	ResetTimeout     time.Duration
}

// CircuitBreaker middleware implements the circuit breaker pattern.
func CircuitBreaker(cfg CircuitBreakerConfig) func(next http.Handler) http.Handler {
	settings := gobreaker.Settings{
		Name:        "api-gateway",
		MaxRequests: cfg.SuccessThreshold,
		Interval:    cfg.ResetTimeout,
		Timeout:     cfg.Timeout,
		ReadyToTrip: func(counts gobreaker.Counts) bool {
			return counts.ConsecutiveFailures >= cfg.FailureThreshold
		},
	}

	cb := gobreaker.NewCircuitBreaker(settings)

	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			_, err := cb.Execute(func() (interface{}, error) {
				// Create response wrapper
				ww := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}
				next.ServeHTTP(ww, r)

				// Consider 5xx as failures
				if ww.statusCode >= 500 {
					return nil, fmt.Errorf("server error: %d", ww.statusCode)
				}

				return nil, nil
			})

			if err != nil {
				if err == gobreaker.ErrOpenState || err == gobreaker.ErrTooManyRequests {
					http.Error(w, `{"error":{"code":"SERVICE_UNAVAILABLE","message":"Service temporarily unavailable"}}`, http.StatusServiceUnavailable)
					return
				}
			}
		})
	}
}

// Metrics middleware collects request metrics.
func Metrics() func(next http.Handler) http.Handler {
	return func(next http.Handler) http.Handler {
		return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
			startTime := time.Now()
			ww := &responseWriter{ResponseWriter: w, statusCode: http.StatusOK}

			next.ServeHTTP(ww, r)

			duration := time.Since(startTime)

			// Record metrics (using prometheus client)
			recordRequestMetrics(r.Method, r.URL.Path, ww.statusCode, duration)
		})
	}
}

// recordRequestMetrics records request metrics to Prometheus.
func recordRequestMetrics(method, path string, status int, duration time.Duration) {
	// This would use prometheus client to record metrics
	// For now, this is a placeholder
}

// GetRequestID returns the request ID from context.
func GetRequestID(ctx context.Context) string {
	if id, ok := ctx.Value(RequestIDKey).(string); ok {
		return id
	}
	return ""
}

// GetUser returns the authenticated user from context.
func GetUser(ctx context.Context) *User {
	if user, ok := ctx.Value(UserKey).(*User); ok {
		return user
	}
	return nil
}
