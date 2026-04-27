# Realtime Sync Logic

## Why CRDT instead of Operational Transform

Operational Transform works well with a central authority that orders every edit and transforms incoming operations against concurrent operations. It is efficient for simple text streams, but the transform matrix becomes complex once the editor needs reconnects, offline edits, rich metadata, undo semantics, and eventually multi-region collaboration.

This project uses Yjs, a sequence CRDT:

- each client applies edits locally;
- edits are encoded as commutative binary updates;
- the server applies and rebroadcasts updates;
- duplicates and out-of-order updates converge safely;
- reconnecting clients receive the server's current document update.

Tradeoff: CRDT metadata is larger than raw text deltas and needs periodic compaction/snapshotting. The backend stores `Document.yState` snapshots and `plainText` to make reads cheap while preserving merge semantics.

## Protocol

WebSocket endpoint:

```text
GET /ws/collaboration?documentId=<documentId>&token=<accessToken>
```

Client to server:

```json
{ "type": "sync", "update": "<base64-yjs-update>" }
```

```json
{ "type": "presence", "cursor": { "lineNumber": 12, "column": 7 } }
```

Server to client:

```json
{ "type": "sync", "update": "<base64-yjs-update>" }
```

```json
{
  "type": "presence",
  "clients": [
    {
      "userId": "cm...",
      "name": "Ada",
      "color": "#2563eb",
      "cursor": { "lineNumber": 12, "column": 7 }
    }
  ]
}
```

## Server room lifecycle

1. Upgrade handler verifies JWT access token and document membership.
2. Room is lazily loaded from Postgres:
   - `yState` is applied if present;
   - otherwise `plainText` is inserted into a new Y.Doc.
3. New client receives `Y.encodeStateAsUpdate(room.ydoc)`.
4. Incoming updates are applied to the in-memory document and broadcast to other sockets.
5. A debounced flush writes `plainText`, `yState`, increments `version`, and creates a `DocumentSnapshot`.

## Client binding

The React hook in `apps/web/src/features/editor/useCollaboration.ts` binds Monaco edits to a Y.Text:

- Monaco change events are converted to Y.Text deletes/inserts using offsets.
- Yjs `update` events are sent over WebSocket as base64.
- Remote updates are applied with origin `"remote"` to avoid echo loops.
- The Monaco model is replaced from the Y.Text after remote changes.

This implementation is intentionally direct and readable. At larger scale the editor binding can be replaced with `y-monaco` or a custom incremental range mapper to avoid full-model replacement after remote edits.

## Presence

Cursor presence is ephemeral and not stored in Postgres. Every socket owns one presence state keyed by connection. On close, the server removes it and rebroadcasts the room's remaining clients.

## Failure handling

- Invalid token or missing document id: upgrade is rejected.
- Unauthorized document access: upgrade is rejected.
- Malformed messages: server sends an error message and leaves the room alive.
- Flush failures: current edit state remains in memory; subsequent edits schedule another flush. Production deployments should alert on repeated failures and flush during graceful shutdown.
- Reconnects: client creates a fresh Y.Doc and receives the server snapshot. For offline-first behavior, persist client updates in IndexedDB and sync them after reconnect.
