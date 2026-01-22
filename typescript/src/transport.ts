export type ReplicationOp = "set" | "del" | "expire" | "pub";

export interface ReplicationMessage {
  op: ReplicationOp;
  key?: string;
  value?: unknown;
  expiresAt?: number;
  version?: number;
  channel?: string;
  payload?: unknown;
}

export interface Transport {
  send(peerId: string, message: ReplicationMessage): void;
}

export type ReplicationHandler = (message: ReplicationMessage) => void;

export class InMemoryTransport implements Transport {
  private handlers = new Map<string, ReplicationHandler>();

  register(peerId: string, handler: ReplicationHandler): void {
    this.handlers.set(peerId, handler);
  }

  send(peerId: string, message: ReplicationMessage): void {
    const handler = this.handlers.get(peerId);
    if (handler) {
      handler(message);
    }
  }
}
