// =============================================================================
// NEXUS PLATFORM - API GATEWAY - CONFIGURATION
// =============================================================================
// Configuration management with environment variable support and validation.
// =============================================================================

package config

import (
	"fmt"
	"os"
	"time"

	"github.com/kelseyhightower/envconfig"
	"gopkg.in/yaml.v3"
)

// Config holds all configuration for the API Gateway.
type Config struct {
	// Environment is the deployment environment (development, staging, production)
	Environment string `envconfig:"NEXUS_ENVIRONMENT" default:"development"`

	// Debug enables debug mode
	Debug bool `envconfig:"NEXUS_DEBUG" default:"false"`

	// ServiceName is the name of this service
	ServiceName string `envconfig:"NEXUS_SERVICE_NAME" default:"api-gateway"`

	// ServiceVersion is the version of this service
	ServiceVersion string `envconfig:"NEXUS_SERVICE_VERSION" default:"1.0.0"`

	// InstanceID is the unique identifier for this instance
	InstanceID string `envconfig:"HOSTNAME" default:""`

	// Server configuration
	Server ServerConfig `envconfig:"SERVER"`

	// Auth configuration
	Auth AuthConfig `envconfig:"AUTH"`

	// RateLimit configuration
	RateLimit RateLimitConfig `envconfig:"RATE_LIMIT"`

	// CircuitBreaker configuration
	CircuitBreaker CircuitBreakerConfig `envconfig:"CIRCUIT_BREAKER"`

	// Retry configuration
	Retry RetryConfig `envconfig:"RETRY"`

	// Backend service configuration
	Backend BackendConfig `envconfig:"BACKEND"`

	// Cache configuration
	Cache CacheConfig `envconfig:"CACHE"`

	// Logging configuration
	Logging LoggingConfig `envconfig:"LOG"`

	// Metrics configuration
	Metrics MetricsConfig `envconfig:"METRICS"`

	// Tracing configuration
	Tracing TracingConfig `envconfig:"TRACING"`
}

// ServerConfig holds HTTP server configuration.
type ServerConfig struct {
	Host                    string `envconfig:"HOST" default:"0.0.0.0"`
	Port                    int    `envconfig:"PORT" default:"8080"`
	RequestTimeout          int    `envconfig:"REQUEST_TIMEOUT" default:"30"`
	KeepaliveTimeout        int    `envconfig:"KEEPALIVE_TIMEOUT" default:"65"`
	GracefulShutdownTimeout int    `envconfig:"GRACEFUL_SHUTDOWN_TIMEOUT" default:"30"`
	MaxRequestSize          int64  `envconfig:"MAX_REQUEST_SIZE" default:"10485760"` // 10MB
	CORSEnabled             bool   `envconfig:"CORS_ENABLED" default:"true"`
	CORSAllowOrigins        string `envconfig:"CORS_ALLOW_ORIGINS" default:"*"`
	CORSAllowMethods        string `envconfig:"CORS_ALLOW_METHODS" default:"GET,POST,PUT,DELETE,PATCH,OPTIONS"`
	CORSAllowHeaders        string `envconfig:"CORS_ALLOW_HEADERS" default:"*"`
	CORSAllowCredentials    bool   `envconfig:"CORS_ALLOW_CREDENTIALS" default:"true"`
	CORSMaxAge              int    `envconfig:"CORS_MAX_AGE" default:"600"`
}

// AuthConfig holds authentication configuration.
type AuthConfig struct {
	JWTSecretKey              string `envconfig:"JWT_SECRET_KEY" default:"CHANGE_ME_IN_PRODUCTION"`
	JWTAlgorithm              string `envconfig:"JWT_ALGORITHM" default:"RS256"`
	JWTPublicKeyPath          string `envconfig:"JWT_PUBLIC_KEY_PATH" default:""`
	JWTPrivateKeyPath         string `envconfig:"JWT_PRIVATE_KEY_PATH" default:""`
	JWTAccessTokenExpireMin   int    `envconfig:"JWT_ACCESS_TOKEN_EXPIRE_MINUTES" default:"15"`
	JWTRefreshTokenExpireDays int    `envconfig:"JWT_REFRESH_TOKEN_EXPIRE_DAYS" default:"7"`
	JWTIssuer                 string `envconfig:"JWT_ISSUER" default:"nexus-platform"`
	JWTAudience               string `envconfig:"JWT_AUDIENCE" default:"nexus-api"`
	APIKeyHeader              string `envconfig:"API_KEY_HEADER" default:"X-API-Key"`
	APIKeyPrefix              string `envconfig:"API_KEY_PREFIX" default:"nxp_"`
}

