package engine

import "github.com/google/uuid"

// NewUUID returns a random UUID string.
func NewUUID() string {
	return uuid.NewString()
}
