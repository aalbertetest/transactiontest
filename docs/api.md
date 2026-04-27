# API design

All REST endpoints are served under `http://localhost:4000/api`. Authenticated routes require:

```http
Authorization: Bearer <accessToken>
```

Errors use:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Project name is required"
  }
}
```

## Authentication

### `POST /auth/register`

Request:

```json
{
  "name": "Ada Lovelace",
  "email": "ada@example.com",
  "password": "password123"
}
```

Response `201`:

```json
{
  "user": { "id": "clx...", "email": "ada@example.com", "name": "Ada Lovelace" },
  "accessToken": "jwt...",
  "refreshToken": "opaque-refresh-token"
}
```

### `POST /auth/login`

Request:

```json
{
  "email": "ada@example.com",
  "password": "password123"
}
```

Response `200`: same shape as register.

### `POST /auth/refresh`

Request:

```json
{
  "refreshToken": "opaque-refresh-token"
}
```

Response:

```json
{
  "accessToken": "new-jwt...",
  "refreshToken": "new-opaque-refresh-token"
}
```

Refresh tokens are rotated; the previous stored token is revoked and linked to the replacement hash.

### `POST /auth/logout`

Request:

```json
{
  "refreshToken": "opaque-refresh-token"
}
```

Response: `204 No Content`.

### `GET /auth/me`

Response:

```json
{
  "user": { "id": "clx...", "email": "ada@example.com", "name": "Ada Lovelace" }
}
```

## Projects

### `GET /projects`

Response:

```json
{
  "projects": [
    {
      "id": "project-id",
      "name": "Compiler",
      "description": "Shared project",
      "documents": [
        {
          "id": "document-id",
          "projectId": "project-id",
          "title": "main.ts",
          "language": "typescript",
          "plainText": "export function hello() {}",
          "version": 3,
          "updatedAt": "2026-04-27T00:00:00.000Z"
        }
      ]
    }
  ]
}
```

### `POST /projects`

Request:

```json
{
  "name": "Compiler",
  "description": "Shared project"
}
```

Response `201`:

```json
{
  "project": {
    "id": "project-id",
    "name": "Compiler",
    "documents": [{ "id": "document-id", "title": "main.ts" }]
  }
}
```

### `POST /projects/:projectId/documents`

Request:

```json
{
  "title": "lexer.ts",
  "language": "typescript",
  "plainText": "export const tokens = [];"
}
```

Response `201`:

```json
{
  "document": {
    "id": "document-id",
    "projectId": "project-id",
    "title": "lexer.ts",
    "language": "typescript",
    "plainText": "export const tokens = [];",
    "version": 0
  }
}
```

## Documents

### `GET /documents/:documentId`

Returns document metadata and the latest plain-text projection.

### `PATCH /documents/:documentId`

Request:

```json
{
  "title": "main.ts",
  "language": "typescript"
}
```

Response:

```json
{
  "document": {
    "id": "document-id",
    "title": "main.ts",
    "language": "typescript"
  }
}
```

### `GET /documents/:documentId/snapshot`

Returns a base64 Yjs update suitable for bootstrapping a CRDT document without opening a websocket.

Response:

```json
{
  "documentId": "document-id",
  "version": 12,
  "stateVector": "base64-state-vector",
  "update": "base64-yjs-update"
}
```

## Realtime websocket

Connect:

```text
ws://localhost:4000/ws/collaboration?documentId=<id>&token=<accessToken>
```

Client messages:

```json
{ "type": "sync", "update": "base64-yjs-update" }
```

```json
{ "type": "presence", "cursor": { "lineNumber": 12, "column": 7 } }
```

Server messages:

```json
{ "type": "sync", "update": "base64-yjs-update" }
```

```json
{
  "type": "presence",
  "clients": [
    {
      "userId": "user-id",
      "name": "Ada",
      "color": "#2563eb",
      "cursor": { "lineNumber": 12, "column": 7 }
    }
  ]
}
```

```json
{ "type": "error", "message": "Invalid collaboration message" }
```
