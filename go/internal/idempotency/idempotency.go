package idempotency

import (
	"crypto/sha256"
	"encoding/hex"
)

func HashRequest(path string, body []byte) string {
	hash := sha256.Sum256(append([]byte(path+":"), body...))
	return hex.EncodeToString(hash[:])
}
