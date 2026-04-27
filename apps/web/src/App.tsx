import { useEffect } from "react";
import { AuthPanel } from "./features/auth/AuthPanel";
import { CollaborativeEditor } from "./features/editor/CollaborativeEditor";
import { ProjectSidebar } from "./features/projects/ProjectSidebar";
import { useAuthStore } from "./store/auth";
import { useProjectStore } from "./store/projects";
import "./styles/global.css";

export default function App() {
  const { user, logout, bootstrap } = useAuthStore();
  const { projects, activeDocumentId, loadProjects, createProject, selectDocument } = useProjectStore();

  useEffect(() => {
    bootstrap();
  }, [bootstrap]);

  useEffect(() => {
    if (user) void loadProjects();
  }, [loadProjects, user]);

  const activeDocument =
    projects.flatMap((project) => project.documents).find((document) => document.id === activeDocumentId) ?? null;

  if (!user) {
    return (
      <main className="auth-shell">
        <section>
          <p className="eyebrow">Collaborative Code Editor</p>
          <h1>Code together in real time.</h1>
          <p className="muted">
            A Google Docs-style CRDT collaboration layer wrapped around a VSCode-like editing surface.
          </p>
        </section>
        <AuthPanel />
      </main>
    );
  }

  return (
    <main className="workspace">
      <header className="topbar">
        <div>
          <strong>CollabCode</strong>
          <span className="muted">Signed in as {user.name}</span>
        </div>
        <button type="button" onClick={logout}>
          Sign out
        </button>
      </header>
      <div className="workspace-grid">
        <ProjectSidebar
          projects={projects}
          activeDocumentId={activeDocumentId}
          onCreateProject={() => {
            const name = window.prompt("Project name");
            if (name) void createProject(name);
          }}
          onSelectDocument={(projectId, documentId) => selectDocument(projectId, documentId)}
        />
        <CollaborativeEditor document={activeDocument} />
      </div>
    </main>
  );
}
