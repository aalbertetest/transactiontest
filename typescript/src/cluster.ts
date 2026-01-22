import { Node } from "./node";
import { HashRing } from "./sharding";

export class Cluster {
  private nodes = new Map<string, Node>();
  private ring: HashRing;
  private replicationFactor: number;

  constructor(nodes: Node[], replicationFactor = 2) {
    for (const node of nodes) {
      this.nodes.set(node.id, node);
    }
    this.ring = new HashRing(64, Array.from(this.nodes.keys()));
    this.replicationFactor = Math.max(1, Math.min(replicationFactor, this.nodes.size));
  }

  addNode(node: Node): void {
    this.nodes.set(node.id, node);
    this.ring.addNode(node.id);
    this.replicationFactor = Math.min(this.replicationFactor, this.nodes.size);
  }

  removeNode(nodeId: string): void {
    this.nodes.delete(nodeId);
    this.ring.removeNode(nodeId);
    this.replicationFactor = Math.min(this.replicationFactor, this.nodes.size);
  }

  get(key: string): unknown | undefined {
    const nodes = this.ring.getNodes(key, this.replicationFactor);
    for (const nodeId of nodes) {
      const value = this.nodes.get(nodeId)?.get(key);
      if (value !== undefined) {
        return value;
      }
    }
    return undefined;
  }

  set(key: string, value: unknown, ttlMs?: number): number {
    const nodes = this.ring.getNodes(key, this.replicationFactor);
    if (nodes.length === 0) {
      throw new Error("cluster has no nodes");
    }
    const primary = nodes[0];
    const replicas = nodes.slice(1);
    return this.nodes.get(primary)!.set(key, value, ttlMs, replicas);
  }

  delete(key: string): boolean {
    const nodes = this.ring.getNodes(key, this.replicationFactor);
    if (nodes.length === 0) {
      return false;
    }
    const primary = nodes[0];
    const replicas = nodes.slice(1);
    return this.nodes.get(primary)!.delete(key, replicas);
  }

  expire(key: string, ttlMs: number): boolean {
    const nodes = this.ring.getNodes(key, this.replicationFactor);
    if (nodes.length === 0) {
      return false;
    }
    const primary = nodes[0];
    const replicas = nodes.slice(1);
    return this.nodes.get(primary)!.expire(key, ttlMs, replicas);
  }

  publish(channel: string, payload: unknown): number {
    if (this.nodes.size === 0) {
      return 0;
    }
    const primary = this.ring.getNode(channel);
    const replicas = Array.from(this.nodes.keys()).filter((id) => id !== primary);
    return this.nodes.get(primary)!.publish(channel, payload, replicas);
  }

  sweepExpired(): void {
    for (const node of this.nodes.values()) {
      node.sweepExpired();
    }
  }

  snapshot(): void {
    for (const node of this.nodes.values()) {
      node.snapshot();
    }
  }
}
