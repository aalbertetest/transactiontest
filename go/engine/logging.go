package engine

import (
	"log"
	"os"
	"strings"
	"time"
)

// Logger provides leveled logging with a fixed format.
type Logger struct {
	level  string
	logger *log.Logger
}

func NewLogger(level string) *Logger {
	return &Logger{
		level:  strings.ToUpper(level),
		logger: log.New(os.Stdout, "", 0),
	}
}

func (l *Logger) Infof(format string, args ...interface{}) {
	if l.allows("INFO") {
		l.printf("INFO", format, args...)
	}
}

func (l *Logger) Warnf(format string, args ...interface{}) {
	if l.allows("WARN") {
		l.printf("WARN", format, args...)
	}
}

func (l *Logger) Errorf(format string, args ...interface{}) {
	if l.allows("ERROR") {
		l.printf("ERROR", format, args...)
	}
}

func (l *Logger) allows(level string) bool {
	levels := map[string]int{"DEBUG": 1, "INFO": 2, "WARN": 3, "ERROR": 4}
	current := levels[l.level]
	if current == 0 {
		current = 2
	}
	return levels[level] >= current
}

func (l *Logger) printf(level, format string, args ...interface{}) {
	timestamp := time.Now().UTC().Format("2006-01-02T15:04:05Z")
	l.logger.Printf(timestamp+" "+level+" "+format, args...)
}
