package engine

import (
	"log"
	"os"
)

type Logger struct {
	*log.Logger
}

func NewLogger(prefix string) *Logger {
	return &Logger{Logger: log.New(os.Stdout, prefix+" ", log.LstdFlags|log.Lmicroseconds)}
}
