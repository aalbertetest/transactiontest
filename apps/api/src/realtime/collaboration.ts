import { parse } from "node:url";
import type { RawData, WebSocket } from "ws";
import { WebSocketServer } from "ws";
import * as Y from "yjs";
import { env } from "../config/env.js";
import type { PrismaClient } from "../generated/prisma/client.js";
import { verifyAccessToken } from "../modules/auth/tokens.js";

type AwarenessState = {
  userId: string;
  name: string;
  color: string;
  cursor?: { lineNumber: number; column: number };
};

type ClientContext = {
  socket: WebSocket;
  userId: string;
  documentId: string;
  color: string;
};

type ServerMessage =
  | { type: "sync"; update: string }
  | { type: "presence"; clients: AwarenessState[] }
  | { type: "error"; message: string };

type ClientMessage =
  | { type: "sync"; update: string }
  | { type: "presence"; cursor?: AwarenessState["cursor"] };

type CollabRoom = {
  ydoc: Y.Doc;
  clients: Map<WebSocket, AwarenessState>;
  flushTimer?: NodeJS.Timeout;
  initialized: Promise<void>;
};

const textName = "code";

export class CollaborationServer {
  private rooms = new Map<string, CollabRoom>();

  constructor(private readonly prisma: PrismaClient) {}

  attach(server: import("node:http").Server) {
    const wss = new WebSocketServer({ noServer: true });

    server.on("upgrade", async (request, socket, head) => {
      const { pathname, query } = parse(request.url ?? "", true);
      if (pathname !== "/ws/collaboration") {
        return;
      }

      const token = typeof query.token === "string" ? query.token : undefined;
      const documentId = typeof query.documentId === "string" ? query.documentId : undefined;
      const auth = this.authenticate(token);

      if (!auth?.sub || !documentId) {
        socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
        socket.destroy();
        return;
      }

      const userId: string = auth.sub;
      const canAccess = await this.canAccessDocument(userId, documentId);
      if (!canAccess) {
        socket.write("HTTP/1.1 403 Forbidden\r\n\r\n");
        socket.destroy();
        return;
      }

      wss.handleUpgrade(request, socket, head, (ws) => {
        this.handleConnection({
          socket: ws,
          userId,
          documentId,
          color: colorForUser(userId)
        }).catch((error: unknown) => {
          ws.send(JSON.stringify({ type: "error", message: "Failed to join collaboration room" } satisfies ServerMessage));
          ws.close(1011, error instanceof Error ? error.message : "Unknown collaboration error");
        });
      });
    });
  }

  private authenticate(token?: string): { sub: string } | null {
    if (!token) return null;

    try {
      const decoded = verifyAccessToken(token);
      return { sub: decoded.sub };
    } catch {
      return null;
    }
  }

  private async canAccessDocument(userId: string, documentId: string) {
    const document = await this.prisma.document.findFirst({
      where: {
        id: documentId,
        project: {
          memberships: { some: { userId } }
        }
      },
      select: { id: true }
    });

    return Boolean(document);
  }

  private async getRoom(documentId: string) {
    const existing = this.rooms.get(documentId);
    if (existing) return existing;

    const room: CollabRoom = {
      ydoc: new Y.Doc(),
      clients: new Map(),
      initialized: this.initializeDocument(documentId)
    };

    this.rooms.set(documentId, room);
    await room.initialized;
    return room;
  }

  private async initializeDocument(documentId: string) {
    const room = this.rooms.get(documentId);
    if (!room) return;

    const document = await this.prisma.document.findUniqueOrThrow({
      where: { id: documentId },
      select: { plainText: true, yState: true }
    });

    if (document.yState) {
      Y.applyUpdate(room.ydoc, new Uint8Array(document.yState));
      return;
    }

    room.ydoc.getText(textName).insert(0, document.plainText);
  }

  private async handleConnection(context: ClientContext) {
    const room = await this.getRoom(context.documentId);
    await room.initialized;

    const user = await this.prisma.user.findUniqueOrThrow({
      where: { id: context.userId },
      select: { name: true }
    });

    room.clients.set(context.socket, {
      userId: context.userId,
      name: user.name,
      color: context.color
    });

    this.send(context.socket, { type: "sync", update: encodeUpdate(Y.encodeStateAsUpdate(room.ydoc)) });
    this.broadcastPresence(room);

    context.socket.on("message", (raw) => {
      this.handleMessage(room, context, raw).catch(() => {
        this.send(context.socket, { type: "error", message: "Invalid collaboration message" });
      });
    });

    context.socket.on("close", () => {
      room.clients.delete(context.socket);
      this.broadcastPresence(room);
      this.scheduleFlush(context.documentId, room);
    });
  }

  private async handleMessage(room: CollabRoom, context: ClientContext, raw: RawData) {
    const message = JSON.parse(raw.toString()) as ClientMessage;

    if (message.type === "sync") {
      Y.applyUpdate(room.ydoc, decodeUpdate(message.update));
      this.broadcast(room, context.socket, { type: "sync", update: message.update });
      this.scheduleFlush(context.documentId, room);
      return;
    }

    if (message.type === "presence") {
      const current = room.clients.get(context.socket);
      if (!current) return;

      room.clients.set(context.socket, { ...current, cursor: message.cursor });
      this.broadcastPresence(room);
    }
  }

  private scheduleFlush(documentId: string, room: CollabRoom) {
    if (room.flushTimer) clearTimeout(room.flushTimer);

    room.flushTimer = setTimeout(() => {
      this.flushDocument(documentId, room).catch(() => {
        // A later edit will schedule another flush; process monitoring should alert on repeated failures.
      });
    }, env.documentFlushMs);
  }

  private async flushDocument(documentId: string, room: CollabRoom) {
    const ytext = room.ydoc.getText(textName);
    const state = Buffer.from(Y.encodeStateAsUpdate(room.ydoc));
    const current = await this.prisma.document.findUniqueOrThrow({
      where: { id: documentId },
      select: { version: true }
    });

    await this.prisma.document.update({
      where: { id: documentId },
      data: {
        plainText: ytext.toString(),
        yState: state,
        version: { increment: 1 },
        updatedAt: new Date(),
        snapshots: {
          create: {
            version: current.version + 1,
            yState: state,
            plainText: ytext.toString()
          }
        }
      }
    });
  }

  private send(socket: WebSocket, message: ServerMessage) {
    if (socket.readyState === socket.OPEN) {
      socket.send(JSON.stringify(message));
    }
  }

  private broadcast(room: CollabRoom, except: WebSocket, message: ServerMessage) {
    for (const socket of room.clients.keys()) {
      if (socket !== except) this.send(socket, message);
    }
  }

  private broadcastPresence(room: CollabRoom) {
    const clients = [...room.clients.values()];
    for (const socket of room.clients.keys()) {
      this.send(socket, { type: "presence", clients });
    }
  }
}

function encodeUpdate(update: Uint8Array) {
  return Buffer.from(update).toString("base64");
}

function decodeUpdate(update: string) {
  return new Uint8Array(Buffer.from(update, "base64"));
}

function colorForUser(userId: string): string {
  const palette = ["#2563eb", "#dc2626", "#16a34a", "#9333ea", "#ea580c", "#0891b2"];
  const index = [...userId].reduce((sum, char) => sum + char.charCodeAt(0), 0) % palette.length;
  return palette[index] ?? "#2563eb";
}
