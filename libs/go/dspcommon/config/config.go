package config

import (
	"fmt"
	"os"
	"strings"
)

// BaseConfig is the cross-service configuration contract.
//
// IMPORTANT: env var names are shared across languages to keep deployments uniform.
type BaseConfig struct {
	Env         string // DSP_ENV (dev/staging/prod)
	ServiceName string // DSP_SERVICE_NAME
	LogLevel    string // DSP_LOG_LEVEL
	HTTPAddr    string // DSP_HTTP_ADDR
	MetricsAddr string // DSP_METRICS_ADDR
}

func LoadBaseFromEnv() (BaseConfig, error) {
	cfg := BaseConfig{
		Env:         strings.TrimSpace(getenv("DSP_ENV", "dev")),
		ServiceName: strings.TrimSpace(os.Getenv("DSP_SERVICE_NAME")),
		LogLevel:    strings.TrimSpace(getenv("DSP_LOG_LEVEL", "info")),
		HTTPAddr:    strings.TrimSpace(getenv("DSP_HTTP_ADDR", "0.0.0.0:8080")),
		MetricsAddr: strings.TrimSpace(getenv("DSP_METRICS_ADDR", "0.0.0.0:9091")),
	}

	if cfg.Env != "dev" && cfg.Env != "staging" && cfg.Env != "prod" {
		return BaseConfig{}, fmt.Errorf("invalid DSP_ENV: %q", cfg.Env)
	}
	if cfg.ServiceName == "" {
		return BaseConfig{}, fmt.Errorf("DSP_SERVICE_NAME is required")
	}
	switch cfg.LogLevel {
	case "debug", "info", "warn", "error":
	default:
		return BaseConfig{}, fmt.Errorf("invalid DSP_LOG_LEVEL: %q", cfg.LogLevel)
	}
	return cfg, nil
}

func getenv(k, def string) string {
	v := strings.TrimSpace(os.Getenv(k))
	if v == "" {
		return def
	}
	return v
}

