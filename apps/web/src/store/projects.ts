import { create } from "zustand";
import { api } from "../lib/api";
import type { Project } from "../lib/types";

type ProjectState = {
  projects: Project[];
  activeProjectId?: string;
  activeDocumentId?: string;
  isLoading: boolean;
  error?: string;
  loadProjects: () => Promise<void>;
  createProject: (name: string) => Promise<void>;
  selectDocument: (projectId: string, documentId: string) => void;
};

export const useProjectStore = create<ProjectState>((set, get) => ({
  projects: [],
  isLoading: false,
  async loadProjects() {
    set({ isLoading: true, error: undefined });
    try {
      const { data } = await api.get<{ projects: Project[] }>("/projects");
      const firstProject = data.projects[0];
      const firstDocument = firstProject?.documents[0];
      set({
        projects: data.projects,
        activeProjectId: get().activeProjectId ?? firstProject?.id,
        activeDocumentId: get().activeDocumentId ?? firstDocument?.id,
        isLoading: false
      });
    } catch (error) {
      set({ error: error instanceof Error ? error.message : "Failed to load projects", isLoading: false });
    }
  },
  async createProject(name) {
    const { data } = await api.post<{ project: Project }>("/projects", { name });
    set((state) => ({
      projects: [data.project, ...state.projects],
      activeProjectId: data.project.id,
      activeDocumentId: data.project.documents[0]?.id
    }));
  },
  selectDocument(projectId, documentId) {
    set({ activeProjectId: projectId, activeDocumentId: documentId });
  }
}));
