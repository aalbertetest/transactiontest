#!/usr/bin/env node
'use strict';

/**
 * Load test: simulates N concurrent WebSocket clients against the game server.
 *
 * Each bot:
 *   - Connects and receives the init message.
 *   - Sends random movement + fire inputs at 20 Hz.
 *   - Tracks latency samples from pong messages.
 *   - Counts bytes received.
 *
 * Usage:
 *   node loadtest.js [clients] [duration_s] [server_url]
 *
 * Examples:
 *   node loadtest.js 200 30 ws://localhost:8080
 *   node loadtest.js 50  10
 */

const { WebSocket } = require('ws');

const NUM_CLIENTS   = parseInt(process.argv[2] || '200', 10);
const DURATION_S    = parseInt(process.argv[3] || '30',  10);
const SERVER_URL    = process.argv[4] || 'ws://localhost:8080';
const INPUT_HZ      = 20;
const INPUT_INTERVAL_MS = Math.round(1000 / INPUT_HZ);
const CONNECT_STAGGER_MS = 20; // ms between each new connection to avoid SYN flood

// ─── Per-client stats ─────────────────────────────────────────────────────────

class BotStats {
  constructor(id) {
    this.id           = id;
    this.connected    = false;
    this.initialized  = false;
    this.msgReceived  = 0;
    this.bytesReceived= 0;
    this.bytesSent    = 0;
    this.inputsSent   = 0;
    this.errors       = 0;
    this.latencySamples = [];
    this.connectTime  = null;
    this.disconnected = false;
  }
}

// ─── Aggregate stats ──────────────────────────────────────────────────────────

const allStats    = [];
let   startTime   = null;
let   totalConns  = 0;
let   totalErrors = 0;

function percentile(sorted, p) {
  if (!sorted.length) return 0;
  const idx = Math.ceil((p / 100) * sorted.length) - 1;
  return sorted[Math.max(0, idx)];
}

function printReport() {
  const elapsed = (Date.now() - startTime) / 1000;
  const connected   = allStats.filter(s => s.connected && !s.disconnected).length;
  const initialized = allStats.filter(s => s.initialized).length;
  const totalMsg    = allStats.reduce((a, s) => a + s.msgReceived, 0);
  const totalInputs = allStats.reduce((a, s) => a + s.inputsSent, 0);
  const totalBytesRx= allStats.reduce((a, s) => a + s.bytesReceived, 0);
  const totalBytesTx= allStats.reduce((a, s) => a + s.bytesSent, 0);
  const errCount    = allStats.reduce((a, s) => a + s.errors, 0);

  const allLatencies = allStats
    .flatMap(s => s.latencySamples)
    .sort((a, b) => a - b);

  const p50  = percentile(allLatencies, 50);
  const p95  = percentile(allLatencies, 95);
  const p99  = percentile(allLatencies, 99);
  const mean = allLatencies.length
    ? Math.round(allLatencies.reduce((a, v) => a + v, 0) / allLatencies.length)
    : 0;

  const kbRx = (totalBytesRx / 1024).toFixed(1);
  const kbTx = (totalBytesTx / 1024).toFixed(1);
  const kbRxSec = (totalBytesRx / 1024 / elapsed).toFixed(1);
  const kbTxSec = (totalBytesTx / 1024 / elapsed).toFixed(1);

  console.log('\n' + '═'.repeat(60));
  console.log('  LOAD TEST REPORT');
  console.log('═'.repeat(60));
  console.log(`  Server URL     : ${SERVER_URL}`);
  console.log(`  Target clients : ${NUM_CLIENTS}`);
  console.log(`  Duration       : ${elapsed.toFixed(1)} s`);
  console.log('─'.repeat(60));
  console.log(`  Connected now  : ${connected}`);
  console.log(`  Initialized    : ${initialized}`);
  console.log(`  Total connects : ${totalConns}`);
  console.log(`  Errors         : ${errCount}`);
  console.log('─'.repeat(60));
  console.log(`  Messages rx    : ${totalMsg}`);
  console.log(`  Inputs sent    : ${totalInputs}`);
  console.log(`  Bytes rx       : ${kbRx} KB  (${kbRxSec} KB/s)`);
  console.log(`  Bytes tx       : ${kbTx} KB  (${kbTxSec} KB/s)`);
  console.log('─'.repeat(60));
  console.log(`  RTT samples    : ${allLatencies.length}`);
  console.log(`  RTT mean       : ${mean} ms`);
  console.log(`  RTT p50        : ${p50} ms`);
  console.log(`  RTT p95        : ${p95} ms`);
  console.log(`  RTT p99        : ${p99} ms`);
  console.log('═'.repeat(60));
  console.log();
}

// ─── Bot factory ─────────────────────────────────────────────────────────────

