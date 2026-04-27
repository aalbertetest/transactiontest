import { renderTemplate } from './templates.js';

const DEFAULT_MAX_ATTEMPTS = 6;
const DEFAULT_BACKOFF_MS = (n) => Math.min(60_000, 2 ** n * 1000);

export class NotificationWorker {
  constructor({ repo, transports, maxAttempts, backoffMs, now }) {
    this.repo = repo;
    this.transports = transports;
    this.maxAttempts = maxAttempts ?? DEFAULT_MAX_ATTEMPTS;
    this.backoffMs = backoffMs ?? DEFAULT_BACKOFF_MS;
    this.now = now ?? (() => Date.now());
    this._timer = null;
  }

  async tick(batchSize = 20) {
    const batch = this.repo.claimDue(batchSize, this.now());
    await Promise.all(batch.map((n) => this._handle(n)));
    return batch.length;
  }

  start({ intervalMs = 1000 } = {}) {
    if (this._timer) return;
    const loop = async () => {
      try {
        await this.tick();
      } catch (e) {
        console.error('[notify-worker] tick failed:', e);
      }
      this._timer = setTimeout(loop, intervalMs);
    };
    this._timer = setTimeout(loop, intervalMs);
  }

  stop() {
    if (this._timer) clearTimeout(this._timer);
    this._timer = null;
  }

  async _handle(n) {
    const transport = this.transports[n.channel];
    if (!transport) {
      this.repo.deadLetter(n.id, `unknown_channel:${n.channel}`);
      return;
    }
    try {
      const message = renderTemplate(n.template, n.payload);
      await transport.send({ to: n.payload.recipient, message });
      this.repo.markSent(n.id);
    } catch (err) {
      const attempts = n.attempts + 1;
      if (attempts >= this.maxAttempts) {
        this.repo.deadLetter(n.id, String(err?.message ?? err));
      } else {
        this.repo.reschedule(
          n.id,
          this.now() + this.backoffMs(attempts),
          attempts,
          String(err?.message ?? err),
        );
      }
    }
  }
}
