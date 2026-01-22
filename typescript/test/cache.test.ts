import test from "node:test";
import assert from "node:assert/strict";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";

import { Cluster } from "../src/cluster";
import { Node } from "../src/node";
import { Persistence } from "../src/persistence";
import { InMemoryTransport } from "../src/transport";

test("set/get with ttl", () => {
  let now = 0;
  const clock = () => now;
  const node = new Node("n1", { clock });
  node.set("a", "value", 10);
  assert.equal(node.get("a"), "value");
  now = 11;
  assert.equal(node.get("a"), undefined);
});

test("lru eviction", () => {
  const node = new Node("n1", { capacity: 2, clock: () => 0 });
  node.set("a", 1);
  node.set("b", 2);
  node.get("a");
  node.set("c", 3);
  assert.equal(node.get("b"), undefined);
  assert.equal(node.get("a"), 1);
});

test("replication across cluster", () => {
  const transport = new InMemoryTransport();
  const nodeA = new Node("a", { transport, clock: () => 0 });
  const nodeB = new Node("b", { transport, clock: () => 0 });
  const cluster = new Cluster([nodeA, nodeB], 2);
  cluster.set("k1", "v1");
  assert.equal(nodeB.get("k1"), "v1");
});

test("persistence snapshot and log", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "cache-"));
  const snapshot = path.join(dir, "snapshot.json");
  const logPath = path.join(dir, "aof.log");
  const persistence = new Persistence(snapshot, logPath);

  let now = 1000;
  const clock = () => now;
  const node = new Node("n1", { clock, persistence });
  node.set("a", "value");
  node.snapshot();
  node.set("b", "value2", 100);

  const node2 = new Node("n2", { clock, persistence });
  node2.load();
  assert.equal(node2.get("a"), "value");
  assert.equal(node2.get("b"), "value2");

  now += 200;
  assert.equal(node2.get("b"), undefined);
});

test("pubsub fan-out in cluster", () => {
  const transport = new InMemoryTransport();
  const nodeA = new Node("a", { transport });
  const nodeB = new Node("b", { transport });
  const cluster = new Cluster([nodeA, nodeB], 2);
  const received: unknown[] = [];
  nodeB.subscribe("news", (payload) => received.push(payload));
  cluster.publish("news", { hello: "world" });
  assert.deepEqual(received, [{ hello: "world" }]);
});
