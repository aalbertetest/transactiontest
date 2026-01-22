export const withRetries = async <T>(
  operation: () => Promise<T> | T,
  maxAttempts: number,
  baseBackoffMs: number,
  isRetryable: (error: unknown) => boolean
): Promise<T> => {
  let lastError: unknown;
  for (let attempt = 1; attempt <= maxAttempts; attempt += 1) {
    try {
      return await operation();
    } catch (error) {
      lastError = error;
      if (!isRetryable(error) || attempt === maxAttempts) {
        break;
      }
      const sleepMs = baseBackoffMs * 2 ** (attempt - 1);
      const jitter = Math.floor(Math.random() * baseBackoffMs * 0.2);
      await new Promise((resolve) => setTimeout(resolve, sleepMs + jitter));
    }
  }
  throw lastError;
};
