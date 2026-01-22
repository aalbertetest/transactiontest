export interface EvictionPolicy {
  onGet(key: string): void;
  onSet(key: string): void;
  onDelete(key: string): void;
  evict(capacity: number, size: number): string[];
}

class LRUNode {
  key: string;
  prev?: LRUNode;
  next?: LRUNode;

  constructor(key: string) {
    this.key = key;
  }
}

export class LRUEviction implements EvictionPolicy {
  private nodes = new Map<string, LRUNode>();
  private head?: LRUNode;
  private tail?: LRUNode;

  onGet(key: string): void {
    const node = this.nodes.get(key);
    if (!node) {
      return;
    }
    this.moveToHead(node);
  }

  onSet(key: string): void {
    const node = this.nodes.get(key);
    if (node) {
      this.moveToHead(node);
      return;
    }
    const created = new LRUNode(key);
    this.nodes.set(key, created);
    this.addToHead(created);
  }

  onDelete(key: string): void {
    const node = this.nodes.get(key);
    if (!node) {
      return;
    }
    this.nodes.delete(key);
    this.remove(node);
  }

  evict(capacity: number, size: number): string[] {
    const evicted: string[] = [];
    while (size > capacity && this.tail) {
      const key = this.tail.key;
      evicted.push(key);
      this.onDelete(key);
      size -= 1;
    }
    return evicted;
  }

  private addToHead(node: LRUNode): void {
    node.prev = undefined;
    node.next = this.head;
    if (this.head) {
      this.head.prev = node;
    }
    this.head = node;
    if (!this.tail) {
      this.tail = node;
    }
  }

  private remove(node: LRUNode): void {
    if (node.prev) {
      node.prev.next = node.next;
    } else {
      this.head = node.next;
    }
    if (node.next) {
      node.next.prev = node.prev;
    } else {
      this.tail = node.prev;
    }
    node.prev = undefined;
    node.next = undefined;
  }

  private moveToHead(node: LRUNode): void {
    if (this.head === node) {
      return;
    }
    this.remove(node);
    this.addToHead(node);
  }
}
