# Collaborative Code Editor Architecture

## 1. High-level design

### Components

- **React web app (`apps/web`)**
  - Monaco editor provides syntax highlighting and a VSCode-like surface.
  - Zustand stores auth/session and project selection state.
  - A Yjs document mirrors the Monaco model and exchanges CRDT updates over WebSocket.
- **Node API (`apps/api`)**
  - Express handles REST APIs, rate limiting, CORS, security headers, and JSON errors.
  - JWT access tokens authenticate REST and WebSocket requests.
  - Refresh tokens are random opaque strings; only SHA-256 hashes are stored.
- **Realtime collaboration server**
  - WebSocket endpoint `/ws/collaboration`.
  - One in-memory Yjs document per active document room.
  - Broadcasts Yjs binary updates and lightweight cursor presence.
  - Debounces persistence to Postgres.
- **Postgres + Prisma**
  - Durable users, projects, memberships, documents, refresh tokens, and snapshots.
  - Documents store both `plainText` for metadata/search/read APIs and `yState` for exact CRDT recovery.

### Data flow

1. User registers/logs in through REST.
2. API returns a short-lived access token and long-lived refresh token.
3. Client loads projects/documents with `Authorization: Bearer <accessToken>`.
4. User selects a document and opens a WebSocket with `documentId` and access token.
5. Server verifies membership, loads or creates an active Yjs room from Postgres, and sends the current CRDT state.
6. Monaco edits are converted into Yjs text operations.
7. Yjs emits binary updates; the client sends base64-encoded updates to the server.
8. Server applies each update, broadcasts it to other sockets, and schedules a debounced flush.
9. Presence updates are ephemeral and broadcast only to currently connected peers.

### Scaling concerns

- The current implementation is intentionally simple: active rooms are process-local. For horizontal scaling, use sticky sessions by document ID or put a collaboration broker in front of rooms.
- For multi-instance collaboration, publish Yjs updates through Redis/NATS/Kafka so every API instance receives room changes.
- Persist snapshots periodically and compact Yjs state to keep replay costs bounded.
- Use a dedicated WebSocket deployment pool if editor traffic grows independently of REST.
- Store document content in object storage or partitioned tables if very large files are supported.

## 2. Database schema

The Prisma schema lives in `apps/api/prisma/schema.prisma`.

Key tables:

- `User`: account identity and password hash.
- `RefreshToken`: hashed refresh tokens with revocation and replacement tracking.
- `Project`: workspace container.
- `ProjectMembership`: project-level role based access control (`OWNER`, `EDITOR`, `VIEWER`).
- `Document`: metadata plus `plainText`, version, and durable Yjs CRDT state.
- `DocumentSnapshot`: append-only recovery/audit snapshots created on debounced flushes.

## 3. API design

See `docs/api.md` for route details and request/response examples.

## 4. Core backend implementation

Important backend files:

- `src/app.ts`: Express app composition and middleware.
- `src/db/prisma.ts`: Prisma client with the Prisma 7 PostgreSQL driver adapter.
- `src/modules/auth/*`: password hashing, token issuance, refresh rotation, auth routes.
- `src/modules/projects/projects.routes.ts`: project listing/creation and document creation.
- `src/modules/documents/documents.routes.ts`: document metadata and CRDT snapshot endpoints.
- `src/realtime/collaboration.ts`: WebSocket authentication, room lifecycle, Yjs update fanout, debounced persistence, presence.

## 5. Frontend structure

Important frontend files:

- `src/App.tsx`: app shell, auth gating, project/document selection.
- `src/store/auth.ts`: Zustand auth state, persisted session, refresh behavior.
- `src/store/projects.ts`: project and active document state.
- `src/features/editor/CollaborativeEditor.tsx`: Monaco editor and presence UI.
- `src/features/editor/useCollaboration.ts`: WebSocket and Yjs binding.
- `src/lib/api.ts`: Axios client and access token refresh interceptor.

## 6. Realtime sync logic

### Why CRDT over operational transform

Operational transform can be efficient and is used by systems like Google Docs, but correctness requires a central transform pipeline with strict operation ordering and careful per-operation transform functions. Code editors also need robust reconnect and offline-friendly semantics.

This app uses **Yjs**, a production-grade CRDT:

- Concurrent inserts/deletes merge deterministically.
- Updates are commutative and idempotent.
- Reconnect can be handled by exchanging state updates rather than replaying ordered operations.
- Clients can apply remote updates without a server-side transform queue.

Tradeoff: CRDT metadata increases memory/storage overhead compared with plain text plus OT operations. The implementation stores `plainText` and compact Yjs state to balance easy reads with exact collaboration recovery.

### Message protocol

Client to server:

```json
{ "type": "sync", "update": "base64-yjs-update" }
```

```json
{ "type": "presence", "cursor": { "lineNumber": 8, "column": 14 } }
```

Server to client:

```json
{ "type": "sync", "update": "base64-yjs-update" }
```

```json
{
  "type": "presence",
  "clients": [
    {
      "userId": "clx123",
      "name": "Ada",
      "color": "#2563eb",
      "cursor": { "lineNumber": 8, "column": 14 }
    }
  ]
}
```

## 7. Edge cases and failure handling

- **Expired access token:** REST requests refresh automatically; WebSockets close and require the UI to reconnect with a fresh token.
- **Refresh token replay:** refresh tokens are rotated and previous tokens are revoked.
- **Unauthorized document access:** WebSocket upgrade is rejected with `403`; REST returns `404` for missing or inaccessible resources.
- **Concurrent editing:** Yjs CRDT updates merge without server-side locks.
- **Database flush failure:** the room keeps the active in-memory state and later edits schedule another flush; production should alert on repeated failures.
- **Client disconnect:** presence is removed immediately and current room state is scheduled for persistence.
- **Malformed WebSocket message:** server sends an error message instead of crashing the room.
- **Read-only members:** REST mutation endpoints check `OWNER`/`EDITOR`; a production hardening step would also attach role checks to each sync update.
- **Large documents:** Monaco and CRDT metadata can become expensive; cap file sizes and add server-side admission controls.

## 8. Testing strategy

Implemented:

- API unit tests for JWT signing and refresh token hashing.
- Web smoke test for anonymous auth rendering.

Recommended next layers:

- Route integration tests with a disposable Postgres database.
- WebSocket multi-client tests that assert convergence after concurrent edits.
- Frontend component tests for project selection and auth refresh errors.
- E2E tests with Playwright covering login, project creation, collaborative editing, and reconnect.
- Load tests for WebSocket fanout and document flush behavior.

## 9. Performance considerations

- Debounced document persistence reduces database writes during rapid typing.
- Store latest CRDT state and plain text together to avoid reconstructing content for simple document loads.
- Use compact snapshots and scheduled Yjs state compaction for long-lived documents.
- Avoid global Redux-style rerenders for high-frequency editor updates; Monaco/Yjs state is kept outside React render state.
- Use Zustand for low-boilerplate app state where updates are coarse-grained.
- Apply websocket backpressure and message size limits before production exposure.

## 10. Local setup

See `README.md` for step-by-step commands.
