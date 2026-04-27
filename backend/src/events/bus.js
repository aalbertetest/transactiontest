import crypto from 'node:crypto';

/**
 * Tiny in-process event bus. Async listeners are awaited in parallel; errors
 * in one listener don't abort the others. Each emit gets a unique eventId so
 * downstream consumers can build idempotency keys.
 *
 * For production multi-node, swap this for a transactional outbox + broker.
 */
export class EventBus {
  constructor() {
    this.listeners = new Map();
  }

  on(event, fn) {
    if (!this.listeners.has(event)) this.listeners.set(event, []);
    this.listeners.get(event).push(fn);
  }

  async emit(event, payload) {
    const eventId = crypto.randomUUID();
    const fns = this.listeners.get(event) ?? [];
    const results = await Promise.allSettled(
      fns.map((fn) => fn({ ...payload, eventId })),
    );
    for (const r of results) {
      if (r.status === 'rejected') {
        // Listener failures are isolated. In prod this is a metric + log.
        console.error(`[bus] listener for ${event} failed:`, r.reason);
      }
    }
    return eventId;
  }
}