const DIRECTIONS = [
  { up: false, down: false, left: false, right: true  },
  { up: false, down: true,  left: false, right: false },
  { up: true,  down: false, left: false, right: false },
  { up: false, down: false, left: true,  right: false },
  { up: true,  down: false, left: false, right: true  },
  { up: false, down: true,  left: true,  right: false },
];

function createBot(index) {
  const stats = new BotStats(index);
  allStats.push(stats);

  let inputInterval = null;
  let pingInterval  = null;
  let inputSeq      = 0;
  let directionIdx  = Math.floor(Math.random() * DIRECTIONS.length);
  let dirChangeTimer = 0;

  const ws = new WebSocket(SERVER_URL);
  totalConns++;

  ws.on('open', () => {
    stats.connected   = true;
    stats.connectTime = Date.now();

    // Send inputs at INPUT_HZ
    inputInterval = setInterval(() => {
      if (!stats.initialized || ws.readyState !== WebSocket.OPEN) return;

      // Change direction every 1-3 seconds
      dirChangeTimer++;
      if (dirChangeTimer > INPUT_HZ * (1 + Math.random() * 2)) {
        directionIdx  = (directionIdx + 1) % DIRECTIONS.length;
        dirChangeTimer = 0;
      }

      const fire  = Math.random() < 0.15; // fire 15% of ticks
      const angle = Math.random() * Math.PI * 2;
      const msg   = JSON.stringify({
        type:  'input',
        seq:   ++inputSeq,
        tick:  0,
        keys:  DIRECTIONS[directionIdx],
        fire,
        angle,
      });

      ws.send(msg);
      stats.inputsSent++;
      stats.bytesSent += msg.length;
    }, INPUT_INTERVAL_MS);

    // Ping every 5s
    pingInterval = setInterval(() => {
      if (ws.readyState !== WebSocket.OPEN) return;
      const msg = JSON.stringify({ type: 'ping', clientTs: Date.now() });
      ws.send(msg);
      stats.bytesSent += msg.length;
    }, 5000);
  });

  ws.on('message', (data) => {
    const raw = data.toString();
    stats.msgReceived++;
    stats.bytesReceived += raw.length;

    let msg;
    try { msg = JSON.parse(raw); } catch { return; }

    if (msg.type === 'init') {
      stats.initialized = true;
    } else if (msg.type === 'pong') {
      const rtt = Date.now() - msg.clientTs;
      if (rtt >= 0 && rtt < 10000) {
        stats.latencySamples.push(rtt);
        if (stats.latencySamples.length > 50) stats.latencySamples.shift();
      }
    }
  });

  ws.on('close', () => {
    stats.connected    = false;
    stats.disconnected = true;
    clearInterval(inputInterval);
    clearInterval(pingInterval);
  });

  ws.on('error', (err) => {
    stats.errors++;
    totalErrors++;
    // Suppress individual error noise during load test
    if (process.env.VERBOSE) {
      console.error(`[bot-${index}] error: ${err.message}`);
    }
  });

  return ws;
}

// ─── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log(`\nArena Game Load Test`);
  console.log(`Connecting ${NUM_CLIENTS} bots to ${SERVER_URL}`);
  console.log(`Duration: ${DURATION_S}s  |  Input rate: ${INPUT_HZ} Hz/bot\n`);

  startTime = Date.now();
  const sockets = [];

  // Stagger connections
  for (let i = 0; i < NUM_CLIENTS; i++) {
    sockets.push(createBot(i));
    if (CONNECT_STAGGER_MS > 0) {
      await new Promise(r => setTimeout(r, CONNECT_STAGGER_MS));
    }
  }

  // Live progress
  const progressInterval = setInterval(() => {
    const connected   = allStats.filter(s => s.connected).length;
    const initialized = allStats.filter(s => s.initialized).length;
    const elapsed     = ((Date.now() - startTime) / 1000).toFixed(1);
    const totalMsg    = allStats.reduce((a, s) => a + s.msgReceived, 0);
    process.stdout.write(
      `\r  t=${elapsed}s  connected=${connected}/${NUM_CLIENTS}  init=${initialized}  msgs_rx=${totalMsg}  errors=${totalErrors}   `
    );
  }, 1000);

  // Run for DURATION_S, then close all and print report
  await new Promise(r => setTimeout(r, DURATION_S * 1000));

  clearInterval(progressInterval);
  process.stdout.write('\n');

  console.log('\nClosing all connections…');
  for (const ws of sockets) {
    if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
      ws.close();
    }
  }

  // Brief settle
  await new Promise(r => setTimeout(r, 500));
  printReport();
  process.exit(0);
}

main().catch(err => {
  console.error('Fatal:', err);
  process.exit(1);
});