// RateLimitConfig holds rate limiting configuration.
type RateLimitConfig struct {
	Enabled                 bool   `envconfig:"ENABLED" default:"true"`
	GlobalRequestsPerMinute int    `envconfig:"GLOBAL_REQUESTS_PER_MINUTE" default:"10000"`
	UserRequestsPerMinute   int    `envconfig:"USER_REQUESTS_PER_MINUTE" default:"100"`
	IPRequestsPerMinute     int    `envconfig:"IP_REQUESTS_PER_MINUTE" default:"60"`
	BurstMultiplier         float64 `envconfig:"BURST_MULTIPLIER" default:"2.0"`
	StorageBackend          string `envconfig:"STORAGE_BACKEND" default:"redis"`
	IncludeHeaders          bool   `envconfig:"INCLUDE_HEADERS" default:"true"`
}

// CircuitBreakerConfig holds circuit breaker configuration.
type CircuitBreakerConfig struct {
	Enabled          bool `envconfig:"ENABLED" default:"true"`
	FailureThreshold int  `envconfig:"FAILURE_THRESHOLD" default:"5"`
	SuccessThreshold int  `envconfig:"SUCCESS_THRESHOLD" default:"3"`
	Timeout          int  `envconfig:"TIMEOUT" default:"30"`
	ResetTimeout     int  `envconfig:"RESET_TIMEOUT" default:"60"`
}

// RetryConfig holds retry configuration.
type RetryConfig struct {
	Enabled           bool    `envconfig:"ENABLED" default:"true"`
	MaxAttempts       int     `envconfig:"MAX_ATTEMPTS" default:"3"`
	InitialBackoffMS  int     `envconfig:"INITIAL_BACKOFF_MS" default:"100"`
	MaxBackoffMS      int     `envconfig:"MAX_BACKOFF_MS" default:"10000"`
	BackoffMultiplier float64 `envconfig:"BACKOFF_MULTIPLIER" default:"2.0"`
	Jitter            bool    `envconfig:"JITTER" default:"true"`
}

// BackendConfig holds backend service configuration.
type BackendConfig struct {
	ServiceDiscoveryEnabled bool   `envconfig:"SERVICE_DISCOVERY_ENABLED" default:"true"`
	ServiceDiscoveryType    string `envconfig:"SERVICE_DISCOVERY_TYPE" default:"kubernetes"`
	AuthServiceURL          string `envconfig:"AUTH_SERVICE_URL" default:"http://auth-service:8081"`
	UserServiceURL          string `envconfig:"USER_SERVICE_URL" default:"http://user-service:8082"`
	PaymentServiceURL       string `envconfig:"PAYMENT_SERVICE_URL" default:"http://payment-service:8083"`
	WorkflowServiceURL      string `envconfig:"WORKFLOW_SERVICE_URL" default:"http://workflow-engine:8084"`
	QueueServiceURL         string `envconfig:"QUEUE_SERVICE_URL" default:"http://distributed-queue:8085"`
	StreamingServiceURL     string `envconfig:"STREAMING_SERVICE_URL" default:"http://streaming-platform:8086"`
	CacheServiceURL         string `envconfig:"CACHE_SERVICE_URL" default:"http://cache-layer:8087"`
	WebSocketServiceURL     string `envconfig:"WEBSOCKET_SERVICE_URL" default:"http://websocket-service:8089"`
	SchedulerServiceURL     string `envconfig:"SCHEDULER_SERVICE_URL" default:"http://scheduler-service:8090"`
	WorkerServiceURL        string `envconfig:"WORKER_SERVICE_URL" default:"http://worker-fleet:8091"`
	ConnectTimeout          int    `envconfig:"CONNECT_TIMEOUT" default:"5"`
	ReadTimeout             int    `envconfig:"READ_TIMEOUT" default:"30"`
	WriteTimeout            int    `envconfig:"WRITE_TIMEOUT" default:"30"`
	MaxIdleConns            int    `envconfig:"MAX_IDLE_CONNS" default:"100"`
	MaxIdleConnsPerHost     int    `envconfig:"MAX_IDLE_CONNS_PER_HOST" default:"10"`
}

