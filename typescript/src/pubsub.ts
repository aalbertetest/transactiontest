export type Subscriber = (payload: unknown) => void;

export class PubSub {
  private subscribers = new Map<string, Subscriber[]>();

  subscribe(channel: string, handler: Subscriber): () => void {
    const handlers = this.subscribers.get(channel) ?? [];
    handlers.push(handler);
    this.subscribers.set(channel, handlers);
    return () => {
      const current = this.subscribers.get(channel) ?? [];
      this.subscribers.set(
        channel,
        current.filter((h) => h !== handler),
      );
    };
  }

  publish(channel: string, payload: unknown): number {
    const handlers = [...(this.subscribers.get(channel) ?? [])];
    for (const handler of handlers) {
      handler(payload);
    }
    return handlers.length;
  }
}
