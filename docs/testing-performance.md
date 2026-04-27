# Testing, Edge Cases, and Performance

## Testing strategy

- **Unit tests**: token signing/hash utilities, CRDT encoding helpers, store reducers/actions.
- **API integration tests**: auth happy paths, refresh token rotation, project/document authorization.
- **Realtime integration tests**: connect two websocket clients, apply concurrent Yjs updates, assert convergence.
- **Frontend tests**: anonymous auth screen, project selection, editor connection status, presence rendering.
- **E2E tests**: Playwright with two browser contexts editing the same document.
- **Load tests**: websocket rooms with many clients and high update frequency; track p95 broadcast latency.

Current repository tests include backend token utility coverage and a frontend auth-shell smoke test.

## Edge cases and failure handling

- Expired access token: REST client uses refresh token rotation and retries once.
- Refresh token replay: old token row is revoked and linked to the replacement hash.
- WebSocket unauthorized: server rejects upgrade with 401/403 before joining a room.
- Client disconnect: presence is removed and the room schedules a persistence flush.
- Persistence failure: later edits schedule another flush; production should alert on repeated flush failures.
- Concurrent edits: Yjs CRDT updates are commutative and idempotent, so all clients converge.
- Empty projects: frontend renders the empty editor state and lets users create a project.
- Large files: current prototype sends compact Yjs updates but Monaco still holds the full file in memory.

## Performance considerations

- Debounced persistence avoids a Postgres write per keystroke.
- The backend stores both `yState` and `plainText`; `plainText` supports fast metadata/search previews while CRDT state remains authoritative.
- Rooms are held in memory, so horizontal scaling requires sticky sessions or a pub/sub layer such as Redis/NATS for room fanout.
- Periodic snapshots cap replay cost. For very active documents, snapshot every N updates or seconds.
- Compress websocket frames at the reverse proxy or `ws` layer for large edits.
- Add per-document max size and update rate limits to protect memory and broadcast loops.
- Use Postgres indexes on memberships and document/project relationships for authorization checks.
