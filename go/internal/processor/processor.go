package processor

import (
	"errors"
)

var ErrRetryable = errors.New("retryable processor error")
var ErrDeclined = errors.New("processor declined")

type Client struct{}

func (c Client) Authorize(amount int, currency, paymentMethodToken string) (string, error) {
	if amount%13 == 0 {
		return "", ErrRetryable
	}
	if amount%7 == 0 {
		return "", ErrDeclined
	}
	tokenPrefix := paymentMethodToken
	if len(tokenPrefix) > 6 {
		tokenPrefix = tokenPrefix[:6]
	}
	return "proc_ref_" + tokenPrefix, nil
}
