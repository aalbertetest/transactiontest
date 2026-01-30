package logging

import (
	"log"
	"os"
	"strings"
)

// Logger wraps the standard logger with level filtering.
type Logger struct {
	level string
	std   *log.Logger
}

// New returns a logger with the given level.
func New(level string) *Logger {
	return &Logger{
		level: strings.ToUpper(level),
		std:   log.New(os.Stdout, "", log.LstdFlags),
	}
}

func (l *Logger) enabled(level string) bool {
	levels := map[string]int{
		"DEBUG": 1,
		"INFO":  2,
		"WARN":  3,
		"ERROR": 4,
	}
	threshold, ok := levels[l.level]
	if !ok {
		threshold = levels["INFO"]
	}
	value, ok := levels[level]
	if !ok {
		value = levels["INFO"]
	}
	return value >= threshold
}

func (l *Logger) Debug(msg string, args ...any) {
	if l.enabled("DEBUG") {
		l.std.Printf("DEBUG "+msg, args...)
	}
}

func (l *Logger) Info(msg string, args ...any) {
	if l.enabled("INFO") {
		l.std.Printf("INFO "+msg, args...)
	}
}

func (l *Logger) Warn(msg string, args ...any) {
	if l.enabled("WARN") {
		l.std.Printf("WARN "+msg, args...)
	}
}

func (l *Logger) Error(msg string, args ...any) {
	if l.enabled("ERROR") {
		l.std.Printf("ERROR "+msg, args...)
	}
}
