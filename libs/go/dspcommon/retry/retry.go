package retry

import (
	"context"
	"time"

	"github.com/cenkalti/backoff/v4"
)

type Options struct {
	MaxElapsedTime time.Duration
	InitialInterval time.Duration
	MaxInterval     time.Duration
}

func Do[T any](ctx context.Context, opts Options, fn func() (T, error), isRetryable func(error) bool) (T, error) {
	var zero T
	b := backoff.NewExponentialBackOff()
	b.InitialInterval = opts.InitialInterval
	b.MaxInterval = opts.MaxInterval
	b.MaxElapsedTime = opts.MaxElapsedTime

	op := func() error {
		v, err := fn()
		if err == nil {
			zero = v
			return nil
		}
		if isRetryable != nil && !isRetryable(err) {
			return backoff.Permanent(err)
		}
		return err
	}

	if err := backoff.Retry(op, backoff.WithContext(b, ctx)); err != nil {
		var out T
		return out, err
	}
	return zero, nil
}

