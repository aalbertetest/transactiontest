import type { Project } from "../../lib/types";

type Props = {
  projects: Project[];
  activeDocumentId?: string;
  onCreateProject: () => void;
  onSelectDocument: (projectId: string, documentId: string) => void;
};

export function ProjectSidebar({ projects, activeDocumentId, onCreateProject, onSelectDocument }: Props) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <h2>Projects</h2>
        <button onClick={onCreateProject}>New</button>
      </div>
      {projects.map((project) => (
        <section key={project.id} className="project-group">
          <h3>{project.name}</h3>
          {project.documents.map((document) => (
            <button
              className={document.id === activeDocumentId ? "document active" : "document"}
              key={document.id}
              onClick={() => onSelectDocument(project.id, document.id)}
            >
              <span>{document.title}</span>
              <small>{document.language}</small>
            </button>
          ))}
        </section>
      ))}
    </aside>
  );
}
