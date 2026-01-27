package logging

import (
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// New constructs a production-grade JSON logger with safe defaults.
//
// Requirements:
// - Never log secrets (tokens/passwords).
// - Always include service/env.
// - Use structured fields for correlation (request_id/trace_id/tenant_id).
func New(service, env, level string) (*zap.Logger, error) {
	lvl := zapcore.InfoLevel
	if err := lvl.Set(level); err != nil {
		return nil, err
	}

	cfg := zap.NewProductionConfig()
	cfg.Level = zap.NewAtomicLevelAt(lvl)
	cfg.EncoderConfig.TimeKey = "ts"
	cfg.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	cfg.InitialFields = map[string]any{
		"service": service,
		"env":     env,
	}

	// IMPORTANT: Zap itself doesn't do deep redaction. We rely on developer discipline
	// + higher-layer request/response logging middleware that explicitly omits secrets.
	return cfg.Build()
}

