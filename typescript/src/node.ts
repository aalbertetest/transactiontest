import { Persistence } from "./persistence";
import { PubSub } from "./pubsub";
import { Replicator } from "./replication";
import { Store } from "./storage";
import { InMemoryTransport, ReplicationMessage, Transport } from "./transport";

export type NodeOptions = {
  capacity?: number;
  clock?: () => number;
  transport?: Transport;
  persistence?: Persistence;
};

export class Node {
  readonly id: string;
  private store: Store;
  private pubsub = new PubSub();
  private replicator: Replicator;
  private persistence?: Persistence;
  private version = 0;
  private clock: () => number;

  constructor(id: string, options: NodeOptions = {}) {
    this.id = id;
    this.clock = options.clock ?? (() => Date.now());
    this.store = new Store(options.capacity ?? 1024, undefined, this.clock);
    this.persistence = options.persistence;
    this.replicator = new Replicator(options.transport);
    if (options.transport instanceof InMemoryTransport) {
      options.transport.register(this.id, (message) => this.applyReplication(message));
    }
  }

  load(): void {
    if (this.persistence) {
      this.persistence.load(this.store);
      this.syncVersion();
    }
  }

  get(key: string): unknown | undefined {
    return this.store.get(key);
  }

  set(key: string, value: unknown, ttlMs?: number, replicaIds: string[] = []): number {
    const version = this.nextVersion();
    const result = this.store.set(key, value, ttlMs, version);
    const entry = this.store.getEntry(key);
    if (this.persistence && entry) {
      this.persistence.appendSet(key, value, entry.expiresAt, result.version);
    }
    this.replicate(replicaIds, {
      op: "set",
      key,
      value,
      expiresAt: entry?.expiresAt,
      version: result.version,
    });
    this.recordEvictions(result.evicted, replicaIds);
    return result.version;
  }

  delete(key: string, replicaIds: string[] = []): boolean {
    const ok = this.store.delete(key);
    if (!ok) {
      return false;
    }
    const version = this.nextVersion();
    if (this.persistence) {
      this.persistence.appendDelete(key, version);
    }
    this.replicate(replicaIds, { op: "del", key, version });
    return true;
  }

  expire(key: string, ttlMs: number, replicaIds: string[] = []): boolean {
    const version = this.nextVersion();
    const ok = this.store.expire(key, ttlMs, version);
    if (!ok) {
      return false;
    }
    const entry = this.store.getEntry(key);
    if (this.persistence && entry?.expiresAt !== undefined) {
      this.persistence.appendExpire(key, entry.expiresAt, version);
    }
    this.replicate(replicaIds, {
      op: "expire",
      key,
      expiresAt: entry?.expiresAt,
      version,
    });
    return true;
  }

  publish(channel: string, payload: unknown, replicaIds: string[] = []): number {
    const delivered = this.pubsub.publish(channel, payload);
    this.replicate(replicaIds, { op: "pub", channel, payload });
    return delivered;
  }

  subscribe(channel: string, handler: (payload: unknown) => void): () => void {
    return this.pubsub.subscribe(channel, handler);
  }

  sweepExpired(): void {
    this.store.sweepExpired();
  }

  snapshot(): void {
    if (this.persistence) {
      this.persistence.snapshot(this.store);
    }
  }

  applyReplication(message: ReplicationMessage): void {
    if (message.op === "set") {
      if (!message.key || this.shouldSkip(message.key, message.version)) {
        return;
      }
      const ttlMs =
        message.expiresAt !== undefined ? Math.max(message.expiresAt - this.clock(), 0) : undefined;
      this.store.set(message.key, message.value, ttlMs, message.version);
      this.bumpVersion(message.version);
    } else if (message.op === "del") {
      if (!message.key || this.shouldSkip(message.key, message.version)) {
        return;
      }
      this.store.delete(message.key);
      this.bumpVersion(message.version);
    } else if (message.op === "expire") {
      if (!message.key || message.expiresAt === undefined) {
        return;
      }
      if (this.shouldSkip(message.key, message.version)) {
        return;
      }
      const ttlMs = Math.max(message.expiresAt - this.clock(), 0);
      this.store.expire(message.key, ttlMs, message.version);
      this.bumpVersion(message.version);
    } else if (message.op === "pub") {
      if (!message.channel) {
        return;
      }
      this.pubsub.publish(message.channel, message.payload);
    }
  }

  private shouldSkip(key: string, incoming?: number): boolean {
    if (incoming === undefined) {
      return false;
    }
    const entry = this.store.getEntry(key);
    return entry !== undefined && incoming <= entry.version;
  }

  private replicate(replicaIds: string[], message: ReplicationMessage): void {
    if (replicaIds.length === 0) {
      return;
    }
    this.replicator.replicate(replicaIds, message);
  }

  private recordEvictions(evicted: string[], replicaIds: string[]): void {
    for (const key of evicted) {
      const version = this.nextVersion();
      if (this.persistence) {
        this.persistence.appendDelete(key, version);
      }
      this.replicate(replicaIds, { op: "del", key, version });
    }
  }

  private nextVersion(): number {
    this.version += 1;
    return this.version;
  }

  private bumpVersion(incoming?: number): void {
    if (incoming !== undefined && incoming > this.version) {
      this.version = incoming;
    }
  }

  private syncVersion(): void {
    let max = 0;
    for (const [, entry] of this.store.items()) {
      if (entry.version > max) {
        max = entry.version;
      }
    }
    this.version = max;
  }
}

