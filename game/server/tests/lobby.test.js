'use strict';

const { describe, it, beforeEach, afterEach } = require('node:test');
const assert = require('node:assert/strict');

const { LobbyManager, Lobby, LOBBY_STATE } = require('../lobbyManager');
const CFG = require('../config');

// ─── Stub WebSocket ───────────────────────────────────────────────────────────

function stubWs() {
  const ws = {
    readyState: 1,  // OPEN
    messages:   [],
    send(data) { this.messages.push(JSON.parse(data)); },
    close() { this.readyState = 3; },
  };
  return ws;
}

// ─── Helpers ──────────────────────────────────────────────────────────────────

function fillLobbyPlayers(lobby, n) {
  const wsList = [];
  for (let i = 0; i < n; i++) {
    const ws = stubWs();
    wsList.push(ws);
    lobby.addPlayer(`p${i}`, `Player${i}`, ws);
  }
  return wsList;
}

// ─────────────────────────────────────────────────────────────────────────────
// LOBBY_STATE constants
// ─────────────────────────────────────────────────────────────────────────────

describe('LOBBY_STATE', () => {
  it('has expected keys', () => {
    assert.equal(LOBBY_STATE.WAITING,     'waiting');
    assert.equal(LOBBY_STATE.COUNTDOWN,   'countdown');
    assert.equal(LOBBY_STATE.IN_PROGRESS, 'in_progress');
    assert.equal(LOBBY_STATE.FINISHED,    'finished');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Lobby — construction
// ─────────────────────────────────────────────────────────────────────────────

describe('Lobby construction', () => {
  it('starts in WAITING state', () => {
    const l = new Lobby('l1', 'Test');
    assert.equal(l.state, LOBBY_STATE.WAITING);
    l.destroy();
  });

  it('has no players or spectators initially', () => {
    const l = new Lobby('l1', 'Test');
    assert.equal(l.players.size, 0);
    assert.equal(l.spectators.size, 0);
    l.destroy();
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Lobby — player management
// ─────────────────────────────────────────────────────────────────────────────

describe('Lobby player management', () => {
  let lobby;
  beforeEach(() => { lobby = new Lobby('l1', 'Test'); });
  afterEach(() => lobby.destroy());

  it('accepts a player when in WAITING and not full', () => {
    const ok = lobby.addPlayer('p1', 'Alice', stubWs());
    assert.ok(ok);
    assert.equal(lobby.players.size, 1);
  });

  it('rejects player when in_progress', () => {
    fillLobbyPlayers(lobby, 2);
    lobby.startMatch();
    const ok = lobby.addPlayer('p_late', 'Late', stubWs());
    assert.equal(ok, false);
  });

  it('rejects player when full', () => {
    fillLobbyPlayers(lobby, CFG.LOBBY_MAX_PLAYERS);
    const ok = lobby.addPlayer('extra', 'Extra', stubWs());
    assert.equal(ok, false);
  });

  it('removes player cleanly', () => {
    lobby.addPlayer('p1', 'Alice', stubWs());
    lobby.removePlayer('p1');
    assert.equal(lobby.players.size, 0);
  });

  it('canJoinAsPlayer is false when full', () => {
    fillLobbyPlayers(lobby, CFG.LOBBY_MAX_PLAYERS);
    assert.equal(lobby.canJoinAsPlayer(), false);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Lobby — spectator management
// ─────────────────────────────────────────────────────────────────────────────

describe('Lobby spectator management', () => {
  let lobby;
  beforeEach(() => { lobby = new Lobby('l1', 'Test'); });
  afterEach(() => lobby.destroy());

  it('accepts a spectator in WAITING state', () => {
    const ok = lobby.addSpectator('s1', 'Viewer', stubWs());
    assert.ok(ok);
    assert.equal(lobby.spectators.size, 1);
  });

  it('accepts a spectator in IN_PROGRESS state', () => {
    fillLobbyPlayers(lobby, 2);
    lobby.startMatch();
    const ok = lobby.addSpectator('s1', 'Viewer', stubWs());
    assert.ok(ok);
  });

  it('rejects spectator when FINISHED', () => {
    lobby.state = LOBBY_STATE.FINISHED;
    const ok = lobby.addSpectator('s1', 'Viewer', stubWs());
    assert.equal(ok, false);
  });

  it('rejects spectator when spectator cap reached', () => {
    for (let i = 0; i < CFG.LOBBY_MAX_SPECTATORS; i++) {
      lobby.addSpectator(`s${i}`, `Viewer${i}`, stubWs());
    }
    const ok = lobby.addSpectator('overflow', 'X', stubWs());
    assert.equal(ok, false);
  });

  it('removes spectator cleanly', () => {
    lobby.addSpectator('s1', 'Viewer', stubWs());
    lobby.removeSpectator('s1');
    assert.equal(lobby.spectators.size, 0);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Lobby — ready system
// ─────────────────────────────────────────────────────────────────────────────

describe('Lobby ready system', () => {
  let lobby;
  beforeEach(() => { lobby = new Lobby('l1', 'Test'); });
  afterEach(() => lobby.destroy());

  it('readyCount starts at 0', () => {
    fillLobbyPlayers(lobby, 2);
    assert.equal(lobby.readyCount, 0);
  });

  it('increments readyCount when player readies', () => {
    fillLobbyPlayers(lobby, 2);
    lobby.setReady('p0', true);
    assert.equal(lobby.readyCount, 1);
  });

  it('allReady is false when count < MIN_TO_START', () => {
    lobby.addPlayer('p0', 'A', stubWs());
    lobby.setReady('p0', true);
    assert.equal(lobby.allReady, false);
  });

  it('allReady is false when some players not ready', () => {
    fillLobbyPlayers(lobby, 2);
    lobby.setReady('p0', true);
    assert.equal(lobby.allReady, false);
  });

  it('allReady is true when all players ready and count >= MIN', () => {
    fillLobbyPlayers(lobby, CFG.LOBBY_MIN_TO_START);
    for (let i = 0; i < CFG.LOBBY_MIN_TO_START; i++) lobby.setReady(`p${i}`, true);
    assert.ok(lobby.allReady);
  });

  it('toggling ready off decrements allReady check', () => {
    fillLobbyPlayers(lobby, 2);
    lobby.setReady('p0', true);
    lobby.setReady('p1', true);
    assert.ok(lobby.allReady);
    lobby.setReady('p0', false);
    assert.equal(lobby.allReady, false);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Lobby — countdown
// ─────────────────────────────────────────────────────────────────────────────

describe('Lobby countdown', () => {
  let lobby;
  beforeEach(() => { lobby = new Lobby('l1', 'Test'); });
  afterEach(() => lobby.destroy());

  it('transitions to COUNTDOWN state', (_, done) => {
    lobby.startCountdown(() => {}, () => { lobby.destroy(); done(); });
    assert.equal(lobby.state, LOBBY_STATE.COUNTDOWN);
  });

  it('calls onTick with initial remaining value', (_, done) => {
    let first = null;
    lobby.startCountdown((r) => {
      if (first === null) { first = r; assert.ok(r > 0); }
    }, () => { lobby.destroy(); done(); });
  });

  it('cancelCountdown reverts to WAITING', () => {
    lobby.startCountdown(() => {}, () => {});
    lobby.cancelCountdown();
    assert.equal(lobby.state, LOBBY_STATE.WAITING);
  });

  it('does not start countdown if already counting down', () => {
    lobby.startCountdown(() => {}, () => {});
    const timer1 = lobby.countdownTimer;
    lobby.startCountdown(() => {}, () => {}); // second call should no-op
    assert.equal(lobby.countdownTimer, timer1);
    lobby.cancelCountdown();
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Lobby — match lifecycle
// ─────────────────────────────────────────────────────────────────────────────

describe('Lobby match lifecycle', () => {
  let lobby;
  beforeEach(() => {
    lobby = new Lobby('l1', 'Test');
    fillLobbyPlayers(lobby, 2);
  });
  afterEach(() => lobby.destroy());

  it('startMatch transitions to IN_PROGRESS', () => {
    lobby.startMatch();
    assert.equal(lobby.state, LOBBY_STATE.IN_PROGRESS);
  });

  it('creates game world with all players', () => {
    lobby.startMatch();
    assert.equal(lobby.world.players.size, 2);
  });

  it('tick advances world tick counter', () => {
    lobby.startMatch();
    const result = lobby.tick(Date.now() + 50);
    assert.ok(result !== null);
    assert.equal(lobby.world.tick, 1);
  });

  it('endMatch transitions to FINISHED', () => {
    lobby.startMatch();
    lobby.endMatch('p0', 'score');
    assert.equal(lobby.state, LOBBY_STATE.FINISHED);
  });

  it('leaderboard is sorted by score descending', () => {
    lobby.startMatch();
    lobby.world.players.get('p0').score = 5;
    lobby.world.players.get('p1').score = 3;
    const board = lobby.leaderboard();
    assert.equal(board[0].score, 5);
    assert.equal(board[1].score, 3);
  });

  it('checkWinCondition returns null before score limit', () => {
    lobby.startMatch();
    assert.equal(lobby.checkWinCondition(), null);
  });

  it('checkWinCondition detects score limit', () => {
    lobby.startMatch();
    lobby.world.players.get('p0').score = CFG.MATCH_SCORE_LIMIT;
    const win = lobby.checkWinCondition();
    assert.ok(win !== null);
    assert.equal(win.winnerId, 'p0');
    assert.equal(win.reason, 'score');
  });

  it('checkWinCondition detects time limit', () => {
    lobby.startMatch();
    lobby.matchStartTime = Date.now() - (CFG.MATCH_TIME_LIMIT_S * 1000 + 100);
    const win = lobby.checkWinCondition();
    assert.ok(win !== null);
    assert.equal(win.reason, 'time');
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Lobby — serialization
// ─────────────────────────────────────────────────────────────────────────────

describe('Lobby toLobbyInfo', () => {
  let lobby;
  beforeEach(() => { lobby = new Lobby('l1', 'My Lobby'); });
  afterEach(() => lobby.destroy());

  it('returns correct id and name', () => {
    const info = lobby.toLobbyInfo();
    assert.equal(info.id,   'l1');
    assert.equal(info.name, 'My Lobby');
  });

  it('returns correct playerCount', () => {
    fillLobbyPlayers(lobby, 3);
    assert.equal(lobby.toLobbyInfo().playerCount, 3);
  });

  it('includes players array with ready flags', () => {
    fillLobbyPlayers(lobby, 2);
    lobby.setReady('p0', true);
    const info = lobby.toLobbyInfo();
    const p0 = info.players.find(p => p.id === 'p0');
    assert.ok(p0.ready);
    const p1 = info.players.find(p => p.id === 'p1');
    assert.equal(p1.ready, false);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// Lobby — broadcast helpers
// ─────────────────────────────────────────────────────────────────────────────

describe('Lobby broadcast', () => {
  let lobby;
  beforeEach(() => { lobby = new Lobby('l1', 'Test'); });
  afterEach(() => lobby.destroy());

  it('broadcastToAll sends to players and spectators', () => {
    const pw = stubWs(); lobby.addPlayer('p1', 'A', pw);
    const sw = stubWs(); lobby.addSpectator('s1', 'V', sw);
    lobby.broadcastToAll({ type: 'test' });
    assert.equal(pw.messages.length, 1);
    assert.equal(sw.messages.length, 1);
  });

  it('broadcastToPlayers does not send to spectators', () => {
    const pw = stubWs(); lobby.addPlayer('p1', 'A', pw);
    const sw = stubWs(); lobby.addSpectator('s1', 'V', sw);
    lobby.broadcastToPlayers({ type: 'test' });
    assert.equal(pw.messages.length, 1);
    assert.equal(sw.messages.length, 0);
  });

  it('broadcastToSpectators does not send to players', () => {
    const pw = stubWs(); lobby.addPlayer('p1', 'A', pw);
    const sw = stubWs(); lobby.addSpectator('s1', 'V', sw);
    lobby.broadcastToSpectators({ type: 'test' });
    assert.equal(pw.messages.length, 0);
    assert.equal(sw.messages.length, 1);
  });

  it('sendToOne sends to a player by id', () => {
    const pw = stubWs(); lobby.addPlayer('p1', 'A', pw);
    lobby.sendToOne('p1', { type: 'hello' });
    assert.equal(pw.messages[0].type, 'hello');
  });

  it('sendToOne sends to a spectator by id', () => {
    const sw = stubWs(); lobby.addSpectator('s1', 'V', sw);
    lobby.sendToOne('s1', { type: 'hello' });
    assert.equal(sw.messages[0].type, 'hello');
  });

  it('skips closed WebSockets', () => {
    const pw = stubWs();
    pw.readyState = 3; // closed
    lobby.addPlayer('p1', 'A', pw);
    assert.doesNotThrow(() => lobby.broadcastToAll({ type: 'test' }));
    assert.equal(pw.messages.length, 0);
  });
});

// ─────────────────────────────────────────────────────────────────────────────
// LobbyManager
// ─────────────────────────────────────────────────────────────────────────────

describe('LobbyManager', () => {
  let mgr;
  beforeEach(() => { mgr = new LobbyManager(); });
  afterEach(() => { for (const l of mgr.lobbies.values()) l.destroy(); });

  it('createLobby creates and stores a lobby', () => {
    const l = mgr.createLobby('Test');
    assert.ok(l);
    assert.equal(mgr.lobbies.size, 1);
  });

  it('getLobby returns lobby by id', () => {
    const l = mgr.createLobby('Test');
    assert.equal(mgr.getLobby(l.id), l);
  });

  it('getLobby returns null for unknown id', () => {
    assert.equal(mgr.getLobby('nope'), null);
  });

  it('listLobbies excludes FINISHED lobbies', () => {
    const l = mgr.createLobby('Done');
    l.state = LOBBY_STATE.FINISHED;
    const list = mgr.listLobbies();
    assert.equal(list.length, 0);
  });

  it('destroyLobby removes lobby', () => {
    const l = mgr.createLobby('Test');
    mgr.destroyLobby(l.id);
    assert.equal(mgr.lobbies.size, 0);
  });

  // ── Queue ────────────────────────────────────────────────────────────────

  it('enqueue adds to queue', () => {
    mgr.enqueue('c1', 'Alice', stubWs());
    assert.equal(mgr.queue.size, 1);
  });

  it('dequeue removes from queue', () => {
    mgr.enqueue('c1', 'Alice', stubWs());
    mgr.dequeue('c1');
    assert.equal(mgr.queue.size, 0);
  });

  it('runMatchmaking does nothing below MIN_QUEUE_TO_FILL', () => {
    mgr.enqueue('c1', 'Alice', stubWs());
    const placed = mgr.runMatchmaking();
    assert.equal(placed.length, 0);
  });

  it('runMatchmaking places queued clients', () => {
    for (let i = 0; i < CFG.MM_MIN_QUEUE_TO_FILL; i++) {
      mgr.enqueue(`c${i}`, `Player${i}`, stubWs());
    }
    const placed = mgr.runMatchmaking();
    assert.ok(placed.length >= CFG.MM_MIN_QUEUE_TO_FILL);
    assert.equal(mgr.queue.size, 0);
  });

  it('runMatchmaking fills existing waiting lobby before creating new one', () => {
    const existingLobby = mgr.createLobby('Existing');
    existingLobby.addPlayer('pre', 'Pre', stubWs());

    for (let i = 0; i < CFG.MM_MIN_QUEUE_TO_FILL; i++) {
      mgr.enqueue(`q${i}`, `Q${i}`, stubWs());
    }
    const lobbyCountBefore = mgr.lobbies.size;
    const placed = mgr.runMatchmaking();
    assert.ok(placed.length > 0);

    // At least some clients should have gone into the existing lobby
    const placedInExisting = placed.filter(p => p.lobby.id === existingLobby.id);
    assert.ok(placedInExisting.length > 0, 'should fill existing lobby first');

    // lobby count should not have grown unnecessarily
    assert.ok(mgr.lobbies.size <= lobbyCountBefore + 1);
  });

  // ── Sweep ─────────────────────────────────────────────────────────────────

  it('sweep removes FINISHED lobbies', () => {
    const l = mgr.createLobby('Done');
    l.state = LOBBY_STATE.FINISHED;
    mgr.sweep();
    assert.equal(mgr.lobbies.size, 0);
  });

  it('sweep removes idle lobbies with _shouldDestroy set', () => {
    const l = mgr.createLobby('Idle');
    l._shouldDestroy = true;
    mgr.sweep();
    assert.equal(mgr.lobbies.size, 0);
  });
});
