export const config = {
  apiKey: process.env.API_KEY ?? "test_key_123",
  webhookSigningSecret: process.env.WEBHOOK_SIGNING_SECRET ?? "whsec_test_123",
  maxRetryAttempts: Number(process.env.MAX_RETRY_ATTEMPTS ?? "5"),
  baseBackoffMs: Number(process.env.BASE_BACKOFF_MS ?? "200"),
  workerPollIntervalMs: Number(process.env.WORKER_POLL_INTERVAL_MS ?? "500"),
  apiPort: Number(process.env.API_PORT ?? "8081")
};