// CacheConfig holds caching configuration.
type CacheConfig struct {
	Enabled          bool   `envconfig:"ENABLED" default:"true"`
	Backend          string `envconfig:"BACKEND" default:"redis"`
	RedisURL         string `envconfig:"REDIS_URL" default:"redis://redis:6379/0"`
	RedisPrefix      string `envconfig:"REDIS_PREFIX" default:"nexus:gateway:cache:"`
	DefaultTTL       int    `envconfig:"DEFAULT_TTL" default:"300"`
	MaxTTL           int    `envconfig:"MAX_TTL" default:"3600"`
}

// LoggingConfig holds logging configuration.
type LoggingConfig struct {
	Level           string `envconfig:"LEVEL" default:"info"`
	Format          string `envconfig:"FORMAT" default:"json"`
	Output          string `envconfig:"OUTPUT" default:"stdout"`
	LogRequests     bool   `envconfig:"LOG_REQUESTS" default:"true"`
	LogRequestBody  bool   `envconfig:"LOG_REQUEST_BODY" default:"false"`
	LogResponseBody bool   `envconfig:"LOG_RESPONSE_BODY" default:"false"`
}

// MetricsConfig holds metrics configuration.
type MetricsConfig struct {
	Enabled  bool   `envconfig:"ENABLED" default:"true"`
	Endpoint string `envconfig:"ENDPOINT" default:"/metrics"`
	Prefix   string `envconfig:"PREFIX" default:"nexus_gateway"`
}

// TracingConfig holds tracing configuration.
type TracingConfig struct {
	Enabled      bool    `envconfig:"ENABLED" default:"true"`
	ServiceName  string  `envconfig:"SERVICE_NAME" default:"api-gateway"`
	JaegerHost   string  `envconfig:"JAEGER_HOST" default:"jaeger"`
	JaegerPort   int     `envconfig:"JAEGER_PORT" default:"6831"`
	SamplingRate float64 `envconfig:"SAMPLING_RATE" default:"1.0"`
}

// Load loads configuration from environment variables and optional YAML file.
func Load() (*Config, error) {
	var cfg Config

	// Check for config file
	configFile := os.Getenv("CONFIG_FILE")
	if configFile != "" {
		if err := loadFromFile(configFile, &cfg); err != nil {
			return nil, fmt.Errorf("failed to load config file: %w", err)
		}
	}

	// Override with environment variables
	if err := envconfig.Process("", &cfg); err != nil {
		return nil, fmt.Errorf("failed to process environment variables: %w", err)
	}

	// Set instance ID if not provided
	if cfg.InstanceID == "" {
		cfg.InstanceID = fmt.Sprintf("gateway-%d", os.Getpid())
	}

	// Validate configuration
	if err := cfg.Validate(); err != nil {
		return nil, fmt.Errorf("configuration validation failed: %w", err)
	}

	return &cfg, nil
}

// loadFromFile loads configuration from a YAML file.
func loadFromFile(path string, cfg *Config) error {
	data, err := os.ReadFile(path)
	if err != nil {
		return err
	}

	return yaml.Unmarshal(data, cfg)
}

// Validate validates the configuration.
func (c *Config) Validate() error {
	// Validate production settings
	if c.Environment == "production" {
		if c.Auth.JWTSecretKey == "CHANGE_ME_IN_PRODUCTION" {
			return fmt.Errorf("JWT secret key must be changed in production")
		}
		if c.Debug {
			return fmt.Errorf("debug mode must be disabled in production")
		}
	}

	// Validate server configuration
	if c.Server.Port < 1 || c.Server.Port > 65535 {
		return fmt.Errorf("invalid server port: %d", c.Server.Port)
	}

	// Validate timeouts
	if c.Server.RequestTimeout < 1 {
		return fmt.Errorf("request timeout must be at least 1 second")
	}

	return nil
}

// IsDevelopment returns true if running in development mode.
func (c *Config) IsDevelopment() bool {
	return c.Environment == "development"
}

// IsProduction returns true if running in production mode.
func (c *Config) IsProduction() bool {
	return c.Environment == "production"
}

// GetReadTimeout returns the read timeout as a Duration.
func (c *Config) GetReadTimeout() time.Duration {
	return time.Duration(c.Backend.ReadTimeout) * time.Second
}

// GetWriteTimeout returns the write timeout as a Duration.
func (c *Config) GetWriteTimeout() time.Duration {
	return time.Duration(c.Backend.WriteTimeout) * time.Second
}

// GetConnectTimeout returns the connect timeout as a Duration.
func (c *Config) GetConnectTimeout() time.Duration {
	return time.Duration(c.Backend.ConnectTimeout) * time.Second
}
