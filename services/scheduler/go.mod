module github.com/cursor/platform/services/scheduler

go 1.23.0

toolchain go1.24.12

replace github.com/cursor/platform/lib/go => ../../lib/go

require (
	github.com/cursor/platform/lib/go v0.0.0-00010101000000-000000000000
	github.com/robfig/cron/v3 v3.0.1
	go.uber.org/zap v1.27.1
)

require go.uber.org/multierr v1.10.0 // indirect
