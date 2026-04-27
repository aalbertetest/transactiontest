import type { editor } from "monaco-editor";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import * as Y from "yjs";
import { WS_URL } from "../../lib/api";
import { useAuthStore } from "../../store/auth";

type PresenceUser = {
  userId: string;
  name: string;
  color: string;
  cursor?: { lineNumber: number; column: number };
};

type ServerMessage =
  | { type: "sync"; update: string }
  | { type: "presence"; clients: PresenceUser[] }
  | { type: "error"; message: string };

const textName = "code";

export function useCollaboration(documentId?: string) {
  const accessToken = useAuthStore((state) => state.accessToken);
  const [presence, setPresence] = useState<PresenceUser[]>([]);
  const [connectionState, setConnectionState] = useState<"idle" | "connecting" | "connected" | "offline">("idle");
  const [boundEditor, setBoundEditor] = useState<editor.IStandaloneCodeEditor | null>(null);
  const ydoc = useMemo(() => new Y.Doc(), [documentId]);
  const socketRef = useRef<WebSocket | null>(null);
  const applyingRemote = useRef(false);

  const bindEditor = useCallback((monacoEditor: editor.IStandaloneCodeEditor) => {
    setBoundEditor(monacoEditor);
  }, []);

  const sendCursor = useCallback((cursor: PresenceUser["cursor"]) => {
    const socket = socketRef.current;
    if (socket?.readyState !== WebSocket.OPEN) return;
    socket.send(JSON.stringify({ type: "presence", cursor }));
  }, []);

  useEffect(() => {
    const monacoEditor = boundEditor;
    if (!documentId || !accessToken || !monacoEditor) return;

    setConnectionState("connecting");
    const socket = new WebSocket(
      `${WS_URL}/ws/collaboration?documentId=${encodeURIComponent(documentId)}&token=${encodeURIComponent(accessToken)}`,
    );
    socketRef.current = socket;
    const ytext = ydoc.getText(textName);
    const model = monacoEditor.getModel();

    const syncModelFromYjs = () => {
      if (!model) return;
      const value = ytext.toString();
      if (model.getValue() === value) return;

      applyingRemote.current = true;
      model.pushEditOperations(
        [],
        [
          {
            range: model.getFullModelRange(),
            text: value,
          },
        ],
        () => null,
      );
      applyingRemote.current = false;
    };

    const modelDisposable = model?.onDidChangeContent((event) => {
      if (applyingRemote.current) return;

      ydoc.transact(() => {
        for (const change of [...event.changes].reverse()) {
          const start = model.getOffsetAt({
            lineNumber: change.range.startLineNumber,
            column: change.range.startColumn
          });
          const end = model.getOffsetAt({
            lineNumber: change.range.endLineNumber,
            column: change.range.endColumn
          });
          ytext.delete(start, end - start);
          ytext.insert(start, change.text);
        }
      });
    });

    const observer = (update: Uint8Array, origin: unknown) => {
      syncModelFromYjs();
      if (origin === "remote" || socket.readyState !== WebSocket.OPEN) return;
      socket.send(JSON.stringify({ type: "sync", update: bytesToBase64(update) }));
    };
    ydoc.on("update", observer);

    socket.onopen = () => setConnectionState("connected");
    socket.onclose = () => setConnectionState("offline");
    socket.onerror = () => setConnectionState("offline");
    socket.onmessage = (event) => {
      const message = JSON.parse(event.data as string) as ServerMessage;
      if (message.type === "sync") {
        Y.applyUpdate(ydoc, base64ToBytes(message.update), "remote");
      }
      if (message.type === "presence") {
        setPresence(message.clients);
      }
      if (message.type === "error") {
        console.warn(message.message);
      }
    };

    return () => {
      ydoc.off("update", observer);
      modelDisposable?.dispose();
      socket.close(1000, "component unmounted");
      socketRef.current = null;
    };
  }, [accessToken, boundEditor, documentId, ydoc]);

  return { ydoc, peers: presence, status: connectionState, bindEditor, sendCursor };
}

function bytesToBase64(update: Uint8Array) {
  let binary = "";
  update.forEach((byte) => {
    binary += String.fromCharCode(byte);
  });
  return window.btoa(binary);
}

function base64ToBytes(update: string) {
  return Uint8Array.from(window.atob(update), (char) => char.charCodeAt(0));
}
