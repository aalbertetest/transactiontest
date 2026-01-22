import { createHash } from "crypto";

type RingEntry = { hash: number; nodeId: string };

export class HashRing {
  private ring: RingEntry[] = [];

  constructor(private vnodes = 64, nodes: string[] = []) {
    for (const node of nodes) {
      this.addNode(node);
    }
  }

  addNode(nodeId: string): void {
    for (let i = 0; i < this.vnodes; i += 1) {
      const hash = this.hash(`${nodeId}:${i}`);
      this.ring.push({ hash, nodeId });
    }
    this.ring.sort((a, b) => a.hash - b.hash);
  }

  removeNode(nodeId: string): void {
    this.ring = this.ring.filter((entry) => entry.nodeId !== nodeId);
  }

  getNode(key: string): string {
    if (this.ring.length === 0) {
      throw new Error("hash ring is empty");
    }
    const hash = this.hash(key);
    let idx = this.search(hash);
    if (idx === this.ring.length) {
      idx = 0;
    }
    return this.ring[idx].nodeId;
  }

  getNodes(key: string, count: number): string[] {
    if (count <= 0 || this.ring.length === 0) {
      return [];
    }
    const hash = this.hash(key);
    let idx = this.search(hash);
    const seen = new Set<string>();
    const nodes: string[] = [];
    while (nodes.length < count && seen.size < this.ring.length) {
      if (idx === this.ring.length) {
        idx = 0;
      }
      const nodeId = this.ring[idx].nodeId;
      if (!seen.has(nodeId)) {
        seen.add(nodeId);
        nodes.push(nodeId);
      }
      idx += 1;
    }
    return nodes;
  }

  private search(hash: number): number {
    let low = 0;
    let high = this.ring.length;
    while (low < high) {
      const mid = Math.floor((low + high) / 2);
      if (this.ring[mid].hash >= hash) {
        high = mid;
      } else {
        low = mid + 1;
      }
    }
    return low;
  }

  private hash(value: string): number {
    const digest = createHash("sha1").update(value).digest();
    return digest.readUInt32BE(0);
  }
}
