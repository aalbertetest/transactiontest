export type RetryOptions = {
  /**
   * Total attempts including the first try.
   */
  maxAttempts: number;

  /**
   * Initial backoff in milliseconds.
   */
  baseDelayMs: number;

  /**
   * Maximum backoff in milliseconds.
   */
  maxDelayMs: number;

  /**
   * Randomize delays to prevent thundering herd.
   */
  jitter: boolean;

  /**
   * Abort signal for cancellation.
   */
  signal?: AbortSignal;

  /**
   * Whether the error is retryable.
   */
  isRetryable?: (err: unknown) => boolean;
};

function sleep(ms: number, signal?: AbortSignal): Promise<void> {
  return new Promise((resolve, reject) => {
    const t = setTimeout(resolve, ms);
    if (signal) {
      if (signal.aborted) {
        clearTimeout(t);
        reject(new Error("aborted"));
        return;
      }
      signal.addEventListener(
        "abort",
        () => {
          clearTimeout(t);
          reject(new Error("aborted"));
        },
        { once: true }
      );
    }
  });
}

export async function retry<T>(fn: (attempt: number) => Promise<T>, opts: RetryOptions): Promise<T> {
  const isRetryable = opts.isRetryable ?? (() => true);

  let attempt = 1;
  let delay = opts.baseDelayMs;

  // NOTE: do not swallow last error; always throw.
  for (;;) {
    try {
      return await fn(attempt);
    } catch (err) {
      const canRetry = attempt < opts.maxAttempts && isRetryable(err);
      if (!canRetry) {
        throw err;
      }

      const jitterFactor = opts.jitter ? 0.5 + Math.random() : 1;
      const sleepMs = Math.min(opts.maxDelayMs, Math.floor(delay * jitterFactor));
      await sleep(sleepMs, opts.signal);

      delay = Math.min(opts.maxDelayMs, delay * 2);
      attempt += 1;
    }
  }
}

