import { EvictionPolicy, LRUEviction } from "./eviction";

export interface Entry {
  value: unknown;
  expiresAt?: number;
  version: number;
}

export class Store {
  private entries = new Map<string, Entry>();
  private eviction: EvictionPolicy;
  private version = 0;

  constructor(
    private capacity = 1024,
    eviction?: EvictionPolicy,
    private clock: () => number = () => Date.now(),
  ) {
    this.eviction = eviction ?? new LRUEviction();
  }

  set(
    key: string,
    value: unknown,
    ttlMs?: number,
    version?: number,
  ): { version: number; evicted: string[] } {
    const expiresAt = ttlMs !== undefined ? this.clock() + ttlMs : undefined;
    if (version === undefined) {
      this.version += 1;
      version = this.version;
    }
    this.entries.set(key, { value, expiresAt, version });
    this.eviction.onSet(key);
    const evicted = this.evictIfNeeded();
    return { version, evicted };
  }

  get(key: string): unknown | undefined {
    const entry = this.entries.get(key);
    if (!entry) {
      return undefined;
    }
    if (this.isExpired(entry)) {
      this.entries.delete(key);
      this.eviction.onDelete(key);
      return undefined;
    }
    this.eviction.onGet(key);
    return entry.value;
  }

  getEntry(key: string): Entry | undefined {
    const entry = this.entries.get(key);
    if (!entry) {
      return undefined;
    }
    if (this.isExpired(entry)) {
      this.entries.delete(key);
      this.eviction.onDelete(key);
      return undefined;
    }
    return entry;
  }

  delete(key: string): boolean {
    const existed = this.entries.delete(key);
    if (existed) {
      this.eviction.onDelete(key);
    }
    return existed;
  }

  expire(key: string, ttlMs: number, version?: number): boolean {
    const entry = this.entries.get(key);
    if (!entry) {
      return false;
    }
    if (version === undefined) {
      this.version += 1;
      version = this.version;
    }
    entry.expiresAt = this.clock() + ttlMs;
    entry.version = version;
    this.entries.set(key, entry);
    return true;
  }

  sweepExpired(): string[] {
    const expired: string[] = [];
    for (const [key, entry] of this.entries.entries()) {
      if (this.isExpired(entry)) {
        this.entries.delete(key);
        this.eviction.onDelete(key);
        expired.push(key);
      }
    }
    return expired;
  }

  items(): Array<[string, Entry]> {
    return Array.from(this.entries.entries());
  }

  now(): number {
    return this.clock();
  }

  private isExpired(entry: Entry): boolean {
    return entry.expiresAt !== undefined && this.clock() >= entry.expiresAt;
  }

  private evictIfNeeded(): string[] {
    if (this.capacity <= 0) {
      return [];
    }
    if (this.entries.size <= this.capacity) {
      return [];
    }
    const evicted = this.eviction.evict(this.capacity, this.entries.size);
    for (const key of evicted) {
      this.entries.delete(key);
    }
    return evicted;
  }
}
