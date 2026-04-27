import { Editor, type OnMount } from "@monaco-editor/react";
import { useCallback, useEffect, useRef } from "react";
import type * as monaco from "monaco-editor";
import type { DocumentRecord } from "../../lib/types";
import { useCollaboration } from "./useCollaboration";

type Props = {
  document: DocumentRecord | null;
};

export function CollaborativeEditor({ document }: Props) {
  const editorRef = useRef<monaco.editor.IStandaloneCodeEditor | null>(null);
  const { status, peers, bindEditor, sendCursor } = useCollaboration(document?.id);

  const handleMount = useCallback<OnMount>(
    (editor) => {
      editorRef.current = editor;
      bindEditor(editor);
      editor.onDidChangeCursorPosition((event) => {
        sendCursor({
          lineNumber: event.position.lineNumber,
          column: event.position.column
        });
      });
    },
    [bindEditor, sendCursor]
  );

  useEffect(() => {
    if (editorRef.current) {
      bindEditor(editorRef.current);
    }
  }, [bindEditor, document?.id]);

  if (!document) {
    return <main className="editor-empty">Create or select a document to start collaborating.</main>;
  }

  return (
    <main className="editor-shell">
      <header className="editor-toolbar">
        <div>
          <strong>{document.title}</strong>
          <span>{document.language}</span>
        </div>
        <div className={`connection connection-${status}`}>{status}</div>
      </header>
      <div className="presence-strip">
        {peers.length === 0 ? (
          <span className="muted">No other collaborators online</span>
        ) : (
          peers.map((peer) => (
            <span key={peer.userId} className="peer-pill" style={{ borderColor: peer.color }}>
              <span style={{ background: peer.color }} />
              {peer.name}
              {peer.cursor ? ` L${peer.cursor.lineNumber}:${peer.cursor.column}` : ""}
            </span>
          ))
        )}
      </div>
      <Editor
        key={document.id}
        height="calc(100vh - 112px)"
        defaultValue={document.plainText}
        language={document.language}
        theme="vs-dark"
        options={{
          minimap: { enabled: true },
          fontSize: 14,
          tabSize: 2,
          automaticLayout: true,
          scrollBeyondLastLine: false
        }}
        onMount={handleMount}
      />
    </main>
  );
}
