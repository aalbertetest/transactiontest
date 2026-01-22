import { performance } from "node:perf_hooks";

import { Cluster } from "../src/cluster";
import { Node } from "../src/node";
import { InMemoryTransport } from "../src/transport";

const benchNode = (iterations = 50000): void => {
  const node = new Node("n1");
  const start = performance.now();
  for (let i = 0; i < iterations; i += 1) {
    node.set(`k${i}`, i);
  }
  const mid = performance.now();
  for (let i = 0; i < iterations; i += 1) {
    node.get(`k${i}`);
  }
  const end = performance.now();
  const setQps = (iterations / (mid - start)) * 1000;
  const getQps = (iterations / (end - mid)) * 1000;
  console.log(`node set: ${setQps.toFixed(0)} ops/s`);
  console.log(`node get: ${getQps.toFixed(0)} ops/s`);
};

const benchCluster = (iterations = 50000): void => {
  const transport = new InMemoryTransport();
  const cluster = new Cluster(
    [new Node("a", { transport }), new Node("b", { transport })],
    2,
  );
  const start = performance.now();
  for (let i = 0; i < iterations; i += 1) {
    cluster.set(`k${i}`, i);
  }
  const mid = performance.now();
  for (let i = 0; i < iterations; i += 1) {
    cluster.get(`k${i}`);
  }
  const end = performance.now();
  const setQps = (iterations / (mid - start)) * 1000;
  const getQps = (iterations / (end - mid)) * 1000;
  console.log(`cluster set: ${setQps.toFixed(0)} ops/s`);
  console.log(`cluster get: ${getQps.toFixed(0)} ops/s`);
};

benchNode();
benchCluster();
