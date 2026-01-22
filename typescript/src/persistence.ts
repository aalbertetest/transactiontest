import fs from "fs";
import path from "path";
import { Store } from "./storage";

type SnapshotEntry = {
  value: unknown;
  expiresAt?: number;
  version: number;
};

type LogRecord = {
  op: "set" | "del" | "expire";
  key: string;
  value?: unknown;
  expiresAt?: number;
  version: number;
};

export class Persistence {
  constructor(private snapshotPath: string, private logPath: string) {}

  appendSet(key: string, value: unknown, expiresAt: number | undefined, version: number): void {
    this.append({ op: "set", key, value, expiresAt, version });
  }

  appendDelete(key: string, version: number): void {
    this.append({ op: "del", key, version });
  }

  appendExpire(key: string, expiresAt: number, version: number): void {
    this.append({ op: "expire", key, expiresAt, version });
  }

  snapshot(store: Store): void {
    const now = store.now();
    const data: Record<string, SnapshotEntry> = {};
    for (const [key, entry] of store.items()) {
      if (entry.expiresAt !== undefined && now >= entry.expiresAt) {
        continue;
      }
      data[key] = {
        value: entry.value,
        expiresAt: entry.expiresAt,
        version: entry.version,
      };
    }
    fs.mkdirSync(path.dirname(this.snapshotPath), { recursive: true });
    fs.writeFileSync(this.snapshotPath, JSON.stringify(data));
    if (fs.existsSync(this.logPath)) {
      fs.writeFileSync(this.logPath, "");
    }
  }

  load(store: Store): void {
    if (fs.existsSync(this.snapshotPath)) {
      const raw = fs.readFileSync(this.snapshotPath, "utf8");
      if (raw.trim().length > 0) {
        const snapshot = JSON.parse(raw) as Record<string, SnapshotEntry>;
        this.applySnapshot(store, snapshot);
      }
    }
    if (fs.existsSync(this.logPath)) {
      const raw = fs.readFileSync(this.logPath, "utf8");
      const lines = raw.split("\n").filter((line) => line.trim().length > 0);
      for (const line of lines) {
        const record = JSON.parse(line) as LogRecord;
        this.applyLogRecord(store, record);
      }
    }
  }

  private append(record: LogRecord): void {
    fs.mkdirSync(path.dirname(this.logPath), { recursive: true });
    fs.appendFileSync(this.logPath, `${JSON.stringify(record)}\n`);
  }

  private applySnapshot(store: Store, snapshot: Record<string, SnapshotEntry>): void {
    const now = store.now();
    for (const [key, entry] of Object.entries(snapshot)) {
      if (entry.expiresAt !== undefined && now >= entry.expiresAt) {
        continue;
      }
      const existing = store.getEntry(key);
      if (existing && entry.version <= existing.version) {
        continue;
      }
      const ttlMs = entry.expiresAt !== undefined ? Math.max(entry.expiresAt - now, 0) : undefined;
      store.set(key, entry.value, ttlMs, entry.version);
    }
  }

  private applyLogRecord(store: Store, record: LogRecord): void {
    const existing = store.getEntry(record.key);
    if (existing && record.version <= existing.version) {
      return;
    }
    if (record.op === "set") {
      const ttlMs =
        record.expiresAt !== undefined ? Math.max(record.expiresAt - store.now(), 0) : undefined;
      store.set(record.key, record.value, ttlMs, record.version);
    } else if (record.op === "del") {
      store.delete(record.key);
    } else if (record.op === "expire") {
      if (record.expiresAt === undefined) {
        return;
      }
      const ttlMs = Math.max(record.expiresAt - store.now(), 0);
      store.expire(record.key, ttlMs, record.version);
    }
  }
}
